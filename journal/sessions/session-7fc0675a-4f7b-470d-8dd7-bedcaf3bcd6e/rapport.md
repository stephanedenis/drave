# Session session- — Mesure du tagger en lot sur 1000 phrases

> **Journaux :** [le jour](../../2026-11-15/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-7fc0675a-4f7b-470d-8dd7-bedcaf3bcd6e` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-15 12:53 |
| Durée | 0.7 h |
| Tours | 1 |
| Messages | 226 |
| Appels d'outils | 254 |
| Fichiers touchés | 5 |
| Commandes | 223 |
| Sous-agents | 0 |
| Commits | 2 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche X3 (J5, la part du pilote) : le tagger **en lot** — mesure le coût et la latence pour **1 000 phrases** (réelles, prises dans le gold + les 50 textes libres), le **taux de cache** (chaud/froid), le **débit** (phrases/min), la **mémoire**, et le **coût en dollars** (~0,04 $/612 → extrapoler) ; le mode `--jsonl` sur un fichier ; le **contrôle négatif** (les mêmes phrases en cache chaud ne doiv … [60 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tâche X3 (J5, la part du pilote) : le tagger **en lot** — mesure le coût et la latence pour **1 000 phrases** (réelles,  … [340 caractères tronqués]

*254 appels d'outils.* Actions notables :

- bash — Inspect repository root and git status
- bash — List reports and pilotage docs
- bash — Find tagger references
- read
- bash — Read tagger API test
- bash — Locate tagger command and jsonl
- bash — Read drave.py tagger section
- bash — Read W3 tagger report
- bash — Inspect gold_reel_50 and tagger 612
- bash — Find $0.04 / 612 context
- bash — Find free texts corpus
- bash — List data directories
- bash — Inspect 50 free texts JSON structures
- bash — Read tagger 612 harness
- … et 217 autres

**Synthèse produite :**

X3 est fait, mesuré, écrit et committé (`2929ccf7`).

**Source des 50 textes libres.** J’ai pris le **banc de robustesse** `reports/pensee-fiabilite-produit.json` (`banc_50.resultats`), qui est le banc canonique des « 50 textes libres » (50 textes, 2 vides, 2 refus, 1 068 mots). Il fournit **69 phrases**. Avec le gold 612, le corpus réel fait **681 lignes / 677 textes distincts** (4 doublons). Le lot de 1 000 items ajoute **319 répétitions déterministes** : ce sont des phrases réelles, mais **677 textes distincts seulement** — le coût à 1 000 textes uniques est extrapolé (×1,4771), et c’est dit dans la fiche.

| mesure | froid | chaud |
|---|---:|---:|
| items | 1 000 | 1 000 |
| requêtes réseau | **672** | **0** |
| rejeux disque / mémoire | 3 / 323 | 675 / 323 |
| refus sans appel | 2 | 2 |
| tokens | **99 971** | **0** |
| durée | **685,2 s** | **2,635 s** |
| débit | **87,6 items/min** | **22 770 items/min** |
| pic RSS | **40,8 Mo** | **38,2 Mo** |
| cache disque | 712 943 o / 672 fichiers | inchangé |
| refus | 4 (3 items) | 4 |
| hashes identiques | — | **1 000 / 1 000** |

**Coût.** Lot mesuré : **0,021770 $** hors pointe. Extrapolé à 1 000 textes uniques : **0,032157 $** hors pointe, **0,064315 $** en pointe. La référence `0,04 $/612 → 0,065359 $` est retrouvée en pointe ; le hors-pointe est moitié moindre parce que la référence était à **deux appels/phrase**, alors que le câblage actuel en fait **un**. Le chiffre W3 (143 870 tokens / 0,031 $) est confirmé à **+2,6 %**.

**Contrôle négatif.** Les mêmes 1 000 items en cache chaud : **0 réseau, 0 token, 0 $**, **1 000/1 000 hashes identiques**, 4 refus identiques. Les 3 rejeux disque du froid sont trois collisions de prompt (ponctuation ignorée), pas un cache chaud ; les 2 refus sans appel (`f14` « 🚀 », `f17` « ... ») ne sont ni réseau ni cache.

**`--jsonl`.** **1 003 lignes** pour 1 000 items (3 phrases du gold contiennent deux phrases). Premier passage chaud : 4 prompts absents du cache, **513 tokens** ; second passage : **0 réseau, 0 token**. Passsage froid de 20 items : **20 appels, 2 907 tokens, 18,9 s**.

**Fichiers.**
- [`reports/rapport-tagger-lot.md`](reports/rapport-tagger-lot.md)
- [`reports/rapport-tagger-lot.json`](reports/rapport-tagger-lot.json)
- [`tools/tests/linguistique/qualifier_tagger_lot.py`](tools/tests/linguistique/qualifier_tagger_lot.py) (`--libres fiabilite|produit`, modes `froid`, `chaud`, `fusion`)

**Portes.** `porte-bloc-linguistique`, `porte-produit`, `porte-deepseek
… [466 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/qualifier_tagger_lot.py` | 1 | 5 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-tagger-lot.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md` | 0 | 6 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-15/README.md` | 0 | 1 |

### Commandes exécutées (échantillon)

- **T1** Inspect repository root and git status
- **T1** List reports and pilotage docs
- **T1** Find tagger references
- **T1** Read tagger API test
- **T1** Locate tagger command and jsonl
- **T1** Read drave.py tagger section
- **T1** Read W3 tagger report
- **T1** Inspect gold_reel_50 and tagger 612
- **T1** Find $0.04 / 612 context
- **T1** Find free texts corpus
- **T1** List data directories
- **T1** Inspect 50 free texts JSON structures
- **T1** Read tagger 612 harness
- **T1** Inspect banc_50 structure
- **T1** Inspect detail entry
- **T1** Search for 1000-sentence builders
- **T1** Inspect gold files
- **T1** Inspect free texts length
- **T1** Gold corpus stats
- **T1** Find X3/J5 task definition
- **T1** Search roadmap for tagger/J5
- **T1** Search session plans for X3
- **T1** Search reports for 1000 sentences task
- **T1** Inspect candidate session digests
- **T1** Inspect free texts in fiabilite
- **T1** Inspect gold_gele
- **T1** Find JSON files with phrases
- **T1** Search 1000 phrase corpus references
- **T1** Gold gele sources
- **T1** Search plan.json for X3
- **T1** Read X1-X3 task specs
- **T1** Inspect work dir recent files
- **T1** Check git changes and ignore
- **T1** Check DeepSeek key availability
- **T1** Inspect caches
- **T1** Read W2 report and H50 source
- **T1** Read H50 harness beginning
- **T1** Map H50 harness functions
- **T1** Read cache and measurement machinery
- **T1** Count sentences in 50 free texts
- … et 183 autres

## 4. Mesures et résultats marquants

- **T1** `f"· unités sémantiques={len(a.unites_semantiques)} ({a.fraction_semantique:.1%} du texte)"`
- **T1** `| **coût 1 000 phrases** | `evaluer --tagger --json` (2 phrases identiques, transport factice) | **0** | `cout_pour_1000_phrases` | extrapolation par phrase (×500) | `TestMatriceW3.test_cout_pour_1000`
- **T1** `> **88,57 % → 97,14 %** sur 20 phrases `hand` (**+8,57 pts**), cohérent avec le **0,9475 contre`
- **T1** `- **Classe tirée au hasard** (12 classes, graine 0) : **10,48 %** ; **classe majoritaire**`
- **T1** `(`VERB`) : **22,86 %**. Le tagger (97,14 %) et l'heuristique (88,57 %) sont très au-dessus :`
- **T1** `./reports/rapport-produit-bloc-l.md:149:syntagme (51,9 %)** sont impliquées, dans **31/50 textes** ; 113 sont des **inclusions**, 19 des`
- **T1** `./reports/rapport-produit-bloc-l.md:159:**graphème** : 49/50 textes à 100 %, x46 à **95,14 %** (7 newlines, catégorie `Cc`, non couvertes).`
- **T1** `./reports/rapport-robustesse-produit.md:25:- **132 paires** de syntagmes qui se chevauchent (31/50 textes, **51,9 % des étiquettes**) : le`
- **T1** `gnBKIix4ApwYYhC9xA6YCAxJ00HR3TPTUkbDezYrX6NypMj3t3Xg70rE/N+ofoyhmvroXtW6MV1ykx3kvTHFYOv0IyaHHjW4Z/bwE3zqlgbaiEfn77F8yUEfA3qOEKehZMIisln1AzmADDAAT/5jbVCg/sTC9XUsnFA3HgP+V+LUO8ugB9zvnXqXvPgBb9dez/j95+g2`
- **T1** `na6YOBCUBSrIqTTwrCA97fhvUH/bN6tLLl6DtJrnh93pWEM3NlI6UYdCkrsoYWx7eUu9Ud5sB0oMmQr/KtOA9dofL0H53eVMfNIV674yTwXu9/+be6td/ZB15/9v9/HqPkRx2LEnkKUrlqgrSO3eMWwqRMVmElsw2JijAdbCzdIMWzhFP+e1elIo3QtADkoExwyCPICq`
- **T1** `33:| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)**`
- **T1** `363:| **R0.7** | **la couche linguistique** : neuf niveaux (graphème → pragmatique), heuristique CPU + neuronal de contrat, substitution/parallèle/cascade, activation sémantique 51–76 % | ✅ **398 lang`
- **T1** `reports/rapport-a83c-lot.md:5:> chemin jeton par jeton, **+3,2 %** sur le chemin par lots. La « non-monotonie » d'A8.3b`
- **T1** `reports/rapport-coherence-docs.md:245:| PÉRIMÉ | **38** | version du format de flux et du disque (7) · nombre de flux à 40 et 1 024 jetons (2) · en-têtes 26 et 39 octets (3) · octets par flux, par lot`
- **T1** `reports/rapport-etat-a.md:71:| **A8.3d** | expliqué | A8.3c | **1,90 %** à **1** et **8** threads | `THREADS=1/8 LOT=1/4` | ce n'est pas le pool, c'est le **noyau par lots** |`
- **T1** `7078:3. **La dégradation avec la longueur n'est pas un bug du moteur** : llama.cpp, mêmes 2 048 identifiants, un seul lot, YaRN déclaré → **714,83** contre **722,56** chez nous (1,1 %). Le `--ppl-prof`
- **T1** `7080:4. **Plan 1 M** : `docs/contexte-long.md` + `--plan --ctx N` qui chiffre tout. Les trois murs : **préremplissage séquentiel** (4,5 h à 32 k, 31 h à 128 k, **1 234 h à 1 M** → chantier n° 1, il fa`
- **T1** `8471:⏵ GEMM : **×2,42 à 16 jetons** sur une matrice réelle. J'écris le forward par lots`
- **T1** `1657:| Pilote + 15 noyaux PTX sm_75 | API CUDA brute, PTX compilé par clang | M | `gpu.rs:40, 187-347`, `drave-core/gpu/` | 2× Quadro RTX 5000 16 Go ; NVLink 25,781 Go/s/sens |`
- **T1** `149:syntagme (51,9 %)** sont impliquées, dans **31/50 textes** ; 113 sont des **inclusions**, 19 des`
- **T1** `159:**graphème** : 49/50 textes à 100 %, x46 à **95,14 %** (7 newlines, catégorie `Cc`, non couvertes).`
- **T1** `| graphème, mot | ✅ | 0 crash, 0 span hors texte, `valeur = texte[debut:fin]` à **100 %**, couverture **49/50 à 100 %** (x46 : 95,14 %, newlines) |`
- **T1** `**27 326 tokens de sortie** (totaux à ±0,5 % près, six prompts dupliqués).`
- **T1** `| 01:31 | `ce7241d5` | 6A — LA BASE HONNÊTE : evaluer --reel (452 PHRASES RÉELLES : POS 88,91 %, F1 79,06 %, ATTACHEMENT 99,46 %) ET LA LIGNE BASE RÉELLE DANS LA SORTIE PAR DÉFAUT ; 20 TESTS |`
- **T1** `| 01:39 | `2d7a7f2b` | 1A — LES DEUX DÉFAUTS DU TAGGER CORRIGÉS : 1 APPEL PAR PHRASE (LE TAGGER DE SYNTAGMES RETIRÉ) ET PONCT RESTITUÉ (25/25) ; POS 612 → 95,75 % (+9,5) |`
- **T1** `| 01:42 | `6560a0a5` | 1A — LE TAGGER SUR LA BASE RÉELLE : 88,91 → 95,00 % (+6,1), 449 APPELS SERVIS PAR LE CACHE ; IL GAGNE SURTOUT SUR LE SYNTHÉTIQUE (+9,5 SUR 612) |`
- **T1** `> **168 mesures** en **10 parties** (`07/p1.md` … `07/p10.md`), pas un fichier de 150 Ko. La lire **par`
- **T1** `| [`rapport-base-reelle.md`](rapport-base-reelle.md) | **B13** — la base honnête : `--reel`, 452 phrases, POS 88,91 %, F1 79,06 % |`
- **T1** `| [`rapport-atomes-niveaux.md`](rapport-atomes-niveaux.md) | **Panini** — la table 14 atomes × 8 |`
- **T1** `| [`rapport-pos-ponctuation.md`](rapport-pos-ponctuation.md) | **B13** — PONCT : POS **85,75 %**, miroir |`
- **T1** `"extrapole_note": "×1.5038 (1000 / 665 textes distincts)",`
- **T1** `COUT: {"tokens": {"prompt_tokens": 83880, "completion_tokens": 15088, "total_tokens": 98968, "prompt_cache_hit_tokens": 0, "prompt_cache_miss_tokens": 83880, "tokens_reseau": 98968, "tokens_cache": 39`
- **T1** `192:(8,65 Mo pour 1 003 lignes) : 8 340 lignes/min au premier passage (4 appels réseau), 19 577 au`
- **T1** `24:| [`rapport-tagger-lot.md`](rapport-tagger-lot.md) | **X3/R0.7** — le tagger **en lot** : **1 000 items** (665 textes), **662 appels réseau**, **98 968 tokens**, **690,4 s**, **86,9 items/min**, **`
- **T1** `- **Note** : l'attachement est à **236/237 (0,9916)**, la couverture 0,9916, POS **86,25 %**, F1 **0,7535**, 2 spans ; la seule rouge est`
- **T1** `> appels réseau** à froid, **98 968 tokens**, **690,4 s**, **86,9 items/min**, **40,8 Mo** de`
- **T1** `— **33,8 %** des items ne sont pas facturés ; **98 968 tokens** (83 880 d'entrée + 15 088 de`
- **T1** `sortie), **690,4 s**, **86,9 items/min**, pic **40,8 Mo**, cache disque **703 720 octets** en`
- **T1** `pic **37,9 Mo** : le contrôle négatif est **exact**, et les **1 000 hashes** d'annotation sont`
- **T1** `1 000 textes uniques est une **extrapolation** (×1,5038), et le lot à 1 000 items est la`
- **T1** `linéairement (×1,5038). Les 160 phrases `synth` du gold sont conservées parce que la consigne`
- **T1** `| **cache total (disque + mémoire)** | **338 / 1 000 = 33,8 %** |`
- **T1** `**Lecture.** Le cache **froid** n'est pas « 0 % » au sens strict : **3 items** sont servis par`
- **T1** `**2 textes distincts sur 665** (0,3 %), tous deux des textes libres longs (URL, e-mail,`
- **T1** `| cache total | 33,8 % | **100 %** |`
- **T1** `| **disque seul** (items servis par un fichier) | 3 / 1 000 = **0,3 %** | 665 / 1 000 = **66,5 %** |`
- **T1** `| **mémoire seule** (texte déjà vu dans la cascade) | 335 / 1 000 = **33,5 %** | 335 / 1 000 = **33,5 %** |`
- **T1** `| **total** (disque + mémoire) | 338 / 1 000 = **33,8 %** | 1 000 / 1 000 = **100 %** |`
- **T1** `| **API prompt cache** (`prompt_cache_hit_tokens`) | **0 / 83 880 = 0 %** | 0 (aucun appel) |`
- **T1** `**Lecture.** Le cache **disque** chaud est à **66,5 %**, pas 100 % : les **335 répétitions** du`
- **T1** `est à 100 % et le coût à 0. Le cache **côté API** (`prompt_cache_hit_tokens`) est **vide** sur`
- **T1** `(8,65 Mo pour 1 003 lignes) : 8 340 lignes/min au premier passage (4 appels réseau), 19 577 au`
- **T1** `garde que les métriques et un hash par item). Le cache disque pèse **0,7 Mo**, soit ~1 058`
- **T1** `octets par texte. Le `--jsonl` à 1 003 lignes pèse **8,65 Mo** sur `stdout` (le sous-processus`
- **T1** `| poste | 1 000 items (mesuré) | 1 000 textes uniques (extrapolé ×1,5038) |`
- **T1** `le 15/11). Le chiffre W3 (**143 870 tokens / 0,031 $ pour 1 000**) est donc **confirmé à +3,4 %**`
- **T1** `à 1 000 textes uniques est extrapolé (×1,5038). Si les 335 textes manquants sont plus longs`
- **T1** `cache disque pèse 0,7 Mo.`
- **T1** `+| [`rapport-tagger-lot.md`](rapport-tagger-lot.md) | **X3/R0.7** — le tagger **en lot** : **1 000 items** (665 textes), **662 appels réseau**, **98 968 tokens**, **690,4 s**, **86,9 items/min**, **40`
- **T1** `25:- **132 paires** de syntagmes qui se chevauchent (31/50 textes, **51,9 % des étiquettes**) : le`
- **T1** `"extrapole_note": "×1.4771 (1000 / 677 textes distincts)",`
- **T1** `0 'Le corpus réel disponible fait 665 textes distincts : 1 000 items = 665 + 335 répétitions ; le coût des 1 000 textes uniques est extrapolé (×1,5038).'`
- **T1** `reports/README.md:24:| [`rapport-tagger-lot.md`](rapport-tagger-lot.md) | **X3/R0.7** — le tagger **en lot** : **1 000 items** (677 textes), **672 appels réseau**, **99 971 tokens**, **685,2 s**, **87`
- **T1** `6:> appels réseau** à froid, **99 971 tokens**, **685,2 s**, **87,6 items/min**, **40,8 Mo** de`

## 5. Erreurs rencontrées

3 sorties en erreur ou divergentes. Les premières :

- **T1** : gold 612 unique texts 609 dups [(('Le vent souffle fort.', 'fr'), 2), (('La voiture roule vite.', 'fr'), 2), (('Paul sees Marie; he speaks to her.', 'en'), 2)] n 3 free sentences 56 unique 56 [stderr]
- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 16, in <module> ValueError: not enough values to unpack (expected 4, got 3) [exit code: 1]
- **T1** : tokens/network 148.8 [stderr] Traceback (most recent call last):   File "<stdin>", line 5, in <module> KeyError: 'corpus' [exit code: 1]

## 6. Commits

- SEMAINE 2 — X3 : LE TAGGER EN LOT (1 000 ITEMS, 662 APPELS RÉSEAU, 98 968 TOKENS, 0,0216 \$ ; CACHE CHAUD 0 \$, 1 000/1 000 HASHES) ; --JSONL 1 003 LIGNES" 2>&1
- SEMAINE 2 — X3 CORRIGÉ : LES 50 TEXTES LIBRES SONT LE BANC DE ROBUSTESSE (1 000 ITEMS, 677 TEXTES, 672 APPELS, 99 971 TOKENS, 0,02177 \$ ; CACHE CHAUD 0 \$, 1 0

