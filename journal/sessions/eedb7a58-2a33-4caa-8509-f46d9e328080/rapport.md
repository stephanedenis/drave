# Session eedb7a58 — Tu travailles dans le dépôt

> **Journaux :** [le jour](../../2026-11-06/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `eedb7a58-2a33-4caa-8509-f46d9e328080` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-06 18:33 |
| Durée | 1.7 h |
| Tours | 1 |
| Messages | 100 |
| Appels d'outils | 114 |
| Fichiers touchés | 6 |
| Commandes | 103 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **expliciter la partition des syntagmes** (P0-3 des audits : 23/46 textes libres à chevauchement, 132 paires), sans dédupliquer en silence.  Contexte : `tools/bloc_linguistique.py` (`Heuristique.analyser`, l'union S+chunker, `Etiquette.meta`), les audits `reports/rapport-fiabilite-produit. … [1869 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **explicit … [2149 caractères tronqués]

*114 appels d'outils.* Actions notables :

- bash — Check repo state and list top-level files
- bash — List reports directory
- bash — Find audit JSON files
- bash — Check key files exist
- bash — Grep overlap mentions in first audit
- bash — Grep overlap mentions in second audit
- bash — Inspect audit JSON structure
- bash — Read dedup simulation table in audit 2
- bash — Inspect banc_50 structure in audit JSON
- bash — Locate key code sections
- bash — Read Etiquette dataclass
- bash — Read syntagm generation and union logic
- bash — Read dedup function and fusion call
- bash — Inspect banc_50 keys and samples
- … et 100 autres

**Synthèse produite :**

⏵ Assembling the machine-readable findings and the report from the pinned measurements

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/tmp/partition_syntagmes/inventaire.py` | 1 | 0 |
| `/tmp/partition_syntagmes/options.py` | 1 | 2 |
| `/tmp/partition_syntagmes/construire_patch.py` | 3 | 0 |
| `/tmp/partition_syntagmes/patch_eval.py` | 1 | 0 |
| `/tmp/partition_syntagmes/stats_finales.py` | 1 | 0 |
| `/tmp/partition_syntagmes/construire_pensee.py` | 1 | 0 |

### Commandes exécutées (échantillon)

- **T1** Check repo state and list top-level files
- **T1** List reports directory
- **T1** Find audit JSON files
- **T1** Check key files exist
- **T1** Grep overlap mentions in first audit
- **T1** Grep overlap mentions in second audit
- **T1** Inspect audit JSON structure
- **T1** Read dedup simulation table in audit 2
- **T1** Inspect banc_50 structure in audit JSON
- **T1** Locate key code sections
- **T1** Read Etiquette dataclass
- **T1** Read syntagm generation and union logic
- **T1** Read dedup function and fusion call
- **T1** Inspect banc_50 keys and samples
- **T1** Check module modification state vs HEAD
- **T1** Compare 50 texts across audits
- **T1** Inspect gold evaluation harness
- **T1** Find gold functions and attachment evaluation
- **T1** Read full gold evaluation logic incl. attachment
- **T1** Read main of gold harness
- **T1** Run gold evaluation baseline
- **T1** Read Heuristique init and analyser start
- **T1** Read analyser signature and module header
- **T1** Run overlap inventory on both audit bancs
- **T1** Get module history and extract audit commit version
- **T1** Compare gold sizes at audit commit and HEAD
- **T1** Check old gold harness compatibility
- **T1** Capture full baseline gold metrics
- **T1** Explore corpus data for free texts
- **T1** Find mentions of free texts in audits
- **T1** Read drave CLI top
- **T1** Inspect CLI output and free corpus
- **T1** Read end of Heuristique.analyser
- **T1** Check semantic units construction
- **T1** Run measured options over gold, bancs, free texts
- **T1** Compare tp/fp/fn base vs eval baseline
- **T1** Run direct eval_bloc twice to check determinism
- **T1** Inspect Cascade/Parallele init for shared state
- **T1** Look for global caches or subprocesses in module
- **T1** Read S generator entry points
- … et 63 autres

## 4. Mesures et résultats marquants

- **T1** `149:syntagme (51,9 %)** sont impliquées, dans **31/50 textes** ; 113 sont des **inclusions**, 19 des`
- **T1** `258:| `valeur` | **surface** pour graphème/mot/pos/syntagme (100 %) ; **normalisée** pour morphème (126/134) ; **tronquée à 60** pour document (42/53) ; **catégorielle** pour phrase/pragmatique/discou`
- **T1** `| **P2-16** | Couvrir les caractères de contrôle dans graphème | x46 : **7 newlines** non couverts, 95,14 % ; 49/50 à 100 % | 1020-1031 | **15 min** |`
- **T1** `diff idx 14 '' || 'Les prix ont augmenté de 12,5 % entre janvier et mars 2024, soit 3 points de plus que prévu.'`
- **T1** `diff idx 33 "Bien que fatigué, il continue à travailler jusqu'à minuit." || 'The prices rose by 12.5% between January and March 2024, three points more than expected.'`
- **T1** `2ba393b0 B13 — LA POS À 83,83 % (R2a/R3/R2b) : F1 0,5849 → 0,6181, ANGLAIS 0,6341 → 0,7273, ATTACHEMENT INCHANGÉ (222/222) ; 183/183`
- **T1** `f"· unités sémantiques={len(a.unites_semantiques)} ({a.fraction_semantique:.1%} du texte)"`
- **T1** `preference {'groupes': 244, 'rang1_gold': 177, 'un_gold': 207, 'groupes_sans_gold': 37}`
- **T1** `GP  [29:51] 'du jardin chaque matin' -> partir   [groupe 0 rang 4/4] | alt croise GV 61:67 | alt inclus GP 29:60 | alt croise GP 58:67`
- **T1** `GP  [29:60] 'du jardin chaque matin avant de' -> fleurs   [groupe 0 rang 2/4] | alt croise GV 61:67 | alt croise GP 58:67 | alt inclut GP 29:51`
- **T1** `GP  [58:67] 'de partir' -> au   [groupe 0 rang 3/4] | alt inclut GV 61:67 | alt croise GP 29:60 | alt croise GP 29:51`
- **T1** `GV  [61:67] 'partir' -> —   [groupe 0 rang 1/4] | alt croise GP 29:60 | alt inclus GP 58:67 | alt croise GP 29:51`
- **T1** `GP  [68:78] 'au travail' -> partir   [groupe 1 rang 2/2] | alt meme_span GV 68:78`
- **T1** `GV  [68:78] 'au travail' -> —   [groupe 1 rang 1/2] | alt meme_span GP 68:78`
- **T1** `GV  [80:96] 'puis elle rentre' -> travail   [groupe 2 rang 2/2] | alt inclut GV 90:96`
- **T1** `GV  [90:96] 'rentre' -> —   [groupe 2 rang 1/2] | alt inclus GV 80:96`
- **T1** `GP  [97:117] 'vers dix-huit heures' -> rentre   [groupe 3 rang 4/5] | alt inclus GP 97:159 | alt croise GV 121:128 | alt croise GN 129:137 | alt croise GP 138:159`
- **T1** `GP  [97:159] 'vers dix-huit heures et prépare le dîner pour ses deux enfants' -> rentre   [groupe 3 rang 1/5] | alt inclut GV 121:128 | alt inclut GN 129:137 | alt inclut GP 97:117 | alt inclut GP 138`
- **T1** `GV  [121:128] 'prépare' -> heures   [groupe 3 rang 2/5] | alt inclus GP 97:159 | alt croise GN 129:137 | alt croise GP 97:117 | alt croise GP 138:159`
- **T1** `GN  [129:137] 'le dîner' -> heures   [groupe 3 rang 3/5] | alt inclus GP 97:159 | alt croise GV 121:128 | alt croise GP 97:117 | alt croise GP 138:159`
- **T1** `GP  [138:159] 'pour ses deux enfants' -> prépare   [groupe 3 rang 5/5] | alt inclus GP 97:159 | alt croise GV 121:128 | alt croise GN 129:137 | alt croise GP 97:117`
- **T1** `GV  [61:67] 'partir' -> —   [groupe 0 rang 1/4] | alt croise GP 29:60 RETIRÉ | alt inclus GP 58:67 RETIRÉ | alt croise GP 29:51 RETIRÉ`
- **T1** `GV  [68:78] 'au travail' -> —   [groupe 1 rang 1/2] | alt meme_span GP 68:78 RETIRÉ`
- **T1** `GV  [90:96] 'rentre' -> —   [groupe 2 rang 1/2] | alt inclus GV 80:96 RETIRÉ`
- **T1** `GP  [97:159] 'vers dix-huit heures et prépare le dîner pour ses deux enfants' -> rentre   [groupe 3 rang 1/5] | alt inclut GV 121:128 RETIRÉ | alt inclut GN 129:137 RETIRÉ | alt inclut GP 97:117 RETIR`
- **T1** `GP  [29:60] 'du jardin chaque matin avant de' -> fleurs   [groupe 0 rang 2/4] | alt croise GV 61:67 | alt croise GP 58:67 RETIRÉ | alt inclut GP 29:51 RETIRÉ`
- **T1** `GV  [61:67] 'partir' -> —   [groupe 0 rang 1/4] | alt croise GP 29:60 | alt inclus GP 58:67 RETIRÉ | alt croise GP 29:51 RETIRÉ`
- **T1** `union_court {'n': 207, 'gold': 0, 'rang1': 177, 'au_moins_un_gold_dans_gardes': 181}`
- **T1** `union_long {'n': 207, 'gold': 0, 'rang1': 179, 'au_moins_un_gold_dans_gardes': 181}`
- **T1** `union_att {'n': 207, 'gold': 0, 'rang1': 178, 'au_moins_un_gold_dans_gardes': 181}`
- **T1** `court {'n': 207, 'gold': 0, 'rang1': 169, 'au_moins_un_gold_dans_gardes': 181}`
- **T1** `long {'n': 207, 'gold': 0, 'rang1': 19, 'au_moins_un_gold_dans_gardes': 181}`
- **T1** `att_court {'n': 207, 'gold': 0, 'rang1': 137, 'au_moins_un_gold_dans_gardes': 181}`
- **T1** `preference {'groupes': 244, 'rang1_gold': 179, 'un_gold': 207, 'groupes_sans_gold': 37}`
- **T1** `pref {'groupes': 244, 'rang1_gold': 179, 'un_gold': 207, 'groupes_sans_gold': 37}`
- **T1** `GP  [29:51] 'du jardin chaque matin' -> partir   [groupe 0 rang 3/4] | alt inclus GP 29:60 | alt croise GV 61:67 | alt croise GP 58:67`
- **T1** `GP  [29:60] 'du jardin chaque matin avant de' -> fleurs   [groupe 0 rang 1/4] | alt croise GV 61:67 | alt inclut GP 29:51 | alt croise GP 58:67`
- **T1** `GP  [58:67] 'de partir' -> au   [groupe 0 rang 4/4] | alt croise GP 29:60 | alt inclut GV 61:67 | alt croise GP 29:51`
- **T1** `GV  [61:67] 'partir' -> —   [groupe 0 rang 2/4] | alt croise GP 29:60 | alt croise GP 29:51 | alt inclus GP 58:67`
- **T1** `+    chunker le plus large **est** ce span (86,5 %) ; le S le plus large ne l'est que 25 fois.`
- **T1** `verdict Les 239 paires des deux bancs sont **toutes** des paires S × chunker : 53,1 % de S qui contient le chunker, 33,5 % l'inverse, 2,5 % de mêmes bornes, 10,9 % de croisements. L'alternative étique`

## 5. Erreurs rencontrées

1 sorties en erreur ou divergentes. Les premières :

- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 47, in <module> KeyError: 'alternative' [exit code: 1]

