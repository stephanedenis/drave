# Audit B13 — l'attachement v2 : 43 valeurs rejouées, 2 arrondis, 1 erreur de prose (46 → 45), 8 docstrings de portes périmées

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅ **chiffres reproduits** ;
> ⚠️ **réserves documentaires** (§ 3, § 4, § 6) — aucune ne change les totaux.
>
> **Audité** : commit **`9d5337ce`** (2026-11-05 14:14), fiche
> [`rapport-pensee-attachement-v2.md`](rapport-pensee-attachement-v2.md) et JSON
> [`pensee-attachement-v2.json`](pensee-attachement-v2.json).
>
> **Dispositif** : depuis la racine, `sys.path.insert(0, '.')` ;
> `evaluer_bloc("h", Heuristique(), charger())` ; le **blob exact du commit v2**
> (`git show 9d5337ce:tools/bloc_linguistique.py`, sha256 `6e843018…`) chargé depuis `/tmp`
> avec `RACINE` forcé à la racine du dépôt. Les ablations sont des copies `/tmp` du même
> blob ; **aucun fichier existant n'a été modifié, aucun commit**. HEAD a bougé pendant
> l'audit (de `de292c7d` à `15ee10d3`) ; jusqu'à ce point, le bloc courant (sha256 `bb020516…`)
> ne différait que par la mémoïsation et redonnait les mêmes chiffres. **Après les mesures v2,
> une intégration v3 (`dcf7bc91`, 15:18) a atterri** : elle change les valeurs (exact 141/145,
> noms 29/29, top1 143, strict 142) et réécrit les assertions des mêmes portes. **Cet audit
> porte sur le commit v2 `9d5337ce`** ; la fiche v2 et ses 180/180 sont un instantané
> historique, pas l'état courant. JSON :
> [`pensee-audit-v2.json`](pensee-audit-v2.json) — 43 comparaisons, 41 écarts nuls, 2 arrondis.

## 1. Verdict

- **Toutes les mesures revendiquées reproduisent** : 145 labels, top1 140, top-k 142, exact
  137, top-k strict 141 ; taux 0,9655 / 0,9793 / 0,9448 / 0,9724 ; rendement 0,5858 / 0,5941
  / 0,5732 ; split 116/111 (0,9569) et 29/26 (0,8966) ; 8 échecs (3 hors candidats, 5 mal
  classés) ; 94 spans (48 REL, 33 SUB, 13 GP) ; avant 126 / 134 / 123 / 88, taux 0,8690 /
  0,9241 / 0,8483 / 0,6069 ; gold 612 = 20 + 432 + 160.
- **Les deux seuls écarts numériques sont des arrondis de la fiche** : `p = 0,18` pour
  `0,179688` et IC `[-0,7 ; +7,6]` pour `[-0,69 ; +7,59]`. Le modèle appris a été rejoué :
  **142/145**, règle **137/145**, gain **+5**, McNemar **7/2**, `p = 0,1797`, bootstrap
  **[-0,69 ; +7,59] pts** — exactement la fiche.
- **Une erreur de prose** : « **46** des 57 échecs étaient des candidats non réduits à leur
  tête » doit se lire « **45** ». Le 46 est l'écart `134 − 88` (sous-chaîne vs strict) ; le
  nombre de têtes candidates égales à la cible est **45** (A2 le dit, le comptage
  indépendant le confirme). Le gain « +45 » est, lui, correct.
- **Une erreur de table** : la colonne « avant » des lignes verbes/noms est étiquetée
  « (POS gold) » alors que **63/82 est l'ancien split lexical** (`_est_verbe` sur le lexique
  pré-v2). Le POS gold appliqué à l'ancien bloc donne **116/29** (verbes 97/116 = 0,8362,
  noms 26/29 = 0,8966). Le « +48 cibles » est `111 − 63`, un mélange de justes et de cibles.
  Le JSON nomme correctement les valeurs avant `verbe_est` / `nom_est`.
- **Portes** : **au commit v2 `9d5337ce`**, les **15 portes citées passent**, avec les valeurs
  revendiquées. Le registre v2 a **180** portes. **Depuis, v3 `dcf7bc91` a réécrit la plupart
  de ces assertions** (exact 141, top1 143, noms 29/29, strict 142, T172 2/2) et le HEAD a
  **181** portes ; le run complet au moment de l'audit (avant v3) donnait **181/181**, et le
  commit v3 annonce 181/181 avec ses valeurs — hors périmètre. Huit docstrings sont périmées
  (T153, T162, T163, T166, T167, T168, T172, T173) ; T168 imprime encore « /146 » et T163
  « 33 avant les correctifs » (33 était un compte d'exacts à `d400e188`, pas un compte
  d'échecs ; l'audit A1 en compte 22).
- **Contrôles** : permutation des cibles (1 000 tirages) moyenne **1,786/145**, max **8**,
  observé **137** (`p < 0,001`) ; candidat aléatoire (1 000 tirages) moyenne **58,566/145**,
  max **75**, observé **137** (`p < 0,001`). Le +45 des têtes vient bien de la réduction des
  candidats (141 → **96** sans les têtes, 0 exact) ; il gonfle aussi la ligne de base du
  candidat aléatoire (43,742 → 58,566, **+10,2 pts**).

## 2. Tableau mesuré / revendiqué

| mesure | revendiqué | mesuré | écart |
|---|---:|---:|---:|
| labels (segments au bon span) | 145 | **145** | 0 |
| top1 | 140 | **140** | 0 |
| top1 / labels | 0,9655 | **0,9655** | 0 |
| top1 / 239 cibles (rendement) | 0,5858 | **0,5858** | 0 |
| top-k (sous-chaîne) | 142 | **142** | 0 |
| top-k / labels | 0,9793 | **0,9793** | 0 |
| top-k / 239 (rendement) | 0,5941 | **0,5941** | 0 |
| **exact** | 137 | **137** | 0 |
| exact / labels | 0,9448 | **0,9448** | 0 |
| exact / 239 (rendement) | 0,5732 | **0,5732** | 0 |
| **top-k strict** (égalité) | 141 | **141** | 0 |
| top-k strict / labels | 0,9724 | **0,9724** | 0 |
| verbe (POS gold) | 111/116 (0,9569) | **111/116 (0,9569)** | 0 |
| nom (POS gold) | 26/29 (0,8966) | **26/29 (0,8966)** | 0 |
| échecs de cible | 8 = 3 hors + 5 mal classés | **8 = 3 + 5** | 0 |
| spans perdus | 94 = 48 REL + 33 SUB + 13 GP | **94 = 48 + 33 + 13** | 0 |
| avant : top1 / top-k / exact / strict | 126 / 134 / 123 / 88 | **126 / 134 / 123 / 88** | 0 |
| avant : taux spans | 0,8690 / 0,9241 / 0,8483 / 0,6069 | **identiques** | 0 |
| avant : split lexical | 63/60 (0,9524) ; 82/63 (0,7683) | **63/60 ; 82/63** | 0 |
| gold | 612 = 20 + 432 + 160 | **612 = 20 + 432 + 160** | 0 |
| modèle appris | 142/145 (0,9793), +5, 7/2, 0,18, [-0,7 ; +7,6] | **142/145, +5, 7/2, 0,179688, [-0,69 ; +7,59]** | arrondis |

Le détail complet des 43 comparaisons est dans `pensee-audit-v2.json`. Les taux sont calculés
avec les dénominateurs de la fiche : **145** labels pour l'exactitude « span », **239** cibles
pour le rendement. `topk_taux` 0,5941 n'est asserté par aucune porte (T162 ne vérifie que le
compte 142) ; il est reproduit mais non couvert.

## 3. D'où viennent les +14 et les +53

Le point le plus utile de l'audit : les trois corrections sont **réelles, additives et
exactement mesurables**. Chaque ligne suivante est une copie `/tmp` du blob v2 avec une seule
correction désactivée, mesurée dans un processus séparé.

| variante | top1 | top-k | exact | top-k strict |
|---|---:|---:|---:|---:|
| avant (`a408a909`) | 126 | 134 | 123 | 88 |
| + têtes des candidats | 126 | 134 | 123 | 133 |
| + têtes + lexique anglais | 134 | 142 | 131 | 141 |
| **v2** (les trois) | **140** | **142** | **137** | **141** |
| v2 − têtes | 140 | 142 | 137 | **96** |
| v2 − lexique | 132 | 134 | 129 | 133 |
| v2 − segment précédent | 134 | 142 | 131 | 141 |
| v2 − helper `_cible_s_par_genre` | 140 | 142 | 137 | 141 |

| correction | gain mesuré | répartition | ids |
|---|---|---|---|
| **têtes des candidats** | **+45 top-k strict**, 0 exact | 26 REL + 19 GP | 45 segments (liste au JSON) |
| **lexique anglais** | **+8 exact, +8 top1, +8 top-k, +8 strict** | 8 GP | r080, r108, r120, r156, r166, r169, r177, r180 |
| **segment précédent** | **+6 exact, +6 top1** | 6 SUB | s012, s030, s052, s097, s124, s139 |
| helper `_cible_s_par_genre` | **0** | — | ajouté au v2, sans effet mesuré, non documenté |

La somme retombe exactement : `88 + 45 + 8 = 141` (strict), `123 + 6 + 8 = 137` (exact),
`126 + 6 + 8 = 140` (top1), `134 + 8 = 142` (top-k). La fiche crédite le segment de **+6 exact
seulement** (il fait aussi **+6 top1**) et le lexique de **+8 exact/+8 top1** (il fait aussi
**+8 top-k/+8 top-k strict**). Les totaux du haut sont justes ; c'est le tableau des
corrections qui ne s'additionne pas tout seul.

**L'erreur « 46 des 57 »** : sur les 57 échecs du top-k strict avant, **45** ont un candidat
`« … » → queue` dont la tête est la cible ; les 45 sont effectivement réparés (133 = 88 + 45).
Le **46** est `134 − 88`, l'écart sous-chaîne/strict, une autre quantité. A2 dit bien 45 ;
notre comptage indépendant donne 45 (26 REL + 19 GP).

## 4. Le split : une reclassification, pas un gain

La matrice complète des 145 labels, avec l'ancien `_est_verbe` (lexique pré-v2) et le POS gold :

| | POS gold VERB | POS gold nom |
|---|---:|---:|
| `_est_verbe` **vrai** | **63** (60 justes) | 0 |
| `_est_verbe` **faux** | **53** (37 justes) | **29** (26 justes) |

- L'ancien split lexical donne **63/60** (0,9524) et **82/63** (0,7683) ;
- le POS gold sur le **même ancien bloc** donne **116/97** (0,8362) et **29/26** (0,8966) ;
- le POS gold sur le **v2** donne **116/111** (0,9569) et **29/26** (0,8966).

Il n'y a **aucune** cible verbe lexical qui devienne nom POS : les 53 sont des noms lexicaux
reclassés en verbes par le POS gold. Le « +48 cibles » de la fiche est `111 − 63`, soit des
justes après moins des cibles avant : ce n'est ni un gain de cibles ni un gain de justes. Le
nombre de cibles verbes passe 63 → 116 (+53) ; les justes 60 → 111 (+51) en comparaison
mixte, ou **97 → 111 (+14) à split POS constant**. Le côté nom est **inchangé** à 26/29. Le
gain d'exact +14 est donc **entièrement du côté verbe** : GP +8 (lexique) et SUB +6 (segment),
REL 0. La fiche le dit en prose (« le split était faux ») mais la table, elle, laisse croire à
un effondrement des noms.

**Multi-cibles** : 36 des 145 labels portent plusieurs `cibles`. `exact` compare à
`cibles[0]` ; `top1` accepte n'importe laquelle. Les 3 cas top1-sans-exact sont r230 (la cible
`appelle` est sous-chaîne de `appelle-moi`) et s108/s122 (la règle choisit `papier`, cible
secondaire ; la cible primaire est le verbe `rêve` / `saute`). C'est une convention du gold,
pas une quatrième correction.

## 5. Les 8 échecs

| id | type | cible | choisi | candidat strict ? | catégorie |
|---|---|---|---|---:|---|
| g002 | GP | chat | — | non | hors candidats (génitif) |
| r309 | SUB | viendra | Peut-être | non | hors candidats |
| s041 | GP | marche | — | non | hors candidats (génitif) |
| g012 | GP | prêt | manger | oui | mal classé |
| r018 | GP | prête | manger | oui | mal classé |
| r230 | SUB | appelle | appelle-moi | **non** (sous-chaîne) | mal classé au sens large |
| s108 | GP | rêve | papier | oui | mal classé (cible secondaire) |
| s122 | GP | saute | papier | oui | mal classé (cible secondaire) |

- **3 hors candidats + 5 mal classés** est exact avec la convention **sous-chaîne** de
  `evaluer_bloc` / T172. En **égalité stricte**, c'est **4/4** : r230 n'a que `appelle-moi`,
  qui contient `appelle` sans être égal. La fiche ne dit pas cette convention.
- Le recouvrement est net : **137** exact sont aussi strict et top1 ; **4** sont stricts sans
  être exacts (g012, r018, s108, s122) ; **1** est top1 sans être strict (r230) ; **3** ne sont
  ni l'un ni l'autre (g002, r309, s041). `137 + 4 + 1 + 3 = 145`.
- A3 (`rapport-classement-appris.md` § 5.4) **qualifie déjà les 8** ; la fiche v2 les dit
  encore « non qualifiés plus finement ». C'est périmé dans le même lot.
- A2 proposait aussi **F3** (repli par tokens : tête du GN à gauche d'un GP, balayage des
  verbes reconnus quand aucun GV, découpage des enclitiques) à **+4 exact/+4 strict** ; la
  fiche v2 n'en dit rien, ni intégration ni rejet. F3 visait **g002, s041, r309 et r230** ;
  les quatre autres (g012, r018, s108, s122) resteraient faux même avec F3. Décision non
  consignée.

## 6. Les portes

**Au commit v2 `9d5337ce`, les 15 portes citées passent** (exécution individuelle, 2026-11-05) :

| porte | attendu | mesuré | état |
|---|---|---|---|
| T153 | cibles 239 ; top1 0,5858 ; exact 0,5732 | 0,5858 ; 0,5732 | ✅ |
| T161 | cibles 239 ; top1 140 ; exact 137 | 140 ; 137 | ✅ |
| T162 | top-k 142 ; tête 142 ; top1 140 | 142 ; 142 ; 140 | ✅ |
| T163 | span 94 ; cible 3 | 94 ; 3 | ✅ |
| T164 | cible `saw` ; exact 137 | `saw` ; 137 | ✅ |
| T166 | 48 REL ; 33 SUB ; 13 GP | 48 ; 33 ; 13 | ✅ |
| T167 | 239 ; 145 ; 0,9655 ; 0,9793 ; 0,9448 | identiques | ✅ |
| T168 | exact 137 ; verbes 116 ; noms 29 | 137 ; 116 ; 29 | ✅ |
| T169 | 116/111/0,9569 ; 29/26/0,8966 | identiques | ✅ |
| T170 | REL `homme` ; GP `joue` | `homme` ; `joue` | ✅ |
| T172 | 3 hors ; 5 mal classés | 3 ; 5 | ✅ |
| T173 | 142 ; 141 ; 0,9724 ; 0,9793 | identiques | ✅ |
| T175 | audit 14/14 ; écarts 0 ; 126/134/123/88 ; 60 | 14/14 ; 0 | ✅ |
| T176 | s052 `ouvre` ; s012 `écoute` | `ouvre` ; `écoute` | ✅ |
| T177 | strict 141 ; 0,9724 | 141 ; 0,9724 | ✅ |

**Portes au total** : **180** au commit v2 ; **181** au HEAD (T178, cache du chunker, ajoutée
après), run complet **181/181** en 5 min 17 s **au moment de l'audit (avant v3)**. La mention
« 180/180 » de la fiche est donc un **instantané daté** : juste au commit v2, périmée au HEAD.
Le JSON `pensee-attachement-v2.json` porte encore `"portes": "180/180"`.

**Depuis, v3 `dcf7bc91` (15:18) a réécrit les assertions** : T153 0,5983/0,59 ; T161 top1 143,
exact 141 ; T162 top1 143 ; T164 exact 141 ; T167 0,9862/0,9724 ; T168 exact 141 ; T169
verbes 112, noms 29/29 ; T171 exact 141 ; T172 2/2 ; T173 strict 142 (0,9793) ; T177 142. Les
docstrings n'ont pas été corrigées et sont encore plus périmées. **La fiche v2 ne doit pas être
comparée aux portes du HEAD** : les mêmes numéros de porte y attendent les valeurs v3.

**Docstrings périmées** (les assertions, elles, sont à jour) :

| porte | docstring | courant |
|---|---|---|
| T153 | « top1 0,5272, exact 0,5105 » | 0,5858 / 0,5732 |
| T162 | « le top-k passe de 78 à 112 (0,4686) » | 142 ; top1 140 |
| T163 | « 94 de span, 33 de cible » | 94 / **3** ; « 33 avant les correctifs » est faux (33 = exacts à `d400e188` ; A1 compte 22 échecs) |
| T166 | « 48 REL, 33 SUB, 12 GP » | 48 / 33 / **13** |
| T167 | « exactitude spans (÷ 146) » | ÷ **145** |
| T168 | « exact 94 » | **137** ; le message imprime « /146 » au lieu de « /145 » |
| T172 | « 11 hors candidats, 11 mal classés » | **3 / 5** |
| T173 | « 88/145 (0,6069), contre 0,9241 » | **141/145 (0,9724)**, contre 0,9793 |

**Chiffres non couverts par une porte** : `topk_taux` 0,5941 ; les taux avant (0,8690 /
0,9241 / 0,8483 / 0,6069) et le split avant nom 82/63 (T175 ne fige que les comptes
126/134/123/88 et `verbe.justes` 60) ; le **69/69 SUB = VERB** (T174 vérifie le texte de
`CONVENTION_CIBLE`, pas le 69/69) ; le **180/180** (la liste est imprimée, pas assertée) ; les
chiffres du **modèle appris** (aucune porte ne lit `classement_cible.py`) ; le **46/57** de la
prose. T175 est un **instantané pré-v2 volontaire**, pas une porte périmée : il vérifie
126/134/123/88 et le courant 239/145.

## 7. Les contrôles

| contrôle (1 000 tirages, graine 20261105) | observé | moyenne | écart-type | min–max | p | ratio |
|---|---:|---:|---:|---:|---:|---:|
| permutation des cibles (v2) | 137 | 1,786 | 1,347 | 0–8 | < 0,001 | 76,7× |
| candidat aléatoire (v2) | 137 | 58,566 | 5,517 | 42–75 | < 0,001 | 2,34× |
| candidat aléatoire (v2 sans têtes) | 137 | 43,742 | 4,618 | 30–58 | < 0,001 | 3,13× |
| candidat aléatoire (avant, A1) | 123 | 39,754 | 4,530 | 27–52 | < 0,001 | 3,09× |

- **Permutation** : aucune des 1 000 permutations n'atteint 137 ; le score est hors
  distribution. La moyenne v2 (1,786) est un peu au-dessus de l'ancienne (1,617 dans l'audit
  A1 ; 1,642 avec notre implantation) parce que les cibles prédites sont plus concentrées.
- **Candidat aléatoire** : 137 contre 58,57 en moyenne, max 75 : l'attachement choisi reste
  très au-dessus du tirage dans la même liste. Mais la **ligne de base monte** de 39,75
  (avant) à 58,57 (v2), dont **+10,2 pts** pour les seules têtes (43,74 → 58,57) : le top-k
  strict mesure la **couverture des candidats**, pas l'exactitude de la règle. C'est cohérent
  avec A2 (« l'emballage ») ; il ne faut pas lire 0,9724 comme 97 % d'attachement correct.
- Le contrôle `attachement_hasard` de `evaluer_gold.main` (1/239 = 0,0042) est un contrôle
  faible, cible gold contre cible gold ; les deux contrôles ci-dessus sont les vrais.
- **Recouvrement** : 137 exact = 137 top1 = 137 strict ; 4 stricts-sans-exact ; 1 top1-sans-
  strict ; 3 ni l'un ni l'autre. Voir § 5.

## 8. Le modèle appris

Rejoué avec `tools/tests/linguistique/classement_cible.py` (JSON écrit dans `/tmp`, aucun
fichier du dépôt touché ; 25,7 s) : **142/145** hors-pli (0,9793) contre **137/145** (0,9448)
pour la règle live, **+5**, McNemar **7/2**, `p = 0,179688`, bootstrap 2 000 tirages
**+0,0345 [-0,0069 ; +0,0759]** (soit **[-0,7 ; +7,6] pts**), rang 0 seul **139/145**,
régressions **r048 / r068**. La fiche et le JSON sont exacts sur ce bloc ; la décision
**« rejeté »** est justifiée (IC contient 0, gain non significatif). Ce n'est pas une porte :
aucune porte ne lit ce résultat.

## 9. Limites de cet audit (et ce qui pourrait le rendre faux)

- **Le replay du bloc pré-v2 depuis `/tmp` exige `RACINE` = racine du dépôt.** Sinon
  `import generateur` (dans `tools/structures`) échoue à froid, `_syntagmes_s` renvoie `None`
  et l'ancien bloc ne rend que **77 labels / 0 exact**. Ce n'est pas un défaut du v2, mais la
  méthode de replay de l'audit A1 (`git show` vers `/tmp`) est fragile sur ce point ; avec
  `RACINE` corrigé, les 126/134/123/88 et 11/11 reproduisent exactement.
- **Le top-k strict est une couverture**, pas une exactitude : les têtes gonflent la ligne de
  base du candidat aléatoire (§ 7). L'exact/top1 (137/140) est la mesure robuste.
- **Le +8 du lexique est une borne haute** : les 8 verbes anglais ajoutés sont exactement les
  8 cibles anglaises du gold (r080, r108, r120, r156, r166, r169, r177, r180). Le gain est
  ajusté au gold ; il ne prouve pas la généralisation.
- **36/145 labels ont plusieurs cibles** ; `exact` lit `cibles[0]`, `top1` accepte les autres.
  Les 3 top1-sans-exact sont r230 (sous-chaîne) et s108/s122 (cible secondaire).
- **Le split 3/5** dépend de la convention sous-chaîne de T172 ; en strict, c'est 4/4.
- **Le HEAD a bougé** (de `de292c7d` à `15ee10d3`) et le bloc v2-compatible a reçu une
  mémoïsation (`bb020516…` contre `6e843018…` au v2) : mêmes chiffres. **Puis v3 `dcf7bc91` a
  atterri après les mesures** (`9da6dee7…`) : exact 141/145, top1 143, noms 29/29, strict 142.
  Les chiffres v2 de cette fiche sont donc **historiques** ; v3 est hors périmètre et ne doit
  pas être mélangé aux 137/140/141.
- **Les 94 spans perdus** (48 REL, 33 SUB, 13 GP) sont inchangés : le 0,9448 est conditionnel
  aux 145 labels ; le rendement /239 (0,5732) est plafonné par la couverture 0,6067. Une
  correction d'attachement ne répare pas les spans.
- **F3** (+4 exact/+4 strict selon A2) n'est ni intégré ni discuté dans la fiche ; il visait
  g002, s041, r309 et r230. g012, r018, s108 et s122 resteraient faux même avec F3.
- **Le gold est vivant** ; les sha256 des trois JSON sont épinglés dans
  `pensee-audit-v2.json` (mêmes empreintes que l'audit A1). Le sous-module `tools/structures`
  est au commit `523d8c1` ; sa modification de travail (`donnees/paragraphes-validations.jsonl`)
  n'est lue que par `serveur.py`, pas par `generateur`.
- **Ce que l'audit ne dit pas** : il ne rejoue pas les 180/181 portes du registre complet
  (seulement les 15 citées et le run du moment, 181/181), ne teste pas la généralisation du
  lexique, ne tranche pas la convention du gold quand plusieurs cibles sont possibles, et
  **n'audite pas v3** (`dcf7bc91`), arrivé après les mesures.

## 10. Fichiers

- [`rapport-pensee-attachement-v2.md`](rapport-pensee-attachement-v2.md) — la fiche auditée.
- [`pensee-attachement-v2.json`](pensee-attachement-v2.json) — son JSON.
- [`pensee-audit-v2.json`](pensee-audit-v2.json) — les 43 comparaisons, la décomposition, les
  contrôles et le détail des portes.
- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — le bloc ; le blob v2 mesuré est
  `6e843018…`. Le HEAD v2-compatible était `bb020516…` (mémoïsation seule) ; le commit v3
  `dcf7bc91` est `9da6dee7…` (hors périmètre), et le HEAD a encore avancé (`b1b1292f`, cache
  T178) après v3.
- [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) — `charger()`,
  `evaluer_bloc`.
- [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py) — `CONVENTION_CIBLE`.
- [`autotest.py`](../tools/pensee/autotest.py) — T153, T161–T177.
- [`rapport-topk-diagnostic.md`](rapport-topk-diagnostic.md) — A2 (45 échecs d'emballage).
- [`rapport-classement-appris.md`](rapport-classement-appris.md) — A3 (8 échecs qualifiés,
  modèle rejeté).
- [`rapport-audit-attachement.md`](rapport-audit-attachement.md) — A1 (les 14 valeurs
  pré-v2 et les contrôles de référence).
- [`rapport-pensee-attachement-v3.md`](rapport-pensee-attachement-v3.md) — l'état suivant,
  hors périmètre : exact 141/145, noms 29/29.
