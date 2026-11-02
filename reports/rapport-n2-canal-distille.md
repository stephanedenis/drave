# N2.x — La distillation du canal : −0,03 en domaine, +0,24 à 512 octets

> **Ligne de roadmap** : N2 · **Date** : 2026-11-02 · **Verdict** : le canal de structure survit à
> la distillation — **3,8509** en domaine contre 3,8761 sans canal (−0,03, dans le bruit) — mais il
> **coûte en longueur** : **6,00** à 512 octets contre 5,76, et 3,95 contre 3,98 à 256. Le canal
> n'est **pas** un levier de distillation ; il reste un prior de prédiction locale.

## La question

N2.l avait montré que le canal donne −0,22 sur la **base** (4,17 contre 4,39). N2.j4 a montré que
la distillation donne −0,51. La question : les deux **s'ajoutent-ils**, ou la distillation
absorbe-t-elle le canal ?

## Le dispositif

- Base : `base-canal.pt` (11,47 M, canal, positions [0, 384]), val 4,1738.
- Professeur : 23,57 M (`route-wiki`, N2.j).
- Distillation : 20 000 pas × 16 × 128, KD T=2 α=0,7, positions [0, 384], **canal fourni à
  l'entraînement et à l'évaluation**, **2 graines**.
- Référence : la distillation **sans** canal (W-g, N2.j4), 3,8761.

## Ce qui est mesuré

| modèle | 128 | 256 | 512 | mélange « milieu » | mélange « tout » |
|---|---:|---:|---:|---:|---:|
| **sans canal** (W-g) | 3,8761 | 3,98 | 5,76 | ×6,8 | ×11,7 |
| **canal** (C-g1/g2) | **3,8509** | 3,96 | 6,00 | ×6,8 | ×12,2 |
| écart | −0,03 | −0,02 | **+0,24** | = | +0,5 |

## Lecture

**Le canal ne s'ajoute pas à la distillation** : −0,03 en domaine, c'est un tiers de l'écart entre
graines. La distillation **absorbe** le canal — elle apprend au modèle ce que le canal lui donnait,
et le canal devient redondant.

**Il coûte même en longueur** : à 512 octets, le modèle à canal vaut 6,00 contre 5,76. Le canal est
un prior **local** (mot, ponctuation) : il aide à prédire l'octet suivant dans les 128 octets, mais
il ne dit rien de la structure au-delà de la fenêtre, et le modèle s'y appuie au détriment du
contexte long.

**Le mélange reste identique** (×6,8) : le canal ne change pas la nature du lecteur — il reste
lettre-dépendant.

## Ce que ça change pour N2

- Le canal **n'entre pas dans la recette de production** : la distillation seule donne le même
  résultat en domaine, sans le coût de longueur.
- Il reste utile comme **sonde** (N2.l) : il montre ce que le modèle ne déduit pas localement.
- La structure, si elle doit aider la longueur, doit venir d'un **schéma de position** (R1.1), pas
  d'un canal local.

## Ce qui pourrait le rendre faux

- **Deux graines** ; l'écart de −0,03 est très petit.
- **Le canal utilisé ici est heuristique** (6 classes) ; un canal plus riche (rôles, dépendances)
  dirait autre chose.
- **20 000 pas** : le modèle à canal pourrait converger différemment.
- **Le texte est du wikitexte nettoyé**, même réserve que N2.j.

## Fichiers

- Élèves : `work/n2j/C-g{1,2}.pt` ; base : `work/n2j/base-canal.pt` ; professeur :
  `work/n2j/route-wiki`.
- Mesures : `work/n2j/eval-canal*.json`.
