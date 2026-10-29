# Porta dell'ecosistema — requisiti di pubblicazione

Questa pagina aggrega soltanto URL pubblici dei sei siti autonomi. Non è un sistema di autenticazione. Il ramo di lavoro NON deve essere distribuito come una pagina riservata finché l'hosting non richiede un'autenticazione reale.

## Identità amministrativa e controllo di accesso: MASTER SINGLE-OWNER

**Politica obbligatoria:** un solo account umano autorizzato, intestato al titolare Salvatore Sinatra, con ruolo di **MASTER ADMIN**. L'accesso al Gateway (HTML, CSS, JS, asset e API di gestione) deve essere rifiutato per impostazione predefinita a chiunque non sia autenticato e autorizzato come questo unico amministratore. Non creare account ospiti, inviti, registrazioni pubbliche, account di prova, password condivise o bypass amministrativi nel frontend. L'accesso a un URL da solo non costituisce autorizzazione.

**Autenticazione raccomandata:** passkey/WebAuthn, protetta da biometria o PIN locale del dispositivo, per l'unico account master. L'eventuale verifica SMS deve avvenire attraverso un servizio server-side affidabile e il solo recapito approvato dal titolare, registrato esclusivamente nella configurazione privata dell'identity provider. SMS/OTP da solo non è prova che il richiedente sia il titolare e non è resistente al phishing; non considerarlo sufficiente per un requisito di esclusività personale. Consentire passkey registrate su più dispositivi posseduti dal titolare; prevedere elenco delle sessioni autorizzate, scadenza delle sessioni, logout remoto e revoca delle credenziali perdute.

**Autorizzazione e funzioni:** l'ID unico dell'account master deve essere assegnato dal provider di autenticazione in una allowlist lato server. Ogni richiesta al portale e a eventuali servizi di monitoraggio deve essere verificata lato hosting/server; le chiamate non autorizzate devono essere respinte prima di servire il contenuto protetto. Il controllo di ruolo solo in JavaScript non è sufficiente. I sei siti pubblici restano indipendenti, accessibili secondo le proprie impostazioni, senza fare ereditare loro le restrizioni del Gateway.

**Vincolo prima della pubblicazione:** il progetto è attualmente soltanto un frontend statico su ramo GitHub. È **vietato promuoverlo o pubblicarlo come accesso privato** finché non siano operativi: fornitore d'identità, unico master registrato e verificato, autorizzazione server-side, blocco di utenti sconosciuti, test in navigazione anonima, test su dispositivi autorizzati e prova di revoca. Per hosting Netlify, una password unica condivisibile non soddisfa l'identificazione personale; anche la protezione con login di team autorizza tutti i membri ammessi, non necessariamente un solo titolare. Non impostarla come soluzione definitiva senza controllare la composizione del team.

**Gestione dei dati:** nessun numero completo, PIN, OTP, token di accesso, lista di device, chiave privata o codice di recupero deve essere scritto nel repository, negli HTML, nei log pubblici o nel contenuto della pagina. I segreti devono rimanere nei sistemi privati del servizio di autenticazione; le impostazioni di accesso si gestiscono tramite interfacce protette.

## Accesso con un solo recapito telefonico autorizzato

È necessaria un'autenticazione telefonica OTP via servizio affidabile: il numero autorizzato va registrato nella configurazione privata del provider, NON nel codice GitHub o nel frontend. Le sessioni dei dispositivi devono poter essere visualizzate e revocate. Un numero associato a un dispositivo non conferisce automaticamente accesso ad altri device; la verifica tramite SMS deve essere esplicita. Password o SSO Netlify possono fornire un controllo d'accesso provvisorio, ma non sono autenticazione SMS.

Non memorizzare numeri di telefono, token, OTP, PIN o credenziali nei file statici. Meta robots noindex non è una protezione.

## Architettura

- docs/accesso/index.html: catalogo dei punti di approdo
- docs/accesso/gateway.css: design responsivo, monocromatico
- docs/accesso/gateway.js: ricerca, filtri, copia URL e tema chiaro/scuro

Nessun controllo HTTP o TLS dal browser viene simulato. Per un vero check-up si usano server o connettori autorizzati. Testare l'autenticazione prima del deploy. Non modificare i sei siti pubblici per pubblicare questo portale.
