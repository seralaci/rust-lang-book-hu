## Haladó típusok {#advanced-types}

A Rust típusrendszerének van néhány olyan vonása, amelyet eddig említettünk
ugyan, de még nem tárgyaltunk. Először általánosságban beszélünk a
newtype-okról, és megvizsgáljuk, miért hasznosak típusként. Ezután rátérünk a
típusálnevekre, amelyek a newtype-okhoz hasonló, de kissé eltérő szemantikájú
nyelvi elemek. Szó lesz a `!` típusról és a dinamikus méretű típusokról is.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-the-newtype-pattern-for-type-safety-and-abstraction"></a>

### Típusbiztonság és absztrakció a newtype mintával {#type-safety-and-abstraction-with-the-newtype-pattern}

Ez a szakasz feltételezi, hogy elolvastad a korábbi [„Külső traitek
megvalósítása a newtype mintával”][newtype]<!-- ignore --> szakaszt. A
newtype minta az eddig tárgyaltakon túl más feladatokra is hasznos, például
arra, hogy statikusan kikényszerítsük, hogy az értékek soha ne keveredjenek
össze, vagy hogy jelezzük egy érték mértékegységét. A 20-16. kódrészletben már
láttál példát arra, hogyan jelezhetünk mértékegységet newtype-okkal: emlékezz,
a `Millimeters` és a `Meters` struktúrák `u32` értékeket burkoltak be egy
newtype-ba. Ha írnánk egy `Millimeters` típusú paraméterrel rendelkező
függvényt, nem tudnánk lefordítani olyan programot, amely véletlenül `Meters`
típusú vagy sima `u32` értékkel próbálná meghívni ezt a függvényt.

A newtype mintával egy típus bizonyos megvalósítási részleteit is
elabsztrahálhatjuk: az új típus a privát belső típus API-jától eltérő
nyilvános API-t tehet közzé.

A newtype-ok a belső megvalósítást is elrejthetik. Például létrehozhatnánk egy
`People` típust, amely egy `HashMap<i32, String>`-et burkol be, és az emberek
azonosítóját a nevükhöz társítva tárolja. A `People`-t használó kód csak az
általunk biztosított nyilvános API-val érintkezne, például egy olyan
metódussal, amely egy névsztringet ad hozzá a `People` gyűjteményhez; ennek a
kódnak nem kellene tudnia arról, hogy belül `i32` azonosítót rendelünk a
nevekhez. A newtype minta egyszerű módja az egységbezárásnak (encapsulation),
amellyel elrejthetjük a megvalósítás részleteit; erről a 18. fejezet [„A
megvalósítás részleteit elrejtő
egységbezárás”][encapsulation-that-hides-implementation-details]<!-- ignore -->
szakaszában volt szó.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-type-synonyms-with-type-aliases"></a>

### Típusszinonimák és típusálnevek {#type-synonyms-and-type-aliases}

A Rust lehetővé teszi, hogy _típusálnevet (type alias)_ deklaráljunk, amellyel
egy meglévő típusnak másik nevet adunk. Ehhez a `type` kulcsszót használjuk.
Például így hozhatjuk létre a `Kilometers` álnevet az `i32`-höz:

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-04-kilometers-alias/src/main.rs:here}}
```

Most a `Kilometers` álnév az `i32` _szinonimája (synonym)_; a 20-16.
kódrészletben létrehozott `Millimeters` és `Meters` típusokkal ellentétben a
`Kilometers` nem különálló, új típus. A `Kilometers` típusú értékeket ugyanúgy
kezeli a fordító, mint az `i32` típusú értékeket:

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-04-kilometers-alias/src/main.rs:there}}
```

Mivel a `Kilometers` és az `i32` ugyanaz a típus, a két típus értékeit
összeadhatjuk, és `Kilometers` értékeket átadhatunk olyan függvényeknek,
amelyek `i32` paramétert várnak. Ezzel a módszerrel azonban nem kapjuk meg azt a
típusellenőrzési előnyt, amelyet a korábban tárgyalt newtype minta nyújt. Más
szóval, ha valahol összekeverjük a `Kilometers` és az `i32` értékeket, a
fordító nem fog hibát jelezni.

A típusszinonimák fő felhasználási területe az ismétlés csökkentése. Lehet
például egy ilyen hosszú típusunk:

```rust,ignore
Box<dyn Fn() + Send + 'static>
```

Ezt a hosszú típust függvényszignatúrákban és típusannotációkként a kódban
mindenhol kiírni fárasztó és hibalehetőségekkel teli lehet. Képzelj el egy
projektet, amely tele van a 20-25. kódrészlethez hasonló kóddal.

<Listing number="20-25" caption="Egy hosszú típus használata sok helyen">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-25/src/main.rs:here}}
```

</Listing>

Egy típusálnév az ismétlés csökkentésével kezelhetőbbé teszi ezt a kódot. A
20-26. kódrészletben bevezettünk egy `Thunk` nevű álnevet a bőbeszédű
típushoz, és a típus minden használatát lecserélhetjük a rövidebb `Thunk`
álnévre.

<Listing number="20-26" caption="Egy `Thunk` típusálnév bevezetése az ismétlés csökkentésére">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-26/src/main.rs:here}}
```

</Listing>

Ezt a kódot sokkal könnyebb olvasni és írni! Ha a típusálnévnek beszédes nevet
választasz, azzal a szándékodat is jobban kifejezheted (a _thunk_ szó olyan
kódot jelöl, amelyet egy későbbi időpontban értékelünk ki, így megfelelő név
egy eltárolt closure számára).

A típusálneveket gyakran használjuk a `Result<T, E>` típussal is az ismétlés
csökkentésére. Vegyük a standard könyvtár `std::io` modulját. Az I/O
műveletek gyakran `Result<T, E>`-t adnak vissza, hogy kezelni lehessen azokat a
helyzeteket, amikor a művelet nem sikerül. Ebben a könyvtárban van egy
`std::io::Error` struktúra, amely az összes lehetséges I/O hibát képviseli. Az
`std::io` számos függvénye olyan `Result<T, E>`-t ad vissza, ahol az `E` az
`std::io::Error`, például a `Write` trait alábbi függvényei:

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-05-write-trait/src/lib.rs}}
```

A `Result<..., Error>` sokszor ismétlődik. Ezért az `std::io`-ban szerepel ez a
típusálnév-deklaráció:

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-06-result-alias/src/lib.rs:here}}
```

Mivel ez a deklaráció az `std::io` modulban van, használhatjuk a teljesen
minősített `std::io::Result<T>` álnevet; ez egy olyan `Result<T, E>`, amelyben
az `E` helyén az `std::io::Error` áll. A `Write` trait függvényszignatúrái
végül így néznek ki:

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-06-result-alias/src/lib.rs:there}}
```

A típusálnév kétféleképpen segít: könnyebbé teszi a kód írását, _és_ egységes
interfészt biztosít az egész `std::io`-ban. Mivel ez csak egy álnév, valójában
egy újabb `Result<T, E>`, ami azt jelenti, hogy minden olyan metódust
használhatunk vele, amely a `Result<T, E>`-n működik, és az olyan speciális
szintaxist is, mint a `?` operátor.

### A never típus, amely soha nem tér vissza {#the-never-type-that-never-returns}

A Rustban van egy `!` nevű speciális típus, amelyet a típuselmélet
szóhasználatában _üres típusnak (empty type)_ neveznek, mert nincsenek
értékei. Mi inkább _never típusnak (never type)_ hívjuk, mert ez áll a
visszatérési típus helyén, ha egy függvény soha nem tér vissza. Íme egy példa:

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-07-never-type/src/lib.rs:here}}
```

Ezt a kódot úgy olvassuk: „a `bar` függvény soha nem tér vissza”. Azokat a
függvényeket, amelyek soha nem térnek vissza, _divergáló függvényeknek
(diverging functions)_ nevezzük. A `!` típusnak nem hozhatunk létre értékeket,
így a `bar` semmiképp sem térhet vissza.

De mire jó egy olyan típus, amelynek soha nem hozhatunk létre értékeket?
Emlékezz a 2-5. kódrészlet kódjára, amely a számkitalálós játék része volt; egy
részletét itt, a 20-27. kódrészletben újra közöljük.

<Listing number="20-27" caption="Egy `match`, amelynek egyik ága `continue`-val végződik">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-05/src/main.rs:ch19}}
```

</Listing>

Akkor átugrottunk néhány részletet ebben a kódban. A 6. fejezet [„A `match`
vezérlési szerkezet”][the-match-control-flow-construct]<!-- ignore -->
szakaszában megbeszéltük, hogy a `match` minden ágának ugyanolyan típust kell
visszaadnia. Így például a következő kód nem működik:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-08-match-arms-different-types/src/main.rs:here}}
```

Ebben a kódban a `guess` típusának egész számnak _és_ sztringnek is kellene
lennie, a Rust pedig megköveteli, hogy a `guess`-nek csak egy típusa legyen.
Mit ad vissza tehát a `continue`? Hogyan adhattunk vissza a 20-27.
kódrészletben az egyik ágból `u32`-t, miközben egy másik ág `continue`-val
végződött?

Ahogy talán sejted, a `continue` értéke `!`. Vagyis amikor a Rust kiszámítja a
`guess` típusát, mindkét match ágat megnézi: az elsőnek `u32` az értéke, a
másodiknak `!`. Mivel a `!`-nek soha nem lehet értéke, a Rust úgy dönt, hogy a
`guess` típusa `u32`.

Ennek a viselkedésnek a formális leírása az, hogy a `!` típusú kifejezések
bármilyen más típusra konvertálhatók (coerce). Ezt a `match` ágat azért
zárhatjuk `continue`-val, mert a `continue` nem ad vissza értéket; ehelyett a
vezérlést visszaviszi a ciklus elejére, így az `Err` esetben soha nem adunk
értéket a `guess`-nek.

A never típus a `panic!` makróval is hasznos. Emlékezz az `unwrap` függvényre,
amelyet `Option<T>` értékeken hívunk meg, hogy egy értéket kapjunk vagy
pánikoljunk; ez a definíciója:

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-09-unwrap-definition/src/lib.rs:here}}
```

Ebben a kódban ugyanaz történik, mint a 20-27. kódrészlet `match`-ében: a Rust
látja, hogy a `val` típusa `T`, a `panic!` típusa pedig `!`, így a teljes
`match` kifejezés eredménye `T`. Ez a kód azért működik, mert a `panic!` nem
állít elő értéket; befejezi a programot. A `None` esetben nem adunk vissza
értéket az `unwrap`-ből, így ez a kód érvényes.

Egy utolsó kifejezés, amelynek `!` a típusa, a ciklus:

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-10-loop-returns-never/src/main.rs:here}}
```

Itt a ciklus soha nem ér véget, így a kifejezés értéke `!`. Ez azonban nem
lenne igaz, ha egy `break`-et is beletennénk, mert a ciklus a `break`-hez érve
befejeződne.

### A dinamikus méretű típusok és a `Sized` trait {#dynamically-sized-types-and-the-sized-trait}

A Rustnak ismernie kell a típusainak bizonyos részleteit, például azt, hogy egy
adott típusú értéknek mennyi helyet kell lefoglalni. Emiatt a típusrendszer egy
szeglete elsőre kissé zavarba ejtő: ez a _dinamikus méretű típusok (dynamically
sized types)_ fogalma. Ezek a típusok – amelyeket néha _DST_-knek vagy _méret
nélküli típusoknak (unsized types)_ is neveznek – lehetővé teszik, hogy olyan
értékeket használó kódot írjunk, amelyeknek a méretét csak futásidőben
ismerhetjük meg.

Nézzük meg részletesen a `str` nevű dinamikus méretű típust, amelyet a könyvben
végig használtunk. Bizony, nem a `&str`, hanem önmagában a `str` egy DST. Sok
esetben, például egy felhasználó által beírt szöveg tárolásakor, csak
futásidőben tudhatjuk meg, milyen hosszú a sztring. Ez azt jelenti, hogy nem
hozhatunk létre `str` típusú változót, és `str` típusú argumentumot sem
fogadhatunk. Vegyük a következő kódot, amely nem működik:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-11-cant-create-str/src/main.rs:here}}
```

A Rustnak tudnia kell, mennyi memóriát foglaljon le egy adott típus bármely
értékének, és egy típus minden értékének ugyanannyi memóriát kell használnia.
Ha a Rust megengedné, hogy ezt a kódot megírjuk, ennek a két `str` értéknek
ugyanannyi helyet kellene elfoglalnia. Csakhogy a hosszuk eltér: az `s1`-nek 12
bájt tárhelyre van szüksége, az `s2`-nek 15-re. Ezért nem lehet dinamikus
méretű típust tartalmazó változót létrehozni.

Mit tegyünk tehát? Ebben az esetben már tudod a választ: az `s1` és az `s2`
típusát `str` helyett sztringszeletté (`&str`) tesszük. Emlékezz a 4. fejezet
[„Sztringszeletek”][string-slices]<!-- ignore --> szakaszából, hogy a szelet
adatszerkezet csak a szelet kezdőpozícióját és hosszát tárolja. Így míg a `&T`
egyetlen érték, amely annak a memóriacímét tárolja, ahol a `T` található, a
sztringszelet _két_ érték: a `str` címe és a hossza. Ezért egy sztringszelet
értékének méretét fordítási időben ismerhetjük: kétszer akkora, mint egy
`usize`. Vagyis egy sztringszelet méretét mindig ismerjük, függetlenül attól,
milyen hosszú sztringre hivatkozik. Általánosságban így használjuk a dinamikus
méretű típusokat a Rustban: van egy kis extra metaadatuk, amely a dinamikus
információ méretét tárolja. A dinamikus méretű típusok aranyszabálya, hogy a
dinamikus méretű típusok értékeit mindig valamilyen mutató mögé kell tennünk.

A `str`-t mindenféle mutatóval kombinálhatjuk: például `Box<str>` vagy
`Rc<str>`. Valójában ezt már láttad korábban, csak egy másik dinamikus méretű
típussal: a traitekkel. Minden trait egy dinamikus méretű típus, amelyre a trait
nevével hivatkozhatunk. A 18. fejezet [„Trait objektumok használata a közös
viselkedés
absztrahálására”][using-trait-objects-to-abstract-over-shared-behavior]<!-- ignore
--> szakaszában említettük, hogy ha traiteket trait objektumként szeretnénk
használni, mutató mögé kell tennünk őket, például `&dyn Trait` vagy `Box<dyn
Trait>` alakban (az `Rc<dyn Trait>` is működne).

A DST-kkel való munkához a Rust a `Sized` traitet biztosítja, amellyel
eldönthető, hogy egy típus mérete ismert-e fordítási időben. Ezt a traitet a
fordító automatikusan megvalósítja minden olyan típusra, amelynek mérete
fordítási időben ismert. Ezenkívül a Rust implicit módon minden generikus
függvényhez hozzáad egy `Sized` korlátot. Vagyis egy ilyen generikus
függvénydefiníciót:

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-12-generic-fn-definition/src/lib.rs}}
```

valójában úgy kezel, mintha ezt írtuk volna:

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-13-generic-implicit-sized-bound/src/lib.rs}}
```

A generikus függvények alapértelmezés szerint csak olyan típusokon működnek,
amelyeknek a mérete fordítási időben ismert. Ezt a korlátozást azonban a
következő speciális szintaxissal enyhítheted:

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-14-generic-maybe-sized/src/lib.rs}}
```

A `?Sized` trait-korlát azt jelenti, hogy „a `T` lehet `Sized`, de lehet, hogy
nem az”, és ez a jelölés felülírja azt az alapértelmezést, hogy a generikus
típusoknak fordítási időben ismert méretűnek kell lenniük. A `?Trait`
szintaxis ezzel a jelentéssel csak a `Sized`-hoz érhető el, más traitekhez nem.

Vedd észre azt is, hogy a `t` paraméter típusát `T`-ről `&T`-re változtattuk.
Mivel a típus lehet, hogy nem `Sized`, valamilyen mutató mögött kell
használnunk. Ebben az esetben egy referenciát választottunk.

A következőkben a függvényekről és a closure-ökről lesz szó!

[encapsulation-that-hides-implementation-details]: ch18-01-what-is-oo.html#encapsulation-that-hides-implementation-details
[string-slices]: ch04-03-slices.html#string-slices
[the-match-control-flow-construct]: ch06-02-match.html#the-match-control-flow-construct
[using-trait-objects-to-abstract-over-shared-behavior]: ch18-02-trait-objects.html#using-trait-objects-to-abstract-over-shared-behavior
[newtype]: ch20-02-advanced-traits.html#implementing-external-traits-with-the-newtype-pattern
