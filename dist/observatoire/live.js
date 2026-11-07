import {uencLayout,allocate} from './models.js';
const roles={input:'Le document arrive en blocs de 64 Kio maximum.',aad:'L’en-tête de 14 octets est authentifié comme données associées (AAD).',nonce:'Nonce : préfixe aléatoire de 7 octets, compteur de 4 et drapeau final de 1.',seal:'Chaque bloc reçoit un tag de 16 octets. Cette animation ne chiffre rien.',tag:'Le bloc final porte last = 1. Même un fichier vide produit un bloc authentifié.',gate:'Répartition du surplus après provision et prime, en centimes entiers.',tax:'Provision marginale sur le cumul de l’exercice, avec les taux configurés dans le logiciel.',bonus:'Prime par défaut : 1 % du net, arrondie à l’inférieur.',cash:'Trésorerie : un tiers du reste et les centimes de division.',rnd:'Recherche et développement : un tiers entier du reste.',assets:'Actifs durables : un tiers entier du reste.'};
for(const model of document.querySelectorAll('[data-model]')){
 const output=model.querySelector('output'),figure=model.querySelector('figure'),controls=model.querySelector('.inspect-buttons');
 const parts=[...model.querySelectorAll('[data-component]')];
 const names=[...new Set(parts.map(p=>p.dataset.component))];
 for(const name of names){
  const button=document.createElement('button');button.type='button';button.textContent=name;
  const inspect=()=>{
   parts.forEach(p=>p.classList.toggle('selected',p.dataset.component===name));
   const part=parts.find(p=>p.dataset.component===name);
   model.querySelector('[data-inspector]').textContent=roles[name]+' Source : '+part.dataset.file+' · '+part.dataset.symbol;
   const source=model.querySelector('[data-source]');
   // Le commit est celui des liens de référence dans la même section.
   const first=model.closest('section').querySelector('details a').href;
   const commit=first.split('/blob/')[1].split('/')[0];
   source.href='https://github.com/papiche/astroportd/blob/'+commit+'/'+part.dataset.file;
   source.textContent=part.dataset.crate+' / '+part.dataset.symbol+' ↗';
  };
  button.addEventListener('click',inspect);controls.append(button);
  parts.filter(p=>p.dataset.component===name).forEach(p=>p.addEventListener('click',inspect));
 }
 function calculate(){
  if(model.dataset.stale==='true'){output.textContent='Source modifiée : modèle à revalider.';return;}
  try{
   if(model.dataset.model==='uenc'){
    const raw=document.getElementById('uenc-size').value;if(!/^\d+$/.test(raw))throw Error('Entier positif ou nul attendu.');
    const m=uencLayout(Number(raw));output.textContent=`${m.size} octets → ${m.chunks} bloc(s) ; ${m.header} octets d’en-tête + ${m.tags} octets de tags ; blob total ${m.total} octets. Nonce : ${m.nonce} octets (7 + 4 + 1).`;
   }else{
    const read=id=>{const s=document.getElementById(id).value;if(!/^\d{1,20}$/.test(s))throw Error('Entiers positifs ou nuls en centimes attendus.');return BigInt(s);};
    const a=allocate(read('surplus'),read('ytd'));
    output.textContent=`Surplus ${a.surplus} c = provision ${a.tax} c + prime ${a.bonus} c + trésorerie ${a.cash} c + R&D ${a.rnd} c + actifs ${a.assets} c. Total conservé : ${a.tax+a.bonus+a.cash+a.rnd+a.assets} c.`;
   }
  }catch(e){output.textContent=e.message;}
 }
 model.querySelector('[data-calculate]').addEventListener('click',calculate);calculate();
 const motion=model.querySelector('[data-motion]');motion.addEventListener('click',()=>{const on=figure.classList.toggle('running');motion.setAttribute('aria-pressed',String(on));motion.textContent=on?'Arrêter la mécanique':'Animer la mécanique';});
 if('IntersectionObserver' in window)new IntersectionObserver(entries=>figure.classList.toggle('paused',!entries[entries.length-1].isIntersecting)).observe(figure);
 document.addEventListener('visibilitychange',()=>figure.classList.toggle('hidden-page',document.hidden));
}
