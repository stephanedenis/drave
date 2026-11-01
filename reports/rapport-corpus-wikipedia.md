# Les corpus Wikipédia par langue

> **Ligne de roadmap** : Données · **Date** : 2026-11-01 · **Verdict** : **10 langues**,
> **21 630 731 articles**, **31,42 G caractères**, **4 643 M mots** (langues à espaces ; ja/zh
> comptés en caractères), **38,8 Go** de prose, splits par article, **0 fuite exacte** entre
> splits, échantillons d'évaluation **0/30** partout sauf l'UDHR citée (it/ja, 1/23) — le stock
> multilingue qui manquait, avec ses limites écrites.

## 1. La source

Dix bases `data/wikipedia/db/<langue>wiki_v14.db`, une par langue (ar, de, en, es, fr, it, ja, pt,
ru, zh), **66 Go** au total. La table `articles` porte `page_id`, `title`, `summary`, `n_chars`,
`n_words` ; le champ `summary` est le **début** de l'article, tronqué à **8 000 caractères** et
déjà débalisé par le pipeline qui a construit `v14`. C'est de la prose de lead et de début de
sections, pas l'article entier.

Le texte intégral demanderait les dumps `xxwiki-latest-pages-articles-multistream.xml.bz2` (67 Go
compressés pour les 10 langues) et un débaliseur complet : c'est le **prochain** chantier.

## 2. La méthode, commune aux dix langues

`tools/corpus_wikipedia.py` :

1. **filtre** `n_chars >= 300` ;
2. **nettoie** : entités HTML, balises résiduelles, caractères de contrôle, espaces insécables ;
   espace inséré aux **jointures minuscule→majuscule** (« bourbonnaiseSa » → « bourbonnaise Sa »,
   ~92 700 dans 200 Mo de français, soit ~3,2 M sur le FR) et **apostrophe restaurée** devant
   majuscule (« lOfficial » → « l' ») — sans effet sur les écritures sans casse (ar, ja, zh) ;
3. **déduplique** les articles par empreinte BLAKE2b du texte normalisé (première occurrence
   gardée) ;
4. **découpe** en tronçons de 8 192 caractères aux frontières de mots — en pratique **un tronçon
   par article** pour les langues à espaces (le résumé est plafonné à 8 000) ; pour le japonais et
   le chinois, sans espaces, la coupe est franche ;
5. **sépare** train/val/test par **article** : hash salé de `page_id` modulo 1 000, 5 % val, 5 %
   test — un article n'est jamais dans deux splits ;
6. écrit `train.txt`, `val.txt`, `test.txt` et un manifeste par langue avec les chiffres, les
   empreintes SHA-256 et les limites.

Les données ne sont **pas** versionnées (`data/` est gitignoré), comme les autres corpus : les
manifestes portent la provenance et les empreintes.

## 3. Les dix corpus

| langue | articles | caractères | mots (est.) | train / val / test | manifeste |
|---|---:|---:|---:|---:|---|
| **fr** | 2 525 902 | 3.68 G | 594 M | 3.43 Go / 191 Mo / 190 Mo | [`corpus-wiki-fr.json`](corpus-wiki-fr.json) |
| **en** | 6 552 645 | 9.91 G | 1599 M | 8.98 Go / 498 Mo / 498 Mo | [`corpus-wiki-en.json`](corpus-wiki-en.json) |
| **de** | 2 884 427 | 4.72 G | 762 M | 4.33 Go / 240 Mo / 240 Mo | [`corpus-wiki-de.json`](corpus-wiki-de.json) |
| **es** | 1 900 560 | 2.79 G | 451 M | 2.57 Go / 143 Mo / 142 Mo | [`corpus-wiki-es.json`](corpus-wiki-es.json) |
| **ru** | 1 956 216 | 2.93 G | 473 M | 4.66 Go / 259 Mo / 257 Mo | [`corpus-wiki-ru.json`](corpus-wiki-ru.json) |
| **it** | 1 592 477 | 2.26 G | 365 M | 2.06 Go / 114 Mo / 114 Mo | [`corpus-wiki-it.json`](corpus-wiki-it.json) |
| **ja** | 1 355 856 | 1.76 G | — (caractères) | 3.97 Go / 220 Mo / 220 Mo | [`corpus-wiki-ja.json`](corpus-wiki-ja.json) |
| **zh** | 823 401 | 0.87 G | — (caractères) | 1.89 Go / 104 Mo / 105 Mo | [`corpus-wiki-zh.json`](corpus-wiki-zh.json) |
| **pt** | 991 389 | 1.35 G | 218 M | 1.25 Go / 70 Mo / 70 Mo | [`corpus-wiki-pt.json`](corpus-wiki-pt.json) |
| **ar** | 1 047 858 | 1.13 G | 183 M | 1.78 Go / 98 Mo / 98 Mo | [`corpus-wiki-ar.json`](corpus-wiki-ar.json) |

**Total : 21 630 731 articles · 31.42 G caractères · 4643 M mots (langues à espaces ; ja/zh comptés en caractères) · 38.8 Go**

Les trois fichiers sont `train.txt`, `val.txt`, `test.txt` (UTF-8, un article par bloc, tronçons séparés par deux sauts de ligne). Les données ne sont pas versionnées ; les manifestes portent les chiffres et les empreintes SHA-256.

## 4. Les fuites, mesurées

`tools/verifie_contamination.py` sur chaque langue :

- **doublons exacts de tronçons entre splits** : **0** partout (0/126 636 et 0/125 972 pour le
  français, 0/52 203 et 0/52 033 pour l'arabe, 0/327 337 et 0/327 877 pour l'anglais, 0/97 650 et
  0/97 198 pour le russe, etc. — le détail est dans le JSON) ;
- **recouvrement avec un jeu d'évaluation aligné** : 30 fenêtres de 128 octets par langue,
  cherchées dans l'entraînement — **XNLI** pour ar/de/en/es/fr/ru/zh (0/30 partout),
  **wikitext2** pour l'anglais (0/30), jeux locaux pour le français (0/30 sur les trois),
  **UDHR** pour it/ja/pt. L'UDHR donne **1/23** pour l'italien et le japonais et 0/30 pour le
  portugais : c'est la **citation de l'UDHR dans Wikipédia**, pas un défaut du corpus — mais
  l'UDHR n'est donc pas un jeu d'évaluation tenu à l'écart pour ces deux langues. Résultats
  complets dans [`corpus-wikipedia-contamination.json`](corpus-wikipedia-contamination.json).

C'est un contrôle d'**exactitude** : une paraphrase, un résumé reformulé ou un quasi-doublon ne
sont **pas** détectés. La déduplication est exacte, pas sémantique.

## 5. Ce que ces corpus valent, et ce qu'ils ne valent pas

**Ce qu'ils valent.** De la prose réelle, locale et gratuite, dans dix langues, avec un split
propre et une licence connue — le stock qui manquait à N2 pour sortir du dépôt (5,36 Mo uniques de
prose française) et aux autres agents pour le multilingue.

**Ce qu'ils ne valent pas.** Des **résumés tronqués à 8 000 caractères**, pas des articles
entiers : la fin de chaque article manque, et les corpus sont plus « lead » que « prose longue ».
Le débalisage de la base laisse des **artefacts** : dates de modèles vides (« né le à »), titres de
sections restés dans le texte, parenthèses de prononciation. La **déduplication est exacte** : les
quasi-doublons restent. Le volume en **mots** est estimé par `caractères / 6,2` : c'est faux pour
le japonais et le chinois, où le **caractère** est l'unité — les manifestes le disent.

**Licence.** Wikipédia est **CC-BY-SA 4.0** (et GFDL) : l'entraînement est libre, une
**redistribution** du corpus ou d'un modèle qui en reproduirait des passages demanderait
attribution et partage à l'identique. Les corpus restent locaux, non diffusés.

## 6. Où les agents les trouvent

| besoin | corpus | chemin |
|---|---|---|
| pré-entraînement français | `fr` | `data/corpus_wiki_fr/` · manifeste [`corpus-wiki-fr.json`](corpus-wiki-fr.json) |
| pré-entraînement anglais | `en` | `data/corpus_wiki_en/` · manifeste [`corpus-wiki-en.json`](corpus-wiki-en.json) |
| allemand, espagnol, russe, italien | `de`, `es`, `ru`, `it` | `data/corpus_wiki_<langue>/` |
| japonais, chinois, portugais, arabe | `ja`, `zh`, `pt`, `ar` | `data/corpus_wiki_<langue>/` |

Les trois fichiers sont `train.txt`, `val.txt`, `test.txt` (UTF-8, un article par bloc, tronçons
séparés par deux sauts de ligne). La commande qui refait tout :

```
python3 tools/corpus_wikipedia.py --toutes-les-langues
```

et celle qui refait la table :

```
python3 tools/catalogue_corpus.py
```

## 7. Ce qui pourrait rendre ces corpus faux

- **Le résumé n'est pas l'article** : 8 000 caractères plafonnés ; la PPL mesurée dessus ne dit
  rien de la fin des articles.
- **Le débalisage de la base n'est pas le nôtre** : on hérite de ses artefacts.
- **La déduplication est exacte** : les quasi-doublons restent et peuvent gonfler le volume.
- **L'échantillon de contrôle est petit** : 30 fenêtres par langue ; c'est un indice, pas une
  preuve exhaustive. Le contrôle exact des tronçons, lui, est exhaustif.
- **Le découpage par article** garantit l'absence de fuite exacte entre splits, pas l'absence de
  fuite entre un corpus et un futur jeu d'évaluation qui n'existe pas encore.

## Fichiers

- Outils : [`tools/corpus_wikipedia.py`](../tools/corpus_wikipedia.py) (extraction/nettoyage/split, `--toutes-les-langues`) ·
  [`tools/verifie_contamination.py`](../tools/verifie_contamination.py) ·
  [`tools/catalogue_corpus.py`](../tools/catalogue_corpus.py) (la table ci-dessus, depuis les manifestes).
- Manifestes : `reports/corpus-wiki-<langue>.json` (un par langue, chiffres + SHA-256 + limites).
- Contamination : [`corpus-wikipedia-contamination.json`](corpus-wikipedia-contamination.json).
- Données : `data/corpus_wiki_<langue>/{train,val,test}.txt` (gitignorées, 38,8 Go).
