## A minták szintaxisa {#pattern-syntax}

Ebben a szakaszban összegyűjtjük a mintákban érvényes összes szintaxist, és
megvitatjuk, miért és mikor érdemes az egyes formákat használni.

### Illesztés literálokra {#matching-literals}

Ahogy a 6. fejezetben láttad, a mintákat közvetlenül literálokra is
illesztheted. Az alábbi kód néhány példát mutat erre:

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-01-literals/src/main.rs:here}}
```

Ez a kód a `one` szöveget írja ki, mert az `x` értéke `1`. Ez a szintaxis
akkor hasznos, ha azt szeretnéd, hogy a kódod egy adott konkrét érték esetén
hajtson végre valamilyen műveletet.

### Illesztés nevesített változókra {#matching-named-variables}

A nevesített változók (named variables) cáfolhatatlan minták, amelyek bármilyen
értékre illeszkednek, és ebben a könyvben már sokszor használtuk őket. Van
azonban egy bonyodalom, ha nevesített változókat használsz `match`, `if let`
vagy `while let` kifejezésekben. Mivel ezek a kifejezések mind új hatókört
nyitnak, a bennük lévő minta részeként deklarált változók árnyékolják a
szerkezeten kívüli, azonos nevű változókat, ahogy az minden változóra igaz. A
19-11. kódrészletben deklarálunk egy `x` nevű változót `Some(5)` értékkel és egy
`y` változót `10` értékkel. Ezután egy `match` kifejezést írunk az `x` értékre.
Nézd meg a match ágak mintáit és a végén lévő `println!`-t, és próbáld meg
kitalálni, mit fog kiírni a kód, mielőtt lefuttatnád vagy továbbolvasnál.

<Listing number="19-11" file-name="src/main.rs" caption="Egy `match` kifejezés olyan ággal, amely egy új változót vezet be, és az árnyékolja a meglévő `y` változót">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-11/src/main.rs:here}}
```

</Listing>

Nézzük végig, mi történik, amikor a `match` kifejezés lefut. Az első match ág
mintája nem illeszkedik az `x` megadott értékére, így a kód továbblép.

A második match ág mintája egy új, `y` nevű változót vezet be, amely egy `Some`
értéken belüli bármilyen értékre illeszkedik. Mivel a `match` kifejezésen belül
új hatókörben vagyunk, ez egy új `y` változó, nem pedig az, amelyet az elején
`10` értékkel deklaráltunk. Ez az új `y` kötés (binding) bármilyen, `Some`-on
belüli értékre illeszkedik, és az `x`-ben éppen ilyen van. Ezért ez az új `y`
az `x`-ben lévő `Some` belső értékéhez kötődik. Ez az érték az `5`, így az ág
kifejezése lefut, és kiírja: `Matched, y = 5`.

Ha az `x` a `Some(5)` helyett `None` érték lett volna, az első két ág mintája
nem illeszkedett volna, így az érték az aláhúzásjelre illeszkedett volna. Az
aláhúzásjeles ág mintájában nem vezettük be az `x` változót, így a
kifejezésben szereplő `x` még mindig a külső, nem árnyékolt `x`. Ebben a
feltételezett esetben a `match` a `Default case, x = None` szöveget írná ki.

Amikor a `match` kifejezés véget ér, a hatóköre is véget ér, és vele együtt a
belső `y` hatóköre is. Az utolsó `println!` kimenete: `at the end: x =
Some(5), y = 10`.

Ha olyan `match` kifejezést szeretnénk írni, amely a külső `x` és `y` értékeit
hasonlítja össze ahelyett, hogy egy új, a meglévő `y` változót árnyékoló
változót vezetne be, akkor őrfeltételt (match guard) kellene használnunk. Az
őrfeltételekről később, a [„Feltételek hozzáadása
őrfeltételekkel”](#adding-conditionals-with-match-guards)<!-- ignore -->
részben lesz szó.

<!-- Old headings. Do not remove or links may break. -->
<a id="multiple-patterns"></a>

### Illesztés több mintára {#matching-multiple-patterns}

A `match` kifejezésekben a `|` szintaxissal több mintára is illeszthetsz; ez a
minták _vagy_ operátora. Az alábbi kódban például az `x` értékét a match
ágakra illesztjük, amelyek közül az elsőben van egy _vagy_ lehetőség, vagyis
ha az `x` értéke az ágban szereplő értékek bármelyikére illeszkedik, az ág
kódja lefut:


```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-02-multiple-patterns/src/main.rs:here}}
```

Ez a kód a `one or two` szöveget írja ki.

### Értéktartományok illesztése a `..=` segítségével {#matching-ranges-of-values-with-}

A `..=` szintaxissal értékek zárt tartományára illeszthetünk. Az alábbi kódban,
ha egy minta a megadott tartomány bármelyik értékére illeszkedik, az adott ág
lefut:

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-03-ranges/src/main.rs:here}}
```

Ha az `x` értéke `1`, `2`, `3`, `4` vagy `5`, az első ág illeszkedik. Több
illesztendő érték esetén ez a szintaxis kényelmesebb, mint ha ugyanezt a `|`
operátorral fejeznénk ki; a `|` használatával azt kellene írnunk, hogy
`1 | 2 | 3 | 4 | 5`. Egy tartomány megadása sokkal rövidebb, különösen ha
mondjuk 1 és 1000 közötti bármely számra szeretnénk illeszteni!

A fordító fordítási időben ellenőrzi, hogy a tartomány nem üres-e, és mivel a
Rust csak a `char` és a numerikus típusok esetében tudja eldönteni, hogy egy
tartomány üres-e, tartományokat csak numerikus vagy `char` értékekkel
használhatunk.

Íme egy példa `char` értékek tartományaira:

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-04-ranges-of-char/src/main.rs:here}}
```

A Rust meg tudja állapítani, hogy a `'c'` az első minta tartományába esik, és
kiírja: `early ASCII letter`.

### Értékek részekre bontása szétbontással {#destructuring-to-break-apart-values}

A mintákkal struktúrákat, enumokat és tuple-öket is szétbonthatunk
(destructuring), hogy ezen értékek különböző részeit használhassuk. Nézzük
végig mindegyiket.

<!-- Old headings. Do not remove or links may break. -->

<a id="destructuring-structs"></a>

#### Struktúrák {#structs}

A 19-12. kódrészlet egy `Point` struktúrát mutat két mezővel, `x`-szel és
`y`-nal, amelyet egy `let` utasításban szereplő mintával részeire bonthatunk.

<Listing number="19-12" file-name="src/main.rs" caption="Egy struktúra mezőinek szétbontása külön változókba">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-12/src/main.rs}}
```

</Listing>

Ez a kód létrehozza az `a` és `b` változókat, amelyek a `p` struktúra `x` és
`y` mezőinek értékeire illeszkednek. A példa azt mutatja, hogy a mintában
szereplő változók nevének nem kell megegyeznie a struktúra mezőneveivel. Mégis
gyakori, hogy a változóneveket a mezőnevekhez igazítjuk, így könnyebb
megjegyezni, melyik változó melyik mezőből származik. Emiatt a gyakori
használat miatt, és mert a `let Point { x: x, y: y } = p;` sok ismétlést
tartalmaz, a Rustban van egy rövidítés a struktúramezőkre illeszkedő
mintákhoz: elég felsorolni a struktúra mezőjének nevét, és a mintából
létrehozott változók ugyanazt a nevet kapják. A 19-13. kódrészlet ugyanúgy
viselkedik, mint a 19-12. kódrészlet kódja, de a `let` mintájában létrehozott
változók az `a` és `b` helyett `x` és `y`.

<Listing number="19-13" file-name="src/main.rs" caption="Struktúramezők szétbontása a rövidített mezőírásmóddal">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-13/src/main.rs}}
```

</Listing>

Ez a kód létrehozza az `x` és `y` változókat, amelyek a `p` változó `x` és `y`
mezőire illeszkednek. Az eredmény az, hogy az `x` és `y` változók a `p`
struktúra értékeit tartalmazzák.

Úgy is szétbonthatunk, hogy a struktúramintában literálértékeket adunk meg,
ahelyett hogy minden mezőhöz változót hoznánk létre. Így egyes mezőket
megvizsgálhatunk, hogy egy adott értéket tartalmaznak-e, miközben a többi mező
szétbontásához változókat hozunk létre.

A 19-14. kódrészletben egy `match` kifejezés három esetre osztja a `Point`
értékeket: azokra a pontokra, amelyek közvetlenül az `x` tengelyen fekszenek
(ez akkor igaz, ha `y = 0`), amelyek az `y` tengelyen fekszenek (`x = 0`),
illetve amelyek egyik tengelyen sem.

<Listing number="19-14" file-name="src/main.rs" caption="Szétbontás és literálértékekre illesztés egyetlen mintában">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-14/src/main.rs:here}}
```

</Listing>

Az első ág bármely, az `x` tengelyen fekvő pontra illeszkedik, mivel azt adja
meg, hogy az `y` mező akkor illeszkedik, ha az értéke a `0` literálra
illeszkedik. A minta ettől még létrehoz egy `x` változót, amelyet az ág
kódjában használhatunk.

Hasonlóképpen a második ág bármely, az `y` tengelyen fekvő pontra illeszkedik,
mivel azt adja meg, hogy az `x` mező akkor illeszkedik, ha az értéke `0`, és
létrehoz egy `y` változót az `y` mező értékéhez. A harmadik ág nem ad meg
literált, így bármely más `Point` értékre illeszkedik, és mind az `x`, mind az
`y` mezőhöz létrehoz egy változót.

Ebben a példában a `p` érték a második ágra illeszkedik, mivel az `x` `0`-t
tartalmaz, így a kód az `On the y axis at 7` szöveget írja ki.

Ne feledd, hogy a `match` kifejezés az első illeszkedő minta megtalálása után
abbahagyja az ágak vizsgálatát, így bár a `Point { x: 0, y: 0 }` az `x` és az
`y` tengelyen is rajta van, ez a kód csak az `On the x axis at 0` szöveget
írná ki.

<!-- Old headings. Do not remove or links may break. -->

<a id="destructuring-enums"></a>

#### Enumok {#enums}

Ebben a könyvben már bontottunk szét enumokat (például a 6. fejezet 6-5.
kódrészletében), de még nem beszéltünk kifejezetten arról, hogy az enum
szétbontására szolgáló minta annak felel meg, ahogyan az enumban tárolt adatok
definiálva vannak. Példaként a 19-15. kódrészletben a 6-2. kódrészlet `Message`
enumját használjuk, és egy olyan `match`-et írunk, amelynek mintái minden belső
értéket szétbontanak.

<Listing number="19-15" file-name="src/main.rs" caption="Különböző fajta értékeket tároló enumváltozatok szétbontása">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-15/src/main.rs}}
```

</Listing>

Ez a kód a `Change color to red 0, green 160, and blue 255` szöveget írja ki.
Próbáld meg megváltoztatni a `msg` értékét, hogy lásd a többi ág kódját is
lefutni.

Az adat nélküli enumváltozatokat, például a `Message::Quit`-et, nem tudjuk
tovább szétbontani. Csak a `Message::Quit` literálértékre illeszthetünk, és
ebben a mintában nincsenek változók.

A struktúraszerű enumváltozatoknál, például a `Message::Move` esetében, a
struktúrák illesztésére használt mintához hasonló mintát használhatunk. A
változat neve után kapcsos zárójeleket írunk, majd felsoroljuk a mezőket
változókkal, így részeire bontjuk az értéket, és a részeket felhasználhatjuk az
ág kódjában. Itt a rövidített formát használjuk, ahogy a 19-13. kódrészletben.

A tuple-szerű enumváltozatoknál, például az egyelemű tuple-t tároló
`Message::Write` és a háromelemű tuple-t tároló `Message::ChangeColor`
esetében, a minta a tuple-ök illesztésére használt mintához hasonló. A mintában
szereplő változók számának meg kell egyeznie az illesztett változat elemeinek
számával.

<!-- Old headings. Do not remove or links may break. -->

<a id="destructuring-nested-structs-and-enums"></a>

#### Beágyazott struktúrák és enumok {#nested-structs-and-enums}

Eddig minden példánk csak egy szint mélységben illesztett struktúrákra vagy
enumokra, de az illesztés beágyazott (nested) elemekre is működik! Például
átalakíthatjuk a 19-15. kódrészlet kódját úgy, hogy a `ChangeColor` üzenet RGB
és HSV színeket is támogasson, ahogy a 19-16. kódrészlet mutatja.

<Listing number="19-16" caption="Illesztés beágyazott enumokra">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-16/src/main.rs}}
```

</Listing>

A `match` kifejezés első ágának mintája egy olyan `Message::ChangeColor`
enumváltozatra illeszkedik, amely egy `Color::Rgb` változatot tartalmaz; a
minta ezután a három belső `i32` értékhez köt. A második ág mintája szintén egy
`Message::ChangeColor` enumváltozatra illeszkedik, de a belső enum ezúttal a
`Color::Hsv` változatra illeszkedik. Ezeket az összetett feltételeket egyetlen
`match` kifejezésben adhatjuk meg, pedig két enum is érintett.

<!-- Old headings. Do not remove or links may break. -->

<a id="destructuring-structs-and-tuples"></a>

#### Struktúrák és tuple-ök {#structs-and-tuples}

A szétbontó mintákat még összetettebb módokon is keverhetjük, párosíthatjuk és
egymásba ágyazhatjuk. Az alábbi példa egy bonyolult szétbontást mutat, ahol
struktúrákat és tuple-öket ágyazunk egy tuple-be, és az összes primitív
értéket kibontjuk belőle:

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-05-destructuring-structs-and-tuples/src/main.rs:here}}
```

Ezzel a kóddal az összetett típusokat alkotórészeikre bonthatjuk, így a minket
érdeklő értékeket külön-külön használhatjuk.

A mintákkal végzett szétbontás kényelmes módja annak, hogy az értékek egyes
darabjait – például egy struktúra egyes mezőinek értékét – egymástól
függetlenül használjuk.

### Értékek figyelmen kívül hagyása egy mintában {#ignoring-values-in-a-pattern}

Láttad már, hogy néha hasznos figyelmen kívül hagyni értékeket egy mintában,
például egy `match` utolsó ágában, hogy olyan mindent elfogó ágat kapjunk,
amely valójában nem csinál semmit, de az összes fennmaradó lehetséges értéket
lefedi. Egy mintában többféleképpen hagyhatunk figyelmen kívül teljes
értékeket vagy értékrészeket: a `_` mintával (ezt már láttad), a `_` minta egy
másik mintán belüli használatával, aláhúzásjellel kezdődő névvel, vagy a `..`
használatával, amely az érték fennmaradó részeit hagyja figyelmen kívül. Nézzük
meg, hogyan és miért érdemes ezeket a mintákat használni.

<!-- Old headings. Do not remove or links may break. -->

<a id="ignoring-an-entire-value-with-_"></a>

#### Egy teljes érték a `_` segítségével {#an-entire-value-with-_}

Az aláhúzásjelet helyettesítő jelként (wildcard) használtuk, olyan mintaként,
amely bármilyen értékre illeszkedik, de nem köt az értékhez. Ez különösen a
`match` kifejezés utolsó ágában hasznos, de bármilyen mintában használhatjuk,
a függvényparamétereket is beleértve, ahogy a 19-17. kódrészlet mutatja.

<Listing number="19-17" file-name="src/main.rs" caption="A `_` használata egy függvényszignatúrában">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-17/src/main.rs}}
```

</Listing>

Ez a kód teljesen figyelmen kívül hagyja az első argumentumként átadott `3`
értéket, és a `This code only uses the y parameter: 4` szöveget írja ki.

Ha egy adott függvényparaméterre már nincs szükséged, a legtöbb esetben úgy
módosítanád a szignatúrát, hogy ne tartalmazza a fel nem használt paramétert.
Egy függvényparaméter figyelmen kívül hagyása például akkor lehet különösen
hasznos, ha egy traitet valósítasz meg, amelyhez egy bizonyos
típusszignatúrára van szükséged, de a megvalósításod függvénytörzsének nincs
szüksége az egyik paraméterre. Így elkerülöd a fel nem használt
függvényparaméterekre vonatkozó fordítói figyelmeztetést, amelyet név
használatakor kapnál.

<!-- Old headings. Do not remove or links may break. -->

<a id="ignoring-parts-of-a-value-with-a-nested-_"></a>

#### Egy érték részei beágyazott `_` segítségével {#parts-of-a-value-with-a-nested-_}

A `_` jelet egy másik mintán belül is használhatjuk, hogy egy értéknek csak egy
részét hagyjuk figyelmen kívül, például ha egy értéknek csak egy részét akarjuk
megvizsgálni, a többi részére pedig nincs szükségünk a futtatandó kódban. A
19-18. kódrészlet egy beállítás értékének kezeléséért felelős kódot mutat. Az
üzleti követelmények szerint a felhasználó nem írhatja felül egy beállítás már
meglévő egyéni értékét, de törölheti a beállítást, és értéket adhat neki, ha az
éppen nincs beállítva.

<Listing number="19-18" caption="Aláhúzásjel használata `Some` változatokra illeszkedő mintákban, amikor nincs szükségünk a `Some`-on belüli értékre">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-18/src/main.rs:here}}
```

</Listing>

Ez a kód a `Can't overwrite an existing customized value`, majd a `setting is
Some(5)` szöveget írja ki. Az első match ágban nem kell illesztenünk vagy
használnunk egyik `Some` változaton belüli értéket sem, de meg kell vizsgálnunk
azt az esetet, amikor a `setting_value` és a `new_setting_value` is `Some`
változat. Ebben az esetben kiírjuk, miért nem változtatjuk meg a
`setting_value` értékét, és az nem is változik.

Minden más esetben (ha akár a `setting_value`, akár a `new_setting_value`
értéke `None`), amelyet a második ágban a `_` minta fejez ki, megengedjük,
hogy a `new_setting_value` legyen a `setting_value` új értéke.

Egy mintán belül több helyen is használhatunk aláhúzásjelet, hogy bizonyos
értékeket figyelmen kívül hagyjunk. A 19-19. kódrészlet egy ötelemű tuple
második és negyedik értékének figyelmen kívül hagyására mutat példát.

<Listing number="19-19" caption="Egy tuple több részének figyelmen kívül hagyása">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-19/src/main.rs:here}}
```

</Listing>

Ez a kód a `Some numbers: 2, 8, 32` szöveget írja ki, a `4` és `16` értékeket
pedig figyelmen kívül hagyja.

<!-- Old headings. Do not remove or links may break. -->

<a id="ignoring-an-unused-variable-by-starting-its-name-with-_"></a>

#### Fel nem használt változó `_`-sal kezdődő névvel {#an-unused-variable-by-starting-its-name-with-_}

Ha létrehozol egy változót, de sehol sem használod, a Rust általában
figyelmeztetést ad, mert a fel nem használt változó hibára utalhat. Néha
azonban hasznos lehet olyan változót létrehozni, amelyet még nem használsz,
például prototípus készítésekor vagy egy projekt elején. Ilyenkor úgy
kérheted meg a Rustot, hogy ne figyelmeztessen a fel nem használt változóra,
hogy a változó nevét aláhúzásjellel kezded. A 19-20. kódrészletben két fel nem
használt változót hozunk létre, de a kód fordításakor csak az egyikre kapunk
figyelmeztetést.

<Listing number="19-20" file-name="src/main.rs" caption="Aláhúzásjellel kezdődő változónév a fel nem használt változókra vonatkozó figyelmeztetések elkerülésére">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-20/src/main.rs}}
```

</Listing>

Itt figyelmeztetést kapunk arra, hogy az `y` változót nem használjuk, a `_x`
változóra viszont nem.

Figyeld meg, hogy van egy finom különbség a puszta `_` és az aláhúzásjellel
kezdődő név használata között. A `_x` szintaxis továbbra is a változóhoz köti
az értéket, míg a `_` egyáltalán nem köt. Hogy megmutassuk, mikor számít ez a
különbség, a 19-21. kódrészlet hibát fog okozni.

<Listing number="19-21" caption="Az aláhúzásjellel kezdődő, fel nem használt változó továbbra is köti az értéket, ami az érték tulajdonjogának átvételével járhat.">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-21/src/main.rs:here}}
```

</Listing>

Hibát kapunk, mert az `s` értéke ettől még átmozgatódik az `_s`-be, ami
megakadályozza, hogy az `s`-t újra használjuk. Az önmagában álló aláhúzásjel
azonban soha nem köt az értékhez. A 19-22. kódrészlet hiba nélkül lefordul,
mert az `s` nem mozgatódik át a `_`-ba.

<Listing number="19-22" caption="Az aláhúzásjel használata nem köti az értéket.">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-22/src/main.rs:here}}
```

</Listing>

Ez a kód tökéletesen működik, mert az `s`-t soha nem kötjük semmihez, így nem
mozgatódik el.

<a id="ignoring-remaining-parts-of-a-value-with-"></a>

#### Egy érték fennmaradó részei a `..` segítségével {#remaining-parts-of-a-value-with-}

A sok részből álló értékeknél a `..` szintaxissal használhatunk bizonyos
részeket, a többit pedig figyelmen kívül hagyhatjuk, így nem kell minden
figyelmen kívül hagyott értékhez aláhúzásjelet írnunk. A `..` minta az érték
minden olyan részét figyelmen kívül hagyja, amelyet a minta többi részében nem
illesztettünk kifejezetten. A 19-23. kódrészletben egy `Point` struktúra egy
háromdimenziós térbeli koordinátát tárol. A `match` kifejezésben csak az `x`
koordinátával szeretnénk dolgozni, az `y` és `z` mezők értékeit pedig
figyelmen kívül hagyjuk.

<Listing number="19-23" caption="Egy `Point` összes mezőjének figyelmen kívül hagyása az `x` kivételével a `..` használatával">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-23/src/main.rs:here}}
```

</Listing>

Felsoroljuk az `x` értéket, majd egyszerűen hozzáírjuk a `..` mintát. Ez
gyorsabb, mint felsorolni az `y: _` és `z: _` részeket, különösen ha sok mezős
struktúrákkal dolgozunk olyan helyzetekben, ahol csak egy-két mező lényeges.

A `..` szintaxis annyi értékre terjed ki, amennyire szükséges. A 19-24.
kódrészlet azt mutatja, hogyan használhatjuk a `..`-ot egy tuple-lel.

<Listing number="19-24" file-name="src/main.rs" caption="Csak egy tuple első és utolsó értékének illesztése, az összes többi érték figyelmen kívül hagyásával">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-24/src/main.rs}}
```

</Listing>

Ebben a kódban az első és az utolsó értéket a `first` és a `last` illeszti. A
`..` mindenre illeszkedik, ami közöttük van, és figyelmen kívül hagyja azt.

A `..` használatának azonban egyértelműnek kell lennie. Ha nem világos, mely
értékeket akarjuk illeszteni és melyeket figyelmen kívül hagyni, a Rust hibát
ad. A 19-25. kódrészlet a `..` kétértelmű használatára mutat példát, ezért nem
fordul le.

<Listing number="19-25" file-name="src/main.rs" caption="Kísérlet a `..` kétértelmű használatára">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-25/src/main.rs}}
```

</Listing>

A példa fordításakor ezt a hibát kapjuk:

```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-25/output.txt}}
```

A Rust nem tudja megállapítani, hogy a tuple hány értékét kell figyelmen kívül
hagynia, mielőtt egy értéket a `second`-höz illesztene, és utána még hány
további értéket kell figyelmen kívül hagynia. Ez a kód jelentheti azt, hogy a
`2`-t figyelmen kívül akarjuk hagyni, a `second`-et a `4`-hez kötni, majd a
`8`-at, a `16`-ot és a `32`-t figyelmen kívül hagyni; vagy azt, hogy a `2`-t és
a `4`-et akarjuk figyelmen kívül hagyni, a `second`-et a `8`-hoz kötni, majd a
`16`-ot és a `32`-t figyelmen kívül hagyni; és így tovább. A `second`
változónév a Rust számára semmi különöset nem jelent, így fordítási hibát
kapunk, mert a `..` ilyen módon, két helyen való használata kétértelmű.

<!-- Old headings. Do not remove or links may break. -->

<a id="extra-conditionals-with-match-guards"></a>

### Feltételek hozzáadása őrfeltételekkel {#adding-conditionals-with-match-guards}

Az _őrfeltétel (match guard)_ egy további `if` feltétel, amelyet egy `match`
ág mintája után adunk meg, és amelynek szintén teljesülnie kell ahhoz, hogy az
adott ág kerüljön kiválasztásra. Az őrfeltételek olyan összetettebb gondolatok
kifejezésére hasznosak, amelyeket egy minta önmagában nem tesz lehetővé. Vedd
azonban figyelembe, hogy csak `match` kifejezésekben érhetők el, `if let` vagy
`while let` kifejezésekben nem.

A feltétel használhatja a mintában létrehozott változókat. A 19-26.
kódrészlet egy olyan `match`-et mutat, amelynek első ágában a `Some(x)` minta
áll, és mellette egy `if x % 2 == 0` őrfeltétel (amely `true`, ha a szám
páros).

<Listing number="19-26" caption="Őrfeltétel hozzáadása egy mintához">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-26/src/main.rs:here}}
```

</Listing>

Ez a példa a `The number 4 is even` szöveget írja ki. Amikor a `num` értéket
az első ág mintájával vetjük össze, illeszkedik, mert a `Some(4)` illeszkedik a
`Some(x)` mintára. Ezután az őrfeltétel ellenőrzi, hogy az `x` 2-vel való
osztásának maradéka egyenlő-e 0-val, és mivel igen, az első ág kerül
kiválasztásra.

Ha a `num` értéke `Some(5)` lett volna, az első ág őrfeltétele `false` lett
volna, mert az 5 2-vel való osztásának maradéka 1, ami nem egyenlő 0-val. A
Rust ekkor a második ágra lépett volna, amely illeszkedett volna, mert a
második ágnak nincs őrfeltétele, így bármely `Some` változatra illeszkedik.

Az `if x % 2 == 0` feltételt egy mintán belül nem lehet kifejezni, így az
őrfeltétel adja meg nekünk a lehetőséget ennek a logikának a kifejezésére. Ennek
a többlet kifejezőerőnek az a hátránya, hogy őrfeltételes kifejezések esetén a
fordító meg sem próbálja ellenőrizni a kimerítőséget.

A 19-11. kódrészlet tárgyalásakor említettük, hogy az őrfeltételekkel
megoldhatjuk a mintaárnyékolási problémánkat. Emlékezz vissza, hogy a `match`
kifejezés mintájában új változót hoztunk létre ahelyett, hogy a `match`-en
kívüli változót használtuk volna. Az új változó miatt nem tudtuk a külső
változó értékével összevetni az értéket. A 19-27. kódrészlet bemutatja, hogyan
javíthatjuk ki ezt a problémát egy őrfeltétellel.

<Listing number="19-27" file-name="src/main.rs" caption="Őrfeltétel használata egy külső változóval való egyenlőség vizsgálatára">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-27/src/main.rs}}
```

</Listing>

Ez a kód most a `Default case, x = Some(5)` szöveget írja ki. A második match
ág mintája nem vezet be új `y` változót, amely árnyékolná a külső `y`-t, így
az őrfeltételben a külső `y`-t használhatjuk. A mintát nem `Some(y)`-ként adjuk
meg, ami árnyékolta volna a külső `y`-t, hanem `Some(n)`-ként. Ez egy új `n`
változót hoz létre, amely semmit sem árnyékol, mert a `match`-en kívül nincs
`n` változó.

Az `if n == y` őrfeltétel nem minta, ezért nem vezet be új változókat. Ez az
`y` _valóban_ a külső `y`, nem pedig egy azt árnyékoló új `y`, és az `n` és
az `y` összehasonlításával olyan értéket kereshetünk, amely megegyezik a
külső `y` értékével.

Egy őrfeltételben a _vagy_ operátort (`|`) is használhatod több minta
megadására; az őrfeltétel ilyenkor az összes mintára vonatkozik. A 19-28.
kódrészlet a precedenciát mutatja be, amikor egy `|`-t használó mintát
őrfeltétellel kombinálunk. A példa lényege, hogy az `if y` őrfeltétel a `4`,
az `5` _és_ a `6` értékre is vonatkozik, még ha úgy is tűnhet, hogy az `if y`
csak a `6`-ra.

<Listing number="19-28" caption="Több minta kombinálása őrfeltétellel">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-28/src/main.rs:here}}
```

</Listing>

Az illesztési feltétel szerint az ág csak akkor illeszkedik, ha az `x` értéke
`4`, `5` vagy `6`, _és_ az `y` értéke `true`. Amikor ez a kód lefut, az első
ág mintája illeszkedik, mert az `x` értéke `4`, de az `if y` őrfeltétel
`false`, így az első ág nem kerül kiválasztásra. A kód továbblép a második
ágra, amely illeszkedik, és a program a `no` szöveget írja ki. Ennek oka, hogy
az `if` feltétel a teljes `4 | 5 | 6` mintára vonatkozik, nem csak az utolsó
`6` értékre. Más szóval az őrfeltétel precedenciája a mintához képest így
működik:

```text
(4 | 5 | 6) if y => ...
```

nem pedig így:

```text
4 | 5 | (6 if y) => ...
```

A kód futtatása után a precedencia egyértelművé válik: ha az őrfeltétel csak a
`|` operátorral megadott értéklista utolsó értékére vonatkozna, az ág
illeszkedett volna, és a program a `yes` szöveget írta volna ki.

<!-- Old headings. Do not remove or links may break. -->

<a id="-bindings"></a>

### A `@` kötések használata {#using--bindings}

A `@` (_at_) operátorral olyan változót hozhatunk létre, amely egy értéket
tárol, miközben ugyanazt az értéket egy mintára illeszkedés szempontjából
vizsgáljuk. A 19-29. kódrészletben azt szeretnénk megvizsgálni, hogy egy
`Message::Hello` `id` mezője a `3..=7` tartományba esik-e. Az értéket emellett
az `id` változóhoz is kötni szeretnénk, hogy az ághoz tartozó kódban
használhassuk.

<Listing number="19-29" caption="A `@` használata egy mintabeli értékhez való kötésre és egyidejű vizsgálatára">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-29/src/main.rs:here}}
```

</Listing>

Ez a példa a `Found an id in range: 5` szöveget írja ki. Azzal, hogy a `3..=7`
tartomány elé `id @`-et írunk, a tartományra illeszkedő értéket egy `id` nevű
változóba mentjük, miközben azt is megvizsgáljuk, hogy az érték illeszkedik-e
a tartománymintára.

A második ágban, ahol a mintában csak egy tartományt adtunk meg, az ághoz
tartozó kódnak nincs olyan változója, amely az `id` mező tényleges értékét
tartalmazná. Az `id` mező értéke lehetett 10, 11 vagy 12, de a mintához
tartozó kód nem tudja, melyik. A minta kódja nem tudja használni az `id` mező
értékét, mert az `id` értékét nem mentettük el egy változóba.

Az utolsó ágban, ahol tartomány nélküli változót adtunk meg, az érték az ág
kódjában egy `id` nevű változóban elérhető. Ennek oka, hogy a rövidített
mezőírásmódot használtuk. Ebben az ágban azonban nem vizsgáltuk meg az `id`
mező értékét úgy, mint az első két ágban: bármilyen érték illeszkedne erre a
mintára.

A `@` segítségével egyetlen mintán belül vizsgálhatunk meg egy értéket és
menthetjük el egy változóba.

## Összefoglalás {#summary}

A Rust mintái nagyon hasznosak a különböző fajta adatok megkülönböztetésében.
A `match` kifejezésekben a Rust biztosítja, hogy a minták minden lehetséges
értéket lefedjenek, különben a program nem fordul le. A `let` utasításokban és
a függvényparaméterekben lévő minták hasznosabbá teszik ezeket a
szerkezeteket, mert lehetővé teszik az értékek kisebb részekre bontását és e
részek változókhoz rendelését. Az igényeinknek megfelelően egyszerű vagy
összetett mintákat hozhatunk létre.

A könyv utolsó előtti fejezetében a Rust különféle nyelvi elemeinek néhány
haladó vonatkozását vesszük szemügyre.
