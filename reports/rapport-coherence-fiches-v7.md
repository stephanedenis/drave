# Cohérence des fiches B13 du 2026-11-05 — v2 → v7

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ❌
> **7 fiches auditées** (1 courante, 6 historiques), **23 écarts numériques**, dont **4 critiques** ;
> **7 fiches** ont au moins une lacune JSON ↔ texte ; **5 fiches** n'ont pas de contrôle négatif ;
> **6 fiches historiques** n'ont pas de mention d'historique ; **2 lignes** de `reports/README.md`
> répètent les valeurs périmées. Aucun renvoi de § faux, aucun lien relatif cassé, un seul tableau
> dont la somme visible ne tombe pas (les corrections de la v2).
>
> **État audité** : commit **`69bd865e`** (2026-11-05 19:22), branche `s/v7`. Pendant l'audit, HEAD a
> avancé de `69bd865e` à **`e4cd4408`** (deux commits `DOCS`/`JOURNAL` seulement) ; les sept fiches,
> leurs JSON et `reports/README.md` sont **identiques** dans les deux commits. L'audit reste ancré
> sur `69bd865e`.
>
> **Méthode** : lecture des 7 fiches et de leurs 7 JSON ; pour chaque fiche, `git show <commit>:` du
> `bloc_linguistique.py` historique chargé comme module, `RACINE` forcé à la racine du dépôt, puis
> `evaluer_bloc` sur le **gold vivant 612** et le **gold gelé 602**. Les chiffres de la v7 sont
> rejoués au commit `69bd865e` ; les chiffres des fiches historiques sont rejoués à leur commit.
> **Aucune fiche modifiée, aucun commit, aucune écriture hors des deux fichiers de sortie.**
> Détail structuré : [`pensee-coherence-fiches-v7.json`](pensee-coherence-fiches-v7.json).

## 1. Synthèse

| indicateur | valeur |
|---|---:|
| fiches vérifiées | **7** |
| fiches courantes / historiques | **1 / 6** |
| fiches sans écart numérique | **1** (v3) |
| fiches avec au moins un écart numérique | **6** (v2, v4, v5, v6, v7, gold-split) |
| écarts numériques | **23** |
| — critiques (chiffre de tête faux) | **4** |
| — majeurs (table, prose, base de mesure) | **17** |
| — mineurs (compte « six » vs « sept ») | **2** |
| fiches avec lacune JSON ↔ texte | **7** |
| fiches sans contrôle négatif | **5** (v4, v5, v6, v7, gold-split) |
| fiches historiques sans mention d'historique | **6** |
| lignes de `reports/README.md` à corriger | **2** (v5, v4) |
| renvois de § faux | **0** |
| liens relatifs cassés | **0** |
| tableaux dont la somme visible ne tombe pas | **1** (v2, corrections) |

**Lecture.** Les trois fiches de la fin de journée (v4, v5, v7) ont été rédigées **en place** :
leur titre et leurs puces gardent l'état intermédiaire d'avant la dernière correction, tandis que
l'en-tête, le tableau et le JSON portent l'état final. Les valeurs finales sont, elles, exactes
(sauf la base F1/tête/POS, mesurée sur le gold gelé 602 et présentée comme le gold 612). La v6 est
juste sur ses propres chiffres, mais sa ligne F1 compare une constante de porte (v5, gold gelé) à
une valeur vivante (v6, gold 612). La v2 porte deux erreurs déjà documentées par l'audit A8
(`rapport-audit-v2.md`), non corrigées. La v3 est la seule dont tous les chiffres se reproduisent,
mais son JSON n'a pas suivi la réparation de son tableau (A13 absent).

## 2. Les sept fiches

| # | fiche | commit | statut | portes | verdict de la fiche | verdict de l'audit | écarts |
|---:|---|---|---|---:|---|---|---:|
| 1 | [`rapport-pensee-attachement-v2.md`](rapport-pensee-attachement-v2.md) | `9d5337ce` | historique | 180/180 | ✅ | ⚠️ chiffres reproduits, 3 écarts de table/prose (A8) | 3 |
| 2 | [`rapport-pensee-attachement-v3.md`](rapport-pensee-attachement-v3.md) | `dcf7bc91` / `e1903e2d` | historique | 181/181 | ✅ | ✅ chiffres ; ⚠️ JSON non mis à jour | 0 |
| 3 | [`rapport-pensee-segmentation-v4.md`](rapport-pensee-segmentation-v4.md) | `392f03aa` | historique | 183/183 | ✅ | ❌ titre/prose périmés + base F1 | 7 |
| 4 | [`rapport-pensee-couverture-v5.md`](rapport-pensee-couverture-v5.md) | `b975011b` | historique | 183/183 | ✅ | ❌ titre/puces périmés + base F1 | 8 |
| 5 | [`rapport-pensee-attachement-parfait.md`](rapport-pensee-attachement-parfait.md) | `0ec6c27d` | historique | 183/183 | ✅ | ⚠️ chiffres justes ; ligne F1 sur deux bases | 1 |
| 6 | [`rapport-gold-split.md`](rapport-gold-split.md) | `85e4082b` | historique | 183/183 (commit) | ✅ | ⚠️ chiffres justes ; une phrase fausse | 1 |
| 7 | [`rapport-pensee-couverture-v7.md`](rapport-pensee-couverture-v7.md) | `69bd865e` | **courante** | 183/183 | ✅ | ❌ base F1/tête/POS + arithmétique + colonne v6 | 3 |

Les sept fiches nomment bien **B13**, la **date 2026-11-05** et un **verdict**. `reports/README.md`
les référence toutes (lignes 18–22, 30 et 36).

## 3. Mesures reproduites

### 3.1 Attachement, couverture, spans

| fiche | labels | exact | top1 | top-k | par langue | autres |
|---|---:|---:|---:|---:|---|---|
| v2 | 145 | 137/145 (0,9448) | 140 (0,9655) | 142 (0,9793) | fr 109/117, en 28/28 | strict 141 ; verbes 111/116 ; noms 26/29 ; spans 94 = 48 REL + 33 SUB + 13 GP |
| v3 | 145 | 141/145 (0,9724) | 143 (0,9862) | 142 (0,9793) | fr 113/117, en 28/28 | strict 142 ; verbes 112/116 ; noms 29/29 ; exact_any 143 ; spans 94 |
| v4 | 160 | 157/160 (0,9812) | 157 | 156/239 (0,6527) | fr 117/118 (0,9915), en 40/42 (0,9524) | spans 79 = 48 REL + 21 SUB + 10 GP ; échecs 3 |
| v5 | 187 | 186/187 (0,9947) | 186 | 161/239 (0,6736) | fr 126/127 (0,9921), en 60/60 | spans 52 = 24 REL + 12 SUB + 16 GP ; dev 126/126 ; test 60/61 |
| v6 | 187 | 187/187 (1,0000) | 187 | 161/239 (0,6736) | fr 127/127, en 60/60 | verbes 131/131 ; noms 56/56 ; dev 126/126 ; test 61/61 ; spans 52 |
| v7 | 196 | 195/196 (0,9949) | 195 | 166/239 (0,6946) | fr 135/135, en 60/61 (0,9836) | spans 43 = 21 REL + 17 SUB + 5 GP |
| gold-split | dev 106, test 54 | dev 104/106 (0,9811), test 53/54 (0,9814) | — | — | dev fr 79/79, en 25/27 ; test fr 38/39, en 15/15 | dev 422 phr. / 163 cibles ; test 190 / 76 ; tout 612 / 239 / 160 |

Toutes ces valeurs se reproduisent. Les écarts de la v4 et de la v5 portent sur le **titre** et les
**puces**, pas sur ce tableau. Le split de la fiche gold-split se reproduit exactement, y compris
les sources (dev 15 hand / 302 reel / 105 synth ; test 5 / 130 / 55 ; tout 20 / 432 / 160) et les
langues (dev 277 fr / 145 en ; test 125 / 65 ; tout 402 / 210).

### 3.2 F1, tête, POS : la base de mesure n'est pas nommée

| fiche | F1 publié | F1 612 | F1 602 | tête publiée | tête 612 | tête 602 | POS publié | POS 612 | POS 602 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| v4 | 0,4539 | 0,4509 | **0,4539** | 0,6432 | 0,6385 | **0,6432** | — | 0,7455 | 0,7475 |
| v5 | 0,5156 | 0,5130 | 0,5164 | 0,6826 | 0,6785 | 0,6834 | — | 0,7461 | 0,7482 |
| v6 | 0,5130 | **0,5130** | 0,5164 | — | 0,6785 | 0,6834 | — | 0,7461 | 0,7482 |
| v7 | 0,5595 | 0,5555 | **0,5595** | 0,7205 | 0,7152 | **0,7205** | 0,7603 | 0,7581 | **0,7603** |

**Le gold 612** = 20 hand + 432 reel + 160 synth (2, 3, 4, 5, 6, 7). **Le gold gelé 602** =
20 hand + **422** reel + 160 synth : dix phrases réelles de moins, mais **les mêmes 239 cibles**.
Les colonnes 612 et 602 sont mesurées au commit de chaque fiche, avec le blob historique chargé
depuis `git show`. Les valeurs en gras sont celles que la fiche publie.

- **v4** publie la F1 et la tête du **602** tout en écrivant « le gold 612 » (§ 3) ; sur 612, le
  code donne 0,4509 et 0,6385.
- **v5** publie 0,5156 / 0,6826, qui ne sont ni le 612 (0,5130 / 0,6785) ni le 602 (0,5164 /
  0,6834) : ce sont les constantes de la porte T112/T113 (tolérance 0,001).
- **v6** publie la F1 du **612** (0,5130), ce qui est cohérent avec le « gold 612 » de sa fiche.
  C'est le seul des quatre dont la F1 est sur le gold annoncé.
- **v7** publie la F1, la tête et la POS du **602** tout en écrivant « le gold 612 » (§ 3) ; sur
  612, le code donne 0,5555 / 0,7152 / 0,7581. La couverture et l'exactitude, elles, sont bien sur
  le 612 (196/239, 195/196).

## 4. Registre des écarts

### 4.1 v2 — `9d5337ce` (3 écarts)

| id | gravité | où | constat | mesure / correction |
|---|---|---|---|---|
| V2-1 | majeure | § 1, lignes 27–29 | la colonne « avant » est étiquetée « (POS gold) » alors que 63/82 est l'**ancien split lexical** (`_est_verbe`) ; la ligne écrit « 63 (0,9524) » et « 82 (0,7683) », des **comptes de labels** avec des taux calculés sur 60/63 et 63/82 ; « +48 cibles » est `111 − 63` (justes après − cibles avant), ni un gain de cibles ni un gain de justes | écrire 60/63 (0,9524) et 63/82 (0,7683) comme split lexical ; le POS gold sur le même bloc donne 97/116 et 26/29, le v2 111/116 et 26/29 ; les cibles passent 63 → 116 (+53) et les justes 60 → 111 (+51), ou +14 à split POS constant |
| V2-2 | majeure | § 2, lignes 46–47 | « **46** des 57 échecs étaient des candidats non réduits à leur tête » ; le même paragraphe dit « +45 » | lire **45** ; le 46 est `134 − 88` (sous-chaîne vs strict), le nombre de têtes candidates égales à la cible est 45 (A2, comptage indépendant de A8) |
| V2-3 | majeure | § 2, tableau des corrections, lignes 35–39 | la colonne « gain » ne s'additionne pas aux totaux : strict 88 + 45 = 133, alors que le total est 141 ; top-k 134 + aucun gain crédité, alors que le total est 142 ; top1 126 + 6 + 8 = 140, mais le +6 du segment n'est pas crédité | créditer le lexique de **+8 top-k et +8 strict** (88 + 45 + 8 = 141 ; 134 + 8 = 142) et le segment de **+6 top1**, ou ajouter une ligne « total » |

Le reste de la fiche se reproduit : 145 labels, 137/145, 140, 142, 141 strict, 111/116, 26/29,
8 échecs (3 + 5), 94 spans (48 + 33 + 13), rendement 0,5858 / 0,5941 / 0,5732, modèle appris
142/145, +5, McNemar 7/2, p = 0,18, IC [−0,7 ; +7,6] (arrondis A8), gold 612 = 20 + 432 + 160.
L'audit A8 a déjà documenté V2-1, V2-2 et V2-3 ; la fiche ne les a pas corrigés.

### 4.2 v3 — `dcf7bc91` / `e1903e2d` (0 écart numérique, 1 lacune JSON)

Tous les chiffres se reproduisent : 141/145, 143 top1, 142 top-k, 142 strict, 112/116 verbes,
29/29 noms, exact_any 143, 94 spans, contrôles 132 (−5), 131 (−6), R3a 2/4, rendement 0,5983 /
0,5941 / 0,5900, plafond 145/239 = 0,6067. Le tableau R2/R3/R4 s'additionne (+2 +1 +1 = +4 en
exact ; +2 +1 = +3 en top1 ; +1 en strict).

Le **JSON n'a pas suivi la réparation du tableau** (`e1903e2d`) : la note A13 ajoutée au Markdown
(43/96 GP, exact_any 143/145, 143/239, McNemar p = 0,5, s108/s122) est **absente du JSON** ; les
comptes 111/116, 112/116, 26/29 et 29/29 n'y sont pas non plus. Le JSON date encore de
`dcf7bc91` (`git diff dcf7bc91..HEAD -- reports/pensee-attachement-v3.json` est vide).

**Ambiguïté non comptée** : R1 est donné « portée 2–3 » alors que la ligne liste trois identifiants
(`s108`, `s122`, `s041`) ; le texte dit que `s041` (`marche`) est hors lexique (`marcher`), ce qui
explique peut-être le 2, mais la fiche ne le dit pas.

### 4.3 v4 — `392f03aa` (7 écarts)

| id | gravité | où | constat | mesure / correction |
|---|---|---|---|---|
| V4-1 | **critique** | titre, ligne 1 | « F1 0,2862 → **0,4194** » | la F1 finale est **0,4539** (en-tête, § 1, § 2, porte T112) ; 0,4194 est l'état d'avant la correction 7 |
| V4-2 | **critique** | titre, ligne 1 | « exact **158/160 (0,9875)** » | **157/160 (0,9812)** (en-tête, § 2, JSON, porte T167) ; 158/160 est l'état d'avant la correction 7 |
| V4-3 | majeure | § 2, ligne 46 | « sans perdre l'exactitude (0,9724 → **0,9875**) » | 0,9724 → **0,9812** |
| V4-4 | majeure | § 2, ligne 45 | « l'exact tient (**41/42**) » | **40/42 (0,9524)** (tableau, JSON, porte T180) |
| V4-5 | majeure | § 5, ligne 70 | « **Les 2 échecs** (r162, r309) » | **3** échecs : r162, r309, **r194** (§ 2, JSON) |
| V4-6 | mineure | § 6, ligne 77 | « les **six** corrections » | **sept** corrections (§ 1, JSON) |
| V4-7 | majeure | § 3, ligne 57 | « Le gold **612** » alors que la F1 et la tête publiées sont mesurées sur le gold **gelé 602** | nommer le 602, ou publier les valeurs du 612 : F1 **0,4509**, tête **0,6385** |

Le tableau des spans s'additionne (48 + 21 + 10 = 79) et le reste des mesures se reproduit
(160 labels, 157/160, 156 top-k, fr 117/118, en 40/42, 3 échecs). La fiche ne porte pas de contrôle
négatif et pas de mention d'historique.

### 4.4 v5 — `b975011b` (8 écarts)

| id | gravité | où | constat | mesure / correction |
|---|---|---|---|---|
| V5-1 | **critique** | titre, ligne 1 | « exact **185/187 (0,9893)** » | **186/187 (0,9947)** (en-tête, § 2, JSON, porte T161/T167) ; 185/187 est l'état intermédiaire |
| V5-2 | majeure | § 2, ligne 46 | « dev **125/126 (0,9921)** » | **126/126 (1,0000)** (en-tête, JSON, split reproduit) ; 0,9921 est le taux français 126/127, recopié |
| V5-3 | majeure | § 2, ligne 44 | « +27 labels et **+28 exact** » | 157 → 186 = **+29 exact** |
| V5-4 | majeure | § 2, ligne 45 | « L'anglais rattrape (**40 → 59**) » | **40 → 60** (tableau, JSON, porte T180) |
| V5-5 | majeure | § 2, § 3, § 5 | « **Les 27 échecs de cible** » | **1 échec de cible** (`echecs_cible` = 1, r309) ; les 27 sont **26 candidats manquants + 1 échec de cible** |
| V5-6 | majeure | § 2, ligne 48 | « le top-k tombe à **0,8556** sur les labels » | 161/187 = **0,8610** (ou 161/239 = 0,6736) ; 0,8556 = 160/187, valeur d'avant le correctif |
| V5-7 | mineure | § 1, ligne 15 ; § 6, ligne 76 | « Les **six** corrections » | **sept** corrections (tableau à 7 lignes, JSON à 7 entrées) |
| V5-8 | majeure | en-tête, § 2 | F1 **0,5156**, tête **0,6826** | sur le gold 612 : **0,5130 / 0,6785** ; sur le 602 : **0,5164 / 0,6834** ; 0,5156/0,6826 sont les constantes de la porte T112/T113, pas la mesure exacte |

Le reste se reproduit : 187 labels, 186/187, 186 top1, 161 top-k, fr 126/127, en 60/60, 52 spans
(24 + 12 + 16), dev 126/126, test 60/61, couverture 0,7824, F1 dev/test 0,5091 / 0,5217. Le titre,
les puces et deux comptes sont restés à l'état intermédiaire (185/187, 125/126, +28, 40 → 59,
27 échecs, six corrections) ; l'en-tête, le tableau et le JSON sont à l'état final.

### 4.5 v6 — `0ec6c27d` (1 écart)

| id | gravité | où | constat | mesure / correction |
|---|---|---|---|---|
| V6-1 | majeure | § 2, ligne 31 | « F1 syntagmes 0,5156 → 0,5130 » | sur un gold constant, la F1 ne bouge pas : sur 612, v5 = v6 = **0,5130** ; sur 602, v5 = v6 = **0,5164**. La baisse 0,5156 → 0,5130 compare la constante de porte de la v5 (602) à la valeur vivante de la v6 (612) |

Les autres chiffres se reproduisent : 187/187, fr 127/127, en 60/60, verbes 131/131, noms 56/56,
dev 126/126, test 61/61, top-k 161/239 (0,6736), couverture 0,7824, 52 spans (24 + 12 + 16).
La fiche n'a pas de contrôle négatif ni de mention d'historique.

### 4.6 v7 — `69bd865e` (3 écarts, fiche courante)

| id | gravité | où | constat | mesure / correction |
|---|---|---|---|---|
| V7-1 | majeure | § 3, ligne 40 | « le contexte … rend **0,0132** de POS » | 0,7603 − 0,7475 = **0,0128** |
| V7-2 | **critique** | en-tête, § 2 | F1 **0,5595**, tête **0,7205**, POS **0,7603** présentées avec le gold **612** (§ 3) | ces trois valeurs sont celles du gold **gelé 602** ; sur 612, le code donne F1 **0,5555**, tête **0,7152**, POS **0,7581**. La couverture (196/239) et l'exactitude (195/196) sont, elles, sur le 612 |
| V7-3 | majeure | § 2, colonne « v6 » | la colonne v6 n'est pas homogène : F1 0,5130 est la v6 sur 612, mais tête **0,6826** est la **v5** (v6 : 0,6785 sur 612, 0,6834 sur 602) et POS **0,7475** est la **constante de porte de la v6** (v6 : 0,7461 sur 612, 0,7482 sur 602) | choisir une base et y ramener les trois valeurs de la v6 ; a minima, corriger la tête et la POS |

Les autres mesures se reproduisent : 196 labels, 195/196, 195 top1, 166 top-k, fr 135/135,
en 60/61, 43 spans (21 + 17 + 5), couverture 0,8201, POS 0,7603 (sur 602), F1 0,5595 (sur 602).
La fiche **ne re-mesure pas dev/test** depuis la v6 (§ 3) et n'a pas de contrôle négatif.

### 4.7 gold-split — `85e4082b` (1 écart)

| id | gravité | où | constat | mesure / correction |
|---|---|---|---|---|
| GS-1 | majeure | § 3, ligne 42 | « la couverture reste 160/239, **identique sur les deux moitiés** » | la couverture est **106/163 = 0,6503 en dev** et **54/76 = 0,7105 en test** ; seul le total est 160/239 = 0,6695. Le split n'est pas « identique » |

Tout le reste se reproduit exactement : 422/163/106 en dev, 190/76/54 en test, 612/239/160 au
total ; sources 15/302/105, 5/130/55, 20/432/160 ; langues 277/145, 125/65, 402/210 ; exact
104/106 et 53/54 ; F1 0,4414 / 0,4719 ; tête 0,6347 / 0,6470 ; fr 79/79 et 38/39 ; en 25/27 et
15/15. Les tableaux d'équilibre s'additionnent parfaitement. La fiche ne donne pas le compte de
portes (le commit est à 183/183), n'a pas de contrôle négatif ni de mention d'historique.

## 5. Tableaux : sommes et dénombrements

**Le seul tableau dont la somme visible ne tombe pas** est celui des corrections de la v2 :
`88 + 45 = 133` pour le top-k strict, alors que le total est 141 ; `134` pour le top-k, alors que
le total est 142 ; le +6 top1 du segment n'est pas crédité. Les totaux de la fiche sont justes,
c'est la colonne « gain » qui est incomplète (V2-3).

Tous les autres tableaux de spans s'additionnent : 48 + 33 + 13 = 94 (v2, v3) ; 48 + 21 + 10 = 79
(v4) ; 24 + 12 + 16 = 52 (v5, v6) ; 21 + 17 + 5 = 43 (v7). Les labels et les cibles se recoupent :
135 + 61 = 196 et 135 + 60 = 195 (v7) ; 131 + 56 = 187 (v6) ; 160 = 106 + 54 et 239 = 163 + 76
(gold-split). Le split gold-split s'additionne aussi par sources et par langues, dans les deux
moitiés et au total.

## 6. JSON ↔ texte

| fiche | chiffres du JSON absents du texte | chiffres du texte absents du JSON |
|---|---|---|
| v2 | aucun (les taux sont repris dans le texte) | 60/63, 63/82, 111, 26, 22 = 11 + 11, 46/57, 139/145, r048/r068, la liste des 8 verbes anglais |
| v3 | aucun | tout le bloc A13 (43/96 GP, 143/145, 143/239, p = 0,5, s108/s122), 111/116, 112/116, 26/29, 29/29, la portée 2–3 de R1 |
| v4 | aucun | les effets intermédiaires des corrections (145 → 159, 141 → 145, 0,2937 → 0,4033, 144 → 152, 30 → 38, 152 → 158, 0,4194, 0,5930), les 84 spans de A12, les 38 assertions, le passif 3/3, le 41/42 |
| v5 | `dev.f1` 0,5091, `dev.couverture` 0,773, `test.f1` 0,5217, `test.couverture` 0,8026 ; `candidats_manquants` 26 (seulement implicite) | les dénominateurs 117/118, 126/127, 60/60 ; les 27 échecs ; 0,8556 ; 125/126 ; 59 |
| v6 | aucun | les 26 candidats incomplets, 130/131 (v5), 0,5156 (v5), la tête (non publiée) |
| v7 | aucun | 0,0132 (faux), la répartition « qui » 12, les 32 assertions, la composition 20 + 432 + 160 |
| gold-split | aucun | tout le tableau des sources et des langues, les 79 spans, 160/239, les dénominateurs 79/79, 38/39, 25/27, 15/15, le point 1,9 |

Le déséquilibre le plus net est la **v3** (le JSON n'a pas suivi la réparation du Markdown) et le
**gold-split** (le JSON ne contient que les taux, pas l'équilibre du split qui est l'objet de la
fiche). Inversement, la **v5** est la seule fiche dont le JSON contient des mesures absentes du
texte (F1 et couverture dev/test).

## 7. Contrôles négatifs

| fiche | contrôle négatif | où | verdict |
|---|---|---|---|
| v2 | modèle appris rejeté : 142/145 contre 137, +5, McNemar 7/2, p = 0,18, IC [−0,7 ; +7,6] ; l'audit A8 ajoute permutations et candidat aléatoire | § 3, JSON `modele_appris` | ✅ |
| v3 | complétion naïve des GV 132 (−5) ; R5 sans condition ADV 131 (−6) ; R3(a) 2/4 | § 2, JSON `controles_negatifs` | ✅ |
| v4 | aucun ; les deux règles de A12 « non intégrées » ne sont pas un négatif mesuré | — | ❌ |
| v5 | aucun ; dev/test est un contrôle de généralisation, pas un négatif | — | ❌ |
| v6 | aucun ; dev/test est un contrôle de généralisation, pas un négatif | — | ❌ |
| v7 | aucun ; dev/test n'ont même pas été re-mesurés depuis la v6 | — | ❌ |
| gold-split | aucun ; le split est l'objet de la fiche, sans test de fuite, de permutation ou de mélange | — | ❌ |

## 8. Mentions d'historique

**Aucune des six fiches historiques ne porte de mention d'historique explicite.** Le numéro de
version (v2…v6) et la date 2026-11-05 sont des indices, pas une phrase disant « instantané au
commit X, ne décrit pas l'état courant ». La v2 est appelée « instantané historique » dans
`rapport-audit-v2.md`, mais cette mention est **externe à la fiche**. La v7 est la fiche courante :
elle devrait porter, elle, une mention « état courant au commit `69bd865e` ».

Formulation recommandée, identique pour les six : « **Instantané historique** : état au commit
`<sha>` (2026-11-05) ; ne décrit pas l'état courant `69bd865e` ». Pour la v7 : « **État courant** :
commit `69bd865e` ».

## 9. `reports/README.md` et renvois

Les sept fiches sont référencées : v7 ligne 18, v6 ligne 19, v5 ligne 20, gold-split ligne 21,
v4 ligne 22, v3 ligne 30, v2 ligne 36. **Deux lignes répètent les valeurs périmées du titre** :

- **ligne 20 (v5)** : « exact **185/187 (0,9893)**, … dev/test **125/126** et 60/61 » → corriger en
  **186/187 (0,9947)** et **126/126** et 60/61.
- **ligne 22 (v4)** : « F1 **0,4194**, exact **158/160** » → corriger en **0,4539** et **157/160
  (0,9812)** ; préciser la base (602) ou mettre les valeurs du 612.

La ligne 18 (v7) est juste, mais gagnerait à dire que F1/POS sont sur le 602 et la couverture sur
le 612.

**Renvois de §** : aucune des sept fiches n'utilise de renvoi « cf. § … » ; il n'y a donc aucun
renvoi faux. **Liens relatifs** : tous résolvent (les 4 fiches amont, `bloc_linguistique.py`,
`evaluer_gold.py`, `gold_reel.py`, `gold_split.py`, `autotest.py`).

## 10. Corrections à faire

**P1 — chiffres de tête (à corriger avant toute citation).**

1. **v4, titre** : `0,4194` → **0,4539** (ou 0,4509 sur 612) ; `158/160 (0,9875)` → **157/160
   (0,9812)**.
2. **v4, § 2** : `0,9875` → **0,9812** ; `41/42` → **40/42**.
3. **v4, § 5/§ 6** : « 2 échecs » → **3** ; « six corrections » → **sept**.
4. **v5, titre** : `185/187 (0,9893)` → **186/187 (0,9947)**.
5. **v5, § 2/§ 3/§ 5** : dev `125/126` → **126/126** ; `+28` → **+29** ; `40 → 59` → **40 → 60** ;
   « 27 échecs de cible » → **1 échec de cible + 26 candidats manquants** ; `0,8556` → **0,8610**
   (161/187) ou **0,6736** (161/239) ; « six corrections » → **sept**.
6. **v7, § 3** : `0,0132` → **0,0128**.
7. **v7, en-tête/§ 2** : nommer la base des trois valeurs F1/tête/POS (602 gelé) ou publier les
   valeurs du 612 (0,5555 / 0,7152 / 0,7581) ; corriger la colonne v6 (tête et POS).

**P2 — tableaux et prose.**

8. **v2, § 1** : étiqueter le split « lexical » (60/63 et 63/82), retirer « (POS gold) » et le
   « +48 cibles », ou publier le split POS gold sur le même bloc (97/116 et 26/29).
9. **v2, § 2** : `46` → **45** (et créditer le lexique de +8 top-k/+8 strict, le segment de +6 top1).
10. **v4, § 3** et **v5, en-tête/§ 2** : nommer le gold 602 pour F1/tête, ou republier sur 612.
11. **v6, § 2** : comparer la F1 sur un gold constant (0,5130 → 0,5130 sur 612, ou 0,5164 → 0,5164
    sur 602) ; ne pas comparer 0,5156 (porte v5, 602) à 0,5130 (v6, 612).
12. **gold-split, § 3** : « identique sur les deux moitiés » → **106/163 (0,6503) en dev, 54/76
    (0,7105) en test ; 160/239 (0,6695) au total**.

**P3 — JSON.**

13. **v3** : ajouter le bloc A13 et les comptes (43/96, 143/145, 143/239, p = 0,5, s108/s122,
    111/116, 112/116, 26/29, 29/29).
14. **v2** : ajouter 60/63, 63/82, 111/116, 26/29, 22 = 11 + 11, 46/57, 139/145, r048/r068.
15. **v4** : ajouter les effets intermédiaires des sept corrections (ou les retirer du texte).
16. **v5** : ajouter les dénominateurs et les 27 = 26 + 1 ; **v6** : ajouter les 26 candidats ;
    **v7** : retirer 0,0132 ou le corriger.
17. **gold-split** : ajouter le tableau des sources et des langues, 79 spans / 160/239, et les
    dénominateurs.
18. **Tous les JSON** : ajouter un champ `gold` par mesure (`612 vivant` / `602 gelé`), et le
    `commit` de la fiche.

**P4 — dispositif.**

19. Ajouter la mention d'historique aux six fiches historiques ; ajouter « état courant » à la v7.
20. Ajouter un contrôle négatif à v4, v5, v6, v7 et gold-split (permutation des cibles, candidat
    aléatoire, mélange des identifiants du split).
21. Corriger les lignes 20 et 22 de `reports/README.md` ; préciser la base sur la ligne 18.
22. Ajouter le compte de portes (183/183) à l'en-tête de gold-split.

## 11. Ce qui pourrait rendre ce rapport faux

- **Une correction des fiches après `69bd865e`** : à `e4cd4408`, aucune des sept fiches n'a bougé ;
  si un commit ultérieur les corrige, les écarts V2…V7 disparaissent (c'est le but).
- **Le choix de la base** : les valeurs 612 et 602 sont toutes deux défendables ; le reproche n'est
  pas qu'elles soient fausses, mais que la fiche nomme **612** et publie du **602** sans le dire.
  Si la convention du dépôt est « F1/POS sur le gelé, couverture sur le vivant », il suffit de
  l'écrire : les chiffres sont alors exacts.
- **Les constantes de porte** : pour la v5, 0,5156 / 0,6826 sont dans la tolérance 0,001 de la
  porte T112/T113 (0,5164 / 0,6834). Si la porte est la référence, la fiche est « dans la
  tolérance » ; elle n'est pas exacte au quatrième chiffre.
- **Le statut de « contrôle négatif »** : si le split dev/test est accepté comme contrôle négatif,
  il en manque trois (v4, v6, v7) au lieu de cinq. Nous avons distingué les deux.
- **La mention d'historique** : si le numéro de version et la date suffisent, il n'en manque aucune ;
  nous avons appliqué la lecture stricte de la consigne.
- **Le blob historique** : les mesures historiques sont obtenues avec le `bloc_linguistique.py` du
  commit et `RACINE` forcé à la racine ; un worktree détaché ne suffit pas (S y perd ses données et
  la v6 tombe à 156 labels). Les hashes des quatre fichiers d'or sont identiques de `9d5337ce` à
  `69bd865e`, ce qui sécurise la comparaison.
- **HEAD a bougé** : `69bd865e` → `e4cd4408` pendant l'audit ; seuls `DOCS` et `JOURNAL` ont changé,
  mais un nouveau commit peut invalider la photographie.

## 12. Fichiers

- [`rapport-coherence-fiches-v7.md`](rapport-coherence-fiches-v7.md) — ce rapport.
- [`pensee-coherence-fiches-v7.json`](pensee-coherence-fiches-v7.json) — le registre structuré
  (7 fiches, 23 écarts, 7 lacunes JSON, 5 contrôles négatifs manquants).
- Sources : les sept fiches et leurs JSON, `tools/pensee/autotest.py` aux commits `9d5337ce`,
  `e1903e2d`, `392f03aa`, `b975011b`, `0ec6c27d`, `85e4082b`, `69bd865e` ;
  `tools/bloc_linguistique.py` aux mêmes commits ; `tools/tests/linguistique/evaluer_gold.py`,
  `gold_split.py`, `gold.json`, `gold_reel.json`, `gold_synthetique.json`, `gold_gele.json` ;
  `rapport-audit-v2.md` (A8) pour la v2.
- **Aucune fiche modifiée, aucun commit.** Seuls les deux fichiers de sortie sont neufs.
