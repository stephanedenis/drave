# B13 — les trois retouches A3 sur le live : +1, +2, +1, et 145/145 exact/top1

> **Ligne de roadmap** : **B13** (moteur de pensée, attachement) · **Date** : 2026-11-05 · **Verdict** : ✅ **R1 (repli cible vide, GP)** et **R3 (complétive en tête, SUB)** à intégrer ; ⚠️ **R2** : ❌ sous sa forme littérale (« préférer un verbe »), ✅ sous sa forme **étroite** (« tête la plus proche »), qui répare les mêmes cas. Sur l'empreinte live `9da6dee7`, les trois valent **+4 net, 0 régression** et amènent à **145/145 exact (1,0000)** et **145/145 top1** ; sur les **239 cibles** : **145/239 (0,6067)**, plafond des 94 spans non prédits. Sur le baseline A3 `bb020516` (137/145), les mêmes retouches valaient **+2/+4/+1 = +7** (144/145, top1 145/145) : le live a déjà absorbé `g002`, `g012`/`r018` et `r230`.
>
> **Dispositif** : [`replis_cible.py`](../tools/tests/linguistique/replis_cible.py), JSON [`pensee-replis-cible.json`](pensee-replis-cible.json). [`bloc_linguistique.py`](../tools/bloc_linguistique.py) **non modifié** ; son empreinte est figée dans le JSON (`9da6dee7`, 105 156 octets, 15:22:00). Le bloc a bougé pendant la session (`6e843018` → `bb020516` → `64b7c520` → `9da6dee7`) : les chiffres sont une photo de la dernière empreinte, stable pendant le run.

## 1. Protocole

- **Population** : 612 phrases (20 `hand` + 432 `reel` + 160 synthétiques), **239 cibles** gold, **145** dont le span `(type, debut, fin)` est prédit par l'heuristique. Les 94 autres n'ont pas de label au span exact.
- **Mesure** : `evaluer_gold.evaluer_bloc` ; **exact** = égalité avec `cibles[0]`, **top1** = cible non vide et sous-chaîne d'une des cibles. On rapporte 145 (span) et 239 (global), les régressions (exact avant → faux après) et le gain net = gains - régressions.
- **Simulation** : sous-classe de `Heuristique` + post-traitement de `meta.attachement.cible`. Le vivier est celui de `classement_cible.py` (tokens pleins, POS ouverte ou `_est_verbe`, auxiliaires exclus ; gauche → droite → dedans, puis distance). Aucun span, aucun `candidats`, aucun lexique modifié ; le top-k reste donc **142/239 strict** pour toutes les variantes.
- **Fidélité** : le témoin no-op redonne exactement **141/145 exact, 143/145 top1** ; les agrégats par segment sont vérifiés contre `evaluer_bloc` pour chaque variante.
- **Dérive** : le code live a été modifié par un autre agent pendant la session (ajout de `_repli_cible_gp`, `_cible_hors_span`, `_sans_enclitique`, cache GV). Le JSON sépare le run final (`9da6dee7`) du snapshot A3 (`bb020516`, 137/145) ; les deux sont mesurés par le même prototype.

## 2. État des lieux de la cible (question 1)

### 2.1 Combien de cibles utilisables ?

| population | total | cible utilisable | vide | absente (pas de span) |
|---|---:|---:|---:|---:|
| 239 cibles gold | 239 | **144** (0,6025) | **1** (`s041`) | **94** (0,3933) |
| 145 au bon span | 145 | **144** (0,9931) | **1** (`s041`) | 0 |
| 94 hors span | 94 | 0 | 0 | **94** (1,0000) |

| type | cibles 239 | spans prédits 145 | vides (145) | absents (94) |
|---|---:|---:|---:|---:|
| GP | 96 | 83 | **1** (`s041`) | 13 |
| REL | 74 | 26 | 0 | 48 |
| SUB | 69 | 36 | 0 | 33 |
| **total** | **239** | **145** | **1** | **94** |

- **Sur les 145** : une seule cible vide, `s041` (GP « devant elles »). Sur le snapshot A3 137, il y en avait **deux** (`g002`, `s041`) ; `g002` est réparé par `_repli_cible_gp` (génitif → tête du GN à gauche).
- **Sur les 239** : 94 spans absents (48 REL, 33 SUB, 13 GP) + 1 vide = **95 cibles sans attachement utilisable**. Les 94 ids sont en annexe.
- **Nom prédit / verbe gold** : 2 cas, `s108` (`papier` au lieu de `rêve`) et `s122` (`papier` au lieu de `saute`). `papier` est POS `VERB` par la désinence `-er` mais `_est_verbe("papier")` est faux : c'est le piège que R2 exploite. Sur le snapshot A3, il y avait un troisième cas, `r230` (`appelle-moi` vs `appelle`), réparé par `_sans_enclitique` (hors des trois retouches).
- **Verbe prédit / gold non-verbe** : 0 sur le live ; 2 sur le snapshot A3 (`g012`, `r018`), réparés par `_cible_hors_span`.
- **Top1 sans exact** : `s108`, `s122` (le gold accepte `papier` comme cible alternative) ; c'est pourquoi R2 gagne +2 exact mais +0 top1.

### 2.2 Croisement des natures (145)

| cible prédite \ gold | verbe | nom/ADJ | total |
|---|---:|---:|---:|
| verbe | 112 | 0 | 112 |
| nom | 2 (`s108`, `s122`) | 29 | 31 |
| autre (ADV) | 1 (`r309`) | 0 | 1 |
| vide | 1 (`s041`) | 0 | 1 |
| **total** | **116** | **29** | **145** |

Sur le snapshot A3 137, le même tableau donnait 111 verbe→verbe, 26 nom→nom, **3 nom→verbe** (`r230`, `s108`, `s122`), **2 verbe→nom** (`g012`, `r018`), 1 autre→verbe (`r309`), 1 vide→nom (`g002`) et 1 vide→verbe (`s041`). Le live a réparé `r230`, `g012` et `r018`.

## 3. R1 — repli cible vide

**Règle** : si un segment non-`GV` n'a pas de cible et que le vivier n'est pas vide, prendre le **rang 0** (token plein le plus proche, gauche → droite → dedans, puis distance). Forme retenue : **GP seulement**.

**Résultat live** : exact **142/145 (+1, `s041` → `marche`)**, top1 **144/145 (+1)**, **0 régression**, **net +1** ; 239 : 142/239 exact (0,5941), 144/239 top1 (0,6025). Surface : **2 étiquettes changées** (1 gold `s041`, 1 hors gold `s027` « avec il » → `marche`).

**Snapshot A3 137** : +2 (`g002` → `chat`, `s041` → `marche`), 0 régression, net +2 ; 3 changements (2 gold / 1 hors). Le live a déjà `g002` ; le marginal est `s041`.

**Contrôles** :

- dernier candidat : 0 exact, +1 top1 (`s041` → `avocat`, cible alternative du gold), 2 changements → remplir ne suffit pas, le choix compte ;
- premier verbe du lexique : 0 gain, 0 changement (`marche` et `chat` ne sont pas reconnus) ;
- tous non-GV : +1 exact mais **113 changements** (112 hors gold, surtout des GN) → le scope GP est ce qui rend R1 minimal.

**Lecture** : le repli est **non régressif par construction sur les 145** (remplacer vide par non-vide ne peut pas baisser l'exact — vide était faux — ni le top1 — vide était faux). Le risque est hors gold (`s027`), pas sur la mesure.

## 4. R2 — préférence de tête (et non « préférence verbe »)

**Le constat** : A3 annonce « préférer un verbe à un nom proche » pour `g012`, `r018`, `s108`, `s122`. Sur le live, `g012`/`r018` sont déjà réparés (`_cible_hors_span` : `manger` dans le GP → tête du GV extérieur `prêt`/`prête`) ; les deux cas restants sont `s108`/`s122` (nom `papier` plus loin que le verbe `rêve`/`saute`). La préférence **littérale** est donc mesurée à part, et elle est néfaste.

**R2 littérale** (cible non verbale → verbe reconnu à distance ≤) :

- live : 0 gain, **3 régressions** (`g002` → `dort`, `g012` → `manger`, `r018` → `manger`), **net -3**, 6 changements (3 gold / 3 hors) ;
- + `rêve`/`saute` au lexique : +2 (`s108`/`s122`) mais 3 régressions → **net -1** ; 8 changements (5/3) ;
- POS au lieu du lexique : 0 gain, **9 régressions**, net -9 ;
- snapshot A3 : 0 gain, 0 régression (rien de correct à défaire) ; +2 avec le lexique étendu.

→ **ne pas intégrer**.

**R2 large** (GP → rang 0, sauf verbe gouverneur reconnu hors segment) : live +2 exact (`s108`/`s122`), 0 régression, top1 +0, **12 changements (2 gold / 10 hors)**, dont `r083` `gare` → `train`, `r324` `est` → `livre`, `r408` `pas` → `viens-tu`. C'est la forme qui valait **+4** sur le snapshot A3 (les 4 cas), mais le live a déjà `g012`/`r018` et la surface hors gold est excessive.

**R2 étroite** (retenue) : pour un GP, si la cible n'est pas un verbe reconnu **et** qu'un candidat **hors segment** est **strictement plus proche**, prendre ce candidat. Live : **+2 exact** (`s108` → `rêve`, `s122` → `saute`), 0 régression, top1 +0, **4 changements (2 gold / 2 hors : `r121`, `r227`)**, net +2. Même gain que R2 large avec 3× moins de changements. Ce n'est pas littéralement « préférer un verbe » : c'est préférer la **tête la plus proche**, qui se trouve être le verbe dans les deux cas.

→ **intégrer la forme étroite, pas la littérale ni la large**.

## 5. R3 — complétive en tête

**Règle étroite** : pour un `SUB`, si la cible actuelle est le **texte du segment immédiatement à gauche** (un GV mal étiqueté), qu'elle n'est pas un token candidat, qu'aucun candidat n'est à gauche et qu'il y a un candidat dedans, prendre le **dernier candidat intérieur** (le verbe de la complétive).

Live : **+1 exact** (`r309` `Peut-être` → `viendra`), +1 top1, **0 régression**, 1 changement, net +1 ; 239 : 142/239 exact (0,5941), 144/239 top1 (0,6025). Snapshot A3 : +1 également.

**Contrôle large** (tout SUB → intérieur) : +1 gain, **-32 net**, 33 régressions, 36 changements. La condition « cible = texte du segment précédent » est toute la valeur : sans elle, `r230` (cible `appelle`, désormais correcte) serait changé en `arrives` (mesuré : +1/-1, net 0). La version étroite distingue la complétive en tête du cas enclitique.

→ **intégrer la forme étroite, pas la large**.

## 6. Combinaison

| mesure | base | R1 | R2 étroite | R3 | combiné |
|---|---:|---:|---:|---:|---:|
| exact 145 | 141 | 142 | 143 | 142 | **145** |
| top1 145 | 143 | 144 | 143 | 144 | **145** |
| exact 239 | 141 | 142 | 143 | 142 | **145** |
| top1 239 | 143 | 144 | 143 | 144 | **145** |
| régressions | — | 0 | 0 | 0 | **0** |
| net exact | — | +1 | +2 | +1 | **+4** |
| changements | 0 | 2 | 4 | 1 | **7** (4 gold / 3 hors) |

Gains combinés : `s041`, `s108`, `s122`, `r309` ; 0 régression. Surface hors gold : `s027` (`""` → `marche`), `r121` (`jardinier` → `plante`), `r227` (`lit` → `dort`). McNemar 4/0 = **0,125** (descriptif, règles dessinées sur les cas ; non significatif à 5 %).

Comparaisons : combiné avec R2 large = 145/145 mais **15 changements** (4/11) ; avec R2 littérale = 140/145, **-1 net**, 3 régressions. Le top-k reste **142/239 strict** ; le plafond global **145/239** est celui des 94 spans non prédits.

Sur le snapshot A3 137 : combiné +7 → **144/145 exact (0,9931)**, **145/145 top1 (1,0000)**, 0 régression. Le live a absorbé `g002`, `g012`/`r018` et `r230` ; les trois retouches ferment les 4 dernières erreurs.

## 7. Contrôles négatifs

| contrôle | exact 145 | net | régressions | changements | lecture |
|---|---:|---:|---:|---:|---|
| no-op | 141 | 0 | 0 | 0 | fidélité du harnais |
| R1 dernier candidat | 141 | 0 | 0 | 2 | top1 +1 par la cible alternative `avocat` ; le choix du rang 0 compte |
| R1 premier verbe | 141 | 0 | 0 | 0 | `marche`/`chat` hors lexique : le repli « verbe » ne mord pas |
| R2 littérale | 138 | -3 | 3 | 6 | défait `g002`/`g012`/`r018` |
| R2 littérale + lexique | 140 | -1 | 3 | 8 | +2 `s108`/`s122` mais 3 régressions |
| R2 POS | 132 | -9 | 9 | 14 | le POS n'est pas un détecteur de verbe sûr |
| R2 large | 143 | +2 | 0 | 12 | même gain que l'étroite, 10 changements hors gold |
| R3 large | 109 | -32 | 33 | 36 | toute complétive → intérieur : catastrophe |
| rang 0 partout (A3 §7.1) | 139 | -2 | 6 | 470 | `g003`, `g014`, `g016`, `r048`, `r068`, `r230` ; 460 changements hors gold |
| combiné R2 large | 145 | +4 | 0 | 15 | 11 hors gold |
| combiné R2 littérale | 140 | -1 | 3 | 9 | interaction : `g002` perdu |

Lecture : les gains viennent du **scope** et des **gardes**, pas d'une règle générique « verbe » ou « rang 0 ».

## 8. Ce qui pourrait rendre cette fiche fausse

- **145 segments, 4 gains marginaux** : les règles ont été dessinées sur les cas réparés (HARKing) ; aucun gold tenu à l'écart. Le +4 est une **borne haute**, pas une estimation.
- **Simulation post-traitement** : ce n'est pas un diff ; une intégration réelle peut interagir avec le S, l'union et `_cible_proche`. Les portes n'ont pas été rejouées (consigne : ne rien modifier/committer).
- **Le bloc bouge** : `6e843018` → `bb020516` → `64b7c520` → `9da6dee7` pendant la session ; si le worktree change encore, relancer le prototype. Le JSON fige l'empreinte et `bloc_stable_pendant_le_run=true`.
- **94 spans non prédits** : le plafond global est **145/239** ; aucune retouche de cible ne le franchit. C'est un problème de segmentation/S, pas d'attachement.
- **Top1** : sous-chaîne et cibles alternatives (`s108`/`s122` déjà top1 vrais ; `s041` → `avocat` gagne du top1 sans exact). L'exact est la mesure de choix.
- **Surface hors gold** : R2 étroite change `r121` (`jardinier` → `plante`) et `r227` (`lit` → `dort`) ; R2 large en change 10, dont `r083` `gare` → `train` qui semble faux. R1 change `s027`. Aucun gold ne couvre ces spans.
- **Lexique** : `rêve`, `saute`, `marche` ne sont pas dans `VERBES_CONNUS` ; la variante littérale n'achète ses +2 qu'en ajoutant les deux cibles du gold. Compléter le lexique est un changement séparé.
- **Convention du gold** : verbe gouverneur ou nom antécédent ; la nature est lue sur le POS du gold, avec `_est_verbe` en repli.
- **Attribution de l'absorption live** : `_repli_cible_gp`, `_cible_hors_span`, `_sans_enclitique` sont identifiés par le diff, pas par une ablation ; le partage exact entre live et retouches est une lecture.

## 9. Recommandation

1. **R1 (repli cible vide, GP seulement)** : ✅ **intégrer**. +1 marginal (+2 sur le baseline A3), 0 régression, 2 changements. C'est le seul moyen de remplir `s041` ; le repli ne peut pas dégrader un exact déjà faux.
2. **R2 étroite (tête la plus proche, GP seulement)** : ✅ **intégrer** si les 2 changements hors gold (`r121`, `r227`) sont acceptables. +2 exact, 0 régression, 4 changements. **Ne pas intégrer** la préférence verbe littérale (nette négative) ni la forme large (même gain, 12 changements).
3. **R3 étroite (complétive en tête)** : ✅ **intégrer**. +1, 0 régression, 1 changement. **Ne pas élargir** (33 régressions).
4. **Les trois ensemble** : **145/145 exact (1,0000)** et **145/145 top1** sur les 145 ; **145/239 (0,6067)** sur les 239. Le +4 marginal (contre +7 sur le baseline A3) est le signe que le live a déjà absorbé une partie ; le reste est un problème de span.
5. **Avant intégration** : gold tenu à l'écart, revue de `r121`/`r227`/`s027`, portes, puis commit unique. La fiche ne modifie ni `bloc_linguistique.py` ni les portes.

## 10. Fichiers

- [`replis_cible.py`](../tools/tests/linguistique/replis_cible.py) — prototype autonome, non importé ailleurs ; n'écrit que le JSON.
- [`pensee-replis-cible.json`](pensee-replis-cible.json) — résultats, 145 audits, snapshot A3 137, dérive des empreintes.
- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — non modifié ; empreinte `9da6dee7` dans le JSON.
- [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) — `charger()` et `evaluer_bloc`, réutilisés tels quels.

## Annexe — les 94 cibles sans span prédit

- **GP (13)** : `g006`, `g020`, `r028`, `r038`, `r060`, `r083`, `r102`, `r153`, `r162`, `s027`, `s146`, `s148`, `s160`.
- **REL (48)** : `r034`, `r035`, `r074`, `r075`, `r114`, `r115`, `r204`, `r206`, `r214`, `r217`, `r220`, `r224`, `r236`, `r239`, `r241`, `r243`, `r246`, `r248`, `r250`, `r255`, `r273`, `r278`, `r280`, `r283`, `r285`, `r287`, `r289`, `r291`, `r293`, `r297`, `r299`, `r300`, `s010`, `s032`, `s035`, `s037`, `s050`, `s061`, `s065`, `s069`, `s070`, `s072`, `s075`, `s115`, `s125`, `s131`, `s135`, `s141`.
- **SUB (33)** : `g017`, `r205`, `r215`, `r216`, `r218`, `r219`, `r237`, `r238`, `r240`, `r242`, `r244`, `r245`, `r247`, `r249`, `r264`, `r279`, `r281`, `r282`, `r284`, `r286`, `r288`, `r290`, `r292`, `r294`, `r296`, `r298`, `r303`, `r313`, `s015`, `s044`, `s112`, `s114`, `s132`.
