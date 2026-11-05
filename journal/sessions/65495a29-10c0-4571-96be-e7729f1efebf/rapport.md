# Session 65495a29 — Tu travailles dans le dépôt

> **Journaux :** [le jour](../../2026-11-05/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `65495a29-10c0-4571-96be-e7729f1efebf` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-05 13:16 |
| Durée | 1.2 h |
| Tours | 1 |
| Messages | 80 |
| Appels d'outils | 93 |
| Fichiers touchés | 1 |
| Commandes | 85 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **mesurer le coût** des règles d'attachement récentes dans `tools/bloc_linguistique.py` et proposer un correctif de cache, sans modifier le fichier.  Contexte : dans `Heuristique.analyser`, le chemin des syntagmes appelle `self._syntagmes_simple(texte, lg)` **à l'intérieur** de la boucle s … [1817 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **mesurer  … [2097 caractères tronqués]

*93 appels d'outils.* Actions notables :

- bash — Show git status, branch, and root files
- bash — Count lines and list reports dir
- grep
- bash — Show file header
- read
- bash — Find charger and 612 references
- bash — Show rest of analyser and nearby
- bash — Find all charger functions
- bash — Find 612 references
- bash — Inspect qualifier_syntagmes charger
- bash — Inspect evaluer_gold and qualifier_cascade chargers
- bash — Count gold sentences across loaders
- bash — Look for existing chunker reports
- bash — Inspect phrase structure
- … et 78 autres

**Synthèse produite :**

⏵ Livraison du rapport et du JSON, avec état git à reprendre

**Livrables créés** (aucun fichier existant modifié par moi, aucun commit de ma part) :
- `reports/rapport-cout-chunker.md` — fiche complète (verdict, protocole, tableaux, complexité, correctif, contrôle négatif, limites)
- `reports/pensee-cout-chunker.json` — données structurées, JSON valide

**Mesures** (instantané `6e8430…`, contenu de HEAD, Xeon, temps CPU, passes entrelacées) :

| | corpus 612 | 20 | 40 | 80 | 160 | 320 |
|---|---:|---:|---:|---:|---:|---:|
| chunker seul, original (ms) | 231,4 | 1,75 | 5,04 | 17,29 | 64,82 | 238,00 |
| chunker seul, cache V2 (ms) | 196,6 | 0,73 | 1,31 | 2,57 | 5,58 | 14,10 |
| défaut S, original (ms) | 394,4 | 1,98 | 4,23 | 9,89 | 27,83 | 88,38 |
| défaut S, cache V2 (ms) | 367,6 | 1,58 | 2,99 | 6,08 | 13,94 | 36,88 |

- **Complexité** : pente log-log 1,74 (chunker, 20-160) et 1,27 (défaut), montant à 1,94 / 1,86 sur 160-1 280. `_syntagmes_simple` est appelé **1+2S** fois en chunker (97 à 160, 193 à 320 ; 3,21/phrase sur le corpus), mais **2 fois** seulement en défaut. Le vrai coût défaut est `_verbe_dans` : 2 320 appels pour 32 GV distincts à 160, 8 736 pour 64 à 320.
- **Gain du cache V2** : **×11,6 à 160** et **×16,9 à 320** en chunker ; **×2,0 / ×2,4** en défaut ; ×33 à 1 280 en chunker, plateau ×3,3-3,6 en défaut. Corpus court : ×1,18 / ×1,07 seulement.
- **Correctif proposé** (pseudo-code dans la fiche, non appliqué) : hoister `simples`/`gvs_simple` (lignes 853-941), ajouter un `cache_gv` local et `_verbe_gv`, remplacer les appels 681/685/701 et passer `cache_gv` aux sites 887/895/899/916/922/935/940. Sortie identique V1/V2/OFF : **612/612** + **10/10 textes longs**.
- **Limite** : le `sorted(gvs, key=ecart)` par segment reste ; le cache ne rend pas la courbe strictement linéaire. V3 (index+bisect) et V4 (tri fusionné) testés, plus lents, non retenus ; V3 avait 1 divergence/612.

**État git à reprendre** : le commit concurrent `2e08cbc7` a committé une version **antérieure** de mes deux fichiers. L'arbre de travail contient les corrections finales (référence `9d5337ce`, plages corpus, typo ; 22 insertions/20 suppressions vs HEAD), mais `git add` a échoué sur `.git/index.lock` (processus git actif). Il faut re-`git add` les deux fichiers avant le prochain commit ; je n'ai ni commité ni touché au lock.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-cout-chunker.md` | 1 | 3 |

### Commandes exécutées (échantillon)

- **T1** Show git status, branch, and root files
- **T1** Count lines and list reports dir
- **T1** Show file header
- **T1** Find charger and 612 references
- **T1** Show rest of analyser and nearby
- **T1** Find all charger functions
- **T1** Find 612 references
- **T1** Inspect qualifier_syntagmes charger
- **T1** Inspect evaluer_gold and qualifier_cascade chargers
- **T1** Count gold sentences across loaders
- **T1** Look for existing chunker reports
- **T1** Inspect phrase structure
- **T1** Check S generator path and simple chunks
- **T1** Time both paths and count calls on 612
- **T1** Test simple chunker on candidate bases
- **T1** Check repeated base segments and GVs
- **T1** Validate 10-token base across lengths
- **T1** Time both paths on growing repeated sentences
- **T1** Profile chunker-only 160 tokens
- **T1** Profile default path 160 tokens
- **T1** Prototype cache subclass and verify identical output
- **T1** Validate V2 cache on functions and output equality
- **T1** Inspect Annotation and helper sets
- **T1** Show Annotation dataclass fields
- **T1** Run full cost benchmark
- **T1** Inspect counters and corpus gains
- **T1** Isolate chunker and V2 costs at larger N
- **T1** Profile V2 residual hotspots at 320/640
- **T1** Run interleaved robust benchmark
- **T1** Measure V3 pre-sorted index variant
- **T1** Find the V3 semantic divergence
- **T1** Debug V3 candidate ordering on failing sentence
- **T1** Inspect GV verb detection and POS tags
- **T1** Count GV verbs scanned per segment
- **T1** Compare auxiliary-only vs full-verb base sensitivity
- **T1** Test fused proximity variant V4
- **T1** Profile residual V2 default cost at 640/1280
- **T1** Read an existing report format
- **T1** Inspect pensee JSON schema
- **T1** Extract all key figures
- … et 45 autres

## 4. Mesures et résultats marquants

- **T1** `segmenter_s=False: original=228.8 ms | V1=247.6 ms (x0.92) | V2=188.1 ms (x1.22) | OFF=251.1 ms (x0.91)`
- **T1** `segmenter_s=True: original=436.8 ms | V1=405.9 ms (x1.08) | V2=386.6 ms (x1.13) | OFF=449.0 ms (x0.97)`
- **T1** `opt=False N= 20: orig=1.63 ms | V1=0.85 ms | V2=0.67 ms | OFF=1.63 ms`
- **T1** `opt=False N= 40: orig=4.66 ms | V1=1.75 ms | V2=1.20 ms | OFF=4.79 ms`
- **T1** `opt=False N= 80: orig=15.57 ms | V1=4.15 ms | V2=2.36 ms | OFF=15.73 ms`
- **T1** `opt=False N=160: orig=64.18 ms | V1=15.52 ms | V2=7.40 ms | OFF=63.22 ms`
- **T1** `opt=False N=320: orig=234.26 ms | V1=34.69 ms | V2=12.67 ms | OFF=247.21 ms`
- **T1** `opt=True N= 20: orig=2.24 ms | V1=3.26 ms | V2=3.04 ms | OFF=3.32 ms`
- **T1** `opt=True N= 40: orig=4.00 ms | V1=3.85 ms | V2=2.72 ms | OFF=3.92 ms`
- **T1** `opt=True N= 80: orig=15.03 ms | V1=9.34 ms | V2=5.93 ms | OFF=13.09 ms`
- **T1** `opt=True N=160: orig=33.48 ms | V1=26.07 ms | V2=13.25 ms | OFF=26.48 ms`
- **T1** `opt=True N=320: orig=90.68 ms | V1=90.16 ms | V2=34.86 ms | OFF=92.27 ms`
- **T1** `opt=False: original=226.7ms x1.00 | V1=195.7ms x1.16 | V2=190.3ms x1.19 | OFF=228.3ms x0.99`
- **T1** `opt=True: original=389.3ms x1.00 | V1=381.0ms x1.02 | V2=372.3ms x1.05 | OFF=394.7ms x0.99`
- **T1** `opt=False N= 20: original=1.63ms x1.00 | V1=0.86ms x1.89 | V2=0.69ms x2.38 | OFF=1.64ms x0.99`
- **T1** `opt=False N= 40: original=4.84ms x1.00 | V1=1.79ms x2.70 | V2=1.21ms x4.00 | OFF=4.76ms x1.02`
- **T1** `opt=False N= 80: original=15.71ms x1.00 | V1=4.18ms x3.76 | V2=2.44ms x6.45 | OFF=15.76ms x1.00`
- **T1** `opt=False N=160: original=61.20ms x1.00 | V1=11.09ms x5.52 | V2=5.23ms x11.69 | OFF=57.76ms x1.06`
- **T1** `opt=False N=320: original=233.65ms x1.00 | V1=36.48ms x6.41 | V2=12.34ms x18.93 | OFF=263.18ms x0.89`
- **T1** `opt=True N= 20: original=1.86ms x1.00 | V1=1.83ms x1.02 | V2=1.50ms x1.24 | OFF=1.88ms x0.99`
- **T1** `opt=True N= 40: original=3.96ms x1.00 | V1=3.83ms x1.03 | V2=2.76ms x1.43 | OFF=3.97ms x1.00`
- **T1** `opt=True N= 80: original=9.66ms x1.00 | V1=9.17ms x1.05 | V2=5.62ms x1.72 | OFF=9.49ms x1.02`
- **T1** `opt=True N=160: original=25.49ms x1.00 | V1=25.06ms x1.02 | V2=12.34ms x2.07 | OFF=25.73ms x0.99`
- **T1** `opt=True N=320: original=88.96ms x1.00 | V1=83.22ms x1.07 | V2=32.83ms x2.71 | OFF=95.74ms x0.93`
- **T1** `opt=False N=  20: original=1.86ms x1.00 | V2=0.71ms x2.61 | V3=0.73ms x2.56`
- **T1** `opt=False N=  40: original=4.74ms x1.00 | V2=1.25ms x3.79 | V3=1.32ms x3.59`
- **T1** `opt=False N=  80: original=16.31ms x1.00 | V2=2.49ms x6.56 | V3=2.71ms x6.02`
- **T1** `opt=False N= 160: original=71.57ms x1.00 | V2=5.55ms x12.91 | V3=6.57ms x10.90`
- **T1** `opt=False N= 320: original=252.89ms x1.00 | V2=13.54ms x18.68 | V3=16.02ms x15.78`
- **T1** `opt=False N= 640: original=989.78ms x1.00 | V2=35.66ms x27.75 | V3=48.58ms x20.37`
- **T1** `opt=False N=1280: original=3844.42ms x1.00 | V2=109.05ms x35.25 | V3=143.35ms x26.82`
- **T1** `opt=True N=  20: original=3.30ms x1.00 | V2=2.41ms x1.37 | V3=2.50ms x1.32`
- **T1** `opt=True N=  40: original=3.97ms x1.00 | V2=2.82ms x1.41 | V3=2.83ms x1.40`
- **T1** `opt=True N=  80: original=10.60ms x1.00 | V2=6.50ms x1.63 | V3=6.23ms x1.70`
- **T1** `opt=True N= 160: original=26.99ms x1.00 | V2=14.36ms x1.88 | V3=14.18ms x1.90`
- **T1** `opt=True N= 320: original=85.26ms x1.00 | V2=33.93ms x2.51 | V3=42.02ms x2.03`
- **T1** `opt=True N= 640: original=306.67ms x1.00 | V2=99.99ms x3.07 | V3=101.80ms x3.01`
- **T1** `opt=True N=1280: original=1170.93ms x1.00 | V2=393.85ms x2.97 | V3=396.65ms x2.95`
- **T1** `opt=False N=  20: original=1.88ms x1.00 | V2=0.74ms x2.52 | V3=0.80ms x2.34`
- **T1** `opt=False N=  40: original=4.63ms x1.00 | V2=1.23ms x3.76 | V3=1.32ms x3.51`
- **T1** `opt=False N=  80: original=16.78ms x1.00 | V2=2.43ms x6.92 | V3=2.61ms x6.42`
- **T1** `opt=False N= 160: original=57.01ms x1.00 | V2=5.37ms x10.62 | V3=5.97ms x9.55`
- **T1** `opt=False N= 320: original=238.72ms x1.00 | V2=13.75ms x17.36 | V3=15.27ms x15.64`
- **T1** `opt=False N= 640: original=987.77ms x1.00 | V2=38.41ms x25.72 | V3=44.11ms x22.39`
- **T1** `opt=False N=1280: original=3834.43ms x1.00 | V2=107.20ms x35.77 | V3=157.06ms x24.41`
- **T1** `opt=True N=  20: original=1.98ms x1.00 | V2=1.50ms x1.32 | V3=1.50ms x1.32`
- **T1** `opt=True N=  40: original=4.08ms x1.00 | V2=4.18ms x0.98 | V3=3.51ms x1.16`
- **T1** `opt=True N=  80: original=9.26ms x1.00 | V2=5.72ms x1.62 | V3=5.75ms x1.61`
- **T1** `opt=True N= 160: original=26.33ms x1.00 | V2=13.90ms x1.89 | V3=18.51ms x1.42`
- **T1** `opt=True N= 320: original=88.70ms x1.00 | V2=32.91ms x2.69 | V3=34.19ms x2.59`
- **T1** `opt=True N= 640: original=310.70ms x1.00 | V2=96.07ms x3.23 | V3=104.16ms x2.98`
- **T1** `opt=True N=1280: original=1140.39ms x1.00 | V2=333.37ms x3.42 | V3=326.76ms x3.49`
- **T1** `opt=False N=  20: original=1.60ms x1.00 | V2=0.68ms x2.36 | V3=0.74ms x2.17`
- **T1** `opt=False N=  40: original=5.02ms x1.00 | V2=1.24ms x4.05 | V3=1.30ms x3.85`
- **T1** `opt=False N=  80: original=15.36ms x1.00 | V2=2.44ms x6.30 | V3=2.61ms x5.88`
- **T1** `opt=False N= 160: original=61.64ms x1.00 | V2=5.45ms x11.30 | V3=6.16ms x10.01`
- **T1** `opt=False N= 320: original=230.59ms x1.00 | V2=12.65ms x18.23 | V3=15.07ms x15.30`
- **T1** `opt=False N= 640: original=946.70ms x1.00 | V2=38.01ms x24.91 | V3=44.28ms x21.38`
- **T1** `opt=False N=1280: original=3700.94ms x1.00 | V2=124.83ms x29.65 | V3=149.15ms x24.81`
- **T1** `opt=True N=  20: original=2.02ms x1.00 | V2=1.64ms x1.23 | V3=1.66ms x1.22`
- **T1** `opt=True N=  40: original=4.14ms x1.00 | V2=2.92ms x1.42 | V3=3.01ms x1.38`
- **T1** `opt=True N=  80: original=10.24ms x1.00 | V2=6.23ms x1.64 | V3=6.33ms x1.62`
- **T1** `opt=True N= 160: original=30.42ms x1.00 | V2=13.95ms x2.18 | V3=14.10ms x2.16`
- **T1** `opt=True N= 320: original=102.01ms x1.00 | V2=40.06ms x2.55 | V3=39.80ms x2.56`
- **T1** `opt=True N= 640: original=322.17ms x1.00 | V2=103.36ms x3.12 | V3=106.99ms x3.01`
- **T1** `opt=True N=1280: original=1172.48ms x1.00 | V2=323.81ms x3.62 | V3=328.67ms x3.57`
- **T1** `N 160 orig 61.68ms V2 9.83ms gain x6.27`
- **T1** `N 320 orig 235.91ms V2 12.73ms gain x18.53`
- **T1** `N 160 orig 26.53ms V2 23.58ms gain x1.13`
- **T1** `N 320 orig 88.88ms V2 32.14ms gain x2.77`
- **T1** `N 160 orig 87.80ms V2 4.49ms gain x19.54`
- **T1** `N 320 orig 323.82ms V2 9.88ms gain x32.77`
- **T1** `N 160 orig 16.07ms V2 11.61ms gain x1.38`
- **T1** `N 320 orig 28.74ms V2 24.83ms gain x1.16`
- **T1** `N 160 orig 54.25ms V2 4.23ms gain x12.81`
- **T1** `N 320 orig 227.90ms V2 9.80ms gain x23.25`
- **T1** `N 160 orig 8.51ms V2 8.11ms gain x1.05`
- **T1** `N 320 orig 18.76ms V2 16.13ms gain x1.16`
- **T1** `opt=False N= 20: original=1.66ms x1.00 | V2=0.70ms x2.38 | V4=0.85ms x1.96`
- **T1** `opt=False N= 40: original=4.81ms x1.00 | V2=1.34ms x3.58 | V4=2.09ms x2.30`
- **T1** `opt=False N= 80: original=17.20ms x1.00 | V2=2.61ms x6.58 | V4=4.96ms x3.47`
- **T1** `opt=False N=160: original=67.14ms x1.00 | V2=5.44ms x12.34 | V4=15.46ms x4.34`
- **T1** `opt=False N=320: original=234.86ms x1.00 | V2=17.06ms x13.77 | V4=57.16ms x4.11`
- **T1** `opt=True N= 20: original=1.90ms x1.00 | V2=1.46ms x1.30 | V4=1.73ms x1.09`
- **T1** `opt=True N= 40: original=3.93ms x1.00 | V2=2.71ms x1.45 | V4=3.21ms x1.22`
- **T1** `opt=True N= 80: original=9.11ms x1.00 | V2=5.55ms x1.64 | V4=7.66ms x1.19`
- **T1** `opt=True N=160: original=26.50ms x1.00 | V2=13.83ms x1.92 | V4=22.47ms x1.18`
- **T1** `opt=True N=320: original=84.45ms x1.00 | V2=33.45ms x2.52 | V4=74.59ms x1.13`
- **T1** `original cpu=  226.7ms min=  219.1 gain=1.000`
- **T1** `V1       cpu=  195.7ms min=  192.4 gain=1.158`
- **T1** `V2       cpu=  190.3ms min=  184.2 gain=1.191`
- **T1** `OFF      cpu=  228.3ms min=  221.6 gain=0.993`
- **T1** `original cpu=  389.3ms min=  383.0 gain=1.000`
- **T1** `V1       cpu=  381.0ms min=  370.1 gain=1.022`
- **T1** `V2       cpu=  372.3ms min=  356.2 gain=1.045`
- **T1** `OFF      cpu=  394.7ms min=  383.2 gain=0.986`
- **T1** `N= 20: original=1.629ms x1.000 | V1=0.860ms x1.894 | V2=0.685ms x2.377 | OFF=1.642ms x0.992`
- **T1** `N= 40: original=4.837ms x1.000 | V1=1.793ms x2.698 | V2=1.210ms x3.998 | OFF=4.761ms x1.016`
- **T1** `N= 80: original=15.711ms x1.000 | V1=4.177ms x3.761 | V2=2.437ms x6.447 | OFF=15.761ms x0.997`
- **T1** `N=160: original=61.203ms x1.000 | V1=11.090ms x5.519 | V2=5.235ms x11.692 | OFF=57.760ms x1.060`
- **T1** `N=320: original=233.653ms x1.000 | V1=36.478ms x6.405 | V2=12.341ms x18.932 | OFF=263.181ms x0.888`
- **T1** `N= 20: original=1.861ms x1.000 | V1=1.830ms x1.017 | V2=1.495ms x1.244 | OFF=1.876ms x0.992`
- **T1** `N= 40: original=3.956ms x1.000 | V1=3.825ms x1.034 | V2=2.759ms x1.434 | OFF=3.968ms x0.997`
- **T1** `N= 80: original=9.657ms x1.000 | V1=9.165ms x1.054 | V2=5.622ms x1.718 | OFF=9.486ms x1.018`
- **T1** `N=160: original=25.492ms x1.000 | V1=25.056ms x1.017 | V2=12.337ms x2.066 | OFF=25.731ms x0.991`
- **T1** `N=320: original=88.959ms x1.000 | V1=83.222ms x1.069 | V2=32.831ms x2.710 | OFF=95.745ms x0.929`
- **T1** `corpus opt=False: original=230.6ms x1.00 | V1=197.2ms x1.17 | V2=189.4ms x1.22 | OFF=228.7ms x1.01`
- **T1** `corpus opt=True: original=385.1ms x1.00 | V1=371.8ms x1.04 | V2=396.0ms x0.97 | OFF=402.4ms x0.96`
- **T1** `opt=False N= 20: original=1.75ms x1.00 | V1=0.93ms x1.87 | V2=0.73ms x2.40 | OFF=1.75ms x1.00`
- **T1** `opt=False N= 40: original=5.04ms x1.00 | V1=1.95ms x2.58 | V2=1.31ms x3.83 | OFF=5.58ms x0.90`
- **T1** `opt=False N= 80: original=17.29ms x1.00 | V1=4.51ms x3.83 | V2=2.57ms x6.73 | OFF=16.39ms x1.05`
- **T1** `opt=False N=160: original=64.82ms x1.00 | V1=11.80ms x5.49 | V2=5.58ms x11.61 | OFF=57.61ms x1.13`
- **T1** `opt=False N=320: original=238.00ms x1.00 | V1=34.80ms x6.84 | V2=14.09ms x16.89 | OFF=233.01ms x1.02`
- **T1** `opt=True N= 20: original=1.98ms x1.00 | V1=1.92ms x1.03 | V2=1.58ms x1.26 | OFF=1.99ms x0.99`
- **T1** `opt=True N= 40: original=4.23ms x1.00 | V1=4.10ms x1.03 | V2=2.99ms x1.41 | OFF=4.19ms x1.01`
- **T1** `opt=True N= 80: original=9.89ms x1.00 | V1=9.62ms x1.03 | V2=6.08ms x1.63 | OFF=9.82ms x1.01`
- **T1** `opt=True N=160: original=27.83ms x1.00 | V1=26.71ms x1.04 | V2=13.94ms x2.00 | OFF=28.41ms x0.98`
- **T1** `opt=True N=320: original=88.38ms x1.00 | V1=89.73ms x0.99 | V2=36.88ms x2.40 | OFF=89.10ms x0.99`
- **T1** `opt=False N= 640: orig=957.9ms V2=37.1ms x25.82`
- **T1** `opt=False N=1280: orig=3748.7ms V2=112.1ms x33.43`
- … (tronqué)

## 5. Erreurs rencontrées

4 sorties en erreur ou divergentes. Les premières :

- **T1** : [(0, 2, 'Le', 'mot'), (3, 7, 'chat', 'mot'), (8, 10, 'de', 'mot'), (11, 13, 'la', 'mot'), (14, 21, 'voisine', 'mot'), (22, 25, 'est', 'mot'), (26, 29, 'sur', 'mot'), (30, 32, 'le', 'mot'), (33, 37, 't
- **T1** : [stderr] fatal: Unable to create '/home/stephane/Data13TB/stephane/GitHub/Qtrinet/.git/index.lock': File exists.  Another git process seems to be running in this repository, or the lock file may be st
- **T1** : fatal: Unable to create '/home/stephane/Data13TB/stephane/GitHub/Qtrinet/.git/index.lock': File exists.  Another git process seems to be running in this repository, or the lock file may be stale [exit
- **T1** : fatal: Unable to create '/home/stephane/Data13TB/stephane/GitHub/Qtrinet/.git/index.lock': File exists.  Another git process seems to be running in this repository, or the lock file may be stale [exit

