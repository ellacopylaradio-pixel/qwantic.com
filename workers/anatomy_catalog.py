"""Catalogue de modèles relus, attachés à des sources Rust figées."""
import hashlib, html, json, shutil, subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
CSP="default-src 'none'; script-src 'self'; style-src 'self'; img-src 'self' blob: data:; connect-src 'self'; base-uri 'none'; object-src 'none'; form-action 'none'"
def resolve(catalog,read):
    result=[]
    for entry in catalog:
        entry=json.loads(json.dumps(entry));entry['review_required']=False
        for ref in entry['sources']:
            try:ref['unchanged']=hashlib.sha256(read(ref['file']).encode()).hexdigest()==ref['sha256']
            except subprocess.CalledProcessError:ref['unchanged']=False
            entry['review_required']|=not ref['unchanged']
        result.append(entry)
    return result

def build(repo,report,dest):
    import sys
    sys.path.insert(0,str(HERE))
    from pipeline import git
    raw=json.loads((HERE/'anatomies/catalog.json').read_text())
    catalog=resolve(raw,lambda f:git(repo,'show',report['head']+':'+f))
    subprocess.run(['/home/pi/.deno/bin/deno','run','--allow-read','--allow-write',str(HERE/'anatomies/build.mjs'),str(dest)],check=True,timeout=120)
    for asset in ['models.mjs','live.mjs','anatomies.css']:
        target=dest/(asset.replace('.mjs','.js'))
        target.write_text((HERE/'anatomies'/asset).read_text().replace('./models.mjs','./models.js'))
    shutil.copyfile(HERE.parent/'dist/assets/anatomy.css',dest/'anatomy-kit.css')
    esc=lambda x:html.escape(str(x),quote=True)
    sections=[]
    for i,view in enumerate(catalog,1):
        id=view['id'];refs=[]
        for ref in view['sources']:
            url='https://github.com/papiche/astroportd/blob/'+view['validated_commit']+'/'+ref['file']+'#L'+str(ref['line'])
            refs.append('<li><a href="'+esc(url)+'">'+esc(ref['file'])+' · '+esc(ref['symbol'] or 'module')+'</a></li>')
        status='À revalider : une source a changé depuis la lecture de référence.' if view['review_required'] else ('Modèle interactif' if view['status']=='interactive' else 'Mécanisme à réaliser — spécification sourcée')
        mechanics=''
        if view['status']=='interactive':
            controls='<label>Taille du fichier en octets <input id="uenc-size" type="number" min="0" max="1073741824" step="1" value="131073"></label>' if id=='uenc' else '<label>Surplus hebdomadaire (centimes) <input id="surplus" type="text" inputmode="numeric" value="100000" maxlength="20" pattern="[0-9]+"></label><label>Résultat cumulé avant la semaine (centimes) <input id="ytd" type="text" inputmode="numeric" value="0" maxlength="20" pattern="[0-9]+"></label>'
            # Calcul autorisé seulement quand toutes les sources du modèle correspondent.
            disabled=' disabled' if view['review_required'] else ''
            mechanics='<div class="model" data-model="'+id+'" data-stale="'+str(view['review_required']).lower()+'"><figure class="iso"><div class="figure-head"><span>FIG. '+str(i)+' / '+esc(view['title'])+'</span></div>'+(dest/(id+'-figure.html')).read_text()+'<figcaption>'+esc(view['mechanism'])+' Aucun traitement réel.</figcaption></figure><fieldset'+disabled+'>'+controls+'<button type="button" data-calculate>Calculer</button><button type="button" data-motion aria-pressed="false">Animer la mécanique</button></fieldset><output aria-live="polite">Calcul en attente.</output><div class="inspect-buttons" aria-label="Explorer les composants"></div><aside><h3>Le composant sélectionné</h3><p data-inspector>Choisissez un composant pour retrouver son rôle et sa source.</p><a data-source href="'+esc('https://github.com/papiche/astroportd/tree/'+view['validated_commit'])+'">Code Rust de référence</a></aside><p><a href="'+id+'.svg">Exporter le SVG</a></p></div>'
        sections.append('<section id="'+id+'"><p class="eyebrow">ANATOMIE '+str(i)+' / '+esc(status)+'</p><h2>'+esc(view['title'])+'</h2><p>'+esc(view['role'])+'</p><p><strong>Mécanisme :</strong> '+esc(view['mechanism'])+'</p><p class="limit">'+esc(view['limit'])+'</p>'+mechanics+'<details><summary>Sources Rust · '+esc(view['validated_commit'][:12])+'</summary><ul>'+''.join(refs)+'</ul></details></section>')
    page='<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta http-equiv="Content-Security-Policy" content="'+esc(CSP)+'"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Les anatomies d’astroportd — Qwantic</title><link rel="stylesheet" href="anatomy-kit.css"><link rel="stylesheet" href="anatomies.css"></head><body><header><a href="../index.html">qwantic</a><a href="index.html">Observatoire du code</a></header><main><p class="eyebrow">L’HUMAIN D’ABORD · LE CODE À PORTÉE DE MAIN</p><h1>Dans la mécanique<br>d’astroportd.</h1><p>Sept anatomies fondatrices : deux modèles interactifs et cinq mécanismes à réaliser. Les mécanismes sont des explications du code, sans télémétrie ni action sur une station.</p><p>Référence du suivi : '+esc(report['head'][:12])+'. Les modèles sont figés sur leur commit de lecture ; si leurs sources changent, le worker les signale et désactive les calculs jusqu’à relecture.</p><nav aria-label="Les sept anatomies">'+''.join('<a href="#'+v['id']+'">'+str(i)+' / '+esc(v['title'])+'</a>' for i,v in enumerate(catalog,1))+'</nav>'+''.join(sections)+'</main><script type="module" src="live.js"></script></body></html>'
    (dest/'anatomies.html').write_text(page)
    (dest/'anatomies.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
