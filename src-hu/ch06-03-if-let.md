## Tömör vezérlés az `if let` és a `let...else` segítségével {#concise-control-flow-with-if-let-and-letelse}

Az `if let` szintaxissal az `if` és a `let` kevésbé bőbeszédű módon
kombinálható olyan értékek kezelésére, amelyek egy mintára illeszkednek,
miközben a többit figyelmen kívül hagyjuk. Vegyük a 6-6. kódrészletben látható
programot, amely a `config_max` változóban lévő `Option<u8>` értékre illeszt,
de csak akkor akar kódot futtatni, ha az érték a `Some` változat.

<Listing number="6-6" caption="Egy `match`, amely csak akkor akar kódot futtatni, ha az érték `Some`">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-06/src/main.rs:here}}
```

</Listing>

Ha az érték `Some`, a `Some` változatban lévő értéket úgy írjuk ki, hogy a
mintában a `max` változóhoz kötjük. A `None` értékkel nem akarunk semmit sem
kezdeni. Ahhoz, hogy a `match` kifejezés elégedett legyen, egyetlen változat
feldolgozása után hozzá kell adnunk a `_ => ()` sort, ami bosszantó,
fölösleges sablonkód (boilerplate).

Ehelyett ezt rövidebben is megírhatjuk az `if let` segítségével. Az alábbi kód
ugyanúgy viselkedik, mint a 6-6. kódrészletben lévő `match`:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-12-if-let/src/main.rs:here}}
```

Az `if let` szintaxis egy mintát és egy kifejezést vár egyenlőségjellel
elválasztva. Ugyanúgy működik, mint a `match`, ahol a kifejezést a `match`
kapja meg, a minta pedig az első ága. Ebben az esetben a minta a `Some(max)`, és
a `max` a `Some`-ban lévő értékhez kötődik. Ezután a `max`-ot ugyanúgy
használhatjuk az `if let` blokk törzsében, ahogy a megfelelő `match` ágban
használtuk. Az `if let` blokkban lévő kód csak akkor fut le, ha az érték
illeszkedik a mintára.

Az `if let` használatával kevesebbet kell gépelni, kevesebb a behúzás és a
sablonkód. Elveszíted viszont a `match` által kikényszerített kimerítő
ellenőrzést, amely biztosítja, hogy egyetlen eset kezelését se felejtsd el. Az,
hogy a `match` és az `if let` közül melyiket választod, attól függ, mit csinálsz
az adott helyzetben, és hogy a tömörség megéri-e a kimerítő ellenőrzés
elvesztését.

Más szóval az `if let`-re úgy is gondolhatsz, mint egy `match` szintaktikai
cukrára (syntax sugar): olyan `match`-ére, amely kódot futtat, ha az érték
egy mintára illeszkedik, minden más értéket pedig figyelmen kívül hagy.

Az `if let` mellé `else` ágat is írhatunk. Az `else`-hez tartozó kódblokk
ugyanaz, mint ami az `if let`-tel és `else`-szel egyenértékű `match`
kifejezésben a `_` esethez tartozna. Idézd fel a 6-4. kódrészletben lévő
`Coin` enum definícióját, ahol a `Quarter` változat egy `UsState` értéket is
tárolt. Ha meg szeretnénk számolni az összes nem 25 centes érmét, amelyet
látunk, és közben a 25 centesek államát is be szeretnénk mondani, ezt egy
`match` kifejezéssel így tehetnénk meg:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-13-count-and-announce-match/src/main.rs:here}}
```

Vagy használhatunk egy `if let` és `else` kifejezést, így:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-14-count-and-announce-if-let-else/src/main.rs:here}}
```

## A „boldog úton” maradva a `let...else` segítségével {#staying-on-the-happy-path-with-letelse}

Gyakori minta, hogy ha egy érték jelen van, valamilyen számítást végzünk vele,
ellenkező esetben pedig egy alapértelmezett értéket adunk vissza. Folytatva az
`UsState` értéket tartalmazó érmés példánkat: ha valami vicceset szeretnénk
mondani attól függően, hogy milyen régi a 25 centesen szereplő állam,
bevezethetnénk az `UsState`-en egy metódust, amely ellenőrzi az állam korát,
így:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-07/src/main.rs:state}}
```

Ezután az `if let` segítségével illeszthetnénk az érme típusára, és a feltétel
törzsében bevezethetnénk egy `state` változót, ahogy a 6-7. kódrészletben.

<Listing number="6-7" caption="Annak ellenőrzése, hogy egy állam létezett-e 1900-ban, egy `if let` belsejébe ágyazott feltételekkel">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-07/src/main.rs:describe}}
```

</Listing>

Ez elvégzi a feladatot, de a munkát az `if let` utasítás törzsébe tolta, és ha
az elvégzendő munka bonyolultabb, nehéz lehet pontosan követni, hogyan
viszonyulnak egymáshoz a legfelső szintű elágazások. Kihasználhatnánk azt is,
hogy a kifejezések értéket állítanak elő: így az `if let`-ből vagy előállítjuk
a `state` értéket, vagy korán visszatérünk, ahogy a 6-8. kódrészletben.
(Valami hasonlót egy `match`-csel is megtehetnél.)

<Listing number="6-8" caption="Az `if let` használata érték előállítására vagy korai visszatérésre">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-08/src/main.rs:describe}}
```

</Listing>

Ezt viszont a maga módján szintén bosszantó követni! Az `if let` egyik ága
értéket állít elő, a másik pedig teljesen kilép a függvényből.

Hogy ezt a gyakori mintát szebben ki lehessen fejezni, a Rustban ott van a
`let...else`. A `let...else` szintaxis a bal oldalon egy mintát, a jobb oldalon
egy kifejezést vár, nagyon hasonlóan az `if let`-hez, de nincs `if` ága, csak
`else` ága. Ha a minta illeszkedik, a mintából származó értéket a külső
hatókörben köti változóhoz. Ha a minta _nem_ illeszkedik, a program az `else`
ágba lép, amelynek vissza kell térnie a függvényből.

A 6-9. kódrészletben láthatod, hogyan néz ki a 6-8. kódrészlet, ha az `if let`
helyett `let...else`-t használunk.

<Listing number="6-9" caption="A `let...else` használata a függvény vezérlési folyamatának átláthatóbbá tételére">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-09/src/main.rs:describe}}
```

</Listing>

Figyeld meg, hogy így a függvény fő törzsében a „boldog úton” (happy path)
maradunk, anélkül hogy a két ág vezérlési folyamata jelentősen eltérne
egymástól, ahogy az `if let` esetében.

Ha olyan helyzetbe kerülsz, amelyben a programod logikája túl bőbeszédű lenne
egy `match` segítségével kifejezve, ne feledd, hogy az `if let` és a
`let...else` is ott van a Rust-eszköztáradban.

## Összefoglalás {#summary}

Megnéztük, hogyan hozhatsz létre enumokkal olyan saját típusokat, amelyek egy
felsorolt értékhalmaz valamelyik elemét vehetik fel. Megmutattuk, hogyan segít
a standard könyvtár `Option<T>` típusa abban, hogy a típusrendszerrel
megelőzd a hibákat. Ha az enum értékek adatokat tartalmaznak, a `match` vagy
az `if let` segítségével nyerheted ki és használhatod ezeket az értékeket,
attól függően, hány esetet kell kezelned.

A Rust-programjaid most már struktúrák és enumok segítségével fejezhetik ki a
problématerületed fogalmait. Ha saját típusokat hozol létre az API-dban,
azzal típusbiztonságot érsz el: a fordító gondoskodik róla, hogy a függvényeid
csak olyan típusú értékeket kapjanak, amilyeneket az egyes függvények várnak.

Ahhoz, hogy jól szervezett, egyszerűen használható API-t biztosíthass a
felhasználóidnak, amely pontosan csak azt teszi elérhetővé, amire szükségük
van, most rátérünk a Rust moduljaira.
