## Egyszálú webszerver készítése {#building-a-single-threaded-web-server}

Kezdjük azzal, hogy működésre bírunk egy egyszálú webszervert. Mielőtt
nekilátnánk, nézzük át röviden a webszerverek készítésében szerepet játszó
protokollokat. Ezeknek a protokolloknak a részletei túlmutatnak a könyv
keretein, de egy rövid áttekintés megadja a szükséges információkat.

A webszerverekben használt két fő protokoll a _Hypertext Transfer Protocol_
_(HTTP)_ és a _Transmission Control Protocol_ _(TCP)_. Mindkettő
_kérés–válasz (request-response)_ protokoll, ami azt jelenti, hogy a _kliens
(client)_ kezdeményezi a kéréseket, a _szerver (server)_ pedig figyeli a
kéréseket, és választ ad a kliensnek. A kérések és válaszok tartalmát a
protokollok határozzák meg.

A TCP az alacsonyabb szintű protokoll, amely leírja, hogyan jut el az
információ az egyik szerverről a másikra, de azt nem határozza meg, mi ez az
információ. A HTTP a TCP-re épül, és a kérések és válaszok tartalmát
definiálja. Technikailag a HTTP más protokollokkal is használható, de az
esetek túlnyomó többségében a HTTP TCP-n keresztül küldi az adatait. Mi a TCP-
és HTTP-kérések és -válaszok nyers bájtjaival fogunk dolgozni.

### A TCP-kapcsolat figyelése {#listening-to-the-tcp-connection}

A webszerverünknek figyelnie kell egy TCP-kapcsolatot, így ezzel kezdjük a
munkát. A standard könyvtár ehhez egy `std::net` modult kínál. Hozzunk létre
egy új projektet a szokásos módon:

```console
$ cargo new hello
     Created binary (application) `hello` project
$ cd hello
```

Kezdésként írd be a 21-1. kódrészlet kódját a _src/main.rs_ fájlba. Ez a kód
a `127.0.0.1:7878` helyi címen figyeli a bejövő TCP-adatfolyamokat. Amikor
egy bejövő adatfolyamot kap, kiírja, hogy `Connection established!`.

<Listing number="21-1" file-name="src/main.rs" caption="A bejövő adatfolyamok figyelése és egy üzenet kiírása, amikor adatfolyamot kapunk">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-01/src/main.rs}}
```

</Listing>

A `TcpListener` segítségével a `127.0.0.1:7878` címen figyelhetjük a
TCP-kapcsolatokat. A címben a kettőspont előtti rész egy IP-cím, amely a te
számítógépedet jelöli (ez minden számítógépen ugyanaz, és nem kifejezetten a
szerzők gépét jelenti), a `7878` pedig a port. Két okból választottuk ezt a
portot: ezen a porton általában nem fogadnak HTTP-forgalmat, így nem valószínű,
hogy a szerverünk ütközni fog egy másik, a gépeden esetleg futó webszerverrel;
ráadásul a 7878 telefonon begépelve azt adja, hogy _rust_.

A `bind` függvény ebben a helyzetben a `new` függvényhez hasonlóan működik,
vagyis egy új `TcpListener` példányt ad vissza. A függvény azért kapta a
`bind` nevet, mert a hálózatkezelésben egy porthoz való kapcsolódást, hogy
azon figyeljünk, „porthoz kötésnek (binding to a port)” nevezik.

A `bind` függvény `Result<T, E>` típust ad vissza, ami jelzi, hogy a kötés
meghiúsulhat, például ha a programunk két példányát futtatnánk, és így két
program figyelne ugyanazon a porton. Mivel csak tanulási céllal írunk egy
egyszerű szervert, nem foglalkozunk az ilyen hibák kezelésével; ehelyett az
`unwrap` segítségével leállítjuk a programot, ha hiba történik.

A `TcpListener` `incoming` metódusa egy iterátort ad vissza, amely
adatfolyamok sorozatát adja nekünk (pontosabban `TcpStream` típusú
adatfolyamokat). Egyetlen _adatfolyam (stream)_ egy nyitott kapcsolatot
jelent a kliens és a szerver között. A _kapcsolat (connection)_ a teljes
kérés–válasz folyamat neve, amelyben a kliens csatlakozik a szerverhez, a
szerver előállít egy választ, majd a szerver lezárja a kapcsolatot. Ennek
megfelelően a `TcpStream`-ből olvasva megnézzük, mit küldött a kliens, majd
a válaszunkat az adatfolyamba írva visszaküldjük az adatokat a kliensnek.
Összességében ez a `for` ciklus sorban feldolgozza az egyes kapcsolatokat, és
adatfolyamok sorozatát állítja elő, amelyeket kezelnünk kell.

Egyelőre az adatfolyam kezelése abból áll, hogy meghívjuk az `unwrap`-ot,
amely leállítja a programot, ha az adatfolyamban bármilyen hiba van; ha nincs
hiba, a program kiír egy üzenetet. A következő kódrészletben további
funkciókat adunk a sikeres esethez. Azért kaphatunk hibát az `incoming`
metódustól, amikor egy kliens csatlakozik a szerverhez, mert valójában nem
kapcsolatokon iterálunk, hanem _kapcsolódási kísérleteken (connection
attempts)_. A kapcsolódás számos okból meghiúsulhat, és ezek közül sok az
operációs rendszertől függ. Sok operációs rendszer például korlátozza, hogy
egyszerre hány nyitott kapcsolatot tud kezelni; az e számon felüli új
kapcsolódási kísérletek hibát okoznak, amíg a nyitott kapcsolatok közül
néhány le nem zárul.

Próbáljuk ki ezt a kódot! Futtasd a `cargo run` parancsot a terminálban, majd
töltsd be a _127.0.0.1:7878_ címet egy webböngészőben. A böngészőnek egy
olyan hibaüzenetet kell mutatnia, mint például „Connection reset”, mert a
szerver jelenleg nem küld vissza adatot. Ha viszont a terminálodra nézel,
több üzenetet is látnod kell, amelyek akkor íródtak ki, amikor a böngésző
csatlakozott a szerverhez!

```text
     Running `target/debug/hello`
Connection established!
Connection established!
Connection established!
```

Előfordulhat, hogy egyetlen böngészőkéréshez több üzenet is kiíródik; ennek
az lehet az oka, hogy a böngésző nemcsak magát az oldalt kéri le, hanem más
erőforrásokat is, például a böngészőfülön megjelenő _favicon.ico_ ikont.

Az is lehet, hogy a böngésző többször is megpróbál csatlakozni a szerverhez,
mert a szerver nem válaszol semmilyen adattal. Amikor a `stream` a ciklus
végén kikerül a hatókörből és eldobódik, a kapcsolat a `drop` megvalósítás
részeként lezárul. A böngészők a lezárt kapcsolatokat néha újrapróbálkozással
kezelik, mert a probléma átmeneti is lehet.

A böngészők néha úgy is nyitnak több kapcsolatot a szerver felé, hogy nem
küldenek rajtuk kérést, hogy ha később *mégis* küldenek, azok a kérések
gyorsabban lezajlódhassanak. Ilyenkor a szerverünk minden kapcsolatot lát,
függetlenül attól, érkezik-e kérés az adott kapcsolaton. Például a Chrome-alapú
böngészők számos verziója így tesz; ezt az optimalizálást kikapcsolhatod, ha
privát böngészési módot vagy egy másik böngészőt használsz.

A lényeg az, hogy sikeresen hozzájutottunk egy TCP-kapcsolat leírójához!

Ne felejtsd el leállítani a programot a <kbd>ctrl</kbd>-<kbd>C</kbd>
billentyűkombinációval, ha végeztél a kód egy adott változatának futtatásával.
Ezután minden kódmódosítás után indítsd újra a programot a `cargo run`
paranccsal, hogy biztosan a legújabb kódot futtasd.

### A kérés beolvasása {#reading-the-request}

Valósítsuk meg a böngészőtől érkező kérés beolvasását! Hogy szétválasszuk a
két felelősségi kört – először a kapcsolat megszerzését, majd a kapcsolattal
végzett műveletet –, egy új függvényt írunk a kapcsolatok feldolgozására. Ebben
az új `handle_connection` függvényben adatokat olvasunk a TCP-adatfolyamból,
és kiírjuk őket, hogy lássuk, milyen adatokat küld a böngésző. Módosítsd a
kódot a 21-2. kódrészletnek megfelelően.

<Listing number="21-2" file-name="src/main.rs" caption="Olvasás a `TcpStream`-ből és az adatok kiírása">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-02/src/main.rs}}
```

</Listing>

Hatókörbe hozzuk a `std::io::BufReader`-t és a `std::io::prelude`-ot, hogy
hozzáférjünk azokhoz a traitekhez és típusokhoz, amelyekkel olvashatunk az
adatfolyamból és írhatunk bele. A `main` függvény `for` ciklusában ahelyett,
hogy kiírnánk egy üzenetet arról, hogy létrejött egy kapcsolat, most meghívjuk
az új `handle_connection` függvényt, és átadjuk neki a `stream`-et.

A `handle_connection` függvényben létrehozunk egy új `BufReader` példányt,
amely a `stream`-re mutató referenciát burkolja. A `BufReader` pufferelést ad
hozzá azzal, hogy helyettünk kezeli a `std::io::Read` trait metódusainak
hívásait.

Létrehozunk egy `http_request` nevű változót, hogy összegyűjtsük a böngésző
által a szerverünknek küldött kérés sorait. A `Vec<_>` típusannotációval
jelezzük, hogy ezeket a sorokat egy vektorba szeretnénk összegyűjteni.

A `BufReader` megvalósítja a `std::io::BufRead` traitet, amely a `lines`
metódust biztosítja. A `lines` metódus egy `Result<String, std::io::Error>`
elemeket adó iterátort ad vissza úgy, hogy az adatfolyamot minden újsor-bájtnál
feldarabolja. Hogy megkapjuk az egyes `String`-eket, a `map` és az `unwrap`
segítségével kibontjuk az egyes `Result` értékeket. A `Result` hiba lehet,
ha az adat nem érvényes UTF-8, vagy ha probléma adódott az adatfolyamból
való olvasáskor. Egy éles program persze ezeket a hibákat is elegánsabban
kezelné, de az egyszerűség kedvéért hiba esetén leállítjuk a programot.

A böngésző két egymást követő újsor-karakterrel jelzi egy HTTP-kérés végét,
ezért ahhoz, hogy egy kérést kiolvassunk az adatfolyamból, addig vesszük a
sorokat, amíg üres sztringet tartalmazó sort nem kapunk. Miután a sorokat
összegyűjtöttük a vektorba, szép (pretty) debug formázással kiírjuk őket, hogy
megnézhessük, milyen utasításokat küld a webböngésző a szerverünknek.

Próbáljuk ki ezt a kódot! Indítsd el a programot, és küldj újra kérést egy
webböngészőből. A böngészőben továbbra is hibaoldalt kapunk, de a program
kimenete a terminálban most valami ilyesmi lesz:

<!-- manual-regeneration
cd listings/ch21-web-server/listing-21-02
cargo run
make a request to 127.0.0.1:7878
Can't automate because the output depends on making requests
-->

```console
$ cargo run
   Compiling hello v0.1.0 (file:///projects/hello)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.42s
     Running `target/debug/hello`
Request: [
    "GET / HTTP/1.1",
    "Host: 127.0.0.1:7878",
    "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:99.0) Gecko/20100101 Firefox/99.0",
    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language: en-US,en;q=0.5",
    "Accept-Encoding: gzip, deflate, br",
    "DNT: 1",
    "Connection: keep-alive",
    "Upgrade-Insecure-Requests: 1",
    "Sec-Fetch-Dest: document",
    "Sec-Fetch-Mode: navigate",
    "Sec-Fetch-Site: none",
    "Sec-Fetch-User: ?1",
    "Cache-Control: max-age=0",
]
```

A böngésződtől függően kissé eltérő kimenetet kaphatsz. Most, hogy kiírjuk a
kérés adatait, a kérés első sorában a `GET` utáni útvonalból azt is
láthatjuk, miért kapunk egyetlen böngészőkérésből több kapcsolatot. Ha az
ismételt kapcsolatok mind a _/_ útvonalat kérik, akkor tudjuk, hogy a böngésző
azért próbálja újra és újra lekérni a _/_ útvonalat, mert nem kap választ a
programunktól.

Bontsuk elemeire ezeket a kérésadatokat, hogy megértsük, mit kér a böngésző a
programunktól.

<!-- Old headings. Do not remove or links may break. -->

<a id="a-closer-look-at-an-http-request"></a>
<a id="looking-closer-at-an-http-request"></a>

### Egy HTTP-kérés közelebbről {#looking-more-closely-at-an-http-request}

A HTTP szövegalapú protokoll, és egy kérés a következő formátumú:

```text
Method Request-URI HTTP-Version CRLF
headers CRLF
message-body
```

Az első sor a _kérés sora (request line)_, amely azt az információt
tartalmazza, hogy mit kér a kliens. A kérés sorának első része a használt
metódust jelzi, például `GET` vagy `POST`, amely azt írja le, hogyan küldi
a kliens ezt a kérést. A kliensünk `GET` kérést használt, ami azt jelenti,
hogy információt kér.

A kérés sorának következő része a _/_, amely a kliens által kért _egységes
erőforrás-azonosítót (uniform resource identifier, URI)_ jelzi. Az URI
majdnem, de nem teljesen ugyanaz, mint az _egységes erőforrás-helymeghatározó
(uniform resource locator, URL)_. Az URI-k és URL-ek közötti különbség e
fejezet szempontjából nem fontos, de a HTTP-specifikáció az _URI_ kifejezést
használja, így itt gondolatban nyugodtan behelyettesíthetjük az _URI_ helyére
az _URL_-t.

Az utolsó rész a kliens által használt HTTP-verzió, majd a kérés sora egy
CRLF szekvenciával zárul. (A _CRLF_ a _kocsivissza (carriage return)_ és a
_soremelés (line feed)_ rövidítése – ezek az írógépek korából származó
kifejezések!) A CRLF szekvencia `\r\n` alakban is írható, ahol a `\r` a
kocsivissza, a `\n` pedig a soremelés. A _CRLF szekvencia_ választja el a
kérés sorát a kérés többi adatától. Figyeld meg, hogy amikor a CRLF kiíródik,
`\r\n` helyett egy új sor kezdődését látjuk.

Ha megnézzük a programunk eddigi futtatásaiból kapott kéréssor-adatokat,
láthatjuk, hogy a metódus a `GET`, a kért URI a _/_, a verzió pedig a
`HTTP/1.1`.

A kérés sora után a `Host:`-tól kezdődő további sorok a fejlécek (headers). A
`GET` kéréseknek nincs törzsük (body).

Próbálj meg egy másik böngészőből kérést küldeni, vagy egy másik címet kérni,
például a _127.0.0.1:7878/test_ címet, és nézd meg, hogyan változnak a
kérés adatai.

Most, hogy tudjuk, mit kér a böngésző, küldjünk vissza neki adatokat!

### Válasz írása {#writing-a-response}

Megvalósítjuk, hogy a kliens kérésére válaszként adatokat küldjünk. A
válaszok formátuma a következő:

```text
HTTP-Version Status-Code Reason-Phrase CRLF
headers CRLF
message-body
```

Az első sor az _állapotsor (status line)_, amely tartalmazza a válaszban
használt HTTP-verziót, a kérés eredményét összegző numerikus állapotkódot,
valamint egy indoklást (reason phrase), amely szöveges leírást ad az
állapotkódról. A CRLF szekvencia után következnek az esetleges fejlécek, egy
újabb CRLF szekvencia, majd a válasz törzse.

Íme egy példaválasz, amely az 1.1-es HTTP-verziót használja, az állapotkódja
200, az indoklása OK, és nincsenek fejlécei és törzse sem:

```text
HTTP/1.1 200 OK\r\n\r\n
```

A 200-as állapotkód a szabványos sikeres válasz. Ez a szöveg egy apró,
sikeres HTTP-válasz. Írjuk ki ezt az adatfolyamba válaszként egy sikeres
kérésre! A `handle_connection` függvényből távolítsd el a kérés adatait kiíró
`println!`-t, és cseréld le a 21-3. kódrészlet kódjára.

<Listing number="21-3" file-name="src/main.rs" caption="Egy apró, sikeres HTTP-válasz írása az adatfolyamba">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-03/src/main.rs:here}}
```

</Listing>

Az első új sor a `response` változót definiálja, amely a sikerüzenet adatait
tartalmazza. Ezután meghívjuk az `as_bytes` metódust a `response`-on, hogy a
sztringadatokat bájtokká alakítsuk. A `stream` `write_all` metódusa egy
`&[u8]` értéket vár, és ezeket a bájtokat közvetlenül a kapcsolatra küldi.
Mivel a `write_all` művelet meghiúsulhat, a korábbiakhoz hasonlóan az
`unwrap`-ot használjuk minden hibás eredményre. Egy valódi alkalmazásban
persze itt is hibakezelést írnál.

Ezekkel a módosításokkal futtassuk a kódunkat, és küldjünk egy kérést. Már
nem írunk ki semmilyen adatot a terminálba, így a Cargo kimenetén kívül nem
fogunk más kimenetet látni. Amikor betöltöd a _127.0.0.1:7878_ címet egy
webböngészőben, hiba helyett egy üres oldalt kell kapnod. Épp most kódoltad le
kézzel egy HTTP-kérés fogadását és egy válasz elküldését!

### Valódi HTML visszaadása {#returning-real-html}

Valósítsuk meg, hogy ne csak egy üres oldalt adjunk vissza. Hozd létre az új
_hello.html_ fájlt a projektmappád gyökerében, nem a _src_ mappában. Bármilyen
HTML-t beírhatsz; a 21-4. kódrészlet egy lehetőséget mutat.

<Listing number="21-4" file-name="hello.html" caption="Egy válaszban visszaadandó minta HTML-fájl">

```html
{{#include ../listings/ch21-web-server/listing-21-05/hello.html}}
```

</Listing>

Ez egy minimális HTML5-dokumentum egy címsorral és egy kis szöveggel. Hogy a
szerver egy kérés beérkezésekor ezt adja vissza, a 21-5. kódrészletben
látható módon módosítjuk a `handle_connection` függvényt: beolvassuk a
HTML-fájlt, törzsként hozzáadjuk a válaszhoz, és elküldjük.

<Listing number="21-5" file-name="src/main.rs" caption="A *hello.html* tartalmának elküldése a válasz törzseként">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-05/src/main.rs:here}}
```

</Listing>

A `use` utasításhoz hozzáadtuk az `fs`-t, hogy hatókörbe hozzuk a standard
könyvtár fájlrendszer-modulját. Egy fájl tartalmát sztringbe olvasó kód
ismerős lehet: a 12-4. kódrészletben használtuk, amikor az I/O projektünkben
egy fájl tartalmát olvastuk be.

Ezután a `format!` segítségével a fájl tartalmát a sikeres válasz törzseként
adjuk hozzá. Hogy érvényes HTTP-választ küldjünk, hozzáadjuk a
`Content-Length` fejlécet, amelynek értéke a válaszunk törzsének mérete –
ebben az esetben a `hello.html` mérete.

Futtasd ezt a kódot a `cargo run` paranccsal, és töltsd be a _127.0.0.1:7878_
címet a böngésződben; a HTML-ednek megjelenítve kell látszania!

Jelenleg figyelmen kívül hagyjuk a `http_request` kérésadatait, és feltétel
nélkül visszaküldjük a HTML-fájl tartalmát. Ez azt jelenti, hogy ha a
böngésződben a _127.0.0.1:7878/something-else_ címet kéred le, akkor is
ugyanezt a HTML-választ kapod vissza. Szerverünk jelenleg nagyon korlátozott,
és nem azt csinálja, amit a legtöbb webszerver. Azt szeretnénk, hogy a
válaszaink a kéréstől függjenek, és a HTML-fájlt csak a _/_ útvonalra
érkező, helyesen formázott kérésre küldjük vissza.

### A kérés ellenőrzése és válogatott válaszadás {#validating-the-request-and-selectively-responding}

Jelenleg a webszerverünk a fájlban lévő HTML-t adja vissza, bármit is kért a
kliens. Adjunk hozzá olyan funkciót, amely a HTML-fájl visszaadása előtt
ellenőrzi, hogy a böngésző a _/_ útvonalat kéri-e, és hibát ad vissza, ha a
böngésző bármi mást kér. Ehhez módosítanunk kell a `handle_connection`
függvényt a 21-6. kódrészletben látható módon. Ez az új kód összeveti a
beérkezett kérés tartalmát azzal, amilyennek egy _/_ útvonalra szóló kérésről
tudjuk, hogy kinéz, és `if` és `else` blokkokat ad hozzá, hogy a kéréseket
eltérően kezelje.

<Listing number="21-6" file-name="src/main.rs" caption="A */* útvonalra érkező kérések a többi kéréstől eltérő kezelése">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-06/src/main.rs:here}}
```

</Listing>

Csak a HTTP-kérés első sorát fogjuk megvizsgálni, ezért ahelyett, hogy a
teljes kérést egy vektorba olvasnánk, a `next` meghívásával lekérjük az
iterátor első elemét. Az első `unwrap` az `Option`-t kezeli, és leállítja a
programot, ha az iterátornak nincsenek elemei. A második `unwrap` a
`Result`-ot kezeli, és ugyanaz a hatása, mint a 21-2. kódrészletben a `map`
belsejébe írt `unwrap`-nak.

Ezután megvizsgáljuk, hogy a `request_line` megegyezik-e egy, a _/_
útvonalra szóló GET kérés kérésének sorával. Ha igen, az `if` blokk a
HTML-fájlunk tartalmát adja vissza.

Ha a `request_line` _nem_ egyezik meg a _/_ útvonalra szóló GET kéréssel,
akkor valamilyen más kérést kaptunk. Hamarosan kódot adunk az `else`
blokkhoz, hogy minden más kérésre is válaszoljunk.

Futtasd most ezt a kódot, és kérd le a _127.0.0.1:7878_ címet; a
_hello.html_ HTML-tartalmát kell kapnod. Ha bármilyen más kérést küldesz,
például a _127.0.0.1:7878/something-else_ címre, kapcsolódási hibát kapsz,
ahhoz hasonlót, amilyet a 21-1. és a 21-2. kódrészlet kódjának futtatásakor
láttál.

Most adjuk hozzá a 21-7. kódrészlet kódját az `else` blokkhoz, hogy egy 404-es
állapotkódú választ adjunk vissza, amely azt jelzi, hogy a kért tartalom nem
található. Egy oldal HTML-jét is visszaadjuk, amelyet a böngésző
megjeleníthet, hogy a végfelhasználó lássa a választ.

<Listing number="21-7" file-name="src/main.rs" caption="Válasz 404-es állapotkóddal és egy hibaoldallal, ha bármi mást kértek, mint a */* útvonalat">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-07/src/main.rs:here}}
```

</Listing>

Itt a válaszunk állapotsorában a 404-es állapotkód és a `NOT FOUND` indoklás
szerepel. A válasz törzse a _404.html_ fájlban lévő HTML lesz. A hibaoldalhoz
létre kell hoznod egy _404.html_ fájlt a _hello.html_ mellett; ismét bármilyen
HTML-t használhatsz, vagy a 21-8. kódrészletben látható példa HTML-t.

<Listing number="21-8" file-name="404.html" caption="Minta tartalom a bármely 404-es válasszal visszaküldendő oldalhoz">

```html
{{#include ../listings/ch21-web-server/listing-21-07/404.html}}
```

</Listing>

Ezekkel a módosításokkal futtasd újra a szerveredet. A _127.0.0.1:7878_ cím
lekérése a _hello.html_ tartalmát kell, hogy visszaadja, minden más kérés,
például a _127.0.0.1:7878/foo_, pedig a _404.html_ hibaoldalának HTML-jét.

<!-- Old headings. Do not remove or links may break. -->

<a id="a-touch-of-refactoring"></a>

### Refaktorálás {#refactoring}

Jelenleg az `if` és az `else` blokk sok ismétlést tartalmaz: mindkettő
fájlokat olvas be, és a fájlok tartalmát az adatfolyamba írja. Csak az
állapotsor és a fájlnév különbözik. Tegyük tömörebbé a kódot azzal, hogy ezeket
a különbségeket külön `if` és `else` sorokba emeljük ki, amelyek az állapotsor
és a fájlnév értékét változókhoz rendelik; ezután ezeket a változókat feltétel
nélkül használhatjuk a fájl beolvasásához és a válasz kiírásához. A 21-9.
kódrészlet mutatja az eredményül kapott kódot a nagy `if` és `else` blokkok
lecserélése után.

<Listing number="21-9" file-name="src/main.rs" caption="Az `if` és `else` blokkok refaktorálása úgy, hogy csak a két eset között eltérő kódot tartalmazzák">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-09/src/main.rs:here}}
```

</Listing>

Most az `if` és az `else` blokk csak az állapotsor és a fájlnév megfelelő
értékét adja vissza egy tuple-ben; ezután szétbontással rendeljük ezt a két
értéket a `status_line` és a `filename` változóhoz egy, a `let` utasításban
szereplő mintával, ahogy a 19. fejezetben tárgyaltuk.

A korábban duplikált kód most az `if` és `else` blokkokon kívül van, és a
`status_line` és `filename` változókat használja. Így könnyebb átlátni a két
eset közötti különbséget, és csak egyetlen helyen kell módosítanunk a kódot,
ha meg akarjuk változtatni a fájlbeolvasás és a válaszírás működését. A 21-9.
kódrészlet kódja ugyanúgy viselkedik, mint a 21-7. kódrészleté.

Nagyszerű! Most már van egy egyszerű webszerverünk nagyjából 40 sornyi
Rust-kódban, amely egy kérésre egy tartalommal teli oldallal válaszol, minden
más kérésre pedig 404-es válasszal.

Jelenleg a szerverünk egyetlen szálon fut, vagyis egyszerre csak egy kérést
tud kiszolgálni. Vizsgáljuk meg, miért lehet ez probléma, néhány lassú kérés
szimulálásával. Ezután kijavítjuk, hogy a szerverünk egyszerre több kérést is
kezelni tudjon.
