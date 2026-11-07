## Kulcsok és hozzájuk tartozó értékek tárolása hasítótáblákban {#storing-keys-with-associated-values-in-hash-maps}

Gyakori gyűjteményeink közül az utolsó a hasítótábla (hash map). A
`HashMap<K, V>` típus `K` típusú kulcsok és `V` típusú értékek közötti
megfeleltetést tárol egy _hasítófüggvény (hashing function)_ segítségével,
amely meghatározza, hogyan helyezi el ezeket a kulcsokat és értékeket a
memóriában. Sok programozási nyelv támogatja ezt az adatszerkezetet, de
gyakran más néven, például _hash_, _map_, _object_, _hash table_,
_dictionary_ vagy _associative array_ néven, hogy csak néhányat említsünk.

A hasítótáblák akkor hasznosak, ha az adatokat nem index alapján szeretnéd
kikeresni, ahogy a vektoroknál, hanem egy kulcs alapján, amely bármilyen
típusú lehet. Egy játékban például egy hasítótáblában tarthatod nyilván az
egyes csapatok pontszámát, ahol minden kulcs egy csapat neve, az értékek pedig
az egyes csapatok pontszámai. Egy csapatnév alapján lekérdezheted a csapat
pontszámát.

Ebben a szakaszban a hasítótáblák alapvető API-ját nézzük át, de a standard
könyvtár által a `HashMap<K, V>`-n definiált függvényekben még sok hasznos
dolog rejlik. Mint mindig, további információkért nézd meg a standard könyvtár
dokumentációját.

### Új hasítótábla létrehozása {#creating-a-new-hash-map}

Üres hasítótáblát például úgy hozhatunk létre, hogy a `new` függvényt
használjuk, és az `insert` metódussal adunk hozzá elemeket. A 8-20.
kódrészletben két csapat pontszámát tartjuk nyilván, amelyek neve _Blue_ (kék)
és _Yellow_ (sárga). A kék csapat 10 ponttal, a sárga csapat 50 ponttal indul.

<Listing number="8-20" caption="Új hasítótábla létrehozása és néhány kulcs és érték beszúrása">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-20/src/main.rs:here}}
```

</Listing>

Figyeld meg, hogy előbb a `use` segítségével be kell hoznunk a `HashMap`-et a
standard könyvtár gyűjteményekkel foglalkozó részéből. A három gyakori
gyűjteményünk közül ezt használják a legritkábban, ezért nincs benne azokban a
nyelvi elemekben, amelyeket a prelude automatikusan hatókörbe hoz. A
hasítótáblákat a standard könyvtár is kevésbé támogatja; például nincs beépített
makró a létrehozásukra.

A vektorokhoz hasonlóan a hasítótáblák is a kupacon tárolják az adataikat. Ennek
a `HashMap`-nek `String` típusú kulcsai és `i32` típusú értékei vannak. A
vektorokhoz hasonlóan a hasítótáblák is homogének: az összes kulcsnak azonos
típusúnak kell lennie, és az összes értéknek is azonos típusúnak kell lennie.

### Értékek elérése egy hasítótáblában {#accessing-values-in-a-hash-map}

Egy értéket úgy kaphatunk meg a hasítótáblából, hogy a kulcsát átadjuk a `get`
metódusnak, ahogy a 8-21. kódrészlet mutatja.

<Listing number="8-21" caption="A hasítótáblában tárolt, kék csapathoz tartozó pontszám elérése">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-21/src/main.rs:here}}
```

</Listing>

Itt a `score` a kék csapathoz tartozó értéket kapja, az eredmény pedig `10`
lesz. A `get` metódus egy `Option<&V>` értéket ad vissza; ha a hasítótáblában
nincs érték az adott kulcshoz, a `get` `None`-t ad vissza. Ez a program úgy
kezeli az `Option`-t, hogy meghívja a `copied` metódust, hogy `Option<&i32>`
helyett `Option<i32>` értéket kapjon, majd az `unwrap_or` metódust, hogy a
`score` értékét nullára állítsa, ha a `scores` nem tartalmaz bejegyzést (entry)
az adott kulcshoz.

A hasítótábla minden kulcs-érték párján a vektorokhoz hasonló módon,
egy `for` ciklussal iterálhatunk végig:

```rust
{{#rustdoc_include ../listings/ch08-common-collections/no-listing-03-iterate-over-hashmap/src/main.rs:here}}
```

Ez a kód tetszőleges sorrendben írja ki az egyes párokat:

```text
Yellow: 50
Blue: 10
```

<!-- Old headings. Do not remove or links may break. -->

<a id="hash-maps-and-ownership"></a>

### A tulajdonjog kezelése hasítótáblákban {#managing-ownership-in-hash-maps}

A `Copy` traitet megvalósító típusok, például az `i32` esetén az értékek
bemásolódnak a hasítótáblába. A saját tulajdonú (owned) értékeknél, például a
`String` esetén, az értékek mozgatással kerülnek be, és a hasítótábla lesz ezek
tulajdonosa, ahogy a 8-22. kódrészlet mutatja.

<Listing number="8-22" caption="Annak bemutatása, hogy a kulcsok és az értékek a beszúrás után a hasítótábla tulajdonába kerülnek">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-22/src/main.rs:here}}
```

</Listing>

A `field_name` és a `field_value` változót nem használhatjuk azután, hogy az
`insert` hívásával bemozgattuk őket a hasítótáblába.

Ha értékekre mutató referenciákat szúrunk be a hasítótáblába, az értékek nem
kerülnek át a hasítótáblába. Azoknak az értékeknek, amelyekre a referenciák
mutatnak, legalább addig érvényesnek kell maradniuk, ameddig a hasítótábla
érvényes. Ezekről a kérdésekről a 10. fejezet [„Referenciák ellenőrzése
élettartamokkal”][validating-references-with-lifetimes]<!-- ignore -->
szakaszában beszélünk bővebben.

### Hasítótábla frissítése {#updating-a-hash-map}

Bár a kulcs-érték párok száma növelhető, minden egyedi kulcshoz egyszerre csak
egy érték tartozhat (fordítva viszont ez nem igaz: például a kék és a sárga
csapathoz is tartozhat egyaránt `10` érték a `scores` hasítótáblában).

Ha módosítani szeretnéd egy hasítótábla adatait, el kell döntened, hogyan
kezeld azt az esetet, amikor egy kulcshoz már tartozik érték. Lecserélheted a
régi értéket az újra, teljesen figyelmen kívül hagyva a régit. Megtarthatod a
régi értéket, és figyelmen kívül hagyhatod az újat, vagyis csak akkor adod
hozzá az új értéket, ha a kulcshoz _még nem_ tartozik érték. Vagy
egyesítheted a régi és az új értéket. Nézzük meg, hogyan valósíthatjuk meg
ezeket!

#### Érték felülírása {#overwriting-a-value}

Ha beszúrunk egy kulcsot és egy értéket egy hasítótáblába, majd ugyanazt a
kulcsot egy másik értékkel is beszúrjuk, a kulcshoz tartozó érték lecserélődik.
Bár a 8-23. kódrészlet kódja kétszer hívja meg az `insert` metódust, a
hasítótábla csak egyetlen kulcs-érték párt fog tartalmazni, mert mindkét
alkalommal a kék csapat kulcsához szúrjuk be az értéket.

<Listing number="8-23" caption="Egy adott kulccsal tárolt érték lecserélése">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-23/src/main.rs:here}}
```

</Listing>

Ez a kód a `{"Blue": 25}` szöveget írja ki. Az eredeti `10` érték felülíródott.

<!-- Old headings. Do not remove or links may break. -->

<a id="only-inserting-a-value-if-the-key-has-no-value"></a>

#### Kulcs és érték hozzáadása csak akkor, ha a kulcs még nincs benne {#adding-a-key-and-value-only-if-a-key-isnt-present}

Gyakori, hogy megvizsgáljuk, létezik-e már egy adott kulcs értékkel a
hasítótáblában, majd a következőképpen járunk el: ha a kulcs létezik a
hasítótáblában, a meglévő érték maradjon változatlan; ha a kulcs nem létezik,
szúrjuk be a kulcsot és egy hozzá tartozó értéket.

A hasítótábláknak erre egy külön API-juk van, az `entry`, amely paraméterként a
vizsgálandó kulcsot kapja. Az `entry` metódus visszatérési értéke egy `Entry`
nevű enum, amely egy olyan értéket képvisel, amely vagy létezik, vagy nem.
Tegyük fel, hogy meg szeretnénk vizsgálni, tartozik-e érték a sárga csapat
kulcsához. Ha nem, az `50` értéket szeretnénk beszúrni, és ugyanígy a kék
csapatnál is. Az `entry` API használatával a kód a 8-24. kódrészlethez hasonlóan
néz ki.

<Listing number="8-24" caption="Az `entry` metódus használata, hogy csak akkor szúrjunk be, ha a kulcshoz még nem tartozik érték">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-24/src/main.rs:here}}
```

</Listing>

Az `Entry` `or_insert` metódusa úgy van definiálva, hogy ha a megfelelő `Entry`
kulcs létezik, a hozzá tartozó értékre mutató módosítható referenciát adja
vissza; ha pedig nem létezik, a paraméterét beszúrja a kulcs új értékeként, és
az új értékre mutató módosítható referenciát adja vissza. Ez a módszer sokkal
áttekinthetőbb, mint ha magunk írnánk meg a logikát, ráadásul jobban
együttműködik a kölcsönzésellenőrzővel.

A 8-24. kódrészlet kódjának futtatása a `{"Yellow": 50, "Blue": 10}` szöveget
írja ki. Az `entry` első hívása beszúrja a sárga csapat kulcsát az `50`
értékkel, mert a sárga csapatnak még nincs értéke. Az `entry` második hívása
nem változtat a hasítótáblán, mert a kék csapatnak már van értéke, a `10`.

#### Érték frissítése a régi érték alapján {#updating-a-value-based-on-the-old-value}

A hasítótáblák másik gyakori felhasználási módja, hogy kikeresünk egy
kulcshoz tartozó értéket, majd a régi érték alapján frissítjük. A 8-25.
kódrészlet például olyan kódot mutat, amely megszámolja, hogy egy szövegben
az egyes szavak hányszor fordulnak elő. Egy hasítótáblát használunk, amelynek a
szavak a kulcsai, és az értéket növeljük, hogy nyilvántartsuk, hányszor láttuk
az adott szót. Ha egy szót először látunk, előbb a `0` értéket szúrjuk be.

<Listing number="8-25" caption="Szavak előfordulásainak megszámolása egy szavakat és darabszámokat tároló hasítótáblával">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-25/src/main.rs:here}}
```

</Listing>

Ez a kód a `{"world": 2, "hello": 1, "wonderful": 1}` szöveget írja ki.
Előfordulhat, hogy ugyanezeket a kulcs-érték párokat más sorrendben látod
kiírva: emlékezz az
[„Értékek elérése egy hasítótáblában”][access]<!-- ignore --> szakaszból, hogy a
hasítótáblán való iterálás tetszőleges sorrendben történik.

A `split_whitespace` metódus egy iterátort ad vissza a `text` értékének
szóközökkel elválasztott részszeletein. Az `or_insert` metódus a megadott
kulcshoz tartozó értékre mutató módosítható referenciát (`&mut V`) ad vissza.
Itt ezt a módosítható referenciát a `count` változóban tároljuk, így ahhoz,
hogy értéket adhassunk neki, előbb a csillaggal (`*`) dereferálnunk kell a
`count`-ot. A módosítható referencia a `for` ciklus végén kikerül a
hatókörből, így ezek a változtatások mind biztonságosak, és a kölcsönzési
szabályok megengedik őket.

### Hasítófüggvények {#hashing-functions}

A `HashMap` alapértelmezés szerint egy _SipHash_ nevű hasítófüggvényt használ,
amely ellenállóvá tehet a hasítótáblákat érintő szolgáltatásmegtagadásos
(denial-of-service, DoS) támadásokkal szemben[^siphash]<!-- ignore -->. Ez nem
a leggyorsabb elérhető hasítóalgoritmus, de a nagyobb biztonságért cserébe
megéri a teljesítménycsökkenést. Ha profilozod a kódodat, és azt tapasztalod,
hogy az alapértelmezett hasítófüggvény túl lassú a céljaidhoz, egy másik
hasítóval (hasher) átválthatsz egy másik függvényre. A _hasító (hasher)_ egy
olyan típus, amely megvalósítja a `BuildHasher` traitet. A traitekről és a
megvalósításukról a [10. fejezetben][traits]<!-- ignore --> beszélünk. Nem
feltétlenül kell a saját hasítódat a nulláról megírnod; a
[crates.io](https://crates.io/)<!-- ignore --> oldalon más Rust-felhasználók
által megosztott könyvtárakat találsz, amelyek számos gyakori hasítóalgoritmust
megvalósító hasítókat kínálnak.

[^siphash]: [https://en.wikipedia.org/wiki/SipHash](https://en.wikipedia.org/wiki/SipHash)

## Összefoglalás {#summary}

A vektorok, a sztringek és a hasítótáblák rengeteg olyan funkciót biztosítanak,
amelyekre a programokban szükség van, amikor adatokat kell tárolni, elérni és
módosítani. Íme néhány feladat, amelynek a megoldásához most már
felkészült vagy:

1. Egy egész számokból álló lista esetén egy vektor segítségével add vissza a
   lista mediánját (rendezés után a középső helyen álló értéket) és móduszát
   (a leggyakrabban előforduló értéket; ehhez jól jön egy hasítótábla).
1. Alakíts át sztringeket „disznó latin” (Pig Latin) nyelvre. Minden szó első
   mássalhangzója a szó végére kerül, és hozzá kapcsolódik az _ay_, így a
   _first_ szóból _irst-fay_ lesz. A magánhangzóval kezdődő szavak végére
   ehelyett a _hay_ kerül (az _apple_ szóból _apple-hay_ lesz). Tartsd észben
   az UTF-8 kódolás részleteit!
1. Egy hasítótábla és vektorok segítségével készíts egy szöveges felületet,
   amelyen a felhasználó dolgozói neveket adhat hozzá egy cég egyik
   részlegéhez; például „Add Sally to Engineering” vagy „Add Amir to Sales”.
   Ezután tedd lehetővé, hogy a felhasználó lekérdezhesse egy részleg összes
   dolgozójának listáját, vagy a cég összes dolgozóját részlegenként,
   ábécérendbe rendezve.

A standard könyvtár API-dokumentációja leírja a vektorok, a sztringek és a
hasítótáblák metódusait, amelyek hasznosak lesznek ezekhez a feladatokhoz!

Egyre összetettebb programokhoz érkezünk, amelyekben a műveletek sikertelenek
is lehetnek, így tökéletes alkalom ez arra, hogy a hibakezelésről beszéljünk.
Ezt tesszük a következő fejezetben!

[validating-references-with-lifetimes]: ch10-03-lifetime-syntax.html#validating-references-with-lifetimes
[access]: #accessing-values-in-a-hash-map
[traits]: ch10-02-traits.html
