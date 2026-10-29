# Porta dell'ecosistema — requisiti di pubblicazione

Questa pagina aggrega soltanto URL pubblici dei sei siti autonomi. Non è un sistema di autenticazione. Il ramo di lavoro NON deve essere distribuito come una pagina riservata finché l'hosting non richiede un'autenticazione reale.

## Accesso con un solo recapito telefonico autorizzato

È necessaria un'autenticazione telefonica OTP via servizio affidabile: il numero autorizzato va registrato nella configurazione privata del provider, NON nel codice GitHub o nel frontend. Le sessioni dei dispositivi devono poter essere visualizzate e revocate. Un numero associato a un dispositivo non conferisce automaticamente accesso ad altri device; la verifica tramite SMS deve essere esplicita. Password o SSO Netlify possono fornire un controllo d'accesso provvisorio, ma non sono autenticazione SMS.

Non memorizzare numeri di telefono, token, OTP, PIN o credenziali nei file statici. Meta robots noindex non è una protezione.

## Architettura

- docs/accesso/index.html: catalogo dei punti di approdo
- docs/accesso/gateway.css: design responsivo, monocromatico
- docs/accesso/gateway.js: ricerca, filtri, copia URL e tema chiaro/scuro

Nessun controllo HTTP o TLS dal browser viene simulato. Per un vero check-up si usano server o connettori autorizzati. Testare l'autenticazione prima del deploy. Non modificare i sei siti pubblici per pubblicare questo portale.
