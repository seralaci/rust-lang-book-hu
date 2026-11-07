<!-- Old headings. Do not remove or links may break. -->

<a id="defining-modules-to-control-scope-and-privacy"></a>

## Hatókör és láthatóság szabályozása modulokkal {#control-scope-and-privacy-with-modules}

Ebben a szakaszban a modulokról és a modulrendszer további részeiről lesz szó,
nevezetesen az _útvonalakról (paths)_, amelyekkel elemeket nevezhetünk meg; a
`use` kulcsszóról, amely egy útvonalat hatókörbe hoz; és a `pub` kulcsszóról,
amellyel elemeket tehetünk nyilvánossá. Megismerkedünk az `as` kulcsszóval, a
külső csomagokkal és a glob operátorral is.

### Puska a modulokhoz {#modules-cheat-sheet}

Mielőtt rátérnénk a modulok és útvonalak részleteire, itt egy gyors
összefoglalót adunk arról, hogyan működnek a modulok, az útvonalak, a `use` és a
`pub` kulcsszó a fordítóban, és hogyan rendszerezi a kódját a legtöbb
fejlesztő. A fejezet során mindegyik szabályra mutatunk példát, de ez a hely
remekül használható emlékeztetőként arra, hogyan működnek a modulok.

- **Kezdés a crate-gyökérnél**: Egy crate fordításakor a fordító először a
  crate-gyökérfájlban (könyvtár crate esetén általában _src/lib.rs_, bináris
  crate esetén _src/main.rs_) keresi a lefordítandó kódot.
- **Modulok deklarálása**: A crate-gyökérfájlban új modulokat deklarálhatsz;
  tegyük fel, hogy egy „garden” modult deklarálsz a `mod garden;` sorral. A
  fordító a következő helyeken keresi a modul kódját:
  - Helyben (inline), kapcsos zárójelek között, amelyek a `mod garden` utáni
    pontosvesszőt helyettesítik
  - Az _src/garden.rs_ fájlban
  - Az _src/garden/mod.rs_ fájlban
- **Almodulok deklarálása**: A crate-gyökéren kívül bármely fájlban
  deklarálhatsz almodulokat. Az _src/garden.rs_ fájlban például deklarálhatod a
  `mod vegetables;` almodult. A fordító a szülőmodulról elnevezett mappán belül
  a következő helyeken keresi az almodul kódját:
  - Helyben, közvetlenül a `mod vegetables` után, pontosvessző helyett kapcsos
    zárójelek között
  - Az _src/garden/vegetables.rs_ fájlban
  - Az _src/garden/vegetables/mod.rs_ fájlban
- **Útvonalak a modulokban lévő kódhoz**: Ha egy modul már a crate része, az
  adott crate bármely más pontjáról hivatkozhatsz a modulban lévő kódra,
  amennyiben a láthatósági szabályok megengedik, a kódhoz vezető útvonal
  segítségével. Egy `Asparagus` típus a garden modul vegetables almodulján
  belül például a `crate::garden::vegetables::Asparagus` útvonalon érhető el.
- **Privát és nyilvános**: Egy modulon belüli kód alapértelmezés szerint privát
  a szülőmoduljai számára. Egy modul nyilvánossá tételéhez `mod` helyett
  `pub mod`-dal deklaráld. Ahhoz, hogy egy nyilvános modulon belüli elemek is
  nyilvánosak legyenek, írd a `pub` kulcsszót a deklarációjuk elé.
- **A `use` kulcsszó**: Egy hatókörön belül a `use` kulcsszó rövidítéseket hoz
  létre az elemekhez, hogy ne kelljen a hosszú útvonalakat ismételgetni. Bármely
  hatókörben, amely hivatkozhat a `crate::garden::vegetables::Asparagus`
  elemre, létrehozhatsz egy rövidítést a `use
  crate::garden::vegetables::Asparagus;` sorral, és ettől kezdve elég az
  `Asparagus` nevet írnod, ha ebben a hatókörben használni akarod a típust.

Itt létrehozunk egy `backyard` nevű bináris crate-et, amely szemlélteti ezeket
a szabályokat. A crate mappája, amelynek neve szintén _backyard_, a következő
fájlokat és mappákat tartalmazza:

```text
backyard
├── Cargo.lock
├── Cargo.toml
└── src
    ├── garden
    │   └── vegetables.rs
    ├── garden.rs
    └── main.rs
```

A crate-gyökérfájl ebben az esetben az _src/main.rs_, és ezt tartalmazza:

<Listing file-name="src/main.rs">

```rust,noplayground,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/quick-reference-example/src/main.rs}}
```

</Listing>

A `pub mod garden;` sor arra utasítja a fordítót, hogy illessze be az
_src/garden.rs_ fájlban talált kódot, amely a következő:

<Listing file-name="src/garden.rs">

```rust,noplayground,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/quick-reference-example/src/garden.rs}}
```

</Listing>

Itt a `pub mod vegetables;` azt jelenti, hogy az _src/garden/vegetables.rs_
fájl kódja is bekerül. Ez a kód:

```rust,noplayground,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/quick-reference-example/src/garden/vegetables.rs}}
```

Most pedig nézzük meg részletesen ezeket a szabályokat, és lássuk őket
működés közben!

### Az összetartozó kód csoportosítása modulokba {#grouping-related-code-in-modules}

A _modulok (modules)_ segítségével a crate-en belül úgy rendszerezhetjük a
kódot, hogy könnyen olvasható és újrahasználható legyen. A modulokkal az elemek
_láthatóságát (privacy)_ is szabályozhatjuk, mivel a modulon belüli kód
alapértelmezés szerint privát. A privát elemek belső megvalósítási részletek,
amelyek kívülről nem használhatók. Dönthetünk úgy, hogy a modulokat és a
bennük lévő elemeket nyilvánossá tesszük, így a külső kód használhatja őket,
és építhet rájuk.

Példaként írjunk egy könyvtár crate-et, amely egy étterem működését
modellezi. A függvények szignatúráit definiáljuk, de a törzsüket üresen
hagyjuk, hogy a kód szerkezetére koncentrálhassunk, ne pedig egy étterem
megvalósítására.

A vendéglátásban az étterem egyes részeit vendégtérnek (front of house),
másokat a háttérnek (back of house) nevezik. A _vendégtér_ az, ahol a vendégek
vannak: itt ülteti le őket a fogadó személyzet, itt veszik fel a pincérek a
rendelést és itt fizetnek a vendégek, és itt készítik a pultosok az italokat.
A _háttér_ az, ahol a séfek és a szakácsok a konyhában dolgoznak, a
mosogatók mosogatnak, a vezetők pedig az adminisztratív munkát végzik.

Ahhoz, hogy a crate-ünket így strukturáljuk, a függvényeit egymásba ágyazott
modulokba szervezhetjük. Hozz létre egy új, `restaurant` nevű könyvtárat a
`cargo new restaurant --lib` paranccsal. Ezután írd be a 7-1. kódrészlet
kódját az _src/lib.rs_ fájlba, hogy definiálj néhány modult és
függvényszignatúrát; ez a kód a vendégtér részét valósítja meg.

<Listing number="7-1" file-name="src/lib.rs" caption="Egy `front_of_house` modul, amely további modulokat tartalmaz, azok pedig függvényeket">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-01/src/lib.rs}}
```

</Listing>

Egy modult a `mod` kulcsszóval és utána a modul nevével (ebben az esetben
`front_of_house`) definiálunk. A modul törzse ezután kapcsos zárójelek közé
kerül. A modulokon belül más modulokat is elhelyezhetünk, mint itt a
`hosting` és a `serving` modult. A modulok más elemek definícióit is
tartalmazhatják, például struktúrákat, enumokat, konstansokat, traiteket és –
ahogy a 7-1. kódrészletben – függvényeket.

A modulok használatával az összetartozó definíciókat csoportosíthatjuk, és
megnevezhetjük, mi köti össze őket. Az ezt a kódot használó programozók a
csoportok alapján igazodhatnak el a kódban, ahelyett, hogy az összes
definíciót végig kellene olvasniuk, így könnyebben megtalálják a számukra
fontos definíciókat. Az új funkciókat hozzáadó programozók pedig tudni fogják,
hová kell elhelyezniük a kódot, hogy a program rendezett maradjon.

Korábban említettük, hogy az _src/main.rs_ és az _src/lib.rs_ fájlt
_crate-gyökérnek (crate root)_ nevezzük. A nevük onnan ered, hogy e két fájl
bármelyikének tartalma egy `crate` nevű modult alkot a crate modulszerkezetének
gyökerében, amelyet _modulfának (module tree)_ nevezünk.

A 7-2. kódrészlet a 7-1. kódrészlet szerkezetének modulfáját mutatja.

<Listing number="7-2" caption="A 7-1. kódrészlet kódjának modulfája">

```text
crate
 └── front_of_house
     ├── hosting
     │   ├── add_to_waitlist
     │   └── seat_at_table
     └── serving
         ├── take_order
         ├── serve_order
         └── take_payment
```

</Listing>

Ez a fa megmutatja, hogyan ágyazódnak egyes modulok más modulokba; például a
`hosting` a `front_of_house` modulba van ágyazva. A fán az is látszik, hogy
egyes modulok _testvérek (siblings)_, vagyis ugyanabban a modulban vannak
definiálva; a `hosting` és a `serving` a `front_of_house` modulban definiált
testvérek. Ha az A modul a B modulon belül található, azt mondjuk, hogy az A
modul a B modul _gyermeke (child)_, a B modul pedig az A modul _szülője
(parent)_. Figyeld meg, hogy az egész modulfa gyökere a `crate` nevű implicit
modul.

A modulfa a számítógéped fájlrendszerének mappafájára emlékeztethet; ez nagyon
találó hasonlat! Ahogy a fájlrendszerben a mappákkal, úgy a modulokkal
rendszerezed a kódodat. És ahogy a mappákban lévő fájlokat, úgy a modulokat is
meg kell tudnunk találni valahogyan.
