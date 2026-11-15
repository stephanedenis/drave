# Session session- — Mesure du tagger sur H50 et delta

> **Journaux :** [le jour](../../2026-11-15/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-2bf7f8da-ddb8-4d2a-a357-4a5fd9847e55` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-15 09:06 |
| Durée | 0.2 h |
| Tours | 1 |
| Messages | 75 |
| Appels d'outils | 91 |
| Fichiers touchés | 0 |
| Commandes | 85 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche W2 (J2 matin) : le tagger sur le split — mesure `evaluer --tagger` sur les 402 (l'entraînement) et sur les 50 H50 (la tenue à l'écart), avec le cache chaud puis l'API ; le POS de l'heuristique et du tagger sur chaque base, le **delta**, le coût par phrase et la latence ; la règle : une règle qui ne gagne que sur H50 est **rejetée**. Fiche `reports/rapport-tagger-h50.md` + JSON. (Si W1 n'a pa … [85 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tâche W2 (J2 matin) : le tagger sur le split — mesure `evaluer --tagger` sur les 402 (l'entraînement) et sur les 50 H50  … [365 caractères tronqués]

*91 appels d'outils.* Actions notables :

- bash — Inspect repo root and git status
- bash — List reports and data directories
- bash — Locate tagger and evaluer code
- bash — Find gold/tagger/H50 reports
- bash — Search W1/W2/H50 references
- bash — Read current state doc
- bash — Find --tagger CLI
- bash — List linguistic tests and read gold 452 report
- bash — Read drave.py header
- bash — Read drave.py evaluer implementation
- bash — Read evaluer command and args
- bash — Read evaluer_gold.py
- bash — Read tagger 612 bench
- bash — Read DeepSeek client and cache
- … et 68 autres

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** Inspect repo root and git status
- **T1** List reports and data directories
- **T1** Locate tagger and evaluer code
- **T1** Find gold/tagger/H50 reports
- **T1** Search W1/W2/H50 references
- **T1** Read current state doc
- **T1** Find --tagger CLI
- **T1** List linguistic tests and read gold 452 report
- **T1** Read drave.py header
- **T1** Read drave.py evaluer implementation
- **T1** Read evaluer command and args
- **T1** Read evaluer_gold.py
- **T1** Read tagger 612 bench
- **T1** Read DeepSeek client and cache
- **T1** Check DeepSeek key and cache presence
- **T1** Inspect gold 452 JSON structure
- **T1** Read tagger option report
- **T1** Inspect prior tagger JSON outputs
- **T1** Extract split ids and composition
- **T1** Inspect gold datasets format
- **T1** Inspect gold_reel_50 script structure
- **T1** Read H50 selection logic
- **T1** Locate tagger classes in bloc_linguistique
- **T1** Read NeuronalLLMPOS implementation
- **T1** Search price references
- **T1** Inspect cost details in prior JSON
- **T1** Read semaine-2 plan
- **T1** Read gold 452 split and controls
- **T1** Read fusion/cascade implementation
- **T1** Locate fusion logic
- **T1** Reproduce H50 split and heuristic metrics
- **T1** Inspect random control draw
- **T1** Search rule wording
- **T1** Inspect W2 plan entry
- **T1** Write W2 bench script draft
- **T1** Fix and install W2 bench script
- **T1** Smoke-test W2 bench on 2 phrases
- **T1** Fix key loading and rerun smoke test
- **T1** Fix per-pass cache dir and rerun smoke
- **T1** Inspect smoke JSON structure
- … et 45 autres

## 4. Mesures et résultats marquants

- **T1** `reports/rapport-gold-452.json:1471:      "lecture": "le tirage au hasard fait 88,13 % de POS ; H50 fait 68,42 % : le lot est un stress test, pas un échantillon."`
- **T1** `reports/rapport-gold-452.json:1804:    "tirage_aleatoire": "graine 20261116 : POS 88,13 %, F1 78,69 %, attachement 100 % ; H50 : 68,42 %, 58,36 %, 95,45 %.",`
- **T1** `reports/rapport-gold-452.md:91:graine donne **88,13 %** de POS, contre **68,42 %** pour H50 : c'est la preuve que H50 est un stress test,`
- **T1** `reports/rapport-gold-452.md:171:**190 segments**, **22 cibles**. H50 fait **11,1 %** des phrases mais porte **37,1 %** des erreurs POS`
- **T1** `reports/rapport-gold-452.md:301:| tirage aléatoire | H50 doit être sous le hasard | **68,42 % vs 88,13 %** (POS) |`
- **T1** `- **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ; page **`/paragraphes`**, **19/19 verdicts `389b99f`** ; **5`
- **T1** `- **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**, **F1 0,7902**, **1 span** ; **`s065`**, **`r035`**, **GV** réglés ; **restitution v1** (46/46) ; **J11.1–J11.4** ([exemples](../../reports/`
- **T1** `- **Panini J7.1** : 532 textes (445 langues) ; hors script, hasard ; famille **66,1 %** / sœur **26,1 %** (hasard 10,3/2,5) ; LANG_TREE : sœurs **0,619** vs **0,0445** (13,9×, p=0,002) ; [fiche](../..`
- **T1** `- **N2 (nuit)** : la distillation tient-elle à 30 000 pas / 122 Mo ? → **non** à parité stricte (erratum) ; la repondération vaut **−0,05**.`
- **T1** `- **R1 (nuit)** : 2 048 à 20 000 pas ? → **oui** : 2×10 000 pas finis (perte 0,9409 → 0,8965 ; PPL 2,614 → 2,4953).`
- **T1** `Le corpus pèse **2 375 tokens** (95,8 % du gold) et **171 cibles** ; le hand pèse **105 tokens** et **13 cibles**.`
- **T1** `graine donne **88,13 %** de POS, contre **68,42 %** pour H50 : c'est la preuve que H50 est un stress test,`
- **T1** `f"· unités sémantiques={len(a.unites_semantiques)} ({a.fraction_semantique:.1%} du texte)"`
- **T1** `> **88,57 % → 97,14 %** sur 20 phrases `hand` (**+8,57 pts**), cohérent avec le **0,9475 contre`
- **T1** `- **Classe tirée au hasard** (12 classes, graine 0) : **10,48 %** ; **classe majoritaire**`
- **T1** `(`VERB`) : **22,86 %**. Le tagger (97,14 %) et l'heuristique (88,57 %) sont très au-dessus :`
- **T1** `docs/archive/biologie-pour-drave.md:394:axes appris suit la même pente (+3,8 % à 384, **+8,0 %** à 512) : le prix de la`
- **T1** `docs/archive/cerveau-facultes.md:190:> * le **prix est stable, le gain ne l'est pas** ✗✓ : perplexité **+148 % et +143 %** selon la graine ✓`
- **T1** `docs/archive/etat-cerveau.md:48:| **C4** | horloges par région | 🟡 premier pas, **et le prix du retard est mesuré** | **un état n'est valide qu'à SA position : un pas de retard coûte ×633** (14,6496 →`
- **T1** `docs/archive/etat-cerveau.md:110:| **E5** | rejeu et distillation · **+ CONFIRMÉ SUR DEUX GRAINES (16/10)** | ✅ **MESURÉE le 14/10 (soir)** | à architecture identique (8 couches + lecteur + LoRA), l'o`
- **T1** `docs/archive/roadmap-detail-2026-10-29.md:45:| A1.1 | **Format de trace** (DRVF v2/v3) : par couche et position, les neurones actifs (indice + valeur) | ✅ | 132 Mo pour 512 jetons (258 ko/jeton) et +8`
- **T1** `docs/pilotage/chantiers.md:89:| **D — les données** (nouveau) | avec quoi entraîne-t-on, et à quel prix ? | ✅ inventaire local ; **10 corpus texte intégral** (20,53 M art., 67,73 G car., 81,2 Go, **8 `
- **T1** `**190 segments**, **22 cibles**. H50 fait **11,1 %** des phrases mais porte **37,1 %** des erreurs POS`
- **T1** `(102/275), **25,1 %** des segments absents (87/346) et **100 %** de l'erreur d'attachement (1/1).`
- **T1** `| tirage aléatoire | H50 doit être sous le hasard | **68,42 % vs 88,13 %** (POS) |`
- **T1** `"lecture": "le tirage au hasard fait 88,13 % de POS ; H50 fait 68,42 % : le lot est un stress test, pas un échantillon."`
- **T1** `| [rapport-familles-9.md](rapport-familles-9.md) | C3.2c — les 9 familles : 7 sur 9 au-dessus de 30 % |`
- **T1** `| [rapport-grappe-intra-couche.md](rapport-grappe-intra-couche.md) | A7.3 — la grappe intra-couche : le top-1024 (21 %) rend la même perplexité |`
- **T1** `> **168 mesures** en **10 parties** (`07/p1.md` … `07/p10.md`), pas un fichier de 150 Ko. La lire **par`
- **T1** `| [`rapport-base-reelle.md`](rapport-base-reelle.md) | **B13** — la base honnête : `--reel`, 452 phrases, POS 88,91 %, F1 79,06 % |`
- **T1** `33:| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)**`
- **T1** `35:| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 langues à 0,9687**, script 1`
- **T1** `363:| **R0.7** | **la couche linguistique** : neuf niveaux (graphème → pragmatique), heuristique CPU + neuronal de contrat, substitution/parallèle/cascade, activation sémantique 51–76 % | ✅ **398 lang`
- **T1** `[still running after 60000ms; moved to background job bash-51]`
- **T1** `| [rapport-modules-famille.md](rapport-modules-famille.md) | C3.2b — un module de restitution par famille : l'indo-européen recopie à 100 % |`
- **T1** `| [rapport-n2-anglais-distille.md](rapport-n2-anglais-distille.md) | N2.n — La distillation anglaise : 4,42 → 3,94, la chaîne complète sur 204 Mo |`
- **T1** `| [rapport-n2-anglais.md](rapport-n2-anglais.md) | N2.m — L'anglais seul : 4,42 sur 204 Mo, et ce que le multilingue coûte (1,6 PPL) |`
- **T1** `| [rapport-n2-canal.md](rapport-n2-canal.md) | N2.l — Le canal de structure : +5 % de PPL, et le même alphabet |`
- **T1** `| [rapport-n2-capacite-reelle.md](rapport-n2-capacite-reelle.md) | N2.j3 — La capacité sur 186 Mo : 21,65 M paie (4,39 → 4,20, et mieux partout) |`
- **T1** `| [rapport-n2-corpus-1go.md](rapport-n2-corpus-1go.md) | N2.aa — Le corpus de 831 Mo à compute constant : un autre domaine, pas plus de savoir |`
- **T1** `| [rapport-n2-corpus-elargi.md](rapport-n2-corpus-elargi.md) | N2.i — Le corpus élargi : 4,84 Mo uniques au lieu de 3,24 |`
- **T1** `| [rapport-n2-corpus-reel.md](rapport-n2-corpus-reel.md) | N2.j — Du vrai français : 186 Mo de Wikipédia, et ce que vaut le filtre « non ambigu » |`
- **T1** `| 01:31 | `ce7241d5` | 6A — LA BASE HONNÊTE : evaluer --reel (452 PHRASES RÉELLES : POS 88,91 %, F1 79,06 %, ATTACHEMENT 99,46 %) ET LA LIGNE BASE RÉELLE DANS LA SORTIE PAR DÉFAUT ; 20 TESTS |`
- **T1** `| 01:39 | `2d7a7f2b` | 1A — LES DEUX DÉFAUTS DU TAGGER CORRIGÉS : 1 APPEL PAR PHRASE (LE TAGGER DE SYNTAGMES RETIRÉ) ET PONCT RESTITUÉ (25/25) ; POS 612 → 95,75 % (+9,5) |`
- **T1** `| 01:42 | `6560a0a5` | 1A — LE TAGGER SUR LA BASE RÉELLE : 88,91 → 95,00 % (+6,1), 449 APPELS SERVIS PAR LE CACHE ; IL GAGNE SURTOUT SUR LE SYNTHÉTIQUE (+9,5 SUR 612) |`
- **T1** `| 01:39 | `2d7a7f2b` | 1A — LES DEUX DÉFAUTS DU TAGGER CORRIGÉS : 1 APPEL PAR PHRASE (LE TAGGER DE SYNTAGMES RETIRÉ) ET PONCT RESTITUÉ (25/25) ; POS 612 → 95,75 % (+9,5) | `en-cours.md`, `README.md`, `
- **T1** `| 01:42 | `6560a0a5` | 1A — LE TAGGER SUR LA BASE RÉELLE : 88,91 → 95,00 % (+6,1), 449 APPELS SERVIS PAR LE CACHE ; IL GAGNE SURTOUT SUR LE SYNTHÉTIQUE (+9,5 SUR 612) | `en-cours.md`, `README.md`, `me`
- **T1** ``0,5270` · `0,092` · `0,160` · `0,811` · `0,657` · `0,440` · `0,429` · `2,7856` · `40,0658` · `95,00 %` · `95,75 %``
- **T1** `| **total** | **17** | **14/17 = 82,35 %** | **16/17 = 94,12 %** | **+2 tokens** |`
- **T1** `450:95,75 %** (**+9,5 pts**) ; sur le **réel 452**, **88,91 % → 95,00 %** (**+6,1 pts**) — le`
- **T1** `[still running after 60000ms; moved to background job bash-71]`

