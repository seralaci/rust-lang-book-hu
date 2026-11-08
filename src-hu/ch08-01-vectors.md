## Értéklisták tárolása vektorokkal {#storing-lists-of-values-with-vectors}

Az első gyűjteménytípus, amelyet megnézünk, a `Vec<T>`, más néven a vektor
(vector). A vektorok lehetővé teszik, hogy egynél több értéket tárolj egyetlen
adatszerkezetben, amely az összes értéket egymás mellé helyezi a memóriában. A
vektorok csak azonos típusú értékeket tárolhatnak. Akkor hasznosak, ha elemek
listájával dolgozol, például egy fájl szövegsoraival vagy egy bevásárlókosárban
lévő termékek áraival.

### Új vektor létrehozása {#creating-a-new-vector}

Új, üres vektor létrehozásához a `Vec::new` függvényt hívjuk meg, ahogy a 8-1.
kódrészlet mutatja.

<Listing number="8-1" caption="Új, üres vektor létrehozása `i32` típusú értékek tárolására">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-01/src/main.rs:here}}
```

</Listing>

Figyeld meg, hogy itt típusannotációt adtunk meg. Mivel ebbe a vektorba nem
szúrunk be értékeket, a Rust nem tudja, milyen elemeket szeretnénk benne
tárolni. Ez fontos szempont. A vektorok generikus típusokkal vannak
megvalósítva; azt, hogyan használhatod a generikus típusokat a saját
típusaiddal, a 10. fejezetben tárgyaljuk. Egyelőre elég annyit tudnod, hogy a
standard könyvtár által biztosított `Vec<T>` típus bármilyen típust
tárolhat. Amikor egy adott típus tárolására hozunk létre vektort, a típust
kacsacsőrök között adhatjuk meg. A 8-1. kódrészletben azt mondtuk a Rustnak,
hogy a `v`-ben lévő `Vec<T>` `i32` típusú elemeket fog tárolni.

Gyakrabban fordul elő, hogy kezdőértékekkel hozol létre egy `Vec<T>`-t, és a
Rust kikövetkezteti, milyen típusú értéket szeretnél tárolni, így ritkán van
szükség erre a típusannotációra. A Rust kényelmes megoldásként a `vec!`
makrót biztosítja, amely egy olyan új vektort hoz létre, amely a megadott
értékeket tartalmazza. A 8-2. kódrészlet egy új `Vec<i32>`-t hoz létre, amely
az `1`, `2` és `3` értékeket tartalmazza. Az egész típus azért `i32`, mert ez
az alapértelmezett egész típus, ahogy azt a 3. fejezet
[„Adattípusok”][data-types]<!-- ignore --> szakaszában tárgyaltuk.

<Listing number="8-2" caption="Értékeket tartalmazó új vektor létrehozása">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-02/src/main.rs:here}}
```

</Listing>

Mivel `i32` típusú kezdőértékeket adtunk meg, a Rust ki tudja következtetni,
hogy `v` típusa `Vec<i32>`, így a típusannotáció nem szükséges. A következő
lépésben megnézzük, hogyan módosíthatunk egy vektort.

### Vektor frissítése {#updating-a-vector}

Ha létre szeretnénk hozni egy vektort, majd elemeket szeretnénk hozzáadni, a
`push` metódust használhatjuk, ahogy a 8-3. kódrészlet mutatja.

<Listing number="8-3" caption="A `push` metódus használata értékek vektorhoz adására">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-03/src/main.rs:here}}
```

</Listing>

Mint bármely változónál, ha módosítani szeretnénk az értékét, a `mut`
kulcsszóval módosíthatóvá kell tennünk, ahogy a 3. fejezetben tárgyaltuk. A
beletett számok mind `i32` típusúak, és ezt a Rust az adatokból kikövetkezteti,
így nincs szükség a `Vec<i32>` annotációra.

### Vektorelemek olvasása {#reading-elements-of-vectors}

Kétféleképpen hivatkozhatunk egy vektorban tárolt értékre: indexeléssel vagy a
`get` metódussal. A következő példákban a nagyobb érthetőség kedvéért
megadtuk az ezekből a függvényekből visszaadott értékek típusát.

A 8-4. kódrészlet a vektor egy értékének elérésére mindkét módszert bemutatja:
az indexelési szintaxist és a `get` metódust.

<Listing number="8-4" caption="Az indexelési szintaxis és a `get` metódus használata egy vektorelem elérésére">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-04/src/main.rs:here}}
```

</Listing>

Figyelj meg itt néhány részletet. A `2` indexértékkel kapjuk meg a harmadik
elemet, mert a vektorokat számokkal indexeljük, nullától kezdve. A `&` és a `[]`
használatával egy referenciát kapunk az adott indexű elemre. Ha a `get`
metódust használjuk, és argumentumként átadjuk neki az indexet, egy
`Option<&T>` értéket kapunk, amelyet a `match`-csel használhatunk.

A Rust azért biztosítja ezt a kétféle módot egy elemre való hivatkozáshoz, hogy
eldönthesd, hogyan viselkedjen a program, ha a létező elemek tartományán kívül
eső indexértéket próbálsz használni. Példaként nézzük meg, mi történik, ha van
egy ötelemű vektorunk, és mindkét módszerrel megpróbáljuk elérni a 100-as
indexű elemet, ahogy a 8-5. kódrészlet mutatja.

<Listing number="8-5" caption="Kísérlet a 100-as indexű elem elérésére egy ötelemű vektorban">

```rust,should_panic,panics
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-05/src/main.rs:here}}
```

</Listing>

Amikor lefuttatjuk ezt a kódot, az első, `[]`-t használó módszer miatt a
program pánikol, mert nem létező elemre hivatkozik. Ezt a módszert akkor
érdemes használni, ha azt szeretnéd, hogy a program összeomoljon, ha valaki a
vektor végén túli elemet próbál elérni.

Ha a `get` metódusnak a vektoron kívül eső indexet adunk át, pánik nélkül
`None`-t ad vissza. Ezt a módszert akkor használnád, ha normál körülmények
között időnként előfordulhat, hogy a vektor tartományán túli elemet érnek el. A
kódodban ekkor lesz egy logika, amely kezeli a `Some(&element)` és a `None`
esetet is, ahogy a 6. fejezetben tárgyaltuk. Az index származhat például
egy személytől, aki egy számot ír be. Ha véletlenül túl nagy számot ír be, és
a program `None` értéket kap, közölheted a felhasználóval, hány elem van a
vektorban, és adhatsz neki még egy esélyt egy érvényes érték megadására. Ez
felhasználóbarátabb lenne, mint egy elírás miatt összeomlasztani a programot!

Ha a programnak érvényes referenciája van, a kölcsönzésellenőrző (borrow
checker) betartatja a tulajdonjog és a kölcsönzés szabályait (amelyekről a 4.
fejezetben volt szó), hogy ez a referencia és a vektor tartalmára mutató
minden más referencia érvényes maradjon. Emlékezz arra a szabályra, amely
szerint ugyanabban a hatókörben nem lehet egyszerre módosítható és nem
módosítható referenciánk. Ez a szabály érvényes a 8-6. kódrészletre is, ahol a
vektor első elemére mutató nem módosítható referenciát tartunk, és közben egy
elemet próbálunk a vektor végéhez adni. Ez a program nem fog működni, ha a
függvényben később is hivatkozni próbálunk erre az elemre.

<Listing number="8-6" caption="Kísérlet egy elem vektorhoz adására, miközben egy elemére mutató referenciát tartunk">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-06/src/main.rs:here}}
```

</Listing>

A kód fordítása ezt a hibát eredményezi:

```console
{{#include ../listings/ch08-common-collections/listing-08-06/output.txt}}
```

A 8-6. kódrészlet kódja úgy tűnhet, mintha működnie kellene: miért érdekelnék
az első elemre mutató referenciát a vektor végén történő változások? A hiba a
vektorok működéséből fakad: mivel a vektorok egymás mellé helyezik az értékeket
a memóriában, egy új elem vektor végéhez adása új memória lefoglalását és a
régi elemek új helyre másolását igényelheti, ha nincs elég hely ahhoz, hogy az
összes elem egymás mellett elférjen ott, ahol a vektor jelenleg tárolva van.
Ebben az esetben az első elemre mutató referencia felszabadított memóriára
mutatna. A kölcsönzési szabályok megakadályozzák, hogy a programok ilyen
helyzetbe kerüljenek.

> Megjegyzés: A `Vec<T>` típus megvalósításának részleteiről [„The
> Rustonomicon”][nomicon] című könyvben olvashatsz bővebben.

### Iterálás a vektor értékein {#iterating-over-the-values-in-a-vector}

Ha egymás után a vektor minden elemét el szeretnénk érni, akkor ahelyett, hogy
indexekkel egyenként érnénk el őket, végigiterálunk az összes elemen. A 8-7.
kódrészlet azt mutatja, hogyan kaphatunk egy `for` ciklussal nem módosítható
referenciát egy `i32` értékeket tartalmazó vektor minden elemére, és hogyan
írathatjuk ki őket.

<Listing number="8-7" caption="Egy vektor minden elemének kiíratása az elemeken `for` ciklussal végigiterálva">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-07/src/main.rs:here}}
```

</Listing>

Egy módosítható vektor elemeire mutató módosítható referenciákon is
iterálhatunk, hogy az összes elemet megváltoztassuk. A 8-8. kódrészlet `for`
ciklusa minden elemhez hozzáad `50`-et.

<Listing number="8-8" caption="Iterálás egy vektor elemeire mutató módosítható referenciákon">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-08/src/main.rs:here}}
```

</Listing>

Ahhoz, hogy megváltoztassuk azt az értéket, amelyre a módosítható referencia
hivatkozik, a `*` dereferáló operátorral kell eljutnunk az `i`-ben lévő
értékhez, mielőtt a `+=` operátort használhatnánk. A dereferáló operátorról a
15. fejezet [„A referencia követése az értékig”][deref]<!-- ignore -->
szakaszában beszélünk részletesebben.

Egy vektoron való iterálás – akár nem módosítható, akár módosítható módon –
a kölcsönzésellenőrző szabályai miatt biztonságos. Ha a 8-7. és a 8-8.
kódrészlet `for` ciklusainak törzsében elemeket próbálnánk beszúrni vagy
eltávolítani, a 8-6. kódrészlet kódjánál kapotthoz hasonló fordítási hibát
kapnánk. A vektorra mutató referencia, amelyet a `for` ciklus tart,
megakadályozza, hogy közben az egész vektort módosítsuk.

### Több típus tárolása enummal {#using-an-enum-to-store-multiple-types}

A vektorok csak azonos típusú értékeket tárolhatnak. Ez kényelmetlen lehet;
biztosan vannak olyan esetek, amikor különböző típusú elemek listáját kell
tárolnunk. Szerencsére egy enum változatai ugyanazon enum típus alatt vannak
definiálva, így ha egyetlen típussal kell különböző típusú elemeket
képviselnünk, definiálhatunk és használhatunk egy enumot!

Tegyük fel például, hogy egy táblázat egy sorából szeretnénk értékeket
kinyerni, ahol a sor egyes oszlopai egész számokat, mások lebegőpontos
számokat, megint mások sztringeket tartalmaznak. Definiálhatunk egy enumot,
amelynek változatai a különböző értéktípusokat tárolják, és az enum összes
változata ugyanannak a típusnak számít: az enum típusának. Ezután létrehozhatunk
egy vektort, amely ezt az enumot tárolja, és így végső soron különböző
típusokat tárol. Ezt a 8-9. kódrészletben mutattuk be.

<Listing number="8-9" caption="Enum definiálása különböző típusú értékek egyetlen vektorban való tárolására">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-09/src/main.rs:here}}
```

</Listing>

A Rustnak fordítási időben tudnia kell, milyen típusok lesznek a vektorban,
hogy pontosan tudja, mennyi memóriára lesz szükség a kupacon az egyes elemek
tárolásához. Azt is egyértelműen meg kell adnunk, milyen típusok engedélyezettek
ebben a vektorban. Ha a Rust megengedné, hogy egy vektor bármilyen típust
tároljon, fennállna az esélye, hogy egy vagy több típus hibát okoz a vektor
elemein végzett műveletek során. Az enum és a `match` kifejezés együttes
használata azt jelenti, hogy a Rust fordítási időben biztosítja, hogy minden
lehetséges esetet kezeljünk, ahogy a 6. fejezetben tárgyaltuk.

Ha nem ismered azoknak a típusoknak a teljes körét, amelyeket a program
futásidőben kap és egy vektorban kell tárolnia, az enumos módszer nem működik.
Ehelyett trait objektumot használhatsz, amelyet a 18. fejezetben tárgyalunk.

Most, hogy áttekintettük a vektorok néhány leggyakoribb használati módját,
mindenképp nézd meg [az API-dokumentációt][vec-api]<!-- ignore --> a standard
könyvtár által a `Vec<T>`-n definiált sok hasznos metódusért. A `push` mellett
például van egy `pop` metódus is, amely eltávolítja és visszaadja az utolsó
elemet.

### A vektor eldobása az elemeit is eldobja {#dropping-a-vector-drops-its-elements}

Mint bármely más `struct`, a vektor is felszabadul, amikor kikerül a
hatókörből, ahogy a 8-10. kódrészlet megjegyzései mutatják.

<Listing number="8-10" caption="Annak bemutatása, hol dobódik el a vektor és az elemei">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-10/src/main.rs:here}}
```

</Listing>

Amikor a vektor eldobódik, a teljes tartalma is eldobódik, vagyis a benne
tárolt egész számok is felszabadulnak. A kölcsönzésellenőrző biztosítja, hogy a
vektor tartalmára mutató referenciákat csak addig használjuk, amíg maga a
vektor érvényes.

Térjünk át a következő gyűjteménytípusra: a `String`-re!

[data-types]: ch03-02-data-types.html#data-types
[nomicon]: https://doc.rust-lang.org/nomicon/vec/vec.html
[vec-api]: https://doc.rust-lang.org/std/vec/struct.Vec.html
[deref]: ch15-02-deref.html#following-the-pointer-to-the-value-with-the-dereference-operator
