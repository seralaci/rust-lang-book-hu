## Telepítés {#installation}

Az első lépés a Rust telepítése. A Rustot a `rustup` segítségével töltjük le;
ez egy parancssori eszköz a Rust-verziók és a hozzájuk tartozó eszközök
kezelésére. A letöltéshez internetkapcsolatra lesz szükséged.

> Megjegyzés: Ha valamilyen okból nem szeretnéd a `rustup`-ot használni, további
> lehetőségeket az [egyéb Rust-telepítési módszereket bemutató
> oldalon][otherinstall] találsz.

Az alábbi lépésekkel a Rust fordító legfrissebb stabil verzióját telepítheted.
A Rust stabilitási garanciái biztosítják, hogy a könyv minden olyan példája,
amely lefordul, a Rust újabb verzióival is le fog fordulni. A kimenet
verzióról verzióra kissé eltérhet, mert a Rust gyakran javít a hibaüzenetein
és figyelmeztetésein. Másként fogalmazva: a Rust bármely újabb stabil
verziójának, amelyet ezekkel a lépésekkel telepítesz, a várakozásoknak
megfelelően kell működnie a könyv tartalmával.

> ### Parancssori jelölések {#command-line-notation}
>
> Ebben a fejezetben és a könyv egészében mutatunk majd néhány, a terminálban
> használt parancsot. A terminálba beírandó sorok mindegyike `$` jellel
> kezdődik. A `$` karaktert nem kell begépelned; ez a parancssori prompt, amely
> az egyes parancsok kezdetét jelzi. A `$` jellel nem kezdődő sorok általában
> az előző parancs kimenetét mutatják. A PowerShell-specifikus példákban
> pedig `$` helyett `>` szerepel.

### A `rustup` telepítése Linuxon vagy macOS-en {#installing-rustup-on-linux-or-macos}

Ha Linuxot vagy macOS-t használsz, nyiss meg egy terminált, és írd be a
következő parancsot:

```console
$ curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh
```

A parancs letölt egy szkriptet, és elindítja a `rustup` eszköz telepítését,
amely a Rust legfrissebb stabil verzióját telepíti. Előfordulhat, hogy a
rendszer a jelszavadat kéri. Ha a telepítés sikeres, a következő sor jelenik
meg:

```text
Rust is installed now. Great!
```

Szükséged lesz egy _linkerre_ is; ez egy olyan program, amellyel a Rust a
lefordított kimeneteit egyetlen fájllá szerkeszti össze. Valószínűleg már van
egy a gépeden. Ha linkerhibákat kapsz, telepíts egy C fordítót, amely
általában linkert is tartalmaz. A C fordító azért is hasznos, mert néhány
gyakran használt Rust-csomag C kódra épül, és szüksége van C fordítóra.

macOS-en a következő paranccsal szerezhetsz C fordítót:

```console
$ xcode-select --install
```

A Linux-felhasználóknak általában a GCC-t vagy a Clangot érdemes telepíteniük a
disztribúciójuk dokumentációja szerint. Ha például Ubuntut használsz, telepítsd
a `build-essential` csomagot.

### A `rustup` telepítése Windowson {#installing-rustup-on-windows}

Windowson látogass el a
[https://www.rust-lang.org/tools/install][install]<!-- ignore --> oldalra, és
kövesd a Rust telepítésére vonatkozó utasításokat. A telepítés egy pontján a
telepítő a Visual Studio telepítését is kéri. Ez biztosítja a linkert és a
programok fordításához szükséges natív könyvtárakat. Ha további segítségre van
szükséged ehhez a lépéshez, nézd meg a
[https://rust-lang.github.io/rustup/installation/windows-msvc.html][msvc]<!--
ignore --> oldalt.

A könyv további részében olyan parancsokat használunk, amelyek a _cmd.exe_-ben
és a PowerShellben is működnek. Ha valahol eltérés van, elmagyarázzuk, melyiket
kell használni.

### Hibaelhárítás {#troubleshooting}

Ha ellenőrizni szeretnéd, hogy helyesen telepítetted-e a Rustot, nyiss meg
egy parancsértelmezőt, és írd be a következő sort:

```console
$ rustc --version
```

Ekkor a legutóbb kiadott stabil verzió verziószámát, commit-hash-ét és
commitdátumát kell látnod a következő formában:

```text
rustc x.y.z (abcabcabc yyyy-mm-dd)
```

Ha ezt az információt látod, sikeresen telepítetted a Rustot! Ha nem, a
következőképpen ellenőrizd, hogy a Rust szerepel-e a `%PATH%`
rendszerváltozóban.

Windows CMD-ben:

```console
> echo %PATH%
```

PowerShellben:

```powershell
> echo $env:Path
```

Linuxon és macOS-en:

```console
$ echo $PATH
```

Ha minden rendben van, és a Rust mégsem működik, több helyen is kérhetsz
segítséget. A [közösségi oldalon][community] megtudhatod, hogyan léphetsz
kapcsolatba más rustaceanekkel (ez a kissé bolondos becenév, amellyel
magunkat illetjük).

### Frissítés és eltávolítás {#updating-and-uninstalling}

Ha a Rustot a `rustup` segítségével telepítetted, az újonnan kiadott verzióra
való frissítés egyszerű. Futtasd a következő frissítő szkriptet a
parancsértelmezőben:

```console
$ rustup update
```

A Rust és a `rustup` eltávolításához futtasd a következő eltávolító szkriptet a
parancsértelmezőben:

```console
$ rustup self uninstall
```

<!-- Old headings. Do not remove or links may break. -->
<a id="local-documentation"></a>

### A helyi dokumentáció olvasása {#reading-the-local-documentation}

A Rust telepítése a dokumentáció helyi másolatát is tartalmazza, így azt
offline is olvashatod. A helyi dokumentációt a `rustup doc` paranccsal
nyithatod meg a böngésződben.

Ha a standard könyvtár valamelyik típusáról vagy függvényéről nem tudod
biztosan, mit csinál vagy hogyan kell használni, keresd meg az
alkalmazásprogramozási felület (API) dokumentációjában!

<!-- Old headings. Do not remove or links may break. -->
<a id="text-editors-and-integrated-development-environments"></a>

### Szövegszerkesztők és IDE-k használata {#using-text-editors-and-ides}

A könyv semmit sem feltételez arról, milyen eszközökkel írod a Rust-kódot.
Szinte bármelyik szövegszerkesztő megteszi! Sok szövegszerkesztő és integrált
fejlesztőkörnyezet (IDE) azonban beépített Rust-támogatással rendelkezik. A
szerkesztők és IDE-k egy viszonylag friss listáját mindig megtalálod a Rust
weboldalának [eszközöket bemutató oldalán][tools].

### Offline munka a könyvvel {#working-offline-with-this-book}

Több példában a standard könyvtáron túli Rust-csomagokat is használunk. Ezeknek
a példáknak a kipróbálásához vagy internetkapcsolatra lesz szükséged, vagy
előre le kell töltened a függőségeket. A függőségek előzetes letöltéséhez
futtasd a következő parancsokat. (Később részletesen elmagyarázzuk, mi az a
`cargo`, és mit csinálnak ezek a parancsok.)

<!-- When updating the version of `rand` used, also update the version of
`rand` used in these files so they all match:

* ch02-00-guessing-game-tutorial.md
* ch07-04-bringing-paths-into-scope-with-the-use-keyword.md
* ch14-03-cargo-workspaces.md
-->

```console
$ cargo new get-dependencies
$ cd get-dependencies
$ cargo add rand@0.10.1 trpl@0.2.0
```

Ez a gyorsítótárba menti a csomagok letöltött változatát, így később nem kell
újra letöltened őket. A parancs lefuttatása után a `get-dependencies` mappát
nem kell megtartanod. Ha lefuttattad ezt a parancsot, a könyv további részében
minden `cargo` parancsnál használhatod az `--offline` kapcsolót, hogy a
hálózat helyett ezeket a gyorsítótárban lévő verziókat használja.

[otherinstall]: https://forge.rust-lang.org/infra/other-installation-methods.html
[install]: https://www.rust-lang.org/tools/install
[msvc]: https://rust-lang.github.io/rustup/installation/windows-msvc.html
[community]: https://www.rust-lang.org/community
[tools]: https://www.rust-lang.org/tools
