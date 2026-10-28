# A7.15 — 64 jetons greedy identiques avec K/V int8

> **Objet.** A7.14 s'arrêtait à 16 jetons. Ici on génère **64 jetons** en greedy avec les mêmes
> hooks int8 par canal sur `k_proj`/`v_proj` des 24 couches.

## Résultats

| mesure | valeur |
|---|---:|
| jetons générés | **64** |
| jetons identiques | **64 / 64** |
| accord | **1,00** |
| texte | identique |

Extrait : « c'est la seule façon de faire des choses. - 1000 mots… »

## Lecture

- La génération reste **exactement identique** sur **64 jetons** : K/V int8 ne change aucune
  décision.
- C'est cohérent avec A7.13 (ΔPPL 0,0 sur 511 jetons) et A7.14 (16/16).
- La longueur **64** est encore courte pour une génération réelle, mais elle dépasse le simple
  préfill.

## Verdict

**A7.15 est positif** : K/V int8 par canal conserve **64/64** jetons greedy. Le cache quantifié est
stable sur une génération courte.

## Limites

- **64 jetons**, un prompt, greedy ; pas d'échantillonnage.
- Le cache n'est pas **stocké** ; les hooks modifient les projections avant l'attention.
- Le coût des échelles n'est pas compté.
- Un seul modèle (0,5 B).

## Fichiers

- Code : [`tools/kv_gen.py`](../tools/kv_gen.py).
- Fiche : [`rapport-kv-gen.md`](rapport-kv-gen.md).
- JSON : [`kv-gen-64.json`](kv-gen-64.json).
