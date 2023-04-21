# pyTTRPG_LLM
 
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

#### Explications : 
- Les scripts ne traitent que les fichiers PDF.
- Les fichiers PDF placés dans les répertoires archives sont ignorés (ex: `HomebrewB&B.pdf` est ignoré). 
- Les fichiers PDF placés dans les répertoires précédés du caractère _ sont ignorés (ex: `B&F2e.pdf` est ignoré). 
- `Yragatheque` est le niveau le plus haut. C'est la racine de l'arbre de la collection des PDFs.
- `A, B, C`,... sont le 2e niveau. C'est la classification alphabétique de tous les jeux.
- `Apocalypse Word` est au 3e niveau. À ce niveau se trouvent les noms des jeux.
- Tous les niveaux en dessous (4e niveau et au-delà) sont des éditions, ou des gammes, ou des sous-classifications. 




## Scripts et flux de numérisation 

Les fichiers `00-nom` sont des scripts Python. 

```graphviz
digraph num {
  nodesep=1.0 

01 [label="01-permission"]
02 [label="02-purge"]
03 [label="03-rename"]
10 [label="10-pdf2yaml"]
11 [label="11-yaml2csv" ]
12 [label="12-csv2yaml"]
a11 [label="Modifier metadata.csv"; shape=none]
30 [label="30-pdf2rawtext"]
33 [label="33-if-rawtextFail"]
b33 [label="Traitement manuel des PDF"; shape=none]
34 [label="34-OCR-byTesseract"]
40 [label="40-yamlntext2sqlite"]
50 [label="50-reportSQlite"]
51 [label="51-searchSQlite"]

subgraph cluster00 { 01 -> 02 -> 03 }
03 -> 10 
subgraph cluster10 { 10 -> 11 -> a11 ->12 }
12 -> 30
subgraph cluster30 { 30 -> 33 -> b33 -> 30 -> 34  } 
34 -> 40
subgraph cluster5060 { 40 -> 50 -> 51}
10 -> "[ .yaml ]"
11 -> "[ metadata.csv ]"
30 -> "[ .rawtext ]"
34 -> "[ .ocrtext ]"
40 -> "[ TTRPG_LLM.sqlite ]" 
}
```

#### Explications : 
- Préparation : 
    - **PARAMETERS** : contient le dossier dans lequel se trouve la collection de PDF.
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
        - À cette étape, on peut modifier le fichier `metadata.csv` pour y ajouter des colonnes (et donc des nouvelles variables yaml), modifier le contenu, etc. Il est recommandé de faire au préalable une sauvegarde du fichier `metadata.csv` original. 
    - **12-csv2yaml**
        - Prend le contenu du fichier `metadata.csv` et réécrit tous les fichiers `.yaml` de la collection avec le nouveau contenu. 
- Numérisation : 
    - **30-pdf2rawtext** 
        - Créé un fichier `.rawtext` de même nom que le pdf au même emplacement, contenant l'extraction du texte si le fichier pdf est au format numérique ou s'il y a une couche d'OCR extractible.
    - **33-if-rawtextFail** 
        - Si le fichier `.rawtext` est trop petit (0k, 1kb ou en fait moins d'1 Kb par 1Mb du pdf), alors on créé une copie du fichier pdf correspondant dans un dossier à part, on lance un OCR manuellement dessus et on le replace dans son dossier original. 
        - On supprime le fichier `.rawtext` et on relance 30-pdf2rawtxt.
    - **34-OCR-byTesseract** 
        - Certains fichiers pdf sont récalcitrants. Alors on lance une numérisation via Tesseract qui va créer un fichier `.orctext` au même endroit que le fichier pdf. 
- Exportation : 
    - **40-yamlntext2sqlite** 
        - On envoie le fichier `.yaml` et le fichier `.rawtext/.ocrtext` correspondant dans une base de données SQlite nommée `TTRPG_LLM.sqlite`
    - **50-reportSQlite**
        - On créé un rapport de la base de données.
    - **51-searchSQlite**
        - On cherche une chaîne de caractère dans la base de données. 
