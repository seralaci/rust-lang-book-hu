## G. függelék: Hogyan készül a Rust, és mi az a „nightly Rust”? {#appendix-g---how-rust-is-made-and-nightly-rust}

Ez a függelék arról szól, hogyan készül a Rust, és ez hogyan érint téged mint
Rust-fejlesztőt.

### Stabilitás stagnálás nélkül {#stability-without-stagnation}

Nyelvként a Rust _nagyon_ sokat ad a kódod stabilitására. Azt szeretnénk, hogy
a Rust sziklaszilárd alap legyen, amelyre építhetsz, és ha a dolgok folyamatosan
változnának, ez lehetetlen volna. Ugyanakkor ha nem kísérletezhetünk új
funkciókkal, előfordulhat, hogy a fontos hibáikra csak a megjelenésük után
derül fény, amikor már nem változtathatunk rajtuk.

Erre a problémára az általunk „stabilitás stagnálás nélkül” néven emlegetett
megoldást alkalmazzuk, és a vezérelvünk a következő: soha nem kell tartanod
attól, hogy a stabil Rust egy új verziójára frissíts. Minden frissítésnek
fájdalommentesnek kell lennie, ugyanakkor új funkciókat, kevesebb hibát és
gyorsabb fordítási időt is kell hoznia.

### Pöfögő vonatok: kiadási csatornák és a vonatokon utazás {#choo-choo-release-channels-and-riding-the-trains}

A Rust fejlesztése _menetrend (train schedule)_ szerint zajlik. Ez azt jelenti,
hogy minden fejlesztés a Rust tárolójának fő ágán történik. A kiadások a
_kiadási vonat (release train)_ modellt követik, amelyet a Cisco IOS és más
szoftverprojektek is használnak. A Rustnak három _kiadási csatornája (release
channel)_ van:

- Nightly
- Beta
- Stable

A legtöbb Rust-fejlesztő elsősorban a stable csatornát használja, de akik ki
szeretnék próbálni a kísérleti új funkciókat, a nightlyt vagy a betát is
használhatják.

Nézzünk egy példát a fejlesztési és kiadási folyamat működésére: tegyük fel,
hogy a Rust csapat a Rust 1.5 kiadásán dolgozik. Ez a kiadás 2015 decemberében
jelent meg, de így valószerű verziószámokkal dolgozhatunk. Egy új funkció
kerül a Rustba: egy új commit érkezik a fő ágra. Minden éjjel elkészül a Rust
egy új nightly verziója. Minden nap kiadási nap, és ezeket a kiadásokat a
kiadási infrastruktúránk automatikusan hozza létre. Ahogy telik az idő, a
kiadásaink így néznek ki, éjjelente egy:

```text
nightly: * - - * - - *
```

Hathetente eljön az ideje egy új kiadás előkészítésének! A Rust tárolójának
`beta` ága leágazik a nightly által használt fő ágról. Így most két kiadás van:

```text
nightly: * - - * - - *
                     |
beta:                *
```

A legtöbb Rust-felhasználó nem használja aktívan a béta kiadásokat, de a CI
rendszerükben a béta ellen is tesztelnek, így segítenek a Rustnak felfedezni
az esetleges regressziókat. Közben továbbra is minden éjjel készül egy nightly
kiadás:

```text
nightly: * - - * - - * - - * - - *
                     |
beta:                *
```

Tegyük fel, hogy találnak egy regressziót. Még jó, hogy volt időnk tesztelni
a béta kiadást, mielőtt a regresszió bekerült volna egy stabil kiadásba! A
javítás a fő ágra kerül, így a nightly is javul, majd a javítást
visszaportolják a `beta` ágra, és elkészül a béta egy új kiadása:

```text
nightly: * - - * - - * - - * - - * - - *
                     |
beta:                * - - - - - - - - *
```

Hat héttel az első béta elkészülte után eljön a stabil kiadás ideje! A
`stable` ág a `beta` ágból készül:

```text
nightly: * - - * - - * - - * - - * - - * - * - *
                     |
beta:                * - - - - - - - - *
                                       |
stable:                                *
```

Hurrá! Kész a Rust 1.5! Egy dologról azonban megfeledkeztünk: mivel eltelt a
hat hét, a Rust _következő_ verziójának, az 1.6-nak is szüksége van egy új
bétára. Így miután a `stable` leágazott a `beta`-ról, a `beta` következő
verziója ismét a `nightly`-ról ágazik le:

```text
nightly: * - - * - - * - - * - - * - - * - * - *
                     |                         |
beta:                * - - - - - - - - *       *
                                       |
stable:                                *
```

Ezt hívják „vonatmodellnek”, mert hathetente egy kiadás „kigördül az
állomásról”, de még végig kell utaznia a béta csatornán, mielőtt stabil
kiadásként célba ér.

A Rust óramű pontossággal hathetente jelenik meg. Ha ismered egy Rust-kiadás
dátumát, a következőét is tudod: hat héttel később lesz. A hathetente ütemezett
kiadások egyik előnye, hogy a következő vonat hamarosan érkezik. Ha egy
funkció történetesen lekési az adott kiadást, nincs miért aggódni: rövidesen
jön a következő! Ez segít csökkenteni a nyomást, hogy esetleg kiforratlan
funkciókat csempésszenek be közvetlenül a kiadási határidő előtt.

Ennek a folyamatnak köszönhetően mindig kipróbálhatod a Rust következő
buildjét, és saját magad ellenőrizheted, hogy könnyű-e rá frissíteni: ha egy
béta kiadás nem úgy működik, ahogy várnád, jelezheted a csapatnak, és még a
következő stabil kiadás előtt kijavíttathatod! A béta kiadások viszonylag
ritkán hibásak, de a `rustc` is csak egy szoftver, és hibák bizony
előfordulnak.

### Támogatási idő {#maintenance-time}

A Rust projekt a legfrissebb stabil verziót támogatja. Amikor egy új stabil
verzió megjelenik, a régi verzió támogatása megszűnik (end of life, EOL). Ez
azt jelenti, hogy minden verzió hat hétig támogatott.

### Instabil funkciók {#unstable-features}

Ennek a kiadási modellnek van még egy csavarja: az instabil funkciók. A Rust
egy „funkciókapcsolóknak” nevezett technikával határozza meg, hogy egy adott
kiadásban mely funkciók engedélyezettek. Ha egy új funkció aktív fejlesztés
alatt áll, bekerül a fő ágra, így a nightlyba is, de egy _funkciókapcsoló
(feature flag)_ mögött. Ha felhasználóként ki szeretnéd próbálni a
fejlesztés alatt álló funkciót, megteheted, de a Rust egy nightly kiadását
kell használnod, és a forráskódodat a megfelelő kapcsolóval kell annotálnod,
hogy bekapcsold.

Ha a Rust béta vagy stabil kiadását használod, semmilyen funkciókapcsolót nem
használhatsz. Ez a kulcsa annak, hogy az új funkciókat a gyakorlatban is
kipróbálhassuk, mielőtt örökre stabilnak nyilvánítanánk őket. Aki a
legújabb fejlesztéseket szeretné használni, megteheti, aki pedig
sziklaszilárd élményre vágyik, maradhat a stable mellett, és tudhatja, hogy a
kódja nem fog elromlani. Stabilitás stagnálás nélkül.

Ez a könyv csak a stabil funkciókról tartalmaz információt, mivel a fejlesztés
alatt álló funkciók még változnak, és biztosan mások lesznek, amikor stabil
buildekben is elérhetővé válnak, mint a könyv írásakor. A csak nightlyban
elérhető funkciók dokumentációját megtalálod az interneten.

### A rustup és a nightly Rust szerepe {#rustup-and-the-role-of-rust-nightly}

A rustup megkönnyíti a Rust különböző kiadási csatornái közötti váltást,
globálisan vagy projektenként. Alapértelmezés szerint a stabil Rust lesz
telepítve. A nightly telepítéséhez például:

```console
$ rustup toolchain install nightly
```

A `rustup` segítségével az összes telepített _eszközláncot (toolchain)_ (a
Rust kiadásait és a hozzájuk tartozó komponenseket) is megnézheted. Íme egy
példa az egyik szerző Windowsos számítógépéről:

```powershell
> rustup toolchain list
stable-x86_64-pc-windows-msvc (default)
beta-x86_64-pc-windows-msvc
nightly-x86_64-pc-windows-msvc
```

Ahogy látod, a stabil eszközlánc az alapértelmezett. A legtöbb
Rust-felhasználó legtöbbször a stable-t használja. Elképzelhető, hogy te is
többnyire a stable-t szeretnéd használni, egy adott projektben viszont a
nightlyt, mert fontos számodra egy legújabb funkció. Ehhez a projekt
mappájában a `rustup override` segítségével beállíthatod, hogy a `rustup` a
nightly eszközláncot használja, amikor abban a mappában vagy:

```console
$ cd ~/projects/needs-nightly
$ rustup override set nightly
```

Mostantól valahányszor a _~/projects/needs-nightly_ mappán belül meghívod a
`rustc`-t vagy a `cargo`-t, a `rustup` gondoskodik róla, hogy a nightly Rustot
használd az alapértelmezett stabil Rust helyett. Ez nagyon jól jön, ha sok
Rust-projekted van!

### Az RFC-folyamat és a csapatok {#the-rfc-process-and-teams}

Hogyan értesülhetsz tehát ezekről az új funkciókról? A Rust fejlesztési
modellje a _Request For Comments (RFC) folyamatot_ követi. Ha valamilyen
fejlesztést szeretnél a Rustban, megírhatsz egy javaslatot, amelyet RFC-nek
nevezünk.

Bárki írhat RFC-t a Rust fejlesztésére, a javaslatokat pedig a Rust csapat
vizsgálja meg és vitatja meg, amely számos témakörönkénti alcsapatból áll. A
csapatok teljes listája megtalálható [a Rust honlapján](https://www.rust-lang.org/governance); ez a projekt
minden területéhez tartalmaz csapatokat: nyelvtervezés, a fordító
megvalósítása, infrastruktúra, dokumentáció és így tovább. Az illetékes csapat
elolvassa a javaslatot és a hozzászólásokat, saját megjegyzéseket is fűz
hozzá, és végül konszenzus születik a funkció elfogadásáról vagy elutasításáról.

Ha a funkciót elfogadják, a Rust tárolójában megnyitnak egy issue-t, és
valaki megvalósíthatja. Könnyen lehet, hogy a megvalósító nem ugyanaz a
személy, aki eredetileg a funkciót javasolta! Amikor a megvalósítás elkészül,
egy funkciókapu (feature gate) mögött bekerül a fő ágra, ahogy azt az
[„Instabil funkciók”](#unstable-features)<!-- ignore --> szakaszban
tárgyaltuk.

Egy idő után, amikor a nightly kiadásokat használó Rust-fejlesztők már
kipróbálhatták az új funkciót, a csapattagok megvitatják a funkciót, azt, hogy
hogyan vált be a nightlyban, és eldöntik, hogy bekerüljön-e a stabil Rustba.
Ha a döntés a továbblépés, a funkciókaput eltávolítják, és a funkció ettől
kezdve stabilnak számít! A vonatokkal együtt utazik be a Rust egy új stabil
kiadásába.
