# B13 — Contrat d'interface L ↔ S : les subordonnées REL/SUB

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
> mesure faite — le contrat `s/v1` **n'est pas tenu** par S. Le générateur S n'a pas été modifié
> par cette fiche ; l'arbre de travail porte un **correctif non committé** du bloc (13:51) qui
> applique la règle SUB → verbe. Les deux états sont mesurés ci-dessous.
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
> [`generateur.py`](../tools/structures/generateur.py),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) rejoué (`ok: true`,
> **état courant : labels 145, exact 137, exactitude spans 0,9448, hasard 0,0042** ; état
> initial, avant le correctif : exact 123, 0,8483).
> **Le chiffre** : sur **239** cibles d'attachement du gold, **94** n'ont pas de segment prédit au
> bon span — **48 REL, 33 SUB, 13 GP**. **81** sont des REL/SUB : **60 absentes**, **19 plus
> larges**, **2 plus étroites**. Le bloc ne répare aucune des 81 ; S seul place **62/143** spans
> REL/SUB (43,4 %). L'attachement REL/SUB passe de **54/62** (état initial) à **60/62** (état
> courant), mais les spans ne bougent pas. L'interface réelle reste **privée** (`_segmente`,
> `_tokens`) et **incomplète** (pas d'antécédent typé, pas de gouverneur à droite, pas de langue,
> pas de refus).

## 1. Le constat : l'interface actuelle est un couplage privé

S n'expose aujourd'hui que deux surfaces publiques, et aucune ne porte le contrat complet ; le
bloc complète avec une troisième, privée :

| surface | fichier | ce qu'elle rend | ce qui manque |
|---|---|---|---|
| `analyser(texte, max_candidats=4)` | `generateur.py:516` | jusqu'à 4 candidats ; **seul le dernier segment ambigu** (GP/REL, jamais SUB) porte `attachement` | les cibles des autres segments, les SUB, un type de cible |
| `structure(texte, roles=True)` | `generateur.py:621` | `[s.dict() for s in segs]` | `Segment.dict()` (`:306`) **omet** `cible_nom`, `cible_gp`, `cible_verbe` |
| `_segmente(texte, toks)`, `_tokens(texte)` | `generateur.py:346, 175` | la liste complète des `Segment` avec leurs `cible_*` | ce sont des **fonctions privées** |

Le bloc fait donc de S un usage de fait privé :

- `Heuristique._syntagmes_s` importe `generateur.analyser(texte)` ;
- `Heuristique._cibles_s` importe `generateur._segmente` et `generateur._tokens`, **re-segmente
  la phrase une seconde fois**, puis écrase les trois canaux en un seul :
  `(s.cible_gp or s.cible_nom or s.cible_verbe)` — priorité **GP > nom > verbe**, sans type ni
  direction ;
- pour un REL/SUB, l'**état initial** n'utilisait pas ce canal : il prenait le `GN` le plus à
  gauche dans `cands[0]["segments"]` et le réduisait avec `_tete_nom` ; à défaut
  seulement, il retombait sur `_cible_proche` (le verbe du GV le plus proche). Le
  **correctif non committé** (13:51) prend le **segment précédent** : `GV` → `_verbe_dans` (SUB),
  `GN` → `_tete_nom` (REL), puis `_cible_proche` en repli.

Trois défauts en découlent. **Un** : aucune version de contrat, donc une modification de S casse L
silencieusement. **Deux** : la phrase est segmentée deux fois par S (deux appels indépendants), et
les deux résultats pourraient diverger. **Trois** : la règle REL/SUB est dans **L**, pas dans S ;
le correctif courant la code en dur (`GV → verbe`, `GN → nom`) et valide 60/62, mais S ne fournit
toujours ni le type d'antécédent, ni la direction du gouverneur : le contrat reste implicite, et
les 81 spans REL/SUB restent chez S. Or la mesure (§ 4, POS du gold) montre que le gold veut un
**antécédent nominal** pour REL (74/74) et un **verbe gouverneur** pour SUB (69/69).

## 2. Le contrat `s/v1`

### 2.1 L'entrée : une seule fonction, un seul appel

Le point d'entrée est **`structure(texte, roles=True, langue=None) -> list[dict]`**, étendu — pas
une nouvelle API parallèle : c'est déjà la fonction publique qui rend des dicts. Le module expose
`CONTRAT = "s/v1"`. Le bloc appelle `structure()` **une fois par phrase** et en tire à la fois les
segments et les cibles ; `_segmente`/`_tokens` ne sont plus importés par L.

Invariants vérifiables sur la sortie :

1. **span demi-ouvert** : `0 <= debut < fin <= len(texte)` et `texte[debut:fin] == texte` ;
2. **partition** : deux segments d'une même phrase ne se chevauchent pas ; pas de doublon
   `(type, debut, fin)` ; l'ordre est l'ordre du texte ;
3. **déterminisme** : même entrée → même sortie, sans mutation de l'entrée ;
4. **ensembles fermés** : `type ∈ {GN, GV, GP, REL, SUB}`, `statut ∈ {sur, ambigu, refus}`,
   `sous_type` et `raison` dans des listes fermées ;
5. **refus explicite** : `statut="refus"` + `raison`, jamais `None` ni `{}` silencieux.

### 2.2 Les champs

| champ | type | requis | sens |
|---|---|---|---|
| `type` | `"GN"｜"GV"｜"GP"｜"REL"｜"SUB"` | oui | le type structural |
| `debut`, `fin` | `int` | oui | span demi-ouvert, `texte[debut:fin] == texte` |
| `texte` | `str` | oui | la surface exacte du span |
| `sous_type` | `"relative"｜"contenu"｜"circonstancielle"｜"autre"` | REL/SUB | structurel, **pas** sémantique |
| `marqueur` | `{debut, fin, texte}｜None` | REL/SUB | le token subordonnant, **élision incluse** (`qu'il` → `qu'`) ; `None` = relative sans marqueur |
| `cible` | `cible｜None` | REL/SUB | le support d'attachement (voir 2.3) |
| `cibles` | `list[cible]` | non | les candidats ordonnés ; `cible` = le premier |
| `confiance` | `float` 0..1 | oui | confiance du segment |
| `statut` | `"sur"｜"ambigu"｜"refus"` | oui | `ambigu` ⇒ lire `cibles` |
| `langue` | `str` | oui | `fr`, `en`, `und` — la langue effective du traitement |
| `role` | `str` | non | **informatif, local à S** ; ne pas l'utiliser pour l'attachement |
| `parent`, `profondeur`, `niveau` | `int` | non | affichage / arbre ; `parent` n'est **pas** une cible |

Une `cible` est :

| champ | type | requis | sens |
|---|---|---|---|
| `genre` | `"GN"｜"GV"｜"GP"` | oui | la classe du support |
| `debut`, `fin`, `texte` | `int`, `int`, `str` | oui | le span du support |
| `direction` | `"gauche"｜"droite"｜"interne"` | oui | position du support par rapport au segment |
| `tete` | `str｜None` | non | tête lexicale *best effort* (nom ou verbe) ; **L la recalcule** avec `_tete_nom` / `_verbe_dans` |
| `tete_debut`, `tete_fin` | `int｜None` | non | span de la tête |
| `confiance` | `float` 0..1 | non | confiance de la cible |

`parent` et `profondeur` restent des champs d'arbre : `construire_arbre` (`:319`) choisit le
segment le plus proche à gauche, ce qui **n'est pas** la cible du gold (pour un REL après un GP,
le parent peut être le GP, pas le GN antécédent). L'attachement se lit dans `cible`, jamais dans
`parent`.

### 2.3 Les cibles, par type

- **REL** : `cible.genre = "GN"`, `cible.direction = "gauche"`, `cible.texte` = le GN antécédent
  (`Le livre`), `cible.tete` = sa tête (`livre`). Gold : **74/74** cibles sont un antécédent
  nominal (73 `NOUN`, 1 `PRON`) à gauche. C'est le seul **type** où la règle « tête du GN à
  gauche » est juste.
- **SUB** : `cible.genre = "GV"`, `cible.direction` = `gauche` (42/69), `droite` (26/69) ou
  `interne` (1/69), `cible.tete` = le **verbe gouverneur**. Gold : **69/69** cibles sont un
  `VERB` — 42 à gauche (`Je pense que…` → `pense`), 26 à droite (`Quand il pleut, je reste` →
  `reste`), 1 interne (`Peut-être qu'il viendra` → `viendra`, cas d'annotation limite).
- **GP** : `genre = "GV"` (verbe gouverneur) ou `"GN"` (nom complété d'un génitif),
  `direction = "gauche"`. Le canal `cible_gp` actuel n'est **pas** ce champ : c'est la tête du GP
  le plus proche à gauche, il vaut `None` sur 1097/1101 segments et **0/89** REL/SUB — il ne doit
  pas servir de cible.

**Ce que S ne fait pas** : il ne choisit pas la convention (nom vs verbe), il ne réduit pas la
tête (il donne le span), il ne colle pas trois canaux en un. **Ce que L fait** : il réduit la tête
(`_tete_nom` pour un GN, `_verbe_dans` pour un GV), choisit le canal **par type** et par
`direction`, et peut ignorer `cible.tete` s'il la juge fausse. S = structure, L = lexique et
convention.

### 2.4 Ce que L doit faire (repli)

1. **REL → antécédent nominal** : `cible.genre == "GN"`, réduire avec `_tete_nom`. C'est déjà le
   comportement actuel, et il est juste 26/26 sur les spans exacts.
2. **SUB → verbe gouverneur** : `cible.genre == "GV"`, réduire avec `_verbe_dans`, **accepter
   `direction="droite"`**. Ne **jamais** prendre le GN sujet à gauche : c'est l'erreur des 6 cas
   synthétiques mesurés. Le correctif non committé applique cette règle (sous la forme « segment
   précédent GV → verbe ») : **34/36** sur les SUB au span exact, contre **28/36** dans l'état
   initial (§ 3.6).
3. **GP → verbe** (ou nom pour un génitif) : le comportement actuel `_cible_proche` est conservé.
4. **Langue** : passer `lg` à `structure(texte, langue=lg)`. Si S refuse la langue, L ne laisse pas
   S traiter l'anglais avec les marqueurs français : il utilise son propre repli ou ne produit
   aucun label, et l'écrit dans `trace`.
5. **Une seule segmentation** : consommer `structure()` ; ne plus appeler `analyser()` **et**
   `_segmente()`. Si S n'est pas en `s/v1`, un adaptateur `s/v0` isole `_cibles_s` et marque
   `meta["contrat"] = "s/v0"` ; il lit alors les trois canaux bruts, sans le `or` prioritaire.
6. **Rôle** : ne pas l'utiliser pour l'attachement. `sous_type` est le champ structurel ;
   `role` reste local à S tant qu'un enum partagé n'existe pas (accord mesuré : REL 7/26,
   SUB 15/36 sur les spans exacts).

### 2.5 Refus et versions

`statut="refus"` avec `raison ∈ {"langue_non_couverte", "texte_vide", "conflit", "version"}` et
**aucun segment** pour la phrase. L'enregistre le refus dans `Annotation.trace` et applique son
repli ; il ne fabrique pas un GV couvrant la phrase (c'est ce que fait S aujourd'hui sur
l'anglais, et c'est la cause des 54 échecs anglais). Si `CONTRAT` est absent, L suppose `s/v0`,
le trace, et n'importe pas de nom privé sans ce marqueur.

## 3. L'écart mesuré

### 3.1 Dispositif

- **Gold** : `tools/tests/linguistique/gold.json` (20) + `gold_reel.json` (432) +
  `gold_synthetique.json` (160) = **612 phrases**, **1863 segments**, **239 cibles**
  (`GP` 96, `REL` 74, `SUB` 69).
- **Bloc** : `Heuristique().analyser(texte, langue)` ; les labels sont les étiquettes de niveau
  `syntagme` ; le span est exact si `(type, debut, fin)` est présent. Sinon : `aucun` si aucun
  segment du même type ne chevauche, `plus large` s'il contient le span gold, `plus étroit` s'il
  est contenu, `coupé` sinon.
- **S seul** : `generateur._segmente(texte, generateur._tokens(texte))` — l'API privée, faute
  d'API publique portant les cibles. Même classement de spans.
- **Cibles** : `cible_nom` réduite par `_tete_nom`, `cible_verbe` par `_verbe_dans`, comparaison
  normalisée (NFD, sans casse) à `cible` du gold.
- **Deux états** : l'**état initial** (celui du début de session, avant le correctif du bloc) et
  l'**état courant** (correctif non committé de 13:51, qui applique SUB → segment précédent et
  change le POS de l'évaluateur). Les spans `94 / 81 / 62` sont identiques sur les deux ; seul
  l'attachement change (123/145 → 137/145).
- **Recette** : le script de mesure était éphémère (`/tmp`), la mission n'autorisant que deux
  fichiers neufs ; les règles ci-dessus suffisent à le refaire. Contrôle indépendant :
  `python3 tools/tests/linguistique/evaluer_gold.py --json /tmp/eval_gold.json` → courant
  `labels 145`, `exact 137`, `exact_taux_span 0,9448` ; initial `exact 123`, `0,8483` ;
  `attachement_hasard 1/239 = 0,0042`.

### 3.2 Les 94 spans du bloc

| type | exact | aucun | plus large | plus étroit | **échecs** |
|---|---:|---:|---:|---:|---:|
| **REL** | 26 | 28 | 19 | 1 | **48** |
| **SUB** | 36 | 32 | 0 | 1 | **33** |
| **GP** | 83 | 5 | 6 | 2 | **13** |
| **tout** | **145** | **65** | **25** | **4** | **94** |

Les **81** REL/SUB se répartissent en **60 absentes**, **19 plus larges** et **2 plus étroites**.
L'union du chunker ne répare **aucune** des 81 : elle ajoute 15 labels `REL`, dont 5 recouvrent une
REL du gold en « plus large » et 10 ne recouvrent aucune REL cible (voir § 4).

### 3.3 S seul sur les REL/SUB

| mesure | S seul | bloc (S + union) |
|---|---:|---:|
| cibles REL/SUB | 143 | 143 |
| **exact** | **62 (43,4 %)** | **62 (43,4 %)** |
| aucun | 60 | 60 |
| plus large | 18 | 19 |
| plus étroit | 3 | 2 |
| **échecs** | **81** | **81** |

À un cas près, l'union déplace une REL de « plus étroite » à « plus large » sans la rendre exacte.
S produit par ailleurs **51 segments REL** et **38 SUB**, contre **74** et **70** dans le gold :
la couverture de production est déjà incomplète (68,9 % et 54,3 %).

| langue | cibles REL | exact REL | cibles SUB | exact SUB | échecs REL/SUB |
|---|---:|---:|---:|---:|---:|
| **fr** | 46 | 26 | 43 | 36 | **27** |
| **en** | 28 | 0 | 26 | 0 | **54** |
| **tout** | 74 | 26 | 69 | 36 | **81** |

**54 des 81 échecs sont anglais** : S ne connaît que les marqueurs français (`RELATIFS`,
`SUBORD_SIMPLE`, `SUBORD_QUE`, `SUBORD_ELIDE`, `generateur.py:22, 52-58`) et traite `that`,
`where`, `who`, `because`, `although`, `when`, `if`, `while` comme des mots ordinaires. Les **27
échecs français** se répartissent en **18 REL larges**, **2 REL étroites**, **6 SUB absentes** et
**1 SUB étroite**.

| source | cibles REL/SUB | exact | échecs |
|---|---:|---:|---:|
| hand | 3 | 2 | 1 (anglais) |
| reel | 109 | 50 | 59 (53 anglais + 6 français) |
| synthetique | 31 | 10 | 21 (16 REL larges + 5 SUB absentes) |
| **tout** | **143** | **62** | **81** |

Les 18 REL larges de S sont **16 synthétiques + 2 réelles** ; l'union en ajoute une troisième,
réelle, en déplaçant une étroite. Le gold synthétique gonfle donc l'effet « plus large », mais le
gold réel garde **52/112** spans exacts (46,4 %) et **60** échecs.

### 3.4 Ce que S ne produit pas, et pourquoi

- **60 absences.** 54 sont anglaises. Les 6 françaises sont : `car` traité comme coordination
  (`Je pars car il est tard.` → S rend `GV Je pars`, `GV il est`, `GP tard`) et **5 phrases
  synthétiques** où le GN avale le verbe principal (`ma fenêtre marche` est un GN parce que
  `marche` n'est pas dans `VERBES_FINIS`), ce qui transforme le `que` suivant en REL au lieu d'un
  SUB. La liste `VERBES_FINIS` (`:81-129`) est un lexique, pas un étiqueteur : c'est une limite
  nommée, mais elle coûte ici 5 spans.
- **18 REL larges.** La boucle REL (`:364-375`) s'arrête sur `PONCT`, `CONJ`, `RELATIF`, et sur un
  `PRON`/`AUX`/adverbe de temps **après** un verbe ; elle ne s'arrête **pas** sur un second verbe
  conjugué. `Le chat que j'ai vu dormait.` → REL `que j'ai vu dormait` (8-27 au lieu de 8-19) et
  **aucun GV** : le verbe principal `dormait` est avalé, donc la phrase n'a plus de prédicat.
  `Le chat que j'ai vu dormait.` est l'exemple canonique : le span faux détruit aussi une cible
  potentielle (`dormait`).
- **3 REL/SUB étroites.** `L'homme dont la voiture est rouge arrive.` → REL `dont la voiture`
  (8-23 au lieu de 8-33) : la boucle coupe sur `est` (`AUX` après un mot), alors que `est rouge`
  est le prédicat **de la relative**. `La fleur qui pousse ici est rare.` → REL `qui pousse`
  (9-19 au lieu de 9-23) : la boucle coupe sur `ici`, adverbe de temps **de la relative**.
  `Je sais qu'il vient demain.` → SUB `qu'il vient` (8-19 au lieu de 8-26) : la boucle coupe sur
  `demain`, adverbe de temps **de la subordonnée**. La règle « un prédicat par clause » manque :
  après le premier verbe plein, c'est le **second** verbe conjugué qui ouvre la principale, pas un
  auxiliaire ni un adverbe.

### 3.5 Les cibles de S

Sur les **62** labels REL/SUB au span exact de S :

| type | labels | `cible_nom` | dont juste | `cible_verbe` | dont juste | aucune |
|---|---:|---:|---:|---:|---:|---:|
| **REL** | 26 | 26 | **26** | 0 | 0 | 0 |
| **SUB** | 36 | 6 | **0** | 23 | **22** | 14 |
| GP (mémoire) | 51 | 41 | 17 | 34 | 32 | 2 |

Deux lectures. **Quand le span est bon**, le canal nominal de S est **parfait pour REL** (26/26,
après réduction par `_tete_nom`) et le canal verbal est bon pour SUB (22/23), mais le canal
nominal de SUB est **toujours faux** (0/6) et 14 SUB n'ont aucune cible. **Quand on aligne sur la
tête** (même `debut`, quelle que soit la `fin`), S trouve **46/74 REL** et **37/69 SUB** ; parmi
les trouvées, la cible est juste **46/46** pour REL (44 par le canal nominal, 2 par le canal
verbal) et la cible verbale **23/37** pour SUB. Autrement dit : **le span est le premier levier ;
la cible n'est pas le problème principal pour REL, mais elle l'est pour SUB** (32 SUB ne sont
même pas trouvées à leur tête).

Les cibles sont des **textes complets**, pas des têtes : `cible_nom = "Le livre"`, pas `livre` ;
`cible_verbe = "Je pense"`, pas `pense`. `cible_gp` est la tête du GP le plus proche à gauche :
**4/1101** segments, **0/89** REL/SUB — canal mort, à ne pas mettre au contrat. Aucune cible n'a
de `direction` : S ne peut pas fournir les 26 SUB à gouverneur droit, et le bloc doit les
retrouver par `_cible_proche` (ce qu'il fait déjà 12/13 fois).

### 3.6 Ce que le bloc fait de ces cibles

Sur les **62** labels REL/SUB au span exact, l'attachement passe de **54/62** (état initial) à
**60/62** (état courant) :

| type | labels | juste initial | juste courant | écart |
|---|---:|---:|---:|---:|
| REL | 26 | 26 | 26 | 0 |
| SUB | 36 | 28 | **34** | **+6** |
| GP | 83 | 69 | 77 | +8 |
| **tout** | **145** | **123 (0,8483)** | **137 (0,9448)** | **+14** |

Le **+14** se décompose : **+6 REL/SUB** (la règle SUB) et **+8 GP** (les autres changements du
même lot non committé : `_cible_s_par_genre`, `_tete_texte`, lexique élargi). La prédiction du
contrat — **+6** sur REL/SUB — est exacte au chiffre près.

Les **8** erreurs SUB de l'état initial étaient :

- **6 synthétiques** `S V que …` : le bloc prenait le GN sujet à gauche (`étoile`, `lettre`,
  `cuisine`, `chanson`, `fenêtre`) au lieu du verbe principal (`écoute`, `cherche`, `ouvre`,
  `commence`, `crie`). C'est l'erreur de **convention** : SUB → verbe, pas nom ; le correctif
  courant les répare en prenant le `GV` précédent.
- **1 impératif** : `Quand tu arrives, appelle-moi.` → `appelle-moi` (le GV est réduit au dernier
  token, le trait d'union n'est pas séparé) au lieu de `appelle` ; **reste faux**.
- **1 cas gold** : `Peut-être qu'il viendra.` → la cible gold est `viendra`, le verbe **de la
  subordonnée**, pas le gouverneur ; le bloc rend `Peut-être`. C'est le seul `direction="interne"`
  du gold ; **reste faux**, la convention doit être tranchée.

Le correctif courant laisse donc **2** erreurs nommées. Il ne répare pas les 81 spans : il ne
s'applique qu'aux 36 SUB déjà segmentées.

## 4. Contrôle négatif

| contrôle | résultat | lecture |
|---|---|---|
| **S coupé** (`Heuristique(segmenter_s=False)`) | **0/143** exact REL/SUB ; 135 absentes, 8 larges | les 62 exacts viennent **tous** de S ; le chunker seul n'en produit aucun |
| **cible au hasard** parmi les 239 cibles | **1/239 = 0,0042** | 60/62 (état courant) n'est pas du hasard |
| **permutation** des 74 cibles REL (2 000 tirages) | observé **44**, moyenne **1,31**, p95 **3**, max **6** | le canal nominal de S est prédictif sur **tout** le gold REL, pas seulement sur les 26 exacts |
| **premier GN de la phrase** sur les 26 REL exactes | **26/26** | le 26/26 REL **n'est pas** une preuve de la règle « plus proche » : sur ce sous-ensemble, le premier GN suffit. La preuve est la permutation sur 74 |
| **POS gold vs `CONVENTION_CIBLE`** | SUB : **69/69 VERB** (42 gauche, 26 droite, 1 interne) ; REL : 73 NOUN + 1 PRON, à gauche | la convention écrite (`gold_reel.py:25-32`, « SUB → antécédent, tête du GN à gauche ») est **contredite par les données** ; le 28/36 SUB de l'état initial doit beaucoup au repli `_cible_proche` (les 6 erreurs synthétiques sont les cas où un GN à gauche existe) |

Le dernier contrôle est le plus important : `_est_verbe` classait **34** cibles SUB comme des noms
(« marche », « commence »…), ce qui a fait croire à une convention mixte. Le correctif courant de
[`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) utilise désormais le **POS du
gold** et donne **116 verbes / 29 noms** (111/116 justes, 26/29) ; les 63/82 des fiches
antérieures sont périmés. C'est la bonne mesure : le gold ne mêle pas deux conventions pour SUB,
il attache **tous** les SUB à un verbe.

## 5. Limites, et ce qui pourrait rendre cette fiche fausse

- **Le gold** : 612 phrases, dont 160 synthétiques ; 452 réelles (dont 20 de `gold.py`). Les 16
  REL larges synthétiques gonflent l'effet « plus large » ; sur le réel seul, **52/112** spans
  exacts et **60** échecs. La conclusion « le span est le premier levier » tient sur les deux.
- **Deux états dans l'arbre** : le correctif non committé du bloc (13:51) et de l'évaluateur (POS)
  n'est pas de cette fiche ; les spans `94 / 81 / 62` sont stables, l'attachement est donné dans
  les deux états. Si le correctif est retiré ou amendé, les chiffres d'attachement changent, pas
  le gap de S.
- **Le classement des spans** est une heuristique de lecture des chevauchements ; un cas change
  de catégorie entre S seul et le bloc (l'union). Le total 94 est stable.
- **Le 93 de la fiche précédente** ([`rapport-pensee-spans.md`](rapport-pensee-spans.md)) est le
  même gold après le bornage du GP ; l'arbre courant donne **94** (13 GP), pas 93 (12 GP). L'écart
  d'un GP est à qualifier — hypothèse : le lexique verbal a changé depuis cette fiche. C'est le
  chiffre du contexte de la mission qui est reproduit ici.
- **`_est_verbe` n'est pas une référence** : 34 cibles SUB mal classées. Toute lecture
  « convention mixte » doit passer par le POS du gold.
- **La convention écrite est fausse pour SUB** ; c'est une décision d'auteur, pas une mesure :
  la fiche propose « SUB → verbe gouverneur », mais le gold doit être corrigé pour que la porte
  T174 et la mesure cessent de se contredire.
- **La règle SUB n'est plus une simulation** : le correctif non committé l'applique et donne
  **34/36** (60/62 REL/SUB) ; les 2 échecs restants sont l'impératif (`appelle-moi`) et la cible
  interne (`Peut-être`). Le **+8 GP** du même lot n'est pas attribué à cette fiche.
- **Le repli anglais n'est pas mesuré** : 54 échecs sont un problème de **couverture de langue**
  (marqueurs), pas de découpage français. La fiche ne dit pas combien de ces 54 un chunker anglais
  récupérerait.
- **Le script de mesure est éphémère** (`/tmp`) : la mission n'autorisait que deux fichiers neufs.
  La recette du § 3.1 et le JSON joint permettent de le refaire ; une porte permanente reste à
  écrire.
- **Les 13 GP** sont hors périmètre : le contrat les mentionne (`cible.genre`, `direction`), mais
  leur mesure fine (5 absents, 6 larges, 2 étroits) n'est pas qualifiée ici.
- **Portes non rejouées** : le correctif du bloc n'est pas committé ; l'évaluateur gold courant
  rend `ok: true` (exact 137, 0,9448). Le parent doit committer le correctif et rejouer
  `tools/toutes-les-portes.sh` ; cette fiche ne remplace pas la porte.

## 6. La suite

1. **S — le contrat** : étendre `Segment.dict()` et `structure()` avec `sous_type`, `marqueur`,
   `cible`, `cibles`, `confiance`, `statut`, `langue`, `CONTRAT = "s/v1"` ; `structure()` devient
   l'entrée unique, `analyser()` reste l'affichage des candidats.
2. **S — les spans** : la règle « **un prédicat par clause** » pour REL/SUB : après le premier
   verbe plein (auxiliaires et participes compris), le **second verbe conjugué** ouvre la
   principale ; ne pas couper sur un auxiliaire ni sur un adverbe de temps de la subordonnée.
   Attendu : les **18 larges** et les **3 étroites**.
3. **S — la langue** : `langue` en paramètre, `statut="refus"` pour `en` (ou jeux de marqueurs
   anglais), au lieu d'un GV qui avale la phrase.
4. **L — la cible (fait dans l'arbre courant, non committé)** : SUB → `_cible_proche` (verbe),
   REL → `_tete_nom` (antécédent), GP → `_cible_proche` ; lire les `cible` typées, ne plus
   écraser les trois canaux ; une seule segmentation. Observé : **60/62** REL/SUB (**+6**),
   **137/145** (0,9448) ; reste à committer et à tester.
5. **Gold — la convention** : corriger `CONVENTION_CIBLE["SUB"]` en « verbe gouverneur » ; trancher
   le cas interne (`Peut-être qu'il viendra`).
6. **La porte** : un test de contrat (invariants du § 2.1) et la mesure des 143 cibles REL/SUB ;
   cible : **≥ 100/143** spans exacts ; l'attachement **60/62** est atteint dans l'état courant,
   à figer par un test. Mesurer le repli anglais séparément, pour ne pas mélanger couverture de
   langue et segmentation.

## 7. Fichiers

- [`generateur.py`](../tools/structures/generateur.py) — lu, **non modifié** : `Segment` (`:293`),
  `_segmente` (`:346`), `construire_arbre` (`:319`), cibles (`:485-497`), `analyser` (`:516`),
  `structure` (`:621`).
- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — lu ; le correctif REL/SUB non
  committé (13:51) est celui du chantier en cours, pas de cette fiche : `_syntagmes_s`,
  `_cibles_s`, `_tete_nom`, `_cible_proche`, branche REL/SUB, union.
- [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) — rejoué ; le correctif POS
  non committé est du chantier (mesure 116 verbes / 29 noms), pas de cette fiche.
- [`autotest.py`](../tools/pensee/autotest.py) — contient le T175 non committé du chantier, pas
  de cette fiche.
- [`pensee-contrat-s.json`](pensee-contrat-s.json) — les chiffres et le contrat lisible par machine.
