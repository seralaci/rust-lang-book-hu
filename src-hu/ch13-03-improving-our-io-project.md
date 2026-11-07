## Az I/O projektünk továbbfejlesztése {#improving-our-io-project}

Az iterátorokról szerzett új tudásunkkal továbbfejleszthetjük a 12. fejezet
I/O projektjét: iterátorok segítségével a kód egyes részeit világosabbá és
tömörebbé tehetjük. Nézzük meg, hogyan javíthatják az iterátorok a
`Config::build` és a `search` függvény megvalósítását.

### Egy `clone` eltávolítása iterátor segítségével {#removing-a-clone-using-an-iterator}

A 12-6. kódrészletben olyan kódot írtunk, amely `String` értékek egy szeletét
vette át, és a szelet indexelésével, valamint az értékek klónozásával
létrehozta a `Config` struktúra egy példányát, így a `Config` struktúra
birtokolhatta ezeket az értékeket. A 13-17. kódrészletben megismételjük a
`Config::build` függvény megvalósítását abban a formában, ahogy a 12-23.
kódrészletben volt.

<Listing number="13-17" file-name="src/main.rs" caption="A `Config::build` függvény a 12-23. kódrészletből">

```rust,ignore
{{#rustdoc_include ../listings/ch13-functional-features/listing-12-23-reproduced/src/main.rs:ch13}}
```

</Listing>

Akkor azt mondtuk, hogy ne foglalkozz a nem hatékony `clone` hívásokkal, mert
később eltávolítjuk őket. Nos, most jött el az ideje!

Azért volt itt szükségünk a `clone`-ra, mert az `args` paraméterben egy
`String` elemekből álló szeletünk van, de a `build` függvény nem birtokolja az
`args`-ot. Ahhoz, hogy egy `Config` példány tulajdonjogát visszaadhassuk, ki
kellett klónoznunk az értékeket a `Config` `query` és `file_path` mezőjébe,
hogy a `Config` példány birtokolhassa az értékeit.

Az iterátorokról szerzett új tudásunkkal módosíthatjuk a `build` függvényt úgy,
hogy egy szelet kölcsönzése helyett egy iterátor tulajdonjogát vegye át
argumentumként. A szelet hosszát ellenőrző és adott pozíciókra indexelő kód
helyett az iterátor funkcionalitását fogjuk használni. Így világosabb lesz,
mit csinál a `Config::build` függvény, mert az értékekhez az iterátor fér hozzá.

Ha a `Config::build` átveszi az iterátor tulajdonjogát, és már nem használ
kölcsönző indexelési műveleteket, a `String` értékeket átmozgathatjuk az
iterátorból a `Config`-ba, ahelyett hogy meghívnánk a `clone`-t, és új
foglalást végeznénk.

#### A visszaadott iterátor közvetlen használata {#using-the-returned-iterator-directly}

Nyisd meg az I/O projekted _src/main.rs_ fájlját, amelynek így kell kinéznie:

<span class="filename">Fájlnév: src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch13-functional-features/listing-12-24-reproduced/src/main.rs:ch13}}
```

Először a `main` függvénynek a 12-24. kódrészletben szereplő elejét
módosítjuk a 13-18. kódrészletben látható kódra, amely ezúttal iterátort
használ. Ez nem fog lefordulni, amíg a `Config::build`-et is át nem írjuk.

<Listing number="13-18" file-name="src/main.rs" caption="Az `env::args` visszatérési értékének átadása a `Config::build`-nek">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-18/src/main.rs:here}}
```

</Listing>

Az `env::args` függvény iterátort ad vissza! Ahelyett hogy az iterátor
értékeit egy vektorba gyűjtenénk, majd egy szeletet adnánk át a
`Config::build`-nek, most az `env::args` által visszaadott iterátor
tulajdonjogát közvetlenül adjuk át a `Config::build`-nek.

Ezután módosítanunk kell a `Config::build` definícióját. Írjuk át a
`Config::build` szignatúráját a 13-19. kódrészletben láthatóra. Ez még mindig
nem fordul le, mert a függvény törzsét is módosítanunk kell.

<Listing number="13-19" file-name="src/main.rs" caption="A `Config::build` szignatúrájának módosítása, hogy iterátort várjon">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-19/src/main.rs:here}}
```

</Listing>

A standard könyvtár dokumentációja szerint az `env::args` függvény által
visszaadott iterátor típusa `std::env::Args`, és ez a típus megvalósítja az
`Iterator` traitet, valamint `String` értékeket ad vissza.

Úgy módosítottuk a `Config::build` függvény szignatúráját, hogy az `args`
paraméter típusa `&[String]` helyett egy `impl Iterator<Item = String>`
trait-korláttal megadott generikus típus legyen. Az `impl Trait` szintaxisnak
ez a használata, amelyet a 10. fejezet [„Traitek használata
paraméterként”][impl-trait]<!-- ignore --> részében tárgyaltunk, azt jelenti,
hogy az `args` bármilyen típus lehet, amely megvalósítja az `Iterator`
traitet, és `String` elemeket ad vissza.

Mivel átvesszük az `args` tulajdonjogát, és az `args`-on végighaladva
módosítani fogjuk, az `args` paraméter megadásához hozzáadhatjuk a `mut`
kulcsszót, hogy módosítható legyen.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-iterator-trait-methods-instead-of-indexing"></a>

#### Az `Iterator` trait metódusainak használata {#using-iterator-trait-methods}

Ezután kijavítjuk a `Config::build` törzsét. Mivel az `args` megvalósítja az
`Iterator` traitet, tudjuk, hogy meghívhatjuk rajta a `next` metódust! A
13-20. kódrészlet úgy módosítja a 12-23. kódrészlet kódját, hogy a `next`
metódust használja.

<Listing number="13-20" file-name="src/main.rs" caption="A `Config::build` törzsének módosítása, hogy iterátormetódusokat használjon">

```rust,ignore,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-20/src/main.rs:here}}
```

</Listing>

Ne feledd, hogy az `env::args` visszatérési értékének első eleme a program
neve. Ezt figyelmen kívül akarjuk hagyni, és a következő értékre akarunk
továbblépni, ezért először meghívjuk a `next`-et, és nem csinálunk semmit a
visszatérési értékével. Ezután ismét meghívjuk a `next`-et, hogy megkapjuk azt
az értéket, amelyet a `Config` `query` mezőjébe szeretnénk tenni. Ha a `next`
`Some`-ot ad vissza, egy `match` segítségével kinyerjük az értéket. Ha `None`-t
ad vissza, az azt jelenti, hogy nem kaptunk elég argumentumot, és egy `Err`
értékkel korán visszatérünk. Ugyanígy járunk el a `file_path` értékkel is.

<!-- Old headings. Do not remove or links may break. -->

<a id="making-code-clearer-with-iterator-adapters"></a>

### A kód világosabbá tétele iterátoradapterekkel {#clarifying-code-with-iterator-adapters}

Az I/O projektünk `search` függvényében is kihasználhatjuk az iterátorokat;
ezt a függvényt itt, a 13-21. kódrészletben megismételjük abban a formában,
ahogy a 12-19. kódrészletben volt.

<Listing number="13-21" file-name="src/lib.rs" caption="A `search` függvény megvalósítása a 12-19. kódrészletből">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-19/src/lib.rs:ch13}}
```

</Listing>

Ezt a kódot iterátoradapter-metódusokkal tömörebben is megírhatjuk. Így a
módosítható `results` köztes vektort is elkerülhetjük. A funkcionális
programozási stílus arra törekszik, hogy a módosítható állapot mennyiségét
minimalizálja, és így világosabbá tegye a kódot. A módosítható állapot
eltávolítása egy jövőbeli továbbfejlesztésként lehetővé teheti, hogy a keresés
párhuzamosan történjen, mert nem kellene kezelnünk a `results` vektorhoz való
konkurens hozzáférést. A 13-22. kódrészlet ezt a módosítást mutatja.

<Listing number="13-22" file-name="src/lib.rs" caption="Iterátoradapter-metódusok használata a `search` függvény megvalósításában">

```rust,ignore
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-22/src/lib.rs:here}}
```

</Listing>

Emlékezz vissza, hogy a `search` függvény célja, hogy visszaadja a `contents`
összes olyan sorát, amely tartalmazza a `query`-t. A 13-16. kódrészlet
`filter` példájához hasonlóan ez a kód a `filter` adaptert használja, hogy csak
azokat a sorokat tartsa meg, amelyekre a `line.contains(query)` `true`-t ad
vissza. Ezután a `collect` segítségével egy másik vektorba gyűjtjük az
illeszkedő sorokat. Sokkal egyszerűbb! Nyugodtan végezd el ugyanezt a
módosítást a `search_case_insensitive` függvényben is, hogy az is
iterátormetódusokat használjon.

További fejlesztésként adj vissza iterátort a `search` függvényből: távolítsd
el a `collect` hívását, és módosítsd a visszatérési típust `impl Iterator<Item
= &'a str>`-re, így a függvény maga is iterátoradapterré válik. Ne feledd,
hogy a teszteket is módosítanod kell! A módosítás előtt és után is keress egy
nagy fájlban a `minigrep` eszközöddel, és figyeld meg a viselkedésbeli
különbséget. A módosítás előtt a program addig nem ír ki egyetlen eredményt
sem, amíg össze nem gyűjtötte az összeset, a módosítás után viszont minden
illeszkedő sor megtalálásakor azonnal kiírja az eredményt, mert a `run`
függvény `for` ciklusa ki tudja használni az iterátor lustaságát.

<!-- Old headings. Do not remove or links may break. -->

<a id="choosing-between-loops-or-iterators"></a>

### Választás a ciklusok és az iterátorok között {#choosing-between-loops-and-iterators}

A következő logikus kérdés, hogy melyik stílust érdemes választanod a saját
kódodban, és miért: a 13-21. kódrészlet eredeti megvalósítását vagy a 13-22.
kódrészlet iterátorokat használó változatát (feltételezve, hogy az összes
eredményt összegyűjtjük, mielőtt visszaadnánk, ahelyett hogy az iterátort
adnánk vissza). A legtöbb Rust-programozó az iterátoros stílust részesíti
előnyben. Elsőre kicsit nehezebb ráérezni, de ha már kiismerted a különféle
iterátoradaptereket és azt, hogy mit csinálnak, az iterátorokat könnyebb
lehet megérteni. Ahelyett hogy a ciklusszervezés apró részleteivel és új
vektorok építésével bíbelődne, a kód a ciklus magas szintű céljára
összpontosít. Ez elrejti a hétköznapi kód egy részét, így könnyebb észrevenni
azokat a fogalmakat, amelyek az adott kódra egyediek, például azt a szűrési
feltételt, amelyen az iterátor minden elemének át kell jutnia.

De valóban egyenértékű a két megvalósítás? Ösztönösen azt feltételezhetnénk,
hogy az alacsonyabb szintű ciklus gyorsabb. Beszéljünk a teljesítményről.

[impl-trait]: ch10-02-traits.html#traits-as-parameters
