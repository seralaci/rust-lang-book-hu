## Kód futtatása felszabadításkor a `Drop` traittel {#running-code-on-cleanup-with-the-drop-trait}

Az okos mutató minta szempontjából fontos második trait a `Drop`, amellyel
testre szabhatod, mi történjen, amikor egy érték éppen kikerülni készül a
hatókörből. A `Drop` trait megvalósítását bármely típuson megadhatod, és ezzel
a kóddal olyan erőforrásokat szabadíthatsz fel, mint a fájlok vagy a hálózati
kapcsolatok.

Azért az okos mutatók kapcsán mutatjuk be a `Drop`-ot, mert a `Drop` trait
funkcionalitását szinte mindig használjuk, amikor okos mutatót valósítunk meg.
Amikor például egy `Box<T>`-t eldobunk, az felszabadítja a kupacon azt a
területet, amelyre a box mutat.

Egyes nyelvekben bizonyos típusoknál a programozónak minden alkalommal meg kell
hívnia a memóriát vagy az erőforrásokat felszabadító kódot, amikor befejezte az
adott típus egy példányának használatát. Ilyenek például a fájlleírók, a
socketek és a zárak. Ha a programozó ezt elfelejti, a rendszer túlterhelődhet
és összeomolhat. A Rustban megadhatod, hogy egy bizonyos kódrészlet fusson le,
valahányszor egy érték kikerül a hatókörből, és a fordító ezt a kódot
automatikusan beilleszti. Így nem kell ügyelned arra, hogy a program minden
olyan pontjára felszabadító kódot helyezz, ahol egy adott típus egy példányára
már nincs szükség – mégsem fogsz erőforrásokat elszivárogtatni!

Azt a kódot, amelynek akkor kell lefutnia, amikor egy érték kikerül a
hatókörből, a `Drop` trait megvalósításával adod meg. A `Drop` trait egyetlen,
`drop` nevű metódus megvalósítását követeli meg, amely egy `self`-re mutató
módosítható referenciát vár. Hogy lássuk, mikor hívja meg a Rust a `drop`-ot,
egyelőre `println!` utasításokkal valósítjuk meg a `drop`-ot.

A 15-14. kódrészlet egy `CustomSmartPointer` struktúrát mutat, amelynek
egyetlen egyedi funkciója, hogy kiírja a `Dropping CustomSmartPointer!`
szöveget, amikor a példány kikerül a hatókörből; így látható, mikor futtatja a
Rust a `drop` metódust.

<Listing number="15-14" file-name="src/main.rs" caption="Egy `CustomSmartPointer` struktúra, amely megvalósítja a `Drop` traitet, ahová a felszabadító kódunkat tennénk">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-14/src/main.rs}}
```

</Listing>

A `Drop` trait benne van a prelude-ban, így nem kell hatókörbe hoznunk. A
`CustomSmartPointer`-en megvalósítjuk a `Drop` traitet, és megadjuk a `drop`
metódus egy olyan megvalósítását, amely meghívja a `println!`-t. A `drop`
metódus törzsébe kerülne minden olyan logika, amelyet akkor szeretnél futtatni,
amikor a típusod egy példánya kikerül a hatókörből. Itt egy szöveget írunk ki,
hogy szemléletesen megmutassuk, mikor hívja meg a Rust a `drop`-ot.

A `main`-ben létrehozunk két `CustomSmartPointer` példányt, majd kiírjuk a
`CustomSmartPointers created` szöveget. A `main` végén a `CustomSmartPointer`
példányaink kikerülnek a hatókörből, és a Rust meghívja a `drop` metódusba
írt kódot, amely kiírja az utolsó üzenetünket. Figyeld meg, hogy a `drop`
metódust nem kellett explicit módon meghívnunk.

A program futtatásakor a következő kimenetet látjuk:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-14/output.txt}}
```

A Rust automatikusan meghívta helyettünk a `drop`-ot, amikor a példányaink
kikerültek a hatókörből, és lefuttatta az általunk megadott kódot. A változók a
létrehozásukkal ellentétes sorrendben kerülnek eldobásra, így a `d` a `c` előtt
lett eldobva. A példa célja, hogy szemléletesen megmutassa, hogyan működik a
`drop` metódus; általában egy kiírt üzenet helyett azt a felszabadító kódot
adnád meg, amelyet a típusodnak futtatnia kell.

<!-- Old headings. Do not remove or links may break. -->

<a id="dropping-a-value-early-with-std-mem-drop"></a>

Sajnos az automatikus `drop` funkciót nem egyszerű kikapcsolni. A `drop`
kikapcsolására általában nincs is szükség; a `Drop` trait lényege éppen az, hogy
mindez automatikusan történik. Időnként azonban előfordulhat, hogy egy értéket
korábban szeretnél felszabadítani. Ilyen eset például, amikor zárakat kezelő
okos mutatókat használsz: érdemes lehet kikényszeríteni a zárat elengedő `drop`
metódus lefutását, hogy az ugyanabban a hatókörben lévő más kód megszerezhesse
a zárat. A Rust nem engedi, hogy a `Drop` trait `drop` metódusát kézzel hívd
meg; ehelyett a standard könyvtár által biztosított `std::mem::drop` függvényt
kell meghívnod, ha ki akarod kényszeríteni egy érték eldobását a hatóköre vége
előtt.

Ha a 15-14. kódrészlet `main` függvényének módosításával megpróbáljuk kézzel
meghívni a `Drop` trait `drop` metódusát, az nem fog működni, ahogy a 15-15.
kódrészlet mutatja.

<Listing number="15-15" file-name="src/main.rs" caption="Kísérlet a `Drop` trait `drop` metódusának kézi meghívására a korai felszabadítás érdekében">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-15/src/main.rs:here}}
```

</Listing>

Amikor megpróbáljuk lefordítani ezt a kódot, a következő hibát kapjuk:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-15/output.txt}}
```

A hibaüzenet azt mondja ki, hogy a `drop`-ot nem hívhatjuk meg explicit módon.
A hibaüzenet a _destruktor (destructor)_ kifejezést használja, amely a
programozásban általánosan egy példányt felszámoló függvényt jelent. A
_destruktor_ a példányt létrehozó _konstruktor (constructor)_ párja. A Rustban
a `drop` függvény egy konkrét destruktor.

A Rust nem engedi, hogy explicit módon meghívjuk a `drop`-ot, mert a `main`
végén a Rust ettől függetlenül automatikusan meghívná a `drop`-ot az értéken.
Ez kétszeres felszabadítási hibát okozna, mivel a Rust kétszer próbálná
felszabadítani ugyanazt az értéket.

Nem kapcsolhatjuk ki a `drop` automatikus beillesztését, amikor egy érték
kikerül a hatókörből, és a `drop` metódust sem hívhatjuk meg explicit módon.
Ha tehát ki kell kényszerítenünk egy érték korai felszabadítását, az
`std::mem::drop` függvényt használjuk.

Az `std::mem::drop` függvény különbözik a `Drop` trait `drop` metódusától. Úgy
hívjuk meg, hogy argumentumként átadjuk neki azt az értéket, amelynek az
eldobását ki akarjuk kényszeríteni. A függvény benne van a prelude-ban, így a
15-15. kódrészlet `main` függvényét módosíthatjuk úgy, hogy a `drop`
függvényt hívja meg, ahogy a 15-16. kódrészlet mutatja.

<Listing number="15-16" file-name="src/main.rs" caption="Az `std::mem::drop` meghívása egy érték explicit eldobására, mielőtt kikerülne a hatókörből">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-16/src/main.rs:here}}
```

</Listing>

A kód futtatása a következőt írja ki:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-16/output.txt}}
```

A ``Dropping CustomSmartPointer with data `some data`!`` szöveg a
`CustomSmartPointer created` és a `CustomSmartPointer dropped before the end of
main` szöveg között jelenik meg, ami azt mutatja, hogy a `drop` metódus kódja
ezen a ponton hívódik meg a `c` eldobásához.

A `Drop` trait megvalósításában megadott kódot sokféleképpen használhatod arra,
hogy a felszabadítás kényelmes és biztonságos legyen: például akár saját
memóriafoglalót is készíthetsz vele! A `Drop` trait és a Rust tulajdonjogi
rendszere révén nem kell emlékezned a felszabadításra, mert a Rust ezt
automatikusan elvégzi.

Azok a problémák miatt sem kell aggódnod, amelyek a még használatban lévő
értékek véletlen felszabadításából adódnának: ugyanaz a tulajdonjogi rendszer,
amely biztosítja, hogy a referenciák mindig érvényesek legyenek, azt is
garantálja, hogy a `drop` csak egyszer hívódjon meg, amikor az értéket már nem
használjuk.

Most, hogy megvizsgáltuk a `Box<T>`-t és az okos mutatók néhány jellemzőjét,
nézzünk meg néhány további, a standard könyvtárban definiált okos mutatót.
