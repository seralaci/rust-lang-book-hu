## Szabályos leállítás és takarítás {#graceful-shutdown-and-cleanup}

A 21-20. kódrészlet kódja – ahogy szerettük volna – egy szálkészlet
segítségével aszinkron módon válaszol a kérésekre. Kapunk néhány
figyelmeztetést a `workers`, `id` és `thread` mezőkre, amelyeket nem
használunk közvetlenül; ez arra emlékeztet minket, hogy semmit sem takarítunk
el. Amikor a kevésbé elegáns <kbd>ctrl</kbd>-<kbd>C</kbd> módszerrel állítjuk
le a fő szálat, az összes többi szál is azonnal leáll, még akkor is, ha épp
egy kérés kiszolgálásának közepén tart.

Ezért a következő lépésben megvalósítjuk a `Drop` traitet, hogy a készlet
minden szálán meghívjuk a `join`-t, így a szálak a leállás előtt befejezhetik
azokat a kéréseket, amelyeken éppen dolgoznak. Ezután megvalósítunk egy
módszert, amellyel jelezhetjük a szálaknak, hogy ne fogadjanak több új
kérést, és álljanak le. Hogy lássuk ezt a kódot működés közben, úgy
módosítjuk a szerverünket, hogy csak két kérést fogadjon, mielőtt szabályosan
leállítja a szálkészletét.

Egy dolgot érdemes menet közben észrevenni: mindez nem érinti a kódnak azokat
a részeit, amelyek a closure-ök végrehajtását kezelik, így minden ugyanígy
nézne ki, ha egy async futtatókörnyezethez használnánk szálkészletet.

### A `Drop` trait megvalósítása a `ThreadPool`-on {#implementing-the-drop-trait-on-threadpool}

Kezdjük azzal, hogy megvalósítjuk a `Drop`-ot a szálkészletünkön. Amikor a
készletet eldobjuk, az összes szálunknak be kell csatlakoznia (join), hogy
biztosan befejezzék a munkájukat. A 21-22. kódrészlet a `Drop` megvalósítás
első kísérletét mutatja; ez a kód még nem egészen működik.

<Listing number="21-22" file-name="src/lib.rs" caption="Minden szál bevárása, amikor a szálkészlet kikerül a hatókörből">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch21-web-server/listing-21-22/src/lib.rs:here}}
```

</Listing>

Először végigiterálunk a szálkészlet összes `workers` elemén. Ehhez a
`&mut`-ot használjuk, mert a `self` módosítható referencia, és a `worker`-t is
módosítanunk kell tudni. Minden `worker` esetén kiírunk egy üzenetet arról,
hogy az adott `Worker` példány leáll, majd meghívjuk a `join`-t az adott
`Worker` példány szálán. Ha a `join` hívása meghiúsul, az `unwrap`
segítségével pánikra késztetjük a Rustot, és nem szabályos leállás
következik.

Ezt a hibát kapjuk, amikor lefordítjuk ezt a kódot:

```console
{{#include ../listings/ch21-web-server/listing-21-22/output.txt}}
```

A hiba azt mondja, hogy nem hívhatjuk meg a `join`-t, mert minden `worker`-ből
csak módosítható kölcsönzésünk van, a `join` pedig átveszi az argumentuma
tulajdonjogát. A probléma megoldásához ki kell mozgatnunk a szálat a
`thread`-et birtokló `Worker` példányból, hogy a `join` felhasználhassa a
szálat. Ennek egyik módja, hogy ugyanazt a megközelítést alkalmazzuk, mint a
18-15. kódrészletben. Ha a `Worker` egy `Option<thread::JoinHandle<()>>`
értéket tárolna, meghívhatnánk az `Option` `take` metódusát, hogy kimozgassuk
az értéket a `Some` változatból, és egy `None` változatot hagyjunk a helyén.
Más szóval egy futó `Worker` `thread` mezőjében `Some` változat lenne, és
amikor el szeretnénk takarítani egy `Worker`-t, a `Some`-ot `None`-ra
cserélnénk, így a `Worker`-nek nem lenne futtatandó szála.

Erre azonban _csak_ a `Worker` eldobásakor lenne szükség. Cserébe mindenhol
egy `Option<thread::JoinHandle<()>>` értékkel kellene foglalkoznunk, ahol a
`worker.thread`-hez hozzáférünk. Az idiomatikus Rust elég gyakran használja
az `Option`-t, de ha azon kapod magad, hogy valamit, amiről tudod, hogy mindig
jelen lesz, ilyen kerülőmegoldásként egy `Option`-be csomagolsz, akkor
érdemes más megközelítést keresni, hogy a kódod tisztább és kevésbé
hibalehetőséges legyen.

Ebben az esetben létezik jobb megoldás: a `Vec::drain` metódus. Ez egy
tartomány paramétert vár, amely meghatározza, mely elemeket kell eltávolítani
a vektorból, és egy iterátort ad vissza ezekre az elemekre. A `..`
tartományszintaxis átadásával a vektor *összes* értékét eltávolítjuk.

A `ThreadPool` `drop` megvalósítását tehát így kell frissítenünk:

<Listing file-name="src/lib.rs">

```rust
{{#rustdoc_include ../listings/ch21-web-server/no-listing-04-update-drop-definition/src/lib.rs:here}}
```

</Listing>

Ez megszünteti a fordítási hibát, és nem igényel más módosítást a kódunkban.
Vedd észre, hogy mivel a drop pánikolás közben is meghívódhat, az unwrap is
pánikolhat, és kétszeres pánikot okozhat, ami azonnal összeomlasztja a
programot, és megszakít minden folyamatban lévő takarítást. Egy
példaprogramnál ez rendben van, de éles kódban nem ajánlott.

### Jelzés a szálaknak, hogy hagyják abba a feladatok figyelését {#signaling-to-the-threads-to-stop-listening-for-jobs}

Az eddigi módosításokkal a kódunk figyelmeztetések nélkül lefordul. A rossz
hír viszont az, hogy ez a kód még nem úgy működik, ahogy szeretnénk. A kulcs
a `Worker` példányok szálai által futtatott closure-ök logikája: jelenleg
meghívjuk a `join`-t, de ez nem állítja le a szálakat, mert azok a `loop`
miatt a végtelenségig feladatokat keresnek. Ha a `drop` jelenlegi
megvalósításával próbálnánk eldobni a `ThreadPool`-t, a fő szál örökre
blokkolna, és arra várna, hogy az első szál befejeződjön.

A probléma megoldásához módosítanunk kell a `ThreadPool` `drop`
megvalósítását, majd a `Worker` ciklusát is.

Először úgy módosítjuk a `ThreadPool` `drop` megvalósítását, hogy
kifejezetten eldobja a `sender`-t, mielőtt megvárná a szálak befejeződését. A
21-23. kódrészlet mutatja a `ThreadPool` módosításait, amelyekkel kifejezetten
eldobjuk a `sender`-t. A szállal ellentétben itt _valóban_ szükségünk van egy
`Option`-re, hogy az `Option::take` segítségével kimozgathassuk a `sender`-t a
`ThreadPool`-ból.

<Listing number="21-23" file-name="src/lib.rs" caption="A `sender` kifejezett eldobása a `Worker` szálak bevárása előtt">

```rust,noplayground,not_desired_behavior
{{#rustdoc_include ../listings/ch21-web-server/listing-21-23/src/lib.rs:here}}
```

</Listing>

A `sender` eldobása lezárja a csatornát, ami azt jelzi, hogy több üzenet nem
érkezik. Amikor ez megtörténik, a `Worker` példányok végtelen ciklusában
végzett összes `recv` hívás hibát ad vissza. A 21-24. kódrészletben úgy
módosítjuk a `Worker` ciklusát, hogy ebben az esetben szabályosan kilépjen a
ciklusból, ami azt jelenti, hogy a szálak befejeződnek, amikor a `ThreadPool`
`drop` megvalósítása meghívja rajtuk a `join`-t.

<Listing number="21-24" file-name="src/lib.rs" caption="Kifejezett kilépés a ciklusból, ha a `recv` hibát ad vissza">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-24/src/lib.rs:here}}
```

</Listing>

Hogy lássuk ezt a kódot működés közben, módosítsuk a `main`-t úgy, hogy csak
két kérést fogadjon, mielőtt szabályosan leállítja a szervert, ahogy a 21-25.
kódrészlet mutatja.

<Listing number="21-25" file-name="src/main.rs" caption="A szerver leállítása két kérés kiszolgálása után a ciklusból való kilépéssel">

```rust,ignore
{{#rustdoc_include ../listings/ch21-web-server/listing-21-25/src/main.rs:here}}
```

</Listing>

Egy valódi webszervertől nem várnád, hogy mindössze két kérés kiszolgálása
után leálljon. Ez a kód csak azt mutatja be, hogy a szabályos leállítás és a
takarítás működik.

A `take` metódus az `Iterator` traitben van definiálva, és legfeljebb az első
két elemre korlátozza az iterációt. A `ThreadPool` a `main` végén kikerül a
hatókörből, és lefut a `drop` megvalósítás.

Indítsd el a szervert a `cargo run` paranccsal, és küldj három kérést. A
harmadik kérésnek hibával kell végződnie, a terminálodban pedig ehhez hasonló
kimenetet kell látnod:

<!-- manual-regeneration
cd listings/ch21-web-server/listing-21-25
cargo run
curl http://127.0.0.1:7878
curl http://127.0.0.1:7878
curl http://127.0.0.1:7878
third request will error because server will have shut down
copy output below
Can't automate because the output depends on making requests
-->

```console
$ cargo run
   Compiling hello v0.1.0 (file:///projects/hello)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.41s
     Running `target/debug/hello`
Worker 0 got a job; executing.
Shutting down.
Shutting down worker 0
Worker 3 got a job; executing.
Worker 1 disconnected; shutting down.
Worker 2 disconnected; shutting down.
Worker 3 disconnected; shutting down.
Worker 0 disconnected; shutting down.
Shutting down worker 1
Shutting down worker 2
Shutting down worker 3
```

Előfordulhat, hogy a `Worker` azonosítók és az üzenetek más sorrendben
íródnak ki. Az üzenetekből láthatjuk, hogyan működik ez a kód: az első két
kérést a 0-s és a 3-as `Worker` példány kapta. A szerver a második kapcsolat
után nem fogadott több kapcsolatot, és a `ThreadPool` `Drop` megvalósítása
már azelőtt elkezd lefutni, hogy a `Worker 3` egyáltalán hozzákezdene a
feladatához. A `sender` eldobása az összes `Worker` példányt lecsatlakoztatja,
és jelzi nekik, hogy álljanak le. A `Worker` példányok mindegyike kiír egy
üzenetet, amikor lecsatlakozik, majd a szálkészlet meghívja a `join`-t, hogy
megvárja az egyes `Worker` szálak befejeződését.

Figyeld meg ennek a konkrét futásnak egy érdekes vonását: a `ThreadPool`
eldobta a `sender`-t, és mielőtt bármelyik `Worker` hibát kapott volna,
megpróbáltuk bevárni a `Worker 0`-t. A `Worker 0` még nem kapott
hibát a `recv`-től, így a fő szál blokkolt, és várta, hogy a `Worker 0`
befejeződjön. Közben a `Worker 3` kapott egy feladatot, majd az összes szál
hibát kapott. Amikor a `Worker 0` befejeződött, a fő szál megvárta, hogy a
többi `Worker` példány is befejeződjön. Ekkorra már mindegyik kilépett a
ciklusából, és leállt.

Gratulálunk! Befejeztük a projektünket: van egy alapvető webszerverünk, amely
szálkészlet segítségével, aszinkron módon válaszol. Képesek vagyunk a szerver
szabályos leállítására, amely a készlet összes szálát eltakarítja.

Íme a teljes kód referenciaként:

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch21-web-server/no-listing-07-final-code/src/main.rs}}
```

</Listing>

<Listing file-name="src/lib.rs">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/no-listing-07-final-code/src/lib.rs}}
```

</Listing>

Még sok mindent tehetnénk! Ha tovább szeretnéd fejleszteni ezt a projektet,
íme néhány ötlet:

- Bővítsd a `ThreadPool` és nyilvános metódusai dokumentációját.
- Írj teszteket a könyvtár funkcióihoz.
- Cseréld le az `unwrap` hívásokat robusztusabb hibakezelésre.
- Használd a `ThreadPool`-t valamilyen más feladat elvégzésére, mint a webes
  kérések kiszolgálása.
- Keress egy szálkészlet-crate-et a [crates.io](https://crates.io/) oldalon,
  és valósíts meg vele egy hasonló webszervert. Ezután vesd össze az API-ját
  és a robusztusságát az általunk megvalósított szálkészletével.

## Összefoglalás {#summary}

Szép munka! Eljutottál a könyv végére! Szeretnénk megköszönni, hogy velünk
tartottál a Rust megismerésének útján. Most már készen állsz arra, hogy
megvalósítsd a saját Rust-projektjeidet, és segíts mások projektjeiben. Ne
feledd, hogy a rustaceanek barátságos közössége szívesen segít bármilyen
kihívásban, amellyel a Rust-utazásod során találkozol.
