# B13 — le top-k de l'attachement : 0,7406 → 0,8870, et le plafond de couverture

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 ·
> **État** : `f908d7b0` (`s/v7`) · **Verdict** : ✅ les **62 échecs** du top-k sont qualifiés
> (0 « autre ») ; **32 des 35 échecs de couverture** viennent d'un **site d'appel** —
> `prec = s` est exécuté avant `_candidats_precedent`, qui reçoit donc le segment lui-même et
> ne voit jamais le GN antécédent. La complétion **R1** (antécédent REL + GP génitif) répare
> **34/35** échecs avec **34 ajouts et 34 hits (100 %)** ; **R2** (verbe propre d'une SUB sans
> candidat verbal) rend le dernier. Le top-k passe à **212/239 = 0,8870**, soit **100 % des
> 212 spans prédits**. Le reste est le **plafond de couverture** : **27 spans non prédits**,
> dont **19 synthétiques**. Le choix, lui, était déjà bon : **exact 212/212** avant et après.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`Heuristique`,
> `_candidats_precedent`, `_verbes_proches`, `_repli_cible_gp`) ·
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) (`charger`, `evaluer_bloc`) ·
> [`gold_split.py`](../tools/tests/linguistique/gold_split.py) (`dev`, `test`) · JSON
> [`pensee-topk-v8.json`](pensee-topk-v8.json) (62 échecs, règles, contrôles).
> **Simulation par sous-classe locale** (`HeuristiqueV8`), **hors dépôt** : aucun fichier
> existant modifié, aucun commit. Les règles sont **additives** (elles n'enlèvent jamais un
> candidat et ne touchent pas `meta["attachement"]["cible"]`).

## 1. La mesure

Gold **612 phrases**, **239 cibles**, **212 labels** au bon span. Le top-k compte la cible
gold **présente dans `candidats`** (`evaluer_bloc`, l. 155) ; une cible sans label compte
comme un échec. La lecture **strict** (`nom == cible`, l. 159) et la lecture **sous-chaîne**
donnent ici **le même chiffre** : pas d'artefact de sous-chaîne.

| mesure | all | dev | test |
|---|---:|---:|---:|
| cibles | 239 | 163 | 76 |
| labels au bon span | 212 | 148 | 64 |
| **exact / labels** | **212/212 = 1,0** | 148/148 = 1,0 | 64/64 = 1,0 |
| **top-k / cibles** | **177/239 = 0,7406** | 120/163 = 0,7362 | 57/76 = 0,7500 |
| top-k / labels | 177/212 = 0,8349 | 120/148 = 0,8108 | 57/64 = 0,8906 |
| top-k strict | 177 | 120 | 57 |

**Ce que ça dit.** L'attachement **choisit** la bonne cible **212 fois sur 212** ; il échoue
à la **déclarer candidat** 35 fois, et 27 cibles n'ont même pas de label. Le top-k est donc
borné par la couverture de span : **212/239 = 0,8870** est le plafond atteignable par
n'importe quelle règle de candidats. Sur les cibles réellement étiquetées, le plafond est
**212/212 = 1,0**.

## 2. Les cinq motifs

1. **L'antécédent des REL n'est jamais ajouté : 32 des 35 échecs de couverture.** Les listes
   ressemblent à `["REL", "dormait"]` ; le nom `chat` manque, alors que le GN `Le chat` est
   prédit. La cause est un **site d'appel** : `_candidats_precedent` (l. 680) sait rendre
   l'antécédent d'une REL (`precedent.type == "GN"`), mais dans les deux branches qui
   l'appellent, `prec = s` (l. 1148 et 1175) est exécuté **avant**
   `_candidats_precedent(texte, s, prec)` (l. 1154 et 1181). Le helper reçoit le segment
   lui-même : la branche `REL → GN` est morte. La branche S (l. 1122) ne l'appelle pas du tout.
2. **Le choix est déjà correct 212 fois sur 212.** Tous les échecs de couverture ont
   `cible == cibles[0]` (exact 1,0) mais la cible n'est pas dans la liste. Ce n'est pas un
   problème de décision d'attachement, c'est un problème de **cohérence de la liste**.
3. **R1 répare 34/35 sans consulter la cible.** En lisant les seuls **GN prédits**, R1 ajoute
   la tête du GN à gauche pour chaque REL (et pour chaque GP génitif) : **34 ajouts, 34 hits,
   100 % de précision**, **+28 sur dev** (les 28 échecs de couverture de dev), **+6 sur test**.
   La règle n'apprend aucun paramètre : elle répare le helper existant.
4. **GP et SUB sont des résidus.** 2 GP hand (`g002`, `g006`) : `_repli_cible_gp` (l. 693)
   connaît déjà la convention génitive pour la **cible**, pas pour les **candidats**. 1 SUB
   (`r309`, « Peut-être qu'il viendra ») : le verbe propre `viendra` n'est candidat nulle part
   et le POS le tague `NOUN` ; `_verbe_dans` le retrouve par son repli dernier mot. Le **verbe
   de la principale**, lui, est déjà couvert par `_verbes_proches` (0 ajout, 0 gain).
5. **Le plafond est la couverture de span, pas les candidats.** 27 échecs (43,5 %) sont des
   spans non prédits : REL 16, SUB 6, GP 5 ; 19 synthétiques, 7 réels, 1 hand. Après R1+R2,
   **212/212 labels** ont la cible dans les candidats, mais **212/239 seulement** des cibles
   ont un label. Sur réel (`hand`+`reel`) : **145/184 = 0,7880 → 176/184 = 0,9565**. Sur
   synthétique : **32/55 = 0,5818 → 36/55 = 0,6545**. La suite est un chantier de **chunker**,
   pas de candidats.

## 3. Qualification des 62 échecs

### 3.1 Par type, langue, source

| type | cibles | labels | échecs | dont span | dont couverture | top-k | taux |
|---|---:|---:|---:|---:|---:|---:|---:|
| REL | 74 | 58 | **48** | 16 | **32** | 26 | 0,3514 |
| SUB | 69 | 63 | 7 | 6 | 1 | 62 | 0,8986 |
| GP | 96 | 91 | 7 | 5 | 2 | 89 | 0,9271 |
| **total** | **239** | **212** | **62** | **27** | **35** | **177** | **0,7406** |

Le gold ne cible **aucun GN ni GV** : les 239 cibles sont **REL 74, SUB 69, GP 96**. Les
colonnes GN/GV sont donc vides par construction, pas par oubli.

| langue | cibles | labels | échecs | span | couverture | top-k | taux |
|---|---:|---:|---:|---:|---:|---:|---:|
| fr | 151 | 129 | 31 | 22 | 9 | 120 | 0,7947 |
| en | 88 | 83 | 31 | 5 | **26** | 57 | 0,6477 |

| source | cibles | labels | échecs | span | couverture | top-k | taux |
|---|---:|---:|---:|---:|---:|---:|---:|
| hand | 13 | 12 | 3 | 1 | 2 | 10 | 0,7692 |
| reel | 171 | 164 | 36 | 7 | 29 | 135 | 0,7895 |
| synthetique | 55 | 36 | 23 | **19** | 4 | 32 | 0,5818 |

### 3.2 Les deux familles d'échecs

**27 spans non prédits** (aucun label au bon span) : **REL 16, SUB 6, GP 5** ; **fr 22, en 5** ;
**synthétique 19, reel 7, hand 1**. Répartition fine : REL 12 synth + 2 fr reel + 2 en reel ;
SUB 3 synth + 1 fr reel + 1 en reel + 1 en hand ; GP 4 synth + 1 en reel. **19/27 sont
synthétiques** (ex. `s027` GP « il », `s146` GP « les jardin ») : le gold y découpe des
constituants que le chunker ne produit pas. Les **8 réels/hand** sont les seuls que le chunker
pourrait viser : `g017` SUB, `r035` REL, `r153` GP, `r255` REL, `r264` SUB, `r273` REL,
`r280` REL, `r288` SUB.

**35 échecs de couverture** (label présent, cible absente des candidats) : **REL 32, GP 2,
SUB 1** ; **en 26, fr 9** ; **reel 29, hand 2, synthétique 4**. Les 32 REL : **26 anglaises**
(toutes `reel`) + **6 françaises** (`r206`, `r224`, `s050`, `s070`, `s075`, `s131`). Les 6
françaises sont des REL **courtes** produites par le chunker simple, qui ne passent pas par
les `noms` du générateur S ; les 26 anglaises n'ont aucun `noms` S (le générateur S est
français, l. 1071) et ne reçoivent que les verbes de `_verbes_proches`.

| cause | effet | type | langue | source | réparé par |
|---|---:|---|---|---|---|
| antécédent REL absent | 32 | REL 32 | en 26, fr 6 | reel 28, synth 4 | R1 |
| antécédent GP génitif absent | 2 | GP 2 | fr 2 | hand 2 | R1 |
| verbe propre de SUB absent | 1 | SUB 1 | fr 1 | reel 1 | R2 |
| span non prédit | 27 | REL 16, SUB 6, GP 5 | fr 22, en 5 | synth 19, reel 7, hand 1 | — (chunker) |
| **total** | **62** | | | | |

### 3.3 Le site d'appel, en clair

`_candidats_precedent` (l. 680) est écrit pour rendre :

- `REL` + `precedent.type == "GN"` → la tête du GN (`chat`) ;
- `SUB` + `precedent.type == "GV"` → le verbe du GV (`dit`).

Mais les branches non-S et union font `prec = s` **avant** l'appel, donc `precedent` est le
segment courant, jamais le précédent. La branche S, elle, ne l'appelle pas. Conséquence :
`exact` (qui lit `meta["attachement"]["cible"]`, calculé **avant** `prec = s`) reste à 1,0 ;
seuls les `candidats` perdent l'antécédent. C'est exactement la signature mesurée : **exact
212/212, top-k 177/239**. La correction de R1 consiste à lire les **GN prédits de toute
l'annotation** (le GN à gauche), ce qui répare le cas court français et le cas anglais sans
dépendre de l'ordre des branches.

## 4. Trois règles de complétion, mesurées

Toutes les règles sont **additives** : ajout en fin de liste, dédupliqué, sans toucher à la
cible choisie. « Pertes » vaut donc **0 par construction** ; le coût se lit en **candidats
ajoutés**, pas en pertes.

- **R1 — antécédent à gauche.** Pour toute `REL` : tête du `GN` prédit le plus proche dont
  `fin <= début`. Pour un `GP` : même tête **si** la préposition initiale est génitive
  (`de, du, des, d', of, from`) — la convention de `_repli_cible_gp`. Pas de tête interne de
  GP. **34 ajouts, 34 hits (100 %).**
- **R2 — repli verbal de la SUB.** Si **aucun candidat n'est un verbe** (`_est_verbe`),
  ajouter le verbe propre du span (`_verbe_dans`, repli dernier mot). **19 ajouts, 1 hit
  (5,3 %)** : r309. Neutre sur dev, +1 sur test.
- **R3 — voisinage verbal ≤ 3 tokens.** Ajouter les tokens `POS=VERB` à distance ≤ 3 tokens.
  **2 ajouts, 0 hit** : dominée. Le POS tague `viendra` `NOUN`, la règle ne le voit pas ;
  c'est `_verbe_dans` (repli dernier mot) qui sauve R2, pas le voisinage.

| règle | dev | gain dev | test | gain test | all | ajouts | hits | candidats (moy./max) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| base | 120/163 | — | 57/76 | — | 177/239 | — | — | 2,434 / 5 |
| **R1** | **148/163** | **+28** | **63/76** | **+6** | **211/239** | 34 | 34 | 2,594 / 5 |
| R2 | 120/163 | 0 | 58/76 | +1 | 178/239 | 19 | 1 | 2,524 / 5 |
| R3 | 120/163 | 0 | 57/76 | 0 | 177/239 | 2 | 0 | 2,443 / 5 |
| **R1+R2** | **148/163** | **+28** | **64/76** | **+7** | **212/239** | 53 | 35 | 2,684 / 5 |

**Lecture.**

- **R1 est la règle à retenir** : +34 cibles, 100 % de précision, **+0,16 candidat par label**,
  maximum inchangé (5). Elle répare **28/28** échecs de couverture de dev et **6/7** de test.
- **R2 est optionnelle** : son seul gain est `r309` (test), et elle ajoute 18 candidats de
  bruit pour ce 1 hit. Elle a le mérite de nommer le résidu (verbe propre de SUB, POS en
  défaut) ; si l'on refuse l'invariant de cohérence ci-dessous, c'est elle qui amène au
  plafond.
- **R3 est dominée** : 2 ajouts, 0 gain. Le « verbe de la principale » suggéré par l'énoncé
  est, lui, **déjà couvert** par `_verbes_proches` (`k = 3`) : **0 ajout, 0 gain**.
- Élargir R1 aux GP non génitifs et à leur tête interne fait passer les ajouts de **34 à 149**
  pour **le même top-k** (211) : la version étroite est la bonne.

**La borne de cohérence.** Puisque `exact` est 212/212, ajouter la **cible choisie** aux
candidats quand elle manque suffit à faire **212/239 en 35 ajouts**, sans aucune règle
linguistique. C'est **tautologique** : la règle utilise la réponse. Ce n'est donc pas un
résultat, mais un **garde-fou** : `cible ∈ candidats` devrait être un invariant. Après R1,
il ne reste **qu'un** ajout à faire (r309) : **R1 + invariant = 35 ajouts, 35 hits, 212/239**,
contre **53** pour R1+R2. L'invariant seul est la preuve que le top-k est ici une mesure de
**cohérence de liste**, pas de qualité de décision.

## 5. Contrôles négatifs

Mesures sur les listes de **R1+R2** (212 labels). Les 1 000/2 000 tirages sont déterministes
(graine 0). « Permutation des ajouts » garde la liste de base et ne permute **que** les 53
ajouts entre labels ; « hasard des ajouts » remplace ces ajouts par des cibles tirées au
hasard, même nombre.

| contrôle | dev | test | all |
|---|---:|---:|---:|
| R1+R2 (référence) | **148/148** | **64/64** | **212/212** |
| ordre intra-liste (brassé) | 148 | 64 | 212 |
| permutation croisée des listes | 1,22 | 0,60 | 1,82 |
| hasard global (même nombre de candidats) | 3,66 | 1,83 | 5,49 |
| hasard typé (même langue + même type) | 16,84 | 7,52 | 24,36 |
| **permutation des ajouts (base gardée)** | **120,08** | **57,03** | **177,11** |
| **hasard des ajouts (base gardée)** | **120,24** | **57,06** | **177,30** |

**Lecture.** Brasser chaque liste **ne change rien** (212) : le top-k est **insensible à
l'ordre**, il ne mesure pas le classement. Une liste prise à un autre label tombe à **1,82** ;
le hasard global à **5,49** ; le hasard qui connaît la langue et le type à **24,36**. Surtout,
permuter ou tirer les **seuls ajouts** ramène à **177,1–177,3**, c'est-à-dire à la base : les
**+35** viennent des ajouts **précis** (les antécédents), pas du simple allongement des listes.
Le contrôle est donc **négatif au bon endroit**.

## 6. Ce qui pourrait rendre ce résultat faux

- **Le split n'est pas aveugle.** R1 a été dessinée après avoir regardé les 62 échecs, test
  compris. Elle reste la réparation d'un helper existant, et le test confirme **+6/76**
  (test du signe exact, 6 gains / 0 perte : p ≈ 0,031 ; R1+R2, 7/0 : p ≈ 0,016). Mais 0 perte
  est **structurel** (complétion additive) : le signe teste le sens des gains, pas la
  généralité de la règle.
- **R2 n'est pas validée sur dev** : +0 sur dev, +1 sur test. C'est une hypothèse sur un cas
  (r309), pas un résultat. Son coût (19 ajouts pour 1 hit) doit être mis en face.
- **Le top-k est insensible à l'ordre.** 100 % sur les spans ne signifie pas que la bonne
  cible est **en tête** ; cela signifie qu'elle est **présente**. Le classement des candidats
  n'est pas mesuré ici.
- **L'invariant rendrait le top-k circulaire** (212/239 en 35 ajouts). C'est pourquoi la
  mesure utile est R1 (34 hits **sans** regarder la cible), pas l'invariant.
- **R1 dépend des GN prédits.** Les 32 REL réparées avaient toutes un GN prédit à gauche ; si
  l'antécédent n'est pas un GN labellisé (ou est un pronom), la règle ne l'ajoute pas. Sur un
  nouveau corpus, la rappel de R1 suivra la couverture des GN, pas celle des REL.
- **Petit échantillon** : 612 phrases, 239 cibles, 76 cibles de test ; les 6–7 gains de test
  sont peu de chose. Le gold synthétique pèse 19 des 27 spans manqués : le plafond 0,887 est
  en partie un artefact du gold synthétique. Sur réel (`hand`+`reel`), le plafond est
  **176/184 = 0,9565**.

## 7. Recommandation

1. **Corriger le site d'appel** : passer le **segment précédent** à `_candidats_precedent`
   (déplacer `prec = s` après la construction des candidats, ou garder `prec_candidats = prec`),
   et l'appeler aussi dans la branche S. Mesure de la correction **stricte** (seul le segment
   précédent) : **+32 REL, top-k 209/239**. Lire le **GN à gauche** comme R1 rend les mêmes
   **32 REL** et reste plus robuste quand le précédent est un GP ; c'est cette lecture qui est
   recommandée.
2. **Étendre la convention génitive** de `_repli_cible_gp` aux candidats : GP `de/du/des/d'/of/from`
   → tête du GN à gauche. **+2** (g002, g006).
3. **R2 en repli** si l'on veut une complétion purement linguistique du cas r309 : +1, 19
   ajouts. Sinon, **l'invariant `cible ∈ candidats`** couvre le résidu en **1 ajout** — mais
   c'est un garde-fou, pas un résultat.
4. **Ne pas célébrer 0,887 comme un attachement résolu** : exact 212/212 avant et après. Le
   top-k est une mesure de **couverture de candidats**, pas de décision ; le prochain chiffre
   à suivre est le **classement** de la cible dans la liste (top-1 candidat, MRR), pas le
   top-k.
5. **Attaquer les 27 spans** : 19 synthétiques (le gold découpe des non-constituants), 8
   réels/hand (chunker). C'est le seul chemin au-delà de 212/239.

## 8. Fichiers et reproductibilité

- [`pensee-topk-v8.json`](pensee-topk-v8.json) — les 62 échecs (id, split, source, langue,
  type, span, cibles, candidats, cible choisie, cause), les règles R1/R2/R3/R1+R2 avec
  dev/test/all, les contrôles, la borne de cohérence, le gold gelé (mêmes chiffres : 177 → 212).
- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — `_candidats_precedent` (l. 680),
  `_repli_cible_gp` (l. 693), `_tete_nom` (l. 753), `_verbe_dans` (l. 760), `_verbes_proches`
  (l. 826), branches S/union (l. 1122, 1148–1156, 1175–1183).
- [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) — `charger` (l. 24),
  top-k (l. 155), top-k strict (l. 159).
- [`gold_split.py`](../tools/tests/linguistique/gold_split.py) — split `dev`/`test` par
  `crc32(id) % 3`, stratifié par source et langue.
- La simulation est une **sous-classe locale** de `Heuristique` : `analyser` appelle
  `super().analyser`, puis ajoute les candidats en fin de liste. Aucun fichier **existant**
  du dépôt n'a été modifié ; seuls les deux fichiers neufs ci-dessus ont été écrits ; aucun
  commit n'a été fait.
