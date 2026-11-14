# J10.1 — le bilan du chantier : F1 0,7533 → 0,7902, attachement 236 → 238, Panini mesuré et borné

> **Instantané historique** — les chiffres publiés ici sont ceux du commit de la fiche ; ils ne
> décrivent pas l'état courant. L'état courant du bloc est dans
> [`en-cours`](../docs/pilotage/en-cours.md) et [`la roadmap`](../docs/pilotage/roadmap.md).

> **Ligne de roadmap** : **B13** (le moteur de pensée), **R0.7** (le bloc langue), **N2**, **S**,
> **R**, **A**, **Panini** · **Tâche** : J10.1 · **Date** : 2026-11-14 · **Verdict** : ✅
>
> **Ce que ce rapport est.** La **relecture consolidée** des fiches du chantier, de J1.1 à J9.1 :
> les chiffres avant/après, les décisions, les rejets, les échecs de la boucle et ce qui reste.
> **Aucune mesure nouvelle** : chaque chiffre est celui de sa fiche, avec sa base, son contrôle
> négatif et sa limite. Le bilan **ne remplace pas** les fiches ; il les ordonne.
>
> **Base.** HEAD `81fc9ecf` (J9.1) ; gold vivant **612 phrases / 239 cibles / 3 179 jetons** ;
> gold gelé **602** ; POS heuristique **0,8625** ; F1 **0,7533** au départ du chantier ;
> **21 lancements** du superviseur, **5 timeouts**, **1 échec d'acceptation** (J5.2).
>
> **Le verdict en une phrase.** Le **produit** gagne **2 attachements exacts** (236 → 238 labels),
> **+0,0369 de F1** (0,7533 → 0,7902) et deux livrables (schéma v2, restitution v1) ; le **tagger
> API** vaut **0,9475 (+8,49)** et la règle dit **intégrer**, avec une réserve sur le réel 432
> (+4,67) ; l'**intégration Panini** est **mesurée et bornée** (table 14/14, corpus 418/438,
> retrieval à porte d'écriture, généalogie à deux faces, sœurs 0,619 contre 0,0445) ; la
> **coordination** N2/S/R/A est **datée** ; **20 tâches sur 21** passent l'acceptation, mais la
> **clôture formelle n'est pas faite** : le tag de J5.2 n'existe pas, et J14.1 doit le porter.

## 1. Ce que le chantier devait produire — et ce qu'il a produit

| axe | prévu (plan § 7) | produit au 14/11 | écart |
|---|---|---|---|
| **produit** | deux spans tranchés (ou déclarés), schéma v2, restitution v0, porte verte | `r035` tranché ; `g017` **déclaré** (convention d'adverbe à trancher, règle rejetée) ; `s065` **réglé** (cible) ; schéma v2 (26 cas / 0 échec) ; restitution v0 puis **v1** (canonique 46/46, strict 0,1087) ; porte produit **183/183** | **un span tranché sur deux** ; la clôture des portes n'est pas le tag |
| **intégration** | table atomes ↔ niveaux, corpus commun, retrieval à époque contrôlée, généalogie à deux faces | table **14/14** (hypothèse) ; corpus **21 textes / 418 sur 438** ; retrieval **3 corpus** ; généalogie **210 paires** ; **J7.1** : 532 textes, 445 langues, sœurs **0,619** contre **0,0445** | **fait, mais borné** : aucune signature V14 des 21 langues, corpus mono-époque |
| **coordination** | un état daté N2/S/R/A, les décisions nommées | 4 fiches + 4 JSON ; **D1–D20** ; aucune écriture dans S/D/N2/A | **fait** ; S n'est pas encore committé, N2 n'est pas promu |
| **consolidation** | passe complète, tag, rapport, roadmap | J5.1 ; **J10.1** ; passe **84 portes / 81 vertes / 3 rouges tolérées** | **le tag et la release manquent** (J5.2 ; J14.1 les reprend) |
| **extension J6–J10** | `g017`, `s065`, Panini approfondi, restitution v1, honnêteté, bilan | `g017` **rejeté** ; `s065` **intégré** ; J7.1 **mesuré** ; v1 **mesurée** ; **19 fiches** annotées ; bilan **écrit** | **6 livrables sur 6** ; `g017` reste une convention, pas une règle |

**Les dates réelles ne sont pas celles du plan.** J1–J3 ont été exécutés le **07/11**, J4–J5 le
**13/11**, J6–J10 le **14/11**. Le plan plaçait J1–J5 du 07 au 11/11. Le décalage vient de la
reprise de la boucle après épuisement du budget, pas d'un changement de périmètre. Ce rapport
décrit l'état **constaté**, pas le calendrier prévu.

## 2. Les chiffres avant/après

### 2.1 Le produit — POS, F1, attachement

| mesure | avant | après | Δ | contrôle | fiche |
|---|---:|---:|---:|---|---|
| POS (heuristique, production) | 0,8625 | **0,8625** | **0** | 0 jeton changé sur 3 179 par J1.1/J1.2/J6.1/J6.2 | [r035](rapport-r035.md), [s065](rapport-s065.md) |
| F1 syntagmes (vue alternative) | 0,7533 | **0,7902** | **+0,0369** | 183/183 ; placebo 0,7758 ; adverbe large rejeté | [convention](rapport-convention-gv.md) |
| F1 dev / test | 0,7476 / 0,7663 | **0,7875 / 0,7962** | **+0,0399 / +0,0299** | le test n'a pas choisi la règle (in-sample) | [convention](rapport-convention-gv.md) |
| F1 vue linéaire | 0,8120 | **0,8144** | **+0,0024** | filtre `filtrer` ; attachement 223/224 | [convention](rapport-convention-gv.md) |
| attachement exact / labels | 236/237 | **238/238** | **+2** | 0 cible perdue, 0 span perdu sur 239 cibles | [r035](rapport-r035.md), [s065](rapport-s065.md) |
| exact / cibles | 236/239 | **238/239** | **+2** | le dénominateur reste 239 (`g017` sans label) | [s065](rapport-s065.md) |
| couverture (labels / 239) | 0,9916 | **0,9958** | **+0,0042** | — | [r035](rapport-r035.md) |
| exactitude sur les spans | 0,9958 | **1,0** | **+0,0042** | 238 labels sur le bon span ; `g017` n'a pas de label | [s065](rapport-s065.md) |

Trois lectures, et il faut les tenir ensemble :

- **POS ne bouge pas.** Les règles J1.1, J1.2, J6.1 et J6.2 sont des règles de **syntagmes** ou
  d'**attachement** ; le diff token par token donne **0 token changé** sur 3 179. Ce n'est pas un
  échec : c'est le contrôle qui dit que les gains ne viennent pas d'une dérive des étiquettes.
- **Le gain F1 se décompose** : `r035` apporte **+0,0016** (0,7533 → 0,7549), la convention des
  GV **+0,0353** (0,7549 → 0,7902). Les deux règles sont des règles de **syntagmes** ou
  d'**attachement** ; aucune ne touche la POS.
- **Le gain F1 est in-sample.** La convention du sujet est **lue dans le gold** (712 GV sur 712
  commencent par un `VERB`, un `AUX` ou un `ADV` de négation) puis appliquée au gold. Le test ne
  la choisit pas, il ne la contredit pas non plus : c'est une **convention**, pas une
  généralisation hors échantillon. La règle `s065` est, elle, un seul cas, en dev.
- **Le dénominateur compte.** 238/238 est le taux sur les **labels** ; 238/239 (0,9958) est le
  taux sur les **cibles**. Le 239e span, `g017`, n'a pas de label : c'est le **1 span** de l'état
  courant, et il ne se règle pas par une règle de surface (§ 5, R22–R24).

### 2.2 Le produit — schéma et restitution

| mesure | avant | après | contrôle | fiche |
|---|---|---|---:|---|
| schéma d'annotation | v1 | **v2** (`meta.partition`, `meta.alternative`) | 26 cas / 0 échec ; 1 836 annotations / 0 échec ; v1 lue ; v2 refuse v1 | [schéma](rapport-schema-v2.md) |
| restitution surface (v0) | — | **46/46 = 1,0000** | sans correctif `C`, 45/46 ; contrôle négatif 46/46 | [restitution v0](rapport-restitution-v0.md) |
| miroir strict (v0) | — | **5/46 = 0,1087** | min(surface, mots, POS) ; 0/46 au mélange et à la troncature | [restitution v0](rapport-restitution-v0.md) |
| forme canonique (v1) | — | **46/46 = 1,0000** | contre la source canonisée ; 1/46 contre la source brute | [restitution v1](rapport-restitution-v1.md) |
| miroir strict (v1) | 0,1087 | **0,1087** | **ne monte pas** : la v1 n'est pas un codec de surface | [restitution v1](rapport-restitution-v1.md) |
| structure canonique | — | **395 segments / 395 rôles / 315 cibles** | 315/315 cibles résolues ; 313/315 dans un autre segment | [restitution v1](rapport-restitution-v1.md) |
| stabilité structurelle | — | **18/46 = 0,3913** | le lexique est stable 46/46 ; la structure ne l'est pas | [restitution v1](rapport-restitution-v1.md) |

**Ce que la restitution dit et ne dit pas.** La v0 est un **codec de surface** : la surface exacte
46/46 ne prouve pas le sens, et le miroir strict 0,1087 le rappelle. La v1 ajoute une **lecture
structurelle** (segments, rôles, cibles) qui est exacte **contre la source canonisée**, mais qui
**tombe à 1/46 contre la source brute** — c'est précisément le contrôle qui montre qu'elle ne
recopie pas la surface. Les rôles et les cibles sont **cohérents** (tous résolus, presque tous
portés par un autre segment), pas **justes** : il n'y a pas de gold de forme canonique.

### 2.3 Le tagger POS

| corpus | heuristique | API | Δ | IC95 bootstrap |
|---|---:|---:|---:|---:|
| **612** | 0,8625 (2 742/3 179) | **0,9475 (3 012/3 179)** | **+8,49 pts** | **[+7,23 ; +9,74]** |
| réel 432 | 0,8893 (2 112/2 375) | **0,9360 (2 223/2 375)** | **+4,67 pts** | [+3,45 ; +6,01] |
| synth 160 | 0,7682 (537/699) | **0,9828 (687/699)** | +21,46 pts | [+18,80 ; +24,15] |
| hand 20 | 0,8857 (93/105) | **0,9714 (102/105)** | +8,57 pts | in-sample |

McNemar **344/74**, **p = 1,1 × 10⁻⁴²**. Contrôles négatifs : majoritaire **0,2145**, classe
fréquente **0,2491**, permutation **0,1667**, uniforme **0,0833**. Coût mesuré : **1 218 appels**,
**358 962 tokens**, **20 min 59 s**, **~0,04 $** hors pointe, cache neuf. La clé était dans
`~/.config/drave/deepseek.key` (0600) : la prémisse « clé absente » était fausse pour le fichier.

**La réserve est décisive.** Le **612** agrège trois corpus : le **réel 432** ne gagne que
**+4,67 pts** (l'IC contient +5), le **synth 160** gagne **+21,46** et tire le 612 au-dessus de
+5, et les **20 hand** sont **in-sample**. La règle `≥ +5 → intégrer` s'applique au 612 :
**intégrer**, mais le **split réel tenu à l'écart** est la prochaine mesure qui peut faire
descendre le chiffre sous +5, voire sous +2. La baseline publiée **0,8500** est **datée** : la
référence du HEAD est **0,8625** ; comparer à 0,8500 surestime le gain de **1,26 pt**.

### 2.4 Panini — cinq briques, cinq contrôles

| brique | avant | après | contrôle | fiche |
|---|---|---|---|---|
| table atomes ↔ niveaux | 0 ligne mesurée | **14/14 lignes, 8 niveaux** | hypothèse, pas corrélation ; 33 paires à ∣r∣ ≥ 0,5 ; 4 composantes > 1 ; 80,7 % de variance sur 3 | [atomes](rapport-atomes-niveaux.md) |
| corpus commun | 0 texte commun | **21 textes, 418/438 paires exactes (95,4 %)** | 8/8 (6 rejets + 2 témoins) ; 20 écarts exclus, pas corrigés | [corpus](rapport-corpus-commun.md) |
| retrieval à époque contrôlée | 0 mesure | **B7 4 004 paires, UDHR 420, Bible 132** | cibles permutées ; années permutées p = 0,19 | [retrieval](rapport-retrieval-epoque.md) |
| généalogie à deux faces | 0 confrontation | **210 paires, 154/154 hors script au hasard** | permutations de labels p = 0,006/0,019 ; LOO | [généalogie](rapport-genealogie-deux-faces.md) |
| retrieval par famille (J7.1) | 0 mesure | **532 textes (445 langues)** ; famille **66,1 %** (hasard 10,3 %), sœur **26,1 %** (2,5 %) | permutations 1 000/500 ; requêtes permutées ; leave-one-language-out ; J3.1 reproduit à l'identique | [familles](rapport-retrieval-familles.md) |

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
- **Retrieval J3.1** : B7 71 langues / 35 concepts / 4 004 paires, top-1 **0,138** contre hasard
  **0,055** ; UDHR 21 langues / 30 articles / 420 paires, top-1 **0,049** contre **0,0333** ;
  Bible 12 traductions / 1 000 versets / 132 paires, top-1 **0,293** contre **0,001**. Bible :
  écriture **+0,609** [0,529 ; 0,702], famille **+0,181** [0,106 ; 0,253], **date −0,034 par
  siècle** [−0,075 ; +0,009], **p = 0,19**, R² **0,763**. À écriture contrôlée, contemporains et
  décalés sont au **même niveau : 0,710 contre 0,710**. Le renversement brut **0,238 contre
  0,427** est un **effet de composition** : 60 % des couples décalés sont de même écriture,
  contre 33 % des contemporains.
- **Généalogie J3.2** : **154/154** paires hors script au **hasard exact** (MRR 0,1332, top-1
  0,0333) ; 56 paires de même script à MRR **0,1999** ; **8 paires même famille + même script** à
  MRR **0,3853**, dont **7/8** au-dessus du hasard. Couverture : Panini `LANG_TREE` **5/21**
  (200/210 paires « inconnu »), métadonnées UDHR **15/21** (105/210), Glottolog **21/21**.
  Là où les deux faces se rencontrent : **15/15 familles**, **14/15 branches** au nœud exact,
  Spearman **0,657**, Pearson **0,918**. Sur les 105 paires couvertes, R² **0,256** (Panini)
  contre **0,230** (Glottolog). V14 ne couvre que **3/21** langues (`udhr_decomposed_v14`),
  **1/21** (`udhr_convergence_v14`).
- **J7.1 — le renversement** : sur les 25 langues `LANG_TREE`, les sœurs valent **0,619** contre
  **0,0445** pour les familles différentes (**13,9×**, Δ **+0,574** [0,490 ; 0,655], coefficient
  de sœur **+0,448**, p = 0,002, contre **+0,213** pour l'écriture). Sur l'**échantillon 20**, le
  contraste est **nul** : sœurs 0,0583 contre 0,0757 pour les familles-autres-branches et 0,0389
  pour les différentes ; coefficient de sœur **+0,0154**, p = 0,078. **J3.1 est reproduit à
  l'identique** (écart 0) : son coefficient de famille (+0,0556) n'était pas faux, il était
  **sous-dimensionné** — l'échantillon 20 ne contient que 12 paires de sœurs, dont 8 hors
  écriture. L'époque est **mono-époque par construction** (1948) ; le placebo de dates donne
  −0,0013, et le seul bras daté (Bible) donne −0,034/siècle (p = 0,19) contre +0,609 pour
  l'écriture. **L'écriture est la porte : hors écriture, tout est au hasard.** Dedans, sur
  `LANG_TREE`, la sœur est le premier effet.

### 2.5 La coordination N2 / S / R / A

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
**0,3566** en test (0,2856 en validation). Le correctif est **local à Hauru** tant que
`rope_model.py` n'est pas promu dans `tools/`.

**S.** Les **11 verdicts** `a004`–`a009` sont **11 lignes non committées** : **6 `resolu`,
1 `compatible`, 4 `exclu`**, soit **7 acceptés / 4 exclus**. Le working tree voit **19 verdicts /
11 acceptés / 0 candidat sans verdict** ; un clone à `523d8c1` voit **8 / 4 / 11**. Les 11
lignes portent **16 mappings uniques** ; **7/16** sont justes, **9/16** faux ou restés aux
défauts de la page. L'option **A** (committer tel quel, puis corriger) est recommandée.

**R.** Voir § 2.3. Les cinq modes neuronaux rendent la **même** exactitude : la fusion est
**neutre** sur ce gold. L'hybride « fermé heuristique / ouvert modèle » gagne **+0,41 pt** mais
McNemar **31/44, p = 0,17** : non significatif, piste et non décision.

**A.** Le MoE `qwen3-30b-a3b-Q4_K_M` existe : **18 556 686 752 o = 17,28 GiB**, **48 couches**,
**128 experts**, **8 utilisés** par jeton. `--ppl` rend **37,2013** ; la porte
`porte-echange-experts` rend **54,5202** à N = 16 avec **768** décisions de routage et un routage
étranger à **36 074,9497**. Le blocage est la **résidence mono-GPU** (17,28 > 16 GiB) et le cache
VRAM câblé pour **MXFP4** seulement, pas pour le **Q4_K**. A8.3b2 est **libre** mais **hors du
graphe** ; le compte des pins A8 reste à trancher : **18** ou **19**.

### 2.6 Les portes et la clôture

| élément | valeur | lecture |
|---|---|---|
| passe complète | **84 portes, 81 vertes, 3 rouges** | rouges **tolérées** : `indice`, `melange`, `sessions` ; pas de régression nommée depuis |
| porte produit | **183/183** | ce n'est **pas** la passe complète : 183 tests, pas 84 portes |
| porte du bloc | **verte** (20 tests) | `g017` rejeté sans toucher au code ; `s065` intégré avec test |
| tag `semaine-2026-11-14` | **absent** | J5.2 a expiré avant ; le tag de clôture prévu est `chantier-2026-11-14` (J14.1) |
| honnêteté des fiches | **19/19** annotées, **0** fiche de résultats périmée | 2 faux positifs nommés (`2 spans` de phrase) et les index |
| compteurs | **723 fiches / 817 JSON** au HEAD | le bilan ajoute 1 fiche + 1 JSON → **724 / 818** |

**Ce que la passe ne dit pas.** 81 vertes sur 84 ne sont pas « toutes vertes » : trois rouges sont
**tolérées** parce qu'elles sont structurelles ou de coordination, pas parce qu'elles sont
inoffensives. Le tag n'existe pas : J5.2 a été lancé, a expiré, et son acceptation était rouge.
La clôture J14.1 doit refaire la passe, relever les rouges, et taguer **si** le relevé est
conforme à `references-non-regression.md`.

## 3. Les décisions

### 3.1 Le produit

| # | décision | preuve | état / suite |
|---|---|---|---|
| **D1** | Adopter la **relative zéro à préposition orpheline** | 237/238, couverture 0,9958 ; 5 contrôles négatifs | ✅ ; `g017` reste |
| **D2** | Adopter **sujet hors du GV** + **adverbe final de temps étroit** ; rejeter l'adverbe large et l'objet hors GV | F1 0,7902, 0 perte d'attachement ; placebo 0,7758 | ✅ ; objet 75 FP / 51 FN ouvert |
| **D3** | Publier le **schéma v2 additif** (`meta.partition`, `meta.alternative`), garder v1 lue | 26 cas / 0 échec ; 1 836 annotations / 0 échec ; v2 refuse v1 | ✅ ; invariants sémantiques à tester |
| **D4** | La **restitution v0** est un codec de surface, pas un décodeur ; ajouter la catégorie `C` | 46/46 surfaces ; miroir 0,1087 ; sans `C` 45/46 | ✅ ; v0.1 ponctuation, gold de restitution |
| **D14** | **Rejeter** la règle de l'adverbe final hors de la SUB (`g017`) | F1 0,7901 ; test −0,0028 ; attachement 236/237 | ✅ ; la convention du gold reste à trancher |
| **D15** | **Intégrer** la règle « REL suivie d'un GV → le sujet de ce GV » (`s065`) | 238/238 labels, 238/239 cibles, 0 span, 0 POS ; test unitaire | ✅ ; un seul cas, en dev |
| **D17** | La **forme canonique** est une lecture structurelle, **pas** un codec ; publier strict **et** canonique | canonique 46/46 ; strict 0,1087 inchangé ; strict sur canonique 1/46 | ✅ ; gold de forme canonique à faire |

### 3.2 Panini

| # | décision | preuve | état / suite |
|---|---|---|---|
| **D5** | La **table atomes ↔ niveaux** est une grille de lecture, pas une mesure ; protocole CLR / permutations / BH / split-half | 14/14 lignes ; 33 paires colinéaires ; 4 composantes > 1 | ✅ ; V14 des 21 langues à mesurer |
| **D6** | Le **corpus commun** est l'UDHR article 1, 21 textes ; **exclure** les 20 écarts, ne pas les corriger | 418/438 exactes ; 8/8 contrôles | ✅ ; corpus multi-époques à construire |
| **D7** | Le **retrieval** est de surface ; **stratifier par écriture** ; ne pas lire le brut | script +0,609 ; date −0,034 (p = 0,19) ; 0,710 contre 0,710 | ✅ ; réplication neuronale ouverte |
| **D8** | Comparer les deux généalogies sur les **paires couvertes** ; « inconnu = 1,0 » n'est **pas** une distance | R² 0,256 contre 0,230 ; 154/154 hors script | ✅ ; V14, 9 dhātus, distance continue |
| **D16** | Lire le retrieval **par écriture d'abord**, puis séparer **sœur** et **famille lointaine** ; la « famille » est un mélange | sœur +0,448 (p = 0,002) contre famille +0,155 ; R² 0,474 → 0,631 ; J3.1 reproduit | ✅ ; l'échantillon 20 est sous-puissant |

### 3.3 La coordination

| # | décision | preuve | état / suite |
|---|---|---|---|
| **D9** | **Ne pas livrer `--rope` seul** ; valider `--rope --canal-dir` et `eval_longueurs.py --rope` ; promouvoir `rope_model.py` | 40,0658 seul contre 2,9726/2,7856 avec canal | ✅ ; porte propre 0,2856/0,3566 |
| **D10** | **Committer les 11 verdicts S tels quels** (option A), puis corriger les 9/16 référents | 7 acceptés / 4 exclus ; clone 8/4/11 ; 16 mappings | ⏳ ; sous-module + pointeur |
| **D11** | **Intégrer le POS API** (neuronal seul, drapeau, repli heuristique) ; split réel tenu à l'écart avant défaut | +8,49 pts ; réel +4,67 ; 0 refus POS | ⏳ ; route + split |
| **D12** | **A6.2 libre** ; métrique M1 = octets lus au lot 192 ; mesurer en **offload CPU** ; **A8.3b2** à nommer ; A8.3 **opt-in** | 37,2013 ; 54,5202 ; ÷15,51 / ÷7,08 | ⏳ ; rapport A6.2, harnais |

### 3.4 La méthode

| # | décision | preuve | état / suite |
|---|---|---|---|
| **D13** | **J5.1** : le produit est mesuré, l'intégration est bornée, la semaine **n'est pas close** | les fiches J1–J4 | ✅ ; J5.2 (passe, tag, release) |
| **D18** | Les fiches historiques portent un **encart qui pointe** vers l'état, **sans recopier** les valeurs | 19/19 encarts ; 38/38 liens ; 0 fiche périmée hors faux positifs | ✅ ; passe générique à faire |
| **D19** | **J10.1** : le chantier est **mesuré et écrit**, mais **pas clos** : le tag manque | 20/21 acceptations ; 84/81/3 ; tag absent | ✅ ; J14.1 (passe + tag) |
| **D20** | La **règle d'acceptation** est confirmée : un timeout avec acceptation verte = fait ; avec acceptation rouge = échec | J1.2/J2.2/J3.1/J8.1 sauvés ; J5.2 échoue | ✅ ; la prochaine boucle garde la règle |

## 4. Les échecs et les timeouts

### 4.1 Le tableau des runs

| tâche | durée | code | acceptation | commit | verdict | ce qui s'est passé |
|---|---:|---:|---|---|---|---|
| **J1.2** convention GV | 5 400,1 s | 124 | ✅ fiche + porte verte | **`92652984`** (13:44:53) | ✅ fait | timeout **après** le commit : le livrable et l'acceptation sont là |
| **J2.2** corpus commun | 5 400,1 s | 124 | ✅ fiche | **`c3467170`** (18:12:33) | ✅ fait | timeout **avant** le commit ; le commit est produit par J3.2, après coup |
| **J3.1** retrieval époque | 5 400,1 s | 124 | ✅ fiche | **`c3467170`** (18:12:33) | ✅ fait | même commit que J2.2 ; le retrieval est livré, le run a expiré |
| **J5.2** passe, tag, release | 5 400,1 s | 124 | ❌ tag absent / ✅ revue | **—** | ❌ **échec** | **le seul échec d'acceptation** : la passe 84/81/3 a été faite ailleurs (`2d6f5bff`), le tag n'existe pas |
| **J8.1** restitution v1 | 5 400,1 s | 124 | ✅ fiche | **`229098ec`** (03:23:33) | ✅ fait | timeout ; le commit est fait par J9.1, après coup |

**Le compte.** **21 lancements**, **5 timeouts** (J1.2, J2.2, J3.1, J5.2, J8.1), **1 échec
d'acceptation** (J5.2), **20 tâches faites** (dont J10.1). Le budget consommé au 14/11 03 h 46
est de **22 032 s** (hors J10.1).

### 4.2 Ce que les timeouts ont coûté — et ce qu'ils n'ont pas coûté

- **J1.2** a produit son commit **avant** le timeout ; le run a expiré pendant la rédaction ou
  les vérifications. Aucune mesure perdue.
- **J2.2** et **J3.1** ont produit leurs fiches, mais **pas leur commit** dans le run : le
  superviseur a vu `head_apres = 9c7f71dc` et les a marqués « timeout ». Le commit
  `c3467170` est arrivé à **18:12:33**, produit par le run suivant (J3.2). La formule
  « timeout après commit » est exacte pour J1.2 ; pour J2.2/J3.1, il faut dire **timeout avant
  le commit, commit récupéré par la tâche suivante**. Ce qui compte est l'**acceptation** :
  elle était verte, donc le travail n'était pas perdu.
- **J8.1** a expiré avant de committer ; J9.1 a trouvé le travail dans l'arbre, l'a vérifié et
  l'a committé (`229098ec`) avant de faire sa propre passe. C'est une **récupération**, pas une
  réussite du run.
- **J5.2** est le seul **vrai échec** : l'acceptation exigeait le tag `semaine-2026-11-14`, il
  n'existe pas. La passe complète a été faite dans un autre commit (`2d6f5bff`), mais un tag ne
  se déduit pas d'une passe : il se pose. J14.1 doit le reposer sous le nom
  `chantier-2026-11-14`.

### 4.3 La leçon

**Un timeout n'est pas un verdict ; l'acceptation en est un.** Le superviseur a été corrigé le
13/11 (`ced21933`) pour compter « fait » un timeout dont l'acceptation passe. Cette règle a sauvé
J1.2, J2.2, J3.1 et J8.1. Elle ne sauve pas J5.2, parce que son acceptation était **rouge**. La
leçon pour la suite : **mettre l'acceptation en premier**, la rendre vérifiable sans le run
(une fiche, un tag, une commande), et **ne pas confondre le commit avec la clôture**. Le budget
de 90 min est trop court pour les mesures longues (J7.1 : 26 min ; R : 42 min ; J8.1 : 90 min
expiré) : les tâches suivantes doivent soit réduire le périmètre, soit déclarer un timeout
explicite et un point de reprise.

## 5. Les rejets

### 5.1 Les nouveaux rejets (J6–J9)

| # | rejeté | chiffre | raison |
|---|---|---|---|
| **R22** | L'**adverbe final de temps hors de la SUB** (`g017`, règle demandée) | F1 **0,7901** (−0,0001) ; test **−0,0028** ; attachement **236/237** | corrige `g017`/`g005` en dev, casse `r264`/`r288` en test ; le gold se contredit |
| **R23** | La **variante étroite** « adverbe passé + SUB modale » | F1 **0,7909** ; **238/239** | elle ne casse rien, mais elle est réglée sur **2 cas de dev**, sans confirmation en test ; ce serait une convention déguisée en règle |
| **R24** | « `g017` est un **problème de règle** » | quatre SUB en adverbe final : 2 exclusions / 2 inclusions | c'est une **convention d'annotation** à trancher, pas un ajout de code |
| **R25** | « La **famille** est une variable unique » | famille **+0,1548** contre sœur **+0,4479** ; R² 0,474 → 0,631 | la famille est un **mélange** de sœurs et de familles lointaines ; il faut la décomposer |
| **R26** | « L'**échantillon 20** résout les sœurs » | sœurs **0,0583** contre autres-branches **0,0757** ; coefficient **+0,0154**, p = 0,078 | 12 paires de sœurs, dont **8 hors écriture** : défaut de puissance, pas effet nul |
| **R27** | « L'**époque** explique l'effet de famille » | UDHR mono-époque ; placebo **−0,0013** ; Bible **−0,034/siècle**, p = 0,19 | l'époque est constante dans l'UDHR ; le seul bras daté ne pèse pas |
| **R28** | « Le **miroir strict** doit monter avec la forme canonique » | strict **0,1087** inchangé ; strict sur canonique **1/46** | la v1 ne fabrique pas de surface ; s'il montait, elle recopierait la source |
| **R29** | « La **forme canonique** prouve la fidélité sémantique » | canonique **46/46** | c'est un **invariant de codec** (mêmes jetons, même ordre, présentation normalisée) ; les rôles ne sont pas jugés |
| **R30** | « L'**encart historique** doit recopier l'état courant » | 19/19 encarts ; 10 réécrits, 9 ajoutés | il deviendrait faux au commit suivant ; il doit **pointer**, pas répliquer |

### 5.2 Les rejets de J5.1 (rappel)

Les **21 rejets** de J5.1 restent valides : R1 adverbe large (0,7552), R2 objet hors GV
(0,7531), R3/R4 placebos, R5 « le schéma v2 prouve le sens », R6 corriger les 20 écarts,
R7 effet d'époque brut (0,238 contre 0,427 ; 0,710 contre 0,710), R8 filiation = famille,
R9 « inconnu = 1,0 », R10 les 9 dhātus mesurables, R11 V14 couvre 21 langues (3/21),
R12 `--rope` seul (40,0658), R13 « 11 verdicts = 11 acceptés », R14 hybride par classe
(p = 0,17), R15 baseline 0,8500, R16 « A6.2 bloquée faute de MoE », R17 A8.3b2 dans le graphe,
R18 `LOT=1/4`, R19 A8.3 par défaut, R20 miroir = 1,0, R21 les 20 hand généralisent. Le détail
est dans [`rapport-semaine.md`](rapport-semaine.md) § 4.

## 6. Ce qui reste pour la suite

| ligne | reste | prochaine action | bloquant | fiche |
|---|---|---|---|---|
| **J5.2 / J14.1** | passe complète, revue, **tag**, release | `toutes-les-portes.sh`, `revue_documentation.py`, tag `chantier-2026-11-14` | temps (~2 h) ; 3 rouges tolérées à relever | — |
| **B13 / `g017`** | **1 span** sans label ; convention d'adverbe non tranchée | trancher l'annotation (`g005`/`g017` vs `r264`/`r288`), puis rejouer la variante étroite sur un gold tenu à l'écart | gold 200+ ; 7B local interdit | [g017](rapport-g017.md) |
| **B13 / `s065`** | règle validée sur **un seul cas**, en dev, phrase synthétique | gold tenu à l'écart avec la même structure (`GN REL GV`) | gold | [s065](rapport-s065.md) |
| **B13 / objet du GV** | 75 FP / 51 FN ; 5 FP sujet | T132/T133, gold 200+ | gold | [convention](rapport-convention-gv.md) |
| **B13 / restitution** | gold de forme canonique ; analyseur insensible à la présentation | mesurer la **justesse** des rôles, pas seulement la cohérence ; v0.1 ponctuation | aucun | [restitution v1](rapport-restitution-v1.md) |
| **R0.7 / tagger** | route API derrière drapeau ; **split réel** tenu à l'écart | mesurer `crc32(id) % 3` ; si < +2 rouvrir et nommer le négatif ; si ≥ +5 route par défaut | ~0,07 $ / 1 000 phrases ; un run | [R](rapport-coordination-r.md) |
| **Panini / atomes** | **signature V14 des 21 langues** | projection multilingue + test invariance/cluster | pas de données V14 sur 21 langues | [atomes](rapport-atomes-niveaux.md) |
| **Panini / dhātus** | matrice **9 dhātus → 14 atomes** | publier la décomposition, projeter les 44 œuvres | aucune matrice publiée | [généalogie](rapport-genealogie-deux-faces.md) |
| **Panini / généalogie** | distance continue, corpus équilibré, retrieval neuronal, multi-époques, arêtes pondérées | une mesure par ligne (§ 7 de la fiche) | corpus | [généalogie](rapport-genealogie-deux-faces.md) |
| **Panini / J12** | §334 (114 textes, 655 paires) et les 44 œuvres ; corpus d'or CIC | J12.1 et J12.2 | corpus Panini (lecture seule) | — |
| **N2** | porte propre : **0,2856** en validation / **0,3566** en test ; `rope_model.py` dans `tools/` | appliquer le correctif, re-épingler, `porte-n2.sh` | GPU / runs N2 | [N2](rapport-coordination-n2.md) |
| **S** | committer les **11 verdicts** + pointeur ; corriger **9/16** référents ; `.gitmodules` en chemin absolu | commande § 3 de la fiche | accès au sous-module | [S](rapport-coordination-s.md) |
| **R** | (voir R0.7 / tagger) | — | — | [R](rapport-coordination-r.md) |
| **A** | rapport A6.2 ; M1/M2/M3 ; harnais A8.3b2 ; 18/19 pins ; cache Q4_K si besoin | D1–D8 de la fiche | GPU 16 GiB ; code Q4_K | [A](rapport-coordination-a.md) |
| **J9.1 / honnêteté** | la passe **générique** (tout chiffre d'arrivée antérieur à HEAD) | commencer par `rapport-pensee-v11.md`, `rapport-pensee-v9.md` | aucun | [passe](rapport-passe-honnetete.md) |

**La suite immédiate du plan.** **J11.1** rejoue les exemples de `docs/produit/exemples.md` — le
mandat porte encore **237/238**, il faut le lire avec l'état courant **238/238 labels** ;
**J11.2** ajoute `evaluer --par-langue` ; **J11.3** re-mesure les 50 textes ; **J11.4**
documente le schéma v2 ; **J12.1** attaque le §334 et les 44 œuvres ; **J12.2** écrit le
vérificateur CIC ; **J13.1** publie la table des mesures ; **J14.1** clôt par la passe et le tag
`chantier-2026-11-14`.

## 7. Ce qui pourrait rendre ce bilan faux

1. **Ce rapport agrège, il ne remesure pas.** Si une fiche change (ou si un chiffre est corrigé
   dans son JSON), le bilan devient faux sans qu'aucun calcul ne l'ait signalé. La source est
   toujours la fiche, pas ce résumé.
2. **Le HEAD est daté.** Les chiffres valent pour `81fc9ecf` ; un commit suivant (J11–J14) les
   change. Les deux bases sont données : vivant **612** (F1 0,7902 ; 238/239) et gelé **602**
   (F1 0,7882 ; 234/239).
3. **Les gains B13 sont in-sample.** La convention du sujet est lue dans le gold (712/712 GV)
   puis appliquée au gold ; `s065` est un seul cas, en dev. Le +0,0369 n'est pas une
   généralisation.
4. **Le gold est une convention.** La relative zéro est annotée une fois, l'adverbe final est
   contradictoire (`g005`/`g017` contre `r264`/`r288`). Un autre corpus annoté autrement
   inverserait certains signes.
5. **Le tagger est un run unique.** Un seul jour, un seul alias (`deepseek-chat` servi par
   `deepseek-flash`), température 0 mais API non déterministe au bit près ; le 612 est tiré par
   les 160 synthétiques ; le réel 432 ne gagne que +4,67 ; le split réel n'est pas fait.
6. **L'intégration Panini est de surface.** Les n-grammes de caractères capturent l'orthographe
   et les cognates, pas le sens ; le corpus est **mono-époque** (1948), **mono-genre**
   (déclaration), 21 textes, 5 familles, 10 écritures ; le signal de famille est porté par
   **2 ou 3 paires** sur 21 langues, et par **60 paires** sur `LANG_TREE`.
7. **« Sœur » est une convention.** LCA ≥ 3, hors ancêtre/descendant ; la variante stricte
   (LCA ≥ 4) donne des chiffres plus forts. Les paires ne sont pas indépendantes ; l'échantillon
   20 n'est pas aléatoire.
8. **N2 mesure une validation, pas une porte.** 2,7856 est le meilleur des quatre longueurs en
   validation ; le test à 1 024 est 2,8566 et manque 0,3566. Une seule graine, un seul run, une
   seule machine.
9. **S n'est vrai que dans le working tree.** Un clone à `523d8c1` voit 8 verdicts / 4 acceptés /
   11 candidats sans verdict. Le `.gitmodules` en chemin absolu peut empêcher un clone sur une
   autre machine.
10. **La passe complète n'est pas la clôture.** 84 portes, 81 vertes, 3 rouges **tolérées** ;
    l'autotest 183/183 n'est pas la passe ; le tag n'existe pas. J14.1 doit refaire la passe et
    taguer **si** le relevé est conforme.
11. **Les compteurs bougent.** Le dépôt a des sessions concurrentes ; 723 fiches / 817 JSON au
    HEAD, 724 / 818 après ce bilan. L'état `en-cours` est la source du compte, pas ce rapport.

## 8. Fichiers

- **Nouveaux** : `reports/rapport-bilan-chantier.md` (ce rapport),
  `reports/rapport-bilan-chantier.json`.
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
- **Relus, J5** : [`rapport-semaine.md`](rapport-semaine.md) + `rapport-semaine.json`.
- **Relus, J6–J9** : [`rapport-g017.md`](rapport-g017.md) + `pensee-g017.json` ;
  [`rapport-s065.md`](rapport-s065.md) + `pensee-s065.json` ;
  [`rapport-retrieval-familles.md`](rapport-retrieval-familles.md) + `retrieval-familles.json` ;
  [`rapport-restitution-v1.md`](rapport-restitution-v1.md) + `pensee-restitution-v1.json` ;
  [`rapport-passe-honnetete.md`](rapport-passe-honnetete.md) + `passe-honnetete.json`.
- **Mis à jour** : [`docs/pilotage/semaine-autonome.md`](../docs/pilotage/semaine-autonome.md)
  (l'état du chantier et le bilan) ; [`docs/pilotage/en-cours.md`](../docs/pilotage/en-cours.md)
  (compteurs et ligne J10.1) ; [`docs/pilotage/roadmap.md`](../docs/pilotage/roadmap.md) (la
  ligne B13 et la suite) ; [`reports/README.md`](README.md) (fiches courantes).
- **Non modifiés** : les fiches et JSON ci-dessus (sauf ce rapport et son JSON), `tools/`,
  `drave-core/`, `data/`, `work/` ; le journal est archivé par le hook, il n'est pas rédigé ici.

## 9. Verdict

**J10.1 est fait.** Le chantier a **20 tâches sur 21** qui passent l'acceptation. Le produit a un
gain mesuré (**F1 0,7533 → 0,7902**, **attachement 236 → 238 labels**, **POS inchangée**,
**schéma v2**, **restitution v1**), le tagger API a une mesure et une décision (**0,9475,
+8,49, intégrer**, réserve sur le réel 432), l'intégration Panini a **cinq briques** mesurées et
**bornées** (table 14/14, corpus 418/438, retrieval J3.1, généalogie J3.2, familles J7.1), et la
coordination N2/S/R/A est **datée**. Les **échecs** sont nommés : **5 timeouts** (J1.2, J2.2,
J3.1, J5.2, J8.1), dont **4 récupérés** par l'acceptation ou par la tâche suivante, et **1 vrai
échec** (J5.2, le tag absent). Ce qui reste est nommé : `g017` (convention), `s065` (hors
échantillon), le split réel du tagger, la signature V14 des 21 langues, la porte N2, le commit S,
le rapport A6.2, la passe générique d'honnêteté, et **J14.1** (passe + tag
`chantier-2026-11-14`). Le chantier est **mesuré et écrit** ; il n'est **pas clos**.
