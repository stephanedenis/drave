# Frontières de phrase — P0-4 du bloc linguistique

> **Ligne** : **P0-4** de l'audit produit [`reports/rapport-fiabilite-produit.md`](rapport-fiabilite-produit.md)
> (`reports/rapport-produit-bloc-l.md` pour le banc de 50 phrases) · **Branche** : `s/v7` ·
> **Commit mesuré** : `ed8f9414` (2026-11-06 20:06) · **Module** :
> [`tools/bloc_linguistique.py`](../tools/bloc_linguistique.py), `sha256 12e73b7ab2cd…` ·
> **Gold** : `c5b80dd8`.
> **Date** : 2026-11-06 · **Verdict** : ✅ **frontières réparées sur le banc** ; ⚠️ **gain dev/test nul
> par construction** ; **2 spans de phrase du gold corrigés** (espace de tête), **0 régression mesurée**.
> **Aucun fichier existant modifié ; aucun commit.** Sorties : ce rapport et
> [`pensee-frontieres-phrase.json`](pensee-frontieres-phrase.json) (les 40 textes, les spans avant/après,
> les mesures et les patchs exacts).
> **Dispositif** : 40 textes libres écrits pour l'analyse (59 phrases attendues) ; `Heuristique` original
> vs sous-classe à règles commutables ; `evaluer_gold.py` sur dev/test (422/190 phrases) ; aucun modèle,
> aucun GPU. Le module a bougé pendant la session (`c6904284` → `ed8f9414`, 2249 → 2282
> lignes ; le fichier de travail porte un `M` d'un autre agent, hash du module ci-dessus) ; **tous les chiffres ci-dessous sont rejoués sur `ed8f9414`**.

**En une phrase.** Sur **40 textes libres**, le découpage passe de **102 à 59 phrases** (59 attendues) :
**32/40** textes avaient une **frontière fausse** (47 coupures en trop, 4 fusions, 9 chevauchements,
5 fausses questions), **24 textes / 31 phrases** commençaient par un espace ; après le patch, **40/40**
textes sont exacts, **0** défaut, **0** chevauchement, **0** fausse question. Sur le **gold 612**, POS,
F1 syntagmes, attachement et tokens sont **inchangés au chiffre près** (delta 0) ; seuls **2 spans de
phrase** se décalent d'un espace (r308, r318), **0 valeur d'acte** change. **Le gain dev/test est donc
0** : le gold ne contient aucune des pathologies (ni chiffre, ni URL, ni abréviation, ni ellipse, ni saut
de ligne) ; il sert de **contrôle de non-régression**, pas de mesure de gain. Le gain se lit sur le banc
libre : **63 actes faux sur 102 phrases → 0 sur 59**.

## 1. Dispositif

- **Banc libre** : 40 textes, **59 phrases attendues**, écrits pour couvrir les cas de l'audit et les
  catégories demandées. Les textes, les spans attendus et les spans prédits avant/après sont dans le JSON
  (`corpus_40`). Aucun texte ne vient du gold.
- **Simulation** : sous-classe de `Heuristique` ; chaque règle (a)–(f) est activable seule. Le patch final
  est testé comme module copié localement, puis `git apply --check` sur le dépôt (sans écriture).
- **Gold** : 612 phrases (hand 20 + reel 432 + synthétique 160), split `gold_split` : dev 422 / test 190.
  L'évaluateur est `tools/tests/linguistique/evaluer_gold.py` (POS, F1 syntagmes, attachement,
  pragmatique). Les valeurs absolues sont celles du **rejoué** au commit `ed8f9414` ;
  elles diffèrent de la fiche v12 (0,7547 / 0,5820 sur dev) parce que le module a été amélioré depuis
  l'audit. **Seuls les deltas sont comparables au gold de l'audit.**
- **Ce que le banc ne mesure pas** : la prose ordinaire (les cas pathologiques sont surreprésentés),
  l'accord inter-annotateurs, la qualité du chunker sur les lignes, ni la justesse sémantique.

### 1.1 Les 40 textes

| famille | n | textes |
|---|---:|---|
| négatifs | 2 | deux et trois phrases réelles |
| décimaux, dates, versions, IP | 5 | 12.5, 12.03.2024, 2.1.3, 192.168.1.10 |
| URL | 4 | requête ?page=2, URL en fin de phrase, parenthèses, question réelle |
| courriels | 2 | adresse seule, adresse + URL |
| chemins et code inline | 4 | src/tools/…, ./data/…, `code`, Heuristique._phrases |
| abréviations et civilités | 8 | M., Dr., etc. minuscule/majuscule, cf., p. ex., initiales, titre en fin de phrase |
| titres et listes | 3 | titre markdown, liste sans point, liste numérotée |
| guillemets | 2 | « Bonjour. » et « Viens-tu ? » |
| ellipses et ponctuation répétée | 4 | ... puis, ... Elle, ?!, … final |
| sans point final, espaces | 2 | phrase sans ponctuation finale, espaces de tête |
| anglais | 3 | Dr., e.g., etc. |
| point-virgule | 1 | virgule forte à l'intérieur d'une phrase |

## 2. Cartographie : avant / après

### 2.1 Le chiffre global

| mesure | avant | après | attendu |
|---|---:|---:|---:|
| phrases | 102 | **59** | 59 |
| textes exacts (spans + types) | 2/40 | **40/40** | 40/40 |
| textes avec au moins une frontière fausse | 32/40 | **0/40** | 0/40 |
| textes avec au moins un défaut (espaces compris) | 38/40 | **0/40** | 0/40 |
| coupures en trop | 47 | **0** | 0 |
| fusions (frontières manquantes) | 4 | **0** | 0 |
| chevauchements de phrases | 9 | **0** | 0 |
| phrases commençant par un espace | 31 (24 textes) | **0** | 0 |
| fausses questions | 5 | **0** | 0 |
| phrases vides | 0 | **0** | 0 |
| actes faux par phrase | 63/102 | **0/59** | 0 |

Le banc de l'audit donnait **6/46** textes coupés ; le banc ci-dessous est **plus dur** (URL, courriels,
chemins, décimaux et abréviations y sont surreprésentés) et mesure aussi les **espaces de tête** et les
**fausses questions**. Les deux chiffres ne sont donc pas comparables directement.

### 2.2 Les textes dont une frontière était fausse

| id | catégorie | avant | après | défauts avant |
|---|---|---:|---:|---|
| `d01` | décimal | 2 | 1 | +1 coupure(s) |
| `d02` | décimal+milliers | 2 | 1 | +1 coupure(s) |
| `d03` | date | 5 | 1 | +4 coupure(s) |
| `d04` | version+IP | 6 | 1 | +5 coupure(s) |
| `u01` | URL+query | 3 | 1 | +2 coupure(s), 1 fausse(s) question(s) |
| `u02` | URL+phrase | 5 | 2 | +3 coupure(s), 1 fausse(s) question(s), 1 espace(s) initial(aux) |
| `e01` | courriel | 2 | 1 | +1 coupure(s) |
| `e02` | courriel+URL | 4 | 1 | +3 coupure(s), 1 fausse(s) question(s) |
| `c01` | chemin+code | 2 | 1 | +1 coupure(s) |
| `c02` | chemin relatif | 3 | 1 | +2 coupure(s) |
| `c03` | code inline | 2 | 1 | +1 coupure(s) |
| `c04` | identifiant pointé | 2 | 1 | +1 coupure(s) |
| `a01` | abréviation M. | 2 | 1 | +1 coupure(s), 1 chevauchement(s), 1 espace(s) initial(aux) |
| `a02` | abréviation Dr. | 2 | 1 | +1 coupure(s), 1 chevauchement(s), 1 espace(s) initial(aux) |
| `a03` | etc. minuscule | 2 | 1 | +1 coupure(s), 1 chevauchement(s), 1 espace(s) initial(aux) |
| `a04` | etc. majuscule | 2 | 2 | 1 chevauchement(s), 1 espace(s) initial(aux) |
| `a05` | abréviation cf. | 2 | 1 | +1 coupure(s), 1 chevauchement(s), 1 espace(s) initial(aux) |
| `a06` | abréviation p. ex. | 3 | 1 | +2 coupure(s), 1 chevauchement(s), 2 espace(s) initial(aux) |
| `a07` | initiales | 3 | 1 | +2 coupure(s), 2 espace(s) initial(aux) |
| `a08` | titre en fin de phrase | 2 | 2 | 1 chevauchement(s), 1 espace(s) initial(aux) |
| `t01` | titre markdown | 1 | 2 | −1 fusion(s) |
| `t02` | liste sans point | 1 | 2 | −1 fusion(s) |
| `t03` | liste avec points | 4 | 2 | +2 coupure(s), 3 espace(s) initial(aux) |
| `g01` | guillemets | 2 | 2 | +1 coupure(s), −1 fusion(s), 1 espace(s) initial(aux) |
| `g02` | guillemets+question | 2 | 2 | +1 coupure(s), −1 fusion(s), 1 espace(s) initial(aux) |
| `x01` | ellipse minuscule | 2 | 1 | +1 coupure(s), 1 espace(s) initial(aux) |
| `en01` | anglais Dr. | 3 | 2 | +1 coupure(s), 1 chevauchement(s), 2 espace(s) initial(aux) |
| `en02` | anglais e.g. | 3 | 1 | +2 coupure(s), 1 espace(s) initial(aux) |
| `en03` | anglais etc. | 2 | 2 | 1 chevauchement(s), 1 espace(s) initial(aux) |
| `u03` | URL entre parenthèses | 3 | 1 | +2 coupure(s), 1 fausse(s) question(s) |
| `d05` | date+phrase | 4 | 2 | +2 coupure(s), 1 espace(s) initial(aux) |
| `u04` | URL+question réelle | 4 | 2 | +2 coupure(s), 1 fausse(s) question(s), 1 espace(s) initial(aux) |

En plus de ces 32 textes, **6 textes** n'avaient qu'un défaut d'espace de tête (`n01`, `n02`, `x02`,
`x03`, `s02`, `s03`) ; ils sont réparés par la règle (e). La liste complète des 40 textes, avec tous les
spans, est dans le JSON.

### 2.3 Six cas représentatifs

**d03 — date**
~~~text
La réunion du 12.03.2024 a été reportée au 15.04.2024.
~~~

Attendu : **1** phrase(s) — `La réunion du 12.03.2024 a été reportée au 15.04.2024.`

Avant : **5** phrase(s) — `La réunion du 12.` | `03.` | `2024 a été reportée au 15.` | `04.` | `2024.`

Après : **1** phrase(s) — `La réunion du 12.03.2024 a été reportée au 15.04.2024.`


**u01 — URL+query**
~~~text
Visitez https://example.com/docs?page=2 pour la documentation.
~~~

Attendu : **1** phrase(s) — `Visitez https://example.com/docs?page=2 pour la documentation.`

Avant : **3** phrase(s) — `Visitez https://example.` | `com/docs?` | `page=2 pour la documentation.`
Fausses questions : ['com/docs?']

Après : **1** phrase(s) — `Visitez https://example.com/docs?page=2 pour la documentation.`


**a01 — abréviation M.**
~~~text
M. Dupont, le directeur, a annoncé sa retraite.
~~~

Attendu : **1** phrase(s) — `M. Dupont, le directeur, a annoncé sa retraite.`

Avant : **2** phrase(s) — `M. Dupont, le directeur, a annoncé sa retraite.` | ` Dupont, le directeur, a annoncé sa retraite.`
Chevauchements : [[0, 47, 2, 47]]

Après : **1** phrase(s) — `M. Dupont, le directeur, a annoncé sa retraite.`


**a04 — etc. majuscule**
~~~text
Il y a des pommes, des poires, etc. Il part demain.
~~~

Attendu : **2** phrase(s) — `Il y a des pommes, des poires, etc.` | `Il part demain.`

Avant : **2** phrase(s) — `Il y a des pommes, des poires, etc. Il part demain.` | ` Il part demain.`
Chevauchements : [[0, 51, 35, 51]]

Après : **2** phrase(s) — `Il y a des pommes, des poires, etc.` | `Il part demain.`


**g01 — guillemets**
~~~text
« Bonjour. » Elle part.
~~~

Attendu : **2** phrase(s) — `« Bonjour. »` | `Elle part.`

Avant : **2** phrase(s) — `« Bonjour.` | ` » Elle part.`

Après : **2** phrase(s) — `« Bonjour. »` | `Elle part.`


**t01 — titre markdown**
~~~text
# Notes de réunion

Le budget 2025 a été validé.
~~~

Attendu : **2** phrase(s) — `# Notes de réunion` | `Le budget 2025 a été validé.`

Avant : **1** phrase(s) — `# Notes de réunion

Le budget 2025 a été validé.`

Après : **2** phrase(s) — `# Notes de réunion` | `Le budget 2025 a été validé.`


**t03 — liste avec points**
~~~text
1. Ouvrir le fichier.
2. Lire la première ligne.
~~~

Attendu : **2** phrase(s) — `1. Ouvrir le fichier.` | `2. Lire la première ligne.`

Avant : **4** phrase(s) — `1.` | ` Ouvrir le fichier.` | `
2.` | ` Lire la première ligne.`

Après : **2** phrase(s) — `1. Ouvrir le fichier.` | `2. Lire la première ligne.`


**x01 — ellipse minuscule**
~~~text
Il hésite... puis il part.
~~~

Attendu : **1** phrase(s) — `Il hésite... puis il part.`

Avant : **2** phrase(s) — `Il hésite...` | ` puis il part.`

Après : **1** phrase(s) — `Il hésite... puis il part.`


### 2.4 Effet sur POS, syntagmes et attachement

- **Le patch de frontières ne change aucun POS, aucun syntagme, aucun attachement** : **0/40** textes
  modifiés sur ces trois niveaux, et **0/612** sur le gold. C'est structurel : `_pos` et `_syntagmes_*`
  ne lisent pas `_phrases` ; seuls `phrase`, `pragmatique` et `discourse` en dépendent.
- **38/40** textes changent de libellés `phrase` et de spans d'acte ; **5/40** changent de connecteurs
  `discours` (fragments d'URL supprimés, spans corrigés). Les **actes faux** passent de **63/102** à
  **0/59**.
- **Syntagmes traversant une frontière** : **0 → 2** (`t01`, `t02`). Ce n'est pas la frontière qui est
  fausse : le chunker S traite `de réunion\n\nLe budget` et `les coûts\n- Échéance` comme des syntagmes.
  La règle (f) révèle ce défaut du chunker (P0-3/P1-4), elle ne le crée pas.
- **Patch B (tokénisation)** : sur les 40 textes, **477 → 362 tokens** (−115), **273 → 232 POS** (−41),
  **47 POS dans des zones protégées avant, 6 après** (les 6 restants sont du code/identifiant/e.g.) ;
  donc **41 POS de fragments URL/courriel/chemin supprimés**, cohérent avec la perte de 41 POS.
  **7 textes** changent de syntagmes : les GV fantômes `https`, `docs`, `a` disparaissent, des GV réels
  (`est`, `ouvrez`, `cherchez`) apparaissent. Sur le gold : **0 token changé, 0 POS/F1/attachement
  changé**.

## 3. Les règles candidates, une par une

| règle | textes exacts (seule) | coupures retirées* | fusions réparées* | espaces retirés* | fausses questions retirées* | Δ dev POS / F1 / att | Δ test POS / F1 / att |
|---|---:|---:|---:|---:|---:|---|---|
| a — décimaux/dates/listes | 6/40 | 15 | 0 | 2 | 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| b — abréviations | 8/40 | 10 | 0 | 10 | 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| c — URL/courriels/chemins/code | 10/40 | 19 | 0 | 0 | 5 | 0 / 0 / 0 | 0 / 0 / 0 |
| d — ponctuation répétée/ellipse | 3/40 | 1 | 0 | 1 | 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| e — espaces/phrases vides | 13/40 | 0 | 0 | 31 | 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| f — saut de ligne structurel | 4/40 | 0 | 2 | 1 | 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| **toutes** | **40/40** | 45 | 2 | 31 | 5 | 0 / 0 / 0 | 0 / 0 / 0 |

\* Les colonnes « retirées » sont mesurées **contre le scanner neutre** (même balayage, toutes règles
désactivées), pas contre l'original : l'original a un bug de chevauchement (9) que le balayage unique
supprime déjà sans règle. Les valeurs absolues par règle sont dans le JSON (`ablations_40`).

**Lecture.** (a) répare les décimaux, dates, versions, IP et numéros de liste ; (b) les civilités et
`etc.` ; (c) les URL, courriels, chemins, code et identifiants pointés, et **supprime à elle seule les
5 fausses questions** ; (d) l'ellipse suivie d'une minuscule ; (e) les espaces de tête (le plus grand
gain de textes exacts à lui seul, 13/40) ; (f) les titres et listes sans ponctuation finale. **Toutes**
les règles donnent **40/40**.

### 3.1 Gain dev/test par règle

| lecture | POS dev | F1 dev | att dev | acte dev | POS test | F1 test | att test | acte test |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| original | 0.8490 | 0.6439 | 0.9816 | 1.0000 | 0.8511 | 0.6552 | 0.9868 | 0.9895 |
| neutre | 0.8490 | 0.6439 | 0.9816 | 1.0000 | 0.8511 | 0.6552 | 0.9868 | 0.9895 |
| regle_a | 0.8490 | 0.6439 | 0.9816 | 1.0000 | 0.8511 | 0.6552 | 0.9868 | 0.9895 |
| regle_b | 0.8490 | 0.6439 | 0.9816 | 1.0000 | 0.8511 | 0.6552 | 0.9868 | 0.9895 |
| regle_c | 0.8490 | 0.6439 | 0.9816 | 1.0000 | 0.8511 | 0.6552 | 0.9868 | 0.9895 |
| regle_d | 0.8490 | 0.6439 | 0.9816 | 1.0000 | 0.8511 | 0.6552 | 0.9868 | 0.9895 |
| regle_e | 0.8490 | 0.6439 | 0.9816 | 1.0000 | 0.8511 | 0.6552 | 0.9868 | 0.9895 |
| regle_f | 0.8490 | 0.6439 | 0.9816 | 1.0000 | 0.8511 | 0.6552 | 0.9868 | 0.9895 |
| toutes | 0.8490 | 0.6439 | 0.9816 | 1.0000 | 0.8511 | 0.6552 | 0.9868 | 0.9895 |

**Toutes les lectures sont identiques au chiffre près.** Les deltas par règle sont donc **0** sur POS,
F1 syntagmes, attachement et acte, sur dev comme sur test. Le seul déplacement est le **span** de
2 phrases du gold (r308, r318), dû à la règle (e) ; **la valeur d'acte ne change pas**. C'est le
résultat attendu : le gold ne contient **aucun** des phénomènes traités (0 chiffre, 0 URL, 0 courriel,
0 chemin, 0 abréviation, 0 ellipse, 0 saut de ligne). **P0-4 ne peut pas améliorer le F1 syntagmes** :
la frontière est en aval des syntagmes.

## 4. Contrôles négatifs

### 4.1 Cas construits

| cas | attendu | avant | après | verdict |
|---|---:|---:|---:|---|
| Il part. Elle reste. | 2 | 2 | 2 | deux phrases réelles restent deux phrases |
| Il part. Elle reste. Nous attendons. | 3 | 3 | 3 | aucune fusion |
| Il hésite... Elle part. | 2 | 2 | 2 | ellipse + majuscule coupe |
| Il y a des pommes, des poires, etc. Il part demain. | 2 | 2 | 2 | etc. + majuscule coupe ; la règle « minuscule » ne fusionne pas |
| Il consulte le Dr. Elle est partie. | 2 | 2 | 2 | un titre suivi d'un pronom de début de phrase coupe |
| Le 12.03.2024. Il part. | 2 | 4 | 2 | le point final de la date coupe, les points internes non |
| Visitez https://example.com?q=1. Que voyez-vous ? | 2 | 4 | 2 | le ? de la requête n'est pas une question ; le ? final oui |
| M. Dupont… | 1 | 2 | 1 | plus de chevauchement |
| « Bonjour. » Elle part. | 2 | 2 | 2 | le guillemet fermant reste avec la première phrase |

Le contrôle demandé — **`Il part. Elle reste.` reste deux phrases** — passe, ainsi que sa version à
trois phrases. Les règles ne fusionnent pas deux phrases réelles ; elles ne coupent pas non plus
`M. Dupont`, `Dr. Martin`, `12.5`, `12.03.2024` ou `https://example.com/docs?page=2`.

### 4.2 Le gold n'est pas cassé

| contrôle | avant | après | verdict |
|---|---|---|---|
| POS (612 textes) | référence | identique | 0 texte différent |
| F1 syntagmes | référence | identique | 0 texte différent |
| attachement | référence | identique | 0 texte différent |
| tokens | référence | identique | 0 texte différent (patch B) |
| nombre de phrases | référence | identique | 0 texte différent |
| spans de phrase | référence | 2 corrigés | r308, r318 : l'espace de tête n'est plus dans le span |
| valeurs d'acte | référence | identique | 0 texte différent |

Les deux spans corrigés sont :

- `r308` — `Marie lit. Elle aime les livres.` : `[10:32]` → `[11:32]` ;
- `r318` — `Marie reads. She loves books.` : `[12:29]` → `[13:29]`.

Ce sont des **corrections**, pas des régressions : la phrase ne commence plus par une espace. Aucune
métrique ne bouge (POS 0,8490 / 0,8511 ; F1 0,6439 / 0,6552 ; att 0,9816 / 0,9868 ; acte 1,0000 /
0,9895 sur dev / test).

### 4.3 Déterminisme, robustesse, temps

- **Déterminisme** : 40/40 textes identiques sur deux passes ; 500 textes aléatoires (lettres, chiffres,
  ponctuation, emoji, sauts de ligne) sans exception, spans valides, non vides, ordonnés, sans
  chevauchement, `texte[debut:fin] == valeur`.
- **Temps** : `_phrases` sur 10 000 caractères : **2,98 ms → 8,47 ms** (×2,8). L'analyse complète de
  l'audit était à 590–765 ms sur 10 000 caractères ; l'ajout est négligeable à cette échelle.
- **Patch B** : 8,97 ms contre 12,96 ms pour `_mots` sur le même texte (moins de tokens).

## 5. Patchs exacts

Deux patchs indépendants, **non appliqués** :

- **Patch A — frontières** (`_phrases`) : le patch P0-4. Il remplace la méthode par
  `return decouper_phrases(texte)` et insère les helpers avant `class Heuristique:`.
- **Patch B — tokénisation** (`_mots`) : le complément P0-4/P1-6. Il remplace la méthode par
  `return decouper_mots(texte)` et rend atteignables les alternatives `url` et `emoji`, en plus de
  `nombre`, `courriel` et `chemin`.

Les diffs ci-dessous sont générés contre `tools/bloc_linguistique.py` **tel qu'il est dans l'arbre de
travail au moment de la mesure** (`sha256 12e73b7ab2cd…`, HEAD `ed8f9414` +
modifications non committées d'un autre agent) et passent `git apply --check` sur cet arbre. **Aucun
`git apply` n'a été exécuté sur le dépôt.** Le JSON contient les mêmes diffs, le code inséré et la
méthode de remplacement.

### 5.1 Patch A — frontières de phrase

````diff
--- a/tools/bloc_linguistique.py
+++ b/tools/bloc_linguistique.py
@@ -551,6 +551,239 @@
 # --------------------------------------------------------------------------- heuristique
 
 
+# --------------------------------------------------------------------------- frontières de phrase
+# P0-4 : un point décimal, une URL, un courriel, un chemin, une abréviation, un numéro de
+# liste ou une ponctuation répétée ne coupent pas la phrase ; un saut de ligne structurel
+# la coupe. Le balayage est **unique** : aucun span ne se chevauche, aucune phrase vide.
+_FERMANTS = "»”’)]}›"
+_OUVRANTS = "«“‘([{‹"
+_TITRES = frozenset({
+    "M", "MM", "Mme", "Mmes", "Mlle", "Mlles", "Me", "Mgr", "St", "Ste",
+    "Dr", "Drs", "Pr", "Prs", "Rév", "Père", "Sr", "Sœur",
+})
+_ABREV_TOUJOURS = frozenset({
+    "cf", "p", "pp", "ex", "réf", "ref", "éd", "ed", "trad", "fig", "chap",
+    "sect", "env", "av", "al", "ibid", "id", "infra", "supra", "coll", "pl",
+    "sq", "suiv", "op", "ca", "n", "no", "nos", "vs", "art", "vol",
+})
+_ABREV_MINUSCULE = frozenset({"etc"})
+# après un titre ou une initiale, ces mots ouvrent presque sûrement une phrase
+_DEBUTS = frozenset({
+    "il", "elle", "on", "nous", "vous", "ils", "elles", "je", "tu", "ce",
+    "cette", "ces", "cet", "mais", "or", "donc", "pourtant", "cependant",
+    "toutefois", "néanmoins", "enfin", "ensuite", "puis", "alors", "ainsi",
+    "quand", "lorsque", "comme", "si", "après", "avant", "dans", "sur",
+    "sous", "avec", "sans", "pour", "par", "the", "he", "she", "it", "we",
+    "they", "you", "i", "this", "that", "but", "then", "however", "when",
+    "if", "after", "before", "finally", "thus",
+})
+_MARQUEUR = re.compile(
+    r"^\s*(?:#{1,6}\s|[-*+]\s|\d+[.)]\s|[A-Za-z][.)]\s|>\s|\||```|---\s*$)"
+)
+_URL = re.compile(r"https?://[^\s<>\"'`]+", re.I)
+_EMAIL = re.compile(r"(?<![\w.+-])[\w.+-]+@[\w-]+(?:\.[A-Za-z]{2,})+(?![\w-])")
+_DOMAINE = re.compile(
+    r"(?<![\w.-])(?:[\w-]+\.)+(?:com|org|net|fr|io|dev|ai|edu|gov|co|uk|de|ch|be|ca|info|eu)(?![\w-])",
+    re.I,
+)
+_CHEMIN = re.compile(
+    r"(?<![\w])(?:[A-Za-z]:[\\/]|\.{0,2}/)?(?:[\w.@+-]+[\\/])+[\w.@+-]+(?:\.[A-Za-z0-9]{1,8})?(?![\w])"
+)
+_EXTENSION = re.compile(
+    r"(?<![\w])(?:[\w.-]+)\.(?:py|pyi|md|rst|txt|json|jsonl|csv|tsv|ya?ml|toml|ini|cfg|sh|bash|zsh|html?|css|js|ts|jsx|tsx|svg|png|jpe?g|gif|pdf|docx?|xlsx?|pptx?|zip|tar|gz|log|sql|xml)(?![\w])",
+    re.I,
+)
+_IDENT_POINTE = re.compile(
+    r"\b[A-Za-z_]\w*(?:\.[a-z_]\w*){2,}(?![\w])|\b[A-Za-z_]\w*\.[_]\w*(?![\w])"
+)
+_ABREV_POINTEE = re.compile(r"\b(?:[A-Za-z]\.)+[A-Za-z]\b")
+_CODE_INLINE = re.compile(r"`[^`\n]+`")
+_CODE_BLOC = re.compile(r"```.*?```", re.S)
+_POINTEE = re.compile(r"(?:[A-Za-z]\.)+[A-Za-z]$")
+_MOTIFS_A_COUPER = (_URL, _EMAIL, _CHEMIN, _EXTENSION)
+
+
+def _couper_fin(texte: str, debut: int, fin: int) -> int:
+    """Retire la ponctuation de phrase collée à la fin d'une URL, d'un courriel, d'un chemin."""
+    while fin > debut and texte[fin - 1] in ".,;:!?»\"”’":
+        fin -= 1
+    while fin > debut and texte[fin - 1] == ")" and "(" not in texte[debut:fin - 1]:
+        fin -= 1
+    return fin
+
+
+def _zones_protegees(texte: str) -> list[tuple[int, int]]:
+    """Les tranches où une ponctuation n'est jamais une frontière de phrase."""
+    zones: list[tuple[int, int]] = []
+    for motif in (_URL, _EMAIL, _DOMAINE, _CHEMIN, _EXTENSION,
+                  _CODE_BLOC, _CODE_INLINE, _ABREV_POINTEE, _IDENT_POINTE):
+        for m in motif.finditer(texte):
+            debut, fin = m.start(), m.end()
+            if motif in _MOTIFS_A_COUPER:
+                fin = _couper_fin(texte, debut, fin)
+            if fin > debut:
+                zones.append((debut, fin))
+    zones.sort()
+    fusion: list[tuple[int, int]] = []
+    for debut, fin in zones:
+        if fusion and debut <= fusion[-1][1]:
+            fusion[-1] = (fusion[-1][0], max(fusion[-1][1], fin))
+        else:
+            fusion.append((debut, fin))
+    return fusion
+
+
+def _dans_zone(zones: list[tuple[int, int]], debut: int, fin: int) -> bool:
+    """Vrai si la ponctuation [debut, fin) touche une zone protégée."""
+    for d, f in zones:
+        if d >= fin:
+            break
+        if f > debut:
+            return True
+    return False
+
+
+def _mot_avant(texte: str, i: int) -> str:
+    j = i
+    while j > 0 and (texte[j - 1].isalnum() or texte[j - 1] in "'’"):
+        j -= 1
+    return texte[j:i]
+
+
+def _apres_ponctuation(texte: str, j: int) -> int:
+    n = len(texte)
+    while j < n and (texte[j].isspace() or texte[j] in _FERMANTS):
+        j += 1
+    return j
+
+
+def _mot_suivant(texte: str, p: int) -> str:
+    m = re.match(r"[^\W\d_][\w'’\-]*", texte[p:p + 80], re.UNICODE)
+    return m.group() if m else ""
+
+
+def _absorber_fermants(texte: str, j: int) -> int:
+    """Absorbe « . » », « . ) » : le fermant appartient à la phrase qui se termine."""
+    n = len(texte)
+    while True:
+        k = j
+        while k < n and texte[k] in " \t":
+            k += 1
+        if k < n and texte[k] in _FERMANTS:
+            j = k + 1
+            continue
+        return j
+
+
+def _nouvelle_ligne_structurelle(texte: str, i: int, j: int) -> bool:
+    """Un saut de ligne coupe la phrase s'il est vide ou s'il borde un titre / une liste."""
+    if texte.count("\n", i, j) >= 2:
+        return True
+    avant = texte[texte.rfind("\n", 0, i) + 1:i]
+    fin = texte.find("\n", j)
+    apres = texte[j:fin if fin >= 0 else len(texte)]
+    return bool(_MARQUEUR.match(avant) or _MARQUEUR.match(apres))
+
+
+def _type_phrase(ponctuation: str) -> str:
+    if "?" in ponctuation:
+        return "interrogative"
+    if "!" in ponctuation:
+        return "exclamative"
+    return "déclarative"
+
+
+def _est_frontiere(texte: str, i: int, j: int, zones: list[tuple[int, int]]) -> bool:
+    n = len(texte)
+    terme = texte[i:j]
+    # (a) un point entre deux chiffres est décimal (12.5, 12.03.2024, 192.168.1.10)
+    if terme == "." and 0 < i < n - 1 and texte[i - 1].isdigit() and texte[i + 1].isdigit():
+        return False
+    # (a bis) un numéro de liste en début de ligne (1. Ouvrir) n'est pas une phrase
+    if terme == "." and 0 < i < n - 1 and texte[i + 1].isspace():
+        avant = texte[texte.rfind("\n", 0, i) + 1:i].strip()
+        if avant.isdigit() and len(avant) <= 3:
+            return False
+    # (d) une ponctuation répétée ne fait qu'une frontière ; une ellipse suivie d'une
+    # minuscule continue la phrase (« Il hésite... puis il part. »)
+    if terme == "…" or (len(terme) >= 2 and set(terme) <= {".", "…"}):
+        p = _apres_ponctuation(texte, j)
+        if p < n and (texte[p].islower() or texte[p].isdigit()):
+            return False
+    # (b) abréviations : minuscule après « etc. » n'ouvre pas une phrase ; « M. Dupont »,
+    # « Dr. Martin », « p. ex. » et « cf. » ne coupent pas.
+    if terme == ".":
+        mot = _mot_avant(texte, i)
+        p = _apres_ponctuation(texte, j)
+        suivant = texte[p] if p < n else ""
+        if mot:
+            if mot in _TITRES or (len(mot) == 1 and mot.isupper()):
+                if not suivant:
+                    return True
+                if not (suivant.isalnum() or suivant in _OUVRANTS):
+                    return True
+                if suivant.isalpha() and _mot_suivant(texte, p).casefold() in _DEBUTS:
+                    return True
+                return False
+            if mot in _ABREV_MINUSCULE:
+                return not (suivant.islower() or suivant.isdigit())
+            if mot in _ABREV_TOUJOURS:
+                return not (suivant.isalnum() or suivant in _OUVRANTS)
+            if _POINTEE.search(texte[max(0, i - 16):i]):
+                if not suivant:
+                    return True
+                if suivant.isalpha() and _mot_suivant(texte, p).casefold() in _DEBUTS:
+                    return True
+                return not (suivant.isalpha() or suivant.isdigit())
+            if suivant == "-" and len(mot) == 1:
+                return False
+    return True
+
+
+def decouper_phrases(texte: str) -> list[tuple[int, int, str, str]]:
+    """Les phrases d'un texte libre, sans chevauchement et sans blanc de tête."""
+    n = len(texte)
+    if not n:
+        return []
+    zones = _zones_protegees(texte)
+    sortie: list[tuple[int, int, str, str]] = []
+    debut = 0
+    i = 0
+
+    def ajouter(fin: int, typ: str) -> None:
+        nonlocal debut
+        d, f = debut, fin
+        while d < f and texte[d].isspace():
+            d += 1
+        while f > d and texte[f - 1].isspace():
+            f -= 1
+        if f > d and texte[d:f].strip():
+            sortie.append((d, f, texte[d:f], typ))
+        debut = fin
+
+    while i < n:
+        ch = texte[i]
+        if ch in "\r\n":
+            j = i
+            while j < n and texte[j].isspace():
+                j += 1
+            if _nouvelle_ligne_structurelle(texte, i, j):
+                ajouter(i, "déclarative")
+            i = j
+            continue
+        if ch not in ".!?…":
+            i += 1
+            continue
+        j = i + 1
+        while j < n and texte[j] in ".!?…":
+            j += 1
+        if not _dans_zone(zones, i, j) and _est_frontiere(texte, i, j, zones):
+            ajouter(_absorber_fermants(texte, j), _type_phrase(texte[i:j]))
+        i = j
+    ajouter(n, "déclarative")
+    return sortie
+
+
 class Heuristique:
     """L'implémentation CPU : elle étiquette la surface et **déclare** ce qu'elle ne couvre pas."""
 
@@ -595,25 +828,7 @@
 
     @staticmethod
     def _phrases(texte: str) -> list[tuple[int, int, str, str]]:
-        # frontières : ponctuation forte + espace ; on protège les abréviations et les décimales
-        motif = re.compile(r"[^.!?…]+(?:[.!?…]+|$)", re.S)
-        sortie = []
-        for m in motif.finditer(texte):
-            morceau = m.group()
-            if not morceau.strip():
-                continue
-            debut = m.start()
-            fin = m.end()
-            # une phrase qui finit par une abréviation connue n'est pas finie
-            while re.search(r"\b(?:M|MM|Mme|Dr|Pr|etc|cf|p|pp|art|vol)\.\s*$", texte[debut:fin]):
-                suivant = motif.search(texte, fin)
-                if not suivant:
-                    break
-                fin = suivant.end()
-                morceau = texte[debut:fin]
-            typ = "interrogative" if "?" in morceau else ("exclamative" if "!" in morceau else "déclarative")
-            sortie.append((debut, fin, morceau, typ))
-        return sortie
+        return decouper_phrases(texte)
 
     @staticmethod
     def _negation(phrase: str) -> bool:
````

### 5.2 Patch B — tokénisation (optionnel)

````diff
--- a/tools/bloc_linguistique.py
+++ b/tools/bloc_linguistique.py
@@ -551,6 +551,53 @@
 # --------------------------------------------------------------------------- heuristique
 
 
+# --------------------------------------------------------------------------- tokens
+# P0-4 / P1-6 : l'URL, le courriel, le chemin, le nombre et l'emoji sont **un** token ;
+# les alternatives mortes `url` et `emoji` redeviennent atteignables.
+_MOTIF_MOTS = re.compile(
+    r"https?://[^\s<>\"'`]*[^\s<>\"'`.,;:!?]"
+    r"|[\w.+-]+@[\w-]+(?:\.[A-Za-z]{2,})+"
+    r"|\b(?:[\w-]+\.)+(?:com|org|net|fr|io|dev|ai|edu|gov|co|uk|de|ch|be|ca|info|eu)\b"
+    r"|(?:\.{0,2}/)?(?:[\w.@+-]+/)+[\w.@+-]+\.[A-Za-z0-9]{1,8}"
+    r"|/(?:[\w.@+-]+/)+[\w.@+-]+"
+    r"|\b[\w.@+-]+\.(?:py|pyi|md|rst|txt|json|jsonl|csv|tsv|ya?ml|toml|ini|cfg|sh|bash|zsh|html?|css|js|ts|jsx|tsx|svg|png|jpe?g|gif|pdf|docx?|xlsx?|pptx?|zip|tar|gz|log|sql|xml)\b"
+    r"|\b[A-Za-z_]\w*(?:\.[a-z_]\w*){2,}\b|\b[A-Za-z_]\w*\.[_]\w*\b"
+    r"|\d+(?:[.,]\d+)*"
+    r"|\b[ldmtsnLDMTNS]['’](?=\w)"
+    r"|\w+(?:['’\-]\w+)*"
+    r"|[\U0001F300-\U0001FAFF]"
+    r"|[^\w\s]",
+    re.I,
+)
+_DOMAINE_SEUL = re.compile(
+    r"(?:[\w-]+\.)+(?:com|org|net|fr|io|dev|ai|edu|gov|co|uk|de|ch|be|ca|info|eu)", re.I)
+
+
+def decouper_mots(texte: str) -> list[tuple[int, int, str, str]]:
+    """Les tokens du bloc : la surface, son span et son type, sans recouvrement."""
+    sortie: list[tuple[int, int, str, str]] = []
+    for m in _MOTIF_MOTS.finditer(texte):
+        t = m.group()
+        if t.lower().startswith(("http://", "https://")):
+            typ = "url"
+        elif re.fullmatch(r"[\w.+-]+@[\w-]+(?:\.[A-Za-z]{2,})+", t):
+            typ = "courriel"
+        elif _DOMAINE_SEUL.fullmatch(t):
+            typ = "url"
+        elif re.fullmatch(r"\d+(?:[.,]\d+)*", t):
+            typ = "nombre"
+        elif len(t) == 1 and ord(t) >= 0x1F300:
+            typ = "emoji"
+        elif re.fullmatch(r"[^\w\s]", t):
+            typ = "ponctuation"
+        elif len(t) > 1 and ("/" in t or "\\" in t):
+            typ = "chemin"
+        else:
+            typ = "mot"
+        sortie.append((m.start(), m.end(), t, typ))
+    return sortie
+
+
 class Heuristique:
     """L'implémentation CPU : elle étiquette la surface et **déclare** ce qu'elle ne couvre pas."""
 
@@ -576,22 +623,7 @@
     # -- tokens -------------------------------------------------------------
     @staticmethod
     def _mots(texte: str) -> list[tuple[int, int, str, str]]:
-        motif = re.compile(r"\b[ldmtsnLDMTNS]['’](?=\w)|\w+(?:['’\-]\w+)*|\d+(?:[.,]\d+)*|https?://\S+|[\U0001F300-\U0001FAFF]|[^\w\s]")
-        sortie = []
-        for m in motif.finditer(texte):
-            t = m.group()
-            if t.startswith(("http://", "https://")):
-                typ = "url"
-            elif t[0].isdigit():
-                typ = "nombre"
-            elif re.fullmatch(r"[^\w\s]", t):
-                typ = "ponctuation"
-            elif len(t) == 1 and ord(t) >= 0x1F300:
-                typ = "emoji"
-            else:
-                typ = "mot"
-            sortie.append((m.start(), m.end(), t, typ))
-        return sortie
+        return decouper_mots(texte)
 
     @staticmethod
     def _phrases(texte: str) -> list[tuple[int, int, str, str]]:
````

### 5.3 Ordre et vérification

1. `git apply --check` (fait, sans écriture) ;
2. appliquer A seul pour les frontières, ou A puis B pour le P0-4 complet ;
3. rejouer `python3 tools/tests/linguistique/evaluer_gold.py` : les valeurs doivent rester identiques ;
4. rejouer les 40 cas du JSON (ou les ajouter à la porte) : **40/40 exacts** ;
5. vérifier `git diff` : aucune autre modification.

## 6. Ce qui pourrait rendre ce résultat faux

- **Banc écrit par l'auteur** : 40 textes choisis pour couvrir les cas de l'audit, pas un échantillon
  aléatoire. Les catégories pathologiques sont surreprésentées ; le taux de 32/40 n'est pas une
  prévalence.
- **Gold aveugle au phénomène** : 0 chiffre, 0 URL, 0 courriel, 0 chemin, 0 abréviation, 0 ellipse,
  0 saut de ligne dans les 612 phrases. Le delta 0 dev/test ne prouve pas que la règle est bonne, il
  prouve qu'elle ne casse pas ce gold.
- **Règle (f) et chunker** : les 2 syntagmes qui traversent une ligne (`t01`, `t02`) sont un défaut du
  chunker S, pas de la frontière ; si le chunker est réparé, ce compteur doit revenir à 0.
- **Ellipse + minuscule** : choix de style. Un SMS qui commence une phrase par une minuscule après
  `...` sera fusionné. Retirer la branche ellipse de `_est_frontiere` rétablit la coupure stricte.
- **Abréviations** : `_DEBUTS` est une liste finie ; `Le Dr. Paul arrive` reste ouvert (voulu), mais un
  titre suivi d'un mot inconnu qui ouvre une phrase peut fusionner. `12. Il part.` en début de ligne est
  pris pour un numéro de liste.
- **Tokénisation** : les types `courriel` et `chemin` sont **additifs** ; si un client impose une
  énumération fermée, les replier sur `mot`/`url`. Les URL exotiques (parenthèses non appariées,
  ponctuation finale ambiguë) restent des cas limites.
- **Temps** : `_phrases` est ~2,8× plus lent ; si un appelant boucle sur des millions de phrases
  courtes, mémoïser les regex ou précompiler le scanner.

## 7. Verdict et suites

- **P0-4 frontières** : corrigé sur le banc (40/40), **sans régression gold** ; le patch A est prêt.
- **P0-4 tokénisation** : patch B proposé ; il faut décider du contrat des types `courriel`/`chemin`.
- **Prochaine action mesurable** : ajouter les 40 cas (ou un sous-ensemble) à
  `tools/tests/linguistique/` et à la porte `tools/porte-bloc-linguistique.sh`, puis rejouer l'audit
  produit sur les 50 phrases pour vérifier la disparition des 6/46 frontières cassées et des 3 fausses
  questions. **Aucune modification de `docs/pilotage/`, `AGENTS.md`, `journal/`, `tools/structures/`,
  `data/` ni des natifs n'a été faite.**
