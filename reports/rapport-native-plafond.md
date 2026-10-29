# N2 — synthèse : le plafond de 2,708

> **Objet.** Rassembler les six derniers essais de distillation et nommer le plafond.

## Les essais

| essai | changement | PPL | verdict |
|---|---|---:|---|
| N2.19 | lr 5e-6, 30k | **2,708** | **meilleur** |
| N2.21 | professeur 30k, lr 3e-6 | 2,823 | dégradation |
| N2.22 | professeur 30k, lr 1e-5 | 2,828 | dégradation |
| N2.23 | professeur 20k, lr 3e-6 | 2,753 | dégradation |
| N2.24 | professeur 20k, T=4 | 2,852 | dégradation |
| N2.25 | professeur 20k, lr 1e-6 | 2,758 | dégradation |

## Lecture

- **Aucun** des six essais ne bat **2,708**.
- Le **professeur 30k** (1,734) est **trop tranchant** ; T=4 ne suffit pas.
- Les lr **3e-6, 1e-5, 1e-6** dégradent tous après 12 000–14 000 pas.
- Le student **11,47 M** a atteint son **plafond de recette** : la distillation seule ne le mène pas
  à **2,5**.

## Verdict

**N2 — plafond confirmé** à **2,708**. La porte **< 2,5** n'est **pas atteinte** ; il faut changer
d'architecture, ajouter des **pertes locales par bloc**, ou augmenter la capacité **avec un budget
réel**.

## Limites

- **Corpus français**, professeur byte-level.
- **Un seul student**.
- **Pas de pertes locales**.
- **Pas de test externe**.

## Fichiers

- Fiches : `rapport-native-prof20k-5.md`, `…-6.md`, `…-7.md`, `…-8.md`, `rapport-native-prof30k*.md`.
- JSON : `native-prof20k-5.json`, `native-prof20k-6.json`, `native-prof20k-7.json`, `native-prof20k-8.json`.
