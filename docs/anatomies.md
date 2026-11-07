# Les sept anatomies — première livraison

Le catalogue est dans `workers/anatomies/catalog.json`. Il porte les fichiers, symboles, lignes et empreintes SHA-256 d’un commit relu. Le worker consulte Git sans exécuter le code distant ; chaque changement d’une source référencée force une relecture. La présence des symboles et la conservation des empreintes ne sont pas un audit de sécurité.

## État réel
- Engine, MULTIPASS/SSSS, sas Nostr, FaceCloud, DRAGON : spécifications sourcées, illustrations à réaliser.
- UENC : figure de 49 solides, modèle de taille et inspecteur de composants. La presse et son sceau expliquent le flux ; aucune opération cryptographique n’est exécutée.
- ẐEN : répartiteur de 64 solides, calcul BigInt de SplitConfig par défaut et inspecteur. L’horloge solaire n’est pas encore dessinée ni simulée.

Tous les visuels sont des métaphores explicatives, sans connexion à un nœud réel, sans statistiques inventées. Le readout des calculs est indépendant de l’animation décorative, qui ne prétend pas compter des octets ou des centimes en transit.

## Précisions issues de la lecture Rust
- Les 5 KeyFormula sont des variantes alternatives ; scrypt Duniter a N=4096, r=16, p=1, graine 32 octets. L’étirement PBKDF2 LOVE est distinct.
- Les parts Shamir portent le secret SALT/PEPPER. P1+P3 rétablissent le compte, pas nécessairement les fichiers : ceux-ci dépendent des sauvegardes et des amis joignables.
- Le gift wrap 1059 a une exception d’amorçage vers un compte hébergé, pas un accès inconditionnel.
- UENC v2 : en-tête 14 octets (AAD), préfixe 7, compteur 4, dernier 1 : nonce 12 octets ; tag 16 octets par bloc. Un fichier vide a un bloc authentifié. Deux algorithmes sont possibles.
- Les seuils RÊVE du code sont ≥150, garde des 80 plus récents et création d’un résumé, donc pas simplement « réduction à 80 ».
- Le partage 3×1/3 porte sur le surplus après provision et prime. Les taux par défaut du logiciel ne constituent pas des taux fiscaux universels.
- Le clustering par voisins mutuels FaceCloud ne doit pas être confondu avec les amis Nostr réciproques.
- La PSK n’atteste pas seule de l’isolation de tous les services Kubo ou des accès exposés.

## CSP et intégration future astro-ui
Les nouvelles pages `dist/observatoire/anatomies.html` et `index.html` utilisent une CSP sans unsafe-inline/eval, avec JS et CSS locaux. Les déplacements de l’observatoire sont dans `motion.css`. Les groupes des nouvelles figures ont data-crate, data-file et data-symbol, et un inspecteur accessible via boutons natifs. Les exports SVG utilisent une feuille locale `anatomy-kit.css` : conserver ce fichier avec le SVG.

Cette livraison ne modifie pas le dépôt astroportd, sa CSP, son chargeur K.mod, ses routes, son guide ou sa coque. L’Atlas est une ressource séparée de Qwantic ; aucun budget « <20 Ko gzip » de la coque astro-ui n’est donc consommé. L’intégration native devra enregistrer et tester les ressources dans `web.rs`, le chargement à la demande et les exports du guide. Pas de revendication de conformité native tant que ces tests ne sont pas faits.

## Reconstruire et vérifier
```
python3 workers/pipeline.py --offline
python3 -m unittest discover -s tests -v
/home/pi/.deno/bin/deno run tests/anatomy_models_test.mjs
```
Le mode normal récupère main et conserve la fréquence quotidienne à 04:00. Les sources modifiées exigent une correction du modèle et de ses tests avant de mettre à jour volontairement le SHA et les empreintes du catalogue. Ne pas les actualiser automatiquement pour masquer une divergence.
