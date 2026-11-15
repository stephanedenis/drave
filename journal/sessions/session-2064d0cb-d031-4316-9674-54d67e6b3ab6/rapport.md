# Session session- — Extension du gold réel 200+

> **Journaux :** [le jour](../../2026-11-15/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-2064d0cb-d031-4316-9674-54d67e6b3ab6` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-15 02:34 |
| Durée | 0.2 h |
| Tours | 1 |
| Messages | 99 |
| Appels d'outils | 148 |
| Fichiers touchés | 2 |
| Commandes | 102 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche C3 : la coordination R — propose et mesure l'extension du gold réel (le « gold 200+ » des fiches R) : prends 50 phrases **réelles** (hand + reel) que l'heuristique rate, écris la fiche `reports/rapport-gold-reel-50.md` + JSON (les erreurs d'attachement par type, les candidats à annoter), sans modifier le gold (S/D territory : le gold est à S).

## 2. Déroulé, étape par étape

### Tour 1 — Tâche C3 : la coordination R — propose et mesure l'extension du gold réel (le « gold 200+ » des fiches R) : prends 50 ph … [231 caractères tronqués]

*148 appels d'outils.* Actions notables :

- bash — List repository root
- bash — List report files
- bash — List pilotage and methode docs
- bash — Read programme R
- bash — Find gold/R related reports
- bash — Find files mentioning gold
- bash — Read coordination R report
- bash — Read seuils gold reel report
- bash — Read gold 200 report
- bash — Search for gold 200 references
- bash — Search for task C3
- bash — List linguistic test tools
- bash — Read attachment report
- bash — Read attachment failure report
- … et 126 autres

**Synthèse produite :**

\## C3 livré — le gold réel étendu

**Fiche** : `reports/rapport-gold-reel-50.md` · **JSON** : `reports/rapport-gold-reel-50.json` · **Script reproductible** : `tools/tests/linguistique/gold_reel_50.py` · **Acceptation** : `FICHE-OK`.

\### Le résultat en chiffres

| mesure | global 452 | **lot dur 50** | reste 402 | hasard stratifié (8 graines) |
|---|---:|---:|---:|---:|
| POS exact | 88,91 % | **68,42 %** | 91,98 % | 87,24–90,77 % |
| POS hors tokenisation | 91,34 % | **75,68 %** | 93,50 % | 89,40–93,31 % |
| F1 syntagmes | 79,06 % | **58,36 %** | 81,90 % | 73,68–83,63 % |
| attachement | 183/184 | **21/22** | 162/162 | 95,0–100 % |

Le lot fait **11,1 %** des phrases mais porte **37,1 %** des erreurs POS (102/275), **25,1 %** des segments absents (87/346) et **100 %** de l'erreur d'attachement (1/1). Il est **hors** des contrôles pour le POS et la F1 ; il ne l'est **pas** pour l'attachement.

\### Ce que ça dit

- **« gold 200+ » est défini** : c'est le gold **linguistique** hand + reel (452 phrases, 2 480 tokens, 184 cibles), pas le gold de pensée. Le libellé « 200+ » est obsolète et ambigu (T15) : le gold fait déjà 452 phrases.
- **L'attachement est saturé** (183/184). L'unique erreur est `g017` : SUB `that she would come` (gold 9–28) prédit `that she would come yesterday` (9–38) — la cible `said` est **bonne**, seul le span est faux. Ajouter des phrases ne testera pas l'attachement : il faut **annoter des cibles**.
- **L'extension utile n'est pas 50 phrases de plus** : c'est un **lot dur tenu à l'écart** (les 50 y sont déjà) + **10 cibles GP/SUB** (9 GP + 1 SUB, dont 4 dans le lot), qui font passer le dénominateur d'attachement de **184 à 194**. Priorité 2 facultative : les **144 GN/GV** du lot (79 GN + 65 GV), soit 338 cibles au total.
- **Sélection déterministe** : score `3×att + 2×POS + 1×segment absent`, 25 fr + 25 en, au plus 2 par signature d'erreur (42 signatures). Sans le plafond : 43 fr / 7 en, monoculture de négations. Sensibilité : 50/50 avec 2/2/1 et 5/2/1, 48/50 avec 3/3/1, 39/50 si le POS tombe à poids 1.

\### Contrôles et honnêteté

- **Hasard** : 50 simples (POS 85,00–91,01 %) et 50 stratifiées (87,24–90,77 %) ; le lot dur (68,42 %) est sous les deux.
- **Planchers** : majoritaire 21,98 % (lot) / 23,47 % (global) ; uniforme 8,36 % / 9,56 %.
- **Tokenisation** : 31 des 102 erreurs POS du lot sont des fusions d'élision/trait d'union (`j'ai`, `qu'il`, `viens-tu`), pas des fautes d'étiquette — c'est nommé dans la fiche.
- **Gold intact** : 
… [694 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel_50.py` | 1 | 23 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-reel-50.md` | 1 | 12 |

### Commandes exécutées (échantillon)

- **T1** List repository root
- **T1** List report files
- **T1** List pilotage and methode docs
- **T1** Read programme R
- **T1** Find gold/R related reports
- **T1** Find files mentioning gold
- **T1** Read coordination R report
- **T1** Read seuils gold reel report
- **T1** Read gold 200 report
- **T1** Search for gold 200 references
- **T1** Search for task C3
- **T1** List linguistic test tools
- **T1** Read attachment report
- **T1** Read attachment failure report
- **T1** Git status and recent log
- **T1** Find coordination R task definitions
- **T1** Show recent commit stats
- **T1** List newest reports
- **T1** Read autonomous week plan
- **T1** Read today's journal
- **T1** Search C3 in today's journal
- **T1** Read current state
- **T1** Inspect plan.json structure
- **T1** Print C tasks definitions
- **T1** Line counts of gold tools
- **T1** Inspect gold JSON structures
- **T1** Read evaluator
- **T1** Read rest of evaluator
- **T1** Inspect gold dicts
- **T1** Read product README around gold 200+
- **T1** Read base reelle report
- **T1** Find attachment code in bloc
- **T1** Find classes in bloc
- **T1** Find evaluer in CLI
- **T1** Read bloc header
- **T1** Gold real statistics
- **T1** Search annotation candidates phrase
- **T1** Search attachment errors phrase
- **T1** Search gold 200+ mentions
- **T1** Analyze per-sentence heuristic errors
- … et 62 autres

## 4. Mesures et résultats marquants

- **T1** `phrases, BM25/regex). Récupération **1,00** à **30 %** du budget sur les 5 types.`
- **T1** `| **R0.2 contrôleur** | 20 questions main, 5 types | récupération **1,000** à 30 % | [`r02`](../../reports/rapport-r02-controleur.md) |`
- **T1** `R13 est **close** : à budget d'octets égal, le BPE perd partout — **+0,39 %** (512, deux graines),`
- **T1** `**+3,92 à +4,09 %** (1024), **+4,22 % / +6,59 %** en anglais. Le natif reste en **octets** ; le`
- **T1** `« gain de 11 % » du pilote était un artefact de budget, corrigé par la mesure.`
- **T1** `- **R4.4 — scans** : 100 scans simulés, 5 familles ; **4/5** familles ≥ **90 %** de parité`
- **T1** `(propre **96,7 %**, photocopie **93,3 %**, photo **90,0 %**, papier **90,0 %**), **fax 56,7 %**`
- **T1** `(limite 1 bit) ; colonnes **89,4 % → 0,5 %** ; tableaux **92,6 %** (propre) / **69,1 %**`
- **T1** `(photocopie) ; **vrai scan** Verne : **7,10 %** de WER, ordre des colonnes prouvé.`
- **T1** `des **71 langues / 449/449** existe, mais le décodeur est **négatif** et le `z` ne lit que ~7 %`
- **T1** `| **le contrôleur** (R0.2) | récupération **1,000** à 30 % | [`r02`](../../reports/rapport-r02-controleur.md) |`
- **T1** `| **le balayage** (R05) | rappel@10 **0,984**, **0,1 ms** | [`r05`](../../reports/rapport-r05-balayage.md) |`
- **T1** `| **les scans** (R4.4) | 4/5 ≥ 90 %, réel **7,10 %** | [`r44`](../../reports/rapport-r44-scans.md) |`
- **T1** `| **la tokenisation** (R13) | octets ; BPE +0,39/+4,09 % | [`r13`](../../reports/rapport-r13-decision.md) |`
- **T1** `| **le fax** (R4.4) | parité **56,7 %** | 120 dpi, 1 bit : l'information n'est plus là |`
- **T1** `- **la parité juge, pas le WER** : un WER de 6 % qui casse la réponse à une question n'est pas`
- **T1** `| R5 | R3, B10.3 | le `z` lit ~7 % du sens |`
- **T1** `BM25, R0.5 (routeur) ne transfère pas, B10.3 ne lit que ~7 % du sens, et la typoglycémie montre`
- **T1** `que le modèle lit les **lettres**, pas les **formes** (×17,8 au mélange intérieur, ×62,7 tout`
- **T1** `> IC95 bootstrap par phrase **[+7,23 ; +9,74]**, McNemar **344/74**, **p = 1,1 × 10⁻⁴²**. La règle`
- **T1** `(15 Mo). La clé de cache est un sha256 de `modèle + messages + température + max_tokens` ; les`
- **T1** `| `7a45325f` — la ponctuation a une POS (`PONCT`) | 85,00 → 85,75 % | **+25** |`
- **T1** `| `6b976cb1` — R4-FR filtré (adjectif connu ou suffixe) | 85,75 → 85,84 % | **+3** |`
- **T1** `| `c43dd5cc` — la règle « que » (pronom après un nom) | 85,84 → 86,25 % | **+13** |`
- **T1** `| **total** | **85,00 → 86,25 %** | **+40** |`
- **T1** `| appels | ~1 200 | **1 218** | +1,5 % |`
- **T1** `| tokens | ~360 000 | **358 962** | −0,3 % |`
- **T1** `| durée | ~20 min | **20 min 59 s** (1 259,2 s) | +5 % |`
- **T1** `| latence moyenne / appel | 0,94 s (run 432) | **1,033 s** | +10 % |`
- **T1** `**27 326 tokens de sortie** (totaux à ±0,5 % près, six prompts dupliqués).`
- **T1** `| **612** | 2742/3179 = **0,8625** | 3012/3179 = **0,9475** | **+8,49 pts** | **[+7,23 ; +9,74]** | **344 / 74** | **1,1 × 10⁻⁴²** |`
- **T1** `| hand 20 | 93/105 = 0,8857 | 102/105 = 0,9714 | +8,57 pts | [+2,75 ; +15,38] | 9 / 0 | 3,9 × 10⁻³ |`
- **T1** `| réel 432 | 2112/2375 = 0,8893 | 2223/2375 = 0,9360 | **+4,67 pts** | **[+3,45 ; +6,01]** | 181 / 70 | 1,7 × 10⁻¹² |`
- **T1** `| synth 160 | 537/699 = 0,7682 | 687/699 = 0,9828 | **+21,46 pts** | [+18,80 ; +24,15] | 154 / 4 | 1,4 × 10⁻⁴⁰ |`
- **T1** `- `--sortie` : le JSON de mesure (47 Ko), avec les six modes, les quatre ventilations, les`
- **T1** `répartition entrée/sortie est reconstruite depuis le cache (six prompts dupliqués, ±0,5 %).`
- **T1** `- **Mesure brute** : [`tagger-612.json`](tagger-612.json) — 47 Ko, six modes, quatre ventilations,`
- **T1** `docs/pilotage/plan-travail.md:39:| **L/B13 — Pensée (session `e181ce02`)** | le bloc langue (contrat heuristique + neuronal), la cascade, la pragmatique ; B13 | L, B13, la couche heuristique | **CPU**`
- **T1** `docs/pilotage/plan-travail.md:195:   **0,7539**, acte **1,0**) ; **DRVM/native** par la règle (**3 nœuds**) ; **DRVM N0.1 6/6** ; **pragmatique 130 : 1,0 / 1,0 / 0,9846 / 0,9769** — elle qualifie ; **`
- **T1** `docs/pilotage/chantiers.md:88:| **L — le bloc langue** (nouveau) | le CPU peut-il étiqueter la surface et le réseau ne traiter que le résidu ? | ✅ **contrat + bloc v0** : 9 niveaux, **398 langues à 0,`
- **T1** `docs/pilotage/chantiers.md:90:| **B13 — le moteur de pensée** | penser est-il une recherche tracée sur des états pluriels ? | ✅ state store v0 + AC-3/alpha-bêta + **DRVF `thought`** + **banc anytime**`
- **T1** `docs/pilotage/roadmap.md:279:| **B13** | le **moteur de pensée** : RSN plurielle, arbre d'états, anytime | ✅ **state store v0** + moteur + **AC-3/alpha-bêta** + **DRVF `thought`** + **banc anytime** +`
- **T1** `XU1KjqNR0u9tmc3Qfak5EsxibAYMGJs/e66XNqEfcvfl2dCiKkEvrge4ExBB/XQ0zHXAxi/O4MtG79f1LKdDeURS2ddryT3/iQKcKdN/DhzxoszEARC+TgiEuMCEifhIkwqtDodC4rpIGnZPOT+iAmUojAUA/LDcu8A8GMEZt8BeRZRAy+bs/oubhElCNQ90FvOYADy7`
- **T1** `docs/pilotage/roadmap.md:280:| **C3.2** | les modules par famille de langues | ✅ | aucune — **7/9 > 30 %**, moyenne **69,5 %**, contrôle **≤ 0,5 %** |`
- **T1** `docs/theorie/carte.md:47:| **C3.2e** sous-familles autres | **mesuré** — uralic 46,7→100 %, benue 88 %, austro 60,3 %, afro ouest 53,5 % | [la fiche](../../reports/rapport-sous-familles-autres.md) |`
- **T1** `docs/theorie/carte.md:48:| **C3.2d** sous-familles IE | **mesuré** — 54,6–100 % ; l'IE à 14,7 % est un effet de composition | [la fiche](../../reports/rapport-ie-sous-familles.md) |`
- **T1** `docs/theorie/carte.md:49:| **C3.2c** 9 familles | **mesuré** — 7/9 > 30 %, moyenne 69,5 %, contrôle 0 ; indo-européen 14,7 %, uralic 46,7 % | [la fiche](../../reports/rapport-familles-9.md) |`
- **T1** `- **La couverture est la première limite** : 145 cibles sur 239 sont annotées (60,7 %) — les`
- **T1** `| **span faux** (aucun segment prédit au même span) | **94** | 74,0 % |`
- **T1** `| **cible hors des candidats** (span bon) | **33** → **32** après le correctif | 26,0 % |`
- **T1** `| **tout** | **127** → **126** après | 100 % |`
- **T1** `6560a0a5 1A — LE TAGGER SUR LA BASE RÉELLE : 88,91 → 95,00 % (+6,1), 449 APPELS SERVIS PAR LE CACHE ; IL GAGNE SURTOUT SUR LE SYNTHÉTIQUE (+9,5 SUR 612)`
- **T1** `2d7a7f2b 1A — LES DEUX DÉFAUTS DU TAGGER CORRIGÉS : 1 APPEL PAR PHRASE (LE TAGGER DE SYNTAGMES RETIRÉ) ET PONCT RESTITUÉ (25/25) ; POS 612 → 95,75 % (+9,5)`
- **T1** `ce7241d5 6A — LA BASE HONNÊTE : evaluer --reel (452 PHRASES RÉELLES : POS 88,91 %, F1 79,06 %, ATTACHEMENT 99,46 %) ET LA LIGNE BASE RÉELLE DANS LA SORTIE PAR DÉFAUT ; 20 TESTS`
- **T1** `6A — LA BASE HONNÊTE : evaluer --reel (452 PHRASES RÉELLES : POS 88,91 %, F1 79,06 %, ATTACHEMENT 99,46 %) ET LA LIGNE BASE RÉELLE DANS LA SORTIE PAR DÉFAUT ; 20 TESTS`
- **T1** `1A — LE TAGGER SUR LA BASE RÉELLE : 88,91 → 95,00 % (+6,1), 449 APPELS SERVIS PAR LE CACHE ; IL GAGNE SURTOUT SUR LE SYNTHÉTIQUE (+9,5 SUR 612)`
- **T1** `(R² 0,30) — la surface capte l'époque ; tout test de style contrôle la date, tout test de famille`
- **T1** `| 2 | **atomes V14 ↔ niveaux** (44 œuvres × 14 flottants, JSON pur) | table + 20 exemples mesurés | permuter les colonnes doit tuer le prédictif | signature lexicale : contrôler la date |`
- **T1** `| **J2** | après-midi : corpus commun | ✅ fait | **21 textes**, 5 familles, 10 écritures, **418/438** paires exactes (95,4 %), 8/8 contrôles | `c3467170` (avec J3.1) | corpus multi-époques / multi-gen`
- **T1** `| 01:31 | `ce7241d5` | 6A — LA BASE HONNÊTE : evaluer --reel (452 PHRASES RÉELLES : POS 88,91 %, F1 79,06 %, ATTACHEMENT 99,46 %) ET LA LIGNE BASE RÉELLE DANS LA SORTIE PAR DÉFAUT ; 20 TESTS |`
- **T1** `| 01:39 | `2d7a7f2b` | 1A — LES DEUX DÉFAUTS DU TAGGER CORRIGÉS : 1 APPEL PAR PHRASE (LE TAGGER DE SYNTAGMES RETIRÉ) ET PONCT RESTITUÉ (25/25) ; POS 612 → 95,75 % (+9,5) |`
- **T1** `| 01:42 | `6560a0a5` | 1A — LE TAGGER SUR LA BASE RÉELLE : 88,91 → 95,00 % (+6,1), 449 APPELS SERVIS PAR LE CACHE ; IL GAGNE SURTOUT SUR LE SYNTHÉTIQUE (+9,5 SUR 612) |`
- **T1** `**Mis à jour : 2026-11-15, 02 h 32 HNE (tagger : 95,75 % sur 612, 95,00 % sur le réel 452)**`
- **T1** `- **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ; page **`/paragraphes`**, **19/19 verdicts `389b99f`** ; **5`
- **T1** `- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/239 (0,9958)**, **F1 0,7902**, **1 span** ; **`s065`** et **`r035`** réglés, **convention des GV** ; **restitution v1** (46/46 canoniq`
- **T1** `- **Panini J7.1** : 532 textes (445 langues) ; hors script, hasard ; famille **66,1 %** / sœur **26,1 %** (hasard 10,3/2,5) ; LANG_TREE : sœurs **0,619** vs **0,0445** (13,9×, p=0,002) ; [fiche](../..`
- **T1** `- **N2 (nuit)** : la distillation tient-elle à 30 000 pas / 122 Mo ? → **non** à parité stricte (erratum) ; la repondération vaut **−0,05**.`
- **T1** `- **R1 (nuit)** : 2 048 à 20 000 pas ? → **oui** : 2×10 000 pas finis (perte 0,9409 → 0,8965 ; PPL 2,614 → 2,4953).`
- **T1** `> phrases réelles** (main + corpus, sans les 160 synthétiques), le **POS monte** (88,91 % contre`
- **T1** `> 86,25 %) et la **F1 est la même** (79,06 % contre 79,02 %) — le synthétique n'aidait donc **pas**`
- **T1** `| POS | 86,25 % | **88,91 %** (fermé 92,94 / ouvert 84,66) |`
- **T1** `| F1 syntagmes | 79,02 % | **79,06 %** |`
- **T1** `| tête F1 | 90,29 % | 89,90 % |`
- **T1** `| attachement exact | 99,58 % | **99,46 %** |`
- **T1** `| couverture | 99,58 % | 99,46 % |`
- **T1** `SYNTAGMES   F1 79.02 %  (P 78.60 % / R 79.44 %)`
- **T1** `tête      F1 90.29 %  ...`
- **T1** `vue linéaire (partition filtrer) F1 79.53 % · attachement 91.85 % de couverture`
- **T1** `BASE RÉELLE (hand + reel, 452 phrases)  POS 88.91 % · F1 79.06 % · attachement 99.46 %`
- **T1** `ATTACHEMENT exact 99.58 % · couverture 99.58 % · ...`
- **T1** `"constat": "le POS réel est meilleur (88,91 % contre 86,25 %) ; le synthétique tirait la moyenne vers le bas ; la F1 est identique",`
- **T1** `reports/07/p4.md:574:   **annoter** (« 41 % de tokens coûteux ») et **laisser l'humain ou une boucle** corriger ✓✗ ;`
- **T1** `| T09 | N2 | La porte propre (0,29 manquant à 2,7856) : données ou capacité | reports/n2-*, work/n2ac/, tools/entrainer_native.py, GPU | recette N2 1 024 | aucun externe ; GPU libres (0 %) | python3 t`

## 5. Erreurs rencontrées

2 sorties en erreur ou divergentes. Les premières :

- **T1** : gold.json {'id': 'g017', 'langue': 'en', 'texte': 'She said that she would come yesterday.', 'mots': [{'texte': 'She', 'pos': 'PRON', 'debut': 0, 'fin': 3}, {'texte': 'said', 'pos': 'VERB', 'debut': 4
- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 9, in <module> KeyError: 'tokens' [exit code: 1]

