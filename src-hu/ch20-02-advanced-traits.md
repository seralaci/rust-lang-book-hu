## Haladó traitek {#advanced-traits}

A traitekkel először a 10. fejezet [„Közös viselkedés definiálása
traitekkel”][traits]<!-- ignore --> szakaszában foglalkoztunk, de a haladóbb
részletekről nem esett szó. Most, hogy már többet tudsz a Rustról, a
részletekbe is belemehetünk.

<!-- Old headings. Do not remove or links may break. -->

<a id="specifying-placeholder-types-in-trait-definitions-with-associated-types"></a>
<a id="associated-types"></a>

### Traitek definiálása társított típusokkal {#defining-traits-with-associated-types}

A _társított típusok (associated types)_ egy típus-helyőrzőt kapcsolnak egy
traithez úgy, hogy a trait metódusdefiníciói a szignatúrájukban használhassák
ezeket a helyőrző típusokat. A trait megvalósítója adja meg, hogy az adott
megvalósításban melyik konkrét típus álljon a helyőrző típus helyén. Így olyan
traitet definiálhatunk, amely bizonyos típusokat használ, anélkül hogy pontosan
tudnunk kellene, melyek ezek a típusok, egészen addig, amíg a traitet meg nem
valósítják.

A fejezetben tárgyalt haladó nyelvi elemek többségéről azt mondtuk, hogy ritkán
van rájuk szükség. A társított típusok valahol középen helyezkednek el:
ritkábban használjuk őket, mint a könyv többi részében bemutatott nyelvi
elemeket, de gyakrabban, mint az ebben a fejezetben tárgyalt sok más elemet.

Társított típussal rendelkező traitre példa a standard könyvtár `Iterator`
traitje. A társított típus neve `Item`, és azoknak az értékeknek a típusát
képviseli, amelyeken az `Iterator` traitet megvalósító típus végigiterál. Az
`Iterator` trait definícióját a 20-13. kódrészlet mutatja.

<Listing number="20-13" caption="Az `Iterator` trait definíciója, amelynek van egy `Item` társított típusa">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-13/src/lib.rs}}
```

</Listing>

Az `Item` típus egy helyőrző, a `next` metódus definíciója pedig azt mutatja,
hogy `Option<Self::Item>` típusú értékeket fog visszaadni. Az `Iterator` trait
megvalósítói adják meg az `Item` konkrét típusát, a `next` metódus pedig egy
ilyen konkrét típusú értéket tartalmazó `Option`-t ad vissza.

A társított típusok a generikus típusokhoz hasonló fogalomnak tűnhetnek,
hiszen az utóbbiakkal is úgy definiálhatunk függvényt, hogy nem adjuk meg,
milyen típusokat képes kezelni. A két fogalom közötti különbség megvizsgálásához
nézzük meg az `Iterator` trait megvalósítását egy `Counter` nevű típuson,
amely azt adja meg, hogy az `Item` típus `u32`:

<Listing file-name="src/lib.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-22-iterator-on-counter/src/lib.rs:ch19}}
```

</Listing>

Ez a szintaxis a generikus típusokéhoz hasonlónak tűnik. Akkor miért nem
definiáljuk egyszerűen generikus típusokkal az `Iterator` traitet, ahogy a
20-14. kódrészlet mutatja?

<Listing number="20-14" caption="Az `Iterator` trait egy elképzelt, generikus típusokat használó definíciója">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-14/src/lib.rs}}
```

</Listing>

A különbség az, hogy generikus típusok használatakor, mint a 20-14.
kódrészletben, minden megvalósításban annotálnunk kell a típusokat; mivel
megvalósíthatjuk az `Iterator<String> for Counter`-t vagy bármilyen más típust
is, az `Iterator`-nak több megvalósítása is lehetne a `Counter`-re. Más szóval,
ha egy traitnek generikus paramétere van, egy típusra többször is
megvalósítható, mindig más konkrét típusokat adva a generikus
típusparamétereknek. Amikor a `Counter`-en a `next` metódust használjuk,
típusannotációkkal kellene jeleznünk, hogy az `Iterator` melyik megvalósítását
szeretnénk használni.

Társított típusok esetén nem kell annotálnunk a típusokat, mert egy traitet nem
valósíthatunk meg többször ugyanarra a típusra. A 20-13. kódrészletben, a
társított típusokat használó definícióval, csak egyszer választhatjuk meg, mi
legyen az `Item` típusa, mert csak egy `impl Iterator for Counter` lehet. Nem
kell mindenhol megadnunk, hogy `u32` értékek iterátorát szeretnénk, ahol a
`Counter`-en meghívjuk a `next`-et.

A társított típusok a trait szerződésének is részévé válnak: a trait
megvalósítóinak meg kell adniuk egy típust, amely a társított típus helyőrzője
helyén áll. A társított típusoknak gyakran olyan nevük van, amely leírja, hogyan
használjuk majd a típust, és jó gyakorlat a társított típust az
API-dokumentációban is dokumentálni.

<!-- Old headings. Do not remove or links may break. -->

<a id="default-generic-type-parameters-and-operator-overloading"></a>

### Alapértelmezett generikus paraméterek és operátor-túlterhelés {#using-default-generic-parameters-and-operator-overloading}

Generikus típusparaméterek használatakor megadhatunk egy alapértelmezett
konkrét típust a generikus típushoz. Így a trait megvalósítóinak nem kell
konkrét típust megadniuk, ha az alapértelmezett típus megfelel. Az
alapértelmezett típust a generikus típus deklarálásakor a
`<PlaceholderType=ConcreteType>` szintaxissal adhatod meg.

Remek példa arra a helyzetre, ahol ez a technika hasznos, az
_operátor-túlterhelés (operator overloading)_, amellyel egy operátor (például a
`+`) viselkedését szabhatod testre bizonyos helyzetekben.

A Rust nem engedi, hogy saját operátorokat hozz létre, vagy tetszőleges
operátorokat túlterhelj. Az `std::ops`-ban felsorolt műveleteket és a hozzájuk
tartozó traiteket azonban túlterhelheted, ha megvalósítod az operátorhoz
tartozó traiteket. A 20-15. kódrészletben például túlterheljük a `+` operátort,
hogy két `Point` példányt összeadhassunk. Ezt úgy tesszük, hogy egy `Point`
struktúrán megvalósítjuk az `Add` traitet.

<Listing number="20-15" file-name="src/main.rs" caption="Az `Add` trait megvalósítása a `+` operátor túlterhelésére `Point` példányokhoz">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-15/src/main.rs}}
```

</Listing>

Az `add` metódus összeadja két `Point` példány `x` értékeit és `y` értékeit,
és ezekből új `Point`-ot hoz létre. Az `Add` traitnek van egy `Output` nevű
társított típusa, amely meghatározza az `add` metódus visszatérési típusát.

Ebben a kódban az alapértelmezett generikus típus az `Add` traiten belül van.
Íme a definíciója:

```rust
trait Add<Rhs=Self> {
    type Output;

    fn add(self, rhs: Rhs) -> Self::Output;
}
```

Ez a kód nagyjából ismerősnek tűnhet: egy trait egy metódussal és egy
társított típussal. Az új rész a `Rhs=Self`: ezt a szintaxist
_alapértelmezett típusparamétereknek (default type parameters)_ nevezzük. Az
`Rhs` generikus típusparaméter (a „right-hand side”, azaz „jobb oldal”
rövidítése) az `add` metódus `rhs` paraméterének típusát határozza meg. Ha az
`Add` trait megvalósításakor nem adunk meg konkrét típust az `Rhs`-nek, az
`Rhs` típusa alapértelmezés szerint `Self` lesz, vagyis az a típus, amelyen az
`Add`-et megvalósítjuk.

Amikor az `Add`-et a `Point`-ra valósítottuk meg, az `Rhs` alapértelmezését
használtuk, mert két `Point` példányt akartunk összeadni. Nézzünk egy olyan
példát az `Add` trait megvalósítására, amelyben az alapértelmezés helyett
testre szeretnénk szabni az `Rhs` típust.

Van két struktúránk, a `Millimeters` és a `Meters`, amelyek különböző
mértékegységben tárolnak értékeket. Egy meglévő típus ilyen vékony
becsomagolását egy másik struktúrába _newtype mintának (newtype pattern)_
nevezzük; ezt részletesebben a [„Külső traitek megvalósítása a newtype
mintával”][newtype]<!-- ignore --> szakaszban írjuk le. Milliméterben megadott
értékeket szeretnénk méterben megadott értékekhez adni úgy, hogy az `Add`
megvalósítása helyesen végezze el az átváltást. Az `Add`-et megvalósíthatjuk a
`Millimeters`-re úgy, hogy a `Meters` legyen az `Rhs`, ahogy a 20-16. kódrészlet
mutatja.

<Listing number="20-16" file-name="src/lib.rs" caption="Az `Add` trait megvalósítása a `Millimeters`-en a `Millimeters` és a `Meters` összeadásához">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-16/src/lib.rs}}
```

</Listing>

A `Millimeters` és a `Meters` összeadásához az `impl Add<Meters>` alakot
használjuk, hogy az `Rhs` típusparaméter értékét a `Self` alapértelmezés
helyett mi adjuk meg.

Az alapértelmezett típusparamétereket két fő célra használod:

1. Egy típus kiterjesztésére a meglévő kód elrontása nélkül
2. Testreszabás lehetővé tételére olyan speciális esetekben, amelyekre a
   legtöbb felhasználónak nincs szüksége

A standard könyvtár `Add` traitje a második célra példa: általában két azonos
típusú értéket adsz össze, de az `Add` trait lehetővé teszi, hogy ennél
tovább is testre szabd. Az alapértelmezett típusparaméter használata az `Add`
trait definíciójában azt jelenti, hogy legtöbbször nem kell megadnod az extra
paramétert. Más szóval, nincs szükség egy kis megvalósítási sablonkódra, így
könnyebb használni a traitet.

Az első cél a másodikhoz hasonló, csak fordítva: ha egy meglévő traithez
típusparamétert szeretnél hozzáadni, adhatsz neki alapértelmezést, hogy a
trait funkcionalitását a meglévő megvalósítási kód elrontása nélkül
bővíthesd.

<!-- Old headings. Do not remove or links may break. -->

<a id="fully-qualified-syntax-for-disambiguation-calling-methods-with-the-same-name"></a>
<a id="disambiguating-between-methods-with-the-same-name"></a>

### Azonos nevű metódusok megkülönböztetése {#disambiguating-between-identically-named-methods}

A Rustban semmi sem akadályozza meg, hogy egy traitnek ugyanolyan nevű
metódusa legyen, mint egy másik trait metódusának, és azt sem, hogy mindkét
traitet megvalósítsd ugyanazon a típuson. Az is lehetséges, hogy közvetlenül a
típuson valósíts meg egy metódust, amelynek ugyanaz a neve, mint a traitek
metódusainak.

Azonos nevű metódusok hívásakor meg kell mondanod a Rustnak, melyiket
szeretnéd használni. Vegyük a 20-17. kódrészlet kódját, amelyben két traitet
definiáltunk, a `Pilot`-ot és a `Wizard`-ot, amelyeknek egyaránt van egy `fly`
nevű metódusa. Ezután mindkét traitet megvalósítjuk egy `Human` típuson,
amelyen már meg van valósítva egy `fly` nevű metódus. Mindegyik `fly` metódus
mást csinál.

<Listing number="20-17" file-name="src/main.rs" caption="Két trait, amelyeknek van `fly` metódusa, és amelyeket a `Human` típuson valósítunk meg, valamint egy közvetlenül a `Human`-en megvalósított `fly` metódus">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-17/src/main.rs:here}}
```

</Listing>

Amikor egy `Human` példányon meghívjuk a `fly`-t, a fordító alapértelmezés
szerint a közvetlenül a típuson megvalósított metódust hívja meg, ahogy a
20-18. kódrészlet mutatja.

<Listing number="20-18" file-name="src/main.rs" caption="A `fly` meghívása egy `Human` példányon">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-18/src/main.rs:here}}
```

</Listing>

A kód futtatása a `*waving arms furiously*` szöveget írja ki, ami azt
mutatja, hogy a Rust a közvetlenül a `Human`-en megvalósított `fly` metódust
hívta meg.

Ahhoz, hogy a `Pilot` vagy a `Wizard` trait `fly` metódusát hívjuk meg,
explicitebb szintaxissal kell megadnunk, melyik `fly` metódusra gondolunk. A
20-19. kódrészlet ezt a szintaxist mutatja be.

<Listing number="20-19" file-name="src/main.rs" caption="Annak megadása, hogy melyik trait `fly` metódusát szeretnénk meghívni">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-19/src/main.rs:here}}
```

</Listing>

Ha a metódus neve elé kiírjuk a trait nevét, azzal egyértelművé tesszük a
Rust számára, hogy a `fly` melyik megvalósítását szeretnénk meghívni. Azt is
írhatnánk, hogy `Human::fly(&person)`, ami egyenértékű a 20-19. kódrészletben
használt `person.fly()`-jal, de ezt kicsit hosszabb leírni, ha nincs szükség
egyértelműsítésre.

A kód futtatása a következőt írja ki:

```console
{{#include ../listings/ch20-advanced-features/listing-20-19/output.txt}}
```

Mivel a `fly` metódus `self` paramétert kap, ha két olyan _típusunk_ lenne,
amelyek ugyanazt az egy _traitet_ valósítják meg, a Rust a `self` típusa
alapján ki tudná találni, hogy a trait melyik megvalósítását használja.

A nem metódus jellegű társított függvényeknek azonban nincs `self` paraméterük.
Ha több típus vagy trait is definiál azonos nevű, nem metódus jellegű függvényt,
a Rust nem mindig tudja, melyik típusra gondolsz, hacsak nem használsz teljesen
minősített szintaxist (fully qualified syntax). A 20-20. kódrészletben például
egy traitet hozunk létre egy állatmenhely számára, amely minden kiskutyát
Spotnak szeretne elnevezni. Létrehozunk egy `Animal` traitet egy nem metódus
jellegű `baby_name` társított függvénnyel. Az `Animal` traitet a `Dog`
struktúrára valósítjuk meg, amelyen közvetlenül is megadunk egy nem metódus
jellegű `baby_name` társított függvényt.

<Listing number="20-20" file-name="src/main.rs" caption="Egy trait társított függvénnyel, és egy típus, amelynek ugyanilyen nevű társított függvénye van, és amely a traitet is megvalósítja">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-20/src/main.rs}}
```

</Listing>

Az összes kiskutyát Spotnak elnevező kódot a `Dog`-on definiált `baby_name`
társított függvényben valósítjuk meg. A `Dog` típus az `Animal` traitet is
megvalósítja, amely az összes állat közös jellemzőit írja le. A kutyakölyköket
angolul puppynak hívják, és ezt a `Dog`-on megvalósított `Animal` trait
`baby_name` függvénye fejezi ki.

A `main`-ben a `Dog::baby_name` függvényt hívjuk meg, ami a közvetlenül a
`Dog`-on definiált társított függvényt hívja meg. A kód a következőt írja ki:

```console
{{#include ../listings/ch20-advanced-features/listing-20-20/output.txt}}
```

Nem ezt a kimenetet szerettük volna. A `Dog`-on megvalósított `Animal` trait
részét képező `baby_name` függvényt szeretnénk meghívni, hogy a kód az
`A baby dog is called a puppy` szöveget írja ki. A trait nevének megadása,
amelyet a 20-19. kódrészletben használtunk, itt nem segít; ha a `main`-t a
20-21. kódrészlet kódjára változtatjuk, fordítási hibát kapunk.

<Listing number="20-21" file-name="src/main.rs" caption="Kísérlet az `Animal` trait `baby_name` függvényének meghívására, de a Rust nem tudja, melyik megvalósítást használja">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-21/src/main.rs:here}}
```

</Listing>

Mivel az `Animal::baby_name`-nek nincs `self` paramétere, és más típusok is
megvalósíthatják az `Animal` traitet, a Rust nem tudja kitalálni, hogy az
`Animal::baby_name` melyik megvalósítását szeretnénk. Ezt a fordítási hibát
kapjuk:

```console
{{#include ../listings/ch20-advanced-features/listing-20-21/output.txt}}
```

Ahhoz, hogy egyértelművé tegyük, és megmondjuk a Rustnak, hogy az `Animal`
`Dog`-ra vonatkozó megvalósítását szeretnénk használni, nem pedig az `Animal`
valamely más típusra vonatkozó megvalósítását, teljesen minősített szintaxist
kell használnunk. A 20-22. kódrészlet bemutatja,
hogyan használhatjuk a teljesen minősített szintaxist.

<Listing number="20-22" file-name="src/main.rs" caption="Teljesen minősített szintaxis annak megadására, hogy az `Animal` trait `Dog`-on megvalósított `baby_name` függvényét szeretnénk meghívni">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-22/src/main.rs:here}}
```

</Listing>

A kacsacsőrök között típusannotációt adunk a Rustnak, amely jelzi, hogy az
`Animal` trait `Dog`-on megvalósított `baby_name` metódusát szeretnénk
meghívni: azt mondjuk, hogy ennél a függvényhívásnál a `Dog` típust
`Animal`-ként szeretnénk kezelni. Ez a kód most már azt írja ki, amit
szeretnénk:

```console
{{#include ../listings/ch20-advanced-features/listing-20-22/output.txt}}
```

Általánosságban a teljesen minősített szintaxis a következőképpen néz ki:

```rust,ignore
<Type as Trait>::function(receiver_if_method, next_arg, ...);
```

A nem metódus jellegű társított függvényeknél nincs `receiver`: csak a többi
argumentum listája szerepel. A teljesen minősített szintaxist mindenhol
használhatnád, ahol függvényt vagy metódust hívsz. Elhagyhatod azonban a
szintaxis bármely részét, amelyet a Rust a program más információiból ki tud
találni. Erre a bőbeszédűbb szintaxisra csak olyan esetekben van szükség,
amikor több megvalósítás is ugyanazt a nevet használja, és a Rustnak segítség
kell ahhoz, hogy azonosítsa, melyik megvalósítást szeretnéd meghívni.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-supertraits-to-require-one-traits-functionality-within-another-trait"></a>

### Szupertraitek használata {#using-supertraits}

Előfordulhat, hogy olyan traitdefiníciót írsz, amely egy másik traittől függ:
ahhoz, hogy egy típus megvalósítsa az első traitet, meg szeretnéd követelni,
hogy a második traitet is megvalósítsa. Ezt azért tennéd, hogy a
traitdefiníciód használhassa a második trait társított elemeit. Azt a traitet,
amelyre a traitdefiníciód támaszkodik, a traited _szupertraitjének
(supertrait)_ nevezzük.

Tegyük fel például, hogy egy `OutlinePrint` traitet szeretnénk készíteni egy
`outline_print` metódussal, amely egy adott értéket csillagokból álló keretbe
foglalva ír ki. Vagyis ha van egy `Point` struktúránk, amely úgy valósítja meg a
standard könyvtár `Display` traitjét, hogy az eredmény `(x, y)` legyen, akkor
egy olyan `Point` példányon meghívva az `outline_print`-et, amelynek `x`
értéke `1`, `y` értéke pedig `3`, a következőt kell kiírnia:

```text
**********
*        *
* (1, 3) *
*        *
**********
```

Az `outline_print` metódus megvalósításában a `Display` trait funkcionalitását
szeretnénk használni. Ezért meg kell adnunk, hogy az `OutlinePrint` trait csak
olyan típusokkal működik, amelyek a `Display`-t is megvalósítják, és így
biztosítják az `OutlinePrint` számára szükséges funkcionalitást. Ezt a
traitdefinícióban az `OutlinePrint: Display` megadásával tehetjük meg. Ez a
technika ahhoz hasonló, mintha trait-korlátot adnánk a traithez. A 20-23.
kódrészlet az `OutlinePrint` trait egy megvalósítását mutatja.

<Listing number="20-23" file-name="src/main.rs" caption="Az `OutlinePrint` trait megvalósítása, amely a `Display` funkcionalitását igényli">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-23/src/main.rs:here}}
```

</Listing>

Mivel megadtuk, hogy az `OutlinePrint` igényli a `Display` traitet,
használhatjuk a `to_string` függvényt, amely automatikusan meg van valósítva
minden olyan típusra, amely megvalósítja a `Display`-t. Ha úgy próbálnánk
használni a `to_string`-et, hogy nem írunk kettőspontot és `Display` traitet a
trait neve után, olyan hibát kapnánk, amely szerint az aktuális hatókörben a
`&Self` típuson nem található `to_string` nevű metódus.

Nézzük meg, mi történik, ha egy olyan típuson próbáljuk megvalósítani az
`OutlinePrint`-et, amely nem valósítja meg a `Display`-t, például a `Point`
struktúrán:

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-02-impl-outlineprint-for-point/src/main.rs:here}}
```

</Listing>

Olyan hibát kapunk, amely szerint a `Display` szükséges, de nincs
megvalósítva:

```console
{{#include ../listings/ch20-advanced-features/no-listing-02-impl-outlineprint-for-point/output.txt}}
```

A javításhoz megvalósítjuk a `Display`-t a `Point`-on, és így teljesítjük az
`OutlinePrint` által megkövetelt megkötést:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-03-impl-display-for-point/src/main.rs:here}}
```

</Listing>

Ezután az `OutlinePrint` trait megvalósítása a `Point`-on sikeresen lefordul,
és egy `Point` példányon meghívhatjuk az `outline_print`-et, hogy csillagokból
álló keretben jelenítsük meg.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-the-newtype-pattern-to-implement-external-traits-on-external-types"></a>
<a id="using-the-newtype-pattern-to-implement-external-traits"></a>

### Külső traitek megvalósítása a newtype mintával {#implementing-external-traits-with-the-newtype-pattern}

A 10. fejezet [„Trait megvalósítása egy
típuson”][implementing-a-trait-on-a-type]<!-- ignore --> szakaszában
említettük az árvaszabályt, amely szerint egy traitet csak akkor valósíthatunk
meg egy típuson, ha a trait vagy a típus – vagy mindkettő – a saját
crate-ünkben van definiálva. Ezt a korlátozást a newtype mintával
megkerülhetjük, amelynek lényege, hogy egy tuple struktúrában új típust hozunk
létre. (A tuple struktúrákról az 5. fejezet [„Különböző típusok létrehozása
tuple struktúrákkal”][tuple-structs]<!-- ignore --> szakaszában volt szó.) A
tuple struktúrának egyetlen mezője lesz, és vékony burkolóként szolgál afölött
a típus fölött, amelyre a traitet meg szeretnénk valósítani. A burkoló típus
így a saját crate-ünkben van definiálva, és megvalósíthatjuk rajta a traitet. A
_newtype_ kifejezés a Haskell programozási nyelvből származik. A minta
használata nem jár futásidejű teljesítményveszteséggel, a burkoló típus
fordítási időben eltűnik.

Tegyük fel például, hogy a `Display`-t szeretnénk megvalósítani a `Vec<T>`-n,
amit az árvaszabály közvetlenül nem enged meg, mert a `Display` trait és a
`Vec<T>` típus is a crate-ünkön kívül van definiálva. Létrehozhatunk egy
`Wrapper` struktúrát, amely egy `Vec<T>` példányt tartalmaz; ezután a
`Display`-t a `Wrapper`-en valósíthatjuk meg, és felhasználhatjuk a `Vec<T>`
értéket, ahogy a 20-24. kódrészlet mutatja.

<Listing number="20-24" file-name="src/main.rs" caption="Egy `Vec<String>` köré épített `Wrapper` típus létrehozása a `Display` megvalósításához">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-24/src/main.rs}}
```

</Listing>

A `Display` megvalósítása a `self.0` segítségével éri el a belső `Vec<T>`-t,
mert a `Wrapper` tuple struktúra, és a `Vec<T>` a tuple 0. indexű eleme.
Ezután a `Display` trait funkcionalitását használhatjuk a `Wrapper`-en.

Ennek a technikának a hátránya, hogy a `Wrapper` új típus, így nincsenek meg
rajta a benne tárolt érték metódusai. A `Vec<T>` összes metódusát közvetlenül
a `Wrapper`-en kellene megvalósítanunk úgy, hogy a metódusok a `self.0`-ra
delegáljanak, és így a `Wrapper`-t pontosan úgy kezelhetnénk, mint egy
`Vec<T>`-t. Ha azt szeretnénk, hogy az új típusnak a belső típus összes
metódusa meglegyen, megoldás lehet a `Deref` trait megvalósítása a
`Wrapper`-en úgy, hogy a belső típust adja vissza (a `Deref` trait
megvalósításáról a 15. fejezet [„Okos mutatók kezelése hagyományos
referenciaként”][smart-pointer-deref]<!-- ignore --> szakaszában volt szó).
Ha nem szeretnénk, hogy a `Wrapper` típusnak a belső típus összes metódusa
meglegyen – például azért, hogy korlátozzuk a `Wrapper` típus viselkedését –,
akkor csak a ténylegesen kívánt metódusokat kellene kézzel megvalósítanunk.

Ez a newtype minta akkor is hasznos, ha nem traitekről van szó. Váltsunk
témát, és nézzünk meg néhány haladó módszert a Rust típusrendszerének
használatára.

[newtype]: ch20-02-advanced-traits.html#implementing-external-traits-with-the-newtype-pattern
[implementing-a-trait-on-a-type]: ch10-02-traits.html#implementing-a-trait-on-a-type
[traits]: ch10-02-traits.html
[smart-pointer-deref]: ch15-02-deref.html#treating-smart-pointers-like-regular-references
[tuple-structs]: ch05-01-defining-structs.html#creating-different-types-with-tuple-structs
