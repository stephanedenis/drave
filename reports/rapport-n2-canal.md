# N2.l — Le canal de structure : +5 % de PPL, et le même alphabet

> **Ligne de roadmap** : N2 (et le canal d'annotation de S) · **Date** : 2026-11-01 ·
> **Verdict** : donner au modèle une **classe de structure par octet** (mot plein, mot
> grammatical, espace, ponctuation, chiffre, frontière) baisse la PPL de **4,3893 à 4,1738** à
> 128 octets, **4,4905 à 4,2143** à 256 et **5,6691 à 5,4460** à 512 — pour **1 344 paramètres**.
> Mais le modèle ne devient pas plus **robuste au mélange des lettres** (×5,6 comme la référence) :
> le canal est un **prior utile**, pas une lecture de formes.

## La question

La typoglycémie (N2.h, ×17,8) a montré que le modèle lit des **lettres**. L'idée du canal est de
lui donner, en entrée, ce qu'il ne sait pas voir : une **classe de structure** par octet, produite
par un outil déterministe (le générateur de [`tools/structures`](../tools/structures/)). Deux
questions : le canal **aide-t-il** ? et fait-il **résister au mélange** (si le modèle s'appuie sur
la structure, la bouillie de lettres devrait coûter moins) ?

## Le dispositif

- **Canal** : [`tools/canal_structure.py`](../tools/canal_structure.py) — 6 classes par octet,
  alignées 1:1 (vérifié : 186 089 472 octets de texte, 186 089 472 de canal) ; classes issues du
  générateur (lexique des mots grammaticaux, ponctuation, chiffres).
- **Modèle** : `NativeModel` gagne une embedding de canal (6 × 224 = **1 344** paramètres),
  ajoutée à l'embedding d'octet et à la position ; `canal=None` reproduit le modèle d'avant.
- **Entraînement** : 20 000 pas × 8 × 128, positions aléatoires [0, 384], lr 3e-4, graine 1, sur
  les 186 Mo du corpus réel — la même recette que N2.j2.
- **Contrôles** : la base sans canal (`base-wiki-pos.pt`, N2.j2), et un **placebo** — le même
  canal, **mélangé** (mêmes classes, même distribution, structure détruite).

## Ce qui est mesuré

| modèle | 128 | 256 | 512 | mélange « milieu » | mélange « tout » |
|---|---:|---:|---:|---:|---:|
| **sans canal** (N2.j2) | 4,3893 | 4,4905 | 5,6691 | ×5,6 | ×10,0 |
| **canal** | **4,1738** | **4,2143** | **5,4460** | ×5,6 | ×10,3 |
| **placebo** | 4,5154 | 4,5617 | 5,8656 | ×5,4 | ×9,8 |

**Ablation** : le modèle entraîné avec le canal, évalué **sans** lui, tombe à **9,60** (128),
**9,70** (256), **10,36** (512) — il s'appuie massivement sur le canal. C'est attendu : le canal
est disponible à l'inférence (l'outil est déterministe), mais un canal absent ou faux coûte cher.

## Lecture

Le canal réel **gagne** : −0,22 sur la base sans canal (4,1738 contre 4,3893) et **−0,34 sur le
placebo** (4,5154) — et le placebo est **pire que la base**, ce qui est le signe qu'un canal
aléatoire est du **bruit**, pas un paramètre neutre. Le gain vient donc de la **structure**, pas de
l'embedding supplémentaire.

Mais la **robustesse au mélange est identique** : ×5,6 dans les trois cas. Le canal aide le modèle
à prédire le prochain octet — il ne lui apprend pas à reconnaître des **formes**. L'hypothèse de
départ (un prior de forme rendrait le mélange moins coûteux) est **infirmée** : le modèle reste un
lecteur de lettres, avec un meilleur dictionnaire de contexte.

L'**ablation** est le résultat le plus instructif : sans canal à l'inférence, le modèle tombe à
9,60. Le canal est donc devenu une **dépendance** — acceptable parce que l'outil est déterministe
et disponible, mais il faut le savoir : un canal absent ou faux coûte très cher.

## Ce que ça change pour N2

Le canal entre dans la recette comme un **prior bon marché** : 1 344 paramètres, −5 % de PPL,
et il ne change pas le reste (positions, longueur). Pour la ligne R, c'est un moyen de faire entrer
la structure dans le modèle **sans la retirer du texte** — exactement l'inverse du filtre non
ambigu (N2.j), qui perdait du signal.

Reste la question de fond : le canal ne rend pas le modèle **robuste aux formes**. Un encodeur de
mots (E2, le pooling de n-grammes) reste la piste pour ça — et il faudra le juger sur le mélange,
pas seulement sur la PPL.

## Ce qui pourrait le rendre faux

- **Une seule graine** ; le gain (−0,22) est petit et pourrait être du bruit d'entraînement — le
  placebo tranche.
- **Le canal est une hypothèse grammaticale** : le lexique des mots grammaticaux est imparfait,
  et une classe fausse est un prior faux (l'ablation le montre).
- **Le canal n'est pas appris** : c'est un outil déterministe, donc il n'apprend rien de nouveau —
  il **ajoute** une information que le modèle ne pouvait pas déduire localement.
- **La mesure est en domaine** : la PPL sur le wiki ne dit rien du transfert hors domaine.

## Fichiers

- Outil : [`tools/canal_structure.py`](../tools/canal_structure.py) ; modèle :
  [`tools/native_model.py`](../tools/native_model.py) (`embed_canal`) ; trainer :
  [`tools/entrainer_native.py`](../tools/entrainer_native.py) (`--canal`).
- Canal : `data/wiki_fr/propre/{train,val,test}.canal`, `train.canal-placebo`.
- Points de contrôle : `work/n2j/base-canal.pt`, `base-placebo.pt` ; mesures :
  `work/n2j/eval-canal.json`, `typo-base.json`.
