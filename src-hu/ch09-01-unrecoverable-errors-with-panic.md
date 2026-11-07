## Helyrehozhatatlan hibák a `panic!` makróval {#unrecoverable-errors-with-panic}

Néha rossz dolgok történnek a kódodban, és semmit sem tehetsz ellenük. Ilyen
esetekre szolgál a Rustban a `panic!` makró. A gyakorlatban kétféleképpen
idézhetünk elő pánikot: olyan művelettel, amelytől a kódunk pánikol (például
egy tömb végén túli elem elérésével), vagy a `panic!` makró explicit
meghívásával. Mindkét esetben pánikot okozunk a programunkban. Alapértelmezés
szerint ezek a pánikok kiírnak egy hibaüzenetet, visszagöngyölítik és
kitakarítják a vermet, majd kilépnek. Egy környezeti változó segítségével azt
is elérheted, hogy a Rust pánik esetén kiírja a hívási vermet, így könnyebb
felderíteni a pánik forrását.

> ### A verem visszagöngyölítése vagy azonnali leállás pánik esetén {#unwinding-the-stack-or-aborting-in-response-to-a-panic}
>
> Alapértelmezés szerint pánik esetén a program megkezdi a verem
> _visszagöngyölítését (unwinding)_, ami azt jelenti, hogy a Rust visszafelé
> halad a veremben, és kitakarítja minden függvény adatait, amellyel
> találkozik. A visszafelé haladás és a takarítás azonban sok munka. Ezért a
> Rust lehetővé teszi, hogy helyette az azonnali _leállást (aborting)_ válaszd,
> amely takarítás nélkül fejezi be a programot.
>
> A program által használt memóriát ekkor az operációs rendszernek kell
> felszabadítania. Ha a projektedben a lehető legkisebb bináris állományra van
> szükséged, a pánik esetén történő visszagöngyölítésről azonnali leállásra
> válthatsz, ha a _Cargo.toml_ fájl megfelelő `[profile]` szakaszaihoz
> hozzáadod a `panic = 'abort'` sort. Ha például release módban szeretnél pánik
> esetén azonnal leállni, add hozzá ezt:
>
> ```toml
> [profile.release]
> panic = 'abort'
> ```

Próbáljuk ki a `panic!` hívását egy egyszerű programban:

<Listing file-name="src/main.rs">

```rust,should_panic,panics
{{#rustdoc_include ../listings/ch09-error-handling/no-listing-01-panic/src/main.rs}}
```

</Listing>

Amikor futtatod a programot, valami ilyesmit fogsz látni:

```console
{{#include ../listings/ch09-error-handling/no-listing-01-panic/output.txt}}
```

Az utolsó két sorban látható hibaüzenetet a `panic!` hívása okozza. Az első
sor a pánik üzenetét és a forráskód azon helyét mutatja, ahol a pánik történt:
a _src/main.rs:2:5_ azt jelzi, hogy a _src/main.rs_ fájlunk második sorának
ötödik karakteréről van szó.

Ebben az esetben a jelzett sor a saját kódunk része, és ha odamegyünk, a
`panic!` makró hívását látjuk. Más esetekben a `panic!` hívás olyan kódban is
lehet, amelyet a mi kódunk hív meg, és ilyenkor a hibaüzenetben szereplő
fájlnév és sorszám valaki más kódjára mutat, ahol a `panic!` makrót meghívták,
nem pedig a saját kódunk azon sorára, amely végül a `panic!` híváshoz vezetett.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-a-panic-backtrace"></a>

Annak a résznek a felderítéséhez, amely a problémát okozza, felhasználhatjuk
azoknak a függvényeknek a veremkiírását (backtrace), amelyekből a `panic!`
hívás érkezett. Hogy megértsük, hogyan használhatjuk a `panic!` veremkiírását,
nézzünk egy másik példát, és lássuk, milyen az, amikor a `panic!` hívás a
kódunk egy hibája miatt egy könyvtárból érkezik, nem pedig abból, hogy a
kódunk közvetlenül meghívja a makrót. A 9-1. kódrészletben olyan kód látható,
amely egy vektor érvényes indextartományán kívül eső indexet próbál elérni.

<Listing number="9-1" file-name="src/main.rs" caption="Kísérlet egy vektor végén túli elem elérésére, ami a `panic!` meghívásához vezet">

```rust,should_panic,panics
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-01/src/main.rs}}
```

</Listing>

Itt a vektorunk 100. elemét próbáljuk elérni (amely a 99-es indexen van, mert
az indexelés nullától kezdődik), de a vektornak csak három eleme van. Ilyen
helyzetben a Rust pánikol. A `[]` használatának egy elemet kellene
visszaadnia, de ha érvénytelen indexet adsz meg, nincs olyan elem, amelyet a
Rust helyesen visszaadhatna.

C-ben egy adatszerkezet végén túli olvasás kísérlete nem definiált viselkedés.
Megkaphatod azt, ami a memóriában azon a helyen található, amely az
adatszerkezet adott elemének felelne meg, még akkor is, ha az a memória nem az
adatszerkezethez tartozik. Ezt _puffertúlolvasásnak (buffer overread)_
nevezzük, és biztonsági résekhez vezethet, ha egy támadó úgy tudja
manipulálni az indexet, hogy olyan, az adatszerkezet után tárolt adatokat
olvasson ki, amelyekhez nem lenne szabad hozzáférnie.

Hogy megvédje a programodat az ilyen sebezhetőségektől, a Rust leállítja a
végrehajtást, és nem hajlandó folytatni, ha nem létező indexen lévő elemet
próbálsz olvasni. Próbáljuk ki:

```console
{{#include ../listings/ch09-error-handling/listing-09-01/output.txt}}
```

Ez a hiba a _main.rs_ 4. sorára mutat, ahol a `v` vektor 99-es indexét
próbáljuk elérni.

A `note:` sor azt mondja, hogy a `RUST_BACKTRACE` környezeti változó
beállításával veremkiírást kaphatunk arról, pontosan mi vezetett a hibához. A
_veremkiírás_ azoknak a függvényeknek a listája, amelyeket addig
meghívtak, amíg a program ehhez a ponthoz eljutott. A veremkiírások a Rustban
ugyanúgy működnek, mint más nyelvekben: az olvasásuk kulcsa, hogy felülről
kezdve addig olvasd, amíg olyan fájlokat nem látsz, amelyeket te írtál. Ott
keletkezett a probléma. Az e fölötti sorok olyan kódot mutatnak, amelyet a te
kódod hívott meg; az alatta lévők pedig olyan kódot, amely a te kódodat hívta.
Ezek az előtte és utána álló sorok tartalmazhatnak a Rust magjához tartozó
kódot, standard könyvtárbeli kódot vagy általad használt crate-eket. Próbáljunk
meg veremkiírást kapni úgy, hogy a `RUST_BACKTRACE` környezeti változót a `0`
kivételével bármilyen értékre beállítjuk. A 9-2. kódrészlet ahhoz hasonló
kimenetet mutat, amilyet látni fogsz.

<!-- manual-regeneration
cd listings/ch09-error-handling/listing-09-01
RUST_BACKTRACE=1 cargo run
copy the backtrace output below
check the backtrace number mentioned in the text below the listing
-->

<Listing number="9-2" caption="A `panic!` hívás által előállított veremkiírás, amely a `RUST_BACKTRACE` környezeti változó beállításakor jelenik meg">

```console
$ RUST_BACKTRACE=1 cargo run
thread 'main' panicked at src/main.rs:4:6:
index out of bounds: the len is 3 but the index is 99
stack backtrace:
   0: rust_begin_unwind
             at /rustc/4d91de4e48198da2e33413efdcd9cd2cc0c46688/library/std/src/panicking.rs:692:5
   1: core::panicking::panic_fmt
             at /rustc/4d91de4e48198da2e33413efdcd9cd2cc0c46688/library/core/src/panicking.rs:75:14
   2: core::panicking::panic_bounds_check
             at /rustc/4d91de4e48198da2e33413efdcd9cd2cc0c46688/library/core/src/panicking.rs:273:5
   3: <usize as core::slice::index::SliceIndex<[T]>>::index
             at file:///home/.rustup/toolchains/1.85/lib/rustlib/src/rust/library/core/src/slice/index.rs:274:10
   4: core::slice::index::<impl core::ops::index::Index<I> for [T]>::index
             at file:///home/.rustup/toolchains/1.85/lib/rustlib/src/rust/library/core/src/slice/index.rs:16:9
   5: <alloc::vec::Vec<T,A> as core::ops::index::Index<I>>::index
             at file:///home/.rustup/toolchains/1.85/lib/rustlib/src/rust/library/alloc/src/vec/mod.rs:3361:9
   6: panic::main
             at ./src/main.rs:4:6
   7: core::ops::function::FnOnce::call_once
             at file:///home/.rustup/toolchains/1.85/lib/rustlib/src/rust/library/core/src/ops/function.rs:250:5
note: Some details are omitted, run with `RUST_BACKTRACE=full` for a verbose backtrace.
```

</Listing>

Ez elég sok kimenet! A pontos kimenet az operációs rendszeredtől és a
Rust-verziótól függően eltérhet. Ahhoz, hogy ezekkel az információkkal együtt
kapj veremkiírást, a hibakeresési szimbólumoknak (debug symbols) engedélyezve
kell lenniük. A hibakeresési szimbólumok alapértelmezés szerint engedélyezve
vannak, ha a `cargo build` vagy a `cargo run` parancsot a `--release` kapcsoló
nélkül használod, ahogy mi is tettük.

A 9-2. kódrészlet kimenetében a veremkiírás 6. sora mutat a projektünk azon
sorára, amely a problémát okozza: a _src/main.rs_ 4. sorára. Ha nem szeretnénk,
hogy a programunk pánikoljon, a vizsgálódást annál a helynél érdemes kezdeni,
amelyre az első, általunk írt fájlt említő sor mutat. A 9-1. kódrészletben,
ahol szándékosan pánikoló kódot írtunk, a pánikot úgy javíthatjuk, hogy nem
kérünk a vektor indextartományán kívül eső elemet. Amikor a jövőben a kódod
pánikol, ki kell derítened, milyen műveletet végez a kód milyen értékekkel,
ami a pánikot okozza, és mit kellene helyette tennie.

Ennek a fejezetnek a későbbi, [„`panic!` vagy nem
`panic!`?”][to-panic-or-not-to-panic]<!-- ignore --> című szakaszában még
visszatérünk a `panic!` makróra, és arra, hogy mikor érdemes és mikor nem
érdemes a `panic!` makróval kezelni a hibahelyzeteket. Most pedig megnézzük,
hogyan hozhatunk helyre egy hibát a `Result` segítségével.

[to-panic-or-not-to-panic]: ch09-03-to-panic-or-not-to-panic.html#to-panic-or-not-to-panic
