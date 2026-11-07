# Minták és mintaillesztés {#patterns-and-matching}

A minták (patterns) a Rust egy különleges szintaxisát alkotják, amellyel
egyszerű és összetett típusok szerkezetére illeszthetünk. Ha a mintákat
`match` kifejezésekkel és más szerkezetekkel együtt használod, jobban
irányíthatod a program vezérlési folyamatát. Egy minta a következők valamilyen
kombinációjából áll:

- literálok
- szétbontott tömbök, enumok, struktúrák vagy tuple-ök
- változók
- helyettesítő jelek (wildcards)
- helyőrzők (placeholders)

Néhány példa a mintákra: `x`, `(a, 3)` és `Some(Color::Red)`. Azokban a
környezetekben, ahol a minták érvényesek, ezek az összetevők az adatok alakját
írják le. A program ezután az értékeket a mintákhoz illeszti, hogy eldöntse,
megfelelő alakú-e az adat ahhoz, hogy egy adott kódrészlet tovább fusson.

Egy minta használatához össze kell vetnünk valamilyen értékkel. Ha a minta
illeszkedik az értékre, az érték részeit felhasználhatjuk a kódunkban. Idézd
fel a 6. fejezet mintákat használó `match` kifejezéseit, például az
érmeválogató gépes példát. Ha az érték illeszkedik a minta alakjára,
használhatjuk a megnevezett részeket. Ha nem, a mintához tartozó kód nem fut le.

Ez a fejezet a mintákkal kapcsolatos tudnivalók kézikönyve. Áttekintjük, hol
használhatunk mintákat, mi a különbség a cáfolható és a cáfolhatatlan minták
között, és milyen különféle mintaszintaxisokkal találkozhatsz. A fejezet
végére tudni fogod, hogyan fejezhetsz ki mintákkal sokféle fogalmat világosan.
