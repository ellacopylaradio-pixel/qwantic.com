'use strict';
const fig=document.querySelector('figure'),button=document.querySelector('#motion');
button.addEventListener('click',()=>{const running=fig.classList.toggle('running');button.setAttribute('aria-pressed',String(running));button.textContent=running?'Arrêter l’animation':'Animer les modules modifiés';});
if('IntersectionObserver' in window)new IntersectionObserver(entries=>fig.classList.toggle('paused',!entries[entries.length-1].isIntersecting)).observe(fig);
document.addEventListener('visibilitychange',()=>fig.classList.toggle('paused',document.hidden));
