# A8.0 — `porte-reflexe` épingle la PPL du chemin tronqué : 11 163 272,0495

> **Ligne de roadmap** : A8.0 · **Date** : 2026-10-29 · **Verdict** : ✅ **treizième porte
> épinglée** — la PPL du chemin tronqué à 8 couches avec adaptateur nul est ancrée, et
> l’invariant d’identité tient. A8.0 reste **partielle** : 13 portes sur 33.
>
> **Dispositif** : `tools/porte-reflexe.sh`, Qwen2.5-0.5B Q8_0, 8 couches, 512 jetons,
> adaptateur d’identité ; référence **11 163 272,0495**, tolérance **5e-4** ; données
> [`a80-porte-reflexe.json`](a80-porte-reflexe.json).

## Ce qui est mesuré

| mesure | valeur |
|---|---:|
| PPL tronquée 8 couches, adaptateur nul | **11 163 272,0495** |
| adaptateur nul contre référence | **identique** |
| accord à 16 couches | **25,4 %** (référence 4,8 %) |
| cos(état 16 couches, état final) | **0,145** |

La porte **exit 0** : le moteur refuse l’adaptateur sans tête partielle, l’adaptateur nul ne
change rien, l’accord est mesuré avant/après.

## Le contrôle négatif

La condition est numérique : `abs(ppl - 11 163 272,0495) <= 5e-4 × 11 163 272,0495`. Un décalage
de **10 %** est refusé. Le contrôle porte sur la valeur, pas sur l’égalité des deux chemins.

## Ce qui pourrait le rendre faux

- **PPL d’un chemin tronqué**, pas une qualité du modèle complet.
- **Adaptateur nul** : la valeur est une borne de plomberie, pas un résultat d’entraînement.
- **512 jetons** ; une seule profondeur (8).
- **5e-4** attrape 0,05 %, pas 0,01 %.

## Ce que ça change

A8.0 passe de **12/33** à **13/33**. N3.2a/b0/b1/b2, N3.3a/b/c, N3.4a/b sont verts ; le
placement (N3.4c) et la composition complète restent.

## Fichiers

- `tools/porte-reflexe.sh` — PPL tronquée épinglée.
- `reports/a80-porte-reflexe.json` — les mesures.
- `reports/rapport-a80-porte-reflexe.md` — cette fiche.
