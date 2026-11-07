# Session 77d26bc7 — Tu travailles dans /home/stephane/Data13

> **Journaux :** [le jour](../../2026-11-07/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `77d26bc7-1657-4c96-83c9-bba7c25dd828` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-07 00:49 |
| Durée | 1.4 h |
| Tours | 1 |
| Messages | 66 |
| Appels d'outils | 94 |
| Fichiers touchés | 6 |
| Commandes | 86 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **re-auditer le produit sur les textes libres** avec le code de la nuit (23 h 30 → 00 h 50), en lecture seule.  Contexte : `tools/drave.py` (CLI : `analyser`, `--fichier`, `--jsonl`, `--partition`), `tools/bloc_linguistique.py`. Les audits précédents : `reports/rapport-fiabilite-produit.md` (50 tex … [1811 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **re-auditer le pro … [2091 caractères tronqués]

*94 appels d'outils.* Actions notables :

- bash — Vérifier branche et état du dépôt
- bash — Vérifier existence des fichiers clés
- read
- bash — Inspecter la structure des JSON d'audit
- bash — Inspecter banc_50.resultats
- bash — Lire le rapport de fiabilité existant
- bash — Suite du rapport fiabilité
- bash — Voir les commits de la nuit
- bash — Repérer contrat et frontières dans le module
- bash — Lire contrat et robustesse du JSON
- bash — Lire la logique de frontières de phrase
- bash — Lire le découpage de phrases actuel
- bash — Lire le dispositif des 40 frontières
- bash — Tester la CLI actuelle
- … et 79 autres

**Synthèse produite :**

⏵ Construction du harnais de rejeu dans /tmp (lecture seule du dépôt)

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/tmp/reaudit/explorer.py` | 1 | 0 |
| `/tmp/reaudit/commun.py` | 1 | 0 |
| `/tmp/reaudit/run50.py` | 1 | 0 |
| `/tmp/reaudit/run40.py` | 1 | 0 |
| `/tmp/reaudit/run20.py` | 1 | 0 |
| `/tmp/reaudit/run_probes.py` | 1 | 0 |

### Commandes exécutées (échantillon)

- **T1** Vérifier branche et état du dépôt
- **T1** Vérifier existence des fichiers clés
- **T1** Inspecter la structure des JSON d'audit
- **T1** Inspecter banc_50.resultats
- **T1** Lire le rapport de fiabilité existant
- **T1** Suite du rapport fiabilité
- **T1** Voir les commits de la nuit
- **T1** Repérer contrat et frontières dans le module
- **T1** Lire contrat et robustesse du JSON
- **T1** Lire la logique de frontières de phrase
- **T1** Lire le découpage de phrases actuel
- **T1** Lire le dispositif des 40 frontières
- **T1** Tester la CLI actuelle
- **T1** Lister les 50 textes du banc
- **T1** Inspecter le corpus 40 et ses règles
- **T1** Lire définitions du rapport frontières
- **T1** Lire la logique d'actes pragmatiques
- **T1** Tester frontières et actes sur cas connus
- **T1** Lire le pipeline d'analyse
- **T1** Lister les 40 textes et effets
- **T1** Lire la définition des actes faux
- **T1** Chercher actes dans le rapport
- **T1** Chercher le chiffre 34/50 dans le rapport
- **T1** Rejouer les 40 frontières avec le code actuel
- **T1** Rejouer les 40 frontières corrigé
- **T1** Vérifier environnement et séparateur --
- **T1** Vérifier espaces de tête
- **T1** Chercher une définition d'anomalie dans le JSON
- **T1** Chercher 34/50 dans les rapports
- **T1** Lire le rapport produit-bloc-l (34/50)
- **T1** État des fichiers et contrat documenté
- **T1** Comparer les deux bancs de 50 textes
- **T1** Lire le contrat publié
- **T1** Chercher les usages du schéma
- **T1** Lire le schéma v1 publié
- **T1** Lire le vérificateur et le test du schéma
- **T1** Confirmer les chiffres courants du produit
- **T1** Vérifier disponibilité et lancer le validateur
- **T1** Préciser F1 et vérifier les hash HEAD
- **T1** Comprendre les étiquettes document
- … et 46 autres

## 4. Mesures et résultats marquants

- **T1** `| temps CLI (50 phrases) | **136,8–226,6 ms**, médiane **152,7 ms** |`
- **T1** `| temps interne (API) | **0,2–45,1 ms**, médiane **1,0 ms** |`
- **T1** `langue=und script=Latn source=heuristique · 13 étiquettes · unités sémantiques=2 (85.7% du texte)`
- **T1** `Le **démarrage** (`--version`, 10 passages) coûte **134–192 ms**, médiane **146 ms**. Pour une`
- **T1** `phrase courte, **plus de 95 % du temps CLI est le démarrage**, pas l'analyse (0,8 ms pour f01).`
- **T1** ``evaluer` coûte **530–543 ms** sur le gold vivant et **577–600 ms** avec `--gold` ; `rejouer``
- **T1** `**146–149 ms**. Les cinq textes les plus lents en CLI`
- **T1** `sont f50 (226,6 ms), f02 (193,8), f05 (181,6), f35 (180,3), f44 (179,1) — l'ordre est surtout`
- **T1** `du bruit de démarrage, sauf f50. En interne, les plus lents sont f50 (45,1 ms), f43 (7,9),`
- **T1** `Le coût est **superlinéaire** (×16,4 de temps pour ×5 de texte entre 10 k et 50 k) ; à 10 000`
- **T1** `caractères, le CLI reste sous la seconde, mais le JSON fait **2,76 Mo** (indenté). Un document`
- **T1** `de 50 000 caractères coûte **5,4 s** et **11,5 Mo** : il n'y a ni plafond ni mode compact.`
- **T1** `| 10 000 car., phrases répétées | 0 | **590–765 ms** | 10 362 | **2 763 666 o** | spans valides, déterminisme |`
- **T1** `| 10 000 car., `a` × 10 000 | 0 | **172 ms** | 7 | 42 482 o | un seul token |`
- **T1** `| 10 000 car., ponctuation | 1 | **155 ms** | — | 0 | refus `vide` (raison fausse) |`
- **T1** `| mode lisible, `a` × 10 000 | 0 | 153 ms | — | 10 457 o | **ligne de 10 010 caractères** |`
- **T1** `10. **Taille et lot** : 2,76 Mo pour 10 000 caractères, 11,5 Mo pour 50 000 ; une invocation =`
- **T1** `26c7b7ab 07 00:16 ROADMAP ET JOURNAL — LA NUIT FINIT À F1 0,7535, POS 86,25 %, 236/237, COUVERTURE 0,9916 ; LA CONVENTION DU SUJET`
- **T1** `5a067ba5 06 23:45 ROADMAP ET JOURNAL — LA NUIT FINIT À 236/237, COUVERTURE 0,9916, POS 86,25 %, 2 SPANS ; r264 RÉGLÉ`
- **T1** `ba42d4cc 06 23:26 FICHE — LES TROIS RÈGLES REJETÉES (PARTICIPES, R4-FR GÉNÉRIQUE, PARTICIPE APRÈS AVOIR) ; POS RESTE À 86,25 %`
- **T1** `c43dd5cc 06 23:23 B13 — LA RÈGLE « QUE » (PRON APRÈS UN NOM, CONJ AILLEURS) : POS 85,84 → 86,25 %, F1 ET ATTACHEMENT INCHANGÉS ; 183/183`
- **T1** `6432bdb9 06 23:09 JOURNAL ET ROADMAP — LA NUIT DES ÉTATS : N2/S/R/A INVENTORIÉS, FRONTIÈRE CORRIGÉE (A6.2 LIBRE), POS 85,84 %, PONCT, R4-FR ; ÉTAT HORODATÉ`
- **T1** `6b976cb1 06 23:05 B13 — R4-FR FILTRÉ (ADJECTIF CONNU OU SUFFIXE) : POS 85,75 → 85,84 %, F1 ET ATTACHEMENT INCHANGÉS ; 183/183`
- **T1** `7a45325f 06 22:57 B13 — LA PONCTUATION A UNE POS (PONCT) : POS 85,00 → 85,75 %, MIROIR 0,196 → 0,2276, F1 ET ATTACHEMENT INCHANGÉS ; 183/183`
- **T1** `bfd98892 06 21:32 DOC PRODUIT — RESYNCHRONISÉE : POS 85,00 %, F1 0,6482, ATTACHEMENT 235/236, GELÉ 85,32 / 0,6511 ; SORTIE D'EVALUER REJOUÉE`
- **T1** `bb67dd59 06 21:14 ÉTAT ET JOURNAL — LA NUIT DES P0 : POS 85,00 %, ATTACHEMENT 235/236, FRONTIÈRES 0/40, PARTITION ÉTIQUETÉE, CONTRAT V1`
- **T1** `"Taille : 2,76 Mo de JSON pour 10 000 caractères (10 362 étiquettes) ; pas de JSONL, pas de lot, une invocation = un texte.",`
- **T1** `"texte": "La remise est de 12,5 % sur 1.234,56 euros.",`
- **T1** `"texte": "La remise est de 12,5 % sur 1.",`
- **T1** `d02 décimal+milliers | 'La remise est de 12,5 % sur 1.234,56 euros.'`
- **T1** `- **Temps** : `_phrases` sur 10 000 caractères : **2,98 ms → 8,47 ms** (×2,8). L'analyse complète de`
- **T1** `l'audit était à 590–765 ms sur 10 000 caractères ; l'ajout est négligeable à cette échelle.`
- **T1** `- **Patch B** : 8,97 ms contre 12,96 ms pour `_mots` sur le même texte (moins de tokens).`
- **T1** `156:Le **démarrage** (`--version`, 10 passages) coûte **134–192 ms**, médiane **146 ms**. Pour une`
- **T1** `583:| **P1-7** | **Compacité et lot** : `--compact`, JSONL, `--fichier`/stdin | **2,76 Mo** pour 10 k ; **11,5 Mo** pour 50 k ; 1 texte par appel | `drave.py` 50-52, 329-341 | **0,5–1 j** | faible : o`
- **T1** `| graphème, mot | ✅ | 0 crash, 0 span hors texte, `valeur = texte[debut:fin]` à **100 %**, couverture **49/50 à 100 %** (x46 : 95,14 %, newlines) |`
- **T1** ``reel_new` + 160 `synthétique`), soit **100 %**. Sur `all` : **612/612**.`
- **T1** `syntagme (51,9 %)** sont impliquées, dans **31/50 textes** ; 113 sont des **inclusions**, 19 des`
- **T1** `**graphème** : 49/50 textes à 100 %, x46 à **95,14 %** (7 newlines, catégorie `Cc`, non couvertes).`
- **T1** `**Mesuré au 06/11** : POS **85,00 %**, syntagmes F1 **0,6482**, attachement **235/236**`
- **T1** `> l'état courant du bloc est dans [`en-cours`](../docs/pilotage/en-cours.md) (POS 86,25 %,`
- **T1** `1/5 f01 rc=0 labels=20 t=149ms chev=0 filtrer=0 api=2.56ms`
- **T1** `2/5 f02 rc=0 labels=60 t=163ms chev=2 filtrer=0 api=1.35ms`
- **T1** `3/5 f03 rc=0 labels=41 t=151ms chev=3 filtrer=0 api=1.76ms`
- **T1** `4/5 f04 rc=0 labels=40 t=147ms chev=0 filtrer=0 api=2.16ms`
- **T1** `5/5 f05 rc=0 labels=31 t=154ms chev=1 filtrer=0 api=2.54ms`
- **T1** `1/50 f01 rc=0 labels=20 t=151ms chev=0 filtrer=0 api=1.58ms`
- **T1** `2/50 f02 rc=0 labels=60 t=163ms chev=2 filtrer=0 api=3.48ms`
- **T1** `3/50 f03 rc=0 labels=41 t=158ms chev=3 filtrer=0 api=3.56ms`
- **T1** `4/50 f04 rc=0 labels=40 t=157ms chev=0 filtrer=0 api=1.11ms`
- **T1** `5/50 f05 rc=0 labels=31 t=162ms chev=1 filtrer=0 api=1.28ms`
- **T1** `6/50 f06 rc=0 labels=67 t=158ms chev=6 filtrer=0 api=2.55ms`
- **T1** `7/50 f07 rc=0 labels=33 t=147ms chev=0 filtrer=0 api=1.61ms`
- **T1** `8/50 f08 rc=0 labels=39 t=166ms chev=0 filtrer=0 api=0.91ms`
- **T1** `9/50 f09 rc=0 labels=34 t=150ms chev=0 filtrer=0 api=0.81ms`
- **T1** `10/50 f10 rc=0 labels=58 t=170ms chev=1 filtrer=0 api=4.62ms`
- **T1** `11/50 f11 rc=0 labels=48 t=157ms chev=1 filtrer=0 api=1.65ms`
- **T1** `12/50 f12 rc=0 labels=70 t=159ms chev=2 filtrer=0 api=2.38ms`
- **T1** `13/50 f13 rc=0 labels=30 t=148ms chev=0 filtrer=0 api=1.07ms`
- **T1** `14/50 f14 rc=3 labels=0 t=169ms chev=0 filtrer=0 api=0.03ms`
- **T1** `15/50 f15 rc=3 labels=0 t=149ms chev=0 filtrer=0 api=0.01ms`
- **T1** `16/50 f16 rc=3 labels=0 t=153ms chev=0 filtrer=0 api=0.02ms`
- **T1** `17/50 f17 rc=3 labels=0 t=166ms chev=0 filtrer=0 api=0.02ms`
- **T1** `18/50 f18 rc=0 labels=7 t=144ms chev=0 filtrer=0 api=0.42ms`
- **T1** `19/50 f19 rc=0 labels=46 t=161ms chev=0 filtrer=0 api=2.17ms`
- **T1** `20/50 f20 rc=0 labels=72 t=171ms chev=3 filtrer=0 api=4.21ms`
- **T1** `21/50 f21 rc=0 labels=64 t=151ms chev=4 filtrer=0 api=3.36ms`
- **T1** `22/50 f22 rc=0 labels=59 t=159ms chev=2 filtrer=0 api=3.38ms`
- **T1** `23/50 f23 rc=0 labels=57 t=183ms chev=2 filtrer=0 api=3.46ms`
- **T1** `24/50 f24 rc=0 labels=75 t=164ms chev=6 filtrer=0 api=1.83ms`
- **T1** `25/50 f25 rc=0 labels=27 t=172ms chev=0 filtrer=0 api=1.61ms`
- **T1** `26/50 f26 rc=0 labels=53 t=160ms chev=2 filtrer=0 api=1.93ms`
- **T1** `27/50 f27 rc=0 labels=14 t=154ms chev=0 filtrer=0 api=0.93ms`
- **T1** `28/50 f28 rc=0 labels=49 t=145ms chev=0 filtrer=0 api=2.76ms`
- **T1** `29/50 f29 rc=0 labels=49 t=154ms chev=2 filtrer=0 api=1.51ms`
- **T1** `30/50 f30 rc=0 labels=43 t=164ms chev=2 filtrer=0 api=2.90ms`
- **T1** `31/50 f31 rc=0 labels=31 t=148ms chev=2 filtrer=0 api=1.79ms`
- **T1** `32/50 f32 rc=0 labels=65 t=161ms chev=1 filtrer=0 api=4.30ms`
- **T1** `33/50 f33 rc=0 labels=36 t=146ms chev=0 filtrer=0 api=1.91ms`
- **T1** `34/50 f34 rc=0 labels=57 t=157ms chev=4 filtrer=0 api=2.96ms`
- **T1** `35/50 f35 rc=0 labels=45 t=161ms chev=0 filtrer=0 api=1.78ms`
- **T1** `36/50 f36 rc=0 labels=50 t=160ms chev=0 filtrer=0 api=1.25ms`
- **T1** `37/50 f37 rc=0 labels=66 t=148ms chev=0 filtrer=0 api=1.75ms`
- **T1** `38/50 f38 rc=0 labels=110 t=166ms chev=1 filtrer=0 api=3.67ms`
- **T1** `39/50 f39 rc=0 labels=79 t=172ms chev=2 filtrer=0 api=3.87ms`
- **T1** `40/50 f40 rc=0 labels=96 t=160ms chev=0 filtrer=0 api=1.75ms`
- **T1** `41/50 f41 rc=0 labels=85 t=152ms chev=3 filtrer=0 api=4.55ms`
- **T1** `42/50 f42 rc=0 labels=34 t=151ms chev=0 filtrer=0 api=2.04ms`
- **T1** `43/50 f43 rc=0 labels=357 t=166ms chev=11 filtrer=0 api=14.30ms`
- **T1** `44/50 f44 rc=0 labels=62 t=143ms chev=2 filtrer=0 api=2.11ms`
- **T1** `45/50 f45 rc=0 labels=65 t=155ms chev=4 filtrer=0 api=2.43ms`
- **T1** `46/50 f46 rc=0 labels=58 t=162ms chev=5 filtrer=0 api=3.49ms`
- **T1** `47/50 f47 rc=0 labels=46 t=147ms chev=0 filtrer=0 api=2.53ms`
- **T1** `48/50 f48 rc=0 labels=92 t=166ms chev=0 filtrer=0 api=2.66ms`
- **T1** `49/50 f49 rc=0 labels=64 t=152ms chev=0 filtrer=0 api=3.53ms`
- **T1** `50/50 f50 rc=0 labels=2149 t=248ms chev=75 filtrer=0 api=55.49ms`
- **T1** `x17 json rc 0 ms 182.0 out 42528`
- **T1** `x17 readable rc 0 ms 168.2 out 10457 maxligne 10010`
- **T1** `1/20 x01 html               rc=0 phr=  2 labels=81 t=172ms json=23054 schema=True zone=0 q=False`
- **T1** `2/20 x02 html               rc=0 phr=  2 labels=281 t=169ms json=73464 schema=True zone=0 q=False`
- **T1** `3/20 x03 html               rc=0 phr=  4 labels=176 t=159ms json=45812 schema=True zone=0 q=True`
- **T1** `4/20 x04 markdown           rc=0 phr=  5 labels=151 t=165ms json=42458 schema=True zone=0 q=False`
- **T1** `5/20 x05 markdown-tableau   rc=0 phr=  4 labels=102 t=155ms json=25116 schema=True zone=0 q=False`
- **T1** `6/20 x06 markdown-code      rc=0 phr=  4 labels=103 t=157ms json=28504 schema=True zone=2 q=False`
- **T1** `7/20 x07 code-python        rc=0 phr=  2 labels=152 t=175ms json=39096 schema=True zone=0 q=False`
- **T1** `8/20 x08 code-json          rc=0 phr=  2 labels=141 t=152ms json=34656 schema=True zone=0 q=False`
- **T1** `9/20 x09 code-shell         rc=0 phr=  2 labels=99 t=156ms json=24703 schema=True zone=0 q=False`
- **T1** `10/20 x10 tableau-tsv        rc=0 phr=  1 labels=67 t=148ms json=16844 schema=True zone=0 q=False`
- **T1** `11/20 x11 tableau-ascii      rc=0 phr=  5 labels=173 t=159ms json=42016 schema=True zone=0 q=False`
- **T1** `12/20 x12 arabe              rc=0 phr=  2 labels=39 t=162ms json=10477 schema=True zone=0 q=False`
- **T1** `13/20 x13 chinois            rc=0 phr=  1 labels=16 t=156ms json=4814 schema=True zone=0 q=False`
- **T1** `14/20 x14 russe              rc=0 phr=  2 labels=39 t=158ms json=10503 schema=True zone=0 q=True`
- **T1** `15/20 x15 hébreu             rc=0 phr=  2 labels=43 t=151ms json=11429 schema=True zone=0 q=True`
- **T1** `16/20 x16 très-long          rc=0 phr=320 labels=18911 t=1657ms json=5803495 schema=True zone=0 q=False`
- **T1** `17/20 x17 très-long-un-token rc=0 phr=  1 labels=7 t=166ms json=42528 schema=True zone=0 q=False`
- **T1** `18/20 x18 nfd                rc=0 phr=  2 labels=54 t=151ms json=14954 schema=True zone=0 q=False`
- **T1** `19/20 x19 nfd-url            rc=0 phr=  1 labels=70 t=157ms json=20961 schema=True zone=0 q=False`
- **T1** `20/20 x20 url-parametres     rc=0 phr=  1 labels=143 t=151ms json=35685 schema=True zone=0 q=False`
- **T1** `| **P1-7** | **Compacité et lot** : `--compact`, JSONL, `--fichier`/stdin | **2,76 Mo** pour 10 k ; **11,5 Mo** pour 50 k ; 1 texte par appel | `drave.py` 50-52, 329-341 | **0,5–1 j** | faible : optio`

