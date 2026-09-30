# Session 5185ccb1 — Tu es relecteur ADVERSARIAL dans

| | |
|---|---|
| Identifiant | `5185ccb1-be24-4716-89df-62621e790444` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-09-30 17:03 |
| Durée | 0.1 h |
| Tours | 1 |
| Messages | 47 |
| Appels d'outils | 62 |
| Fichiers touchés | 5 |
| Commandes | 52 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu es relecteur ADVERSARIAL dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave » : moteur d'inférence LLM en Rust, `std` seul, binaire `drave`). Tout est en FRANÇAIS : écris en français. Ton rôle est de TROUVER DES DÉFAUTS, pas de valider.  CONTEXTE : la dernière heure a corrigé dix défauts trouvés par une relecture précédente du **mode 4 « lot en listes »** (protocole v … [3851 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu es relecteur ADVERSARIAL dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave » : moteur d'i … [4131 caractères tronqués]

*62 appels d'outils.* Actions notables :

- bash — List commits and repo contents
- bash — Check git status and HEAD
- bash — Show stat and src diff of 998d409
- bash — Show main.rs and model.rs diff
- bash — Read recevoir_flux implementation
- bash — Locate helpers
- bash — Read flux structs and verifier_taille
- bash — Read rest of recevoir_flux
- bash — Locate functions
- bash — Read run_ppl_reparti
- bash — Read server loop rest
- bash — Read quant_scratch and norme_finale
- bash — Read emb_imposee and rmsnorm
- bash — List models, reports, tools
- … et 46 autres

**Synthèse produite :**

⏵ Exécution du test D (8 flux mode 4, cap cumulatif)

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/tmp/adv/flux.py` | 1 | 0 |
| `/tmp/adv/testA_serveur.py` | 1 | 0 |
| `/tmp/adv/testB_client.py` | 1 | 0 |
| `/tmp/adv/testC_reel.py` | 1 | 0 |
| `/tmp/adv/testD_plafond.py` | 1 | 0 |

### Commandes exécutées (échantillon)

- **T1** List commits and repo contents
- **T1** Check git status and HEAD
- **T1** Show stat and src diff of 998d409
- **T1** Show main.rs and model.rs diff
- **T1** Read recevoir_flux implementation
- **T1** Locate helpers
- **T1** Read flux structs and verifier_taille
- **T1** Read rest of recevoir_flux
- **T1** Locate functions
- **T1** Read run_ppl_reparti
- **T1** Read server loop rest
- **T1** Read quant_scratch and norme_finale
- **T1** Read emb_imposee and rmsnorm
- **T1** List models, reports, tools
- **T1** Inspect Cargo.toml and CPU count
- **T1** Run release tests limited to 4 threads
- **T1** Show stats of KV policy commits
- **T1** Run release tests in drave-core
- **T1** Show KV report diffs
- **T1** Grep KV env vars
- **T1** Read KV config docs and parsing
- **T1** Read KV store selection
- **T1** Find mirror disable condition
- **T1** Read KV mirror init
- **T1** Check GPU availability
- **T1** Read forward with emb_imposee
- **T1** Read R4 requirements in plan
- **T1** Read R4 rule text
- **T1** Find banc-kv
- **T1** Read plan section 4
- **T1** Read run_banc_kv
- **T1** Read cle/valeur/vers_gpu
- **T1** Read kv_allouer
- **T1** Read main dispatch and CLI options
- **T1** Look for ids corpus files
- **T1** Read start of run_ppl_reparti
- **T1** Read option parser
- **T1** Read protocol constants and envoyer_flux
- **T1** Check binary and create workdir
- **T1** Read decoder_paires_blocs
- … et 12 autres

## 4. Mesures et résultats marquants

- **T1** `état pouvait être légal sans que le total le soit — 268 Mo par état sur 74 898`
- **T1** `// inconnu se refusait après avoir lu `n × 4` octets et s'être désynchronisé,`
- **T1** `+                // 268 Mo par état sur 74 898 états. La mémoire reste bornée (on`
- **T1** `+        // coût (0,9 ko annoncés contre 1,45 réels à 20 jetons en lots de 16).`
- **T1** `1780-    // inconnu se refusait après avoir lu `n × 4` octets et s'être désynchronisé,`
- **T1** `1863-                // 268 Mo par état sur 74 898 états. La mémoire reste bornée (on`
- **T1** `1901-            // relecture adversariale : VmSize 17 572 760 ko sur une seule trame).`
- **T1** `/// annonce `n = 4 milliards` fait allouer `n × dimension × 4` octets AVANT tout`
- **T1** `/// contrôle : jusqu'à ~15 To demandés au noyau. 256 Mo couvrent largement un lot`
- **T1** `/// de 8 192 jetons × 8 192 canaux (268 Mo... soit un lot par fenêtre maximale).`
- **T1** `// distantes : **97,6 ms** d'attente contre 15,6 ms de calcul local — six fois`
- **T1** `// coût (0,9 ko annoncés contre 1,45 réels à 20 jetons en lots de 16).`
- **T1** `3693-        // int8 — et non par le pool. Le pool coûtait 4 ms de plus par jeton pour`
- **T1** `3694-        // 72 Mo lus au lieu de 136 : ses seize tampons de sortie (9,7 Mo) sont`
- **T1** `- **les clés f16 coûtent 2,3× le temps CPU** des clés f32 (162 contre 70 ms par`
- **T1** `dernier coûte +2,25 % de perplexité. La tâche est robuste là où la perplexité ne`
- **T1** `+f16 coûtent **2,3× le temps CPU** des clés f32 (162 contre 70 ms par passe), et le`
- **T1** `+miroir VRAM — qui ramène l'attention à 1,7 ms par passe — **exige une disposition`
- **T1** `Chronométré sur 256 jetons, machine au repos : **116,7 ms par jeton** en flux simple`
- **T1** `le même à 4 096 (+0,011 % contre +2,25 % pour l'int8 complet), donc ce n'est pas un`
- **T1** `+  divise le temps de l'attention par 40 (1,7 ms contre 70 à 174 ms par passe) ;`
- **T1** `+* les **clés f16 coûtent 2,3× le temps CPU** des clés f32 (162 contre 70 ms par`
- **T1** `+D'où, par régime : **clés f16 + valeurs int8** (39 % du f32, +0,018 %) à contexte`
- **T1** `+| f32 | **70,5** | ✅ déporté (1,8 ms) | +3,2e-5 |`
- **T1** `+| int8 | 174,0 | ✅ déporté (1,7 ms) | +3,4e-5 |`
- **T1** `+1. **les clés f16 coûtent 2,3× le temps CPU des clés f32** (162 contre 70 ms par`
- **T1** `+| contexte court ou moyen, CPU | **clés f16 + valeurs int8** (39 % du f32, +0,018 %) | le meilleur compromis taille/qualité, et le temps CPU n'y est pas le facteur limitant |`
- **T1** `+| contexte long **avec** `DRAVE_GPU_KV=1` | **int8/int8** (28 %, +3,04 %) ou f32/f32 | le miroir exige une disposition homogène ; il divise le temps de l'attention par 40 (43 ms contre 1,7 s par jeto`
- **T1** `/// 4 octets pour 64 valeurs (3 % en int8). Les clés et les valeurs sont`
- **T1** `/// ce qui explique l'écart mesuré avec llama.cpp (+5,2 % de perplexité`
- **T1** `/// contre +0,8 % pour son cache q8_0).`
- **T1** `// écrase. C'est la différence mesurée avec llama.cpp (+5,2 % de`
- **T1** `// perplexité contre +0,8 % pour son cache q8_0).`
- **T1** `// de 23 à 159 ms. Le noyau lit une ligne par fil, donc des adresses`
- **T1** `// rentable : l'ancien lisait une ligne par fil (23 → 159 ms mesurés).`
- **T1** `| 33%   38C    P5             29W /  230W |    1399MiB /  16384MiB |     29%      Default |`
- **T1** `| 33%   32C    P8             20W /  230W |     381MiB /  16384MiB |     20%      Default |`
- **T1** `9:> disait, le code en écrivait quatre) ; et la règle R4 (plafond de 256 Mo) est`
- **T1** `76:* **R4** — `n == 0` et `n × hidden × 4 > 256 Mo` sont refusés **avant**`
- **T1** `l'état du jeton (position + j) commence à l'offset j × hidden × 4`
- **T1** `* **R3** — la dimension n'est pas transmise : le récepteur lit `n × hidden × 4``
- **T1** `* **R4** — `n == 0` et `n × hidden × 4 > 256 Mo` sont refusés **avant**`
- **T1** ``PLAFOND_FLUX` vaut 256 Mo et `verifier_taille` est la seule porte. En mode 4,`
- **T1** `peut annoncer `t × 256 Mo` de corps licites un par un : la mémoire resterait`
- **T1** `// Mesuré sur gpt-oss à contexte 512 : YaRN ×32 coûte un facteur 9`
- **T1** `// barrière ne tolère aucune sursouscription (mesuré : ×1,3 de perte à 40+1`
- **T1** `|   deux nœuds        : perplexité 333160063.9550  (0.2 s)`
- **T1** `|   transport         : dense f32 · 3663 octets par flux (aller) · 3663 au retour · 100.0 % d'activité (896 neurones par flux) · 5 flux`
- **T1** `|   temps             : 23.8 ms par jeton en local · 0.3 ms à attendre le pair (son calcul + l'aller-retour) · soit 0.01× le calcul local seul`
- **T1** `| [modele] 24 couches chargées en 818.593986ms — listes 0.00 Go , 4 threads`
- **T1** `|   référence locale  : perplexité 102.6664  (0.4 s)`
- **T1** `| [modele] 24 couches chargées en 803.077723ms — listes 0.00 Go , 4 threads`
- **T1** `|   deux nœuds        : perplexité 276304148.0523  (0.2 s)`
- **T1** `|   transport         : dense f32 · 3663 octets par flux (aller) · 3659 au retour · 100.0 % d'activité (896 neurones par flux) · 5 flux`
- **T1** `|   temps             : 26.6 ms par jeton en local · 0.2 ms à attendre le pair (son calcul + l'aller-retour) · soit 0.01× le calcul local seul`
- **T1** `| [modele] 24 couches chargées en 804.943447ms — listes 0.00 Go , 4 threads`
- **T1** `| [modele] 24 couches chargées en 823.626057ms — listes 0.00 Go , 4 threads`
- **T1** `| [modele] 24 couches chargées en 762.31551ms — listes 0.00 Go , 4 threads`
- **T1** `|   deux nœuds        : perplexité 151936.0000  (0.1 s)`
- **T1** `|   transport         : dense f32 · 3663 octets par flux (aller) · 79 au retour · 100.0 % d'activité (896 neurones par flux) · 5 flux`
- **T1** `|   temps             : 23.4 ms par jeton en local · 0.2 ms à attendre le pair (son calcul + l'aller-retour) · soit 0.01× le calcul local seul`
- **T1** `| [modele] 24 couches chargées en 776.686755ms — listes 0.00 Go , 4 threads`
- **T1** `|   transport         : dense f32 · 3663 octets par flux (aller) · 199 au retour · 100.0 % d'activité (896 neurones par flux) · 5 flux`
- **T1** `|   temps             : 23.5 ms par jeton en local · 0.2 ms à attendre le pair (son calcul + l'aller-retour) · soit 0.01× le calcul local seul`
- **T1** `| [modele] 24 couches chargées en 774.539682ms — listes 0.00 Go , 4 threads`
- **T1** `exactement le point de franchissement des 256 Mo, en nommant le cumul.`
- **T1** `total ne pas l'être — un pair annonçait 268 Mo par état sur 74 898 états`
- **T1** `+   franchit les 256 Mo, en le disant :`
- **T1** `+   plafond de 256 Mo` — 258 Mo envoyés en 1,4 s, aucun octet de trop décodé ;`
- **T1** `|   référence locale  : perplexité 151936.0000  (0.9 s)`
- **T1** `|   deux nœuds        : perplexité 151936.0000  (0.4 s)`
- **T1** `|   transport         : listes à échelle par bloc (2 octets/actif, écarts) · 199 octets par flux (aller) · 199 au retour · 0.0 % d'activité (0 neurones par flux) · 19 flux`
- **T1** `|   temps             : 17.1 ms par jeton en local · 2.6 ms à attendre le pair (son calcul + l'aller-retour) · soit 0.15× le calcul local seul`
- **T1** `|   référence locale  : perplexité 144.3267  (1.1 s)`
- **T1** `|   deux nœuds        : perplexité 886458700.4678  (1.1 s)`
- **T1** `|   transport         : lot dense f32 · lots de 16 jetons au plus · 35919 octets par lot (aller) · 3.5 ko par jeton · 2 lots pour 20 jetons`
- **T1** `|   temps             : 219.6 ms par LOT en local · 261.8 ms à attendre le pair · soit 1.19× le calcul local seul`
- **T1** `VERIF arithmetique : 35919 × 2 = 71838 octets ; 71838/20/1024 = 3.5077 ko/jeton (annonce 3.5)`
- **T1** `|   transport         : lot dense f32 · lots de 1000 jetons au plus · 71759 octets par lot (aller) · 3.5 ko par jeton · 1 lots pour 20 jetons`
- **T1** `|   temps             : 440.2 ms par LOT en local · 539.7 ms à attendre le pair · soit 1.23× le calcul local seul`
- **T1** `par message`, mesuré dans `reports/rapport-transport-liste.md`). Avec 60 ms`
- **T1** ``tools/proxy_latence.py` ajoute 20 ms par message, comme le ferait un lien`
- **T1** `| **en UN lot de 64** | 1 | 1 145 ms | 1 488 ms | **2,6 s** |`
- **T1** `| un flux par jeton | 63 | 350 ms/jeton | 394 ms/jeton | **47,6 s** |`
- **T1** `coûte ~4 × 20 ms de latence pure, et le mode lot en supprime 62 sur 63. C'est`
- **T1** `| un flux par jeton | 116,7 ms | **116,7 ms** |`
- **T1** `| lots de 16 | 358,0 ms | 22,4 ms |`
- **T1** `| lots de 64 | 1 185,3 ms | 18,5 ms |`
- **T1** `| **un seul lot de 256** | 4 255,6 ms | **16,6 ms** |`
- **T1** `|   référence locale  : perplexité 144.3267  (1.0 s)`
- **T1** `|   deux nœuds        : perplexité 144.3267  (1.1 s)`

## 5. Erreurs rencontrées

2 sorties en erreur ou divergentes. Les premières :

- **T1** : === mode 1 (LISTE) · n=1 · pos=100000 (ctx 64) ===   envoi      : 83 octets   reception  : reponse du serveur : 0 octets (mode=?, n=?)   serveur    : code=-6 signal=6     | [flux] client connecté : 12
- **T1** : === controle · reponse mode 0 · n=896 ===   requetes recues par le faux serveur : [(0, 896), (0, 896), (0, 896), (0, 896), (0, 896)]   client : code=0 signal=None     |   deux nœuds        : perplexit

