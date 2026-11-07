## A buildek testreszabása release profilokkal {#customizing-builds-with-release-profiles}

A Rustban a _release profilok (release profiles)_ előre definiált,
testreszabható profilok, eltérő konfigurációkkal, amelyek révén a programozó
jobban kézben tarthatja a kód fordításának különféle beállításait. Minden
profil a többitől függetlenül konfigurálható.

A Cargónak két fő profilja van: a `dev` profil, amelyet a Cargo a `cargo
build` futtatásakor használ, és a `release` profil, amelyet a `cargo build
--release` futtatásakor használ. A `dev` profil alapértelmezései a
fejlesztéshez, a `release` profil alapértelmezései pedig a release buildekhez
megfelelőek.

Ezek a profilnevek ismerősek lehetnek a buildjeid kimenetéből:

<!-- manual-regeneration
anywhere, run:
cargo build
cargo build --release
and ensure output below is accurate
-->

```console
$ cargo build
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.00s
$ cargo build --release
    Finished `release` profile [optimized] target(s) in 0.32s
```

A `dev` és a `release` a fordító által használt két különböző profil.

A Cargo minden profilhoz alapértelmezett beállításokat használ, amelyek akkor
érvényesek, ha a projekt _Cargo.toml_ fájljában nem adtál meg kifejezetten
`[profile.*]` szakaszokat. Ha bármelyik testreszabni kívánt profilhoz
`[profile.*]` szakaszt adsz hozzá, az alapértelmezett beállítások tetszőleges
részhalmazát felülbírálhatod. Például így néznek ki az `opt-level` beállítás
alapértelmezett értékei a `dev` és a `release` profilban:

<span class="filename">Fájlnév: Cargo.toml</span>

```toml
[profile.dev]
opt-level = 0

[profile.release]
opt-level = 3
```

Az `opt-level` (optimalizálási szint) beállítás azt szabályozza, hogy a Rust
mennyi optimalizálást alkalmazzon a kódodra; értéke 0 és 3 között lehet. Több
optimalizálás hosszabb fordítási időt jelent, ezért ha fejlesztés közben
gyakran fordítod a kódodat, kevesebb optimalizálást szeretnél, hogy gyorsabban
forduljon, még ha az eredményül kapott kód lassabban fut is. Ezért a `dev`
alapértelmezett `opt-level` értéke `0`. Amikor készen állsz a kódod
kiadására, érdemes több időt szánni a fordításra. Release módban csak egyszer
fordítasz, a lefordított programot viszont sokszor futtatod, így a release mód
a hosszabb fordítási időért cserébe gyorsabban futó kódot ad. Ezért a
`release` profil alapértelmezett `opt-level` értéke `3`.

Egy alapértelmezett beállítást felülbírálhatsz, ha a _Cargo.toml_ fájlban más
értéket adsz meg hozzá. Ha például a fejlesztői profilban az 1-es
optimalizálási szintet szeretnénk használni, a következő két sort adhatjuk
hozzá a projektünk _Cargo.toml_ fájljához:

<span class="filename">Fájlnév: Cargo.toml</span>

```toml
[profile.dev]
opt-level = 1
```

Ez a kód felülbírálja a `0` alapértelmezett beállítást. Ha most lefuttatjuk a
`cargo build` parancsot, a Cargo a `dev` profil alapértelmezéseit használja,
kiegészítve az `opt-level` általunk testreszabott értékével. Mivel az
`opt-level` értékét `1`-re állítottuk, a Cargo több optimalizálást alkalmaz,
mint alapértelmezés szerint, de nem annyit, mint egy release buildben.

Az egyes profilok összes konfigurációs lehetőségének és alapértelmezésének
teljes listáját [a Cargo dokumentációjában](https://doc.rust-lang.org/cargo/reference/profiles.html)
találod.
