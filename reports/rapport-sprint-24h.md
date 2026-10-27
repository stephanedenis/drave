# Sprint 24 h — bilan B12 → B18

> **Cible** : 2026-10-28 09:39 HAE. **Objet** : poursuivre les suites naturelles de M1–M9 avec
> des sous-agents, corriger les scores gonflés, mesurer ce qui tient. **Ce bilan est daté du
> 2026-10-27 13:10** ; il ne remplace pas les fiches par chantier.

## Ce qui a été fait

- **A1–A11** : M5/M6 (A1, A6), M7/M8/M9 (A2, A7, A11), M2 (A3, A5, A9), M3/M4 (A4), multilingue (A10).
- **B13** : chaîne M1→M5→M6→M8, **528/528**, M5 contexte **18,70 % vs 12,60 %**, M6 **94,3 %**.
- **B14** : M2 dans la chaîne → **n'ajoute rien** (M1 100 %, M2 93,4/93,6 %, aucun étage ne le consomme).
- **B15** : M1 sur **66 langues**, **528/528**, invariance **26/26** et **15/15** avec contexte, contrôle permuté **0/90 %**.
- **B16** : M7-bis LFU **+23,1 pts** répétés, **+4,25** suffixe, LFU+récence **= LFU** ; c'est la fréquence, pas la neuromodulation.
- **B17** : LFU dans la chaîne **9,28 %** suffixe surface vs FIFO **5,03 %** ; M8 couverture **70,75 %**, lookup 100 %, généralisation **0**.
- **B18** : restitution canonique **528/528** rendus et relus, **0 échec** ; codec, pas décodeur.

## Ce qui tient

| module | statut | chiffre |
|---|---|---|
| **M1** | ✅ **solide** | 528/528, 70,8 % sans contexte, canonique 100 % |
| **M2** | ⚠️ **vu + règles** | 93,6 % (vu 126/126, inédit 10,7/20) ; aug-formes 13/20 ; aucune variante ne domine |
| **M3** | ❌ **tautologique** | span 12/12 même avec des codes aléatoires |
| **M4** | ❌ **lookup** | 29 codes, 0/6 non stockés, 0/10 complétions exactes |
| **M5** | ⚠️ **contexte** | sans contexte 12,60 % ; avec plateau **18,70 %**, surprise 2,423 vs 3,112 |
| **M6** | ⚠️ **sélecteur** | 94,3 % (base 75 %), commutation 0 |
| **M7** | ⚠️ **fréquence** | LFU +23,1 pts répétés, +4,25 suffixe ; LFU+récence = LFU |
| **M8** | ❌ **marginal** | 96,48 % champs, exact 65,1 %, baseline par jeu 96,10 %, LOO 0 |
| **M9** | ✅ **réel** | `de` 91,8→2,05, déficit 89,7 ; action triviale |

## Ce qui ne tient pas

- **M2** n'est pas un étage de la chaîne : M1 le dépasse et aucun étage ne le consomme.
- **M3/M4/M8** sont structurels : tampon exact, table de hachage, marginale.
- **M5** sans contexte est négatif ; le gain vient du **plateau**, pas du code.
- **M6** est un sélecteur de canal, pas un contrôle exécutif.
- **M7** : la fréquence est le levier, pas la neuromodulation ; LFU+récence ne départage jamais.
- **B10** : le décodeur neuronal reste négatif (chrF 14,0/5,4 contre plancher 38,8).

## Portes et tests

- Tests cerveau : **126 OK** (19 skips sans torch), `test_voies` 8/8 avec torch.
- Revue de documentation : **verte** (180 fiches, 248 JSON, 53 docs).
- `porte-tableaux` : **verte**.
- Dernière passe complète : **47 vertes, 2 rouges structurelles** (`porte-indice`, `porte-melange`) ;
  une nouvelle passe est en cours au moment de ce bilan.

## Fichiers

- Fiches : [`rapport-cerveau-corrections.md`](rapport-cerveau-corrections.md),
  [`rapport-pipeline-semantique.md`](rapport-pipeline-semantique.md),
  [`rapport-pipeline-m2.md`](rapport-pipeline-m2.md),
  [`rapport-multilingue.md`](rapport-multilingue.md),
  [`rapport-m7-frequence.md`](rapport-m7-frequence.md),
  [`rapport-pipeline-memoire.md`](rapport-pipeline-memoire.md),
  [`rapport-restitution.md`](rapport-restitution.md).
- JSON : `cerveau-mesures-corrigees.json`, `pipeline-semantique.json`, `pipeline-m2.json`,
  `multilingue.json`, `m7-frequence.json`, `pipeline-memoire.json`, `restitution.json`.
- Code : `tools/cerveau/`.
