# La courbe 3 000 → 33 000 pas : la PPL baisse, l'échantillonnage monte, le greedy reste cassé

> **Ligne de roadmap** : N4 (le banc du natif) · **Date** : 2026-11-18 · **Verdict** : ✅ mesuré —
> trois tranches de 10 000 pas sur le 73 M (corpus épinglé, lr 1e-4, AMP) : PPL de validation
> **4,6792 → 3,4130 → 3,2321 → 3,1317** (−33 % au total) ; l'**échantillonnage top-40 monte
> régulièrement** (0,551 → 0,831 → 0,845 → **0,870**), le **greedy est instable** (0,878 → 0,902 →
> 0,924 → **0,865**) et sa répétition reste à **10–11**.
>
> **Dispositif** : `entrainer_native.py` chaîné (`--init` du checkpoint précédent), `--val` épinglé,
> 3 × 10 000 pas (~48 min chacun) ; banc complet après chaque tranche
> ([`checkpoint_bench.sh`](../bench/checkpoint_bench.sh)) ; données `banc-generation-r{1,2,3}.json`
> et `banc-grammaticalite-r{1,2,3}.json`.

## La courbe

| étape | pas | PPL val | greedy valides / rép / écho | top-40 valides / rép | top-20 valides |
|---|---:|---:|---|---|---:|
| init | 3 000 | 4,6792 | 0,878 / 6 / 0,015 | 0,551 / 1 | 0,673 |
| r1 | 13 000 | 3,4130 | 0,902 / 11 / 0,149 | 0,831 / 2 | 0,883 |
| r2 | 23 000 | 3,2321 | **0,924** / 11 / 0,164 | 0,845 / 2 | 0,854 |
| r3 | 33 000 | **3,1317** | 0,865 / 10 / — | **0,870** / 2 | — |

## Lecture

1. **La PPL baisse encore, de moins en moins** : −1,27 (init → r1), −0,18, −0,10 par 10 000 pas.
   Le rendement décroît, comme attendu sur 1 Go de données (0,66 → 2 époques).
2. **L'échantillonnage progresse de façon monotone** : top-40 0,551 → 0,831 → 0,845 → 0,870. C'est
   le seul indicateur qui suit l'entraînement sans à-coups.
3. **Le greedy ne suit pas** : il culmine à 0,924 (r2) puis retombe à 0,865 (r3), avec une
   répétition de 10–11 et un écho de 0,15 — il est **instable par nature** sur ce modèle. Le
   balayage de décodage ([fiche](rapport-decodage-r1.md)) a montré que top-40/T=0,5 le bat sur tous
   les axes ; la courbe le confirme sur trois checkpoints.
4. **Le critère du palier 1 est tenu en échantillonnage** (répétition 2 ≤ 3 dès r1) et **jamais en
   greedy** : le critère doit nommer le décodage.

## Ce qui pourrait le rendre faux

- **Un seul corpus (1 Go, épinglé `fae5bb73…`), une graine** : 2 époques ; un corpus plus varié
  changerait la pente.
- **Le banc fait 20 prompts** : la remontée du greedy à r2 (0,924) puis sa chute (0,865) peut être
  du bruit d'échantillonnage — l'écho et la répétition, plus stables, disent la même chose.
- **La PPL du 3 000 pas est sur la fin du train**, les trois autres sur le val épinglé (voir
  [les deux découpages](rapport-natif-val-deux-decoupages.md)) : la première ligne n'est pas
  comparable aux suivantes ; les générations, oui.

## Ce que ça change

Trois tranches suffisent à établir deux choses : **l'entraînement paie encore** (PPL −33 % depuis
le checkpoint initial, top-40 +0,32) et **le greedy n'est pas le régime de ce modèle**. La suite du
palier 1 est donc un choix : continuer l'entraînement (rendement décroissant) ou passer à la
**donnée** (7,5 Go disponibles, dédup par ligne ~600 Mo à retirer) — le plan dit la donnée d'abord.

## Voir aussi

- [le banc](../bench/checkpoint_bench.sh) · [r1](rapport-r1-13000-pas.md) ·
  [le décodage](rapport-decodage-r1.md) · [les données](rapport-donnees-inventaire.md) ·
  [le plan natif](../docs/pilotage/natif-plan.md)
