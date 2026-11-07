## A. függelék: Kulcsszavak {#appendix-a-keywords}

Az alábbi listák a Rust nyelv által jelenlegi vagy jövőbeli használatra
fenntartott kulcsszavakat tartalmazzák. Emiatt ezek nem használhatók
azonosítóként (kivéve nyers azonosítóként, ahogy azt a [„Nyers
azonosítók”][raw-identifiers]<!-- ignore --> szakaszban tárgyaljuk). Az
_azonosítók (identifiers)_ a függvények, változók, paraméterek, struktúramezők,
modulok, crate-ek, konstansok, makrók, statikus értékek, attribútumok, típusok,
traitek és élettartamok nevei.

[raw-identifiers]: #raw-identifiers

### Jelenleg használt kulcsszavak {#keywords-currently-in-use}

Az alábbi lista a jelenleg használt kulcsszavakat és azok szerepét mutatja be.

- **`as`**: primitív típuskonverzió, egy elemet tartalmazó konkrét trait
  egyértelműsítése, vagy elemek átnevezése `use` utasításokban.
- **`async`**: `Future` visszaadása az aktuális szál blokkolása helyett.
- **`await`**: a végrehajtás felfüggesztése, amíg egy `Future` eredménye el nem
  készül.
- **`break`**: azonnali kilépés egy ciklusból.
- **`const`**: konstans elemek vagy konstans nyers mutatók definiálása.
- **`continue`**: továbblépés a ciklus következő iterációjára.
- **`crate`**: modulútvonalban a crate-gyökérre hivatkozik.
- **`dyn`**: dinamikus hívásfeloldás (dynamic dispatch) egy trait objektumon
  keresztül.
- **`else`**: az `if` és `if let` vezérlési szerkezetek alternatív ága.
- **`enum`**: felsorolás definiálása.
- **`extern`**: külső függvény vagy változó csatolása.
- **`false`**: a logikai hamis literál.
- **`fn`**: függvény vagy függvénymutató-típus definiálása.
- **`for`**: iteráció egy iterátor elemein, trait megvalósítása, vagy magasabb
  rendű élettartam megadása.
- **`if`**: elágazás egy feltételes kifejezés eredménye alapján.
- **`impl`**: saját (inherent) vagy trait-funkcionalitás megvalósítása.
- **`in`**: a `for` ciklus szintaxisának része.
- **`let`**: változó kötése.
- **`loop`**: feltétel nélküli ciklus.
- **`match`**: egy érték illesztése mintákra.
- **`mod`**: modul definiálása.
- **`move`**: a closure az összes elfogott értékét a tulajdonába veszi.
- **`mut`**: módosíthatóság jelölése referenciákban, nyers mutatókban vagy
  mintabeli kötésekben.
- **`pub`**: nyilvános láthatóság jelölése struktúramezőkön, `impl` blokkokon
  vagy modulokon.
- **`ref`**: kötés referencia szerint.
- **`return`**: visszatérés a függvényből.
- **`Self`**: típusálnév arra a típusra, amelyet éppen definiálunk vagy
  megvalósítunk.
- **`self`**: a metódus alanya vagy az aktuális modul.
- **`static`**: globális változó, vagy a program teljes futása alatt érvényes
  élettartam.
- **`struct`**: struktúra definiálása.
- **`super`**: az aktuális modul szülőmodulja.
- **`trait`**: trait definiálása.
- **`true`**: a logikai igaz literál.
- **`type`**: típusálnév vagy társított típus definiálása.
- **`union`**: [union][union]<!-- ignore --> definiálása; csak union
  deklarációban használva kulcsszó.
- **`unsafe`**: nem biztonságos kód, függvények, traitek vagy megvalósítások
  jelölése.
- **`use`**: szimbólumok hatókörbe hozása.
- **`where`**: egy típust korlátozó záradékok jelölése.
- **`while`**: feltételes ciklus egy kifejezés eredménye alapján.

[union]: ../reference/items/unions.html

### Jövőbeli használatra fenntartott kulcsszavak {#keywords-reserved-for-future-use}

Az alábbi kulcsszavaknak még nincs semmilyen funkciójuk, de a Rust fenntartja
őket egy esetleges jövőbeli használatra:

- `abstract`
- `become`
- `box`
- `do`
- `final`
- `gen`
- `macro`
- `override`
- `priv`
- `try`
- `typeof`
- `unsized`
- `virtual`
- `yield`

### Nyers azonosítók {#raw-identifiers}

A _nyers azonosítók (raw identifiers)_ olyan szintaxist jelentenek, amellyel
kulcsszavakat használhatsz ott, ahol ez egyébként nem megengedett. Nyers
azonosítót úgy használhatsz, hogy a kulcsszó elé az `r#` előtagot írod.

Például a `match` kulcsszó. Ha megpróbálod lefordítani az alábbi függvényt,
amelynek a neve `match`:

<span class="filename">Fájlnév: src/main.rs</span>

```rust,ignore,does_not_compile
fn match(needle: &str, haystack: &str) -> bool {
    haystack.contains(needle)
}
```

ezt a hibát kapod:

```text
error: expected identifier, found keyword `match`
 --> src/main.rs:4:4
  |
4 | fn match(needle: &str, haystack: &str) -> bool {
  |    ^^^^^ expected identifier, found keyword
```

A hiba azt mutatja, hogy a `match` kulcsszót nem használhatod a függvény
azonosítójaként. Ahhoz, hogy a `match` függvénynévként szerepelhessen, a nyers
azonosító szintaxisát kell használnod, így:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
fn r#match(needle: &str, haystack: &str) -> bool {
    haystack.contains(needle)
}

fn main() {
    assert!(r#match("foo", "foobar"));
}
```

Ez a kód hiba nélkül lefordul. Figyeld meg az `r#` előtagot a függvény nevén,
mind a definíciójában, mind ott, ahol a `main`-ben meghívjuk.

A nyers azonosítókkal bármilyen szót választhatsz azonosítónak, még akkor is,
ha az a szó éppen fenntartott kulcsszó. Így szabadabban választhatunk
azonosítóneveket, és olyan nyelveken írt programokkal is együtt tudunk
működni, amelyekben ezek a szavak nem kulcsszavak. Emellett a nyers
azonosítókkal olyan könyvtárakat is használhatsz, amelyek más Rust-kiadásban
(edition) készültek, mint a te crate-ed. Például a `try` a 2015-ös kiadásban
nem kulcsszó, a 2018-as, a 2021-es és a 2024-es kiadásban viszont igen. Ha
olyan könyvtártól függsz, amely a 2015-ös kiadással készült, és van egy `try`
függvénye, akkor a későbbi kiadásokban a nyers azonosító szintaxisát – ebben
az esetben az `r#try` alakot – kell használnod, hogy meghívhasd ezt a
függvényt a kódodból. A kiadásokról az [E.
függelékben][appendix-e]<!-- ignore --> olvashatsz bővebben.

[appendix-e]: appendix-05-editions.html
