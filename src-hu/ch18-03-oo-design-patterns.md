## Egy objektumorientált tervezési minta megvalósítása {#implementing-an-object-oriented-design-pattern}

Az _állapot minta (state pattern)_ egy objektumorientált _tervezési minta
(design pattern)_. A minta lényege, hogy meghatározzuk azoknak az állapotoknak
a halmazát, amelyekben egy érték belül lehet. Az állapotokat
_állapotobjektumok (state objects)_ halmaza ábrázolja, és az érték viselkedése
az állapotától függően változik. Egy blogbejegyzést ábrázoló struktúra példáján
fogunk végigmenni, amelynek van egy mezője az állapota tárolására; ez egy
állapotobjektum lesz a „vázlat”, az „ellenőrzés alatt” és a „közzétett”
állapotok halmazából.

Az állapotobjektumok közös funkcionalitással rendelkeznek: Rustban persze
objektumok és öröklődés helyett struktúrákat és traiteket használunk. Minden
állapotobjektum felel a saját viselkedéséért, és azért, hogy mikor kell egy
másik állapotba átváltania. Az az érték, amely az állapotobjektumot tárolja,
semmit sem tud az állapotok eltérő viselkedéséről, sem arról, hogy mikor kell
állapotot váltani.

Az állapot minta használatának előnye, hogy amikor a program üzleti
követelményei megváltoznak, nem kell módosítanunk sem az állapotot tároló
érték kódját, sem az értéket használó kódot. Csak az egyik állapotobjektum
kódját kell frissítenünk, hogy megváltoztassuk a szabályait, esetleg újabb
állapotobjektumokat kell hozzáadnunk.

Először hagyományosabb objektumorientált módon valósítjuk meg az állapot
mintát. Utána egy olyan megközelítést mutatunk, amely Rustban valamivel
természetesebb. Lássunk hozzá, és valósítsunk meg lépésről lépésre egy
blogbejegyzés-kezelő munkafolyamatot az állapot mintával!

A végleges funkcionalitás így fog kinézni:

1. A blogbejegyzés üres vázlatként indul.
1. Amikor a vázlat elkészült, ellenőrzést kérünk a bejegyzésre.
1. Amikor a bejegyzést jóváhagyják, közzéteszik.
1. Csak a közzétett blogbejegyzések adnak vissza kiírható tartalmat, így a
   jóvá nem hagyott bejegyzéseket nem lehet véletlenül közzétenni.

A bejegyzésen megkísérelt minden egyéb változtatásnak hatástalannak kell
lennie. Ha például megpróbálunk jóváhagyni egy vázlat blogbejegyzést, mielőtt
ellenőrzést kértünk volna rá, a bejegyzésnek közzé nem tett vázlatnak kell
maradnia.

<!-- Old headings. Do not remove or links may break. -->

<a id="a-traditional-object-oriented-attempt"></a>

### Kísérlet a hagyományos objektumorientált stílusra {#attempting-traditional-object-oriented-style}

Végtelenül sokféleképpen lehet a kódot felépíteni ugyanannak a problémának a
megoldására, és mindegyik más kompromisszumokkal jár. Ennek a szakasznak a
megvalósítása inkább hagyományos objektumorientált stílusú, amely Rustban is
megírható, de nem használja ki a Rust néhány erősségét. Később egy másik
megoldást is bemutatunk, amely továbbra is az objektumorientált tervezési
mintát használja, de olyan szerkezetű, amely az objektumorientált
tapasztalattal rendelkező programozók számára kevésbé tűnhet ismerősnek. A két
megoldást összehasonlítva megtapasztaljuk, milyen kompromisszumokkal jár, ha a
Rust-kódot másképp tervezzük, mint más nyelvek kódját.

A 18-11. kódrészlet kód formájában mutatja ezt a munkafolyamatot: ez egy
`blog` nevű könyvtár crate-ben megvalósítandó API használatát szemlélteti. Ez a
kód még nem fordul le, mert még nem valósítottuk meg a `blog` crate-et.

<Listing number="18-11" file-name="src/main.rs" caption="Kód, amely a `blog` crate-től elvárt viselkedést szemlélteti">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch18-oop/listing-18-11/src/main.rs:all}}
```

</Listing>

Lehetővé szeretnénk tenni, hogy a felhasználó a `Post::new` segítségével új
vázlat blogbejegyzést hozzon létre. Azt szeretnénk, hogy a blogbejegyzéshez
szöveget lehessen hozzáadni. Ha a jóváhagyás előtt rögtön megpróbáljuk
lekérni a bejegyzés tartalmát, nem szabad szöveget kapnunk, mert a bejegyzés
még vázlat. Szemléltetésként `assert_eq!` hívásokat tettünk a kódba. Kiváló
egységteszt volna erre annak ellenőrzése, hogy egy vázlat blogbejegyzés
`content` metódusa üres sztringet ad vissza, de ehhez a példához nem fogunk
teszteket írni.

Ezután lehetővé szeretnénk tenni, hogy ellenőrzést lehessen kérni a
bejegyzésre, és azt szeretnénk, hogy a `content` üres sztringet adjon vissza,
amíg a bejegyzés az ellenőrzésre vár. Amikor a bejegyzés jóváhagyást kap,
közzé kell tenni, vagyis a `content` meghívásakor a bejegyzés szövegét kell
visszaadni.

Figyeld meg, hogy a crate-ből egyedül a `Post` típussal dolgozunk. Ez a típus
az állapot mintát fogja használni, és egy olyan értéket fog tárolni, amely a
három állapotobjektum egyike lesz – vázlat, ellenőrzés alatt vagy közzétett –,
amelyek a bejegyzés lehetséges állapotait ábrázolják. Az egyik állapotból a
másikba való váltást a `Post` típus belül kezeli. Az állapotok a könyvtárunk
felhasználói által a `Post` példányon meghívott metódusok hatására változnak,
de a felhasználóknak nem kell közvetlenül kezelniük az állapotváltásokat.
Emellett a felhasználók nem hibázhatnak az állapotokkal, például nem tehetnek
közzé egy bejegyzést, mielőtt azt ellenőrizték volna.

<!-- Old headings. Do not remove or links may break. -->

<a id="defining-post-and-creating-a-new-instance-in-the-draft-state"></a>

#### A `Post` definiálása és új példány létrehozása {#defining-post-and-creating-a-new-instance}

Kezdjünk hozzá a könyvtár megvalósításához! Tudjuk, hogy szükségünk van egy
nyilvános `Post` struktúrára, amely valamilyen tartalmat tárol, ezért a
struktúra definíciójával és egy hozzá társított nyilvános `new` függvénnyel
kezdünk, amely létrehoz egy `Post` példányt, ahogy a 18-12. kódrészlet
mutatja. Létrehozunk egy privát `State` traitet is, amely azt a viselkedést
definiálja, amellyel egy `Post` minden állapotobjektumának rendelkeznie kell.

Ezután a `Post` egy `state` nevű privát mezőben, egy `Option<T>`-n belül
`Box<dyn State>` trait objektumot tárol majd, amely az állapotobjektumot
tartalmazza. Hamarosan látni fogod, miért van szükség az `Option<T>`-re.

<Listing number="18-12" file-name="src/lib.rs" caption="Egy `Post` struktúra és egy új `Post` példányt létrehozó `new` függvény definíciója, egy `State` trait és egy `Draft` struktúra">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-12/src/lib.rs}}
```

</Listing>

A `State` trait a különböző bejegyzésállapotok közös viselkedését definiálja.
Az állapotobjektumok a `Draft`, a `PendingReview` és a `Published`, és
mindegyik meg fogja valósítani a `State` traitet. A traitnek egyelőre nincsenek
metódusai, és először csak a `Draft` állapotot definiáljuk, mert ebben az
állapotban szeretnénk, hogy egy bejegyzés induljon.

Amikor új `Post`-ot hozunk létre, a `state` mezőjét egy olyan `Some` értékre
állítjuk, amely egy `Box`-ot tartalmaz. Ez a `Box` a `Draft` struktúra egy új
példányára mutat. Ez biztosítja, hogy valahányszor új `Post` példányt hozunk
létre, az vázlatként induljon. Mivel a `Post` `state` mezője privát, semmilyen
más állapotban nem lehet `Post`-ot létrehozni! A `Post::new` függvényben a
`content` mezőt egy új, üres `String`-re állítjuk.

#### A bejegyzés szöveges tartalmának tárolása {#storing-the-text-of-the-post-content}

A 18-11. kódrészletben láttuk, hogy szeretnénk meghívni egy `add_text` nevű
metódust, és átadni neki egy `&str`-t, amelyet aztán hozzáadunk a blogbejegyzés
szöveges tartalmához. Ezt metódusként valósítjuk meg ahelyett, hogy a
`content` mezőt `pub`-ként tennénk elérhetővé, hogy később megvalósíthassunk
egy metódust, amely szabályozza, hogyan olvasható ki a `content` mező
tartalma. Az `add_text` metódus meglehetősen egyszerű, ezért adjuk hozzá a
18-13. kódrészletben látható megvalósítást az `impl Post` blokkhoz.

<Listing number="18-13" file-name="src/lib.rs" caption="Az `add_text` metódus megvalósítása, amely szöveget ad egy bejegyzés `content` mezőjéhez">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-13/src/lib.rs:here}}
```

</Listing>

Az `add_text` metódus módosítható referenciát vesz át a `self`-re, mert azt a
`Post` példányt módosítjuk, amelyen az `add_text`-et meghívjuk. Ezután
meghívjuk a `push_str` metódust a `content` mezőben lévő `String`-en, és
átadjuk neki a `text` argumentumot, hogy hozzáadjuk a tárolt `content`
tartalomhoz. Ez a viselkedés nem függ a bejegyzés állapotától, így nem része az
állapot mintának. Az `add_text` metódus egyáltalán nem érinti a `state` mezőt,
de része annak a viselkedésnek, amelyet támogatni szeretnénk.

<!-- Old headings. Do not remove or links may break. -->

<a id="ensuring-the-content-of-a-draft-post-is-empty"></a>

#### Annak biztosítása, hogy a vázlat tartalma üres legyen {#ensuring-that-the-content-of-a-draft-post-is-empty}

Még azután is, hogy meghívtuk az `add_text` metódust, és tartalmat adtunk a
bejegyzéshez, azt szeretnénk, hogy a `content` metódus üres sztringszeletet
adjon vissza, mert a bejegyzés még vázlat állapotban van, ahogy a 18-11.
kódrészlet első `assert_eq!` hívása mutatja. Egyelőre valósítsuk meg a
`content` metódust a legegyszerűbb módon, amely teljesíti ezt a követelményt:
mindig üres sztringszeletet ad vissza. Ezt később módosítjuk, amikor
megvalósítjuk, hogy a bejegyzés állapotát meg lehessen változtatni, és így
közzé lehessen tenni. Eddig a bejegyzések csak vázlat állapotban lehetnek,
ezért a bejegyzés tartalmának mindig üresnek kell lennie. A 18-14. kódrészlet
ezt a helyőrző megvalósítást mutatja.

<Listing number="18-14" file-name="src/lib.rs" caption="Helyőrző megvalósítás hozzáadása a `Post` `content` metódusához, amely mindig üres sztringszeletet ad vissza">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-14/src/lib.rs:here}}
```

</Listing>

Ezzel a hozzáadott `content` metódussal a 18-11. kódrészletben az első
`assert_eq!` hívásig minden a szándékunk szerint működik.

<!-- Old headings. Do not remove or links may break. -->

<a id="requesting-a-review-of-the-post-changes-its-state"></a>
<a id="requesting-a-review-changes-the-posts-state"></a>

#### Ellenőrzés kérése, amely megváltoztatja a bejegyzés állapotát {#requesting-a-review-which-changes-the-posts-state}

Ezután hozzá kell adnunk a funkcionalitást, amellyel ellenőrzést kérhetünk egy
bejegyzésre; ennek az állapotot `Draft`-ról `PendingReview`-ra kell
változtatnia. A 18-15. kódrészlet ezt a kódot mutatja.

<Listing number="18-15" file-name="src/lib.rs" caption="A `request_review` metódusok megvalósítása a `Post` típuson és a `State` traitben">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-15/src/lib.rs:here}}
```

</Listing>

A `Post` kap egy `request_review` nevű nyilvános metódust, amely módosítható
referenciát vesz át a `self`-re. Ezután meghívunk egy belső `request_review`
metódust a `Post` aktuális állapotán, és ez a második `request_review` metódus
elfogyasztja az aktuális állapotot, és egy új állapotot ad vissza.

A `request_review` metódust hozzáadjuk a `State` traithez; mostantól minden
típusnak, amely megvalósítja a traitet, meg kell valósítania a
`request_review` metódust is. Figyeld meg, hogy a metódus első paramétere nem
`self`, `&self` vagy `&mut self`, hanem `self: Box<Self>`. Ez a szintaxis azt
jelenti, hogy a metódus csak akkor érvényes, ha egy, a típust tartalmazó
`Box`-on hívjuk meg. Ez a szintaxis átveszi a `Box<Self>` tulajdonjogát, és
érvényteleníti a régi állapotot, így a `Post` állapotértéke új állapottá
alakulhat.

A régi állapot elfogyasztásához a `request_review` metódusnak át kell vennie az
állapotérték tulajdonjogát. Itt jön képbe a `Post` `state` mezőjében lévő
`Option`: meghívjuk a `take` metódust, hogy kivegyük a `Some` értéket a `state`
mezőből, és egy `None`-t hagyjunk a helyén, mert a Rust nem engedi, hogy egy
struktúrában kitöltetlen mezők legyenek. Így kimozgathatjuk a `state` értéket a
`Post`-ból ahelyett, hogy kölcsönöznénk. Ezután a bejegyzés `state` értékét
ennek a műveletnek az eredményére állítjuk.

A `state` értékét ideiglenesen `None`-ra kell állítanunk, ahelyett hogy
közvetlenül, például `self.state = self.state.request_review();` kóddal
állítanánk be, hogy megkapjuk a `state` érték tulajdonjogát. Ez biztosítja,
hogy a `Post` ne használhassa a régi `state` értéket azután, hogy új állapottá
alakítottuk.

A `Draft` `request_review` metódusa egy új `PendingReview` struktúra új,
dobozba csomagolt példányát adja vissza; ez az az állapot, amikor egy bejegyzés
ellenőrzésre vár. A `PendingReview` struktúra is megvalósítja a
`request_review` metódust, de semmilyen átalakítást nem végez. Ehelyett saját
magát adja vissza, mert ha egy már `PendingReview` állapotban lévő bejegyzésre
kérünk ellenőrzést, annak `PendingReview` állapotban kell maradnia.

Most már kezdjük látni az állapot minta előnyeit: a `Post` `request_review`
metódusa ugyanaz, bármi legyen is a `state` értéke. Minden állapot a saját
szabályaiért felel.

A `Post` `content` metódusát változatlanul hagyjuk, továbbra is üres
sztringszeletet ad vissza. Most már a `Draft` állapot mellett `PendingReview`
állapotban is lehet egy `Post`, de a `PendingReview` állapotban is ugyanezt a
viselkedést szeretnénk. A 18-11. kódrészlet most már a második `assert_eq!`
hívásig működik!

<!-- Old headings. Do not remove or links may break. -->

<a id="adding-the-approve-method-that-changes-the-behavior-of-content"></a>
<a id="adding-approve-to-change-the-behavior-of-content"></a>

#### Az `approve` hozzáadása a `content` viselkedésének megváltoztatásához {#adding-approve-to-change-contents-behavior}

Az `approve` metódus hasonló lesz a `request_review` metódushoz: a `state`
értékét arra az értékre állítja, amelyet az aktuális állapot szerint akkor kell
felvennie, amikor az adott állapotot jóváhagyják, ahogy a 18-16. kódrészlet
mutatja.

<Listing number="18-16" file-name="src/lib.rs" caption="Az `approve` metódus megvalósítása a `Post` típuson és a `State` traitben">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-16/src/lib.rs:here}}
```

</Listing>

Hozzáadjuk az `approve` metódust a `State` traithez, és hozzáadunk egy új,
`State`-et megvalósító struktúrát, a `Published` állapotot.

A `PendingReview` `request_review` metódusának működéséhez hasonlóan, ha egy
`Draft`-on hívjuk meg az `approve` metódust, annak nem lesz hatása, mert az
`approve` a `self`-et adja vissza. Ha a `PendingReview`-n hívjuk meg az
`approve` metódust, az a `Published` struktúra egy új, dobozba csomagolt
példányát adja vissza. A `Published` struktúra megvalósítja a `State` traitet,
és a `request_review` és az `approve` metódus is saját magát adja vissza,
mert ezekben az esetekben a bejegyzésnek `Published` állapotban kell maradnia.

Most frissítenünk kell a `Post` `content` metódusát. Azt szeretnénk, hogy a
`content` által visszaadott érték a `Post` aktuális állapotától függjön, ezért
a `Post` a `state` mezőjén definiált `content` metódusra fogja delegálni a
feladatot, ahogy a 18-17. kódrészlet mutatja.

<Listing number="18-17" file-name="src/lib.rs" caption="A `Post` `content` metódusának frissítése, hogy a `State` egy `content` metódusára delegáljon">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch18-oop/listing-18-17/src/lib.rs:here}}
```

</Listing>

Mivel az a cél, hogy ezek a szabályok mind a `State`-et megvalósító
struktúrákon belül legyenek, a `state` mezőben lévő értéken meghívunk egy
`content` metódust, és argumentumként átadjuk neki a bejegyzéspéldányt (vagyis
a `self`-et). Ezután visszaadjuk azt az értéket, amelyet a `state` értéken
meghívott `content` metódus visszaad.

Az `Option`-ön meghívjuk az `as_ref` metódust, mert az `Option`-ön belüli
értékre mutató referenciát szeretnénk, nem pedig az érték tulajdonjogát. Mivel
a `state` típusa `Option<Box<dyn State>>`, az `as_ref` meghívásakor egy
`Option<&Box<dyn State>>` értéket kapunk vissza. Ha nem hívnánk meg az
`as_ref`-et, hibát kapnánk, mert a `state` nem mozgatható ki a függvény
paraméteréből kölcsönzött `&self`-ből.

Ezután meghívjuk az `unwrap` metódust, amelyről tudjuk, hogy soha nem fog
pánikolni, mert tudjuk, hogy a `Post` metódusai biztosítják, hogy a `state`
mindig `Some` értéket tartalmazzon, amikor ezek a metódusok befejeződnek. Ez
az egyik olyan eset, amelyről a 9. fejezet [„Amikor több információd van, mint
a fordítónak”][more-info-than-rustc]<!-- ignore --> szakaszában beszéltünk:
tudjuk, hogy `None` érték soha nem fordulhat elő, bár a fordító ezt nem képes
belátni.

Ezen a ponton, amikor a `&Box<dyn State>`-en meghívjuk a `content` metódust, a
deref-konverzió érvénybe lép a `&`-en és a `Box`-on, így a `content` metódust
végül a `State` traitet megvalósító típuson hívjuk meg. Ez azt jelenti, hogy a
`content` metódust hozzá kell adnunk a `State` trait definíciójához, és ott
helyezzük el azt a logikát, amely az aktuális állapottól függően eldönti, milyen
tartalmat adjunk vissza, ahogy a 18-18. kódrészlet mutatja.

<Listing number="18-18" file-name="src/lib.rs" caption="A `content` metódus hozzáadása a `State` traithez">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-18/src/lib.rs:here}}
```

</Listing>

A `content` metódushoz alapértelmezett megvalósítást adunk, amely üres
sztringszeletet ad vissza. Így a `content` metódust nem kell megvalósítanunk a
`Draft` és a `PendingReview` struktúrán. A `Published` struktúra felülírja a
`content` metódust, és a `post.content` értékét adja vissza. Bár kényelmes, ha
a `State` `content` metódusa határozza meg a `Post` tartalmát, ez elmossa a
határt a `State` és a `Post` felelőssége között.

Figyeld meg, hogy ehhez a metódushoz élettartam-annotációkra van szükségünk,
ahogy azt a 10. fejezetben tárgyaltuk. Egy `post` referenciát veszünk át
argumentumként, és ennek a `post`-nak egy részére mutató referenciát adunk
vissza, így a visszaadott referencia élettartama a `post` argumentum
élettartamához kapcsolódik.

És kész vagyunk – a 18-11. kódrészlet most már teljes egészében működik!
Megvalósítottuk az állapot mintát a blogbejegyzés-kezelő munkafolyamat
szabályaival. A szabályokhoz kapcsolódó logika az állapotobjektumokban
található, ahelyett hogy szét lenne szórva a `Post`-ban.

> ### Miért nem enum? {#why-not-an-enum}
>
> Talán elgondolkodtál azon, miért nem egy olyan enumot használtunk, amelynek
> változatai a bejegyzés lehetséges állapotai. Ez természetesen lehetséges
> megoldás; próbáld ki, és hasonlítsd össze az eredményeket, hogy lásd, melyik
> tetszik jobban! Az enum használatának egyik hátránya, hogy minden helyen, ahol
> az enum értékét ellenőrizzük, szükség lesz egy `match` kifejezésre vagy
> hasonlóra, amely minden lehetséges változatot kezel. Ez több ismétlődéssel
> járhat, mint ez a trait objektumos megoldás.

<!-- Old headings. Do not remove or links may break. -->

<a id="trade-offs-of-the-state-pattern"></a>

#### Az állapot minta értékelése {#evaluating-the-state-pattern}

Megmutattuk, hogy a Rust képes megvalósítani az objektumorientált állapot
mintát, hogy egységbe zárja azokat a különféle viselkedéseket, amelyekkel egy
bejegyzésnek az egyes állapotokban rendelkeznie kell. A `Post` metódusai semmit
sem tudnak a különféle viselkedésekről. A kód szervezésének köszönhetően csak
egyetlen helyen kell keresgélnünk, hogy megtudjuk, milyen módokon viselkedhet
egy közzétett bejegyzés: a `State` trait `Published` struktúrán lévő
megvalósításában.

Ha olyan alternatív megvalósítást készítenénk, amely nem használja az állapot
mintát, ehelyett `match` kifejezéseket használhatnánk a `Post` metódusaiban,
vagy akár a `main` kódjában, amelyek ellenőrzik a bejegyzés állapotát, és azokon
a helyeken változtatják meg a viselkedést. Ez azt jelentené, hogy több helyen
kellene keresgélnünk ahhoz, hogy megértsük, mivel jár, ha egy bejegyzés
közzétett állapotban van.

Az állapot mintával a `Post` metódusainak és azoknak a helyeknek, ahol a
`Post`-ot használjuk, nincs szükségük `match` kifejezésekre, és egy új állapot
hozzáadásához csak egy új struktúrát kellene létrehoznunk, és egyetlen helyen,
ezen az egy struktúrán megvalósítanunk a trait metódusait.

Az állapot mintát használó megvalósítás könnyen bővíthető további
funkcionalitással. Hogy lásd, milyen egyszerű az állapot mintát használó kód
karbantartása, próbálj ki néhányat az alábbi javaslatok közül:

- Adj hozzá egy `reject` metódust, amely a bejegyzés állapotát `PendingReview`
  állapotból visszaállítja `Draft` állapotba.
- Legyen szükség két `approve` hívásra, mielőtt az állapot `Published`-ra
  változhat.
- A felhasználók csak akkor adhassanak szöveges tartalmat a bejegyzéshez, ha az
  `Draft` állapotban van. Tipp: az állapotobjektum feleljen azért, ami a
  tartalommal kapcsolatban változhat, de ne ő feleljen a `Post` módosításáért.

Az állapot minta egyik hátránya, hogy mivel az állapotok valósítják meg az
állapotok közötti átmeneteket, egyes állapotok összekapcsolódnak egymással. Ha
a `PendingReview` és a `Published` közé egy újabb állapotot, például
`Scheduled`-et vennénk fel, a `PendingReview` kódját úgy kellene módosítanunk,
hogy ehelyett a `Scheduled` állapotba váltson. Kevesebb munkával járna, ha a
`PendingReview`-n nem kellene változtatni egy új állapot hozzáadásakor, ez
azonban egy másik tervezési mintára való áttérést jelentene.

Egy másik hátrány, hogy a logika egy részét megdupláztuk. Az ismétlődés egy
részének kiküszöbölésére megpróbálhatnánk a `State` traitben a `self`-et
visszaadó alapértelmezett megvalósítást adni a `request_review` és az
`approve` metódusnak. Ez azonban nem működne: amikor a `State`-et trait
objektumként használjuk, a trait nem tudja, pontosan mi lesz a konkrét `self`,
így a visszatérési típus fordítási időben nem ismert. (Ez az egyik korábban
említett dyn-kompatibilitási szabály.)

További ismétlődést jelent a `Post` `request_review` és `approve` metódusának
hasonló megvalósítása. Mindkét metódus az `Option::take`-et használja a `Post`
`state` mezőjén, és ha a `state` értéke `Some`, a becsomagolt érték ugyanilyen
nevű metódusának megvalósítására delegálnak, majd a `state` mező új értékét az
eredményre állítják. Ha a `Post`-nak sok ilyen mintát követő metódusa volna,
fontolóra vehetnénk egy makró definiálását az ismétlődés kiküszöbölésére (lásd
a 20. fejezet [„Makrók”][macros]<!-- ignore --> szakaszát).

Azzal, hogy az állapot mintát pontosan úgy valósítjuk meg, ahogy az
objektumorientált nyelvekre definiálták, nem használjuk ki annyira a Rust
erősségeit, amennyire lehetne. Nézzük meg, milyen változtatásokat tehetünk a
`blog` crate-ben, amelyekkel az érvénytelen állapotok és átmenetek fordítási
idejű hibákká válnak.

### Állapotok és viselkedés kódolása típusokként {#encoding-states-and-behavior-as-types}

Megmutatjuk, hogyan gondolhatjuk újra az állapot mintát, hogy más
kompromisszumokat kapjunk. Ahelyett, hogy az állapotokat és az átmeneteket
teljesen egységbe zárnánk, hogy a külső kód semmit se tudjon róluk, az
állapotokat különböző típusokba kódoljuk. Ennek következtében a Rust
típusellenőrző rendszere fordítási hibával megakadályozza, hogy vázlat
bejegyzéseket használjunk ott, ahol csak közzétett bejegyzések megengedettek.

Vegyük a 18-11. kódrészletben lévő `main` első részét:

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch18-oop/listing-18-11/src/main.rs:here}}
```

</Listing>

Továbbra is lehetővé tesszük új, vázlat állapotú bejegyzések létrehozását a
`Post::new` segítségével, és azt, hogy szöveget adjunk a bejegyzés
tartalmához. Ahelyett azonban, hogy a vázlat bejegyzésnek olyan `content`
metódusa lenne, amely üres sztringet ad vissza, úgy alakítjuk ki, hogy a
vázlat bejegyzéseknek egyáltalán ne legyen `content` metódusuk. Így ha
megpróbáljuk lekérni egy vázlat bejegyzés tartalmát, fordítási hibát kapunk,
amely közli, hogy a metódus nem létezik. Ennek eredményeként lehetetlen lesz,
hogy éles környezetben véletlenül megjelenítsük egy vázlat bejegyzés
tartalmát, mert az ilyen kód le sem fordul. A 18-19. kódrészlet egy `Post`
struktúra és egy `DraftPost` struktúra definícióját, valamint mindkettő
metódusait mutatja.

<Listing number="18-19" file-name="src/lib.rs" caption="Egy `content` metódussal rendelkező `Post` és egy `content` metódus nélküli `DraftPost`">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-19/src/lib.rs}}
```

</Listing>

A `Post` és a `DraftPost` struktúrának is van egy privát `content` mezője,
amely a blogbejegyzés szövegét tárolja. A struktúráknak már nincs `state`
mezőjük, mert az állapot kódolását a struktúrák típusaiba helyezzük át. A
`Post` struktúra egy közzétett bejegyzést fog ábrázolni, és van egy `content`
metódusa, amely visszaadja a `content` értékét.

Továbbra is van `Post::new` függvényünk, de ez nem `Post` példányt ad vissza,
hanem `DraftPost` példányt. Mivel a `content` privát, és nincs olyan függvény,
amely `Post`-ot adna vissza, jelenleg nem lehet `Post` példányt létrehozni.

A `DraftPost` struktúrának van `add_text` metódusa, így a korábbiakhoz
hasonlóan szöveget adhatunk a `content` mezőhöz, de figyeld meg, hogy a
`DraftPost` típuson nincs definiálva `content` metódus! A program tehát most
már biztosítja, hogy minden bejegyzés vázlatként induljon, és a vázlat
bejegyzések tartalma ne legyen megjeleníthető. Ezeknek a megkötéseknek a
megkerülésére tett minden kísérlet fordítási hibát eredményez.

<!-- Old headings. Do not remove or links may break. -->

<a id="implementing-transitions-as-transformations-into-different-types"></a>

Hogyan kapunk tehát közzétett bejegyzést? Ki szeretnénk kényszeríteni azt a
szabályt, hogy egy vázlat bejegyzést ellenőrizni és jóváhagyni kell, mielőtt
közzé lehetne tenni. Az ellenőrzésre váró állapotban lévő bejegyzés továbbra
sem jeleníthet meg semmilyen tartalmat. Valósítsuk meg ezeket a megkötéseket
egy újabb struktúra, a `PendingReviewPost` hozzáadásával: a `DraftPost`
típuson definiálunk egy `request_review` metódust, amely `PendingReviewPost`-ot
ad vissza, a `PendingReviewPost` típuson pedig egy `approve` metódust, amely
`Post`-ot ad vissza, ahogy a 18-20. kódrészlet mutatja.

<Listing number="18-20" file-name="src/lib.rs" caption="Egy `PendingReviewPost`, amely a `DraftPost` `request_review` metódusának meghívásával jön létre, és egy `approve` metódus, amely a `PendingReviewPost`-ot közzétett `Post`-tá alakítja">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-20/src/lib.rs:here}}
```

</Listing>

A `request_review` és az `approve` metódus átveszi a `self` tulajdonjogát, így
elfogyasztja a `DraftPost`, illetve a `PendingReviewPost` példányt, és
`PendingReviewPost`-tá, illetve közzétett `Post`-tá alakítja őket. Így nem
maradnak meg `DraftPost` példányok azután, hogy meghívtuk rajtuk a
`request_review` metódust, és így tovább. A `PendingReviewPost` struktúrán
nincs definiálva `content` metódus, így a tartalmának kiolvasására tett
kísérlet fordítási hibát eredményez, ugyanúgy, mint a `DraftPost` esetében.
Mivel a definiált `content` metódussal rendelkező, közzétett `Post` példányt
csak úgy kaphatjuk meg, ha egy `PendingReviewPost`-on meghívjuk az `approve`
metódust, `PendingReviewPost`-ot pedig csak úgy kaphatunk, ha egy
`DraftPost`-on meghívjuk a `request_review` metódust, a blogbejegyzés-kezelő
munkafolyamatot most már a típusrendszerbe kódoltuk.

A `main`-en azonban néhány apró változtatást is végre kell hajtanunk. A
`request_review` és az `approve` metódus új példányokat ad vissza, ahelyett
hogy módosítaná azt a struktúrát, amelyen meghívjuk őket, ezért további
`let post =` árnyékoló értékadásokat kell hozzáadnunk a visszaadott példányok
megőrzéséhez. Azokat az állításokat sem tarthatjuk meg, amelyek szerint a
vázlat és az ellenőrzésre váró bejegyzések tartalma üres sztring, de nincs is
rájuk szükségünk: az olyan kód, amely ezekben az állapotokban lévő bejegyzések
tartalmát próbálja használni, már le sem fordul. A `main` frissített kódját a
18-21. kódrészlet mutatja.

<Listing number="18-21" file-name="src/main.rs" caption="A `main` módosításai a blogbejegyzés-kezelő munkafolyamat új megvalósításának használatához">

```rust,ignore
{{#rustdoc_include ../listings/ch18-oop/listing-18-21/src/main.rs}}
```

</Listing>

A `post` újbóli értékadásához szükséges változtatások a `main`-ben azt
jelentik, hogy ez a megvalósítás már nem egészen követi az objektumorientált
állapot mintát: az állapotok közötti átalakítások már nincsenek teljesen a
`Post` megvalósításába zárva. Ugyanakkor azt nyertük, hogy az érvénytelen
állapotok most már lehetetlenek a típusrendszernek és a fordítási időben
végzett típusellenőrzésnek köszönhetően! Ez biztosítja, hogy bizonyos hibák,
például egy közzé nem tett bejegyzés tartalmának megjelenítése, még azelőtt
kiderüljenek, hogy éles környezetbe kerülnének.

Próbáld ki az ennek a szakasznak az elején javasolt feladatokat a `blog`
crate-en, abban az állapotában, ahogy a 18-21. kódrészlet után van, hogy lásd,
mit gondolsz a kód ezen változatának tervezéséről. Figyeld meg, hogy ebben a
tervben néhány feladat talán már eleve teljesül.

Láttuk, hogy bár a Rust képes objektumorientált tervezési minták
megvalósítására, más minták is elérhetők benne, például az állapot kódolása a
típusrendszerbe. Ezek a minták más-más kompromisszumokkal járnak. Bár lehet,
hogy nagyon jól ismered az objektumorientált mintákat, ha a problémát úgy
gondolod újra, hogy kihasználd a Rust nyelvi elemeit, az előnyökkel járhat,
például bizonyos hibák már fordítási időben kiszűrhetők. Az objektumorientált
minták nem mindig jelentik a legjobb megoldást Rustban bizonyos nyelvi elemek
miatt, például a tulajdonjog miatt, amely az objektumorientált nyelvekben
nincs meg.

## Összefoglalás {#summary}

Függetlenül attól, hogy e fejezet elolvasása után objektumorientált nyelvnek
tartod-e a Rustot, most már tudod, hogy trait objektumokkal bizonyos
objektumorientált elemekhez juthatsz Rustban. A dinamikus hívásfeloldás némi
rugalmasságot adhat a kódodnak, cserébe egy kevés futásidejű teljesítményért.
Ezt a rugalmasságot felhasználhatod olyan objektumorientált minták
megvalósítására, amelyek javíthatják a kódod karbantarthatóságát. A Rust más
nyelvi elemekkel is rendelkezik, például a tulajdonjoggal, amelyek az
objektumorientált nyelvekben nincsenek meg. Egy objektumorientált minta nem
mindig a legjobb módja annak, hogy kihasználd a Rust erősségeit, de elérhető
lehetőség.

A következő fejezetben a mintákkal foglalkozunk, amelyek a Rust egy másik,
nagy rugalmasságot biztosító nyelvi elemét jelentik. A könyvben már röviden
találkoztunk velük, de még nem láttuk minden képességüket. Vágjunk bele!

[more-info-than-rustc]: ch09-03-to-panic-or-not-to-panic.html#cases-in-which-you-have-more-information-than-the-compiler
[macros]: ch20-05-macros.html#macros
