## Hello, World! {#hello-world}

Most, hogy telepítetted a Rustot, ideje megírnod az első Rust-programodat.
Egy új nyelv tanulásakor hagyomány, hogy egy kis programot írunk, amely a
`Hello, world!` szöveget írja ki a képernyőre – mi is ezt tesszük!

> Megjegyzés: A könyv feltételezi, hogy alapszinten ismered a parancssort. A
> Rust semmilyen különleges elvárást nem támaszt a szerkesztővel, az eszközökkel
> vagy a kódod helyével kapcsolatban, így ha a parancssor helyett szívesebben
> használsz IDE-t, nyugodtan használd a kedvencedet. Ma már sok IDE támogatja
> valamilyen szinten a Rustot; a részletekért nézd meg az adott IDE
> dokumentációját. A Rust csapata a `rust-analyzer` segítségével arra
> összpontosít, hogy kiváló IDE-támogatást tegyen lehetővé. További
> részleteket [a D. függelékben][devtools]<!-- ignore --> találsz.

<!-- Old headings. Do not remove or links may break. -->
<a id="creating-a-project-directory"></a>

### A projektmappa létrehozása {#project-directory-setup}

Először hozz létre egy mappát a Rust-kódod tárolására. A Rust számára mindegy,
hol van a kódod, de a könyv gyakorlataihoz és projektjeihez azt javasoljuk,
hogy hozz létre egy _projects_ mappát a saját felhasználói mappádban, és ott
tartsd az összes projektedet.

Nyiss meg egy terminált, és a következő parancsokkal hozz létre egy _projects_
mappát, azon belül pedig egy mappát a „Hello, world!” projekt számára.

Linuxon, macOS-en és Windowson a PowerShellben ezt írd be:

```console
$ mkdir ~/projects
$ cd ~/projects
$ mkdir hello_world
$ cd hello_world
```

Windows CMD-ben ezt:

```cmd
> mkdir "%USERPROFILE%\projects"
> cd /d "%USERPROFILE%\projects"
> mkdir hello_world
> cd hello_world
```

<!-- Old headings. Do not remove or links may break. -->
<a id="writing-and-running-a-rust-program"></a>

### A Rust-programok alapjai {#rust-program-basics}

Ezután hozz létre egy új forrásfájlt, és nevezd el _main.rs_-nek. A
Rust-fájlok kiterjesztése mindig _.rs_. Ha a fájlnév több szóból áll, a
konvenció szerint aláhúzásjellel választjuk el őket. Például _hello_world.rs_
legyen a neve, ne _helloworld.rs_.

Most nyisd meg az imént létrehozott _main.rs_ fájlt, és írd be az 1-1.
kódrészletben látható kódot.

<Listing number="1-1" file-name="main.rs" caption="Egy program, amely kiírja, hogy `Hello, world!`">

```rust
fn main() {
    println!("Hello, world!");
}
```

</Listing>

Mentsd el a fájlt, és térj vissza a terminálablakba, a
_~/projects/hello_world_ mappába. Linuxon vagy macOS-en a következő
parancsokkal fordíthatod le és futtathatod a fájlt:

```console
$ rustc main.rs
$ ./main
Hello, world!
```

Windowson a `./main` helyett a `.\main` parancsot írd be:

```powershell
> rustc main.rs
> .\main
Hello, world!
```

Az operációs rendszeredtől függetlenül a `Hello, world!` szövegnek kell
megjelennie a terminálban. Ha nem ezt a kimenetet látod, a segítségkérés
lehetőségeiről a Telepítés szakasz
[„Hibaelhárítás”][troubleshooting]<!-- ignore --> részében olvashatsz.

Ha megjelent a `Hello, world!`, gratulálunk! Hivatalosan is megírtad az első
Rust-programodat. Ezzel Rust-programozó lettél – üdvözlünk!

<!-- Old headings. Do not remove or links may break. -->

<a id="anatomy-of-a-rust-program"></a>

### Egy Rust-program felépítése {#the-anatomy-of-a-rust-program}

Nézzük meg részletesen ezt a „Hello, world!” programot. Íme a kirakós első
darabja:

```rust
fn main() {

}
```

Ezek a sorok egy `main` nevű függvényt definiálnak. A `main` függvény
különleges: minden futtatható Rust-programban mindig ez a kód fut le
elsőként. Az első sor egy `main` nevű függvényt deklarál, amelynek nincsenek
paraméterei, és nem ad vissza semmit. Ha lennének paraméterei, azok a zárójelek
(`()`) közé kerülnének.

A függvény törzsét `{}` veszi körül. A Rust minden függvénytörzs körül
kapcsos zárójelet követel meg. Jó stílus, ha a nyitó kapcsos zárójelet a
függvénydeklarációval egy sorba írjuk, egy szóközzel elválasztva.

> Megjegyzés: Ha a Rust-projektjeidben egységes stílust szeretnél követni, a
> `rustfmt` nevű automatikus formázóeszközzel egy adott stílusra formázhatod a
> kódodat (a `rustfmt`-ről bővebben [a D. függelékben][devtools]<!-- ignore -->
> olvashatsz). A Rust csapata ezt az eszközt – a `rustc`-hez hasonlóan – a
> standard Rust-disztribúció részévé tette, így valószínűleg már telepítve van a
> gépeden!

A `main` függvény törzse a következő kódot tartalmazza:

```rust
println!("Hello, world!");
```

Ez a sor végzi el a kis programunk teljes munkáját: szöveget ír ki a
képernyőre. Három fontos részletet érdemes itt észrevenni.

Először is: a `println!` egy Rust-makrót hív meg. Ha függvényt hívna, akkor
`println` alakban szerepelne (`!` nélkül). A Rust-makrók segítségével olyan
kódot írhatunk, amely kódot generál, és így kibővíti a Rust szintaxisát; a
makrókat részletesebben [a 20. fejezetben][ch20-macros]<!-- ignore -->
tárgyaljuk. Egyelőre elég annyit tudnod, hogy a `!` azt jelzi, hogy makrót
hívsz meg, nem pedig közönséges függvényt, és hogy a makrók nem mindig
ugyanazokat a szabályokat követik, mint a függvények.

Másodszor: láthatod a `"Hello, world!"` sztringet. Ezt a sztringet
argumentumként adjuk át a `println!` makrónak, és a sztring megjelenik a
képernyőn.

Harmadszor: a sort pontosvesszővel (`;`) zárjuk, amely jelzi, hogy ez a
kifejezés véget ért, és kezdődhet a következő. A Rust-kód legtöbb sora
pontosvesszővel végződik.

<!-- Old headings. Do not remove or links may break. -->
<a id="compiling-and-running-are-separate-steps"></a>

### Fordítás és futtatás {#compilation-and-execution}

Az imént futtattál egy frissen megírt programot, úgyhogy vizsgáljuk meg a
folyamat egyes lépéseit.

Egy Rust-program futtatása előtt le kell fordítanod a Rust fordítóval: írd be
a `rustc` parancsot, és add át neki a forrásfájlod nevét, így:

```console
$ rustc main.rs
```

Ha van C vagy C++ előismereted, észreveheted, hogy ez a `gcc`-hez vagy a
`clang`-hoz hasonló. Sikeres fordítás után a Rust egy bináris futtatható
állományt hoz létre.

Linuxon, macOS-en és Windowson a PowerShellben a futtatható állományt a
parancsértelmezőbe írt `ls` paranccsal láthatod:

```console
$ ls
main  main.rs
```

Linuxon és macOS-en két fájlt fogsz látni. Windowson a PowerShellben
ugyanazt a három fájlt látod, mint a CMD használatakor. Windowson a CMD-ben a
következőt kell beírnod:

```cmd
> dir /B %= the /B option says to only show the file names =%
main.exe
main.pdb
main.rs
```

Itt látható a _.rs_ kiterjesztésű forráskódfájl, a futtatható állomány
(Windowson _main.exe_, minden más platformon _main_), valamint Windows
használata esetén egy _.pdb_ kiterjesztésű fájl, amely hibakeresési
információkat tartalmaz. Innen a _main_ vagy a _main.exe_ fájlt futtathatod,
így:

```console
$ ./main # or .\main on Windows
```

Ha a _main.rs_ a „Hello, world!” programod, ez a sor kiírja a terminálba, hogy
`Hello, world!`.

Ha inkább dinamikus nyelvekben, például Rubyban, Pythonban vagy JavaScriptben
vagy otthon, lehet, hogy nem szoktad meg, hogy a program fordítása és
futtatása külön lépés. A Rust _előre fordított (ahead-of-time compiled)_
nyelv, ami azt jelenti, hogy lefordíthatsz egy programot, a futtatható
állományt odaadhatod valaki másnak, és ő akkor is futtathatja, ha nincs
telepítve nála a Rust. Ha viszont valakinek egy _.rb_, _.py_ vagy _.js_ fájlt
adsz, akkor rendelkeznie kell (rendre) egy Ruby-, Python- vagy
JavaScript-megvalósítással. Ezekben a nyelvekben viszont egyetlen paranccsal
lefordíthatod és futtathatod a programodat. A nyelvtervezésben minden
kompromisszum kérdése.

Egyszerű programokhoz elég a `rustc`-vel fordítani, de ahogy a projekted nő,
kezelni szeretnéd majd a különböző beállításokat, és meg szeretnéd könnyíteni
a kódod megosztását. A következő részben bemutatjuk a Cargo eszközt, amely
segít valódi, a gyakorlatban is használható Rust-programokat írni.

[troubleshooting]: ch01-01-installation.html#troubleshooting
[devtools]: appendix-04-useful-development-tools.html
[ch20-macros]: ch20-05-macros.html
