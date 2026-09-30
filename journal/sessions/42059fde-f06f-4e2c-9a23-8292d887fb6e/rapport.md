# Session 42059fde — Tu es vérificateur de documentation

| | |
|---|---|
| Identifiant | `42059fde-f06f-4e2c-9a23-8292d887fb6e` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-09-30 12:20 |
| Durée | 0.2 h |
| Tours | 1 |
| Messages | 88 |
| Appels d'outils | 132 |
| Fichiers touchés | 1 |
| Commandes | 97 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu es vérificateur de documentation dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave » : moteur d'inférence LLM en Rust, `std` seul, binaire `drave`). Tout est en FRANÇAIS : écris en français.  MISSION : traquer les **contradictions entre les documents et l'état réel du code**, et les **chiffres périmés**. Ce dépôt se veut rigoureux : chaque affirmation est censée être … [3143 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu es vérificateur de documentation dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave » : mo … [3423 caractères tronqués]

*132 appels d'outils.* Actions notables :

- bash — Lister la racine du dépôt
- bash — Voir l'historique git récent
- bash — Lister docs et reports
- bash — Lister le code source
- grep
- read
- bash — Extraire les drapeaux CLI du code
- bash — Extraire les variables d'environnement du code
- bash — Recenser les drapeaux cités dans la documentation
- bash — Comparer drapeaux docs vs code
- bash — Chercher le drapeau flux-norme retiré
- bash — Chercher autres drapeaux obsolètes
- bash — Relever les mentions de version par document
- bash — Comparer les octets par flux cités
- … et 89 autres

**Synthèse produite :**

⏵ Rédaction du rapport de cohérence documentaire

J'ai terminé les vérifications. J'écris maintenant le livrable.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs.md` | 1 | 3 |

### Commandes exécutées (échantillon)

- **T1** Lister la racine du dépôt
- **T1** Voir l'historique git récent
- **T1** Lister docs et reports
- **T1** Lister le code source
- **T1** Extraire les drapeaux CLI du code
- **T1** Extraire les variables d'environnement du code
- **T1** Recenser les drapeaux cités dans la documentation
- **T1** Comparer drapeaux docs vs code
- **T1** Chercher le drapeau flux-norme retiré
- **T1** Chercher autres drapeaux obsolètes
- **T1** Relever les mentions de version par document
- **T1** Comparer les octets par flux cités
- **T1** Comparer les tailles d'en-tête citées
- **T1** Voir les dates des commits récents
- **T1** Voir la dernière modif des docs clés
- **T1** Vérifier l'usage du mode LOT
- **T1** Dernière modification par fichier
- **T1** Vérifier les renvois vers fichiers inexistants
- **T1** Traquer les chiffres 356694 / 17,43
- **T1** Vérifier les faux positifs de renvois
- **T1** Voir qui cite ces fichiers
- **T1** Inspecter le nom exact du rapport prefill
- **T1** Fichiers touchés par les commits récents
- **T1** Inspecter le commit du compteur de flux
- **T1** Vérifier profil-experts dans vision
- **T1** Trouver l'affichage du nombre de flux
- **T1** Trouver le commit de renommage
- **T1** Comparer le chiffre du croisement push/pull
- **T1** Vérifier les appels Model::load
- **T1** Vérifier les corrections de drapeaux
- **T1** Compter les lignes du moteur
- **T1** Vérifier le +9,1 % du README
- **T1** Vérifier le 41,6 tok/s du README
- **T1** Vérifier la perplexité 24,90 du README
- **T1** Chercher 41,6 partout
- **T1** Vérifier les comptes de lignes cités
- **T1** Relever les chiffres de contexte-long
- **T1** Relever les statuts de contexte-long
- **T1** Comparer le statut de E5
- **T1** Comparer les variables DRAVE_*
- … et 57 autres

## 4. Mesures et résultats marquants

- **T1** `6b3b53f DRVF v2 sur le disque : −49,87 % de trace, rejeu identique`
- **T1** `af18f29 Transport en listes à 1 024 jetons : ÷2,3 pour 1,3 % d'écart`
- **T1** `17:| 0.3 | **Le format EST le contrat d'échange** (phase 3) : versionné, en-tête + paires | ✅ | codec de référence (`tools/flux_codec.py`) : aller-retour **identique** sur 132 Mo ; **et le rejeu dans `
- **T1** `111:| 2026-09-30 | protocole de flux v2, deux processus, localhost | en-tête de 39 octets (version, mode, réglages d'activation) · dense f32 **3 623 octets/flux** · listes i16 2 159 · **blocs + indice`
- **T1** `22:| la version change ? | **oui, 2 → 3** | un nœud v2 lirait `n×4` octets d'un corps qui en fait `n×hidden×4` avant de répondre « mode inconnu » : erreur exacte mais tardive, et qui ne dit pas que c'`
- **T1** `docs/roadmap.md:56:| 3.2 | **Granularité** : par couche, par bloc de canaux, par expert | 🔬 | livrés et mesurés : listes i16, **échelles par bloc de 32 canaux (valeurs i8)** et **indices par écarts** `
- **T1** `docs/roadmap.md:111:| 2026-09-30 | protocole de flux v2, deux processus, localhost | en-tête de 39 octets (version, mode, réglages d'activation) · dense f32 **3 623 octets/flux** · listes i16 2 159 · `
- **T1** `docs/roadmap.md:250:**1 745 octets contre 2 159** pour la liste i16, et 14 % d'écart contre 16 % —`
- **T1** `reports/rapport-transport-liste.md:4:3 623), mais à seuil 5 % le découpage coûte **×1,8 de perplexité** — la courbe`
- **T1** `reports/rapport-transport-liste.md:24:| dense f32 | 100 % | 3 623 | 3 623 | 144,8289 | **144,8289** | **0,00e0** |`
- **T1** `reports/rapport-transport-liste.md:25:| listes 0,00 | 100,0 % (896) | 3 622 | 3 622 | 144,8289 | 141,0539 | 2,6e-2 |`
- **T1** `reports/rapport-transport-liste.md:26:| listes 0,02 | 60,4 % (541) | 2 203 | 2 677 | 203,8033 | 213,7739 | 4,9e-2 |`
- **T1** `reports/rapport-transport-liste.md:104:| 0,00 | 98,1 % | 2 793 | 7,1e-2 | 3 622 octets · 2,6e-2 |`
- **T1** `reports/rapport-transport-liste.md:105:| 0,02 | 60,4 % | **1 778** | **2,2e-3** | 2 203 octets · 4,9e-2 |`
- **T1** `reports/rapport-transport-liste.md:131:| dense f32 | — | 100 % | 3 623 | **0,00e0** |`
- **T1** `reports/rapport-transport-liste.md:132:| blocs | 0,01 | 78,6 % | 2 268 | 2,7e-2 |`
- **T1** `reports/rapport-transport-liste.md:134:| listes i16 | 0,02 | 59,2 % | 2 159 | 1,6e-1 |`
- **T1** `reports/rapport-transport-liste.md:137:toujours les listes à sparsité égale (1 745 contre 2 159 octets, et 14 % contre`
- **T1** `reports/rapport-transport-liste.md:150:| 256 | 2,74e-2 | 2 268 | 78,6 % |`
- **T1** `reports/rapport-transport-liste.md:151:| **1 024** | **1,32e-2** | **1 589** | 79,8 % |`
- **T1** `reports/rapport-transport-liste.md:181:3 623 à 1 568 octets, soit **÷2,3**, pour 2,7 % d'écart sur 256 jetons de vrai`
- **T1** `docs/plan-prefill-reparti.md:20:| nouveau mode ou champ `t` ? | **mode 3** (`MODE_LOT`), pas de champ | le corps dense d'un lot est `t × hidden × 4` : `n` (offset 18) porte déjà le compte, l'en-tête r`
- **T1** `reports/rapport-compacite-trace.md:93:**Meilleur résultat tout court : `écarts+blocs` + zstd 19, 11 128 840 octets, −79,0 %.**`
- **T1** `reports/rapport-phase3-reparti.md:62:flux** (20 d'en-tête + 896 × 4) — soit 3,2 ko par couche d'état, alors que le`
- **T1** `6b3b53f 09-30 12:17 DRVF v2 sur le disque : −49,87 % de trace, rejeu identique`
- **T1** `af18f29 09-30 11:37 Transport en listes à 1 024 jetons : ÷2,3 pour 1,3 % d'écart`
- **T1** `=== 6b3b53f DRVF v2 sur le disque : −49,87 % de trace, rejeu identique`
- **T1** `Vérifié après la correction : écart **0,00e0** inchangé, perplexité 18,0206 des`
- **T1** `README.md:34:| **Croisement push/pull à 10 % de densité** | ✅ mesuré → [`reports/rapport-croisement-push-pull.md`](reports/rapport-croisement-push-pull.md) |`
- **T1** `README.md:376:| **pull** (`--dense`) | densité d'activation > 22 % — le cas d'un LLM dense | 29,5 tok/s |`
- **T1** `README.md:377:| **push** (`--push`) | densité < 22 % — réseau creux, k-WTA, ReLU | 13,6 tok/s à 100 %, 20,6 à 5 % |`
- **T1** `README.md:389:| Croisement push/pull | **~22 %** de densité d'activation, mesuré — pas 10 % (voir [`reports/rapport-croisement-push-pull.md`](reports/rapport-croisement-push-pull.md)) |`
- **T1** `REPRISE.md:124:1. **Mesurer avant de conclure.** Le croisement push/pull était annoncé à 10 %,`
- **T1** `REPRISE.md:125:   il est à 22 %. Dérouler un noyau « évident » n'a rien donné : le chemin était`
- **T1** `REPRISE.md:180:| KV déporté, ctx 512 (point de croisement) | attention 2,91 (CPU) contre 3,22 ms (GPU) : le noyau ne paie qu'au-delà de ~4 000 clés |`
- **T1** `docs/convertisseur.md:225:dessous du croisement mesuré à 22 % de densité : le régime où l'architecture`
- **T1** `docs/histoire.md:12:| **le virage événementiel** | l'idée qui a tout changé : ne plus multiplier des matrices, mais **pousser des listes d'activation** vers leurs destinations (AER, *Address Event Rep`
- **T1** `docs/vision.md:46:**mesuré** : en dessous d'environ **10 % de densité**, le push (listes) bat le`
- **T1** `docs/vision.md:133:   croisement push/pull à 10 % donne déjà l'ordre de grandeur de ce qu'on`
- **T1** `docs/vision.md:198:* **ce n'est pas « le sparse gagne toujours »** : le croisement à 10 % de densité`
- **T1** `reports/rapport-croisement-push-pull.md:43:➡️ **Les deux architectures se croisent à ~22 % de densité d'activation**, pas à`
- **T1** `reports/rapport-croisement-push-pull.md:96:| 200 | 22 % | 0 év — 9,6 s | 18,1 G év — 8,7 s (bascule) |`
- **T1** `reports/rapport-croisement-push-pull.md:100:➡️ La bascule tombe exactement au seuil mesuré (22 %), et le gain croît à mesure`
- **T1** `reports/rapport-croisement-push-pull.md:106:1. **Sur CPU, le mode pull est le bon choix** au-dessus de 22 % de densité. Le`
- **T1** `126:3. Le gain de bout en bout est **×1,39** (28,3 → 39,2 tok/s) pour **+26 % de`
- **T1** `144:| Qwen2.5-0.5B **Q4_0** | int8 (requantifié) | 21,1971 | +10,0 % | 18,0 | 28,3 |`
- **T1** `145:| Qwen2.5-0.5B **Q4_0** | **4 bits verbatim** | **21,0116** | **+9,1 %** | **13,1** | **38,9** |`
- **T1** `153:1. **Le prix réel des 4 bits sur ce modèle est +9,1 % de perplexité** — pas les`
- **T1** `155:   vrai coupable : elle coûtait 12 % de perplexité *en plus* du format.`
- **T1** `199:  choix sans hésitation : ×1,34 de débit **et** une perplexité légèrement`
- **T1** `201:- **Pour un modèle 8 bits**, requantifier en 4 bits coûte +26 % de perplexité :`
- **T1** `README.md:170:| 2 % | 1,020 | 0,251 | ×4,06 | 44,0 | ×7,96 |`
- **T1** `README.md:378:| **4 bits** (`--q4`, `--q4-tout`) | modèle 4 bits existant (Q4_0) ou débit prioritaire | **41,6 – 44 tok/s** |`
- **T1** `README.md:394:requantification), fait tourner un vrai Qwen2.5-0.5B **Q4_0** à **41,6 tok/s**`
- **T1** `reports/rapport-mur-memoire-4bits.md:114:| 4 bits corps entier | 21,9118 | +25,9 % | **39,2** | 13,1 |`
- **T1** `reports/rapport-mur-memoire-4bits.md:126:3. Le gain de bout en bout est **×1,39** (28,3 → 39,2 tok/s) pour **+26 % de`
- **T1** `reports/rapport-inference.md:251:| **Perplexité WikiText-2** | **24,90** | **27,83** | **+12 %** |`
- **T1** `reports/rapport-compacite-trace.md:145:   (50,1 Mo contre 41,6 Mo). Vérifié sur quatre segments du fichier : ce n'est`
- **T1** `reports/rapport-passage-a-l-echelle.md:47:par jeton ÷ 20 Go/s = **13 ms/jeton = 41 tok/s**, contre **41,6 tok/s mesurés**.`
- **T1** `reports/rapport-passage-a-l-echelle.md:56:| Qwen2.5-0.5B (dense) | 0,49 G | 0,26 Go | 13 ms | **41,6** (mesuré) |`
- **T1** `12:| gpt-oss-120b | 131 072 | 4 096 | ×32 | ×8 au-delà du déclaré → extrapolation |`
- **T1** `77:YaRN ×32 couvre **exactement** 131 072 jetons (4 096 × 32), c'est-à-dire le`
- **T1** `194:| f32 | 4 096 | 1,3 | **0,3** | ×4 | 5,1e-6 |`
- **T1** `252:| 4 096 | **KV déporté** | **12,2175** | **3,29** | **136,2 s** (−38 %) |`
- **T1** `341:à 2 048 jetons). L'écart de +3,0 % contre +0,8 % à 8 192 vient donc d'ailleurs :`
- **T1** `390:deux régimes décrochent (×6 entre 1 024 et 1 536 jetons de contexte). La`
- **T1** `431:**×32 en faveur du simple.** Sur toute l'étendue mesurée — 128, 512, 1 024,`
- **T1** `433:creuse avec la longueur (×1,1 à 512, ×131 à 5 120, ×32 à 16 384).`
- **T1** `102:| E2 | **KV int8** | **fait** (échelle par vecteur, dequantification à la lecture) | ÷4 sur le KV ; 128 k confortable | mesuré : +7,1 % de perplexité (llama.cpp q8_0 : +3,1 %) |`
- **T1** `103:| E3 | **KV int4** | **fait** (nibbles empaquetés) | 1 M tient en RAM (9,7 Go) et en VRAM | mesuré : **+384 %** — llama.cpp q4_0 : +411 % ; à réserver aux cas où la mémoire manque |`
- **T1** `104:| E4 | **KV déporté sur les 2 GPU** (pagination, préchargement) | **fait** : noyau `attn_kv_*` (tuiles de 32 clés en mémoire partagée, une passe par (tête KV, tranche), recombinaison + puits), mir`
- **T1** `REPRISE.md:152:| 8 | suite du plan 1 M | **fait pour E4/E5** | **E4 KV déporté en VRAM** : noyaux `attn_kv_*` (tuiles de 32 clés, softmax en ligne, recombinaison + puits), miroir du cache **paginé** (`
- **T1** `/// canaux, ~22 % plus petit, avec perte).`
- **T1** `// f16 par bloc de 32 canaux (l'étude de compacité annonce −22 % de plus,`
- **T1** `// début et personne ne s'en apercevait (2 octets sur 132 Mo).`
- **T1** `docs/plan-mla-vision.md:461:`tools/mtmd/clip.cpp` (320 ko) a été récupéré et dépouillé. Ce qui s'y lit, pour`
- **T1** `README.md:168:| **12,5 %** | 1,125 | **0,871** | **×1,29** | 12,7 | **×2,30** |`
- **T1** `reports/rapport-encodage.md:54:| 12.5 % | 1.125 | **0.871** | ×1.29 | 12.7 | ×2.30 |`
- **T1** `reports/rapport-transport-liste.md:230:ou 1 989 (blocs à 68 % d'activité), et le calcul distant coûte 16 ms : le réseau`
- **T1** `docs/roadmap.md:116:| 2026-09-30 | découpage fidèle à **1 024 jetons** (1 024 flux, texte réel) | perplexité **9,5146** des deux côtés, écart **0,00e0** · 19,4 ms en local contre 19,7 ms à attendre le`
- **T1** `docs/format-flux.md:142:| un lot ne change pas le résultat non plus | 256 jetons en 4 lots de 64 : écart **0,00e0** (18,0851 = 18,0851) ; en 1 lot de 256 : **0,00e0** (918 ko sur le fil) |`
- **T1** `docs/roadmap.md:285:| avant correction | 144,8289 | 1 621,7239 | ×11,2 |`
- **T1** `docs/roadmap.md:286:| après la norme seule | 144,8289 | 693,4492 | ×4,8 |`
- **T1** `reports/rapport-phase3-reparti.md:44:| avant correction | 144,8289 | 1 621,7239 | ×11,2 |`
- **T1** `reports/rapport-phase3-reparti.md:45:| après la norme seule | 144,8289 | 693,4492 | ×4,8 |`
- **T1** `disque coûte 6,04 octets par neurone actif (66 % d'indices u32) : indices par`
- **T1** `écarts = −49,7 % sans perte, avec blocs i8 = −60,9 %, + zstd = −79 %.`
- **T1** `+f32 dense (3,5 ko par jeton) ; le lot en listes est le mode 4, pas encore écrit.`
- **T1** `DRVF v2 sur le disque : −49,87 % de trace, rejeu identique`
- **T1** `L'étude de compacité déléguée disait où était le gras : **66 % du fichier est fait`
- **T1** `précédent tient sur un octet dans 99,9997 % des cas (22 échappements sur 8,79 M`
- **T1** `| trace dense, 512 jetons | 132 396 736 o | **66 370 408 o (−49,87 %)** |`
- **T1** `132 Mo, mais la comptabilité mentait depuis le premier jour).`
- **T1** `-actif**, et 505 ko par jeton sur une exécution dense (deux listes par couche).`
- **T1** `+99,9997 % des cas (22 échappements sur 8 790 000 mesurés). Trois octets par`
- **T1** `+| trace dense, 512 jetons | 132 396 736 o | **66 370 408 o (−49,87 %)** |`
- **T1** `| la taille suit l'activité | densité ÷2,3 → trace ÷2,5 (132 Mo → 53 Mo) |`
- **T1** `REPRISE.md:277:`TCP_NODELAY` a divisé l'attente du pair par six (**97,6 → 16,1 ms** par jeton,`
- **T1** `docs/colab-reparti.md:25:| latence | ✅ `TCP_NODELAY` : 16,1 ms d'attente contre 15,9 ms de calcul local (97,6 ms avant) |`
- **T1** `docs/contexte-long.md:260:appel — 24 couches × 6 appels CUDA par jeton, mesuré **24,5 ms/jeton** à 512`
- **T1** `docs/plan-prefill-reparti.md:355:   différé du pair la retarde : **97,6 ms d'attente contre 15,6 ms de calcul**,`
- **T1** `docs/roadmap.md:112:| 2026-09-30 | `TCP_NODELAY` sur le banc réparti, 200 jetons | attente du pair **97,6 → 16,1 ms** par jeton (calcul local : 15,9 ms) · banc complet 24,5 → **8,3 s**, soit le temps `
- **T1** `docs/roadmap.md:263:de 12 couches prend 15,9 ms par jeton, l'attente du pair 16,1 ms — soit **1,01×**.`
- **T1** `docs/roadmap.md:265:identiques. Avant `TCP_NODELAY`, cette attente était de 97,6 ms (6,26×) : le`
- **T1** `reports/rapport-mur-memoire-4bits.md:112:| 4 bits **attention** | 18,3503 | +5,4 % | 24,5 | 27,0 |`
- **T1** `reports/rapport-transport-liste.md:190:| calcul local (12 couches) | 15,6 ms/jeton | 15,9 ms/jeton |`
- **T1** `reports/rapport-transport-liste.md:191:| attente du pair | **97,6 ms/jeton** | **16,1 ms/jeton** |`
- **T1** `reports/rapport-transport-liste.md:195:L'attente de 97,6 ms n'était ni le calcul distant ni le débit : c'était **Nagle`
- **T1** `de cartes **Stratix V** (Microsoft Storey Peak) — 100 % logique, sans DSP.`
- **T1** `@@ -273,7 +273,7 @@ n'étaient pas le goulot. Et il coûte 838 ms là où l'accumulation en coûte 1`
- **T1** `docs/histoire.md:11:| **Qtrinet** (origine) | inférence de LLM en ternaire / multi-bits sur un cluster de cartes **Stratix V** (Microsoft Storey Peak), 100 % logique, sans DSP. Le cahier des charges d`
- **T1** `[timed out after 60000ms]`
- **T1** `REPRISE.md:147:| 3 | KV int8 puis int4 | **fait, jusqu'à 8 192** | **échelles par bloc de 32** : int8 +**1,5 %** à 512 (était +7,1 %), **+3,0 % à 8 192** (llama.cpp +0,8 %) ; int4 **+364 % à 8 192** c`
- **T1** `REPRISE.md:169:| KV int4, échelles par bloc | +219 % (512) et +287 % (4 591) — était +384 % et +450 % |`
- **T1** `REPRISE.md:170:| KV à 8 192 jetons (longueur de la référence llama.cpp) | f32 **14,2339** · int8 **14,6667 (+3,0 %)** contre +0,8 % chez llama.cpp · int4 **66,0369 (+364 %)** contre +494 % chez llama.`
- **T1** `REPRISE.md:233:| `DRAVE_KV_BITS=8` ou `4` | quantifie le cache KV (défaut f32) | le 4 bits coûte +364 % de perplexité à 8 192 |`
- **T1** `docs/contexte-long.md:103:| E3 | **KV int4** | **fait** (nibbles empaquetés) | 1 M tient en RAM (9,7 Go) et en VRAM | mesuré : **+384 %** — llama.cpp q4_0 : +411 % ; à réserver aux cas où la mémoire m`
- **T1** `docs/contexte-long.md:125:| **int4** | **63,61** (+384 %) | 72,80 (+411 %) | **71,05** (+450 %) | 98,53 (+494 %) |`
- **T1** `docs/contexte-long.md:144:| int4 | 63,6107 (+384 %) | **41,9442 (+219 %)** | **49,9438 (+287 %)** |`
- **T1** `docs/contexte-long.md:160:| **int4** | **66,0369** | **+364 %** | 98,53 | +494 % | 1 461 s |`
- … (tronqué)

## 5. Erreurs rencontrées

2 sorties en erreur ou divergentes. Les premières :

- **T1** : -rw-------. 1 stephane stephane 10689 30 sep 08:44 rapport-prefill-par-lots.md -rw-------. 1 stephane stephane  7101 30 sep 08:44 rapport-programme-evolutif.md -rw-r--r--. 1 stephane stephane 12143 30
- **T1** : bpe_np.py encoding.py gguf_min.py __pycache__ roofline.py sparsity.py ternary.py tiny_model.py transformer_np.py cpu_aer.c cpu_merge.c wikitext2_test.txt wt2.json [exit code: 2]

