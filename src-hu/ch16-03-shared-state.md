## Megosztott állapotú konkurencia {#shared-state-concurrency}

Az üzenetküldés jó módja a konkurencia kezelésének, de nem az egyetlen. Egy
másik módszer az, hogy több szál fér hozzá ugyanahhoz a megosztott adathoz.
Gondolj ismét a Go nyelv dokumentációjából idézett jelmondat erre a részére:
„Ne a memória megosztásával kommunikálj.”

Hogyan nézne ki a memória megosztásával történő kommunikáció? Továbbá miért
óvnak az üzenetküldés hívei a memória megosztásától?

Bizonyos értelemben bármely programozási nyelvben a csatornák az egyszeres
tulajdonjoghoz hasonlítanak, mert miután egy értéket átadtál egy csatornán,
többé nem szabad használnod. A megosztott memóriás konkurencia a többszörös
tulajdonjoghoz hasonlít: több szál is hozzáférhet ugyanahhoz a memóriahelyhez
egy időben. Ahogy a 15. fejezetben láttad, ahol az okos mutatók tették
lehetővé a többszörös tulajdonjogot, a többszörös tulajdonjog bonyolultabbá
teheti a dolgokat, mert ezeket a különböző tulajdonosokat kezelni kell. A Rust
típusrendszere és tulajdonjogi szabályai sokat segítenek abban, hogy ez a
kezelés helyes legyen. Példaként nézzük meg a mutexeket, a megosztott memória
egyik gyakoribb konkurenciaprimitívjét.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-mutexes-to-allow-access-to-data-from-one-thread-at-a-time"></a>

### A hozzáférés szabályozása mutexekkel {#controlling-access-with-mutexes}

A _mutex_ a _mutual exclusion_, azaz _kölcsönös kizárás_ rövidítése: egy
mutex egyszerre csak egy szálnak engedi meg, hogy hozzáférjen bizonyos
adatokhoz. Ahhoz, hogy egy szál hozzáférjen a mutexben lévő adatokhoz,
először jeleznie kell, hogy hozzáférést szeretne, azaz kérnie kell a mutex
zárjának megszerzését. A _zár (lock)_ a mutex részét képező adatszerkezet,
amely nyilvántartja, hogy éppen kinek van kizárólagos hozzáférése az
adatokhoz. Ezért mondjuk, hogy a mutex a zárolási rendszeren keresztül
_őrzi (guarding)_ a benne tárolt adatokat.

A mutexek arról híresek, hogy nehéz őket használni, mert két szabályt kell
észben tartanod:

1. Az adatok használata előtt meg kell próbálnod megszerezni a zárat.
2. Amikor végeztél a mutex által őrzött adatokkal, fel kell oldanod az adatok
   zárolását, hogy más szálak is megszerezhessék a zárat.

A mutex valós életbeli megfelelőjeként képzelj el egy konferencián tartott
kerekasztal-beszélgetést, ahol csak egy mikrofon van. Mielőtt egy résztvevő
megszólalhatna, kérnie vagy jeleznie kell, hogy használni szeretné a
mikrofont. Amikor megkapja a mikrofont, addig beszélhet, ameddig csak akar,
majd átadja a mikrofont a következő résztvevőnek, aki szólni kíván. Ha egy
résztvevő elfelejti átadni a mikrofont, amikor végzett, senki más nem tud
megszólalni. Ha a közös mikrofon kezelése félresiklik, a beszélgetés nem a
tervek szerint zajlik!

A mutexek helyes kezelése hihetetlenül bonyolult lehet, ezért lelkesednek
annyian a csatornákért. A Rust típusrendszerének és tulajdonjogi
szabályainak köszönhetően azonban a zárolást és a feloldást nem ronthatod el.

#### A `Mutex<T>` API-ja {#the-api-of-mutext}

A mutex használatának bemutatására kezdjük azzal, hogy egy mutexet egyszálú
környezetben használunk, ahogy a 16-12. kódrészlet mutatja.

<Listing number="16-12" file-name="src/main.rs" caption="A `Mutex<T>` API-jának felfedezése az egyszerűség kedvéért egyszálú környezetben">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-12/src/main.rs}}
```

</Listing>

Sok más típushoz hasonlóan a `Mutex<T>` értéket a `new` társított
függvénnyel hozzuk létre. A mutexben lévő adatok eléréséhez a `lock`
metódussal megszerezzük a zárat. Ez a hívás blokkolja az aktuális szálat, így
az nem végezhet semmilyen munkát, amíg nem mi következünk a zár
birtoklásában.

A `lock` hívása meghiúsulna, ha egy másik, a zárat birtokló szál pánikolt
volna. Ebben az esetben soha senki nem tudná megszerezni a zárat, ezért úgy
döntöttünk, hogy az `unwrap` metódust hívjuk, és ebben a helyzetben ez a szál
is pánikoljon.

Miután megszereztük a zárat, a visszatérési értéket – amelynek ebben az
esetben `num` a neve – a benne lévő adatra mutató módosítható referenciaként
kezelhetjük. A típusrendszer biztosítja, hogy megszerezzük a zárat, mielőtt
az `m`-ben lévő értéket használnánk. Az `m` típusa `Mutex<i32>`, nem pedig
`i32`, ezért _muszáj_ meghívnunk a `lock` metódust ahhoz, hogy az `i32`
értéket használhassuk. Nem felejthetjük el; a típusrendszer máskülönben nem
engedi, hogy hozzáférjünk a belső `i32` értékhez.

A `lock` hívása egy `MutexGuard` nevű típust ad vissza egy `LockResult`-ba
csomagolva, amelyet az `unwrap` hívásával kezeltünk. A `MutexGuard` típus
megvalósítja a `Deref` traitet, hogy a belső adatainkra mutasson; a típusnak
van egy `Drop`-megvalósítása is, amely automatikusan feloldja a zárat, amikor
egy `MutexGuard` kikerül a hatókörből, ami a belső hatókör végén történik
meg. Így nem fenyeget az a veszély, hogy elfelejtjük feloldani a zárat, és
ezzel megakadályozzuk, hogy más szálak használják a mutexet, mert a zár
feloldása automatikusan megtörténik.

Miután eldobtuk a zárat, kiírhatjuk a mutex értékét, és láthatjuk, hogy
sikerült a belső `i32` értéket `6`-ra módosítanunk.

<!-- Old headings. Do not remove or links may break. -->

<a id="sharing-a-mutext-between-multiple-threads"></a>

#### Közös hozzáférés a `Mutex<T>` értékhez {#shared-access-to-mutext}

Most próbáljunk meg egy értéket több szál között megosztani a `Mutex<T>`
segítségével. Elindítunk 10 szálat, és mindegyikkel 1-gyel növeltetünk egy
számlálót, így a számláló 0-ról 10-re nő. A 16-13. kódrészlet példája
fordítási hibát fog adni, és ezt a hibát arra használjuk, hogy többet
megtudjunk a `Mutex<T>` használatáról, és arról, hogyan segít a Rust a
helyes használatában.

<Listing number="16-13" file-name="src/main.rs" caption="Tíz szál, amelyek mindegyike növel egy `Mutex<T>` által őrzött számlálót">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-13/src/main.rs}}
```

</Listing>

Létrehozunk egy `counter` változót, amely egy `Mutex<T>`-ben tárol egy `i32`
értéket, ahogy a 16-12. kódrészletben is tettük. Ezután egy számtartományon
végigiterálva 10 szálat hozunk létre. A `thread::spawn` függvényt használjuk,
és minden szálnak ugyanazt a closure-t adjuk: egy olyat, amely a számlálót a
szálba mozgatja, a `lock` metódus meghívásával megszerzi a `Mutex<T>`
zárját, majd 1-et ad a mutexben lévő értékhez. Amikor egy szál befejezi a
closure-je futtatását, a `num` kikerül a hatókörből, és feloldja a zárat,
hogy egy másik szál megszerezhesse.

A fő szálban összegyűjtjük az összes join-leírót (join handle). Ezután,
ahogy a 16-2. kódrészletben is tettük, mindegyik leírón meghívjuk a `join`
metódust, hogy biztosan befejeződjön az összes szál. Ekkor a fő szál
megszerzi a zárat, és kiírja a program eredményét.

Utaltunk rá, hogy ez a példa nem fordul le. Most nézzük meg, miért!

```console
{{#include ../listings/ch16-fearless-concurrency/listing-16-13/output.txt}}
```

A hibaüzenet szerint a `counter` értéket a ciklus előző iterációjában már
átmozgattuk. A Rust azt közli velünk, hogy a `counter` zár tulajdonjogát nem
mozgathatjuk át több szálba. Javítsuk ki a fordítási hibát a 15. fejezetben
tárgyalt többszörös tulajdonjogi módszerrel.

#### Többszörös tulajdonjog több szállal {#multiple-ownership-with-multiple-threads}

A 15. fejezetben úgy adtunk egy értéknek több tulajdonost, hogy az `Rc<T>`
okos mutatóval létrehoztunk egy referenciaszámlált értéket. Tegyük meg itt is
ugyanezt, és nézzük meg, mi történik. A 16-14. kódrészletben a `Mutex<T>`
értéket egy `Rc<T>`-be csomagoljuk, és az `Rc<T>`-t klónozzuk, mielőtt a
tulajdonjogot átmozgatnánk a szálba.

<Listing number="16-14" file-name="src/main.rs" caption="Kísérlet az `Rc<T>` használatára, hogy több szál is birtokolhassa a `Mutex<T>` értéket">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-14/src/main.rs}}
```

</Listing>

Ismét lefordítjuk, és… más hibákat kapunk! A fordító sokat tanít nekünk:

```console
{{#include ../listings/ch16-fearless-concurrency/listing-16-14/output.txt}}
```

Hűha, ez a hibaüzenet nagyon bőbeszédű! Itt van a fontos rész, amelyre
figyelnünk kell: `` `Rc<Mutex<i32>>` cannot be sent between threads safely ``.
A fordító azt is megmondja, mi ennek az oka: `` the trait `Send` is not
implemented for `Rc<Mutex<i32>>` ``. A `Send` traitről a következő részben
beszélünk: ez az egyik olyan trait, amely biztosítja, hogy a szálakkal
használt típusaink konkurens helyzetekben való használatra készültek.

Sajnos az `Rc<T>` nem osztható meg biztonságosan a szálak között. Amikor az
`Rc<T>` kezeli a referenciaszámlálót, minden `clone` hívásnál növeli a
számlálót, és minden klón eldobásakor csökkenti. Nem használ azonban
semmilyen konkurenciaprimitívet annak biztosítására, hogy a számláló
módosításait ne szakíthassa meg egy másik szál. Ez hibás számlálóértékekhez
vezethet – olyan rejtett hibákhoz, amelyek pedig memóriaszivárgáshoz vagy
ahhoz vezethetnek, hogy egy értéket eldobunk, mielőtt végeztünk volna vele.
Olyan típusra van szükségünk, amely pontosan olyan, mint az `Rc<T>`, de a
referenciaszámlálót szálbiztos módon módosítja.

#### Atomi referenciaszámlálás az `Arc<T>` segítségével {#atomic-reference-counting-with-arct}

Szerencsére az `Arc<T>` _valóban_ az `Rc<T>`-hez hasonló típus, amelyet
biztonságosan használhatunk konkurens helyzetekben. Az _a_ az _atomic_
(atomi) szót jelöli, vagyis ez egy _atomi referenciaszámlálású (atomically
reference-counted)_ típus. Az atomi típusok a konkurenciaprimitívek egy
további fajtáját alkotják, amelyekkel itt nem foglalkozunk részletesen:
további részletekért lásd a standard könyvtár
[`std::sync::atomic`][atomic]<!-- ignore --> dokumentációját. Egyelőre elég
annyit tudnod, hogy az atomi típusok úgy működnek, mint a primitív típusok,
de biztonságosan megoszthatók a szálak között.

Felmerülhet benned a kérdés, hogy miért nem atomi az összes primitív típus,
és miért nem az `Arc<T>` használatára épülnek alapértelmezésben a standard
könyvtár típusai. Ennek az az oka, hogy a szálbiztonságnak
teljesítménybeli ára van, amelyet csak akkor érdemes megfizetni, ha tényleg
szükség van rá. Ha csak egyetlen szálon belül végzel műveleteket
értékeken, a kódod gyorsabban futhat, ha nem kell kikényszerítenie az atomi
típusok által nyújtott garanciákat.

Térjünk vissza a példánkhoz: az `Arc<T>` és az `Rc<T>` API-ja megegyezik,
így a programunkat úgy javítjuk ki, hogy módosítjuk a `use` sort, a `new`
hívását és a `clone` hívását. A 16-15. kódrészlet kódja végre lefordul és
lefut.

<Listing number="16-15" file-name="src/main.rs" caption="A `Mutex<T>` becsomagolása egy `Arc<T>`-be, hogy a tulajdonjogot több szál között is megoszthassuk">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-15/src/main.rs}}
```

</Listing>

Ez a kód a következőt írja ki:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
Result: 10
```

Sikerült! 0-tól 10-ig számoltunk, ami talán nem tűnik túl lenyűgözőnek, de
sokat tanultunk belőle a `Mutex<T>` típusról és a szálbiztonságról. Ennek a
programnak a szerkezetét bonyolultabb műveletekre is használhatod, mint egy
számláló növelése. Ezzel a stratégiával egy számítást független részekre
oszthatsz, ezeket a részeket szétoszthatod a szálak között, majd egy
`Mutex<T>` segítségével minden szál a saját részével frissítheti a végső
eredményt.

Ha egyszerű numerikus műveleteket végzel, vedd figyelembe, hogy a
[standard könyvtár `std::sync::atomic` modulja][atomic]<!-- ignore --> a
`Mutex<T>` típusoknál egyszerűbb típusokat is kínál. Ezek a típusok
biztonságos, konkurens, atomi hozzáférést biztosítanak a primitív típusokhoz.
Ebben a példában azért választottuk a `Mutex<T>` használatát egy primitív
típussal, hogy arra összpontosíthassunk, hogyan működik a `Mutex<T>`.

<!-- Old headings. Do not remove or links may break. -->

<a id="similarities-between-refcelltrct-and-mutextarct"></a>

### A `RefCell<T>`/`Rc<T>` és a `Mutex<T>`/`Arc<T>` összehasonlítása {#comparing-refcelltrct-and-mutextarct}

Talán feltűnt, hogy a `counter` nem módosítható, mégis kaphattunk egy
módosítható referenciát a benne lévő értékre; ez azt jelenti, hogy a
`Mutex<T>` belső módosíthatóságot biztosít, ahogy a `Cell` család is. Ahogy
a 15. fejezetben a `RefCell<T>` segítségével módosítottuk egy `Rc<T>`
tartalmát, ugyanúgy a `Mutex<T>` segítségével módosítjuk egy `Arc<T>`
tartalmát.

Egy másik figyelemre méltó részlet, hogy a Rust nem tud megvédeni a logikai
hibák minden fajtájától, amikor a `Mutex<T>` típust használod. Emlékezz a
15. fejezetből, hogy az `Rc<T>` használata magában hordozta a
referenciaciklusok létrehozásának kockázatát, amikor két `Rc<T>` érték
egymásra hivatkozik, és ez memóriaszivárgást okoz. Hasonlóképpen a `Mutex<T>`
a _holtpontok (deadlocks)_ létrehozásának kockázatával jár. Ezek akkor
fordulnak elő, amikor egy műveletnek két erőforrást kell zárolnia, és két
szál mindegyike megszerezte az egyik zárat, ami miatt örökké egymásra
várnak. Ha érdekelnek a holtpontok, próbálj meg írni egy Rust-programot,
amelyben holtpont alakul ki; aztán nézz utána, milyen stratégiák léteznek a
mutexek holtpontjainak elkerülésére bármely nyelvben, és próbáld meg
megvalósítani őket Rustban. A standard könyvtár `Mutex<T>` és `MutexGuard`
típusának API-dokumentációja hasznos információkat tartalmaz.

A fejezetet a `Send` és a `Sync` trait tárgyalásával zárjuk, és azzal, hogyan
használhatjuk őket saját típusokkal.

[atomic]: ../std/sync/atomic/index.html
