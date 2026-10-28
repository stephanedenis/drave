# A7.11 — le KV int8 change 2,3 % des argmax d'attention

> **Objet.** A7.10 mesurait la reconstruction du cache KV int8. Ici on va jusqu'à la **sortie
> d'attention** : Q aléatoire, K/V du cache, softmax, sortie f32 contre KV int8. Ce n'est pas un
> modèle : c'est la **sensibilité de l'attention** à la quantification.

## Résultats (64 jetons, 2 têtes, d=64)

| mesure | valeur |
|---|---:|
| diff max | **0,0154** |
| diff moyenne | **0,0048** |
| **accord d'argmax** | **97,66 %** |
| corrélation | **0,99998** |
| octets f32 | 65 548 |
| octets int8 | **17 420** |
| ratio | **0,266** |

## Lecture

- La **sortie d'attention** est presque inchangée : corrélation **0,99998**, diff max **0,015**.
- **2,3 %** des positions changent d'argmax : ce n'est pas nul, mais c'est **petit**.
- Le cache int8 coûte **26,6 %** du f32 : le compromis volume/fidélité est **favorable** sur cette
  mesure.
- Ce n'est **pas** une preuve de fidélité du modèle : Q est aléatoire, il n'y a ni couche ni
  softmax quantifié.

## Verdict

**A7.11 est positif pour l'attention isolée** : le KV int8 conserve **97,7 %** des argmax et une
corrélation **0,99998**, à **26,6 %** du volume. Il reste à mesurer les **logits/PPL** avec un vrai
décodage.

## Limites

- **Q aléatoire**, pas un vrai modèle ; une seule couche.
- Pas de **softmax quantifié**, pas de cache multi-couches.
- **64 jetons**, une graine.
- L'accord d'argmax est une mesure **grossière** ; la PPL reste la juge.

## Fichiers

- Code : [`tools/kv_attention.py`](../tools/kv_attention.py).
- Test : [`tools/cerveau/tests/test_kv_attention.py`](../tools/cerveau/tests/test_kv_attention.py).
- JSON : [`kv-attention.json`](kv-attention.json).
