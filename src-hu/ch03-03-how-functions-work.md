## Függvények {#functions}

A függvények mindenütt jelen vannak a Rust-kódban. Már láttad a nyelv egyik
legfontosabb függvényét: a `main` függvényt, amely sok program belépési
pontja. Láttad az `fn` kulcsszót is, amellyel új függvényeket deklarálhatsz.

A Rust-kód a függvény- és változónevekhez a _snake case_ stílust használja,
amelyben minden betű kisbetű, a szavakat pedig aláhúzásjel választja el. Íme
egy program, amely egy példa függvénydefiníciót tartalmaz:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-16-functions/src/main.rs}}
```

A Rustban úgy definiálunk egy függvényt, hogy beírjuk az `fn` kulcsszót, majd
a függvény nevét és egy zárójelpárt. A kapcsos zárójelek jelzik a fordítónak,
hol kezdődik és hol végződik a függvény törzse.

Bármelyik általunk definiált függvényt meghívhatjuk úgy, hogy beírjuk a nevét,
majd egy zárójelpárt. Mivel az `another_function` definiálva van a programban,
a `main` függvényen belülről meghívható. Figyeld meg, hogy az
`another_function`-t a forráskódban a `main` függvény _után_ definiáltuk;
definiálhattuk volna előtte is. A Rustot nem érdekli, hol definiálod a
függvényeidet, csak az, hogy valahol olyan hatókörben legyenek definiálva,
amelyet a hívó lát.

Indítsunk egy új, _functions_ nevű bináris projektet, hogy tovább
ismerkedjünk a függvényekkel. Tedd az `another_function` példát az
_src/main.rs_ fájlba, és futtasd. A következő kimenetet kell látnod:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-16-functions/output.txt}}
```

A sorok abban a sorrendben hajtódnak végre, ahogyan a `main` függvényben
szerepelnek. Először a „Hello, world!” üzenet íródik ki, majd meghívódik az
`another_function`, és kiíródik az ő üzenete.

### Paraméterek {#parameters}

A függvényeket _paraméterekkel (parameters)_ is definiálhatjuk; ezek olyan
különleges változók, amelyek a függvény szignatúrájának részei. Ha egy
függvénynek vannak paraméterei, konkrét értékeket adhatsz meg nekik.
Technikailag ezeket a konkrét értékeket _argumentumoknak (arguments)_
nevezzük, de a hétköznapi beszédben a _paraméter_ és az _argumentum_ szót
gyakran felcserélhetően használják, akár a függvény definíciójában szereplő
változókra, akár a függvény hívásakor átadott konkrét értékekre.

Az `another_function` következő változatában egy paramétert adunk hozzá:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-17-functions-with-parameters/src/main.rs}}
```

Próbáld meg futtatni ezt a programot; a következő kimenetet kell kapnod:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-17-functions-with-parameters/output.txt}}
```

Az `another_function` deklarációjában egy `x` nevű paraméter szerepel. Az `x`
típusa `i32`. Amikor az `5`-öt átadjuk az `another_function`-nek, a `println!`
makró az `5`-öt arra a helyre teszi a formázási sztringben, ahol az `x`-et
tartalmazó kapcsos zárójelpár volt.

A függvényszignatúrákban _kötelező_ megadni minden paraméter típusát. Ez a Rust
tervezésének tudatos döntése: mivel a függvénydefiníciókban kötelező a
típusannotáció, a fordítónak szinte soha nincs szüksége arra, hogy a kód más
részein is használd őket ahhoz, hogy kitalálja, milyen típusra gondolsz. A
fordító hasznosabb hibaüzeneteket is tud adni, ha tudja, milyen típusokat vár
a függvény.

Több paraméter definiálásakor a paraméterdeklarációkat vesszővel válaszd el,
így:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-18-functions-with-multiple-parameters/src/main.rs}}
```

Ez a példa egy `print_labeled_measurement` nevű, kétparaméteres függvényt hoz
létre. Az első paraméter neve `value`, és `i32` típusú. A második neve
`unit_label`, és `char` típusú. A függvény ezután egy olyan szöveget ír ki,
amely a `value`-t és a `unit_label`-t is tartalmazza.

Próbáljuk meg futtatni ezt a kódot. Cseréld le a _functions_ projekted
_src/main.rs_ fájljában lévő programot az előző példára, és futtasd a
`cargo run` paranccsal:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-18-functions-with-multiple-parameters/output.txt}}
```

Mivel a függvényt az `5` értékkel hívtuk meg a `value` paraméterhez és a `'h'`
értékkel a `unit_label` paraméterhez, a program kimenete ezeket az értékeket
tartalmazza.

### Utasítások és kifejezések {#statements-and-expressions}

A függvénytörzsek utasítások sorozatából állnak, amelyet opcionálisan egy
kifejezés zár. Az eddig tárgyalt függvények nem tartalmaztak záró kifejezést,
de már láttál kifejezést egy utasítás részeként. Mivel a Rust kifejezésalapú
nyelv, ezt a különbséget fontos megérteni. Más nyelvekben nincsenek ugyanilyen
megkülönböztetések, ezért nézzük meg, mik az utasítások és a kifejezések, és
hogyan befolyásolják a különbségeik a függvények törzsét.

- Az _utasítások (statements)_ olyan utasítások, amelyek valamilyen műveletet
  végeznek, és nem adnak vissza értéket.
- A _kifejezések (expressions)_ kiértékelésük eredményeként egy értéket adnak.

Nézzünk néhány példát.

Valójában már használtunk utasításokat és kifejezéseket. Egy változó
létrehozása és értékadása a `let` kulcsszóval utasítás. A 3-1. kódrészletben
a `let y = 6;` egy utasítás.

<Listing number="3-1" file-name="src/main.rs" caption="Egy `main` függvény deklarációja, amely egyetlen utasítást tartalmaz">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-01/src/main.rs}}
```

</Listing>

A függvénydefiníciók is utasítások; az előző teljes példa önmagában egy
utasítás. (Ahogy hamarosan látni fogjuk, a függvény meghívása viszont nem
utasítás.)

Az utasítások nem adnak vissza értéket. Ezért egy `let` utasítást nem adhatsz
értékül egy másik változónak, ahogy a következő kód próbálja; hibát fogsz
kapni:

<span class="filename">Fájlnév: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-19-statements-vs-expressions/src/main.rs}}
```

Ha futtatod ezt a programot, a kapott hiba így néz ki:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-19-statements-vs-expressions/output.txt}}
```

A `let y = 6` utasítás nem ad vissza értéket, így nincs mihez kötni az `x`-et.
Ez eltér attól, ami más nyelvekben, például a C-ben és a Rubyban történik, ahol
az értékadás visszaadja a hozzárendelt értéket. Ezekben a nyelvekben írhatod
azt, hogy `x = y = 6`, és ekkor az `x` és az `y` értéke is `6` lesz; a Rustban
ez nem így van.

A kifejezések kiértékelésük eredményeként egy értéket adnak, és a Rustban írt
kódod nagy részét ezek alkotják. Vegyünk egy matematikai műveletet, például az
`5 + 6`-ot, amely egy `11` értékre kiértékelődő kifejezés. A kifejezések
utasítások részei is lehetnek: a 3-1. kódrészletben a `let y = 6;`
utasításban szereplő `6` egy kifejezés, amely a `6` értékre értékelődik ki.
Egy függvény meghívása kifejezés. Egy makró meghívása kifejezés. A kapcsos
zárójelekkel létrehozott új hatóköri blokk is kifejezés, például:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-20-blocks-are-expressions/src/main.rs}}
```

Ez a kifejezés:

```rust,ignore
{
    let x = 3;
    x + 1
}
```

egy blokk, amely ebben az esetben a `4` értékre értékelődik ki. Ez az érték a
`let` utasítás részeként az `y`-hoz kötődik. Figyeld meg, hogy az `x + 1`
sor végén nincs pontosvessző, ellentétben az eddig látott sorok többségével. A
kifejezések végén nincs pontosvessző. Ha egy kifejezés végére pontosvesszőt
teszel, utasítássá alakítod, és akkor nem ad vissza értéket. Tartsd ezt észben,
amikor a következőkben a függvények visszatérési értékeivel és a kifejezésekkel
ismerkedsz.

### Visszatérési értékkel rendelkező függvények {#functions-with-return-values}

A függvények értékeket adhatnak vissza az őket hívó kódnak. A visszatérési
értékeket nem nevezzük el, de a típusukat egy nyíl (`->`) után meg kell adnunk.
A Rustban a függvény visszatérési értéke ugyanaz, mint a függvénytörzs
blokkjában szereplő utolsó kifejezés értéke. A `return` kulcsszóval és egy
érték megadásával korábban is visszatérhetsz egy függvényből, de a legtöbb
függvény implicit módon az utolsó kifejezést adja vissza. Íme egy példa egy
értéket visszaadó függvényre:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-21-function-return-values/src/main.rs}}
```

A `five` függvényben nincs függvényhívás, makró, de még `let` utasítás sem –
csak maga az `5` szám. Ez a Rustban teljesen érvényes függvény. Figyeld meg,
hogy a függvény visszatérési típusa is meg van adva, `-> i32` formában.
Próbáld meg futtatni ezt a kódot; a kimenetnek így kell kinéznie:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-21-function-return-values/output.txt}}
```

A `five`-ban szereplő `5` a függvény visszatérési értéke, ezért `i32` a
visszatérési típus. Vizsgáljuk meg ezt részletesebben. Két fontos dolog van:
először is a `let x = five();` sor azt mutatja, hogy egy függvény visszatérési
értékét használjuk egy változó inicializálására. Mivel a `five` függvény `5`-öt
ad vissza, ez a sor ugyanaz, mint a következő:

```rust
let x = 5;
```

Másodszor, a `five` függvénynek nincsenek paraméterei, és megadja a
visszatérési érték típusát, a függvény törzse viszont egy magányos `5`,
pontosvessző nélkül, mert ez egy kifejezés, amelynek értékét vissza szeretnénk
adni.

Nézzünk egy másik példát:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-22-function-parameter-and-return/src/main.rs}}
```

A kód futtatása a `The value of x is: 6` szöveget írja ki. De mi történik, ha
az `x + 1`-et tartalmazó sor végére pontosvesszőt teszünk, és ezzel
kifejezésből utasítássá alakítjuk?

<span class="filename">Fájlnév: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-23-statements-dont-return-values/src/main.rs}}
```

A kód fordítása a következő hibát eredményezi:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-23-statements-dont-return-values/output.txt}}
```

A fő hibaüzenet, a `mismatched types`, rávilágít a kód alapvető problémájára.
A `plus_one` függvény definíciója szerint a függvény `i32`-t ad vissza, az
utasítások azonban nem értékelődnek ki értékre, amit a `()`, a unit típus
fejez ki. Ezért semmi sem kerül visszaadásra, ami ellentmond a függvény
definíciójának, és hibát eredményez. Ebben a kimenetben a Rust egy üzenettel
próbál segíteni a probléma orvoslásában: azt javasolja, hogy távolítsd el a
pontosvesszőt, ami kijavítaná a hibát.
