# A8.0 — `porte-consolidation` épingle la PPL de base : 17,4268

> **Ligne de roadmap** : A8.0 · **Date** : 2026-10-29 · **Verdict** : ✅ **dixième porte
> épinglée** — la PPL du modèle de base et celle du LoRA aléatoire sont ancrées. A8.0 reste
> **partielle** : 10 portes sur 33.
>
> **Dispositif** : `tools/porte-consolidation.sh`, Qwen2.5-0.5B Q8_0, 256 jetons ; références
> **17,4268** (base), **17,1655** (aléatoire), rapport **0,9850**, tolérance **5e-4** ; données
> [`a80-porte-consolidation.json`](a80-porte-consolidation.json).

## Ce qui est mesuré

| mesure | valeur |
|---|---:|
| LoRA nul fusionné | **identique au bit** (531 068 480 octets) |
| PPL base | **17,4268** |
| PPL LoRA aléatoire | **17,1655** |
| rapport aléatoire / base | **0,9850** |

La porte **exit 0** : la fusion nulle est exacte, la fusion aléatoire est visible dans le moteur,
le lecteur de sortie reste hors du fichier.

## Le contrôle négatif

La condition est numérique : `abs(ppl - attendu) <= 5e-4 × attendu` sur les deux PPL. Un décalage
de **10 %** est refusé par la même expression. Le contrôle porte sur la valeur, pas sur l’égalité
des fichiers.

## Ce qui pourrait le rendre faux

- **Un seul modèle** ; 256 jetons.
- **Le rapport 0,9850** est un déplacement de PPL, pas une amélioration démontrée.
- **Le LoRA aléatoire** est un contrôle de visibilité, pas une qualité.
- **5e-4** attrape 0,05 %, pas 0,01 %.

## Ce que ça change

A8.0 passe de **9/33** à **10/33**. A8.3b est rétréci au chemin lot ; A8.3 reste opt-in. N3.2a
(service) et N3.3a (routage) sont verts ; N3.2b et la composition restent.

## Fichiers

- `tools/porte-consolidation.sh` — deux PPL épinglées.
- `reports/a80-porte-consolidation.json` — les mesures.
- `reports/rapport-a80-porte-consolidation.md` — cette fiche.
