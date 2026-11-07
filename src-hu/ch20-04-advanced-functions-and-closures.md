## Haladó függvények és closure-ök {#advanced-functions-and-closures}

Ez a szakasz a függvényekkel és closure-ökkel kapcsolatos néhány haladó nyelvi
elemet mutat be, köztük a függvénymutatókat és a closure-ök visszaadását.

### Függvénymutatók {#function-pointers}

Beszéltünk már arról, hogyan adhatunk át closure-öket függvényeknek; de
szokásos függvényeket is átadhatsz függvényeknek! Ez a technika akkor hasznos,
ha egy már definiált függvényt szeretnél átadni ahelyett, hogy új closure-t
definiálnál. A függvények az `fn` típusra konvertálódnak (kis _f_-fel), amelyet
nem szabad összekeverni az `Fn` closure-traittel. Az `fn` típust
_függvénymutatónak (function pointer)_ nevezzük. Ha függvényeket
függvénymutatókkal adsz át, függvényeket használhatsz más függvények
argumentumaként.

Annak a szintaxisa, hogy egy paraméter függvénymutató, a closure-ökéhez
hasonló, ahogy a 20-28. kódrészlet mutatja, ahol egy `add_one` függvényt
definiáltunk, amely 1-et ad a paraméteréhez. A `do_twice` függvény két
paramétert kap: egy függvénymutatót bármely olyan függvényre, amely egy `i32`
paramétert kap és `i32`-t ad vissza, valamint egy `i32` értéket. A `do_twice`
függvény kétszer hívja meg az `f` függvényt, mindkétszer átadva neki az `arg`
értéket, majd összeadja a két függvényhívás eredményét. A `main` függvény a
`do_twice`-t az `add_one` és az `5` argumentummal hívja meg.

<Listing number="20-28" file-name="src/main.rs" caption="Az `fn` típus használata függvénymutató argumentumként való fogadására">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-28/src/main.rs}}
```

</Listing>

Ez a kód a `The answer is: 12` szöveget írja ki. Megadjuk, hogy a `do_twice`
`f` paramétere egy olyan `fn`, amely egy `i32` típusú paramétert kap, és
`i32`-t ad vissza. Ezután a `do_twice` törzsében meghívhatjuk az `f`-et. A
`main`-ben az `add_one` függvénynevet adhatjuk át a `do_twice` első
argumentumaként.

A closure-ökkel ellentétben az `fn` típus, nem pedig trait, így közvetlenül az
`fn`-t adjuk meg paramétertípusként, ahelyett hogy egy generikus
típusparamétert deklarálnánk valamelyik `Fn` traittel mint trait-korláttal.

A függvénymutatók mindhárom closure-traitet (`Fn`, `FnMut` és `FnOnce`)
megvalósítják, ami azt jelenti, hogy függvénymutatót mindig átadhatsz
argumentumként egy olyan függvénynek, amely closure-t vár. A legjobb, ha a
függvényeidet generikus típussal és valamelyik closure-traittel írod meg, így
a függvényeid függvényeket és closure-öket egyaránt elfogadhatnak.

Ugyanakkor van példa arra, amikor csak `fn`-t szeretnél elfogadni, closure-öket
nem: ez az olyan külső kóddal való együttműködés, amelyben nincsenek
closure-ök. A C függvények elfogadhatnak függvényeket argumentumként, de a
C-ben nincsenek closure-ök.

Példaként arra, amikor egy helyben definiált closure-t és egy névvel ellátott
függvényt is használhatsz, nézzük meg a standard könyvtár `Iterator` traitje
által biztosított `map` metódus egy használatát. Ha a `map` metódussal egy
számokat tartalmazó vektort sztringeket tartalmazó vektorrá szeretnénk
alakítani, használhatunk closure-t, ahogy a 20-29. kódrészletben.

<Listing number="20-29" caption="Closure használata a `map` metódussal számok sztringgé alakítására">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-29/src/main.rs:here}}
```

</Listing>

Vagy a closure helyett egy függvényt is megnevezhetünk a `map` argumentumaként.
A 20-30. kódrészlet mutatja, hogyan nézne ki ez.

<Listing number="20-30" caption="A `String::to_string` függvény használata a `map` metódussal számok sztringgé alakítására">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-30/src/main.rs:here}}
```

</Listing>

Vedd észre, hogy a [„Haladó traitek”][advanced-traits]<!-- ignore -->
szakaszban tárgyalt teljesen minősített szintaxist kell használnunk, mert több
`to_string` nevű függvény is elérhető.

Itt a `ToString` traitben definiált `to_string` függvényt használjuk, amelyet a
standard könyvtár minden olyan típusra megvalósított, amely megvalósítja a
`Display`-t.

Emlékezz a 6. fejezet [„Enum értékek”][enum-values]<!-- ignore -->
szakaszából, hogy minden általunk definiált enum változat neve egyben
inicializáló függvénnyé is válik. Ezeket az inicializáló függvényeket a
closure-traiteket megvalósító függvénymutatóként használhatjuk, ami azt
jelenti, hogy az inicializáló függvényeket closure-t váró metódusok
argumentumaként is megadhatjuk, ahogy a 20-31. kódrészletben látható.

<Listing number="20-31" caption="Enum inicializáló használata a `map` metódussal `Status` példányok létrehozására számokból">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-31/src/main.rs:here}}
```

</Listing>

Itt a `Status::Value` inicializáló függvényével `Status::Value` példányokat
hozunk létre minden egyes `u32` értékből abban a tartományban, amelyen a
`map`-et meghívjuk. Van, aki ezt a stílust kedveli, és van, aki inkább
closure-öket használ. Ugyanarra a kódra fordulnak le, így azt a stílust
használd, amelyik számodra világosabb.

### Closure-ök visszaadása {#returning-closures}

A closure-öket traitek reprezentálják, ami azt jelenti, hogy closure-öket nem
adhatsz vissza közvetlenül. A legtöbb esetben, amikor egy traitet szeretnél
visszaadni, ehelyett a traitet megvalósító konkrét típust használhatod a
függvény visszatérési értékeként. A closure-ökkel azonban ezt általában nem
teheted meg, mert nincs visszaadható konkrét típusuk; az `fn`
függvénymutatót például nem használhatod visszatérési típusként, ha a closure
bármilyen értéket elkap a hatóköréből.

Ehelyett általában a 10. fejezetben megismert `impl Trait` szintaxist
használod. Bármilyen függvénytípust visszaadhatsz az `Fn`, `FnOnce` és `FnMut`
segítségével. A 20-32. kódrészlet kódja például gond nélkül lefordul.

<Listing number="20-32" caption="Closure visszaadása egy függvényből az `impl Trait` szintaxissal">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-32/src/lib.rs}}
```

</Listing>

Ahogy azonban a 13. fejezet [„A closure-ök típusainak következtetése és
annotálása”][closure-types]<!-- ignore --> szakaszában megjegyeztük, minden
closure egyben saját, különálló típus is. Ha több olyan függvénnyel kell
dolgoznod, amelyeknek ugyanaz a szignatúrája, de eltér a megvalósítása, trait
objektumot kell használnod hozzájuk. Nézzük meg, mi történik, ha a 20-33.
kódrészlethez hasonló kódot írsz.

<Listing file-name="src/main.rs" number="20-33" caption="Egy `Vec<T>` létrehozása `impl Fn` típusokat visszaadó függvények által definiált closure-ökből">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-33/src/main.rs}}
```

</Listing>

Itt két függvényünk van, a `returns_closure` és a
`returns_initialized_closure`, amelyek mindketten `impl Fn(i32) -> i32`-t adnak
vissza. Vedd észre, hogy az általuk visszaadott closure-ök különbözőek, annak
ellenére, hogy ugyanazt a típust valósítják meg. Ha megpróbáljuk lefordítani,
a Rust jelzi, hogy ez nem fog működni:

```text
{{#include ../listings/ch20-advanced-features/listing-20-33/output.txt}}
```

A hibaüzenet azt mondja, hogy valahányszor `impl Trait`-et adunk vissza, a
Rust egy egyedi _átlátszatlan típust (opaque type)_ hoz létre: olyan típust,
amelynek nem láthatunk bele a részleteibe, vagyis abba, amit a Rust
létrehoz nekünk, és azt a típust sem tudjuk kitalálni, amelyet a Rust
generálni fog, hogy magunk írjuk le. Így hiába adnak vissza ezek a függvények
olyan closure-öket, amelyek ugyanazt a traitet, az `Fn(i32) -> i32`-t
valósítják meg, a Rust által mindegyikhez generált átlátszatlan típusok
különböznek. (Ez ahhoz hasonló, ahogy a Rust különböző konkrét típusokat állít
elő a különböző async blokkokhoz, még akkor is, ha ugyanaz a kimeneti típusuk,
ahogy a 17. fejezet [„A `Pin` típus és az `Unpin` trait”][future-types]<!--
ignore --> szakaszában láttuk.) Erre a problémára már néhányszor láttunk
megoldást: trait objektumot használhatunk, ahogy a 20-34. kódrészletben.

<Listing number="20-34" caption="Egy `Vec<T>` létrehozása `Box<dyn Fn>`-t visszaadó függvények által definiált closure-ökből, hogy azonos típusúak legyenek">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-34/src/main.rs:here}}
```

</Listing>

Ez a kód gond nélkül lefordul. A trait objektumokról bővebben a 18. fejezet
[„Trait objektumok használata a közös viselkedés
absztrahálására”][trait-objects]<!-- ignore --> szakaszában olvashatsz.

Következzenek a makrók!

[advanced-traits]: ch20-02-advanced-traits.html#advanced-traits
[enum-values]: ch06-01-defining-an-enum.html#enum-values
[closure-types]: ch13-01-closures.html#closure-type-inference-and-annotation
[future-types]: ch17-03-more-futures.html
[trait-objects]: ch18-02-trait-objects.html
