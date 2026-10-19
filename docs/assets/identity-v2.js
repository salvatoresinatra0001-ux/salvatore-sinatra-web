
/* Shared theme controller: accessible progressive enhancement, no external dependencies */
(()=>{'use strict';
const key='salvatore-identity-theme';
const body=document.body;
const buttons=[...document.querySelectorAll('[data-identity-theme-toggle]')];
let stored=null;
try{stored=localStorage.getItem(key)||localStorage.getItem('atlas-theme')}catch(_){}
const preferLight=window.matchMedia&&window.matchMedia('(prefers-color-scheme: light)').matches;
function apply(value){
 const theme=value==='light'?'light':'dark';body.dataset.theme=theme;
 document.documentElement.style.colorScheme=theme;
 const meta=document.querySelector('meta[name="theme-color"]');
 if(meta)meta.setAttribute('content',theme==='light'?'#f3f3ef':'#080808');
 buttons.forEach(b=>{b.textContent=theme==='light'?'Modalità scura':'Modalità chiara';b.setAttribute('aria-label','Attiva '+(theme==='light'?'la modalità scura':'la modalità chiara'));b.setAttribute('aria-pressed',String(theme==='light'))});
}
apply(stored==='light'||stored==='dark'?stored:(preferLight?'light':'dark'));
buttons.forEach(button=>button.addEventListener('click',()=>{
 const next=body.dataset.theme==='light'?'dark':'light';apply(next);
 try{localStorage.setItem(key,next);localStorage.setItem('atlas-theme',next)}catch(_){}
}));
})();
