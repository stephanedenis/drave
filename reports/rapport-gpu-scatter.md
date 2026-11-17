# P1 — la dispersion GPU optimisée bat la projection FPGA

> **Ligne de roadmap** : A5.4 (porte P1) · **Date** : 2026-11-17 · **Verdict** : ✅ **P1 tranché** —
> la dispersion d'événements sur **une** Quadro RTX 5000 atteint **29,37 G év/s** avec des
> accumulateurs par bancs (et **25,65 G év/s** avec la primitive à atomiques), contre **19,3 G év/s**
> *projetés* pour **4 cartes** Stratix V. Le GPU gagne par **1,52×** : le **débit** ne justifie pas le
> ring 40G.
>
> **Dispositif** : [`bench/gpu_scatter.py`](../bench/gpu_scatter.py) · Quadro RTX 5000 (15,6 Gio,
> 48 SM) · **268 435 456** événements, accumulateur de **4 096** sorties (celui du PE), valeurs et
> accumulateur **int32** (somme exacte, donc indépendante de l'ordre) · données
> [`gpu-scatter.json`](gpu-scatter.json).

## Ce qui est mesuré

| charge | atomiques | bancs B=4 | B=16 | B=64 |
|---|---:|---:|---:|---:|
| **O = 4 096, 268 M événements** | **25,65** | 29,18 | 29,34 | **29,37** |
| O = 4 096, 67 M événements | 25,22 | 26,40 | 27,15 | 27,31 |
| O = 1 024, 67 M événements | 8,45 | 18,49 | 27,09 | **27,32** |
| O = 65 536, 67 M événements | **27,03** | 27,10 | 2,71 | 1,16 |

*G év/s, médiane de 3 passes ; le résultat d'une méthode est **bit-exact** celui des autres.*

## Ce que ça corrige

Le bilan multi-matériel donnait **18,1 G év/s** pour la dispersion GPU : sur la même carte, la
primitive à atomiques mesurée ici fait **25,2–25,7 G**. Le chiffre de référence était donc celui
d'une primitive plus lente, pas la limite de la carte. **La référence GPU est corrigée à 25,7 G év/s
(atomiques), 29,4 G (bancs).**

## Le contrôle négatif, et il compte

- **Le harnais est vérifié** : sur un million d'événements, `np.bincount` (CPU) et l'accumulateur GPU
  donnent le même vecteur — **écart maximal 0**.
- **Toutes les méthodes sont bit-exactes** entre elles (l'entier est associatif) : la banque ne
  « gagne » pas en changeant le résultat.
- **La banque n'est pas magique** : à O = 65 536, B = 64 fait **s'effondrer** le débit (1,16 G év/s)
  — 64 × 65 536 = 4,2 M de cases dispersées, la mémoire cache ne suit plus. Le mécanisme a un
  domaine, et il est mesuré.
- **La contention est la vraie limite** : à O = 1 024, les atomiques tombent à 8,45 G év/s ; les
  bancs rendent 3,2×. C'est ce que la banque achète — de la contention, pas de la bande passante.

## Ce qui pourrait le rendre faux

- **Destinations uniformes** : les listes réelles ont de la localité (les listes sont croissantes par
  source, les destinations groupées), ce qui *aide* les deux méthodes — le chiffre uniforme est un
  plancher déguisé, pas un plafond.
- **Les valeurs sont int32** : le moteur accumule en `f32` ; la somme flottante n'est pas associente
  et la banque changerait le résultat à l'arrondi près (à déclarer dans un contrat, comme `bloque`).
- **L'accumulateur est remis à zéro à chaque appel**, alors que le moteur le réutilise : un
  accumulateur chaud changerait la part de l'écriture.
- **Un seul GPU, un seul flux** : le débit est celui d'une carte ; NVLink et le multi-carte ne sont
  pas testés ici.
- **Le flux d'événements n'est pas lu depuis la mémoire** : dans le moteur, 0,7 Go de listes par
  jeton doivent d'abord être lus (380 Go/s → ~42 G év/s au mieux, à 9 octets par événement) — le
  29,4 G mesuré est ~70 % de cette borne, pas un débit hors-sol.

## Ce que ça change

**P1 d'A5.4 est clos : le débit ne justifie pas le ring 40G.** Ce qui reste au FPGA est nommé et
plus faible : l'**énergie** (8,3 nJ/év *projeté* contre 12,7 nJ déduits pour le GPU, soit 1,5× et
non 7× — les 7× sont contre le CPU), le **déterminisme** bit-exact, la **capacité** (16 Go, égale à
la VRAM d'un GPU) et la **démonstration** du réparti. La décision de rouvrir A5.4 ne se prend plus
sur le débit : elle se prend sur P2 (le ring tient-il 4,8 Go/s ?) et sur une charge où le calcul
domine, qui n'existe pas encore.

Côté moteur, la leçon est directe : un accumulateur **petit** (≤ 4 096) gagne à être bancarisé
(1,08–1,15× ici, 3,2× sous forte contention) ; un accumulateur **grand** n'y gagne rien et peut y
perdre.

## Voir aussi

- [le banc](../bench/gpu_scatter.py) · [les données](gpu-scatter.json) ·
  [bilan multi-matériel](bilan-multi-materiel.md) · [rapport-cpu-aer](rapport-cpu-aer.md) ·
  [A5.4](../docs/pilotage/backlog/A5.4-fpga.md)
