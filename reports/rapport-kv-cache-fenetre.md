# A7.22 — fenêtre f32 glissante : pire que le cache mixte

> **Objet.** A7.21 montrait qu'un cache mixte (f32 sur les **64 premiers** jetons, int8 ensuite) tient
> **237 jetons** sur 256. On teste l'inverse : garder les **64 derniers** jetons en f32 et quantifier
> tout le reste.

## Résultats (256 jetons)

| variante | premier divergent | accord |
|---|---:|---:|
| mixte f32→64 puis int8 (A7.21) | **237** | **92,58 %** |
| **fenêtre f32 sur les 64 derniers** | **77** | **32,42 %** |

## Lecture

- La fenêtre glissante est **beaucoup pire** : la divergence revient au **77ᵉ** et l'accord tombe à
  **32,4 %**.
- Ce sont les **premiers** jetons qui portent la trajectoire : les garder en f32 stabilise la
  génération ; garder les **derniers** ne compense pas l'erreur accumulée sur les premiers.
- Le **cache mixte d'A7.21** reste la meilleure variante.

## Verdict

**A7.22 est négatif** : une fenêtre f32 sur les derniers jetons **aggrave** la divergence. Il faut
protéger le **début** du cache, pas la fin.

## Limites

- **256 jetons**, un prompt, greedy ; une graine.
- Fenêtre **64** seulement.
- Re-quantification à chaque pas ; coût CPU non compté.
- Un seul modèle (0,5 B).

## Fichiers

- Code : [`tools/kv_cache_int8.py`](../tools/kv_cache_int8.py) (`CacheFenetre`).
- Fiche : [`rapport-kv-cache-mixte-256.md`](rapport-kv-cache-mixte-256.md).
- JSON : [`kv-cache-fenetre.json`](kv-cache-fenetre.json).
