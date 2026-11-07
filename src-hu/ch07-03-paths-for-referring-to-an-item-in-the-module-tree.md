## Útvonalak a modulfa elemeire való hivatkozáshoz {#paths-for-referring-to-an-item-in-the-module-tree}

Ahhoz, hogy megmutassuk a Rustnak, hol talál meg egy elemet a modulfában,
útvonalat használunk, ugyanúgy, ahogy egy fájlrendszerben való navigáláskor is
útvonalat használunk. Egy függvény meghívásához ismernünk kell az útvonalát.

Az útvonal kétféle lehet:

- Az _abszolút útvonal (absolute path)_ a crate gyökerétől induló teljes
  útvonal; külső crate-ből származó kód esetén az abszolút útvonal a crate
  nevével kezdődik, az aktuális crate kódja esetén pedig a `crate` literállal.
- A _relatív útvonal (relative path)_ az aktuális modulból indul, és a
  `self`, a `super` kulcsszóval vagy az aktuális modulban lévő azonosítóval
  kezdődik.

Az abszolút és a relatív útvonalat is egy vagy több, dupla kettősponttal
(`::`) elválasztott azonosító követi.

Térjünk vissza a 7-1. kódrészlethez, és tegyük fel, hogy meg akarjuk hívni az
`add_to_waitlist` függvényt. Ez ugyanaz, mintha azt kérdeznénk: mi az
`add_to_waitlist` függvény útvonala? A 7-3. kódrészlet a 7-1. kódrészletet
tartalmazza, néhány modul és függvény eltávolításával.

Két módját mutatjuk be annak, hogyan hívhatjuk meg az `add_to_waitlist`
függvényt egy új, a crate-gyökérben definiált `eat_at_restaurant` függvényből.
Ezek az útvonalak helyesek, de van még egy másik probléma, amely miatt ez a
példa ebben a formában nem fordul le. Hamarosan elmagyarázzuk, miért.

Az `eat_at_restaurant` függvény a könyvtár crate-ünk nyilvános API-jának
része, ezért a `pub` kulcsszóval jelöljük meg. Az [„Útvonalak nyilvánossá
tétele a `pub` kulcsszóval”][pub]<!-- ignore --> szakaszban részletesebben is
foglalkozunk a `pub` kulcsszóval.

<Listing number="7-3" file-name="src/lib.rs" caption="Az `add_to_waitlist` függvény meghívása abszolút és relatív útvonallal">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-03/src/lib.rs}}
```

</Listing>

Amikor először hívjuk meg az `add_to_waitlist` függvényt az
`eat_at_restaurant` függvényben, abszolút útvonalat használunk. Az
`add_to_waitlist` függvény ugyanabban a crate-ben van definiálva, mint az
`eat_at_restaurant`, ezért az abszolút útvonalat kezdhetjük a `crate`
kulcsszóval. Ezután sorra felsoroljuk az egymást követő modulokat, amíg el nem
jutunk az `add_to_waitlist` függvényig. Elképzelhetsz egy ugyanilyen
szerkezetű fájlrendszert: az `add_to_waitlist` program futtatásához a
`/front_of_house/hosting/add_to_waitlist` útvonalat adnánk meg; a `crate`
névvel a crate gyökerétől indulni olyan, mint a shellben a `/` jellel a
fájlrendszer gyökerétől indulni.

Amikor másodszor hívjuk meg az `add_to_waitlist` függvényt az
`eat_at_restaurant` függvényben, relatív útvonalat használunk. Az útvonal a
`front_of_house` névvel kezdődik, amely a modulfa ugyanazon szintjén
definiált modul neve, ahol az `eat_at_restaurant` is van. Itt a fájlrendszerbeli
megfelelő a `front_of_house/hosting/add_to_waitlist` útvonal használata
lenne. Ha az útvonal egy modulnévvel kezdődik, akkor relatív.

Az, hogy relatív vagy abszolút útvonalat használsz-e, a projektedtől függő
döntés, és attól függ, hogy az elem definíciójának kódját valószínűbben az
elemet használó kódtól külön vagy azzal együtt fogod-e áthelyezni. Ha
például a `front_of_house` modult és az `eat_at_restaurant` függvényt egy
`customer_experience` nevű modulba helyeznénk át, akkor az `add_to_waitlist`
függvényhez vezető abszolút útvonalat frissítenünk kellene, a relatív útvonal
viszont továbbra is érvényes maradna. Ha azonban az `eat_at_restaurant`
függvényt külön egy `dining` nevű modulba helyeznénk át, az `add_to_waitlist`
hívásához vezető abszolút útvonal változatlan maradna, a relatív útvonalat
viszont frissíteni kellene. Általában az abszolút útvonalakat részesítjük
előnyben, mert valószínűbb, hogy a kóddefiníciókat és az elemhívásokat
egymástól függetlenül szeretnénk majd áthelyezni.

Próbáljuk meg lefordítani a 7-3. kódrészletet, és derítsük ki, miért nem
fordul még le! A kapott hibákat a 7-4. kódrészlet mutatja.

<Listing number="7-4" caption="A 7-3. kódrészlet fordításakor kapott fordítói hibák">

```console
{{#include ../listings/ch07-managing-growing-projects/listing-07-03/output.txt}}
```

</Listing>

A hibaüzenetek szerint a `hosting` modul privát. Más szóval a `hosting`
modulhoz és az `add_to_waitlist` függvényhez vezető útvonalak helyesek, de a
Rust nem engedi használni őket, mert nincs hozzáférése a privát részekhez. A
Rustban alapértelmezés szerint minden elem (függvény, metódus, struktúra,
enum, modul és konstans) privát a szülőmodulok számára. Ha egy elemet, például
egy függvényt vagy struktúrát privátként akarsz kezelni, tedd egy modulba.

A szülőmodulban lévő elemek nem használhatják a gyermekmodulokon belüli privát
elemeket, a gyermekmodulokban lévő elemek viszont használhatják az
ősmoduljaikban lévő elemeket. Ennek az az oka, hogy a gyermekmodulok
becsomagolják és elrejtik a megvalósítási részleteiket, de látják azt a
környezetet, amelyben definiálták őket. Hogy a hasonlatnál maradjunk: gondolj
úgy a láthatósági szabályokra, mint egy étterem irodájára. Ami ott történik,
az az étterem vendégei számára rejtve marad, az irodavezetők azonban mindent
látnak és megtehetnek az általuk működtetett étteremben.

A Rust azért működteti így a modulrendszert, hogy a belső megvalósítási
részletek elrejtése legyen az alapértelmezés. Így tudod, hogy a belső kód mely
részeit változtathatod meg anélkül, hogy a külső kód elromlana. A Rust
ugyanakkor lehetőséget ad arra, hogy a gyermekmodulok kódjának belső részeit
elérhetővé tedd a külső ősmodulok számára: a `pub` kulcsszóval nyilvánossá
teheted az adott elemet.

### Útvonalak nyilvánossá tétele a `pub` kulcsszóval {#exposing-paths-with-the-pub-keyword}

Térjünk vissza a 7-4. kódrészletben kapott hibához, amely szerint a `hosting`
modul privát. Azt szeretnénk, hogy a szülőmodulban lévő `eat_at_restaurant`
függvény hozzáférjen a gyermekmodulban lévő `add_to_waitlist` függvényhez,
ezért a `hosting` modult megjelöljük a `pub` kulcsszóval, ahogy a 7-5.
kódrészlet mutatja.

<Listing number="7-5" file-name="src/lib.rs" caption="A `hosting` modul deklarálása `pub`-ként, hogy az `eat_at_restaurant` függvényből használhassuk">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-05/src/lib.rs:here}}
```

</Listing>

Sajnos a 7-5. kódrészlet kódja is fordítási hibákat eredményez, ahogy a 7-6.
kódrészlet mutatja.

<Listing number="7-6" caption="A 7-5. kódrészlet fordításakor kapott fordítói hibák">

```console
{{#include ../listings/ch07-managing-growing-projects/listing-07-05/output.txt}}
```

</Listing>

Mi történt? Ha a `pub` kulcsszót a `mod hosting` elé írjuk, a modul
nyilvánossá válik. Ezzel a változtatással, ha hozzáférünk a `front_of_house`
modulhoz, a `hosting` modulhoz is hozzáférünk. A `hosting` modul _tartalma_
azonban továbbra is privát; a modul nyilvánossá tétele nem teszi nyilvánossá a
tartalmát. A modulon lévő `pub` kulcsszó csak azt teszi lehetővé, hogy az
ősmoduljaiban lévő kód hivatkozzon rá, azt nem, hogy hozzáférjen a belső
kódjához. Mivel a modulok tárolók, azzal, hogy csak a modult tesszük
nyilvánossá, nem sokra megyünk; tovább kell lépnünk, és a modulon belüli
elemek közül is egyet vagy többet nyilvánossá kell tennünk.

A 7-6. kódrészletben látható hibák szerint az `add_to_waitlist` függvény
privát. A láthatósági szabályok a modulok mellett a struktúrákra, az
enumokra, a függvényekre és a metódusokra is vonatkoznak.

Tegyük nyilvánossá az `add_to_waitlist` függvényt is úgy, hogy a definíciója
elé írjuk a `pub` kulcsszót, ahogy a 7-7. kódrészletben.

<Listing number="7-7" file-name="src/lib.rs" caption="Ha a `pub` kulcsszót a `mod hosting` és az `fn add_to_waitlist` elé írjuk, meghívhatjuk a függvényt az `eat_at_restaurant` függvényből.">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-07/src/lib.rs:here}}
```

</Listing>

Most már lefordul a kód! Hogy lássuk, a láthatósági szabályok szempontjából
miért teszi lehetővé a `pub` kulcsszó hozzáadása, hogy ezeket az útvonalakat
használjuk az `eat_at_restaurant` függvényben, nézzük meg az abszolút és a
relatív útvonalat.

Az abszolút útvonalban a `crate` névvel kezdünk, amely a crate-ünk modulfájának
gyökere. A `front_of_house` modul a crate-gyökérben van definiálva. Bár a
`front_of_house` nem nyilvános, mivel az `eat_at_restaurant` függvény
ugyanabban a modulban van definiálva, mint a `front_of_house` (vagyis az
`eat_at_restaurant` és a `front_of_house` testvérek), az
`eat_at_restaurant` függvényből hivatkozhatunk a `front_of_house` modulra.
Ezután következik a `pub` kulcsszóval megjelölt `hosting` modul. Hozzáférünk
a `hosting` szülőmoduljához, így a `hosting` modulhoz is hozzáférünk. Végül
az `add_to_waitlist` függvény `pub` jelölésű, és hozzáférünk a
szülőmoduljához, így ez a függvényhívás működik!

A relatív útvonalban a logika ugyanaz, mint az abszolút útvonalban, az első
lépést kivéve: az útvonal nem a crate gyökeréből, hanem a `front_of_house`
modulból indul. A `front_of_house` modul ugyanabban a modulban van
definiálva, mint az `eat_at_restaurant`, így működik az a relatív útvonal,
amely abból a modulból indul, amelyben az `eat_at_restaurant` definiálva van.
Ezután, mivel a `hosting` és az `add_to_waitlist` `pub` jelölésű, az útvonal
többi része is működik, és ez a függvényhívás érvényes!

Ha meg akarod osztani a könyvtár crate-edet, hogy más projektek is
használhassák a kódodat, a nyilvános API-d a crate-ed felhasználóival kötött
szerződésed, amely meghatározza, hogyan léphetnek kapcsolatba a kódoddal. A
nyilvános API változásainak kezelésénél sok szempontot kell figyelembe venni,
hogy mások könnyebben függhessenek a crate-edtől. Ezek a szempontok túlmutatnak
e könyv keretein; ha érdekel a téma, olvasd el [a Rust API-irányelveit (Rust API
Guidelines)][api-guidelines].

> #### Bevált gyakorlatok bináris és könyvtár crate-et is tartalmazó csomagokhoz {#best-practices-for-packages-with-a-binary-and-a-library}
>
> Említettük, hogy egy csomag tartalmazhat egy _src/main.rs_ bináris
> crate-gyökeret és egy _src/lib.rs_ könyvtár crate-gyökeret is, és
> alapértelmezés szerint mindkét crate a csomag nevét viseli. Az ilyen,
> könyvtár és bináris crate-et is tartalmazó csomagokban a bináris crate
> jellemzően csak annyi kódot tartalmaz, amennyi egy olyan futtatható állomány
> elindításához szükséges, amely a könyvtár crate-ben definiált kódot hívja.
> Így más projektek a lehető legtöbbet hasznosíthatják a csomag által nyújtott
> funkciókból, mert a könyvtár crate kódja megosztható.
>
> A modulfát az _src/lib.rs_ fájlban érdemes definiálni. Ezután a nyilvános
> elemek a bináris crate-ben is használhatók, ha az útvonalakat a csomag
> nevével kezdjük. A bináris crate ugyanúgy a könyvtár crate felhasználójává
> válik, ahogy egy teljesen külső crate használná a könyvtár crate-et: csak a
> nyilvános API-t használhatja. Ez segít jó API-t tervezni, hiszen nemcsak a
> szerzője, hanem a felhasználója is vagy!
>
> A [12. fejezetben][ch12]<!-- ignore --> ezt a szervezési gyakorlatot egy
> olyan parancssori programmal mutatjuk be, amely bináris és könyvtár crate-et
> is tartalmaz.

### Relatív útvonalak kezdése a `super` kulcsszóval {#starting-relative-paths-with-super}

Olyan relatív útvonalakat is létrehozhatunk, amelyek nem az aktuális modulból
vagy a crate gyökeréből, hanem a szülőmodulból indulnak: ehhez az útvonal
elejére a `super` kulcsszót írjuk. Ez olyan, mintha egy fájlrendszerbeli
útvonalat a `..` szintaxissal kezdenénk, amely a szülőmappába lépést jelenti.
A `super` segítségével olyan elemre hivatkozhatunk, amelyről tudjuk, hogy a
szülőmodulban van. Ez megkönnyítheti a modulfa átrendezését, ha a modul
szorosan kapcsolódik a szülőjéhez, de a szülőt egyszer esetleg a modulfa egy
másik pontjára helyezzük át.

Nézzük a 7-8. kódrészlet kódját, amely azt a helyzetet modellezi, amikor egy
séf kijavít egy hibás rendelést, és személyesen viszi ki a vendégnek. A
`back_of_house` modulban definiált `fix_incorrect_order` függvény úgy hívja
meg a szülőmodulban definiált `deliver_order` függvényt, hogy a
`deliver_order` útvonalát a `super` kulcsszóval kezdve adja meg.

<Listing number="7-8" file-name="src/lib.rs" caption="Függvényhívás `super` kulcsszóval kezdődő relatív útvonallal">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-08/src/lib.rs}}
```

</Listing>

A `fix_incorrect_order` függvény a `back_of_house` modulban van, így a
`super` kulcsszóval a `back_of_house` szülőmoduljába léphetünk, amely ebben az
esetben a `crate`, vagyis a gyökér. Onnan megkeressük a `deliver_order`
függvényt, és meg is találjuk. Siker! Úgy gondoljuk, hogy a `back_of_house`
modul és a `deliver_order` függvény valószínűleg ugyanabban a viszonyban
marad egymással, és együtt mozognak, ha úgy döntünk, hogy átszervezzük a crate
modulfáját. Ezért használtuk a `super` kulcsszót: így a jövőben kevesebb
helyen kell majd frissíteni a kódot, ha egy másik modulba kerül.

### Struktúrák és enumok nyilvánossá tétele {#making-structs-and-enums-public}

A `pub` kulcsszóval struktúrákat és enumokat is nyilvánossá tehetünk, de a
`pub` struktúrákkal és enumokkal való használatának van néhány további
részlete. Ha a `pub` kulcsszót egy struktúradefiníció elé írjuk, a struktúra
nyilvánossá válik, de a mezői továbbra is privátok maradnak. Az egyes
mezőkről esetenként dönthetünk, hogy nyilvánosak legyenek-e. A 7-9.
kódrészletben egy nyilvános `back_of_house::Breakfast` struktúrát
definiáltunk egy nyilvános `toast` és egy privát `seasonal_fruit` mezővel. Ez
azt az éttermi helyzetet modellezi, amikor a vendég kiválaszthatja, milyen
kenyeret kér az ételhez, de azt, hogy milyen gyümölcs jár mellé, a séf dönti
el aszerint, hogy mi van szezonban és raktáron. Az elérhető gyümölcsök gyorsan
változnak, ezért a vendégek nem választhatják ki a gyümölcsöt, és azt sem
láthatják, milyet kapnak.

<Listing number="7-9" file-name="src/lib.rs" caption="Struktúra néhány nyilvános és néhány privát mezővel">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-09/src/lib.rs}}
```

</Listing>

Mivel a `back_of_house::Breakfast` struktúra `toast` mezője nyilvános, az
`eat_at_restaurant` függvényben pontjelöléssel írhatjuk és olvashatjuk a
`toast` mezőt. Figyeld meg, hogy a `seasonal_fruit` mezőt nem használhatjuk az
`eat_at_restaurant` függvényben, mert a `seasonal_fruit` privát. Próbáld ki,
milyen hibát kapsz, ha kiveszed a kommentből azt a sort, amely a
`seasonal_fruit` mező értékét módosítja!

Vedd észre azt is, hogy mivel a `back_of_house::Breakfast` struktúrának van
privát mezője, a struktúrának biztosítania kell egy nyilvános társított
függvényt, amely létrehozza a `Breakfast` egy példányát (itt `summer` nevet
adtunk neki). Ha a `Breakfast` struktúrának nem lenne ilyen függvénye, nem
tudnánk létrehozni a `Breakfast` példányát az `eat_at_restaurant`
függvényben, mert az `eat_at_restaurant` függvényben nem tudnánk beállítani a
privát `seasonal_fruit` mező értékét.

Ezzel szemben, ha egy enumot nyilvánossá teszünk, az összes változata is
nyilvános lesz. Csak az `enum` kulcsszó elé kell a `pub`, ahogy a 7-10.
kódrészlet mutatja.

<Listing number="7-10" file-name="src/lib.rs" caption="Ha egy enumot nyilvánossá teszünk, az összes változata is nyilvános lesz.">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-10/src/lib.rs}}
```

</Listing>

Mivel az `Appetizer` enumot nyilvánossá tettük, a `Soup` és a `Salad`
változatot használhatjuk az `eat_at_restaurant` függvényben.

Az enumok nem igazán hasznosak, ha a változataik nem nyilvánosak; bosszantó
lenne minden esetben az összes enumváltozatot `pub` jelöléssel ellátni, ezért
az enumváltozatok alapértelmezés szerint nyilvánosak. A struktúrák gyakran
akkor is hasznosak, ha a mezőik nem nyilvánosak, ezért a struktúramezőkre az
az általános szabály vonatkozik, hogy alapértelmezés szerint minden privát,
hacsak nincs `pub` jelöléssel ellátva.

Van még egy, a `pub` kulcsszóval kapcsolatos helyzet, amelyről nem esett szó,
és ez a modulrendszer utolsó nyelvi eleme: a `use` kulcsszó. Először magát a
`use` kulcsszót mutatjuk be, majd azt, hogyan kombinálható a `pub` és a `use`.

[pub]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html#exposing-paths-with-the-pub-keyword
[api-guidelines]: https://rust-lang.github.io/api-guidelines/
[ch12]: ch12-00-an-io-project.html
