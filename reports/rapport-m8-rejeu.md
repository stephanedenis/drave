# B25 — le rejeu ne sauve pas M8

> **Objet.** A7 avait montré que M8 (prototypes) ne généralise pas : leave-one-code-out exact **0**.
> Ici on ajoute un **rejeu** des épisodes stockés et un **hybride** prototype + plus proche épisode,
> sur 6 codes tenus à l'écart.

## Résultats

| mesure | valeur |
|---|---:|
| codes train / test | **23 / 6** |
| épisodes train / test | 442 / 86 |
| prototypes | 6 |
| M8 exact | **0,00 %** |
| M8 champs | 74,57 % |
| **rejeu exact** | **0,00 %** |
| **hybride exact** | **0,00 %** |

## Lecture

- Le **rejeu** ne peut pas produire un code qu'il n'a jamais vu : les 6 codes de test sont absents
  des 442 épisodes ; le prototype ne sort qu'un code vu.
- L'**hybride** prototype + plus proche épisode échoue aussi : le plus proche épisode est un
  **autre code**, et le code exact n'est jamais reconstruit.
- Les **champs** restent à 74,6 % (marginales), mais l'**exact** est **0** : ce n'est pas de la
  généralisation.
- C'est le même négatif qu'A7, avec le rejeu en plus : **M8 ne compose pas un code neuf**.

## Verdict

**B25 est négatif** : le rejeu et l'hybride ne sauvent pas M8 sur un code tenu à l'écart. La
consolidation **résume** les codes vus ; elle ne les **recombine** pas.

## Limites

- 6 codes de test, 86 épisodes, une graine.
- Les prototypes sont par `(jeu, action)` ; un prototype plus fin ne peut pas inventer des
  coordonnées absentes.
- Le rejeu est **passif** (on réinjecte les épisodes) ; un rejeu **actif** avec génération n'est
  pas testé.

## Fichiers

- Code : [`tools/cerveau/sommeil_rejeu.py`](../tools/cerveau/sommeil_rejeu.py).
- Test : [`tools/cerveau/tests/test_sommeil_rejeu.py`](../tools/cerveau/tests/test_sommeil_rejeu.py).
- JSON : [`m8-rejeu.json`](m8-rejeu.json).
