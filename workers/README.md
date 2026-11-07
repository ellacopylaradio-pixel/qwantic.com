# Workers de l’observatoire astroportd

Trois étapes séquentielles, sans agents IA autonomes ni exécution du code téléchargé :
1. Synchronisation Git dans `~/.local/state/qwantic-workers/astroportd`. `fetch` remplit un clone dédié sans toucher au checkout de développement.
2. Analyse : nouveaux commits, fichiers ajoutés/modifiés/supprimés, dépendances Cargo de production et mentions de protocoles dans les lignes ajoutées. Toutes les preuves pointent vers le SHA analysé. Une mention n’est pas une validation du protocole.
3. Rendu : figure isométrique Anatomy des modules, animation des seuls modules modifiés, tableau des dépendances, journal et citations. Le bouton arrête l’animation, les préférences de mouvement réduit et la sortie de l’écran sont respectées. SVG statique disponible sans JS.

## Fréquence
**Une exécution quotidienne à 04:00, heure locale de libra**, sans délai aléatoire. `Persistent=true` rattrape une échéance manquée après un arrêt. Le changement d’heure saisonnier suit l’horloge locale.

## Activation
Les unités sont copiées dans `/home/pi/.config/systemd/user/`. Depuis le terminal de pi :
```
systemctl --user daemon-reload
systemctl --user enable --now qwantic-observatoire.timer
systemctl --user list-timers qwantic-observatoire.timer
```
Pour démarrer un essai sans attendre :
```
systemctl --user start qwantic-observatoire.service
journalctl --user -u qwantic-observatoire.service -n 50
```
Pour continuer après la fermeture de session, vérifier `loginctl show-user pi -p Linger` ; l’administrateur peut activer `sudo loginctl enable-linger pi` si nécessaire.
L’activation du timer n’a pas pu être effectuée dans la session de préparation : accès au bus utilisateur refusé. Le téléchargement GitHub y échoue aussi ; ces restrictions ne prouvent pas un échec depuis le service utilisateur normal de libra.

## Exécution manuelle
```
python3 workers/pipeline.py
python3 workers/pipeline.py --offline
```
Le mode hors ligne suit le clone de développement local, indique explicitement `local-only` dans le rapport et n’avance pas le curseur des mises à jour distantes. Pour initialiser le premier rapport, les trois derniers commits sont comparés. Ensuite le curseur suit le dernier SHA rendu après récupération distante réussie. Une réécriture d’historique est refusée : examiner le changement et réinitialiser le curseur manuellement si voulu.

## Sortie et exploitation
`dist/observatoire/index.html` est servie directement par le conteneur statique existant (montage de dist en lecture seule). Aucune modification de NPM nécessaire si ce montage est actif. Le journal garde au plus 30 éditions dans `dist/observatoire/editions/`. Les dates et intervalles restent visibles.
Les erreurs sont écrites dans `~/.local/state/qwantic-workers/status.json` et retournent un code non nul. Une récupération échouée conserve la page existante ; elle n’est pas présentée comme une synchronisation réussie. Aucun push GitHub ou communiqué n’est envoyé automatiquement.

Python 3.10+, Git et Deno installé sur libra sont requis ; pas de dépendances Python externes, aucun modèle IA et aucune clé API. Le code du projet téléchargé n’est ni compilé ni exécuté. L’illustration utilise le kit local Anatomy sous MIT.

## Vérifications
`python3 -m unittest discover -s tests -v` vérifie l’extraction du diff, les dépendances hors tests, les lignes de preuve et l’échappement des extraits HTML. Le rendu navigateur reste à vérifier sur libra : Chromium échoue au démarrage dans l’environnement de préparation.

Cette version révèle les changements structurels de façon déterministe. Elle ne prétend pas expliquer automatiquement la sémantique de chaque patch. Les annonces de résultats, déploiements ou performances nécessitent une revue humaine.

## Anatomies fondatrices
`anatomies.html` complète l’observatoire avec un catalogue des sept vues. UENC et la répartition du surplus ont des modèles pédagogiques interactifs ; les cinq autres vues sont explicitement des spécifications à réaliser. Chaque modèle est rattaché à un commit et à des empreintes de fichiers : si une source change, le rendu indique « à revalider » et désactive le calcul. Voir `docs/anatomies.md` pour les limites et la future intégration astro-ui.
