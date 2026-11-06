'use strict';
(async function(){
const modes=[['Un espace pour vos fichiers.','uCloud propose un stockage personnel chiffré, accessible dans le navigateur et avec un client WebDAV.'],['Des photos à partager avec ses proches.','FaceCloud propose la recherche par visage et le partage chiffré. Un moteur de reconnaissance et ses modèles doivent être configurés.'],['La coopération, avec un accord.','Un proche peut accepter une sauvegarde chiffrée. Sa disponibilité et vos clés de secours conditionnent la restauration.']];
function select(index){document.querySelectorAll('[data-mode]').forEach(b=>b.setAttribute('aria-pressed',String(Number(b.dataset.mode)===index)));document.querySelectorAll('[data-drawer]').forEach(d=>d.classList.toggle('active',Number(d.dataset.drawer)===index));document.getElementById('figure-title').textContent=modes[index][0];document.getElementById('figure-description').textContent=modes[index][1];}
document.querySelectorAll('[data-mode]').forEach(button=>button.addEventListener('click',()=>select(Number(button.dataset.mode))));select(0);
})();
