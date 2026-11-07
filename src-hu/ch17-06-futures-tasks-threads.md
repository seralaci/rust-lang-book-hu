## Mindent összerakva: future-ök, taskok és szálak {#putting-it-all-together-futures-tasks-and-threads}

Ahogy a [16. fejezetben][ch16]<!-- ignore --> láttuk, a szálak a konkurencia
egyik megközelítését kínálják. Ebben a fejezetben egy másik megközelítést is
láttunk: az async használatát future-ökkel és streamekkel. Ha azon
gondolkodsz, mikor melyik módszert válaszd, a válasz az, hogy attól függ! És
sok esetben a választás nem az, hogy szálak _vagy_ async, hanem inkább szálak
_és_ async.

Sok operációs rendszer már évtizedek óta biztosít szálalapú
konkurenciamodelleket, és ennek eredményeként sok programozási nyelv támogatja
őket. Ezek a modellek azonban nem mentesek a kompromisszumoktól. Sok operációs
rendszeren szálanként elég sok memóriát használnak. A szálak ráadásul csak
akkor jöhetnek szóba, ha az operációs rendszered és a hardvered támogatja őket.
A szokásos asztali és mobil számítógépekkel ellentétben egyes beágyazott
rendszereken egyáltalán nincs operációs rendszer, így szálak sincsenek.

Az async modell másfajta – és végső soron kiegészítő jellegű – kompromisszumokat
kínál. Az async modellben a konkurens műveleteknek nincs szükségük saját
szálakra. Ehelyett _taskokon (tasks)_ futhatnak, ahogy akkor is, amikor a
streamekről szóló részben a `trpl::spawn_task` segítségével egy szinkron
függvényből indítottunk munkát. A task hasonló a szálhoz, de nem az operációs
rendszer kezeli, hanem könyvtárszintű kód: a futtatókörnyezet.

Megvan az oka annak, hogy a szálak és a taskok indítására szolgáló API-k
ennyire hasonlók. A szálak a szinkron műveletek csoportjainak határaként
működnek; a konkurencia a szálak _között_ lehetséges. A taskok az _aszinkron_
műveletek csoportjainak határaként működnek; a konkurencia a taskok _között_ és
_azokon belül_ is lehetséges, mert egy task a törzsében válthat a future-ök
között. Végül a future-ök a Rust legfinomabb szemcsézettségű
konkurenciaegységei, és minden future más future-ök egy fáját is képviselheti.
A futtatókörnyezet – pontosabban annak végrehajtója – kezeli a taskokat, a
taskok pedig a future-öket. Ebből a szempontból a taskok a könnyűsúlyú,
futtatókörnyezet által kezelt szálakhoz hasonlítanak, olyan további
képességekkel, amelyek abból fakadnak, hogy nem az operációs rendszer, hanem
egy futtatókörnyezet kezeli őket.

Ez nem jelenti azt, hogy az async taskok mindig jobbak a szálaknál (vagy
fordítva). A szálakkal megvalósított konkurencia bizonyos szempontból
egyszerűbb programozási modell, mint az `async`-kel megvalósított. Ez lehet
erősség és gyengeség is. A szálak afféle „elindítod és elfelejted” jellegűek;
nincs a future-nek megfelelő natív megfelelőjük, így egyszerűen végigfutnak,
anélkül hogy bármi megszakítaná őket, kivéve magát az operációs rendszert.

És kiderül, hogy a szálak és a taskok gyakran nagyon jól működnek együtt,
mert a taskokat (legalábbis egyes futtatókörnyezetekben) mozgatni lehet a
szálak között. Valójában a háttérben az általunk használt futtatókörnyezet –
beleértve a `spawn_blocking` és a `spawn_task` függvényt is – alapértelmezés
szerint többszálú! Sok futtatókörnyezet a _munkalopás (work stealing)_ nevű
megközelítést használja arra, hogy a taskokat átláthatóan mozgassa a szálak
között, attól függően, hogy éppen mennyire vannak kihasználva a szálak, hogy
javítsa a rendszer teljesítményét. Ehhez a megközelítéshez valójában szálakra
_és_ taskokra, és így future-ökre is szükség van.

Amikor azon gondolkodsz, mikor melyik módszert használd, vedd figyelembe ezeket
az ökölszabályokat:

- Ha a munka _jól párhuzamosítható_ (vagyis CPU-korlátos), például egy csomó
  adat feldolgozása, ahol minden rész külön feldolgozható, a szálak a jobb
  választás.
- Ha a munka _erősen konkurens_ (vagyis I/O-korlátos), például egy csomó
  különböző forrásból érkező üzenet kezelése, amelyek eltérő időközönként vagy
  eltérő ütemben érkezhetnek, az async a jobb választás.

Ha pedig párhuzamosságra és konkurenciára is szükséged van, nem kell választanod
a szálak és az async között. Szabadon használhatod őket együtt, és mindegyikre
azt a szerepet bízhatod, amelyben a legjobb. A 17-25. kódrészlet például egy
meglehetősen gyakori példát mutat az ilyen keverésre a valós Rust kódban.

<Listing number="17-25" caption="Üzenetek küldése blokkoló kóddal egy szálban, és az üzenetek bevárása egy async blokkban" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-25/src/main.rs:all}}
```

</Listing>

Először létrehozunk egy async csatornát, majd indítunk egy szálat, amely a
`move` kulcsszó segítségével átveszi a csatorna küldő oldalának tulajdonjogát.
A szálon belül elküldjük a számokat 1-től 10-ig, mindegyik között egy
másodpercig alva. Végül egy async blokkal létrehozott future-t futtatunk,
amelyet a `trpl::block_on`-nak adunk át, ugyanúgy, ahogy a fejezet során
végig. Ebben a future-ben bevárjuk ezeket az üzeneteket, ugyanúgy, mint a
többi látott üzenetküldéses példában.

Hogy visszatérjünk a forgatókönyvhöz, amellyel a fejezetet kezdtük, képzeld
el, hogy videókódolási feladatok egy sorát egy dedikált szálon futtatod (mert
a videókódolás számításkorlátos), de egy async csatornán keresztül értesíted a
felhasználói felületet arról, hogy ezek a műveletek befejeződtek. Számtalan
példa van az ilyen kombinációkra a valós felhasználási esetekben.

## Összefoglalás {#summary}

Nem most találkozol utoljára a konkurenciával ebben a könyvben. A
[21. fejezet][ch21]<!-- ignore --> projektje ezeket a fogalmakat egy az itt
tárgyalt egyszerűbb példáknál valósághűbb helyzetben alkalmazza, és
közvetlenebbül összeveti a szálakkal, illetve a taskokkal és future-ökkel
történő problémamegoldást.

Akármelyik megközelítést is választod, a Rust megadja a szükséges eszközöket
biztonságos, gyors, konkurens kód írásához – legyen szó egy nagy
áteresztőképességű webszerverről vagy egy beágyazott operációs rendszerről.

A következőkben arról lesz szó, milyen idiomatikus módokon modellezhetjük a
problémákat és strukturálhatjuk a megoldásokat, ahogy a Rust programjaid egyre
nagyobbak lesznek. Emellett megvitatjuk, hogyan viszonyulnak a Rust idiómái
azokhoz, amelyeket az objektumorientált programozásból ismerhetsz.

[ch16]: ch16-00-concurrency.html
[combining-futures]: ch17-03-more-futures.html#building-our-own-async-abstractions
[streams]: ch17-04-streams.html#composing-streams
[ch21]: ch21-00-final-project-a-web-server.html
