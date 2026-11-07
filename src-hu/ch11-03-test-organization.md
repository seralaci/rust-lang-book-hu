## A tesztek szervezése {#test-organization}

Ahogy a fejezet elején említettük, a tesztelés összetett tudományág, és
különböző emberek különböző terminológiát és szervezési módot használnak. A
Rust-közösség két fő kategóriában gondolkodik a tesztekről: egységtesztekben és
integrációs tesztekben. Az _egységtesztek (unit tests)_ kicsik és célzottabbak:
egyszerre egy modult tesztelnek elszigetelten, és privát interfészeket is
tesztelhetnek. Az _integrációs tesztek (integration tests)_ teljesen kívül esnek
a könyvtáradon, és ugyanúgy használják a kódodat, mint bármely más külső kód:
csak a nyilvános interfészt használják, és tesztenként akár több modult is
igénybe vehetnek.

Mindkétféle teszt megírása fontos ahhoz, hogy biztos lehess benne: a
könyvtárad részei azt teszik, amit elvársz tőlük, külön-külön és együtt is.

### Egységtesztek {#unit-tests}

Az egységtesztek célja, hogy a kód minden egységét a kód többi részétől
elszigetelten teszteljék, így gyorsan behatárolható, hol működik és hol nem
működik a kód az elvárt módon. Az egységteszteket az _src_ mappában, abban a
fájlban helyezed el, amelyik a tesztelt kódot tartalmazza. A konvenció az,
hogy minden fájlban létrehozunk egy `tests` nevű modult a tesztfüggvények
számára, és a modult a `cfg(test)` annotációval látjuk el.

#### A `tests` modul és a `#[cfg(test)]` {#the-tests-module-and-cfgtest}

A `tests` modulon lévő `#[cfg(test)]` annotáció azt mondja a Rustnak, hogy a
tesztkódot csak a `cargo test` futtatásakor fordítsa le és futtassa, a `cargo
build` futtatásakor ne. Ez fordítási időt takarít meg, ha csak a könyvtárat
szeretnéd lefordítani, és helyet is spórol a lefordított termékben, mert a
tesztek nem kerülnek bele. Látni fogod, hogy mivel az integrációs tesztek
másik mappába kerülnek, nekik nincs szükségük a `#[cfg(test)]` annotációra. Az
egységtesztek viszont ugyanazokban a fájlokban vannak, mint a kód, ezért a
`#[cfg(test)]` segítségével kell jelezned, hogy ne kerüljenek bele a lefordított
eredménybe.

Emlékezz vissza: amikor a fejezet első szakaszában létrehoztuk az új `adder`
projektet, a Cargo ezt a kódot generálta nekünk:

<span class="filename">Fájlnév: src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-01/src/lib.rs}}
```

Az automatikusan generált `tests` modulon a `cfg` attribútum a _configuration_
(konfiguráció) rövidítése, és azt mondja a Rustnak, hogy a következő elemet
csak egy bizonyos konfigurációs beállítás megléte esetén vegye figyelembe.
Ebben az esetben a konfigurációs beállítás a `test`, amelyet a Rust a tesztek
fordításához és futtatásához biztosít. A `cfg` attribútum használatával a
Cargo csak akkor fordítja le a tesztkódunkat, ha ténylegesen a `cargo test`
paranccsal futtatjuk a teszteket. Ez a `#[test]` attribútummal megjelölt
függvényeken kívül a modulban esetleg található segédfüggvényekre is
vonatkozik.

<!-- Old headings. Do not remove or links may break. -->

<a id="testing-private-functions"></a>

#### Privát függvények tesztelése {#private-function-tests}

A tesztelők közösségében vita folyik arról, hogy a privát függvényeket
közvetlenül tesztelni kell-e vagy sem, és más nyelvek megnehezítik vagy
egyenesen lehetetlenné teszik a privát függvények tesztelését. Akármelyik
tesztelési irányzatot követed is, a Rust láthatósági szabályai lehetővé teszik
a privát függvények tesztelését. Nézd meg a 11-12. kódrészlet kódját az
`internal_adder` privát függvénnyel.

<Listing number="11-12" file-name="src/lib.rs" caption="Privát függvény tesztelése">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-12/src/lib.rs}}
```

</Listing>

Figyeld meg, hogy az `internal_adder` függvény nincs `pub`-ként megjelölve. A
tesztek is csak Rust-kódok, és a `tests` modul is csak egy újabb modul. Ahogy
az [„Útvonalak a modulfa elemeire való hivatkozáshoz”][paths]<!-- ignore -->
című részben tárgyaltuk, a gyermekmodulok elemei használhatják az őseik
moduljaiban lévő elemeket. Ebben a tesztben a `use super::*` segítségével a
`tests` modul szülőjéhez tartozó összes elemet a hatókörbe hozzuk, így a teszt
meghívhatja az `internal_adder` függvényt. Ha úgy gondolod, hogy a privát
függvényeket nem kell tesztelni, a Rustban semmi sem kényszerít rá.

### Integrációs tesztek {#integration-tests}

A Rustban az integrációs tesztek teljesen kívül esnek a könyvtáradon. Ugyanúgy
használják a könyvtáradat, mint bármely más kód, vagyis csak a könyvtárad
nyilvános API-jának részét képező függvényeket hívhatják meg. Céljuk annak
tesztelése, hogy a könyvtárad több része helyesen működik-e együtt. Az
önmagukban helyesen működő kódegységeknél is felléphetnek problémák, amikor
összekapcsoljuk őket, ezért az összekapcsolt kód tesztlefedettsége is fontos.
Integrációs tesztek létrehozásához először egy _tests_ mappára van
szükséged.

#### A _tests_ mappa {#the-tests-directory}

A _tests_ mappát a projektmappa legfelső szintjén hozzuk létre, az _src_
mellett. A Cargo tudja, hogy az integrációs tesztek fájljait ebben a mappában
kell keresnie. Ezután annyi tesztfájlt készíthetünk, amennyit csak akarunk, és a
Cargo mindegyik fájlt külön crate-ként fordítja le.

Hozzunk létre egy integrációs tesztet. Miközben a 11-12. kódrészlet kódja még
mindig az _src/lib.rs_ fájlban van, hozz létre egy _tests_ mappát, benne egy új
_tests/integration_test.rs_ nevű fájllal. A mappaszerkezetednek így kell
kinéznie:

```text
adder
├── Cargo.lock
├── Cargo.toml
├── src
│   └── lib.rs
└── tests
    └── integration_test.rs
```

Írd be a 11-13. kódrészlet kódját a _tests/integration_test.rs_ fájlba.

<Listing number="11-13" file-name="tests/integration_test.rs" caption="Az `adder` crate egy függvényének integrációs tesztje">

```rust,ignore
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-13/tests/integration_test.rs}}
```

</Listing>

A _tests_ mappa minden fájlja külön crate, ezért a könyvtárunkat minden
tesztcrate hatókörébe be kell hoznunk. Emiatt írjuk a kód elejére a `use
adder::add_two;` sort, amelyre az egységtesztekben nem volt szükség.

A _tests/integration_test.rs_ fájlban egyetlen kódrészletet sem kell a
`#[cfg(test)]` annotációval ellátnunk. A Cargo különlegesen kezeli a _tests_
mappát, és az itt lévő fájlokat csak akkor fordítja le, amikor a `cargo test`
parancsot futtatjuk. Futtasd most a `cargo test` parancsot:

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-13/output.txt}}
```

A kimenet három szakasza az egységteszteket, az integrációs tesztet és a
dokumentációs teszteket tartalmazza. Fontos, hogy ha egy szakaszban bármelyik
teszt elbukik, a következő szakaszok nem futnak le. Ha például egy egységteszt
elbukik, az integrációs és a dokumentációs tesztekhez nem lesz kimenet, mert
ezek a tesztek csak akkor futnak le, ha minden egységteszt sikeres.

Az egységtesztek első szakasza ugyanolyan, mint amilyet eddig is láttunk:
minden egységteszthez egy sor (egy `internal` nevű, amelyet a 11-12.
kódrészletben adtunk hozzá), majd egy összesítő sor az egységtesztekhez.

Az integrációs tesztek szakasza a `Running tests/integration_test.rs` sorral
kezdődik. Ezután az adott integrációs teszt minden tesztfüggvényéhez tartozik
egy sor, majd egy összesítő sor az integrációs teszt eredményeiről, közvetlenül
a `Doc-tests adder` szakasz kezdete előtt.

Minden integrációs tesztfájlnak saját szakasza van, így ha további fájlokat
adunk a _tests_ mappához, több integrációs tesztszakasz is lesz.

Egy adott integrációs tesztfüggvényt továbbra is futtathatunk úgy, hogy a
tesztfüggvény nevét argumentumként átadjuk a `cargo test`-nek. Egy adott
integrációs tesztfájl összes tesztjének futtatásához használd a `cargo test`
`--test` argumentumát, utána pedig a fájl nevét:

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-05-single-integration/output.txt}}
```

Ez a parancs csak a _tests/integration_test.rs_ fájlban lévő teszteket
futtatja.

#### Almodulok az integrációs tesztekben {#submodules-in-integration-tests}

Ahogy egyre több integrációs tesztet adsz hozzá, érdemes lehet több fájlt
létrehozni a _tests_ mappában, hogy rendszerezd őket; a tesztfüggvényeket
például az általuk tesztelt funkciók szerint csoportosíthatod. Ahogy korábban
említettük, a _tests_ mappa minden fájlja külön crate-ként fordul le, ami
hasznos ahhoz, hogy különálló hatóköröket hozzunk létre, és így jobban
utánozzuk azt, ahogyan a végfelhasználók a crate-edet használni fogják. Ez
azonban azt is jelenti, hogy a _tests_ mappa fájljai nem úgy viselkednek, mint
az _src_ fájljai, ahogy azt a 7. fejezetben a kód modulokra és fájlokra
bontásáról tanultad.

A _tests_ mappa fájljainak eltérő viselkedése akkor a legszembetűnőbb, ha van
néhány segédfüggvényed, amelyeket több integrációs tesztfájlban is használnál,
és a 7. fejezet [„Modulok szétválasztása külön
fájlokba”][separating-modules-into-files]<!-- ignore --> című szakaszának
lépéseit követve egy közös modulba próbálod kiemelni őket. Ha például
létrehozzuk a _tests/common.rs_ fájlt, és elhelyezünk benne egy `setup` nevű
függvényt, a `setup`-ba írhatunk olyan kódot, amelyet több tesztfájl több
tesztfüggvényéből is meg szeretnénk hívni:

<span class="filename">Fájlnév: tests/common.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-12-shared-test-code-problem/tests/common.rs}}
```

Ha újra lefuttatjuk a teszteket, a tesztkimenetben új szakasz jelenik meg a
_common.rs_ fájlhoz, pedig ez a fájl nem tartalmaz tesztfüggvényeket, és a
`setup` függvényt sem hívtuk meg sehonnan:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-12-shared-test-code-problem/output.txt}}
```

Nem ezt akartuk: hogy a `common` megjelenjen a teszteredmények között, mellette
a `running 0 tests` felirattal. Csak meg akartunk osztani némi kódot a többi
integrációs tesztfájllal. Hogy a `common` ne jelenjen meg a tesztkimenetben, a
_tests/common.rs_ helyett a _tests/common/mod.rs_ fájlt hozzuk létre. A
projektmappa most így néz ki:

```text
├── Cargo.lock
├── Cargo.toml
├── src
│   └── lib.rs
└── tests
    ├── common
    │   └── mod.rs
    └── integration_test.rs
```

Ez az a régebbi elnevezési konvenció, amelyet a Rust szintén ért, és amelyet
a 7. fejezet [„Alternatív fájlútvonalak”][alt-paths]<!-- ignore --> című
részében említettünk. Ha így nevezzük el a fájlt, a Rust nem kezeli a `common`
modult integrációs tesztfájlként. Amikor a `setup` függvény kódját áthelyezzük a
_tests/common/mod.rs_ fájlba, és töröljük a _tests/common.rs_ fájlt, a
tesztkimenetben többé nem jelenik meg a hozzá tartozó szakasz. A _tests_ mappa
almappáiban lévő fájlok nem fordulnak le külön crate-ként, és nincs saját
szakaszuk a tesztkimenetben.

Miután létrehoztuk a _tests/common/mod.rs_ fájlt, bármelyik
integrációs tesztfájlból használhatjuk modulként. Íme egy példa arra, hogyan
hívjuk meg a `setup` függvényt a _tests/integration_test.rs_ fájl
`it_adds_two` tesztjéből:

<span class="filename">Fájlnév: tests/integration_test.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-13-fix-shared-test-code-problem/tests/integration_test.rs}}
```

Figyeld meg, hogy a `mod common;` deklaráció ugyanolyan, mint a 7-21.
kódrészletben bemutatott moduldeklaráció. Ezután a tesztfüggvényben
meghívhatjuk a `common::setup()` függvényt.

#### Integrációs tesztek bináris crate-ekhez {#integration-tests-for-binary-crates}

Ha a projektünk egy bináris crate, amely csak egy _src/main.rs_ fájlt
tartalmaz, és nincs _src/lib.rs_ fájlja, akkor nem hozhatunk létre integrációs
teszteket a _tests_ mappában úgy, hogy az _src/main.rs_ fájlban definiált
függvényeket egy `use` utasítással a hatókörbe hozzuk. Csak a könyvtár crate-ek
tesznek elérhetővé olyan függvényeket, amelyeket más crate-ek használhatnak; a
bináris crate-eket önálló futtatásra szánják.

Ez az egyik oka annak, hogy a binárist biztosító Rust-projektekben egy egyszerű
_src/main.rs_ fájl található, amely az _src/lib.rs_ fájlban lévő logikát hívja
meg. Ezzel a felépítéssel az integrációs tesztek a `use` segítségével _tudják_
tesztelni a könyvtár crate-et, és elérhetővé tehetik a fontos funkciókat. Ha a
fontos funkciók működnek, az _src/main.rs_ fájlban lévő kis mennyiségű kód is
működni fog, és ezt a kis mennyiségű kódot nem kell tesztelni.

## Összefoglalás {#summary}

A Rust tesztelési funkcióival megadhatod, hogyan kell működnie a kódnak, így
biztosíthatod, hogy az elvárásaid szerint működjön akkor is, amikor
változtatsz rajta. Az egységtesztek a könyvtár különböző részeit külön-külön
próbálják ki, és privát implementációs részleteket is tesztelhetnek. Az
integrációs tesztek azt ellenőrzik, hogy a könyvtár több része helyesen
működik-e együtt, és a könyvtár nyilvános API-ján keresztül ugyanúgy tesztelik
a kódot, ahogyan a külső kód használni fogja. Bár a Rust típusrendszere és
tulajdonjogi szabályai segítenek megelőzni bizonyos hibafajtákat, a tesztek
továbbra is fontosak ahhoz, hogy csökkentsük a kód elvárt viselkedésével
kapcsolatos logikai hibákat.

Kombináljuk az ebben és a korábbi fejezetekben megszerzett tudást, és lássunk
neki egy projektnek!

[paths]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html
[separating-modules-into-files]: ch07-05-separating-modules-into-different-files.html
[alt-paths]: ch07-05-separating-modules-into-different-files.html#alternate-file-paths
