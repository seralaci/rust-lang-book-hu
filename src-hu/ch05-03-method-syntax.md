## Metódusok {#methods}

A metódusok a függvényekhez hasonlítanak: az `fn` kulcsszóval és
egy névvel deklaráljuk őket, lehetnek paramétereik és visszatérési értékük, és
olyan kódot tartalmaznak, amely akkor fut le, amikor a metódust valahonnan
meghívják. A függvényekkel ellentétben a metódusokat egy struktúra
kontextusában definiáljuk (vagy egy enum, illetve egy trait objektum
kontextusában, amelyekkel [a 6. fejezetben][enums]<!-- ignore --> és [a 18.
fejezetben][trait-objects]<!-- ignore --> foglalkozunk), és az első
paraméterük mindig a `self`, amely a struktúrának azt a példányát jelöli,
amelyen a metódust meghívjuk.

<!-- Old headings. Do not remove or links may break. -->

<a id="defining-methods"></a>

### Metódusszintaxis {#method-syntax}

Alakítsuk át a `Rectangle` példányt paraméterként kapó `area` függvényt egy, a
`Rectangle` struktúrán definiált `area` metódussá, ahogy az 5-13. kódrészlet
mutatja.

<Listing number="5-13" file-name="src/main.rs" caption="Egy `area` metódus definiálása a `Rectangle` struktúrán">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-13/src/main.rs}}
```

</Listing>

Ahhoz, hogy a függvényt a `Rectangle` kontextusában definiáljuk, egy `impl`
(implementációs) blokkot nyitunk a `Rectangle` számára. Ebben az `impl`
blokkban minden a `Rectangle` típushoz lesz társítva. Ezután az `area`
függvényt áthelyezzük az `impl` kapcsos zárójelei közé, és az első (ebben az
esetben egyetlen) paramétert `self`-re változtatjuk a szignatúrában és a
törzsben mindenhol. A `main`-ben, ahol eddig az `area` függvényt hívtuk meg, és
a `rect1`-et adtuk át argumentumként, most a _metódusszintaxissal (method
syntax)_ hívhatjuk meg az `area` metódust a `Rectangle` példányunkon. A
metódusszintaxis a példány után következik: egy pontot írunk, majd a metódus
nevét, zárójeleket és az esetleges argumentumokat.

Az `area` szignatúrájában a `rectangle: &Rectangle` helyett a `&self` formát
használjuk. A `&self` valójában a `self: &Self` rövidítése. Egy `impl` blokkon
belül a `Self` típus annak a típusnak az álneve, amelyhez az `impl` blokk
tartozik. A metódusok első paraméterének egy `Self` típusú, `self` nevű
paraméternek kell lennie, ezért a Rust megengedi, hogy az első paraméter helyén
ezt egyszerűen a `self` névvel rövidítsd. Figyeld meg, hogy a `self` rövidítés
elé továbbra is ki kell írnunk a `&` jelet, jelezve, hogy ez a metódus
kölcsönveszi a `Self` példányt, ahogy a `rectangle: &Rectangle` esetében is
tettük. A metódusok – ahogy bármely más paraméterüket – a `self`-et is
átvehetik tulajdonként, kölcsönvehetik nem módosíthatóan, ahogy itt tettük,
vagy kölcsönvehetik módosíthatóan.

Itt ugyanazért választottuk a `&self` formát, amiért a függvényes változatban a
`&Rectangle` típust használtuk: nem akarjuk átvenni a tulajdonjogot,
és csak olvasni szeretnénk a struktúra adatait, írni nem. Ha a metódus
működésének részeként módosítani szeretnénk a példányt, amelyen meghívtuk,
első paraméterként a `&mut self` formát használnánk. Ritka az olyan metódus,
amely azzal veszi át a példány tulajdonjogát, hogy első paraméterként csak a
`self` szerepel; ezt a technikát általában akkor használjuk, amikor a metódus a
`self`-et valami mássá alakítja, és meg akarjuk akadályozni, hogy a hívó az
átalakítás után az eredeti példányt használja.

A metódusok függvények helyetti használatának fő oka – azon túl, hogy
metódusszintaxist kapunk, és nem kell minden metódus szignatúrájában
megismételni a `self` típusát – a kód szervezése. Mindent, amit egy típus
példányával tehetünk, egyetlen `impl` blokkba tettünk, ahelyett hogy a kódunk
jövőbeli felhasználóinak a `Rectangle` képességeit az általunk biztosított
könyvtár különböző pontjain kellene keresgélniük.

Figyeld meg, hogy egy metódusnak a struktúra valamelyik mezőjével azonos nevet
is adhatunk. Definiálhatunk például a `Rectangle`-ön egy szintén `width` nevű
metódust:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-06-method-field-interaction/src/main.rs:here}}
```

</Listing>

Itt úgy döntünk, hogy a `width` metódus `true` értéket adjon vissza, ha a
példány `width` mezőjének értéke nagyobb `0`-nál, és `false` értéket, ha az
érték `0`: egy azonos nevű metóduson belül a mezőt bármilyen célra
használhatjuk. Amikor a `main`-ben a `rect1.width` után zárójeleket írunk, a
Rust tudja, hogy a `width` metódusra gondolunk. Ha nem írunk zárójeleket, a
Rust tudja, hogy a `width` mezőre gondolunk.

Gyakran, de nem mindig, ha egy metódusnak egy mezővel azonos nevet adunk, azt
szeretnénk, hogy csak a mező értékét adja vissza, és semmi mást ne tegyen. Az
ilyen metódusokat _getter_-eknek nevezzük, és a Rust – néhány más nyelvvel
ellentétben – nem hozza létre őket automatikusan a struktúra mezőihez. A
getterek azért hasznosak, mert a mezőt privátnak, a metódust viszont
nyilvánosnak tehetjük, így a típus nyilvános API-jának részeként csak olvasási
hozzáférést biztosíthatunk a mezőhöz. Arról, hogy mit jelent a nyilvános és a
privát, és hogyan jelölhetünk egy mezőt vagy metódust nyilvánosnak vagy
privátnak, [a 7. fejezetben][public]<!-- ignore --> lesz szó.

> ### Hol van a `->` operátor? {#wheres-the---operator}
>
> A C-ben és a C++-ban két különböző operátorral hívhatunk metódusokat: a `.`
> operátort használjuk, ha közvetlenül az objektumon hívunk meg egy metódust,
> és a `->` operátort, ha az objektumra mutató mutatón hívjuk meg a metódust,
> és előbb dereferálnunk kell a mutatót. Másként fogalmazva: ha az `object`
> egy mutató, az `object->something()` hasonló az `(*object).something()`
> kifejezéshez.
>
> A Rustban nincs a `->` operátornak megfelelő operátor; ehelyett a Rustban van
> egy _automatikus referenciaképzés és dereferálás (automatic referencing and
> dereferencing)_ nevű nyelvi elem. A metódushívás egyike azon kevés helynek a
> Rustban, ahol ez a viselkedés érvényesül.
>
> Így működik: amikor az `object.something()` formában hívsz meg egy metódust,
> a Rust automatikusan hozzáadja a `&`, `&mut` vagy `*` jelet, hogy az `object`
> illeszkedjen a metódus szignatúrájához. Másként fogalmazva, a következő két
> sor ugyanazt jelenti:
>
> <!-- CAN'T EXTRACT SEE BUG https://github.com/rust-lang/mdBook/issues/1127 -->
>
> ```rust
> # #[derive(Debug,Copy,Clone)]
> # struct Point {
> #     x: f64,
> #     y: f64,
> # }
> #
> # impl Point {
> #    fn distance(&self, other: &Point) -> f64 {
> #        let x_squared = f64::powi(other.x - self.x, 2);
> #        let y_squared = f64::powi(other.y - self.y, 2);
> #
> #        f64::sqrt(x_squared + y_squared)
> #    }
> # }
> # let p1 = Point { x: 0.0, y: 0.0 };
> # let p2 = Point { x: 5.0, y: 6.5 };
> p1.distance(&p2);
> (&p1).distance(&p2);
> ```
>
> Az első sokkal áttekinthetőbb. Ez az automatikus referenciaképzés azért
> működik, mert a metódusoknak egyértelmű fogadójuk (receiver) van – a `self`
> típusa. A fogadó és a metódus neve alapján a Rust egyértelműen el tudja
> dönteni, hogy a metódus olvas (`&self`), módosít (`&mut self`) vagy felemészt
> (`self`). Az, hogy a Rust a metódusok fogadójánál implicitté teszi a
> kölcsönzést, nagyban hozzájárul ahhoz, hogy a tulajdonjog
> kezelése a gyakorlatban kényelmes legyen.

### Metódusok több paraméterrel {#methods-with-more-parameters}

Gyakoroljuk a metódusok használatát egy második metódus megvalósításával a
`Rectangle` struktúrán. Ezúttal azt szeretnénk, hogy a `Rectangle` egy példánya
egy másik `Rectangle` példányt kapjon, és `true` értéket adjon vissza, ha a
második `Rectangle` teljes egészében elfér a `self`-ben (az első
`Rectangle`-ben); ellenkező esetben `false` értéket adjon vissza. Vagyis a
`can_hold` metódus definiálása után az 5-14. kódrészletben látható programot
szeretnénk megírni.

<Listing number="5-14" file-name="src/main.rs" caption="A még meg nem írt `can_hold` metódus használata">

```rust,ignore
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-14/src/main.rs}}
```

</Listing>

A várt kimenet a következő, mert a `rect2` mindkét mérete kisebb a `rect1`
méreteinél, a `rect3` viszont szélesebb a `rect1`-nél:

```text
Can rect1 hold rect2? true
Can rect1 hold rect3? false
```

Tudjuk, hogy egy metódust szeretnénk definiálni, így az az `impl Rectangle`
blokkban lesz. A metódus neve `can_hold` lesz, és paraméterként egy másik
`Rectangle` nem módosítható kölcsönzését kapja. A paraméter típusát a metódust
meghívó kódból olvashatjuk ki: a `rect1.can_hold(&rect2)` hívás a `&rect2`
értéket adja át, ami a `rect2`-nek, egy `Rectangle` példánynak a nem
módosítható kölcsönzése. Ez ésszerű, mert a `rect2`-t csak olvasnunk kell
(írnunk nem, ahhoz módosítható kölcsönzésre lenne szükség), és azt szeretnénk,
hogy a `main` megtartsa a `rect2` tulajdonjogát, hogy a `can_hold` metódus
meghívása után újra használhassuk. A `can_hold` visszatérési értéke logikai
érték lesz, a megvalósítás pedig azt ellenőrzi, hogy a `self` szélessége és
magassága nagyobb-e a másik `Rectangle` szélességénél, illetve magasságánál.
Adjuk hozzá az új `can_hold` metódust az 5-13. kódrészlet `impl` blokkjához,
ahogy az 5-15. kódrészlet mutatja.

<Listing number="5-15" file-name="src/main.rs" caption="A `can_hold` metódus megvalósítása a `Rectangle`-ön; a metódus egy másik `Rectangle` példányt kap paraméterként">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-15/src/main.rs:here}}
```

</Listing>

Ha ezt a kódot az 5-14. kódrészlet `main` függvényével futtatjuk, a kívánt
kimenetet kapjuk. A metódusok több paramétert is kaphatnak, ezeket a
szignatúrában a `self` paraméter után adjuk meg, és pontosan úgy működnek, mint
a függvények paraméterei.

### Társított függvények {#associated-functions}

Az `impl` blokkon belül definiált összes függvényt _társított függvénynek
(associated function)_ nevezzük, mert az `impl` után megnevezett típushoz
vannak társítva. Olyan társított függvényeket is definiálhatunk, amelyeknek az
első paramétere nem a `self` (így nem metódusok), mert nincs szükségük a típus
egy példányára a működésükhöz. Egy ilyen függvényt már használtunk is: a
`String` típuson definiált `String::from` függvényt.

A metódusnak nem számító társított függvényeket gyakran konstruktorként
használjuk, amelyek a struktúra egy új példányát adják vissza. Ezeket gyakran
`new`-nak nevezik, de a `new` nem különleges név, és nincs beépítve a nyelvbe.
Dönthetünk például úgy, hogy biztosítunk egy `square` nevű társított függvényt,
amely egyetlen méretparamétert kap, és azt használja szélességként és
magasságként is, így könnyebben hozhatunk létre négyzet alakú `Rectangle`-t,
anélkül hogy ugyanazt az értéket kétszer kellene megadnunk:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-03-associated-functions/src/main.rs:here}}
```

A visszatérési típusban és a függvény törzsében szereplő `Self` kulcsszavak az
`impl` kulcsszó után álló típus álnevei, ami ebben az esetben a `Rectangle`.

A társított függvény meghívásához a `::` szintaxist használjuk a struktúra
nevével; erre példa a `let sq = Rectangle::square(3);` sor. Ez a függvény a
struktúra névterébe tartozik: a `::` szintaxist a társított függvényekhez és a
modulok által létrehozott névterekhez is használjuk. A modulokról [a 7.
fejezetben][modules]<!-- ignore --> lesz szó.

### Több `impl` blokk {#multiple-impl-blocks}

Minden struktúrának lehet több `impl` blokkja is. Az 5-15. kódrészlet például
egyenértékű az 5-16. kódrészletben látható kóddal, amelyben minden metódus a
saját `impl` blokkjában van.

<Listing number="5-16" caption="Az 5-15. kódrészlet átírása több `impl` blokk használatával">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-16/src/main.rs:here}}
```

</Listing>

Itt semmi okunk nincs arra, hogy ezeket a metódusokat több `impl` blokkra
osszuk szét, de a szintaxis érvényes. A 10. fejezetben, ahol a generikus
típusokról és a traitekről lesz szó, látni fogunk egy olyan esetet, amelyben a
több `impl` blokk hasznos.

## Összefoglalás {#summary}

A struktúrákkal olyan egyedi típusokat hozhatsz létre, amelyek a te
tárgyterületeden értelmesek. A struktúrák használatával az összetartozó
adatelemeket összekapcsolva tarthatod, és minden elemnek nevet adhatsz, hogy a
kódod világos legyen. Az `impl` blokkokban a típusodhoz társított függvényeket
definiálhatsz, a metódusok pedig a társított függvények egy olyan fajtája,
amellyel megadhatod, hogyan viselkedjenek a struktúráid példányai.

A struktúrák azonban nem az egyetlen módja az egyedi típusok létrehozásának:
térjünk rá a Rust enumjaira, hogy egy újabb eszközzel bővítsük az
eszköztáradat.

[enums]: ch06-00-enums.html
[trait-objects]: ch18-02-trait-objects.md
[public]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html#exposing-paths-with-the-pub-keyword
[modules]: ch07-02-defining-modules-to-control-scope-and-privacy.html
