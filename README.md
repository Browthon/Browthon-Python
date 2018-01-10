# PyWeb
Navigateur web en python

## Dépendances :
- Python 3.5+
- PyQt5 (pip install pyqt5)
- Requests (pip install requests)

## Autres informations :
- Développeur principal : LavaPower
- Contributeur : x
- Développé sous :
  - Système :
    - Windows 10 (V ?.?.? --> Latest)
    - Linux Ubuntu 17.10 (V 0.5.0 --> V ?.?.?)
    - Linux Debian 9 (V 0.2.0 --> V 0.5.0)
    - Windows 7 (V 0.1.0 --> V 0.2.0)
  - Version Python :
    - 3.6.4 (V ?.?.? --> Latest)
    - 3.6.3 (V 0.5.0 --> V ?.?.?)
    - 3.5.3 (V 0.2.0 --> V 0.5.0)
    - 3.6.1 (V 0.1.0 --> V 0.2.0)
  - Libs :
    - Requests (V 0.6.0 --> Latest)
    - PyQt5 (V 2.0.0 --> Latest)
    - PySide (V 0.2.0 --> V 2.0.0)
    - PyQt4 (V 0.1.0 --> V 0.2.0)

## Bugs connus de la version en développement :

- Les liens ouvrant un nouvel onglet n'ouvrent pas ce nouvel onglet.

## Changelog : 

### V ?.?.? : ??? Update (NON DISPO) :
- Paramètre : Url d'accueil modifiable depuis PyWeb
- Bug Fix : Le choix d'un moteur réinitialise les autres paramètres.
- Bug Fix : Le choix d'une url d'accueil réinitialise les autres paramètres.
- Bug Fix : Quand on sélectionne un moteur, PyWeb ne fonctionne plus

### V 2.0.1 : Bug Fix Update (LATEST) :
- Enregistrement des paramètres
- Fichier config plus user-friendly
- Bug Fix : Les boutons reculer, reload et avancer n'avaient d'effet que sur le première page
- Bug Fix : La recherche via la barre d'url retournait toujours une page blanche
- Bug Fix : La touche 'Echap' ne fonctionnait qu'une fois pour quitter le mode plein écran
- Bug Fix : Les favoris et l'historique n'avait pas d'interactions

### V 2.0.0 : PyQt5 Update :
- Reprogrammation en utilisant PyQt5
- Le FullScreen est maintenant disponible ! (Merci à Feldrise)

### V 1.1.0 : Tab Update V3 :
- Reprogrammation du système d'onglet
- Réorganisation de la fenêtre principale
- Ajout d'un bouton home correspondant à la page d'accueil
- Ajout de '[Privé]' dans le titre de la fenêtre quand on est en navigation privé
- Paramètre : Déplacement à l'ouverture d'un onglet

### V 1.0.0 : First Update :
- Respect de la PEP8 (sauf de la limite de caractères par ligne)
- Paramètre : Navigation privée
- Raccourci : Q --> Fermeture de l'onglet actuel
- Raccourci : P --> Ouverture du menu des paramètres
- Raccourci : R --> Reload la page
- Raccourci : H --> Ouverture du menu de l'historique
- Raccourci : F --> Ouverture du menu des favoris
- Raccourci : N --> Création d'un nouvel onglet

### V 0.6.0 : Favorite Update :
- Vérification de mise à jour
- Recherche sur le moteur choisi des mots écrits dans l'url si il n'y a pas de point.
- Début des Favoris (Ajout et suppression mais pas d'interaction)
- Amélioration Favori et Historique avec des messages pour chaque action (ex : Suppression de l'historique)
- Paramètre : Moteur de recherche préféré
- Paramètre : JavaScript Activé/Désactivé
- Raccourci : F10 --> Ouverture du menu des paramètres
- Bug Fix : L'historique ne se supprimait pas

### V 0.5.0 : History Update :
- Création d'une page perso à PyWeb (https://lavapower.github.io/pyweb.html)
- Page perso comme page d'accueil par défaut.
- Confirmation avant extinction lors de la fermeture du dernier onglet.
- Début de l'historique (Affichage + Suppression mais pas d'interaction)
- Séparation de MainWindow dans le fichier "PyWeb_main"
- Déplacement des fichiers .py utilisé par "PyWeb.py" dans files
- Début des raccourcis claviers (F5 --> Reload la page)
- Bug Fix : Toutes les lettres identiques à la première sont en majuscules.

### V 0.4.0 : Tab Update V2 :
- Changement du nom de l'onglet suivant le titre de la page (limité à 12 caractères)
- Création d'option pour l'url d'accueil (modifiable que via le config.txt)
- Fermeture du logiciel lors de la fermeture du dernier onglet
- Nom du button de l'onglet ouvert set sans avoir besoin de cliquer dessus

### V 0.3.0 : Tab Update :
- Changement du titre de la fenêtre suivant le titre de la page avec écrit "- PyWeb" à la fin
- Gestion d'url sans "http://" ni "https://"
- Début de la gestion d'onglet (Limité à 10, fermer les onglets via le menu "⁞")
- Division du code avec un fichier "PyWeb-utils.py"

### V 0.2.1 : Fix Reload Update :
- Ajout d'information dans le README
- Le Bouton Reload fonctionne

### V 0.2.0 : PySide Update :
- Passage à PySide
- Liaison du bouton "Entrer" à la barre URL
- Les vidéos YouTube fonctionnent

### V 0.1.0 : URL Update :
- Ajout d'une barre d'url (qui se met à jour automatiquement)
- Ajout d'un bouton pour entrer l'url
- Ajout d'un bouton pour revenir en arrière
- Ajout d'un bouton pour aller en avant
- Ajout d'un bouton reload pour reload la page

### V 0.0.1 : Initial Update :
- Première version
