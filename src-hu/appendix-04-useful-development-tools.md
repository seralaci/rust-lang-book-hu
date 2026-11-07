## D. függelék: Hasznos fejlesztőeszközök {#appendix-d-useful-development-tools}

Ebben a függelékben néhány hasznos fejlesztőeszközről lesz szó, amelyeket a
Rust projekt biztosít. Megnézzük az automatikus formázást, a figyelmeztetések
javításainak gyors alkalmazását, egy lintert (kódelemzőt), valamint az
IDE-kkel való integrációt.

### Automatikus formázás a `rustfmt`-tel {#automatic-formatting-with-rustfmt}

A `rustfmt` eszköz a közösségi kódstílus szerint formázza újra a kódodat. Sok
közös fejlesztésű projekt használja a `rustfmt`-et, hogy elkerülje a vitákat
arról, milyen stílusban írják a Rust-kódot: mindenki ezzel az eszközzel
formázza a kódját.

A Rust telepítése alapértelmezés szerint tartalmazza a `rustfmt`-et, így a
`rustfmt` és a `cargo-fmt` programnak már elérhetőnek kell lennie a
rendszereden. Ez a két parancs a `rustc` és a `cargo` párosához hasonlít:
a `rustfmt` finomabb vezérlést tesz lehetővé, a `cargo-fmt` pedig ismeri a
Cargót használó projektek konvencióit. Bármely Cargo-projekt formázásához add
ki a következő parancsot:

```console
$ cargo fmt
```

Ez a parancs az aktuális crate összes Rust-kódját újraformázza. Ennek csak a
kód stílusát szabad megváltoztatnia, a jelentését nem. A `rustfmt`-ről
bővebben [a dokumentációjában][rustfmt] olvashatsz.

### Javítsd a kódodat a `rustfix`-szel {#fix-your-code-with-rustfix}

A `rustfix` eszköz része a Rust telepítésének, és automatikusan képes
kijavítani azokat a fordítói figyelmeztetéseket, amelyeknél egyértelmű, hogyan
orvosolható a probléma, és valószínűleg épp ezt a javítást szeretnéd. Biztosan
láttál már fordítói figyelmeztetéseket. Vegyük például ezt a kódot:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
fn main() {
    let mut x = 42;
    println!("{x}");
}
```

Itt az `x` változót módosíthatóként definiáljuk, de valójában soha nem
módosítjuk. A Rust figyelmeztet erre:

```console
$ cargo build
   Compiling myprogram v0.1.0 (file:///projects/myprogram)
warning: variable does not need to be mutable
 --> src/main.rs:2:9
  |
2 |     let mut x = 0;
  |         ----^
  |         |
  |         help: remove this `mut`
  |
  = note: `#[warn(unused_mut)]` on by default
```

A figyelmeztetés azt javasolja, hogy távolítsuk el a `mut` kulcsszót. Ezt a
javaslatot automatikusan alkalmazhatjuk a `rustfix` eszközzel, a `cargo fix`
parancs futtatásával:

```console
$ cargo fix
    Checking myprogram v0.1.0 (file:///projects/myprogram)
      Fixing src/main.rs (1 fix)
    Finished dev [unoptimized + debuginfo] target(s) in 0.59s
```

Ha újra megnézzük az _src/main.rs_ fájlt, látni fogjuk, hogy a `cargo fix`
megváltoztatta a kódot:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
fn main() {
    let x = 42;
    println!("{x}");
}
```

Az `x` változó most már nem módosítható, és a figyelmeztetés sem jelenik meg
többé.

A `cargo fix` paranccsal a kódodat a különböző Rust-kiadások (edition) között
is átállíthatod. A kiadásokról az [E. függelékben][editions]<!-- ignore -->
lesz szó.

### További lintek a Clippyvel {#more-lints-with-clippy}

A Clippy eszköz lintek (kódelemző ellenőrzések) gyűjteménye, amelyek
elemzik a kódodat, így elkaphatod a gyakori hibákat, és jobbá teheted a
Rust-kódodat. A Clippy a Rust szabványos telepítésének része.

Bármely Cargo-projekten a Clippy lintjeit a következő paranccsal futtathatod:

```console
$ cargo clippy
```

Tegyük fel például, hogy olyan programot írsz, amely egy matematikai
konstans, például a pi közelítő értékét használja, ahogy ez a program is:

<Listing file-name="src/main.rs">

```rust
fn main() {
    let x = 3.1415;
    let r = 8.0;
    println!("the area of the circle is {}", x * r * r);
}
```

</Listing>

Ha ezen a projekten lefuttatod a `cargo clippy` parancsot, ezt a hibát kapod:

```text
error: approximate value of `f{32, 64}::consts::PI` found
 --> src/main.rs:2:13
  |
2 |     let x = 3.1415;
  |             ^^^^^^
  |
  = note: `#[deny(clippy::approx_constant)]` on by default
  = help: consider using the constant directly
  = help: for further information visit https://rust-lang.github.io/rust-clippy/master/index.html#approx_constant
```

Ez a hiba jelzi, hogy a Rustban már definiálva van egy pontosabb `PI`
konstans, és a programod helyesebb lenne, ha inkább azt használnád. Ezután
átírnád a kódodat úgy, hogy a `PI` konstanst használja.

A következő kód semmilyen hibát vagy figyelmeztetést nem vált ki a Clippyből:

<Listing file-name="src/main.rs">

```rust
fn main() {
    let x = std::f64::consts::PI;
    let r = 8.0;
    println!("the area of the circle is {}", x * r * r);
}
```

</Listing>

A Clippyről bővebben [a dokumentációjában][clippy] olvashatsz.

### IDE-integráció a `rust-analyzer` segítségével {#ide-integration-using-rust-analyzer}

Az IDE-integrációhoz a Rust közösség a
[`rust-analyzer`][rust-analyzer]<!-- ignore --> használatát javasolja. Ez az
eszköz fordítóközpontú segédprogramok gyűjteménye, amelyek a [Language Server
Protocol][lsp]<!-- ignore --> nyelvén beszélnek; ez egy specifikáció,
amelynek segítségével az IDE-k és a programozási nyelvek kommunikálni tudnak
egymással. A `rust-analyzer`-t különböző kliensek használhatják, például [a
Visual Studio Code-hoz készült Rust analyzer bővítmény][vscode].

A telepítési útmutatóért látogass el a `rust-analyzer` projekt
[honlapjára][rust-analyzer]<!-- ignore -->, majd telepítsd a nyelvi szerver
támogatását a saját IDE-dben. Az IDE-d olyan képességekkel bővül majd, mint az
automatikus kiegészítés, az ugrás a definícióhoz és a sorközi hibajelzés.

[rustfmt]: https://github.com/rust-lang/rustfmt
[editions]: appendix-05-editions.md
[clippy]: https://github.com/rust-lang/rust-clippy
[rust-analyzer]: https://rust-analyzer.github.io
[lsp]: http://langserver.org/
[vscode]: https://marketplace.visualstudio.com/items?itemName=rust-lang.rust-analyzer
