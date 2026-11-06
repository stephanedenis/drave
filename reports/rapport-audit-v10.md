# Audit v10 — les chiffres rejouent, l'attribution des corrections ne rejoue pas

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Branche** : `s/v7` ·
> **Commit audité** : `710ec7f9` (parent `160d08ca`) · **Date** : 2026-11-05 ·
> **Verdict** : chiffres ✅ (deux écarts), règles ❌, portes ✅.
> **Aucun fichier existant modifié ; aucun commit.** Sorties : ce rapport et
> [`pensee-audit-v10.json`](pensee-audit-v10.json).

**En une phrase.** Les valeurs de la fiche [`rapport-pensee-v10.md`](rapport-pensee-v10.md)
rejouent presque toutes : **220/220**, couverture **0,9205**, **F1 0,5880** (gelé 602),
**tête 0,7388**, **fr 134/134**, **en 86/86**, **19 spans** (9 REL, 6 SUB, 4 GP),
**top-k 219**, **183/183 portes**. Mais la fiche attribue le gain à **deux** corrections :
la seconde, le **`-ée`**, est **antérieure à la v10** (commit `a408a909`, déjà dans v8 et v9)
et **inerte sur ce gold** (0 différence d'annotation sur 612 phrases) ; `r255` reste absent
car `acheter` n'est pas dans le lexique. Le **seul** gain v10 est la **garde DET du GP**
(`r153`, test), **+1 exact**. Les **19 spans** ne sont pas « 17 inatteignables + `r255` +
`r264` » : `r255`/`r264` sont déjà dans les 17 ; les deux extras réels sont **`s037`**
(7e régression v8, toujours ouverte) et **`r303`** (régression v9 par `predicat_vu`, non
listée). Enfin, le F1 « avant » **0,5822** est la valeur du **vivant 612** ; le **gelé 602**
vaut **0,5866**, donc le gain F1 v9→v10 est **+0,0014**, pas +0,0058 ; et le **test** v10
n'est pas actualisé : **68/68**, pas 67/67 (le 67/67 est explicitement la v9).

## 1. Dispositif et fidélité du harnais

- **Gold vivant** : `evaluer_gold.charger()` — **612** phrases (20 `hand`, 432 `reel`,
  160 `synthetique`), **239** cibles, 3 179 tokens.
- **Gold gelé** : `evaluer_gold.charger_gele()` — **602** phrases, mêmes **239** cibles ;
  les 10 phrases ajoutées après le gel n'ont aucune cible.
- **Split** : `gold_split` (`crc32(id) % 3 == 0` → test) — **422 dev + 190 test = 612**,
  **163 + 76 = 239** cibles.
- **Mesure** : `evaluer_gold.evaluer_bloc` pour les valeurs officielles ; harnais local
  pour les ensembles d'identifiants, les ablations et les contrôles.
- **Ablations** : le module [`bloc_linguistique.py`](../tools/bloc_linguistique.py) est copié
  dans `/tmp/audit_v10/mods`, une seule règle est retirée par variante, puis le module copié
  est importé et mesuré. Aucun patch du dépôt.
- **Fidélité** : `v10` moins la garde DET du GP et moins le `-ée` redonne **exactement** le
  module `v9` (`160d08ca`) : **219/219, F1 gelé 0,5866, 20 spans, dev 152/152, test 67/67**.
  Le module `v8` (`f908d7b0`) redonne **212/212, F1 0,5763, 27 spans, top-k 177, dev
  148/148, test 64/64** — conforme à l'[audit A19](rapport-audit-r1r3.md). C'est le contrôle
  de fidélité du harnais.
- **Portes** : `PYTHONPATH=. python3 -m tools.pensee.autotest` → **183/183**, exit 0.
  L'invocation directe `python3 tools/pensee/autotest.py` échoue sur l'import relatif
  (`ImportError`) ; il faut `-m`.

### 1 bis. Note d'arbre de travail (importante)

Au début de l'audit, `tools/bloc_linguistique.py` était **byte-identique** à `710ec7f9`
(sha256 `308f6eed…`). Pendant la rédaction, le fichier a été **modifié sans commit** (mtime
`2026-11-06 00:15:37`) : deux changements dans `_syntagmes_simple` — la condition R2
(`stype = "SUB" if (est_sub(n) or n in SUBORDONNANTS or precedent == "GV")`, qui répare
`s037`) et la **suppression de la garde d'adverbe final** (qui répare `r303` mais perd
`g017`). **Toutes les mesures de ce rapport sont ancrées sur le commit** : le module est lu
par `git show 710ec7f9:tools/bloc_linguistique.py`, copié dans `/tmp/audit_v10/mods` et
importé ; le fichier de travail n'est jamais utilisé. Les chiffres du commit sont **220/220,
0,5880, 19 spans, test 68/68** ; l'arbre courant, lui, donne **221/221, F1 0,5843, top-k 220,
18 spans (9 REL, 5 SUB, 4 GP), dev 152/152, test 69/69** (il répare `s037` et `r303`, perd
`g017`, ajoute `r241`). Ce changement n'est **pas** de cet audit et n'est **pas** évalué ici ;
son auteur doit le vérifier et le committer. Les **183/183 portes** ont été obtenues quand
l'arbre était encore au commit.

## 2. Rejeu des valeurs v10 — 2 écarts

### 2.1 Valeurs « après »

| grandeur | fiche / JSON | vivant 612 | gelé 602 | écart |
|---|---:|---:|---:|---:|
| labels au bon span | 220 | **220** | **220** | 0 |
| exact / labels | 220/220 = 1,0000 | **220/220** | **220/220** | 0 |
| `exact_span` | 1,0000 | **1,0000** | **1,0000** | 0 |
| couverture (labels / cibles) | 0,9205 | **0,9205** | **0,9205** | 0 |
| F1 union | 0,5880 | 0,5836 | **0,5880** | 0 sur le gelé |
| S (F1) | 0,5014 | 0,4957 | **0,5014** | 0 sur le gelé |
| chunker (F1) | 0,6203 | 0,6163 | **0,6203** | 0 sur le gelé |
| tête (F1) | 0,7388 | 0,7332 | **0,7388** | 0 sur le gelé |
| français | 134/134 | **134/134** | **134/134** | 0 |
| anglais | 86/86 | **86/86** | **86/86** | 0 |
| top-k | 219 ; 0,9163 | **219 ; 0,9163** | **219 ; 0,9163** | 0 |
| top-k strict (hors fiche) | — | **219 ; 0,9955** | **219 ; 0,9955** | — |
| spans restants | 19 (9 REL, 6 SUB, 4 GP) | **19 (9/6/4)** | **19 (9/6/4)** | 0 |

Les compteurs d'attachement sont identiques sur les deux golds ; `F1`, `S`, `chunker` et
`tête` sont les valeurs du **gelé 602** dans la fiche (les valeurs vivantes sont entre
parenthèses ci-dessus). `evaluer_bloc` redonne au chiffre près : `verbe` **149/149**,
`nom` **71/71**, `exact_any` **220/220**, `topk_exact` **219**.

### 2.2 Les deux écarts

1. **F1 « avant » (v9)** : la fiche et le JSON donnent **0,5822** en le présentant comme
   « gelé 602 » (ligne F1). Or **0,5822 est la valeur du vivant 612** ; sur le gelé 602, la
   v9 vaut **0,5866**. Le tableau « avant / après » compare donc **0,5822 (vivant)** à
   **0,5880 (gelé)** : le gain affiché est **+0,0058**, le gain réel à base constante est
   **+0,0014** (0,5866 → 0,5880). C'est un écart de **base**, pas de code.
2. **dev / test (valeur non actualisée)** : la fiche publie « dev 152/152, test 67/67
   (avant ces deux corrections) ». C'est exact pour la **v9** ; après la garde DET du GP,
   le **test v10 est 68/68** (couverture 0,8947), le **dev reste 152/152** (0,9325). Le
   `-ée` n'ajoute rien. Le JSON v10 ne publie pas ces deux moitiés : la valeur courante
   manque.

## 3. Rejeu des valeurs v9 — F1 mal basé, spans mal décomposés

| grandeur | fiche / JSON | mesuré vivant 612 | mesuré gelé 602 | écart |
|---|---:|---:|---:|---:|
| labels | 219 | **219** | **219** | 0 |
| exact / labels | 219/219 = 1,0000 | **219/219** | **219/219** | 0 |
| couverture | 0,9163 | **0,9163** | **0,9163** | 0 |
| F1 union | 0,5822 (« gelé 602 ») | **0,5822** | **0,5866** | **−0,0044 : mauvaise base** |
| S / chunker | 0,5006 / 0,6178 | 0,4950 / 0,6138 | **0,5006 / 0,6178** | 0 sur le gelé |
| tête | 0,7381 | 0,7326 | **0,7381** | 0 sur le gelé |
| français | 134/134 | **134/134** | **134/134** | 0 |
| anglais | 85/85 | **85/85** | **85/85** | 0 |
| top-k | 218 ; 0,9121 | **218 ; 0,9121** | **218 ; 0,9121** | 0 |
| spans | 20 (9 REL, 6 SUB, 5 GP) | **20 (9/6/5)** | **20 (9/6/5)** | 0 (comptes) |

**dev/test v9** : **152/152** et **67/67**, mesurés sur les deux moitiés (section 6) ;
conformes à la fiche.

**Ce qui ne rejoue pas dans la fiche v9.**

- **Le F1 0,5822 est mal basé** : c'est le vivant 612, pas le gelé 602. Le JSON v9 mélange
  d'ailleurs les bases : `f1` = vivant, `f1_s`/`f1_chunker`/`tête` = gelé. Sur le gelé, la
  v9 vaut **0,5866**, donc la v9 **sous-estime** son propre gain (0,5763 → 0,5866 = **+0,0103**,
  et non +0,0059).
- **« Les 7 régressions de la v8 sont réparées » est faux** : **6** le sont (`r273`, `s032`,
  `s069`, `s072`, `s115`, `s135`) ; **`s037` reste absente**. C'est la 7e régression de
  l'audit A19, et elle est encore dans les 19 spans de la v10.
- **La décomposition des 20 spans est fausse** : « 17 étaient déjà inatteignables + 3 gains
  de A17 (`r153`, `r255`, `r264`) ». `r255` et `r264` **appartiennent aux 17** ; les trois
  non-résiduels réels sont **`s037`**, **`r303`** et **`r153`**. La fiche double donc deux
  identifiants et omet `s037` et `r303`.
- **L'arithmétique ne somme pas** : la fiche annonce « 7 régressions + 3 spans », soit
  **+10** sur 212 = **222** ; le mesuré est **8 gains bruts** (6 REL + `r280` + `g017`) et
  **1 perte** (`r303`), soit **+7 = 219**. La différence est `r303`, perdue.
- **`predicat_vu` n'est pas un gain net** : il rouvre `g017` mais **ferme `r303`**
  (`car il est tard`, SUB `[8:23]` → `[8:18]`). Net **0** exact, **0** F1 ; la fiche ne
  mentionne pas la perte, et le dev 152/152 cache l'échange.

## 4. Ablations — l'effet réel de chaque correction

**Lecture.** On part du code v10 (220 exacts). « Gain » = cible exacte du code livré qui
**cesse** de l'être quand on retire la règle ; « perte » = cible exacte **rétablie** quand on
la retire. `F1` = union sur le **gelé 602**. Les identifiants sont `phrase:type`.

| ablation | labels | exact | Δ exact | gains | pertes | F1 gelé (Δ) | top-k | spans | dev | test |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **garde PRON** (retirée, SUJETS relatifs conservés) | 203 | 203 | **−17** | **17** | 0 | 0,5718 (−0,0162) | 202 | 36 (18 REL, 14 SUB) | 138/138 | 65/65 |
| **expansion SUJETS** (retirée, garde conservée) | 214 | 214 | **−6** | 6 | 0 | 0,5833 (−0,0047) | 213 | 25 (15 REL, 6 SUB) | 149/149 | 65/65 |
| **PRON + SUJETS** (les deux retirées) | 214 | 214 | **−6** | 6 | 0 | 0,5808 (−0,0072) | 213 | 25 (15 REL, 6 SUB) | 149/149 | 65/65 |
| **`est_sub`** (retiré) | 219 | 219 | **−1** | 1 | 0 | 0,5849 (−0,0031) | 218 | 20 (10 REL, 6 SUB, 4 GP) | 151/151 | 68/68 |
| **`predicat_vu`** (retiré) | 220 | 220 | **0** | 1 | **1** | 0,5880 (0) | 219 | 19 (9/6/4) | 152/152 | 68/68 |
| **`-ée`** (retiré) | 220 | 220 | **0** | 0 | 0 | 0,5880 (0) | 219 | 19 (9/6/4) | 152/152 | 68/68 |
| **garde DET du GP** (retirée) | 219 | 219 | **−1** | 1 | 0 | 0,5866 (−0,0014) | 218 | 20 (9 REL, 6 SUB, 5 GP) | 152/152 | 67/67 |
| *module v9* (`160d08ca`) | 219 | 219 | −1 | 1 | 0 | 0,5866 (−0,0014) | 218 | 20 (9/6/5) | 152/152 | 67/67 |
| *module v8* (`f908d7b0`) | 212 | 212 | −8 | 9 | **1** | 0,5763 (−0,0117) | 177 | 27 (16/6/5) | 148/148 | 64/64 |

### 4.1 Identifiants

- **Garde PRON** — gains : `g017 r034 r074 r114 r205 r219 r240 r243 r247 r278 r280 r285
  r296 r299` (dev), `r214 r216 r281` (test) ; aucune perte.
- **Expansion SUJETS** — gains : `r273 s069 s135` (dev), `s032 s072 s115` (test) ; aucune
  perte. **PRON + SUJETS** : mêmes six gains, mêmes pertes nulles.
- **`est_sub`** — gain : `r280` (dev) ; aucune perte.
- **`predicat_vu`** — gain : `g017` (dev) ; **perte : `r303`** (dev).
- **`-ée`** — aucun gain, aucune perte.
- **Garde DET du GP** — gain : `r153` (test) ; aucune perte.
- **v8 → v10** — 9 gains (`g017 r273 r280 s069 s135` dev ; `r153 s032 s072 s115` test),
  1 perte (`r303` dev) : net **+8** (212 → 220).

### 4.2 Ce que les ablations disent

- **Le `-ée` est totalement inerte sur ce gold.** Retirer la boucle ne change **aucune**
  étiquette (niveau, type, span) sur les **612** phrases : labels, exact, F1, top-k et spans
  sont identiques. `_est_verbe("achetée")` reste **False** car `acheter` n'est **pas** dans
  `VERBES_CONNUS` (0 occurrence) ; `r255` reste donc absent, contrairement à la table de la
  fiche qui lui attribue l'effet `r255`. Le `-ée` est présent dès `a408a909`
  (« lexique élargi », 10:39), donc dans **v8** (`f908d7b0`, 21:08) et **v9** (`160d08ca`,
  22:56). Le commit `710ec7f9` ne modifie, dans le bloc, que la **boucle GP** (3 lignes).
- **La garde PRON est conditionnelle à l'expansion SUJETS.** Sans l'expansion, elle est
  inerte (`sans_pron_sujets` = `sans_sujets` = 214) ; avec l'expansion, la retirer coûte
  **17** exacts. Les **6 REL françaises** réparées en v9 (`r273 s032 s069 s072 s115 s135`)
  viennent de l'**expansion SUJETS**, pas de la garde : `sans_sujets` les perd, `sans_pron`
  ne les perd pas. La garde sert à empêcher les **pronoms** de devenir verbes par position
  (`that I read`), ce qui évite **17** pertes collatérales. Le faisceau v9 (SUJETS + garde)
  vaut **+6 net** par rapport à l'absence des deux.
- **`est_sub` vaut +1** (`r280`, dev), 0 perte : conforme à la v9.
- **`predicat_vu` est un échange, pas un gain** : `g017` gagné, `r303` perdu, net **0**.
  La fiche v9 ne mentionne pas `r303` ; le dev reste à 152/152, ce qui masque l'échange.
- **La garde DET du GP est la seule correction v10** : **+1** (`r153`, test), 0 perte.
  Elle change aussi **`g004`** et **`r147`** : le chunker y produisait un GP court + un GV
  (« pour attraper le | bus », « devant la | porte ») en doublon du GP de S ; la garde les
  supprime. Ces deux phrases ne portent pas de cible, mais leurs faux positifs expliquent
  une part du **+0,0014** de F1 (le reste est `r153`).
- **Le risque « `idée` → `ider` » de la fiche est faux** : `_est_verbe("idée")` = **False**
  (`ider` n'est pas au lexique). Les vrais faux positifs de la règle sont `entrée` →
  `entrer`, `portée` → `porter`, `aimée` → `aimer`, qui sont au lexique ; ils ne sont pas
  observés sur ce gold.
- **Le risque « de la voir » de la garde GP est réel** : sur `Il parle de la voir.`, le GP
  prédit est `[9:19]` « de la voir », verbe compris. Aucune perte sur ce gold, mais la règle
  est trop large pour ce cas.

## 5. Contrôles négatifs

Contrôles exécutés sur le code v10, **220 labels**, graine 0, **2 000 tirages**.

| contrôle | observé | référence nulle | p |
|---|---:|---:|---:|
| **permutation globale des cibles** (top-1) | **220/220 = 1,0** | moyenne **1,997/220 = 0,908 %** ; médiane 2 ; max 10 ; p95 5 | **0/2 000** |
| **candidat aléatoire** (top-1) | **220/220 = 1,0** | moyenne **92,7/220 = 42,14 %** (585 candidats, 2,66/label) | **0/2 000** |
| **permutation des listes de candidats** (top-k, égalité) | **219/220 = 0,9955** | moyenne **2,18/220 = 0,99 %** ; max 8 | **0/2 000** |
| **permutation des listes de candidats** (top-k, sous-chaîne) | **219/220 = 0,9955** | moyenne **2,58/220 = 1,17 %** ; max 9 | **0/2 000** |

**Lecture.** L'attachement n'est pas un artefact du hasard : la permutation des cibles divise
l'exact par 110, le candidat aléatoire par 2,4, le top-k par 85. Le contrôle « candidat
aléatoire » est haut (42,14 %) parce que les listes de candidats contiennent presque toujours
la cible (top-k 99,55 %) et comptent 2,66 candidats en moyenne ; il reste très loin de 100 %.
Le top-k officiel (sous-chaîne) est peu discriminant : une liste de candidats permutée garde
1,17 % de réussite ; le top-1 aléatoire, lui, vaut 42,14 %. Les deux contrôles donnent p = 0.

La fiche v10 ne publie pas de contrôle courant : elle renvoie au dispositif A19
(**2,04/212**, p = 0). Notre mesure (**1,997/220**, p = 0) est du même ordre et la confirme.

### 5.1 Les 19 spans vérifiés

Les 19 spans sont bien **9 REL, 6 SUB, 4 GP** ; **17 français, 2 anglais** ;
**14 synthétiques, 5 réels**. Ce sont **exactement** les 17 résiduels d'A19 **plus** `s037`
et `r303`. La fiche v10 annonce « 17 inatteignables + `r255` + `r264` » : `r255` et `r264`
sont déjà dans les 17 ; les deux extras réels sont `s037` et `r303`.

| id | lg | source | type | span | texte | cible | classe |
|---|---|---|---:|---:|---|---|---|
| `s027` | fr | synthétique | GP | 31:33 | il | `marche` | A17 résiduel |
| `s146` | fr | synthétique | GP | 25:35 | les jardin | `observe` | A17 résiduel |
| `s148` | fr | synthétique | GP | 20:39 | les ancienne lettre | `nage` | A17 résiduel |
| `s160` | fr | synthétique | GP | 20:29 | le renard | `nage` | A17 résiduel |
| `r035` | en | réel | REL | 9:24 | she talks about | `film` | A17 résiduel (relative zéro) |
| `r255` | fr | réel | REL | 11:27 | que j'ai achetée | `voiture` | A17 résiduel (lexique `acheter`) |
| `s010` | fr | synthétique | REL | 10:18 | qui nage | `chemin` | A17 résiduel |
| `s035` | fr | synthétique | REL | 10:19 | qui ferme | `papier` | A17 résiduel |
| `s037` | fr | synthétique | REL | 5:15 | qui marche | `Paul` | **régression v8 (R2), non réparée** |
| `s061` | fr | synthétique | REL | 9:18 | qui saute | `nuage` | A17 résiduel |
| `s065` | fr | synthétique | REL | 5:17 | qui commence | `elle` | A17 résiduel |
| `s125` | fr | synthétique | REL | 11:21 | qui compte | `renard` | A17 résiduel |
| `s141` | fr | synthétique | REL | 5:15 | qui trouve | `Emma` | A17 résiduel |
| `r264` | fr | réel | SUB | 8:26 | qu'il vient demain | `sais` | A17 résiduel (tokenisation) |
| `r288` | en | réel | SUB | 7:29 | that he comes tomorrow | `know` | A17 résiduel (adverbe final) |
| `r303` | fr | réel | SUB | 8:23 | car il est tard | `pars` | **régression v9 (`predicat_vu`), non listée** |
| `s044` | fr | synthétique | SUB | 17:29 | que ils crie | `nage` | A17 résiduel |
| `s112` | fr | synthétique | SUB | 24:39 | que Lucas ferme | `nage` | A17 résiduel |
| `s114` | fr | synthétique | SUB | 22:43 | que les avocat compte | `dessine` | A17 résiduel |

Parmi les 17 résiduels, l'audit A19 distinguait **13 non récupérables** (lexique synthétique,
gold sans préposition) et **4 hors périmètre mais récupérables** (`r035`, `r255`, `r264`,
`r288`). La fiche v10 les appelle tous « inatteignables » : c'est trop fort pour ces quatre.

## 6. dev / test — re-mesure des deux moitiés

| moitié | phrases | cibles | v8 labels/exact | v9 labels/exact | **v10 labels/exact** | couv. v10 | F1 v10 | tête v10 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **dev** | 422 | 163 | 148/148 | 152/152 | **152/152** | **0,9325** | **0,5812** | **0,7330** |
| **test** | 190 | 76 | 64/64 | 67/67 | **68/68** | **0,8947** | **0,5890** | **0,7337** |

**Par langue (v10)** : dev fr **91/91** (101 cibles), en **61/61** (62) ; test fr **43/43**
(50), en **25/25** (26). Les 19 spans sont 17 français + 2 anglais.

**Le +1 test est `r153`**, la garde DET du GP ; le `-ée` n'ajoute rien. Le dev reste à
152/152, mais sa composition change : `predicat_vu` gagne `g017` et perd `r303`, tous deux
en dev. La fiche v10 publie encore le **test 67/67** en le datant d'avant les corrections ;
la valeur courante est **68/68**.

## 7. Portes

`PYTHONPATH=. python3 -m tools.pensee.autotest` → **183/183 portes tenues**, exit 0,
**0 échec**. Les assertions du périmètre attachement/segmentation portent bien les valeurs
mesurées : `T153` top-1/exact 0,9205, `T161` 220/239, `T162` top-k 219/239 et tête 219/220,
`T163` 19 spans et 1 cible, `T166` 9 REL / 6 SUB / 4 GP, `T167` labels 220 et top-k span
0,9955, `T173` 219 sous-chaîne et 219 exacts (0,9955), `T180` fr 134/134 et en 86/86. Les
portes **entérinent** les valeurs courantes ; elles ne testent pas l'attribution des règles
(le `-ée` inerte et `r303` passent sans être vus).

**Onze docstrings du périmètre attachement/segmentation sont périmées** : elles contredisent
leur propre assertion (qui, elle, passe). Le commit `710ec7f9` a mis à jour 19 assertions,
pas ces textes.

| porte | docstring | mesure affichée |
|---|---|---|
| T153 | top1/exact/couverture 0,887 | **0,9205 / 0,9205 / 0,9205** |
| T161 | 212/212 | **220/220** |
| T162 | 211/239 (0,8828) | **219/239 (0,9163)** |
| T163 | 27 de span | **19 de span** |
| T166 | 16 REL, 6 SUB, 5 GP (27) | **9 REL, 6 SUB, 4 GP (19)** |
| T167 | exactitude spans ÷ 212 | **÷ 220** |
| T172 | exact 212/212 | **220/220** |
| T173 | 211/212 (0,9953) ; 211/239 (0,8828) | **219/220 (0,9955) ; 219/239 (0,9163)** |
| T177 | 88 → 211 | **219** |
| T179 | exact_any 212/212 | **220/220** |
| T180 | « la couverture anglaise non » | **en 86/88 = 0,9773 ; fr 134/151 = 0,8874** (l'anglaise est la plus haute) |

Ces docstrings ne changent pas le verdict des portes, mais ils font dire au banc le contraire
de ce qu'il mesure.

## 8. Écarts, par gravité

1. **Majeure — le `-ée` n'est pas une correction v10.** Il est introduit par `a408a909`
   (avant v8), déjà présent dans v8/v9, et **inerte** sur ce gold : 0 différence d'annotation
   sur 612 phrases, 0 gain, 0 perte. `r255` reste absent car `acheter` n'est pas dans
   `VERBES_CONNUS`. La table « deux corrections » et l'effet `r255` sont faux ; le seul gain
   v10 est la garde DET du GP (`r153`, +1).
2. **Majeure — la décomposition des 19 spans est fausse.** « 17 inatteignables + `r255` +
   `r264` » double compte deux identifiants du résiduel et omet `s037` et `r303`. Les 19
   sont 17 résiduels + `s037` + `r303`.
3. **Majeure — `r303` est une régression non documentée.** `predicat_vu` (v9) rouvre `g017`
   mais ferme `r303` (`car il est tard`) ; net 0. La fiche v9 dit « tous les compteurs
   montent » et ne mentionne pas la perte.
4. **Majeure — « les 7 régressions de la v8 sont réparées » est faux.** 6 le sont ; `s037`
   reste absente. L'arithmétique 212 + 7 régressions + 3 spans ne somme pas ; le mesuré est
   **8 gains bruts, 1 perte, net +7** (212 → 219), puis +1 (`r153`) pour la v10.
5. **Majeure / moyenne — le F1 « avant » est mal basé.** La v9 vaut 0,5822 sur le **vivant**
   et 0,5866 sur le **gelé** ; la fiche v9 étiquette 0,5822 « gelé 602 » et la v10 le reprend.
   Le gain F1 v9→v10 est **+0,0014**, pas +0,0058. La v9 **sous-estime** son propre gain
   (0,5763 → 0,5866 = +0,0103, pas +0,0059).
6. **Moyenne — la valeur courante du test n'est pas publiée : 68/68, pas 67/67.** Le
   67/67 est explicitement la v9 ; le +1 est `r153` (garde DET du GP) ; le dev reste
   152/152. Le JSON v10 omet les deux moitiés.
7. **Moyenne — l'attribution des 6 REL à la garde PRON seule est imprécise.** Les 6 REL
   viennent de l'**expansion SUJETS** ; la garde PRON vaut **+17 conditionnel** (sans
   l'expansion, elle est inerte ; le faisceau vaut +6 net). La garde est indispensable, mais
   pas pour la raison écrite.
8. **Mineure — « 17 inatteignables »** : A19 distinguait 13 non récupérables et 4 hors
   périmètre récupérables (`r035`, `r255`, `r264`, `r288`). La v10 répète le raccourci.
9. **Mineure — l'exemple de risque `idée` → `ider` est faux.** `_est_verbe("idée")` =
   False ; les vrais faux positifs sont `entrée`, `portée`, `aimée` (stems au lexique),
   non observés sur ce gold. Le risque « de la voir » de la garde GP, lui, est réel.
10. **Mineure — le contrôle négatif de la fiche est emprunté à A19** (2,04/212) et non
    courant (220). Notre contrôle (1,997/220, p = 0) le confirme, mais la fiche ne publie
    pas de contrôle v10.
11. **Mineure — l'invocation directe `python3 tools/pensee/autotest.py` échoue** sur
    l'import relatif ; la commande correcte est `-m`.
12. **Moyenne — 11 docstrings de portes sont périmées** (T153, T161, T162, T163, T166,
    T167, T172, T173, T177, T179, T180) : elles annoncent 212/0,887/27 spans/211 top-k
    alors que le banc mesure 220/0,9205/19 spans/219. Les portes passent, mais leur texte
    contredit leur assertion ; les 19 assertions mises à jour par le commit n'ont pas
    entraîné ces docstrings.
13. **Mineure — les bases de F1/tête ne sont pas explicites dans le JSON** : la fiche dit
    « 602 » sur la ligne F1, pas sur la tête ; le JSON v9 mélange `f1` vivant et
    `f1_s`/`f1_chunker`/`tête` gelés.

## 9. Ce qui pourrait rendre cet audit faux

- **In-sample** : les règles sont dessinées sur ce gold ; le test n'est pas aveugle (A17 a
  diagnostiqué sur dev et test). L'audit mesure l'intégration, pas la généralisation.
- **Un seul split déterministe** (`crc32 % 3`), sans validation croisée ; les valeurs
  dev/test sont celles de ce split.
- **Ablations par copies** : la fidélité est vérifiée par `v10 − GP − -ée = v9` (219, 0,5866,
  20 spans, 152/152, 67/67) et par le module v8 (212, 0,5763, 27 spans, 177 top-k, 148/148,
  64/64). Les variantes intermédiaires ne retirent qu'une règle à la fois.
- **Le `-ée` est inerte sur ce gold** (0 différence d'annotation sur 612 phrases) ; un autre
  corpus pourrait révéler des faux positifs (`entrée`, `portée`, `aimée`) ou des effets hors
  gold. L'inertie mesurée ne prouve pas que la règle est bonne, seulement qu'elle ne change
  rien ici.
- **La garde DET du GP inclut un vrai verbe après déterminant** (« de la voir » → GP
  « de la voir ») : risque réel, non mesuré sur ce gold.
- **Le top-k officiel (sous-chaîne) est peu discriminant** : la permutation des listes de
  candidats laisse 1,17 % de réussite, le top-1 aléatoire 42,14 % ; les deux donnent p = 0.
- **Dépôt déjà modifié** : `journal/`, plusieurs `reports/` et le sous-module
  `tools/structures` portaient des modifications non commitées antérieures à cet audit. Le
  fichier `tools/bloc_linguistique.py` a été **modifié en cours d'audit** (mtime
  `2026-11-06 00:15:37`, deux changements R2/adverbe) : les mesures sont faites sur la copie
  du **commit** `710ec7f9`, pas sur l'arbre courant. La reproductibilité sur l'arbre courant
  n'est donc pas garantie tant que ce changement n'est pas committé ou reverté.

## 10. Fichiers

- [`rapport-audit-v10.md`](rapport-audit-v10.md) — ce rapport.
- [`pensee-audit-v10.json`](pensee-audit-v10.json) — les chiffres, les ids et les contrôles.

**Aucun fichier existant n'a été modifié ; aucun commit n'a été fait.** Les scripts de mesure
vivaient dans `/tmp/audit_v10/` et ne sont pas livrés.
