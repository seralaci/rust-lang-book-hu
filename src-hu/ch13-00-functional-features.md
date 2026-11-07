# Funkcionális nyelvi elemek: iterátorok és closure-ök {#functional-language-features-iterators-and-closures}

A Rust tervezése sok létező nyelvből és technikából merített ihletet, és ezek
egyik jelentős forrása a _funkcionális programozás (functional programming)_.
A funkcionális stílusú programozás gyakran azt jelenti, hogy a függvényeket
értékként használjuk: argumentumként adjuk át őket, más függvényekből adjuk
vissza őket, változókhoz rendeljük őket, hogy később végrehajtsuk őket, és így
tovább.

Ebben a fejezetben nem vitatjuk meg, mi a funkcionális programozás és mi nem
az, hanem a Rust néhány olyan nyelvi elemét tárgyaljuk, amelyek hasonlítanak
sok, gyakran funkcionálisnak nevezett nyelv nyelvi elemeire.

Pontosabban a következőkről lesz szó:

- _Closure-ök_: függvényszerű szerkezetek, amelyeket változóban tárolhatsz
- _Iterátorok_: elemsorozatok feldolgozásának egy módja
- Hogyan használhatjuk a closure-öket és az iterátorokat a 12. fejezet I/O
  projektjének továbbfejlesztésére
- A closure-ök és az iterátorok teljesítménye (előre eláruljuk: gyorsabbak,
  mint gondolnád!)

Más, szintén a funkcionális stílus hatását mutató nyelvi elemeket – például a
mintaillesztést és az enumokat – már bemutattunk. Mivel a closure-ök és az
iterátorok elsajátítása fontos része a gyors, idiomatikus Rust-kód írásának,
ezt az egész fejezetet nekik szenteljük.
