<!-- Old headings. Do not remove or links may break. -->

<a id="using-trait-objects-that-allow-for-values-of-different-types"></a>

## Trait objektumok használata a közös viselkedés absztrahálására {#using-trait-objects-to-abstract-over-shared-behavior}

A 8. fejezetben említettük, hogy a vektorok egyik korlátja, hogy csak egyféle
típusú elemet tárolhatnak. A 8-9. kódrészletben találtunk erre egy kerülőutat:
definiáltunk egy `SpreadsheetCell` enumot, amelynek változatai egész számokat,
lebegőpontos számokat és szöveget tárolhattak. Így minden cellában különböző
típusú adatot tárolhattunk, és mégis lehetett egy vektorunk, amely egy
cellasort ábrázolt. Ez tökéletesen jó megoldás, ha az egymással felcserélhető
elemeink típusai egy rögzített halmazból kerülnek ki, amelyet a kód
fordításakor ismerünk.

Néha azonban azt szeretnénk, hogy a könyvtárunk felhasználója bővíthesse az
adott helyzetben érvényes típusok halmazát. Hogy megmutassuk, hogyan érhetjük
ezt el, készítünk egy példa grafikus felhasználói felület (GUI) eszközt, amely
végigmegy egy elemlistán, és mindegyik elemen meghív egy `draw` metódust, hogy
kirajzolja a képernyőre – ez gyakori technika a GUI-eszközökben. Létrehozunk
egy `gui` nevű könyvtár crate-et, amely egy GUI-könyvtár szerkezetét
tartalmazza. Ez a crate tartalmazhat néhány típust, például `Button`-t vagy
`TextField`-et, amelyeket mások használhatnak. Ezen felül a `gui`
felhasználói saját, kirajzolható típusokat is szeretnének majd létrehozni:
az egyik programozó például hozzáadhat egy `Image`-et, egy másik pedig egy
`SelectBox`-ot.

A könyvtár megírásakor nem ismerhetjük és nem definiálhatjuk az összes típust,
amelyet más programozók létre akarhatnak hozni. Azt viszont tudjuk, hogy a
`gui`-nak sok különböző típusú értéket kell nyilvántartania, és mindegyik
ilyen, eltérő típusú értéken meg kell hívnia egy `draw` metódust. Nem kell
pontosan tudnia, mi történik, amikor meghívjuk a `draw` metódust, csak azt,
hogy az érték rendelkezik ezzel a meghívható metódussal.

Egy öröklődést ismerő nyelvben ehhez definiálhatnánk egy `Component` nevű
osztályt, amelynek van egy `draw` nevű metódusa. A többi osztály, például a
`Button`, az `Image` és a `SelectBox`, a `Component` osztályból örökölne, így
megörökölné a `draw` metódust. Mindegyik felülírhatná a `draw` metódust, hogy
meghatározza a saját egyedi viselkedését, a keretrendszer pedig az összes típust
`Component` példányként kezelhetné, és meghívhatná rajtuk a `draw` metódust.
Mivel azonban a Rustban nincs öröklődés, más módon kell felépítenünk a `gui`
könyvtárat, hogy a felhasználók a könyvtárral kompatibilis új típusokat
hozhassanak létre.

### Trait definiálása a közös viselkedéshez {#defining-a-trait-for-common-behavior}

A `gui` kívánt viselkedésének megvalósításához definiálunk egy `Draw` nevű
traitet, amelynek egyetlen, `draw` nevű metódusa lesz. Ezután definiálhatunk egy
vektort, amely trait objektumokat tárol. Egy _trait objektum (trait object)_
egyszerre mutat a megadott traitet megvalósító típus egy példányára és egy
táblázatra, amellyel futásidőben kikereshetők az adott típus trait-metódusai.
Trait objektumot úgy hozunk létre, hogy megadunk valamilyen mutatót, például
egy referenciát vagy egy `Box<T>` okos mutatót, majd a `dyn` kulcsszót, végül
pedig a megfelelő traitet. (Azt, hogy a trait objektumoknak miért kell mutatót
használniuk, a 20. fejezet [„A dinamikus méretű típusok és a `Sized`
trait”][dynamically-sized]<!-- ignore --> szakaszában tárgyaljuk.) A trait
objektumokat generikus vagy konkrét típus helyett használhatjuk. Ahol trait
objektumot használunk, a Rust típusrendszere fordítási időben biztosítja, hogy
az abban a környezetben használt összes érték megvalósítsa a trait objektum
traitjét. Emiatt nem kell fordítási időben ismernünk az összes lehetséges
típust.

Említettük, hogy a Rustban tartózkodunk attól, hogy a struktúrákat és az
enumokat „objektumoknak” nevezzük, hogy megkülönböztessük őket más nyelvek
objektumaitól. Egy struktúrában vagy enumban a struktúra mezőiben lévő adatok
és az `impl` blokkokban lévő viselkedés el vannak választva egymástól, míg más
nyelvekben az egyetlen fogalomba egyesített adatot és viselkedést gyakran
nevezik objektumnak. A trait objektumok abban különböznek más nyelvek
objektumaitól, hogy egy trait objektumhoz nem adhatunk hozzá adatot. A trait
objektumok nem olyan általánosan hasznosak, mint más nyelvek objektumai:
kifejezett céljuk, hogy lehetővé tegyék a közös viselkedés feletti
absztrakciót.

A 18-3. kódrészlet azt mutatja, hogyan definiálhatunk egy `Draw` nevű traitet
egyetlen, `draw` nevű metódussal.

<Listing number="18-3" file-name="src/lib.rs" caption="A `Draw` trait definíciója">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-03/src/lib.rs}}
```

</Listing>

Ez a szintaxis ismerős lehet a 10. fejezetből, ahol a traitek definiálásáról
beszéltünk. Ezután némi új szintaxis következik: a 18-4. kódrészlet egy
`Screen` nevű struktúrát definiál, amely egy `components` nevű vektort tárol.
Ennek a vektornak a típusa `Box<dyn Draw>`, ami egy trait objektum; bármely
olyan, `Box`-ban lévő típust helyettesít, amely megvalósítja a `Draw` traitet.

<Listing number="18-4" file-name="src/lib.rs" caption="A `Screen` struktúra definíciója egy `components` mezővel, amely a `Draw` traitet megvalósító trait objektumok vektorát tárolja">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-04/src/lib.rs:here}}
```

</Listing>

A `Screen` struktúrán definiálunk egy `run` nevű metódust, amely a
`components` mindegyik elemén meghívja a `draw` metódust, ahogy a 18-5.
kódrészlet mutatja.

<Listing number="18-5" file-name="src/lib.rs" caption="Egy `run` metódus a `Screen` típuson, amely minden komponensen meghívja a `draw` metódust">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-05/src/lib.rs:here}}
```

</Listing>

Ez másképp működik, mint egy olyan struktúra definiálása, amely trait-korlátos
generikus típusparamétert használ. Egy generikus típusparamétert egyszerre csak
egyetlen konkrét típus helyettesíthet, a trait objektumok viszont lehetővé
teszik, hogy futásidőben több konkrét típus is a trait objektum helyére
kerüljön. Definiálhattuk volna például a `Screen` struktúrát generikus típussal
és trait-korláttal is, ahogy a 18-6. kódrészletben.

<Listing number="18-6" file-name="src/lib.rs" caption="A `Screen` struktúra és `run` metódusa egy alternatív, generikus típusokat és trait-korlátokat használó megvalósítása">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-06/src/lib.rs:here}}
```

</Listing>

Ez olyan `Screen` példányra korlátoz minket, amelynek komponenslistájában vagy
csupa `Button`, vagy csupa `TextField` típusú elem van. Ha mindig csak homogén
gyűjteményeid lesznek, érdemesebb generikus típusokat és trait-korlátokat
használni, mert a definíciók fordítási időben monomorfizálódnak, és a konkrét
típusokat használják.

Ezzel szemben a trait objektumokat használó metódusnál egyetlen `Screen`
példány is tárolhat olyan `Vec<T>`-t, amely egy `Box<Button>`-t és egy
`Box<TextField>`-et is tartalmaz. Nézzük meg, hogyan működik ez, majd
beszélünk a futásidejű teljesítményre gyakorolt hatásáról is.

### A trait megvalósítása {#implementing-the-trait}

Most hozzáadunk néhány típust, amely megvalósítja a `Draw` traitet. Megadjuk a
`Button` típust. Egy GUI-könyvtár tényleges megvalósítása ismét csak
meghaladja e könyv kereteit, ezért a `draw` metódus törzsében nem lesz hasznos
megvalósítás. Hogy elképzeld, hogyan nézhetne ki a megvalósítás, egy `Button`
struktúrának lehetnek `width`, `height` és `label` mezői, ahogy a 18-7.
kódrészlet mutatja.

<Listing number="18-7" file-name="src/lib.rs" caption="Egy `Button` struktúra, amely megvalósítja a `Draw` traitet">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-07/src/lib.rs:here}}
```

</Listing>

A `Button` `width`, `height` és `label` mezői eltérnek majd más komponensek
mezőitől; egy `TextField` típusnak például ugyanezek a mezői lehetnek, és még
egy `placeholder` mező is. Minden típus, amelyet a képernyőre szeretnénk
rajzolni, megvalósítja a `Draw` traitet, de a `draw` metódusban más-más kód
határozza meg, hogyan rajzoljuk ki az adott típust, ahogy itt a `Button`
esetében is (a tényleges GUI-kód nélkül, ahogy említettük). A `Button`
típusnak lehet például egy további `impl` blokkja is olyan metódusokkal,
amelyek ahhoz kapcsolódnak, mi történik, amikor a felhasználó a gombra
kattint. Az ilyen metódusok nem vonatkoznak a `TextField`-hez hasonló
típusokra.

Ha a könyvtárunk valamelyik felhasználója úgy dönt, hogy megvalósít egy
`SelectBox` struktúrát `width`, `height` és `options` mezőkkel, akkor a
`SelectBox` típuson is megvalósítja a `Draw` traitet, ahogy a 18-8. kódrészlet
mutatja.

<Listing number="18-8" file-name="src/main.rs" caption="Egy másik crate, amely a `gui`-t használja, és megvalósítja a `Draw` traitet egy `SelectBox` struktúrán">

```rust,ignore
{{#rustdoc_include ../listings/ch18-oop/listing-18-08/src/main.rs:here}}
```

</Listing>

A könyvtárunk felhasználója most megírhatja a `main` függvényét, amely
létrehoz egy `Screen` példányt. A `Screen` példányhoz hozzáadhat egy
`SelectBox`-ot és egy `Button`-t úgy, hogy mindegyiket `Box<T>`-be teszi, így
azok trait objektummá válnak. Ezután meghívhatja a `Screen` példány `run`
metódusát, amely mindegyik komponensen meghívja a `draw` metódust. A 18-9.
kódrészlet ezt a megvalósítást mutatja.

<Listing number="18-9" file-name="src/main.rs" caption="Trait objektumok használata ugyanazt a traitet megvalósító, különböző típusú értékek tárolására">

```rust,ignore
{{#rustdoc_include ../listings/ch18-oop/listing-18-09/src/main.rs:here}}
```

</Listing>

Amikor a könyvtárat megírtuk, nem tudtuk, hogy valaki hozzáadhatja a
`SelectBox` típust, a `Screen` megvalósításunk mégis képes volt az új típussal
dolgozni és kirajzolni azt, mert a `SelectBox` megvalósítja a `Draw` traitet,
vagyis megvalósítja a `draw` metódust.

Ez a gondolat – hogy csak azzal foglalkozunk, milyen üzenetekre válaszol egy
érték, nem pedig az érték konkrét típusával – hasonlít a dinamikusan típusos
nyelvek _kacsatípusosság (duck typing)_ fogalmához: ha úgy jár, mint egy kacsa,
és úgy hápog, mint egy kacsa, akkor az bizony kacsa! A `Screen` `run`
metódusának a 18-5. kódrészletben szereplő megvalósításában a `run`-nak nem
kell tudnia, mi az egyes komponensek konkrét típusa. Nem ellenőrzi, hogy egy
komponens `Button` vagy `SelectBox` példány-e, egyszerűen meghívja rajta a
`draw` metódust. Azzal, hogy a `components` vektor értékeinek típusaként
`Box<dyn Draw>`-t adtunk meg, úgy definiáltuk a `Screen` típust, hogy olyan
értékekre legyen szüksége, amelyeken meghívhatjuk a `draw` metódust.

Annak előnye, hogy trait objektumokkal és a Rust típusrendszerével a
kacsatípusosságot használó kódhoz hasonló kódot írunk, az, hogy soha nem kell
futásidőben ellenőriznünk, megvalósít-e egy érték egy adott metódust, és nem
kell aggódnunk amiatt, hogy hibát kapunk, ha egy érték nem valósít meg egy
metódust, mi mégis meghívjuk. A Rust nem fordítja le a kódunkat, ha az értékek
nem valósítják meg azokat a traiteket, amelyekre a trait objektumoknak
szükségük van.

A 18-10. kódrészlet például azt mutatja, mi történik, ha egy olyan `Screen`-t
próbálunk létrehozni, amelynek egyik komponense egy `String`.

<Listing number="18-10" file-name="src/main.rs" caption="Kísérlet olyan típus használatára, amely nem valósítja meg a trait objektum traitjét">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch18-oop/listing-18-10/src/main.rs}}
```

</Listing>

Ezt a hibát kapjuk, mert a `String` nem valósítja meg a `Draw` traitet:

```console
{{#include ../listings/ch18-oop/listing-18-10/output.txt}}
```

Ez a hiba jelzi, hogy vagy olyasmit adunk át a `Screen`-nek, amit nem akartunk,
és ezért más típust kellene átadnunk, vagy meg kellene valósítanunk a `Draw`
traitet a `String` típuson, hogy a `Screen` meghívhassa rajta a `draw`
metódust.

<!-- Old headings. Do not remove or links may break. -->

<a id="trait-objects-perform-dynamic-dispatch"></a>

### Dinamikus hívásfeloldás {#performing-dynamic-dispatch}

Idézd fel a 10. fejezet [„A generikus típusokat használó kód
teljesítménye”][performance-of-code-using-generics]<!-- ignore --> című
szakaszát, ahol arról volt szó, hogyan monomorfizálja a fordító a generikus
típusokat: a fordító minden olyan konkrét típushoz, amelyet egy generikus
típusparaméter helyén használunk, a függvények és metódusok nem generikus
megvalósításait állítja elő. A monomorfizációból származó kód _statikus
hívásfeloldást (static dispatch)_ végez, ami azt jelenti, hogy a fordító már
fordítási időben tudja, melyik metódust hívod meg. Ennek ellentéte a
_dinamikus hívásfeloldás (dynamic dispatch)_, amikor a fordító fordítási időben
nem tudja megállapítani, melyik metódust hívod meg. Dinamikus hívásfeloldás
esetén a fordító olyan kódot állít elő, amely futásidőben fogja tudni, melyik
metódust kell meghívni.

Trait objektumok használatakor a Rustnak dinamikus hívásfeloldást kell
alkalmaznia. A fordító nem ismeri az összes típust, amelyet a trait
objektumokat használó kóddal használhatnak, ezért nem tudja, melyik típuson
megvalósított melyik metódust kell meghívnia. Ehelyett a Rust futásidőben a
trait objektumban lévő mutatók alapján dönti el, melyik metódust hívja meg. Ez
a kikeresés olyan futásidejű költséggel jár, amely statikus hívásfeloldásnál
nem merül fel. A dinamikus hívásfeloldás azt is megakadályozza, hogy a fordító
beágyazza (inline) egy metódus kódját, ami pedig bizonyos optimalizációkat
akadályoz meg. A Rustnak ráadásul vannak szabályai arra, hol használható és hol
nem a dinamikus hívásfeloldás; ezeket _dyn-kompatibilitásnak (dyn
compatibility)_ nevezzük. Ezek a szabályok túlmutatnak a mostani tárgyaláson,
de bővebben olvashatsz róluk
[a referenciában][dyn-compatibility]<!-- ignore -->. Ugyanakkor nagyobb
rugalmasságot nyertünk a 18-5. kódrészletben megírt és a 18-9. kódrészletben
támogatott kódban, így ez mérlegelendő kompromisszum.

[performance-of-code-using-generics]: ch10-01-syntax.html#performance-of-code-using-generics
[dynamically-sized]: ch20-03-advanced-types.html#dynamically-sized-types-and-the-sized-trait
[dyn-compatibility]: https://doc.rust-lang.org/reference/items/traits.html#dyn-compatibility
