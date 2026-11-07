## A Cargo bővítése egyéni parancsokkal {#extending-cargo-with-custom-commands}

A Cargót úgy tervezték, hogy új alparancsokkal bővíthesd anélkül, hogy
módosítanod kellene. Ha a `$PATH` változódban szereplő valamelyik bináris neve
`cargo-something`, akkor a `cargo something` paranccsal úgy futtathatod,
mintha a Cargo egyik alparancsa lenne. Az ilyen egyéni parancsok a
`cargo --list` futtatásakor is megjelennek a listában. Az, hogy a
`cargo install` paranccsal bővítményeket telepíthetsz, majd ugyanúgy
futtathatod őket, mint a Cargo beépített eszközeit, a Cargo felépítésének egy
rendkívül kényelmes előnye!

## Összefoglalás {#summary}

A kód megosztása a Cargóval és a [crates.io](https://crates.io/)<!-- ignore
--> oldallal az egyik oka annak, hogy a Rust ökoszisztémája sokféle feladathoz
hasznos. A Rust standard könyvtára kicsi és stabil, a crate-eket viszont
könnyű megosztani, használni és fejleszteni, a nyelvétől eltérő ütemezés
szerint. Ne habozz megosztani a számodra hasznos kódot a
[crates.io](https://crates.io/)<!-- ignore --> oldalon; valószínűleg másnak is
hasznos lesz!
