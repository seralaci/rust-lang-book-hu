## Unsafe Rust {#unsafe-rust}

Az eddig tárgyalt kódokban a Rust fordítási időben kikényszerítette a
memóriabiztonsági garanciáit. A Rustban azonban rejtőzik egy második nyelv is,
amely nem kényszeríti ki ezeket a memóriabiztonsági garanciákat: ez az _unsafe
Rust_ (nem biztonságos Rust), amely pontosan úgy működik, mint a szokásos Rust,
de extra szuperképességeket ad.

Az unsafe Rust azért létezik, mert a statikus elemzés természeténél fogva
óvatos. Amikor a fordító megpróbálja eldönteni, hogy a kód betartja-e a
garanciákat, jobb, ha elutasít néhány érvényes programot, mint ha elfogadna
néhány érvénytelent. Hiába lehet, hogy a kód _talán_ rendben van, ha a Rust
fordítónak nincs elég információja ahhoz, hogy biztos legyen benne, elutasítja
a kódot. Ilyenkor unsafe kóddal mondhatod meg a fordítónak: „Bízz bennem, tudom,
mit csinálok.” Ne feledd azonban, hogy az unsafe Rustot a saját felelősségedre
használod: ha helytelenül használsz unsafe kódot, a memória nem biztonságos
kezeléséből fakadó problémák léphetnek fel, például null mutató dereferálása.

A Rust nem biztonságos alteregójának másik oka, hogy a számítógép mögöttes
hardvere eleve nem biztonságos. Ha a Rust nem engedne nem biztonságos
műveleteket, bizonyos feladatokat nem tudnál elvégezni. A Rustnak lehetővé kell
tennie az alacsony szintű rendszerprogramozást, például az operációs rendszerrel
való közvetlen együttműködést, vagy akár egy saját operációs rendszer megírását.
Az alacsony szintű rendszerprogramozás támogatása a nyelv egyik célja. Nézzük
meg, mit tehetünk az unsafe Rusttal, és hogyan!

<!-- Old headings. Do not remove or links may break. -->

<a id="unsafe-superpowers"></a>

### Unsafe szuperképességek használata {#performing-unsafe-superpowers}

Az unsafe Rustra úgy válthatsz át, hogy az `unsafe` kulcsszó után egy új
blokkot nyitsz, amely a nem biztonságos kódot tartalmazza. Az unsafe Rustban öt
olyan dolgot tehetsz meg, amelyet a biztonságos Rustban nem; ezeket _unsafe
szuperképességeknek (unsafe superpowers)_ nevezzük. Ezek a szuperképességek a
következők:

1. Nyers mutató dereferálása.
1. Unsafe függvény vagy metódus meghívása.
1. Módosítható statikus változó elérése vagy módosítása.
1. Unsafe trait megvalósítása.
1. `union`-ok mezőinek elérése.

Fontos megérteni, hogy az `unsafe` nem kapcsolja ki a kölcsönzésellenőrzőt, és
a Rust többi biztonsági ellenőrzését sem tiltja le: ha unsafe kódban
referenciát használsz, az továbbra is ellenőrzés alá esik. Az `unsafe` kulcsszó
csak ehhez az öt nyelvi elemhez ad hozzáférést, amelyeknek a memóriabiztonságát
aztán a fordító nem ellenőrzi. Egy unsafe blokkon belül is megmarad tehát a
biztonság bizonyos foka.

Ráadásul az `unsafe` nem jelenti azt, hogy a blokkon belüli kód feltétlenül
veszélyes, vagy hogy biztosan memóriabiztonsági problémái lesznek: a szándék az,
hogy programozóként te gondoskodj arról, hogy az `unsafe` blokkon belüli kód
érvényes módon férjen hozzá a memóriához.

Az emberek tévednek, és hibák mindig lesznek, de mivel ennek az öt nem
biztonságos műveletnek `unsafe` jelölésű blokkokban kell lennie, tudni fogod,
hogy minden memóriabiztonsággal kapcsolatos hibának egy `unsafe` blokkon belül
kell lennie. Tartsd kicsinek az `unsafe` blokkokat; később hálás leszel érte,
amikor memóriahibák után nyomozol.

Hogy a nem biztonságos kódot a lehető legjobban elszigeteld, érdemes az ilyen
kódot egy biztonságos absztrakcióba zárni, és biztonságos API-t nyújtani – erről
a fejezet későbbi részében lesz szó, amikor az unsafe függvényeket és
metódusokat vizsgáljuk. A standard könyvtár egyes részei is biztonságos
absztrakcióként vannak megvalósítva auditált unsafe kód fölött. Ha a nem
biztonságos kódot biztonságos absztrakcióba burkolod, azzal megakadályozod, hogy
az `unsafe` használata kiszivárogjon mindazokra a helyekre, ahol te vagy a
felhasználóid az `unsafe` kóddal megvalósított funkcionalitást használni
szeretnétek, hiszen egy biztonságos absztrakció használata biztonságos.

Vegyük sorra az öt unsafe szuperképességet! Megnézünk néhány olyan
absztrakciót is, amely biztonságos interfészt nyújt nem biztonságos kódhoz.

### Nyers mutató dereferálása {#dereferencing-a-raw-pointer}

A 4. fejezet [„Lógó referenciák”][dangling-references]<!-- ignore -->
szakaszában említettük, hogy a fordító biztosítja, hogy a referenciák mindig
érvényesek legyenek. Az unsafe Rustban van két új típus, a _nyers mutatók (raw
pointers)_, amelyek a referenciákhoz hasonlítanak. A referenciákhoz hasonlóan a
nyers mutatók is lehetnek nem módosíthatók vagy módosíthatók, és `*const T`,
illetve `*mut T` alakban írjuk őket. A csillag itt nem a dereferáló operátor,
hanem a típusnév része. Nyers mutatók esetén a _nem módosítható (immutable)_
azt jelenti, hogy a mutatónak a dereferálás után nem lehet közvetlenül értéket
adni.

A referenciáktól és az okos mutatóktól eltérően a nyers mutatók:

- figyelmen kívül hagyhatják a kölcsönzési szabályokat, vagyis lehet egyszerre
  nem módosítható és módosítható mutatójuk, vagy több módosítható mutatójuk
  ugyanarra a helyre
- nem garantáltan mutatnak érvényes memóriára
- lehetnek null értékűek
- nem valósítanak meg semmilyen automatikus takarítást

Ha lemondasz arról, hogy a Rust kikényszerítse ezeket a garanciákat, a
garantált biztonságot nagyobb teljesítményre, vagy arra a lehetőségre
cserélheted, hogy olyan más nyelvvel vagy hardverrel működj együtt, amelyre a
Rust garanciái nem vonatkoznak.

A 20-1. kódrészlet bemutatja, hogyan hozhatunk létre egy nem módosítható és egy
módosítható nyers mutatót.

<Listing number="20-1" caption="Nyers mutatók létrehozása a nyers kölcsönző operátorokkal">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-01/src/main.rs:here}}
```

</Listing>

Figyeld meg, hogy ebben a kódban nem szerepel az `unsafe` kulcsszó. Nyers
mutatókat biztonságos kódban is létrehozhatunk; csak dereferálni nem tudjuk
őket egy unsafe blokkon kívül, ahogy hamarosan látni fogod.

A nyers mutatókat a nyers kölcsönző operátorokkal (raw borrow operators) hoztuk
létre: a `&raw const num` egy `*const i32` típusú, nem módosítható nyers
mutatót, a `&raw mut num` pedig egy `*mut i32` típusú, módosítható nyers
mutatót hoz létre. Mivel közvetlenül egy lokális változóból hoztuk létre őket,
tudjuk, hogy ezek a konkrét nyers mutatók érvényesek, de ezt nem
feltételezhetjük bármilyen nyers mutatóról.

Ennek szemléltetésére most létrehozunk egy olyan nyers mutatót, amelynek
érvényességében nem lehetünk ennyire biztosak: a nyers kölcsönző operátor
helyett az `as` kulcsszóval alakítunk át egy értéket. A 20-2. kódrészlet azt
mutatja, hogyan hozhatunk létre nyers mutatót a memória egy tetszőleges
helyére. Tetszőleges memória használatának megkísérlése nem definiált: lehet,
hogy azon a címen vannak adatok, lehet, hogy nincsenek, a fordító úgy is
optimalizálhatja a kódot, hogy egyáltalán ne történjen memória-hozzáférés, de az
is lehet, hogy a program szegmentálási hibával (segmentation fault) leáll.
Általában nincs jó ok arra, hogy ilyen kódot írjunk, különösen ott, ahol
helyette nyers kölcsönző operátort is használhatunk, de lehetséges.

<Listing number="20-2" caption="Nyers mutató létrehozása egy tetszőleges memóriacímre">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-02/src/main.rs:here}}
```

</Listing>

Emlékezz: nyers mutatókat létrehozhatunk biztonságos kódban, de nem
dereferálhatjuk őket, és nem olvashatjuk ki az adatot, amelyre mutatnak. A 20-3.
kódrészletben a `*` dereferáló operátort egy olyan nyers mutatón használjuk,
amelyhez `unsafe` blokk szükséges.

<Listing number="20-3" caption="Nyers mutatók dereferálása egy `unsafe` blokkon belül">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-03/src/main.rs:here}}
```

</Listing>

Egy mutató létrehozása nem okoz kárt; csak akkor kerülhetünk szembe érvénytelen
értékkel, amikor megpróbáljuk elérni az értéket, amelyre mutat.

Vedd észre azt is, hogy a 20-1. és a 20-3. kódrészletben olyan `*const i32` és
`*mut i32` nyers mutatókat hoztunk létre, amelyek ugyanarra a memóriahelyre
mutattak, ahol a `num` tárolódik. Ha ehelyett egy nem módosítható és egy
módosítható referenciát próbáltunk volna létrehozni a `num`-ra, a kód nem
fordult volna le, mert a Rust tulajdonjogi szabályai nem engednek meg
módosítható referenciát nem módosítható referenciákkal egy időben. Nyers
mutatókkal létrehozhatunk egy módosítható és egy nem módosítható mutatót
ugyanarra a helyre, és a módosítható mutatón keresztül megváltoztathatjuk az
adatot, ami adatversenyhez vezethet. Légy óvatos!

Ennyi veszély mellett miért használnál egyáltalán nyers mutatókat? Az egyik fő
felhasználási terület a C kóddal való együttműködés, ahogy a következő
szakaszban látni fogod. Egy másik az olyan biztonságos absztrakciók építése,
amelyeket a kölcsönzésellenőrző nem ért meg. Bemutatjuk az unsafe függvényeket,
majd megnézünk egy példát egy unsafe kódot használó biztonságos absztrakcióra.

### Unsafe függvény vagy metódus meghívása {#calling-an-unsafe-function-or-method}

A második olyan művelet, amelyet unsafe blokkban végezhetsz, az unsafe
függvények meghívása. Az unsafe függvények és metódusok pontosan úgy néznek ki,
mint a szokásos függvények és metódusok, de a definíciójuk elején egy extra
`unsafe` áll. Az `unsafe` kulcsszó ebben a kontextusban azt jelzi, hogy a
függvénynek olyan követelményei vannak, amelyeket a hívásakor nekünk kell
betartanunk, mert a Rust nem tudja garantálni, hogy teljesítettük őket. Amikor
egy unsafe függvényt egy `unsafe` blokkon belül hívunk meg, azt mondjuk, hogy
elolvastuk a függvény dokumentációját, és vállaljuk a felelősséget a függvény
szerződésének betartásáért.

Íme egy `dangerous` nevű unsafe függvény, amelynek a törzse semmit sem csinál:

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-01-unsafe-fn/src/main.rs:here}}
```

A `dangerous` függvényt egy külön `unsafe` blokkon belül kell meghívnunk. Ha
`unsafe` blokk nélkül próbáljuk meghívni a `dangerous`-t, hibát kapunk:

```console
{{#include ../listings/ch20-advanced-features/output-only-01-missing-unsafe/output.txt}}
```

Az `unsafe` blokkal azt állítjuk a Rustnak, hogy elolvastuk a függvény
dokumentációját, értjük, hogyan kell helyesen használni, és meggyőződtünk róla,
hogy teljesítjük a függvény szerződését.

Ha egy `unsafe` függvény törzsében nem biztonságos műveleteket szeretnél
végezni, akkor is `unsafe` blokkot kell használnod, akárcsak egy szokásos
függvényben, és a fordító figyelmeztet, ha elfelejted. Ez segít abban, hogy az
`unsafe` blokkokat a lehető legkisebbre szabjuk, hiszen a nem biztonságos
műveletekre nem feltétlenül van szükség a függvény teljes törzsében.

#### Biztonságos absztrakció létrehozása nem biztonságos kód fölött {#creating-a-safe-abstraction-over-unsafe-code}

Attól, hogy egy függvény nem biztonságos kódot tartalmaz, még nem kell az egész
függvényt unsafe-ként megjelölnünk. Sőt, a nem biztonságos kód biztonságos
függvénybe burkolása gyakori absztrakció. Példaként vizsgáljuk meg a standard
könyvtár `split_at_mut` függvényét, amelyhez némi unsafe kód szükséges.
Megnézzük, hogyan valósíthatnánk meg. Ez a biztonságos metódus módosítható
szeleteken van definiálva: egy szeletet kap, és kettévágja azt az
argumentumként megadott indexnél. A 20-4. kódrészlet a `split_at_mut`
használatát mutatja.

<Listing number="20-4" caption="A biztonságos `split_at_mut` függvény használata">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-04/src/main.rs:here}}
```

</Listing>

Ezt a függvényt nem tudjuk csak biztonságos Rusttal megvalósítani. Egy
próbálkozás a 20-5. kódrészlethez hasonlóan nézhet ki, ami nem fordul le. Az
egyszerűség kedvéért a `split_at_mut`-ot metódus helyett függvényként
valósítjuk meg, és csak `i32` értékek szeleteire, nem pedig egy generikus `T`
típusra.

<Listing number="20-5" caption="Kísérlet a `split_at_mut` megvalósítására csak biztonságos Rusttal">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-05/src/main.rs:here}}
```

</Listing>

A függvény először lekéri a szelet teljes hosszát. Ezután ellenőrzi, hogy a
paraméterként kapott index a szeleten belül van-e, vagyis kisebb-e a hossznál,
vagy egyenlő-e vele. Az állítás azt jelenti, hogy ha a hossznál nagyobb indexet
adunk át a szelet kettévágásához, a függvény pánikol, még mielőtt megpróbálná
használni az indexet.

Ezután két módosítható szeletet adunk vissza egy tuple-ben: az egyik az eredeti
szelet elejétől a `mid` indexig tart, a másik a `mid`-től a szelet végéig.

Ha megpróbáljuk lefordítani a 20-5. kódrészlet kódját, hibát kapunk:

```console
{{#include ../listings/ch20-advanced-features/listing-20-05/output.txt}}
```

A Rust kölcsönzésellenőrzője nem érti, hogy a szelet különböző részeit
kölcsönözzük; csak azt tudja, hogy kétszer kölcsönzünk ugyanabból a szeletből.
Egy szelet különböző részeinek kölcsönzése alapvetően rendben van, mert a két
szelet nem fedi át egymást, de a Rust nem elég okos ahhoz, hogy ezt tudja. Ha
mi tudjuk, hogy a kód rendben van, de a Rust nem, akkor jött el az ideje, hogy
unsafe kódhoz nyúljunk.

A 20-6. kódrészlet bemutatja, hogyan tehetjük működőképessé a `split_at_mut`
megvalósítását egy `unsafe` blokk, egy nyers mutató és néhány unsafe függvény
meghívásának segítségével.

<Listing number="20-6" caption="Unsafe kód használata a `split_at_mut` függvény megvalósításában">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-06/src/main.rs:here}}
```

</Listing>

Emlékezz a 4. fejezet [„A szelet típus”][the-slice-type]<!-- ignore -->
szakaszából, hogy a szelet egy adatra mutató mutatóból és a szelet hosszából
áll. A `len` metódussal kérjük le a szelet hosszát, az `as_mut_ptr` metódussal
pedig a szelet nyers mutatóját. Ebben az esetben, mivel `i32` értékek
módosítható szeletével van dolgunk, az `as_mut_ptr` egy `*mut i32` típusú nyers
mutatót ad vissza, amelyet a `ptr` változóban tárolunk.

Megtartjuk azt az állítást, hogy a `mid` index a szeleten belül van. Ezután
jön a nem biztonságos kód: a `slice::from_raw_parts_mut` függvény egy nyers
mutatót és egy hosszt kap, és ezekből szeletet hoz létre. Ezzel a függvénnyel
létrehozunk egy szeletet, amely a `ptr`-től indul, és `mid` elem hosszú. Ezután
a `ptr`-en meghívjuk az `add` metódust a `mid` argumentummal, hogy egy `mid`-nél
kezdődő nyers mutatót kapjunk, és ezzel a mutatóval, valamint a `mid` utáni
elemek számával mint hosszal létrehozunk egy másik szeletet.

A `slice::from_raw_parts_mut` függvény unsafe, mert nyers mutatót kap, és meg
kell bíznia abban, hogy ez a mutató érvényes. A nyers mutatók `add` metódusa is
unsafe, mert meg kell bíznia abban, hogy az eltolással kapott hely is érvényes
mutató. Ezért kellett a `slice::from_raw_parts_mut` és az `add` hívásait egy
`unsafe` blokkba tennünk, hogy meghívhassuk őket. A kódot megnézve, és mivel
hozzáadtuk azt az állítást, hogy a `mid` kisebb vagy egyenlő a `len`-nél,
megállapíthatjuk, hogy az `unsafe` blokkon belül használt összes nyers mutató
érvényes mutató lesz a szeleten belüli adatokra. Ez az `unsafe` elfogadható és
helyénvaló használata.

Vedd észre, hogy az eredményül kapott `split_at_mut` függvényt nem kell
`unsafe`-ként megjelölnünk, és meghívhatjuk biztonságos Rustból. Biztonságos
absztrakciót hoztunk létre a nem biztonságos kód fölött a függvény olyan
megvalósításával, amely biztonságos módon használja az `unsafe` kódot, mert
csak olyan adatokból hoz létre érvényes mutatókat, amelyekhez a függvénynek
hozzáférése van.

Ezzel szemben a `slice::from_raw_parts_mut` 20-7. kódrészletbeli használata
valószínűleg összeomláshoz vezetne a szelet használatakor. Ez a kód egy
tetszőleges memóriahelyből egy 10 000 elem hosszú szeletet hoz létre.

<Listing number="20-7" caption="Szelet létrehozása egy tetszőleges memóriahelyből">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-07/src/main.rs:here}}
```

</Listing>

Ezen a tetszőleges helyen lévő memória nem a miénk, és semmi sem garantálja,
hogy a kód által létrehozott szelet érvényes `i32` értékeket tartalmaz. Ha a
`values`-t érvényes szeletként próbáljuk használni, az nem definiált
viselkedéshez vezet.

#### `extern` függvények használata külső kód meghívására {#using-extern-functions-to-call-external-code}

Előfordulhat, hogy a Rust kódodnak egy másik nyelven írt kóddal kell
együttműködnie. Erre a Rustban az `extern` kulcsszó szolgál, amely megkönnyíti
egy _idegenfüggvény-interfész (Foreign Function Interface, FFI)_ létrehozását
és használatát. Az FFI segítségével egy programozási nyelv függvényeket
definiálhat, és lehetővé teheti, hogy egy másik (idegen) programozási nyelv
meghívja ezeket a függvényeket.

A 20-8. kódrészlet bemutatja, hogyan állíthatunk be integrációt a C standard
könyvtár `abs` függvényével. Az `extern` blokkokon belül deklarált függvények
meghívása Rust kódból általában nem biztonságos, ezért az `extern` blokkokat is
`unsafe`-ként kell megjelölni. Ennek oka, hogy más nyelvek nem kényszerítik ki
a Rust szabályait és garanciáit, a Rust pedig nem tudja ellenőrizni őket, így a
biztonság szavatolásának felelőssége a programozóra hárul.

<Listing number="20-8" file-name="src/main.rs" caption="Egy másik nyelven definiált `extern` függvény deklarálása és meghívása">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-08/src/main.rs}}
```

</Listing>

Az `unsafe extern "C"` blokkon belül felsoroljuk azoknak a másik nyelvből
származó külső függvényeknek a nevét és szignatúráját, amelyeket meg szeretnénk
hívni. A `"C"` rész azt határozza meg, hogy a külső függvény melyik _bináris
alkalmazásinterfészt (application binary interface, ABI)_ használja: az ABI
azt definiálja, hogyan kell a függvényt assembly szinten meghívni. A `"C"` ABI
a leggyakoribb, és a C programozási nyelv ABI-ját követi. A Rust által
támogatott összes ABI-ról [a Rust referenciában][ABI] találsz információt.

Egy `unsafe extern` blokkon belül deklarált minden elem implicit módon unsafe.
Néhány FFI-függvény meghívása azonban *valóban* biztonságos. Például a C
standard könyvtárának `abs` függvénye nem vet fel memóriabiztonsági kérdéseket,
és tudjuk, hogy bármilyen `i32` értékkel meghívható. Ilyen esetekben a `safe`
kulcsszóval jelezhetjük, hogy ez a konkrét függvény biztonságosan meghívható,
annak ellenére, hogy egy `unsafe extern` blokkban van. E változtatás után a
meghívásához már nem kell `unsafe` blokk, ahogy a 20-9. kódrészlet mutatja.

<Listing number="20-9" file-name="src/main.rs" caption="Egy függvény explicit `safe` jelölése egy `unsafe extern` blokkon belül, és biztonságos meghívása">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-09/src/main.rs}}
```

</Listing>

Attól, hogy egy függvényt `safe`-ként jelölsz meg, az még nem válik
biztonságossá! Ez inkább egy ígéret, amelyet a Rustnak teszel arra, hogy a
függvény biztonságos. Továbbra is a te felelősséged, hogy ezt az ígéretet
betartsd!

#### Rust függvények hívása más nyelvekből {#calling-rust-functions-from-other-languages}

Az `extern` kulcsszóval olyan interfészt is létrehozhatunk, amely lehetővé
teszi, hogy más nyelvek Rust függvényeket hívjanak meg. Egy teljes `extern`
blokk létrehozása helyett az adott függvény `fn` kulcsszava elé írjuk az
`extern` kulcsszót, és megadjuk a használandó ABI-t. Egy `#[unsafe(no_mangle)]`
annotációt is hozzá kell adnunk, hogy jelezzük a Rust fordítónak: ne
manglingolja (ne kódolja át) a függvény nevét. A _névkódolás (mangling)_ az,
amikor a fordító a függvénynek adott nevünket egy másik névre változtatja,
amely több információt tartalmaz a fordítási folyamat más részei számára, de
emberi szemmel kevésbé olvasható. Minden programozási nyelv fordítója kissé
másképp kódolja a neveket, ezért ahhoz, hogy egy Rust függvényt más nyelvekből
név szerint el lehessen érni, ki kell kapcsolnunk a Rust fordító névkódolását.
Ez nem biztonságos, mert a beépített névkódolás nélkül névütközések
fordulhatnak elő a könyvtárak között, így a mi felelősségünk meggyőződni arról,
hogy a választott név névkódolás nélkül is biztonságosan exportálható.

A következő példában a `call_from_c` függvényt elérhetővé tesszük a C kód
számára, miután megosztott könyvtárrá fordítottuk, és a C kódhoz linkeltük:

```
#[unsafe(no_mangle)]
pub extern "C" fn call_from_c() {
    println!("Just called a Rust function from C!");
}
```

Az `extern` ilyen használatánál az `unsafe` csak az attribútumban szükséges, az
`extern` blokkon nem.

### Módosítható statikus változó elérése vagy módosítása {#accessing-or-modifying-a-mutable-static-variable}

Ebben a könyvben még nem beszéltünk a globális változókról, amelyeket a Rust
támogat, de amelyek problémásak lehetnek a Rust tulajdonjogi szabályai
szempontjából. Ha két szál ugyanahhoz a módosítható globális változóhoz fér
hozzá, az adatversenyt okozhat.

A Rustban a globális változókat _statikus (static)_ változóknak nevezzük. A
20-10. kódrészlet egy sztringszelet értékű statikus változó deklarálására és
használatára mutat példát.

<Listing number="20-10" file-name="src/main.rs" caption="Nem módosítható statikus változó definiálása és használata">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-10/src/main.rs}}
```

</Listing>

A statikus változók hasonlítanak a konstansokhoz, amelyekről a 3. fejezet
[„Konstansok deklarálása”][constants]<!-- ignore --> szakaszában volt szó. A
statikus változók neve megállapodás szerint `SCREAMING_SNAKE_CASE` stílusú. A
statikus változók csak `'static` élettartamú referenciákat tárolhatnak, ami azt
jelenti, hogy a Rust fordító ki tudja következtetni az élettartamot, és nem
kell explicit módon annotálnunk. Nem módosítható statikus változó elérése
biztonságos.

A konstansok és a nem módosítható statikus változók között apró különbség, hogy
a statikus változók értékei rögzített memóriacímen vannak. Az érték használata
mindig ugyanahhoz az adathoz fér hozzá. A konstansok ezzel szemben minden
használatukkor duplikálhatják az adataikat. Egy másik különbség, hogy a
statikus változók lehetnek módosíthatók. Módosítható statikus változók elérése
és módosítása _nem biztonságos_. A 20-11. kódrészlet bemutatja, hogyan
deklarálhatunk, érhetünk el és módosíthatunk egy `COUNTER` nevű módosítható
statikus változót.

<Listing number="20-11" file-name="src/main.rs" caption="Egy módosítható statikus változó olvasása és írása nem biztonságos.">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-11/src/main.rs}}
```

</Listing>

A szokásos változókhoz hasonlóan a módosíthatóságot a `mut` kulcsszóval adjuk
meg. Minden kódnak, amely a `COUNTER`-t olvassa vagy írja, `unsafe` blokkon
belül kell lennie. A 20-11. kódrészlet kódja lefordul, és a várakozásnak
megfelelően `COUNTER: 3`-at ír ki, mert egyszálú. Ha több szál férne hozzá a
`COUNTER`-hez, az valószínűleg adatversenyhez vezetne, így ez nem definiált
viselkedés. Ezért az egész függvényt `unsafe`-ként kell megjelölnünk, és
dokumentálnunk kell a biztonsági korlátozást, hogy aki meghívja a függvényt,
tudja, mit szabad és mit nem szabad biztonságosan megtennie.

Valahányszor unsafe függvényt írunk, idiomatikus egy `SAFETY` kezdetű kommentet
írni, amely elmagyarázza, mit kell tennie a hívónak ahhoz, hogy biztonságosan
meghívhassa a függvényt. Hasonlóképpen, valahányszor nem biztonságos műveletet
végzünk, idiomatikus egy `SAFETY` kezdetű kommentben elmagyarázni, hogyan
tartjuk be a biztonsági szabályokat.

Emellett a fordító egy lint segítségével alapértelmezés szerint elutasít minden
olyan kísérletet, amely módosítható statikus változóra mutató referenciát hozna
létre. Vagy explicit módon le kell mondanod a lint védelméről egy
`#[allow(static_mut_refs)]` annotáció hozzáadásával, vagy a módosítható statikus
változót a nyers kölcsönző operátorok egyikével létrehozott nyers mutatón
keresztül kell elérned. Ez azokra az esetekre is vonatkozik, amikor a referencia
láthatatlanul jön létre, például amikor ebben a kódrészletben a `println!`-ben
használjuk. Azzal, hogy a módosítható statikus változókra mutató referenciákat
nyers mutatókon keresztül kell létrehozni, nyilvánvalóbbá válnak a használatuk
biztonsági követelményei.

Globálisan elérhető, módosítható adatok esetén nehéz biztosítani, hogy ne
legyenek adatversenyek, ezért tekinti a Rust a módosítható statikus változókat
nem biztonságosnak. Ahol lehetséges, érdemes inkább a 16. fejezetben tárgyalt
konkurens programozási technikákat és szálbiztos okos mutatókat használni, hogy
a fordító ellenőrizze, hogy a különböző szálakból történő adathozzáférés
biztonságos.

### Unsafe trait megvalósítása {#implementing-an-unsafe-trait}

Az `unsafe` segítségével unsafe traitet is megvalósíthatunk. Egy trait akkor
unsafe, ha legalább egy metódusának van olyan invariánsa, amelyet a fordító nem
tud ellenőrizni. Úgy deklarálunk egy traitet `unsafe`-ként, hogy a `trait` elé
odaírjuk az `unsafe` kulcsszót, és a trait megvalósítását is `unsafe`-ként
jelöljük meg, ahogy a 20-12. kódrészlet mutatja.

<Listing number="20-12" caption="Unsafe trait definiálása és megvalósítása">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-12/src/main.rs:here}}
```

</Listing>

Az `unsafe impl` használatával megígérjük, hogy betartjuk azokat az
invariánsokat, amelyeket a fordító nem tud ellenőrizni.

Példaként idézd fel a `Send` és `Sync` jelölő traiteket (marker traits),
amelyeket a 16. fejezet [„Bővíthető konkurencia a `Send` és a `Sync`
traittel”][send-and-sync]<!-- ignore --> szakaszában tárgyaltunk: a fordító
automatikusan megvalósítja ezeket a traiteket, ha a típusaink teljes egészében
olyan más típusokból állnak, amelyek megvalósítják a `Send`-et és a `Sync`-et.
Ha olyan típust valósítunk meg, amely olyan típust tartalmaz, amely nem
valósítja meg a `Send`-et vagy a `Sync`-et – ilyenek például a nyers mutatók –,
és ezt a típust `Send`-ként vagy `Sync`-ként szeretnénk megjelölni, akkor az
`unsafe`-et kell használnunk. A Rust nem tudja ellenőrizni, hogy a típusunk
betartja-e azokat a garanciákat, hogy biztonságosan átküldhető a szálak között,
vagy több szálból is elérhető; ezért ezeket az ellenőrzéseket kézzel kell
elvégeznünk, és ezt az `unsafe`-fel kell jeleznünk.

### Union mezőinek elérése {#accessing-fields-of-a-union}

Az utolsó művelet, amely csak `unsafe`-fel működik, egy union mezőinek
elérése. A *union* a `struct`-hoz hasonlít, de egy adott példányban egyszerre
csak egy deklarált mezőt használunk. A unionokat elsősorban a C kódban lévő
unionokkal való együttműködésre használjuk. A union mezőinek elérése nem
biztonságos, mert a Rust nem tudja garantálni, hogy milyen típusú adat van
éppen eltárolva a union példányában. A unionokról [a Rust
referenciában][unions] tudhatsz meg többet.

### Unsafe kód ellenőrzése a Mirivel {#using-miri-to-check-unsafe-code}

Amikor unsafe kódot írsz, érdemes lehet ellenőrizni, hogy amit írtál, valóban
biztonságos és helyes-e. Ennek egyik legjobb módja a Miri, a Rust nem
definiált viselkedést felderítő hivatalos eszköze. Míg a kölcsönzésellenőrző
_statikus_ eszköz, amely fordítási időben dolgozik, a Miri _dinamikus_ eszköz,
amely futásidőben működik. Úgy ellenőrzi a kódodat, hogy lefuttatja a
programodat vagy annak tesztkészletét, és felderíti, ha megsérted azokat a
szabályokat, amelyeket a Rust működéséről ismer.

A Miri használatához a Rust egy nightly buildjére van szükség (erről bővebben
a [G. függelékben: Hogyan készül a Rust, és mi az a „nightly
Rust”?][nightly]<!-- ignore --> olvashatsz). A Rust nightly verzióját és a Miri
eszközt egyaránt telepítheted a `rustup +nightly component add miri` parancs
begépelésével. Ez nem változtatja meg, hogy a projekted a Rust melyik
verzióját használja; csak hozzáadja az eszközt a rendszeredhez, hogy
használhasd, amikor szeretnéd. A Mirit egy projekten a `cargo +nightly miri run`
vagy a `cargo +nightly miri test` begépelésével futtathatod.

Hogy lásd, mennyire hasznos lehet, nézzük meg, mi történik, ha a 20-7.
kódrészleten futtatjuk.

```console
{{#include ../listings/ch20-advanced-features/listing-20-07/output.txt}}
```

A Miri helyesen figyelmeztet arra, hogy egy egész számot mutatóvá alakítunk,
ami problémát jelenthet, de nem tudja eldönteni, hogy valóban van-e probléma,
mert nem tudja, honnan származik a mutató. Ezután a Miri hibát jelez ott, ahol
a 20-7. kódrészletben nem definiált viselkedés van, mert lógó mutatónk van. A
Mirinek köszönhetően most már tudjuk, hogy fennáll a nem definiált viselkedés
kockázata, és elgondolkodhatunk azon, hogyan tehetnénk biztonságossá a kódot.
Bizonyos esetekben a Miri még javaslatokat is tud tenni a hibák javítására.

A Miri nem kap el mindent, amit unsafe kód írásakor elronthatsz. A Miri
dinamikus elemzőeszköz, így csak a ténylegesen lefutó kódban lévő problémákat
kapja el. Ez azt jelenti, hogy jó tesztelési technikákkal együtt kell
használnod, hogy jobban megbízhass a megírt unsafe kódodban. A Miri azt sem
fedi le teljesen, hogy a kódod mi minden módon lehet hibás (unsound).

Másképp fogalmazva: ha a Miri _talál_ egy problémát, akkor tudod, hogy hiba
van, de attól, hogy a Miri _nem_ talál hibát, még lehet probléma. Sok mindent
elkap azonban. Próbáld ki a fejezet többi unsafe kódpéldáján is, és nézd meg,
mit mond!

A Miriről [a GitHub-tárolójában][miri] tudhatsz meg többet.

<!-- Old headings. Do not remove or links may break. -->

<a id="when-to-use-unsafe-code"></a>

### Az unsafe kód helyes használata {#using-unsafe-code-correctly}

Az `unsafe` használata az imént tárgyalt öt szuperképesség valamelyikéhez nem
helytelen, és nem is rosszallandó, de nehezebb helyes `unsafe` kódot írni, mert
a fordító nem tud segíteni a memóriabiztonság fenntartásában. Ha okod van
`unsafe` kódot használni, megteheted, és az explicit `unsafe` annotáció
megkönnyíti a problémák forrásának felkutatását, amikor felmerülnek.
Valahányszor unsafe kódot írsz, a Miri segíthet abban, hogy jobban
megbizonyosodj róla, hogy a megírt kód betartja a Rust szabályait.

Ha sokkal mélyebben szeretnéd megismerni, hogyan dolgozhatsz hatékonyan az
unsafe Rusttal, olvasd el a Rust hivatalos `unsafe`-útmutatóját, a [The
Rustonomicont][nomicon].

[dangling-references]: ch04-02-references-and-borrowing.html#dangling-references
[ABI]: ../reference/items/external-blocks.html#abi
[constants]: ch03-01-variables-and-mutability.html#declaring-constants
[send-and-sync]: ch16-04-extensible-concurrency-sync-and-send.html
[the-slice-type]: ch04-03-slices.html#the-slice-type
[unions]: ../reference/items/unions.html
[miri]: https://github.com/rust-lang/miri
[editions]: appendix-05-editions.html
[nightly]: appendix-07-nightly-rust.html
[nomicon]: https://doc.rust-lang.org/nomicon/
