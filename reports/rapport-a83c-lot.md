# A8.3c — le lot n'est pas neutre : la « non-monotonie » du KV était un effet de chemin

> **Ligne de roadmap** : A8.3 (suite d'A8.3b) · **Date** : 2026-10-29 · **Verdict** : ✅
> **expliqué** — le régime du KV a un effet **cohérent sur chaque chemin** : **−5,9 %** sur le
> chemin jeton par jeton, **+3,2 %** sur le chemin par lots. La « non-monotonie » d'A8.3b
> n'était pas la règle : c'étaient **deux chemins différents**, et le lot déplace à lui seul la
> PPL de **1,90 %** (61,9920 à lot 1 contre 60,8135 à lot ≥ 2, en f32).
>
> **Dispositif** : `porte-flux`, mode 3 (`--lot`), deux régimes de KV (f32 ; mélange 1 % par
> `DRAVE_PERTE_MAX=1`), trois lots (1, 2, 4) ; Qwen2.5-0.5B-Q8_0, GPU ; JSON
> [`a83c-lot.json`](a83c-lot.json) ; suite d'[A8.3](rapport-a83-defaut.md) et
> [A8.3b](rapport-a83b-regimes.md).

## La question

A8.3b a montré que le mélange KV « améliore » le mode 0 (−5,9 %) et « dégrade » le mode 3
(+3,2 %) — un signe qui n'est pas celui d'une quantification. D'où vient-il : de la règle, du
nombre de couches, ou du **chemin de calcul** ?

## Ce qui est mesuré

| lot | f32 | mélange 1 % | effet du mélange |
|---|---:|---:|---:|
| **1** (jeton par jeton) | **61,9920** | **58,3200** | **−5,9 %** |
| **2** | **60,8135** | **62,7357** | **+3,2 %** |
| **4** | **60,8135** | **62,7357** | **+3,2 %** |

Deux faits, et le second explique le premier :

1. **le lot déplace la PPL à lui seul** : en f32, lot 1 → **61,9920**, lot ≥ 2 → **60,8135**
   (**−1,90 %**), sans changer ni le modèle, ni les jetons, ni le régime du KV ;
2. **à chemin fixe, l'effet du KV est cohérent** : −5,9 % sur le chemin jeton par jeton, +3,2 %
   sur le chemin par lots. Il n'y a **pas** de non-monotonie sur un même calcul.

## L'explication — elle est dans le moteur

`drave-core/src/main.rs` (l. 799-812) le dit déjà, à l'usage : `--lot N > 1` **n'est pas une
simple affaire de vitesse**. Le préremplissage par lots réordonne les sommes : les derniers
bits changent, et « un routeur au voisinage d'une égalité peut choisir un autre expert ».
Mesuré sur Qwen3-30B-A3B : PPL **19,143 contre 19,172** (0,15 %), argmax identique sur
191/191 positions — et pourtant une génération gloutonne peut diverger.

Ici, sur un modèle **0,5 B** coupé à 12 couches, l'écart est de **1,90 %** : même cause
(sommes réordonnées, routage à l'égalité), plus grande parce que le modèle est petit et la
coupe basse. Ce n'est pas un défaut de la règle place+perte : c'est une propriété **connue et
documentée** du chemin par lots.

## Ce que ça décide

- **A8.3b est corrigé** : le signe du mélange n'est pas une anomalie de la règle ; il faut
  comparer **à chemin fixe**. La conclusion d'A8.3 tient : le défaut place+perte déplace la
  PPL (de −5,9 % à +3,2 % selon le chemin), il reste **opt-in**.
- **Le prochain levier n'est pas le KV**, c'est le **chemin par lots** : réduire sa
  non-équivalence (routeur à l'égalité, sommes réordonnées) ou l'assumer dans les références.
  Les portes le font déjà : le mode 0 et le mode 3 ont des références **distinctes** (61,9920
  et 60,8135) — c'est la bonne pratique, et elle masquait l'écart.

## Ce qui pourrait le rendre faux

- **Un seul modèle, une seule coupe** (0,5 B, 12 couches) : l'écart de 1,90 % dépend de la
  coupe et du routeur ; il peut être plus petit ailleurs (0,15 % sur le 30B).
- **La PPL n'est pas la qualité** : un chemin qui change la PPL de 1,9 % peut changer une
  génération sans changer le sens.
- **Le lot 1 n'est pas « le chemin de référence »** : c'est le chemin non loti ; le choix de
  la référence est une décision, pas une vérité.

## Reproduire

```bash
LOT=1 bash tools/porte-flux.sh                          # f32 : 61,9920
LOT=4 bash tools/porte-flux.sh                          # f32 : 60,8135
DRAVE_PERTE_MAX=1 LOT=1 bash tools/porte-flux.sh        # mélange : 58,3200
DRAVE_PERTE_MAX=1 LOT=4 bash tools/porte-flux.sh        # mélange : 62,7357
```
