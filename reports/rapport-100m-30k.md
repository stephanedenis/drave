# Le 100 M à 30 000 pas — le run de nuit

> **Ce que ce document est.** Le suivi du run du 100 M (96,7 M de paramètres, d_model 640, 8 blocs,
> AMP, GPU) sur 30 000 pas, et ce qu'on en attend. Le banc à 3 000 pas est dans
> [`rapport-banc-generation.md`](rapport-banc-generation.md) ; le checkpoint :
> `work/n2ac/mix1024-100m-30k.pt` (à la fin).

## Le run

| mesure | valeur |
|---|---|
| le pas | **0,293 s** (8 × 1 024, AMP, une RTX 5000) |
| 30 000 pas | **~2 h 27** (ETA 22 h 55) |
| la VRAM | 5,7 Go / 16 |
| le GPU | 99 % |
| la PPL de validation | **3,202 à 11 450 pas** (en cours) |

## Ce qu'on attend (les hypothèses, écrites d'avance)

1. **La PPL** : le 34 M à 30 000 pas est à **2,40** ; le 100 M devrait passer **sous 2,0** s'il
   convertit ses 30× moins de données vues en qualité — sinon, l'échelle ne paie pas sur la PPL.
2. **Les mots valides** : 0,882 à 3 000 pas ; on attend **≥ 0,90** à 30 000, et une répétition
   **≤ 3**.
3. **Le débit** : ~80 octets/s sur GPU (le 100 M) — la génération reste memory-bound.

## Ce qui pourrait rendre ce run faux

- **Le sur-apprentissage** : 30 000 pas sur 1 Go, c'est ~30 tokens/paramètre (le 34 M en est à 7) —
  la PPL de validation peut remonter après 20 000 pas.
- **Le fp16** : la convergence en AMP n'est pas validée (le run le fera, ou pas).
- **Le corpus** : non épinglé (le val commence au milieu d'un mot) — la PPL n'est comparable qu'au
  même découpage.

## L'état (le 21/11, 21 h 20)

Le run est à **11 450 / 30 000 pas** (38 %), la PPL est à **3,202**, le GPU à 99 %. La suite : le
banc à la fin, puis la passe des portes.
