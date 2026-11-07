## Az objektumorientált nyelvek jellemzői {#characteristics-of-object-oriented-languages}

A programozói közösségben nincs egyetértés abban, milyen elemekkel kell
rendelkeznie egy nyelvnek ahhoz, hogy objektumorientáltnak tekintsük. A Rustra
számos programozási paradigma hatott, köztük az OOP is; a 13. fejezetben
például a funkcionális programozásból átvett elemeket vizsgáltuk meg.
Vitatható, de az OOP-nyelvekben van néhány közös jellemző, mégpedig az
objektumok, az egységbezárás és az öröklődés. Nézzük meg, mit jelentenek ezek a
jellemzők, és támogatja-e őket a Rust!

### Az objektumok adatot és viselkedést tartalmaznak {#objects-contain-data-and-behavior}

Erich Gamma, Richard Helm, Ralph Johnson és John Vlissides _Design Patterns:
Elements of Reusable Object-Oriented Software_ című könyve (Addison-Wesley,
1994), amelyet a köznyelv csak _Gang of Four (Négyek bandája)_ könyvként
emleget, objektumorientált tervezési minták katalógusa. Az OOP-t így
definiálja:

> Az objektumorientált programok objektumokból állnak. Egy **objektum**
> egybecsomagolja az adatokat és az azokon dolgozó eljárásokat. Ezeket az
> eljárásokat jellemzően **metódusoknak** vagy **műveleteknek** nevezik.

E definíció szerint a Rust objektumorientált: a struktúrák és az enumok adatot
tartalmaznak, az `impl` blokkok pedig metódusokat biztosítanak a struktúrákhoz
és az enumokhoz. Bár a metódusokkal rendelkező struktúrákat és enumokat nem
_nevezzük_ objektumoknak, a Négyek bandájának objektumdefiníciója szerint
ugyanazt a funkcionalitást nyújtják.

### A megvalósítás részleteit elrejtő egységbezárás {#encapsulation-that-hides-implementation-details}

Az OOP-hoz gyakran társított másik szempont az _egységbezárás (encapsulation)_
gondolata, ami azt jelenti, hogy egy objektum megvalósításának részletei nem
érhetők el az objektumot használó kód számára. Így az objektummal csak a
nyilvános API-ján keresztül lehet kapcsolatba lépni; az objektumot használó
kód nem nyúlhat bele az objektum belsejébe, és nem módosíthatja közvetlenül az
adatait vagy a viselkedését. Ez lehetővé teszi, hogy a programozó
megváltoztassa és refaktorálja az objektum belsejét anélkül, hogy az
objektumot használó kódot módosítania kellene.

A 7. fejezetben megbeszéltük, hogyan szabályozhatjuk az egységbezárást: a `pub`
kulcsszóval eldönthetjük, hogy a kódunk mely moduljai, típusai, függvényei és
metódusai legyenek nyilvánosak, alapértelmezetten pedig minden más privát.
Definiálhatunk például egy `AveragedCollection` struktúrát, amelynek van egy
`i32` értékekből álló vektort tartalmazó mezője. A struktúrának lehet egy olyan
mezője is, amely a vektorban lévő értékek átlagát tartalmazza, így az átlagot
nem kell minden alkalommal kiszámolni, amikor valakinek szüksége van rá. Más
szóval az `AveragedCollection` gyorsítótárazza számunkra a kiszámított átlagot.
A 18-1. kódrészlet az `AveragedCollection` struktúra definícióját mutatja.

<Listing number="18-1" file-name="src/lib.rs" caption="Egy `AveragedCollection` struktúra, amely egész számok listáját és a gyűjtemény elemeinek átlagát tartja nyilván">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-01/src/lib.rs}}
```

</Listing>

A struktúra `pub` jelölést kapott, hogy más kód is használhassa, a benne lévő
mezők azonban privátok maradnak. Ez ebben az esetben azért fontos, mert
biztosítani szeretnénk, hogy valahányszor egy értéket hozzáadunk a listához vagy
eltávolítunk belőle, az átlag is frissüljön. Ezt úgy érjük el, hogy
megvalósítjuk az `add`, a `remove` és az `average` metódust a struktúrán, ahogy
a 18-2. kódrészlet mutatja.

<Listing number="18-2" file-name="src/lib.rs" caption="Az `add`, a `remove` és az `average` nyilvános metódus megvalósítása az `AveragedCollection` típuson">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-02/src/lib.rs:here}}
```

</Listing>

Az `add`, a `remove` és az `average` nyilvános metódus az egyetlen módja annak,
hogy egy `AveragedCollection` példány adataihoz hozzáférjünk, vagy módosítsuk
őket. Amikor az `add` metódussal hozzáadunk egy elemet a `list` mezőhöz, vagy a
`remove` metódussal eltávolítunk belőle egyet, mindkét metódus megvalósítása
meghívja a privát `update_average` metódust, amely az `average` mező
frissítéséről is gondoskodik.

A `list` és az `average` mezőt privátként hagyjuk, hogy a külső kód semmiképp
ne adhasson hozzá vagy távolíthasson el közvetlenül elemeket a `list` mezőből;
ellenkező esetben az `average` mező elszakadhatna a `list` tartalmától, amikor
az megváltozik. Az `average` metódus az `average` mező értékét adja vissza, így
a külső kód kiolvashatja az átlagot, de nem módosíthatja.

Mivel az `AveragedCollection` struktúra megvalósításának részleteit
egységbe zártuk, a jövőben könnyedén megváltoztathatunk bizonyos dolgokat,
például az adatszerkezetet. A `list` mezőhöz használhatnánk például
`Vec<i32>` helyett `HashSet<i32>`-t is. Amíg az `add`, a `remove` és az
`average` nyilvános metódus szignatúrája változatlan marad, az
`AveragedCollection` típust használó kódon nem kellene változtatni. Ha viszont
a `list` mezőt nyilvánossá tennénk, ez nem feltétlenül volna így: a
`HashSet<i32>` és a `Vec<i32>` más-más metódusokkal ad hozzá és távolít el
elemeket, így a külső kódon valószínűleg változtatni kellene, ha közvetlenül
módosítaná a `list` mezőt.

Ha az egységbezárás szükséges feltétele annak, hogy egy nyelvet
objektumorientáltnak tekintsünk, akkor a Rust megfelel ennek a
követelménynek. Az, hogy a kód különböző részeinél eldönthetjük, használjuk-e a
`pub` kulcsszót, lehetővé teszi a megvalósítás részleteinek egységbezárását.

### Az öröklődés mint típusrendszer és mint kódmegosztás {#inheritance-as-a-type-system-and-as-code-sharing}

Az _öröklődés (inheritance)_ olyan mechanizmus, amellyel egy objektum elemeket
örökölhet egy másik objektum definíciójából, így megkapja a szülőobjektum
adatait és viselkedését anélkül, hogy azokat újra definiálnod kellene.

Ha egy nyelvnek ahhoz, hogy objektumorientált legyen, rendelkeznie kell
öröklődéssel, akkor a Rust nem ilyen nyelv. Makró használata nélkül nem lehet
olyan struktúrát definiálni, amely örökli a szülőstruktúra mezőit és
metódusmegvalósításait.

Ha azonban megszoktad, hogy az öröklődés ott van a programozói eszköztáradban,
Rustban más megoldásokat is használhatsz, attól függően, hogy eredetileg miért
nyúltál volna az öröklődéshez.

Két fő oka lehet annak, hogy az öröklődést választod. Az egyik a kód
újrafelhasználása: egy adott viselkedést megvalósíthatsz egy típusra, és az
öröklődés lehetővé teszi, hogy ezt a megvalósítást egy másik típusnál is
újrahasznosítsd. Ezt Rust-kódban korlátozott módon az alapértelmezett
trait-metódusmegvalósításokkal teheted meg, amelyeket a 10-14. kódrészletben
láttál, amikor a `Summary` trait `summarize` metódusához alapértelmezett
megvalósítást adtunk. Bármely típus, amely megvalósítja a `Summary` traitet,
további kód nélkül rendelkezik a `summarize` metódussal. Ez hasonló ahhoz,
amikor egy szülőosztály tartalmazza egy metódus megvalósítását, és az öröklő
gyermekosztály is rendelkezik ezzel a megvalósítással. A `summarize` metódus
alapértelmezett megvalósítását felül is írhatjuk, amikor megvalósítjuk a
`Summary` traitet, ami ahhoz hasonló, amikor egy gyermekosztály felülírja egy
szülőosztálytól örökölt metódus megvalósítását.

Az öröklődés használatának másik oka a típusrendszerhez kapcsolódik: lehetővé
teszi, hogy egy gyermektípust ugyanott használjunk, ahol a szülőtípust. Ezt
_polimorfizmusnak (polymorphism)_ is nevezik, ami azt jelenti, hogy futásidőben
több objektumot is felcserélhetsz egymással, ha vannak bizonyos közös
jellemzőik.

> ### Polimorfizmus {#polymorphism}
>
> Sokak számára a polimorfizmus az öröklődés szinonimája. Valójában azonban ez
> egy általánosabb fogalom, amely olyan kódra utal, amely többféle típusú
> adattal is tud dolgozni. Öröklődés esetén ezek a típusok általában
> alosztályok.
>
> A Rust ehelyett generikus típusokkal absztrahál a különböző lehetséges
> típusok felett, trait-korlátokkal pedig megkötéseket ír elő arra, hogy mit
> kell ezeknek a típusoknak biztosítaniuk. Ezt néha _korlátozott parametrikus
> polimorfizmusnak (bounded parametric polymorphism)_ nevezik.

A Rust azzal, hogy nem kínál öröklődést, más kompromisszumokat választott. Az
öröklődésnél gyakran fennáll a veszélye, hogy a szükségesnél több kód lesz
közös. Az alosztályoknak nem mindig kellene a szülőosztályuk összes jellemzőjén
osztozniuk, öröklődéssel azonban ez történik. Ez kevésbé rugalmassá teheti a
program tervezését. Emellett lehetővé teszi, hogy az alosztályokon olyan
metódusokat hívjunk meg, amelyeknek nincs értelme, vagy amelyek hibát okoznak,
mert a metódusok nem illenek az alosztályra. Ráadásul egyes nyelvek csak
_egyszeres öröklődést (single inheritance)_ engednek meg (vagyis egy alosztály
csak egyetlen osztálytól örökölhet), ami tovább korlátozza a program
tervezésének rugalmasságát.

Ezen okok miatt a Rust más megközelítést választ: az öröklődés helyett trait
objektumokkal valósítja meg a futásidejű polimorfizmust. Nézzük meg, hogyan
működnek a trait objektumok!
