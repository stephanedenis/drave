# Session 850eebf1 — Tu travailles dans le dépôt

| | |
|---|---|
| Identifiant | `850eebf1-88b1-443e-b75e-6f89890b35ec` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-08 09:18 |
| Durée | 0.1 h |
| Tours | 1 |
| Messages | 35 |
| Appels d'outils | 60 |
| Fichiers touchés | 0 |
| Commandes | 22 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave » : un moteur d'inférence écrit en Rust dans drave-core/, plus ~100 outils d'analyse en Python dans tools/, des rapports dans reports/, des sprints dans sprints/, et un fichier de reprise REPRISE.md).  MISSION : dresser l'inventaire FACTUEL et CHIFFRÉ de tout ce qui est mesuré dans ce dépôt sur la PARCIMONI … [2112 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave » : un moteur d'inférence éc … [2392 caractères tronqués]

*60 appels d'outils.* Actions notables :

- bash — List repository root
- bash — List key source directories
- grep
- read
- bash — Find CLI flags for sparsity in main.rs
- bash — Locate sparsity settings in main.rs
- bash — Inspect SparseVec definition
- bash — Find SparseVec and push matrix definitions
- bash — Trace flux flags and Options defaults
- bash — Find push/pull decision sites
- bash — Trace --flux usage in main.rs
- bash — Grep density figures in reports and docs
- bash — Grep REPRISE.md for sparsity entries
- bash — List all flux mentions in main.rs
- … et 11 autres

**Synthèse produite :**

⏵ Rapport livré au parent ; restitution du résultat

Inventaire factuel et chiffré — parcimonie des activations et mode événementiel (Drave). Aucun fichier modifié, aucune compilation lancée.
Légende : **[M]** mesuré dans le dépôt · **[D]** déduit/projeté par l'auteur du rapport source · **[S]** supposé. Toutes les mesures [M] sont sur 2×Xeon E5-2687W v3, 16 threads (`reports/rapport-cpu-aer.md:14`).

\## 1. Le mécanisme exact
- Un **événement** = une activation quantifiée non nulle poussée vers ses destinations : `SparseVec { idx: Vec<u32>, val: Vec<i32> }` (`engine.rs:29-32`) ; en mode listes « une paire EST un événement » (`model.rs:4535-4540`, test `list.rs:1591`). Événement ≠ paire payée : les chemins denses (MLA f32, experts IQ déquantifiés, tête, 4 bits) paient la matrice entière sans liste (`rapport-p0-flux.md:29-34`).
- Construction : `quant_scratch(x, levels, thresh, topk, renorm, scratch)` (`model.rs:4401-4451`). Échelle `s = max|x|/levels` (4406), `q = round(v/s)` (4428/4446). Si `topk>0` → **k-WTA** : `k = round(topk/1000 × dimension)` borné `[1,dim]` (4419-4420) ; seuil = (len−k)-ième magnitude via `select_nth_unstable_by` (4425) ; garde si `|v| ≥ cut` **et** `q ≠ 0` (4426-4429). `topk` est un **pour-mille de la dimension**, pas un k absolu. Sinon seuil absolu : `q ≠ 0` et `|q| > thresh×levels` (4409, 4447). `renorm` remet la L1 des gardés à celle du vecteur complet (4431-4443).
- Défauts : `act_levels=127` (8 bits) en inférence/modes flux (`main.rs:873,2493` ; `model.rs:4339`), `32767` (16 bits) en perplexité (`main.rs:5091`) ; `act_thresh=0.0`, `act_topk=0`, `act_renorm=false`, `act_topk_proj=[0;7]`, `attn_topk=qk_topk=moe_topk=0` (`model.rs:4339-4341`) ; `seuil_push=0.22` (`model.rs:4358`).
- CLI : `--act-thresh`, `--act-topk`, `--topk-q/k/v/o/gate/up/down` (`main.rs:754-762`), `--act-renorm` (781), `--abits` (736 ; niveaux = `(1<<(abits−1))−1`, borné 16, `main.rs:2477-2490`), `--attn-topk/--qk-topk/--moe-topk` (742-747), `--profil-neurones` (791). **Aucune option `--act-levels`** : les niveaux ne se règlent que par `--abits`.
- `--flux` n'est **pas** le mode événementiel : c'est la sortie texte en flux (`main.rs:591,1156`). Le transport en listes = `--flux-liste`/`--flux-blocs` (771-772), protocole TCP v6, en-tête 79 o portant le contrat d'activation complet (`main.rs:2525,2558-2561`).
- Bascule dense→liste : `matvec` choisit push/pull selon `frac > seuil_push` (`model.rs:4492-4504`) ; `--auto` charge les deux et bascule par mesure, `--pus
… [8603 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** List repository root
- **T1** List key source directories
- **T1** Find CLI flags for sparsity in main.rs
- **T1** Locate sparsity settings in main.rs
- **T1** Inspect SparseVec definition
- **T1** Find SparseVec and push matrix definitions
- **T1** Trace flux flags and Options defaults
- **T1** Find push/pull decision sites
- **T1** Trace --flux usage in main.rs
- **T1** Grep density figures in reports and docs
- **T1** Grep REPRISE.md for sparsity entries
- **T1** List all flux mentions in main.rs
- **T1** Find abits defaults per mode
- **T1** Locate quantifier and trace write sites
- **T1** Read profiling threshold section
- **T1** Read trace write contexts
- **T1** Inspect run_sparsity.py counters
- **T1** Grep event counts in optimisation reports
- **T1** Read tool header and key doc excerpts
- **T1** Grep events per token figures
- **T1** Read hardware rates and mode-4 speedup source
- **T1** Verify remaining cited lines

## 4. Mesures et résultats marquants

- **T1** `reports/rapport-8bits.md:7:- densité : **99.2 %**`
- **T1** `reports/rapport-analyse-flux.md:14:Le croisement push/pull du projet est mesuré à **~10 % de densité**. Ce qui`
- **T1** `reports/rapport-analyse-flux.md:30:Neurones actifs dans au moins 90 % des jetons, par couche : **0,89 % à 1,90 %**`
- **T1** `reports/rapport-analyse-flux.md:56:Le croisement push/pull mesuré du projet est à ~10 % de densité. Avec les densités`
- **T1** `reports/rapport-attention-creuse.md:39:matrice **creuse à ~12,5 %**. Et cette densité **décroît avec le contexte** :`
- **T1** `reports/rapport-attention-creuse.md:110:| Poids creux, donc listables | ✅ 12,5 % de densité à 256, 0,8 % à 4 096 |`
- **T1** `reports/rapport-coherence-docs-2.md:82:| 28 | `docs/format-flux.md:58-61`, `REPRISE.md:248,340-341`, `docs/roadmap.md:94` | v3 : **45 079 930 o** (−32,1 % vs v2), rejeu 19,4029 (+0,074 %), 21 630 645 `
- **T1** `reports/rapport-coherence-docs.md:113:| 35 | `reports/rapport-transport-liste.md:25` | listes seuil 0,00 : **3 622** pour 100,0 % (896 actifs) | 39 + 4 × 896 = **3 623** ; l'octet manquant n'est pas e`
- **T1** `reports/rapport-coherence-docs.md:128:| 45 | `README.md:34` | « Croisement push/pull à **10 %** de densité ✅ mesuré » | `reports/rapport-croisement-push-pull.md:43` : « **~22 %** … pas à 10 » ; le REA`
- **T1** `reports/rapport-coherence-docs.md:248:| OK | **17** | formats des modes 2 et 3 · `flux_brut` · `hôte:port` · trace dense 66 370 408 o (fichier réellement relu) · 66 370 406 hors sentinelle · 24 576 li`
- **T1** `reports/rapport-coherence-vision.md:70:| `comparaison-spiking.md` | **corrigé, 4 sites** | encadré : le spike est un **moyen** d'obtenir la parcimonie, le cœur de Drave (grappes + lecture des flux) n'`
- **T1** `reports/rapport-cpu-aer.md:32:## Projection 7B (densité 5 %, 0,476 b/poids)`
- **T1** `reports/rapport-croisement-push-pull.md:43:➡️ **Les deux architectures se croisent à ~22 % de densité d'activation**, pas à`
- **T1** `reports/rapport-croisement-push-pull.md:44:10 %. Le chiffre se lit dans le rapport à pleine densité : le pull traite 4,7 fois`
- **T1** `reports/rapport-croisement-push-pull.md:101:que la densité baisse — ×1,47 à 5 % de densité. Le choix n'est plus une`
- **T1** `reports/rapport-croisement-push-pull.md:106:1. **Sur CPU, le mode pull est le bon choix** au-dessus de 22 % de densité. Le`
- **T1** `reports/rapport-encodage.md:59:**Bascule vers 20 % de densité** : au-dessus, le bitmap + signe gagne (les`
- **T1** `reports/rapport-encodage.md:69:2. **Le gain dépend entièrement de la densité** : ~×1,3 à 12,5 %, ×2,2 à 5 %,`
- **T1** `reports/rapport-encodage.md:83:> *densités atteignables* viennent du MLP jouet : sur un LLM réel, 5-12 % de`
- **T1** `reports/rapport-eparsite.md:7:- poids non nuls : **26.3 %** (densité d = 0.263)`
- **T1** `reports/rapport-eparsite.md:63:3. **Le CSR, lui, est disqualifié** : rentable seulement sous 6 % (indice 32 b) ou 12 % (indice 16 b) de densité — un régime que les LLM n'atteignent pas sans s'effondre`
- **T1** `reports/rapport-eparsite.md:65:5. **Recommandation** : garder le dense 2 bits comme chemin nominal (simple, déterministe, déjà validé) et ajouter un **encodage bitmap + signe** là où la densité est fa`
- **T1** `reports/rapport-eparsite.md:70:- La densité naturelle (26.3 %) est propre à ce modèle. Un modèle **entraîné** en ternaire (BitNet b1.58) tourne plutôt autour de 50-70 % de non-nuls : le gain du bitmap`
- **T1** `reports/rapport-inference.md:86:Montée en charge de l'inférence (meilleur de 2, densité 100 %) :`
- **T1** `reports/rapport-inference.md:196:   1,44 octet par poids — contre 1,06 pour Q8_0 dense. À 99 % de densité, les listes`
- **T1** `reports/rapport-inference.md:262:gros, parce qu'à 99 % de densité chaque poids a besoin de son octet d'écart.)*`
- **T1** `reports/rapport-localite-activation.md:24:| opérateurs creux par neurone | chemin par **listes d'événements** (`SparseVec`, push) | bascule push/pull mesurée à **22 % de densité** (`seuil_push = 0.22``
- **T1** `reports/rapport-localite-activation.md:37:(mesuré : densité de 51 104 %).`
- **T1** `reports/rapport-localite-activation.md:43:| densité d'activation (seuil 5 % du max) | **17,9 %** des neurones par jeton (82 % ne font rien) |`
- **T1** `reports/rapport-localite-activation.md:49:**Lecture** : la localité existe (82 % des neurones sont inactifs par jeton) mais`
- **T1** `reports/rapport-mode-listes.md:7:Mesures sur **qwen2 Q8_0** (494.0 M poids, densité 99.2 %).`
- **T1** `reports/rapport-mur-memoire-4bits.md:55:À 10 % de densité le push est ×2,1 plus rapide ; à 1 %, ×8,3. L'affirmation`
- **T1** `reports/rapport-optimisations-auto.md:117:modèle (densité 5,1 % ⇒ perplexité ×107). Détail dans`
- **T1** `reports/rapport-optimisations.md:5:sorties, **4 303 745 événements** (ternaire issu des signes réels, densité 100 %).`
- **T1** `reports/rapport-optimisations.md:21:Les écarts d'un octet (99,99 % des événements à forte densité) sont décodés **8 à`
- **T1** `reports/rapport-optimisations.md:63:## Montée en charge (meilleur de 3 passes, densité 100 %)`
- **T1** `reports/rapport-passage-a-l-echelle.md:39:| listes d'événements (`PushMat`) | **1,98** | densité d'activation < 22 % |`
- **T1** `reports/rapport-passage-a-l-echelle.md:40:| int8 dense (`DenseQ8`) | 1,00 | densité > 22 % |`
- **T1** `reports/rapport-passage-a-l-echelle.md:176:| le croisement est à 22 % de densité | l'événementiel n'est rentable que sur une parcimonie **structurelle** |`
- **T1** `reports/rapport-toutes-langues.md:356:| **canaux actifs dans TOUTES les langues** | **48 / 896 (5 %)** |`
- **T1** `reports/rapport-toutes-langues.md:366:Autrement dit **95 % des canaux ne sont pas universellement actifs** — ils`
- **T1** `reports/rapport-valeur-unaire.md:8:- zéros : **12.9 %** des poids (densité 87.1 %)`
- **T1** `docs/comparaison-spiking.md:70:qui s'active » reste théorique. À seuil 5 % du max, la densité mesurée tombe à`
- **T1** `docs/convertisseur.md:231:dessous du croisement mesuré à 22 % de densité : le régime où l'architecture`
- **T1** `docs/format-flux.md:64:| neurones actifs | 22 008 776 | 21 630 645 (−1,7 % : les valeurs qui s'arrondissent à zéro ne sont pas écrites) |`
- **T1** `docs/glossaire.md:940:| `tools/profil_flux.py` | densité par couche, part des 10 % les plus forts, export CSV | `docs/roadmap.md:129-149` |`
- **T1** `docs/glossaire.md:1354:**Croisement push/pull (≈22 %)** — La densité d'activation à laquelle le coût des`
- **T1** `docs/glossaire.md:1366:La densité **par couche** varie de 20 % à 56 %, donc la décision push/pull est une`
- **T1** `docs/glossaire.md:1532:   mesuré à **~10 % de densité** » — contredit par`
- **T1** `docs/glossaire.md:1534:   croisent à **~22 % de densité d'activation**, pas à 10 % », et par`
- **T1** `docs/histoire.md:12:| **le virage événementiel** | l'idée qui a tout changé : ne plus multiplier des matrices, mais **pousser des listes d'activation** vers leurs destinations (AER, *Address Event Rep`
- **T1** `docs/plan-mode4-lot-listes.md:112:| un jeton, mode 2 (seuil 0,01, 78,6 % d'actifs) | `79 + 8 + 112 + 2a` | 1 607 | 1 607 |`
- **T1** `docs/roadmap.md:15:| 0.1 | **Format de trace du flux** : par (couche, position), la liste des neurones actifs (indice + valeur), l'échelle, le nombre | ✅ | écrit et relu sans perte ; **132 Mo pour 512`
- **T1** `docs/roadmap.md:18:| 0.4 | **Profilage par neurone généralisé** : trace exploitable par couche et par expert, pas seulement des compteurs | ✅ | `tools/profil_flux.py` : densité par couche, part des 10`
- **T1** `docs/roadmap.md:28:| 1.2 | **Quantification choisie par la mesure** : par couche, par tenseur, plutôt qu'un réglage global | 🔬 | la densité par couche varie de **20 % à 56 %** (`reports/rapport-analys`
- **T1** `docs/roadmap.md:137:| réglage | densité par couche | taille de trace | top 10 % portent |`
- **T1** `docs/vision.md:46:**mesuré** : en dessous d'environ **22 % de densité**, le push (listes) bat le`
- **T1** `docs/vision.md:55:La densité observée, elle, dépend du modèle et de la couche : **17,9 %** sur`
- **T1** `docs/vision.md:243:* la densité d'activation (17,9 %) est l'argument énergétique : **on ne lit que`
- **T1** `docs/vision.md:253:* **ce n'est pas « le sparse gagne toujours »** : le croisement à ~22 % de densité`
- **T1** `731:1. **Mesurer avant de conclure.** Le croisement push/pull était annoncé à 10 %,`
- **T1** `1582:| sparsité de l'entrée | densité 5,1 % ⇒ perplexité **×107** |`
- **T1** `for (seuil, nom) in [(0.9f32, "> 90 %"), (0.5, "> 50 %"), (0.1, "> 10 %")] {`
- **T1** `// sur 128, soit 6 % du FFN — et c'est le régime où l'architecture`
- **T1** `reports/rapport-passage-a-l-echelle.md:178:| l'accumulateur décide du débit en régime creux (mesuré : ×1,7 entre 4 et 32 threads sur des événements épars) | le **tuilage de la dimension de sortie** es`
- **T1** `reports/rapport-passage-a-l-echelle.md:179:| QSFP+ 4,8 Go/s, NVLink 25,78 Go/s, PCIe x8 6,5 Go/s | le flux d'événements adressé par destination est un protocole réseau naturel : c'est la thèse du CDC,`
- **T1** `reports/rapport-mur-memoire-4bits.md:20:> 180,7 G événements — les trois modes empruntent donc bien des chemins`
- **T1** `reports/rapport-mur-memoire-4bits.md:52:le push ne traite d'événements, donc l'égalité tombe vers 1/4,7 = 21 %. Le seuil`
- **T1** `Matrice réelle `blk.0.ffn_gate.weight` de Qwen2.5-0.5B-Q8_0 : 4864 entrées × 896`
- **T1** `sorties, **4 303 745 événements** (ternaire issu des signes réels, densité 100 %).`
- **T1** `**0,484 ms → 0,011 ms** (×44). C'est ce qui rend le débit *variable* exploitable :`
- **T1** `Les écarts d'un octet (99,99 % des événements à forte densité) sont décodés **8 à`
- **T1** `| listes d'événements (`PushMat`) | **1,98** | densité d'activation < 22 % |`
- **T1** `| int8 dense (`DenseQ8`) | 1,00 | densité > 22 % |`
- **T1** `Bande passante atteinte sur cette machine : **20–25 Go/s** (théorique ≈ 68 Go/s`
- **T1** `**mesuré** : en dessous d'environ **22 % de densité**, le push (listes) bat le`
- **T1** `+0,074 % près** (19,4029 contre 19,3885) et l'écart d'activation entre le calcul`
- **T1** `La densité observée, elle, dépend du modèle et de la couche : **17,9 %** sur`
- **T1** `| trace dense, 512 jetons | 132 396 736 o | **66 370 408 o (−49,87 %)** |`
- **T1** `| trace dense, 512 jetons | 66 370 408 o | **45 079 930 o (−32,1 %)** |`
- **T1** `| rejeu `--flux-forcer` | 19,3885 | **19,4029 (+0,074 %)** |`
- **T1** `| neurones actifs | 22 008 776 | 21 630 645 (−1,7 % : les valeurs qui s'arrondissent à zéro ne sont pas écrites) |`
- **T1** `| erreur par valeur | nulle | RMS **0,085 %** du max de la liste (max 0,394 %) |`
- **T1** `reports/bilan-multi-materiel.md:46:| CPU (16 threads) | **5,3 G évts/s** mesuré | ~57 nJ |`
- **T1** `reports/bilan-multi-materiel.md:47:| FPGA (1 carte, 51 voies) | 4,83 G évts/s *projeté* (limite DDR3) | **~8,3 nJ** |`
- **T1** `reports/bilan-multi-materiel.md:48:| GPU (dispersion) | **18,1 G évts/s** mesuré | ~12,7 nJ |`
- **T1** `reports/bilan-multi-materiel.md:56:| GPU | 18,1 G évts/s de dispersion, 380 Go/s de lecture |`
- **T1** `reports/bilan-multi-materiel.md:93:| « Fusion divergente au rang 0 » et « 7,53 G évts/s » | **Fausses** — un état partagé à deux contrats de nettoyage ; valeurs réelles 3,66 / 4,99 G |`
- **T1** `reports/bilan-multi-materiel.md:109:Une carte = 4,83 G évts/s = **un CPU 20 cœurs**, pour 41 % de la logique et 41 %`
- **T1** `reports/rapport-coherence-vision.md:55:| `programme-recherche.md` | **cohérent, 4 sites** | 4ᵉ propriété structurelle « **le flux se route** » ; 5,3 G événements/s sourcé |`
- **T1** `reports/rapport-cpu-aer.md:17:- dispersion (`np.bincount`) : **183999808.87 G événements/s**`
- **T1** `reports/rapport-cpu-aer.md:18:- dispersion (`np.add.at`) : 364797216.41 G événements/s`
- **T1** `reports/rapport-cpu-aer.md:25:| Dispersion pure | 0,96 G év/s | 3,46 | 3,20 | 3,22 |`
- **T1** `reports/rapport-cpu-aer.md:37:| CPU, borné noyau (7,79 G év/s) | 44.93 | 22.3 |`
- **T1** `reports/rapport-cpu-aer.md:48:   cache : 183999808.9 G événements/s mesurés contre 0.35 G nécessaires par token.`
- **T1** `reports/rapport-croisement-push-pull.md:96:| 200 | 22 % | 0 év — 9,6 s | 18,1 G év — 8,7 s (bascule) |`
- **T1** `reports/rapport-croisement-push-pull.md:97:| 100 | 11 % | 0 év — 9,1 s | 9,1 G év — **7,1 s** |`
- **T1** `reports/rapport-croisement-push-pull.md:98:| 50 | 5 % | 0 év — 9,1 s | 4,5 G év — **6,2 s** |`
- **T1** `reports/rapport-inference.md:84:| Débit pendant le forward | **3,9 G événements/s** |`
- **T1** `reports/rapport-inference.md:183:3. Le débit est **entièrement déterminé par le nombre d'événements** : 3,9 G év/s,`
- **T1** `reports/rapport-inference.md:193:2. **Aucun avantage de cadence brute** : 3,9 G événements/s sur 20 cœurs ≈ 1 événement`
- **T1** `reports/rapport-inference.md:219:identiques. Le débit par événement passe de 3,6 à **5,3 G év/s**.`
- **T1** `reports/rapport-inference.md:271:| 100 % | 352,7 M | 10,33 | 3,56 G év/s |`
- **T1** `reports/rapport-inference.md:272:| 50 % | 178,6 M | 12,17 | 2,28 G év/s |`
- **T1** `reports/rapport-inference.md:273:| 25 % | 89,5 M | 15,64 | 1,43 G év/s |`
- **T1** `reports/rapport-inference.md:274:| 10 % | 35,6 M | 21,40 | 0,88 G év/s |`
- **T1** `reports/rapport-optimisations.md:48:| 1 % | 43 560 | 0,14 G év/s | 0,42 G év/s |`
- **T1** `reports/rapport-optimisations.md:49:| 5 % | 216 960 | 1,15 G év/s | 1,50 G év/s |`
- **T1** `reports/rapport-optimisations.md:50:| 10 % | 430 359 | 1,81 G év/s | 2,30 G év/s |`
- **T1** `| CPU (16 threads) | **5,3 G évts/s** mesuré | ~57 nJ |`
- **T1** `| FPGA (1 carte, 51 voies) | 4,83 G évts/s *projeté* (limite DDR3) | **~8,3 nJ** |`
- **T1** `| GPU (dispersion) | **18,1 G évts/s** mesuré | ~12,7 nJ |`
- **T1** `| FPGA | 1 événement/cycle/voie, **0,86 mesuré** avec le lecteur ; optimum à 32 PE pour le banc seul (177 MHz) |`
- **T1** `| GPU | 18,1 G évts/s de dispersion, 380 Go/s de lecture |`
- **T1** `| Énergie par opération | E_AC = 0,9 pJ contre E_MAC = 4,5 pJ (Horowitz) | 8,3 nJ/événement (FPGA, **projeté** : 4,83 G évts/s, limite DDR3) contre 57 nJ (CPU, **mesuré**) — rapport 6,9× |`
- **T1** `qui s'active » reste théorique. À seuil 5 % du max, la densité mesurée tombe à`
- **T1** `**17,9 %** — sous le croisement push/pull de **22 %**`
- **T1** `reports/rapport-coherence-docs-2.md:89:| 35 | `reports/rapport-session-2026-09-30.md:12`, `reports/rapport-prefill-reparti.md:57-61,72-78`, `REPRISE.md:377-379` | mode lot : **18×** à 20 ms (2,6 s con`
- **T1** `reports/rapport-empreinte-memoire.md:319:**18×**. Un préchargement prédictif, même parfait, ne masquerait que **6 %** de`
- **T1** `reports/rapport-prefill-reparti.md:81:les deux tableaux : moins d'allers-retours sur un lien distant (18× à 20 ms), et`
- … (tronqué)

## 5. Erreurs rencontrées

1 sorties en erreur ou divergentes. Les premières :

- **T1** : === struct === [exit code: 1]

