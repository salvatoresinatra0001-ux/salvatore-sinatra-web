# Release notes — Digital Identity Atlas V500

## V500.1 — Hardening e pubblicazione aggiuntiva

- CSS e JavaScript separati in asset statici locali per caching e compatibilità con CSP.
- Ritratto estratto in un JPEG statico e riutilizzato per anteprima social, eliminando due grandi data URI dall'HTML.
- Metadati canonical, Open Graph e Twitter Card uniformati e deduplicati.
- Dati strutturati Schema.org per persona, sito e pagina, senza aggiungere titoli o riconoscimenti non documentati.
- Attributi di stile inline convertiti in classi CSS per mantenere una CSP restrittiva.
- Robots e sitemap Netlify specifici per il route V500, senza mescolare nel sitemap le URL canoniche del sito GitHub Pages.
- La pagina resta una release aggiuntiva, non sostituisce il sito esistente né i precedenti archivi.
