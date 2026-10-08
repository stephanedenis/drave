# Session 04ed1834 — Tu travailles dans le dépôt

| | |
|---|---|
| Identifiant | `04ed1834-b0f8-42a1-aa21-75a75c19647e` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-08 09:18 |
| Durée | 0.0 h |
| Tours | 1 |
| Messages | 27 |
| Appels d'outils | 42 |
| Fichiers touchés | 0 |
| Commandes | 28 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (moteur d'inférence Rust « Drave », drave-core/). LECTURE SEULE STRICTE : ne modifie aucun fichier, ne compile pas, ne lance aucun test ni binaire.  Objectif : extraire tous les faits MESURÉS concernant la RÉPARTITION SUR PLUSIEURS MACHINES EN RÉSEAU (nœuds distants, pilote/nœud moteur, transport TCP, préremplissage répart … [1609 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (moteur d'inférence Rust « Drave », drave-co … [1889 caractères tronqués]

*42 appels d'outils.* Actions notables :

- bash — List repo, reports and docs directories
- glob
- read
- bash — Grep TCP_NODELAY, ethernet, RTT keywords
- bash — Grep two-machine and remote-link mentions
- bash — Grep IP addresses and LAN mentions
- bash — Grep latency proxy tool and list tools
- bash — Read roadmap phase 3 section
- bash — Read REPRISE network section
- bash — Grep flux-serveur usage across repo
- bash — Inspect Colab notebook for execution outputs
- bash — Find porte-flux and colab tools
- bash — Read REPRISE test section and git history for colab
- bash — Show Colab verification commit messages
- … et 17 autres

**Synthèse produite :**

⏵ Synthèse livrée ; voici le condensé final

**1) Chiffres mesurés** (valeur · contexte · source:ligne) — « mesuré » sauf mention contraire
- Qwen2.5-0.5B Q8_0, 2 processus 127.0.0.1, 12 couches/nœud, ctx 256 : 144,8289 = 144,8289, écart 0,00e0 à 40 jetons ; avant correctifs 1 621,7239 (×11,2), après la norme seule 693,4492 (×4,8) — `reports/rapport-phase3-reparti.md:42-46`
- Même banc 1 024 jetons : 9,5146 des deux côtés (0,00e0) ; 19,4 ms/jeton local vs 19,7 ms en attente du pair — `:50-54` ; flux dense = 3 663 o (79 d'en-tête + 896×4) — `:62-64`, `docs/format-flux.md:178`
- Préremplissage mode 3 : 256 jetons en 4 lots de 64 → 0,00e0 (18,0851) ; 1 lot de 917 583 o → 0,00e0 ; contrôle `--lot 1` (255 flux) → 0,00e0 (18,0206) ; 1 024 jetons/16 lots → 0,00e0 (9,5939) — `reports/rapport-prefill-reparti.md:39-44`
- Lots vs jeton, localhost machine au repos (256 jetons) : 116,7 → 22,4 (lots 16) → 18,5 (lots 64) → 16,6 ms/jeton (1 lot) = **7×** — `:71-77`
- Lien latent simulé (+20 ms/message, 64 jetons) : 1 lot = 1 145 ms calcul + 1 488 ms attente = **2,6 s** ; 1 flux/jeton = 350+394 ms/jeton = **47,6 s** → **18×**, écart 0,00e0 — `:56-61`
- TCP_NODELAY (200 jetons, localhost) : attente **97,6 → 16,1 ms/jeton** (calcul local 15,9 ms, 1,01×) ; banc 24,5 → 8,3 s (réf. locale 8,2 s) — `reports/rapport-transport-liste.md:187-200`, `docs/roadmap.md:113`
- Latence simulée (relais local) : 0 ms → 16,8 ms/jeton (1,01×) ; 5 ms → 33,0 (1,99×) ; 20 ms → 81,8 (4,89×) ; **attente ≈ calcul distant + 3,2 × latence**, 0,00e0 partout — `rapport-transport-liste.md:207-222`
- Débits : 0,25 Mbit/s à 20 jetons/s (blocs) ; « < 1 Mbit/s » ; lot de 64 = 229 455 o = 3,5 ko/jeton — `rapport-transport-liste.md:183`, `docs/colab-reparti.md:42-45`
- Listes : mode blocs 1 608 o/flux à 256 jetons (vs 3 663 dense), écart 2,74e-2 (÷2,3) ; mode 4 (lots de 16) 1,5 ko/jeton vs 3,5, écart 3,03e-2 — `REPRISE.md:926-928`, `reports/rapport-mode4-lot-listes.md:25-31`
- V4-Flash (hc), 2 processus même machine : dense 65 615 o/flux, 0,00e0, 4 873 ms/jeton (1,11×) ; listes 65 544 o, 9,13e-2 (399,6 % d'activité = état dense) — `reports/rapport-v4-reparti.md:14-17,88`
- V4.1 365,71 Go coupé couche 20 : 82 016 o/flux aller (79+1+16+20 480×4), 81 999 retour, 3 flux, 0,00e0, 1 743 713,6243 des deux côtés (68,0 vs 51,3 s) — `reports/rapport-decoupage-v41.md:4,82-90`
- K3 : relais 142 ko/saut (4 jetons × 7 168 canaux), transporté par **fichier** — `reports/rapport-passe-k3-disque.md:430-434,478`

**2) Deux machi
… [2946 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** List repo, reports and docs directories
- **T1** Grep TCP_NODELAY, ethernet, RTT keywords
- **T1** Grep two-machine and remote-link mentions
- **T1** Grep IP addresses and LAN mentions
- **T1** Grep latency proxy tool and list tools
- **T1** Read roadmap phase 3 section
- **T1** Read REPRISE network section
- **T1** Grep flux-serveur usage across repo
- **T1** Inspect Colab notebook for execution outputs
- **T1** Find porte-flux and colab tools
- **T1** Read REPRISE test section and git history for colab
- **T1** Show Colab verification commit messages
- **T1** Read start of prefill plan doc
- **T1** Locate journal digest for colab commit
- **T1** Show journal digest content from colab commit
- **T1** Grep journal digest for Colab runs
- **T1** Grep journal for LAN IP tests
- **T1** Read journal LAN IP test region
- **T1** Read journal colab simulation region
- **T1** Grep LAN port usage in journal
- **T1** Read prefill plan validation section
- **T1** Read K3 relay file-based transport section
- **T1** Grep assumptions and untested items
- **T1** Get line numbers from mode4 and v4 reports
- **T1** Get line numbers for bandwidth and latency figures
- **T1** Grep throughput units and iperf
- **T1** Read vision phase 3 and roadmap closing
- **T1** Grep protocol v6 and premix mentions

## 4. Mesures et résultats marquants

- **T1** `reports/rapport-transport-liste.md:224:Application à Colab : un aller-retour de 60 ms donne 16 + 3,2 × 30 ≈ **112 ms par`
- **T1** `reports/rapport-coherence-docs-2.md:61:| 12 | `docs/plan-prefill-reparti.md:76-78` + bandeau `:9-10` | règle R4 : « `n == 0` **et** `n × hidden × 4 > 256 Mo` sont refusés » ; « la règle R4 est mainten`
- **T1** `docs/roadmap.md:17:| 0.3 | **Le format EST le contrat d'échange** (phase 3) : versionné, en-tête + paires | ✅ | codec de référence (`tools/flux_codec.py`) : aller-retour **identique** sur 132 Mo ; **e`
- **T1** `docs/roadmap.md:113:| 2026-09-30 | `TCP_NODELAY` sur le banc réparti, 200 jetons | attente du pair **97,6 → 16,1 ms** par jeton (calcul local : 15,9 ms) · banc complet 24,5 → **8,3 s**, soit le temps `
- **T1** `docs/roadmap.md:282:identiques. Avant `TCP_NODELAY`, cette attente était de 97,6 ms (6,26×) : le`
- **T1** `docs/plan-prefill-reparti.md:111:3.4, pas dans le débit (cf. `docs/colab-reparti.md` : à 60 ms d'aller-retour,`
- **T1** `docs/plan-prefill-reparti.md:364:| 8 | `docs/colab-reparti.md` | répétition réelle (nœud moteur local, pilote Colab) | 200 jetons, `--lot 16`, écart **0,00e0** avec 60 ms d'aller-retour, et le tableau`
- **T1** `docs/plan-deepseek-v4-flash.md:38:| shard 1 (5,3 Mo) | ✅ l'**architecture** (`--plan` : « deepseek4, 43 couches, 256 experts (top-6) ») et le **tokenizer** : 129 280 jetons, aller-retour texte→jetons→`
- **T1** `docs/colab-reparti.md:30:| latence | ✅ `TCP_NODELAY` : 16,1 ms d'attente contre 15,9 ms de calcul local (97,6 ms avant) |`
- **T1** `docs/colab-reparti.md:58:  Un aller-retour Colab de 60 ms donne donc ≈ 112 ms par jeton, soit ~8 jetons/s`
- **T1** `docs/vision.md:174:   latence aller-retour jusqu'à 20 ms, attente ≈ calcul distant + 3,2 × latence`
- **T1** `docs/glossaire.md:1071:réparti au lieu de 15,9 ms de calcul ; `set_nodelay(true)` ramène l'attente à`
- **T1** `REPRISE.md:930:`TCP_NODELAY` a divisé l'attente du pair par six (**97,6 → 16,1 ms** par jeton,`
- **T1** `REPRISE.md:937:0,25 Mbit/s suffisent. Un aller-retour Colab de 60 ms donnerait ~8 jetons/s`
- **T1** `reports/rapport-transport-liste.md:196:L'attente de 97,6 ms n'était ni le calcul distant ni le débit : c'était **Nagle`
- **T1** `reports/rapport-transport-liste.md:231:ou 1 989 (blocs à 68 % d'activité), et le calcul distant coûte 16 ms : le réseau`
- **T1** `reports/rapport-coherence-docs.md:111:| 33 | `docs/colab-reparti.md:36` | « **1 989** en listes à échelle par bloc (68 % d'activité) » | 1 989 = ancien format (indices u16, 3 o/actif, en-tête 39). For`
- **T1** `reports/rapport-coherence-docs.md:149:| 61 | `docs/colab-reparti.md:103` | « `--flux-blocs --act-thresh 0.02` (÷2 sur le fil pour **0,2 %**) » | le rapport que ce document cite réfute explicitement ce`
- **T1** `reports/rapport-coherence-docs.md:245:| PÉRIMÉ | **38** | version du format de flux et du disque (7) · nombre de flux à 40 et 1 024 jetons (2) · en-têtes 26 et 39 octets (3) · octets par flux, par lot`
- **T1** `reports/rapport-prefill-reparti.md:81:les deux tableaux : moins d'allers-retours sur un lien distant (18× à 20 ms), et`
- **T1** `reports/rapport-session-2026-09-30.md:20:| **Colab prêt** | dépôt en un fichier (4,5 Mo), notebook (texte réel : perplexité ~20 au lieu de 17 869), trois voies de tunnel — vérifié de bout en bout | `c`
- **T1** `reports/rapport-coherence-docs-2.md:71:| 17 | `docs/format-flux.md:140`, `docs/colab-reparti.md:37`, `reports/rapport-session-2026-09-30.md:13`, `reports/rapport-prefill-reparti.md:85` | flux dense = `
- **T1** `reports/rapport-coherence-docs-2.md:79:| 25 | `reports/rapport-transport-liste.md:100` et `:230-231` | « trois octets par neurone actif (indice u16, valeur i8) » ; « 1 989 (blocs à 68 % d'activité) » `
- **T1** `docs/roadmap.md:57:| 3.3 | **Seuil de rentabilité** : à partir de quel débit réseau le découpage gagne | 🔬 | mesuré jusqu'à 20 ms de latence par message (`tools/proxy_latence.py`) : **attente ≈ calcul`
- **T1** `docs/roadmap.md:58:| 3.4 | **Démonstration Colab** : préremplissage réparti (le décodage reste séquentiel — c'est écrit dans la vision) | 🔬 | **le préremplissage par lots sur le fil est FAIT et fidèle`
- **T1** `docs/roadmap.md:119:| 2026-09-30 | coût du découpage selon la latence (relais retardateur, 256 jetons) | attente **16,8 ms** à 0 ms · **33,0** à 5 ms · **81,8** à 20 ms → `attente ≈ calcul distant + 3`
- **T1** `docs/colab-reparti.md:17:`tools/preparer_colab.sh` produit le dépôt en **un fichier** (`drave.bundle`, 4,5 Mo`
- **T1** `reports/rapport-minimal.md:13:| multi 2 plans ternaires | 4.00 | 73.44 % | -2.64 pt |`
- **T1** `reports/rapport-minimal.md:14:| multi 3 plans ternaires | 6.00 | 74.12 % | -1.95 pt |`
- **T1** `reports/rapport-minimal.md:15:| multi 4 plans ternaires | 8.00 | 75.98 % | -0.10 pt |`
- **T1** `reports/rapport-minimal.md:64:| modèle minimal — multi 4 bits (1 b/plan) | 0.0 Mo | 0.000 | 6994931.2 | 156 | 4680 |`
- **T1** `reports/rapport-minimal.md:79:3. **Le découpage en plans (multi-bits) dégrade progressivement** : 4 plans → 76.0 % (-0.1 pt). C'est la voie naturelle pour réutiliser un modèle 4 bits existant sans rée`
- **T1** `reports/rapport-coherence-docs.md:95:| 22 | `docs/plan-prefill-reparti.md:66-68` (règle R4) | refus de `n == 0` et de `n × hidden × 4 > 256 Mo` **avant** l'allocation | `recevoir_flux` fait `vec![0u8;`
- **T1** `reports/rapport-prefill-reparti.md:53:`tools/proxy_latence.py` ajoute 20 ms par message, comme le ferait un lien`
- **T1** `reports/rapport-passe-k3-disque.md:445:| **A** | 0..12 | écrit le relais : *« reprend à la couche 13 · 4 jetons × 7 168 canaux · 2 banque(s) »* |`
- **T1** `reports/rapport-passe-k3-disque.md:478:bit près, et le relais qui circule entre deux nœuds fait 142 ko par saut.`
- **T1** `docs/colab-reparti.md:65:  relais qui ajoute 20 ms par message (64 jetons, 12 couches par nœud), un seul`
- **T1** `| 2.2 | **Streaming des poids depuis le NVMe** (3,5 Go/s) pour ce qui ne tient pas en RAM — c'est la même idée : ne lire que ce qui parle | ⏳ | un modèle > RAM exécuté, débit mesuré |`
- **T1** `| 2.3 | **Cache d'experts rentable** : +6 % aujourd'hui ; grouper les trois projections par expert et supprimer les copies | ⏳ | ≥ +30 %, sinon abandonné (et écrit) |`
- **T1** `| 3.2 | **Granularité** : par couche, par bloc de canaux, par expert | ✅ | listes i16, **échelles par bloc (i8)** et **indices par écarts** (1 608 octets par flux à 256 jetons) ; **mode 4 « lot en lis`
- **T1** `| 3.3 | **Seuil de rentabilité** : à partir de quel débit réseau le découpage gagne | 🔬 | mesuré jusqu'à 20 ms de latence par message (`tools/proxy_latence.py`) : **attente ≈ calcul distant + 3,2 × la`
- **T1** `| 3.4 | **Démonstration Colab** : préremplissage réparti (le décodage reste séquentiel — c'est écrit dans la vision) | 🔬 | **le préremplissage par lots sur le fil est FAIT et fidèle** (mode 3 : 256 je`
- **T1** `contre 66 370 408, au prix de +0,074 % de perplexité au rejeu). Le protocole`
- **T1** `| 2026-09-30 | trace du flux, Qwen2.5-0.5B, 512 jetons, 24 couches, 2 points par couche | 24 576 listes · **132 Mo** en v1 · 6 octets par neurone actif · **+8 % de temps** (aujourd'hui : 66 Mo en v2 s`
- **T1** `| 2026-09-30 | calcul réparti sur deux processus (12 couches chacun), 40 jetons | écart local/réparti **0,00e0** (144,8289 = 144,8289) après correction de deux défauts ; avant : ×11,2 |`
- **T1** `| 2026-09-30 | diff KV f32 contre KV int8 (perplexité 19,3885 contre 19,8059) | première divergence couche 1 jeton 0 · couche la plus touchée FFN 2 (3,9 × la dynamique) · 229 000 neurones changés sur `
- **T1** `| 2026-09-30 | attribution du cache KV int8, 8 191 jetons, ctx 8 192 | f32 **14,2339** · int8 **14,6667** (+3,0 %) · **clés f32** + valeurs int8 **14,2372** (+0,023 %) · clés int8 + **valeurs f32** 14`
- **T1** `| 2026-09-30 | protocole de flux, deux processus, localhost | en-tête de **39 octets** à l'époque (79 aujourd'hui : les top-k voyagent) · dense f32 **3 623 octets/flux** · listes i16 2 159 · **blocs +`
- **T1** `| 2026-09-30 | `TCP_NODELAY` sur le banc réparti, 200 jetons | attente du pair **97,6 → 16,1 ms** par jeton (calcul local : 15,9 ms) · banc complet 24,5 → **8,3 s**, soit le temps du calcul local (8,2`
- **T1** `| 2026-09-30 | où mettre les bits du cache KV, 8 191 jetons, ctx 8 192 | à taille ÉGALE : clés f32 + valeurs int8 **+0,023 %** contre clés int8 + valeurs f32 **+3,01 %** (facteur 130) ; à 4,625 octets`
- **T1** `| 2026-09-30 | préremplissage par lots sur un lien à 20 ms par message | **2,6 s** en un lot de 64 contre **47,6 s** en un flux par jeton — 18×, écart 0,00e0 des deux côtés |`
- **T1** `| 2026-09-30 | mode 4 : lot en LISTES, 256 jetons par lots de 16 | **1,5 ko par jeton** (dense : 3,5) pour **3,03e-2** d'écart, contre 2,74e-2 pour le mode 2 par jeton |`
- **T1** `| 2026-09-30 | coût du découpage selon la latence (relais retardateur, 256 jetons) | attente **16,8 ms** à 0 ms · **33,0** à 5 ms · **81,8** à 20 ms → `attente ≈ calcul distant + 3,2 × latence`, écart`
- **T1** `| 2026-09-30 | découpage fidèle à **1 024 jetons** (1 023 flux, texte réel) | perplexité **9,5146** des deux côtés, écart **0,00e0** · 19,4 ms en local contre 19,7 ms à attendre le pair |`
- **T1** `réparti prenant le temps du calcul local (19,7 contre 19,4 ms par jeton). Il a`
- **T1** ``TCP_NODELAY` a divisé l'attente du pair par six (**97,6 → 16,1 ms** par jeton,`
- **T1** `0 ms, 1,99× à 5 ms, 4,89× à 20 ms, fidélité intacte (0,00e0) dans les trois cas.`
- **T1** `0,25 Mbit/s suffisent. Un aller-retour Colab de 60 ms donnerait ~8 jetons/s`
- **T1** `KV int8 (+3,0 % à 8 192) vient **entièrement des clés** — clés f32 + valeurs int8`
- **T1** `donne +0,023 %, clés int8 + valeurs f32 donne +3,01 %. Réglage utilisable tout de`
- **T1** `suite : `DRAVE_KV_BITS=8 DRAVE_KV_K_F32=1` (75 % de la taille f32 pour +0,02 %).`
- **T1** `(`git bundle`, 4,5 Mo — il n'y a pas de dépôt distant) et vérifie l'empreinte du`
- **T1** `#    moteur déporte alors tout seul les projections Q8_0 de plus de 8 Mo — le`
- **T1** `#    du même ordre que les 0,06 % mesurés alors — non re-mesuré depuis.)`
- **T1** `da6415b Colab : le mode lot chiffré dans la recette (2,6 s contre 47,6 s à 20 ms par message)`
- **T1** `d'une autre interface : écart 0,00e0, 15,7 ms d'attente contre 15,1 ms de calcul`
- **T1** `> disait, le code en écrivait quatre) ; et la règle R4 (plafond de 256 Mo) est`
- **T1** `| nouveau mode ou champ `t` ? | **mode 3** (`MODE_LOT`), pas de champ | le corps dense d'un lot est `t × hidden × 4` : `n` (offset 18) porte déjà le compte, l'en-tête reste **39 octets**, tous les off`
- **T1** `| la version change ? | **oui, 2 → 3** | un nœud v2 lirait `n×4` octets d'un corps qui en fait `n×hidden×4` avant de répondre « mode inconnu » : erreur exacte mais tardive, et qui ne dit pas que c'est`
- **T1** `l'état du jeton (position + j) commence à l'offset j × hidden × 4`
- **T1** `* **R3** — la dimension n'est pas transmise : le récepteur lit `n × hidden × 4``
- **T1** `* **R4** — `n == 0` et `n × hidden × 4 > 256 Mo` sont refusés **avant**`
- **T1** `3.4, pas dans le débit (cf. `docs/colab-reparti.md` : à 60 ms d'aller-retour,`
- **T1** `-Gain mesuré sur un lien à 20 ms par message : **2,6 s en un lot contre 47,6 s flux par flux** (18×). Je l'écris dans le rapport et la recette Colab.`
- **T1** `@@ -2179,7 +2179,7 @@ Gain mesuré sur un lien à 20 ms par message : **2,6 s en un lot contre 47,6 s`
- **T1** `@@ -2446,4 +2446,5 @@ Gain mesuré sur un lien à 20 ms par message : **2,6 s en un lot contre 47,6 s`
- **T1** `- Mode lot sur un lien latent : 18× (2,6 s contre 47,6 s)  Mesuré avec le relais retardateur (20 ms par message, 64 jetons, 12 couches par nœud) : un seul lot de`
- **T1** `- Colab : le mode lot chiffré dans la recette (2,6 s contre 47,6 s à 20 ms par message)" && git log --oneline -1 | cat; date +"%H:%M:%S"`
- **T1** `journal/sessions/34e1d4be-3708-4065-ae77-eca21f86e857/digest.md:313:12: `tools/preparer_colab.sh` produit le dépôt en **un fichier** (`drave.bundle`, 4,5 Mo`
- **T1** `journal/sessions/34e1d4be-3708-4065-ae77-eca21f86e857/digest.md:731:- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs && echo \"=== croisement 22/10 % ===\"; grep -n \"2`
- **T1** `référence locale  : perplexité 144.8289  (1.6 s)`
- **T1** `deux nœuds        : perplexité 144.8289  (1.6 s)`
- **T1** `transport         : dense f32 · 3623 octets par flux (aller) · 3623 au retour · 100.0 % d'activité (896 neurones par flux) · 40 flux`
- **T1** `temps             : 15.1 ms par jeton en local · 15.7 ms à attendre le pair (son calcul + l'aller-retour) · soit 1.04× le calcul local seul`
- **T1** `ordre de grandeur à 60 ms d'aller-retour : ~8 jetons/s (le découpage ne sert pas à accélérer)`
- **T1** `référence locale  : perplexité 17869.5162  (16.6 s)`
- **T1** `deux nœuds        : perplexité 17869.5162  (15.9 s)`
- **T1** `transport         : LOTS de 64 jetons · 229455 octets par lot (aller) · 3.5 ko par jeton · 4 lots (au lieu de 255 flux)`
- **T1** `temps             : 1564.1 ms par LOT en local · 1540.0 ms à attendre le pair · soit 0.98× le calcul local seul`
- **T1** `| 8 | `docs/colab-reparti.md` | répétition réelle (nœud moteur local, pilote Colab) | 200 jetons, `--lot 16`, écart **0,00e0** avec 60 ms d'aller-retour, et le tableau ms/jeton lots vs séquentiel |`
- **T1** `différé du pair la retarde : **97,6 ms d'attente contre 15,6 ms de calcul**,`
- **T1** `**Le remède tient en un fichier de 142 ko.** Pour 4 jetons et 7 168 canaux :`
- **T1** `| flux résiduel (4 × 7 168 f32) | 114 688 o |`
- **T1** `| pile (2 banques × 4 × 7 168 f32) | 229 376 o |`
- **T1** `| **A** | 0..12 | écrit le relais : *« reprend à la couche 13 · 4 jetons × 7 168 canaux · 2 banque(s) »* |`
- **T1** `bit près, et le relais qui circule entre deux nœuds fait 142 ko par saut.`
- **T1** `4:au lieu de f32 dense — 1,5 ko par jeton contre 3,5 — au prix d'une quantification`
- **T1** `28:| **mode 4, lots de 16** | **1,5 ko** (contre 3,5 en lot dense) | **3,03e-2** |`
- **T1** `93:   lots de 16, elle annonçait 0,9 ko par jeton pour 1,45 réels ;`
- **T1** `16:| deux nœuds, dense | **8 311,3347** — écart **0,00e0** | 65 615 | 400 % (16 384 canaux) | 4 873 ms (1,11×) |`
- **T1** `17:| deux nœuds, listes | 9,13e-2 d'écart | 65 544 | 399,6 % | 5 123 ms (1,16×) |`
- **T1** `docs/colab-reparti.md:44:  229 455 octets par lot de 64 jetons, soit **3,5 ko par jeton** — et surtout UN`
- **T1** `docs/roadmap.md:280:de 12 couches prend 15,9 ms par jeton, l'attente du pair 16,1 ms — soit **1,01×**.`
- **T1** `REPRISE.md:782:| 7 | noyaux GPU | **fait, quatre formats** | warp par ligne : tête **Q8_0** (1,6 ms contre 7,3 CPU, écart 2e-7), **MXFP4** (0,1 ms, écart **0,00e0** — bit à bit), **Q4_K** (0,5 contre `
- **T1** `REPRISE.md:794:| tête Q6_K déportée (Qwen 1.5B Q4_K_M, ctx 256, 510 jetons) | 7,58 → **3,60 ms/jeton** ; bout en bout 44,4 → 41,4 s (−7 %) ; lot 512 : 36,0 → 34,0 s ; **perplexité identique** (13,6877`
- **T1** `reports/rapport-transport-liste.md:192:| attente du pair | **97,6 ms/jeton** | **16,1 ms/jeton** |`
- **T1** `reports/rapport-minimal.md:59:Débits **mesurés** : DDR3 9,66 Go/s · PCIe x8 6,5 Go/s · fmax actuel 124 MHz.`
- **T1** `reports/rapport-minimal.md:81:5. **Tout le projet est borné par la DDR3**, pas par le calcul : à 124 MHz il ne faut que ~312 voies de MAC (≈ 9 400 ALM, 5 % du FPGA) pour saturer les 9,66 Go/s. 96 % du`
- **T1** `reports/rapport-precision.md:63:   passante. Le débit est fixé par la DDR3 (9,66 Go/s) ; 312 voies suffisent à la`
- **T1** `reports/rapport-cpu-aer.md:16:- bande passante lecture séquentielle : **11.5 Go/s**`
- **T1** `reports/rapport-cpu-aer.md:24:| Lecture séquentielle | 4,1 Go/s | 23,4 | **28,7** | 28,2 |`
- **T1** `reports/rapport-cpu-aer.md:36:| CPU, borné bande passante (28,7 Go/s) | 14.51 | 68.9 |`
- **T1** `reports/rapport-cpu-aer.md:50:   3× la bande passante (28,7 contre 9,66 Go/s) mais il est limité par sa`
- **T1** `reports/rapport-mode-listes.md:31:| 1 carte FPGA (9,66 Go/s) | 1.4 tok/s | 0.26 tok/s |`
- **T1** `reports/rapport-mode-listes.md:33:| CPU (28,7 Go/s) | 4.1 tok/s | 0.77 tok/s |`
- **T1** `reports/rapport-inference.md:201:Le moteur lisait 706 Mo par token en 95 ms, soit **7,4 Go/s sur les 28,7 Go/s`
- **T1** `reports/rapport-inference.md:232:**Ce qui reste sur la table** : 10,4 Go/s utilisés sur 28,7 → **2,8× avant`
- **T1** `reports/bilan-multi-materiel.md:8:RTX 5000 (16 Go, NVLink 25,78 Go/s), 1 carte Stratix V GS (Storey Peak,`
- **T1** `reports/bilan-multi-materiel.md:9:DDR3 9,66 Go/s, PCIe Gen3 ×8 6,5 Go/s, QSFP+ 4,8 Go/s).`
- **T1** `reports/bilan-multi-materiel.md:56:| GPU | 18,1 G évts/s de dispersion, 380 Go/s de lecture |`
- … (tronqué)

