## B. függelék: Operátorok és szimbólumok {#appendix-b-operators-and-symbols}

Ez a függelék a Rust szintaxisának szójegyzékét tartalmazza, beleértve az
operátorokat és más szimbólumokat, amelyek önmagukban, illetve útvonalak,
generikus típusok, trait-korlátok, makrók, attribútumok, kommentek, tuple-ök
és zárójelek környezetében fordulnak elő.

### Operátorok {#operators}

A B-1. táblázat a Rust operátorait tartalmazza: mindegyikhez egy példát arra,
hogyan jelenik meg az operátor a kódban, egy rövid magyarázatot, valamint azt,
hogy az operátor túlterhelhető-e. Ha egy operátor túlterhelhető, a táblázat
azt a traitet is megadja, amellyel a túlterhelés megvalósítható.

<span class="caption">B-1. táblázat: Operátorok</span>

| Operátor                  | Példa                                                   | Magyarázat                                                            | Túlterhelhető? |
| ------------------------- | ------------------------------------------------------- | --------------------------------------------------------------------- | -------------- |
| `!`                       | `ident!(...)`, `ident!{...}`, `ident![...]`             | Makrókifejtés                                                         |                |
| `!`                       | `!expr`                                                 | Bitenkénti vagy logikai tagadás (komplemens)                          | `Not`          |
| `!=`                      | `expr != expr`                                          | Egyenlőtlenség vizsgálata                                             | `PartialEq`    |
| `%`                       | `expr % expr`                                           | Aritmetikai maradék                                                   | `Rem`          |
| `%=`                      | `var %= expr`                                           | Aritmetikai maradék és értékadás                                      | `RemAssign`    |
| `&`                       | `&expr`, `&mut expr`                                    | Kölcsönzés                                                            |                |
| `&`                       | `&type`, `&mut type`, `&'a type`, `&'a mut type`        | Kölcsönzött mutatótípus                                               |                |
| `&`                       | `expr & expr`                                           | Bitenkénti ÉS                                                         | `BitAnd`       |
| `&=`                      | `var &= expr`                                           | Bitenkénti ÉS és értékadás                                            | `BitAndAssign` |
| `&&`                      | `expr && expr`                                          | Rövidzáras logikai ÉS                                                 |                |
| `*`                       | `expr * expr`                                           | Aritmetikai szorzás                                                   | `Mul`          |
| `*=`                      | `var *= expr`                                           | Aritmetikai szorzás és értékadás                                      | `MulAssign`    |
| `*`                       | `*expr`                                                 | Dereferálás                                                           | `Deref`        |
| `*`                       | `*const type`, `*mut type`                              | Nyers mutató                                                          |                |
| `+`                       | `trait + trait`, `'a + trait`                           | Összetett típuskorlát                                                 |                |
| `+`                       | `expr + expr`                                           | Aritmetikai összeadás                                                 | `Add`          |
| `+=`                      | `var += expr`                                           | Aritmetikai összeadás és értékadás                                    | `AddAssign`    |
| `,`                       | `expr, expr`                                            | Argumentum- és elemelválasztó                                         |                |
| `-`                       | `- expr`                                                | Aritmetikai negálás                                                   | `Neg`          |
| `-`                       | `expr - expr`                                           | Aritmetikai kivonás                                                   | `Sub`          |
| `-=`                      | `var -= expr`                                           | Aritmetikai kivonás és értékadás                                      | `SubAssign`    |
| `->`                      | `fn(...) -> type`, <code>&vert;...&vert; -> type</code> | Függvény és closure visszatérési típusa                               |                |
| `.`                       | `expr.ident`                                            | Mezőelérés                                                            |                |
| `.`                       | `expr.ident(expr, ...)`                                 | Metódushívás                                                          |                |
| `.`                       | `expr.0`, `expr.1` és így tovább                        | Tuple indexelése                                                      |                |
| `..`                      | `..`, `expr..`, `..expr`, `expr..expr`                  | Jobbról nyílt tartományliterál                                        | `PartialOrd`   |
| `..=`                     | `..=expr`, `expr..=expr`                                | Jobbról zárt tartományliterál                                         | `PartialOrd`   |
| `..`                      | `..expr`                                                | Struktúraliterál frissítő szintaxisa                                  |                |
| `..`                      | `variant(x, ..)`, `struct_type { x, .. }`               | „És a többi” mintakötés                                               |                |
| `...`                     | `expr...expr`                                           | (Elavult, helyette használd a `..=` alakot) Mintában: zárt tartományminta |            |
| `/`                       | `expr / expr`                                           | Aritmetikai osztás                                                    | `Div`          |
| `/=`                      | `var /= expr`                                           | Aritmetikai osztás és értékadás                                       | `DivAssign`    |
| `:`                       | `pat: type`, `ident: type`                              | Korlátok                                                              |                |
| `:`                       | `ident: expr`                                           | Struktúramező inicializálása                                          |                |
| `:`                       | `'a: loop {...}`                                        | Cikluscímke                                                           |                |
| `;`                       | `expr;`                                                 | Utasítás- és elemlezáró                                               |                |
| `;`                       | `[...; len]`                                            | A rögzített méretű tömb szintaxisának része                           |                |
| `<<`                      | `expr << expr`                                          | Balra léptetés                                                        | `Shl`          |
| `<<=`                     | `var <<= expr`                                          | Balra léptetés és értékadás                                           | `ShlAssign`    |
| `<`                       | `expr < expr`                                           | Kisebb mint összehasonlítás                                           | `PartialOrd`   |
| `<=`                      | `expr <= expr`                                          | Kisebb vagy egyenlő összehasonlítás                                   | `PartialOrd`   |
| `=`                       | `var = expr`, `ident = type`                            | Értékadás/egyenértékűség                                              |                |
| `==`                      | `expr == expr`                                          | Egyenlőség vizsgálata                                                 | `PartialEq`    |
| `=>`                      | `pat => expr`                                           | A match ág szintaxisának része                                        |                |
| `>`                       | `expr > expr`                                           | Nagyobb mint összehasonlítás                                          | `PartialOrd`   |
| `>=`                      | `expr >= expr`                                          | Nagyobb vagy egyenlő összehasonlítás                                  | `PartialOrd`   |
| `>>`                      | `expr >> expr`                                          | Jobbra léptetés                                                       | `Shr`          |
| `>>=`                     | `var >>= expr`                                          | Jobbra léptetés és értékadás                                          | `ShrAssign`    |
| `@`                       | `ident @ pat`                                           | Mintakötés                                                            |                |
| `^`                       | `expr ^ expr`                                           | Bitenkénti kizáró VAGY                                                | `BitXor`       |
| `^=`                      | `var ^= expr`                                           | Bitenkénti kizáró VAGY és értékadás                                   | `BitXorAssign` |
| <code>&vert;</code>       | <code>pat &vert; pat</code>                             | Mintaalternatívák                                                     |                |
| <code>&vert;</code>       | <code>expr &vert; expr</code>                           | Bitenkénti VAGY                                                       | `BitOr`        |
| <code>&vert;=</code>      | <code>var &vert;= expr</code>                           | Bitenkénti VAGY és értékadás                                          | `BitOrAssign`  |
| <code>&vert;&vert;</code> | <code>expr &vert;&vert; expr</code>                     | Rövidzáras logikai VAGY                                               |                |
| `?`                       | `expr?`                                                 | Hibatovábbadás                                                        |                |

### Nem operátor szimbólumok {#non-operator-symbols}

Az alábbi táblázatok azokat a szimbólumokat tartalmazzák, amelyek nem
operátorként működnek, vagyis nem úgy viselkednek, mint egy függvény- vagy
metódushívás.

A B-2. táblázat azokat a szimbólumokat mutatja, amelyek önmagukban állnak, és
sokféle helyen érvényesek.

<span class="caption">B-2. táblázat: Önálló szintaxis</span>

| Szimbólum                                                              | Magyarázat                                                             |
| ---------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| `'ident`                                                               | Elnevezett élettartam vagy cikluscímke                                 |
| Számjegyek, közvetlenül utánuk `u8`, `i32`, `f64`, `usize` és így tovább | Adott típusú számliterál                                             |
| `"..."`                                                                | Sztringliterál                                                         |
| `r"..."`, `r#"..."#`, `r##"..."##` és így tovább                       | Nyers sztringliterál; az escape-karaktereket nem dolgozza fel          |
| `b"..."`                                                               | Bájtsztring-literál; sztring helyett bájttömböt hoz létre              |
| `br"..."`, `br#"..."#`, `br##"..."##` és így tovább                    | Nyers bájtsztring-literál; a nyers és a bájtsztring-literál kombinációja |
| `'...'`                                                                | Karakterliterál                                                        |
| `b'...'`                                                               | ASCII bájtliterál                                                      |
| <code>&vert;...&vert; expr</code>                                      | Closure                                                                |
| `!`                                                                    | Divergáló függvények mindig üres „bottom” típusa                       |
| `_`                                                                    | „Figyelmen kívül hagyott” mintakötés; egész literálok olvashatóbbá tételére is használják |

A B-3. táblázat azokat a szimbólumokat mutatja, amelyek a modulhierarchián át
egy elemhez vezető útvonal környezetében fordulnak elő.

<span class="caption">B-3. táblázat: Útvonalakkal kapcsolatos szintaxis</span>

| Szimbólum                               | Magyarázat                                                                                                   |
| --------------------------------------- | -------------------------------------------------------------------------------------------------------------|
| `ident::ident`                          | Névtérútvonal                                                                                                |
| `::path`                                | A crate-gyökérhez viszonyított útvonal (azaz explicit abszolút útvonal)                                      |
| `self::path`                            | Az aktuális modulhoz viszonyított útvonal (azaz explicit relatív útvonal)                                    |
| `super::path`                           | Az aktuális modul szülőjéhez viszonyított útvonal                                                            |
| `type::ident`, `<type as trait>::ident` | Társított konstansok, függvények és típusok                                                                  |
| `<type>::...`                           | Közvetlenül meg nem nevezhető típus társított eleme (például `<&T>::...`, `<[T]>::...` és így tovább)        |
| `trait::method(...)`                    | Metódushívás egyértelműsítése az azt definiáló trait megnevezésével                                          |
| `type::method(...)`                     | Metódushívás egyértelműsítése annak a típusnak a megnevezésével, amelyre definiálva van                     |
| `<type as trait>::method(...)`          | Metódushívás egyértelműsítése a trait és a típus megnevezésével                                              |

A B-4. táblázat azokat a szimbólumokat mutatja, amelyek generikus
típusparaméterek használatának környezetében fordulnak elő.

<span class="caption">B-4. táblázat: Generikus típusok</span>

| Szimbólum                      | Magyarázat                                                                                                                                          |
| ------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `path<...>`                    | Egy generikus típus paramétereit adja meg egy típusban (például `Vec<u8>`)                                                                         |
| `path::<...>`, `method::<...>` | Egy generikus típus, függvény vagy metódus paramétereit adja meg egy kifejezésben; gyakran _turbofish_ néven emlegetik (például `"42".parse::<i32>()`) |
| `fn ident<...> ...`            | Generikus függvény definiálása                                                                                                                      |
| `struct ident<...> ...`        | Generikus struktúra definiálása                                                                                                                     |
| `enum ident<...> ...`          | Generikus felsorolás definiálása                                                                                                                    |
| `impl<...> ...`                | Generikus megvalósítás definiálása                                                                                                                  |
| `for<...> type`                | Magasabb rendű élettartam-korlátok                                                                                                                  |
| `type<ident=type>`             | Olyan generikus típus, amelyben egy vagy több társított típus konkrét értéket kap (például `Iterator<Item=T>`)                                     |

A B-5. táblázat azokat a szimbólumokat mutatja, amelyek a generikus
típusparaméterek trait-korlátokkal való megszorításának környezetében
fordulnak elő.

<span class="caption">B-5. táblázat: Trait-korlátok</span>

| Szimbólum                     | Magyarázat                                                                                                                                 |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `T: U`                        | A `T` generikus paraméter olyan típusokra korlátozva, amelyek megvalósítják az `U`-t                                                       |
| `T: 'a`                       | A `T` generikus típusnak túl kell élnie az `'a` élettartamot (vagyis a típus közvetve sem tartalmazhat `'a`-nál rövidebb élettartamú referenciát) |
| `T: 'static`                  | A `T` generikus típus a `'static` referenciákon kívül nem tartalmaz kölcsönzött referenciát                                                |
| `'b: 'a`                      | A `'b` generikus élettartamnak túl kell élnie az `'a` élettartamot                                                                         |
| `T: ?Sized`                   | Megengedi, hogy a generikus típusparaméter dinamikus méretű típus legyen                                                                   |
| `'a + trait`, `trait + trait` | Összetett típuskorlát                                                                                                                      |

A B-6. táblázat azokat a szimbólumokat mutatja, amelyek makrók hívásának vagy
definiálásának, illetve elemek attribútumainak megadásakor fordulnak elő.

<span class="caption">B-6. táblázat: Makrók és attribútumok</span>

| Szimbólum                                   | Magyarázat         |
| ------------------------------------------- | ------------------ |
| `#[meta]`                                   | Külső attribútum   |
| `#![meta]`                                  | Belső attribútum   |
| `$ident`                                    | Makróhelyettesítés |
| `$ident:kind`                               | Makró-metaváltozó  |
| `$(...)...`                                 | Makróismétlés      |
| `ident!(...)`, `ident!{...}`, `ident![...]` | Makróhívás         |

A B-7. táblázat a kommenteket létrehozó szimbólumokat mutatja.

<span class="caption">B-7. táblázat: Kommentek</span>

| Szimbólum  | Magyarázat                       |
| ---------- | -------------------------------- |
| `//`       | Egysoros komment                 |
| `//!`      | Belső egysoros dokumentációs komment |
| `///`      | Külső egysoros dokumentációs komment |
| `/*...*/`  | Blokkkomment                     |
| `/*!...*/` | Belső dokumentációs blokkkomment |
| `/**...*/` | Külső dokumentációs blokkkomment |

A B-8. táblázat azt mutatja, milyen környezetekben használunk kerek
zárójeleket.

<span class="caption">B-8. táblázat: Kerek zárójelek</span>

| Szimbólum                | Magyarázat                                                                                  |
| ------------------------ | ------------------------------------------------------------------------------------------- |
| `()`                     | Üres tuple (más néven unit), literálként és típusként is                                    |
| `(expr)`                 | Zárójelezett kifejezés                                                                      |
| `(expr,)`                | Egyelemű tuple kifejezés                                                                    |
| `(type,)`                | Egyelemű tuple típus                                                                        |
| `(expr, ...)`            | Tuple kifejezés                                                                             |
| `(type, ...)`            | Tuple típus                                                                                 |
| `expr(expr, ...)`        | Függvényhívás-kifejezés; tuple `struct`-ok és tuple `enum`-változatok inicializálására is használják |

A B-9. táblázat azt mutatja, milyen környezetekben használunk kapcsos
zárójeleket.

<span class="caption">B-9. táblázat: Kapcsos zárójelek</span>

| Környezet    | Magyarázat         |
| ------------ | ------------------ |
| `{...}`      | Blokkifejezés      |
| `Type {...}` | Struktúraliterál   |

A B-10. táblázat azt mutatja, milyen környezetekben használunk szögletes
zárójeleket.

<span class="caption">B-10. táblázat: Szögletes zárójelek</span>

| Környezet                                          | Magyarázat                                                                                                                    |
| -------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `[...]`                                            | Tömbliterál                                                                                                                   |
| `[expr; len]`                                      | Az `expr` `len` darab másolatát tartalmazó tömbliterál                                                                        |
| `[type; len]`                                      | A `type` `len` darab példányát tartalmazó tömbtípus                                                                           |
| `expr[expr]`                                       | Gyűjtemény indexelése; túlterhelhető (`Index`, `IndexMut`)                                                                    |
| `expr[..]`, `expr[a..]`, `expr[..b]`, `expr[a..b]` | Szeletelésnek álcázott gyűjteményindexelés, amely „indexként” `Range`, `RangeFrom`, `RangeTo` vagy `RangeFull` értéket használ |
