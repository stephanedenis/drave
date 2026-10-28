# A7.14 — génération greedy identique avec K/V int8

> **Objet.** A7.13 mesurait la PPL. Ici on **génère** 16 jetons en greedy avec les mêmes hooks
> int8 par canal sur `k_proj`/`v_proj` des 24 couches, et on compare au modèle intact.

## Résultats

| mesure | valeur |
|---|---:|
| prompt | « La mesure est reine parce que » |
| jetons générés | **16** |
| jetons identiques | **16 / 16** |
| accord | **1,00** |
| texte base | « c'est la seule façon de faire des choses. - 1000 » |
| texte int8 | **identique** |

## Lecture

- La génération greedy est **exactement identique** sur 16 jetons : K/V int8 par canal ne change
  pas la décision.
- C'est cohérent avec A7.13 (ΔPPL 0,0 sur 511 jetons) et A7.11 (argmax 97,7 %).
- Le résultat est **court** : 16 jetons, un prompt ; il ne prouve pas la stabilité sur une longue
  génération.

## Verdict

**A7.14 est positif** : K/V int8 par canal laisse la **génération greedy identique** sur 16 jetons.
Le cache quantifié est un candidat sérieux pour le transport et la mémoire.

## Limites

- **16 jetons**, un prompt, greedy seulement ; pas d'échantillonnage.
- Les hooks modifient `k_proj`/`v_proj` avant l'attention ; le cache réel n'est pas stocké.
- Le coût des échelles n'est pas compté.
- Un seul modèle (0,5 B).

## Fichiers

- Code : [`tools/kv_gen.py`](../tools/kv_gen.py).
- Test : [`tools/cerveau/tests/test_kv_gen.py`](../tools/cerveau/tests/test_kv_gen.py).
- JSON : [`kv-gen.json`](kv-gen.json).
