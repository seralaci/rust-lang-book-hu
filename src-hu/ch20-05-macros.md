## Makrók {#macros}

A könyvben végig használtunk olyan makrókat, mint a `println!`, de még nem
vizsgáltuk meg alaposan, mi is az a makró, és hogyan működik. A _makró
(macro)_ kifejezés a Rust nyelvi elemeinek egy családjára utal: a
`macro_rules!`-szal létrehozott deklaratív makrókra és a procedurális makrók
három fajtájára:

- Egyéni `#[derive]` makrók, amelyek a struktúrákon és enumokon használt
  `derive` attribútummal hozzáadott kódot határozzák meg
- Attribútumszerű makrók, amelyek bármely elemen használható egyéni
  attribútumokat definiálnak
- Függvényszerű makrók, amelyek függvényhívásnak látszanak, de az
  argumentumként megadott tokeneken dolgoznak

Sorra vesszük mindegyiket, de előbb nézzük meg, miért van egyáltalán szükségünk
makrókra, ha már vannak függvényeink.

### A makrók és a függvények közötti különbség {#the-difference-between-macros-and-functions}

A makrók alapvetően olyan kód írására szolgálnak, amely más kódot ír; ezt
_metaprogramozásnak (metaprogramming)_ nevezzük. A C. függelékben tárgyaljuk a
`derive` attribútumot, amely különféle traitek megvalósítását generálja
helyetted. A könyvben végig használtuk a `println!` és a `vec!` makrót is.
Ezek a makrók mind _kifejtődnek (expand)_, és több kódot állítanak elő annál,
amit kézzel megírtál.

A metaprogramozás hasznos a megírandó és karbantartandó kód mennyiségének
csökkentésére, ami egyben a függvények egyik szerepe is. A makróknak azonban
van néhány további képességük, amelyekkel a függvények nem rendelkeznek.

Egy függvényszignatúrának deklarálnia kell a függvény paramétereinek számát és
típusát. A makrók ezzel szemben változó számú paramétert fogadhatnak: a
`println!("hello")`-t egy argumentummal, a `println!("hello {}", name)`-et
pedig kettővel hívhatjuk meg. Emellett a makrók kifejtése még azelőtt
megtörténik, hogy a fordító értelmezné a kód jelentését, így egy makró például
megvalósíthat egy traitet egy adott típuson. Egy függvény erre nem képes, mert
futásidőben hívódik meg, egy traitet pedig fordítási időben kell megvalósítani.

A makró függvény helyett történő megvalósításának hátránya, hogy a
makródefiníciók bonyolultabbak a függvénydefinícióknál, mert olyan Rust kódot
írsz, amely Rust kódot ír. Ennek a közvetettségnek köszönhetően a
makródefiníciókat általában nehezebb olvasni, megérteni és karbantartani, mint
a függvénydefiníciókat.

Egy másik fontos különbség a makrók és a függvények között, hogy a makrókat egy
fájlban azelőtt kell definiálnod vagy hatókörbe hoznod, _mielőtt_ meghívnád
őket, míg a függvényeket bárhol definiálhatod és bárhol meghívhatod.

<!-- Old headings. Do not remove or links may break. -->

<a id="declarative-macros-with-macro_rules-for-general-metaprogramming"></a>

### Deklaratív makrók általános metaprogramozáshoz {#declarative-macros-for-general-metaprogramming}

A Rustban a makrók legelterjedtebb formája a _deklaratív makró (declarative
macro)_. Ezeket néha „példa alapján definiált makróknak” (macros by example),
„`macro_rules!` makróknak” vagy egyszerűen „makróknak” is nevezik. A deklaratív
makrók lényegében a Rust `match` kifejezéséhez hasonló dolgot tesznek
lehetővé. Ahogy a 6. fejezetben tárgyaltuk, a `match` kifejezések olyan
vezérlési szerkezetek, amelyek egy kifejezést kapnak, a kifejezés eredményül
kapott értékét mintákkal vetik össze, majd az illeszkedő mintához tartozó kódot
futtatják. A makrók is egy értéket vetnek össze bizonyos kódhoz tartozó
mintákkal: ebben az esetben az érték a makrónak átadott szó szerinti Rust
forráskód, a mintákat ennek a forráskódnak a szerkezetével vetjük össze, és az
egyes mintákhoz tartozó kód illeszkedés esetén a makrónak átadott kód helyére
kerül. Mindez fordítás közben történik.

Makró definiálásához a `macro_rules!` szerkezetet használjuk. Nézzük meg, hogyan
kell a `macro_rules!`-t használni, azon keresztül, hogyan van definiálva a
`vec!` makró. A 8. fejezetben bemutattuk, hogyan hozhatunk létre a `vec!`
makróval adott értékeket tartalmazó új vektort. A következő makró például egy
három egész számot tartalmazó új vektort hoz létre:

```rust
let v: Vec<u32> = vec![1, 2, 3];
```

A `vec!` makróval két egész számból álló vektort vagy öt sztringszeletből álló
vektort is létrehozhatnánk. Függvénnyel ugyanezt nem tudnánk megtenni, mert nem
ismernénk előre az értékek számát és típusát.

A 20-35. kódrészlet a `vec!` makró kissé egyszerűsített definícióját mutatja.

<Listing number="20-35" file-name="src/lib.rs" caption="A `vec!` makró definíciójának egyszerűsített változata">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-35/src/lib.rs}}
```

</Listing>

> Megjegyzés: A `vec!` makró standard könyvtárbeli tényleges definíciója olyan
> kódot is tartalmaz, amely előre lefoglalja a megfelelő mennyiségű memóriát.
> Ez a kód egy optimalizáció, amelyet a példa egyszerűsítése érdekében itt nem
> szerepeltetünk.

A `#[macro_export]` annotáció azt jelzi, hogy ezt a makrót elérhetővé kell
tenni, valahányszor azt a crate-et, amelyben a makró definiálva van, hatókörbe
hozzák. Enélkül az annotáció nélkül a makrót nem lehet hatókörbe hozni.

Ezután a makródefiníciót a `macro_rules!`-szal és a definiált makró
felkiáltójel _nélküli_ nevével kezdjük. A nevet – ebben az esetben `vec` –
kapcsos zárójelek követik, amelyek a makródefiníció törzsét jelölik.

A `vec!` törzsének szerkezete a `match` kifejezés szerkezetéhez hasonló. Itt
egyetlen águnk van a `( $( $x:expr ),* )` mintával, amelyet a `=>` és az
ehhez a mintához tartozó kódblokk követ. Ha a minta illeszkedik, a hozzá
tartozó kódblokk kerül a kimenetbe. Mivel ez az egyetlen minta ebben a
makróban, csak egyféleképpen lehet illeszkedni; bármilyen más minta hibát
eredményez. Az összetettebb makróknak egynél több águk lesz.

A makródefiníciókban érvényes mintaszintaxis eltér a 19. fejezetben tárgyalt
mintaszintaxistól, mert a makrómintákat a Rust kód szerkezetére illesztjük, nem
pedig értékekre. Nézzük végig, mit jelentenek a 20-29. kódrészlet mintájának
darabjai; a teljes makrómintaszintaxist [a Rust referenciában][ref] találod.

Először egy zárójelpárral fogjuk közre a teljes mintát. Dollárjellel (`$`)
deklarálunk egy változót a makrórendszerben, amely a mintára illeszkedő Rust
kódot fogja tartalmazni. A dollárjel egyértelművé teszi, hogy ez egy
makróváltozó, nem pedig egy szokásos Rust változó. Ezután egy újabb zárójelpár
következik, amely elkapja a zárójeleken belüli mintára illeszkedő értékeket,
hogy felhasználhassuk őket a helyettesítő kódban. A `$()` belsejében a
`$x:expr` áll, amely bármilyen Rust kifejezésre illeszkedik, és a kifejezésnek
az `$x` nevet adja.

A `$()` utáni vessző azt jelzi, hogy a `$()`-on belüli kódra illeszkedő kód
minden példánya között egy szó szerinti vessző elválasztó karakternek kell
állnia. A `*` azt adja meg, hogy a minta a `*` előtt álló bármiből nulla vagy
több előfordulásra illeszkedik.

Ha ezt a makrót a `vec![1, 2, 3];` alakban hívjuk meg, az `$x` minta háromszor
illeszkedik, az `1`, `2` és `3` kifejezésre.

Most nézzük meg az ehhez az ághoz tartozó kód törzsében lévő mintát: a `$()*`
belsejében lévő `temp_vec.push()` minden olyan részhez legenerálódik, amely a
mintában a `$()`-ra illeszkedik, nullaszor vagy többször, attól függően, hogy a
minta hányszor illeszkedik. Az `$x` helyére rendre az illeszkedő kifejezések
kerülnek. Ha ezt a makrót a `vec![1, 2, 3];` alakban hívjuk meg, a makróhívás
helyére generált kód a következő lesz:

```rust,ignore
{
    let mut temp_vec = Vec::new();
    temp_vec.push(1);
    temp_vec.push(2);
    temp_vec.push(3);
    temp_vec
}
```

Definiáltunk egy makrót, amely tetszőleges számú, tetszőleges típusú
argumentumot fogadhat, és képes olyan kódot generálni, amely a megadott
elemeket tartalmazó vektort hoz létre.

Ha többet szeretnél megtudni a makróírásról, nézd meg az online dokumentációt
vagy más forrásokat, például a Daniel Keep által elkezdett és Lukas Wirth által
folytatott [„The Little Book of Rust Macros”][tlborm] című könyvet.

### Procedurális makrók kód generálására attribútumokból {#procedural-macros-for-generating-code-from-attributes}

A makrók második formája a procedurális makró, amely inkább függvényként
viselkedik (és egyfajta eljárás, azaz procedúra). A _procedurális makrók
(procedural macros)_ bemenetként kódot kapnak, ezen a kódon dolgoznak, és
kimenetként kódot állítanak elő, ahelyett hogy mintákra illesztenének, és a
kódot más kódra cserélnék, ahogy a deklaratív makrók teszik. A procedurális
makrók három fajtája az egyéni `derive`, az attribútumszerű és a függvényszerű
makró, és mindhárom hasonló módon működik.

Procedurális makrók létrehozásakor a definícióknak egy saját, speciális típusú
crate-ben kell lenniük. Ennek összetett technikai okai vannak, amelyeket
reméljük, hogy a jövőben megszüntethetünk. A 20-36. kódrészletben bemutatjuk,
hogyan definiálhatunk procedurális makrót; a `some_attribute` egy adott
makrófajta használatának helyőrzője.

<Listing number="20-36" file-name="src/lib.rs" caption="Példa procedurális makró definiálására">

```rust,ignore
use proc_macro::TokenStream;

#[some_attribute]
pub fn some_name(input: TokenStream) -> TokenStream {
}
```

</Listing>

A procedurális makrót definiáló függvény bemenetként egy `TokenStream`-et kap,
és kimenetként egy `TokenStream`-et állít elő. A `TokenStream` típust a Rusttal
együtt érkező `proc_macro` crate definiálja, és tokenek sorozatát reprezentálja.
Ez a makró lényege: a forráskód, amelyen a makró dolgozik, alkotja a bemeneti
`TokenStream`-et, a makró által előállított kód pedig a kimeneti
`TokenStream`. A függvényhez egy attribútum is tartozik, amely megadja, hogy
milyen fajta procedurális makrót hozunk létre. Ugyanabban a crate-ben többféle
procedurális makró is lehet.

Nézzük meg a procedurális makrók különböző fajtáit! Az egyéni `derive` makróval
kezdünk, majd elmagyarázzuk azokat az apró eltéréseket, amelyekben a többi
forma különbözik tőle.

<!-- Old headings. Do not remove or links may break. -->

<a id="how-to-write-a-custom-derive-macro"></a>

### Egyéni `derive` makrók {#custom-derive-macros}

Hozzunk létre egy `hello_macro` nevű crate-et, amely egy `HelloMacro` nevű
traitet definiál egy `hello_macro` nevű társított függvénnyel. Ahelyett hogy a
felhasználóinkkal minden egyes típusukra megvalósíttatnánk a `HelloMacro`
traitet, egy procedurális makrót biztosítunk, hogy a felhasználók a
`#[derive(HelloMacro)]` annotációval láthassák el a típusukat, és így
megkapják a `hello_macro` függvény alapértelmezett megvalósítását. Az
alapértelmezett megvalósítás a `Hello, Macro! My name is TypeName!` szöveget
írja ki, ahol a `TypeName` annak a típusnak a neve, amelyen ezt a traitet
definiálták. Más szóval olyan crate-et írunk, amelynek segítségével egy másik
programozó a 20-37. kódrészlethez hasonló kódot írhat.

<Listing number="20-37" file-name="src/main.rs" caption="A kód, amelyet a crate-ünk felhasználója a procedurális makrónk használatával írhat">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-37/src/main.rs}}
```

</Listing>

Ez a kód, ha elkészültünk, a `Hello, Macro! My name is Pancakes!` szöveget
írja ki. Az első lépés egy új könyvtár crate létrehozása, így:

```console
$ cargo new hello_macro --lib
```

Ezután a 20-38. kódrészletben definiáljuk a `HelloMacro` traitet és a hozzá
tartozó társított függvényt.

<Listing file-name="src/lib.rs" number="20-38" caption="Egy egyszerű trait, amelyet a `derive` makróval fogunk használni">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-38/hello_macro/src/lib.rs}}
```

</Listing>

Van egy traitünk és annak függvénye. Ezen a ponton a crate-ünk felhasználója
megvalósíthatná a traitet a kívánt funkcionalitás eléréséhez, ahogy a 20-39.
kódrészletben.

<Listing number="20-39" file-name="src/main.rs" caption="Így nézne ki, ha a felhasználók kézzel írnák meg a `HelloMacro` trait megvalósítását">

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-39/pancakes/src/main.rs}}
```

</Listing>

Ehhez azonban minden olyan típushoz meg kellene írniuk a megvalósító blokkot,
amelyet a `hello_macro`-val szeretnének használni; ettől a munkától szeretnénk
megkímélni őket.

Ráadásul a `hello_macro` függvényhez még nem tudunk olyan alapértelmezett
megvalósítást adni, amely kiírja annak a típusnak a nevét, amelyen a trait meg
van valósítva: a Rustban nincs reflexió (reflection), így futásidőben nem tudja
lekérdezni a típus nevét. Makróra van szükségünk, amely fordítási időben
generál kódot.

A következő lépés a procedurális makró definiálása. E sorok írásakor a
procedurális makróknak saját crate-ben kell lenniük. Ez a korlátozás idővel
megszűnhet. A crate-ek és a makró-crate-ek szerkezetének megszokott elnevezése a
következő: egy `foo` nevű crate-hez tartozó egyéni `derive` procedurális makró
crate neve `foo_derive`. Hozzunk létre egy új, `hello_macro_derive` nevű
crate-et a `hello_macro` projektünkön belül:

```console
$ cargo new hello_macro_derive --lib
```

A két crate szorosan összefügg, ezért a procedurális makró crate-et a
`hello_macro` crate mappáján belül hozzuk létre. Ha megváltoztatjuk a
traitdefiníciót a `hello_macro`-ban, a `hello_macro_derive`-ban lévő
procedurális makró megvalósítását is módosítanunk kell. A két crate-et külön
kell majd közzétenni, és az ezeket használó programozóknak mindkettőt fel kell
venniük függőségként, és mindkettőt hatókörbe kell hozniuk. Ehelyett azt is
megtehetnénk, hogy a `hello_macro` crate függőségként használja a
`hello_macro_derive`-ot, és újraexportálja a procedurális makró kódját. A
projekt általunk választott szerkezete azonban lehetővé teszi, hogy a
programozók akkor is használhassák a `hello_macro`-t, ha nem kérnek a `derive`
funkcionalitásból.

A `hello_macro_derive` crate-et procedurális makró crate-ként kell
deklarálnunk. Szükségünk lesz a `syn` és a `quote` crate funkcionalitására is,
ahogy mindjárt látni fogod, ezért ezeket fel kell vennünk függőségként. Add
hozzá a következőt a `hello_macro_derive` _Cargo.toml_ fájljához:

<Listing file-name="hello_macro_derive/Cargo.toml">

```toml
{{#include ../listings/ch20-advanced-features/listing-20-40/hello_macro/hello_macro_derive/Cargo.toml:6:12}}
```

</Listing>

A procedurális makró definiálásának megkezdéséhez írd a 20-40. kódrészlet
kódját a `hello_macro_derive` crate _src/lib.rs_ fájljába. Vedd figyelembe,
hogy ez a kód addig nem fordul le, amíg nem adunk definíciót az
`impl_hello_macro` függvénynek.

<Listing number="20-40" file-name="hello_macro_derive/src/lib.rs" caption="A kód, amelyre a legtöbb procedurális makró crate-nek szüksége lesz a Rust kód feldolgozásához">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-40/hello_macro/hello_macro_derive/src/lib.rs}}
```

</Listing>

Figyeld meg, hogy a kódot két részre osztottuk: a `hello_macro_derive`
függvényre, amely a `TokenStream` elemzéséért felel, és az `impl_hello_macro`
függvényre, amely a szintaxisfa átalakításáért felel: így kényelmesebb
procedurális makrót írni. A külső függvény (ebben az esetben a
`hello_macro_derive`) kódja szinte minden procedurális makró crate-ben ugyanaz
lesz, amellyel találkozol vagy amelyet létrehozol. A belső függvény (ebben az
esetben az `impl_hello_macro`) törzsében megadott kód a procedurális makród
céljától függően eltérő lesz.

Három új crate-et vezettünk be: a `proc_macro`, a [`syn`][syn]<!-- ignore -->
és a [`quote`][quote]<!-- ignore --> crate-et. A `proc_macro` crate a Rusttal
együtt érkezik, így nem kellett felvennünk a függőségek közé a _Cargo.toml_
fájlban. A `proc_macro` crate a fordító API-ja, amely lehetővé teszi, hogy a
saját kódunkból Rust kódot olvassunk és módosítsunk.

A `syn` crate a Rust kódot egy sztringből olyan adatszerkezetté elemzi, amelyen
műveleteket végezhetünk. A `quote` crate a `syn` adatszerkezeteit visszaalakítja
Rust kóddá. Ezek a crate-ek sokkal egyszerűbbé teszik bármilyen Rust kód
elemzését, amelyet kezelni szeretnénk: egy teljes elemző (parser) megírása a
Rust kódhoz nem egyszerű feladat.

A `hello_macro_derive` függvény akkor hívódik meg, amikor a könyvtárunk egy
felhasználója egy típuson megadja a `#[derive(HelloMacro)]`-t. Ez azért
lehetséges, mert itt a `hello_macro_derive` függvényt a `proc_macro_derive`
annotációval láttuk el, és megadtuk a `HelloMacro` nevet, amely megegyezik a
traitünk nevével; a legtöbb procedurális makró ezt a megállapodást követi.

A `hello_macro_derive` függvény először az `input`-ot `TokenStream`-ből olyan
adatszerkezetté alakítja, amelyet aztán értelmezhetünk, és amelyen műveleteket
végezhetünk. Itt lép színre a `syn`. A `syn` `parse` függvénye egy
`TokenStream`-et kap, és egy `DeriveInput` struktúrát ad vissza, amely az
elemzett Rust kódot reprezentálja. A 20-41. kódrészlet a `DeriveInput`
struktúra azon részeit mutatja, amelyeket a `struct Pancakes;` sztring
elemzésekor kapunk.

<Listing number="20-41" caption="A `DeriveInput` példány, amelyet a 20-37. kódrészlet makróattribútummal ellátott kódjának elemzésekor kapunk">

```rust,ignore
DeriveInput {
    // --snip--

    ident: Ident {
        ident: "Pancakes",
        span: #0 bytes(95..103)
    },
    data: Struct(
        DataStruct {
            struct_token: Struct,
            fields: Unit,
            semi_token: Some(
                Semi
            )
        }
    )
}
```

</Listing>

A struktúra mezői azt mutatják, hogy az általunk elemzett Rust kód egy
unit-szerű struktúra, amelynek `ident`-je (_identifier_, azaz azonosító, vagyis
a név) `Pancakes`. A struktúrának további mezői is vannak, amelyekkel mindenféle
Rust kód leírható; további információért nézd meg a [`syn` `DeriveInput`-ra
vonatkozó dokumentációját][syn-docs].

Hamarosan definiáljuk az `impl_hello_macro` függvényt, amelyben felépítjük a
beilleszteni kívánt új Rust kódot. Előtte azonban vedd észre, hogy a `derive`
makrónk kimenete is egy `TokenStream`. A visszaadott `TokenStream` hozzáadódik
a crate-ünk felhasználói által írt kódhoz, így amikor lefordítják a
crate-jüket, megkapják azt az extra funkcionalitást, amelyet a módosított
`TokenStream`-ben biztosítunk.

Talán észrevetted, hogy az `unwrap` meghívásával idézzük elő a
`hello_macro_derive` függvény pánikolását, ha itt a `syn::parse` függvény
hívása sikertelen. A procedurális makrónknak hiba esetén pánikolnia kell, mert a
`proc_macro_derive` függvényeknek `Result` helyett `TokenStream`-et kell
visszaadniuk, hogy megfeleljenek a procedurális makrók API-jának. A példát az
`unwrap` használatával egyszerűsítettük; éles kódban a `panic!` vagy az
`expect` segítségével konkrétabb hibaüzeneteket kell adnod arról, hogy mi
romlott el.

Most, hogy megvan a kód, amely az annotált Rust kódot `TokenStream`-ből
`DeriveInput` példánnyá alakítja, generáljuk le azt a kódot, amely az annotált
típuson megvalósítja a `HelloMacro` traitet, ahogy a 20-42. kódrészlet mutatja.

<Listing number="20-42" file-name="hello_macro_derive/src/lib.rs" caption="A `HelloMacro` trait megvalósítása az elemzett Rust kód segítségével">

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-42/hello_macro/hello_macro_derive/src/lib.rs:here}}
```

</Listing>

Az `ast.ident` segítségével egy `Ident` struktúrapéldányt kapunk, amely az
annotált típus nevét (azonosítóját) tartalmazza. A 20-41. kódrészletben látható
struktúra azt mutatja, hogy ha az `impl_hello_macro` függvényt a 20-37.
kódrészlet kódján futtatjuk, a kapott `ident` `ident` mezőjének értéke
`"Pancakes"` lesz. Így a 20-42. kódrészletben a `name` változó egy olyan
`Ident` struktúrapéldányt fog tartalmazni, amely kiírva a `"Pancakes"`
sztringet adja, vagyis a 20-37. kódrészletben szereplő struktúra nevét.

A `quote!` makróval definiálhatjuk a visszaadni kívánt Rust kódot. A fordító
mást vár, mint a `quote!` makró végrehajtásának közvetlen eredménye, ezért
`TokenStream`-mé kell alakítanunk. Ezt az `into` metódus meghívásával tesszük
meg, amely felemészti ezt a köztes reprezentációt, és a szükséges
`TokenStream` típusú értéket adja vissza.

A `quote!` makró nagyon ügyes sablonkezelési mechanizmusokat is biztosít:
beírhatjuk a `#name`-et, és a `quote!` a `name` változóban lévő értékkel
helyettesíti. Még ismétlést is végezhetünk, a szokásos makrók működéséhez
hasonlóan. Alapos bevezetésért nézd meg [a `quote` crate
dokumentációját][quote-docs].

Azt szeretnénk, hogy a procedurális makrónk legenerálja a `HelloMacro`
traitünk megvalósítását arra a típusra, amelyet a felhasználó annotált, és
amelyet a `#name` segítségével érhetünk el. A trait megvalósításának egyetlen
függvénye a `hello_macro`, amelynek törzse a biztosítani kívánt
funkcionalitást tartalmazza: kiírja a `Hello, Macro! My name is` szöveget,
majd az annotált típus nevét.

Az itt használt `stringify!` makró a Rust beépített makrója. Egy Rust
kifejezést kap, például `1 + 2`, és fordítási időben sztringliterállá alakítja,
például `"1 + 2"`. Ez különbözik a `format!` és a `println!` makrótól, amelyek
kiértékelik a kifejezést, majd az eredményt `String`-gé alakítják. Előfordulhat,
hogy a `#name` bemenet egy szó szerint kiírandó kifejezés, ezért a
`stringify!`-t használjuk. A `stringify!` használatával egy memóriafoglalást is
megspórolunk, mert a `#name`-et fordítási időben alakítjuk sztringliterállá.

Ezen a ponton a `cargo build`-nek sikeresen le kell futnia a `hello_macro`-ban
és a `hello_macro_derive`-ban is. Kapcsoljuk össze ezeket a crate-eket a 20-37.
kódrészlet kódjával, hogy működés közben lássuk a procedurális makrót! Hozz
létre egy új bináris projektet a _projects_ mappádban a `cargo new pancakes`
paranccsal. A `hello_macro`-t és a `hello_macro_derive`-ot függőségként kell
felvennünk a `pancakes` crate _Cargo.toml_ fájljába. Ha a `hello_macro` és a
`hello_macro_derive` saját változatát közzéteszed a
[crates.io](https://crates.io/)<!-- ignore --> oldalon, akkor ezek szokásos
függőségek lennének; ha nem, `path` függőségként is megadhatod őket a
következőképpen:

```toml
{{#include ../listings/ch20-advanced-features/no-listing-21-pancakes/pancakes/Cargo.toml:6:8}}
```

Írd a 20-37. kódrészlet kódját az _src/main.rs_ fájlba, és futtasd a
`cargo run` parancsot: a `Hello, Macro! My name is Pancakes!` szöveget kell
kiírnia. A procedurális makróból származó `HelloMacro` trait megvalósítás
bekerült a kódba anélkül, hogy a `pancakes` crate-nek meg kellett volna
valósítania; a `#[derive(HelloMacro)]` hozzáadta a trait megvalósítását.

Ezután nézzük meg, miben különbözik a procedurális makrók többi fajtája az
egyéni `derive` makróktól.

### Attribútumszerű makrók {#attribute-like-macros}

Az attribútumszerű makrók az egyéni `derive` makrókhoz hasonlóak, de ahelyett
hogy a `derive` attribútumhoz generálnának kódot, új attribútumok létrehozását
teszik lehetővé. Rugalmasabbak is: a `derive` csak struktúrákon és enumokon
működik, az attribútumok viszont más elemekre, például függvényekre is
alkalmazhatók. Íme egy példa egy attribútumszerű makró használatára. Tegyük fel,
hogy van egy `route` nevű attribútumod, amellyel egy webalkalmazás-keretrendszer
használatakor a függvényeket annotálod:

```rust,ignore
#[route(GET, "/")]
fn index() {
```

Ezt a `#[route]` attribútumot a keretrendszer procedurális makróként
definiálná. A makródefiníciós függvény szignatúrája így nézne ki:

```rust,ignore
#[proc_macro_attribute]
pub fn route(attr: TokenStream, item: TokenStream) -> TokenStream {
```

Itt két `TokenStream` típusú paraméterünk van. Az első az attribútum
tartalmáé: a `GET, "/"` részé. A második annak az elemnek a törzse, amelyhez az
attribútum tartozik: ebben az esetben az `fn index() {}` és a függvény
törzsének többi része.

Ettől eltekintve az attribútumszerű makrók ugyanúgy működnek, mint az egyéni
`derive` makrók: létrehozol egy `proc-macro` típusú crate-et, és megvalósítasz
egy függvényt, amely a kívánt kódot generálja!

### Függvényszerű makrók {#function-like-macros}

A függvényszerű makrók olyan makrókat definiálnak, amelyek függvényhívásnak
látszanak. A `macro_rules!` makrókhoz hasonlóan rugalmasabbak a függvényeknél;
például ismeretlen számú argumentumot fogadhatnak. A `macro_rules!` makrókat
azonban csak a korábban, a [„Deklaratív makrók általános
metaprogramozáshoz”][decl]<!-- ignore --> szakaszban tárgyalt, a `match`-hez
hasonló szintaxissal lehet definiálni. A függvényszerű makrók egy
`TokenStream` paramétert kapnak, és a definíciójuk Rust kóddal manipulálja ezt
a `TokenStream`-et, ahogy a procedurális makrók másik két fajtája is. Példa
függvényszerű makróra egy `sql!` makró, amelyet így hívhatnánk meg:

```rust,ignore
let sql = sql!(SELECT * FROM posts WHERE id=1);
```

Ez a makró elemezné a benne lévő SQL utasítást, és ellenőrizné, hogy
szintaktikailag helyes-e, ami sokkal összetettebb feldolgozás, mint amire egy
`macro_rules!` makró képes. Az `sql!` makrót így definiálnánk:

```rust,ignore
#[proc_macro]
pub fn sql(input: TokenStream) -> TokenStream {
```

Ez a definíció az egyéni `derive` makró szignatúrájához hasonló: megkapjuk a
zárójeleken belüli tokeneket, és visszaadjuk a generálni kívánt kódot.

## Összefoglalás {#summary}

Hű! Most már van néhány olyan Rust nyelvi elem az eszköztáradban, amelyet
valószínűleg nem fogsz gyakran használni, de tudni fogod, hogy nagyon speciális
körülmények között rendelkezésedre állnak. Számos összetett témát mutattunk be,
hogy amikor hibaüzenetek javaslataiban vagy mások kódjában találkozol velük,
felismerd ezeket a fogalmakat és szintaxisokat. Használd ezt a fejezetet
kézikönyvként, amely a megoldások felé vezet.

Következő lépésként mindazt, amiről a könyvben szó volt, a gyakorlatba
ültetjük, és elkészítünk még egy projektet!

[ref]: ../reference/macros-by-example.html
[tlborm]: https://veykril.github.io/tlborm/
[syn]: https://crates.io/crates/syn
[quote]: https://crates.io/crates/quote
[syn-docs]: https://docs.rs/syn/2.0/syn/struct.DeriveInput.html
[quote-docs]: https://docs.rs/quote
[decl]: #declarative-macros-with-macro_rules-for-general-metaprogramming
