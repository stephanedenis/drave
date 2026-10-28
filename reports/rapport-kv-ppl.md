# A7.12 — K/V int8 dans un vrai modèle : ΔPPL −1,2e-6

> **Objet.** A7.10 et A7.11 mesuraient la reconstruction et l'attention isolée. Ici on branche des
> hooks sur **`k_proj`** et **`v_proj`** des **24 couches** de Qwen2.5-0.5B : la sortie est quantifiée
> **int8 par canal**, déquantifiée, puis l'attention continue. On compare la **PPL** au modèle intact.

## Résultats (5 textes, 85 jetons)

| mesure | valeur |
|---|---:|
| PPL base | **2,6792016** |
| PPL K/V int8 | **2,6792004** |
| Δ | **−1,17e-6** |
| ratio | **0,9999996** |
| couches | **24** |

## Lecture

- La **PPL ne bouge pas** : l'écart est de **−1,2e-6**, soit du bruit numérique.
- La quantification **par canal** des K/V, appliquée à **toutes** les couches, ne dégrade pas la
  prédiction sur cet échantillon.
- C'est cohérent avec A7.11 (argmax 97,7 %, corrélation 0,99998) : le KV int8 est **stable**.
- **Mais** 85 jetons et 5 textes courts : ce n'est pas une preuve de qualité en génération.

## Verdict

**A7.12 est positif** : K/V int8 par canal laisse la **PPL inchangée** (Δ **−1,2e-6**) sur 24 couches.
Le cache quantifié devient un candidat sérieux pour le transport, sous réserve d'un test plus long.

## Limites

- **85 jetons**, 5 textes ; pas de génération, pas de long contexte.
- La quantification est **par canal**, pas par bloc ; le coût des échelles n'est pas compté.
- Les hooks modifient **k_proj/v_proj** en place avant l'attention ; le cache réel n'est pas testé.
- Une seule graine implicite.

## Fichiers

- Code : [`tools/kv_ppl.py`](../tools/kv_ppl.py).
- Test : [`tools/cerveau/tests/test_kv_ppl.py`](../tools/cerveau/tests/test_kv_ppl.py).
- JSON : [`kv-ppl.json`](kv-ppl.json).
