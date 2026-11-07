# Session 538288b3 — Tu travailles dans /home/stephane/Data13

> **Journaux :** [le jour](../../2026-11-06/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `538288b3-117b-4daf-8d16-0cd8d6b0090d` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-06 21:13 |
| Durée | 0.3 h |
| Tours | 1 |
| Messages | 43 |
| Appels d'outils | 76 |
| Fichiers touchés | 0 |
| Commandes | 45 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7). Mission : **état du chantier A** (le moteur) — lecture seule, aucun code.  Contexte : `docs/pilotage/roadmap.md` (A : A2.6 experts/tête, A6.2, A8.3a, A17, A23, A24…), `docs/pilotage/en-cours.md`, `docs/pilotage/backlog/index.md` + `dependances.md`, les fiches `reports/rapport-a*.md`. A23 a noté : « A2.6 n'est pas li … [1370 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7). Mission : **état du chantier A** (le  … [1650 caractères tronqués]

*76 appels d'outils.* Actions notables :

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
- … et 35 autres

**Synthèse produite :**

⏵ Rejeu d'une porte A8.3a en régime 1 % pour vérifier le chiffre épinglé
Le code compile et les 8 tests de placement passent ; je lance `porte-flux` en régime 1 %.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

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
- … et 5 autres

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

## 5. Erreurs rencontrées

2 sorties en erreur ou divergentes. Les premières :

- **T1** : a26-bilan.json a26-lot-disque.json a83a-coupe.json a83a-flux.json a83a-pont.json a83b-decision.json a83b-lot.json a83b-regimes.json a83c-ctx.json a83c-lot.json a83-defaut.json a83d-lot-threads.json ra
- **T1** : # B13 — le gold corrigé : 4 GP retrouvés, exact 226/226, couverture 0,9456  > **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-06 · **Verdict** : ✅ > **Un défaut du générateur de

