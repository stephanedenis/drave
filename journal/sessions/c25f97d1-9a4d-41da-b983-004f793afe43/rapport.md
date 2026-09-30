# Session c25f97d1 — Tu travailles dans le dépôt

| | |
|---|---|
| Identifiant | `c25f97d1-9a4d-41da-b983-004f793afe43` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-09-30 11:47 |
| Durée | 0.2 h |
| Tours | 1 |
| Messages | 73 |
| Appels d'outils | 104 |
| Fichiers touchés | 1 |
| Commandes | 77 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave » : moteur d'inférence LLM en Rust, `std` seul, paquet `drave-core`, binaire `drave`). Toute la documentation et les rapports sont en FRANÇAIS : écris en français.  CONTEXTE UTILE : ce dépôt a un mode d'échec récurrent, documenté par ses auteurs : un drapeau de ligne de commande ou une variable d'environnem … [2866 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave » : moteur d'inférence LLM e … [3146 caractères tronqués]

*104 appels d'outils.* Actions notables :

- bash — Lister le dépôt et les sources
- bash — Vérifier rapports, modèle et binaire
- bash — Extraire la structure Options
- bash — Lister les fonctions de main.rs
- read
- bash — Chercher toutes les variables d'environnement
- bash — Lister tous les accès opt.champ
- bash — Lister les affectations mdl.champ
- bash — Chercher les champs du modèle dans model.rs
- bash — Vérifier les statiques globales bits et pin
- bash — Chercher les mentions d'options ignorées
- bash — Historique git récent
- bash — Lire REPRISE.md et histoire.md
- bash — Chercher la doc des variables DRAVE_
- … et 75 autres

**Synthèse produite :**

⏵ Audit terminé, rapport écrit et transmis au parent

Rapport écrit : `reports/rapport-drapeaux-ignores.md` (234 lignes, français, tableaux + preuves de code + 4 vérifications empiriques + recommandation).

**Résumé (10 lignes)**
1. **110 options auditées** : 84 drapeaux `--xxx` (extraits d'`analyser`, main.rs:396-519) + 26 variables `DRAVE_*`.
2. **46 drapeaux (55 %) sont ignorés dans au moins un mode où ils devraient s'appliquer**, dont 20 classés critiques ; 5 de plus le sont sur le sous-chemin `--topk` de l'inférence ; 1 variable (`DRAVE_FLUX_VERIF`) est muette dès `--lot > 1`.
3. **N°1** — `--topk-q/-k/-v/-o/-gate/-up/-down` (+ `--attn-topk`, `--qk-topk`, `--moe-topk`) ne sont ni appliqués ni transportés en `--flux-serveur`/`--ppl-reparti` : **deux nœuds divergent en silence** (main.rs:1214-1220 ; en-tête `Act` 1265-1270, 1412-1415) — le correctif `--abits`/`--act-thresh` est donc incomplet.
4. **N°2** — `--keep` ignoré en `--ppl` (`Model::load(…, 1.0, …)` en dur, main.rs:2707) : PPL 1929.3230 **identique** avec et sans `--keep 0.05`, alors qu'en `--infer` les jetons changent.
5. **N°3** — `--ffn-gain` ignoré en `--infer` (prouvé : jetons `[6, 25010, 10, 4999]` avec et sans) alors qu'il fait passer la PPL de 1929,3 à 4949,5 en `--ppl`.
6. Autres : mode par défaut qui a gardé la boucle `i += 2` (`--dense --threads 4` → 30 fils, prouvé) · `--banc-vision` ne reçoit aucune `Options` · `--threads`=16 en dur en FS/PR/BM/BV · `--hebb-q`/`--hebb-out` en dur en `--ppl` · `--sans-yarn` ignoré en FS/PR et trace `[config] rotation` mensongère · `--plan` annonce 512 au lieu des 32768 déclarés · précédence `--sans-fenetre`/`--attn-window` inversée entre `--infer` et `--ppl`.
7. Ce qui est correct : `--abits/--act-thresh/--act-topk/--act-renorm` partout, `--pin` et `--bits` globaux (516-517), les réglages d'activation voyagent dans le flux, `--ppl-texte`/`--depuis`/`--trace-flux`+`--lot`/`--patch`/`--q4`.
8. Recommandation : `--options-actives` (imprime les réglages réellement en vigueur lus sur `mdl` après toutes les affectations, signale tout drapeau d'`argv` absent) + `--options-strict`, suppression des `..` dans les déstructurations, transport de tous les champs d'activation avec `VERSION_FLUX` incrémenté, test de non-régression sur la liste des 84 drapeaux.
9. Réserve : `main.rs` a été **modifié pendant l'audit** (zone flux, +167 lignes, `--lot` maintenant appliqué en `--ppl-reparti`) ; les numéros cités valent pour la révision `1726f9ac…` (2999 l., 11:54:25) e
… [184 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-drapeaux-ignores.md` | 1 | 9 |

### Commandes exécutées (échantillon)

- **T1** Lister le dépôt et les sources
- **T1** Vérifier rapports, modèle et binaire
- **T1** Extraire la structure Options
- **T1** Lister les fonctions de main.rs
- **T1** Chercher toutes les variables d'environnement
- **T1** Lister tous les accès opt.champ
- **T1** Lister les affectations mdl.champ
- **T1** Chercher les champs du modèle dans model.rs
- **T1** Vérifier les statiques globales bits et pin
- **T1** Chercher les mentions d'options ignorées
- **T1** Historique git récent
- **T1** Lire REPRISE.md et histoire.md
- **T1** Chercher la doc des variables DRAVE_
- **T1** Mapper chaque champ aux fonctions qui le citent
- **T1** Extraire toutes les variables DRAVE_ citées
- **T1** Vérifier l'usage de --lot et mdl.lot
- **T1** Vérifier generate/lot et DRAVE_FLUX_VERIF
- **T1** Vérifier BITS_POIDS et DenseQ8
- **T1** Vérifier trace et rejeu dans forward/forward_lot
- **T1** Chercher la documentation de drapeaux précis
- **T1** Chercher un corpus de test existant
- **T1** Test T3 : --plan sans --ctx
- **T1** Extraire la ligne contexte du plan
- **T1** Vérifier le contexte déclaré du modèle
- **T1** Vérifier la branche else de --plan
- **T1** T1a : perplexité de référence
- **T1** T1b : perplexité avec --keep 0.05
- **T1** T1c : inférence de référence
- **T1** T1d : inférence avec --keep 0.05
- **T1** T2a : --ffn-gain en perplexité
- **T1** T2b : --ffn-gain en inférence (attendu ignoré)
- **T1** Vérifier le message poids gardés
- **T1** Lire envoyer_flux et l'en-tête Act
- **T1** Vérifier l'usage réel de attn_sinks
- **T1** Lire l'en-tête du flux et le chemin attn_sinks
- **T1** Vérifier gpu.rs et les appels GPU
- **T1** Lire la logique YaRN
- **T1** Tracer cfg.yarn dans model.rs
- **T1** Vérifier l'usage de cfg.yarn au chargement et en forward
- **T1** Test : drapeau booléen avant --threads
- … et 37 autres

## 4. Mesures et résultats marquants

- **T1** `docs/convertisseur.md:102:  Un plan de placement qui ignore les nœuds NUMA laisse 20 % sur la table, et`
- **T1** `af18f29 Transport en listes à 1 024 jetons : ÷2,3 pour 1,3 % d'écart`
- **T1** `| 3 | KV int8 puis int4 | **fait, jusqu'à 8 192** | **échelles par bloc de 32** : int8 +**1,5 %** à 512 (était +7,1 %), **+3,0 % à 8 192** (llama.cpp +0,8 %) ; int4 **+364 % à 8 192** contre +494 % po`
- **T1** `| 4 | préremplissage par lots | **fait, −20 % et attribué** | tuilage, **attention groupée dans le lot** et **tête en lot** (`logits_lot`) : Qwen ctx 512, **17,1 s → 13,6 s (−20 %)** à perplexité égal`
- **T1** `| 5 | échelles par bloc pour `DenseQ8` | **fait, hypothèse réfutée** | 23,696 contre 23,612 : les échelles par bloc n'apportent rien ; l'avantage du 6 bits est son coût (25 % d'octets en moins à quali`
- **T1** `| 7 | noyaux GPU | **fait, quatre formats** | warp par ligne : tête **Q8_0** (1,6 ms contre 7,3 CPU, écart 2e-7), **MXFP4** (0,1 ms, écart **0,00e0** — bit à bit), **Q4_K** (0,5 contre 1,2 ms, 4e-7), `
- **T1** `| 8 | suite du plan 1 M | **fait pour E4/E5** | **E4 KV déporté en VRAM** : noyaux `attn_kv_*` (tuiles de 32 clés, softmax en ligne, recombinaison + puits), miroir du cache **paginé** (capacité doublé`
- **T1** `| noyau GPU Q8_0 warp (tête Qwen 0.5B, 144,6 Mo) | **1,6 ms** contre 7,3 ms CPU (×4,6), écart 2e-7 |`
- **T1** `| noyau GPU MXFP4 warp (expert gpt-oss, 4,4 Mo) | **0,1 ms** contre 7,5 ms CPU (×75), écart **0,00e0** |`
- **T1** `| noyau GPU Q4_K warp (Qwen 1.5B, 7,7 Mo) | 0,5 ms contre 1,2 ms CPU (×2,2), écart 4e-7 |`
- **T1** `| noyau GPU Q6_K warp (tête liée Qwen 1.5B, 191,4 Mo) | **3,6 ms** contre 8,3 ms CPU 16 fils (23,2 → 53,6 Go/s), écart 3,3e-7 |`
- **T1** `| noyau GPU Q6_K warp (ffn_down Qwen 1.5B, 11,3 Mo) | **0,3 ms** contre 1,5 ms CPU (×5), écart 7,1e-7 |`
- **T1** `| tête Q6_K déportée (Qwen 1.5B Q4_K_M, ctx 256, 510 jetons) | 7,58 → **3,60 ms/jeton** ; bout en bout 44,4 → 41,4 s (−7 %) ; lot 512 : 36,0 → 34,0 s ; **perplexité identique** (13,6877 / 13,6864) |`
- **T1** `| préremplissage par lots (Qwen, ctx 512) | lot 1 = **17,1 s** · lot 512 = **13,6 s** → **−20 %** (perplexité 13,1368 → 13,1359) |`
- **T1** `docs/contexte-long.md:104:| E4 | **KV déporté sur les 2 GPU** (pagination, préchargement) | **fait** : noyau `attn_kv_*` (tuiles de 32 clés en mémoire partagée, une passe par (tête KV, tranche), recom`
- **T1** `REPRISE.md:151:| 7 | noyaux GPU | **fait, quatre formats** | warp par ligne : tête **Q8_0** (1,6 ms contre 7,3 CPU, écart 2e-7), **MXFP4** (0,1 ms, écart **0,00e0** — bit à bit), **Q4_K** (0,5 contre `
- **T1** `REPRISE.md:152:| 8 | suite du plan 1 M | **fait pour E4/E5** | **E4 KV déporté en VRAM** : noyaux `attn_kv_*` (tuiles de 32 clés, softmax en ligne, recombinaison + puits), miroir du cache **paginé** (`
- **T1** `REPRISE.md:171:| porte gpt-oss selon l'ouverture du pilote | sans `DRAVE_GPU` : **15,1757** · avec `DRAVE_GPU=1` : **15,1667** — l'écart vient du déport automatique des projections Q8_0 (> 8 Mo), pas `
- **T1** `REPRISE.md:174:| KV déporté dans le moteur (`DRAVE_GPU_KV=1`, ctx 4 096) | attention **22,16 → 3,29 ms/jeton** (÷6,7) · balayage 219,4 → **136,2 s** · perplexité 12,2177 → 12,2175 |`
- **T1** `README.md:377:| **push** (`--push`) | densité < 22 % — réseau creux, k-WTA, ReLU | 13,6 tok/s à 100 %, 20,6 à 5 % |`
- **T1** `README.md:378:| **4 bits** (`--q4`, `--q4-tout`) | modèle 4 bits existant (Q4_0) ou débit prioritaire | **41,6 – 44 tok/s** |`
- **T1** `0        2.0 Mo       13.9 Mo        0.0 Mo        0.02 Go  CPU`
- **T1** `1        2.0 Mo       13.9 Mo        0.0 Mo        0.03 Go  CPU`
- **T1** `2        2.0 Mo       13.9 Mo        0.0 Mo        0.05 Go  CPU`
- **T1** `3        2.0 Mo       13.9 Mo        0.0 Mo        0.06 Go  CPU`
- **T1** `4        2.0 Mo       13.9 Mo        0.0 Mo        0.08 Go  CPU`
- **T1** `5        2.0 Mo       13.9 Mo        0.0 Mo        0.10 Go  CPU`
- **T1** `6        2.0 Mo       13.9 Mo        0.0 Mo        0.11 Go  CPU`
- **T1** `7        2.0 Mo       13.9 Mo        0.0 Mo        0.13 Go  CPU`
- **T1** `KV par jeton et par couche : 2 têtes KV × 64 dim × 2 (K et V)`
- **T1** `=== perplexité 1929.3230 sur 3 tokens (0 événements, 0.3 s) ===`
- **T1** `=== perplexité 4949.4977 sur 3 tokens (0 événements, 0.3 s) ===`
- **T1** `// réécrire les boucles ne gagnait rien (mesuré : 12,4 → 12,5 ms).`
- **T1** `// de 23 à 159 ms. Le noyau lit une ligne par fil, donc des adresses`
- **T1** `// rentable : l'ancien lisait une ligne par fil (23 → 159 ms mesurés).`
- **T1** `// Mesuré sur gpt-oss à contexte 512 : YaRN ×32 coûte un facteur 9`
- **T1** `// rapide que le chemin scalaire Q6_K, qui coûtait 42 % du temps par`
- **T1** `GGUF ouvert en 222.300567ms — 290 tenseurs`
- **T1** `GGUF ouvert en 191.749149ms — 290 tenseurs`
- **T1** `// Mesuré sur le 30B-A3B : les tranches d'experts sont lues à 8 Go/s,`
- **T1** `// pas 20 — dix-huit mille tranches de 900 Ko dispersées sur 18 Go`

