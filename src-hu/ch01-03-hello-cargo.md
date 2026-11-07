## Hello, Cargo! {#hello-cargo}

A Cargo a Rust buildrendszere és csomagkezelője. A legtöbb rustacean ezzel az
eszközzel kezeli a Rust-projektjeit, mert a Cargo sok feladatot elvégez
helyetted, például lefordítja a kódodat, letölti azokat a könyvtárakat,
amelyekre a kódod épül, és azokat is lefordítja. (Azokat a könyvtárakat,
amelyekre a kódodnak szüksége van, _függőségeknek (dependencies)_ nevezzük.)

A legegyszerűbb Rust-programoknak, mint amilyet eddig írtunk, nincsenek
függőségeik. Ha a „Hello, world!” projektet a Cargóval készítettük volna, az
a Cargónak csak azt a részét használná, amely a kód lefordításáért felel. Ahogy
egyre összetettebb Rust-programokat írsz, függőségeket is hozzáadsz majd, és
ha a projektet a Cargóval kezded, a függőségek hozzáadása sokkal egyszerűbb
lesz.

Mivel a Rust-projektek túlnyomó többsége a Cargót használja, a könyv további
része azt feltételezi, hogy te is a Cargót használod. A Cargo a Rusttal együtt
települ, ha a [„Telepítés”][installation]<!-- ignore --> szakaszban bemutatott
hivatalos telepítőket használtad. Ha a Rustot más módon telepítetted,
ellenőrizd, hogy a Cargo telepítve van-e, ehhez írd be a következőt a
terminálba:

```console
$ cargo --version
```

Ha egy verziószámot látsz, akkor megvan! Ha hibát látsz, például `command not
found`, nézd meg a telepítési módszered dokumentációjában, hogyan telepítheted
külön a Cargót.

### Projekt létrehozása a Cargóval {#creating-a-project-with-cargo}

Hozzunk létre egy új projektet a Cargóval, és nézzük meg, miben különbözik az
eredeti „Hello, world!” projektünktől. Lépj vissza a _projects_ mappádba (vagy
oda, ahol a kódodat tárolod). Ezután bármelyik operációs rendszeren futtasd a
következőt:

```console
$ cargo new hello_cargo
$ cd hello_cargo
```

Az első parancs létrehoz egy új, _hello_cargo_ nevű mappát és projektet. A
projektünknek a _hello_cargo_ nevet adtuk, és a Cargo egy ugyanilyen nevű
mappában hozza létre a fájljait.

Lépj be a _hello_cargo_ mappába, és listázd ki a fájlokat. Láthatod, hogy a
Cargo két fájlt és egy mappát hozott létre nekünk: egy _Cargo.toml_ fájlt és
egy _src_ mappát, benne egy _main.rs_ fájllal.

Emellett inicializált egy új Git-tárolót is, egy _.gitignore_ fájllal együtt.
Ha a `cargo new` parancsot egy már létező Git-tárolón belül futtatod, a
Git-fájlok nem jönnek létre; ezt a viselkedést a `cargo new --vcs=git`
paranccsal felülbírálhatod.

> Megjegyzés: A Git egy elterjedt verziókezelő rendszer. A `--vcs` kapcsolóval
> beállíthatod, hogy a `cargo new` más verziókezelő rendszert használjon, vagy
> egyáltalán ne használjon verziókezelést. Az elérhető lehetőségeket a
> `cargo new --help` paranccsal tekintheted meg.

Nyisd meg a _Cargo.toml_ fájlt a kedvenc szövegszerkesztődben. Az 1-2.
kódrészletben láthatóhoz hasonlóan kell kinéznie.

<Listing number="1-2" file-name="Cargo.toml" caption="A `cargo new` által létrehozott *Cargo.toml* tartalma">

```toml
[package]
name = "hello_cargo"
version = "0.1.0"
edition = "2024"

[dependencies]
```

</Listing>

Ez a fájl [_TOML_][toml]<!-- ignore --> (_Tom’s Obvious, Minimal Language_)
formátumú; ez a Cargo konfigurációs formátuma.

Az első sor, a `[package]`, egy szakaszfejléc, amely azt jelzi, hogy az utána
következő utasítások egy csomagot konfigurálnak. Ahogy további információkat
adunk ehhez a fájlhoz, újabb szakaszokat is felveszünk majd.

A következő három sor azokat a konfigurációs adatokat adja meg, amelyekre a
Cargónak a program lefordításához szüksége van: a nevet, a verziót és a
használandó Rust-kiadást. Az `edition` kulcsról [az E.
függelékben][appendix-e]<!-- ignore --> lesz szó.

Az utolsó sor, a `[dependencies]`, annak a szakasznak a kezdete, ahol a
projekted függőségeit sorolhatod fel. A Rustban a kódcsomagokat _crate-eknek_
nevezzük. Ehhez a projekthez nem lesz szükségünk más crate-ekre, de a 2.
fejezet első projektjében igen, így ott majd használjuk ezt a függőségi
szakaszt.

Most nyisd meg az _src/main.rs_ fájlt, és nézd meg:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
fn main() {
    println!("Hello, world!");
}
```

A Cargo egy „Hello, world!” programot hozott létre neked, pontosan olyat, mint
amilyet az 1-1. kódrészletben írtunk! Eddig a mi projektünk és a Cargo által
létrehozott projekt között annyi a különbség, hogy a Cargo a kódot az _src_
mappába tette, és a legfelső mappában van egy _Cargo.toml_ konfigurációs
fájlunk.

A Cargo azt várja, hogy a forrásfájljaid az _src_ mappában legyenek. A
legfelső szintű projektmappa csak a README-fájloknak, a licencinformációknak,
a konfigurációs fájloknak és minden egyébnek való, ami nem a kódodhoz
kapcsolódik. A Cargo használata segít rendben tartani a projektjeidet. Mindennek
megvan a helye, és minden a helyén van.

Ha olyan projektet kezdtél, amely nem használja a Cargót – ahogy mi tettük a
„Hello, world!” projekttel –, átalakíthatod Cargót használó projektté. Helyezd
át a projekt kódját az _src_ mappába, és hozz létre egy megfelelő _Cargo.toml_
fájlt. A _Cargo.toml_ fájlhoz a legkönnyebben a `cargo init` parancs
futtatásával juthatsz, amely automatikusan létrehozza neked.

### Cargo-projekt buildelése és futtatása {#building-and-running-a-cargo-project}

Most nézzük meg, mi változik, ha a „Hello, world!” programot a Cargóval
buildeljük és futtatjuk! A _hello_cargo_ mappában a következő paranccsal
buildelheted a projektedet:

```console
$ cargo build
   Compiling hello_cargo v0.1.0 (file:///projects/hello_cargo)
    Finished dev [unoptimized + debuginfo] target(s) in 2.85 secs
```

Ez a parancs a futtatható állományt nem az aktuális mappában, hanem a
_target/debug/hello_cargo_ (Windowson a _target\debug\hello_cargo.exe_)
helyen hozza létre. Mivel az alapértelmezett build debug build, a Cargo a
binárist egy _debug_ nevű mappába teszi. A futtatható állományt ezzel a
paranccsal futtathatod:

```console
$ ./target/debug/hello_cargo # or .\target\debug\hello_cargo.exe on Windows
Hello, world!
```

Ha minden jól megy, a `Hello, world!` szövegnek kell megjelennie a
terminálban. A `cargo build` első futtatásakor a Cargo egy új fájlt is
létrehoz a legfelső szinten: a _Cargo.lock_ fájlt. Ez a fájl a projekted
függőségeinek pontos verzióit tartja nyilván. Ennek a projektnek nincsenek
függőségei, ezért a fájl meglehetősen szűkszavú. Ezt a fájlt soha nem kell
kézzel módosítanod; a tartalmát a Cargo kezeli helyetted.

A projektet az imént a `cargo build` paranccsal buildeltük, és a
`./target/debug/hello_cargo` paranccsal futtattuk, de a `cargo run`
paranccsal egyetlen lépésben le is fordíthatjuk a kódot, és futtathatjuk az
eredményül kapott futtatható állományt:

```console
$ cargo run
    Finished dev [unoptimized + debuginfo] target(s) in 0.0 secs
     Running `target/debug/hello_cargo`
Hello, world!
```

A `cargo run` használata kényelmesebb, mint ha arra kellene emlékezned, hogy
előbb a `cargo build` parancsot futtasd, majd a bináris teljes elérési útját
használd, ezért a legtöbb fejlesztő a `cargo run` parancsot használja.

Figyeld meg, hogy ezúttal nem láttunk olyan kimenetet, amely azt jelezte
volna, hogy a Cargo lefordítja a `hello_cargo`-t. A Cargo rájött, hogy a
fájlok nem változtak, ezért nem buildelt újra, csak futtatta a binárist. Ha
módosítottad volna a forráskódot, a Cargo futtatás előtt újrabuildelte volna
a projektet, és ezt a kimenetet láttad volna:

```console
$ cargo run
   Compiling hello_cargo v0.1.0 (file:///projects/hello_cargo)
    Finished dev [unoptimized + debuginfo] target(s) in 0.33 secs
     Running `target/debug/hello_cargo`
Hello, world!
```

A Cargo egy `cargo check` nevű parancsot is biztosít. Ez a parancs gyorsan
ellenőrzi, hogy a kódod lefordul-e, de nem hoz létre futtatható állományt:

```console
$ cargo check
   Checking hello_cargo v0.1.0 (file:///projects/hello_cargo)
    Finished dev [unoptimized + debuginfo] target(s) in 0.32 secs
```

Miért ne szeretnél futtatható állományt? A `cargo check` gyakran sokkal
gyorsabb, mint a `cargo build`, mert kihagyja a futtatható állomány
előállításának lépését. Ha kódírás közben folyamatosan ellenőrzöd a munkádat,
a `cargo check` használatával gyorsabban kiderül, hogy a projekted még mindig
lefordul-e! Ezért sok rustacean programírás közben rendszeresen futtatja a
`cargo check` parancsot, hogy megbizonyosodjon róla, hogy a kód lefordul.
Majd amikor készen állnak a futtatható állomány használatára, lefuttatják a
`cargo build` parancsot.

Foglaljuk össze, mit tanultunk eddig a Cargóról:

- Projektet a `cargo new` paranccsal hozhatunk létre.
- Projektet a `cargo build` paranccsal buildelhetünk.
- Egy lépésben buildelhetünk és futtathatunk egy projektet a `cargo run`
  paranccsal.
- A `cargo check` paranccsal bináris előállítása nélkül buildelhetünk egy
  projektet, hogy ellenőrizzük, van-e benne hiba.
- A Cargo a build eredményét nem a kódunkkal azonos mappába menti, hanem a
  _target/debug_ mappába.

A Cargo használatának további előnye, hogy a parancsok ugyanazok, bármelyik
operációs rendszeren dolgozol is. Ezért mostantól nem adunk külön utasításokat
Linuxra és macOS-re, illetve Windowsra.

### Buildelés kiadáshoz {#building-for-release}

Amikor a projekted végre készen áll a kiadásra, a `cargo build --release`
paranccsal optimalizálásokkal fordíthatod le. Ez a parancs a futtatható
állományt a _target/debug_ helyett a _target/release_ mappában hozza létre.
Az optimalizálások gyorsabbá teszik a Rust-kódod futását, de bekapcsolásuk
megnöveli a program fordítási idejét. Ezért van két különböző profil: az egyik
a fejlesztéshez, amikor gyorsan és gyakran szeretnél újrabuildelni, a másik
pedig annak a végleges programnak a buildeléséhez, amelyet a felhasználónak
adsz át, amelyet nem buildelsz újra ismételten, és amelynek a lehető
leggyorsabban kell futnia. Ha a kódod futásidejét méred, mindenképpen a
`cargo build --release` paranccsal fordíts, és a _target/release_ mappában
lévő futtatható állománnyal végezd a mérést.

<!-- Old headings. Do not remove or links may break. -->
<a id="cargo-as-convention"></a>

### A Cargo konvencióinak kihasználása {#leveraging-cargos-conventions}

Egyszerű projekteknél a Cargo nem nyújt sokkal többet, mint a `rustc` puszta
használata, de ahogy a programjaid egyre összetettebbek lesznek, megmutatja,
mennyit ér. Amint a programok több fájlból állnak, vagy függőségre van
szükségük, sokkal egyszerűbb a Cargóra bízni a build koordinálását.

Bár a `hello_cargo` projekt egyszerű, már most is azoknak a valódi eszközöknek
a nagy részét használja, amelyekkel a Rust-pályafutásod hátralévő részében
dolgozni fogsz. Sőt, bármely meglévő projekten való munkához a következő
parancsokkal töltheted le a kódot a Gittel, léphetsz be a projekt mappájába,
és buildelheted:

```console
$ git clone example.org/someproject
$ cd someproject
$ cargo build
```

A Cargóról további információkat [a dokumentációjában][cargo] találsz.

## Összefoglalás {#summary}

Nagyszerűen elindultál a Rust-utazásodon! Ebben a fejezetben megtanultad,
hogyan kell:

- telepíteni a Rust legfrissebb stabil verzióját a `rustup` segítségével,
- frissíteni egy újabb Rust-verzióra,
- megnyitni a helyben telepített dokumentációt,
- megírni és közvetlenül a `rustc` segítségével futtatni egy „Hello, world!”
  programot,
- létrehozni és futtatni egy új projektet a Cargo konvencióit követve.

Itt az ideje, hogy egy komolyabb programot írj, és hozzászokj a Rust-kód
olvasásához és írásához. Ezért a 2. fejezetben egy számkitalálós játékot
készítünk. Ha inkább azzal kezdenéd, hogy megtanulod, hogyan működnek az
általános programozási fogalmak a Rustban, olvasd el a 3. fejezetet, majd
térj vissza a 2. fejezethez.

[installation]: ch01-01-installation.html#installation
[toml]: https://toml.io
[appendix-e]: appendix-05-editions.html
[cargo]: https://doc.rust-lang.org/cargo/
