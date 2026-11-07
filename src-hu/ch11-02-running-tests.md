## A tesztek futtatásának szabályozása {#controlling-how-tests-are-run}

Ahogy a `cargo run` lefordítja a kódot, majd futtatja az eredményül kapott
binárist, úgy a `cargo test` tesztmódban fordítja le a kódot, és az eredményül
kapott tesztbinárist futtatja. A `cargo test` által előállított bináris
alapértelmezés szerint az összes tesztet párhuzamosan futtatja, és elfogja a
tesztek futása közben keletkező kimenetet: nem jeleníti meg, így könnyebb
elolvasni a teszteredményekhez tartozó kimenetet. Ezt az alapértelmezett
viselkedést azonban parancssori kapcsolókkal megváltoztathatod.

Egyes parancssori kapcsolók a `cargo test`-nek szólnak, mások az eredményül
kapott tesztbinárisnak. A kétféle argumentum elválasztásához először a `cargo
test`-nek szóló argumentumokat sorolod fel, utána jön a `--` elválasztó, majd a
tesztbinárisnak szólók. A `cargo test --help` kiírja a `cargo test`-tel
használható kapcsolókat, a `cargo test -- --help` pedig azokat, amelyeket az
elválasztó után adhatsz meg. Ezek a kapcsolók a [_The `rustc` Book_ „Tests”
szakaszában][tests] is dokumentálva vannak.

[tests]: https://doc.rust-lang.org/rustc/tests/index.html

### Tesztek párhuzamos vagy egymás utáni futtatása {#running-tests-in-parallel-or-consecutively}

Ha több tesztet futtatsz, azok alapértelmezés szerint szálak segítségével
párhuzamosan futnak, így hamarabb végeznek, és gyorsabban kapsz visszajelzést.
Mivel a tesztek egyszerre futnak, gondoskodnod kell arról, hogy ne függjenek
egymástól, sem semmilyen közös állapottól, beleértve a közös környezetet is,
például az aktuális munkamappát vagy a környezeti változókat.

Tegyük fel például, hogy minden teszted futtat valamilyen kódot, amely
létrehoz a lemezen egy _test-output.txt_ nevű fájlt, és adatokat ír bele. Ezután
minden teszt beolvassa a fájl tartalmát, és ellenőrzi, hogy a fájl egy adott
értéket tartalmaz, amely tesztenként más és más. Mivel a tesztek egyszerre
futnak, előfordulhat, hogy az egyik teszt felülírja a fájlt abban az időben,
amikor egy másik teszt már írt bele, de még nem olvasta vissza. A második teszt
ekkor elbukik – nem azért, mert a kód hibás, hanem mert a tesztek párhuzamos
futás közben zavarták egymást. Az egyik megoldás az, hogy minden teszt másik
fájlba ír; a másik az, hogy a teszteket egyenként futtatjuk.

Ha nem szeretnéd párhuzamosan futtatni a teszteket, vagy finomabban szeretnéd
szabályozni a használt szálak számát, a tesztbinárisnak átadhatod a
`--test-threads` kapcsolót a kívánt szálszámmal. Nézd meg a következő példát:

```console
$ cargo test -- --test-threads=1
```

A tesztszálak számát `1`-re állítjuk, vagyis azt mondjuk a programnak, hogy ne
használjon párhuzamosságot. A tesztek egy szálon való futtatása tovább tart,
mint a párhuzamos futtatás, viszont a tesztek nem zavarják egymást, ha közös
állapoton osztoznak.

### A függvények kimenetének megjelenítése {#showing-function-output}

Ha egy teszt sikeres, a Rust tesztkönyvtára alapértelmezés szerint elfog
mindent, amit a standard kimenetre írunk. Ha például egy tesztben meghívjuk a
`println!`-t, és a teszt sikeres, a `println!` kimenetét nem látjuk a
terminálban; csak azt a sort látjuk, amely jelzi, hogy a teszt sikeres volt. Ha
egy teszt elbukik, a standard kimenetre írt tartalmat a hibaüzenet többi
részével együtt látjuk.

Példaként a 11-10. kódrészletben van egy együgyű függvény, amely kiírja a
paramétere értékét, és 10-et ad vissza, valamint egy sikeres és egy elbukó
teszt.

<Listing number="11-10" file-name="src/lib.rs" caption="Tesztek egy olyan függvényhez, amely meghívja a `println!` makrót">

```rust,panics,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-10/src/lib.rs}}
```

</Listing>

Ha ezeket a teszteket a `cargo test` paranccsal futtatjuk, a következő
kimenetet látjuk:

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-10/output.txt}}
```

Figyeld meg, hogy ebben a kimenetben sehol sem látjuk az `I got the value 4`
szöveget, amelyet a sikeres teszt futása ír ki. Ezt a kimenetet a
tesztkönyvtár elfogta. Az elbukott teszt kimenete, az `I got the value 8`
viszont megjelenik a tesztösszesítő kimenet azon szakaszában, amely a teszt
kudarcának okát is mutatja.

Ha a sikeres tesztek kiírt értékeit is látni szeretnénk, a `--show-output`
kapcsolóval megmondhatjuk a Rustnak, hogy a sikeres tesztek kimenetét is
jelenítse meg:

```console
$ cargo test -- --show-output
```

Ha a 11-10. kódrészlet tesztjeit újra lefuttatjuk a `--show-output`
kapcsolóval, a következő kimenetet látjuk:

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-01-show-output/output.txt}}
```

### A tesztek egy részének futtatása név alapján {#running-a-subset-of-tests-by-name}

A teljes tesztkészlet futtatása néha sokáig tarthat. Ha a kód egy adott
részén dolgozol, előfordulhat, hogy csak az ahhoz a kódhoz tartozó teszteket
szeretnéd futtatni. Úgy választhatod ki, mely tesztek fussanak, hogy a futtatni
kívánt teszt vagy tesztek nevét argumentumként átadod a `cargo test`-nek.

Hogy bemutassuk, hogyan lehet a tesztek egy részét futtatni, először három
tesztet írunk az `add_two` függvényünkhöz, ahogy a 11-11. kódrészlet mutatja,
majd kiválasztjuk, melyiket futtassuk.

<Listing number="11-11" file-name="src/lib.rs" caption="Három teszt három különböző névvel">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-11/src/lib.rs}}
```

</Listing>

Ha argumentumok nélkül futtatjuk a teszteket, ahogy korábban láttuk, az összes
teszt párhuzamosan fut:

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-11/output.txt}}
```

#### Egyetlen teszt futtatása {#running-single-tests}

Bármelyik tesztfüggvény nevét átadhatjuk a `cargo test`-nek, hogy csak azt a
tesztet futtassa:

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-02-single-test/output.txt}}
```

Csak a `one_hundred` nevű teszt futott le; a másik kettő nem illeszkedett erre
a névre. A tesztkimenet a végén megjelenő `2 filtered out` felirattal jelzi,
hogy további tesztjeink is vannak, amelyek nem futottak le.

Így nem adhatjuk meg több teszt nevét; a `cargo test`-nek átadott értékek közül
csak az első számít. Van azonban mód több teszt futtatására is.

#### Több teszt futtatása szűréssel {#filtering-to-run-multiple-tests}

Megadhatjuk egy tesztnév egy részét is, és minden olyan teszt lefut, amelynek a
neve illeszkedik erre az értékre. Mivel például két tesztünk nevében is
szerepel az `add`, ezt a kettőt a `cargo test add` paranccsal futtathatjuk:

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-03-multiple-tests/output.txt}}
```

Ez a parancs az összes olyan tesztet lefuttatta, amelynek a nevében szerepel
az `add`, a `one_hundred` nevű tesztet pedig kiszűrte. Azt is érdemes
megjegyezni, hogy az a modul, amelyben a teszt található, a teszt nevének
része lesz, így egy modul összes tesztjét lefuttathatjuk, ha a modul nevére
szűrünk.

<!-- Old headings. Do not remove or links may break. -->

<a id="ignoring-some-tests-unless-specifically-requested"></a>

### Tesztek kihagyása, ha nem kérjük kifejezetten a futtatásukat {#ignoring-tests-unless-specifically-requested}

Néha egy-egy teszt végrehajtása nagyon időigényes lehet, ezért érdemes lehet
kihagyni őket a `cargo test` legtöbb futtatásakor. Ahelyett, hogy
argumentumként felsorolnád az összes tesztet, amelyet futtatni szeretnél, az
időigényes teszteket inkább megjelölheted az `ignore` attribútummal, hogy
kimaradjanak, ahogy itt látható:

<span class="filename">Fájlnév: src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-11-ignore-a-test/src/lib.rs:here}}
```

A `#[test]` után hozzáadjuk az `#[ignore]` sort ahhoz a teszthez, amelyet ki
szeretnénk hagyni. Ha most futtatjuk a teszteket, az `it_works` lefut, az
`expensive_test` viszont nem:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-11-ignore-a-test/output.txt}}
```

Az `expensive_test` függvény `ignored`-ként szerepel a listában. Ha csak a
kihagyott teszteket szeretnénk futtatni, a `cargo test -- --ignored` parancsot
használhatjuk:

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-04-running-ignored/output.txt}}
```

Azzal, hogy szabályozod, mely tesztek fussanak le, biztosíthatod, hogy a `cargo
test` gyorsan eredményt adjon. Amikor eljutsz arra a pontra, ahol már érdemes
megnézni az `ignored` tesztek eredményét, és van időd kivárni őket, futtathatod
helyette a `cargo test -- --ignored` parancsot. Ha az összes tesztet futtatni
szeretnéd, akár kihagyottak, akár nem, használd a `cargo test --
--include-ignored` parancsot.
