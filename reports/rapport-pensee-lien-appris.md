# B13 — le lien appris : perceptron de rang, LOO 9/9, le hasard 0,1 et la surface seule 2/9

> **Ligne de roadmap** : **L/B13** · **Date** : 2026-11-03 · **Verdict** : ✅ **le lien s'apprend** —
> un perceptron de rang entraîné en **leave-one-out** sur les **9 paires** (5 arrière r418–r422 →
> r423–r427, 4 avant r408–r411 → r423–r426 ; la croisée r412→r427 écartée) retrouve **9/9**, comme
> les règles à la main. Le **hasard** fait **0,10** et la **surface seule** (sujet + proximité)
> **2/9** : les traits appris ne sont pas un artefact.

## 1. Le dispositif

- **Traits** (6) : même sujet normalisé, même verbe, même adverbe (hors négation), acte
  question→assertion, phrase simple (pas de SUB, pas de `;`), proximité `1/(1+rang)`.
- **Modèle** : perceptron de rang — pour chaque question, si le meilleur négatif dépasse le
  positif, on pousse `w += f(pos) − f(meilleur_neg)` ; 20 époques, graine 1.
- **Évaluation** : **LOO** — on retire une paire, on apprend sur les 8 autres, on teste sur la
  retirée. Aucune paire ne sert à son propre test.

## 2. Les résultats

| lecture | justes | taux |
|---|---:|---:|
| **lien appris (LOO)** | **9/9** | **1,00** |
| règles à la main (rappel) | 9/9 | 1,00 |
| hasard (poids aléatoires, 50 graines) | — | **0,10** |
| surface seule (sujet + proximité) | **2/9** | 0,22 |

## 3. Le contrôle négatif

- **Hasard** : 0,10 de justesse moyenne — le problème n'est pas trivial.
- **Surface seule** : 2/9 — le sujet et la proximité ne suffisent pas ; ce sont bien le verbe,
  l'adverbe, l'acte et la phrase simple qui portent.
- **LOO** : la paire testée n'est jamais vue à l'entraînement — le 9/9 n'est pas du par-cœur.

## 4. Ce qui pourrait rendre ce résultat faux

- 9 paires seulement : la LOO est fragile, un seul renversement ferait 8/9.
- Les **traits** sont choisis à la main ; seul le **poids** est appris. Ce n'est pas un modèle de
  langue, c'est la validation que les règles sont **apprenables**.
- La paire croisée r412→r427 est écartée (défaut du gold, documenté).

## 5. La suite

1. Étendre les paires (20, 50) pour stabiliser la LOO.
2. Apprendre aussi les **traits** (représentations) — le vrai « apprentissage » du lien.
3. Le lien est prêt : 9/9 règles, 9/9 appris.

## 6. Fichiers

- [`pensee-lien-appris.json`](pensee-lien-appris.json) — les mesures et les poids par pli.
- [`tools/tests/linguistique/qualifier_lien_appris.py`](../tools/tests/linguistique/qualifier_lien_appris.py) —
  le banc.
