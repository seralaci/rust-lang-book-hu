## A `RefCell<T>` és a belső módosíthatóság mintája {#refcellt-and-the-interior-mutability-pattern}

A _belső módosíthatóság (interior mutability)_ a Rust egy tervezési mintája,
amely lehetővé teszi, hogy akkor is módosíts adatokat, amikor nem módosítható
referenciák mutatnak rájuk; ezt a kölcsönzési szabályok általában nem
engedik meg. Az adatok módosításához a minta egy adatszerkezeten belül `unsafe`
kódot használ, hogy kijátssza a Rust módosítást és kölcsönzést szabályozó
szokásos szabályait. Az unsafe kód azt jelzi a fordítónak, hogy a szabályokat
kézzel ellenőrizzük, ahelyett hogy a fordítóra hagynánk az ellenőrzést; az
unsafe kódról a 20. fejezetben lesz bővebben szó.

A belső módosíthatóság mintáját követő típusokat csak akkor használhatjuk, ha
biztosítani tudjuk, hogy a kölcsönzési szabályok futásidőben teljesülni
fognak, még ha a fordító ezt nem is tudja garantálni. Az érintett `unsafe` kód
ekkor egy biztonságos API-ba van burkolva, és a külső típus továbbra is nem
módosítható.

Ismerkedjünk meg ezzel a fogalommal a belső módosíthatóság mintáját követő
`RefCell<T>` típuson keresztül.

<!-- Old headings. Do not remove or links may break. -->

<a id="enforcing-borrowing-rules-at-runtime-with-refcellt"></a>

### A kölcsönzési szabályok kikényszerítése futásidőben {#enforcing-borrowing-rules-at-runtime}

Az `Rc<T>`-vel ellentétben a `RefCell<T>` típus egyetlen tulajdonost jelent az
általa tárolt adat felett. Mi különbözteti meg akkor a `RefCell<T>`-t egy
olyan típustól, mint a `Box<T>`? Idézd fel a 4. fejezetben tanult kölcsönzési
szabályokat:

- Egy adott pillanatban _vagy_ egyetlen módosítható referenciád lehet, _vagy_
  tetszőleges számú nem módosítható referenciád (de a kettő egyszerre nem).
- A referenciáknak mindig érvényesnek kell lenniük.

Referenciák és a `Box<T>` esetén a kölcsönzési szabályok invariánsait a fordító
fordítási időben kényszeríti ki. A `RefCell<T>` esetén ezek az invariánsok
_futásidőben_ érvényesülnek. Ha referenciák esetén megszeged ezeket a
szabályokat, fordítási hibát kapsz. Ha a `RefCell<T>` esetén szeged meg őket, a
programod pánikol és kilép.

A kölcsönzési szabályok fordítási idejű ellenőrzésének előnye, hogy a hibák a
fejlesztési folyamat korábbi szakaszában derülnek ki, és nincs hatása a
futásidejű teljesítményre, mert minden elemzés előre lezajlik. Ezen okokból a
legtöbb esetben a kölcsönzési szabályok fordítási idejű ellenőrzése a legjobb
választás, és ezért ez a Rust alapértelmezése.

A kölcsönzési szabályok futásidejű ellenőrzésének előnye viszont az, hogy így
bizonyos memóriabiztos forgatókönyvek is megengedetté válnak, amelyeket a
fordítási idejű ellenőrzések tiltanának. A statikus elemzés – mint amilyet a
Rust fordítója is végez – eredendően konzervatív. A kód bizonyos tulajdonságait
lehetetlen a kód elemzésével felismerni: a leghíresebb példa erre a megállási
probléma (Halting Problem), amely túlmutat e könyv keretein, de érdekes téma,
érdemes utánanézni.

Mivel bizonyos elemzések lehetetlenek, ha a Rust fordítója nem lehet biztos
abban, hogy a kód megfelel a tulajdonjogi szabályoknak, akkor egy helyes
programot is elutasíthat; ebben az értelemben konzervatív. Ha a Rust elfogadna
egy helytelen programot, a felhasználók nem bízhatnának a Rust által nyújtott
garanciákban. Ha viszont a Rust elutasít egy helyes programot, az a
programozónak kényelmetlen, de semmi katasztrofális nem történhet. A
`RefCell<T>` típus akkor hasznos, ha biztos vagy benne, hogy a kódod betartja a
kölcsönzési szabályokat, de a fordító ezt nem képes megérteni és garantálni.

Az `Rc<T>`-hez hasonlóan a `RefCell<T>` is csak egyszálú környezetben
használható, és fordítási hibát kapsz, ha többszálú környezetben próbálod
használni. Arról, hogyan érhető el a `RefCell<T>` funkcionalitása többszálú
programban, a 16. fejezetben lesz szó.

Íme összefoglalva, mikor érdemes a `Box<T>`-t, az `Rc<T>`-t vagy a
`RefCell<T>`-t választani:

- Az `Rc<T>` lehetővé teszi, hogy ugyanannak az adatnak több tulajdonosa
  legyen; a `Box<T>`-nek és a `RefCell<T>`-nek egyetlen tulajdonosa van.
- A `Box<T>` fordítási időben ellenőrzött nem módosítható vagy módosítható
  kölcsönzéseket enged meg; az `Rc<T>` csak fordítási időben ellenőrzött nem
  módosítható kölcsönzéseket enged meg; a `RefCell<T>` futásidőben ellenőrzött
  nem módosítható vagy módosítható kölcsönzéseket enged meg.
- Mivel a `RefCell<T>` futásidőben ellenőrzött módosítható kölcsönzéseket
  enged meg, a `RefCell<T>`-n belüli értéket akkor is módosíthatod, ha maga a
  `RefCell<T>` nem módosítható.

Egy nem módosítható értéken belüli érték módosítása a belső módosíthatóság
mintája. Nézzünk meg egy olyan helyzetet, amelyben a belső módosíthatóság
hasznos, és vizsgáljuk meg, hogyan lehetséges.

<!-- Old headings. Do not remove or links may break. -->

<a id="interior-mutability-a-mutable-borrow-to-an-immutable-value"></a>

### A belső módosíthatóság használata {#using-interior-mutability}

A kölcsönzési szabályok egyik következménye, hogy egy nem módosítható értéket
nem kölcsönözhetsz módosíthatóként. Például ez a kód nem fordul le:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/no-listing-01-cant-borrow-immutable-as-mutable/src/main.rs}}
```

Ha megpróbálnád lefordítani ezt a kódot, a következő hibát kapnád:

```console
{{#include ../listings/ch15-smart-pointers/no-listing-01-cant-borrow-immutable-as-mutable/output.txt}}
```

Vannak azonban olyan helyzetek, amikor hasznos lenne, ha egy érték a saját
metódusaiban módosíthatná önmagát, a többi kód számára viszont nem
módosíthatónak tűnne. Az érték metódusain kívüli kód nem tudná módosítani az
értéket. A `RefCell<T>` használata az egyik módja annak, hogy belső
módosíthatóságot érjünk el, de a `RefCell<T>` nem kerüli meg teljesen a
kölcsönzési szabályokat: a fordító kölcsönzésellenőrzője megengedi ezt a belső
módosíthatóságot, a kölcsönzési szabályok ellenőrzése pedig ehelyett
futásidőben történik. Ha megszeged a szabályokat, fordítási hiba helyett
`panic!`-ot kapsz.

Dolgozzunk végig egy gyakorlati példát, amelyben a `RefCell<T>` segítségével
módosítunk egy nem módosítható értéket, és nézzük meg, miért hasznos ez.

<!-- Old headings. Do not remove or links may break. -->

<a id="a-use-case-for-interior-mutability-mock-objects"></a>

#### Tesztelés mock objektumokkal {#testing-with-mock-objects}

A programozók tesztelés közben néha egy típust egy másik helyett használnak,
hogy megfigyeljenek egy bizonyos viselkedést, és ellenőrizzék, hogy az
helyesen van-e megvalósítva. Ezt a helyettesítő típust _tesztdublőrnek (test
double)_ nevezzük. Gondolj rá úgy, mint a filmkészítésben a kaszkadőrre, aki
beugrik, és egy színészt helyettesít egy különösen nehéz jelenetben. A
tesztdublőrök a tesztek futtatásakor más típusokat helyettesítenek. A _mock
objektumok (mock objects)_ a tesztdublőrök olyan speciális fajtái, amelyek
rögzítik, mi történik egy teszt során, így ellenőrizheted, hogy a megfelelő
műveletek történtek-e meg.

A Rustban nincsenek objektumok abban az értelemben, ahogyan más nyelvekben, és
a Rust standard könyvtárába – egyes más nyelvekkel ellentétben – nincs beépítve
mock objektum funkcionalitás. Mindazonáltal nyugodtan létrehozhatsz egy olyan
struktúrát, amely ugyanazt a célt szolgálja, mint egy mock objektum.

Ezt a forgatókönyvet fogjuk tesztelni: készítünk egy könyvtárat, amely egy
értéket egy maximális értékhez viszonyítva követ, és aszerint küld üzeneteket,
hogy az aktuális érték mennyire közelíti meg a maximumot. Ezt a könyvtárat
például arra lehetne használni, hogy nyomon kövessük egy felhasználó
kvótáját, vagyis hogy hány API-hívást indíthat.

A könyvtárunk csak azt a funkcionalitást biztosítja, hogy nyomon kövesse,
mennyire közelíti meg egy érték a maximumot, és hogy mikor milyen üzeneteket
kell küldeni. A könyvtárunkat használó alkalmazásoktól elvárjuk, hogy ők
biztosítsák az üzenetek küldésének mechanizmusát: az alkalmazás megjelenítheti
az üzenetet közvetlenül a felhasználónak, küldhet e-mailt vagy SMS-t, vagy
valami mást is tehet. A könyvtárnak nem kell ismernie ezt a részletet. Csak
valamire van szüksége, ami megvalósít egy általunk biztosított, `Messenger`
nevű traitet. A 15-20. kódrészlet a könyvtár kódját mutatja.

<Listing number="15-20" file-name="src/lib.rs" caption="Egy könyvtár, amely nyomon követi, mennyire közelíti meg egy érték a maximumot, és figyelmeztet, ha az érték bizonyos szinteket elér">

```rust,noplayground
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-20/src/lib.rs}}
```

</Listing>

A kód egyik fontos része, hogy a `Messenger` traitnek egyetlen, `send` nevű
metódusa van, amely egy `self`-re mutató nem módosítható referenciát és az
üzenet szövegét várja. Ez a trait az az interfész, amelyet a mock
objektumunknak meg kell valósítania, hogy a mockot ugyanúgy lehessen használni,
mint egy valódi objektumot. A másik fontos rész, hogy a `LimitTracker`
`set_value` metódusának viselkedését szeretnénk tesztelni. Változtathatjuk,
hogy mit adunk át a `value` paraméternek, de a `set_value` nem ad vissza
semmit, amire állításokat tehetnénk. Azt szeretnénk kimondani, hogy ha egy
`LimitTracker`-t valamivel, ami megvalósítja a `Messenger` traitet, és egy
adott `max` értékkel hozunk létre, akkor az üzenetküldő a `value` különböző
értékeinek átadásakor utasítást kap a megfelelő üzenetek elküldésére.

Olyan mock objektumra van szükségünk, amely a `send` hívásakor e-mail vagy SMS
küldése helyett csak nyilvántartja azokat az üzeneteket, amelyeknek az
elküldésére utasítást kapott. Létrehozhatjuk a mock objektum egy új
példányát, létrehozhatunk egy `LimitTracker`-t, amely a mock objektumot
használja, meghívhatjuk a `LimitTracker` `set_value` metódusát, majd
ellenőrizhetjük, hogy a mock objektumban megvannak-e a várt üzenetek. A 15-21.
kódrészlet egy kísérletet mutat egy ilyen mock objektum megvalósítására, de a
kölcsönzésellenőrző ezt nem engedi meg.

<Listing number="15-21" file-name="src/lib.rs" caption="Kísérlet egy `MockMessenger` megvalósítására, amelyet a kölcsönzésellenőrző nem enged meg">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-21/src/lib.rs:here}}
```

</Listing>

Ez a tesztkód egy `MockMessenger` struktúrát definiál, amelynek van egy
`sent_messages` mezője: ez `String` értékek `Vec`-je, amely nyilvántartja
azokat az üzeneteket, amelyeknek az elküldésére utasítást kapott. Definiálunk
egy `new` társított függvényt is, hogy kényelmesen hozhassunk létre új,
üres üzenetlistával induló `MockMessenger` értékeket. Ezután megvalósítjuk a
`Messenger` traitet a `MockMessenger`-re, hogy egy `MockMessenger`-t
adhassunk egy `LimitTracker`-nek. A `send` metódus definíciójában a
paraméterként átadott üzenetet a `MockMessenger` `sent_messages` listájában
tároljuk.

A tesztben azt vizsgáljuk, mi történik, amikor a `LimitTracker` utasítást kap,
hogy a `value` értékét a `max` érték 75 százalékánál nagyobbra állítsa. Először
létrehozunk egy új `MockMessenger`-t, amely üres üzenetlistával indul. Ezután
létrehozunk egy új `LimitTracker`-t, és átadjuk neki az új `MockMessenger`-re
mutató referenciát és a `100`-as `max` értéket. A `LimitTracker` `set_value`
metódusát a `80`-as értékkel hívjuk meg, ami több mint a 100 75 százaléka. Végül
ellenőrizzük, hogy a `MockMessenger` által nyilvántartott üzenetlistában most
egy üzenet van.

Ezzel a teszttel azonban van egy probléma, ahogy itt látható:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-21/output.txt}}
```

Nem módosíthatjuk a `MockMessenger`-t az üzenetek nyilvántartásához, mert a
`send` metódus egy `self`-re mutató nem módosítható referenciát vár. A
hibaüzenet azon javaslatát sem fogadhatjuk meg, hogy az `impl` metódusban és a
traitdefinícióban is `&mut self`-et használjunk. Nem szeretnénk a `Messenger`
traitet csupán a tesztelés kedvéért módosítani. Ehelyett meg kell találnunk a
módját, hogyan működhet helyesen a tesztkódunk a meglévő tervezéssel.

Ez egy olyan helyzet, amelyben a belső módosíthatóság segíthet! A
`sent_messages`-t egy `RefCell<T>`-ben tároljuk, és így a `send` metódus
módosíthatja a `sent_messages`-t, hogy eltárolja a látott üzeneteket. A 15-22.
kódrészlet mutatja, hogyan néz ki ez.

<Listing number="15-22" file-name="src/lib.rs" caption="A `RefCell<T>` használata egy belső érték módosítására, miközben a külső érték nem módosíthatónak számít">

```rust,noplayground
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-22/src/lib.rs:here}}
```

</Listing>

A `sent_messages` mező típusa most `Vec<String>` helyett
`RefCell<Vec<String>>`. A `new` függvényben az üres vektor köré egy új
`RefCell<Vec<String>>` példányt hozunk létre.

A `send` metódus megvalósításában az első paraméter továbbra is a `self` nem
módosítható kölcsönzése, ami megfelel a traitdefiníciónak. A
`self.sent_messages`-ben lévő `RefCell<Vec<String>>`-en meghívjuk a
`borrow_mut`-ot, hogy módosítható referenciát kapjunk a
`RefCell<Vec<String>>`-en belüli értékre, vagyis a vektorra. Ezután a
vektorra mutató módosítható referencián meghívhatjuk a `push`-t, hogy
nyilvántartsuk a teszt során elküldött üzeneteket.

Az utolsó változtatás, amelyet el kell végeznünk, az állításban van: hogy
lássuk, hány elem van a belső vektorban, a `RefCell<Vec<String>>`-en
meghívjuk a `borrow`-t, hogy egy nem módosítható referenciát kapjunk a
vektorra.

Most, hogy láttad, hogyan használható a `RefCell<T>`, nézzük meg, hogyan
működik!

<!-- Old headings. Do not remove or links may break. -->

<a id="keeping-track-of-borrows-at-runtime-with-refcellt"></a>

#### A kölcsönzések nyilvántartása futásidőben {#tracking-borrows-at-runtime}

Nem módosítható és módosítható referenciák létrehozásakor a `&`, illetve a
`&mut` szintaxist használjuk. A `RefCell<T>` esetén a `borrow` és a
`borrow_mut` metódust használjuk, amelyek a `RefCell<T>`-hez tartozó
biztonságos API részei. A `borrow` metódus egy `Ref<T>` okos mutatótípust ad
vissza, a `borrow_mut` pedig egy `RefMut<T>` okos mutatótípust. Mindkét típus
megvalósítja a `Deref`-et, így hagyományos referenciaként kezelhetjük őket.

A `RefCell<T>` nyilvántartja, hány `Ref<T>` és `RefMut<T>` okos mutató aktív
éppen. Minden `borrow` hívásnál a `RefCell<T>` megnöveli az aktív nem
módosítható kölcsönzések számlálóját. Amikor egy `Ref<T>` érték kikerül a
hatókörből, a nem módosítható kölcsönzések száma 1-gyel csökken. A fordítási
idejű kölcsönzési szabályokhoz hasonlóan a `RefCell<T>` bármely pillanatban
sok nem módosítható kölcsönzést vagy egyetlen módosítható kölcsönzést enged
meg.

Ha megpróbáljuk megszegni ezeket a szabályokat, akkor ahelyett, hogy a
referenciákhoz hasonlóan fordítási hibát kapnánk, a `RefCell<T>`
megvalósítása futásidőben pánikol. A 15-23. kódrészlet a 15-22. kódrészletbeli
`send` megvalósításának egy módosítását mutatja. Szándékosan próbálunk két,
ugyanabban a hatókörben aktív módosítható kölcsönzést létrehozni, hogy
szemléltessük: a `RefCell<T>` ezt futásidőben megakadályozza.

<Listing number="15-23" file-name="src/lib.rs" caption="Két módosítható referencia létrehozása ugyanabban a hatókörben, hogy lássuk, a `RefCell<T>` pánikolni fog">

```rust,ignore,panics
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-23/src/lib.rs:here}}
```

</Listing>

Létrehozunk egy `one_borrow` változót a `borrow_mut` által visszaadott
`RefMut<T>` okos mutató számára. Ezután ugyanígy létrehozunk egy másik
módosítható kölcsönzést a `two_borrow` változóban. Így ugyanabban a hatókörben
két módosítható referencia jön létre, ami nem megengedett. Amikor lefuttatjuk
a könyvtárunk tesztjeit, a 15-23. kódrészlet kódja hiba nélkül lefordul, de a
teszt elbukik:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-23/output.txt}}
```

Figyeld meg, hogy a kód az `already borrowed: BorrowMutError` üzenettel
pánikolt. A `RefCell<T>` így kezeli a kölcsönzési szabályok futásidejű
megsértését.

Ha úgy döntesz, hogy a kölcsönzési hibákat – ahogy itt tettük – fordítási idő
helyett futásidőben kapod el, az azt jelenti, hogy a kódod hibáit
esetleg csak később, a fejlesztési folyamat egy későbbi szakaszában találod
meg: akár csak azután, hogy a kódod éles környezetbe került. Emellett a kódod
egy kis futásidejű teljesítményveszteséget is elszenved, mivel a
kölcsönzéseket fordítási idő helyett futásidőben tartja nyilván. A
`RefCell<T>` használata viszont lehetővé teszi, hogy olyan mock objektumot
írj, amely módosítani tudja önmagát, hogy nyilvántartsa a látott üzeneteket,
miközben olyan környezetben használod, ahol csak nem módosítható értékek
megengedettek. A kompromisszumai ellenére is használhatod a `RefCell<T>`-t,
hogy több funkcionalitást kapj, mint amennyit a hagyományos referenciák
nyújtanak.

<!-- Old headings. Do not remove or links may break. -->

<a id="having-multiple-owners-of-mutable-data-by-combining-rc-t-and-ref-cell-t"></a>
<a id="allowing-multiple-owners-of-mutable-data-with-rct-and-refcellt"></a>

### Több tulajdonos engedélyezése módosítható adatokhoz {#allowing-multiple-owners-of-mutable-data}

A `RefCell<T>` gyakori felhasználási módja az `Rc<T>`-vel való kombinálás.
Emlékezz, hogy az `Rc<T>` lehetővé teszi, hogy egy adatnak több tulajdonosa
legyen, de csak nem módosítható hozzáférést ad az adathoz. Ha van egy
`RefCell<T>`-t tároló `Rc<T>`-d, olyan értéket kaphatsz, amelynek több
tulajdonosa lehet, _és_ amelyet módosíthatsz is!

Idézd fel például a 15-18. kódrészlet cons lista példáját, amelyben az
`Rc<T>`-vel tettük lehetővé, hogy több lista osztozzon egy másik lista
tulajdonjogán. Mivel az `Rc<T>` csak nem módosítható értékeket tárol, a lista
értékeit a létrehozásuk után nem változtathatjuk meg. Adjuk hozzá a
`RefCell<T>`-t, hogy megváltoztathassuk a listákban lévő értékeket. A 15-24.
kódrészlet azt mutatja, hogy a `Cons` definíciójában egy `RefCell<T>`-t
használva az összes listában tárolt értéket módosíthatjuk.

<Listing number="15-24" file-name="src/main.rs" caption="Az `Rc<RefCell<i32>>` használata egy módosítható `List` létrehozására">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-24/src/main.rs}}
```

</Listing>

Létrehozunk egy értéket, amely az `Rc<RefCell<i32>>` egy példánya, és egy
`value` nevű változóban tároljuk, hogy később közvetlenül hozzáférhessünk.
Ezután létrehozunk egy `List`-et az `a`-ban egy olyan `Cons` változattal,
amely a `value`-t tárolja. A `value`-t klónoznunk kell, hogy az `a` és a
`value` is birtokolja a belső `5` értéket, ahelyett hogy a tulajdonjogot a
`value`-ból az `a`-ba mozgatnánk, vagy hogy az `a` a `value`-ból kölcsönözne.

Az `a` listát egy `Rc<T>`-be burkoljuk, hogy amikor létrehozzuk a `b` és a `c`
listát, mindkettő hivatkozhasson az `a`-ra, ahogy a 15-18. kódrészletben is
tettük.

Miután létrehoztuk az `a`, `b` és `c` listát, 10-et szeretnénk hozzáadni a
`value`-ban lévő értékhez. Ezt úgy tesszük meg, hogy meghívjuk a
`borrow_mut`-ot a `value`-n, amely az 5. fejezet [„Hol van a `->`
operátor?”][wheres-the---operator]<!-- ignore --> részében tárgyalt automatikus
dereferálási funkciót használja ahhoz, hogy az `Rc<T>`-t a belső `RefCell<T>`
értékre dereferálja. A `borrow_mut` metódus egy `RefMut<T>` okos mutatót ad
vissza, amelyen a dereferáló operátort használva megváltoztatjuk a belső
értéket.

Amikor kiírjuk az `a`-t, a `b`-t és a `c`-t, láthatjuk, hogy mindegyikben az
`5` helyett a módosított `15` érték szerepel:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-24/output.txt}}
```

Ez a technika igazán ügyes! A `RefCell<T>` használatával kívülről nem
módosítható `List` értékünk van. A `RefCell<T>` belső módosíthatóságot
biztosító metódusaival azonban módosíthatjuk az adatainkat, amikor szükséges. A
kölcsönzési szabályok futásidejű ellenőrzése megvéd minket az
adatversenyektől, és néha megéri egy kis sebességet feláldozni az
adatszerkezeteink e rugalmasságáért. Figyelj arra, hogy a `RefCell<T>` nem
működik többszálú kódban! A `Mutex<T>` a `RefCell<T>` szálbiztos változata; a
`Mutex<T>`-et a 16. fejezetben tárgyaljuk.

[wheres-the---operator]: ch05-03-method-syntax.html#wheres-the---operator
