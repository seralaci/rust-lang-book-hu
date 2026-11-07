## Példaprogram struktúrákkal {#an-example-program-using-structs}

Hogy megértsük, mikor érdemes struktúrákat használni, írjunk egy programot,
amely egy téglalap területét számítja ki. Először különálló változókkal
kezdünk, majd addig refaktoráljuk a programot, amíg végül struktúrákat nem
használunk helyettük.

Hozzunk létre a Cargóval egy új, _rectangles_ nevű bináris projektet, amely egy
pixelben megadott szélességű és magasságú téglalap területét számítja ki. Az
5-8. kódrészlet egy rövid programot mutat, amely a projektünk _src/main.rs_
fájljában pontosan ezt teszi meg, egy lehetséges módon.

<Listing number="5-8" file-name="src/main.rs" caption="Egy különálló szélesség- és magasságváltozóval megadott téglalap területének kiszámítása">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-08/src/main.rs:all}}
```

</Listing>

Most futtasd a programot a `cargo run` paranccsal:

```console
{{#include ../listings/ch05-using-structs-to-structure-related-data/listing-05-08/output.txt}}
```

Ez a kód sikeresen kiszámítja a téglalap területét úgy, hogy mindkét
méretével meghívja az `area` függvényt, de tehetünk még azért, hogy a kód
világosabb és olvashatóbb legyen.

A kód problémája az `area` szignatúrájában látszik:

```rust,ignore
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-08/src/main.rs:here}}
```

Az `area` függvénynek egy téglalap területét kellene kiszámítania, de az
általunk írt függvénynek két paramétere van, és a programunkból sehonnan sem
derül ki, hogy a paraméterek összetartoznak. Olvashatóbb és jobban kezelhető
lenne, ha a szélességet és a magasságot összecsoportosítanánk. Ennek egyik
módját, a tuple-ök használatát, már tárgyaltuk a 3. fejezet [„A tuple
típus”][the-tuple-type]<!-- ignore --> című szakaszában.

### Refaktorálás tuple-ökkel {#refactoring-with-tuples}

Az 5-9. kódrészlet a programunk egy másik, tuple-öket használó változatát
mutatja.

<Listing number="5-9" file-name="src/main.rs" caption="A téglalap szélességének és magasságának megadása egy tuple-lel">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-09/src/main.rs}}
```

</Listing>

Ez a program bizonyos szempontból jobb. A tuple-ök egy kis szerkezetet visznek
a kódba, és most már csak egy argumentumot adunk át. Más szempontból viszont ez
a változat kevésbé világos: a tuple-ök nem nevezik el az elemeiket, ezért
indexeléssel kell elérnünk a tuple részeit, ami kevésbé nyilvánvalóvá teszi a
számítást.

A terület kiszámításánál nem számítana, ha összekevernénk a szélességet és a
magasságot, de ha a téglalapot a képernyőre szeretnénk rajzolni, már igen!
Észben kellene tartanunk, hogy a `width` a `0` indexű, a `height` pedig az `1`
indexű elem a tuple-ben. Ezt valaki másnak még nehezebb lenne kitalálnia és
fejben tartania, ha a kódunkat használná. Mivel a kódunkban nem fejeztük ki az
adataink jelentését, most könnyebb hibát vétenünk.

<!-- Old headings. Do not remove or links may break. -->

<a id="refactoring-with-structs-adding-more-meaning"></a>

### Refaktorálás struktúrákkal {#refactoring-with-structs}

A struktúrákkal az adatok felcímkézése révén adunk jelentést a kódnak. Az
általunk használt tuple-t átalakíthatjuk egy struktúrává, amelynek az egésze és
a részei is nevet kapnak, ahogy az 5-10. kódrészlet mutatja.

<Listing number="5-10" file-name="src/main.rs" caption="Egy `Rectangle` struktúra definiálása">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-10/src/main.rs}}
```

</Listing>

Itt definiáltunk egy struktúrát, és a `Rectangle` nevet adtuk neki. A kapcsos
zárójeleken belül a `width` és a `height` mezőt definiáltuk, mindkettő `u32`
típusú. Ezután a `main`-ben létrehoztuk a `Rectangle` egy konkrét példányát,
amelynek szélessége `30`, magassága pedig `50`.

Az `area` függvényünket most egyetlen paraméterrel definiáltuk, amelynek a
`rectangle` nevet adtuk, és amelynek típusa egy `Rectangle` struktúrapéldány nem
módosítható kölcsönzése (borrow). Ahogy a 4. fejezetben említettük, a struktúrát
kölcsön szeretnénk venni ahelyett, hogy átvennénk a tulajdonjogát (ownership).
Így a `main` megtartja a tulajdonjogát, és továbbra is használhatja a
`rect1`-et; ezért használjuk a `&` jelet a függvény szignatúrájában és ott, ahol
a függvényt meghívjuk.

Az `area` függvény a `Rectangle` példány `width` és `height` mezőit éri el
(figyeld meg, hogy egy kölcsönzött struktúrapéldány mezőinek elérése nem
helyezi át a mezők értékeit, ezért látsz gyakran struktúrakölcsönzéseket). Az
`area` szignatúrája most pontosan azt mondja, amit gondolunk: számítsd ki a
`Rectangle` területét a `width` és a `height` mezője alapján. Ebből kiderül,
hogy a szélesség és a magasság összetartozik, és az értékek beszédes nevet
kapnak a `0` és `1` tuple-indexek helyett. Ez nagy nyereség az érthetőség
szempontjából.

<!-- Old headings. Do not remove or links may break. -->

<a id="adding-useful-functionality-with-derived-traits"></a>

### Funkciók hozzáadása származtatott traitekkel {#adding-functionality-with-derived-traits}

Hasznos lenne, ha a programunk hibakeresése közben ki tudnánk íratni egy
`Rectangle` példányt, és látnánk az összes mezőjének értékét. Az 5-11.
kódrészlet a korábbi fejezetekben már használt [`println!`
makróval][println]<!-- ignore --> próbálkozik. Ez azonban nem fog működni.

<Listing number="5-11" file-name="src/main.rs" caption="Kísérlet egy `Rectangle` példány kiíratására">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-11/src/main.rs}}
```

</Listing>

Amikor lefordítjuk ezt a kódot, egy hibát kapunk, amelynek a lényege ez:

```text
{{#include ../listings/ch05-using-structs-to-structure-related-data/listing-05-11/output.txt:3}}
```

A `println!` makró sokféle formázásra képes, és alapértelmezés szerint a
kapcsos zárójelek azt mondják a `println!`-nak, hogy a `Display` néven ismert
formázást használja: ez a közvetlenül a végfelhasználónak szánt kimenet. Az
eddig látott primitív típusok alapértelmezés szerint megvalósítják a
`Display`-t, mert egy `1`-et vagy bármely más primitív típust csak egyféleképpen
akarnál megmutatni a felhasználónak. A struktúráknál azonban kevésbé
egyértelmű, hogyan formázza a `println!` a kimenetet, mert több megjelenítési
lehetőség van: legyenek vesszők, vagy ne? Ki kell-e írni a kapcsos zárójeleket?
Minden mezőt meg kell-e jeleníteni? E kétértelműség miatt a Rust nem próbálja
kitalálni, mit szeretnénk, és a struktúráknak nincs előre megadott
`Display`-megvalósítása, amelyet a `println!` és a `{}` helyőrző
használhatna.

Ha tovább olvassuk a hibaüzeneteket, ezt a hasznos megjegyzést találjuk:

```text
{{#include ../listings/ch05-using-structs-to-structure-related-data/listing-05-11/output.txt:9:10}}
```

Próbáljuk ki! A `println!` makróhívás most így néz ki: `println!("rect1 is
{rect1:?}");`. Ha a kapcsos zárójelek közé a `:?` jelölőt tesszük, azzal azt
mondjuk a `println!`-nak, hogy a `Debug` nevű kimeneti formátumot szeretnénk
használni. A `Debug` trait lehetővé teszi, hogy a struktúránkat a fejlesztők
számára hasznos módon írassuk ki, így hibakeresés közben láthatjuk az értékét.

Fordítsd le a kódot ezzel a módosítással. A csudába! Még mindig hibát kapunk:

```text
{{#include ../listings/ch05-using-structs-to-structure-related-data/output-only-01-debug/output.txt:3}}
```

De a fordító ismét ad egy hasznos megjegyzést:

```text
{{#include ../listings/ch05-using-structs-to-structure-related-data/output-only-01-debug/output.txt:9:10}}
```

A Rust _valóban_ tartalmaz hibakeresési információk kiíratására szolgáló
funkciót, de ezt kifejezetten be kell kapcsolnunk ahhoz, hogy a struktúránk
számára elérhető legyen. Ehhez közvetlenül a struktúradefiníció elé a
`#[derive(Debug)]` külső attribútumot írjuk, ahogy az 5-12. kódrészlet
mutatja.

<Listing number="5-12" file-name="src/main.rs" caption="Az attribútum hozzáadása a `Debug` trait származtatásához, és a `Rectangle` példány kiíratása debug formázással">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-12/src/main.rs}}
```

</Listing>

Ha most futtatjuk a programot, nem kapunk hibát, és a következő kimenetet
látjuk:

```console
{{#include ../listings/ch05-using-structs-to-structure-related-data/listing-05-12/output.txt}}
```

Remek! Nem ez a legszebb kimenet, de megmutatja a példány összes mezőjének
értékét, ami hibakeresés közben biztosan segítene. Nagyobb struktúráknál
hasznos, ha a kimenet egy kicsit könnyebben olvasható; ilyenkor a `println!`
sztringjében a `{:?}` helyett a `{:#?}` formát használhatjuk. Ebben a példában
a `{:#?}` stílus a következő kimenetet adja:

```console
{{#include ../listings/ch05-using-structs-to-structure-related-data/output-only-02-pretty-debug/output.txt}}
```

Egy értéket a `Debug` formátummal úgy is kiírathatunk, hogy a [`dbg!`
makrót][dbg]<!-- ignore --> használjuk. Ez átveszi egy kifejezés tulajdonjogát
(szemben a `println!`-nal, amely referenciát kap), kiírja, hogy a kódban melyik
fájl melyik sorában történik a `dbg!` makró hívása, valamint a kifejezés
eredményül kapott értékét, majd visszaadja az érték tulajdonjogát.

> Megjegyzés: A `dbg!` makró hívása a standard hibakimenetre (`stderr`) ír,
> szemben a `println!`-nal, amely a standard kimenetre (`stdout`) ír. A
> `stderr`-ről és az `stdout`-ról bővebben a [12. fejezet „Hibák átirányítása
> a standard hibakimenetre” című szakaszában][err]<!-- ignore --> lesz szó.

Íme egy példa, amelyben a `width` mezőhöz rendelt érték, valamint a `rect1`
változóban lévő teljes struktúra értéke érdekel minket:

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-05-dbg-macro/src/main.rs}}
```

A `30 * scale` kifejezést körbevehetjük a `dbg!` hívással, és mivel a `dbg!`
visszaadja a kifejezés értékének tulajdonjogát, a `width` mező ugyanazt az
értéket kapja, mintha ott sem lenne a `dbg!` hívás. Nem szeretnénk, hogy a
`dbg!` átvegye a `rect1` tulajdonjogát, ezért a következő hívásban egy
`rect1`-re mutató referenciát használunk. A példa kimenete így néz ki:

```console
{{#include ../listings/ch05-using-structs-to-structure-related-data/no-listing-05-dbg-macro/output.txt}}
```

Láthatjuk, hogy a kimenet első része az _src/main.rs_ 10. sorából származik,
ahol a `30 * scale` kifejezést vizsgáljuk, és ennek eredménye `60` (az egész
számokra megvalósított `Debug` formázás csak az értéküket írja ki). Az
_src/main.rs_ 14. sorában lévő `dbg!` hívás a `&rect1` értékét írja ki, ami a
`Rectangle` struktúra. Ez a kimenet a `Rectangle` típus szépen formázott
`Debug` kimenetét használja. A `dbg!` makró nagyon hasznos lehet, amikor ki
szeretnéd deríteni, mit csinál a kódod!

A `Debug` trait mellett a Rust számos más traitet is biztosít, amelyeket a
`derive` attribútummal használhatunk, és amelyek hasznos viselkedéssel
bővíthetik az egyedi típusainkat. Ezeket a traiteket és viselkedésüket [a C.
függelék][app-c]<!-- ignore --> sorolja fel. A 10. fejezetben bemutatjuk,
hogyan valósíthatod meg ezeket a traiteket egyedi viselkedéssel, és hogyan
hozhatsz létre saját traiteket. A `derive`-on kívül sok más attribútum is
létezik; ezekről bővebben a [Rust Reference „Attributes” című
szakaszában][attributes] olvashatsz.

Az `area` függvényünk nagyon specifikus: csak téglalapok területét számítja ki.
Hasznos lenne ezt a viselkedést szorosabban a `Rectangle` struktúránkhoz kötni,
mert más típussal úgysem működik. Nézzük meg, hogyan refaktorálhatjuk tovább
ezt a kódot úgy, hogy az `area` függvényt a `Rectangle` típusunkon definiált
`area` metódussá alakítjuk.

[the-tuple-type]: ch03-02-data-types.html#the-tuple-type
[app-c]: appendix-03-derivable-traits.md
[println]: ../std/macro.println.html
[dbg]: ../std/macro.dbg.html
[err]: ch12-06-writing-to-stderr-instead-of-stdout.html
[attributes]: ../reference/attributes.html
