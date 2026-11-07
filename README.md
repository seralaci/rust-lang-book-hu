# A Rust programozási nyelv – magyar fordítás

[![Magyar könyv publikálása](https://github.com/seralaci/rust-lang-book-hu/actions/workflows/hu-pages.yml/badge.svg)](https://github.com/seralaci/rust-lang-book-hu/actions/workflows/hu-pages.yml)

Ez a repó a [*The Rust Programming Language*][original] (közismert nevén „a
Rust könyv”) magyar fordítását tartalmazza. A [rust-lang/book][upstream] repó
forkja; az angol eredetit folyamatosan követjük.

**📖 A könyv online olvasható: <https://seralaci.github.io/rust-lang-book-hu/>**

[original]: https://doc.rust-lang.org/stable/book/
[upstream]: https://github.com/rust-lang/book

## Állapot

A könyv teljes szövege le van fordítva: a címoldal, az előszó, a bevezetés,
mind a 21 fejezet és az A–G. függelék. A fordítás lektorálása folyamatban van –
ha hibát, pontatlanságot vagy döcögős mondatot találsz, kérjük, jelezd!

| Rész                                         | Állapot                   |
| -------------------------------------------- | ------------------------- |
| Címoldal, előszó, bevezetés, tartalomjegyzék | ✅ lefordítva             |
| 1–21. fejezet                                | ✅ lefordítva             |
| Függelékek (A–G)                             | ✅ lefordítva             |
| Lektorálás                                   | ⏳ folyamatban            |
| Kódpéldák kommentjei (`listings/`)           | 🇬🇧 egyelőre angolul      |

A fordítás a Rust 1.99.1-es verziójához és a 2024-es kiadáshoz (edition)
készült könyvváltozatot követi; a pontos upstream commitot a
[`hu/UPSTREAM`](hu/UPSTREAM) fájl rögzíti.

## A repó felépítése

| Hely                    | Tartalom                                                         |
| ----------------------- | ---------------------------------------------------------------- |
| `src-hu/`               | A magyar fordítás (Markdown).                                    |
| `hu/`                   | A magyar könyv build-konfigurációja és az ellenőrző szkript.     |
| `FORDITAS.md`           | Fordítási útmutató, stílusszabályok és szójegyzék.               |
| `src/`, `listings/`     | Az angol eredeti és a kódpéldák – ezeket nem módosítjuk.         |

Az angol forrás érintetlenül marad, így az upstream változásai konfliktus
nélkül behúzhatók, és pontosan látszik, mit kell a fordításban frissíteni.

## Buildelés

Szükséges hozzá a [Rust] és az [mdBook] (a CI-val azonos 0.5.1-es verzió):

```console
$ cargo install mdbook --locked --version 0.5.1
```

A repó gyökeréből:

```console
$ mdbook serve hu --open    # élő előnézet: http://localhost:3000
$ mdbook build hu           # statikus build: hu/book/
$ python3 hu/ellenorzes.py  # a fordítás ellenőrzése (build után)
```

A `main` ágra pusholt változásokat a [`hu-pages.yml`](.github/workflows/hu-pages.yml)
GitHub Actions workflow automatikusan buildeli és publikálja GitHub Pagesre.

[Rust]: https://www.rust-lang.org/tools/install
[mdBook]: https://github.com/rust-lang/mdBook

## Közreműködés

Örülünk minden segítségnek – új fejezet fordításának, javításnak, lektorálásnak!
Mielőtt nekikezdesz, olvasd el a [fordítási útmutatót](FORDITAS.md): ebben
vannak a stílusszabályok, a kötelező szakszavak szójegyzéke és az upstream
szinkron menete.

- Hibát találtál a fordításban? Nyiss egy [issue-t][issues], vagy küldj pull
  requestet.
- Az angol eredeti tartalmi hibáit az [eredeti repóban][upstream] jelezd.

[issues]: https://github.com/seralaci/rust-lang-book-hu/issues

## Licenc

Az eredeti könyvhöz hasonlóan a fordítás is az MIT és az Apache 2.0 licenc
alatt érhető el, választásod szerint. Részletek: [LICENSE-MIT](LICENSE-MIT),
[LICENSE-APACHE](LICENSE-APACHE), [COPYRIGHT](COPYRIGHT).

Az eredeti könyv szerzői Steve Klabnik, Carol Nichols és Chris Krycho, a Rust
közösség közreműködésével. A könyv nyomtatott változata a [No Starch
Press][nostarch] kiadásában jelent meg.

[nostarch]: https://nostarch.com/rust-programming-language-3rd-edition
