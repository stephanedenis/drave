# Session 8b315bb2 — Tu es relecteur ADVERSE. Tu

| | |
|---|---|
| Identifiant | `8b315bb2-abba-4033-b3d4-177d04b4f194` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-02 09:51 |
| Durée | 0.1 h |
| Tours | 1 |
| Messages | 23 |
| Appels d'outils | 30 |
| Fichiers touchés | 0 |
| Commandes | 23 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu es relecteur ADVERSE. Tu ne modifies AUCUN fichier : tu produis un rapport de constats, avec citations exactes et numéros de ligne.  Contexte : le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet contient un moteur d'inférence nommé **Drave**. Sa vision est définie dans `docs/vision.md` et `docs/programme-recherche.md` — lis-les ENTIER d'abord, ce sont les textes de référence.  Résumé de l … [4333 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu es relecteur ADVERSE. Tu ne modifies AUCUN fichier : tu produis un rapport de constats, avec citations exactes et num … [4613 caractères tronqués]

*30 appels d'outils.* Actions notables :

- bash — Count lines of documents to audit
- read
- bash — List docs and reports
- grep
- bash — Check sourced figures in reports
- bash — Check density, trace size and test figures
- bash — Grep version, clusters, encoding and analysis wording
- bash — Read gates script and locate 15,6017 source
- bash — Read density figures in analyse-flux report
- bash — Locate sources for vision section 3 and 6 figures
- bash — Verify crossing and attention transfer figures
- bash — Check prior audit and programme-recherche sources
- bash — Grep each unsourced vision figure repo-wide
- bash — Verify FPGA link and remaining figures
- … et 12 autres

**Synthèse produite :**

⏵ Rapport terminé : 24 constats, envoyés au parent.

Relecture adverse des cinq documents. Aucun fichier modifié. Tous les numéros de ligne ont été revérifiés par `grep` sur l'état courant du dépôt (attention : certaines références de l'audit précédent, `reports/rapport-coherence-docs-2.md`, pointent des lignes qui ont bougé — elles ont été recalculées ici).

| fichier:ligne | citation exacte (≤ 25 mots) | problème | correction minimale proposée (texte de remplacement exact) | gravité |
|---|---|---|---|---|
| docs/vision.md:222 | `\| **3. Répartir sur machines** \| **rien** — hypothèse écrite \|` | Contredit vision.md:120 (« Le transport existe, et c'est l'axe où le projet a le plus avancé depuis ») et roadmap.md:55-59 (3.1 ✅ transport TCP fidèle 0,00e0, 3.2 ✅ mode 4, 3.5 ✅). | `\| **3. Répartir sur machines** \| **transport en place et fidèle** (0,00e0) ; restent l'ordonnanceur et Colab \|` | ÉLEVÉE |
| docs/vision.md:151 | « Cette section est une **hypothèse de travail**, pas un résultat. » | Le §4 juste au-dessus donne des acquis mesurés ; la même formule revient en §7 (vision.md:209-210). | « Cette section mêle un **acquis** (le transport, fidèle à 0,00e0) et une **hypothèse de travail** (placement, granularité). » | MOYENNE |
| docs/vision.md:147 | « 5. **les mesures à faire** : débit d'un flux sérialisé, latence aller-retour, » | Déjà mesurées : roadmap.md:57 (latence jusqu'à 20 ms, 0,25 Mbit/s) et :112 (1 608 octets/flux). | « 5. **les mesures faites** : 1 608 octets par flux à 256 jetons, 0,25 Mbit/s, attente ≈ calcul distant + 3,2 × latence (`docs/roadmap.md`) ; » | MOYENNE |
| docs/vision.md:209-210 | « l'axe 3 est une hypothèse, avec ses mesures à faire » | Même dérive : les mesures existent (roadmap.md:57, :112, :119). | « l'axe 3 est **engagé** (transport fidèle), avec ses mesures faites (latence, débit, taille des tranches) » | MOYENNE |
| docs/vision.md:121 | « Deux processus se passent des flux (protocole v4 : version, modes dense / listes / » | Protocole en **v5** à cinq modes (roadmap.md:96-97) ; la liste en omet un. | « (protocole v5 : version, modes dense / listes / blocs / **lot dense** / **lot en listes**, contrat d'activation complet) » | MOYENNE |
| docs/vision.md:79 | « `--attn-topk 256` **améliore** la perplexité (234,88 contre 298,56 à contexte » | Chiffre sans source, déclaré non reproductible par docs/plan-gpu-topk.md:94 (« 234,88 ne correspond à aucun réglage reproductible »). | « `--attn-topk 256` **améliore** la perplexité 
… [8317 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** Count lines of documents to audit
- **T1** List docs and reports
- **T1** Check sourced figures in reports
- **T1** Check density, trace size and test figures
- **T1** Grep version, clusters, encoding and analysis wording
- **T1** Read gates script and locate 15,6017 source
- **T1** Read density figures in analyse-flux report
- **T1** Locate sources for vision section 3 and 6 figures
- **T1** Verify crossing and attention transfer figures
- **T1** Check prior audit and programme-recherche sources
- **T1** Grep each unsourced vision figure repo-wide
- **T1** Verify FPGA link and remaining figures
- **T1** Read rest of gates script
- **T1** Read top-k plan and search analysis purpose
- **T1** Check GPU model, format claims and margin figures
- **T1** Read V4.1 plan intro and gate list
- **T1** Check referenced paths and count formats
- **T1** Read formats gate script header
- **T1** Verify f16/int4 measured values
- **T1** Print exact lines to be quoted
- **T1** Verify all citation line numbers by grep
- **T1** Confirm mode 4 implementation and roadmap lines
- **T1** Find vision module validation sources

## 4. Mesures et résultats marquants

- **T1** `reports/rapport-localite-activation.md:43:| densité d'activation (seuil 5 % du max) | **17,9 %** des neurones par jeton (82 % ne font rien) |`
- **T1** `reports/rapport-analyse-flux.md:32:et c'est cohérent avec la mesure d'activation du projet (0,08 % « chauds » plus`
- **T1** `reports/rapport-architecture-memoire.md:374:| **DeepSeek-V4.1-Flash** | **365,70 Go** | **0,08 s** | **47 Mo** |`
- **T1** `reports/rapport-compacite-trace.md:17:> valeur de **0,085 % RMS** du max de la liste — la prévision de ce rapport était`
- **T1** `reports/rapport-compacite-trace.md:18:> 0,077-0,081 %, elle tient. La v3 est avec perte, donc la v2 reste le défaut.`
- **T1** `reports/rapport-compacite-trace.md:193:   pour une erreur RMS de 0,08 % du max de la liste. Le seuil, lui, reste global :`
- **T1** `reports/rapport-compacite-trace.md:236:   **normée** ; l'erreur mesurée ici (0,08 % du max) plaide pour, mais c'est le`
- **T1** `reports/rapport-localite-activation.md:45:| neurones tirés **> 90 %** du temps | **0,08 %** |`
- **T1** `reports/rapport-localite-activation.md:51:minuscule (0,08 %). Un préchargement figé à la PowerInfer ne couvrirait donc`
- **T1** `reports/rapport-localite-activation.md:77:  stable est trop petit (0,08 %) pour payer la complexité.`
- **T1** `=== 1,2 Mo ===`
- **T1** `reports/rapport-capteur-hebbien.md:34:sa copie coûte 7 Ko par matrice, 1,2 Mo par token, soit 19 Mo/s à 15,8 tok/s.`
- **T1** `reports/rapport-coherence-docs.md:97:| 41 | `docs/roadmap.md:107` | trace 512 jetons = « **12 288 listes** · 132 Mo · 6 octets par neurone actif » | 24 576 listes pour 512 jetons × 24 couches × 2 poin`
- **T1** `reports/rapport-compacite-trace.md:61:Ce sont les deux traces citées par le projet (« 132 Mo pour 512 jetons, 53 Mo en`
- **T1** `reports/rapport-compacite-trace.md:129:## 5. La trace dense (132 Mo, 512 jetons)`
- **T1** `reports/rapport-compacite-trace.md:154:   pas un artefact d'échantillon. Les 132 Mo de i16/u32 peu corrélés ne`
- **T1** `reports/rapport-compacite-trace.md:221:* **La sentinelle 0xFFFF et la lecture des traces v1.** Les 132 Mo et 53 Mo`
- **T1** `reports/rapport-inference.md:301:1,2 Mo d'accumulateurs, qui débordent le cache L2 de chaque cœur : chaque écriture`
- **T1** `reports/rapport-programme-evolutif.md:19:| Journal des activations de toutes les couches (24) | ~1,2 Mo/token, soit 19 Mo/s à 15,8 tok/s |`
- **T1** `reports/rapport-programme-evolutif.md:23:les *listes d'activations* suffit à rejouer intégralement le calcul. 1,2 Mo/token`
- **T1** `docs/format-flux.md:178:| la taille suit l'activité | densité ÷2,3 → trace ÷2,5 (132 Mo → 53 Mo) |`
- **T1** `docs/programme-recherche.md:29:   nommées. Journaliser les listes d'activations (1,2 Mo/token, **+3,0 %**)`
- **T1** `docs/roadmap.md:15:| 0.1 | **Format de trace du flux** : par (couche, position), la liste des neurones actifs (indice + valeur), l'échelle, le nombre | ✅ | écrit et relu sans perte ; **132 Mo pour 512`
- **T1** `docs/roadmap.md:17:| 0.3 | **Le format EST le contrat d'échange** (phase 3) : versionné, en-tête + paires | ✅ | codec de référence (`tools/flux_codec.py`) : aller-retour **identique** sur 132 Mo ; **e`
- **T1** `docs/roadmap.md:108:| 2026-09-30 | trace du flux, Qwen2.5-0.5B, 512 jetons, 24 couches, 2 points par couche | 24 576 listes · **132 Mo** en v1 · 6 octets par neurone actif · **+8 % de temps** (aujourd`
- **T1** `docs/roadmap.md:139:| `--abits 16` (défaut) | 99-100 % (rien n'est seuillé) | 132 Mo | 25 à 42 % |`
- **T1** `docs/roadmap.md:203:Mesuré, Qwen2.5-0.5B, 512 jetons, deux fenêtres de contexte, trace de 132 Mo :`
- **T1** `=== +3,0 % journalisation ===`
- **T1** `docs/programme-recherche.md:51:| Journalisation | +3,0 %, digest versionnable, archive automatique |`
- **T1** `=== 20 % à 56 % ===`
- **T1** `reports/rapport-attention-creuse.md:27:| **32** | **23,3302 (−1,20 %)** | **26,1199 (−0,52 %)** | **24,6857 (−0,86 %)** | **19,4136 (−0,56 %)** |`
- **T1** `reports/rapport-attention-creuse.md:66:(−1,20 % à 256, −0,56 % à 512). C'est la même complexité qu'une attention`
- **T1** `reports/rapport-empreinte-memoire.md:8:non pas en découpant les experts mais parce que **56 % du modèle (203 Go) est une`
- **T1** `reports/rapport-empreinte-memoire.md:235:## 8. LA DÉCOUVERTE : 56 % du modèle n'est pas un modèle de poids`
- **T1** `reports/rapport-empreinte-memoire.md:507:experts, mais parce que **56 % du modèle est une table creuse par nature** que`
- **T1** `docs/roadmap.md:28:| 1.2 | **Quantification choisie par la mesure** : par couche, par tenseur, plutôt qu'un réglage global | 🔬 | la densité par couche varie de **20 % à 56 %** (`reports/rapport-analys`
- **T1** `docs/roadmap.md:140:| `--abits 8 --act-thresh 0.05` | **26 à 56 %** | **53 Mo** | 26 à 56 % |`
- **T1** `docs/roadmap.md:95:contre 66 370 408, au prix de +0,074 % de perplexité au rejeu). Le protocole`
- **T1** `docs/roadmap.md:112:| 2026-09-30 | protocole de flux, deux processus, localhost | en-tête de **39 octets** à l'époque (79 aujourd'hui : les top-k voyagent) · dense f32 **3 623 octets/flux** · listes i`
- **T1** `docs/roadmap.md:58:| 3.4 | **Démonstration Colab** : préremplissage réparti (le décodage reste séquentiel — c'est écrit dans la vision) | 🔬 | **le préremplissage par lots sur le fil est FAIT et fidèle`
- **T1** `docs/roadmap.md:109:| 2026-09-30 | calcul réparti sur deux processus (12 couches chacun), 40 jetons | écart local/réparti **0,00e0** (144,8289 = 144,8289) après correction de deux défauts ; avant : ×1`
- **T1** `docs/roadmap.md:113:| 2026-09-30 | `TCP_NODELAY` sur le banc réparti, 200 jetons | attente du pair **97,6 → 16,1 ms** par jeton (calcul local : 15,9 ms) · banc complet 24,5 → **8,3 s**, soit le temps `
- **T1** `docs/programme-recherche.md:108:1. **Les motifs récurrents expliquent moins de 1 % de la difficulté.** Les grappes`
- **T1** `docs/histoire.md:11:| **Qtrinet** (origine) | inférence de LLM en ternaire / multi-bits sur un cluster de cartes **Stratix V** (Microsoft Storey Peak), 100 % logique, sans DSP. Le cahier des charges d`
- **T1** `docs/programme-recherche.md:180:| L'espace de caractéristiques est saturé | 100 % des directions dans le span | **déjà observé** (69 % des poids) |`
- **T1** `14:Le croisement push/pull du projet est mesuré à **~10 % de densité**. Ce qui`
- **T1** `19:| **9** | **20,1 %** | 6 | 40,5 % |`
- **T1** `20:| 0 | 25,9 % | 5 | 45,6 % |`
- **T1** `21:| 4 | 26,7 % | **1** | **56,3 %** |`
- **T1** `22:| 3 | 28,8 % | 8 | 29,2 % |`
- **T1** `30:Neurones actifs dans au moins 90 % des jetons, par couche : **0,89 % à 1,90 %**`
- **T1** `32:et c'est cohérent avec la mesure d'activation du projet (0,08 % « chauds » plus`
- **T1** `33:de 90 % du temps sur un autre modèle et un autre seuil).`
- **T1** `37:Par couche, les **10 % de neurones les plus forts portent 26 % à 67 %** de la`
- **T1** `38:magnitude, et le 1 % le plus fort en porte 5 % à 16 %. La couche 9 est la plus`
- **T1** `39:concentrée (67 % pour 10 %), la couche 1 la moins (26 %) — et c'est aussi la plus`
- **T1** `46:**28 % à 86 %**. Les couches 5 à 8 se partagent 84-86 % de leurs neurones`
- **T1** `48:partage que 28 %.`
- **T1** `56:Le croisement push/pull mesuré du projet est à ~10 % de densité. Avec les densités`
- **T1** `61:| 9 (20,1 %), 0 (25,9 %), 4 (26,7 %), 3 (28,8 %), 8 (29,2 %) | au-dessus du croisement | les listes coûtent moins que la matrice |`
- **T1** `62:| 6 (40,5 %), 5 (45,6 %), 1 (56,3 %) | en dessous | la matrice dense est plus économique |`
- **T1** `reports/rapport-coherence-docs-2.md:135:| 66 | `docs/plan-gpu-topk.md` (apparu pendant l'audit) | ×73 pour le KV en VRAM, 968 ms CPU, 1,99e-7, 12,4 → 12,5 ms en top-k CPU | ces chiffres sont ceux de ``
- **T1** `reports/rapport-gpu-topk-selection.md:344:| 5 | mesure 1 M de clés : ms/couche avec et sans top-k | ✅ **fait au niveau des noyaux** : chaîne complète **3,90 ms** pour 14 lignes × 1 M clés contre 539,9`
- **T1** `reports/rapport-session-2026-09-30.md:19:| **Plan du noyau GPU de top-k** | chiffré : le mode creux retombe sur le CPU (968 ms par couche à 1 M contre 13,2 ms avec le miroir VRAM) — le prochain chanti`
- **T1** `reports/rapport-prefill-par-lots.md:137:   le déport GPU (`DRAVE_GPU_TETE=1`, déjà mesuré à 6,2 ms/jeton contre 15,6 pour`
- **T1** `=== 13,6 / 7,0 ms / 308 Go/s ===`
- **T1** `reports/rapport-capteur-hebbien.md:8:création de nœuds par Hebb n'ajoute rien sur 69 % des poids du modèle, pour une`
- **T1** `reports/rapport-croisement-push-pull.md:107:   moteur gagne ×2,27 de bout en bout (13,6 → 30,7 tok/s, 510 jetons) à basculer`
- **T1** `reports/rapport-prefill-par-lots.md:193:| Qwen2.5-0.5B Q8_0, `--dense`, 16 fils | 512 | 17,1 s | **13,6 s** | **−20 %** |`
- **T1** `reports/rapport-transport-liste.md:29:| listes 0,10 | 36,5 % (327) | 1 347 | 216 | 35 483,0643 | 66 813,6606 | 8,8e-1 |`
- **T1** `reports/rapport-mla-experts.md:97:  61 couches MLA, routage sigmoïde ×2,827, 384 experts dont 8 par jeton.`
- **T1** `reports/bilan-multi-materiel.md:8:RTX 5000 (16 Go, NVLink 25,78 Go/s), 1 carte Stratix V GS (Storey Peak,`
- **T1** `reports/bilan-multi-materiel.md:97:| « Le FPGA n'a pas NVLink / les RTX 5000 non plus » | **Corrigée** — l'utilisateur avait raison, 25,78 Go/s mesurés par lien |`
- **T1** `reports/rapport-architecture-memoire.md:224:| **GPU 0 ↔ GPU 1** | | | **NVLink, 25,78 Go/s** |`
- **T1** `reports/rapport-architecture-memoire.md:226:**Le NVLink est là, et il vaut 2× le PCIe** (25,78 contre ~12 Go/s réels). CUDA`
- **T1** `reports/rapport-optimisations-auto.md:79:| `madvise(WILLNEED)` après le routage (experts) | 25,73 s contre 25,80 | 0,3 % |`
- **T1** `reports/rapport-passage-a-l-echelle.md:179:| QSFP+ 4,8 Go/s, NVLink 25,78 Go/s, PCIe x8 6,5 Go/s | le flux d'événements adressé par destination est un protocole réseau naturel : c'est la thèse du CDC,`
- **T1** `76:| 22 | `docs/roadmap.md:56` | critère 3.2 : « **3 623 → 1 589** octets par flux (÷2,3) pour 1,3 % d'écart à 1 024 jetons » | avec l'en-tête v4 : **3 663 → 1 629** ; le ÷2,3 et le 1,3 % restent vrai`
- **T1** `81:| 27 | `docs/format-flux.md:47`, `reports/rapport-compacite-trace.md:4-5`, `docs/roadmap.md:108` | trace dense 512 jetons : 132 396 736 → **66 370 408** (−49,87 %) | cohérent partout (le rapport ex`
- **T1** `82:| 28 | `docs/format-flux.md:58-61`, `REPRISE.md:248,340-341`, `docs/roadmap.md:94` | v3 : **45 079 930 o** (−32,1 % vs v2), rejeu 19,4029 (+0,074 %), 21 630 645 actifs | valeurs cohérentes entre do`
- **T1** `97:| 38 | `REPRISE.md:245,314`, `docs/roadmap.md:173-174`, `reports/rapport-attribution-kv.md:33-34` | clés f32 + valeurs int8 = **75 %** de la taille f32 ; int8 complet = **50 %** | le rapport de la `
- **T1** `98:| 39 | `docs/roadmap.md:184` | « la mesure clés f16 + valeurs int4 **est en cours** » | mesurée : 14,3209, **+0,61 %**, 2,625 o/33 % (`reports/rapport-placement-bits-kv.md:23`, `REPRISE.md:367`) | `
- **T1** `102:| 43 | `docs/roadmap.md:30` (1.4), `reports/rapport-session-2026-09-30.md:14`, `REPRISE.md:244` | clés f16 = +0,018 %/39 %, facteurs 130 et 840, int4 +364 % | conforme au rapport de placement (`:1`
- **T1** `156:4. **Corriger `docs/roadmap.md`** : ligne 56, « 3 663 → 1 629 » (÷2,3 et 1,3 %`
- **T1** `=== 5,3 G ev/s ===`
- **T1** `reports/bilan-multi-materiel.md:46:| CPU (16 threads) | **5,3 G évts/s** mesuré | ~57 nJ |`
- **T1** `reports/rapport-inference.md:219:identiques. Le débit par événement passe de 3,6 à **5,3 G év/s**.`
- **T1** `=== 380 Go/s / 18,1 ===`
- **T1** `reports/bilan-multi-materiel.md:48:| GPU (dispersion) | **18,1 G évts/s** mesuré | ~12,7 nJ |`
- **T1** `reports/bilan-multi-materiel.md:56:| GPU | 18,1 G évts/s de dispersion, 380 Go/s de lecture |`
- **T1** `reports/bilan-multi-materiel.md:113:contre 380 Go/s.`
- **T1** `reports/rapport-croisement-push-pull.md:96:| 200 | 22 % | 0 év — 9,6 s | 18,1 G év — 8,7 s (bascule) |`
- **T1** `docs/vision.md:100:| attention complète | noyau GPU, décodage **et** préremplissage | 22,16 → **3,29 ms/jeton** (÷6,7) ; préremplissage **×2,8** |`
- **T1** `REPRISE.md:185:| KV déporté dans le moteur (`DRAVE_GPU_KV=1`, ctx 4 096) | attention **22,16 → 3,29 ms/jeton** (÷6,7) · balayage 219,4 → **136,2 s** · perplexité 12,2177 → 12,2175 |`
- **T1** `=== 3,29 ms ===`
- **T1** `docs/vision.md:102:| tête Q6_K | GPU | 7,58 → **3,60 ms/jeton** |`
- **T1** `REPRISE.md:162:| 7 | noyaux GPU | **fait, quatre formats** | warp par ligne : tête **Q8_0** (1,6 ms contre 7,3 CPU, écart 2e-7), **MXFP4** (0,1 ms, écart **0,00e0** — bit à bit), **Q4_K** (0,5 contre `
- **T1** `REPRISE.md:174:| tête Q6_K déportée (Qwen 1.5B Q4_K_M, ctx 256, 510 jetons) | 7,58 → **3,60 ms/jeton** ; bout en bout 44,4 → 41,4 s (−7 %) ; lot 512 : 36,0 → 34,0 s ; **perplexité identique** (13,6877`
- **T1** `=== 3,60 ms ===`
- **T1** `REPRISE.md:192:| miroir VRAM paginé (capacité doublée à la demande) | à **ctx 1 M** : cache CPU 25,77 Go contre **0,05 Go** de VRAM pour 512 jetons écrits (l'allocation d'un bloc exigeait 25,77 Go et `
- **T1** `docs/contexte-long.md:234:| int4 | 1 048 576 | 968,5 | **13,2** | **×73** | 5,9e-5 |`
- **T1** `docs/vision.md:99:| cache KV d'une couche | VRAM (paginée, sur **deux** cartes) | attention à 1 M de clés : 968 → **13,2 ms** par couche |`
- **T1** `docs/plan-gpu-topk.md:17:| attention 1 M de clés, **CPU** (int4, host) | **968 ms** par couche |`
- **T1** `docs/plan-gpu-topk.md:85:doit montrer l'effet cherché : **968 ms → quelques dizaines de ms par couche**.`
- **T1** `=== 308 Go/s ===`
- **T1** `docs/contexte-long.md:245:   au lieu d'être transposée) : à 1 M de clés, **7,0 ms en f32 (308 Go/s, 69 %`
- **T1** `docs/vision.md:192:  **7,0 ms** par couche à 1 M (308 Go/s, 69 % de la bande VRAM) : quand le`
- **T1** `REPRISE.md:187:| dépaquetage vectorisé du noyau (1 M de clés) | f32 13,6 → **7,0 ms** (308 Go/s) · int8 15,0 → **6,5** · int4 13,2 → **7,4 ms** |`
- **T1** `=== +1,5 % ===`
- **T1** `reports/rapport-coherence-docs-2.md:100:| 41 | `docs/contexte-long.md:101-102` (E2) | KV int8 « **fait** (échelle par vecteur) », « mesuré : **+7,1 %** (llama.cpp : +3,1 %) » | le même document §4.bis`
- **T1** `docs/contexte-long.md:143:| int8 | 14,0707 (+7,1 %) | **13,3360 (+1,5 %)** | **13,3459 (+3,4 %)** |`
- **T1** `docs/contexte-long.md:164:1. **L'int8 reste à +3 %** (contre +1,5 % à 512 et +3,4 % à 4 591) : le coût ne`
- **T1** `docs/vision.md:188:* l'int8 sur le cache KV coûte **+1,5 %** de perplexité à 512 jetons et`
- **T1** `REPRISE.md:179:| KV int8, échelles par bloc | +1,5 % (512 jetons) et +3,4 % (4 591) — était +7,1 % et +5,2 % |`
- **T1** `reports/rapport-cpu-aer.md:18:- dispersion (`np.add.at`) : 364797216.41 G événements/s`
- **T1** `reports/rapport-coherence-docs.md:112:| 51 | `docs/contexte-long.md:103` | KV int4 « mesuré : **+384 %** — llama.cpp : +411 % » | +384 % est l'ancienne mesure à 512 jetons à échelle unique ; la mesure`
- **T1** `reports/rapport-placement-bits-kv.md:22:| int4 | int4 | 1,25 | 16 % | 66,0369 | **+364 %** |`
- **T1** `reports/rapport-placement-bits-kv.md:30:16 %  int4/int4 ................ +364 %`
- **T1** `reports/rapport-placement-bits-kv.md:52:   Et le 4 bits des DEUX côtés (1,25 octet, 16 % du f32) coûte **+364 %** : c'est`
- **T1** `reports/rapport-localite-activation.md:44:| magnitude portée par les 1 / 10 / 50 % de neurones les plus lourds | 12,3 % / **33,1 %** / 74,2 % |`
- … (tronqué)

## 5. Erreurs rencontrées

2 sorties en erreur ou divergentes. Les premières :

- **T1** : === portes.sh === #!/bin/bash # Les portes du dépôt, en une commande. # # Un chiffre de référence qui dérive sans qu'on s'en aperçoive ne vaut rien : # chaque porte est comparée à la valeur ATTENDUE, 
- **T1** : === portes.sh rest === # 5. Portes de FORMATS : chaque déquantificateur contre libggml. if [ "$RAPIDE" = "rapide" ]; then     echo "  (portes de formats : ignorées en mode rapide)" else     if command

