# Le corpus de prose française depuis Wikipédia

> **Ligne de roadmap** : Données · **Date** : 2026-11-01 · **Verdict** : **2 525 902 articles**,
> **3,68 G caractères**, **593,6 M mots** de prose française, découpés en train/val/test par
> article, **0 fuite exacte** entre splits et **0/120 fenêtres** d'évaluation retrouvées dans
> l'entraînement. C'est le premier corpus local d'un autre ordre de grandeur que le dépôt
> (5,36 Mo uniques) — avec ses limites, écrites.

## 1. La source

La base `data/wikipedia/db/frwiki_v14.db` (7,25 Go, table `articles`) porte **2 755 035 articles**
et **7,0 Go de résumés** déjà débalisés : `page_id`, `title`, `summary`, `n_chars`, `n_words`. Le
champ `summary` est le **début** de l'article, tronqué à **8 000 caractères** — pas l'article
entier. C'est de la prose de lead et de début de sections, pas un dump complet.

Le texte intégral demanderait le dump `dumps/fr/frwiki-latest-pages-articles-multistream.xml.bz2`
(7,13 Go compressés) et un débaliseur complet : c'est le **prochain** chantier, pas celui-ci.

## 2. La méthode

`tools/corpus_wikipedia.py` :

1. **filtre** `n_chars >= 300` (2 526 107 articles lus) ;
2. **nettoie** : entités HTML, balises résiduelles, caractères de contrôle, espaces insécables ;
   **espace inséré aux jointures minuscule→majuscule** (« bourbonnaiseSa » → « bourbonnaise Sa »,
   ~92 700 dans 200 Mo, soit ~3,2 M sur le corpus) et **apostrophe restaurée** devant majuscule
   (« lOfficial » → « l' ») ;
3. **déduplique** les articles par empreinte BLAKE2b du texte normalisé (première occurrence
   gardée) ;
4. **découpe** en tronçons de 8 192 caractères aux frontières de mots — en pratique **1 tronçon
   par article**, puisque le résumé est plafonné à 8 000 caractères ; la déduplication de tronçons
   est donc, sur ce corpus, la déduplication d'articles ;
5. **sépare** train/val/test par **article** : hash salé de `page_id` modulo 1 000, 5 % val,
   5 % test — un article n'est jamais dans deux splits ;
6. écrit les trois fichiers et le manifeste [`corpus-wiki-fr.json`](corpus-wiki-fr.json) avec les
   chiffres et les empreintes SHA-256.

## 3. Ce qui est mesuré

| | valeur |
|---|---:|
| articles dans la base | 2 755 035 |
| articles lus (≥ 300 caractères) | 2 526 107 |
| articles gardés | **2 525 902** |
| doublons exacts retirés | 204 |
| caractères | **3 680 374 275** |
| mots (caractères / 6,2) | **593 608 754** |
| train | **2 273 294 articles · 3,43 Go** |
| val | **126 636 articles · 191 Mo** |
| test | **125 972 articles · 190 Mo** |
| tronçons | 2 525 902 (1 par article) |

Les trois fichiers ont leurs empreintes SHA-256 dans le manifeste. Les données ne sont **pas**
versionnées (`data/` est gitignoré), comme les autres corpus : le manifeste porte la provenance.

## 4. Les fuites, mesurées

`tools/verifie_contamination.py` :

- **doublons exacts de tronçons entre splits** : **0** en validation (0/126 636) et **0** en test
  (0/125 972) — la séparation par article et la déduplication globale le garantissent ;
- **recouvrement avec les jeux d'évaluation** : **0/30** fenêtres de 128 octets retrouvées dans
  l'entraînement pour chacun des quatre jeux testés — `corpus_propre/test`, `corpus_litt_propre/test`,
  `corpus_repo_propre/test`, `wikitext2_test` (voir
  [`corpus-wiki-fr-contamination.json`](corpus-wiki-fr-contamination.json)).

C'est un contrôle d'**exactitude** : une paraphrase, un résumé reformulé ou un quasi-doublon ne
sont **pas** détectés. La déduplication est exacte, pas sémantique.

## 5. Ce que le corpus vaut, et ce qu'il ne vaut pas

**Ce qu'il vaut.** 593 M mots de français réel, gratuit et local — cent fois la prose du dépôt
(5,36 Mo uniques), avec un split propre et une licence connue. C'est le stock qui manquait à N2
pour sortir du domaine.

**Ce qu'il ne vaut pas.** Ce sont des **résumés tronqués à 8 000 caractères**, pas des articles
entiers : la fin de chaque article manque, et le corpus est plus « lead » que « prose longue ».
Le débalisage de la base laisse des **artefacts** : dates de modèles vides (« né le à »), titres
de sections restés dans le texte (« Biographie Enfance et formation »), quelques parenthèses de
prononciation. La **déduplication est exacte** : les quasi-doublons (stubs similaires) restent.
Enfin, la licence est **CC-BY-SA 4.0** (et GFDL) : l'entraînement est libre, une **redistribution**
du corpus ou d'un modèle qui en reproduirait des passages demanderait attribution et partage à
l'identique — le corpus reste local, non diffusé.

## 6. Ce qu'on en fait

1. **N2** : c'est le corpus de prose française pour la recette `n2-propre` — remplacer
   `data/corpus_fr.txt` (0,79 M mots, source incertaine) par un échantillon de Wikipédia, à volume
   de budget constant, et mesurer la PPL en domaine et hors domaine.
2. **Filtrer** avant : retirer les articles-les-plus-courts (stubs < 1 000 caractères) et les
   pages de listes ; le corpus actuel garde tout ce qui fait ≥ 300 caractères.
3. **Nettoyer les artefacts** : un débaliseur de titres de sections et de modèles vides
   améliorerait la prose ; c'est un travail de qualité, pas de volume.
4. **Passer au texte intégral** : le dump `xml.bz2` (7,13 Go) + un débaliseur complet donnerait
   l'article entier — le vrai corpus long, à construire ensuite.

## 7. Ce qui pourrait rendre ce résultat faux

- **Le résumé n'est pas l'article** : 8 000 caractères plafonnés ; un article long est tronqué.
  La PPL mesurée sur ce corpus ne dit rien de la fin des articles.
- **Le débalisage de la base n'est pas le nôtre** : les dates vides et les titres de sections
  viennent du pipeline qui a construit `v14` ; on hérite de ses artefacts.
- **La déduplication est exacte** : les quasi-doublons restent et peuvent gonfler le volume
  apparent.
- **L'échantillon de contrôle est petit** : 30 fenêtres par jeu d'évaluation ; c'est un indice,
  pas une preuve exhaustive. Le contrôle exact des tronçons, lui, est exhaustif.

## Fichiers

- Outil : [`tools/corpus_wikipedia.py`](../tools/corpus_wikipedia.py) ·
  [`tools/verifie_contamination.py`](../tools/verifie_contamination.py).
- Manifeste : [`corpus-wiki-fr.json`](corpus-wiki-fr.json) (chiffres, SHA-256, licence, limites).
- Contamination : [`corpus-wiki-fr-contamination.json`](corpus-wiki-fr-contamination.json).
- Données : `data/corpus_wiki_fr/{train,val,test}.txt` (gitignorées, 3,8 Go).
