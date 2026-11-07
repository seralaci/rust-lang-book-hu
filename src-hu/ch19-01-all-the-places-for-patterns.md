## Ahol mintákat használhatunk {#all-the-places-patterns-can-be-used}

A minták a Rustban számos helyen felbukkannak, és te is sokat használtad már
őket anélkül, hogy észrevetted volna! Ez a szakasz sorra veszi mindazokat a
helyeket, ahol minták szerepelhetnek.

### `match` ágak {#match-arms}

Ahogy a 6. fejezetben láttuk, a mintákat a `match` kifejezések ágaiban (arms)
használjuk. Formálisan a `match` kifejezés a `match` kulcsszóból, egy
illesztendő értékből és egy vagy több ágból áll; minden ág egy mintából és egy
kifejezésből tevődik össze, amely akkor fut le, ha az érték illeszkedik az ág
mintájára, így:

<!--
  Manually formatted rather than using Markdown intentionally: Markdown does not
  support italicizing code in the body of a block like this!
-->

<pre><code>match <em>VALUE</em> {
    <em>PATTERN</em> => <em>EXPRESSION</em>,
    <em>PATTERN</em> => <em>EXPRESSION</em>,
    <em>PATTERN</em> => <em>EXPRESSION</em>,
}</code></pre>

Itt van például a 6-5. kódrészlet `match` kifejezése, amely az `x` változóban
lévő `Option<i32>` értékre illeszt:

```rust,ignore
match x {
    None => None,
    Some(i) => Some(i + 1),
}
```

Ebben a `match` kifejezésben a minták a `None` és a `Some(i)`, az egyes nyilak
bal oldalán.

A `match` kifejezésekkel szemben az egyik követelmény, hogy kimerítőnek
(exhaustive) kell lenniük abban az értelemben, hogy a `match` kifejezésben
szereplő érték minden lehetőségét kezelniük kell. Az egyik módja annak, hogy
biztosan minden lehetőséget lefedj, ha az utolsó ágban egy mindent elfogó
minta (catch-all pattern) áll: például egy bármilyen értékre illeszkedő
változónév sosem vallhat kudarcot, így az összes fennmaradó esetet lefedi.

A `_` minta speciális: bármire illeszkedik, de soha nem köt az értékhez
változót, ezért gyakran használjuk az utolsó ágban. A `_` minta például akkor
lehet hasznos, ha minden nem megadott értéket figyelmen kívül szeretnél hagyni.
A `_` mintával részletesebben ennek a fejezetnek a későbbi, [„Értékek figyelmen
kívül hagyása egy mintában”][ignoring-values-in-a-pattern]<!-- ignore -->
részében foglalkozunk.

### `let` utasítások {#let-statements}

Ebben a fejezetben eddig csak a `match` és az `if let` esetében beszéltünk
kifejezetten a minták használatáról, valójában azonban más helyeken is
használtunk már mintákat, például a `let` utasításokban. Vegyük például ezt az
egyszerű változó-értékadást `let`-tel:

```rust
let x = 5;
```

Valahányszor ilyen `let` utasítást használtál, mintákat használtál, még ha
nem is tudtál róla! Formálisabban a `let` utasítás így néz ki:

<!--
  Manually formatted rather than using Markdown intentionally: Markdown does not
  support italicizing code in the body of a block like this!
-->

<pre>
<code>let <em>PATTERN</em> = <em>EXPRESSION</em>;</code>
</pre>

Az olyan utasításokban, mint a `let x = 5;`, ahol a PATTERN helyén egy
változónév áll, a változónév a minta egy különösen egyszerű formája. A Rust
összeveti a kifejezést a mintával, és hozzárendeli az értékeket az ott talált
nevekhez. A `let x = 5;` példában tehát az `x` egy minta, amely azt jelenti:
„kösd az itt illeszkedő értéket az `x` változóhoz”. Mivel az `x` név az egész
minta, ez a minta gyakorlatilag azt jelenti: „köss mindent az `x` változóhoz,
bármi legyen is az érték”.

Hogy a `let` mintaillesztő jellegét jobban lásd, nézd meg a 19-1.
kódrészletet, amely egy `let`-tel használt mintával bont szét egy tuple-t.


<Listing number="19-1" caption="Egy tuple szétbontása mintával, egyszerre három változót létrehozva">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-01/src/main.rs:here}}
```

</Listing>

Itt egy tuple-t illesztünk egy mintára. A Rust összeveti az `(1, 2, 3)` értéket
az `(x, y, z)` mintával, és látja, hogy az érték illeszkedik a mintára – azaz
mindkettőben ugyanannyi elem van –, ezért az `1`-et az `x`-hez, a `2`-t az
`y`-hoz, a `3`-at pedig a `z`-hez köti. Ezt a tuple-mintát úgy is
elképzelheted, mintha három különálló változómintát ágyazna magába.

Ha a mintában lévő elemek száma nem egyezik meg a tuple elemeinek számával, a
teljes típus nem fog egyezni, és fordítási hibát kapunk. A 19-2. kódrészlet
például egy háromelemű tuple két változóba történő szétbontására tesz
kísérletet, ami nem fog működni.

<Listing number="19-2" caption="Hibásan felépített minta, amelynek változói nem egyeznek a tuple elemeinek számával">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-02/src/main.rs:here}}
```

</Listing>

Ha megpróbáljuk lefordítani ezt a kódot, ezt a típushibát kapjuk:

```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-02/output.txt}}
```

A hiba javításához a tuple egy vagy több értékét figyelmen kívül hagyhatnánk a
`_` vagy a `..` segítségével, ahogy azt az [„Értékek figyelmen kívül hagyása
egy mintában”][ignoring-values-in-a-pattern]<!-- ignore --> részben látni
fogod. Ha az a gond, hogy túl sok változó van a mintában, a megoldás az, hogy
a változók elhagyásával egyeztetjük a típusokat, amíg a változók száma meg nem
egyezik a tuple elemeinek számával.

### Feltételes `if let` kifejezések {#conditional-if-let-expressions}

A 6. fejezetben azt tárgyaltuk, hogyan használhatjuk az `if let` kifejezéseket
főként arra, hogy rövidebben írjunk meg egy olyan `match`-et, amely csak egy
esetre illeszt. Az `if let`-hez opcionálisan tartozhat egy `else` ág is, amely
akkor futtatandó kódot tartalmaz, ha az `if let` mintája nem illeszkedik.

A 19-3. kódrészlet azt mutatja, hogy az `if let`, az `else if` és az `else if
let` kifejezéseket tetszés szerint keverhetjük is. Ez nagyobb rugalmasságot ad,
mint egy `match` kifejezés, amelyben csak egyetlen értéket vethetünk össze a
mintákkal. Ráadásul a Rust nem követeli meg, hogy egy `if let`, `else if` és
`else if let` ágakból álló sorozat feltételei összefüggjenek egymással.

A 19-3. kódrészlet kódja több feltétel ellenőrzésének sorozata alapján dönti
el, milyen színű legyen a háttered. Ebben a példában beégetett értékű
változókat hoztunk létre, amelyeket egy valódi program a felhasználói
bemenetből kaphatna.

<Listing number="19-3" file-name="src/main.rs" caption="Az `if let`, az `else if`, az `else if let` és az `else` keverése">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-03/src/main.rs}}
```

</Listing>

Ha a felhasználó megad egy kedvenc színt, az lesz a háttérszín. Ha nem ad meg
kedvenc színt, és ma kedd van, a háttérszín zöld. Egyébként, ha a felhasználó
sztringként megadja az életkorát, és azt sikerül számmá alakítanunk, a szín a
szám értékétől függően lila vagy narancssárga lesz. Ha egyik feltétel sem
teljesül, a háttérszín kék.

Ezzel a feltételes szerkezettel összetett követelményeket is kezelhetünk. Az
itt beégetett értékekkel a példa a `Using purple as the background color`
szöveget írja ki.

Láthatod, hogy az `if let` is bevezethet olyan új változókat, amelyek
árnyékolják a meglévő változókat, ugyanúgy, ahogy a `match` ágak: az `if let
Ok(age) = age` sor egy új `age` változót vezet be, amely az `Ok` változatban
lévő értéket tartalmazza, és árnyékolja a meglévő `age` változót. Ez azt
jelenti, hogy az `if age > 30` feltételt ezen a blokkon belül kell
elhelyeznünk: a két feltételt nem vonhatjuk össze
`if let Ok(age) = age && age > 30` formában. Az új `age`, amelyet a 30-hoz
akarunk hasonlítani, csak a kapcsos zárójellel kezdődő új hatókörben érvényes.

Az `if let` kifejezések hátránya, hogy a fordító nem ellenőrzi a
kimerítőséget, míg a `match` kifejezéseknél igen. Ha elhagynánk az utolsó
`else` blokkot, és így néhány esetet nem kezelnénk, a fordító nem figyelmeztetne
minket a lehetséges logikai hibára.

### `while let` feltételes ciklusok {#while-let-conditional-loops}

Az `if let`-hez hasonló felépítésű `while let` feltételes ciklus lehetővé
teszi, hogy egy `while` ciklus addig fusson, amíg egy minta továbbra is
illeszkedik. A 19-4. kódrészletben egy olyan `while let` ciklust mutatunk be,
amely szálak között küldött üzenetekre vár, de ebben az esetben `Option`
helyett egy `Result` értéket vizsgál.

<Listing number="19-4" caption="`while let` ciklus használata értékek kiírására mindaddig, amíg az `rx.recv()` `Ok` értéket ad vissza">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-04/src/main.rs:here}}
```

</Listing>

Ez a példa kiírja az `1`, a `2`, majd a `3` értéket. A `recv` metódus kiveszi
az első üzenetet a csatorna fogadó oldaláról, és egy `Ok(value)` értéket ad
vissza. Amikor a 16. fejezetben először láttuk a `recv`-et, a hibát közvetlenül
kicsomagoltuk, vagy iterátorként kezeltük egy `for` ciklussal. Ahogy azonban a
19-4. kódrészlet mutatja, a `while let` is használható, mert a `recv` metódus
minden üzenet érkezésekor `Ok` értéket ad vissza, amíg a küldő létezik, majd
`Err` értéket ad, amint a küldő oldal lekapcsolódik.

### `for` ciklusok {#for-loops}

Egy `for` ciklusban a közvetlenül a `for` kulcsszó után álló érték egy minta.
A `for x in y` esetében például az `x` a minta. A 19-5. kódrészlet bemutatja,
hogyan használhatunk mintát egy `for` ciklusban arra, hogy a ciklus részeként
szétbontsunk, vagyis részeire szedjünk egy tuple-t.


<Listing number="19-5" caption="Minta használata egy `for` ciklusban egy tuple szétbontására">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-05/src/main.rs:here}}
```

</Listing>

A 19-5. kódrészlet kódja a következőt írja ki:


```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-05/output.txt}}
```

Az iterátort az `enumerate` metódussal alakítjuk át úgy, hogy egy értéket és
annak indexét állítsa elő, egy tuple-be helyezve. Az első előállított érték a
`(0, 'a')` tuple. Amikor ezt az értéket az `(index, value)` mintára illesztjük,
az index `0`, az érték pedig `'a'` lesz, és a kimenet első sora kiíródik.


### Függvényparaméterek {#function-parameters}

A függvényparaméterek is lehetnek minták. A 19-6. kódrészlet kódja, amely egy
`foo` nevű függvényt deklarál egyetlen, `x` nevű, `i32` típusú paraméterrel,
mostanra már ismerősnek tűnhet.

<Listing number="19-6" caption="Mintákat használó paraméterek egy függvényszignatúrában">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-06/src/main.rs:here}}
```

</Listing>

Az `x` rész egy minta! Ahogy a `let` esetében, a függvény argumentumaiban is
illeszthetünk egy tuple-t a mintára. A 19-7. kódrészlet szétbontja egy tuple
értékeit, miközben átadjuk egy függvénynek.

<Listing number="19-7" file-name="src/main.rs" caption="Függvény olyan paraméterekkel, amelyek egy tuple-t bontanak szét">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-07/src/main.rs}}
```

</Listing>

Ez a kód a `Current location: (3, 5)` szöveget írja ki. A `&(3, 5)` értékek
illeszkednek a `&(x, y)` mintára, így az `x` értéke `3`, az `y` értéke pedig
`5` lesz.

A closure-ök paraméterlistájában ugyanúgy használhatunk mintákat, mint a
függvények paraméterlistájában, mert a closure-ök – ahogy a 13. fejezetben
láttuk – hasonlítanak a függvényekhez.

Most már több módját is láttad a minták használatának, de a minták nem minden
helyen működnek ugyanúgy. Bizonyos helyeken a mintáknak cáfolhatatlannak kell
lenniük, más esetekben cáfolhatók is lehetnek. A következőkben ezt a két
fogalmat tárgyaljuk.

[ignoring-values-in-a-pattern]: ch19-03-pattern-syntax.html#ignoring-values-in-a-pattern
