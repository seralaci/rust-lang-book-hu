## E. függelék: Kiadások {#appendix-e-editions}

Az 1. fejezetben láttad, hogy a `cargo new` egy kis metaadatot ad a
_Cargo.toml_ fájlodhoz a kiadásról. Ez a függelék elmagyarázza, mit jelent ez!

A Rust nyelv és fordító hathetes kiadási ciklusban fejlődik, vagyis a
felhasználók folyamatosan kapják az új funkciókat. Más programozási nyelvek
ritkábban adnak ki nagyobb változásokat; a Rust gyakrabban ad ki kisebb
frissítéseket. Egy idő után ezek az apró változások összeadódnak. Kiadásról
kiadásra azonban nehéz visszatekinteni, és azt mondani: „Hűha, a Rust 1.10 és
a Rust 1.31 között sokat változott a Rust!”

Nagyjából háromévente a Rust csapat kiad egy új Rust-_kiadást (edition)_. Minden
kiadás egy jól áttekinthető csomagba gyűjti az addig bekerült funkciókat,
teljesen frissített dokumentációval és eszközökkel. Az új kiadások a szokásos
hathetes kiadási folyamat részeként jelennek meg.

A kiadások különböző embereknek különböző célt szolgálnak:

- Az aktív Rust-felhasználóknak az új kiadás a fokozatos változásokat egy
  könnyen érthető csomagba gyűjti.
- Azoknak, akik még nem használják a Rustot, az új kiadás jelzi, hogy jelentős
  fejlesztések kerültek a nyelvbe, így talán érdemes újra ránézniük.
- A Rust fejlesztőinek az új kiadás közös célpontot ad az egész projekt
  számára.

E sorok írásakor négy Rust-kiadás érhető el: a Rust 2015, a Rust 2018, a Rust
2021 és a Rust 2024. Ez a könyv a Rust 2024-es kiadás idiómáit használja.

A _Cargo.toml_ `edition` kulcsa jelzi, melyik kiadást használja a fordító a
kódodhoz. Ha a kulcs nem létezik, a Rust a visszafelé kompatibilitás miatt a
`2015` értéket használja kiadásként.

Minden projekt választhat az alapértelmezett 2015-ös kiadástól eltérő kiadást.
A kiadások tartalmazhatnak inkompatibilis változásokat, például egy olyan új
kulcsszót, amely ütközik a kódban lévő azonosítókkal. Amíg azonban nem
választod ezeket a változásokat, a kódod továbbra is lefordul, még akkor is,
ha frissíted a használt Rust fordító verzióját.

Minden Rust fordítóverzió támogat minden olyan kiadást, amely a fordító
megjelenése előtt létezett, és bármely támogatott kiadású crate-eket képes
összekapcsolni. A kiadásváltozások csak azt befolyásolják, hogyan elemzi a
fordító kezdetben a kódot. Ezért ha a Rust 2015-öt használod, és az egyik
függőséged a Rust 2018-at, a projekted le fog fordulni, és használni tudja azt
a függőséget. A fordított helyzet is működik, amikor a projekted a Rust
2018-at, egy függőség pedig a Rust 2015-öt használja.

Hogy egyértelmű legyen: a legtöbb funkció minden kiadásban elérhető lesz.
Bármely Rust-kiadást használó fejlesztők továbbra is élvezhetik a
fejlesztéseket, ahogy az új stabil kiadások megjelennek. Bizonyos esetekben
azonban, főleg új kulcsszavak bevezetésekor, egyes új funkciók csak a későbbi
kiadásokban lehetnek elérhetők. Ha ilyen funkciókat szeretnél kihasználni,
kiadást kell váltanod.

További részletekért lásd a [_The Rust Edition Guide_][edition-guide] című
könyvet. Ez egy teljes könyv, amely felsorolja a kiadások közötti különbségeket,
és elmagyarázza, hogyan frissítheted automatikusan a kódodat egy új kiadásra a
`cargo fix` segítségével.

[edition-guide]: https://doc.rust-lang.org/stable/edition-guide
