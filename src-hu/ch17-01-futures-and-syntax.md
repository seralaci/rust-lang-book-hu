## Future-ök és az async szintaxis {#futures-and-the-async-syntax}

Az aszinkron programozás kulcselemei a Rustban a _future-ök (futures)_,
valamint a Rust `async` és `await` kulcsszavai.

A _future_ olyan érték, amely most még nem feltétlenül áll készen, de a jövőben
valamikor készen fog állni. (Ugyanez a fogalom sok nyelvben megjelenik, néha
más néven, például _task_ vagy _promise_ néven.) A Rust építőelemként egy
`Future` traitet biztosít, hogy a különböző aszinkron műveleteket különböző
adatszerkezetekkel, de közös interfésszel lehessen megvalósítani. A Rustban a
future-ök olyan típusok, amelyek megvalósítják a `Future` traitet. Minden
future maga tárolja az információt arról, hogy mennyit haladt eddig, és mit
jelent számára a „kész” állapot.

Az `async` kulcsszót blokkokra és függvényekre alkalmazhatod, jelezve, hogy
azok megszakíthatók és folytathatók. Egy async blokkon vagy async függvényen
belül az `await` kulcsszóval _bevárhatsz egy future-t (await a future)_
(vagyis megvárhatod, amíg készen áll). Minden pont, ahol egy async blokkon vagy
függvényen belül bevársz egy future-t, olyan lehetséges hely, ahol a blokk vagy
függvény megállhat, majd folytatódhat. Azt a folyamatot, amikor egy future-nél
ellenőrizzük, hogy elérhető-e már az értéke, _lekérdezésnek (polling)_ nevezzük.

Néhány más nyelv, például a C# és a JavaScript, szintén `async` és `await`
kulcsszavakat használ az aszinkron programozáshoz. Ha ismered ezeket a
nyelveket, észrevehetsz néhány jelentős különbséget abban, ahogyan a Rust a
szintaxist kezeli. Ennek jó oka van, ahogy látni fogjuk!

Async Rust kód írásakor legtöbbször az `async` és az `await` kulcsszót
használjuk. A Rust ezeket a `Future` traitet használó, egyenértékű kóddá
fordítja le, hasonlóan ahhoz, ahogyan a `for` ciklusokat az `Iterator` traitet
használó, egyenértékű kóddá fordítja. Mivel azonban a Rust biztosítja a
`Future` traitet, szükség esetén a saját adattípusaidra is megvalósíthatod. A
fejezetben látott függvények közül sok olyan típust ad vissza, amely saját
`Future`-megvalósítással rendelkezik. A fejezet végén visszatérünk a trait
definíciójához, és alaposabban megvizsgáljuk, hogyan működik, de egyelőre ennyi
részlet elég ahhoz, hogy továbbhaladjunk.

Mindez kissé elvontnak tűnhet, ezért írjuk meg az első async programunkat: egy
kis webkaparót (web scraper). Két URL-t adunk át a parancssorból, mindkettőt
konkurensen lekérjük, és annak az eredményét adjuk vissza, amelyik előbb
végez. Ebben a példában elég sok új szintaxis lesz, de ne aggódj – menet közben
mindent elmagyarázunk, amit tudnod kell.

## Az első async programunk {#our-first-async-program}

Hogy ebben a fejezetben az async megtanulására koncentrálhassunk, és ne az
ökoszisztéma különböző részeivel kelljen bajlódnunk, létrehoztuk a `trpl`
crate-et (a `trpl` a „The Rust Programming Language” rövidítése). Ez
újraexportálja az összes típust, traitet és függvényt, amelyre szükséged lesz,
elsősorban a [`futures`][futures-crate]<!-- ignore --> és a
[`tokio`][tokio]<!-- ignore --> crate-ből. A `futures` crate az async kóddal
kapcsolatos Rust-kísérletezés hivatalos otthona, és valójában itt tervezték meg
eredetileg a `Future` traitet. A Tokio ma a legszélesebb körben használt
aszinkron futtatókörnyezet a Rustban, különösen webalkalmazásokhoz. Vannak más
kiváló futtatókörnyezetek is, és ezek a te céljaidra akár alkalmasabbak is
lehetnek. Mi a `trpl` hátterében a `tokio` crate-et használjuk, mert jól
tesztelt és széles körben használt.

Néhány esetben a `trpl` át is nevezi vagy be is burkolja az eredeti API-kat,
hogy a fejezet szempontjából lényeges részletekre koncentrálhass. Ha meg
szeretnéd érteni, mit csinál a crate, javasoljuk, hogy nézd meg a
[forráskódját][crate-source]. Láthatod, hogy az egyes újraexportált elemek
melyik crate-ből származnak, és bőséges kommenteket is hagytunk, amelyek
elmagyarázzák, mit csinál a crate.

Hozz létre egy új, `hello-async` nevű bináris projektet, és add hozzá
függőségként a `trpl` crate-et:

```console
$ cargo new hello-async
$ cd hello-async
$ cargo add trpl
```

Most már használhatjuk a `trpl` által biztosított különböző elemeket az első
async programunk megírásához. Egy kis parancssori eszközt készítünk, amely
lekér két weboldalt, mindegyikből kiveszi a `<title>` elemet, és kiírja
annak az oldalnak a címét, amelyik előbb végez ezzel a teljes folyamattal.

### A page_title függvény definiálása {#defining-the-page_title-function}

Kezdjük egy olyan függvény megírásával, amely paraméterként egy oldal URL-jét
kapja, kérést küld neki, és visszaadja a `<title>` elem szövegét (lásd a 17-1.
kódrészletet).

<Listing number="17-1" file-name="src/main.rs" caption="Async függvény definiálása, amely lekéri egy HTML-oldal title elemét">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-01/src/main.rs:all}}
```

</Listing>

Először definiálunk egy `page_title` nevű függvényt, és megjelöljük az `async`
kulcsszóval. Ezután a `trpl::get` függvénnyel lekérjük az átadott URL-t, és az
`await` kulcsszóval bevárjuk a választ. A `response` szövegének lekéréséhez
meghívjuk a `text` metódusát, és ismét bevárjuk az `await` kulcsszóval.
Mindkét lépés aszinkron. A `get` függvénynél meg kell várnunk, hogy a szerver
visszaküldje a válaszának első részét, amely HTTP-fejléceket, sütiket és
hasonlókat tartalmaz, és a válasz törzsétől külön is megérkezhet. Különösen ha
a törzs nagyon nagy, eltarthat egy ideig, amíg teljesen megérkezik. Mivel meg
kell várnunk, hogy a válasz _teljes egészében_ megérkezzen, a `text` metódus is
aszinkron.

Mindkét future-t kifejezetten be kell várnunk, mert a Rustban a future-ök
_lusták (lazy)_: semmit sem csinálnak, amíg az `await` kulcsszóval meg nem
kérjük őket rá. (Valójában a Rust fordítói figyelmeztetést ad, ha nem használsz
fel egy future-t.) Ez emlékeztethet az iterátorokról szóló megbeszélésre a 13.
fejezet
[„Elemsorozatok feldolgozása iterátorokkal”][iterators-lazy]<!-- ignore -->
című részében. Az iterátorok semmit sem csinálnak, hacsak meg nem hívod a
`next` metódusukat – akár közvetlenül, akár `for` ciklusokkal vagy olyan
metódusokkal, mint a `map`, amelyek a háttérben a `next`-et használják.
Ugyanígy a future-ök sem csinálnak semmit, hacsak kifejezetten meg nem kéred
őket rá. Ez a lustaság lehetővé teszi, hogy a Rust ne futtassa az async kódot,
amíg ténylegesen nincs rá szükség.

> Megjegyzés: Ez eltér attól a viselkedéstől, amelyet a `thread::spawn`
> használatakor láttunk a 16. fejezet
> [„Új szál létrehozása a `spawn` segítségével”][thread-spawn]<!-- ignore -->
> című részében, ahol a másik szálnak átadott closure azonnal elkezdett futni.
> Eltér attól is, ahogyan sok más nyelv az asynchoz viszonyul. A Rust számára
> azonban fontos, hogy biztosítani tudja a teljesítménygaranciáit, ugyanúgy,
> ahogy az iterátoroknál is.

Amint megvan a `response_text`, az `Html::parse` segítségével egy `Html`
típusú példánnyá elemezhetjük. Nyers sztring helyett most már egy olyan
adattípusunk van, amellyel a HTML-t gazdagabb adatszerkezetként kezelhetjük.
Különösen a `select_first` metódussal megkereshetjük egy adott CSS-szelektor
első előfordulását. A `"title"` sztringet átadva a dokumentum első `<title>`
elemét kapjuk meg, ha van ilyen. Mivel lehet, hogy egyetlen illeszkedő elem
sincs, a `select_first` egy `Option<ElementRef>` értéket ad vissza. Végül az
`Option::map` metódust használjuk, amellyel dolgozhatunk az `Option`-ben lévő
elemmel, ha van ilyen, és nem csinálunk semmit, ha nincs. (Itt egy `match`
kifejezést is használhatnánk, de a `map` idiomatikusabb.) A `map`-nek átadott
függvény törzsében meghívjuk az `inner_html`-t a `title`-ön, hogy megkapjuk a
tartalmát, amely egy `String`. Végeredményben egy `Option<String>` értékünk
lesz.

Figyeld meg, hogy a Rust `await` kulcsszava a bevárt kifejezés _után_ áll, nem
előtte. Vagyis ez egy _utótag (postfix)_ kulcsszó. Ez eltérhet attól, amit
megszoktál, ha más nyelvekben használtad már az `async`-et, de a Rustban így
sokkal kényelmesebb a metódusláncokkal dolgozni. Ennek eredményeként a
`page_title` törzsét úgy is módosíthatnánk, hogy a `trpl::get` és a `text`
függvényhívást láncoljuk, köztük az `await`-tel, ahogy a 17-2. kódrészlet
mutatja.

<Listing number="17-2" file-name="src/main.rs" caption="Láncolás az `await` kulcsszóval">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-02/src/main.rs:chaining}}
```

</Listing>

Ezzel sikeresen megírtuk az első async függvényünket! Mielőtt a `main`-be
kódot írnánk a meghívásához, beszéljünk még egy kicsit arról, mit írtunk, és mit
jelent.

Amikor a Rust egy `async` kulcsszóval megjelölt _blokkot_ lát, egy egyedi,
névtelen adattípussá fordítja le, amely megvalósítja a `Future` traitet. Amikor
a Rust egy `async`-kel megjelölt _függvényt_ lát, egy nem async függvénnyé
fordítja le, amelynek a törzse egy async blokk. Egy async függvény visszatérési
típusa az a névtelen adattípus, amelyet a fordító az adott async blokkhoz
létrehoz.

Az `async fn` megírása tehát egyenértékű egy olyan függvény megírásával, amely
a visszatérési típus egy _future_-jét adja vissza. A fordító számára egy olyan
függvénydefiníció, mint a 17-1. kódrészletben lévő `async fn page_title`,
nagyjából egyenértékű egy így definiált, nem async függvénnyel:

```rust
# extern crate trpl; // required for mdbook test
use std::future::Future;
use trpl::Html;

fn page_title(url: &str) -> impl Future<Output = Option<String>> {
    async move {
        let text = trpl::get(url).await.text().await;
        Html::parse(&text)
            .select_first("title")
            .map(|title| title.inner_html())
    }
}
```

Nézzük végig az átalakított változat egyes részeit:

- A 10. fejezet [„Traitek használata paraméterként”][impl-trait]<!-- ignore -->
  című részében tárgyalt `impl Trait` szintaxist használja.
- A visszaadott érték megvalósítja a `Future` traitet egy `Output` társított
  típussal. Figyeld meg, hogy az `Output` típus `Option<String>`, ami
  megegyezik a `page_title` `async fn` változatának eredeti visszatérési
  típusával.
- Az eredeti függvény törzsében hívott összes kód egy `async move` blokkba van
  burkolva. Ne feledd, hogy a blokkok kifejezések. Ez a teljes blokk a
  függvényből visszaadott kifejezés.
- Ez az async blokk egy `Option<String>` típusú értéket állít elő, ahogy az
  imént leírtuk. Ez az érték illeszkedik a visszatérési típusban szereplő
  `Output` típushoz. Ez pontosan olyan, mint a többi blokk, amelyet már láttál.
- Az új függvénytörzs azért `async move` blokk, mert így használja az `url`
  paramétert. (Az `async` és az `async move` különbségéről a fejezet későbbi
  részében még sokkal többet beszélünk.)

Most már meghívhatjuk a `page_title`-t a `main`-ben.

<!-- Old headings. Do not remove or links may break. -->

<a id ="determining-a-single-pages-title"></a>

### Async függvény végrehajtása futtatókörnyezettel {#executing-an-async-function-with-a-runtime}

Kezdetnek egyetlen oldal címét kérjük le, ahogy a 17-3. kódrészlet mutatja.
Sajnos ez a kód még nem fordul le.

<Listing number="17-3" file-name="src/main.rs" caption="A `page_title` függvény meghívása a `main`-ből egy felhasználó által megadott argumentummal">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-03/src/main.rs:main}}
```

</Listing>

Ugyanazt a mintát követjük, amelyet a parancssori argumentumok lekéréséhez
használtunk a 12. fejezet
[„Parancssori argumentumok fogadása”][cli-args]<!-- ignore --> című részében.
Ezután átadjuk az URL-argumentumot a `page_title`-nek, és bevárjuk az
eredményt. Mivel a future által előállított érték `Option<String>`, egy `match`
kifejezéssel különböző üzeneteket írunk ki attól függően, hogy volt-e az
oldalnak `<title>` eleme.

Az `await` kulcsszót csak async függvényekben vagy blokkokban használhatjuk, a
Rust pedig nem engedi, hogy a különleges `main` függvényt `async`-ként
jelöljük meg.

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-03
cargo build
copy just the compiler error
-->

```text
error[E0752]: `main` function is not allowed to be `async`
 --> src/main.rs:6:1
  |
6 | async fn main() {
  | ^^^^^^^^^^^^^^^ `main` function is not allowed to be `async`
```

A `main` azért nem jelölhető meg `async`-ként, mert az async kódnak
_futtatókörnyezetre (runtime)_ van szüksége: egy olyan Rust crate-re, amely az
aszinkron kód végrehajtásának részleteit kezeli. Egy program `main` függvénye
_inicializálhat_ egy futtatókörnyezetet, de _maga_ nem futtatókörnyezet.
(Hamarosan többet is látunk arról, hogy miért van ez így.) Minden Rust
programnak, amely async kódot hajt végre, van legalább egy pontja, ahol
beállít egy futtatókörnyezetet, amely végrehajtja a future-öket.

A legtöbb asyncet támogató nyelv tartalmaz beépített futtatókörnyezetet, a Rust
azonban nem. Ehelyett sok különböző aszinkron futtatókörnyezet érhető el,
amelyek mindegyike más-más kompromisszumot köt, a megcélzott felhasználási
területnek megfelelően. Egy nagy áteresztőképességű webszervernek, amely sok
CPU-maggal és nagy mennyiségű RAM-mal rendelkezik, például egészen mások az
igényei, mint egy egymagos mikrovezérlőnek, amelynek kevés RAM-ja van, és nem
képes kupacfoglalásra. Az ilyen futtatókörnyezeteket biztosító crate-ek
gyakran az általános funkciók – például a fájl- vagy hálózati I/O – aszinkron
változatait is kínálják.

Itt és a fejezet hátralévő részében a `trpl` crate `block_on` függvényét
használjuk, amely argumentumként egy future-t kap, és blokkolja az aktuális
szálat, amíg ez a future le nem fut. A háttérben a `block_on` hívása a `tokio`
crate segítségével beállít egy futtatókörnyezetet, amely az átadott future-t
futtatja (a `trpl` crate `block_on` függvényének viselkedése hasonló más
futtatókörnyezet-crate-ek `block_on` függvényeihez). Amint a future befejeződik,
a `block_on` visszaadja azt az értéket, amelyet a future előállított.

A `page_title` által visszaadott future-t közvetlenül is átadhatnánk a
`block_on`-nak, és amint befejeződött, illeszthetnénk a kapott
`Option<String>`-re, ahogy a 17-3. kódrészletben próbáltuk. A fejezet legtöbb
példájában (és a valós async kód nagy részében) azonban többet fogunk csinálni
egyetlen async függvényhívásnál, ezért ehelyett egy `async` blokkot adunk át,
és kifejezetten bevárjuk a `page_title` hívásának eredményét, ahogy a 17-4.
kódrészletben.

<Listing number="17-4" caption="Egy async blokk bevárása a `trpl::block_on` segítségével" file-name="src/main.rs">

<!-- should_panic,noplayground because mdbook test does not pass args -->

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch17-async-await/listing-17-04/src/main.rs:run}}
```

</Listing>

Amikor futtatjuk ezt a kódot, azt a viselkedést kapjuk, amelyet eredetileg
vártunk:

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-04
cargo build # skip all the build noise
cargo run -- "https://www.rust-lang.org"
# copy the output here
-->

```console
$ cargo run -- "https://www.rust-lang.org"
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.05s
     Running `target/debug/async_await 'https://www.rust-lang.org'`
The title for https://www.rust-lang.org was
            Rust Programming Language
```

Hű – végre van egy kis működő async kódunk! Mielőtt azonban megírnánk a kódot,
amely két webhelyet versenyeztet egymással, röviden térjünk vissza ahhoz, hogyan
működnek a future-ök.

Minden _await-pont (await point)_ – vagyis minden hely, ahol a kód az `await`
kulcsszót használja – olyan pontot jelöl, ahol a vezérlés visszakerül a
futtatókörnyezethez. Ahhoz, hogy ez működjön, a Rustnak nyilván kell tartania
az async blokk állapotát, hogy a futtatókörnyezet elindíthasson valamilyen más
munkát, majd visszatérhessen, amikor készen áll arra, hogy ismét megpróbálja
továbbvinni az elsőt. Ez egy láthatatlan állapotgép (state machine), mintha egy
ilyen enumot írtál volna, hogy minden await-pontnál elmentsd az aktuális
állapotot:

```rust
{{#rustdoc_include ../listings/ch17-async-await/no-listing-state-machine/src/lib.rs:enum}}
```

Az állapotok közötti átmenetek kódjának kézi megírása azonban fárasztó és
hibalehetőségekkel teli lenne, különösen ha később további funkciókat és
állapotokat kell hozzáadnod a kódhoz. Szerencsére a Rust fordító automatikusan
létrehozza és kezeli az async kódhoz tartozó állapotgép-adatszerkezeteket. Az
adatszerkezetekre vonatkozó szokásos kölcsönzési és tulajdonjogi szabályok
továbbra is érvényesek, és szerencsére ezek ellenőrzését is a fordító végzi
helyettünk, hasznos hibaüzenetekkel. A fejezet későbbi részében néhányat ezek
közül végig is veszünk.

Végső soron valaminek végre kell hajtania ezt az állapotgépet, és ez a valami
egy futtatókörnyezet. (Ezért találkozhatsz a futtatókörnyezetek kapcsán a
_végrehajtók (executors)_ említésével: a végrehajtó a futtatókörnyezetnek az a
része, amely az async kód végrehajtásáért felel.)

Most már láthatod, miért akadályozott meg minket a fordító abban, hogy a 17-3.
kódrészletben magát a `main`-t async függvénnyé tegyük. Ha a `main` async
függvény lenne, valami másnak kellene kezelnie az állapotgépet ahhoz a
future-höz, amelyet a `main` visszaad, de a `main` a program kiindulópontja!
Ehelyett a `main`-ben meghívtuk a `trpl::block_on` függvényt, hogy beállítson
egy futtatókörnyezetet, és az `async` blokk által visszaadott future-t addig
futtassa, amíg el nem készül.

> Megjegyzés: Egyes futtatókörnyezetek makrókat biztosítanak, hogy _írhass_
> async `main` függvényt. Ezek a makrók az `async fn main() { ... }` kódot egy
> normál `fn main`-né írják át, amely ugyanazt teszi, amit mi kézzel a 17-4.
> kódrészletben: meghív egy függvényt, amely a `trpl::block_on`-hoz hasonlóan
> a befejezéséig futtat egy future-t.

Most rakjuk össze ezeket a darabokat, és nézzük meg, hogyan írhatunk konkurens
kódot!

<!-- Old headings. Do not remove or links may break. -->

<a id="racing-our-two-urls-against-each-other"></a>

### Két URL konkurens versenyeztetése {#racing-two-urls-against-each-other-concurrently}

A 17-5. kódrészletben a `page_title`-t két különböző, a parancssorból átadott
URL-lel hívjuk meg, és versenyeztetjük őket úgy, hogy azt a future-t
választjuk ki, amelyik előbb végez.

<Listing number="17-5" caption="A `page_title` meghívása két URL-re, hogy lássuk, melyik tér vissza előbb" file-name="src/main.rs">

<!-- should_panic,noplayground because mdbook does not pass args -->

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch17-async-await/listing-17-05/src/main.rs:all}}
```

</Listing>

Először meghívjuk a `page_title`-t mindkét, a felhasználó által megadott
URL-re. Az így kapott future-öket `title_fut_1` és `title_fut_2` néven mentjük
el. Ne feledd, ezek még semmit sem csinálnak, mert a future-ök lusták, és még
nem vártuk be őket. Ezután átadjuk a future-öket a `trpl::select`-nek, amely
egy olyan értéket ad vissza, amely jelzi, hogy a neki átadott future-ök közül
melyik végzett előbb.

> Megjegyzés: A háttérben a `trpl::select` a `futures` crate-ben definiált,
> általánosabb `select` függvényre épül. A `futures` crate `select` függvénye
> sok mindenre képes, amire a `trpl::select` függvény nem, de van némi
> többletbonyolultsága is, amelyet most átugorhatunk.

Bármelyik future jogosan „nyerhet”, így nincs értelme `Result`-ot visszaadni.
Ehelyett a `trpl::select` egy olyan típust ad vissza, amellyel még nem
találkoztunk: a `trpl::Either`-t. Az `Either` típus némileg hasonlít a
`Result`-hoz, abban, hogy két esete van. A `Result`-tal ellentétben azonban az
`Either`-be nincs beépítve a siker vagy kudarc fogalma. Ehelyett a `Left` és a
`Right` segítségével jelzi, hogy „az egyik vagy a másik”:

```rust
enum Either<A, B> {
    Left(A),
    Right(B),
}
```

A `select` függvény `Left`-et ad vissza az adott future kimenetével, ha az első
argumentum nyer, és `Right`-ot a második future-argumentum kimenetével, ha _az_
nyer. Ez megfelel az argumentumok sorrendjének a függvény hívásakor: az első
argumentum a második argumentumtól balra áll.

A `page_title`-t is módosítjuk, hogy ugyanazt az URL-t adja vissza, amelyet
kapott. Így ha az elsőként visszatérő oldalnak nincs olyan `<title>` eleme,
amelyet fel tudnánk oldani, akkor is ki tudunk írni egy értelmes üzenetet.
Ezzel az információval a kezünkben végül frissítjük a `println!` kimenetét,
hogy jelezze, melyik URL végzett előbb, és ha van, mi az adott URL-en lévő
weboldal `<title>` eleme.

Most már elkészítettél egy kis működő webkaparót! Válassz néhány URL-t, és
futtasd a parancssori eszközt. Felfedezheted, hogy egyes webhelyek
következetesen gyorsabbak másoknál, míg más esetekben a gyorsabb webhely
futtatásról futtatásra változik. Ami még fontosabb, megtanultad a future-ökkel
való munka alapjait, így most mélyebbre áshatunk abban, mit kezdhetünk az
asynckel.

[impl-trait]: ch10-02-traits.html#traits-as-parameters
[iterators-lazy]: ch13-02-iterators.html
[thread-spawn]: ch16-01-threads.html#creating-a-new-thread-with-spawn
[cli-args]: ch12-01-accepting-command-line-arguments.html

<!-- TODO: map source link version to version of Rust? -->

[crate-source]: https://github.com/rust-lang/book/tree/main/packages/trpl
[futures-crate]: https://crates.io/crates/futures
[tokio]: https://tokio.rs
