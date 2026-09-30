# Drave — l'architecture « push » (AER) sur CPU

## L'architecture

Au lieu de **tirer** les activations à des indices arbitraires (gather), on
**pousse** : chaque source active émet un événement, sa liste de destinations se
lit **séquentiellement**, et on disperse `acc[dest] += signe · x[src]`.

- la liste d'activation se construit **en cascade** (compaction des non-nuls) ;
- l'accès aléatoire se déplace de l'entrée (activation, large) vers la sortie
  (accumulateur, 4096 × 24 bits = **12 Kio**, tient dans les M20K) ;
- les poids se lisent en **flux séquentiel** : plus aucun gather.

## Mesures sur ce bi-Xeon E5-2687W v3

- bande passante lecture séquentielle : **11.5 Go/s**
- dispersion (`np.bincount`) : **183999808.87 G événements/s**
- dispersion (`np.add.at`) : 364797216.41 G événements/s

## Limites mesurées du CPU (bench/cpu_aer.c, 16 threads)

| Test | 1 th | 8 th | 16 th | 32 th |
|---|---|---|---|---|
| Lecture séquentielle | 4,1 Go/s | 23,4 | **28,7** | 28,2 |
| Dispersion pure | 0,96 G év/s | 3,46 | 3,20 | 3,22 |
| **Écarts + dispersion** | 0,87 | 4,55 | **7,79** | 6,79 |

La dispersion sature vers 8 threads : c'est l'accès aléatoire à
l'accumulateur qui limite, pas la bande passante. Le décodage par écarts est
quasi gratuit (le noyau complet est plus rapide que la dispersion pure).

## Projection 7B (densité 5 %, 0,476 b/poids)

| Cible | ms/token | tok/s |
|---|---|---|
| CPU, borné bande passante (28,7 Go/s) | 14.51 | 68.9 |
| CPU, borné noyau (7,79 G év/s) | 44.93 | 22.3 |
| **CPU réaliste** | **44.93** | **22.3** |
| 1 carte FPGA | 43.12 | 23.2 |
| 4 cartes FPGA (modèle réparti) | 10.78 | 92.8 |

## Verdict

1. **Oui, c'est pensable sur CPU** — et c'est même la bonne façon de valider le
   format avant d'écrire du RTL : un CPU sert de **modèle d'or** pour la sémantique
   des événements (quels non-nuls, quel ordre, quelles échelles).
2. **La dispersion n'est pas le goulot** tant que l'accumulateur tient dans le
   cache : 183999808.9 G événements/s mesurés contre 0.35 G nécessaires par token.
3. **Une carte FPGA ≈ ce CPU** (23 contre 22 tok/s) : le CPU a
   3× la bande passante (28,7 contre 9,66 Go/s) mais il est limité par sa
   **cadence d'événements** (7,8 G/s), là où la carte est limitée par sa DDR3.
   Les deux arrivent au même point par des chemins opposés.
4. **L'avantage du FPGA est le passage à l'échelle, pas la carte seule** :
   4 cartes = 4 mémoires et 4 jeux de voies indépendants → 4× le débit, là où
   le CPU bute sur ses contrôleurs mémoire. C'est **exactement l'argument du
   ring** : additionner des systèmes mémoire autonomes.
5. **Conséquence pratique** : écrire d'abord l'implémentation CPU. Elle est
   immédiate, elle valide le format et la sémantique des événements, et elle
   fournit le **modèle d'or** que le RTL devra reproduire. Le FPGA n'a de sens
   qu'à partir de 2-4 cartes.

> ⚠️ Mesures sur un seul type de couche et un CPU donné. La dispersion réelle
> d'un noyau optimisé (SIMD, multi-thread, accumulateurs par banc) peut aller
> plus vite que `np.bincount` ; à confirmer avec un noyau C/OpenMP avant de
> conclure définitivement.


---
*Généré par `run_cpu.py` — Drave.*
