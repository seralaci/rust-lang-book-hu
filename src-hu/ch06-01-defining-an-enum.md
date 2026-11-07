## Enum definiálása {#defining-an-enum}

Míg a struktúrákkal összetartozó mezőket és adatokat csoportosíthatsz – például
egy `Rectangle`-t a `width` és `height` értékével –, az enumokkal azt fejezheted
ki, hogy egy érték egy adott értékhalmaz egyik eleme. Mondhatjuk például, hogy
a `Rectangle` a lehetséges alakzatok egyike, amelyek közé a `Circle` és a
`Triangle` is tartozik. Ehhez a Rust lehetővé teszi, hogy ezeket a
lehetőségeket egy enumként kódoljuk.

Nézzünk meg egy helyzetet, amelyet kódban szeretnénk kifejezni, és lássuk, miért
hasznosak az enumok, és miért alkalmasabbak ebben az esetben a struktúráknál!
Tegyük fel, hogy IP-címekkel kell dolgoznunk. Jelenleg két fő szabvány létezik
az IP-címekre: a négyes és a hatos verzió. Mivel a programunk csak ezzel a két
IP-cím-fajtával fog találkozni, az összes lehetséges változatot _felsorolhatjuk
(enumerate)_ – innen kapta a nevét a felsorolás típus (enumeration).

Bármely IP-cím vagy négyes, vagy hatos verziójú lehet, de egyszerre a kettő nem.
Az IP-címeknek ez a tulajdonsága teszi alkalmassá rájuk az enum adatszerkezetet,
mert egy enum értéke mindig csak az egyik változata lehet. A négyes és a hatos
verziójú címek alapvetően mégis mindketten IP-címek, ezért ugyanazon típusként
kell kezelni őket, amikor a kód bármilyen IP-címre érvényes helyzetekkel
foglalkozik.

Ezt a fogalmat kódban úgy fejezhetjük ki, hogy definiálunk egy `IpAddrKind`
enumot, és felsoroljuk benne, milyen fajtájú lehet egy IP-cím: `V4` és `V6`.
Ezek az enum változatai (variants):

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-01-defining-enums/src/main.rs:def}}
```

Az `IpAddrKind` most már egy saját adattípus, amelyet a kódunk más részeiben is
használhatunk.

### Enum értékek {#enum-values}

Az `IpAddrKind` két változatának egy-egy példányát így hozhatjuk létre:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-01-defining-enums/src/main.rs:instance}}
```

Figyeld meg, hogy az enum változatai az enum azonosítójának névterében vannak,
és a kettőt dupla kettősponttal választjuk el egymástól. Ez azért hasznos, mert
így az `IpAddrKind::V4` és az `IpAddrKind::V6` érték is ugyanolyan típusú:
`IpAddrKind`. Ezután például definiálhatunk egy függvényt, amely bármilyen
`IpAddrKind` értéket elfogad:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-01-defining-enums/src/main.rs:fn}}
```

Ezt a függvényt pedig bármelyik változattal meghívhatjuk:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-01-defining-enums/src/main.rs:fn_call}}
```

Az enumok használatának ennél is több előnye van. Ha tovább gondolkodunk az
IP-cím típusunkon, jelenleg nincs módunk a tényleges IP-cím _adatainak_
tárolására; csak azt tudjuk, milyen _fajtájú_ a cím. Mivel az 5. fejezetben
épp most ismerkedtél meg a struktúrákkal, kézenfekvőnek tűnhet, hogy a
problémát struktúrákkal oldd meg, ahogy a 6-1. kódrészlet mutatja.

<Listing number="6-1" caption="Egy IP-cím adatainak és `IpAddrKind` változatának tárolása `struct` segítségével">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-01/src/main.rs:here}}
```

</Listing>

Itt egy `IpAddr` struktúrát definiáltunk, amelynek két mezője van: egy
`IpAddrKind` típusú (a korábban definiált enum) `kind` mező és egy `String`
típusú `address` mező. A struktúrának két példánya van. Az első a `home`,
amelynek `kind` értéke `IpAddrKind::V4`, a hozzá tartozó címadat pedig
`127.0.0.1`. A második példány a `loopback`. Ennek `kind` értéke az `IpAddrKind`
másik változata, a `V6`, a hozzá tartozó cím pedig `::1`. Egy struktúrával
fogtuk össze a `kind` és az `address` értéket, így a változat most már az
értékhez kapcsolódik.

Ugyanezt a fogalmat azonban tömörebben is ábrázolhatjuk pusztán egy enummal:
ahelyett, hogy egy enumot egy struktúrába tennénk, az adatokat közvetlenül az
enum egyes változataiba helyezhetjük. Az `IpAddr` enum alábbi új definíciója
szerint a `V4` és a `V6` változathoz is egy-egy `String` érték tartozik:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-02-enum-with-data/src/main.rs:here}}
```

Az adatokat közvetlenül az enum egyes változataihoz csatoljuk, így nincs
szükség külön struktúrára. Itt az enumok működésének egy másik részlete is
jobban látszik: minden általunk definiált enumváltozat neve egyben egy olyan
függvény is lesz, amely az enum egy példányát hozza létre. Vagyis az
`IpAddr::V4()` egy függvényhívás, amely egy `String` argumentumot vár, és egy
`IpAddr` típusú példányt ad vissza. Ezt a konstruktorfüggvényt az enum
definiálásával automatikusan megkapjuk.

Van még egy előnye annak, ha struktúra helyett enumot használunk: az egyes
változatokhoz különböző típusú és mennyiségű adat tartozhat. A négyes verziójú
IP-címek mindig négy számkomponensből állnak, amelyek értéke 0 és 255 közé
esik. Ha a `V4` címeket négy `u8` értékként szeretnénk tárolni, a `V6` címeket
viszont továbbra is egyetlen `String` értékként kifejezni, azt egy struktúrával
nem tudnánk megtenni. Az enumok ezt az esetet könnyedén kezelik:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-03-variants-with-different-data/src/main.rs:here}}
```

Több különböző módot is bemutattunk arra, hogyan definiálhatunk
adatszerkezeteket a négyes és hatos verziójú IP-címek tárolására. Kiderül
azonban, hogy az IP-címek tárolása és fajtájuk kódolása annyira gyakori igény,
hogy [a standard könyvtárban van egy definíció, amelyet
használhatunk!][IpAddr]<!-- ignore --> Nézzük meg, hogyan definiálja a
standard könyvtár az `IpAddr`-t! Pontosan
ugyanaz az enum és ugyanazok a változatok szerepelnek benne, amelyeket mi is
definiáltunk és használtunk, de a címadatokat két különböző struktúra formájában
ágyazza be a változatokba, és ezek a struktúrák változatonként eltérően vannak
definiálva:

```rust
struct Ipv4Addr {
    // --snip--
}

struct Ipv6Addr {
    // --snip--
}

enum IpAddr {
    V4(Ipv4Addr),
    V6(Ipv6Addr),
}
```

Ez a kód azt szemlélteti, hogy egy enumváltozatba bármilyen adatot tehetsz:
például sztringeket, numerikus típusokat vagy struktúrákat. Akár egy másik
enumot is! Emellett a standard könyvtár típusai gyakran nem sokkal
bonyolultabbak annál, amit te magad is kitalálhatnál.

Figyeld meg, hogy bár a standard könyvtár tartalmazza az `IpAddr` definícióját,
a saját definíciónkat ütközés nélkül létrehozhatjuk és használhatjuk, mert a
standard könyvtár definícióját nem hoztuk be a hatókörünkbe. A típusok
hatókörbe hozásáról a 7. fejezetben lesz bővebben szó.

Nézzünk meg egy másik példát is enumra a 6-2. kódrészletben: ennek a
változataiba sokféle típus van beágyazva.

<Listing number="6-2" caption="Egy `Message` enum, amelynek változatai különböző mennyiségű és típusú értéket tárolnak">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-02/src/main.rs:here}}
```

</Listing>

Ennek az enumnak négy, különböző típusú változata van:

- `Quit`: Egyáltalán nem tartozik hozzá adat
- `Move`: Elnevezett mezői vannak, ahogy egy struktúrának
- `Write`: Egyetlen `String` értéket tartalmaz
- `ChangeColor`: Három `i32` értéket tartalmaz

Egy olyan enum definiálása, amilyen a 6-2. kódrészletben látható, hasonlít
különböző fajta struktúrák definiálásához, azzal a különbséggel, hogy az enum
nem használja a `struct` kulcsszót, és az összes változat a `Message` típus alá
van csoportosítva. Az alábbi struktúrák ugyanazokat az adatokat tárolhatnák,
mint az előző enum változatai:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-04-structs-similar-to-message-enum/src/main.rs:here}}
```

Ha azonban a különböző struktúrákat használnánk, amelyek mindegyike saját
típussal rendelkezik, nem tudnánk olyan könnyen definiálni egy függvényt, amely
bármelyik ilyen üzenetfajtát elfogadja, mint a 6-2. kódrészletben definiált
`Message` enum esetén, amely egyetlen típus.

Van még egy hasonlóság az enumok és a struktúrák között: ahogy a struktúrákon
az `impl` segítségével metódusokat definiálhatunk, ugyanúgy az enumokon is.
Íme egy `call` nevű metódus, amelyet a `Message` enumunkon definiálhatnánk:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-05-methods-on-enums/src/main.rs:here}}
```

A metódus törzse a `self` segítségével éri el azt az értéket, amelyen a
metódust meghívtuk. Ebben a példában létrehoztunk egy `m` változót, amelynek
értéke `Message::Write(String::from("hello"))`, és a `call` metódus törzsében
a `self` ez lesz, amikor az `m.call()` lefut.

Nézzünk meg a standard könyvtárban egy másik enumot, amely nagyon gyakori és
hasznos: az `Option`-t.

<!-- Old headings. Do not remove or links may break. -->

<a id="the-option-enum-and-its-advantages-over-null-values"></a>

### Az `Option` enum {#the-option-enum}

Ez a szakasz esettanulmányként az `Option`-t vizsgálja, amely a standard
könyvtár egy másik enumja. Az `Option` típus azt a nagyon gyakori helyzetet
kódolja, amikor egy érték lehet valami, de lehet semmi is.

Ha például egy nem üres lista első elemét kéred, egy értéket kapsz. Ha egy üres
lista első elemét kéred, semmit sem kapsz. Ha ezt a fogalmat a típusrendszer
eszközeivel fejezzük ki, a fordító ellenőrizni tudja, hogy minden szükséges
esetet kezeltél-e; ez a funkció olyan hibákat előzhet meg, amelyek más
programozási nyelvekben rendkívül gyakoriak.

A programozási nyelvek tervezéséről gyakran annak alapján gondolkodunk, hogy
milyen nyelvi elemeket tartalmaznak, de az is fontos, mit hagyunk ki. A Rustban
nincs meg a null, amely sok más nyelvben megtalálható. A _null_ egy olyan érték,
amely azt jelenti, hogy ott nincs érték. A nullt ismerő nyelvekben a változók
mindig két állapot egyikében lehetnek: null vagy nem null.

Tony Hoare, a null feltalálója, 2009-es „Null References: The Billion Dollar
Mistake” (Null referenciák: a milliárd dolláros hiba) című előadásában ezt
mondta:

> Ez az én milliárd dolláros hibám. Akkoriban egy objektumorientált nyelv
> referenciáinak első átfogó típusrendszerét terveztem. A célom az volt, hogy a
> referenciák minden használata teljesen biztonságos legyen, és ezt a fordító
> automatikusan ellenőrizze. De nem tudtam ellenállni a kísértésnek, hogy
> beletegyem a null referenciát, egyszerűen azért, mert olyan könnyű volt
> megvalósítani. Ez számtalan hibához, sebezhetőséghez és rendszerösszeomláshoz
> vezetett, amelyek az elmúlt negyven évben valószínűleg milliárd dollárnyi
> fejfájást és kárt okoztak.

A null értékekkel az a gond, hogy ha egy null értéket nem null értékként
próbálsz használni, valamilyen hibát kapsz. Mivel ez a null vagy nem null
tulajdonság mindenütt jelen van, rendkívül könnyű ilyen hibát elkövetni.

Maga a fogalom azonban, amelyet a null kifejezni próbál, továbbra is hasznos: a
null egy olyan érték, amely valamilyen okból jelenleg érvénytelen vagy hiányzik.

A probléma valójában nem a fogalommal, hanem a konkrét megvalósítással van.
Ezért a Rustban nincs null, viszont van egy enum, amely azt a fogalmat kódolja,
hogy egy érték jelen van vagy hiányzik. Ez az enum az `Option<T>`, amelyet [a
standard könyvtár][option]<!-- ignore --> a következőképpen definiál:

```rust
enum Option<T> {
    None,
    Some(T),
}
```

Az `Option<T>` enum annyira hasznos, hogy még a prelude is tartalmazza; nem kell
kifejezetten hatókörbe hoznod. A változatai is benne vannak a prelude-ban: a
`Some` és a `None` közvetlenül, `Option::` előtag nélkül is használható. Az
`Option<T>` enum ettől még csak egy közönséges enum, a `Some(T)` és a `None`
pedig továbbra is az `Option<T>` típus változatai.

A `<T>` szintaxis a Rust egy olyan nyelvi eleme, amelyről még nem beszéltünk.
Ez egy generikus típusparaméter; a generikus típusokkal részletesebben a 10.
fejezetben foglalkozunk. Egyelőre elég annyit tudnod, hogy a `<T>` azt jelenti,
hogy az `Option` enum `Some` változata bármilyen típusú adatból egyet
tárolhat, és minden konkrét típus, amelyet a `T` helyén használunk, az
`Option<T>` típust egy másik típussá teszi. Íme néhány példa arra, hogyan
tárolhatunk `Option` értékekben szám- és karaktertípusokat:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-06-option-examples/src/main.rs:here}}
```

A `some_number` típusa `Option<i32>`. A `some_char` típusa `Option<char>`, ami
egy másik típus. A Rust ki tudja következtetni ezeket a típusokat, mert a
`Some` változaton belül megadtunk egy értéket. Az `absent_number` esetén
viszont a Rust megköveteli, hogy annotáljuk a teljes `Option` típust: a fordító
pusztán egy `None` értékből nem tudja kikövetkeztetni, milyen típusú értéket
tárolna a megfelelő `Some` változat. Itt közöljük a Rusttal, hogy az
`absent_number` típusát `Option<i32>`-nek szánjuk.

Ha `Some` értékünk van, tudjuk, hogy van érték, és ez az érték a `Some`-ban
található. Ha `None` értékünk van, az bizonyos értelemben ugyanazt jelenti,
mint a null: nincs érvényes értékünk. Akkor hát miért jobb az `Option<T>`, mint
a null?

Röviden: mivel az `Option<T>` és a `T` (ahol a `T` bármilyen típus lehet)
különböző típusok, a fordító nem engedi, hogy egy `Option<T>` értéket úgy
használjunk, mintha biztosan érvényes érték lenne. Ez a kód például nem
fordul le, mert egy `i8` értéket próbál hozzáadni egy `Option<i8>` értékhez:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-07-cant-use-option-directly/src/main.rs:here}}
```

Ha lefuttatjuk ezt a kódot, egy ehhez hasonló hibaüzenetet kapunk:

```console
{{#include ../listings/ch06-enums-and-pattern-matching/no-listing-07-cant-use-option-directly/output.txt}}
```

Durva! Ez a hibaüzenet lényegében azt jelenti, hogy a Rust nem tudja, hogyan
adjon össze egy `i8` és egy `Option<i8>` értéket, mert ezek különböző típusok.
Ha a Rustban egy olyan típusú értékünk van, mint az `i8`, a fordító biztosítja,
hogy mindig érvényes értékünk legyen. Magabiztosan haladhatunk tovább anélkül,
hogy az érték használata előtt ellenőriznünk kellene, nem null-e. Csak akkor
kell aggódnunk amiatt, hogy esetleg nincs értékünk, ha `Option<i8>` (vagy
akármilyen típusú, éppen használt `Option`) értékünk van, és a fordító
gondoskodik róla, hogy ezt az esetet az érték használata előtt kezeljük.

Más szóval egy `Option<T>` értéket `T` értékké kell alakítanod, mielőtt `T`
műveleteket végezhetnél vele. Ez általában segít elkapni a null egyik
leggyakoribb problémáját: azt, hogy valamiről azt feltételezzük, hogy nem null,
pedig valójában az.

Ha megszűnik annak a kockázata, hogy tévesen nem null értéket feltételezel,
magabiztosabb lehetsz a kódodban. Ahhoz, hogy egy érték esetleg null lehessen,
kifejezetten jelezned kell ezt azzal, hogy az érték típusát `Option<T>`-nek adod
meg. Ezután az érték használatakor kötelezően, kifejezetten kezelned kell azt az
esetet, amikor az érték null. Mindenhol, ahol egy érték típusa nem `Option<T>`,
_igenis_ nyugodtan feltételezheted, hogy az érték nem null. Ez a Rust tudatos
tervezési döntése volt, hogy korlátozza a null elterjedtségét, és növelje a
Rust-kód biztonságát.

Hogyan juthatsz hozzá tehát egy `Some` változatban lévő `T` értékhez, ha egy
`Option<T>` típusú értéked van, hogy használni tudd? Az `Option<T>` enumnak
rengeteg metódusa van, amelyek sokféle helyzetben hasznosak; ezeket [a
dokumentációjában][docs]<!-- ignore --> nézheted meg. Az `Option<T>`
metódusainak megismerése rendkívül hasznos lesz a Rusttal való utazásod során.

Általában ahhoz, hogy egy `Option<T>` értéket használj, olyan kódra van
szükséged, amely minden változatot kezel. Kell egy kód, amely csak akkor fut,
ha `Some(T)` értéked van, és ez a kód használhatja a belső `T` értéket. Kell egy
másik kód is, amely csak akkor fut, ha `None` értéked van, és ennek a kódnak
nincs elérhető `T` értéke. A `match` kifejezés egy olyan vezérlési szerkezet,
amely enumokkal használva pontosan ezt teszi: attól függően futtat különböző
kódot, hogy az enum melyik változatát kapja, és ez a kód használhatja az
illeszkedő értékben lévő adatokat.

[IpAddr]: ../std/net/enum.IpAddr.html
[option]: ../std/option/enum.Option.html
[docs]: ../std/option/enum.Option.html
