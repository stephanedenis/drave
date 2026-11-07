# B13 — la convention des GV : le sujet hors du GV, F1 0,7549 → 0,7902

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Tâche** : J1.2 · **Date** : 2026-11-07 ·
> **Verdict** : ✅
> Les **322 FP / 180 FN** du plan sont les erreurs **de GV** du gold d'avant `r035` (F1 0,7533) ;
> après `r035` (J1.1), la base courante est **320 FP / 179 FN** (F1 0,7549). Le classement ne
> change pas : **144 FP de sujet (45 %)** dominent, puis 73 d'objet, 39 de troncature. Deux règles
> candidates sont mesurées : **le sujet hors du GV** (F1 **+0,0332**, 0 perte d'attachement) et
> **l'arrêt à l'adverbe final de temps** (F1 **+0,0026**). Les deux sont **gardées** et combinées :
> **F1 0,7549 → 0,7902** (dev **0,7875**, test **0,7962**), **POS 0,8625 inchangée**, **attachement
> 237/238 inchangé** (0 cible perdue), **183/183 portes**. S/D/N2 intouchés.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_sujet_hors_gv`,
> `ADVERBES_TEMPS`, la condition d'adverbe du GV), [`autotest.py`](../tools/pensee/autotest.py)
> (T110–T115, T156 recalés) ; JSON [`pensee-convention-gv.json`](pensee-convention-gv.json).

## 1. Le chiffre du plan et le chiffre courant

Le plan J1.2 porte **322 FP / 180 FN** : c'est la mesure **d'avant `r035`**. J1.1 a depuis réglé
`r035` ; la base courante est **320 FP / 179 FN**. Les deux classements sont identiques à un ou
deux près, et le gain de J1.2 se mesure sur la base courante.

| mesure | plan (avant `r035`, `25a6c0ff^`) | **courant** (`25a6c0ff`) |
|---|---:|---:|
| F1 syntagmes | 0,7533 | **0,7549** |
| précision / rappel | 0,7239 / 0,7853 | **0,7254 / 0,7869** |
| tp / fp / fn (tous) | 1463 / 558 / 400 | **1466 / 555 / 397** |
| **FP de GV** | **322** | **320** |
| **FN de GV** | **180** | **179** |
| POS | 0,8625 | **0,8625** |
| attachement exact | 236/237 | **237/238** |

La classification ci-dessous est faite sur les **GV seuls** (320 FP, 179 FN) ; les 555 FP et
397 FN du F1 incluent aussi les GN, GP, REL et SUB. Elle est reproductible par
`python3 tools/tests/linguistique/classer_gv.py` (le même script accepte `--module` pour une
copie du bloc).

## 2. Le classement des erreurs de GV

Le classement compare chaque GV prédit au GV du gold qui le recouvre le plus. FP = GV prédit qui
n'est pas exactement un GV du gold ; FN = GV du gold non retrouvé exactement.

| **FP de GV** | base | part | + sujet | + adverbe | **A+B** | ce que c'est |
|---|---:|---:|---:|---:|---:|---|
| **sujet** | **144** | 45 % | 4 | 144 | **5** | le GV commence avant le verbe, sur le sujet (« Il a couru ») |
| objet | 73 | 23 % | 75 | 73 | **75** | le GV avale un nom nu objet (« love music ») |
| tronque | 39 | 12 % | 42 | 40 | **42** | le GV est plus court que le gold (« venir » pour « Peux-tu venir ») |
| deux_cotes | 27 | 8 % | 18 | 25 | **15** | le GV déborde des deux côtés |
| adverbe | 16 | 5 % | 16 | 10 | **10** | le GV avale un adverbe final (« viens demain ») |
| parasite | 16 | 5 % | 16 | 16 | **16** | GV sans recouvrement (une préposition prise pour un verbe) |
| gauche_autre | 5 | 2 % | 3 | 6 | **4** | débordement à gauche hors GN sujet |
| **total** | **320** | 100 % | **174** | **315** | **167** | |

| **FN de GV** | base | part | + sujet | + adverbe | **A+B** | ce que c'est |
|---|---:|---:|---:|---:|---:|---|
| chev_droite | 75 | 42 % | 80 | 72 | **77** | le gold est plus long à droite (« souffle » vs « souffle fort ») |
| avale_GN | 51 | 28 % | 51 | 51 | **51** | le GV du gold est avalé par un GN/GP prédit |
| chev_deux | 28 | 16 % | 17 | 23 | **15** | recouvrement des deux côtés |
| tronque | 19 | 11 % | 19 | 19 | **20** | le GV prédit est à l'intérieur du gold |
| chev_gauche | 6 | 3 % | 3 | 9 | **5** | le GV prédit déborde à gauche |
| **total** | **179** | 100 % | **170** | **174** | **168** | |

Deux lectures dominent :

- **Le sujet est la première cause** : 144 FP, dont **133 sont des doublons** — le GV du
  générateur S (« Il a couru ») recouvre un GV correct du chunker (« a couru ») et reste dans
  l'union comme un second segment. Le gold, lui, est **unanime** : sur **712 GV**, **712**
  commencent par un `VERB` (590), un `AUX` (97) ou un `ADV` de négation (25, dont 24 `ne` et
  1 `still`) ; **aucun** ne commence par un sujet (`PRON`/`NOUN`). La règle « sujet hors du GV »
  n'est donc pas une correction locale : c'est **la convention du gold**.
- **L'adverbe final n'est pas une convention unique** : 39 GV du gold finissent par un `ADV`,
  mais 72 `ADV` sont hors GV, et deux phrases **identiques** sont annotées différemment —
  « Le vent souffle fort. » (`r019` : GV « souffle » ; `r186` : GV « souffle fort ») et
  « La voiture roule vite. » (`r051` : GV « roule » ; `r189` : GV « roule vite »). La règle
  d'adverbe est donc un **choix**, pas une vérité du gold ; c'est pourquoi elle est gardée dans
  sa forme **étroite** (circonstants de temps), et pourquoi la version large est rejetée (§ 4).

## 3. Les deux règles

### 3.1 Sujet hors du GV (`_sujet_hors_gv`)

> Un GV ne commence pas par son sujet. Si un GV du générateur S commence par un **pronom sujet**
> (y compris élidé `j'`), un **clitique** (`s'`, `l'`, `m'`, `t'`, `d'`) ou un **nom propre**
> suivi de son verbe, le sujet est émis comme **GN agent** et le GV commence au prédicat. Le
> clitique reste dans le GV (`elle s'ouvre` → GN « Elle », GV « s'ouvre »). La forme inversée
> `Peux-tu` n'est pas un sujet : elle reste un GV. Le générateur S n'est pas modifié : la règle
> s'applique à la lecture de ses segments, dans `bloc_linguistique.py`.

Le verbe est reconnu par le **POS contextuel** déjà calculé (`pos_verbes`) : « Elle téléphone »
est un `VERB` à 0,85 par la règle 3 a, même si le lexique ouvert le donne `NOUN` à 0,30. C'est ce
qui distingue la règle d'un simple découpage du premier token (le placebo du § 5 perd 38 phrases).

Portée : **français** (le générateur S ne segmente pas l'anglais). C'est la règle qui explique
le gain français de +0,0495 ; l'anglais ne gagne que par l'adverbe (+0,0044).

### 3.2 Arrêt à l'adverbe final de temps (`ADVERBES_TEMPS`)

> Un adverbe de **temps** final (`hier`, `demain`, `aujourd'hui`, `maintenant`, `yesterday`,
> `tomorrow`, `today`, `now`, `later`, `soon`, `tonight`) n'est pas dans le GV : « Tu viens |
> demain » donne GV « viens ». La négation (`ne`, `pas`…) n'est pas concernée : « ne dort pas »
> reste un GV. La règle ne s'applique qu'à l'adverbe **final** (suivi d'une ponctuation ou de la
> fin) ; « demain matin » n'est pas coupé.

Portée : **le chunker** (toutes langues). C'est la règle qui fait passer l'anglais de 0,8612 à
0,8656 et le français de 0,6980 à 0,6996.

### 3.3 Ce qui n'est pas gardé

- **L'adverbe large** (tout `ADV` final, POS) : F1 0,7552 (+0,0003) mais **test 0,7656 < 0,7663**.
  Il corrige 12 FP d'adverbe et crée 11 FP de troncature : le gold contradictoire ne permet pas
  de généraliser. C'est le contrôle de sensibilité du § 5.
- **L'objet hors du GV** (testé le 05/11, `gv_A_objet`) : F1 0,7531, **en baisse** ; 20 FP d'objet
  corrigés mais 13 FP de troncature créés. Les 75 FP d'objet et 51 FN `avale_GN` restent ouverts.

## 4. La mesure sur dev / test

Gold vivant **612 phrases**, **239 cibles**, split déterministe `crc32(id) % 3` de
[`gold_split.py`](../tools/tests/linguistique/gold_split.py) ; mesure `evaluer_bloc` de
[`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py). La base est le commit `25a6c0ff`
(J1.1) ; les variantes intermédiaires sont mesurées sur des copies du module, la combinaison
retenue est intégrée.

| mesure | base | **+ sujet** | **+ adverbe** | **A+B** |
|---|---:|---:|---:|---:|
| **F1 all** | 0,7549 | **0,7881** | **0,7575** | **0,7902** |
| F1 dev | 0,7498 | **0,7861** | **0,7520** | **0,7875** |
| F1 test | 0,7663 | **0,7924** | **0,7696** | **0,7962** |
| précision / rappel (all) | 0,7254 / 0,7869 | 0,7828 / 0,7933 | 0,7279 / 0,7896 | **0,7860 / 0,7944** |
| tp / fp / fn (all) | 1466 / 555 / 397 | 1478 / 410 / 385 | 1471 / 550 / 392 | **1480 / 403 / 383** |
| tête (F1) | 0,8651 | 0,9029 | 0,8651 | **0,9029** |
| POS | 0,8625 | 0,8625 | 0,8625 | **0,8625** |
| attachement exact / labels | 237/238 | 237/238 | 237/238 | **237/238** |
| couverture | 0,9958 | 0,9958 | 0,9958 | **0,9958** |

Deltas de la combinaison : **F1 +0,0353**, dev **+0,0377**, test **+0,0299**, tp **+14**,
fp **−152**, fn **−14**. Par langue : français **0,6980 → 0,7475** (+0,0495), anglais
**0,8612 → 0,8656** (+0,0044). Par source : réel **0,7503 → 0,7857**, synthétique
**0,7553 → 0,7888**, hand **0,8571 → 0,9016**.

**Phrases changées** (diff des segments prédits, phrase par phrase) :

| règle | phrases changées | gagnantes | perdantes | neutres |
|---|---:|---:|---:|---:|
| sujet | 147 | 140 | **0** | 7 |
| adverbe | 10 | 6 | **1** (`r190`) | 3 |
| A+B | 152 | 144 | **1** (`r190`) | 7 |

La seule phrase perdante est `r190` « Ils arrivent demain. » : le gold y **inclut** « demain »
dans le GV, alors que `r010`/`r030`/`r423`/`r427` l'en excluent. C'est la contradiction de
convention du § 2, pas un défaut de la règle.

**Vue linéaire** (partition `filtrer`, un segment par groupe — la vue « linéaire » du plan) :
F1 **0,8120 → 0,8144** (+0,0024), tp 1443 → 1450, fp 248 → 248, fn 420 → 413, attachement
**223/224 → 223/224**. La référence du plan (0,8104) est un instantané antérieur ; la base
mesurée ici est 0,8120. Le gain linéaire est petit parce que le filtre retire déjà le GV du S
qui contient un GV du chunker ; c'est la vue **alternative** (celle du F1 0,7549) qui compte les
doublons que la règle supprime.

## 5. Contrôles

### 5.1 Contrôles négatifs

| contrôle | ce qu'il fait | F1 | verdict |
|---|---|---:|---|
| **placebo sujet** | déplacer le premier token **sans condition** (même un verbe, un DET) | 0,7758 | 38 phrases perdantes contre **0** pour la règle conditionnelle |
| **placebo adverbe** | arrêter le GV au **dernier token**, sans condition de classe | 0,7440 | 627 FP contre 555 ; tronquer au hasard détruit des GV |
| **adverbe large** | tout `ADV` final hors du GV | 0,7552 | test **0,7656 < 0,7663** ; 12 FP d'adverbe corrigés, 11 FP de troncature créés |
| **attachement** | diff segment par segment sur les 239 cibles | — | **0 perdue, 0 gagnée, 0 span perdu** ; les **237 mêmes** cibles restent justes |
| **POS** | diff token par token | — | **0 token** changé (0,8625) |

### 5.2 Cas concrets

| phrase | attendu | observé |
|---|---|---|
| « Il a couru. » | GN « Il » + GV « a couru » | ✅ |
| « Il ne dort pas. » | GN « Il » + GV « ne dort pas » | ✅ (la négation reste dans le GV) |
| « Marie lit un livre. » | GN « Marie » + GV « lit » + GN « un livre » | ✅ |
| « Le garçon joue au ballon. » | GN déjà séparé, pas de second GN | ✅ (la garde « GN précédent » évite le doublon) |
| « Peux-tu venir ? » | GV « Peux-tu venir » (inversion) | ✅ (la forme en `-tu` n'est pas un sujet) |
| « Viens ici ! » | GV « Viens » + GP « ici » | ✅ l'impératif n'est pas coupé ; l'adverbe `ici` n'est pas temporel |
| « Elle s'ouvre. » | GN « Elle » + GV « s'ouvre » | ✅ (le clitique reste dans le GV) |
| « Tu viens demain ? » | GV « viens » | ✅ (`demain` final hors du GV) |
| « Le vent souffle fort. » | GV « souffle fort » (`r186`) ou « souffle » (`r019`) | ⚠️ le gold se contredit ; la règle étroite laisse « souffle fort » |

### 5.3 Le test n'a pas choisi la règle

La règle du sujet a été écrite après avoir vu les 144 FP du **gold** (dev + test mélangés dans
le classement). Le gain test (+0,0299) n'est donc pas une confirmation hors échantillon : c'est
la même convention, vue sur les mêmes phrases. Le test ne bouge pas contre la règle, mais il ne
la prouve pas non plus. C'est la limite principale, dite au § 6.

## 6. Ce qui pourrait rendre ce résultat faux

1. **Le gold est la source de la règle.** La convention « le sujet est un GN » est lue dans le
   gold (712/712) puis appliquée au gold : le gain est **in-sample**. Un autre corpus annoté
   autrement (GV incluant le sujet) inverserait le signe.
2. **L'adverbe final est contradictoire.** `r019`/`r186` et `r051`/`r189` sont deux conventions
   pour la même phrase. Le +0,0026 de la règle étroite est un **choix** ; la version large le
   montre (test en baisse). Le gain peut s'inverser sur un autre échantillon.
3. **Le POS contextuel est une heuristique.** Les verbes à suffixe nominal (`avance`, `amuse`)
   restent `NOUN` : 5 FP de sujet subsistent (r252, r277, r314, r354, r389).
4. **La règle du sujet est française.** Le générateur S ne segmente pas l'anglais ; les GV
   anglais à sujet initial (inversion `Do you come`, conjonction `reads and he writes`) ne sont
   pas traités. Le gain anglais ne vient que de l'adverbe.
5. **Les 75 FP d'objet et 51 FN `avale_GN` restent.** La règle d'objet testée le 05/11 perdait du
   F1 ; elle n'est pas reprise.
6. **La vue linéaire ne gagne que +0,0024.** Le filtre `filtrer` retire déjà le doublon du S ;
   le gain de +0,0353 est celui de la vue **alternative**, qui garde les deux segments et compte
   donc les doublons.
7. **L'attachement est un agrégat de 239 cibles.** Le diff segment par segment couvre les 239,
   mais une règle qui changerait un span cible sans changer le compte ne serait pas vue par le
   seul agrégat ; c'est pourquoi le diff est joint.

## 7. La suite

1. **L'objet hors du GV** : 75 FP d'objet, 51 FN `avale_GN` ; la version du 05/11 perdait du F1,
   une version ciblée (nom nu après un verbe, sans casser `a couru`) est à mesurer.
2. **Les 5 FP de sujet restants** : conjonctions de propositions (r252, r277), inversion
   (r314), verbes à suffixe nominal (r354, r389).
3. **La convention d'adverbe** : décider et **écrire** la convention du gold (r019/r186,
   r051/r189) avant d'ajouter une règle ; sinon chaque règle déplace le seuil.
4. **La vue linéaire** : le doublon du S est déjà filtré ; le prochain gain linéaire est dans la
   frontière du GV, pas dans le sujet.

## 8. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — `_sujet_hors_gv`, `ADVERBES_TEMPS`,
  la condition d'adverbe final du GV, le POS contextuel passé au chunker.
- [`autotest.py`](../tools/pensee/autotest.py) — T110–T115 et T156 recalés sur les nouvelles
  valeurs (183/183).
- [`test_bloc_linguistique.py`](../tools/tests/linguistique/test_bloc_linguistique.py) —
  `test_sujet_hors_du_gv`, `test_adverbe_final_hors_du_gv` (**19 tests**).
- [`pensee-convention-gv.json`](pensee-convention-gv.json) — les chiffres, le classement, les
  contrôles et les limites.
- [`classer_gv.py`](../tools/tests/linguistique/classer_gv.py) — le classement reproductible
  des FP/FN de GV (le même script accepte `--module` pour une copie du bloc).
- [Gold et split](../tools/tests/linguistique/evaluer_gold.py) — la mesure (`charger`,
  `evaluer_bloc`, `gold_split.py`).
