## UTF-8 kódolású szöveg tárolása sztringekkel {#storing-utf-8-encoded-text-with-strings}

A sztringekről már a 4. fejezetben beszéltünk, most azonban alaposabban is
megvizsgáljuk őket. A kezdő rustaceanek három ok együttes hatása miatt szoktak
elakadni a sztringeknél: a Rust hajlamos a lehetséges hibákat a felszínre
hozni, a sztringek bonyolultabb adatszerkezetek, mint ahogy azt sok programozó
gondolja, és ott van még az UTF-8 is. Ezek a tényezők együtt nehéznek tűnhetnek,
ha más programozási nyelvekből érkezel.

A sztringeket a gyűjtemények kontextusában tárgyaljuk, mert a sztringek
bájtok (bytes) gyűjteményeként vannak megvalósítva, kiegészítve néhány
metódussal, amelyek hasznos funkciókat nyújtanak, amikor ezeket a bájtokat
szövegként értelmezzük. Ebben a szakaszban a `String` azon műveleteiről
beszélünk, amelyekkel minden gyűjteménytípus rendelkezik, például a
létrehozásról, a frissítésről és az olvasásról. Azt is megvizsgáljuk, miben
különbözik a `String` a többi gyűjteménytől, nevezetesen azt, hogy a `String`
indexelését hogyan bonyolítják az emberek és a számítógépek `String`-adatokat
értelmező módja közötti különbségek.

<!-- Old headings. Do not remove or links may break. -->

<a id="what-is-a-string"></a>

### A sztring fogalma {#defining-strings}

Először meghatározzuk, mit értünk a _sztring (string)_ kifejezés alatt. A
Rust magjában csak egyetlen sztringtípus van, a `str` sztringszelet, amely
általában kölcsönzött formájában, `&str`-ként fordul elő. A 4. fejezetben a
sztringszeletekről beszéltünk, amelyek valahol máshol tárolt, UTF-8 kódolású
sztringadatokra mutató referenciák. A sztringliterálok például a program
binárisában tárolódnak, ezért sztringszeletek.

A `String` típus, amelyet nem a nyelv magja, hanem a Rust standard könyvtára
biztosít, egy bővíthető, módosítható, saját tulajdonú (owned), UTF-8 kódolású
sztringtípus. Amikor a rustaceanek „sztringekről” beszélnek a Rustban, akkor a
`String` és a `&str` sztringszelet típus bármelyikére gondolhatnak, nem csak az
egyikre. Bár ez a szakasz nagyrészt a `String`-ről szól, mindkét típust sokat
használja a Rust standard könyvtára, és a `String` és a sztringszeletek is
UTF-8 kódolásúak.

### Új sztring létrehozása {#creating-a-new-string}

A `Vec<T>`-vel elérhető műveletek közül sok a `String`-gel is elérhető, mert a
`String` valójában egy bájtvektor köré épített burkolóként (wrapper) van
megvalósítva, néhány további garanciával, korlátozással és képességgel. Egy
olyan függvényre, amely a `Vec<T>` és a `String` esetében is ugyanúgy működik,
példa a példányt létrehozó `new` függvény, amelyet a 8-11. kódrészlet mutat.

<Listing number="8-11" caption="Új, üres `String` létrehozása">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-11/src/main.rs:here}}
```

</Listing>

Ez a sor egy új, üres, `s` nevű sztringet hoz létre, amelybe aztán adatokat
tölthetünk. Gyakran van valamilyen kezdeti adatunk, amellyel a sztringet
kezdeni szeretnénk. Ehhez a `to_string` metódust használjuk, amely minden olyan
típuson elérhető, amely megvalósítja a `Display` traitet, ahogy a
sztringliterálok is. A 8-12. kódrészlet két példát mutat.

<Listing number="8-12" caption="A `to_string` metódus használata `String` létrehozására egy sztringliterálból">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-12/src/main.rs:here}}
```

</Listing>

Ez a kód egy `initial contents` tartalmú sztringet hoz létre.

A `String::from` függvénnyel is létrehozhatunk `String`-et egy
sztringliterálból. A 8-13. kódrészlet kódja egyenértékű a 8-12. kódrészlet
`to_string`-et használó kódjával.

<Listing number="8-13" caption="A `String::from` függvény használata `String` létrehozására egy sztringliterálból">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-13/src/main.rs:here}}
```

</Listing>

Mivel a sztringeket nagyon sok mindenre használjuk, számos különböző generikus
API-t használhatunk velük, ami sok lehetőséget kínál. Némelyik feleslegesnek
tűnhet, de mindegyiknek megvan a helye! Ebben az esetben a `String::from` és a
`to_string` ugyanazt csinálja, így az, hogy melyiket választod, stílus és
olvashatóság kérdése.

Ne feledd, hogy a sztringek UTF-8 kódolásúak, így bármilyen helyesen kódolt
adatot tartalmazhatnak, ahogy a 8-14. kódrészlet mutatja.

<Listing number="8-14" caption="Különböző nyelvű üdvözlések tárolása sztringekben">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-14/src/main.rs:here}}
```

</Listing>

Ezek mind érvényes `String` értékek.

### Sztring frissítése {#updating-a-string}

Egy `String` mérete nőhet, a tartalma pedig változhat, akárcsak egy `Vec<T>`
tartalma, ha további adatokat teszel bele. Ezenkívül a `String` értékek
összefűzésére (concatenation) kényelmesen használhatod a `+` operátort vagy a
`format!` makrót.

<!-- Old headings. Do not remove or links may break. -->

<a id="appending-to-a-string-with-push_str-and-push"></a>

#### Hozzáfűzés a `push_str` vagy a `push` metódussal {#appending-with-push_str-or-push}

Egy `String`-et úgy bővíthetünk, hogy a `push_str` metódussal egy
sztringszeletet fűzünk hozzá, ahogy a 8-15. kódrészlet mutatja.

<Listing number="8-15" caption="Sztringszelet hozzáfűzése egy `String`-hez a `push_str` metódussal">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-15/src/main.rs:here}}
```

</Listing>

E két sor után `s` a `foobar` értéket tartalmazza. A `push_str` metódus
sztringszeletet vár, mert nem feltétlenül szeretnénk átvenni a paraméter
tulajdonjogát. A 8-16. kódrészlet kódjában például azt szeretnénk, hogy az
`s2`-t azután is használhassuk, hogy a tartalmát az `s1`-hez fűztük.

<Listing number="8-16" caption="Sztringszelet használata azután, hogy a tartalmát egy `String`-hez fűztük">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-16/src/main.rs:here}}
```

</Listing>

Ha a `push_str` metódus átvenné az `s2` tulajdonjogát, az utolsó sorban nem
tudnánk kiíratni az értékét. Ez a kód azonban úgy működik, ahogy várjuk!

A `push` metódus egyetlen karaktert kap paraméterként, és hozzáadja a
`String`-hez. A 8-17. kódrészlet a `push` metódussal az _l_ betűt adja hozzá egy
`String`-hez.

<Listing number="8-17" caption="Egy karakter hozzáadása egy `String` értékhez a `push` metódussal">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-17/src/main.rs:here}}
```

</Listing>

Ennek eredményeként `s` a `lol` értéket tartalmazza.

<!-- Old headings. Do not remove or links may break. -->

<a id="concatenation-with-the--operator-or-the-format-macro"></a>

#### Összefűzés a `+` operátorral vagy a `format!` makróval {#concatenating-with--or-format}

Gyakran két meglévő sztringet szeretnél egyesíteni. Ennek egyik módja a `+`
operátor használata, ahogy a 8-18. kódrészlet mutatja.

<Listing number="8-18" caption="A `+` operátor használata két `String` érték egy új `String` értékké egyesítésére">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-18/src/main.rs:here}}
```

</Listing>

Az `s3` sztring a `Hello, world!` értéket tartalmazza. Az, hogy az `s1` az
összeadás után már nem érvényes, és hogy az `s2`-re referenciát használtunk,
annak a metódusnak a szignatúrájával függ össze, amely a `+` operátor
használatakor meghívódik. A `+` operátor az `add` metódust használja, amelynek
szignatúrája nagyjából így néz ki:

```rust,ignore
fn add(self, s: &str) -> String {
```

A standard könyvtárban az `add` generikus típusokkal és társított típusokkal
van definiálva. Itt konkrét típusokat helyettesítettünk be, ez történik, amikor
ezt a metódust `String` értékekkel hívjuk meg. A generikus típusokat a 10.
fejezetben tárgyaljuk. Ez a szignatúra megadja azokat a támpontokat, amelyekre
szükségünk van ahhoz, hogy megértsük a `+` operátor trükkös részeit.

Először is az `s2` előtt `&` áll, vagyis a második sztring egy referenciáját
adjuk hozzá az első sztringhez. Ez az `add` függvény `s` paramétere miatt van
így: egy `String`-hez csak sztringszeletet adhatunk hozzá; két `String` értéket
nem adhatunk össze. De várjunk csak – az `&s2` típusa `&String`, nem pedig
`&str`, ahogy azt az `add` második paramétere előírja. Akkor miért fordul le a
8-18. kódrészlet?

Azért használhatjuk az `&s2`-t az `add` hívásában, mert a fordító képes a
`&String` argumentumot `&str`-ré alakítani. Amikor meghívjuk az `add`
metódust, a Rust deref-konverziót (deref coercion) alkalmaz, amely itt az
`&s2`-t `&s2[..]`-vé alakítja. A deref-konverziót a 15. fejezetben tárgyaljuk
részletesebben. Mivel az `add` nem veszi át az `s` paraméter tulajdonjogát, az
`s2` a művelet után is érvényes `String` marad.

Másodszor, a szignatúrából látható, hogy az `add` átveszi a `self`
tulajdonjogát, mert a `self` előtt _nincs_ `&`. Ez azt jelenti, hogy a 8-18.
kódrészletben az `s1` bekerül (mozgatással) az `add` hívásába, és utána már nem
lesz érvényes. Így bár a `let s3 = s1 + &s2;` úgy néz ki, mintha mindkét
sztringet lemásolná, és egy újat hozna létre, ez az utasítás valójában átveszi
az `s1` tulajdonjogát, hozzáfűzi az `s2` tartalmának másolatát, majd visszaadja
az eredmény tulajdonjogát. Más szóval úgy tűnik, mintha sok másolatot készítene,
de nem így van; a megvalósítás hatékonyabb a másolásnál.

Ha több sztringet kell összefűznünk, a `+` operátor viselkedése nehezen
kezelhetővé válik:

```rust
{{#rustdoc_include ../listings/ch08-common-collections/no-listing-01-concat-multiple-strings/src/main.rs:here}}
```

Ezen a ponton `s` értéke `tic-tac-toe` lesz. A sok `+` és `"` karakter miatt
nehéz átlátni, mi történik. A sztringek bonyolultabb módon való egyesítésére
inkább a `format!` makrót használhatjuk:

```rust
{{#rustdoc_include ../listings/ch08-common-collections/no-listing-02-format/src/main.rs:here}}
```

Ez a kód is `tic-tac-toe` értékre állítja `s`-t. A `format!` makró úgy
működik, mint a `println!`, de ahelyett, hogy a kimenetet a képernyőre írná,
egy `String`-et ad vissza a tartalommal. A kód `format!`-ot használó változata
sokkal könnyebben olvasható, és a `format!` makró által generált kód
referenciákat használ, így ez a hívás egyik paraméterének tulajdonjogát sem
veszi át.

### Sztringek indexelése {#indexing-into-strings}

Sok más programozási nyelvben a sztring egyes karaktereinek index alapján való
elérése érvényes és gyakori művelet. Ha azonban a Rustban indexelési
szintaxissal próbálod elérni egy `String` részeit, hibát kapsz. Nézd meg a
8-19. kódrészlet érvénytelen kódját.

<Listing number="8-19" caption="Kísérlet az indexelési szintaxis használatára egy `String` esetén">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-19/src/main.rs:here}}
```

</Listing>

Ez a kód a következő hibát eredményezi:

```console
{{#include ../listings/ch08-common-collections/listing-08-19/output.txt}}
```

A hiba mindent elmond: a Rust sztringjei nem támogatják az indexelést. De miért
nem? Ahhoz, hogy erre a kérdésre válaszolni tudjunk, meg kell vizsgálnunk,
hogyan tárolja a Rust a sztringeket a memóriában.

#### Belső ábrázolás {#internal-representation}

A `String` egy `Vec<u8>` köré épített burkoló. Nézzük meg a 8-14. kódrészlet
néhány helyesen kódolt UTF-8 példasztringjét. Először ezt:

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-14/src/main.rs:spanish}}
```

Ebben az esetben a `len` értéke `4` lesz, ami azt jelenti, hogy a `"Hola"`
sztringet tároló vektor 4 bájt hosszú. Ezek a betűk UTF-8 kódolásban egyenként
1 bájtot foglalnak. A következő sor azonban meglephet (figyeld meg, hogy ez a
sztring a nagy cirill _Ze_ betűvel kezdődik, nem a 3-as számmal):

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-14/src/main.rs:russian}}
```

Ha megkérdeznék, milyen hosszú ez a sztring, azt mondhatnád, hogy 12. A Rust
válasza valójában 24: ennyi bájt kell a „Здравствуйте” UTF-8 kódolásához, mert
ebben a sztringben minden Unicode skalárérték (Unicode scalar value) 2 bájt
tárhelyet foglal. Ezért a sztring bájtjaiba mutató index nem mindig felel meg
egy érvényes Unicode skalárértéknek. Szemléltetésként nézd meg ezt az
érvénytelen Rust-kódot:

```rust,ignore,does_not_compile
let hello = "Здравствуйте";
let answer = &hello[0];
```

Már tudod, hogy az `answer` nem az első betű, a `З` lesz. UTF-8 kódolásban a
`З` első bájtja `208`, a második `151`, így úgy tűnhet, hogy az `answer`
értékének valójában `208`-nak kellene lennie, de a `208` önmagában nem
érvényes karakter. A `208` visszaadása valószínűleg nem az, amit egy
felhasználó szeretne, ha a sztring első betűjét kérné; a Rustnak azonban a 0-s
bájtindexen csak ez az adat áll rendelkezésére. A felhasználók általában akkor
sem a bájtértéket szeretnék visszakapni, ha a sztring csak latin betűket
tartalmaz: ha a `&"hi"[0]` érvényes kód lenne, amely a bájtértéket adja
vissza, akkor `104`-et adna vissza, nem `h`-t.

A válasz tehát az, hogy a Rust – annak elkerülésére, hogy váratlan értéket
adjon vissza, és olyan hibákat okozzon, amelyek nem feltétlenül derülnek ki
azonnal – egyáltalán nem fordítja le ezt a kódot, és már a fejlesztési
folyamat elején megelőzi a félreértéseket.

<!-- Old headings. Do not remove or links may break. -->

<a id="bytes-and-scalar-values-and-grapheme-clusters-oh-my"></a>

#### Bájtok, skalárértékek és graféma-klaszterek {#bytes-scalar-values-and-grapheme-clusters}

Az UTF-8-cal kapcsolatban egy másik szempont, hogy a Rust nézőpontjából
valójában háromféleképpen tekinthetünk a sztringekre: bájtokként,
skalárértékekként és graféma-klaszterekként (grapheme clusters) – ez utóbbi áll
a legközelebb ahhoz, amit _betűknek_ neveznénk.

Ha a dévanágari írással írt „नमस्ते” hindi szót nézzük, az `u8` értékek egy
olyan vektoraként tárolódik, amely így néz ki:

```text
[224, 164, 168, 224, 164, 174, 224, 164, 184, 224, 165, 141, 224, 164, 164,
224, 165, 135]
```

Ez 18 bájt, és végső soron így tárolják a számítógépek ezt az adatot. Ha
Unicode skalárértékekként nézzük őket – a Rust `char` típusa ilyen –, akkor
ezek a bájtok így néznek ki:

```text
['न', 'म', 'स', '्', 'त', 'े']
```

Itt hat `char` érték van, de a negyedik és a hatodik nem betű: ezek
mellékjelek, amelyeknek önmagukban nincs értelmük. Végül, ha
graféma-klaszterekként nézzük őket, azt a négy betűt kapjuk, amelyekből egy
ember szerint a hindi szó áll:

```text
["न", "म", "स्", "ते"]
```

A Rust különböző módokat kínál a számítógépek által tárolt nyers sztringadatok
értelmezésére, így minden program azt az értelmezést választhatja, amelyre
szüksége van, függetlenül attól, hogy az adat milyen emberi nyelven íródott.

Az utolsó ok, amiért a Rust nem engedi, hogy egy `String` indexelésével
karaktert kapjunk, az, hogy az indexelési műveletektől elvárjuk, hogy mindig
állandó időben (O(1)) fussanak le. Egy `String` esetén azonban ez a
teljesítmény nem garantálható, mert a Rustnak az elejétől az indexig végig
kellene haladnia a tartalmon, hogy megállapítsa, hány érvényes karakter van
benne.

### Sztringek szeletelése {#slicing-strings}

Egy sztring indexelése gyakran rossz ötlet, mert nem egyértelmű, mi legyen a
sztringindexelő művelet visszatérési típusa: egy bájtérték, egy karakter, egy
graféma-klaszter vagy egy sztringszelet. Ha tehát valóban indexekkel kell
sztringszeleteket létrehoznod, a Rust azt kéri, hogy fogalmazz pontosabban.

Ahelyett, hogy a `[]`-t egyetlen számmal indexelnél, a `[]`-t egy
tartománnyal is használhatod, hogy adott bájtokat tartalmazó sztringszeletet
hozz létre:

```rust
let hello = "Здравствуйте";

let s = &hello[0..4];
```

Itt az `s` egy `&str` lesz, amely a sztring első 4 bájtját tartalmazza.
Korábban említettük, hogy ezek a karakterek egyenként 2 bájtosak, ami azt
jelenti, hogy az `s` értéke `Зд` lesz.

Ha egy karakter bájtjainak csak egy részét próbálnánk kiszeletelni, például az
`&hello[0..1]` kifejezéssel, a Rust futásidőben pánikolna, ugyanúgy, mintha egy
vektorban érvénytelen indexet próbálnánk elérni:

```console
{{#include ../listings/ch08-common-collections/output-only-01-not-char-boundary/output.txt}}
```

Óvatosan hozz létre sztringszeleteket tartományokkal, mert ez összeomolhatja a
programodat.

<!-- Old headings. Do not remove or links may break. -->

<a id="methods-for-iterating-over-strings"></a>

### Iterálás sztringeken {#iterating-over-strings}

A sztringrészleteken végzett műveletekhez a legjobb, ha egyértelműen megadod,
hogy karaktereket vagy bájtokat szeretnél. Az egyes Unicode skalárértékekhez a
`chars` metódust használd. Ha a „Зд” sztringen meghívod a `chars` metódust, az
szétválasztja és két `char` típusú értékként adja vissza őket, és az eredményen
végigiterálva minden elemet elérhetsz:

```rust
for c in "Зд".chars() {
    println!("{c}");
}
```

Ez a kód a következőt írja ki:

```text
З
д
```

Másik lehetőségként a `bytes` metódus minden nyers bájtot visszaad, ami az
adott feladatkörben megfelelő lehet:

```rust
for b in "Зд".bytes() {
    println!("{b}");
}
```

Ez a kód a sztringet alkotó 4 bájtot írja ki:

```text
208
151
208
180
```

Mindenképp tartsd azonban észben, hogy az érvényes Unicode skalárértékek 1
bájtnál többől is állhatnak.

A graféma-klaszterek kinyerése a sztringekből – például a dévanágari írás
esetén – bonyolult, ezért ezt a funkciót a standard könyvtár nem biztosítja. Ha
erre a funkcióra van szükséged, a [crates.io](https://crates.io/)<!-- ignore -->
oldalon találsz hozzá crate-eket.

<!-- Old headings. Do not remove or links may break. -->

<a id="strings-are-not-so-simple"></a>

### A sztringek összetettségének kezelése {#handling-the-complexities-of-strings}

Összefoglalva: a sztringek bonyolultak. A különböző programozási nyelvek
különbözőképpen döntenek arról, hogyan tárják ezt a bonyolultságot a programozó
elé. A Rust úgy döntött, hogy a `String`-adatok helyes kezelése legyen minden
Rust-program alapértelmezett viselkedése, ami azt jelenti, hogy a
programozóknak már az elején többet kell gondolkodniuk az UTF-8 adatok
kezelésén. Ez a kompromisszum a sztringek bonyolultságából többet tár fel, mint
ami más programozási nyelvekben látszik, de megkímél attól, hogy a fejlesztési
életciklus későbbi szakaszában nem ASCII karaktereket érintő hibákat kelljen
kezelned.

A jó hír az, hogy a standard könyvtár rengeteg, a `String` és a `&str`
típusra épülő funkciót kínál, amelyek segítenek ezeket a bonyolult helyzeteket
helyesen kezelni. Mindenképp nézd meg a dokumentációban az olyan hasznos
metódusokat, mint a sztringben való keresésre szolgáló `contains`, vagy a
sztring részeinek egy másik sztringre cserélésére szolgáló `replace`.

Térjünk át valami kicsit kevésbé bonyolultra: a hasítótáblákra!
