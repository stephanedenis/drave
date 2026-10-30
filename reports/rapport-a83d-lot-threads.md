# A8.3d — le lot n'est pas les threads : l'écart de 1,90 % survit à 1 thread

> **Ligne de roadmap** : A8.3 (suite d'A8.3c) · **Date** : 2026-10-30 · **Verdict** : ✅
> **condition affinée** — l'écart de PPL entre lot 1 et lot 4 (**1,90 %**) est **le même à 1 et à
> 8 threads**. Ce n'est donc pas le pool de threads : c'est le **noyau par lots** lui-même.
>
> **Dispositif** : `tools/porte-flux.sh` (mode 3, `--lot`), quatre réglages `THREADS` 1/8 ×
> `LOT` 1/4, Qwen2.5-0.5B-Q8_0, 24 ids, ctx 64 ; JSON
> [`a83d-lot-threads.json`](a83d-lot-threads.json).

## La question

A8.3c a montré que le lot déplace la PPL à lui seul : **61,9920** au lot 1 contre **60,8135** au lot
≥ 2 (−1,90 %), et l'a attribué aux « sommes réordonnées ». Deux causes restaient possibles : le
**pool de threads** (8 par défaut) ou le **noyau par lots** (sommes par bloc). Passer à **1 thread**
sépare les deux.

## Ce qui est mesuré

| threads | lot 1 | lot 4 | écart |
|---:|---:|---:|---:|
| **8** | **61,9920** | **60,8135** | **−1,90 %** |
| **1** | **61,9920** | **60,8135** | **−1,90 %** |

Le mode 0 (f32 dense, chemin jeton par jeton) donne **61,9920** aux deux nombres de threads : le pool
ne déplace pas le chemin non loti. Le mode 3 au lot 4 donne **60,8135** aux deux : le pool ne déplace
pas la valeur lotie. L'écart est donc **dans le chemin par lots**, pas dans les threads.

## Le contrôle négatif

- **Mode 0 à 1 thread = 61,9920** (la référence) : le pool n'est pas la cause de l'écart.
- **Mode 3 lot 4 à 1 thread = 60,8135** : le pool n'est pas la cause de la valeur lotie.
- **À 8 threads**, les deux réglages reproduisent A8.3c : 61,9920 / 60,8135.
- Si le pool était la cause, le lot 4 à 1 thread vaudrait 61,9920 ; il vaut 60,8135.

## Ce que ça décide

A8.3c est **affiné** : les sommes réordonnées sont celles du **noyau par lots** (sommes par bloc),
pas celles du pool de threads. Sur ce modèle **dense**, le routeur ne peut pas être la cause (il n'y
en a pas). Réduire l'écart demande un **ordre de somme déterministe dans le noyau par lots**, ou de
l'**assumer** comme deux références distinctes — ce que les portes font déjà (mode 0 : 61,9920 ;
mode 3 : 60,8135). Le nombre de threads n'est pas le levier.

## Ce qui pourrait le rendre faux

- **0,5 B, 24 ids, ctx 64** : l'ampleur de 1,90 % dépend du modèle et de la coupe ; elle peut être
  plus petite ailleurs (0,15 % sur le 30B, A8.3c).
- **La PPL n'est pas la qualité** : un chemin qui change la PPL de 1,9 % peut changer une génération
  sans changer le sens.
- **Le lot 1 n'est pas « la référence »** : c'est le chemin non loti ; le choix de la référence est
  une décision.
- **Un autre noyau, un autre ordre** : la conclusion « ce n'est pas le pool » est mesurée ; la cause
  précise (ordre des blocs, échelles d'activation) reste à instrumenter si l'on veut corriger.

## Fichiers

- `tools/porte-flux.sh` — le levier `THREADS` (défaut 8) ; la porte garde ses références.
- `reports/a83d-lot-threads.json` — les mesures.
- `reports/rapport-a83d-lot-threads.md` — cette fiche.
