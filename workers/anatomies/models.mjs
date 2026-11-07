// Modèles pédagogiques portés du commit indiqué dans catalog.json.
// Aucun secret, chiffrement, transfert réseau ou transaction réelle.
export function uencLayout(size){
 if(!Number.isSafeInteger(size)||size<0||size>1073741824)throw new RangeError('Taille de démonstration : 0 à 1 Gio.');
 const chunks=Math.max(1,Math.ceil(size/65536));
 return {size,chunks,header:14,tags:chunks*16,total:14+size+chunks*16,nonce:12,prefix:7,counter:4,last:1};
}
export function allocate(surplus,ytd=0n){
 if(typeof surplus!=='bigint'||typeof ytd!=='bigint'||surplus<0n||ytd<0n||surplus+ytd>18446744073709551615n)throw new RangeError('Montants u64 en centimes attendus.');
 const due=p=>((p<4250000n?p:4250000n)*1500n+(p>4250000n?p-4250000n:0n)*2500n)/10000n;
 const tax=due(ytd+surplus)-due(ytd),net=surplus-tax,bonus=net*100n/10000n,rest=net-bonus,third=rest/3n;
 return {surplus,tax,net,bonus,cash:rest-2n*third,rnd:third,assets:third};
}
