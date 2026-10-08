# Session 48ec07ab — Tu travailles dans le dépôt

| | |
|---|---|
| Identifiant | `48ec07ab-ec9d-4297-a7bf-d84974667e61` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-08 09:18 |
| Durée | 0.1 h |
| Tours | 1 |
| Messages | 50 |
| Appels d'outils | 62 |
| Fichiers touchés | 0 |
| Commandes | 36 |
| Sous-agents | 2 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave » : moteur d'inférence Rust dans drave-core/, outils Python dans tools/, rapports dans reports/, sprints dans sprints/, journal des sessions dans journal/, reprise dans REPRISE.md).  MISSION : inventorier TOUT le travail « côté modèle » de ce dépôt — c'est-à-dire ce que le projet a lui-même entraîné, ajusté … [2641 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave » : moteur d'inférence Rust  … [2921 caractères tronqués]

*62 appels d'outils.* Actions notables :

- bash — List repo root
- bash — List tools, reports, docs
- bash — List remaining tools and data dirs
- bash — Check pont scripts existence
- sous-agent — Inventaire corpus dépôt
- sous-agent — Inventaire poids et entraînements
- bash — Count lines of target reports
- read
- bash — Grep recapitulatif for direction work
- bash — List headings of rapport-toutes-langues
- bash — Tail headings of big report
- bash — Headings of recapitulatif
- bash — Check existence of mission-mentioned files
- bash — List most recent reports and tools
- … et 27 autres

**Synthèse produite :**

⏵ Livraison du rapport final.

Rapport envoyé au parent. Le voici (lecture seule ; aucun fichier modifié, aucun entraînement lancé) :

\# Inventaire du travail « côté modèle » — Qtrinet / Drave
[M] = mesuré (rapport ou artefact) · [D] = déduit du code · [S] = supposé.

\## 1. TABLEAU DES DISPOSITIFS ENTRAÎNÉS
Professeur = Qwen2.5-0.5B GGUF (24 couches, 896 canaux), **jamais entraîné ici**, lu en boîte noire (couche 0 → couche 10). Tout apprentissage est en **forme fermée, numpy seul** : aucun torch, aucun `backward` dans `tools/` [M].

| Dispositif | Architecture / taille | Corpus | Coût | Fid. appr. | Fid. TEST | Invariance | Pire paire | Source |
|---|---|---|---|---|---|---|---|---|
| Pont linéaire rang 1 (`pont_recurrent.py`, `pont_fidele.py`) | y=(e·W0)·Pᵀ+moy ; 1 792–2 688 nombres ; artefact `pont_semantique_r1.npz` 16 560 o | UDHR art.1, 20 langues apprises / 20 jamais vues | 1 inversion ridge, 3 254 pas | 0,6677 | — | **0,9492** | **0,7762** | `reports/rapport-pont-semantique.md` §5 |
| Pont linéaire rang 128 (`pont_semantique.npz`, 1,38 Mo) | P,W0 896×128 = 230 400 param. | UDHR art.1, 40 langues → 6 tenues | idem | 0,8444 | **0,3691** | 0,2812 | — | idem §7 |
| ELM 2 couches (R aléatoire gelé + tanh, W ajusté) | H=64 : 114 688 p. ; H=256 : 458 752 ; H=4096 : 7 340 032 | idem | 1 inversion | 0,7278 / 0,7753 / 0,8947 | 0,5725 / 0,5795 / 0,5557 | 0,8882 / 0,7855 / 0,6048 | — | idem §7 |
| Réservoir 1 couche récurrente (`pont_reservoir.py`), réglé a=0,2 ride 3·10⁻¹, N=64 | s=(1−a)s+a·tanh(A·s+B·e) ; A,B gelés ; W ajusté ; 118 784 p. | UDHR art.1, 40 langues → 6 non latines | 1 inversion | — | **0,5921** (1 unité) / **0,4767** (10 unités) | **0,9772** / 0,9797 | **0,9576** / 0,9606 | `rapport-pont-semantique.md` §8-10 ; `rapport-pont-generatif.md` §13 |
| Réservoir variantes | N=256 ; N=8 ; ride 10 ; ensemble K=2 ; saut e_t ; rayon 0,7→1,2 | idem | idem | — | 0,5868 / 0,5671 / 0,5653 / 0,6010 / 0,3792 / 0,5924 | 0,8187 / 0,9884 / 0,9989 / 0,8563 / 0,2757 / 0,9076 | 0,6918 / 0,9777 / 0,9978 / 0,7938 / −0,0693 / 0,844 | idem §8-10 |
| Cascade générative + attrition (`pont_generatif.py`) : naissance 1 neurone à la fois, couches réelles, a=0,5 ride 1,0 | 256 neurones · 11 couches ; 1 neurone ; 128 | données PROPRES, 40 langues → 6, 10 unités | Gram recalculée par naissance | 0,7330 (256) | 0,4734 → 0,5059 → **0,5186** | 0,9983 → 0,9327 → 0,8874 | 0,6738 | `rapport-pont-generatif.md` §11-14 |
| Cascade sur données contaminées (comparaison) | 256/9 couches ; 
… [13755 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Sous-agents lancés

- tour 1 — Inventaire corpus dépôt
- tour 1 — Inventaire poids et entraînements

### Commandes exécutées (échantillon)

- **T1** List repo root
- **T1** List tools, reports, docs
- **T1** List remaining tools and data dirs
- **T1** Check pont scripts existence
- **T1** Count lines of target reports
- **T1** Grep recapitulatif for direction work
- **T1** List headings of rapport-toutes-langues
- **T1** Tail headings of big report
- **T1** Headings of recapitulatif
- **T1** Check existence of mission-mentioned files
- **T1** List most recent reports and tools
- **T1** Grep references to direction tools
- **T1** List sprints and journal
- **T1** List recent journal sessions
- **T1** Inspect main pont session report
- **T1** Find Hebb-related reports and code
- **T1** Headings of cancellation note
- **T1** Grep Hebb mentions in big report
- **T1** Inspect corpus dir near repo
- **T1** Find weight artifacts
- **T1** Check save calls in pont scripts
- **T1** Inspect npz weight contents
- **T1** Locate cache npz files
- **T1** Inspect wiki corpus dirs
- **T1** Read headers of corpus producers
- **T1** Measure Wikipedia and Gutenberg corpora
- **T1** Measure UDHR corpora and trace counts
- **T1** Measure UDHR xml and Gutenberg dbs
- **T1** Count corpus files and find Gutenberg
- **T1** Size Gutenberg databases
- **T1** Read headers of pont_fidele and pont_recurrent
- **T1** Read headers of direction tools
- **T1** Read plateau and invariance tool headers
- **T1** List scripts with optimization loops
- **T1** Confirm no torch or backprop
- **T1** Inspect torch-using scripts

## 4. Mesures et résultats marquants

- **T1** `120:| **50 % de l'énergie** | **34** | **4 %** |`
- **T1** `121:| 90 % de l'énergie | 293 | 33 % |`
- **T1** `122:| 99 % de l'énergie | 599 | 67 % |`
- **T1** `205:- Le sous-ensemble actif (34 canaux pour 50 % de l'énergie ; 24 % de canaux non`
- **T1** `365:| énergie 90 % | 645 | 0,4945 | 0,5137 | **+0,0192** | 0,9530 | 0,8440 |`
- **T1** `366:| énergie 75 % | 424 | 0,5319 | 0,5505 | **+0,0186** | 0,9575 | 0,8566 |`
- **T1** `367:| énergie 50 % | 157 | 0,6140 | 0,6346 | **+0,0206** | **0,9653** | **0,8893** |`
- **T1** `424:| énergie 90 % | 645 | 0,5357 | 0,5137 | 0,959 |`
- **T1** `425:| énergie 75 % | 424 | 0,5605 | 0,5505 | 0,982 |`
- **T1** `426:| énergie 50 % | 157 | 0,6030 | 0,6346 | 1,052 |`
- **T1** `702:| 424 (énergie 75 %) | [41, 15, 8, 8, 8] | 0,5536 | 0,6366 | **+0,0830** | 0,6915 | 0,7239 | **+0,0324** |`
- **T1** `703:| **157 (énergie 50 %)** | **[30, 8, 8, 8, 8, 8, 8, 2]** | **0,6383** | **0,7076** | **+0,0693** | **0,7500** | **0,7769** | **+0,0269** |`
- **T1** `750:| énergie 75 % | 424 | 0,5319 | 0,5536 | **+0,0217** |`
- **T1** `751:| énergie 50 % | 157 | 0,6140 | 0,6383 | **+0,0243** |`
- **T1** `752:| énergie 25 % | 23 | 0,7316 | 0,7519 | **+0,0203** |`
- **T1** `753:| **énergie 10 %** | **3** | **0,8991** | **0,9038** | **+0,0047** |`
- **T1** `5263:## 85. NOTRE PONT SUR LA PIRE PAIRE : 14 à 23 % du professeur, et jusqu'à 62 % sur de–fr`
- **T1** `5621:## 89. LOCALITÉ : la couche 8 doit 24 % au jeton, 33 % à trois jetons, et 67 % à autre chose`
- **T1** `5828:### 91.5 Le discriminant de rang 2 — et l'endroit où il est appris`
- **T1** `5913:## 92. LA PIRE PAIRE, APRÈS ÉCHELLE : de–en à 486 % du professeur, mais 5 paires sur 15 échouent`
- **T1** `6069:## 94. RANG 1, 2 OU 3 : le meilleur rang n'est pas celui du meilleur chiffre`
- **T1** `6106:### 94.3 Pourquoi le rang 3 est plus stable que le rang 2`
- **T1** `483:## 9. Le plafond, attaqué : la lecture non linéaire paie +18 %`
- **T1** `journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md:6673:**La méthode** — naissance d'un neurone à la fois, un neurone ajouté ne lit que la couche précédente (et sa propre couche) ; attri`
- **T1** `4221:| **renforcement/atrophie** | **§72** | **+1,7 % du chemin nécessaire** |`
- **T1** `4739:(§69, bornée à 64 %), ni le renforcement/atrophie (§72, +1,7 % du chemin nécessaire).`
- **T1** `plus petit gagnerait ×2 ou ×3 sur la passe avant ; raccourcir l'entrée gagne ×20,`
- **T1** `/home/stephane/Data13TB/stephane/GitHub/Panini-Research/data/mass_ingestion/backlog_gutenberg_de.db 9.4 Mo`
- **T1** `/home/stephane/Data13TB/stephane/GitHub/Panini-Research/data/mass_ingestion/backlog_gutenberg_en.db 21.1 Mo`
- **T1** `/home/stephane/Data13TB/stephane/GitHub/Panini-Research/data/mass_ingestion/backlog_gutenberg_es.db 11.2 Mo`
- **T1** `/home/stephane/Data13TB/stephane/GitHub/Panini-Research/data/mass_ingestion/backlog_gutenberg_fr.db 6.7 Mo`
- **T1** `LE SOUS-ESPACE du rang courant. Comparer un rang 1 et un rang 64 ainsi revient à`
- **T1** `Usage : pont_recurrent.py <dossier_train> <dossier_test> [--couche 10] [--rang 64]`
- **T1** `le rapport contenu/langue à **105 % du professeur**. Mais ce résultat a été obtenu SUR LE`
- **T1** `LA QUESTION. Le §92 montre qu'un discriminant de rang 2 appris sur nos sorties sépare le`
- **T1** `atteint **136 % du RAPPORT** du professeur avec **3,4 % de son énergie de contenu** et`
- **T1** `2,5 % de son énergie de langue. Le rapport est un quotient : deux énergies qui s'effondrent`
- **T1** `* un LLM dense n'a JAMAIS d'activation exactement nulle (**0,00 % de zéros**) :`
- **T1** `* imposer la parcimonie APRÈS l'entraînement plafonne à **−15 % d'événements`
- **T1** `pour +0,6 à +1,2 % de perplexité** — et le seuil absolu est pire encore`
- **T1** `**~22 % de densité**, le push (listes) bat le pull (dense), mesuré sur`

