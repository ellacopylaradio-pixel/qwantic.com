# Servir sur libra avec Nginx Proxy Manager
Le conteneur `qwantic-web` sert désormais `dist/` sur le réseau
`nginxproxymanager_default`. Configuration reproductible : `compose.yaml` ;
démarrage : `docker compose up -d`. Aucun port supplémentaire n'est publié.
Le raccordement du domaine et le certificat restent à configurer dans NPM.

1. Servir le dossier `dist/` depuis un conteneur nginx séparé, joignable depuis NPM sur un réseau Docker commun.
2. Dans NPM, créer le Proxy Host `qwantic.com`, schéma `http`, cible : nom du conteneur statique, port 80.
3. Vérifier les DNS A/AAAA et l’arrivée des ports 80/443 ; demander le certificat Let's Encrypt et activer Force SSL.
4. Vérifier accueil, sources, téléchargement TXT et SVG, navigation mobile et HTTPS avant ouverture.

L’ancien vhost système utilise PHP et un lien /var/www/qwantic.com cassé. Ne pas le remettre en service pour cette version statique. NPM possède déjà les publications 80/81/443 dans son compose ; vérifier l’état réel et les réseaux Docker avant installation.

Ne pas modifier directement la base NPM ou ses configurations générées.
