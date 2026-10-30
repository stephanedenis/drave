# A8.0 — `porte-trace` épingle sa PPL répartie : 59,0790

> **Ligne de roadmap** : A8.0 · **Date** : 2026-10-29 · **Verdict** : ✅ **douzième porte
> épinglée** — la PPL du chemin réparti f32 est ancrée, et le rejeu reste exact. A8.0 reste
> **partielle** : 12 portes sur 33.
>
> **Dispositif** : `tools/porte-trace.sh`, Qwen2.5-0.5B Q8_0, topologie 0–11/12–23, f32 ;
> référence **59,0790**, tolérance **5e-4** ; données [`a80-porte-trace.json`](a80-porte-trace.json).

## Ce qui est mesuré

| mesure | valeur |
|---|---:|
| PPL répartie f32 | **59,0790** |
| croisements enregistrés | **126** |
| rejeu | **identique** (aucune divergence) |
| trace fausse d’un bit | **détectée et nommée** |

La porte **exit 0** : la trace est produite, rejouée, et une fausse trace est refusée.

## Le contrôle négatif

La condition est numérique : `abs(ppl - 59,0790) <= 5e-4 × 59,0790`. Un décalage de **10 %**
est refusé par la même expression. Le contrôle porte sur la valeur, pas sur le nombre de lignes.

## Ce qui pourrait le rendre faux

- **Un seul modèle** et une topologie.
- **La PPL dépend de la limite** de la porte ; 59,0790 n’est pas 113,0068 (autre réglage).
- **Le rejeu ne dit rien de la qualité** ; il dit que la trace est fidèle.
- **5e-4** attrape 0,05 %, pas 0,01 %.

## Ce que ça change

A8.0 passe de **11/33** à **12/33**. N3.2a/b0/b1/b2, N3.3a/b/c, N3.4a/b sont verts ; le
placement (N3.4c) et une composition complète restent.

## Fichiers

- `tools/porte-trace.sh` — PPL répartie épinglée.
- `reports/a80-porte-trace.json` — les mesures.
- `reports/rapport-a80-porte-trace.md` — cette fiche.
