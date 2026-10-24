# La carte du raisonnement naturel : quatre mesures, trois courbes, deux axes

> Synthèse du 24/10/2026, sur les données de `xnli_latent.py` (1,5 B / 3 B / 14 B / 32 B) et `nli_fr_dur.py`
> (DACCORD). **Chaque chiffre a sa fiche et son JSON** ; ce document ne mesure rien de neuf, il **relie** — et il
> écrit ses limites.

## Les quatre mesures

1. **La sonde** (ridge / MLP) : l'accès **linéaire** à l'état.
2. **Le pont** (EN→FR) : le **transfert** de l'état entre langues.
3. **Le pic** : la couche où chaque modèle lit le mieux.
4. **Le balayage** : l'écart entre son pire et son meilleur point.

## Les trois courbes

| modèle | couches mesurées | sonde (pic) | pont (pic) | balayage |
|---|---|---|---:|---:|---:|
| 1,5 B | 14, 18, 22, 26 | **0,810** (l22, DACCORD) | **0,83** (l18, XNLI) | +0,232 |
| 3 B | 12, 18, 24, 30 | **0,865** (l30, DACCORD) | **0,8568** (l30, XNLI) | +0,354 |
| 14 B | 18, 24, 30, 36 | **0,7376** (l36, XNLI) | **0,8715** (l36) | +0,147 |
| 32 B | 18, 32 | 0,5997 (l32) | 0,7724 (l32) | +0,19 |

## Les deux axes

- **La sonde sature dès le 1,5 B** : sur XNLI, 0,7256 / 0,7269 / 0,7189 / 0,7376 à leurs pics — **dix fois la taille
  pour +0,001**.
- **Le pont monte encore puis sature** : 0,826 → 0,857 → 0,870 → 0,872 — **+0,046 en tout, plafond à 0,87**.

## Les quatre leçons

1. **Le point de mesure décide de la conclusion** — quatre « décroissances » du jour étaient des mauvais points
   (la couche 18, la profondeur 50 %, le l24 « non mesuré », le « pas de gain » du 14 B).
2. **La profondeur décide autant que le modèle** : +0,147 à +0,354 de balayage entre le pire et le meilleur point.
3. **La taille ne garantit rien** : à 50 %, le **14 B est dernier** (0,4833) et le 32 B premier (0,5997).
4. **La structure bat la taille** : la sonde sature au 1,5 B, le pont à 0,87 — dix fois plus de paramètres
   n'achètent presque rien sur la lecture.

## Ce que cette fiche ne dit pas

- **Les pics ne sont pas cherchés exhaustivement** : on a mesuré les couches rondes (12, 18, 24, 30, 36) — le vrai pic
  peut être entre deux.
- **Le 32 B n'a que deux points** (18 et 32) : sa courbe est une droite, pas un pic ; son pic n'est pas mesuré
  (10-20 h en 4 bits, documenté et non forcé).
- **XNLI et DACCORD ne se comparent pas** (3 classes, hasard 0,33 contre 2 classes, hasard 0,50) : chaque comparaison
  de cette fiche est **à dataset égal**.
- **Le pont du 3 B sur DACCORD n'existe pas** (le jeu est français seulement) : son pont est mesuré sur XNLI.
