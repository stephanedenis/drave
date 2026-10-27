# B21 — M9 par dose : M3 tautologique, M5 +4,25 pts, sham nul

> **Objet.** Compléter M9 par des **doses** (capacité M3, ordre M5), un **sham** et une
> **double lésion**. Résultat : M3 est **linéaire et tautologique**, M5 gagne **4,25 pts** de l'ordre 1
> à l'ordre 2, le sham est **nul**, la double lésion **n'ajoute pas**.

## M3 — capacité 0/4/8/12/16

| capacité | span | exact | essais |
|---:|---:|---:|---:|
| 0 | **0** | 0,0 % | 0 |
| 4 | **4** | 100 % | 3 200 |
| 8 | **8** | 100 % | 6 266 |
| 12 | **12** | 100 % | 8 733 |
| 16 | **12** | 100 % | 8 733 |

Le span est **exactement** `min(longueur, capacité)` : ce n'est pas une courbe de mémoire, c'est
la définition du tampon. Le plateau à 12 est la longueur des séquences.

## M5 — ordre 0/1/2 (`source`, 847 pas)

| ordre | exact | majoritaire | surprise | gain surprise |
|---:|---:|---:|---:|---:|
| 0 | 13,81 % | 6,02 % | 2,472 | +1,080 |
| 1 | 15,70 % | 6,02 % | 2,444 | +1,108 |
| 2 | **18,06 %** | 6,02 % | **2,432** | **+1,119** |

**+4,25 pts** de l'ordre 1 à l'ordre 2, **+0,012 nat** de surprise : le gain est réel mais petit.
Il vient de la structure de partie (alternance, prises), pas d'une compréhension du plateau.

## Sham et double lésion

| condition | M3 | M5 |
|---|---:|---:|
| intacte | span 12, exact 1,0 | 15,70 % |
| **sham** (copie sans effet) | span 12, exact 1,0 | **15,70 %** |
| **double** M3 capacité 0 + M5 ordre 0 | span 0 | **13,81 %** |

Le sham est **exactement** l'intact : l'instrument ne fabrique pas d'effet. La double lésion ne
compose pas : M5 ordre 0 reste à 13,81 %, M3 tombe à 0.

## Verdict

- **M3** : dose **linéaire** et **tautologique** ; aucun seuil, aucune mémoire graduée.
- **M5** : ordre 2 **+4,25 pts** ; gain **mécanique**.
- **M9** : la table de privations est **cohérente** ; elle ne prouve pas une fonction biologique.
- **Sham** : nul ; l'instrument est fiable.

## Fichiers

- Code : [`tools/cerveau/lesion_complet.py`](../tools/cerveau/lesion_complet.py).
- Test : [`tools/cerveau/tests/test_lesion_complet.py`](../tools/cerveau/tests/test_lesion_complet.py).
- JSON : [`m9-dose.json`](m9-dose.json).
