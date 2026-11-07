# POS — R4 + classes fermées : +1,19 pt dev / +1,11 test en paquet sûr, +1,51/+1,51 en paquet max

> **Ligne de roadmap** : **A25** (gold anglais) · **B13** (moteur de pensée) · **Date** : 2026-11-06 ·
> **Verdict** : ✅ les deux derniers leviers POS sont mesurés. **R4 bilingue** vaut **+0,74 dev /
> +0,71 test** (23 correctifs, 0 cassé), **les classes fermées** **+0,78 / +0,81** (25 correctifs,
> 0 cassé). Le **paquet sûr** (R4-en + classes fermées) vaut **+1,19 / +1,11**, **37/0**, F1
> **+0,0007**, attachement **222/222**. Le **paquet max** (R4 bilingue) vaut **+1,51 / +1,51**,
> 48/0, mais **11 faux→faux** et **5 faux positifs français** sur les 50 textes libres. R4 n’est
> donc **pas « 0 perte »** : « 0 cassé » est une propriété d’exactitude, pas de sens.
>
> **Snapshot** : référence **B13** commit `2ba393b0`, `bloc_linguistique.py` SHA
> `f3db75fc…`, gold `3663be6c…` / `05d4f6df…` / `e3e704ce…` ; split `gold_split.py`
> (`crc32(id) % 3 == 0` → test). Le dépôt a bougé **pendant** la mesure (correctif d’élision,
> gold corrigé) : un instantané HEAD `dd0e5e47…` sert de contrôle de reproductibilité (§ 2.3),
> pas de référence.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_pos`, `POS_FERME`,
> boucles 3 a/3 b/3 a bis), [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`gold_split.py`](../tools/tests/linguistique/gold_split.py). Copies **en mémoire** du module ;
> patches appliqués à des copies `/tmp` ; **aucun fichier du dépôt modifié**.
>
> **JSON** : [`pensee-pos-r4.json`](pensee-pos-r4.json) (patchs exacts inclus).

## 1. Verdict

- **R4 bilingue** : **+0,74 dev / +0,71 test** (POS 84,55 %), **23 correctifs / 0 cassé**, F1
  **strictement inchangé** (0,6181), attachement **222/222**. C’est la reproduction de la piste
  A25 (+0,73 / +0,70, 23/0).
- **Classes fermées** : **+0,78 dev / +0,81 test** (POS 84,62 %), **25 correctifs / 0 cassé**,
  F1 **+0,0007** (0,6181 → 0,6188, anglais 0,7273 → 0,7295), attachement **222/222**.
- **Paquet sûr** (R4-en + classes fermées) : **+1,19 dev / +1,11 test**, POS **85,00 %**, **37/0**,
  **2 faux→faux** (born, hung), F1 0,6188, attachement 222/222 ; **1 seul changement** sur les
  50 textes libres (`Where` interrogatif, faux).
- **Paquet max** (R4 bilingue + classes fermées) : **+1,51 / +1,51**, POS **85,34 %**, **48/0**,
  **11 faux→faux**, F1 0,6188, attachement 222/222 ; **9 changements libres** (3 justes, 6 faux).
- **Les deux contrôles demandés passent** — `He is a doctor.` reste NOUN, `He is running.` reste
  VERB — **mais pas pour la bonne raison** : le premier est protégé par le DET `a`, le second par
  la désinence `-ing`. R4 n’a **aucun garde nom/verbe** : `He is doctor.`, `She is president.`,
  `He remains president.`, `They became members.` et les participes irréguliers `born`/`hung`
  deviennent ADJ. En français, `Il est médecin.`, `La réunion est reportée.` et
  `Les enfants sont arrivés.` aussi.
- **Placebo** : sur 200 tirages (mêmes actions, mêmes nombres, jetons aléatoires dans la même
  phrase), le **maximum** du placebo reste **sous** le gain observé pour les deux leviers et les
  deux paquets (§ 6).
- **F1** : R4 n’ajoute **rien** au F1 ; les classes fermées ajoutent **+0,0007**, expliqué par un
  seul segment (`The children play outside`, r197). **Le levier est POS, pas F1.**
- **Attachement** : **strictement 222/222** partout (couverture 0,9289, top-k 221), sauf la
  variante « large » des classes fermées qui perd 1 attachement (221/221) — rejetée.

### 1.1 Les deux leviers, seuls

| variante | POS tout | dev | Δ dev | test | Δ test | corr. / cassés | faux→faux | F1 | attachement |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **V0** (B13) | 83,83 | 83,75 | — | 84,00 | — | — | — | 0,6181 | 222/222 |
| **R4-en** | 84,21 | 84,16 | +0,41 | 84,31 | +0,31 | 12 / 0 | 8 | 0,6181 | 222/222 |
| **R4-fr** | 84,18 | 84,07 | +0,32 | 84,41 | +0,41 | 11 / 0 | 9 | 0,6181 | 222/222 |
| **R4 bilingue** | **84,55** | **84,49** | **+0,74** | **84,71** | **+0,71** | **23 / 0** | **17** | 0,6181 | 222/222 |
| **Classes fermées** | **84,62** | **84,53** | **+0,78** | **84,81** | **+0,81** | **25 / 0** | **0** | **0,6188** | 222/222 |
| Classes + `fast` | 84,68 | 84,58 | +0,83 | 84,91 | +0,91 | 27 / 0 | 1 | 0,6188 | 222/222 |

### 1.2 Les paquets

| paquet | POS tout | dev | Δ dev | test | Δ test | corr. / cassés | faux→faux | F1 | att. | 50 textes libres |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **R4-en + classes** | **85,00** | **84,94** | **+1,19** | **85,11** | **+1,11** | **37 / 0** | **2** | 0,6188 | 222/222 | 1 faux (`Where`) |
| R4-en + classes sans `where` | 84,81 | 84,76 | +1,01 | 84,91 | +0,91 | 31 / 0 | 2 | 0,6188 | 222/222 | 0 changement |
| **R4 bilingue + classes** | **85,34** | **85,26** | **+1,51** | **85,51** | **+1,51** | **48 / 0** | **11** | 0,6188 | 222/222 | 3 justes / 6 faux |
| R4 bilingue + classes sans `where` | 85,15 | 85,08 | +1,33 | 85,31 | +1,31 | 42 / 0 | 11 | 0,6188 | 222/222 | 3 justes / 5 faux |
| R4 bilingue + classes + `fast` | 85,37 | 85,31 | +1,56 | 85,51 | +1,51 | 49 / 0 | 12 | 0,6188 | 222/222 | 3 justes / 6 faux |

Le **paquet sûr** est le meilleur rapport effet/risque : il ne laisse que `born` et `hung` en
faux→faux, et un seul changement libre (faux). Le **paquet max** gagne +0,32 pt de plus au test,
au prix de 9 faux→faux français et de 5 faux positifs français sur les textes libres.

## 2. Dispositif et protocole

### 2.1 Gold et split

**Gold.** 612 phrases, 3 179 jetons : 402 françaises (2 031 jetons), 210 anglaises (1 148). Le split
de `gold_split.py` donne **dev** 422 phrases / 2 185 jetons (145 anglaises, 801) et **test** 190
phrases / 994 jetons (65 anglaises, 347) ; l’union redonne les 612. Le test anglais fait **347
jetons : 1 jeton = 0,29 pt**.

**Mesure.** `evaluer_gold.evaluer_bloc` : POS exacte au jeton ; exactitude **fermée**
(DET, PREP, PRON, CONJ, AUX, ADV, NUM) et **ouverte** ; F1 syntagme, F1 « tête » ; attachement
(exact, top-k, couverture). Les règles sont appliquées à une **copie en mémoire** du module
(`exec(compile(source))`, `__file__` pointé sur le dépôt) ; les patches sont des remplacements de
chaîne ou des mutations de `POS_FERME["en"]`. **Aucun fichier du dépôt n’est modifié.**

### 2.2 Référence et contrôle HEAD

La fiche B13 est la référence : elle reproduit **exactement** 83,83 % / 0,6181 / 222-222 avec le
module `2ba393b0` et le gold B13. Le dépôt a bougé pendant la session (correctif d’élision, gold
corrigé) ; un instantané HEAD `dd0e5e47…` + gold `e159db…` est mesuré en contrôle. Les **gains
POS sont identiques** (+0,74/+0,71 ; +0,78/+0,81 ; +1,51/+1,51), mais le F1/attachement de base
diffèrent (0,6474 / 235-236) : ce sont les changements parallèles, pas les deux leviers.

| état | POS | fermé | ouvert | F1 | F1 anglais | F1 tête | attachement | couverture |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **B13 (référence)** | 83,83 | 91,33 | 76,73 | **0,6181** | 0,7273 | 0,7511 | **222/222** | 0,9289 |
| HEAD instantané | 83,83 | 91,33 | 76,73 | 0,6474 | 0,7273 | 0,7671 | 235/236 | 0,9874 |

## 3. R4 — après une copule, un mot inconnu est un ADJECTIF

### 3.1 Énoncé et insertion

**Énoncé.** Après une **copule** (`is`, `are`, `was`, `seems`, `looks`, `est`, `semble`…), un mot
inconnu (**NOUN**, confiance ≤ 0,45) est un **ADJECTIF** attribut.

**Insertion.** Dans `Heuristique.analyser`, **après la boucle « 3 a bis » (R2b)** et **avant**
`# 4. phrase + pragmatique`. La liste `COPULES` est stricte : les verbes à objet direct
(`feel`, `taste`, `smell`, `grow`, `turn`, `get`, `keep`) en sont exclus — mesuré : ils convertissent
des noms (`The farmers grow wheat` → `wheat` ADJ).

Le code exact est en **annexe A.1** ; il est aussi dans le JSON (`patchs_exacts.r4`).

### 3.2 Mesure

| variante | dev | Δ | test | Δ | corr. | cassés | faux→faux | F1 | att. |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| R4-en | 84,16 | +0,41 | 84,31 | +0,31 | 12 | 0 | 8 | 0,6181 | 222/222 |
| R4-fr | 84,07 | +0,32 | 84,41 | +0,41 | 11 | 0 | 9 | 0,6181 | 222/222 |
| **R4 bilingue** | **84,49** | **+0,74** | **84,71** | **+0,71** | **23** | **0** | **17** | 0,6181 | 222/222 |
| R4 bilingue + garde `_est_verbe` | 84,49 | +0,74 | 84,61 | +0,61 | 22 | 0 | 9 | 0,6181 | 222/222 |
| R4-en « large » | 84,12 | +0,37 | 84,31 | +0,31 | 12 | **1** | 8 | 0,6181 | 222/222 |

**Les 23 correctifs** : 12 anglais (`fast`, `calm`, `dark`, `right` ×2, `absent`, `mean`, `fresh`,
`quiet`, `alone`, `rare`, `hungry`) et 11 français (`calme` ×2, `rapide`, `passionnant`, `ouverte`,
`sombre`, `absent`, `méchant`, `frais`, `seule`, `rare`). **0 cassé** au sens strict : aucun jeton
gold-juste ne devient faux.

**Mais 17 faux→faux** : des jetons déjà faux changent de classe fausse. Anglais : `late` ×2, `out`,
`maybe`, `far`, `mine`, `born`, `hung`. Français : `sorti`, `accroché`, `là`, `venue`, `partie`,
`arrivés`, `rêve`, `observe`, `saute`. C’est le vrai coût sémantique de R4 : le chiffre POS ne le
voit pas, le produit le verrait.

**Le garde `_est_verbe`** réduit les faux→faux de 17 à 9, mais **coûte 1 correctif** (`ouverte`,
participe/adjectif) et **ne protège pas** les participes irréguliers anglais (`born`, `hung`). Il
fait passer le test de +0,71 à +0,61 : rejeté.

**La variante « large »** (avec `feel`, `taste`, `smell`, `grow`, `turn`, `get`, `keep`) **casse
`wheat`** dans `The farmers grow wheat` (r159) : c’est le contrôle négatif de la liste stricte.

### 3.3 Les contrôles : les deux sondes demandées passent, la propriété générale non

| sonde | attendu | base | R4-en | R4 bilingue | verdict |
|---|---|---|---:|---:|---:|---|
| `He is a doctor.` | `doctor` NOUN | NOUN | NOUN | NOUN | ✅ |
| `He is running.` | `running` VERB | VERB | VERB | VERB | ✅ |
| `He is doctor.` | `doctor` NOUN | NOUN | **ADJ** | **ADJ** | ❌ |
| `She is president.` | `president` NOUN | NOUN | **ADJ** | **ADJ** | ❌ |
| `He remains president.` | `president` NOUN | NOUN | **ADJ** | **ADJ** | ❌ |
| `They became members.` | `members` NOUN | NOUN | **ADJ** | **ADJ** | ❌ |
| `The house where I was born is small.` | `born` VERB | NOUN | **ADJ** | **ADJ** | ❌ |
| `The painting is hung on the wall.` | `hung` VERB | NOUN | **ADJ** | **ADJ** | ❌ |
| `She seems calm.` | `calm` ADJ | NOUN | ADJ | ADJ | ✅ |
| `It looks quiet.` | `quiet` ADJ | NOUN | ADJ | ADJ | ✅ |
| `The car is fast.` | `fast` ADJ | NOUN | ADJ | ADJ | ✅ |
| `He feels pain.` | `pain` NOUN | NOUN | NOUN | NOUN | ✅ (liste stricte) |
| `The farmers grow wheat.` | `wheat` NOUN | NOUN | NOUN | NOUN | ✅ (liste stricte) |
| `Il est médecin.` | `médecin` NOUN | NOUN | NOUN | **ADJ** | ❌ (fr) |
| `La réunion est reportée.` | `reportée` VERB | NOUN | NOUN | **ADJ** | ❌ (fr) |
| `Les enfants sont arrivés.` | `arrivés` VERB | NOUN | NOUN | **ADJ** | ❌ (fr) |
| `Elle est calme.` | `calme` ADJ | NOUN | NOUN | ADJ | ✅ (fr) |

**Lecture.** Les deux contrôles demandés passent **par accident de surface** : `a` est un DET,
`running` est VERB par `-ing`. Dès qu’un nom est **nu** (`he is doctor`, `she is president`) ou
qu’un participe irrégulier est tagué NOUN (`born`, `hung`), R4 le convertit. En français, le prédicat
nu (`il est médecin`) et les participes (`reportée`, `arrivés`) sont les cas d’échec. **Ne pas
vendre R4 comme « ne convertit jamais un nom ni un verbe ».**

### 3.4 Les 50 textes libres

| variante | textes touchés | changements POS | transitions | segments | attachements | invariants | revue |
|---|---:|---:|---|---:|---:|---:|---|
| R4-en | 0 | 0 | — | 0 | 0 | 0 | — |
| **R4 bilingue** | **6** | **8** | NOUN→ADJ ×8 | 0 | 0 | 0 | **3 justes / 5 faux** |
| R4 bilingue + classes | 7 | 9 | 8 ADJ + 1 PRON | 0 | 0 | 0 | 3 justes / 6 faux |

Les 8 changements français de R4 :

| id | mot | base → après | contexte | revue |
|---|---|---|---|---|
| f20 | `arrivés` | NOUN → ADJ | « … sont arrivés vers 9 h. » | **faux** (participe passé) |
| f28 | `gratuite` | NOUN → ADJ | « … l’eau est gratuite. » | juste (adjectif attribut) |
| f38 | `parfois` | NOUN → ADJ | « … sont parfois coupées. » | **faux** (adverbe) |
| f43 | `cohérent` | NOUN → ADJ | « … tout reste cohérent … » | juste (adjectif attribut) |
| f49 | `reportée` | NOUN → ADJ | « La réunion est reportée … » | **faux** (participe passé) |
| f50 | `entrés` | NOUN → ADJ | « … trois chats sont entrés … » | **faux** (participe passé) |
| f50 | `ouverte` | NOUN → ADJ | « Une question reste ouverte … » | juste (adjectif attribut) |
| f50 | `acceptés` | NOUN → ADJ | « … sont acceptés dans les notes … » | **faux** (participe passé) |

**R4-en ne change rien** sur les 5 textes anglais du lot : ils ne contiennent pas de copule suivie
d’un mot inconnu. Le lot libre ne **valide** donc pas R4-en ; il montre seulement l’absence de
régression sur ces 5 textes. Les 5 faux français sont, eux, un vrai signal : R4-fr n’est pas
intégrable tel quel.

**Recommandation R4** : intégrer **R4-en** (propre sur les 50 textes libres, +0,41/+0,31) ; garder
R4-fr derrière un garde participe/adverbe (ou un lexique), et ne pas compter son +0,32/+0,41 comme
acquis.

## 4. Classes fermées anglaises — compléter `POS_FERME["en"]`

### 4.1 Le patch

Le patch (bloc exact en **annexe A.2**) :

- **PRON** : ajoute `where`, `whose`, `mine` ;
- **CONJ** : ajoute `as` ;
- **AUX** : ajoute `am` ;
- **ADV** : ajoute `late`, `out`, `maybe`, `hard`, `far`, `again`, `now`, `down`, `outside` ;
- **PREP** : retire `outside` (déplacé en ADV) ;
- **ne touche pas** `when` (reste CONJ) ni `n't` (le tokeniseur ne le produit pas).

`where` est **PRON** dans ce gold (6/6, relatifs « the city where we live »), pas ADV comme le
suggérait la liste indicative. Le mettre en ADV corrigerait **0** jeton et laisserait les 6 erreurs.
`when` en PRON corrigerait 1 `when` relatif mais **casserait 4 `When` conjonctifs** (net **−3**).
`fast` est traité à part (§ 4.4).

### 4.2 Mesure, mot par mot

Chaque ligne est mesurée **seule** (un mot ajouté, ou `outside` déplacé) sur le gold B13 :

| mot | classe | opération | net EN | dev | test | corr. | cassés | exemple |
|---|---|---|---:|---:|---:|---:|---:|---|
| `where` | PRON | ajout | **+6** | +4 | +2 | 6 | 0 | the city **where** we live |
| `late` | ADV | ajout | +4 | +4 | 0 | 4 | 0 | it is **late** |
| `out` | ADV | ajout | +2 | +1 | +1 | 2 | 0 | the film is **out** |
| `maybe` | ADV | ajout | +2 | +1 | +1 | 2 | 0 | she is **maybe** tired |
| `hard` | ADV | ajout | +1 | +1 | 0 | 1 | 0 | the wind blows **hard** |
| `far` | ADV | ajout | +1 | +1 | 0 | 1 | 0 | the place is **far** |
| `again` | ADV | ajout | +1 | +1 | 0 | 1 | 0 | she leaves **again** |
| `now` | ADV | ajout | +1 | 0 | +1 | 1 | 0 | I must leave **now** |
| `down` | ADV | ajout | +1 | 0 | +1 | 1 | 0 | she puts it **down** |
| `outside` | ADV | PREP→ADV | +1 | +1 | 0 | 1 | 0 | the children play **outside** |
| `as` | CONJ | ajout | +2 | +1 | +1 | 2 | 0 | **As** it was raining |
| `am` | AUX | ajout | +1 | +1 | 0 | 1 | 0 | I **am** tired |
| `whose` | PRON | ajout | +1 | 0 | +1 | 1 | 0 | the man **whose** car is red |
| `mine` | PRON | ajout | +1 | +1 | 0 | 1 | 0 | the book is **mine** |
| **total core** | | | **+25** | **+17** | **+8** | **25** | **0** | |
| `fast` | ADV | ajout | +2 | +1 | +1 | 2 | 0 | the car drives **fast** |
| `when` | PRON | CONJ→PRON | **−3** | −3 | 0 | 1 | **4** | When it rains… (cassé) |
| `n't` | ADV | ajout | 0 | 0 | 0 | 0 | 0 | le tokeniseur ne le produit pas |

**Mesure du patch core** : POS **84,62 %**, dev **84,53** (**+0,78**), test **84,81** (**+0,81**),
anglais **93,21 %** (91,03 → 93,21), **25 correctifs / 0 cassé / 0 faux→faux**. F1 **0,6188**
(+0,0007 ; anglais 0,7273 → 0,7295), tête 0,7513, attachement **222/222**.

**D’où vient le F1 ?** D’un seul segment : `The children play outside` (r197) passe de
`GV(13,17) + GP(18,25)` à `GV(13,25)` parce que `outside` n’est plus PREP. C’est le seul gain F1 du
lot ; il ne faut pas le lire comme un gain général de segmentation.

### 4.3 Les ambiguïtés : une liste ne tranche pas le contexte

| sonde | attendu | `cc_core` | verdict |
|---|---|---|---:|
| `The city where we live is beautiful.` | `where` PRON | PRON | ✅ |
| `Where is the nearest station?` | `Where` ADV | **PRON** | ❌ |
| `As it was raining, we stayed.` | `As` CONJ | CONJ | ✅ |
| `He works as a teacher.` | `as` PREP | **CONJ** | ❌ |
| `The train arrives late.` | `late` ADV | ADV | ✅ |
| `The late president arrived.` | `late` ADJ | **ADV** | ❌ |
| `The children play outside.` | `outside` ADV | ADV | ✅ |
| `He plays outside the house.` | `outside` PREP | **ADV** | ❌ |
| `The wind blows hard.` | `hard` ADV | ADV | ✅ |
| `It is hard work.` | `hard` ADJ | **ADV** | ❌ |
| `She puts it down.` | `down` ADV | ADV | ✅ |
| `He walks down the street.` | `down` PREP | **ADV** | ❌ |
| `The car is fast.` | `fast` ADJ | NOUN (core) / **ADV** (`fast`) | core ✅, `fast` ❌ |

Ces six mots (`where`, `as`, `late`, `outside`, `hard`, `down`) sont **contextuels**. La liste
fermée est un choix majoritaire, pas une règle ; les 50 textes libres n’en exercent qu’un
(`Where` interrogatif). Il faut des règles contextuelles pour les six.

### 4.4 Les variantes rejetées

- **`fast` en ADV** : +2 correctifs (les deux `fast` adverbiaux), mais **bloque le ADJ de
  `The car is fast`** quand R4 est présent. Seul : +0,83/+0,91 ; dans le paquet : +1,24/+1,11
  (contre +1,19/+1,11 sans `fast`), et 3 faux→faux au lieu de 2. **Ne pas l’ajouter** tant que
  `fast` n’a pas de règle contextuelle.
- **`when` en PRON** : net **−3** (4 `When` CONJ cassés). **Ne pas l’ajouter.**
- **`n't` en ADV** : **inerte** (0 changement), le tokeniseur ne produit pas `n't` comme le gold.
- **Bloc « large » (90 mots, dont DET)** : POS test 84,71 (**+0,71**, moins que le core), F1 0,6177,
  **attachement 221/221** (perte d’1). Le bisect montre que c’est le **bloc DET** qui perd
  l’attachement et 1 jeton test. **Ne pas compléter en bloc.**

### 4.5 Les 50 textes libres

- `cc_core` : **1 seul changement** — f08 `Where` NOUN→PRON, dans
  « Where is the nearest train station? ». C’est un **faux** : interrogatif, ADV attendu. Le gold
  n’a que des `where` relatifs ; la liste ne peut pas distinguer.
- `cc_sans_where` : **0 changement** sur les 50 textes, mais +0,60/+0,61 seulement (perte des 6
  `where` relatifs).
- `cc_fast` : même 1 changement (`Where`), `fast` n’apparaît pas dans les 5 textes anglais.
- Aucun changement de segment ni d’attachement, aucun invariant cassé, sur les 46 textes mesurables.

## 5. Les paquets : ce que les deux leviers font ensemble

### 5.1 La synergie

Les classes fermées **rattrapent 6 des 17 faux→faux** de R4 bilingue : `late` ×2, `out`, `maybe`,
`far`, `mine` deviennent ADV/PRON corrects, donc R4 ne les convertit plus en ADJ. Il reste **11
faux→faux** : `born`, `hung` (anglais) et 9 français (`sorti`, `accroché`, `là`, `venue`, `partie`,
`arrivés`, `rêve`, `observe`, `saute`). Le paquet sûr (R4-en) n’en laisse que **2** (`born`, `hung`).

### 5.2 Les chiffres

| paquet | POS tout | dev | Δ dev | test | Δ test | corr. / cassés | faux→faux | F1 | att. | fermé | ouvert | anglais | français |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| R4-en + classes | 85,00 | 84,94 | +1,19 | 85,11 | +1,11 | 37 / 0 | 2 | 0,6188 | 222/222 | 92,95 | 77,46 | 94,25 | 79,76 |
| R4-en + classes sans `where` | 84,81 | 84,76 | +1,01 | 84,91 | +0,91 | 31 / 0 | 2 | 0,6188 | 222/222 | 92,56 | 77,46 | 93,73 | 79,76 |
| R4 bilingue + classes | 85,34 | 85,26 | +1,51 | 85,51 | +1,51 | 48 / 0 | 11 | 0,6188 | 222/222 | 92,95 | 78,14 | 94,25 | 80,31 |
| R4 bilingue + classes sans `where` | 85,15 | 85,08 | +1,33 | 85,31 | +1,31 | 42 / 0 | 11 | 0,6188 | 222/222 | 92,56 | 78,14 | 93,73 | 80,31 |
| R4 bilingue + classes + `fast` | 85,37 | 85,31 | +1,56 | 85,51 | +1,51 | 49 / 0 | 12 | 0,6188 | 222/222 | 93,08 | 78,08 | 94,34 | 80,31 |

**Lecture.** Le paquet sûr est **à +1,19/+1,11** avec **2 faux→faux** et **1 faux libre** ; c’est
le point de fonctionnement recommandé. Le paquet max gagne **+0,32 pt au test** mais paie **9
faux→faux français** et **5 faux libres français** : c’est un maximum de POS, pas un paquet
produit. Le `fast` ajoute +0,05 pt dev mais 1 faux→faux de plus : à laisser à une règle
contextuelle.

## 6. Contrôles

### 6.1 Placebo — mêmes actions, positions aléatoires

Pour chaque action réelle (R4 : NOUN→ADJ ; classes : ouvert→fermé), on rejoue **le même nombre**
d’actions de la **même direction** sur des jetons tirés au hasard dans la **même phrase**, 200
tirages par variante (graine 0..199). Le placebo est un changement de POS post-hoc : il contrôle
la métrique POS, pas le chunker.

| levier / paquet | actions | placebo moyen (tout) | min | max | observé dev / test |
|---|---:|---:|---:|---:|---|
| R4-en | 20 | −0,34 pt | −0,44 | −0,25 | **+0,41 / +0,31** |
| R4 bilingue | 40 | −0,80 pt | −0,91 | −0,69 | **+0,74 / +0,71** |
| Classes fermées | 25 | −0,64 pt | −0,72 | −0,57 | **+0,78 / +0,81** |
| Paquet sûr | 37 | −0,96 pt | −1,07 | −0,82 | **+1,19 / +1,11** |
| Paquet max | 65 | −1,42 pt | −1,54 | −1,29 | **+1,51 / +1,51** |

**Dans les cinq cas, le maximum du placebo reste sous le gain observé.** Le gain n’est pas un
effet de nombre ou de direction.

### 6.2 Attachement

- **B13** : 222/222 exact, 239 cibles, couverture 0,9289, top-k 221. **Strictement inchangé** pour
  R4, les classes, le paquet sûr et le paquet max.
- **Exception** : le bloc « large » des classes fermées perd 1 attachement (221/221, couverture
  0,9247) — cause : le bloc DET. C’est le seul perdant du lot.
- **HEAD instantané** : 235/236, couverture 0,9874, top-k 234 ; **inchangé** par les deux leviers.

### 6.3 Les 50 textes libres

- **Base** : 46 textes mesurables (4 refus), **766 POS** ; les comptes POS reproduisent **46/46**
  ceux de l’audit `pensee-fiabilite-produit.json`. Les comptages de syntagmes/attachements
  diffèrent sur 4 textes (386 vs 360 syntagmes, 295 vs 284 attachements) : état de
  `tools/structures`/mode CLI. Les effets sont donc mesurés **en différentiel** base→variante.
- **R4-en** : 0 changement, 0 segment, 0 attachement, 0 invariant.
- **R4 bilingue** : 6 textes, 8 POS, 0 segment, 0 attachement, 0 invariant ; 3 justes / 5 faux.
- **Classes** : 1 texte, 1 POS (`Where`), 0 segment, 0 attachement, 0 invariant ; faux.
- **Paquet sûr** : 1 texte, 1 POS (`Where`), 0 segment, 0 attachement, 0 invariant ; faux.
- **Paquet max** : 7 textes, 9 POS, 0 segment, 0 attachement, 0 invariant ; 3 justes / 6 faux.
- **Sans `where`** : 0 changement pour le paquet sûr, 8 changements (3 justes / 5 faux) pour le
  paquet max.

### 6.4 Reproductibilité du patch exact

Le patch exact (A.1 + A.2), appliqué à une copie `/tmp/pos_r4/bloc_patche.py`
(SHA `0bf4d3eb…`), reproduit **POS 85,34 %** (dev 85,26 / test 85,51), **F1 0,6188**,
**attachement 222/222**, **48 correctifs / 0 cassé** — exactement le paquet max mesuré par
mutation de `POS_FERME`. Les quatre contrôles de chaîne (`COPULES` en/fr, insertion R4, bloc `en`)
sont vrais.

## 7. Ce qui pourrait rendre ces chiffres faux

1. **R4 « 0 cassé » n’est pas « 0 perte ».** 17 jetons déjà faux changent de classe fausse ; 5 des
   8 changements français sur les 50 textes libres sont faux. Le chiffre POS ne voit pas cette
   dérive ; le produit la verrait.
2. **R4 n’a pas de garde nom/verbe.** `He is a doctor` passe par le DET, `He is running` par
   `-ing` ; les noms nus (`he is doctor`, `she is president`, `he remains president`, `they became
   members`) et les participes irréguliers (`born`, `hung`) sont convertis. En français, `il est
   médecin`, `reportée`, `arrivés` aussi.
3. **R4-fr est le point faible** : 3 justes / 5 faux sur les 50 textes libres. Le garde
   `_est_verbe` coûte 1 correctif (`ouverte`) et ne protège pas `born`/`hung` ; il ne suffit pas.
4. **Les classes fermées sont une liste, pas une règle contextuelle.** `where`, `as`, `late`,
   `outside`, `hard`, `down`, `fast` ont au moins deux classes selon le contexte ; la liste choisit
   la majorité du gold. Les 50 textes libres n’exercent que `Where` interrogatif (faux).
5. **Les mots des classes fermées sont choisis sur les erreurs de l’union (C3).** Le split dev/test
   ne protège pas de ce choix : le gain test **n’est pas hors-échantillon**. La cohérence dev/test
   est un contrôle de consistance, pas une preuve de généralisation. Un gold disjoint (ou un
   corpus de fonction words hors gold) serait nécessaire pour trancher.
6. **Le gold est petit et templaté** : le test anglais fait 347 jetons, 1 jeton = 0,29 pt ; les
   mêmes formes reviennent (`where` 6, `late` 4, `fast` 3). Un correctif sur 3 occurrences peut
   disparaître dans un autre tirage.
7. **Les 50 textes libres sont surtout français** (41 fr, 5 en) : R4-en n’y change rien, donc ils
   ne valident pas R4-en ; ils montrent seulement l’absence de régression sur 5 textes anglais.
8. **Le POS de base des 50 textes reproduit 46/46 les comptes de l’audit, mais pas les
   syntagmes/attachements** (4 textes diffèrent). Les effets segments/attachements sont
   différentiels, pas comparés à l’audit.
9. **Le dépôt a bougé pendant la mesure** : le module `bloc_linguistique.py` était modifié en
   parallèle et le gold a été corrigé. La référence B13 est pinnée ; le contrôle HEAD donne les
   mêmes gains POS mais un F1/attachement de base différent.
10. **Le placebo est post-hoc** : il rejoue les changements de POS, pas le chunker. Il contrôle la
    métrique POS ; le F1 n’a pas de placebo propre (mais R4 ne le bouge pas et les classes ne le
    bougent que par un segment identifié).

## 8. Recommandation

1. **Intégrer R4-en + classes fermées (sans `fast`, avec `where`)** : **+1,19 dev / +1,11 test**,
   POS 85,00 %, 37/0, 2 faux→faux, F1 +0,0007, attachement 222/222. C’est le meilleur rapport
   effet/risque ; le seul faux libre connu est `Where` interrogatif, à corriger par une règle
   contextuelle ou à retirer.
2. **Variante zéro régression libre** : R4-en + classes **sans `where`** → **+1,01 / +0,91**,
   31/0, 2 faux→faux, **0 changement** sur les 50 textes. À préférer si le produit ne veut aucun
   changement libre ; on perd 6 `where` relatifs.
3. **Paquet max** : R4 bilingue + classes → **+1,51 / +1,51**, 48/0, mais 11 faux→faux et 5 faux
   français libres. **Ne pas l’intégrer sans garde participe/adverbe** (français) ; c’est un
   plafond de POS, pas un paquet produit.
4. **Ne pas ajouter** `when` en PRON (net −3), `fast` en ADV (bloque le ADJ de `The car is fast`),
   ni le bloc DET/large (perd 1 attachement et 0,10 pt test).
5. **Règles contextuelles de suivi** : `where` (après GN → PRON, sinon ADV), `late`/`hard`/`fast`
   (après copule → ADJ, sinon ADV), `as` (devant GN → PREP, devant clause → CONJ), `outside`
   (devant GN → PREP), `down` (devant GN → PREP). À mesurer sur un gold disjoint.
6. **R4-fr** : ne pas compter son +0,32/+0,41 comme acquis ; le garder derrière un garde
   participe/adverbe, ou le remplacer par une règle « adjectif attribut » avec un lexique
   d’adjectifs français.

## 9. Reproduction

Le dispositif complet tient dans des scripts hors dépôt, dans `/tmp/pos_r4/` :
`harness.py` (copie en mémoire + patches), `run_matrix.py` (matrice), `detail.py`
(correctifs/cassés/faux→faux), `placebo_final.py` (200 tirages), `compute_final.py`,
`compute_aux.py`, `assemble_json.py`. Le patch exact est construit par `build_patch.py` et
appliqué à `/tmp/pos_r4/bloc_patche.py` (SHA `0bf4d3eb…`).

```bash
# référence B13 (module 2ba393b0 + gold B13)
python3 /tmp/pos_r4/run_matrix.py
python3 /tmp/pos_r4/detail.py
python3 /tmp/pos_r4/placebo_final.py
python3 /tmp/pos_r4/compute_final.py
python3 /tmp/pos_r4/compute_aux.py
python3 /tmp/pos_r4/assemble_json.py
```

Aucun fichier du dépôt n’a été modifié par cette session : les deux livrables sont
`reports/rapport-pos-r4.md` et `reports/pensee-pos-r4.json`. Les patches n’ont été appliqués
qu’à des copies `/tmp`.

### Annexe A.1 — R4 (deux insertions)

**A.1.a — `COPULES`, après `ADJECTIFS`, avant `MOTS_DOUBLE_SENS`** (garder `en` seul pour R4-en) :

```python
# Copules : après elles, un mot inconnu est un adjectif attribut (« she is calm », « il est
# rapide »). Liste volontairement stricte : les verbes à objet direct (« feel pain », « grow
# wheat ») n'y sont pas — mesuré : ils convertissent des noms.
COPULES = {
    "fr": set("""est sont était étaient semble semblent semblait semblaient
        paraît paraissent paraissait paraissaient devient deviennent devenait devenaient
        reste restent restait restaient demeure demeurent""".split()),
    "en": set("""is are was were am be been being seem seems seemed seeming
        look looks looked looking appear appears appeared appearing become becomes became becoming
        remain remains remained remaining""".split()),
}
```

**A.1.b — dans `Heuristique.analyser`, après la boucle « 3 a bis » (R2b), avant
`# 4. phrase + pragmatique`** :

```python
        # 3 c. R4 — après une copule, un mot inconnu est un ADJECTIF (« she is calm »).
        _copules = COPULES.get(lg, set())
        if _copules:
            for _k, _i in enumerate(pos_idx):
                _e = etiquettes[_i]
                if _k == 0 or _e.type != "NOUN" or _e.confiance > 0.45:
                    continue
                _av = etiquettes[pos_idx[_k - 1]]
                if _normaliser(_av.valeur) not in _copules:
                    continue
                etiquettes[_i] = Etiquette("pos", "ADJ", _e.valeur, _e.debut, _e.fin, self.nom,
                                           0.5, candidats=["adj"], langue=lg, script=script,
                                           meta={"ouvert": True, "contexte": "copule"})
```

### Annexe A.2 — classes fermées (bloc `"en"` de `POS_FERME`)

Remplacer le bloc `"en"` par :

```python
    "en": {
        "DET": set("the a an this that these those my your his her its our their".split()),
        "PREP": set("of to in on at by with from for about into over under between through during without since above below near behind across along beside beyond despite except inside toward towards until upon within".split()),
        "PRON": set("i you he she it we they me him her us them who whom which that where whose mine".split()),
        "CONJ": set("and or but nor for so yet because although while if when as".split()),
        "AUX": set("is are was were be been being have has had do does did can could will would shall should may might must am".split()),
        "ADV": set("not never very well here yesterday today tomorrow often always already still too late out maybe hard far again now down outside".split()),
        "NUM": set("one two three four five six seven eight nine ten".split()),
    },
```

`outside` est **retiré de PREP** et **ajouté à ADV**. `when` reste CONJ. `n't` n’est pas ajouté
(inerte). `fast` n’est pas ajouté (variante rejetée, § 4.4).

### Annexe A.3 — les sondes de contrôle

Les 30 sondes (nom/verbe, adjectif, ambiguïtés `where`/`as`/`late`/`outside`/`hard`/`down`) sont
dans le JSON, clé `controles`, avec les colonnes `base`, `r4_en`, `r4_bilingue`, `r4_en_large`,
`cc_core`, `cc_fast`, `r4_en+cc_core`, `r4_bilingue+cc_core`. Les jugements y sont `ok` / `ko`.

> **Non intégré.** Ces patches sont des propositions mesurées, pas du code appliqué : la mission
> interdisait de modifier l’existant. Les lignes citées sont celles du snapshot B13 `2ba393b0` ;
> toute évolution de `_pos`, de la boucle 3 bis ou de `POS_FERME` décale les ancres, pas les règles.
