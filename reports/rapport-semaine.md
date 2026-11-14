# J5.1 — le rapport de semaine : le produit gagne 3,69 points de F1, l'intégration est bornée

> **Instantané historique** — les chiffres publiés ici sont ceux du commit de la fiche ; ils ne
> décrivent pas l'état courant. L'état courant du bloc est dans
> [`en-cours`](../docs/pilotage/en-cours.md) et [`la roadmap`](../docs/pilotage/roadmap.md).

> **Ligne de roadmap** : **B13** (le moteur de pensée), **R0.7** (le bloc langue), **N2**, **S**,
> **R**, **A**, **Panini** · **Tâche** : J5.1 · **Date** : 2026-11-13 · **Verdict** : ✅
>
> **Ce que ce rapport est.** La **relecture consolidée** des fiches des jours 1 à 4 : les chiffres
> avant/après, les décisions, les rejets et ce qui reste. **Aucune mesure nouvelle** : chaque
> chiffre est celui de sa fiche, avec sa base, son contrôle négatif et sa limite.
>
> **Base.** Gold vivant **612 phrases / 239 cibles / 3 179 jetons** ; POS heuristique **0,8625** ;
> F1 **0,7533** au départ de la semaine ; commits J1–J3 `25a6c0ff` → `c2e629b3` ; fiches J4 du
> **13/11** (HEAD `dc78f223`). Les fiches J4 de N2, S et A ne sont pas encore committées au moment
> de la rédaction : **J5.1 les emporte avec ce rapport**.
>
> **Le verdict en une phrase.** Le **produit** a gagné **+0,0369 de F1** (0,7533 → 0,7902),
> **1 attachement exact** (236 → 237) et deux livrables (schéma v2, restitution v0) ; le **tagger
> API** mesure **+8,49 pts** (0,8625 → 0,9475) et la règle dit **intégrer** ; l'**intégration
> Panini** est **mesurée et bornée** (table 14/14, corpus 418/438, retrieval à script dominant,
> généalogie à deux faces) ; la **coordination** N2/S/R/A est **datée**, mais **la passe complète,
> le tag et la release restent à faire (J5.2)**.

## 1. Ce que la semaine devait produire — et ce qu'elle a produit

| axe | prévu (plan § 7) | produit au 13/11 | écart |
|---|---|---|---|
| **produit** | 2 spans tranchés (ou déclarés), schéma v2, restitution v0, porte verte | `r035` tranché (1 span), `g017` déclaré, `s065` cible fausse déclarée ; schéma v2 (26 cas / 0 échec) ; restitution v0 (46/46, miroir 0,1087) ; autotest 183/183 | **1 span sur 2** ; la porte complète est J5.2 |
| **intégration** | table atomes ↔ niveaux, corpus commun, retrieval à époque contrôlée, généalogie à deux faces | table 14/14 (**hypothèse**) ; corpus 21 textes / 418 sur 438 ; retrieval 3 corpus ; généalogie 210 paires | **fait, mais borné** : aucune signature V14 des 21 langues |
| **coordination** | état daté N2/S/R/A, décisions nommées | 4 fiches + 4 JSON ; décisions D1–D8 ; aucune écriture dans S/D/N2/A | **fait** ; les commits J4 sont emportés par J5.1 |
| **consolidation** | passe complète, tag, rapport, roadmap | ce rapport ; état et roadmap mis à jour | **J5.2 reste** : passe, tag, release |

**Les dates réelles ne sont pas celles du plan.** J1, J2 et J3 ont été exécutés le **07/11**
(le plan les plaçait du 07 au 09) ; J4 le **13/11** (plan : 10/11) ; J5.1 le **13/11**
(plan : 11/11). Le décalage vient de la reprise de la boucle après épuisement du budget, pas d'un
changement de périmètre. Ce rapport décrit l'état **constaté**, pas le calendrier prévu.

## 2. Les chiffres avant/après

### 2.1 Le produit : F1, attachement, POS

| mesure | avant | après | Δ | contrôle | fiche |
|---|---:|---:|---:|---|---|
| POS (heuristique, production) | 0,8625 | **0,8625** | 0 | 0 jeton changé sur 3 179 par J1.1/J1.2 | [r035](rapport-r035.md) |
| F1 syntagmes (vue alternative) | 0,7533 | **0,7902** | **+0,0369** | 183/183 ; placebo 0,7758 ; adverbe large rejeté | [convention](rapport-convention-gv.md) |
| F1 dev / test | 0,7476 / 0,7663 | **0,7875 / 0,7962** | +0,0399 / +0,0299 | le test n'a pas choisi la règle (in-sample) | [convention](rapport-convention-gv.md) |
| F1 vue linéaire | 0,8120 | **0,8144** | +0,0024 | filtre `filtrer` ; attachement 223/224 | [convention](rapport-convention-gv.md) |
| attachement exact / labels | 236/237 | **237/238** | **+1** | 0 cible perdue, 0 span perdu sur 239 cibles | [r035](rapport-r035.md) |
| couverture (labels / 239) | 0,9916 | **0,9958** | +0,0042 | — | [r035](rapport-r035.md) |
| schéma | v1 | **v2** | +2 champs | 26 cas / 0 échec ; 1 836 annotations / 0 échec ; v2 refuse v1 | [schéma](rapport-schema-v2.md) |
| restitution surface | — | **46/46 = 1,0000** | — | contrôle négatif 46/46 ; sans correctif `C`, 45/46 | [restitution](rapport-restitution-v0.md) |
| miroir strict | — | **5/46 = 0,1087** | — | min(surface, mots, POS) ; 0/46 au mélange et à la troncature | [restitution](rapport-restitution-v0.md) |

Trois lectures, et il faut les tenir ensemble :

- **POS ne bouge pas.** Les deux règles J1.1 et J1.2 sont des règles de **syntagmes** ; le diff
  token par token donne **0 token changé** sur 3 179. Ce n'est pas un échec : c'est le contrôle
  qui dit que le gain F1 ne vient pas d'une dérive des étiquettes.
- **Le gain F1 est in-sample.** La convention du sujet est **lue dans le gold** (712 GV sur 712
  commencent par un `VERB`, un `AUX` ou un `ADV` de négation) puis appliquée au gold. Le test ne
  la choisit pas, il ne la contredit pas non plus : c'est une **convention**, pas une
  généralisation hors échantillon.
- **Le miroir strict n'est pas 1,0.** La surface est exacte, mais `mots` et `POS` séparent
  `dort.` en `dort .` : la restitution v0 est un **codec de surface**, pas un décodeur. Le
  correctif `C` (sauts de ligne) a ramené la surface de 45/46 à 46/46 : le miroir a trouvé un
  trou, c'est son résultat utile.

### 2.2 Le tagger POS : la seule mesure qui change l'ordre de grandeur

| corpus | heuristique | API | Δ | IC95 bootstrap |
|---|---:|---:|---:|---:|
| **612** | 0,8625 (2 742/3 179) | **0,9475 (3 012/3 179)** | **+8,49 pts** | **[+7,23 ; +9,74]** |
| réel 432 | 0,8893 (2 112/2 375) | **0,9360 (2 223/2 375)** | **+4,67 pts** | [+3,45 ; +6,01] |
| synth 160 | 0,7682 (537/699) | **0,9828 (687/699)** | +21,46 pts | [+18,80 ; +24,15] |
| hand 20 | 0,8857 (93/105) | **0,9714 (102/105)** | +8,57 pts | in-sample |

McNemar **344/74**, **p = 1,1 × 10⁻⁴²**. Contrôles négatifs : majoritaire **0,2145**, classe
fréquente **0,2491**, permutation **0,1667**, uniforme **0,0833** — tous sous 0,25, loin des
0,8625 et 0,9475. Coût mesuré : **1 218 appels**, **358 962 tokens**, **20 min 59 s**, **~0,04 $**
hors pointe, cache neuf. La clé était dans `~/.config/drave/deepseek.key` (0600), pas dans
`DEEPSEEK_API_KEY` : la prémisse « clé absente » était fausse.

**La réserve est décisive.** Le **612** agrège trois corpus : le **réel 432** ne gagne que
**+4,67 pts** (l'IC contient +5), le **synth 160** gagne **+21,46** et tire le 612 au-dessus de
+5, et les **20 hand** sont **in-sample** (ils ont servi au choix du modèle et du prompt). La
règle de décision `≥ +5 → intégrer` s'applique au 612 : **intégrer**, mais le **split réel tenu à
l'écart** est la prochaine mesure qui peut faire descendre le chiffre sous +5, voire sous +2.
La baseline publiée **0,8500** est **datée** : elle reproduit au commit `97256b8f`, la référence
du HEAD est **0,8625** ; comparer à 0,8500 surestime le gain de **1,26 pt**.

### 2.3 L'intégration Panini : quatre briques, quatre contrôles

| brique | avant | après | contrôle | fiche |
|---|---|---|---|---|
| table atomes ↔ niveaux | 0 ligne mesurée | **14/14 lignes, 8 niveaux** | hypothèse, pas corrélation ; 33 paires à ∣r∣ ≥ 0,5 | [atomes](rapport-atomes-niveaux.md) |
| corpus commun | 0 texte commun | **21 textes, 418/438 paires exactes (95,4 %)** | 8/8 (6 rejets + 2 témoins) | [corpus](rapport-corpus-commun.md) |
| retrieval | 0 mesure | **B7 4 004 paires, UDHR 420, Bible 132** | cibles permutées au hasard ; années permutées p = 0,19 | [retrieval](rapport-retrieval-epoque.md) |
| généalogie | 0 confrontation | **210 paires, 154/154 hors script au hasard** | permutations de labels p = 0,006/0,019 ; LOO | [généalogie](rapport-genealogie-deux-faces.md) |

**Ce que les chiffres portent.**

- **Table** : 14 atomes, 8 niveaux, 14 lignes ; **33 paires** d'atomes à ∣r∣ ≥ 0,5 en brut,
  **4 composantes > 1**, les trois premières à **80,7 %** de la variance (6,967 · 2,845 · 1,491).
  **Aucune correspondance atome ↔ niveau n'est mesurée** : la table est une **grille de lecture**
  et un protocole. Les trois candidats directs sont **№ → mot**, **⊗ → pos**, **⊞ → document** ;
  si eux ne corrèlent pas, le problème est la signature lexicale de Panini, pas la table.
- **Corpus** : 532 langues Panini, 456 Drave, **453 communes**, 438 appariables,
  **418 exactes (95,4 %)** ; **20 écarts de surface exclus, pas corrigés** (apostrophes,
  cédilles, virgules, ordre des diacritiques) ; 21 textes (20 strates + français pivot),
  **5 familles, 10 écritures, 42 phrases, 3 603 caractères** ; 8/8 contrôles.
- **Retrieval** : B7 71 langues / 35 concepts / 4 004 paires, top-1 **0,138** contre hasard
  **0,055** ; UDHR 21 langues / 30 articles / 420 paires, top-1 **0,049** contre **0,0333** ;
  Bible 12 traductions / 1 000 versets / 132 paires, top-1 **0,293** contre **0,001**. Bible :
  écriture **+0,609** [0,529 ; 0,702], famille **+0,181** [0,106 ; 0,253], **date −0,034 par
  siècle** [−0,075 ; +0,009], **p = 0,19**, R² **0,763**. À écriture contrôlée, contemporains et
  décalés sont au **même niveau : 0,710 vs 0,710**. Le renversement brut **0,238 vs 0,427** est
  un **effet de composition** : 60 % des couples décalés sont de même écriture, contre 33 % des
  contemporains.
- **Généalogie** : **154/154** paires hors script au **hasard exact** (MRR 0,1332, top-1 0,0333) ;
  56 paires de même script à MRR **0,1999** ; **8 paires même famille + même script** à MRR
  **0,3853**, dont **7/8** au-dessus du hasard. Couverture : Panini `LANG_TREE` **5/21**
  (200/210 paires « inconnu »), métadonnées UDHR **15/21** (105/210), Glottolog **21/21**.
  Là où les deux faces se rencontrent : **15/15 familles**, **14/15 branches** au nœud exact,
  Spearman **0,657**, Pearson **0,918**. Sur les 105 paires couvertes, R² **0,256** (Panini)
  contre **0,230** (Glottolog) : même information, deux granularités. V14 ne couvre que
  **3/21** langues (`udhr_decomposed_v14`), **1/21** (`udhr_convergence_v14`).

### 2.4 La coordination N2 / S / R / A

| ligne | avant | après | décision | fiche |
|---|---|---|---|---|
| **N2** | `eval_n2_propre` **8,0225** à 128 | **2,9726** à 128 / **2,7856** à 1 024 (RoPE + canal) | `--rope --canal-dir`, pas `--rope` seul (40,0658) | [N2](rapport-coordination-n2.md) |
| **S** | clone `523d8c1` : **8 verdicts / 4 acceptés** | working tree : **19 / 11 / 0 candidat sans verdict** | committer les 11 (7 acceptés, 4 exclus) + pointeur | [S](rapport-coordination-s.md) |
| **R** | heuristique **0,8625** | API **0,9475** (**+8,49**) | intégrer derrière un drapeau ; split réel tenu à l'écart | [R](rapport-coordination-r.md) |
| **A** | A6.2 « bloquée » | **A6.2 libre** (MoE 18,56 Go, PPL 37,2013, porte 54,5202) | D1–D8 ; A8.3b2 à nommer dans le graphe | [A](rapport-coordination-a.md) |

**N2.** Le bug a **deux** causes : `charge()` construit un `NativeModel` absolu et
`ppl_protocole()` oublie le canal. `--rope` seul rend **40,0658** ; `--rope --canal-dir` rend
**2,9726 / 2,8988 / 2,8443 / 2,7856** à 128/256/512/1 024, identique au mètre de référence
`eval_longueurs.py --rope`. Le **test** à 1 024 est **2,8566** ; le seuil est 2,5 ; il manque
**0,3566** en test (0,2856 en validation). Contrôles : permutation **1 692,39** (canal inchangé)
et **1 880,66** (canal permuté) ; checkpoint absolu **3,0971 / 3,2098** ; `rope2048` **5,4773** à
128 et **4,6321** à 1 024. Le correctif est **local à Hauru** tant que `rope_model.py` n'est pas
promu dans `tools/`.

**S.** Les **11 verdicts** `a004`–`a009` sont **11 lignes non committées** (lignes 9–19) :
**6 `resolu`, 1 `compatible`, 4 `exclu`**, soit **7 acceptés / 4 exclus**. Le working tree voit
**19 verdicts / 11 acceptés / 0 candidat sans verdict** ; un clone à `523d8c1` voit **8 / 4 / 11**.
Les 11 lignes portent **16 mappings uniques** ; **7/16** sont justes, **9/16** faux ou restés aux
défauts de la page. L'option **A** (committer tel quel, puis corriger les référents séparément)
est recommandée ; l'option **B** (corriger avant le commit) ferait perdre la seule trace de la
valeur d'origine.

**R.** Voir § 2.2. Les cinq modes neuronaux rendent la **même** exactitude : la fusion est
**neutre** sur ce gold. L'hybride « fermé heuristique / ouvert modèle » gagne **+0,41 pt** mais
McNemar **31/44, p = 0,17** : **non significatif**, piste et non décision.

**A.** Le MoE `qwen3-30b-a3b-Q4_K_M` existe : **18 556 686 752 o = 17,28 GiB**, **48 couches**,
**128 experts**, **8 utilisés** par jeton. `--ppl` rend **37,2013** (limit 32) ; la porte
`porte-echange-experts` rend **54,5202** à N = 16 avec **768** décisions de routage, l'invariant
exact et le routage étranger à **36 074,9497**. Le blocage est la **résidence mono-GPU** (17,28 >
16 GiB), pas l'absence de MoE ; le cache VRAM d'experts n'est câblé que pour **MXFP4**, pas pour
le **Q4_K**. Regroupement par expert : **÷15,51** au lot 192, **÷7,08** au lot 64, **÷2,27** au
lot 8 ; préremplissage **×1,58** au lot 192 ; cache LRU 25 % → **74,8 à 87 %** des lectures,
50 % → **92 à 93 %** ; cache VRAM plafond **×1,09** ; cache RAM **+4 % / +21 %** (perdant).
A8.3b2 est **libre** mais **hors du graphe** ; `LOT=1` échoue **par construction** (61,9920
contre 60,8135) ; l'A/B manuel lot 1 / lot 4 redonne **61,9920 / 60,8135**. Le compte des pins A8
reste à trancher : **18** (`a83b-decision.json`) ou **19** (audit A8.0).

## 3. Les décisions

| # | décision | preuve | état / suite |
|---|---|---|---|
| **D1** | Adopter la **relative zéro à préposition orpheline** | 237/238, couverture 0,9958 ; 5 contrôles négatifs ; généralisation « The book he reads about » | ✅ ; `g017` reste |
| **D2** | Adopter **sujet hors du GV** + **adverbe final de temps** étroit ; rejeter l'adverbe large et l'objet hors GV | F1 0,7902, 0 perte d'attachement ; placebo 0,7758 ; adverbe large 0,7552 | ✅ ; objet 75 FP / 51 FN ouvert |
| **D3** | Publier le **schéma v2 additif** (`meta.partition`, `meta.alternative`), garder v1 lue | 26 cas / 0 échec ; 1 836 annotations / 0 échec ; v2 refuse v1 | ✅ ; invariants sémantiques à tester |
| **D4** | La **restitution v0** est un codec de surface, pas un décodeur ; ajouter la catégorie `C` | 46/46 surfaces ; miroir 0,1087 ; contrôle 46/46 ; sans `C` 45/46 | ✅ ; v0.1 ponctuation, gold de restitution |
| **D5** | La **table atomes ↔ niveaux** est une grille de lecture, pas une mesure ; protocole CLR / permutations / BH / split-half | 14/14 lignes ; 33 paires colinéaires ; 4 composantes > 1 | ✅ ; V14 des 21 langues à mesurer |
| **D6** | Le **corpus commun** est l'UDHR article 1, 21 textes ; **exclure** les 20 écarts, ne pas les corriger | 418/438 exactes ; 8/8 contrôles ; 20 écarts listés | ✅ ; corpus multi-époques à construire |
| **D7** | Le **retrieval** est de surface ; **stratifier par écriture** ; ne pas lire le brut | script +0,609 ; date −0,034 (p = 0,19) ; 0,710 vs 0,710 ; brut 0,238 vs 0,427 | ✅ ; réplication neuronale ouverte |
| **D8** | Comparer les deux généalogies sur les **paires couvertes** ; « inconnu = 1,0 » n'est **pas** une distance | R² 0,256 vs 0,230 ; 154/154 hors script ; indicateur d'inconnu −0,172/−0,290 | ✅ ; V14, 9 dhātus, distance continue |
| **D9** | **Ne pas livrer `--rope` seul** ; valider `--rope --canal-dir` et `eval_longueurs.py --rope` ; promouvoir `rope_model.py` | 40,0658 seul contre 2,9726/2,7856 avec canal | ✅ ; porte propre 0,2856/0,3566 |
| **D10** | **Committer les 11 verdicts S tels quels** (option A), puis corriger les 9/16 référents | 7 acceptés / 4 exclus ; clone 8/4/11 ; 16 mappings | ⏳ ; sous-module + pointeur |
| **D11** | **Intégrer le POS API** (neuronal seul, drapeau, repli heuristique) ; split réel tenu à l'écart avant défaut | +8,49 pts ; réel +4,67 ; 0 refus POS | ⏳ ; route + split |
| **D12** | **A6.2 libre** ; métrique M1 = octets lus au lot 192 ; mesurer en **offload CPU** ; **A8.3b2** à nommer ; A8.3 **opt-in** | 37,2013 ; 54,5202 ; ÷15,51 / ÷7,08 | ⏳ ; rapport A6.2, harnais |
| **D13** | **J5.1** : le produit est mesuré, l'intégration est bornée, la semaine **n'est pas close** | les fiches J1–J4 | ✅ ; J5.2 (passe, tag, release) |

## 4. Les rejets

| # | rejeté | chiffre | raison |
|---|---|---|---|
| **R1** | L'**adverbe large** (tout `ADV` final hors GV) | F1 0,7552 (+0,0003) ; test 0,7656 < 0,7663 | 12 FP d'adverbe corrigés, 11 FP de troncature créés ; le gold se contredit |
| **R2** | L'**objet hors du GV** | F1 0,7531 (en baisse) | 20 FP d'objet corrigés, 13 FP de troncature créés |
| **R3** | Le **placebo sujet** (déplacer le premier token sans condition) | F1 0,7758 ; 38 phrases perdantes | 0 phrase perdante pour la règle conditionnelle |
| **R4** | Le **placebo adverbe** (arrêter au dernier token) | F1 0,7440 ; 627 FP contre 555 | tronquer au hasard détruit des GV |
| **R5** | « Le **schéma v2** prouve le sens » | 26 cas / 0 échec | il valide la **forme**, pas la réciprocité, les rangs ni l'unicité |
| **R6** | **Corriger** les 20 écarts de surface Panini ↔ Drave | 20 exclus sur 438 appariables | corriger une source pour l'autre **fabrique** l'accord |
| **R7** | Un **effet d'époque** dans le retrieval | brut 0,238 vs 0,427 ; à script contrôlé 0,710 vs 0,710 ; date −0,034, p = 0,19 | effet de **composition** (60 % vs 33 % de même écriture) |
| **R8** | « La **filiation** de Panini = la **famille** de Drave » | 3/655 paires inter-langues, 479 avec une langue vide | deux objets : **tradition** contre **famille de langues** |
| **R9** | « **Inconnu = 1,0** » comme distance | 200/210 paires P1, 105/210 P2 | c'est une **valeur manquante** ; l'indicateur d'inconnu porte −0,172/−0,290 |
| **R10** | Les **9 dhātus** mesurables en l'état | aucune matrice V14 ; 4 composantes (corrélation) ou 1 (covariance) | sans matrice, la projection n'est pas identifiable |
| **R11** | « V14 couvre les 21 langues » | 3/21 (`udhr_decomposed_v14`), 1/21 (`udhr_convergence_v14`) | la face atomes n'existe que pour 3 langues |
| **R12** | Le correctif **`--rope` seul** | 40,0658 (au lieu de 2,79) | le canal manque : `--rope` déplace le bug, il ne le ferme pas |
| **R13** | « **11 verdicts = 11 acceptés** » | 7 acceptés / 4 exclus ; clone 8/4/11 | deux ensembles différents ; le clone ne voit pas les 11 |
| **R14** | L'**hybride par classe** R | +0,41 pt ; McNemar 31/44, p = 0,17 | non significatif ; piste, pas décision |
| **R15** | La baseline **0,8500** | 0,8500 à `97256b8f` ; 0,8625 au HEAD | datée ; comparer à 0,8500 surestime de 1,26 pt |
| **R16** | « A6.2 bloquée faute de MoE » | MoE 18,56 Go, PPL 37,2013, porte 54,5202 | le blocage est la **résidence mono-GPU** (17,28 > 16 GiB) |
| **R17** | « A8.3b2 est dans le graphe » | absente du backlog, de la roadmap et des arêtes | nommée par une fiche et le plan, pas par le graphe |
| **R18** | La commande **`LOT=1/4 porte-flux`** | LOT=1 : 61,9920 contre 60,8135 attendu | invalide pour LOT=1 : la porte échoue **par construction** |
| **R19** | **A8.3 par défaut** | 18 ou 19 pins, 3 duales ; cause non nommée | reste **opt-in** tant que A8.3b2 n'a pas donné sa cause |
| **R20** | « Miroir = 1,0 parce que la surface est exacte » | surface 46/46, miroir 5/46 = 0,1087 | le miroir est le **minimum** surface/mots/POS |
| **R21** | « Les 20 hand généralisent » | +8,57 pts | ils ont servi au choix du modèle et du prompt : **in-sample** |

## 5. Ce qui reste

| ligne | reste | prochaine action | bloquant | fiche |
|---|---|---|---|---|
| **B13 / produit** | `g017` (1 span), `s065` (1 cible fausse) ; objet 75 FP / 51 FN ; 5 FP sujet ; vue linéaire +0,0024 | `g017`, puis T132/T133, gold 200+ | gold 200+ ; 7B local interdit | [r035](rapport-r035.md), [convention](rapport-convention-gv.md) |
| **B13 / restitution** | v0.1 ponctuation ; gold de restitution | `rendre_pos` replace la ponctuation ; banc dédié | aucun | [restitution](rapport-restitution-v0.md) |
| **B13 / schéma** | invariants sémantiques (réciprocité, rangs, unicité) | tests du bloc, pas le validateur JSON | aucun | [schéma](rapport-schema-v2.md) |
| **R0.7 / tagger** | route API derrière drapeau ; split réel tenu à l'écart | mesurer `crc32(id) % 3` ; si < +2 rouvrir et nommer le négatif | coût ~0,07 $ / 1 000 phrases ; un run | [R](rapport-coordination-r.md) |
| **Panini / atomes** | signature V14 des 21 langues | projection multilingue + test invariance/cluster | pas de données V14 sur 21 langues | [atomes](rapport-atomes-niveaux.md), [généalogie](rapport-genealogie-deux-faces.md) |
| **Panini / dhātus** | matrice 9 dhātus → 14 atomes | publier la décomposition, projeter les 44 œuvres | aucune matrice publiée | [généalogie](rapport-genealogie-deux-faces.md) |
| **Panini / généalogie** | distance continue, corpus équilibré, retrieval neuronal, multi-époques, arêtes pondérées | une mesure par ligne (§ 7 de la fiche) | corpus | [généalogie](rapport-genealogie-deux-faces.md) |
| **N2** | porte propre : 0,2856 en validation / 0,3566 en test ; `--rope --canal-dir` ; `porte-n2.sh` ; `rope_model.py` dans `tools/` | appliquer le correctif, re-épingler | GPU / runs N2 | [N2](rapport-coordination-n2.md) |
| **S** | committer les 11 verdicts + pointeur ; corriger 9/16 référents ; `.gitmodules` en chemin absolu | commande § 3 de la fiche | accès au sous-module | [S](rapport-coordination-s.md) |
| **R** | (voir R0.7 / tagger) | — | — | [R](rapport-coordination-r.md) |
| **A** | rapport A6.2 ; M1/M2/M3 ; harnais A8.3b2 ; 18/19 pins ; cache Q4_K si besoin | D1–D8 de la fiche | GPU 16 GiB ; code Q4_K | [A](rapport-coordination-a.md) |
| **J5.2** | passe complète, revue docs, tag annoté, release | `toutes-les-portes.sh` ; `revue_documentation.py` ; tag | temps (~2 h) | — |

**Ce que la semaine n'a pas produit, et qu'il faut dire.**

- **Le deuxième span n'est pas tranché.** `g017` (SUB « that she would come ») et `s065` (REL
  synthétique, cible `elle` prédite `nage`) restent ouverts ; le plan prévoyait « 2 spans
  tranchés ou déclarés », un seul l'est.
- **L'intégration n'est pas une preuve de la théorie.** La table est une hypothèse, le corpus
  est mono-époque (1948), le retrieval est de surface, la face atomes couvre 3/21 langues : ce
  sont des **bornes**, pas une validation de V14.
- **La coordination n'est pas encore durable.** Les fiches J4 sont des fichiers de travail ;
  tant que S n'a pas committé ses 11 verdicts et son pointeur, un clone ne les voit pas ; tant que
  `rope_model.py` reste dans `work/`, le correctif N2 n'est pas reproductible sur un clone neuf.
- **La semaine n'est pas close.** La passe complète, le tag et la release sont J5.2. L'autotest
  **183/183** est vert, mais ce n'est pas la passe des **84 portes**.

## 6. La chronologie et les commits

| jour | vague | tâches | livrables | commits | verdict |
|---|---|---|---|---|---|
| **J1 · 07/11** | matin | J1.1 `r035`, J1.2 convention GV | exact 237/238 ; F1 0,7533 → 0,7902 | `25a6c0ff`, `92652984` | ✅ |
| **J1 · 07/11** | après-midi | J1.3 schéma v2, J1.4 restitution v0 | 26 cas / 0 échec ; 46/46 surfaces, miroir 0,1087 | `9a259953`, `8eb0cc49` | ✅ |
| **J2 · 07/11** | matin | J2.1 inventaire + table atomes ↔ niveaux | 14/14 lignes, 33 paires colinéaires | `9c7f71dc` (+ `fffbbe5d`) | ✅ |
| **J2 · 07/11** | après-midi | J2.2 corpus commun | 21 textes, 418/438, 8/8 contrôles | `c3467170` (avec J3.1) | ✅ |
| **J3 · 07/11** | matin | J3.1 retrieval à époque contrôlée | B7 4 004, UDHR 420, Bible 132 ; script +0,609 | `c3467170` | ✅ |
| **J3 · 07/11** | après-midi | J3.2 généalogie à deux faces | 154/154 hors script ; 5/21 / 15/21 / 21/21 | `c2e629b3` | ✅ |
| **J4 · 13/11** | matin | N2, S, R | N2 8,0225 → 2,9726/2,7856 ; S 11 verdicts (7/4) ; R 0,9475 (+8,49) | fiches J4 (commit J5.1) | ✅ |
| **J4 · 13/11** | après-midi | A | A6.2 libre ; A8.3b2 hors graphe ; D1–D8 | fiche J4 (commit J5.1) | ✅ |
| **J5 · 13/11** | matin | J5.1 rapport de semaine | ce rapport + JSON ; état par jour | commit J5.1 | ✅ |
| **J5 · 13/11** | après-midi | J5.2 passe, tag, release | — | — | ⏳ |

## 7. Ce qui pourrait rendre ce rapport faux

1. **Ce rapport agrège, il ne remesure pas.** Si une fiche change (ou si un chiffre est corrigé
   dans son JSON), le rapport devient faux sans qu'aucun calcul ne l'ait signalé. La source est
   toujours la fiche, pas ce résumé.
2. **Les gains B13 sont in-sample.** La convention du sujet est lue dans le gold (712/712 GV) puis
   appliquée au gold ; le test n'a pas choisi la règle. Le +0,0369 n'est pas une généralisation.
3. **Le gold est une convention.** La relative zéro est annotée une fois, l'adverbe final est
   contradictoire (`r019`/`r186`, `r051`/`r189`). Un autre corpus annoté autrement inverserait
   certains signes.
4. **L'intégration est de surface.** Les n-grammes de caractères capturent l'orthographe et les
   cognates, pas le sens ; le corpus est **mono-époque** (1948), **mono-genre** (déclaration),
   21 textes, 5 familles, 10 écritures. Le signal de famille est porté par **2 ou 3 paires**.
5. **Le POS API est un run unique.** Un seul jour, un seul alias (`deepseek-chat` servi par
   `deepseek-flash`), température 0 mais API non déterministe au bit près ; le 612 est tiré par
   les 160 synthétiques ; le réel 432 ne gagne que +4,67. Le split réel tenu à l'écart n'est pas
   fait.
6. **N2 mesure une validation, pas une porte.** 2,7856 est le meilleur des quatre longueurs en
   validation ; le test à 1 024 est 2,8566 et manque 0,3566. Une seule graine, un seul run, une
   seule machine ; pas de barre d'erreur.
7. **A6.2 mesure le MoE existant, pas un routeur appris.** La porte et `--ppl` sont des rejeux,
   pas une performance interactive ; `reports/rapport-a62-moe.md` n'existe pas ; la résidence
   mono-GPU est une constatation de taille, pas une mesure de latence.
8. **S n'est vrai que dans le working tree.** Un clone à `523d8c1` voit 8 verdicts / 4 acceptés /
   11 candidats sans verdict. Le `.gitmodules` en chemin absolu peut même empêcher un clone sur
   une autre machine.
9. **La passe complète n'est pas faite.** L'autotest 183/183 n'est pas les 84 portes ; J5.2 doit
   lancer `toutes-les-portes.sh`, la revue de documentation et le tag. Les rouges tolérées sont
   celles de `references-non-regression.md`, pas celles qu'on découvre.
10. **Les compteurs bougent.** Le dépôt a des sessions concurrentes ; les fiches J4 et ce rapport
    changent le compte des fichiers et des JSON. L'état `en-cours` est la source du compte, pas
    ce rapport.

## 8. Fichiers

- **Nouveaux** : `reports/rapport-semaine.md` (ce rapport), `reports/rapport-semaine.json`.
- **Relus, J1** : [`rapport-r035.md`](rapport-r035.md) + `pensee-r035.json` ;
  [`rapport-convention-gv.md`](rapport-convention-gv.md) + `pensee-convention-gv.json` ;
  [`rapport-schema-v2.md`](rapport-schema-v2.md) + `pensee-schema-v2.json` ;
  [`rapport-restitution-v0.md`](rapport-restitution-v0.md) + `pensee-restitution-v0.json`.
- **Relus, J2–J3** : [`rapport-atomes-niveaux.md`](rapport-atomes-niveaux.md) +
  `atomes-niveaux.json` ; [`rapport-corpus-commun.md`](rapport-corpus-commun.md) +
  `corpus-commun.json` ; [`rapport-retrieval-epoque.md`](rapport-retrieval-epoque.md) +
  `retrieval-epoque.json` ; [`rapport-genealogie-deux-faces.md`](rapport-genealogie-deux-faces.md)
  + `genealogie-deux-faces.json`.
- **Relus, J4** : [`rapport-coordination-n2.md`](rapport-coordination-n2.md) +
  `rapport-coordination-n2.json` ; [`rapport-coordination-s.md`](rapport-coordination-s.md) +
  `rapport-coordination-s.json` ; [`rapport-coordination-r.md`](rapport-coordination-r.md) +
  `rapport-coordination-r.json` ; [`rapport-coordination-a.md`](rapport-coordination-a.md) +
  `rapport-coordination-a.json`.
- **Mis à jour** : [`docs/pilotage/semaine-autonome.md`](../docs/pilotage/semaine-autonome.md)
  (l'état de chaque jour) ; [`docs/pilotage/en-cours.md`](../docs/pilotage/en-cours.md)
  (compteurs et ligne J5.1) ; [`reports/README.md`](README.md) (fiches courantes) ;
  [`reports/INDEX.md`](INDEX.md) (régénéré).
- **Non modifiés** : les fiches et JSON ci-dessus (sauf ce rapport et son JSON), `tools/`,
  `drave-core/`, `data/`, `work/` ; le journal est archivé par le hook, il n'est pas rédigé ici.

## 9. Verdict

**J5.1 est fait.** Le produit a un gain mesuré (**F1 0,7533 → 0,7902**, **attachement 236 → 237**,
**schéma v2**, **restitution 46/46**), le tagger API a une mesure et une décision (**0,9475,
+8,49, intégrer**), l'intégration Panini a quatre briques mesurées et **bornées**, la coordination
N2/S/R/A est **datée** et ses décisions sont **nommées**. Ce qui reste est nommé : `g017`, l'objet
du GV, le split réel du tagger, la signature V14 des 21 langues, la porte N2, le commit S, le
rapport A6.2, et **J5.2** (passe, tag, release).
