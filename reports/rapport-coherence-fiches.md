# Cohérence des fiches B13 du 2026-11-05 — vérification

> **Date de vérification** : 2026-11-05T13:54-05:00, **arrêtée avant l'intégration v2 stagée à
> 14:11** · **Branche** : `s/v7` · **Périmètre** : les **11 fiches B13 datées du 2026-11-05** et
> leurs 11 JSON homonymes (`reports/`), confrontés aux portes de `tools/pensee/autotest.py`
> (T153, T161, T162, T163, T166, T167, T168, T169, T172, T173, plus les portes propres des
> fiches : T164, T165, T170, T171, T174).
> **Verdict global** : ✅ **8 fiches cohérentes** avec leur JSON et leur porte d'époque ; ❌ **3 fiches
> portent une divergence réelle** (7 écarts : 4 valeurs fausses dans `lexique-elargi`, 2 incohérences
> de dénombrement dans `spans`, 1 attribution inexacte dans `denominateur`) ; 🕓 **7 paliers
> historiques reconnus** (verbe-gv → attachement-cible), plus les colonnes « avant » de
> `lexique-elargi`.
> **⚠️ v2 concurrente** : depuis 14:11, une **intégration v2 stagée** (non committée) change les
> portes (177 → **180**) et la convention SUB (POS gold : **116 verbes / 29 noms**, pas 63/82) ;
> les valeurs dites « actuelles » ci-dessous sont **pré-v2**. Voir § 6.2.
> **Méthode** : lecture des fiches et des JSON ; pour chaque fiche, `git show <commit>:tools/pensee/autotest.py`
> pour lire la porte **telle qu'elle était au commit** ; exécution des 15 portes ciblées et de la
> suite complète (`python3 -m tools.pensee.autotest` → **177/177**) à HEAD **avant la v2**.
> **Aucune fiche modifiée, aucun commit.** Plusieurs fichiers de périmètre ont été modifiés par
> **d'autres agents** pendant la vérification : voir § 6.

## 1. Les 11 fiches et leur verdict

| # | fiche | titre (raccourci) | commit / heure | portes d'alors | portes au 13:54 (pré-v2) | verdict |
|---:|---|---|---|---:|---:|---|
| 1 | [`rapport-pensee-verbe-gv.md`](rapport-pensee-verbe-gv.md) | le verbe du GV : exact 0,0586 → 0,0962 | `9ff4adda` / 08:58 | 167/167 | 177/177 | ✅ cohérente — 🕓 historique |
| 2 | [`rapport-pensee-lexique-verbal.md`](rapport-pensee-lexique-verbal.md) | le lexique verbal : exact 0,0962 → 0,1381 | `d400e188` / 09:11 | 168/168 | 177/177 | ✅ cohérente — 🕓 historique |
| 3 | [`rapport-pensee-spans.md`](rapport-pensee-spans.md) | les 94 spans : 48 REL, 33 SUB, 12 GP (blob committé) | `13e8bb2d` / 09:35 | 169/169 | 177/177 | ⚠️ corps cohérent — ❌ titre/catégories (cf. § 4.2) |
| 4 | [`rapport-pensee-denominateur.md`](rapport-pensee-denominateur.md) | 239 cibles, 146 segments | `f8f5bc04` / 09:42 | 170/170 | 177/177 | ⚠️ chiffres cohérents — ❌ attribution « 93 chez S » (cf. § 4.3) |
| 5 | [`rapport-pensee-classement.md`](rapport-pensee-classement.md) | le classement : exact 0,2260 → 0,6438 | `d8edd1d9` / 10:02 | 171/171 | 177/177 | ✅ cohérente — 🕓 historique |
| 6 | [`rapport-pensee-conventions.md`](rapport-pensee-conventions.md) | verbes 0,7255, noms 0,6000 | `f70a1b2a` / 10:09 | 172/172 | 177/177 | ✅ cohérente — 🕓 historique |
| 7 | [`rapport-pensee-attachement-cible.md`](rapport-pensee-attachement-cible.md) | l'attachement ciblé : exact 0,6438 → 0,8082 | `23853cb7` / 10:18 | 173/173 | 177/177 | ✅ cohérente — 🕓 historique |
| 8 | [`rapport-pensee-lexique-elargi.md`](rapport-pensee-lexique-elargi.md) | le lexique élargi : exact 0,8082 → 0,8483 | `a408a909` / 10:39 | 174/174 | 177/177 | ❌ divergence réelle (cf. § 4.1) |
| 9 | [`rapport-pensee-echecs-cible.md`](rapport-pensee-echecs-cible.md) | les 22 échecs : 11 hors candidats, 11 mal classés | `a048cb83` / 10:49 | 175/175 | 177/177 | ✅ cohérente — actuelle |
| 10 | [`rapport-pensee-topk-strict.md`](rapport-pensee-topk-strict.md) | le top-k strict : 0,6069, pas 0,9241 | `e223a98d` / 10:59 | 176/176 | 177/177 | ✅ cohérente — actuelle |
| 11 | [`rapport-pensee-convention-doc.md`](rapport-pensee-convention-doc.md) | la convention des cibles est documentée | `0ddd4fb9` / 11:10 | 177/177 | 177/177 | ✅ cohérente — actuelle |

La v2 stagée à 14:11 annonce **180/180** et change les valeurs ; la colonne « portes au 13:54 »
est **pré-v2** (voir § 6.2).

Les 11 fiches portent bien la date **2026-11-05** et la ligne **B13** ; elles sont les seules
fiches `rapport-pensee-*.md` à contenir cette date (les fiches B13 du 04/11 — passifs, cible par
proximité, candidats verbes, échecs d'attachement — sont hors périmètre). L'ordre ci-dessus est
l'ordre des commits, pas l'ordre alphabétique.

**Lecture du verdict.** « ✅ cohérente » signifie : les chiffres de la fiche sont exacts **pour son
commit**, son JSON les reprend, et la porte du commit les attendait. « 🕓 historique » signifie que
ces chiffres ne sont plus ceux de HEAD : les portes ont été mises à jour par les commits suivants.
« ❌ divergence » signifie qu'un chiffre est faux **même pour son commit** (arithmétique, table
interne ou porte d'alors).

## 2. Tableau de contrôle

Colonnes : ce que dit la **fiche**, ce que dit le **JSON** homonyme, ce qu'attendait la **porte**
au moment de la vérification (13:54, **pré-v2**), puis la valeur au commit de la fiche entre
crochets. Les valeurs entre parenthèses sont les taux ; `—` signifie que le JSON ne stocke pas ce
champ (le taux est alors recalculé depuis le compte). **La v2 stagée à 14:11 change les
assertions** (T153, T161, T162, T163, T164, T167, T168, T169, T171, T173) ; voir § 6.2. Les
lignes de ce tableau restent la comparaison des fiches à leur commit et aux portes pré-v2.

| Fiche | Chiffre | Fiche (valeur) | JSON | Porte (attendue) | Verdict |
|---|---|---|---:|---|---|
| verbe-gv | portes | 167/167 | 167/167 | 177/177 (actuel) ; **167** au commit | 🕓 historique |
| verbe-gv | exact | 23 (0,0962) | 23 | T153/T161/T164 = 123 (0,5146) ; **[23 / 0,0962]** | 🕓 historique |
| verbe-gv | top1 / top-k | 105 (0,4393) / 122 (0,5105) | 105 / 122 | T153/T161 = 126 (0,5272) ; T162 = 134 (0,5607) ; **[105 / 122]** | 🕓 historique |
| verbe-gv | tête top1 / top-k | 105 (0,7241) / 122 (0,8414) | 105 / 122 | T162 = 122 (tête top-k) ; T161 message 105 (tête top1) ; **[105 / 122]** | 🕓 historique |
| verbe-gv | échecs span / cible | 94 / 23 (total 117) | 94 / 23 | T163 = 94 / 11 (actuel) ; **[94 / 23]** | 🕓 historique |
| verbe-gv | « 23/239 restent faux » | 23 | `echecs.cible_apres` = 23 | T163 cible = 11 (actuel) ; **23** au commit | ⚠️ ambigu : 23 est le résiduel « cible hors candidats », pas 23/239 exact faux (216/239) |
| lexique-verbal | portes | 168/168 | 168/168 | 177/177 (actuel) ; **168** au commit | 🕓 historique |
| lexique-verbal | exact | 33 (0,1381) | 33 | T153/T161 = 123 (0,5146) ; **[33 / 0,1381]** | 🕓 historique |
| lexique-verbal | top1 / top-k | 115 (0,4812) / 132 (0,5523) | 115 / 132 | T153/T161 = 126 (0,5272) ; T162 = 134 (0,5607) ; **[115 / 132]** | 🕓 historique |
| lexique-verbal | tête top1 / top-k | 114 (0,7862) / 131 (0,9034) | 114 / 131 | T162 = 131 (tête top-k) ; T161 message 114 ; **[114 / 131]** | 🕓 historique |
| lexique-verbal | cible hors candidats | 13 | 13 | T163 = 11 (actuel) ; **13** au commit | 🕓 historique |
| spans | portes | 169/169 | 169/169 | 177/177 (actuel) ; **169** au commit | 🕓 historique |
| spans | labels | 145 → 146 | 145 → 146 | T163 = 93/14 ⇒ **146** labels (commit) ; T167 = **145** (actuel) | 🕓 historique |
| spans | span / cible | 94 / 13 → 93 / 14 | 94 / 13 → 93 / 14 | T163 = **94 / 11** (actuel) ; **[93 / 14]** | 🕓 historique |
| spans | REL / SUB / GP | 48 / 33 / 12 (total 93) | 48 / 33 / 12 (total 93) | T166 = **48 / 33 / 13** (total 94) ; **[48 / 33 / 12]** | 🕓 pour 12 (état post-correctif) ; ❌ pour le titre « 94 » (cf. § 4.2) |
| spans | catégories | 65 / 25 / 3 / 1 = **94** | 65 / 25 / 3 / 1 = **94** | après le correctif : **65 / 24 / 3 / 1 = 93** (rejoué, audit A1) | ❌ divergence de dénombrement |
| spans | « 81 des 93 » | 81 | 48 REL + 33 SUB | T166 = 48 + 33 = 81 | ✅ cohérent (le total 93 est historique) |
| spans | « 65 + 25 subordonnées » | 65 + 25 = 90 | — | 81 REL/SUB seulement | ❌ attribution (65/25 sont tous types, pas seulement les subordonnées) |
| denominateur | portes | 170/170 | 170/170 | 177/177 (actuel) ; **170** au commit | 🕓 historique |
| denominateur | labels | 146 | 146 | T167 = **145** (actuel) ; **146** au commit | 🕓 historique |
| denominateur | rendement (÷239) | 0,4812 / 0,5523 / 0,1381 | idem | T153 = 0,5272 / 0,5607 / 0,5146 (actuel) ; **[0,4812 / 0,1381]** | 🕓 historique |
| denominateur | exactitude spans (÷146) | 0,7877 / 0,9041 / 0,2260 | idem | T167 = 0,869 / 0,9241 / 0,8483 (actuel) ; **[0,7877 / 0,9041 / 0,2260]** | 🕓 historique |
| denominateur | « 93 cibles sans segment (REL/SUB de S) » | 93 | 93 | T163 = 93 au commit ; **94** actuel | 🕓 pour 93 ; ❌ pour l'attribution : 81 REL/SUB + 12 GP (cf. § 4.3) |
| classement | portes | 171/171 | 171/171 | 177/177 (actuel) ; **171** au commit | 🕓 historique |
| classement | labels | 146 | 146 | T167 = **145** (actuel) ; **146** au commit | 🕓 historique |
| classement | exact | 94 (0,6438) | 94 | T168 = 123 (0,8483) (actuel) ; **[94 / 0,6438]** | 🕓 historique |
| classement | top1 / top-k | 114 (0,7808) / 132 (0,9041) | 114 / 132 | T161 = 126 ; T167 = 0,869 / 0,9241 ; **[114 / 132]** | 🕓 historique |
| classement | conventions | 51 / 95 ; justes 37 / 57 | 51 / 95 ; 37 / 57 | T168/T169 = 63 / 82 ; 60 / 63 | 🕓 historique |
| classement | échecs | 52 | 52 (`limites`) | 146 − 94 = 52 au commit ; 22 actuel | 🕓 historique |
| conventions | portes | 172/172 | 172/172 | 177/177 (actuel) ; **172** au commit | 🕓 historique |
| conventions | verbes | 37/51 (0,7255) | 37/51 (0,7255) | T169 = 60/63 (0,9524) (actuel) ; **[37/51]** | 🕓 historique |
| conventions | noms | 57/95 (0,6000) | 57/95 (0,6000) | T169 = 63/82 (0,7683) (actuel) ; **[57/95]** | 🕓 historique |
| conventions | total | 94/146 (0,6438) | 94 (0,6438) | T168 = 123 (0,8483) (actuel) ; **[94]** | 🕓 historique |
| conventions | « 0,6438 = 51 × 0,73 + 95 × 0,60 » | 0,6438 | — | exact avec 0,7255 ; 0,6454 avec 0,73 | ⚠️ arrondi non bloquant (cf. § 4.4) |
| attachement-cible | portes | 173/173 | 173/173 | 177/177 (actuel) ; **173** au commit | 🕓 historique |
| attachement-cible | exact | 118 (0,8082) | 118 | T167 = 0,8483 ; T168 = 123 (actuel) ; **[118 / 0,8082]** | 🕓 historique |
| attachement-cible | top1 / top-k | 122 (0,8356) / 132 (0,9041) | 122 / 132 | T167 = 0,869 / 0,9241 (actuel) ; **[0,8356 / 0,9041]** | 🕓 historique |
| attachement-cible | verbes / noms | 48/51 (0,9412) / 70/95 (0,7368) | 0,9412 / 0,7368 | T169 = 60/63 / 63/82 (actuel) ; **[48/51 / 70/95]** | 🕓 historique |
| attachement-cible | rendement global | 0,5105 / 0,5523 / 0,4937 | idem | T153 = 0,5272 / 0,5607 / 0,5146 (actuel) ; **[0,5105 / 0,4937]** | 🕓 historique |
| attachement-cible | échecs | 28 | 28 | 146 − 118 = 28 au commit ; 22 actuel | 🕓 historique |
| lexique-elargi | portes | 174/174 | 174/174 | 177/177 (actuel) ; **174** au commit | 🕓 (le compte seul) |
| lexique-elargi | labels | 145 | 145 | T167 = **145** | ✅ cohérent |
| lexique-elargi | exact | 123 (0,8483) | 123 | T153/T161/T167/T171 = 123 (0,8483) | ✅ cohérent |
| lexique-elargi | top1 | 126 (0,8690) | 126 | T153/T161/T167 = 126 (0,8690) | ✅ cohérent |
| lexique-elargi | top-k | 134 (0,9241) | 134 | T162/T167/T173 = 134 (0,9241) | ✅ cohérent |
| lexique-elargi | verbes / noms (table) | 60/63 (0,9524) / 63/82 (0,7683) | 0,9524 / 0,7683 | T169 = 60/63 / 63/82 | ✅ cohérent |
| lexique-elargi | rendement global | 0,5272 / 0,5607 / 0,5146 | idem | T153 = idem | ✅ cohérent |
| lexique-elargi | « 51 → 62 verbes, 95 → 83 noms » | 62 / 83 | note = 62 | T168/T169 = **63 / 82** | ❌ divergence réelle |
| lexique-elargi | « 0,7368 → 0,7590 » | 0,7590 | 0,7683 | T169 = **0,7683** (63/82) | ❌ divergence réelle |
| lexique-elargi | « 23/145 restent faux » | 23 | 23 (`limites`) | T171 = 123/145 ⇒ **22** ; `echecs-cible` dit 22 | ❌ divergence réelle |
| lexique-elargi | « Sur les 145 segments » (colonne avant) | 145 | `labels` = 145 ; `avant.exact_span` = 0,8082 | T167 au commit précédent = **146** ; 118/146 = 0,8082 | ❌ dénominateur mélangé (146 → 145) |
| lexique-elargi | « +4 » | 4 | — | 118 → 123 = **+5** (ou +4,01 points de taux) | ⚠️ ambiguïté d'unité |
| echecs-cible | portes | 175/175 | 175/175 | 177/177 (actuel) ; **175** au commit | 🕓 (le compte seul) |
| echecs-cible | 145 / 123 / 22 | idem | idem | T171/T172 = 123 / 22 | ✅ cohérent |
| echecs-cible | 11 hors candidats / 11 mal classés | 11 / 11 | 11 / 11 | T172 = 11 / 11 | ✅ cohérent |
| echecs-cible | par type | GP 14/0/10 ; SUB 5/3/1 ; REL 0/0/0 | idem | 14 + 0 + 5 + 3 = 22 ; hors 10 + 1 = 11 | ✅ cohérent |
| topk-strict | portes | 176/176 | 176/176 | 177/177 (actuel) ; **176** au commit | 🕓 (le compte seul) |
| topk-strict | top-k / strict | 134 (0,9241) / 88 (0,6069) | idem | T173 = 134 / 88 / 0,6069 / 0,9241 | ✅ cohérent |
| topk-strict | 46 / 57 | 46 / 57 | — | 134 − 88 = 46 ; 145 − 88 = 57 | ✅ cohérent |
| convention-doc | portes | 177/177 | 177/177 | 177/177 | ✅ cohérent |
| convention-doc | 63 / 82 / 145 | idem | idem | T168/T169 = 63/82 ; T167 = 145 | ✅ cohérent |
| convention-doc | 22 échecs (11 / 11) | 22 | 22 | T172 = 11 / 11 | ✅ cohérent |
| convention-doc | convention REL/SUB/GP/GN/GV | antécédent / verbe / nom | idem | T174 + `CONVENTION_CIBLE` | ✅ cohérent |

**Ce que le tableau ne montre pas** : les 7 fiches historiques ne sont pas « fausses » ; leurs
chiffres sont ceux de leur commit, et les portes T153/T161/T162/T163/T166/T167/T168/T169 ont été
**réécrites** à chaque commit pour suivre. La section 5 donne la chronologie et la valeur d'alors
de chaque porte. Les seules lignes `❌` sont les 7 écarts du § 4.

## 3. Ce que disait l'état au moment de la vérification (13:33–13:54, pré-v2)

Valeurs mesurées et gates exécutées (15 portes ciblées, puis suite complète **177/177**) :

| mesure | valeur | porte qui l'attend |
|---|---:|---|
| cibles | 239 | T153, T161, T167 |
| labels | 145 | T167 |
| top1 / top-k / exact | 126 / 134 / 123 | T153, T161, T162, T168, T171 |
| rendement global (÷239) | 0,5272 / 0,5607 / 0,5146 | T153 |
| exactitude spans (÷145) | 0,8690 / 0,9241 / 0,8483 | T167 |
| top-k strict | 88 (0,6069 ; 0,3682 ÷239) | T173 |
| verbes / noms | 60/63 (0,9524) / 63/82 (0,7683) | T169 |
| spans perdus | 48 REL / 33 SUB / 13 GP (94) | T166 |
| échecs de cible | 11 hors candidats / 11 mal classés | T172 |
| suite complète | 177/177 | `python3 -m tools.pensee.autotest` |

**Depuis 14:11, la v2 stagée** donne : portes **180/180** (annoncé), exact **137/145 (0,9448)**,
top1 **140 (0,9655)**, top-k **142 (0,9793)**, top-k strict **141 (0,9724)**, verbes **116**
(111 justes, 0,9569), noms **29** (26 justes, 0,8966), **8 échecs** (3 hors, 5 mal classés),
rendement **0,5858 / 0,5941 / 0,5732**. Elle n'a **pas** été exécutée ici ; ces valeurs sont
celles de `rapport-pensee-attachement-v2.md` et `pensee-attachement-v2.json` (voir § 6.2).

C'est l'état que les **4 dernières fiches** (lexique-elargi, echecs-cible, topk-strict,
convention-doc) décrivent, aux 4 valeurs fausses du § 4.1 près pour la première. Les 7 fiches
antérieures décrivent l'état d'avant le lexique élargi (sauf le corps de `spans`, qui décrit
l'état post-correctif GP, lui aussi historique).

## 4. Divergences réelles

### 4.1 `lexique-elargi` — 4 valeurs fausses (prose et JSON), la table est juste

La fiche a une table et des champs JSON **corrects** (60/63, 63/82, 0,9524, 0,7683, 123,
0,8483, 126, 134), mais sa prose garde un état intermédiaire (62/83) et son JSON deux champs
faux (`note` = 62, `limites` = 23) ; le décompte 145/146 est mélangé dans les deux :

| # | ce qui est écrit | où | valeur fausse | valeur attendue | preuve |
|---:|---|---|---|---:|---|
| L1 | « la part verbes passe de 51 à **62** cibles » | fiche l. 29 ; JSON `note` | 62 | **63** | table 60/63 ; T168/T169 ; `convention-doc` |
| L2 | « la part noms de 95 à **83** » ; « 0,7368 → **0,7590** » | fiche l. 30, 33 | 83 ; 0,7590 | **82** ; **0,7683** | table 63/82 ; T169 ; 0,7590 = 63/83 |
| L3 | « **23**/145 restent faux » ; « Les **23** échecs » | fiche l. 35 ; JSON `limites` | 23 | **22** (= 145 − 123) | `echecs-cible` (22) ; T171 (123/145) ; doc T171 (22) |
| L4 | « Sur les **145** segments » pour la colonne « avant » | fiche l. 6 | 145 (avant) | **146** (avant) → 145 (après) | T167 au commit `23853cb7` = 146 ; 118/146 = 0,8082 |

**Pourquoi c'est réel et non historique.** Les valeurs 62/83/0,7590/23 ne sont pas les valeurs
d'un commit antérieur : elles ne figurent dans aucun état daté. Le commit `a408a909` publie
60/63 et 63/82 (T169), 123/145 (T171), et le commit suivant `a048cb83` dit 22 échecs. La fiche
elle-même donne 63/82 dans sa table et 123 dans son titre. C'est un **reste d'un état
intermédiaire** (probablement 62 verbes / 83 noms avant les deux dernières reclassifications de
`_est_verbe`), non mis à jour dans la prose. Le JSON `pensee-lexique-elargi.json` reproduit
l'erreur dans `note` (« 51 à 62 ») et `limites` (« 23 échecs »), et son `avant.exact_span`
0,8082 est calculé sur 146 alors que son champ `labels` vaut 145 : **le dénominateur change
entre l'avant (146) et l'après (145)** sans être nommé.

**Ce qu'il faudrait lire (sans corriger la fiche)** : la transition est 146 → 145 labels ;
118 → 123 corrects ; 0,8082 → 0,8483 ; les cibles verbes passent de 51 à 63 (60 justes, 0,9524),
les noms de 95 à 82 (63 justes, 0,7683) ; les échecs passent de 28 à 22. Le « +4 » est ambigu :
+5 en nombre de cibles correctes, +4,01 points de taux (0,8483 − 0,8082).

### 4.2 `spans` — deux incohérences de dénombrement (avant/après mélangés)

**(a) Le titre.** Blob committé (`13e8bb2d`) : « les **94** spans : **48 REL, 33 SUB, 12 GP** ».
Or 48 + 33 + 12 = **93**, et le corps dit « **93** après le correctif ». Le 94 est le total
**avant** le correctif GP (T163 à `9ff4adda`/`d400e188` : 94 de span), le 48/33/12 est la
ventilation **après** (`13e8bb2d` : 93, 12 GP). Le titre mélange les deux états ; le corps, lui,
est cohérent (93 / 12 GP / 48 / 33). L'audit parallèle A1 le qualifie d'« incohérence de
rédaction, pas de mesure » — c'est la bonne lecture.

**(b) Les catégories.** La table « Les 93 spans » donne 65 + 25 + 3 + 1 = **94**, pas 93. Le
JSON committé a la même incohérence : `spans.total` = 93, `categories` = 65/25/3/1 = 94.
Rejoué au commit `13e8bb2d`, l'après-correctif donne **65/24/3/1 = 93** (le correctif GP
transforme un « plus large » en succès : 25 → 24) ; l'avant `d400e188` donne bien 65/25/3/1 =
94. La table publiée est donc la photo **avant**, présentée sous le titre « Les 93 spans ». Le
courant (après le lexique élargi) est **65/24/4/1 = 94** (un « plus étroit » de plus), ce que
le bloc `courant` ajouté depuis (non committé) enregistre.

**(c) L'attribution.** « les subordonnées ne sont pas produites (65 cas) ou le sont avec un span
plus large (25) » : 65 + 25 = 90, alors qu'il n'y a que **81** REL/SUB (48 + 33). Les 65/25 sont
les catégories de **tous** les spans perdus (GP compris), pas seulement des subordonnées. La
phrase suivante, « les subordonnées sont le trou (81 des 93) », est correcte ; c'est la première
qui ne l'est pas.

**Verdict** : la mesure du corps (93 / 12 GP / 48 / 33 / 81 REL/SUB) est juste à son commit ;
le titre et la table des catégories racontent l'état d'avant sans le dire. Ce sont des
divergences réelles de **dénombrement/libellé**, pas des mesures fausses.

### 4.3 `denominateur` — une attribution inexacte (les chiffres sont justes)

La fiche dit : « 93 cibles n'ont pas de segment au bon span (**REL/SUB de S**) » et « les 93
spans manquants : chez S (REL/SUB) ». Les **93** sont justes à son commit (`239 − 146`), mais
leur composition est **48 REL + 33 SUB + 12 GP** : il y a **81** REL/SUB et **12** GP. Les GP ne
sont pas « chez S » (le générateur de structures) ; ce sont les groupes prépositionnels, dont la
fiche `spans` dit qu'ils sont dans son territoire (le GP borné au verbe). La même erreur est
dans `pensee-denominateur.json` (`limites: ["les 93 spans chez S"]`). C'est une divergence
d'**attribution**, pas de chiffre.

### 4.4 Les ambiguïtés qui ne sont pas comptées comme divergences

- **`verbe-gv` « 23/239 restent faux »** : le nombre 23 est le résiduel « cible hors des
  candidats » (JSON `echecs.cible_apres`), pas 23/239 exact faux (l'exact a 23 justes sur 239,
  donc 216 faux). La phrase est trompeuse ; le chiffre 23 est juste dans sa catégorie.
- **`conventions` « 0,6438 = 51 × 0,73 + 95 × 0,60 »** : avec 0,73 (arrondi), on obtient 0,6454 ;
  l'égalité n'est exacte qu'avec 0,7255 (37/51) : (51 × 0,7255 + 95 × 0,60) / 146 = 0,6438.
  C'est un arrondi de rédaction, pas un chiffre faux.
- **`lexique-elargi` « +4 »** : ambigu entre +5 cibles correctes et +4,01 points de taux ; les
  deux lectures sont défendables, la fiche ne dit pas l'unité.
- **« global »** : dans `conventions`, 0,6438 est le taux sur les 146 segments ; dans
  `denominateur`, « rendement global » désigne ÷239 (0,3933 à l'époque). Le mot est surchargé
  entre les deux fiches, sans conséquence sur les chiffres.
- **« (T28 les couvrent) »** : phrase de template répétée dans les 7 premières fiches ; T28 est
  l'audit des mesures « seule » (`tools/pensee/audit.py`, 15 lignes politiques × mondes), il ne
  couvre pas l'attachement. C'est un **faux renvoi** de rédaction, pas un chiffre faux.

## 5. Chiffres historiques reconnus

### 5.1 La chronologie qui explique les écarts

Toutes les fiches sont datées **2026-11-05**, mais leurs commits sont horodatés de 08:58 à
11:10. Chaque commit a **réécrit** la porte de la fiche pour attendre la nouvelle valeur ; les
portes actuelles (T153, T161, T162, T163, T166, T167, T168, T169) attendent donc l'état final,
pas celui des fiches antérieures. C'est la définition même d'un chiffre historique : une valeur
d'alors, juste à sa date, devenue fausse comme description de HEAD.

| heure | fiche | portes | labels | top1 / top-k / exact (numérateurs) | span / cible | conventions |
|---|---:|---:|---:|---|---:|---|
| 08:58 | verbe-gv | 167 | 145 | 105 / 122 / 23 | 94 / 23 | — |
| 09:11 | lexique-verbal | 168 | 145 | 115 / 132 / 33 | 94 / 13 | — |
| 09:35 | spans | 169 | 145 → 146 | 115 / 132 / 33 | 94 → 93 / 13 → 14 | — |
| 09:42 | denominateur | 170 | 146 | 115 / 132 / 33 | 93 / 14 | — |
| 10:02 | classement | 171 | 146 | 114 / 132 / 94 | 93 / 14 | 51 / 95 ; 37 / 57 |
| 10:09 | conventions | 172 | 146 | 114 / 132 / 94 | 93 / 14 | 51 / 95 ; 37 / 57 |
| 10:18 | attachement-cible | 173 | 146 | 122 / 132 / 118 | 93 / 14 | 51 / 95 ; 48 / 70 |
| 10:39 | lexique-elargi | 174 | 146 → 145 | 126 / 134 / 123 | 94 / 11 | 63 / 82 ; 60 / 63 |
| 10:49 | echecs-cible | 175 | 145 | 126 / 134 / 123 | 94 / 11 | 63 / 82 ; 60 / 63 |
| 10:59 | topk-strict | 176 | 145 | 126 / 134 / 123 | 94 / 11 | 63 / 82 ; 60 / 63 |
| 11:10 | convention-doc | 177 | 145 | 126 / 134 / 123 | 94 / 11 | 63 / 82 ; 60 / 63 |

Les numérateurs `top1 / top-k / exact` sont ceux de la fiche ; le taux se calcule sur **239**
(rendement global) ou sur **`labels`** (exactitude spans) selon la ligne ; les deux lectures ne
sont jamais mélangées dans une même comparaison.

Les valeurs de la ligne 09:35 (`spans`) sont le couple avant/après du correctif GP ; le
`146 / 93 / 12 GP` de cette ligne est l'état **post-correctif GP** (09:35–10:18), pas l'état
courant. Le `145 / 94 / 13 GP` revient avec le lexique élargi (`a408a909`, 10:39) : il perd le
label gagné par le correctif (les frontières de GP dépendent de `_est_verbe`, que le lexique
élargi change), mais gagne 5 cibles exactes. C'est le même total **94** qu'au début, mais avec
une histoire différente : le correctif GP était descendu à **93 / 12 GP**, le lexique élargi
remonte à **94 / 13 GP** ; le F1 courant (0,2862) diffère de l'avant (0,2864).

### 5.2 Les 7 paliers reconnus

1. **verbe-gv** (167/167) : exact 23 (0,0962), top1 105 (0,4393), top-k 122 (0,5105), tête
   105/122, span 94, cible 23.
2. **lexique-verbal** (168/168) : exact 33 (0,1381), top1 115 (0,4812), top-k 132 (0,5523),
   tête 114/131, cible 13.
3. **spans** (169/169) : labels 145 → 146, couverture 0,6067 → 0,6109, F1 0,2864 → 0,2869,
   span 94 → 93, cible 13 → 14, 48/33/12.
4. **denominateur** (170/170) : 146 labels, rendement 0,4812/0,5523/0,1381, exactitude spans
   0,7877/0,9041/0,2260.
5. **classement** (171/171) : exact 94 (0,6438), top1 114 (0,7808), top-k 132 (0,9041),
   conventions 51/95, justes 37/57, 52 échecs.
6. **conventions** (172/172) : 37/51 (0,7255), 57/95 (0,6000), 94/146 (0,6438), 52 échecs.
7. **attachement-cible** (173/173) : exact 118 (0,8082), top1 122 (0,8356), top-k 132 (0,9041),
   verbes 48/51 (0,9412), noms 70/95 (0,7368), rendement 0,5105/0,5523/0,4937, 28 échecs.

À quoi s'ajoutent les **colonnes « avant »** de `lexique-elargi` : 118 (0,8082), 122 (0,8356),
132 (0,9041), 146 labels, 48/51, 70/95, 28 échecs. Ces valeurs sont celles d'`attachement-cible`
(10:18), pas une erreur ; elles sont simplement comparées à l'après (145 labels, 123, 0,8483)
dans une fiche qui dit « 145 » pour les deux.

### 5.3 Les docstrings de portes qui gardent l'historique

Les **assertions** des portes sont à jour (elles passent toutes, 177/177) ; plusieurs
**docstrings** ou messages sont restés à un état antérieur. C'est une dette de libellé des
portes, pas une erreur des fiches, mais elle peut tromper un lecteur qui prendrait le
docstring pour la valeur attendue :

- **T162** : docstring « le top-k passe de 78 à 112 (0,4686) » ; l'assertion attend 134
  (0,5607).
- **T163** : docstring « 94 de span, 33 de cible » ; l'assertion attend 94 / 11 (le message
  garde « 33 avant les correctifs », ce qui est une note historique correcte).
- **T166** : docstring « 48 REL, 33 SUB, 12 GP » ; l'assertion attend **13** GP (le 12 est
  l'état post-correctif GP, historique).
- **T167** : docstring « exactitude spans (÷146) » ; l'assertion attend `labels == 145`.
- **T168** : docstring « exact 94 » et message « exact 123/146 » ; l'assertion attend
  `exact == 123` sur 145 labels.
- **T153**, **T161**, **T169**, **T172**, **T173**, **T174** : cohérents avec l'état courant.

## 6. Concurrence : deux fichiers modifiés pendant la vérification

Je n'ai modifié **aucun** fichier existant et n'ai fait **aucun** commit. Pendant la
vérification (vers 13:43–13:54), un **autre agent** a modifié deux fichiers de périmètre :

- `reports/pensee-spans.json` : ajout d'un bloc `courant` (145 labels, couverture 0,6067, F1
  0,2862, 94 spans, REL 48 / SUB 33 / GP 13, catégories 65/24/4/1), sourcé « audit A1
  (`pensee-audit-attachement.json`) » ; les blocs `spans`, `categories`, `avant`, `apres`
  committés restent l'historique. Ce bloc est cohérent avec la mesure courante.
- `reports/rapport-pensee-spans.md` : titre et table des types passés à l'état courant
  (94 / 13 GP / catégories 65/24/4/1), avec une note « audit A1 ». **La correction est
  partielle** : le chapô dit encore « sont 48 REL, 33 SUB et **12 GP** » ; la narrative dit
  encore « plus large (**25**) » ; et le tableau intitulé « après le GP borné » garde, pour les
  lignes labels / couverture / F1 / top1-top-k-exact, les valeurs historiques
  `146 / 0,6109 / 0,2869 / 115-132-33` alors que la note affirme qu'il donne « désormais » le
  courant (`145 / 0,6067 / 0,2862 / 126-134-123`). C'est une incohérence **nouvelle**, créée par
  la correction partielle ; elle n'est pas de moi.

Le constat du § 4.2 porte sur le **blob committé** (`git show 13e8bb2d:...`), qui est la
référence historique. L'état du worktree au moment de la rédaction est le suivant :
`rapport-pensee-spans.md` et `pensee-spans.json` sont `M` (non committés), les autres 10 fiches
et 10 JSON sont propres. Si la correction doit être validée, il reste à aligner le chapô (12 →
13 GP), la narrative (25 → 24) et les lignes labels/couverture/F1/top1 du tableau sur l'état
courant — ou à assumer que ce tableau est l'historique du correctif GP et le dire dans son
en-tête.

## 7. Limites

- **Les 7 fiches historiques n'ont pas été rejouées** en exécutant leur code d'époque : j'ai lu
  leurs valeurs dans la fiche, leur JSON et `git show <commit>:tools/pensee/autotest.py`. C'est
  suffisant pour la cohérence documentaire ; ce n'est pas une reproduction métrologique. Un
  audit parallèle (A1, `pensee-audit-attachement.json`, non committé) a, lui, rejoué 4 commits
  et trouve les mêmes valeurs ; il est cité comme **corroboration**, pas comme source primaire.
- **Les portes** : les 15 portes ciblées et la suite complète ont été exécutées à HEAD
  (177/177). Les valeurs d'alors viennent des assertions des commits, pas d'une exécution des
  177 portes à chaque commit.
- **Les docstrings de portes** sont périmées par endroits (§ 5.3) ; je me suis appuyé sur les
  **assertions**, jamais sur les docstrings, pour les valeurs attendues.
- **Hors périmètre** : `docs/implantation/moteur-de-pensee.md` porte encore « 48 REL, 33 SUB,
  12 GP » à la ligne T166 (valeur historique) et `reports/README.md` reprend les titres des
  fiches (donc le 12 GP de `spans`) ; la roadmap, elle, est à jour (13 GP, 177/177). Je ne les
  modifie pas (consigne).
- **Concurrence** : voir § 6. Les deux fichiers `spans` ont bougé sous moi ; le constat
  principal est daté par le blob `13e8bb2d`. Aucun autre fichier de périmètre n'a bougé.
- **Pas de correction** : les valeurs « attendues » du § 4 sont celles des portes, des JSON et
  de l'arithmétique ; aucune fiche n'a été réécrite. Le fichier `pensee-spans.json` contient
  désormais un bloc `courant` ajouté par un autre agent ; je ne l'ai pas touché.

## 8. Fichiers

- cette fiche : [`rapport-coherence-fiches.md`](rapport-coherence-fiches.md) ;
- le détail structuré : [`pensee-coherence-fiches.json`](pensee-coherence-fiches.json) ;
- les 11 fiches et leurs 11 JSON : voir le tableau § 1 ;
- les portes : [`tools/pensee/autotest.py`](../tools/pensee/autotest.py) (`t153_attachement`,
  `t161_cible_proximite` … `t174_convention_documentee`) ;
- la mesure : [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
  [`bloc_linguistique.py`](../tools/bloc_linguistique.py) ;
- corroboration externe (non committée, autre agent) : `pensee-audit-attachement.json`,
  `rapport-audit-attachement.md`.
