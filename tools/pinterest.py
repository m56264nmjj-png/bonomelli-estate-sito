#!/usr/bin/env python3
"""Genera pinterest.xml: l'elenco (feed RSS) che Pinterest legge per creare i Pin da solo.

    python3 tools/pinterest.py

Per aggiungere un Pin: una riga nuova in PIN (in cima), poi rilanciare lo script.
Regole (note di Brenda): nel titolo prima il nome dell'opera, poi le parole cercate in inglese;
© su ogni immagine; «Render concept · design di Brenda Bonomelli»; EUIPO solo per la Serra dei Sogni;
mai prezzi. Le immagini dei Pin stanno in img/pin/ (verticali, JPEG).
"""
import pathlib
from email.utils import format_datetime
from datetime import datetime, timezone
from xml.sax.saxutils import escape

SITE = "https://bonomelliestate.com/"
ROOT = pathlib.Path(__file__).resolve().parent.parent
FIRMA = "Disegno registrato UE · EUIPO n. 015156041 / Registered EU design. Render concept · design di Brenda Bonomelli."
SERRA = "serra-dei-sogni.html"

# (data, immagine, titolo, descrizione, pagina)
PIN = [
    # I quattro Pin di Natale sono stati tolti il 21/11: il pavimento a mosaico non era quello giusto.
    # Si rimettono quando le immagini di Natale sono rifatte con i pavimenti veri (img/*-alto.webp).
    ("2026-11-21", "serra-glicine.jpg", "Serra Glicine · Bonomelli Estate | Wisteria stained glass greenhouse, iron and glass orangery",
     "Serra dei Sogni, versione Glicine: galleria ad archi in ferro brunito e vetro, vetrate a glicine e pavimento a mosaico di ciottoli Via Florae. Su commissione privata. A bespoke iron and glass greenhouse with wisteria stained glass.", SERRA),
    ("2026-11-21", "serra-giglio.jpg", "Serra Giglio · Bonomelli Estate | Lily stained glass conservatory, luxury garden",
     "Serra dei Sogni, versione Giglio: archi in ferro brunito, vetrate a gigli, mosaico di ciottoli. Su commissione privata. A bespoke conservatory with lily stained glass and a pebble mosaic floor.", SERRA),
    ("2026-11-21", "serra-ortensia.jpg", "Serra Ortensia · Bonomelli Estate | Hydrangea stained glass greenhouse, winter garden",
     "Serra dei Sogni, versione Ortensia: una galleria vetrata tra serra vittoriana e orangerie, con le ortensie nel vetro e nel pavimento. Su commissione privata. A bespoke winter garden with hydrangea stained glass.", SERRA),
    ("2026-11-21", "serra-girasole.jpg", "Serra Girasole · Bonomelli Estate | Sunflower stained glass orangery, pebble mosaic floor",
     "Serra dei Sogni, versione Girasole: ferro brunito, vetro e girasoli nelle vetrate e nel mosaico. Su commissione privata. A bespoke iron and glass orangery with sunflower stained glass.", SERRA),
]


def main():
    voci = []
    for data, img, titolo, descr, pagina in PIN:
        f = ROOT / "img" / "pin" / img
        if not f.exists():
            raise SystemExit(f"Manca l'immagine img/pin/{img}")
        if len(titolo) > 100:
            raise SystemExit(f"Titolo oltre 100 caratteri: {titolo}")
        quando = format_datetime(datetime.fromisoformat(data).replace(hour=19, tzinfo=timezone.utc))
        link = SITE + pagina
        voci.append(
            "  <item>\n"
            f"    <title>{escape(titolo)}</title>\n"
            f"    <link>{escape(link)}</link>\n"
            f"    <guid isPermaLink=\"false\">{escape(SITE + 'img/pin/' + img)}</guid>\n"
            f"    <description>{escape(descr + ' ' + FIRMA)}</description>\n"
            f"    <pubDate>{quando}</pubDate>\n"
            f"    <enclosure url=\"{escape(SITE + 'img/pin/' + img)}\" length=\"{f.stat().st_size}\" type=\"image/jpeg\"/>\n"
            f"    <media:content url=\"{escape(SITE + 'img/pin/' + img)}\" medium=\"image\" type=\"image/jpeg\"/>\n"
            "  </item>\n"
        )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/" xmlns:atom="http://www.w3.org/2005/Atom">\n<channel>\n'
        "  <title>Bonomelli Estate · Serra dei Sogni</title>\n"
        f"  <link>{SITE}</link>\n"
        "  <description>Serre in ferro e vetro, padiglioni e arredi in pietra di Brenda Bonomelli.</description>\n"
        "  <language>it</language>\n"
        f'  <atom:link href="{SITE}pinterest.xml" rel="self" type="application/rss+xml"/>\n'
        + "".join(voci)
        + "</channel>\n</rss>\n"
    )
    (ROOT / "pinterest.xml").write_text(xml, encoding="utf-8")
    print(f"Scritto pinterest.xml con {len(voci)} Pin.")


if __name__ == "__main__":
    main()
