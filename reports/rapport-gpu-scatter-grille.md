# P1b — la grille : la banque est un remède à la contention, pas un accélérateur

> **Ligne de roadmap** : A5.4 (P1) · **Date** : 2026-11-17 · **Verdict** : ✅ mesuré — sur la même
> Quadro RTX 5000 et 67,1 M d'événements, la dispersion par bancs vaut **6,0×** à **512** sorties,
> **3,3×** à 1 024, **1,06×** à 4 096, **rien** à 16 384 et **nuit** à 65 536 (1,16 G év/s à B=64).
> Le plateau est **26–28 G év/s** : le débit maximal ne dépend pas de la méthode, seulement de la
> taille de l'accumulateur.
>
> **Dispositif** : [`bench/gpu_scatter.py`](../bench/gpu_scatter.py) · accumulateur de `O` sorties ×
> `B` bancs, valeurs et accumulateur **int32** (somme exacte) · données
> [`gpu-scatter-grille.json`](gpu-scatter-grille.json).

## La grille (G év/s, médiane de 3 passes)

| O \ B | atomiques | B=4 | B=16 | B=64 |
|---:|---:|---:|---:|---:|
| **512** | 4,76 | 16,55 | 28,16 | **28,52** |
| **1 024** | 8,42 | 19,65 | 27,14 | **27,53** |
| **4 096** | 25,18 | 26,02 | 26,51 | **26,57** |
| **16 384** | **26,58** | 26,51 | **26,64** | 2,73 |
| **65 536** | **26,98** | 26,36 | 2,70 | 1,16 |

## Lecture

- **À gauche, c'est la contention qui limite** : 512 sorties et 67 M d'événements, chaque case est
  écrite ~131 000 fois ; les atomiques s'écroulent à 4,76 G év/s. La banque divise la pression par
  `B` et rend **6×**.
- **Au milieu, c'est la bande passante** : dès 4 096 sorties, les atomiques atteignent le plateau
  (~25–27 G év/s) et la banque n'apporte plus que 5 %.
- **À droite, la banque se retourne** : 64 bancs × 65 536 sorties = 4,2 M de cases dispersées ; le
  tableau de bancs ne tient plus dans le cache et le débit s'effondre à 1,16 G év/s. **Le remède
  devient le mal.**
- **L'accumulateur du PE (4 096 sorties) est exactement au genou** : 25,18 (atomiques) contre 26,57
  (B=64), soit +5,5 % — pas de quoi changer une architecture, mais de quoi choisir la variante.

## Contrôles

- **Bit-exact** : toutes les méthodes rendent le même accumulateur (l'entier est associatif) ;
  `B=1` (bancs) ≡ atomiques, ce qui valide le harnais de bancs.
- **Référence CPU** : `np.bincount` sur 1 M d'événements — écart maximal **0**.
- **Le retournement est mesuré**, pas supposé : c'est lui qui donne un domaine à la technique.
- **Les deux cartes** (Quadro identiques, `--gpu 0` / `--gpu 1`) : atomiques **25,20 / 25,23**,
  bancs B=64 **28,14 / 27,07** — ~4 % d'écart, dans le bruit. La mesure n'est pas liée à une carte.

## Ce qui pourrait le rendre faux

- **Destinations uniformes** : les listes réelles ont de la localité ; les deux méthodes en
  profiteraient, mais pas dans les mêmes proportions.
- **int32** : le moteur accumule en `f32` ; la somme flottante n'est pas associative, et la banque
  changerait le résultat à l'arrondi près (à déclarer dans un contrat).
- **Un GPU, un flux, N = 67 M** : le plateau et le genou peuvent se déplacer avec la carte et le
  nombre d'événements (à 268 M, le plateau monte à ~29,4 G).

## Ce que ça change

Pour le moteur : **bancariser seulement quand l'accumulateur est petit** (≤ 1 024 : 3–6×), pas
au-delà. Pour A5.4 : même le pire cas mesuré (25,2 G év/s à 4 096 sorties) reste **au-dessus** des
19,3 G projetés pour 4 cartes — P1 tient, la grille ne fait que préciser où.

## Voir aussi

- [P1](rapport-gpu-scatter.md) · [le banc](../bench/gpu_scatter.py) ·
  [les données](gpu-scatter-grille.json) · [A5.4](../docs/pilotage/backlog/A5.4-fpga.md)
