<!-- Old headings. Do not remove or links may break. -->

<a id="comparing-performance-loops-vs-iterators"></a>

## Teljesítmény: ciklusok és iterátorok {#performance-in-loops-vs-iterators}

Ahhoz, hogy eldönthesd, ciklusokat vagy iterátorokat használj-e, tudnod kell,
melyik megvalósítás a gyorsabb: a `search` függvény explicit `for` ciklust
használó változata vagy az iterátoros változat.

Végeztünk egy teljesítménymérést (benchmark): Sir Arthur Conan Doyle _Sherlock
Holmes kalandjai (The Adventures of Sherlock Holmes)_ című művének teljes
szövegét betöltöttük egy `String`-be, és a _the_ szót kerestük benne. Íme a
mérés eredményei a `search` `for` ciklust használó és iterátorokat használó
változatára:

```text
test bench_search_for  ... bench:  19,620,300 ns/iter (+/- 915,700)
test bench_search_iter ... bench:  19,234,900 ns/iter (+/- 657,200)
```

A két megvalósítás teljesítménye hasonló! A mérés kódját itt nem
magyarázzuk el, mert nem az a cél, hogy bebizonyítsuk a két változat
egyenértékűségét, hanem hogy általános képet kapjunk arról, hogyan viszonyul
egymáshoz a két megvalósítás teljesítménye.

Egy átfogóbb teljesítménymérésnél különféle méretű szövegeket kellene
`contents`-ként, különböző szavakat és különböző hosszúságú szavakat
`query`-ként, valamint mindenféle egyéb változatot kipróbálnod. A lényeg a
következő: az iterátorok, noha magas szintű absztrakciót jelentenek, nagyjából
ugyanarra a kódra fordulnak le, mintha magad írtad volna meg az alacsonyabb
szintű kódot. Az iterátorok a Rust _költségmentes absztrakcióinak (zero-cost
abstractions)_ egyike, ami azt jelenti, hogy az absztrakció használata nem jár
további futásidejű többletköltséggel. Ez ahhoz hasonló, ahogyan Bjarne
Stroustrup, a C++ eredeti tervezője és megvalósítója a „zero-overhead”
(többletköltség-mentesség) fogalmát definiálja a 2012-es ETAPS konferencián
tartott „Foundations of C++” című nyitóelőadásában:

> Általánosságban a C++-megvalósítások betartják a többletköltség-mentesség
> elvét: amit nem használsz, azért nem fizetsz. Továbbá: amit használsz,
> annál jobbat kézzel sem tudnál írni.

A Rust iterátorokat használó kódja sok esetben ugyanarra az assembly kódra
fordul le, amelyet kézzel írnál. Az olyan optimalizációk, mint a
ciklus-kibontás (loop unrolling) és a tömbelérések határellenőrzésének
elhagyása, itt is érvényesülnek, és rendkívül hatékonnyá teszik az eredményül
kapott kódot. Most, hogy ezt tudod, félelem nélkül használhatod az
iterátorokat és a closure-öket! A kódot magasabb szintűnek tüntetik fel, de
ezért nem kell futásidejű teljesítménnyel fizetni.

## Összefoglalás {#summary}

A closure-ök és az iterátorok a funkcionális programozási nyelvek ötletei által
ihletett nyelvi elemei a Rustnak. Hozzájárulnak ahhoz, hogy a Rust magas
szintű gondolatokat világosan, alacsony szintű teljesítménnyel fejezhessen ki.
A closure-ök és az iterátorok megvalósítása olyan, hogy a futásidejű
teljesítményt nem befolyásolja. Ez része a Rust azon céljának, hogy
költségmentes absztrakciókat nyújtson.

Most, hogy az I/O projektünk kifejezőerejét javítottuk, nézzük meg a `cargo`
néhány további lehetőségét, amelyek segítenek megosztani a projektet a
világgal.
