# La courbe 3 000 → 53 000 pas : la PPL baisse encore, l'échantillonnage repart au 5e tour, le greedy reste cassé

> **Ligne de roadmap** : N4 (le banc du natif) · **Date** : 2026-11-18 · **Verdict** : ✅ mesuré —
> cinq tranches de 10 000 pas sur le 73 M (corpus épinglé, lr 1e-4, AMP) : PPL de validation
> **4,6792 → 3,4130 → 3,2321 → 3,1317 → 3,0628 → 3,0098** (−36 % au total) ; l'**échantillonnage
> top-40** a plafonné à 0,867-0,870 (33k-43k) puis **repart à 0,895** au 5e tour, le top-20 à **0,932** ;
> le **greedy est instable** (0,902 → 0,924 → 0,865 → 0,896 → 0,897) et sa répétition reste à **10–13**.
>
> **Dispositif** : `entrainer_native.py` chaîné (`--init` du checkpoint précédent), `--val` épinglé,
> 5 × 10 000 pas (~48 min chacun) ; banc complet après chaque tranche
> ([`checkpoint_bench.sh`](../bench/checkpoint_bench.sh)) ; données `banc-generation-r{1,2,3,4,5a}.json`
> et `banc-grammaticalite-r{1,2,3,4,5a}.json`.

## La courbe

| étape | pas | PPL val | greedy valides / rép / écho | top-40 valides / rép | top-20 valides |
|---|---:|---:|---|---|---:|
| init | 3 000 | 4,6792 | 0,878 / 6 / 0,015 | 0,551 / 1 | 0,673 |
| r1 | 13 000 | 3,4130 | 0,902 / 11 / 0,149 | 0,831 / 2 | 0,883 |
| r2 | 23 000 | 3,2321 | **0,924** / 11 / 0,164 | 0,845 / 2 | 0,854 |
| r3 | 33 000 | 3,1317 | 0,865 / 10 / — | **0,870** / 2 | — |
| r4 | 43 000 | 3,0628 | 0,896 / 13 / 0,146 | 0,867 / 2 | 0,879 |
| r5a | 53 000 | **3,0098** | 0,897 / 11 / — | **0,895** / 2 | **0,932** / 3 |

## Lecture

1. **La PPL baisse encore, de moins en moins** : −1,27 (init → r1), −0,18, −0,10 par 10 000 pas.
   Le rendement décroît, comme attendu sur 1 Go de données (0,66 → 2 époques).
2. **L'échantillonnage progresse par paliers** : top-40 0,551 → 0,831 → 0,845 → 0,870 → 0,867 →
   **0,895** ; le plateau de 33k-43k s'est rouvert au 5e tour, et le top-20 atteint **0,932** (le
   meilleur chiffre du banc). Sur 20 prompts, une partie du mouvement est du bruit : la tendance
   reste haussière, pas monotone.
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
