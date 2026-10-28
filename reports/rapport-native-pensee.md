# N1.5 — la pensée contractante de `drave-n0` : λ = 0,709

> **Objet.** La cellule de pensée du premier `drave-n0` était un **résidu** `x + tanh(Wx)` : son
> Jacobien valait **λ = 1,42**, donc elle **amplifiait** au lieu de contracter. On la remplace par
> un pas **contractant** `tanh(Wx + U h0)`, on réentraîne, et on mesure λ et le contenu.

## Dispositif

- **Modèle** : 11 418 792 paramètres, 6 blocs, octets, 3 têtes précoces, **2 pas de pensée**.
- **Corpus** : `data/corpus_fr.txt`, 4,63 Mo ; validation = derniers 5 %.
- **10 000 pas**, lot 8, séquence 128, lr 3e-4, graine 1 ; **425 s** GPU.
- **λ** : itération de puissance sur le Jacobien du pas de pensée, **30 itérations**, `d=224`.
- **Contenu** : PPL de validation **sans** pensée (`thought_steps=0`) contre **avec** (2 pas).

## Résultats

| mesure | valeur |
|---|---:|
| **λ du pas de pensée** | **0,7086** |
| PPL avec pensée | **3,580** |
| PPL sans pensée | **721 725,8** |
| PPL avec pensée (8 lots) | **3,530** |
| précision principale | **61,79 %** |
| têtes précoces | **55,64 / 60,72 / 61,72 %** |
| paramètres | **11 418 792** |

## Lecture

- La cellule **contracte** : **λ = 0,709 < 1**. Le résidu précédent était à **1,42**.
- Le **contenu** est bien porté par la pensée : sans elle, la PPL explose à **721 726** ; avec elle,
  **3,53**. Ce n'est pas un module décoratif.
- Le prix est une **PPL de 3,58** contre **3,36** pour le modèle à résidu : **+6,5 %**. La
  contraction coûte de la qualité, mais elle rend la pensée **stable**.
- Les têtes précoces restent à **55,6 / 60,7 / 61,7 %** : la contraction ne les casse pas.

## Verdict

**N1.5 est atteint** : la pensée est **contractante** (λ < 1) et **porte le contenu** (sans elle, la
PPL est catastrophique). Le coût est une PPL légèrement plus haute, à documenter.

## Limites

- **Même corpus** pour l'entraînement et la validation ; pas de test externe.
- **λ** est une estimation par itération de puissance sur un point ; ce n'est pas une borne globale.
- **2 pas** seulement ; 4 ou 8 pourraient changer le compromis.
- La **PPL sans pensée** est si haute qu'elle prouve la dépendance, pas la qualité de la
  représentation.

## Fichiers

- Code : [`tools/native_model.py`](../tools/native_model.py),
  [`tools/entrainer_native.py`](../tools/entrainer_native.py).
- JSON : [`native-pensee.json`](native-pensee.json).
