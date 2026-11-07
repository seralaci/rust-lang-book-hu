<!-- Old headings. Do not remove or links may break. -->

<a id="traits-defining-shared-behavior"></a>

## Közös viselkedés definiálása traitekkel {#defining-shared-behavior-with-traits}

Egy _trait_ azt a funkcionalitást definiálja, amellyel egy adott típus
rendelkezik, és amelyet más típusokkal is megoszthat. A traitekkel absztrakt
módon definiálhatunk közös viselkedést. _Trait-korlátokkal (trait bounds)_
megadhatjuk, hogy egy generikus típus bármilyen olyan típus lehet, amely
bizonyos viselkedéssel rendelkezik.

> Megjegyzés: A traitek hasonlítanak ahhoz a nyelvi elemhez, amelyet más
> nyelvekben gyakran _interfészeknek (interfaces)_ neveznek, bár van néhány
> különbség.

### Trait definiálása {#defining-a-trait}

Egy típus viselkedését azok a metódusok alkotják, amelyeket meghívhatunk rajta.
Különböző típusok akkor osztoznak ugyanazon a viselkedésen, ha mindegyikükön
ugyanazokat a metódusokat hívhatjuk meg. A traitdefiníciókkal
metódusszignatúrákat csoportosíthatunk, hogy meghatározzuk az egy bizonyos cél
eléréséhez szükséges viselkedések halmazát.

Tegyük fel például, hogy több struktúránk van, amelyek különféle fajtájú és
mennyiségű szöveget tárolnak: egy `NewsArticle` struktúra, amely egy adott
helyszínről beküldött hírt tárol, és egy `SocialPost`, amely legfeljebb 280
karakterből állhat, és olyan metaadatokkal rendelkezik, amelyek jelzik, hogy új
bejegyzésről, megosztásról vagy egy másik bejegyzésre adott válaszról van-e
szó.

Egy `aggregator` nevű médiagyűjtő könyvtár crate-et szeretnénk készíteni,
amely összefoglalókat tud megjeleníteni a `NewsArticle` vagy `SocialPost`
példányokban tárolt adatokról. Ehhez minden típustól egy összefoglalóra van
szükségünk, amelyet úgy kérünk le, hogy egy példányon meghívjuk a `summarize`
metódust. A 10-12. kódrészlet egy nyilvános `Summary` trait definícióját
mutatja, amely ezt a viselkedést fejezi ki.

<Listing number="10-12" file-name="src/lib.rs" caption="Egy `Summary` trait, amely a `summarize` metódus által biztosított viselkedésből áll">

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-12/src/lib.rs}}
```

</Listing>

Itt a `trait` kulcsszóval, majd a trait nevével – ebben az esetben `Summary` –
deklarálunk egy traitet. A traitet `pub`-ként is deklaráljuk, hogy az erre a
crate-re épülő crate-ek is használhassák, ahogy néhány példában majd látni
fogjuk. A kapcsos zárójeleken belül deklaráljuk azokat a
metódusszignatúrákat, amelyek az ezt a traitet megvalósító típusok
viselkedését írják le; ebben az esetben ez az `fn summarize(&self) -> String`.

A metódusszignatúra után kapcsos zárójelek közötti megvalósítás helyett
pontosvesszőt írunk. Minden típusnak, amely megvalósítja ezt a traitet, saját
viselkedést kell biztosítania a metódus törzséhez. A fordító kikényszeríti, hogy
minden típusnak, amely rendelkezik a `Summary` traittel, legyen pontosan ezzel
a szignatúrával definiált `summarize` metódusa.

Egy trait törzsében több metódus is lehet: a metódusszignatúrák soronként
egyesével szerepelnek, és minden sor pontosvesszővel végződik.

### Trait megvalósítása egy típuson {#implementing-a-trait-on-a-type}

Most, hogy definiáltuk a `Summary` trait metódusainak kívánt szignatúráit,
megvalósíthatjuk a traitet a médiagyűjtőnk típusain. A 10-13. kódrészlet a
`Summary` trait egy megvalósítását mutatja a `NewsArticle` struktúrán, amely a
főcímből, a szerzőből és a helyszínből állítja elő a `summarize` visszatérési
értékét. A `SocialPost` struktúránál a `summarize` a felhasználónevet adja
vissza, majd a bejegyzés teljes szövegét, feltételezve, hogy a bejegyzés
tartalma eleve legfeljebb 280 karakter.

<Listing number="10-13" file-name="src/lib.rs" caption="A `Summary` trait megvalósítása a `NewsArticle` és a `SocialPost` típuson">

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-13/src/lib.rs:here}}
```

</Listing>

Egy trait megvalósítása egy típuson hasonló a szokásos metódusok
megvalósításához. A különbség az, hogy az `impl` után a megvalósítani kívánt
trait nevét írjuk, majd a `for` kulcsszót, végül annak a típusnak a nevét,
amelyre a traitet meg akarjuk valósítani. Az `impl` blokkon belül a
traitdefinícióban definiált metódusszignatúrákat írjuk. Az egyes szignatúrák
után pontosvessző helyett kapcsos zárójeleket használunk, és a metódus törzsét
azzal a konkrét viselkedéssel töltjük ki, amelyet a trait metódusaitól az adott
típusnál várunk.

Most, hogy a könyvtár megvalósította a `Summary` traitet a `NewsArticle`-ön és
a `SocialPost`-on, a crate felhasználói ugyanúgy hívhatják meg a trait
metódusait a `NewsArticle` és a `SocialPost` példányain, ahogy a szokásos
metódusokat. Az egyetlen különbség, hogy a felhasználónak a típusok mellett a
traitet is hatókörbe kell hoznia. Íme egy példa arra, hogyan használhatná egy
bináris crate az `aggregator` könyvtár crate-ünket:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-01-calling-trait-method/src/main.rs}}
```

Ez a kód a következőt írja ki: `1 new post: horse_ebooks: of course, as you
probably already know, people`.

Az `aggregator` crate-re épülő más crate-ek is hatókörbe hozhatják a `Summary`
traitet, hogy a saját típusaikon megvalósítsák a `Summary`-t. Egy fontos
megkötés, hogy egy traitet csak akkor valósíthatunk meg egy típuson, ha a trait
vagy a típus (vagy mindkettő) a saját crate-ünkben van definiálva. Az
`aggregator` crate funkcionalitásának részeként például megvalósíthatunk
standard könyvtárbeli traiteket, mint a `Display`, egy saját típuson, mint a
`SocialPost`, mert a `SocialPost` típus az `aggregator` crate-ünkben van
definiálva. Az `aggregator` crate-ünkben a `Summary`-t is megvalósíthatjuk a
`Vec<T>`-n, mert a `Summary` trait az `aggregator` crate-ünkben van
definiálva.

Külső traiteket viszont nem valósíthatunk meg külső típusokon. Az `aggregator`
crate-ünkben például nem valósíthatjuk meg a `Display` traitet a `Vec<T>`-n,
mert a `Display` és a `Vec<T>` egyaránt a standard könyvtárban van definiálva,
nem pedig az `aggregator` crate-ünkben. Ez a megkötés a _koherencia
(coherence)_ nevű tulajdonság része, pontosabban az _árvaszabályé (orphan
rule)_, amely azért kapta ezt a nevet, mert a szülőtípus nincs jelen. Ez a
szabály biztosítja, hogy mások kódja ne tehesse tönkre a te kódodat, és
fordítva. A szabály nélkül két crate is megvalósíthatná ugyanazt a traitet
ugyanarra a típusra, és a Rust nem tudná, melyik megvalósítást használja.

<!-- Old headings. Do not remove or links may break. -->

<a id="default-implementations"></a>

### Alapértelmezett megvalósítások használata {#using-default-implementations}

Néha hasznos, ha egy trait néhány vagy akár összes metódusának van
alapértelmezett viselkedése, ahelyett hogy minden típuson minden metódus
megvalósítását megkövetelnénk. Így amikor a traitet egy adott típuson
megvalósítjuk, minden metódus alapértelmezett viselkedését megtarthatjuk vagy
felülírhatjuk.

A 10-14. kódrészletben a `Summary` trait `summarize` metódusához egy
alapértelmezett sztringet adunk meg, ahelyett hogy csak a metódus szignatúráját
definiálnánk, ahogy a 10-12. kódrészletben tettük.

<Listing number="10-14" file-name="src/lib.rs" caption="Egy `Summary` trait definiálása a `summarize` metódus alapértelmezett megvalósításával">

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-14/src/lib.rs:here}}
```

</Listing>

Ha a `NewsArticle` példányainak összefoglalásához az alapértelmezett
megvalósítást akarjuk használni, egy üres `impl` blokkot adunk meg:
`impl Summary for NewsArticle {}`.

Bár a `summarize` metódust már nem közvetlenül a `NewsArticle`-ön definiáljuk,
adtunk egy alapértelmezett megvalósítást, és megadtuk, hogy a `NewsArticle`
megvalósítja a `Summary` traitet. Ennek eredményeként a `NewsArticle` egy
példányán továbbra is meghívhatjuk a `summarize` metódust, így:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-02-calling-default-impl/src/main.rs:here}}
```

Ez a kód a következőt írja ki: `New article available! (Read more...)`.

Az alapértelmezett megvalósítás létrehozása miatt semmit sem kell
megváltoztatnunk a `Summary` 10-13. kódrészletbeli, `SocialPost`-on lévő
megvalósításán. Ennek az az oka, hogy egy alapértelmezett megvalósítás
felülírásának szintaxisa ugyanaz, mint egy alapértelmezett megvalósítással nem
rendelkező traitmetódus megvalósításáé.

Az alapértelmezett megvalósítások ugyanannak a traitnek más metódusait is
meghívhatják, még akkor is, ha azoknak a metódusoknak nincs alapértelmezett
megvalósításuk. Így egy trait sok hasznos funkciót nyújthat, miközben a
megvalósítóktól csak egy kis részük megadását követeli meg. Definiálhatnánk
például úgy a `Summary` traitet, hogy legyen egy `summarize_author` metódusa,
amelynek a megvalósítása kötelező, majd definiálhatnánk egy `summarize`
metódust, amelynek alapértelmezett megvalósítása meghívja a `summarize_author`
metódust:

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-03-default-impl-calls-other-methods/src/lib.rs:here}}
```

A `Summary` ezen változatának használatához csak a `summarize_author`-t kell
definiálnunk, amikor a traitet egy típuson megvalósítjuk:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-03-default-impl-calls-other-methods/src/lib.rs:impl}}
```

Miután definiáltuk a `summarize_author`-t, meghívhatjuk a `summarize`-t a
`SocialPost` struktúra példányain, és a `summarize` alapértelmezett
megvalósítása az általunk megadott `summarize_author` definíciót hívja meg.
Mivel megvalósítottuk a `summarize_author`-t, a `Summary` trait megadta nekünk
a `summarize` metódus viselkedését anélkül, hogy további kódot kellett volna
írnunk. Ez így néz ki:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-03-default-impl-calls-other-methods/src/main.rs:here}}
```

Ez a kód a következőt írja ki: `1 new post: (Read more from @horse_ebooks...)`.

Figyelj arra, hogy egy metódus felülíró megvalósításából nem lehet meghívni
ugyanannak a metódusnak az alapértelmezett megvalósítását.

<!-- Old headings. Do not remove or links may break. -->

<a id="traits-as-parameters"></a>

### Traitek használata paraméterként {#using-traits-as-parameters}

Most, hogy tudod, hogyan kell traiteket definiálni és megvalósítani,
megnézhetjük, hogyan definiálhatunk traitek segítségével olyan függvényeket,
amelyek sokféle típust elfogadnak. A 10-13. kódrészletben a `NewsArticle` és a
`SocialPost` típuson megvalósított `Summary` traittel definiálunk egy `notify`
függvényt, amely meghívja a `summarize` metódust az `item` paraméterén, amely
valamilyen, a `Summary` traitet megvalósító típusú. Ehhez az `impl Trait`
szintaxist használjuk, így:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-04-traits-as-parameters/src/lib.rs:here}}
```

Az `item` paraméternél konkrét típus helyett az `impl` kulcsszót és a trait
nevét adjuk meg. Ez a paraméter bármilyen típust elfogad, amely megvalósítja a
megadott traitet. A `notify` törzsében az `item`-en a `Summary` trait bármely
metódusát meghívhatjuk, például a `summarize`-t. A `notify`-t meghívhatjuk, és
átadhatjuk neki a `NewsArticle` vagy a `SocialPost` bármely példányát. Az a
kód, amely bármilyen más típussal, például `String`-gel vagy `i32`-vel hívja
meg a függvényt, nem fordul le, mert ezek a típusok nem valósítják meg a
`Summary`-t.

<!-- Old headings. Do not remove or links may break. -->

<a id="fixing-the-largest-function-with-trait-bounds"></a>

#### A trait-korlát szintaxisa {#trait-bound-syntax}

Az `impl Trait` szintaxis egyszerű esetekben jól működik, de valójában csak
szintaktikai cukor egy hosszabb formához, amelyet _trait-korlátnak (trait
bound)_ nevezünk; így néz ki:

```rust,ignore
pub fn notify<T: Summary>(item: &T) {
    println!("Breaking news! {}", item.summarize());
}
```

Ez a hosszabb forma egyenértékű az előző szakasz példájával, csak bőbeszédűbb.
A trait-korlátokat a generikus típusparaméter deklarációjánál, kettőspont után
és csúcsos zárójeleken belül adjuk meg.

Az `impl Trait` szintaxis kényelmes, és egyszerű esetekben tömörebb kódot
eredményez, a teljesebb trait-korlát szintaxis viszont más esetekben
összetettebb dolgokat is ki tud fejezni. Lehet például két paraméterünk, amely
megvalósítja a `Summary`-t. Ez az `impl Trait` szintaxissal így néz ki:

```rust,ignore
pub fn notify(item1: &impl Summary, item2: &impl Summary) {
```

Az `impl Trait` használata akkor megfelelő, ha azt szeretnénk, hogy ez a
függvény megengedje, hogy az `item1` és az `item2` különböző típusú legyen
(amennyiben mindkét típus megvalósítja a `Summary`-t). Ha viszont azt akarjuk
kikényszeríteni, hogy a két paraméter azonos típusú legyen, trait-korlátot kell
használnunk, így:

```rust,ignore
pub fn notify<T: Summary>(item1: &T, item2: &T) {
```

Az `item1` és az `item2` paraméter típusaként megadott `T` generikus típus úgy
korlátozza a függvényt, hogy az `item1` és az `item2` argumentumaként átadott
értékek konkrét típusának meg kell egyeznie.

<!-- Old headings. Do not remove or links may break. -->

<a id="specifying-multiple-trait-bounds-with-the--syntax"></a>

#### Több trait-korlát a `+` szintaxissal {#multiple-trait-bounds-with-the--syntax}

Több trait-korlátot is megadhatunk. Tegyük fel, hogy azt szeretnénk, hogy a
`notify` az `item`-en a `summarize` mellett megjelenítési formázást is
használjon: a `notify` definíciójában megadjuk, hogy az `item`-nek a `Display`
és a `Summary` traitet is meg kell valósítania. Ezt a `+` szintaxissal tehetjük
meg:

```rust,ignore
pub fn notify(item: &(impl Summary + Display)) {
```

A `+` szintaxis a generikus típusok trait-korlátjainál is érvényes:

```rust,ignore
pub fn notify<T: Summary + Display>(item: &T) {
```

A két megadott trait-korláttal a `notify` törzse meghívhatja a `summarize`-t,
és a `{}` segítségével formázhatja az `item`-et.

#### Áttekinthetőbb trait-korlátok `where` záradékkal {#clearer-trait-bounds-with-where-clauses}

A túl sok trait-korlát használatának megvannak a hátrányai. Minden generikus
típusnak saját trait-korlátjai vannak, így a több generikus típusparaméterrel
rendelkező függvények neve és paraméterlistája között rengeteg
trait-korlát-információ állhat, ami nehezen olvashatóvá teszi a függvény
szignatúráját. Ezért a Rustban van egy másik szintaxis is, amellyel a
trait-korlátokat a függvényszignatúra utáni `where` záradékban adhatjuk meg.
Ahelyett tehát, hogy ezt írnánk:

```rust,ignore
fn some_function<T: Display + Clone, U: Clone + Debug>(t: &T, u: &U) -> i32 {
```

használhatunk egy `where` záradékot, így:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-07-where-clause/src/lib.rs:here}}
```

Ennek a függvénynek a szignatúrája kevésbé zsúfolt: a függvény neve, a
paraméterlista és a visszatérési típus közel van egymáshoz, hasonlóan egy sok
trait-korlát nélküli függvényhez.

### Traiteket megvalósító típusok visszaadása {#returning-types-that-implement-traits}

Az `impl Trait` szintaxist visszatérési pozícióban is használhatjuk, hogy
valamilyen, egy traitet megvalósító típusú értéket adjunk vissza, ahogy itt
látható:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-05-returning-impl-trait/src/lib.rs:here}}
```

Azzal, hogy visszatérési típusként az `impl Summary`-t használjuk, megadjuk,
hogy a `returns_summarizable` függvény valamilyen, a `Summary` traitet
megvalósító típust ad vissza, anélkül hogy megneveznénk a konkrét típust. Ebben
az esetben a `returns_summarizable` egy `SocialPost`-ot ad vissza, de a
függvényt meghívó kódnak ezt nem kell tudnia.

Az a lehetőség, hogy a visszatérési típust csak az általa megvalósított
traittel adjuk meg, különösen a closure-ök és az iterátorok esetében hasznos,
amelyekről a 13. fejezetben lesz szó. A closure-ök és az iterátorok olyan
típusokat hoznak létre, amelyeket csak a fordító ismer, vagy amelyeket nagyon
hosszú lenne leírni. Az `impl Trait` szintaxissal tömören megadhatod, hogy egy
függvény valamilyen, az `Iterator` traitet megvalósító típust ad vissza,
anélkül hogy egy nagyon hosszú típust kellene kiírnod.

Az `impl Trait` azonban csak akkor használható, ha egyetlen típust adsz vissza.
Például ez a kód, amely vagy egy `NewsArticle`-t, vagy egy `SocialPost`-ot ad
vissza `impl Summary` visszatérési típussal, nem működne:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-06-impl-trait-returns-one-type/src/lib.rs:here}}
```

Az, hogy vagy egy `NewsArticle`-t, vagy egy `SocialPost`-ot adjunk vissza, nem
megengedett, mert az `impl Trait` szintaxis fordítóbeli megvalósítása ezt
korlátozza. Azt, hogy hogyan írhatunk ilyen viselkedésű függvényt, a 18.
fejezet [„Trait objektumok használata a közös viselkedés
absztrahálására”][trait-objects]<!-- ignore --> szakaszában tárgyaljuk.

### Metódusok feltételes megvalósítása trait-korlátokkal {#using-trait-bounds-to-conditionally-implement-methods}

Ha egy generikus típusparamétereket használó `impl` blokkban trait-korlátot
alkalmazunk, feltételesen valósíthatunk meg metódusokat azokra a típusokra,
amelyek megvalósítják a megadott traiteket. A 10-15. kódrészlet `Pair<T>`
típusa például mindig megvalósítja a `new` függvényt, amely a `Pair<T>` egy új
példányát adja vissza (az 5. fejezet
[„Metódusszintaxis”][methods]<!-- ignore --> szakaszából emlékezhetsz rá, hogy a `Self` az `impl` blokk típusának
típusálneve, ami ebben az esetben a `Pair<T>`). A következő `impl` blokkban
viszont a `Pair<T>` csak akkor valósítja meg a `cmp_display` metódust, ha a
belső `T` típusa megvalósítja az összehasonlítást lehetővé tévő `PartialOrd`
traitet _és_ a kiírást lehetővé tévő `Display` traitet.

<Listing number="10-15" file-name="src/lib.rs" caption="Metódusok feltételes megvalósítása egy generikus típuson a trait-korlátoktól függően">

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-15/src/lib.rs}}
```

</Listing>

Egy traitet feltételesen is megvalósíthatunk bármely olyan típusra, amely egy
másik traitet megvalósít. Egy trait olyan megvalósításait, amelyek bármely, a
trait-korlátoknak megfelelő típusra vonatkoznak, _átfogó megvalósításoknak
(blanket implementations)_ nevezzük, és a Rust standard könyvtára széles körben
használja őket. A standard könyvtár például minden olyan típuson megvalósítja a
`ToString` traitet, amely megvalósítja a `Display` traitet. A standard
könyvtárban az `impl` blokk nagyjából így néz ki:

```rust,ignore
impl<T: Display> ToString for T {
    // --snip--
}
```

Mivel a standard könyvtárban megvan ez az átfogó megvalósítás, a `ToString`
trait által definiált `to_string` metódust bármely olyan típuson meghívhatjuk,
amely megvalósítja a `Display` traitet. Az egész számokat például így
alakíthatjuk a nekik megfelelő `String` értékekké, mert az egész számok
megvalósítják a `Display`-t:

```rust
let s = 3.to_string();
```

Az átfogó megvalósítások a trait dokumentációjában az „Implementors” szakaszban
jelennek meg.

A traitek és a trait-korlátok lehetővé teszik, hogy olyan kódot írjunk, amely
generikus típusparaméterekkel csökkenti az ismétlődést, ugyanakkor jelezzük a
fordítónak, hogy a generikus típustól bizonyos viselkedést várunk. A fordító
ezután a trait-korlátokban megadott információ alapján ellenőrizheti, hogy a
kódunkkal használt összes konkrét típus a megfelelő viselkedést nyújtja-e.
Dinamikusan típusos nyelvekben futásidejű hibát kapnánk, ha egy olyan típuson
hívnánk meg egy metódust, amely nem definiálja azt. A Rust viszont ezeket a
hibákat fordítási időre hozza előre, így kénytelenek vagyunk kijavítani a
problémákat, mielőtt a kódunk egyáltalán futni tudna. Ráadásul nem kell olyan
kódot írnunk, amely futásidőben ellenőrzi a viselkedést, hiszen ezt már
fordítási időben ellenőriztük. Ez javítja a teljesítményt anélkül, hogy le
kellene mondanunk a generikus típusok rugalmasságáról.

[trait-objects]: ch18-02-trait-objects.html#using-trait-objects-to-abstract-over-shared-behavior
[methods]: ch05-03-method-syntax.html#method-syntax
