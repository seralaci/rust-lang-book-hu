<!-- Old headings. Do not remove or links may break. -->

<a id="extensible-concurrency-with-the-sync-and-send-traits"></a>
<a id="extensible-concurrency-with-the-send-and-sync-traits"></a>

## Bővíthető konkurencia a `Send` és a `Sync` traittel {#extensible-concurrency-with-send-and-sync}

Érdekes módon szinte minden konkurenciával kapcsolatos funkció, amelyről eddig
ebben a fejezetben beszéltünk, a standard könyvtár része volt, nem a nyelvé.
A konkurencia kezelésére szolgáló lehetőségeid nem korlátozódnak a nyelvre
vagy a standard könyvtárra; írhatsz saját konkurenciafunkciókat, vagy
használhatod mások által írtakat is.

A legfontosabb konkurenciafogalmak közül azonban, amelyek nem a standard
könyvtárba, hanem magába a nyelvbe vannak beépítve, ott van a két
`std::marker` trait, a `Send` és a `Sync`.

<!-- Old headings. Do not remove or links may break. -->

<a id="allowing-transference-of-ownership-between-threads-with-send"></a>

### Tulajdonjog átadása szálak között {#transferring-ownership-between-threads}

A `Send` _jelölő trait (marker trait)_ azt jelzi, hogy a `Send` traitet
megvalósító típus értékeinek tulajdonjoga átadható a szálak között. Szinte
minden Rust-típus megvalósítja a `Send` traitet, de van néhány kivétel,
köztük az `Rc<T>`: ez nem valósíthatja meg a `Send` traitet, mert ha
klónoznál egy `Rc<T>` értéket, és a klón tulajdonjogát megpróbálnád átadni
egy másik szálnak, akkor mindkét szál egyszerre módosíthatná a
referenciaszámlálót. Emiatt az `Rc<T>` egyszálú helyzetekben való
használatra készült, ahol nem szeretnéd megfizetni a szálbiztonság
teljesítménybeli árát.

Így a Rust típusrendszere és trait-korlátai biztosítják, hogy soha ne
küldhess véletlenül, nem biztonságos módon egy `Rc<T>` értéket a szálak
között. Amikor ezzel próbálkoztunk a 16-14. kódrészletben, a `` the trait
`Send` is not implemented for `Rc<Mutex<i32>>` `` hibát kaptuk. Amikor
átváltottunk az `Arc<T>` típusra, amely megvalósítja a `Send` traitet, a kód
lefordult.

Minden olyan típus, amely kizárólag `Send` típusokból áll, automatikusan
szintén `Send`-ként jelölődik meg. Szinte minden primitív típus `Send`, a
nyers mutatók (raw pointers) kivételével, amelyekről a 20. fejezetben lesz
szó.

<!-- Old headings. Do not remove or links may break. -->

<a id="allowing-access-from-multiple-threads-with-sync"></a>

### Hozzáférés több szálból {#accessing-from-multiple-threads}

A `Sync` jelölő trait azt jelzi, hogy a `Sync` traitet megvalósító típusra
biztonságosan lehet hivatkozni több szálból. Más szóval bármely `T` típus
akkor valósítja meg a `Sync` traitet, ha a `&T` (egy `T`-re mutató nem
módosítható referencia) megvalósítja a `Send` traitet, vagyis a referencia
biztonságosan elküldhető egy másik szálnak. A `Send`-hez hasonlóan minden
primitív típus megvalósítja a `Sync` traitet, és a kizárólag `Sync` traitet
megvalósító típusokból álló típusok is megvalósítják a `Sync` traitet.

Az `Rc<T>` okos mutató ugyanazok miatt az okok miatt nem valósítja meg a
`Sync` traitet, amelyek miatt a `Send` traitet sem. A `RefCell<T>` típus
(amelyről a 15. fejezetben beszéltünk) és a rokon `Cell<T>` típusok családja
sem valósítja meg a `Sync` traitet. A kölcsönzésellenőrzés, amelyet a
`RefCell<T>` futásidőben végez, nem szálbiztos módon van megvalósítva. A
`Mutex<T>` okos mutató megvalósítja a `Sync` traitet, és használható arra,
hogy több szál között megosszuk a hozzáférést, ahogy azt a [„Közös
hozzáférés a `Mutex<T>` értékhez”][shared-access]<!-- ignore --> részben
láttad.

### A `Send` és a `Sync` kézi megvalósítása nem biztonságos {#implementing-send-and-sync-manually-is-unsafe}

Mivel azok a típusok, amelyek kizárólag a `Send` és a `Sync` traitet
megvalósító más típusokból állnak, automatikusan maguk is megvalósítják a
`Send` és a `Sync` traitet, ezeket a traiteket nem kell kézzel
megvalósítanunk. Jelölő traitekként még megvalósítandó metódusaik sincsenek.
Csupán arra jók, hogy a konkurenciával kapcsolatos invariánsokat
kikényszerítsék.

Ezeknek a traiteknek a kézi megvalósítása unsafe Rust-kód írásával jár. Az
unsafe Rust-kód használatáról a 20. fejezetben beszélünk; egyelőre az a
fontos, hogy olyan új konkurens típusok készítése, amelyek nem `Send` és
`Sync` részekből állnak, alapos átgondolást igényel a biztonsági garanciák
fenntartásához. A [„The Rustonomicon”][nomicon] további információkat
tartalmaz ezekről a garanciákról és fenntartásuk módjáról.

## Összefoglalás {#summary}

Nem most találkozol utoljára a konkurenciával ebben a könyvben: a következő
fejezet az aszinkron programozásra összpontosít, a 21. fejezet projektje pedig
az itt tárgyalt kisebb példáknál valósághűbb helyzetben használja majd ennek a
fejezetnek a fogalmait.

Ahogy korábban említettük, mivel a Rust konkurenciakezelésének csak nagyon
kis része tartozik magához a nyelvhez, sok konkurenciamegoldás crate-ként
van megvalósítva. Ezek gyorsabban fejlődnek, mint a standard könyvtár, ezért
mindenképp keress rá az interneten az aktuális, korszerű crate-ekre,
amelyeket többszálú helyzetekben használhatsz.

A Rust standard könyvtára csatornákat biztosít az üzenetküldéshez, valamint
olyan okosmutató-típusokat, mint a `Mutex<T>` és az `Arc<T>`, amelyek
biztonságosan használhatók konkurens környezetben. A típusrendszer és a
kölcsönzésellenőrző biztosítja, hogy az ezeket a megoldásokat használó
kódban ne alakuljanak ki adatversenyek vagy érvénytelen referenciák. Ha
egyszer sikerül lefordítanod a kódodat, nyugodt lehetsz, hogy vidáman fut
majd több szálon, azok nélkül a nehezen felderíthető hibák nélkül, amelyek
más nyelvekben gyakoriak. A konkurens programozás többé nem olyan fogalom,
amelytől félni kellene: vágj bele, és tedd a programjaidat konkurenssé,
félelem nélkül!

[shared-access]: ch16-03-shared-state.html#shared-access-to-mutext
[nomicon]: https://doc.rust-lang.org/nomicon/index.html
