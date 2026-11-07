# Gyakori gyűjtemények {#common-collections}

A Rust standard könyvtára számos nagyon hasznos adatszerkezetet tartalmaz,
amelyeket _gyűjteményeknek (collections)_ nevezünk. A legtöbb más adattípus egy
konkrét értéket képvisel, a gyűjtemények viszont több értéket is
tartalmazhatnak. A beépített tömb és tuple típustól eltérően azokat az adatokat,
amelyekre ezek a gyűjtemények mutatnak, a kupacon tároljuk, így az adatok
mennyiségét nem kell fordítási időben ismerni, és az a program futása közben
nőhet vagy csökkenhet. Minden gyűjteményfajtának mások a képességei és a
költségei, és az, hogy az adott helyzethez megfelelőt válassz, olyan készség,
amely idővel fejlődik ki. Ebben a fejezetben három gyűjteményt tárgyalunk,
amelyeket nagyon gyakran használnak a Rust-programok:

- A _vektor (vector)_ lehetővé teszi, hogy változó számú értéket tárolj
  egymás mellett.
- A _sztring (string)_ karakterek gyűjteménye. A `String` típust korábban már
  említettük, de ebben a fejezetben részletesen is foglalkozunk vele.
- A _hasítótábla (hash map)_ lehetővé teszi, hogy egy értéket egy adott
  kulcshoz rendelj. Ez az általánosabb, _leképezésnek (map)_ nevezett
  adatszerkezet egy konkrét megvalósítása.

A standard könyvtár által biztosított többi gyűjteményfajtáról
[a dokumentációban][collections] olvashatsz.

Megnézzük, hogyan hozhatunk létre és frissíthetünk vektorokat, sztringeket és
hasítótáblákat, valamint azt is, mitől különleges mindegyik.

[collections]: ../std/collections/index.html
