# Cohérence des documents avec le code — audit
> **Relecture du 03/10 (bloc 20) : les trouvailles ci-dessous sont datées.** Ce
> rapport a été écrit sur un état ANCIEN du code ; plusieurs de ses points sont
> depuis corrigés, et les laisser tels quels ferait mentir un document durable.
> Vérifiés et annotés un par un (le reste n'a pas été re-vérifié) :
>
> - **n° 17** (le `n` de l'en-tête par mode) : **toujours manquant** dans
>   `docs/format-flux.md` → corrigé le 03/10 ;
> - **n° 20** (échappement 255 du mode blocs réseau) : **CORRIGÉ** — l'émetteur
>   écrit bien `&i.to_le_bytes()[..2]` (`encoder_paires_blocs`) et le récepteur en
>   lit deux : la désynchronisation annoncée n'existe plus ;
> - **n° 21** (réglages transportés) : **CORRIGÉ** — la doc liste les 14 champs
>   (`7 × top-k`, `attn`, `q·k`, `moe`) ;
> - **n° 22** (plafond R4) : **CORRIGÉ** — `PLAFOND_FLUX = 256 Mo` et
>   `verifier_taille` gardent chaque allocation pilotée par le réseau, y compris
>   les 12 octets de taille du mode 4 ;
> - **n° 24** (le mode 4 n'existe pas) : **CORRIGÉ** — le mode 4 (lot en listes)
>   existe, est émis par `envoyer_lot_listes` et couvert par
>   `tools/porte-flux.sh` ;
> - **n° 23** (règle R1 : un état seul doit partir en mode 0) : **à trancher** —
>   le pilote envoie un lot même d'un seul état (mode 3), ce que R1 déconseille ;
>   ce n'est pas une contradiction de format mais une recommandation non suivie.


**En une ligne** : **80 affirmations** vérifiées une par une contre le code (et
contre les traces réelles du disque) ; **38 sont fausses (PÉRIMÉ)**, **15 se
contredisent entre documents (CONTRADICTOIRE)**, **10 existent dans le code et
manquent aux documents (MANQUANT)**, **17 tiennent (OK)** — les trois plus graves
touchent la **version du protocole de flux** (deux binaires « v3 » aux contrats
différents se croient compatibles), un **échappement d'indice écrit sur 4 octets et
lu sur 2** en mode blocs, et `REPRISE.md` §6bis (pourtant écrit il y a une heure)
déjà faux sur quatre points.

## Révision auditée, méthode, réserves

| | |
|---|---|
| Commit de référence | `ae85043` (2026-09-30 12:30) |
| `drave-core/src/main.rs` | sha256 `d5e90136…` · 3 112 lignes |
| `drave-core/src/model.rs` | sha256 `3e5dde2d…` · 3 872 lignes |
| Traces relues | `/tmp/flux_v2.bin` (66 370 408 o, en-tête `DRVF` version **2**), `/tmp/flux_v3.bin` (version **3**) |

Deux réserves de méthode, parce qu'elles changent la portée des constats :

1. **L'arbre de travail a bougé pendant l'audit.** Quand il a commencé, HEAD était
   `a0687b9` avec 165 lignes de `model.rs` non commitées (trace v3) ; le commit
   `ae85043` (12:30) les a intégrées et a complété `docs/format-flux.md` en
   conséquence. Les constats ci-dessous décrivent l'état **après** ce commit, et
   les deux points qui étaient vrais avant lui (`flux_codec.py` refusait la v3 ; la
   v3 n'était documentée nulle part) sont notés comme résolus dans le tableau.
   À la publication, `model.rs` portait de nouveau 31 lignes non commitées
   (`DRAVE_KV_K_F16`, clés en f16) : cet ajout n'est pas audité ici, et la variable
   n'est encore documentée nulle part.
2. **Aucune exécution du moteur n'a été faite** : pas de `cargo build` (interdit),
   pas de `--flux-serveur` ni de `--ppl-reparti` (interdits). Les tailles d'en-tête
   et les formats viennent des constantes, des `assert_eq!` et des offsets de
   `recevoir_flux`, pas d'une capture réseau. Deux vérifications chiffrées ont été
   faites hors moteur : la taille et la version de `/tmp/flux_v2.bin` (lecture
   binaire), et les recalculs d'en-tête (79 = 39 + 40).

Le `journal/` n'a pas été lu, conformément à la consigne.

---

## 1. Version du protocole et du format

| # | document | affirmation | ce que dit le code / la mesure | verdict |
|---|---|---|---|---|
| 1 | `main.rs:1286-1295` (commentaire) | « Version 4 : le bloc de réglages transporte AUSSI les top-k » | `const VERSION_FLUX: u8 = 3;` (main.rs:1295) — l'en-tête transporte bien les top-k, mais **la version n'a pas été incrémentée** | CONTRADICTOIRE |
| 2 | `reports/rapport-drapeaux-ignores.md:7` + intitulé du commit `d59d061` | « le protocole de flux passe en version 4 » | la build écrit 3 dans chaque en-tête ; sa propre recommandation (§8.2 : « transporter … **et incrémenter `VERSION_FLUX`** ») n'est appliquée qu'à moitié | CONTRADICTOIRE |
| 3 | `docs/format-flux.md:63` vs `:68` | titre « protocole **v3** », puis « version u8 **4** » dans le même bloc | 3 — le document se contredit à cinq lignes d'intervalle | CONTRADICTOIRE |
| 4 | `docs/format-flux.md:109` | message d'erreur : « cette build parle la **4** » | le message réel dirait « cette build parle la **3** » (main.rs:1562) | PÉRIMÉ |
| 5 | `reports/rapport-transport-liste.md:87` | message d'erreur : « cette build parle la **2** » | 3 — le rapport a deux versions de retard | PÉRIMÉ |
| 6 | `docs/format-flux.md:1` et `:20` | titre « Le format de flux (**DRVF v1**) », en-tête « version u16 **= 1** » | `TraceFlux::nouveau` écrit **2** par défaut et **3** si `DRAVE_TRACE_BLOCS=1` (model.rs:549) ; `/tmp/flux_v2.bin` est bien version 2 | PÉRIMÉ |
| 7 | `REPRISE.md:262` | « Le protocole de flux est en **v2** … en-tête de **39 octets** » | v3 (constante) et en-tête de **79 octets** | PÉRIMÉ |
| 8 | `docs/roadmap.md:111` | « protocole de flux **v2** … en-tête de 39 octets » | v3 / 79 | PÉRIMÉ |
| 9 | `docs/plan-prefill-reparti.md:14,22,103` | « `VERSION_FLUX` vaut encore **2** », « la version change : 2 → 3 » | 3 (le plan décrit un travail déjà fait) | PÉRIMÉ |
| 10 | `docs/format-flux.md:64` | « Le lecteur lit **les deux versions** » | le lecteur lit **1, 2 et 3** (model.rs:691-693) — et le même document l'écrit correctement ligne 156 (« v1/v2/v3 lues ») : contradiction interne depuis l'ajout de la v3 | PÉRIMÉ |
| 11 | `docs/format-flux.md:137` (invariant « deux implémentations ») | Rust et Python lisent le même fichier | vrai **depuis `ae85043`** : `tools/flux_codec.py:62` lit 1, 2 et 3 ; avant ce commit, l'invariant ne tenait plus pour la v3 | OK |
| 12 | `docs/format-flux.md:141` et `docs/roadmap.md:55` | « 40 puis **199 flux** » à 40 et 200 jetons | depuis `2184fc5`, les flux envoyés valent N−1 (le dernier jeton est sauté) : **39** à 40 jetons, 199 à 200 | PÉRIMÉ |
| 13 | `REPRISE.md:251`, `docs/roadmap.md:116`, `reports/rapport-phase3-reparti.md:51` | « 1 024 jetons (**1 024 flux**) » | le même correctif `2184fc5` (11:41, **après** ces trois textes) donne **1 023 flux** ; le message du commit dit lui-même « 255 flux au lieu de 256 » à 256 jetons | PÉRIMÉ |

## 2. En-tête, champs, modes

| # | document | affirmation | ce que dit le code / la mesure | verdict |
|---|---|---|---|---|
| 14 | `docs/format-flux.md:66` | en-tête « **26 octets** » | `TAILLE_TETE = 79` : 26 (v1) + 13 (niveaux/seuil/top-k/renorm) + 40 (7 top-k de projection + attn + q·k + moe) | PÉRIMÉ |
| 15 | `reports/rapport-transport-liste.md:9,14,15,196` | en-tête « **39 octets** » | 79 (offsets vérifiés : topk_proj 39..66, attn 67, qk 71, moe 75) | PÉRIMÉ |
| 16 | `docs/plan-prefill-reparti.md:20,28,78,105,140` | en-tête « **39 octets** », tous les offsets ≤ 38 | 79, avec quatre champs de plus après l'offset 38 | PÉRIMÉ |
| 17 | `docs/format-flux.md:74` | « `n` : dimension (mode 0) ou **actifs (mode 1)** » | `n` = actifs aussi en mode 2, et **états** en mode 3 (`MODE_LOT`, main.rs:1307-1312) | MANQUANT |
| 18 | `docs/format-flux.md:86` | mode 2 = `n_blocs u32 · n_blocs × f32 · longueur u32 · paires` | conforme à l'émetteur (main.rs:1446-1466) et au récepteur (1591-1628) | OK |
| 19 | `docs/format-flux.md:87` | mode 3 = `n × dimension × f32`, `n` = états | conforme (`envoyer_lot`, main.rs:1512-1544) | OK |
| 20 | `docs/format-flux.md:30` | échappement 255 → « l'indice ABSOLU sur les **deux octets** suivants » | **faux pour le réseau** : `main.rs:1457` écrit `i.to_le_bytes()` = **4 octets**, alors que le récepteur `main.rs:1618` en lit **2** — toute trame contenant un écart ≥ 255 se désynchronise. Le disque, lui, est correct (model.rs:605,628 : 2 octets) | CONTRADICTOIRE |
| 21 | `docs/format-flux.md:76-83`, `docs/colab-reparti.md:24` | les réglages transportés = « niveaux, seuil, top-k, renorm » | le code transporte **en plus** `topk_proj[7]`, `attn_topk`, `qk_topk`, `moe_topk` (main.rs:1495-1498) : 14 champs au total | MANQUANT |
| 22 | `docs/plan-prefill-reparti.md:66-68` (règle R4) | refus de `n == 0` et de `n × hidden × 4 > 256 Mo` **avant** l'allocation | `recevoir_flux` fait `vec![0u8; n * hidden * 4]` (main.rs:1584) **sans aucun plafond** : un en-tête corrompu peut demander une allocation démesurée. Aucune constante `PLAFOND_LOT` dans le code | MANQUANT |
| 23 | `docs/plan-prefill-reparti.md:57-59` (règle R1) | « l'émetteur DOIT utiliser le mode 0 pour un jeton seul » | `run_ppl_reparti` envoie le dernier lot même s'il vaut 1 état, en mode 3 (main.rs:1826-1834) | CONTRADICTOIRE |
| 24 | `docs/format-flux.md:96`, `docs/plan-prefill-reparti.md:21` | « le lot en listes est le **mode 4**, pas encore écrit » | les modes du code sont 0, 1, 2, 3 ; aucun mode 4 n'existe ni n'est réservé dans `recevoir_flux` | MANQUANT |
| 25 | `docs/format-flux.md:124-131` | règle « qui applique la norme finale » (`flux_brut`) | `flux_brut` existe et le serveur le pose (main.rs:1695) | OK |
| 26 | `docs/colab-reparti.md:26`, `REPRISE.md:265` | `--flux-serveur` accepte `hôte:port` | `rsplit_once(':')` (main.rs:1659-1662) | OK |

## 3. Chiffres de transport et de trace

| # | document | affirmation | ce que dit le code / la mesure | verdict |
|---|---|---|---|---|
| 27 | `docs/format-flux.md:119`, `reports/rapport-transport-liste.md:14,24`, `REPRISE.md:273`, `docs/colab-reparti.md:36`, `docs/roadmap.md:56,243` | flux dense = **3 623 octets** (39 + 3 584) | avec `TAILLE_TETE = 79` : **3 663** (79 + 3 584) | PÉRIMÉ |
| 28 | `reports/rapport-phase3-reparti.md:61-62` | « **3 604 octets** (20 d'en-tête + 896 × 4) » | 20 octets était l'en-tête d'avant les réglages d'activation ; le même jour, `rapport-transport-liste.md` dit 3 623 et le code dit 3 663 | PÉRIMÉ |
| 29 | `docs/roadmap.md:292` | « aujourd'hui du f32 dense, **3 604** octets par flux » | contredit la ligne 243 du même document (3 623) et le code (3 663) | CONTRADICTOIRE |
| 30 | `REPRISE.md:274` | listes i16 seuil 0,01 : « **~2 300** » octets | aucun chiffre de ce type dans le rapport cité : 2 159 (listes i16, seuil 0,02, vrai texte), 1 568 (blocs + écarts, seuil 0,01) | PÉRIMÉ |
| 31 | `REPRISE.md:275` | échelles par bloc seuil 0,01 : **2 268** octets | 2 268 est la mesure **avant** les indices par écarts (`rapport-transport-liste.md:176) ; après écarts : **1 568** (ligne 177), résultat commité à 11:34 — REPRISE §6bis, écrit à 11:39, l'ignore | PÉRIMÉ |
| 32 | `docs/roadmap.md:56` | `--flux-blocs --act-thresh 0.01` : **3 623 → 1 589** (÷2,3) | 1 589 est la mesure à 1 024 jetons avec l'en-tête de 39 : avec 79, **1 629** ; l'écart 1,32e-2 reste | PÉRIMÉ |
| 33 | `docs/colab-reparti.md:36` | « **1 989** en listes à échelle par bloc (68 % d'activité) » | 1 989 = ancien format (indices u16, 3 o/actif, en-tête 39). Format actuel (écarts u8, 2 o/actif, en-tête 79) : **≈ 1 419** | PÉRIMÉ |
| 34 | `reports/rapport-transport-liste.md:3` | « en liste creuse (**871** octets au lieu de 3 623) » | son propre tableau donne **897** (listes i16, seuil 0,05) et 799 (blocs) ; 871 ne correspond à aucune ligne mesurée | CONTRADICTOIRE |
| 35 | `reports/rapport-transport-liste.md:25` | listes seuil 0,00 : **3 622** pour 100,0 % (896 actifs) | 39 + 4 × 896 = **3 623** ; l'octet manquant n'est pas expliqué | PÉRIMÉ |
| 36 | `docs/format-flux.md:94` | « 1 seul lot de **917 543 octets** » | 39 + 256 × 896 × 4 ; avec l'en-tête de 79 : **917 583** | PÉRIMÉ |
| 37 | `docs/format-flux.md:142` | « 1 lot de 256 : 0,00e0 (**918 ko** sur le fil) » | 917 583 o ≈ 918 ko (arrondi décimal) | OK |
| 38 | `docs/format-flux.md:45`, `reports/rapport-compacite-trace.md:5,92` | trace dense 512 j : 132 396 736 → **66 370 408** (−49,87 %) | `/tmp/flux_v2.bin` = exactement 66 370 408 octets, version 2 | OK |
| 39 | `reports/rapport-compacite-trace.md:79,126` | « écarts + i16 = **66 370 406** » | 66 370 408 avec la sentinelle de fin (2 o), 406 sans — l'écart est expliqué §2 du même rapport | OK (2 o) |
| 40 | `docs/format-flux.md:47`, `reports/rapport-compacite-trace.md:8` | 24 576 listes · 22 008 776 actifs | conforme au commit `6b3b53f` et au tableau du rapport ; non recompté ici (ré-encodage Python interrompu au-delà de 60 s) | OK (source) |
| 41 | `docs/roadmap.md:107` | trace 512 jetons = « **12 288 listes** · 132 Mo · 6 octets par neurone actif » | 24 576 listes pour 512 jetons × 24 couches × 2 points ; 12 288 = la valeur pour **256 jetons** | PÉRIMÉ |
| 42 | `docs/format-flux.md:34` | « 6,02 octets par neurone actif en v1, 3,01 en v2 » | vrai pour la trace **dense** ; la trace creuse coûte 6,04 en v1 et 3,04 en v2 (`rapport-compacite-trace.md:35,79`) | MANQUANT (précision) |
| 43 | `docs/format-flux.md:143` | « `--topk-q 900` contre `--topk-q 4` → 0,00e0 (vérifié) » | la vérification date d'**avant** `d59d061` : à l'époque les top-k n'étaient ni appliqués ni transportés dans les modes flux (`rapport-drapeaux-ignores.md:72`), donc l'égalité était tautologique. Jamais re-mesurée depuis | MANQUANT |
| 44 | `reports/rapport-compacite-trace.md:13-14` | « restent à faire : valeurs i8 (−60,9 %), échelles f16 (−63,5 %), zstd (−79 %) » | i8 + échelles f16 par bloc sont **faits et commités** (`ae85043` : trace dense 45 079 930 o, −65,9 % depuis la v1, rejeu 19,4029) ; seul zstd reste. Le rapport n'a pas été mis à jour | PÉRIMÉ |

## 4. Autres chiffres (perplexités, densité, tailles)

| # | document | affirmation | ce que dit le code / la mesure | verdict |
|---|---|---|---|---|
| 45 | `README.md:34` | « Croisement push/pull à **10 %** de densité ✅ mesuré » | `reports/rapport-croisement-push-pull.md:43` : « **~22 %** … pas à 10 » ; le README lui-même le dit ligne 389 | CONTRADICTOIRE |
| 46 | `docs/vision.md:46,133,198` et `docs/histoire.md:12` | croisement « mesuré » à **10 %** | 22 % (rapport de référence + REPRISE §5.1 + `docs/convertisseur.md:225`) | CONTRADICTOIRE |
| 47 | `README.md:280` | « le moteur tient en **386 lignes** » | 11 440 lignes aujourd'hui (main.rs 3 112, model.rs 3 872) ; 386 était l'état initial (`rapport-optimisations.md:3`) | PÉRIMÉ |
| 48 | `README.md:354` | « **2 319 lignes** de Rust » | idem : chiffre de `rapport-inference.md:3`, dépassé (11 440) | PÉRIMÉ |
| 49 | `REPRISE.md:16` | « ~**5 000** lignes » | 11 440 lignes de `.rs` (dont 6 984 pour main+model) | PÉRIMÉ |
| 50 | `docs/contexte-long.md:103` | E5 attention creuse « **à faire** » | le même document donne les résultats §6 (234,88 contre 298,56) et `REPRISE.md:152` la classe « fait pour E4/E5 » | CONTRADICTOIRE |
| 51 | `docs/contexte-long.md:103` | KV int4 « mesuré : **+384 %** — llama.cpp : +411 % » | +384 % est l'ancienne mesure à 512 jetons à échelle unique ; la mesure de référence à 8 192 est **+364 %** contre +494 % (même document, lignes 144 et 160) | PÉRIMÉ |
| 52 | `REPRISE.md:53` | Qwen 6 bits : « **19,3045** ← bat l'int8 » | aucune source dans `reports/` : ni 19,3045 ni `--bits-attn 6` n'y figurent ; REPRISE §5.2 ne cite que « 19,30 » | MANQUANT |
| 53 | `README.md:388` | perplexité WikiText-2 : 24,90 contre 25,00 numpy | `rapport-inference.md:66,251` : 24,90 contre 25,0004 | OK |
| 54 | `README.md:397` | Q4_0 : +9,1 % contre Q8_0 | 21,0116 contre 19,2647 = +9,07 % (`rapport-mur-memoire-4bits.md:143-145`) | OK |
| 55 | `README.md:344` | gpt-oss-120b : perplexité « **—** » | 15,1757 (REPRISE §2) et 20,8361 à 63 jetons : le chiffre existe | MANQUANT |
| 56 | `docs/format-flux.md:138` | rejeu par lots : **17,4294** | cohérent avec les mesures de rejeu ; la valeur 18,0851 du mode lot est, elle, employée dans `REPRISE.md` sans source de rapport (le rapport de la phase 3.4 n'a jamais été écrit) | OK |

## 5. Statuts et affirmations « vérifié »

| # | document | affirmation | ce que dit le code / la mesure | verdict |
|---|---|---|---|---|
| 57 | `REPRISE.md:298-300` (§6bis, chantier 1) | « Préremplissage par LOTS sur le fil : le vrai bloqueur » | fait et mesuré au commit `cda3162` (12:02), **23 minutes après** l'écriture de §6bis | PÉRIMÉ |
| 58 | `REPRISE.md:304-306` (§6bis, chantier 3) | « l'écart **croît** avec la longueur : chercher pourquoi » | le commit `976cb81` et `rapport-transport-liste.md:141-152` : il **décroît** (1,37e-1 à 64 → 1,32e-2 à 1 024) | PÉRIMÉ |
| 59 | `docs/colab-reparti.md:28,32` | « préremplissage par lots sur le fil : ❌ un flux par jeton aujourd'hui », « le chantier suivant » | `MODE_LOT`, `envoyer_lot`, `--lot T` sont dans le code, et le document a été retouché à 12:20, **18 minutes après** la phase 3.4 | PÉRIMÉ |
| 60 | `reports/rapport-phase3-reparti.md:61-64` | « c'est le prochain chantier (3.2) : faire voyager la LISTE » | fait : `--flux-liste`, `--flux-blocs`, 3 623 → 1 568 octets (`cb37c83`, `af18f29`) | PÉRIMÉ |
| 61 | `docs/colab-reparti.md:103` | « `--flux-blocs --act-thresh 0.02` (÷2 sur le fil pour **0,2 %**) » | le rapport que ce document cite réfute explicitement cette formulation (`rapport-transport-liste.md:162-164`) ; la configuration recommandée est 0,01, pour 1,3 % à 1 024 jetons | CONTRADICTOIRE |
| 62 | `docs/vision.md:120` et `:216` | axe 3 (plusieurs machines) : « **Rien n'existe ici** », état « rien » | transport TCP, découpage fidèle 0,00e0, mode lot et recette Colab : la phase 3 existe | PÉRIMÉ |
| 63 | `docs/roadmap.md:55,57,59` | 3.1 ✅ 0,00e0 sur « 40 et 199 flux », 3.3 🔬, 3.5 ✅ | 3.1/3.3/3.5 sont faits et mesurés (le tableau de la même page dit 3.2 🔬) ; « 40 » flux est faux (39) | PÉRIMÉ |
| 64 | `docs/roadmap.md:293` | « Ce qui reste : le transport lui-même (3.2), la granularité, le seuil de rentabilité et la version du format » | les quatre sont livrés (tableaux 55-59 du même document) : la conclusion contredit l'état affiché plus haut | CONTRADICTOIRE |
| 65 | `docs/plan-prefill-reparti.md:346` | renvoi vers `reports/rapport-prefill-reparti.md` | ce fichier **n'existe pas** (le rapport existant s'appelle `rapport-prefill-par-lots.md`, et porte sur le préremplissage **local**) : le rapport de la phase 3.4 n'a jamais été écrit | PÉRIMÉ |
| 66 | `docs/plan-prefill-reparti.md:8,103` | « numéros de ligne du commit `2184fc5` » : `VERSION_FLUX` 1231, `TAILLE_TETE` 1251 | 1295 et 1323 dans l'arbre actuel — le plan est une pièce datée, mais rien ne le signale | PÉRIMÉ |

## 6. Drapeaux, variables, renvois et phrases cassées

| # | document | affirmation | ce que dit le code / la mesure | verdict |
|---|---|---|---|---|
| 67 | `docs/vision.md:69` | `--profil-experts` « quels experts sont choisis (MoE) » | ce drapeau **n'existe pas** ; seuls `--profil-neurones` et `--neurones-sortie` existent | PÉRIMÉ |
| 68 | `docs/plan-prefill-reparti.md:256` | `DRAVE_FLUX_POS=1` imprime `[flux] lot pos …` | variable absente du code | PÉRIMÉ |
| 69 | `model.rs:526,549` | `DRAVE_TRACE_BLOCS` (trace v3) | documentée depuis `ae85043` dans `docs/format-flux.md:49` (tableau v2/v3 et invariant ligne 156) — encore absente de `REPRISE.md` et du README, mais le document de format est le bon endroit | OK |
| 70 | `model.rs` | `DRAVE_BANC_KV_UNIT`, `_V1`, `_GRAD`, `_KUNIT`, `_DEBUG` | le `rapport-drapeaux-ignores.md:113` en cite sept (`_K0`, `_UNIT`, `_GRAD`, `_KUNIT`, `_GPU_SEUL`, `_DEBUG`) mais en omet, et aucune n'est décrite dans un document de référence | MANQUANT |
| 71 | `README.md:29-30` | renvois `reports/rapport-pe-evenementiel.md` et `reports/rapport-lecteur-ddr3.md` (état ✅) | **ces fichiers n'existent pas dans le dépôt** ; ils sont dans `../FPGA-Stratix-V/docs/` — le chemin est faux, pas le contenu | PÉRIMÉ |
| 72 | `REPRISE.md:323` | carte du dépôt : `gpu/drave_gpu.cu + .ptx` | les noyaux sont dans `drave-core/gpu/drave_gpu.{cu,ptx}` (chargés par `include_str!("../gpu/drave_gpu.ptx")`) | PÉRIMÉ |
| 73 | `README.md:3` | « *Anciennement `Drave`.* » | le projet s'appelait **Qtrinet** (`docs/histoire.md:11-16`) ; le renommage automatique du 30/09 a remplacé le mot dans sa propre phrase d'origine | CONTRADICTOIRE |
| 74 | `README.md:12` | « Le nom du crate et du binaire … **changera dans un commit dédié** » | le commit dédié est `b97d129` (30/09 08:48) ; `docs/vision.md:229` dit « Le renommage est fait … partout » | CONTRADICTOIRE |
| 75 | `docs/vision.md:14` | « Le projet s'appelait `Drave`, du nom de son origine » | même cassure : c'était `Qtrinet` (`docs/histoire.md`) | CONTRADICTOIRE |
| 76 | `rapport-drapeaux-ignores.md:43,57-61,66` | défauts d'audit : `--keep` en `--ppl`, `--ffn-gain` en `--infer`, `--threads`/`--q4` en FS/PR, `i += 2` du mode par défaut | tous corrigés : `opt.keep` en FS/PR (main.rs:1668,1768), `keep` en P (2803), `ffn_gain` en I (606), `fils(&opt)` (1668,1768), pas de 2 sélectif (80-91) | OK |
| 77 | `REPRISE.md:229-238` (table `DRAVE_*`) | `DRAVE_GPU_TETE`, `DRAVE_GPU_KV`, `DRAVE_KV_*`, `DRAVE_YARN*` | toutes présentes dans le code, et le piège « sans `DRAVE_GPU` rien ne s'exécute » est réel | OK |
| 78 | `docs/format-flux.md:139` | `DRAVE_FLUX_VERIF=1` chiffre la fidélité | présente (model.rs), mais muette dès `--lot > 1` (`rapport-drapeaux-ignores.md:109`) — le document ne le dit pas | MANQUANT |
| 79 | `docs/roadmap.md:18` | `tools/profil_flux.py` | présent dans `tools/` | OK |
| 80 | `reports/bilan-multi-materiel.md:149,152` | `tools/pack_lists.py`, `tools/quartus_env.sh` | présents dans `../FPGA-Stratix-V/tools/`, après le `cd ../FPGA-Stratix-V` du même bloc : chemins valides | OK |

---

## Les 10 corrections à faire, dans l'ordre

1. **Incrémenter `VERSION_FLUX` à 4** (`main.rs:1295`), ou supprimer le commentaire
   « Version 4 » : aujourd'hui deux binaires parlant « 3 » peuvent transporter des
   contrats d'activation **différents** (l'un sans les top-k, l'autre avec) et se
   croient compatibles — le silence exact que la phase 3.5 et le
   `rapport-drapeaux-ignores.md` §8.2 voulaient empêcher.
2. **Corriger l'échappement d'indice du mode blocs réseau** (`main.rs:1457` :
   écrire `&i.to_le_bytes()[..2]` comme le fait le disque en `model.rs:605`) : le
   récepteur en lit deux octets, l'émetteur en écrit quatre ; toute trame avec un
   écart ≥ 255 se désynchronise, et c'est un cas que la doc dit possible.
3. **Réécrire la section transport de `docs/format-flux.md`** avec les valeurs du
   code : version unique (3, ou 4 après la correction 1), en-tête **79 octets**,
   dense **3 663**, lot de 256 **917 583**, réglages transportés au complet
   (14 champs), et retirer la mention du mode 4.
4. **Mettre `REPRISE.md` §6bis à jour** (il a vingt minutes de retard sur quatre
   points) : protocole v3/79 octets, 1 023 flux à 1 024 jetons, indices par écarts
   (1 568 et non 2 268), préremplissage par lots **fait**, et l'écart qui **décroît**
   avec la longueur (retirer le chantier 3).
5. **Mettre `docs/colab-reparti.md` à jour** : passer le préremplissage par lots de
   ❌ à ✅ (mode 3, `--lot T`, écart 0,00e0), corriger 3 623 → 3 663 et 1 989 → ≈ 1 419,
   et supprimer « ÷2 pour 0,2 % » que le rapport cité réfute.
6. **Écrire le rapport manquant de la phase 3.4** (`reports/rapport-prefill-reparti.md`),
   ou corriger le renvoi de `docs/plan-prefill-reparti.md:346` et y consigner les
   mesures : 4 lots de 64 → 0,00e0 (18,0851 = 18,0851), 1 lot → 0,00e0, 917 583
   octets avec l'en-tête actuel ; c'est aujourd'hui le seul chantier livré **sans
   rapport**, alors que la règle du dépôt est que chaque chiffre a sa source.
7. **Corriger le README** : « Anciennement `Drave` » → `Qtrinet` (ligne 3), retirer
   « changera dans un commit dédié » (ligne 12), 10 % → ~22 % (ligne 34), pointer
   les deux rapports FPGA vers `../FPGA-Stratix-V/docs/` (lignes 29-30), et rafraîchir
   les comptes de lignes (386 / 2 319 → 11 440).
8. **Corriger `docs/vision.md` et `docs/histoire.md`** : 10 % → ~22 % (vision 46,
   133, 198 ; histoire 12), « Rien n'existe ici »/« rien » de l'axe 3 (vision 120,
   216) → transport TCP, mode lot et recette Colab, phrase « s'appelait `Drave` »
   (vision 14) → `Qtrinet`, et remplacer `--profil-experts` (vision 69) par les
   drapeaux réels.
9. **Corriger `docs/roadmap.md`** : « 12 288 listes » → 24 576 (ligne 107), l'en-tête
   de 39 octets (111), les 3 604 octets (292) et la conclusion « ce qui reste »
   (293) ; remonter les statuts 3.2/3.3/3.5 de 🔬/✅ à leur état réel et y ajouter
   la ligne de la phase 3.4 avec le mode lot.
10. **Documenter les variables qui restent dans l'ombre** : `DRAVE_BANC_KV_UNIT`,
    `_V1`, `_GRAD`, `_KUNIT`, `_DEBUG` ne sont décrites nulle part,
    `DRAVE_FLUX_VERIF` est muet en mode lot (`rapport-drapeaux-ignores.md` §5), et
    le `--options-actives`/`--options-strict` recommandé par le §8 n'existe toujours
    pas. La trace v3 est désormais documentée (`docs/format-flux.md`) et lisible par
    `tools/flux_codec.py` depuis `ae85043`, mais `REPRISE.md` et le README ignorent
    encore la variable `DRAVE_TRACE_BLOCS` et le fait que la v3 existe.

## Ce que cet audit n'a pas vérifié

* Les performances et les perplexités « en vol » : aucune exécution du moteur n'a été
  autorisée ici, donc les chiffres **recalculables** (3 663, 917 583, 1 419, 1 023)
  sont des **conséquences arithmétiques** du code, pas des mesures neuves ; ils
  invalident les chiffres publiés, mais la valeur mesurée reste à produire par
  l'agent qui corrigera les documents. Les chiffres de la v3 (45 079 930 o,
  19,4029, −65,9 %) viennent du commit `ae85043` et de `docs/format-flux.md`, pas
  d'un recomptage indépendant.
* Le contenu de `journal/` (ignoré par consigne) et les documents
  `docs/comparaison-spiking.md`, `docs/plan-mla-vision.md`,
  `docs/programme-recherche.md`, `docs/convertisseur.md` (survolés par grep
  seulement) ; `convertisseur.md:225` est du bon côté du croisement (22 %).
* La qualité des réponses du mode vision, qui n'a pas de référence locale
  (réserve déjà écrite dans `REPRISE.md` §6).

## Récapitulatif

| verdict | nombre | principaux foyers |
|---|---:|---|
| PÉRIMÉ | **38** | version du format de flux et du disque (7) · nombre de flux à 40 et 1 024 jetons (2) · en-têtes 26 et 39 octets (3) · octets par flux, par lot et par neurone actif (8) · 12 288 listes · KV int4 +384 % · comptes de lignes 386/2 319 (3) · statuts de `REPRISE.md` §6bis et de `colab-reparti.md` (8) · drapeaux et renvois inexistants (4) · rapport de compacité non mis à jour après `ae85043` |
| CONTRADICTOIRE | **15** | code « Version 4 » contre `VERSION_FLUX = 3` (3) · échappement écrit sur 4 octets / lu sur 2 · règles R1/R4 du plan contre le code (2) · 3 604 contre 3 623 dans `roadmap.md` · 871 contre 897 · **10 % contre 22 %** (README, vision, histoire) · E5 « à faire » contre mesuré · « ÷2 pour 0,2 % » · conclusion de roadmap · trois phrases cassées par le renommage |
| MANQUANT | **10** | 10 champs de réglages en plus des 4 documentés · plafond R4 du lot · mode 4 · précision 6,02/6,04 · « vérifié » des top-k jamais re-mesuré · 19,3045 sans source · gpt-oss « — » · `DRAVE_BANC_KV_*`, `DRAVE_FLUX_VERIF` muet en lot |
| OK | **17** | formats des modes 2 et 3 · `flux_brut` · `hôte:port` · trace dense 66 370 408 o (fichier réellement relu) · 66 370 406 hors sentinelle · 24 576 listes / 22 008 776 actifs (source) · 918 ko · 24,90 / 25,00 · +9,1 % · rejeu 17,4294 · corrections de l'audit drapeaux · table `DRAVE_*` de REPRISE · `profil_flux.py` · outils FPGA · `flux_codec.py` lit la v3 · `DRAVE_TRACE_BLOCS` documentée |
| **total** | **80** | |


