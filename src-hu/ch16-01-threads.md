## Kód egyidejű futtatása szálakkal {#using-threads-to-run-code-simultaneously}

A legtöbb mai operációs rendszerben egy elindított program kódja egy
_folyamatban (process)_ fut, és az operációs rendszer egyszerre több
folyamatot kezel. Egy programon belül is lehetnek egymástól független részek,
amelyek egyidejűleg futnak. Az ezeket a független részeket futtató
mechanizmusokat _szálaknak (threads)_ nevezzük. Egy webszervernek például
lehet több szála, hogy egyszerre több kérésre is válaszolni tudjon.

Ha a program számítását több szálra bontod, hogy egyszerre több feladatot
futtass, javulhat a teljesítmény, de a bonyolultság is nő. Mivel a szálak
egyidejűleg futhatnak, semmi sem garantálja eleve, hogy a kódod különböző
szálakon lévő részei milyen sorrendben futnak le. Ez olyan problémákhoz
vezethet, mint például:

- Versenyhelyzetek (race conditions), amelyekben a szálak következetlen
  sorrendben férnek hozzá adatokhoz vagy erőforrásokhoz
- Holtpontok (deadlocks), amelyekben két szál egymásra vár, és így egyikük sem
  tud továbbhaladni
- Olyan hibák, amelyek csak bizonyos helyzetekben jelentkeznek, és nehéz őket
  megbízhatóan reprodukálni és kijavítani

A Rust igyekszik mérsékelni a szálak használatának negatív hatásait, de a
többszálú környezetben való programozás továbbra is alapos átgondolást
igényel, és más kódszerkezetet kíván, mint az egyetlen szálon futó programok.

A programozási nyelvek többféleképpen valósítják meg a szálakat, és sok
operációs rendszer biztosít olyan API-t, amelyet a programozási nyelv új
szálak létrehozásához meghívhat. A Rust standard könyvtára a szálak
_1:1_ modelljét használja, amelyben a program minden nyelvi szálhoz egy
operációsrendszer-szálat használ. Vannak crate-ek, amelyek a szálkezelés más
modelljeit valósítják meg, és az 1:1 modellhez képest más kompromisszumokat
kötnek. (A Rust async rendszere, amelyet a következő fejezetben látunk majd,
szintén egy másik megközelítést kínál a konkurenciához.)

### Új szál létrehozása a `spawn` segítségével {#creating-a-new-thread-with-spawn}

Új szál létrehozásához meghívjuk a `thread::spawn` függvényt, és átadunk neki
egy closure-t (a closure-ökről a 13. fejezetben beszéltünk), amely az új
szálon futtatni kívánt kódot tartalmazza. A 16-1. kódrészlet példája egy
fő szálról ír ki valamilyen szöveget, egy új szálról pedig egy másikat.

<Listing number="16-1" file-name="src/main.rs" caption="Új szál létrehozása, amely kiír valamit, miközben a fő szál valami mást ír ki">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-01/src/main.rs}}
```

</Listing>

Figyeld meg, hogy amikor egy Rust-program fő szála befejeződik, az összes
elindított szál leáll, akár végzett már a futással, akár nem. A program
kimenete minden alkalommal kicsit eltérhet, de nagyjából így fog kinézni:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the main thread!
hi number 1 from the spawned thread!
hi number 2 from the main thread!
hi number 2 from the spawned thread!
hi number 3 from the main thread!
hi number 3 from the spawned thread!
hi number 4 from the main thread!
hi number 4 from the spawned thread!
hi number 5 from the spawned thread!
```

A `thread::sleep` hívások arra kényszerítik a szálat, hogy rövid időre
felfüggessze a futását, így egy másik szál futhat. A szálak valószínűleg
felváltva futnak majd, de ez nem garantált: attól függ, hogyan ütemezi az
operációs rendszered a szálakat. Ebben a futtatásban a fő szál írt ki először,
pedig az elindított szál kiíró utasítása szerepel előbb a kódban. És bár azt
mondtuk az elindított szálnak, hogy addig írjon ki, amíg `i` el nem éri a
`9`-et, csak az `5`-ig jutott, mielőtt a fő szál leállt.

Ha a kód futtatásakor csak a fő szál kimenetét látod, vagy nem látsz
átfedést, próbáld megnövelni a tartományokban szereplő számokat, hogy az
operációs rendszernek több lehetősége legyen a szálak közötti váltásra.

<!-- Old headings. Do not remove or links may break. -->

<a id="waiting-for-all-threads-to-finish-using-join-handles"></a>

### Várakozás az összes szál befejeződésére {#waiting-for-all-threads-to-finish}

A 16-1. kódrészlet kódja nemcsak hogy a legtöbbször idő előtt leállítja az
elindított szálat a fő szál befejeződése miatt, hanem mivel semmi sem
garantálja a szálak futási sorrendjét, azt sem tudjuk garantálni, hogy az
elindított szál egyáltalán lefut-e!

Azt a problémát, hogy az elindított szál nem fut le, vagy idő előtt
befejeződik, úgy oldhatjuk meg, hogy a `thread::spawn` visszatérési értékét
egy változóba mentjük. A `thread::spawn` visszatérési típusa
`JoinHandle<T>`. A `JoinHandle<T>` egy saját tulajdonú érték, amely – ha
meghívjuk rajta a `join` metódust – megvárja, hogy a szála befejeződjön. A
16-2. kódrészlet bemutatja, hogyan használhatjuk a 16-1. kódrészletben
létrehozott szál `JoinHandle<T>` értékét, és hogyan hívhatjuk meg a `join`
metódust, hogy biztosítsuk, hogy az elindított szál a `main` kilépése előtt
befejeződjön.

<Listing number="16-2" file-name="src/main.rs" caption="A `thread::spawn` által visszaadott `JoinHandle<T>` elmentése, hogy garantáljuk a szál végigfutását">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-02/src/main.rs}}
```

</Listing>

Ha a leírón meghívjuk a `join` metódust, az blokkolja az éppen futó szálat,
amíg a leíró által képviselt szál be nem fejeződik. Egy szál _blokkolása
(blocking)_ azt jelenti, hogy a szál nem végezhet munkát, és ki sem léphet.
Mivel a `join` hívását a fő szál `for` ciklusa után helyeztük el, a 16-2.
kódrészlet futtatása ehhez hasonló kimenetet ad:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the main thread!
hi number 2 from the main thread!
hi number 1 from the spawned thread!
hi number 3 from the main thread!
hi number 2 from the spawned thread!
hi number 4 from the main thread!
hi number 3 from the spawned thread!
hi number 4 from the spawned thread!
hi number 5 from the spawned thread!
hi number 6 from the spawned thread!
hi number 7 from the spawned thread!
hi number 8 from the spawned thread!
hi number 9 from the spawned thread!
```

A két szál továbbra is felváltva fut, de a fő szál a `handle.join()` hívás
miatt vár, és nem fejeződik be, amíg az elindított szál nem végzett.

Nézzük meg viszont, mi történik, ha a `handle.join()` hívást a `main`-beli
`for` ciklus elé helyezzük, így:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/no-listing-01-join-too-early/src/main.rs}}
```

</Listing>

A fő szál megvárja, hogy az elindított szál befejeződjön, és csak utána
futtatja a saját `for` ciklusát, így a kimenet már nem keveredik, ahogy itt
látható:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the spawned thread!
hi number 2 from the spawned thread!
hi number 3 from the spawned thread!
hi number 4 from the spawned thread!
hi number 5 from the spawned thread!
hi number 6 from the spawned thread!
hi number 7 from the spawned thread!
hi number 8 from the spawned thread!
hi number 9 from the spawned thread!
hi number 1 from the main thread!
hi number 2 from the main thread!
hi number 3 from the main thread!
hi number 4 from the main thread!
```

Az olyan apró részletek, mint hogy hol hívjuk meg a `join` metódust,
befolyásolhatják, hogy a szálaid egy időben futnak-e.

### `move` closure-ök használata szálakkal {#using-move-closures-with-threads}

A `thread::spawn` függvénynek átadott closure-öknél gyakran használjuk a
`move` kulcsszót, mert így a closure átveszi a környezetéből használt értékek
tulajdonjogát, és ezzel ezeknek az értékeknek a tulajdonjoga az egyik szálról
a másikra kerül át. A 13. fejezet [„Referenciák elkapása vagy a tulajdonjog
átmozgatása”][capture]<!-- ignore --> részében a `move` kulcsszót a closure-ök
kontextusában tárgyaltuk. Most inkább a `move` és a `thread::spawn`
kölcsönhatására összpontosítunk.

Figyeld meg, hogy a 16-1. kódrészletben a `thread::spawn` függvénynek átadott
closure nem vár argumentumot: az elindított szál kódjában nem használunk
adatot a fő szálból. Ahhoz, hogy a fő szál adatait az elindított szálban
használjuk, az elindított szál closure-jének el kell kapnia a szükséges
értékeket. A 16-3. kódrészlet egy kísérletet mutat arra, hogy a fő szálban
létrehozzunk egy vektort, és az elindított szálban használjuk. Ez azonban,
ahogy mindjárt látni fogod, még nem működik.

<Listing number="16-3" file-name="src/main.rs" caption="Kísérlet a fő szál által létrehozott vektor használatára egy másik szálban">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-03/src/main.rs}}
```

</Listing>

A closure használja a `v`-t, ezért elkapja azt, és a closure környezetének
részévé teszi. Mivel a `thread::spawn` ezt a closure-t egy új szálon futtatja,
elvileg hozzá kellene tudnunk férni a `v`-hez az új szálon belül. Amikor
azonban lefordítjuk a példát, a következő hibát kapjuk:

```console
{{#include ../listings/ch16-fearless-concurrency/listing-16-03/output.txt}}
```

A Rust _kikövetkezteti_, hogyan kapja el a `v`-t, és mivel a `println!`
makrónak csak egy referenciára van szüksége a `v`-re, a closure megpróbálja
kölcsönvenni a `v`-t. Van azonban egy probléma: a Rust nem tudja megállapítani,
meddig fog futni az elindított szál, így azt sem tudja, hogy a `v`-re mutató
referencia mindig érvényes lesz-e.

A 16-4. kódrészlet egy olyan helyzetet mutat, amelyben még valószínűbb, hogy a
`v`-re mutató referencia érvénytelen lesz.

<Listing number="16-4" file-name="src/main.rs" caption="Egy szál olyan closure-rel, amely megpróbál elkapni egy referenciát a `v`-re egy olyan fő szálból, amely eldobja a `v`-t">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-04/src/main.rs}}
```

</Listing>

Ha a Rust megengedné ennek a kódnak a futtatását, előfordulhatna, hogy az
elindított szál azonnal a háttérbe kerül, és egyáltalán nem fut. Az elindított
szálon belül van egy referencia a `v`-re, a fő szál viszont azonnal eldobja a
`v`-t a 15. fejezetben tárgyalt `drop` függvénnyel. Amikor aztán az elindított
szál elkezd futni, a `v` már nem érvényes, így a rá mutató referencia sem az.
Jaj, ne!

A 16-3. kódrészlet fordítási hibájának kijavításához megfogadhatjuk a
hibaüzenet tanácsát:

<!-- manual-regeneration
after automatic regeneration, look at listings/ch16-fearless-concurrency/listing-16-03/output.txt and copy the relevant part
-->

```text
help: to force the closure to take ownership of `v` (and any other referenced variables), use the `move` keyword
  |
6 |     let handle = thread::spawn(move || {
  |                                ++++
```

Ha a closure elé kiírjuk a `move` kulcsszót, arra kényszerítjük a closure-t,
hogy átvegye az általa használt értékek tulajdonjogát, ahelyett, hogy hagynánk
a Rustot kikövetkeztetni, hogy kölcsön kell vennie az értékeket. A 16-3.
kódrészletnek a 16-5. kódrészletben látható módosítása lefordul, és úgy fut,
ahogy szeretnénk.

<Listing number="16-5" file-name="src/main.rs" caption="A `move` kulcsszó használata, hogy a closure kénytelen legyen átvenni az általa használt értékek tulajdonjogát">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-05/src/main.rs}}
```

</Listing>

Csábító lehet ugyanezzel próbálkozni a 16-4. kódrészlet kódjának javításánál,
ahol a fő szál meghívta a `drop` függvényt, vagyis `move` closure-t
használni. Ez a javítás azonban nem működik, mert amit a 16-4. kódrészlet
megpróbál, az más okból tiltott. Ha a closure-höz hozzáadnánk a `move`
kulcsszót, a `v`-t a closure környezetébe mozgatnánk, és a fő szálban többé
nem hívhatnánk meg rá a `drop` függvényt. Ehelyett ezt a fordítási hibát
kapnánk:

```console
{{#include ../listings/ch16-fearless-concurrency/output-only-01-move-drop/output.txt}}
```

A Rust tulajdonjogi szabályai ismét megmentettek minket! A 16-3. kódrészlet
kódjára azért kaptunk hibát, mert a Rust óvatos volt, és csak kölcsönvette a
`v`-t a szál számára, ami azt jelentette, hogy a fő szál elméletileg
érvényteleníthette volna az elindított szál referenciáját. Azzal, hogy
megmondjuk a Rustnak, hogy a `v` tulajdonjogát mozgassa át az elindított
szálba, garantáljuk a Rustnak, hogy a fő szál többé nem használja a `v`-t. Ha
a 16-4. kódrészletet ugyanígy módosítjuk, akkor megsértjük a tulajdonjogi
szabályokat, amikor a fő szálban megpróbáljuk használni a `v`-t. A `move`
kulcsszó felülírja a Rust óvatos alapértelmezését, a kölcsönzést; azt viszont
nem engedi, hogy megsértsük a tulajdonjogi szabályokat.

Most, hogy áttekintettük, mik a szálak, és milyen metódusokat kínál a
szálkezelő API, nézzünk meg néhány helyzetet, amelyben szálakat
használhatunk.

[capture]: ch13-01-closures.html#capturing-references-or-moving-ownership
