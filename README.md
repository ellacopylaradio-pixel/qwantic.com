# qwantic.com
Vitrine publique du G1FabLab. HTML, CSS, JavaScript natifs ; aucun framework, service distant ou compilation nécessaire pour servir `dist/`.

## Aperçu
`python3 -m http.server 8088 --directory dist`

## Illustration Anatomy
Le SVG est généré avec le kit Anatomy vendorié sous MIT. Node 20.10+ recommandé :
`node scripts/build-figure.mjs`
Alternative disponible sur libra : `/home/pi/.deno/bin/deno run --allow-read --allow-write scripts/build-figure.mjs`.
Le fragment généré est intégré dans index.html. Si la géométrie change, remplacer le contenu de `#station-figure` par `dist/assets/figure.html`.

## Éditorial
Voir `docs/sources.md` et `dist/sources.html`. Pas de stations, partenaires ou résultats inventés. Contact presse et identité de l’éditeur à valider avant ouverture publique. Intégration Duniter testée selon confirmation du responsable ; compte rendu à joindre.

## Publication GitHub
La clé publique dédiée a été remise au responsable. Clé privée hors dépôt : `/home/pi/.ssh/qwantic_github_ed25519`.
Créer un dépôt `qwantic.com` sur le compte `ellacopylaradio-pixel`, puis depuis ce dossier :
```
git remote add origin git@github.com:ellacopylaradio-pixel/qwantic.com.git
GIT_SSH_COMMAND='ssh -i /home/pi/.ssh/qwantic_github_ed25519 -o IdentitiesOnly=yes' git push -u origin main
```
Le nom de dépôt est proposé, non vérifié. Aucun dépôt distant n’a été créé dans cette session.

## Hébergement sur libra
Voir `docs/hebergement.md`. Le site n’est pas encore mis en production.

## Licence
Code et illustration : MIT, voir LICENSE. Kit Anatomy : licence conservée dans vendor/anatomy/LICENSE.
