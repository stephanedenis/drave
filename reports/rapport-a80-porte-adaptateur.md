# A8.0 — `porte-adaptateur-sortie` épingle ses PPL : 17,4315 / 2 687 292,8165

> **Ligne de roadmap** : A8.0 · **Date** : 2026-10-29 · **Verdict** : ✅ **septième porte
> épinglée** — les deux PPL de l’écriture (modèle complet et tête partielle) sont ancrées.
> A8.0 reste **partielle** : 7 portes sur 33.
>
> **Dispositif** : `tools/porte-adaptateur-sortie.sh`, Qwen2.5-0.5B Q8_0, plage 0:8, 256 jetons ;
> références **17,4315** (complet) et **2 687 292,8165** (tronqué), tolérance **5e-4** ; données
> [`a80-porte-adaptateur.json`](a80-porte-adaptateur.json).

## Ce qui est mesuré

| mesure | valeur |
|---|---:|
| PPL modèle complet | **17,4315** |
| PPL tête partielle (tronqué) | **2 687 292,8165** |
| écriture réécrite, complet | 17,4315 |
| écriture réécrite, tronqué | 2 687 292,8165 |
| demi-échelle (le drapeau agit) | 7 740 947,0594 (×2,8806) |

La porte **exit 0** : écriture fidèle, invariant d’identité, effet du drapeau, refus des trois cas
invalides.

## Le contrôle négatif

La condition est numérique : `abs(ppl - attendu) <= 5e-4 × attendu` sur les deux références. Un
décalage de **10 %** est refusé par la même expression. Le contrôle porte sur la valeur, pas sur
l’égalité entre les deux chemins.

## Ce qui pourrait le rendre faux

- **Un seul modèle** et une seule plage 0:8 ; 256 jetons.
- **Le tronqué** est une PPL de tête partielle, énorme par construction : elle n’est pas une
  qualité du modèle complet.
- **La demi-échelle** est un test d’effet, pas une mesure de qualité.
- **5e-4** attrape 0,05 %, pas 0,01 %.

## Ce que ça change

A8.0 passe de **6/33** à **7/33** portes épinglées. La prochaine est `porte-gain` (29,0206 →
1297,5437) ou `porte-topologie` déjà faite. A8.3 reste **opt-in** ; A8.3a est fait pour flux,
pont et coupe.

## Fichiers

- `tools/porte-adaptateur-sortie.sh` — deux PPL épinglées.
- `reports/a80-porte-adaptateur.json` — les mesures.
- `reports/rapport-a80-porte-adaptateur.md` — cette fiche.
