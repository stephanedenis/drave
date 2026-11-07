# Session 538288b3 — Tu travailles dans /home/stephane/Data13

> **Journaux :** [le jour](../../2026-11-06/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `538288b3-117b-4daf-8d16-0cd8d6b0090d` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-06 21:13 |
| Durée | 1.0 h |
| Tours | 1 |
| Messages | 73 |
| Appels d'outils | 126 |
| Fichiers touchés | 2 |
| Commandes | 83 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7). Mission : **état du chantier A** (le moteur) — lecture seule, aucun code.  Contexte : `docs/pilotage/roadmap.md` (A : A2.6 experts/tête, A6.2, A8.3a, A17, A23, A24…), `docs/pilotage/en-cours.md`, `docs/pilotage/backlog/index.md` + `dependances.md`, les fiches `reports/rapport-a*.md`. A23 a noté : « A2.6 n'est pas li … [1370 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7). Mission : **état du chantier A** (le  … [1650 caractères tronqués]

*126 appels d'outils.* Actions notables :

- bash — Show repo root, branch, recent commits
- glob
- bash — Count lines of key documents
- grep
- read
- bash — List report files matching A-numbered variants
- bash — Check for existing target files and git status
- bash — Read prior sibling session digest
- bash — Inspect prior sibling session outcome
- bash — Check if target files ever existed in git
- bash — Check artifacts for A17/A23/A24
- bash — Extract A2.6 mentions with context from A23 report
- bash — List verification tools and placement tests
- bash — Run backlog verification read-only
- … et 81 autres

**Synthèse produite :**

⏵ Clôture : résumé de l'état A

\## Fichiers

Deux fichiers neufs, écrits seuls :
- `reports/rapport-etat-a.md` — l'état détaillé, les tableaux, les commandes de vérification.
- `reports/pensee-etat-a.json` — la version machine (JSON valide, 398 lignes).

Je n'ai rien commité ni stagé. Une autre session a intégré les deux fichiers dans `3caa8938` pendant que je finissais ; mes deux dernières nuances (A6.2 « ressource absente » vs « résidence mono-GPU » ; 8 tests vs 4) sont restées non indexées. Aucun existant modifié, liens vérifiés (3 719 OK).

\## L'état des lignes A

| ligne | état réel | le chiffre |
|---|---|---|
| **A1, A4, A7** | ✅ faits | trace 45,1 Mo, PPL 28,4015 ; 19,3885/15,6017 ; greffe 648 s |
| **A2** | ✅ / ⚠️ A2.6 partiel | KV ×1,93/×5,8 ; lot 503/502 Mio, +27 %, −0,006 % |
| **A3** | ✅ / 🧱 A3.4 bloqué | 1 608 o/flux ; attente 1,01/1,99/4,89 |
| **A5** | ✅ / 🧱 A5.4 bloqué | int8 +3,0 %, f16 +0,018 %, int4 +364 % |
| **A6** | ✅ / A6.2 mal classé | hebbien +3,0 % ; 0 neurone mort/116 736 |
| **A8** | ✅ opt-in, A8.3a **3/19** | 19 pins, 3 duales ; défaut −5,9 → +19,5 % |

**A2.6** : règle générique et KV faits ; `placement.rs` a **8 tests, pas 4** (rejoués 8/8). La tête est **refusée par décision** (`TETE_4BIT.perte_ppl = 10`, test à 5 %), pas par une mesure courante — la fiche se contredit (étape 2 ✅ tête refusée, étape 4 ⏳ tête à faire). Les experts ne sont **pas bloqués par A6.2**.

**A6.2** : **faux bloqué**. Le MoE local existe : `Qwen3-30B-A3B Q4`, 18 Go, 48 couches/128 experts/8 utilisés, machine **2×16 Go VRAM + 125 Go RAM** ; `porte-echange-experts.sh` le prend par défaut. Le « 16 Go » est une **résidence mono-GPU**, pas une absence de modèle.

**A8.3a** : **fait 3/19**, pas « fait ». `DRAVE_PERTE_MAX=1 porte-flux` rejoué **exit 0** (58,3200/62,7357) ; pont 111,8003/115,6406 ; coupe variance 8,9 → 2,4 %. Les 16 autres pins n'ont pas de régime dual ; le défaut reste refusé.

**A17/A23/A24** : ce sont des **identifiants d'audit**, pas des lignes A. A17 = 222/239, 0,9289, 17 spans (historique ; état courant 235/236, 0,9874, 3 spans). A23 = 29 tâches, 6 doublons, 18 périmées ; T18 non appliqué. A24 = 50 phrases, 0 plantage, 34/50 anomalies, 132 chevauchements, 18 correctifs (partiellement appliqués). Collision « A26 » (audit CLI) avec A2.6.

\## La frontière réelle

- **Outil** : `verifie_backlog.py` → **3** (A2.6, N2, N4). **Doc** : **4** (A2.6, N2, N3, N4) — N3 est mesurée, doc périmée.
- **A2.6 y est** parce que `Dépend de A2` et pas de `
… [1710 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `reports/rapport-etat-a.md` | 1 | 3 |
| `reports/pensee-etat-a.json` | 1 | 2 |

### Commandes exécutées (échantillon)

- **T1** Show repo root, branch, recent commits
- **T1** Count lines of key documents
- **T1** List report files matching A-numbered variants
- **T1** Check for existing target files and git status
- **T1** Read prior sibling session digest
- **T1** Inspect prior sibling session outcome
- **T1** Check if target files ever existed in git
- **T1** Check artifacts for A17/A23/A24
- **T1** Extract A2.6 mentions with context from A23 report
- **T1** List verification tools and placement tests
- **T1** Run backlog verification read-only
- **T1** Inspect placement tests
- **T1** Read A2.6 and A8.3a JSON artifacts
- **T1** Inspect cargo package and placement reports
- **T1** Read placement KV and loss rule reports
- **T1** Count A8.0 pinned gate reports and tools
- **T1** Check which gates have dual 1% regime
- **T1** Read A24 audit report head and commands
- **T1** Read A17 spans report head and commands
- **T1** Inspect gold evaluator usage
- **T1** Run thought engine autotest
- **T1** Run gold evaluator to /tmp
- **T1** Inspect frontier computation logic
- **T1** Read frontier and fiche parsing logic
- **T1** Read gold evaluator output
- **T1** Read v12 verdict and A23 verification section
- **T1** Check A17/A23/A24 JSON artifacts and product tests
- **T1** Locate A24 key figures and fixes
- **T1** Read A24 fixes list
- **T1** Read A24 before/after table and sections
- **T1** Read A3.2 and A3.3 fiches
- **T1** Locate A details in archived roadmap
- **T1** List latest reports and gold-related fiches
- **T1** Read latest gold correction report
- **T1** Check autotest and latest partition state
- **T1** Inspect head 4-bit constant and lot script
- **T1** Check Rust toolchain availability
- **T1** Run placement unit tests in /tmp target
- **T1** Locate local GGUF models
- **T1** Inspect porte-flux script
- … et 43 autres

## 4. Mesures et résultats marquants

- **T1** `182-        // Un KV de 1 M de jetons sur un 0,5 B : ~100 Mo lus par jeton.`
- **T1** `202-        // Un petit KV (100 Mo) va en VRAM.`
- **T1** `210-        // Le KV tardif : l'int8 (+0,03 %) passe un budget de 1 % ; l'int4 (+2,7 %) non.`
- **T1** `226-        // +10 % de PPL : elle « tient », mais la place n'est pas la qualité.`
- **T1** `229-        // Et l'int4 global (+364 %) ne passe aucun budget raisonnable.`
- **T1** `236-        // 24 couches : l'int8 passe sur les 12-23 (+0,03 %), pas sur les 0-11 (+2,28 %).`
- **T1** `241-        // Un budget de 3 % laisse passer les deux.`
- **T1** `"preuve": "rapport-placement-kv-8k.md, ×1,93 / ×5,8"`
- **T1** `"preuve": "TETE_4BIT +10 % PPL ; choisir_avec_perte la refuse à 5 %"`
- **T1** `"controle": "choisir_avec_perte refuse la tête 4 bits à 5 % (test) ; sans MoE local, les experts ne sont pas mesurables",`
- **T1** `# Le placement du KV à 8 k : ×1,93 sur le préremplissage, ×5,8 sur l'attention`
- **T1** `est le cas type : sa **lecture par jeton** croît linéairement avec le contexte (5 337 jetons × 24 couches × 2 têtes`
- **T1** `KV × 64 dim × 4 octets ≈ **65,6 Mo par jeton**), et la bande passante de la RAM (~22,5 Go/s mesurés) contre celle`
- **T1** `de la VRAM (~84,9 Go/s mesurés) décide du coût. À quel point la règle se voit-elle sur un contexte long ?`
- **T1** `| **préremplissage** (5 337 jetons) | 297,0 s (18,0 tok/s) | **153,7 s (34,7 tok/s)** | **×1,93** |`
- **T1** `| **attention** (par jeton) | 32,3 ms | **5,6 ms** | **×5,8** |`
- **T1** `| décodage (8 jetons) | 0,696 s (11,5 tok/s) | **0,278 s (28,7 tok/s)** | ×2,5 |`
- **T1** `| total mesuré (par jeton) | 59,0 ms | **32,2 ms** | ×1,84 |`
- **T1** `| TTFT | 55,7 ms | **28,8 ms** | ×1,93 |`
- **T1** `quelques milliers de jetons, va dans la **mémoire la plus rapide où il tient** — et cela vaut **×1,93** sur le`
- **T1** ``placement::kv_precision(couche, n_layer, budget_pct)` : l'**int8** si sa perte **mesurée** (A5.3 : **+2,28 %** sur les`
- **T1** `premières couches, **+0,03 %** sur les dernières) tient dans le budget, le **f32** sinon. C'est`
- **T1** `coûte +10 % de PPL) appliquée au KV. **Deux tests** : les 24 couches (l'int8 passe sur 12-23 seulement), le budget`
- **T1** `3 % (il passe partout), le budget 0 % (nulle part).`
- **T1** `| **la règle place + perte (`DRAVE_PERTE_MAX=1`, budget 1 %)** | **30,7286** |`
- **T1** `- Le coût mesuré est de **−0,12 %** (légèrement *mieux* que le f32) — **dans le bruit** des 255 jetons, à ne pas`
- **T1** `**dans le budget de perte** » — un 4 bits de tête (+10 %) serait refusé par le même budget.`
- **T1** ``porte-coupe` est passée de +0,52-17,09 % à 5,9-11,6 % et a **échoué**. *Un changement de défaut qui déplace les`
- **T1** `| graphème, mot | ✅ | 0 crash, 0 span hors texte, `valeur = texte[debut:fin]` à **100 %**, couverture **49/50 à 100 %** (x46 : 95,14 %, newlines) |`
- **T1** `[still running after 60000ms; moved to background job bash-3979]`
- **T1** `215:| parallèle | 1,51 ms | 6,18 ms | 27,22 ms | 0,136 |`
- **T1** `Un flux d'activations transporté en dense coûte 3,5 ko par jeton. La vision dit que le coût`
- **T1** `octets par flux** à 256 jetons ; le mode « lot en listes » : **1,5 ko/jeton contre 3,5 en`
- **T1** `**Mesurée** — l'attente vaut `calcul distant + 3,2 × latence` : **1,01×** à 0 ms, **1,99×** à`
- **T1** `5 ms, **4,89×** à 20 ms. Le **débit ne compte pas** (0,25 Mbit/s) : c'est la latence qui coûte.`
- **T1** `- latence nulle (0 ms) : le découpage doit rester ≈ 1× — c'est le plancher ;`
- **T1** `- latence élevée (20 ms) : il doit perdre — c'est la pente ;`
- **T1** `45:| A1.1 | **Format de trace** (DRVF v2/v3) : par couche et position, les neurones actifs (indice + valeur) | ✅ | 132 Mo pour 512 jetons (258 ko/jeton) et +8 % de temps ; la v3 (i8, échelle par bloc `
- **T1** `47:| A1.3 | **Le format EST le contrat d'échange** (A3) : versionné, en-tête + paires | ✅ | codec de référence : aller-retour identique sur 132 Mo ; le rejeu redonne les mêmes logits |`
- **T1** `48:| A1.4 | **Profilage par neurone** : densité par couche, part des 10 % les plus forts, neurones dominants | ✅ | densité **20 à 56 %** selon la couche ; top 10 % → **33,1 %** de la magnitude ; **0,0`
- **T1** `49:| A1.5 | **La décision par couche** : la quantification et le chemin (push/pull) choisis par la mesure, couche par couche | ✅ | la **table** (la densité par couche + le croisement 22 %) et la **vér`
- **T1** `57:| A2.1 | **Cache KV sur deux cartes** (paginé) | ✅ | attention à 1 M de clés : 968 → **13,2 ms** |`
- **T1** `58:| A2.2 | **Attention complète sur GPU** (décodage et préremplissage) | ✅ | 22,16 → **3,29 ms/jeton** (÷6,7) |`
- **T1** `59:| A2.3 | **Projections Q8_0 et tête Q6_K sur GPU** (opt-in) | ✅ | 15,6 → 6,2 ms/jeton ; tête : 7,58 → **3,60** |`
- **T1** `60:| A2.4 | **Cache d'experts MXFP4** | ✅ mesuré, **verdict : non** | +6 % — on ne l'active pas tel quel, et c'est écrit |`
- **T1** `61:| A2.5 | **Top-k dans le noyau d'attention GPU** — le dernier chemin qui retombe sur le CPU | ✅ mesuré — opt-in (`DRAVE_GPU_TOPK=1`) | le noyau fusionné (**1 lancement**) gagne jusqu'à ~64 k, la ch`
- **T1** `62:| A2.6 | **Ordonnanceur de placement** : chaque opérateur là où son flux coûte le moins cher (2 GPU, CPU, VRAM, RAM, NVMe) | 🔬 — la règle écrite **et appliquée** | le module [`placement.rs`](../../`
- **T1** `71:| A3.2 | **Granularité** : par couche, par bloc, par expert | ✅ | listes i16, échelles par bloc, indices par écarts : **1 608 octets par flux** à 256 jetons ; le mode « lot en listes » : 1,5 ko/jet`
- **T1** `72:| A3.3 | **Seuil de rentabilité** : à quel débit/latence le découpage gagne | 🔬 | attente ≈ calcul distant + **3,2 × latence** : 1,01× à 0 ms, 1,99× à 5 ms, 4,89× à 20 ms ; le débit ne compte pas (`
- **T1** `96:| A5.2 | **Quantification du KV choisie par la mesure** | ✅ | l'écart int8 (+3,0 % à 8 192) est **attribué aux clés** ; clés f16 = **+0,018 %** pour 39 % de la taille ; l'int4 coûte +364 % — le déb`
- **T1** `97:| A5.3 | **Quantification par bloc, par couche** | ✅ — la sensibilité mesurée, la politique écrite | le coût de l'int8 est **tout** dans les premières couches : 8 bits sur 0-11 → **+2,28 %**, sur 1`
- **T1** `100:**Prochaine action** : aucune — le 8 bits tardif est gratuit (+0,03 %), le 4 bits +2,7 % ; A5.4 est bloquée par le matériel.`
- **T1** `108:| A6.1 | **Capteur hebbien** : apprendre des journaux d'activation | ✅ mesuré — **négatif** | le capteur coûte +3,0 % ; la création de nœuds par Hebb n'ajoute rien sur 69 % des poids ; et les **pr`
- **T1** `110:| A6.3 | **Élagage guidé par les logs** : retirer les neurones qui ne s'allument jamais | ✅ mesuré — le critère est **vide** | **0 neurone mort** sur 116 736 (255 jetons) ; **63 %** s'allument à m`
- **T1** `123:| A7.2 | **Une couche exécutée ailleurs** : la même sortie, un autre nœud | ✅ | le **relais ne change pas un chiffre** (`porte-topologie`, 92 s, 42.5477) ; le coût du flux : **1 608 octets/flux**,`
- **T1** `124:| A7.3 | **La grappe intra-couche** : un sous-ensemble de neurones, pas une frontière de couche | ✅ mesuré | le **top-1024** (21 % des 4 864 neurones FFN) rend la **même perplexité** (30,7286 à qu`
- **T1** `128:**Prochaine action** : aucune sur A7.5 — le transport sparse est **mesuré** (4,44×, fidélité 100 %, 0,125 ms loopback). La suite (exécution d'une couche à distance, WAN) reste **hors plan**.`
- **T1** `139:| A8.2 | **Le terme de perte** : chaque précision a son coût mesuré (PPL) | ✅ `choisir_avec_perte` + **3 tests** | l'int8 tardif (+0,03 %) passe un budget de **1 %**, l'int4 tardif (+2,7 %) exige `
- **T1** `366:| B26.1 | **M6 conflit** | ❌ **nul** | réplication d'A6 : exact **94,95 %** (792 cas), conflit **0**, commutation **0** ; c'est un **sélecteur** sans compétition, pas un contrôle exécutif ; pas de`
- **T1** `424:4. ~~A1.5 / A5.3 — la décision par couche~~ **fait** (l'int8 sur les tardives +0,03 %, le 4 bits +2,7 % — un curseur).`
- **T1** `> **toutes** des paires S × chunker (53,1 % de S qui contient le chunker, 33,5 % l'inverse,`
- **T1** `> 2,5 % de mêmes bornes, 10,9 % de croisements). Le mode **`alternative`** (défaut) garde les deux`
- **T1** `> exact 235/236, POS 85,00 %** — les mesures de la base, **sans déduplication silencieuse**. Le mode`
- **T1** `| **`alternative`** (défaut) | 239 | **0,6482** | **235/236** | +10,4 % |`
- **T1** `| `filtrer_union` | 91 | 0,6163 | 217/239 → 217/218 | +7,2 % |`
- **T1** `| `filtrer` (partition stricte) | **0** | **0,6954** | 217/218 | +2,0 % |`
- **T1** `# A8.3a — le régime 1 % a ses propres références et ses propres plafonds : la`
- **T1** `0, 154 MiB, 16384 MiB, 0 %`
- **T1** `1, 4 MiB, 16384 MiB, 0 %`
- **T1** `{'date': '2026-10-29', 'ligne': 'A2.6', 'verdict': 'partielle', 'controle': 'choisir_avec_perte refuse la tête 4 bits à 5 % (test) ; sans MoE local, les experts ne sont pas mesurables'}`
- **T1** `{'ligne': 'A8.3d', 'date': '2026-10-30', 'verdict': "le lot n'est pas les threads : l'ecart de 1,90 % survit a 1 thread"}`
- **T1** `reports/rapport-a83c-lot.md:40:Mesuré sur Qwen3-30B-A3B : PPL **19,143 contre 19,172** (0,15 %), argmax identique sur`
- **T1** `/dev/mapper/system-root   11T  9,0T  1,9T  83% /home/stephane/Data13TB`
- **T1** `> Verdict : **non — et la mesure a d'abord menti.** Le premier essai donnait **×0,81** (une`
- **T1** `> amélioration de 19 % !) en imposant à A le routage de B à la dernière couche. Les contrôles l'ont`
- **T1** `> démonté : **tout** routage différent y fait varier la perplexité de ±20 à 50 %, **le signe dépend`
- **T1** `> du texte** (A : ×0,81 · A2 : ×1,46 · B en sens inverse : ×1,26), et l'ordre « le routage réel fait`
- **T1** `> ×0,94 contre réel ×1,26). Il n'y a **pas** de gain latéral.`
- **T1** `(0,006 %) — parce que la trace **trie** les experts (« l'ordre de `select_nth` est arbitraire ») et`
- **T1** `(±20 %) aurait baigné dans un artefact de 0,006 % — petit, mais du même genre que ce qu'on cherche.`
- **T1** `**Réponse courte : non.** ×1,09 prédit, pour un plafond absolu de ×1,41 — contre`
- **T1** `un plafond de ×3,1 pour le chantier du dense, qui est déjà nommé.`
- **T1** `| **experts routés** (16 sur 896) | 25,83 | 29,3 % |`
- **T1** `| experts partagés (2 par couche) | 12,40 | 14,1 % |`
- **T1** `| **dense Q8_0** (attention, KDA, MLA, routage) | 48,56 | **55,1 %** |`
- **T1** `| tête de sortie | 1,30 | 1,5 % |`
- **T1** `| 100 % (impossible) | **×1,41** |`
- **T1** `| 70 % | ×1,26 |`
- **T1** `| 47 % | ×1,16 |`
- **T1** `| 25 % | ×1,08 |`
- **T1** `2 × 16 Go = 32 Go. Une matrice d'expert K3 (3 × 3072 × 3584 à 4,25 bits) pèse`
- **T1** `**17,5 Mo** → **1 828 matrices**, soit **19,7 par couche sur 896**.`
- **T1** `reports/rapport-c9-echange-experts.md:9:> amélioration de 19 % !) en imposant à A le routage de B à la dernière couche. Les contrôles l'ont`
- **T1** `reports/rapport-c9-echange-experts.md:10:> démonté : **tout** routage différent y fait varier la perplexité de ±20 à 50 %, **le signe dépend`
- **T1** `reports/rapport-c9-echange-experts.md:11:> du texte** (A : ×0,81 · A2 : ×1,46 · B en sens inverse : ×1,26), et l'ordre « le routage réel fait`
- **T1** `reports/rapport-c9-echange-experts.md:41:| A avec **son** routage (référence) | **37,2013** | ×1,00 |`
- **T1** `reports/rapport-c9-echange-experts.md:42:| A + le routage de **B** (autre texte) | **3 445,03** | **×92,6** |`
- **T1** `reports/rapport-c9-echange-experts.md:43:| A + routage **aléatoire** | 13 958,96 | ×375 |`
- **T1** `reports/rapport-c9-echange-experts.md:44:| A + routage de B **décalé d'une couche** | 37 825,73 | ×1 017 |`
- **T1** `reports/rapport-c9-echange-experts.md:70:| rien (son propre routage) | 37,2013 (×1,00) | 92,4832 (×1,00) | 84,6539 (×1,00) |`
- **T1** `reports/rapport-c9-echange-experts.md:71:| **le routage de l'autre instance** | **30,1705 (×0,81)** | **135,0935 (×1,46)** | **107,0258 (×1,26)** |`
- **T1** `reports/rapport-c9-echange-experts.md:72:| routage **aléatoire** | 35,4832 (×0,95) | 143,1992 (×1,55) | **79,4284 (×0,94)** |`
- **T1** `reports/rapport-c9-echange-experts.md:73:| routage de l'autre **décalé** d'une couche | 37,9628 (×1,02) | — | — |`
- **T1** `reports/rapport-c9-echange-experts.md:80:* **tout** routage différent à la dernière couche fait bouger la perplexité de ±20 à 50 %, y`
- **T1** `reports/rapport-c9-echange-experts.md:86:* le contrôle **décalé** (×1,02) montre qu'un routage cohérent mais mal apparié est inerte — c'est`
- **T1** `bb67dd59 ÉTAT ET JOURNAL — LA NUIT DES P0 : POS 85,00 %, ATTACHEMENT 235/236, FRONTIÈRES 0/40, PARTITION ÉTIQUETÉE, CONTRAT V1`
- **T1** `015d7c56 B13 — LA PARTITION DES SYNTAGMES (P0-3) : meta.alternative PAR DÉFAUT (MESURES INCHANGÉES), filtrer EN OPTION (F1 +0,047) ; outside/feel CORRIGÉS, POS 85,00 %`
- **T1** `5c5d3b52 B13 — LE PAQUET POS SÛR (CLASSES FERMÉES + R4-EN) : POS 83,83 → 84,96 %, 37 CORRIGÉS / 0 CASSÉ, ATTACHEMENT INCHANGÉ ; 183/183`
- **T1** `e2258fb9 DOC PRODUIT — LES CHIFFRES À JOUR : POS 83,83 %, F1 64,74 %, ATTACHEMENT 235/236 (98,33 %), 3 SPANS ; SORTIE D'EVALUER REJOUÉE`
- **T1** `reports/rapport-partition-integree.md:8:> exact 235/236, POS 85,00 %** — les mesures de la base, **sans déduplication silencieuse**. Le mode`
- **T1** `reports/rapport-partition-integree.md:21:| **`alternative`** (défaut) | 239 | **0,6482** | **235/236** | +10,4 % |`
- **T1** `bfd98892 DOC PRODUIT — RESYNCHRONISÉE : POS 85,00 %, F1 0,6482, ATTACHEMENT 235/236, GELÉ 85,32 / 0,6511 ; SORTIE D'EVALUER REJOUÉE`
- **T1** `# S'il est faux, les effets mesurés (±20 %) baignent dans un artefact — et c'est arrivé : la`
- **T1** `57:| 24 | 37,1813 | ×1,00 |`
- **T1** `reports/rapport-partition-syntagmes.md:306:| moins de chevauchements, coût minimal | `filtrer_union` | 0,6163 | 217/239 | 91 | +7,2 % |`
- **T1** `reports/rapport-partition-syntagmes.md:307:| partition stricte, F1 d'abord | `filtrer` | 0,6172 | 205/239 | 0 | +2,0 % |`
- **T1** `48:| **A6** apprendre des flux | ✅ / ⏳ **A6.2 mal classé** | A1, A2 | hebbien +**3,0 %**, produits **+0,0045** de R² ; **0 neurone mort** sur 116 736 ; 63 % < 0,1 % ; top 10 % → **19 %** de la masse |`
- **T1** `60:| **A2.6** | **partiel, libre (P2)** | A2 acquis ; **pas** A6.2 pour les experts ; tête décidée | KV ×1,93/×5,8 ; lot **503/502 Mio**, **24,0 → 30,5 tok/s** (+27 %), PPL **15,8452 → 15,8443** (−0,0`
- **T1** `162:| **A6.2** | **oui** | MoE local 18 Go, 2×16 Go VRAM, 125 Go RAM ; trace et imposition du routage existent ; le MoE tourne en offload/CPU, le blocage « 16 Go » est une résidence mono-GPU | **actio`
- **T1** `-| **A6.2** | **oui** | MoE local 18 Go, 2×16 Go VRAM, 125 Go RAM ; trace et imposition du routage existent | **action 2** |`
- … (tronqué)

## 5. Erreurs rencontrées

2 sorties en erreur ou divergentes. Les premières :

- **T1** : a26-bilan.json a26-lot-disque.json a83a-coupe.json a83a-flux.json a83a-pont.json a83b-decision.json a83b-lot.json a83b-regimes.json a83c-ctx.json a83c-lot.json a83-defaut.json a83d-lot-threads.json ra
- **T1** : # B13 — le gold corrigé : 4 GP retrouvés, exact 226/226, couverture 0,9456  > **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-06 · **Verdict** : ✅ > **Un défaut du générateur de

