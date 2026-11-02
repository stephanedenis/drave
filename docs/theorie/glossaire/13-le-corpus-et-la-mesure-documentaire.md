# 13. Le corpus et la mesure documentaire

> **Famille 13 du glossaire** (13 familles). Index : [le glossaire](../glossaire.md).

**Corpus** *(corpus ; corpus)* — un **ensemble de textes** réuni pour une mesure, avec son mode d'emploi : d'où il vient, ce qu'on a retiré, comment il est découpé. Dans le dépôt, un corpus n'existe pas sans son **manifeste** (`reports/corpus-*.json`) : nombre d'articles ou de documents, caractères, octets par split, empreintes SHA-256. Les données vivent dans `data/` (gitignoré), les chiffres dans `reports/`. *Voir* : `reports/rapport-corpus-wiki-texte.md`, `tools/corpus_wikipedia_texte.py`.

**Sous-corpus** *(sous-ensemble ; subset)* — un corpus qui ne garde qu'une **partie** d'un corpus plus large, choisie pour une raison nommée : une langue, un genre, un fonds. Le corpus OCR est ainsi le sous-corpus des **scans** du fonds `Biblio_large` et de `archives/CEGEP` : les PDF sans couche texte, que `pdftotext` ne lit pas.

**Dump** *(dump ; dump)* — la **copie brute** d'une base ou d'un site, publiée périodiquement, avant tout traitement. Wikipédia publie `frwiki-latest-pages-articles-multistream.xml.bz2` : du XML compressé, un article par page, avec le wikitexte d'origine. Le dump est la source ; le corpus est ce qu'on en tire après filtre, débalisage et déduplication.

**WARC** *(Web ARChive ; WARC)* — le **format d'archive** du Web (ISO 28500) : un fichier qui enregistre des réponses HTTP brutes (en-têtes + corps), utilisé par les robots d'archivage pour conserver des pages telles qu'elles ont été servies. Le dépôt n'en produit pas encore : le corpus web s'appuie sur les dumps Wikipédia ; le WARC est le format à connaître le jour où l'on archivera des pages vivantes.

**BLAKE2b** — une **fonction de hachage** cryptographique rapide, utilisée dans le dépôt pour **dédupliquer** : deux articles ou deux tronçons de texte identiques ont la même empreinte, et le second est écarté. Elle sert aussi à **répartir** les documents entre train/val/test (hash salé du chemin ou du `page_id`). *Voir* : `tools/corpus_wikipedia.py`, `tools/corpus_wikipedia_texte.py`.

**SHA-256** — l'empreinte **de fichier** (256 bits) qui identifie un corpus fini : le manifeste donne `sha256_train`, `sha256_val`, `sha256_test`, ce qui permet de vérifier qu'un corpus n'a pas bougé depuis sa mesure. C'est le complément de BLAKE2b, qui déduplique pendant la construction. *Voir* : `reports/corpus-*.json`.

**CEGEP** — le fonds des **notes de cours** de l'établissement, dans `archives/CEGEP/` : des PDF administratifs et pédagogiques (exercices, annexes, programmes de colloque), souvent sans couche texte. C'est la deuxième racine de l'OCR (`tools/ocr_pdf.py --racine CEGEP`), après les livres de `Biblio_large` ; licences : droits réservés, usage local, non diffusé.

**Split** *(découpage ; split)* — la **partition** d'un corpus en trois fichiers : `train.txt` (l'entraînement), `val.txt` (le réglage), `test.txt` (la mesure finale). Le dépôt la tire d'un **hash salé** de l'identifiant du document (le `page_id` ou le chemin), avec un sel fixé par `--graine` : la même graine redonne le même split, et un document ne change jamais de camp. *Voir* : `tools/corpus_wikipedia_texte.py`, `--val` et `--test`.

**Contamination** *(fuite entre splits ; leakage)* — la présence d'un même **texte** dans deux splits, ou dans un split et un jeu d'évaluation. Le dépôt la mesure à l'unité qui compte — la **fenêtre de 8 Ko**, pas la ligne — avec `verifie_contamination.py --taille-troncon 8192` : un doublon exact est cherché entre train, val et test. Sans ce contrôle à zéro, un score de test ment. *Voir* : `tools/verifie_contamination.py`, `reports/*-contamination.json`.

**Tronçon** *(chunk)* — un **morceau de texte** de taille fixe (8 192 caractères par défaut), coupé de préférence à un espace pour ne pas casser un mot. Le corpus est écrit en tronçons séparés par une ligne vide ; la déduplication se fait au tronçon pour le train. Le mot « tronçon » et le mot anglais « chunk » sont employés indifféremment. *Voir* : `--chunk` dans `tools/corpus_wikipedia_texte.py`.

**Manifeste** *(manifest ; manifest)* — le **JSON de résultats** d'une extraction : source, méthode, filtres, déduplication, split, compteurs, octets, empreintes, limites. C'est la pièce qui rend un corpus **reproductible** ; il vit dans `reports/` et il est committé, contrairement aux données. *Voir* : `--manifeste` dans les outils, `reports/corpus-pdf.json`.

**Fiche de résultat** *(fiche ; report)* — le **document court** qui accompagne un manifeste : ce que c'est, le chiffre, le dispositif, le **contrôle négatif**, ce qui pourrait être faux, la suite. Une livraison sans fiche n'est pas une livraison. *Voir* : `docs/methode/resultats.md`, `reports/rapport-*.md`.

**Pipeline** *(chaîne de traitement ; pipeline)* — la **suite d'étapes** qui transforme une source en corpus : télécharger, décompresser, parser, débaliser, filtrer, dédupliquer, découper, écrire, mesurer. Chaque étape est un outil du dépôt ; le manifeste dit laquelle a tourné. *Voir* : `tools/corpus_wikipedia_texte.py`, `tools/extrait_pdf.py`, `tools/ocr_pdf.py`.

**Tesseract** — le **moteur d'OCR** libre (version 5.5.3 ici), installé sans root dans `work/ocr/root/`. Il lit une image de page et rend du texte ; le dépôt l'appelle page à page, en `fra+eng`, après un rendu `pdftoppm` à 300 dpi en gris. Sa qualité se mesure par le **WER** (mot-clé : *WER*), pas à l'œil. *Voir* : `tools/ocr_pdf.py`, `tools/installer_ocr.sh`.

**Poppler (pdftotext, pdftoppm, pdfinfo)** — la **boîte à outils PDF** utilisée partout : `pdfinfo` donne le nombre de pages, `pdftotext` extrait la couche texte (absente sur un scan), `pdftoppm` rend les pages en images pour l'OCR. C'est `pdftotext` qui **décide** si un PDF est un scan : moins de 50 caractères par page, et il part à l'OCR. *Voir* : `tools/extrait_pdf.py`, `tools/ocr_pdf.py`.

**Licence** *(licence ; license)* — le **régime de droits** d'un corpus : CC-BY-SA 4.0 pour Wikipédia, « droits réservés, usage local, non diffusé » pour les livres et les notes de cours, « personnel » pour les documents. Elle est écrite dans le manifeste et dans la fiche ; un corpus sans licence nommée n'entre pas dans `reports/`.

**Genre** *(genre textuel ; genre)* — la **famille de texte** que le corpus représente : encyclopédie, livre, document administratif, notes de cours. Le dépôt la mesure par des indices simples — longueur moyenne de ligne, part de lignes dupliquées, couverture lexicale — avec `tools/compare_genres.py` ; c'est ce qui distingue une encyclopédie (103-147 car/ligne) d'un livre (32-38). *Voir* : `reports/rapport-genres.md`.

**Catalogue** *(catalogue de corpus ; catalogue)* — le **tableau récapitulatif** des corpus d'une même famille : une ligne par langue ou par fonds, avec le chiffre mesuré et le lien vers la fiche. Il se génère (`tools/catalogue_corpus.py --texte`) pour éviter les tableaux recopiés à la main qui divergent. *Voir* : `reports/rapport-corpus-wiki-texte.md`.

**Fonds** *(fonds documentaire ; collection)* — l'**ensemble d'origine** d'où viennent les documents, avant tout traitement : `Biblio_large` (les livres), `archives/CEGEP` (les notes de cours), `Documents` (les documents personnels). Un fonds a une licence et un parcours ; le corpus, lui, est ce qu'on en garde après filtre. *Voir* : `tools/extrait_pdf.py` (les racines), `reports/rapport-corpus-documents.md`.
