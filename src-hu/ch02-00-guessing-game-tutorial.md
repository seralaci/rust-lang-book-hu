# Számkitalálós játék programozása {#programming-a-guessing-game}

Vágjunk bele a Rustba egy közös, gyakorlati projekten keresztül! Ez a fejezet
néhány gyakori Rust-fogalmat mutat be, és megmutatja, hogyan használhatod őket
egy valódi programban. Megismered a `let`-et, a `match`-et, a metódusokat, a
társított függvényeket, a külső crate-eket és még sok mást! A következő
fejezetekben ezeket az ötleteket részletesebben is megvizsgáljuk. Ebben a
fejezetben csak az alapokat gyakorolod.

Egy klasszikus kezdő programozási feladatot valósítunk meg: egy számkitalálós
játékot. Így működik: a program generál egy véletlen egész számot 1 és 100
között. Ezután megkéri a játékost, hogy írjon be egy tippet. A tipp beírása után
a program jelzi, hogy a tipp túl kicsi vagy túl nagy. Ha a tipp helyes, a játék
kiír egy gratuláló üzenetet, és kilép.

## Új projekt létrehozása {#setting-up-a-new-project}

Új projekt létrehozásához lépj be az 1. fejezetben létrehozott _projects_
mappába, és hozz létre egy új projektet a Cargóval, így:

```console
$ cargo new guessing_game
$ cd guessing_game
```

Az első parancs, a `cargo new`, első argumentumként a projekt nevét
(`guessing_game`) kapja. A második parancs átlép az új projekt mappájába.

Nézd meg a generált _Cargo.toml_ fájlt:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial
rm -rf no-listing-01-cargo-new
cargo new no-listing-01-cargo-new --name guessing_game
cd no-listing-01-cargo-new
cargo run > output.txt 2>&1
cd ../../..
-->

<span class="filename">Fájlnév: Cargo.toml</span>

```toml
{{#include ../listings/ch02-guessing-game-tutorial/no-listing-01-cargo-new/Cargo.toml}}
```

Ahogy az 1. fejezetben láttad, a `cargo new` létrehoz neked egy „Hello, world!”
programot. Nézd meg a _src/main.rs_ fájlt:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/no-listing-01-cargo-new/src/main.rs}}
```

Most fordítsuk le és futtassuk ezt a „Hello, world!” programot egyetlen
lépésben, a `cargo run` paranccsal:

```console
{{#include ../listings/ch02-guessing-game-tutorial/no-listing-01-cargo-new/output.txt}}
```

A `run` parancs akkor jön jól, ha gyorsan kell iterálnod egy projekten, ahogy
ebben a játékban is tesszük: minden iterációt gyorsan kipróbálunk, mielőtt
továbblépnénk a következőre.

Nyisd meg újra a _src/main.rs_ fájlt. Az összes kódot ebbe a fájlba fogod írni.

## A tipp feldolgozása {#processing-a-guess}

A számkitalálós program első része bekéri a felhasználó bemenetét, feldolgozza
azt, és ellenőrzi, hogy a bemenet a várt formában van-e. Kezdésként lehetővé
tesszük, hogy a játékos beírjon egy tippet. Írd be a 2-1. kódrészletben látható
kódot a _src/main.rs_ fájlba.

<Listing number="2-1" file-name="src/main.rs" caption="Kód, amely bekér egy tippet a felhasználótól, és kiírja">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:all}}
```

</Listing>

Ez a kód sok információt tartalmaz, ezért nézzük át sorról sorra. Ahhoz, hogy
bekérjük a felhasználó bemenetét, majd kiírjuk az eredményt, a hatókörbe (scope)
kell hoznunk az `io` bemeneti/kimeneti könyvtárat. Az `io` könyvtár a standard
könyvtárból származik, amelyet `std` néven ismerünk:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:io}}
```

A Rust alapértelmezés szerint a standard könyvtárban definiált elemek egy
bizonyos készletét minden program hatókörébe behozza. Ezt a készletet
_prelude_-nak nevezzük, és a teljes tartalmát megtekintheted [a standard
könyvtár dokumentációjában][prelude].

Ha egy használni kívánt típus nincs benne a prelude-ban, akkor egy `use`
utasítással kifejezetten a hatókörbe kell hoznod. Az `std::io` könyvtár
használata számos hasznos funkciót ad, többek között a felhasználói bemenet
fogadásának képességét.

Ahogy az 1. fejezetben láttad, a `main` függvény a program belépési pontja:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:main}}
```

Az `fn` szintaxis egy új függvényt deklarál; a zárójelek, `()`, azt jelzik,
hogy nincsenek paraméterek; a kapcsos zárójel, `{`, pedig a függvény törzsét
nyitja meg.

Ahogy szintén az 1. fejezetben tanultad, a `println!` egy makró, amely egy
sztringet ír ki a képernyőre:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:print}}
```

Ez a kód egy felszólítást ír ki, amely közli, miről szól a játék, és bemenetet
kér a felhasználótól.

### Értékek tárolása változókban {#storing-values-with-variables}

Ezután létrehozunk egy _változót (variable)_ a felhasználói bemenet tárolására,
így:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:string}}
```

Most kezd érdekessé válni a program! Ebben a kis sorban sok minden történik. A
`let` utasítással hozzuk létre a változót. Íme egy másik példa:

```rust,ignore
let apples = 5;
```

Ez a sor létrehoz egy új, `apples` nevű változót, és az `5` értékhez köti. A
Rustban a változók alapértelmezés szerint nem módosíthatók (immutable), vagyis
ha egyszer értéket adtunk a változónak, az érték nem változik meg. Ezt a
fogalmat részletesen tárgyaljuk majd a 3. fejezet [„Változók és
módosíthatóság”][variables-and-mutability]<!-- ignore --> című szakaszában.
Ahhoz, hogy egy változó módosítható (mutable) legyen, a változó neve elé a
`mut` kulcsszót írjuk:

```rust,ignore
let apples = 5; // immutable
let mut bananas = 5; // mutable
```

> Megjegyzés: A `//` szintaxis egy megjegyzést kezd, amely a sor végéig tart. A
> Rust a megjegyzésekben lévő mindent figyelmen kívül hagy. A megjegyzésekről
> részletesebben a [3. fejezetben][comments]<!-- ignore --> lesz szó.

Visszatérve a számkitalálós programhoz: most már tudod, hogy a `let mut guess`
egy `guess` nevű, módosítható változót vezet be. Az egyenlőségjel (`=`) azt
mondja a Rustnak, hogy most valamit a változóhoz szeretnénk kötni. Az
egyenlőségjel jobb oldalán az az érték áll, amelyhez a `guess` kötődik: ez a
`String::new` hívásának eredménye, egy olyan függvényé, amely egy `String` új
példányát adja vissza. A [`String`][string]<!-- ignore --> a standard könyvtár
által biztosított sztringtípus, amely bővíthető, UTF-8 kódolású szöveget tárol.

A `::new` sorban szereplő `::` szintaxis azt jelzi, hogy a `new` a `String`
típus társított függvénye. A _társított függvény (associated function)_ olyan
függvény, amely egy típuson van megvalósítva, ebben az esetben a `String`-en.
Ez a `new` függvény egy új, üres sztringet hoz létre. Sok típuson találsz `new`
függvényt, mert ez a szokásos neve annak a függvénynek, amely valamilyen új
értéket hoz létre.

Összességében tehát a `let mut guess = String::new();` sor létrehozott egy
módosítható változót, amely jelenleg egy `String` új, üres példányához kötődik.
Huh!

### A felhasználói bemenet fogadása {#receiving-user-input}

Emlékezz, hogy a program első sorában a `use std::io;` segítségével behoztuk a
standard könyvtár bemeneti/kimeneti funkcióit. Most meghívjuk az `io` modul
`stdin` függvényét, amely lehetővé teszi, hogy kezeljük a felhasználói
bemenetet:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:read}}
```

Ha a program elején nem importáltuk volna az `io` modult a `use std::io;`
sorral, akkor is használhatnánk a függvényt, ha a hívást `std::io::stdin`
alakban írnánk. Az `stdin` függvény az
[`std::io::Stdin`][iostdin]<!-- ignore --> egy példányát adja vissza, amely a
terminálod standard bemenetére mutató leírót (handle) reprezentáló típus.

Ezután a `.read_line(&mut guess)` sor meghívja a [`read_line`][read_line]<!--
ignore --> metódust a standard bemenet leíróján, hogy bekérje a felhasználó
bemenetét. A `&mut guess`-t is átadjuk a `read_line`-nak argumentumként, hogy
megmondjuk neki, melyik sztringben tárolja a felhasználói bemenetet. A
`read_line` feladata az, hogy bármit, amit a felhasználó a standard bemenetre
gépel, hozzáfűzzön egy sztringhez (annak tartalmának felülírása nélkül), ezért
ezt a sztringet adjuk át argumentumként. A sztring argumentumnak módosíthatónak
kell lennie, hogy a metódus megváltoztathassa a sztring tartalmát.

A `&` azt jelzi, hogy ez az argumentum egy _referencia (reference)_, amellyel a
kódod több része is hozzáférhet ugyanahhoz az adathoz anélkül, hogy azt többször
át kellene másolni a memóriába. A referenciák összetett nyelvi elemek, és a Rust
egyik fő előnye, hogy milyen biztonságos és egyszerű a referenciák használata. A
program befejezéséhez nem kell sok részletet tudnod róluk. Egyelőre csak annyit
kell tudnod, hogy a változókhoz hasonlóan a referenciák is alapértelmezés
szerint nem módosíthatók. Ezért kell `&guess` helyett `&mut guess`-t írnod, hogy
módosíthatóvá tedd. (A 4. fejezet részletesebben elmagyarázza a referenciákat.)

<!-- Old headings. Do not remove or links may break. -->

<a id="handling-potential-failure-with-the-result-type"></a>

### Az esetleges hibák kezelése a `Result`-tal {#handling-potential-failure-with-result}

Még mindig ugyanazon a kódsoron dolgozunk. Most egy harmadik szövegsort
tárgyalunk, de vedd észre, hogy ez még mindig egyetlen logikai kódsor része. A
következő rész ez a metódus:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:expect}}
```

Ezt a kódot így is írhattuk volna:

```rust,ignore
io::stdin().read_line(&mut guess).expect("Failed to read line");
```

Egy hosszú sort azonban nehéz olvasni, ezért jobb felosztani. Amikor egy
metódust a `.method_name()` szintaxissal hívsz meg, gyakran érdemes sortörést és
más szóközöket beiktatni a hosszú sorok tördeléséhez. Most nézzük meg, mit
csinál ez a sor.

Ahogy korábban említettük, a `read_line` beleteszi a felhasználó által beírt
szöveget az általunk átadott sztringbe, de emellett egy `Result` értéket is
visszaad. A [`Result`][result]<!-- ignore --> egy
[_felsorolás típus (enumeration)_][enums]<!-- ignore -->, amelyet gyakran
_enum_-nak hívnak: olyan típus, amely több lehetséges állapot egyikében lehet.
Az egyes lehetséges állapotokat _változatoknak (variants)_ nevezzük.

A [6. fejezet][enums]<!-- ignore --> részletesebben foglalkozik az enumokkal. A
`Result` típusok célja a hibakezeléshez szükséges információk kódolása.

A `Result` változatai az `Ok` és az `Err`. Az `Ok` változat azt jelzi, hogy a
művelet sikeres volt, és tartalmazza a sikeresen előállított értéket. Az `Err`
változat azt jelenti, hogy a művelet sikertelen volt, és információt tartalmaz
arról, hogyan vagy miért hiúsult meg a művelet.

A `Result` típusú értékeknek, mint bármely típus értékeinek, vannak rajtuk
definiált metódusaik. A `Result` egy példányának van egy
[`expect` metódusa][expect]<!-- ignore -->, amelyet meghívhatsz. Ha a `Result`
adott példánya `Err` érték, az `expect` összeomlasztja a programot, és kiírja
azt az üzenetet, amelyet argumentumként átadtál az `expect`-nek. Ha a
`read_line` metódus `Err`-t ad vissza, az valószínűleg az alatta lévő operációs
rendszerből érkező hiba következménye. Ha a `Result` adott példánya `Ok` érték,
az `expect` veszi az `Ok` által tárolt visszatérési értéket, és csak ezt az
értéket adja vissza neked, hogy használhasd. Ebben az esetben ez az érték a
felhasználói bemenet bájtjainak száma.

Ha nem hívod meg az `expect`-et, a program lefordul, de figyelmeztetést kapsz:

```console
{{#include ../listings/ch02-guessing-game-tutorial/no-listing-02-without-expect/output.txt}}
```

A Rust figyelmeztet, hogy nem használtad fel a `read_line` által visszaadott
`Result` értéket, ami azt jelzi, hogy a program nem kezelt egy lehetséges hibát.

A figyelmeztetés elnémításának helyes módja az, hogy ténylegesen megírjuk a
hibakezelő kódot, de a mi esetünkben csak össze szeretnénk omlasztani a
programot, ha probléma lép fel, így használhatjuk az `expect`-et. A hibákból
való helyreállításról a [9. fejezetben][recover]<!-- ignore --> tanulsz majd.

### Értékek kiírása a `println!` helyőrzőivel {#printing-values-with-println-placeholders}

A záró kapcsos zárójelen kívül már csak egy sort kell megbeszélnünk az eddigi
kódból:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:print_guess}}
```

Ez a sor kiírja azt a sztringet, amely most már a felhasználó bemenetét
tartalmazza. A `{}` kapcsos zárójelpár egy helyőrző (placeholder): képzeld el a
`{}`-t úgy, mint egy kis rákollót, amely a helyén tart egy értéket. Egy változó
értékének kiírásakor a változó neve a kapcsos zárójelek közé kerülhet. Egy
kifejezés kiértékelésének eredményét úgy írhatod ki, hogy üres kapcsos
zárójeleket helyezel a formázó sztringbe, majd a formázó sztring után
vesszővel elválasztva felsorolod azokat a kifejezéseket, amelyeket az egyes üres
kapcsos zárójeles helyőrzőkbe szeretnél kiírni, ugyanabban a sorrendben. Egy
változó és egy kifejezés eredményének kiírása egyetlen `println!` hívásban így
nézne ki:

```rust
let x = 5;
let y = 10;

println!("x = {x} and y + 2 = {}", y + 2);
```

Ez a kód azt írná ki, hogy `x = 5 and y + 2 = 12`.

### Az első rész kipróbálása {#testing-the-first-part}

Próbáljuk ki a számkitalálós játék első részét. Futtasd a `cargo run`
paranccsal:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-01/
cargo clean
cargo run
input 6 -->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 6.44s
     Running `target/debug/guessing_game`
Guess the number!
Please input your guess.
6
You guessed: 6
```

Ezen a ponton a játék első része elkészült: bekérjük a bemenetet a
billentyűzetről, majd kiírjuk.

## A titkos szám generálása {#generating-a-secret-number}

Ezután generálnunk kell egy titkos számot, amelyet a felhasználó megpróbál
kitalálni. A titkos számnak minden alkalommal másnak kell lennie, hogy a játékot
többször is élvezetes legyen játszani. Egy 1 és 100 közötti véletlen számot
használunk, hogy a játék ne legyen túl nehéz. A Rust standard könyvtára még nem
tartalmaz véletlenszám-generáló funkciót. A Rust csapat azonban biztosít egy
ilyen funkciót nyújtó [`rand` crate-et][randcrate].

<!-- Old headings. Do not remove or links may break. -->
<a id="using-a-crate-to-get-more-functionality"></a>

### A funkcionalitás bővítése egy crate-tel {#increasing-functionality-with-a-crate}

Emlékezz: a crate Rust-forrásfájlok gyűjteménye. Az eddig épített projektünk egy
bináris crate, vagyis egy futtatható állomány. A `rand` crate egy könyvtár
crate, amely más programokban való felhasználásra szánt kódot tartalmaz, és
önmagában nem futtatható.

A Cargo a külső crate-ek koordinálásában igazán kiemelkedő. Mielőtt a `rand`-ot
használó kódot írhatnánk, módosítanunk kell a _Cargo.toml_ fájlt, hogy
függőségként (dependency) felvegyük a `rand` crate-et. Nyisd meg most ezt a
fájlt, és add hozzá a következő sort a végére, a Cargo által neked létrehozott
`[dependencies]` szakaszfejléc alá. Ügyelj arra, hogy a `rand`-ot pontosan úgy
add meg, ahogy mi, ezzel a verziószámmal, különben előfordulhat, hogy az
útmutató kódpéldái nem fognak működni:

<!-- When updating the version of `rand` used, also update the version of
`rand` used in these files so they all match:

* ch01-01-installation.md
* ch07-04-bringing-paths-into-scope-with-the-use-keyword.md
* ch14-03-cargo-workspaces.md
-->

<span class="filename">Fájlnév: Cargo.toml</span>

```toml
{{#include ../listings/ch02-guessing-game-tutorial/listing-02-02/Cargo.toml:8:}}
```

A _Cargo.toml_ fájlban minden, ami egy fejlécet követ, annak a szakasznak a
része, amely egészen a következő szakasz kezdetéig tart. A `[dependencies]`
szakaszban adod meg a Cargónak, hogy a projekted mely külső crate-ektől függ,
és ezeknek a crate-eknek mely verzióira van szükséged. Ebben az esetben a `rand`
crate-et a `0.10.1` szemantikus verziómegadással határozzuk meg. A Cargo érti a
[szemantikus verziókezelést (Semantic Versioning)][semver]<!-- ignore -->
(néha _SemVer_ néven is emlegetik), amely a verziószámok írásának egy
szabványa. A `0.10.1` megadás valójában a `^0.10.1` rövidítése, ami bármely
olyan verziót jelent, amely legalább 0.10.1, de 0.11.0 alatti.

A Cargo úgy tekinti, hogy ezeknek a verzióknak a nyilvános API-ja kompatibilis
a 0.10.1-es verzióéval, és ez a megadás biztosítja, hogy a legfrissebb olyan
javítókiadást (patch release) kapd meg, amellyel az ebben a fejezetben szereplő
kód még lefordul. A 0.11.0-s vagy annál újabb verzióknál nem garantált, hogy
ugyanaz az API-juk, mint amit a következő példák használnak.

Most, a kód módosítása nélkül, buildeljük le a projektet, ahogy a 2-2.
kódrészlet mutatja.

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-02/
rm Cargo.lock
cargo clean
cargo build -->

<Listing number="2-2" caption="A `cargo build` futtatásának kimenete, miután a `rand` crate-et függőségként hozzáadtuk">

```console
$ cargo build
    Updating crates.io index
     Locking 8 packages to latest Rust 1.96.0 compatible versions
  Downloaded rand_core v0.10.1
  Downloaded chacha20 v0.10.1
  Downloaded rand v0.10.1
  Downloaded 3 crates (162.9KiB) in 0.59s
   Compiling libc v0.2.186
   Compiling rand_core v0.10.1
   Compiling getrandom v0.4.3
   Compiling cfg-if v1.0.4
   Compiling chacha20 v0.10.1
   Compiling rand v0.10.1
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 2.03s
```

</Listing>

Lehet, hogy más verziószámokat látsz (de a SemVernek köszönhetően mind
kompatibilis lesz a kóddal!), és más sorokat (az operációs rendszertől
függően), és a sorok sorrendje is eltérhet.

Amikor egy külső függőséget veszünk fel, a Cargo letölti mindannak a legfrissebb
verzióját, amire az adott függőségnek szüksége van, a _regiszterből
(registry)_, amely a [Crates.io][cratesio] adatainak másolata. A Crates.io az a
hely, ahová a Rust-ökoszisztéma tagjai feltöltik nyílt forráskódú
Rust-projektjeiket, hogy mások is használhassák őket.

A regiszter frissítése után a Cargo ellenőrzi a `[dependencies]` szakaszt, és
letölti a felsorolt crate-ek közül azokat, amelyek még nincsenek letöltve. Ebben
az esetben, bár csak a `rand`-ot adtuk meg függőségként, a Cargo azokat a
további crate-eket is letöltötte, amelyektől a `rand` működése függ. A crate-ek
letöltése után a Rust lefordítja őket, majd a rendelkezésre álló függőségekkel
lefordítja a projektet.

Ha módosítás nélkül azonnal újra lefuttatod a `cargo build` parancsot, a
`Finished` soron kívül semmilyen kimenetet nem kapsz. A Cargo tudja, hogy már
letöltötte és lefordította a függőségeket, és te semmit sem változtattál rajtuk
a _Cargo.toml_ fájlban. A Cargo azt is tudja, hogy a kódodon sem változtattál
semmit, így azt sem fordítja újra. Mivel nincs tennivalója, egyszerűen kilép.

Ha megnyitod a _src/main.rs_ fájlt, végzel rajta egy apró módosítást, majd
elmented és újra buildeled, csak két sornyi kimenetet fogsz látni:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-02/
touch src/main.rs
cargo build -->

```console
$ cargo build
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.13s
```

Ezek a sorok azt mutatják, hogy a Cargo csak a _src/main.rs_ fájlon végzett apró
módosításoddal frissíti a buildet. A függőségeid nem változtak, így a Cargo
tudja, hogy újrahasznosíthatja azt, amit már letöltött és lefordított hozzájuk.

<!-- Old headings. Do not remove or links may break. -->
<a id="ensuring-reproducible-builds-with-the-cargo-lock-file"></a>

#### Reprodukálható buildek biztosítása {#ensuring-reproducible-builds}

A Cargónak van egy mechanizmusa, amely biztosítja, hogy ugyanazt a terméket
építhesd újra minden alkalommal, amikor te vagy bárki más lefordítja a kódodat:
a Cargo csak az általad megadott függőségverziókat használja, amíg mást nem
jelzel. Tegyük fel például, hogy jövő héten megjelenik a `rand` crate 0.10.2-es
verziója, amely egy fontos hibajavítást tartalmaz, de egy regressziót is, amely
elrontja a kódodat. Ennek kezelésére a Rust az első `cargo build` futtatásakor
létrehozza a _Cargo.lock_ fájlt, így ez most már megtalálható a _guessing_game_
mappában.

Amikor először buildelsz egy projektet, a Cargo kideríti a függőségek összes
olyan verzióját, amely megfelel a feltételeknek, majd ezeket beírja a
_Cargo.lock_ fájlba. Amikor a jövőben buildeled a projektet, a Cargo látni
fogja, hogy a _Cargo.lock_ fájl létezik, és az abban megadott verziókat
használja ahelyett, hogy újra elvégezné a verziók kiderítésének teljes munkáját.
Így automatikusan reprodukálható buildet kapsz. Más szóval, a _Cargo.lock_
fájlnak köszönhetően a projekted a 0.10.1-es verziónál marad, amíg kifejezetten
nem frissítesz. Mivel a _Cargo.lock_ fájl fontos a reprodukálható buildekhez,
gyakran a projekt többi kódjával együtt a verziókezelőbe is bekerül.

#### Crate frissítése új verzióra {#updating-a-crate-to-get-a-new-version}

Amikor _valóban_ frissíteni szeretnél egy crate-et, a Cargo erre az `update`
parancsot biztosítja, amely figyelmen kívül hagyja a _Cargo.lock_ fájlt, és
kideríti az összes legfrissebb verziót, amely megfelel a _Cargo.toml_ fájlban
megadott követelményeidnek. A Cargo ezután ezeket a verziókat írja a
_Cargo.lock_ fájlba. Ettől eltekintve a Cargo alapértelmezés szerint csak a
0.10.1-nél nagyobb és 0.11.0-nál kisebb verziókat keresi. Ha a `rand` crate két
új verziót adott ki, a 0.10.2-t és a 0.999.0-t, akkor a `cargo update`
futtatásakor a következőt látnád:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-02/
cargo update
assuming there is a new version of rand; otherwise use another update
as a guide to creating the hypothetical output shown here -->

```console
$ cargo update
    Updating crates.io index
     Locking 1 package to latest Rust 1.96.0 compatible version
    Updating rand v0.10.1 -> v0.10.2 (available: v0.999.0)
```

A Cargo figyelmen kívül hagyja a 0.999.0-s kiadást. Ezen a ponton azt is
észrevennéd, hogy a _Cargo.lock_ fájlod megváltozott, és jelzi, hogy a `rand`
crate most használt verziója 0.10.2. Ha a `rand` 0.999.0-s verzióját vagy a
0.999._x_ sorozat bármely verzióját szeretnéd használni, a _Cargo.toml_ fájlt
így kellene módosítanod (ezt a változtatást valójában ne végezd el, mert a
következő példák azt feltételezik, hogy a `rand` 0.10-s verzióját használod):

```toml
[dependencies]
rand = "0.999.0"
```

A következő `cargo build` futtatásakor a Cargo frissíti az elérhető crate-ek
regiszterét, és az általad megadott új verzió alapján újraértékeli a `rand`-ra
vonatkozó követelményeidet.

Még sok mindent lehetne mondani a [Cargóról][doccargo]<!-- ignore --> és
[ökoszisztémájáról][doccratesio]<!-- ignore -->, ezekről a 14. fejezetben lesz
szó, de egyelőre ennyit kell tudnod. A Cargo nagyon megkönnyíti a könyvtárak
újrafelhasználását, így a rustaceanek kisebb projekteket írhatnak, amelyeket
több csomagból raknak össze.

### Véletlen szám generálása {#generating-a-random-number}

Kezdjük el használni a `rand`-ot a kitalálandó szám generálásához. A következő
lépés a _src/main.rs_ frissítése, ahogy a 2-3. kódrészlet mutatja.

<Listing number="2-3" file-name="src/main.rs" caption="Kód hozzáadása egy véletlen szám generálásához">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-03/src/main.rs:all}}
```

</Listing>

Először hozzáadjuk a `use rand::prelude::*;` sort. A `prelude` modul a `rand`
crate leggyakrabban használt részeit tartalmazza, a `use` pedig ezeket az
elemeket elérhetővé teszi a programunk hatókörében.

Ezután középen két sort adunk hozzá. Az első sorban meghívjuk a `rand::rng`
függvényt, amely megadja azt a konkrét véletlenszám-generátort, amelyet
használni fogunk: egy olyat, amely az aktuális végrehajtási szálhoz tartozik, és
amelynek kezdőértékét (seed) az operációs rendszer adja. Ezután meghívjuk a
véletlenszám-generátor `random_range` metódusát. Ezt a metódust az `RngExt`
trait definiálja, amely a `rand::prelude` modul része, amit a `use
rand::prelude::*;` utasítással hoztunk be a hatókörbe. A `random_range` metódus
egy tartománykifejezést vár argumentumként, és egy véletlen számot generál a
tartományon belül. Az itt használt tartománykifejezés `start..=end` alakú, és az
alsó és a felső határt is magában foglalja, ezért az `1..=100`-at kell megadnunk
ahhoz, hogy egy 1 és 100 közötti számot kérjünk.

> Megjegyzés: Nem fogod magadtól tudni, hogy mit kell a hatókörbe hozni, és egy
> crate mely metódusait és függvényeit kell meghívni, ezért minden crate-hez
> tartozik dokumentáció a használatára vonatkozó utasításokkal. A Cargo egy
> másik remek funkciója, hogy a `cargo doc --open` parancs futtatása helyben
> lefordítja az összes függőséged által biztosított dokumentációt, és megnyitja
> a böngésződben. Ha például a `rand` crate egyéb funkciói érdekelnek, futtasd
> a `cargo doc --open` parancsot, és kattints a bal oldali sávban a `rand`-ra.

A második új sor kiírja a titkos számot. Ez a program fejlesztése közben
hasznos, hogy ki tudjuk próbálni, de a végső változatból törölni fogjuk. Nem sok
értelme van a játéknak, ha a program rögtön az indulásakor kiírja a választ!

Próbáld ki néhányszor a programot:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-03/
cargo run
4
cargo run
5
-->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.02s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 7
Please input your guess.
4
You guessed: 4

$ cargo run
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.02s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 83
Please input your guess.
5
You guessed: 5
```

Különböző véletlen számokat kell kapnod, és mindegyiknek 1 és 100 közé kell
esnie. Ha figyelmeztetéseket kapsz, nyugodtan figyelmen kívül hagyhatod őket. Ha
hibákat kapsz, ellenőrizd, hogy a *Cargo.toml* fájlodban `rand = "0.10.1"`
szerepel-e, mert a `rand` jövőbeli verzióinak más lehet az API-ja, de a `0.10`
sorozat bármely verziójának működnie kell az ebben a fejezetben szereplő kóddal.

## A tipp összehasonlítása a titkos számmal {#comparing-the-guess-to-the-secret-number}

Most, hogy megvan a felhasználói bemenet és egy véletlen szám, össze tudjuk
hasonlítani őket. Ezt a lépést a 2-4. kódrészlet mutatja. Vedd figyelembe, hogy
ez a kód még nem fordul le, ahogy majd el is magyarázzuk.

<Listing number="2-4" file-name="src/main.rs" caption="Két szám összehasonlításának lehetséges visszatérési értékeinek kezelése">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-04/src/main.rs:here}}
```

</Listing>

Először egy újabb `use` utasítást adunk hozzá, amely a standard könyvtárból egy
`std::cmp::Ordering` nevű típust hoz be a hatókörbe. Az `Ordering` típus szintén
egy enum, amelynek változatai a `Less`, a `Greater` és az `Equal`. Ez az a három
lehetséges kimenet, amely két érték összehasonlításakor előállhat.

Ezután öt új sort adunk hozzá a végén, amelyek az `Ordering` típust használják.
A `cmp` metódus két értéket hasonlít össze, és bármin meghívható, ami
összehasonlítható. Egy referenciát vár arra, amivel össze akarod hasonlítani:
itt a `guess`-t hasonlítja össze a `secret_number`-rel. Ezután az `Ordering`
enum egy változatát adja vissza, amelyet a `use` utasítással hoztunk be a
hatókörbe. Egy [`match`][match]<!-- ignore --> kifejezéssel döntjük el, mi
történjen ezután, attól függően, hogy az `Ordering` melyik változatát adta
vissza a `cmp` hívása a `guess` és a `secret_number` értékeivel.

A `match` kifejezés _ágakból (arms)_ áll. Egy ág egy _mintából (pattern)_ áll,
amelyre illesztünk, valamint abból a kódból, amelynek le kell futnia, ha a
`match`-nek átadott érték illeszkedik az ág mintájára. A Rust veszi a
`match`-nek átadott értéket, és sorban végignézi az egyes ágak mintáit. A minták
és a `match` szerkezet a Rust hatékony nyelvi elemei: lehetővé teszik, hogy
kifejezd a kódod által esetleg tapasztalt helyzetek sokféleségét, és
gondoskodnak róla, hogy mindegyiket kezeld. Ezekről a nyelvi elemekről a 6.,
illetve a 19. fejezetben lesz részletesen szó.

Nézzünk végig egy példát az itt használt `match` kifejezéssel. Tegyük fel, hogy
a felhasználó 50-et tippelt, és a véletlenszerűen generált titkos szám ezúttal
38.

Amikor a kód összehasonlítja az 50-et a 38-cal, a `cmp` metódus
`Ordering::Greater`-t ad vissza, mert az 50 nagyobb, mint a 38. A `match`
kifejezés megkapja az `Ordering::Greater` értéket, és elkezdi ellenőrizni az
egyes ágak mintáit. Megnézi az első ág mintáját, az `Ordering::Less`-t, és
látja, hogy az `Ordering::Greater` érték nem illeszkedik az `Ordering::Less`-re,
ezért figyelmen kívül hagyja az ág kódját, és továbblép a következő ágra. A
következő ág mintája az `Ordering::Greater`, amely _illeszkedik_ az
`Ordering::Greater`-re! Az ághoz tartozó kód lefut, és kiírja a képernyőre, hogy
`Too big!`. A `match` kifejezés az első sikeres illeszkedés után véget ér, így
ebben az esetben az utolsó ágat már meg sem nézi.

A 2-4. kódrészlet kódja azonban még nem fordul le. Próbáljuk ki:

<!--
The error numbers in this output should be that of the code **WITHOUT** the
anchor or snip comments
-->

```console
{{#include ../listings/ch02-guessing-game-tutorial/listing-02-04/output.txt}}
```

A hiba lényege, hogy _eltérő típusok (mismatched types)_ szerepelnek. A Rust
erős, statikus típusrendszerrel rendelkezik. Ugyanakkor típuskövetkeztetéssel
(type inference) is. Amikor azt írtuk, hogy `let mut guess = String::new()`, a
Rust ki tudta következtetni, hogy a `guess`-nek `String`-nek kell lennie, és nem
kellett kiírnunk a típust. A `secret_number` viszont egy számtípus. A Rust
számtípusai közül több is tárolhat 1 és 100 közötti értéket: az `i32`, egy 32
bites szám; az `u32`, egy előjel nélküli 32 bites szám; az `i64`, egy 64 bites
szám; és mások is. Ha mást nem adunk meg, a Rust alapértelmezés szerint az
`i32`-t használja, így ez lesz a `secret_number` típusa, hacsak máshol nem adsz
meg olyan típusinformációt, amely miatt a Rust egy másik számtípusra
következtetne. A hiba oka az, hogy a Rust nem tud összehasonlítani egy sztringet
és egy számtípust.

Végső soron a program által bemenetként beolvasott `String`-et számtípussá
szeretnénk alakítani, hogy számként hasonlíthassuk össze a titkos számmal. Ezt
úgy tesszük meg, hogy a következő sort adjuk a `main` függvény törzséhez:

<span class="filename">Fájlnév: src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/no-listing-03-convert-string-to-number/src/main.rs:here}}
```

A sor a következő:

```rust,ignore
let guess: u32 = guess.trim().parse().expect("Please type a number!");
```

Létrehozunk egy `guess` nevű változót. De várjunk csak, nincs már a programban
egy `guess` nevű változó? De van, ám a Rust készségesen megengedi, hogy a
`guess` korábbi értékét egy újjal árnyékoljuk. Az _árnyékolás (shadowing)_
lehetővé teszi, hogy újrahasznosítsuk a `guess` változónevet, ahelyett hogy két
különálló változót kellene létrehoznunk, például `guess_str`-t és `guess`-t.
Erről részletesebben a [3. fejezetben][shadowing]<!-- ignore --> lesz szó, de
egyelőre elég annyit tudnod, hogy ezt a funkciót gyakran használjuk, amikor egy
értéket egyik típusból egy másikba szeretnénk alakítani.

Ezt az új változót a `guess.trim().parse()` kifejezéshez kötjük. A kifejezésben
szereplő `guess` az eredeti `guess` változóra hivatkozik, amely sztringként
tartalmazta a bemenetet. Egy `String` példány `trim` metódusa eltávolítja az
elején és a végén lévő összes szóközt, amit meg kell tennünk, mielőtt a
sztringet `u32`-vé alakíthatnánk, amely csak számadatot tartalmazhat. A
felhasználónak meg kell nyomnia az <kbd>enter</kbd> billentyűt, hogy a
`read_line` elfogadja a tippjét, ez pedig egy újsor karaktert ad a sztringhez.
Ha például a felhasználó beírja az <kbd>5</kbd>-öt, és megnyomja az
<kbd>enter</kbd>-t, a `guess` így néz ki: `5\n`. A `\n` az „újsort” jelöli.
(Windowson az <kbd>enter</kbd> lenyomása egy kocsivissza és egy újsor karaktert
eredményez: `\r\n`.) A `trim` metódus eltávolítja a `\n`-t vagy a `\r\n`-t, így
csak az `5` marad.

A [sztringek `parse` metódusa][parse]<!-- ignore --> egy sztringet egy másik
típusra alakít. Itt arra használjuk, hogy egy sztringet számmá alakítsunk. A
`let guess: u32` segítségével meg kell mondanunk a Rustnak, pontosan milyen
számtípust szeretnénk. A `guess` utáni kettőspont (`:`) azt mondja a Rustnak,
hogy annotálni fogjuk a változó típusát. A Rustnak van néhány beépített
számtípusa; az itt látható `u32` egy előjel nélküli, 32 bites egész szám. Kis
pozitív számokhoz jó alapértelmezett választás. A többi számtípusról a
[3. fejezetben][integers]<!-- ignore --> tanulsz majd.

Ezenfelül az `u32` annotáció ebben a példaprogramban és a `secret_number`-rel
való összehasonlítás azt eredményezi, hogy a Rust arra következtet, hogy a
`secret_number`-nek is `u32`-nek kell lennie. Így most már két azonos típusú
érték között történik az összehasonlítás!

A `parse` metódus csak olyan karaktereken működik, amelyek logikusan számmá
alakíthatók, ezért könnyen hibát okozhat. Ha például a sztring `A👍%`-ot
tartalmazna, azt semmiképp sem lehetne számmá alakítani. Mivel meghiúsulhat, a
`parse` metódus egy `Result` típust ad vissza, ugyanúgy, ahogy a `read_line`
metódus is (erről korábban, [„Az esetleges hibák kezelése a
`Result`-tal”](#handling-potential-failure-with-result)<!-- ignore --> című
részben volt szó). Ezt a `Result`-ot ugyanúgy kezeljük, ismét az `expect`
metódussal. Ha a `parse` egy `Err` `Result` változatot ad vissza, mert nem
tudott számot előállítani a sztringből, az `expect` hívás összeomlasztja a
játékot, és kiírja az általunk megadott üzenetet. Ha a `parse` sikeresen számmá
tudja alakítani a sztringet, a `Result` `Ok` változatát adja vissza, az `expect`
pedig visszaadja az általunk kívánt számot az `Ok` értékből.

Futtassuk most a programot:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/no-listing-03-convert-string-to-number/
touch src/main.rs
cargo run
  76
-->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.26s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 58
Please input your guess.
  76
You guessed: 76
Too big!
```

Remek! Bár a tipp elé szóközöket írtunk, a program mégis rájött, hogy a
felhasználó 76-ot tippelt. Futtasd le néhányszor a programot, hogy ellenőrizd a
különböző viselkedést különféle bemenetekre: találd el a számot, tippelj egy túl
nagy számot, és tippelj egy túl kicsi számot.

A játék nagy része már működik, de a felhasználó csak egyszer tippelhet.
Változtassunk ezen egy ciklus hozzáadásával!

## Több tipp lehetővé tétele ciklussal {#allowing-multiple-guesses-with-looping}

A `loop` kulcsszó egy végtelen ciklust hoz létre. Hozzáadunk egy ciklust, hogy a
felhasználóknak több esélyük legyen kitalálni a számot:

<span class="filename">Fájlnév: src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/no-listing-04-looping/src/main.rs:here}}
```

Ahogy láthatod, a tippet bekérő felszólítástól kezdve mindent áthelyeztünk egy
ciklusba. Ügyelj arra, hogy a ciklus belsejében lévő sorokat további négy
szóközzel beljebb húzd, majd futtasd újra a programot. A program most már
örökké újabb és újabb tippet fog kérni, ami valójában egy új problémát vet fel.
Úgy tűnik, a felhasználó nem tud kilépni!

A felhasználó természetesen bármikor megszakíthatja a programot a
<kbd>ctrl</kbd>-<kbd>C</kbd> billentyűkombinációval. De van egy másik mód is,
hogy elmeneküljünk ettől a telhetetlen szörnyetegtől, ahogy azt a `parse`
tárgyalásánál, [„A tipp összehasonlítása a titkos
számmal”](#comparing-the-guess-to-the-secret-number)<!-- ignore --> című
részben említettük: ha a felhasználó nem számot ír be, a program összeomlik. Ezt
kihasználhatjuk arra, hogy a felhasználó kiléphessen, ahogy itt látható:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/no-listing-04-looping/
touch src/main.rs
cargo run
(too small guess)
(too big guess)
(correct guess)
quit
-->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.23s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 59
Please input your guess.
45
You guessed: 45
Too small!
Please input your guess.
60
You guessed: 60
Too big!
Please input your guess.
59
You guessed: 59
You win!
Please input your guess.
quit

thread 'main' (6694925) panicked at src/main.rs:28:47:
Please type a number!: ParseIntError { kind: InvalidDigit }
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

A `quit` beírása kilép a játékból, de ahogy észreveheted, bármilyen más, nem
szám bemenet beírása is. Ez enyhén szólva sem ideális; azt szeretnénk, hogy a
játék akkor is leálljon, ha a felhasználó kitalálta a helyes számot.

### Kilépés helyes tipp után {#quitting-after-a-correct-guess}

Programozzuk be a játékot úgy, hogy kilépjen, ha a felhasználó nyer, egy `break`
utasítás hozzáadásával:

<span class="filename">Fájlnév: src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/no-listing-05-quitting/src/main.rs:here}}
```

Ha a `You win!` után hozzáadjuk a `break` sort, a program kilép a ciklusból,
amikor a felhasználó helyesen kitalálja a titkos számot. A ciklusból való
kilépés egyben a programból való kilépést is jelenti, mert a ciklus a `main`
utolsó része.

### Érvénytelen bemenet kezelése {#handling-invalid-input}

Hogy tovább finomítsuk a játék viselkedését, ahelyett, hogy összeomlasztanánk a
programot, amikor a felhasználó nem számot ír be, érjük el, hogy a játék
figyelmen kívül hagyja a nem szám bemenetet, így a felhasználó folytathatja a
tippelést. Ezt úgy tehetjük meg, hogy módosítjuk azt a sort, ahol a `guess`-t
`String`-ből `u32`-vé alakítjuk, ahogy a 2-5. kódrészlet mutatja.

<Listing number="2-5" file-name="src/main.rs" caption="Nem szám tipp figyelmen kívül hagyása és újabb tipp kérése a program összeomlasztása helyett">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-05/src/main.rs:here}}
```

</Listing>

Az `expect` hívásról egy `match` kifejezésre váltunk, hogy a hiba esetén történő
összeomlás helyett kezeljük a hibát. Emlékezz, hogy a `parse` egy `Result`
típust ad vissza, a `Result` pedig egy enum, amelynek `Ok` és `Err` változatai
vannak. Itt egy `match` kifejezést használunk, ahogy a `cmp` metódus `Ordering`
eredményénél is tettük.

Ha a `parse` sikeresen számmá tudja alakítani a sztringet, egy `Ok` értéket ad
vissza, amely tartalmazza a kapott számot. Ez az `Ok` érték illeszkedik az első
ág mintájára, és a `match` kifejezés egyszerűen visszaadja azt a `num` értéket,
amelyet a `parse` előállított, és az `Ok` értékbe tett. Ez a szám pontosan oda
kerül, ahová szeretnénk: az általunk létrehozott új `guess` változóba.

Ha a `parse` _nem_ tudja számmá alakítani a sztringet, egy `Err` értéket ad
vissza, amely további információt tartalmaz a hibáról. Az `Err` érték nem
illeszkedik az első `match` ág `Ok(num)` mintájára, de illeszkedik a második ág
`Err(_)` mintájára. Az aláhúzásjel, `_`, egy mindent elfogó érték; ebben a
példában azt mondjuk, hogy minden `Err` értékre illeszkedni szeretnénk,
függetlenül attól, milyen információ van bennük. Így a program a második ág
kódját, a `continue`-t hajtja végre, amely azt mondja a programnak, hogy lépjen
a `loop` következő iterációjára, és kérjen egy újabb tippet. Így a program
gyakorlatilag figyelmen kívül hagyja az összes hibát, amellyel a `parse`
találkozhat!

Most már a program minden részének az elvárt módon kell működnie. Próbáljuk ki:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-05/
cargo run
(too small guess)
(too big guess)
foo
(correct guess)
-->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.13s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 61
Please input your guess.
10
You guessed: 10
Too small!
Please input your guess.
99
You guessed: 99
Too big!
Please input your guess.
foo
Please input your guess.
61
You guessed: 61
You win!
```

Nagyszerű! Egy utolsó apró igazítással befejezzük a számkitalálós játékot.
Emlékezz, hogy a program még mindig kiírja a titkos számot. Ez a teszteléshez
jól jött, de tönkreteszi a játékot. Töröljük azt a `println!`-t, amely a titkos
számot írja ki. A 2-6. kódrészlet mutatja a végleges kódot.

<Listing number="2-6" file-name="src/main.rs" caption="A számkitalálós játék teljes kódja">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-06/src/main.rs}}
```

</Listing>

Ezen a ponton sikeresen elkészítetted a számkitalálós játékot. Gratulálunk!

## Összefoglalás {#summary}

Ez a projekt gyakorlati módon mutatott be számos új Rust-fogalmat: a `let`-et, a
`match`-et, a függvényeket, a külső crate-ek használatát és még sok mást. A
következő néhány fejezetben ezeket a fogalmakat részletesebben is megismered. A
3. fejezet olyan fogalmakkal foglalkozik, amelyek a legtöbb programozási
nyelvben megtalálhatók, például a változókkal, az adattípusokkal és a
függvényekkel, és megmutatja, hogyan használhatod őket a Rustban. A 4. fejezet a
tulajdonjogot (ownership) vizsgálja, azt a tulajdonságot, amely a Rustot
megkülönbözteti más nyelvektől. Az 5. fejezet a struktúrákat (struct) és a
metódusszintaxist tárgyalja, a 6. fejezet pedig elmagyarázza, hogyan működnek az
enumok.

[prelude]: https://doc.rust-lang.org/std/prelude/index.html
[variables-and-mutability]: ch03-01-variables-and-mutability.html#variables-and-mutability
[comments]: ch03-04-comments.html
[string]: https://doc.rust-lang.org/std/string/struct.String.html
[iostdin]: https://doc.rust-lang.org/std/io/struct.Stdin.html
[read_line]: https://doc.rust-lang.org/std/io/struct.Stdin.html#method.read_line
[result]: https://doc.rust-lang.org/std/result/enum.Result.html
[enums]: ch06-00-enums.html
[expect]: https://doc.rust-lang.org/std/result/enum.Result.html#method.expect
[recover]: ch09-02-recoverable-errors-with-result.html
[randcrate]: https://crates.io/crates/rand
[semver]: http://semver.org
[cratesio]: https://crates.io/
[doccargo]: https://doc.rust-lang.org/cargo/
[doccratesio]: https://doc.rust-lang.org/cargo/reference/publishing.html
[match]: ch06-02-match.html
[shadowing]: ch03-01-variables-and-mutability.html#shadowing
[parse]: https://doc.rust-lang.org/std/primitive.str.html#method.parse
[integers]: ch03-02-data-types.html#integer-types
