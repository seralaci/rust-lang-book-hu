## Parancssori argumentumok fogadása {#accepting-command-line-arguments}

Hozzunk létre egy új projektet, mint mindig, a `cargo new` paranccsal. A
projektünket `minigrep`-nek nevezzük el, hogy megkülönböztessük a `grep`
eszköztől, amely talán már a rendszereden is megvan:

```console
$ cargo new minigrep
     Created binary (application) `minigrep` project
$ cd minigrep
```

Az első feladat az, hogy a `minigrep` fogadja a két parancssori argumentumát:
a fájl elérési útját és a keresendő sztringet. Vagyis azt szeretnénk, hogy a
programunkat a `cargo run` paranccsal futtathassuk, utána két kötőjellel
jelezzük, hogy a következő argumentumok a programunknak szólnak, nem a
`cargo`-nak, majd megadjuk a keresendő sztringet és annak a fájlnak az
elérési útját, amelyben keresni szeretnénk, így:

```console
$ cargo run -- searchstring example-filename.txt
```

Jelenleg a `cargo new` által generált program nem tudja feldolgozni a neki
átadott argumentumokat. A [crates.io](https://crates.io/) oldalon található
néhány könyvtár segíthet a parancssori argumentumokat fogadó programok
megírásában, de mivel most tanulod ezt a témát, valósítsuk meg ezt a
képességet magunk.

### Az argumentumok értékeinek beolvasása {#reading-the-argument-values}

Ahhoz, hogy a `minigrep` be tudja olvasni a neki átadott parancssori
argumentumok értékét, a Rust standard könyvtárában található
`std::env::args` függvényre lesz szükségünk. Ez a függvény a `minigrep`-nek
átadott parancssori argumentumok iterátorát adja vissza. Az iterátorokat a
[13. fejezetben][ch13]<!-- ignore --> tárgyaljuk részletesen. Egyelőre elég
két dolgot tudnod róluk: az iterátorok értékek sorozatát állítják elő, és egy
iterátoron meghívhatjuk a `collect` metódust, hogy gyűjteménnyé – például
vektorrá – alakítsuk, amely az iterátor által előállított összes elemet
tartalmazza.

A 12-1. kódrészletben látható kód lehetővé teszi, hogy a `minigrep` program
beolvassa a neki átadott parancssori argumentumokat, majd az értékeket egy
vektorba gyűjtse.

<Listing number="12-1" file-name="src/main.rs" caption="A parancssori argumentumok vektorba gyűjtése és kiírása">

```rust
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-01/src/main.rs}}
```

</Listing>

Először egy `use` utasítással hatókörbe hozzuk az `std::env` modult, hogy
használhassuk az `args` függvényét. Figyeld meg, hogy az `std::env::args`
függvény két modulszint mélyen van beágyazva. Ahogy a
[7. fejezetben][ch7-idiomatic-use]<!-- ignore --> megbeszéltük, ha a kívánt
függvény egynél több modulba van beágyazva, nem magát a függvényt, hanem a
szülőmodulját hozzuk hatókörbe. Így az `std::env` többi függvényét is
könnyen használhatjuk. Ez egyértelműbb is, mint ha `use std::env::args`
sort írnánk, majd a függvényt csupán `args` néven hívnánk meg, mert az
`args`-ot könnyen összetéveszthetnénk egy, az aktuális modulban definiált
függvénnyel.

> ### Az `args` függvény és az érvénytelen Unicode {#the-args-function-and-invalid-unicode}
>
> Vedd figyelembe, hogy az `std::env::args` pánikol, ha bármelyik argumentum
> érvénytelen Unicode-ot tartalmaz. Ha a programodnak érvénytelen Unicode-ot
> tartalmazó argumentumokat is el kell fogadnia, használd helyette az
> `std::env::args_os` függvényt. Ez olyan iterátort ad vissza, amely `String`
> helyett `OsString` értékeket állít elő. Az egyszerűség kedvéért választottuk
> itt az `std::env::args`-ot, mert az `OsString` értékek platformonként
> eltérnek, és bonyolultabb velük dolgozni, mint a `String` értékekkel.

A `main` első sorában meghívjuk az `env::args` függvényt, és azonnal a
`collect` segítségével vektorrá alakítjuk az iterátort, amely az iterátor által
előállított összes értéket tartalmazza. A `collect` függvénnyel sokféle
gyűjteményt létrehozhatunk, ezért az `args` típusát kifejezetten annotáljuk,
jelezve, hogy sztringek vektorát szeretnénk. Bár a Rustban nagyon ritkán kell
típusokat annotálnod, a `collect` azon függvények egyike, amelyeknél gyakran
szükség van rá, mert a Rust nem tudja kikövetkeztetni, milyen gyűjteményt
szeretnél.

Végül a debug makróval kiírjuk a vektort. Próbáljuk ki a kódot először
argumentumok nélkül, majd két argumentummal:

```console
{{#include ../listings/ch12-an-io-project/listing-12-01/output.txt}}
```

```console
{{#include ../listings/ch12-an-io-project/output-only-01-with-args/output.txt}}
```

Figyeld meg, hogy a vektor első értéke `"target/debug/minigrep"`, ami a
binárisunk neve. Ez a C argumentumlistájának viselkedését követi, és
lehetővé teszi, hogy a programok futás közben használhassák azt a nevet,
amellyel meghívták őket. Gyakran kényelmes hozzáférni a program nevéhez,
ha ki szeretnéd írni üzenetekben, vagy ha a program viselkedését aszerint
szeretnéd módosítani, hogy melyik parancssori álnévvel hívták meg. Ennek a
fejezetnek a céljaira azonban figyelmen kívül hagyjuk, és csak a szükséges két
argumentumot mentjük el.

### Az argumentumok értékeinek mentése változókba {#saving-the-argument-values-in-variables}

A program jelenleg hozzáfér a parancssori argumentumként megadott
értékekhez. Most a két argumentum értékét változókba kell mentenünk, hogy a
program többi részében használhassuk őket. Ezt a 12-2. kódrészletben tesszük
meg.

<Listing number="12-2" file-name="src/main.rs" caption="Változók létrehozása a keresett kifejezést és a fájl elérési útját tartalmazó argumentum tárolására">

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-02/src/main.rs}}
```

</Listing>

Ahogy a vektor kiírásakor láttuk, a vektor első értékét, az `args[0]`-t a
program neve foglalja el, ezért az argumentumokat az 1-es indextől kezdjük. A
`minigrep` első argumentuma a keresett sztring, ezért az első argumentumra
mutató referenciát a `query` változóba tesszük. A második argumentum a fájl
elérési útja lesz, ezért a második argumentumra mutató referenciát a
`file_path` változóba tesszük.

Ideiglenesen kiírjuk ezeknek a változóknak az értékét, hogy igazoljuk: a kód
úgy működik, ahogy szeretnénk. Futtassuk újra a programot a `test` és a
`sample.txt` argumentummal:

```console
{{#include ../listings/ch12-an-io-project/listing-12-02/output.txt}}
```

Remek, a program működik! A szükséges argumentumok értékei a megfelelő
változókba kerülnek. Később hibakezelést is hozzáadunk, hogy kezeljünk
bizonyos lehetséges hibás helyzeteket, például azt, amikor a felhasználó nem
ad meg argumentumot; egyelőre ezt a helyzetet figyelmen kívül hagyjuk, és
inkább a fájlbeolvasás képességén dolgozunk.

[ch13]: ch13-00-functional-features.html
[ch7-idiomatic-use]: ch07-04-bringing-paths-into-scope-with-the-use-keyword.html#creating-idiomatic-use-paths
