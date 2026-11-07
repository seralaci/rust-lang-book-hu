## Csomagok és crate-ek {#packages-and-crates}

A modulrendszer első részei, amelyekkel foglalkozunk, a csomagok és a
crate-ek.

A _crate_ a kód legkisebb egysége, amelyet a Rust fordító egyszerre kezel.
Akkor is, ha a `cargo` helyett a `rustc`-t futtatod, és egyetlen forrásfájlt
adsz át neki (ahogy azt még az 1. fejezet [„A Rust-programok
alapjai”][basics]<!-- ignore --> szakaszában tettük), a fordító ezt a fájlt
crate-nek tekinti. A crate-ek modulokat tartalmazhatnak, a modulok pedig más
fájlokban is definiálhatók, amelyek a crate-tel együtt fordulnak le, ahogy a
következő szakaszokban látni fogjuk.

Egy crate kétféle lehet: bináris crate vagy könyvtár crate. A _bináris
crate-ek (binary crates)_ olyan programok, amelyeket futtatható állománnyá
fordíthatsz és futtathatsz, például egy parancssori program vagy egy szerver.
Mindegyiknek kell lennie egy `main` nevű függvényének, amely meghatározza, mi
történik a futtatható állomány indításakor. Az eddig létrehozott crate-jeink
mind bináris crate-ek voltak.

A _könyvtár crate-eknek (library crates)_ nincs `main` függvényük, és nem
futtatható állománnyá fordulnak. Ehelyett olyan funkciókat definiálnak,
amelyeket több projekt is használhat. A [2. fejezetben][rand]<!-- ignore -->
használt `rand` crate például véletlenszámokat előállító funkciókat nyújt. A
rustaceanek legtöbbször könyvtár crate-et értenek „crate” alatt, és a „crate”
szót a „könyvtár” általános programozási fogalmával felcserélhetően használják.

A _crate-gyökér (crate root)_ az a forrásfájl, amelyből a Rust fordító kiindul,
és amely a crate gyökérmodulját alkotja (a modulokat részletesen a
[„Hatókör és láthatóság szabályozása modulokkal”][modules]<!-- ignore -->
szakaszban magyarázzuk el).

A _csomag (package)_ egy vagy több crate-ből álló egység, amely valamilyen
funkciókészletet nyújt. A csomag tartalmaz egy _Cargo.toml_ fájlt, amely
leírja, hogyan kell ezeket a crate-eket lefordítani. A Cargo maga is egy
csomag, amely a kódod buildeléséhez használt parancssori eszköz bináris
crate-jét tartalmazza. A Cargo csomagja egy könyvtár crate-et is tartalmaz,
amelytől a bináris crate függ. Más projektek is függhetnek a Cargo könyvtár
crate-jétől, hogy ugyanazt a logikát használják, mint a Cargo parancssori
eszköze.

Egy csomag tetszőleges számú bináris crate-et tartalmazhat, de legfeljebb egy
könyvtár crate-et. Egy csomagnak legalább egy crate-et tartalmaznia kell,
legyen az könyvtár vagy bináris crate.

Nézzük végig, mi történik, amikor létrehozunk egy csomagot. Először kiadjuk a
`cargo new my-project` parancsot:

```console
$ cargo new my-project
     Created binary (application) `my-project` package
$ ls my-project
Cargo.toml
src
$ ls my-project/src
main.rs
```

A `cargo new my-project` futtatása után az `ls` paranccsal megnézzük, mit hoz
létre a Cargo. A _my-project_ mappában van egy _Cargo.toml_ fájl, ez adja a
csomagot. Van egy _src_ mappa is, amely a _main.rs_ fájlt tartalmazza. Nyisd
meg a _Cargo.toml_ fájlt a szövegszerkesztődben, és figyeld meg, hogy az
_src/main.rs_ sehol sem szerepel benne. A Cargo azt a konvenciót követi, hogy
az _src/main.rs_ egy, a csomaggal azonos nevű bináris crate crate-gyökere.
Hasonlóképpen a Cargo tudja, hogy ha a csomag mappája tartalmaz egy
_src/lib.rs_ fájlt, akkor a csomag egy, a csomaggal azonos nevű könyvtár
crate-et tartalmaz, amelynek crate-gyökere az _src/lib.rs_. A Cargo a
crate-gyökérfájlokat adja át a `rustc`-nek a könyvtár vagy a bináris
lefordításához.

Itt egy olyan csomagunk van, amely csak az _src/main.rs_ fájlt tartalmazza,
vagyis csak egy `my-project` nevű bináris crate van benne. Ha egy csomag az
_src/main.rs_ és az _src/lib.rs_ fájlt is tartalmazza, akkor két crate-je van:
egy bináris és egy könyvtár crate, mindkettő a csomaggal azonos nevű. Egy
csomagnak több bináris crate-je is lehet, ha fájlokat helyezünk az _src/bin_
mappába: minden fájl egy külön bináris crate lesz.

[basics]: ch01-02-hello-world.html#rust-program-basics
[modules]: ch07-02-defining-modules-to-control-scope-and-privacy.html
[rand]: ch02-00-guessing-game-tutorial.html#generating-a-random-number
