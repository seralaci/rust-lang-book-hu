# Összetartozó adatok rendezése struktúrákkal {#using-structs-to-structure-related-data}

A _struktúra (struct, structure)_ egy egyedi adattípus, amellyel több,
egymáshoz kapcsolódó, együtt értelmes csoportot alkotó értéket foghatsz össze
és nevezhetsz el. Ha ismersz valamilyen objektumorientált nyelvet, a struktúra
olyan, mint egy objektum adatattribútumai. Ebben a fejezetben összevetjük a
tuple-öket a struktúrákkal, hogy arra építsünk, amit már tudsz, és megmutassuk,
mikor jobb választás a struktúra az adatok csoportosítására.

Bemutatjuk, hogyan definiálhatsz és példányosíthatsz struktúrákat.
Megbeszéljük, hogyan definiálhatsz _társított függvényeket (associated
functions)_, különösen a _metódusoknak (methods)_ nevezett társított
függvényeket, amelyekkel egy struktúratípushoz kapcsolódó viselkedést adhatsz
meg. A struktúrák és az enumok (ezekről a 6. fejezetben lesz szó) azok az
építőkövek, amelyekkel a programod tárgyterületének új típusait hozhatod létre,
hogy teljes mértékben kihasználhasd a Rust fordítási idejű típusellenőrzését.
