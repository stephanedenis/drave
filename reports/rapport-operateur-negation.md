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

## Ce que ça ne dit pas

- **« Il est faux que : H »** est une négation de **surface** : le modèle peut ne pas la parser comme une négation
  logique. La négation grammaticale (« ne…pas ») et une négation **apprise** (B4.2) sont les variantes à tester.
- **Une seule couche** (la 22) et **un seul modèle** (le 1,5 B) : la négation peut être portée plus tard ou plus tôt.
- Le test mesure la **lecture** de l'opérateur par la sonde, pas la capacité du modèle à **raisonner** la négation.
- Le « garde » au-dessus du hasard peut aussi être un **biais de la prémisse** : les paires niées gardent la prémisse,
  et la sonde peut lire la relation par la prémisse seule. C'est une explication à tester (la prémisse seule contre
  l'hypothèse seule).
