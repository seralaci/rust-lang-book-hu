## Cargo-munkaterületek {#cargo-workspaces}

A 12. fejezetben olyan csomagot készítettünk, amely egy bináris crate-et és egy
könyvtár crate-et tartalmazott. Ahogy a projekted fejlődik, előfordulhat, hogy
a könyvtár crate egyre nagyobb lesz, és a csomagodat tovább szeretnéd bontani
több könyvtár crate-re. A Cargo erre a _munkaterületek (workspaces)_ nevű
funkciót kínálja, amely segít kezelni több, egymással összefüggő, párhuzamosan
fejlesztett csomagot.

### Munkaterület létrehozása {#creating-a-workspace}

A _munkaterület_ olyan csomagok halmaza, amelyek közös _Cargo.lock_ fájlt és
kimeneti mappát használnak. Készítsünk egy munkaterületet használó projektet –
egyszerű kódot írunk, hogy a munkaterület szerkezetére összpontosíthassunk.
Egy munkaterületet többféleképpen is fel lehet építeni, ezért csak egy gyakori
módot mutatunk be. A munkaterületünk egy bináris crate-et és két könyvtárat
tartalmaz majd. A bináris crate, amely a fő funkciót biztosítja, a két
könyvtártól függ. Az egyik könyvtár egy `add_one`, a másik egy `add_two`
függvényt biztosít. Ez a három crate ugyanannak a munkaterületnek lesz a része.
Kezdjük azzal, hogy létrehozunk egy új mappát a munkaterület számára:

```console
$ mkdir add
$ cd add
```

Ezután az _add_ mappában létrehozzuk a _Cargo.toml_ fájlt, amely az egész
munkaterületet konfigurálja. Ebben a fájlban nem lesz `[package]` szakasz.
Ehelyett egy `[workspace]` szakasszal kezdődik, amellyel tagokat vehetünk fel a
munkaterületbe. Arra is ügyelünk, hogy a munkaterületünkben a Cargo
függőségfeloldó algoritmusának (resolver) legújabb és legjobb változatát
használjuk, ezért a `resolver` értékét `"3"`-ra állítjuk:

<span class="filename">Fájlnév: Cargo.toml</span>

```toml
{{#include ../listings/ch14-more-about-cargo/no-listing-01-workspace/add/Cargo.toml}}
```

Ezután létrehozzuk az `adder` bináris crate-et a `cargo new` parancs
futtatásával az _add_ mappán belül:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/output-only-01-adder-crate/add
remove `members = ["adder"]` from Cargo.toml
rm -rf adder
cargo new adder
copy output below
-->

```console
$ cargo new adder
     Created binary (application) `adder` package
      Adding `adder` as member of workspace at `file:///projects/add`
```

Ha egy munkaterületen belül futtatod a `cargo new` parancsot, az az újonnan
létrehozott csomagot automatikusan fel is veszi a munkaterület _Cargo.toml_
fájljában a `[workspace]` definíció `members` kulcsához, így:

```toml
{{#include ../listings/ch14-more-about-cargo/output-only-01-adder-crate/add/Cargo.toml}}
```

Ezen a ponton a `cargo build` futtatásával lebuildelhetjük a munkaterületet.
Az _add_ mappádban lévő fájloknak így kell kinézniük:

```text
├── Cargo.lock
├── Cargo.toml
├── adder
│   ├── Cargo.toml
│   └── src
│       └── main.rs
└── target
```

A munkaterületnek egyetlen _target_ mappája van a legfelső szinten, ebbe
kerülnek a lefordított buildtermékek; az `adder` csomagnak nincs saját
_target_ mappája. Még ha az _adder_ mappán belülről futtatnánk is a
`cargo build` parancsot, a lefordított buildtermékek akkor is az _add/target_
mappába kerülnének, nem az _add/adder/target_ mappába. A Cargo azért építi fel
így a _target_ mappát egy munkaterületen, mert a munkaterület crate-jei arra
szolgálnak, hogy egymástól függjenek. Ha minden crate-nek saját _target_
mappája lenne, minden crate-nek újra kellene fordítania a munkaterület összes
többi crate-jét, hogy a buildtermékeket a saját _target_ mappájába tegye. Egy
közös _target_ mappa használatával a crate-ek elkerülhetik a szükségtelen
újrabuildelést.

### A második csomag létrehozása a munkaterületen {#creating-the-second-package-in-the-workspace}

Most hozzunk létre egy másik tagcsomagot a munkaterületen, és nevezzük el
`add_one`-nak. Generálj egy új, `add_one` nevű könyvtár crate-et:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/output-only-02-add-one/add
remove `"add_one"` from `members` list in Cargo.toml
rm -rf add_one
cargo new add_one --lib
copy output below
-->

```console
$ cargo new add_one --lib
     Created library `add_one` package
      Adding `add_one` as member of workspace at `file:///projects/add`
```

A legfelső szintű _Cargo.toml_ `members` listájában most már szerepel az
_add_one_ útvonal is:

<span class="filename">Fájlnév: Cargo.toml</span>

```toml
{{#include ../listings/ch14-more-about-cargo/no-listing-02-workspace-with-two-crates/add/Cargo.toml}}
```

Az _add_ mappádban most a következő mappáknak és fájloknak kell lenniük:

```text
├── Cargo.lock
├── Cargo.toml
├── add_one
│   ├── Cargo.toml
│   └── src
│       └── lib.rs
├── adder
│   ├── Cargo.toml
│   └── src
│       └── main.rs
└── target
```

Az _add_one/src/lib.rs_ fájlba írjunk egy `add_one` függvényt:

<span class="filename">Fájlnév: add_one/src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch14-more-about-cargo/no-listing-02-workspace-with-two-crates/add/add_one/src/lib.rs}}
```

Most már elérhetjük, hogy a bináris crate-ünket tartalmazó `adder` csomag a
könyvtárunkat tartalmazó `add_one` csomagtól függjön. Először fel kell
vennünk az `add_one`-ra mutató útvonalfüggőséget (path dependency) az
_adder/Cargo.toml_ fájlba.

<span class="filename">Fájlnév: adder/Cargo.toml</span>

```toml
{{#include ../listings/ch14-more-about-cargo/no-listing-02-workspace-with-two-crates/add/adder/Cargo.toml:6:7}}
```

A Cargo nem feltételezi, hogy a munkaterület crate-jei egymástól függenek,
ezért a függőségi viszonyokat kifejezetten meg kell adnunk.

Ezután használjuk az (`add_one` crate-ben lévő) `add_one` függvényt az `adder`
crate-ben. Nyisd meg az _adder/src/main.rs_ fájlt, és módosítsd a `main`
függvényt úgy, hogy meghívja az `add_one` függvényt, ahogy a 14-7.
kódrészletben látható.

<Listing number="14-7" file-name="adder/src/main.rs" caption="Az `add_one` könyvtár crate használata az `adder` crate-ből">

```rust,ignore
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-07/add/adder/src/main.rs}}
```

</Listing>

Buildeljük le a munkaterületet a `cargo build` futtatásával a legfelső szintű
_add_ mappában!

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/listing-14-07/add
cargo build
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo build
   Compiling add_one v0.1.0 (file:///projects/add/add_one)
   Compiling adder v0.1.0 (file:///projects/add/adder)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.22s
```

Ha a bináris crate-et az _add_ mappából szeretnénk futtatni, a `cargo run`
parancsnál a `-p` argumentummal és a csomag nevével adhatjuk meg, hogy a
munkaterület melyik csomagját szeretnénk futtatni:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/listing-14-07/add
cargo run -p adder
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo run -p adder
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.00s
     Running `target/debug/adder`
Hello, world! 10 plus one is 11!
```

Ez az _adder/src/main.rs_ kódját futtatja, amely az `add_one` crate-től függ.

<!-- Old headings. Do not remove or links may break. -->

<a id="depending-on-an-external-package-in-a-workspace"></a>

### Külső csomagtól való függés {#depending-on-an-external-package}

Figyeld meg, hogy a munkaterületnek csak egyetlen _Cargo.lock_ fájlja van a
legfelső szinten, ahelyett hogy minden crate mappájában lenne egy-egy
_Cargo.lock_. Ez biztosítja, hogy minden crate minden függőségnek ugyanazt a
verzióját használja. Ha a `rand` csomagot felvesszük az _adder/Cargo.toml_ és
az _add_one/Cargo.toml_ fájlba, a Cargo mindkettőt a `rand` egyetlen
verziójára oldja fel, és ezt az egyetlen _Cargo.lock_ fájlban rögzíti. Ha a
munkaterület minden crate-je ugyanazokat a függőségeket használja, a crate-ek
mindig kompatibilisek lesznek egymással. Vegyük fel a `rand` crate-et az
_add_one/Cargo.toml_ fájl `[dependencies]` szakaszába, hogy az `add_one`
crate-ben használhassuk a `rand` crate-et:

<!-- When updating the version of `rand` used, also update the version of
`rand` used in these files so they all match:

* ch01-01-installation.md
* ch02-00-guessing-game-tutorial.md
* ch07-04-bringing-paths-into-scope-with-the-use-keyword.md
-->

<span class="filename">Fájlnév: add_one/Cargo.toml</span>

```toml
{{#include ../listings/ch14-more-about-cargo/no-listing-03-workspace-with-external-dependency/add/add_one/Cargo.toml:6:7}}
```

Most már hozzáadhatjuk a `use rand;` sort az _add_one/src/lib.rs_ fájlhoz, és
ha az _add_ mappában a `cargo build` futtatásával lebuildeljük az egész
munkaterületet, a Cargo letölti és lefordítja a `rand` crate-et. Egy
figyelmeztetést kapunk, mert nem hivatkozunk a hatókörbe hozott `rand`-ra:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/no-listing-03-workspace-with-external-dependency/add
cargo build
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo build
    Updating crates.io index
  Downloaded rand v0.10.1
   --snip--
   Compiling rand v0.10.1
   Compiling add_one v0.1.0 (file:///projects/add/add_one)
warning: unused import: `rand`
 --> add_one/src/lib.rs:1:5
  |
1 | use rand;
  |     ^^^^
  |
  = note: `#[warn(unused_imports)]` (part of `#[warn(unused)]`) on by default

warning: `add_one` (lib) generated 1 warning (run `cargo fix --lib -p add_one` to apply 1 suggestion)
   Compiling adder v0.1.0 (file:///projects/add/adder)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.95s
```

A legfelső szintű _Cargo.lock_ most már tartalmazza azt az információt, hogy
az `add_one` a `rand`-tól függ. Ám bár a `rand`-ot a munkaterület valamely
pontján használjuk, a munkaterület más crate-jeiben csak akkor használhatjuk,
ha az ő _Cargo.toml_ fájljaikba is felvesszük a `rand`-ot. Ha például az
`adder` csomag _adder/src/main.rs_ fájljához hozzáadjuk a `use rand;` sort,
hibát kapunk:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/output-only-03-use-rand/add
cargo build
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo build
  --snip--
   Compiling adder v0.1.0 (file:///projects/add/adder)
error[E0432]: unresolved import `rand`
 --> adder/src/main.rs:2:5
  |
2 | use rand;
  |     ^^^^ no external crate `rand`
```

Ennek javításához szerkeszd az `adder` csomag _Cargo.toml_ fájlját, és jelezd
benne, hogy a `rand` ennek is függősége. Az `adder` csomag buildelése
felveszi a `rand`-ot az `adder` függőségeinek listájára a _Cargo.lock_
fájlban, de a `rand` további példányai nem töltődnek le. A Cargo biztosítja,
hogy a munkaterület minden csomagjának minden olyan crate-je, amely a `rand`
csomagot használja, ugyanazt a verziót használja, feltéve, hogy a `rand`
kompatibilis verzióit adják meg; így helyet takarítunk meg, és biztosítjuk,
hogy a munkaterület crate-jei kompatibilisek legyenek egymással.

Ha a munkaterület crate-jei ugyanannak a függőségnek egymással nem
kompatibilis verzióit adják meg, a Cargo mindegyiket feloldja, de továbbra is
igyekszik a lehető legkevesebb verzióra feloldani őket.

### Teszt hozzáadása a munkaterülethez {#adding-a-test-to-a-workspace}

Egy újabb fejlesztésként adjunk hozzá egy tesztet az `add_one::add_one`
függvényhez az `add_one` crate-en belül:

<span class="filename">Fájlnév: add_one/src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch14-more-about-cargo/no-listing-04-workspace-with-tests/add/add_one/src/lib.rs}}
```

Most futtasd a `cargo test` parancsot a legfelső szintű _add_ mappában. Ha egy
ilyen felépítésű munkaterületen futtatod a `cargo test` parancsot, az a
munkaterület összes crate-jének tesztjeit lefuttatja:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/no-listing-04-workspace-with-tests/add
cargo test
copy output below; the output updating script doesn't handle subdirectories in
paths properly
-->

```console
$ cargo test
   Compiling add_one v0.1.0 (file:///projects/add/add_one)
   Compiling adder v0.1.0 (file:///projects/add/adder)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.20s
     Running unittests src/lib.rs (target/debug/deps/add_one-93c49ee75dc46543)

running 1 test
test tests::it_works ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

     Running unittests src/main.rs (target/debug/deps/adder-3a47283c568d2b6a)

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests add_one

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

A kimenet első része azt mutatja, hogy az `add_one` crate `it_works` tesztje
sikeres volt. A következő rész azt mutatja, hogy az `adder` crate-ben nulla
tesztet talált, az utolsó rész pedig azt, hogy az `add_one` crate-ben nulla
dokumentációs tesztet talált.

A legfelső szintű mappából a munkaterület egy adott crate-jének tesztjeit is
futtathatjuk, ha a `-p` kapcsolóval megadjuk a tesztelni kívánt crate nevét:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/no-listing-04-workspace-with-tests/add
cargo test -p add_one
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo test -p add_one
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.00s
     Running unittests src/lib.rs (target/debug/deps/add_one-93c49ee75dc46543)

running 1 test
test tests::it_works ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests add_one

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

Ez a kimenet azt mutatja, hogy a `cargo test` csak az `add_one` crate
tesztjeit futtatta, az `adder` crate tesztjeit nem.

Ha a munkaterület crate-jeit közzéteszed a
[crates.io](https://crates.io/)<!-- ignore --> oldalon, a munkaterület minden
crate-jét külön kell közzétenni. A `cargo test`-hez hasonlóan a
munkaterületünk egy adott crate-jét úgy tehetjük közzé, hogy a `-p`
kapcsolóval megadjuk a közzétenni kívánt crate nevét.

Gyakorlásképpen adj hozzá ehhez a munkaterülethez egy `add_two` crate-et az
`add_one` crate-hez hasonló módon!

Ahogy a projekted növekszik, fontold meg egy munkaterület használatát: így
egyetlen nagy kódtömb helyett kisebb, könnyebben érthető komponensekkel
dolgozhatsz. Ráadásul ha a crate-eket egy munkaterületen tartod, könnyebb
összehangolni őket, ha gyakran egyszerre változnak.
