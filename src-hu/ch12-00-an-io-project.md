# Egy I/O projekt: parancssori program készítése {#an-io-project-building-a-command-line-program}

Ez a fejezet összefoglalja az eddig megszerzett tudásod nagy részét, és
megismertet a standard könyvtár néhány további lehetőségével. Egy olyan
parancssori eszközt készítünk, amely fájlokkal és parancssori bemenettel,
illetve kimenettel dolgozik, hogy begyakorolhasd a Rust már elsajátított
fogalmainak egy részét.

A Rust sebessége, biztonsága, egyetlen bináris fájlt előállító buildje és
platformfüggetlensége ideális nyelvvé teszi parancssori eszközök készítésére,
ezért a projektünkben a klasszikus parancssori keresőeszköz, a `grep`
(**g**lobally search a **r**egular **e**xpression and **p**rint, azaz egy
reguláris kifejezés globális keresése és kiírása) saját változatát készítjük
el. A legegyszerűbb esetben a `grep` egy megadott fájlban keres egy megadott
sztringet. Ehhez a `grep` argumentumként egy fájl elérési útját és egy
sztringet kap. Ezután beolvassa a fájlt, megkeresi benne azokat a sorokat,
amelyek tartalmazzák a sztringargumentumot, és kiírja ezeket a sorokat.

Közben azt is megmutatjuk, hogyan használhatja a parancssori eszközünk a
terminál azon lehetőségeit, amelyekre sok más parancssori eszköz is épít. Egy
_környezeti változó (environment variable)_ értékét olvassuk be, hogy a
felhasználó beállíthassa az eszközünk viselkedését. A hibaüzeneteket pedig a
standard kimenet (`stdout`) helyett a standard hibakimenetre (`stderr`) írjuk
ki, így a felhasználó például fájlba irányíthatja a sikeres kimenetet, a
hibaüzeneteket mégis látja a képernyőn.

A Rust közösség egyik tagja, Andrew Gallant már elkészítette a `grep` egy
teljes funkcionalitású, nagyon gyors változatát `ripgrep` néven. Ehhez képest
a mi változatunk meglehetősen egyszerű lesz, de ez a fejezet megadja azt a
háttértudást, amely egy olyan valós projekt megértéséhez kell, mint a
`ripgrep`.

A `grep` projektünk számos eddig megismert fogalmat ötvöz:

- A kód szervezése ([7. fejezet][ch7]<!-- ignore -->)
- Vektorok és sztringek használata ([8. fejezet][ch8]<!-- ignore -->)
- Hibakezelés ([9. fejezet][ch9]<!-- ignore -->)
- Traitek és élettartamok használata, ahol indokolt
  ([10. fejezet][ch10]<!-- ignore -->)
- Tesztek írása ([11. fejezet][ch11]<!-- ignore -->)

Röviden bemutatjuk a closure-öket, az iterátorokat és a trait objektumokat is,
amelyekkel a [13. fejezet][ch13]<!-- ignore --> és a
[18. fejezet][ch18]<!-- ignore --> foglalkozik részletesen.

[ch7]: ch07-00-managing-growing-projects-with-packages-crates-and-modules.html
[ch8]: ch08-00-common-collections.html
[ch9]: ch09-00-error-handling.html
[ch10]: ch10-00-generics.html
[ch11]: ch11-00-testing.html
[ch13]: ch13-00-functional-features.html
[ch18]: ch18-00-oop.html
