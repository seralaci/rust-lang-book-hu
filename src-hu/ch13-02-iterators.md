## Elemsorozatok feldolgozása iterátorokkal {#processing-a-series-of-items-with-iterators}

Az iterátorminta lehetővé teszi, hogy egy elemsorozat elemein egymás után
valamilyen feladatot hajts végre. Az iterátor felel azért a logikáért, amely
végighalad az egyes elemeken, és megállapítja, mikor ért véget a sorozat. Ha
iterátorokat használsz, ezt a logikát nem kell magadnak újra megvalósítanod.

A Rustban az iterátorok _lusták (lazy)_, vagyis semmilyen hatásuk sincs,
amíg meg nem hívsz olyan metódusokat, amelyek elfogyasztják (consume), azaz
felhasználják az iterátort. A 13-10. kódrészlet kódja például a `Vec<T>`-n
definiált `iter` metódus meghívásával létrehoz egy iterátort a `v1` vektor
elemei fölött. Ez a kód önmagában semmi hasznosat nem csinál.

<Listing number="13-10" file-name="src/main.rs" caption="Iterátor létrehozása">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-10/src/main.rs:here}}
```

</Listing>

Az iterátort a `v1_iter` változóban tároljuk. Ha létrehoztunk egy iterátort,
sokféleképpen használhatjuk. A 3-5. kódrészletben egy `for` ciklussal
haladtunk végig egy tömbön, hogy minden elemén lefuttassunk valamilyen kódot.
A háttérben ez implicit módon létrehozott, majd elfogyasztott egy iterátort,
de eddig nem részleteztük, hogy ez pontosan hogyan működik.

A 13-11. kódrészlet példájában szétválasztjuk az iterátor létrehozását az
iterátor `for` ciklusbeli használatától. Amikor a `for` ciklus a `v1_iter`-ben
lévő iterátorral fut, az iterátor minden eleme a ciklus egy-egy iterációjában
kerül felhasználásra, és a ciklus kiírja az egyes értékeket.

<Listing number="13-11" file-name="src/main.rs" caption="Iterátor használata `for` ciklusban">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-11/src/main.rs:here}}
```

</Listing>

Azokban a nyelvekben, amelyeknek a standard könyvtára nem biztosít
iterátorokat, ugyanezt a funkcionalitást valószínűleg úgy írnád meg, hogy egy
változót 0-s indexről indítasz, ezzel a változóval indexeled a vektort, hogy
megkapj egy értéket, majd egy ciklusban addig növeled a változó értékét, amíg
el nem éri a vektor elemeinek számát.

Az iterátorok ezt az egész logikát elintézik helyetted, így kevesebb az
ismétlődő kód, amelyet esetleg elronthatnál. Az iterátorok nagyobb
rugalmasságot adnak: ugyanazt a logikát sokféle sorozattal használhatod, nem
csak indexelhető adatszerkezetekkel, mint például a vektorok. Nézzük meg,
hogyan érik ezt el az iterátorok.

### Az `Iterator` trait és a `next` metódus {#the-iterator-trait-and-the-next-method}

Minden iterátor megvalósít egy `Iterator` nevű traitet, amelyet a standard
könyvtár definiál. A trait definíciója így néz ki:

```rust
pub trait Iterator {
    type Item;

    fn next(&mut self) -> Option<Self::Item>;

    // methods with default implementations elided
}
```

Figyeld meg, hogy ez a definíció új szintaxist használ: a `type Item` és a
`Self::Item` egy ehhez a traithez tartozó társított típust (associated type)
definiál. A társított típusokról részletesen a 20. fejezetben lesz szó.
Egyelőre elég annyit tudnod, hogy ez a kód azt mondja: az `Iterator` trait
megvalósításához egy `Item` típust is definiálnod kell, és ezt az `Item`
típust a `next` metódus visszatérési típusa használja. Más szóval az `Item`
típus lesz az iterátor által visszaadott típus.

Az `Iterator` trait a megvalósítóitól csak egyetlen metódus definiálását
követeli meg: a `next` metódusét, amely egyszerre egy elemet ad vissza az
iterátorból `Some`-ba csomagolva, az iteráció végén pedig `None`-t ad vissza.

A `next` metódust közvetlenül is meghívhatjuk az iterátorokon; a 13-12.
kódrészlet bemutatja, milyen értékeket adnak vissza a `next` ismételt hívásai
a vektorból létrehozott iterátoron.

<Listing number="13-12" file-name="src/lib.rs" caption="A `next` metódus meghívása egy iterátoron">

```rust,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-12/src/lib.rs:here}}
```

</Listing>

Figyeld meg, hogy a `v1_iter`-t módosíthatóvá kellett tennünk: a `next`
metódus meghívása egy iterátoron megváltoztatja azt a belső állapotot, amellyel
az iterátor nyomon követi, hol tart a sorozatban. Más szóval ez a kód
_elfogyasztja_, azaz felhasználja az iterátort. A `next` minden hívása
elfogyaszt egy elemet az iterátorból. Amikor `for` ciklust használtunk, nem
kellett módosíthatóvá tennünk a `v1_iter`-t, mert a ciklus átvette a
`v1_iter` tulajdonjogát, és a háttérben módosíthatóvá tette.

Azt is figyeld meg, hogy a `next` hívásaiból kapott értékek nem módosítható
referenciák a vektorban lévő értékekre. Az `iter` metódus nem módosítható
referenciák fölötti iterátort állít elő. Ha olyan iterátort szeretnénk
létrehozni, amely átveszi a `v1` tulajdonjogát, és saját tulajdonú értékeket
ad vissza, az `iter` helyett az `into_iter`-t hívhatjuk meg. Hasonlóképpen, ha
módosítható referenciákon szeretnénk végighaladni, az `iter` helyett az
`iter_mut`-ot hívhatjuk meg.

### Az iterátort elfogyasztó metódusok {#methods-that-consume-the-iterator}

Az `Iterator` traitnek számos különféle metódusa van, amelyeknek az
alapértelmezett megvalósítását a standard könyvtár biztosítja; ezekről a
metódusokról a standard könyvtár API-dokumentációjában, az `Iterator` traitnél
tájékozódhatsz. Ezen metódusok némelyike a definíciójában meghívja a `next`
metódust, ezért kell megvalósítanod a `next` metódust, amikor az `Iterator`
traitet megvalósítod.

A `next`-et meghívó metódusokat _fogyasztó adaptereknek (consuming
adapters)_ nevezzük, mert a meghívásuk elfogyasztja az iterátort. Ilyen
például a `sum` metódus, amely átveszi az iterátor tulajdonjogát, és a `next`
ismételt hívásával végighalad az elemeken, így elfogyasztja az iterátort. Az
elemeken végighaladva mindegyiket hozzáadja egy folyamatosan frissülő
összeghez, és az iteráció végén visszaadja az összeget. A 13-13. kódrészlet
egy tesztet tartalmaz, amely a `sum` metódus használatát szemlélteti.

<Listing number="13-13" file-name="src/lib.rs" caption="A `sum` metódus meghívása az iterátor összes elemének összegéhez">

```rust,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-13/src/lib.rs:here}}
```

</Listing>

A `sum` hívása után már nem használhatjuk a `v1_iter`-t, mert a `sum` átveszi
annak az iterátornak a tulajdonjogát, amelyen meghívjuk.

### Más iterátorokat előállító metódusok {#methods-that-produce-other-iterators}

Az _iterátoradapterek (iterator adapters)_ az `Iterator` traiten definiált
olyan metódusok, amelyek nem fogyasztják el az iterátort. Ehelyett más
iterátorokat állítanak elő az eredeti iterátor valamely jellemzőjének
megváltoztatásával.

A 13-14. kódrészlet egy példát mutat a `map` iterátoradapter-metódus
meghívására, amely egy closure-t vár, és azt minden elemre meghívja, ahogy
végighalad rajtuk. A `map` metódus egy új iterátort ad vissza, amely a
módosított elemeket állítja elő. Az itteni closure egy olyan új iterátort hoz
létre, amelyben a vektor minden eleme 1-gyel meg lesz növelve.

<Listing number="13-14" file-name="src/main.rs" caption="A `map` iterátoradapter meghívása egy új iterátor létrehozásához">

```rust,not_desired_behavior
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-14/src/main.rs:here}}
```

</Listing>

Ez a kód azonban figyelmeztetést ad:

```console
{{#include ../listings/ch13-functional-features/listing-13-14/output.txt}}
```

A 13-14. kódrészlet kódja semmit sem csinál; a megadott closure soha nem
hívódik meg. A figyelmeztetés emlékeztet minket az okára: az iterátoradapterek
lusták, és itt el kell fogyasztanunk az iterátort.

A figyelmeztetés megszüntetéséhez és az iterátor elfogyasztásához a `collect`
metódust használjuk, amelyet a 12-1. kódrészletben az `env::args`-szal
együtt használtunk. Ez a metódus elfogyasztja az iterátort, és az eredményül
kapott értékeket egy gyűjtemény adattípusba gyűjti.

A 13-15. kódrészletben egy vektorba gyűjtjük annak az iterátornak az elemeit,
amelyet a `map` hívása ad vissza. Ez a vektor végül az eredeti vektor összes
elemét tartalmazza, mindegyiket 1-gyel megnövelve.

<Listing number="13-15" file-name="src/main.rs" caption="A `map` metódus meghívása egy új iterátor létrehozásához, majd a `collect` metódus meghívása az új iterátor elfogyasztásához és egy vektor létrehozásához">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-15/src/main.rs:here}}
```

</Listing>

Mivel a `map` egy closure-t vár, bármilyen műveletet megadhatunk, amelyet az
egyes elemeken végre szeretnénk hajtani. Ez remek példa arra, hogyan teszik
lehetővé a closure-ök, hogy testreszabj valamilyen viselkedést, miközben
újrahasznosítod az `Iterator` trait által biztosított iterálási viselkedést.

Az iterátoradapterek több hívását láncba is fűzheted, hogy összetett
műveleteket olvasható módon végezz el. De mivel minden iterátor lusta, meg kell
hívnod valamelyik fogyasztó adapter metódust, hogy eredményt kapj az
iterátoradapterek hívásaiból.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-closures-that-capture-their-environment"></a>

### A környezetüket elkapó closure-ök {#closures-that-capture-their-environment}

Sok iterátoradapter closure-öket vár argumentumként, és az iterátoradaptereknek
argumentumként megadott closure-ök általában olyanok lesznek, amelyek
elkapják a környezetüket.

Ebben a példában a `filter` metódust használjuk, amely egy closure-t vár. A
closure megkap egy elemet az iterátorból, és egy `bool` értéket ad vissza. Ha
a closure `true`-t ad vissza, az érték bekerül a `filter` által előállított
iterátorba. Ha a closure `false`-t ad vissza, az érték nem kerül bele.

A 13-16. kódrészletben a `filter`-t egy olyan closure-rel használjuk, amely a
környezetéből elkapja a `shoe_size` változót, hogy végighaladjon `Shoe`
struktúrapéldányok egy gyűjteményén. Csak a megadott méretű cipőket adja
vissza.

<Listing number="13-16" file-name="src/lib.rs" caption="A `filter` metódus használata egy, a `shoe_size`-t elkapó closure-rel">

```rust,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-16/src/lib.rs}}
```

</Listing>

A `shoes_in_size` függvény paraméterként átveszi egy cipőket tartalmazó vektor
tulajdonjogát és egy cipőméretet. Egy olyan vektort ad vissza, amely csak a
megadott méretű cipőket tartalmazza.

A `shoes_in_size` törzsében meghívjuk az `into_iter`-t, hogy létrehozzunk egy
iterátort, amely átveszi a vektor tulajdonjogát. Ezután meghívjuk a
`filter`-t, hogy ezt az iterátort egy olyan új iterátorrá alakítsuk, amely
csak azokat az elemeket tartalmazza, amelyekre a closure `true`-t ad vissza.

A closure elkapja a környezetből a `shoe_size` paramétert, és összehasonlítja
az értékét az egyes cipők méretével, így csak a megadott méretű cipőket tartja
meg. Végül a `collect` meghívása egy vektorba gyűjti az átalakított iterátor
által visszaadott értékeket, és ezt a vektort adja vissza a függvény.

A teszt azt mutatja, hogy a `shoes_in_size` meghívásakor csak azokat a
cipőket kapjuk vissza, amelyeknek a mérete megegyezik a megadott értékkel.
