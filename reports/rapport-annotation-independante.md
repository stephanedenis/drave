# Contrôle indépendant de la convention d'attachement — 20 segments annotés à la main

**Date** 2026-11-05 · **Branche** `s/v7` · **HEAD** `e1171032` · **Graine** `20261105` · **Statut** contrôle
externe ; aucun fichier existant modifié **par moi** ; aucun commit.

**Deux versions du bloc, pinées.** La mesure aveugle porte sur `HEAD e1171032`,
`tools/bloc_linguistique.py` sha256 `d9c9d559…`. Pendant la rédaction, le fichier de travail a changé
(correctif `SUB`) : j'ai copié le snapshot à 13:51:26, sha256 `6e843018…`, et je le mesure à part. Les
tableaux des § 2, 3.1 et 3.2 sont la mesure aveugle ; la § 3.3 est une re-exécution **post-hoc**, pas un
résultat aveugle. La doc `gold_reel.py` a aussi changé pendant la session : `CONVENTION_CIBLE["SUB"]`
est passée de « antécédent » à « verbe gouverneur (69/69 cibles VERB) » ; la mesure aveugle reste celle de
HEAD, la correction est citée et validée à part.

## Verdict

| mesure | accord | IC95 Wilson |
|---|---:|---:|
| **moi ↔ gold**, cible top-1 | **20/20 = 100 %** | 83,9–100 % |
| moi ↔ gold, sans `r057` (cas non aveugle) | 19/19 = 100 % | 83,2–100 % |
| **moi ↔ bloc HEAD**, strict (même type + span) | **10/20 = 50 %** | 29,9–70,1 % |
| moi ↔ bloc HEAD, cible d'attachement seule | **17/20 = 85 %** | 64,0–94,8 % |
| moi ↔ bloc post-correctif, strict | 11/20 = 55 % | 34,2–74,2 % |
| moi ↔ bloc post-correctif, attachement seul | 18/20 = 90 % | 69,9–97,2 % |

1. **La convention est reconstructible** : 20/20 sur le gold, avec 9 SUB, 7 GP et 4 REL. Elle n'est pas le
   hasard (0,77 %).
2. **La ligne `SUB` de `CONVENTION_CIBLE` (version mesurée) était fausse** : 69/69 cibles SUB sont des verbes (POS gold), jamais
   un antécédent nominal. C'est le seul écart de convention franc de l'échantillon (`s052`).
3. **Le bloc mesuré à l'aveugle a la bonne cible dans 17/20** ; ses 10 désaccords stricts sont 7 fois des
   erreurs de span/type (3 REL trop longues, 4 segments typés `GN`) et 3 fois de vraies cibles fausses
   (`r293`, `s052`, `r230`). Au span exact, il est juste **10/12 = 83,3 %**, cohérent avec le gold entier
   (**123/145 = 84,8 %**).
4. **Le correctif SUB appliqué pendant la session marche** : sur le snapshot, `s052` → `ouvre`, strict
   **11/20**, attachement **18/20** ; sur tout le gold **137/145 = 94,5 %** (contre 123/145) et les échecs
   SUB au span exact tombent de **8 à 2** (`r230`, `r309`). La couverture (145/239) ne bouge pas ; la doc a
   été corrigée dans le même sens pendant la session (voir § 3.3), et le contrôle valide la formulation
   (69/69).
5. **Le split `attachement.verbe` / `.nom` est faux** : `_est_verbe` compte 53 verbes comme noms sur les
   145 labels (HEAD), encore 45 après le correctif. À corriger avant de lire ce split.

## 1. Dispositif

- **Population** : `charger()` → 612 phrases, 1 863 segments, **239 segments avec cible** : **96 GP,
  69 SUB, 74 REL** ; **171 reel, 55 synthétique, 13 hand**.
- **Tirage** : énumération des 239 couples (phrase, segment) avec cible ; `random.seed(20261105);
  random.sample(cas, 20)`. Rangs 0-based : `25, 32, 38, 43, 76, 105, 108, 116, 154, 157, 162, 169, 174,
  191, 194, 201, 202, 204, 215, 222`. Échantillon : **7 GP, 9 SUB, 4 REL** ; **13 reel, 7 synthétique,
  0 hand**.
- **Aveuglement** : le script d'extraction supprime les clés `cible`/`cibles` (assertion sur le JSON
  produit) ; il ne laisse que la phrase, les tokens/POS gold, et les spans/rôles des segments. Les 20
  annotations ont été écrites sur disque **avant** la comparaison et avant tout appel au bloc. Après le
  gel, un simple contrôle de format du bloc sur le cas 1 (`r047`) a été exécuté ; il n'a pas modifié les
  annotations.
- **Annotation** : `REL` → antécédent (tête du GN à gauche) ; `GP` → verbe gouverneur (ou nom complété) ;
  `SUB` → la convention dit « antécédent », mais aucune des 9 SUB n'est une relative : 4 sont antéposées
  sans GN à gauche, 5 suivent un GV ; je choisis le **verbe gouverneur** (complétive) ou le **verbe de la
  principale** (circonstancielle antéposée), et je note l'ambiguïté.
- **Comparaison** : gold `cibles[0]` (et appartenance à `cibles`) ; bloc
  `Heuristique().analyser(...).etiquettes` → `meta.attachement.cible`, d'abord même **type + span**, puis
  **même type couvrant** (« tête »), puis **tout type couvrant**.
- **Une fuite assumée** : `r057` a sa cible (`aboie`) visible dans un extrait de `gold_reel.py` lu avant le
  tirage, pendant le repérage de la convention. Sensibilité sans ce cas : 19/19 ; le retirer ne change pas
  le verdict.

## 2. Les 20 cas (mesure aveugle, HEAD `d9c9d559`)

| # | id | phrase | type | segment | moi | gold | bloc | verdict |
|---:|---|---|---|---|---|---|---|---|
| 1 | `r047` | Les fleurs poussent dans le jardin. | GP | dans le jardin | `poussent` | `poussent` (+ `fleurs`) | `poussent` | ✅ |
| 2 | `s061` | ce nuage qui saute observe | REL | qui saute | `nuage` | `nuage` | `nuage` *(REL +)* | ◐ |
| 3 | `r293` | The person whom I mention is here. | REL | whom I mention | `person` | `person` | `here` *(GN)* | ❌ |
| 4 | `s052` | cette ancienne cuisine ouvre que un sombre village trouve | SUB | que un sombre village trouve | `ouvre` | `ouvre` | `cuisine` | ❌ |
| 5 | `r057` | Le chien aboie contre le facteur. | GP | contre le facteur | `aboie` | `aboie` | `aboie` | ✅ |
| 6 | `s089` | la étoile commence sur ce jardin | GP | sur ce jardin | `commence` | `commence` (+ `étoile`) | `commence` | ✅ |
| 7 | `r270` | Quand tu veux, nous partons. | SUB | Quand tu veux | `partons` | `partons` | `partons` | ✅ |
| 8 | `r031` | The train leaves at noon. | GP | at noon | `leaves` | `leaves` | `leaves` | ✅ |
| 9 | `r219` | I know that you come. | SUB | that you come | `know` | `know` | `know` *(GN)* | ◐ |
| 10 | `r274` | Bien que je sois fatigué, je continue. | SUB | Bien que je sois fatigué | `continue` | `continue` | `continue` | ✅ |
| 11 | `r281` | He says that it rains. | SUB | that it rains | `says` | `says` | `says` *(GN)* | ◐ |
| 12 | `r067` | The flowers grow in the garden. | GP | in the garden | `grow` | `grow` (+ `flowers`) | `grow` | ✅ |
| 13 | `r222` | Si tu viens, nous partirons. | SUB | Si tu viens | `partirons` | `partirons` | `partirons` | ✅ |
| 14 | `s115` | la secrète fenêtre qui observe ferme | REL | qui observe | `fenêtre` | `fenêtre` | `fenêtre` *(REL +)* | ◐ |
| 15 | `r160` | The postman passes in the morning. | GP | in the morning | `passes` | `passes` | `passes` | ✅ |
| 16 | `r288` | I know that he comes tomorrow. | SUB | that he comes tomorrow | `know` | `know` | `know` *(GN)* | ◐ |
| 17 | `s027` | mon sombre village marche avec il | GP | il | `marche` | `marche` (+ `village`) | `marche` *(GN)* | ◐ |
| 18 | `s035` | un papier qui ferme observe | REL | qui ferme | `papier` | `papier` | `papier` *(REL +)* | ◐ |
| 19 | `r230` | Quand tu arrives, appelle-moi. | SUB | Quand tu arrives | `appelle` | `appelle` | `appelle-moi` | ❌ |
| 20 | `s054` | elle trouve que une rapide rivière écoute | SUB | que une rapide rivière écoute | `trouve` | `trouve` | `trouve` | ✅ |

Légende : `moi` = mon annotation ; `gold` = `cibles[0]` (entre parenthèses, les alternatives que le gold
accepte) ; `bloc` = cible du bloc au même type+span, ou sur le segment couvrant. ✅ accord strict ;
◐ cible juste mais span ou type faux ; ❌ cible fausse. `(GN)` = segment couvrant typé `GN` ;
`(REL +)` = span `REL` plus long que le gold.

## 3. Accords et désaccords

### 3.1 Les 10 désaccords stricts avec HEAD

| # | id | bloc | cause du désaccord | catégorie | verdict |
|---:|---|---|---|---|---|
| 2 | `s061` | `nuage` *(REL +)* | span REL = « qui saute observe » | découpage | ◐ |
| 3 | `r293` | `here` *(GN)* | pas de REL ; GN « The person whom I mention » → `here` | découpage + cible | ❌ |
| 4 | `s052` | `cuisine` | règle littérale « GN à gauche » → sujet `cuisine` | convention (SUB) | ❌ |
| 9 | `r219` | `know` *(GN)* | span exact mais type `GN` au lieu de `SUB` | typologie | ◐ |
| 11 | `r281` | `says` *(GN)* | span exact mais type `GN` au lieu de `SUB` | typologie | ◐ |
| 14 | `s115` | `fenêtre` *(REL +)* | span REL = « qui observe ferme » | découpage | ◐ |
| 16 | `r288` | `know` *(GN)* | span exact mais type `GN` au lieu de `SUB` | typologie | ◐ |
| 17 | `s027` | `marche` *(GN)* | span exact mais type `GN` au lieu de `GP` | typologie | ◐ |
| 18 | `s035` | `papier` *(REL +)* | span REL = « qui ferme observe » | découpage | ◐ |
| 19 | `r230` | `appelle-moi` | cible `appelle-moi` (GV entier) au lieu du verbe `appelle` | cible | ❌ |

Bilan : **7 ◐** (3 découpage REL, 4 typologie) + **3 ❌** (1 découpage sans cible, 2 cibles fausses). **17/20** si
l'on demande seulement « la bonne cible d'attachement a-t-elle été choisie ? ».

### 3.2 Par type (HEAD)

| type | n | span exact | cible juste au span | juste via tête | juste via type ignoré | cible fausse |
|---|---:|---:|---:|---:|---:|---:|
| GP | 7 | 6 | 6 | 0 | 1 | 0 |
| SUB | 9 | 6 | 4 | 0 | 3 | 2 |
| REL | 4 | 0 | 0 | 3 | 0 | 1 |
| **total** | **20** | **12** | **10** | **3** | **4** | **3** |

Le span exact (12/20 = 60 %) et la justesse au span exact (10/12 = 83,3 %) sont dans la même zone que le
gold entier : **145/239 = 60,7 %** de spans exacts et **123/145 = 84,8 %** de cibles justes au span exact.
L'échantillon n'est pas atypique — mais il est petit.

### 3.3 Après le correctif SUB (post-hoc, snapshot `6e843018`)

Le fichier de travail a changé pendant la session : la cible d'un SUB est désormais le verbe quand le
segment précédent est un GV, l'antécédent quand c'est un GN. J'ai copié le fichier à 13:51:26 et mesuré
cette copie (hash identique au live au moment de la mesure ; il peut encore bouger).

| version | hash | strict | tête | attachement seul | cible fausse | global juste / labels | GP | SUB | REL |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| HEAD `e1171032` (aveugle) | `d9c9d559` | 10/20 | 13/20 | 17/20 | 3 | 123/145 = 84,8 % | 69/83 | 28/36 | 26/26 |
| snapshot 13:51:26 | `6e843018` | **11/20** | 14/20 | **18/20** | **2** | **137/145 = 94,5 %** | 77/83 | 34/36 | 26/26 |

- Seul changement de cible sur les 20 : `s052` `cuisine` → `ouvre` (le cas de la § 4.1).
- Restent faux : `r293` (`here` au lieu de `person`, REL non reconnue) et `r230` (`appelle-moi` au lieu de
  `appelle`, GV entier).
- Les 7 autres désaccords (spans REL, types `GN`) sont inchangés : la couverture reste **145/239** et le
  correctif ne touche que la cible, pas le découpage.
- Échecs SUB au span exact : **8 → 2** ; les 6 échecs « GN à gauche » (`s012`, `s030`, `s052`, `s097`,
  `s124`, `s139`) disparaissent ; il reste `r230` et `r309` (`Peut-être` au lieu de `viendra`).
- **La doc a été corrigée pendant la session** : `CONVENTION_CIBLE["SUB"]` est passé de « antécédent
  (tête du GN à gauche) » à « verbe gouverneur (69/69 cibles sont des VERB au POS gold) », et `REL` à
  « antécédent ... quand le segment précédent est un GN ». C'est la formulation que les données soutiennent ;
  la mesure aveugle, elle, a été faite sur l'ancienne ligne. Le split `_est_verbe` reste, lui, à corriger.

## 4. Où la convention était ambiguë (et où la doc se trompait)

### 4.1 `SUB` : « antécédent » contredit par 69/69 cibles

`CONVENTION_CIBLE` disait, dans la version mesurée (HEAD) :

> `REL / SUB` : la cible est l'**antécédent** — la tête nominale du GN à gauche.

C'était vrai pour l'essentiel de `REL` (73 noms + 1 pronom sur 74). C'était **faux pour `SUB`** :

- **69/69** premières cibles `SUB` ont le POS **`VERB`** dans le gold ; **0** sont des noms ;
- dans l'échantillon, **9/9** SUB ciblent un verbe, y compris **4 SUB antéposées sans aucun GN à gauche**
  (`r270` → `partons`, `r274` → `continue`, `r222` → `partirons`, `r230` → `appelle`) ;
- le bloc appliquait la lettre : sur les **36** SUB qu'il segmente au span exact, **8** cibles étaient
  fausses, et **6** l'étaient parce qu'il prenait la tête du GN de gauche au lieu du verbe gouverneur :
  `s012` (`étoile` au lieu de `écoute`), `s030` (`lettre` au lieu de `cherche`), `s052` (`cuisine` au lieu
  de `ouvre`), `s097` (`chanson` au lieu de `commence`), `s124` (`fenêtre` au lieu de `commence`), `s139`
  (`lettre` au lieu de `crie`). Les deux autres : `r230` (`appelle-moi` au lieu de `appelle`) et `r309`
  (`Peut-être` au lieu de `viendra`).
- La roadmap ne mentionne d'ailleurs que « REL → antécédent, GP → verbe » ; la ligne SUB était la plus
  gravement contredite par les données.

**Correction (appliquée dans le fichier de travail pendant la session)** : `SUB` → « verbe gouverneur
(69/69 cibles VERB) » dans `CONVENTION_CIBLE` ; la formulation complète serait « verbe gouverneur
(complétive) ou verbe de la principale (circonstancielle antéposée) ; l'antécédent nominal n'est pas
observé dans le gold ». Côté bloc, le correctif déjà appliqué va dans ce sens ; la doc est alignée dans le
fichier de travail, pas encore forcément committée.

### 4.2 `GP` : quatre adjectifs gouverneurs, et 43 multi-cibles

La doc (toujours en vigueur pour `GP`) dit « verbe gouverneur, ou nom complété pour un génitif ». Le gold a aussi **4 GP à gouverneur
adjectival** : `g012` « Le canard est prêt à manger » → `prêt`, `g020`, `r018`, `r038`. Et **2 génitifs**
nominaux (`g002` « de la voisine » → `chat`, `g006`). La doc est incomplète pour l'adjectif.

Surtout, **43/96 GP** du gold déclarent **deux cibles** `[gouverneur, cible nominale]` (41 noms, 1 « l'homme »,
1 pronom) : `r047`
`["poussent", "fleurs"]`, `g012` `["prêt", "canard"]`, etc. Or `evaluer_gold` ne compare qu'à `cibles[0]` :
choisir l'alternative nominale est compté faux alors que le gold la déclare acceptable. Dans l'échantillon,
4 GP sont multi-cibles (cas 1, 6, 12, 17) ; j'ai toujours choisi la première (le verbe) et le bloc aussi,
donc aucun effet ici — mais la métrique est plus stricte que le gold.

### 4.3 `REL` : l'antécédent est clair, le span est fragile

74 REL : 73 noms + 1 pronom (`s065` « elle qui commence nage » → `elle`). Le bloc ne segmente au span exact
que **26/74** REL (35,1 %), mais quand il le fait, la cible est juste **26/26**. Dans l'échantillon,
**0/4** spans REL exacts : le bloc absorbe le verbe principal (`qui saute observe`, `qui observe ferme`,
`qui ferme observe`). Ce n'est pas une ambiguïté de convention, c'est un problème de découpage — mais il
coûte 3 des 10 désaccords.

### 4.4 Cas `s027` : un GP synthetique hors convention

« mon sombre village marche avec il » : le gold marque `GP` sur `il` seul, avec `avec` dans le `GV` ; le
bloc marque `GP` sur `avec il` et `GN` sur `il`. La cible est la même (`marche`). La convention n'a pas de
règle pour un complément pronominal ; cas à ne pas surinterpréter.

### 4.5 Le split `attachement.verbe` / `.nom` est faux

`evaluer_gold` classe la cible avec `bl._est_verbe` (lexique + désinences). Sur les **145 labels**, HEAD
compte **63 verbes / 82 noms** ; le POS gold donne **116 verbes / 29 noms** : **53 verbes sont comptés
comme noms**. Sur les **239 cibles**, 81/158 contre **159/80**. Le snapshot post-correctif élargit le
lexique (91/148 sur 239 ; 71/74 sur 145), mais il reste **68 verbes non reconnus** sur 239 et **45** sur
145. Sur mes 20 cas, **16 cibles sont des verbes**, `_est_verbe` n'en reconnaît que **9** ; il voit comme
noms `poussent`, `aboie`, `commence`, `continue`, `marche`, `appelle`, `trouve` (7 occurrences).

Conséquence : `attachement.verbe` / `.nom` ne mesure pas la convention (verbe vs nom), mais la
reconnaissance d'un lexique. **Correction suggérée** : classer la cible avec le POS gold de la phrase
(`phrase["mots"]`), que `evaluer_gold` a déjà ; les 239 premières cibles correspondent toutes à un token.

## 5. Contrôle négatif — le hasard

Pour chaque cas, une cible prédite tirée uniformément parmi les **239 premières cibles** (154 distinctes),
10 000 répétitions, `random.Random(0)` :

| | valeur |
|---|---:|
| accord moyen avec le gold | **0,77 %** |
| IC95 des simulations | 0–5 % |
| meilleur tirage sur 10 000 | 3/20 |
| P(≥ 10/20) | 0 |
| P(≥ 17/20) | 0 |
| observé (moi) | **20/20** |

Le contrôle interne d'`evaluer_gold` (`c in rng.choice(cibles)`) donne 1/239 = 0,42 %, du même ordre. Le
20/20 n'est pas le hasard ; le 10/20 du bloc n'est pas non plus le hasard (P(≥10) = 0), mais il est très
loin du 20/20.

## 6. Limites — ce qui pourrait rendre ce contrôle faux

1. **n = 20** : IC larges (20/20 → 83,9–100 % ; 10/20 → 29,9–70,1 %). On ne conclut pas sur les 239 ; on
   contrôle la convention, pas le taux global.
2. **Un seul annotateur, subjectif** : pas de kappa inter-annotateurs. Mon 20/20 mesure surtout que la
   convention implicite du gold est reconstructible par un lecteur qui connaît la doc — pas une norme
   externe.
3. **Annotation avec la segmentation gold** (spans, rôles), cibles retirées : l'antécédent est plus facile
   à identifier que sur texte brut. Une annotation à l'aveugle complète (segmentation incluse) aurait pu
   différer, notamment sur les phrases synthetiques.
4. **Une fuite** : `r057` (cible `aboie` vue avant le tirage). Sensibilité 19/19 ; je la garde dans le
   tableau et je signale le cas.
5. **7/20 cas synthétiques**, parfois agrammaticaux (« que un », « avec il ») : la convention y est moins
   naturelle. Le gold `hand` (13 cibles) n'est pas représenté.
6. **Le bloc et la doc ont changé pendant la session** : mesure aveugle sur HEAD `e1171032` (sha256
   `d9c9d559…`), re-exécution post-hoc sur le snapshot `6e843018…` ; les chiffres « après correctif » ne sont
   pas garantis sur l'état final, et les tableaux des § 2, 3.1 et 3.2 restent la mesure aveugle.
7. **Les constats 4.1 et 4.5 sont des lectures du gold** : je n'ai modifié ni `CONVENTION_CIBLE`, ni
   `_est_verbe`, ni le bloc ; les correctifs SUB du bloc et de la doc sont venus d'ailleurs, pendant la
   session. Le split `_est_verbe` reste à corriger.

## 7. Reproduire

```python
import random, sys
sys.path.insert(0, "tools/tests/linguistique")
import evaluer_gold as eg
ph = eg.charger()
cas = [(pi, si) for pi, p in enumerate(ph) for si, s in enumerate(p["segments"])
       if s.get("cibles") or s.get("cible")]
assert len(cas) == 239
random.seed(20261105)
tirage = random.sample(cas, 20)          # -> r047, s061, r293, ...
```

Puis retirer `cible`/`cibles` des segments avant annotation ; figer les annotations ; seulement ensuite
appeler `Heuristique().analyser(texte, langue)` et lire `meta.attachement.cible` sur le segment de même
`(type, debut, fin)`. Pour rejouer la version aveugle : `git show HEAD:tools/bloc_linguistique.py >
/tmp/bloc_head.py` (sha256 `d9c9d559…`).

## Fichiers

- `reports/rapport-annotation-independante.md` (cette fiche)
- `reports/pensee-annotation-independante.json` (les 20 annotations, leurs raisons, les accords, le
  contrôle négatif, l'audit de la convention et les deux versions du bloc)

Aucun fichier existant modifié par moi ; aucun commit.
