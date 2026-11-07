## Adattípusok {#data-types}

A Rustban minden érték valamilyen _adattípusú (data type)_, amely megmondja a
Rustnak, hogy milyen fajta adatról van szó, így tudja, hogyan kell vele
dolgoznia. Az adattípusok két alcsoportját fogjuk megnézni: a skalár és az
összetett típusokat.

Ne feledd, hogy a Rust _statikusan típusos (statically typed)_ nyelv, ami azt
jelenti, hogy fordítási időben ismernie kell az összes változó típusát. A
fordító általában az érték és a használat módja alapján ki tudja következtetni,
milyen típust szeretnénk használni. Amikor több típus is lehetséges, például
amikor a 2. fejezet [„A tipp összehasonlítása a titkos
számmal”][comparing-the-guess-to-the-secret-number]<!-- ignore --> című
szakaszában egy `String`-et a `parse` segítségével számtípussá alakítottunk,
típusannotációt kell megadnunk, így:

```rust
let guess: u32 = "42".parse().expect("Not a number!");
```

Ha nem adjuk meg az előző kódban látható `: u32` típusannotációt, a Rust a
következő hibát jeleníti meg, ami azt jelenti, hogy a fordítónak több
információra van szüksége tőlünk ahhoz, hogy tudja, melyik típust szeretnénk
használni:

```console
{{#include ../listings/ch03-common-programming-concepts/output-only-01-no-type-annotations/output.txt}}
```

Más adattípusoknál más típusannotációkat fogsz látni.

### Skalár típusok {#scalar-types}

A _skalár (scalar)_ típus egyetlen értéket képvisel. A Rustnak négy elsődleges
skalár típusa van: az egész számok, a lebegőpontos számok, a logikai értékek
és a karakterek. Ezeket más programozási nyelvekből is ismerheted. Lássuk,
hogyan működnek a Rustban.

#### Egész típusok {#integer-types}

Az _egész szám (integer)_ olyan szám, amelynek nincs törtrésze. A 2.
fejezetben már használtunk egy egész típust, a `u32` típust. Ez a
típusdeklaráció azt jelzi, hogy a hozzá tartozó érték előjel nélküli egész
szám (az előjeles egész típusok `u` helyett `i`-vel kezdődnek), amely 32 bitet
foglal el. A 3-1. táblázat a Rust beépített egész típusait mutatja. Ezen
változatok bármelyikével megadhatjuk egy egész érték típusát.

<span class="caption">3-1. táblázat: Egész típusok a Rustban</span>

| Hossz   | Előjeles | Előjel nélküli |
| ------- | ------- | -------- |
| 8 bites   | `i8`    | `u8`     |
| 16 bites  | `i16`   | `u16`    |
| 32 bites  | `i32`   | `u32`    |
| 64 bites  | `i64`   | `u64`    |
| 128 bites | `i128`  | `u128`   |
| Architektúrafüggő | `isize` | `usize`  |

Minden változat lehet előjeles vagy előjel nélküli, és meghatározott mérete
van. Az _előjeles (signed)_ és az _előjel nélküli (unsigned)_ arra utal, hogy
a szám lehet-e negatív – más szóval, hogy a számnak szüksége van-e előjelre
(előjeles), vagy mindig csak pozitív lesz, és ezért előjel nélkül is
ábrázolható (előjel nélküli). Olyan ez, mint amikor számokat írunk papírra: ha
az előjel számít, a számot plusz vagy mínusz jellel írjuk; ha viszont nyugodtan
feltételezhetjük, hogy a szám pozitív, előjel nélkül írjuk. Az előjeles
számokat [kettes komplemens][twos-complement]<!-- ignore --> ábrázolásban
tároljuk.

Minden előjeles változat −(2<sup>n − 1</sup>) és 2<sup>n − 1</sup> − 1 közötti
számokat tárolhat (a határokat is beleértve), ahol _n_ a változat által
használt bitek száma. Egy `i8` tehát −(2<sup>7</sup>) és 2<sup>7</sup> − 1
közötti számokat tárolhat, ami −128-tól 127-ig terjed. Az előjel nélküli
változatok 0 és 2<sup>n</sup> − 1 közötti számokat tárolhatnak, így egy `u8`
0 és 2<sup>8</sup> − 1 közötti számokat tárolhat, ami 0-tól 255-ig terjed.

Ezenkívül az `isize` és a `usize` típus attól a számítógép-architektúrától
függ, amelyen a programod fut: 64 bites architektúrán 64 bitesek, 32 bites
architektúrán 32 bitesek.

Az egész literálokat a 3-2. táblázatban látható bármelyik formában írhatod.
Az olyan számliterálok, amelyek több számtípusúak is lehetnek, típusutótagot is
kaphatnak, például `57u8`, a típus megjelölésére. A számliterálokban a `_`
vizuális elválasztóként is használható, hogy a szám könnyebben olvasható
legyen, például `1_000`, amelynek ugyanaz az értéke, mintha `1000`-et írtál
volna.

<span class="caption">3-2. táblázat: Egész literálok a Rustban</span>

| Számliterál      | Példa       |
| ---------------- | ------------- |
| Decimális          | `98_222`      |
| Hexadecimális              | `0xff`        |
| Oktális            | `0o77`        |
| Bináris           | `0b1111_0000` |
| Bájt (csak `u8`) | `b'A'`        |

Honnan tudod tehát, melyik egész típust használd? Ha bizonytalan vagy, a Rust
alapértelmezései általában jó kiindulópontot jelentenek: az egész típusok
alapértelmezése az `i32`. Az `isize` vagy a `usize` használatának fő esete
valamilyen gyűjtemény indexelése.

> ##### Egészszám-túlcsordulás {#integer-overflow}
>
> Tegyük fel, hogy van egy `u8` típusú változód, amely 0 és 255 közötti
> értékeket tárolhat. Ha a változót ezen a tartományon kívüli értékre próbálod
> állítani, például 256-ra, _egészszám-túlcsordulás (integer overflow)_
> következik be, ami kétféle viselkedést eredményezhet. Ha debug módban
> fordítasz, a Rust ellenőrzéseket épít be az egészszám-túlcsordulásra,
> amelyek hatására a program futásidőben _pánikol (panic)_, ha ez bekövetkezik.
> A Rust a _pánikolás (panicking)_ kifejezést használja arra, amikor egy
> program hibával kilép; a pánikokról részletesebben a 9. fejezet
> [„Helyrehozhatatlan hibák a `panic!`
> makróval”][unrecoverable-errors-with-panic]<!-- ignore --> című szakaszában
> lesz szó.
>
> Ha release módban, a `--release` kapcsolóval fordítasz, a Rust _nem_ épít be
> pánikot okozó ellenőrzéseket az egészszám-túlcsordulásra. Ehelyett
> túlcsordulás esetén a Rust _kettes komplemens szerinti körbefordulást (two’s
> complement wrapping)_ végez. Röviden: a típus által tárolható legnagyobb
> értéknél nagyobb értékek „körbefordulnak” a típus által tárolható legkisebb
> értékre. Egy `u8` esetén a 256-os értékből 0 lesz, a 257-ből 1, és így
> tovább. A program nem pánikol, de a változó értéke valószínűleg nem az lesz,
> amire számítottál. Az egészszám-túlcsordulás körbeforduló viselkedésére
> hagyatkozni hibának számít.
>
> A túlcsordulás lehetőségének kifejezett kezelésére a standard könyvtár által
> a primitív számtípusokhoz biztosított következő metóduscsaládokat
> használhatod:
>
> - Körbefordulás minden fordítási módban a `wrapping_*` metódusokkal, például
>   a `wrapping_add`-dal.
> - A `None` érték visszaadása túlcsordulás esetén a `checked_*` metódusokkal.
> - Az érték és egy, a túlcsordulás bekövetkeztét jelző logikai érték
>   visszaadása az `overflowing_*` metódusokkal.
> - Telítés az érték minimumánál vagy maximumánál a `saturating_*`
>   metódusokkal.

#### Lebegőpontos típusok {#floating-point-types}

A Rustnak két primitív típusa van a _lebegőpontos számokhoz (floating-point
numbers)_ is, vagyis a tizedesponttal rendelkező számokhoz. A Rust
lebegőpontos típusai az `f32` és az `f64`, amelyek mérete 32, illetve 64 bit.
Az alapértelmezett típus az `f64`, mert a modern CPU-kon nagyjából ugyanolyan
gyors, mint az `f32`, de nagyobb pontosságra képes. Minden lebegőpontos típus
előjeles.

Íme egy példa, amely működés közben mutatja a lebegőpontos számokat:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-06-floating-point/src/main.rs}}
```

A lebegőpontos számok ábrázolása az IEEE-754 szabványt követi.

#### Numerikus műveletek {#numeric-operations}

A Rust minden számtípusra támogatja az elvárható alapvető matematikai
műveleteket: az összeadást, a kivonást, a szorzást, az osztást és a
maradékképzést. Az egész osztás nulla felé csonkít a legközelebbi egész
számra. A következő kód bemutatja, hogyan használhatod az egyes numerikus
műveleteket egy `let` utasításban:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-07-numeric-operations/src/main.rs}}
```

Ezekben az utasításokban minden kifejezés egy matematikai operátort használ, és
egyetlen értékké értékelődik ki, amelyet aztán egy változóhoz kötünk. [A B.
függelék][appendix_b]<!-- ignore --> tartalmazza a Rust összes operátorának
listáját.

#### A logikai típus {#the-boolean-type}

A legtöbb programozási nyelvhez hasonlóan a Rustban is két lehetséges értéke
van a logikai (Boolean) típusnak: `true` és `false`. A logikai értékek mérete
egy bájt. A logikai típust a Rustban a `bool` jelöli. Például:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-08-boolean/src/main.rs}}
```

A logikai értékeket főként feltételekben használjuk, például egy `if`
kifejezésben. Az `if` kifejezések Rustbeli működését a
[„Vezérlési szerkezetek”][control-flow]<!-- ignore --> című szakaszban
tárgyaljuk.

#### A karaktertípus {#the-character-type}

A Rust `char` típusa a nyelv legelemibb betűtípusa. Íme néhány példa `char`
értékek deklarálására:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-09-char/src/main.rs}}
```

Figyeld meg, hogy a `char` literálokat aposztrófok között adjuk meg, szemben a
sztringliterálokkal, amelyek idézőjeleket használnak. A Rust `char` típusa 4
bájt méretű, és egy Unicode skalárértéket képvisel, ami azt jelenti, hogy jóval
többet tud ábrázolni, mint pusztán az ASCII-t. Az ékezetes betűk; a kínai,
japán és koreai karakterek; az emojik; és a nulla szélességű szóközök mind
érvényes `char` értékek a Rustban. A Unicode skalárértékek tartománya `U+0000`
és `U+D7FF`, valamint `U+E000` és `U+10FFFF` között van (a határokat is
beleértve). A „karakter” azonban nem igazán Unicode-fogalom, így az, amit
emberi intuícióval karakternek gondolsz, nem feltétlenül egyezik meg azzal,
ami a Rustban egy `char`. Erről a témáról részletesen a 8. fejezet [„UTF-8
kódolású szöveg tárolása sztringekkel”][strings]<!-- ignore --> című
szakaszában lesz szó.

### Összetett típusok {#compound-types}

Az _összetett típusok (compound types)_ több értéket foglalhatnak egyetlen
típusba. A Rustnak két primitív összetett típusa van: a tuple-ök és a tömbök.

#### A tuple típus {#the-tuple-type}

A _tuple_ egy általános módja annak, hogy több, különféle típusú értéket
egyetlen összetett típusba csoportosítsunk. A tuple-ök hossza rögzített:
deklarálásuk után nem nőhetnek és nem zsugorodhatnak.

Tuple-t úgy hozunk létre, hogy zárójelek között vesszővel elválasztott
értékeket sorolunk fel. A tuple minden pozíciójának van egy típusa, és a
tuple-ben lévő különböző értékek típusának nem kell megegyeznie. Ebben a
példában nem kötelező típusannotációkat is megadtunk:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-10-tuples/src/main.rs}}
```

A `tup` változó a teljes tuple-höz kötődik, mert a tuple egyetlen összetett
elemnek számít. Az egyes értékek tuple-ből való kinyeréséhez
mintaillesztéssel szétbonthatjuk a tuple értéket, így:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-11-destructuring-tuples/src/main.rs}}
```

Ez a program először létrehoz egy tuple-t, és a `tup` változóhoz köti. Ezután
egy mintát használ a `let`-tel, hogy a `tup`-ot három külön változóvá alakítsa:
`x`-szé, `y`-ná és `z`-vé. Ezt _szétbontásnak (destructuring)_ nevezzük, mert
az egyetlen tuple-t három részre bontja. Végül a program kiírja az `y`
értékét, ami `6.4`.

Egy tuple elemét közvetlenül is elérhetjük, ha egy pontot (`.`) írunk, majd
utána az elérni kívánt érték indexét. Például:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-12-tuple-indexing/src/main.rs}}
```

Ez a program létrehozza az `x` tuple-t, majd a megfelelő indexek segítségével
eléri a tuple minden elemét. A legtöbb programozási nyelvhez hasonlóan a tuple
első indexe a 0.

Az érték nélküli tuple-nek külön neve van: _unit_. Ezt az értéket és a hozzá
tartozó típust is `()` alakban írjuk, és üres értéket vagy üres visszatérési
típust jelöl. A kifejezések implicit módon a unit értéket adják vissza, ha nem
adnak vissza más értéket.

#### A tömb típus {#the-array-type}

Több érték gyűjteményének egy másik módja a _tömb (array)_. A tuple-lel
ellentétben a tömb minden elemének azonos típusúnak kell lennie. Egyes más
nyelvek tömbjeivel ellentétben a Rustban a tömbök hossza rögzített.

A tömb értékeit szögletes zárójelek között, vesszővel elválasztott listaként
írjuk:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-13-arrays/src/main.rs}}
```

A tömbök akkor hasznosak, ha azt szeretnéd, hogy az adataid – az eddig látott
többi típushoz hasonlóan – a _veremben (stack)_ legyenek lefoglalva, ne pedig
a _kupacban (heap)_ (a veremről és a kupacról bővebben [a 4.
fejezetben][stack-and-heap]<!-- ignore --> lesz szó), vagy ha biztosítani
szeretnéd, hogy mindig rögzített számú elemed legyen. A tömb azonban nem olyan
rugalmas, mint a vektor típus. A vektor egy hasonló, a standard könyvtár által
biztosított gyűjteménytípus, amelynek mérete _növekedhet_ és csökkenhet, mert
a tartalma a kupacban él. Ha nem vagy biztos benne, hogy tömböt vagy vektort
használj, valószínűleg vektort érdemes. [A 8. fejezet][vectors]<!-- ignore -->
részletesebben foglalkozik a vektorokkal.

A tömbök viszont akkor hasznosabbak, ha tudod, hogy az elemek számának nem kell
változnia. Ha például egy programban a hónapok neveit használnád,
valószínűleg tömböt használnál vektor helyett, mert tudod, hogy mindig 12
elemet fog tartalmazni:

```rust
let months = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"];
```

A tömb típusát szögletes zárójelek között adod meg: az elemek típusa, egy
pontosvessző, majd a tömb elemeinek száma, így:

```rust
let a: [i32; 5] = [1, 2, 3, 4, 5];
```

Itt az `i32` az egyes elemek típusa. A pontosvessző után az `5` szám azt
jelzi, hogy a tömb öt elemet tartalmaz.

Egy tömböt úgy is inicializálhatsz, hogy minden eleme ugyanazt az értéket
tartalmazza: add meg a kezdőértéket, majd egy pontosvesszőt, végül a tömb
hosszát szögletes zárójelek között, ahogy itt látható:

```rust
let a = [3; 5];
```

Az `a` nevű tömb `5` elemet fog tartalmazni, amelyek kezdetben mind a `3`
értéket kapják. Ez ugyanaz, mintha azt írtuk volna, hogy
`let a = [3, 3, 3, 3, 3];`, csak tömörebben.

<!-- Old headings. Do not remove or links may break. -->
<a id="accessing-array-elements"></a>

#### Tömbelemek elérése {#array-element-access}

A tömb egyetlen, ismert és rögzített méretű memóriaterület, amely a veremben
foglalható le. A tömb elemeit indexeléssel érheted el, így:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-14-array-indexing/src/main.rs}}
```

Ebben a példában a `first` nevű változó az `1` értéket kapja, mert ez az érték
áll a tömb `[0]` indexén. A `second` nevű változó a tömb `[1]` indexén lévő `2`
értéket kapja.

#### Érvénytelen tömbelem-elérés {#invalid-array-element-access}

Nézzük meg, mi történik, ha a tömb végén túli elemet próbálsz elérni. Tegyük
fel, hogy a 2. fejezet találgatós játékához hasonlóan ezt a kódot futtatod,
hogy a felhasználótól kérj be egy tömbindexet:

<span class="filename">Fájlnév: src/main.rs</span>

```rust,ignore,panics
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-15-invalid-array-access/src/main.rs}}
```

Ez a kód sikeresen lefordul. Ha a `cargo run` paranccsal futtatod, és a `0`,
`1`, `2`, `3` vagy `4` értéket adod meg, a program kiírja a tömb adott indexén
lévő értéket. Ha viszont a tömb végén túli számot adsz meg, például `10`-et,
ehhez hasonló kimenetet látsz:

<!-- manual-regeneration
cd listings/ch03-common-programming-concepts/no-listing-15-invalid-array-access
cargo run
10
-->

```console
thread 'main' panicked at src/main.rs:19:19:
index out of bounds: the len is 5 but the index is 10
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

A program futásidejű hibát okozott azon a ponton, ahol az indexelési
műveletben érvénytelen értéket használt. A program hibaüzenettel kilépett, és
nem hajtotta végre az utolsó `println!` utasítást. Amikor indexeléssel próbálsz
elérni egy elemet, a Rust ellenőrzi, hogy a megadott index kisebb-e a tömb
hosszánál. Ha az index nagyobb vagy egyenlő a hosszal, a Rust pánikol. Ennek
az ellenőrzésnek futásidőben kell megtörténnie, különösen ebben az esetben,
mert a fordító nem tudhatja, milyen értéket ad meg a felhasználó, amikor
később futtatja a kódot.

Ez a Rust memóriabiztonsági elveinek gyakorlati példája. Sok alacsony szintű
nyelvben nem végeznek ilyen ellenőrzést, és ha hibás indexet adsz meg,
érvénytelen memóriaterülethez lehet hozzáférni. A Rust úgy véd meg az ilyen
hibától, hogy azonnal kilép, ahelyett, hogy engedélyezné a memória-hozzáférést,
és folytatná a futást. A 9. fejezet bővebben tárgyalja a Rust hibakezelését,
és azt, hogyan írhatsz olvasható, biztonságos kódot, amely sem nem pánikol, sem
nem enged érvénytelen memória-hozzáférést.

[comparing-the-guess-to-the-secret-number]: ch02-00-guessing-game-tutorial.html#comparing-the-guess-to-the-secret-number
[twos-complement]: https://en.wikipedia.org/wiki/Two%27s_complement
[control-flow]: ch03-05-control-flow.html#control-flow
[strings]: ch08-02-strings.html#storing-utf-8-encoded-text-with-strings
[stack-and-heap]: ch04-01-what-is-ownership.html#the-stack-and-the-heap
[vectors]: ch08-01-vectors.html
[unrecoverable-errors-with-panic]: ch09-01-unrecoverable-errors-with-panic.html
[appendix_b]: appendix-02-operators.md
