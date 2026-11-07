<!-- Old headings. Do not remove or links may break. -->
<a id="developing-the-librarys-functionality-with-test-driven-development"></a>

## Funkciók hozzáadása tesztvezérelt fejlesztéssel {#adding-functionality-with-test-driven-development}

Most, hogy a keresési logika a `main` függvénytől elkülönítve a _src/lib.rs_
fájlban van, sokkal könnyebb teszteket írni a kódunk alapvető
funkcióihoz. A függvényeket közvetlenül meghívhatjuk különféle
argumentumokkal, és ellenőrizhetjük a visszatérési értékeket anélkül, hogy a
binárisunkat a parancssorból kellene meghívnunk.

Ebben a szakaszban a keresési logikát a _tesztvezérelt fejlesztés
(test-driven development, TDD)_ folyamatával adjuk hozzá a `minigrep`
programhoz, a következő lépésekben:

1. Írj egy tesztet, amely elbukik, és futtasd le, hogy meggyőződj róla: azért
   bukik el, amiért várod.
2. Írj vagy módosíts éppen annyi kódot, hogy az új teszt sikeres legyen.
3. Refaktoráld az imént hozzáadott vagy módosított kódot, és győződj meg róla,
   hogy a tesztek továbbra is sikeresek.
4. Ismételd az 1. lépéstől!

Bár ez csak egy a szoftverírás sok módja közül, a TDD segíthet a kód
tervezésének irányításában. Ha a tesztet még azelőtt megírod, hogy megírnád
a tesztet sikeressé tevő kódot, a folyamat során végig magas
tesztlefedettséget tarthatsz fenn.

Tesztekkel vezérelve valósítjuk meg azt a funkciót, amely ténylegesen
megkeresi a keresett sztringet a fájl tartalmában, és előállítja a keresett
kifejezésre illeszkedő sorok listáját. Ezt a funkciót egy `search` nevű
függvényben adjuk hozzá.

### Elbukó teszt írása {#writing-a-failing-test}

A _src/lib.rs_ fájlban hozzáadunk egy `tests` modult egy tesztfüggvénnyel,
ahogy a [11. fejezetben][ch11-anatomy]<!-- ignore --> is tettük. A
tesztfüggvény azt a viselkedést határozza meg, amelyet a `search`
függvénytől elvárunk: kap egy keresett kifejezést és egy szöveget, amelyben
keresni kell, és csak azokat a sorokat adja vissza a szövegből, amelyek
tartalmazzák a keresett kifejezést. A 12-15. kódrészlet mutatja ezt a tesztet.

<Listing number="12-15" file-name="src/lib.rs" caption="Elbukó teszt készítése a `search` függvényhez a kívánt funkcióra">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-15/src/lib.rs:here}}
```

</Listing>

Ez a teszt a `"duct"` sztringet keresi. A szöveg, amelyben keresünk, három
sorból áll, és ezek közül csak egy tartalmazza a `"duct"` sztringet (figyeld
meg, hogy a nyitó idézőjel utáni fordított perjel azt mondja a Rustnak, hogy
ne tegyen újsor karaktert a sztringliterál tartalmának elejére). Azt
ellenőrizzük, hogy a `search` függvény által visszaadott érték csak az
általunk várt sort tartalmazza.

Ha most lefuttatjuk ezt a tesztet, el fog bukni, mert az `unimplemented!`
makró a „not implemented” üzenettel pánikol. A TDD elveinek megfelelően egy
kis lépést teszünk: éppen annyi kódot adunk hozzá, hogy a teszt ne
pánikoljon a függvény meghívásakor, mégpedig úgy, hogy a `search` függvényt
mindig üres vektort visszaadóként definiáljuk, ahogy a 12-16. kódrészlet
mutatja. Ezután a tesztnek le kell fordulnia, és el kell buknia, mert egy
üres vektor nem egyezik egy olyan vektorral, amely a `"safe, fast,
productive."` sort tartalmazza.

<Listing number="12-16" file-name="src/lib.rs" caption="A `search` függvény éppen annyira definiálva, hogy a meghívása ne okozzon pánikot">

```rust,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-16/src/lib.rs:here}}
```

</Listing>

Most beszéljük meg, miért kell a `search` szignatúrájában egy explicit `'a`
élettartamot definiálnunk, és ezt az élettartamot a `contents` argumentummal
és a visszatérési értékkel használnunk. Emlékezz vissza: a
[10. fejezetben][ch10-lifetimes]<!-- ignore --> láttuk, hogy az
élettartam-paraméterek határozzák meg, melyik argumentum élettartama
kapcsolódik a visszatérési érték élettartamához. Ebben az esetben azt
jelezzük, hogy a visszaadott vektor olyan sztringszeleteket tartalmaz,
amelyek a `contents` argumentum (és nem a `query` argumentum) szeleteire
hivatkoznak.

Más szóval azt mondjuk a Rustnak, hogy a `search` függvény által
visszaadott adatok addig élnek, ameddig a `search` függvénynek a `contents`
argumentumban átadott adatok. Ez fontos! A szelet _által_ hivatkozott
adatoknak érvényesnek kell lenniük ahhoz, hogy a referencia érvényes legyen;
ha a fordító azt feltételezi, hogy a `contents` helyett a `query`-ből
készítünk sztringszeleteket, helytelenül végzi el a biztonsági
ellenőrzéseit.

Ha elfelejtjük az élettartam-annotációkat, és megpróbáljuk lefordítani ezt
a függvényt, a következő hibát kapjuk:

```console
{{#include ../listings/ch12-an-io-project/output-only-02-missing-lifetimes/output.txt}}
```

A Rust nem tudhatja, hogy a két paraméter közül melyikre van szükségünk a
kimenethez, ezért ezt kifejezetten meg kell mondanunk neki. Figyeld meg,
hogy a súgószöveg azt javasolja, hogy minden paraméterhez és a kimeneti
típushoz is ugyanazt az élettartam-paramétert adjuk meg, ami helytelen!
Mivel a `contents` az a paraméter, amely a teljes szövegünket tartalmazza,
és ennek a szövegnek az illeszkedő részeit szeretnénk visszaadni, tudjuk,
hogy egyedül a `contents` paramétert kell az élettartam-szintaxissal a
visszatérési értékhez kapcsolni.

Más programozási nyelvekben nem kell a szignatúrában összekapcsolni az
argumentumokat a visszatérési értékekkel, de ez a gyakorlat idővel egyre
könnyebb lesz. Érdemes lehet összevetned ezt a példát a 10. fejezet
[„Referenciák ellenőrzése
élettartamokkal”][validating-references-with-lifetimes]<!-- ignore -->
szakaszának példáival.

### A tesztet teljesítő kód írása {#writing-code-to-pass-the-test}

A tesztünk jelenleg elbukik, mert mindig üres vektort adunk vissza. Ahhoz,
hogy ezt kijavítsuk, és megvalósítsuk a `search` függvényt, a programunknak
a következő lépéseket kell végrehajtania:

1. Végigmegy a tartalom minden során.
2. Ellenőrzi, hogy a sor tartalmazza-e a keresett sztringet.
3. Ha igen, hozzáadja a visszaadandó értékek listájához.
4. Ha nem, nem tesz semmit.
5. Visszaadja az illeszkedő eredmények listáját.

Haladjunk végig az egyes lépéseken, kezdve a sorok bejárásával.

#### A sorok bejárása a `lines` metódussal {#iterating-through-lines-with-the-lines-method}

A Rustnak van egy hasznos metódusa a sztringek soronkénti bejárására, amely
találó módon a `lines` nevet viseli, és a 12-17. kódrészletben látható módon
működik. Vedd figyelembe, hogy ez még nem fordul le.

<Listing number="12-17" file-name="src/lib.rs" caption="A `contents` minden sorának bejárása">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-17/src/lib.rs:here}}
```

</Listing>

A `lines` metódus egy iterátort ad vissza. Az iterátorokról a
[13. fejezetben][ch13-iterators]<!-- ignore --> beszélünk részletesen. De
emlékezz vissza: az iterátorok ilyen használatát már láttad a
[3-5. kódrészletben][ch3-iter]<!-- ignore -->, ahol egy `for` ciklust
használtunk egy iterátorral, hogy egy gyűjtemény minden elemén lefuttassunk
valamilyen kódot.

#### A keresett kifejezés keresése az egyes sorokban {#searching-each-line-for-the-query}

Ezután ellenőrizzük, hogy az aktuális sor tartalmazza-e a keresett
sztringet. Szerencsére a sztringeknek van egy hasznos, `contains` nevű
metódusuk, amely ezt elvégzi helyettünk! Adj hozzá egy `contains`
metódushívást a `search` függvényhez a 12-18. kódrészletben látható módon.
Vedd figyelembe, hogy ez még mindig nem fordul le.

<Listing number="12-18" file-name="src/lib.rs" caption="Annak ellenőrzése, hogy a sor tartalmazza-e a `query`-ben lévő sztringet">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-18/src/lib.rs:here}}
```

</Listing>

Jelenleg a funkciót építjük fel lépésről lépésre. Ahhoz, hogy a kód
leforduljon, vissza kell adnunk egy értéket a törzsből, ahogy a függvény
szignatúrájában jeleztük.

#### Az illeszkedő sorok tárolása {#storing-matching-lines}

A függvény befejezéséhez szükségünk van egy módra, amellyel tárolhatjuk a
visszaadni kívánt illeszkedő sorokat. Ehhez a `for` ciklus előtt
létrehozhatunk egy módosítható vektort, és a `push` metódus meghívásával
eltárolhatunk benne egy-egy `line`-t. A `for` ciklus után visszaadjuk a
vektort, ahogy a 12-19. kódrészlet mutatja.

<Listing number="12-19" file-name="src/lib.rs" caption="Az illeszkedő sorok tárolása, hogy visszaadhassuk őket">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-19/src/lib.rs:here}}
```

</Listing>

Most a `search` függvénynek csak azokat a sorokat kell visszaadnia, amelyek
tartalmazzák a `query`-t, és a tesztünknek sikeresnek kell lennie. Futtassuk
le a tesztet:

```console
{{#include ../listings/ch12-an-io-project/listing-12-19/output.txt}}
```

A tesztünk sikeres, tehát tudjuk, hogy a kód működik!

Ezen a ponton elgondolkodhatnánk azon, hogyan refaktorálhatnánk a
keresőfüggvény megvalósítását úgy, hogy a tesztek sikeresek maradjanak, és
így a működés is változatlan legyen. A keresőfüggvény kódja nem rossz, de
nem használja ki az iterátorok néhány hasznos lehetőségét. A
[13. fejezetben][ch13-iterators]<!-- ignore --> visszatérünk erre a példára,
ahol részletesen megismerjük az iterátorokat, és megnézzük, hogyan
javíthatunk rajta.

Most már az egész programnak működnie kell! Próbáljuk ki, először egy olyan
szóval, amely pontosan egy sort ad vissza Emily Dickinson verséből: _frog_.

```console
{{#include ../listings/ch12-an-io-project/no-listing-02-using-search-in-run/output.txt}}
```

Klassz! Most próbáljunk ki egy olyan szót, amely több sorra is illeszkedik,
például a _body_-t:

```console
{{#include ../listings/ch12-an-io-project/output-only-03-multiple-matches/output.txt}}
```

Végül győződjünk meg arról, hogy nem kapunk egyetlen sort sem, ha olyan szóra
keresünk, amely sehol sem szerepel a versben, például a
_monomorphization_-re:

```console
{{#include ../listings/ch12-an-io-project/output-only-04-no-matches/output.txt}}
```

Kiváló! Elkészítettük egy klasszikus eszköz saját mini változatát, és sokat
tanultunk arról, hogyan strukturáljuk az alkalmazásokat. Egy keveset a fájlok
beolvasásáról és írásáról, az élettartamokról, a tesztelésről és a
parancssor feldolgozásáról is megtanultunk.

A projekt lezárásaként röviden bemutatjuk, hogyan dolgozhatunk környezeti
változókkal, és hogyan írhatunk a standard hibakimenetre; mindkettő hasznos,
amikor parancssori programokat írsz.

[validating-references-with-lifetimes]: ch10-03-lifetime-syntax.html#validating-references-with-lifetimes
[ch11-anatomy]: ch11-01-writing-tests.html#the-anatomy-of-a-test-function
[ch10-lifetimes]: ch10-03-lifetime-syntax.html
[ch3-iter]: ch03-05-control-flow.html#looping-through-a-collection-with-for
[ch13-iterators]: ch13-02-iterators.html
