## Fájl beolvasása {#reading-a-file}

Most hozzáadjuk azt a funkciót, amely beolvassa a `file_path` argumentumban
megadott fájlt. Először is szükségünk van egy mintafájlra, amellyel
kipróbálhatjuk: egy rövid, több soros szöveget tartalmazó fájlt használunk,
amelyben néhány szó ismétlődik. A 12-3. kódrészletben Emily Dickinson egyik
verse szerepel, amely kiválóan megfelel erre! Hozz létre egy _poem.txt_ nevű
fájlt a projekted gyökerében, és írd bele az „I’m Nobody! Who are you?” című
verset.

<Listing number="12-3" file-name="poem.txt" caption="Emily Dickinson egyik verse jó tesztesetnek bizonyul.">

```text
{{#include ../listings/ch12-an-io-project/listing-12-03/poem.txt}}
```

</Listing>

Miután a szöveg a helyén van, szerkeszd a _src/main.rs_ fájlt, és add hozzá a
fájlt beolvasó kódot a 12-4. kódrészletben látható módon.

<Listing number="12-4" file-name="src/main.rs" caption="A második argumentumban megadott fájl tartalmának beolvasása">

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-04/src/main.rs:here}}
```

</Listing>

Először egy `use` utasítással hatókörbe hozzuk a standard könyvtár egy
szükséges részét: a fájlok kezeléséhez az `std::fs`-re van szükségünk.

A `main`-ben az új `fs::read_to_string` utasítás megkapja a `file_path`-t,
megnyitja a fájlt, és egy `std::io::Result<String>` típusú értéket ad vissza,
amely a fájl tartalmát tartalmazza.

Ezután ismét egy ideiglenes `println!` utasítást adunk hozzá, amely a fájl
beolvasása után kiírja a `contents` értékét, így ellenőrizhetjük, hogy a
program eddig rendben működik.

Futtassuk a kódot úgy, hogy első parancssori argumentumként tetszőleges
sztringet adunk meg (mert a keresést még nem valósítottuk meg), másodikként
pedig a _poem.txt_ fájlt:

```console
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-04/output.txt}}
```

Remek! A kód beolvasta, majd kiírta a fájl tartalmát. A kódnak azonban van
néhány hiányossága. Jelenleg a `main` függvénynek több felelőssége is van:
általában a függvények áttekinthetőbbek és könnyebben karbantarthatók, ha
mindegyik csak egyetlen dologért felel. A másik probléma, hogy a hibákat nem
kezeljük olyan jól, ahogy lehetne. A program még kicsi, így ezek a
hiányosságok nem jelentenek nagy gondot, de ahogy a program nő, egyre
nehezebb lesz őket tisztán kijavítani. Jó gyakorlat már a program
fejlesztésének korai szakaszában elkezdeni a refaktorálást, mert kisebb
mennyiségű kódot sokkal könnyebb refaktorálni. A következőkben ezt tesszük.
