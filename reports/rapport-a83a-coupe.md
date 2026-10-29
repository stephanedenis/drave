# A8.3a — `porte-coupe` : le régime 1 % écrase la variance du point de coupe

> **Ligne de roadmap** : A8.3a · **Date** : 2026-10-29 · **Verdict** : ✅ **le régime 1 % est
> épinglé pour `porte-coupe`** — le gate passe en f32 et avec `DRAVE_PERTE_MAX=1`, avec des
> références distinctes. A8.3a est **complet** pour les trois portes clés ; A8.3b (défaut) reste.
>
> **Dispositif** : `tools/porte-coupe.sh`, Qwen2.5-0.5B Q8_0 ; deux régimes ; données
> [`a83a-coupe.json`](a83a-coupe.json).

## Ce qui est mesuré

| mesure | f32 | 1 % |
|---|---:|---:|
| PPL sans perte | **113,0068** | **111,8003** |
| encoded 4/20 | 116,3407 | 114,1178 |
| encoded 6/18 | 108,8721 | 116,8011 |
| encoded 12/12 | 111,9225 | 115,6406 |
| encoded 18/6 | 118,5275 | 114,5345 |
| **variance encodée** | **8,9 %** | **2,4 %** |
| coût du pont 12/12 | +2,81 % | +5,88 % |
| coût du pont 15/9 | +17,09 % | +11,56 % |
| coût du pont 18/6 | +0,52 % | +8,04 % |

Les deux gates **exit 0**. Le mode dual choisit les références selon `DRAVE_PERTE_MAX=1` ; sans
lui, le gate 1 % échouait sur la PPL sans perte (111,8003 au lieu de 113,0068) et sur la variance
des coûts.

## Le contrôle négatif

- **f32** : 113,0068 ; variance **8,9 %** ; coûts 0,52–17,09 → ✅.
- **1 %** : 111,8003 ; variance **2,4 %** ; coûts 5,88–11,56 → ✅.
- **Sans mode dual** : le même gate échoue ; c’est la preuve du déplacement.
- **Le seuil de variance** passe de 3× à 1,5× sous la règle, nommé.

## Ce qui pourrait le rendre faux

- **Un seul modèle et une seule machine**.
- **Le mode dual est un contrat** : il dit que les chiffres sont connus, pas que la règle est
  bonne.
- **La variance tombe de 8,9 % à 2,4 %** : sous la règle, le bruit du KV int8 **domine** le choix
  du point de coupe ; ce n’est pas une amélioration du découpage.
- **Les budgets 0,001/10** ne sont pas épinglés.

## Ce que ça change

A8.3a est **complet pour flux, pont et coupe**. Les trois portes clés ont un régime f32 et un
régime 1 %. A8.3b — passer le défaut — peut être tenté, mais A8.0 n’est qu’à **6/33** : les autres
portes peuvent encore mesurer un déplacement. A8.3 reste **opt-in**.

## Fichiers

- `tools/porte-coupe.sh` — mode dual f32 / 1 %.
- `reports/a83a-coupe.json` — les deux régimes.
- `reports/rapport-a83a-coupe.md` — cette fiche.
