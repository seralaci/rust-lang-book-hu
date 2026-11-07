# Enumok és mintaillesztés {#enums-and-pattern-matching}

Ebben a fejezetben a felsorolás típusokkal, más néven _enumokkal (enums)_
foglalkozunk. Az enumok lehetővé teszik, hogy egy típust a lehetséges
változatainak felsorolásával definiálj. Először definiálunk és használunk egy
enumot, hogy megmutassuk, hogyan hordozhat egy enum jelentést az adatok mellett.
Ezután megismerkedünk egy különösen hasznos enummal, az `Option`-nel, amely azt
fejezi ki, hogy egy érték vagy valami, vagy semmi. Majd megnézzük, hogyan teszi
a `match` kifejezésben használt mintaillesztés egyszerűvé, hogy egy enum
különböző értékeire különböző kód fusson. Végül bemutatjuk, hogy az `if let`
szerkezet egy újabb kényelmes és tömör eszköz az enumok kezelésére a kódodban.
