<!-- Old headings. Do not remove or links may break. -->

<a id="writing-error-messages-to-standard-error-instead-of-standard-output"></a>

## Hibák átirányítása a standard hibakimenetre {#redirecting-errors-to-standard-error}

Jelenleg minden kimenetünket a `println!` makróval írjuk a terminálra. A
legtöbb terminálban kétféle kimenet létezik: a _standard kimenet (standard
output, `stdout`)_ az általános információknak, a _standard hibakimenet
(standard error, `stderr`)_ pedig a hibaüzeneteknek. Ez a megkülönböztetés
lehetővé teszi, hogy a felhasználók egy program sikeres kimenetét fájlba
irányítsák, a hibaüzenetek pedig mégis megjelenjenek a képernyőn.

A `println!` makró csak a standard kimenetre tud írni, ezért valami mást kell
használnunk ahhoz, hogy a standard hibakimenetre írjunk.

### Annak ellenőrzése, hová kerülnek a hibák {#checking-where-errors-are-written}

Először figyeljük meg, hogy a `minigrep` által kiírt tartalom jelenleg a
standard kimenetre kerül, beleértve azokat a hibaüzeneteket is, amelyeket
inkább a standard hibakimenetre szeretnénk írni. Ezt úgy tesszük meg, hogy a
standard kimeneti adatfolyamot egy fájlba irányítjuk, miközben szándékosan
hibát idézünk elő. A standard hibakimenet adatfolyamát nem irányítjuk át, így
minden, a standard hibakimenetre küldött tartalom továbbra is megjelenik a
képernyőn.

A parancssori programoktól elvárás, hogy a hibaüzeneteket a standard
hibakimenet adatfolyamára küldjék, így akkor is látjuk a hibaüzeneteket a
képernyőn, ha a standard kimeneti adatfolyamot fájlba irányítjuk. A
programunk jelenleg nem viselkedik helyesen: mindjárt látni fogjuk, hogy a
hibaüzenetet ehelyett fájlba menti!

Ennek bemutatására a programot a `>` jellel és annak a fájlnak az elérési
útjával, az _output.txt_-vel futtatjuk, amelybe a standard kimeneti
adatfolyamot át szeretnénk irányítani. Nem adunk meg argumentumokat, aminek
hibát kell okoznia:

```console
$ cargo run > output.txt
```

A `>` szintaxis azt mondja a shellnek, hogy a standard kimenet tartalmát a
képernyő helyett az _output.txt_ fájlba írja. Nem láttuk a képernyőn a várt
hibaüzenetet, tehát az a fájlba került. Az _output.txt_ tartalma a
következő:

```text
Problem parsing arguments: not enough arguments
```

Igen, a hibaüzenetünk a standard kimenetre kerül. Az ilyen hibaüzenetek
sokkal hasznosabbak, ha a standard hibakimenetre íródnak, így csak a sikeres
futás adatai kerülnek a fájlba. Ezen változtatunk.

### Hibák kiírása a standard hibakimenetre {#printing-errors-to-standard-error}

A 12-24. kódrészletben látható kóddal megváltoztatjuk a hibaüzenetek
kiírásának módját. A fejezet korábbi részében végzett refaktorálásnak
köszönhetően minden kód, amely hibaüzenetet ír ki, egyetlen függvényben, a
`main`-ben található. A standard könyvtár biztosítja az `eprintln!` makrót,
amely a standard hibakimenet adatfolyamára ír, ezért cseréljük le azt a két
helyet, ahol a `println!` makrót hívtuk a hibák kiírására, az `eprintln!`
makróra.

<Listing number="12-24" file-name="src/main.rs" caption="Hibaüzenetek írása a standard kimenet helyett a standard hibakimenetre az `eprintln!` segítségével">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-24/src/main.rs:here}}
```

</Listing>

Futtassuk most újra a programot ugyanúgy, argumentumok nélkül, a standard
kimenetet a `>` jellel átirányítva:

```console
$ cargo run > output.txt
Problem parsing arguments: not enough arguments
```

Most látjuk a hibát a képernyőn, az _output.txt_ pedig üres, ahogy azt a
parancssori programoktól elvárjuk.

Futtassuk újra a programot olyan argumentumokkal, amelyek nem okoznak hibát,
de a standard kimenetet továbbra is fájlba irányítjuk, így:

```console
$ cargo run -- to poem.txt > output.txt
```

A terminálon nem látunk semmilyen kimenetet, az _output.txt_ pedig az
eredményeinket tartalmazza:

<span class="filename">Fájlnév: output.txt</span>

```text
Are you nobody, too?
How dreary to be somebody!
```

Ez azt mutatja, hogy most már a megfelelő módon használjuk a standard
kimenetet a sikeres kimenethez, a standard hibakimenetet pedig a
hibakimenethez.

## Összefoglalás {#summary}

Ez a fejezet áttekintette az eddig megismert legfontosabb fogalmak egy
részét, és bemutatta, hogyan végezhetünk gyakori I/O-műveleteket Rustban. A
parancssori argumentumok, a fájlok, a környezeti változók és a hibák
kiírására szolgáló `eprintln!` makró használatával most már felkészültél
parancssori alkalmazások írására. Az előző fejezetek fogalmaival együtt a
kódod jól szervezett lesz, hatékonyan tárolja majd az adatokat a megfelelő
adatszerkezetekben, szépen kezeli a hibákat, és alaposan tesztelt lesz.

Következőként a Rust néhány olyan nyelvi elemét ismerjük meg, amelyeket a
funkcionális nyelvek ihlettek: a closure-öket és az iterátorokat.
