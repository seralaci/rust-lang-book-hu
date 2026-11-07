## Kommentek {#comments}

Minden programozó arra törekszik, hogy a kódja könnyen érthető legyen, de néha
további magyarázatra van szükség. Ilyenkor a programozók _kommenteket
(comments)_ hagynak a forráskódban, amelyeket a fordító figyelmen kívül hagy,
a forráskódot olvasók viszont hasznosnak találhatják.

Íme egy egyszerű komment:

```rust
// hello, world
```

A Rustban az idiomatikus kommentstílus szerint a komment két perjellel
kezdődik, és a sor végéig tart. Az egy sornál hosszabb kommentekhez minden
sorba ki kell írnod a `//`-t, így:

```rust
// So we're doing something complicated here, long enough that we need
// multiple lines of comments to do it! Whew! Hopefully, this comment will
// explain what's going on.
```

Kommentet kódot tartalmazó sorok végére is írhatunk:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-24-comments-end-of-line/src/main.rs}}
```

Gyakrabban fogod azonban ebben a formában látni őket, amikor a komment külön
sorban, az általa magyarázott kód fölött áll:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-25-comments-above-line/src/main.rs}}
```

A Rustban van egy másik fajta komment is, a dokumentációs komment, amelyről a
14. fejezet [„Crate közzététele a Crates.io-n”][publishing]<!-- ignore -->
című szakaszában lesz szó.

[publishing]: ch14-02-publishing-to-crates-io.html
