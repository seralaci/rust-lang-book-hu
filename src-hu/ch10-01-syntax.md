## Generikus adattípusok {#generic-data-types}

A generikus típusokkal olyan elemekhez készíthetünk definíciót, mint a
függvényszignatúrák vagy a struktúrák, amelyeket aztán sokféle konkrét
adattípussal használhatunk. Először nézzük meg, hogyan definiálhatunk
függvényeket, struktúrákat, enumokat és metódusokat generikus típusokkal.
Ezután arról lesz szó, hogyan hatnak a generikus típusok a kód teljesítményére.

### Függvénydefiníciókban {#in-function-definitions}

Ha olyan függvényt definiálunk, amely generikus típusokat használ, a generikus
típusokat a függvény szignatúrájában arra a helyre írjuk, ahol egyébként a
paraméterek és a visszatérési érték adattípusát adnánk meg. Így a kódunk
rugalmasabb lesz, és több funkciót kínál a függvényünk hívóinak, miközben
elkerüljük a kódismétlést.

A `largest` függvénynél folytatva a 10-4. kódrészlet két függvényt mutat,
amelyek mindegyike egy szelet legnagyobb értékét keresi meg. Ezeket aztán
egyetlen, generikus típusokat használó függvénnyé vonjuk össze.

<Listing number="10-4" file-name="src/main.rs" caption="Két függvény, amelyek csak a nevükben és a szignatúrájukban szereplő típusokban különböznek">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-04/src/main.rs:here}}
```

</Listing>

A `largest_i32` függvény az, amelyet a 10-3. kódrészletben emeltünk ki, és
amely egy szelet legnagyobb `i32` értékét keresi meg. A `largest_char` függvény
egy szelet legnagyobb `char` értékét keresi meg. A két függvénytörzs kódja
azonos, ezért szüntessük meg az ismétlődést úgy, hogy egyetlen függvényben egy
generikus típusparamétert vezetünk be.

Ahhoz, hogy egy új, egyetlen függvényben paraméterezzük a típusokat, nevet kell
adnunk a típusparaméternek, ahogy a függvény értékparamétereinek is. A
típusparaméter neve bármilyen azonosító lehet. Mi mégis a `T`-t használjuk,
mert megállapodás szerint a Rustban a típusparaméterek neve rövid, gyakran
csak egyetlen betű, a Rust típuselnevezési konvenciója pedig az UpperCamelCase.
A _type_ (típus) szó rövidítéseként a `T` a legtöbb Rust-programozó
alapértelmezett választása.

Ha egy paramétert használunk a függvény törzsében, a paraméter nevét
deklarálnunk kell a szignatúrában, hogy a fordító tudja, mit jelent ez a név.
Ehhez hasonlóan, ha egy típusparaméter nevét használjuk a függvény
szignatúrájában, a típusparaméter nevét deklarálnunk kell, mielőtt
használnánk. A generikus `largest` függvény definiálásához a típusnevek
deklarációját csúcsos zárójelek, `<>` közé tesszük, a függvény neve és a
paraméterlista közé, így:

```rust,ignore
fn largest<T>(list: &[T]) -> &T {
```

Ezt a definíciót így olvassuk: „A `largest` függvény generikus valamilyen `T`
típusra nézve.” A függvénynek egy `list` nevű paramétere van, amely `T` típusú
értékek szelete. A `largest` függvény egy ugyanilyen `T` típusú értékre mutató
referenciát ad vissza.

A 10-5. kódrészlet az összevont `largest` függvény definícióját mutatja, amely
a szignatúrájában a generikus adattípust használja. A kódrészlet azt is
megmutatja, hogyan hívhatjuk meg a függvényt akár `i32`, akár `char` értékek
szeletével. Figyelj arra, hogy ez a kód még nem fordul le.

<Listing number="10-5" file-name="src/main.rs" caption="A generikus típusparamétereket használó `largest` függvény; ez még nem fordul le">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-05/src/main.rs}}
```

</Listing>

Ha most lefordítjuk ezt a kódot, ezt a hibát kapjuk:

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-05/output.txt}}
```

A súgószöveg megemlíti a `std::cmp::PartialOrd`-ot, amely egy trait; a
traitekről a következő szakaszban lesz szó. Egyelőre elég annyit tudnod, hogy
ez a hiba azt mondja: a `largest` törzse nem fog működni minden lehetséges
típusra, amely a `T` helyén állhat. Mivel a törzsben `T` típusú értékeket
akarunk összehasonlítani, csak olyan típusokat használhatunk, amelyek értékei
sorba rendezhetők. Az összehasonlítás lehetővé tételére a standard könyvtárban
ott van a `std::cmp::PartialOrd` trait, amelyet típusokra megvalósíthatsz
(erről a traitről bővebben a C. függelékben olvashatsz). A 10-5. kódrészlet
javításához követhetjük a súgószöveg javaslatát, és a `T` helyén érvényes
típusokat azokra korlátozhatjuk, amelyek megvalósítják a `PartialOrd`-ot. A
kódrészlet ekkor lefordul, mert a standard könyvtár az `i32`-re és a `char`-ra
is megvalósítja a `PartialOrd`-ot.

### Struktúradefiníciókban {#in-struct-definitions}

A `<>` szintaxissal olyan struktúrákat is definiálhatunk, amelyek egy vagy több
mezőjükben generikus típusparamétert használnak. A 10-6. kódrészlet egy
`Point<T>` struktúrát definiál, amely tetszőleges típusú `x` és `y`
koordinátaértékeket tárol.

<Listing number="10-6" file-name="src/main.rs" caption="Egy `Point<T>` struktúra, amely `T` típusú `x` és `y` értékeket tárol">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-06/src/main.rs}}
```

</Listing>

A generikus típusok szintaxisa a struktúradefiníciókban hasonló a
függvénydefiníciókban használthoz. Először a struktúra neve után csúcsos
zárójelek között deklaráljuk a típusparaméter nevét. Ezután a generikus típust
a struktúradefinícióban ott használjuk, ahol egyébként konkrét adattípusokat
adnánk meg.

Figyeld meg, hogy mivel a `Point<T>` definiálásához csak egyetlen generikus
típust használtunk, ez a definíció azt mondja, hogy a `Point<T>` struktúra
generikus valamilyen `T` típusra nézve, és az `x` és az `y` mező _mindkettő_
ugyanilyen típusú, bármi legyen is ez a típus. Ha a `Point<T>` egy olyan
példányát hozzuk létre, amelynek különböző típusú értékei vannak, ahogy a
10-7. kódrészletben, a kódunk nem fordul le.

<Listing number="10-7" file-name="src/main.rs" caption="Az `x` és az `y` mezőnek azonos típusúnak kell lennie, mert mindkettő ugyanazt a `T` generikus adattípust használja.">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-07/src/main.rs}}
```

</Listing>

Ebben a példában, amikor az `x`-nek az `5` egész értéket adjuk, tudatjuk a
fordítóval, hogy a `T` generikus típus a `Point<T>` ezen példányában egész
szám lesz. Amikor aztán az `y`-nak `4.0`-t adunk meg, amelyet az `x`-szel
azonos típusúnak definiáltunk, a következőhöz hasonló típuseltérési hibát
kapunk:

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-07/output.txt}}
```

Ha olyan `Point` struktúrát akarunk definiálni, amelyben az `x` és az `y`
egyaránt generikus, de különböző típusú is lehet, több generikus
típusparamétert használhatunk. A 10-8. kódrészletben például úgy módosítjuk a
`Point` definícióját, hogy a `T` és az `U` típusra nézve legyen generikus, ahol
az `x` `T` típusú, az `y` pedig `U` típusú.

<Listing number="10-8" file-name="src/main.rs" caption="Egy két típusra nézve generikus `Point<T, U>`, így az `x` és az `y` különböző típusú érték lehet">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-08/src/main.rs}}
```

</Listing>

Most már a `Point` összes bemutatott példánya megengedett! Egy definícióban
annyi generikus típusparamétert használhatsz, amennyit csak akarsz, de ha
néhánynál többet használsz, a kód nehezen olvashatóvá válik. Ha azt veszed
észre, hogy sok generikus típusra van szükséged a kódodban, az arra utalhat,
hogy a kódot kisebb darabokra kellene bontanod.

### Enumdefiníciókban {#in-enum-definitions}

Ahogy a struktúráknál, úgy olyan enumokat is definiálhatunk, amelyek
változatai generikus adattípusokat tárolnak. Vessünk egy újabb pillantást a
standard könyvtár `Option<T>` enumjára, amelyet a 6. fejezetben használtunk:

```rust
enum Option<T> {
    Some(T),
    None,
}
```

Ennek a definíciónak most már több értelme lehet számodra. Ahogy látod, az
`Option<T>` enum generikus a `T` típusra nézve, és két változata van: a `Some`,
amely egy `T` típusú értéket tárol, és a `None` változat, amely semmilyen
értéket nem tárol. Az `Option<T>` enummal kifejezhetjük az opcionális érték
absztrakt fogalmát, és mivel az `Option<T>` generikus, ezt az absztrakciót
használhatjuk, bármilyen típusú is az opcionális érték.

Az enumok több generikus típust is használhatnak. Erre példa a `Result` enum
definíciója, amelyet a 9. fejezetben használtunk:

```rust
enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

A `Result` enum két típusra, a `T`-re és az `E`-re nézve generikus, és két
változata van: az `Ok`, amely egy `T` típusú értéket tárol, és az `Err`, amely
egy `E` típusú értéket tárol. Ez a definíció kényelmessé teszi a `Result` enum
használatát bárhol, ahol olyan műveletünk van, amely sikerülhet (valamilyen
`T` típusú értéket ad vissza), vagy meghiúsulhat (valamilyen `E` típusú hibát
ad vissza). Valójában ezt használtuk egy fájl megnyitására a 9-3.
kódrészletben, ahol a `T` helyére a `std::fs::File` típus került, ha a fájlt
sikerült megnyitni, az `E` helyére pedig a `std::io::Error` típus, ha a fájl
megnyitása közben gond adódott.

Ha a kódodban olyan helyzeteket veszel észre, ahol több struktúra- vagy
enumdefiníció csak a tárolt értékek típusában különbözik, az ismétlődést
elkerülheted, ha helyettük generikus típusokat használsz.

### Metódusdefiníciókban {#in-method-definitions}

Struktúrákra és enumokra metódusokat valósíthatunk meg (ahogy az 5.
fejezetben tettük), és a definíciójukban generikus típusokat is használhatunk.
A 10-9. kódrészlet a 10-6. kódrészletben definiált `Point<T>` struktúrát
mutatja, amelyre egy `x` nevű metódust valósítottunk meg.

<Listing number="10-9" file-name="src/main.rs" caption="Egy `x` nevű metódus megvalósítása a `Point<T>` struktúrán, amely a `T` típusú `x` mezőre mutató referenciát ad vissza">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-09/src/main.rs}}
```

</Listing>

Itt a `Point<T>`-n definiáltunk egy `x` nevű metódust, amely az `x` mezőben
lévő adatra mutató referenciát ad vissza.

Figyeld meg, hogy a `T`-t közvetlenül az `impl` után deklarálnunk kell, hogy a
`T` segítségével megadhassuk: a `Point<T>` típusra valósítunk meg metódusokat.
Azzal, hogy a `T`-t az `impl` után generikus típusként deklaráljuk, a Rust
felismeri, hogy a `Point` csúcsos zárójelei között álló típus generikus típus,
nem pedig konkrét típus. Ennek a generikus paraméternek választhattunk volna a
struktúradefinícióban deklarált generikus paraméterétől eltérő nevet is, de
megszokott, hogy ugyanazt a nevet használjuk. Ha egy generikus típust
deklaráló `impl`-ben írsz egy metódust, az a metódus a típus bármely
példányán definiálva lesz, függetlenül attól, hogy végül melyik konkrét típus
kerül a generikus típus helyére.

A típuson definiált metódusoknál a generikus típusokra korlátozásokat is
megadhatunk. Megtehetjük például, hogy csak `Point<f32>` példányokon valósítunk
meg metódusokat, nem pedig bármilyen generikus típusú `Point<T>` példányon. A
10-10. kódrészletben a konkrét `f32` típust használjuk, vagyis az `impl` után
nem deklarálunk típusokat.

<Listing number="10-10" file-name="src/main.rs" caption="Egy `impl` blokk, amely csak arra a struktúrára vonatkozik, amelynek a `T` generikus típusparamétere egy adott konkrét típus">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-10/src/main.rs:here}}
```

</Listing>

Ez a kód azt jelenti, hogy a `Point<f32>` típusnak lesz `distance_from_origin`
metódusa; a `Point<T>` többi példányán, ahol a `T` nem `f32` típusú, ez a
metódus nem lesz definiálva. A metódus azt méri, milyen messze van a pontunk a
(0.0, 0.0) koordinátájú ponttól, és olyan matematikai műveleteket használ,
amelyek csak lebegőpontos típusokhoz érhetők el.

A struktúradefiníció generikus típusparaméterei nem mindig egyeznek meg
azokkal, amelyeket ugyanannak a struktúrának a metódusszignatúráiban
használsz. A 10-11. kódrészlet a példa érthetősége kedvéért a `Point`
struktúrához az `X1` és `Y1`, a `mixup` metódus szignatúrájához pedig az `X2`
és `Y2` generikus típusokat használja. A metódus egy új `Point` példányt hoz
létre a `self` `Point` (`X1` típusú) `x` értékével és az átadott `Point`
(`Y2` típusú) `y` értékével.

<Listing number="10-11" file-name="src/main.rs" caption="Egy metódus, amely a struktúra definíciójától eltérő generikus típusokat használ">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-11/src/main.rs}}
```

</Listing>

A `main`-ben definiáltunk egy `Point`-ot, amelynek az `x` mezője `i32` (`5`
értékkel), az `y` mezője pedig `f64` (`10.4` értékkel). A `p2` változó egy
olyan `Point` struktúra, amelynek az `x` mezője sztringszelet (`"Hello"`
értékkel), az `y` mezője pedig `char` (`c` értékkel). Ha a `p1`-en a `p2`
argumentummal meghívjuk a `mixup`-ot, a `p3`-at kapjuk, amelynek az `x` mezője
`i32` lesz, mert az `x` a `p1`-ből származik. A `p3` változó `y` mezője `char`
lesz, mert az `y` a `p2`-ből származik. A `println!` makróhívás a
`p3.x = 5, p3.y = c` szöveget írja ki.

Ennek a példának az a célja, hogy bemutasson egy olyan helyzetet, amelyben
egyes generikus paramétereket az `impl`-lel, másokat pedig a
metódusdefinícióval deklarálunk. Itt az `X1` és `Y1` generikus paramétereket az
`impl` után deklaráljuk, mert a struktúradefinícióhoz tartoznak. Az `X2` és
`Y2` generikus paramétereket az `fn mixup` után deklaráljuk, mert csak a
metódus szempontjából lényegesek.

### A generikus típusokat használó kód teljesítménye {#performance-of-code-using-generics}

Talán felmerül benned, hogy jár-e futásidejű költséggel a generikus
típusparaméterek használata. A jó hír az, hogy a generikus típusok
használatától a programod semmivel sem fut lassabban, mint konkrét típusokkal.

A Rust ezt úgy éri el, hogy fordítási időben monomorfizálja a generikus
típusokat használó kódot. A _monomorfizáció (monomorphization)_ az a folyamat,
amely a generikus kódot konkrét kóddá alakítja azáltal, hogy behelyettesíti a
fordításkor használt konkrét típusokat. Ebben a folyamatban a fordító a
fordítottját teszi annak, amit mi tettünk a 10-5. kódrészlet generikus
függvényének létrehozásakor: a fordító megnézi az összes helyet, ahol generikus
kódot hívunk meg, és kódot generál azokra a konkrét típusokra, amelyekkel a
generikus kódot meghívjuk.

Nézzük meg, hogyan működik ez a standard könyvtár generikus `Option<T>`
enumjával:

```rust
let integer = Some(5);
let float = Some(5.0);
```

Amikor a Rust lefordítja ezt a kódot, monomorfizációt végez. A folyamat során a
fordító beolvassa az `Option<T>` példányokban használt értékeket, és kétféle
`Option<T>`-t azonosít: az egyik `i32`, a másik `f64`. Ennek megfelelően az
`Option<T>` generikus definícióját két, az `i32`-re, illetve az `f64`-re
specializált definícióvá bontja ki, így a generikus definíciót a konkrétakkal
helyettesíti.

A kód monomorfizált változata nagyjából így néz ki (a fordító más neveket
használ, mint amelyeket mi itt a szemléltetés kedvéért használunk):

<Listing file-name="src/main.rs">

```rust
enum Option_i32 {
    Some(i32),
    None,
}

enum Option_f64 {
    Some(f64),
    None,
}

fn main() {
    let integer = Option_i32::Some(5);
    let float = Option_f64::Some(5.0);
}
```

</Listing>

A generikus `Option<T>` helyére a fordító által létrehozott konkrét definíciók
kerülnek. Mivel a Rust a generikus kódot olyan kóddá fordítja, amely minden
előfordulásnál megadja a típust, a generikus típusok használatáért nem fizetünk
futásidejű költséget. Futáskor a kód pontosan úgy teljesít, mintha minden
definíciót kézzel duplikáltunk volna. A monomorfizáció folyamata rendkívül
hatékonnyá teszi a Rust generikus típusait futásidőben.
