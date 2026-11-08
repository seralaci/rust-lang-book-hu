# A magyar fordítás útmutatója

Ez a dokumentum a *The Rust Programming Language* magyar fordításának
szabályait, szójegyzékét és az upstream szinkron menetét rögzíti. Minden
fordítónak (embernek és MI-ügynöknek egyaránt) ezt kell követnie.

## Szerkezet

| Hely                           | Szerep                                                     |
| ------------------------------ | ---------------------------------------------------------- |
| `src/`                         | Az angol eredeti. **Soha nem módosítjuk.**                 |
| `src-hu/`                      | A magyar fordítás, fájlonként megfeleltetve a `src/`-nek.  |
| `listings/`                    | Kódpéldák. **Nem módosítjuk**, a kommentek angolok maradnak. |
| `hu/book.toml`                 | A magyar könyv build-konfigurációja.                       |
| `hu/UPSTREAM`                  | Az utolsó upstream commit, amelyhez a fordítás igazodik.   |
| `.github/workflows/hu-pages.yml` | Buildeli és GitHub Pagesre publikálja a magyar könyvet (https://seralaci.github.io/rust-lang-book-hu/). |
| `packages/mdbook-trpl`         | Előfeldolgozók; a feliratok (`Listing`, `Filename`, `Note:`) a `hu/book.toml`-ban konfigurálhatók. |

Build és előnézet a repó gyökeréből:

```console
$ mdbook build hu    # kimenet: hu/book/
$ mdbook serve hu    # élő előnézet a böngészőben
```

Ellenőrzés a build után (szerkezet az angolhoz képest, címsor-horgonyok,
sorhossz, belső linkek):

```console
$ python3 hu/ellenorzes.py            # minden lefordított fájl
$ python3 hu/ellenorzes.py ch06       # csak a 6. fejezet
```

Még le nem fordított fájlok angolul maradnak a `src-hu/`-ban, így a könyv a
fordítás bármely állapotában buildelhető.

## Alapelvek

1. **Bekezdésről bekezdésre fordítunk.** A magyar fájl szerkezete (címsorok,
   bekezdések, listák, kódblokkok, linkdefiníciók sorrendje) pontosan kövesse
   az angolt. Így az upstream változásai könnyen átvezethetők.
2. **Természetes magyar szöveg**, nem tükörfordítás. A mondatokat nyugodtan
   átszerkeszthetjük, de tartalmat nem hagyunk el és nem teszünk hozzá.
3. **Megszólítás: tegeződés.** Az olvasót tegezzük („telepítsd”, „láthatod”), a
   szerzők többes szám első személyben beszélnek („megnézzük”, „írunk”).
4. **Sortörés:** a bekezdéseket kb. 80 karakternél tördeljük, ahogy az eredeti.

## Mit fordítunk és mit nem

**Fordítjuk:**

- a prózát, a címsorokat, a táblázatok szövegét;
- a `<Listing>` elem `caption` attribútumát;
- a képek `alt` szövegét;
- a linkek *szövegét* (a `[szöveg][hivatkozás]` első felét);
- a `<span class="filename">Filename: …</span>` feliratot → `Fájlnév: …`.

**Nem fordítjuk:**

- kódot, kódkommentet, konzolkimenetet, fordítói hibaüzenetet (sem a
  `listings/`-ben, sem a markdownba ágyazott kódblokkokban);
- a `{{#include …}}`, `{{#rustdoc_include …}}` direktívákat;
- a linkdefiníciókat (`[ch20-macros]: ch20-05-macros.html`) és URL-eket –
  **egy kivétellel**: a `../std/…`, `../reference/…` stb. relatív linkek az
  angol könyvben a doc.rust-lang.org-on belül működnek, nálunk viszont nem,
  ezért ezeket `https://doc.rust-lang.org/std/…` alakra írjuk át;
- a `<!-- ignore -->` jelöléseket és a karbantartóknak szóló HTML-kommenteket
  (pl. `<!-- Old headings. Do not remove or links may break. -->`);
- a `<a id="…"></a>` horgonyokat;

A `<!-- ignore -->` jelölést **blokkidézetben (`> …`) soha ne törd két sorra**:
a sor eleji `> ` szétszakítja a HTML-kommentet, és elrontja a megjegyzésdobozt.

Tördeléskor ügyelj arra, hogy egy prózai sor **ne kezdődjön** `- `, `* `, `+ `,
`> ` vagy `1. ` alakkal (pl. „1. fejezet”): ezek bekezdés közepén is listát,
illetve blokkidézetet indítanak. Az ellenőrző szkript jelzi az ilyen eseteket.
- a `<Listing>` elem `number` és `file-name` attribútumát;
- a „Hello, world!” szöveget (az a kódkimenet része).

## Címsorok és horgonyok

A lefordított címsor megváltoztatná az automatikus horgonyt (`#troubleshooting`),
amire más fejezetek linkjei hivatkoznak. Ezért **minden lefordított címsor
végére odaírjuk az eredeti angol horgonyt**:

```markdown
### Hibaelhárítás {#troubleshooting}
```

A horgony az angol címsorból képzett azonosító: kisbetűs, a szóközök helyén
kötőjel, az írásjelek elhagyva (pl. `Installing rustup on Linux or macOS` →
`installing-rustup-on-linux-or-macos`, `Hello, Cargo!` → `hello-cargo`).

## Tipográfia

- Idézőjel: „…” (belső idézőjel: »…«). Az angol “…” helyett mindig „…”.
- Gondolatjel: szóközökkel körülvett nagykötőjel ( – ). Az angol szóköz nélküli
  „—” helyett ` – `.
- Felsorolás után, ha a tétel teljes mondat, pont; egyébként nincs írásjel,
  ahogy az eredetiben.
- Fejezetre hivatkozás: „Chapter 2” → „a 2. fejezet”; „Appendix D” →
  „a D. függelék”; „Listing 1-1” → „az 1-1. kódrészlet”. A névelőt a szám
  kiejtése szerint választjuk (*az* 1-1., *a* 2-3., *az* 5. fejezet).
- Megjegyzések: `> Note:` → `> Megjegyzés:` (az előfeldolgozó erre a
  kezdetre formázza a dobozt).
- Angol szakszó ragozása: kötőjellel, ha a kiejtés és az írás eltér, vagy a szó
  néma betűre végződik (`crate-et`, `trait-ek`), egyébként egybeírva
  (`Cargóval`, `rustupot`). A kódként írt szót mindig kötőjellel ragozzuk:
  `` `rustup`-ot ``, `` `main`-ben ``.

## Szakkifejezések kezelése

- Ahol van bevett magyar megfelelő, azt használjuk, és **az első
  előfordulásnál – fejezetenként – zárójelben megadjuk az angolt** is, dőlten:
  *tulajdonjog (ownership)*. Ezután csak a magyar alak szerepel.
- Ahol nincs bevett magyar szó (trait, crate, closure, future), az angol szó
  marad, magyar ragozással.
- Ha az eredeti dőlttel vezet be egy fogalmat (`_dependencies_`), a magyar
  változat is dőlt, és mögötte zárójelben az angol: _függőségek
  (dependencies)_.

## Szójegyzék

A táblázat a kötelező fordításokat tartalmazza. Új kifejezésnél előbb ide
vegyük fel, és csak utána használjuk.

### Általános és eszközök

| Angol                        | Magyar                                  | Megjegyzés |
| ---------------------------- | --------------------------------------- | ---------- |
| ahead-of-time compiled       | előre fordított                         | |
| API documentation            | API-dokumentáció                        | |
| argument                     | argumentum                              | |
| artifact (build output)      | termék, buildtermék                     | |
| benchmark                    | teljesítménymérés; ige: mér             | |
| binary (file)                | bináris (fájl)                          | |
| boilerplate                  | sablonkód (boilerplate)                 | |
| build (noun)                 | build                                   | pl. „debug build”, „release build” |
| build (verb)                 | lefordít, buildel                        | a „buildel” csak Cargo-kontextusban |
| build system                 | buildrendszer                           | |
| byte                         | bájt                                    | |
| cheat sheet                  | puska                                   | |
| cleanup                      | takarítás                               | |
| client / server              | kliens / szerver                        | |
| command line                 | parancssor                              | |
| compile                      | lefordít                                | |
| compiler                     | fordító, fordítóprogram                 | |
| compiler-driven development  | fordítóvezérelt fejlesztés              | |
| configuration                | konfiguráció                            | |
| connection                   | kapcsolat                               | |
| constructor                  | konstruktor                             | |
| deadlock                     | holtpont                                | |
| denial-of-service (DoS)      | szolgáltatásmegtagadásos (DoS) támadás  | |
| dependency                   | függőség                                | |
| deprecate                    | elavulttá nyilvánít                     | |
| design pattern               | tervezési minta                         | |
| directory                    | mappa                                   | **nem** „könyvtár” (az a library) |
| doc tests                    | dokumentációs tesztek (doc tests)       | |
| documentation comment        | dokumentációs komment                   | |
| edition                      | kiadás (edition)                        | a Rust-kiadásokra, pl. „2024-es kiadás” |
| environment variable         | környezeti változó                      | |
| executable                   | futtatható állomány                     | |
| exit code / exit status      | kilépési kód                            | |
| feature (language)           | nyelvi elem, funkció                    | |
| feature flag / unstable feature | funkciókapcsoló / instabil funkció      | |
| figure / table (numbered)    | ábra / táblázat                         | „a 4-1. ábrán”, „a 3-1. táblázat” |
| graceful shutdown            | szabályos leállítás                     | |
| handle                       | leíró (handle)                          | |
| hardcoded                    | beégetett                               | |
| IDE                          | IDE (integrált fejlesztőkörnyezet)      | |
| idiomatic                    | idiomatikus                             | |
| interface                    | interfész                               | |
| iteration                    | iteráció                                | |
| job / queue                  | feladat / várakozási sor                | |
| library                      | könyvtár                                | |
| linker                       | linker                                  | első előfordulásnál „összeszerkesztő” magyarázattal |
| linter                       | linter (kódelemző)                      | |
| listing                      | kódrészlet                              | |
| memory leak                  | memóriaszivárgás                        | |
| metadata                     | metaadatok                              | |
| mock object / test double    | mock objektum / tesztdublőr             | |
| nightly                      | nightly                                 | |
| package                      | csomag                                  | |
| package manager              | csomagkezelő                            | |
| parser                       | elemző (parser)                         | |
| patch release                | javítókiadás (patch release)            | |
| placeholder                  | helyőrző (placeholder)                  | |
| prelude                      | prelude                                 | nem fordítjuk |
| process (OS)                 | folyamat                                | |
| production                   | éles környezet                          | |
| publish                      | közzétesz, közzététel                   | |
| random number generator      | véletlenszám-generátor                  | |
| refactoring                  | refaktorálás                            | |
| registry                     | regiszter (registry)                    | pl. a Crates.io |
| regression                   | regresszió                              | |
| release (Cargo profile)      | release                                 | pl. „release build” |
| release (noun, version)      | kiadás, verzió                          | |
| release channel              | kiadási csatorna                        | |
| release profile              | release profil                          | |
| reproducible build           | reprodukálható build                    | |
| request / response           | kérés / válasz                          | |
| Rustacean                    | rustacean                               | többes szám: rustaceanek |
| Semantic Versioning          | szemantikus verziókezelés (Semantic Versioning) | |
| separation of concerns       | a felelősségi körök szétválasztása      | |
| shell                        | parancsértelmező, shell                 | |
| side effect                  | mellékhatás                             | |
| source file                  | forrásfájl                              | |
| standard library             | standard könyvtár                       | |
| standard output / standard error | standard kimenet / standard hibakimenet | **nem** „szabványos” |
| stream (I/O)                 | adatfolyam                              | az async streamekre lásd lent |
| subcommand                   | alparancs                               | |
| syntax sugar                 | szintaktikai cukor (syntax sugar)       | |
| systems programming          | rendszerprogramozás                     | |
| terminal                     | terminál                                | |
| test-driven development (TDD) | tesztvezérelt fejlesztés                | |
| thread pool                  | szálkészlet                             | |
| throughput                   | áteresztőképesség                       | |
| toolchain                    | eszközlánc (toolchain)                  | |
| web server                   | webszerver                              | |
| workflow                     | munkafolyamat                           | |
| workspace                    | munkaterület; Cargo-munkaterület        | |
| wrapper                      | burkoló (wrapper)                       | |
| yank                         | visszavonás (yank)                      | |
| zero-cost abstraction        | költségmentes absztrakció               | |

### A nyelv fogalmai

| Angol                        | Magyar                                  | Megjegyzés |
| ---------------------------- | --------------------------------------- | ---------- |
| `@` binding                  | `@`-kötés                               | |
| ABI                          | bináris alkalmazásinterfész (ABI)       | |
| abort (on panic)             | azonnali leállás (abort)                | |
| alias                        | álnév                                   | |
| allocate / allocator         | lefoglal, foglalás / memóriafoglaló     | |
| `Arc<T>` / atomic reference counting | atomi referenciaszámlálás               | |
| arm (`match`, `if`)          | ág                                      | |
| array                        | tömb                                    | |
| assertion / assert           | állítás (assertion) / ellenőriz         | |
| associated function          | társított függvény                      | |
| associated type              | társított típus                         | |
| async runtime / executor     | aszinkron futtatókörnyezet / végrehajtó | |
| attribute / annotation       | attribútum / annotáció                  | |
| backtrace                    | veremkiírás (backtrace)                 | |
| binary crate / library crate | bináris crate / könyvtár crate          | |
| binding / bind               | kötés / köt                             | |
| blanket implementation       | átfogó megvalósítás (blanket implementation) | |
| Boolean                      | logikai (érték, típus)                  | |
| borrow / borrowing           | kölcsönöz / kölcsönzés                  | |
| borrow checker               | kölcsönzésellenőrző (borrow checker)    | |
| box (`Box<T>`)               | box                                     | ragozva: boxot, boxban |
| call stack                   | hívási verem                            | |
| capture (closure)            | elkap                                   | **nem** „megragad” |
| catch-all pattern            | mindent elfogó minta                    | |
| channel / transmitter / receiver | csatorna / küldő / fogadó               | |
| clone                        | klónozás                                | a `clone` metódusnév marad |
| closure                      | closure                                 | |
| coherence / orphan rule      | koherencia / árvaszabály                | |
| collection                   | gyűjtemény                              | |
| comment                      | komment                                 | |
| concatenation                | összefűzés                              | |
| concurrency                  | konkurencia, konkurens programozás      | **nem** párhuzamosság |
| cons list                    | cons lista                              | |
| constant                     | konstans                                | |
| control flow                 | vezérlési szerkezetek                   | |
| cooperative multitasking     | kooperatív többfeladatos működés        | |
| crate                        | crate                                   | ragozva: crate-et, crate-ek |
| crate root                   | crate-gyökér                            | |
| dangling reference / pointer | lógó referencia / mutató                | |
| data race / race condition   | adatverseny / versenyhelyzet            | |
| data type                    | adattípus                               | |
| declarative / procedural macro | deklaratív / procedurális makró         | |
| default implementation       | alapértelmezett megvalósítás            | |
| deref coercion               | deref-konverzió                         | |
| dereferencing                | dereferálás                             | |
| derive / derived trait       | származtat / származtatott trait        | |
| derive macro / attribute-like / function-like | `derive` makró / attribútumszerű / függvényszerű makró | |
| destructuring                | szétbontás                              | |
| double free                  | kétszeres felszabadítás                 | |
| drop                         | eldob, eldobás (drop)                   | a memória visszaadására: felszabadít |
| dyn compatibility            | dyn-kompatibilitás                      | |
| dynamic / static dispatch    | dinamikus / statikus hívásfeloldás      | |
| dynamically sized type (DST) | dinamikus méretű típus                  | |
| encapsulation                | egységbezárás                           | |
| entry (hash map)             | bejegyzés (entry)                       | |
| enum                         | enum (felsorolás típus)                 | |
| error kind                   | hibafajta                               | |
| exhaustive                   | kimerítő                                | |
| expression                   | kifejezés                               | |
| FFI                          | idegenfüggvény-interfész (FFI)          | |
| field                        | mező                                    | |
| field init shorthand         | rövidített mezőinicializálás (field init shorthand) | |
| floating-point number        | lebegőpontos szám                       | |
| fully qualified syntax       | teljesen minősített szintaxis           | |
| function                     | függvény                                | |
| function pointer             | függvénymutató                          | |
| future                       | future                                  | |
| garbage collector            | szemétgyűjtő                            | |
| generic                      | generikus                               | |
| generics                     | generikus típusok                       | |
| glob operator                | glob operátor                           | |
| grapheme cluster             | graféma-klaszter                        | |
| hash map                     | hasítótábla (hash map)                  | |
| hashing function / hasher    | hasítófüggvény / hasító (hasher)        | |
| heap                         | kupac (heap)                            | |
| immutable                    | nem módosítható (immutable)             | |
| `impl` block                 | `impl` blokk                            | |
| implement / implementation   | megvalósít / megvalósítás               | **nem** „implementál” |
| indexing                     | indexelés                               | |
| indirection                  | indirekció (indirection)                | |
| inheritance                  | öröklődés                               | |
| instance / instantiate       | példány / példányosít                   | |
| integer                      | egész szám                              | |
| integer overflow             | egészszám-túlcsordulás                  | |
| interior mutability          | belső módosíthatóság                    | |
| item (module)                | elem                                    | |
| iterator                     | iterátor                                | |
| iterator adapter / consuming adapter | iterátoradapter / fogyasztó adapter     | |
| join (thread)                | bevár; `JoinHandle` → join-leíró        | |
| key / value                  | kulcs / érték                           | |
| keyword                      | kulcsszó                                | |
| lazy                         | lusta                                   | |
| lifetime                     | élettartam                              | |
| lifetime annotation / parameter | élettartam-annotáció / élettartam-paraméter | |
| lifetime elision             | élettartam-elhagyás                     | |
| literal / string literal     | literál / sztringliterál                | |
| lock / mutex                 | zár, zárol / mutex                      | |
| loop / loop label            | ciklus / cikluscímke                    | |
| macro                        | makró                                   | |
| marker trait                 | jelölő trait                            | |
| match arm                    | match ág                                | |
| match guard                  | őrfeltétel (match guard)                | |
| message passing / shared state | üzenetküldés / megosztott állapot       | |
| metaprogramming              | metaprogramozás                         | |
| method                       | metódus                                 | |
| module                       | modul                                   | |
| module tree / module system  | modulfa / modulrendszer                 | |
| monomorphization             | monomorfizáció                          | |
| move (ownership)             | mozgatás; ige: mozgat, kimozgat         | **nem** „áthelyez” (az a kód áthelyezésére marad) |
| mutability                   | módosíthatóság                          | |
| mutable                      | módosítható (mutable)                   | |
| never type                   | never típus                             | |
| newtype pattern              | newtype minta                           | |
| object-oriented              | objektumorientált                       | |
| operator overloading         | operátor-túlterhelés                    | |
| owned (type)                 | saját tulajdonú (owned)                 | |
| owner / ownership            | tulajdonos / tulajdonjog (ownership)    | |
| panic                        | pánik; ige: pánikol                     | |
| parallelism                  | párhuzamosság                           | |
| parameter                    | paraméter                               | |
| parent / child / sibling module | szülő- / gyermek- / testvérmodul        | |
| path                         | útvonal                                 | abszolút / relatív útvonal |
| pattern / pattern matching   | minta / mintaillesztés                  | |
| pinning / `Pin`              | rögzítés / `Pin`                        | |
| pointer                      | mutató                                  | |
| polling                      | lekérdezés                              | |
| polymorphism                 | polimorfizmus                           | |
| propagating errors           | hibák továbbadása                       | |
| public / private / privacy   | nyilvános / privát / láthatóság         | |
| range / range expression     | tartomány / tartománykifejezés          | |
| raw identifier / reserved keyword | nyers azonosító / fenntartott kulcsszó  | |
| raw pointer                  | nyers mutató                            | |
| re-exporting                 | újraexportálás                          | |
| receiver                     | fogadó (receiver)                       | |
| recoverable / unrecoverable error | helyrehozható / helyrehozhatatlan hiba  | |
| recursive type               | rekurzív típus                          | |
| reference                    | referencia                              | |
| reference counting / reference cycle | referenciaszámlálás / referenciaciklus  | |
| refutable / irrefutable      | cáfolható / cáfolhatatlan               | |
| scalar / compound type       | skalár / összetett típus                | |
| scope                        | hatókör                                 | |
| self-referential             | önhivatkozó                             | |
| shadowing                    | árnyékolás (shadowing)                  | |
| shallow / deep copy          | sekély / mély másolás                   | |
| signature                    | szignatúra                              | |
| signed / unsigned            | előjeles / előjel nélküli               | |
| slice                        | szelet (slice)                          | |
| smart pointer                | okos mutató (smart pointer)             | |
| spawn (thread, task)         | elindít, létrehoz                       | |
| stack                        | verem (stack)                           | |
| starvation                   | kiéheztetés                             | |
| state machine                | állapotgép                              | |
| state pattern                | állapot minta                           | |
| statement                    | utasítás                                | |
| static lifetime              | statikus élettartam                     | |
| statically typed             | statikusan típusos                      | |
| stream (async)               | stream                                  | ragozva: streamek |
| string                       | sztring                                 | |
| string slice                 | sztringszelet                           | |
| struct                       | struktúra (struct)                      | |
| struct update syntax         | struktúrafrissítő szintaxis (struct update syntax) | |
| submodule                    | almodul                                 | |
| supertrait                   | szupertrait                             | |
| task (async)                 | task                                    | ragozva: taskot, taskok |
| test function / module / suite | tesztfüggvény / tesztmodul / tesztkészlet | |
| test runner / test harness   | tesztfuttató / tesztkörnyezet           | |
| thread                       | szál                                    | |
| thread-safe                  | szálbiztos                              | |
| timeout                      | időkorlát                               | |
| trait                        | trait                                   | ragozva: traitet, traitek |
| trait bound                  | trait-korlát                            | ragozva: trait-korlátot |
| trait object                 | trait objektum                          | |
| tuple                        | tuple                                   | |
| tuple struct                 | tuple struktúra (tuple struct)          | |
| type alias                   | típusálnév                              | |
| type annotation              | típusannotáció                          | |
| type inference               | típuskövetkeztetés (type inference)     | |
| type parameter               | típusparaméter                          | |
| undefined behavior           | nem definiált viselkedés                | |
| Unicode scalar value         | Unicode skalárérték                     | |
| unit test / integration test | egységteszt / integrációs teszt         | |
| unit type / unit-like struct | unit típus / unit-szerű struktúra       | |
| unsafe                       | unsafe (nem biztonságos)                | |
| unwinding                    | visszagöngyölítés (unwinding)           | |
| variable                     | változó                                 | |
| variant (enum)               | változat (variant)                      | |
| vector                       | vektor                                  | |
| weak / strong reference      | gyenge / erős referencia                | |
| `where` clause               | `where` záradék                         | |
| wildcard                     | helyettesítő jel (wildcard)             | |
| yield control                | a vezérlés átadása                      | |

### Fejezetcímek és állandó kifejezések

| Angol                        | Magyar                                  |
| ---------------------------- | --------------------------------------- |
| The Rust Programming Language | A Rust programozási nyelv              |
| Foreword                     | Előszó                                  |
| Introduction                 | Bevezetés                               |
| Summary                      | Összefoglalás                           |
| Appendix                     | Függelék                                |
| Note:                        | Megjegyzés:                             |
| Filename:                    | Fájlnév:                                |

## Upstream szinkron

A fordítás az angol eredeti egy adott commitjához igazodik; ezt a `hu/UPSTREAM`
fájl tárolja. Frissítéskor:

Egyszeri beállítás klónozás után (a `.gitattributes` szerint a `README.md`
merge-nél mindig a magyar változat marad, ehhez kell ez a driver):

```console
$ git config merge.ours.driver true
```

```console
$ git fetch upstream
$ git merge upstream/main          # a src/ konfliktus nélkül frissül
$ git diff $(cat hu/UPSTREAM) HEAD -- src/   # mi változott angolul?
```

1. A diff alapján vezessük át a változásokat a `src-hu/` megfelelő fájljaiba
   (új fájlt az angolból másoljunk át, majd fordítsunk le).
2. Ha a `SUMMARY.md` változott, a `src-hu/SUMMARY.md`-t is igazítsuk.
3. Írjuk a `hu/UPSTREAM` fájlba a merge-ölt upstream commit hash-ét.
4. `mdbook build hu` – ellenőrizzük, hogy hiba nélkül fut.
