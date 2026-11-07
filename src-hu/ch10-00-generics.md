# Generikus típusok, traitek és élettartamok {#generic-types-traits-and-lifetimes}

Minden programozási nyelvben vannak eszközök a fogalmak ismétlődésének
hatékony kezelésére. A Rustban az egyik ilyen eszköz a _generikus típusok
(generics)_ köre: konkrét típusok vagy más tulajdonságok absztrakt
helyettesítői.
Kifejezhetjük a generikus típusok viselkedését, illetve azt, hogyan kapcsolódnak
más generikus típusokhoz, anélkül hogy tudnánk, mi kerül majd a helyükre a kód
fordításakor és futtatásakor.

A függvények egy konkrét típus, például az `i32` vagy a `String` helyett
valamilyen generikus típusú paramétert is kaphatnak, ugyanúgy, ahogy ismeretlen
értékű paramétereket kapnak, hogy ugyanazt a kódot több konkrét értéken is
lefuttathassák. Valójában már használtunk generikus típusokat: a 6. fejezetben
az `Option<T>`-t, a 8. fejezetben a `Vec<T>`-t és a `HashMap<K, V>`-t, a 9.
fejezetben pedig a `Result<T, E>`-t. Ebben a fejezetben megismered, hogyan
definiálhatsz saját típusokat, függvényeket és metódusokat generikus típusokkal!

Először áttekintjük, hogyan emelhetünk ki egy függvényt a kódismétlés
csökkentésére. Ezután ugyanezzel a módszerrel két olyan függvényből, amelyek
csak a paramétereik típusában különböznek, egy generikus függvényt készítünk.
Azt is elmagyarázzuk, hogyan használhatunk generikus típusokat struktúra- és
enumdefiníciókban.

Ezután megtanulod, hogyan definiálhatsz viselkedést generikus módon traitek
segítségével. A traiteket generikus típusokkal kombinálva korlátozhatod, hogy
egy generikus típus ne akármilyen típust fogadjon el, hanem csak azokat,
amelyek rendelkeznek egy bizonyos viselkedéssel.

Végül az _élettartamokról (lifetimes)_ lesz szó: ezek a generikus típusok egy
olyan fajtája, amely arról ad információt a fordítónak, hogyan viszonyulnak
egymáshoz a referenciák. Az élettartamokkal elég információt adhatunk a
fordítónak a kölcsönzött értékekről ahhoz, hogy több helyzetben is
garantálhassa a referenciák érvényességét, mint amennyiben a segítségünk
nélkül tudná.

## Az ismétlődés megszüntetése egy függvény kiemelésével {#removing-duplication-by-extracting-a-function}

A generikus típusokkal a konkrét típusokat egy olyan helyőrzővel cserélhetjük
le, amely több típust képvisel, és így megszüntethetjük a kódismétlést. Mielőtt
belemerülnénk a generikus típusok szintaxisába, nézzük meg először, hogyan
szüntethetjük meg az ismétlődést generikus típusok nélkül: egy olyan függvény
kiemelésével, amely a konkrét értékeket egy több értéket képviselő helyőrzővel
helyettesíti. Ezután ugyanezt a módszert alkalmazzuk egy generikus függvény
kiemelésére! Ha megtanulod felismerni a függvénybe kiemelhető ismétlődő kódot,
azt az ismétlődő kódot is fel fogod ismerni, amelyben generikus típusokat
használhatsz.

Kezdjük a 10-1. kódrészlet rövid programjával, amely megkeresi egy lista
legnagyobb számát.

<Listing number="10-1" file-name="src/main.rs" caption="Egy számlista legnagyobb számának megkeresése">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-01/src/main.rs:here}}
```

</Listing>

Egész számok egy listáját a `number_list` változóban tároljuk, a lista első
számára mutató referenciát pedig egy `largest` nevű változóba tesszük. Ezután
végigmegyünk a lista összes számán, és ha az aktuális szám nagyobb, mint a
`largest`-ben tárolt szám, lecseréljük a változóban lévő referenciát. Ha
viszont az aktuális szám kisebb vagy egyenlő az eddig látott legnagyobb
számmal, a változó nem módosul, és a kód a lista következő számára lép. Miután
a lista összes számát megvizsgáltuk, a `largest`-nek a legnagyobb számra kell
hivatkoznia, ami ebben az esetben a 100.

Most az a feladatunk, hogy két különböző számlistában keressük meg a
legnagyobb számot. Ehhez megtehetjük, hogy lemásoljuk a 10-1. kódrészlet kódját,
és ugyanazt a logikát a program két különböző pontján használjuk, ahogy a 10-2.
kódrészlet mutatja.

<Listing number="10-2" file-name="src/main.rs" caption="Kód, amely *két* számlistában keresi meg a legnagyobb számot">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-02/src/main.rs}}
```

</Listing>

Bár ez a kód működik, a kód ismétlése fárasztó és hibalehetőségeket rejt.
Arra is emlékeznünk kell, hogy ha módosítani akarjuk a kódot, több helyen
kell frissítenünk.

Az ismétlődés megszüntetésére egy absztrakciót hozunk létre: definiálunk egy
függvényt, amely bármilyen, paraméterként átadott egészszám-listán működik. Ez
a megoldás érthetőbbé teszi a kódot, és lehetővé teszi, hogy a lista legnagyobb
számának megkeresését absztrakt módon fejezzük ki.

A 10-3. kódrészletben a legnagyobb számot megkereső kódot egy `largest` nevű
függvénybe emeljük ki. Ezután meghívjuk a függvényt, hogy megkeressük a
legnagyobb számot a 10-2. kódrészlet két listájában. A függvényt bármely más,
`i32` értékekből álló listán is használhatnánk, amely a jövőben a kezünkbe
kerül.

<Listing number="10-3" file-name="src/main.rs" caption="Absztrakt kód, amely két listában keresi meg a legnagyobb számot">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-03/src/main.rs:here}}
```

</Listing>

A `largest` függvénynek van egy `list` nevű paramétere, amely `i32` értékek
bármely konkrét szeletét képviseli, amelyet átadhatunk a függvénynek. Ennek
eredményeként a függvény meghívásakor a kód azokon a konkrét értékeken fut le,
amelyeket átadunk neki.

Összefoglalva, ezeket a lépéseket tettük, hogy a 10-2. kódrészlet kódjából a
10-3. kódrészlet kódja legyen:

1. Azonosítsuk az ismétlődő kódot.
1. Emeljük ki az ismétlődő kódot a függvény törzsébe, és adjuk meg a kód
   bemeneteit és visszatérési értékeit a függvény szignatúrájában.
1. Frissítsük az ismétlődő kód két előfordulását úgy, hogy helyettük a
   függvényt hívják meg.

Most ugyanezeket a lépéseket alkalmazzuk generikus típusokkal a kódismétlés
csökkentésére. Ahogy a függvénytörzs konkrét értékek helyett egy absztrakt
`list`-en dolgozhat, úgy a generikus típusok lehetővé teszik, hogy a kód
absztrakt típusokon dolgozzon.

Tegyük fel például, hogy két függvényünk van: az egyik egy `i32` értékekből
álló szelet legnagyobb elemét keresi meg, a másik egy `char` értékekből álló
szeletét. Hogyan szüntethetnénk meg ezt az ismétlődést? Derítsük ki!
