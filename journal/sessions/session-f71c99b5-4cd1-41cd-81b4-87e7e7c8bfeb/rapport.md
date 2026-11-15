# Session session- — Rapport semaine 2 et tag

> **Journaux :** [le jour](../../2026-11-15/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-f71c99b5-4cd1-41cd-81b4-87e7e7c8bfeb` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-15 12:05 |
| Durée | 0.4 h |
| Tours | 1 |
| Messages | 115 |
| Appels d'outils | 136 |
| Fichiers touchés | 4 |
| Commandes | 109 |
| Sous-agents | 0 |
| Commits | 4 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche W6 (J5 après-midi) : la clôture de la semaine 2 — le rapport `reports/rapport-semaine-2.md` + JSON (les chiffres avant/après de chaque vague W1-W5, les négatifs, les décisions), la mise à jour de `docs/pilotage/en-cours.md` et `semaine-2.md` (l'état par jour), le **tag annoté** `semaine-2-2026-11-20` sur le dernier commit vert, et le relevé des portes. Ne relance pas la passe complète : lis  … [15 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tâche W6 (J5 après-midi) : la clôture de la semaine 2 — le rapport `reports/rapport-semaine-2.md` + JSON (les chiffres a … [295 caractères tronqués]

*136 appels d'outils.* Actions notables :

- bash — Inspect repo state and recent commits
- bash — List repo structure and key directories
- read
- bash — List portes directories
- bash — Inspect branches, dates, reflog
- bash — Read latest gates registry
- bash — Find latest gate passes and recent reports
- bash — Search for W5 references
- bash — Check diffs, W5 report, gates registry
- bash — Read greffe gate logs and tolerated reds
- bash — Check for running gate processes
- bash — Check journal for week 2 narrative
- bash — Identify running gate pass outputs
- bash — Read gate runner script
- … et 111 autres

**Synthèse produite :**

Clôture W6 faite.

\## Livré

- **`reports/rapport-semaine-2.md`** + **`reports/rapport-semaine-2.json`** : les cinq vagues W1–W5 avec avant/après, dispositif, contrôles négatifs, décisions D1–D6, limites. Chiffres clés :
  - W1 : gold **452** (20 hand + 432 corpus, 242 fr / 210 en), split **402/H50**, **184 → 194** cibles, sha256 identique.
  - W2 : 402 **0,9198 → 0,9643** (+4,45), H50 **0,6842 → 0,8607** (+17,65), F1/attachement 402 inchangés, fermé 402 **−1,55**.
  - W3 : défaut **code 0 / 0 socket**, clé invalide **4**, réseau coupé **0** après 3 essais, 1 000 phrases = **143 870 tokens / ~0,031 $**.
  - W4 : **bloqué** — 26 signatures à recevoir, rejeu **27/60**, calibration **42/44**, 3 sources courtes, 5 doublons, **N5 vide**, aucune p-value.
  - W5 : gold S **144/144** (18/18), gold v2 **20/46** (F1 **0,5406**, lieu **0,60**), permutation **0/18**.

- **`docs/pilotage/en-cours.md`** : état de clôture, W5/W6, compteurs **754 fiches / 847 JSON**, dernière passe **15/11 09h53 (85, 81/4)** with reds named, reste (J4, page `/`, Panini, `auto`).
- **`docs/pilotage/semaine-2.md`** : nouvelle section **« L'état par jour (constaté le 15/11) »** J1→J5, avec les vagues réelles, les non-ouvertes (J4) et le tag.
- **`docs/pilotage/references-non-regression.md`**, **`roadmap.md`**, **`journal/2026-11-15/`** : relevé de passe, tag, récit W6.

\## Commits et tag

| quoi | hash |
|---|---|
| W5 (restitution v3 + champ de coût W3 manquant + heartbeat) | **`73edb3dd`** |
| W6 (clôture, rapport, état, docs) | **`6f862993`** |
| tag annoté `semaine-2-2026-11-20` | **`73edb3dd`** (vérifié : `git cat-file -t` → `tag`, `rev-parse ^{}` → `73edb3dd`) |

Le tag est posé sur le **dernier commit de code vert** (W5), pas sur le commit de clôture — convention du dépôt, limite explicitement nommée dans le rapport.

\## Portes

Pas de passe complète relancée, conformément à la consigne. Relevé lu :
- **`work/portes-1115-09h53`** : **85 portes, 81 vertes, 4 rouges** — `indice`, `melange` (structurelles), `sessions` (heartbeat réparé à 12 h 20), `prechargement` (environnementale : deux passes en parallèle, PPL identique 799,8557).
- **`work/portes-w5`** : passe à `DELAI=600`, non concluante ; `greffe 124` = borne (780 s verte le 14/11), pas régression.
- **Ciblage W6** : **8/9** puis **9/9** (`work/portes/w6-final`).
- `revue_documentation.py` : ✅ (754 / 847 / 124 / 85) ; `verifie_en_cours`, `verifie_journal`, `taille_documents`, `verifier_schemas`, `porte-tableaux` : ✅.

Les modificat
… [153 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-semaine-2.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-2.md` | 0 | 3 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md` | 0 | 7 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/references-non-regression.md` | 0 | 2 |

### Commandes exécutées (échantillon)

- **T1** Inspect repo state and recent commits
- **T1** List repo structure and key directories
- **T1** List portes directories
- **T1** Inspect branches, dates, reflog
- **T1** Read latest gates registry
- **T1** Find latest gate passes and recent reports
- **T1** Search for W5 references
- **T1** Check diffs, W5 report, gates registry
- **T1** Read greffe gate logs and tolerated reds
- **T1** Check for running gate processes
- **T1** Check journal for week 2 narrative
- **T1** Identify running gate pass outputs
- **T1** Read gate runner script
- **T1** Locate outputs of the two passes
- **T1** Check pass env and 09h53 registry
- **T1** Read failing gate logs from 09h53 pass
- **T1** Read week 1 closure report template
- **T1** Read weekly report and index conventions
- **T1** Check system date and weekly report files
- **T1** Read results method requirements
- **T1** Inspect weekly report JSON structure
- **T1** Read W1-W4 report headers
- **T1** Find W1-W5 JSON files
- **T1** Read rest of gold 452 report
- **T1** Inspect JSON keys of W1-W5
- **T1** Extract W1 figures
- **T1** Extract W2 figures
- **T1** Extract W3 figures
- **T1** Extract W4 figures
- **T1** Extract W4 short sources and duplicates
- **T1** Extract W5 key figures
- **T1** Search for W6 and tag references
- **T1** Read roadmap state
- **T1** Read W1-W6 tasks from plan.json
- **T1** Read current session plan and digest mandate
- **T1** Read current session digest head and tail
- **T1** Inspect existing tags and annotations
- **T1** Find previous tag closure narrative
- **T1** Check gate pass progress
- **T1** Review staged W5 docs changes
- … et 69 autres

## 4. Mesures et résultats marquants

- **T1** `docs/pilotage/roadmap.md:33:| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 c`
- **T1** `variantes écrites : ×0, ×0,6, ×1,0 (depuis /tmp/n4/rang4-lora.pt)`
- **T1** `porte de l'homéostasie (E9) — LoRA rang 4, amplitudes ×0 / ×0,6 / ×1,0`
- **T1** `sigfiges : occupation de l'ATTENTION à 25.2 % (cible : 0.25 gardé)`
- **T1** `lognormal : occupation de l'ATTENTION à 25.2 % (cible : 0.25 gardé)`
- **T1** `libres : occupation de l'ATTENTION à 25.2 % (cible : 0.25 gardé)`
- **T1** `| attachement (réel) | — | **99,46 %** | réel 452 |`
- **T1** `| **la table 14 atomes × 8 niveaux** | 14/14 lignes, 33 paires colinéaires |`
- **T1** `| **le §334** | leur loi H0 **reproduite** (R² 0,909) ; leur β époque **+0,138 non reproduit** (−0,006) ; le plan est **colinéaire** |`
- **T1** `McNemar **344/74**, **p = 1,1 × 10⁻⁴²**. Contrôles négatifs : majoritaire **0,2145**, classe`
- **T1** `| corpus commun | 0 texte commun | **21 textes, 418/438 paires exactes (95,4 %)** | 8/8 (6 rejets + 2 témoins) | [corpus](rapport-corpus-commun.md) |`
- **T1** `**4 composantes > 1**, les trois premières à **80,7 %** de la variance (6,967 · 2,845 · 1,491).`
- **T1** `**418 exactes (95,4 %)** ; **20 écarts de surface exclus, pas corrigés** (apostrophes,`
- **T1** `un **effet de composition** : 60 % des couples décalés sont de même écriture, contre 33 % des`
- **T1** `| [rapport-speculatif-reflexe.md](rapport-speculatif-reflexe.md) | Le réflexe propose, le cerveau vérifie — acceptation 2 à 30 % (le cerveau non entraîné : 0 %) |`
- **T1** `| [rapport-vitesse-v41.md](rapport-vitesse-v41.md) | Rapport — La nuit des optimisations V4.1 : ×3,54 sur la passe, et pas un chiffre changé |`
- **T1** `- un chiffre sans dispositif (« 73 % ») ;`
- **T1** `Le corpus pèse **2 375 tokens** (95,8 % du gold) et **171 cibles** ; le hand pèse **105 tokens** et **13 cibles**.`
- **T1** `graine donne **88,13 %** de POS, contre **68,42 %** pour H50 : c'est la preuve que H50 est un stress test,`
- **T1** `**190 segments**, **22 cibles**. H50 fait **11,1 %** des phrases mais porte **37,1 %** des erreurs POS`
- **T1** `(102/275), **25,1 %** des segments absents (87/346) et **100 %** de l'erreur d'attachement (1/1).`
- **T1** `controles_negatifs.tirage_aleatoire str graine 20261116 : POS 88,13 %, F1 78,69 %, attachement 100 % ; H50 : 68,42 %, 58,36 %, 95,45 %.`
- **T1** `81pJ9Nv6Rx9Ea4w6jDLjxZxbFY06Xzm+uwuoU0wcr43+FAfSy0sc+lbMaZWT1m4FK53qQoMxga6schjKTbz3I5nD3HpZK38yeOVjWquOCGu+CFP+5wXhjMksvghSnNWaiyIy6pQTSBA3s5LetRRY0ZA3iFlrovMH8xjm/74Fe232PPC8nDezNJpUkUD18Yeae2XkMNvg`
- **T1** `s="marker flowchart-v2" viewBox="0 0 11.5 14" refX="11.5" refY="7" markerUnits="userSpaceOnUse" markerWidth="10.5" markerHeight="14" orient="auto"><path d="M 0 0 L 11.5 7 L 0 14 z" class="arrowMarkerP`
- **T1** `journal/sessions/session-9a7f5c6a-2798-4ca2-9b0f-131347ef53c3/digest.md:319:QlaErYTMvvpsFuJWrjlKAsu7/Xs3Qy93zHJ9w3e+Ml4qOCI76UxmHmy+e8dMf2rC+ptejYyv4XfhSvnfPvajGbn/rY+IR85dXePWyu4f/lh2Uv7v1gdx0LOGMucX`
- **T1** `| **A — le moteur** | formats, placement, transport, [rejeu](../theorie/glossaire/entrees/rejeu.md), matériels, ordonnanceur | ✅ A1–A8 ; **A3.4, A5.4 bloqués** ; **A6.2 libre** (MoE local 18 Go) ; A2.`
- **T1** `| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ; `
- **T1** `| **S — les structures** | coloration, rôles, validation humaine, banque d'interprétations | ✅ **v7** : **61/61** types, **144/144** rôles, **56 tests** ; **19/19 verdicts `/paragraphes`** (11 accepté`
- **T1** `| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 langues à 0,9687**, script 1,00`
- **T1** `| **D — les données** | inventaire, corpus 10 langues, texte intégral, PDF/[OCR](../theorie/glossaire/entrees/ocr.md), documents, genres | ✅ inventaire ; **10 corpus texte intégral** (20,53 M art., 67`
- **T1** `**État au 14/11 07 h 10.** B13 : **POS 86,25 %**, **attachement exact 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (238/238 ; [fiche](../../reports/`
- **T1** `**J7.1** sépare la **sœur** de la **famille lointaine** : sur 532 textes Panini (445 langues, 1948), le top-1 est de la même famille **66,1 %** (hasard 10,3 %) et de la même branche **26,1 %** (hasard`
- **T1** `devant, mais l'anglais est **100 % réel** quand le français ajoute **160 synthétiques** ; sur le`
- **T1** `canonique**, le strict **5/46** ; temps CLI médian **159,2 ms**, API **2,7 ms**. Comparaison`
- **T1** `sources acquises ne sont pas 102 URL (71 URL uniques). La loi H0 se reproduit (**R² = 0,909139** sur`
- **T1** `contre null **−0,129**, p=0,335). Sur les 44 signatures, le retrieval brut donne **61,4 %** de même`
- **T1** `tradition et **56,8 %** de voisins à ≤50 ans, mais les contrôles croisés ramènent la filiation à`
- **T1** `**50,0 %** (p=0,0492, Holm 0,128) et l'époque à **53,8 %** (p=0,373) ; seule une petite prédiction`
- **T1** `d'année intra-tradition survit (**R²=0,042**, p=0,0086, Holm 0,034). Le β époque **+0,138** de la v150`
- **T1** `-- **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ; page **`/paragraphes`**, **19/19 verdicts `389b99f`** ; **`
- **T1** `- **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**, **F1 0,7902** ; **D1–D3**, **E1–E2** livrés ([exemples](../../reports/rapport-exemples-tagger.md), [FAQ](../../reports/rapport-faq.md), [er`
- **T1** `-- **Panini** : **14 atomes** ; UDHR **418/438** ; J3.2 **5/21** langues (Glottolog **21/21**), **154/154** hors script au hasard, **V14 3/21** ; B2 **négatif** (niveaux non prédits) ; J7.1 famille **`
- **T1** `+- **Panini** : **14 atomes** ; UDHR **418/438** ; J3.2 **5/21** langues (Glottolog **21/21**), **154/154** hors script au hasard, **V14 3/21** ; B2 **négatif** (niveaux non prédits) ; J7.1 famille **`
- **T1** `- **R1 (nuit)** : 2 048 à 20 000 pas ? → **oui** : 2×10 000 pas finis (perte 0,9409 → 0,8965 ; PPL 2,614 → 2,4953).`
- **T1** `-| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ;`
- **T1** `+| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ;`
- **T1** `-**État au 14/11 07 h 10.** B13 : **POS 86,25 %**, **attachement exact 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (REL suivie d'un GV → le sujet d`
- **T1** `+**État au 14/11 07 h 10.** B13 : **POS 86,25 %**, **attachement exact 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (238/238 ; [fiche](../../reports`
- **T1** `[still running after 60000ms; moved to background job bash-53]`
- **T1** `- **Note** : l'attachement est à **236/237 (0,9916)**, la couverture 0,9916, POS **86,25 %**, F1 **0,7535**, 2 spans ; la seule rouge est`
- **T1** `✅ 6. le PROJECTEUR reproduit la référence (écart 0.7139 % = la quantification)`
- **T1** `docs/pilotage/roadmap.md:38:**État au 15/11 12 h 20.** La **semaine 2** est close : W1 gold 452, W2 tagger 402/H50, W3 défaut hors ligne, W4 Panini bloqué, W5 restitution v3 ; tag `semaine-2-2026-11-2`
- **T1** ``88,91 %` · `79,06 %` · `99,46 %``

## 5. Erreurs rencontrées

3 sorties en erreur ou divergentes. Les premières :

- **T1** : #!/bin/bash # toutes-les-portes.sh — LA PASSE COMPLÈTE, et l'instrument qui manquait. # # POURQUOI CETTE PORTE EXISTE. Le 12 octobre, `tools/porte-gain.sh` §9 exigeait un REFUS # (`--attn-window` en r
- **T1** : chantier-2026-11-14 semaine-2026-11-14 --- == chantier-2026-11-14 tag chantier-2026-11-14 Chantier 2026-11-14 : 84 portes, 81 vertes, 3 rouges nommées (indice, melange, sessions) ; 28/28 acceptations 
- **T1** : work/msg-backlog-n2.txt work/msg-bilan.txt work/msg-claims.txt work/msg-cle2.txt work/msg-cle3.txt work/msg-cle.txt work/msg-cpt.txt work/msg-etat.txt work/msg-homeo2.txt work/msg-homeo.txt work/msg-j

## 6. Commits

- cat > work/msg-w5.txt <<'EOF' SEMAINE 2 — W5 : LA RESTITUTION v3 SÉPARE LES CINQ RÔLES (GOLD S 144/144, 18/18, PERMUTATION 0/18) ; LE GOLD v2 NE GAGNE QU'UN CAD
- git add journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md && git commit --amend --no-edit --quiet && git log -1 --format='%h %s'
- git commit -F work/msg-w6.txt --quiet && git log -1 --format='%h %ci %s'
- git add reports/rapport-semaine-2.md reports/rapport-semaine-2.json docs/pilotage/en-cours.md docs/pilotage/references-non-regression.md journal/2026-11-15/port

