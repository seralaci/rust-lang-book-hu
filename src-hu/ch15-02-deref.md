<!-- Old headings. Do not remove or links may break. -->

<a id="treating-smart-pointers-like-regular-references-with-the-deref-trait"></a>
<a id="treating-smart-pointers-like-regular-references-with-deref"></a>

## Okos mutatók kezelése hagyományos referenciaként {#treating-smart-pointers-like-regular-references}

A `Deref` trait megvalósításával testre szabhatod a `*` _dereferáló operátor
(dereference operator)_ viselkedését (ezt ne keverd össze a szorzás vagy a glob
operátorral). Ha a `Deref`-et úgy valósítod meg, hogy egy okos mutatót
hagyományos referenciaként lehessen kezelni, olyan kódot írhatsz, amely
referenciákkal dolgozik, és ugyanezt a kódot okos mutatókkal is használhatod.

Először nézzük meg, hogyan működik a dereferáló operátor hagyományos
referenciákkal. Ezután megpróbálunk definiálni egy saját típust, amely a
`Box<T>`-hez hasonlóan viselkedik, és megnézzük, miért nem működik a
dereferáló operátor referenciaként az újonnan definiált típusunkon.
Megvizsgáljuk, hogyan teszi lehetővé a `Deref` trait megvalósítása, hogy az okos
mutatók a referenciákhoz hasonló módon működjenek. Végül megnézzük a Rust
_deref-konverzió (deref coercion)_ nevű funkcióját, és azt, hogyan teszi
lehetővé, hogy referenciákkal és okos mutatókkal egyaránt dolgozhassunk.

<!-- Old headings. Do not remove or links may break. -->

<a id="following-the-pointer-to-the-value-with-the-dereference-operator"></a>
<a id="following-the-pointer-to-the-value"></a>

### A referencia követése az értékig {#following-the-reference-to-the-value}

A hagyományos referencia a mutatók egy fajtája, és a mutatóra gondolhatunk úgy
is, mint egy nyílra, amely valahol máshol tárolt értékre mutat. A 15-6.
kódrészletben létrehozunk egy referenciát egy `i32` értékre, majd a dereferáló
operátorral követjük a referenciát az értékig.

<Listing number="15-6" file-name="src/main.rs" caption="A dereferáló operátor használata egy `i32` értékre mutató referencia követésére">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-06/src/main.rs}}
```

</Listing>

Az `x` változó az `5` `i32` értéket tárolja. Az `y` értékét az `x`-re mutató
referenciára állítjuk. Ellenőrizhetjük, hogy az `x` egyenlő `5`-tel. Ha
azonban az `y`-ban lévő értékről szeretnénk állítást tenni, a `*y` alakot kell
használnunk, hogy a referenciát követve eljussunk ahhoz az értékhez, amelyre
mutat (innen a _dereferálás_ elnevezés), így a fordító a tényleges értéket
tudja összehasonlítani. Miután dereferáltuk az `y`-t, hozzáférünk ahhoz az
egész értékhez, amelyre az `y` mutat, és ezt összehasonlíthatjuk az `5`-tel.

Ha ehelyett azt próbálnánk írni, hogy `assert_eq!(5, y);`, a következő
fordítási hibát kapnánk:

```console
{{#include ../listings/ch15-smart-pointers/output-only-01-comparing-to-reference/output.txt}}
```

Egy szám és egy számra mutató referencia összehasonlítása nem megengedett, mert
különböző típusúak. A dereferáló operátorral kell követnünk a referenciát
ahhoz az értékhez, amelyre mutat.

### A `Box<T>` használata referenciaként {#using-boxt-like-a-reference}

A 15-6. kódrészlet kódját átírhatjuk úgy, hogy referencia helyett `Box<T>`-t
használjon; a 15-7. kódrészletben a `Box<T>`-n használt dereferáló operátor
ugyanúgy működik, mint a 15-6. kódrészletben a referencián használt.

<Listing number="15-7" file-name="src/main.rs" caption="A dereferáló operátor használata egy `Box<i32>`-n">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-07/src/main.rs}}
```

</Listing>

A fő különbség a 15-7. és a 15-6. kódrészlet között az, hogy itt az `y`-t egy
olyan box példányára állítjuk, amely az `x` értékének egy másolatára mutat,
nem pedig egy olyan referenciára, amely az `x` értékére mutat. Az utolsó
állításban a dereferáló operátorral ugyanúgy követhetjük a box mutatóját, mint
amikor az `y` referencia volt. A következőkben egy saját box típus
definiálásával megvizsgáljuk, mi a különleges a `Box<T>`-ben, ami lehetővé
teszi számunkra a dereferáló operátor használatát.

### Saját okos mutató definiálása {#defining-our-own-smart-pointer}

Készítsünk egy, a standard könyvtár `Box<T>` típusához hasonló burkoló típust,
hogy megtapasztaljuk, miben viselkednek az okos mutatótípusok alapértelmezés
szerint másként, mint a referenciák. Ezután megnézzük, hogyan adhatjuk hozzá a
dereferáló operátor használatának képességét.

> Megjegyzés: Van egy nagy különbség az általunk készítendő `MyBox<T>` típus és
> a valódi `Box<T>` között: a mi változatunk nem a kupacon tárolja az adatait.
> Ebben a példában a `Deref`-re összpontosítunk, így az, hogy az adat
> ténylegesen hol tárolódik, kevésbé fontos, mint a mutatószerű viselkedés.

A `Box<T>` típus végső soron egy egyelemű tuple struktúraként van definiálva,
ezért a 15-8. kódrészlet ugyanígy definiál egy `MyBox<T>` típust. Definiálunk
egy `new` függvényt is, amely a `Box<T>`-n definiált `new` függvénynek felel
meg.

<Listing number="15-8" file-name="src/main.rs" caption="Egy `MyBox<T>` típus definiálása">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-08/src/main.rs:here}}
```

</Listing>

Definiálunk egy `MyBox` nevű struktúrát, és deklarálunk egy `T` generikus
paramétert, mert azt szeretnénk, hogy a típusunk bármilyen típusú értéket
tárolhasson. A `MyBox` típus egy tuple struktúra, amelynek egyetlen, `T` típusú
eleme van. A `MyBox::new` függvény egy `T` típusú paramétert vár, és egy olyan
`MyBox` példányt ad vissza, amely az átadott értéket tárolja.

Próbáljuk meg a 15-7. kódrészlet `main` függvényét hozzáadni a 15-8.
kódrészlethez, és módosítsuk úgy, hogy a `Box<T>` helyett az általunk
definiált `MyBox<T>` típust használja. A 15-9. kódrészlet kódja nem fordul le,
mert a Rust nem tudja, hogyan dereferálja a `MyBox`-ot.

<Listing number="15-9" file-name="src/main.rs" caption="Kísérlet a `MyBox<T>` használatára ugyanúgy, ahogy a referenciákat és a `Box<T>`-t használtuk">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-09/src/main.rs:here}}
```

</Listing>

Ez az eredményül kapott fordítási hiba:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-09/output.txt}}
```

A `MyBox<T>` típusunk nem dereferálható, mert ezt a képességet nem valósítottuk
meg a típusunkon. Ahhoz, hogy a `*` operátorral dereferálni lehessen,
megvalósítjuk a `Deref` traitet.

<!-- Old headings. Do not remove or links may break. -->

<a id="treating-a-type-like-a-reference-by-implementing-the-deref-trait"></a>

### A `Deref` trait megvalósítása {#implementing-the-deref-trait}

Ahogy a 10. fejezet [„Trait megvalósítása egy
típuson”][impl-trait]<!-- ignore --> részében tárgyaltuk, egy trait
megvalósításához meg kell adnunk a trait kötelező metódusainak megvalósítását.
A standard könyvtár által biztosított `Deref` trait egyetlen, `deref` nevű
metódus megvalósítását követeli meg, amely kölcsönveszi a `self`-et, és a belső
adatra mutató referenciát ad vissza. A 15-10. kódrészlet a `Deref` egy
megvalósítását tartalmazza, amelyet a `MyBox<T>` definíciójához adunk hozzá.

<Listing number="15-10" file-name="src/main.rs" caption="A `Deref` megvalósítása a `MyBox<T>`-n">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-10/src/main.rs:here}}
```

</Listing>

A `type Target = T;` szintaxis egy társított típust (associated type) definiál,
amelyet a `Deref` trait használ. A társított típusok a generikus paraméterek
deklarálásának egy kissé eltérő módját jelentik, de ezek miatt most nem kell
aggódnod; a 20. fejezetben részletesebben foglalkozunk velük.

A `deref` metódus törzsét a `&self.0` kifejezéssel töltjük ki, így a `deref`
egy olyan értékre mutató referenciát ad vissza, amelyhez a `*` operátorral
szeretnénk hozzáférni; idézd fel az 5. fejezet [„Különböző típusok létrehozása
tuple struktúrákkal”][tuple-structs]<!-- ignore --> részéből, hogy a `.0` egy
tuple struktúra első értékéhez fér hozzá. A 15-9. kódrészlet `main` függvénye,
amely a `*`-ot a `MyBox<T>` értéken hívja meg, most már lefordul, és az
állítások teljesülnek!

A `Deref` trait nélkül a fordító csak `&` referenciákat tud dereferálni. A
`deref` metódus lehetővé teszi a fordító számára, hogy bármely olyan típusú
értéket vegyen, amely megvalósítja a `Deref`-et, és meghívja rajta a `deref`
metódust, hogy olyan referenciát kapjon, amelyet tud dereferálni.

Amikor a 15-9. kódrészletben a `*y` kifejezést írtuk, a Rust a háttérben
valójában ezt a kódot futtatta:

```rust,ignore
*(y.deref())
```

A Rust a `*` operátort a `deref` metódus hívására, majd egy egyszerű
dereferálásra cseréli, így nem kell azon gondolkodnunk, hogy meg kell-e hívnunk
a `deref` metódust. A Rustnak ez a funkciója lehetővé teszi, hogy olyan kódot
írjunk, amely ugyanúgy működik, akár hagyományos referenciánk van, akár egy
olyan típusunk, amely megvalósítja a `Deref`-et.

Az, hogy a `deref` metódus egy értékre mutató referenciát ad vissza, és hogy a
`*(y.deref())` kifejezésben a zárójeleken kívüli egyszerű dereferálásra továbbra
is szükség van, a tulajdonjogi rendszerrel függ össze. Ha a `deref` metódus az
értékre mutató referencia helyett közvetlenül az értéket adná vissza, az érték
kimozgatódna a `self`-ből. Sem ebben az esetben, sem a legtöbb olyan esetben,
amikor a dereferáló operátort használjuk, nem akarjuk átvenni a `MyBox<T>`-n
belüli érték tulajdonjogát.

Figyeld meg, hogy a `*` operátor minden alkalommal, amikor a kódunkban `*`-ot
használunk, csak egyszer cserélődik le a `deref` metódus hívására, majd a `*`
operátor egyszeri hívására. Mivel a `*` operátor helyettesítése nem rekurzív a
végtelenségig, végül `i32` típusú adatot kapunk, amely megfelel a 15-9.
kódrészletben az `assert_eq!`-ben szereplő `5`-nek.

<!-- Old headings. Do not remove or links may break. -->

<a id="implicit-deref-coercions-with-functions-and-methods"></a>
<a id="using-deref-coercions-in-functions-and-methods"></a>

### A deref-konverzió használata függvényekben és metódusokban {#using-deref-coercion-in-functions-and-methods}

A _deref-konverzió (deref coercion)_ egy olyan típusra mutató referenciát,
amely megvalósítja a `Deref` traitet, egy másik típusra mutató referenciává
alakít. A deref-konverzió például a `&String`-et `&str`-ré tudja alakítani,
mert a `String` úgy valósítja meg a `Deref` traitet, hogy az `&str`-t ad
vissza. A deref-konverzió egy kényelmi szolgáltatás, amelyet a Rust a
függvények és metódusok argumentumain végez el, és csak olyan típusokon
működik, amelyek megvalósítják a `Deref` traitet. Automatikusan megtörténik,
amikor egy adott típusú értékre mutató referenciát olyan függvénynek vagy
metódusnak adunk át argumentumként, amelynek a definíciójában szereplő
paramétertípus nem egyezik vele. A `deref` metódus egymást követő hívásai az
általunk megadott típust a paraméter által várt típussá alakítják.

A deref-konverziót azért adták hozzá a Rusthoz, hogy a függvény- és
metódushívásokat író programozóknak ne kelljen olyan sok explicit referenciát
és dereferálást hozzáadniuk a `&` és a `*` segítségével. A deref-konverzió
emellett lehetővé teszi, hogy több olyan kódot írjunk, amely referenciákkal és
okos mutatókkal egyaránt működik.

Hogy lássuk a deref-konverziót működés közben, használjuk a 15-8.
kódrészletben definiált `MyBox<T>` típust, valamint a 15-10. kódrészletben
hozzáadott `Deref`-megvalósítást. A 15-11. kódrészlet egy olyan függvény
definícióját mutatja, amelynek sztringszelet paramétere van.

<Listing number="15-11" file-name="src/main.rs" caption="Egy `hello` függvény, amelynek `name` paramétere `&str` típusú">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-11/src/main.rs:here}}
```

</Listing>

A `hello` függvényt meghívhatjuk egy sztringszelet argumentummal, például így:
`hello("Rust");`. A deref-konverzió lehetővé teszi, hogy a `hello`-t egy
`MyBox<String>` típusú értékre mutató referenciával hívjuk meg, ahogy a 15-12.
kódrészlet mutatja.

<Listing number="15-12" file-name="src/main.rs" caption="A `hello` meghívása egy `MyBox<String>` értékre mutató referenciával, ami a deref-konverzió miatt működik">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-12/src/main.rs:here}}
```

</Listing>

Itt a `hello` függvényt az `&m` argumentummal hívjuk meg, amely egy
`MyBox<String>` értékre mutató referencia. Mivel a 15-10. kódrészletben
megvalósítottuk a `Deref` traitet a `MyBox<T>`-n, a Rust a `deref`
meghívásával `&MyBox<String>`-ből `&String`-et tud csinálni. A standard
könyvtár biztosítja a `Deref` egy olyan megvalósítását a `String`-en, amely
sztringszeletet ad vissza; ez szerepel a `Deref` API-dokumentációjában. A Rust
ismét meghívja a `deref`-et, hogy a `&String`-ből `&str` legyen, ami már
megfelel a `hello` függvény definíciójának.

Ha a Rust nem valósítaná meg a deref-konverziót, a 15-12. kódrészlet kódja
helyett a 15-13. kódrészletben látható kódot kellene írnunk ahhoz, hogy a
`hello`-t egy `&MyBox<String>` típusú értékkel hívjuk meg.

<Listing number="15-13" file-name="src/main.rs" caption="A kód, amelyet akkor kellene írnunk, ha a Rustban nem lenne deref-konverzió">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-13/src/main.rs:here}}
```

</Listing>

A `(*m)` a `MyBox<String>`-et `String`-gé dereferálja. Ezután a `&` és a `[..]`
a `String`-ből egy olyan sztringszeletet képez, amely a teljes sztringgel
egyenlő, hogy megfeleljen a `hello` szignatúrájának. Deref-konverzió nélkül
ezt a kódot a sok szimbólum miatt nehezebb olvasni, írni és megérteni. A
deref-konverzió lehetővé teszi, hogy a Rust automatikusan elvégezze helyettünk
ezeket az átalakításokat.

Ha az érintett típusokra definiálva van a `Deref` trait, a Rust elemzi a
típusokat, és annyiszor alkalmazza a `Deref::deref`-et, ahányszor szükséges
ahhoz, hogy a paraméter típusának megfelelő referenciát kapjon. Az, hogy a
`Deref::deref`-et hányszor kell beszúrni, fordítási időben dől el, így a
deref-konverzió kihasználásának nincs futásidejű költsége!

<!-- Old headings. Do not remove or links may break. -->

<a id="how-deref-coercion-interacts-with-mutability"></a>

### A deref-konverzió módosítható referenciák esetén {#handling-deref-coercion-with-mutable-references}

Ahhoz hasonlóan, ahogy a `Deref` traittel felülírhatod a `*` operátort nem
módosítható referenciákon, a `DerefMut` traittel felülírhatod a `*` operátort
módosítható referenciákon.

A Rust három esetben végez deref-konverziót, amikor típusokat és
trait-megvalósításokat talál:

1. `&T`-ről `&U`-ra, ha `T: Deref<Target=U>`
2. `&mut T`-ről `&mut U`-ra, ha `T: DerefMut<Target=U>`
3. `&mut T`-ről `&U`-ra, ha `T: Deref<Target=U>`

Az első két eset ugyanaz, azzal a különbséggel, hogy a második módosíthatóságot
is megvalósít. Az első eset azt mondja ki, hogy ha van egy `&T`-d, és a `T`
valamilyen `U` típusra valósítja meg a `Deref`-et, akkor átlátszóan kaphatsz
egy `&U`-t. A második eset azt mondja ki, hogy ugyanez a deref-konverzió
módosítható referenciák esetén is megtörténik.

A harmadik eset trükkösebb: a Rust egy módosítható referenciát nem
módosíthatóvá is konvertál. A fordítottja azonban _nem_ lehetséges: a nem
módosítható referenciák soha nem konvertálódnak módosítható referenciává. A
kölcsönzési szabályok miatt ha van egy módosítható referenciád, annak az adatra
mutató egyetlen referenciának kell lennie (különben a program nem fordulna le).
Egy módosítható referencia átalakítása egy nem módosítható referenciává soha
nem sérti a kölcsönzési szabályokat. Egy nem módosítható referencia
módosíthatóvá alakításához az kellene, hogy a kiinduló nem módosítható
referencia legyen az adatra mutató egyetlen nem módosítható referencia, ezt
azonban a kölcsönzési szabályok nem garantálják. Ezért a Rust nem
feltételezheti, hogy egy nem módosítható referencia módosíthatóvá alakítása
lehetséges.

[impl-trait]: ch10-02-traits.html#implementing-a-trait-on-a-type
[tuple-structs]: ch05-01-defining-structs.html#creating-different-types-with-tuple-structs
