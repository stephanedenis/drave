# Session session- — Rédiger le rapport de coordination N2 v2

> **Journaux :** [le jour](../../2026-11-15/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-6b564867-141f-4839-907b-f75a14b99ccd` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-15 02:03 |
| Durée | 0.2 h |
| Tours | 1 |
| Messages | 61 |
| Appels d'outils | 93 |
| Fichiers touchés | 4 |
| Commandes | 58 |
| Sous-agents | 0 |
| Commits | 1 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche C1 : la coordination N2, suite de J4.1 — écris `reports/rapport-coordination-n2-v2.md` + JSON : la commande **validée** `python3 work/n2ac/eval_longueurs.py --rope --canal-dir <dir>` (le correctif mesuré 2,79), la commande à ne PAS utiliser (`--rope` seul : 40,07), le test de non-régression proposé (`porte-n2.sh` : la porte à 3,09 doit rester à 3,09), et la mise à jour de la ligne N2 de `doc … [78 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tâche C1 : la coordination N2, suite de J4.1 — écris `reports/rapport-coordination-n2-v2.md` + JSON : la commande **vali … [358 caractères tronqués]

*93 appels d'outils.* Actions notables :

- bash — List repo structure and relevant dirs
- bash — Check git status and recent log
- bash — Find N2-related reports, tools, scripts
- bash — Find N2 line in en-cours
- read
- bash — Search for J4.1 and key figures
- bash — Search for porte-n2 and J4.1 references
- bash — Read plan.json C1 context
- bash — Check tools/n2 and canal-dir usages
- bash — Read existing v1 JSON
- bash — Search prior work on v2
- bash — Read en-cours N2 section
- bash — Check eval_n2_propre current options
- bash — Check file timestamps and modifications
- … et 73 autres

**Synthèse produite :**

All checks pass. I'll commit only the five C1 files (explicit paths), then re-verify the state.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2-v2.md` | 1 | 6 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2-v2.json` | 1 | 5 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md` | 0 | 12 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md` | 0 | 1 |

### Commandes exécutées (échantillon)

- **T1** List repo structure and relevant dirs
- **T1** Check git status and recent log
- **T1** Find N2-related reports, tools, scripts
- **T1** Find N2 line in en-cours
- **T1** Search for J4.1 and key figures
- **T1** Search for porte-n2 and J4.1 references
- **T1** Read plan.json C1 context
- **T1** Check tools/n2 and canal-dir usages
- **T1** Read existing v1 JSON
- **T1** Search prior work on v2
- **T1** Read en-cours N2 section
- **T1** Check eval_n2_propre current options
- **T1** Check file timestamps and modifications
- **T1** Check GPU and eval_longueurs CLI
- **T1** Read en-cours header
- **T1** Verify artifacts exist
- **T1** Test whether --canal-dir is accepted
- **T1** Replay validated RoPE+canal measurement
- **T1** Replay 3.09 absolute control
- **T1** Replay test-split 1024 measurement
- **T1** Inspect charge_rope signature
- **T1** Find charge_rope definition
- **T1** Reproduce 40.07 control without canal
- **T1** Run documentation review baseline
- **T1** Inspect reports README/INDEX
- **T1** Read documentation review checks
- **T1** Rest of documentation review
- **T1** Find 3.09 in gate report
- **T1** Inspect index generator
- **T1** Check index freshness and counts
- **T1** Confirm argparse exit code for canal-dir
- **T1** Read gate report header
- **T1** Inspect patched /tmp tool options
- **T1** Replay patched eval_n2_propre canal-dir
- **T1** Replay 1024 for determinism
- **T1** Locate lines to edit in en-cours
- **T1** Regenerate index and validate JSON
- **T1** Run documentation review after edits
- **T1** Validate en-cours state
- **T1** Check document size budget
- … et 18 autres

## 4. Mesures et résultats marquants

- **T1** `6560a0a5 1A — LE TAGGER SUR LA BASE RÉELLE : 88,91 → 95,00 % (+6,1), 449 APPELS SERVIS PAR LE CACHE ; IL GAGNE SURTOUT SUR LE SYNTHÉTIQUE (+9,5 SUR 612)`
- **T1** `2d7a7f2b 1A — LES DEUX DÉFAUTS DU TAGGER CORRIGÉS : 1 APPEL PAR PHRASE (LE TAGGER DE SYNTAGMES RETIRÉ) ET PONCT RESTITUÉ (25/25) ; POS 612 → 95,75 % (+9,5)`
- **T1** `ce7241d5 6A — LA BASE HONNÊTE : evaluer --reel (452 PHRASES RÉELLES : POS 88,91 %, F1 79,06 %, ATTACHEMENT 99,46 %) ET LA LIGNE BASE RÉELLE DANS LA SORTIE PAR DÉFAUT ; 20 TESTS`
- **T1** `134:- **N2 (nuit)** : la distillation tient-elle à 30 000 pas / 122 Mo ? → **non** à parité stricte (erratum) ; la repondération vaut **−0,05**.`
- **T1** `journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/rapport.md:2174:**Attention** : l'hypothèse « relecture du cache KV » a été **réfutée** par la mesure (chemin groupé par tête KV : 3,20 → 3,27 ms)`
- **T1** `journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md:6461:non structuré         1    5.0%  59.08% |    1.05    2.64    2.79   2.00 |     0.29    20.15`
- **T1** `journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md:10543:- Qwen2.5-0.5B measures: real Q8_0 494 M weights, density 99.2%, E[|v|]=42.79, E[popcount]=3.13; Q4_0 E[|v|]=3.02, E[popcount]=1.3`
- **T1** `journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md:10881:threads=8      100.0%       4303745  fusion   3.09 G (1.3949 ms) | 2-listes   3.23 G (1.3307 ms)`
- **T1** `journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md:10885:threads=40      100.0%       4303745  fusion   1.54 G (2.7994 ms) | 2-listes   1.52 G (2.8268 ms)`
- **T1** `journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md:10897:threads=40      100.0%       4303745  fusion   1.54 G (2.7924 ms) | 2-listes   1.54 G (2.7859 ms)`
- **T1** `journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md:11233:2. **`&mut` dans la boucle chaude** : 3,09 → 0,97 G év/s à 8 threads, simple barrière d'aliasing. Corrigé en variables locales.`
- **T1** `journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md:21895:**Attention** : l'hypothèse « relecture du cache KV » a été **réfutée** par la mesure (chemin groupé par tête KV : 3,20 → 3,27 ms)`
- **T1** `journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:32955:> d'aliasing : 3,09 → 0,97 G év/s), et la **sursouscription** de l'attente active`
- **T1** `journal/sessions/4b146dfd-ce0b-4af8-910f-610ab438d4e6/rapport.md:102:- **T1** `> d'aliasing : 3,09 → 0,97 G év/s), et la **sursouscription** de l'attente active``
- **T1** `journal/sessions/4b146dfd-ce0b-4af8-910f-610ab438d4e6/digest.md:454:> d'aliasing : 3,09 → 0,97 G év/s), et la **sursouscription** de l'attente active`
- **T1** `journal/sessions/4e786d3f-0b66-4b23-8dc4-b452bc383bea/digest.md:1525:> d'aliasing : 3,09 → 0,97 G év/s), et la **sursouscription** de l'attente active`
- **T1** `journal/sessions/5c1bbea7-1d14-47b6-a48c-fea15f2b857e/rapport.md:216:- **T1** `> d'aliasing : 3,09 → 0,97 G év/s), et la **sursouscription** de l'attente active``
- **T1** `journal/sessions/3d5618a0-4e3a-45bb-943d-a72c753fb7da/digest.md:1401:- `:7-11` — « densité : **99.2 %** » ; « niveaux distincts : **256** » ; « `E[|v|]` : **42.79** » ; « `E[popcount(|v|)]` : **3.13**`
- **T1** `journal/sessions/3d5618a0-4e3a-45bb-943d-a72c753fb7da/digest.md:2148:- `:176-192` — «| scores `q·k` | **2,10 ms** | **0,65 ms** | / | **total** | **3,09** | **1,57** |» ; «(2,10 → 2,16 ms)» ; «En AVX2`
- **T1** `journal/sessions/3d5618a0-4e3a-45bb-943d-a72c753fb7da/digest.md:2550:**optimisations.md** — :4 « 4864 entrées × 896 sorties, **4 303 745 événements** » · :6 « 2 × Xeon E5-2687W v3 (20 cœurs / 40 CPU l`
- **T1** `journal/sessions/3d5618a0-4e3a-45bb-943d-a72c753fb7da/digest.md:2636:- `reports/rapport-optimisations.md:105` — « chuter le débit de 3,09 à 0,97 G év/s (8 threads) » et `:121` — « `yield_now()` ... a `
- **T1** `journal/sessions/56879594-1434-4e34-83cc-de42cdf192a1/digest.md:1422:- `reports/rapport-mur-memoire-4bits.md:176-192` — «| scores `q·k` | **2,10 ms** | **0,65 ms** | / | softmax | 0,28 | 0,27 | / | so`
- **T1** `journal/sessions/8549abcb-5d9a-4594-915b-5628c80a2a08/digest.md:1063:- `:105` — « chuter le débit de 3,09 à 0,97 G év/s (8 threads) »`
- **T1** `journal/sessions/8549abcb-5d9a-4594-915b-5628c80a2a08/digest.md:1568:- `reports/rapport-optimisations.md:105` — « chuter le débit de 3,09 à 0,97 G év/s (8 threads) » et `:121` — « `yield_now()` après `
- **T1** `journal/sessions/d31b3d9b-58e4-4d34-85fa-381b6f6a6a76/digest.md:4812:=== perplexité 353877796603.0974 sur 127 tokens (0 événements, 0.1 s) ===`
- **T1** `./reports/rapport-native-capacite-egal.md:46:d'entraînement domine** (+26 % pour le 11,47 M entraîné). La porte N2 (**PPL < 2,5**) reste hors de portée à 5 000 pas.`
- **T1** `[still running after 60000ms; moved to background job bash-8]`
- **T1** `"protocole": "validation data/corpus_propre/val.txt, fenêtres Van der Corput dans les chunks de 8192, 8 lots × 16 fenêtres",`
- **T1** `- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/239 (0,9958)**, **F1 0,7902**, **1 span** ; **`s065`** et **`r035`** réglés, **convention des GV** ; **restitution v1** (46/46 canoniq`
- **T1** `- **Panini J7.1** : 532 textes (445 langues) ; hors script, hasard ; famille **66,1 %** / sœur **26,1 %** (hasard 10,3/2,5) ; LANG_TREE : sœurs **0,619** vs **0,0445** (13,9×, p=0,002) ; [fiche](../..`
- **T1** `- **N2 (nuit)** : la distillation tient-elle à 30 000 pas / 122 Mo ? → **non** à parité stricte (erratum) ; la repondération vaut **−0,05**.`
- **T1** `- **R1 (nuit)** : 2 048 à 20 000 pas ? → **oui** : 2×10 000 pas finis (perte 0,9409 → 0,8965 ; PPL 2,614 → 2,4953).`
- **T1** `[still running after 60000ms; moved to background job bash-13]`
- **T1** `0, Quadro RTX 5000, 1 MiB, 16384 MiB, 0 %`
- **T1** `1, Quadro RTX 5000, 1 MiB, 16384 MiB, 0 %`
- **T1** `**Mis à jour : 2026-11-15, 01 h 50 HNE (tagger : 95,75 % sur 612, 95,00 % sur le réel 452)**`
- **T1** `- **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ; page **`/paragraphes`**, **banque 9 paragraphes** ; **56 te`
- **T1** `> **168 mesures** en **10 parties** (`07/p1.md` … `07/p10.md`), pas un fichier de 150 Ko. La lire **par`
- **T1** `| [`rapport-base-reelle.md`](rapport-base-reelle.md) | **B13** — la base honnête : `--reel`, 452 phrases, POS 88,91 %, F1 79,06 % |`
- **T1** `| [`rapport-atomes-niveaux.md`](rapport-atomes-niveaux.md) | **Panini** — la table 14 atomes × 8 |`
- **T1** `| [`rapport-pos-ponctuation.md`](rapport-pos-ponctuation.md) | **B13** — PONCT : POS **85,75 %**, miroir |`
- **T1** `| [`rapport-pos-r4-integre.md`](rapport-pos-r4-integre.md) | **B13** — paquet POS sûr, **84,96 %** |`
- **T1** `| [rapport-a80-porte-delais.md](rapport-a80-porte-delais.md) | A8.0 — `porte-delais` épingle la PPL : 59,0790 à 0 et 50 ms |`
- **T1** `| [rapport-a80-porte-pont.md](rapport-a80-porte-pont.md) | A8.0 — `porte-pont` épingle sa PPL et sa falaise : 113,0068 / 111,9225, +2,81 % / +25,35 % |`
- **T1** `reports/rapport-n2-porte-propre.md:18:corpus dédupliqué, split par chunks, **0 % de fuite**). La chaîne honnête y valait **3,0904** avec`
- **T1** `> fenêtre est le **seul bras dont la courbe descend avec la longueur** : à octets égaux (33 Mo),`
- **T1** `> **capacité ne ferme pas la porte** : à fenêtre 512, init aléatoire et 33 Mo vus, 11,47 M donne`
- **T1** `corpus dédupliqué, split par chunks, **0 % de fuite**). La chaîne honnête y valait **3,0904** avec`
- **T1** `- **Deux bras à octets égaux** (33 Mo vus), RoPE, 34,3 M, lot 8, lr 3e-4, graine 1, init`
- **T1** `18:corpus dédupliqué, split par chunks, **0 % de fuite**). La chaîne honnête y valait **3,0904** avec`
- **T1** `75:   validation. C'est **moins** que les 0,59 de N2.h, et c'est obtenu avec **33 Mo vus** — 8 000`
- **T1** `3:**Mis à jour : 2026-11-15, 01 h 50 HNE (tagger : 95,75 % sur 612, 95,00 % sur le réel 452)**`
- **T1** `-**Mis à jour : 2026-11-15, 01 h 50 HNE (tagger : 95,75 % sur 612, 95,00 % sur le réel 452)**`
- **T1** `+**Mis à jour : 2026-11-15, 02 h 15 HNE (tagger : 95,75 % sur 612, 95,00 % sur le réel 452 ; N2 : commande validée, 2,7856)**`

## 5. Erreurs rencontrées

1 sorties en erreur ou divergentes. Les premières :

- **T1** : total 208 drwxr-xr-x. 1 stephane stephane   686  6 nov 09:52 . drwxr-xr-x. 1 stephane stephane  2532  5 nov 10:41 .. -rw-r--r--. 1 stephane stephane  9977  3 nov 09:19 AGENTS.md drwxr-xr-x. 1 stephane

## 6. Commits

- C1 — LA COMMANDE N2 VALIDÉE : --rope + canal (2,7856), JAMAIS --rope SEUL (40,0658), TÉMOIN 3,09" -- reports/rapport-coordination-n2-v2.md reports/rapport-coord

