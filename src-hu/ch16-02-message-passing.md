<!-- Old headings. Do not remove or links may break. -->

<a id="using-message-passing-to-transfer-data-between-threads"></a>

## Adatátadás szálak között üzenetküldéssel {#transfer-data-between-threads-with-message-passing}

A biztonságos konkurencia biztosításának egyre népszerűbb megközelítése az
_üzenetküldés (message passing)_, amelyben a szálak vagy aktorok úgy
kommunikálnak, hogy adatokat tartalmazó üzeneteket küldenek egymásnak. Az
ötletet [a Go nyelv dokumentációjának](https://golang.org/doc/effective_go.html#concurrency)
egy jelmondata foglalja össze: „Ne a memória megosztásával kommunikálj;
inkább a kommunikációval oszd meg a memóriát.”

Az üzenetküldéses konkurenciához a Rust standard könyvtára a csatornák
megvalósítását biztosítja. A _csatorna (channel)_ egy általános programozási
fogalom, amelynek segítségével adatot küldhetünk az egyik szálból a másikba.

A programozásbeli csatornát úgy képzelheted el, mint egy irányított
vízcsatornát, például egy patakot vagy folyót. Ha valamit, mondjuk egy
gumikacsát beleteszel a folyóba, az lefelé úszik a vízfolyás végéig.

A csatornának két fele van: egy küldő (transmitter) és egy fogadó (receiver).
A küldő fele a folyó felső szakasza, ahol a gumikacsát a vízbe teszed, a
fogadó fele pedig az a hely, ahol a gumikacsa a folyó alsó szakaszán
kiköt. A kódod egyik része a küldő metódusait hívja meg a küldeni kívánt
adattal, egy másik része pedig a fogadó oldalon figyeli a beérkező
üzeneteket. Egy csatornát _lezártnak (closed)_ nevezünk, ha a küldő vagy a
fogadó fele eldobásra került.

Itt lépésről lépésre egy olyan programot készítünk, amelyben az egyik szál
értékeket állít elő, és elküldi őket egy csatornán, egy másik szál pedig
fogadja és kiírja az értékeket. A funkció szemléltetésére egyszerű értékeket
küldünk a szálak között egy csatornán keresztül. Ha már ismered a technikát,
bármilyen szálakhoz használhatsz csatornákat, amelyeknek kommunikálniuk kell
egymással, például egy csevegőrendszerben, vagy egy olyan rendszerben, ahol
sok szál végzi egy számítás egyes részeit, és a részeredményeket egyetlen,
az eredményeket összesítő szálnak küldi el.

Először a 16-6. kódrészletben létrehozunk egy csatornát, de nem csinálunk vele
semmit. Vegyük észre, hogy ez még nem fordul le, mert a Rust nem tudja
megállapítani, milyen típusú értékeket szeretnénk a csatornán küldeni.

<Listing number="16-6" file-name="src/main.rs" caption="Csatorna létrehozása, és a két fele hozzárendelése a `tx` és az `rx` változóhoz">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-06/src/main.rs}}
```

</Listing>

Új csatornát az `mpsc::channel` függvénnyel hozunk létre; az `mpsc` a
_multiple producer, single consumer_, azaz „több termelő, egy fogyasztó”
rövidítése. Röviden: a Rust standard könyvtára úgy valósítja meg a
csatornákat, hogy egy csatornának több _küldő_ vége lehet, amelyek értékeket
állítanak elő, de csak egy _fogadó_ vége, amely felhasználja ezeket az
értékeket. Képzeld el, hogy több patak folyik össze egy nagy folyóvá: bármit
is küldünk le bármelyik patakon, a végén egyetlen folyóban köt ki. Egyelőre
egyetlen termelővel kezdünk, de amikor a példa már működik, több termelőt is
hozzáadunk.

Az `mpsc::channel` függvény egy tuple-t ad vissza, amelynek első eleme a
küldő vég – a küldő –, második eleme pedig a fogadó vég – a fogadó. A `tx` és
az `rx` rövidítést sok területen hagyományosan a _transmitter_ (küldő) és a
_receiver_ (fogadó) jelölésére használják, ezért a változóinkat is így
nevezzük el, hogy jelezzük, melyik vég melyik. Egy olyan `let` utasítást
használunk, amelynek mintája szétbontja a tuple-t; a minták `let`
utasításokban való használatát és a szétbontást a 19. fejezetben tárgyaljuk.
Egyelőre elég annyit tudni, hogy a `let` utasítás ilyen használata kényelmes
módja az `mpsc::channel` által visszaadott tuple részeinek kinyerésére.

Mozgassuk át a küldő véget egy elindított szálba, és küldjünk vele egy
sztringet, hogy az elindított szál kommunikáljon a fő szállal, ahogy a 16-7.
kódrészlet mutatja. Ez olyan, mintha a folyó felső szakaszán a vízbe tennénk
egy gumikacsát, vagy egy csevegőüzenetet küldenénk az egyik szálból a
másikba.

<Listing number="16-7" file-name="src/main.rs" caption='A `tx` átmozgatása egy elindított szálba, és a `"hi"` elküldése'>

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-07/src/main.rs}}
```

</Listing>

Ismét a `thread::spawn` segítségével hozunk létre egy új szálat, majd a
`move` kulcsszóval a `tx`-et a closure-be mozgatjuk, így a `tx` tulajdonosa
az elindított szál lesz. Az elindított szálnak birtokolnia kell a küldőt
ahhoz, hogy üzeneteket küldhessen a csatornán.

A küldőnek van egy `send` metódusa, amely átveszi az elküldeni kívánt értéket.
A `send` metódus `Result<T, E>` típust ad vissza, így ha a fogadót már
eldobtuk, és nincs hová elküldeni az értéket, a küldési művelet hibát ad
vissza. Ebben a példában az `unwrap` metódust hívjuk meg, hogy hiba esetén a
program pánikoljon. Egy valódi alkalmazásban azonban rendesen kezelnénk a
hibát: a megfelelő hibakezelési stratégiák áttekintéséhez lapozz vissza a
9. fejezethez.

A 16-8. kódrészletben a fő szálban kivesszük az értéket a fogadóból. Ez olyan,
mintha a folyó végén kihalásznánk a gumikacsát a vízből, vagy megkapnánk egy
csevegőüzenetet.

<Listing number="16-8" file-name="src/main.rs" caption='A `"hi"` érték fogadása a fő szálban és kiírása'>

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-08/src/main.rs}}
```

</Listing>

A fogadónak két hasznos metódusa van: a `recv` és a `try_recv`. Mi a `recv`
metódust használjuk (a _receive_, azaz „fogad” rövidítése), amely blokkolja a
fő szál végrehajtását, és addig vár, amíg egy érték érkezik a csatornán. Amint
megérkezik egy érték, a `recv` egy `Result<T, E>`-be csomagolva visszaadja.
Amikor a küldő lezárul, a `recv` hibát ad vissza, jelezve, hogy több érték
már nem fog érkezni.

A `try_recv` metódus nem blokkol, hanem azonnal visszaad egy `Result<T, E>`
értéket: egy üzenetet tartalmazó `Ok` értéket, ha van elérhető üzenet, és egy
`Err` értéket, ha éppen nincs üzenet. A `try_recv` akkor hasznos, ha ennek a
szálnak az üzenetekre várva más dolga is van: írhatnánk egy ciklust, amely
időnként meghívja a `try_recv` metódust, feldolgozza az üzenetet, ha van
ilyen, egyébként pedig egy kis ideig más munkát végez, mielőtt újra
ellenőrizné.

Ebben a példában az egyszerűség kedvéért a `recv` metódust használtuk; a fő
szálnak az üzenetekre való várakozáson kívül nincs más dolga, így a fő szál
blokkolása helyénvaló.

Amikor lefuttatjuk a 16-8. kódrészlet kódját, látni fogjuk a fő szálból
kiírt értéket:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
Got: hi
```

Tökéletes!

<!-- Old headings. Do not remove or links may break. -->

<a id="channels-and-ownership-transference"></a>

### Tulajdonjog átadása csatornákon keresztül {#transferring-ownership-through-channels}

A tulajdonjogi szabályok létfontosságú szerepet játszanak az üzenetküldésben,
mert segítenek biztonságos, konkurens kódot írni. A konkurens programozásban
előforduló hibák megelőzése az az előny, amelyet az nyújt, ha a Rust-programjaid
egészében a tulajdonjogban gondolkodsz. Végezzünk el egy kísérletet, amely
megmutatja, hogyan dolgoznak együtt a csatornák és a tulajdonjog a problémák
megelőzésében: megpróbálunk egy `val` értéket az elindított szálban
használni _azután_, hogy elküldtük a csatornán. Próbáld meg lefordítani a
16-9. kódrészlet kódját, hogy lásd, miért nem megengedett ez a kód.

<Listing number="16-9" file-name="src/main.rs" caption="Kísérlet a `val` használatára azután, hogy elküldtük a csatornán">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-09/src/main.rs}}
```

</Listing>

Itt megpróbáljuk kiírni a `val` értéket, miután a `tx.send` segítségével
elküldtük a csatornán. Rossz ötlet lenne ezt megengedni: amint az értéket
elküldtük egy másik szálnak, az a szál módosíthatja vagy eldobhatja, mielőtt
mi újra megpróbálnánk használni. A másik szál módosításai következetlen vagy
nem létező adatok miatt hibákat vagy váratlan eredményeket okozhatnak. A Rust
azonban hibát ad, ha megpróbáljuk lefordítani a 16-9. kódrészlet kódját:

```console
{{#include ../listings/ch16-fearless-concurrency/listing-16-09/output.txt}}
```

A konkurenciával kapcsolatos hibánk fordítási idejű hibát okozott. A `send`
függvény átveszi a paramétere tulajdonjogát, és amikor az értéket
átmozgatjuk, a fogadó veszi át a tulajdonjogát. Ez megakadályozza, hogy
véletlenül újra használjuk az értéket az elküldése után; a tulajdonjogi
rendszer ellenőrzi, hogy minden rendben van-e.

<!-- Old headings. Do not remove or links may break. -->

<a id="sending-multiple-values-and-seeing-the-receiver-waiting"></a>

### Több érték küldése {#sending-multiple-values}

A 16-8. kódrészlet kódja lefordult és lefutott, de nem mutatta meg
egyértelműen, hogy két külön szál beszélget egymással a csatornán keresztül.

A 16-10. kódrészletben néhány módosítást végeztünk, amelyek bizonyítják, hogy
a 16-8. kódrészlet kódja konkurensen fut: az elindított szál most több
üzenetet küld, és minden üzenet között egy másodpercre megáll.

<Listing number="16-10" file-name="src/main.rs" caption="Több üzenet küldése, szünetet tartva mindegyik között">

```rust,noplayground
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-10/src/main.rs}}
```

</Listing>

Ezúttal az elindított szálnak van egy sztringekből álló vektora, amelyet el
szeretnénk küldeni a fő szálnak. Végigiterálunk rajtuk, mindegyiket külön
elküldjük, és mindegyik között szünetet tartunk úgy, hogy meghívjuk a
`thread::sleep` függvényt egy egymásodperces `Duration` értékkel.

A fő szálban már nem hívjuk meg kifejezetten a `recv` függvényt: ehelyett az
`rx`-et iterátorként kezeljük. Minden fogadott értéket kiírunk. Amikor a
csatorna lezárul, az iteráció véget ér.

A 16-10. kódrészlet kódjának futtatásakor a következő kimenetet kell látnod,
minden sor között egymásodperces szünettel:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
Got: hi
Got: from
Got: the
Got: thread
```

Mivel a fő szál `for` ciklusában nincs olyan kód, amely szüneteltetne vagy
késleltetne, megállapíthatjuk, hogy a fő szál az elindított száltól érkező
értékekre vár.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-multiple-producers-by-cloning-the-transmitter"></a>

### Több termelő létrehozása {#creating-multiple-producers}

Korábban említettük, hogy az `mpsc` a _multiple producer, single consumer_
(több termelő, egy fogyasztó) rövidítése. Használjuk ki az `mpsc` adta
lehetőséget, és bővítsük ki a 16-10. kódrészlet kódját úgy, hogy több szálat
hozzon létre, amelyek mind ugyanannak a fogadónak küldenek értékeket. Ezt a
küldő klónozásával tehetjük meg, ahogy a 16-11. kódrészlet mutatja.

<Listing number="16-11" file-name="src/main.rs" caption="Több üzenet küldése több termelőtől">

```rust,noplayground
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-11/src/main.rs:here}}
```

</Listing>

Ezúttal, mielőtt létrehoznánk az első elindított szálat, meghívjuk a `clone`
metódust a küldőn. Így kapunk egy új küldőt, amelyet átadhatunk az első
elindított szálnak. Az eredeti küldőt egy második elindított szálnak adjuk
át. Így két szálunk lesz, amelyek mindegyike különböző üzeneteket küld az
egyetlen fogadónak.

Amikor lefuttatod a kódot, a kimenetnek nagyjából így kell kinéznie:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
Got: hi
Got: more
Got: from
Got: messages
Got: for
Got: the
Got: thread
Got: you
```

A rendszeredtől függően az értékeket más sorrendben is láthatod. Ez teszi a
konkurenciát egyszerre érdekessé és nehézzé. Ha kísérletezel a
`thread::sleep` függvénnyel, és a különböző szálakban különböző értékeket
adsz meg neki, minden futtatás még kevésbé lesz determinisztikus, és minden
alkalommal más kimenetet ad.

Most, hogy megnéztük, hogyan működnek a csatornák, nézzük meg a konkurencia
egy másik módszerét.
