# Le 73 M à 13 000 pas — l'échantillonnage décolle, le greedy se dégrade

> **Ligne de roadmap** : N4 (le banc du natif) · **Date** : 2026-11-18 · **Verdict** : ✅ mesuré —
> 10 000 pas de plus sur le 73 M (13 000 au total, corpus épinglé, lr 1e-4) font passer la
> perplexité de validation de **4,6792 à 3,4130** (−27 %). Le même pas fait **décoller
> l'échantillonnage** (top-40 : **0,551 → 0,831** de mots valides) et **dégrader le greedy**
> (répétition **6 → 11**, écho **0,015 → 0,149**, diversité **0,652 → 0,329**).
>
> **Dispositif** : `entrainer_native.py` (init `mix1024-100m.pt`, `--val` épinglé, AMP, seq 1 024,
> lot 8, 10 000 pas, 48,4 min) → `work/n3/r1.pt` ; banc complet
> [`bench/checkpoint_bench.sh`](../bench/checkpoint_bench.sh) (20 prompts, 128 octets, 3 réglages,
> contrôle aléatoire n=128) · données [`banc-generation-r1.json`](banc-generation-r1.json),
> [`banc-grammaticalite-r1.json`](banc-grammaticalite-r1.json).

## La table (n = 128, même banc)

| modèle | pas | PPL val | greedy mots / rép / d2 / écho | top-40 mots | top-20 mots |
|---|---:|---:|---|---:|---:|
| 34 M | 30 000 | 2,404 (fin du train) | **0,870** / **15** / 0,726 / 0,009 | 0,490 | 0,735 |
| 73 M | 3 000 | 4,014 (fin du train) | 0,878 / 6 / 0,652 / 0,015 | 0,551 | 0,673 |
| **73 M** | **13 000** | **3,413 (val épinglé)** | 0,902 / **11** / **0,329** / **0,149** | **0,831** | **0,883** |

*La PPL du 73 M à 13 000 est sur le `val.txt` épinglé ; les deux autres sont des mesures d'époque
sur la fin du train (voir [la fiche des deux découpages](rapport-natif-val-deux-decoupages.md)) :
les PPL ne sont pas comparables entre lignes, les générations le sont.*

## Lecture

1. **L'échantillonnage décolle** : top-40 passe de 0,551 à **0,831** de mots valides (+0,28),
   top-20 de 0,673 à **0,883** (+0,21) — c'est la première fois que le natif s'approche du 34 M en
   échantillonnage (0,490 / 0,735), et le dépasse.
2. **Le greedy se dégrade** : répétition 6 → **11**, écho 0,015 → **0,149** (le modèle recopie le
   prompt), diversité 0,652 → **0,329**. Plus le modèle est entraîné, plus le greedy tombe dans une
   boucle — un phénomène de **décodage**, pas une perte de modèle : le même checkpoint, échantillonné,
   est meilleur.
3. **Le critère du palier 1** (« répétition ≤ 3 ») est **atteint en échantillonnage** (top-40 : 2) et
   **pas en greedy** (11). Le critère doit donc nommer le réglage de décodage, sinon il mesure la
   stratégie de décodage et non le modèle.
4. **La grammaticalité suit le décodage** : greedy GV 0,50 et **75 % des textes sans verbe**
   (dégénérescence) ; top-40 GV 3,50, ciment 0,547, 5 % sans verbe. Le contrôle aléatoire garde
   GV 2,30-4,00 et un ciment ~0,80 — le ciment récompense les textes longs et réguliers, il ne
   mesure donc pas la qualité seule.

## Les contrôles

- **Même banc, même graine de prompts, même contrôle aléatoire** (n=128, poids au hasard) : le
  contraste modèle/bruit reste net en échantillonnage ; en greedy, le 73 M entraîné (GV 0,50) est
  **sous** son contrôle aléatoire (2,30) — signe que le greedy est un mauvais régime pour ce
  modèle, pas que le modèle a régressé.
- **Même corpus épinglé** (`fae5bb73…`), même val : la PPL 3,4130 nomme son corpus.
- **La courbe de PPL est monotone** : 4,6792 (init) → 3,612 (pas 9 700) → 3,413 (fin), sans
  divergence (lr 1e-4, AMP, clip 1.0).

## Ce qui pourrait le rendre faux

- **Une graine, un corpus de 1 Go, 0,66 époque** : le run n'a pas vu tout le corpus ; un second
  passage pourrait changer la courbe.
- **20 prompts, 128 octets** : le banc est petit ; l'écho de 0,149 en greedy peut dépendre des
  prompts.
- **La PPL n'est pas comparable entre les trois lignes** (val différents) ; seule la génération l'est.
- **Le « sans verbe » du greedy** peut refléter les phrases nominales autant que la dégénérescence ;
  l'écho et la répétition sont plus solides.

## Ce que ça change

Le palier 1 a maintenant son premier vrai point : **13 000 pas suffisent à débloquer
l'échantillonnage** (top-40 et top-20 au-dessus du 34 M), pas le greedy. La suite est double :
**continuer l'entraînement** (r2, en cours) pour voir si la répétition tombe encore, et **choisir un
décodage** (top-p) comme régime de production — le critère du palier doit être reformulé en
conséquence.

## Voir aussi

- [le banc](../bench/checkpoint_bench.sh) · [les données](banc-generation-r1.json) ·
  [la grammaticalité](rapport-grammaticalite-100m.md) · [les deux val](rapport-natif-val-deux-decoupages.md) ·
  [le plan natif](../docs/pilotage/natif-plan.md)
