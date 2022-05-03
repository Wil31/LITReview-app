# LITReview-app

Site web permettant à une communauté d'utilisateurs de consulter ou de
solliciter une critique de livre à la demande.

## Utilisation

### Prérequis

* Un terminal (par exemple Windows PowerShell)
* Python3 version >= 3.10 (vérifier avec `python -V`)

### 1 - Télécharger les fichiers

* Téléchargez depuis le lien:
  [https://github.com/.../main.zip](https://github.com/Wil31/LITReview-app/archive/refs/heads/main.zip)
* Extraire le .zip

### 2 - Configurer l'environnement virtuel

* Ouvrez un terminal
* Naviguez vers le dossier extrait _([...]\LITReview-app)_
* Créez un environnement virtuel avec la commande `python -m venv env`
* Activer l'environnement
  avec `.\env\Scripts\activate` (`source env/bin/activate` sur Linux)
* Installez les packages avec `pip install -r .\requirements.txt`

### 3 - Exécuter le code

* Lancez le serveur depuis le terminal avec la
  commande `py.exe manage.py runserver`
* Entrez l'adresse suivante dans un navigateur : [http:/127.0.0.1:8000/]()

### 4 - Tester le site

Utilisez les identifiants des comptes suivants pour essayer les
fonctionnalités du site.

**Username 1** : `Marie`  
**MdP** : `blagnac24`

**Username 2** : `testuser`  
**MdP** : `blagnac11`

## Rapport flake8

Le repository contient un rapport flake8 dans le dossier _flake8_rapport_.
Il est possible de générer un nouveau rapport avec la commande :

```bash
flake8
```

Le fichier ```.flake8``` à la racine contient les paramètres concernant la
génération du rapport.