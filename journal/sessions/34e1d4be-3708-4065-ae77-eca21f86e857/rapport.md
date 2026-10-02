# Session 34e1d4be — Tu es relecteur ADVERSE. Tu

| | |
|---|---|
| Identifiant | `34e1d4be-3708-4065-ae77-eca21f86e857` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-02 09:52 |
| Durée | 0.1 h |
| Tours | 1 |
| Messages | 38 |
| Appels d'outils | 53 |
| Fichiers touchés | 0 |
| Commandes | 37 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu es relecteur ADVERSE. Tu ne modifies AUCUN fichier : tu produis un rapport de constats, avec citations exactes et numéros de ligne.  Contexte : le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet contient un moteur d'inférence nommé **Drave**. Sa vision est définie dans `docs/vision.md` et `docs/programme-recherche.md` — lis-les ENTIER d'abord (ce sont les textes de référence), puis audite … [4125 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu es relecteur ADVERSE. Tu ne modifies AUCUN fichier : tu produis un rapport de constats, avec citations exactes et num … [4405 caractères tronqués]

*53 appels d'outils.* Actions notables :

- bash — List docs and count lines
- read
- bash — List tools and reports
- bash — Grep key figures across repo
- bash — Grep format table and verification tools
- bash — Grep protocol, gate figures, llama.cpp mentions
- bash — Check vision patch claims
- bash — Read prior coherence report
- bash — Check protocol version constants in code
- bash — Grep dense and optimization framing
- bash — Verify format-clusters measurements
- bash — Check type table count and QTNT naming
- bash — Check YaRN threshold and CLI flags
- bash — Check README/REPRISE vision status
- … et 25 autres

**Synthèse produite :**

| fichier:ligne | citation exacte (≤ 25 mots) | problème | correction minimale proposée (texte de remplacement exact) | gravité |
|---|---|---|---|---|
| docs/format-flux.md:3 | « Ce format sert **trois choses à la fois**, et c'est délibéré : » | Le format/transport ne nomme jamais la finalité d'analyse de la vision (« comprendre le modèle et adapter l'architecture à la tâche », vision.md:94-99), alors que les outils existent (`tools/analyse_flux.py`, `profil_flux.py`, `diff_flux.py`) et que la vision fait du journal « l'instrument de réglage ». | Remplacer par « Ce format sert **quatre choses à la fois**, et c'est délibéré : » puis ajouter après l'item 3 (ligne 10) : « 4. l'**analyse** : les mêmes octets, relus par `tools/profil_flux.py`, `tools/analyse_flux.py` et `tools/diff_flux.py`, disent quels neurones travaillent — la donnée qui adapte l'architecture à la tâche. » | moyenne |
| docs/format-flux.md:119 | « est qu'il ne coûte pas plus de 1,5 fois celui-ci. » | Le critère des 1,5× n'est vérifié qu'à 256 jetons ; `reports/rapport-mode4-lot-listes.md` (tableau « selon la longueur ») mesure **5,6× à 20 jetons** et 0,50× à 64 : la réserve n'est pas portée. | « est qu'il ne coûte pas plus de 1,5 fois celui-ci **à 256 jetons** (5,6× à 20 jetons — `reports/rapport-mode4-lot-listes.md`). » | basse |
| docs/format-clusters.md:5-6 | « un nœud n'ouvre que ce qu'il sert — mesuré **3,20 Go au lieu de 18,56** et **625 ms au lieu de 3,9 s** » | Les grappes sont cadrées comme un rangement de fichiers et un gain de chargement, alors que la vision en fait l'unité de **placement** des neurones entre machines (axe 3, vision.md:131-143) — le document ne dit jamais que les flux se routent entre grappes. | Ajouter après la ligne 6 : « **Et c'est le mécanisme de placement** : ces grappes sont les neurones qu'on répartit entre nœuds, et le flux d'activation se route de l'une à l'autre (vision, axe 3). » | moyenne |
| docs/convertisseur.md:111 | « ## 5. Format proposé : `QTNT` » | `QTNT` porte l'ancien nom du projet (Qtrinet) alors que le renommage du 30/09 est « fait partout » (`docs/histoire.md:28-36`, vision.md:264-266) ; aucun autre fichier du dépôt ne l'emploie, et le conteneur n'est jamais relié au format de flux réellement implémenté (`DRVF`). | « ## 5. Format proposé : conteneur **Drave** (ex-`QTNT`), adossé au format de flux `DRVF` » — même remplacement du jeton à la ligne 166 (« conteneur **Drave** (ex-`QTNT`) + index de placement »). | basse |
| docs/convertisseur.m
… [10592 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** List docs and count lines
- **T1** List tools and reports
- **T1** Grep key figures across repo
- **T1** Grep format table and verification tools
- **T1** Grep protocol, gate figures, llama.cpp mentions
- **T1** Check vision patch claims
- **T1** Read prior coherence report
- **T1** Check protocol version constants in code
- **T1** Grep dense and optimization framing
- **T1** Verify format-clusters measurements
- **T1** Check type table count and QTNT naming
- **T1** Check YaRN threshold and CLI flags
- **T1** Check README/REPRISE vision status
- **T1** Find YaRN threshold in code
- **T1** Check density crossing figures in docs
- **T1** Read push/pull crossing report header
- **T1** Read needle test reports
- **T1** Confirm 12/12 needle result
- **T1** Grep analysis-purpose wording
- **T1** Check cluster placement framing and converter/flux link
- **T1** Check last commit dates of audited docs
- **T1** Verify remaining cluster figures
- **T1** Read mode 4 report
- **T1** Check borrowed formats in code
- **T1** Check colab artifacts and repo size
- **T1** Estimate git packed size
- **T1** Inspect flux analysis tools
- **T1** Verify remaining figures and vocabulary
- **T1** Find sources for converter loading figures
- **T1** Check gpt-oss report and latency sources
- **T1** Read gpt-oss perplexity report summary
- **T1** Verify prefill-by-lots figures
- **T1** Print exact lines for citation
- **T1** Print converter lines for citation
- **T1** Final check on calque and vision lines
- **T1** Check if docs changed during audit
- **T1** Check plan-gpu-topk on A/B figures

## 4. Mesures et résultats marquants

- **T1** `./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:3663:=== perplexité 15.1757 sur 510 tokens (0 événements, 98.0 s) ===`
- **T1** `./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:5619:=== perplexité 15.1757 sur 510 tokens (0 événements, 97.3 s) ===`
- **T1** `./reports/rapport-routage-experts.md:75:déplacé la porte Qwen3-30B de 799,8557 à 799,8152 (−0,005 %). Cause : la`
- **T1** `./REPRISE.md:1002:| `tools/portes_formats.sh` | **17 formats × 2 blocs** | tous exacts contre libggml |`
- **T1** `./REPRISE.md:1089:tools/portes_formats.sh          # 17 formats × 2 blocs, contre libggml`
- **T1** `./README.md:364:tools/portes_formats.sh                   # 17 formats × 2 blocs, contre libggml`
- **T1** `59:| rejeu `--flux-forcer` | 19,3885 | **19,4029 (+0,074 %)** |`
- **T1** `102:| E2 | **KV int8** | **fait** (échelle par vecteur, dequantification à la lecture) | ÷4 sur le KV ; 128 k confortable | mesuré : +7,1 % de perplexité (llama.cpp q8_0 : +3,1 %) |`
- **T1** `103:| E3 | **KV int4** | **fait** (nibbles empaquetés) | 1 M tient en RAM (9,7 Go) et en VRAM | mesuré : **+384 %** à 512 jetons, **+364 % à 8 192** — llama.cpp q4_0 : +411 % puis +494 % ; à réserver `
- **T1** `135:3. **Notre int8 était plus cher que celui de llama.cpp** (+5,2 % contre +0,8 %)`
- **T1** `146:L'écart avec llama.cpp (+0,8 %) est donc comblé à contexte court, et le 4 bits`
- **T1** `166:   llama.cpp reste meilleur (+0,8 %) — son cache q8_0 garde une échelle par bloc`
- **T1** `169:2. **Le 4 bits est ici MEILLEUR que llama.cpp** (+364 % contre +494 %) tout en`
- **T1** `./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:19517:| projecteur (fusion 2 × 2 → `mm.0` → GELU → `mm.2`) | ✅ validé (1,7e-6) |`
- **T1** `./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:20841:patchs : le banc est sur une image de 16 × 16 patchs et la référence suppose 28 × 28 — comparaison sautée (elle a été validée à `
- **T1** `./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:20865:La référence numpy, elle, annonce proprement qu'elle ne peut plus comparer à cette taille et rappelle les valeurs validées (5,4e`
- **T1** `./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:21117:| 5 | **MLA et vision** | **MLA** : modèle synthétique + référence numpy, écart **5,2e-7** · **Vision** : chaîne complète démont`
- **T1** `cache KV** (« 75 % / 50 % » contre « 64 % / 28 % » dans le rapport qui l'a mesuré) et`
- **T1** `| 10 | `model.rs:527,547` (commentaire) | la v3 est « ~22 % plus petit » | mesuré : **−32,1 %** contre la v2 (66 370 408 → 45 079 930 o, `docs/format-flux.md:58`) et −65,9 % contre la v1 | CONTRADICTO`
- **T1** `59:| 10 | `model.rs:527,547` (commentaire) | la v3 est « ~22 % plus petit » | mesuré : **−32,1 %** contre la v2 (66 370 408 → 45 079 930 o, `docs/format-flux.md:58`) et −65,9 % contre la v1 | CONTRADI`
- **T1** `71:| 17 | `docs/format-flux.md:140`, `docs/colab-reparti.md:37`, `reports/rapport-session-2026-09-30.md:13`, `reports/rapport-prefill-reparti.md:85` | flux dense = **3 663 octets** (79 + 896 × 4) | co`
- **T1** `75:| 21 | `REPRISE.md:324` | « en UN lot de **917 543** octets » | 79 + 256 × 896 × 4 = **917 583** (`docs/format-flux.md:115`, `reports/rapport-prefill-reparti.md:42`) | PÉRIMÉ |`
- **T1** `79:| 25 | `reports/rapport-transport-liste.md:100` et `:230-231` | « trois octets par neurone actif (indice u16, valeur i8) » ; « 1 989 (blocs à 68 % d'activité) » | son propre « Ajout — les indices p`
- **T1** `81:| 27 | `docs/format-flux.md:47`, `reports/rapport-compacite-trace.md:4-5`, `docs/roadmap.md:108` | trace dense 512 jetons : 132 396 736 → **66 370 408** (−49,87 %) | cohérent partout (le rapport ex`
- **T1** `82:| 28 | `docs/format-flux.md:58-61`, `REPRISE.md:248,340-341`, `docs/roadmap.md:94` | v3 : **45 079 930 o** (−32,1 % vs v2), rejeu 19,4029 (+0,074 %), 21 630 645 actifs | valeurs cohérentes entre do`
- **T1** `86:| 32 | `docs/format-flux.md:169` | lot : 4×64 → 18,0851 ; 1 lot de 256 → 918 ko, 0,00e0 | conforme à `reports/rapport-prefill-reparti.md:41-42` (917 583 o ≈ 918 ko) | OK |`
- **T1** `100:| 41 | `docs/contexte-long.md:101-102` (E2) | KV int8 « **fait** (échelle par vecteur) », « mesuré : **+7,1 %** (llama.cpp : +3,1 %) » | le même document §4.bis (`:143-145`) dit « corrigé, échelle`
- **T1** `format-flux.md:47:| trace dense, 512 jetons | 132 396 736 o | **66 370 408 o (−49,87 %)** |`
- **T1** `format-flux.md:58:| trace dense, 512 jetons | 66 370 408 o | **45 079 930 o (−32,1 %)** |`
- **T1** `format-flux.md:128:f32 dense (3,5 ko par jeton) ; le lot en LISTES est le mode 4 (1,5 ko par jeton,`
- **T1** `format-flux.md:152:Le mode dense coûte **3 663 octets par flux** (79 d'en-tête + 896 × 4) pour`
- **T1** `convertisseur.md:59:➡️ **Le seuil est à 25 %, et MXFP4 est à 12–18 % : en dense, abolir les zéros`
- **T1** `convertisseur.md:96:| GPU, lecture | 380 Go/s | poids denses |`
- **T1** `=== 3,20 / 625 ms ===`
- **T1** `reports/rapport-decoupage-moe.md:106:cluster, 625 ms au lieu de 3,9 s, 1 587 tenseurs vérifiés — le format est décrit`
- **T1** `reports/rapport-decoupage-moe.md:42:| 8 | **0,607** | **3,08** | 0,319 | 5,32 | ×1,9 |`
- **T1** `reports/bilan-multi-materiel.md:95:| « 27 PE suffisent, 3 % de la logique » | **Corrigée** — en comptant le lecteur : 51 voies, 41 % de la logique et 41 % de la M20K |`
- **T1** `reports/bilan-multi-materiel.md:109:Une carte = 4,83 G évts/s = **un CPU 20 cœurs**, pour 41 % de la logique et 41 %`
- **T1** `reports/rapport-architecture-memoire.md:240:| **lecture NVMe** (8 lecteurs) | 22,41 | 21,45 | 22,57 Go/s |`
- **T1** `reports/rapport-coherence-docs-2.md:100:| 41 | `docs/contexte-long.md:101-102` (E2) | KV int8 « **fait** (échelle par vecteur) », « mesuré : **+7,1 %** (llama.cpp : +3,1 %) » | le même document §4.bis`
- **T1** `reports/rapport-coherence-docs.md:97:| 41 | `docs/roadmap.md:107` | trace 512 jetons = « **12 288 listes** · 132 Mo · 6 octets par neurone actif » | 24 576 listes pour 512 jetons × 24 couches × 2 poin`
- **T1** `reports/rapport-cpu-aer.md:18:- dispersion (`np.add.at`) : 364797216.41 G événements/s`
- **T1** `reports/rapport-encodage.md:26:| groupé (blocs de 8) | 1 | 6.9 % | 53.42 % | 1.07 | **2.60** | 3.41 | 2.00 | 0.36 | 12.2 |`
- **T1** `reports/rapport-eparsite.md:30:| 75.0 % | 19.8 % | 49.41 % | 2.00 | 1.20 | 3.36 | 6.52 | ×1.67 |`
- **T1** `reports/rapport-passage-a-l-echelle.md:47:par jeton ÷ 20 Go/s = **13 ms/jeton = 41 tok/s**, contre **41,6 tok/s mesurés**.`
- **T1** `reports/rapport-precision.md:27:| creux 2 bits d=0.250 | 2 | 24.0 % | 1.48 | 70.41 % | 7.5 **◀** |`
- **T1** `reports/rapport-precision.md:51:| 1.48 | creux 2 bits d=0.250 | 70.41 % | 7.5 |`
- **T1** `drave-core/src/model.rs:1519:    /// deux architectures se croisent à 10 % de densité ; on bascule un peu`
- **T1** `163:| 8 | suite du plan 1 M | **fait pour E4/E5** | **E4 KV déporté en VRAM** : noyaux `attn_kv_*` (tuiles de 32 clés, softmax en ligne, recombinaison + puits), miroir du cache **paginé** (capacité do`
- **T1** `1519:    /// deux architectures se croisent à 10 % de densité ; on bascule un peu`
- **T1** `=== croisement 22/10 % ===`
- **T1** `convertisseur.md:225:dessous du croisement mesuré à 22 % de densité : le régime où l'architecture`
- **T1** `Elles donnent **exactement le même résultat** — vérifié : perplexité 19,2647 au`
- **T1** `Mesure refaite sur `blk.0.ffn_gate.weight` (4 864 × 896, 4,36 M poids), 16 threads,`
- **T1** `| 0 % | 0,004 | 0,167 | 0,03 |`
- **T1** `| 1 % | 0,019 | 0,162 | 0,12 |`
- **T1** `| 5 % | 0,047 | 0,168 | 0,28 |`
- **T1** `| **10 %** | 0,078 | 0,163 | **0,48** |`
- **T1** `| **25 %** | 0,180 | 0,163 | **1,11** |`
- **T1** `| 50 % | 0,355 | 0,165 | 2,15 |`
- **T1** `**En une ligne** : à 4 096 clés, l'attention à **256 clés (6,25 %)** des 24 jetons`
- **T1** `générés (0,58 % des passes), ce qui est bien le moment où le modèle doit regarder`
- **T1** `reports/rapport-aiguille.md:74:**12 sondes sur 12** trouvées, à toutes les profondeurs — y compris à 90 % de la`
- **T1** `82:**625 ms au lieu de 3,9 s (6,2× plus vite)**. Avec huit nœuds, chacun ne lit que`
- **T1** `63:  produit aucun événement. 15 % de zéros MXFP4 = 0,30 octet/poids économisé,`
- **T1** `64:  soit 15 % du flux d'événements ;`
- **T1** `97:| GPU, dispersion d'événements | 18,1 G év/s | mode push |`
- **T1** `106:  le CPU tient 5,3 G év/s (≈ 10,6 Go/s d'événements). **Le seuil d'intérêt du`
- **T1** `134:2. **Les listes d'événements ne sont pas matérialisées** : 1,98 o/poids × 120 G`
- **T1** `reports/rapport-lecteur-multifichiers.md:239:| conversion | 435 + 8 × 144 = **1 587 tenseurs**, 18,60 Go, 351,7 s |`
- **T1** `au lieu de f32 dense — 1,5 ko par jeton contre 3,5 — au prix d'une quantification`
- **T1** `| **mode 4, lots de 16** | **1,5 ko** (contre 3,5 en lot dense) | **3,03e-2** |`
- **T1** `croisement mesuré est à ~10 % de densité) — mais elle se prend PAR COUCHE, pas`
- **T1** `reports/rapport-coherence-docs.md:226:| OK | **17** | formats des modes 2 et 3 · `flux_brut` · `hôte:port` · trace dense 66 370 408 o (fichier réellement relu) · 66 370 406 hors sentinelle · 24 576 li`
- **T1** `=== 1,3 % transport ===`
- **T1** `reports/rapport-transport-liste.md:161:ci-dessous — **÷2,3 sur le fil pour 1,3 % d'écart à 1 024 jetons** (2,7 % à 256,`
- **T1** `reports/rapport-capteur-hebbien.md:44:| Énergie expliquée par `W · C` (prédiction linéaire) | **R² = 0,845** |`
- **T1** `=== 413 Mo / 21,0110 / 353 Mo ===`
- **T1** `reports/rapport-coherence-docs.md:115:| 54 | `README.md:397` | Q4_0 : +9,1 % contre Q8_0 | 21,0116 contre 19,2647 = +9,07 % (`rapport-mur-memoire-4bits.md:143-145`) | OK |`
- **T1** `reports/rapport-mur-memoire-4bits.md:145:| Qwen2.5-0.5B **Q4_0** | **4 bits verbatim** | **21,0116** | **+9,1 %** | **13,1** | **38,9** |`
- **T1** `reports/rapport-gpu-topk-selection.md:145:| 262 144 | 256 | 0,07 ms | 0,98 ms | **2,70e-7** |`
- **T1** `| Tenseur (couche 0) | \|w\|<5 % max | <10 % | <20 % |`
- **T1** `| blk.0.attn_norm.weight | 19.0 % | 77.9 % | 92.2 % |`
- **T1** `| blk.0.ffn_down.weight | 62.5 % | 91.1 % | 99.7 % |`
- **T1** `| blk.0.ffn_gate.weight | 73.8 % | 96.3 % | 99.9 % |`
- **T1** `| blk.0.ffn_up.weight | 56.5 % | 87.5 % | 99.7 % |`
- **T1** `| blk.0.ffn_norm.weight | 0.0 % | 0.0 % | 0.0 % |`
- **T1** `| blk.0.attn_k.weight | 68.5 % | 87.7 % | 96.8 % |`
- **T1** `| blk.0.attn_output.weight | 95.9 % | 99.7 % | 100.0 % |`
- **T1** `| blk.0.attn_q.weight | 79.3 % | 94.3 % | 99.1 % |`
- **T1** `| blk.0.attn_v.weight | 45.2 % | 74.6 % | 95.7 % |`
- **T1** `=== 195 ms / 62,2 ===`
- **T1** `reports/rapport-transport-liste.md:192:| attente du pair | **97,6 ms/jeton** | **16,1 ms/jeton** |`
- **T1** `reports/rapport-transport-liste.md:196:L'attente de 97,6 ms n'était ni le calcul distant ni le débit : c'était **Nagle`
- **T1** `127:**33,7 / 33,9 / 34,4 s**, perplexité 13,7205 dans tous les cas.`
- **T1** `193:| Qwen2.5-0.5B Q8_0, `--dense`, 16 fils | 512 | 17,1 s | **13,6 s** | **−20 %** |`
- **T1** `194:| gpt-oss-120b MXFP4, MoE groupé, 16 fils | 256 | ≈ 50 s | 34,4 s (lot 256) | **−31 %** |`
- **T1** `2	| E2 | **KV int8** | **fait** (échelle par vecteur, dequantification à la lecture) | ÷4 sur le KV ; 128 k confortable | mesuré : +7,1 % de perplexité (llama.cpp q8_0 : +3,1 %) |`
- **T1** `3	| E3 | **KV int4** | **fait** (nibbles empaquetés) | 1 M tient en RAM (9,7 Go) et en VRAM | mesuré : **+384 %** à 512 jetons, **+364 % à 8 192** — llama.cpp q4_0 : +411 % puis +494 % ; à réserver au`
- **T1** `jetons, 16 par lot, seuil 0,01 : **1,5 ko par jeton au lieu de 3,5** (÷2,3) pour`
- **T1** `18,56** et **625 ms au lieu de 3,9 s** sur Qwen3-30B-A3B.`
- **T1** `en-tête      magie, version, nb_calques, nb_tenseurs, alignement (2 Mo), graine`
- **T1** `| 5 | placement : épinglage NUMA, threads par calque | à faire | 20,7 → 24,7 Go/s mesuré au banc |`
- **T1** `2. **Épinglage NUMA** : 20 % mesurés, mais `sched_setaffinity` n'est pas dans`
- **T1** `./docs/convertisseur.md:116:en-tête      magie, version, nb_calques, nb_tenseurs, alignement (2 Mo), graine`
- **T1** `./docs/convertisseur.md:167:| 5 | placement : épinglage NUMA, threads par calque | à faire | 20,7 → 24,7 Go/s mesuré au banc |`

## 5. Erreurs rencontrées

1 sorties en erreur ou divergentes. Les premières :

- **T1** : === format-flux.md === === format-clusters.md === === convertisseur.md === 316:configuration dit ce qui est actif — c'est ce qui manquait pour déboguer un === colab-reparti.md === === contexte-long.md

