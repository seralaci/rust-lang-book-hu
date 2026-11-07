# Hibakezelés {#error-handling}

A hibák a szoftverfejlesztés elkerülhetetlen részei, ezért a Rust számos
nyelvi elemet kínál azoknak a helyzeteknek a kezelésére, amikor valami elromlik.
A Rust sok esetben megköveteli, hogy tudomásul vedd egy hiba lehetőségét, és
tegyél valamit, mielőtt a kódod lefordulna. Ez a követelmény robusztusabbá teszi
a programodat, mert biztosítja, hogy a hibákat még azelőtt felfedezd és
megfelelően kezeld, hogy a kódodat éles környezetbe telepítenéd!

A Rust a hibákat két nagy csoportba sorolja: helyrehozható és helyrehozhatatlan
hibákra. Egy _helyrehozható hiba (recoverable error)_, például a _fájl nem
található_ hiba esetén valószínűleg csak jelezni szeretnénk a problémát a
felhasználónak, és újra megpróbálni a műveletet. A _helyrehozhatatlan hibák
(unrecoverable errors)_ mindig programhibák tünetei, ilyen például egy tömb
végén túli hely elérésének kísérlete, ezért ilyenkor azonnal le szeretnénk
állítani a programot.

A legtöbb nyelv nem tesz különbséget e két hibafajta között, és mindkettőt
ugyanúgy kezeli, például kivételek (exceptions) segítségével. A Rustban
nincsenek kivételek. Ehelyett a helyrehozható hibákra a `Result<T, E>` típus, a
helyrehozhatatlan hibákra pedig a `panic!` makró szolgál, amely leállítja a
végrehajtást, ha a program helyrehozhatatlan hibába ütközik. Ez a fejezet
először a `panic!` hívásával foglalkozik, majd a `Result<T, E>` értékek
visszaadásáról szól. Ezen kívül megvizsgáljuk, mit érdemes mérlegelni, amikor
eldöntjük, hogy megpróbáljuk-e helyrehozni egy hibát, vagy inkább leállítjuk a
végrehajtást.
