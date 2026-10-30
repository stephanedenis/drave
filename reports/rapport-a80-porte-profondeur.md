# A8.0 — `porte-profondeur-routee` épingle la PPL pleine profondeur : 14,6496

> **Ligne de roadmap** : A8.0 · **Date** : 2026-10-29 · **Verdict** : ✅ **dix-huitième porte
> épinglée** — la PPL du modèle plein (24 couches, 8192 jetons) est ancrée, et la chaîne
> hors-ligne reproduit le moteur. A8.0 reste **partielle** : 18 portes sur 33.
>
> **Dispositif** : `tools/porte-profondeur-routee.sh`, Qwen2.5-0.5B Q8_0, 8192 jetons ;
> référence **14,6496**, tolérance **5e-4** ; données [`a80-porte-profondeur.json`](a80-porte-profondeur.json).

## Ce qui est mesuré

| mesure | valeur |
|---|---:|
| PPL pleine profondeur (24 couches, moteur) | **14,6496** |
| PPL 16 couches (adaptateur entraîné) | 429 684,6614 |
| accord 16/24 | **30,93 %** (619 jetons sur 2001) |
| oracle par jeton | **51,92 %** |

La porte **exit 0** : la chaîne hors-ligne est vérifiée contre le moteur, la borne de l’oracle
est chiffrée, la cascade et le témoin sont mesurés.

## Le contrôle négatif

La condition est numérique : `abs(ppl - 14,6496) <= 5e-4 × 14,6496` sur la profondeur pleine.
Un décalage de **10 %** est refusé. La PPL 16 couches n’est **pas** épinglée : elle dépend de
l’adaptateur entraîné.

## Ce qui pourrait le rendre faux

- **Un seul modèle** ; 8192 jetons.
- **La PPL 16 couches** est un résultat d’adaptateur, pas une borne stable.
- **L’oracle par jeton** est une analyse hors-ligne, pas un routeur réel.
- **5e-4** attrape 0,05 %, pas 0,01 %.

## Ce que ça change

A8.0 passe de **17/33** à **18/33**. Les portes mesurables restantes sont surtout des rouges
structurelles (`porte-indice`, `porte-melange`) ; N3.5a est bit-exact, N3.5b (TCP) reste.

## Fichiers

- `tools/porte-profondeur-routee.sh` — PPL pleine profondeur épinglée.
- `reports/a80-porte-profondeur.json` — les mesures.
- `reports/rapport-a80-porte-profondeur.md` — cette fiche.
