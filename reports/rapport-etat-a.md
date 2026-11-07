# État du chantier A — le moteur : deux bloqués réels, un faux bloqué, une frontière à requalifier

> **Ligne de roadmap** : **A** (le moteur) · **Date** : 2026-11-06, 21 h 51 HNE · **Branche** : `s/v7` ·
> **HEAD** : `7a876f70` (le HEAD a bougé pendant l'audit : `d31aa9a2` → `7a876f70`) ·
> **Mission** : lecture seule, aucun code, aucun fichier existant modifié ; deux fichiers neufs.
>
> **Verdict** : ⚠️ **l'état A est sain, le récit A est en retard.** Les lignes fermées le sont
> réellement ; **A8.3a est fait pour 3 portes sur 19** (et non « fait » tout court) ; **A2.6 est
> partiel mais libre** — sa tête est **décidée** (refusée), ses experts ne sont **pas** bloqués par
> l'absence d'un MoE : un **Qwen3-30B-A3B Q4 de 18 Go est présent et tourne**. Les **deux seuls
> bloqués réels** de A sont **A3.4** (compte Colab) et **A5.4** (carte Stratix V). **A6.2 est
> mal classé** : aucune ressource ne manque (le MoE local existe) ; c'est une tâche de code/mesure,
> pas un bloqué. **A23 a raison sur l'effet** (A2.6 ne doit pas être la
> tête de frontière) **mais tort sur la cause** (les experts ne sont pas bloqués par A6.2).
>
> **Dispositif** : lecture de `docs/pilotage/roadmap.md`, `en-cours.md`, `backlog/index.md`,
> `backlog/dependances.md`, des fiches `backlog/A*.md` et des `reports/rapport-a*.md` ; **rejeux
> ciblés** : `cargo test placement`, `DRAVE_PERTE_MAX=1 bash tools/porte-flux.sh`,
> `python3 -m tools.pensee.autotest`, `python3 tools/tests/linguistique/evaluer_gold.py`,
> `bash tools/porte-produit.sh`, `bash tools/porte-bloc-linguistique.sh`,
> `python3 tools/verifie_backlog.py`. **Pas de nouvelle mesure** au-delà de ces rejeux.

## 1. Ce que j'ai rejoué (et ce que ça donne)

| commande | résultat | ce qu'elle prouve |
|---|---|---|
| `CARGO_TARGET_DIR=/tmp/etat-a-target cargo test --manifest-path drave-core/Cargo.toml placement` | **8/8**, exit 0 | la règle `choisir` / `choisir_avec_perte` / `kv_precision` est testée — **8 tests, pas 4** |
| `DRAVE_PERTE_MAX=1 bash tools/porte-flux.sh` | **exit 0**, modes 0–4, réf. **58.3200 / 62.7357** | A8.3a tient sur `porte-flux` : le régime 1 % est bien épinglé |
| `python3 -m tools.pensee.autotest` | **183/183**, exit 0 | l'état B13 est à jour |
| `python3 tools/tests/linguistique/evaluer_gold.py --json /tmp/etat-a-gold.json` | **exit 0** ; POS **0,85** ; F1 **0,6482** ; exact **235/236** ; couverture **0,9874** | l'état courant dépassé A17 (222/239) ; **3 spans** restants |
| `bash tools/porte-produit.sh` | **exit 0**, 10 tests, 183/183 | le produit est vert |
| `bash tools/porte-bloc-linguistique.sh` | **exit 0**, 10 verdicts vrais | le bloc linguistique est vert (le négatif de A23 est périmé) |
| `python3 tools/verifie_backlog.py` | **exit 0**, frontière **(3) : A2.6, N2, N4** | le graphe est cohérent — mais il ne voit pas le blocage des experts |

**Ce que je n'ai pas rejoué** : les trois portes de A8.3a (`pont`, `coupe`), les mesures de lot
(`LOT=1/4`), la porte du MoE (`porte-echange-experts`) et le harnais A17 (non committé). Les
chiffres correspondants sont lus dans les fiches, pas reproduits ici.

## 2. L'inventaire A — les huit chantiers

| # | état réel | dépendance | chiffre publié | commande de vérification |
|---|---|---|---|---|
| **A1** observation, trace, diff, profilage | ✅ fait | aucune | trace v3 **45,1 Mo** contre 66,4 (+0,074 % PPL) ; densité **20–56 %** ; top 10 % → **33,1 %** de la magnitude ; **0,08 %** de neurones chauds ; PPL **28,4015** identique push/dense, dense **2 %** plus rapide (9,2 vs 9,4 s) | `bash tools/porte-trace.sh` ; `bash tools/porte-diff-couche.sh` |
| **A2** placement machine, KV, top-k, ordonnanceur | ✅ / ⚠️ **A2.6 partiel** | A1 | KV ×**1,93** préremplissage / ×**5,8** attention à 8 k ; KV paginé 968 → **13,2 ms** ; attention 22,16 → **3,29 ms/jeton** ; projections 15,6 → **6,2 ms** ; top-k **9,7e-7** à 1 M | `bash tools/porte-flux.sh` ; `bash tools/porte-topologie.sh` ; A2.6 : `cargo test placement` |
| **A3** répartition, protocole v5, granularité, seuil | ✅ / 🧱 **A3.4 bloqué** | A2 | en-tête **79 octets** ; écart local/réparti **0,00e0** ; **1 608 octets/flux** ; lot en listes 1,5 vs 3,5 ko/jeton (÷**2,3**) ; attente **1,01× / 1,99× / 4,89×** à 0/5/20 ms | `bash tools/porte-flux.sh` ; `bash tools/porte-topologie.sh` |
| **A4** rejouer, comparer | ✅ fait | A1, A2 | Qwen ctx 256 = **19,3885** ; gpt-oss = **15,6017** ; MLA **5,2e-7** contre numpy, **0,999024** contre llama.cpp ; divergence KV 8 bits : couche 1, jeton 1, 857 neurones, **9,3e-5** | `bash tools/porte-diff-couche.sh` ; `bash tools/porte-harnais-invariants.sh` |
| **A5** formats, matériels, énergie | ✅ / 🧱 **A5.4 bloqué** | A1, A2 | int8 +**3,0 %** à 8 192 ; clés f16 +**0,018 %** pour 39 % de taille ; int4 +**364 %** ; par couche **+2,28 % / +0,03 % / +2,7 %** | fiches `rapport-kv-par-couche.md` et `rapport-placement-bits-kv.md` ; pas de porte KV unitaire |
| **A6** apprendre des flux | ✅ / ⏳ **A6.2 mal classé** | A1, A2 | hebbien +**3,0 %**, produits **+0,0045** de R² ; **0 neurone mort** sur 116 736 ; 63 % < 0,1 % ; top 10 % → **19 %** de la masse | `bash tools/porte-echange-experts.sh` ; `bash tools/porte-occupation-elagage.sh` |
| **A7** grappe déportée | ✅ fait | A3, A4 | greffe **648 s** ; **1 608 octets/flux** ; **0,25 Mbit/s** ; top-1024 rend **30,7286** ; format v2 **4,22×** moins cher ; transport sparse **4,44×**, fidélité 100 %, **0,125 ms** loopback | `bash tools/porte-greffe.sh` ; `bash tools/porte-topologie.sh` |
| **A8** ordonnanceur place **et** perte | ✅ **opt-in** | A2.6, A8.0 | **19 portes PPL épinglées** (audit A8.0), **3** avec régime 1 % dual ; le défaut déplace de **−5,9 % à +19,5 %** ; A8.3a : **58,3200 / 62,7357**, **111,8003 / 115,6406**, variance **8,9 → 2,4 %** ; lot **1,90 %** ; threads 1/8 : mêmes chiffres | `DRAVE_PERTE_MAX=1 bash tools/porte-flux.sh` ; `LOT=1/4` ; `THREADS=1/8` |

**Lecture.** A1–A7 sont des lignes **fermées** (ou bloquées par une ressource) ; A8 est **décidé
opt-in**, pas ouvert. Le seul travail A réellement neuf est **A8.3b2** (instrumenter le chemin lot),
nommé par la fiche A8.3b et absent du graphe.

## 3. Les lignes ouvertes, une par une

| ligne | état réel | dépendance | chiffre publié | commande | ce qui est vraiment fait |
|---|---|---|---|---|---|
| **A2.6** | **partiel, libre (P2)** | A2 acquis ; **pas** A6.2 pour les experts ; tête décidée | KV ×1,93/×5,8 ; lot **503/502 Mio**, **24,0 → 30,5 tok/s** (+27 %), PPL **15,8452 → 15,8443** (−0,006 %) ; tête **+10 % PPL** (constante, pas de run courant) | `cargo test placement` (8/8) ; `bash tools/mesure_lot_disque.sh models/Qwen2.5-0.5B-Q8_0.gguf <ids>` | règle générique + KV **faits** ; tête **refusée par décision** ; experts **non mesurés** mais **mesurables** sur le MoE local |
| **A3.2** | mesurée | A3 | **1 608 octets/flux** à 256 jetons ; **1,5 vs 3,5 ko** (÷2,3) | `bash tools/porte-flux.sh` (modes 2/4) | listes i16, échelles par bloc, indices par écarts, rejouées |
| **A3.3** | mesurée | A3.2 | attente ≈ calcul distant + **3,2 × latence** ; **1,01 / 1,99 / 4,89** ; débit **0,25 Mbit/s** | `bash tools/porte-topologie.sh` | le seuil est un chiffre, pas une intuition |
| **A3.4** | **bloquée** | A3 | — | aucune (compte Colab) | préremplissage réparti fait et fidèle ; runtime absent |
| **A5.4** | **bloquée** | A5 | — | aucune (carte Stratix V) | PE et lecteur DDR3 vérifiés ; carte absente |
| **A6.2** | **« bloquée » — faux** | A6 | aucun chiffre A6.2 ; MoE local : PPL **37,2013** (C9), **19,143 / 19,172** (A8.3c) ; chargement **2,69 Go / 26,95 s** | `bash tools/porte-echange-experts.sh` (défaut : `$HOME/IA/modeles/qwen3-30b-a3b-Q4_K_M.gguf`, présent) | le **MoE existe** (18 Go, 48 couches, 128 experts, 8 utilisés) ; `DRAVE_TRACE_EXPERTS` + `DRAVE_ROUTAGE_FORCER` ; le blocage « 16 Go » est une **résidence mono-GPU**, pas une absence de modèle |
| **A8.0** | mesurée | A8 | **19 / 33** portes épinglées ; 3 comparatifs, 2 rouges qualifiées, 1 verte sans PPL, 8 sans PPL | `bash tools/porte-flux.sh` ; `bash tools/porte-pont.sh` ; `bash tools/porte-topologie.sh` | les pins existent ; **3 seulement** ont un régime 1 % |
| **A8.3** | mesurée **négative** | A8.0 | défaut **−5,9 % … +19,5 %** ; trois régimes reproductibles | `DRAVE_PERTE_MAX=0.001/1/10 bash tools/porte-flux.sh` | le défaut est **refusé** ; la règle reste opt-in |
| **A8.3a** | **fait 3/19** | A8.0 | flux **58,3200 / 62,7357** ; pont **111,8003 / 115,6406** ; coupe variance **8,9 → 2,4 %** | `DRAVE_PERTE_MAX=1 bash tools/porte-flux.sh` (rejoué **exit 0**) | les **3 portes clés** ont un régime 1 % ; les **16 autres pins** n'en ont pas |
| **A8.3b** | décidé | A8.3a | **61,9920 / 60,8135** (f32) ; **58,3200 / 62,7357** (1 %) ; bascule lot 1 vs ≥2 | `LOT=1` / `LOT=4 bash tools/porte-flux.sh` | le signe bascule avec le **chemin lot**, pas la taille |
| **A8.3c** | expliqué | A8.3b | lot **1,90 %** à lui seul ; effet KV **−5,9 %** (jeton) / **+3,2 %** (lot) | `LOT=1/4` | la « non-monotonie » était **deux chemins** |
| **A8.3d** | expliqué | A8.3c | **1,90 %** à **1** et **8** threads | `THREADS=1/8 LOT=1/4` | ce n'est pas le pool, c'est le **noyau par lots** |
| **A8.3b2** | **à faire — libre** | A8.3b | — | `LOT=1/4 bash tools/porte-flux.sh` + instrumentation | **nommé par la fiche A8.3b, absent du graphe** |

## 4. Vérification des six objets demandés

### A2.6 — partiel, mais pas « bloqué par A6.2 »

- **Fait** : `placement.rs` (règle `choisir`, `choisir_avec_perte`, `kv_precision`), **8 tests verts** ;
  le KV l'applique ; ×1,93 / ×5,8 à 8 k ; le lot disque est mesuré (503/502 Mio, +27 % tok/s,
  −0,006 % PPL).
- **Tête** : **refusée** — `TETE_4BIT` porte `perte_ppl = 10,0` et le test vérifie qu'elle n'est pas
  choisie à 5 %. **Ce n'est pas une mesure courante** : le JSON dit « pas de chiffre courant » ; la
  fiche dit à la fois « tête essayée (refusée) » (étape 2 ✅) et « tête : une place qui ne coûte pas
  la PPL » (étape 4 ⏳). **Contradiction de fiche** à corriger.
- **Experts** : **pas mesurés**, mais **pas bloqués par A6.2** : le MoE local existe (18 Go) et le
  moteur sait capturer/imposer le routage. Ce qui manque est le **code de placement des experts**
  (cache/VRAM/RAM), pas la brique d'entrée.
- **Chiffre à corriger** : la fiche et le JSON disent **4 tests** ; `placement.rs` en a **8**
  (les 4 de `choisir` + 4 autres), tous verts au HEAD.

### A6.2 — le faux bloqué

- La fiche dit « aucun MoE local ne tient dans 16 Go de VRAM ». **Faux au sens littéral** :
  `modeles/gguf/Qwen3-30B-A3B-Instruct-2507-Q4_K_M.gguf` (18 Go) est présent ; la machine a
  **2 × 16 Go de VRAM** et **125 Go de RAM** ; `rapport-chargement-paresseux.md` le charge en
  **7,36 s** (2,69 Go de listes) ; `rapport-c9-echange-experts.md` le fait tourner (48 couches,
  128 experts, 8 utilisés) ; `porte-echange-experts.sh` le prend par défaut.
- **Le vrai bloqueur** : un MoE de 18 Go ne **réside pas** dans **une** GPU de 16 Go ; le moteur
  l'exécute en offload/CPU. Ce n'est pas « pas de MoE », c'est « pas de résidence mono-GPU ».
- **Conséquence** : A6.2 n'est pas bloqué par une ressource ; c'est une **tâche de code/mesure**
  (routage appris, qualité égale, coût ÷10) sur un MoE présent. Il doit sortir de la liste des
  bloqués.

### A8.3a — fait pour 3 portes, pas pour 19

- `porte-flux` **rejoué** en 1 % : **exit 0**, modes 0–4, réf. **58,3200 / 62,7357**.
- `porte-pont` : **111,8003 / 115,6406** ; falaise 448 fibres **+2,81 → +5,88 %**.
- `porte-coupe` : variance **8,9 → 2,4 %** ; coûts **0,52–17,09 % → 5,88–11,56 %**.
- **Mais** : A8.0 a **19 pins**, A8.3b n'en donne que **3** en dual. Le **défaut** exigerait
  **19/19** ; il reste **refusé**. Le JSON `a83a-flux.json` dit encore « pont/coupe restent » :
  **périmé** par rapport aux trois fiches `a83a-*.md`.
- **Chiffre à corriger** : la roadmap A8 dit « 6 portes épinglées » (l. 152) ; A8.0 en compte **19**
  (l. 19 de `rapport-a80-audit-final.md`). Trois comptes coexistent : 6, 18, 19.

### A17 — un diagnostic historique, pas une ligne ouverte

- `rapport-spans-v7.md` (2026-11-05) : **222/239 = 0,9289**, **17 spans** ; le harnais
  (`/tmp/spans/sim3.py`) **n'est pas committé** — le chiffre n'est pas reproductible depuis le dépôt.
- **État courant** (rejoué) : POS **0,85**, F1 **0,6482**, exact **235/236**, couverture **0,9874**,
  **3 spans** (`g017`, `r035`, `r264`). La cible de A17 est **atteinte et dépassée** ; la fiche n'est
  plus l'état, c'est l'**histoire**.
- **À retenir** : A17 n'est **pas une ligne de roadmap A** ; c'est un identifiant d'audit
  (comme A23, A24, A26, A29). Il ne doit pas figurer dans l'inventaire A.

### A23 — la note est juste sur l'effet, fausse sur la cause

- `rapport-file-taches.md` : **29 tâches** (8 autonomes, 11 coordination, 10 bloquées), **6 doublons**,
  **18 périmées** ; T18 propose de retirer A2.6 de la frontière.
- **Effet** : A2.6 **ne doit pas** être la tête de frontière (tête décidée, A8.3a fait, lot répondu).
  **D'accord.**
- **Cause** : « experts bloqués A6.2 » est **faux** — le MoE existe ; la dépendance A6.2 est un
  **plafond conceptuel**, pas une arête dure. **Désaccord.**
- **Non appliqué** : `verifie_backlog.py` liste toujours **A2.6, N2, N4** ; `dependances.md` § 5
  annonce **4** items (A2.6, N2, N3, N4) alors que N3 est mesurée. La doc est en retard de deux
  corrections.

### A24 — un audit, pas une ligne ; les correctifs sont partiels

- `rapport-produit-bloc-l.md` : **50 phrases**, **0 plantage**, **34/50** avec au moins une anomalie,
  **132 paires** de chevauchement (31/50), **18 correctifs** ; harnais **non committé** (`/tmp/audit_produit_bl`).
- **Appliqué depuis** : robustesse surrogate/non-str (2 bugs), frontières de phrase **0/40**,
  compositions sans perte, partition `alternative` par défaut ; le re-test `filtrer` donne
  **0 chevauchement / 297 segments** (les 5 sans syntagme sont non linguistiques).
- **Reste** : le défaut `alternative` garde **145** chevauchements (re-test 21 h) ; `filtrer` en
  supprime mais perd des attachements ; P0-4 (cascade) et P0-5 (langue) restent.
- **Collision d'identifiants** : `rapport-re-test-produit.md` appelle l'audit CLI « **A26** » —
  homonyme de la ligne **A2.6**. Les audits A17/A23/A24/A26/A29 ne sont pas des lignes de roadmap.

## 5. La frontière réelle

### Ce que le graphe calcule

`python3 tools/verifie_backlog.py` → **frontière (3) : A2.6, N2, N4**. A2.6 y est parce que sa fiche
dit `Dépend de : A2` (acquis) et n'a **pas** de `Bloqué par` ; A6.2 est un **plafond** (`douce`), pas
une arête dure. L'outil est cohérent avec les fiches ; ce sont les fiches qui sont fausses.

### Ce qui est réellement libre en A

| ligne | libre ? | pourquoi | suite |
|---|---|---|---|
| **A2.6** | **oui, mais P2** | tête décidée ; experts mesurables sur le MoE local ; le travail restant est du **code de placement** | à ne pas mettre en tête de frontière ; suite de A6.2 |
| **A6.2** | **oui** | MoE local 18 Go, 2×16 Go VRAM, 125 Go RAM ; trace et imposition du routage existent ; le MoE tourne en offload/CPU, le blocage « 16 Go » est une résidence mono-GPU | **action 2** |
| **A8.3b2** | **oui** | instrumenter `forward_lot` ; aucune ressource externe | **action 3** |
| **A3.4** | **non** | compte et runtime Colab | bloqué réel |
| **A5.4** | **non** | carte Stratix V | bloqué réel |

### Ce qui est fermé ou décidé (pas « libre »)

A1, A3.2, A3.3, A4, A5.1–A5.3, A6.1, A6.3, A7, A8.0 : **faits/mesurés**. A8.3 : **décidé opt-in**
(négatif). A8.3a : **fait 3/19**. A8.3b/c/d : **expliqués**. A2.6 tête : **décidée**.

### La frontière, en une phrase

**A a trois lignes libres (A2.6 P2, A6.2, A8.3b2), deux bloqués réels (A3.4, A5.4) et un faux
bloqué (A6.2).** Le graphe en annonce trois, dont un (A2.6) pour la mauvaise raison et sans les
deux autres. **A23 avait raison de vouloir retirer A2.6 de la tête ; il faut aussi retirer A6.2 de
la liste des bloqués.**

## 6. Les trois prochaines actions de A, mesurables

### Action 1 — requalifier la frontière A (docs, aucun code)

- **Quoi** : A2.6 → « partiel, P2 ; tête refusée (décision, +10 % historique, pas de run courant) ;
  experts : placement sur le MoE local, suite de A6.2 » ; **8 tests**, pas 4 ; **A8.3a fait 3/19**,
  pas « à venir » ; A6.2 → « libre, MoE local 18 Go ; le blocage est la résidence mono-GPU 16 Go » ;
  A8.3b2 → ligne nommée ; `dependances.md` § 5 : **4 → 2/3** items ; roadmap A8 : **6 → 19** pins.
- **Mesure** : `python3 tools/verifie_backlog.py` (frontière sans A2.6 en tête ; A6.2 hors bloqués) ;
  `grep -R "aucun MoE local∣4 tests∣A8.3a à venir"` → **0** occurrence dans les fiches A.
- **Cible** : **2 bloqués** (A3.4, A5.4), **3 libres** (A2.6 P2, A6.2, A8.3b2), **0 faux bloqué**.
- **Contrôle négatif** : si A2.6 est marqué « bloquée par A6.2 », le graphe sera cohérent mais
  **faux** — c'est exactement le défaut actuel.

### Action 2 — A6.2 : mesurer le routage sur le MoE local

- **Quoi** : `bash tools/porte-echange-experts.sh` (18 Go, 48 couches, 128 experts, 8 utilisés) ;
  capturer `DRAVE_TRACE_EXPERTS`, imposer `DRAVE_ROUTAGE_FORCER` ; mesurer la PPL et le coût de
  routage sur le 30B.
- **Mesure** : invariant **exact** (son propre routage = référence) ; routage étranger ≠ référence ;
  taux de succès du cache d'experts ; octets lus par jeton ; PPL à qualité égale (**±0,1**).
- **Cible** : qualité égale et **coût de routage ÷10** (le contrat A6.2), ou une **borne nommée**
  (VRAM/offload) ; fiche `reports/rapport-a62-moe.md` + JSON.
- **Contrôle négatif** : routage **aléatoire** (doit dégrader), trace **vide** (la porte doit
  refuser), et le même run sans `DRAVE_ROUTAGE_FORCER`.

### Action 3 — A8.3b2 : instrumenter le chemin lot

- **Quoi** : instrumenter `forward_lot` (ordre de sommation, quantification d'activation) pour
  expliquer l'écart **61,9920 / 60,8135** (1,90 %) entre lot 1 et lot ≥ 2.
- **Mesure** : `LOT=1` / `LOT=4 bash tools/porte-flux.sh` ; écart avant/après instrumentation ;
  vérifier que **THREADS=1** ne change rien (déjà mesuré).
- **Cible** : écart **< 0,1 %** (somme déterministe) **ou** cause nommée ; les **19/19** pins ont
  alors un régime dual ; fiche `reports/rapport-a83b2-lot.md` + JSON.
- **Contrôle négatif** : `THREADS=1` (le pool n'est pas la cause) et `LOT=1` = mode 0 (le chemin
  non loti est la référence).

## 7. Contrôle négatif de cet état, et ce qui pourrait le rendre faux

- **Ce qui pourrait le rendre faux** : le HEAD a bougé pendant l'audit (`d31aa9a2` → `7a876f70`) ;
  les fiches A24/A26 sont des instantanés et le code du bloc a changé à 21 h 47 ; les portes
  `pont`/`coupe` n'ont pas été rejouées ; le harnais A17 n'est pas committé ; le MoE n'a pas été
  relancé ici (les chiffres C9/A8.3c sont lus, pas reproduits).
- **Le contrôle qui compte** : `cargo test placement` (**8/8**) et `DRAVE_PERTE_MAX=1 porte-flux`
  (**exit 0**, 58,3200 / 62,7357) sont des **rejeux**, pas des lectures. Ils confirment A2.6
  (règle) et A8.3a (régime 1 %) au HEAD.
- **Ce qui invaliderait la frontière** : si le MoE local ne tournait **pas** sur cette machine, A6.2
  et A2.6-experts seraient bloqués. Ce n'est pas le cas : le fichier de 18 Go est présent, la
  machine a 125 Go de RAM et 2 × 16 Go de VRAM, et trois fiches l'ont fait tourner.

## 8. Fichiers et limites

- **Fichiers neufs** : `reports/rapport-etat-a.md` (ce rapport) et `reports/pensee-etat-a.json`
  (la version machine).
- **Aucun existant modifié, aucun commit.** Le rapport n'est pas ajouté à `reports/README.md` ni à
  `reports/INDEX.md` (ce serait modifier un existant) ; il est découvrable par son nom.
- **Limite de méthode** : cet état **lit** les fiches et **rejoue** six commandes ; il ne remplace
  ni une passe complète (`bash tools/toutes-les-portes.sh`, 2 h) ni les runs A8.3b2/A6.2.
- **Voir aussi** : [`roadmap.md`](../docs/pilotage/roadmap.md) ·
  [`en-cours.md`](../docs/pilotage/en-cours.md) ·
  [`backlog/index.md`](../docs/pilotage/backlog/index.md) ·
  [`dependances.md`](../docs/pilotage/backlog/dependances.md) ·
  [`A2.6`](../docs/pilotage/backlog/A2.6-ordonnanceur.md) ·
  [`A6.2`](../docs/pilotage/backlog/A6.2-moe-local.md) ·
  [`A8.3`](../docs/pilotage/backlog/A8.3-defaut.md) ·
  [`rapport-a26-bilan.md`](rapport-a26-bilan.md) ·
  [`rapport-a83a-coupe.md`](rapport-a83a-coupe.md) ·
  [`rapport-file-taches.md`](rapport-file-taches.md) ·
  [`rapport-produit-bloc-l.md`](rapport-produit-bloc-l.md) ·
  [`rapport-spans-v7.md`](rapport-spans-v7.md).
