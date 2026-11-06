# Audit v7 — 195/196 sur les deux golds, mais cinq valeurs de qualité sont gelées

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 ·
> **Commit audité** : `69bd865e` (branche `s/v7`) · **Verdict** : ✅ chiffres reproduits ;
> ⚠️ cinq valeurs sont mesurées sur le **gold gelé 602**, la colonne « avant » n'est pas la v6,
> et deux récits de la fiche sont faux.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`Heuristique`,
> `_syntagmes_simple`, `_cible_precedent`, `_cible_hors_span`),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) (`charger`, `evaluer_bloc`),
> [`gold_split.py`](../tools/tests/linguistique/gold_split.py) (`dev`, `test`),
> [`autotest.py`](../tools/pensee/autotest.py) (183 portes) · **JSON** :
> [`pensee-audit-v7.json`](pensee-audit-v7.json).

## 1. Le verdict en une page

| question | réponse |
|---|---|
| les chiffres de la fiche sont-ils rejouables ? | **oui**, au commit `69bd865e`, sans modifier le code |
| sur le même gold ? | **non** : POS, F1, S, chunker et tête viennent du **gelé 602** ; le reste est identique sur le vivant 612 |
| la colonne « avant » est-elle la v6 ? | **non** : POS = v4, tête = v5a, F1 = v6 vivant |
| les 183 portes ? | **183/183**, zéro échec |
| les contrôles négatifs ? | permutation 1,81/196 (0,92 %) ; par type+langue 9,40/196 (4,79 %) ; observé 195/196 |
| dev/test ? | **dev 133/134 (0,9925)**, **test 62/62 (1,0)** ; F1 0,5512 / 0,5651 ; couverture 0,8221 / 0,8158 |

**Les invariants de l'attachement** — identiques sur les deux golds : **196 labels**, **195 exacts**
(0,9949), **couverture 196/239 = 0,8201**, **top-k 166/239 = 0,6946**, **fr 135/135**,
**en 60/61**, **43 spans perdus (21 REL, 17 SUB, 5 GP)**. Ces chiffres-là sont solides : les
10 phrases ajoutées après le gel n'ont **aucune cible**, donc elles ne peuvent pas changer
l'exact, les labels, la couverture ni le top-k.

**Les cinq valeurs qui changent** — la fiche donne les valeurs du **gelé 602** ; sur le **vivant
612**, elles sont plus basses :

| mesure | fiche (gelé 602) | vivant 612 | écart |
|---|---:|---:|---:|
| POS | **0,7603** | **0,7581** | −0,0022 |
| F1 union | **0,5595** | **0,5555** | −0,0040 |
| F1 S | **0,4741** | **0,4688** | −0,0053 |
| F1 chunker | **0,5858** | **0,5822** | −0,0036 |
| F1 tête | **0,7205** | **0,7152** | −0,0053 |

**Deux récits faux** :
1. le POS contextuel ne rend pas **neuf** labels mais **huit** (196 − 188), et **+0,0118** de POS
   sur le gelé (**+0,0116** sur le vivant), pas +0,0132 ;
2. l'exemple `SUB « that she would come »` n'est **pas** produit : la prédiction est
   `SUB « that she »` (span 9–17) et le span gold reste parmi les 43 perdus.

**Le dispositif des portes est juste mais daté** : 183/183, aucune porte rouge, mais **26
docstrings** portent encore les chiffres d'avant v7 et **6 messages** affichent un dénominateur
`/145` qui n'existe plus (196 labels). Aucune porte ne couvre **dev/test**.

## 2. Protocole

- **Commit** : `git rev-parse HEAD` = `69bd865ec1bae1958b6f617bde4bf685a15d7d67`. Le working tree
  portait déjà des modifications de journaux et de `reports/` d'autres sessions ; nous n'avons
  modifié aucun fichier existant et n'avons écrit que les deux fichiers de cet audit.
- **Gold vivant** : `evaluer_gold.charger()` = **612 phrases** (20 `hand`, 432 `reel`, 160
  `synthetique`), 3179 tokens, 1863 segments, **239 cibles**.
- **Gold gelé** : `evaluer_gold.charger_gele()` = **602 phrases** (20 `hand`, 422 `reel`, 160
  `synthetique`), 3141 tokens, 1831 segments, **239 cibles**.
- **Mesure** : `evaluer_bloc("heuristique", Heuristique(), phrases)`, puis les champs
  `attachement`, `syntagme` et `pos`. L'exact est la cible juste **parmi les labels au bon span**
  (`exact / labels` = 195/196) ; la couverture est `labels / cibles` = 196/239.
- **Portes** : `PYTHONPATH=. python3 -m tools.pensee.autotest` → **183/183**, 0 échec.
- **Contrôles négatifs** : 1 000 tirages par contrôle, graine fixe `20261105` ; permutations
  globales, par type, par langue, par type+langue ; candidat aléatoire dans la liste du label,
  dans le pool global, cible uniforme ; listes de candidats permutées pour le top-k.
- **Ablations** : copie locale de `bloc_linguistique.py` dans `/tmp` (aucun fichier du dépôt
  modifié), `RACINE` repointée vers le dépôt pour que le générateur S reste accessible. Trois
  variantes : POS contextuel retiré, segment précédent retiré, puis les deux moitiés de la règle
  du précédent séparément (cible / candidats).
- **dev/test** : `gold_split.dev(charger())` et `test(charger())` ; le split est
  `crc32(str(id)) % 3 == 0 → test`, non stratifié, vérifié a posteriori.

Reproduction minimale :

```bash
python3 tools/tests/linguistique/evaluer_gold.py
PYTHONPATH=. python3 -m tools.pensee.autotest
```

## 3. Les valeurs, une par une

| mesure | fiche v7 | vivant 612 | gelé 602 | écart vivant | statut |
|---|---:|---:|---:|---:|---|
| labels au bon span | 196 | **196** | **196** | 0 | ✅ |
| exact / labels | 195 | **195** | **195** | 0 | ✅ |
| exact / labels (taux) | 0,9949 | **0,9949** | **0,9949** | 0 | ✅ |
| couverture (labels / 239) | 0,8201 | **0,8201** | **0,8201** | 0 | ✅ |
| top-k (/ 239) | 166 | **166** | **166** | 0 | ✅ |
| top-k (taux / 239) | 0,6946 | **0,6946** | **0,6946** | 0 | ✅ |
| POS (token) | 0,7603 | **0,7581** | **0,7603** | −0,0022 | ⚠️ gelé |
| F1 syntagmes (union) | 0,5595 | **0,5555** | **0,5595** | −0,0040 | ⚠️ gelé |
| F1 S (union=False) | 0,4741 | **0,4688** | **0,4741** | −0,0053 | ⚠️ gelé |
| F1 chunker (union=False, S off) | 0,5858 | **0,5822** | **0,5858** | −0,0036 | ⚠️ gelé |
| F1 tête du découpage | 0,7205 | **0,7152** | **0,7205** | −0,0053 | ⚠️ gelé |
| français (exact / labels) | 135/135 | **135/135** | **135/135** | 0 | ✅ |
| anglais (exact / labels) | 60/61 | **60/61** | **60/61** | 0 | ✅ |
| spans perdus (REL/SUB/GP) | 43 (21/17/5) | **43 (21/17/5)** | **43 (21/17/5)** | 0 | ✅ |
| exact global (exact / 239) | absent | **195/239 = 0,8159** | **0,8159** | 0 | ⚠️ non écrit |
| top-k span (top-k / 196) | absent | **166/196 = 0,8469** | **0,8469** | 0 | ⚠️ non écrit |

Deux précisions de lecture :

- **« tête » = `syntagme.tete.f1`**, la F1 par tête du découpage (0,7205 gelé / 0,7152 vivant),
  pas `attachement_tete` (0,9949 sur 196 labels). La fiche ne confond pas les deux, mais le mot
  « tête » est ambigu dans le dépôt.
- **l'exact global 195/239 = 0,8159** n'est pas dans la fiche ni dans le JSON ; il est pourtant
  asserté par T153, et c'est le produit exact de la couverture (196/239) par l'exact conditionnel
  (195/196) : 0,8201 × 0,9949 = 0,8159. Le **top-k span 166/196 = 0,8469** est de même absent de
  la fiche, alors que T167/T173/T177 l'assertent.

## 4. Le gold : 612 vivant, 602 gelé

Les deux golds ne diffèrent que par **10 phrases réelles ajoutées après le gel** (`r423` à
`r432`), **toutes sans cible** :

| | vivant | gelé | différence |
|---|---:|---:|---:|
| phrases | 612 | 602 | 10 |
| tokens | 3179 | 3141 | 38 |
| segments gold | 1863 | 1831 | 32 |
| cibles | 239 | 239 | **0** |
| labels prédits | 196 | 196 | **0** |

Ces 10 phrases (`Tu viens demain.`, `Il mange.`, `Elle dort.`, `Ils partent.`, `You come tomorrow.`,
`Il pleut.`, `On dit que c'est vrai.`, `Elle est partie.`, `Ils sont arrivés.`, `It rains.`) sont
courtes et sans cible : elles ajoutent 38 tokens et 32 segments, ce qui **baisse** la POS de
0,7603 à 0,7581 et la F1 de 0,5595 à 0,5555. Elles ne touchent ni l'exact, ni les labels, ni la
couverture, ni le top-k, ni les spans.

C'est pourquoi `python3 tools/tests/linguistique/evaluer_gold.py`, qui utilise `charger()` par
défaut, affiche **0,5555 / 0,7581 / 0,7152** : un lecteur qui rejoue la fiche sans savoir qu'elle
est gelée conclut à un écart. La fiche dit pourtant « **le gold 612** : 432 réels + 160
synthétiques + 20 de `gold.py` » (§ 3) ; les cinq valeurs de qualité, elles, sont sur le 602. Le
JSON n'a **aucun champ `gold`** qui permettrait de le voir.

**Ce qui est invariant** : labels 196, exact 195, 0,9949, couverture 0,8201, top-k 166, fr
135/135, en 60/61, spans 43 (21/17/5). **Ce qui est gelé** : POS, F1 union, F1 S, F1 chunker,
F1 tête.

## 5. L'« avant » n'est pas la v6

La colonne « avant » du tableau de la fiche (et le bloc `avant` du JSON) mélange trois états :

| valeur « avant » | fiche | v6 vivant | v6 gelé | provenance réelle |
|---|---:|---:|---:|---|
| POS | 0,7475 | 0,7461 | 0,7482 | **v4 gelé** (0,7475) |
| F1 union | 0,5130 | **0,5130** | 0,5164 | **v6 vivant** |
| F1 tête | 0,6826 | 0,6785 | 0,6834 | **v5a gelé** (0,6826) |
| labels | 187 | 187 | 187 | v6 |
| exact | 187 | 187 | 187 | v6 |
| couverture | 0,7824 | 0,7824 | 0,7824 | v6 |
| spans | 52 | 52 | 52 | v6 |

Le POS 0,7475 est l'ancienne valeur de T107, mesurée sur le **v4**. La tête 0,6826 est l'ancienne
valeur de T113, mesurée sur le **v5a** (`7a9f0d6a`). Seule la F1 0,5130 est bien la v6, et elle est
mesurée sur le **vivant**. La v6, elle, donne :

| mesure | v6 vivant | v6 gelé |
|---|---:|---:|
| POS | 0,7461 | 0,7482 |
| F1 union | 0,5130 | 0,5164 |
| F1 tête | 0,6785 | 0,6834 |
| S | 0,4530 | 0,4582 |
| chunker | 0,5321 | 0,5351 |

Les deltas affichés par la fiche sont donc des **deltas de golds différents** :

| delta | fiche | v6 vivant → v7 vivant | v6 gelé → v7 gelé |
|---|---:|---:|---:|
| POS | +0,0132 (texte) / +0,0128 (table) | **+0,0120** | **+0,0121** |
| F1 union | +0,0465 | **+0,0425** | **+0,0431** |
| F1 tête | +0,0379 | **+0,0367** | **+0,0371** |
| labels | +9 | **+9** | **+9** |
| exact | +8 | **+8** | **+8** |
| couverture | +0,0377 | **+0,0377** | **+0,0377** |
| top-k | +5 | **+5** | **+5** |
| spans | −9 | **−9** | **−9** |

Le « +0,0132 » du texte n'est même pas la différence des valeurs affichées (0,7603 − 0,7475 =
0,0128). Le vrai gain POS est **+0,0118** (gelé) ou **+0,0116** (vivant). Le gain F1 est
**+0,0425** (vivant) ou **+0,0431** (gelé), pas +0,0465. Le gain tête est **+0,0367** / **+0,0371**,
pas +0,0379. Les deltas d'attachement (labels, exact, couverture, top-k, spans) sont, eux, corrects.

## 6. Les portes : 183/183, mais un dispositif daté

### 6.1 Le run

```
183/183 portes tenues
```

Le compte est exact : la liste `portes` de `main()` contient 183 entrées, et le run n'a produit
aucun `❌`. Les 32 fonctions touchées par le commit `69bd865e` dans `autotest.py` sont bien celles
qui portent les valeurs v7 ; le « 32 assertions recalées » de la fiche est donc exact au sens
« 32 fonctions ».

### 6.2 Ce que chaque porte citée attend

| porte | gold | assertion | mesure au HEAD | statut |
|---|---|---|---|---|
| T86-T90 | `gold_reel` (sous-ensembles) | T86 0,8452 / 0,8221 ; T87 0,7353 ; T88 0,7236 ; T89 0,7327 ; T90 0,719 | idem | ✅ |
| T107 | **gelé 602** | 602 phrases, POS 0,7603 | 602, 0,7603, tête 0,7205 | ✅ |
| T110 | **gelé 602** | S 0,4741, chunker 0,5858 | idem | ✅ |
| T111 | **gelé 602** | tête hybride 0,7265 | 0,7265 | ✅ |
| T112 | **gelé 602** | union F1 0,5595 | 0,5595 | ✅ |
| T113 | **gelé 602** | F1 0,5595, tête 0,7205 | idem | ✅ |
| T114 | **gelé 602** | cascade 0,5864 / 0,7285, 602 appels | idem | ✅ |
| T115 | **gelé 602** | tête cascade 0,6709 | 0,6709 | ✅ |
| T119 | **gelé 602** | résumé 0,7465 / 0,6914 | idem | ✅ |
| T138 | vivant 612 | confiance 0,7465, niveau 0,3454 | idem | ✅ |
| T141 | vivant 612 | POS 0,7581 | 0,7581 | ✅ |
| T153 | vivant 612 | top1 0,8159, exact 0,8159, cibles 239 | 0,8159 ; couverture 0,8201 imprimée | ✅ |
| T156 | vivant 612 | 257/546 | 257/546 (0,4707) | ✅ |
| T157 | vivant 612 | 231 rôles, 151 avant, 46 après | 231 / 151 / 46 | ✅ |
| T161 | vivant 612 | top1 195, exact 195, cibles 239 | 195/239 | ✅ |
| T162 | vivant 612 | top-k 166, tête topk 167, top1 195 | 166/239 (0,6946), tête 167 | ✅ |
| T163 | vivant 612 | 43 spans, 30 échecs de cible | 43 / 30 | ✅ |
| T164 | vivant 612 | cible `saw`, exact 195 | `saw`, 195/239 | ✅ |
| T166 | vivant 612 | 21 REL, 17 SUB, 5 GP | 21 / 17 / 5 | ✅ |
| T167 | vivant 612 | 196 labels, 0,9949 / 0,8469 / 0,9949 | idem | ✅ |
| T168 | vivant 612 | exact 195, 137 verbes, 59 noms | 195 ; 137 / 59 | ✅ |
| T169 | vivant 612 | verbes 136/137, noms 59/59 | 136/137 (0,9927), 59/59 | ✅ |
| T171 | vivant 612 | exact 195 | 195 | ✅ |
| T172 | vivant 612 | 1 hors candidats, 0 mal classé | 1 / 0 | ✅ |
| T173 | vivant 612 | top-k 166, topk_exact 166, 0,8469 | 166 / 166 / 0,8469 | ✅ |
| T177 | vivant 612 | topk_exact 166, 0,8469 | 166, 0,8469 | ✅ |
| T179 | vivant 612 | exact 195, exact_any 195, 0,9949 | 195 / 195 / 0,9949 | ✅ |
| T180 | vivant 612 | fr 135/135, en 60/61 | idem | ✅ |

**Aucune assertion n'est fausse.** Deux portes qui semblent se contredire ne mesurent pas la même
chose : **T163** compte les **30 labels** (justes ou faux) dont la cible n'est pas dans
`candidats` ; **T172** ne compte que les **échecs d'attachement** dont la cible manque dans
`candidats` (**1**, r102). D'où 30 contre 1, sans contradiction.

Les portes qui portent les cinq valeurs « gelées »
(T107, T110, T112, T113) et les autres portes gelées (T111, T114, T115, T119) utilisent
`charger_gele()` ; celles qui portent l'attachement (T138, T141, T153, T156, T157, T161-T164,
T166-T169, T171-T173, T177, T179, T180) utilisent `charger()` ; T86-T90 utilisent
`gold_reel.construire()`. Le « 183/183 » est donc vrai, mais il certifie **deux golds différents**
sans le dire.

### 6.3 Les portes périmées (docstrings et messages)

**26 docstrings** portent encore des chiffres d'avant v7. Les plus trompeurs :

| porte | docstring | valeur v7 |
|---|---|---|
| T107 | « 522 phrases, POS 0,7586 » | 602 phrases, POS 0,7603 |
| T110 | « S 0,4582, chunker 0,5351, tête 0,6358 / 0,7006 » | S 0,4741, chunker 0,5858, tête 0,6518 / 0,7441 |
| T112 / T113 | « F1 0,2833, tête 0,5027 » | F1 0,5595, tête 0,7205 |
| T141 | « POS 0,7455 (+0,0011) sur les 432 phrases » | POS 0,7581 sur 612 phrases |
| T153 | « top1 0,5983, exact 0,5900 » | top1 0,8159, exact 0,8159 |
| T156 | « 221/637 (0,3469) » | 257/546 (0,4707) |
| T157 | « 322 GN sans rôle : 129 avant, 172 après » | 231 sans rôle, 151 avant, 46 après |
| T162 / T173 | « top-k 142/145 (0,9793) » | top-k 166/196 (0,8469) |
| T166 | « 48 REL, 33 SUB, 13 GP (94) » | 21 REL, 17 SUB, 5 GP (43) |
| T172 | « 2 hors candidats, 2 mal classés, exact 141/145 » | 1 hors candidats, 0 mal classé, exact 195/196 |
| T177 | « le top-k strict passe de 88 à 141 » | 166 |
| T179 | « 43 GP ont deux cibles ; exact_any 143/145 » | exact_any 195/196 |
| T86-T90 | POS 0,8214/0,7897, 0,6471, 0,6829, 0,7013, 0,6984 | 0,8452/0,8221, 0,7353, 0,7236, 0,7327, 0,719 |
| T111 / T114 / T115 / T119 / T138 | 0,4183 ; 0,3203/0,4817 ; 0,455/0,441 ; 0,7834/0,7472 ; 0,7424/0,3432 | 0,7265 ; 0,5864/0,7285 ; 0,6709 ; 0,7465/0,6914 ; 0,7465/0,3454 |

**6 messages de portes** affichent un dénominateur `/145` qui n'existe plus (196 labels) :

- T161 : `tête 195/145` (devrait être `195/196`) ;
- T162 : `tête 167/145` (devrait être `167/196`) ;
- T168 : `exact 195/145` (devrait être `195/196`) ;
- T171 : `exact 195/145` ;
- T177 : `166/145` ;
- T179 : `exact 195/145, exact_any 195/145`.

Ces messages sont **mathématiquement impossibles** (195 > 145) et un lecteur qui ne regarde que
la sortie peut croire à un dénominateur de 145. Les assertions, elles, sont justes.

### 6.4 Les chiffres non couverts

- **dev/test** : aucune porte ne mesure `gold_split.dev` / `test`. Les **133/134** et **62/62**
  mesurés ici (et les 126/126, 61/61 de la v6) reposent sur des scripts ad hoc, pas sur le
  registre.
- **POS vivant 0,7581 et F1 vivant 0,5555** : T141 couvre la POS vivante, T112/T113 couvrent la
  F1 gelée, mais aucune porte n'associe les deux valeurs vivantes dans un même snapshot. Celui qui
  rejoue `evaluer_gold.py` obtient 0,5555/0,7581 sans qu'une porte ne confirme le couple dans un
  même snapshot.
- **couverture 0,8201** : T153 l'affiche mais ne l'asserte pas ; elle est impliquée par T167
  (`labels == 196` et `cibles == 239`), pas testée directement.
- **exact global 195/239 = 0,8159** : asserté par T153, absent de la fiche et du JSON.
- **top-k span 166/196 = 0,8469** : asserté par T167/T173/T177, absent de la fiche.
- **T114/T115/T119/T138/T156/T157** : valeurs recalées par le commit, mais aucune n'apparaît dans
  la fiche v7. Ce n'est pas une faute — la fiche ne prétend pas tout dire — mais le « 183/183 »
  couvre plus que les 14 lignes du tableau.
- **T154/T155/T175** : contrôles de structure ou instantanés (1624/1863 segments sans cible,
  294 GN / 206 GV, audit v4 avec `labels 145`, `top1 126`, `exact 123`) ; ils passent, mais ils ne
  couvrent aucune valeur v7. T175 ne demande que `labels >= 145` sur le courant.

## 7. Contrôles négatifs

Les contrôles portent sur les **196 labels au bon span**. L'observé est **195/196 = 0,9949** en
exact et **166/196 = 0,8469** en top-k. 1 000 tirages par contrôle, graine `20261105`.

| contrôle | mesure | moyenne /196 | taux | min–max | p(≥ observé) |
|---|---|---:|---:|---:|---:|
| permutation des cibles (globale) | exact | 1,81 | 0,92 % | 0–7 | < 0,001 |
| permutation par type | exact | 5,16 | 2,63 % | 0–13 | < 0,001 |
| permutation par langue | exact | 3,47 | 1,77 % | 0–13 | < 0,001 |
| permutation par type + langue | exact | **9,40** | **4,79 %** | 2–20 | < 0,001 |
| permutation des listes de cibles | exact | 1,90 | 0,97 % | 0–7 | < 0,001 |
| cible uniforme (239 cibles) | exact | 1,93 | 0,98 % | 0–8 | < 0,001 |
| candidat aléatoire (liste du label) | exact | **70,24** | **35,84 %** | — max 92 | < 0,001 |
| candidat aléatoire (pool global) | exact | 0,76 | 0,39 % | — max 4 | < 0,001 |
| listes de candidats permutées | top-k | 2,46 | 1,26 % | 0–8 | < 0,001 |

Lecture :

- **Le contrôle le plus conservateur** (permutation par type + langue) laisse une chance de
  9,40/196 = 4,79 %, avec un maximum de 20/196 sur 1 000 tirages. L'observé 195/196 est à
  **175 unités** au-dessus du maximum : le signal n'est pas un artefact de la distribution des
  cibles ni du mélange REL/SUB/GP ou fr/en.
- **Le candidat aléatoire dans la liste du label** monte à 70,24/196 = 35,84 % (max 92) : les
  listes de candidats sont **informatives** (le gold y est présent 166 fois sur 196, longueur
  moyenne 2,47). Mais le choix du bon candidat vaut **63,65 points** de plus que le tirage au sort
  dans cette liste : l'attachement n'est pas un effet des candidats.
- **Les candidats permutés** font tomber le top-k de 166/196 (84,69 %) à 2,46/196 (1,26 %) :
  les candidats sont bien **propres au label**, pas un sac de verbes commun.
- Le contrôle `attachement_hasard` déjà présent dans `evaluer_gold.py` (0,0042) est un contrôle de
  **sous-chaîne** sur les 239 cibles ; il n'est pas comparable à une permutation exacte sur 196
  labels. Il reste valide comme garde-fou grossier, pas comme contrôle principal.

## 8. Ablations

### 8.1 Retirer la règle du segment précédent

Variante : `_cible_precedent` rend `None`, `_candidats_precedent` rend `[]`, et la branche inline
de la voie S (`if s.get("type") in ("REL", "SUB")`) est désactivée. Mesure sur le gelé 602 :

| variante | labels | exact | exact/labels | couverture | top-k | fr | en | dev | test |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| témoin | 196 | 195 | 0,9949 | 0,8201 | 166 | 135/135 | 60/61 | 133/134 | 62/62 |
| sans segment précédent | 196 | **160** | **0,8163** | 0,8201 | 166 | 115/135 | 45/61 | 105/134 | 55/62 |

La règle vaut **35 attachements exacts** (195 − 160), **20 en français**, **15 en anglais**,
**28 en dev**, **7 en test**. Elle ne change ni les labels, ni la couverture, ni le top-k, ni la
POS/F1/tête : c'est une règle d'attachement pur.

**La moitié « candidats du précédent » est redondante** : en ne retirant que
`_candidats_precedent` (la cible reste), **tous les chiffres sont identiques au témoin** (195/196,
top-k 166, fr 135/135, en 60/61, dev 133/134, test 62/62). En ne retirant que la cible
(`_cible_precedent` + branche S), on retrouve exactement le 160/196. Autrement dit, en v7, le
top-k 166 vient des **noms S et des verbes proches**, pas des candidats du précédent ; la règle
du précédent ne porte que la cible. C'est un point à noter pour la fiche amont v5, qui créditait
les candidats du précédent d'un gain de top-k.

### 8.2 Retirer le POS contextuel

Variante : le bloc « 3 bis » (un `VERB` de suffixe après `DET`/`PREP`/`ADJ` devient `NOUN`) est
supprimé. Mesure sur le gelé 602 :

| variante | POS | labels | exact | exact/labels | couverture | top-k | F1 | tête | fr | en | dev | test |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| témoin | 0,7603 | 196 | 195 | 0,9949 | 0,8201 | 166 | 0,5595 | 0,7205 | 135/135 | 60/61 | 133/134 | 62/62 |
| sans POS contextuel | **0,7485** | **188** | **188** | **1,0** | **0,7866** | **159** | **0,5534** | **0,7185** | 135/135 | **53/53** | **126/126** | 62/62 |

Sur le vivant : POS 0,7581 → **0,7465**, labels 196 → **188**, exact 195 → **188**, couverture
0,8201 → **0,7866**, top-k 166 → **159**, F1 0,5555 → **0,5495**, tête 0,7152 → **0,7133**,
en 60/61 → **53/53**, fr 135/135 inchangé.

Le vrai effet du POS contextuel est donc :

- **+8 labels** (196 − 188), pas +9 ; **+7 exacts** (195 − 188), et l'exact conditionnel passe
  de 1,0 à 0,9949 : les 8 labels achetés sont anglais, et l'un d'eux (r102) est faux ;
- **+0,0118 de POS** sur le gelé (0,7603 − 0,7485), **+0,0116** sur le vivant, pas +0,0132 ;
- **+7 de top-k** (166 − 159), **+0,0061 de F1** (gelé), **+0,0020 de tête** ;
- **par langue** (gelé) : français 0,7555 → 0,7575 (**+0,0020**), anglais 0,7362 → 0,7651
  (**+0,0289**) ; le gain est massivement anglais ;
- **dev/test** : les 8 labels et l'erreur sont **tous dans dev** (126/126 → 133/134) ; **test ne
  change pas** (62/62 avant et après). Le split ne valide donc pas le gain POS — il ne le
  contredit pas non plus, mais il ne le teste pas.

La fiche attribue « neuf labels » au POS contextuel : c'est le gain **total** 187 → 196. Le
POS n'en explique que **8** ; le neuvième vient des autres corrections v7 (188 labels sans POS
contextuel, contre 187 en v6). De même, le « +0,0132 » est calculé sur le 0,7475 de la v4, pas
sur la v6 (0,7482 gelé / 0,7461 vivant).

### 8.3 L'exemple `SUB « that she would come »` n'est pas produit

Sur la phrase gold `g017` (« She said that she would come yesterday. ») :

- gold : `SUB « that she would come »` (span 9–28), cible `said` ;
- prédit : `SUB « that she »` (span 9–17), puis `GV « would come yesterday »` (span 18–38) ;
- le span gold est **l'un des 43 perdus** (c'est même l'un des 17 SUB).

La cause est la règle du **sujet-verbe** ajoutée en v7 : `that` est dans `SUJETS`, donc le mot
suivant `she` est classé « verbe » (`est_verbe`), ce qui coupe la SUB après `she` et ouvre un GV
sur `would come yesterday`. La règle `who speaks` fonctionne, mais `that + pronom` est un faux
positif. L'exemple de la fiche est donc à retirer ou à corriger ; le span reste dans la file des
43.

### 8.4 « qui » 12 : c'est 6

La fiche dit « 21 REL (« qui » 12) ». Le compte exact des 21 REL manquantes est :

| premier mot | nombre | langue |
|---|---:|---|
| `that` | 10 | en |
| `qui` | **6** | fr |
| `she` | 1 | en |
| `where` | 1 | en |
| `dont` | 1 | fr |
| `whose` | 1 | en |
| `que` | 1 | fr |

Il y a **6** REL commençant par « qui », toutes françaises, pas 12. Le nombre 12 correspond aux
**12 spans français REL+SUB manquants** (8 REL + 4 SUB), pas aux « qui ». La répartition par
langue des 43 spans est : **en 27** (13 REL, 13 SUB, 1 GP), **fr 16** (8 REL, 4 SUB, 4 GP).
La suite « REL "qui" (12), SUB anglais, GP » est donc doublement imprécise : les SUB manquantes
ne sont pas toutes anglaises (4 françaises), et les GP manquants sont majoritairement français
(4 sur 5).

### 8.5 Le total cache une régression SUB

| | v6 | v7 | delta |
|---|---:|---:|---:|
| REL | 24 | 21 | −3 |
| SUB | 12 | **17** | **+5** |
| GP | 16 | 5 | −11 |
| total | 52 | 43 | −9 |

Le total baisse de 9, mais les SUB manquantes **augmentent de 5**. La fiche ne le dit pas ; c'est
cohérent avec les prépositions ambiguës et l'ordre GV/GP, sans que cet audit isole la cause. Le
résultat reste positif (le total baisse), mais la phrase « les spans perdus tombent de 52 à 43 »
ne doit pas faire croire que les trois catégories baissent.

## 9. dev/test

Le split est `crc32(str(id)) % 3 == 0 → test` sur les 612 phrases. Il est **non stratifié** mais
équilibré a posteriori : dev 422 phrases / 163 cibles / 134 labels ; test 190 / 76 / 62 ; union
612, intersection 0. Aucune phrase dupliquée.

| | phrases | cibles | labels | couverture | exact/labels | F1 | tête | POS | top-k |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **dev** | 422 | 163 | 134 | 134/163 = **0,8221** | 133/134 = **0,9925** | 0,5512 | 0,7132 | 0,7547 | 111/163 = 0,6810 |
| **test** | 190 | 76 | 62 | 62/76 = **0,8158** | 62/62 = **1,0** | 0,5651 | 0,7196 | 0,7656 | 55/76 = 0,7237 |
| tout | 612 | 239 | 196 | 196/239 = **0,8201** | 195/196 = **0,9949** | 0,5555 | 0,7152 | 0,7581 | 166/239 = 0,6946 |

Par langue :

| | dev cibles | dev labels | dev exact | test cibles | test labels | test exact |
|---|---:|---:|---:|---:|---:|---:|
| fr | 101 | 92 | 92 (1,0) | 50 | 43 | 43 (1,0) |
| en | 62 | 42 | 41/42 (0,9762) | 26 | 19 | 19 (1,0) |

**Le seul échec est r102** (`GP/en` « since this morning », gold `falls`, prédit vide). Il est
dans **dev**. Le test est parfait (62/62) mais ne couvre que 62 des 76 cibles (0,8158) et seulement
**19 labels anglais** ; `REL/en` y est la cellule la plus mince (5 cibles, 2 labels). Le split
n'est donc pas un held-out au sens fort : les règles v7 ont été dessinées en regardant tout le
gold, test compris.

**Comparaison v6** :

| | v6 | v7 |
|---|---:|---:|
| dev exact/labels | 126/126 (1,0) | **133/134 (0,9925)** |
| test exact/labels | 61/61 (1,0) | **62/62 (1,0)** |
| dev F1 | 0,5091 | **0,5512** |
| test F1 | 0,5217 | **0,5651** |
| dev couverture | 0,7730 | **0,8221** |
| test couverture | 0,8026 | **0,8158** |

Le test gagne **un label** et reste parfait ; le dev gagne **8 labels** et **une erreur**. Le
solde est **+9 labels, +8 exacts**, mais il cache des flux : les 8 labels du POS contextuel sont
tous dans dev, et l'erreur r102 aussi. Le test ne montre donc **aucun** des 8 labels du POS
contextuel ; l'ablation du précédent en retire 7 au test, ce qui valide cette règle-là mais pas le
gain POS. C'est un point de lecture important : « test 62/62 » ne veut pas dire « le gain POS
généralise », il veut dire « le test ne contient pas les cas qui dépendent du POS contextuel ».

Sur le gelé 602, les mêmes dev/test valent 133/134 et 62/62 (les 10 phrases ajoutées n'ont pas de
cible) ; seules la F1 et la POS changent : dev F1 0,5556, test F1 0,5679 ; dev POS 0,7572, test
POS 0,7670.

## 10. Les fiches amont v4 et v5

| fiche | titre | corps | mesure au commit | verdict |
|---|---|---|---|---|
| **v4** `392f03aa` | « exact 158/160 (0,9875) » | « 157/160 (0,9812) » | 157/160, F1 0,4539, tête 0,6432, S 0,4285, chunker 0,4143, POS 0,7475, top-k 156, spans 79 | **titre faux d'un label** ; corps et JSON corrects |
| **v5** `b975011b` | « exact 185/187 (0,9893) » | « 186/187 (0,9947) » | 186/187, F1 **0,5164**, tête **0,6834**, S 0,4582, chunker 0,5351, POS 0,7482, top-k 161, spans 52 | **titre faux d'un label** ; F1/tête de `7a9f0d6a` (0,5156/0,6826), exact/S/chunker de `b975011b` : **mélange de deux commits** |
| **v6** `0ec6c27d` | « 187/187 (1,0) » | — | 187/187, F1 0,5130 vivant / 0,5164 gelé, tête 0,6785/0,6834, POS 0,7461/0,7482, dev 126/126, test 61/61 | **correct** ; c'est la v7 qui ne le reprend pas dans sa colonne « avant » |

Deux conséquences :

- les titres de v4 et v5 sont **périmés d'un label** ; pour v4, le corps et le JSON sont corrects ;
  pour v5, le corps et le JSON **mélangent deux commits** (F1/tête de `7a9f0d6a`, exact/S/chunker
  de `b975011b`), c'est le même type de dette que les docstrings de portes ;
- la fiche v5 est **hybride** : `7a9f0d6a` pour la F1/tête, `b975011b` pour l'exact/S/chunker.
  La v7 a hérité de cette habitude en mélangeant v4/v5/v6 dans sa colonne « avant ».

## 11. Ce qui pourrait rendre cet audit faux

- **Le split dev/test est petit et non stratifié** : 62 labels au test, 1 cas = 1,6 point ;
  `REL/en` = 5 cibles, `hand` = 3 cibles au test. Les 62/62 ne sont pas une garantie de
  généralisation.
- **Le split n'est pas un held-out** : les règles v7 ont été réglées en regardant tout le gold,
  test compris. Il mesure la stabilité au découpage, pas le surajustement global.
- **Les cinq valeurs gelées sont sensibles aux 10 phrases ajoutées** (38 tokens, 32 segments) ;
  l'attachement est invariant parce qu'elles n'ont pas de cible, mais POS/F1/tête/S/chunker ne le
  sont pas. Une future phrase avec cible changerait aussi l'exact.
- **Les contrôles négatifs mesurent une association sur le même gold**, pas une causalité. Le
  candidat aléatoire dans la liste du label (35,84 %) utilise les listes du modèle lui-même ; ce
  n'est pas une baseline indépendante.
- **La règle du sujet-verbe est trop large** (`that` dans `SUJETS`) : l'exemple g017 est coupé en
  `that she`; d'autres phrases `that + pronom` peuvent être touchées. Le vrai taux de SUB
  manquantes (17) le montre déjà.
- **Les docstrings et messages périmés** peuvent faire croire à des valeurs qui ne sont plus
  mesurées ; ils ne cassent rien mais trompent le lecteur pressé.
- **Le gold 612 est vivant** : toute nouvelle phrase avec cible changera l'exact/labels, pas
  seulement la POS/F1. La fiche doit dire sur quel gold elle parle, ou les deux.

## 12. Ce qu'il faut corriger (recommandations)

1. **Nommer le gold** dans la fiche et le JSON : soit « gelé 602 » pour les cinq valeurs de
   qualité, soit re-mesurer les cinq sur le vivant 612 et remplacer 0,7603/0,5595/0,4741/0,5858/
   0,7205 par 0,7581/0,5555/0,4688/0,5822/0,7152. Le plus simple est d'ajouter un champ
   `"gold": "gele-602"` au JSON et une note en tête du tableau.
2. **Remplacer la colonne « avant »** par la v6 mesurée : POS 0,7461 (vivant) / 0,7482 (gelé),
   F1 0,5130 / 0,5164, tête 0,6785 / 0,6834, ou par les deux colonnes.
3. **Corriger le récit POS** : +8 labels (pas 9), +0,0118 (gelé) / +0,0116 (vivant) de POS,
   +7 top-k, +0,0061 F1 ; les 8 labels et l'erreur sont dans dev, test inchangé.
4. **Corriger l'exemple SUB** : soit retirer `that she would come`, soit restreindre `SUJETS` pour
   qu'un pronom après `that` ne soit pas classé verbe. En l'état, le span est perdu.
5. **Corriger « qui 12 » en « qui 6 »**, ou écrire « 12 REL+SUB françaises ».
6. **Rafraîchir les 26 docstrings et les 6 messages `/145`** ; au minimum T107, T110, T112, T113,
   T141, T153, T156, T157, T162, T163, T166, T167, T172, T173, T177, T179 et les messages de
   T161/T162/T168/T171/T177/T179.
7. **Ajouter une porte dev/test** (133/134, 62/62, F1 0,5512/0,5651, couverture 0,8221/0,8158)
   pour que le split ne soit pas seulement une affirmation de fiche.
8. **Ajouter une porte qui associe POS vivant 0,7581 et F1 vivant 0,5555**, ou qui asserte
   explicitement le gelé, pour que le « 183/183 » ne puisse pas certifier deux golds à la fois
   sans le dire.
9. **Noter la régression SUB 12 → 17** et la redondance des candidats du précédent (0 effet en
   v7) : ce sont deux informations utiles pour la suite.

## 13. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — l'heuristique auditée (non modifiée).
- [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) — `charger`, `charger_gele`,
  `evaluer_bloc` (non modifié).
- [`gold_split.py`](../tools/tests/linguistique/gold_split.py) — dev/test (non modifié).
- [`autotest.py`](../tools/pensee/autotest.py) — 183 portes (non modifié).
- [`rapport-pensee-couverture-v7.md`](rapport-pensee-couverture-v7.md) — la fiche auditée.
- [`pensee-couverture-v7.json`](pensee-couverture-v7.json) — le JSON audité.
- [`rapport-pensee-couverture-v5.md`](rapport-pensee-couverture-v5.md) — fiche amont v5.
- [`rapport-pensee-segmentation-v4.md`](rapport-pensee-segmentation-v4.md) — fiche amont v4.
- [`pensee-audit-v7.json`](pensee-audit-v7.json) — les chiffres de cet audit.

**Aucun fichier existant n'a été modifié ; aucun commit n'a été fait.**
