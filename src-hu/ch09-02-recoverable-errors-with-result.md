## Helyrehozható hibák a `Result` típussal {#recoverable-errors-with-result}

A legtöbb hiba nem elég súlyos ahhoz, hogy a program teljes leállítását
indokolja. Néha, amikor egy függvény meghiúsul, annak olyan oka van, amelyet
könnyen értelmezhetsz, és reagálhatsz rá. Ha például megpróbálsz megnyitni egy
fájlt, és a művelet azért hiúsul meg, mert a fájl nem létezik, akkor a folyamat
leállítása helyett talán inkább létrehoznád a fájlt.

Emlékezz vissza: a 2. fejezet [„Az esetleges hibák kezelése a
`Result`-tal”][handle_failure]<!-- ignore --> szakaszában láttuk, hogy a
`Result` enum két változattal, az `Ok`-val és az `Err`-rel van definiálva, így:

```rust
enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

A `T` és az `E` generikus típusparaméterek: a generikus típusokról
részletesebben a 10. fejezetben lesz szó. Most csak annyit kell tudnod, hogy a
`T` annak az értéknek a típusát jelöli, amelyet siker esetén az `Ok`
változatban kapunk vissza, az `E` pedig annak a hibának a típusát, amelyet
kudarc esetén az `Err` változatban kapunk vissza. Mivel a `Result` ezekkel a
generikus típusparaméterekkel rendelkezik, a `Result` típust és a rajta
definiált függvényeket sok különböző helyzetben használhatjuk, ahol a
visszaadni kívánt sikeres érték és hibaérték típusa eltérhet.

Hívjunk meg egy olyan függvényt, amely `Result` értéket ad vissza, mert a
függvény meghiúsulhat. A 9-3. kódrészletben megpróbálunk megnyitni egy fájlt.

<Listing number="9-3" file-name="src/main.rs" caption="Egy fájl megnyitása">

```rust
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-03/src/main.rs}}
```

</Listing>

A `File::open` visszatérési típusa `Result<T, E>`. A `T` generikus paramétert
a `File::open` implementációja a sikeres érték típusával, a `std::fs::File`
típussal töltötte ki, amely egy fájlleíró (file handle). A hibaértékben
használt `E` típusa `std::io::Error`. Ez a visszatérési típus azt jelenti, hogy
a `File::open` hívása sikerülhet, és visszaadhat egy fájlleírót, amelyből
olvashatunk, vagy amelybe írhatunk. A függvényhívás meg is hiúsulhat: például
lehet, hogy a fájl nem létezik, vagy nincs jogosultságunk hozzáférni. A
`File::open` függvénynek valahogy közölnie kell velünk, hogy sikerült-e vagy
sem, és egyúttal meg kell adnia nekünk vagy a fájlleírót, vagy a hiba
adatait. Pontosan ezt az információt közvetíti a `Result` enum.

Ha a `File::open` sikerrel jár, a `greeting_file_result` változó értéke egy
fájlleírót tartalmazó `Ok` példány lesz. Ha meghiúsul, a
`greeting_file_result` értéke egy olyan `Err` példány lesz, amely további
információt tartalmaz a bekövetkezett hiba fajtájáról.

Ki kell egészítenünk a 9-3. kódrészlet kódját, hogy a `File::open` által
visszaadott értéktől függően különböző műveleteket végezzünk. A 9-4.
kódrészlet a `Result` kezelésének egyik módját mutatja egy alapvető eszközzel,
a 6. fejezetben tárgyalt `match` kifejezéssel.

<Listing number="9-4" file-name="src/main.rs" caption="A visszaadható `Result` változatok kezelése egy `match` kifejezéssel">

```rust,should_panic
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-04/src/main.rs}}
```

</Listing>

Figyeld meg, hogy az `Option` enumhoz hasonlóan a `Result` enumot és
változatait is hatókörbe hozza a prelude, így a `match` ágakban nem kell az
`Ok` és az `Err` változat elé kiírnunk a `Result::` előtagot.

Ha az eredmény `Ok`, ez a kód kiveszi a belső `file` értéket az `Ok`
változatból, és ezt a fájlleíró értéket a `greeting_file` változóhoz rendeljük.
A `match` után a fájlleírót olvasásra vagy írásra használhatjuk.

A `match` másik ága azt az esetet kezeli, amikor a `File::open` egy `Err`
értéket ad vissza. Ebben a példában a `panic!` makró meghívását választottuk.
Ha az aktuális mappánkban nincs _hello.txt_ nevű fájl, és lefuttatjuk ezt a
kódot, a `panic!` makró a következő kimenetet adja:

```console
{{#include ../listings/ch09-error-handling/listing-09-04/output.txt}}
```

Szokás szerint ez a kimenet pontosan megmondja, mi romlott el.

### Illesztés különböző hibákra {#matching-on-different-errors}

A 9-4. kódrészlet kódja mindenképpen `panic!`-ot hív, bármi is legyen az oka
annak, hogy a `File::open` meghiúsult. Mi azonban különböző okok esetén
különbözőképpen szeretnénk eljárni. Ha a `File::open` azért hiúsult meg, mert
a fájl nem létezik, létre szeretnénk hozni a fájlt, és visszaadni az új fájl
leíróját. Ha a `File::open` bármilyen más okból hiúsult meg – például mert
nem volt jogosultságunk megnyitni a fájlt –, továbbra is azt szeretnénk, hogy
a kód ugyanúgy `panic!`-ot hívjon, mint a 9-4. kódrészletben. Ehhez egy belső
`match` kifejezést adunk hozzá, ahogy a 9-5. kódrészlet mutatja.

<Listing number="9-5" file-name="src/main.rs" caption="Különböző fajtájú hibák eltérő kezelése">

<!-- ignore this test because otherwise it creates hello.txt which causes other
tests to fail lol -->

```rust,ignore
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-05/src/main.rs}}
```

</Listing>

A `File::open` által az `Err` változatban visszaadott érték típusa
`io::Error`, amely a standard könyvtár által biztosított struktúra. Ennek a
struktúrának van egy `kind` metódusa, amelyet meghívva egy `io::ErrorKind`
értéket kapunk. Az `io::ErrorKind` enumot a standard könyvtár biztosítja, és a
változatai azokat a különböző hibafajtákat képviselik, amelyek egy `io`
műveletből eredhetnek. Mi az `ErrorKind::NotFound` változatot szeretnénk
használni, amely azt jelzi, hogy a megnyitni kívánt fájl még nem létezik. A
`greeting_file_result` értékére tehát illesztünk, de van egy belső illesztésünk
is az `error.kind()` értékére.

A belső illesztésben azt szeretnénk ellenőrizni, hogy az `error.kind()` által
visszaadott érték az `ErrorKind` enum `NotFound` változata-e. Ha igen,
megpróbáljuk létrehozni a fájlt a `File::create` segítségével. Mivel azonban a
`File::create` is meghiúsulhat, a belső `match` kifejezésben szükségünk van egy
második ágra is. Ha a fájlt nem sikerül létrehozni, egy másik hibaüzenet íródik
ki. A külső `match` második ága változatlan marad, így a program a hiányzó fájl
hibáján kívül minden más hiba esetén pánikol.

> #### Alternatívák a `match` használatára a `Result<T, E>` esetén {#alternatives-to-using-match-with-resultt-e}
>
> Ez rengeteg `match`! A `match` kifejezés nagyon hasznos, de egyben nagyon
> kezdetleges eszköz is. A 13. fejezetben megismered a closure-öket, amelyeket
> a `Result<T, E>` típuson definiált számos metódussal együtt használhatunk.
> Ezek a metódusok tömörebbek lehetnek a `match` használatánál, amikor a
> kódodban `Result<T, E>` értékeket kezelsz.
>
> Íme például egy másik módja annak, hogy ugyanazt a logikát írjuk meg, mint a
> 9-5. kódrészletben, ezúttal closure-ök és az `unwrap_or_else` metódus
> segítségével:
>
> <!-- CAN'T EXTRACT SEE https://github.com/rust-lang/mdBook/issues/1127 -->
>
> ```rust,ignore
> use std::fs::File;
> use std::io::ErrorKind;
>
> fn main() {
>     let greeting_file = File::open("hello.txt").unwrap_or_else(|error| {
>         if error.kind() == ErrorKind::NotFound {
>             File::create("hello.txt").unwrap_or_else(|error| {
>                 panic!("Problem creating the file: {error:?}");
>             })
>         } else {
>             panic!("Problem opening the file: {error:?}");
>         }
>     });
> }
> ```
>
> Bár ez a kód ugyanúgy viselkedik, mint a 9-5. kódrészlet, egyetlen `match`
> kifejezést sem tartalmaz, és könnyebben olvasható. Térj vissza ehhez a
> példához, miután elolvastad a 13. fejezetet, és nézd meg az `unwrap_or_else`
> metódust a standard könyvtár dokumentációjában. Sok más ilyen metódus is
> segíthet rendet tenni a hatalmas, egymásba ágyazott `match` kifejezések
> között, amikor hibákkal dolgozol.

<!-- Old headings. Do not remove or links may break. -->

<a id="shortcuts-for-panic-on-error-unwrap-and-expect"></a>

#### Rövidítések a hiba esetén történő pánikhoz {#shortcuts-for-panic-on-error}

A `match` használata elég jól működik, de kissé bőbeszédű lehet, és nem
mindig fejezi ki jól a szándékot. A `Result<T, E>` típuson számos segédmetódus
van definiálva különféle, specifikusabb feladatokra. Az `unwrap` metódus egy
rövidítés, amely pontosan úgy van megvalósítva, mint a 9-4. kódrészletben
írt `match` kifejezés. Ha a `Result` értéke az `Ok` változat, az `unwrap`
visszaadja az `Ok`-ban lévő értéket. Ha a `Result` az `Err` változat, az
`unwrap` meghívja helyettünk a `panic!` makrót. Íme egy példa az `unwrap`
működésére:

<Listing file-name="src/main.rs">

```rust,should_panic
{{#rustdoc_include ../listings/ch09-error-handling/no-listing-04-unwrap/src/main.rs}}
```

</Listing>

Ha ezt a kódot _hello.txt_ fájl nélkül futtatjuk, az `unwrap` metódus által
végrehajtott `panic!` hívás hibaüzenetét látjuk:

<!-- manual-regeneration
cd listings/ch09-error-handling/no-listing-04-unwrap
cargo run
copy and paste relevant text
-->

```text
thread 'main' panicked at src/main.rs:4:49:
called `Result::unwrap()` on an `Err` value: Os { code: 2, kind: NotFound, message: "No such file or directory" }
```

Hasonlóképpen, az `expect` metódussal a `panic!` hibaüzenetét is mi
választhatjuk meg. Ha az `unwrap` helyett az `expect` metódust használjuk, és
jó hibaüzeneteket adunk meg, kifejezhetjük a szándékunkat, és könnyebben
felderíthetjük egy pánik forrását. Az `expect` szintaxisa így néz ki:

<Listing file-name="src/main.rs">

```rust,should_panic
{{#rustdoc_include ../listings/ch09-error-handling/no-listing-05-expect/src/main.rs}}
```

</Listing>

Az `expect` metódust ugyanúgy használjuk, mint az `unwrap`-et: visszaadja a
fájlleírót, vagy meghívja a `panic!` makrót. Az `expect` által a `panic!`
hívásakor használt hibaüzenet az a paraméter lesz, amelyet az `expect`
metódusnak átadunk, nem pedig a `panic!` alapértelmezett üzenete, amelyet az
`unwrap` használ. Így néz ki:

<!-- manual-regeneration
cd listings/ch09-error-handling/no-listing-05-expect
cargo run
copy and paste relevant text
-->

```text
thread 'main' panicked at src/main.rs:5:10:
hello.txt should be included in this project: Os { code: 2, kind: NotFound, message: "No such file or directory" }
```

Éles környezetbe szánt kódban a legtöbb rustacean az `unwrap` helyett az
`expect` metódust választja, és több kontextust ad arról, miért várható, hogy
a művelet mindig sikerül. Így ha a feltételezéseidről valaha kiderül, hogy
tévesek, több információ áll rendelkezésedre a hibakereséshez.

### Hibák továbbadása {#propagating-errors}

Ha egy függvény implementációja olyasmit hív meg, ami meghiúsulhat, akkor
ahelyett, hogy magában a függvényben kezelnéd a hibát, visszaadhatod azt a
hívó kódnak, hogy az döntse el, mit tegyen. Ezt a hiba _továbbadásának
(propagating)_ nevezzük, és nagyobb irányítást ad a hívó kódnak, ahol több
olyan információ vagy logika állhat rendelkezésre, amely meghatározza, hogyan
kell kezelni a hibát, mint amennyi a te kódod kontextusában elérhető.

A 9-6. kódrészlet például egy olyan függvényt mutat, amely egy felhasználónevet
olvas be egy fájlból. Ha a fájl nem létezik, vagy nem olvasható, ez a függvény
visszaadja ezeket a hibákat a függvényt meghívó kódnak.

<Listing number="9-6" file-name="src/main.rs" caption="Egy függvény, amely a `match` segítségével adja vissza a hibákat a hívó kódnak">

<!-- Deliberately not using rustdoc_include here; the `main` function in the
file panics. We do want to include it for reader experimentation purposes, but
don't want to include it for rustdoc testing purposes. -->

```rust
{{#include ../listings/ch09-error-handling/listing-09-06/src/main.rs:here}}
```

</Listing>

Ez a függvény sokkal rövidebben is megírható, de a hibakezelés megismerése
érdekében először sok mindent kézzel csinálunk; a végén megmutatjuk a rövidebb
módot is. Nézzük meg először a függvény visszatérési típusát:
`Result<String, io::Error>`. Ez azt jelenti, hogy a függvény `Result<T, E>`
típusú értéket ad vissza, ahol a `T` generikus paramétert a `String` konkrét
típus, az `E` generikus típust pedig az `io::Error` konkrét típus tölti ki.

Ha ez a függvény minden probléma nélkül sikerrel jár, az őt meghívó kód egy
`String`-et tartalmazó `Ok` értéket kap – azt a `username` értéket, amelyet ez
a függvény a fájlból beolvasott. Ha a függvény bármilyen problémába ütközik, a
hívó kód egy `Err` értéket kap, amely egy `io::Error` példányt tartalmaz,
további információkkal arról, mik voltak a problémák. Azért választottuk az
`io::Error` típust a függvény visszatérési típusaként, mert éppen ez a típusa a
függvény törzsében hívott mindkét, esetleg meghiúsuló művelet által visszaadott
hibaértéknek: a `File::open` függvénynek és a `read_to_string` metódusnak.

A függvény törzse a `File::open` függvény meghívásával kezdődik. Ezután a
`Result` értéket a 9-4. kódrészletbelihez hasonló `match` kifejezéssel
kezeljük. Ha a `File::open` sikerrel jár, a `file` mintaváltozóban lévő
fájlleíró lesz a `username_file` módosítható változó értéke, és a függvény
folytatódik. Az `Err` esetben a `panic!` hívása helyett a `return` kulcsszóval
idő előtt kilépünk az egész függvényből, és a `File::open` hibaértékét – amely
most az `e` mintaváltozóban van – a függvény hibaértékeként visszaadjuk a hívó
kódnak.

Ha tehát van egy fájlleírónk a `username_file` változóban, a függvény ezután
létrehoz egy új `String`-et a `username` változóban, és meghívja a
`read_to_string` metódust a `username_file` változóban lévő fájlleírón, hogy a
fájl tartalmát beolvassa a `username` változóba. A `read_to_string` metódus is
`Result` értéket ad vissza, mert meghiúsulhat, még akkor is, ha a `File::open`
sikerrel járt. Ezért egy újabb `match` kifejezésre van szükségünk ennek a
`Result` értéknek a kezeléséhez: ha a `read_to_string` sikerrel jár, a
függvényünk is sikerrel járt, és visszaadjuk a fájlból származó, most a
`username` változóban lévő felhasználónevet egy `Ok`-ba csomagolva. Ha a
`read_to_string` meghiúsul, a hibaértéket ugyanúgy adjuk vissza, ahogy a
`File::open` visszatérési értékét kezelő `match` kifejezésben. A `return`
kulcsszót azonban nem kell explicit módon kiírnunk, mert ez a függvény utolsó
kifejezése.

Az ezt a kódot meghívó kód ezután vagy egy felhasználónevet tartalmazó `Ok`
értéket, vagy egy `io::Error` értéket tartalmazó `Err` értéket kap, és ezt kell
kezelnie. A hívó kódon múlik, mit kezd ezekkel az értékekkel. Ha a hívó kód
`Err` értéket kap, meghívhatja például a `panic!` makrót, és összeomlaszthatja
a programot, használhat egy alapértelmezett felhasználónevet, vagy a fájlon
kívül máshonnan is megkeresheti a felhasználónevet. Nincs elég információnk
arról, mit próbál valójában tenni a hívó kód, ezért minden sikeres vagy
hibainformációt felfelé továbbadunk, hogy az megfelelően kezelhesse.

A hibák továbbadásának ez a mintája annyira gyakori a Rustban, hogy a Rust
ennek megkönnyítésére biztosítja a `?` kérdőjel-operátort.

<!-- Old headings. Do not remove or links may break. -->

<a id="a-shortcut-for-propagating-errors-the--operator"></a>

#### A `?` operátor mint rövidítés {#the--operator-shortcut}

A 9-7. kódrészlet a `read_username_from_file` olyan implementációját mutatja,
amely ugyanazt a funkcionalitást nyújtja, mint a 9-6. kódrészletben, de ez az
implementáció a `?` operátort használja.

<Listing number="9-7" file-name="src/main.rs" caption="Egy függvény, amely a `?` operátor segítségével adja vissza a hibákat a hívó kódnak">

<!-- Deliberately not using rustdoc_include here; the `main` function in the
file panics. We do want to include it for reader experimentation purposes, but
don't want to include it for rustdoc testing purposes. -->

```rust
{{#include ../listings/ch09-error-handling/listing-09-07/src/main.rs:here}}
```

</Listing>

A `Result` érték után írt `?` úgy van definiálva, hogy majdnem ugyanúgy
működjön, mint azok a `match` kifejezések, amelyeket a 9-6. kódrészletben a
`Result` értékek kezelésére definiáltunk. Ha a `Result` értéke `Ok`, az `Ok`-ban
lévő érték lesz a kifejezés eredménye, és a program folytatódik. Ha az érték
`Err`, az `Err` az egész függvényből visszatér, mintha a `return` kulcsszót
használtuk volna, így a hibaérték továbbadódik a hívó kódnak.

Van egy különbség aközött, amit a 9-6. kódrészlet `match` kifejezése tesz, és
aközött, amit a `?` operátor tesz: azok a hibaértékek, amelyeken a `?`
operátort meghívjuk, átmennek a `from` függvényen, amely a standard könyvtár
`From` traitjében van definiálva, és értékek egyik típusból a másikba való
átalakítására szolgál. Amikor a `?` operátor meghívja a `from` függvényt, a
kapott hibatípus átalakul az aktuális függvény visszatérési típusában
definiált hibatípussá. Ez akkor hasznos, ha egy függvény egyetlen hibatípust ad
vissza, amely a függvény meghiúsulásának összes lehetséges módját képviseli,
még akkor is, ha az egyes részek sokféle okból hiúsulhatnak meg.

Módosíthatnánk például a 9-7. kódrészlet `read_username_from_file` függvényét
úgy, hogy egy általunk definiált, `OurError` nevű egyéni hibatípust adjon
vissza. Ha definiáljuk az `impl From<io::Error> for OurError` implementációt
is, amely egy `io::Error` értékből létrehoz egy `OurError` példányt, akkor a
`read_username_from_file` törzsében lévő `?` operátorhívások meghívják a
`from` függvényt, és átalakítják a hibatípusokat anélkül, hogy bármilyen
további kódot kellene a függvényhez adnunk.

A 9-7. kódrészlet esetében a `File::open` hívás végén álló `?` az `Ok`-ban
lévő értéket adja a `username_file` változónak. Ha hiba történik, a `?`
operátor idő előtt kilép az egész függvényből, és a hívó kódnak adja az `Err`
értéket. Ugyanez érvényes a `read_to_string` hívás végén álló `?`-re is.

A `?` operátor sok ismétlődő sablonkódot (boilerplate) szüntet meg, és
egyszerűbbé teszi ennek a függvénynek az implementációját. Még tovább is
rövidíthetnénk ezt a kódot, ha a metódushívásokat közvetlenül a `?` után
láncolnánk, ahogy a 9-8. kódrészlet mutatja.

<Listing number="9-8" file-name="src/main.rs" caption="Metódushívások láncolása a `?` operátor után">

<!-- Deliberately not using rustdoc_include here; the `main` function in the
file panics. We do want to include it for reader experimentation purposes, but
don't want to include it for rustdoc testing purposes. -->

```rust
{{#include ../listings/ch09-error-handling/listing-09-08/src/main.rs:here}}
```

</Listing>

Az új `String` létrehozását a `username` változóban a függvény elejére
helyeztük; ez a rész nem változott. Ahelyett, hogy létrehoznánk a
`username_file` változót, a `read_to_string` hívását közvetlenül a
`File::open("hello.txt")?` eredményéhez láncoltuk. A `read_to_string` hívás
végén továbbra is ott van egy `?`, és továbbra is a `username` értéket
tartalmazó `Ok` értéket adjuk vissza, ha a `File::open` és a `read_to_string`
is sikerrel jár, ahelyett hogy hibát adnánk vissza. A működés ismét ugyanaz,
mint a 9-6. és a 9-7. kódrészletben; ez csak egy másik, kényelmesebb módja a
megírásának.

A 9-9. kódrészlet azt mutatja, hogyan tehetjük ezt még rövidebbé az
`fs::read_to_string` használatával.

<Listing number="9-9" file-name="src/main.rs" caption="Az `fs::read_to_string` használata a fájl megnyitása és beolvasása helyett">

<!-- Deliberately not using rustdoc_include here; the `main` function in the
file panics. We do want to include it for reader experimentation purposes, but
don't want to include it for rustdoc testing purposes. -->

```rust
{{#include ../listings/ch09-error-handling/listing-09-09/src/main.rs:here}}
```

</Listing>

Egy fájl beolvasása egy sztringbe meglehetősen gyakori művelet, ezért a
standard könyvtár biztosítja a kényelmes `fs::read_to_string` függvényt, amely
megnyitja a fájlt, létrehoz egy új `String`-et, beolvassa a fájl tartalmát,
elhelyezi azt ebben a `String`-ben, majd visszaadja. Természetesen az
`fs::read_to_string` használata nem adott volna lehetőséget arra, hogy a teljes
hibakezelést elmagyarázzuk, ezért először a hosszabb utat választottuk.

<!-- Old headings. Do not remove or links may break. -->

<a id="where-the--operator-can-be-used"></a>

#### Hol használható a `?` operátor? {#where-to-use-the--operator}

A `?` operátor csak olyan függvényekben használható, amelyek visszatérési
típusa kompatibilis azzal az értékkel, amelyen a `?` operátort használjuk.
Ennek az az oka, hogy a `?` operátor úgy van definiálva, hogy egy értékkel idő
előtt kilépjen a függvényből, ugyanúgy, mint a 9-6. kódrészletben definiált
`match` kifejezés. A 9-6. kódrészletben a `match` egy `Result` értéket
használt, és az idő előtti kilépést végző ág egy `Err(e)` értéket adott vissza.
A függvény visszatérési típusának `Result`-nak kell lennie, hogy kompatibilis
legyen ezzel a `return` utasítással.

A 9-10. kódrészletben nézzük meg, milyen hibát kapunk, ha a `?` operátort egy
olyan `main` függvényben használjuk, amelynek visszatérési típusa nem
kompatibilis annak az értéknek a típusával, amelyen a `?` operátort használjuk.

<Listing number="9-10" file-name="src/main.rs" caption="A `?` használata a `()` típust visszaadó `main` függvényben nem fordul le.">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-10/src/main.rs}}
```

</Listing>

Ez a kód megnyit egy fájlt, ami meghiúsulhat. A `?` operátor a `File::open`
által visszaadott `Result` érték után áll, de ennek a `main` függvénynek a
visszatérési típusa `()`, nem pedig `Result`. Amikor lefordítjuk ezt a kódot, a
következő hibaüzenetet kapjuk:

```console
{{#include ../listings/ch09-error-handling/listing-09-10/output.txt}}
```

Ez a hiba arra figyelmeztet, hogy a `?` operátort csak olyan függvényben
használhatjuk, amely `Result`, `Option` vagy más, a `FromResidual` traitet
megvalósító típust ad vissza.

A hiba kijavítására két lehetőséged van. Az egyik, hogy a függvényed
visszatérési típusát kompatibilissé teszed azzal az értékkel, amelyen a `?`
operátort használod, feltéve, hogy semmilyen megkötés nem akadályozza ezt. A
másik, hogy egy `match` kifejezéssel vagy a `Result<T, E>` valamelyik
metódusával kezeled a `Result<T, E>` értéket a helyzetnek megfelelő módon.

A hibaüzenet azt is megemlítette, hogy a `?` operátor `Option<T>` értékekkel
is használható. Ahogy a `?` operátort `Result` esetén, úgy `Option` esetén is
csak olyan függvényben használhatod, amely `Option` típust ad vissza. A `?`
operátor viselkedése `Option<T>` értéken hasonló a `Result<T, E>` értéken
mutatott viselkedéséhez: ha az érték `None`, a függvény ezen a ponton idő előtt
`None` értékkel tér vissza. Ha az érték `Some`, a `Some`-ban lévő érték lesz a
kifejezés eredménye, és a függvény folytatódik. A 9-11. kódrészlet egy olyan
függvényt mutat be, amely megkeresi a megadott szöveg első sorának utolsó
karakterét.

<Listing number="9-11" caption="A `?` operátor használata egy `Option<T>` értéken">

```rust
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-11/src/main.rs:here}}
```

</Listing>

Ez a függvény `Option<char>` típust ad vissza, mert lehetséges, hogy ott van
egy karakter, de az is lehetséges, hogy nincs. Ez a kód a `text`
sztringszelet-argumentumon meghívja a `lines` metódust, amely egy, a sztring
sorain végighaladó iterátort ad vissza. Mivel ez a függvény az első sort
szeretné megvizsgálni, meghívja az iterátoron a `next` metódust, hogy megkapja
az iterátor első értékét. Ha a `text` üres sztring, a `next` hívása `None`
értéket ad vissza, és ebben az esetben a `?` segítségével megállunk, és `None`
értékkel térünk vissza a `last_char_of_first_line` függvényből. Ha a `text`
nem üres sztring, a `next` egy olyan `Some` értéket ad vissza, amely a `text`
első sorának sztringszeletét tartalmazza.

A `?` kiveszi a sztringszeletet, és ezen a sztringszeleten meghívhatjuk a
`chars` metódust, hogy megkapjuk a karakterein végighaladó iterátort. Minket az
első sor utolsó karaktere érdekel, ezért meghívjuk a `last` metódust, hogy
visszakapjuk az iterátor utolsó elemét. Ez egy `Option`, mert lehetséges, hogy
az első sor üres sztring; például ha a `text` üres sorral kezdődik, de a többi
sorban vannak karakterek, mint a `"\nhi"` esetében. Ha azonban az első sornak
van utolsó karaktere, az a `Some` változatban kerül visszaadásra. A középen
álló `?` operátor tömör módot ad ennek a logikának a kifejezésére, így a
függvényt egyetlen sorban megvalósíthatjuk. Ha nem használhatnánk a `?`
operátort `Option` értéken, ezt a logikát több metódushívással vagy egy `match`
kifejezéssel kellene megvalósítanunk.

Figyeld meg, hogy a `?` operátort `Result` értéken olyan függvényben
használhatod, amely `Result` típust ad vissza, és `Option` értéken olyan
függvényben, amely `Option` típust ad vissza, de a kettőt nem keverheted. A `?`
operátor nem alakítja át automatikusan a `Result` értéket `Option` értékké vagy
fordítva; ilyen esetekben az átalakítást explicit módon végezheted el, például
a `Result` `ok` metódusával vagy az `Option` `ok_or` metódusával.

Eddig az összes általunk használt `main` függvény `()` típust adott vissza. A
`main` függvény különleges, mert egy futtatható program belépési és kilépési
pontja, és megkötések vonatkoznak arra, mi lehet a visszatérési típusa, hogy a
program az elvárt módon viselkedjen.

Szerencsére a `main` `Result<(), E>` típust is visszaadhat. A 9-12. kódrészlet
a 9-10. kódrészlet kódját tartalmazza, de a `main` visszatérési típusát
`Result<(), Box<dyn Error>>` típusra módosítottuk, és a végére egy `Ok(())`
visszatérési értéket adtunk. Ez a kód most már lefordul.

<Listing number="9-12" file-name="src/main.rs" caption="Ha a `main` `Result<(), E>` típust ad vissza, használhatjuk a `?` operátort `Result` értékeken.">

```rust,ignore
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-12/src/main.rs}}
```

</Listing>

A `Box<dyn Error>` típus egy trait objektum, amelyről a 18. fejezet [„Trait
objektumok használata a közös viselkedés absztrahálására”][trait-objects]<!--
ignore --> szakaszában lesz szó. Egyelőre a `Box<dyn Error>` kifejezést
olvashatod úgy, hogy „bármilyen hiba”. Egy `Box<dyn Error>` hibatípusú `main`
függvényben megengedett a `?` operátor használata `Result` értéken, mert így
bármilyen `Err` érték idő előtt visszaadható. Bár ennek a `main` függvénynek a
törzse mindig csak `std::io::Error` típusú hibákat ad vissza, a
`Box<dyn Error>` megadásával ez a szignatúra akkor is helyes marad, ha a `main`
törzsébe később más hibákat visszaadó kód is kerül.

Ha egy `main` függvény `Result<(), E>` típust ad vissza, a futtatható állomány
`0` értékkel lép ki, ha a `main` `Ok(())` értéket ad vissza, és nullától eltérő
értékkel, ha a `main` `Err` értéket ad vissza. A C-ben írt futtatható
állományok kilépéskor egész számot adnak vissza: a sikeresen kilépő programok
a `0` egész számot, a hibával kilépők pedig valamilyen `0`-tól eltérő egész
számot. A Rust is egész számokat ad vissza a futtatható állományokból, hogy
kompatibilis legyen ezzel a konvencióval.

A `main` függvény bármilyen típust visszaadhat, amely megvalósítja [a
`std::process::Termination` traitet][termination]<!-- ignore -->, amely egy
`ExitCode` értéket visszaadó `report` függvényt tartalmaz. A `Termination`
trait saját típusokra való megvalósításáról a standard könyvtár
dokumentációjában találsz további információt.

Most, hogy részletesen megismertük a `panic!` hívását és a `Result`
visszaadását, térjünk vissza arra a kérdésre, hogyan dönthetjük el, melyiket
mikor érdemes használni.

[handle_failure]: ch02-00-guessing-game-tutorial.html#handling-potential-failure-with-result
[trait-objects]: ch18-02-trait-objects.html#using-trait-objects-to-abstract-over-shared-behavior
[termination]: https://doc.rust-lang.org/std/process/trait.Termination.html
