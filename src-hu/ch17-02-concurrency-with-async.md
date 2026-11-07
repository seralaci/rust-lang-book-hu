<!-- Old headings. Do not remove or links may break. -->

<a id="concurrency-with-async"></a>

## Konkurencia az async segítségével {#applying-concurrency-with-async}

Ebben a szakaszban az asyncet néhány olyan konkurenciaproblémára alkalmazzuk,
amelyeket a 16. fejezetben szálakkal oldottunk meg. Mivel a kulcsfontosságú
ötletek nagy részéről már ott beszéltünk, ebben a szakaszban arra
összpontosítunk, miben különböznek a szálak és a future-ök.

Sok esetben az asynckel megvalósított konkurencia API-jai nagyon hasonlítanak a
szálakéihoz. Más esetekben viszont egészen eltérőek. Még ha a szálak és az
async API-jai _hasonlónak is tűnnek_, a viselkedésük gyakran eltér – és szinte
mindig eltérőek a teljesítményjellemzőik.

<!-- Old headings. Do not remove or links may break. -->

<a id="counting"></a>

### Új task létrehozása a `spawn_task` segítségével {#creating-a-new-task-with-spawn_task}

Az első feladat, amellyel a 16. fejezet [„Új szál létrehozása a `spawn`
segítségével”][thread-spawn]<!-- ignore --> című részében foglalkoztunk, a
számlálás volt két külön szálon. Csináljuk meg ugyanezt asynckel! A `trpl`
crate biztosít egy `spawn_task` függvényt, amely nagyon hasonlít a
`thread::spawn` API-ra, valamint egy `sleep` függvényt, amely a `thread::sleep`
API async változata. Ezeket együtt használva megvalósíthatjuk a számlálós
példát, ahogy a 17-6. kódrészlet mutatja.

<Listing number="17-6" caption="Új task létrehozása, amely kiír valamit, miközben a fő task valami mást ír ki" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-06/src/main.rs:all}}
```

</Listing>

Kiindulópontként a `main` függvényünket a `trpl::block_on` segítségével
állítjuk be, hogy a legfelső szintű függvényünk async lehessen.

> Megjegyzés: A fejezetben innentől kezdve minden példa pontosan ugyanezt a
> `trpl::block_on`-os burkoló kódot tartalmazza a `main`-ben, ezért gyakran
> kihagyjuk, ahogy a `main`-t is. Ne felejtsd el beleírni a saját kódodba!

Ezután két ciklust írunk ebbe a blokkba, mindegyikben egy `trpl::sleep`
hívással, amely fél másodpercet (500 milliszekundumot) vár, mielőtt elküldené a
következő üzenetet. Az egyik ciklust egy `trpl::spawn_task` törzsébe tesszük, a
másikat egy legfelső szintű `for` ciklusba. A `sleep` hívások után egy-egy
`await`-et is írunk.

Ez a kód a szálalapú megvalósításhoz hasonlóan viselkedik – beleértve azt is,
hogy a saját terminálodban futtatva az üzenetek más sorrendben jelenhetnek meg:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the second task!
hi number 1 from the first task!
hi number 2 from the first task!
hi number 2 from the second task!
hi number 3 from the first task!
hi number 3 from the second task!
hi number 4 from the first task!
hi number 4 from the second task!
hi number 5 from the first task!
```

Ez a változat azonnal leáll, amint a fő async blokk törzsében lévő `for` ciklus
befejeződik, mert a `spawn_task` által indított task leáll, amikor a `main`
függvény véget ér. Ha azt szeretnéd, hogy a task teljesen végigfusson, egy
join-leíróval (join handle) kell megvárnod, hogy az első task befejeződjön. A
szálaknál a `join` metódussal „blokkoltunk”, amíg a szál be nem fejezte a
futását. A 17-7. kódrészletben ugyanezt az `await`-tel tehetjük meg, mert maga a
task-leíró is egy future. Az `Output` típusa egy `Result`, ezért a bevárása után
ki is csomagoljuk.

<Listing number="17-7" caption="Az `await` használata egy join-leíróval, hogy egy task végigfusson" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-07/src/main.rs:handle}}
```

</Listing>

Ez a frissített változat addig fut, amíg _mindkét_ ciklus be nem fejeződik:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the second task!
hi number 1 from the first task!
hi number 2 from the first task!
hi number 2 from the second task!
hi number 3 from the first task!
hi number 3 from the second task!
hi number 4 from the first task!
hi number 4 from the second task!
hi number 5 from the first task!
hi number 6 from the first task!
hi number 7 from the first task!
hi number 8 from the first task!
hi number 9 from the first task!
```

Eddig úgy tűnik, hogy az async és a szálak hasonló eredményt adnak, csak eltérő
szintaxissal: a join-leírón hívott `join` helyett az `await`-et használjuk, és
bevárjuk a `sleep` hívásokat.

A nagyobb különbség az, hogy ehhez nem kellett újabb operációsrendszer-szálat
indítanunk. Valójában itt még taskot sem kell indítanunk. Mivel az async
blokkok névtelen future-ökké fordulnak le, mindkét ciklust egy-egy async
blokkba tehetjük, és a `trpl::join` függvénnyel a futtatókörnyezetre bízhatjuk,
hogy mindkettőt végigfuttassa.

A 16. fejezet
[„Várakozás az összes szál befejeződésére”][join-handles]<!-- ignore --> című
részében megmutattuk, hogyan használható a `join` metódus az
`std::thread::spawn` hívásakor visszaadott `JoinHandle` típuson. A `trpl::join`
függvény hasonló, csak future-ökhöz. Ha két future-t adsz át neki, egyetlen új
future-t állít elő, amelynek kimenete egy tuple, amely az átadott future-ök
kimenetét tartalmazza, miután _mindkettő_ befejeződött. Ezért a 17-8.
kódrészletben a `trpl::join` segítségével várjuk meg, hogy az `fut1` és az
`fut2` is befejeződjön. _Nem_ az `fut1`-et és az `fut2`-t várjuk be, hanem a
`trpl::join` által előállított új future-t. A kimenetet figyelmen kívül
hagyjuk, mert az csak egy két unit értéket tartalmazó tuple.

<Listing number="17-8" caption="A `trpl::join` használata két névtelen future bevárásához" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-08/src/main.rs:join}}
```

</Listing>

Ha ezt futtatjuk, azt látjuk, hogy mindkét future végigfut:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the first task!
hi number 1 from the second task!
hi number 2 from the first task!
hi number 2 from the second task!
hi number 3 from the first task!
hi number 3 from the second task!
hi number 4 from the first task!
hi number 4 from the second task!
hi number 5 from the first task!
hi number 6 from the first task!
hi number 7 from the first task!
hi number 8 from the first task!
hi number 9 from the first task!
```

Most minden alkalommal pontosan ugyanazt a sorrendet látod, ami nagyon eltér
attól, amit a szálaknál és a 17-7. kódrészletben a `trpl::spawn_task`
használatakor láttunk. Ennek az az oka, hogy a `trpl::join` függvény
_igazságos (fair)_, vagyis minden future-t ugyanolyan gyakran ellenőriz,
felváltva közöttük, és soha nem engedi, hogy az egyik előreszaladjon, ha a
másik készen áll. A szálaknál az operációs rendszer dönti el, melyik szálat
ellenőrizze, és mennyi ideig hagyja futni. Az async Rustban a futtatókörnyezet
dönti el, melyik taskot ellenőrizze. (A gyakorlatban a részletek bonyolultak,
mert egy aszinkron futtatókörnyezet a konkurencia kezelésének részeként a
háttérben operációsrendszer-szálakat is használhat, így az igazságosság
garantálása több munkát jelenthet egy futtatókörnyezetnek – de így is
lehetséges!) A futtatókörnyezeteknek nem kell garantálniuk az igazságosságot
egyetlen adott műveletnél sem, és gyakran különböző API-kat kínálnak, hogy
eldönthesd, szeretnél-e igazságosságot vagy sem.

Próbáld ki a future-ök bevárásának néhány alábbi változatát, és nézd meg, mit
csinálnak:

- Távolítsd el az async blokkot az egyik vagy mindkét ciklus körül.
- Várj be minden async blokkot közvetlenül a definiálása után.
- Csak az első ciklust burkold async blokkba, és az így kapott future-t a
  második ciklus törzse után várd be.

Plusz kihívásként próbáld meg kitalálni, mi lesz a kimenet az egyes esetekben,
_mielőtt_ lefuttatnád a kódot!

<!-- Old headings. Do not remove or links may break. -->

<a id="message-passing"></a>
<a id="counting-up-on-two-tasks-using-message-passing"></a>

### Adatküldés két task között üzenetküldéssel {#sending-data-between-two-tasks-using-message-passing}

Az adatok future-ök közötti megosztása is ismerős lesz: ismét üzenetküldést
használunk, de ezúttal a típusok és függvények async változataival. Egy kicsit
más utat választunk, mint a 16. fejezet [„Adatátadás szálak között
üzenetküldéssel”][message-passing-threads]<!-- ignore --> című részében, hogy
bemutassuk a szálalapú és a future-alapú konkurencia néhány fontos
különbségét. A 17-9. kódrészletben egyetlen async blokkal kezdünk – és _nem_
indítunk külön taskot, ahogy korábban külön szálat indítottunk.

<Listing number="17-9" caption="Async csatorna létrehozása, és a két fele hozzárendelése a `tx`-hez és az `rx`-hez" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-09/src/main.rs:channel}}
```

</Listing>

Itt a `trpl::channel`-t használjuk, amely annak a több termelős, egy fogyasztós
csatorna API-nak az async változata, amelyet a 16. fejezetben a szálakkal
használtunk. Az API async változata csak kicsit tér el a szálalapútól: nem
módosítható helyett módosítható `rx` fogadót használ, és a `recv` metódusa egy
future-t állít elő, amelyet be kell várnunk, ahelyett, hogy közvetlenül az
értéket adná. Most már küldhetünk üzeneteket a küldőtől a fogadónak. Figyeld
meg, hogy nem kell külön szálat vagy akár taskot indítanunk; csupán be kell
várnunk az `rx.recv` hívást.

Az `std::mpsc::channel` szinkron `Receiver::recv` metódusa blokkol, amíg
üzenetet nem kap. A `trpl::Receiver::recv` metódus nem, mert aszinkron.
Blokkolás helyett visszaadja a vezérlést a futtatókörnyezetnek, amíg vagy üzenet
nem érkezik, vagy a csatorna küldő oldala be nem zárul. Ezzel szemben a `send`
hívást nem várjuk be, mert az nem blokkol. Nincs is rá szüksége, mert a
csatorna, amelybe küldünk, korlátlan méretű.

> Megjegyzés: Mivel ez az egész async kód egy `trpl::block_on` hívásban lévő
> async blokkban fut, a benne lévő kód elkerülheti a blokkolást. A rajta
> _kívüli_ kód azonban blokkolni fog, amíg a `block_on` függvény vissza nem
> tér. Pontosan ez a `trpl::block_on` függvény lényege: lehetővé teszi, hogy
> _eldöntsd_, hol blokkoljon a program egy adott async kódrészletre várva, és
> így hol legyen az átmenet a szinkron és az async kód között.

Két dolgot vegyél észre ebben a példában. Először is, az üzenet azonnal
megérkezik. Másodszor, bár itt future-t használunk, még nincs konkurencia. A
kódrészletben minden egymás után történik, pontosan úgy, mintha egyáltalán nem
lennének future-ök.

Az első problémát úgy kezeljük, hogy üzenetek sorozatát küldjük, és közöttük
alszunk egy kicsit, ahogy a 17-10. kódrészlet mutatja.

<!-- We cannot test this one because it never stops! -->

<Listing number="17-10" caption="Több üzenet küldése és fogadása az async csatornán, az egyes üzenetek között egy `await`-tel alvás" file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch17-async-await/listing-17-10/src/main.rs:many-messages}}
```

</Listing>

Az üzenetek elküldésén túl fogadnunk is kell őket. Ebben az esetben, mivel
tudjuk, hány üzenet érkezik, ezt kézzel is megtehetnénk, négyszer meghívva az
`rx.recv().await`-et. A valóságban azonban általában _ismeretlen_ számú
üzenetre várunk, így addig kell várakoznunk, amíg meg nem állapítjuk, hogy
nincs több üzenet.

A 16-10. kódrészletben egy `for` ciklussal dolgoztuk fel a szinkron csatornáról
kapott összes elemet. A Rustban azonban még nincs mód arra, hogy egy `for`
ciklust _aszinkron módon előállított_ elemsorozattal használjunk, ezért egy
olyan ciklust kell használnunk, amellyel még nem találkoztunk: a `while let`
feltételes ciklust. Ez annak az `if let` szerkezetnek a ciklusváltozata, amelyet
a 6. fejezet [„Tömör vezérlés az `if let` és a `let...else`
segítségével”][if-let]<!-- ignore --> című részében láttunk. A ciklus addig fut,
amíg az általa megadott minta továbbra is illeszkedik az értékre.

Az `rx.recv` hívás egy future-t állít elő, amelyet bevárunk. A
futtatókörnyezet szünetelteti a future-t, amíg az készen nem áll. Amint
megérkezik egy üzenet, a future `Some(message)` értékre oldódik fel, ahányszor
csak üzenet érkezik. Amikor a csatorna bezárul, függetlenül attól, hogy
érkezett-e _egyáltalán_ üzenet, a future ehelyett `None` értékre oldódik fel,
jelezve, hogy nincs több érték, így abba kell hagynunk a lekérdezést – vagyis a
bevárást.

A `while let` ciklus mindezt összefogja. Ha az `rx.recv().await` hívás
eredménye `Some(message)`, hozzáférünk az üzenethez, és használhatjuk a ciklus
törzsében, ugyanúgy, mint az `if let` esetében. Ha az eredmény `None`, a ciklus
véget ér. Minden alkalommal, amikor a ciklus egy kört befejez, ismét eléri az
await-pontot, így a futtatókörnyezet újra szünetelteti, amíg újabb üzenet nem
érkezik.

A kód most már sikeresen elküldi és fogadja az összes üzenetet. Sajnos azonban
még mindig van néhány probléma. Egyrészt az üzenetek nem félmásodperces
időközönként érkeznek, hanem mind egyszerre, 2 másodperccel (2000
milliszekundummal) a program indítása után. Másrészt ez a program soha nem lép
ki! Ehelyett örökké új üzenetekre vár. A <kbd>ctrl</kbd>-<kbd>C</kbd>
billentyűkombinációval kell leállítanod.

#### Az egy async blokkon belüli kód lineárisan fut {#code-within-one-async-block-executes-linearly}

Kezdjük azzal, hogy megvizsgáljuk, miért érkeznek az üzenetek mind egyszerre a
teljes késleltetés után, ahelyett, hogy egyenként, késleltetésekkel érkeznének.
Egy adott async blokkon belül az `await` kulcsszavak kódbeli sorrendje egyben az
a sorrend is, amelyben a program futásakor végrehajtódnak.

A 17-10. kódrészletben csak egyetlen async blokk van, így benne minden
lineárisan fut. Még mindig nincs konkurencia. Először lefut az összes `tx.send`
hívás, az összes `trpl::sleep` hívással és a hozzájuk tartozó await-pontokkal
váltakozva. A `while let` ciklus csak ezután jut el a `recv` hívások bármelyik
`await`-pontjához.

Ahhoz, hogy a kívánt viselkedést kapjuk, vagyis hogy az alvási késleltetés az
egyes üzenetek között történjen, a `tx` és az `rx` műveleteit saját async
blokkokba kell tennünk, ahogy a 17-11. kódrészlet mutatja. Ezután a
futtatókörnyezet a `trpl::join` segítségével külön-külön végrehajthatja őket,
ugyanúgy, mint a 17-8. kódrészletben. Ismét a `trpl::join` hívás eredményét
várjuk be, nem az egyes future-öket. Ha az egyes future-öket egymás után
várnánk be, egyszerűen visszajutnánk egy szekvenciális folyamathoz – pontosan
ahhoz, amit _nem_ szeretnénk.

<!-- We cannot test this one because it never stops! -->

<Listing number="17-11" caption="A `send` és a `recv` szétválasztása saját `async` blokkokba, és az ezekhez a blokkokhoz tartozó future-ök bevárása" file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch17-async-await/listing-17-11/src/main.rs:futures}}
```

</Listing>

A 17-11. kódrészlet frissített kódjával az üzenetek 500 milliszekundumos
időközönként jelennek meg, nem pedig mind egyszerre, 2 másodperc után.

#### A tulajdonjog átmozgatása egy async blokkba {#moving-ownership-into-an-async-block}

A program azonban még mindig nem lép ki soha, mert a `while let` ciklus így
működik együtt a `trpl::join`-nal:

- A `trpl::join` által visszaadott future csak akkor fejeződik be, amikor a
  neki átadott future-ök közül _mindkettő_ befejeződött.
- A `tx_fut` future akkor fejeződik be, amikor a `vals` utolsó üzenetének
  elküldése után befejezi az alvást.
- Az `rx_fut` future nem fejeződik be, amíg a `while let` ciklus véget nem ér.
- A `while let` ciklus nem ér véget, amíg az `rx.recv` bevárása `None` értéket
  nem ad.
- Az `rx.recv` bevárása csak akkor ad vissza `None` értéket, ha a csatorna
  másik vége bezárult.
- A csatorna csak akkor zárul be, ha meghívjuk az `rx.close`-t, vagy ha a küldő
  oldalt, a `tx`-et eldobjuk.
- Az `rx.close`-t sehol sem hívjuk meg, a `tx` pedig nem dobódik el, amíg a
  `trpl::block_on`-nak átadott legkülső async blokk véget nem ér.
- A blokk nem érhet véget, mert blokkolva van, amíg a `trpl::join` be nem
  fejeződik, és ezzel visszajutottunk a lista elejére.

Jelenleg az az async blokk, amelyben az üzeneteket küldjük, csak
_kölcsönveszi_ a `tx`-et, mert az üzenetküldéshez nincs szükség tulajdonjogra,
de ha a `tx`-et _átmozgathatnánk_ ebbe az async blokkba, akkor az a blokk
végén eldobódna. A 13. fejezet [„Referenciák elkapása vagy a tulajdonjog
átmozgatása”][capture-or-move]<!-- ignore --> című részében megtanultad, hogyan
használd a `move` kulcsszót closure-ökkel, és ahogy a 16. fejezet [„`move`
closure-ök használata szálakkal”][move-threads]<!-- ignore --> című részében
tárgyaltuk, a szálakkal végzett munka során gyakran kell adatokat
closure-ökbe mozgatnunk. Ugyanez az alapvető mechanizmus érvényes az async
blokkokra is, így a `move` kulcsszó ugyanúgy működik az async blokkokkal, mint
a closure-ökkel.

A 17-12. kódrészletben az üzenetküldéshez használt blokkot `async`-ről
`async move`-ra változtatjuk.

<Listing number="17-12" caption="A 17-11. kódrészlet kódjának javított változata, amely a befejezéskor helyesen leáll" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-12/src/main.rs:with-move}}
```

</Listing>

Ha a kód _ezen_ változatát futtatjuk, az az utolsó üzenet elküldése és
fogadása után szabályosan leáll. Ezután nézzük meg, mit kellene
megváltoztatni ahhoz, hogy több future-ből is küldhessünk adatokat.

#### Több future összekapcsolása a `join!` makróval {#joining-a-number-of-futures-with-the-join-macro}

Ez az async csatorna is több termelős csatorna, így ha több future-ből
szeretnénk üzeneteket küldeni, meghívhatjuk a `clone`-t a `tx`-en, ahogy a
17-13. kódrészlet mutatja.

<Listing number="17-13" caption="Több termelő használata async blokkokkal" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-13/src/main.rs:here}}
```

</Listing>

Először klónozzuk a `tx`-et, létrehozva a `tx1`-et az első async blokkon kívül.
A `tx1`-et ugyanúgy átmozgatjuk ebbe a blokkba, ahogy korábban a `tx`-szel
tettük. Később pedig az eredeti `tx`-et egy _új_ async blokkba mozgatjuk, ahol
további üzeneteket küldünk, valamivel lassabb késleltetéssel. Ezt az új async
blokkot történetesen az üzenetek fogadására szolgáló async blokk után tesszük,
de ugyanúgy állhatna előtte is. A lényeg a future-ök bevárásának sorrendje, nem
pedig az, hogy milyen sorrendben jönnek létre.

Mindkét üzenetküldő async blokknak `async move` blokknak kell lennie, hogy a
`tx` és a `tx1` is eldobódjon, amikor ezek a blokkok befejeződnek. Különben
ugyanabba a végtelen ciklusba jutunk vissza, amelyből kiindultunk.

Végül a `trpl::join`-ról a `trpl::join!`-ra váltunk, hogy a további future-t
is kezelni tudjuk: a `join!` makró tetszőleges számú future-t be tud várni,
ha a future-ök száma fordítási időben ismert. Az ismeretlen számú future-ből
álló gyűjtemény bevárásáról a fejezet későbbi részében lesz szó.

Most már mindkét küldő future összes üzenetét látjuk, és mivel a küldő
future-ök a küldés után kissé eltérő késleltetést használnak, az üzenetek is
ezekkel az eltérő időközökkel érkeznek:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
received 'hi'
received 'more'
received 'from'
received 'the'
received 'messages'
received 'future'
received 'for'
received 'you'
```

Megnéztük, hogyan küldhetünk adatokat future-ök között üzenetküldéssel, hogyan
fut szekvenciálisan az async blokkon belüli kód, hogyan mozgathatjuk át a
tulajdonjogot egy async blokkba, és hogyan kapcsolhatunk össze több future-t.
Most beszéljük meg, hogyan és miért jelezzük a futtatókörnyezetnek, hogy
átválthat egy másik taskra.

[thread-spawn]: ch16-01-threads.html#creating-a-new-thread-with-spawn
[join-handles]: ch16-01-threads.html#waiting-for-all-threads-to-finish
[message-passing-threads]: ch16-02-message-passing.html
[if-let]: ch06-03-if-let.html
[capture-or-move]: ch13-01-closures.html#capturing-references-or-moving-ownership
[move-threads]: ch16-01-threads.html#using-move-closures-with-threads
