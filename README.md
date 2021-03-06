# Browthon-Python
First version of Browthon made with Python and PyQt5

## Dépendances :
- Python 3.5+
- PyQt5 (pip install pyqt5)
- Requests (pip install requests)

## Autres informations :
- Développeur principal : LavaPower
- Contributeur : x
- Développé sous :
  - Système :
    - Linux Manjaro / Windows 7 (V 2.2.0 --> Latest)
    - Windows 10 (V 2.1.0 --> V 2.2.0)
    - Linux Ubuntu 17.10 (V 0.5.0 --> V 2.1.0)
    - Linux Debian 9 (V 0.2.0 --> V 0.5.0)
    - Windows 7 (V 0.1.0 --> V 0.2.0)
  - Version Python :
    - 3.6.5 (V 2.2.0 --> Latest)
    - 3.6.4 (V 2.1.0 --> V 2.2.0)
    - 3.6.3 (V 0.5.0 --> V 2.1.0)
    - 3.5.3 (V 0.2.0 --> V 0.5.0)
    - 3.6.1 (V 0.1.0 --> V 0.2.0)
  - Libs :
    - PyQt5 (V 2.0.0 --> Latest)
    - Requests (V 0.6.0 --> Latest)
    - PySide (V 0.2.0 --> V 2.0.0)
    - PyQt4 (V 0.1.0 --> V 0.2.0)

## Remerciements :
- Feldrise : https://github.com/Feldrise - Pour l'aide dans le développement
- LechatGris : https://github.com/LechatGris - Pour l'idée du logo

## Bugs connus de la version en développement :
- /

## Changelog : 

### V 2.6.0 : Addon Update - 14 Juil 2018 :
- Ajout d'addons créé en Python
- Ajout d'une galerie d'addons sur le site
- Ajout d'une page de remerciement au premiier lancement
- Nouvelle version du Launcher
- Nombreux bug fixes

### V 2.5.0 : Basic Update - 3 Juil 2018 :
- Système de téléchargements avec menu
- Nouveau menu pour l'historique et les favoris (avec raccourci H et F)
- Nouveau système de logs
- Système de fenêtre pour tous les anciens menus
- Création de fenêtre pour les informations sur Browthon, PyQt et Qt

### V 2.4.0 : Browthon Update - 16 Juin 2018 :
- Changement du nom (de PyWeb à Browthon)
- Réécriture du launcher
- Ajout du système de session (nom, enregistrement, lancement...)
- Ajout du système de raccourci URL
- Ajout d'un menu de clique droit complètement personnalisé
- Enregistrement de la session avant de quitter (+ paramètre pour la charger automatiquement au lancement)
- Mise à jour du thème Dark
- Ajout des thèmes Red et Blue
- Ajout du clic molette pour ouvrir un lien dans un nouvel onglet
- Suppression du système de langues
- Plusieurs bugs fixes et optimisation

### V 2.3.0 : Appearance Update - 30 Mai 2018 :
- Création d'un package pour ArchLinux (et Manjaro)
- Création d'un launcher pour télécharger les nouvelles versions automatiquement
- Création de thèmes (juste le sombre pour l'instant)
- Gestion basique des thèmes
- Changement de traduction (modification et nouveaux ajouts)
- Nouvelle apparence de PyWeb avec moins de boutons
- Modification du logo de PyWeb
- Bug Fix : L'icone de l'onglet ne changeait que si c'était le premier onglet
- Bug Fix : Le texte de la fênetre de fermeture de PyWeb n'avaient pas de retour à la ligne

### V 2.2.1 : Fail Update - 23 Mai 2018 :
- Update des versions dans le code et l'updater

### V 2.2.0 : Rebirth Update - 23 Mai 2018 :
- Possibilité de voir le code source de la page actuel via F2 puis de repasser en mode "normal" toujours avec F2
- Modification de l'icone du logiciel (merci LechatGris)
- Ajout de l'icone du site dans les onglets
- Bug Fix : Changement du site PyWeb
- Bug Fix : Sur Linux, les fichiers de langues n'était pas en UTF8 valide.
- Bug Fix : Le texte des fenêtres "Nouvelle MAJ" et "Informations" n'avaient pas de retour à la ligne

### V 2.1.0 : Language Update - 19 Jav 2018 :
- Système de langue pour PyWeb (Francais et Anglais dispo par défaut)
- Suppression de print() de debug qui avait été laissé par erreur
- Paramètre : Url d'accueil modifiable depuis PyWeb
- Paramètre : Langue utilisé par PyWeb
- Bug Fix : Le choix d'un moteur réinitialise les autres paramètres.
- Bug Fix : Le choix d'une url d'accueil réinitialise les autres paramètres.
- Bug Fix : Quand on sélectionne un moteur, PyWeb ne fonctionne plus

### V 2.0.1 : Bug Fix Update - 5 Jan 2018 :
- Enregistrement des paramètres
- Fichier config plus user-friendly
- Bug Fix : Les boutons reculer, reload et avancer n'avaient d'effet que sur le première page
- Bug Fix : La recherche via la barre d'url retournait toujours une page blanche
- Bug Fix : La touche 'Echap' ne fonctionnait qu'une fois pour quitter le mode plein écran
- Bug Fix : Les favoris et l'historique n'avait pas d'interactions

### V 2.0.0 : PyQt5 Update - 4 Jan 2018 :
- Reprogrammation en utilisant PyQt5
- Le FullScreen est maintenant disponible ! (Merci à Feldrise)

### V 1.1.0 : Tab Update V3 - 2 Jan 2018 :
- Reprogrammation du système d'onglet
- Réorganisation de la fenêtre principale
- Ajout d'un bouton home correspondant à la page d'accueil
- Ajout de '[Privé]' dans le titre de la fenêtre quand on est en navigation privé
- Paramètre : Déplacement à l'ouverture d'un onglet

### V 1.0.0 : First Update - 30 Dec 2017 :
- Respect de la PEP8 (sauf de la limite de caractères par ligne)
- Paramètre : Navigation privée
- Raccourci : Q --> Fermeture de l'onglet actuel
- Raccourci : P --> Ouverture du menu des paramètres
- Raccourci : R --> Reload la page
- Raccourci : H --> Ouverture du menu de l'historique
- Raccourci : F --> Ouverture du menu des favoris
- Raccourci : N --> Création d'un nouvel onglet

### V 0.6.0 : Favorite Update - 28 Dec 2017 :
- Vérification de mise à jour
- Recherche sur le moteur choisi des mots écrits dans l'url si il n'y a pas de point.
- Début des Favoris (Ajout et suppression mais pas d'interaction)
- Amélioration Favori et Historique avec des messages pour chaque action (ex : Suppression de l'historique)
- Paramètre : Moteur de recherche préféré
- Paramètre : JavaScript Activé/Désactivé
- Raccourci : F10 --> Ouverture du menu des paramètres
- Bug Fix : L'historique ne se supprimait pas

### V 0.5.0 : History Update - 20 Dec 2017 :
- Création d'une page perso à PyWeb (https://lavapower.github.io/pyweb.html)
- Page perso comme page d'accueil par défaut.
- Confirmation avant extinction lors de la fermeture du dernier onglet.
- Début de l'historique (Affichage + Suppression mais pas d'interaction)
- Séparation de MainWindow dans le fichier "PyWeb_main"
- Déplacement des fichiers .py utilisé par "PyWeb.py" dans files
- Début des raccourcis claviers (F5 --> Reload la page)
- Bug Fix : Toutes les lettres identiques à la première sont en majuscules.

### V 0.4.0 : Tab Update V2 - 10 Dec 2017 :
- Changement du nom de l'onglet suivant le titre de la page (limité à 12 caractères)
- Création d'option pour l'url d'accueil (modifiable que via le config.txt)
- Fermeture du logiciel lors de la fermeture du dernier onglet
- Nom du button de l'onglet ouvert set sans avoir besoin de cliquer dessus

### V 0.3.0 : Tab Update - 8 Dec 2017 :
- Changement du titre de la fenêtre suivant le titre de la page avec écrit "- PyWeb" à la fin
- Gestion d'url sans "http://" ni "https://"
- Début de la gestion d'onglet (Limité à 10, fermer les onglets via le menu "⁞")
- Division du code avec un fichier "PyWeb-utils.py"

### V 0.2.1 : Fix Reload Update - 4 Dec 2017 :
- Ajout d'information dans le README
- Le Bouton Reload fonctionne

### V 0.2.0 : PySide Update - 3 Dec 2017 :
- Passage à PySide
- Liaison du bouton "Entrer" à la barre URL
- Les vidéos YouTube fonctionnent

### V 0.1.0 : URL Update - 28 Nov 2017 :
- Ajout d'une barre d'url (qui se met à jour automatiquement)
- Ajout d'un bouton pour entrer l'url
- Ajout d'un bouton pour revenir en arrière
- Ajout d'un bouton pour aller en avant
- Ajout d'un bouton reload pour reload la page

### V 0.0.1 : Initial Update - 27 Nov 2017 :
- Première version
