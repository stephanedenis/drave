# B13 — audit du gold anglais : 25 phrases à corriger, 60/94 spans perdus, et la segmentation est la cause

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ⚠️ gold
> utilisable ; l'échec anglais est la **segmentation**, pas le gold.
> **Snapshot** : HEAD `dcf7bc91` (v3) mesuré, revérifié à `8281d51e` ; `bloc_linguistique.py` SHA
> `64b7c520…` puis `9544f173…`, chiffres **identiques** ; `gold_reel.json` SHA `05d4f6df…`.
> **Dispositif** : [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py) et
> [`gold_reel.json`](../tools/tests/linguistique/gold_reel.json) (432 phrases réelles : 228 fr, 204 en),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) (`charger`, `evaluer_bloc`),
> [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`Heuristique()`), comparaison des cibles à
> `_est_verbe` et au POS gold.
> **JSON** : [`pensee-gold-anglais.json`](pensee-gold-anglais.json).

## 1. Verdict

Le gold anglais **n'est pas la cause principale** des échecs d'attachement anglais.

- **Structurellement, il est sain** : 0 span qui ne correspond pas au texte, 0 chevauchement, 0 borne
  non alignée sur un token, 0 cible absente ou non-token, 0 cible dans son propre segment, 0 GN qui
  avale un verbe, 0 SUB dont la cible n'est pas un VERB. Les 97 cibles anglaises sont **97 tokens
  exacts** (0 multi-mots, 0 lemme).
- **25 phrases anglaises sur 210 (11,9 %)** portent au moins une anomalie, mais seulement **16 (7,6 %)**
  sur les couches effectivement mesurées (POS dure, cibles, rôles, pragmatique, grammaticalité). Le
  reste est une convention (`that`) ou de la coref non évaluée.
- **60 des 94 spans perdus sont anglais (63,8 %)**, alors que l'anglais ne pèse que 88/239 segments à
  cible (36,8 %). Mais ces 60 échecs sont **des spans**, pas des cibles : sur les 28 segments anglais
  trouvés au bon span (tous des GP), l'attachement exact est **28/28**. Les 54 cibles REL/SUB anglaises
  ne sont jamais évaluées parce que **S ne produit aucun REL/SUB en anglais**.
- **La cause est côté analyseur** : S rend 277 GV anglais (dont 147 couvrent toute la phrase), **0 GN,
  0 GP, 0 REL, 0 SUB**, et 2 spans exacts sur 702. `_pos` tague 176 occurrences de VERB gold en NOUN
  (`talks` → NOUN, `brother` → VERB), alors que le gold est juste.
- **Priorité** : segmenter l'anglais (S language-aware ou chunker anglais), puis corriger `_pos`, puis
  l'hygiène du gold (7 tags POS durs, 4 cibles après verbe, rôles, phrases non grammaticales).

## 2. Le gold réel est structurellement propre

Contrôles d'intégrité sur le **gold réel** (fr 228, en 204) ; le gold anglais complet ajoute 6 phrases
`hand` (5 chaînes de cibles) sans anomalie structurelle.

| contrôle | fr réel | en réel |
|---|---:|---:|
| phrases | 228 | 204 |
| tokens | 1 258 | 1 117 |
| segments | 759 | 686 |
| segments à cible | 86 | 85 |
| chaînes de cibles | 93 | 92 |
| mots dont le span ne correspond pas au texte | 0 | 0 |
| segments dont le span ne correspond pas au texte | 0 | 0 |
| chevauchements de segments | 0 | 0 |
| bornes non alignées sur un token | 0 | 0 |
| cibles absentes du texte | 0 | 0 |
| cibles non-token | 0 | 0 |
| cible dans son propre segment | 1 (`r309`) | 0 |
| REL dont la cible n'est pas la tête du GN à gauche | 0 | 0 |
| SUB dont la cible n'est pas un VERB | 0 | 0 |
| GP dont la cible n'est gouvernée par aucun GV/GN | 0 | 0 (1 cible ADJ, `r038`) |
| GN contenant un VERB/AUX | 0 | 0 |
| tags POS divergents (même forme, même fonction) | 7 (`est`×4, `que`×3) | 10 (7 durs + 3 `that`) |
| cibles GP/SUB manquantes | 4 (3 GP après copule, 1 SUB `r429`) | 6 (4 après verbe, 2 après copule) |
| doublons exacts | 2 (`r019`/`r186`, `r051`/`r189`) | 1 (`r336`/`r358`) |
| tokens hors segment | 40 dans 36 phrases | 23 dans 20 phrases |
| phrases avec PONCT tokenisée | 22/228 | 3/204 |

**Ce que ça dit** : les spans, les têtes et les cibles sont **cohérents** ; les problèmes sont locaux
(POS, cibles manquantes, rôles, conventions de bloc). Le contrôle « un GN avale un verbe » est **vide
dans le gold** ; il est en revanche très présent dans la **sortie de l'analyseur** (le chunker produit
des GN de phrase entière, par exemple `The dog eats an apple`).

## 3. Mesures par langue (`Heuristique()`, HEAD `dcf7bc91`)

| mesure | fr 402 | en 210 | fr réel 228 | en réel 204 |
|---|---:|---:|---:|---:|
| POS exacte | 0,7518 | 0,7343 | 0,7591 | 0,7278 |
| POS fermé | 0,8956 | 0,9031 | 0,8779 | 0,9018 |
| POS ouvert | 0,6235 | **0,5571** | 0,6334 | **0,5466** |
| F1 syntagmes | 0,3786 | **0,1210** | 0,3654 | **0,1206** |
| F1 tête | 0,5822 | 0,3614 | 0,5344 | 0,3618 |
| couverture attachement | 0,7748 | **0,3182** | 0,9070 | **0,3176** |
| exact global | 0,7483 | 0,3182 | 0,8953 | 0,3176 |
| exact sur span | 0,9658 | **1,0000** | 0,9872 | **1,0000** |
| top-k sur span | 0,9744 | 1,0000 | 0,9872 | 1,0000 |
| spans perdus | 34/151 | **60/88** | 8/86 | **58/85** |

Lecture : l'écart fr/en est de **−45,7 points de couverture** (plein) et **−58,9 points** (réel seul),
alors que l'exactitude sur les spans trouvés est **meilleure** en anglais (1,0 contre 0,9658). C'est la
signature d'un problème de **production de spans**, pas de choix de cible. IC 95 % Wilson : couverture
en `[23,0 ; 42,1]`, fr `[70,2 ; 83,4]` ; en réel `[22,8 ; 42,3]`, fr réel `[82,7 ; 95,2]`.

### 3.1 Les 94 spans, par type et par catégorie

| type | fr cibles | fr perdus | en cibles | en perdus | total perdus |
|---|---:|---:|---:|---:|---:|
| REL | 46 | 20 | 28 | **28** | **48** |
| SUB | 43 | 7 | 26 | **26** | **33** |
| GP | 62 | 7 | 34 | 6 | 13 |
| **total** | **151** | **34** | **88** | **60** | **94** |

| catégorie | fr | en | total |
|---|---:|---:|---:|
| aucun segment du même type | 6 | **59** | 65 |
| plus large | 24 | 0 | 24 |
| plus étroit | 3 | 1 | 4 |
| coupé | 1 | 0 | 1 |

En réel seul, le français ne perd que **8/86** spans (1 aucun, 3 plus larges, 3 plus étroits, 1 coupé),
l'anglais **58/85** (57 aucun, 1 plus étroit). Les 26 spans français « synthétiques » expliquent
l'essentiel de l'écart entre 0,907 (réel) et 0,775 (plein) ; le taux anglais, lui, ne bouge pas.

**Ce que ça dit** : les échecs anglais sont presque tous des **« aucun »** — REL et SUB ne sont pas
produits du tout. Les échecs français sont surtout des **« plus large »** — les REL françaises existent
mais débordent. Ce ne sont pas les mêmes correctifs : production pour l'anglais, bornage pour le
français.

## 4. Les annotations suspectes

### 4.1 POS : 10 tags divergents, dont 7 erreurs probables et 3 dus à la convention `that`

| IDs | token | gold | attendu | classe | raison |
|---|---|---|---|---|---|
| `r034`, `r074`, `r114` | that | CONJ | PRON | convention | relatives : 11 `that`/PRON dans les blocs récents ; les 8 complétives sont CONJ |
| `r291`, `r328`, `r363` | is | VERB | AUX | erreur | 43 `is`/AUX ; `r291` et `r328` ont aussi un `is`/AUX dans la même phrase |
| `r422` | do | VERB | AUX | erreur | `do`/AUX en `r029`/`r314` ; le GV de `r422` exclut `do` |
| `r218`, `r313` | late | ADV | ADJ | erreur | attribut du sujet ; `late`/ADV est correct en `r199`/`r365` (adverbial) |
| `r250` | far | ADV | ADJ | erreur | attribut du sujet (`is far`) |

Le gold est ici **plus fiable que l'analyseur** : dans le gold, `talks` est VERB (`r025`, `r035`,
`r064`) et `brother` est NOUN (`r025`) ; `_pos` rend l'inverse (`talks` → NOUN, `brother` → VERB). Le
commentaire de `bloc_linguistique.py` sur « talks » NOUN et « brother » VERB décrit donc **l'analyseur**,
pas le gold.

### 4.2 Cibles et rôles

| IDs | segment | constat | attendu | classe |
|---|---|---|---|---|
| `r336`, `r342`, `r358`, `r367` | GP `to her` / `to him` | cible absente | `speaks` / `listen` | omission (4) |
| `r328`, `r363` | GP `on the table` | cible absente après copule | aucune (convention) | trou de convention (2) |
| `r165` | GN `noon` | rôle `patient` | `temps` | faux |
| `r239` | REL `whose car is red` | rôle `objet` | `possessif` | faux |
| `r180` | GP `to the library` | rôle `destinataire` | `possesseur/thème` | discutable |
| `r247` | phrase | `must` sans `modalite=true` | `modalite=true` | omission |
| `r038` (et `g020`) | GP `to eat` | cible ADJ `ready` | hors convention verbe/nom | convention |
| 9 segments GP | multi-cibles | verbe + nom (ex. `play`, `children`) | l'exact ne lit que la 1re | convention |

Les 6 GP sans cible sont **6 segments sur 6 phrases** : 4 après un verbe lexical (`r336`, `r342`,
`r358`, `r367`), 2 après la copule (`r328`, `r363`). `r336` et `r358` sont le même texte. Les 3
omissions après verbe (`r336`, `r342`, `r358`) cachent une **erreur de l'analyseur** (cible `her` au
lieu de `speaks`) ; `r367` est juste (`listen`). Compléter ces cibles ferait **baisser** l'exact mesuré
(0,3182 → 0,3085) : le gold ne masque pas un gain, il masque trois erreurs et un succès.

### 4.3 Données et conventions

| IDs / périmètre | constat |
|---|---|
| `r028`, `r102`, `r165` | phrases non grammaticales (`It rains since yesterday.`, `The rain falls since this morning.`, `The bell rings noon.`) |
| `r336` = `r358` | doublon exact ; la coref diffère (`her` seul contre `he` + `her`) |
| 20 phrases | 23 tokens hors segment : 10 PRON (`it`×9, `them`), 7 ADV, 3 CONJ, 1 AUX (`Do`), 1 NOUN (`morning`), 1 VERB (`do`) |
| `r422`, `r427`, `r432` | 3/204 phrases avec PONCT ; 201 sans ; `r422` a le token mais pas le segment |
| `r291` | le REL `that is on the table` contient un GP `on the table` non annoté (annotation plate) |
| `r340` | le GN contient des virgules non tokenisées |
| 44 phrases | coref ; 6 suspectes (voir 4.4) |

Les conventions changent avec les **blocs d'annotation**, pas au hasard :

| convention | blocs anciens | blocs récents | exemples |
|---|---|---|---|
| relative `that` | CONJ (3) | PRON (11) | `r034`/`r074`/`r114` vs `r214`+ |
| rôle REL | `qualité` (6) | `sujet`/`objet`/`lieu`/`temps` (22) | `r034`–`r115` vs `r204`+ |
| copule | GV fusionné (14) | GV `is` + ADJ `attribut` (24) | `r032` `is fast` vs `r214` `is` + `good` |
| adverbes | dans le GV (10), ADV (8), omis (7) | — | `r197` `play outside`, `r314` `tomorrow`, `r069` `deeply` |
| négation | dans le GV (2) | ADV séparé (1) | `r029`/`r316` vs `r422` |
| ponctuation | non tokenisée (201) | PONCT (3) | `r422`/`r427`/`r432` |
| sujet de copule | agent 12 / patient 28 | pas de règle unique | `r032` agent vs `r291` patient ; `r328` « The book » patient mais « it » agent |

Ce n'est pas une incohérence de spans : les têtes restent justes. C'est une **non-uniformité de
conventions**, qui rend les rôles et les découpages non comparables d'un bloc à l'autre. Une mesure de
rôles ou de POS par bloc serait faussée si elle ne versionne pas la convention.

### 4.4 Coref (hors mesure actuelle)

`evaluer_gold` n'évalue pas la coref ; les 44 phrases annotées sont donc hors du chiffre. Six cas sont
suspects : `r340` (`they` → `mouse`, alors que le sujet coordonné est « chat, chien, souris »), `r368`
(`they` → `paul` au lieu de « Marie et Paul »), et les collisions de clé `r333`/`r341`/`r361` (deux
`it` ne peuvent pas avoir deux référents dans un dict indexé par la chaîne). `r336`/`r358` est le
doublon à coref différente. Une clé par **span** est nécessaire, pas par forme de surface.

### 4.5 Combien d'annotations suspectes ?

| périmètre | phrases | % de 210 |
|---|---:|---:|
| POS seuls (10 tags) | 10 | 4,8 % |
| couches mesurées : 7 POS durs + 4 cibles après verbe + 2 rôles faux + 1 modalité + 2 non grammaticales | **16** | **7,6 %** |
| + convention `that` | 19 | 9,0 % |
| + coref | 24 | 11,4 % |
| + rôle discutable `r180` | **25** | **11,9 %** |

La liste des 25 : `r028`, `r034`, `r074`, `r102`, `r114`, `r165`, `r180`, `r218`, `r239`, `r247`,
`r250`, `r291`, `r313`, `r328`, `r333`, `r336`, `r340`, `r341`, `r342`, `r358`, `r361`, `r363`,
`r367`, `r368`, `r422`. Le chiffre dépend du périmètre ; les cinq lignes du tableau donnent la règle.

## 5. Les cibles anglaises sont des têtes réduites ; le POS gold est fiable

| | en réel | en complet |
|---|---:|---:|
| chaînes de cibles | 92 | 97 |
| tokens exacts | **92 (100 %)** | **97 (100 %)** |
| multi-mots / lemmes | 0 / 0 | 0 / 0 |
| formes uniques | 67 | 70 |
| POS gold des cibles | 56 VERB / 35 NOUN / 1 ADJ | 58 VERB / 37 NOUN / 2 ADJ |
| accord `_est_verbe` | 76/92 (82,6 %) | 81/97 (83,5 %) |
| rappel verbes | 41/56 (73,2 %) | 43/58 (74,1 %) |
| précision verbes | 41/42 (97,6 %) | 43/44 (97,7 %) |
| faux négatifs | 15 (12 formes) | 15 |
| faux positif | `flower` | `flower` |

Les cibles sont des **formes de surface réduites**, pas des textes complets : `saw` (pas `see`), `talks`
(pas `talk`), `book` (pas `The book`), `ready` pour le seul cas adjectival. **Aucune** cible n'est un
lemme, un multi-mot ou un span complet. Toute mesure future doit donc matcher la **surface**, pas un
lemme.

Le POS gold des cibles est **97/97 correct** à la lecture grammaticale ; `_est_verbe` n'est d'accord
que sur 81/97. Les 15 faux négatifs sont `rains`, `falls`, `hung`, `eat`, `think`, `stay`, `believe`,
`cries`, `call`, `stayed`, `goes`, `continue` (12 formes, 15 occurrences) ; le faux positif est
`flower` (`flow` + `-er`). Le lexique de `_est_verbe` est donc **moins fiable que le gold** : garder le
POS gold comme référence pour le split verbe/nom, et ne pas remplacer le gold par `_est_verbe`.

L'analyseur, lui, tague seulement **17/58** des verbes-cibles anglais en VERB (41 en NOUN). Le faible
score POS anglais est donc **côté analyseur** : `_pos` utilise `VERBES["en"]` (petit) et des suffixes
`-er/-ir/-ing/-ed` qui transforment `teacher`, `letter`, `morning`, `river` en VERB, tandis que
`talks`, `sings`, `writes` restent NOUN. Une simulation de `_pos` consultant `VERBES_CONNUS` avec une
petite liste d'exclusion (`a`, `as`, `bus`, `flower`, `leaves`, `open`) fait passer le POS anglais de
**0,7343 à 0,8031 (+6,9 pts)** et l'ouvert de **0,5571 à 0,6982 (+14,1 pts)**, sans changer
l'attachement. C'est une **borne haute** (liste ajustée sur les faux positifs du gold), pas une règle à
intégrer telle quelle.

## 6. Pourquoi l'anglais échoue (hors gold)

| | en | fr |
|---|---:|---:|
| segments produits par S | **277 GV** (dont 147 couvrent toute la phrase) | 824 : GN 315, GV 342, GP 78, SUB 38, REL 51 |
| spans S exacts / gold | **2/702 (0,28 %)** | 410/1161 (35,3 %) |
| REL/SUB produits par S | **0** | **89** (38 SUB + 51 REL) |
| types prédits (S + union) | GV 323, GN 164, GP 34 ; **0 REL/SUB**, 0 ADJ/ADV/PONCT | GN 473, GV 361, GP 88, SUB 38, REL 66 |
| types gold | GN 321, GV 259, GP 40, REL 28, SUB 26, ADJ 18, ADV 8, PONCT 2 | GN 507, GV 453, GP 65, REL 46, SUB 44, ADJ 17, ADV 22, PONCT 7 |

Les 2 seuls spans S exacts en anglais sont `r032` `is fast` et `r245` `call me` — deux GV gold qui
incluent le complément, par hasard. S traite chaque proposition anglaise comme **un seul GV** : il ne
peut donc pas produire les 28 REL et 26 SUB du gold, ni même les GN/GP. Le chunker d'union fournit des
GP (28 spans exacts) et le GV de phrase de S fournit la cible du GP (d'où l'exact 28/28 sur ces 28
labels) ; il ne fournit **aucun** REL/SUB.

Conséquence : **54 des 88 cibles anglaises (61,4 %) sont dans des REL/SUB**, donc jamais évaluées. La
couverture anglaise plafonne à 0,318 même si la règle de cible est bonne. Le contrôle
`Heuristique(segmenter_s=False)` le confirme : la couverture reste 0,3182 (le chunker trouve les GP),
mais l'exact sur span tombe à **0** (plus de GV lexical pour fournir la cible). S est donc nécessaire
aux cibles, mais **inopérant pour les spans anglais**.

## 7. Contrôles

| contrôle | en | fr | lecture |
|---|---:|---:|---|
| hasard de cible (`evaluer_gold`, sous-chaîne) | 3,41 % | 0,66 % | l'analyseur est au-dessus du hasard |
| permutation des cibles sur les labels (1 000 tirages) | 4,25 % (0–17,9) | 4,64 % (0–12,8) | idem ; les 28 exacts anglais ne sont pas du hasard |
| POS majoritaire (toujours VERB) | 23,43 % | 25,75 % | l'analyseur fait mieux, mais l'écart fr/en reste |
| POS gold corrigé (10 tags en, 7 fr) | 0,7369 (+0,26) | 0,7548 (+0,30) | le bruit du gold n'explique pas l'écart ouvert de 6,6 pts |
| retrait des 5 phrases anglaises annotées (`r028`, `r102`, `r165`, `r336`, `r358`) | POS 0,7384 ; F1 0,1209 ; couv. 0,3256 ; exact 0,3256 | — | +0,74 pt, pas +45 |
| ajout des 6 cibles manquantes anglaises | couv. 32/94 = 0,3404 ; exact 29/94 = 0,3085 | — | corriger le gold **baisse** l'exact : 3 erreurs d'analyseur masquées |
| exact-any (toutes les cibles du segment) | 28/28 | 115/117 (+2 : `s108`, `s122`) | la convention « 1re cible » pénalise 2 cas français |
| `segmenter_s=False` | couv. 0,3182 ; exact span 0 | couv. 0,3245 ; exact span 0 | S fournit les cibles, pas les spans |
| `_pos` patch `VERBES_CONNUS` (simulation) | 0,8031 (+6,9) | 0,7760 (+2,4) | l'écart POS est côté analyseur ; attachement inchangé |
| IC 95 % Wilson, couverture | [23,0 ; 42,1] | [70,2 ; 83,4] | l'écart fr/en est hors IC |

**Contrôle négatif principal** : la permutation des cibles sur les labels donne ~4 %, très loin des
28/28 anglais et des 113/117 français. Les exacts observés ne sont pas un artefact de fréquence. Mais
ce contrôle porte sur les **labels trouvés** : il ne dit rien des 60 spans anglais manquants, qui sont
le vrai problème.

## 8. Ce que ce banc ne dit pas

- **Les 54 cibles REL/SUB anglaises** ne sont pas évaluées : aucun span anglais REL/SUB n'est produit.
  La règle de cible REL/SUB n'est donc testée que par sa cohérence interne au gold (0 tête fausse,
  0 SUB non-VERB), pas par une prédiction.
- **Les rôles et la coref** ne sont pas des métriques : les 3 rôles et les 6 coref sont des lectures
  manuelles, pas un accord inter-annotateur.
- **Les segments imbriqués** ne sont pas annotés : `r291` (GP dans REL) est une limite de l'annotation
  plate, pas un span faux.
- **Le gold `hand` anglais** ne pèse que 6 phrases (5 chaînes de cibles) ; il ne change pas les
  conclusions, mais il ne permet pas de généraliser.
- **Aucun segmenteur anglais** n'est testé : on mesure l'absence, pas la qualité d'une solution. La
  borne haute de couverture si les spans étaient produits n'est pas connue.

## 9. Ce qui pourrait rendre cette fiche fausse

- **Le snapshot bouge** : les chiffres sont identiques à `dcf7bc91` et `8281d51e`, mais un futur
  segmenteur anglais, un lexique ou une règle de cible peuvent les changer. Le JSON porte les SHA.
- **Les jugements manuels** (`that`, `sick`, `out`, `front`, `r180`, les coref) peuvent être contestés :
  un second annotateur pourrait classer `that` en convention plutôt qu'en erreur, ou `to the library`
  en destinataire acceptable.
- **`_est_verbe` dépend du lexique** : les 15 faux négatifs et le faux positif `flower` sont des
  mesures du lexique courant, pas une propriété du gold.
- **La simulation `_pos`** utilise une liste d'exclusion ajustée sur les faux positifs du gold : c'est
  une borne haute, pas un résultat intégré.
- **L'ajout des cibles manquantes** suppose la convention « GP → verbe lexical » ; une autre convention
  (pas de cible après copule, cible = AUX) changerait le dénominateur.
- **Les IC sont larges** (28 labels anglais) et aucun test de signification n'est conduit ; l'écart
  fr/en est assez grand pour être robuste, mais les taux anglais fins ne le sont pas.
- **Le plein inclut le français synthétique** (160 phrases) : c'est pourquoi le tableau donne aussi le
  réel seul. Le taux français plein (0,775) n'est pas comparable au taux anglais plein (0,318) sans
  cette réserve ; le réel seul (0,907 vs 0,318) est la comparaison honnête.
- **La v2 est périmée** : le dépôt est passé à la v3 (`137/145` → `141/145`) pendant l'audit ;
  l'anglais est inchangé. Utiliser la v3 pour l'attachement.

## 10. Recommandation

1. **Segmenter l'anglais d'abord.** C'est le seul levier des 60 spans perdus : rendre S language-aware
   (passer `langue` à `_syntagmes_s` et produire la grammaire anglaise) ou ajouter un chunker anglais
   qui produise GN/GV/GP/**REL/SUB**. Les cibles REL/SUB sont déjà cohérentes dans le gold ; c'est la
   production des spans qui manque. Ne pas réécrire le gold pour compenser.
2. **Corriger `_pos` ensuite** (couche POS, pas attachement) : consulter `VERBES_CONNUS` avec une règle
   de contexte, pas une liste ajustée au gold ; traiter `that`/`her` selon le contexte, ajouter `am`
   aux AUX, et remplacer les suffixes `-er/-ir/-ing/-ed` par un lexique ou un modèle. Simulation :
   +6,9 pts POS, +14,1 pts ouvert, attachement inchangé.
3. **Hygiène du gold** (bon marché, gain faible) : 7 tags durs (`is`×3, `do`, `late`×2, `far`) ;
   normaliser `that` (3 CONJ → PRON) ou versionner ; ajouter les 4 cibles GP après verbe (`r336`,
   `r342`, `r358` → `speaks` ; `r367` → `listen`) et trancher les 2 GP de copule ; corriger les rôles
   `r165`, `r239`, `r180` et la modalité `r247` ; remplacer `r028`, `r102`, `r165` par des phrases
   grammaticales ; réparer le doublon `r336`/`r358` et sa coref ; corriger `r340`/`r368` et indexer la
   coref par span.
4. **Mesurer par langue** : `evaluer_gold` ne sépare que `hand`/`reel`/`synthetique` ; publier `fr` et
   `en`, plein et réel seul, et distinguer **239 segments à cible** de **282 chaînes de cibles** (43
   segments ont 2 cibles). Publier `exact-first` et `exact-any` (le français gagne 2 cas).
5. **Ne pas ajuster le lexique au gold** : les 15 faux négatifs de `_est_verbe` sont une mesure du
   lexique, pas une invitation à ajouter `rains`, `falls`, `hung`… au gold ou au lexique sans règle
   générale. La v2/v3 a déjà documenté ce risque d'ajustement.

## 11. Fichiers et reproduction

- [`pensee-gold-anglais.json`](pensee-gold-anglais.json) — chiffres, spans, cibles, anomalies, contrôles.
- [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py) / [`gold_reel.json`](../tools/tests/linguistique/gold_reel.json) — le gold réel (432 phrases).
- [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) — `charger`, `evaluer_bloc`, POS/syntagmes/attachement.
- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — `Heuristique`, `_est_verbe`, `_pos`.
- [`rapport-pensee-attachement-v3.md`](rapport-pensee-attachement-v3.md) — l'attachement courant (141/145).
- [`rapport-pensee-spans.md`](rapport-pensee-spans.md) — les 94 spans (48 REL, 33 SUB, 13 GP).

Reproduction (le worktree et le HEAD donnaient les mêmes chiffres à l'audit) :

```python
import sys; sys.path.insert(0, "tools"); sys.path.insert(0, "tools/tests/linguistique")
import evaluer_gold as eg, bloc_linguistique as bl
h, phrases = bl.Heuristique(), eg.charger()
for lg in ("fr", "en"):
    r = eg.evaluer_bloc("heuristique", h, [p for p in phrases if p["langue"] == lg])
    print(lg, r["pos"]["exactitude"], r["syntagme"]["f1"],
          r["attachement"]["couverture"], r["attachement"]["exact_taux_span"])
```
