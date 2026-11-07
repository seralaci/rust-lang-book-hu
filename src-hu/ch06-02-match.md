<!-- Old headings. Do not remove or links may break. -->

<a id="the-match-control-flow-operator"></a>

## A `match` vezérlési szerkezet {#the-match-control-flow-construct}

A Rustban van egy rendkívül hatékony vezérlési szerkezet, a `match`, amellyel
egy értéket mintákból (patterns) álló sorozattal vethetsz össze, majd attól
függően futtathatsz kódot, hogy melyik minta illeszkedik. A minták állhatnak
literálokból, változónevekből, helyettesítő jelekből (wildcards) és sok minden
másból; a [19. fejezet][ch19-00-patterns]<!-- ignore --> az összes mintafajtát
és azok működését bemutatja. A `match` ereje a minták kifejezőképességéből
fakad, valamint abból, hogy a fordító ellenőrzi, minden lehetséges eset
kezelve van-e.

Képzeld el a `match` kifejezést úgy, mint egy érmeválogató gépet: az érmék egy
pályán csúsznak le, amely mentén különböző méretű lyukak vannak, és minden érme
az első olyan lyukon esik át, amelybe belefér. Ugyanígy az értékek is
végighaladnak a `match` egyes mintáin, és az első olyan mintánál, amelybe az
érték „belefér”, az érték a hozzá tartozó kódblokkba esik, és ott a végrehajtás
során felhasználható.

Ha már az érméknél tartunk, használjuk őket példaként a `match`-hez! Írhatunk
egy függvényt, amely egy ismeretlen amerikai érmét kap, és a számlálógéphez
hasonlóan megállapítja, melyik érméről van szó, majd visszaadja az értékét
centben, ahogy a 6-3. kódrészlet mutatja.

<Listing number="6-3" caption="Egy enum és egy `match` kifejezés, amelynek mintái az enum változatai">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-03/src/main.rs:here}}
```

</Listing>

Bontsuk részeire a `value_in_cents` függvényben lévő `match`-et! Először a
`match` kulcsszót írjuk, majd utána egy kifejezést, amely ebben az esetben a
`coin` érték. Ez nagyon hasonlít az `if`-fel használt feltételes kifejezésre,
de van egy nagy különbség: az `if` esetén a feltételnek logikai értékre kell
kiértékelődnie, itt viszont bármilyen típus lehet. A `coin` típusa ebben a
példában az első sorban definiált `Coin` enum.

Ezután következnek a `match` ágai (arms). Egy ág két részből áll: egy mintából
és némi kódból. Az első ág mintája itt a `Coin::Penny` érték, utána pedig a
`=>` operátor következik, amely elválasztja a mintát a futtatandó kódtól. A
kód ebben az esetben csak az `1` érték. Az egyes ágakat vessző választja el
egymástól.

Amikor a `match` kifejezés lefut, az eredményül kapott értéket sorban
összeveti az egyes ágak mintájával. Ha egy minta illeszkedik az értékre, a
hozzá tartozó kód végrehajtódik. Ha a minta nem illeszkedik, a végrehajtás a
következő ággal folytatódik, akárcsak egy érmeválogató gépben. Annyi águnk
lehet, amennyire szükségünk van: a 6-3. kódrészletben a `match`-nek négy ága
van.

Az egyes ágakhoz tartozó kód egy kifejezés, és az illeszkedő ágban lévő
kifejezés eredménye lesz az egész `match` kifejezés visszaadott értéke.

Ha a match ág kódja rövid, általában nem használunk kapcsos zárójelet, ahogy a
6-3. kódrészletben sem, ahol minden ág csak egy értéket ad vissza. Ha egy match
ágban több sornyi kódot szeretnél futtatni, kapcsos zárójelet kell használnod,
és ilyenkor az ág utáni vessző elhagyható. Az alábbi kód például minden
alkalommal kiírja, hogy „Lucky penny!”, amikor a metódust egy `Coin::Penny`
értékkel hívjuk meg, de továbbra is a blokk utolsó értékét, az `1`-et adja
vissza:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-08-match-arm-multiple-lines/src/main.rs:here}}
```

### Értékekhez kötő minták {#patterns-that-bind-to-values}

A match ágak egy másik hasznos tulajdonsága, hogy hozzá tudnak kötni (bind)
változókat az értékek mintára illeszkedő részeihez. Így tudunk értékeket
kinyerni az enumváltozatokból.

Példaként alakítsuk át az egyik enumváltozatunkat úgy, hogy adatot tároljon!
Az Egyesült Államok 1999 és 2008 között olyan 25 centes érméket (quarter)
vert, amelyek egyik oldalán mind az 50 államnak saját mintázata volt. Más
érmék nem kaptak állami mintázatot, így csak a 25 centesekhez tartozik ez a
többletérték. Ezt az információt úgy adhatjuk hozzá az `enum`-unkhoz, hogy a
`Quarter` változatot egy benne tárolt `UsState` értékkel bővítjük, ahogy a 6-4.
kódrészletben tettük.

<Listing number="6-4" caption="Egy `Coin` enum, amelyben a `Quarter` változat egy `UsState` értéket is tárol">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-04/src/main.rs:here}}
```

</Listing>

Képzeljük el, hogy egy barátunk mind az 50 állam 25 centesét szeretné
összegyűjteni. Miközben az aprópénzünket érmefajták szerint válogatjuk, minden
25 centesnél bemondjuk a hozzá tartozó állam nevét is, hogy ha olyan, amelyik
még hiányzik a barátunknak, hozzáadhassa a gyűjteményéhez.

A kód match kifejezésében a `Coin::Quarter` változat értékeire illeszkedő
mintához hozzáadunk egy `state` nevű változót. Amikor egy `Coin::Quarter`
illeszkedik, a `state` változó az adott 25 centes államának értékéhez kötődik.
Ezután a `state`-et használhatjuk az adott ág kódjában, így:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-09-variable-in-pattern/src/main.rs:here}}
```

Ha meghívnánk a `value_in_cents(Coin::Quarter(UsState::Alaska))` függvényt, a
`coin` értéke `Coin::Quarter(UsState::Alaska)` lenne. Amikor ezt az értéket
összevetjük az egyes match ágakkal, egyik sem illeszkedik, amíg el nem érjük a
`Coin::Quarter(state)` ágat. Ekkor a `state` kötés (binding) értéke
`UsState::Alaska` lesz. Ezt a kötést aztán felhasználhatjuk a `println!`
kifejezésben, így kinyerve a belső állam értéket a `Coin` enum `Quarter`
változatából.

<!-- Old headings. Do not remove or links may break. -->

<a id="matching-with-optiont"></a>

### Az `Option<T>` `match` mintája {#the-optiont-match-pattern}


Az előző szakaszban a `Some` esetből szerettük volna kinyerni a belső `T`
értéket, amikor `Option<T>`-t használunk; az `Option<T>`-t is kezelhetjük a
`match` segítségével, ahogy a `Coin` enummal tettük! Érmék helyett az
`Option<T>` változatait vetjük össze, de a `match` kifejezés működése
ugyanaz marad.

Tegyük fel, hogy olyan függvényt szeretnénk írni, amely egy `Option<i32>`
értéket kap, és ha van benne érték, hozzáad 1-et. Ha nincs benne érték, a
függvény adja vissza a `None` értéket, és ne próbáljon semmilyen műveletet
végezni.

A `match`-nek köszönhetően ezt a függvényt nagyon könnyű megírni; a 6-5.
kódrészlethez hasonlóan fog kinézni.

<Listing number="6-5" caption="Egy függvény, amely `match` kifejezést használ egy `Option<i32>` értéken">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-05/src/main.rs:here}}
```

</Listing>

Vizsgáljuk meg részletesebben a `plus_one` első végrehajtását! Amikor
meghívjuk a `plus_one(five)` függvényt, a `plus_one` törzsében az `x` változó
értéke `Some(5)` lesz. Ezt összevetjük az egyes match ágakkal:

```rust,ignore
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-05/src/main.rs:first_arm}}
```

A `Some(5)` érték nem illeszkedik a `None` mintára, így a következő ággal
folytatjuk:

```rust,ignore
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-05/src/main.rs:second_arm}}
```

Illeszkedik-e a `Some(5)` a `Some(i)` mintára? Igen! Ugyanaz a változat. Az `i`
a `Some`-ban lévő értékhez kötődik, így az `i` értéke `5` lesz. Ezután a match
ág kódja végrehajtódik: hozzáadunk 1-et az `i` értékéhez, és létrehozunk egy új
`Some` értéket, amelyben az összeg, a `6` található.

Most nézzük meg a `plus_one` második hívását a 6-5. kódrészletben, ahol az `x`
értéke `None`. Belépünk a `match`-be, és összevetjük az első ággal:

```rust,ignore
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-05/src/main.rs:first_arm}}
```

Illeszkedik! Nincs érték, amihez hozzáadhatnánk, így a program megáll, és a
`=>` jobb oldalán lévő `None` értéket adja vissza. Mivel az első ág
illeszkedett, a többi ággal már nem történik összevetés.

A `match` és az enumok kombinálása sok helyzetben hasznos. Ezzel a mintával
sokszor találkozol majd a Rust-kódokban: `match` egy enumon, egy változó
hozzákötése a benne lévő adathoz, majd ennek alapján kód végrehajtása. Elsőre
kicsit trükkös, de ha egyszer megszokod, minden nyelvben hiányozni fog. A
felhasználók kedvence, és az is marad.

### A `match` kimerítő {#matches-are-exhaustive}

A `match`-nek van még egy szempontja, amelyről beszélnünk kell: az ágak
mintáinak minden lehetőséget le kell fedniük. Nézzük a `plus_one`
függvényünknek ezt a változatát, amely hibás, és nem fordul le:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-10-non-exhaustive-match/src/main.rs:here}}
```

Nem kezeltük a `None` esetet, így ez a kód hibát okoz. Szerencsére ez olyan
hiba, amelyet a Rust el tud kapni. Ha megpróbáljuk lefordítani ezt a kódot,
ezt a hibát kapjuk:

```console
{{#include ../listings/ch06-enums-and-pattern-matching/no-listing-10-non-exhaustive-match/output.txt}}
```

A Rust tudja, hogy nem fedtünk le minden lehetséges esetet, sőt azt is tudja,
melyik mintát felejtettük el! A Rustban a `match` _kimerítő (exhaustive)_:
minden egyes lehetőséget ki kell merítenünk ahhoz, hogy a kód érvényes legyen.
Különösen az `Option<T>` esetén, amikor a Rust megakadályozza, hogy
elfelejtsük kifejezetten kezelni a `None` esetet, megvéd attól, hogy
feltételezzük, hogy van értékünk, amikor valójában nullunk lehet – így
lehetetlenné teszi a korábban tárgyalt milliárd dolláros hibát.

### Mindent elfogó minták és a `_` helyőrző {#catch-all-patterns-and-the-_-placeholder}

Enumokkal azt is megtehetjük, hogy néhány konkrét értéknél különleges
műveletet végzünk, minden más értéknél pedig egy alapértelmezett műveletet.
Képzeld el, hogy egy játékot írunk, amelyben ha a kockadobásod 3, a játékosod
nem lép, hanem kap egy új, díszes kalapot. Ha 7-et dobsz, a játékosod elveszít
egy díszes kalapot. Minden más értéknél a játékosod annyi mezőt lép előre a
játéktáblán. Íme egy `match`, amely ezt a logikát valósítja meg; a kockadobás
eredménye véletlenszerű érték helyett be van égetve a kódba, a többi logikát
pedig törzs nélküli függvények jelképezik, mert a tényleges megvalósításuk
túlmutat ennek a példának a keretein:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-15-binding-catchall/src/main.rs:here}}
```

Az első két ág mintái a `3` és a `7` literálok. Az utolsó ágnál, amely minden
más lehetséges értéket lefed, a minta egy változó, amelynek az `other` nevet
adtuk. Az `other` ágban futó kód úgy használja a változót, hogy átadja a
`move_player` függvénynek.

Ez a kód lefordul, bár nem soroltuk fel az összes lehetséges értéket, amelyet
egy `u8` felvehet, mert az utolsó minta minden olyan értékre illeszkedik,
amelyet nem soroltunk fel kifejezetten. Ez a mindent elfogó minta (catch-all
pattern) kielégíti azt a követelményt, hogy a `match`-nek kimerítőnek kell
lennie. Figyeld meg, hogy a mindent elfogó ágat utolsónak kell írnunk, mert a
minták kiértékelése sorrendben történik. Ha a mindent elfogó ágat korábbra
tennénk, a többi ág soha nem futna le, ezért a Rust figyelmeztet, ha egy
mindent elfogó ág után további ágakat adunk meg!

A Rustban van egy olyan minta is, amelyet akkor használhatunk, ha mindent el
akarunk fogni, de a mindent elfogó mintában lévő értéket nem akarjuk
_felhasználni_: a `_` egy különleges minta, amely bármilyen értékre illeszkedik,
de nem köt hozzá változót. Ezzel jelezzük a Rustnak, hogy nem fogjuk használni
az értéket, így a Rust nem figyelmeztet fel nem használt változó miatt.

Változtassunk a játékszabályokon: mostantól ha 3-on vagy 7-en kívül bármi mást
dobsz, újra kell dobnod. A mindent elfogó értéket már nem kell felhasználnunk,
így a kódunkban az `other` nevű változó helyett `_`-t használhatunk:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-16-underscore-catchall/src/main.rs:here}}
```

Ez a példa is teljesíti a kimerítőség követelményét, mert az utolsó ágban
kifejezetten figyelmen kívül hagyunk minden más értéket; semmit sem
felejtettünk el.

Végül még egyszer megváltoztatjuk a játékszabályokat: ha 3-on vagy 7-en kívül
bármi mást dobsz, a körödben semmi más nem történik. Ezt úgy fejezhetjük ki,
hogy a `_` ághoz tartozó kódként a unit értéket (az üres tuple típust, amelyet
[„A tuple típus”][tuples]<!-- ignore --> szakaszban említettünk) használjuk:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-17-underscore-unit/src/main.rs:here}}
```

Itt kifejezetten közöljük a Rusttal, hogy semmilyen más értéket nem fogunk
használni, amely nem illeszkedik egy korábbi ág mintájára, és ebben az esetben
semmilyen kódot nem akarunk futtatni.

A mintákról és az illesztésről a [19.
fejezetben][ch19-00-patterns]<!-- ignore --> lesz még szó. Most továbblépünk
az `if let` szintaxisra, amely olyan helyzetekben lehet hasznos, amikor a
`match` kifejezés kissé bőbeszédű.

[tuples]: ch03-02-data-types.html#the-tuple-type
[ch19-00-patterns]: ch19-00-patterns.html
