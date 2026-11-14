# J13.1 — la table des mesures : F1 0,7533 → 0,7902, attachement 236/237 → 238/238, base 612/602

> **Ligne de roadmap** : **B13** (le produit), **R0.7** (le bloc langue), **L**, **Panini**, **N2**, **S**, **R**, **A** · **Tâche** : J13.1 · **Date** : 2026-11-14 · **Verdict** : ✅
>
> **Ce que ce tableau est.** La **table consolidée** des mesures du chantier, de J1.1 à J12.2 :
> POS, F1, attachement, couverture, spans, le produit (schéma, restitution, robustesse, exemples,
> langues), le tagger et Panini (table, corpus, retrieval, généalogie, familles, §334, CIC) —
> **avant/après**, avec la **base** (612/602), les **commits** et les **contrôles négatifs**. Il
> **ne remplace pas** les fiches : il les ordonne et il nomme, pour chaque ligne, la fiche qui la
> porte. **Aucune mesure nouvelle** n'est revendiquée, sauf la **re-mesure de la base** au HEAD
> `b20a4c31` (`drave evaluer` sur le vivant 612 et le gelé 602), qui fixe les valeurs « après » du
> cœur produit et montre l'écart entre les deux bases.
>
> **Le chiffre.** Sur le **vivant 612** : **POS 0,8625** (inchangée), **F1 0,7533 → 0,7902**
> (**+0,0369**), **attachement 236/237 → 238/238 labels** (238/239 cibles, **0,9958**),
> **couverture 0,9916 → 0,9958**, **spans sans label 2 → 1** (`r035` réglé, `g017` reste une
> convention). Sur le **gelé 602** : **F1 0,7882**, **attachement 234/239** — la même mesure, une
> autre base. Le **tagger API** vaut **0,9475 (+8,49 pts)** ; le **produit** gagne le **schéma v2**,
> la **restitution v1** (canonique 46/46, strict 0,1087), les **50 textes** (0 plantage, 50/50 v2),
> les **5 exemples** (4 corrigés) et le **détail fr/en**. **Panini** est mesuré et borné : table
> **14/14**, corpus **418/438**, retrieval à porte d'écriture, généalogie **154/154** hors script,
> familles (**sœurs 0,619 vs 0,0445**), §334 (**H0 0,909139 / 0,906307**, date **0,0089** après
> topo, V150 β **−0,006 ≠ +0,138**) et CIC (**42/42**, **36/36** preuves altérées rejetées).
>
> **Dispositif** : `python3 tools/drave.py evaluer --json` et `python3 tools/drave.py evaluer
> --gold --json` pour la base ; les fiches et JSON de `reports/` pour les autres lignes. Le
> **commit mesuré** est `b20a4c31` (J12.2). **JSON** : [`tableau-mesures.json`](tableau-mesures.json).
>
> **Comment lire.** Chaque ligne porte sa **base**, son **avant**, son **après**, son **Δ**, un
> **contrôle négatif** (le détail est au § 8), son **commit** et sa **fiche**. Les valeurs
> « avant » sont **publiées** par la fiche ; les valeurs « après » du cœur produit sont
> **re-mesurées** au HEAD (sauf P10, publiée), les autres sont **publiées** (tagger, Panini,
> livrables). Un chiffre sans base n'est pas lu.

## 1. La base — 612 et 602

La re-mesure au HEAD `b20a4c31` donne deux jeux de chiffres, et **les deux sont vrais** : ils ne
portent pas sur le même gold. Le **vivant 612** est le gold qui grandit (hand + réel + synthétique) ;
le **gelé 602** est la copie figée pour les portes à nombre absolu.

| gold | phrases | jetons | POS | F1 | tête | labels / cibles | exact | couverture | span exact |
|---|---|---|---|---|---|---|---|---|---|
| **vivant 612** | 612 | 3179 | **0,8625** | **0,7902** | 0,9029 | 238/239 | 238 | 0,9958 | 1,0 |
| **gelé 602** | 602 | 3141 | **0,8625** | **0,7882** | 0,9025 | 234/239 | 234 | 0,9791 | 1,0 |

**Ce que l'écart dit.** La POS est **identique** (0,8625), le F1 perd **0,0020** et l'attachement
**4 labels** (234/239 contre 238/239). Le **top-k** vaut **236/239 (0,9874)** sur 612 et
**232/239 (0,9707)** sur 602 ; la vue linéaire vaut **0,8144** sur 612 et **0,8127** sur 602. Le
contrôle négatif est le même sur les deux : une cible exacte tirée au hasard vaut **1,67 %**
(239 cibles, graine 0). Une fiche qui publie « 0,79 » sans dire **612 ou 602** peut donc tromper
même avec un chiffre exact — c'est la raison de la colonne « base » dans tout le tableau.

**Commandes et commit.**

```bash
python3 tools/drave.py evaluer --json        # vivant 612 : 0,7902 ; 238/239 ; 1,0
python3 tools/drave.py evaluer --gold --json # gelé 602  : 0,7882 ; 234/239 ; 1,0
```

Le commit mesuré est `b20a4c31` ; la re-mesure est faite au HEAD de J13.1, avant l'écriture de
cette fiche. Le **602** ne remplace pas le **612** : il le **contrôle**.

## 2. Le produit — POS, F1, attachement, couverture, spans

| # | mesure | base | avant | après | Δ | contrôle négatif (résumé) | commit · fiche |
|---|---|---|---|---|---|---|---|
| P01 | POS heuristique | 612 · 3 179 jetons | 0,8625 | **0,8625** | **0** | 0 jeton changé sur 3 179 (diff token à token) | J1.1 `25a6c0ff` · J1.2 `92652984` · J6.2 `b6e474dc` · [r035](rapport-r035.md) · [s065](rapport-s065.md) |
| P02 | POS heuristique | 602 · 3 141 jetons | — (non publié sur 602) | **0,8625** | — | même exactitude ; 3 141 jetons (38 de moins) ; ouvert 0,7914 contre 0,7918 | HEAD `b20a4c31` · [passe-honnetete](rapport-passe-honnetete.md) |
| P03 | F1 syntagmes (vue alternative) | 612 · 239 cibles | 0,7533 (P 0,7239 / R 0,7853 ; 1 463/558/400) | **0,7902** (P 0,7860 / R 0,7944 ; 1 480/403/383) | **+0,0369** | 183/183 ; placebo sujet 0,7758 ; adverbe large rejeté (test 0,7656 < 0,7663) ; test non utilisé pour choisir la règle (in-sample) | J1.1 `25a6c0ff` · J1.2 `92652984` · [convention GV](rapport-convention-gv.md) |
| P04 | F1 syntagmes (vue alternative) | 602 · 239 cibles | — (non publié sur 602) | **0,7882** (P 0,7818 / R 0,7946 ; 1 455/406/376) | −0,0020 vs 612 | 234 labels au lieu de 238 ; même span exact 1,0 ; plancher aléatoire 1,67 % | HEAD `b20a4c31` · [passe-honnetete](rapport-passe-honnetete.md) |
| P05 | F1 dev / test | 612 · 422 dev / 190 test | 0,7476 / 0,7663 | **0,7875 / 0,7962** | **+0,0399 / +0,0299** | le test n'a pas choisi la règle ; il ne la contredit pas | J1.2 `92652984` · [convention GV](rapport-convention-gv.md) |
| P06 | F1 vue linéaire (partition `filtrer`) | 612 · 224 labels | 0,8120 (223/224 labels) | **0,8144** (224/224 labels ; couverture 0,9372) | **+0,0024** | filtre `filtrer` : 0 chevauchement ; attachement 224/224 | J1.2 `92652984` · [convention GV](rapport-convention-gv.md) |
| P07 | Attachement exact / labels | 612 · 239 cibles | 236/237 labels (236/239 cibles ; couverture 0,9916) | **238/238 labels** (238/239 cibles ; couverture 0,9958) | **+2 labels exacts** | 0 cible perdue, 0 span perdu sur 239 cibles | J1.1 `25a6c0ff` · J6.2 `b6e474dc` · [r035](rapport-r035.md) · [s065](rapport-s065.md) |
| P08 | Attachement exact / labels | 602 · 239 cibles | — (non publié sur 602) | **234/239 labels** (0,9791) | −4 labels vs 612 | 0 span perdu ; 4 cibles non couvertes | HEAD `b20a4c31` · [passe-honnetete](rapport-passe-honnetete.md) |
| P09 | Couverture (labels / 239) | 612 · 239 cibles | 0,9916 (237/239) | **0,9958** (238/239) | **+0,0042** | dénominateur 239 ; le 239e span, g017, n'a pas de label | J1.1 `25a6c0ff` · J6.2 `b6e474dc` · [r035](rapport-r035.md) · [s065](rapport-s065.md) |
| P10 | Spans sans label | 612 · 239 cibles | **2** (r035, g017) | **1** (g017) | **−1** | r035 désormais prédit (rejeu J11.1) ; g017 reste une convention d'adverbe non tranchée | J1.1 `25a6c0ff` · J6.1 `64d9dd23` · [r035](rapport-r035.md) · [g017](rapport-g017.md) · [exemples](rapport-exemples-rejoues.md) |
| P11 | Exactitude sur les spans | 612 · labels | 0,9958 (236/237) | **1,0** (238/238) | **+0,0042** | 238 labels sur le bon span ; g017 n'a pas de label | J6.2 `b6e474dc` · [s065](rapport-s065.md) |
| P12 | Top-k attachement (mesure secondaire) | 612 · 239 cibles | — (non publié) | 236/239 (0,9874) ; 236/238 sur les spans (0,9916) | — | 3 cibles hors top-k ; le top-k n'est pas le taux exact | HEAD `b20a4c31` · [s065](rapport-s065.md) |

**Trois lectures, à tenir ensemble.**

- **La POS ne bouge pas.** Les règles J1.1, J1.2, J6.1 et J6.2 sont des règles de **syntagmes** ou
  d'**attachement** ; le diff token par token donne **0 token changé** sur 3 179. Ce n'est pas un
  échec : c'est le contrôle qui dit que les gains ne viennent pas d'une dérive des étiquettes.
- **Le gain F1 se décompose** : `r035` apporte **+0,0016** (0,7533 → 0,7549), la convention des GV
  **+0,0353** (0,7549 → 0,7902). Les deux règles sont des règles de **syntagmes** ou
  d'**attachement** ; aucune ne touche la POS. Le gain est **in-sample** : la convention du sujet
  est lue dans le gold (712 GV sur 712 commencent par un `VERB`, un `AUX` ou un `ADV` de négation)
  puis appliquée au gold ; le test ne la choisit pas, il ne la contredit pas non plus.
- **Le dénominateur compte.** 238/238 est le taux sur les **labels** ; 238/239 (0,9958) est le taux
  sur les **cibles**. Le 239e span, `g017`, n'a pas de label : c'est le **1 span** de l'état
  courant, et il ne se règle pas par une règle de surface. L'exactitude sur les spans (1,0) ne dit
  pas qu'il ne manque rien : elle dit que les 238 labels sont sur le bon span.

## 3. Le tagger POS — la seule mesure qui change l'ordre de grandeur

| # | mesure | base | avant | après | Δ | contrôle négatif (résumé) | commit · fiche |
|---|---|---|---|---|---|---|---|
| T01 | POS API (tagger neuronal seul) | 612 · 3 179 jetons | 0,8625 (2 742/3 179) | **0,9475** (3 012/3 179) | **+8,49 pts** [7,23 ; 9,74] | majoritaire 0,2145 ; classe fréquente 0,2491 ; permutation 0,1667 ; uniforme 0,0833 ; McNemar 344/74, p = 1,1 × 10⁻⁴² | J4.3 `a934d779` · [R](rapport-coordination-r.md) |

| corpus | heuristique | API | Δ | IC95 bootstrap |
|---|---:|---:|---:|---:|
| **612** | 0,8625 (2 742/3 179) | **0,9475 (3 012/3 179)** | **+8,49 pts** | **[+7,23 ; +9,74]** |
| réel 432 | 0,8893 (2 112/2 375) | **0,9360 (2 223/2 375)** | **+4,67 pts** | [+3,45 ; +6,01] |
| synth 160 | 0,7682 (537/699) | **0,9828 (687/699)** | +21,46 pts | [+18,80 ; +24,15] |
| hand 20 | 0,8857 (93/105) | **0,9714 (102/105)** | +8,57 pts | in-sample |

**La réserve est décisive.** Le **612** agrège trois corpus : le **réel 432** ne gagne que
**+4,67 pts** (l'IC contient +5), le **synth 160** gagne **+21,46** et tire le 612 au-dessus de
+5, et les **20 hand** sont **in-sample**. La règle `≥ +5 → intégrer` s'applique au 612 :
**intégrer**, mais le **split réel tenu à l'écart** est la prochaine mesure qui peut faire
descendre le chiffre sous +5, voire sous +2. La baseline publiée **0,8500** est **datée** : la
référence du HEAD est **0,8625** ; comparer à 0,8500 surestime le gain de **1,26 pt**.

## 4. Le produit — contrat, restitution, robustesse, exemples, langues

| # | mesure | base | avant | après | Δ | contrôle négatif (résumé) | commit · fiche |
|---|---|---|---|---|---|---|---|
| Q01 | Schéma d'annotation | 612 annotations · 2 schémas | v1 | **v2** (`meta.partition` 4 champs, `meta.alternative` 10 champs) | +14 champs additifs | 26 cas / 0 échec ; 1 836 annotations / 0 échec ; v2 refuse v1 ; v1 refuse v2 ; mutation d'un champ obligatoire refusée | J1.3 `9a259953` · J11.4 `febfdfff` · [schéma v2](rapport-schema-v2.md) · [doc v2](rapport-schema-v2-doc.md) |
| Q02 | Restitution v0 | 50 textes · 46 annotations · 4 refus | — (pas de restitution) | surface **46/46 = 1,0** ; miroir strict **5/46 = 0,1087** | — | sans correctif C 45/46 ; mélange 0/46 exact et 46/46 détecté ; troncature 0/46 exact et 46/46 détecté | J1.4 `8eb0cc49` · [v0](rapport-restitution-v0.md) |
| Q03 | Restitution v1 | 46 annotations | v0 : strict 0,1087 ; canonique non mesuré | canonique **46/46 = 1,0** ; strict **0,1087** inchangé ; structure 395 segments / 395 rôles / 315 cibles ; stabilité **18/46 = 0,3913** | — | strict sur canonique 1/46 = 0,0217 ; mélange/troncature 0/46 exact, 46/46 détecté ; rôles retirés 395 ; cibles retirées 315 ; clé changée 43/43 | J8.1 `229098ec` · [v1](rapport-restitution-v1.md) |
| Q04 | Exemples de la doc rejoués | 5 blocs de `docs/produit/exemples.md` | 4 blocs périmés (06/11) ; r035 = échec connu | 5/5 reproduits ; **4 corrigés**, 1 identique ; r035 prédit (`REL [9:24] → film`) | 4/5 corrigés | mutation d'un token dans une copie de la doc : 4/5 détectée | J11.1 `84e393bb` · [exemples](rapport-exemples-rejoues.md) |
| Q05 | Mesure par langue | 612 · fr 402 phrases / 2 031 tokens / 151 cibles ; en 210 / 1 148 / 88 | global seul : POS 0,8625 ; F1 0,7902 ; att. 238/239 | fr POS **0,8159** / F1 **0,7475** / att. **151/151** ; en POS **0,9451** / F1 **0,8656** / att. **87/88** | global inchangé | plancher aléatoire 1,99 % fr / 2,27 % en / 1,67 % global ; non-régression du global ; sommes 612 | J11.2 `09e54143` · [par langue](rapport-evaluer-langue.md) |
| Q06 | Robustesse — 50 textes libres | 50 textes A26 · 46 annotations · 4 refus | A26 (06/11) : 4 refus code 1 sans JSON ; 0/46 champs 8 ; 107 chevauchements alternative ; 0 filtrer | **0 plantage** ; 50/50 JSON valide ; 50/50 8 champs ; 50/50 schéma v2 ; 4 refus code 3 ; **115** chevauchements alternative (21/46) / **0** filtrer (313 segments) ; restitution 46/46, strict 0,1087 ; CLI médian 159,2 ms, API 2,7 ms | +8 chevauchements alternative (107 → 115) ; 8 champs 0 → 50/50 ; refus code 1 → 3 | schéma v1 lue ; v2 refuse v1 ; champ manquant refusé ; chevauchement injecté détecté ; filtrer non vide ; mélange/troncature 46/46 détectés ; rôles 395, cibles 315 ; 0 span hors texte / 4 827 | J11.3 `55bde5c5` · [robustesse](rapport-robustesse-semaine.md) |
| Q07 | Schéma v2 documenté | 612 annotations · 2 schémas | v2 non documenté | 4 champs partition + 10 champs alternative documentés ; 6 cas / 0 échec ; --gold 20 → 26 cas / 0 échec ; 612/612 v2 + 612/612 v1 | — | v2 refuse v1 612/612 ; v1 refuse v2 612/612 ; mutation d'un champ obligatoire refusée ; 146 groupes / 437 porteurs / 930 alternatives cohérents avec B13 | J11.4 `febfdfff` · [doc v2](rapport-schema-v2-doc.md) |

**Ce que ces lignes ajoutent au cœur.**

- **Le schéma v2 est additif** : `meta.partition` (4 champs) et `meta.alternative` (10 champs)
  n'existent que sur un syntagme qui appartient à un groupe de chevauchement ; v1 reste lue. Les
  contrôles croisés refusent la version adverse (612/612 dans les deux sens) et la mutation d'un
  champ obligatoire.
- **La restitution v0 est un codec de surface, pas un décodeur** : 46/46 surfaces exactes, mais le
  miroir strict reste **0,1087**. La v1 ajoute une lecture **structurelle** (395 segments, 395
  rôles, 315 cibles) exacte **contre la source canonisée**, et **tombe à 1/46 contre la source
  brute** — c'est le contrôle qui montre qu'elle ne recopie pas la surface. La stabilité
  structurelle reste **18/46** : le lexique est stable 46/46, la structure ne l'est pas.
- **Les 50 textes libres** passent de **0/46 champs 8** (A26) à **50/50**, de **4 refus code 1
  sans JSON** à **4 refus code 3 avec JSON**, et de **107 à 115** chevauchements en `alternative`
  (le code a changé, pas le compteur). En `filtrer`, **313 segments** et **0 chevauchement**.
- **Les 5 exemples** de la doc sont reproduits ; **4 corrigés**, **1 identique** ; `r035` — l'ancien
  échec connu — est désormais prédit. La mesure vérifie que **la doc dit ce que le code fait**, pas
  la qualité du produit.
- **Le détail par langue** ne change pas le global : **fr** POS 0,8159 / F1 0,7475 / att. 151/151 ;
  **en** POS 0,9451 / F1 0,8656 / att. 87/88. L'anglais est devant, mais il est **100 % réel** quand
  le français ajoute **160 synthétiques** : le confondant de composition reste.

## 5. Panini — sept briques, sept contrôles

| # | mesure | base | avant | après | Δ | contrôle négatif (résumé) | commit · fiche |
|---|---|---|---|---|---|---|---|
| N01 | Table atomes ↔ niveaux | 14 atomes × 8 niveaux | 0 ligne mesurée | **14/14 lignes** ; 33 paires ∣r∣ ≥ 0,5 ; 4 composantes > 1 ; 3 premières = **80,7 %** de la variance (6,967 / 2,845 / 1,491) | 14 lignes | hypothèse, pas corrélation ; protocole CLR/permutations/BH/split-half ; aucune correspondance atome ↔ niveau mesurée | J2.1 `9c7f71dc` · [atomes](rapport-atomes-niveaux.md) |
| N02 | Corpus commun UDHR | 532 langues Panini / 456 Drave / 438 appariables | 0 texte commun | 21 textes ; **418/438 paires exactes (95,4 %)** ; 20 écarts de surface exclus ; 5 familles, 10 écritures, 42 phrases, 3 603 caractères | 418 exactes | 8/8 (6 rejets + 2 témoins) ; altérer un caractère casse l'égalité ; appariement croisé rejeté | J2.2 `c3467170` · [corpus](rapport-corpus-commun.md) |
| N03 | Retrieval à époque contrôlée | B7 4 004 paires ; UDHR 420 ; Bible 132 | 0 mesure | B7 top-1 **0,138** vs 0,055 ; UDHR **0,049** vs 0,0333 ; Bible **0,293** vs 0,001 ; Bible écriture **+0,609** [0,529 ; 0,702], famille **+0,181** [0,106 ; 0,253], date **−0,034/siècle** [−0,075 ; +0,009], p = 0,19, R² 0,763 ; à écriture contrôlée **0,710 vs 0,710** | — | cibles permutées ; années permutées ; candidats mélangés ; le brut 0,238 vs 0,427 est un effet de composition | J3.1 `c3467170` · [retrieval](rapport-retrieval-epoque.md) |
| N04 | Généalogie à deux faces | 210 paires / 21 langues / 15 labelisées | 0 confrontation | **154/154** hors script au hasard exact (MRR 0,1332, top-1 0,0333) ; 56 même script MRR 0,1999 ; 8 même famille + script MRR 0,3853 (7/8 au-dessus) ; couverture Panini 5/21, UDHR 15/21, Glottolog 21/21 ; 15/15 familles, 14/15 branches exactes, Spearman 0,657, Pearson 0,918 ; R² 0,256 Panini vs 0,230 Glottolog sur 105 paires | — | permutations de labels p = 0,006/0,019 ; chemins Glottolog p = 0,019 ; LOO ; split-half atomes | J3.2 `c2e629b3` · [généalogie](rapport-genealogie-deux-faces.md) |
| N05 | Retrieval par famille | 532 textes (445 langues) ; LANG_TREE 25 ; échantillon 20 ; union 39 | J3.1 : famille +0,0556, non décomposée | famille **66,1 %** vs 10,3 % ; sœur **26,1 %** vs 2,5 % ; LANG_TREE sœurs **0,619** vs **0,0445** (13,9× ; Δ +0,574 [0,490 ; 0,655] ; coefficient +0,448, p = 0,002, contre +0,213 pour l'écriture) ; échantillon 20 nul (0,0583 vs 0,0757 ; +0,0154, p = 0,078) ; J3.1 reproduit à l'identique (écart 0) | — | permutations 1 000/500 ; requêtes permutées ; LOO ; placebo de dates ; UDHR mono-époque ; Bible −0,034/siècle p = 0,19 | J7.1 `d31e8788` · [familles](rapport-retrieval-familles.md) |
| N06 | §334 et 44 œuvres | 655 lignes = 495 paires uniques (160 doublons, 7 auto-paires) ; 48 textes ; 44 signatures ; 488 paires d'inférence | 0 mesure ; annonce 114 textes, 655 paires, 102 sources | H0 **R² 0,909139** (655) / **0,906307** (488) ; date seule 0,258 ; date après topo **0,0089** (p = 0,86 ; β std −0,035) ; filiation **61,4 %** vs 50,0 % (p = 0,0492 ; Holm 0,128) ; époque **56,8 %** vs 53,8 % (p = 0,373) ; année intra-tradition **R² 0,042** (p = 0,0086 ; Holm 0,034) ; V150 β date **−0,006 ≠ +0,138** (p = 0,093) | — | tradition permutée dans des tranches de 250 ans ; années permutées dans chaque tradition ; signatures permutées (2 000) ; doublons retirés ; eng–eng seules (24 œuvres, 276 paires) ; Holm-Bonferroni 4 tests | J12.1 `bb68b820` · [§334](rapport-panini-334.md) |
| N07 | Corpus d'or CIC | 42 entrées (36 acceptées, 6 rejetées) ; 3 defs, 21 consts ; 46 714 octets | vérificateur Panini seul | **42/42 verdicts** ; **42/42 empreintes** ; **42/42 sérialisations** ; 36/36 preuves altérées rejetées ; **1 020/1 020** mutations de eq(2,2) rejetées ; non-trivialité : accepte-tout 6 désaccords, rejette-tout 36 ; 21 tests ; porte verte | — | altérer le dernier octet ; mutations exhaustives ; accepte-tout/rejette-tout ; sha256 du corpus ; copie byte-identique | J12.2 `b20a4c31` · [CIC](rapport-cic-verificateur.md) |

**Ce que les chiffres portent, et ce qu'ils ne portent pas.**

- **La table atomes ↔ niveaux est une grille de lecture, pas une mesure.** 14 atomes, 8 niveaux,
  14 lignes ; **33 paires** d'atomes à ∣r∣ ≥ 0,5 en brut, **4 composantes > 1**, les trois premières
  à **80,7 %** de la variance. **Aucune correspondance atome ↔ niveau n'est mesurée** : les trois
  candidats directs (№ → mot, ⊗ → pos, ⊞ → document) restent à tester.
- **Le corpus commun est étroit mais vérifié.** 532 langues Panini, 456 Drave, **453 communes**,
  **438 appariables**, **418 exactes (95,4 %)** ; **20 écarts de surface exclus, pas corrigés**.
  21 textes (20 strates + français pivot), **5 familles, 10 écritures, 42 phrases, 3 603
  caractères** ; 8/8 contrôles. Le corpus est **mono-époque** (1948), **mono-genre** (déclaration),
  article 1 seulement.
- **Le retrieval est de surface, et l'écriture est la porte.** Bible : écriture **+0,609**
  [0,529 ; 0,702], famille **+0,181** [0,106 ; 0,253], date **−0,034/siècle** [−0,075 ; +0,009],
  **p = 0,19**, R² **0,763** ; à écriture contrôlée, contemporains et décalés sont au **même
  niveau : 0,710 contre 0,710**. Le renversement brut **0,238 contre 0,427** est un **effet de
  composition**.
- **La généalogie à deux faces ne mesure pas le même objet.** Panini `LANG_TREE` couvre **5/21**
  langues (200/210 paires « inconnu »), les métadonnées UDHR **15/21**, Glottolog **21/21** ;
  **154/154** paires hors script au **hasard exact** (MRR 0,1332, top-1 0,0333) ; là où les deux
  faces se rencontrent : **15/15 familles**, **14/15 branches** au nœud exact, Spearman **0,657**,
  Pearson **0,918** ; sur les 105 paires couvertes, R² **0,256** (Panini) contre **0,230**
  (Glottolog). La face atomes n'est pas disponible (V14 3/21).
- **Le renversement de J7.1** : sur les 25 langues `LANG_TREE`, les sœurs valent **0,619** contre
  **0,0445** pour les familles différentes (**13,9×**, Δ **+0,574** [0,490 ; 0,655], coefficient
  de sœur **+0,448**, p = 0,002, contre **+0,213** pour l'écriture). Sur l'**échantillon 20**, le
  contraste est **nul** : sœurs 0,0583 contre 0,0757, coefficient **+0,0154**, p = 0,078. J3.1 est
  **reproduit à l'identique** (écart 0) : son coefficient de famille (+0,0556) n'était pas faux,
  il était **sous-dimensionné**.
- **Le §334 ne sépare pas l'époque de la filiation.** La H0 se reproduit (**R² = 0,909139** sur
  655 lignes, **0,906307** sur 488 paires uniques non auto) ; la date seule explique **0,258**,
  mais n'ajoute que **0,0089** après la topologie (p = 0,86 ; β standardisé −0,035). Le plan est
  **colinéaire** : 180 paires de même tradition ont **28,7 ans** d'écart en moyenne (max 230), les
  308 paires inter-traditions **1 189 ans** (**136** à ≤ 100 ans). Le contraste de filiation à
  date fixe (**Δ = −0,166**, p = 0,0005) **disparaît à surface contrôlée** (**Δ = −0,135** contre
  un null de **−0,129**, p = 0,335). Sur les 44 signatures, le retrieval brut donne **61,4 %** de
  même tradition (hasard 22,4 %) et **56,8 %** de voisins à ≤ 50 ans (hasard 22,8 %) ; les
  contrôles croisés ramènent la filiation à **50,0 %** (p = 0,0492, **Holm 0,128**) et l'époque à
  **53,8 %** (p = 0,373). Seule une **petite** prédiction d'année intra-tradition survit
  (**R² = 0,042**, p = 0,0086, **Holm 0,034**). Le β époque **+0,138** de la v150 **n'est pas
  reproduit** : sur **374** paires, le coefficient de date est **négatif** (**−0,006**) et non
  significatif (p = 0,093).
- **Le corpus d'or CIC est portable et rejouable hors de Panini.** Un noyau CIC-lite réécrit côté
  Drave, sans importer le code de Panini, rend **42/42** verdicts (**36** acceptés, **6** rejetés),
  **42/42** empreintes `sha256(preuve || type)` et **42/42** sérialisations canoniques. Altérer le
  dernier octet des **36** preuves acceptées les fait **36/36** rejeter ; les **1 020** mutations
  d'un octet de `eq(2,2)` sont **1 020/1 020** rejetées ; un noyau « accepte tout » et un noyau
  « rejette tout » échouent (respectivement **6** et **36** désaccords). Le corpus n'exerce que
  **20** des **39** étiquettes du format : c'est un **verrou de portabilité**, pas une preuve de
  correction du noyau Panini.

## 6. Les portes et la clôture

| # | mesure | base | avant | après | Δ | contrôle négatif (résumé) | commit · fiche |
|---|---|---|---|---|---|---|---|
| G01 | Porte produit | 183 tests | 183/183 (J6.2) | **183/183** | 0 | fixtures d'attachement à 238/238 ; 13 contrôles (16 + 8 + 4 + 22 tests) | J6.2 `e4288023` · [s065](rapport-s065.md) |
| G02 | Passe complète | 84 portes | 84 portes, 81 vertes, 3 rouges tolérées (`indice`, `melange`, `sessions`) [2d6f5bff] | **à refaire en J14.1** (aucune passe nouvelle en J13.1) | — | `tools/toutes-les-portes.sh` ; verdict `awk '$2 != 0'` ; rouges tolérées listées dans `references-non-regression.md` | passe `2d6f5bff` · [rouges tolérées](../docs/pilotage/references-non-regression.md) |
| G03 | Tag de clôture | — | absent (J5.2 échec) | **absent** (J14.1 doit le poser) | — | `git tag -l 'chantier-2026-11-14'` | — · [bilan](rapport-bilan-chantier.md) |

**Ce que la passe ne dit pas.** **81 vertes sur 84** ne sont pas « toutes vertes » : trois rouges
sont **tolérées** parce qu'elles sont structurelles ou de coordination (`indice`, `melange`,
`sessions` du hub), pas parce qu'elles sont inoffensives. Le tag n'existe pas : J5.2 a été lancé, a
expiré, et son acceptation était rouge. **J14.1** doit refaire la passe, relever les rouges et
taguer **si** le relevé est conforme à `references-non-regression.md`.

## 7. Les commits du chantier

| tâche | commit | date | objet | statut |
|---|---|---|---|---|
| J1.1 | `25a6c0ff` | 2026-11-07 | r035 : relative zéro ; exact 236 → 237 ; POS inchangée | fait |
| J1.2 | `92652984` | 2026-11-07 | convention des GV : F1 0,7549 → 0,7902 ; attachement 237/238 | fait |
| J1.3 | `9a259953` | 2026-11-07 | schéma v2 : `meta.partition` + `meta.alternative`, 26 cas / 0 échec | fait |
| J1.4 | `8eb0cc49` | 2026-11-07 | restitution v0 : 46/46 surfaces, miroir strict 0,1087 | fait |
| J2.1 | `9c7f71dc` | 2026-11-07 | table 14 atomes × 8 niveaux : 14/14 lignes, 33 paires colinéaires | fait |
| J2.2 | `c3467170` | 2026-11-07 | corpus commun : 418/438 paires exactes, 8/8 contrôles | fait |
| J3.1 | `c3467170` | 2026-11-07 | retrieval à époque contrôlée : écriture +0,609, date −0,034/siècle (p = 0,19) | fait |
| J3.2 | `c2e629b3` | 2026-11-07 | généalogie à deux faces : 154/154 hors script au hasard | fait |
| J4.1 | `34e3e4ab` | 2026-11-13 | coordination N2 : 2,9726 / 2,7856 (avec `--rope --canal-dir`) | fait |
| J4.2 | `34e3e4ab` | 2026-11-13 | coordination S : 11 verdicts, 7 acceptés / 4 exclus | fait |
| J4.3 | `a934d779` | 2026-11-13 | tagger POS 612 : 0,9475 (+8,49), décision intégrer | fait |
| J4.4 | `34e3e4ab` | 2026-11-13 | coordination A : A6.2 libre (MoE 18 Go), A8.3b2 hors graphe | fait |
| J5.1 | `34e3e4ab` | 2026-11-13 | rapport de semaine : F1 0,7533 → 0,7902, 13 décisions, 21 rejets | fait |
| J5.2 | `0e75f101` | 2026-11-14 | passe, tag, release : le tag `semaine-2026-11-14` est posé en J14.1 sur le dernier commit vert | fait (réparé en J14.1) |
| J6.1 | `64d9dd23` | 2026-11-14 | g017 : règle de l'adverbe final rejetée (F1 0,7901 ; test −0,0028) | fait (rejet) |
| J6.2 | `b6e474dc` | 2026-11-14 | s065 : 238/238 labels, 238/239 cibles, 0 span, 0 POS | fait |
| J7.1 | `d31e8788` | 2026-11-14 | retrieval par famille : sœurs 0,619 vs 0,0445 (13,9×), J3.1 reproduit | fait |
| J8.1 | `229098ec` | 2026-11-14 | restitution v1 : canonique 46/46, strict 0,1087 (ne monte pas) | fait |
| J9.1 | `ecef7250` | 2026-11-14 | passe d'honnêteté : 19 fiches « instantané historique » | fait |
| J10.1 | `03ecee41` | 2026-11-14 | bilan du chantier : 20/21, 5 timeouts, 1 échec (le tag) | fait |
| J11.1 | `84e393bb` | 2026-11-14 | 5 exemples rejoués : 4 corrigés, r035 prédit | fait |
| J11.2 | `09e54143` | 2026-11-14 | evaluer --par-langue : fr 0,8159/0,7475, en 0,9451/0,8656 | fait |
| J11.3 | `55bde5c5` | 2026-11-14 | 50 textes : 0 plantage, 50/50 v2, 115 / 0 chevauchements | fait |
| J11.4 | `febfdfff` | 2026-11-14 | schéma v2 documenté : 6 cas / 0 échec, 612/612 + 612/612 | fait |
| J12.1 | `bb68b820` | 2026-11-14 | §334 : H0 0,909139 / 0,906307, date 0,0089 après topo, V150 β −0,006 | fait |
| J12.2 | `b20a4c31` | 2026-11-14 | CIC : 42/42 verdicts, 42/42 empreintes, 36/36 + 1 020/1 020 rejets | fait |

**Le compte.** **26 tâches** mesurées de J1.1 à J12.2, **25 acceptations vertes**, **1 échec**
(J5.2, le tag), **5 timeouts** (J1.2, J2.2, J3.1, J5.2, J8.1) dont **4 récupérés** par une
acceptation verte ou le commit de la tâche suivante. Les commits J4.1, J4.2 et J4.4 sont emportés
par `34e3e4ab` (J5.1) ; J2.2 et J3.1 partagent `c3467170`. Le commit de cette fiche n'est pas dans
la table : il est dans l'historique.

## 8. Les contrôles négatifs

| # | contrôle | dispositif | résultat | verdict | fiche |
|---|---|---|---|---|---|
| C01 | POS — invariance | diff token à token sur 612 et 602 | 0 jeton changé (3 179 et 3 141 jetons) | pass | [rapport-r035](rapport-r035.md) |
| C02 | F1 — placebo du sujet | déplacer le premier token sans condition | F1 0,7758 < 0,7881 ; 38 phrases perdantes contre 0 | pass | [rapport-convention-gv](rapport-convention-gv.md) |
| C03 | F1 — adverbe large | tout ADV final hors du GV | F1 0,7552 ; test 0,7656 < 0,7663 ; rejeté | pass | [rapport-convention-gv](rapport-convention-gv.md) |
| C04 | Attachement — non-perte | diff segment par segment sur 239 cibles | 0 cible perdue, 0 span perdu ; 238/238 | pass | [rapport-s065](rapport-s065.md) |
| C05 | Tagger — planchers | majoritaire, classe fréquente, permutation, uniforme | 0,2145 / 0,2491 / 0,1667 / 0,0833 ; McNemar 344/74, p = 1,1 × 10⁻⁴² | pass | [rapport-coordination-r](rapport-coordination-r.md) |
| C06 | Schéma — versions croisées | v2 refuse v1 ; v1 refuse v2 ; mutation d'un champ obligatoire | 612/612 ; 612/612 ; mutation refusée | pass | [rapport-schema-v2-doc](rapport-schema-v2-doc.md) |
| C07 | Restitution — mélange / troncature | mélanger et tronquer 46 annotations | 0/46 exact ; 46/46 détecté (les deux) | pass | [rapport-restitution-v0](rapport-restitution-v0.md) |
| C08 | Restitution — structure | retirer rôles, cibles ; changer la clé | 395 rôles, 315 cibles, 43/43 clés détectés | pass | [rapport-restitution-v1](rapport-restitution-v1.md) |
| C09 | Exemples — mutation | muter un token dans une copie de la doc | 4/5 détecté | pass | [rapport-exemples-rejoues](rapport-exemples-rejoues.md) |
| C10 | Par langue — plancher aléatoire | cible exacte tirée au hasard par langue | 1,99 % fr / 2,27 % en / 1,67 % global | pass | [rapport-evaluer-langue](rapport-evaluer-langue.md) |
| C11 | Robustesse — schéma et spans | v1 lue ; v2 refuse v1 ; champ manquant ; chevauchement injecté ; filtrer non vide | tous pass ; 0 span hors texte / 4 827 | pass | [rapport-robustesse-semaine](rapport-robustesse-semaine.md) |
| C12 | Atomes — statut de la table | protocole CLR/permutations/BH/split-half ; aucune correspondance mesurée | 33 paires, 4 composantes ; hypothèse, pas corrélation | pass | [rapport-atomes-niveaux](rapport-atomes-niveaux.md) |
| C13 | Corpus — appariement | 6 rejets + 2 témoins | 8/8 | pass | [rapport-corpus-commun](rapport-corpus-commun.md) |
| C14 | Retrieval — permutations | cibles et années permutées ; candidats mélangés | date p = 0,19 ; brut 0,238 vs 0,427 | pass | [rapport-retrieval-epoque](rapport-retrieval-epoque.md) |
| C15 | Généalogie — labels | labels Panini et Glottolog permutés ; LOO | p = 0,006 / 0,019 ; 154/154 hors script au hasard | pass | [rapport-genealogie-deux-faces](rapport-genealogie-deux-faces.md) |
| C16 | Familles — permutations | permutations 1 000/500 ; requêtes permutées ; LOO ; placebo de dates | famille p = 0,001 ; sœur p = 0,001 ; J3.1 écart 0 | pass | [rapport-retrieval-familles](rapport-retrieval-familles.md) |
| C17 | §334 — contrôles croisés | tradition/années/signatures permutées ; doublons retirés ; eng–eng ; Holm | filiation Holm 0,128 ; époque p = 0,373 ; année intra Holm 0,034 ; V150 β −0,006 | pass | [rapport-panini-334](rapport-panini-334.md) |
| C18 | CIC — altérations | octet altéré 36/36 ; eq(2,2) 1 020/1 020 ; accepte-tout / rejette-tout | 36/36 ; 1 020/1 020 ; 6 / 36 désaccords | pass | [rapport-cic-verificateur](rapport-cic-verificateur.md) |

**Le principe.** Un chiffre sans contrôle n'est pas un résultat. Les contrôles ci-dessus ne sont
pas tous du même type : **plancher** (hasard, majoritaire, uniforme), **permutation** (labels,
années, signatures), **altération** (un octet, un token, un champ), **version adverse** (v1/v2),
**mutation de structure** (rôles, cibles, clé), **placebo** (sujet, adverbe, dates). Chacun est
reproductible par la commande de sa fiche. Les contrôles qui **échouent** sont nommés : J5.2 (le
tag), `g017` (la convention d'adverbe), l'échantillon 20 (sous-puissant), le split réel du tagger
(pas fait), la V14 des 21 langues (pas de données), les 19 étiquettes CIC non exercées.

## 9. Ce qui pourrait rendre ce tableau faux

1. **Ce tableau agrège, il ne remplace pas les fiches.** Les valeurs « avant » sont celles publiées
   par la fiche à son commit ; les valeurs « après » du cœur produit (P01–P12, sauf P10) sont re-mesurées
   au HEAD `b20a4c31`, les autres sont publiées par leur fiche. Si une fiche change, le tableau devient
   faux sans qu'aucun calcul ne l'ait signalé.
2. **La base change les chiffres** : vivant 612 (F1 0,7902 ; 238/239) contre gelé 602 (F1 0,7882 ;
   234/239). Une ligne sans base peut tromper même avec des chiffres exacts.
3. **Le gain F1 est in-sample** : la convention du sujet est lue dans le gold (712/712 GV) puis
   appliquée au gold ; `s065` est un seul cas, en dev. Le +0,0369 n'est pas une généralisation.
4. **Le gold est une convention** : la relative zéro est annotée une fois, l'adverbe final est
   contradictoire (`g005`/`g017` contre `r264`/`r288`). Un autre corpus annoté autrement inverserait
   certains signes.
5. **Le tagger est un run unique** : un seul jour, un seul alias, température 0 mais API non
   déterministe au bit près ; le 612 est tiré par les 160 synthétiques ; le réel 432 ne gagne que
   +4,67 ; le split réel n'est pas fait.
6. **Panini est de surface** : les n-grammes de caractères capturent l'orthographe et les cognates,
   pas le sens ; le corpus est mono-époque (1948), mono-genre (déclaration), 21 textes, 5 familles,
   10 écritures ; le signal de famille est porté par 2 ou 3 paires sur 21 langues, et par 60 paires
   sur `LANG_TREE`.
7. **Le §334 ne sépare pas l'époque de la filiation** : 44 œuvres, 10 traditions (19 GRECO), IC
   larges ; signatures de traductions anglaises alors que la date est celle de la composition ;
   `d_topo` est une distance de transmission, corrélée à la date (ρ ≈ 0,61) ; les 44 signatures ne
   sont pas les vecteurs qui produisent `d_lex`/`cos` des 655 paires (r ≈ 0,37) ; les doublons et
   auto-paires du fichier de paires ; les seuils (50 ans, 250 ans, cos 0,99999) sont des
   conventions.
8. **Le CIC est un verrou de portabilité, pas une preuve de correction** : le corpus n'exerce que
   20 des 39 étiquettes du format ; l'indépendance est de code, pas de spécification ; les 19
   étiquettes non exercées ne sont pas validées.
9. **La passe complète n'est pas la clôture** : 84 portes, 81 vertes, 3 rouges tolérées. J14.1
   n'a **pas refait la passe** : il a revérifié les trois rouges et posé le tag annoté
   `chantier-2026-11-14` sur le dernier commit vert (`0e75f101`), plus le tag de semaine
   `semaine-2026-11-14` (J5.2). Voir [`rapport-cloture-chantier.md`](rapport-cloture-chantier.md).
10. **Les compteurs bougent** : 732 fiches / 826 JSON après la clôture ; l'état `en-cours` est la
    source du compte, pas ce rapport.

## 10. Fichiers

- **Nouveaux** : `reports/rapport-tableau-mesures.md` (ce rapport),
  `reports/tableau-mesures.json`.
- **Base** : `tools/drave.py` (`evaluer --json`, `evaluer --gold --json`) ;
  `tools/tests/linguistique/gold.json`, `gold_gele.json`, `evaluer_gold.py`.
- **Relus, produit** : [`rapport-r035.md`](rapport-r035.md),
  [`rapport-convention-gv.md`](rapport-convention-gv.md),
  [`rapport-schema-v2.md`](rapport-schema-v2.md),
  [`rapport-restitution-v0.md`](rapport-restitution-v0.md),
  [`rapport-g017.md`](rapport-g017.md), [`rapport-s065.md`](rapport-s065.md),
  [`rapport-restitution-v1.md`](rapport-restitution-v1.md),
  [`rapport-exemples-rejoues.md`](rapport-exemples-rejoues.md),
  [`rapport-evaluer-langue.md`](rapport-evaluer-langue.md),
  [`rapport-robustesse-semaine.md`](rapport-robustesse-semaine.md),
  [`rapport-schema-v2-doc.md`](rapport-schema-v2-doc.md).
- **Relus, tagger** : [`rapport-coordination-r.md`](rapport-coordination-r.md).
- **Relus, Panini** : [`rapport-atomes-niveaux.md`](rapport-atomes-niveaux.md),
  [`rapport-corpus-commun.md`](rapport-corpus-commun.md),
  [`rapport-retrieval-epoque.md`](rapport-retrieval-epoque.md),
  [`rapport-genealogie-deux-faces.md`](rapport-genealogie-deux-faces.md),
  [`rapport-retrieval-familles.md`](rapport-retrieval-familles.md),
  [`rapport-panini-334.md`](rapport-panini-334.md),
  [`rapport-cic-verificateur.md`](rapport-cic-verificateur.md).
- **Relus, bilan** : [`rapport-bilan-chantier.md`](rapport-bilan-chantier.md),
  [`rapport-passe-honnetete.md`](rapport-passe-honnetete.md),
  [`rapport-semaine.md`](rapport-semaine.md).
- **JSON lus** : `rapport-bilan-chantier.json`, `pensee-convention-gv.json`,
  `schema-v2-doc.json`, `pensee-robustesse-semaine.json`, `evaluer-langue.json`,
  `atomes-niveaux.json`, `corpus-commun.json`, `retrieval-epoque.json`,
  `genealogie-deux-faces.json`, `retrieval-familles.json`, `panini-334.json`,
  `cic-verificateur.json`, `passe-honnetete.json`.
- **Mis à jour** : `docs/pilotage/en-cours.md`, `docs/pilotage/roadmap.md`,
  `reports/README.md`, `reports/INDEX.md`, `journal/2026-11-14/mesures.md`.
- **Non modifiés** : les fiches et JSON ci-dessus, `tools/`, `data/`, `drave-core/`, `models/`.

## 11. Verdict

**J13.1 est fait.** Le chantier est **mesuré, écrit et ordonné** : **26 tâches** de J1.1 à J12.2,
**25 acceptations vertes**, **1 échec** (J5.2, le tag), **5 timeouts** dont **4 récupérés**. Le
produit a un gain mesuré (**F1 0,7533 → 0,7902**, **attachement 236/237 → 238/238 labels**,
**POS inchangée**, **couverture 0,9916 → 0,9958**, **spans 2 → 1**), le tagger API vaut
**0,9475 (+8,49)** avec sa réserve, et Panini a **sept briques** mesurées et **bornées** (table
14/14, corpus 418/438, retrieval à porte d'écriture, généalogie 154/154 hors script, familles
sœurs 0,619 vs 0,0445, §334 date 0,0089 après topo, CIC 42/42). Le **612** et le **602** sont
donnés ensemble, avec le même contrôle négatif. Ce qui reste est **nommé** : `g017` (convention),
`s065` (hors échantillon), le split réel du tagger, la signature V14 des 21 langues, la porte N2,
le commit S, le rapport A6.2, la passe générique d'honnêteté. **J14.1 a clos le chantier** :
les trois rouges sont revérifiées (sessions verte, `indice` et `melange` structurelles) et le tag
`chantier-2026-11-14` est posé ; le détail est dans
[`rapport-cloture-chantier.md`](rapport-cloture-chantier.md).

