# B16 — M7-bis : la fréquence, pas la neuromodulation

> **Objet.** Après le négatif A2, construire `MemoireFrequence` (LFU, LFU+récence) et comparer
> aux politiques FIFO/LRU sur 30 permutations appariées. Résultat : **LFU gagne**, mais c'est la
> **fréquence** qui porte le gain, pas un signal neuromodulateur ; **LFU+récence n'ajoute rien**.

## Résultats (30 permutations, capacité 16)

| politique | répétés surface | suffixe surface | suffixe code | nouveaux utiles |
|---|---:|---:|---:|---:|
| FIFO | 0,287 | 0,050 | 0,717 | 0,101 |
| LRU | 0,337 | 0,059 | 0,719 | 0,107 |
| **LFU** | **0,519** | **0,093** | **0,747** | **0,188** |
| LFU+récence | 0,519 | 0,093 | 0,747 | 0,188 |
| contexte jeu | 0,091 | 0,008 | 0,706 | 0,040 |
| contexte jeu + LFU | 0,229 | 0,039 | 0,463 | 0,039 |

**Deltas vs FIFO** : LFU **+23,1 pts** de répétés (30/30), **+4,25 pts** de suffixe surface
(27/30), **+8,73 pts** de nouveaux utiles (29/30), **+7,61 pts** de suffixe code (26/30,
p=4,2e-7). **LFU+récence = LFU** (0 gain sur les trois métriques) ; le contexte **dégrade**
(−8,5 pts de suffixe surface, −42,9 pts de répétés).

## Contrôle synthétique (Zipf, capacité 8, 15 permutations)

LFU code **68,2 %** de suffixe code contre FIFO 54,7 % ; le contrôle positif voit donc la
fréquence quand elle est là. **Le signal contexte**, lui, ne bat pas LFU même quand il est réel :
la fréquence est le prédicteur optimal sur un flux permuté.

## Verdict

- **LFU est une meilleure politique** que FIFO/LRU pour une mémoire bornée sur ce flux.
- **Ce n'est pas de la neuromodulation** : le gain vient de la **fréquence**, pas de la nouveauté,
  de l'incertitude ou de la récompense (A2 : −19,6 / −38,7 / −53,3 pts).
- **LFU+récence n'ajoute rien** ; **le contexte jeu dégrade**.
- La métrique historique 3,64 % reste le plafond 16/439 : elle ne départage pas les politiques.

## Limites

- Les permutations rendent le suffixe échangeable avec le préfixe : la fréquence y est optimale
  **par construction** ; le contexte ne peut pas la battre.
- `rep_surface` est en partie tautologique (LFU est défini pour garder les répétés).
- 30 permutations, un seul corpus ; pas de test de signification au-delà du signe.

## Fichiers

- Code : [`tools/cerveau/neuromodulation.py`](../tools/cerveau/neuromodulation.py).
- JSON : [`m7-frequence.json`](m7-frequence.json).
