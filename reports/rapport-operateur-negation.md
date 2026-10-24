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

## Ce que ça ne dit pas

- **« Il est faux que : H »** est une négation de **surface** : le modèle peut ne pas la parser comme une négation
  logique. La négation grammaticale (« ne…pas ») et une négation **apprise** (B4.2) sont les variantes à tester.
- **Une seule couche** (la 22) et **un seul modèle** (le 1,5 B) : la négation peut être portée plus tard ou plus tôt.
- Le test mesure la **lecture** de l'opérateur par la sonde, pas la capacité du modèle à **raisonner** la négation.
- Le « garde » au-dessus du hasard peut aussi être un **biais de la prémisse** : les paires niées gardent la prémisse,
  et la sonde peut lire la relation par la prémisse seule. C'est une explication à tester (la prémisse seule contre
  l'hypothèse seule).
