# pyTTRPG_LLM
 
## Objectifs du projet

- Classer des PDF dans des dossiers.
- Extraire et retravailler leurs métadonnées en Python et csv.
- Extraire le texte intégral en Python et autres.
- Verser les métadonnées et le texte intégral dans une base de données SQlite.
- Jouer avec la base de données SQlite.

 
## Structure du système de dossiers et fichiers

- Yragatheque
  - A
    - Apocalypse World
        - Apocalypse World 1st ed
            - `Apocalypse World 1st ed.pdf`
        - Apocalypse World 2nd ed
            - `Apocalypse World 2nd ed.pdf`
  - B
    - Bunnies & Burrows
        - archives
            - `HomebrewB&B.pdf`
        - 1st ed
            - `B&B1sted.pdf`
        - GURPS ed
            - `GURPS B&B.pdf`
    - _Baguettes & Fromages
        - `B&F2e.pdf`
    - _working_directory
    - _corrupted

#### Explications : 
- Les scripts ne traitent que les fichiers PDF.
- Les fichiers PDF placés dans les répertoires archives sont ignorés (ex: `HomebrewB&B.pdf` est ignoré). 
- Les fichiers PDF placés dans les répertoires précédés du caractère _ sont ignorés (ex: `B&F2e.pdf` est ignoré). 
- `Yragatheque` est le niveau le plus haut. C'est la racine de l'arbre de la collection des PDFs.
- `A, B, C`,... sont le 2e niveau. C'est la classification alphabétique de tous les jeux.
- `Apocalypse Word` est au 3e niveau. À ce niveau se trouvent les noms des jeux.
- Tous les niveaux en dessous (4e niveau et au-delà) sont des éditions, ou des gammes, ou des sous-classifications. 
- `_working_directory`  contient les fichiers csv produits, les listes d'autorité et la base de données SQLite.
- `_corrupted` contient tous les fichiers PDFs et fichiers associés (yaml, rawtext,...) qui n'ont pu être traité (non ouvert car corrompus, pages internes illisibles,...). 



## Scripts et flux de numérisation 

Les fichiers `00-nom` sont des scripts Python. 

![](https://jdr.hypotheses.org/files/2023/04/ttrpg_llm-flux.png)

#### Explications : 
- Préparation : 
    - **PARAMETERS** : contient le chemin du dossier dans lequel se trouve la collection de PDF.
    - **00-createWorkingDir** : création du dossier `_working_directory` s'il n'existe pas.
    - **01-permission** : parcours tous les dossiers et donne les droits en lecture-écriture partout
    - **02-purge** : supprime les fichiers `.yaml` , `.rawtext` et `.ocrtext` qui peuvent subsister de traitements précédents
    - **03-rename** : normalise les noms de fichiers (supprime les accents, les caractères spéciaux, remplace les espaces par des traits, etc.)
- Métadonnées : 
    - **10-pdf2yaml** : créé un fichier `.yaml` du même nom que le fichiers pdf, au même emplacement, avec comme variables : 
        - path = chemin absolu du fichier pdf
        - name = nom du fichier sans .pdf
        - size = poid du pdf en Mb
        - pages = nombre de pages du pdf 
        - game = nom du dossier de 3e niveau
        - line = nom des dossiers de 4e niveau et+
    - **11-yaml2csv**
        - Écrit un fichier `metadata.csv` à partir de tous les fichiers .yaml de toute la collection.
        - À cette étape, on peut modifier le fichier `metadata.csv` pour y ajouter des colonnes (et donc des nouvelles variables yaml), modifier le contenu, etc. Il est recommandé de faire une sauvegarde du fichier modifié (exemple : `metadata.backup.csv`) pour ne pas écraser toutes ces modifications manuelles. 
    - **12-csv2yaml**
        - Prend le contenu du fichier `metadata.csv` et réécrit tous les fichiers `.yaml` de la collection avec le nouveau contenu.
- Numérisation : 
    - **30-pdf2rawtext** 
        - Créé un fichier `.rawtext` de même nom que le pdf au même emplacement, contenant l'extraction du texte si le fichier pdf est au format numérique ou s'il y a une couche d'OCR extractible. Si l'extraction ne fonctionne pas ou pose problème, un fichier est créé tout de même mais vide.
    - **34-OCR-byTesseract** 
        - Certains fichiers pdf sont récalcitrants à l'extraction mentionnée précédemment. Alors, si le fichier `.rawtext` est vide ou tout petit, on lance une numérisation via Tesseract qui va créer un fichier `.orctext` au même endroit que le fichier pdf. C'est un processus assez long. 
- Exportation : 
    - **40-yamlntext2sqlite** 
        - On envoie le fichier `.yaml`, accompagné du fichier `.rawtext` ou `.ocrtext` (le plus gros) correspondant, dans une base de données SQlite nommée `TTRPG_LLM.sqlite`
    - **50-reportSQlite**
        - On créé un rapport de la base de données.
    - **51-searchSQlite**
        - On cherche une chaîne de caractère dans la base de données. 


https://github.com/pmartinolli/pyTTRPG_LLM
