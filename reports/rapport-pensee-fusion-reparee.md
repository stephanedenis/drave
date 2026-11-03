# L — la fusion réparée : par niveau (neuronal POS/syntagmes, heuristique pragmatique) — 0,9309 / 0,8226 / 0,8784 / 0,9954, le maximum des deux

> **Ligne de roadmap** : **L** (le bloc langue) · **Date** : 2026-11-03 · **Verdict** : ✅ **la fusion ne
> dégrade plus** — la porte des quatre modes avait montré que parallèle et cascade (0,928 / 0,802 /
> 0,857) passaient **sous** le neuronal seul (0,9309 / 0,8226 / 0,8784). La cause : les deux sources
> concouraient **par confiance**. La réparation : choisir la source **par niveau** — et la fusion
> rend exactement le **maximum des deux** sur chaque niveau.

## 1. Le diagnostic

La fusion (`_supprimer_chevauchements`) triait les étiquettes par **confiance** : l'heuristique met
0,92 sur les classes fermées, le tagger neuronal 0,6 ; sur un même span, l'heuristique gagnait donc
la POS et la segmentation, **même quand elle avait tort**. Résultat mesuré (porte des quatre modes) :

| mode | POS | syntagmes | tête |
|---|---:|---:|---:|
| heuristique | 0,7394 | 0,2524 | 0,4516 |
| neuronal | **0,9309** | **0,8226** | **0,8784** |
| parallèle (ancien) | 0,9280 | 0,8020 | 0,8570 |
| cascade (ancienne) | 0,9280 | 0,8020 | 0,8570 |

La fusion était **sous** le neuronal sur ses propres niveaux : le contrat promettait le maximum, le
code rendait moins.

## 2. La réparation

`PRIORITE_NIVEAU` (dans `tools/bloc_linguistique.py`) : **le neuronal tient** `pos`, `syntagme` ;
**l'heuristique tient** `graphème`, `morphème`, `mot`, `phrase`, `pragmatique`, `discours`,
`document`. `_fusion(..., priorite_par_niveau=...)` filtre alors les étiquettes **par source et par
niveau** — les sources ne concourent plus, elles se **substituent** niveau par niveau.

- `Parallele(..., priorite_par_niveau=PRIORITE_NIVEAU)` ;
- `Cascade(..., priorite_par_niveau=PRIORITE_NIVEAU)`.

## 3. Les résultats (même gold 432, même passe)

| mode | POS | syntagmes | tête | acte | fraction |
|---|---:|---:|---:|---:|---:|
| heuristique | 0,7394 | 0,2524 | 0,4516 | **0,9954** | 0,5165 |
| neuronal | 0,9309 | 0,8226 | 0,8784 | 0,0 | 0,0 |
| parallèle (ancien) | 0,9280 | 0,8020 | 0,8570 | 0,9954 | 0,5165 |
| cascade (ancienne) | 0,9280 | 0,8020 | 0,8570 | 0,9954 | 0,5165 |
| **parallèle (par niveau)** | **0,9309** | **0,8226** | **0,8784** | **0,9954** | **0,5165** |
| **cascade (par niveau)** | **0,9309** | **0,8226** | **0,8784** | **0,9954** | **0,5165** |

**La fusion par niveau rend exactement le maximum des deux sources** : la POS, les syntagmes et la
tête du neuronal ; l'acte et la fraction de l'heuristique. C'est la promesse du contrat, tenue.

## 4. Le contrôle négatif

- **L'ancienne fusion** (mesurée dans la même passe) : 0,928 / 0,802 / 0,857 — **sous** le neuronal.
  C'est le « avant » qui prouve que la réparation change quelque chose.
- **Le repli rejeté** : une première version, quand le neuronal ne segmentait pas une phrase,
  prenait les syntagmes de l'heuristique. Mesuré : **0,9331 / 0,8069 / 0,8704** — la POS gagne
  0,0022, mais les syntagmes perdent **0,0157** (46 phrases de syntagmes heuristiques faux).
  **Rejeté** : la fusion stricte par niveau est meilleure.
- **Les seuils de la porte** : `parallele_niveau` et `cascade_niveau` **passent** ; l'ancien
  `parallele` **échoue** (0,928 < 0,9299) ; `aucun_refus` échoue (**1 refus**, `r353`).
- **Tests du contrat** : 16/16 ; **porte du bloc linguistique** : verte.

## 5. Ce qui pourrait rendre ce résultat faux

- Un seul gold (432 phrases), une seule passe API (température 0, cache versionné).
- Le choix des niveaux (`PRIORITE_NIVEAU`) est **une décision**, pas une mesure : il vient des
  mesures de la porte (le neuronal gagne POS/syntagmes/tête, l'heuristique la pragmatique).
- La fusion stricte **n'a pas de repli** : si le neuronal ne rend pas un niveau, ce niveau est vide
  (le contrat du refus). C'est assumé — le repli mesuré était pire.
- Le refus `r353` reste ouvert.

## 6. La suite de L

1. **La pragmatique neuronale** : le composite ne la rend pas (acte 0,0) ; l'heuristique la tient.
2. **Le refus `r353`** : le nommer, le traiter.
3. **Le défaut de la fusion** : `PRIORITE_NIVEAU` devrait devenir le défaut des portes, pas une
   option du banc — à décider après une passe complète.
4. La porte des quatre modes est **verte** (hors le refus) : la fiche de la porte est à rejouer.

## 7. Fichiers

- [`pensee-quatre-modes-niveau.json`](pensee-quatre-modes-niveau.json) — les six modes, les seuils.
- [`tools/bloc_linguistique.py`](../tools/bloc_linguistique.py) — `PRIORITE_NIVEAU`, `_fusion`,
  `Parallele`, `Cascade`.
- [`rapport-pensee-quatre-modes.md`](rapport-pensee-quatre-modes.md) — la porte avant réparation.
