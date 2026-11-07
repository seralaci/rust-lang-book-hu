
<!-- Old headings. Do not remove or links may break. -->

<a id="yielding"></a>

### A vezérlés átadása a futtatókörnyezetnek {#yielding-control-to-the-runtime}

Emlékezz vissza: [„Az első async programunk”][async-program]<!-- ignore -->
című részben láttuk, hogy minden await-pontnál a Rust lehetőséget ad a
futtatókörnyezetnek arra, hogy szüneteltesse a taskot, és átváltson egy
másikra, ha a bevárt future még nem áll készen. Ennek a fordítottja is igaz: a
Rust _csak_ await-pontoknál szünetelteti az async blokkokat, és csak ott adja
vissza a vezérlést a futtatókörnyezetnek. Az await-pontok között minden
szinkron.

Ez azt jelenti, hogy ha egy async blokkban sok munkát végzel await-pont
nélkül, az a future minden más future-t megakadályoz abban, hogy haladjon.
Előfordulhat, hogy ezt úgy hallod emlegetni, hogy az egyik future
_kiéhezteti (starving)_ a többi future-t. Ez bizonyos esetekben nem nagy baj.
Ha azonban valamilyen költséges előkészítést vagy hosszan futó munkát végzel,
vagy van egy future-öd, amely a végtelenségig folytat egy bizonyos feladatot,
végig kell gondolnod, mikor és hol adod vissza a vezérlést a
futtatókörnyezetnek.

Szimuláljunk egy hosszan futó műveletet, hogy szemléltessük a kiéheztetés
problémáját, majd nézzük meg, hogyan oldható meg. A 17-14. kódrészlet bevezet
egy `slow` függvényt.

<Listing number="17-14" caption="A `thread::sleep` használata lassú műveletek szimulálására" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-14/src/main.rs:slow}}
```

</Listing>

Ez a kód a `trpl::sleep` helyett az `std::thread::sleep`-et használja, így a
`slow` meghívása néhány milliszekundumra blokkolja az aktuális szálat. A
`slow`-t olyan valós műveletek helyettesítésére használhatjuk, amelyek
egyszerre hosszan futók és blokkolók.

A 17-15. kódrészletben a `slow` segítségével egy future-pár esetében utánozzuk
ezt a fajta CPU-korlátos munkát.

<Listing number="17-15" caption="A `slow` függvény meghívása lassú műveletek szimulálására" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-15/src/main.rs:slow-futures}}
```

</Listing>

Mindegyik future csak azután adja vissza a vezérlést a futtatókörnyezetnek,
_miután_ elvégzett egy csomó lassú műveletet. Ha futtatod ezt a kódot, ezt a
kimenetet látod:

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-15/
cargo run
copy just the output
-->

```text
'a' started.
'a' ran for 30ms
'a' ran for 10ms
'a' ran for 20ms
'b' started.
'b' ran for 75ms
'b' ran for 10ms
'b' ran for 15ms
'b' ran for 350ms
'a' finished.
```

Ahogy a 17-5. kódrészletben, ahol a `trpl::select` segítségével két URL-t lekérő
future-öket versenyeztettünk, a `select` itt is befejeződik, amint az `a`
elkészül. A két future `slow` hívásai között azonban nincs váltakozás. Az `a`
future addig végzi az összes munkáját, amíg el nem jut a `trpl::sleep` hívás
bevárásáig, majd a `b` future végzi az összes munkáját, amíg el nem jut a saját
`trpl::sleep` hívásának bevárásáig, végül az `a` future befejeződik. Ahhoz,
hogy mindkét future haladhasson a lassú feladatai között, await-pontokra van
szükségünk, ahol visszaadhatjuk a vezérlést a futtatókörnyezetnek. Ehhez pedig
valamire, amit bevárhatunk!

Ezt a fajta vezérlésátadást már a 17-15. kódrészletben is láthatjuk: ha
eltávolítanánk a `trpl::sleep`-et az `a` future végéről, az úgy fejeződne be,
hogy a `b` future _egyáltalán_ nem futna. Próbáljuk meg kiindulópontként a
`trpl::sleep` függvényt használni arra, hogy a műveletek felváltva haladjanak,
ahogy a 17-16. kódrészlet mutatja.

<Listing number="17-16" caption="A `trpl::sleep` használata, hogy a műveletek felváltva haladjanak" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-16/src/main.rs:here}}
```

</Listing>

A `slow` egyes hívásai közé await-pontokkal ellátott `trpl::sleep` hívásokat
tettünk. Most a két future munkája váltakozik:

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-16
cargo run
copy just the output
-->

```text
'a' started.
'a' ran for 30ms
'b' started.
'b' ran for 75ms
'a' ran for 10ms
'b' ran for 10ms
'a' ran for 20ms
'b' ran for 15ms
'a' finished.
```

Az `a` future még mindig fut egy darabig, mielőtt átadná a vezérlést a `b`-nek,
mert a `slow`-t még azelőtt hívja meg, hogy egyáltalán meghívná a
`trpl::sleep`-et, de ezután a future-ök minden alkalommal helyet cserélnek,
amikor valamelyikük eléri egy await-pontot. Ebben az esetben ezt minden `slow`
hívás után megtettük, de a munkát bármilyen módon feloszthatnánk, ahogy
számunkra a legésszerűbb.

Valójában azonban nem _aludni_ szeretnénk itt: a lehető leggyorsabban
szeretnénk haladni. Csak vissza kell adnunk a vezérlést a futtatókörnyezetnek.
Ezt közvetlenül is megtehetjük a `trpl::yield_now` függvénnyel. A 17-17.
kódrészletben az összes `trpl::sleep` hívást `trpl::yield_now`-ra cseréljük.

<Listing number="17-17" caption="A `yield_now` használata, hogy a műveletek felváltva haladjanak" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-17/src/main.rs:yields}}
```

</Listing>

Ez a kód egyrészt világosabban kifejezi a tényleges szándékot, másrészt
jelentősen gyorsabb is lehet, mint a `sleep` használata, mert az olyan
időzítőknek, mint amilyet a `sleep` használ, gyakran korlátozott a
felbontásuk. Az általunk használt `sleep` változat például mindig legalább egy
milliszekundumig alszik, még akkor is, ha egy nanoszekundumos `Duration`-t
adunk át neki. Ismét: a modern számítógépek _gyorsak_, egy milliszekundum alatt
rengeteg mindenre képesek!

Ez azt jelenti, hogy az async még számításkorlátos feladatoknál is hasznos
lehet, attól függően, mit csinál még a programod, mert hasznos eszközt ad a
program különböző részei közötti kapcsolatok strukturálásához (de az async
állapotgép többletterhelésének árán). Ez a _kooperatív többfeladatos működés
(cooperative multitasking)_ egy formája, ahol minden future maga dönti el,
mikor adja át a vezérlést az await-pontokon keresztül. Ezért minden future
felelőssége az is, hogy ne blokkoljon túl sokáig. Egyes Rust-alapú beágyazott
operációs rendszerekben ez az _egyetlen_ fajta többfeladatos működés!

A valós kódban persze általában nem fogsz minden egyes sorban függvényhívásokat
és await-pontokat váltogatni. Bár a vezérlés ilyen módon történő átadása
viszonylag olcsó, nem ingyenes. Sok esetben egy számításkorlátos feladat
feldarabolása jelentősen lassabbá teheti azt, így néha a _teljes_
teljesítmény szempontjából jobb, ha hagyjuk, hogy egy művelet rövid ideig
blokkoljon. Mindig mérd meg, hol vannak a kódod tényleges szűk keresztmetszetei!
Az alapul szolgáló mechanizmust azonban fontos szem előtt tartani, ha azt
_látod_, hogy sok munka sorosan történik, amelyről azt vártad, hogy
konkurensen fog történni!

### Saját async absztrakciók készítése {#building-our-own-async-abstractions}

A future-öket össze is kombinálhatjuk, hogy új mintákat hozzunk létre.
Készíthetünk például egy `timeout` függvényt a már meglévő async
építőelemeinkből. Amikor elkészülünk, az eredmény egy újabb építőelem lesz,
amellyel még több async absztrakciót hozhatunk létre.

A 17-18. kódrészlet azt mutatja, hogyan várnánk, hogy ez a `timeout` egy lassú
future-rel működjön.

<Listing number="17-18" caption="Az elképzelt `timeout` használata egy lassú művelet időkorláttal való futtatására" file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-18/src/main.rs:here}}
```

</Listing>

Valósítsuk meg! Kezdetnek gondoljuk végig a `timeout` API-ját:

- Magának is async függvénynek kell lennie, hogy bevárhassuk.
- Az első paramétere egy futtatandó future kell legyen. Generikussá tehetjük,
  hogy bármilyen future-rel működjön.
- A második paramétere a várakozás maximális ideje lesz. Ha `Duration`-t
  használunk, azt könnyű lesz továbbadni a `trpl::sleep`-nek.
- Egy `Result`-ot kell visszaadnia. Ha a future sikeresen befejeződik, a
  `Result` `Ok` lesz a future által előállított értékkel. Ha előbb lejár az
  időkorlát (timeout), a `Result` `Err` lesz azzal az időtartammal, ameddig az
  időkorlát várt.

A 17-19. kódrészlet ezt a deklarációt mutatja.

<!-- This is not tested because it intentionally does not compile. -->

<Listing number="17-19" caption="A `timeout` szignatúrájának definiálása" file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-19/src/main.rs:declaration}}
```

</Listing>

Ez kielégíti a típusokkal kapcsolatos céljainkat. Most gondoljuk végig, milyen
_viselkedésre_ van szükségünk: az átadott future-t szeretnénk versenyeztetni az
időtartammal. A `trpl::sleep` segítségével az időtartamból időzítő future-t
készíthetünk, a `trpl::select` segítségével pedig ezt az időzítőt a hívó által
átadott future-rel együtt futtathatjuk.

A 17-20. kódrészletben a `timeout`-ot úgy valósítjuk meg, hogy a
`trpl::select` bevárásának eredményére illesztünk.

<Listing number="17-20" caption="A `timeout` definiálása a `select` és a `sleep` segítségével" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-20/src/main.rs:implementation}}
```

</Listing>

A `trpl::select` megvalósítása nem igazságos: az argumentumokat mindig abban a
sorrendben kérdezi le, amelyben átadták őket (más `select` megvalósítások
véletlenszerűen választják ki, melyik argumentumot kérdezzék le először).
Ezért a `future_to_try`-t adjuk át először a `select`-nek, hogy akkor is
legyen esélye befejeződni, ha a `max_time` nagyon rövid időtartam. Ha a
`future_to_try` végez előbb, a `select` `Left`-et ad vissza a `future_to_try`
kimenetével. Ha a `timer` végez előbb, a `select` `Right`-ot ad vissza az
időzítő `()` kimenetével.

Ha a `future_to_try` sikeres, és `Left(output)`-ot kapunk, `Ok(output)`-ot adunk
vissza. Ha ehelyett az alvási időzítő jár le, és `Right(())`-ot kapunk, a `()`-t
a `_` segítségével figyelmen kívül hagyjuk, és helyette `Err(max_time)`-ot adunk
vissza.

Ezzel van egy működő `timeout` függvényünk, amely két másik async segédből
épül fel. Ha futtatjuk a kódunkat, az időkorlát lejárta után kiírja a hibás
eset üzenetét:

```text
Failed after 2 seconds
```

Mivel a future-ök más future-ökkel kombinálhatók, kisebb async építőelemekből
igazán hatékony eszközöket építhetsz. Ugyanezzel a megközelítéssel például
összekombinálhatod az időkorlátokat az újrapróbálkozásokkal, és ezeket
hálózati hívásokhoz hasonló műveletekkel (például a 17-5. kódrészletben
lévőkkel) használhatod.

A gyakorlatban általában közvetlenül az `async`-kel és az `await`-tel
dolgozol, másodsorban pedig olyan függvényekkel, mint a `select`, és olyan
makrókkal, mint a `join!`, hogy szabályozd, hogyan hajtódnak végre a
legkülső future-ök.

Most már számos módját láttuk annak, hogyan dolgozhatunk egyszerre több
future-rel. A következőkben azt nézzük meg, hogyan dolgozhatunk több future-rel
időben egymás után, sorozatként, a _streamek (streams)_ segítségével.

[async-program]: ch17-01-futures-and-syntax.html#our-first-async-program
