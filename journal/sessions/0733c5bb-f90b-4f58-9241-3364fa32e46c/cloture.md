# Session `0733c5bb` — N2, le natif : 200 000 pas et la fenêtre

> **Id DSH** : `0733c5bb-f90b-4f58-9241-3364fa32e46c`.
> **Rôle** : N2 — le natif, GPU (programme N, puis R1.1/R1.2 vus depuis N2).
> **Mandat** : [`plan.md`](plan.md) · **Journaux** : [le 02/11](../../../journal/2026-11-02/README.md),
> [l'état](../../../docs/pilotage/en-cours.md), [l'index des sessions](../../README.md#sessions).

## Ce qui a été livré

- **200 000 pas sur le mélange 1 Go** (`data/wiki_mix/propre`, 1 017 487 092 octets), recette
  N2.ac à un paramètre près, GPU 0, **11 410 s** (3 h 10, 57 ms/pas). Cinq PPL mesurées avec le
  mètre de N2.ac repassé sur le témoin 60 k **à l'identique** : validation française **3,4902 →
  3,1591** (−0,33), grand corpus **3,3565 → 3,0035**, littérature **6,0283 → 5,6056**, anglais
  **8,3352 → 7,2770**, wikitext2 **9,0525 → 8,0018** ; transfert au corpus propre 9,27 → 9,13 ;
  précision top-1 **0,6416 → 0,6741**. Fiche
  [`n2-200k`](../../../reports/rapport-n2-200k.md), agrégat
  [`n2-200k.json`](../../../reports/n2-200k.json).
- **La réponse à la question ouverte de N2** : la porte **< 2,5 n'est pas atteinte** (3,1591 en
  domaine) ; la loi de puissance de la trajectoire — exposant **0,0987** sur 20 k–200 k,
  **0,0894** sur 40 k–200 k, et il **décroît** — place 2,5 à **1,3–2,7 millions de pas**, 21 à
  44 h de GPU. Le gain **s'inverse à 512 octets** (+0,14) : le compute ne remplace pas une
  fenêtre entraînée.
- **R1.1 — les positions relatives** : variante **RoPE** du modèle natif (aucune position apprise,
  `pos_debut` sans effet, autotest). À recette et budget égaux, la PPL à 1 000 octets passe de
  **8,2024** à **3,2545** ; la porte R1.1 (facteur 1,5) est tenue à **0,97×** contre 2,33×, et la
  PPL à 128 **s'améliore** de 0,14. Le mécanisme est contrôlé deux fois : à texte et prédécesseurs
  **identiques**, RoPE est invariant au décalage absolu (Δ 0,0017) quand la table absolue **×4,8**
  (3,8468 → 18,6055) ; et le contrôle causal — entraîner les positions 0–1279 — fait tomber
  l'explosion à **4,0956**.
- **La nuance qui change la lecture** : depuis une **initialisation aléatoire figée**, RoPE est
  meilleur à 128 (−0,29) mais **se dégrade dès 160 octets** et **ne se redresse pas** à 40 000 pas
  (3,3215 → 6,4259). La platitude de R1.1 vient de l'**histoire de l'initialisation** (un modèle
  absolu déjà entraîné, dont les décalages aléatoires ont fait voir les positions 0…511), pas du
  seul schéma.
- **R1.2 — la fenêtre entraînée** : à **octets constants** (5 000 pas × 8 × 512 = 20,5 Mo vus,
  exactement ceux de R1.1), la fenêtre 512 gagne à **toutes** les longueurs et le gain **croît
  avec la longueur** : 128 3,3399 (−0,03), 256 3,2271 (−0,10), 512 3,0990 (−0,19), 1 000
  **3,0107** (−0,24). Le contrôle « même texte » montre que le modèle **utilise** les octets
  au-delà de 256 (2,9654 → 2,8819) là où le modèle à fenêtre 256 ne le peut pas (+0,08). Fiche
  [`n2-r11`](../../../reports/rapport-n2-r11.md), agrégat
  [`n2-r11.json`](../../../reports/n2-r11.json).
- **Le miroir de sortie** : le banc de copie à distance est **muet** (justesse 0,0078 au mieux,
  autotest du banc 0,469) — les modèles de 34,3 M / 40 k pas **n'ont pas de circuit de copie**.
  La PPL n'est pas la lecture : c'est écrit dans la fiche.
- **Le code du banc** est archivé avec la session : `code/` (modèle RoPE, entraîneurs, bancs,
  agrégateurs, chaînes de runs).

## Ce qui reste (hors session)

- **R1.2 à 1 024 octets entraînés** — c'est le levier que ce cycle désigne ; les mêmes pas que
  R1.1 à 512 (20 000) coûteraient 4× les octets, non faits ici.
- **Le mécanisme de l'écart entre les deux bras RoPE** (adapté vs depuis zéro) n'est pas établi ;
  l'hypothèse à tester est un RoPE depuis zéro **entraîné sur 256 octets**.
- **La porte < 2,5** : elle demande un autre levier (capacité ou architecture), pas un 500 k pas.
- **N4** (0/4), **N5** gelé, **B10.3**.

## État et commits

- **Résultats** : **`2cff8dba`** (R1.1/R1.2) et **`e12c39c1`** (200 000 pas) ; mandat `dc7f9c56`.
- **État** : `en-cours` porte la ligne N2 (3,1591 / 5,6056 / 7,2770 / 8,0018), la ligne R1
  (0,97× la porte, fenêtre 512 −0,244) et les deux fiches ; compteurs au disque.
- **Réservations rendues** : `data/`, `tools/corpus*`, `reports/n2-*`, `reports/rapport-n2-*`,
  `work/n2ac/` — le GPU 0 et le GPU 1 sont **libres**.
- **Portes** : revue de documentation **verte** aux deux commits (560 fiches / 647 JSON) ; journal,
  en-cours et schémas verts ; la passe complète des 81 portes reste au hub (1 h 46).
