<!-- Old headings. Do not remove or links may break. -->

<a id="turning-our-single-threaded-server-into-a-multithreaded-server"></a>
<a id="from-single-threaded-to-multithreaded-server"></a>

## Egyszálú szerverből többszálú {#from-a-single-threaded-to-a-multithreaded-server}

Jelenleg a szerver sorban egymás után dolgozza fel a kéréseket, vagyis addig
nem kezd hozzá a második kapcsolat feldolgozásához, amíg az első kapcsolat
feldolgozása be nem fejeződött. Ha a szerverhez egyre több kérés érkezne, ez a
soros végrehajtás egyre kevésbé lenne optimális. Ha a szerver olyan kérést
kap, amelynek a feldolgozása sokáig tart, a további kéréseknek meg kell
várniuk, amíg a hosszú kérés befejeződik, még akkor is, ha az új kérések
gyorsan feldolgozhatók lennének. Ezt ki kell javítanunk, de előbb nézzük meg
a problémát működés közben.

<!-- Old headings. Do not remove or links may break. -->

<a id="simulating-a-slow-request-in-the-current-server-implementation"></a>

### Egy lassú kérés szimulálása {#simulating-a-slow-request}

Megnézzük, hogyan befolyásolhatja egy lassan feldolgozott kérés a jelenlegi
szervermegvalósításunkhoz érkező többi kérést. A 21-10. kódrészlet egy
_/sleep_ útvonalra érkező kérés kezelését valósítja meg egy szimulált lassú
válasszal, amely miatt a szerver öt másodpercig alszik, mielőtt válaszolna.

<Listing number="21-10" file-name="src/main.rs" caption="Egy lassú kérés szimulálása ötmásodperces alvással">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-10/src/main.rs:here}}
```

</Listing>

Most, hogy három esetünk van, az `if`-ről `match`-re váltottunk. A
`request_line` egy szeletére kifejezetten illesztenünk kell ahhoz, hogy a
sztringliterál-értékekre mintaillesztést végezhessünk; a `match` nem végez
automatikus referenciaképzést és dereferálást, ahogy az egyenlőségvizsgáló
metódus.

Az első ág ugyanaz, mint a 21-9. kódrészlet `if` blokkja. A második ág a
_/sleep_ útvonalra érkező kérésre illeszkedik. Amikor ilyen kérés érkezik, a
szerver öt másodpercig alszik, mielőtt megjelenítené a sikeres HTML-oldalt. A
harmadik ág ugyanaz, mint a 21-9. kódrészlet `else` blokkja.

Láthatod, mennyire kezdetleges a szerverünk: a valódi könyvtárak sokkal
tömörebben kezelnék a különféle kérések felismerését!

Indítsd el a szervert a `cargo run` paranccsal. Ezután nyiss meg két
böngészőablakot: az egyikben a _http://127.0.0.1:7878_, a másikban a
_http://127.0.0.1:7878/sleep_ címet. Ha a korábbiakhoz hasonlóan néhányszor
beírod a _/_ URI-t, láthatod, hogy gyorsan válaszol. Ha viszont beírod a
_/sleep_ címet, majd betöltöd a _/_ címet, látni fogod, hogy a _/_ megvárja,
amíg a `sleep` végigalussza a teljes öt másodpercet, és csak utána töltődik
be.

Több technikát is alkalmazhatnánk, hogy a kérések ne torlódjanak fel egy
lassú kérés mögött, például az async használatát, ahogy a 17. fejezetben
tettük; mi egy szálkészletet fogunk megvalósítani.

### Az áteresztőképesség javítása szálkészlettel {#improving-throughput-with-a-thread-pool}

A _szálkészlet (thread pool)_ elindított szálak csoportja, amelyek készen
állnak egy feladat kezelésére, és várnak rá. Amikor a program új feladatot
kap, a készlet egyik szálát a feladathoz rendeli, és az a szál dolgozza fel a
feladatot. A készlet többi szála elérhető marad minden más feladat
kezelésére, amely az első szál feldolgozása közben beérkezik. Amikor az első
szál végzett a feladata feldolgozásával, visszakerül a tétlen szálak
készletébe, és készen áll egy új feladat kezelésére. A szálkészlet lehetővé
teszi, hogy a kapcsolatokat konkurensen dolgozd fel, ami növeli a szervered
áteresztőképességét.

A készletben lévő szálak számát egy kis számra korlátozzuk, hogy megvédjük
magunkat a szolgáltatásmegtagadásos (DoS) támadásoktól; ha a programunk
minden beérkező kéréshez új szálat hozna létre, valaki, aki 10 millió kérést
küld a szerverünknek, komoly kárt okozhatna azzal, hogy elhasználja a
szerverünk összes erőforrását, és teljesen leállítja a kérések
feldolgozását.

Ezért ahelyett, hogy korlátlan számú szálat indítanánk, rögzített számú szál
fog várakozni a készletben. A beérkező kéréseket feldolgozásra a készletnek
küldjük. A készlet a beérkező kérésekből egy várakozási sort tart fenn. A
készlet minden szála kivesz egy kérést ebből a sorból, kezeli a kérést, majd
újabb kérést kér a sortól. Ezzel a felépítéssel legfeljebb _`N`_ kérést
dolgozhatunk fel konkurensen, ahol _`N`_ a szálak száma. Ha minden szál egy
hosszan futó kérésre válaszol, a további kérések továbbra is feltorlódhatnak
a sorban, de megnöveltük azoknak a hosszan futó kéréseknek a számát, amelyeket
kezelni tudunk, mielőtt ez bekövetkezne.

Ez a technika csak egy a sok közül, amellyel egy webszerver
áteresztőképessége javítható. Más lehetőségek, amelyeket felfedezhetsz: a
fork/join modell, az egyszálú aszinkron I/O modell és a többszálú aszinkron
I/O modell. Ha érdekel a téma, olvass többet a többi megoldásról, és próbáld
meg megvalósítani őket; egy olyan alacsony szintű nyelvvel, mint a Rust, ezek
mindegyike lehetséges.

Mielőtt nekilátnánk a szálkészlet megvalósításának, beszéljünk arról, hogyan
kellene kinéznie a készlet használatának. Amikor kódot tervezel, segíthet a
tervezésben, ha először a kliens felőli interfészt írod meg. Úgy írd meg a
kód API-ját, hogy az olyan szerkezetű legyen, ahogyan hívni szeretnéd; aztán
ezen a szerkezeten belül valósítsd meg a funkciókat, ahelyett, hogy előbb a
funkciókat valósítanád meg, és utána terveznéd meg a nyilvános API-t.

Ahhoz hasonlóan, ahogy a 12. fejezet projektjében tesztvezérelt fejlesztést
alkalmaztunk, itt fordítóvezérelt fejlesztést (compiler-driven development)
fogunk alkalmazni. Megírjuk a kódot, amely a kívánt függvényeket hívja, majd
a fordító hibaüzeneteiből állapítjuk meg, mit kell legközelebb módosítanunk,
hogy a kód működjön. Mielőtt azonban ezt megtennénk, kiindulópontként
megvizsgáljuk azt a technikát, amelyet nem fogunk használni.

<!-- Old headings. Do not remove or links may break. -->

<a id="code-structure-if-we-could-spawn-a-thread-for-each-request"></a>

#### Szál indítása minden kéréshez {#spawning-a-thread-for-each-request}

Először nézzük meg, hogyan nézne ki a kódunk, ha minden kapcsolathoz új
szálat hozna létre. Ahogy korábban említettük, a korlátlan számú szál
indításának lehetséges problémái miatt nem ez a végleges tervünk, de jó
kiindulópont ahhoz, hogy először egy működő többszálú szervert kapjunk.
Ezután továbbfejlesztésként hozzáadjuk a szálkészletet, és így könnyebb lesz
összevetni a két megoldást.

A 21-11. kódrészlet azokat a módosításokat mutatja, amelyeket a `main`-ben
kell elvégezni ahhoz, hogy a `for` ciklusban minden adatfolyam kezeléséhez új
szálat indítsunk.

<Listing number="21-11" file-name="src/main.rs" caption="Új szál indítása minden adatfolyamhoz">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-11/src/main.rs:here}}
```

</Listing>

Ahogy a 16. fejezetben megtanultad, a `thread::spawn` létrehoz egy új szálat,
majd az új szálban futtatja a closure-ben lévő kódot. Ha futtatod ezt a kódot,
és a böngésződben betöltöd a _/sleep_ címet, majd két további böngészőfülön a
_/_ címet, valóban láthatod, hogy a _/_ címre érkező kéréseknek nem kell
megvárniuk, amíg a _/sleep_ befejeződik. Ahogy azonban említettük, ez végül
túlterheli a rendszert, mert korlát nélkül hoznál létre új szálakat.

Talán a 17. fejezetből is emlékszel, hogy éppen ez az a helyzet, amelyben az
async és az await igazán elemükben vannak! Tartsd ezt észben, amíg a
szálkészletet építjük, és gondold végig, mi lenne másképp vagy ugyanígy az
async használatával.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-a-similar-interface-for-a-finite-number-of-threads"></a>

#### Véges számú szál létrehozása {#creating-a-finite-number-of-threads}

Azt szeretnénk, hogy a szálkészletünk hasonló, ismerős módon működjön, hogy a
szálakról szálkészletre való váltás ne igényeljen nagy változtatásokat az
API-nkat használó kódban. A 21-12. kódrészlet egy `ThreadPool` struktúra
elképzelt interfészét mutatja, amelyet a `thread::spawn` helyett szeretnénk
használni.

<Listing number="21-12" file-name="src/main.rs" caption="Az ideális `ThreadPool` interfészünk">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch21-web-server/listing-21-12/src/main.rs:here}}
```

</Listing>

A `ThreadPool::new` segítségével egy új szálkészletet hozunk létre
konfigurálható számú szállal, ebben az esetben néggyel. Ezután a `for`
ciklusban a `pool.execute` interfésze a `thread::spawn`-éhoz hasonló, abban az
értelemben, hogy egy closure-t vár, amelyet a készletnek minden adatfolyamra
le kell futtatnia. Meg kell valósítanunk a `pool.execute`-ot úgy, hogy átvegye
a closure-t, és odaadja a készlet egyik szálának futtatásra. Ez a kód még nem
fordul le, de azért megpróbáljuk lefordítani, hogy a fordító eligazítson
minket a javításban.

<!-- Old headings. Do not remove or links may break. -->

<a id="building-the-threadpool-struct-using-compiler-driven-development"></a>

#### A `ThreadPool` elkészítése fordítóvezérelt fejlesztéssel {#building-threadpool-using-compiler-driven-development}

Végezd el a 21-12. kódrészlet módosításait a _src/main.rs_ fájlban, majd a
`cargo check` fordítási hibái alapján haladjunk a fejlesztéssel. Íme az első
hiba, amelyet kapunk:

```console
{{#include ../listings/ch21-web-server/listing-21-12/output.txt}}
```

Remek! Ez a hiba azt jelzi, hogy szükségünk van egy `ThreadPool` típusra vagy
modulra, úgyhogy most elkészítünk egyet. A `ThreadPool` megvalósításunk
független lesz attól, milyen munkát végez a webszerverünk. Ezért alakítsuk át
a `hello` crate-et bináris crate-ből könyvtár crate-té, amely a `ThreadPool`
megvalósításunkat tartalmazza. A könyvtár crate-re való átállás után a
különálló szálkészlet-könyvtárat bármilyen olyan munkára használhatnánk,
amelyhez szálkészletre van szükség, nemcsak webes kérések kiszolgálására.

Hozz létre egy _src/lib.rs_ fájlt a következő tartalommal, amely a
`ThreadPool` struktúra jelenleg lehetséges legegyszerűbb definíciója:

<Listing file-name="src/lib.rs">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/no-listing-01-define-threadpool-struct/src/lib.rs}}
```

</Listing>


Ezután szerkeszd a _main.rs_ fájlt, hogy a könyvtár crate-ből hatókörbe hozd
a `ThreadPool`-t; ehhez add hozzá a következő kódot a _src/main.rs_ elejéhez:

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch21-web-server/no-listing-01-define-threadpool-struct/src/main.rs:here}}
```

</Listing>

Ez a kód még mindig nem működik, de ellenőrizzük újra, hogy megkapjuk a
következő hibát, amellyel foglalkoznunk kell:

```console
{{#include ../listings/ch21-web-server/no-listing-01-define-threadpool-struct/output.txt}}
```

Ez a hiba azt jelzi, hogy a következő lépésben létre kell hoznunk egy `new`
nevű társított függvényt a `ThreadPool` számára. Azt is tudjuk, hogy a
`new`-nak egy olyan paraméterre van szüksége, amely argumentumként elfogadja a
`4`-et, és egy `ThreadPool` példányt kell visszaadnia. Valósítsuk meg a
legegyszerűbb `new` függvényt, amely rendelkezik ezekkel a tulajdonságokkal:

<Listing file-name="src/lib.rs">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/no-listing-02-impl-threadpool-new/src/lib.rs}}
```

</Listing>

A `size` paraméter típusának azért a `usize`-t választottuk, mert tudjuk, hogy
a negatív számú szálnak semmi értelme. Azt is tudjuk, hogy ezt a `4`-et egy
szálakból álló gyűjtemény elemeinek számaként fogjuk használni, és pontosan
erre való a `usize` típus, ahogy a 3. fejezet
[„Egész típusok”][integer-types]<!-- ignore --> részében tárgyaltuk.

Ellenőrizzük újra a kódot:

```console
{{#include ../listings/ch21-web-server/no-listing-02-impl-threadpool-new/output.txt}}
```

Most azért kapunk hibát, mert a `ThreadPool`-nak nincs `execute` metódusa.
Emlékezz vissza: a [„Véges számú szál
létrehozása”](#creating-a-finite-number-of-threads)<!-- ignore --> részben
úgy döntöttünk, hogy a szálkészletünknek a `thread::spawn`-éhoz hasonló
interfésszel kell rendelkeznie. Emellett az `execute` függvényt úgy valósítjuk
meg, hogy átvegye a kapott closure-t, és odaadja a készlet egyik tétlen
szálának futtatásra.

Az `execute` metódust a `ThreadPool`-on úgy definiáljuk, hogy paraméterként
egy closure-t vegyen át. Emlékezz vissza a 13. fejezet [„Elkapott értékek
kimozgatása a closure-ökből”][moving-out-of-closures]<!-- ignore --> részéből,
hogy a closure-öket háromféle traittel vehetjük át paraméterként: `Fn`,
`FnMut` és `FnOnce`. El kell döntenünk, milyen closure-t használjunk itt.
Tudjuk, hogy végül valami olyasmit fogunk csinálni, mint a standard könyvtár
`thread::spawn` megvalósítása, így megnézhetjük, milyen korlátokat ír elő a
`thread::spawn` szignatúrája a paraméterére. A dokumentáció a következőt
mutatja:

```rust,ignore
pub fn spawn<F, T>(f: F) -> JoinHandle<T>
    where
        F: FnOnce() -> T,
        F: Send + 'static,
        T: Send + 'static,
```

Itt az `F` típusparaméter az, amellyel foglalkozunk; a `T` típusparaméter a
visszatérési értékhez kapcsolódik, és az most nem érdekel minket. Láthatjuk,
hogy a `spawn` az `FnOnce`-t használja trait-korlátként az `F`-en. Valószínűleg
nekünk is erre van szükségünk, mert az `execute`-ban kapott argumentumot végül
továbbadjuk a `spawn`-nak. Még biztosabbak lehetünk abban, hogy az `FnOnce` a
megfelelő trait, mert egy kérést futtató szál az adott kérés closure-ját csak
egyszer hajtja végre, ami egybevág az `FnOnce`-beli `Once`-szal.

Az `F` típusparaméternek van még egy `Send` trait-korlátja és egy `'static`
élettartam-korlátja is, amelyek a mi helyzetünkben hasznosak: a `Send`-re
azért van szükség, hogy a closure-t átvihessük egyik szálból a másikba, a
`'static`-ra pedig azért, mert nem tudjuk, mennyi ideig tart a szálnak a
végrehajtás. Hozzunk létre a `ThreadPool`-on egy `execute` metódust, amely egy
`F` típusú generikus paramétert vár ezekkel a korlátokkal:

<Listing file-name="src/lib.rs">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/no-listing-03-define-execute/src/lib.rs:here}}
```

</Listing>

Az `FnOnce` után továbbra is ott a `()`, mert ez az `FnOnce` egy olyan
closure-t jelöl, amely nem vár paramétereket, és a `()` unit típust adja
vissza. A függvénydefiníciókhoz hasonlóan a visszatérési típus elhagyható a
szignatúrából, de a zárójelekre akkor is szükség van, ha nincsenek
paramétereink.

Ez ismét az `execute` metódus legegyszerűbb megvalósítása: nem csinál
semmit, de most csak azt próbáljuk elérni, hogy a kódunk leforduljon.
Ellenőrizzük újra:

```console
{{#include ../listings/ch21-web-server/no-listing-03-define-execute/output.txt}}
```

Lefordul! De vedd észre, hogy ha kipróbálod a `cargo run`-t, és küldesz egy
kérést a böngészőből, akkor a böngészőben ugyanazokat a hibákat látod, mint a
fejezet elején. A könyvtárunk valójában még nem hívja meg az `execute`-nak
átadott closure-t!

> Megjegyzés: A szigorú fordítóval rendelkező nyelvekről, például a Haskellről
> és a Rustról, gyakran hallani azt a mondást, hogy „Ha a kód lefordul, akkor
> működik is.” Ez a mondás azonban nem mindig igaz. A projektünk lefordul, de
> semmit sem csinál! Ha valódi, teljes projektet építenénk, most lenne jó
> alkalom egységtesztek írására, amelyek ellenőrzik, hogy a kód lefordul,
> _és_ a kívánt módon viselkedik.

Gondold végig: mi lenne itt másképp, ha closure helyett egy future-t
kellene végrehajtanunk?

#### A szálak számának ellenőrzése a `new`-ban {#validating-the-number-of-threads-in-new}

A `new` és az `execute` paramétereivel egyelőre semmit sem csinálunk.
Valósítsuk meg ezeknek a függvényeknek a törzsét a kívánt viselkedéssel.
Kezdjük a `new`-val. Korábban előjel nélküli típust választottunk a `size`
paraméterhez, mert egy negatív számú szálból álló készletnek nincs értelme.
Ugyanakkor a nulla szálból álló készletnek sincs értelme, a nulla mégis
teljesen érvényes `usize` érték. Hozzáadunk egy kódot, amely a `ThreadPool`
példány visszaadása előtt ellenőrzi, hogy a `size` nagyobb-e nullánál, és az
`assert!` makró segítségével pánikoltatjuk a programot, ha nullát kap, ahogy a
21-13. kódrészlet mutatja.

<Listing number="21-13" file-name="src/lib.rs" caption="A `ThreadPool::new` megvalósítása úgy, hogy pánikoljon, ha a `size` nulla">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-13/src/lib.rs:here}}
```

</Listing>

Dokumentációs kommentekkel némi dokumentációt is adtunk a `ThreadPool`-hoz.
Figyeld meg, hogy a jó dokumentációs gyakorlatot követve felvettünk egy
részt, amely felsorolja, milyen helyzetekben pánikolhat a függvényünk, ahogy
a 14. fejezetben tárgyaltuk. Próbáld ki a `cargo doc --open` parancsot, és
kattints a `ThreadPool` struktúrára, hogy lásd, hogyan néz ki a `new`
generált dokumentációja!

Ahelyett, hogy az `assert!` makrót adnánk hozzá, ahogy itt tettük, a `new`-t
átalakíthatnánk `build`-dé, és visszaadhatnánk egy `Result`-ot, ahogy az I/O
projektben a 12-9. kódrészletben a `Config::build`-del tettük. Ebben az
esetben azonban úgy döntöttünk, hogy egy szálak nélküli szálkészlet
létrehozásának kísérlete helyrehozhatatlan hiba kell, hogy legyen. Ha
nagyratörő kedvedben vagy, próbálj meg írni egy `build` nevű függvényt a
következő szignatúrával, hogy összevesd a `new` függvénnyel:

```rust,ignore
pub fn build(size: usize) -> Result<ThreadPool, PoolCreationError> {
```

#### Hely létrehozása a szálak tárolásához {#creating-space-to-store-the-threads}

Most, hogy már meg tudjuk állapítani, hogy érvényes számú szálat kell a
készletben tárolnunk, létrehozhatjuk ezeket a szálakat, és eltárolhatjuk őket
a `ThreadPool` struktúrában, mielőtt visszaadnánk a struktúrát. De hogyan
lehet egy szálat „eltárolni”? Nézzük meg újra a `thread::spawn`
szignatúráját:

```rust,ignore
pub fn spawn<F, T>(f: F) -> JoinHandle<T>
    where
        F: FnOnce() -> T,
        F: Send + 'static,
        T: Send + 'static,
```

A `spawn` függvény egy `JoinHandle<T>`-t ad vissza, ahol a `T` a closure által
visszaadott típus. Próbáljuk meg mi is a `JoinHandle`-t használni, és nézzük
meg, mi történik. A mi esetünkben a szálkészletnek átadott closure-ök a
kapcsolatot kezelik, és nem adnak vissza semmit, így a `T` a `()` unit típus
lesz.

A 21-14. kódrészlet kódja lefordul, de még nem hoz létre szálakat.
Megváltoztattuk a `ThreadPool` definícióját, hogy `thread::JoinHandle<()>`
példányok vektorát tárolja, a vektort `size` kapacitással inicializáltuk,
létrehoztunk egy `for` ciklust, amely valamilyen kódot futtat majd a szálak
létrehozásához, és visszaadtunk egy ezeket tartalmazó `ThreadPool` példányt.

<Listing number="21-14" file-name="src/lib.rs" caption="Vektor létrehozása a `ThreadPool` számára a szálak tárolásához">

```rust,ignore,not_desired_behavior
{{#rustdoc_include ../listings/ch21-web-server/listing-21-14/src/lib.rs:here}}
```

</Listing>

A könyvtár crate-ben hatókörbe hoztuk a `std::thread`-et, mert a
`thread::JoinHandle`-t használjuk a `ThreadPool` vektorában lévő elemek
típusaként.

Amint érvényes méretet kap, a `ThreadPool` létrehoz egy új vektort, amely
`size` darab elemet tud tárolni. A `with_capacity` függvény ugyanazt a
feladatot látja el, mint a `Vec::new`, egy fontos különbséggel: előre
lefoglalja a helyet a vektorban. Mivel tudjuk, hogy `size` darab elemet kell
tárolnunk a vektorban, ez az előzetes foglalás valamivel hatékonyabb, mint a
`Vec::new` használata, amely az elemek beszúrása során méretezi át magát.

Ha újra lefuttatod a `cargo check` parancsot, sikeresnek kell lennie.

<!-- Old headings. Do not remove or links may break. -->
<a id ="a-worker-struct-responsible-for-sending-code-from-the-threadpool-to-a-thread"></a>

#### Kód küldése a `ThreadPool`-ból egy szálnak {#sending-code-from-the-threadpool-to-a-thread}

A 21-14. kódrészlet `for` ciklusában hagytunk egy kommentet a szálak
létrehozásáról. Most megnézzük, hogyan hozzuk létre ténylegesen a szálakat. A
standard könyvtár a `thread::spawn`-t kínálja a szálak létrehozására, a
`thread::spawn` pedig azt várja, hogy kapjon valamilyen kódot, amelyet a szál
a létrehozása után azonnal futtat. A mi esetünkben azonban azt szeretnénk,
hogy a szálak létrejöjjenek, és _várjanak_ a később elküldött kódra. A
standard könyvtár szálmegvalósítása erre nem kínál semmilyen módot; ezt
kézzel kell megvalósítanunk.

Ezt a viselkedést úgy valósítjuk meg, hogy a `ThreadPool` és a szálak közé
bevezetünk egy új adatszerkezetet, amely ezt az új viselkedést kezeli. Ezt az
adatszerkezetet _Workernek_ nevezzük, ami a készletalapú megvalósításokban
bevett kifejezés. A `Worker` felveszi a futtatandó kódot, és a saját szálában
futtatja.

Gondolj egy étterem konyháján dolgozó emberekre: a dolgozók megvárják, amíg
beérkeznek a vendégek rendelései, majd ők felelnek azért, hogy átvegyék és
elkészítsék ezeket a rendeléseket.

Ahelyett, hogy `JoinHandle<()>` példányok vektorát tárolnánk a
szálkészletben, a `Worker` struktúra példányait tároljuk. Minden `Worker`
egyetlen `JoinHandle<()>` példányt tárol. Ezután a `Worker`-en megvalósítunk
egy metódust, amely átvesz egy futtatandó kódot tartalmazó closure-t, és
elküldi a már futó szálnak végrehajtásra. Minden `Worker`-nek adunk egy
`id`-t is, hogy naplózáskor vagy hibakereséskor meg tudjuk különböztetni a
készletben lévő különböző `Worker` példányokat.

Íme az új folyamat, amely egy `ThreadPool` létrehozásakor lezajlik. A closure-t
a szálnak elküldő kódot azután valósítjuk meg, hogy a `Worker`-t így
beállítottuk:

1. Definiálj egy `id`-t és egy `JoinHandle<()>`-t tároló `Worker` struktúrát.
2. Módosítsd a `ThreadPool`-t úgy, hogy `Worker` példányok vektorát tárolja.
3. Definiálj egy `Worker::new` függvényt, amely egy `id` számot vár, és egy
   olyan `Worker` példányt ad vissza, amely az `id`-t és egy üres closure-rel
   indított szálat tárol.
4. A `ThreadPool::new`-ban a `for` ciklus számlálójával állíts elő egy `id`-t,
   hozz létre ezzel az `id`-vel egy új `Worker`-t, és tárold el a `Worker`-t a
   vektorban.

Ha kedved van egy kis kihíváshoz, próbáld meg magad megvalósítani ezeket a
módosításokat, mielőtt megnéznéd a 21-15. kódrészlet kódját.

Készen állsz? Íme a 21-15. kódrészlet, az előző módosítások elvégzésének egy
lehetséges módjával.

<Listing number="21-15" file-name="src/lib.rs" caption="A `ThreadPool` módosítása úgy, hogy közvetlenül a szálak helyett `Worker` példányokat tároljon">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-15/src/lib.rs:here}}
```

</Listing>

A `ThreadPool` mezőjének nevét `threads`-ről `workers`-re változtattuk, mert
most már `JoinHandle<()>` példányok helyett `Worker` példányokat tárol. A
`for` ciklus számlálóját használjuk a `Worker::new` argumentumaként, és minden
új `Worker`-t a `workers` nevű vektorban tárolunk.

A külső kódnak (például a _src/main.rs_-ben lévő szerverünknek) nem kell
ismernie azokat a megvalósítási részleteket, hogy a `ThreadPool` egy `Worker`
struktúrát használ, ezért a `Worker` struktúrát és a `new` függvényét privátnak
hagyjuk. A `Worker::new` függvény a neki átadott `id`-t használja, és egy
olyan `JoinHandle<()>` példányt tárol, amely egy új szál üres closure-rel való
indításával jön létre.

> Megjegyzés: Ha az operációs rendszer nem tud szálat létrehozni, mert nincs
> elég rendszererőforrás, a `thread::spawn` pánikol. Ez az egész szerverünket
> pánikra készteti, még akkor is, ha néhány szál létrehozása sikerülne. Az
> egyszerűség kedvéért ez a viselkedés megfelelő, de egy éles
> szálkészlet-megvalósításban valószínűleg inkább a
> [`std::thread::Builder`][builder]<!-- ignore --> típust és annak
> [`spawn`][builder-spawn]<!-- ignore --> metódusát használnád, amely
> `Result`-ot ad vissza.

Ez a kód lefordul, és annyi `Worker` példányt tárol, amennyit a
`ThreadPool::new` argumentumaként megadtunk. Az `execute`-ban kapott closure-t
azonban _még mindig_ nem dolgozzuk fel. Nézzük meg most, hogyan tehetjük ezt
meg.

#### Kérések küldése a szálaknak csatornákon keresztül {#sending-requests-to-threads-via-channels}

A következő probléma, amelyet megoldunk, az, hogy a `thread::spawn`-nak átadott
closure-ök semmit sem csinálnak. Jelenleg az `execute` metódusban kapjuk meg
a végrehajtandó closure-t. A `thread::spawn`-nak viszont egy futtatandó
closure-t kell adnunk, amikor a `ThreadPool` létrehozása során létrehozzuk az
egyes `Worker`-eket.

Azt szeretnénk, hogy az imént létrehozott `Worker` struktúrák a `ThreadPool`
által tárolt várakozási sorból vegyék ki a futtatandó kódot, és elküldjék azt
a saját szálukba futtatásra.

A 16. fejezetben megismert csatornák (channels) – amelyek egyszerű módot
adnak két szál közötti kommunikációra – tökéletesek erre a feladatra. Egy
csatornát fogunk a feladatok (jobs) várakozási soraként használni, az
`execute` pedig a `ThreadPool`-ból elküld egy feladatot a `Worker`
példányoknak, amelyek továbbküldik a feladatot a saját száluknak. A terv a
következő:

1. A `ThreadPool` létrehoz egy csatornát, és megtartja a küldő oldalát.
2. Minden `Worker` megtartja a fogadó oldalt.
3. Létrehozunk egy új `Job` struktúrát, amely a csatornán elküldendő
   closure-öket tárolja.
4. Az `execute` metódus a küldő oldalon keresztül elküldi a végrehajtandó
   feladatot.
5. A `Worker` a saját szálában ciklusban olvassa a fogadó oldalt, és
   végrehajtja minden kapott feladat closure-ját.

Kezdjük azzal, hogy a `ThreadPool::new`-ban létrehozunk egy csatornát, és a
küldő oldalt a `ThreadPool` példányban tároljuk, ahogy a 21-16. kódrészlet
mutatja. A `Job` struktúra egyelőre nem tárol semmit, de ez lesz a csatornán
küldött elemek típusa.

<Listing number="21-16" file-name="src/lib.rs" caption="A `ThreadPool` módosítása úgy, hogy egy `Job` példányokat továbbító csatorna küldő oldalát tárolja">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-16/src/lib.rs:here}}
```

</Listing>

A `ThreadPool::new`-ban létrehozzuk az új csatornánkat, és a készlet tárolja
a küldő oldalt. Ez sikeresen lefordul.

Próbáljuk meg átadni a csatorna fogadó oldalát minden `Worker`-nek, amikor a
szálkészlet létrehozza a csatornát. Tudjuk, hogy a fogadó oldalt a `Worker`
példányok által indított szálban szeretnénk használni, ezért a closure-ben a
`receiver` paraméterre hivatkozunk. A 21-17. kódrészlet kódja még nem egészen
fordul le.

<Listing number="21-17" file-name="src/lib.rs" caption="A fogadó oldal átadása minden `Worker`-nek">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch21-web-server/listing-21-17/src/lib.rs:here}}
```

</Listing>

Néhány kisebb, egyszerű módosítást végeztünk: átadjuk a fogadó oldalt a
`Worker::new`-nak, majd a closure-ben használjuk.

Amikor megpróbáljuk ellenőrizni ezt a kódot, a következő hibát kapjuk:

```console
{{#include ../listings/ch21-web-server/listing-21-17/output.txt}}
```

A kód több `Worker` példánynak próbálja átadni a `receiver`-t. Ez nem fog
működni, ahogy a 16. fejezetből emlékezhetsz: a Rust által biztosított
csatornamegvalósítás több _termelős (producer)_, egy _fogyasztós (consumer)_.
Ez azt jelenti, hogy nem klónozhatjuk egyszerűen a csatorna fogyasztó oldalát
a kód kijavításához. Azt sem szeretnénk, hogy egy üzenetet többször, több
fogyasztónak küldjünk el; egyetlen üzenetlistát szeretnénk több `Worker`
példánnyal úgy, hogy minden üzenet egyszer kerüljön feldolgozásra.

Ráadásul egy feladat kivétele a csatorna várakozási sorából a `receiver`
módosításával jár, így a szálaknak biztonságos módra van szükségük a
`receiver` megosztásához és módosításához; különben versenyhelyzetek
alakulhatnak ki (ahogy a 16. fejezetben tárgyaltuk).

Emlékezz vissza a 16. fejezetben tárgyalt szálbiztos okos mutatókra: ahhoz,
hogy a tulajdonjogot több szál között megosszuk, és lehetővé tegyük, hogy a
szálak módosítsák az értéket, az `Arc<Mutex<T>>`-t kell használnunk. Az `Arc`
típus lehetővé teszi, hogy több `Worker` példány birtokolja a fogadó oldalt, a
`Mutex` pedig biztosítja, hogy egyszerre csak egy `Worker` kapjon feladatot a
fogadó oldaltól. A 21-18. kódrészlet mutatja a szükséges módosításokat.

<Listing number="21-18" file-name="src/lib.rs" caption="A fogadó oldal megosztása a `Worker` példányok között az `Arc` és a `Mutex` segítségével">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-18/src/lib.rs:here}}
```

</Listing>

A `ThreadPool::new`-ban a fogadó oldalt egy `Arc`-ba és egy `Mutex`-be
tesszük. Minden új `Worker` számára klónozzuk az `Arc`-ot, hogy megnöveljük a
referenciaszámlálót, így a `Worker` példányok közösen birtokolhatják a fogadó
oldalt.

Ezekkel a módosításokkal a kód lefordul! Haladunk!

#### Az `execute` metódus megvalósítása {#implementing-the-execute-method}

Valósítsuk meg végre a `ThreadPool` `execute` metódusát. A `Job`-ot is
átalakítjuk struktúrából egy trait objektumra vonatkozó típusálnévvé, amely az
`execute` által kapott closure típusát tárolja. Ahogy a 20. fejezet
[„Típusszinonimák és típusálnevek”][type-aliases]<!-- ignore --> részében
tárgyaltuk, a típusálnevek lehetővé teszik, hogy a hosszú típusokat a
könnyebb használat érdekében lerövidítsük. Nézd meg a 21-19. kódrészletet.

<Listing number="21-19" file-name="src/lib.rs" caption="Egy `Job` típusálnév létrehozása egy, az egyes closure-öket tároló `Box` számára, majd a feladat elküldése a csatornán">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-19/src/lib.rs:here}}
```

</Listing>

Miután az `execute`-ban kapott closure-ből létrehoztunk egy új `Job` példányt,
elküldjük ezt a feladatot a csatorna küldő oldalán. A `send`-en meghívjuk az
`unwrap`-ot arra az esetre, ha a küldés meghiúsulna. Ez például akkor
fordulhat elő, ha az összes szálunk végrehajtását leállítjuk, vagyis a fogadó
oldal már nem fogad új üzeneteket. Jelenleg nem tudjuk leállítani a szálaink
végrehajtását: a szálaink addig futnak, amíg a készlet létezik. Azért
használjuk az `unwrap`-ot, mert tudjuk, hogy a hibaeset nem fog bekövetkezni,
de a fordító ezt nem tudja.

De még nem végeztünk egészen! A `Worker`-ben a `thread::spawn`-nak átadott
closure-ünk még mindig csak _hivatkozik_ a csatorna fogadó oldalára. Ehelyett
arra van szükségünk, hogy a closure a végtelenségig ciklusban fusson,
feladatot kérjen a csatorna fogadó oldalától, és ha kap egyet, lefuttassa. A
21-20. kódrészletben látható módon módosítsuk a `Worker::new`-t.

<Listing number="21-20" file-name="src/lib.rs" caption="A feladatok fogadása és végrehajtása a `Worker` példány szálában">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-20/src/lib.rs:here}}
```

</Listing>

Itt először meghívjuk a `lock`-ot a `receiver`-en, hogy megszerezzük a
mutexet, majd meghívjuk az `unwrap`-ot, hogy hiba esetén pánikoljunk. A zár
(lock) megszerzése meghiúsulhat, ha a mutex _mérgezett (poisoned)_
állapotban van; ez akkor fordulhat elő, ha egy másik szál pánikolt, miközben
a zárat tartotta, ahelyett hogy elengedte volna. Ebben a helyzetben a helyes
lépés az `unwrap` meghívása, hogy ez a szál is pánikoljon. Nyugodtan
cseréld le ezt az `unwrap`-ot egy olyan `expect`-re, amelynek a hibaüzenete
számodra beszédes.

Ha megkapjuk a zárat a mutexen, meghívjuk a `recv`-et, hogy egy `Job`-ot
fogadjunk a csatornáról. Egy utolsó `unwrap` itt is átlép minden hibán; hiba
akkor fordulhat elő, ha a küldő oldalt tartó szál leállt, hasonlóan ahhoz,
ahogy a `send` metódus is `Err`-t ad vissza, ha a fogadó oldal leáll.

A `recv` hívás blokkol, így ha még nincs feladat, az aktuális szál addig vár,
amíg egy feladat elérhetővé nem válik. A `Mutex<T>` biztosítja, hogy egyszerre
csak egy `Worker` szál próbáljon feladatot kérni.

A szálkészletünk most már működőképes! Futtasd a `cargo run` paranccsal, és
küldj néhány kérést:

<!-- manual-regeneration
cd listings/ch21-web-server/listing-21-20
cargo run
make some requests to 127.0.0.1:7878
Can't automate because the output depends on making requests
-->

```console
$ cargo run
   Compiling hello v0.1.0 (file:///projects/hello)
warning: field `workers` is never read
 --> src/lib.rs:7:5
  |
6 | pub struct ThreadPool {
  |            ---------- field in this struct
7 |     workers: Vec<Worker>,
  |     ^^^^^^^
  |
  = note: `#[warn(dead_code)]` on by default

warning: fields `id` and `thread` are never read
  --> src/lib.rs:48:5
   |
47 | struct Worker {
   |        ------ fields in this struct
48 |     id: usize,
   |     ^^
49 |     thread: thread::JoinHandle<()>,
   |     ^^^^^^

warning: `hello` (lib) generated 2 warnings
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 4.91s
     Running `target/debug/hello`
Worker 0 got a job; executing.
Worker 2 got a job; executing.
Worker 1 got a job; executing.
Worker 3 got a job; executing.
Worker 0 got a job; executing.
Worker 2 got a job; executing.
Worker 1 got a job; executing.
Worker 3 got a job; executing.
Worker 0 got a job; executing.
Worker 2 got a job; executing.
```

Siker! Most már van egy szálkészletünk, amely aszinkron módon hajtja végre a
kapcsolatokat. Soha nem jön létre négynél több szál, így a rendszerünk nem
terhelődik túl, ha a szerver sok kérést kap. Ha kérést küldünk a _/sleep_
címre, a szerver a többi kérést úgy tudja kiszolgálni, hogy egy másik szál
futtatja őket.

> Megjegyzés: Ha a _/sleep_ címet egyszerre több böngészőablakban nyitod meg,
> előfordulhat, hogy egyenként, ötmásodperces időközönként töltődnek be.
> Egyes webböngészők gyorsítótárazási okokból ugyanannak a kérésnek a több
> példányát egymás után hajtják végre. Ezt a korlátozást nem a webszerverünk
> okozza.

Most érdemes megállni, és végiggondolni, miben különbözne a 21-18., 21-19. és
21-20. kódrészlet kódja, ha az elvégzendő munkához closure helyett
future-öket használnánk. Mely típusok változnának meg? Különböznének-e a
metódusszignatúrák, és ha igen, hogyan? A kód mely részei maradnának
változatlanok?

Miután a 17. és a 19. fejezetben megismerted a `while let` ciklust, talán
felmerül benned a kérdés, miért nem a 21-21. kódrészletben látható módon
írtuk meg a `Worker` szál kódját.

<Listing number="21-21" file-name="src/lib.rs" caption="A `Worker::new` egy alternatív megvalósítása a `while let` használatával">

```rust,ignore,not_desired_behavior
{{#rustdoc_include ../listings/ch21-web-server/listing-21-21/src/lib.rs:here}}
```

</Listing>

Ez a kód lefordul és fut, de nem eredményezi a kívánt többszálú viselkedést:
egy lassú kérés továbbra is arra kényszeríti a többi kérést, hogy várjanak a
feldolgozásukra. Az ok meglehetősen finom: a `Mutex` struktúrának nincs
nyilvános `unlock` metódusa, mert a zár tulajdonjoga a `lock` metódus által
visszaadott `LockResult<MutexGuard<T>>`-ben lévő `MutexGuard<T>`
élettartamán alapul. Fordítási időben a kölcsönzésellenőrző így ki tudja
kényszeríteni azt a szabályt, hogy egy `Mutex` által őrzött erőforráshoz csak
akkor férhetünk hozzá, ha a zárat birtokoljuk. Ez a megvalósítás azonban azt
is eredményezheti, hogy a zárat a szándékoltnál tovább tartjuk, ha nem
figyelünk oda a `MutexGuard<T>` élettartamára.

A 21-20. kódrészlet kódja, amely a `let job =
receiver.lock().unwrap().recv().unwrap();` sort használja, azért működik, mert
a `let` esetén az egyenlőségjel jobb oldalán álló kifejezésben használt
ideiglenes értékek a `let` utasítás végén azonnal eldobódnak. A `while let`
(valamint az `if let` és a `match`) viszont csak a hozzá tartozó blokk végén
dobja el az ideiglenes értékeket. A 21-21. kódrészletben a zár a `job()`
hívás teljes időtartama alatt megmarad, vagyis a többi `Worker` példány nem
kaphat feladatokat.

[type-aliases]: ch20-03-advanced-types.html#type-synonyms-and-type-aliases
[integer-types]: ch03-02-data-types.html#integer-types
[moving-out-of-closures]: ch13-01-closures.html#moving-captured-values-out-of-closures
[builder]: ../std/thread/struct.Builder.html
[builder-spawn]: ../std/thread/struct.Builder.html#method.spawn
