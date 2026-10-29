# A8.3b — les trois régimes de KV : le mélange tardif est meilleur que le f32, l'int8 partout est pire

> **Ligne de roadmap** : A8.3 (suite d'A8.3 et d'A8.0) · **Date** : 2026-10-29 · **Verdict** :
> ✅ **la non-monotonie est réelle et reproductible** — trois régimes, trois chiffres :
> f32 (**61,9920 / 60,8135 / 113,0068**), mélange tardif 1 % (**58,3200 / 62,7357 / 111,8003**),
> int8 partout (**66,6195 / 72,6501 / 120,0813**). Le mélange améliore **deux mesures sur
> trois** ; l'int8 partout dégrade **partout**. Ce n'est pas un artefact de la règle : le
> chemin explicite (`DRAVE_KV_BITS=8`) redonne exactement les chiffres du budget 10 %.
>
> **Dispositif** : Qwen2.5-0.5B-Q8_0, portes `porte-flux` et `porte-pont`, GPU ; trois régimes
> par variable d'environnement (`DRAVE_KV_BITS`, `DRAVE_PERTE_MAX`) ; JSON
> [`a83b-regimes.json`](a83b-regimes.json) ; suite d'[A8.3](rapport-a83-defaut.md).

## La question

A8.3 a montré que le défaut place+perte déplace les portes de −5,9 % à +19,5 %. Le signe
positif (un mode *s'améliore*) est suspect : une quantification ne devrait que dégrader.
D'où vient-il — de la règle, du nombre de couches, ou du chemin de calcul ?

## Ce qui est mesuré

| régime | flux mode 0 | flux mode 3 | pont (dense) |
|---|---:|---:|---:|
| **f32** (aucun KV int8) | **61,9920** | **60,8135** | **113,0068** |
| **mélange 1 %** (dernières couches int8) | **58,3200** (−5,9 %) | **62,7357** (+3,2 %) | **111,8003** (−1,1 %) |
| **int8 partout** (`DRAVE_KV_BITS=8`) | **66,6195** (+7,5 %) | **72,6501** (+19,5 %) | **120,0813** (+6,3 %) |

**Trois faits, et un seul est surprenant** :
1. l'int8 **partout** dégrade **partout** (+6,3 % à +19,5 %) — c'est le comportement attendu
   d'une quantification ;
2. le mélange **tardif** est un **troisième** point, reproductible : ce n'est ni le f32 ni
   l'int8 partout ;
3. sur **deux mesures sur trois** (flux mode 0, pont), le mélange fait **mieux** que le f32 —
   et sur le mode 3 (lot), il fait **moins bien**. Le mode de lot est donc dans l'effet.

## Le contrôle qui compte

**`DRAVE_KV_BITS=8` redonne exactement le budget 10 %** : **66,6195 / 72,6501** dans les deux
chemins. Ce n'est pas une coïncidence : le budget 10 % sélectionne **toutes** les couches, et
le chemin explicite force toutes les couches. La règle (`kv_precision`) fait donc exactement
ce qu'elle dit ; les chiffres du mélange ne viennent ni d'un bug de sélection ni d'un cache
mal initialisé.

Et **`DRAVE_PERTE_MAX=0.001`** (aucune couche ne passe) redonne **61,9920 / 60,8135** : le
f32 est le régime zéro.

## Ce qui pourrait le rendre faux

- **Deux portes, un modèle** : Qwen2.5-0.5B Q8_0 ; le signe du mélange peut changer avec un
  autre modèle, une autre taille de cache ou un autre contexte.
- **La PPL n'est pas la qualité** : une PPL qui baisse de 5,9 % sur un mode n'est pas une
  amélioration démontrée — c'est un déplacement, et le mode 3 va dans l'autre sens.
- **La cause du signe n'est pas isolée** : « le mode de lot est dans l'effet » est une
  inférence de la comparaison mode 0 / mode 3, pas une mesure du mécanisme (occupation du
  cache, ordre des passes, alignement mémoire).
- **Une seule graine par mesure** : la PPL est déterministe ici, mais le cache et l'ordre des
  passes ne sont pas vérifiés au bit près entre deux exécutions.

## Ce que ça décide

**A8.3 reste opt-in** — mais la raison change : ce n'est plus « le défaut bouge les portes »
(c'est mesuré et reproductible), c'est **« le mélange a un effet de signe inexpliqué sur le
mode de lot »**. Le prochain pas n'est plus d'épingler le régime 1 % (il est reproductible),
c'est d'**isoler le mode de lot** : même régime, deux lots, comparer. Si l'effet est le lot,
la règle peut passer par défaut avec une note ; si l'effet est la précision, il faut revoir
`kv_precision`.

## Reproduire

```bash
bash tools/porte-flux.sh                                   # f32 : 61,9920 / 60,8135
DRAVE_PERTE_MAX=1 bash tools/porte-flux.sh                 # mélange : 58,3200 / 62,7357
DRAVE_KV_BITS=8 bash tools/porte-flux.sh                   # int8 partout : 66,6195 / 72,6501
CUDA_VISIBLE_DEVICES=1 DRAVE_KV_BITS=8 bash tools/porte-pont.sh   # 120,0813
```
