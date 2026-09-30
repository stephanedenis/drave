# Session aa5f9fc5 — Tu es vérificateur de documentation

| | |
|---|---|
| Identifiant | `aa5f9fc5-9450-4118-b65f-e8b99a28519d` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-09-30 15:07 |
| Durée | 0.1 h |
| Tours | 1 |
| Messages | 32 |
| Appels d'outils | 46 |
| Fichiers touchés | 0 |
| Commandes | 27 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu es vérificateur de documentation dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave » : moteur d'inférence LLM en Rust, `std` seul, binaire `drave`). Tout est en FRANÇAIS : écris en français.  CONTEXTE : la journée a produit ~50 commits qui ont changé beaucoup de choses : protocole de flux passé en **version 4** (en-tête de **79 octets**, quatre modes : dense, listes, … [3099 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu es vérificateur de documentation dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave » : mo … [3379 caractères tronqués]

*46 appels d'outils.* Actions notables :

- bash — List repo, docs and reports directories
- bash — Check for running drave and list sources
- bash — Find Rust sources and recent git log
- bash — Read start of previous coherence report
- bash — Read rest of previous audit report
- bash — Check git status and Rust line counts
- todo_write
- bash — Grep protocol constants in main.rs
- read
- bash — List all DRAVE_ env vars in code
- bash — Show DRAVE_ env var usages with context
- bash — Grep CLI flags in main.rs
- bash — Grep R4 cap constant
- bash — Read receiving code around validation
- … et 15 autres

**Synthèse produite :**

⏵ Je vérifie le codec Python et les chiffres KV dans les autres documents.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** List repo, docs and reports directories
- **T1** Check for running drave and list sources
- **T1** Find Rust sources and recent git log
- **T1** Read start of previous coherence report
- **T1** Read rest of previous audit report
- **T1** Check git status and Rust line counts
- **T1** Grep protocol constants in main.rs
- **T1** List all DRAVE_ env vars in code
- **T1** Show DRAVE_ env var usages with context
- **T1** Grep CLI flags in main.rs
- **T1** Grep R4 cap constant
- **T1** Read receiving code around validation
- **T1** Read encodage mode blocs emitter
- **T1** Find pair codec functions
- **T1** Read trace writer and reader in model.rs
- **T1** Count lines of key documents
- **T1** Grep key facts across reference docs
- **T1** Diff DRAVE_ vars code vs docs
- **T1** Find doc DRAVE_ vars possibly nonexistent
- **T1** Diff env vars docs vs code excluding journal
- **T1** Check all markdown links for dead paths
- **T1** Count test functions in Rust code
- **T1** Read plan diagnostic section and its git history
- **T1** Read run_ppl_reparti lot sending logic
- **T1** Grep lot chunking in main.rs
- **T1** Read ppl_reparti lot loop
- **T1** Check codec versions and KV percentages

## 4. Mesures et résultats marquants

- **T1** `dc8a193 Feuille de route : les clés f16 mesurées (+0,018 % pour 39 % de la taille du f32)`
- **T1** `528639c Cache KV : les clés en f16 sont le meilleur réglage mesuré (+0,018 % pour 39 % de la taille)`
- **T1** `d89e340 Cache KV : int4/int4 mesuré (+364 %), la courbe a ses six premiers points`
- **T1** `da6415b Colab : le mode lot chiffré dans la recette (2,6 s contre 47,6 s à 20 ms par message)`
- **T1** `1bc0470 Règle R4 : plafond des allocations pilotées par le réseau (256 Mo)`
- **T1** `ae85043 DRVF v3 : −66 % de trace au total, pour +0,074 % de perplexité`
- **T1** `6b3b53f DRVF v2 sur le disque : −49,87 % de trace, rejeu identique`
- **T1** `af18f29 Transport en listes à 1 024 jetons : ÷2,3 pour 1,3 % d'écart`
- **T1** `| 22 | `docs/plan-prefill-reparti.md:66-68` (règle R4) | refus de `n == 0` et de `n × hidden × 4 > 256 Mo` **avant** l'allocation | `recevoir_flux` fait `vec![0u8; n * hidden * 4]` (main.rs:1584) **sa`
- **T1** `| 28 | `reports/rapport-phase3-reparti.md:61-62` | « **3 604 octets** (20 d'en-tête + 896 × 4) » | 20 octets était l'en-tête d'avant les réglages d'activation ; le même jour, `rapport-transport-liste.`
- **T1** `| 33 | `docs/colab-reparti.md:36` | « **1 989** en listes à échelle par bloc (68 % d'activité) » | 1 989 = ancien format (indices u16, 3 o/actif, en-tête 39). Format actuel (écarts u8, 2 o/actif, en-t`
- **T1** `| 35 | `reports/rapport-transport-liste.md:25` | listes seuil 0,00 : **3 622** pour 100,0 % (896 actifs) | 39 + 4 × 896 = **3 623** ; l'octet manquant n'est pas expliqué | PÉRIMÉ |`
- **T1** `| 36 | `docs/format-flux.md:94` | « 1 seul lot de **917 543 octets** » | 39 + 256 × 896 × 4 ; avec l'en-tête de 79 : **917 583** | PÉRIMÉ |`
- **T1** `| 37 | `docs/format-flux.md:142` | « 1 lot de 256 : 0,00e0 (**918 ko** sur le fil) » | 917 583 o ≈ 918 ko (arrondi décimal) | OK |`
- **T1** `| 38 | `docs/format-flux.md:45`, `reports/rapport-compacite-trace.md:5,92` | trace dense 512 j : 132 396 736 → **66 370 408** (−49,87 %) | `/tmp/flux_v2.bin` = exactement 66 370 408 octets, version 2 `
- **T1** `| 41 | `docs/roadmap.md:107` | trace 512 jetons = « **12 288 listes** · 132 Mo · 6 octets par neurone actif » | 24 576 listes pour 512 jetons × 24 couches × 2 points ; 12 288 = la valeur pour **256 je`
- **T1** `| 44 | `reports/rapport-compacite-trace.md:13-14` | « restent à faire : valeurs i8 (−60,9 %), échelles f16 (−63,5 %), zstd (−79 %) » | i8 + échelles f16 par bloc sont **faits et commités** (`ae85043` `
- **T1** `| 45 | `README.md:34` | « Croisement push/pull à **10 %** de densité ✅ mesuré » | `reports/rapport-croisement-push-pull.md:43` : « **~22 %** … pas à 10 » ; le README lui-même le dit ligne 389 | CONTRA`
- **T1** `| 46 | `docs/vision.md:46,133,198` et `docs/histoire.md:12` | croisement « mesuré » à **10 %** | 22 % (rapport de référence + REPRISE §5.1 + `docs/convertisseur.md:225`) | CONTRADICTOIRE |`
- **T1** `| 51 | `docs/contexte-long.md:103` | KV int4 « mesuré : **+384 %** — llama.cpp : +411 % » | +384 % est l'ancienne mesure à 512 jetons à échelle unique ; la mesure de référence à 8 192 est **+364 %** c`
- **T1** `| 54 | `README.md:397` | Q4_0 : +9,1 % contre Q8_0 | 21,0116 contre 19,2647 = +9,07 % (`rapport-mur-memoire-4bits.md:143-145`) | OK |`
- **T1** `| 61 | `docs/colab-reparti.md:103` | « `--flux-blocs --act-thresh 0.02` (÷2 sur le fil pour **0,2 %**) » | le rapport que ce document cite réfute explicitement cette formulation (`rapport-transport-li`
- **T1** `et supprimer « ÷2 pour 0,2 % » que le rapport cité réfute.`
- **T1** `« changera dans un commit dédié » (ligne 12), 10 % → ~22 % (ligne 34), pointer`
- **T1** `8. **Corriger `docs/vision.md` et `docs/histoire.md`** : 10 % → ~22 % (vision 46,`
- **T1** `19,4029, −65,9 %) viennent du commit `ae85043` et de `docs/format-flux.md`, pas`
- **T1** `seulement) ; `convertisseur.md:225` est du bon côté du croisement (22 %).`
- **T1** `| PÉRIMÉ | **38** | version du format de flux et du disque (7) · nombre de flux à 40 et 1 024 jetons (2) · en-têtes 26 et 39 octets (3) · octets par flux, par lot et par neurone actif (8) · 12 288 lis`
- **T1** `| CONTRADICTOIRE | **15** | code « Version 4 » contre `VERSION_FLUX = 3` (3) · échappement écrit sur 4 octets / lu sur 2 · règles R1/R4 du plan contre le code (2) · 3 604 contre 3 623 dans `roadmap.md`
- **T1** `| OK | **17** | formats des modes 2 et 3 · `flux_brut` · `hôte:port` · trace dense 66 370 408 o (fichier réellement relu) · 66 370 406 hors sentinelle · 24 576 listes / 22 008 776 actifs (source) · 91`
- **T1** `1391:/// payait 256 allers-retours. Le corps fait `n × hidden × 4` octets ; la`
- **T1** `1463:/// contrôle : jusqu'à ~15 To demandés au noyau. 256 Mo couvrent largement un lot`
- **T1** `1464:/// de 8 192 jetons × 8 192 canaux (268 Mo... soit un lot par fenêtre maximale).`
- **T1** `2971:    // Défauts du mode PERPLEXITÉ : 256 jetons, trois quarts des cœurs, 16 bits`
- **T1** `3145:    // 800 Mo sur gpt-oss, la garder en mémoire serait absurde).`
- **T1** `// relecture adversariale : VmSize 17 572 760 ko sur une seule trame).`
- **T1** `/// canaux, ~22 % plus petit, avec perte).`
- **T1** `// f16 par bloc de 32 canaux (l'étude de compacité annonce −22 % de plus,`
- **T1** `// début et personne ne s'en apercevait (2 octets sur 132 Mo).`
- **T1** `REPRISE.md:247:| `DRAVE_KV_K_F16=1` | clés en **f16** (2 octets/valeur, précision relative) | **le meilleur réglage mesuré** : à 8 192 jetons, clés f16 + valeurs int8 = **+0,018 %** pour **39 % de la `
- **T1** `REPRISE.md:248:| `DRAVE_TRACE_BLOCS=1` | trace DRVF **v3** : valeurs i8, échelle f16 par bloc de 32 | 45 079 930 o contre 66 370 408 en v2 (−32 %), rejeu 19,4029 contre 19,3885 (+0,074 %) |`
- **T1** `REPRISE.md:390:  l'en-tête refusent au-delà de 256 Mo — un pair pouvait demander ~15 To.`
- **T1** `docs/colab-reparti.md:38:  listes à échelle par bloc à 68 % d'activité. En **lots** (`--lot 64`), c'est`
- **T1** `docs/format-flux.md:117:f32 dense (3,5 ko par jeton) ; le lot en listes est le mode 4, pas encore écrit.`
- **T1** `docs/format-flux.md:140:Le mode dense coûte **3 663 octets par flux** (79 d'en-tête + 896 × 4) pour`
- **T1** `docs/plan-prefill-reparti.md:9:> disait, le code en écrivait quatre) ; et la règle R4 (plafond de 256 Mo) est`
- **T1** `docs/plan-prefill-reparti.md:30:| nouveau mode ou champ `t` ? | **mode 3** (`MODE_LOT`), pas de champ | le corps dense d'un lot est `t × hidden × 4` : `n` (offset 18) porte déjà le compte, l'en-tête r`
- **T1** `docs/plan-prefill-reparti.md:76:* **R4** — `n == 0` et `n × hidden × 4 > 256 Mo` sont refusés **avant**`
- **T1** `docs/plan-prefill-reparti.md:357:| 8 | `docs/colab-reparti.md` | répétition réelle (nœud moteur local, pilote Colab) | 200 jetons, `--lot 16`, écart **0,00e0** avec 60 ms d'aller-retour, et le tableau`
- **T1** `docs/roadmap.md:30:| 1.4 | **Écart int8 résiduel** (+3,0 % contre +0,8 % chez llama.cpp à 8 192) | ✅ | **attribué** : tout l'écart est dans les CLÉS (clés f32 + valeurs int8 = +0,023 % ; l'inverse = +`
- **T1** `docs/roadmap.md:56:| 3.2 | **Granularité** : par couche, par bloc de canaux, par expert | 🔬 | livrés et mesurés : listes i16, **échelles par bloc de 32 canaux (valeurs i8)** et **indices par écarts** `
- **T1** `docs/roadmap.md:58:| 3.4 | **Démonstration Colab** : préremplissage réparti (le décodage reste séquentiel — c'est écrit dans la vision) | 🔬 | **le préremplissage par lots sur le fil est FAIT et fidèle`
- **T1** `docs/roadmap.md:108:| 2026-09-30 | trace du flux, Qwen2.5-0.5B, 512 jetons, 24 couches, 2 points par couche | 24 576 listes · **132 Mo** en v1 · 6 octets par neurone actif · **+8 % de temps** (aujourd`
- **T1** `docs/roadmap.md:112:| 2026-09-30 | protocole de flux, deux processus, localhost | en-tête de **39 octets** à l'époque (79 aujourd'hui : les top-k voyagent) · dense f32 **3 623 octets/flux** · listes i`
- **T1** `/// n'est plus bornée par la RAM (20 Go/s) mais par la VRAM (≈ 450 Go/s).`
- **T1** `REPRISE.md:158:| 3 | KV int8 puis int4 | **fait, jusqu'à 8 192** | **échelles par bloc de 32** : int8 +**1,5 %** à 512 (était +7,1 %), **+3,0 % à 8 192** (llama.cpp +0,8 %) ; int4 **+364 % à 8 192** c`
- **T1** `REPRISE.md:180:| KV int4, échelles par bloc | +219 % (512) et +287 % (4 591) — était +384 % et +450 % |`
- **T1** `REPRISE.md:181:| KV à 8 192 jetons (longueur de la référence llama.cpp) | f32 **14,2339** · int8 **14,6667 (+3,0 %)** contre +0,8 % chez llama.cpp · int4 **66,0369 (+364 %)** contre +494 % chez llama.`
- **T1** `REPRISE.md:244:| `DRAVE_KV_BITS=8` ou `4` | quantifie le cache KV (défaut f32) | le 4 bits coûte +364 % de perplexité à 8 192 |`
- **T1** `REPRISE.md:245:| `DRAVE_KV_K_F32=1` | garde les CLÉS en f32 (valeurs quantifiées) | **le bon compromis mesuré** : à 8 192, 75 % de la taille f32 pour +0,02 % de perplexité, contre +3,0 % pour l'int8 c`
- **T1** `REPRISE.md:313:donne +0,023 %, clés int8 + valeurs f32 donne +3,01 %. Réglage utilisable tout de`
- **T1** `REPRISE.md:314:suite : `DRAVE_KV_BITS=8 DRAVE_KV_K_F32=1` (75 % de la taille f32 pour +0,02 %).`
- **T1** `REPRISE.md:364:| clés f16 · valeurs int8 | 3,125 | **39 %** | **+0,018 %** ← le meilleur point |`
- **T1** `REPRISE.md:365:| clés f32 · valeurs int8 | 5,125 | 64 % | +0,023 % |`
- **T1** `REPRISE.md:368:| int8 · int8 | 2,25 | 28 % | +3,04 % |`
- **T1** `REPRISE.md:369:| int4 · int4 | 1,25 | 16 % | +364 % |`
- **T1** `REPRISE.md:424:   élément contre 2,25 en int8/int8 et 8 en f32) donne **+0,057 %** à contexte 256`
- **T1** `docs/contexte-long.md:103:| E3 | **KV int4** | **fait** (nibbles empaquetés) | 1 M tient en RAM (9,7 Go) et en VRAM | mesuré : **+384 %** à 512 jetons, **+364 % à 8 192** — llama.cpp q4_0 : +411 % pui`
- **T1** `docs/contexte-long.md:125:| **int4** | **63,61** (+384 %) | 72,80 (+411 %) | **71,05** (+450 %) | 98,53 (+494 %) |`
- **T1** `docs/contexte-long.md:144:| int4 | 63,6107 (+384 %) | **41,9442 (+219 %)** | **49,9438 (+287 %)** |`
- **T1** `docs/contexte-long.md:160:| **int4** | **66,0369** | **+364 %** | 98,53 | +494 % | 1 461 s |`
- **T1** `docs/contexte-long.md:169:2. **Le 4 bits est ici MEILLEUR que llama.cpp** (+364 % contre +494 %) tout en`
- **T1** `docs/roadmap.md:111:| 2026-09-30 | attribution du cache KV int8, 8 191 jetons, ctx 8 192 | f32 **14,2339** · int8 **14,6667** (+3,0 %) · **clés f32** + valeurs int8 **14,2372** (+0,023 %) · clés int8 `
- **T1** `docs/roadmap.md:116:| 2026-09-30 | où mettre les bits du cache KV, 8 191 jetons, ctx 8 192 | à taille ÉGALE : clés f32 + valeurs int8 **+0,023 %** contre clés int8 + valeurs f32 **+3,01 %** (facteur 1`
- **T1** `docs/roadmap.md:164:| **clés f32** · valeurs int8 | **14,2372** | **+0,023 %** | **99,2 % expliqué** |`
- **T1** `docs/roadmap.md:173:cache à **75 % de la taille f32** pour +0,02 % de perplexité, là où l'int8 complet`
- **T1** `docs/roadmap.md:179:coûte +0,023 % là où clés int8 + valeurs f32 coûte +3,01 % (facteur 130), et le`
- **T1** `docs/roadmap.md:180:4 bits des clés coûte +385 % contre +0,46 % pour celui des valeurs (facteur 840).`
- **T1** `docs/roadmap.md:181:Les **clés en f16** sont mesurées : clés f16 + valeurs int8 = **+0,018 %** à`
- **T1** `docs/roadmap.md:182:8 192 jetons pour **39 % de la taille f32** — le meilleur réglage de la courbe`
- **T1** `docs/roadmap.md:183:(les clés f32, à 64 % de la taille, font +0,023 % ; l'int8 complet, à 28 %, +3,04 %).`
- **T1** `docs/vision.md:189:  **+3,0 %** à 8 192, là où l'int4 coûte +364 % — le débat n'est pas « combien de`
- **T1** `reports/rapport-analyse-flux.md:46:**28 % à 86 %**. Les couches 5 à 8 se partagent 84-86 % de leurs neurones`
- **T1** `reports/rapport-analyse-flux.md:48:partage que 28 %.`
- **T1** `reports/rapport-attention-creuse.md:26:| 64 | 23,4621 (−0,64 %) | 26,1959 (−0,23 %) | 24,6867 | **19,3700 (−0,78 %)** |`
- **T1** `reports/rapport-attribution-kv.md:15:| **clés f32** · valeurs int8 | **14,2372** | **+0,023 %** | **99,2 % expliqué** |`
- **T1** `reports/rapport-attribution-kv.md:33:DRAVE_KV_K_F32=1` donne un cache à **75 % de la taille f32** pour +0,02 % de`
- **T1** `reports/rapport-campagne-parcimonie.md:19:| activations du FFN (k-WTA 90 %) | +0,15 à +0,28 % | ✅ acceptable |`
- **T1** `reports/rapport-campagne-parcimonie.md:21:| entrée des projections d'attention (90 %) | +0,06 % | ✅ quasi gratuit |`
- **T1** `reports/rapport-parcimonie-imposee.md:50:| 90 % | 319,1 M (−9,9 %) | 23,6790 (+0,28 %) | 26,2950 (+0,15 %) |`
- **T1** `reports/rapport-parcimonie-imposee.md:68:| attention seule à 90 % | 350,0 M (−1,2 %) | +0,06 % | — |`
- **T1** `reports/rapport-placement-bits-kv.md:5:donnent 39 % de la taille f32 pour +0,06 %.`
- **T1** `reports/rapport-placement-bits-kv.md:16:| **f32** | **int8** | 5,125 | 64 % | **14,2372** | **+0,023 %** |`
- **T1** `reports/rapport-placement-bits-kv.md:17:| **int8** | **f32** | 5,125 | 64 % | 14,6622 | **+3,01 %** |`
- **T1** `reports/rapport-placement-bits-kv.md:19:| int4 | f32 | 4,625 | 58 % | 69,0464 | **+385 %** |`
- **T1** `reports/rapport-placement-bits-kv.md:20:| int8 | int8 | 2,25 | 28 % | 14,6667 | +3,04 % |`
- **T1** `reports/rapport-placement-bits-kv.md:21:| **f16** | **int8** | **3,125** | **39 %** | **14,2365** | **+0,018 %** |`
- **T1** `reports/rapport-placement-bits-kv.md:22:| int4 | int4 | 1,25 | 16 % | 66,0369 | **+364 %** |`
- **T1** `reports/rapport-placement-bits-kv.md:30:16 %  int4/int4 ................ +364 %`
- **T1** `reports/rapport-placement-bits-kv.md:31:28 %  int8/int8 ................ +3,04 %`
- **T1** `reports/rapport-placement-bits-kv.md:33:39 %  clés f16 · valeurs int8 .. +0,018 %   ← le meilleur point`
- **T1** `reports/rapport-placement-bits-kv.md:35:64 %  clés f32 · valeurs int8 .. +0,023 %`

