# Ce qui se consolide, c'est la STRUCTURE PARTAGÉE — même mémorisation (−22,5 %), transfert −7,4 % ou +1,2 %

> Campagne : **cerveau** · expérience : la consolidation sur **deux corpus**, et la **fusion** de
> deux expériences (latéralité / corps calleux).
> Question : la consolidation transfère-t-elle toujours, ou seulement quand le corpus a une
> structure **partagée** ? Et deux expériences différentes peuvent-elles tenir dans un seul modèle ?
> Verdict : **même mémorisation, transfert opposé.** Deux spécialistes, même modèle, même budget
> (LoRA rang 8 sur 8 couches) : sur le morceau **rejoué**, les deux gagnent **−22,7 %** (wikitext) et
> **−22,5 %** (corpus_en) — c'est de la mémorisation, et elle est identique. Sur un morceau **jamais
> vu du même corpus**, le premier gagne **−7,4 %** et le second **+1,2 %** (il perd). Ce qui se
> consolide est la **structure partagée** des textes rejoués : wikitext2 est un domaine unique,
> `corpus_en` en est plusieurs — et **la fusion des deux expériences garde le gain du fort et
> accumule les coûts du faible**.
> Date réelle : **2026-10-15 01 h 45-02 h 15 HAE** (heure lue sur la machine)
> Protocole : `tools/n4_dessin_b.py --objectif plein` · **A** : rejeu m0..m9 (wikitext2, 10 morceaux,
> 10 époques, graine 0) · **B** : rejeu des 10 puis 20 premiers morceaux de `/tmp/n4/ids-en.txt`
> (`data/corpus_en_val.txt` tokenisé, 15 époques) · export par `tools/exporter_gguf_dense.py` ·
> perplexité du **modèle complet**, mesurée par **le moteur**, sur des morceaux de 1 024 jetons.

## 1. Les deux spécialistes, sur trois morceaux chacun

| modèle | corpus | morceau **rejoué** | validation | **test** (jamais vu) |
|---|---|---:|---:|---:|
| base | wikitext2 | 9,4346 | — | 7,4250 |
| **A** (rejeu m0..m9) | wikitext2 | **7,2962 (−22,7 %)** | — | **6,8767 (−7,4 %)** |
| base | corpus_en | 25,0708 | 4,8110 | 17,1140 |
| **B2** (rejeu des 20 premiers) | corpus_en | **19,4392 (−22,5 %)** | 4,6391 (−3,6 %) | **17,3258 (+1,2 %)** |

Ce que ça dit :

* **la mémorisation est la même partout** : −22,7 % et −22,5 % sur le morceau rejoué — c'est le
  même mécanisme, au même prix, sur deux corpus que tout oppose (perplexité de base 9,4 contre
  25,1) ;
* **le transfert, lui, dépend du corpus** : −7,4 % sur wikitext2 (un domaine unique, un style
  d'article) contre **+1,2 %** sur `corpus_en` (2 Mo de textes divers). Adapter le modèle à vingt
  morceaux d'un corpus hétérogène ne l'améliore sur **aucun autre** morceau du même fichier ;
* **la colonne « validation » est un piège, et elle est écrite** : −3,6 % sur le morceau qui a servi
  à choisir l'époque. Ce n'est pas un transfert, c'est de la **sélection** — le seul chiffre honnête
  est la colonne « test », choisie avant de mesurer ;
* **conséquence pour le protocole de sommeil** : « consolider » n'est pas synonyme de « apprendre ».
  Ce qui s'apprend est ce que les textes rejoués ont **en commun** ; s'ils n'ont rien en commun, il
  ne reste que la mémorisation — utile pour un magasin (C6 l'épisodique), pas pour des poids.

## 2. La fusion de deux expériences (latéralité) : le gain du fort, les coûts du faible

Les deux spécialistes fusionnés en **sommant leurs déplacements** (`W + ΔA + ΔB`,
`exporter_gguf_dense.py --lora A,B`) :

| modèle | wikitext2 (m32) | corpus_en (test) |
|---|---:|---:|
| base | 7,4250 | 17,1140 |
| **A** seul | **6,8767 (−7,4 %)** | 17,2742 (+0,9 %) |
| **B** seul | 7,1461 (−3,8 %) | 17,1692 (+0,3 %) |
| **A + B** (somme) | **6,8845 (−7,3 %)** | 17,3228 (+1,2 %) |

* **la somme conserve exactement le gain du spécialiste fort** (−7,3 % contre −7,4 % pour A seul) :
  deux expériences **ne s'effacent pas** l'une l'autre, et c'est la première mesure de
  **continuité** du dépôt à l'échelle des poids (elle recoupe la fiche des deux nuits) ;
* **mais elle accumule aussi les coûts** : sur corpus_en, A coûte +0,9 %, B +0,3 %, et la somme
  **+1,2 %** — c'est-à-dire **plus** que chacun (l'effet des deux déplacements s'additionne) ;
* **et un bug a été attrapé par une ÉGALITÉ** : la première version de la fusion rangeait les
  adaptateurs dans un dictionnaire indexé par nom — le second fichier **écrasait** le premier, et
  « A+B » rendait **exactement** les chiffres de B (7,1461 et 17,1692, au chiffre près). C'est
  l'égalité qui a dénoncé le bug, pas une relecture : *deux nombres égaux ne prouvent pas qu'ils
  mesurent la même chose* — ici, ils prouvaient que l'un des deux n'était pas appliqué. La fusion
  **somme** désormais les déplacements (`echelle · B·A`), ce qui est exact même à échelles
  différentes.

## 3. Ce que ça change pour le cerveau

* **la consolidation n'est pas une faculté uniforme** : elle vaut ce que vaut la **structure
  partagée** du rejeu. Un cerveau qui dort sur une journée incohérente ne consolide rien de
  transférable — et le dépôt le mesure au lieu de l'espérer ;
* **l'arbitrage « consolider ou se souvenir » se précise** : quand le rejeu est hétérogène,
  consolider revient à mémoriser (−22 %) sans transférer (+1,2 %) — exactement ce que fait la
  mémoire épisodique (C6) **sans toucher aux poids** et pour 11 jetons sur 2 048 ;
* **la fusion des expériences est possible et sans interférence destructrice** (le gain de A
  survit à l'ajout de B) : c'est une **latéralité de fait**, obtenue par somme et non par échange
  d'activations — et elle vient après deux résultats négatifs sur l'échange (couches : gain nul ;
  experts : transfert nul) ;
* **ce qui reste ouvert** : fusionner deux spécialistes **forts** (ici B était faible) — la
  question « deux bons hémisphères valent-ils mieux qu'un ? » n'est pas tranchée par cette mesure.

## 4. Ce que cette fiche ne dit pas

* **un seul morceau de test par corpus** : « corpus_en ne transfère pas » repose sur **un** morceau
  (et la fiche de l'échelle a montré que le morceau pèse ×10) — il faudrait plusieurs morceaux de
  test par corpus, c'est la limite principale ;
* **deux corpus, un seul réglage** : ni le volume ni le taux ne sont ajustés par corpus ; un rejeu
  plus long sur `corpus_en` transférerait peut-être (le § 1 de la fiche du budget dit que la donnée
  paie — mais ici, 20 morceaux n'ont rien transféré) ;
* **la somme des déplacements n'est pas la seule fusion possible** : moyenne, concaténation,
  routage par entrée (un vrai corps calleux) ne sont pas essayés ;
* **rien sur la génération** : toutes les mesures sont des perplexités ;
* **le corpus_en n'est pas décrit** : « hétérogène » est une **hypothèse** qui explique le +1,2 %,
  et elle n'est pas mesurée (il faudrait mesurer la dispersion des morceaux, p. ex. la distance
  entre leurs distributions).
