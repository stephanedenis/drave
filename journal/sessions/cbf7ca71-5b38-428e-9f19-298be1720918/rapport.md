# Session cbf7ca71 — Tu travailles dans /home/stephane/Data13

> **Journaux :** [le jour](../../2026-11-18/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `cbf7ca71-5b38-428e-9f19-298be1720918` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-18 10:17 |
| Durée | 1.0 h |
| Tours | 1 |
| Messages | 123 |
| Appels d'outils | 124 |
| Fichiers touchés | 5 |
| Commandes | 96 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet (Drave, en français). Machine dédiée (40 threads, 125 Go RAM). NE TOUCHE PAS à `data/` (lecture seule).  CONTEXTE : l'inventaire `reports/rapport-donnees-inventaire.md` a montré que `data/corpus_wiki_fr_texte/train.txt` fait **7,50 Go** et pourrait fermer l'écart du palier 1, MAIS l'outil actuel `tools/corpus_propre.py` tient tous  … [2581 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet (Drave, en français). Machine dédiée (40 threads, 125 … [2861 caractères tronqués]

*124 appels d'outils.* Actions notables :

- bash — List workspace structure
- bash — Inspect data corpus size and disk
- bash — Check inventory report and corpus tool
- bash — Inspect beginning of train corpus
- read
- bash — Check Python, numpy, hardware, work dir
- bash — List related reports and style sample
- bash — Create 200MB slice for benchmarks
- bash — Measure Python set memory per entry
- bash — Benchmark pure-Python shingle hashing
- bash — Check git state, ignore rules, time binary
- bash — Micro-benchmark hash extraction variants
- bash — Check JSON manifest style and named-error conventions
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_blocs.py`
- … et 98 autres

**Synthèse produite :**

⏵ Bilan final : chiffres, contrôles, chemins

Travail terminé. Voici le bilan.

\## Livrables

| fichier | quoi |
|---|---|
| `tools/dedup_blocs.py` | l'outil (CLI demandée + autotest intégré, erreurs nommées) |
| `reports/rapport-dedup-blocs.md` | le rapport (dispositif, chiffres, contrôles, failles, comparaison inventaire) |
| `reports/dedup-blocs-7.5go.json` | le manifeste JSON de la passe |
| `work/dedup/train.txt` | la sortie (7 504 078 589 o, sha256 `27277e32…`), + `prouve-200Mo.json`, `controle/`, `granularite/`, diagnostics |

`data/` n'a pas été modifié (`train.txt` intact, mtime inchangé), aucun commit, aucun appel API, `en-cours`/`roadmap`/`AGENTS` intacts.

\## Chiffres — 7,50 Go, `--bloc-mo 64 --memoire-mo 2048`

- **Temps : 430,7 s = 7 min 11 s** (16,6 Mio/s ; CPU 99 %, 419,9 s user) — c'est le hachage qui domine, pas l'I/O.
- **RSS max : 954,3 Mio** pour un budget de 2 048 Mio (marge 1 094) ; confirmé de l'extérieur par `/usr/bin/time` (977 200 Kio).
- **112 blocs : 112 gardés, 0 écarté, 0 octet écarté → 0,000 %** ; sortie identique à l'entrée à l'octet près (`cmp`).
- 191 312 755 shingles calculés, 6 006 207 échantillonnés (1/32) : **4,177 % déjà vus avant leur bloc, 5,171 % avec les répétitions internes**. Le bloc le plus chargé est à **48,9 %** — loin du seuil de 80 %.
- Preuve de budget : **200 Mo avec 256 Mio → RSS 120,8 Mio** (marge 135) ; budget impossible → `ERREUR budget_memoire_impossible` (rc 3) ; chien de garde déclenché pour de vrai → `ERREUR memoire_depassee` (rc 3).

\## Les 4 cas de contrôle (18/18 assertions vertes)

| cas | attendu | observé |
|---|---|---|
| (a) texte unique | gardé | **gardé**, 0,0 % |
| (b) copie exacte | écarté | **écarté**, 100,0 % |
| (c) copie à 9,4 % modifiée | écarté à 0,8, gardé à 0,95 | **écarté** (90,04–90,21 %), **gardé à 0,95** — le seuil tranche entre 0,90 et 0,95 |
| (d) texte différent | gardé | **gardé**, 0,0 % |

En plus : copie **décalée de 21 octets** écartée (99,9–100 %) — c'est précisément ce qu'une grille à pas fixe rate ; copie à **10 % de mots dispersés gardée** (1–3 % vus) ; **stabilité** : deux passes → même sha256 (`1a5c01ef…`), mêmes décisions, mêmes octets.

\## Le résultat qui change la suite

Le dédoublonnage **par blocs ne ferme pas l'écart** : à 64 Mio, 0 % ; même à 4 Kio, 0,147 % seulement. La mesure exacte ligne à ligne montre pourquoi : **53,98 % des lignes sont des répétitions, mais 8,28 % des octets** (621 Mo, dont 23 Mo de lignes vides à préserver → 598 Mo de contenu ; 2
… [448 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_blocs.py` | 2 | 8 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/dedup/diagnostic_ancrage.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/dedup/diagnostic_lignes.py` | 2 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/dedup/diagnostic_lignes_exact.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dedup-blocs.md` | 1 | 0 |

### Commandes exécutées (échantillon)

- **T1** List workspace structure
- **T1** Inspect data corpus size and disk
- **T1** Check inventory report and corpus tool
- **T1** Inspect beginning of train corpus
- **T1** Check Python, numpy, hardware, work dir
- **T1** List related reports and style sample
- **T1** Create 200MB slice for benchmarks
- **T1** Measure Python set memory per entry
- **T1** Benchmark pure-Python shingle hashing
- **T1** Check git state, ignore rules, time binary
- **T1** Micro-benchmark hash extraction variants
- **T1** Check JSON manifest style and named-error conventions
- **T1** Smoke test on 3 MB slice
- **T1** Run the autotest (negative control)
- **T1** Re-run the autotest
- **T1** Inspect first autotest cases
- **T1** Inspect per-block journal of control run
- **T1** Check whether identical blocks hash identically
- **T1** Inspect the hashing/insertion code
- **T1** Instrument the loop to find the insertion bug
- **T1** Compare fixed-grid vs line-anchored shingle duplication
- **T1** Word-anchored and stride-1 duplication ceiling
- **T1** True duplicate rate vs anchoring on 20 MB
- **T1** Measure anchor density and seen rate on 200 MB
- **T1** Run the autotest with content-defined anchors
- **T1** Run tool directly to see the traceback
- **T1** Regenerate control files and run directly
- **T1** Re-run the autotest after fixing nonlocal
- **T1** Measure real set memory cost per entry
- **T1** Replace calibration with measured constant
- **T1** Re-run autotest after memory model change
- **T1** Run 200 MB proof with 256 MiB budget
- **T1** Measure RSS by block size on 1 MB
- **T1** Profile allocations with tracemalloc
- **T1** Time normalization, hashing, anchoring separately
- **T1** Instrument RSS by phase
- **T1** Compare regex normalization memory
- **T1** Fix normalization memory and re-test 200 MB
- **T1** Inspect 200 MB proof JSON
- **T1** Add within-block-inclusive metric and re-run 200 MB
- … et 56 autres

## 4. Mesures et résultats marquants

- **T1** `/dev/mapper/system-root   11T  9,0T  1,9T  83% /home/stephane/Data13TB`
- **T1** `"split": "hash salé (graine 1) de page_id : 5% val, 5% test"`
- **T1** `recouvrement de contexte en Mio (défaut : 2 % du bloc,`
- **T1** `{'budget_mio': 512.0, 'plancher_mio': 80.3, 'bloc_mio': 0.06, 'recouvrement_octets': 1310, 'recouvrement_origine': '2 % du bloc, plafonné à 1 Mio', 'cout_entree': {'table_octets_entree': 104.9, 'entie`
- **T1** `grille pas=96 : 2083333 shingles, 27942 vus (1.34 %) en 2.7s`
- **T1** `grille pas=48 : 4166665 shingles, 64493 vus (1.55 %) en 5.4s`
- **T1** `lignes        : 1741348 shingles, 48527 vus (2.79 %) en 2.6s`
- **T1** `ancrage mots  : 7596803 shingles, 23735 vus (0.31 %) en 12.5s`
- **T1** `stride 1 (/8) : 6249988 shingles, 5080 vus (0.08 %) en 19.5s`
- **T1** `tous, hash 1/16: 1249191 éch., 3035 vus (0.24 %) en 21.8s`
- **T1** `grille 96      : 208333 éch., 17 vus (0.01 %) en 0.3s`
- **T1** `grille 48      : 416665 éch., 57 vus (0.01 %) en 0.5s`
- **T1** `lignes         : 145317 éch., 462 vus (0.32 %) en 0.2s`
- **T1** `débuts de ligne seuls: 1279914 ancres (0.006/octet), 34632 vus (2.71 %), 2.5s`
- **T1** `lignes + pas 192: 1905640 ancres (0.010/octet), 49546 vus (2.60 %), 3.6s`
- **T1** `lignes + pas 96: 2829425 ancres (0.014/octet), 70820 vus (2.50 %), 5.1s`
- **T1** `lignes + pas 48: 4830662 ancres (0.024/octet), 116448 vus (2.41 %), 8.3s`
- **T1** `-rw-r--r--. 1 stephane stephane 200000000 18 nov 10:46 work/dedup/slice-200Mo.txt`
- **T1** `[bloc 1] 0/1 Mio, 0.0% vu, gardé, RSS 70 Mio, 7 s`
- **T1** `[bloc 1] 0/1 Mio, 0.0% vu, gardé, RSS 58 Mio, 0 s`
- **T1** `1+ (actuel): 60.8 ms, pic RSS 45.9 Mio (+33.3), len=1000000`
- **T1** `2+ (proposé): 19.0 ms, pic RSS 45.9 Mio (+0.0), len=1000000`
- **T1** `=== 1 Mo ===`
- **T1** `=== 200 Mo, budget 256 ===`
- **T1** `[bloc 18] 136/191 Mio, 15.9% vu, gardé, RSS 121 Mio, 8 s`
- **T1** `[bloc 19] 144/191 Mio, 7.6% vu, gardé, RSS 121 Mio, 9 s`
- **T1** `[bloc 20] 152/191 Mio, 2.8% vu, gardé, RSS 121 Mio, 9 s`
- **T1** `[bloc 21] 160/191 Mio, 3.7% vu, gardé, RSS 126 Mio, 10 s`
- **T1** `[bloc 22] 168/191 Mio, 1.3% vu, gardé, RSS 127 Mio, 10 s`
- **T1** `[bloc 23] 176/191 Mio, 0.3% vu, gardé, RSS 128 Mio, 10 s`
- **T1** `[bloc 24] 184/191 Mio, 0.6% vu, gardé, RSS 128 Mio, 11 s`
- **T1** `"recouvrement_origine": "2 % du bloc, plafonné à 1 Mio",`
- **T1** `[bloc 5] 256/7156 Mio, 3.3% vu, gardé, RSS 437 Mio, 18 s`
- **T1** `[bloc 6] 320/7156 Mio, 1.5% vu, gardé, RSS 439 Mio, 22 s`
- **T1** `[bloc 7] 384/7156 Mio, 1.9% vu, gardé, RSS 442 Mio, 26 s`
- **T1** `[bloc 14] 832/7156 Mio, 1.8% vu, gardé, RSS 504 Mio, 52 s`
- **T1** `[bloc 15] 896/7156 Mio, 7.0% vu, gardé, RSS 506 Mio, 56 s`
- **T1** `[still running after 60000ms; moved to background job bash-646]`
- **T1** `[bloc 37] 2304/7156 Mio, 1.4% vu, gardé, RSS 587 Mio, 139 s`
- **T1** `[bloc 38] 2368/7156 Mio, 2.0% vu, gardé, RSS 589 Mio, 143 s`
- **T1** `[bloc 64] 4032/7156 Mio, 2.0% vu, gardé, RSS 716 Mio, 243 s`
- **T1** `[bloc 65] 4096/7156 Mio, 2.1% vu, gardé, RSS 718 Mio, 247 s`
- **T1** `[bloc 96] 6080/7156 Mio, 2.4% vu, gardé, RSS 792 Mio, 368 s`
- **T1** `[bloc 97] 6144/7156 Mio, 2.1% vu, gardé, RSS 794 Mio, 372 s`
- **T1** `[bloc 98] 6208/7156 Mio, 2.7% vu, gardé, RSS 796 Mio, 376 s`
- **T1** `Percent of CPU this job got: 99%`
- **T1** `grille 96 (inventaire)   pas= 96 shingles=   1041666 vus=     412 (0.04 %) en 1.5 s`
- **T1** `grille 48                pas= 48 shingles=   2083332 vus=    1531 (0.07 %) en 2.9 s`
- **T1** `ancres (outil)           pas= 48 shingles=   2436451 vus=   10971 (0.45 %) en 3.7 s`
- **T1** `lignes déjà vues : 724258 (41.59 %)`
- **T1** `octets dans ces lignes : 7488062 (3.74 %)`
- **T1** `vides          461435     461434    100.0%        461434     0.23%`
- **T1** `1-19 o         290809     201021     69.1%       1972881     0.99%`
- **T1** `20-79 o        453824      51527     11.4%       1545074     0.77%`
- **T1** `80 o et +      535281      10276      1.9%       3508673     1.75%`
- **T1** `lignes dupliquées de 80 o et + : 10276 (1.9 % des lignes longues), 3508673 octets = 1.75 % du fichier`
- **T1** `ok True cas 18 ko 0`
- **T1** `=== granularité (200 Mo) ===`
- **T1** `bloc   0.004 Mio :  50837 blocs,    74 écartés,     293157 o (0.147 %), RSS 108 Mio, 13.5 s, vus 2.45 % / 2.47 %`
- **T1** `bloc   0.064 Mio :   2993 blocs,     0 écartés,          0 o (0.000 %), RSS 109 Mio, 12.1 s, vus 2.40 % / 2.47 %`
- **T1** `bloc     1.0 Mio :    191 blocs,     0 écartés,          0 o (0.000 %), RSS 117 Mio, 11.6 s, vus 2.31 % / 2.47 %`
- **T1** `bloc    64.0 Mio :      3 blocs,     0 écartés,          0 o (0.000 %), RSS 474 Mio, 10.9 s, vus 1.59 % / 2.35 %`
- **T1** `=== 200 Mo / 256 Mio ===`
- **T1** `lignes dupliquées 1156196 (47.7 %), octets dupliqués 10155845 (5.08 %)`
- **T1** `vides      lignes=  619341 dupl=  619340 (100.0 %) octets=    619341 dup=   619340 (100.0 %)`
- **T1** `1-19 o     lignes=  569080 dupl=  398705 ( 70.1 %) octets=   6795543 dup=  4372268 ( 64.3 %)`
- **T1** `20-79 o    lignes=  663142 dupl=  131314 ( 19.8 %) octets=  27349272 dup=  4028645 ( 14.7 %)`
- **T1** `80 o et +  lignes=  572411 dupl=    6837 (  1.2 %) octets= 165235798 dup=  1135592 (  0.7 %)`
- **T1** `lignes déjà vues : 47563661 (53.98 %) ; octets : 621277675 (8.28 %)`
- **T1** `1-19 o         42878299     39484010     92.1%      250044292     201832862     80.7%`
- **T1** `20-79 o        24089913      7261823     30.1%      962983444     223686767     23.2%`
- **T1** `80 o et +      21146220       817828      3.9%     6291050853     195758046      3.1%`
- **T1** `blocs > 20%: 3`
- **T1** `vides          23037969     23037968    100.0%       23037969      23037968    100.0%`
- **T1** `1-19 o         20689727     16900629     81.7%      243994263     187886634     77.0%`
- **T1** `20-79 o        23410695      6825264     29.2%      959609824     216037267     22.5%`
- **T1** `80 o et +      20976041       799800      3.8%     6277436533     194315806      3.1%`
- **T1** `280:   hachage, avec normalisation. Les chiffres entre 2 et 5 % mesurent des choses voisines, pas`
- **T1** `296:- **La duplication réelle est plus grande que 2 %, et plus courte.** 54 % des lignes, 8,28 % des`
- **T1** `2,9M	work/dedup/essai-3mo-garde.txt`
- **T1** `4,0K	work/dedup/essai-3mo.json`
- **T1** `2,9M	work/dedup/essai-3mo.txt`
- **T1** `8,0K	work/dedup/prouve-200Mo.json`
- **T1** `4,0K	work/dedup/prouve-200Mo.log`
- **T1** `4,0K	work/dedup/prouve-200Mo.out`
- **T1** `191M	work/dedup/slice-200Mo-garde.txt`
- **T1** `191M	work/dedup/slice-200Mo.txt`
- **T1** `-rw-r--r--. 1 stephane stephane   3000000 18 nov 10:34 work/dedup/essai-3mo-garde.txt`
- **T1** `-rw-r--r--. 1 stephane stephane      2879 18 nov 10:34 work/dedup/essai-3mo.json`
- **T1** `-rw-r--r--. 1 stephane stephane   3000000 18 nov 10:34 work/dedup/essai-3mo.txt`
- **T1** `200 Mo, blocs de exactement 8 Mio : 0`
- **T1** `forcerait une coupe) — plus une marge de contexte **après** le bloc (2 % du bloc, max 1 Mio)`
- **T1** `sans nl         rc=0 sortie=/tmp/edge/sans_nl.txt stderr=[bloc 1] 0/0 Mio, 0.0% vu, gardé, RSS 22 Mio, 0 s`
- **T1** `seuil 0         rc=0 sortie=/tmp/edge/seuil_0.txt stderr=[bloc 1] 0/0 Mio, 0.0% vu, gardé, RSS 22 Mio, 0 s`
- **T1** `seuil 1         rc=0 sortie=/tmp/edge/seuil_1.txt stderr=[bloc 1] 0/0 Mio, 0.0% vu, gardé, RSS 22 Mio, 0 s`
- **T1** `court      rc=0 stderr=[bloc 1] 0/0 Mio, 0.0% vu, gardé, RSS 22 Mio, 0 s`
- **T1** `sans nl    rc=0 stderr=[bloc 1] 0/0 Mio, 0.0% vu, gardé, RSS 22 Mio, 0 s`
- **T1** `8 octets   rc=0 stderr=[bloc 1] 0/0 Mio, 0.0% vu, gardé, RSS 22 Mio, 0 s`
- **T1** `214:jusqu'à 621 Mo (8,28 %), dont 23 Mo de lignes vides à préserver comme séparateurs : **598 Mo`
- **T1** `288:   **ligne**, on retirerait jusqu'à 621 Mo (8,28 %), dont 23 Mo de lignes vides (à garder) et`
- **T1** `308:  octets (598 Mo hors lignes vides), dont 2,6 % de prose. La conclusion de l'inventaire — « le volume est là, il faut`
- **T1** `- **Le chiffre de l'inventaire est à corriger** dans les documents de pilotage : 2,0 % est une`
- **T1** `sous-estimation (méthode à grille fixe) et la masse retirable par ligne est plutôt de 8 % des`
- **T1** `octets (598 Mo hors lignes vides), dont 2,6 % de prose. La conclusion de l'inventaire — « le volume est là, il faut`
- **T1** `- **Ce qui n'est pas tranché** : retirer 8,28 % des octets en supprimant les lignes répétées`
- **T1** `octets (598 Mo hors lignes vides), dont 2,6 % de prose. La conclusion de l'inventaire — « le`
- **T1** `301: 138:   octets ; pour les lignes de 80 o et +, 3,1 % de leurs octets (194 Mo, 2,59 % du fichier). La prochaine action est un dédoublonnage **par`
- **T1** `- **La duplication réelle est plus grande que 2 %, et plus courte.** 54 % des lignes, 8,28 % des`
- **T1** `octets ; pour les lignes de 80 o et +, 3,1 % de leurs octets (194 Mo, 2,59 % du fichier).`
- **T1** `-rw-r--r--. 1 stephane stephane       7513 18 nov 11:11 prouve-200Mo.json`
- **T1** `-rw-r--r--. 1 stephane stephane       2237 18 nov 11:11 prouve-200Mo.log`
- **T1** `-rw-r--r--. 1 stephane stephane       1032 18 nov 11:11 prouve-200Mo.out`
- **T1** `-rw-r--r--. 1 stephane stephane  200000000 18 nov 11:11 slice-200Mo-garde.txt`
- **T1** `-rw-r--r--. 1 stephane stephane  200000000 18 nov 10:46 slice-200Mo.txt`

