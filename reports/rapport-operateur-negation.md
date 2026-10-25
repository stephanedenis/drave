# B4.1 — la négation n'est pas une opération portée par l'état

> Mesure du 24/10/2026, **Qwen2.5-1.5B-Instruct**, couche **22** (le pic de la sonde : 0,8103 sur DACCORD),
> 723 paires d'entraînement, 311 de test, `tools/operateur_negation.py`.

## Le protocole

- On entraîne la sonde sur les paires **originales** (prémisse, hypothèse, étiquette 0/1).
- On **nie l'hypothèse** (« Il est faux que : H ») — l'étiquette **doit basculer** (`1 − y`).
- On relit l'état des paires **niées** : la sonde, entraînée sur l'original, doit lire l'étiquette **basculée** si
  la négation est une opération portée par l'état ; sinon elle relit l'originale.

## Les résultats

| | |
|---|---:|
| référence (paires originales) | **0,8103** |
| **flip** — le nié, étiquette basculée | **0,4148** |
| **garde** — le nié, étiquette originale | **0,5852** |
| flip (MLP) | 0,3698 |
| garde (MLP) | 0,6302 |
| contrôle (étiquettes mélangées) | 0,4566 |

## Ce que ça dit

- **La négation n'est pas portée par l'état** : le flip (0,4148) est **sous** le hasard (0,5) et la garde (0,5852)
  **au-dessus**. La sonde relit l'étiquette **originale** sur les paires niées : elle lit la **relation de
  surface**, pas l'**opération**.
- **La référence (0,8103) tient** : l'état porte bien la relation entre la prémisse et l'hypothèse — il ne porte pas
  la **composition** de la négation. C'est exactement la distinction de l'étage 2 : *lire le sens* (fait) vs
  *opérer sur le sens* (échoue).
- Le contrôle au hasard est propre (0,4566) : rien de parasitaire.

## B4.2 — la négation est APPRENABLE (mais pas par transfert)

| | |
|---|---:|
| sonde entraînée sur le nié → le nié | **0,7042** |
| sonde entraînée sur le nié → l'original | 0,3312 (sous le hasard : les géométries sont opposées) |
| contrôle (étiquettes mélangées) | 0,4952 |

**La négation est dans l'état** : une sonde **réentraînée** sur les paires niées lit la relation basculée à
**0,7042** (hasard 0,5), avec un contrôle propre. Mais elle **ne se transfère pas** : la sonde de l'original ne lit
pas le nié (0,4148) et réciproquement (0,3312). *L'opérateur n'est pas une direction : c'est une **géométrie
locale** — exactement la leçon du plan (« les géométries sont locales aux tâches », synthèse 05).*

**Ce que ça change pour B4** : l'opération n'est **pas** un vecteur à ajouter, c'est un **réapprentissage**. C'est
cohérent avec tout le reste : le plan avait dû être entraîné (mesure 119) ; la composition est alignée par un pont
(0,76/0,865) mais le plan résiste. **B4.3** : un opérateur appris sur une **paire** d'opérations transfère-t-il à une
autre, ou faut-il un réapprentissage par opération ?

## B4.3 — les deux opérations tiennent dans **un seul** opérateur

| | |
|---|---:|
| le mélange (l'original + le nié) → l'original | **0,7749** |
| le mélange → le nié | **0,6977** |
| contrôle (le mélange, étiquettes mélangées) | 0,4791 |

**Les deux opérations coexistent** dans un seul opérateur linéaire : entraîné sur le **mélange**, il lit l'original
à **0,7749** et le nié à **0,6977** — le coût de la jointure est faible (l'original perd 0,035 par rapport à la
sonde seule, le nié 0,006). *L'opérateur n'est ni une direction ni deux géométries séparées : c'est un
**sous-espace** — une relation et une polarité — que la sonde du mélange sépare.*

**Ce que ça dit sur l'étage 2** : une opération n'est pas un vecteur, c'est un **sous-espace appris**, et deux
opérations y tiennent ensemble. C'est la première brique d'un opérateur compositionnel ; la question suivante est la
**composition** : le nié du nié revient-il à l'original ?

## B4.4 — la composition n'est **pas algébrique** : le nié du nié ne revient pas

| | |
|---|---:|
| la sonde de l'original → le double nié (cible : l'original) | **0,5691** |
| le mélange → le double nié | 0,3601 |
| la sonde du nié → le double nié | 0,3344 |
| contrôle | 0,5080 |

**La composition échoue** : le nié du nié n'est pas lu comme l'original (0,5691 contre 0,8103 de référence), et le
mélange est **sous** le hasard (0,3601). *L'opérateur n'est pas une **algèbre** : deux négations ne s'annulent pas
dans l'état.* Les opérations sont des **sous-espaces appris** (B4.3), pas les générateurs d'un groupe.

**Ce que ça dit pour l'étage 2** : « penser sans verbaliser » ne consiste pas à appliquer des opérateurs algébriques
à l'état — **la composition doit être apprise** comme une tâche, pas déduite. C'est cohérent avec tout le reste : le
plan s'entraîne (mesure 119), la composition est alignée par un pont, mais rien ne se compose gratuitement.

**Ce que ça ne dit pas** : « Il est faux que » une fois ou deux est une négation de **surface** ; la négation
grammaticale et une négation **apprise** (LoRA) restent à tester. Et une seule couche (la 22).

## B4.5 — la composition **s'apprend**, mais faiblement

| | |
|---|---:|
| le triple (original, nié, double nié) → le double nié (cible : l'original) | **0,6174** |
| contrôle (étiquettes mélangées) | 0,4598 |

**La composition est apprenable, mais c'est la plus coûteuse des quatre tâches** : 0,6174 (soit **+0,117** sur le
hasard) contre 0,8103 pour l'original, 0,7042 pour le nié seul et 0,7749/0,6977 pour le mélange. *Rien ne se compose
gratuitement* : l'état porte la composition, mais il faut la lui **apprendre**, et elle coûte plus que les opérations
qu'elle combine.

## Le bilan de B4

| mesure | la question | la réponse |
|---|---|---|
| **B4.1** | l'opérateur est-il une **direction** ? | **non** — 0,4148 (sous le hasard), la garde 0,5852 |
| **B4.2** | est-il **apprenable** ? | **oui** — 0,7042 en réentraînant, mais **pas transférable** (0,3312) |
| **B4.3** | deux opérations tiennent-elles ensemble ? | **oui** — 0,7749/0,6977, un **sous-espace** (relation + polarité) |
| **B4.4** | la composition est-elle **algébrique** ? | **non** — le nié du nié ne revient pas (0,5691) |
| **B4.5** | est-elle **apprenable** ? | **oui, faiblement** — 0,6174 |

**La réponse de B4 à la question de l'étage 2** : les opérations sont des **géométries apprises**, locales, non
compositionnelles gratuitement — et la composition s'apprend à un **coût**. C'est la carte la plus précise que le
projet ait du « penser sans verbaliser » : *l'état porte les opérations, mais il ne les calcule pas.*

## B4, suite — le LoRA de la négation (la conception)

**La question** : B4.2 a montré que la négation est **apprenable par une sonde réentraînée** (0,7042) ; B4.5, que la
composition s'apprend **faiblement** (0,6174). La question suivante est celle du **poids** : peut-on apprendre
l'opération **dans le modèle** (un LoRA), pour que l'état la porte **sans sonde** ?

**Le dispositif** : le LoRA (`poser_lora` de `tools/adaptateur_langue.py`, rang 8) sur le 1,5 B ; l'entraînement sur
les paires **niées** (le même corpus que B4.2, les étiquettes basculées) ; puis **les cinq tests de B4** refaits sur
le modèle adapté — la sonde de l'original lit-elle le nié ? C'est le transfert que B4.1 avait refusé (0,4148).

**Le critère** : le flip **passe le hasard** sur le modèle adapté, avec le contrôle au hasard.

**Le coût** : ~1-2 h de GPU (le 1,5 B, le rang 8, les 723 paires) ; à lancer **après la passe** (elle occupe le GPU).

**Ce qui pourrait le rendre faux** : le LoRA peut **apprendre la surface** (« il est faux que ») sans apprendre
l'opération — c'est le risque de tous les adaptateurs. Le contrôle est de tester sur une **négation différente**
(« ce n'est pas le cas que »).

## B4.6 — le LoRA de la négation : l'entraînement **inverse** la lecture, il ne la transfère pas

| | |
|---|---:|
| `reference_orig` (le modèle adapté, sur l'original) | **0,8135** — le modèle est intact |
| `garde_sonde` (l'original) | **0,7717** |
| **`flip_sonde` (le nié)** | **0,2283** — sous le hasard, et **exactement** `1 − 0,7717` |
| la perte finale | 0,0022 |

**L'entraînement converge** (0,0022), **le modèle reste intact** (0,8135) — et **la sonde de l'original lit le nié à
0,2283**, l'**inverse** de ce qu'elle lit sur l'original (0,7717). *Le LoRA n'a pas appris le transfert : il a appris
à **inverser** la lecture.* Le `flip_sonde + garde_sonde = 1,0000` exactement le dit : le LoRA a appris la **surface**
(« il est faux que ») comme un **marqueur d'inversion**, pas l'opération.

**C'est le négatif de B4.6**, cohérent avec toute la ligne : la négation apprise dans les poids ne rend pas l'état
« négation-aware ». L'opération n'est pas un vecteur que l'entraînement transfère — c'est une **géométrie** que la
sonde doit réapprendre (B4.2).

**La réserve** : `flip_sonde = 1 − garde_sonde` peut être un **artefact de la sonde** (elle rend le complément), pas un
fait du LoRA. **Le contrôle qui tranche** : entraîner le LoRA sur les paires **originales** ; si le `flip_sonde` reste
à 0,41 (le B4.1), le LoRA a appris quelque chose de spécifique ; sinon, c'est la sonde.

**Le trajet de la mesure** (trois instruments réparés) : le flag `--lora` manquait ; `poser_lora` rend la liste des
conteneurs (pas le modèle) ; les paramètres du LoRA étaient en float32 contre un modèle float16 (la perte partait en
NaN). Le diagnostic `--sans-entrainement` a tranché : le **forward** était propre (0,8103), c'était l'**entraînement**
qui cassait le modèle.

## Ce que ça ne dit pas

- **« Il est faux que : H »** est une négation de **surface** : le modèle peut ne pas la parser comme une négation
  logique. La négation grammaticale (« ne…pas ») et une négation **apprise** (B4.2) sont les variantes à tester.
- **Une seule couche** (la 22) et **un seul modèle** (le 1,5 B) : la négation peut être portée plus tard ou plus tôt.
- Le test mesure la **lecture** de l'opérateur par la sonde, pas la capacité du modèle à **raisonner** la négation.
- Le « garde » au-dessus du hasard peut aussi être un **biais de la prémisse** : les paires niées gardent la prémisse,
  et la sonde peut lire la relation par la prémisse seule. C'est une explication à tester (la prémisse seule contre
  l'hypothèse seule).
