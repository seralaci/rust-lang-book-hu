## `panic!` vagy nem `panic!`? {#to-panic-or-not-to-panic}

Hogyan döntöd el tehát, mikor hívd meg a `panic!` makrót, és mikor adj vissza
`Result` értéket? Ha a kód pánikol, nincs mód a helyreállításra. Bármilyen
hibahelyzetben meghívhatnád a `panic!` makrót, akár van lehetőség a
helyreállításra, akár nincs, de ekkor te döntöd el a hívó kód helyett, hogy a
helyzet helyrehozhatatlan. Ha `Result` érték visszaadását választod, választási
lehetőséget adsz a hívó kódnak. A hívó kód dönthet úgy, hogy a saját
helyzetének megfelelő módon megpróbálja helyrehozni a hibát, vagy úgy is
dönthet, hogy az `Err` érték ebben az esetben helyrehozhatatlan, és meghívja a
`panic!` makrót, ezzel a helyrehozható hibádat helyrehozhatatlanná alakítva.
Ezért egy esetleg meghiúsuló függvény definiálásakor a `Result` visszaadása jó
alapértelmezett választás.

Olyan helyzetekben, mint a példák, a prototípuskód és a tesztek, helyénvalóbb
olyan kódot írni, amely pánikol, ahelyett hogy `Result` értéket adna vissza.
Nézzük meg, miért, majd beszéljük meg azokat a helyzeteket, amikor a fordító
nem tudja megállapítani, hogy a meghiúsulás lehetetlen, te viszont emberként
igen. A fejezet néhány általános irányelvvel zárul arról, hogyan döntsd el,
hogy egy könyvtár kódjában pánikolj-e.

### Példák, prototípuskód és tesztek {#examples-prototype-code-and-tests}

Ha egy fogalom szemléltetésére írsz példát, a robusztus hibakezelő kód
hozzáadása kevésbé áttekinthetővé teheti a példát. A példákban magától
értetődik, hogy egy esetleg pánikoló metódus, például az `unwrap` hívása
helyőrzőként szolgál annak a módnak a helyén, ahogyan az alkalmazásodban a
hibákat kezelni szeretnéd, és ez a kódod többi részétől függően eltérő lehet.

Hasonlóképpen, az `unwrap` és az `expect` metódus nagyon hasznos, amikor
prototípust készítesz, és még nem állsz készen arra, hogy eldöntsd, hogyan
kezeld a hibákat. Egyértelmű jelzéseket hagynak a kódodban arra az időre,
amikor már készen állsz arra, hogy robusztusabbá tedd a programodat.

Ha egy tesztben egy metódushívás meghiúsul, azt szeretnéd, hogy az egész teszt
meghiúsuljon, még akkor is, ha nem az adott metódus a tesztelt funkció. Mivel a
`panic!` az a mód, ahogyan egy teszt sikertelennek jelölődik, az `unwrap` vagy
az `expect` hívása pontosan az, aminek történnie kell.

<!-- Old headings. Do not remove or links may break. -->

<a id="cases-in-which-you-have-more-information-than-the-compiler"></a>

### Amikor több információd van, mint a fordítónak {#when-you-have-more-information-than-the-compiler}

Az `expect` hívása akkor is helyénvaló, ha van valamilyen más logikád, amely
biztosítja, hogy a `Result` értéke `Ok` lesz, de ezt a logikát a fordító nem
érti. Továbbra is lesz egy `Result` értéked, amelyet kezelned kell: bármilyen
műveletet hívsz is meg, az általánosságban továbbra is meghiúsulhat, még ha a
te konkrét helyzetedben ez logikailag lehetetlen is. Ha a kód kézi
átvizsgálásával biztosítani tudod, hogy soha nem kapsz `Err` változatot,
teljesen elfogadható az `expect` hívása, és az argumentum szövegében annak
dokumentálása, miért gondolod, hogy soha nem kapsz `Err` változatot. Íme egy
példa:

```rust
{{#rustdoc_include ../listings/ch09-error-handling/no-listing-08-unwrap-that-cant-fail/src/main.rs:here}}
```

Egy `IpAddr` példányt hozunk létre egy beégetett sztring elemzésével. Látjuk,
hogy a `127.0.0.1` érvényes IP-cím, ezért itt elfogadható az `expect`
használata. Egy beégetett, érvényes sztring azonban nem változtat a `parse`
metódus visszatérési típusán: továbbra is `Result` értéket kapunk, és a fordító
továbbra is megköveteli, hogy úgy kezeljük a `Result` értéket, mintha az `Err`
változat lehetséges lenne, mert a fordító nem elég okos ahhoz, hogy lássa: ez a
sztring mindig érvényes IP-cím. Ha az IP-cím sztringje a felhasználótól
származna, ahelyett hogy be lenne égetve a programba, és ezért _valóban_
fennállna a meghiúsulás lehetősége, mindenképpen robusztusabb módon
szeretnénk kezelni a `Result` értéket. Ha megemlítjük azt a feltételezést, hogy
ez az IP-cím be van égetve, az arra fog késztetni minket, hogy az `expect`
hívást jobb hibakezelő kódra cseréljük, ha a jövőben valamilyen más forrásból
kell megszereznünk az IP-címet.

### Irányelvek a hibakezeléshez {#guidelines-for-error-handling}

Tanácsos, hogy a kódod pánikoljon, ha előfordulhat, hogy rossz állapotba
kerül. Ebben a kontextusban _rossz állapot (bad state)_ az, amikor valamilyen
feltételezés, garancia, szerződés vagy invariáns sérül, például amikor
érvénytelen, ellentmondásos vagy hiányzó értékeket adnak át a kódodnak – és
emellett a következők közül egy vagy több is teljesül:

- A rossz állapot váratlan, szemben azzal, ami valószínűleg időnként
  előfordul, például amikor egy felhasználó rossz formátumban ad meg adatokat.
- A kódodnak ettől a ponttól kezdve arra kell támaszkodnia, hogy nincs ebben a
  rossz állapotban, ahelyett hogy minden lépésnél ellenőrizné a problémát.
- Nincs jó módja annak, hogy ezt az információt a használt típusokban kódold.
  Hogy mire gondolunk, azt egy példán keresztül mutatjuk be a 18. fejezet
  [„Állapotok és viselkedés kódolása típusokként”][encoding]<!-- ignore -->
  szakaszában.

Ha valaki meghívja a kódodat, és értelmetlen értékeket ad át neki, a legjobb,
ha lehetőség szerint hibát adsz vissza, hogy a könyvtár felhasználója
eldönthesse, mit szeretne tenni ebben az esetben. Olyan esetekben azonban,
amikor a folytatás nem biztonságos vagy káros lehet, a legjobb választás a
`panic!` meghívása lehet, amellyel figyelmezteted a könyvtáradat használó
személyt a kódjában lévő hibára, hogy a fejlesztés során kijavíthassa.
Hasonlóképpen, a `panic!` gyakran helyénvaló, ha olyan külső kódot hívsz, amely
nem áll az irányításod alatt, és olyan érvénytelen állapotot ad vissza, amelyet
nem tudsz kijavítani.

Ha azonban a meghiúsulás várható, helyénvalóbb `Result` értéket visszaadni,
mint `panic!` hívást végezni. Ilyen eset például, amikor egy elemző (parser)
hibás formátumú adatot kap, vagy amikor egy HTTP-kérés olyan állapotkódot ad
vissza, amely azt jelzi, hogy elérted a kéréskorlátot (rate limit). Ilyenkor a
`Result` visszaadása azt jelzi, hogy a meghiúsulás várható lehetőség, és a hívó
kódnak kell eldöntenie, hogyan kezelje.

Ha a kódod olyan műveletet végez, amely veszélybe sodorhatja a felhasználót, ha
érvénytelen értékekkel hívják meg, akkor a kódodnak először ellenőriznie kell,
hogy az értékek érvényesek-e, és pánikolnia kell, ha nem azok. Ennek
elsősorban biztonsági okai vannak: az érvénytelen adatokon végzett műveletek
sebezhetővé tehetik a kódodat. Ez a fő oka annak, hogy a standard könyvtár
meghívja a `panic!` makrót, ha határokon kívüli memóriaelérést kísérelsz meg:
az aktuális adatszerkezethez nem tartozó memória elérésének kísérlete gyakori
biztonsági probléma. A függvényeknek gyakran vannak _szerződéseik (contracts)_:
a viselkedésük csak akkor garantált, ha a bemenetek megfelelnek bizonyos
követelményeknek. A szerződés megsértésekor ésszerű pánikolni, mert a
szerződésszegés mindig a hívó oldalán lévő programhibát jelez, és ez nem olyan
fajta hiba, amelyet a hívó kódnak explicit módon kellene kezelnie. Valójában a
hívó kód számára nincs is ésszerű módja a helyreállításnak; a hívó
_programozóknak_ kell kijavítaniuk a kódot. Egy függvény szerződéseit –
különösen, ha megsértésük pánikot okoz – a függvény API-dokumentációjában kell
elmagyarázni.

Ha azonban minden függvényedben rengeteg hibaellenőrzés lenne, az bőbeszédű és
bosszantó lenne. Szerencsére a Rust típusrendszerével (és így a fordító által
végzett típusellenőrzéssel) sok ellenőrzést elvégeztethetsz. Ha a függvényednek
egy adott típusú paramétere van, a kódod logikáját abban a tudatban
folytathatod, hogy a fordító már biztosította, hogy érvényes értéked van. Ha
például `Option` helyett egy konkrét típusod van, a programod azt várja, hogy
_valami_ legyen ott, ne pedig _semmi_. A kódodnak ekkor nem kell két esetet
kezelnie a `Some` és a `None` változat számára: csak egy esete lesz, amikor
biztosan van érték. Az a kód, amely semmit sem próbál átadni a függvényednek,
le sem fordul, így a függvényednek futásidőben nem kell ezt az esetet
ellenőriznie. Egy másik példa egy előjel nélküli egész típus, például az `u32`
használata, amely biztosítja, hogy a paraméter soha nem negatív.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-custom-types-for-validation"></a>

### Egyéni típusok az ellenőrzéshez {#custom-types-for-validation}

Vigyük egy lépéssel tovább azt az ötletet, hogy a Rust típusrendszerével
biztosítjuk az érvényes értéket, és nézzük meg, hogyan hozhatunk létre egyéni
típust az ellenőrzéshez (validation). Emlékezz vissza a 2. fejezet
számkitalálós játékára, amelyben a kódunk arra kérte a felhasználót, hogy
tippeljen egy 1 és 100 közötti számra. Mielőtt a tippet összevetettük volna a
titkos számmal, soha nem ellenőriztük, hogy a felhasználó tippje e két szám
közé esik-e; csak azt ellenőriztük, hogy a tipp pozitív. Ebben az esetben a
következmények nem voltak túl súlyosak: a „Too high” vagy „Too low” kimenetünk
így is helyes lett volna. Hasznos fejlesztés lenne azonban, ha a felhasználót
érvényes tippek felé terelnénk, és másként viselkednénk, amikor a felhasználó
a tartományon kívül eső számot tippel, mint amikor például számok helyett
betűket gépel be.

Ennek egyik módja az lenne, ha a tippet csak `u32` helyett `i32` típusként
elemeznénk, hogy esetleg negatív számokat is megengedjünk, majd ellenőriznénk,
hogy a szám a tartományon belül van-e, így:

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch09-error-handling/no-listing-09-guess-out-of-range/src/main.rs:here}}
```

</Listing>

Az `if` kifejezés ellenőrzi, hogy az értékünk a tartományon kívül esik-e,
tájékoztatja a felhasználót a problémáról, és a `continue` meghívásával
elindítja a ciklus következő iterációját, újabb tippet kérve. Az `if`
kifejezés után abban a tudatban folytathatjuk a `guess` és a titkos szám
összehasonlítását, hogy a `guess` 1 és 100 között van.

Ez azonban nem ideális megoldás: ha feltétlenül szükséges lenne, hogy a program
csak 1 és 100 közötti értékekkel dolgozzon, és sok függvénye lenne ezzel a
követelménnyel, egy ilyen ellenőrzés minden függvényben fárasztó lenne (és a
teljesítményt is ronthatná).

Ehelyett létrehozhatunk egy új típust egy erre szolgáló modulban, és az
ellenőrzéseket a típus példányát létrehozó függvénybe tehetjük, ahelyett hogy
mindenhol megismételnénk őket. Így a függvények biztonságosan használhatják az
új típust a szignatúrájukban, és magabiztosan használhatják a kapott értékeket.
A 9-13. kódrészlet a `Guess` típus definiálásának egyik módját mutatja, amely
csak akkor hoz létre `Guess` példányt, ha a `new` függvény 1 és 100 közötti
értéket kap.

<Listing number="9-13" caption="Egy `Guess` típus, amely csak 1 és 100 közötti értékekkel folytatja a működést" file-name="src/guessing_game.rs">

```rust
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-13/src/guessing_game.rs}}
```

</Listing>

Figyeld meg, hogy a *src/guessing_game.rs* fájlban lévő kód feltételezi, hogy
a *src/lib.rs* fájlba felvettünk egy `mod guessing_game;` moduldeklarációt,
amelyet itt nem mutattunk meg. Ennek az új modulnak a fájljában definiálunk egy
`Guess` nevű struktúrát, amelynek van egy `i32` típusú értéket tároló, `value`
nevű mezője. Itt lesz tárolva a szám.

Ezután megvalósítunk a `Guess` típuson egy `new` nevű társított függvényt,
amely `Guess` értékek példányait hozza létre. A `new` függvény úgy van
definiálva, hogy egy `i32` típusú, `value` nevű paramétere van, és egy
`Guess` értéket ad vissza. A `new` függvény törzsében lévő kód ellenőrzi a
`value` értékét, hogy biztosan 1 és 100 között legyen. Ha a `value` nem megy át
ezen az ellenőrzésen, `panic!` hívást végzünk, amely figyelmezteti a hívó kódot
író programozót, hogy olyan programhiba van a kódjában, amelyet ki kell
javítania, hiszen egy ezen a tartományon kívül eső `value` értékkel rendelkező
`Guess` létrehozása megsértené azt a szerződést, amelyre a `Guess::new`
támaszkodik. Azokat a feltételeket, amelyek mellett a `Guess::new` pánikolhat,
a nyilvános API-dokumentációjában kell tárgyalni; a 14. fejezetben bemutatjuk
azokat a dokumentációs konvenciókat, amelyekkel az általad készített
API-dokumentációban jelezheted a `panic!` lehetőségét. Ha a `value` átmegy az
ellenőrzésen, létrehozunk egy új `Guess` értéket, amelynek `value` mezője a
`value` paraméter értékét kapja, és visszaadjuk a `Guess` értéket.

Ezután megvalósítunk egy `value` nevű metódust, amely kölcsönveszi a `self`
értéket, nincs más paramétere, és egy `i32` értéket ad vissza. Az ilyen fajta
metódust néha _getternek_ nevezik, mert a célja az, hogy a mezőiből kinyerjen
valamilyen adatot, és visszaadja azt. Erre a nyilvános metódusra azért van
szükség, mert a `Guess` struktúra `value` mezője privát. Fontos, hogy a `value`
mező privát legyen, hogy a `Guess` struktúrát használó kód ne állíthassa be
közvetlenül a `value` értékét: a `guessing_game` modulon kívüli kódnak a
`Guess::new` függvényt _kell_ használnia egy `Guess` példány létrehozásához,
így biztosítva, hogy egy `Guess` ne rendelkezhessen olyan `value` értékkel,
amelyet a `Guess::new` függvény feltételei nem ellenőriztek.

Egy olyan függvény, amelynek paramétere vagy visszatérési értéke csak 1 és 100
közötti szám lehet, a szignatúrájában ezután deklarálhatja, hogy `i32` helyett
`Guess` értéket fogad vagy ad vissza, és a törzsében nem kell további
ellenőrzéseket végeznie.

## Összefoglalás {#summary}

A Rust hibakezelő eszközei arra szolgálnak, hogy segítsenek robusztusabb kódot
írni. A `panic!` makró azt jelzi, hogy a programod olyan állapotban van,
amelyet nem tud kezelni, és lehetővé teszi, hogy leállítsd a folyamatot,
ahelyett hogy érvénytelen vagy helytelen értékekkel próbálnál továbbhaladni. A
`Result` enum a Rust típusrendszerét használja annak jelzésére, hogy a
műveletek olyan módon hiúsulhatnak meg, amelyből a kódod helyreállhat. A
`Result` segítségével azt is jelezheted a kódodat hívó kódnak, hogy kezelnie
kell az esetleges sikert vagy kudarcot. Ha a `panic!` makrót és a `Result`
típust a megfelelő helyzetekben használod, a kódod megbízhatóbb lesz az
elkerülhetetlen problémákkal szemben.

Most, hogy láttad, milyen hasznos módokon használja a standard könyvtár a
generikus típusokat az `Option` és a `Result` enumokban, arról lesz szó, hogyan
működnek a generikus típusok, és hogyan használhatod őket a kódodban.

[encoding]: ch18-03-oo-design-patterns.html#encoding-states-and-behavior-as-types
