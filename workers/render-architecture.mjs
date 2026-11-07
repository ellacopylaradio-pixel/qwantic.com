import fs from 'node:fs';
import * as k from '../vendor/anatomy/iso-kit.mjs';
const dir=process.argv[2], report=JSON.parse(fs.readFileSync(dir+'/report.json','utf8'));
const modules=report.modules, rows=Math.ceil(modules.length/4);
const plans=modules.map((m,i)=>({x:(i%4)*80,y:Math.floor(i/4)*75,w:65,d:55,r:3}));
const P=k.fitProjection(plans.flatMap(p=>k.boxCorners(p,-6,32)),850,580,{pad:45,azimuth:40,elevation:34});
const solid=(p,z,h,t='mid')=>k.solidSvg(k.slabOf(p,z,h,P,4,.6),{tone:t});
let pieces=[];
modules.forEach((m,i)=>{
 const p=plans[i];let svg='';
 // Socle, 4 pieds, 2 rails, tiroir, façade, poignée et attaches, couvercle, vis et ventilation.
 for(const [x,y] of k.corners(p,6))svg+=solid({x:x-2,y:y-2,w:4,d:4,r:.5},-6,3,'lo');
 svg+=solid(p,-3,5,'lo');
 for(const x of [p.x+4,p.x+55])svg+=solid({x,y:p.y+4,w:4,d:45,r:1},2,3,'lo');
 let moving=solid({x:p.x+9,y:p.y+5,w:47,d:44,r:2},5,12,m.changed_files?'hi':'mid');
 moving+=solid({x:p.x+7,y:p.y+47,w:51,d:4,r:1},5,17,m.changed_files?'hi':'mid');
 for(const x of [p.x+19,p.x+43])moving+=solid({x,y:p.y+51,w:3,d:4,r:.5},10,4);
 moving+=solid({x:p.x+19,y:p.y+55,w:27,d:3,r:.6},10,4,'hi');
 const a=k.iso([0,0,0],P),b=k.iso([0,9,0],P);
 svg+=`<g class="module-drawer${m.changed_files?' changed':''}" style="--dx:${b[0]-a[0]}px;--dy:${b[1]-a[1]}px;--delay:${i*.12}s">${moving}</g>`;
 svg+=solid({x:p.x,y:p.y,w:4,d:55,r:1},2,24)+solid({x:p.x+61,y:p.y,w:4,d:55,r:1},2,24);
 svg+=solid(p,26,4,m.changed_files?'hi':'mid');
 for(let v=0;v<5;v++)svg+=solid({x:p.x+14+v*7,y:p.y+9,w:2,d:22,r:.7},30,.3,'lo');
 svg+=k.dotsSvg(k.corners(p,5).map(([x,y])=>k.iso([x,y,30],P)),{size:.55});
 // Étiquette réellement posée sur le toit ; nom échappé (nom Cargo).
 svg+=k.faceTextSvg(k.topMatrix([p.x+8,p.y+43],30.4,P),m.name,{size:3.5,tone:'hi'});
 pieces.push({depth:k.depthOf([p.x+32,p.y+27,0],P),svg});
});
pieces.sort((a,b)=>a.depth-b.depth);const body=pieces.map(p=>p.svg).join('');
const label='Maquette isométrique des modules Cargo astroportd. Les tiroirs éclairés indiquent les modules dont des fichiers ont changé.';
fs.writeFileSync(dir+'/figure.html',k.figureSvg({width:850,height:580,label,body}));
fs.writeFileSync(dir+'/architecture.svg',k.figureSvg({width:850,height:580,label,body,standalone:'light'}));
console.log(`Anatomy : ${modules.length} modules, ${modules.filter(m=>m.changed_files).length} modifiés.`);
