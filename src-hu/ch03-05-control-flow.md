## Vezérlési szerkezetek {#control-flow}

Az, hogy egy kódrészletet attól függően futtathatunk, hogy egy feltétel `true`
értékű-e, valamint hogy egy kódrészletet ismételten futtathatunk, amíg egy
feltétel `true`, a legtöbb programozási nyelv alapvető építőkövei közé
tartozik. A Rust-kód végrehajtásának menetét leggyakrabban az `if`
kifejezésekkel és a ciklusokkal irányíthatod.

### `if` kifejezések {#if-expressions}

Az `if` kifejezéssel feltételektől függően ágaztathatod el a kódodat. Megadsz
egy feltételt, majd kijelented: „Ha ez a feltétel teljesül, futtasd ezt a
kódblokkot. Ha a feltétel nem teljesül, ne futtasd ezt a kódblokkot.”

Hozz létre egy új, _branches_ nevű projektet a _projects_ mappádban, hogy
megismerkedj az `if` kifejezéssel. Az _src/main.rs_ fájlba írd be a
következőt:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-26-if-true/src/main.rs}}
```

Minden `if` kifejezés az `if` kulcsszóval kezdődik, amelyet egy feltétel
követ. Ebben az esetben a feltétel azt vizsgálja, hogy a `number` változó
értéke kisebb-e 5-nél. A feltétel `true` értéke esetén végrehajtandó
kódblokkot közvetlenül a feltétel után, kapcsos zárójelek közé tesszük. Az
`if` kifejezések feltételeihez tartozó kódblokkokat néha _ágaknak (arms)_ is
nevezik, akárcsak a `match` kifejezések ágait, amelyeket a 2. fejezet [„A tipp
összehasonlítása a titkos
számmal”][comparing-the-guess-to-the-secret-number]<!-- ignore --> című
szakaszában tárgyaltunk.

Opcionálisan egy `else` kifejezést is megadhatunk – itt ezt választottuk –,
hogy a programnak legyen egy alternatív végrehajtandó kódblokkja arra az
esetre, ha a feltétel `false` értékre értékelődik ki. Ha nem adsz meg `else`
kifejezést, és a feltétel `false`, a program egyszerűen átugorja az `if`
blokkot, és a kód következő részével folytatja.

Próbáld meg futtatni ezt a kódot; a következő kimenetet kell látnod:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-26-if-true/output.txt}}
```

Próbáljuk meg a `number` értékét olyanra változtatni, amely mellett a feltétel
`false` lesz, és nézzük meg, mi történik:

```rust,ignore
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-27-if-false/src/main.rs:here}}
```

Futtasd újra a programot, és nézd meg a kimenetet:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-27-if-false/output.txt}}
```

Azt is érdemes megjegyezni, hogy ebben a kódban a feltételnek _kötelezően_
`bool` típusúnak kell lennie. Ha a feltétel nem `bool`, hibát kapunk. Próbáld
meg például a következő kódot futtatni:

<span class="filename">Fájlnév: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-28-if-condition-must-be-bool/src/main.rs}}
```

Az `if` feltétele ezúttal a `3` értékre értékelődik ki, és a Rust hibát jelez:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-28-if-condition-must-be-bool/output.txt}}
```

A hiba azt jelzi, hogy a Rust `bool`-t várt, de egész számot kapott. Az olyan
nyelvekkel ellentétben, mint a Ruby és a JavaScript, a Rust nem próbálja meg
automatikusan logikai értékké alakítani a nem logikai típusokat. Ezt
kifejezetten meg kell adnod, és az `if` feltételeként mindig logikai értéket
kell megadnod. Ha például azt szeretnénk, hogy az `if` kódblokkja csak akkor
fusson le, ha egy szám nem egyenlő `0`-val, az `if` kifejezést a következőre
módosíthatjuk:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-29-if-not-equal-0/src/main.rs}}
```

A kód futtatása a `number was something other than zero` szöveget írja ki.

#### Több feltétel kezelése `else if`-fel {#handling-multiple-conditions-with-else-if}

Több feltételt is használhatsz, ha az `if`-et és az `else`-t egy `else if`
kifejezésben kombinálod. Például:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-30-else-if/src/main.rs}}
```

Ennek a programnak négy lehetséges útja van. Futtatás után a következő
kimenetet kell látnod:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-30-else-if/output.txt}}
```

Amikor ez a program fut, sorra megvizsgálja az egyes `if` kifejezéseket, és az
első olyan törzset hajtja végre, amelynek feltétele `true` értékre értékelődik
ki. Figyeld meg, hogy bár a 6 osztható 2-vel, nem látjuk a `number is
divisible by 2` kimenetet, és az `else` blokkból származó `number is not
divisible by 4, 3, or 2` szöveget sem. Ennek az az oka, hogy a Rust csak az
első `true` feltételhez tartozó blokkot hajtja végre, és ha talált egyet, a
többit már meg sem vizsgálja.

A túl sok `else if` kifejezés zsúfolttá teheti a kódodat, ezért ha egynél több
van belőlük, érdemes lehet refaktorálnod a kódot. A 6. fejezet egy hatékony
Rust-elágazási szerkezetet mutat be ezekre az esetekre, a `match`-et.

#### Az `if` használata `let` utasításban {#using-if-in-a-let-statement}

Mivel az `if` kifejezés, egy `let` utasítás jobb oldalán is használhatjuk,
hogy az eredményét egy változóhoz rendeljük, ahogy a 3-2. kódrészletben
látható.

<Listing number="3-2" file-name="src/main.rs" caption="Egy `if` kifejezés eredményének hozzárendelése egy változóhoz">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-02/src/main.rs}}
```

</Listing>

A `number` változó az `if` kifejezés eredményétől függő értékhez kötődik.
Futtasd ezt a kódot, és nézd meg, mi történik:

```console
{{#include ../listings/ch03-common-programming-concepts/listing-03-02/output.txt}}
```

Ne feledd, hogy a kódblokkok a bennük lévő utolsó kifejezés értékére
értékelődnek ki, és a számok önmagukban is kifejezések. Ebben az esetben a
teljes `if` kifejezés értéke attól függ, melyik kódblokk hajtódik végre. Ez azt
jelenti, hogy az `if` egyes ágaiból potenciálisan származó értékeknek azonos
típusúaknak kell lenniük; a 3-2. kódrészletben az `if` ág és az `else` ág
eredménye is `i32` típusú egész szám volt. Ha a típusok nem egyeznek, ahogy a
következő példában, hibát kapunk:

<span class="filename">Fájlnév: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-31-arms-must-return-same-type/src/main.rs}}
```

Amikor megpróbáljuk lefordítani ezt a kódot, hibát kapunk. Az `if` és az
`else` ág értékeinek típusa nem összeegyeztethető, és a Rust pontosan
megmutatja, hol található a probléma a programban:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-31-arms-must-return-same-type/output.txt}}
```

Az `if` blokkban lévő kifejezés egész számra, az `else` blokkban lévő
kifejezés pedig sztringre értékelődik ki. Ez nem működik, mert a változóknak
egyetlen típusuk lehet, és a Rustnak fordítási időben biztosan tudnia kell,
milyen típusú a `number` változó. Ha a fordító ismeri a `number` típusát,
ellenőrizni tudja, hogy a típus mindenhol érvényes, ahol a `number`-t
használjuk. A Rust erre nem lenne képes, ha a `number` típusa csak futásidőben
dőlne el; a fordító bonyolultabb lenne, és kevesebb garanciát tudna nyújtani a
kódra, ha bármely változóhoz több feltételezett típust is nyilván kellene
tartania.

### Ismétlés ciklusokkal {#repetition-with-loops}

Gyakran hasznos, ha egy kódblokkot többször is végrehajthatunk. Erre a
feladatra a Rust többféle _ciklust (loop)_ kínál, amelyek a ciklustörzsben
lévő kódot a végéig lefuttatják, majd azonnal újrakezdik az elejéről. A
ciklusokkal való kísérletezéshez hozzunk létre egy új, _loops_ nevű projektet.

A Rustban háromféle ciklus van: `loop`, `while` és `for`. Próbáljuk ki
mindegyiket.

#### Kód ismétlése a `loop`-pal {#repeating-code-with-loop}

A `loop` kulcsszó arra utasítja a Rustot, hogy egy kódblokkot újra és újra
végrehajtson, vagy örökké, vagy amíg kifejezetten meg nem mondod neki, hogy
álljon le.

Példaként módosítsd a _loops_ mappádban lévő _src/main.rs_ fájlt úgy, hogy így
nézzen ki:

<span class="filename">Fájlnév: src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-32-loop/src/main.rs}}
```

Amikor futtatjuk ezt a programot, azt látjuk, hogy az `again!` szöveg
folyamatosan, újra és újra kiíródik, amíg kézzel le nem állítjuk a programot.
A legtöbb terminál támogatja a <kbd>ctrl</kbd>-<kbd>C</kbd> billentyűparancsot
egy végtelen ciklusba ragadt program megszakítására. Próbáld ki:

<!-- manual-regeneration
cd listings/ch03-common-programming-concepts/no-listing-32-loop
cargo run
CTRL-C
-->

```console
$ cargo run
   Compiling loops v0.1.0 (file:///projects/loops)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.08s
     Running `target/debug/loops`
again!
again!
again!
again!
^Cagain!
```

A `^C` jel azt a pontot mutatja, ahol lenyomtad a
<kbd>ctrl</kbd>-<kbd>C</kbd> billentyűket.

Az is lehet, hogy a `^C` után még kiíródik az `again!` szó, de az is, hogy
nem; ez attól függ, hol tartott a kód a ciklusban, amikor megkapta a
megszakítási jelet.

Szerencsére a Rust arra is lehetőséget ad, hogy kódból lépjünk ki egy
ciklusból. A ciklusba helyezett `break` kulcsszóval megmondhatod a programnak,
mikor hagyja abba a ciklus végrehajtását. Emlékezz vissza, hogy ezt tettük a
találgatós játékban a 2. fejezet [„Kilépés helyes tipp
után”][quitting-after-a-correct-guess]<!-- ignore --> című szakaszában, hogy
kilépjünk a programból, amikor a felhasználó a helyes szám kitalálásával
megnyerte a játékot.

A találgatós játékban a `continue`-t is használtuk, amely egy ciklusban arra
utasítja a programot, hogy hagyja ki a ciklus aktuális iterációjában hátralévő
kódot, és lépjen a következő iterációra.

#### Értékek visszaadása ciklusokból {#returning-values-from-loops}

A `loop` egyik felhasználási módja egy olyan művelet újrapróbálása, amelyről
tudod, hogy meghiúsulhat, például annak ellenőrzése, hogy egy szál befejezte-e
a munkáját. Előfordulhat, hogy ennek a műveletnek az eredményét is ki kell
juttatnod a ciklusból a kód többi része számára. Ehhez a ciklust leállító
`break` kifejezés után megadhatod a visszaadni kívánt értéket; ez az érték
visszakerül a ciklusból, így felhasználhatod, ahogy itt látható:

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-33-return-value-from-loop/src/main.rs}}
```

A ciklus előtt deklarálunk egy `counter` nevű változót, és `0`-ra
inicializáljuk. Ezután deklarálunk egy `result` nevű változót, amely a
ciklusból visszaadott értéket tárolja. A ciklus minden iterációjában `1`-et
adunk a `counter` változóhoz, majd ellenőrizzük, hogy a `counter` egyenlő-e
`10`-zel. Ha igen, a `break` kulcsszót használjuk a `counter * 2` értékkel. A
ciklus után egy pontosvesszővel zárjuk le azt az utasítást, amely az értéket a
`result`-hoz rendeli. Végül kiírjuk a `result` értékét, ami ebben az esetben
`20`.

Egy cikluson belülről `return`-nel is visszatérhetsz. Míg a `break` csak az
aktuális ciklusból lép ki, a `return` mindig az aktuális függvényből lép ki.

<!-- Old headings. Do not remove or links may break. -->
<a id="loop-labels-to-disambiguate-between-multiple-loops"></a>

#### Egyértelműsítés cikluscímkékkel {#disambiguating-with-loop-labels}

Ha ciklusokat ágyazol egymásba, a `break` és a `continue` az adott ponton a
legbelső ciklusra vonatkozik. Egy ciklusnak opcionálisan _cikluscímkét (loop
label)_ is adhatsz, amelyet aztán a `break`-kel vagy a `continue`-val
használva megadhatod, hogy ezek a kulcsszavak a legbelső ciklus helyett a
megcímkézett ciklusra vonatkozzanak. A cikluscímkéknek egy aposztróffal kell
kezdődniük. Íme egy példa két egymásba ágyazott ciklussal:

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-32-5-loop-labels/src/main.rs}}
```

A külső ciklus címkéje `'counting_up`, és 0-tól 2-ig számol felfelé. A címke
nélküli belső ciklus 10-től 9-ig számol lefelé. Az első, címkét nem megadó
`break` csak a belső ciklusból lép ki. A `break 'counting_up;` utasítás a
külső ciklusból lép ki. Ez a kód a következőt írja ki:

```console
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-32-5-loop-labels/output.txt}}
```

<!-- Old headings. Do not remove or links may break. -->
<a id="conditional-loops-with-while"></a>

#### Feltételes ciklusok egyszerűsítése a while-lal {#streamlining-conditional-loops-with-while}

Egy programnak gyakran ki kell értékelnie egy feltételt egy cikluson belül.
Amíg a feltétel `true`, a ciklus fut. Amikor a feltétel már nem `true`, a
program meghívja a `break`-et, és leállítja a ciklust. Ilyen viselkedést a
`loop`, az `if`, az `else` és a `break` kombinációjával is megvalósíthatsz;
ha szeretnéd, most kipróbálhatod egy programban. Ez a minta azonban annyira
gyakori, hogy a Rustnak beépített nyelvi szerkezete van rá, a `while` ciklus.
A 3-3. kódrészletben a `while`-lal háromszor futtatjuk a ciklust, minden
alkalommal lefelé számolva, majd a ciklus után kiírunk egy üzenetet, és
kilépünk.

<Listing number="3-3" file-name="src/main.rs" caption="Egy `while` ciklus használata kód futtatására, amíg egy feltétel `true` értékre értékelődik ki">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-03/src/main.rs}}
```

</Listing>

Ez a szerkezet sok olyan egymásba ágyazást szüntet meg, amelyre a `loop`, az
`if`, az `else` és a `break` használatakor szükség lenne, és érthetőbb is. Amíg
egy feltétel `true` értékre értékelődik ki, a kód fut; ellenkező esetben
kilép a ciklusból.

#### Gyűjtemény bejárása a `for`-ral {#looping-through-a-collection-with-for}

A `while` szerkezettel egy gyűjtemény, például egy tömb elemein is
végigmehetsz. Például a 3-4. kódrészletben lévő ciklus kiírja az `a` tömb
minden elemét.

<Listing number="3-4" file-name="src/main.rs" caption="Egy gyűjtemény minden elemének bejárása `while` ciklussal">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-04/src/main.rs}}
```

</Listing>

Itt a kód sorra végigszámol a tömb elemein. A `0` indexről indul, majd addig
ismétel, amíg el nem éri a tömb utolsó indexét (vagyis amíg az `index < 5` már
nem `true`). A kód futtatása a tömb minden elemét kiírja:

```console
{{#include ../listings/ch03-common-programming-concepts/listing-03-04/output.txt}}
```

Ahogy vártuk, mind az öt tömbérték megjelenik a terminálban. Bár az `index`
egy ponton eléri az `5` értéket, a ciklus leáll, mielőtt megpróbálna egy
hatodik értéket lekérni a tömbből.

Ez a megközelítés azonban hibalehetőségeket rejt; pánikot okozhatunk a
programban, ha az index értéke vagy a vizsgált feltétel hibás. Ha például az
`a` tömb definícióját négy eleműre módosítanád, de elfelejtenéd a feltételt
`while index < 4`-re frissíteni, a kód pánikolna. Lassú is, mert a fordító
olyan futásidejű kódot ad hozzá, amely a ciklus minden iterációjában
ellenőrzi, hogy az index a tömb határain belül van-e.

Tömörebb alternatívaként használhatsz `for` ciklust, és egy gyűjtemény minden
elemére végrehajthatsz valamilyen kódot. Egy `for` ciklus a 3-5.
kódrészletben látható kódhoz hasonlóan néz ki.

<Listing number="3-5" file-name="src/main.rs" caption="Egy gyűjtemény minden elemének bejárása `for` ciklussal">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-05/src/main.rs}}
```

</Listing>

Amikor futtatjuk ezt a kódot, ugyanazt a kimenetet látjuk, mint a 3-4.
kódrészletnél. Ennél is fontosabb, hogy most növeltük a kód biztonságát, és
kiküszöböltük azoknak a hibáknak a lehetőségét, amelyek abból eredhetnek, hogy
túlmegyünk a tömb végén, vagy nem megyünk elég messzire, és kihagyunk néhány
elemet. A `for` ciklusokból generált gépi kód hatékonyabb is lehet, mert az
indexet nem kell minden iterációban összehasonlítani a tömb hosszával.

A `for` ciklus használatakor nem kellene más kódot módosítanod, ha
megváltoztatnád a tömbben lévő értékek számát, ellentétben a 3-4.
kódrészletben használt módszerrel.

A `for` ciklusok biztonsága és tömörsége miatt ezek a Rust leggyakrabban
használt ciklusszerkezetei. Még olyan helyzetekben is, amikor egy kódot
meghatározott számú alkalommal szeretnél lefuttatni, mint a 3-3.
kódrészletben `while` ciklust használó visszaszámlálós példában, a legtöbb
rustacean `for` ciklust használna. Ehhez a standard könyvtár által biztosított
`Range`-et kellene használni, amely egy adott számtól kezdve egy másik szám
előttig sorban előállítja az összes számot.

Így nézne ki a visszaszámlálás egy `for` ciklussal és egy másik, eddig még nem
tárgyalt metódussal, a `rev`-vel, amely megfordítja a tartományt:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-34-for-range/src/main.rs}}
```

Ez a kód kicsit szebb, nem igaz?

## Összefoglalás {#summary}

Megcsináltad! Ez egy terjedelmes fejezet volt: megismerted a változókat, a
skalár és összetett adattípusokat, a függvényeket, a kommenteket, az `if`
kifejezéseket és a ciklusokat! Az ebben a fejezetben tárgyalt fogalmak
gyakorlásához próbálj meg olyan programokat írni, amelyek a következőket
végzik:

- Hőmérséklet átváltása Fahrenheit és Celsius között.
- Az *n*-edik Fibonacci-szám előállítása.
- A „The Twelve Days of Christmas” című karácsonyi dal szövegének kiírása, a
  dalban lévő ismétlődések kihasználásával.

Ha készen állsz a továbblépésre, egy olyan Rust-fogalomról lesz szó, amely más
programozási nyelvekben általában _nem_ létezik: a tulajdonjogról
(ownership).

[comparing-the-guess-to-the-secret-number]: ch02-00-guessing-game-tutorial.html#comparing-the-guess-to-the-secret-number
[quitting-after-a-correct-guess]: ch02-00-guessing-game-tutorial.html#quitting-after-a-correct-guess
