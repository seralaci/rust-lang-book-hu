# Automatizált tesztek írása {#writing-automated-tests}

Edsger W. Dijkstra 1972-es, „The Humble Programmer” (Az alázatos programozó)
című esszéjében azt írta, hogy „a programok tesztelése nagyon hatékony módja
lehet a hibák jelenlétének kimutatására, de reménytelenül alkalmatlan a
hiányuk bizonyítására”. Ez persze nem jelenti azt, hogy ne próbálnánk annyit
tesztelni, amennyit csak tudunk!

A programjaink _helyessége (correctness)_ azt jelenti, hogy a kódunk mennyire
azt csinálja, amit szánunk neki. A Rust tervezésekor nagy hangsúlyt kapott a
programok helyessége, a helyesség azonban összetett dolog, és nem könnyű
bizonyítani. Ennek a terhének jelentős részét a Rust típusrendszere viseli, de
a típusrendszer nem képes mindent kiszűrni. Ezért a Rust beépített támogatást
nyújt automatizált szoftvertesztek írásához.

Tegyük fel, hogy írunk egy `add_two` függvényt, amely 2-t ad hozzá a neki
átadott számhoz. A függvény szignatúrája egy egész számot fogad paraméterként,
és egy egész számot ad vissza eredményként. Amikor megírjuk és lefordítjuk ezt
a függvényt, a Rust elvégzi az összes eddig megismert típus- és
kölcsönzésellenőrzést, hogy például ne adhassunk át a függvénynek `String`
értéket vagy érvénytelen referenciát. A Rust azonban _nem tudja_ ellenőrizni,
hogy a függvény pontosan azt teszi-e, amit szeretnénk, vagyis a paraméter plusz
2-t adja-e vissza, és nem mondjuk a paraméter plusz 10-et vagy a paraméter
mínusz 50-et! Itt jönnek képbe a tesztek.

Írhatunk olyan teszteket, amelyek például azt ellenőrzik, hogy ha `3`-at adunk
át az `add_two` függvénynek, akkor a visszaadott érték `5`. Ezeket a teszteket
a kód minden módosításakor lefuttathatjuk, így meggyőződhetünk róla, hogy a már
meglévő helyes működés nem változott meg.

A tesztelés összetett készség: bár egyetlen fejezetben nem tudjuk a jó tesztek
írásának minden részletét lefedni, ebben a fejezetben áttekintjük a Rust
tesztelési eszközeinek működését. Szó lesz a tesztek írásakor rendelkezésedre
álló annotációkról és makrókról, a tesztek futtatásának alapértelmezett
viselkedéséről és beállítási lehetőségeiről, valamint arról, hogyan szervezheted
a teszteket _egységtesztekbe (unit tests)_ és _integrációs tesztekbe
(integration tests)_.
