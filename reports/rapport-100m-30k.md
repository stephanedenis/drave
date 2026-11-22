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
## Le résultat du run (le 22/11, 02 h 55 UTC / 22 h 55 HNE)

| mesure | valeur | l'hypothèse écrite d'avance | verdict |
|---|---:|---|---|
| le pas | 0,292 s | — | ✅ |
| la durée | **2 h 26** (8 759 s) | ~2 h 27 | ✅ |
| la PPL de validation | **2,944** | < 2,0 | ❌ |
| la précision top-1 | **0,676** | — | — |
| le banc, mots valides (greedy) | **0,501** | ≥ 0,90 | ❌ |
| le banc, répétition | **1** | ≤ 3 | ✅ |
| le banc, distinct_2 | **1,000** | — | — |

**Le résultat honnête : l'échelle ne paie pas au-delà de 3 000 pas.** Le 100 M à 30 000 pas
(**0,501** de mots valides) fait **moins bien** que le même modèle à 3 000 pas (**0,882**) — et
que le 34 M à 30 000 pas (0,870). La PPL de validation (2,944) **dépasse** celle du 34 M (2,40).

**L'explication la plus probable : le sur-apprentissage.** 30 000 pas sur 1 Go, c'est **~30
tokens/paramètre** — le 34 M en est à 7. Le modèle a mémorisé le corpus (la précision top-1 monte
à 0,676, la répétition tombe à 1, le distinct_2 monte à 1,000) au détriment de la généralisation
(les mots valides s'effondrent, la sortie devient du texte mémorisé, pas composé).

**Ce que ça change** : le **palier 1 n'est pas « un plus gros modèle »** — c'est **un plus gros
modèle AVEC plus de données**. Le 3 000 pas du 100 M (0,882) reste le meilleur point de la courbe,
et il a vu 30× moins de données. La donnée est le verrou, pas la taille.

**Ce qui pourrait rendre ce verdict faux** : un taux d'apprentissage trop élevé à 30 k (la perte
d'entraînement descend à 1,0 — le modèle colle au train), ou un corpus trop étroit (1 Go, ~98 %
Wikipédia). Le test décisif : le **même run avec 10× plus de données**.
