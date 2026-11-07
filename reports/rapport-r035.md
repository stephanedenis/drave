# B13 — la relative zéro (r035) : exact 236 → 237, POS inchangée

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Tâche** : J1.1 · **Date** : 2026-11-07 ·
> **Verdict** : ✅
> **`r035` est réglé** : « The film **she talks about** is out. » n'a aucun marqueur de relative.
> La règle **structurelle** `[GN antécédent] [pronom sujet] [verbe] [préposition orpheline] → REL`
> retrouve le span **[9:24]**, cible **`film`**. L'attachement exact passe de **236 à 237**,
> les labels de **237 à 238**, la couverture de **0,9916 à 0,9958** ; **POS inchangée**
> (0,8625), **F1 0,7533 → 0,7549**. **183/183 portes**.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_syntagmes_simple`,
> `relative_zero`), [`test_bloc_linguistique.py`](../tools/tests/linguistique/test_bloc_linguistique.py)
> (test unitaire), [`autotest.py`](../tools/pensee/autotest.py) (183 portes, valeurs recalées) ;
> JSON [`pensee-r035.json`](pensee-r035.json).

## 1. Le cas, reproduit

Gold de `r035` (`tools/tests/linguistique/gold_reel.json`) :

| segment | span | texte | cible |
|---|---|---|---|
| GN | [0:8] | « The film » | — |
| **REL** | **[9:24]** | **« she talks about »** | **`film`** |
| GV | [25:31] | « is out » | — |

Avant la règle, le chunker rend :

| segment | span | texte | cible |
|---|---|---|---|
| GN | [0:12] | « The film she » | `talks` |
| GV | [13:18] | « talks » | — |
| GV | [19:31] | « about is out » | — |

Deux mécanismes se cumulent. (1) La boucle du GN à déterminant avale le pronom sujet `she`,
parce qu'un pronom n'est ni une préposition, ni un auxiliaire, ni un verbe. (2) `about` est une
préposition, mais le mot suivant `is` est un auxiliaire : la branche GV se déclenche et fabrique
« about is out ». Aucune REL n'est produite, donc la cible `film` n'a pas de label.

## 2. La règle

> **Relative zéro à préposition orpheline.** Un GN antécédent suivi d'un **pronom sujet**, puis
> d'un **verbe**, puis d'une **préposition sans complément nominal** (le mot suivant est un
> auxiliaire, un verbe, une ponctuation, ou la fin) ouvre une **REL** du pronom à la préposition
> incluse ; la cible est la **tête du GN antécédent**.

La règle ne dépend d'aucun lexique de noms, de verbes ou de prépositions : elle teste des
**places structurelles**. Elle est limitée à l'**anglais** ; le français marque la relative par
`dont`/`que`, et une préposition orpheline y est agrammaticale. La préposition n'est « orpheline »
que si le mot suivant n'est **pas** un nom, un déterminant, un pronom ou un adverbe : `about the
film`, `about it`, `about today` restent des GP ordinaires.

Le code ajoute aussi une garde de frontière : un GN à déterminant ne peut plus contenir un
pronom sujet suivi d'un verbe. C'est la même condition grammaticale, et c'est elle qui rend le
GN « The film » exact.

## 3. Mesure sur dev / test

Gold vivant **612 phrases**, **239 cibles**, split déterministe `crc32(id) % 3` de
[`gold_split.py`](../tools/tests/linguistique/gold_split.py) ; `r035` est en **dev**. Mesure
`evaluer_bloc` de [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py).

| mesure | avant | **après** | Δ |
|---|---:|---:|---:|
| POS (tous) | 0,8625 | **0,8625** | 0 |
| F1 syntagmes | 0,7533 | **0,7549** | +0,0016 |
| précision / rappel | 0,7239 / 0,7853 | **0,7254 / 0,7869** | +0,0015 / +0,0016 |
| exact / labels | 236/237 | **237/238** | +1 / +1 |
| couverture | 0,9916 | **0,9958** | +0,0042 |
| tête (F1) | 0,8640 | **0,8651** | +0,0011 |
| dev — exact / labels | 160/161 | **161/162** | +1 / +1 |
| dev — POS | 0,8618 | **0,8618** | 0 |
| dev — F1 | 0,7476 | **0,7498** | +0,0022 |
| test — exact / labels | 76/76 | **76/76** | 0 |
| test — POS | 0,8642 | **0,8642** | 0 |
| test — F1 | 0,7663 | **0,7663** | 0 |

Lecture : l'attachement **exact** gagne le cas `r035` (236 → 237) ; le nombre de labels gagne
aussi le label REL (237 → 238), donc la couverture est **238/239 = 0,9958**, et non 1,0. Les
deux mesures restantes sont hors du périmètre de cette tâche : **1 span manquant** (`g017`, SUB
« that she would come ») et **1 cible fausse** (`s065`, REL synthétique : cible gold `elle`,
prédite `nage`). Le test ne bouge pas : il ne contient pas de relative zéro, donc il ne confirme
rien — il montre seulement l'absence d'effet de bord.

## 4. Contrôles

- **Diff du gold entier** : une seule phrase sur **612** change (`r035`) ; **0 token POS** sur
  **3 179** change. Le diff exact est : `+GN [0:8]`, `+REL [9:24]`, `+GV [25:31]` ;
  `−GN [0:12]`, `−GV [13:18]`, `−GV [19:31]`.
- **Contrôles négatifs de la règle** (même analyseur, anglais sauf mention) :

| phrase | attendu | observé |
|---|---|---|
| « The film she talks about **the book** is out. » | pas de REL (complément nominal) | pas de REL |
| « The film she talks about **it** is out. » | pas de REL (pronom objet) | pas de REL |
| « The film she talks about **today** is out. » | pas de REL (adverbe complément) | pas de REL |
| « The film talks about is out. » | pas de REL (pas de pronom sujet) | pas de REL |
| « Le film elle parle est sorti. » | pas de REL (français, pas de relative zéro) | pas de REL |

- **Généralisation hors du lexique de `r035`** : « The book **he reads about** is good. » rend
  une REL **[9:23]**, cible **`book`** — autre nom, autre pronom, autre verbe. La règle n'est donc
  pas liée aux mots du cas.
- **Portes** : `183/183` (autotest), `porte-bloc-linguistique` verte, `porte-produit` verte,
  **17 tests unitaires** dont le nouveau `test_relative_zero`.

## 5. Ce qui pourrait rendre ce résultat faux

1. **Un seul cas dans le gold, et il est en dev.** La règle a été écrite après avoir vu `r035` :
   le gain dev est *in-sample*. Le test ne bouge pas, ce n'est pas une confirmation hors
   échantillon.
2. **Listes fermées.** Les pronoms sujets et les prépositions viennent de listes ; un pronom ou
   une préposition inconnus ne déclenchent pas. Symétriquement, un complément nominal non
   reconnu après la préposition pourrait être pris pour une préposition orpheline.
3. **La frontière du GN est plus générale que `r035`.** Elle s'applique à tout GN à déterminant
   suivi d'un pronom sujet + verbe ; sur le gold elle ne change que `r035`, mais sur du texte
   libre elle peut modifier d'autres GN.
4. **Le gold est une convention.** La relative zéro est annotée une fois ; il n'y a pas d'accord
   inter-annotateurs sur ce cas.
5. **Le gain F1 est petit** (+0,0016) et vaut un span : il ne faut pas le lire comme un gain de
   segmentation général.

## 6. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — la fonction `relative_zero` et la
  garde de frontière du GN.
- [`test_bloc_linguistique.py`](../tools/tests/linguistique/test_bloc_linguistique.py) —
  `test_relative_zero` (cas gold, généralisation, cinq contrôles négatifs).
- [`autotest.py`](../tools/pensee/autotest.py) — les valeurs d'attachement recalées (237/238).
- [`pensee-r035.json`](pensee-r035.json) — les chiffres avant/après, dev/test, contrôles.
