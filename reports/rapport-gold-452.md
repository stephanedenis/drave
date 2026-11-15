# W1 — le gold réel 452 : composition, split 402 / H50, sha256 et 10 candidats GP/SUB

> **Ligne de roadmap** : **R0.7** (bloc linguistique) / **B13** · **Tâche** : W1 (semaine 2, J1 matin, la part du pilote) ·
> **Date** : 2026-11-15 (J1 · 16/11) · **HEAD mesuré** : `6b2208ee` · **Verdict** : ✅ **le gold réel 452 est
> nommé et composé ; le split 402/H50 est figé ; le gold est intact ; les 10 GP/SUB sont listés pour S.**

**En trois lignes.** (1) Le gold réel fait **452** phrases = **20 hand** (`gold.json`) + **432 corpus**
(`gold_reel.json`) ; **242 fr + 210 en** ; **2 480 tokens**, **1 501 segments**, **184 cibles** d'attachement.
(2) Le split proposé est **402 / H50** : H50 = les **50 phrases dures** de C3 (2 hand + 48 corpus ; 25 fr + 25 en),
sélectionnées par score d'erreur, **sans aléa** ; la **graine 20261116** ne sert qu'au contrôle aléatoire et au
manifeste. (3) **10 GP/SUB** sans cible sont proposés à S (9 GP + 1 SUB ; **4 dans H50**) : le dénominateur
d'attachement passe de **184 à 194**. Le **sha256** du gold est identique avant/après ; aucun fichier gold n'est modifié.

**Ce que cette fiche est, et n'est pas.**

- **Est** : la composition exacte du gold réel 452, le **split 402/H50** proposé avec sa règle et sa graine,
  le **sha256 avant** (et après) du gold, la **liste des 10 GP/SUB** à annoter avec leur phrase et leur cible,
  et le **retrait du libellé « gold 200+ »** des docs.
- **N'est pas** : une annotation (le gold est à S), une modification de `gold.json`/`gold_reel.json`, une mesure
  du tagger (c'est W2), ni un nouveau gold. Les 10 cibles sont des **propositions** ; S valide ou corrige.
- **Public** : **S** (le gold), **R/B13** (R0.7), **W2** (le tagger sur 402/H50).

## 1. La composition exacte des 452

### 1.1 Par source et par langue

| source | langue | phrases | tokens | segments | cibles |
|---|---|---|---|---|---|
| hand (`gold.json`) | fr | 14 | 74 | 40 | 10 |
| hand (`gold.json`) | en | 6 | 31 | 16 | 3 |
| hand (`gold.json`) | **total** | **20** | **105** | **56** | **13** |
| corpus (`gold_reel.json`) | fr | 228 | 1258 | 759 | 86 |
| corpus (`gold_reel.json`) | en | 204 | 1117 | 686 | 85 |
| corpus (`gold_reel.json`) | **total** | **432** | **2375** | **1445** | **171** |
| — | **fr** | **242** | **1332** | **799** | **96** |
| — | **en** | **210** | **1148** | **702** | **88** |
| — | **total** | **452** | **2480** | **1501** | **184** |

**Lecture.** 20 hand = **14 fr + 6 en** ; 432 corpus = **228 fr + 204 en** ; total **242 fr + 210 en**.
Le corpus pèse **2 375 tokens** (95,8 % du gold) et **171 cibles** ; le hand pèse **105 tokens** et **13 cibles**.
Le champ `source` de `gold_reel.json` vaut `reel` ; ici, **corpus** désigne ce lot.

### 1.2 Segments et cibles par type

| type de segment | hand | corpus | total |
|---|---|---|---|
| GN | 23 | 658 | 681 |
| GV | 20 | 532 | 552 |
| GP | 10 | 71 | 81 |
| REL | 1 | 57 | 58 |
| SUB | 2 | 53 | 55 |
| ADJ | 0 | 35 | 35 |
| ADV | 0 | 30 | 30 |
| PONCT | 0 | 9 | 9 |
| **total** | **56** | **1445** | **1501** |

| type de cible | hand | corpus | total |
|---|---|---|---|
| GP | 10 | 62 | 72 |
| REL | 1 | 57 | 58 |
| SUB | 2 | 52 | 54 |
| **total** | **13** | **171** | **184** |

**Les cibles sont saturées sur GP/REL/SUB, pas sur GN/GV.** 184 cibles = **GP 72 + REL 58 + SUB 54**.
Il reste **10 segments GP/SUB sans cible** (9 GP + 1 SUB) : ce sont exactement les 10 candidats du § 4.
Les **1 233 GN/GV** n'ont pas de cible ; les annoter est une deuxième vague facultative, pas ce lot.

## 2. Le split 402 / H50

### 2.1 La règle déterministe

Le split n'est **pas** un tirage au hasard : H50 est le **lot dur** de C3, sélectionné sur les erreurs de
l'heuristique. La règle est déterministe et reproductible :

```text
score(p) = 3 × |cibles d'attachement évaluées absentes ou fausses|
         + 2 × |tokens POS faux|
         + 1 × |segments gold absents|
```

1. Calculer le score sur les **452** phrases, au HEAD `6b2208ee`, avec `bloc_linguistique.Heuristique`.
   Les 10 segments **sans cible gold** ne comptent pas dans le premier terme : ils ne sont pas évalués.
2. Pour chaque langue (`fr`, `en`), trier par **score décroissant**, puis par **id croissant**.
3. Prendre gloutonnement, avec **au plus 2 phrases par signature d'erreur** — la signature est
   `(langue, couples (POS gold, POS prédit), types de segments absents, couples (type, erreur) d'attachement)`.
4. Quota **25 fr + 25 en** ; si le plafond bloque, compléter par rang.
5. `H50` = les 50 prises ; `402` = les 452 − H50. Aucun aléa, aucun doublon.

**La graine.** La graine est **`20261116`**. Elle ne sert **pas** à tirer H50 : elle fixe le **contrôle
négatif** (tirage stratifié 24+1 fr / 24+1 en) et le **manifeste** du split. Un tirage au hasard avec cette
graine donne **88,13 %** de POS, contre **68,42 %** pour H50 : c'est la preuve que H50 est un stress test,
pas un échantillon. Si S exige un split aléatoire, le tirage `20261116` est fourni dans le JSON ; il n'est
**pas** retenu comme H50.

### 2.2 La partition

| base | phrases | hand | corpus | fr | en | tokens | segments | cibles |
|---|---|---|---|---|---|---|---|---|
| **H50** | 50 | 2 | 48 | 25 | 25 | 323 | 190 | 22 |
| **402** | 402 | 18 | 384 | 217 | 185 | 2157 | 1311 | 162 |
| **total** | 452 | 20 | 432 | 242 | 210 | 2480 | 1501 | 184 |

**Partition vérifiée** : H50 ∩ 402 = **0**, H50 ∪ 402 = **452**, aucun id dupliqué. Le manifeste
`sha256` des 50 ids triés est `1615c17a97bb998451de66585dadcea0643ba1d7f8d962ccbdf28a13b575d970`.

### 2.3 Les 50 phrases de H50

Les 50 sont listées ci-dessous, groupées par langue ; le JSON porte les mêmes champs et les ids du 402.

**FR — 25 phrases**

| # | id | src | score | phrase |
|---|---|---|---|---|
| 1 | `g004` | hand | 6 | Il a couru pour attraper le bus. |
| 2 | `r091` | corpus | 7 | Le médecin soigne les malades. |
| 3 | `r203` | corpus | 8 | Le livre que j'ai lu est bon. |
| 4 | `r210` | corpus | 6 | Bien qu'il soit tard, il travaille. |
| 5 | `r225` | corpus | 6 | Je crois qu'il a raison. |
| 6 | `r227` | corpus | 6 | Pendant qu'il dort, elle lit. |
| 7 | `r255` | corpus | 8 | La voiture que j'ai achetée roule. |
| 8 | `r260` | corpus | 6 | Bien qu'il pleuve, il sort. |
| 9 | `r261` | corpus | 8 | La table que nous avons prise est grande. |
| 10 | `r262` | corpus | 6 | Pendant qu'elle dort, il travaille. |
| 11 | `r266` | corpus | 6 | Elle pleure parce qu'elle est seule. |
| 12 | `r272` | corpus | 6 | Elle dit qu'elle part. |
| 13 | `r304` | corpus | 7 | Viens-tu demain ? |
| 14 | `r309` | corpus | 7 | Peut-être qu'il viendra. |
| 15 | `r324` | corpus | 6 | Le livre est sur la table ; il est rouge. |
| 16 | `r331` | corpus | 8 | Les enfants aiment les fleurs ; ils les cueillent. |
| 17 | `r339` | corpus | 10 | Marie lit un livre ; elle le ferme ; elle le pose. |
| 18 | `r343` | corpus | 6 | Paul voit Marie ; il lui parle ; elle lui répond. |
| 19 | `r346` | corpus | 8 | Le chien poursuit le chat ; il l'attrape. |
| 20 | `r347` | corpus | 6 | Sophie regarde Paul ; elle lui sourit. |
| 21 | `r349` | corpus | 10 | Le livre est sur la table ; je le lis. |
| 22 | `r357` | corpus | 7 | Paul écrit une lettre ; il l'envoie. |
| 23 | `r408` | corpus | 8 | Ne viens-tu pas demain ? |
| 24 | `r409` | corpus | 9 | Ne mange-t-il pas ? |
| 25 | `r410` | corpus | 7 | Ne dort-elle pas ? |

**EN — 25 phrases**

| # | id | src | score | phrase |
|---|---|---|---|---|
| 1 | `g017` | hand | 4 | She said that she would come yesterday. |
| 2 | `r034` | corpus | 4 | The book that I read is exciting. |
| 3 | `r071` | corpus | 3 | The car drives fast. |
| 4 | `r076` | corpus | 3 | They arrive tomorrow morning. |
| 5 | `r102` | corpus | 4 | The rain falls since this morning. |
| 6 | `r104` | corpus | 4 | We prepare dinner. |
| 7 | `r106` | corpus | 4 | The children laugh loudly. |
| 8 | `r119` | corpus | 5 | The tourists visit the museum. |
| 9 | `r159` | corpus | 4 | The farmers grow wheat. |
| 10 | `r163` | corpus | 5 | The students review their lessons. |
| 11 | `r179` | corpus | 7 | The rain washes the streets. |
| 12 | `r217` | corpus | 4 | The student whom I mention is absent. |
| 13 | `r241` | corpus | 4 | The day when we left was beautiful. |
| 14 | `r246` | corpus | 6 | The dog that barks is mean. |
| 15 | `r285` | corpus | 4 | The table that we took is big. |
| 16 | `r287` | corpus | 6 | The bird that flies is blue. |
| 17 | `r291` | corpus | 6 | The book that is on the table is mine. |
| 18 | `r293` | corpus | 4 | The person whom I mention is here. |
| 19 | `r328` | corpus | 6 | The book is on the table; it is red. |
| 20 | `r362` | corpus | 4 | The car is red; it runs fast. |
| 21 | `r363` | corpus | 5 | The book is on the table; I read it. |
| 22 | `r366` | corpus | 4 | The rain falls; it wets the ground. |
| 23 | `r368` | corpus | 5 | Marie and Paul dance; they have fun. |
| 24 | `r370` | corpus | 4 | The house is old; it still stands. |
| 25 | `r422` | corpus | 7 | You don't come tomorrow? |

**Composition de H50** : **2 hand** (`g004`, `g017`) + **48 corpus** ; **25 fr + 25 en** ; **323 tokens**,
**190 segments**, **22 cibles**. H50 fait **11,1 %** des phrases mais porte **37,1 %** des erreurs POS
(102/275), **25,1 %** des segments absents (87/346) et **100 %** de l'erreur d'attachement (1/1).

### 2.4 La mesure du split

Les chiffres sont recalculés au HEAD `6b2208ee` et **identiques à C3** :

| mesure | H50 | 402 | tirage graine 20261116 |
|---|---|---|---|
| POS (tokens) | 68,42 | 91,98 | 88,13 |
| POS hors tokenisation | 75,68 | 93,50 | 91,42 |
| F1 syntagmes | 58,36 | 81,90 | 78,69 |
| attachement | 95,45 (21/22) | 100,00 (162/162) | 100,00 (23/23) |
| tokens | 323 | 2157 | 278 |

**Contrôle négatif** : le tirage aléatoire de la graine `20261116` est **au-dessus** de H50 sur les trois
niveaux (POS, F1, attachement) ; H50 est donc bien un lot **dur**, pas un échantillon représentatif.
L'attachement de H50 ne vaut que **21/22** : la seule erreur est `g017`, une erreur de **span**, pas de cible.

### 2.5 Ce que le split n'est pas
- **Pas une généralisation** : H50 est sélectionné sur les erreurs de l'heuristique ; il est circulaire.
- **Pas un partage de cibles** : 4 candidats sont dans H50, 6 dans 402. Si S les annote, H50 passe de
  **22 à 26** cibles et 402 de **162 à 168** ; le total de **184 à 194**.
- **Pas encore un test** : H50 devient un test quand S a validé les 50 phrases et les 4 cibles de H50.

## 3. Le sha256 du gold

Le gold est **lu deux fois** ; aucun fichier n'est écrit. Les deux empreintes sont identiques avant/après :

| fichier | octets | sha256 |
|---|---|---|
| `tools/tests/linguistique/gold.json` | 20 009 | `3663be6cea2f22e2166df9a2ab6b7c459ff7806cf72d238263b1423ac4e2e58a` |
| `tools/tests/linguistique/gold_reel.json` | 470 149 | `05d4f6dfae67dc72b714dbef69e8764a811247bc72c31b103bad9603be11ff11` |
| **concaténation ordonnée** (`gold.json` puis `gold_reel.json`) | 490 158 | `cff6b6d703546ad5992c5ada4fc99e1bdaa8e76e9cd089bd3e3b88bd71e90ac5` |

**Avant = après** ; `git diff -- tools/tests/linguistique/gold.json tools/tests/linguistique/gold_reel.json`
est **vide**. La commande de contrôle est :

```bash
sha256sum tools/tests/linguistique/gold.json tools/tests/linguistique/gold_reel.json
```

## 4. Les 10 GP/SUB candidats à annoter

**Principe.** Le gold ne s'étend pas par des phrases (elles y sont déjà) mais par des **cibles
d'attachement**. Les **10 segments GP/SUB sans cible** sont les seuls spans non attachés ; ils sont
listés ci-dessous avec leur phrase et la **cible proposée**. La convention est celle de `gold_reel.py` :
**GP → verbe gouverneur (GV)**, ou nom complété pour un génitif ; **SUB → verbe gouverneur (GV)** ;
**REL → antécédent**. La cible est une **proposition** : S valide ou corrige.

| # | id | lg | type | span | phrase | cible proposée | H50 | double codage |
|---|---|---|---|---|---|---|---|---|
| 1 | `r267` | fr | GP | à moi (34–39) | Le livre qui est sur la table est à moi. | est (30–33), GV | non | non |
| 2 | `r324` | fr | GP | sur la table (13–25) | Le livre est sur la table ; il est rouge. | est (9–12), GV | oui | oui |
| 3 | `r328` | en | GP | on the table (12–24) | The book is on the table; it is red. | is (9–11), GV | oui | oui |
| 4 | `r336` | en | GP | to her (27–33) | Paul sees Marie; he speaks to her. | speaks (20–26), GV | non | non |
| 5 | `r342` | en | GP | to her (27–33) | Paul sees Marie; he speaks to her; she listens. | speaks (20–26), GV | non | non |
| 6 | `r349` | fr | GP | sur la table (13–25) | Le livre est sur la table ; je le lis. | est (9–12), GV | oui | oui |
| 7 | `r358` | en | GP | to her (27–33) | Paul sees Marie; he speaks to her. | speaks (20–26), GV | non | non |
| 8 | `r363` | en | GP | on the table (12–24) | The book is on the table; I read it. | is (9–11), GV | oui | oui |
| 9 | `r367` | en | GP | to him (40–46) | The teacher speaks; the students listen to him. | listen (33–39), GV | non | non |
| 10 | `r429` | fr | SUB | que c'est vrai (7–21) | On dit que c'est vrai. | dit (3–6), GV | non | non |

**Effet de l'annotation.** Les 10 candidats sont **9 GP + 1 SUB** ; 4 sont dans H50, 6 dans 402.

| base | cibles avant | candidats | cibles après |
|---|---|---|---|
| H50 | 22 | 4 | 26 |
| 402 | 162 | 6 | 168 |
| **total** | **184** | **10** | **194** |

Par type : **GP 72 → 81**, **REL 58 → 58**, **SUB 54 → 55**. Après annotation, **tous les GP et SUB**
du gold ont une cible ; les REL l'avaient déjà.

**Ce que S doit trancher.**
- La famille **« sur la table » / « on the table »** (4 phrases : `r324`, `r328`, `r349`, `r363`) :
  le GP se rattache-t-il au **nom** (`livre`, `book`) ou au **verbe** (`est`, `is`) ? La convention
  proposée est le **verbe** ; c'est le cas le plus utile à trancher.
- `r267` « à moi » : deux `est` dans la phrase ; la cible proposée est le **second** (GV 30–33).
- `r429` « que c'est vrai » : SUB complétive, cible `dit` (GV 3–6).
- **Double codage 4/10** : les 4 de H50 (`r324`, `r328`, `r349`, `r363`) sont proposés au double codage.
- **Ordre** : annoter les 4 de H50 **avant** la mesure W2, sinon le dénominateur de H50 change après la mesure.

**Détail des cibles.**

- `r267` (GP, fr) — « Le livre qui est sur la table est à moi. » : `à moi` → **est** (30–33, GV). GP prédicatif ; deux `est` dans la phrase, la cible est le second (GV 30–33, AUX au POS gold).
- `r324` (GP, fr) — « Le livre est sur la table ; il est rouge. » : `sur la table` → **est** (9–12, GV). Famille « sur la table » : ambiguïté nom `livre` / verbe `est` ; la convention retient le verbe.
- `r328` (GP, en) — « The book is on the table; it is red. » : `on the table` → **is** (9–11, GV). Famille « on the table » : ambiguïté nom `book` / verbe `is` ; la convention retient le verbe.
- `r336` (GP, en) — « Paul sees Marie; he speaks to her. » : `to her` → **speaks** (20–26, GV). GP datif ; cible = le verbe `speaks`.
- `r342` (GP, en) — « Paul sees Marie; he speaks to her; she listens. » : `to her` → **speaks** (20–26, GV). GP datif ; cible = le verbe `speaks`.
- `r349` (GP, fr) — « Le livre est sur la table ; je le lis. » : `sur la table` → **est** (9–12, GV). Famille « sur la table » ; cible = le verbe `est`.
- `r358` (GP, en) — « Paul sees Marie; he speaks to her. » : `to her` → **speaks** (20–26, GV). GP datif ; cible = le verbe `speaks`.
- `r363` (GP, en) — « The book is on the table; I read it. » : `on the table` → **is** (9–11, GV). Famille « on the table » ; cible = le verbe `is`.
- `r367` (GP, en) — « The teacher speaks; the students listen to him. » : `to him` → **listen** (33–39, GV). GP datif ; cible = le verbe `listen`.
- `r429` (SUB, fr) — « On dit que c'est vrai. » : `que c'est vrai` → **dit** (3–6, GV). SUB complétive ; cible = le verbe `dit`.

## 5. Le retrait de « gold 200+ » des docs

Le libellé **« gold 200+ »** est retiré des docs ; il recouvrait deux objets différents, désormais nommés :

| objet | nom retenu | occurrences |
|---|---|---:|
| gold linguistique réel | **gold réel 452** (20 hand + 432 corpus) | 3 |
| gold de pensée de B13 | **gold de pensée (B13)** (noté `gold B13` dans la roadmap) | 12 |
| archive de la semaine 1 | **gold réel 452** (corrigé sans réécrire l'histoire) | 1 |
| mentions de la consigne (semaine 2) | **l'ancien nom / l'ancien libellé** | 2 |
| **total** | | **18** |

| fichier | avant | après | remplacement |
|---|---|---|---|
| `docs/pilotage/chantiers.md` | 3 | 0 | gold réel 452 (L) ; gold de pensée (B13) |
| `docs/pilotage/en-cours.md` | 3 | 0 | gold de pensée (B13) |
| `docs/pilotage/plan-travail.md` | 4 | 0 | gold de pensée (B13) |
| `docs/pilotage/roadmap.md` | 3 | 0 | gold B13 (pensée) |
| `docs/pilotage/semaine-2.md` | 2 | 0 | l'ancien nom ; l'ancien libellé |
| `docs/pilotage/semaine-autonome.md` | 1 | 0 | gold réel 452 (archive corrigée) |
| `docs/produit/README.md` | 2 | 0 | gold réel 452 |

**Vérification** : `0` ligne contenant `200+` dans `docs/**/*.md` (18 occurrences `gold 200+` avant,
0 après). Les occurrences **B13** ne sont **pas** devenues « gold réel 452 » : elles désignent le gold de
pensée (RSN/opérateurs), un autre objet. Les occurrences **linguistiques** et le produit deviennent
« gold réel 452 ».

## 6. Contrôles négatifs

| contrôle | attente | résultat |
|---|---|---|
| partition | H50 ∩ 402 = 0 ; union = 452 | **0 / 452** |
| reproduction | recalcul au HEAD `6b2208ee` = C3 | **50/50 ids, 50/50 scores, Jaccard 1,0** |
| hash | avant = après | **oui**, `git diff` vide |
| tirage aléatoire | H50 doit être sous le hasard | **68,42 % vs 88,13 %** (POS) |
| candidats | 10 spans, 0 cible | **10** (9 GP + 1 SUB), **4 dans H50** |
| docs | 0 « 200+ » | **0** |

## 7. Ce qui pourrait rendre ce résultat faux

- Une écriture dans gold.json ou gold_reel.json (le sha256 changerait, le split serait périmé).
- Un changement de l'heuristique ou de la tokenisation après le 2026-11-15 : les scores, donc H50, changent.
- Un changement de la signature d'erreur, du plafond 2 ou du quota 25.
- Une renumérotation des ids ou une collision d'id.
- Une annotation des 4 cibles de H50 après la mesure W2 (le test serait contaminé).
- Une convention d'attachement différente (GP au nom plutôt qu'au verbe).

## 8. Fichiers et reproduction

- **Cette fiche** : [`reports/rapport-gold-452.md`](rapport-gold-452.md).
- **JSON** : [`reports/rapport-gold-452.json`](rapport-gold-452.json) — composition, sha256, split, 50 phrases,
  10 candidats, contrôles.
- **Lus, non modifiés** : `tools/tests/linguistique/gold.json`, `tools/tests/linguistique/gold_reel.json`,
  `tools/bloc_linguistique.py`.
- **Sélection H50** : [`tools/tests/linguistique/gold_reel_50.py`](../tools/tests/linguistique/gold_reel_50.py)
  (lecture seule ; c'est le script de C3). Le split est figé par `h50_ids` dans le JSON.
- **Docs modifiés** : `chantiers.md`, `en-cours.md`, `plan-travail.md`, `roadmap.md`, `semaine-2.md`,
  `semaine-autonome.md`, `produit/README.md`.

**Reproduire la sélection H50** :

```bash
python3 tools/tests/linguistique/gold_reel_50.py --sortie /tmp/c3.json
# puis comparer les 50 ids à reports/rapport-gold-452.json (champ split.h50_ids)
```

**Vérifier le split** :

```bash
python3 - <<'PY'
import json
d = json.load(open('reports/rapport-gold-452.json'))
h = set(d['split']['h50_ids']); r = set(d['split']['reste_402_ids'])
assert len(h) == 50 and len(r) == 402 and not (h & r) and len(h | r) == 452
print('SPLIT-OK', len(h), len(r))
PY
```

## 9. La décision et la suite

1. **S valide ou corrige** les 10 cibles (priorité 1) et les 50 phrases de H50 ; le pilote ne touche pas
   au gold. Le **double codage** porte sur les 4 de H50.
2. **W2** mesure le tagger sur **402** (l'entraînement) et **H50** (la tenue à l'écart) ; une règle qui ne
   gagne que sur H50 est **rejetée**. Le contrôle est la non-régression du 402, pas le gain sur H50.
3. **Ne pas ajouter 50 phrases** : les 50 sont déjà dans le gold ; ce qui manque est leur **statut de test**
   et **10 cibles**, pas du volume.
4. **Ne pas rouvrir** le libellé « gold 200+ » : le nom est remplacé par **gold réel 452**, **lot dur H50**
   et **cibles 184 → 194**.
