# Le pool de tampons : neutre en temps — et l'hypothèse qui l'avait motivé est réfutée

> Campagne : **moteur** · expérience : le pool des tampons de lecture séquentielle
> Question : la lecture dans nos tampons (`DRAVE_TAMPONS=1`) allouait **un tampon neuf par plage**
> — ~1 152 tampons de 0,88 Mo par jeton sur Qwen3-30B (48 couches × 8 experts × 3 matrices). Un
> tampon neuf au-dessus de 128 Ko, c'est un `mmap` anonyme : ~215 défauts de page **par** tampon,
> soit ~250 000 par jeton, pour des pages que `read_exact_at` remplit aussitôt. Un pool devait donc
> faire gagner du temps.
> Verdict : **non — le pool est neutre en temps.** Mesuré sur la même passe, mêmes conditions,
> deux répétitions : **2,4 s avant, 2,3-2,4 s après** (perplexité **799,8557** dans les deux cas).
> L'hypothèse des défauts de page était **fausse** : `glibc` réutilise les blocs de 0,88 Mo rendus
> par le jeton précédent (son seuil de `mmap` s'adapte après des `free` répétés), donc le chemin
> d'allocation ne repassait pas par le noyau. Le pool est **gardé** — il ne coûte rien, il **borne**
> la mémoire des tampons et il rend le mécanisme lisible — mais il n'est pas une optimisation.
> Date réelle : **2026-10-13, 06 h 00-06 h 20 HAE** (heure lue sur la machine)
> Protocole : `DRAVE_TAMPONS=1 drave <Qwen3-30B-A3B-Q4_K_M> --ppl … --limit 8 --threads 16`, deux
> binaires (avec et sans pool, construits du même arbre par `git stash`), deux répétitions chacun

## 1. Les mesures

| binaire | répétition | perplexité | passe |
|---|---|---:|---:|
| avant (allocation par tampon) | 1 | 799,8557 | 2,4 s |
| avant | 2 | 799,8557 | 2,4 s |
| **après (pool)** | 1 | 799,8557 | 2,4 s |
| **après (pool)** | 2 | 799,8557 | **2,3 s** |

Et le témoin du pool lui-même, publié par le moteur à la fin d'une passe :

```
[tampons] 32 allocations, 9184 réutilisations, 8 gardés (7,1 Mo) — le pool évite 100 % des allocations
```

Ce que ça dit :

* **le pool fait exactement ce qu'il annonce** : 9 184 tampons réutilisés pour 32 allocations
  (les 8 gardés couvrent les tailles du modèle), et **7,1 Mo** retenus au lieu de ~1 Go de tampons
  vivants ;
* **et il ne fait pas gagner de temps** : l'écart (0,0-0,1 s) est dans le bruit de deux
  répétitions. La porte des lecteurs le confirme de son côté (tampons : **6,21 Go lus, 3,05 s de
  calcul**, le meilleur des quatre bras — comme avant le pool, à 0,15 s près) ;
* **l'hypothèse était fausse, et c'est la partie utile** : « un tampon neuf = un `mmap` = 215
  défauts de page » est vrai **pour un tampon isolé**, pas pour une boucle qui alloue et libère la
  même taille mille fois par seconde — `glibc` monte alors son seuil de `mmap` et sert ces blocs
  depuis le tas. Le raisonnement était plausible et non mesuré ; la mesure l'a réfuté.

## 2. Ce qui est gardé, et pourquoi

Le pool reste dans le moteur, sur trois arguments qui ne sont pas de vitesse :

1. **la mémoire est bornée** (plafond de 512 Mo, 7,1 Mo en pratique sur ce modèle) au lieu de
   dépendre du comportement de l'allocateur ;
2. **le mécanisme est lisible** : la ligne `[tampons]` dit combien d'allocations ont été évitées,
   ce qui rend une régression visible (si le compte d'allocations se remet à grimper, la lecture
   ne passe plus par le pool) ;
3. **c'est l'endroit où un `madvise`/`MADV_DONTNEED` sur les tampons morts pourra se brancher** si
   l'on veut un jour rendre la mémoire au noyau — question qui, elle, n'est pas tranchée.

## 3. Ce que cette fiche ne dit pas

* elle ne dit rien du **recouvrement** (lire la couche suivante pendant qu'on calcule la
  courante) : c'est le pas suivant du chantier des lecteurs, et il se mesure autrement ;
* elle ne dit rien d'un **autre allocateur** (`jemalloc`/`mimalloc`) ni d'un autre noyau : la
  conclusion « neutre » vaut pour `glibc` sur cette machine, ce qui est le cas qui compte ici.
