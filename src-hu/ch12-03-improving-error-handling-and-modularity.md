## Refaktorálás a modularitás és a hibakezelés javításáért {#refactoring-to-improve-modularity-and-error-handling}

A program javítása érdekében négy problémát orvosolunk, amelyek a program
szerkezetével és a lehetséges hibák kezelésével kapcsolatosak. Először is a
`main` függvényünk most két feladatot lát el: feldolgozza az argumentumokat és
beolvassa a fájlokat. Ahogy a program nő, a `main` függvény által kezelt
különálló feladatok száma is növekedni fog. Minél több felelőssége van egy
függvénynek, annál nehezebb átlátni a működését, annál nehezebb tesztelni, és
annál nehezebb úgy módosítani, hogy egyik része se romoljon el. A legjobb, ha
szétválasztjuk a funkciókat, hogy minden függvény egyetlen feladatért feleljen.

Ez a második problémához is kapcsolódik: bár a `query` és a `file_path` a
programunk konfigurációs változói, az olyan változók, mint a `contents`, a
program logikájának végrehajtásához kellenek. Minél hosszabb lesz a `main`,
annál több változót kell hatókörbe hoznunk; minél több változó van
hatókörben, annál nehezebb nyomon követni, melyiknek mi a célja. A legjobb,
ha a konfigurációs változókat egyetlen struktúrába csoportosítjuk, hogy
egyértelmű legyen a céljuk.

A harmadik probléma, hogy az `expect` segítségével írunk ki hibaüzenetet, ha a
fájl beolvasása nem sikerül, de a hibaüzenet csak annyit ír ki, hogy `Should
have been able to read the file`. Egy fájl beolvasása többféle okból is
meghiúsulhat: például hiányozhat a fájl, vagy nincs jogosultságunk megnyitni.
Jelenleg a helyzettől függetlenül mindig ugyanazt a hibaüzenetet írnánk ki,
ami semmilyen információt nem adna a felhasználónak!

Negyedszer, az `expect` segítségével kezelünk egy hibát, és ha a felhasználó
nem ad meg elég argumentumot a program futtatásakor, a Rusttól egy `index out
of bounds` hibát kap, amely nem magyarázza el egyértelműen a problémát. Az
lenne a legjobb, ha az összes hibakezelő kód egy helyen lenne, így a kód
jövőbeli karbantartóinak csak egyetlen helyen kellene utánanézniük, ha a
hibakezelési logikán változtatni kell. Ha az összes hibakezelő kód egy helyen
van, azt is biztosítja, hogy a végfelhasználók számára érthető üzeneteket
írunk ki.

Oldjuk meg ezt a négy problémát a projektünk refaktorálásával.

<!-- Old headings. Do not remove or links may break. -->

<a id="separation-of-concerns-for-binary-projects"></a>

### A felelősségi körök szétválasztása bináris projektekben {#separating-concerns-in-binary-projects}

Az a szervezési probléma, hogy több feladat felelősségét is a `main`
függvényre bízzuk, sok bináris projektben előfordul. Ezért sok
Rust-programozó hasznosnak tartja, hogy szétválassza egy bináris program
különálló felelősségi köreit (concerns), amikor a `main` függvény kezd nagyra
nőni. A folyamat a következő lépésekből áll:

- Oszd fel a programodat egy _main.rs_ és egy _lib.rs_ fájlra, és helyezd át
  a program logikáját a _lib.rs_ fájlba.
- Amíg a parancssor-feldolgozó logika kicsi, maradhat a `main` függvényben.
- Amikor a parancssor-feldolgozó logika kezd bonyolulttá válni, emeld ki a
  `main` függvényből más függvényekbe vagy típusokba.

A folyamat után a `main` függvényben maradó felelősségek a következőkre
korlátozódnak:

- A parancssor-feldolgozó logika meghívása az argumentumok értékeivel
- Az egyéb konfiguráció beállítása
- Egy `run` függvény meghívása a _lib.rs_ fájlban
- A hiba kezelése, ha a `run` hibát ad vissza

Ez a minta a felelősségi körök szétválasztásáról (separation of concerns)
szól: a _main.rs_ a program futtatásáért felel, a _lib.rs_ pedig az adott
feladat teljes logikájáért. Mivel a `main` függvényt nem tesztelheted
közvetlenül, ez a szerkezet lehetővé teszi, hogy a program teljes logikáját
teszteld, miután kiemelted azt a `main` függvényből. A `main` függvényben
maradó kód elég kicsi lesz ahhoz, hogy pusztán elolvasva meggyőződhess a
helyességéről. Alakítsuk át a programunkat e folyamat szerint.

#### Az argumentumfeldolgozó kiemelése {#extracting-the-argument-parser}

Az argumentumok feldolgozásának funkcióját egy olyan függvénybe emeljük ki,
amelyet a `main` hív meg. A 12-5. kódrészlet a `main` függvény új elejét
mutatja, amely egy új, `parse_config` nevű függvényt hív meg; ezt a
_src/main.rs_ fájlban definiáljuk.

<Listing number="12-5" file-name="src/main.rs" caption="Egy `parse_config` függvény kiemelése a `main`-ből">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-05/src/main.rs:here}}
```

</Listing>

A parancssori argumentumokat továbbra is egy vektorba gyűjtjük, de ahelyett,
hogy a `main` függvényen belül az 1-es indexű argumentumértéket a `query`
változóhoz, a 2-es indexűt pedig a `file_path` változóhoz rendelnénk, az
egész vektort átadjuk a `parse_config` függvénynek. Ezután a `parse_config`
függvény tartalmazza azt a logikát, amely meghatározza, melyik argumentum
melyik változóba kerül, és visszaadja az értékeket a `main`-nek. A `query` és
a `file_path` változót továbbra is a `main`-ben hozzuk létre, de már nem a
`main` felelőssége meghatározni, hogyan felelnek meg egymásnak a parancssori
argumentumok és a változók.

Ez az átalakítás túlzásnak tűnhet egy ilyen kis programnál, de kis,
fokozatos lépésekben refaktorálunk. A változtatás után futtasd újra a
programot, hogy meggyőződj róla: az argumentumok feldolgozása továbbra is
működik. Érdemes gyakran ellenőrizni a haladást, mert így könnyebb
azonosítani a problémák okát, amikor felmerülnek.

#### A konfigurációs értékek csoportosítása {#grouping-configuration-values}

Egy újabb kis lépéssel tovább javíthatjuk a `parse_config` függvényt.
Jelenleg egy tuple-t adunk vissza, de aztán azonnal újra szétbontjuk az egyes
részeire. Ez arra utal, hogy talán még nem találtuk meg a megfelelő
absztrakciót.

Egy másik jel, amely arra mutat, hogy van még hová javítani, a `parse_config`
név `config` része, amely azt sugallja, hogy a két visszaadott érték
összetartozik, és mindkettő egyetlen konfigurációs érték része. Ezt a
jelentést jelenleg az adatok szerkezetében semmi más nem fejezi ki, csak az,
hogy a két értéket egy tuple-be csoportosítjuk; ehelyett a két értéket egy
struktúrába tesszük, és a struktúra mezőinek beszédes nevet adunk. Így a kód
jövőbeli karbantartói könnyebben megértik, hogyan kapcsolódnak egymáshoz a
különböző értékek, és mi a céljuk.

A 12-6. kódrészlet a `parse_config` függvény továbbfejlesztett változatát
mutatja.

<Listing number="12-6" file-name="src/main.rs" caption="A `parse_config` refaktorálása, hogy egy `Config` struktúra példányát adja vissza">

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-06/src/main.rs:here}}
```

</Listing>

Hozzáadtunk egy `Config` nevű struktúrát, amelynek `query` és `file_path`
nevű mezői vannak. A `parse_config` szignatúrája most azt jelzi, hogy egy
`Config` értéket ad vissza. A `parse_config` törzsében korábban olyan
sztringszeleteket adtunk vissza, amelyek az `args`-ban lévő `String`
értékekre hivatkoztak, most viszont úgy definiáljuk a `Config`-ot, hogy saját
tulajdonú `String` értékeket tartalmazzon. A `main`-ben lévő `args` változó
az argumentumértékek tulajdonosa, és csak kölcsönadja őket a `parse_config`
függvénynek, ami azt jelenti, hogy megsértenénk a Rust kölcsönzési
szabályait, ha a `Config` megpróbálná átvenni az `args`-ban lévő értékek
tulajdonjogát.

A `String` adatokat többféleképpen is kezelhetnénk; a legegyszerűbb, bár
kissé nem hatékony megoldás, ha meghívjuk az értékeken a `clone` metódust. Ez
teljes másolatot készít az adatokról, amelyek a `Config` példány tulajdonába
kerülnek, és ez több időt és memóriát igényel, mint ha egy referenciát
tárolnánk a sztringadatokra. Az adatok klónozása ugyanakkor nagyon egyszerűvé
teszi a kódunkat, mert nem kell a referenciák élettartamát kezelnünk; ebben a
helyzetben megéri egy kevés teljesítményt feláldozni az egyszerűségért
cserébe.

> ### A `clone` használatának előnyei és hátrányai {#the-trade-offs-of-using-clone}
>
> Sok rustacean hajlamos elkerülni a `clone` használatát a tulajdonjoggal
> kapcsolatos problémák megoldására, a futásidejű költsége miatt. A
> [13. fejezetben][ch13]<!-- ignore --> megtanulod, hogyan használhatsz
> hatékonyabb módszereket az ilyen helyzetekben. Egyelőre azonban teljesen
> rendben van néhány sztringet lemásolni, hogy haladhassunk, mert ezeket a
> másolatokat csak egyszer készíted el, és a fájl elérési útja és a keresett
> sztring is nagyon kicsi. Jobb egy kissé nem hatékony, de működő program,
> mint ha már az első nekifutásra túloptimalizálni próbálnád a kódot. Ahogy
> egyre tapasztaltabb leszel a Rustban, könnyebb lesz rögtön a leghatékonyabb
> megoldással kezdeni, de egyelőre teljesen elfogadható a `clone` meghívása.

Frissítettük a `main`-t, hogy a `parse_config` által visszaadott `Config`
példányt egy `config` nevű változóba tegye, és módosítottuk azt a kódot is,
amely korábban a különálló `query` és `file_path` változókat használta, hogy
most helyettük a `Config` struktúra mezőit használja.

A kódunk most már egyértelműbben kifejezi, hogy a `query` és a `file_path`
összetartozik, és az a céljuk, hogy beállítsák, hogyan működjön a program.
Minden kód, amely ezeket az értékeket használja, tudja, hogy a `config`
példányban, a céljuknak megfelelően elnevezett mezőkben találja őket.

#### Konstruktor készítése a `Config` számára {#creating-a-constructor-for-config}

Eddig kiemeltük a `main`-ből a parancssori argumentumok feldolgozásáért
felelős logikát, és a `parse_config` függvénybe helyeztük. Ennek
köszönhetően láttuk, hogy a `query` és a `file_path` értékek összetartoznak,
és ezt a kapcsolatot a kódunknak is ki kell fejeznie. Ezután hozzáadtunk egy
`Config` struktúrát, hogy megnevezzük a `query` és a `file_path` közös
célját, és hogy a `parse_config` függvényből az értékeket struktúramezőkként,
névvel ellátva adhassuk vissza.

Most, hogy a `parse_config` függvény célja egy `Config` példány létrehozása, a
`parse_config` egyszerű függvényt átalakíthatjuk egy `new` nevű függvénnyé,
amely a `Config` struktúrához van társítva. Ezzel a változtatással a kód
idiomatikusabb lesz. A standard könyvtár típusainak – például a `String`-nek
– úgy hozhatunk létre példányait, hogy meghívjuk a `String::new` függvényt.
Ehhez hasonlóan, ha a `parse_config`-ot a `Config`-hoz társított `new`
függvénnyé alakítjuk, a `Config::new` meghívásával hozhatunk létre `Config`
példányokat. A 12-7. kódrészlet mutatja a szükséges változtatásokat.

<Listing number="12-7" file-name="src/main.rs" caption="A `parse_config` átalakítása `Config::new` függvénnyé">

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-07/src/main.rs:here}}
```

</Listing>

A `main`-ben, ahol eddig a `parse_config`-ot hívtuk meg, most a `Config::new`
függvényt hívjuk. A `parse_config` nevét `new`-ra változtattuk, és egy `impl`
blokkba helyeztük, amely a `new` függvényt a `Config`-hoz társítja. Próbáld
meg újra lefordítani a kódot, hogy meggyőződj róla, működik.

### A hibakezelés javítása {#fixing-the-error-handling}

Most a hibakezelés javításán dolgozunk. Emlékezz vissza, hogy ha az `args`
vektor 1-es vagy 2-es indexén lévő értékhez próbálunk hozzáférni, a program
pánikol, ha a vektor háromnál kevesebb elemet tartalmaz. Próbáld meg
argumentumok nélkül futtatni a programot; ezt fogod látni:

```console
{{#include ../listings/ch12-an-io-project/listing-12-07/output.txt}}
```

Az `index out of bounds: the len is 1 but the index is 1` sor programozóknak
szóló hibaüzenet. Nem segít a végfelhasználóknak megérteni, mit kellene
tenniük helyette. Javítsuk ki ezt most.

#### A hibaüzenet javítása {#improving-the-error-message}

A 12-8. kódrészletben egy ellenőrzést adunk a `new` függvényhez, amely az 1-es
és a 2-es indexhez való hozzáférés előtt meggyőződik arról, hogy a szelet
elég hosszú. Ha a szelet nem elég hosszú, a program pánikol, és egy jobb
hibaüzenetet jelenít meg.

<Listing number="12-8" file-name="src/main.rs" caption="Az argumentumok számának ellenőrzése">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-08/src/main.rs:here}}
```

</Listing>

Ez a kód hasonlít [a 9-13. kódrészletben megírt `Guess::new`
függvényhez][ch9-custom-types]<!-- ignore -->, ahol a `panic!` makrót hívtuk
meg, ha a `value` argumentum kívül esett az érvényes értékek tartományán.
Itt nem egy értéktartományt ellenőrzünk, hanem azt, hogy az `args` hossza
legalább `3`, így a függvény többi része abból a feltevésből indulhat ki,
hogy ez a feltétel teljesül. Ha az `args` háromnál kevesebb elemet
tartalmaz, a feltétel `true` lesz, és meghívjuk a `panic!` makrót, hogy
azonnal leállítsuk a programot.

Miután ez a néhány extra sor bekerült a `new` függvénybe, futtassuk újra a
programot argumentumok nélkül, és nézzük meg, hogyan néz ki most a hiba:

```console
{{#include ../listings/ch12-an-io-project/listing-12-08/output.txt}}
```

Ez a kimenet már jobb: van egy értelmes hibaüzenetünk. Ugyanakkor olyan
fölösleges információk is megjelennek, amelyeket nem szeretnénk a
felhasználóink elé tárni. Talán a 9-13. kódrészletben alkalmazott technika
nem a legjobb választás itt: a `panic!` hívása inkább programozási hibára
való, mint használati problémára, [ahogy a 9. fejezetben
megbeszéltük][ch9-error-guidelines]<!-- ignore -->. Ehelyett a 9. fejezetben
megismert másik technikát alkalmazzuk: [egy `Result` értéket
adunk vissza][ch9-result]<!-- ignore -->, amely vagy a sikert, vagy egy
hibát jelez.

<!-- Old headings. Do not remove or links may break. -->

<a id="returning-a-result-from-new-instead-of-calling-panic"></a>

#### `Result` visszaadása a `panic!` hívása helyett {#returning-a-result-instead-of-calling-panic}

Ehelyett visszaadhatunk egy `Result` értéket, amely sikeres esetben egy
`Config` példányt tartalmaz, hiba esetén pedig leírja a problémát. A függvény
nevét is megváltoztatjuk `new`-ról `build`-re, mert sok programozó azt várja,
hogy a `new` függvények soha ne hiúsuljanak meg. Amikor a `Config::build` a
`main`-nel kommunikál, a `Result` típussal jelezhetjük, hogy probléma
történt. Ezután módosíthatjuk a `main`-t úgy, hogy az `Err` változatot a
felhasználók számára hasznosabb hibává alakítsa, a `panic!` hívása által
okozott, a `thread 'main'`-ről és a `RUST_BACKTRACE`-ről szóló kísérőszöveg
nélkül.

A 12-9. kódrészlet azokat a változtatásokat mutatja, amelyeket a most már
`Config::build` nevű függvény visszatérési értékén és törzsén kell
végrehajtanunk ahhoz, hogy `Result`-ot adjon vissza. Vedd figyelembe, hogy ez
addig nem fordul le, amíg a `main`-t is nem frissítjük; ezt a következő
kódrészletben tesszük meg.

<Listing number="12-9" file-name="src/main.rs" caption="`Result` visszaadása a `Config::build` függvényből">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-09/src/main.rs:here}}
```

</Listing>

A `build` függvényünk egy `Result`-ot ad vissza, amely sikeres esetben egy
`Config` példányt, hiba esetén pedig egy sztringliterált tartalmaz. A
hibaértékeink mindig `'static` élettartamú sztringliterálok lesznek.

A függvény törzsében két változtatást hajtottunk végre: ahelyett, hogy a
`panic!` makrót hívnánk meg, ha a felhasználó nem ad meg elég argumentumot,
most egy `Err` értéket adunk vissza, a `Config` visszatérési értéket pedig
egy `Ok`-ba csomagoltuk. Ezekkel a változtatásokkal a függvény megfelel az új
típusszignatúrájának.

Ha a `Config::build` egy `Err` értéket ad vissza, a `main` függvény kezelheti
a `build` függvény által visszaadott `Result` értéket, és hiba esetén
tisztábban léptetheti ki a folyamatot.

<!-- Old headings. Do not remove or links may break. -->

<a id="calling-confignew-and-handling-errors"></a>

#### A `Config::build` meghívása és a hibák kezelése {#calling-configbuild-and-handling-errors}

Ahhoz, hogy kezeljük a hibás esetet, és felhasználóbarát üzenetet írjunk ki,
frissítenünk kell a `main`-t, hogy kezelje a `Config::build` által
visszaadott `Result`-ot, ahogy a 12-10. kódrészlet mutatja. Azt a
felelősséget is elvesszük a `panic!`-től, hogy nem nulla hibakóddal léptesse
ki a parancssori eszközt, és ezt inkább kézzel valósítjuk meg. A nem nulla
kilépési kód (exit status) egy konvenció, amellyel a programunkat meghívó
folyamatnak jelezzük, hogy a program hibaállapotban lépett ki.

<Listing number="12-10" file-name="src/main.rs" caption="Kilépés hibakóddal, ha a `Config` létrehozása nem sikerül">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-10/src/main.rs:here}}
```

</Listing>

Ebben a kódrészletben egy olyan metódust használtunk, amelyet még nem
tárgyaltunk részletesen: az `unwrap_or_else`-t, amelyet a standard könyvtár
a `Result<T, E>` típuson definiál. Az `unwrap_or_else` segítségével saját,
`panic!` nélküli hibakezelést definiálhatunk. Ha a `Result` egy `Ok` érték, a
metódus az `unwrap`-hoz hasonlóan viselkedik: visszaadja az `Ok` által
becsomagolt belső értéket. Ha viszont az érték `Err`, a metódus a closure-ben
lévő kódot hívja meg; a closure egy névtelen függvény, amelyet mi definiálunk,
és argumentumként átadunk az `unwrap_or_else`-nek. A closure-öket a
[13. fejezetben][ch13]<!-- ignore --> tárgyaljuk részletesebben. Egyelőre
csak annyit kell tudnod, hogy az `unwrap_or_else` az `Err` belső értékét –
ebben az esetben a 12-9. kódrészletben hozzáadott `"not enough arguments"`
statikus sztringet – átadja a closure-ünknek a függőleges vonalak között
szereplő `err` argumentumban. A closure-ben lévő kód ezután futás közben
használhatja az `err` értéket.

Hozzáadtunk egy új `use` sort, hogy a standard könyvtárból hatókörbe hozzuk a
`process`-t. A closure-ben lévő, hiba esetén lefutó kód mindössze két sor:
kiírjuk az `err` értéket, majd meghívjuk a `process::exit` függvényt. A
`process::exit` függvény azonnal leállítja a programot, és a neki átadott
számot adja vissza kilépési kódként. Ez hasonlít a 12-8. kódrészletben
használt, `panic!`-re épülő kezeléshez, de már nem kapjuk meg a sok extra
kimenetet. Próbáljuk ki:

```console
{{#include ../listings/ch12-an-io-project/listing-12-10/output.txt}}
```

Remek! Ez a kimenet sokkal barátságosabb a felhasználóink számára.

<!-- Old headings. Do not remove or links may break. -->

<a id="extracting-logic-from-the-main-function"></a>

### A logika kiemelése a `main`-ből {#extracting-logic-from-main}

Most, hogy befejeztük a konfiguráció feldolgozásának refaktorálását,
térjünk rá a program logikájára. Ahogy [„A felelősségi körök szétválasztása
bináris projektekben”](#separation-of-concerns-for-binary-projects)<!-- ignore
--> szakaszban leírtuk, kiemelünk egy `run` nevű függvényt, amely a `main`
függvény jelenlegi logikájából mindazt tartalmazza, ami nem a konfiguráció
beállításával vagy a hibák kezelésével foglalkozik. Ha végeztünk, a `main`
függvény tömör lesz, és ránézésre is könnyen ellenőrizhető, a többi
logikához pedig teszteket írhatunk.

A 12-11. kódrészlet egy `run` függvény kiemelésének kis, fokozatos javítását
mutatja.

<Listing number="12-11" file-name="src/main.rs" caption="A program többi logikáját tartalmazó `run` függvény kiemelése">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-11/src/main.rs:here}}
```

</Listing>

A `run` függvény most a `main` összes fennmaradó logikáját tartalmazza, a
fájl beolvasásától kezdve. A `run` függvény argumentumként kapja meg a
`Config` példányt.

<!-- Old headings. Do not remove or links may break. -->

<a id="returning-errors-from-the-run-function"></a>

#### Hibák visszaadása a `run` függvényből {#returning-errors-from-run}

Most, hogy a program fennmaradó logikája a `run` függvénybe került,
javíthatjuk a hibakezelést, ahogy a 12-9. kódrészletben a `Config::build`
esetében is tettük. Ahelyett, hogy az `expect` meghívásával hagynánk
pánikolni a programot, a `run` függvény egy `Result<T, E>` értéket ad vissza,
ha valami hiba történik. Így a hibák kezelésének logikáját felhasználóbarát
módon tovább összpontosíthatjuk a `main`-ben. A 12-12. kódrészlet mutatja,
milyen változtatásokat kell végrehajtanunk a `run` szignatúráján és
törzsén.

<Listing number="12-12" file-name="src/main.rs" caption="A `run` függvény módosítása, hogy `Result`-ot adjon vissza">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-12/src/main.rs:here}}
```

</Listing>

Három jelentős változtatást hajtottunk végre. Először is a `run` függvény
visszatérési típusát `Result<(), Box<dyn Error>>`-ra változtattuk. Ez a
függvény korábban a unit típust, a `()`-t adta vissza, és ezt az `Ok` esetben
visszaadott értékként megtartjuk.

A hibatípushoz a `Box<dyn Error>` trait objektumot használtuk (és a fájl
tetején egy `use` utasítással hatókörbe hoztuk az `std::error::Error`-t). A
trait objektumokat a [18. fejezetben][ch18]<!-- ignore --> tárgyaljuk.
Egyelőre elég annyit tudnod, hogy a `Box<dyn Error>` azt jelenti, hogy a
függvény egy olyan típust ad vissza, amely megvalósítja az `Error` traitet,
de nem kell megadnunk, pontosan milyen típusú lesz a visszatérési érték. Ez
rugalmasságot ad ahhoz, hogy a különböző hibás esetekben különböző típusú
hibaértékeket adhassunk vissza. A `dyn` kulcsszó a _dynamic_ (dinamikus)
rövidítése.

Másodszor, az `expect` hívását a `?` operátorra cseréltük, amelyről a
[9. fejezetben][ch9-question-mark]<!-- ignore --> beszéltünk. Ahelyett, hogy
hiba esetén `panic!`-et váltana ki, a `?` visszaadja a hibaértéket az
aktuális függvényből, hogy a hívó kezelje.

Harmadszor, a `run` függvény sikeres esetben most egy `Ok` értéket ad vissza.
A szignatúrában a `run` függvény sikeres típusaként a `()`-t adtuk meg, ami
azt jelenti, hogy a unit típusú értéket be kell csomagolnunk az `Ok` értékbe.
Ez az `Ok(())` szintaxis elsőre kissé furcsának tűnhet. De a `()` ilyen
használata az idiomatikus módja annak, hogy jelezzük: a `run`-t csak a
mellékhatásai miatt hívjuk meg; nem ad vissza olyan értéket, amelyre
szükségünk volna.

Ha lefuttatod ezt a kódot, lefordul, de egy figyelmeztetést jelenít meg:

```console
{{#include ../listings/ch12-an-io-project/listing-12-12/output.txt}}
```

A Rust azt jelzi, hogy a kódunk figyelmen kívül hagyta a `Result` értéket,
pedig a `Result` érték azt is jelezheti, hogy hiba történt. Mi azonban nem
ellenőrizzük, hogy történt-e hiba, és a fordító emlékeztet minket, hogy
valószínűleg valamilyen hibakezelő kódot szerettünk volna ide írni! Hozzuk
most rendbe ezt a problémát.

#### A `run` által visszaadott hibák kezelése a `main`-ben {#handling-errors-returned-from-run-in-main}

A hibákat a 12-10. kódrészletben a `Config::build` esetében alkalmazotthoz
hasonló technikával ellenőrizzük és kezeljük, egy kis különbséggel:

<span class="filename">Fájlnév: src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/no-listing-01-handling-errors-in-main/src/main.rs:here}}
```

Az `unwrap_or_else` helyett az `if let` szerkezettel ellenőrizzük, hogy a
`run` `Err` értéket ad-e vissza, és ha igen, meghívjuk a `process::exit(1)`
függvényt. A `run` függvény nem ad vissza olyan értéket, amelyet ugyanúgy ki
akarnánk csomagolni az `unwrap`-pal, ahogy a `Config::build` visszaadja a
`Config` példányt. Mivel a `run` sikeres esetben `()`-t ad vissza, csak a
hiba észlelése érdekel minket, így nincs szükségünk az `unwrap_or_else`-re a
kicsomagolt érték visszaadásához, hiszen az úgyis csak `()` lenne.

Az `if let` és az `unwrap_or_else` függvények törzse mindkét esetben
ugyanaz: kiírjuk a hibát, és kilépünk.

### A kód szétválasztása egy könyvtár crate-be {#splitting-code-into-a-library-crate}

A `minigrep` projektünk eddig jól halad! Most szétválasztjuk a _src/main.rs_
fájlt, és a kód egy részét a _src/lib.rs_ fájlba tesszük. Így tesztelhetjük a
kódot, és a _src/main.rs_ fájlnak kevesebb felelőssége lesz.

A szövegben keresésért felelős kódot a _src/main.rs_ helyett a _src/lib.rs_
fájlban definiáljuk, így mi (vagy bárki más, aki a `minigrep` könyvtárunkat
használja) a keresőfüggvényt a `minigrep` binárisunknál több helyről is
meghívhatjuk.

Először definiáljuk a `search` függvény szignatúráját a _src/lib.rs_ fájlban a
12-13. kódrészletben látható módon, egy olyan törzzsel, amely az
`unimplemented!` makrót hívja meg. A szignatúrát részletesebben akkor
magyarázzuk el, amikor kitöltjük a megvalósítást.

<Listing number="12-13" file-name="src/lib.rs" caption="A `search` függvény definiálása a *src/lib.rs* fájlban">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-13/src/lib.rs}}
```

</Listing>

A függvénydefiníción a `pub` kulcsszót használtuk, hogy a `search`-öt a
könyvtár crate-ünk nyilvános API-jának részévé tegyük. Most már van egy
könyvtár crate-ünk, amelyet a bináris crate-ünkből használhatunk, és amelyet
tesztelhetünk!

Most a _src/lib.rs_ fájlban definiált kódot a _src/main.rs_ fájlban lévő
bináris crate hatókörébe kell hoznunk, és meg kell hívnunk, ahogy a 12-14.
kódrészlet mutatja.

<Listing number="12-14" file-name="src/main.rs" caption="A `minigrep` könyvtár crate `search` függvényének használata a *src/main.rs* fájlban">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-14/src/main.rs:here}}
```

</Listing>

Hozzáadunk egy `use minigrep::search` sort, hogy a `search` függvényt a
könyvtár crate-ből a bináris crate hatókörébe hozzuk. Ezután a `run`
függvényben a fájl tartalmának kiírása helyett meghívjuk a `search`
függvényt, és argumentumként átadjuk neki a `config.query` értéket és a
`contents`-et. Ezután a `run` egy `for` ciklussal kiírja a `search` által
visszaadott, a keresett kifejezésre illeszkedő sorokat. Ez egyben jó
alkalom arra is, hogy eltávolítsuk a `main` függvényből azokat a `println!`
hívásokat, amelyek a keresett kifejezést és a fájl elérési útját írták ki,
így a programunk (ha nem történik hiba) csak a keresés eredményeit írja ki.

Vedd figyelembe, hogy a keresőfüggvény az összes eredményt egy vektorba
gyűjti, amelyet visszaad, mielőtt bármit kiírnánk. Ez a megvalósítás
nagy fájlokban való keresésnél lassan jelenítheti meg az eredményeket, mert
azokat nem a megtalálásuk pillanatában írjuk ki; a 13. fejezetben
megvizsgálunk egy lehetséges megoldást erre az iterátorok segítségével.

Huh! Ez sok munka volt, de megalapoztuk a jövőbeli sikereinket. Most már
sokkal könnyebb kezelni a hibákat, és a kódot is modulárisabbá tettük.
Mostantól szinte minden munkánkat a _src/lib.rs_ fájlban végezzük.

Használjuk ki ezt az újonnan szerzett modularitást, és tegyünk valamit, ami a
régi kóddal nehéz lett volna, az újjal viszont könnyű: írjunk néhány tesztet!

[ch13]: ch13-00-functional-features.html
[ch9-custom-types]: ch09-03-to-panic-or-not-to-panic.html#creating-custom-types-for-validation
[ch9-error-guidelines]: ch09-03-to-panic-or-not-to-panic.html#guidelines-for-error-handling
[ch9-result]: ch09-02-recoverable-errors-with-result.html
[ch18]: ch18-00-oop.html
[ch9-question-mark]: ch09-02-recoverable-errors-with-result.html#a-shortcut-for-propagating-errors-the--operator
