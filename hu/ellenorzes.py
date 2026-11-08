#!/usr/bin/env python3
"""A magyar fordítás ellenőrzése.

Használat a repó gyökeréből (előtte: `mdbook build hu`):

    python3 hu/ellenorzes.py                  # minden lefordított fájl
    python3 hu/ellenorzes.py ch04 ch05        # csak a megadott előtagú fájlok

Ellenőrzi:
  1. a szerkezetet az angol eredetihez képest (címsorok, kódblokkok, <Listing>,
     {{#...}} direktívák, linkdefiníciók, <a id> horgonyok száma),
  2. hogy minden lefordított címsoron van-e `{#angol-horgony}`,
  3. a 80 karakternél hosszabb prózai sorokat,
  4. hogy a belső linkek (`fájl.html#horgony`) létező horgonyra mutatnak-e a
     buildelt könyvben (hu/book/),
  5. hogy a más szakaszok címét idéző linkszövegek egyeznek-e a cél címsorával
     (csak tájékoztató jellegű: a leíró linkszöveg, pl. „a 3. fejezetben”,
     szándékosan eltérhet).
"""

import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

HEADING = re.compile(r"^#{1,6} ")
FENCE = re.compile(r"^\s*(?:> )?```")


def is_translated(path):
    """Egy fájl lefordított, ha eltér az angol eredetitől."""
    en = os.path.join("src", os.path.basename(path))
    return not os.path.exists(en) or open(en).read() != open(path).read()


LIST_ITEM = re.compile(r"^(?:> )?\s*(?:[-*+]|\d+[.)])\s")


def prose_lines(lines):
    """A kódblokkokon kívüli sorok."""
    in_code = False
    for l in lines:
        if FENCE.match(l):
            in_code = not in_code
            continue
        if not in_code:
            yield l


def count_list_items(prose):
    """Listaelemek a CommonMark szabálya szerint: bekezdés közepén csak a
    felsorolásjel (`-`, `*`, `+`) és az `1.` kezdetű számozás indít listát; a
    sor elején álló „3. fejezet” folytatja a bekezdést."""
    count = 0
    prev = ""
    for l in prose:
        bare = l[2:] if l.startswith("> ") else l
        m = LIST_ITEM.match(l)
        if m:
            numbered = re.match(r"\s*(\d+)[.)]", bare)
            prev_bare = prev[2:] if prev.startswith("> ") else prev
            starts_block = not prev_bare.strip() or LIST_ITEM.match(prev)
            if not numbered or numbered.group(1) == "1" or starts_block:
                count += 1
        prev = l
    return count


def structure(text):
    lines = text.split("\n")
    prose = list(prose_lines(lines))
    # Blokkidézet-blokk: egymást követő `>` kezdetű sorok csoportja. Ha egy
    # tördelt sor véletlenül `> ` jellel kezdődik, ez a szám eltér.
    quotes = sum(
        1
        for i, l in enumerate(prose)
        if l.startswith(">") and (i == 0 or not prose[i - 1].startswith(">"))
    )
    return {
        "címsor": sum(1 for l in lines if HEADING.match(l.lstrip("> "))),
        "kódblokk-kerítés": sum(1 for l in lines if FENCE.match(l)),
        "<Listing>": text.count("<Listing"),
        "{{#...}}": text.count("{{#"),
        "linkdefiníció": len(re.findall(r"^\[[^\]]+\]:", text, re.M)),
        "<a id>": text.count("<a id="),
        # Ha egy tördelt sor véletlenül `- ` vagy `1. ` alakkal kezdődik,
        # listaelemmé válik; ez a szám jelzi.
        "listaelem": count_list_items(prose),
        "blokkidézet": quotes,
    }


def main(prefixes):
    files = sorted(glob.glob("src-hu/*.md"))
    files = [f for f in files if os.path.basename(f) != "SUMMARY.md"]
    if prefixes:
        files = [f for f in files if os.path.basename(f).startswith(tuple(prefixes))]
    files = [f for f in files if is_translated(f)]

    problems = 0

    # 1–3: szerkezet, horgonyok, sorhossz
    for f in files:
        hu = open(f).read()
        en_path = os.path.join("src", os.path.basename(f))
        if os.path.exists(en_path):
            en_s, hu_s = structure(open(en_path).read()), structure(hu)
            for k in en_s:
                if en_s[k] != hu_s[k]:
                    print(f"{f}: szerkezet – {k}: angol {en_s[k]}, magyar {hu_s[k]}")
                    problems += 1
        in_code = in_comment = False
        for i, line in enumerate(hu.split("\n"), 1):
            if FENCE.match(line):
                in_code = not in_code
                continue
            if "<!--" in line and "-->" not in line.split("<!--")[-1]:
                in_comment = True
            if in_comment:
                in_comment = "-->" not in line
                continue
            if in_code:
                continue
            bare = line.lstrip("> ")
            if HEADING.match(bare) and not re.search(r"\{#[^}]+\}\s*$", bare):
                print(f"{f}:{i}: címsor horgony nélkül: {bare}")
                problems += 1
            if (
                len(line) > 80
                and not line.startswith(("|", "[", "#", "<", "{{"))
                and "http" not in line
                and not HEADING.match(bare)
            ):
                print(f"{f}:{i}: {len(line)} karakter hosszú sor")
                problems += 1

    # 4–5: belső linkek
    if not os.path.isdir("hu/book"):
        print("A hu/book nem létezik – futtasd előbb: mdbook build hu")
        return 1
    ids = {
        os.path.basename(p): set(re.findall(r'id="([^"]+)"', open(p).read()))
        for p in glob.glob("hu/book/*.html")
    }
    heads = {}
    for p in glob.glob("src-hu/*.md"):
        page = os.path.basename(p)[:-3] + ".html"
        for m in re.finditer(r"^#+ (.*?) \{#([^}]+)\}\s*$", open(p).read(), re.M):
            heads[(page, m.group(2))] = m.group(1)

    notes = []
    for f in files:
        text = open(f).read()
        defs = dict(re.findall(r"^\[([^\]]+)\]:\s*(\S+)", text, re.M))
        for ref, target in defs.items():
            # Az angol könyv a doc.rust-lang.org-on fut, ott a ../std/ stb.
            # relatív linkek működnek; nálunk abszolút cím kell.
            if target.startswith("../"):
                print(f"{f}: relatív külső link, írd át https://doc.rust-lang.org/ "
                      f"kezdetűre: [{ref}]: {target}")
                problems += 1
                continue
            if target.startswith("http") or "#" not in target:
                continue
            page, anchor = target.split("#", 1)
            page = page or os.path.basename(f)[:-3] + ".html"
            if page.endswith(".md"):  # az mdbook a .md linkeket .html-re alakítja
                page = page[:-3] + ".html"
            if anchor not in ids.get(page, set()):
                print(f"{f}: nem létező horgony: [{ref}]: {target}")
                problems += 1
        for m in re.finditer(r"\[((?:[^\[\]]|\n)+?)\]\[([^\]]+)\]", text):
            label = " ".join(m.group(1).split()).strip("„”")
            target = defs.get(m.group(2), "")
            if "#" not in target or target.startswith("http"):
                continue
            page, anchor = target.split("#", 1)
            if page.endswith(".md"):
                page = page[:-3] + ".html"
            heading = heads.get((page, anchor))
            if heading and label != heading and "„" in m.group(1):
                notes.append(f"{f}: „{label}” ≠ cél címsor: „{heading}”")

    if notes:
        print("\nIdézett címek, amelyek eltérnek a cél címsorától (nézd át):")
        print("\n".join(notes))

    print(f"\n{len(files)} lefordított fájl, {problems} hiba.")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
