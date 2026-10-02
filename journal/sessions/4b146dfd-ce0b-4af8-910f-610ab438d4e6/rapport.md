# Session 4b146dfd — Tu es relecteur ADVERSE. Tu

| | |
|---|---|
| Identifiant | `4b146dfd-ce0b-4af8-910f-610ab438d4e6` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-02 09:52 |
| Durée | 0.1 h |
| Tours | 1 |
| Messages | 18 |
| Appels d'outils | 23 |
| Fichiers touchés | 0 |
| Commandes | 14 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu es relecteur ADVERSE. Tu ne modifies AUCUN fichier : tu produis un rapport de constats, avec citations exactes et numéros de ligne.  Contexte : le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet contient un moteur d'inférence nommé **Drave**. Sa vision est définie dans `docs/vision.md` et `docs/programme-recherche.md` — lis-les ENTIER d'abord (textes de référence), puis audite les documen … [3691 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu es relecteur ADVERSE. Tu ne modifies AUCUN fichier : tu produis un rapport de constats, avec citations exactes et num … [3971 caractères tronqués]

*23 appels d'outils.* Actions notables :

- bash — List docs and count lines
- read
- bash — Grep gate values and test counts
- bash — Inspect portes.sh and format counts
- bash — Check protocol version and forward coverage
- bash — Read README model table and list reports
- bash — Check MLA validation and format coverage
- bash — Check routing gates and format type list
- bash — Locate sources for MLA and attention figures
- bash — Check report coverage for MLA/vision figures
- bash — Check doc history and report dates
- bash — Check journal sourcing and list mentions
- bash — Count vision keywords per plan
- bash — Check machine/node mentions
- … et 2 autres

**Synthèse produite :**

⏵ Restitution du rapport adverse, 19 constats, aucune écriture.

Rapport adverse — 4 plans audités contre `docs/vision.md`, `docs/programme-recherche.md` et les faits du 02/10/2026. Aucun fichier modifié ; chaque citation a été revérifiée à la ligne. **19 constats.**

| fichier:ligne | citation exacte (≤ 25 mots) | problème | correction minimale proposée (texte de remplacement exact) | gravité |
|---|---|---|---|---|
| docs/plan-modeles-lourds.md:75-77 | « comparable à llama.cpp, ou l'écart expliqué — c'est la définition de « capable de rouler du best of breed » » | Objectif affiché = égaler llama.cpp ; la vision fait du flux de listes le contrat et llama.cpp une porte de correction (cf. plan-deepseek41-complet.md:9). | Remplacer par : « comparable à llama.cpp, ou l'écart expliqué — la conformité à llama.cpp est une porte de correction, pas le but : le but est de conduire des flux. » | élevée |
| docs/plan-modeles-lourds.md:99 | « perplexité sur 512 jetons comparable à llama.cpp, ou l'écart expliqué » | Critère de succès du forward réduit à la référence externe, sans porte de flux (tracé puis rejoué à l'identique) que le plan V4.1 impose (P0/P3). | Remplacer par : « perplexité comparable à llama.cpp **et** flux tracé puis rejoué à l'identique (portes Drave) ; sinon l'écart est expliqué » | moyenne |
| docs/plan-mla-vision.md:55 | « ### ÉTAT : MLA EST FAIT ET VALIDÉ » | Le chemin MLA validé est dense (numpy, 5,2e-7) ; le plan ne dit nulle part qu'il doit produire des listes/événements — le plan V4.1 en fait le premier écart (« 0 événements », P0). | Remplacer par : « ### ÉTAT : MLA EST FAIT ET VALIDÉ (chemin dense ; compteur d'événements à instrumenter, cf. plan-deepseek41-complet.md P0) » | moyenne |
| docs/plan-modeles-lourds.md:83 | « \| DeepSeek-V4 / V4-Flash / V4.1-Flash \| `deepseek4` (43 couches, 256 experts top-6, 1 M ctx) \| » | V4.1-Flash est `deepseek41` (même doc, l.120), 40 couches, 384 experts top-6 (plan V4.1, l.69) ; llama.cpp ne connaît pas `deepseek41`. | Remplacer par : « \| DeepSeek-V4 / V4-Flash \| `deepseek4` (43 couches, 256 experts top-6, 1 M ctx) ; V4.1-Flash : `deepseek41` (40 couches, 384 experts top-6) \| » | élevée |
| docs/plan-modeles-lourds.md:135-136 | « Aucune n'a de `forward` dans le moteur — c'est le chantier suivant. » | Faux depuis le 02/10 : `deepseek2` (Kimi-K2.7, 1 026 G) et `glm-dsa` (GLM-5.3, 754 G) se calculent (README, rapport-mla-experts) ; restent `deepseek4`/`deepseek41`. | Remplacer par : « `deepseek4` et `de
… [7353 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** List docs and count lines
- **T1** Grep gate values and test counts
- **T1** Inspect portes.sh and format counts
- **T1** Check protocol version and forward coverage
- **T1** Read README model table and list reports
- **T1** Check MLA validation and format coverage
- **T1** Check routing gates and format type list
- **T1** Locate sources for MLA and attention figures
- **T1** Check report coverage for MLA/vision figures
- **T1** Check doc history and report dates
- **T1** Check journal sourcing and list mentions
- **T1** Count vision keywords per plan
- **T1** Check machine/node mentions
- **T1** Print exact cited lines

## 4. Mesures et résultats marquants

- **T1** `./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:3663:=== perplexité 15.1757 sur 510 tokens (0 événements, 98.0 s) ===`
- **T1** `./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:5619:=== perplexité 15.1757 sur 510 tokens (0 événements, 97.3 s) ===`
- **T1** `./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:15970:gpt-oss ctx 256 (attendu 15.1757) : perplexité 15.1757 sur 510 tokens (0 événements, 98.2 s)`
- **T1** `./reports/rapport-transport-liste.md:48:(19,3885), mais ici 16 bits coûtent 2,6 % : la différence n'est pas la précision,`
- **T1** `./reports/rapport-compacite-trace.md:6:> **identique** (perplexité 19,3885 dans les deux cas), et la relecture par`
- **T1** `./reports/rapport-compacite-trace.md:16:> **+0,074 % de perplexité au rejeu** (19,4029 contre 19,3885) et d'une erreur par`
- **T1** `./reports/rapport-tete-restreinte.md:93:| 0 | 85,4 % | **19,3885** | référence |`
- **T1** `./reports/rapport-routage-experts.md:75:déplacé la porte Qwen3-30B de 799,8557 à 799,8152 (−0,005 %). Cause : la`
- **T1** `./reports/rapport-routage-experts.md:136:Qwen2.5-0.5B, **sans YaRN** : 19,3885 contre 18,9750 chez llama.cpp (2,2 %).`
- **T1** `./journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md:23916:| Qwen2.5-0.5B | Q8_0 | 19,3885 | 32 tok/s | **0,81 s** | **0,57 Go** |`
- **T1** `./journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md:25079:**Fidélité** : chemin CPU bit-exact (19,3885 avec et sans `QT_GPU`) ; sur gpt-oss l'écart est de 1,2 %, dû à l'ordre de sommatio`
- **T1** `**Montée en charge** (densité 100 %, meilleur de 3 passes) : 1 thread 0,41 G év/s →`
- **T1** `**Sans multiplieur** : décalages + additions donnent le résultat exact en 112,3 ms`
- **T1** `contre 2,5 ms pour i8×i8 (×44,9 sur CPU) — mais **sur FPGA le multiplieur n'existe`
- **T1** `> un débit surestimé à 7,53 G év/s), un `&mut` dans la boucle chaude (barrière`
- **T1** `> d'aliasing : 3,09 → 0,97 G év/s), et la **sursouscription** de l'attente active`
- **T1** `> (39+1 threads sur 40 CPU : effondrement ×2,4 — et le `yield_now()` censé le`
- **T1** `tools/portes_formats.sh                   # 17 formats × 2 blocs, contre libggml`
- **T1** `| Qwen2.5-0.5B | Q4_0 | 21,01 | 39 tok/s | 0,41 Go |`
- **T1** `| Qwen2.5-1.5B | Q4_K_M | 12,92 | 17 tok/s | 1,1 Go |`
- **T1** `| Qwen2.5-VL-7B | Q4_K_M | 10,99 | 2,8 tok/s | 4,5 Go |`
- **T1** `| **Qwen3-30B-A3B** (MoE 128 experts, top-8) | Q4_K_M | **7,61** | 5,4 tok/s | **17,7 Go** |`
- **T1** `61 couches MLA, routage sigmoïde ×2,827, 384 experts dont 8 par jeton.`
- **T1** `Comparaison à 7 jetons notés (llama.cpp : perplexité 890,4559) :`
- **T1** `259:/// IQ1_S : 50 octets par super-bloc de 256 poids (42 à 45 % des poids de GLM).`
- **T1** `route "GLM-5.3 : sigmoïde ×2,5" "$M/GLM-5.3-UD-IQ1_S/GLM-5.3-UD-IQ1_S-00001-of-00006.gguf" "sigmoïde"`
- **T1** `route "Kimi-K2.7 : sigmoïde ×2,827" "$M/Kimi-K2.7-Code-UD-IQ1_M/Kimi-K2.7-Code-UD-IQ1_M-00001-of-00008.gguf" "sigmoïde"`
- **T1** `docs/plan-mla-vision.md:179:| embedding de patchs (convolution 14 × 14) | **5,37e-07** |`
- **T1** `docs/plan-mla-vision.md:181:| projecteur (fusion 2 × 2 → `mm.0` → GELU → `mm.2`) | **1,73e-06** |`
- **T1** `reports/rapport-decoupage-moe.md:106:cluster, 625 ms au lieu de 3,9 s, 1 587 tenseurs vérifiés — le format est décrit`
- **T1** `reports/rapport-lecteur-multifichiers.md:239:| conversion | 435 + 8 × 144 = **1 587 tenseurs**, 18,60 Go, 351,7 s |`
- **T1** `101:| 5 | **format** : manifeste + index + disposition contiguë | ✅ **écrit et mesuré sur Qwen3-30B-A3B** : `commun.gguf` + 8 `cluster-XX.gguf`, un nœud charge **3,20 Go au lieu de 18,56** et 625 ms a`
- **T1** `docs/plan-modeles-lourds.md:22 | | **DeepSeek-V4.1-Flash** | le plus lourd des ouverts, MoE, agentique | **365,7 Go** (Q2) | — | **en cours** (26 % à 09h36) |`

## 5. Erreurs rencontrées

2 sorties en erreur ou divergentes. Les premières :

- **T1** : === portes.sh === #!/bin/bash # Les portes du dépôt, en une commande. # # Un chiffre de référence qui dérive sans qu'on s'en aperçoive ne vaut rien : # chaque porte est comparée à la valeur ATTENDUE, 
- **T1** : case "$v" in         *"$3"*) printf "  %-42s %s  ✅\n" "$1" "$3" ;;         *)      printf "  %-42s %s  ❌ (attendu %s)\n" "$1" "${v:-—}" "$3"; ECHEC=1 ;;     esac } M=/home/stephane/Data13TB/stephane/m

