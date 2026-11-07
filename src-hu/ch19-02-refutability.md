## Cáfolhatóság: illeszkedhet-e egy minta {#refutability-whether-a-pattern-might-fail-to-match}

A mintáknak két fajtája van: cáfolható és cáfolhatatlan. Azok a minták, amelyek
bármilyen átadott lehetséges értékre illeszkednek, _cáfolhatatlanok
(irrefutable)_. Ilyen például az `x` a `let x = 5;` utasításban, mert az `x`
bármire illeszkedik, így nem fordulhat elő, hogy ne illeszkedjen. Azok a
minták, amelyek bizonyos lehetséges értékekre nem illeszkednek, _cáfolhatók
(refutable)_. Ilyen például a `Some(x)` az `if let Some(x) = a_value`
kifejezésben, mert ha az `a_value` változóban lévő érték `None`, nem pedig
`Some`, akkor a `Some(x)` minta nem fog illeszkedni.

A függvényparaméterek, a `let` utasítások és a `for` ciklusok csak
cáfolhatatlan mintákat fogadnak el, mert a program semmi értelmeset nem tud
tenni, ha az értékek nem illeszkednek. Az `if let` és a `while let` kifejezések,
valamint a `let...else` utasítás cáfolható és cáfolhatatlan mintákat is
elfogadnak, de a fordító figyelmeztet a cáfolhatatlan mintákra, mert ezek a
szerkezetek definíció szerint a lehetséges kudarc kezelésére szolgálnak: egy
feltételes szerkezet lényege éppen az, hogy a sikertől vagy a kudarctól
függően másképp viselkedhet.

Általában nem kell törődnöd a cáfolható és a cáfolhatatlan minták közötti
különbséggel; a cáfolhatóság fogalmát azonban ismerned kell, hogy reagálni
tudj rá, ha egy hibaüzenetben találkozol vele. Ilyenkor a kód szándékolt
viselkedésétől függően vagy a mintát, vagy azt a szerkezetet kell
megváltoztatnod, amelyben a mintát használod.

Nézzük meg egy példán, mi történik, ha cáfolható mintát próbálunk használni
ott, ahol a Rust cáfolhatatlant vár, és fordítva. A 19-8. kódrészlet egy `let`
utasítást mutat, de mintaként a `Some(x)` cáfolható mintát adtuk meg. Ahogy
sejtheted, ez a kód nem fordul le.

<Listing number="19-8" caption="Kísérlet cáfolható minta használatára a `let`-tel">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-08/src/main.rs:here}}
```

</Listing>

Ha a `some_option_value` egy `None` érték lenne, nem illeszkedne a `Some(x)`
mintára, vagyis a minta cáfolható. A `let` utasítás azonban csak cáfolhatatlan
mintát fogadhat el, mert a kód semmi érvényeset nem tudna kezdeni egy `None`
értékkel. Fordítási időben a Rust jelezni fogja, hogy cáfolható mintát
próbáltunk használni ott, ahol cáfolhatatlan minta szükséges:

```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-08/output.txt}}
```

Mivel a `Some(x)` mintával nem fedtük le (és nem is fedhettük le!) az összes
érvényes értéket, a Rust jogosan fordítási hibát ad.

Ha ott van cáfolható mintánk, ahol cáfolhatatlanra volna szükség, a mintát
használó kód módosításával javíthatjuk a hibát: a `let` helyett használhatjuk a
`let...else` szerkezetet. Így ha a minta nem illeszkedik, a kapcsos zárójelek
közötti kód kezeli az értéket. A 19-9. kódrészlet mutatja, hogyan javíthatjuk
ki a 19-8. kódrészlet kódját.

<Listing number="19-9" caption="A `let...else` és egy blokk használata cáfolható mintákkal a `let` helyett">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-09/src/main.rs:here}}
```

</Listing>

Adtunk a kódnak egy kiutat! Ez a kód teljesen érvényes, bár azt jelenti, hogy
cáfolhatatlan mintát nem használhatunk figyelmeztetés nélkül. Ha a
`let...else`-nek olyan mintát adunk, amely mindig illeszkedik – például az
`x`-et, ahogy a 19-10. kódrészlet mutatja –, a fordító figyelmeztetést ad.

<Listing number="19-10" caption="Kísérlet cáfolhatatlan minta használatára a `let...else`-szel">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-10/src/main.rs:here}}
```

</Listing>

A Rust jelzi, hogy nincs értelme a `let...else`-t cáfolhatatlan mintával
használni, mert az `else` ágra sosem kerül sor:

```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-10/output.txt}}
```

Ezért a match ágaknak cáfolható mintákat kell használniuk, kivéve az utolsó
ágat, amelynek egy cáfolhatatlan mintával kell illeszkednie az összes
fennmaradó értékre. A Rust megengedi, hogy egyetlen ágból álló `match`-ben
cáfolhatatlan mintát használjunk, de ez a szintaxis nem különösebben hasznos,
és egy egyszerűbb `let` utasítással helyettesíthető.

Most, hogy már tudod, hol használhatsz mintákat, és mi a különbség a
cáfolható és a cáfolhatatlan minták között, vegyük sorra a minták
létrehozására szolgáló összes szintaxist.
