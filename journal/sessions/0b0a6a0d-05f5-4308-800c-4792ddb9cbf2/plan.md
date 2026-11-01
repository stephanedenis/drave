# Plan de session — N2.h, le mètre propre

> **Mandat ouvert** le 2026-10-31 22 h 30 HAE depuis [`docs/pilotage/en-cours.md`](../../../docs/pilotage/en-cours.md)
> — mandat libre de 10 h (nuit du 31/10 au 1/11). Le heartbeat est celui de l'état.

- **Session** : `0b0a6a0d-05f5-4308-800c-4792ddb9cbf2`
- **Rôle** : calcul : distillation ; corpus ; évaluation
- **Périmètre** : N2.h — corpus propre, porte honnête, généralité, verrou de longueur
- **Fichiers réservés** : `data/`, `tools/corpus*`, `tools/eval_n2_propre.py`,
  `tools/distiller_budget.py`, `reports/n2-*`, `work/n2h/`,
  `journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/`
- **Heartbeat** : 2026-10-31 22:40 HAE
- **Objectif final** : un **mètre honnête** pour N2 — corpus dédupliqué (0 % de fenêtres de
  validation dans l'entraînement), chaîne refaite dessus, porte < 2,5 redéfinie — puis trancher
  ce que les chiffres contaminés ne pouvaient pas trancher : la **généralité hors dépôt** et le
  **verrou de longueur**.
- **Plan** : 1) `tools/corpus_propre.py` (dédup shingles, split par chunks, vérification) ;
  2) chaîne propre (professeur 23,5 M, base 20 000 pas, distillation 20 000 pas × 3 graines,
  curriculum 129 × 3) ; 3) porte honnête + hors domaine (littérature, anglais, wikitext2) +
  décomposition (têtes précoces, pensée) ; 4) diversité française 50/50 dépôt-littérature, × 3 ;
  5) verrou de longueur : courbe 129→512 et **positions aléatoires** × 3 ; 6) fiches, portes, commit.
- **Stratégie** : un seul changement à la fois, trois graines, contrôle par permutation, le corpus
  d'abord — un levier mesuré sur un mètre faux ne vaut rien.
- **Ambition** : sortir N2 du chiffre qui flattait (2,85 sur un jeu contaminé à 32,8 %), donner à R
  un modèle qui lit du français général, trancher le verrou de longueur par une expérience.
- **Prochaine action** : distillation A (3 graines) puis évaluation de la porte honnête.
- **État** : en cours
