## Változók és módosíthatóság {#variables-and-mutability}

Ahogy azt az [„Értékek tárolása
változókban”][storing-values-with-variables]<!-- ignore --> szakaszban
említettük, a változók alapértelmezés szerint _nem módosíthatók (immutable)_.
Ez egyike annak a sok apró ösztönzésnek, amellyel a Rust arra terel, hogy úgy
írd a kódodat, hogy kihasználd a Rust által kínált biztonságot és könnyű
konkurenciát. Ennek ellenére lehetőséged van arra, hogy a változóidat
_módosíthatóvá (mutable)_ tedd. Nézzük meg, hogyan és miért ösztönöz a Rust a
nem módosíthatóság előnyben részesítésére, és miért lehet, hogy néha mégis
eltérnél ettől.

Ha egy változó nem módosítható, akkor miután egy értéket egy névhez kötöttünk,
azt az értéket már nem változtathatod meg. Ennek szemléltetésére hozz létre egy
új, _variables_ nevű projektet a _projects_ mappádban a `cargo new variables`
paranccsal.

Ezután az új _variables_ mappában nyisd meg az _src/main.rs_ fájlt, és cseréld
le a kódját a következőre, amely egyelőre még nem fordul le:

<span class="filename">Fájlnév: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-01-variables-are-immutable/src/main.rs}}
```

Mentsd el, és futtasd a programot a `cargo run` paranccsal. Egy hibaüzenetet
kell kapnod, amely a nem módosíthatóság megsértésére vonatkozik, ahogy ebben a
kimenetben látható:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-01-variables-are-immutable/output.txt}}
```

Ez a példa megmutatja, hogyan segít a fordító megtalálni a programjaidban lévő
hibákat. A fordítási hibák bosszantóak lehetnek, de valójában csak annyit
jelentenek, hogy a programod még nem biztonságosan teszi azt, amit szeretnél;
_nem_ azt jelentik, hogy rossz programozó vagy! A tapasztalt rustaceanek is
kapnak fordítási hibákat.

A `` cannot assign twice to immutable variable `x` `` hibaüzenetet azért
kaptad, mert egy második értéket próbáltál adni a nem módosítható `x`
változónak.

Fontos, hogy fordítási idejű hibát kapjunk, amikor egy nem módosíthatónak
jelölt értéket próbálunk megváltoztatni, mert éppen ez a helyzet vezethet
programhibákhoz. Ha a kódunk egyik része abból a feltételezésből indul ki, hogy
egy érték soha nem változik, a kód egy másik része pedig megváltoztatja ezt az
értéket, akkor előfordulhat, hogy a kód első része nem azt fogja csinálni,
amire tervezték. Az ilyen hiba okát utólag nehéz lehet felderíteni, különösen,
ha a második kódrész csak _néha_ változtatja meg az értéket. A Rust fordító
garantálja, hogy ha kijelented, hogy egy érték nem fog változni, akkor az
valóban nem fog változni, így neked nem kell nyomon követned. A kódodat így
könnyebb átlátni és végiggondolni.

A módosíthatóság viszont nagyon hasznos is lehet, és kényelmesebbé teheti a
kódírást. Bár a változók alapértelmezés szerint nem módosíthatók, módosíthatóvá
teheted őket, ha a változó neve elé a `mut` kulcsszót írod, ahogy azt [a 2.
fejezetben][storing-values-with-variables]<!-- ignore --> is tetted. A `mut`
hozzáadása a kód jövőbeli olvasóinak is jelzi a szándékot: azt, hogy a kód más
részei meg fogják változtatni ennek a változónak az értékét.

Például módosítsuk az _src/main.rs_ fájlt a következőre:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-02-adding-mut/src/main.rs}}
```

Ha most futtatjuk a programot, ezt kapjuk:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-02-adding-mut/output.txt}}
```

A `mut` használatával megváltoztathatjuk az `x`-hez kötött értéket `5`-ről
`6`-ra. Végső soron rajtad múlik, hogy használsz-e módosíthatóságot vagy sem,
és attól függ, hogy az adott helyzetben szerinted mi a legérthetőbb.

<!-- Old headings. Do not remove or links may break. -->
<a id="constants"></a>

### Konstansok deklarálása {#declaring-constants}

A nem módosítható változókhoz hasonlóan a _konstansok (constants)_ is olyan
értékek, amelyek egy névhez vannak kötve, és nem változtathatók meg, de van
néhány különbség a konstansok és a változók között.

Először is, a `mut` nem használható konstansokkal. A konstansok nem csupán
alapértelmezés szerint nem módosíthatók – hanem mindig azok. Konstanst a `let`
kulcsszó helyett a `const` kulcsszóval deklarálunk, és az érték típusát
_kötelező_ megadni annotációval. A típusokkal és a típusannotációkkal a
következő, [„Adattípusok”][data-types]<!-- ignore --> című szakaszban
foglalkozunk, úgyhogy a részletek miatt most ne aggódj. Csak annyit jegyezz
meg, hogy a típust mindig meg kell adnod.

Konstansokat bármilyen hatókörben deklarálhatunk, a globális hatókört is
beleértve, ami hasznossá teszi őket olyan értékekhez, amelyekről a kód sok
részének tudnia kell.

Az utolsó különbség az, hogy a konstansok értéke csak konstans kifejezés lehet,
olyan érték nem, amelyet csak futásidőben lehetne kiszámítani.

Íme egy példa konstans deklarálására:

```rust
const THREE_HOURS_IN_SECONDS: u32 = 60 * 60 * 3;
```

A konstans neve `THREE_HOURS_IN_SECONDS`, az értéke pedig a 60 (egy perc
másodperceinek száma), a 60 (egy óra perceinek száma) és a 3 (a programban
számolni kívánt órák száma) szorzata. A Rust elnevezési konvenciója szerint a
konstansok nevét csupa nagybetűvel írjuk, a szavak között aláhúzásjellel. A
fordító a műveletek egy korlátozott körét fordítási időben is ki tudja
értékelni, így ezt az értéket olyan formában írhatjuk le, amely könnyebben
érthető és ellenőrizhető, ahelyett, hogy a konstanst a 10 800 értékre
állítanánk. A konstansok deklarálásakor használható műveletekről [a Rust
Reference konstanskiértékelésről szóló szakaszában][const-eval] találsz több
információt.

A konstansok a program teljes futási ideje alatt érvényesek abban a
hatókörben, amelyben deklarálták őket. Ez a tulajdonság hasznossá teszi a
konstansokat az alkalmazásod tárgyterületének olyan értékeinél, amelyekről a
program több részének is tudnia kell, például hogy egy játékban egy játékos
legfeljebb hány pontot szerezhet, vagy hogy mekkora a fénysebesség.

Ha a programban mindenütt használt, a kódba beégetett értékeket konstansként
nevezed el, azzal a kód jövőbeli karbantartóinak is átadod az érték jelentését.
Az is segít, hogy a kódban csak egyetlen helyen kell módosítanod, ha a
beégetett értéket a jövőben frissíteni kell.

### Árnyékolás {#shadowing}

Ahogy azt a találgatós játékról szóló bemutatóban, [a 2.
fejezetben][comparing-the-guess-to-the-secret-number]<!-- ignore --> láttad,
deklarálhatsz egy új változót ugyanazzal a névvel, mint egy korábbi változóé.
A rustaceanek azt mondják, hogy az első változót a második _árnyékolja
(shadowing)_, ami azt jelenti, hogy amikor a változó nevét használod, a fordító
a második változót fogja látni. Valójában a második változó beárnyékolja az
elsőt, és a változónév minden használatát magára vonja, amíg őt magát is be
nem árnyékolják, vagy véget nem ér a hatókör. Egy változót úgy
árnyékolhatunk, hogy ugyanazt a változónevet használjuk, és megismételjük a
`let` kulcsszót, így:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-03-shadowing/src/main.rs}}
```

Ez a program először az `x`-et az `5` értékhez köti. Ezután a `let x =`
megismétlésével létrehoz egy új `x` változót, amely az eredeti értékhez `1`-et
ad, így `x` értéke `6` lesz. Ezután a kapcsos zárójelekkel létrehozott belső
hatókörben a harmadik `let` utasítás szintén árnyékolja az `x`-et, és egy új
változót hoz létre, amely az előző értéket `2`-vel megszorozva `x`-nek `12`
értéket ad. Amikor ez a hatókör véget ér, a belső árnyékolás is megszűnik, és
`x` értéke ismét `6` lesz. A program futtatásakor a következő kimenetet kapjuk:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-03-shadowing/output.txt}}
```

Az árnyékolás különbözik attól, ha egy változót `mut`-ként jelölünk meg, mert
fordítási idejű hibát kapunk, ha véletlenül a `let` kulcsszó nélkül próbálunk
új értéket adni a változónak. A `let` használatával néhány átalakítást
végezhetünk egy értéken, a változó viszont ezek után az átalakítások után nem
módosítható marad.

A `mut` és az árnyékolás közötti másik különbség az, hogy mivel a `let`
kulcsszó ismételt használatakor valójában egy új változót hozunk létre,
megváltoztathatjuk az érték típusát, miközben ugyanazt a nevet használjuk
újra. Tegyük fel például, hogy a programunk megkéri a felhasználót, hogy
szóköz karakterek beírásával adja meg, hány szóközt szeretne valamilyen szöveg
között, majd ezt a bemenetet számként szeretnénk tárolni:

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-04-shadowing-can-change-types/src/main.rs:here}}
```

Az első `spaces` változó sztring típusú, a második `spaces` változó pedig szám
típusú. Az árnyékolás így megkímél attól, hogy különböző neveket kelljen
kitalálnunk, például `spaces_str` és `spaces_num`; ehelyett újra használhatjuk
az egyszerűbb `spaces` nevet. Ha viszont ehhez a `mut`-ot próbáljuk használni,
ahogy itt látható, fordítási idejű hibát kapunk:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-05-mut-cant-change-types/src/main.rs:here}}
```

A hiba azt mondja, hogy egy változó típusát nem változtathatjuk meg:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-05-mut-cant-change-types/output.txt}}
```

Most, hogy megismertük a változók működését, nézzük meg, milyen további
adattípusaik lehetnek.

[comparing-the-guess-to-the-secret-number]: ch02-00-guessing-game-tutorial.html#comparing-the-guess-to-the-secret-number
[data-types]: ch03-02-data-types.html#data-types
[storing-values-with-variables]: ch02-00-guessing-game-tutorial.html#storing-values-with-variables
[const-eval]: ../reference/const_eval.html
