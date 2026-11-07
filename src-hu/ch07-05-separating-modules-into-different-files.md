## Modulok szétválasztása külön fájlokba {#separating-modules-into-different-files}

Ebben a fejezetben eddig minden példa több modult definiált egyetlen fájlban.
Ha a modulok nagyra nőnek, érdemes lehet a definícióikat külön fájlba
áthelyezni, hogy könnyebb legyen eligazodni a kódban.

Induljunk ki például a 7-17. kódrészlet kódjából, amely több éttermi modult
tartalmazott. Ahelyett, hogy minden modult a crate-gyökérfájlban
definiálnánk, a modulokat külön fájlokba emeljük ki. Ebben az esetben a
crate-gyökérfájl az _src/lib.rs_, de ez az eljárás azokkal a bináris
crate-ekkel is működik, amelyek crate-gyökérfájlja az _src/main.rs_.

Először a `front_of_house` modult emeljük ki egy saját fájlba. Töröld a
`front_of_house` modul kapcsos zárójelei közötti kódot, és csak a
`mod front_of_house;` deklarációt hagyd meg, hogy az _src/lib.rs_ a 7-21.
kódrészletben látható kódot tartalmazza. Vedd figyelembe, hogy ez nem fordul
le, amíg létre nem hozzuk a 7-22. kódrészletben látható
_src/front_of_house.rs_ fájlt.

<Listing number="7-21" file-name="src/lib.rs" caption="A `front_of_house` modul deklarálása, amelynek törzse az *src/front_of_house.rs* fájlba kerül">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-21-and-22/src/lib.rs}}
```

</Listing>

Ezután helyezd a kapcsos zárójelek között lévő kódot egy új,
_src/front_of_house.rs_ nevű fájlba, ahogy a 7-22. kódrészlet mutatja. A
fordító azért tudja, hogy ebben a fájlban kell keresnie, mert a
crate-gyökérben egy `front_of_house` nevű moduldeklarációval találkozott.

<Listing number="7-22" file-name="src/front_of_house.rs" caption="A `front_of_house` modul definíciói az *src/front_of_house.rs* fájlban">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-21-and-22/src/front_of_house.rs}}
```

</Listing>

Fontos, hogy egy fájlt a `mod` deklarációval a modulfában csak _egyszer_ kell
betöltened. Ha a fordító már tudja, hogy a fájl a projekt része (és azt is
tudja, hol helyezkedik el a kód a modulfában, attól függően, hová írtad a
`mod` utasítást), a projekted többi fájljának a betöltött fájl kódjára a
deklaráció helyéhez vezető útvonallal kell hivatkoznia, ahogy azt az
[„Útvonalak a modulfa elemeire való hivatkozáshoz”][paths]<!-- ignore -->
szakaszban bemutattuk. Más szóval a `mod` _nem_ olyan „include” művelet, amilyet
más programozási nyelvekben láthattál.

Ezután a `hosting` modult emeljük ki egy saját fájlba. A folyamat kicsit
eltér, mert a `hosting` a `front_of_house` gyermekmodulja, nem pedig a
gyökérmodulé. A `hosting` fájlját egy új mappába helyezzük, amely a modulfában
lévő őseiről kapja a nevét, ebben az esetben ez az _src/front_of_house_.

A `hosting` áthelyezésének megkezdéséhez úgy módosítjuk az
_src/front_of_house.rs_ fájlt, hogy csak a `hosting` modul deklarációját
tartalmazza:

<Listing file-name="src/front_of_house.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/no-listing-02-extracting-hosting/src/front_of_house.rs}}
```

</Listing>

Ezután létrehozunk egy _src/front_of_house_ mappát, benne pedig egy
_hosting.rs_ fájlt, amely a `hosting` modulban lévő definíciókat tartalmazza:

<Listing file-name="src/front_of_house/hosting.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/no-listing-02-extracting-hosting/src/front_of_house/hosting.rs}}
```

</Listing>

Ha ehelyett a _hosting.rs_ fájlt az _src_ mappába tennénk, a fordító azt
várná, hogy a _hosting.rs_ kódja egy olyan `hosting` modulban van, amelyet a
crate-gyökérben deklaráltak, nem pedig a `front_of_house` modul gyermekeként.
A fordító szabályai arra vonatkozóan, hogy mely modulok kódját mely fájlokban
keresse, azt eredményezik, hogy a mappák és a fájlok szorosabban követik a
modulfát.

> ### Alternatív fájlútvonalak {#alternate-file-paths}
>
> Eddig a Rust fordító által használt legidiomatikusabb fájlútvonalakat
> mutattuk be, de a Rust egy régebbi stílusú fájlútvonalat is támogat. Egy
> crate-gyökérben deklarált, `front_of_house` nevű modul esetén a fordító a
> következő helyeken keresi a modul kódját:
>
> - _src/front_of_house.rs_ (amit bemutattunk)
> - _src/front_of_house/mod.rs_ (régebbi stílus, még mindig támogatott útvonal)
>
> Egy `hosting` nevű modul esetén, amely a `front_of_house` almodulja, a
> fordító a következő helyeken keresi a modul kódját:
>
> - _src/front_of_house/hosting.rs_ (amit bemutattunk)
> - _src/front_of_house/hosting/mod.rs_ (régebbi stílus, még mindig támogatott
>   útvonal)
>
> Ha ugyanarra a modulra mindkét stílust használod, fordítási hibát kapsz.
> Ugyanabban a projektben különböző modulokhoz vegyesen használhatod a két
> stílust, de ez zavaró lehet azok számára, akik a projektedben próbálnak
> eligazodni.
>
> A _mod.rs_ nevű fájlokat használó stílus fő hátránya, hogy a projektedben sok
> _mod.rs_ nevű fájl gyűlhet össze, ami zavaró lehet, ha egyszerre több is
> nyitva van a szerkesztődben.

Minden modul kódját külön fájlba helyeztük át, a modulfa pedig ugyanaz maradt.
Az `eat_at_restaurant` függvényben lévő függvényhívások változtatás nélkül
működnek, annak ellenére, hogy a definíciók különböző fájlokban vannak. Ezzel
a technikával a modulokat új fájlokba helyezheted át, ahogy nőnek.

Vedd észre, hogy az _src/lib.rs_ fájlban lévő
`pub use crate::front_of_house::hosting` utasítás sem változott, és a `use`
arra sincs hatással, hogy mely fájlok fordulnak le a crate részeként. A `mod`
kulcsszó modulokat deklarál, a Rust pedig a modullal azonos nevű fájlban
keresi az adott modulba kerülő kódot.

## Összefoglalás {#summary}

A Rust lehetővé teszi, hogy egy csomagot több crate-re, egy crate-et pedig
modulokra bonts, így az egyik modulban definiált elemekre egy másik modulból is
hivatkozhatsz. Ezt abszolút vagy relatív útvonalak megadásával teheted meg.
Ezeket az útvonalakat egy `use` utasítással hatókörbe hozhatod, így az adott
hatókörben az elem többszöri használatakor rövidebb útvonalat írhatsz. A
modulok kódja alapértelmezés szerint privát, de a `pub` kulcsszóval
nyilvánossá teheted a definíciókat.

A következő fejezetben a standard könyvtár néhány gyűjteményként szolgáló
adatszerkezetét nézzük meg, amelyeket a szépen rendszerezett kódodban
használhatsz.

[paths]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html
