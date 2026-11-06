# Servir sur libra avec Nginx Proxy Manager
Préparation uniquement : aucune modification des services en production.

1. Servir le dossier `dist/` depuis un conteneur nginx séparé, joignable depuis NPM sur un réseau Docker commun.
2. Dans NPM, créer le Proxy Host `qwantic.com`, schéma `http`, cible : nom du conteneur statique, port 80.
3. Vérifier les DNS A/AAAA et l’arrivée des ports 80/443 ; demander le certificat Let's Encrypt et activer Force SSL.
4. Vérifier accueil, sources, téléchargement TXT et SVG, navigation mobile et HTTPS avant ouverture.

L’ancien vhost système utilise PHP et un lien /var/www/qwantic.com cassé. Ne pas le remettre en service pour cette version statique. NPM possède déjà les publications 80/81/443 dans son compose ; vérifier l’état réel et les réseaux Docker avant installation.

La session actuelle n’a pas accès à Docker ni au réseau : état actif non vérifié. Ne pas modifier directement la base NPM ou ses configurations générées.
