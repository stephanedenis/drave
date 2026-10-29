# A8.3 — le défaut place+perte n'est pas neutre : les portes épinglées bougent de −5,9 % à +19,5 %

> **Ligne de roadmap** : A8.3 (et A8.0) · **Date** : 2026-10-29 · **Verdict** : ❌ **le
> passage par défaut est refusé, chiffres en main** — la règle place+perte déplace la PPL
> des portes épinglées de **−5,9 %** (flux mode 0, budget 1 %) à **+19,5 %** (flux mode 3,
> budget 10 %). Elle **reste opt-in** ; ce qui manque n'est pas une porte, c'est un
> **régime** de référence.
>
> **Dispositif** : `DRAVE_PERTE_MAX` (budget en %) sur les portes déjà épinglées par A8.0 ;
> trois budgets — **0,001 %** (aucune couche ne passe en int8), **1 %** (le défaut prévu),
> **10 %** (toutes les couches) ; CPU/GPU comme les portes ; JSON
> [`a83-defaut.json`](a83-defaut.json) ; porte
> [`porte-flux.sh`](../tools/porte-flux.sh) et [`porte-pont.sh`](../tools/porte-pont.sh).

## La question

A8.0 a épinglé deux portes qui mesurent une PPL (flux **61,9920 / 60,8135**, pont
**113,0068**). A8.3 demandait : la règle **place et perte** peut-elle devenir le **défaut** ?
La réponse devait être oui si les portes épinglées ne bougeaient pas. Elles bougent.

## Ce qui est mesuré

| budget `DRAVE_PERTE_MAX` | flux mode 0 | flux mode 3 | pont (dense) |
|---|---:|---:|---:|
| **0,001 %** (aucune couche int8) | **61,9920** (réf) | **60,8135** (réf) | — |
| **1 %** (le défaut prévu) | **58,3200** (−5,9 %) | **62,7357** (+3,2 %) | **111,8003** (−1,1 %) |
| **10 %** (toutes les couches) | **66,6195** (+7,5 %) | **72,6501** (+19,5 %) | — |

**Ce que la dose-réponse établit** : à budget quasi nul, la règle ne sélectionne aucune
couche int8 et les portes rendent **exactement** leur référence — le chemin de l'env var
fonctionne, et l'écart n'est pas un artefact de lancement. À 10 %, la quantification dégrade
dans le sens attendu (+7,5 % / +19,5 %). À 1 %, le mélange (dernières couches en int8,
premières en f32) **n'est pas monotone** : flux mode 0 *s'améliore* de 5,9 % quand flux
mode 3 se dégrade de 3,2 %. Ce signe n'est pas celui d'une quantification ; il y a un
**second effet** (probablement la taille du cache KV, donc l'occupation mémoire et l'ordre
des passes) que cette campagne ne sépare pas.

## Le contrôle négatif

| contrôle | ce qu'il devait faire | ce qu'il a fait |
|---|---|---|
| **budget 0,001 %** (aucune couche) | rendre la référence exacte | ✅ **61,9920 / 60,8135**, au chiffre près |
| **budget 10 %** (toutes les couches) | dégrader | ✅ **+7,5 % / +19,5 %** |
| **comparaison à A8.0** | le même chiffre sans la règle | ✅ 61,9920 / 60,8135 / 113,0068 |

Le premier contrôle est celui qui compte : sans lui, un écart pourrait venir du lancement,
du cache ou du modèle. Avec lui, l'écart est **causalement** la règle.

## Ce qui pourrait le rendre faux

- **Un seul modèle, une seule machine** : Qwen2.5-0.5B Q8_0 sur cette machine ; le signe
  peut changer avec un autre modèle ou un autre matériel.
- **La PPL n'est pas la qualité** : une PPL qui baisse de 5,9 % n'est pas une amélioration
  démontrée ; c'est un déplacement de la mesure.
- **Le second effet n'est pas isolé** : la non-monotonie à 1 % (mode 0 s'améliore) peut venir
  de l'occupation du cache KV, pas de sa précision — la campagne ne sépare pas les deux.
- **Deux portes, pas toutes** : flux et pont sont épinglées ; coupe, gain et les autres ne
  sont pas mesurées ici (elles ont leurs propres références).
- **Le budget 1 % n'a pas été vérifié couche par couche** : le nombre exact de couches
  passées en int8 est celui que `kv_precision` choisit, pas un comptage indépendant.

## Ce que ça décide

**A8.3 reste opt-in.** Le passage par défaut exigerait de **épingler le régime 1 %** en plus
du régime f32 — deux références par porte, pas une — et d'expliquer la non-monotonie avant de
la choisir. C'est le prochain pas nommé : `A8.3a` (épingler le régime 1 %) puis `A8.3b`
(défaut), ou corriger la règle si le second effet est un défaut.

## Reproduire

```bash
DRAVE_PERTE_MAX=0.001 bash tools/porte-flux.sh   # référence exacte
DRAVE_PERTE_MAX=1     bash tools/porte-flux.sh   # le défaut prévu
DRAVE_PERTE_MAX=10    bash tools/porte-flux.sh   # toutes les couches
DRAVE_PERTE_MAX=1     bash tools/porte-pont.sh   # 111,8003 au lieu de 113,0068
```
