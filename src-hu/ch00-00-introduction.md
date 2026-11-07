# Bevezetés {#introduction}

> Megjegyzés: A könyv jelen kiadása megegyezik a No Starch Press által
> nyomtatott és e-könyv formátumban kiadott [The Rust Programming
> Language][nsprust] című könyvvel ([No Starch Press][nsp]).

[nsprust]: https://nostarch.com/rust-programming-language-3rd-edition
[nsp]: https://nostarch.com/

Üdvözlünk _A Rust programozási nyelv_ oldalain! Ez a könyv a Rust nyelvbe
vezet be. A Rust programozási nyelv segít gyorsabb és megbízhatóbb szoftvert
írni. A programozási nyelvek tervezésében a magas szintű kényelem és az
alacsony szintű irányítás gyakran ütközik egymással; a Rust ezt az ellentétet
kérdőjelezi meg. A komoly technikai képességek és a kiváló fejlesztői élmény
egyensúlyával a Rust lehetővé teszi, hogy az alacsony szintű részleteket
(például a memóriahasználatot) is kézben tartsd, anélkül hogy meg kellene
küzdened az ezzel hagyományosan járó nehézségekkel.

## Kinek szól a Rust? {#who-rust-is-for}

A Rust sokféle ember számára sokféle okból ideális választás. Nézzük meg a
legfontosabb csoportokat!

### Fejlesztőcsapatok {#teams-of-developers}

A Rust hatékony eszköznek bizonyul a nagy fejlesztőcsapatok együttműködésében,
még akkor is, ha a csapattagok rendszerprogramozási tudása eltérő szintű. Az
alacsony szintű kódban könnyen megbújnak alattomos hibák, amelyeket a legtöbb
nyelvben csak alapos teszteléssel és tapasztalt fejlesztők gondos
kódátnézésével lehet elkapni. A Rustban a fordító kapuőrként működik: nem
hajlandó lefordítani az ilyen nehezen megfogható hibákat tartalmazó kódot,
beleértve a konkurens programozásból eredő hibákat is. A fordítóval együtt
dolgozva a csapat a program logikájára összpontosíthat ahelyett, hogy a
hibákat hajkurászná.

A Rust a modern fejlesztőeszközöket is elhozza a rendszerprogramozás
világába:

- A Cargo, a beépített függőségkezelő és buildeszköz, fájdalommentessé és a
  teljes Rust-ökoszisztémában egységessé teszi a függőségek hozzáadását,
  fordítását és kezelését.
- A `rustfmt` formázóeszköz egységes kódstílust biztosít a fejlesztők
  között.
- A Rust Language Server adja az integrált fejlesztőkörnyezetek (IDE-k)
  kódkiegészítését és a szerkesztőben megjelenő hibaüzeneteket.

Ezekkel és a Rust-ökoszisztéma többi eszközével a fejlesztők rendszerszintű
kód írása közben is hatékonyak lehetnek.

### Diákok {#students}

A Rust a diákoknak és mindazoknak szól, akiket érdekelnek a rendszerszintű
fogalmak. A Rust segítségével sokan tanultak meg például operációs rendszereket
fejleszteni. A közösség nagyon befogadó, és szívesen válaszol a diákok
kérdéseire. Az olyan kezdeményezésekkel, mint ez a könyv, a Rust csapatai
szeretnék minél több ember számára elérhetővé tenni a rendszerszintű
fogalmakat, különösen a programozással most ismerkedők számára.

### Cégek {#companies}

Kis- és nagyvállalatok százai használják a Rustot éles környezetben a
legkülönfélébb feladatokra, többek között parancssori eszközökhöz,
webszolgáltatásokhoz, DevOps-eszközökhöz, beágyazott eszközökhöz, hang- és
videóelemzéshez és -átkódoláshoz, kriptovalutákhoz, bioinformatikához,
keresőmotorokhoz, a dolgok internetét (IoT) kiszolgáló alkalmazásokhoz, gépi
tanuláshoz, sőt a Firefox webböngésző jelentős részeihez is.

### Nyílt forráskódú fejlesztők {#open-source-developers}

A Rust azoknak szól, akik szeretnének részt venni a Rust programozási nyelv, a
közösség, a fejlesztőeszközök és a könyvtárak építésében. Örülnénk, ha te is
hozzájárulnál a Rust nyelvhez!

### Akiknek fontos a sebesség és a stabilitás {#people-who-value-speed-and-stability}

A Rust azoknak szól, akik sebességet és stabilitást várnak el egy nyelvtől.
Sebességen egyrészt azt értjük, milyen gyorsan fut a Rust-kód, másrészt azt,
milyen gyorsan lehet Rustban programot írni. A Rust fordítójának ellenőrzései
új funkciók hozzáadásakor és refaktoráláskor is biztosítják a stabilitást. Ez
éles ellentétben áll az ilyen ellenőrzéseket nélkülöző nyelveken írt, törékeny
örökölt kóddal, amelyhez a fejlesztők sokszor hozzá sem mernek nyúlni. A
költségmentes absztrakciókra (zero-cost abstractions) – vagyis olyan magasabb
szintű nyelvi elemekre, amelyek ugyanolyan gyors alacsonyabb szintű kódra
fordulnak, mint a kézzel írt kód – törekedve a Rust arra igyekszik, hogy a
biztonságos kód egyben gyors kód is legyen.

A Rust nyelv sok más felhasználót is szeretne támogatni; az itt említettek
csupán a legnagyobb érintett csoportok. Összességében a Rust legnagyobb
ambíciója az, hogy megszüntesse azokat a kompromisszumokat, amelyeket a
programozók évtizedek óta elfogadnak: biztonságot _és_ hatékonyságot,
sebességet _és_ kényelmet kínál. Próbáld ki a Rustot, és nézd meg, beválnak-e
neked a döntései!

## Kinek szól ez a könyv? {#who-this-book-is-for}

A könyv feltételezi, hogy írtál már kódot valamilyen más programozási nyelven,
de azt nem, hogy melyiken. Igyekeztünk az anyagot a legkülönfélébb programozói
háttérrel rendelkezők számára is érthetővé tenni. Nem töltünk sok időt azzal,
hogy mi _is_ a programozás, vagy hogyan érdemes gondolkodni róla. Ha teljesen
új vagy a programozásban, jobban jársz, ha egy kifejezetten a programozás
alapjaiba bevezető könyvvel kezded.

## Hogyan használd ezt a könyvet? {#how-to-use-this-book}

A könyv általában azt feltételezi, hogy az elejétől a végéig, sorrendben
olvasod. A későbbi fejezetek a korábbiakban bemutatott fogalmakra építenek, a
korábbi fejezetek pedig olykor nem mennek bele egy-egy téma részleteibe, mert
egy későbbi fejezetben visszatérünk rájuk.

A könyvben kétféle fejezetet találsz: fogalmi és projektfejezeteket. A fogalmi
fejezetekben a Rust egy-egy aspektusával ismerkedsz meg. A projektfejezetekben
közösen kis programokat írunk, és alkalmazzuk mindazt, amit addig megtanultál.
A 2., a 12. és a 21. fejezet projektfejezet, a többi fogalmi fejezet.

Az **1. fejezet** bemutatja, hogyan telepítsd a Rustot, hogyan írj egy „Hello,
world!” programot, és hogyan használd a Cargót, a Rust csomagkezelőjét és
buildeszközét. A **2. fejezet** gyakorlati bevezetés a Rust-programok írásába:
egy számkitalálós játékot készítesz benne. Itt a fogalmakat csak nagy vonalakban
érintjük, a későbbi fejezetek részletesebben is kifejtik őket. Ha rögtön bele
szeretnél vágni a gyakorlatba, a 2. fejezet a neked való hely. Ha viszont
különösen alapos tanuló vagy, aki minden részletet meg szeretne érteni, mielőtt
továbblépne, érdemes lehet kihagynod a 2. fejezetet, és egyenesen a **3.
fejezettel** folytatnod, amely a Rust azon elemeit tárgyalja, amelyek más
programozási nyelvekben is megtalálhatók. Ezután visszatérhetsz a 2.
fejezethez, amikor szívesen dolgoznál egy projekten, és alkalmaznád a megismert
részleteket.

A **4. fejezetben** a Rust tulajdonjogi rendszerével ismerkedsz meg. Az **5.
fejezet** a struktúrákat és a metódusokat tárgyalja. A **6. fejezet** az
enumokról, a `match` kifejezésekről, valamint az `if let` és a `let...else`
vezérlési szerkezetekről szól. A struktúrák és az enumok segítségével saját
típusokat hozhatsz létre.

A **7. fejezetben** a Rust modulrendszerével, valamint a kód és annak
nyilvános alkalmazásprogramozási felülete (API) szervezését szolgáló
láthatósági szabályokkal ismerkedsz meg. A **8. fejezet** a standard könyvtár
néhány gyakran használt gyűjtemény-adatszerkezetét mutatja be: a vektorokat, a
sztringeket és a hasítótáblákat. A **9. fejezet** a Rust hibakezelési
filozófiáját és technikáit járja körül.

A **10. fejezet** a generikus típusokba, a traitekbe és az élettartamokba ás
bele; ezekkel olyan kódot definiálhatsz, amely több típusra is alkalmazható.
A **11. fejezet** teljes egészében a tesztelésről szól, amelyre a Rust
biztonsági garanciái mellett is szükség van ahhoz, hogy a program logikája
biztosan helyes legyen. A **12. fejezetben** saját megvalósítást készítünk a
`grep` parancssori eszköz funkcióinak egy részéből; ez az eszköz szöveget keres
fájlokban. Ehhez az előző fejezetekben tárgyalt fogalmak közül sokat
felhasználunk.

A **13. fejezet** a closure-öket és az iterátorokat mutatja be: a Rust azon
elemeit, amelyek a funkcionális programozási nyelvekből származnak. A **14.
fejezetben** alaposabban megvizsgáljuk a Cargót, és arról is szót ejtünk,
milyen bevált gyakorlatok segítenek a könyvtáraid megosztásában. A **15.
fejezet** a standard könyvtár okos mutatóit és a működésüket lehetővé tevő
traiteket tárgyalja.

A **16. fejezetben** végigvesszük a konkurens programozás különböző modelljeit,
és megmutatjuk, hogyan segít a Rust abban, hogy félelem nélkül programozz több
szálon. A **17. fejezet** erre épít: megismerkedünk a Rust async és await
szintaxisával, a taskokkal, a future-ökkel és a streamekkel, valamint az
általuk lehetővé tett pehelysúlyú konkurenciamodellel.

A **18. fejezet** azt vizsgálja, hogyan viszonyulnak a Rust idiómái a talán
már ismerős objektumorientált programozási elvekhez. A **19. fejezet** a
mintákról és a mintaillesztésről szóló referencia; ezek a Rust-programokban
mindenütt használt, hatékony kifejezőeszközök. A **20. fejezet** haladó témák
egész tárházát kínálja, többek között az unsafe Rustot, a makrókat, és további
tudnivalókat az élettartamokról, a traitekről, a típusokról, a függvényekről
és a closure-ökről.

A **21. fejezetben** egy olyan projektet valósítunk meg, amelyben egy alacsony
szintű, többszálú webszervert készítünk!

Végül néhány függelék hasznos tudnivalókat tartalmaz a nyelvről, inkább
referenciaszerű formában. Az **A. függelék** a Rust kulcsszavait, a **B.
függelék** a Rust operátorait és szimbólumait, a **C. függelék** a standard
könyvtár által biztosított, származtatható traiteket, a **D. függelék** néhány
hasznos fejlesztőeszközt mutat be, az **E. függelék** pedig a Rust kiadásait
magyarázza el. Az **F. függelékben** a könyv fordításait találod, a **G.
függelékben** pedig azt mutatjuk be, hogyan készül a Rust, és mi az a nightly
Rust.

Ezt a könyvet nem lehet rosszul olvasni: ha előre szeretnél ugrani, nyugodtan!
Lehet, hogy vissza kell majd lapoznod korábbi fejezetekhez, ha valami nem
világos. De csináld úgy, ahogy neked a legjobb.

<span id="ferris"></span>

A Rust tanulásának fontos része, hogy megtanuld olvasni a fordító
hibaüzeneteit: ezek elvezetnek a működő kódhoz. Ezért sok olyan példát
mutatunk, amely nem fordul le, a fordító által az adott helyzetben kiírt
hibaüzenettel együtt. Ne feledd: ha beírsz és futtatsz egy tetszőleges példát,
előfordulhat, hogy nem fordul le! Mindig olvasd el a körülötte lévő szöveget,
hogy kiderüljön, szándékosan hibás-e a futtatni kívánt példa. A legtöbb esetben
elvezetünk a nem forduló kód helyes változatához. Ferris is segít
megkülönböztetni azokat a kódokat, amelyeket nem működésre szántunk:

| Ferris                                                                                                               | Jelentés                                         |
| -------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| <img src="img/ferris/does_not_compile.svg" class="ferris-explain" alt="Ferris kérdőjellel"/>                         | Ez a kód nem fordul le!                          |
| <img src="img/ferris/panics.svg" class="ferris-explain" alt="Ferris kétségbeesetten széttárja az ollóit"/>                     | Ez a kód pánikol!                                |
| <img src="img/ferris/not_desired_behavior.svg" class="ferris-explain" alt="Ferris egyik ollóját felemelve vállat von"/> | Ez a kód nem a kívánt módon viselkedik.          |

A legtöbb esetben elvezetünk a nem forduló kód helyes változatához.

## Forráskód {#source-code}

A könyv forrásfájljai, amelyekből ez a könyv készül, megtalálhatók a
[GitHubon][book].

[book]: https://github.com/rust-lang/book/tree/main/src
