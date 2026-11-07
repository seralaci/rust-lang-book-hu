<!-- Old headings. Do not remove or links may break. -->

<a id="managing-growing-projects-with-packages-crates-and-modules"></a>

# Csomagok, crate-ek és modulok {#packages-crates-and-modules}

Ahogy egyre nagyobb programokat írsz, a kód rendszerezése egyre fontosabbá
válik. Ha az összetartozó funkciókat csoportosítod, a különálló feladatokat
ellátó kódot pedig szétválasztod, egyértelmű lesz, hol találod egy adott
funkció megvalósítását, és hová kell nyúlnod, ha meg akarod változtatni a
működését.

Az eddig megírt programjaink egyetlen fájl egyetlen moduljában voltak. Ahogy
egy projekt növekszik, érdemes a kódot több modulra, majd több fájlra
szétosztva rendszerezni. Egy csomag több bináris crate-et és legfeljebb egy
könyvtár crate-et tartalmazhat. Ahogy a csomag növekszik, egyes részeit külön
crate-ekbe emelheted ki, amelyek külső függőségekké válnak. Ez a fejezet
ezeket a technikákat mutatja be. Az egymással összefüggő, együtt fejlődő
csomagokból álló, nagyon nagy projektekhez a Cargo-munkaterületeket
(workspaces) kínál; ezekről a 14. fejezet
[„Cargo-munkaterületek”][workspaces]<!-- ignore --> szakaszában lesz szó.

Szó lesz a megvalósítás részleteinek elrejtéséről (egységbezárásáról) is,
amely lehetővé teszi, hogy a kódot magasabb szinten használd újra: ha
egyszer megvalósítottál egy műveletet, más kód a nyilvános interfészén
keresztül hívhatja anélkül, hogy tudnia kellene, hogyan működik a
megvalósítás. A kód megírásának módja határozza meg, mely részek nyilvánosak,
vagyis más kód számára használhatók, és melyek a privát megvalósítási
részletek, amelyek megváltoztatásának jogát fenntartod magadnak. Ez is egy
módja annak, hogy kevesebb részletet kelljen fejben tartanod.

Ehhez kapcsolódó fogalom a hatókör: a kód beágyazott környezetéhez, amelyben
íródik, tartozik egy névhalmaz, amelyről azt mondjuk, hogy „hatókörben van”. A
kód olvasásakor, írásakor és fordításakor a programozóknak és a fordítóknak
tudniuk kell, hogy egy adott helyen egy adott név változóra, függvényre,
struktúrára, enumra, modulra, konstansra vagy más elemre hivatkozik-e, és mit
jelent az az elem. Létrehozhatsz hatóköröket, és megváltoztathatod, mely nevek
vannak hatókörben, illetve azon kívül. Ugyanabban a hatókörben nem lehet két
azonos nevű elem; a névütközések feloldására eszközök állnak rendelkezésre.

A Rustnak számos nyelvi eleme segíti a kód szerkezetének kezelését, beleértve
azt is, hogy mely részletek láthatók kívülről, melyek privátok, és milyen nevek
vannak az egyes hatókörökben a programjaidban. Ezek a nyelvi elemek, amelyeket
néha összefoglalóan _modulrendszernek (module system)_ nevezünk, a
következők:

* **Csomagok (packages)**: a Cargo egy funkciója, amellyel crate-eket
  buildelhetsz, tesztelhetsz és oszthatsz meg
* **Crate-ek**: modulok fája, amelyből egy könyvtár vagy futtatható állomány
  készül
* **Modulok és a use**: lehetővé teszik az útvonalak szervezésének,
hatókörének és láthatóságának szabályozását
* **Útvonalak (paths)**: egy elem, például egy struktúra, függvény vagy modul
  megnevezésének módja

Ebben a fejezetben mindezeket a nyelvi elemeket bemutatjuk, megvizsgáljuk,
hogyan hatnak egymásra, és elmagyarázzuk, hogyan kezelheted velük a
hatókört. A végére szilárdan meg fogod érteni a modulrendszert, és profi
módon bánsz majd a hatókörökkel!

[workspaces]: ch14-03-cargo-workspaces.html
