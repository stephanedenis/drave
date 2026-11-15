# R0.7 / B13 — le gold réel étendu : 50 phrases que l'heuristique rate, et ce qu'elles disent

> **Ligne de roadmap** : **R0.7** (le bloc linguistique) / **B13** · **Tâche** : C3 (coordination R) ·
> **Date** : 2026-11-15 · **HEAD mesuré** : `f926b5bc` · **Verdict** : ✅ **le gold réel n'est pas un
> problème de nombre** (452 phrases, déjà > 200) : c'est un problème de **discrimination**. Les
> **50 phrases réelles dures** (2 hand + 48 reel ; 25 fr + 25 en ; les plus coûteuses, à
> diversité plafonnée) portent **37,1 %** des erreurs POS et **25,1 %** des segments absents pour
> **11,1 %** des phrases ; l'heuristique y fait **68,42 %** de POS (étiquettes seules **75,68 %**)
> contre **91,98 %** sur le reste. L'attachement, lui, est **saturé** : **183/184** (une seule
> erreur, `g017`). L'extension utile est donc **un lot dur tenu à l'écart** + **10 cibles GP/SUB à
> annoter** (dont 4 dans le lot), **pas 50 phrases de plus**.

**En trois lignes.** (1) Le « gold 200+ » est **défini** : c'est le gold **linguistique** hand + reel
(452 phrases, 2 480 tokens, 184 cibles d'attachement), pas le gold de pensée ; le libellé « 200+ »
est **obsolète** et ambigu (T15). (2) On sélectionne **50 phrases** par un score déterministe
(3 × attachement + 2 × POS + 1 × segment absent), 25 fr + 25 en, **au plus 2 par signature
d'erreur** : 102/275 erreurs POS (37,1 %), 87/346 segments absents (25,1 %), 1/1 erreur
d'attachement. (3) Mesure : lot dur **68,42 %** POS, **58,36 %** F1, **21/22** attachement ; reste
402 **91,98 %**, **81,90 %**, **162/162** ; 50 aléatoires stratifiées **87,24–90,77 %** POS,
**73,68–83,63 %** F1, **95,0–100 %** attachement. Le lot dur est **hors** des contrôles pour le POS
et la segmentation ; il **ne l'est pas** pour l'attachement.

**Ce que cette fiche est, et n'est pas.**

- **Est** : une **proposition mesurée** d'extension du gold réel — le lot dur H50, la taxonomie de
  ses erreurs **par type**, et les **candidats à annoter** — avec sa fiche, son JSON et son script
  reproductible. Le gold est **lu deux fois** (sha256 avant/après) : **aucun fichier du gold n'est
  modifié** (territoire S/D).
- **N'est pas** : une modification de `gold.json`/`gold_reel.json`, une nouvelle annotation, une
  mesure du tagger neuronal, ni une mesure de généralisation (le lot est sélectionné **sur** les
  erreurs de l'heuristique).
- **Public** : **S** (le gold), **R** (R0.7, le split réel), **B13** (le bloc linguistique).

## 1. L'objet : « gold 200+ » ne veut pas dire 200 phrases

Le libellé « gold 200+ » apparaît **13 fois** dans le pilotage sans définition (T15,
[`rapport-file-taches.md`](rapport-file-taches.md)). Il recouvre deux objets :

| objet | ce que c'est | état |
|---|---|---|
| **gold linguistique** (cette fiche) | `gold.json` 20 hand + `gold_reel.json` 432 reel = **452 phrases**, POS/segments/attachement | **452 > 200** ; le chiffre est déjà atteint |
| **gold de pensée** | les états/étiquettes de B13 (RSN, opérateurs) | autre chantier, non traité ici |

**Définition retenue** : le gold **linguistique réel** (hand + reel), celui que mesurent
`evaluer_gold.py`, le CLI `drave evaluer` et les fiches R/B13. Ce n'est **pas** le gold de pensée.
Le nom « 200+ » peut être retiré : le gold fait **452 phrases**, et son problème n'est plus le
nombre.

| grandeur | valeur | source |
|---|---:|---|
| phrases | **452** (20 hand + 432 reel) | `gold.json`, `gold_reel.json` |
| tokens gold | **2 480** | `mots` |
| segments gold | **1 501** (GN 681, GV 552, GP 81, REL 58, SUB 55, ADJ 35, ADV 30, PONCT 9) | `segments` |
| cibles d'attachement | **184** (GP 72, REL 58, SUB 54) | `cible`/`cibles` |
| POS heuristique | **88,91 %** (2 205/2 480 ; fermé 92,94 %, ouvert 84,66 %) | cette fiche |
| POS hors tokenisation | **91,34 %** (2 205/2 414) | cette fiche |
| F1 syntagmes | **79,06 %** (P 81,28 / R 76,95) | cette fiche |
| attachement | **183/184 = 99,46 %** | cette fiche |

**Le résidu est concentré.** 191 phrases ont au moins une erreur POS, 213 au moins un segment
absent ou en trop, **une seule** une erreur d'attachement. Autrement dit : le gold réel **teste
encore le POS et la segmentation**, mais il ne teste **plus** l'attachement (183/184).

## 2. La règle des 50

**Univers** : les 452 phrases réelles (hand + reel). Aucune phrase n'est ajoutée, aucune n'est
retirée du gold.

**Score par phrase** (déterministe, aucune graine) :

```text
score = 3 × (cible d'attachement absente ou fausse)
      + 2 × (token POS faux)
      + 1 × (segment gold absent au même span)
```

**Sélection** : 25 français + 25 anglais ; **au plus 2 phrases par signature d'erreur** (les POS
confondus, les types de segments absents, les types d'attachement) ; départage par identifiant.
Le plafond empêche une construction de prendre le lot : les **11 négations** (10 françaises
`r408`–`r417` + l'anglaise `r422`) sont ramenées à **4**. Sans le plafond, le top 50 serait
**43 fr / 7 en**, dominé par les négations et les relatives : un lot dur, mais **monoculture**.

| composition | valeur |
|---|---:|
| phrases | **50** |
| sources | **2 hand** (`g004`, `g017`) + **48 reel** |
| langues | **25 fr + 25 en** |
| signatures distinctes | **42** |
| score min / max | **3 / 10** |
| tokens | **323** |
| segments | **190** |
| cibles d'attachement | **22** |

**Robustesse de la règle** (mêmes phrases quand on change les poids) :

| poids att/POS/segment | phrases communes au lot | Jaccard |
|---|---:|---:|
| **3 / 2 / 1** (référence) | **50** | 1,000 |
| 2 / 2 / 1 | **50** | 1,000 |
| 5 / 2 / 1 | **50** | 1,000 |
| 3 / 3 / 1 | 48 | 0,923 |
| 3 / 1 / 1 | 39 | 0,639 |
| 1 / 1 / 1 | 39 | 0,639 |

Le lot est **stable** tant que le POS pèse au moins **2** (et l'attachement **3**) ; il change si
le POS tombe à **1** : c'est le signe que le lot est **piloté par le POS**, pas par le hasard.

## 3. Les erreurs du lot, par type

### 3.1 POS : 102 erreurs, dont 31 de tokenisation

| mesure | global 452 | **lot dur 50** | reste 402 |
|---|---:|---:|---:|
| POS exact | 88,91 % | **68,42 %** | 91,98 % |
| POS hors tokenisation | 91,34 % | **75,68 %** | 93,50 % |
| erreurs POS | 275 | **102** | 173 |
| dont **tokenisation** (`?`) | 66 | **31** | 35 |
| dont **étiquette** | 209 | **71** | 138 |
| fermé / ouvert | 92,94 / 84,66 | 75,42 / 59,72 | 95,80 / 88,04 |

**Ce que « tokenisation » veut dire.** Le gold sépare `j'` + `ai`, `qu'` + `il`, `l'` + `homme`,
`viens` + `tu`, `mange` + `t` + `il` ; l'heuristique garde `j'ai`, `qu'il`, `l'homme`, `viens-tu`,
`mange-t-il`. Le token gold n'a alors **aucun token prédit au même span** : le POS vaut `?` et
compte comme une erreur. Ce n'est **pas** une faute d'étiquette, c'est une **convention de
tokenisation** non tranchée. Les 66 erreurs globales (24 % du total) et les 31 du lot (30 %)
sont dans ce cas : le lot dur est aussi un **test de tokenisation**.

**Confusions POS** (les 10 premières) :

| gold → prédit | global 452 | lot dur 50 | lecture |
|---|---:|---:|---|
| **VERB → NOUN** | **125** | **31** | le verbe lexical n'est pas reconnu (« achetée », « roule », « boit ») |
| PRON → `?` | 30 | 15 | élision (`j'ai`, `qu'il`, `c'est`) : tokenisation |
| VERB → `?` | 16 | 5 | trait d'union (`viens-tu`, `mange-t-il`) : tokenisation |
| PRON → DET | 14 | 8 | `le`/`la` pronom pris pour un déterminant |
| CONJ → `?` | 13 | 8 | `qu'` non séparé : tokenisation |
| **NOUN → ADJ** | **11** | **8** | « table » après préposition étiqueté ADJ |
| ADJ → NOUN | 11 | 1 | « seule », « rouge » pris pour des noms |
| CONJ → PRON | 8 | 1 | `que` relatif vs conjonction |
| ADV → NOUN | 7 | 2 | « demain », « pas » |
| VERB → AUX | 7 | 6 | « est » lexical vs auxiliaire |

Les **trois familles** qui restent : le **verbe lexical** (VERB→NOUN, 45,5 % des erreurs globales),
la **tokenisation** des élisions/traits d'union (24 %), et les **classes ouvertes** (NOUN↔ADJ,
PRON→DET, CONJ→PRON). Le lot dur **sur-représente** la tokenisation (30 % contre 24 %) : c'est un
biais de sélection, nommé au § 7.

### 3.2 Segmentation : 87 segments absents, 60 en trop

| mesure | global 452 | **lot dur 50** | reste 402 |
|---|---:|---:|---:|
| TP / FP / FN | 1 155 / 266 / 346 | **103 / 60 / 87** | 1 052 / 206 / 259 |
| précision | 81,28 % | **63,19 %** | 83,62 % |
| rappel | 76,95 % | **54,21 %** | 80,24 % |
| F1 | **79,06 %** | **58,36 %** | 81,90 % |

**Segments absents (FN) et en trop (FP), par type** :

| type | FN global | FN lot | FP global | FP lot | F1 global | F1 lot |
|---|---:|---:|---:|---:|---:|---:|
| GN | 124 | **28** | 101 | **22** | 83,20 % | 67,11 % |
| GV | 147 | **38** | 125 | **28** | 74,86 % | **45,00 %** |
| GP | 0 | 0 | 25 | 4 | 86,63 % | 75,00 % |
| REL | 0 | 0 | 11 | 5 | 91,34 % | 81,48 % |
| SUB | 1 | 1 | 4 | 1 | 95,58 % | 88,89 % |
| ADJ | 35 | 11 | 0 | 0 | 0 % | 0 % |
| ADV | 30 | 9 | 0 | 0 | 0 % | 0 % |
| PONCT | 9 | 0 | 0 | 0 | 0 % | 0 % |

**Deux constats.**

1. **GP/REL/SUB sont trouvés** (rappel 1,0 ; seul `g017` manque) : leurs erreurs sont des **FP**
   (segments en trop) et des **confusions de type**, pas des spans manquants. Exemple : `r304`
   « Viens-tu demain ? » → `demain` prédit **GP** (gold **ADV**) ; `r255` « La voiture que j'ai
   achetée roule. » → **deux REL** prédites (gold une).
2. **ADJ/ADV/PONCT ne sont jamais produits** (rappel 0) : **74 des 346** segments absents (21,4 %)
   sont **structurels**, pas des erreurs de frontière. Le F1 79,06 % est donc **plombé par une
   fonction manquante** (la segmentation ADJ/ADV/PONCT), pas seulement par des erreurs.

Le lot dur **amplifie** les deux : GV F1 **45,00 %** (le pire des types **produits**), GN
**67,11 %**, et 20 des 87 segments absents sont ADJ/ADV (structurels). Il reste **67 segments
absents réels** (GN 28, GV 38, SUB 1) et **60 FP**.

### 3.3 Attachement par type : 1 erreur, et elle est un span

**C'est le cœur de la demande C3.** Le gold n'a que **184 cibles**, toutes sur **GP, REL, SUB**.

| type | cibles | justes | erreurs | exactitude | erreur |
|---|---:|---:|---:|---:|---|
| **GP** | 72 | 72 | 0 | **1,000** | — |
| **REL** | 58 | 58 | 0 | **1,000** | — |
| **SUB** | 54 | 53 | **1** | **0,9815** | `g017`, `span_absent` |
| **total** | **184** | **183** | **1** | **0,9946** | |

Dans le **lot dur 50** :

| type | cibles | justes | erreurs | exactitude |
|---|---:|---:|---:|---:|
| GP | 2 | 2 | 0 | 1,000 |
| REL | 11 | 11 | 0 | 1,000 |
| SUB | 9 | 8 | **1** | 0,8889 |
| **total** | **22** | **21** | **1** | **0,9545** |

**L'unique erreur** : `g017` « She said that she would come yesterday. » — la cible est **bonne**
(`said`), le span est **faux** : le gold a SUB `that she would come` (9–28), l'heuristique prédit
SUB `that she would come yesterday` (9–38). C'est une **erreur de span**, pas de cible : sur les
**183 segments évaluables**, **183/183** ont la bonne cible. L'attachement est donc **saturé** : le
lot dur **ne le teste pas** (22 cibles, 21 justes ; les 50 aléatoires stratifiées font 95,0–100 %).
**Ajouter des phrases ne le testera pas davantage** : il faut **annoter de nouvelles cibles**
(§ 5).

## 4. La mesure : lot dur, reste, hasard

| mesure | global 452 | **lot dur 50** | reste 402 | hasard stratifié (8 graines) |
|---|---:|---:|---:|---:|
| POS exact | 88,91 % | **68,42 %** | 91,98 % | **87,24–90,77 %** (moy. 89,18) |
| POS hors tokenisation | 91,34 % | **75,68 %** | 93,50 % | **89,40–93,31 %** (moy. 91,37) |
| F1 syntagmes | 79,06 % | **58,36 %** | 81,90 % | **73,68–83,63 %** (moy. 78,61) |
| attachement | 99,46 % | **95,45 %** | **100 %** | **95,0–100 %** (moy. 99,38) |
| phrases | 452 | 50 | 402 | 50 |
| tokens | 2 480 | 323 | 2 157 | 260–296 |

**Part des erreurs** : le lot fait **11,1 %** des phrases et **13,0 %** des tokens, mais il porte
**37,1 %** des erreurs POS (102/275), **25,1 %** des segments absents (87/346) et **100 %** de
l'erreur d'attachement (1/1). C'est un **stress test**, pas un échantillon.

**Écart mesuré, pas projeté** : le lot dur est **23,56 points** sous le reste pour le POS,
**23,54** sous le reste pour la F1, **4,55** sous le reste pour l'attachement (mais ce dernier
n'est que `g017`).

**Contrôles négatifs.**

| contrôle | POS | F1 | attachement |
|---|---:|---:|---:|
| majoritaire (classe la plus fréquente) | **21,98 %** (PRON, lot) · 23,47 % (global) | — | — |
| uniforme (12 classes, graine 0) | **8,36 %** (lot) · 9,56 % (global) | — | — |
| 50 au hasard, 8 graines | 85,00–91,01 % | 76,22–83,85 % | 100 % |
| 50 stratifiées, 8 graines | 87,24–90,77 % | 73,68–83,63 % | 95,0–100 % |
| **lot dur 50** | **68,42 %** | **58,36 %** | **95,45 %** |

Le lot dur est **sous les deux plages** pour le POS et la F1 ; pour l'attachement, il est **dans**
la plage stratifiée (une graine tire `g017`). L'heuristique reste **3,1×** au-dessus du majoritaire
sur le lot (68,42 / 21,98) : le lot n'est pas du bruit.

**Projection (pas une mesure).** Si S ajoutait un **nouveau** lot de 50 phrases du **même profil**
(le gold passerait à 502), les chiffres agrégés deviendraient : POS **86,55 %** (−2,36 pts),
F1 **76,82 %** (−2,24 pts), attachement **204/206 = 99,03 %** (−0,43 pt). C'est une **projection**
sur le profil du lot, pas une mesure : les 50 sont **déjà** dans le gold. La mesure réelle est le
**split** 402/50 (91,98 % contre 68,42 %), pas 452/502.

## 5. Les candidats à annoter

**Principe.** Le gold ne peut pas être étendu par des phrases (elles y sont déjà) ; il peut l'être
par des **cibles d'attachement**. Le gold courant a **0 cible** sur 1 233 GN/GV et **10 segments
GP/SUB sans cible** (9 GP + 1 SUB ; 0 REL). Ce sont eux qui manquent, pas des phrases.

**Le lot lui-même** est le **candidat de première ligne** : les 50 phrases sont déjà dans le gold,
mais elles n'ont **pas de statut de test** et 4 d'entre elles ont un GP sans cible. Le JSON les
liste dans `candidats_a_annoter.phrases_du_lot` ; S peut les **valider** (ou corriger) avant de les
tenir à l'écart.

### 5.1 Priorité 1 — les 10 GP/SUB sans cible (attachement)

| # | id | type | segment | dans le lot dur | phrase |
|---:|---|---|---|---|---|
| 1 | `r267` | GP | `à moi` | non | Le livre qui est sur la table est à moi. |
| 2 | `r324` | GP | `sur la table` | **oui** | Le livre est sur la table ; il est rouge. |
| 3 | `r328` | GP | `on the table` | **oui** | The book is on the table; it is red. |
| 4 | `r336` | GP | `to her` | non | Paul sees Marie; he speaks to her. |
| 5 | `r342` | GP | `to her` | non | Paul sees Marie; he speaks to her; she listens. |
| 6 | `r349` | GP | `sur la table` | **oui** | Le livre est sur la table ; je le lis. |
| 7 | `r358` | GP | `to her` | non | Paul sees Marie; he speaks to her. |
| 8 | `r363` | GP | `on the table` | **oui** | The book is on the table; I read it. |
| 9 | `r367` | GP | `to him` | non | The teacher speaks; the students listen to him. |
| 10 | `r429` | SUB | `que c'est vrai` | non | On dit que c'est vrai. |

**Effet** : le dénominateur d'attachement passe de **184 à 194** (+5,4 %). Les 4 du lot dur sont
exactement la famille **« sur la table » / « on the table »**, l'ambiguïté d'attachement du GP
(au nom `livre` ou au verbe `est` ?) : c'est le cas le plus utile à trancher. La convention est
celle de `gold_reel.py` : **GP → verbe gouverneur, ou nom complété pour un génitif ; SUB → verbe
gouverneur**.

### 5.2 Priorité 2 — les 144 GN/GV du lot dur (argument structure)

| type | sans cible (global) | dont lot dur | effort |
|---|---:|---:|---:|
| GN | 681 | **79** | 79 cibles |
| GV | 552 | **65** | 65 cibles |
| **total** | **1 233** | **144** | **144 cibles** |

C'est un lot **plus lourd** (il double presque les 184 cibles) et **facultatif** : il étend
l'attachement à la structure argumentale (sujet/objet), pas seulement aux GP/REL/SUB. À proposer
comme **deuxième vague**, après la priorité 1.

### 5.3 Non-candidats — ADJ/ADV/PONCT

| type | segments sans cible | dans le lot dur |
|---|---:|---:|
| ADJ | 35 | 11 |
| ADV | 30 | 9 |
| PONCT | 9 | 0 |
| **total** | **74** | **20** |

L'heuristique **ne produit pas** ces types (rappel 0) : les annoter ne testerait pas l'attachement,
mais une **fonction manquante**. Ils restent hors du gold d'attachement tant que la segmentation
ADJ/ADV/PONCT n'est pas une décision de convention (S).

## 6. Le lot, phrase par phrase

`POS` = erreurs de tokens, `FN`/`FP` = segments gold absents / en trop, `att` = erreurs
d'attachement. Les erreurs détaillées (token, gold, prédit) sont dans le JSON
([`rapport-gold-reel-50.json`](rapport-gold-reel-50.json), `erreurs_hard_50.phrases`).

| # | id | src | lg | phrase | POS | FN | FP | att |
|---:|---|---|---|---|---:|---:|---:|---:|
| 1 | `g017` | hand | en | She said that she would come yesterday. | 0 | 1 | 1 | 1 |
| 2 | `r034` | reel | en | The book that I read is exciting. | 2 | 0 | 0 | 0 |
| 3 | `r071` | reel | en | The car drives fast. | 1 | 1 | 1 | 0 |
| 4 | `r076` | reel | en | They arrive tomorrow morning. | 1 | 1 | 1 | 0 |
| 5 | `r102` | reel | en | The rain falls since this morning. | 2 | 0 | 0 | 0 |
| 6 | `r104` | reel | en | We prepare dinner. | 1 | 2 | 1 | 0 |
| 7 | `r106` | reel | en | The children laugh loudly. | 1 | 2 | 1 | 0 |
| 8 | `r119` | reel | en | The tourists visit the museum. | 1 | 3 | 1 | 0 |
| 9 | `r159` | reel | en | The farmers grow wheat. | 1 | 2 | 1 | 0 |
| 10 | `r163` | reel | en | The students review their lessons. | 1 | 3 | 1 | 0 |
| 11 | `r179` | reel | en | The rain washes the streets. | 2 | 3 | 1 | 0 |
| 12 | `r217` | reel | en | The student whom I mention is absent. | 1 | 2 | 1 | 0 |
| 13 | `r241` | reel | en | The day when we left was beautiful. | 1 | 2 | 1 | 0 |
| 14 | `r246` | reel | en | The dog that barks is mean. | 2 | 2 | 1 | 0 |
| 15 | `r285` | reel | en | The table that we took is big. | 1 | 2 | 1 | 0 |
| 16 | `r287` | reel | en | The bird that flies is blue. | 2 | 2 | 1 | 0 |
| 17 | `r291` | reel | en | The book that is on the table is mine. | 2 | 2 | 1 | 0 |
| 18 | `r293` | reel | en | The person whom I mention is here. | 1 | 2 | 1 | 0 |
| 19 | `r328` | reel | en | The book is on the table; it is red. | 2 | 2 | 1 | 0 |
| 20 | `r362` | reel | en | The car is red; it runs fast. | 1 | 2 | 1 | 0 |
| 21 | `r363` | reel | en | The book is on the table; I read it. | 2 | 1 | 1 | 0 |
| 22 | `r366` | reel | en | The rain falls; it wets the ground. | 2 | 0 | 0 | 0 |
| 23 | `r368` | reel | en | Marie and Paul dance; they have fun. | 2 | 1 | 1 | 0 |
| 24 | `r370` | reel | en | The house is old; it still stands. | 1 | 2 | 1 | 0 |
| 25 | `r422` | reel | en | You don't come tomorrow? | 2 | 3 | 1 | 0 |
| 26 | `g004` | hand | fr | Il a couru pour attraper le bus. | 3 | 0 | 0 | 0 |
| 27 | `r091` | reel | fr | Le médecin soigne les malades. | 2 | 3 | 1 | 0 |
| 28 | `r203` | reel | fr | Le livre que j'ai lu est bon. | 3 | 2 | 2 | 0 |
| 29 | `r210` | reel | fr | Bien qu'il soit tard, il travaille. | 3 | 0 | 1 | 0 |
| 30 | `r225` | reel | fr | Je crois qu'il a raison. | 3 | 0 | 0 | 0 |
| 31 | `r227` | reel | fr | Pendant qu'il dort, elle lit. | 3 | 0 | 2 | 0 |
| 32 | `r255` | reel | fr | La voiture que j'ai achetée roule. | 4 | 0 | 1 | 0 |
| 33 | `r260` | reel | fr | Bien qu'il pleuve, il sort. | 3 | 0 | 1 | 0 |
| 34 | `r261` | reel | fr | La table que nous avons prise est grande. | 3 | 2 | 1 | 0 |
| 35 | `r262` | reel | fr | Pendant qu'elle dort, il travaille. | 3 | 0 | 2 | 0 |
| 36 | `r266` | reel | fr | Elle pleure parce qu'elle est seule. | 3 | 0 | 0 | 0 |
| 37 | `r272` | reel | fr | Elle dit qu'elle part. | 3 | 0 | 0 | 0 |
| 38 | `r304` | reel | fr | Viens-tu demain ? | 2 | 3 | 2 | 0 |
| 39 | `r309` | reel | fr | Peut-être qu'il viendra. | 3 | 1 | 2 | 0 |
| 40 | `r324` | reel | fr | Le livre est sur la table ; il est rouge. | 2 | 2 | 1 | 0 |
| 41 | `r331` | reel | fr | Les enfants aiment les fleurs ; ils les cueillent. | 3 | 2 | 2 | 0 |
| 42 | `r339` | reel | fr | Marie lit un livre ; elle le ferme ; elle le pose. | 3 | 4 | 4 | 0 |
| 43 | `r343` | reel | fr | Paul voit Marie ; il lui parle ; elle lui répond. | 1 | 4 | 3 | 0 |
| 44 | `r346` | reel | fr | Le chien poursuit le chat ; il l'attrape. | 2 | 4 | 3 | 0 |
| 45 | `r347` | reel | fr | Sophie regarde Paul ; elle lui sourit. | 1 | 4 | 2 | 0 |
| 46 | `r349` | reel | fr | Le livre est sur la table ; je le lis. | 4 | 2 | 2 | 0 |
| 47 | `r357` | reel | fr | Paul écrit une lettre ; il l'envoie. | 3 | 1 | 2 | 0 |
| 48 | `r408` | reel | fr | Ne viens-tu pas demain ? | 2 | 4 | 2 | 0 |
| 49 | `r409` | reel | fr | Ne mange-t-il pas ? | 3 | 3 | 1 | 0 |
| 50 | `r410` | reel | fr | Ne dort-elle pas ? | 2 | 3 | 1 | 0 |

## 7. Ce que cette fiche ne dit pas

- **Pas de généralisation.** Le lot est sélectionné **sur** les erreurs de l'heuristique : il est
  circulaire par construction. Il mesure ce que l'heuristique **rate déjà**, pas ce qu'elle ratera
  sur un texte neuf.
- **Pas le tagger.** La mesure du tagger (R0.7) n'est pas refaite ici. La décision « intégrer »
  garde son split réel ; le lot dur est le **prochain** test du tagger, pas sa preuve.
- **Pas une annotation.** Le gold n'est pas modifié ; les 10 GP/SUB et les 144 GN/GV sont des
  **candidats** proposés à S, pas des cibles écrites.
- **Pas le gold de pensée.** Le « gold 200+ » de B13 (RSN/opérateurs) est un autre objet.
- **Pas un échantillon représentatif.** 2 hand (in-sample) + 48 reel ; 25 fr + 25 en ; 42
  signatures. Le lot est un **stress test** équilibré, pas un tirage.
- **Pas une faute d'étiquette.** Les 66 `?` globaux (31 dans le lot) sont une **convention non
  tranchée** (élision/trait d'union), pas une faute d'étiquette : le POS « hors tokenisation »
  (91,34 % global, 75,68 % lot) est le chiffre d'étiquetage.

## 8. Ce qui pourrait rendre ce résultat faux

- **Le gold.** Une étiquette fausse sur les 50 (POS, segment, cible) change le score, donc la
  sélection et les taux. Les 20 hand ont servi à dessiner les règles : les 2 hand du lot sont
  **in-sample**.
- **L'heuristique.** Une règle modifiée après le 2026-11-15 change le score, donc le lot. Le
  HEAD mesuré est `f926b5bc` ; le JSON porte le commit et le sha256 des deux fichiers gold.
- **La tokenisation.** Les 31 `?` du lot sur-représentent les élisions/traits d'union ; un
  tokeniseur qui les sépare ferait monter le POS du lot sans changer les étiquettes.
- **La sélection.** Le plafond de 2 par signature est un choix : sans lui, le lot serait 43 fr /
  7 en et dominé par les négations. La sensibilité (3/1/1 → 39/50) montre que le lot dépend du
  poids du POS.
- **L'attachement.** 184 cibles, **une** erreur : le taux 99,46 % a une barre de confiance énorme
  (1 erreur = 0,54 pt). Les 22 cibles du lot ne testent que `g017` ; les 10 candidats n'ont pas
  encore de vérité.
- **Le hasard.** Les contrôles sont à **8 graines**, pas exhaustifs : une autre graine peut sortir
  de la plage (l'attachement stratifié va de 95,0 à 100 % à cause de `g017`).
- **La convention d'attachement.** GP « verbe ou nom », SUB « verbe gouverneur », REL
  « antécédent » : une autre convention change les cibles et les taux.

## 9. La décision et la suite

**Décision proposée à S et à R** (le gold est à S ; cette fiche ne l'écrit pas) :

1. **Retirer le libellé « gold 200+ »** : le gold réel fait 452 phrases ; le nom est obsolète et
   ambigu (T15). Le remplacer par **« gold réel 452 »** + **« lot dur H50 »** + **« cibles 184 »**.
2. **Tenir H50 à l'écart** comme **test dur** (50 phrases, 323 tokens) : les mesures R/B13 ne
   doivent plus être **toutes** in-sample. Le split 402/50 donne 91,98 % contre 68,42 % : c'est la
   mesure qui manquait.
3. **Annoter la priorité 1** (10 GP/SUB, dont 4 dans H50) : le dénominateur d'attachement passe de
   184 à 194, et la famille « sur la table » est tranchée. C'est le seul levier qui étend
   réellement l'attachement.
4. **Ne pas ajouter ADJ/ADV/PONCT** au gold d'attachement tant que la segmentation de ces types
   n'est pas une décision de convention.
5. **Prochaine mesure** : le **tagger** sur H50 (cache chaud, puis API), et une règle qui doit
   améliorer H50 **sans** dégrader le reste 402. Une règle qui ne gagne que sur H50 est du
   sur-apprentissage ; c'est le contrôle négatif qui manque encore.

**Ce que l'extension n'est pas** : 50 phrases de plus. Les 50 sont **déjà** dans le gold ; ce qui
manque, c'est leur **statut de test** et **10 cibles** — ou **154** si S accepte aussi la priorité 2
(le dénominateur passerait alors de 184 à **338**).

## 10. Fichiers

- **Cette fiche** : [`reports/rapport-gold-reel-50.md`](rapport-gold-reel-50.md).
- **JSON** : [`reports/rapport-gold-reel-50.json`](rapport-gold-reel-50.json) — 452 phrases
  analysées, 50 sélectionnées, erreurs par type, candidats, contrôles, sha256 du gold.
- **Script** : [`tools/tests/linguistique/gold_reel_50.py`](../tools/tests/linguistique/gold_reel_50.py)
  — lecture seule, `--sortie`, aucune graine pour la sélection.
- **Lus, non modifiés** : `tools/tests/linguistique/gold.json` (sha256
  `3663be6c…`), `tools/tests/linguistique/gold_reel.json` (sha256 `05d4f6df…`),
  `tools/bloc_linguistique.py`.
- **Reproduire** :

```bash
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet
python3 tools/tests/linguistique/gold_reel_50.py \
  --sortie reports/rapport-gold-reel-50.json
# attendu : phrases 452, selection 50, global 0.8891, hard 0.6842,
#           reste 0.9198, hard_f1 0.5836, hard_att 0.9545, gold_intact true
```

- **Commit (session principale)** : la fiche, le JSON et le script ; `git add` explicite. Le gold
  **n'est pas** indexé (aucun fichier du gold n'est modifié) ; `en-cours`, `INDEX` et `README`
  restent à mettre à jour par la session qui clôt C3.
