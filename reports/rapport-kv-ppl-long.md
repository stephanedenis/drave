# A7.13 — K/V int8 sur 512 jetons : ΔPPL exactement 0

> **Objet.** A7.12 ne testait que **85 jetons**. Ici on prend un texte long (UDHR concaténé,
> **511 jetons**) et on mesure la PPL avec les **mêmes hooks** int8 par canal sur les **24 couches**.

## Résultats

| mesure | valeur |
|---|---:|
| jetons | **511** |
| PPL base | **4,6979356** |
| PPL K/V int8 | **4,6979356** |
| Δ | **0,0** |
| couches | **24** |

## Lecture

- La **PPL est identique au bit** sur 511 jetons : la quantification int8 par canal des K/V ne
  change pas la prédiction mesurable.
- C'est cohérent avec A7.12 (Δ −1,2e-6 sur 85 jetons) : l'effet est **sous le bruit**.
- Le résultat est **surprenant** par son exactitude ; il faut le lire comme **absence de perte
  mesurable** sur ce texte, pas comme une preuve que la quantization est sans effet.
- Le **coût** des 896 échelles par couche n'est pas compté.

## Verdict

**A7.13 est positif** : à **511 jetons**, K/V int8 par canal laisse la **PPL inchangée** (Δ **0**).
Le cache quantifié tient sur un contexte plus long, sans génération.

## Limites

- **Un seul texte**, 511 jetons ; pas de génération ni de cache réel.
- Quantification **par canal**, pas par bloc.
- Les hooks modifient la sortie de `k_proj`/`v_proj` avant l'attention ; le cache n'est pas stocké.
- L'exactitude du Δ peut cacher un effet **sous la résolution** de la PPL.

## Fichiers

- Code : [`tools/kv_ppl_long.py`](../tools/kv_ppl_long.py).
- Test : [`tools/cerveau/tests/test_kv_ppl_long.py`](../tools/cerveau/tests/test_kv_ppl_long.py).
- JSON : [`kv-ppl-long.json`](kv-ppl-long.json).
