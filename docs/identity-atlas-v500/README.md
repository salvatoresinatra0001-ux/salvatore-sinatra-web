# Salvatore Sinatra — Digital Identity Atlas V500.1

Release statica responsive e autonoma come sezione aggiuntiva, mantenuta distinta dalla homepage esistente.

## Pubblicazione

- Percorso: `/identity-atlas-v500/`
- Landing: `index.html`
- CSS e JavaScript locali: `atlas.css`, `atlas.js`
- Ritratto fotografico autentico e anteprima social: `portrait.jpg`
- Nessun framework o passaggio di build richiesto.
- Tema iniziale Soft Minimal Light; alternativa Dark Black AMOLED.

## Contenuto e separazione editoriale

La pagina organizza identità personale, fotografia, ricerca visiva, profili e directory. Assemblage 23 Italia e The Birthday Massacre Italia sono indicati come progetti editoriali italiani indipendenti, distinti dai siti internazionali ufficiali. Non vengono dichiarate affiliazioni non documentate.

## SEO, prestazioni e sicurezza

- Canonical, robots, Open Graph, Twitter Card e dati strutturati Schema.org.
- Immagine del ritratto esternalizzata in un file JPEG riutilizzabile, non duplicata nel markup.
- CSS e JavaScript serviti come asset locali per consentire una Content Security Policy restrittiva.
- Sitemap Netlify dedicata al solo URL canonico V500; il sitemap GitHub Pages mantiene il proprio host.
- Le otto dichiarazioni di stile inline sono convertite in classi CSS.
- Link esterni con protezioni `noopener noreferrer` dove previsti; nessun token o credenziale inclusa.

## Diritti

© 2026 Salvatore Sinatra per i contenuti originali propri. I materiali e i marchi di terzi restano dei rispettivi titolari. Nessuna licenza open-source viene assegnata automaticamente.

## Prossima integrazione

La versione destinata al sito personale ufficiale viene pubblicata separatamente nel repository di produzione, sotto lo stesso percorso, senza sostituire la homepage. La raggiungibilità del dominio `www` e il certificato TLS devono essere verificati end-to-end sul provider.
