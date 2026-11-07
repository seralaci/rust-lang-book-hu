<!-- Old headings. Do not remove or links may break. -->

<a id="closures-anonymous-functions-that-can-capture-their-environment"></a>
<a id="closures-anonymous-functions-that-capture-their-environment"></a>

## Closure-ök {#closures}

A Rust closure-jei névtelen függvények, amelyeket változóba menthetsz, vagy
argumentumként átadhatsz más függvényeknek. A closure-t létrehozhatod az egyik
helyen, majd máshol meghívhatod, hogy egy másik kontextusban értékelődjön ki.
A függvényekkel ellentétben a closure-ök képesek elkapni (capture) értékeket
abból a hatókörből, amelyben definiáltuk őket. Megmutatjuk, hogyan teszik
lehetővé a closure-ök ezen tulajdonságai a kód újrafelhasználását és a
viselkedés testreszabását.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-an-abstraction-of-behavior-with-closures"></a>
<a id="refactoring-using-functions"></a>
<a id="refactoring-with-closures-to-store-code"></a>
<a id="capturing-the-environment-with-closures"></a>

### A környezet elkapása {#capturing-the-environment}

Először azt vizsgáljuk meg, hogyan használhatjuk a closure-öket arra, hogy
későbbi használatra elkapjunk értékeket abból a környezetből, amelyben
definiáltuk őket. A forgatókönyv a következő: pólócégünk időnként promóció
keretében egy exkluzív, limitált kiadású pólót ajándékoz valakinek a
levelezőlistánkról. A levelezőlistán szereplők a profiljukban opcionálisan
megadhatják a kedvenc színüket. Ha az ingyenes pólóra kiválasztott személy
beállította a kedvenc színét, abban a színben kapja meg a pólót. Ha nem adott
meg kedvenc színt, abból a színből kap, amelyből a cégnek éppen a legtöbb van
raktáron.

Ezt sokféleképpen meg lehet valósítani. Ebben a példában egy `ShirtColor` nevű
enumot használunk, amelynek `Red` és `Blue` változatai vannak (az egyszerűség
kedvéért korlátozzuk az elérhető színek számát). A cég készletét egy
`Inventory` struktúra képviseli, amelynek `shirts` nevű mezője egy
`Vec<ShirtColor>` értéket tartalmaz, amely a jelenleg raktáron lévő pólók
színeit tárolja. Az `Inventory`-n definiált `giveaway` metódus megkapja az
ingyenes póló nyertesének opcionális színpreferenciáját, és visszaadja annak a
pólónak a színét, amelyet a nyertes kapni fog. Ezt a felállást a 13-1.
kódrészlet mutatja.

<Listing number="13-1" file-name="src/main.rs" caption="A pólócég ajándékozási helyzete">

```rust,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-01/src/main.rs}}
```

</Listing>

A `main`-ben definiált `store`-ban két kék és egy piros póló maradt, amelyeket
ebben a limitált kiadású promócióban szétoszthatunk. Meghívjuk a `giveaway`
metódust egy olyan felhasználóra, aki a piros pólót részesíti előnyben, és egy
olyanra, akinek nincs preferenciája.

Ezt a kódot is sokféleképpen meg lehetne valósítani; itt, hogy a closure-ökre
összpontosíthassunk, a már megtanult fogalmaknál maradtunk, kivéve a `giveaway`
metódus törzsét, amely egy closure-t használ. A `giveaway` metódusban a
felhasználói preferenciát egy `Option<ShirtColor>` típusú paraméterként kapjuk
meg, és meghívjuk rajta az `unwrap_or_else` metódust. Az [`Option<T>`
`unwrap_or_else` metódusát][unwrap-or-else]<!-- ignore --> a standard könyvtár
definiálja. Egyetlen argumentumot vár: egy argumentum nélküli closure-t, amely
egy `T` értéket ad vissza (ugyanazt a típust, amelyet az `Option<T>` `Some`
változata tárol, ebben az esetben a `ShirtColor`-t). Ha az `Option<T>` a
`Some` változat, az `unwrap_or_else` a `Some`-on belüli értéket adja vissza.
Ha az `Option<T>` a `None` változat, az `unwrap_or_else` meghívja a closure-t,
és a closure által visszaadott értéket adja vissza.

Az `unwrap_or_else` argumentumaként a `|| self.most_stocked()`
closure-kifejezést adjuk meg. Ez egy olyan closure, amely maga nem vár
paramétert (ha a closure-nek lennének paraméterei, azok a két függőleges
vonal között szerepelnének). A closure törzse meghívja a `self.most_stocked()`
metódust. A closure-t itt definiáljuk, és az `unwrap_or_else` megvalósítása
később értékeli ki, ha szükség van az eredményre.

A kód futtatása a következőt írja ki:

```console
{{#include ../listings/ch13-functional-features/listing-13-01/output.txt}}
```

Érdekes, hogy olyan closure-t adtunk át, amely az aktuális `Inventory`
példányon hívja meg a `self.most_stocked()` metódust. A standard könyvtárnak
semmit sem kellett tudnia az általunk definiált `Inventory` és `ShirtColor`
típusokról, sem az ebben a helyzetben használni kívánt logikáról. A closure
egy nem módosítható referenciát kap el a `self` `Inventory` példányra, és az
általunk megadott kóddal együtt átadja az `unwrap_or_else` metódusnak. A
függvények ezzel szemben nem képesek így elkapni a környezetüket.

<!-- Old headings. Do not remove or links may break. -->

<a id="closure-type-inference-and-annotation"></a>

### A closure-ök típusainak következtetése és annotálása {#inferring-and-annotating-closure-types}

A függvények és a closure-ök között további különbségek is vannak. A
closure-ök általában nem igénylik, hogy annotáld a paraméterek vagy a
visszatérési érték típusát, ahogy az `fn` függvények igen. A függvényeknél
azért kötelező a típusannotáció, mert a típusok a felhasználóid felé nyújtott
explicit interfész részei. Ennek az interfésznek a szigorú definiálása fontos
ahhoz, hogy mindenki egyetértsen abban, milyen típusú értékeket használ és ad
vissza egy függvény. A closure-öket viszont nem használjuk ilyen nyilvános
interfészben: változókban tároljuk őket, és anélkül használjuk őket, hogy
nevet adnánk nekik és a könyvtárunk felhasználói elé tárnánk őket.

A closure-ök jellemzően rövidek, és nem tetszőleges helyzetekben, hanem csak
egy szűk kontextuson belül relevánsak. Ezekben a korlátozott kontextusokban a
fordító képes kikövetkeztetni a paraméterek és a visszatérési érték típusát,
hasonlóan ahhoz, ahogy a legtöbb változó típusát is ki tudja következtetni
(ritkán előfordul, hogy a fordítónak a closure-ök típusannotációira is
szüksége van).

A változókhoz hasonlóan itt is írhatunk típusannotációkat, ha nagyobb
egyértelműségre és világosságra törekszünk, annak árán, hogy a kód bőbeszédűbb
lesz a feltétlenül szükségesnél. Egy closure típusainak annotálása a 13-2.
kódrészletben látható definícióhoz hasonlóan nézne ki. Ebben a példában
definiálunk egy closure-t, és egy változóban tároljuk, ahelyett hogy azon a
helyen definiálnánk, ahol argumentumként átadjuk, ahogy a 13-1. kódrészletben
tettük.

<Listing number="13-2" file-name="src/main.rs" caption="A paraméter és a visszatérési érték opcionális típusannotációinak hozzáadása a closure-höz">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-02/src/main.rs:here}}
```

</Listing>

Típusannotációkkal a closure-ök szintaxisa jobban hasonlít a függvények
szintaxisára. Itt összehasonlításképpen definiálunk egy függvényt, amely 1-et
ad hozzá a paraméteréhez, és egy closure-t, amely ugyanígy viselkedik. Néhány
szóközt is beszúrtunk, hogy az egymásnak megfelelő részek egy vonalba
kerüljenek. Ez jól mutatja, hogy a closure-szintaxis hasonlít a
függvényszintaxisra, eltekintve a függőleges vonalak használatától és attól,
hogy mennyi a szintaxisban az elhagyható rész:

```rust,ignore
fn  add_one_v1   (x: u32) -> u32 { x + 1 }
let add_one_v2 = |x: u32| -> u32 { x + 1 };
let add_one_v3 = |x|             { x + 1 };
let add_one_v4 = |x|               x + 1  ;
```

Az első sor egy függvénydefiníciót, a második egy teljesen annotált
closure-definíciót mutat. A harmadik sorban eltávolítjuk a típusannotációkat a
closure-definícióból. A negyedik sorban a kapcsos zárójeleket is elhagyjuk,
amelyek opcionálisak, mivel a closure törzse egyetlen kifejezésből áll. Ezek
mind érvényes definíciók, amelyek meghíváskor ugyanúgy viselkednek. Az
`add_one_v3` és az `add_one_v4` sor csak akkor fordul le, ha a closure-öket ki
is értékeljük, mert a típusukat a használatukból következteti ki a fordító.
Ez ahhoz hasonló, ahogy a `let v = Vec::new();` utasításnál is típusannotáció
kell, vagy valamilyen típusú értékeket kell a `Vec`-be tenni ahhoz, hogy a Rust
ki tudja következtetni a típust.

A closure-definícióknál a fordító minden paraméterhez és a visszatérési
értékhez egy-egy konkrét típust következtet ki. A 13-3. kódrészlet például egy
rövid closure definícióját mutatja, amely egyszerűen visszaadja a paraméterként
kapott értéket. Ez a closure a példán kívül nem túl hasznos. Figyeld meg, hogy
a definícióhoz nem adtunk típusannotációt. Mivel nincsenek típusannotációk,
bármilyen típussal meghívhatjuk a closure-t – itt elsőre `String`-gel tettük.
Ha ezután egész számmal próbáljuk meghívni az `example_closure`-t, hibát
kapunk.

<Listing number="13-3" file-name="src/main.rs" caption="Kísérlet egy kikövetkeztetett típusú closure meghívására két különböző típussal">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-03/src/main.rs:here}}
```

</Listing>

A fordító a következő hibát adja:

```console
{{#include ../listings/ch13-functional-features/listing-13-03/output.txt}}
```

Amikor először hívjuk meg az `example_closure`-t a `String` értékkel, a
fordító arra következtet, hogy az `x` típusa és a closure visszatérési
típusa is `String`. Ezek a típusok ezután rögzülnek az `example_closure`-ben
lévő closure-ben, és típushibát kapunk, amikor legközelebb egy másik típust
próbálunk használni ugyanazzal a closure-rel.

### Referenciák elkapása vagy a tulajdonjog átmozgatása {#capturing-references-or-moving-ownership}

A closure-ök háromféleképpen kaphatnak el értékeket a környezetükből, ami
közvetlenül megfelel annak a háromféle módnak, ahogy egy függvény egy
paramétert átvehet: nem módosítható kölcsönzéssel, módosítható kölcsönzéssel
és a tulajdonjog átvételével. A closure attól függően dönti el, hogy ezek közül
melyiket használja, hogy a törzse mit csinál az elkapott értékekkel.

A 13-4. kódrészletben olyan closure-t definiálunk, amely egy nem módosítható
referenciát kap el a `list` nevű vektorra, mert az érték kiírásához csak nem
módosítható referenciára van szüksége.

<Listing number="13-4" file-name="src/main.rs" caption="Nem módosítható referenciát elkapó closure definiálása és meghívása">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-04/src/main.rs}}
```

</Listing>

Ez a példa azt is szemlélteti, hogy egy változó egy closure-definícióhoz is
köthető, és a closure-t később a változó nevével és zárójelekkel hívhatjuk
meg, mintha a változó neve egy függvény neve volna.

Mivel egyszerre több nem módosítható referenciánk is lehet a `list`-re, a
`list` továbbra is elérhető a closure-definíció előtti kódból, a
closure-definíció után, de még a closure meghívása előtt, és a closure
meghívása után is. Ez a kód lefordul, lefut, és a következőt írja ki:

```console
{{#include ../listings/ch13-functional-features/listing-13-04/output.txt}}
```

Ezután a 13-5. kódrészletben úgy módosítjuk a closure törzsét, hogy egy elemet
adjon a `list` vektorhoz. A closure most már módosítható referenciát kap el.

<Listing number="13-5" file-name="src/main.rs" caption="Módosítható referenciát elkapó closure definiálása és meghívása">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-05/src/main.rs}}
```

</Listing>

Ez a kód lefordul, lefut, és a következőt írja ki:

```console
{{#include ../listings/ch13-functional-features/listing-13-05/output.txt}}
```

Figyeld meg, hogy a `borrows_mutably` closure definíciója és meghívása között
már nincs `println!`: amikor a `borrows_mutably`-t definiáljuk, az egy
módosítható referenciát kap el a `list`-re. A closure meghívása után már nem
használjuk újra a closure-t, így a módosítható kölcsönzés véget ér. A
closure-definíció és a closure-hívás között nem megengedett egy kiíráshoz
szükséges nem módosítható kölcsönzés, mert módosítható kölcsönzés fennállása
alatt semmilyen más kölcsönzés nem megengedett. Próbálj meg odaírni egy
`println!`-t, és nézd meg, milyen hibaüzenetet kapsz!

Ha arra akarod kényszeríteni a closure-t, hogy átvegye a környezetben használt
értékek tulajdonjogát, noha a closure törzsének szigorúan véve nincs szüksége a
tulajdonjogra, a paraméterlista elé írhatod a `move` kulcsszót.

Ez a technika leginkább akkor hasznos, amikor egy closure-t egy új szálnak
adunk át, hogy az adatokat átmozgassuk, és azok az új szál tulajdonába
kerüljenek. A szálakat és azt, hogy miért érdemes használni őket, részletesen
a 16. fejezetben tárgyaljuk, amikor a konkurenciáról lesz szó, de most röviden
megnézzük, hogyan indíthatunk új szálat egy olyan closure-rel, amelyhez a
`move` kulcsszó szükséges. A 13-6. kódrészlet a 13-4. kódrészlet módosított
változata, amely a vektort nem a fő szálon, hanem egy új szálon írja ki.

<Listing number="13-6" file-name="src/main.rs" caption="A `move` használata, hogy a szál closure-je átvegye a `list` tulajdonjogát">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-06/src/main.rs}}
```

</Listing>

Elindítunk egy új szálat, és argumentumként egy futtatandó closure-t adunk
neki. A closure törzse kiírja a listát. A 13-4. kódrészletben a closure csak
nem módosítható referenciával kapta el a `list`-et, mert a kiíráshoz ennyi
hozzáférés is elég. Ebben a példában – bár a closure törzsének továbbra is
csak nem módosítható referenciára van szüksége – meg kell adnunk, hogy a
`list` a closure-be mozogjon, ezért a closure-definíció elejére a `move`
kulcsszót írjuk. Ha a fő szál még további műveleteket végezne, mielőtt az új
szálon meghívja a `join`-t, az új szál a fő szál többi része előtt is
befejeződhetne, de az is lehet, hogy a fő szál végez előbb. Ha a fő szál
megtartaná a `list` tulajdonjogát, de az új szál előtt véget érne, és eldobná
a `list`-et, a szálban lévő nem módosítható referencia érvénytelenné válna.
Ezért a fordító megköveteli, hogy a `list` az új szálnak átadott closure-be
mozogjon, hogy a referencia érvényes maradjon. Próbáld meg eltávolítani a
`move` kulcsszót, vagy használni a `list`-et a fő szálon a closure definiálása
után, és nézd meg, milyen fordítási hibákat kapsz!

<!-- Old headings. Do not remove or links may break. -->

<a id="storing-closures-using-generic-parameters-and-the-fn-traits"></a>
<a id="limitations-of-the-cacher-implementation"></a>
<a id="moving-captured-values-out-of-the-closure-and-the-fn-traits"></a>
<a id="moving-captured-values-out-of-closures-and-the-fn-traits"></a>

### Elkapott értékek kimozgatása a closure-ökből {#moving-captured-values-out-of-closures}

Miután egy closure elkapott egy referenciát vagy egy érték tulajdonjogát abból
a környezetből, amelyben definiáltuk (és ezzel meghatározta, hogy mi – ha
egyáltalán valami – mozog _be_ a closure-be), a closure törzsében lévő kód
határozza meg, mi történik a referenciákkal vagy értékekkel, amikor a
closure-t később kiértékeljük (és ezzel azt, hogy mi – ha egyáltalán valami –
mozog _ki_ a closure-ből).

Egy closure törzse a következők bármelyikét teheti: kimozgathat egy elkapott
értéket a closure-ből, módosíthatja az elkapott értéket, sem nem mozgatja ki,
sem nem módosítja az értéket, vagy eleve semmit sem kap el a környezetből.

Az, ahogyan egy closure elkapja és kezeli a környezetéből származó értékeket,
meghatározza, mely traiteket valósítja meg a closure, a traitek pedig azt
teszik lehetővé, hogy a függvények és a struktúrák megadják, milyen fajta
closure-öket tudnak használni. A closure-ök automatikusan megvalósítják ezen
`Fn` traitek közül az egyiket, kettőt vagy mindhármat, egymásra épülő módon,
attól függően, hogy a closure törzse hogyan kezeli az értékeket:

* Az `FnOnce` azokra a closure-ökre vonatkozik, amelyek egyszer hívhatók meg.
  Minden closure megvalósítja legalább ezt a traitet, hiszen minden closure
  meghívható. Az a closure, amely elkapott értékeket mozgat ki a törzséből,
  csak az `FnOnce`-t valósítja meg, a többi `Fn` traitet nem, mert csak
  egyszer hívható meg.
* Az `FnMut` azokra a closure-ökre vonatkozik, amelyek nem mozgatnak ki
  elkapott értékeket a törzsükből, de módosíthatják azokat. Ezek a closure-ök
  többször is meghívhatók.
* Az `Fn` azokra a closure-ökre vonatkozik, amelyek nem mozgatnak ki elkapott
  értékeket a törzsükből, és nem is módosítják azokat, valamint azokra,
  amelyek semmit sem kapnak el a környezetükből. Ezek a closure-ök többször is
  meghívhatók anélkül, hogy módosítanák a környezetüket, ami például akkor
  fontos, ha egy closure-t többször, egyidejűleg hívunk meg.

Nézzük meg az `Option<T>` `unwrap_or_else` metódusának definícióját, amelyet a
13-1. kódrészletben használtunk:

```rust,ignore
impl<T> Option<T> {
    pub fn unwrap_or_else<F>(self, f: F) -> T
    where
        F: FnOnce() -> T
    {
        match self {
            Some(x) => x,
            None => f(),
        }
    }
}
```

Emlékezz vissza, hogy a `T` az a generikus típus, amely az `Option` `Some`
változatában lévő érték típusát jelöli. Ez a `T` típus egyben az
`unwrap_or_else` függvény visszatérési típusa is: az a kód, amely például egy
`Option<String>` értéken hívja meg az `unwrap_or_else`-t, egy `String`-et kap.

Figyeld meg azt is, hogy az `unwrap_or_else` függvénynek van egy további
generikus típusparamétere, az `F`. Az `F` az `f` nevű paraméter típusa, ez
pedig az a closure, amelyet az `unwrap_or_else` meghívásakor megadunk.

Az `F` generikus típusra megadott trait-korlát az `FnOnce() -> T`, ami azt
jelenti, hogy az `F`-nek egyszer meghívhatónak kell lennie, nem vehet át
argumentumot, és egy `T`-t kell visszaadnia. Az `FnOnce` használata a
trait-korlátban azt a megkötést fejezi ki, hogy az `unwrap_or_else` legfeljebb
egyszer hívja meg az `f`-et. Az `unwrap_or_else` törzsében láthatjuk, hogy ha
az `Option` `Some`, az `f` nem hívódik meg. Ha az `Option` `None`, az `f`
egyszer hívódik meg. Mivel minden closure megvalósítja az `FnOnce`-t, az
`unwrap_or_else` mindhárom fajta closure-t elfogadja, és a lehető
legrugalmasabb.

> Megjegyzés: Ha amit tenni szeretnénk, nem igényli egy érték elkapását a
> környezetből, closure helyett egy függvény nevét is használhatjuk ott, ahol
> valamire szükségünk van, ami megvalósítja az `Fn` traitek egyikét. Egy
> `Option<Vec<T>>` értéken például meghívhatjuk az `unwrap_or_else(Vec::new)`
> metódust, hogy egy új, üres vektort kapjunk, ha az érték `None`. A fordító
> automatikusan megvalósítja egy függvénydefinícióra az `Fn` traitek közül
> azokat, amelyek alkalmazhatók rá.

Most nézzük meg a standard könyvtár szeleteken definiált `sort_by_key`
metódusát, hogy lássuk, miben különbözik az `unwrap_or_else`-től, és miért az
`FnMut`-ot használja a `sort_by_key` trait-korlátként az `FnOnce` helyett. A
closure egy argumentumot kap: egy referenciát a szelet éppen vizsgált elemére,
és egy `K` típusú, rendezhető értéket ad vissza. Ez a függvény akkor hasznos,
ha egy szeletet az egyes elemek egy bizonyos tulajdonsága szerint akarsz
rendezni. A 13-7. kódrészletben `Rectangle` példányok listájával dolgozunk, és
a `sort_by_key` segítségével a `width` tulajdonságuk szerint növekvő sorrendbe
rendezzük őket.

<Listing number="13-7" file-name="src/main.rs" caption="Téglalapok rendezése szélesség szerint a `sort_by_key` segítségével">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-07/src/main.rs}}
```

</Listing>

Ez a kód a következőt írja ki:

```console
{{#include ../listings/ch13-functional-features/listing-13-07/output.txt}}
```

A `sort_by_key` azért vár `FnMut` closure-t, mert többször is meghívja a
closure-t: a szelet minden elemére egyszer. A `|r| r.width` closure semmit sem
kap el, nem módosít és nem mozgat ki a környezetéből, így megfelel a
trait-korlát követelményeinek.

Ezzel szemben a 13-8. kódrészlet egy olyan closure-re mutat példát, amely
csak az `FnOnce` traitet valósítja meg, mert kimozgat egy értéket a
környezetéből. A fordító nem engedi, hogy ezt a closure-t a `sort_by_key`-jel
használjuk.

<Listing number="13-8" file-name="src/main.rs" caption="Kísérlet egy `FnOnce` closure használatára a `sort_by_key`-jel">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-08/src/main.rs}}
```

</Listing>

Ez egy erőltetett, körülményes (és nem működő) módja annak, hogy
megszámoljuk, hányszor hívja meg a `sort_by_key` a closure-t a `list`
rendezése közben. A kód úgy próbálja elvégezni a számlálást, hogy a `value`-t
– egy `String`-et a closure környezetéből – a `sort_operations` vektorba
teszi. A closure elkapja a `value`-t, majd kimozgatja a closure-ből azzal,
hogy a `value` tulajdonjogát átadja a `sort_operations` vektornak. Ez a
closure egyszer hívható meg; a második hívás nem működne, mert a `value`
ekkor már nem lenne a környezetben, hogy ismét a `sort_operations`-be
tehessük! Ezért ez a closure csak az `FnOnce`-t valósítja meg. Amikor
megpróbáljuk lefordítani ezt a kódot, azt a hibát kapjuk, hogy a `value` nem
mozgatható ki a closure-ből, mert a closure-nek az `FnMut`-ot kell
megvalósítania:

```console
{{#include ../listings/ch13-functional-features/listing-13-08/output.txt}}
```

A hiba a closure törzsének arra a sorára mutat, amely kimozgatja a `value`-t a
környezetből. A javításhoz úgy kell módosítanunk a closure törzsét, hogy ne
mozgasson ki értékeket a környezetből. Ha egy számlálót tartunk a
környezetben, és a closure törzsében növeljük az értékét, az egyszerűbb módja
annak, hogy megszámoljuk, hányszor hívódik meg a closure. A 13-9.
kódrészletben lévő closure működik a `sort_by_key`-jel, mert csak egy
módosítható referenciát kap el a `num_sort_operations` számlálóra, ezért
többször is meghívható.

<Listing number="13-9" file-name="src/main.rs" caption="Egy `FnMut` closure használata a `sort_by_key`-jel megengedett.">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-09/src/main.rs}}
```

</Listing>

Az `Fn` traitek fontosak, amikor closure-öket használó függvényeket vagy
típusokat definiálunk vagy használunk. A következő részben az iterátorokról
lesz szó. Sok iterátormetódus closure-argumentumokat vár, ezért a továbbiakban
is tartsd észben a closure-ök ezen részleteit!

[unwrap-or-else]: ../std/option/enum.Option.html#method.unwrap_or_else
