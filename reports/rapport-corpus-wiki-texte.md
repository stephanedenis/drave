# Le texte intégral de Wikipédia — le pilote et le run FR

> **Verdict.** Le débaliseur `tools/corpus_wikipedia_texte.py` a produit le **texte intégral** du
> français : **2 388 219 articles**, **8,025 G caractères**, **1,294 G mots** (estimés), **8,34 Go**,
> résidus **1 / 20 000 lignes** (`{{`), **0 / 49 655** fenêtres de 8 Ko de la validation et
> **0 / 49 148** du test retrouvées dans l'entraînement, **0 / 40** fenêtres sur les cinq jeux
> d'évaluation. Le texte intégral vaut **2,18×** les résumés (3,68 Go) — et non les 7× du pilote :
> le pilote n'était pas représentatif.
>
> **Date** : 2026-11-01. **Ligne** : Données (D/R/A). **Machine** : CPU seul.

## 1. La source

Les corpus `data/corpus_wiki_<langue>/` sont les **résumés** (`summary`) de la base v14,
**tronqués à 8 000 caractères**. Le dump `frwiki-latest-pages-articles-multistream.xml.bz2`
(**7,13 Go** compressés, **5 968 207 pages**) porte les **articles entiers**. Le run complet donne
**3,36 Ko par article** en moyenne (contre **1,46 Ko** de résumé) : **2,18×** de texte, la prose
entière, les sections, les listes, les paragraphes. Le **pilote** des 100 000 premiers `page_id`
donnait **10,45 Ko** par article — les articles les plus anciens sont les plus longs ; ce n'est
pas un échantillon aléatoire, et la projection de 26 Go qu'il suggérait est **réfutée** par le
run (8,34 Go).

## 2. La méthode

`tools/corpus_wikipedia_texte.py` :

1. lit le dump en flux (`bz2` + `ElementTree.iterparse`) ;
2. garde l'espace de noms 0, sans redirection ; filtre `< 300` caractères ;
3. **débalise** : commentaires, `<ref>`, tableaux `{| … |}`, modèles `{{ … }}` (30 itérations),
   fichiers et catégories retirés, **liens remplacés par leur libellé**, titres de sections
   conservés, listes décapitées, entités HTML décodées, `&nbsp;` normalisé ;
4. **déduplique** les articles (BLAKE2b) et les tronçons de l'entraînement ;
5. **sépare** par article (hash salé du `page_id`, 5 % val, 5 % test) ;
6. écrit `train/val/test.txt` (tronçons de 8 192 caractères, coupés aux mots), le **SHA-256** des
   trois fichiers et le **manifeste** JSON.

## 3. Le pilote (100 000 articles)

| grandeur | valeur |
|---|---:|
| pages lues | 146 250 |
| articles gardés | **100 000** |
| redirections écartées | 31 998 |
| articles trop courts (< 300 car.) | 3 574 |
| caractères gardés | **1 045 085 924** |
| mots estimés (car. / 6,2) | **168 562 245** |
| train / val / test | 972,6 Mo / 56,3 Mo / 52,7 Mo |
| résidus (`{{` / `[[` / `<`) sur 20 000 lignes | **1 / 0 / 3** |

## 4. Le run complet (2 388 219 articles)

| grandeur | valeur |
|---|---:|
| pages lues | **5 968 207** |
| articles gardés | **2 388 219** |
| redirections écartées | 1 827 807 |
| autres espaces de noms | 1 385 362 |
| articles trop courts | 366 649 |
| doublons d'articles | 170 |
| caractères gardés | **8 025 059 777** |
| mots estimés (car. / 6,2) | **1 294 364 480** |
| tronçons (8 192 car.) | 2 755 825 (783 doublons) |
| train / val / test | 7,50 Go / 419,6 Mo / 415,3 Mo |
| articles train / val / test | 2 149 330 / 119 866 / 119 023 |
| résidus (`{{` / `[[` / `<`) sur 20 000 lignes | **1 / 0 / 3** |

**Aucune fuite entre splits.** Les **jeux d'évaluation** (XNLI fr, UDHR, trois jeux locaux)
donnent **0 / 40** fenêtres chacun. Au **niveau du tronçon réel (8 Ko)**, **0 / 49 655** (validation)
et **0 / 49 148** (test) fenêtres sont dans l'entraînement. Le contrôle standard (unité = ligne)
signale 5,53 % et 5,47 % de lignes dupliquées — ce sont les **titres de sections répétés**
(« Biographie », « Notes et références »…) et les lignes de boîte, pas de la prose ; la fiche
nomme la limite de ce contrôle et le contrôle 8 Ko qui le corrige.

**Ce que le débaliseur perd** : les **infobox** et les dates de modèles, les **formules `<math>`**,
les **tableaux** ; les liens deviennent des libellés, les titres de sections restent. C'est de la
**prose encyclopédique**, pas l'article complet mis en forme.

## 5. Ce qui pourrait être faux

- **Le pilote n'est pas un échantillon aléatoire** : les 100 000 premiers `page_id` sont les
  articles les plus anciens, deux fois plus longs en moyenne (10,45 Ko contre 3,36 Ko) ; la
  projection de 26 Go était **fausse** (8,34 Go au run). C'est le run qui fait foi.
- **Le débaliseur est regex** : les modèles non fermés, les tableaux imbriqués et les liens de
  légende peuvent laisser des résidus au-delà des 20 000 lignes mesurées.
- **La déduplication est exacte** : les quasi-doublons (traductions, copies) restent.
- **La licence** : CC-BY-SA 4.0 (et GFDL) — le corpus reste local, l'attribution et le partage à
  l'identique s'appliquent à toute diffusion.
- **Le contrôle 8 Ko est ad hoc** : il mérite d'entrer dans `verifie_contamination.py` comme
  option de taille de tronçon.
- **La langue** : seul le français est fait ; les neuf autres suivent le même outil.

## 6. La suite

Les **neuf autres langues** (`--langue de`, `en`, `es`, `it`, `ja`, `pt`, `ru`, `zh`, `ar`), puis
l'**extraction PDF native et OCR** (les 104 livres, les 2 711 PDF du CEGEP, les collections) avec
leurs licences, puis la **préparation de R1.1/R1.2**.

## Fichiers

- `tools/corpus_wikipedia_texte.py` — l'outil (dump → texte intégral).
- `reports/corpus-wiki-fr-texte.json` — le manifeste du run complet (SHA-256 des trois fichiers).
- `reports/corpus-wiki-fr-texte-contamination.json` — le contrôle du run complet.
- `reports/corpus-wiki-fr-texte-pilote.json` — le manifeste du pilote (archivé pour comparaison).
- `reports/corpus-wiki-fr-texte-pilote-contamination.json` — le contrôle du pilote.
- `data/corpus_wiki_fr_texte/` — le corpus (8,34 Go, gitignoré).
