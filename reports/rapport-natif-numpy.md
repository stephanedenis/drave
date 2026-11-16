# L'inférence numpy du natif — 4/4 de parité, sans torch

> **Ligne de roadmap** : **N4** (le runtime du natif) · **Date** : 2026-11-16 ·
> **Verdict** : ✅ **le DRVM s'infère en numpy seul** — la **parité 4/4** avec torch sur le
> greedy, **sans torch** (numpy uniquement), à **~0,6 s/octet** (contre ~0,15 pour torch).
>
> **Le chiffre.** `tools/drvm_infere.py` charge les **127 tenseurs** du DRVM (130,9 Mo) en
> numpy et refait la passe avant : la **même sortie** que torch sur 4 prompts (16, 16, 8 et 24
> octets) ; `drave generer --moteur numpy` l'expose dans la CLI, **sans torch**.

## 1. Ce qui est livré

- [`tools/drvm_infere.py`](../tools/drvm_infere.py) : le chargeur (les 127 tenseurs, le
  manifeste), la passe avant (`_ln`, `_linear`, `_silu`, `_ffn` (la MoE, top-2, k-WTA), `_bloc`
  (l'attention causale + la fenêtre), le pont, la pensée, la tête), le greedy.
- [`tools/drave.py`](../tools/drave.py) : `generer --moteur {auto,torch,numpy}` ; `numpy` lit le
  **DRVM** (le `.drvm` à côté du `.pt`), `torch` le `.pt` ; les refus (code 4) sans torch ni DRVM.

## 2. La parité (le contrôle le plus dur)

| prompt | octets | torch | numpy |
|---|---:|---|---|
| « La France est un pays » | 16 | `don d d da d 20` | **identique** |
| « Dans les années 1950 » | 16 | `le por le de la` | **identique** |
| « Le chat » | 8 | `in de en` | **identique** |
| « Il était une fois » | 24 | `de de pre dile de de de` | **identique** |

**4/4.** Le greedy est déterministe : la moindre différence de calcul (la norme, l'attention, la
MoE) produirait un autre octet ; la parité exacte prouve que la passe avant est reproduite.

## 3. Le coût

| moteur | dépendance | 16 octets | par octet |
|---|---|---:|---:|
| **torch** | `torch` (~200 Mo installé) | 3,3 s | **~0,15 s** |
| **numpy** | `numpy` (déjà là) | 15,1 s | **~0,6 s** |

La numpy est **~4× plus lente** (pas de BLAS fusionné, pas de threading) mais elle **supprime la
dépendance lourde** : c'est le chemin « 0 dépendance » du produit.

## 4. Ce que ce travail ne change pas

- **La qualité** : le modèle produit toujours des **collages** (le banc) — la numpy ne rend pas
  le 34 M meilleur, elle le rend **portable**.
- **La vitesse** : 0,6 s/octet reste lent pour un service (le byte-level) ; le palier 1
  (100–150 M) sera plus lent encore en numpy.
- **Le DRVM** : l'extraction des tenseurs passe par `bytes()` (une copie de 130 Mo) ; le mmap
  direct demanderait un lecteur par tenseur (une optimisation, pas un blocage).

## 5. La conclusion

Le natif est désormais **exécutable sans torch**, sur le seul numpy — le conteneur DRVM tient sa
promesse (« lisible par bloc », sans framework). C'est la brique **runtime** du plan
([`natif-plan.md`](../docs/pilotage/natif-plan.md)) : le palier 1 pourra être servi par ce
chemin, et le produit garde son « 0 dépendance » pour le bloc linguistique.
