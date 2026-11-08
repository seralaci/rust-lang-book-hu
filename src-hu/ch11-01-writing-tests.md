## Hogyan írjunk teszteket? {#how-to-write-tests}

A _tesztek (tests)_ olyan Rust-függvények, amelyek azt ellenőrzik, hogy a nem
tesztelésre szolgáló kód az elvárt módon működik-e. A tesztfüggvények törzse
általában az alábbi három lépést végzi el:

- Előkészíti a szükséges adatokat vagy állapotot.
- Lefuttatja a tesztelni kívánt kódot.
- Ellenőrzi, hogy az eredmények megfelelnek-e az elvárásainknak.

Nézzük meg, milyen eszközöket biztosít a Rust kifejezetten az ilyen lépéseket
végző tesztek írásához: ezek közé tartozik a `test` attribútum, néhány makró és
a `should_panic` attribútum.

<!-- Old headings. Do not remove or links may break. -->

<a id="the-anatomy-of-a-test-function"></a>

### A tesztfüggvények felépítése {#structuring-test-functions}

A legegyszerűbb esetben a Rustban egy teszt egy olyan függvény, amelyet a `test`
_attribútummal (attribute)_ jelöltünk meg. Az attribútumok a Rust-kód egyes
részeihez tartozó metaadatok; ilyen például a `derive` attribútum, amelyet az 5.
fejezetben a struktúráknál használtunk. Ahhoz, hogy egy függvényből
tesztfüggvény legyen, írd a `#[test]` sort az `fn` elé. Amikor a `cargo test`
paranccsal futtatod a teszteket, a Rust lefordít egy _tesztfuttató (test
runner)_ binárist, amely lefuttatja a megjelölt függvényeket, és jelenti, hogy
az egyes tesztfüggvények sikeresek vagy sikertelenek lettek.

Valahányszor új könyvtárprojektet hozunk létre a Cargóval, automatikusan
létrejön egy tesztmodul is, benne egy tesztfüggvénnyel. Ez a modul sablont ad a
tesztek írásához, így nem kell minden új projekt indításakor kikeresned a
pontos szerkezetet és szintaxist. Annyi további tesztfüggvényt és tesztmodult
adhatsz hozzá, amennyit csak szeretnél!

Mielőtt ténylegesen bármilyen kódot tesztelnénk, a sablonként kapott teszttel
kísérletezve megvizsgáljuk a tesztek működésének néhány aspektusát. Utána
valódi teszteket írunk, amelyek meghívják az általunk írt kódot, és
ellenőrzik, hogy helyesen viselkedik-e.

Hozzunk létre egy új, `adder` nevű könyvtárprojektet, amely két számot ad
össze:

```console
$ cargo new adder --lib
     Created library `adder` project
$ cd adder
```

Az `adder` könyvtárad _src/lib.rs_ fájljának tartalma a 11-1. kódrészlethez
hasonlóan kell, hogy kinézzen.

<Listing number="11-1" file-name="src/lib.rs" caption="A `cargo new` által automatikusan generált kód">

<!-- manual-regeneration
cd listings/ch11-writing-automated-tests
rm -rf listing-11-01
cargo new listing-11-01 --lib --name adder
cd listing-11-01
echo "$ cargo test" > output.txt
RUSTFLAGS="-A unused_variables -A dead_code" RUST_TEST_THREADS=1 cargo test >> output.txt 2>&1
git diff output.txt # commit any relevant changes; discard irrelevant ones
cd ../../..
-->

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-01/src/lib.rs}}
```

</Listing>

A fájl egy példa `add` függvénnyel kezdődik, hogy legyen mit tesztelnünk.

Egyelőre koncentráljunk csak az `it_works` függvényre. Figyeld meg a `#[test]`
annotációt: ez az attribútum jelzi, hogy tesztfüggvényről van szó, így a
tesztfuttató tudja, hogy tesztként kell kezelnie. A `tests` modulban lehetnek
nem teszt jellegű függvények is, amelyek gyakori helyzetek előkészítésében vagy
gyakori műveletek elvégzésében segítenek, ezért mindig jelölnünk kell, mely
függvények a tesztek.

A példafüggvény törzse az `assert_eq!` makróval ellenőrzi, hogy a `result`,
amely az `add` 2-vel és 2-vel történő meghívásának eredményét tartalmazza,
egyenlő-e 4-gyel. Ez az _állítás (assertion)_ jól mutatja egy tipikus teszt
felépítését. Futtassuk le, és nézzük meg, hogy a teszt sikeres-e.

A `cargo test` parancs a projekt összes tesztjét lefuttatja, ahogy a 11-2.
kódrészlet mutatja.

<Listing number="11-2" caption="Az automatikusan generált teszt futtatásának kimenete">

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-01/output.txt}}
```

</Listing>

A Cargo lefordította és lefuttatta a tesztet. Látjuk a `running 1 test` sort. A
következő sor a generált tesztfüggvény nevét mutatja – ez `tests::it_works` –,
valamint azt, hogy a teszt futtatásának eredménye `ok`. Az összesítő `test
result: ok.` azt jelenti, hogy minden teszt sikeres volt, az `1 passed; 0
failed` rész pedig összesíti a sikeres és a sikertelen tesztek számát.

Egy tesztet kihagyottként is megjelölhetünk, hogy bizonyos esetekben ne fusson
le; erről a fejezet későbbi, [„Tesztek kihagyása, ha nem kérjük kifejezetten a
futtatásukat”][ignoring]<!-- ignore --> című szakaszában lesz szó. Mivel itt
ezt nem tettük meg, az összesítés `0 ignored`-ot mutat. A `cargo test`
parancsnak argumentumot is átadhatunk, hogy csak azokat a teszteket futtassa,
amelyeknek a neve illeszkedik egy adott sztringre; ezt _szűrésnek (filtering)_
nevezzük, és [„A tesztek egy részének futtatása név
alapján”][subset]<!-- ignore --> című szakaszban foglalkozunk vele. Itt nem
szűrtük a futtatott teszteket, így az összesítés végén `0 filtered out` áll.

A `0 measured` statisztika a teljesítményt mérő benchmarktesztekre vonatkozik.
A benchmarktesztek e sorok írásakor csak a nightly Rustban érhetők el. További
információért lásd [a benchmarktesztek dokumentációját][bench].

A tesztkimenet következő, `Doc-tests adder` sorral kezdődő része a
dokumentációs tesztek eredményeit tartalmazza. Dokumentációs tesztjeink még
nincsenek, de a Rust képes lefordítani az API-dokumentációnkban szereplő
kódpéldákat. Ez a funkció segít szinkronban tartani a dokumentációt és a kódot!
A dokumentációs tesztek írásáról a 14. fejezet [„Dokumentációs kommentek mint
tesztek”][doc-comments]<!-- ignore --> című szakaszában lesz szó. Egyelőre
figyelmen kívül hagyjuk a `Doc-tests` kimenetet.

Kezdjük el a saját igényeinkhez igazítani a tesztet. Először nevezzük át az
`it_works` függvényt valami másra, például `exploration`-re, így:

<span class="filename">Fájlnév: src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-01-changing-test-name/src/lib.rs}}
```

Ezután futtasd újra a `cargo test` parancsot. A kimenetben most `it_works`
helyett `exploration` szerepel:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-01-changing-test-name/output.txt}}
```

Most hozzáadunk egy újabb tesztet, de ezúttal olyat, amely elbukik! A tesztek
akkor buknak el, ha a tesztfüggvényben valami pánikol. Minden teszt egy új
szálban fut, és amikor a fő szál azt látja, hogy egy tesztszál leállt, a tesztet
sikertelennek jelöli. A 9. fejezetben szó volt róla, hogy a pánikolás
legegyszerűbb módja a `panic!` makró meghívása. Írd be az új tesztet egy
`another` nevű függvényként, hogy az _src/lib.rs_ fájlod a 11-3. kódrészlethez
hasonlóan nézzen ki.

<Listing number="11-3" file-name="src/lib.rs" caption="Egy második teszt hozzáadása, amely elbukik, mert meghívjuk a `panic!` makrót">

```rust,panics,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-03/src/lib.rs}}
```

</Listing>

Futtasd újra a teszteket a `cargo test` paranccsal. A kimenetnek a 11-4.
kódrészlethez hasonlóan kell kinéznie, amely azt mutatja, hogy az `exploration`
teszt sikeres volt, az `another` pedig elbukott.

<Listing number="11-4" caption="A teszteredmények, amikor az egyik teszt sikeres, a másik elbukik">

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-03/output.txt}}
```

</Listing>

<!-- manual-regeneration
rg panicked listings/ch11-writing-automated-tests/listing-11-03/output.txt
check the line number of the panic matches the line number in the following paragraph
 -->

Az `ok` helyett a `test tests::another` sorban `FAILED` áll. Az egyes
eredmények és az összesítés között két új szakasz jelenik meg: az első minden
sikertelen tesztnél részletesen kiírja a hiba okát. Ebben az esetben azt
tudjuk meg, hogy a `tests::another` azért bukott el, mert az _src/lib.rs_ fájl
17. sorában a `Make this test fail` üzenettel pánikolt. A következő szakasz
csak a sikertelen tesztek nevét sorolja fel, ami akkor hasznos, ha sok tesztünk
és sok részletes hibakimenetünk van. Egy sikertelen teszt nevével csak azt az
egy tesztet futtathatjuk le, hogy könnyebben megtaláljuk a hibát; a tesztek
futtatásának módjairól bővebben [„A tesztek futtatásának
szabályozása”][controlling-how-tests-are-run]<!-- ignore --> című szakaszban
lesz szó.

A végén az összesítő sor jelenik meg: a teszteredményünk összességében
`FAILED`. Egy tesztünk sikeres volt, egy pedig elbukott.

Most, hogy láttad, hogyan néznek ki a teszteredmények különböző helyzetekben,
nézzünk meg néhány olyan makrót a `panic!`-en kívül, amelyek hasznosak a
tesztekben.

<!-- Old headings. Do not remove or links may break. -->

<a id="checking-results-with-the-assert-macro"></a>

### Eredmények ellenőrzése az `assert!` makróval {#checking-results-with-assert}

A standard könyvtár által biztosított `assert!` makró akkor hasznos, ha meg
akarunk győződni arról, hogy egy feltétel a tesztben `true` értékre értékelődik
ki. Az `assert!` makrónak egy logikai értékre kiértékelődő argumentumot adunk.
Ha az érték `true`, semmi sem történik, és a teszt sikeres. Ha az érték
`false`, az `assert!` makró meghívja a `panic!`-et, és a teszt elbukik. Az
`assert!` makró segítségével ellenőrizhetjük, hogy a kódunk a szándékunk
szerint működik.

Az 5. fejezet 5-15. kódrészletében egy `Rectangle` struktúrát és egy
`can_hold` metódust használtunk; ezeket a 11-5. kódrészlet megismétli. Tegyük
ezt a kódot az _src/lib.rs_ fájlba, majd írjunk hozzá néhány tesztet az
`assert!` makróval.

<Listing number="11-5" file-name="src/lib.rs" caption="A `Rectangle` struktúra és a `can_hold` metódusa az 5. fejezetből">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-05/src/lib.rs}}
```

</Listing>

A `can_hold` metódus logikai értéket ad vissza, vagyis tökéletes alkalmazási
terület az `assert!` makró számára. A 11-6. kódrészletben olyan tesztet írunk,
amely kipróbálja a `can_hold` metódust: létrehoz egy 8 szélességű és 7
magasságú `Rectangle` példányt, és ellenőrzi, hogy belefér-e egy
másik, 5 szélességű és 1 magasságú `Rectangle` példányt.

<Listing number="11-6" file-name="src/lib.rs" caption="Teszt a `can_hold` metódushoz, amely ellenőrzi, hogy egy nagyobb téglalapba valóban belefér-e egy kisebb">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-06/src/lib.rs:here}}
```

</Listing>

Figyeld meg a `use super::*;` sort a `tests` modulban. A `tests` modul egy
szokásos modul, amely a 7. fejezet [„Útvonalak a modulfa elemeire való
hivatkozáshoz”][paths-for-referring-to-an-item-in-the-module-tree]<!--
ignore -->
című szakaszában tárgyalt láthatósági szabályokat követi. Mivel a `tests` modul
belső modul, a külső modulban lévő, tesztelendő kódot be kell hoznunk a belső
modul hatókörébe. Itt globot használunk, így minden, amit a külső modulban
definiálunk, elérhető ebben a `tests` modulban.

A tesztünket `larger_can_hold_smaller`-nek neveztük el, és létrehoztuk a két
szükséges `Rectangle` példányt. Ezután meghívtuk az `assert!` makrót, és
átadtuk neki a `larger.can_hold(&smaller)` hívás eredményét. Ennek a
kifejezésnek `true`-t kell visszaadnia, így a tesztünknek sikeresnek kell
lennie. Nézzük meg!

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-06/output.txt}}
```

Valóban sikeres! Adjunk hozzá még egy tesztet, ezúttal azt ellenőrizve, hogy
egy kisebb téglalapba nem fér bele egy nagyobb:

<span class="filename">Fájlnév: src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-02-adding-another-rectangle-test/src/lib.rs:here}}
```

Mivel ebben az esetben a `can_hold` függvény helyes eredménye `false`, ezt az
eredményt tagadnunk kell, mielőtt átadjuk az `assert!` makrónak. Így a
tesztünk akkor lesz sikeres, ha a `can_hold` `false`-t ad vissza:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-02-adding-another-rectangle-test/output.txt}}
```

Két sikeres teszt! Most nézzük meg, mi történik a teszteredményekkel, ha hibát
viszünk a kódunkba. Módosítsuk a `can_hold` metódus implementációját úgy, hogy
a szélességek összehasonlításakor a nagyobb jelet (`>`) kisebb jelre (`<`)
cseréljük:

```rust,not_desired_behavior,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-03-introducing-a-bug/src/lib.rs:here}}
```

A tesztek futtatása most a következőt eredményezi:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-03-introducing-a-bug/output.txt}}
```

A tesztjeink elkapták a hibát! Mivel a `larger.width` értéke `8`, a
`smaller.width` értéke pedig `5`, a szélességek összehasonlítása a `can_hold`
metódusban most `false`-t ad vissza: a 8 nem kisebb az 5-nél.

<!-- Old headings. Do not remove or links may break. -->

<a id="testing-equality-with-the-assert_eq-and-assert_ne-macros"></a>

### Egyenlőség tesztelése az `assert_eq!` és az `assert_ne!` makróval {#testing-equality-with-assert_eq-and-assert_ne}

A működés ellenőrzésének gyakori módja, hogy megvizsgáljuk, egyenlő-e a
tesztelt kód eredménye azzal az értékkel, amelyet elvárunk tőle. Ezt
megtehetnéd az `assert!` makróval is, ha egy `==` operátort használó kifejezést
adsz át neki. Ez azonban annyira gyakori teszt, hogy a standard könyvtár két
makrót – az `assert_eq!`-t és az `assert_ne!`-t – is biztosít a kényelmesebb
elvégzéséhez. Ezek a makrók két argumentumot hasonlítanak össze egyenlőségre,
illetve különbözőségre. Ha az állítás nem teljesül, a két értéket ki is írják,
így könnyebb belátni, _miért_ bukott el a teszt; ezzel szemben az `assert!`
makró csak azt jelzi, hogy az `==` kifejezés `false` értéket adott, de a
`false` eredményhez vezető értékeket nem írja ki.

A 11-7. kódrészletben írunk egy `add_two` nevű függvényt, amely `2`-t ad a
paraméteréhez, majd ezt a függvényt az `assert_eq!` makróval teszteljük.

<Listing number="11-7" file-name="src/lib.rs" caption="Az `add_two` függvény tesztelése az `assert_eq!` makróval">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-07/src/lib.rs}}
```

</Listing>

Ellenőrizzük, hogy sikeres-e!

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-07/output.txt}}
```

Létrehozunk egy `result` nevű változót, amely az `add_two(2)` hívás
eredményét tárolja. Ezután a `result`-ot és a `4`-et adjuk át argumentumként
az `assert_eq!` makrónak. A teszthez tartozó kimeneti sor `test
tests::it_adds_two ... ok`, és az `ok` szöveg jelzi, hogy a tesztünk sikeres
volt!

Vigyünk hibát a kódunkba, hogy lássuk, hogyan néz ki az `assert_eq!`, amikor
elbukik. Módosítsd az `add_two` függvény implementációját úgy, hogy inkább
`3`-at adjon hozzá:

```rust,not_desired_behavior,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-04-bug-in-add-two/src/lib.rs:here}}
```

Futtasd újra a teszteket:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-04-bug-in-add-two/output.txt}}
```

A tesztünk elkapta a hibát! A `tests::it_adds_two` teszt elbukott, és az
üzenet közli, hogy a nem teljesült állítás a `left == right` volt, valamint
hogy mik a `left` és a `right` értékek. Ez az üzenet segít elindulni a
hibakeresésben: a `left` argumentum, amelyben az `add_two(2)` hívás eredménye
volt, `5` lett, a `right` argumentum viszont `4`. Képzeld el, mennyire hasznos
ez akkor, amikor rengeteg tesztünk fut.

Érdemes megjegyezni, hogy egyes nyelvekben és tesztkeretrendszerekben az
egyenlőséget vizsgáló függvények paramétereit `expected`-nek és `actual`-nek
nevezik, és számít, milyen sorrendben adjuk meg az argumentumokat. A Rustban
azonban `left` és `right` a nevük, és nem számít, milyen sorrendben adjuk meg
az elvárt értéket és a kód által előállított értéket. Ebben a tesztben az
állítást `assert_eq!(4, result)` formában is írhatnánk, ami ugyanazt a
`` assertion `left == right` failed `` hibaüzenetet eredményezné.

Az `assert_ne!` makró akkor sikeres, ha a neki átadott két érték nem egyenlő,
és akkor bukik el, ha egyenlők. Ez a makró akkor a leghasznosabb, ha nem
tudjuk biztosan, mi _lesz_ egy érték, de azt tudjuk, hogy mi biztosan _nem_
lehet. Ha például olyan függvényt tesztelünk, amely garantáltan valamilyen
módon megváltoztatja a bemenetét, de hogy pontosan hogyan, az attól függ, a hét
melyik napján futtatjuk a teszteket, akkor a legjobb, amit ellenőrizhetünk,
talán az, hogy a függvény kimenete nem egyenlő a bemenetével.

A háttérben az `assert_eq!` és az `assert_ne!` makró az `==`, illetve a `!=`
operátort használja. Ha az állítás nem teljesül, ezek a makrók debug
formázással írják ki az argumentumaikat, ami azt jelenti, hogy az
összehasonlított értékeknek megvalósítaniuk kell a `PartialEq` és a `Debug`
traitet. Minden primitív típus és a standard könyvtár legtöbb típusa
megvalósítja ezeket a traiteket. A saját magad által definiált struktúráknál
és enumoknál megvalósítanod kell a `PartialEq`-et, hogy ellenőrizhesd az ilyen
típusú értékek egyenlőségét. A `Debug`-ot is megvalósítanod kell, hogy az
értékek kiírhatók legyenek, ha az állítás nem teljesül. Mivel mindkét trait
származtatható, ahogy az 5. fejezet 5-12. kódrészleténél említettük, ez
általában nem több, mint a `#[derive(PartialEq, Debug)]` annotáció hozzáadása a
struktúra vagy enum definíciójához. Ezekről és a többi származtatható traitről
további részleteket a C. függelékben, a [„Származtatható
traitek”][derivable-traits]<!-- ignore --> részben találsz.

### Egyéni hibaüzenetek hozzáadása {#adding-custom-failure-messages}

Az `assert!`, az `assert_eq!` és az `assert_ne!` makrónak opcionális
argumentumként egyéni üzenetet is átadhatsz, amely a hibaüzenettel együtt
jelenik meg. A kötelező argumentumok után megadott argumentumokat a makrók
továbbadják a `format!` makrónak (erről a 8. fejezet [„Összefűzés a `+`
operátorral vagy a `format!` makróval”][concatenating]<!-- ignore --> című
részében volt szó), így megadhatsz egy `{}` helyőrzőket tartalmazó
formázósztringet, valamint a helyőrzők helyére kerülő értékeket. Az egyéni
üzenetek jól dokumentálják, mit jelent egy állítás; ha egy teszt elbukik,
jobban fogod látni, mi a gond a kóddal.

Tegyük fel például, hogy van egy függvényünk, amely név szerint üdvözli az
embereket, és tesztelni szeretnénk, hogy a függvénynek átadott név megjelenik a
kimenetben:

<span class="filename">Fájlnév: src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-05-greeter/src/lib.rs}}
```

A program követelményeiben még nem állapodtunk meg, és elég biztosak vagyunk
benne, hogy az üdvözlés elején álló `Hello` szöveg meg fog változni. Úgy
döntöttünk, hogy nem szeretnénk a tesztet frissíteni, amikor a követelmények
változnak, ezért ahelyett, hogy a `greeting` függvény visszatérési értékével
való pontos egyezést vizsgálnánk, csak azt ellenőrizzük, hogy a kimenet
tartalmazza-e a bemeneti paraméter szövegét.

Most vigyünk hibát a kódba: módosítsuk úgy a `greeting` függvényt, hogy
kihagyja a `name`-et, és nézzük meg, hogyan néz ki az alapértelmezett
tesztkudarc:

```rust,not_desired_behavior,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-06-greeter-with-bug/src/lib.rs:here}}
```

A teszt futtatása a következőt eredményezi:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-06-greeter-with-bug/output.txt}}
```

Ez az eredmény csak annyit mond, hogy az állítás nem teljesült, és hogy melyik
sorban van. Hasznosabb lenne, ha a hibaüzenet kiírná a `greeting` függvénytől
kapott értéket. Adjunk hozzá egy egyéni hibaüzenetet, amely egy
formázósztringből áll, a helyőrzőjébe pedig a `greeting` függvénytől
ténylegesen kapott érték kerül:

```rust,ignore
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-07-custom-failure-message/src/lib.rs:here}}
```

Ha most futtatjuk a tesztet, informatívabb hibaüzenetet kapunk:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-07-custom-failure-message/output.txt}}
```

A tesztkimenetben látjuk a ténylegesen kapott értéket, ami segít kideríteni,
mi történt ahelyett, amire számítottunk.

### Pánik ellenőrzése a `should_panic` attribútummal {#checking-for-panics-with-should_panic}

A visszatérési értékek ellenőrzése mellett fontos azt is ellenőrizni, hogy a
kódunk az elvárásaink szerint kezeli-e a hibás helyzeteket. Vegyük például a
`Guess` típust, amelyet a 9. fejezet 9-13. kódrészletében hoztunk létre. A
`Guess`-t használó más kódrészek arra a garanciára építenek, hogy a `Guess`
példányok csak 1 és 100 közötti értékeket tartalmaznak. Írhatunk olyan
tesztet, amely biztosítja, hogy egy ezen a tartományon kívüli értékkel
létrehozott `Guess` példány pánikot okoz.

Ehhez a `should_panic` attribútumot adjuk a tesztfüggvényünkhöz. A teszt akkor
sikeres, ha a függvényen belüli kód pánikol, és akkor bukik el, ha a függvényen
belüli kód nem pánikol.

A 11-8. kódrészlet egy olyan tesztet mutat, amely ellenőrzi, hogy a
`Guess::new` hibás esetei akkor következnek-e be, amikor várjuk.

<Listing number="11-8" file-name="src/lib.rs" caption="Annak tesztelése, hogy egy feltétel `panic!`-et okoz">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-08/src/lib.rs}}
```

</Listing>

A `#[should_panic]` attribútumot a `#[test]` attribútum után és az általa
érintett tesztfüggvény elé írjuk. Nézzük meg az eredményt, amikor a teszt
sikeres:

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-08/output.txt}}
```

Jól néz ki! Most vigyünk hibát a kódunkba: töröljük azt a feltételt, amely
miatt a `new` függvény pánikol, ha az érték 100-nál nagyobb:

```rust,not_desired_behavior,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-08-guess-with-bug/src/lib.rs:here}}
```

Ha lefuttatjuk a 11-8. kódrészlet tesztjét, elbukik:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-08-guess-with-bug/output.txt}}
```

Ebben az esetben nem kapunk túl hasznos üzenetet, de ha megnézzük a
tesztfüggvényt, látjuk, hogy a `#[should_panic]` attribútummal jelöltük meg. A
kapott hiba azt jelenti, hogy a tesztfüggvényben lévő kód nem okozott pánikot.

A `should_panic` tesztek pontatlanok lehetnek. Egy `should_panic` teszt akkor
is sikeres lenne, ha a teszt más okból pánikolna, mint amire számítottunk.
Hogy a `should_panic` tesztek pontosabbak legyenek, a `should_panic`
attribútumhoz megadhatunk egy opcionális `expected` paramétert. A
_tesztkörnyezet (test harness)_ ilyenkor ellenőrzi, hogy a hibaüzenet
tartalmazza-e a megadott szöveget. Vegyük például a `Guess` 11-9.
kódrészletben látható módosított kódját, ahol a `new` függvény attól függően
pánikol különböző üzenetekkel, hogy az érték túl kicsi vagy túl nagy.

<Listing number="11-9" file-name="src/lib.rs" caption="`panic!` tesztelése egy adott részsztringet tartalmazó pániküzenettel">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-09/src/lib.rs:here}}
```

</Listing>

Ez a teszt sikeres lesz, mert a `should_panic` attribútum `expected`
paraméterében megadott érték részsztringje annak az üzenetnek, amellyel a
`Guess::new` függvény pánikol. Megadhattuk volna a teljes várt pániküzenetet
is, ami ebben az esetben `Guess value must be less than or equal to 100, got
200` lenne. Hogy mit adsz meg, az attól függ, a pániküzenet mekkora része
egyedi vagy dinamikus, és mennyire szeretnéd pontossá tenni a tesztet. Ebben
az esetben a pániküzenet egy részsztringje is elég ahhoz, hogy biztosak
legyünk benne: a tesztfüggvényben lévő kód az `else if value > 100` ágat hajtja
végre.

Hogy lássuk, mi történik, ha egy `expected` üzenettel ellátott `should_panic`
teszt elbukik, vigyünk ismét hibát a kódunkba: cseréljük fel az `if value < 1`
és az `else if value > 100` blokk törzsét:

```rust,ignore,not_desired_behavior
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-09-guess-with-panic-msg-bug/src/lib.rs:here}}
```

Ezúttal, amikor lefuttatjuk a `should_panic` tesztet, az elbukik:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-09-guess-with-panic-msg-bug/output.txt}}
```

A hibaüzenet azt jelzi, hogy a teszt valóban pánikolt, ahogy vártuk, de a
pániküzenet nem tartalmazta a várt `less than or equal to 100` sztringet. A
kapott pániküzenet ebben az esetben `Guess value must be greater than or equal
to 1, got 200` volt. Most már elkezdhetjük kideríteni, hol a hiba!

### A `Result<T, E>` használata tesztekben {#using-resultt-e-in-tests}

Eddigi tesztjeink mind pánikolnak, amikor elbuknak. Olyan teszteket is
írhatunk, amelyek `Result<T, E>`-t használnak! Íme a 11-1. kódrészlet tesztje,
átírva úgy, hogy `Result<T, E>`-t használjon, és pánikolás helyett `Err`-t adjon
vissza:

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-10-result-in-tests/src/lib.rs:here}}
```

Az `it_works` függvény visszatérési típusa most `Result<(), String>`. A
függvény törzsében az `assert_eq!` makró meghívása helyett `Ok(())`-t adunk
vissza, ha a teszt sikeres, és egy `String`-et tartalmazó `Err`-t, ha a teszt
elbukik.

Ha a tesztek `Result<T, E>`-t adnak vissza, a tesztek törzsében használhatod a
kérdőjel operátort, ami kényelmes módja lehet az olyan tesztek írásának,
amelyeknek el kell bukniuk, ha bármelyik bennük lévő művelet `Err` változatot
ad vissza.

A `#[should_panic]` annotációt nem használhatod `Result<T, E>`-t használó
teszteken. Ha azt szeretnéd ellenőrizni, hogy egy művelet `Err` változatot ad
vissza, a `Result<T, E>` értéken _ne_ használd a kérdőjel operátort. Helyette
használd az `assert!(value.is_err())` formát.

Most, hogy ismersz néhány módot a tesztek írására, nézzük meg, mi történik,
amikor lefuttatjuk a teszteket, és ismerkedjünk meg a `cargo test` paranccsal
használható különféle beállításokkal.

[concatenating]: ch08-02-strings.html#concatenating-with--or-format
[bench]: https://doc.rust-lang.org/unstable-book/library-features/test.html
[ignoring]: ch11-02-running-tests.html#ignoring-tests-unless-specifically-requested
[subset]: ch11-02-running-tests.html#running-a-subset-of-tests-by-name
[controlling-how-tests-are-run]: ch11-02-running-tests.html#controlling-how-tests-are-run
[derivable-traits]: appendix-03-derivable-traits.html
[doc-comments]: ch14-02-publishing-to-crates-io.html#documentation-comments-as-tests
[paths-for-referring-to-an-item-in-the-module-tree]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html
