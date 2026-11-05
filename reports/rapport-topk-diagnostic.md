# B13 — le top-k strict de l'attachement : 57 échecs, dont 45 d'emballage

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 ·
> **Verdict** : ✅ **les 57 échecs du top-k strict sont qualifiés** (0 « autre »). Sur les
> **145 segments gold dont le span est prédit**, la cible est dans les candidats **134 fois en
> sous-chaîne** (0,9241) mais **88 fois en égalité exacte** (0,6069) : **57 échecs**. **45** sont
> des **candidats du générateur S non réduits à leur tête** — la cible est déjà dans la chaîne
> « « segment » → … », il suffit d'en extraire la tête ; **8** sont des **verbes anglais hors
> lexique** ; **4** sont de la **couverture locale** (génitif, enclitique, GV mal délimité).
> Le **top-1 est déjà juste 41 fois sur 57** : le top-k strict mesure surtout l'**emballage** des
> candidats, pas le choix de la cible. Trois correctifs **simulés, non appliqués**, couvrent
> **45 + 8 + 4 = 57** — borne haute, mesurée sur le même gold.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`Heuristique`,
> `_tete_nom`, `_verbes_proches`, `VERBES_CONNUS`) · [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py)
> (`charger()`, `evaluer_bloc`) · JSON [`pensee-topk-diagnostic.json`](pensee-topk-diagnostic.json)
> (57 lignes, une par échec) · script de diagnostic exécuté par heredoc, **lecture seule** :
> aucun fichier existant modifié, aucun commit.

## 1. La mesure

Gold de **612 phrases** (20 `hand` + 432 `reel` + 160 `synthetique`), **239 cibles**, **145
segments dont le span est prédit**. Deux lectures du top-k coexistent dans `evaluer_bloc` :

| mesure (sur 145 segments au bon span) | valeur | taux |
|---|---:|---:|
| cible trouvée en **sous-chaîne** (top-k lenient) | 134 | 0,9241 |
| cible trouvée en **égalité exacte** (top-k strict) | **88** | **0,6069** |
| **échecs stricts** | **57** | 0,3931 |
| dont **top-1 déjà juste** (cible choisie = cible gold) | 41 | — |
| top-1 exact (rendement sur les 145) | 123 | 0,8483 |

Rendement global (÷ **239** cibles, spans manquants compris) : top-k lenient **0,5607**
(134/239), top-k strict **0,3682** (88/239). Le plafond du rendement global est la couverture
de span : **145/239 = 0,6067**, même si les 57 échecs sont tous réparés.

**Ce que ça dit.** L'écart 134 − 88 = **46** est le cœur du problème : la cible est **déjà
présente** dans la liste, mais **engluée dans une chaîne de présentation** (« « que j'ai lu » →
Le livre ») qui n'est pas un candidat. Le top-1 (123/145) est bien meilleur que le top-k strict
(88/145) : **41 des 57 échecs ont la bonne cible choisie**. Ce n'est donc pas d'abord un
problème de règle d'attachement, mais de **forme des candidats**.

## 2. Les 57 échecs, qualifiés

Classement **exclusif**, produit par le script (règle de décision par cause, aucune ligne
« autre »). `sous-chaîne` = la cible apparaît dans un candidat sans lui être égale.

| # | cause | eff. | dont sous-chaîne | types | sources | correctif |
|---|---|---:|---:|---|---|---|
| C1 | **candidat S non réduit — cible nominale** (« … → Le livre ») | 26 | 26 | REL 26 | hand 1, reel 25 | F1 |
| C2 | **candidat S non réduit — cible verbale** (« … → Les fleurs poussent ») | 17 | 17 | GP 17 | reel 7, synth. 10 | F1 |
| C3 | **candidat S non réduit — cible attribut** (« … → est prêt ») | 2 | 2 | GP 2 | hand 1, reel 1 | F1 |
| C4 | **verbe anglais hors lexique** (`fly`, `climbs`…) | 8 | 0 | GP 8 | reel 8 | F2 |
| C5 | **GP génitif — tête du GN à gauche jamais candidate** | 1 | 0 | GP 1 | hand 1 | F3 |
| C6 | **verbe français hors lexique, aucun GV** (`marche`) | 1 | 0 | GP 1 | synth. 1 | F3 |
| C7 | **candidat tokenisé avec enclitique** (`appelle-moi`) | 1 | 1 | SUB 1 | reel 1 | F3 |
| C8 | **GV du S mal délimité** (`Peut-être` pris pour un GV) | 1 | 0 | SUB 1 | reel 1 | F3 |
| | **total** | **57** | **46** | REL 26, GP 29, SUB 2 | hand 3, reel 43, synth. 11 | |

**Lecture par cause.**

- **C1 (26 REL)** : le S nomme l'antécédent dans `« que j'ai lu » → Le livre` ; `_tete_nom`
  rendrait `livre`, mais `candidats` garde la chaîne entière (plus `est`). Exemple :
  `g011` « que j'ai lu » → `livre`, candidats `["« que j'ai lu » → Le livre", "est"]`.
- **C2 (17 GP)** : le S nomme le verbe dans `« dans le jardin » → Les fleurs poussent` ; la
  cible `poussent` est le **dernier token** de la queue. 15/17 ont déjà la bonne cible choisie ;
  **s108** et **s122** choisissent en plus le nom `papier` au lieu de `rêve`/`saute` (la cible
  nominale du S, `cible_nom`, passe avant `cible_verbe`).
- **C3 (2 GP)** : `g012` « à manger » → `prêt`, `r018` → `prête` ; la cible est l'adjectif
  attribut de `est prêt`/`est prête`, la cible choisie est le verbe `manger`.
- **C4 (8 GP anglais)** : `_est_verbe("fly")` est faux (absent de `VERBES_CONNUS`), le POS le
  tague NOUN et le GV du S n'est pas coupé au verbe ; les candidats sont `["GP", "lake"]` au
  lieu de contenir `fly`. Les 8 verbes manquants : `fly, climbs, flows, swims, get, smiles,
  wait, belongs`.
- **C5 (1)** : `g002` « Le chat de la voisine dort » — convention du gold (commit `0ddd4fb9`) :
  pour un génitif, la cible est le nom complété (`chat`). Le GV `dort` est avalé par le GP dans
  le S et aucun candidat nominal de gauche n'est produit.
- **C6 (1)** : `s041` « les avocat marche devant elles » — `marche` est tagué NOUN, aucun GV
  n'est détecté, la liste tombe à `["GP"]`.
- **C7 (1)** : `r230` « Quand tu arrives, appelle-moi » — la cible est `appelle`, le candidat
  est le token entier `appelle-moi` : le trait d'union n'est pas découpé.
- **C8 (1)** : `r309` « Peut-être qu'il viendra » — le S prend `Peut-être` pour un GV et
  `viendra` n'est ni reconnu ni candidat.

## 3. Trois correctifs, ordonnés par gain

Tous sont **simulés** (greffe de lexique et ajout de candidats en mémoire), **aucun n'est
appliqué** : le code du dépôt est inchangé. La colonne « gain » est **incrémentale** dans
l'ordre proposé. Fichier commun : [`tools/bloc_linguistique.py`](../tools/bloc_linguistique.py).

| ordre | correctif | fonction à modifier | gain top-k strict | top-1 |
|---|---|---|---:|---:|
| 1 | **F1 — réduire chaque candidat S à sa tête** | `Heuristique.analyser`, branche « 5. syntagmes » (construction de `noms` l. 826 et de `candidats` l. 858/874/892) ; helper existant `_tete_nom` (l. 616) | **+45** | 0 |
| 2 | **F2 — compléter le lexique verbal anglais** | `_est_verbe` (l. 428) via `VERBES_CONNUS` (l. 374) ; pour le POS, `VERBES["en"]` (l. 319) | **+8** | +8 |
| 3 | **F3 — repli par tokens** (GN à gauche, verbes reconnus, enclitiques) | `Heuristique._verbes_proches` (l. 670) et `Heuristique._cible_proche` (l. 643) ; compléter `VERBES_CONNUS` | **+4** | +4* |

\* top-1 conditionnel : F3 ne le rend que si `_cible_proche` suit la même règle (non simulé).

**F1 — 45 segments (C1 26 + C2 17 + C3 2).** Pour chaque candidat S de la forme
`« segment » → queue`, prendre la queue après `→` et ajouter sa **tête** aux `candidats` :
`_tete_nom("Le livre")` → `livre`, `_tete_nom("Les fleurs poussent")` → `poussent`,
`_tete_nom("est prêt")` → `prêt`. L'élision est déjà gérée (`L'homme` → `homme`) — c'est le
même piège que T170, resté dans l'emballage des candidats. Variante plus propre que le
découpage de la chaîne d'affichage : lire `_cibles_s` par segment et en prendre la tête.
**F1 ne change pas le top-1** : s108/s122 (`papier` au lieu de `rêve`/`saute`) et g012/r018
(`manger` au lieu de `prêt`) restent faux en top-1.

**F2 — 8 segments (C4).** Ajouter à `VERBES_CONNUS` : `fly, climb, flow, swim, get, smile,
wait, belong` et leurs flexions (`-s`, `-ed`, `-ing`, irréguliers `flew/flown, swam/swum,
got/gotten`). Le GV du S est alors coupé au verbe et `_verbe_dans` rend `fly` au lieu du
dernier nom (`lake`). Mesuré : **+8 top-k et +8 top-1**, **0 régression** sur les 145 segments.

**F3 — 4 segments (C5, C6, C7, C8).** Quatre ajouts coordonnés à la source de candidats :
(a) pour un **GP**, ajouter la **tête du GN à gauche** (`de la voisine` → `chat`) ;
(b) **si aucun GV**, balayer les **verbes reconnus** dans une fenêtre autour du segment ;
(c) **découper les enclitiques** (`appelle-moi` → `appelle`) ;
(d) compléter `VERBES_CONNUS` (`marche`, `appelle`, `viendra`) pour que (b) et (c) mordent.
(a) répare `g002` et `s041` — `s041` seulement parce que le GN du chunker avale le verbe
(`les avocat marche`) : c'est fragile, et c'est justement l'argument pour (d).

**Gains cumulés (simulés).**

| étape | top-k strict | taux | top-1 |
|---|---:|---:|---:|
| base | 88/145 | 0,6069 | 123/145 |
| + F1 | 133/145 | 0,9172 | 123/145 |
| + F2 | 141/145 | 0,9724 | 131/145 |
| + F3 | **145/145** | **1,0** | 135/145* |

\* conditionnel : le top-1 de F3 n'est pas simulé ; seule la colonne top-k est mesurée.

## 4. Contrôle négatif

Quatre témoins, exécutés par le même script, mesurent la **spécificité** de chaque correctif :

| témoin | résultat | lecture |
|---|---:|---|
| F1 avec le **premier** token de la queue au lieu de la tête | **0/45** | le gain vient de la position de tête, pas du fait d'ajouter un token quelconque |
| F2 avec 8 verbes anglais **non pertinents** (`jump, read, write, eat, sleep, run, sing, dance`) | **0/8** | des verbes anglais corrects mais hors cible ne réparent rien : le gain est lexical, pas générique |
| F3 avec le **premier mot de la phrase** ajouté comme candidat | **0/4** | un token arbitraire ne répare pas ; il faut la bonne relation (GN à gauche / verbe) |
| **oracle** : ajouter la cible du gold elle-même | **57/57** | plafond trivial : la mesure compte la **couverture** des candidats, pas la compréhension |

L'oracle est le contrôle qui **borne l'interprétation** : les 57/57 de la ligne F1+F2+F3 sont un
plafond par construction (même gold), pas une performance attendue. Les trois témoins montrent
que les gains ne sont pas l'effet d'un ajout aléatoire ; ils ne prouvent pas la généralisation.

## 5. Limites — ce qui pourrait rendre cette fiche fausse

- **Même gold** : les correctifs sont déduits des 57 échecs du gold de mesure ; les gains sont
  des **bornes hautes**, pas une estimation de généralisation. Un gold tenu à l'écart est requis
  avant de conclure.
- **F3(d) est le point le plus exposé au sur-apprentissage** : `marche`, `appelle`, `viendra`
  sont des formes observées dans le gold. F2 l'est aussi (les 8 verbes anglais sont ceux du
  gold), même s'il s'agit de verbes courants.
- **F1 ne répare pas le top-1** : 4 segments (s108, s122, g012, r018) gardent une cible choisie
  fausse. Le top-k strict est un indicateur de **couverture**, pas de qualité du choix.
- **Couplage au format d'affichage du S** : F1 découpe `nom = « … » → …`, une chaîne de
  présentation. La bonne API est `attachement` par segment (le S l'a déjà pour le dernier
  segment ambigu) ; le découpage de chaîne est un pis-aller.
- **Chevauchement F2/F3** : le GN du chunker avale le verbe, donc la tête du GN à gauche d'un GP
  anglais vaut déjà le verbe (`fly`). Isolé, F3 vaudrait **29**, dont **25 recouvrent F1 (17 C2)
  et F2 (8 C4)** : c'est un chevauchement, pas un gain supplémentaire.
- **Rendement global plafonné** : 145/239 = **0,6067**, car 94 cibles n'ont pas de span prédit.
  Aucun correctif de candidats ne franchira cette borne.
- **Aucune porte ni régression** : le code n'est pas modifié (mesure en lecture seule) ; les
  gains sont des simulations, pas un diff. Les portes restent à rejouer après application.
- **Le gold mêle deux conventions** (verbe gouverneur / nom antécédent) ; le diagnostic les
  sépare par le POS du gold, mais la convention reste une hypothèse mesurée, pas une vérité
  documentée par le corpus.

## 6. Annexe — les 57 segments, par cause

- **C1 (26)** : g011, r014, r015, r054, r055, r094, r095, r201, r203, r209, r213, r221, r226,
  r228, r231, r233, r235, r253, r257, r259, r261, r263, r265, r267, r269, r275.
- **C2 (17)** : r047, r057, r088, r100, r126, r139, r150, s045, s047, s058, s064, s108, s109,
  s120, s122, s144, s150.
- **C3 (2)** : g012, r018.
- **C4 (8)** : r080, r108, r120, r156, r166, r169, r177, r180.
- **C5 (1)** : g002.
- **C6 (1)** : s041.
- **C7 (1)** : r230.
- **C8 (1)** : r309.

Le détail par segment (type, texte, cible gold, cible choisie, candidats, cause, raison) est
dans [`pensee-topk-diagnostic.json`](pensee-topk-diagnostic.json).

## 7. Fichiers

- [`pensee-topk-diagnostic.json`](pensee-topk-diagnostic.json) — mesure, causes, correctifs,
  contrôles, limites, **57 lignes** de diagnostic.
- [`../tools/bloc_linguistique.py`](../tools/bloc_linguistique.py) — `Heuristique.analyser`,
  `_tete_nom`, `_verbes_proches`, `_cible_proche`, `VERBES_CONNUS` (à modifier, non modifiés).
- [`../tools/tests/linguistique/evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) —
  `charger()`, `evaluer_bloc` (mesure du top-k strict, `att_topk_exact`).
