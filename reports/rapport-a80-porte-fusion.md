# A8.0 — `porte-fusion` épingle sa PPL répartie : 113,0068

> **Ligne de roadmap** : A8.0 · **Date** : 2026-10-29 · **Verdict** : ✅ **onzième porte
> épinglée** — la PPL du chemin réparti f32 est ancrée, et la fusion des traces reste exacte.
> A8.0 reste **partielle** : 11 portes sur 33.
>
> **Dispositif** : `tools/porte-fusion.sh`, Qwen2.5-0.5B Q8_0, topologie 0–11/12–23, f32 ;
> référence **113,0068**, tolérance **5e-4** ; données [`a80-porte-fusion.json`](a80-porte-fusion.json).

## Ce qui est mesuré

| mesure | valeur |
|---|---:|
| PPL répartie f32 | **113,0068** |
| croisements fusionnés | **188** |
| divergence d’un bit | **détectée et attribuée** (code 3) |
| trace v1 | **refusée** (code 2) |

La porte **exit 0** : la fusion ordonne par temps mural, confronte les deux bouts, détecte la
divergence et refuse une trace sans horodatage.

## Le contrôle négatif

La condition est numérique : `abs(ppl - 113,0068) <= 5e-4 × 113,0068`. Un décalage de **10 %**
est refusé par la même expression. Le contrôle porte sur la valeur, pas sur le nombre de lignes.

## Ce qui pourrait le rendre faux

- **Un seul modèle et une topologie** (0–11/12–23) ; f32.
- **La PPL ne dit rien de la qualité de la fusion** : la porte vérifie l’ordre et la divergence.
- **188 croisements** dépendent du corpus et du nombre de pas.
- **5e-4** attrape 0,05 %, pas 0,01 %.

## Ce que ça change

A8.0 passe de **10/33** à **11/33**. N3.2a/N3.2b0/N3.3a/b/c/N3.4a sont verts ; N3.2b (seuil de
confiance) et la composition avec pont/placement restent.

## Fichiers

- `tools/porte-fusion.sh` — PPL répartie épinglée.
- `reports/a80-porte-fusion.json` — les mesures.
- `reports/rapport-a80-porte-fusion.md` — cette fiche.
