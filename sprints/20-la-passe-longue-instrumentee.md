# Sprint 20 — La passe longue, INSTRUMENTÉE : le profil par profondeur et les logits

- **Début** : 01:17 · **Fin prévue** : 03:17 (boxing de 120 min)
- **Objectif** : le bloc 19 a montré que la passe de 1 024 jetons **tourne** ; il
  n'a pas montré qu'elle est **juste**. Relancer la même passe (~60 min) avec
  `--ppl-profil` (perplexité par tranche de 256 positions) et `--logits-bin` : la
  courbe par profondeur distingue « médiocre partout » de « catastrophique au-delà
  de 1 024 », et les logits permettent de comparer sans relancer.
- **Engagement de fin** : dépôt vert (tests + portes), machine rendue, tout commité.

## Revue — ce qui est livré, mesuré

_(mesure en cours)_

## Rétrospective — garder / changer / doute

_(à écrire)_

## Planning du bloc 21

_(à écrire)_
