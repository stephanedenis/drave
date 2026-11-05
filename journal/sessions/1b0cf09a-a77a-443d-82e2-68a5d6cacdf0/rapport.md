# Session 1b0cf09a — Tu travailles dans le dépôt

> **Journaux :** [le jour](../../2026-11-05/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `1b0cf09a-a77a-443d-82e2-68a5d6cacdf0` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-05 14:22 |
| Durée | 0.3 h |
| Tours | 1 |
| Messages | 46 |
| Appels d'outils | 49 |
| Fichiers touchés | 1 |
| Commandes | 40 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **valider le cache du chunker** proposé par la fiche `reports/rapport-cout-chunker.md` (O(n²) confirmé, cache ×11,6 à 160 tokens) — sans modifier le code du dépôt.  Contexte : `tools/bloc_linguistique.py`, classe `Heuristique` : `analyser` appelle `self._syntagmes_simple(texte, lg)` à l'in … [1794 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **valider  … [2074 caractères tronqués]

*49 appels d'outils.* Actions notables :

- bash — Check repo status and branch
- bash — List reports and file sizes
- read
- bash — Hash and diff of the linguistic block
- bash — Locate key functions in the source
- bash — Read top of linguistic block
- bash — Read rest of analyser and next classes
- bash — Read Heuristique class init
- bash — Inspect gold evaluation corpus loader
- bash — Load 612-sentence corpus and stats
- bash — Inspect pensee JSON schema
- bash — Top-level structure of pensee file
- bash — Inspect key sections of pensee JSON
- bash — Inspect default-path long points
- … et 30 autres

**Synthèse produite :**

⏵ Résultats principaux obtenus : je vérifie le contrôle OFF et je prépare le patch réel

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/tmp/bench_cache_chunker.py` | 1 | 0 |

### Commandes exécutées (échantillon)

- **T1** Check repo status and branch
- **T1** List reports and file sizes
- **T1** Hash and diff of the linguistic block
- **T1** Locate key functions in the source
- **T1** Read top of linguistic block
- **T1** Read rest of analyser and next classes
- **T1** Read Heuristique class init
- **T1** Inspect gold evaluation corpus loader
- **T1** Load 612-sentence corpus and stats
- **T1** Inspect pensee JSON schema
- **T1** Top-level structure of pensee file
- **T1** Inspect key sections of pensee JSON
- **T1** Inspect default-path long points
- **T1** Environment and CPU information
- **T1** Read gold evaluation attachment logic
- **T1** Smoke-test cache equality on 30 sentences
- **T1** Re-check current source around analyser
- **T1** Inspect concurrent modification and HEAD snapshot hash
- **T1** Check RACINE usage and generator path deps
- **T1** Read remainder of concurrent patch
- **T1** Freeze HEAD snapshot of the block
- **T1** Check new commit and file state
- **T1** Switch bench to frozen HEAD snapshot
- **T1** Smoke-test equality against frozen snapshot
- **T1** Run full cache validation benchmark
- **T1** Check target files do not exist
- **T1** Read existing fiche limits for context
- **T1** Check benchmark progress and load
- **T1** Read benchmark summary output
- **T1** Inspect long-text and complexity results
- **T1** Generate and inspect exact patch on /tmp copy
- **T1** Locate duplicate return statement
- **T1** Inspect all GV verb calls
- **T1** Fix patch anchor and regenerate diff
- **T1** Write OFF re-measure and real patch benchmark
- **T1** Fix fabric and equality loop bugs
- **T1** Run OFF re-measure and real patch benchmark
- **T1** Read patch benchmark error
- **T1** Fix lambda keyword and rerun patch benchmark
- **T1** Generate markdown tables from benchmark JSON

## 4. Mesures et résultats marquants

- **T1** `"V1": "_syntagmes_simple m\u00e9mo\u00efs\u00e9 par (texte, langue) dans une sous-classe locale",`
- **T1** `"textes_longs_20_320": "V1, V2 et OFF identiques à l’original sur les 5 longueurs × 2 chemins"`
- **T1** `"Base synthétique A (« est sur le toit ») : le GV a pour tête l'auxiliaire « est » ; _cible_proche le saute et scanne tous les GV. C'est un cas défavorable réel (copules), mais il amplifie le coût. Av`
- **T1** `"Corpus court : 6,13 tokens _mots/phrase, 1,10 segment, 0,19 GV. Le gain corpus est faible (×1,18-1,22 chunker, ×0,97-1,07 défaut) ; le O(n²) ne mord pas sur le gold actuel.",`
- **T1** `"Bruit de mesure : Xeon partagé, temps CPU, 3-11 passes ; l'OFF varie de ×0,90 à ×1,13 selon le point (médiane ×1,00). Les facteurs à ±10 % près.",`
- **T1** `| original | 245.3 | ×1.000 | 400.8 | 395.2 | ×1.000 | 645.8 |`
- **T1** `| C1 | 198.0 | ×1.239 | 323.6 | 388.3 | ×1.018 | 634.5 |`
- **T1** `| C2 | 196.1 | ×1.251 | 320.4 | 385.1 | ×1.026 | 629.2 |`
- **T1** `| OFF | 275.6 | ×0.890 | 450.4 | 398.4 | ×0.992 | 650.9 |`
- **T1** `| 20 | 6 | 2 | 1.64 | 0.88 | 0.71 | 1.67 | ×1.88 | ×2.32 | ×0.98 |`
- **T1** `| 40 | 12 | 4 | 4.97 | 2.38 | 1.40 | 4.99 | ×2.09 | ×3.55 | ×1.00 |`
- **T1** `| 80 | 24 | 8 | 16.19 | 4.26 | 2.50 | 16.44 | ×3.80 | ×6.46 | ×0.99 |`
- **T1** `| 160 | 48 | 16 | 57.74 | 11.27 | 5.25 | 62.02 | ×5.12 | ×11.00 | ×0.93 |`
- **T1** `| 320 | 96 | 32 | 233.47 | 33.80 | 12.00 | 241.33 | ×6.91 | ×19.46 | ×0.97 |`
- **T1** `| 640 | 192 | 64 | 925.09 | 119.60 | 31.70 | 919.54 | ×7.74 | ×29.18 | ×1.01 |`
- **T1** `| 1280 | 384 | 128 | 3740.44 | 426.46 | 100.93 | 3657.45 | ×8.77 | ×37.06 | ×1.02 |`
- **T1** `| 20 | 6 | 2 | 2.02 | 1.95 | 1.60 | 2.03 | ×1.03 | ×1.26 | ×0.99 |`
- **T1** `| 40 | 12 | 4 | 4.04 | 3.90 | 2.92 | 4.10 | ×1.04 | ×1.39 | ×0.99 |`
- **T1** `| 80 | 24 | 8 | 14.88 | 12.54 | 6.03 | 14.09 | ×1.19 | ×2.47 | ×1.06 |`
- **T1** `| 160 | 48 | 16 | 27.88 | 27.27 | 13.55 | 30.76 | ×1.02 | ×2.06 | ×0.91 |`
- **T1** `| 320 | 96 | 32 | 91.33 | 89.07 | 35.04 | 90.22 | ×1.03 | ×2.61 | ×1.01 |`
- **T1** `| 640 | 192 | 64 | 344.96 | 321.58 | 103.40 | 317.65 | ×1.07 | ×3.34 | ×1.09 |`
- **T1** `| 1280 | 384 | 128 | 1161.80 | 1164.81 | 318.29 | 1188.64 | ×1.00 | ×3.65 | ×0.98 |`

## 5. Erreurs rencontrées

2 sorties en erreur ou divergentes. Les premières :

- **T1** : False C1 egal True n_etq 18 [stderr] Traceback (most recent call last):   File "<stdin>", line 9, in <module>   File "/tmp/bench_cache_chunker.py", line 84, in analyser     return super().analyser(tex
- **T1** : diff exit=1 [stderr] Traceback (most recent call last):   File "/tmp/appliquer_correctif.py", line 93, in <module>     rem('return Heuristique._verbe_dans(texte, g["debut"], g["fin"], verbes)',     ~~

