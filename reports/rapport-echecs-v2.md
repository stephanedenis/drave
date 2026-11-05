# B13 — les 8 échecs restants de l'attachement v2 : qualifiés, chiffrés, 5 règles pour 145/145

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
> Les **8 échecs** de l'exact (137/145) sont qualifiés **un par un** (causes non exclusives) :
> **2 cibles vides**, **4 cibles absentes des candidats** en lecture stricte (**3** en sous-chaîne),
> **4 présentes mais mal choisies**, **1 tokenisation**, **0 « autre »**. **5 règles déterministes
> simulées** (code inchangé) les réparent **tous** — portée mesurée **1 à 2 segments chacune**,
> **0 régression** → **exact 145/145**. C'est une **borne haute sur le même gold** : les règles sont
> étroites (R3a n'est juste que 2/4, R4 et R5 n'ont qu'un cas), et top-k strict 145/145 suppose
> d'ajouter la cible réparée aux candidats.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`Heuristique`,
> `_verbe_dans`, `_cible_proche`, `_tete_texte`, `VERBES_CONNUS`),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) (`charger`, `evaluer_bloc`) ;
> JSON [`pensee-echecs-v2.json`](pensee-echecs-v2.json). **Lecture seule** : aucun fichier existant
> modifié, aucun commit, les simulations tournent par greffe en mémoire (scripts jetables hors dépôt).

## 1. La mesure, et la convention qui manquait

Base reproduite par `evaluer_gold.py` : **239 cibles**, **145 segments au bon span**, **exact 137**
(0,9448), top1 140 (0,9655), top-k 142 (0,9793), **top-k strict 141** (0,9724) ; couverture
**145/239 = 0,6067**. Les 8 échecs = **5,52 %** des 145, **3,35 %** des 239.

Le rapport v2 ventile « **3 hors candidats, 5 mal classés** ». C'est la lecture **sous-chaîne** :
`appelle` est contenu dans `appelle-moi`, donc r230 y est « présent ». En **égalité stricte**, la
ventilation est **4 / 4** — c'est exactement le chiffre du top-k strict (141/145). Les deux lectures
sont vraies ; elles ne comptent pas la même chose :

| lecture | cible absente des candidats | présente mais mal choisie |
|---|---:|---:|
| sous-chaîne (rapport v2) | 3 | 5 |
| **égalité stricte** (top-k strict) | **4** | **4** |

## 2. Les 8 segments, un par un

`cibles[0]` = la cible mesurée par l'exact ; `[1]` (entre parenthèses) = la cible secondaire du gold,
qui n'est pas testée par l'exact.

| # | id | source | type | segment | cible gold | choisie | candidats | qualification |
|---|---|---|---|---|---|---|---|---|
| 1 | **g002** | hand | GP | `de la voisine` | `chat` | *(vide)* | `GP` | **cible vide** + absente |
| 2 | **g012** | hand | GP | `à manger` | `prêt` | `manger` | `« à manger » → Le canard`, `« à manger » → est prêt`, `manger`, `est`, `canard`, `prêt` | **mal choisie** + auto-attachement |
| 3 | **r018** | reel | GP | `à manger` | `prête` | `manger` | `« à manger » → La souris`, `« à manger » → est prête`, `manger`, `est`, `souris`, `prête` | **mal choisie** + auto-attachement |
| 4 | **r230** | reel | SUB | `Quand tu arrives` | `appelle` | `appelle-moi` | `structure la plus proche`, `appelle-moi` | **tokenisation** (absente en strict, présente en sous-chaîne) |
| 5 | **r309** | reel | SUB | `qu'il viendra` | `viendra` | `Peut-être` | `structure la plus proche`, `Peut-être` | **absente** + pseudo-GV du S |
| 6 | **s041** | synthétique | GP | `devant elles` | `marche` | *(vide)* | `GP` | **cible vide** + verbe hors lexique |
| 7 | **s108** | synthétique | GP | `sous le nuage` | `rêve` (`papier`) | `papier` | `« sous le nuage » → ce calme papier rêve`, `rêve` | **mal choisie** + POS/lexique |
| 8 | **s122** | synthétique | GP | `vers les montagne` | `saute` (`papier`) | `papier` | `« vers les montagne » → mon papier saute`, `saute` | **mal choisie** + POS/lexique |

**Ce que la lecture par cas ajoute** (les causes se recoupent, il n'y a pas 8 causes exclusives) :

- **2 cibles vides** (g002, s041) : le segment prédit n'a **aucun** `meta.attachement`. Ce sont les
  deux seuls `cible == ""` parmi les 145 — donc deux échecs certains, jamais des « presque ».
- **2 auto-attachements** (g012, r018) : la cible choisie est un mot **du segment lui-même**
  (`manger` ⊂ `à manger`). La cible du gold (`prêt`/`prête`) est pourtant **dans les candidats**.
- **3 POS/lexique** (s041, s108, s122) : `marche`, `rêve`, `saute` sont des verbes du gold tagués
  **NOUN** (absents de `VERBES_CONNUS`), et `papier` est un nom tagué **VERB** par la règle de
  suffixe `-er` (`bloc_linguistique.py`, `_pos`). À quoi s'ajoutent **2 têtes de GV adjectivales**
  (g012, r018) : `_verbe_dans("est prêt")` rend l'auxiliaire `est`, pas l'adjectif attribut.
- **1 tokenisation** (r230) : `_mots` garde `appelle-moi` comme **un seul token** (18-29) ; le gold
  le découpe (`appelle` 18-25 + `moi` 26-29).
- **1 pseudo-GV du S** (r309) : `Peut-être` (ADV) est typé **GV** par le générateur S (0-9) ; la
  règle v2 du segment précédent le prend pour gouverneur.
- **Convention** : s108/s122 choisissent `papier`, qui est la **cible secondaire** du gold
  (`cibles[1]`, convention S) — pas `cibles[0]`. L'exact ne teste que `cibles[0]` ; le top1
  sous-chaîne les compte justes. C'est ce qui explique l'écart 140 − 137 = 3 (r230 + s108 + s122).

Par type : **GP 6, SUB 2, REL 0**. Par source : **hand 2** (g002, g012), **reel 3** (r018, r230,
r309), **synthétique 3** (s041, s108, s122). Par POS gold de la cible : **VERB 5**, **ADJ 2**,
**NOUN 1**.

## 3. Les règles candidates, chiffrées

Toutes simulées par greffe en mémoire, **appliquées dans l'ordre** ; « portée » = nombre de segments
dont la cible change, « gain net » = réparés − régressions. Exact cumulé après chaque règle.

| ordre | règle | répare | portée | gain net | exact cumulé |
|---|---|---|---:|---:|---:|
| 0 | *(base)* | — | — | — | **137** |
| 1 | **R1 — lexique verbal** (`rêver`, `sauter`, `marcher` + flexions) | s108, s122 | 2 | **+2** | **139** |
| 2 | **R2 — un GP n'est pas gouverné par un mot de son span** | g012, r018 | 2 | **+2** | **141** |
| 3 | **R3 — cible vide** : (a) génitif → tête du GN gauche ; (b) sinon verbe reconnu le plus proche | g002, s041 | 2 | **+2** | **143** |
| 4 | **R4 — enclitique** (`appelle-moi` → `appelle`) | r230 | 1 | **+1** | **144** |
| 5 | **R5 — pseudo-GV ADV** : ignorer un « GV » d'un seul token ADV ; repli sur le dernier mot du SUB | r309 | 1 | **+1** | **145** |
| | **total** | **8/8** | **8** | **+8** | **145/145** |

**R1 — lexique verbal.** `_verbe_dans` essaie le lexique (`_est_verbe`) **avant** le POS ; ajouter
`rêver`/`sauter`/`marcher` fait rendre `rêve`/`saute` au lieu de `papier` (s108/s122) et `marche` au
lieu de rien (s041). Portée **2** sur les 145, **0 régression**. Sur les 239, **13** segments
contiennent une forme de ces trois verbes, **2** seulement sont dans les 145 — c'est la même famille
que le lexique anglais de la fiche v2 (+8), avec le **même risque** : les formes sont prises dans le
gold. La variante « corriger la règle `-er` du POS » est plus générale mais non mesurée ici.

**R2 — pas d'auto-attachement pour un GP.** Un groupe prépositionnel ne peut pas être gouverné par
un mot de son propre span. Quand la cible choisie tombe **dans** le GP, on écarte les GV dont la tête
y est et on prend la tête du GV extérieur le plus proche : `est prêt à manger` (10-27) est écarté
parce que sa tête `manger` est dedans ; `est prêt` (10-18) donne `prêt` via `_tete_texte`. Portée
**2**, **0 régression**. Piège latent confirmé : `_verbe_dans("est prêt")` rend **`est`** (l'auxiliaire,
2ᵉ boucle de `_verbe_dans`), c'est `_tete_texte` qui rend la bonne tête. La règle est écrite pour les
GP ; appliquée à tous les types, elle ne change rien de plus sur ce gold : s022 (dont la cible
`nage` est aussi un token du SUB) retrouve `nage` par le GV extérieur `ils nage`.

**R3 — cible vide.** Deux branches, mesurées séparément : (a) un GP génitif (`de`/`du`/`des`) prend
la **tête du GN contigu à gauche** (`chat`, g002) ; (b) sinon, le **verbe reconnu le plus proche**
(`marche` à distance 1 pour s041, dépend de R1). Portée **2**, **0 régression** — mais **(a) n'est
juste que 2/4** sur ses quatre déclencheurs du gold (g002 `chat` ✓, g006 `chien` ✓, s081 `fenêtre` ✗
— le gold attend `trouve`, s120 `lettre` ✗ — le gold attend `prépare`). Une variante « verbe du GV
précédent d'abord, sinon tête du GN » donnerait **3/4** ; il faut un troisième repli « tête de la
cible S » pour atteindre 4/4 (s120, où le S a fusionné le verbe dans le GN) — trois branches pour
quatre cas, c'est déjà de l'ajustement au gold, et ce n'est pas simulé. Pour g002, l'autre lecture — **propager** la cible du GP
large de S (8-26) au GP étroit (8-21) — donne aussi `chat`, sans le défaut de généralité.

**R4 — enclitique.** `appelle-moi` → `appelle` (liste fermée `-moi, -toi, -nous, -vous, -le, -la,
-les, -lui, -leur, -y, -en`). Portée **1**, **+1**, 0 régression. Le vrai correctif est en amont,
dans `_mots` : le gold tokenise `appelle` + `moi`, l'heuristique un seul token. n=1, donc aucune
précision estimable.

**R5 — pseudo-GV.** Pour un SUB, la règle v2 « segment précédent » est juste **si le GV précédent
contient un verbe**. Ici le S a typé `Peut-être` en GV ; le test « un seul token, POS ADV » suffit
à l'écarter, et le repli sur le **dernier mot du SUB** donne `viendra`. Portée **1**, **+1**, 0
régression. La condition est **nécessaire** : sans elle, la même règle touche 13 SUB et en casse 12
(voir § 4).

**Ce que le total ne dit pas.** 8/8 est un **plafond par construction** : les règles sont déduites
des 8 échecs qu'elles réparent. Quatre réparations (g002, s041, r230, r309) rendent une cible qui
**n'est pas dans `candidats`** : pour rester cohérent, la règle doit aussi l'y ajouter. Sous cette
condition, top-k strict passerait aussi à **145/145** — non simulé, conséquence directe. À l'inverse,
sans mise à jour des candidats, top-k strict resterait à 141 et contredirait l'exact.

## 4. Contrôles négatifs

| contrôle | résultat | lecture |
|---|---|---|
| **complétion naïve des GV** : tout token `VERB` devient un GV | portée 13, **+3 / −8**, exact **132** (−5) | la règle « générale » qui vient naturellement **coûte 5 points** : le GV le plus proche devient un verbe du SUB ou de la relative (r041, r147, r222, r227, r258, r262, r268, r270) |
| **R5 sans la condition ADV** (tout SUB précédé d'un pseudo-GV) | portée 13, **+1 / −12**, exact **131** (−11) | la condition « un seul token + ADV » est nécessaire ; sans elle la règle casse 12 SUB justes |
| **placebo lexical** : 6 verbes corrects hors corpus (bronzer, jardiner, peindre, scier, coudre, tricoter) | portée 0, gain **0** | le gain de R1 est lexical et ciblé, pas l'effet d'un lexique plus gros |
| **R3a sur ses 4 déclencheurs du gold** | **2/4** (g002 ✓, g006 ✓, s081 ✗, s120 ✗) | la branche « tête du GN gauche » n'est pas générale ; c'est le point le plus exposé au sur-apprentissage |
| **R4 placebo** : couper à **tout** trait d'union | portée 2, +1 / −0, exact 138 ; r309 devient `Peut` (toujours faux) | sur n=1, la liste fermée d'enclitiques n'est pas discriminante |
| **oracle** : mettre la cible du gold | exact **145** | plafond trivial ; 8/8 par construction n'est pas une performance attendue |
| **hasard** (contrôle déjà dans `evaluer_gold`) | top1 **0,0042** (1/239) | plancher : la règle vivante est à 0,5858, **139×** le hasard |

## 5. Vérification des deux cas déjà connus

**r230 — « Quand tu arrives, appelle-moi. »** Confirmé : gold `appelle`, choisi `appelle-moi`,
candidats `[structure la plus proche, appelle-moi]`. Le SUB est **en tête** : la règle v2 du segment
précédent est **inerte** (aucun segment avant), la cible vient de `_cible_proche` → GV suivant
`appelle-moi`. `_verbe_dans` retombe sur le token entier (POS heuristique **NOUN**, `_est_verbe`
faux). Le gold tokenise `appelle` + `moi` ; l'heuristique, un seul token (18-29). **Ce n'est pas un
échec de la règle d'attachement mais de la tokenisation** ; R4 le répare, et c'est le seul cas de ce
type dans le gold.

**r309 — « Peut-être qu'il viendra. »** Confirmé : gold `viendra`, choisi `Peut-être`, candidats
`[structure la plus proche, Peut-être]`. Le S segmente `GV (0-9, Peut-être)` + `SUB (10-23,
qu'il viendra)`. Ici la règle v2 **s'applique** (le GV `Peut-être` finit avant le SUB) et prend son
dernier mot ; `viendra` est **dans** le SUB mais tagué **NOUN**, absent de `VERBES_CONNUS` et des
candidats. **Ce n'est pas le même échec que r230** : pseudo-GV du S + trou de lexique, pas
tokenisation. R5 le répare (ignorer le pseudo-GV, repli sur le dernier mot du SUB) ; le lexique futur
(`-ra`) réparerait aussi le POS mais c'est une règle morphologique plus large, non mesurée ici.

## 6. Limites — ce qui pourrait rendre cette fiche fausse

- **Même gold** : les règles sont déduites des 8 échecs qu'elles réparent ; 8/8 est un **plafond**,
  pas un gain attendu. Aucune n'est validée sur un gold tenu à l'écart.
- **Portée 1 à 2 segments** par règle : aucune n'est éprouvée au-delà de ses cas.
- **R1 est lexicale** et les formes (`rêve`, `saute`, `marche`) sont prises dans le gold — même
  risque d'ajustement que le lexique anglais (+8) de la fiche v2, qui était déjà une borne haute.
- **R2** est mesurée sur deux segments de **même construction** (g012/r018) : n=2.
- **R3a** est juste **2/4** sur ses déclencheurs ; **R3b** dépend de R1 et n'a qu'un cas ; **R4** et
  **R5** ont n=1.
- **Top-k strict 145/145** suppose d'ajouter la cible réparée aux `candidats` (4 cas) : non simulé.
- **L'exact ne teste que `cibles[0]`** : s108/s122 choisissent `cibles[1]`, la cible nominale du S —
  des échecs de convention, pas de compréhension.
- **Les 94 spans perdus** ne bougent pas : le rendement global reste plafonné à **145/239 = 0,6067**.
- **Aucun code modifié, aucune porte jouée** : le 8/8 est une simulation en mémoire, pas un diff.
  Les portes restent à rejouer après application.

## 7. Fichiers

- [`pensee-echecs-v2.json`](pensee-echecs-v2.json) — les 8 fiches, les 5 règles, les contrôles, les
  chiffres.
- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — lu, non modifié : `_mots`, `_pos`,
  `_est_verbe`, `VERBES_CONNUS`, `_verbe_dans`, `_cible_proche`, `_tete_texte`, branche 5 de
  `analyser`.
- [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) — lu, non modifié : `charger`,
  `evaluer_bloc`, `att_topk_exact`.
- Fiche v2 : [`rapport-pensee-attachement-v2.md`](rapport-pensee-attachement-v2.md) ; diagnostic
  top-k : [`rapport-topk-diagnostic.md`](rapport-topk-diagnostic.md) ; annotation indépendante :
  [`rapport-annotation-independante.md`](rapport-annotation-independante.md).
