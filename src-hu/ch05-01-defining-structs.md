## Struktúrák definiálása és példányosítása {#defining-and-instantiating-structs}

A struktúrák hasonlítanak a tuple-ökhöz, amelyekről [„A tuple
típus”][tuples]<!-- ignore --> szakaszban volt szó, abban, hogy mindkettő több,
egymáshoz kapcsolódó értéket tárol. A tuple-ökhöz hasonlóan egy struktúra részei
is lehetnek különböző típusúak. A tuple-ökkel ellentétben azonban a struktúrában
minden adatelemnek nevet adsz, így egyértelmű, mit jelentenek az értékek. Ezek a
nevek rugalmasabbá teszik a struktúrákat a tuple-öknél: nem kell az adatok
sorrendjére hagyatkoznod, amikor egy példány értékeit megadod vagy eléred.

Egy struktúra definiálásához a `struct` kulcsszót írjuk, és nevet adunk az
egész struktúrának. A struktúra neve fejezze ki, mi a jelentősége az
összecsoportosított adatoknak. Ezután kapcsos zárójelek között megadjuk az
adatelemek nevét és típusát; ezeket _mezőknek (fields)_ nevezzük. Az 5-1.
kódrészlet például egy olyan struktúrát mutat, amely egy felhasználói fiók
adatait tárolja.

<Listing number="5-1" file-name="src/main.rs" caption="Egy `User` struktúra definíciója">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-01/src/main.rs:here}}
```

</Listing>

Ahhoz, hogy a definiálás után használni tudjuk a struktúrát, létrehozzuk egy
_példányát (instance)_ úgy, hogy minden mezőjének konkrét értéket adunk. Egy
példányt úgy hozunk létre, hogy leírjuk a struktúra nevét, majd utána kapcsos
zárójelek között _`kulcs: érték`_ párokat adunk meg, ahol a kulcsok a mezők
nevei, az értékek pedig az adatok, amelyeket ezekben a mezőkben tárolni
szeretnénk. A mezőket nem kell abban a sorrendben megadnunk, amelyben a
struktúrában deklaráltuk őket. Másként fogalmazva: a struktúradefiníció a
típus általános sablonja, a példányok pedig konkrét adatokkal töltik ki ezt a
sablont, így hozva létre a típus értékeit. Egy adott felhasználót például az
5-2. kódrészletben látható módon deklarálhatunk.

<Listing number="5-2" file-name="src/main.rs" caption="A `User` struktúra egy példányának létrehozása">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-02/src/main.rs:here}}
```

</Listing>

Egy struktúra adott értékét pontjelöléssel érhetjük el. Ennek a felhasználónak
az e-mail-címét például a `user1.email` kifejezéssel kapjuk meg. Ha a példány
módosítható, egy értéket úgy változtathatunk meg, hogy a pontjelöléssel egy
adott mezőnek új értéket adunk. Az 5-3. kódrészlet azt mutatja, hogyan
változtathatjuk meg egy módosítható `User` példány `email` mezőjének értékét.

<Listing number="5-3" file-name="src/main.rs" caption="Egy `User` példány `email` mezőjében tárolt érték megváltoztatása">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-03/src/main.rs:here}}
```

</Listing>

Figyeld meg, hogy az egész példánynak módosíthatónak kell lennie; a Rust nem
engedi, hogy csak bizonyos mezőket jelöljünk módosíthatónak. Mint bármely
kifejezésnél, a struktúra új példányát a függvénytörzs utolsó kifejezéseként is
létrehozhatjuk, így a függvény implicit módon ezt az új példányt adja vissza.

Az 5-4. kódrészlet egy `build_user` függvényt mutat, amely a megadott
e-mail-címmel és felhasználónévvel ad vissza egy `User` példányt. Az `active`
mező a `true` értéket kapja, a `sign_in_count` pedig az `1` értéket.

<Listing number="5-4" file-name="src/main.rs" caption="Egy `build_user` függvény, amely egy e-mail-címet és egy felhasználónevet kap, és egy `User` példányt ad vissza">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-04/src/main.rs:here}}
```

</Listing>

Ésszerű, hogy a függvény paramétereinek ugyanazt a nevet adjuk, mint a
struktúra mezőinek, de kissé fárasztó, hogy az `email` és a `username`
mezőneveket és változókat ismételgetnünk kell. Ha a struktúrának több mezője
lenne, az egyes nevek ismétlése még bosszantóbb lenne. Szerencsére van erre egy
kényelmes rövidítés!

<!-- Old headings. Do not remove or links may break. -->

<a id="using-the-field-init-shorthand-when-variables-and-fields-have-the-same-name"></a>

### A rövidített mezőinicializálás használata {#using-the-field-init-shorthand}

Mivel az 5-4. kódrészletben a paraméternevek és a struktúra mezőnevei pontosan
megegyeznek, a _rövidített mezőinicializálás (field init shorthand)_
szintaxisával átírhatjuk a `build_user` függvényt úgy, hogy pontosan ugyanúgy
működjön, de ne kelljen ismételni a `username` és az `email` nevet, ahogy az
5-5. kódrészlet mutatja.

<Listing number="5-5" file-name="src/main.rs" caption="Egy `build_user` függvény, amely rövidített mezőinicializálást használ, mert a `username` és az `email` paraméter neve megegyezik a struktúra mezőinek nevével">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-05/src/main.rs:here}}
```

</Listing>

Itt a `User` struktúra egy új példányát hozzuk létre, amelynek van egy `email`
nevű mezője. Az `email` mező értékét a `build_user` függvény `email`
paraméterének értékére szeretnénk állítani. Mivel az `email` mezőnek és az
`email` paraméternek ugyanaz a neve, elég az `email` nevet leírnunk az
`email: email` helyett.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-instances-from-other-instances-with-struct-update-syntax"></a>

### Példányok létrehozása a struktúrafrissítő szintaxissal {#creating-instances-with-struct-update-syntax}

Gyakran hasznos, ha egy struktúrának olyan új példányát hozzuk létre, amely egy
ugyanilyen típusú másik példány értékeinek többségét tartalmazza, de néhányat
megváltoztat. Ezt a struktúrafrissítő szintaxissal tehetjük meg.

Először az 5-6. kódrészletben megmutatjuk, hogyan hozhatunk létre egy új `User`
példányt a `user2` változóban a szokásos módon, a frissítő szintaxis nélkül. Az
`email` mezőnek új értéket adunk, egyébként pedig az 5-2. kódrészletben
létrehozott `user1` értékeit használjuk.

<Listing number="5-6" file-name="src/main.rs" caption="Új `User` példány létrehozása a `user1` értékeinek felhasználásával, egy kivételével">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-06/src/main.rs:here}}
```

</Listing>

A _struktúrafrissítő szintaxissal (struct update syntax)_ ugyanezt kevesebb
kóddal érhetjük el, ahogy az 5-7. kódrészlet mutatja. A `..` szintaxis azt
jelzi, hogy a kifejezetten meg nem adott többi mező ugyanazt az értéket kapja,
mint a megadott példány megfelelő mezői.

<Listing number="5-7" file-name="src/main.rs" caption="A struktúrafrissítő szintaxis használata egy `User` példány új `email` értékének megadására, a többi értéket a `user1`-ből véve">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-07/src/main.rs:here}}
```

</Listing>

Az 5-7. kódrészlet kódja szintén egy olyan példányt hoz létre a `user2`
változóban, amelynek más az `email` értéke, de a `username`, az `active` és a
`sign_in_count` mező értékei ugyanazok, mint a `user1`-ben. A `..user1`
kifejezésnek az utolsó helyen kell állnia, jelezve, hogy minden fennmaradó mező
a `user1` megfelelő mezőiből kapja az értékét, de annyi mezőnek adhatunk
értéket, amennyinek csak szeretnénk, tetszőleges sorrendben, függetlenül attól,
hogy a mezők milyen sorrendben szerepelnek a struktúra definíciójában.

Figyeld meg, hogy a struktúrafrissítő szintaxis az értékadáshoz hasonlóan `=`
jelet használ; ez azért van, mert mozgatja az adatokat, ahogy azt a [„Változók
és adatok kölcsönhatása mozgatással”][move]<!-- ignore --> szakaszban
láttuk.
Ebben a példában a `user2` létrehozása után már nem használhatjuk a `user1`
változót, mert a `user1` `username` mezőjében lévő `String` át lett mozgatva a
`user2`-be. Ha a `user2`-nek az `email` és a `username` mezőhöz is új `String`
értéket adtunk volna, és így a `user1`-ből csak az `active` és a
`sign_in_count` értékét használtuk volna, akkor a `user1` a `user2`
létrehozása után is érvényes maradna. Az `active` és a `sign_in_count` is olyan
típusú, amely megvalósítja a `Copy` traitet, így a [„Csak veremben tárolt
adatok: Copy”][copy]<!-- ignore --> szakaszban tárgyalt viselkedés érvényes
rájuk. Ebben a példában a `user1.email` mezőt is használhatjuk még, mert annak
az értéke nem lett kimozgatva a `user1`-ből.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-tuple-structs-without-named-fields-to-create-different-types"></a>

### Különböző típusok létrehozása tuple struktúrákkal {#creating-different-types-with-tuple-structs}

A Rust a tuple-ökhöz hasonló struktúrákat is támogat; ezeket _tuple
struktúráknak (tuple structs)_ nevezzük. A tuple struktúrák a struktúra nevéből
fakadó többletjelentéssel bírnak, de a mezőiknek nincs nevük, csak típusuk. A
tuple struktúrák akkor hasznosak, ha az egész tuple-nek nevet szeretnél adni,
és a többi tuple-től eltérő típussá szeretnéd tenni, illetve ha az egyes mezők
elnevezése, mint egy hagyományos struktúrában, túl bőbeszédű vagy fölösleges
lenne.

Egy tuple struktúra definiálásához a `struct` kulcsszóval és a struktúra
nevével kezdj, majd ezeket kövessék a tuple-ben lévő típusok. Itt például két
tuple struktúrát definiálunk és használunk, `Color` és `Point` néven:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-01-tuple-structs/src/main.rs}}
```

</Listing>

Figyeld meg, hogy a `black` és az `origin` érték különböző típusú, mert
különböző tuple struktúrák példányai. Minden általad definiált struktúra önálló
típus, még akkor is, ha a struktúrán belüli mezők típusa megegyezik. Egy
`Color` típusú paramétert váró függvény például nem kaphat argumentumként egy
`Point` értéket, pedig mindkét típus három `i32` értékből áll. Ettől eltekintve
a tuple struktúrák példányai a tuple-ökhöz hasonlóan viselkednek: szétbonthatod
őket az egyes részeikre, és egy `.` jellel, majd az indexszel elérheted az
egyes értékeket. A tuple-ökkel ellentétben a tuple struktúrák szétbontásakor meg
kell adnod a struktúra típusának nevét. Például a `let Point(x, y, z) = origin;`
sort írnánk, hogy az `origin` pont értékeit az `x`, `y` és `z` nevű változókba
bontsuk szét.

<!-- Old headings. Do not remove or links may break. -->

<a id="unit-like-structs-without-any-fields"></a>

### Unit-szerű struktúrák definiálása {#defining-unit-like-structs}

Olyan struktúrákat is definiálhatsz, amelyeknek egyáltalán nincs mezőjük! Ezeket
_unit-szerű struktúráknak (unit-like structs)_ nevezzük, mert a `()` értékhez,
vagyis a unit típushoz hasonlóan viselkednek, amelyet [„A tuple
típus”][tuples]<!-- ignore --> szakaszban említettünk. A unit-szerű struktúrák
akkor lehetnek hasznosak, ha egy típuson meg kell valósítanod egy traitet, de
nincs olyan adat, amelyet magában a típusban szeretnél tárolni. A traitekről a
10. fejezetben lesz szó. Íme egy példa egy `AlwaysEqual` nevű egységstruktúra
deklarálására és példányosítására:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-04-unit-like-structs/src/main.rs}}
```

</Listing>

Az `AlwaysEqual` definiálásához a `struct` kulcsszót, a kívánt nevet, majd egy
pontosvesszőt írunk. Nincs szükség kapcsos vagy kerek zárójelekre! Ezután
hasonló módon kaphatunk egy `AlwaysEqual` példányt a `subject` változóban: a
definiált nevet használjuk, kapcsos vagy kerek zárójelek nélkül. Képzeld el,
hogy később olyan viselkedést valósítunk meg ehhez a típushoz, amelynek
eredményeként az `AlwaysEqual` minden példánya mindig egyenlő bármely más típus
minden példányával – például azért, hogy teszteléskor ismert eredményt
kapjunk. Ennek a viselkedésnek a megvalósításához semmilyen adatra nem lenne
szükségünk! A 10. fejezetben látni fogod, hogyan definiálhatsz traiteket, és
hogyan valósíthatod meg őket bármilyen típuson, a unit-szerű struktúrákat is
beleértve.

> ### A struktúra adatainak tulajdonjoga {#ownership-of-struct-data}
>
> Az 5-1. kódrészletben szereplő `User` struktúradefinícióban a saját
> tulajdonú (owned) `String` típust használtuk a `&str` sztringszelet-típus
> helyett. Ez szándékos döntés, mert azt szeretnénk, hogy a struktúra minden
> példánya birtokolja az összes adatát, és hogy ezek az adatok addig legyenek
> érvényesek, ameddig az egész struktúra érvényes.
>
> Az is lehetséges, hogy a struktúrák valami más tulajdonában lévő adatokra
> mutató referenciákat tároljanak, ehhez azonban _élettartamokat (lifetimes)_
> kell használni, ami a Rust egyik nyelvi eleme, és a 10. fejezetben tárgyaljuk.
> Az élettartamok biztosítják, hogy a struktúra által hivatkozott adatok addig
> érvényesek legyenek, ameddig maga a struktúra. Tegyük fel, hogy élettartamok
> megadása nélkül próbálsz referenciát tárolni egy struktúrában, például így,
> az *src/main.rs* fájlban; ez nem fog működni:
>
> <Listing file-name="src/main.rs">
>
> <!-- CAN'T EXTRACT SEE https://github.com/rust-lang/mdBook/issues/1127 -->
>
> ```rust,ignore,does_not_compile
> struct User {
>     active: bool,
>     username: &str,
>     email: &str,
>     sign_in_count: u64,
> }
>
> fn main() {
>     let user1 = User {
>         active: true,
>         username: "someusername123",
>         email: "someone@example.com",
>         sign_in_count: 1,
>     };
> }
> ```
>
> </Listing>
>
> A fordító panaszkodni fog, hogy élettartam-jelölőkre van szüksége:
>
> ```console
> $ cargo run
>    Compiling structs v0.1.0 (file:///projects/structs)
> error[E0106]: missing lifetime specifier
>  --> src/main.rs:3:15
>   |
> 3 |     username: &str,
>   |               ^ expected named lifetime parameter
>   |
> help: consider introducing a named lifetime parameter
>   |
> 1 ~ struct User<'a> {
> 2 |     active: bool,
> 3 ~     username: &'a str,
>   |
>
> error[E0106]: missing lifetime specifier
>  --> src/main.rs:4:12
>   |
> 4 |     email: &str,
>   |            ^ expected named lifetime parameter
>   |
> help: consider introducing a named lifetime parameter
>   |
> 1 ~ struct User<'a> {
> 2 |     active: bool,
> 3 |     username: &str,
> 4 ~     email: &'a str,
>   |
>
> For more information about this error, try `rustc --explain E0106`.
> error: could not compile `structs` (bin "structs") due to 2 previous errors
> ```
>
> A 10. fejezetben megmutatjuk, hogyan javíthatod ki ezeket a hibákat, hogy
> referenciákat tárolhass a struktúrákban, egyelőre azonban az ilyen hibákat
> úgy javítjuk, hogy referenciák (például `&str`) helyett saját tulajdonú
> típusokat (például `String`) használunk.

<!-- manual-regeneration
for the error above
after running update-rustc.sh:
pbcopy < listings/ch05-using-structs-to-structure-related-data/no-listing-02-reference-in-struct/output.txt
paste above
add `> ` before every line -->

[tuples]: ch03-02-data-types.html#the-tuple-type
[move]: ch04-01-what-is-ownership.html#variables-and-data-interacting-with-move
[copy]: ch04-01-what-is-ownership.html#stack-only-data-copy
