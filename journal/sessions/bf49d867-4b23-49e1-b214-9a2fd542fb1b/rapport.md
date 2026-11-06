# Session bf49d867 — Tu travailles dans le dépôt

> **Journaux :** [le jour](../../2026-11-06/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `bf49d867-4b23-49e1-b214-9a2fd542fb1b` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-06 11:17 |
| Durée | 1.8 h |
| Tours | 1 |
| Messages | 102 |
| Appels d'outils | 103 |
| Fichiers touchés | 2 |
| Commandes | 86 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **diagnostiquer la POS anglaise** et proposer des correctifs mesurés, sans modifier le code.  Contexte : `tools/bloc_linguistique.py` (`_pos`, `POS_FERME`, `VERBES`, `ADJECTIFS`, la règle de contexte DET/PRÉP/ADJ → nom), `tools/tests/linguistique/evaluer_gold.py` (`evaluer_bloc`). État : P … [1858 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **diagnost … [2138 caractères tronqués]

*103 appels d'outils.* Actions notables :

- bash — Check repo state and branch
- bash — List repo and tools directories
- bash — List test harness directories
- grep
- read
- bash — Inspect gold dataset composition
- bash — Run gold evaluation baseline
- bash — Print baseline POS metrics
- bash — Diagnose English POS errors
- bash — Decompose EN errors by mechanism
- bash — Compute dev/test split and conditional stats
- bash — Audit rule risks on gold
- bash — Run POS rule variants on dev and test
- bash — Fix patch anchor and rerun variants
- … et 79 autres

**Synthèse produite :**

⏵ Final file check before reporting to the parent

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pos-anglais.md` | 1 | 3 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-pos-anglais.json` | 0 | 1 |

### Commandes exécutées (échantillon)

- **T1** Check repo state and branch
- **T1** List repo and tools directories
- **T1** List test harness directories
- **T1** Inspect gold dataset composition
- **T1** Run gold evaluation baseline
- **T1** Print baseline POS metrics
- **T1** Diagnose English POS errors
- **T1** Decompose EN errors by mechanism
- **T1** Compute dev/test split and conditional stats
- **T1** Audit rule risks on gold
- **T1** Run POS rule variants on dev and test
- **T1** Fix patch anchor and rerun variants
- **T1** Token-level fixes and breaks per rule
- **T1** Debug R3 brother/mother breaks
- **T1** Fix R3 lookahead and rerun
- **T1** Print full metrics table
- **T1** Check split membership and branch counts
- **T1** Run final measurement script
- **T1** Inspect breaks and transitions
- **T1** Inspect flowers/books breaks
- **T1** Inspect R2S patch text
- **T1** Instrument R2s on the break phrases
- **T1** Trace R2s decisions
- **T1** Rerun measurements with reordered R2s
- **T1** List breaks and residual errors
- **T1** Print breaks and residual list from file
- **T1** Print R2 breaks and residual errors
- **T1** Compute cause partition with counts
- **T1** Print final metrics table and deltas
- **T1** Measure context rule precision and FR branches
- **T1** List penssee JSON files in reports
- **T1** Inspect penssee JSON structure
- **T1** Find A14 and baseline POS references
- **T1** Locate A14 in docs
- **T1** Read A14 context and related reports
- **T1** Read existing English/POS JSON reports
- **T1** Read English gold audit structure
- **T1** Check report style and hashes
- **T1** Read English gold report style and POS section
- **T1** Check when English VERBES_CONNUS was added
- … et 46 autres

## 4. Mesures et résultats marquants

- **T1** `ADJ   n=  40 ok=  24 (60.0%)  NOUN:12  VERB:4`
- **T1** `ADV   n=  34 ok=  17 (50.0%)  NOUN:15  PREP:1  ?:1`
- **T1** `AUX   n=  61 ok=  60 (98.4%)  NOUN:1`
- **T1** `CONJ  n=  36 ok=  22 (61.1%)  DET:12  NOUN:2`
- **T1** `DET   n= 213 ok= 213 (100.0%)`
- **T1** `NOUN  n= 248 ok= 238 (96.0%)  ADJ:5  VERB:5`
- **T1** `NUM   n=   1 ok=   1 (100.0%)`
- **T1** `PONCT n=   3 ok=   0 (0.0%)  ?:3`
- **T1** `PREP  n=  43 ok=  43 (100.0%)`
- **T1** `PRON  n= 200 ok= 177 (88.5%)  DET:14  NOUN:8  CONJ:1`
- **T1** `VERB  n= 269 ok=  83 (30.9%)  NOUN:176  ADJ:5  AUX:4  ?:1`
- **T1** `VERB   186 (68.9%)`
- **T1** `PRON    23 (8.5%)`
- **T1** `ADV     17 (6.3%)`
- **T1** `ADJ     16 (5.9%)`
- **T1** `CONJ    14 (5.2%)`
- **T1** `NOUN    10 (3.7%)`
- **T1** `PONCT    3 (1.1%)`
- **T1** `AUX      1 (0.4%)`
- **T1** `176 (65.2%)  C1 défaut nominal / lexique verbal non consulté`
- **T1** `15 ( 5.6%)  C3 ADV anglais absent du lexique`
- **T1** `14 ( 5.2%)  C2 DET ambigu prioritaire (that/her)`
- **T1** `12 ( 4.4%)  C2 DET ambigu prioritaire (that)`
- **T1** `12 ( 4.4%)  C5 ADJ attribut inconnu après copule`
- **T1** `8 ( 3.0%)  C3 PRON anglais absent (where/whose/mine)`
- **T1** `5 ( 1.9%)  C4 morphologie fr (-able/-al → ADJ) sur nom`
- **T1** `5 ( 1.9%)  C4 morphologie fr (-ive/-able/-al) sur verbe`
- **T1** `5 ( 1.9%)  C7 bruit or/span (ponctuation, tokenisation)`
- **T1** `4 ( 1.5%)  C4 morphologie fr (-ed/-ing → verbe) sur ADJ`
- **T1** `4 ( 1.5%)  C7 convention or (copule taguée VERB)`
- **T1** `3 ( 1.1%)  C4 VERBES[en] contient un nom (rain)`
- **T1** `2 ( 0.7%)  C4 morphologie fr (-er → verbe) sur nom`
- **T1** `2 ( 0.7%)  C3 CONJ anglais absent + majuscule (as)`
- **T1** `1 ( 0.4%)  C3 PREP/PREP ambigu (outside)`
- **T1** `1 ( 0.4%)  C3 pronom relatif → CONJ (when)`
- **T1** `1 ( 0.4%)  C3 AUX anglais absent (am)`
- **T1** `docs/produit/README.md:121:POS         exactitude 75.81 %  (fermé 90.04 %, ouvert 62.34 %)`
- **T1** `| **1 bis** | A5 contrat S, A6 coût/cache | interface S, O(n²) | ✅ intégrée (cache ×139) |`
- **T1** `.spans.reel.note = L'anglais réel perd 58/85 (68,2 %) ; le français réel 8/86 (9,3 %). Les 60 spans anglais pleins sont 28 REL, 26 SUB, 6 GP.`
- **T1** `.verdict.gold_anomalies = 25/210 phrases (11,9 %), dont 16 (7,6 %) sur les couches mesurées ; 10 tags POS divergents, 6 GP sans cible, 3 rôles`
- **T1** `.verdict.anglais_echec = 60/94 spans perdus, 100 % des REL et SUB anglais ; la cause est la segmentation, pas le gold`
- **T1** `.verdict.est_verbe = 83,5 % d'accord avec le POS gold sur les cibles ; 15 FN, 1 FP (flower) ; garder le POS gold comme référence`
- **T1** `.recommandation[] 3. Hygiène du gold : 7 tags durs (is×3, do, late×2, far), normaliser that (3 CONJ→PRON) ou versionner, 4 cibles GP après verbe, 2 GP de copule à trancher, rôles r165/r239/r180, modal`
- **T1** `> substituables, un parallèle et une cascade, une activation sémantique à **51–76 %** ; la`
- **T1** `- **25 phrases anglaises sur 210 (11,9 %)** portent au moins une anomalie, mais seulement **16 (7,6 %)**`
- **T1** `- **60 des 94 spans perdus sont anglais (63,8 %)**, alors que l'anglais ne pèse que 88/239 segments à`
- **T1** `cible (36,8 %). Mais ces 60 échecs sont **des spans**, pas des cibles : sur les 28 segments anglais`
- **T1** `| tags POS en contradiction avec une autre occurrence | 7 (`est`×4, `que`×3) | 10 (7 durs + 3 `that`) |`
- **T1** `59:| tags POS en contradiction avec une autre occurrence | 7 (`est`×4, `que`×3) | 10 (7 durs + 3 `that`) |`
- **T1** `195:| POS seuls (10 tags) | 10 | 4,8 % |`
- **T1** `196:| couches mesurées : 7 POS durs + 4 cibles après verbe + 2 rôles faux + 1 modalité + 2 non grammaticales | **16** | **7,6 %** |`
- **T1** `268:| POS majoritaire (toujours VERB) | 23,43 % | 25,75 % | l'analyseur fait mieux, mais l'écart fr/en reste |`
- **T1** `ADJ   n=  94 ok=  26 (27.7%)  NOUN:68`
- **T1** `ADV   n= 107 ok= 100 (93.5%)  NOUN:5  PREP:1  ADJ:1`
- **T1** `AUX   n=  67 ok=  58 (86.6%)  PREP:4  ?:3  NOUN:2`
- **T1** `CONJ  n=  62 ok=  22 (35.5%)  PRON:25  ?:13  PREP:2`
- **T1** `DET   n= 375 ok= 373 (99.5%)  ?:2`
- **T1** `NOUN  n= 434 ok= 419 (96.5%)  ADJ:12  VERB:2  ?:1`
- **T1** `PONCT n=  22 ok=   0 (0.0%)  ?:22`
- **T1** `PREP  n=  71 ok=  71 (100.0%)`
- **T1** `PRON  n= 275 ok= 234 (85.1%)  ?:30  DET:11`
- **T1** `VERB  n= 523 ok= 228 (43.6%)  NOUN:274  ?:15  AUX:3  PREP:2  ADV:1`
- **T1** `résidu 78`
- **T1** `NOUN+VERB+ADJ = **557 jetons (48,5 %)** et **212 des 270 erreurs (78,5 %)** :`
- **T1** `verdict: Le défaut nominal de _pos (176 VERB->NOUN, 65,2 % des erreurs anglaises) n'est pas la règle de contexte (33 conversions, 33/33 justes) ; R2+R3 valent +7,44 pts`
- **T1** `- **L'anglais n'est pas la langue la plus faible** : 76,48 % contre 75,43 % pour le français, et`
- **T1** `35,1 % des erreurs pour 36,1 % des jetons. Sa spécificité est la **forme** de l'erreur (65,2 % en`
- **T1** `morphologie française appliquée à l'anglais — qui pèsent **27,0 %** de ses erreurs ; un quatrième,`
- **T1** `l'adjectif attribut, en ajoute 4,4 %.`
- **T1** `**+5,23 pt** ; anglais 76,48 → **85,28 %**, français 75,43 → **79,81 %**. F1 et attachement`
- **T1** ``-er`). Coût accepté de 0,5 : 3 infinitifs français après PRÉP (`attraper`, `manger` ×2) restent`

## 5. Erreurs rencontrées

3 sorties en erreur ou divergentes. Les premières :

- **T1** : V0 dev 0.7547 test 0.7656 | dev_en 0.7528 test_en 0.7925 [stderr] Traceback (most recent call last):   File "/tmp/qpos/sim.py", line 125, in <module>     mod = charger('bl_' + nom.replace('+','_'), pa
- **T1** : ok   File "/tmp/qpos/mesures_finales.py", line 81, in <module>     P_R4 = [(FIN_3BIS, FIN_3BIS + R4)]                                   ^^ NameError: name 'R4' is not defined. Did you mean: 'R3'? [std
- **T1** : (no output) [exit code: 1]

