# SEO Master System — Salvatore Sinatra

**Versione:** 1.0 · **Data:** 19 ottobre 2026  
**Modalità:** inventario centralizzato e audit statico non distruttivo.

## Obiettivo

Applicare uno standard SEO tecnico, editoriale e di controllo ripetibile a siti personali, portfolio fotografici, Webflow, Netlify, GitHub Pages e repository con contenuti pubblicati. Ogni proprietà conserva il proprio ruolo e il proprio dominio: non si presume che l'intero ecosistema debba diventare un solo sito.

## File di sistema

- `seo-sites.json`: inventario dei target, repository e directory pubblicate da esaminare.
- `scripts/seo_audit.py`: scanner statico senza dipendenze esterne per HTML, metadati e sitemap.
- `.github/workflows/seo-audit.yml`: scansione pianificata e su modifica del framework.
- `seo-sites.json` è descrittivo: un dominio indicato come candidato non è una certificazione di DNS, HTTPS, proprietà o indicizzazione.

## Perimetro

Il primo inventario distingue:

1. **Identità principale:** repository `salvatoresinatra`, deploy Netlify `salvatoresinatra-production`; il dominio personalizzato `www.salvatoresinatra.it` è ancora da certificare end-to-end.
2. **Archivio italiano con trattini:** `www.salvatore-sinatra.it`, proprietà distinta da `salvatoresinatra.it`.
3. **Portfolio fotografico:** `salvatoresinatraphotography`, più altri progetti/domini fotografici che devono essere mappati prima di uniformare canonical o redirect.
4. **Hub e archivi editoriali:** GitHub Pages e progetti musicali indipendenti, con canonical coerenti con il rispettivo hosting definitivo.
5. **Repository non web:** il profilo README GitHub è inventariato ma escluso dallo scanner HTML.

L'inventario tecnico non equivale alla verifica completa di tutti i domini pubblici. Le proprietà amministrative e i progetti con hosting multiplo devono avere un proprietario, un ruolo editoriale e un dominio canonico approvato.

### Altre proprietà Netlify individuate nel workspace

Le seguenti proprietà Netlify sono presenti nell'account collegato, ma non sono ancora abbinate con certezza al repository e al ref che generano la versione pubblicata. Sono quindi registrate nel file JSON ma non sottoposte a scansione della sorgente finché la mappatura non è verificata:

- Portfolio Netlify `salvatoresinatra-portfolio.it` / progetto `salvatore-sinatra-fine-art-authorial` (dominio riportato da Netlify in HTTP; la variante HTTPS con www va verificata).
- Preview `salvatoresinatra-atlas-preview.netlify.app`: confermare che l'accesso non pubblico impedisca l'indicizzazione e che il preview non confluisca nelle sitemap di produzione.
- `salvatoresinatra-artista.eu`.
- `www.salvatoresinatraphotography.net`.
- `www.salvatoresinatraphotography.online`.
- `www.alizee-moilolita.it`.
- `www.sandra-music-italia.it`: esiste una cartella con nome corrispondente in `music-archives-italia`, ma non è ancora provato che sia la base directory collegata al progetto Netlify.

Il sistema contiene quindi **22 record inventariati**: **13 root di sorgente sono configurate per l'audit automatico**, **7 proprietà Netlify attendono una verifica di sorgente/ref/base directory**, **1 record è il profilo README GitHub** (non è un sito HTML tradizionale) e **1 record è il sito Webflow**, inserito nell'inventario ma da controllare tramite le impostazioni native Webflow. Il sito Webflow non ha ancora un dominio personalizzato collegato; la homepage è pubblicata, mentre `/home-v2-editoriale` è una bozza. La homepage ha i campi SEO title/description, ma l'immagine Open Graph non risulta impostata. Una proprietà non ancora mappata non viene dichiarata “SEO verificata”.

## Risultati preliminari verificati nei sorgenti

- `salvatoresinatra/index.html`: title, description, lingua `it`, canonical e markup JSON-LD presenti; sitemap di sole due URL (home e privacy), da confrontare con le pagine effettivamente indicizzabili.
- `salvatore-sinatra-it/index.html`: title, description e canonical presenti; manca Open Graph image ed è assente JSON-LD nell'HTML esaminato.
- `salvatoresinatraphotography/index.html`: title, description e canonical presenti; nell'HTML esaminato non risultano Open Graph image né JSON-LD.
- `salvatoresinatra0001-ux.github.io/index.html`: la sorgente contiene 22 H1 e la sitemap include solo due URL. Sono rilievi da verificare semanticamente; uno schema con molte sezioni non è automaticamente un errore, ma una gerarchia di heading poco chiara può compromettere l'accessibilità.
- `heartagram-italia/index.html`: il canonical punta al percorso GitHub Pages `salvatoresinatra0001-ux.github.io/heartagram-italia/`, mentre è presente anche un progetto Netlify indipendente. Occorre decidere quale deploy è autorevole; non va risolto con un redirect automatico.
- `mylenefarmer-italia`: `robots.txt` e sitemap sono presenti; la sitemap contiene 14 URL e `lastmod`. Netlify pubblica `dist/`, mentre lo scanner iniziale legge i file sorgente nella root: una scansione post-build deve essere aggiunta quando la build è riproducibile.
- `sandra-italia`: canonical e voci sitemap usano in parte `index.html`; da valutare il percorso canonico preferito e l'eventuale coerenza delle versioni clean URL.
- Alcuni progetti non hanno ancora un URL pubblico confermato nell'inventario e restano marcati come provvisori. Non si attribuisce un canonical a un host non confermato.

Le verifiche sopra sono ispezioni del codice sorgente, non prove di indicizzazione Google, prestazioni Lighthouse o comportamento HTTP corrente.

## Standard dell'audit

### Tecnico
- singolo canonical assoluto per pagina e dominio coerente con la decisione editoriale;
- `robots.txt` raggiungibile e senza blocchi globali involontari;
- sitemap XML valida, con URL assoluti, univoci e canonici, limitata alle pagine che si desidera proporre per l'indicizzazione;
- coerenza tra host HTTPS, sitemap, canonical e redirect;
- link e asset interni che risolvano nel contesto di pubblicazione;
- assenza di `noindex` involontari e di pagine di anteprima esposte all'indicizzazione;
- status code, redirect chain, pagine 404, rendering e accessibilità da controllare anche dal sito pubblicato.

### Contenuti e metadata
- title unici, descrittivi e concisi;
- meta description specifiche della pagina, senza keyword stuffing;
- un argomento primario e una gerarchia di heading comprensibile;
- Open Graph coerente con la pagina e con un'immagine social valida;
- alt text descrittivi per immagini informative e alt vuoto per immagini decorative;
- dati strutturati JSON-LD validi e coerenti con informazioni realmente presenti nella pagina;
- contenuti distinti per ciascun sito, con link contestuali tra proprietà che abbiano davvero un rapporto editoriale;
- fonti, crediti, date e diritti fotografici verificati, soprattutto negli archivi musicali.

### Fotografia Fine Art
- non sostituire mai master fotografici o immagini originali;
- conservare i nomi dei file e i metadati necessari ai crediti e all'archivio;
- nominare le copie derivate in modo descrittivo e utilizzare alt text pertinenti alla fotografia, non sequenze di keyword;
- verificare risoluzioni, compressione, formati moderni, dimensioni responsive e caricamento differito senza compromettere la qualità;
- non usare immagini sintetiche come sostituti di opere fotografiche autentiche.

### Misurazione
Per ogni dominio verificato: Google Search Console, sitemap inviata, pagine indicizzate, query e click organici, query brand vs non-brand, Core Web Vitals e conversioni rilevanti. Le impressioni/click vanno confrontate su intervalli omogenei; la presenza di codice SEO non garantisce ranking.

## Priorità

- **P0 — decisioni canoniche e host:** distinguere `salvatoresinatra.it` da `salvatore-sinatra.it`; certificare DNS/SSL, canonical e redirect prima di cambiare i domini; individuare le proprietà Netlify che pubblicano lo stesso codice o versioni diverse.
- **P1 — scansione e indicizzazione:** validare tutte le sitemap, assicurare che includano le pagine giuste e corrispondano alle canonical; verificare robots, noindex, anteprime e risposte HTTP.
- **P1 — contenuto SEO:** title, description, heading, immagini social, alt text e collegamenti interni sulle pagine importanti.
- **P2 — performance e accessibilità:** Lighthouse, Core Web Vitals, contrasto, navigazione da tastiera, immagini responsive e JavaScript.
- **P2 — autorità identitaria:** profili esterni verificati, biografie coerenti, riferimenti incrociati editorialmente motivati e dati strutturati appropriati.

## Esecuzione locale

Da una copia del repository:

```bash
python3 scripts/seo_audit.py --root docs
```

Per fare il check anche sui riferimenti locali:

```bash
python3 scripts/seo_audit.py --root docs --check-links
```

Usare la directory di pubblicazione reale come `--root`. Per i progetti che costruiscono `dist/`, eseguire prima la build e poi analizzare `dist/`. La scansione statica non controlla richieste HTTP esterne, DNS, certificati, dati di Search Console o Core Web Vitals reali.

## Controlli manuali necessari prima di ogni rilascio

- [ ] Confermare il repository, branch/ref e directory di publish attivi.
- [ ] Confermare dominio primario, varianti www/apex e URL canonici.
- [ ] Verificare HTTPS, status 200, redirect e sitemap pubblicata.
- [ ] Assicurarsi che i deploy preview siano bloccati dall'indicizzazione e non entrino nella sitemap.
- [ ] Testare le pagine dopo la pubblicazione su desktop e dispositivi mobili.
- [ ] Consultare Search Console e gli strumenti ufficiali per dati strutturati, performance e indicizzazione.
- [ ] Creare backup/commit di rollback prima di ogni modifica ai contenuti o alle configurazioni di routing.

## Riferimenti ufficiali

- [Guida introduttiva SEO di Google Search Central](https://developers.google.com/search/docs/fundamentals/seo-starter-guide)
- [Creare e inviare una sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap)
- [Canonical e consolidamento di URL duplicati](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls)

**Vincolo di sicurezza:** il framework è in sola lettura verso le proprietà web. Nessuna pubblicazione, migrazione, modifica DNS, rimozione di pagine, riscrittura di canonical o redirect viene eseguita automaticamente.
