## C. függelék: Származtatható traitek {#appendix-c-derivable-traits}

A könyv több pontján is szó volt már a `derive` attribútumról, amelyet
struktúra- vagy enumdefiníciókra alkalmazhatsz. A `derive` attribútum olyan
kódot generál, amely a `derive` szintaxissal annotált típuson megvalósít egy
traitet, annak saját alapértelmezett megvalósításával.

Ebben a függelékben a standard könyvtár összes olyan traitjét bemutatjuk,
amely a `derive` segítségével használható. Minden szakasz a következőket
tárgyalja:

- Milyen operátorokat és metódusokat tesz elérhetővé a trait származtatása
- Mit csinál a trait `derive` által biztosított megvalósítása
- Mit jelent a típusra nézve, ha megvalósítja a traitet
- Milyen feltételek mellett szabad vagy nem szabad megvalósítani a traitet
- Példák olyan műveletekre, amelyekhez szükség van a traitre

Ha a `derive` attribútum által biztosítottól eltérő viselkedést szeretnél,
a traitek kézi megvalósításának részleteiről az egyes traitek [standard
könyvtárbeli dokumentációjában](../std/index.html)<!-- ignore --> olvashatsz.

Az itt felsorolt traitek az egyetlenek a standard könyvtárban definiáltak
közül, amelyek a `derive` segítségével megvalósíthatók a saját típusaidon. A
standard könyvtár többi traitjének nincs értelmes alapértelmezett viselkedése,
így rajtad múlik, hogy azokat a céljaidnak megfelelő módon valósítsd meg.

Nem származtatható trait például a `Display`, amely a végfelhasználóknak szánt
formázásért felel. Mindig mérlegelned kell, hogyan érdemes egy típust a
végfelhasználónak megjeleníteni. A típus mely részeit láthatja a
végfelhasználó? Mely részeket találná fontosnak? Milyen formátumban lenne
számára a leghasznosabb az adat? A Rust fordító ezt nem láthatja előre, ezért
nem tud megfelelő alapértelmezett viselkedést biztosítani helyetted.

Az ebben a függelékben felsorolt származtatható traitek listája nem teljes: a
könyvtárak a saját traitjeikhez is megvalósíthatják a `derive`-ot, így azoknak
a traiteknek a listája, amelyekkel a `derive` használható, valójában nyitott.
A `derive` megvalósításához procedurális makrót kell használni, erről a 20.
fejezet [„Egyéni `derive` makrók”][custom-derive-macros]<!-- ignore -->
szakaszában lesz szó.

### `Debug` a programozóknak szóló kimenethez {#debug-for-programmer-output}

A `Debug` trait lehetővé teszi a hibakeresési (debug) formázást a
formázósztringekben, amelyet a `{}` helyőrzőkbe írt `:?` jelöl.

A `Debug` trait segítségével hibakeresési céllal kiírhatod egy típus
példányait, így te és a típusodat használó többi programozó megvizsgálhatjátok
a példányt a program futásának egy adott pontján.

A `Debug` traitre például az `assert_eq!` makró használatához van szükség. Ez
a makró kiírja az argumentumként kapott példányok értékét, ha az egyenlőségre
vonatkozó állítás nem teljesül, így a programozók láthatják, miért nem volt
egyenlő a két példány.

### `PartialEq` és `Eq` az egyenlőség vizsgálatához {#partialeq-and-eq-for-equality-comparisons}

A `PartialEq` trait lehetővé teszi egy típus példányainak összehasonlítását
egyenlőség szempontjából, és elérhetővé teszi a `==` és `!=` operátorokat.

A `PartialEq` származtatása megvalósítja az `eq` metódust. Ha struktúrákon
származtatjuk a `PartialEq`-t, két példány csak akkor egyenlő, ha _minden_
mezőjük egyenlő, és nem egyenlők, ha _bármelyik_ mezőjük eltér. Enumokon
származtatva minden változat egyenlő önmagával, és nem egyenlő a többi
változattal.

A `PartialEq` traitre például az `assert_eq!` makró használatához van szükség,
amelynek képesnek kell lennie egy típus két példányát egyenlőség szempontjából
összehasonlítani.

Az `Eq` traitnek nincsenek metódusai. Azt jelzi, hogy az annotált típus minden
értéke egyenlő önmagával. Az `Eq` trait csak olyan típusokra alkalmazható,
amelyek a `PartialEq`-t is megvalósítják, ugyanakkor nem minden `PartialEq`-t
megvalósító típus valósíthatja meg az `Eq`-t. Erre példák a lebegőpontos
számtípusok: a lebegőpontos számok megvalósítása szerint a nem-szám (`NaN`)
érték két példánya nem egyenlő egymással.

Az `Eq`-ra például a `HashMap<K, V>` kulcsainál van szükség, hogy a
`HashMap<K, V>` el tudja dönteni, hogy két kulcs azonos-e.

### `PartialOrd` és `Ord` a sorrend szerinti összehasonlításhoz {#partialord-and-ord-for-ordering-comparisons}

A `PartialOrd` trait lehetővé teszi egy típus példányainak összehasonlítását
rendezési célból. A `PartialOrd`-ot megvalósító típus használható a `<`, `>`,
`<=` és `>=` operátorokkal. A `PartialOrd` trait csak olyan típusokra
alkalmazható, amelyek a `PartialEq`-t is megvalósítják.

A `PartialOrd` származtatása megvalósítja a `partial_cmp` metódust, amely
`Option<Ordering>` értéket ad vissza; ez `None` lesz, ha a megadott értékek
között nem állapítható meg sorrend. Olyan érték például, amely nem állít elő
sorrendet – noha az adott típus legtöbb értéke összehasonlítható –, a `NaN`
lebegőpontos érték. Ha a `partial_cmp`-t bármely lebegőpontos számmal és a
`NaN` lebegőpontos értékkel hívjuk meg, `None` értéket ad vissza.

Struktúrákon származtatva a `PartialOrd` úgy hasonlít össze két példányt, hogy
mezőnként összeveti az értékeket, abban a sorrendben, ahogy a mezők a
struktúra definíciójában szerepelnek. Enumokon származtatva az enum
definíciójában korábban deklarált változatok kisebbnek számítanak a később
felsoroltaknál.

A `PartialOrd` traitre például a `rand` crate `gen_range` metódusához van
szükség, amely egy tartománykifejezéssel megadott tartományban generál
véletlen értéket.

Az `Ord` trait azt biztosítja, hogy az annotált típus bármely két értéke
között létezik érvényes sorrend. Az `Ord` trait a `cmp` metódust valósítja meg,
amely `Option<Ordering>` helyett `Ordering` értéket ad vissza, mert érvényes
sorrend mindig megállapítható. Az `Ord` trait csak olyan típusokra
alkalmazható, amelyek a `PartialOrd`-ot és az `Eq`-t is megvalósítják (az
`Eq`-hoz pedig a `PartialEq` szükséges). Struktúrákon és enumokon származtatva
a `cmp` ugyanúgy viselkedik, mint a `PartialOrd` származtatott `partial_cmp`
megvalósítása.

Az `Ord`-ra például akkor van szükség, amikor értékeket tárolunk egy
`BTreeSet<T>`-ben, amely az értékek rendezési sorrendje alapján tárolja az
adatokat.

### `Clone` és `Copy` az értékek másolásához {#clone-and-copy-for-duplicating-values}

A `Clone` trait lehetővé teszi, hogy explicit módon mély másolatot készíts egy
értékről; a másolás során tetszőleges kód futhat, és kupacon tárolt adatok is
másolódhatnak. A `Clone`-ról bővebben a 4. fejezet [„Változók és adatok
kölcsönhatása
klónozással”][variables-and-data-interacting-with-clone]<!-- ignore -->
szakaszában olvashatsz.

A `Clone` származtatása megvalósítja a `clone` metódust, amely – a teljes
típusra megvalósítva – a típus minden részén meghívja a `clone`-t. Ez azt
jelenti, hogy a `Clone` származtatásához a típus összes mezőjének vagy
értékének is meg kell valósítania a `Clone`-t.

A `Clone`-ra például akkor van szükség, amikor egy szeleten a `to_vec`
metódust hívjuk meg. A szelet nem birtokolja a benne lévő típuspéldányokat,
a `to_vec` által visszaadott vektornak viszont birtokolnia kell a saját
példányait, ezért a `to_vec` minden elemen meghívja a `clone`-t. Így a
szeletben tárolt típusnak meg kell valósítania a `Clone`-t.

A `Copy` trait lehetővé teszi egy érték másolását pusztán a veremben tárolt
bitek átmásolásával; ehhez nincs szükség tetszőleges kódra. A `Copy`-ról
bővebben a 4. fejezet [„Csak veremben tárolt adatok:
Copy”][stack-only-data-copy]<!-- ignore --> szakaszában olvashatsz.

A `Copy` trait nem definiál metódusokat, így a programozók nem tudják ezeket
túlterhelni, és nem sérülhet az a feltételezés, hogy nem fut tetszőleges kód.
Így minden programozó számíthat arra, hogy egy érték másolása nagyon gyors.

A `Copy`-t bármely olyan típuson származtathatod, amelynek minden része
megvalósítja a `Copy`-t. A `Copy`-t megvalósító típusnak a `Clone`-t is meg
kell valósítania, mert a `Copy`-t megvalósító típusnak a `Clone` triviális
megvalósítása ugyanazt a feladatot végzi, mint a `Copy`.

A `Copy` traitre ritkán van szükség; a `Copy`-t megvalósító típusoknál
optimalizációk érhetők el, vagyis nem kell meghívnod a `clone`-t, ami
tömörebbé teszi a kódot.

Mindent, ami a `Copy`-val lehetséges, a `Clone`-nal is elérhetsz, csak a kód
lassabb lehet, vagy egyes helyeken a `clone`-t kell használnia.

### `Hash` egy érték rögzített méretű értékre való leképezéséhez {#hash-for-mapping-a-value-to-a-value-of-fixed-size}

A `Hash` trait lehetővé teszi, hogy egy tetszőleges méretű típus egy példányát
egy hasítófüggvény segítségével rögzített méretű értékre képezd le. A `Hash`
származtatása megvalósítja a `hash` metódust. A `hash` metódus származtatott
megvalósítása a típus minden részén meghívott `hash` eredményét kombinálja,
vagyis a `Hash` származtatásához minden mezőnek vagy értéknek is meg kell
valósítania a `Hash`-t.

A `Hash`-re például a kulcsok `HashMap<K, V>`-ben való tárolásához van szükség,
hogy az adatok tárolása hatékony legyen.

### `Default` az alapértelmezett értékekhez {#default-for-default-values}

A `Default` trait lehetővé teszi, hogy egy típushoz alapértelmezett értéket
hozz létre. A `Default` származtatása megvalósítja a `default` függvényt. A
`default` függvény származtatott megvalósítása a típus minden részén meghívja
a `default` függvényt, vagyis a `Default` származtatásához a típus összes
mezőjének vagy értékének is meg kell valósítania a `Default`-ot.

A `Default::default` függvényt gyakran használjuk az 5. fejezet
[„Példányok létrehozása a struktúrafrissítő szintaxissal”][creating-instances-from-other-instances-with-struct-update-syntax]<!-- ignore -->
szakaszában tárgyalt struktúrafrissítő szintaxissal együtt. Egy struktúra
néhány mezőjét testre szabhatod, a többi mezőhöz pedig alapértelmezett
értéket állíthatsz be és használhatsz a `..Default::default()` segítségével.

A `Default` traitre például akkor van szükség, amikor az `Option<T>`
példányokon az `unwrap_or_default` metódust használod. Ha az `Option<T>`
értéke `None`, az `unwrap_or_default` metódus az `Option<T>`-ben tárolt `T`
típus `Default::default` eredményét adja vissza.

[creating-instances-from-other-instances-with-struct-update-syntax]: ch05-01-defining-structs.html#creating-instances-from-other-instances-with-struct-update-syntax
[stack-only-data-copy]: ch04-01-what-is-ownership.html#stack-only-data-copy
[variables-and-data-interacting-with-clone]: ch04-01-what-is-ownership.html#variables-and-data-interacting-with-clone
[custom-derive-macros]: ch20-05-macros.html#custom-derive-macros
