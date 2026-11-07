# Okos mutatók {#smart-pointers}

A _mutató (pointer)_ általános fogalom: olyan változót jelent, amely egy
memóriacímet tartalmaz. Ez a cím valamilyen más adatra hivatkozik, vagyis arra
„mutat”. A Rustban a mutatók leggyakoribb fajtája a referencia, amelyet a 4.
fejezetben ismertél meg. A referenciákat a `&` szimbólum jelöli, és kölcsönzik
azt az értéket, amelyre mutatnak. Az adatra való hivatkozáson kívül nincs
semmilyen különleges képességük, és nincs többletköltségük sem.

Az _okos mutatók (smart pointers)_ ezzel szemben olyan adatszerkezetek, amelyek
mutatóként viselkednek, de további metaadatokkal és képességekkel is
rendelkeznek. Az okos mutatók fogalma nem a Rust sajátja: a C++-ból származnak,
és más nyelvekben is léteznek. A Rust standard könyvtárában többféle okos
mutató is definiálva van, amelyek a referenciákon túlmutató funkcionalitást
nyújtanak. Az általános fogalom felfedezéséhez megnézünk néhány különböző okos
mutatót, köztük egy _referenciaszámláló (reference counting)_ okos
mutatótípust. Ez a mutató lehetővé teszi, hogy egy adatnak több tulajdonosa
legyen: nyilvántartja a tulajdonosok számát, és amikor már egy sem marad,
felszabadítja az adatot.

A Rustban, a tulajdonjog és a kölcsönzés fogalma miatt, van egy további
különbség is a referenciák és az okos mutatók között: míg a referenciák csak
kölcsönzik az adatot, az okos mutatók sok esetben _birtokolják_ azt az adatot,
amelyre mutatnak.

Az okos mutatókat általában struktúrákkal valósítjuk meg. A közönséges
struktúrákkal ellentétben az okos mutatók megvalósítják a `Deref` és a `Drop`
traitet. A `Deref` trait lehetővé teszi, hogy az okos mutató struktúra egy
példánya referenciaként viselkedjen, így a kódodat úgy írhatod meg, hogy
referenciákkal és okos mutatókkal egyaránt működjön. A `Drop` trait lehetővé
teszi, hogy testre szabd azt a kódot, amely akkor fut le, amikor az okos mutató
egy példánya kikerül a hatókörből. Ebben a fejezetben mindkét traitet
tárgyaljuk, és megmutatjuk, miért fontosak az okos mutatók szempontjából.

Mivel az okos mutató minta egy általános, a Rustban gyakran használt tervezési
minta, ez a fejezet nem tárgyal minden létező okos mutatót. Sok könyvtárnak
megvannak a saját okos mutatói, sőt akár sajátot is írhatsz. A standard
könyvtár leggyakoribb okos mutatóit vesszük sorra:

- a `Box<T>`-t, amellyel értékeket foglalhatunk le a kupacon
- az `Rc<T>`-t, egy referenciaszámláló típust, amely lehetővé teszi a
  többszörös tulajdonjogot
- a `Ref<T>`-t és a `RefMut<T>`-t, amelyeket a `RefCell<T>`-n keresztül érünk
  el; ez utóbbi típus fordítási idő helyett futásidőben kényszeríti ki a
  kölcsönzési szabályokat

Emellett a _belső módosíthatóság (interior mutability)_ mintáját is
tárgyaljuk, amelyben egy nem módosítható típus olyan API-t biztosít, amellyel
egy belső érték módosítható. Szót ejtünk a referenciaciklusokról is: arról,
hogyan okozhatnak memóriaszivárgást, és hogyan előzhetjük meg őket.

Vágjunk bele!
