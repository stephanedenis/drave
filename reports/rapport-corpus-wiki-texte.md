# Le texte intégral de Wikipédia — le français et les neuf langues

> **Verdict.** Le débaliseur `tools/corpus_wikipedia_texte.py` a produit le **texte intégral** du
> français : **2 388 219 articles**, **8,025 G caractères**, **1,294 G mots** (estimés), **8,34 Go**,
> résidus **1 / 20 000 lignes** (`{{`), **0 / 51 250** fenêtres de 8 Ko de la validation et
> **0 / 50 730** du test retrouvées dans l'entraînement, **0 / 40** sur le XNLI et les trois jeux
> locaux, **2 / 24** pour l'UDHR — **citée dans Wikipédia**. Les huit premiers autres corpus
> (ar, pt, zh, ja, it, ru, es, de) sont mesurés : **8 Ko à zéro partout**, l'UDHR portugaise (2/40) et japonaise
> (1/23) citées. Le texte intégral vaut **2,18×** les résumés (3,68 Go) — et non les 7× du pilote :
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

**Aucune fuite de prose entre splits.** Le **XNLI fr** et les **trois jeux locaux** donnent
**0 / 40** fenêtres chacun ; l'**UDHR** donne **2 / 24** — l'UDHR est **citée dans Wikipédia** (le
français rejoint l'italien, le japonais et le portugais), ce n'est donc pas un jeu tenu à l'écart
pour lui. Au **niveau du tronçon réel (8 Ko)**, **0 / 51 250** (validation) et **0 / 50 730**
(test) fenêtres sont dans l'entraînement. Le contrôle standard (unité = ligne) signale 5,53 % et
5,47 % de lignes dupliquées — ce sont les **titres de sections répétés**
(« Biographie », « Notes et références »…) et les lignes de boîte, pas de la prose ; la fiche
nomme la limite de ce contrôle et le contrôle 8 Ko qui le corrige.

**Ce que le débaliseur perd** : les **infobox** et les dates de modèles, les **formules `<math>`**,
les **tableaux** ; les liens deviennent des libellés, les titres de sections restent. C'est de la
**prose encyclopédique**, pas l'article complet mis en forme.

## 5. Les neuf autres langues

Même outil, même chaîne. Les neuf premiers corpus (fr, ar, pt, zh, ja, it, ru, es, de) sont mesurés ; le dernier (en) est
en cours au 1/11 20 h. Les neuf mesurés : **14,51 M articles**, **45,54 G caractères**, **59,0 Go**.
La table se régénère depuis les manifestes : `python3 tools/catalogue_corpus.py --texte`.

| langue | articles | caractères | mots (car. / 6,2) | octets | fuite lignes | fuite 8 Ko | éval | résidus `{{`/`[[`/`<` |
|---|---:|---:|---:|---:|---:|---:|---|---|
| fr | 2 388 219 | 8,025 G | 1 294 M | 8,34 Go | 5,5 % | **0** | XNLI 0/40, UDHR 2/24 (citée) | 1/0/3 |
| ar | 1 000 310 | 1,994 G | 322 M | 3,57 Go | 28,9 % | **0** | XNLI 0/40 | 1/161/0 |
| pt | 970 793 | 3,104 G | 501 M | 3,21 Go | 4,5 % | **0** | UDHR 2/40 (citée) | 1/296/0 |
| zh | 643 122 | 1,045 G | — (caractères) | 2,63 Go | 2,2 % | **0** | XNLI 0/40 | 14/0/0 |
| ja | 1 271 107 | 2,809 G | 453 M | 7,33 Go | 3,7 % | **0** | UDHR 1/23 (citée) | 2/62/0 |
| it | 1 561 411 | 5,211 G | 840 M | 5,29 Go | 6,2 % | **0** | UDHR 2/23 (citée) | 0/0/0 |
| ru | 1 943 725 | 6,258 G | 1 009 M | 11,16 Go | 18,0 % | **0** | XNLI 0/40 | 0/52/0 |
| es | 1 868 078 | 6,651 G | 1 073 M | 6,83 Go | 6,3 % | **0** | XNLI 0/40 | 1/228/1 |
| de | 2 864 934 | 10,443 G | 1 684 M | 10,68 Go | 4,7 % | **0** | XNLI 0/40 | 0/15/0 |
| en | en cours | | | | | | | |

**Lecture.** Le **8 Ko est à zéro partout** : aucune unité d'entraînement ne traverse les splits.
Les **lignes** dupliquées sont un diagnostic de style : 28,9 % en arabe (les formules, les
références et les phrases coraniques se répètent d'un article à l'autre) et **18,0 % en russe** (les
dates, les références, les formules soviétiques), 6,3 % en espagnol, 4,7 % en allemand, 6,2 % en italien, 4,5 % en
portugais, 3,7 % en japonais, 2,2 % en chinois — ce ne sont pas des fuites de tronçon. L'**UDHR** est citée dans Wikipédia pour le
français, le portugais et l'italien (2 fenêtres) et le japonais (1) ; le **XNLI** est à 0 pour le français,
l'arabe et le chinois.
Le débaliseur laisse des liens `[[…]]` résiduels en arabe (161 lignes sur 20 000) et en portugais
(296) : les légendes et notes complexes ; c'est une limite nommée, une passe finale les enlèvera.

## 6. Ce qui pourrait être faux


- **Le pilote n'est pas un échantillon aléatoire** : les 100 000 premiers `page_id` sont les
  articles les plus anciens, deux fois plus longs en moyenne (10,45 Ko contre 3,36 Ko) ; la
  projection de 26 Go était **fausse** (8,34 Go au run). C'est le run qui fait foi.
- **Le débaliseur est regex** : les modèles non fermés, les tableaux imbriqués et les liens de
  légende peuvent laisser des résidus au-delà des 20 000 lignes mesurées.
- **La déduplication est exacte** : les quasi-doublons (traductions, copies) restent.
- **La licence** : CC-BY-SA 4.0 (et GFDL) — le corpus reste local, l'attribution et le partage à
  l'identique s'appliquent à toute diffusion.
- **Le contrôle 8 Ko** est dans `verifie_contamination.py --taille-troncon 8192` ; les
  **jeux d'évaluation** sont extraits par langue (`tools/extraire_evals_langues.py`) — l'UDHR
  reste **citée** dans Wikipédia pour le fr, l'it, le ja et le pt.
- **Les liens résiduels** : l'arabe (161 lignes sur 20 000) et le portugais (296) gardent des
  `[[…]]` dans les légendes et notes complexes ; la passe finale est à faire.
- **Les langues** : quatre corpus sont mesurés (fr, ar, pt, zh) ; les six autres suivent.

## 7. La suite

Les **six langues restantes** (`de`, `en`, `es`, `it`, `ja`, `ru`), puis le **catalogue complet des dix**, puis
l'**extraction PDF native et OCR** (les 104 livres, les 2 711 PDF du CEGEP, les collections) avec
leurs licences, puis la **préparation de R1.1/R1.2**.

## Fichiers

- `tools/corpus_wikipedia_texte.py` — l'outil (dump → texte intégral).
- `tools/extraire_evals_langues.py` — les jeux d'évaluation par langue.
- `tools/catalogue_corpus.py --texte` — la table du texte intégral, depuis les manifestes.
- `reports/corpus-wiki-fr-texte.json` — le manifeste du run complet (SHA-256 des trois fichiers).
- `reports/corpus-wiki-fr-texte-contamination.json` — le contrôle du run complet.
- `reports/corpus-wiki-fr-texte-pilote.json` — le manifeste du pilote (archivé pour comparaison).
- `reports/corpus-wiki-fr-texte-pilote-contamination.json` — le contrôle du pilote.
- `reports/corpus-wiki-{ar,pt,zh,ja,it,ru,es,de}-texte.json` + `-contamination.json` — les huit premiers autres corpus.
- `data/corpus_wiki_fr_texte/` — le corpus (8,34 Go, gitignoré).
