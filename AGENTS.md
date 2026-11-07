# Rust könyv – magyar fordítás

Ez a rust-lang/book forkja; a cél a könyv magyar fordítása.

- A fordítás szabályai, a szójegyzék és az upstream szinkron menete:
  **[FORDITAS.md](FORDITAS.md)** – fordítás előtt mindig olvasd el, és új
  szakkifejezést előbb ott vegyél fel.
- A magyar szöveg a `src-hu/` mappában van. A `src/` (angol eredeti) és a
  `listings/` (kódpéldák) **nem módosítható**.
- Build: `mdbook build hu` (a repó gyökeréből), utána ellenőrzés:
  `python3 hu/ellenorzes.py` (szerkezet, horgonyok, sorhossz, belső linkek). Minden
  fordítás után futtasd le mindkettőt; 0 hibának kell lennie.
- Fejezet fordításakor a más fejezetekre mutató linkek szövegét a cél
  fejezet már lefordított címsorához igazítsd (a `src-hu/SUMMARY.md` és a
  lefordított fájlok címsorai a mérvadók); az ellenőrző szkript jelzi az
  eltéréseket.
- A fordítás bekezdésről bekezdésre követi az angol fájl szerkezetét; minden
  lefordított címsor végére kerüljön oda az eredeti angol horgony: `{#angol-horgony}`.
