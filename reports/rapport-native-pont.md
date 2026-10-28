# N1.6 — le pont de région de `drave-n0` : il paie

> **Objet.** Le pont entre les deux moitiés du graphe (après le bloc 3) est une projection apprise.
> On mesure son **coût** (PPL avec pont contre sans pont) et son **effet** (pont neutralisé).

## Dispositif

- `drave-n0` : **11 469 192** paramètres, 6 blocs, **pont** après le bloc 3, pensée contractante
  (λ = 0,709), 3 têtes précoces.
- **Corpus** : `data/corpus_fr.txt`, 4,63 Mo ; validation = derniers 5 %.
- **10 000 pas**, lot 8, séquence 128, lr 3e-4 ; **438 s** GPU.

## Résultats

| mesure | valeur |
|---|---:|
| **PPL avec pont** | **3,465** (JSON) / **3,703** (8 lots) |
| **PPL pont neutralisé** | **4,080** |
| effet du pont | **−9,3 %** de PPL |
| PPL du modèle **sans pont entraîné** | 3,580 |
| coût vs modèle sans pont | **−3,2 %** (le pont n'ajoute pas de PPL) |
| précision principale | **62,70 %** |
| têtes précoces | **57,57 / 61,60 / 62,06 %** |
| paramètres | **11 469 192** |

## Lecture

- **Neutraliser le pont** fait passer la PPL de **3,70** à **4,08** : le pont **porte du contenu**.
- Le modèle **avec pont** est à **3,465**, **sous** le modèle sans pont (**3,580**), alors qu'il a une
  couche de plus : le pont n'est pas un coût, c'est un gain.
- Les têtes précoces **ne sont pas cassées** : 57,6 / 61,6 / 62,1 %.
- Le **critère N1.6** (coût ≤ 5 % de PPL) est donc **largement tenu** : le coût est négatif.

## Verdict

**N1.6 est atteint** : le pont de région **réduit** la PPL de **3,2 %** par rapport au modèle sans
pont et **porte 9,3 %** de PPL quand on le neutralise. Il n'y a pas de compromis à payer.

## Limites

- **Même corpus** pour l'entraînement et la validation ; pas de test externe.
- **Initialisations différentes** entre le modèle avec et sans pont : la comparaison directe est
  indicative, l'ablation dans le même modèle est la preuve.
- **Un seul point de pont** (après le bloc 3) ; un pont plus tôt ou plus tard pourrait changer.
- **8 lots** pour la mesure d'ablation : la variance n'est pas estimée.

## Fichiers

- Code : [`tools/native_model.py`](../tools/native_model.py),
  [`tools/entrainer_native.py`](../tools/entrainer_native.py).
- JSON : [`native-pont.json`](native-pont.json).
