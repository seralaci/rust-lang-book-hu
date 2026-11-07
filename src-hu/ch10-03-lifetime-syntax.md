## Referenciák ellenőrzése élettartamokkal {#validating-references-with-lifetimes}

Az élettartamok a generikus típusok egy másik fajtáját alkotják, amelyet már
eddig is használtunk. Ahelyett hogy azt biztosítanák, hogy egy típus a kívánt
viselkedéssel rendelkezzen, az élettartamok azt biztosítják, hogy a
referenciák addig érvényesek maradjanak, ameddig szükségünk van rájuk.

A 4. fejezet [„Referenciák és
kölcsönzés”][references-and-borrowing]<!-- ignore --> szakaszában nem
beszéltünk arról a részletről, hogy a Rustban minden referenciának van
_élettartama (lifetime)_, vagyis egy hatóköre, amelyen belül a referencia
érvényes. Az élettartamok legtöbbször implicitek és
kikövetkeztetettek, ahogy legtöbbször a típusok is kikövetkeztetettek. Típusokat
csak akkor kell annotálnunk, ha több típus is szóba jöhet. Hasonlóképpen az
élettartamokat akkor kell annotálnunk, ha a referenciák élettartamai többféle
módon is összefügghetnek. A Rust megköveteli, hogy ezeket az összefüggéseket
generikus élettartam-paraméterekkel annotáljuk, így biztosítva, hogy a
futásidőben használt tényleges referenciák biztosan érvényesek legyenek.

Az élettartamok annotálása olyan fogalom, amely a legtöbb más programozási
nyelvben egyáltalán nem létezik, ezért szokatlan lesz. Bár ebben a fejezetben
nem tárgyaljuk teljes egészében az élettartamokat, áttekintjük, milyen gyakori
formákban találkozhatsz az élettartam-szintaxissal, hogy megbarátkozhass a
fogalommal.

<!-- Old headings. Do not remove or links may break. -->

<a id="preventing-dangling-references-with-lifetimes"></a>

### Lógó referenciák {#dangling-references}

Az élettartamok fő célja a lógó referenciák megakadályozása; ha ezek
létezhetnének, a program más adatra hivatkozna, mint amelyre szeretne.
Vegyük a 10-16. kódrészlet programját, amelyben van egy külső és egy belső
hatókör.

<Listing number="10-16" caption="Kísérlet egy olyan referencia használatára, amelynek értéke már kikerült a hatókörből">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-16/src/main.rs}}
```

</Listing>

> Megjegyzés: A 10-16., a 10-17. és a 10-23. kódrészlet példái úgy deklarálnak
> változókat, hogy nem adnak nekik kezdőértéket, így a változó neve a külső
> hatókörben létezik. Első ránézésre ez ellentmondásnak tűnhet azzal, hogy a
> Rustban nincsenek null értékek. Ha azonban egy változót azelőtt próbálunk
> használni, hogy értéket adnánk neki, fordítási idejű hibát kapunk, ami azt
> mutatja, hogy a Rust valóban nem enged meg null értékeket.

A külső hatókör egy `r` nevű változót deklarál kezdőérték nélkül, a belső
hatókör pedig egy `x` nevű változót `5` kezdőértékkel. A belső hatókörön belül
megpróbáljuk az `r` értékét az `x`-re mutató referenciára állítani. Ezután a
belső hatókör véget ér, és megpróbáljuk kiírni az `r`-ben lévő értéket. Ez a
kód nem fordul le, mert az az érték, amelyre az `r` hivatkozik, kikerült a
hatókörből, mielőtt használni próbálnánk. Ez a hibaüzenet:

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-16/output.txt}}
```

A hibaüzenet szerint az `x` változó „nem él elég sokáig” („does not live long
enough”). Ennek az az oka, hogy az `x` kikerül a hatókörből, amikor a belső
hatókör a 7. sorban véget ér. Az `r` viszont a külső hatókörben még érvényes;
mivel a hatóköre nagyobb, azt mondjuk, hogy „tovább él”. Ha a Rust engedné,
hogy ez a kód működjön, az `r` olyan memóriára hivatkozna, amelyet az `x`
hatókörből való kikerülésekor felszabadítottunk, és bármi, amit az `r`-rel
próbálnánk tenni, nem működne helyesen. Hogyan állapítja meg tehát a Rust, hogy
ez a kód érvénytelen? Egy kölcsönzésellenőrzővel.

### A kölcsönzésellenőrző {#the-borrow-checker}

A Rust fordítójában van egy _kölcsönzésellenőrző (borrow checker)_, amely a
hatóköröket összehasonlítva állapítja meg, hogy minden kölcsönzés érvényes-e.
A 10-17. kódrészlet ugyanazt a kódot mutatja, mint a 10-16. kódrészlet, de a
változók élettartamait jelző annotációkkal.

<Listing number="10-17" caption="Az `r` és az `x` élettartamának annotációi, `'a`, illetve `'b` néven">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-17/src/main.rs}}
```

</Listing>

Itt az `r` élettartamát `'a`-val, az `x` élettartamát pedig `'b`-vel
annotáltuk. Ahogy látod, a belső `'b` blokk jóval kisebb, mint a külső `'a`
élettartam-blokk. Fordításkor a Rust összehasonlítja a két élettartam
hosszát, és látja, hogy az `r` élettartama `'a`, de olyan memóriára hivatkozik,
amelynek élettartama `'b`. A program elutasításra kerül, mert a `'b` rövidebb,
mint az `'a`: a referencia tárgya nem él olyan sokáig, mint maga a referencia.

A 10-18. kódrészlet úgy javítja ki a kódot, hogy ne legyen benne lógó
referencia, és hiba nélkül leforduljon.

<Listing number="10-18" caption="Egy érvényes referencia, mert az adat élettartama hosszabb, mint a referenciáé">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-18/src/main.rs}}
```

</Listing>

Itt az `x` élettartama `'b`, ami ebben az esetben nagyobb, mint az `'a`. Ez azt
jelenti, hogy az `r` hivatkozhat az `x`-re, mert a Rust tudja, hogy az `r`-ben
lévő referencia mindig érvényes lesz, amíg az `x` érvényes.

Most, hogy tudod, hol vannak a referenciák élettartamai, és hogyan elemzi a
Rust az élettartamokat, hogy a referenciák mindig érvényesek legyenek,
vizsgáljuk meg a generikus élettartamokat a függvényparaméterekben és a
visszatérési értékekben.

### Generikus élettartamok függvényekben {#generic-lifetimes-in-functions}

Írunk egy függvényt, amely két sztringszelet közül a hosszabbat adja vissza.
Ez a függvény két sztringszeletet kap, és egyetlen sztringszeletet ad vissza.
Miután megvalósítottuk a `longest` függvényt, a 10-19. kódrészlet kódjának a
`The longest string is abcd` szöveget kell kiírnia.

<Listing number="10-19" file-name="src/main.rs" caption="Egy `main` függvény, amely a `longest` függvényt hívja meg, hogy megtalálja két sztringszelet közül a hosszabbat">

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-19/src/main.rs}}
```

</Listing>

Figyeld meg, hogy azt szeretnénk, hogy a függvény sztringek helyett
sztringszeleteket kapjon, amelyek referenciák, mert nem akarjuk, hogy a
`longest` függvény átvegye a paraméterei feletti tulajdonjogot. Arról, hogy
miért éppen ezeket a paramétereket akarjuk használni a 10-19. kódrészletben,
bővebben a 4. fejezet [„Sztringszeletek
paraméterként”][string-slices-as-parameters]<!-- ignore --> szakaszában
olvashatsz.

Ha a `longest` függvényt a 10-20. kódrészletben látható módon próbáljuk
megvalósítani, nem fordul le.

<Listing number="10-20" file-name="src/main.rs" caption="A `longest` függvény egy megvalósítása, amely két sztringszelet közül a hosszabbat adja vissza, de még nem fordul le">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-20/src/main.rs:here}}
```

</Listing>

Ehelyett a következő hibát kapjuk, amely élettartamokról szól:

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-20/output.txt}}
```

A súgószövegből kiderül, hogy a visszatérési típusnak generikus
élettartam-paraméterre van szüksége, mert a Rust nem tudja megállapítani, hogy
a visszaadott referencia az `x`-re vagy az `y`-ra hivatkozik. Valójában mi sem
tudjuk, mert a függvény törzsében az `if` blokk az `x`-re, az `else` blokk
pedig az `y`-ra mutató referenciát ad vissza!

Amikor ezt a függvényt definiáljuk, nem ismerjük azokat a konkrét értékeket,
amelyeket átadnak neki, így azt sem tudjuk, hogy az `if` vagy az `else` ág fut
le. Az átadott referenciák konkrét élettartamait sem ismerjük, így nem
vizsgálhatjuk meg a hatóköröket úgy, ahogy a 10-17. és a 10-18.
kódrészletben, hogy megállapítsuk, a visszaadott referencia mindig érvényes
lesz-e. A kölcsönzésellenőrző sem tudja ezt megállapítani, mert nem tudja,
hogyan viszonyul az `x` és az `y` élettartama a visszatérési érték
élettartamához. A hiba javításához generikus élettartam-paramétereket adunk
hozzá, amelyek meghatározzák a referenciák közötti kapcsolatot, hogy a
kölcsönzésellenőrző elvégezhesse az elemzését.

### Az élettartam-annotáció szintaxisa {#lifetime-annotation-syntax}

Az élettartam-annotációk nem változtatják meg, hogy a referenciák meddig
élnek. Ehelyett több referencia élettartamának egymáshoz való viszonyát írják
le, anélkül hogy az élettartamokat befolyásolnák. Ahogy a függvények bármilyen
típust elfogadhatnak, ha a szignatúra generikus típusparamétert ad meg, úgy
bármilyen élettartamú referenciát is elfogadhatnak, ha generikus
élettartam-paramétert adunk meg.

Az élettartam-annotációk szintaxisa kissé szokatlan: az élettartam-paraméterek
nevének aposztróffal (`'`) kell kezdődnie, és általában csupa kisbetűsek és
nagyon rövidek, mint a generikus típusok. A legtöbben az `'a` nevet használják
az első élettartam-annotációhoz. Az élettartam-paraméterek annotációit a
referencia `&` jele után írjuk, és szóközzel választjuk el az annotációt a
referencia típusától.

Íme néhány példa – egy `i32`-re mutató referencia élettartam-paraméter
nélkül, egy `i32`-re mutató referencia, amelynek `'a` nevű élettartam-paramétere
van, és egy `i32`-re mutató módosítható referencia, amelynek szintén `'a` az
élettartama:

```rust,ignore
&i32        // a reference
&'a i32     // a reference with an explicit lifetime
&'a mut i32 // a mutable reference with an explicit lifetime
```

Egyetlen élettartam-annotációnak önmagában nincs sok jelentése, mert az
annotációk arra valók, hogy közöljék a Rusttal, hogyan viszonyulnak egymáshoz
több referencia generikus élettartam-paraméterei. Vizsgáljuk meg, hogyan
viszonyulnak egymáshoz az élettartam-annotációk a `longest` függvény
esetében.

<!-- Old headings. Do not remove or links may break. -->

<a id="lifetime-annotations-in-function-signatures"></a>

### Függvényszignatúrákban {#in-function-signatures}

Ha élettartam-annotációkat szeretnénk használni függvényszignatúrákban, a
generikus élettartam-paramétereket a függvény neve és a paraméterlista között,
csúcsos zárójeleken belül kell deklarálnunk, ahogy a generikus
típusparamétereknél tettük.

Azt szeretnénk, hogy a szignatúra a következő megkötést fejezze ki: a
visszaadott referencia addig érvényes, amíg mindkét paraméter érvényes. Ez a
kapcsolat a paraméterek és a visszatérési érték élettartamai között. Az
élettartamot `'a`-nak nevezzük el, majd minden referenciához hozzáadjuk, ahogy
a 10-21. kódrészlet mutatja.

<Listing number="10-21" file-name="src/main.rs" caption="A `longest` függvény definíciója, amely előírja, hogy a szignatúrában szereplő összes referenciának ugyanaz az `'a` élettartama legyen">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-21/src/main.rs:here}}
```

</Listing>

Ennek a kódnak le kell fordulnia, és a kívánt eredményt kell adnia, ha a 10-19.
kódrészlet `main` függvényével használjuk.

A függvényszignatúra most azt közli a Rusttal, hogy valamilyen `'a`
élettartamra a függvény két paramétert kap, és mindkettő olyan sztringszelet,
amely legalább az `'a` élettartamig él. A függvényszignatúra azt is közli a
Rusttal, hogy a függvény által visszaadott sztringszelet legalább az `'a`
élettartamig élni fog. A gyakorlatban ez azt jelenti, hogy a `longest` függvény
által visszaadott referencia élettartama megegyezik a függvényargumentumok által
hivatkozott értékek élettartamai közül a rövidebbel. Azt szeretnénk, hogy a
Rust ezeket a kapcsolatokat használja a kód elemzésekor.

Ne feledd: amikor ebben a függvényszignatúrában megadjuk az
élettartam-paramétereket, nem változtatjuk meg egyetlen átadott vagy
visszaadott érték élettartamát sem. Ehelyett azt adjuk meg, hogy a
kölcsönzésellenőrző utasítson el minden olyan értéket, amely nem felel meg
ezeknek a megkötéseknek. Figyeld meg, hogy a `longest` függvénynek nem kell
pontosan tudnia, meddig él az `x` és az `y`, csak azt, hogy az `'a` helyére
behelyettesíthető valamilyen hatókör, amely kielégíti ezt a szignatúrát.

Amikor függvényekben annotálunk élettartamokat, az annotációk a függvény
szignatúrájába kerülnek, nem a függvény törzsébe. Az élettartam-annotációk a
függvény szerződésének részévé válnak, akárcsak a szignatúrában szereplő
típusok. Ha a függvényszignatúrák tartalmazzák az élettartamokra vonatkozó
szerződést, a Rust fordító által végzett elemzés egyszerűbb lehet. Ha gond van
azzal, ahogyan egy függvényt annotáltunk vagy ahogyan meghívjuk, a fordító
hibaüzenetei pontosabban rámutathatnak a kódunk érintett részére és a
megkötésekre. Ha ehelyett a Rust fordító több következtetést vonna le arról,
milyen kapcsolatot szántunk az élettartamok között, a fordító talán csak a
kódunk egy olyan használatára tudna rámutatni, amely sok lépésnyire van a
probléma okától.

Amikor konkrét referenciákat adunk át a `longest`-nek, az `'a` helyére
behelyettesített konkrét élettartam az `x` hatókörének az a része, amely
átfedésben van az `y` hatókörével. Más szóval az `'a` generikus élettartam azt
a konkrét élettartamot kapja, amely az `x` és az `y` élettartama közül a
rövidebbel egyenlő. Mivel a visszaadott referenciát ugyanazzal az `'a`
élettartam-paraméterrel annotáltuk, a visszaadott referencia is az `x` és az
`y` élettartama közül a rövidebbik hosszáig lesz érvényes.

Nézzük meg, hogyan korlátozzák az élettartam-annotációk a `longest` függvényt,
ha különböző konkrét élettartamú referenciákat adunk át neki. A 10-22.
kódrészlet egy egyszerű példa.

<Listing number="10-22" file-name="src/main.rs" caption="A `longest` függvény használata különböző konkrét élettartamú `String` értékekre mutató referenciákkal">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-22/src/main.rs:here}}
```

</Listing>

Ebben a példában a `string1` a külső hatókör végéig érvényes, a `string2` a
belső hatókör végéig, a `result` pedig olyasmire hivatkozik, ami a belső
hatókör végéig érvényes. Ha lefuttatod ezt a kódot, láthatod, hogy a
kölcsönzésellenőrző jóváhagyja; a kód lefordul, és a `The longest string is
long string is long` szöveget írja ki.

Most próbáljunk ki egy olyan példát, amely megmutatja, hogy a `result`-ban
lévő referencia élettartamának a két argumentum közül a rövidebb élettartamnak
kell lennie. A `result` változó deklarációját a belső hatókörön kívülre
helyezzük, de az értékadást a `result` változónak a `string2`-t tartalmazó
hatókörön belül hagyjuk. Ezután a `result`-ot használó `println!`-t a belső
hatókörön kívülre, a belső hatókör vége utánra helyezzük. A 10-23. kódrészlet
kódja nem fordul le.

<Listing number="10-23" file-name="src/main.rs" caption="Kísérlet a `result` használatára, miután a `string2` kikerült a hatókörből">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-23/src/main.rs:here}}
```

</Listing>

Amikor megpróbáljuk lefordítani ezt a kódot, ezt a hibát kapjuk:

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-23/output.txt}}
```

A hiba azt mutatja, hogy ahhoz, hogy a `result` érvényes legyen a `println!`
utasításnál, a `string2`-nek a külső hatókör végéig érvényesnek kellene
lennie. A Rust ezt azért tudja, mert a függvényparaméterek és a visszatérési
értékek élettartamait ugyanazzal az `'a` élettartam-paraméterrel annotáltuk.

Emberként ránézhetünk erre a kódra, és láthatjuk, hogy a `string1` hosszabb,
mint a `string2`, ezért a `result` a `string1`-re mutató referenciát fog
tartalmazni. Mivel a `string1` még nem került ki a hatókörből, a `string1`-re
mutató referencia a `println!` utasításnál is érvényes lesz. A fordító azonban
nem látja, hogy a referencia ebben az esetben érvényes. Azt közöltük a
Rusttal, hogy a `longest` függvény által visszaadott referencia élettartama
megegyezik az átadott referenciák élettartamai közül a rövidebbel. Ezért a
kölcsönzésellenőrző nem engedélyezi a 10-23. kódrészlet kódját, mert az
esetleg érvénytelen referenciát tartalmazhat.

Próbálj meg további kísérleteket kitalálni, amelyekben változtatod a
`longest` függvénynek átadott referenciák értékeit és élettartamait, valamint
azt, hogyan használod a visszaadott referenciát. Fordítás előtt állíts fel
hipotézist arról, hogy a kísérleteid átmennek-e a kölcsönzésellenőrzőn; aztán
ellenőrizd, igazad volt-e!

<!-- Old headings. Do not remove or links may break. -->

<a id="thinking-in-terms-of-lifetimes"></a>

### Kapcsolatok {#relationships}

Az, hogy hogyan kell megadnod az élettartam-paramétereket, attól függ, mit
csinál a függvényed. Ha például úgy módosítanánk a `longest` függvény
megvalósítását, hogy mindig az első paramétert adja vissza a hosszabb
sztringszelet helyett, nem kellene élettartamot megadnunk az `y` paraméteren.
A következő kód lefordul:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-08-only-one-reference-with-lifetime/src/main.rs:here}}
```

</Listing>

Az `x` paraméterhez és a visszatérési típushoz megadtunk egy `'a`
élettartam-paramétert, az `y` paraméterhez viszont nem, mert az `y`
élettartama semmilyen kapcsolatban nincs sem az `x`, sem a visszatérési érték
élettartamával.

Ha egy függvényből referenciát adunk vissza, a visszatérési típus
élettartam-paraméterének meg kell egyeznie valamelyik paraméter
élettartam-paraméterével. Ha a visszaadott referencia _nem_ valamelyik
paraméterre hivatkozik, akkor egy, a függvényen belül létrehozott értékre kell
hivatkoznia. Ez azonban lógó referencia lenne, mert az érték a függvény végén
kikerül a hatókörből. Vegyük a `longest` függvény következő megvalósítási
kísérletét, amely nem fordul le:

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-09-unrelated-lifetime/src/main.rs:here}}
```

</Listing>

Itt bár megadtunk egy `'a` élettartam-paramétert a visszatérési típushoz, ez a
megvalósítás nem fordul le, mert a visszatérési érték élettartama egyáltalán
nincs kapcsolatban a paraméterek élettartamával. Ezt a hibaüzenetet kapjuk:

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-09-unrelated-lifetime/output.txt}}
```

A probléma az, hogy a `result` a `longest` függvény végén kikerül a
hatókörből, és felszabadul. Mi pedig a `result`-ra mutató referenciát
próbálunk visszaadni a függvényből. Semmilyen élettartam-paraméterrel nem
tudnánk megváltoztatni a lógó referenciát, a Rust pedig nem engedi, hogy lógó
referenciát hozzunk létre. Ebben az esetben a legjobb megoldás az lenne, ha
referencia helyett saját tulajdonú adattípust adnánk vissza, így az érték
felszabadítása a hívó függvény felelőssége lenne.

Végső soron az élettartam-szintaxis arról szól, hogy összekapcsoljuk a
függvények különböző paramétereinek és visszatérési értékeinek élettartamait.
Ha ezek össze vannak kapcsolva, a Rust elég információval rendelkezik ahhoz,
hogy engedélyezze a memóriabiztos műveleteket, és megtiltsa azokat, amelyek
lógó mutatókat hoznának létre, vagy más módon sértenék a memóriabiztonságot.

<!-- Old headings. Do not remove or links may break. -->

<a id="lifetime-annotations-in-struct-definitions"></a>

### Struktúradefiníciókban {#in-struct-definitions}

Az eddig definiált struktúráink mind saját tulajdonú típusokat tároltak.
Definiálhatunk referenciákat tároló struktúrákat is, de ebben az esetben a
struktúra definíciójában minden referenciához élettartam-annotációt kell
adnunk. A 10-24. kódrészletben egy `ImportantExcerpt` nevű struktúra látható,
amely egy sztringszeletet tárol.

<Listing number="10-24" file-name="src/main.rs" caption="Egy referenciát tároló struktúra, amelyhez élettartam-annotáció szükséges">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-24/src/main.rs}}
```

</Listing>

Ennek a struktúrának egyetlen mezője van, a `part`, amely egy sztringszeletet,
vagyis egy referenciát tárol. A generikus adattípusokhoz hasonlóan a generikus
élettartam-paraméter nevét a struktúra neve után, csúcsos zárójelek között
deklaráljuk, hogy a struktúradefiníció törzsében használhassuk az
élettartam-paramétert. Ez az annotáció azt jelenti, hogy az `ImportantExcerpt`
egy példánya nem élheti túl a `part` mezőjében tárolt referenciát.

A `main` függvény itt az `ImportantExcerpt` struktúra egy példányát hozza
létre, amely a `novel` változó tulajdonában lévő `String` első mondatára mutató
referenciát tárol. A `novel` adatai már az `ImportantExcerpt` példány
létrehozása előtt léteznek. Ráadásul a `novel` csak azután kerül ki a
hatókörből, hogy az `ImportantExcerpt` kikerült a hatókörből, így az
`ImportantExcerpt` példányban lévő referencia érvényes.

### Élettartam-elhagyás {#lifetime-elision}

Megtanultad, hogy minden referenciának van élettartama, és hogy a referenciákat
használó függvényekhez vagy struktúrákhoz élettartam-paramétereket kell
megadnod. A 4-9. kódrészletben azonban volt egy függvényünk – a 10-25.
kódrészletben újra látható –, amely élettartam-annotációk nélkül is
lefordult.

<Listing number="10-25" file-name="src/lib.rs" caption="A 4-9. kódrészletben definiált függvény, amely élettartam-annotációk nélkül is lefordult, pedig a paraméter és a visszatérési típus is referencia">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-25/src/main.rs:here}}
```

</Listing>

Ennek a függvénynek az élettartam-annotációk nélküli lefordulása történeti
okokra vezethető vissza: a Rust korai (1.0 előtti) verzióiban ez a kód nem
fordult volna le, mert minden referenciához explicit élettartam kellett.
Akkoriban a függvény szignatúráját így kellett volna megírni:

```rust,ignore
fn first_word<'a>(s: &'a str) -> &'a str {
```

Miután rengeteg Rust-kódot megírtak, a Rust csapata azt tapasztalta, hogy a
Rust-programozók bizonyos helyzetekben újra meg újra ugyanazokat az
élettartam-annotációkat írják be. Ezek a helyzetek kiszámíthatók voltak, és
néhány determinisztikus mintát követtek. A fejlesztők beprogramozták ezeket a
mintákat a fordító kódjába, hogy a kölcsönzésellenőrző ezekben a helyzetekben
ki tudja következtetni az élettartamokat, és ne legyen szükség explicit
annotációkra.

A Rust történetének ez a darabja azért fontos, mert elképzelhető, hogy további
determinisztikus minták bukkannak fel, és bekerülnek a fordítóba. A jövőben
talán még kevesebb élettartam-annotációra lesz szükség.

A Rust referenciaelemzésébe beprogramozott mintákat _élettartam-elhagyási
szabályoknak (lifetime elision rules)_ nevezzük. Ezek nem a programozók által
követendő szabályok; olyan esetek halmazát alkotják, amelyeket a fordító
figyelembe vesz, és ha a kódod megfelel ezeknek az eseteknek, nem kell
explicit módon kiírnod az élettartamokat.

Az elhagyási szabályok nem biztosítanak teljes következtetést. Ha a szabályok
alkalmazása után is kétértelmű marad, milyen élettartamúak a referenciák, a
fordító nem fogja kitalálni, mi legyen a fennmaradó referenciák élettartama.
Találgatás helyett a fordító hibát ad, amelyet élettartam-annotációk
hozzáadásával oldhatsz meg.

A függvény- vagy metódusparaméterek élettartamait _bemeneti élettartamoknak
(input lifetimes)_, a visszatérési értékek élettartamait pedig _kimeneti
élettartamoknak (output lifetimes)_ nevezzük.

A fordító három szabály segítségével állapítja meg a referenciák élettartamait,
ha nincsenek explicit annotációk. Az első szabály a bemeneti élettartamokra
vonatkozik, a második és a harmadik pedig a kimeneti élettartamokra. Ha a
fordító a három szabály végére ér, és még mindig vannak olyan referenciák,
amelyeknek nem tudja megállapítani az élettartamát, hibával leáll. Ezek a
szabályok az `fn` definíciókra és az `impl` blokkokra egyaránt vonatkoznak.

Az első szabály az, hogy a fordító minden referencia típusú paraméterhez
hozzárendel egy élettartam-paramétert. Más szóval az egyparaméteres függvény
egy élettartam-paramétert kap: `fn foo<'a>(x: &'a i32)`; a kétparaméteres
függvény két külön élettartam-paramétert kap: `fn foo<'a, 'b>(x: &'a i32,
y: &'b i32)`; és így tovább.

A második szabály az, hogy ha pontosan egy bemeneti élettartam-paraméter van,
akkor ez az élettartam lesz hozzárendelve az összes kimeneti
élettartam-paraméterhez: `fn foo<'a>(x: &'a i32) -> &'a i32`.

A harmadik szabály az, hogy ha több bemeneti élettartam-paraméter van, de az
egyik közülük `&self` vagy `&mut self`, mert metódusról van szó, akkor a
`self` élettartama lesz hozzárendelve az összes kimeneti
élettartam-paraméterhez. Ez a harmadik szabály sokkal könnyebben olvashatóvá
és írhatóvá teszi a metódusokat, mert kevesebb szimbólumra van szükség.

Képzeljük magunkat a fordító helyébe. Alkalmazzuk ezeket a szabályokat, hogy
megállapítsuk a 10-25. kódrészlet `first_word` függvényének szignatúrájában
szereplő referenciák élettartamait. A szignatúra kezdetben semmilyen, a
referenciákhoz társított élettartamot nem tartalmaz:

```rust,ignore
fn first_word(s: &str) -> &str {
```

Ezután a fordító alkalmazza az első szabályt, amely szerint minden paraméter
saját élettartamot kap. Szokás szerint `'a`-nak nevezzük, így a szignatúra
most ez:

```rust,ignore
fn first_word<'a>(s: &'a str) -> &str {
```

A második szabály is érvényes, mert pontosan egy bemeneti élettartam van. A
második szabály szerint az egyetlen bemeneti paraméter élettartama hozzá lesz
rendelve a kimeneti élettartamhoz, így a szignatúra most ez:

```rust,ignore
fn first_word<'a>(s: &'a str) -> &'a str {
```

Most már ebben a függvényszignatúrában minden referenciának van élettartama, és
a fordító folytathatja az elemzést anélkül, hogy a programozónak annotálnia
kellene az élettartamokat ebben a függvényszignatúrában.

Nézzünk meg egy másik példát, ezúttal a `longest` függvénnyel, amelynek nem
voltak élettartam-paraméterei, amikor a 10-20. kódrészletben elkezdtünk vele
dolgozni:

```rust,ignore
fn longest(x: &str, y: &str) -> &str {
```

Alkalmazzuk az első szabályt: minden paraméter saját élettartamot kap. Ezúttal
egy helyett két paraméterünk van, így két élettartamunk lesz:

```rust,ignore
fn longest<'a, 'b>(x: &'a str, y: &'b str) -> &str {
```

Láthatod, hogy a második szabály nem érvényes, mert egynél több bemeneti
élettartam van. A harmadik szabály sem érvényes, mert a `longest` függvény,
nem metódus, így egyik paramétere sem `self`. Mindhárom szabály alkalmazása
után sem tudtuk megállapítani, mi a visszatérési típus élettartama. Ezért
kaptunk hibát, amikor a 10-20. kódrészlet kódját próbáltuk lefordítani: a
fordító végigment az élettartam-elhagyási szabályokon, de még így sem tudta
megállapítani a szignatúrában szereplő referenciák összes élettartamát.

Mivel a harmadik szabály valójában csak metódusszignatúrákra vonatkozik, a
következőkben ebben a környezetben vizsgáljuk meg az élettartamokat, hogy
lássuk, a harmadik szabály miatt miért nem kell túl gyakran élettartamokat
annotálnunk a metódusszignatúrákban.

<!-- Old headings. Do not remove or links may break. -->

<a id="lifetime-annotations-in-method-definitions"></a>

### Metódusdefiníciókban {#in-method-definitions}

Amikor élettartamokkal rendelkező struktúrán valósítunk meg metódusokat,
ugyanazt a szintaxist használjuk, mint a generikus típusparamétereknél, ahogy
a 10-11. kódrészletben látható. Az, hogy hol deklaráljuk és használjuk az
élettartam-paramétereket, attól függ, hogy a struktúra mezőihez vagy a
metódus paramétereihez és visszatérési értékeihez kapcsolódnak-e.

A struktúramezők élettartamneveit mindig az `impl` kulcsszó után kell
deklarálni, majd a struktúra neve után használni, mert ezek az élettartamok a
struktúra típusának részei.

Az `impl` blokkon belüli metódusszignatúrákban a referenciák kötődhetnek a
struktúra mezőiben lévő referenciák élettartamához, de függetlenek is lehetnek
tőle. Ráadásul az élettartam-elhagyási szabályok miatt a metódusszignatúrákban
gyakran nincs szükség élettartam-annotációkra. Nézzünk néhány példát a 10-24.
kódrészletben definiált `ImportantExcerpt` nevű struktúrával.

Először egy `level` nevű metódust használunk, amelynek egyetlen paramétere a
`self`-re mutató referencia, visszatérési értéke pedig egy `i32`, amely nem
referencia semmire:

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-10-lifetimes-on-methods/src/main.rs:1st}}
```

Az `impl` utáni élettartam-paraméter-deklaráció és annak használata a típusnév
után kötelező, de az első elhagyási szabály miatt nem kell annotálnunk a
`self`-re mutató referencia élettartamát.

Íme egy példa, amelyben a harmadik élettartam-elhagyási szabály érvényesül:

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-10-lifetimes-on-methods/src/main.rs:3rd}}
```

Két bemeneti élettartam van, így a Rust alkalmazza az első élettartam-elhagyási
szabályt, és a `&self` és az `announcement` is saját élettartamot kap. Ezután,
mivel az egyik paraméter `&self`, a visszatérési típus a `&self` élettartamát
kapja, és ezzel minden élettartam meg van határozva.

### A statikus élettartam {#the-static-lifetime}

Egy különleges élettartamról is beszélnünk kell, ez a `'static`, amely azt
jelzi, hogy az érintett referencia a program teljes futása alatt _élhet_. Minden
sztringliterál élettartama `'static`, amit így annotálhatunk:

```rust
let s: &'static str = "I have a static lifetime.";
```

Ennek a sztringnek a szövege közvetlenül a program binárisában tárolódik, amely
mindig elérhető. Ezért minden sztringliterál élettartama `'static`.

Előfordulhat, hogy hibaüzenetekben azt a javaslatot látod, hogy használd a
`'static` élettartamot. Mielőtt azonban egy referencia élettartamaként a
`'static`-et adnád meg, gondold végig, hogy a referenciád valóban a programod
teljes élettartama alatt él-e, és hogy egyáltalán ezt szeretnéd-e. Legtöbbször
a `'static` élettartamot javasló hibaüzenet abból adódik, hogy lógó referenciát
próbálunk létrehozni, vagy a rendelkezésre álló élettartamok nem illeszkednek.
Ilyen esetekben a megoldás ezeknek a problémáknak a kijavítása, nem pedig a
`'static` élettartam megadása.

<!-- Old headings. Do not remove or links may break. -->

<a id="generic-type-parameters-trait-bounds-and-lifetimes-together"></a>

## Generikus típusparaméterek, trait-korlátok és élettartamok {#generic-type-parameters-trait-bounds-and-lifetimes}

Nézzük meg röviden, hogyan adhatunk meg generikus típusparamétereket,
trait-korlátokat és élettartamokat egyetlen függvényben!

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-11-generics-traits-and-lifetimes/src/main.rs:here}}
```

Ez a 10-21. kódrészlet `longest` függvénye, amely két sztringszelet közül a
hosszabbat adja vissza. Most azonban van egy további, `ann` nevű, `T`
generikus típusú paramétere is, amelynek helyére bármilyen típus kerülhet,
amely – a `where` záradék előírása szerint – megvalósítja a `Display` traitet.
Ezt a további paramétert a `{}` segítségével írjuk ki, ezért van szükség a
`Display` trait-korlátra. Mivel az élettartamok a generikus típusok egy
fajtáját alkotják, az `'a` élettartam-paraméter és a `T` generikus
típusparaméter deklarációja ugyanabba a listába kerül, a függvény neve utáni
csúcsos zárójelek közé.

## Összefoglalás {#summary}

Sok mindenről volt szó ebben a fejezetben! Most, hogy ismered a generikus
típusparamétereket, a traiteket és a trait-korlátokat, valamint a generikus
élettartam-paramétereket, készen állsz arra, hogy ismétlés nélküli kódot írj,
amely sokféle helyzetben működik. A generikus típusparaméterekkel a kódot
különböző típusokra alkalmazhatod. A traitek és a trait-korlátok biztosítják,
hogy a típusok – bár generikusak – rendelkezzenek a kód által igényelt
viselkedéssel. Megtanultad, hogyan biztosíthatod élettartam-annotációkkal,
hogy ebben a rugalmas kódban ne legyenek lógó referenciák. És mindez az elemzés
fordítási időben történik, így nem befolyásolja a futásidejű teljesítményt!

Akár hiszed, akár nem, az ebben a fejezetben tárgyalt témákról még sokkal több
tanulnivaló van: a 18. fejezet a trait objektumokat tárgyalja, amelyek a
traitek használatának egy másik módját jelentik. Vannak az
élettartam-annotációkat érintő összetettebb esetek is, amelyekre csak nagyon
haladó helyzetekben lesz szükséged; ezekhez a [Rust Reference][reference]
anyagát érdemes elolvasnod. Most azonban megtanulod, hogyan írhatsz teszteket
a Rustban, hogy megbizonyosodhass arról, hogy a kódod úgy működik, ahogy kell.

[references-and-borrowing]: ch04-02-references-and-borrowing.html#references-and-borrowing
[string-slices-as-parameters]: ch04-03-slices.html#string-slices-as-parameters
[reference]: ../reference/trait-bounds.html
