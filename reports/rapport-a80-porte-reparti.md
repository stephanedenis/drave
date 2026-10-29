# A8.0 — `porte-reparti-moteur` épingle sa PPL : 9,1748

> **Ligne de roadmap** : A8.0 · **Date** : 2026-10-29 · **Verdict** : ✅ **cinquième porte
> épinglée** — le découpage de **notre** modèle route ne change pas la PPL, et la valeur absolue
> est ancrée. A8.0 reste **partielle** : 5 portes sur 33.
>
> **Dispositif** : `tools/porte-reparti-moteur.sh`, modèle route seed 1 (192 dim, 4 couches,
> 8 experts top-2), 255 octets de `corpus_en_val` ; référence **9,1748**, tolérance **1e-3** ;
> données [`a80-porte-reparti.json`](a80-porte-reparti.json).

## Ce qui est mesuré

| mesure | PPL | écart |
|---|---:|---:|
| modèle entier | **9,1748** | — |
| deux nœuds, 2 couches locales | **9,1748** | 0,0000 % |

La porte **exit 0** ; la PPL est épinglée, le découpage ne change pas le chiffre.

## Le contrôle négatif

La condition est numérique : `abs(ref - 9,1748) <= 1e-3 × 9,1748`. Un décalage de **10 %** est
refusé par la même expression. Le contrôle porte sur la valeur, pas sur l’égalité entre les deux
bras.

## Ce qui pourrait le rendre faux

- **Modèle régénéré par la porte** : la valeur dépend de la graine (1) et de la machine.
- **255 octets** : la PPL est bruitée ; la tolérance 1e-3 est serrée mais la valeur est stable.
- **Un seul modèle** : un autre modèle route peut déplacer la référence.
- **Le découpage est dense f32** : l’égalité est attendue ; un flux quantifié aurait une perte.

## Ce que ça change

A8.0 passe de **4/33** à **5/33** portes épinglées. La prochaine est `porte-budget` (PPL de deux
nœuds) ou `porte-adaptateur-sortie` (7,4242). A8.3 reste **opt-in**.

## Fichiers

- `tools/porte-reparti-moteur.sh` — référence PPL épinglée.
- `reports/a80-porte-reparti.json` — les mesures.
- `reports/rapport-a80-porte-reparti.md` — cette fiche.
