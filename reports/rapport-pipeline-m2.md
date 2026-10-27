# B14 — M2 dans la chaîne : un rameau, pas un étage

> **Objet.** Brancher M2 (`voies.py`) dans la chaîne B13 et mesurer s'il **ajoute** quelque chose.
> Résultat : **non**. M1 lit **100 %** des 146 items `de`/`vers` ; M2 lit **93,4 / 93,6 %** ; et
> aucun étage ne consomme M2. C'est un **rameau neural parallèle**, pas un étage du pipeline.

## Mesures (3 graines, 300 pas)

| lecture | `de` | `vers` |
|---|---:|---:|
| M1 avec contexte | **100 %** | **100 %** |
| M1 sans contexte | 94,5 % | 94,5 % |
| M2 avec contexte | **93,4 %** | **93,6 %** |
| M2 sans contexte | 93,6 % | 93,6 % |
| M2 écart vs M1 | **−6,6 pts** | **−6,4 pts** |

- M2 **vu** : 126/126 ; **inédit couvert** : 79,5 % (`de`), 82,1 % (`vers`) ; **nouvelle classe** 0/7.
- **M2 ne bat pas M1** ; l'ajouter **dégrade** le champ dorsal.
- **Aucun étage ne consomme M2** : M5 consomme le code M1 ; M6 ne lit pas le champ dorsal.

## M5 et M6 dans la chaîne

| étage | mesure |
|---|---:|
| M5 `source` avec plateau | **18,70 %** (majoritaire 6,49 %) ; surprise **2,423** |
| M5 `source` sans plateau | **12,60 %** ; surprise **3,112** |
| M5 `source` sans transitions | 14,29 % |
| M5 `source` M1 sans contexte | 28,03 % (n=396) — **artefact de couverture** |
| M6 confluence | **94,32 %** |
| M6 commutation | **94,95 %** |
| M6 commutation coût | **0,000** |

### Correction M5 : le 28,03 % est une perte de couverture

Le « M1 sans contexte » de M5 ne lit que **396 pas sur 770** (couverture **51,4 %**) : seuls les
pas de **dames** survivent ; les **374 pas d'échecs** sont perdus. Sur **ces mêmes 396 pas**, la
référence fait exactement **28,03 %** : ce n'est pas un gain, c'est une **sélection**. Pour
`cible`, le brut 13,10 % a une couverture de **74,5 %** ; `go` tombe à **0 %** avec une surprise
de **18,21 nat**. Le chiffre honnête est donc **M5 sans contexte = 12,60 % sur 770**, pas 28,03 %.

## M9

| privation | effet |
|---|---:|
| M1 sans contexte | **70,83 %** (déficit 29,17) |
| M2 lésion dorsale `de` | **2,05 %** (déficit 91,32) |
| M2 lésion dorsale `vers` | **2,74 %** (déficit 90,87) |
| M2 lésion ventrale | **0,0** de déficit |
| M5 sans plateau | **−6,10 pts** d'exact, **−0,688 nat** |
| M5 sans transitions | **−4,42 pts** d'exact |

## Verdict

**M2 n'ajoute rien à la chaîne** : M1 est plus exact et M2 n'est consommé par personne. Il ne
pourrait servir que de **secours** sur des surfaces que le codec ne lit pas — cas absent de ce
corpus et **non mesuré** ici. Ce n'est pas un échec de M2 comme décodeur isolé ; c'est un échec
d'**intégration**.

## Fichiers

- Code : [`tools/cerveau/pipeline_semantique_m2.py`](../tools/cerveau/pipeline_semantique_m2.py).
- Test : [`tools/cerveau/tests/test_pipeline_semantique_m2.py`](../tools/cerveau/tests/test_pipeline_semantique_m2.py).
- JSON : [`pipeline-m2.json`](pipeline-m2.json).
