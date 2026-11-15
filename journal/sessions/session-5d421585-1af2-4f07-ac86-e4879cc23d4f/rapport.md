# Session session- — Rapport manifeste Panini et rejeu protocole

> **Journaux :** [le jour](../../2026-11-15/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-5d421585-1af2-4f07-ac86-e4879cc23d4f` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-15 10:44 |
| Durée | 0.3 h |
| Tours | 1 |
| Messages | 103 |
| Appels d'outils | 132 |
| Fichiers touchés | 0 |
| Commandes | 114 |
| Sous-agents | 0 |
| Commits | 3 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche W4 (J3 matin, la part du pilote) : le manifeste à envoyer à Panini — les **26 signatures manquantes** (la liste des œuvres du §334 sans signature V14), la commande exacte qu'ils doivent lancer, le format attendu ; et le **rejeu des 60 paires** du protocole (`rapport-protocole-date.md`) sur ce qui est disponible, avec le contrôle négatif. Fiche `reports/rapport-panini-manifeste.md` + JSON. ** … [30 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tâche W4 (J3 matin, la part du pilote) : le manifeste à envoyer à Panini — les **26 signatures manquantes** (la liste de … [310 caractères tronqués]

*132 appels d'outils.* Actions notables :

- bash — List root and git state
- grep
- glob
- read
- bash — Inspect protocole JSON structure
- bash — Read protocol tool head
- bash — Outline protocol tool
- bash — Print JSON metadata and a_signer
- bash — Inspect pair/text records
- bash — Locate W4 in plan
- bash — Read week 2 plan
- bash — Read replay implementation
- bash — Check for existing manifest work
- bash — Inspect Panini signatures and state
- … et 105 autres

**Synthèse produite :**

W4 livré et committé : **`93e046f7`**.

\## Livrables

- **Fiche** : [`reports/rapport-panini-manifeste.md`](reports/rapport-panini-manifeste.md)
- **JSON** : [`reports/panini-manifeste.json`](reports/panini-manifeste.json)
- **Script côté Panini** : [`tools/panini_signatures_26.py`](tools/panini_signatures_26.py)
- **Constructeur/rejeu** : [`tools/panini_manifeste.py`](tools/panini_manifeste.py)

\## Le manifeste

Les **26 textes** du protocole B1 sans signature `analytic_sigs_v1` sont listés avec source, SHA-256, mots et paires servies. Point important : **un seul** des 26 (`zadeh_1965`) appartient aux 48 textes des 655 paires §334 ; les 25 autres sont des textes du manifeste des 60 paires hors des 655. Les 3 autres textes §334 sans signature (`an7_64_kodhana`, `aristotle_de_anima`, `brahma_sutra_badarayana`) sont hors protocole et non acquis.

Commande exacte :

```bash
cd /chemin/vers/Panini/research
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  /chemin/vers/Qtrinet/tools/panini_signatures_26.py \
  --manifeste /chemin/vers/Qtrinet/reports/panini-manifeste.json \
  --sortie /tmp/panini-v14-26.json
```

Format : JSON UTF-8, `signatures` = 59 vecteurs (44 de référence + 26 nouvelles), 14 clés exactes, somme = 1 ± 10⁻⁶. **Garde-fou** : si la calibration n’est pas 44/44, les 26 restent dans `nouvelles` et `signatures` ne contient que les 44 références, donc le rejeu B1 reste `incomplet` au lieu de tester sur un instrument non calibré. Testée : elle tourne, sort en code **2** avec `42/44`.

\## Le rejeu disponible

- **27/60 paires** calculées : **G1 1/20**, **G2 14/20**, **G3 12/20** ; **33 manquantes**.
- **Aucune p-value de H0** : noyau choisi par la disponibilité, pas un test.
- Contrôles : N2 (dates permutées G2) `p_perm` **0,252** ; N3 (G3) `p_perm` **0,001**, tiré par `G3-08` (`bengio_2003`, non calibré) ; N4 : l’instrument voit la **famille** sur G2 mais pas la date ; **N5 est vide** (permutation commune des colonnes = isométrie L2).
- **Calibration 42/44** : échecs `bengio_2003` (cos 0,9678) et `mengzi` (cos 0,9891). **3 sources < 300 mots** : `epicurus_letters` (84), `sextus_pyrrho` (42), `zadeh_1965` (278). **5 groupes de doublons** parmi les 26, dont `daodejing`/`zhuangzi` déjà identiques à `qiwulun` ; `G2-15` aura `d_sig = 0`.

**Verdict** : manifeste prêt et envoyable ; **test bloqué** par les 26 signatures et par la calibration 44/44. Rien n’a été modifié chez Panini (statut git des dossiers lus identique, sorties uniquement dans `/tmp`).

\## V
… [432 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** List root and git state
- **T1** Inspect protocole JSON structure
- **T1** Read protocol tool head
- **T1** Outline protocol tool
- **T1** Print JSON metadata and a_signer
- **T1** Inspect pair/text records
- **T1** Locate W4 in plan
- **T1** Read week 2 plan
- **T1** Read replay implementation
- **T1** Check for existing manifest work
- **T1** Inspect Panini signatures and state
- **T1** List pairs and signature status
- **T1** Find V14 extractor scripts
- **T1** Find V14-related files
- **T1** Find references to signature artifact
- **T1** Inspect V14 signature scripts
- **T1** Targeted search for signature artifact
- **T1** List Nipada modules
- **T1** Trace signature artifact history
- **T1** Inspect analytical projection module
- **T1** Inspect corpus cache layout
- **T1** Check signature provenance
- **T1** Search analytics artifact references
- **T1** Find sign_analytic usage
- **T1** Read signature generator script
- **T1** Find corpus-to-signature pipeline
- **T1** Read reports index conventions
- **T1** Inspect documentation review
- **T1** Read W4 plan entry
- **T1** Inspect graph v35 structure
- **T1** Compute complete and missing pairs
- **T1** Check source files for 26
- **T1** Count words in 26 sources
- **T1** Validate 44 signatures
- **T1** Check graph signatures for 26
- **T1** Audit 44 signature sources
- **T1** Find duplicate sources among 26
- **T1** Read corpus selection logic
- **T1** Test Panini extractor on one work
- **T1** Check for Panini venv
- … et 74 autres

## 4. Mesures et résultats marquants

- **T1** `"standardisés |β| ≳ 0,55 (α = 0,05, 80 %) ; les effets plus petits seront bornés par l'IC et "`
- **T1** `[still running after 60000ms; moved to background job bash-15]`
- **T1** `[still running after 60000ms; moved to background job bash-17]`
- **T1** `c71b1b80 §120-§127 — V8_math : extension mathématique-physique + test Penrose 82.2%`
- **T1** `> **168 mesures** en **10 parties** (`07/p1.md` … `07/p10.md`), pas un fichier de 150 Ko. La lire **par`
- **T1** `| [`rapport-base-reelle.md`](rapport-base-reelle.md) | **B13** — la base honnête : `--reel`, 452 phrases, POS 88,91 %, F1 79,06 % |`
- **T1** `| [`rapport-atomes-niveaux.md`](rapport-atomes-niveaux.md) | **Panini** — la table 14 atomes × 8 |`
- **T1** `| [`rapport-pos-ponctuation.md`](rapport-pos-ponctuation.md) | **B13** — PONCT : POS **85,75 %**, miroir |`
- **T1** `| [`rapport-pos-r4-integre.md`](rapport-pos-r4-integre.md) | **B13** — paquet POS sûr, **84,96 %** |`
- **T1** `| [`rapport-pos-anglais-v2.md`](rapport-pos-anglais-v2.md) | **B13** — POS **83,83 %** (R2a/R3/R2b), F1 **0,6181** |`
- **T1** `| [`rapport-cache-chunker-applique.md`](rapport-cache-chunker-applique.md) | **B13** — le cache appliqué : **×139** en |`
- **T1** `| [rapport-a80-porte-delais.md](rapport-a80-porte-delais.md) | A8.0 — `porte-delais` épingle la PPL : 59,0790 à 0 et 50 ms |`
- **T1** `| [rapport-a80-porte-pont.md](rapport-a80-porte-pont.md) | A8.0 — `porte-pont` épingle sa PPL et sa falaise : 113,0068 / 111,9225, +2,81 % / +25,35 % |`
- **T1** `| [rapport-a83-defaut.md](rapport-a83-defaut.md) | A8.3 — le défaut place+perte n'est pas neutre : les portes épinglées bougent de −5,9 % à +19,5 % |`
- **T1** `| [rapport-a83a-coupe.md](rapport-a83a-coupe.md) | A8.3a — `porte-coupe` : le régime 1 % écrase la variance du point de coupe |`
- **T1** `| [rapport-a83a-flux.md](rapport-a83a-flux.md) | A8.3a — `porte-flux` : le régime 1 % a ses propres références |`
- **T1** `| [rapport-a83a-pont.md](rapport-a83a-pont.md) | A8.3a — `porte-pont` : le régime 1 % change la falaise |`
- **T1** `| [rapport-a83d-lot-threads.md](rapport-a83d-lot-threads.md) | A8.3d — le lot n'est pas les threads : l'écart de 1,90 % survit à 1 thread |`
- **T1** `"id": f"{groupe}-{rang:02d}",`
- **T1** `49:- **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ; page **`/paragraphes`**, **19/19 verdicts `389b99f`** ; `
- **T1** `- **Panini** : **14 atomes** ; UDHR **418/438** ; J3.2 **5/21** langues (Glottolog **21/21**), **154/154** hors script au hasard, **V14 3/21** ; B2 **négatif** (niveaux non prédits) ; J7.1 famille **6`
- **T1** `- **N2 (nuit)** : la distillation tient-elle à 30 000 pas / 122 Mo ? → **non** à parité stricte (erratum) ; la repondération vaut **−0,05**.`
- **T1** `- **R1 (nuit)** : 2 048 à 20 000 pas ? → **oui** : 2×10 000 pas finis (perte 0,9409 → 0,8965 ; PPL 2,614 → 2,4953).`
- **T1** `sources acquises ne sont pas 102 URL (71 URL uniques). La loi H0 se reproduit (**R² = 0,909139** sur`
- **T1** `contre null **−0,129**, p=0,335). Sur les 44 signatures, le retrieval brut donne **61,4 %** de même`
- **T1** `tradition et **56,8 %** de voisins à ≤50 ans, mais les contrôles croisés ramènent la filiation à`
- **T1** `**50,0 %** (p=0,0492, Holm 0,128) et l'époque à **53,8 %** (p=0,373) ; seule une petite prédiction`
- **T1** `d'année intra-tradition survit (**R²=0,042**, p=0,0086, Holm 0,034). Le β époque **+0,138** de la v150`
- **T1** `35:| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 langues à 0,9687**, script 1`
- **T1** `38:**État au 14/11 07 h 10.** B13 : **POS 86,25 %**, **attachement exact 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (REL suivie d'un GV → le sujet`
- **T1** `48:**J7.1** sépare la **sœur** de la **famille lointaine** : sur 532 textes Panini (445 langues, 1948), le top-1 est de la même famille **66,1 %** (hasard 10,3 %) et de la même branche **26,1 %** (has`
- **T1** `193:   suivante, jamais l'attente. **N5 est gelé** jusqu'au verdict de R11 sur le contexte ; B10.3 attend un **z qui porte** : l'objectif mot a levé le décodeur (32,5 ; **26,7 sur JW, au-dessus du pla`
- **T1** `211:[B1–B12] lasts 1 day and is 100% complete and is colored in #2e7d32`
- **T1** `212:[B10.2bis] lasts 1 day and is 100% complete and is colored in #2e7d32`
- **T1** `213:[B10.3] lasts 2 days and is 15% complete and is colored in #b03a2e`
- **T1** `214:[B11.10] lasts 1 day and is 100% complete and is colored in #2e7d32`
- **T1** `[still running after 60000ms; moved to background job bash-105]`
- **T1** `[still running after 60000ms; moved to background job bash-112]`

## 5. Erreurs rencontrées

5 sorties en erreur ou divergentes. Les premières :

- **T1** : erreurs.append(f"{p['id']} : paire dupliquée {cle}")         vus.add(cle)         textes.add(a); textes.add(b)     if len(textes) != manifeste["composition"]["textes_distincts"]:         erreurs.appen
- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 5, in <module>   File "/home/stephane/Data13TB/stephane/GitHub/Panini/research/src/nipada/signing/analytical_projection.py", line 35,
- **T1** : research/.venv .venv ./.venv/bin/python /usr/bin/python3 [exit code: 1]
- **T1** : [stderr] Traceback (most recent call last):   File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/panini_manifeste.py", line 559, in <module>     raise SystemExit(main())                      
- **T1** : [stderr] Traceback (most recent call last):   File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/panini_manifeste.py", line 561, in <module>     raise SystemExit(main())                      

## 6. Commits

- SEMAINE 2 — W4 : LE MANIFESTE PANINI (26 SIGNATURES, COMMANDE, FORMAT) ; REJEU 27/60, CALIBRATION 42/44, 3 SOURCES COURTES, CONTRÔLE N5 VIDE" -m "Le manifeste r
- git add reports/rapport-panini-manifeste.md && git commit --amend --no-edit | tail -5; echo exit=${PIPESTATUS[0]}; git log --oneline -1
- python3 - <<'PY' p='docs/pilotage/en-cours.md' s=open(p).read() s=s.replace('**Mis à jour : 2026-11-15, 11 h 05 HNE (W4 : le manifeste Panini et le rejeu dispon

