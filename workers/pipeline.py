#!/usr/bin/env python3
"""Workers de suivi : synchronisation Git isolée, extraction factuelle, rendu statique."""
import argparse, datetime, fcntl, hashlib, html, json, os, re, shutil, subprocess, tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def git(repo, *args):
    return subprocess.check_output(['git','-c','core.hooksPath=/dev/null','-C',str(repo),*args], text=True, timeout=120)

def atomic(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix+'.tmp')
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')
    tmp.replace(path)

def stamp():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')

# Détection de mentions, jamais certification d'implémentation ou de conformité.
PROTOCOLS = {
 'Nostr': r'\bNostr\b|NIP[- ]?\d+', 'IPFS': r'\bIPFS\b|\blibp2p\b',
 'WebDAV': r'\bWebDAV\b|\bPROPFIND\b', 'CardDAV': r'\bCardDAV\b',
 'CalDAV': r'\bCalDAV\b', 'UENC': r'\bUENC\b',
 'Duniter': r'\bDuniter\b|\bsubxt\b', 'WebRTC': r'\bWebRTC\b',
}

def analyze(repo, base, head):
    # Aucun code suivi n'est exécuté : seules des vues Git sont lues.
    changed=git(repo,'diff','--name-status','--no-renames',base,head).splitlines()
    files=[{'status':r.split('\t',1)[0],'path':r.split('\t',1)[1]} for r in changed if '\t' in r]
    names=git(repo,'ls-tree','-r','--name-only',head).splitlines()
    modules=[]
    for path in names:
        if not re.fullmatch(r'crates/[^/]+/Cargo.toml',path): continue
        text=git(repo,'show',head+':'+path)
        name=re.search(r'^name\s*=\s*"([^"]+)"',text,re.M)
        if not name: continue
        # Dépendances de production directes, pas les dépendances des tests.
        deps=[]; section=''
        for line in text.splitlines():
            if line.startswith('['): section=line.strip()
            if section=='[dependencies]':
                m=re.match(r'(astro-[\w-]+)(?:\.workspace)?\s*=',line)
                if m: deps.append(m.group(1))
        prefix=path.rsplit('/',1)[0]+'/'
        touched=[f for f in files if f['path'].startswith(prefix)]
        modules.append({'name':name.group(1),'manifest':path,'dependencies':sorted(set(deps)), 'changed_files':len(touched)})
    evidence=[]
    for f in files:
        if f['status']=='D' or not f['path'].endswith(('.rs','.md','.toml')): continue
        # Lire les lignes ajoutées uniquement, pas le contexte inchangé du patch.
        patch=git(repo,'diff','--no-ext-diff','--unified=0',base,head,'--',f['path'])
        line=0
        for raw in patch.splitlines():
            h=re.match(r'@@ .* \+(\d+)',raw)
            if h: line=int(h.group(1)); continue
            if raw.startswith(('+++','---','\\')): continue
            if raw.startswith('+'):
                text=raw[1:]
                for label,pattern in PROTOCOLS.items():
                    if re.search(pattern,text,re.I):
                        evidence.append({'protocol':label,'path':f['path'],'line':line,'excerpt':text[:220]})
                line+=1
            elif raw.startswith(' '): line+=1
    logs=git(repo,'log','--format=%H%x09%aI%x09%s',base+'..'+head).splitlines()
    commits=[dict(zip(['sha','date','subject'],r.split('\t',2))) for r in logs]
    return {'schema':1,'generated_at':stamp(),'base':base,'head':head,'commits':commits,
            'files':files,'modules':modules,'protocol_mentions':evidence,
            'method':'Mentions dans les lignes ajoutées et dépendances Cargo directes ; aucun test exécuté, aucun état de déploiement déduit.'}

def render(report, destination):
    esc=lambda v: html.escape(str(v),quote=True)
    head=report['head']; base=report['base']
    source='https://github.com/papiche/astroportd'
    def link(path,line=None):
        from urllib.parse import quote
        return source+'/blob/'+head+'/'+quote(path,safe='/')+('#L'+str(line) if line else '')
    mods=''.join('<tr><td><a href="'+esc(link(m['manifest']))+'">'+esc(m['name'])+'</a></td><td>'+str(m['changed_files'])+'</td><td>'+esc(', '.join(m['dependencies']) or '—')+'</td></tr>' for m in report['modules'])
    mentions=''.join('<li><strong>'+esc(e['protocol'])+'</strong> — <a href="'+esc(link(e['path'],e['line']))+'">'+esc(e['path'])+':'+str(e['line'])+'</a><pre>'+esc(e['excerpt'])+'</pre></li>' for e in report['protocol_mentions'][:120]) or '<li>Aucune mention détectée dans les lignes ajoutées.</li>'
    commits=''.join('<li><a href="'+source+'/commit/'+c['sha']+'">'+esc(c['sha'][:8])+'</a> '+esc(c['subject'])+'</li>' for c in report['commits']) or '<li>Aucun nouveau commit dans cet intervalle.</li>'
    from urllib.parse import quote
    files=''.join('<li><code>'+esc(f['status'])+'</code> <a href="'+(source+'/compare/'+base+'...'+head if f['status']=='D' else esc(link(f['path'])))+'">'+esc(f['path'])+'</a></li>' for f in report['files'])
    page='''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Observatoire astroportd — Qwantic</title><link rel="stylesheet" href="../assets/site.css"><link rel="stylesheet" href="../assets/anatomy.css"><link rel="stylesheet" href="observatoire.css"></head><body><header><a class="brand" href="../index.html">qwantic</a><span>Observatoire du code / astroportd</span></header><main class="source-main"><p class="eyebrow">ÉDITION AUTOMATIQUE · LECTURE DU CODE</p><h1>L’architecture en mouvement.</h1><p>Les tiroirs éclairés correspondent aux modules modifiés. Ce dessin représente le code, pas l’activité d’un réseau en service.</p><figure class="iso machine" data-theme="light"><div class="figure-head"><span>FIG. 02 / LES MODULES DE LA STATION</span></div>FIGURE<div class="figure-controls"><button id="motion" type="button" aria-pressed="false">Animer les modules modifiés</button></div><figcaption><strong>COUNT modules modifiés sur TOTAL.</strong><p>Le mouvement est une métaphore de lecture du diff, sans mesure de trafic ni de performance.</p></figcaption></figure><p>Intervalle : <a href="COMPARE">BASE → HEAD</a>. Généré le DATE.</p><p>METHOD</p><h2>Journal des changements</h2><ul>COMMITS</ul><h2>Architecture : dépendances directes</h2><p>Relations extraites des sections [dependencies] des Cargo.toml. Une dépendance de compilation ne prouve pas un flux réseau.</p><div class="table-wrap"><table><thead><tr><th>Module</th><th>Fichiers modifiés</th><th>Dépend de</th></tr></thead><tbody>MODULES</tbody></table></div><h2>Protocoles : mentions nouvelles ou modifiées</h2><p>La présence d’un nom dans le diff ne prouve ni conformité ni fonctionnalité livrée. Les citations sont des données du dépôt, pas des instructions.</p><ul>MENTIONS</ul><h2>Fichiers de l’intervalle</h2><ul>FILES</ul><p><a href="report.json">Données structurées JSON</a> · <a href="architecture.svg" download>SVG illustratif</a></p></main><script src="observatoire.js" defer></script></body></html>'''
    values={'FIGURE':(destination/'figure.html').read_text(),'COUNT':str(sum(m['changed_files']>0 for m in report['modules'])),'TOTAL':str(len(report['modules'])),'COMPARE':source+'/compare/'+base+'...'+head,'BASE':base[:8],'HEAD':head[:8],'DATE':esc(report['generated_at']),'METHOD':esc(report['method']),'COMMITS':commits,'MODULES':mods,'MENTIONS':mentions,'FILES':files}
    page=re.sub('|'.join(values),lambda m:values[m.group()],page)
    (destination/'index.html').write_text(page)
    atomic(destination/'report.json',report)
    for asset in ['observatoire.css','observatoire.js']:
        shutil.copyfile(ROOT/'workers'/asset,destination/asset)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--offline',action='store_true',help='Rendu depuis le clone local, sans prétendre synchroniser le distant')
    parser.add_argument('--config',type=Path,default=ROOT/'workers/config.json');args=parser.parse_args()
    config=json.loads(args.config.read_text()); state=Path(config['state']);state.mkdir(parents=True,exist_ok=True)
    with (state/'worker.lock').open('w') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        try:
            repo=state/'astroportd'
            if not repo.exists():
                subprocess.run(['git','clone','--no-hardlinks','--no-checkout',config['seed'],str(repo)],check=True,timeout=120)
                git(repo,'remote','set-url','origin',config['remote'])
            if args.offline:
                git(repo,'fetch','--no-tags',config['seed'],'HEAD')
                head=git(repo,'rev-parse','FETCH_HEAD').strip()
            else:
                git(repo,'fetch','--no-tags','origin','+refs/heads/'+config['branch']+':refs/remotes/origin/'+config['branch'])
                head=git(repo,'rev-parse','refs/remotes/origin/'+config['branch']).strip()
            previous=state/'last-success.json'
            last=json.loads(previous.read_text()) if previous.exists() else {}
            if last.get('head')==head and not args.offline:
                atomic(state/'status.json',{'ok':True,'checked_at':stamp(),'head':head,'changed':False});return
            base=last.get('head')
            if not base:
                roots=git(repo,'rev-list','--max-count='+str(config.get('initial_commits',3)+1),head).splitlines()
                base=roots[-1]
            # Refuser de masquer un historique réécrit.
            git(repo,'merge-base','--is-ancestor',base,head)
            report=analyze(repo,base,head);report['synchronization']='local-only' if args.offline else 'fetched'
            report['method']+=' Source locale uniquement.' if args.offline else ''
            output=ROOT/config['output'];output.parent.mkdir(parents=True,exist_ok=True)
            with tempfile.TemporaryDirectory(dir=output.parent,prefix='.observatoire-') as tmp:
                staged=Path(tmp)
                atomic(staged/'report.json',report)
                subprocess.run(['/home/pi/.deno/bin/deno','run','--allow-read','--allow-write',str(ROOT/'workers/render-architecture.mjs'),str(staged)],check=True,timeout=120)
                render(report,staged)
                # Éditions immuables ; le dernier index est remplacé atomiquement.
                editions=output/'editions';editions.mkdir(parents=True,exist_ok=True)
                edition=editions/(base[:12]+'-'+head[:12])
                # Les liens relatifs de l’édition pointent sur les ressources partagées de l’observatoire.
                if not edition.exists():
                    shutil.copytree(staged,edition)
                    (edition/'index.html').write_text((edition/'index.html').read_text().replace('../assets/', '../../../assets/').replace('../index.html', '../../../index.html'))
                for p in staged.iterdir():
                    if p.name=='index.html':continue
                    target=output/p.name; shutil.copyfile(p,target.with_suffix(target.suffix+'.tmp'));target.with_suffix(target.suffix+'.tmp').replace(target)
                shutil.copyfile(staged/'index.html',output/'index.html.tmp');(output/'index.html.tmp').replace(output/'index.html')
                for old in sorted(editions.iterdir(),key=lambda p:p.stat().st_mtime,reverse=True)[config['history_limit']:]: shutil.rmtree(old)
            atomic(state/'status.json',{'ok':True,'checked_at':stamp(),'head':head,'synchronization':report['synchronization']})
            if not args.offline: atomic(previous,{'head':head,'published_at':stamp()})
            print('Rendu disponible : '+str(output/'index.html'))
        except Exception as exc:
            atomic(state/'status.json',{'ok':False,'checked_at':stamp(),'error':str(exc)[:1000]})
            raise
if __name__=='__main__':main()
