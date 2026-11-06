# Rapport — les 43 spans non prédits de l'attachement v7

> **Ligne de roadmap** : **B13** (attachement, règle 6) · **Date** : 2026-11-05 ·
> **Commit de départ** : `69bd865ec1bae1958b6f617bde4bf685a15d7d67` (branche `s/v7`) ·
> **Périmètre** : `tools/bloc_linguistique.py` (`Heuristique`, `_syntagmes_simple`,
> `_cible_precedent`), `tools/tests/linguistique/evaluer_gold.py` (`charger`, `evaluer_bloc`),
> `tools/tests/linguistique/gold_split.py` (`dev`, `test`).
> **Livrables** : ce rapport + [`pensee-spans-v7.json`](pensee-spans-v7.json).
> **Aucun fichier existant n'a été modifié par cette session** ; les mesures viennent d'une copie locale
> (`/tmp/spans/sim3.py`, sous-classe de `Heuristique` + copie instrumentée de
> `_syntagmes_simple`), non commitée. Le dispositif officiel (`evaluer_bloc`) redonne
> **exactement** la ligne de base 196/195 et F1 0,5555 sur le gold vivant 612.

## 1. Résumé

**État de départ** : 239 cibles, **196 labels au bon span**, **195 exacts / 196** (0,9949),
43 non prédits = **21 REL, 17 SUB, 5 GP**. **État final** de la meilleure combinaison :
**222 labels, 222 exacts / 222** (1,0000), soit **222/239 = 0,9289** des cibles ; il reste
**17 cibles non couvertes** (8 REL, 5 SUB, 4 GP), toutes explicitement classées au § 7.

| mesure | départ | final | delta |
|---|---:|---:|---:|
| cibles | 239 | 239 | — |
| labels au bon span | 196 | 222 | +26 |
| exacts (span + cible) | 195 | 222 | **+27** |
| exact / labels | 0,9949 | **1,0000** | +0,0051 |
| couverture (labels / cibles) | 0,8201 | **0,9289** | +0,1088 |
| exact / cibles | 0,8159 | **0,9289** | +0,1130 |
| F1 syntagmes (gold vivant 612) | 0,5555 | **0,5851** | +0,0296 |
| dev — exact / labels | 133 / 134 (0,9925) | **154 / 154 (1,0000)** | +21 |
| test — exact / labels | 62 / 62 (1,0000) | **68 / 68 (1,0000)** | +6 |
| dev — couverture | 134 / 163 | **154 / 163** | +20 |
| test — couverture | 62 / 76 | **68 / 76** | +6 |

> **Le 0,5595 du commit est le gold gelé 602** ; sur le gold **vivant 612** (celui de
> `charger()`), la F1 de départ est **0,5555** — c'est la valeur reproductible et celle
> utilisée ici. L'attachement (196/195) est identique sur les deux golds, car les 10 phrases
> ajoutées après le gel n'ont aucune cible (cf. [`rapport-audit-v7.md`](rapport-audit-v7.md)).

**Trois règles retenues** :

| règle | quoi | dev | test | tous |
|---|---|---:|---:|---:|
| **R1** | frontière de clause REL/SUB (pronom, modaux, 2e prédicat) | **+15 / −0** | **+5 / −0** | **+20 / −0** |
| **R2** | type REL/SUB par antécédent | **+3 / −0** (+1 label faux, r245) | 0 / −0 | **+3 / −0** |
| **R3** | trois gardes de lexique/contexte (a `car`, b GP/déterminant, c `fall`/`call`) | **+1 / −0** seule ; **+3** en marge de R1+R2 | **+1 / −0** | **+2 / −0** seule ; **+4** en marge |
| **R1+R2+R3** | combinaison | **154 / 154** | **68 / 68** | **222 / 222** |

> Les colonnes « dev » et « test » comptent les **exacts gagnés / perdus** par rapport à
> la ligne de base (195 exacts). Un « +3 » signifie trois cibles passées de non-exactes à
> exactes ; aucune cible exacte n'est devenue fausse.

## 2. Dispositif et protocole

- **Gold** : `charger()` = 20 phrases *hand* + 432 *reel* + 160 *synthetique* = **612 phrases**,
  **3 179 tokens**, **1 863 segments**, **239 cibles** (GP 96, SUB 69, REL 74).
- **Split** : `crc32(id) % 3 == 0` → test. **dev** = 422 phrases / **163 cibles** (fr 277,
  en 145 ; hand 15, reel 302, synthetique 105) ; **test** = 190 phrases / **76 cibles**
  (fr 125, en 65 ; hand 5, reel 130, synthetique 55). Aucune phrase des deux côtés.
- **Ligne de base** : `bl.Heuristique()` (S activé, union activée), `evaluer_bloc`, gold vivant :
  `cibles 239, labels 196, exact 195, exact/labels 0,9949, couverture 0,8201, F1 0,5555`.
- **Harnais** : sous-classe `Sim(Heuristique)` dans `/tmp/spans/sim3.py` ; `_syntagmes_simple`
  est **recopiée** et instrumentée par des drapeaux (R1, R2, R3GP, R4, NOADV). Aucun
  fichier du dépôt n'est touché. Le harnais reproduit la ligne de base au chiffre près
  (196/195, F1 0,5555), ce qui valide la fidélité de la simulation.
- **Réglage** : les règles ont été **paramétrées sur dev seul** ; le test n'a été lu qu'après
  sélection. Limite honnête : le **diagnostic** des 43 (demandé) a porté sur dev **et** test,
  donc le test n'est pas aveugle au sens strict ; ses 6 gains sont une **confirmation**, pas
  une prédiction. Le split est un seul découpage déterministe, sans validation croisée.

## 3. Les 43, par cause probable

### 3.1 Effectifs par cause

| cause | effectif | dont REL / SUB / GP | mécanisme | règle | sort |
|---|---:|---|---|---|---|
| **Frontière de clause (arrêt précoce + 2e prédicat)** | **20** | 12 REL / 8 SUB / 0 GP | le scanner REL/SUB s'arrête au pronom pris pour un verbe, ou avale le 2e prédicat | R1 | 20 exacts |
| **Type attendu différent** | **4** | 0 / 4 / 0 | « when » sans antécédent classé REL ; r245 : cible `call` non reconnue | R2 (+R3c) | 4 exacts |
| **GN qui avale** | **4** | 1 REL / 3 SUB / 0 GP | 3 verbes synthétiques hors lexique + le « car » français en anglais | R3a (+R1/R2) ; sinon lexique disjoint | 1 exact, 3 absents |
| **Lexique disjoint synthétique (REL sur-longues)** | **6** | 6 / 0 / 0 | le 2e verbe de la relative est hors lexique → la REL inclut la principale | — (protocole) | 6 absents |
| **Gold synthétique sans préposition** | **4** | 0 / 0 / 4 | le GP du gold commence après la préposition (bug du générateur) | — (gold) | 4 absents |
| **Marqueur absent ou élidé** | **2** | 1 / 1 / 0 | relative zéro (r035) ; « qu'il » non tokenisé (r264) | — | 2 absents |
| **Lexique verbal réel** | **1** | 1 / 0 / 0 | `achetée` / `roule` hors lexique | — (lexique ouvert) | 1 absent |
| **GP tronqué par un faux verbe** | **1** | 0 / 0 / 1 | `bus` reconnu verbe par « bu » + « s » | R3b | 1 exact |
| **Adverbe final (arbitrage dev/test)** | **1** | 0 / 1 / 0 | `tomorrow` exclu par la règle d'adverbe final | — (arbitrage) | 1 absent |
| **Total** | **43** | **21 / 17 / 5** | | | **26 exacts, 17 absents** |

### 3.2 Sous-causes

| sous-cause | effectif | type | règle | sort |
|---|---:|---|---|---|
| arrêt précoce : pronom pris pour un verbe | **15** | 7 REL / 8 SUB | R1a | 15 exacts |
| 2e prédicat avalé (2e AUX, 2e verbe, AUX saturé) | **5** | 5 REL | R1b/c | 5 exacts |
| type REL→SUB (« when » sans antécédent) | **3** | 3 SUB | R2 | 3 exacts |
| type récupéré mais cible `call` non reconnue | **1** | 1 SUB | R2 + R3c | 1 exact |
| GN avalé par la collision `car` | **1** | 1 REL | R3a + R1/R2 | 1 exact |
| GN avalé par un verbe synthétique hors lexique | **3** | 3 SUB | — (lexique disjoint) | 3 absents |
| REL synthétique sur-longue (2e verbe hors lexique) | **6** | 6 REL | — (lexique disjoint) | 6 absents |
| GP synthétique sans préposition | **4** | 4 GP | — (gold) | 4 absents |
| verbe réel hors lexique (`achetée`/`roule`) | **1** | 1 REL | — (lexique réel) | 1 absent |
| relative zéro (marqueur absent) | **1** | 1 REL | — | 1 absent |
| « qu' » élidé non tokenisé | **1** | 1 SUB | — (tokenisation) | 1 absent |
| GP tronqué (`bus`) | **1** | 1 GP | R3b | 1 exact |
| adverbe final (`tomorrow`) | **1** | 1 SUB | — (arbitrage) | 1 absent |
| **Total** | **43** | **21 REL / 17 SUB / 5 GP** | | **26 exacts, 17 absents** |

### 3.3 Les 43, cas par cas

Colonnes : `split` (dev/test), `lg` (langue), `type`, `span` (offsets gold), `texte` (span gold),
`marqueur` (premier token du span, ou `∅` quand le marqueur est absent), `cible` (gold),
`phrase` (contexte), `sortie` (état après la meilleure combinaison).

#### frontière de clause — arrêt précoce (pronom pris pour un verbe) — 15 cas

| id | split | lg | type | span | texte | marqueur | cible | phrase | sortie |
|---|---|---|---|---|---|---|---|---|---|
| `g017` | dev | en | SUB | 9:28 | « that she would come » | `that` | `said` | « She said that she would come yesterday. » | exact (R1) |
| `r034` | dev | en | REL | 9:20 | « that I read » | `that` | `book` | « The book that I read is exciting. » | exact (R1) |
| `r074` | dev | en | REL | 9:22 | « that you read » | `that` | `book` | « The book that you read is long. » | exact (R1) |
| `r114` | dev | en | REL | 9:20 | « that we saw » | `that` | `film` | « The film that we saw was long. » | exact (R1) |
| `r205` | dev | en | SUB | 8:26 | « that you are right » | `that` | `think` | « I think that you are right. » | exact (R1) |
| `r214` | test | en | REL | 9:20 | « that I read » | `that` | `book` | « The book that I read is good. » | exact (R1) |
| `r216` | test | en | SUB | 9:22 | « that he comes » | `that` | `says` | « She says that he comes. » | exact (R1) |
| `r219` | dev | en | SUB | 7:20 | « that you come » | `that` | `know` | « I know that you come. » | exact (R1) |
| `r240` | dev | en | SUB | 10:26 | « that he is right » | `that` | `believe` | « I believe that he is right. » | exact (R1) |
| `r243` | dev | en | REL | 10:24 | « that we bought » | `that` | `house` | « The house that we bought is old. » | exact (R1) |
| `r247` | dev | en | SUB | 8:26 | « that we must leave » | `that` | `think` | « I think that we must leave. » | exact (R1) |
| `r278` | dev | en | REL | 10:22 | « that you eat » | `that` | `bread` | « The bread that you eat is fresh. » | exact (R1) |
| `r281` | test | en | SUB | 8:21 | « that it rains » | `that` | `says` | « He says that it rains. » | exact (R1) |
| `r285` | dev | en | REL | 10:22 | « that we took » | `that` | `table` | « The table that we took is big. » | exact (R1) |
| `r296` | dev | en | SUB | 9:24 | « that she leaves » | `that` | `says` | « She says that she leaves. » | exact (R1) |

#### frontière de clause — 2e prédicat avalé — 5 cas

| id | split | lg | type | span | texte | marqueur | cible | phrase | sortie |
|---|---|---|---|---|---|---|---|---|---|
| `r115` | test | en | REL | 10:26 | « where I was born » | `where` | `house` | « The house where I was born is small. » | exact (R1) |
| `r224` | dev | fr | REL | 8:33 | « dont la voiture est rouge » | `dont` | `homme` | « L'homme dont la voiture est rouge arrive. » | exact (R1) |
| `r239` | test | en | REL | 8:24 | « whose car is red » | `whose` | `man` | « The man whose car is red arrives. » | exact (R1) |
| `r291` | dev | en | REL | 9:29 | « that is on the table » | `that` | `book` | « The book that is on the table is mine. » | exact (R1) |
| `r299` | dev | en | REL | 11:24 | « that we cross » | `that` | `bridge` | « The bridge that we cross is old. » | exact (R1) |

#### type attendu différent (REL→SUB) — 3 cas

| id | split | lg | type | span | texte | marqueur | cible | phrase | sortie |
|---|---|---|---|---|---|---|---|---|---|
| `r215` | dev | en | SUB | 0:13 | « When it rains » | `When` | `stay` | « When it rains, I stay. » | exact (R2) |
| `r279` | dev | en | SUB | 0:13 | « When it snows » | `When` | `stay` | « When it snows, we stay. » | exact (R2) |
| `r294` | dev | en | SUB | 0:13 | « When you want » | `When` | `leave` | « When you want, we leave. » | exact (R2) |

#### type récupéré, cible non (verbe call hors lexique) — 1 cas

| id | split | lg | type | span | texte | marqueur | cible | phrase | sortie |
|---|---|---|---|---|---|---|---|---|---|
| `r245` | dev | en | SUB | 0:15 | « When you arrive » | `When` | `call` | « When you arrive, call me. » | exact (R2+R3c) |

#### GN avalé par la collision car (SUBORDONNANTS fr en anglais) — 1 cas

| id | split | lg | type | span | texte | marqueur | cible | phrase | sortie |
|---|---|---|---|---|---|---|---|---|---|
| `r280` | dev | en | REL | 8:21 | « that I bought » | `that` | `car` | « The car that I bought runs. » | exact (R3a+R1/R2) |

#### SUB synthétique : verbe principal hors lexique → GN l'avale — 3 cas

| id | split | lg | type | span | texte | marqueur | cible | phrase | sortie |
|---|---|---|---|---|---|---|---|---|---|
| `s044` | dev | fr | SUB | 17:29 | « que ils crie » | `que` | `nage` | « une fenêtre nage que ils crie » | absent (lexique disjoint) |
| `s112` | test | fr | SUB | 24:39 | « que Lucas ferme » | `que` | `nage` | « la brillante forêt nage que Lucas ferme » | absent (lexique disjoint) |
| `s114` | dev | fr | SUB | 22:43 | « que les avocat compte » | `que` | `dessine` | « ce doux nuage dessine que les avocat compte » | absent (lexique disjoint) |

#### REL synthétique : 2e verbe hors lexique disjoint — 6 cas

| id | split | lg | type | span | texte | marqueur | cible | phrase | sortie |
|---|---|---|---|---|---|---|---|---|---|
| `s010` | dev | fr | REL | 10:18 | « qui nage » | `qui` | `chemin` | « un chemin qui nage prépare » | absent (lexique disjoint) |
| `s035` | test | fr | REL | 10:19 | « qui ferme » | `qui` | `papier` | « un papier qui ferme observe » | absent (lexique disjoint) |
| `s061` | dev | fr | REL | 9:18 | « qui saute » | `qui` | `nuage` | « ce nuage qui saute observe » | absent (lexique disjoint) |
| `s065` | dev | fr | REL | 5:17 | « qui commence » | `qui` | `elle` | « elle qui commence nage » | absent (lexique disjoint) |
| `s125` | dev | fr | REL | 11:21 | « qui compte » | `qui` | `renard` | « mon renard qui compte crie » | absent (lexique disjoint) |
| `s141` | test | fr | REL | 5:15 | « qui trouve » | `qui` | `Emma` | « Emma qui trouve compte » | absent (lexique disjoint) |

#### gold synthétique sans préposition (bug générateur) — 4 cas

| id | split | lg | type | span | texte | marqueur | cible | phrase | sortie |
|---|---|---|---|---|---|---|---|---|---|
| `s027` | dev | fr | GP | 31:33 | « il » | `∅ (préposition hors span)` | `marche` | « mon sombre village marche avec il » | absent (gold) |
| `s146` | test | fr | GP | 25:35 | « les jardin » | `∅ (préposition hors span)` | `observe` | « ma montagne observe avec les jardin » | absent (gold) |
| `s148` | dev | fr | GP | 20:39 | « les ancienne lettre » | `∅ (préposition hors span)` | `nage` | « le voyage nage pour les ancienne lettre » | absent (gold) |
| `s160` | test | fr | GP | 20:29 | « le renard » | `∅ (préposition hors span)` | `nage` | « le chemin nage avec le renard » | absent (gold) |

#### couverture verbale réelle (achetée/roule) — 1 cas

| id | split | lg | type | span | texte | marqueur | cible | phrase | sortie |
|---|---|---|---|---|---|---|---|---|---|
| `r255` | test | fr | REL | 11:27 | « que j'ai achetée » | `que` | `voiture` | « La voiture que j'ai achetée roule. » | absent (lexique réel) |

#### marqueur absent (relative zéro) — 1 cas

| id | split | lg | type | span | texte | marqueur | cible | phrase | sortie |
|---|---|---|---|---|---|---|---|---|---|
| `r035` | dev | en | REL | 9:24 | « she talks about » | `∅ (relative zéro)` | `film` | « The film she talks about is out. » | absent (pas de règle) |

#### marqueur élidé qu' non tokenisé — 1 cas

| id | split | lg | type | span | texte | marqueur | cible | phrase | sortie |
|---|---|---|---|---|---|---|---|---|---|
| `r264` | test | fr | SUB | 8:26 | « qu'il vient demain » | `qu'il` | `sais` | « Je sais qu'il vient demain. » | absent (tokenisation) |

#### GP tronqué par un faux verbe (bus) — 1 cas

| id | split | lg | type | span | texte | marqueur | cible | phrase | sortie |
|---|---|---|---|---|---|---|---|---|---|
| `r153` | test | en | GP | 8:19 | « for the bus » | `for` | `wait` | « We wait for the bus. » | exact (R3b) |

#### adverbe final (règle trop stricte, arbitrage dev/test) — 1 cas

| id | split | lg | type | span | texte | marqueur | cible | phrase | sortie |
|---|---|---|---|---|---|---|---|---|---|
| `r288` | test | en | SUB | 7:29 | « that he comes tomorrow » | `that` | `know` | « I know that he comes tomorrow. » | absent (arbitrage) |

**Lecture** : 26 des 43 sont récupérés exactement ; les 17 autres sont absents, aucun n'est
faux. Les 26 se répartissent en **R1 = 20**, **R2 = 3** (r215, r279, r294), **R2+R3c = 1**
(r245), **R3a = 1** (r280), **R3b = 1** (r153).

## 4. Mécanismes (pourquoi ces spans manquent)

### 4.1 Frontière de clause — 20 cas

Trois bugs se cumulent dans la boucle REL/SUB de `_syntagmes_simple` :

1. **Un pronom est pris pour un verbe par position.** `est_verbe` dit « le mot après un
   pronom sujet est un verbe ». Or `SUJETS` contient `that`, `which`, `who`, `qu`, `qui` :
   dans « The book **that I** read », `I` est déclaré verbe, `read` devient le 2e verbe, et la
   REL s'arrête à `that I` (span [9:15] au lieu de [9:20]). **13 cas** : r034, r074, r114,
   r205, r214, r216, r219, r240, r243, r278, r281, r285, r296.
2. **Les modaux ne sont pas des AUX.** `AUXILIAIRES` ne contient ni `would`, ni `must`, ni
   `can`, `could`, `should`, `will`, `shall`, `may`, `might`. « that she **would** come » :
   `would` est compté verbe plein, `come` devient le 2e verbe → arrêt à `that she would`
   (**2 cas** : g017, r247). Le total « arrêt précoce » est donc 13 + 2 = 15.
3. **Le 2e prédicat est avalé.** Un 2e AUX (« that is on the table **is** mine »), ou un verbe
   plein après un AUX déjà saturé (« whose car is red **arrives** », « dont la voiture est
   rouge **arrive** »), n'ouvre pas la principale : la REL va jusqu'au bout (r115, r224, r239,
   r291, r299).

### 4.2 Type attendu différent — 4 cas

La règle actuelle `SUB si (marqueur ∈ SUBORDONNANTS ou précédent = GV), sinon REL` classe
« **When** it rains » en REL quand il n'y a **aucun** segment précédent (début de phrase).
C'est le cas de r215, r279, r294 (dev) et r245 (dev). Le gold attend SUB. r245 est particulier :
le span devient juste avec R2, mais la cible `call` reste vide car `call` n'est pas dans le
lexique verbal anglais ; R3c la récupère.

### 4.3 GN qui avale — 4 cas

Trois SUB synthétiques (s044, s112, s114) : le verbe principal (« nage », « dessine ») est hors
lexique, donc le GN l'avale (« une fenêtre nage »), le `que` suit un GN et devient REL au lieu
de SUB. Un cas réel : r280 « The **car** that I bought runs » — `car` est dans
`SUBORDONNANTS` (conjonction française), donc le GN s'arrête à `The` et la REL cherchée
n'existe pas. R3a (conditionner `SUBORDONNANTS` par la langue) + R1/R2 récupèrent r280.

### 4.4 Lexique disjoint synthétique — 9 cas

Le générateur `gold_synthetique.py` utilise un lexique verbal **disjoint** de l'heuristique
(« pour mesurer la généralisation des classes ouvertes ») : `nage, crie, rêve, prépare, range,
compte, dessine, observe, écoute, cherche, trouve, ouvre, ferme, commence, finit, saute,
marche`. Sept lemmes manquent au lexique du bloc (`nage, crie, dessine, observe, prépare,
compte, range`). Sans eux, le 2e verbe n'est pas reconnu (6 REL sur-longues : s010, s035,
s061, s065, s125, s141) ou le verbe principal est avalé par le GN (3 SUB : s044, s112, s114).
**Les ajouter serait tricher** : c'est le vocabulaire tenu à l'écart par le protocole du
générateur. Mesuré pour information : +8 exacts (5 dev, 3 test), s065 restant absent ;
voir § 6.2.

### 4.5 Gold synthétique sans préposition — 4 cas

Le générateur a **deux conventions** de GP. En mode `sv_gp` (ligne 104) le GP commence à la
préposition (`i - 1`, préposition incluse) ; en mode `sv` (ligne 98) :
`i = v + [t[0] for t in gv].index(prep) + 1` puis `("GP", i, i + len(g))` : le GP commence
**après** la préposition. Les 4 cas sont s027 (« avec il » → GP gold « il »), s146 (« avec les
jardin » → « les jardin »), s148 (« pour les ancienne lettre » → « les ancienne lettre »),
s160 (« avec le renard » → « le renard »). Ce n'est **pas une erreur du modèle** : le modèle
prédit le GP avec la préposition, comme les 20 autres GP synthétiques et les 72 GP hand/reel.
Contrefactuel mesuré : corriger le gold (démarrer à la préposition) rend les 4 cas exacts,
**sans aucune perte** (+4 exacts, 0 régression). C'est une correction de **gold**, pas une
règle de modèle.

### 4.6 Lexique verbal réel — 1 cas

r255 « La voiture que j'ai **achetée roule** » : `achetée` et `roule` ne sont pas reconnus,
donc la REL va jusqu'à `roule` ([11:33] au lieu de [11:27]). Une extension lexicale
(`acheter`, `rouler`) le corrigerait, mais le lexique est un puits sans fond ; ce n'est pas
une règle de segmentation. À traiter dans un chantier « couverture verbale », pas ici.

### 4.7 Marqueur absent ou élidé — 2 cas

- **r035** « The film **she** talks about is out » : relative zéro, aucun marqueur ; le GN
  avale `she` (« The film she »), `about` est traité comme un verbe, et la REL [9:24] n'existe
  pas. Une règle « GN s'arrête devant un pronom sujet suivi d'un verbe, puis REL jusqu'à la
  préposition finale » serait ad hoc pour un seul cas.
- **r264** « Je sais **qu'il** vient demain » : `_mots` tokenise `qu'il` en **un seul token**
  (la classe d'élision `[ldmtsnLDMTNS]` ne contient pas `q`), donc la branche marqueur ne se
  déclenche pas ; le GV `sais qu'il vient demain` avale tout. Le générateur S donne bien
  SUB [8:19], mais pas `demain`. Il faudrait tokeniser `qu'` (ou tester `qu'` comme marqueur)
  **et** relâcher la règle d'adverbe final.

### 4.8 GP tronqué par un faux verbe — 1 cas

r153 « We wait **for the bus** » : `_est_verbe("bus")` est vrai parce que `bus` finit par
`s` et que `bu` (participe de *boire*) est dans `VERBES_CONNUS`. Le GP s'arrête à `for the`
([8:15] au lieu de [8:19]). Un déterminant ne peut pas introduire un verbe : R3b.

### 4.9 Adverbe final — 1 cas

r288 « I know that he comes **tomorrow** » : la règle existante « un adverbe final
n'appartient pas à la clause » coupe `tomorrow` ([7:20] au lieu de [7:29]). La retirer
récupère r288 (test) mais **perd g017** (« that she would come **yesterday** », dev), dont le
gold exclut `yesterday`. C'est un **arbitrage 1 pour 1** entre deux golds : la règle est
conservée car dev perdrait 1 gain. La portée de l'adverbe final est une ambiguïté de gold,
pas une erreur de règle.

## 5. Règles proposées et mesures

Chaque règle est mesurée **seule** puis **en marge** de la précédente. Les colonnes `labels`,
`exacts` et `exact/labels` sont sur le corpus indiqué ; `gains` et `pertes` comptent les
transitions **exact → non exact** (une perte) et **non exact → exact** (un gain) par rapport
à la ligne de base. Un **nouveau label faux** (cible vide ou fausse sur un span qui était
absent) est signalé séparément : il ne compte pas comme une perte d'exact mais dégrade
`exact/labels`.

### 5.1 R1 — Frontière de clause REL/SUB

**Où** : `_syntagmes_simple`, branche `if typ == "mot" and (n in RELATIFS or n in SUBORDONNANTS)`
(lignes 858-897 de l'état `69bd865e`), et le `est_verbe` local (lignes 843-855).

**Quoi** : trois corrections dans la boucle de scan :

```python
# R1a — un pronom n'est jamais un verbe par la règle de position
if _normaliser(m) in lex.get("PRON", set()):
    return False

# R1b — les modaux sont des AUX
AUX_MOD = AUXILIAIRES | {"would","must","can","could","should","will","shall","may","might"}
aux_vus = 0
while j < len(mots) and mots[j][3] == "mot":
    m = mots[j][2]
    aux = _normaliser(m) in AUX_MOD
    if aux:
        if verbes_vus >= 1 or aux_vus >= 1:   # 2e AUX = principale
            break
        aux_vus += 1
    elif est_verbe(mots[j][0], m):
        if verbes_vus >= 1:                   # 2e verbe plein = principale
            break
        if aux_vus >= 1 and _normaliser(mots[j-1][2]) not in AUX_MOD:
            break                             # AUX saturé + verbe = principale
        verbes_vus += 1
    # la règle existante « adverbe final » est conservée (cf. § 4.9)
    j += 1
```

**Effet** : `that I read` [9:15] → [9:20] ; `that she would come` [9:17] → [9:28] ;
`whose car is red arrives` [8:32] → [8:24] ; `dont la voiture est rouge arrive` [8:40] → [8:33].

| corpus | labels / cibles | exacts | exact/labels | gains | pertes | F1 |
|---|---:|---:|---:|---:|---:|---:|
| dev | 149/163 | 148 | 0,9933 | +15 | −0 | 0,5717 |
| test | 67/76 | 67 | 1,0000 | +5 | −0 | 0,5823 |
| tous | 216/239 | 215 | 0,9954 | +20 | −0 | 0,5750 |

Gains dev : `g017, r034, r074, r114, r205, r219, r224, r240, r243, r247, r278, r285, r291,
r296, r299`. Gains test : `r115, r214, r216, r239, r281`. **Aucune perte, aucun nouveau
label faux.** C'est la règle à implémenter en premier.

### 5.2 R2 — Type REL/SUB par antécédent

**Où** : même branche, ligne 874 :

```python
DURS = {"qui","dont","où","which","who","whom","whose","where"}
stype = "REL" if (n in DURS or (precedent == "GN" and n in RELATIFS)) else "SUB"
```

**Quoi** : une REL n'est possible qu'avec un antécédent GN (ou un relatif dur) ; sinon c'est
une SUB. Corrige « **When** it rains » (aucun précédent → SUB), « **that** … » après un GV
(SUB) et après un GN (REL).

| corpus | labels / cibles | exacts | exact/labels | gains | pertes | F1 |
|---|---:|---:|---:|---:|---:|---:|
| dev | 138/163 | 136 | 0,9855 | +3 | −0 | 0,5547 |
| test | 62/76 | 62 | 1,0000 | +0 | −0 | 0,5651 |
| tous | 200/239 | 198 | 0,9900 | +3 | −0 | 0,5579 |

Gains dev : `r215, r279, r294`. **0 perte**, mais **1 nouveau label faux** : `r245` passe de
« absent » à SUB [0:15] avec la cible `arrive` au lieu de `call` (car `call` n'est pas un
verbe pour le bloc). R3c le corrige ; sans R3c, `exact/labels` dev vaut 136/138 = 0,9855.
Sur test, R2 ne gagne rien (les 3 cas « When » sont en dev) mais ne perd rien.

### 5.3 R3 — Trois gardes de lexique et de contexte

R3 est un **faisceau de trois micro-règles** indépendantes, toutes du même ordre : une classe
fermée ou un lexique doit être **conditionné par la langue ou le contexte**. Chacune est
mesurée séparément ; le faisceau est retenu parce qu'il ne perd rien et gagne 4 exacts en
marge de R1+R2.

#### R3a — `car` n'est pas un subordonnant anglais

```python
SUB = (SUBORDONNANTS - {"car"}) if langue == "en" else SUBORDONNANTS
# remplacer les trois occurrences de SUBORDONNANTS par SUB dans _syntagmes_simple
```

Récupère r280 avec R1/R2 (`The car that I bought runs`), en empêchant le GN de s'arrêter à
`The`. Seul, R3a ne gagne rien (le span et la cible dépendent aussi de R1/R2) ; c'est une
**synergie**.

#### R3b — un déterminant n'introduit pas un verbe dans un GP

```python
def est_verbe_gp(d, m):
    idx = par_debut.get(d)
    if idx and _normaliser(mots[idx-1][2]) in lex.get("DET", set()):
        return False
    return est_verbe(d, m)
# utiliser est_verbe_gp (et non est_verbe) dans la boucle GP
```

Récupère r153 (`for the bus`). **Portée volontairement limitée au GP** : appliquée partout,
la même règle casse 4 cas dev et 1 test (cf. § 6.1).

#### R3c — compléter le lexique anglais (`fall`, `call`)

```python
VERBES["en"] |= {"fall","falls","fell","fallen","call","calls","called","calling"}
VERBES_CONNUS |= {"fall","falls","fell","fallen","call","calls","called","calling"}
```

Récupère la cible de r245 (`call me` devient un GV, la cible de la SUB est `call`) et le cas
**r102** (`The rain falls since this morning`, seul faux du baseline : le GP avait le bon
span mais une cible vide). Deux verbes anglais courants, pas le lexique synthétique.

| corpus | labels / cibles | exacts | exact/labels | gains | pertes | F1 |
|---|---:|---:|---:|---:|---:|---:|
| dev | 134/163 | 134 | 1,0000 | +1 | −0 | 0,5582 |
| test | 63/76 | 63 | 1,0000 | +1 | −0 | 0,5722 |
| tous | 197/239 | 197 | 1,0000 | +2 | −0 | 0,5625 |

R3 seule : gains dev `r102`, test `r153` ; 0 perte, 0 label faux. En marge de R1+R2, elle
ajoute **+3 dev** (`r280`, `r102`, `r245`) et **+1 test** (`r153`) : R1+R2 passe de 151 à
154 exacts en dev, de 67 à 68 en test.

### 5.4 Combinaison R1+R2+R3

| corpus | labels / cibles | exacts | exact/labels | couverture | gains | pertes | F1 |
|---|---:|---:|---:|---:|---:|---:|---:|
| dev | 154/163 | 154 | 1,0000 | 0,9448 | +21 | −0 | 0,5831 |
| test | 68/76 | 68 | 1,0000 | 0,8947 | +6 | −0 | 0,5896 |
| tous | 222/239 | 222 | 1,0000 | 0,9289 | +27 | −0 | 0,5851 |

**Tous les labels couverts sont exacts** : `exact/labels = 1,0000` sur dev, test et tous.
Il reste 17 cibles non couvertes, toutes classées au § 7. Les 27 gains sont les 26 gains des
43 (`r215`, `r279`, `r294`, `r245`, `r280`, `r153` et les 20 de R1) plus **r102**, hors 43.

### 5.5 Décomposition du gain final

| variante | labels | exacts | exact/labels | F1 |
|---|---:|---:|---:|---:|
| ligne de base | 196 | 195 | 0,9949 | 0,5555 |
| R1+R2 | 220 | 218 | 0,9909 | 0,5774 |
| + R3a/R3b (`car`, GP/déterminant) | 222 | 220 | 0,9910 | 0,5819 |
| + R3c `fall` | 222 | 221 | 0,9955 | 0,5848 |
| + R3c `call` | 222 | **222** | **1,0000** | **0,5851** |

La marche `R1+R2` fait payer 2 labels faux (r102, préexistant, et r245, nouveau) : `exact/labels` baisse
temporairement de 0,9949 à 0,9909. **R3c la rétablit à 1,0000** ; c'est la raison de garder
R3c dans le faisceau, même si sa marge dev (2 exacts) peut sembler modeste.

### 5.6 Par langue et par type

| groupe | cibles | labels | exacts | exact/cibles | exact/labels |
|---|---:|---:|---:|---:|---:|
| fr | 151 | 136 | 136 | 0,9007 | 1,0000 |
| en | 88 | 86 | 86 | 0,9773 | 1,0000 |
| REL | 74 | 66 | 66 | 0,8919 | 1,0000 |
| SUB | 69 | 64 | 64 | 0,9275 | 1,0000 |
| GP | 96 | 92 | 92 | 0,9583 | 1,0000 |

Ligne de base correspondante (exacts) : fr **135/151**, en **60/88**, REL **53/74**, SUB
**52/69**, GP **90/96**. Le corpus porte surtout sur l'anglais (88 cibles sur 239) : c'est là que R1
gagne le plus (60 → 86 exacts, 0,9773 des cibles).

## 6. Règles rejetées, ou qui échouent

### 6.1 R3 globale — le contexte DET appliqué partout

**Idée** : un mot précédé d'un déterminant n'est jamais un verbe, dans **tous** les chunkers.
**Mesure** : dev **+11 / −4** (pertes `r083`, `r246`, `r287`, `r297`), F1 0,5607 ; test
**+4 / −1** (perte `r220`), F1 0,5725. **Rejetée.** Deux contre-exemples suffisent :
« The cat **that sleeps** is black » (`that` est DET, mais `sleeps` est bien un verbe) et
« Le train **entre** en gare » (`entre` est PREP **et** verbe). La règle n'est valide que
dans le GP, où un déterminant ne peut pas précéder un verbe (R3b).

### 6.2 R4 — ajouter le lexique verbal synthétique

**Idée** : ajouter les 7 lemmes manquants (`nage, crie, dessine, observe, prépare, compte,
range`). **Mesure** : **+5 dev** (`s010, s044, s061, s114, s125`), **+3 test** (`s035, s112,
s141`), 0 perte ; s065 reste absent (l'antécédent `elle` n'est pas un GN). **Rejetée comme
mesure de généralisation** : le générateur déclare ce lexique **disjoint** précisément pour
tester les classes ouvertes ; l'ajouter, c'est apprendre le vocabulaire du test. C'est
pourtant la preuve que les 9 cas synthétiques sont un **artefact de vocabulaire**, pas un
défaut de règle de segmentation.

### 6.3 Supprimer la règle « adverbe final » (NOADV)

**Idée** : ne plus exclure un adverbe final. **Mesure** (avec R1+R2+R3) : dev **153/154**
au lieu de **154/154** (g017 n'est plus récupéré ; ce n'est pas une perte d'exact, g017 était
déjà absent), test **69/76** au lieu de **68/76** (r288 récupéré). **Rejetée par le protocole
dev** : elle échange 1 gain dev (g017) contre 1 gain test (r288). La portée de `yesterday` /
`tomorrow` est une ambiguïté de gold ; on garde la règle existante et on documente r288
comme non récupéré.

### 6.4 Relative zéro (r035)

Une règle « GN s'arrête devant un pronom sujet suivi d'un verbe, puis REL jusqu'à la
préposition finale » récupérerait r035, mais elle est écrite pour **un seul cas** et
dépend d'une préposition finale (`about`) que le chunker traite comme un verbe. Non
implémentée : coût/risque disproportionné.

### 6.5 Correction du gold synthétique (contrefactuel)

Ce n'est pas une règle de modèle, mais le contrefactuel est net : en corrigeant la ligne 98
de `gold_synthetique.py` (GP démarrant à la préposition), les 4 cas s027, s146, s148, s160
deviennent exacts, **sans aucune perte** (+4 exacts). Le modèle prédit déjà le bon span avec
la préposition. À faire dans un commit **gold**, pas dans le modèle.

## 7. Cas non récupérables (explicite)

### 7.1 Non récupérables par une règle de modèle justifiée — 13

| catégorie | n | ids | pourquoi | que faudrait-il ? |
|---|---:|---|---|---|
| Gold synthétique sans préposition | 4 | `s027, s146, s148, s160` | bug du générateur (ligne 98) : le GP gold commence après la préposition | corriger le **gold** (+4 exacts, 0 perte) |
| Lexique disjoint synthétique — REL | 6 | `s010, s035, s061, s065, s125, s141` | le 2e verbe de la relative est hors lexique | ajouter les 7 lemmes = **tricher** sur le protocole ; 5/6 récupérés, s065 non |
| Lexique disjoint synthétique — SUB | 3 | `s044, s112, s114` | le verbe principal est hors lexique, le GN l'avale | idem ; 3/3 récupérés par le lexique |

**Total 13.** Les 9 cas synthétiques sont un artefact du vocabulaire disjoint ; les 4 GP sont
un bug de gold. Aucun n'est un échec de règle de segmentation.

### 7.2 Récupérables seulement hors périmètre ou par arbitrage — 4

| cas | id | pourquoi ce n'est pas dans R1/R2/R3 | que faudrait-il ? |
|---|---|---|---|
| Relative zéro | `r035` | pas de marqueur ; règle ad hoc pour 1 cas | une règle dédiée, coût/risque élevé |
| Couverture verbale réelle | `r255` | `achetée`/`roule` hors lexique ; le lexique est ouvert | chantier « couverture verbale », pas une règle de segmentation |
| `qu'` élidé | `r264` | `_mots` tokenise `qu'il` en un token ; il faut changer la tokenisation **et** l'adverbe final | tokeniser `qu'` comme marqueur |
| Adverbe final | `r288` | retirer la règle perd g017 (dev) | arbitrage de gold : `yesterday` vs `tomorrow` |

**Total 4.** Avec les 13 du § 7.1, on retrouve les **17 cibles non couvertes** (8 REL, 5 SUB,
4 GP) et **0 cible fausse** : `222/222` labels exacts, `222/239` cibles.

## 8. Contrôle négatif

Deux contrôles, tous deux sur les **222 labels couverts** :

| contrôle | résultat | lecture |
|---|---|---|
| permutation des cibles prédites (2 000 tirages, graine 0) | **2,011 / 222 = 0,91 %** en moyenne ; max 9 (4,05 %) ; p95 5 (2,25 %) ; observé **222 / 222 = 100 %** | le bon attachement n'est pas un hasard de fréquence : les cibles ne sont pas interchangeables |
| hasard officiel de `evaluer_gold.py` (graine 0) | **1 / 239 = 0,0042** | contrôle historique, moins informatif que la permutation |

L'audit du même commit trouve **1,81 / 196 = 0,92 %** pour la permutation sur le baseline :
nos deux contrôles sont cohérents. Le bootstrap apparié sur les 239 cibles donne un gain de
**+27 / 239 = +0,1130**, IC 95 % **[0,0753 ; 0,1548]** (5 000 rééchantillonnages) : le gain
n'est pas marginal.

## 9. Ce qui pourrait rendre ces résultats faux

1. **Le test n'est pas aveugle.** Le diagnostic des 43 (demandé) a été fait sur dev **et**
   test avant le réglage ; les règles ont ensuite été paramétrées sur dev, mais les listes
   (modaux, relatifs durs, `car`, `fall`/`call`) ont été choisies en connaissance du gold.
   Les 6 gains test sont une **confirmation**, pas une prédiction hors échantillon.
2. **Un seul split**, déterministe (`crc32`), sans validation croisée ni intervalle de
   confiance par corpus. Le test ne fait que 76 cibles (14 absentes au départ) ; un gain de 6
   est petit en valeur absolue.
3. **Le lexique `fall`/`call`** est une complétion de deux verbes anglais courants, mais elle
   est motivée par deux échecs observés. Une étude de couverture verbale plus large est
   nécessaire avant de généraliser ; le lexique français (`achetée`, `roule`) n'est pas traité.
4. **Le gold synthétique** a un bug de GP (4 cas) et un lexique disjoint (9 cas) : les 13 cas
   « non récupérables » sont des propriétés du générateur, pas du langage.
5. **La F1 0,5555 → 0,5851 est sur le gold vivant 612** ; le 0,5595 du commit est le gelé 602.
   Ne pas comparer les deux F1 sans le dire (cf. audit).
6. **L'implémentation réelle peut différer** de la copie locale (placement du garde PRON,
   ordre des tests, portée du garde DET). Les chiffres doivent être re-mesurés après
   implémentation, avec `evaluer_gold.py` et les portes.

## 10. Recommandation

1. **Implémenter R1 d'abord**, seule : +20 exacts sur tous, 0 perte, 0 nouveau label faux ;
   c'est le meilleur rapport gain/risque. Re-mesurer dev/test, committer.
2. **Puis R2** : +3 exacts, 0 perte, mais r245 devient un label faux tant que R3c n'est pas
   là. Implémenter R2 et R3c **ensemble** pour ne pas faire baisser `exact/labels`.
3. **Puis R3a/R3b/R3c** : +4 exacts en marge (r280, r153, r102, r245), 0 perte. Le garde
   DET reste **limité au GP** ; ne pas l'étendre (6.1).
4. **Corriger le gold synthétique** (ligne 98) dans un commit gold séparé : +4 exacts
   contrefactuels, 0 perte, et cela retire une fausse dette du modèle.
5. **Ne pas ajouter le lexique synthétique** : +8 exacts mais mesure invalide (protocole du
   générateur). Si le protocole est explicitement rouvert, le noter comme tel.
6. **Prochains leviers réels** : r035 (relative zéro), r255 (couverture verbale française),
   r264 (tokenisation `qu'`), r288 (portée de l'adverbe final) ; puis les 9 synthétiques si
   le protocole change.
7. **Cible attendue** après implémentation : **222 labels, 222 exacts / 222**, **222/239**
   cibles (0,9289), F1 vivant **0,5851**, dev **154/154**, test **68/68**. Rejouer
   `python3 tools/tests/linguistique/evaluer_gold.py` et `bash tools/toutes-les-portes.sh` ;
   ce rapport ne remplace pas les portes.

---

**Fichiers** : ce rapport et [`pensee-spans-v7.json`](pensee-spans-v7.json). **Aucun** autre
fichier n'a été créé ou modifié par cette session ; aucun commit n'a été fait.
