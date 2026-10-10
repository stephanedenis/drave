# C8 — la tête réflexe sur un texte JAMAIS VU : ÷79, et ce que ça dit de la généralisation

> Campagne : **cerveau** · expérience : adaptateur entraîné sur 7 morceaux de corpus, testé sur un 8ᵉ
> Question : la tête entraînée de l'expérience précédente était apprise sur la **première moitié
> d'un texte** et évaluée sur la **seconde** — les deux moitiés parlent du même sujet, avec le même
> vocabulaire. Alors : **une tête entraînée sur des textes sait-elle lire un texte qu'elle n'a
> JAMAIS vu ?**
> Verdict : **oui, et de deux ordres de grandeur, mais sept fois moins bien que sur le même texte** —
> sur le morceau de test (jamais vu), le chemin tronqué passe de **208 438,39** (tête empruntée,
> mesurée par le moteur) à **2 632,05** (adaptateur, meilleure époque 4) : **÷79**. Sur le même
> texte, la même recette donnait **÷540**. Le modèle complet vaut **10,3866** sur ce morceau : la
> tête généralisante reste **×253** derrière.
> Date réelle : **2026-10-10 13:40 HAE**.
> Protocole : `tools/c8_corpus.sh` (8 morceaux de 1 024 jetons pris à des endroits **différents** du
> corpus) puis `tools/c8_entrainer_tete.py --train m0..m6 --test m7`.

## 1. Le protocole, et pourquoi il change la question

| | expérience précédente | **celle-ci** |
|---|---|---|
| entraînement | première moitié d'un texte | **7 morceaux distincts** (jetons 0, 10k, 21k, …) |
| test | seconde moitié **du même texte** | **un morceau jamais vu**, pris ailleurs |
| ce que le chiffre mesure | l'adaptation au texte | la **généralisation** |

Les morceaux sont pris à des positions réparties dans tout le corpus (pas des fenêtres voisines),
et **les cibles de chaque morceau sont ses propres jetons** — un seul fichier d'identifiants pour
tous aurait donné des cibles étrangères aux états, c'est-à-dire un apprentissage sur du bruit qui
aurait « mesuré » que la tête ne généralise pas.

## 2. Les chiffres

| chemin (morceau 7, jamais vu, 1 024 jetons) | perplexité |
|---|---|
| tête **empruntée** (moteur, `--couches 0:16 --tete-partielle`) | 208 438,3879 |
| tête empruntée (même chaîne en Python, `A = identité`) | 207 427,5289 |
| **tête ENTRAÎNÉE** (adaptateur, époque 4) | **2 632,0454** |
| modèle complet (moteur, même morceau) | **10,3866** |

**÷79** sur la tête empruntée ; **×253** sous le modèle complet. Et la comparaison entre les deux
expériences, à protocole égal :

| protocole | tête empruntée | tête entraînée | gain |
|---|---|---|---|
| même texte (moitié/moitié) | 456 586,60 | 845,45 | **÷540** |
| **textes distincts** | 208 438,39 | 2 632,05 | **÷79** |

**La généralisation coûte un facteur 7** — et elle reste massive : la tête apprend quelque chose
qui **se transporte** d'un texte à l'autre, pas seulement une clé de lecture propre à un texte.

## 3. Le surapprentissage, encore, et c'est lui qui fixe le chiffre

| époque | entraînement (7 morceaux) | test (morceau 8) |
|---|---|---|
| 1 | 1 071 140,76 | 8 209,22 |
| 2 | 299,31 | 3 584,03 |
| **4** | **18,96** | **2 632,05** ← meilleur test |
| 6 | 3,52 | 3 780,72 |
| 10 | 1,30 | 13 328,02 |
| 20 | 1,08 | 45 448,70 |

L'adaptateur **apprend les morceaux d'entraînement par cœur** (perplexité 1,08) et se dégrade
ensuite sur le texte neuf. Le chiffre à lire est l'époque 4 (2 632), pas la dernière (45 449) —
c'est le script qui le sait et qui restaure la meilleure époque avant d'écrire le tableau.

## 4. Ce que ça change pour C8

**Acquis** : le maillon faible était la tête ; une tête **ajustée pour sa profondeur** rend le
réflexe utilisable (milliers au lieu de centaines de milliers) **même sur un texte qu'elle n'a
jamais vu** — et le chemin court va **×1,54 plus vite** en génération (mesuré, fiche
`rapport-c8-tete-entrainee.md` § 3 bis).

**Ce qui reste ouvert, et ce sont les vraies questions** :
- **7 morceaux de 1 024 jetons, c'est très peu** pour apprendre une lecture : la question devient
  « combien de textes pour combler les ×253 restants ? » — c'est un entraînement, pas une sonde ;
- **une tête linéaire** (l'adaptateur est une matrice) : une tête **non linéaire** devrait faire
  mieux, et c'est la prochaine marche ;
- **une seule profondeur** (16) : la courbe de la fiche `rapport-c8-sonde-profondeur.md` dit où
  l'information est lisible ; il reste à mesurer **qualité × vitesse** par profondeur pour choisir
  le point de fonctionnement ;
- **le coût du surapprentissage** : il faudrait une **régularisation** (pénalité, arrêt précoce
  systématique, plus de données) — ici, c'est l'arrêt précoce manuel qui a sauvé le chiffre.

## 5. Protocole, pour rejouer

```bash
tools/c8_corpus.sh 8 1024 16            # 8 morceaux pris à des endroits différents, états capturés
CUDA_VISIBLE_DEVICES=0 /home/stephane/gpu-env/bin/python tools/c8_entrainer_tete.py \
   --train /tmp/c8-corpus/etat-m0,...,/tmp/c8-corpus/etat-m6 \
   --test  /tmp/c8-corpus/etat-m7 \
   --ids /tmp/c8-corpus/morceau-7.txt --modele models/Qwen2.5-0.5B-Q8_0.gguf \
   --limite 1024 --epoques 20
```
