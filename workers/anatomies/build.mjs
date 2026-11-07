import fs from 'node:fs';
import * as k from '../../vendor/anatomy/iso-kit.mjs';
const directory=process.argv[2], catalog=JSON.parse(fs.readFileSync(new URL('catalog.json',import.meta.url),'utf8'));
const frame={x:-130,y:-65,w:260,d:130,r:5};
const P=k.fitProjection(k.boxCorners({x:-140,y:-70,w:280,d:155,r:0},-10,105),760,450,{pad:35,azimuth:40,elevation:32});
const solid=(x,y,w,d,z,h,t='mid')=>k.solidSvg(k.slabOf({x,y,w,d,r:1.5},z,h,P,4,.6),{tone:t});
const point=(x,y,z)=>k.dotsSvg([k.iso([x,y,z],P)],{size:.6});
for(const id of ['uenc','economy']){
 const view=catalog.find(v=>v.id===id),ref=view.sources[0];
 let body='';let partCount=0;
 const S=(...a)=>{partCount++;return solid(...a);};
 for(const [x,y] of k.corners(frame,12))body+=S(x-4,y-4,8,8,-10,5,'lo');
 body+=S(-130,-65,260,130,-5,7,'lo');
 body+=k.lineSvg(k.planOutline(k.insetPlan(frame,5),2,P),{tone:'lo'});
 for(const [x,y] of k.corners(frame,8))body+=point(x,y,2)+S(x-1,y-1,2,2,2,.5,'hi');
 const annotate=(name,svg)=>`<g data-component="${name}" data-crate="${id==='uenc'?'astro-crypto':'astro-economy'}" data-file="${ref.file}" data-symbol="${id==='uenc'&&name==='nonce'?'nonce':ref.symbol}">${svg}</g>`;
 if(id==='uenc'){
  // Convoyeur, deux rails, six traverses ; presse à quatre montants, chapeau et poinçon.
  for(const y of [-15,20])body+=S(-115,y,225,4,2,5,'mid');
  for(let x=-105;x<110;x+=35)body+=S(x,-18,5,46,2,3,'lo');
  for(const x of [-25,25])for(const y of [-25,30])body+=S(x,y,5,5,2,70,'mid');
  body+=annotate('nonce',S(-32,-30,69,70,72,7,'hi'));
  for(let x=-20;x<24;x+=8)body+=S(x,-20,3,35,79,.5,'lo');
  body+=`<g class="press-head" data-part="seal">${annotate('seal',S(-18,-12,40,35,46,9,'hi'))}</g>`;
  for(let i=0;i<3;i++){
   let x=-102+i*75,part=S(x,-10,30,28,7,8,'hi');
   for(let n=0;n<4;n++)part+=S(x+4+n*6,-5,2,17,15,.3,'lo');
   if(i===2)part+=S(x+22,-10,8,28,15,2,'hi');
   body+=`<g class="parcel parcel-${i}">${annotate(['input','aad','tag'][i],part)}</g>`;
  }
  // Plateau de contrôle et deux boutons sur leur embase.
  body+=annotate('aad',S(-110,-55,55,22,2,10,'mid'));
  for(const x of [-100,-80])body+=S(x,-50,8,10,12,3,'hi');
 }else{
  // Répartiteur : glissières et palettes au-dessus de cinq bacs ouverts.
  for(const y of [-25,-18])body+=S(-115,y,232,4,2,5,'lo');
  body+=S(-23,-46,48,35,7,17,'hi');
  for(let x=-17;x<22;x+=7)body+=S(x,-42,2,21,24,.4,'lo');
  body+=`<g class="allocation-gate">${annotate('gate',S(-18,-10,38,12,11,5,'hi'))}</g>`;
  const compartments=['tax','bonus','cash','rnd','assets'];
  for(let i=0;i<5;i++){
   const x=-120+i*49;let bin=S(x,5,42,46,2,3,'lo');
   bin+=S(x,5,3,46,5,17)+S(x+39,5,3,46,5,17)+S(x,5,42,3,5,17)+S(x,48,42,3,5,17);
   bin+=S(x+6,14,30,27,5,2,'hi');
   for(let n=0;n<3;n++)bin+=S(x+8+n*8,19,5,16,7,.4,'lo');
   body+=annotate(compartments[i],bin);
  }
 }
 const label=id==='uenc'?'Presse de scellement UENC : convoyeur, blocs et sceau d’authentification.':'Répartiteur du surplus : provision, prime et trois compartiments.';
 fs.writeFileSync(directory+'/'+id+'-figure.html',k.figureSvg({width:760,height:450,label,body}));
 // Export SVG statique, stylage externe pour rester sans styles inline.
 fs.writeFileSync(directory+'/'+id+'.svg',`<?xml-stylesheet type="text/css" href="anatomy-kit.css"?>\n`+k.figureSvg({width:760,height:450,label,body,className:'iso'}));
 console.log(`${id} : ${partCount} solides, sources ${ref.file}#${ref.symbol}`);
}
