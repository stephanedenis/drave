# Cohérence des documents avec le code — second passage

**En une ligne** : **66 affirmations** revérifiées contre le code et les rapports
**après** les changements du 30/09 ; **27 tiennent**, **17 sont périmées**, **14 se
contredisent** et **8 manquent** — les deux plus graves sont le **chiffre vedette du
cache KV** (« 75 % / 50 % » contre « 64 % / 28 % » dans le rapport qui l'a mesuré) et
la règle **R4** dont la moitié (`n == 0` refusé) n'est **pas** dans le code alors que
le plan affirme le contraire.

## Révision auditée, méthode, réserves

| | |
|---|---|
| Commit de référence | `a383cd7` (2026-09-30 15:11) |
| `drave-core/src/main.rs` | sha256 `bc53a66ad757faa6…` · 3 508 lignes |
| `drave-core/src/model.rs` | sha256 `61582adb8ded0f25…` · 3 928 lignes |
| Total `.rs` du moteur | **11 901 lignes** (7 fichiers) |
| Arbre au moment d'écrire | `journal/` modifié, `docs/plan-mode4-lot-listes.md` non suivi ; **73 commits** dans la journée |

Trois réserves, parce qu'elles changent la portée des constats :

1. **L'arbre a bougé pendant l'audit.** Deux documents sont apparus en cours de
   route : `docs/plan-mode4-lot-listes.md` (15:12, non commité) et
   `docs/plan-gpu-topk.md` (15:11, commité avec `a383cd7`). Ils sont examinés
   comme les autres, mais un plan daté du jour ne peut pas être jugé sur les
   chiffres qu'il promet ; seuls ses points d'ancrage au code l'ont été (lignes 65
   et 66 du tableau).
2. **Deux exécutions courtes seulement**, comme autorisé (`--limit 4`, 2 fils),
   pendant qu'une campagne de mesure tournait (`--ppl … --ctx 4096 --limit 4096
   --lot 512`) : aucune conclusion de performance n'en est tirée. Elles ont
   confirmé expérimentalement deux choses : la trace écrite par défaut est bien
   **DRVF v2** (`/tmp/verif_v2.bin`, 517 366 o, 192 listes, 171 554 actifs) et
   `DRAVE_TRACE_BLOCS=1` écrit bien **v3** (`/tmp/verif_v3.bin`, 346 636 o,
   192 listes, 166 206 actifs — avec perte, donc) ; et le tableau de bord
   `--options-actives` imprime bien l'état APRÈS affectations (les variantes KV
   qu'il sait afficher n'ont pas été exercées, faute de réglage quantifié).
3. **Pas de `cargo build` ni de `cargo test`** (interdits). Le compte de tests
   (13 `#[test]`) vient d'un `grep`, pas d'une exécution. Les chiffres de débit et
   de perplexité cités sont recoupés **entre documents**, pas re-mesurés.

Le `journal/` n'a pas été lu (consigne). Les liens `[texte](chemin)` de tous les
documents de référence ont été vérifiés par script : **aucun lien mort**.

---

## 1. Version du protocole, en-tête, modes, sémantique de `n`

| # | document | affirmation | ce que dit le code / la mesure | verdict |
|---|---|---|---|---|
| 1 | `main.rs:1363-1404` | constante de référence | `VERSION_FLUX = 4` (1376), `TAILLE_TETE = 79` (1404, verrouillé par `assert_eq!` 3344-3345), modes 0 dense · 1 listes · 2 blocs · 3 lot (1378-1393) | OK |
| 2 | `docs/format-flux.md:84-108` | en-tête de **79 octets**, version **4**, quatre modes, offsets | conforme à `recevoir_flux` (1707-1735) : topk_proj 39..66, attn 67, q·k 71, moe 75 | OK |
| 3 | `REPRISE.md:284-291`, `docs/roadmap.md:94-97`, `docs/vision.md:121`, `docs/colab-reparti.md:23-24` | protocole v4, quatre modes, version dans chaque en-tête | conforme au code | OK |
| 4 | `docs/format-flux.md:20` | diagramme du fichier : `version u16 = 1` | `TraceFlux::nouveau` écrit **2** par défaut et **3** si `DRAVE_TRACE_BLOCS=1` (`model.rs:549`) — la valeur « 1 » n'est plus qu'un cas historique relégué en §« Version 2 » | PÉRIMÉ |
| 5 | `docs/format-flux.md:28-30` | corps d'une liste : `indice u32 · valeur i16` [v1] puis `écart u8 · valeur i16` [v2] | la **v3** a un corps différent — `n_blocs u32 · n_blocs × f16 · n × (écart u8 [échappement → u16] · valeur i8)` (`model.rs:576-604`) — et cette disposition d'octets n'est écrite nulle part | MANQUANT |
| 6 | `docs/format-flux.md:34` | « `14 + 6 × n_actifs` en v1, `14 + 3 × n_actifs` en v2 » | exact, mais la v3 manque : `14 + 4 + 2·⌈n/32⌉ + 2·n_actifs` (`model.rs:622-626`) | MANQUANT |
| 7 | `docs/format-flux.md:51-61` | v3 = valeurs i8 + échelle f16 par bloc de 32, **avec perte** | conforme (`model.rs:557-604`) ; vérifié par les deux exécutions courtes (v3 plus petite, moins d'actifs, même nombre de listes) | OK |
| 8 | `docs/format-flux.md:66-67` | « le lecteur lit les trois versions » | `model.rs:691` refuse tout sauf 1, 2, 3 ; `tools/flux_codec.py:62` idem | OK |
| 9 | `docs/format-flux.md:30` | indice 255 → « l'indice ABSOLU sur les deux octets suivants » | vrai **aussi** pour le réseau depuis le correctif : `encoder_paires_blocs` écrit 2 octets (1548-1564), le décodeur en lit 2 (1566-1594), et ils sont testés ensemble | OK |
| 10 | `model.rs:527,547` (commentaire) | la v3 est « ~22 % plus petit » | mesuré : **−32,1 %** contre la v2 (66 370 408 → 45 079 930 o, `docs/format-flux.md:58`) et −65,9 % contre la v1 | CONTRADICTOIRE |
| 11 | `docs/format-flux.md:95` | `n` = « dimension (mode 0) ou actifs (mode 1) » | en mode 2 `n` = **actifs** (`main.rs:1627-1631`), en mode 3 = **états** (`envoyer_lot`, 1690) ; le commentaire `main.rs:1447` (« canaux (dense, listes) ») est faux pour les listes, `n` y valant `idx.len()` | MANQUANT |
| 12 | `docs/plan-prefill-reparti.md:76-78` + bandeau `:9-10` | règle R4 : « `n == 0` **et** `n × hidden × 4 > 256 Mo` sont refusés » ; « la règle R4 est maintenant DANS le code, avec son test » | seul le plafond existe : `verifier_taille` (`main.rs:1468`) ne teste que `> 256 Mo` et est appelé **4 fois** (1745, 1762, 1770, 1783), plus un contrôle direct dans le décodeur (1570) ; **aucun refus de `n == 0`**, aucun test (les 7 tests de `main.rs:3343-3474` couvrent l'en-tête, l'échappement, la troncature, l'aller-retour dense, l'indice hors dimension, les blocs démesurés et le lot géant) | CONTRADICTOIRE |
| 13 | `docs/plan-prefill-reparti.md:266` | « `DRAVE_FLUX_POS=1` fait imprimer `[flux] lot pos .. pos+t-1` des deux côtés » | cette variable **n'existe pas** ; le diagnostic livré est `DRAVE_DEBUG_FLUX` (`main.rs:1866`), côté serveur seulement, et imprime `[debug] lot reçu : n=… pos=… états=… plat=… corps=…` | PÉRIMÉ |
| 14 | `docs/plan-prefill-reparti.md:22-24,30,36-38,88,98,113,350` | en-tête de **39 octets**, `VERSION_FLUX` « encore 2 » puis « 2 → 3 », offsets ≤ 38 | 79 octets et version **4**. Le bandeau `:3-11` a bien été ajouté (v4, échappement 2 octets, R4) mais **ne dit pas que l'en-tête a gagné 40 octets**, donc les tableaux §1.1, §1.4 et §5 restent faux de 40 octets sans avertissement local | PÉRIMÉ |
| 15 | `docs/format-flux.md:117` | « le lot en listes est le mode 4, pas encore écrit » | exact (aucun `MODE_LOT_LISTES` dans le code) ; mais `docs/plan-mode4-lot-listes.md`, écrit le 30/09 à 15:12, spécifie ce mode 4 sans que `format-flux.md` y renvoie | MANQUANT |
| 16 | `docs/plan-prefill-reparti.md:67-69` (règle R1) | « l'émetteur DOIT utiliser le mode 0 pour un jeton seul » | vrai : la boucle du pilote est `while pos + 1 < ids.len()` (`main.rs:1991`), donc `t ≥ 2` toujours, et `--lot 1` passe par le chemin séquentiel | OK |

## 2. Chiffres de transport et de trace

| # | document | affirmation | ce que dit le code / la mesure | verdict |
|---|---|---|---|---|
| 17 | `docs/format-flux.md:140`, `docs/colab-reparti.md:37`, `reports/rapport-session-2026-09-30.md:13`, `reports/rapport-prefill-reparti.md:85` | flux dense = **3 663 octets** (79 + 896 × 4) | conforme : `hidden = 896` (confirmé par `[config] hidden 896` d'une exécution courte), `TAILLE_TETE + 896×4 = 3 663` | OK |
| 18 | `reports/rapport-phase3-reparti.md:62-63` | « **3 663 octets par flux** (20 d'en-tête + 896 × 4) » | 20 + 3 584 = **3 604**, pas 3 663 : le chiffre a été mis à jour, la parenthèse est restée à l'ancien en-tête | PÉRIMÉ |
| 19 | `REPRISE.md:297` | tableau « Ce que coûte le transport » : dense **3 623** | 3 663 ; et cette section est présentée comme l'état courant, 13 lignes après avoir annoncé l'en-tête de 79 octets (`:284`) | PÉRIMÉ |
| 20 | `REPRISE.md:298` | « listes i16, seuil 0,01 : **~2 300** octets » | aucune mesure de ce type : 2 159 est l'i16 au seuil **0,02** (vrai texte, `rapport-transport-liste.md:135`) et 2 268 est le mode blocs au seuil 0,01 à l'époque des 39 octets (`:133`, soit 2 308 avec l'en-tête v4) | PÉRIMÉ |
| 21 | `REPRISE.md:324` | « en UN lot de **917 543** octets » | 79 + 256 × 896 × 4 = **917 583** (`docs/format-flux.md:115`, `reports/rapport-prefill-reparti.md:42`) | PÉRIMÉ |
| 22 | `docs/roadmap.md:56` | critère 3.2 : « **3 623 → 1 589** octets par flux (÷2,3) pour 1,3 % d'écart à 1 024 jetons » | avec l'en-tête v4 : **3 663 → 1 629** ; le ÷2,3 et le 1,3 % restent vrais, mais ce sont les chiffres d'avant les top-k | PÉRIMÉ |
| 23 | `docs/roadmap.md:254-266` | tableaux : dense 3 623 · listes 0,00 = 3 622 · listes 0,05 = 897 · blocs 2 268 → 1 568 | valeurs de l'époque des 39 octets, non datées, alors que le même document dit 79 octets « aujourd'hui » (`:96`, `:112`) et que `docs/format-flux.md:145-148` met justement en garde contre la comparaison de deux époques | CONTRADICTOIRE |
| 24 | `reports/rapport-transport-liste.md:10` vs `:87-89` | §1 « dans le même en-tête de **39 octets** » ; §Ajouts « cette build parle la **4** » | le commit `d59d061` (12:11) a fait les deux **ensemble** : version 3 → 4 **et** en-tête 39 → 79. Un en-tête de 39 octets ne peut pas dire « 4 » : le rapport mélange deux époques dans le même document | CONTRADICTOIRE |
| 25 | `reports/rapport-transport-liste.md:100` et `:230-231` | « trois octets par neurone actif (indice u16, valeur i8) » ; « 1 989 (blocs à 68 % d'activité) » | son propre « Ajout — les indices par écarts » (`:167-183`) dit **2 octets par actif** et 1 568 : les deux phrases sont restées au format u16 ; avec l'en-tête v4, la valeur comparable est ≈ 1 419 (`docs/colab-reparti.md:37-38`) | CONTRADICTOIRE |
| 26 | `reports/rapport-phase3-reparti.md:64-65` | « le disque sait déjà écrire la même information en **6 octets par neurone actif** » ; « c'est le **prochain chantier (3.2)** : faire voyager la LISTE » | 6 octets/actif est la **v1** ; la v2 écrit 3,01 (`docs/format-flux.md:34-35`) et la v3 2,08 ; et la liste voyage depuis `--flux-liste`/`--flux-blocs` (commits `7b88131`, `af18f29`, `cb37c83`) | PÉRIMÉ |
| 27 | `docs/format-flux.md:47`, `reports/rapport-compacite-trace.md:4-5`, `docs/roadmap.md:108` | trace dense 512 jetons : 132 396 736 → **66 370 408** (−49,87 %) | cohérent partout (le rapport explique les 2 octets de sentinelle, `:75`, `:134`) | OK |
| 28 | `docs/format-flux.md:58-61`, `REPRISE.md:248,340-341`, `docs/roadmap.md:94` | v3 : **45 079 930 o** (−32,1 % vs v2), rejeu 19,4029 (+0,074 %), 21 630 645 actifs | valeurs cohérentes entre documents ; l'exécution courte confirme le sens (v3 plus petite, 166 206 actifs contre 171 554 sur la même trace de 4 jetons) | OK |
| 29 | `reports/rapport-compacite-trace.md:136` | « blocs, échelles f16 : **45 836 190** » (trace dense 512) | c'est la **projection** de l'étude ; la v3 réellement implémentée et mesurée donne **45 079 930** (bandeau `:14`, `docs/format-flux.md:58`) — l'écart n'est pas signalé dans le tableau | CONTRADICTOIRE |
| 30 | `reports/rapport-compacite-trace.md:231-243` et `:255-257` | « ce qu'il reste à valider : le rejeu i8, l'aller-retour Rust↔Python, la rétrocompatibilité » ; « les perplexités du rejeu … devront être refaites » | les trois sont faits : rejeu v3 = 19,4029 (bandeau `:13-18`), `flux_codec.py` lit 1/2/3, et le lecteur Rust aussi ; seul l'emballage zstd reste, et le bandeau le dit (`:20-22`) | PÉRIMÉ |
| 31 | `docs/format-flux.md:168` | « 39 puis 199 flux » à 40 et 200 jetons (le dernier n'est pas envoyé) | conforme à la boucle `while pos + 1 < ids.len()` (`main.rs:1991`) | OK |
| 32 | `docs/format-flux.md:169` | lot : 4×64 → 18,0851 ; 1 lot de 256 → 918 ko, 0,00e0 | conforme à `reports/rapport-prefill-reparti.md:41-42` (917 583 o ≈ 918 ko) | OK |
| 33 | `docs/format-flux.md:170` | « `--topk-q 900` contre `--topk-q 4` → 0,00e0, vérifié après `d59d061` » | conforme à `REPRISE.md:330-334` ; la vérification n'est plus tautologique depuis que les top-k s'appliquent et voyagent | OK |
| 34 | `reports/rapport-prefill-reparti.md:41-43` | 4 lots de 64, 1 lot, contrôle `--lot 1` = 255 flux, écarts 0,00e0 | conforme à la boucle du pilote ; le chemin réparti lui-même n'a pas été rejoué ici (campagne en cours, interdiction du mode serveur) | OK |
| 35 | `reports/rapport-session-2026-09-30.md:12`, `reports/rapport-prefill-reparti.md:57-61,72-78`, `REPRISE.md:377-379` | mode lot : **18×** à 20 ms (2,6 s contre 47,6 s) et **7×** par jeton (116,7 → 16,6 ms) | cohérent entre les trois ; les rapports 116,7/16,6 = 7,0 et 47,6/2,6 = 18,3 | OK |

## 3. Cache KV : le chiffre vedette contredit sa propre source

| # | document | affirmation | ce que dit le code / la mesure | verdict |
|---|---|---|---|---|
| 36 | `reports/rapport-placement-bits-kv.md:5` | en-tête : « clés f16 … 39 % de la taille f32 pour **+0,06 %** » | le tableau du même rapport (`:21`) donne **+0,018 %** à 8 191 jetons ; +0,057 % est la valeur à **contexte 256** (`:77`, `REPRISE.md:424`) — le titre est resté à l'ancienne campagne | CONTRADICTOIRE |
| 37 | `reports/rapport-placement-bits-kv.md:72-79` | « les deux lignes correspondantes du tableau se rempliront toutes seules » (campagne 8 192 en cours) | les lignes f16/int8 (`:21`) et f16/int4 (`:23`) **sont** remplies et déjà citées par `REPRISE.md:247,367` et `docs/roadmap.md:181-183` | PÉRIMÉ |
| 38 | `REPRISE.md:245,314`, `docs/roadmap.md:173-174`, `reports/rapport-attribution-kv.md:33-34` | clés f32 + valeurs int8 = **75 %** de la taille f32 ; int8 complet = **50 %** | le rapport de la campagne complète dit **64 %** (5,125 o/élément, `:16`) et **28 %** (2,25 o, `:20`) ; `REPRISE.md:365,368` dit lui-même 64 % et 28 % ; le code confirme 4 + 1,125 = 5,125 o (`model.rs:1074-1076`) | CONTRADICTOIRE |
| 39 | `docs/roadmap.md:184` | « la mesure clés f16 + valeurs int4 **est en cours** » | mesurée : 14,3209, **+0,61 %**, 2,625 o/33 % (`reports/rapport-placement-bits-kv.md:23`, `REPRISE.md:367`) | PÉRIMÉ |
| 40 | `REPRISE.md:423-426` (chantier 2) | « la campagne à 8 192 jetons est **en cours** ; reste à confirmer » | `REPRISE.md:247,360-373` présente déjà `DRAVE_KV_BITS=8 DRAVE_KV_K_F16=1` comme « le meilleur réglage mesuré » et « le réglage recommandé » — contradiction interne au même document | CONTRADICTOIRE |
| 41 | `docs/contexte-long.md:101-102` (E2) | KV int8 « **fait** (échelle par vecteur) », « mesuré : **+7,1 %** (llama.cpp : +3,1 %) » | le même document §4.bis (`:143-145`) dit « corrigé, échelles par bloc de 32 : **+1,5 %** à 512, **+3,0 %** à 8 192 » ; la ligne E2 n'a pas suivi | PÉRIMÉ |
| 42 | `docs/contexte-long.md` (chapitre KV, §4.bis et tableau E) | — | aucune mention de la **campagne de placement des bits**, de `DRAVE_KV_K_F16` ni du réglage recommandé, alors que c'est le document de référence du cache KV et que le sujet a été tranché le jour même | MANQUANT |
| 43 | `docs/roadmap.md:30` (1.4), `reports/rapport-session-2026-09-30.md:14`, `REPRISE.md:244` | clés f16 = +0,018 %/39 %, facteurs 130 et 840, int4 +364 % | conforme au rapport de placement (`:16-33`) et à `contexte-long.md:160` | OK |
| 44 | `REPRISE.md:247,364-369` | table f16 3,125 o / 39 % / +0,018 % | conforme au rapport (`:21`) | OK |

## 4. Drapeaux, variables, renvois

| # | document | affirmation | ce que dit le code / la mesure | verdict |
|---|---|---|---|---|
| 45 | `REPRISE.md:383-387` | `--options-actives` imprime « APRÈS toutes les affectations », branché dans les quatre modes principaux, cache KV avec sa variante | conforme : `main.rs:507`, fonction 350-372, appels 699 (inférence), 1822 (nœud moteur), 1923 (pilote), 3080 (perplexité) ; vérifié par exécution pour la forme générale (`[options] cache KV : 32 bits · f16 avant false`), les variantes `k_f32`/`k_f16`/`v_f32` étant dans le code (366-370) — non exercées ici, faute de réglage KV quantifié | OK |
| 46 | `REPRISE.md:388` | « un drapeau inconnu est signalé » | `main.rs:605` (avertissement, plus d'avalage silencieux) | OK |
| 47 | `reports/rapport-drapeaux-ignores.md:196-198` | recommande « `--options-actives` (et `--options-strict`) » | `--options-actives` **existe** depuis `1a4beb3` ; `--options-strict` n'existe pas ; l'addendum (`:1-11`) signale les correctifs de drapeaux mais pas cette moitié faite | PÉRIMÉ |
| 48 | `REPRISE.md:240-259` | table des variables `DRAVE_*` | les 28 variables du code y sont décrites (les six `DRAVE_BANC_KV_*` sous forme abrégée `_UNIT`, `_KUNIT`, …) ; aucune variable documentée n'est absente du code, **sauf** `DRAVE_FLUX_POS` (ligne 13) | OK |
| 49 | `README.md:345` | ligne gpt-oss : `\| … \| MXFP4 \| **blocs lus** \| **15,1757 (ctx 256)** \| 60 Go \|` | la ligne est **décalée d'une colonne** : « blocs lus » occupe la colonne perplexité et 15,1757 la colonne débit ; la référence est 15,1757 (`REPRISE.md:70`) | CONTRADICTOIRE |
| 50 | `docs/vision.md:109` | renvoi `reports/rapport-pe-evenementiel.md` | ce fichier n'existe pas dans le dépôt ; il est dans `../FPGA-Stratix-V/docs/` — `README.md:30-31` a été corrigé le 30/09, `vision.md` ne l'a pas été | PÉRIMÉ |
| 51 | tous les documents de référence | liens `[texte](chemin)` | vérification par script : **aucun lien mort** ; les rapports cités existent, sauf `reports/rapport-mode4-lot-listes.md` qui est un livrable **annoncé** par le plan mode 4 (étape 7), pas un renvoi cassé | OK |
| 52 | `docs/colab-reparti.md:10-16` | mise en place : `tools/preparer_colab.sh`, `colab/README.md`, `colab/Drave-reparti.ipynb` | les trois existent ; mais `tools/colab_cote_local.sh` (créé à 15:09, commit `90a74a6`) n'est cité par aucun document | MANQUANT |
| 53 | `REPRISE.md:446` | carte du dépôt : `gpu/drave_gpu.cu + .ptx` | les noyaux sont dans **`drave-core/gpu/`** (`include_str!("../gpu/drave_gpu.ptx")`) ; la ligne est placée sous un bloc titré `drave-core/src/`, donc elle se lit `drave-core/src/gpu/…` — le correctif de l'audit n°1 a déplacé la ligne sans lever l'ambiguïté | PÉRIMÉ |

## 5. Statuts, comptes de lignes, affirmations « fait / à faire »

| # | document | affirmation | ce que dit le code / la mesure | verdict |
|---|---|---|---|---|
| 54 | `docs/vision.md:222` et `:147`,`:210` | axe 3 : « **rien** — hypothèse écrite » ; « les **mesures à faire** : débit d'un flux sérialisé, latence aller-retour… » ; « l'axe 3 est une hypothèse » | le §4 du même document (`:117-125`) dit « le transport existe, et c'est l'axe où le projet a le plus avancé », et `docs/roadmap.md` donne 3.1 à 3.5 ✅/🔬 avec les mesures (3 663 o, 1 419, 0,25 Mbit/s, `attente ≈ calcul + 3,2 × latence`) | CONTRADICTOIRE |
| 55 | `docs/roadmap.md:248` | « Le protocole, lui, **n'a pas changé d'un octet** : c'est le moteur qui était faux » | vrai du correctif de fidélité décrit juste avant, faux comme phrase de la page : le même document date l'en-tête de 79 octets « aujourd'hui » (`:96`, `:112`) et le protocole est passé de 39 à 79 octets le jour même (`d59d061`) | CONTRADICTOIRE |
| 56 | `docs/roadmap.md:305-307` | « Ce qui reste : le lot en listes (mode 4), l'ordonnanceur de placement, la démonstration sur Colab » | conforme au code : aucun `MODE_LOT_LISTES`, aucune phase 4 livrée | OK |
| 57 | `docs/colab-reparti.md:22-28` | fidélité ✅, version ✅, latence ✅, au-delà de localhost ✅, « deux machines avec le même GGUF » ❌, préremplissage par lots ✅ | conforme : `Model::load` lit le fichier entier, `--flux-serveur` accepte `0.0.0.0:PORT` (`main.rs:1807-1814`), `MODE_LOT` existe | OK |
| 58 | `REPRISE.md:35` vs `:409`, `reports/rapport-session-2026-09-30.md:66` | « `cargo test` **11/11** » ; ailleurs « **Treize tests** » et « 13/13 » | le code contient **13** `#[test]` (main.rs 7, list.rs 3, engine.rs 2, model.rs 1) | CONTRADICTOIRE |
| 59 | `reports/rapport-session-2026-09-30.md:4` vs `:66` | « **Trente-cinq** commits » ; plus bas « **quarante** commits » | la journée compte **73 commits** (dont **70** déjà commités à 14:09) : les deux nombres ne peuvent pas être vrais ensemble | CONTRADICTOIRE |
| 60 | `README.md:281`, `README.md:355`, `REPRISE.md:16` | « **11 440** lignes » de Rust | **11 901** lignes de `.rs` (main.rs 3 508, model.rs 3 928, list.rs 1 440) ; le chiffre datait de l'audit n°1, les tests du soir l'ont dépassé | PÉRIMÉ |
| 61 | `README.md:18-46` (« État du projet ») | tableau d'état du projet | n'a **aucune ligne** sur le chantier du jour : protocole v4, DRVF v2/v3, transport TCP, mode lot, `--options-actives`, clés KV f16, kit Colab — ni renvoi vers `REPRISE.md`/`docs/roadmap.md`/`docs/format-flux.md` | MANQUANT |
| 62 | `docs/colab-reparti.md:24` | réglages transportés = « niveaux, seuil, top-k, renorm » | le code en transporte **14** : les quatre cités + 7 top-k de projection + attn + q·k + MoE (`main.rs:1649-1656`) ; `docs/format-flux.md:97-104` les liste, pas ce document | MANQUANT |
| 63 | `REPRISE.md:389-390` | « les **trois modes** qui allouent sur une taille lue dans l'en-tête refusent au-delà de 256 Mo » | le plafond couvre **4 appels** de `verifier_taille` (1745 lot, 1762 blocs, 1770 longueur, 1783 corps générique) **plus** un contrôle direct dans `decoder_paires_blocs` (1570) ; l'affirmation de fond est vraie, « trois modes » sous-compte | OK |
| 64 | `REPRISE.md:409-411` | « Treize tests : les sept du protocole et du plafond, dont deux qui envoient une VRAIE trame forgée dans une socket » | conforme : 7 tests dans `main.rs`, dont `une_trame_liste_hors_dimension_ne_tue_pas_le_noeud` et `un_nombre_de_blocs_dement_grand_est_refuse` | OK |
| 65 | `docs/plan-mode4-lot-listes.md` (apparu pendant l'audit) | mode 4 = protocole **v5**, en-tête inchangé de 79 octets, `n` = états | cohérent avec l'état du code (`VERSION_FLUX = 4`, `TAILLE_TETE = 79`, `MODE_LOT = 3`, pas de mode 4) ; le document dit lui-même « non écrit » | OK |
| 66 | `docs/plan-gpu-topk.md` (apparu pendant l'audit) | ×73 pour le KV en VRAM, 968 ms CPU, 1,99e-7, 12,4 → 12,5 ms en top-k CPU | ces chiffres sont ceux de `REPRISE.md:163-164,184,224` et de la mesure GPU du jour ; rien de contradictoire relevé | OK |

---

## Les corrections à faire, dans l'ordre

1. **Trancher le chiffre du cache KV, et l'écrire une fois pour toutes.** Les
   documents publient « 75 % de la taille f32 » (REPRISE:245,314 ;
   roadmap:173-174 ; rapport-attribution-kv:33) et « int8 complet 50 % »
   (attribution:34 ; roadmap:174) alors que le rapport de la campagne complète
   donne **64 %** et **28 %** — et le tableau de REPRISE:365,368 dit déjà 64/28.
   Corriger les quatre documents, ou re-mesurer si la campagne en cours dit autre
   chose, mais ne pas laisser deux valeurs pour le même réglage.
2. **Corriger `reports/rapport-placement-bits-kv.md`** : ligne 5, « +0,06 % » →
   « +0,018 % à 8 191 jetons (+0,057 % à contexte 256) » ; remplacer la section
   « La suite : clés en f16 » (72-79) par le résultat mesuré. Puis retirer les
   « en cours » de `docs/roadmap.md:184` et `REPRISE.md:423-426`.
3. **Mettre à jour la section transport de `REPRISE.md` §6bis** (297-299) :
   en-tête 79, dense **3 663**, ligne des écarts ~1 608 (256 jetons) / **1 629**
   (1 024), et supprimer « ~2 300 » qui ne correspond à aucune mesure ; ligne 324,
   **917 543 → 917 583**.
4. **Corriger `docs/roadmap.md`** : ligne 56, « 3 663 → 1 629 » (÷2,3 et 1,3 %
   inchangés) ; dater explicitement les tableaux 254-266 « en-tête de 39 octets à
   l'époque », comme le fait déjà le journal ligne 112.
5. **Dater `reports/rapport-transport-liste.md`** : en-tête de 39 octets (§1, §TCP
   ligne 197) et « cette build parle la 4 » (87-89) ne peuvent pas coexister ;
   ajouter l'avertissement de `docs/format-flux.md:145-148`, et corriger les
   chiffres pré-écarts restés lignes 100 et 230-231 (3 o/actif, 1 989).
6. **Corriger `reports/rapport-phase3-reparti.md:62-65`** : « 79 d'en-tête » (et
   non 20), « 3,01 octets par neurone actif en v2 » (et non 6), et « fait depuis »
   au lieu de « prochain chantier (3.2) ».
7. **Corriger `reports/rapport-compacite-trace.md`** : étiqueter la ligne 136
   comme **projection** et renvoyer à la mesure **45 079 930** ; marquer « fait »
   la liste « Ce qu'il reste à valider » (231-243) et le §8 (255-257).
8. **Trancher la règle R4** : soit ajouter le refus de `n == 0` dans
   `recevoir_flux` (et son test), soit corriger `docs/plan-prefill-reparti.md:76-78`
   et son bandeau `:9-10` ; dans les deux cas, remplacer `DRAVE_FLUX_POS` (266) par
   `DRAVE_DEBUG_FLUX` et préciser ce qu'il imprime réellement.
9. **Compléter le bandeau de `docs/plan-prefill-reparti.md`** : dire que l'en-tête
   est passé à **79 octets** (+40), sinon les tableaux §1.1 (39 octets, offsets),
   §1.4 et §5 restent faux de 40 octets malgré le bandeau « plan d'origine ».
10. **Corriger `docs/format-flux.md`** : ligne 20 (`version u16 = 2` par défaut,
   3 si `DRAVE_TRACE_BLOCS=1`), ajouter la disposition d'octets et la formule de
    taille de la **v3** (§Version 3), compléter la sémantique de `n` (modes 2 et 3)
    ligne 95, et renvoyer vers `docs/plan-mode4-lot-listes.md` ligne 117.
11. **Corriger `docs/vision.md`** : §4 liste 129-148 et §7 208-210 (« mesures à
    faire » déjà faites), tableau §8 ligne 222 (« rien » → transport TCP, lot,
    Colab), et le renvoi FPGA ligne 109 vers `../FPGA-Stratix-V/docs/`.
12. **Corriger les compteurs** : README:281, README:355, REPRISE:16 → **11 901**
    lignes ; REPRISE:35 → **13/13** ; rapport-session:4 vs :66 (trancher le nombre
    de commits, ou écrire « ~70 »).
13. **Corriger `README.md:345`** : la ligne gpt-oss est décalée d'une colonne
    (« blocs lus » en perplexité, 15,1757 en débit) ; remettre perplexité =
    15,1757 (ctx 256), débit = « blocs lus » ou la valeur réelle, mémoire = 60 Go.
14. **Ajouter au README un paragraphe d'état sur le chantier du jour** (protocole
    v4, DRVF v2/v3, transport et mode lot, `--options-actives`, clés KV f16,
    Colab) avec les renvois vers `REPRISE.md`, `docs/roadmap.md` et
    `docs/format-flux.md`.
15. **Finitions** : compléter `docs/colab-reparti.md:24` (les 14 champs
    transportés), citer `tools/colab_cote_local.sh`, lever l'ambiguïté de
    `REPRISE.md:446` (`gpu/` est sous `drave-core/`, pas sous `src/`), et
    actualiser `reports/rapport-drapeaux-ignores.md:196` (`--options-actives` fait,
    `--options-strict` non fait).

## Ce que cet audit n'a pas vérifié

* Les **performances et perplexités en vol** : la campagne `--ctx 4096 --limit 4096
  --lot 512` tournait pendant l'audit et aucune exécution longue n'était permise.
  Les seuls faits neufs mesurés ici sont la version écrite par défaut (v2), celle
  écrite sous `DRAVE_TRACE_BLOCS=1` (v3, avec perte) et le contenu du tableau de
  bord `--options-actives`.
* Les chiffres de débit du mode lot (18×, 7×, 2,6 s, 47,6 s) et les mesures KV à
  8 192 (25-28 min par passe) : ils sont recoupés entre documents, pas rejoués.
* Le contenu de `journal/` (consigne) et les documents `docs/comparaison-spiking.md`,
  `docs/plan-mla-vision.md`, `docs/programme-recherche.md`,
  `docs/convertisseur.md`, `Qtrinet-bootstrap.md` (survolés par `grep` seulement).
* Les deux plans apparus pendant l'audit (`docs/plan-mode4-lot-listes.md`,
  `docs/plan-gpu-topk.md`) : seuls leurs points d'ancrage au code ont été vérifiés,
  pas leurs projections.

## Résumé (10 lignes)

1. 66 affirmations revérifiées après les changements du 30/09 : 27 OK, 17 PÉRIMÉ,
   14 CONTRADICTOIRE, 8 MANQUANT.
2. Le défaut n°1 est le **cache KV** : « 75 %/50 % » (REPRISE, roadmap, rapport
   d'attribution) contre « 64 %/28 % » dans le rapport de la campagne complète et
   dans le tableau de REPRISE lui-même.
3. Le défaut n°2 est **R4** : le plan affirme que `n == 0` et le plafond de 256 Mo
   sont refusés ; seul le plafond est dans le code (`verifier_taille`), sans test
   du cas `n == 0`.
4. Le défaut n°3 est le **mélange des époques** de l'en-tête : « 39 octets +
   version 4 » est impossible depuis `d59d061` (v4 = 79 octets) ; cela contamine
   `rapport-transport-liste.md`, `REPRISE` §6bis, `roadmap:56` et `phase3:62`.
5. `docs/plan-prefill-reparti.md` reste globalement un plan d'époque : son bandeau
   dit v4 mais pas les 79 octets, et son diagnostic `DRAVE_FLUX_POS` n'existe pas.
6. `docs/format-flux.md` est à jour sur la v4 mais pas sur le disque : la v3 n'a ni
   disposition d'octets ni formule de taille, et la sémantique de `n` s'arrête au
   mode 1.
7. Les compteurs sont périmés (11 440 → 11 901 lignes) et REPRISE se contredit sur
   `cargo test` (11/11 contre « Treize tests » — le code en compte 13).
8. `README.md` ignore tout le chantier du jour et sa ligne gpt-oss est décalée
   d'une colonne ; `docs/vision.md` dit encore « rien » pour l'axe 3.
9. Aucun lien `[texte](chemin)` n'est mort ; les manques sont des renvois absents
   (`plan-mode4`, `colab_cote_local.sh`) et des documents silencieux
   (`contexte-long` sur les clés f16).
10. Priorité de correction : le chiffre KV, R4, puis les chiffres de transport
    datés — le reste est de la republication, pas de la mesure.
