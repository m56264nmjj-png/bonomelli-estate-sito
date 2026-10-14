#!/usr/bin/env python3
"""Genera il sito in due lingue a partire dalle pagine bilingui in src/.

    python3 tools/build.py          # scrive le pagine italiane alla radice e quelle inglesi in en/
    python3 tools/build.py --check  # controlla che le pagine pubblicate siano aggiornate

Le pagine in src/ contengono entrambe le lingue (<span lang="it"> / <span lang="en">).
Ogni pagina generata contiene una sola lingua, con titolo, descrizione, canonical e
hreflang propri: così Google indicizza separatamente la versione italiana e quella inglese.
Non modificare a mano le pagine alla radice o in en/: modificare src/ e rilanciare lo script.
"""
import hashlib
import json
import pathlib
import re
import sys

from bs4 import BeautifulSoup, Comment
from bs4.formatter import HTMLFormatter

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from i18n import ATTR_EN, ORG_DESC_EN, PAGES, SAME, SITE  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
ASSET_DIRS = ("img/", "video/", "assets/", "fonts/")


class KeepOrder(HTMLFormatter):
    """Come il formatter "minimal" di BeautifulSoup, ma senza riordinare gli attributi né chiudere i tag vuoti con />."""

    def __init__(self):
        super().__init__(entity_substitution=HTMLFormatter.REGISTRY["minimal"].entity_substitution, void_element_close_prefix=None)

    def attributes(self, tag):
        return list(tag.attrs.items())


NOTICE = " Pagina generata da tools/build.py: modificare src/{} e rilanciare lo script. "


def url(lang, name):
    """Indirizzo pubblico di una pagina (name = nome del file sorgente)."""
    if lang == "it":
        return SITE if name == "index.html" else SITE + name
    en = PAGES[name]["en"]
    return SITE + "en/" if en == "index.html" else SITE + "en/" + en


def rel(here, there, name):
    """Indirizzo relativo, da una pagina nella lingua here, della stessa pagina nella lingua there."""
    file = name if there == "it" else PAGES[name]["en"]
    file = "./" if file == "index.html" else file
    if here == there:
        return file
    return ("en/" if there == "en" else "../") + ("" if file == "./" else file)


def version(path):
    return hashlib.md5((ROOT / path).read_bytes()).hexdigest()[:8]


def build_page(name, lang):
    src = (SRC / name).read_text(encoding="utf-8")
    soup = BeautifulSoup(src, "html.parser")
    meta = PAGES[name]
    other = "en" if lang == "it" else "it"
    errors = []

    soup.html["lang"] = lang

    # 1. Tiene solo la lingua della pagina.
    for el in soup.find_all(attrs={"lang": other}):
        if el.name != "html":
            el.decompose()
    for opt in soup.find_all("option", attrs={"data-it": True}):
        opt.string = opt["data-" + lang]
        del opt["data-it"]
        del opt["data-en"]

    # 2. Testi alternativi delle immagini e etichette per i lettori di schermo.
    if lang == "en":
        for attr in ("alt", "aria-label"):
            for el in soup.find_all(attrs={attr: True}):
                v = el[attr]
                if v in ATTR_EN:
                    el[attr] = ATTR_EN[v]
                elif v not in SAME:
                    errors.append(f"{name}: manca la traduzione inglese di {attr}={v!r} in tools/i18n.py")

    # 3. Selettore di lingua: link alla stessa pagina nell'altra lingua.
    for box in soup.select("div.lang"):
        box.clear()
        box["aria-label"] = "Lingua" if lang == "it" else "Language"
        for code in ("it", "en"):
            a = soup.new_tag("a", href=rel(lang, code, name), hreflang=code)
            if code == lang:
                a["aria-current"] = "true"
            a.string = code.upper()
            box.append(a)

    # 4. Indirizzi interni e percorsi dei file per le pagine in en/.
    if lang == "en":
        pattern = re.compile(r"^(" + "|".join(re.escape(p) for p in PAGES) + r")(#.*)?$")
        for el in soup.find_all(href=True):
            m = pattern.match(el["href"])
            if m:
                el["href"] = PAGES[m.group(1)]["en"] + (m.group(2) or "")
        for attr in ("src", "href", "poster"):
            for el in soup.find_all(attrs={attr: True}):
                if el[attr].startswith(ASSET_DIRS):
                    el[attr] = "../" + el[attr]

    # 5. Versione dei file condivisi, perché i browser non usino copie vecchie.
    for el in soup.find_all(["link", "script"]):
        for attr in ("href", "src"):
            v = el.get(attr, "")
            base = v.split("?")[0]
            for asset in ("assets/style.css", "assets/site.js"):
                if base.endswith(asset):
                    el[attr] = f"{base}?v={version(asset)}"

    # 6. Intestazione: titolo, descrizione, anteprime social, canonical, hreflang.
    head = soup.head
    title, desc = meta[lang + "_title"], meta[lang + "_desc"]
    head.title.string = title

    def set_meta(key, val, value):
        tag = head.find("meta", attrs={key: val})
        if tag is None:
            errors.append(f"{name}: manca <meta {key}={val!r}>")
        else:
            tag["content"] = value

    set_meta("name", "description", desc)
    set_meta("property", "og:title", title)
    set_meta("property", "og:description", desc)
    set_meta("property", "og:url", url(lang, name))
    set_meta("property", "og:locale", "it_IT" if lang == "it" else "en_GB")
    set_meta("property", "og:locale:alternate", "en_GB" if lang == "it" else "it_IT")
    canonical = head.find("link", rel="canonical")
    canonical["href"] = url(lang, name)
    for old in head.find_all("link", rel="alternate"):
        old.decompose()
    anchor = canonical
    for code, href in (("it", url("it", name)), ("en", url("en", name)), ("x-default", url("en", name))):
        link = soup.new_tag("link", rel="alternate", hreflang=code, href=href)
        anchor.insert_after(link)
        anchor.insert_after("\n")
        anchor = link
    if lang == "en":
        for script in head.find_all("script", type="application/ld+json"):
            data = json.loads(script.string)
            if data.get("@type") == "Organization":
                data["description"] = ORG_DESC_EN
            script.string = json.dumps(data, ensure_ascii=False)

    # 7. Avviso per chi apre il file generato.
    for c in soup.find_all(string=lambda s: isinstance(s, Comment) and "tools/build.py" in s):
        c.extract()
    head.insert(0, Comment(NOTICE.format(name)))

    leftover = soup.body.find_all(attrs={"lang": other})
    if leftover:
        errors.append(f"{name} ({lang}): restano elementi nell'altra lingua: {leftover[:3]}")
    return soup.decode(formatter=KeepOrder()), errors


def sitemap():
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for name in PAGES:
        if 'content="noindex"' in (SRC / name).read_text(encoding="utf-8"):
            continue
        for lang in ("it", "en"):
            out.append(f"  <url><loc>{url(lang, name)}</loc>")
            for code, href in (("it", url("it", name)), ("en", url("en", name)), ("x-default", url("en", name))):
                out.append(f'    <xhtml:link rel="alternate" hreflang="{code}" href="{href}"/>')
            out.append("  </url>")
    out.append("</urlset>")
    return "\n".join(out) + "\n"


def main():
    check = "--check" in sys.argv
    sources = sorted(p.name for p in SRC.glob("*.html"))
    errors = [f"src/{s}: pagina senza voce in tools/i18n.py" for s in sources if s not in PAGES]
    errors += [f"tools/i18n.py: {p} non esiste in src/" for p in PAGES if p not in sources]
    outputs = {}
    for name in PAGES:
        if name not in sources:
            continue
        for lang in ("it", "en"):
            html, errs = build_page(name, lang)
            errors += errs
            target = name if lang == "it" else "en/" + PAGES[name]["en"]
            outputs[target] = html
    outputs["sitemap.xml"] = sitemap()
    if errors:
        print("\n".join(errors))
        sys.exit(1)
    stale = []
    for target, content in outputs.items():
        path = ROOT / target
        if check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(target)
        else:
            path.parent.mkdir(exist_ok=True)
            path.write_text(content, encoding="utf-8")
    if check and stale:
        print("Pagine non aggiornate (lanciare python3 tools/build.py):\n  " + "\n  ".join(stale))
        sys.exit(1)
    print(f"{'Controllate' if check else 'Scritte'} {len(outputs)} pagine.")


if __name__ == "__main__":
    main()
