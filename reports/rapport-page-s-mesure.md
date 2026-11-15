# La page `/` de S : 369/0 contre 359/99 — la recette, et pourquoi « 0 » n'est pas « zéro verdict »

> **Ligne de roadmap** : S · **Tâche** : X1 / J4 après-midi (la part du pilote) · **Date** :
> 2026-11-15 12 h 37 HNE · **HEAD parent mesuré** : `049343d3` · **Sous-module
> `tools/structures`** : `389b99f` · **Verdict** : la page `/` sert **toujours l'ancien banc** —
> **369 candidats**, **0 avec `profondeur`**, **0 à ≥ 3**, distribution des `niveau` **10 / 277 /
> 82** — alors que la v7 dynamique donne **359 candidats**, **2 / 37 / 221 / 84 / 13 / 2** et
> **99 à ≥ 3**. Le **106 conservés / 41 en quarantaine** de la v2 est **reproduit à la lettre**
> (signature exacte), mais la signature nue ne donne que **65 cibles distinctes** : **41
> collisions**. Avec l'attachement, **106/41** devient injectif ; avec les espaces normalisés et
> l'attachement, **115/32** ; avec la cible réduite à sa tête, **117/30**. Les référents sont
> **28 mappings / 16 justes / 12 faux / 2 manquants**, **0 note** ; la cible **14 occurrences /
> 12 formes** ne couvre que **a001–a003**. **Aucune écriture dans `tools/structures/`** : le
> sous-module est **propre**, **56/56 tests** passent en **4,3 s**, le port **8765** est intact
> (`financemeteo`), le port **9000** est libre, et le **contrôle négatif** rejette l'hypothèse
> « les deux bancs sont le même ».

**En trois lignes.** (1) « 369/0 » et « 359/99 » ne sont **pas** des comptes de verdicts : ce
sont **candidats / candidats à profondeur ≥ 3**. La page `/` porte **150 verdicts / 147 paires** ;
la v7 n'a **aucun verdict natif**. (2) La migration exacte reproduit **106/41**, mais **106
verdicts tombent sur 65 candidats** (41 collisions) ; l'attachement résout les collisions et
laisse **106/41**, les espaces normalisés donnent **115/32**, la cible-tête **117/30** — le
chiffre dépend de la convention, et **41 n'est pas un invariant**. (3) Les référents sont
toujours **12/28 faux**, **2 manquants**, **0 note** ; la cible **14/12** est le périmètre
**a001–a003** (9/12 justes aujourd'hui), pas les neuf paragraphes. **S n'a rien intégré** :
`work/banque-v7/` et `work/referents/` sont absents, `phrases_generees.json` date du **02/11** et
`/api/phrases` rend **0/369** `profondeur`.

## Ce que cette fiche est, et n'est pas

- **Est** : la **recette indépendante** de la page `/` de S, en **lecture seule**. Elle rejoue la
  mesure de la v7, vérifie les chiffres de [`rapport-coordination-s-v2.md`](rapport-coordination-s-v2.md),
  liste les **41 paires en quarantaine**, mesure le **106** en cibles distinctes, audite les
  **référents** et fournit le **contrôle négatif** qui sépare les deux bancs. Le JSON archivé est
  [`rapport-page-s-mesure.json`](rapport-page-s-mesure.json) ; le harnais **local** qui l'a produit
  est [`work/page-s-mesure/mesurer.py`](../work/page-s-mesure/mesurer.py) (`work/` est ignoré par
  git ; le JSON, lui, est dans `reports/`).
- **N'est pas** : une migration, un patch, un commit de S, ni une correction des référents. Le
  pilote **ne décide pas** garder ou régénérer `/` ; il mesure et il nomme ce que la décision
  devra trancher. Aucun `POST`, aucune écriture dans `tools/structures/`.
- **Public** : la session S (prochaine action : spécifier la migration et les référents), le
  superviseur du chantier J4 et la session de clôture.
- **Mesure** : sous-module `389b99f`, parent `049343d3` au moment de la mesure, **2026-11-15
  12 h 37 HNE**. Le parent a bougé pendant la session (`6f862993` → `9960b37f` → `049343d3`) ;
  le pointeur du sous-module, lui, est resté `389b99f`. **56 tests** passent en **4,3 s**.

## 1. Ce que `/` sert réellement

### 1.1 Le service et les routes

Le serveur a été lancé sur un **port éphémère** (pas 8765), uniquement pour des `GET`, puis
arrêté. Le port **8765** est tenu par `financemeteo` (`python3 src/app.py --no-browser`, pid
**2725542**) : `GET http://127.0.0.1:8765/` rend **200**, **174 051 o**, `<title>Portefeuille iA
— tableau de bord</title>`. Le port **9000** est **libre** ; aucun `serveur.py` S n'écoute.

| route | code | contenu mesuré |
|---|---:|---|
| `GET /` | **200** | 2 350 o, `<title>Structures — le banc d'interprétations</title>` |
| `GET /api/phrases` | **200** | **207 phrases**, **369 candidats**, **150 validations**, **0** `profondeur`, **2 414** segments |
| `GET /paragraphes` | **200** | 3 493 o, `<title>Structures — paragraphes complets</title>` |
| `GET /api/paragraphes` | **200** | **9 paragraphes**, **19 candidats**, **19 verdicts**, **169/169** segments avec `profondeur` |

C'est exactement ce que la v2 avait mesuré sur 9000 : la page `/` **sert l'ancien banc**, et
`/paragraphes` est la **seule fenêtre v7**. Le serveur de mesure est arrêté ; le port 9000 est
libre après la recette.

### 1.2 Les données servies

| fichier | phrases | candidats | `profondeur` | mtime |
|---|---:|---:|---:|---|
| `donnees/phrases.json` | 7 | 14 | 0 | 2026-11-02 02:10 |
| `donnees/phrases_generees.json` | 200 | 355 | 0 | **2026-11-02 20:35** |
| **total** | **207** | **369** | **0/369** | — |

Les segments ne portent que l'ancien `niveau` ; la distribution des **maxima par candidat** est
**10 / 277 / 82** pour 0 / 1 / 2. Aucun candidat n'atteint 3, aucun segment ne porte
`profondeur`. Le SHA-256 de `phrases_generees.json` est
`43957a3b…` ; celui de `phrases.json` est `51e07f1c…`.

### 1.3 Le rendu ne peut pas inventer la v7

- `static/app.js` indente avec **`s.niveau * 1.4`** et `niveauDe()` lit le `niveau` de la
  dernière validation ; le mot **`profondeur` n'y apparaît pas** (0 occurrence).
- `static/paragraphes.js` affiche **`s.profondeur ?? s.niveau`** : c'est la page qui montre la
  v7, pas `/`.
- Pour que `/` affiche la v7, il ne suffit pas d'ajouter `profondeur` aux candidats : il faut
  **régénérer `phrases_generees.json`** (ou réécrire `niveau = profondeur`), donc **écrire dans
  le sous-module**. Ce n'est pas fait.

### 1.4 « 0 » n'est pas « zéro verdict »

C'est la correction de lecture la plus importante de cette recette. Le `/` de « 369/0 » a
**0 candidat à profondeur ≥ 3**, pas **0 verdict** :

| mesure | `/` (banc stocké) |
|---|---:|
| verdicts (lignes) | **150** |
| paires (phrase, candidat) uniques | **147** |
| révisions | **3** |
| phrases jugées en entier | **74/207** (35,7 %) |
| phrases sans aucun verdict | **133** (64,3 %) |
| candidats jugés | **147/369** (39,8 %) |
| dernier verdict : `resolu` / `exclu` / `compatible` | **73 / 63 / 11** |
| lignes : `resolu` / `exclu` / `compatible` / `double_sens` | **74 / 64 / 11 / 1** |
| lectures acceptées / exclues (dernier verdict) | **84 / 63** |
| notes non vides | **1** |
| contextes non vides | **6/147** |
| auteurs | **1** (`humain`, sans identité) |

La page `/` affiche ces verdicts (`app.js`, `#s-valides` = 150). Écrire « 369 candidats, 0
verdict » est donc **faux au sens littéral** ; c'est vrai seulement si « 0 » veut dire **0
candidat profond**. La même ambiguïté vaut pour « 359/99 » : **99 est un nombre de candidats à
≥ 3**, pas un nombre de verdicts.

## 2. La v7 dynamique : 359 candidats, 99 à ≥ 3

Mesure rejouée avec `mesure_arbre.mesurer()` et `generateur.analyser()` à `389b99f`, sans écrire
`donnees/mesure-arbre.json`.

| mesure | `/` (stocké) | v7 dynamique |
|---|---:|---:|
| phrases | 207 | **207** |
| candidats | **369** | **359** |
| segments | 2 414 | **2 308** |
| candidats avec `profondeur` | **0/369** | **359/359** |
| distribution des profondeurs max | 10 / 277 / 82 (0→2) | **2 / 37 / 221 / 84 / 13 / 2** (0→5) |
| candidats à profondeur ≥ 3 | **0** | **99** (27,6 %) |
| verdicts natifs | 150 lignes / 147 paires | **0** |
| référents | non affichés sur `/` | **371 occurrences**, **29 formes**, **294 avec candidat**, **77 sans**, **170/207** phrases |

Les **371** de la v2 sont des **occurrences**, pas des formes : il y a **29 formes uniques**
(`y` 109, `en` 67, `se` 44, `me` 19, `il` 18, `son` 18, `elle` 9, `je` 9, `vous` 9, `lui` 8…).
La v2 écrit « 371 formes » ; la mesure dit **371 occurrences / 29 formes**. C'est la même
distinction que le **14 occurrences / 12 formes** des référents.

**Les 99 ne sont pas 99 verdicts.** La v7 n'a **aucun verdict natif** : les 147 paires de
`validations.jsonl` portent sur les signatures de l'ancien banc. Après migration exacte **avec
attachement**, **46 des 99** candidats profonds reçoivent un verdict migré ; **53** restent à
juger. Après normalisation des espaces + attachement, **47/99**. Le reste de la profondeur est
donc **à gagner**, pas **déjà jugé**.

`/paragraphes` est la fenêtre v7 : **9 paragraphes**, **19 candidats**, **19 verdicts**,
**169/169** segments avec `profondeur`. C'est le seul endroit où l'arbre v7 est réellement
visible aujourd'hui.

## 3. La couverture et les verdicts

### 3.1 La couverture du banc ancien

La couverture est **partielle et datée** : **74/207** phrases complètes (35,7 %), **133** sans
aucun verdict (64,3 %), **147/369** candidats (39,8 %). Les 7 phrases du banc sont **7/7**
jugées ; les 200 phrases de littérature sont **67/200** (33,5 %). Un seul annotateur, une seule
journée (2026-11-03), **1 note**, **0 double-codage**, **0 test-retest**. Ce n'est pas une
accuracy.

### 3.2 Ce que la migration fait à cette couverture

Sous la **signature exacte de la v2** — `(texte, type, rôle)` des segments, dans l'ordre —,
**106 paires** ont une correspondance v7 et **41** n'en ont pas. Mais **106 paires tombent sur
seulement 65 candidats v7 distincts** : **41 collisions**. Autrement dit, cette signature ne
peut pas attacher **106 verdicts distincts** : **41 se disputent les mêmes 65 candidats**, et
une table indexée par candidat en perdrait 41. L'attachement (segment + cible) sépare ces
variantes : on garde **106/41** et on obtient **106 cibles distinctes**.

| convention | gardés | quarantaine | cibles distinctes | collisions | phrases v7 complètes | profonds jugés |
|---|---:|---:|---:|---:|---:|---:|
| exacte `(texte, type, rôle)` | **106** | **41** | **65** | **41** | 21 (+35 partielles) | 23 |
| exacte + attachement | **106** | **41** | **106** | **0** | **56** (+0) | **46** |
| espaces normalisés | 119 | 28 | 74 | 45 | 24 (+39) | 24 |
| espaces normalisés + attachement | **115** | **32** | **115** | **0** | **59** (+4) | **47** |
| espaces normalisés + attachement, cible = tête | **117** | **30** | **117** | **0** | **61** (+2) | **48** |

Deux lectures de ce tableau :

1. **Le 106/41 de la v2 est exact** sous sa convention. Ce n'est **pas** un compte de migration
   sûr : sans attachement, ce sont **65 cibles** et **41 collisions**. Avec l'attachement exact,
   **106/41** devient **injectif** ; c'est la convention minimale à retenir.
2. **Le 41 n'est pas un invariant.** Neuf paires sont quarantinées uniquement parce que les
   segments des 7 phrases du banc portent des **espaces de tête** (`' de la voisine'` contre
   `'de la voisine'`). En normalisant les espaces, **115/32** ; en réduisant la cible
   d'attachement à sa tête (`de la voisine` → `voisine`, `à Marie` → `Marie`), **117/30**. Le
   chiffre dépend de la convention, et la fiche doit le dire.

Sous **exact + attachement**, la couverture v7 est **56 phrases complètes / 0 partielle / 151
sans verdict** ; les 74 phrases complètes de l'ancien banc se répartissent en **56 conservées**
et **18 perdues en entier** (dans ces données, les 18 sont perdues en bloc, pas en partie).
Sous **normalisé + attachement**, **59 complètes + 4 partielles + 144 sans verdict**.

Statuts des **106** (exact + attachement) : **55 `resolu`, 46 `exclu`, 5 `compatible`** —
**60 acceptés / 46 exclus**. Statuts des **41** en quarantaine : **18 `resolu`, 17 `exclu`, 6
`compatible`** — **24 acceptés / 17 exclus**. La quarantaine n'est donc pas marginale : **24
lectures acceptées** attendent un re-jugement.

## 4. Les référents : 14 occurrences / 12 formes

### 4.1 Ce que le journal contient

`donnees/paragraphes-validations.jsonl` : **19 lignes**, **9 paragraphes**, **19/19 candidats**,
**11 acceptés / 8 exclus**, **0 note**, `auteur: humain`, mtime **2026-11-04 15:10:08**, SHA-256
`a3c54c9c…`. Ces 19 verdicts sont **committés** à `389b99f` ; ils ne sont **pas** dans le lot
des 41, qui sont des verdicts de la banque `/` (`validations.jsonl`). Les 19 verdicts portent **28 mappings uniques** (les mêmes valeurs sont répétées
d'un candidat à l'autre), comparés à la source anglaise et à la table de l'audit
[`rapport-etat-s.md`](rapport-etat-s.md) § 2 :

| mesure | valeur |
|---|---:|
| mappings uniques | **28** |
| justes | **16/28** |
| faux | **12/28** |
| formes manquantes | **2** |
| paragraphes fautifs | **6/9** (a001, a002, a005, a006, a008, a009) |
| paragraphes propres | **3/9** (a003, a004, a007) |
| notes | **0** |

Les **12 faux** et les **2 manquants** :

| phrase | forme | enregistré | attendu | verdict |
|---|---|---|---|---|
| a001 | `en` | Alice | non référent (partitif « les larmes ») | **faux** |
| a002 | `en` | Alice | non référent (préposition « en verre ») | **faux** |
| a002 | `y` | Alice | la boîte | **faux** |
| a005 | `en` | coup | la salle | **faux** |
| a006 | `cela` | Comme | attendre à la petite porte | **faux** |
| a008 | `Je` | le contenu | Alice | **faux** |
| a008 | `me` | le contenu | Alice | **faux** |
| a008 | `je` | Je me sens toute drôle | Alice | **faux** |
| a008 | `on` | Je me sens toute drôle | indéfini | **faux** |
| a008 | `en` | Je me sens toute drôle | préposition | **faux** |
| a009 | `se` | Un moment | Alice | **faux** |
| a009 | `en` | Un moment | préposition | **faux** |
| a001 | `les` | *(absent)* | les conseils | **manquant** |
| a002 | `l'` | *(absent)* | la boîte | **manquant** |

### 4.2 Le périmètre a001–a003 : 12 formes / 14 occurrences

C'est le périmètre de la fiche de traduction (`rapport-s-traductions.md`) et la cible
« **14 occurrences / 12 formes** » :

| mesure | a001–a003 |
|---|---:|
| formes uniques (clés par paragraphe) | **12** |
| occurrences dans le texte | **14** (`se` deux fois en a001, `sa` deux fois en a003) |
| justes | **9/12** |
| faux | **3/12** (a001 `en`, a002 `en`, a002 `y`) |
| manquants | **2** (`les`, `l'`) |
| cible corrigée | **12/12 justes, 14/14 occurrences, 0 faux, 0 manquant** |

La cible **14/12** est donc bien définie — mais elle **ne couvre que a001–a003**. Les
**a004–a009** portent **16 mappings**, **7 justes**, **9 faux**, **0 manquant** ; ils sont
**4/9** à être fautifs (a005, a006, a008, a009). Corriger seulement les 12 formes de a001–a003
laisse donc **9 faux** dans les six autres paragraphes. Pour atteindre le **0/9 fautif** de
l'action A2, il faut aussi corriger ces 9 ; la cible 14/12 ne suffit pas. Autrement dit, la
cible **14/12** et la mesure **0/9** ne portent pas sur le même périmètre : 14/12 = a001–a003 ;
0/9 = les neuf paragraphes, donc **9 faux de plus** à corriger.

### 4.3 Une correction de la v2 : « 9/16 faux » n'est pas le bon compte

La v2 écrit, en § 1.3 et § 7 : « **9/16 mappings uniques faux** (12/28 occurrences) ». Les
données de l'audit disent :

- **16/28 justes**, **12/28 faux** sur les 9 paragraphes ;
- **9/12 justes** sur a001–a003 ;
- **7/16 justes** sur a004–a009.

Le **9** est le numérateur des **justes** de a001–a003 ; le **16** est le numérateur des
**justes** des 9 paragraphes ; **28** est le nombre de **mappings uniques**, pas d'occurrences.
La formulation correcte est : **16/28 justes (12 faux)**, et **9/12 justes sur a001–a003**. Ce
n'est pas un chiffre de données à changer, c'est une **transposition de la fiche** à corriger.

### 4.4 L'intégration de S est absente

`work/referents/` **n'existe pas** ; `paragraphes-validations.jsonl` est **inchangé** (19 lignes,
0 note, mtime 04/11). La phrase du plan J4 — « S intègre les référents (14 occurrences / 12
formes) » — **n'est donc pas réalisée**. La page `/paragraphes` continue d'afficher les 19
verdicts et leurs référents enregistrés, avec les défauts de la page (les `<select>` ne sont pas
forcés). Le `14/14` de la fiche de traduction reste un résultat **côté anglais**, pas une
validation humaine.

### 4.5 Les référents de la v7 ne sont pas les 14/12

La v7 dynamique propose **371 occurrences / 29 formes** sur les 207 phrases, **294 avec au moins
un antécédent**, **77 sans**, **170/207** phrases avec un référent. C'est une **proposition**,
pas une résolution : elle ne remplace ni les 12 formes de a001–a003, ni les 28 mappings du
journal. La page `/` n'affiche pas ces référents ; `/paragraphes` les affiche. Ne pas confondre
les deux mesures.

## 5. Les 106 conservés / 41 en quarantaine

### 5.1 Le compte exact

Sous la signature de la v2, **106 paires** ont une correspondance v7 et **41** n'en ont pas.
Ces 41 sont des verdicts de la **banque `/`** (`validations.jsonl`), pas les 19 verdicts de
`/paragraphes` :

| mesure | valeur |
|---|---:|
| paires uniques | **147** |
| conservées (signature exacte) | **106** |
| en quarantaine | **41** |
| lignes concernées par la quarantaine | **44** |
| révisions (lignes en plus des paires) | **3** |
| phrases concernées | **18** |
| dont candidats sans index | **5** |
| dont même index mais contenu changé | **36** |
| acceptés / exclus dans la quarantaine | **24 / 17** |

Les **3 révisions** sont des paires de la quarantaine jugées plusieurs fois : **44 lignes = 41
paires + 3 révisions**. Les **41** sont **les mêmes avec ou sans attachement** : l'attachement ne
change pas la quarantaine, il sépare les **106** (voir § 5.3). Les **41 paires** sont réparties
sur **18 phrases** :

| phrase | paires | candidats (statut) | raison |
|---|---:|---|---|
| p001 | 2 | c1 `resolu`, c2 `exclu` | même index, contenu changé |
| p002 | 2 | c1 `resolu`, c2 `compatible` | même index, contenu changé |
| p003 | 2 | c1 `resolu`, c2 `exclu` | même index, contenu changé |
| p004 | 2 | c1 `resolu`, c2 `compatible` | même index, contenu changé |
| p005 | 2 | c1 `exclu`, c2 `resolu` | même index, contenu changé |
| p006 | 2 | c1 `resolu`, c2 `compatible` | c2 sans index |
| p007 | 2 | c1 `resolu`, c2 `compatible` | même index, contenu changé |
| c002 | 2 | c1 `resolu`, c2 `compatible` | même index, contenu changé |
| c004 | 2 | c1 `compatible`, c2 `resolu` | même index, contenu changé |
| c009 | 3 | c1–c3 `exclu` | même index, contenu changé |
| c011 | 2 | c1 `exclu`, c2 `resolu` | même index, contenu changé |
| c013 | 3 | c1 `exclu`, c2–c3 `resolu` | même index, contenu changé |
| c020 | 3 | c1–c3 `exclu` | même index, contenu changé |
| c023 | 3 | c1–c2 `resolu`, c3 `exclu` | c3 sans index |
| c043 | 2 | c1 `exclu`, c2 `resolu` | même index, contenu changé |
| c056 | 3 | c1 `exclu`, c2 `exclu`, c3 `resolu` | c2–c3 sans index |
| c064 | 2 | c1 `resolu`, c2 `exclu` | c2 sans index |
| c065 | 2 | c1 `exclu`, c2 `resolu` | même index, contenu changé |

La liste complète, avec l'index ancien, le nombre de candidats v7, l'attachement et le niveau
max, est dans le JSON (`migration.quarantaine_exacte.detail`).

### 5.2 Les 5 sans index ne sont pas 5 verdicts perdus

Les **5 candidats sans index** sont `p006-c2`, `c023-c3`, `c056-c2`, `c056-c3`, `c064-c2`. Un
seul est récupérable par la signature normalisée : **`p006-c2`** a une correspondance en
**v7-c1** (l'index 2 n'existe plus, mais le contenu y est). Les **4 autres** n'ont aucune
correspondance, même normalisée. La v1 disait « 5 verdicts à risque » : c'est vrai **par
l'index**, pas **par le contenu**. La v2 a raison de dire que **5 sans index ≠ 41 sans
correspondance** ; la recette ajoute que **5 sans index ≠ 5 perdus**.

### 5.3 Le piège des collisions

Sous la signature nue, **106 paires → 65 candidats distincts** : **41 collisions**. Si la
migration écrit les verdicts dans une table indexée par candidat v7 sans distinguer
l'attachement, **41 verdicts sont écrasés** (le dernier gagne) et **41 autres sont en
quarantaine** — deux ensembles de 41 **différents**, ce qui prête à confusion. Avec
l'attachement, les **106** sont injectifs. C'est la correction opérationnelle la plus
importante de cette recette.

### 5.4 Le contrôle par index

La migration **par index** recollerait **36/147** verdicts à un **autre contenu** (les 36
candidats « même index, contenu changé ») ; les **5 sans index** n'auraient plus de cible. La
signature exacte n'en recolle **aucun** (0/106), au prix des 41 quarantaines. Le contrôle est net : **l'index est
faux**, la signature est la bonne clé — à condition d'y mettre l'attachement.

## 6. Le contrôle négatif : les deux bancs diffèrent

**Hypothèse H0** : « les deux bancs sont le même » — mêmes candidats, même contenu, même
présence de `profondeur`, même distribution. Elle est **rejetée** par six mesures indépendantes :

| test | `/` (stocké) | v7 | identiques ? |
|---|---:|---:|---|
| cardinalité des candidats | **369** | **359** | non |
| candidats avec `profondeur` | **0/369** | **359/359** | non |
| candidats à profondeur ≥ 3 | **0** | **99** | non |
| empreinte SHA-256 des signatures exactes | `569a61fa…` | `46202525…` | non |
| Jaccard multiset des signatures | — | **0,7170** | non (1,0 attendu sous H0) |
| Jaccard global des signatures | — | **0,7391** | non |
| migration sous H0 | 147/147 attendus | **106/147** observés | non |

**Contrôle positif** : chaque banc comparé **à lui-même** donne la même empreinte
(`569a61fa…` pour l'ancien, `46202525…` pour la v7). Le comparateur sait donc dire
« identique » ; la différence n'est pas un artefact de comparaison.

**La différence est localisée, pas totale** : **304/369** signatures sont identiques au même
index, **55** changent et **10** disparaissent (`304 identiques / 55 changés / 10 orphelins`).
Les deux bancs sont **proches** — c'est pour cela que la migration a un sens — mais **pas
identiques**. Jaccard multiset **0,7170**, Jaccard global **0,7391**.

**Contrôle de la migration** : par index, **36/147** verdicts seraient recollés au mauvais
contenu ; par signature exacte, **0/106**. C'est le contrôle négatif de la clé de migration.

**Conclusion** : H0 est rejetée. La page `/` **n'est pas** la v7 ; elle sert l'ancien banc. Le
négatif n'est pas « les deux bancs sont différents parce qu'on a regardé » : il est
**reproductible** (empreintes, comptes, Jaccard) et **contrôlé** (même source → identique).

## 7. Service, tests et état

| contrôle | résultat |
|---|---|
| port **8765** | occupé par `financemeteo` (pid **2725542**), `GET /` **200**, **174 051 o**, titre « Portefeuille iA — tableau de bord » |
| port **9000** | **libre** ; aucun `serveur.py` S en écoute |
| serveur de mesure | port **éphémère**, `GET` seulement, **arrêté** après la recette |
| **56 tests** | **56/56 OK** en **4,3 s** (`python3 -m unittest discover -s tests`) |
| sous-module `389b99f` | **propre** (`git status --porcelain` vide) ; `origin/master` = `389b99f` |
| pointeur du parent | `160000 commit 389b99f… tools/structures` |
| `work/banque-v7/` | **absent** |
| `work/referents/` | **absent** |
| écritures dans `tools/structures/` | **aucune** |
| HEAD parent à la mesure | `049343d3` (branche `s/v7`, `describe` `semaine-2-2026-11-20-1-g049343d3`) |

Le parent a bougé **pendant** la session (`6f862993` → `9960b37f` → `049343d3`), puis
**après** la mesure (`2b5bd1cd`, journal régénéré) ; il porte **des modifications hors
périmètre**. Le sous-module, lui, est resté à `389b99f` et **propre**, et le pointeur du parent
est toujours `389b99f`.
Un premier lancement manuel du serveur sur **9000** a laissé un processus (pid **602059**) : il
a été **tué**, et la mesure finale a été prise **après** nettoyage (9000 libre, aucun
`serveur.py`). Le JSON final est celui de cet état nettoyé.

## 8. Ce qui pourrait rendre cette fiche fausse

- **Le sous-module bouge** : `389b99f`, les 369/150/147, les 359/99, les 106/41 et les 28
  mappings dépendent de ce commit et des fichiers `donnees/`. Un commit S qui régénère
  `phrases_generees.json` change tous ces chiffres.
- **Le parent bouge** : `049343d3` est un instantané ; le pointeur du sous-module peut avancer
  sans que les données changent, ou l'inverse.
- **La signature change de convention** : 106/41 (exacte), 106/41 avec attachement mais 0
  collision, 115/32 (espaces + attachement), 117/30 (cible = tête). Le **41** n'est pas un
  invariant ; le **106** non plus.
- **Le jugement « faux » sur les référents est celui de l'audit** : une convention différente
  sur `en`/`sa`/`y` déplacerait quelques cas. Les 12 faux et 2 manquants sont listés ligne à
  ligne, ce qui permet de contester chaque cas.
- **Les 150 verdicts sont un seul annotateur, une seule journée** ; les taux d'acceptation ne
  sont pas une accuracy. Les 19 verdicts de `/paragraphes` sont aussi un seul annotateur, 0
  note.
- **La mesure HTTP utilise un port éphémère**, pas 8765 ; 8765 est tenu par `financemeteo` et
  n'a pas été touché. Le serveur de mesure a été arrêté.
- **Les 56 tests passent, mais la passe complète des portes du parent n'est pas rejouée ici** :
  un rouge de porte n'est pas couvert par cette recette.
- **S n'a rien intégré** : si S régénère ou corrige après cette fiche, les chiffres de
  couverture et de référents changent ; c'est précisément l'objet de la prochaine session.

## 9. Fichiers lus, non modifiés

- `tools/structures/donnees/phrases.json`, `phrases_generees.json`, `validations.jsonl`
- `tools/structures/donnees/paragraphes.json`, `paragraphes-validations.jsonl`
- `tools/structures/generateur.py`, `mesure_arbre.py`, `serveur.py`
- `tools/structures/static/app.js`, `static/paragraphes.js`
- `tools/structures/tests/` (lus/exécutés : **56 tests**)
- `tools/structures/.git` (HEAD, status, remote)
- `reports/rapport-coordination-s-v2.md`, `rapport-etat-s.md`, `rapport-s-traductions.md`,
  `rapport-s-paragraphes.md`
- `docs/pilotage/semaine-2.md`
- `/proc`, `ss`, `ps` (lecture seule)

**Aucune écriture dans `tools/structures/`** : le sous-module est resté propre
(`git status --porcelain` vide) ; le serveur de mesure a été arrêté ; aucun `POST` n'a été
envoyé.

## 10. Références

- [rapport-coordination-s-v2.md](rapport-coordination-s-v2.md) — la fiche de coordination, les
  106/41, les 359/99.
- [rapport-etat-s.md](rapport-etat-s.md) — l'audit des 28 référents, les 12 faux, les 2
  manquants.
- [rapport-s-traductions.md](rapport-s-traductions.md) — les 14 occurrences / 12 formes de
  a001–a003 et la source anglaise.
- [rapport-s-paragraphes.md](rapport-s-paragraphes.md) — les neuf paragraphes d'Alice.
- [semaine-2.md](../docs/pilotage/semaine-2.md) — la ligne J4, les 106/41 et le 369/0.
- [mesurer.py](../work/page-s-mesure/mesurer.py) — le harnais **local** (ignoré par git) qui a
  produit le JSON ; la mesure se rejoue avec `PYTHONDONTWRITEBYTECODE=1 python3
  work/page-s-mesure/mesurer.py`.
- [rapport-page-s-mesure.json](rapport-page-s-mesure.json) — le JSON de la mesure.
- [generateur.py](../tools/structures/generateur.py) — `analyser`, `referents`, l'arbre.
- [mesure_arbre.py](../tools/structures/mesure_arbre.py) — la mesure v7.
- [app.js](../tools/structures/static/app.js) — le rendu de `/` (`niveau`).
- [paragraphes.js](../tools/structures/static/paragraphes.js) — le rendu de `/paragraphes`
  (`profondeur ?? niveau`).
