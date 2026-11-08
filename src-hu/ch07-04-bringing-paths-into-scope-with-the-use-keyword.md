## Útvonalak hatókörbe hozása a `use` kulcsszóval {#bringing-paths-into-scope-with-the-use-keyword}

Kényelmetlennek és ismétlődőnek érezheted, hogy a függvényhívásokhoz ki kell
írni az útvonalakat. A 7-7. kódrészletben akár az abszolút, akár a relatív
útvonalat választottuk az `add_to_waitlist` függvényhez, valahányszor meg
akartuk hívni az `add_to_waitlist` függvényt, a `front_of_house` és a
`hosting` modult is meg kellett adnunk. Szerencsére ez egyszerűsíthető: a
`use` kulcsszóval egyszer létrehozhatunk egy rövidítést egy útvonalhoz, és
utána a hatókörben mindenhol a rövidebb nevet használhatjuk.

A 7-11. kódrészletben a `crate::front_of_house::hosting` modult az
`eat_at_restaurant` függvény hatókörébe hozzuk, így az `eat_at_restaurant`
függvényben elég a `hosting::add_to_waitlist` útvonalat megadnunk az
`add_to_waitlist` függvény meghívásához.

<Listing number="7-11" file-name="src/lib.rs" caption="Modul hatókörbe hozása a `use` kulcsszóval">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-11/src/lib.rs}}
```

</Listing>

Ha egy hatókörben a `use` kulcsszót és egy útvonalat adunk meg, az hasonló
ahhoz, mint amikor egy szimbolikus linket hozunk létre a fájlrendszerben. A
`use crate::front_of_house::hosting` crate-gyökérbe írásával a `hosting`
érvényes névvé válik ebben a hatókörben, mintha a `hosting` modult a
crate-gyökérben definiáltuk volna. A `use` kulcsszóval hatókörbe hozott
útvonalakra is vonatkoznak a láthatósági szabályok, mint bármely más
útvonalra.

Fontos, hogy a `use` csak abban a hatókörben hozza létre a rövidítést,
amelyben a `use` szerepel. A 7-12. kódrészlet az `eat_at_restaurant`
függvényt egy új, `customer` nevű gyermekmodulba helyezi át, amely már más
hatókör, mint ahol a `use` utasítás van, ezért a függvény törzse nem fordul le.

<Listing number="7-12" file-name="src/lib.rs" caption="A `use` utasítás csak abban a hatókörben érvényes, amelyben szerepel.">

```rust,noplayground,test_harness,does_not_compile,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-12/src/lib.rs}}
```

</Listing>

A fordítói hiba azt mutatja, hogy a rövidítés a `customer` modulon belül már
nem érvényes:

```console
{{#include ../listings/ch07-managing-growing-projects/listing-07-12/output.txt}}
```

Figyeld meg, hogy egy figyelmeztetést is kapunk arról, hogy a `use` már nincs
használatban a saját hatókörében! A probléma megoldásához helyezd át a `use`
utasítást is a `customer` modulba, vagy a `customer` gyermekmodulon belül
hivatkozz a szülőmodulban lévő rövidítésre a `super::hosting` útvonallal.

### Idiomatikus `use` útvonalak létrehozása {#creating-idiomatic-use-paths}

A 7-11. kódrészletnél talán elgondolkodtál azon, miért a `use
crate::front_of_house::hosting` útvonalat adtuk meg, és miért a
`hosting::add_to_waitlist` függvényt hívtuk meg az `eat_at_restaurant`
függvényben, ahelyett, hogy a `use` útvonalat egészen az `add_to_waitlist`
függvényig adtuk volna meg, ugyanezt az eredményt elérve, ahogy a 7-13.
kódrészletben.

<Listing number="7-13" file-name="src/lib.rs" caption="Az `add_to_waitlist` függvény hatókörbe hozása a `use` kulcsszóval, ami nem idiomatikus">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-13/src/lib.rs}}
```

</Listing>

Bár a 7-11. és a 7-13. kódrészlet ugyanazt a feladatot végzi el, a 7-11.
kódrészlet mutatja az idiomatikus módját annak, hogyan hozzunk egy függvényt
hatókörbe a `use` kulcsszóval. Ha a függvény szülőmodulját hozzuk hatókörbe a
`use` kulcsszóval, a függvény hívásakor meg kell adnunk a szülőmodult. A
szülőmodul megadása a függvény hívásakor egyértelművé teszi, hogy a függvény
nem helyben van definiálva, ugyanakkor a teljes útvonal ismétlését is a
minimumra csökkenti. A 7-13. kódrészlet kódjából nem derül ki egyértelműen,
hol van definiálva az `add_to_waitlist`.

Ha viszont struktúrákat, enumokat és más elemeket hozunk hatókörbe a `use`
kulcsszóval, az idiomatikus megoldás a teljes útvonal megadása. A 7-14.
kódrészlet azt mutatja, hogyan hozzuk idiomatikusan egy bináris crate
hatókörébe a standard könyvtár `HashMap` struktúráját.

<Listing number="7-14" file-name="src/main.rs" caption="A `HashMap` hatókörbe hozása idiomatikus módon">

```rust
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-14/src/main.rs}}
```

</Listing>

Ennek az idiómának nincs különösebb oka: egyszerűen ez a konvenció alakult ki,
és az emberek megszokták, hogy így olvassák és írják a Rust-kódot.

Ez alól az idióma alól kivétel, ha két azonos nevű elemet hozunk hatókörbe
`use` utasításokkal, mert ezt a Rust nem engedi. A 7-15. kódrészlet azt
mutatja, hogyan hozhatunk hatókörbe két olyan `Result` típust, amelyeknek
azonos a nevük, de különböző a szülőmoduljuk, és hogyan hivatkozhatunk rájuk.

<Listing number="7-15" file-name="src/lib.rs" caption="Két azonos nevű típus ugyanabba a hatókörbe hozásához a szülőmoduljukat kell használnunk.">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-15/src/lib.rs:here}}
```

</Listing>

Ahogy láthatod, a szülőmodulok használata megkülönbözteti a két `Result`
típust. Ha ehelyett a `use std::fmt::Result` és a `use std::io::Result` sort
írnánk, két `Result` típus lenne ugyanabban a hatókörben, és a Rust nem
tudná, melyikre gondolunk, amikor a `Result` nevet használjuk.

### Új nevek megadása az `as` kulcsszóval {#providing-new-names-with-the-as-keyword}

Két azonos nevű típus ugyanabba a hatókörbe hozásának problémájára a `use`
kulcsszóval van egy másik megoldás is: az útvonal után megadhatjuk az `as`
kulcsszót és a típus új helyi nevét, más szóval _álnevét (alias)_. A 7-16.
kódrészlet a 7-15. kódrészlet kódjának egy másik változatát mutatja, amelyben
az `as` segítségével átnevezzük a két `Result` típus egyikét.

<Listing number="7-16" file-name="src/lib.rs" caption="Típus átnevezése az `as` kulcsszóval, amikor hatókörbe hozzuk">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-16/src/lib.rs:here}}
```

</Listing>

A második `use` utasításban az `IoResult` új nevet választottuk a
`std::io::Result` típusnak, így nem ütközik a `std::fmt` modulból származó
`Result` típussal, amelyet szintén hatókörbe hoztunk. A 7-15. és a 7-16.
kódrészlet is idiomatikusnak számít, így rajtad múlik, melyiket választod!

### Nevek újraexportálása a `pub use` segítségével {#re-exporting-names-with-pub-use}

Amikor a `use` kulcsszóval egy nevet hatókörbe hozunk, a név privát abban a
hatókörben, amelybe importáltuk. Ahhoz, hogy a hatókörön kívüli kód is úgy
hivatkozhasson erre a névre, mintha abban a hatókörben definiálták volna,
kombinálhatjuk a `pub` és a `use` kulcsszót. Ezt a technikát
_újraexportálásnak (re-exporting)_ nevezzük, mert egy elemet hatókörbe hozunk,
de egyúttal elérhetővé is tesszük mások számára, hogy ők is a saját
hatókörükbe hozhassák.

A 7-17. kódrészlet a 7-11. kódrészlet kódját mutatja úgy, hogy a gyökérmodulban
lévő `use` helyére `pub use` került.

<Listing number="7-17" file-name="src/lib.rs" caption="Név elérhetővé tétele bármely kód számára egy új hatókörből a `pub use` segítségével">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-17/src/lib.rs}}
```

</Listing>

E változtatás előtt a külső kódnak az
`restaurant::front_of_house::hosting::add_to_waitlist()` útvonallal kellett
volna meghívnia az `add_to_waitlist` függvényt, amihez a `front_of_house`
modult is `pub` jelöléssel kellett volna ellátni. Most, hogy ez a `pub use`
újraexportálta a `hosting` modult a gyökérmodulból, a külső kód helyette a
`restaurant::hosting::add_to_waitlist()` útvonalat használhatja.

Az újraexportálás akkor hasznos, ha a kódod belső szerkezete eltér attól,
ahogyan a kódodat hívó programozók a szakterületről gondolkodnak. Az éttermes
hasonlatnál maradva az étterem üzemeltetői „vendégtérben” és „háttérben”
gondolkodnak, az étterembe betérő vendégek viszont valószínűleg nem így
gondolnak az étterem részeire. A `pub use` segítségével a kódot egy bizonyos
szerkezetben írhatjuk meg, kifelé azonban egy másik szerkezetet mutathatunk.
Így a könyvtárunk jól szervezett lesz a könyvtáron dolgozó és a könyvtárat
hívó programozók számára is. A `pub use` egy másik példáját, és azt, hogy
hogyan befolyásolja a crate dokumentációját, a 14. fejezet [„Kényelmes
nyilvános API exportálása”][ch14-pub-use]<!-- ignore --> szakaszában nézzük
meg.

### Külső csomagok használata {#using-external-packages}

A 2. fejezetben egy számkitalálós játékot programoztunk, amely egy `rand` nevű
külső csomagot használt véletlenszámok előállítására. Ahhoz, hogy a `rand`
csomagot használhassuk a projektünkben, a következő sort adtuk hozzá a
_Cargo.toml_ fájlhoz:

<!-- When updating the version of `rand` used, also update the version of
`rand` used in these files so they all match:

* ch01-01-installation.md
* ch02-00-guessing-game-tutorial.md
* ch14-03-cargo-workspaces.md
-->

<Listing file-name="Cargo.toml">

```toml
{{#include ../listings/ch02-guessing-game-tutorial/listing-02-02/Cargo.toml:9:}}
```

</Listing>

Ha a `rand` csomagot függőségként felvesszük a _Cargo.toml_ fájlba, azzal
arra utasítjuk a Cargót, hogy töltse le a `rand` csomagot és annak összes
függőségét a [crates.io](https://crates.io/) oldalról, és tegye elérhetővé a
`rand` csomagot a projektünk számára.

Ezután, hogy a `rand` definícióit a csomagunk hatókörébe hozzuk, felvettünk
egy `use` sort, amely a crate nevével, a `rand` szóval kezdődik, és
felsoroltuk azokat az elemeket, amelyeket hatókörbe akartunk hozni. Emlékezz
vissza: a 2. fejezet [„Véletlen szám generálása”][rand]<!-- ignore -->
szakaszában a `rand::prelude` modul elemeit hoztuk hatókörbe, és a
`rand::rng` függvényt hívtuk meg:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-03/src/main.rs:ch07-04}}
```

A Rust-közösség tagjai számos csomagot tettek elérhetővé a
[crates.io](https://crates.io/) oldalon, és bármelyiknek a csomagodba való
bevonása ugyanezekből a lépésekből áll: fel kell venned őket a csomagod
_Cargo.toml_ fájljába, és a `use` kulcsszóval hatókörbe kell hoznod az
elemeket a crate-jeikből.

Fontos, hogy a `std` standard könyvtár is egy, a csomagunkhoz képest külső
crate. Mivel a standard könyvtár a Rust nyelvvel együtt érkezik, a `std`
használatához nem kell módosítanunk a _Cargo.toml_ fájlt. Ahhoz viszont
hivatkoznunk kell rá a `use` kulcsszóval, hogy elemeket hozzunk belőle a
csomagunk hatókörébe. A `HashMap` esetében például ezt a sort használnánk:

```rust
use std::collections::HashMap;
```

Ez egy abszolút útvonal, amely a `std` névvel, a standard könyvtár crate
nevével kezdődik.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-nested-paths-to-clean-up-large-use-lists"></a>

### Beágyazott útvonalak a `use` listák rendezéséhez {#using-nested-paths-to-clean-up-use-lists}

Ha több, ugyanabban a crate-ben vagy ugyanabban a modulban definiált elemet
használunk, és minden elemet külön sorban sorolunk fel, az sok függőleges
helyet foglalhat el a fájljainkban. A 2-4. kódrészletben, a számkitalálós
játékban például ez a két `use` utasítás hozott elemeket hatókörbe a `std`
könyvtárból:

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/no-listing-01-use-std-unnested/src/main.rs:here}}
```

</Listing>

Ehelyett beágyazott útvonalakkal (nested paths) ugyanezeket az elemeket egyetlen
sorban hozhatjuk hatókörbe. Ehhez megadjuk az útvonal közös részét, utána két
kettőspontot, majd kapcsos zárójelek között az útvonalak eltérő részeinek
listáját, ahogy a 7-18. kódrészlet mutatja.

<Listing number="7-18" file-name="src/main.rs" caption="Beágyazott útvonal megadása több, azonos előtagú elem hatókörbe hozásához">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-18/src/main.rs:here}}
```

</Listing>

Nagyobb programokban, ha sok elemet hozunk hatókörbe ugyanabból a crate-ből
vagy modulból, a beágyazott útvonalakkal jelentősen csökkenthetjük a szükséges
különálló `use` utasítások számát!

Beágyazott útvonalat az útvonal bármely szintjén használhatunk, ami akkor
hasznos, ha két olyan `use` utasítást vonunk össze, amelyeknek közös az
alútvonaluk. A 7-19. kódrészlet például két `use` utasítást mutat: az egyik a
`std::io`, a másik a `std::io::Write` elemet hozza hatókörbe.

<Listing number="7-19" file-name="src/lib.rs" caption="Két `use` utasítás, amelyek közül az egyik a másik alútvonala">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-19/src/lib.rs}}
```

</Listing>

A két útvonal közös része a `std::io`, és ez egyben a teljes első útvonal. Ha
a két útvonalat egyetlen `use` utasításba akarjuk összevonni, a beágyazott
útvonalban a `self` kulcsszót használhatjuk, ahogy a 7-20. kódrészlet mutatja.

<Listing number="7-20" file-name="src/lib.rs" caption="A 7-19. kódrészlet útvonalainak összevonása egyetlen `use` utasításba">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-20/src/lib.rs}}
```

</Listing>

Ez a sor a `std::io` és a `std::io::Write` elemet is hatókörbe hozza.

<!-- Old headings. Do not remove or links may break. -->

<a id="the-glob-operator"></a>

### Elemek importálása a glob operátorral {#importing-items-with-the-glob-operator}

Ha egy útvonalon definiált _összes_ nyilvános elemet hatókörbe akarjuk hozni,
megadhatjuk az útvonalat, utána pedig a `*` glob operátort:

```rust
use std::collections::*;
```

Ez a `use` utasítás a `std::collections` modulban definiált összes nyilvános
elemet az aktuális hatókörbe hozza. Óvatosan bánj a glob operátorral! A glob
megnehezítheti annak megállapítását, hogy mely nevek vannak hatókörben, és hol
definiálták a programodban használt egyes neveket. Ráadásul ha a függőség
megváltoztatja a definícióit, az is megváltozik, amit importáltál, ami fordítási
hibákhoz vezethet a függőség frissítésekor, például ha a függőség olyan
definíciót vesz fel, amelynek ugyanaz a neve, mint egy saját definíciódnak
ugyanabban a hatókörben.

A glob operátort gyakran tesztelésnél használják arra, hogy minden tesztelendő
elemet a `tests` modulba hozzanak; erről a 11. fejezet [„Hogyan írjunk
teszteket?”][writing-tests]<!-- ignore --> szakaszában lesz szó. A glob
operátort néha a prelude minta részeként is használják: erről a mintáról
bővebben
[a standard könyvtár dokumentációjában](https://doc.rust-lang.org/std/prelude/index.html#other-preludes)<!-- ignore -->
olvashatsz.

[ch14-pub-use]: ch14-02-publishing-to-crates-io.html#exporting-a-convenient-public-api
[rand]: ch02-00-guessing-game-tutorial.html#generating-a-random-number
[writing-tests]: ch11-01-writing-tests.html#how-to-write-tests
