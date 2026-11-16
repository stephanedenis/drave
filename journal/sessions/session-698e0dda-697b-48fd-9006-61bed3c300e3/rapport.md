# Session session- — Rédiger le guide de démarrage

> **Journaux :** [le jour](../../2026-11-15/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-698e0dda-697b-48fd-9006-61bed3c300e3` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-15 22:16 |
| Durée | 0.3 h |
| Tours | 1 |
| Messages | 146 |
| Appels d'outils | 167 |
| Fichiers touchés | 7 |
| Commandes | 131 |
| Sous-agents | 0 |
| Commits | 1 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche T3 (exploitable, 3/5) : **le quickstart** — écris `docs/produit/demarrage.md` (le clone, l'install T1, les 3 commandes, la sortie attendue, le JSON, le tagger optionnel, les 3 erreurs courantes et leur code) ; vérifie **chaque commande** en la rejouant (le texte et la sortie réels) ; ajoute le lien dans `docs/produit/README.md` et `docs/README.md` ; le **contrôle négatif** : un débutant sans … [98 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tâche T3 (exploitable, 3/5) : **le quickstart** — écris `docs/produit/demarrage.md` (le clone, l'install T1, les 3 comma … [378 caractères tronqués]

*167 appels d'outils.* Actions notables :

- bash — List repository root and docs/produit
- bash — Read product and docs READMEs
- bash — Find T1/T3 task references
- bash — Read current state
- bash — Find T1 install task context
- bash — Recent sessions and commits
- bash — Inspect T1-T2 and plan commits
- bash — Find plan file
- bash — Read plan JSON
- bash — Search T3 context in journals
- bash — Search git log and status
- bash — Read T1-T5 plan table in digest
- bash — Show T tasks with acceptance
- bash — Read T1 report and JSON
- … et 142 autres

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/demarrage.md` | 2 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md` | 0 | 4 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/README.md` | 0 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/.gitignore` | 0 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-quickstart.md` | 1 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md` | 0 | 9 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-15/README.md` | 0 | 1 |

### Commandes exécutées (échantillon)

- **T1** List repository root and docs/produit
- **T1** Read product and docs READMEs
- **T1** Find T1/T3 task references
- **T1** Read current state
- **T1** Find T1 install task context
- **T1** Recent sessions and commits
- **T1** Inspect T1-T2 and plan commits
- **T1** Find plan file
- **T1** Read plan JSON
- **T1** Search T3 context in journals
- **T1** Search git log and status
- **T1** Read T1-T5 plan table in digest
- **T1** Show T tasks with acceptance
- **T1** Read T1 report and JSON
- **T1** Read result method
- **T1** Read T1 negative control and product intro
- **T1** Find product README sections
- **T1** Check version and CLI help
- **T1** Find exit code handling
- **T1** Read analyser and main
- **T1** Read main function
- **T1** Read end of main
- **T1** Search plan details for quickstart
- **T1** Check remote URL and key presence
- **T1** Check public HTTPS clone
- **T1** Check branch and existing venv
- **T1** Check remote branch state
- **T1** Clean clone and editable install
- **T1** Replay version, analyser, evaluer cleanly
- **T1** Check local analyzer output and T2 diff
- **T1** Diff clean clone vs local files
- **T1** Inspect installed package resolution
- **T1** Test HOME effect on analysis
- **T1** Diff whole trees
- **T1** Diff tools directory
- **T1** Diff test linguistic data
- **T1** Cross-run scripts and cwd
- **T1** Compare with fresh bytecode cache
- **T1** Check roles vocabulary and remaining diffs
- **T1** Check DRAVE and Python env vars
- … et 91 autres

## 4. Mesures et résultats marquants

- **T1** `attachement 99,46 %). Les chiffres de la fiche v12 (0,6511/0,6482, 235/236) sont **datés** : ils`
- **T1** `langue=fr script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (61.5% du texte)`
- **T1** `POS         exactitude 86.25 %  (fermé 93.73 %, ouvert 79.18 %)`
- **T1** `SYNTAGMES   F1 79.02 %  (P 78.60 % / R 79.44 %)`
- **T1** `tête      F1 90.29 %  (P 92.61 % / R 88.08 %)`
- **T1** `vue linéaire (partition filtrer) F1 81.44 %  · attachement 93.72 % de couverture`
- **T1** `ATTACHEMENT exact 99.58 % · couverture 99.58 % · exact sur span 100.00 % · top-k 98.74 %`
- **T1** `tête      couverture 100.00 % · top-k 99.16 %`
- **T1** `PRAGMATIQUE acte 99.67 % · négation 97.71 % · modalité 98.86 % · double sens 94.44 %`
- **T1** `FRACTION SÉMANTIQUE 54.76 %`
- **T1** `CONTRÔLE NÉGATIF cible exacte tirée au hasard 1.67 % (graine 0, 239 cibles)`
- **T1** `**Lecture.** `exact 99.58 %` est le **rendement** (238/239 cibles) ; `exact sur span 100.00 %` est`
- **T1** ``--gold` mesure le gold gelé 602 (F1 78,82 %, POS 86,25 %). La commande sort **0** : elle ne`
- **T1** `POS 94.51 % (fermé 98.30 %, ouvert 90.54 %) · SYNTAGMES F1 86.56 % (tête 95.27 %)`
- **T1** `ATTACHEMENT exact 98.86 % · couverture 98.86 % · top-k 98.86 % · PRAGMATIQUE acte 99.52 %`
- **T1** `CONTRÔLE NÉGATIF cible exacte tirée au hasard 2.27 % (graine 0, 88 cibles)`
- **T1** `POS 81.59 % (fermé 90.92 %, ouvert 73.25 %) · SYNTAGMES F1 74.75 % (tête 87.33 %)`
- **T1** `ATTACHEMENT exact 100.00 % · couverture 100.00 % · top-k 98.68 % · PRAGMATIQUE acte 99.75 %`
- **T1** `CONTRÔLE NÉGATIF cible exacte tirée au hasard 1.99 % (graine 0, 151 cibles)`
- **T1** `POS (94,51 % contre 81,59 %) et en syntagmes (F1 86,56 % contre 74,75 %) ; l'attachement est`
- **T1** `**Lecture.** Le porteur `REL [22:42]` est le **rang 2** d'un groupe de **3** segments ; ses deux`
- **T1** `alternatives sont au rang 1 (la REL longue `[22:54]`, qui le **contient** : `inclus`) et au rang 3`
- **T1** `fidélité    : exacte 1.0000 · caractères 1.0000 · couverture 100.00%`
- **T1** `mots        : exacte 0.0000 · caractères 0.9286 · couverture 84.62%`
- **T1** `pos         : exacte 0.0000 · caractères 0.9286 · couverture 84.62%`
- **T1** `**88,91 %**, F1 **79,06 %**, attachement **99,46 %**. Sans lui, `evaluer` publie la ligne`
- **T1** `langue=fr script=Latn source=cascade · 20 étiquettes · unités sémantiques=2 (61.5% du texte)`
- **T1** `**La mesure.** Sur les **20 phrases `hand`** du gold (105 tokens) : POS **88,57 % → 97,14 %**`
- **T1** `(**+8,57 pts**), syntagmes et attachement **inchangés**. Sur le **gold 612** : **86,25 % →`
- **T1** `95,75 %** (**+9,5 pts**) ; sur le **réel 452**, **88,91 % → 95,00 %** (**+6,1 pts**) — le`
- **T1** `SYNTAGMES   F1 78.82 %  (P 78.18 % / R 79.46 %)`
- **T1** `tête      F1 90.25 %  (P 92.34 % / R 88.26 %)`
- **T1** `**86,25 % à 95,75 %** (**+9,5 pts**) ; sur le réel 452, de **88,91 % à 95,00 %** (**+6,1**).`
- **T1** `**1,67 %** ; l'audit v10 ajoute un **candidat aléatoire** dans les listes (**42,14 %** de top-1)`
- **T1** `et une **permutation des cibles** (**0,908 %**). La mesure est **in-sample** : les règles ont`
- **T1** `base réelle 452, **183/184 (99,46 %)**. Détail : [`rapport-g017.md`](../../reports/rapport-g017.md).`
- **T1** `| **la performance du cache** (×139, conditions) | [`reports/rapport-cache-chunker-applique.md`](../../reports/rapport-cache-chunker-applique.md) |`
- **T1** `docs/pilotage/chantiers.md:90:| **B13 — le moteur de pensée** | penser est-il une recherche tracée sur des états pluriels ? | ✅ state store v0 + AC-3/alpha-bêta + **DRVF `thought`** + **banc anytime**`
- **T1** `docs/pilotage/plan-travail.md:39:| **L/B13 — Pensée (session `e181ce02`)** | le bloc langue (contrat heuristique + neuronal), la cascade, la pragmatique ; B13 | L, B13, la couche heuristique | **CPU**`
- **T1** `docs/pilotage/plan-travail.md:195:   **0,7539**, acte **1,0**) ; **DRVM/native** par la règle (**3 nœuds**) ; **DRVM N0.1 6/6** ; **pragmatique 130 : 1,0 / 1,0 / 0,9846 / 0,9769** — elle qualifie ; **`
- **T1** `docs/pilotage/roadmap.md:288:| **B13** | le **moteur de pensée** : RSN plurielle, arbre d'états, anytime | ✅ **state store v0** + moteur + **AC-3/alpha-bêta** + **DRVF `thought`** + **banc anytime** +`
- **T1** `reports/archive/rapport-campagne-benefices.md:2104:blocs à 97,7 % d'activité, **1 096 à 50 %** (§31). Un contrôle au démarrage ne pourrait`
- **T1** `reports/campagne-benefices/035-32-budget-doctets-par-lien-c10-declare-et-v.md:11:blocs à 97,7 % d'activité, **1 096 à 50 %** (§31). Un contrôle au démarrage ne pourrait`
- **T1** `reports/traduction-eurlex-7b.json:309:    "sortie": "(27) Pour faciliter la mise en œuvre du plan, la Commission et chaque État membre concerné devraient conclure un arrangement opérationnel détaillan`
- **T1** `reports/traduction-eurlex-3b.json:309:    "sortie": "Pour faciliter la mise en œuvre du plan, la Commission et chaque État membre concerné devraient entamer une arrangement opérationnel comportant des`
- **T1** `reports/traduction-eurlex-1.5b.json:309:    "sortie": "Pour faciliter l'application du plan, la Commission et chaque État membre concerné devraient entrer en un accord opérationnel avec des détails su`
- **T1** `reports/traduction-eurlex-14b.json:309:    "sortie": "(Afin de faciliter la mise en œuvre du plan, la Commission et chaque État membre concerné devraient conclure un accord opérationnel comportant des`
- **T1** `reports/traduction-langues-7b.json:188:    "sortie": "(27) Pour faciliter la mise en œuvre du plan, la Commission et chaque État membre concerné devraient conclure un arrangement opérationnel détailla`
- **T1** `reports/traduction-langues-3b.json:188:    "sortie": "Pour faciliter la mise en œuvre du plan, la Commission et chaque État membre concerné devraient entamer une arrangement opérationnel comportant de`
- **T1** `reports/rapport-pensee-stochastique.md:13:Même labyrinthe que T11, mais `sonde_p_sto` ouvre la porte avec **80 %** de probabilité ; en cas`
- **T1** `- **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**, **F1 0,7902** ; D1–E2 ([exemples](../../reports/rapport-exemples-tagger.md), [FAQ](../../reports/rapport-faq.md), [erreurs](../../reports/r`
- **T1** `- **N2 (nuit)** : la distillation tient-elle à 30 000 pas / 122 Mo ? → **non** à parité stricte (erratum) ; la repondération vaut **−0,05**.`
- **T1** `- **R1 (nuit)** : 2 048 à 20 000 pas ? → **oui** : 2×10 000 pas finis (perte 0,9409 → 0,8965 ; PPL 2,614 → 2,4953).`
- **T1** `journal/sessions/15fd322f-7e9e-48c0-a970-f36335eb622a/rapport.md:118:- **T1** `docs/convertisseur.md:20:| mémoire crête (fichier 353 Mo) | ~700 Mo | **413 Mo** |``
- **T1** `journal/sessions/15fd322f-7e9e-48c0-a970-f36335eb622a/rapport.md:119:- **T1** `docs/format-flux.md:33:actif**, et 505 ko par jeton sur une exécution dense (deux listes par couche).``
- **T1** `journal/sessions/15fd322f-7e9e-48c0-a970-f36335eb622a/rapport.md:120:- **T1** `docs/format-flux.md:97:| la taille suit l'activité | densité ÷2,3 → trace ÷2,5 (132 Mo → 53 Mo) |``
- **T1** `journal/sessions/15fd322f-7e9e-48c0-a970-f36335eb622a/rapport.md:121:- **T1** `docs/roadmap.md:15:| 0.1 | **Format de trace du flux** : par (couche, position), la liste des neurones actifs (indice + v`
- **T1** `journal/sessions/15fd322f-7e9e-48c0-a970-f36335eb622a/rapport.md:122:- **T1** `docs/roadmap.md:17:| 0.3 | **Le format EST le contrat d'échange** (phase 3) : versionné, en-tête + paires | ✅ | codec de `
- **T1** `journal/sessions/15fd322f-7e9e-48c0-a970-f36335eb622a/rapport.md:123:- **T1** `docs/roadmap.md:107:| 2026-09-30 | trace du flux, Qwen2.5-0.5B, 512 jetons, 24 couches, 2 points par couche | 12 288 list`
- **T1** `journal/sessions/15fd322f-7e9e-48c0-a970-f36335eb622a/rapport.md:124:- **T1** `docs/roadmap.md:135:| `--abits 16` (défaut) | 99-100 % (rien n'est seuillé) | 132 Mo | 25 à 42 % |``
- **T1** `journal/sessions/15fd322f-7e9e-48c0-a970-f36335eb622a/rapport.md:125:- **T1** `docs/roadmap.md:136:| `--abits 8 --act-thresh 0.05` | **26 à 56 %** | **53 Mo** | 26 à 56 % |``
- **T1** `journal/sessions/15fd322f-7e9e-48c0-a970-f36335eb622a/rapport.md:126:- **T1** `docs/roadmap.md:189:Mesuré, Qwen2.5-0.5B, 512 jetons, deux fenêtres de contexte, trace de 132 Mo :``
- **T1** `journal/sessions/c25f97d1-9a4d-41da-b983-004f793afe43/rapport.md:118:- **T1** `docs/convertisseur.md:102:  Un plan de placement qui ignore les nœuds NUMA laisse 20 % sur la table, et``
- **T1** `journal/sessions/42059fde-f06f-4e2c-9a23-8292d887fb6e/rapport.md:124:- **T1** `docs/roadmap.md:250:**1 745 octets contre 2 159** pour la liste i16, et 14 % d'écart contre 16 % —``
- **T1** `journal/sessions/42059fde-f06f-4e2c-9a23-8292d887fb6e/rapport.md:138:- **T1** `docs/plan-prefill-reparti.md:20:| nouveau mode ou champ `t` ? | **mode 3** (`MODE_LOT`), pas de champ | le corps dense d'`
- **T1** `journal/sessions/42059fde-f06f-4e2c-9a23-8292d887fb6e/rapport.md:152:- **T1** `docs/convertisseur.md:225:dessous du croisement mesuré à 22 % de densité : le régime où l'architecture``
- **T1** `journal/sessions/42059fde-f06f-4e2c-9a23-8292d887fb6e/rapport.md:154:- **T1** `docs/vision.md:46:**mesuré** : en dessous d'environ **10 % de densité**, le push (listes) bat le``
- **T1** `journal/sessions/42059fde-f06f-4e2c-9a23-8292d887fb6e/rapport.md:155:- **T1** `docs/vision.md:133:   croisement push/pull à 10 % donne déjà l'ordre de grandeur de ce qu'on``
- **T1** `journal/sessions/42059fde-f06f-4e2c-9a23-8292d887fb6e/rapport.md:156:- **T1** `docs/vision.md:198:* **ce n'est pas « le sparse gagne toujours »** : le croisement à 10 % de densité``
- **T1** `journal/sessions/42059fde-f06f-4e2c-9a23-8292d887fb6e/rapport.md:186:- **T1** `103:| E3 | **KV int4** | **fait** (nibbles empaquetés) | 1 M tient en RAM (9,7 Go) et en VRAM | mesuré : **+384 %** — lla`
- **T1** `journal/sessions/42059fde-f06f-4e2c-9a23-8292d887fb6e/rapport.md:192:- **T1** `docs/plan-mla-vision.md:461:`tools/mtmd/clip.cpp` (320 ko) a été récupéré et dépouillé. Ce qui s'y lit, pour``
- **T1** `journal/sessions/42059fde-f06f-4e2c-9a23-8292d887fb6e/rapport.md:196:- **T1** `docs/roadmap.md:116:| 2026-09-30 | découpage fidèle à **1 024 jetons** (1 024 flux, texte réel) | perplexité **9,5146** d`
- **T1** `journal/sessions/42059fde-f06f-4e2c-9a23-8292d887fb6e/rapport.md:197:- **T1** `docs/format-flux.md:142:| un lot ne change pas le résultat non plus | 256 jetons en 4 lots de 64 : écart **0,00e0** (18,0`
- **T1** `journal/sessions/42059fde-f06f-4e2c-9a23-8292d887fb6e/rapport.md:198:- **T1** `docs/roadmap.md:285:| avant correction | 144,8289 | 1 621,7239 | ×11,2 |``
- **T1** `journal/sessions/42059fde-f06f-4e2c-9a23-8292d887fb6e/rapport.md:199:- **T1** `docs/roadmap.md:286:| après la norme seule | 144,8289 | 693,4492 | ×4,8 |``
- **T1** `journal/sessions/42059fde-f06f-4e2c-9a23-8292d887fb6e/rapport.md:215:- **T1** `docs/colab-reparti.md:25:| latence | ✅ `TCP_NODELAY` : 16,1 ms d'attente contre 15,9 ms de calcul local (97,6 ms avant) |`
- **T1** `journal/sessions/42059fde-f06f-4e2c-9a23-8292d887fb6e/rapport.md:216:- **T1** `docs/contexte-long.md:260:appel — 24 couches × 6 appels CUDA par jeton, mesuré **24,5 ms/jeton** à 512``
- **T1** `journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:22605:        2    36.3%        0.89%   10.8%   38.1%   33/50 (66%)`
- **T1** `journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:22611:        8    29.2%        1.34%   14.8%   47.2%   43/50 (86%)`
- **T1** `journal/sessions/5c1bbea7-1d14-47b6-a48c-fea15f2b857e/digest.md:1389:| docs/comparaison-spiking.md:6 | `Sources : [Spikformer](https://ar5iv.labs.arxiv.org/html/2209.15425) (Zhang et` | Seules les sou`
- **T1** `journal/sessions/ee19a880-cc76-4c5c-9fe0-5972bd73b533/digest.md:1274:9. tools/sous_espace_du_contenu.py — apprentissage une fois : offsets de contenu E=(contenus×canaux) L116, SVD L117, projecteur Π=V`
- **T1** `journal/sessions/ee19a880-cc76-4c5c-9fe0-5972bd73b533/digest.md:1300:9. `tools/sous_espace_du_contenu.py` — SVD des offsets de contenu L116-117, projecteur Π=Vᵀ_rV_r (896×896) L120 appris une fois ; r`
- **T1** `journal/sessions/f3ca67c4-b171-4eee-9e14-29f9dd1c8c23/digest.md:1178:9. `tools/sous_espace_du_contenu.py` — SVD des offsets de contenu L116-117, projecteur Π=Vᵀ_rV_r (896×896) L120 appris une fois ; r`
- **T1** `**Ce qui marche déjà** : `analyser` (POS 86,25 %, F1 0,7902, attachement 238/239), `evaluer` (612 / gelé 602 / **réel 452**), `restituer`, le schéma v2 (v1 lue), le refus (code 3), le JSON déterminist`
- **T1** `"langue=fr script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (61.5% du texte)",`
- **T1** `- un chiffre sans dispositif (« 73 % ») ;`
- **T1** `51796:**Performance** (Xeon E5-2687W v3, Python 3.13.16) : heuristique **1,08 / 4,60 / 19,43 ms** à 10/50/200 mots (923/218/51,5 phrases/s), 0,09–0,11 ms/mot. Parallèle 1,51/6,18/27,22 ms ; cascade 1,`
- **T1** `51950:- Mémoire : pic **540,6 Kio** pour 200 mots ; RSS **30,7 Mio**, **delta 0** après 100 analyses ; démarrage à froid **99–113 ms**.`
- **T1** `52243:- **Temps CLI** : 136,8–226,6 ms, médiane **152,7 ms** (démarrage ~146 ms) ; **interne** : 0,2–45,1 ms, médiane **1,0 ms** ; f50 45,1 ms. **10 k** : 590–765 ms CLI, 331,6 ms interne, 2,76 Mo JSO`
- **T1** `52266:**Ce qu'il confirme** : 50 phrases, **0 plantage sur le banc**, 50/50 déterminisme, spans valides, 11 clés racine stables. Temps : **1,0 ms** interne (médiane), **152,7 ms** via la CLI (démarrag`
- **T1** `52313:- **Temps CLI** : 136,8–226,6 ms, médiane **152,7 ms** (démarrage ~146 ms) ; **interne** : 0,2–45,1 ms, médiane **1,0 ms**. **10 k** : 590–765 ms CLI, 331,6 ms interne, 2,76 Mo de JSON ; **50 k*`
- **T1** `SYNTAGMES   F1 81.88 %  (P 86.64 % / R 77.62 %)`
- **T1** `tête      F1 90.83 %  (P 96.11 % / R 86.10 %)`
- **T1** `vue linéaire (partition filtrer) F1 81.88 %  · attachement 93.72 % de couverture`
- **T1** `BASE RÉELLE (hand + reel, 452 phrases)  POS 88.91 % · F1 80.14 % · attachement 91.85 %`
- **T1** `ATTACHEMENT exact 88.70 % · couverture 93.72 % · exact sur span 94.64 % · top-k 89.54 %`
- **T1** `tête      couverture 100.00 % · top-k 95.54 %`
- **T1** `langue=und script=Latn source=heuristique · 16 étiquettes · unités sémantiques=2 (80.0% du texte)`
- **T1** `langue=en script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (60.0% du texte)`
- **T1** `langue=und script=Latn source=heuristique · 11 étiquettes · unités sémantiques=1 (80.0% du texte)`
- **T1** `langue=und script=Latn source=heuristique · 10 étiquettes · unités sémantiques=1 (87.5% du texte)`
- **T1** `langue=und script=Latn source=heuristique · 10 étiquettes · unités sémantiques=1 (80.0% du texte)`
- **T1** `BASE RÉELLE (hand + reel, 452 phrases)  POS 88.91 % · F1 79.06 % · attachement 99.46 %`
- **T1** `chevauchement (v2) ; `rang: 1` est la vue préférée, pas une suppression.`

## 5. Erreurs rencontrées

2 sorties en erreur ou divergentes. Les premières :

- **T1** : __pycache__/ *.pyc *.egg-info/ /build/ /dist/ reports/*.tmp models/ data/ qtrinet-core/target/  # Traces de session : la copie brute reste sur disque (volumineuse, binaire), # le digest markdown est v
- **T1** : #!/bin/bash # toutes-les-portes.sh — LA PASSE COMPLÈTE, et l'instrument qui manquait. # # POURQUOI CETTE PORTE EXISTE. Le 12 octobre, `tools/porte-gain.sh` §9 exigeait un REFUS # (`--attn-window` en r

## 6. Commits

- T3 — LE DÉMARRAGE EN 5 MINUTES : 3/3 COMMANDES REJOUÉES, JSON V2 5 899 OCTETS, TAGGER 4/0, ERREURS 3/4/1 ; LE CLONE PUBLIC SANS tools/structures EST DÉGRADÉ, DO

