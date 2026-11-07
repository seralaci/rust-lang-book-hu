# A tulajdonjog megértése {#understanding-ownership}

A _tulajdonjog (ownership)_ a Rust legegyedibb tulajdonsága, és mélyreható
következményei vannak a nyelv egészére nézve. Ennek köszönhetően a Rust
szemétgyűjtő (garbage collector) nélkül is garantálni tudja a memória
biztonságos használatát, ezért fontos megérteni, hogyan működik a tulajdonjog.
Ebben a fejezetben a tulajdonjog mellett néhány kapcsolódó nyelvi elemről is
szó lesz: a kölcsönzésről (borrowing), a szeletekről (slices), és arról, hogyan
helyezi el a Rust az adatokat a memóriában.
