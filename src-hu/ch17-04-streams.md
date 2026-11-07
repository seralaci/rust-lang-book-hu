<!-- Old headings. Do not remove or links may break. -->

<a id="streams"></a>

## Streamek: future-ök sorozatban {#streams-futures-in-sequence}

Emlékezz vissza, hogyan használtuk korábban ebben a fejezetben az async
csatornánk fogadóját az [„Üzenetküldés”][17-02-messages]<!-- ignore --> című
részben. Az async `recv` metódus idővel elemek sorozatát állítja elő. Ez egy
sokkal általánosabb minta, a _stream_ egyik példája. Sok fogalom természetes
módon streamként ábrázolható: egy sorban elérhetővé váló elemek, a
fájlrendszerből fokozatosan beolvasott adatdarabok, amikor a teljes adathalmaz
túl nagy a számítógép memóriájához, vagy a hálózaton idővel beérkező adatok.
Mivel a streamek future-ök, bármilyen más future-rel együtt használhatjuk és
érdekes módokon kombinálhatjuk őket. Például kötegelhetjük az eseményeket,
hogy elkerüljük a túl sok hálózati hívás kiváltását, időkorlátokat állíthatunk
be hosszan futó műveletek sorozataira, vagy ritkíthatjuk (throttle) a
felhasználói felület eseményeit, hogy elkerüljük a fölösleges munkát.

Elemek sorozatával már a 13. fejezetben is találkoztunk, amikor az Iterator
traitet vizsgáltuk [„Az `Iterator` trait és a `next`
metódus”][iterator-trait]<!-- ignore --> című részben, de az iterátorok és az
async csatorna fogadója között két különbség van. Az első különbség az idő: az
iterátorok szinkronok, míg a csatorna fogadója aszinkron. A második különbség
az API. Amikor közvetlenül az `Iterator`-ral dolgozunk, a szinkron `next`
metódusát hívjuk meg. A `trpl::Receiver` stream esetében viszont ehelyett egy
aszinkron `recv` metódust hívtunk meg. Ettől eltekintve ezek az API-k nagyon
hasonlónak tűnnek, és ez a hasonlóság nem véletlen. A stream olyan, mint az
iteráció aszinkron formája. Míg azonban a `trpl::Receiver` kifejezetten
üzenetek fogadására vár, az általános célú stream API sokkal tágabb: ugyanúgy
a következő elemet adja, ahogy az `Iterator`, csak aszinkron módon.

Az iterátorok és a streamek közötti hasonlóság a Rustban azt jelenti, hogy
valójában bármelyik iterátorból létrehozhatunk streamet. Ahogy egy
iterátorral, egy streammel is úgy dolgozhatunk, hogy meghívjuk a `next`
metódusát, majd bevárjuk a kimenetet, ahogy a 17-21. kódrészletben, amely még
nem fordul le.

<Listing number="17-21" caption="Stream létrehozása egy iterátorból, és az értékeinek kiírása" file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-21/src/main.rs:stream}}
```

</Listing>

Egy számokból álló tömbbel kezdünk, amelyet iterátorrá alakítunk, majd
meghívjuk rajta a `map`-et, hogy minden értéket megduplázzunk. Ezután a
`trpl::stream_from_iter` függvénnyel az iterátort streammé alakítjuk. Végül a
`while let` ciklussal végigmegyünk a stream elemein, ahogy megérkeznek.

Sajnos amikor megpróbáljuk futtatni a kódot, az nem fordul le, hanem azt
jelzi, hogy nem érhető el `next` metódus:

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-21
cargo build
copy only the error output
-->

```text
error[E0599]: no method named `next` found for struct `tokio_stream::iter::Iter` in the current scope
  --> src/main.rs:10:40
   |
10 |         while let Some(value) = stream.next().await {
   |                                        ^^^^
   |
   = help: items from traits can only be used if the trait is in scope
help: the following traits which provide `next` are implemented but not in scope; perhaps you want to import one of them
   |
1  + use crate::trpl::StreamExt;
   |
1  + use futures_util::stream::stream::StreamExt;
   |
1  + use std::iter::Iterator;
   |
1  + use std::str::pattern::Searcher;
   |
help: there is a method `try_next` with a similar name
   |
10 |         while let Some(value) = stream.try_next().await {
   |                                        ~~~~~~~~
```

Ahogy ez a kimenet elmagyarázza, a fordítási hiba oka az, hogy a `next` metódus
használatához a megfelelő traitnek hatókörben kell lennie. Az eddigiek alapján
joggal várhatnád, hogy ez a trait a `Stream`, valójában azonban a
`StreamExt`. Az `Ext` az _extension_ (kiterjesztés) rövidítése, és gyakori
minta a Rust-közösségben arra, hogy egy traitet egy másikkal bővítsenek.

A `Stream` trait egy alacsony szintű interfészt definiál, amely gyakorlatilag az
`Iterator` és a `Future` traitet egyesíti. A `StreamExt` egy magasabb szintű
API-készletet biztosít a `Stream` fölött, beleértve a `next` metódust, valamint
más, az `Iterator` trait által biztosítottakhoz hasonló segédmetódusokat. A
`Stream` és a `StreamExt` még nem része a Rust standard könyvtárának, de az
ökoszisztéma legtöbb crate-je hasonló definíciókat használ.

A fordítási hibát úgy javíthatjuk, hogy hozzáadunk egy `use` utasítást a
`trpl::StreamExt`-hez, ahogy a 17-22. kódrészletben.

<Listing number="17-22" caption="Egy iterátor sikeres használata egy stream alapjaként" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-22/src/main.rs:all}}
```

</Listing>

Ezekkel a darabokkal összerakva ez a kód úgy működik, ahogy szeretnénk! Sőt,
most, hogy a `StreamExt` hatókörben van, az összes segédmetódusát
használhatjuk, ugyanúgy, mint az iterátoroknál.

[17-02-messages]: ch17-02-concurrency-with-async.html#message-passing
[iterator-trait]: ch13-02-iterators.html#the-iterator-trait-and-the-next-method
