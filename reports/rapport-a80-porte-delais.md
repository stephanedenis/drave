# A8.0 — `porte-delais` épingle la PPL : 59,0790 à 0 et 50 ms

> **Ligne de roadmap** : A8.0 · **Date** : 2026-10-29 · **Verdict** : ✅ **seizième porte
> épinglée** — le délai ne change aucun chiffre, seul le temps change. A8.0 reste **partielle** :
> 16 portes sur 33.
>
> **Dispositif** : `tools/porte-delais.sh`, Qwen2.5-0.5B Q8_0, 64 pas, topologie 0–11/12–23 ;
> référence **59,0790**, tolérance **5e-4** ; données [`a80-porte-delais.json`](a80-porte-delais.json).

## Ce qui est mesuré

| mesure | valeur |
|---|---:|
| PPL délai 0 ms | **59,0790** |
| PPL délai 50 ms | **59,0790** |
| empreintes | **identiques** |
| temps mural | 7,24 s → 10,43 s (+3,2 s ≈ 50 ms × 64 pas) |

La porte **exit 0** : le délai ne modifie aucun chiffre, le temps augmente.

## Le contrôle négatif

La condition est numérique : `abs(ppl - 59,0790) <= 5e-4 × 59,0790` sur les deux délais. Un
décalage de **10 %** est refusé. Le contrôle porte sur la valeur, pas sur la durée.

## Ce qui pourrait le rendre faux

- **Un seul modèle** ; 64 pas.
- **Le temps dépend de la machine** : la porte l’affiche, elle ne l’épingle pas.
- **La PPL dépend de la limite** ; 59,0790 est lié à ce montage.
- **5e-4** attrape 0,05 %, pas 0,01 %.

## Ce que ça change

A8.0 passe de **15/33** à **16/33**. La prochaine est `porte-bus-socket` ; A8.3b/c et N3 suivent.

## Fichiers

- `tools/porte-delais.sh` — PPL épinglée.
- `reports/a80-porte-delais.json` — les mesures.
- `reports/rapport-a80-porte-delais.md` — cette fiche.
