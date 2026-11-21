# Sito Bonomelli Estate

Sito statico pubblicato con GitHub Pages su https://bonomelliestate.com (ramo `main`).

## Pagine in due lingue

- Le pagine si modificano **solo in `src/`**. Ogni file sorgente contiene entrambe le lingue
  (`<span lang="it">…</span><span lang="en">…</span>`).
- Dopo ogni modifica: `python3 tools/build.py`. Lo script scrive le pagine italiane alla
  radice e quelle inglesi in `en/` (con indirizzi inglesi, es. `en/pavilion-caelo.html`),
  più `sitemap.xml`. Non modificare a mano i file generati: verrebbero sovrascritti.
- Titoli, descrizioni e indirizzi inglesi di ogni pagina, e le traduzioni di `alt` e
  `aria-label`, stanno in `tools/i18n.py`. Una nuova pagina in `src/` va aggiunta lì,
  altrimenti lo script si ferma con un errore.
- `python3 tools/build.py --check` controlla che i file pubblicati siano aggiornati
  (lo esegue anche la GitHub Action "Controllo sito").

## Altro

- `jarvis/` è l'app privata di Brenda: non fa parte del sito pubblico e non passa dal build.
- Questo repository è pubblico tramite GitHub Pages: non salvarci note private o dati di clienti.

## Pinterest

- `pinterest.xml` è l'elenco (feed RSS) che Pinterest legge per creare i Pin da solo. Si genera con
  `python3 tools/pinterest.py`: per un Pin nuovo si aggiunge una riga in `PIN` dentro lo script e si rilancia.
- Le immagini dei Pin stanno in `img/pin/` (verticali, JPEG, con la firma ©).
- Il tag `p:domain_verify` nella home serve a Pinterest: non toglierlo.
