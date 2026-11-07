# Félelem nélküli konkurencia {#fearless-concurrency}

A konkurens programozás biztonságos és hatékony kezelése a Rust egy másik fő
célja. A _konkurens programozás (concurrent programming)_, amelyben a program
különböző részei egymástól függetlenül futnak, és a _párhuzamos programozás
(parallel programming)_, amelyben a program különböző részei egy időben
futnak, egyre fontosabbá válik, ahogy egyre több számítógép használja ki a
több processzorát. Ilyen környezetben programozni történetileg nehéz volt, és
könnyen vezetett hibákhoz. A Rust ezen szeretne változtatni.

A Rust csapata kezdetben úgy gondolta, hogy a memóriabiztonság garantálása és
a konkurenciából fakadó problémák megelőzése két külön feladat, amelyeket
eltérő módszerekkel kell megoldani. Idővel a csapat rájött, hogy a
tulajdonjog és a típusrendszer olyan hatékony eszközkészlet, amely a
memóriabiztonsági _és_ a konkurenciaproblémák kezelésében is segít! A
tulajdonjog és a típusellenőrzés kihasználásával a Rustban sok konkurenciahiba
fordítási idejű hiba, nem pedig futásidejű. Ezért ahelyett, hogy rengeteg
időt kellene töltened azoknak a pontos körülményeknek a reprodukálásával,
amelyek között egy futásidejű konkurenciahiba fellép, a hibás kód le sem
fordul, és a fordító a problémát elmagyarázó hibaüzenetet ad. Így a kódodat
még munka közben javíthatod, nem pedig esetleg csak azután, hogy éles
környezetbe került. A Rustnak ezt a tulajdonságát _félelem nélküli
konkurenciának (fearless concurrency)_ neveztük el. A félelem nélküli
konkurencia lehetővé teszi, hogy rejtett hibáktól mentes kódot írj, amely
könnyen refaktorálható anélkül, hogy új hibákat vinnél bele.

> Megjegyzés: Az egyszerűség kedvéért sok problémát egyszerűen _konkurensnek_
> nevezünk, ahelyett, hogy pontosabban _konkurensnek és/vagy párhuzamosnak_
> mondanánk. Ebben a fejezetben kérjük, gondolatban helyettesítsd a
> _konkurens_ szót a _konkurens és/vagy párhuzamos_ kifejezéssel. A következő
> fejezetben, ahol a különbségnek nagyobb a jelentősége, pontosabbak leszünk.

Sok nyelv dogmatikusan ragaszkodik a konkurens problémák kezelésére kínált
saját megoldásaihoz. Az Erlang például elegáns eszközöket kínál az
üzenetküldéses konkurenciához, a szálak közötti állapotmegosztásra viszont csak
körülményes módokat ad. A lehetséges megoldásoknak csak egy részét támogatni
észszerű stratégia a magasabb szintű nyelveknél, mert egy magasabb szintű
nyelv azt ígéri, hogy az irányítás egy részéről lemondva absztrakciókat
nyerünk. Az alacsonyabb szintű nyelvektől viszont azt várjuk, hogy minden
helyzetben a legjobb teljesítményű megoldást nyújtsák, és kevesebb
absztrakciót tegyenek a hardver fölé. Ezért a Rust sokféle eszközt kínál a
problémák modellezésére, bármilyen módon is illik az a helyzetedhez és az
igényeidhez.

Ebben a fejezetben a következő témákat tárgyaljuk:

- Hogyan hozhatsz létre szálakat, hogy több kódrészt egy időben futtass
- Az _üzenetküldéses (message-passing)_ konkurencia, ahol csatornák
  küldenek üzeneteket a szálak között
- A _megosztott állapotú (shared-state)_ konkurencia, ahol több szál is
  hozzáfér ugyanahhoz az adathoz
- A `Sync` és a `Send` trait, amelyek a Rust konkurenciagaranciáit a
  felhasználó által definiált típusokra és a standard könyvtár típusaira is
  kiterjesztik
