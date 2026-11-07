<!-- Old headings. Do not remove or links may break. -->

<a id="installing-binaries-from-cratesio-with-cargo-install"></a>

## Bináris programok telepítése a `cargo install` paranccsal {#installing-binaries-with-cargo-install}

A `cargo install` paranccsal bináris crate-eket telepíthetsz és használhatsz
helyben. Ez nem a rendszercsomagok kiváltására szolgál; inkább kényelmes
módja annak, hogy a Rust-fejlesztők telepíthessék azokat az eszközöket,
amelyeket mások a [crates.io](https://crates.io/)<!-- ignore --> oldalon
megosztottak. Fontos, hogy csak olyan csomagokat telepíthetsz, amelyeknek van
bináris célja. A _bináris cél (binary target)_ az a futtatható program,
amely akkor jön létre, ha a crate-nek van _src/main.rs_ fájlja vagy más,
binárisként megadott fájlja – szemben a könyvtár céllal (library target),
amely önmagában nem futtatható, de alkalmas arra, hogy más programokba
beépítsük. A crate-ek README-fájljában általában szerepel, hogy a crate
könyvtár-e, van-e bináris célja, vagy mindkettő.

A `cargo install` paranccsal telepített összes bináris a telepítési gyökér
_bin_ mappájába kerül. Ha a Rustot a _rustup.rs_ segítségével telepítetted, és
nincs egyéni konfigurációd, ez a mappa a *$HOME/.cargo/bin* lesz. Győződj meg
róla, hogy ez a mappa szerepel a `$PATH` változódban, hogy futtatni tudd a
`cargo install` paranccsal telepített programokat.

A 12. fejezetben például említettük, hogy a fájlokban való kereséshez létezik
a `grep` eszköznek egy `ripgrep` nevű Rust-megvalósítása. A `ripgrep`
telepítéséhez a következőt futtathatjuk:

<!-- manual-regeneration
cargo install something you don't have, copy relevant output below
-->

```console
$ cargo install ripgrep
    Updating crates.io index
  Downloaded ripgrep v14.1.1
  Downloaded 1 crate (213.6 KB) in 0.40s
  Installing ripgrep v14.1.1
--snip--
   Compiling grep v0.3.2
    Finished `release` profile [optimized + debuginfo] target(s) in 6.73s
  Installing ~/.cargo/bin/rg
   Installed package `ripgrep v14.1.1` (executable `rg`)
```

A kimenet utolsó előtti sora a telepített bináris helyét és nevét mutatja,
amely a `ripgrep` esetében `rg`. Ha a telepítési mappa szerepel a `$PATH`
változódban, ahogy korábban említettük, akkor futtathatod az `rg --help`
parancsot, és elkezdheted használni ezt a gyorsabb, rustosabb eszközt a
fájlokban való kereséshez!
