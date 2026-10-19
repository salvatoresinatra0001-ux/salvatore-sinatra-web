# Portfolio Netlify — v.10.1

Questo branch contiene una distribuzione statica autonoma del portfolio editoriale Salvatore Sinatra, predisposta per il progetto Netlify `salvatore-sinatra-fine-art-authorial`.

## Struttura della distribuzione
- `deploy/index.html` — pagina principale, metadati SEO/Open Graph e contenuti.
- `deploy/styles.css` — layout editoriale responsive.
- `deploy/script.js` — navigazione mobile e aggiornamento dell'anno.
- `netlify.toml` — directory di pubblicazione e intestazioni HTTP.

## Collegamento a Netlify
Nelle impostazioni del progetto Netlify esistente, collegare il repository GitHub `salvatoresinatra0001-ux/salvatore-sinatra-web` e impostare il branch di produzione su `netlify-portfolio-v10.1`. La directory di pubblicazione è già configurata a `deploy`; non è necessario un comando di build.

Questo collegamento non è stato eseguito via API da questa sessione. Dopo aver scelto branch e repository nel pannello Netlify, verificare che il deploy vada in stato Ready e provare l'URL .netlify.app prima di modificare il dominio definitivo.

## Fotografia
Il ritratto punta all'asset originale già presente nella libreria Webflow. Non è stato ritoccato, ritagliato, rigenerato o ricompresso. L'immagine usa il rapporto originale quadrato con `width: 100%`, `height: auto` e `object-fit: contain`.

## Regole di staging
- La pagina e le intestazioni indicano `noindex,nofollow` finché è in staging.
- Non sono stati modificati DNS, nameserver o dominio personalizzato.
- L'archivio è presentato come nuclei editoriali; non vengono inventate immagini di opere o gallerie.
- Prima della pubblicazione sul dominio definitivo, approvare i contenuti, testare desktop/mobile e aggiornare la regola noindex/canonical.

© 2026 Salvatore Sinatra. Tutti i diritti riservati sulle opere originali salvo diversa indicazione.
