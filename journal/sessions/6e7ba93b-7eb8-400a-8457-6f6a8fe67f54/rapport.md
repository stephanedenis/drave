# Session 6e7ba93b — Tu travailles dans /home/stephane/Data13

> **Journaux :** [le jour](../../2026-11-18/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `6e7ba93b-7eb8-400a-8457-6f6a8fe67f54` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-18 11:47 |
| Durée | 0.8 h |
| Tours | 1 |
| Messages | 71 |
| Appels d'outils | 87 |
| Fichiers touchés | 2 |
| Commandes | 47 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet (Drave, en français). Machine dédiée. `data/` est en LECTURE SEULE.  CONTEXTE : `reports/rapport-dedup-blocs.md` vient d'établir que le dédoublonnage par blocs n'écarte rien (0 %) sur `data/corpus_wiki_fr_texte/train.txt` (7,50 Go) parce que la duplication est courte et diffuse : la mesure exacte donne **53,98 % des lignes répétées … [2657 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet (Drave, en français). Machine dédiée. `data/` est en  … [2937 caractères tronqués]

*87 appels d'outils.* Actions notables :

- bash — List workspace, tools, reports, work
- bash — Inspect data dir and machine resources
- bash — Find dedup-related files
- read
- bash — Read dedup_blocs.py header and CLI
- bash — Inspect proof JSON, env, gitignore
- bash — Map functions and CLI in dedup_blocs.py
- bash — Read execute core of dedup_blocs.py
- bash — Read JSON skeleton, autotest and main
- bash — Read exact-lines diagnostic log and input signature
- bash — Benchmark hash table throughput on 200MB slice
- bash — Measure 1GiB array allocation RSS peak
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py`
- bash — Compile the new tool
- … et 62 autres

**Synthèse produite :**

⏵ Dédoublonnage par ligne terminé, mesuré et contrôlé

\## Chiffres (passe principale)

- **Entrée** : `data/corpus_wiki_fr_texte/train.txt`, **7 504 078 589 o**, sha256 `27277e32…`
- **Sortie** : `work/dedup/train-lignes.txt`, **6 900 585 097 o** (6,43 Gio), **63 438 199 lignes**, sha256 **`e3112a842ed6d97a15b2da0dd20d5f3d6ea81477356d0741fce175d7f3858552`**
- **Écarté** : **24 676 233 lignes (28,005 %** ; 37,919 % des non-vides) et **603 493 492 o (8,042 %)**
- **Préservé** : **23 037 969 lignes vides** (26,146 % des lignes, 0,307 % des octets)
- **Temps** : **161,1 s de passe** (2 min 41 s) + 21,3 s de relecture `--verifier` = **182,4 s** ; **44,4 Mio/s** de passe ; CPU 169,97 s user + 8,51 s sys.
- **RSS** : `ru_maxrss` **1 053,4 Mio**, VmRSS 1 053,8, pour budget **2 048 Mio** (marge **994,6 Mio**). Table exacte de 1 GiB (2^27 cases, 40 400 230 entrées, charge 30,10 %).
- **Preuve 200 Mo** : budget **64 Mio**, `ru_maxrss` **49,5 Mio** (marge 14,5), table 16 Mio, 263 917 lignes / 7 053 497 o écartés (15,156 % / 3,527 %), sortie 192 946 503 o.
- **Idempotence** : 2ᵉ passe sur la sortie → **0 ligne écartée**, même sha256, mêmes 6 900 585 097 o ; 118,5 s, même RSS.

\## Comparaison aux 53,98 % / 8,28 %

Réconciliation exacte avec le rapport blocs :
- `47 563 661 − 23 037 968 (vides préservées) + 150 540 (espaces de fin) = 24 676 233 lignes`
- `621 277 675 − 23 037 968 + 5 253 785 = 603 493 492 o`

Soit **54,150 % / 8,349 %** à politique de lignes vides égale, et **28,005 % / 8,042 %** en pratique (les vides expliquent −0,307 point ; le `rstrip` ajoute +0,070 point). La variante `--normaliser` retire 164 547 lignes / 6 528 572 o de plus, mais coûte 260,8 s.

\## Autotest : 16/16

(a) ligne unique gardée (6 non-vides, sortie exacte) ;
(b) copie exacte écartée (1) ;
(c) copie avec espaces de fin écartée par défaut (1), première occurrence écrite **telle quelle** avec ses espaces ;
(d) ligne différente gardée ;
(e) 4 lignes vides préservées (3 `\n` + 1 `   \n`), `vides_lues = 4` ;
(f) deux passes → **même sha256** `3de1a6d9…`, sorties identiques.

Extras : `--normaliser` (4 écartées vs 2, sha stable), `budget_memoire_impossible` rc 3, `capacite_depassee` rc 3, `memoire_depassee` rc 3, `--verifier` OK.

\## Chemins

- `tools/dedup_lignes.py`
- `reports/rapport-dedup-lignes.md`
- `reports/dedup-lignes-7.5go.json`
- `work/dedup/train-lignes.txt` (corpus v2)
- `work/dedup/prouve-200Mo-lignes.json`
- `work/dedup/autotest-lignes/autotest.json`
- `work/dedup/idempotence-t
… [706 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py` | 1 | 17 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dedup-lignes.md` | 1 | 7 |

### Commandes exécutées (échantillon)

- **T1** List workspace, tools, reports, work
- **T1** Inspect data dir and machine resources
- **T1** Find dedup-related files
- **T1** Read dedup_blocs.py header and CLI
- **T1** Inspect proof JSON, env, gitignore
- **T1** Map functions and CLI in dedup_blocs.py
- **T1** Read execute core of dedup_blocs.py
- **T1** Read JSON skeleton, autotest and main
- **T1** Read exact-lines diagnostic log and input signature
- **T1** Benchmark hash table throughput on 200MB slice
- **T1** Measure 1GiB array allocation RSS peak
- **T1** Compile the new tool
- **T1** Locate lines to patch
- **T1** Run autotest and show summary
- **T1** Show autotest case results
- **T1** Read full autotest stderr log
- **T1** Fix bytes in autotest JSON detail
- **T1** Rerun autotest and print cases
- **T1** Test ru_maxrss inheritance across fork/exec
- **T1** Locate RSS usages
- **T1** Rerun autotest after RSS fix
- **T1** Run 200MB proof at 64 MiB budget
- **T1** Run full 7.5GB line dedup
- **T1** Inspect full-run manifest and external RSS
- **T1** Locate timing code
- **T1** Re-run autotest after timing patch
- **T1** Rerun 200MB proof with separate timings
- **T1** Full 7.5GB run with timing fix
- **T1** Idempotence pass on 6.9GB output
- **T1** External sha256, wc, stat on output
- **T1** Compute exact comparison percentages
- **T1** Compute comparison percentages with f-strings
- **T1** Run normalized full-corpus ablation
- **T1** Read exact main-run memory and timing fields
- **T1** Direct named budget-impossible refusal
- **T1** Check pycache and git status
- **T1** Collect exact proof and autotest figures
- **T1** Add margin and percentage fields
- **T1** Regenerate autotest and 200MB proof
- **T1** Final 7.5GB pass
- … et 7 autres

## 4. Mesures et résultats marquants

- **T1** `/dev/mapper/system-root   11T  9,0T  1,9T  83% /home/stephane/Data13TB`
- **T1** `-rw-r--r--. 1 stephane stephane       7513 18 nov 11:11 prouve-200Mo.json`
- **T1** `-rw-r--r--. 1 stephane stephane       2237 18 nov 11:11 prouve-200Mo.log`
- **T1** `-rw-r--r--. 1 stephane stephane       1032 18 nov 11:11 prouve-200Mo.out`
- **T1** `-rw-r--r--. 1 stephane stephane  200000000 18 nov 11:11 slice-200Mo-garde.txt`
- **T1** `-rw-r--r--. 1 stephane stephane  200000000 18 nov 10:46 slice-200Mo.txt`
- **T1** `n'est coupée), plus une marge de contexte **après** le bloc (2 % du bloc, au plus`
- **T1** `1 chance sur pas (mesuré : 0,01 % de shingles vus à pas 96 contre 0,24 % avec`
- **T1** `l'ancrage, sur 20 Mo — voir `work/dedup/diagnostic_ancrage.py`). Les hachages sont`
- **T1** `"chemin": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/dedup/slice-200Mo.txt",`
- **T1** `"chemin": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/dedup/slice-200Mo-garde.txt",`
- **T1** `"recouvrement_origine": "2 % du bloc, plafonné à 1 Mio",`
- **T1** `[bloc 1] 0/191 Mio, 0.0% vu, gardé, RSS 63 Mio, 0 s`
- **T1** `[bloc 2] 8/191 Mio, 0.0% vu, gardé, RSS 79 Mio, 1 s`
- **T1** `[bloc 3] 16/191 Mio, 0.1% vu, gardé, RSS 81 Mio, 1 s`
- **T1** `[bloc 4] 24/191 Mio, 0.1% vu, gardé, RSS 90 Mio, 2 s`
- **T1** `[bloc 5] 32/191 Mio, 0.1% vu, gardé, RSS 90 Mio, 2 s`
- **T1** `[bloc 6] 40/191 Mio, 0.0% vu, gardé, RSS 90 Mio, 3 s`
- **T1** `[bloc 7] 48/191 Mio, 0.7% vu, gardé, RSS 90 Mio, 3 s`
- **T1** `[bloc 8] 56/191 Mio, 0.1% vu, gardé, RSS 97 Mio, 4 s`
- **T1** `[bloc 9] 64/191 Mio, 0.1% vu, gardé, RSS 98 Mio, 4 s`
- **T1** `[bloc 10] 72/191 Mio, 1.0% vu, gardé, RSS 107 Mio, 5 s`
- **T1** `[bloc 11] 80/191 Mio, 0.4% vu, gardé, RSS 108 Mio, 5 s`
- **T1** `[bloc 12] 88/191 Mio, 0.7% vu, gardé, RSS 110 Mio, 6 s`
- **T1** `[bloc 13] 96/191 Mio, 0.4% vu, gardé, RSS 111 Mio, 6 s`
- **T1** `[bloc 14] 104/191 Mio, 0.3% vu, gardé, RSS 112 Mio, 6 s`
- **T1** `[bloc 15] 112/191 Mio, 3.8% vu, gardé, RSS 121 Mio, 7 s`
- **T1** `[bloc 16] 120/191 Mio, 6.3% vu, gardé, RSS 121 Mio, 7 s`
- **T1** `[bloc 17] 128/191 Mio, 0.3% vu, gardé, RSS 121 Mio, 8 s`
- **T1** `[bloc 18] 136/191 Mio, 15.9% vu, gardé, RSS 121 Mio, 8 s`
- **T1** `[bloc 19] 144/191 Mio, 7.6% vu, gardé, RSS 121 Mio, 9 s`
- **T1** `[bloc 20] 152/191 Mio, 2.8% vu, gardé, RSS 121 Mio, 9 s`
- **T1** `[bloc 21] 160/191 Mio, 3.7% vu, gardé, RSS 121 Mio, 10 s`
- **T1** `[bloc 22] 168/191 Mio, 1.3% vu, gardé, RSS 121 Mio, 10 s`
- **T1** `[bloc 23] 176/191 Mio, 0.3% vu, gardé, RSS 121 Mio, 11 s`
- **T1** `[bloc 24] 184/191 Mio, 0.6% vu, gardé, RSS 121 Mio, 11 s`
- **T1** `Command being timed: "python3 tools/dedup_blocs.py --entree work/dedup/slice-200Mo.txt --sortie work/dedup/slice-200Mo-garde.txt --bloc-mo 8 --memoire-mo 256 --json work/dedup/prouve-200Mo.json"`
- **T1** `Percent of CPU this job got: 97%`
- **T1** `rec_origine = "2 % du bloc, plafonné à 1 Mio"`
- **T1** `"""Remplace `fraction` des mots par d'autres, dispersés : la copie « 10 % modifiée »."""`
- **T1** `# C : un paragraphe sur dix remplacé → ≈ 9,4 % des octets neufs, uniformément par bloc`
- **T1** `# seuil 0,95 : C (≈ 90 % vu) repasse`
- **T1** `# 10 % dispersé : les shingles sont locaux, la copie est gardée`
- **T1** `"(défaut : 2 %% du bloc, max 1 Mio)")`
- **T1** `lignes déjà vues : 47563661 (53.98 %) ; octets : 621277675 (8.28 %)`
- **T1** `vides          23037969     23037968    100.0%       23037969      23037968    100.0%`
- **T1** `1-19 o         20689727     16900629     81.7%      243994263     187886634     77.0%`
- **T1** `20-79 o        23410695      6825264     29.2%      959609824     216037267     22.5%`
- **T1** `80 o et +      20976041       799800      3.8%     6277436533     194315806      3.1%`
- **T1** `Percent of CPU this job got: 99%`
- **T1** `Percent of CPU this job got: 100%`
- **T1** `entree {"chemin": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/dedup/slice-200Mo.txt", "octets": 200000000, "mtime": "2026-11-18T10:46:48"}`
- **T1** `sortie {"chemin": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/dedup/slice-200Mo-lignes.txt", "octets": 192946503, "sha256": "1ec785b6dab27396cfedbb802883a0777fa11e092b9d1f2e964fcfa4df320222"`
- **T1** `[still running after 60000ms; moved to background job bash-762]`
- **T1** `diag non vides : lignes 24525693 = 27.834 % du total, 37.688 % des non-vides`
- **T1** `diag non vides octets 598239707 = 7.972 %`
- **T1** `equiv lignes 47714201 = 54.150 %`
- **T1** `equiv octets 626531460 = 8.349 %`
- **T1** `200Mo memoire {'budget_mio': 64.0, 'rss_max_mio': 45.7, 'ru_maxrss_mio': 49.3, 'marge_mio': 18.3, 'capacite_slots': 2097152, 'octets_table': 16777216, 'entrees_max': 1677721, 'plancher_mio': 48.0}`
- **T1** `200Mo table {'slots_utilises': 1015997, 'charge_finale': 0.4845, 'entrees_max': 1677721} durees {'duree_s': 4.1, 'duree_passe_s': 3.5, 'duree_verification_s': 0.6, 'debit_mio_s': 53.7, 'debit_total_mi`
- **T1** `200Mo lignes {'lues': 1741349, 'gardees': 1477432, 'ecartees': 263917, 'vides_lues': 461435, 'vides_gardees': 461435, 'non_vides_lues': 1279914, 'non_vides_gardees': 1015997, 'non_vides_ecartees': 263`
- **T1** `[still running after 60000ms; moved to background job bash-776]`
- **T1** `OK   ../work/dedup/prouve-200Mo-lignes.json`
- **T1** `work/dedup/prouve-200Mo-lignes.json OK ok`
- **T1** `## 4. Comparaison aux 53,98 % / 8,28 % du rapport blocs`
- **T1** `150 540) ; ici le hachage est sur 64 bits (≈ 4,4 × 10⁻⁵ collision attendue), donc l'écart`
- **T1** `La tranche de 200 Mo confirme aussi l'avertissement du rapport blocs : elle ne perd que`
- **T1** `**3,527 %** de ses octets (c'est le début du fichier, avec moins de boilerplate), contre`
- **T1** `**8,042 %** sur le fichier entier. Toute mesure sur une tranche **sous-estime**.`
- **T1** `uniques, on attend **4,4 × 10⁻⁵ collision**, soit **0,0044 %** de chance qu'une ligne`
- **T1** `53,98 % (qui supprimaient les vides) ; c'est pourquoi les deux taux sont donnés. Une ligne`
- **T1** `elle peut accueillir 107 374 182 entrées (40,4 M utilisées, **62,4 %** de marge). Avec un`

## 5. Erreurs rencontrées

2 sorties en erreur ou divergentes. Les premières :

- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 2, in <module> FileNotFoundError: [Errno 2] No such file or directory: 'work/dedup/autotest-lignes/autotest.json' [exit code: 1]
- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 6, in <module> TypeError: not enough arguments for format string [exit code: 1]

