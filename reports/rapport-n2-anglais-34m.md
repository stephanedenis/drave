# N2.w — L'anglais à 34,3 M distillé : 3,77, et 4,18 à 512 octets

> **Ligne de roadmap** : N2 · **Date** : 2026-11-02 · **Verdict** : la chaîne anglaise complète
> (base 34,3 M à positions aléatoires + distillation du professeur 23,57 M, **2 graines**) vaut
> **3,7651** sur la validation (base 4,2396, −0,47), **4,394** sur le banc anglais (4,9327),
> **4,683** sur wikitext2 (5,281) et **4,185** à 512 octets (4,5265). L'anglais suit exactement la
> loi du français : capacité + distillation se composent.

## Le dispositif

- Corpus : anglais, 204,6 Mo (N2.m).
- Base : **34,3 M** (`384/512`), positions [0, 384] (N2.w base), val 4,2396.
- Professeur : 23,57 M (`route-en`, N2.m).
- Distillation : 20 000 pas × 16 × 128, KD T=2 α=0,7, positions [0, 384], **2 graines**.

## Ce qui est mesuré

| modèle | val anglais | banc anglais | wikitext2 | 512 |
|---|---:|---:|---:|---:|
| base 11,47 M | 4,4234 | 5,2967 | 5,5607 | 6,60 |
| base 34,3 M | 4,2396 | 4,9327 | 5,2810 | 4,53 |
| **34,3 M distillé** | **3,7651** | **4,3940** | **4,6830** | **4,185** |
| écart base → distillé | **−0,47** | −0,54 | −0,60 | −0,34 |

Courbe de longueur du distillé : **3,76 / 3,73 / 3,74 / 3,93 / 4,18** à 129/192/256/384/512.

## Lecture

**La chaîne anglaise reproduit la française, chiffre pour chiffre** : le 34,3 M distillé vaut 3,765
(le français : 3,685), avec la même courbe de longueur plate (4,18 à 512 contre 4,09). Les deux
langues ont donc la même **loi** : capacité → −0,2, distillation → −0,4, longueur → −0,3.

Le plafond de fenêtre est le même : à 512 octets, la PPL monte de 0,4 environ (la fenêtre locale de
256), pas de 2 comme à 11,47 M.

## Ce que ça change pour N2

- Les **deux meilleurs modèles de la nuit** sont : français **3,685** (N2.r) et anglais **3,765**
  (N2.w), tous deux à 34,3 M distillé, courbes plates.
- C'est la base de la ligne R : un lecteur bilingue à 34,3 M, avec la robustesse de longueur.
- La **distillation du canal** et la **loi d'échelle multilingue** restent les questions ouvertes.

## Ce qui pourrait le rendre faux

- **Deux graines** ; l'écart entre graines (0,001) est minuscule, mais l'intervalle n'est pas mesuré.
- **20 000 pas** (10 % du corpus) : la base et l'élève ne sont pas convergés.
- **Le texte est du wikitexte nettoyé**, même réserve que N2.j.

## Fichiers

- Base : `work/n2k/base-en-34m.pt` ; élèves : `work/n2k/E34-g{1,2}.pt` ; professeur :
  `work/n2k/route-en`.
- Mesures : `work/n2k/eval-en-34.json`, `eval-en34-distill.json`.
