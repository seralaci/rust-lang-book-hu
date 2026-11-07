## Környezeti változók használata {#working-with-environment-variables}

A `minigrep` binárist egy újabb funkcióval bővítjük: egy olyan beállítással,
amellyel a felhasználó egy környezeti változón keresztül bekapcsolhatja a
_kis- és nagybetűt nem megkülönböztető keresést (case-insensitive search)_.
Ezt a funkciót parancssori kapcsolóként is megvalósíthatnánk, és
megkövetelhetnénk, hogy a felhasználók minden alkalommal megadják, amikor
érvényesülnie kell, de ha környezeti változóvá tesszük, a felhasználók
egyszer beállíthatják a környezeti változót, és abban a terminál-munkamenetben
minden keresésük kis- és nagybetűt nem megkülönböztető lesz.

<!-- Old headings. Do not remove or links may break. -->
<a id="writing-a-failing-test-for-the-case-insensitive-search-function"></a>

### Elbukó teszt írása a kis- és nagybetűt nem megkülönböztető kereséshez {#writing-a-failing-test-for-case-insensitive-search}

Először egy új `search_case_insensitive` függvényt adunk a `minigrep`
könyvtárhoz, amelyet akkor hívunk meg, ha a környezeti változónak van
értéke. Továbbra is a TDD folyamatát követjük, így az első lépés ismét egy
elbukó teszt megírása. Hozzáadunk egy új tesztet az új
`search_case_insensitive` függvényhez, a régi tesztünket pedig
`one_result`-ról `case_sensitive`-re nevezzük át, hogy egyértelműbb legyen a
két teszt közötti különbség, ahogy a 12-20. kódrészlet mutatja.

<Listing number="12-20" file-name="src/lib.rs" caption="Új, elbukó teszt hozzáadása a hamarosan elkészülő, kis- és nagybetűt nem megkülönböztető függvényhez">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-20/src/lib.rs:here}}
```

</Listing>

Figyeld meg, hogy a régi teszt `contents` értékét is módosítottuk. Hozzáadtunk
egy új sort `"Duct tape."` szöveggel, nagy _D_ betűvel, amely nem illeszkedhet
a `"duct"` keresett kifejezésre, ha a kis- és nagybetűket megkülönböztetve
keresünk. Ha a régi tesztet így módosítjuk, azzal biztosítjuk, hogy véletlenül
se rontsuk el a már megvalósított, kis- és nagybetűket megkülönböztető
keresést. Ennek a tesztnek most sikeresnek kell lennie, és annak is kell
maradnia, miközben a kis- és nagybetűt nem megkülönböztető keresésen
dolgozunk.

A kis- és nagybetűt _nem_ megkülönböztető keresés új tesztje a `"rUsT"`
kifejezést keresi. A hamarosan hozzáadandó `search_case_insensitive`
függvényben a `"rUsT"` keresett kifejezésnek illeszkednie kell a nagy _R_
betűs `"Rust:"` sorra és a `"Trust me."` sorra is, annak ellenére, hogy
mindkettőben eltér a betűk kis- és nagybetűs írása a keresett kifejezésétől.
Ez az elbukó tesztünk, és le sem fog fordulni, mert még nem definiáltuk a
`search_case_insensitive` függvényt. Nyugodtan adj hozzá egy vázlatos
megvalósítást, amely mindig üres vektort ad vissza – hasonlóan ahhoz, ahogy a
12-16. kódrészletben a `search` függvénynél tettük –, hogy lásd, ahogy a teszt
lefordul és elbukik.

### A `search_case_insensitive` függvény megvalósítása {#implementing-the-search_case_insensitive-function}

A 12-21. kódrészletben látható `search_case_insensitive` függvény szinte
ugyanolyan lesz, mint a `search` függvény. Az egyetlen különbség, hogy a
`query`-t és minden `line`-t kisbetűssé alakítjuk, így a bemeneti
argumentumok írásmódjától függetlenül azonos lesz a betűméretük, amikor
ellenőrizzük, hogy a sor tartalmazza-e a keresett kifejezést.

<Listing number="12-21" file-name="src/lib.rs" caption="A `search_case_insensitive` függvény definiálása, amely összehasonlítás előtt kisbetűssé alakítja a keresett kifejezést és a sort">

```rust,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-21/src/lib.rs:here}}
```

</Listing>

Először kisbetűssé alakítjuk a `query` sztringet, és egy azonos nevű új
változóban tároljuk, árnyékolva az eredeti `query`-t. A `to_lowercase`
meghívása a keresett kifejezésen azért szükséges, hogy akár `"rust"`,
`"RUST"`, `"Rust"` vagy `"rUsT"` a felhasználó keresett kifejezése, úgy
kezeljük, mintha `"rust"` volna, és ne számítson a kis- és nagybetűs írásmód.
Bár a `to_lowercase` kezeli az alapvető Unicode-ot, nem lesz száz
százalékosan pontos. Ha valódi alkalmazást írnánk, itt még némi munkát
végeznénk, de ez a szakasz a környezeti változókról szól, nem a Unicode-ról,
ezért itt ennyiben hagyjuk.

Figyeld meg, hogy a `query` most már `String`, nem sztringszelet, mert a
`to_lowercase` meghívása új adatot hoz létre ahelyett, hogy meglévő adatra
hivatkozna. Tegyük fel például, hogy a keresett kifejezés `"rUsT"`: ez a
sztringszelet nem tartalmaz kisbetűs `u`-t vagy `t`-t, amelyet
felhasználhatnánk, ezért le kell foglalnunk egy új, `"rust"` tartalmú
`String`-et. Amikor most a `query`-t argumentumként átadjuk a `contains`
metódusnak, egy és-jelet kell elé tennünk, mert a `contains` szignatúrája
sztringszeletet vár.

Ezután minden `line`-on meghívjuk a `to_lowercase`-t, hogy az összes
karakterét kisbetűssé alakítsuk. Most, hogy a `line`-t és a `query`-t is
kisbetűssé alakítottuk, a keresett kifejezés kis- és nagybetűs írásmódjától
függetlenül megtaláljuk az egyezéseket.

Nézzük meg, sikeresek-e a tesztek ezzel a megvalósítással:

```console
{{#include ../listings/ch12-an-io-project/listing-12-21/output.txt}}
```

Remek! Sikeresek. Most hívjuk meg az új `search_case_insensitive` függvényt a
`run` függvényből. Először hozzáadunk egy konfigurációs beállítást a `Config`
struktúrához, amellyel választhatunk a kis- és nagybetűket megkülönböztető
és a kis- és nagybetűt nem megkülönböztető keresés között. Ennek a mezőnek a
hozzáadása fordítási hibákat okoz, mert még sehol sem inicializáljuk:

<span class="filename">Fájlnév: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-22/src/main.rs:here}}
```

Hozzáadtuk az `ignore_case` mezőt, amely egy logikai értéket tárol. Ezután
arra van szükség, hogy a `run` függvény ellenőrizze az `ignore_case` mező
értékét, és ennek alapján döntse el, hogy a `search` vagy a
`search_case_insensitive` függvényt hívja-e meg, ahogy a 12-22. kódrészlet
mutatja. Ez még mindig nem fordul le.

<Listing number="12-22" file-name="src/main.rs" caption="A `search` vagy a `search_case_insensitive` meghívása a `config.ignore_case` értékétől függően">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-22/src/main.rs:there}}
```

</Listing>

Végül ellenőriznünk kell a környezeti változót. A környezeti változók
kezelésére szolgáló függvények a standard könyvtár `env` moduljában
találhatók, amely már hatókörben van a _src/main.rs_ elején. Az `env` modul
`var` függvényével ellenőrizzük, hogy beállítottak-e bármilyen értéket egy
`IGNORE_CASE` nevű környezeti változónak, ahogy a 12-23. kódrészlet mutatja.

<Listing number="12-23" file-name="src/main.rs" caption="Annak ellenőrzése, hogy van-e bármilyen értéke az `IGNORE_CASE` nevű környezeti változónak">

```rust,ignore,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-23/src/main.rs:here}}
```

</Listing>

Itt létrehozunk egy új változót, az `ignore_case`-t. Az értékének
beállításához meghívjuk az `env::var` függvényt, és átadjuk neki az
`IGNORE_CASE` környezeti változó nevét. Az `env::var` függvény egy
`Result`-ot ad vissza, amely a sikeres `Ok` változat lesz, és a környezeti
változó értékét tartalmazza, ha a környezeti változónak bármilyen értéke be
van állítva. Ha a környezeti változó nincs beállítva, az `Err` változatot
adja vissza.

A `Result` `is_ok` metódusával ellenőrizzük, hogy be van-e állítva a
környezeti változó, ami azt jelenti, hogy a programnak kis- és nagybetűt nem
megkülönböztető keresést kell végeznie. Ha az `IGNORE_CASE` környezeti
változónak nincs értéke, az `is_ok` `false`-t ad vissza, és a program kis- és
nagybetűket megkülönböztető keresést végez. A környezeti változó _értéke_
nem érdekel minket, csak az, hogy be van-e állítva vagy sem, ezért az
`is_ok`-ot ellenőrizzük, ahelyett hogy az `unwrap`, az `expect` vagy a
`Result` bármely más, már látott metódusát használnánk.

Az `ignore_case` változó értékét átadjuk a `Config` példánynak, így a `run`
függvény kiolvashatja ezt az értéket, és eldöntheti, hogy a
`search_case_insensitive` vagy a `search` függvényt hívja-e meg, ahogy a
12-22. kódrészletben megvalósítottuk.

Próbáljuk ki! Először a környezeti változó beállítása nélkül futtatjuk a
programot, a `to` keresett kifejezéssel, amelynek minden olyan sorra
illeszkednie kell, amely csupa kisbetűvel tartalmazza a _to_ szót:

```console
{{#include ../listings/ch12-an-io-project/listing-12-23/output.txt}}
```

Úgy tűnik, ez továbbra is működik! Most futtassuk a programot úgy, hogy az
`IGNORE_CASE` értéke `1`, de ugyanazzal a `to` keresett kifejezéssel:

```console
$ IGNORE_CASE=1 cargo run -- to poem.txt
```

Ha PowerShellt használsz, a környezeti változó beállítását és a program
futtatását külön parancsként kell megadnod:

```console
PS> $Env:IGNORE_CASE=1; cargo run -- to poem.txt
```

Így az `IGNORE_CASE` a shell-munkamenet hátralévő részében is megmarad. A
`Remove-Item` parancsmaggal (cmdlet) törölheted a beállítását:

```console
PS> Remove-Item Env:IGNORE_CASE
```

Olyan sorokat kell kapnunk, amelyek a _to_ szót tartalmazzák, akár
nagybetűkkel is:

<!-- manual-regeneration
cd listings/ch12-an-io-project/listing-12-23
IGNORE_CASE=1 cargo run -- to poem.txt
can't extract because of the environment variable
-->

```console
Are you nobody, too?
How dreary to be somebody!
To tell your name the livelong day
To an admiring bog!
```

Kiváló, a _To_ szót tartalmazó sorokat is megkaptuk! A `minigrep`
programunk most már egy környezeti változóval vezérelt, kis- és nagybetűt nem
megkülönböztető keresésre is képes. Most már tudod, hogyan kezelheted a
parancssori argumentumokkal vagy környezeti változókkal megadott
beállításokat.

Egyes programok ugyanahhoz a konfigurációhoz argumentumokat _és_ környezeti
változókat is elfogadnak. Ilyenkor a program eldönti, hogy melyiknek van
elsőbbsége. Önálló gyakorlásként próbáld meg a kis- és nagybetűk
megkülönböztetését parancssori argumentummal vagy környezeti változóval is
vezérelni. Döntsd el, hogy a parancssori argumentumnak vagy a környezeti
változónak legyen-e elsőbbsége, ha a programot úgy futtatják, hogy az egyik
a kis- és nagybetűk megkülönböztetésére, a másik pedig azok figyelmen kívül
hagyására van beállítva.

Az `std::env` modul még sok más hasznos lehetőséget kínál a környezeti
változók kezelésére: nézd meg a dokumentációját, hogy lásd, mi minden érhető
el.
