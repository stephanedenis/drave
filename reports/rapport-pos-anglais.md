# POS anglaise — les 176 VERB gold tagués NOUN viennent du défaut nominal, pas de la règle de contexte

> **Ligne de roadmap** : **A14** (gold anglais) · **Date** : 2026-11-06 · **Verdict** : ✅ trois règles
> générales mesurées sur **dev** puis **test** ; le paquet **R2+R3** — sans un mot de lexique nouveau —
> vaut **+7,44 pts de POS au test** et **+3,3 pts de F1** (+9,3 pts sur le F1 anglais) ; le paquet complet (**R1+R2+R3**)
> vaut **+9,76 pts au test**, mais **R1 exploite un lexique écrit sur ce gold** : son gain mesuré est
> en partie de la mémorisation et n'est pas comptable comme généralisation.
>
> **Snapshot** : HEAD `56eb43af` · `bloc_linguistique.py` SHA `084517d9…` · `gold.json` `3663be6c…`,
> `gold_reel.json` `05d4f6df…`, `gold_synthetique.json` `e3e704ce…` · split `gold_split.py`
> (`crc32(id) % 3 == 0` → test).
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_pos`, `POS_FERME`,
> `VERBES`, `ADJECTIFS`, `_est_verbe`, règle 3 bis), [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py)
> (`evaluer_bloc`), [`gold_split.py`](../tools/tests/linguistique/gold_split.py).
>
> **JSON** : [`pensee-pos-anglais.json`](pensee-pos-anglais.json).

## 1. Verdict

- **La confusion dominante n'est pas produite par la règle de contexte.** Sur les 176 VERB anglais
  tagués NOUN, **176 viennent du défaut nominal de `_pos`** (172 au défaut `NOUN` 0,30, 4 à la branche
  suffixe nominal 0,45 ; **aucun** ne porte `meta.contexte`), **0** de la règle « après DET/PRÉP/ADJ →
  nom ». Cette règle ne se déclenche que **33 fois** en anglais et elle a **raison 33/33** : elle est
  **trop timide**, pas trop gourmande.
- **`_pos` ignore le lexique verbal du module.** **100 des 176** formes sont dans `VERBES_CONNUS`, et
  `_est_verbe` — que le chunker utilise déjà — les reconnaît ; `_pos` ne le consulte jamais.
- **L'anglais n'est pas la langue la plus faible** : 76,48 % contre 75,43 % pour le français, et
  35,1 % des erreurs pour 36,1 % des jetons. Sa spécificité est la **forme** de l'erreur (65,2 % en
  VERB→NOUN) plus trois familles de bugs — classes fermées ambiguës, lexiques anglais incomplets,
  morphologie française appliquée à l'anglais — qui pèsent **27,0 %** de ses erreurs ; un quatrième,
  l'adjectif attribut, en ajoute 4,4 %.
- **Trois règles générales — R2 et R3 sans aucun lexique, R1 branchée sur le lexique verbal existant —
  valent +9,76 pts au test** (75,81 → 86,38 sur les 612) ; **le cœur propre (R2+R3) vaut +7,44 pts** et
  **+3,3 pts de F1**, **0 attachement perdu**.
- **R1 est mécaniquement juste mais non comptable** : 101/101 de ses correctifs anglais sont des
  membres exacts de `VERBES_CONNUS`, lexique ajouté le 05/11 pour les cibles d'attachement du **même**
  gold (commit `d400e188`). A14 l'avait déjà qualifié de « borne haute, à ne pas intégrer telle
  quelle » ; la mesure ci-dessous le confirme.

## 2. Dispositif et protocole

**Gold.** 612 phrases, 3 179 jetons : 402 phrases françaises (2 031 jetons) et 210 anglaises
(1 148 jetons). Le split de `gold_split.py` donne **dev** 422 phrases / 2 185 jetons (145 phrases
anglaises, 801 jetons) et **test** 190 phrases / 994 jetons (65 phrases anglaises, 347 jetons) ;
l'union redonne les 612, aucune phrase ne change de camp.

**Mesure.** `evaluer_gold.evaluer_bloc` : POS exacte au jeton, exactitude **fermée** (DET, PREP, PRON,
CONJ, AUX, ADV, NUM) et **ouverte** (le reste, ponctuation incluse), F1 syntagme et F1 « tête »,
attachement (exact, top-1, top-k). Les règles sont appliquées à une **copie en mémoire** du module
(`exec(compile(source))` avec `__file__` pointé sur l'original pour que `RACINE` reste le dépôt) :
aucun fichier du dépôt n'est modifié, aucun état n'est partagé. Les trois inserts exacts sont en
annexe.

**Protocole.** Diagnostic sur les 612 phrases (union) ; règles écrites puis mesurées **sur dev**, et
**revalidées sur test**. Une décision de mise au point de R3 a été informée par une phrase du test
(§ 7) : les chiffres test sont une borne légèrement optimiste, les chiffres dev la borne in-sample ;
les deux sont donnés partout.

## 3. Diagnostic : où sont les 270 erreurs anglaises ?

| | jetons | erreurs | POS | fermé | ouvert* | part des erreurs |
|---|---:|---:|---:|---:|---:|---:|
| français | 2 031 | 499 | 75,43 % | 89,67 % | 62,72 % | 64,9 % |
| anglais | 1 148 | 270 | 76,48 % | 90,65 % | 61,61 % | 35,1 % |
| tout | 3 179 | 769 | 75,81 % | 90,04 % | 62,34 % | 100 % |

\* ouverte au sens d'`evaluer_bloc` : tout ce qui n'est pas une des 7 classes fermées, ponctuation
comprise ; hors ponctuation, l'anglais ouvert est à 61,94 % (345/557).

L'anglais pèse **36,1 %** des jetons et **35,1 %** des erreurs : il n'est pas sur-représenté. C'est la
**structure** de ses erreurs qui est particulière.

### 3.1 La matrice anglaise (gold → prédit)

| classe gold | n | juste | taux | confusions |
|---|---:|---:|---:|---|
| VERB | 269 | 83 | **30,9 %** | **NOUN 176**, ADJ 5, AUX 4, ? 1 |
| NOUN | 248 | 238 | 96,0 % | ADJ 5, VERB 5 |
| ADJ | 40 | 24 | 60,0 % | NOUN 12, VERB 4 |
| PRON | 200 | 177 | 88,5 % | DET 14, NOUN 8, CONJ 1 |
| CONJ | 36 | 22 | 61,1 % | DET 12, NOUN 2 |
| ADV | 34 | 17 | 50,0 % | NOUN 15, PREP 1, ? 1 |
| DET | 213 | 213 | 100 % | — |
| AUX | 61 | 60 | 98,4 % | NOUN 1 |
| PREP | 43 | 43 | 100 % | — |
| PONCT | 3 | 0 | 0 % | ? 3 |
| NUM | 1 | 1 | 100 % | — |

Le **VERB→NOUN anglais (176) est 39,1 %** du VERB→NOUN global (450 : 176 en anglais, 274 en
français) ; le NOUN→VERB est 5 des 7 (2 en français). La confusion est donc **massivement un défaut
du tagger**, pas une propriété de l'anglais.

### 3.2 Les 30 formes les plus souvent mal taguées (anglais, union)

| # | forme | gold → prédit | n | # | forme | gold → prédit | n |
|---:|---|---|---:|---:|---|---|---:|
| 1 | that | CONJ → DET | 12 | 16 | talks | VERB → NOUN | 3 |
| 2 | that | PRON → DET | 11 | 17 | prepares | VERB → NOUN | 3 |
| 3 | leave | VERB → NOUN | 7 | 18 | live | VERB → ADJ | 3 |
| 4 | sings | VERB → NOUN | 6 | 19 | barks | VERB → NOUN | 3 |
| 5 | where | PRON → NOUN | 6 | 20 | rain | NOUN → VERB | 3 |
| 6 | writes | VERB → NOUN | 5 | 21 | falls | VERB → NOUN | 3 |
| 7 | speaks | VERB → NOUN | 5 | 22 | works | VERB → NOUN | 3 |
| 8 | sees | VERB → NOUN | 5 | 23 | stay | VERB → NOUN | 3 |
| 9 | leaves | VERB → NOUN | 4 | 24 | mention | VERB → NOUN | 3 |
| 10 | play | VERB → NOUN | 4 | 25 | cries | VERB → NOUN | 3 |
| 11 | runs | VERB → NOUN | 4 | 26 | is | VERB → AUX | 3 |
| 12 | arrives | VERB → NOUN | 4 | 27 | her | PRON → DET | 3 |
| 13 | late | ADV → NOUN | 4 | 28 | love | VERB → NOUN | 2 |
| 14 | table | NOUN → ADJ | 4 | 29 | out | ADV → NOUN | 2 |
| 15 | shines | VERB → NOUN | 3 | 30 | tired | ADJ → VERB | 2 |

Les ex æquo sont listés dans l'ordre de première occurrence. **Vingt et une** des trente lignes sont
des verbes, dont **quinze formes en `-s`** (`is` compris) ; trois lignes sont des classes fermées
(`that` ×2, `her`).

### 3.3 Les classes ouvertes

NOUN+VERB+ADJ = **557 jetons (48,5 %)** et **212 des 270 erreurs (78,5 %)** :

| classe | jetons | justes | taux |
|---|---:|---:|---:|
| VERB | 269 | 83 | 30,9 % |
| NOUN | 248 | 238 | 96,0 % |
| ADJ | 40 | 24 | 60,0 % |

Le problème est donc **concentré sur le verbe** : 269 jetons, 83 justes, et 186 erreurs (68,9 % des
erreurs anglaises) dont 176 en NOUN. À l'inverse, le nom anglais est presque parfait (96,0 %) et le
DET parfait (213/213).

## 4. Les cinq causes (et le bruit)

Partition exacte des **270** erreurs anglaises, sans double comptage :

| # | cause | effectif | part | exemples | traitée par |
|---|---|---:|---:|---|---|
| **C1** | **défaut nominal : le POS ouvert ne consulte pas le lexique verbal** | **176** | **65,2 %** | leave, sings, play, stay, arrives | R1 (lexique) + R2 (position) |
| C2 | classes fermées ambiguës : le DET l'emporte sur PRON/CONJ | 26 | 9,6 % | `that` 23, `her` 3 | R3 |
| C3 | lexiques fermés anglais incomplets (+ règle de majuscule) | 28 | 10,4 % | where 6, late 4, out 2, as 2, whose, when, mine, outside, am | données (pas une règle) |
| C4 | morphologie française appliquée à l'anglais | 19 | 7,0 % | table 4, live 3, rain 3, tired 2, arrive 2 | données |
| C5 | adjectif attribut inconnu après copule | 12 | 4,4 % | right 2, fast, calm, dark, absent, mean, fresh, quiet, alone, rare, hungry | R4 (piste, § 8) |
| C7 | bruit or/span + convention de copule | 9 | 3,3 % | PONCT 3, `don't` 2, `is` 3, `have` 1 | or |

**C1 en détail.** 126 formes en `-s`/`-es` (71,6 %), 50 formes nues (28,4 %), 0 en `-ing`/`-ed`
(les formes en `-ing`/`-ed` tombent sur la branche VERB 0,40, pas sur le défaut). **100 formes sont dans
`VERBES_CONNUS`** (56,8 %) — donc déjà connues du module. **165 sont précédées d'un sujet** :
85 d'un pronom (48,3 %), 80 d'un nom (45,5 %). La confiance de sortie est 0,30 pour 172 d'entre elles,
0,45 pour 4 : c'est bien le **défaut** qui parle, pas une règle de contexte.

**C2 en détail.** `that` est dans `POS_FERME["en"]["DET"]` **et** dans PRON et CONJ ; l'ordre du
dictionnaire fait gagner DET (0,92) partout. `her` est DET et PRON, même effet. Résultat : 23 `that`
(12 CONJ, 11 PRON) et 3 `her` (PRON) mal tagués.

**C3 en détail.** ADV 16 (`late` 4, `out` 2, `fast` 2, `maybe`/`Maybe` 2, `hard`, `outside`, `far`,
`again`, `now`, `down`, `n't` ; `outside` y est compté ADV→PREP), PRON 9 (`where` 6, `whose`,
`when`, `mine`), CONJ 2 (`as`), AUX 1 (`am`). Total 28. Trois le sont via la règle « majuscule →
NOUN » (`As` 2, `Maybe` 1).

**C4 en détail.** 15 par les suffixes français : `-able`/`-al` → ADJ sur des noms (table 4, meal 1),
`-ive` → ADJ sur des verbes (live 3, arrive 2), `-ed`/`-ing` → VERB sur des adjectifs (tired 2,
exciting 1), `-er` → VERB sur des noms (morning, dinner). 4 par `VERBES["en"]`, qui contient des noms
(`rain` 3) ou des adjectifs (`open` 1).

**C7 en détail.** 3 jetons de ponctuation comptés dans les `mots` du gold (`PONCT`), 2 jetons de
`don't` que le tokeniseur ne coupe pas comme le gold (`do` + `n't`), 4 conventions de gold où la
copule est étiquetée VERB (`is` 3, `have` 1) alors que le lexique la met en AUX.

### 4.1 Deux hypothèses réfutées

- **« La règle de contexte DET/PRÉP/ADJ → nom est trop gourmande » : réfutée.** Elle convertit 33
  jetons anglais, **tous** gold NOUN (33/33) ; elle ne touche **aucun** des 176. En français elle est
  moins précise : 10 conversions, 7 NOUN ; les 3 VERB, toutes après PRÉP, sont des infinitifs
  (`attraper`, `manger` ×2).
- **« La règle littérale “après DET/PRÉP/ADJ, tout est nom sauf verbe irrégulier connu” suffit » :
  réfutée.** Appliquée seule (conversion de tout VERB non `_est_verbe` après DET/PRÉP/ADJ), elle fait
  **0 correctif et 4 casses** (dev −0,14 pt, test −0,10 pt, anglais −0,17 pt) : elle avale les
  infinitifs après PRÉP (`to eat` ×2) et des verbes français absents du lexique (`lit`, `attrape`).
  L'exception « sauf verbe connu » n'est fiable que si le lexique est complet — il ne l'est pas. La
  bonne direction est l'inverse : **le lexique d'abord, le contexte seulement pour les formes
  ambiguës** (R1), et **la position du sujet** (R2).

## 5. Trois règles générales, mesurées sur dev puis test

### 5.1 R1 — le lexique verbal tranche le défaut ouvert

**Énoncé.** Un mot inconnu n'est pas un nom par défaut : si le lexique verbal productif le connaît
(`_est_verbe`, qui gère aussi base + `-s`/`-ed`/`-ing`), il est VERBE ; la position nominale
(DET/PRÉP/ADJ) ne le convertit en nom que si la confiance verbale est faible (≤ 0,5).

**Insertion.** `_pos` après le test `ADJECTIFS` (l. 609-610 du snapshot) ; seuil de la boucle 3 bis
`> 0,45` → `> 0,5` (l. 1055). Code exact en annexe A.1.

**Mesure.** 190 correctifs, **0 cassé** (101 en anglais, 89 en français). Dev **+6,31 pt**, test
**+5,23 pt** ; anglais 76,48 → **85,28 %**, français 75,43 → **79,81 %**. F1 et attachement
**inchangés**. **MAIS** 101/101 correctifs anglais sont des membres exacts de `VERBES_CONNUS` (0 hors
lexique) : le gain est mécaniquement réel sur ce gold, et non comptable comme généralisation (§ 7).

**Sensibilité du seuil.** Le seuil 0,5 est **nécessaire** : à 0,45, R1 gagne 8 correctifs de plus mais
**casse 15 jetons** (`porte` 6, `bus` 3, `flower` 2, `cours`, `painting`, `painter`, `leaves`) — des
noms que le lexique verbal revendique par sa morphologie (`bus` = `bu` + `-s`, `flower` = `flow` +
`-er`). Coût accepté de 0,5 : 3 infinitifs français après PRÉP (`attraper`, `manger` ×2) restent
convertis en noms, comme avant.

### 5.2 R2 — la position du sujet tranche le nom/verbe

**Énoncé.** (a) après un **pronom sujet**, un mot inconnu est un verbe (sauf désinence nominale
connue) ; (b) une forme en **`-s`/`-es` après un nom sujet** est un verbe. (b) s'applique **après** la
résolution nominale (3 bis), sinon un nom transitoire (« gardener ») fait dérailler la chaîne.

**Insertion.** (a) après `pos_idx`, avant 3 bis (l. 1052) ; (b) après la boucle 3 bis (l. 1061). Code
exact en annexe A.2.

**Mesure.** **235 correctifs, 0 cassé** (147 anglais, 88 français). Dev **+7,60 pts**, test
**+6,94 pts** ; anglais **89,29 %**, français **79,76 %**. C'est la **seule règle qui bouge le F1** :
dev 0,5820 → **0,6153**, test 0,5914 → **0,6243** (+3,3 pts), F1 tête +1,8 pt ; attachement inchangé.
Prise seule, (b) sans (a) casse 1 jeton (« books » dans *She loves books*, parce que « loves » est
encore NOUN) ; avec (a) d'abord, 0 casse.

### 5.3 R3 — un DET ambigu exige un nom à sa droite

**Énoncé.** Un mot de classe fermée **ambigu** (DET ∩ PRON/CONJ : `that`, `her`) n'est DET que s'il
introduit une tête nominale ; sinon il est PRON, ou CONJ après un verbe. Un DET non ambigu (`the`) n'est
jamais touché — c'est ce qui protège « the rain » et « le ».

**Insertion.** après `pos_idx`, **après R2(a)** et avant 3 bis (l. 1052) : l'ordre compte, R3 doit voir
le verbe que R2 vient de poser. Code exact en annexe A.3.

**Mesure.** 15 correctifs, **0 cassé** (11 PRON, 4 CONJ). Dev **+0,50 pt**, test **+0,40 pt** ; anglais
**77,79 %**. Dans le paquet R2+R3, la synergie porte le total à **+0,68 pt dev / +0,50 pt test** de plus
que R2 seul. F1 et attachement inchangés.

### 5.4 Les mesures, règle par règle

| variante | dev POS | Δ dev | test POS | Δ test | anglais | français | F1 dev / test | att. dev / test | corrigés / cassés |
|---|---:|---:|---:|---:|---:|---:|---|---|---:|
| **V0** | 75,47 | — | 76,56 | — | 76,48 | 75,43 | 0,5820 / 0,5914 | 0,9387 / 0,9079 | — |
| **R1** | 81,78 | +6,31 | 81,79 | +5,23 | 85,28 | 79,81 | 0,5820 / 0,5914 | idem | 190 / 0 |
| **R2** | 83,07 | +7,60 | 83,50 | +6,94 | 89,29 | 79,76 | **0,6153 / 0,6243** | idem | 235 / 0 |
| **R3** | 75,97 | +0,50 | 76,96 | +0,40 | 77,79 | 75,43 | 0,5820 / 0,5914 | idem | 15 / 0 |
| **R2+R3** | 83,75 | **+8,28** | 84,00 | **+7,44** | 91,03 | 79,76 | 0,6153 / 0,6243 | idem | 255 / 0 |
| **R1+R2+R3** | 86,41 | **+10,94** | 86,32 | **+9,76** | **93,21** | **82,52** | 0,6153 / 0,6243 | idem | 336 / 0 |
| R4 (piste) | 76,20 | +0,73 | 77,26 | +0,70 | 77,53 | 75,97 | 0,5820 / 0,5914 | idem | 23 / 0 |
| R1l (rejetée) | 75,33 | −0,14 | 76,46 | −0,10 | 76,31 | — | — | — | 0 / 4 |

Les colonnes « anglais » et « français » sont `evaluer_bloc` sur les sous-ensembles de langue (union
des 612) : c'est là que se lit le gain réel (V0 76,48 → 93,21 anglais avec le paquet complet). Sur
les 612 phrases : **75,81 → 86,38** avec R1+R2+R3, **75,81 → 83,83** avec R2+R3. L'attachement est
**strictement inchangé** partout (exact 222/239 = 0,9289 ; top-k 221/239 = 0,9247 ; par langue,
anglais 86/88 = 0,9773 avec un conditionnel 86/86 = 1,0, français 136/151 = 0,9007).

### 5.5 Pourquoi R2 gagne 9,3 pts de F1 anglais sans toucher l'attachement

Le chunker (`_syntagmes_simple`) utilisait déjà la règle « après un pronom sujet → verbe », mais **pas**
« après un nom sujet ». R2(b) ferme cet écart : les GV anglais « the cat sleeps », « the train arrives »
sont enfin détectés. Sur les 702 segments anglais : tp 376 → **448**, fp 108 → **82**, fn 326 → **254**
(précision 0,7769 → 0,8453, rappel 0,5356 → 0,6382) ; F1 anglais 0,6341 → **0,7273**, F1 tête
0,7791 → **0,8263**. L'attachement ne bouge pas parce qu'il est mesuré sur les segments déjà trouvés au
bon span (222/239) : le gain est un gain de **couverture de segmentation**, pas de cible.

## 6. Contrôles

### 6.1 Contrôle négatif — même action, position aléatoire

Pour chaque règle, on rejoue le **même nombre** de changements, de la **même direction**, sur un jeton
tiré au hasard dans la même phrase (200 tirages, graine 20261106) :

| règle | actions | placebo moyen | p05 | p95 | max | gain observé (dev) |
|---|---:|---:|---:|---:|---:|---:|
| R1 | 190 | −2,46 pts | −2,99 | −1,82 | −1,54 | **+6,31** |
| R2 | 235 | −2,83 pts | −3,43 | −2,23 | −1,86 | **+7,60** |
| R3 | 15 | −0,21 pt | −0,38 | −0,06 | +0,16 | **+0,50** |
| paquet | 336 | −4,18 pts | −4,91 | −3,43 | −2,80 | **+10,94** |

Pour R1, R2 et le paquet, **le meilleur tirage aléatoire reste négatif** ; pour R3 (15 actions, petit
nombre), le maximum est +0,16 pt, très loin des +0,50 observés. Le gain observé est à l'opposé de la
distribution dans les quatre cas.

### 6.2 Contrôle français

Les trois règles ne sont pas anglaises : elles **aident aussi le français** (R1 +4,55/+4,01 pts,
R2 +4,33/+4,32, R3 0,0) sans le casser. R2 corrige même **58 jetons français hors lexique** (sur 88) :
« la position du sujet » est une règle de langue, pas un ajustement anglais.

### 6.3 Contrôle de contamination — d'où viennent les correctifs ?

| règle | correctifs anglais | hors `VERBES_CONNUS` | dans `VERBES_CONNUS` |
|---|---:|---:|---:|
| R1 | 101 | **0** | 101 |
| R2 | 147 | **66** | 81 |
| R3 | 15 | **15** | 0 |
| R2+R3 | 167 | **86** | 81 |
| R1+R2+R3 | 192 | **88** | 104 |

`VERBES_CONNUS` a été ajouté au dépôt le **05/11** (commit `d400e188`, « LE LEXIQUE VERBAL : EXACT
0,0962 → 0,1381 ») avec le commentaire « mesuré le 05/11 sur les 22 GP restants » : il a été écrit en
regardant ce gold. Le split dev/test ne protège **pas** contre cette contamination, puisque le
lexique a été écrit sur l'ensemble du gold, test compris. Conclusion : **R1 est une correction de
cohérence** (le chunker consulte `_est_verbe`, le POS non), pas un gain de généralisation mesuré ;
**R2 et R3 sont propres** — aucune liste de mots du gold, et 81 correctifs anglais hors lexique à
elles deux (86 pour le paquet, synergies comprises).

### 6.4 Les seuils du verdict restent verts

Tous les seuils de `evaluer_gold` restent vrais sous les deux paquets, et leurs marges augmentent :

| seuil (plancher) | V0 | R2+R3 | R1+R2+R3 |
|---|---:|---:|---:|
| POS main (0,85) | 0,8857 | 0,8952 | 0,8952 |
| POS réel (0,70) | 0,7661 | 0,8613 | 0,8831 |
| POS synthétique (0,60) | 0,7296 | 0,7568 | 0,7954 |
| F1 réel (0,16) | 0,5806 | 0,6230 | 0,6230 |

Aucune porte n'est lancée ici : **aucun code n'a été modifié**.

## 7. Ce qui pourrait rendre ces chiffres faux

1. **Protocole.** Le diagnostic a été fait sur l'union (612), pas sur dev seul : les règles ont donc
   « vu » le test au moment d'être écrites. Une décision de R3 (le garde-fou de tête nominale) a été
   affinée après la phrase **r117** (« She calls her mother »), qui est dans test, et **r025/r169**
   (dev). Le chiffre test est une borne **légèrement optimiste** ; le chiffre dev est la borne
   in-sample.
2. **Taille.** Le test anglais fait **347 jetons** : un jeton vaut 0,29 pt. Les +14,70 pts anglais au
   test (R1+R2+R3) reposent sur **51 correctifs nets** ; les +7,44 pts du paquet R2+R3 sur **74
   correctifs** (dont 46 anglais) répartis sur les 994 jetons du test.
3. **Gold templaté.** `gold_reel` est engendré par patrons : les mêmes formes reviennent (sings,
   leaves…). Une règle qui gagne sur 3 occurrences dev peut n'en voir qu'une dans test ; la
   consistance dev/test (même signe, même ordre de grandeur) est rassurante, pas démonstrative.
4. **Lexique in-sample.** Voir § 6.3 : le +8,8 pts anglais de R1 est, à la lettre, de la mémorisation.
   Ne pas le citer comme un gain de généralisation.
5. **Seuils de confiance.** R1 et R2 s'appuient sur l'échelle de confiance de `_pos` (0,30 / 0,40 /
   0,45 / 0,50 / 0,55). Si l'échelle change, les seuils sont à recalibrer — c'est le seul paramètre
   « réglé » des règles.
6. **Effets de bord hors gold.** R2(b) casserait un composé nom+nom (« the car mats ») ; R2(a)
   casserait « I, John, … » ; R3 tranche `that` selon la convention du gold (relative = PRON,
   complétive = CONJ) : 3 résidus sont exactement les conventions déjà signalées par A14.
7. **Fuite inter-langue.** `_est_verbe` est bilingue : R1 fait de `As` un VERB via le `as` français
   (auxiliaire d'*avoir*). Sur ce gold le solde est nul (`As` était déjà faux en NOUN), mais une
   version par langue est préférable.
8. **L'attachement ne bouge pas.** Ces règles ne sont **pas** un levier d'attachement : elles
   alignent la couche POS sur le chunker et rendent l'erreur mesurable. Ne pas les vendre comme un
   gain de bout en bout.

## 8. Recommandation

1. **Intégrer R2** ((a) puis (b), dans cet ordre) : **+6,94 pts test**, **+9,3 pts de F1 anglais**
   (+3,3 pts toutes langues), 0 cassé, aucune donnée nouvelle. C'est le meilleur rapport effet/risque
   du lot.
2. **Intégrer R3** ensuite : +0,50 pt test dans le paquet, ~10 lignes, corrige une classe de bugs
   (`that`/`her`) sans lexique. Prévoir la version à deux phases si l'on veut supprimer le résidu
   r297 (un mot transitoirement VERB lu par R3 avant la résolution nominale) : +1 jeton.
3. **R1 : intégrer le câblage, ne pas compter le gain.** La cohérence (`_pos` doit consulter le
   lexique verbal que le chunker utilise déjà) est réelle ; le +8,8 pts anglais ne l'est pas. Le
   conditionner à un **lexique anglais reconstruit hors gold** (source externe ou corpus disjoint),
   puis re-mesurer. Sans cela, le paquet R2+R3 est la seule mesure défendable.
4. **Pistes suivantes, mesurées ici pour information** : R4 (copule → ADJ pour un mot inconnu) vaut
   **+0,70 pt test**, 23 correctifs (12 anglais, 11 français), 0 cassé — non retenue dans les trois
   règles pour rester dans le périmètre demandé, mais c'est le levier suivant. Puis les **données** :
   compléter les classes fermées anglaises (C3 : 28 erreurs) vaut plus que n'importe quelle règle
   restante.
5. **Ne pas toucher** à la règle 3 bis dans le sens « plus de nom » : la mesure la donne à 33/33 en
   anglais. Le problème n'était pas sa gourmandise, mais le défaut qu'elle ne voyait jamais.

## 9. Reproduction

Le dispositif complet tient dans un script hors dépôt (~200 lignes) : chargement de
`tools/tests/linguistique/{gold,gold_reel,gold_synthetique}.json`, split `gold_split.dev/test`,
copie en mémoire de `bloc_linguistique.py`, application des inserts A.1–A.3, puis
`evaluer_gold.evaluer_bloc` sur dev, test, anglais, français. Les inserts exacts et les ancres sont
ci-dessous ; les chiffres du JSON sont ceux de ce script, rejoués le 2026-11-06. Aucun fichier du
dépôt n'a été modifié (git status des deux fichiers : ajout seul).

### Annexe A.1 — R1 (deux modifications)

```python
# dans _pos(), après le test ADJECTIFS (l. 609-610)
        if _est_verbe(n):
            return "VERB", True, 0.5

# boucle 3 bis (l. 1055) : le seuil passe de 0,45 à 0,5 pour couvrir la confiance 0,5 de R1
            if e.type != "VERB" or e.confiance > 0.5 or k == 0:
```

### Annexe A.2 — R2(a) puis R3, avant la boucle 3 bis (après `pos_idx`, l. 1052)

```python
        # 3 a. apres un pronom sujet, un mot inconnu est un verbe (« she sings ») ; l'exception
        # est morphologique : une desinence nominale reste un nom (« happiness »).
        _nominales = ("tion", "sion", "ness", "ity", "ité", "ance", "ence", "ment", "ship")
        for _k, _i in enumerate(pos_idx):
            _e = etiquettes[_i]
            if _k == 0 or _e.type not in ("NOUN", "ADJ") or _e.confiance > 0.45:
                continue
            _av = etiquettes[pos_idx[_k - 1]]
            if (_av.type == "PRON" and _normaliser(_av.valeur) in SUJETS
                    and not _normaliser(_e.valeur).endswith(_nominales)):
                etiquettes[_i] = Etiquette("pos", "VERB", _e.valeur, _e.debut, _e.fin, self.nom,
                                           0.5, candidats=["verb"], langue=lg, script=script,
                                           meta={"ouvert": True, "contexte": "pron_sujet"})

        # 3 b. un DET **ambigu** sans nom a sa droite n'est pas un DET (« the book that I
        # read », « he speaks to her ») : c'est un PRON, ou un CONJ apres un verbe.
        _lexd = POS_FERME.get(lg, POS_FERME["fr"])
        for _k, _i in enumerate(pos_idx):
            _e = etiquettes[_i]
            if _e.type != "DET":
                continue
            if _normaliser(_e.valeur) not in (_lexd.get("PRON", set()) | _lexd.get("CONJ", set())):
                continue
            _suiv = etiquettes[pos_idx[_k + 1]] if _k + 1 < len(pos_idx) else None
            if _suiv is not None and (_suiv.type in ("NOUN", "ADJ", "NUM") or (
                    _suiv.type == "VERB" and _suiv.confiance <= 0.45
                    and not _est_verbe(_suiv.valeur))):
                continue
            _av = etiquettes[pos_idx[_k - 1]] if _k else None
            _cls = "CONJ" if (_av is not None and _av.type in ("VERB", "AUX")) else "PRON"
            etiquettes[_i] = Etiquette("pos", _cls, _e.valeur, _e.debut, _e.fin, self.nom, 0.6,
                                       candidats=[_cls.lower()], langue=lg, script=script,
                                       meta={"ouvert": False, "contexte": "det_sans_nom"})
```

### Annexe A.3 — R2(b), après la boucle 3 bis (l. 1061)

```python
        # 3 a bis. une forme en -s/-es apres un NOM sujet est un verbe (« the cat sleeps »).
        for _k, _i in enumerate(pos_idx):
            _e = etiquettes[_i]
            if _k == 0 or _e.type != "NOUN" or _e.confiance > 0.45:
                continue
            _av = etiquettes[pos_idx[_k - 1]]
            if _av.type == "NOUN" and _normaliser(_e.valeur).endswith(("s", "es")):
                etiquettes[_i] = Etiquette("pos", "VERB", _e.valeur, _e.debut, _e.fin, self.nom,
                                           0.5, candidats=["verb"], langue=lg, script=script,
                                           meta={"ouvert": True, "contexte": "nom_sujet_3s"})
```

> **Non intégré.** Ces inserts sont des propositions mesurées, pas du code appliqué : la mission
> interdisait de modifier l'existant. Les lignes citées sont celles du snapshot `084517d9…` ; toute
> évolution de `_pos` ou de la boucle 3 bis décale les ancres, pas les règles.
