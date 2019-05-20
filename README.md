# La Bascule
Script pour automatiser la recherche d'information des différentes sensibilités écologiques des mairies d'IDF.

## Ça fait quoi ?

Le script récupère des informations **PUBLIQUES** dans des bases de données administratives (publiques ou privées) pour les aggréger et interpréter le niveau de sensibilisation des maires d'IDF à l'écologie.

### Scraping

le script crée un fichier CSV pour chaque département et va chercher des informations sur les sites :
 * www.annuaire-des-mairies.com
 * www.mairie.net
 * www.mairie.biz
 * www.mon-maire.fr

le format des fichiers CSV et la localisation où ils sont créés est configurable dans le fichier `config.ini`

**DISCLAIMER : toutes les données utilisées sont PUBLIQUES** et leur utilisation est à des seules fin d'information.

### Note de Site

En plus de ces informations le script attribue une "note écolo" aux sites des mairies. Cette note est calculée avec le nombre d'occurence de mots-clés spécifiés dans le fichier `config.ini` pondérés.
Les occurences de ces mots-clés sont mesurées sur :
 * la première page du site de la mairie
 * toutes les pages ou ressources vers lesquelles la première

### Note Twitter

Chaque mot-clé est associé à un coefficient. Par exemple `environnement` a un coefficient de 5, alors que `nature` a un coefficient de 3 (moins pertinent).

Le processus de note écolo Twitter cherche : 
 
 * le nombre de tweets retournés par la recherche `<nom de la ville> <mot-clé>` pour chaque mot-clé, pondéré par le coefficient dudit mot-clé.
 * le nombre de tweets venant des comptes officiels retournés par les mêmes recherches. Les comptes officiels sont déterminés par ce que renvoie une recherche de compte de type `ville de <nom de la ville>`. S'il y a plusieurs résultats, les scores sont pondérés par `1/<ordre de retour du compte>`. Par exemple, un compte arrivant second de la recherche a un coefficient 1/2 dans le score, le troisième a un coefficient 1/3.

Toutes les recherches de tweets ne cherchent que les tweets en français à partir des dernières élections municipales.

### Environnement
modules needed : 
 * tweepy
 * requests-html
 * configparser
 * argparse
```
pip3 install tweepy
pip3 install requests-html
pip3 install configparser
pip3 install argparse
```

## Usage

```
usage: main.py [-h] --config CONFIG [--log LOG] [-d D]

Script pour La Bascule IDF scraping des mairies en IDF.

optional arguments:
  -h, --help         show this help message and exit
  --config CONFIG    required config file
  --log LOG, -l LOG  log file, default : log.txt
  -d D               Département à récupérer
```

## TODO

 * notes sur le site
 * formule note Twitter
 * front-end et migration vers une BD