# Haladó témák {#advanced-features}

Mostanra már megismerted a Rust programozási nyelv leggyakrabban használt
részeit. Mielőtt a 21. fejezetben még egy projektbe belevágnánk, megnézzük a
nyelv néhány olyan vonását, amelyekkel időnként találkozhatsz, de valószínűleg
nem minden nap használod őket. Ezt a fejezetet kézikönyvként is használhatod,
amikor ismeretlen dologba botlasz. Az itt tárgyalt nyelvi elemek nagyon
specifikus helyzetekben hasznosak. Bár nem fogsz gyakran nyúlni hozzájuk,
szeretnénk, ha átfogó képed lenne mindarról, amit a Rust nyújt.

Ebben a fejezetben a következőkről lesz szó:

- Unsafe Rust: hogyan mondhatsz le a Rust néhány garanciájáról, és vállalhatod
  magadra e garanciák kézi betartásának felelősségét
- Haladó traitek: társított típusok, alapértelmezett típusparaméterek,
  teljesen minősített szintaxis, szupertraitek és a newtype minta a traitekkel
  összefüggésben
- Haladó típusok: további tudnivalók a newtype mintáról, típusálnevek, a never
  típus és a dinamikus méretű típusok
- Haladó függvények és closure-ök: függvénymutatók és closure-ök visszaadása
- Makrók: módszerek olyan kód definiálására, amely fordítási időben további
  kódot definiál

A Rust nyelvi elemeinek egész tárháza ez, mindenki talál benne valamit
magának! Vágjunk bele!
