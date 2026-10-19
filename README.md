# Salvatore Sinatra — Web Identity 2.0

**Fotografia · Arti visive · Direzione creativa · Formazione · Creative Technology · Digital Identity Atlas**

Repository editoriale multipagina di Salvatore Sinatra. I contenuti originali e le loro eventuali riproduzioni rimangono tutelati dalle rispettive condizioni di copyright.

## Architettura del progetto

| Sezione | Percorso | Funzione |
| --- | --- | --- |
| Home | `docs/index.html` | Identità generale e portale editoriale |
| Profilo | `docs/identity/` | Biografia e formazione |
| Portfolio fotografico | `docs/professional/` | Linguaggio e attività fotografiche |
| Formazione | `docs/academic/` | Studi e interessi interdisciplinari |
| LuceVision | `docs/lucevision/` | Ricerca visiva e direzione creativa |
| Visual Arts | `docs/visual-arts/` | Disegno, grafica d'arte, opere |
| Creative Technology | `docs/creative-technology/` | Web, design, imaging e processi |
| Digital Identity Atlas | `docs/identity-atlas/` | Profilo interdisciplinare e directory |
| Site Tree | `docs/site-tree/` | Mappa interattiva ricercabile e filtrabile |

## Design system

Le pagine costruite con il layout editoriale condiviso utilizzano:
- `docs/assets/style.css` — base originale e layout responsive;
- `docs/assets/identity-v2.css` — componenti, griglie e temi monocromatici;
- `docs/assets/identity-v2.js` — selezione tema persistente e accessibile;
- `docs/assets/portfolio-system.css` — stile dedicato delle pagine portfolio esistenti.

Il progetto non usa framework JavaScript o dipendenze di build. Sono rispettate le preferenze di movimento ridotto e la navigazione da tastiera. Alcune pagine storiche mantengono un'identità stilistica dedicata.

## Pubblicazione GitHub e Netlify

**Branch sorgente:** `main`  
**Directory pubblica:** `docs`  
**Comando build:** nessuno.

Netlify Preview: https://salvatoresinatra-atlas-preview.netlify.app/

La configurazione è dichiarata nel file `netlify.toml` alla radice. Ogni commit destinato alla pubblicazione deve essere verificato sia sul repository sia sul deploy corrente; il semplice push non prova che il sito pubblico sia stato aggiornato.

GitHub Pages (se abilitato nelle impostazioni del repository): usare `main` → `/docs`. Gli indirizzi GitHub Pages non vengono descritti come attivi senza verifica.

## Rigore editoriale

- Fotografie autentiche, opere d'arte e immagini sintetiche devono essere distinguibili.
- Non si usano fotografie AI come riproduzioni documentarie di opere reali.
- Titoli accademici, riconoscimenti e periodi formativi non documentati non vengono presentati come certificati.
- Un dominio o progetto in preparazione non va etichettato come sito online verificato.
- Per le schede delle opere sono richiesti provenienza, tecnica, dimensioni, data e fotografia dell'originale quando disponibili.

## Progetti originali su Sites

Questa edizione è un adattamento editoriale statico e non un'esportazione integrale dei sorgenti o delle gallerie originali.

- Fotografia & Arti Visive: https://salvatore-sinatra.free-trail-0346.chatgpt.site
- LuceVision: https://salvatore-sinatra-lucevision.free-trail-0346.chatgpt.site
- Digital Identity Atlas: https://salvatore-sinatra-identity-atlas.free-trail-0346.chatgpt.site

© 2026 Salvatore Sinatra. Tutti i diritti riservati sulle opere originali salvo diversa indicazione.
