# Messages_LAN (2022-2023)
Permet de s'échanger des messages par une console python à travers le réseau local

## Utilisation

### Si vous voulez lancer un serveur : 

Exécutez dans une console Python le fichier `server_multi.py`

### Si vous voulez lancer un client :

Exécutez dans une console Python le fichier `messagerie.py`

Vous pouvez désormais envoyer des messages grâce au prompt.*

-> Faire commencer votre message par un / fera s'exécuter la suite du message comme une commande shell sur l'ordinateur de ceux qui le reçoivent. (Je ne suis pas responsable des /reboot)

**/!\ Si vous recevez un message pendant que vous en rédigez un, le message reçu sera écrit sur la ligne sur laquelle vous êtes en train d'écrire.**

## Informations techniques

Programmé avec Python 3

Modules : socket, threading, time, os

### Par défaut :
Port de communication : 8080

