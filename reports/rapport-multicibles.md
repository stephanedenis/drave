# Multi-cibles du gold et mesure d'attachement — 43 GP, +2 exact en V2 et V3

> **Ligne de roadmap** : **B13** (attachement, moteur de pensée) · tâche **A13** (multi-cibles) ·
> **Date** : 2026-11-05 · **Branche** : `s/v7` · **HEAD de mesure** : `b1b1292f` (V3) · **Statut** :
> mesure seule ; aucun fichier existant modifié ; aucun commit.
>
> **Verdict.** Les multi-cibles sont **réelles et structurées** : **43/96 GP** (44,79 %) ont deux
> cibles, toutes de la forme `[gouverneur, tête nominale]` ; aucune REL/SUB n'en a. Leur effet sur
> la mesure d'attachement est **faible mais stable** : sur les 145 segments au bon span, l'exact
> passe de **141/145 = 97,24 %** (définition actuelle `cible == cibles[0]`) à
> **143/145 = 98,62 %** (`cible in cibles`), soit **+2 cas, +1,38 pt**. Sur les 239 cibles,
> **59,00 % → 59,83 %** (+0,84 pt). La définition par **tête** (c) est un **no-op** : `(c) = (b)`,
> 143/145.
>
> Les deux gains sont **s108** et **s122**, deux GP **synthétiques** où le bloc a choisi la cible
> nominale (`papier`) que le gold autorise ; sur hand+reel, `(a) = (b) = 114/115 = 99,13 %`.
> Le contrôle négatif montre que ces deux alternatives sont **spécifiques** (permutation des
> alternatives : p = 0,0011), mais l'écart reste **non significatif** à n=145 (McNemar p=0,5 ;
> bootstrap du delta [0 ; +3,45] pt).
>
> **Robustesse au changement de version.** Au pin **V2** `15ee10d3` (bloc `5640809e…`, le contexte
> de la fiche A7), les mêmes deux cas donnent **137/145 = 94,48 % → 139/145 = 95,86 %**, soit
> **le même +2**. V3 a corrigé quatre autres échecs (g002, g012, r018, r230) et réduit les échecs
> multi de **3 à 1** (s041) ; le **delta multi reste +2**.
>
> **Recommandation.** Adopter **(b)** par fidélité au gold, sans vendre un gain robuste ; **ne pas
> ajouter (c)** ; documenter la convention multi-cible et corriger à part s041 (et r309, hors
> multi). Détail chiffré : [`pensee-multicibles.json`](pensee-multicibles.json).

## 1. Dispositif et pin

- **Population** : `charger()` → **612 phrases**, **1 863 segments**, **239 segments avec cible**
  (**96 GP, 69 SUB, 74 REL**), dont **145 au bon span** (**83 GP, 36 SUB, 26 REL**) — le
  `att_labels` d'`evaluer_bloc`, même `(type, debut, fin)`. Couverture **145/239 = 60,67 %** ;
  94 segments sans label (48 REL, 33 SUB, 13 GP).
- **Bloc** : `Heuristique` seul — c'est lui qui produit les 145 labels et le chiffre publié
  `exact = 0,9724` en V3. La cascade et le neuronal ne sont pas mesurés ici.
- **Mesure** : `meta.attachement.cible` (`.strip()`), comparée aux trois définitions :
  - **(a)** `cible == cibles[0]` — l'actuelle ;
  - **(b)** `cible in cibles` — n'importe laquelle ;
  - **(c)** `cible in {tete(c) : c in cibles}`, avec `tete = Heuristique._tete_texte`
    (« verbe plein s'il y en a un, sinon dernier mot »).
- **Dénominateurs** : **239** = rendement (les 94 sans label comptent faux) ; **145** =
  exactitude conditionnelle au span. Les deux sont donnés, par type.
- **Pin principal** : **HEAD `b1b1292f`** (V3, commit `dcf7bc91` inclus) ;
  `tools/bloc_linguistique.py` sha256 `9da6dee7…`, `evaluer_gold.py` sha256 `c4d2dbc0…`, gold
  `gold.json` `3663be6c…`, `gold_reel.json` `05d4f6df…`, `gold_synthetique.json` `e3e704ce…`.
  Le gold est **inchangé** entre V2 et V3 : seuls les choix du bloc changent.
- **Pin historique V2** : `15ee10d3`, bloc sha256 `5640809e…` — c'est le contexte de la fiche A7
  et le chiffre publié `exact = 0,9448`. Il sert de **comparaison de robustesse** (§ 3.3).
- **Note de concurrence** : le worktree `tools/bloc_linguistique.py` est encore modifié par un
  autre agent (sha256 `9544f173…`, retrait de `_cible_s_par_genre`) ; **il n'est pas mesuré**. La
  fiche pinne l'état **committé** `b1b1292f`. Le commit V3 `dcf7bc91` a déjà corrigé g002, g012,
  r018, r230 ; c'est ce qui fait passer le taux de base de 137 à 141 sous (a), sans toucher aux
  deux gains multi.

## 2. Combien de cibles multiples ?

| type | cibles | > 1 cible | % | alt. | moy. alt./cible | labels | > 1 cible | % | alt. | moy. alt./cible |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| GP | 96 | **43** | 44,79 | 43 | 0,448 | 83 | **36** | 43,37 | 36 | 0,434 |
| SUB | 69 | 0 | 0,00 | 0 | 0,000 | 36 | 0 | 0,00 | 0 | 0,000 |
| REL | 74 | 0 | 0,00 | 0 | 0,000 | 26 | 0 | 0,00 | 0 | 0,000 |
| **Total** | **239** | **43** | **17,99** | **43** | **0,180** | **145** | **36** | **24,83** | **36** | **0,248** |

En clair : **43/239 cibles (17,99 %)** et **36/145 labels (24,83 %)** ont plus d'une cible ; côté
GP, **43/96 (44,79 %)** et **36/83 (43,37 %)**. Aucun autre type n'est concerné.

- **Toutes** les multi ont **exactement 2 cibles** : aucune n'en a 3 ou plus. La longueur moyenne
  d'une liste est donc `1 + moy. alt.` = **1,180** (239) / **1,248** (145) ; parmi les multi,
  elle vaut **2,0** (1 alternative).
- **43 alternatives** au total, **33 distinctes** ; 10 sont dupliquées deux fois (`enfants`,
  `canard`, `Emma`, `avocat`, `fenêtre`, `étoile`, `chemin`, `nuage`, `papier`, `lettre`).
- **Premières cibles** : **39 VERB + 4 ADJ** (`prêt`, `ready`, `prête`, `ready`). **Alternatives** :
  **41 NOUN + 1 PRON** (`nous`) **+ 1 forme élidée** (`l'homme`, POS DET dans le gold). Ce ne sont
  jamais des verbes : la liste encode l'ambiguïté **gouverneur vs tête nominale**, pas deux
  variantes du même gouverneur.
- **Par source** : 239 → hand 5/13 (38,46 %), reel 14/171 (8,19 %), synthétique 24/55 (43,64 %) ;
  145 → hand 4/10 (40,00 %), reel 12/105 (11,43 %), synthétique 20/30 (66,67 %). Le phénomène est
  donc **rare dans le gold réel** et **massif dans le synthétique**.

## 3. Les trois définitions

### 3.1 Sur les 145 segments au bon span (exactitude, V3)

| type | n | (a) `== cibles[0]` | (b) `in cibles` | (c) `in têtes` | Δ (b−a) | Δ (c−b) |
|---|---:|---:|---:|---:|---:|---:|
| GP | 83 | 80 (96,39 %) | **82 (98,80 %)** | 82 (98,80 %) | **+2 (+2,41 pt)** | 0 |
| SUB | 36 | 35 (97,22 %) | 35 (97,22 %) | 35 (97,22 %) | 0 | 0 |
| REL | 26 | 26 (100,00 %) | 26 (100,00 %) | 26 (100,00 %) | 0 | 0 |
| **Total** | **145** | **141 (97,24 %)** | **143 (98,62 %)** | **143 (98,62 %)** | **+2 (+1,38 pt)** | **0** |

IC95 Wilson : total (a) **[93,12 ; 98,92]**, (b) **[95,11 ; 99,62]** ; GP (a) [89,90 ; 98,76],
(b) [93,49 ; 99,79] ; SUB [85,83 ; 99,51] ; REL [87,13 ; 100,00].

### 3.2 Sur les 239 cibles (rendement, V3)

| type | n | (a) `== cibles[0]` | (b) `in cibles` | (c) `in têtes` | Δ (b−a) |
|---|---:|---:|---:|---:|---:|
| GP | 96 | 80 (83,33 %) | **82 (85,42 %)** | 82 (85,42 %) | **+2 (+2,08 pt)** |
| SUB | 69 | 35 (50,72 %) | 35 (50,72 %) | 35 (50,72 %) | 0 |
| REL | 74 | 26 (35,14 %) | 26 (35,14 %) | 26 (35,14 %) | 0 |
| **Total** | **239** | **141 (59,00 %)** | **143 (59,83 %)** | **143 (59,83 %)** | **+2 (+0,84 pt)** |

IC95 Wilson : total (a) **[52,67 ; 65,04]**, (b) **[53,51 ; 65,84]**. Le dénominateur 239 dilue
l'écart (94 segments sans label) ; c'est le **145** qui isole l'attachement.

### 3.3 Comparaison V2 ─ V3 : le delta est invariant

| pin | bloc | (a) 145 | (b) 145 | Δ 145 | (a) 239 | (b) 239 | échecs multi |
|---|---|---:|---:|---:|---:|---:|---|
| **V2** `15ee10d3` | `5640809e…` | 137 (94,48 %) | 139 (95,86 %) | **+2 (+1,38 pt)** | 137 (57,32 %) | 139 (58,16 %) | g012, r018, s041 |
| **V3** `b1b1292f` | `9da6dee7…` | 141 (97,24 %) | 143 (98,62 %) | **+2 (+1,38 pt)** | 141 (59,00 %) | 143 (59,83 %) | s041 |

- Les **deux gains sont les mêmes** dans les deux pins : **s108** et **s122**. V3 a corrigé
  g002 (génitif), g012/r018 (gouverneur adjectival) et r230 (enclitique) — quatre échecs **hors
  multi-target** — ce qui remonte le taux de base de 4 cas et laisse **un seul** échec multi
  (s041, cible vide). Le **delta (b−a) reste +2** dans les deux versions.
- C'est l'argument de robustesse de la fiche : le chiffre absolu dépend de la version du bloc,
  mais **l'effet de la définition multi-cible ne dépend pas** de V2/V3.

- **Le top-k strict ne bouge pas** : **142/239** (0,5941) et **142/145 au span** (0,9793) sous
  (a), (b) et (c) en V3. Pour s108/s122, le premier gouverneur (`rêve`/`saute`) est déjà dans les
  candidats ; seul le **choix** de la cible (l'exact) change. Le `top1` et le `top-k` tolérant
  utilisent déjà **toutes** les cibles (`any(c in ...)`), donc ils n'ont jamais eu le problème.
- **Conséquence de méthode** : parmi les métriques d'attachement, seuls `exact` et `topk_exact`
  comparent à `cibles[0]` ; `top1`/`topk` étaient déjà multi-cibles. La correction est donc
  localisée.

## 4. Où l'écart se produit (et où il ne se produit pas)

Sur les **36 GP multi labellisés** (V3), le bloc choisit : **33 fois la première cible**
(gouverneur), **2 fois la seconde** (nominal), **1 fois aucune**. Les 2 choix nominaux sont
exactement les 2 gains ; le « aucune » est s041.

| id | source | type | segment | cibles | prédit | (a) | (b) |
|---|---|---|---|---|---|---:|---:|
| r309 | reel | SUB | qu'il viendra | `[viendra]` | `Peut-être` | faux | faux |
| s041 | synth | GP | devant elles | `[marche, avocat]` | `""` | faux | faux |
| **s108** | **synth** | **GP** | **sous le nuage** | `[rêve, papier]` | **`papier`** | **faux** | **juste** |
| **s122** | **synth** | **GP** | **vers les montagne** | `[saute, papier]` | **`papier`** | **faux** | **juste** |

- **4 échecs** de l'exact sous (a) en V3, **2** sous (b) : (b) corrige **s108** et **s122** et
  n'introduit **aucune** régression (`a` juste ⇒ `b` juste, par construction).
- **s041** est le seul **échec multi** de V3 (cible vide) ; (b) ne le corrige pas. **r309** est
  un échec SUB hors multi (`Peut-être` au lieu de `viendra`).
- Au pin V2, les 8 échecs comprenaient en plus **g002** (génitif sans cible), **g012/r018**
  (gouverneur adjectival : le bloc prenait `manger`), **r230** (`appelle-moi` au lieu de
  `appelle`) ; ces quatre cas sont **corrigés par V3** et ne sont plus des échecs.

Décomposition (V3) :

| sous-population | n | (a) | (b) | Δ |
|---|---:|---:|---:|---:|
| multi (> 1 cible) | 36 | 33 (91,67 %) | **35 (97,22 %)** | **+2 (+5,56 pt)** |
| mono-cible | 109 | 108 (99,08 %) | 108 (99,08 %) | 0 |
| **Total** | **145** | **141 (97,24 %)** | **143 (98,62 %)** | **+2 (+1,38 pt)** |

| source | n | dont multi | (a) | (b) | Δ |
|---|---:|---:|---:|---:|---:|
| hand | 10 | 4 | 10 (100,00 %) | 10 (100,00 %) | 0 |
| reel | 105 | 12 | 104 (99,05 %) | 104 (99,05 %) | 0 |
| synthétique | 30 | 20 | 27 (90,00 %) | **29 (96,67 %)** | **+2 (+6,67 pt)** |
| **Total** | **145** | **36** | **141 (97,24 %)** | **143 (98,62 %)** | **+2 (+1,38 pt)** |

**Le +2 est entièrement synthétique.** Sur hand+reel (115 labels), `(a) = (b) = 114/115 = 99,13 %`,
écart **0**. Les **16 GP multi de hand+reel** labellisés (4 hand + 12 reel) choisissent **tous**
la première cible (le verbe) ; les 2 choix nominaux sont dans deux phrases synthétiques
agrammaticales. C'est le point le plus important de la fiche : la correction est **juste par
convention**, mais son effet mesuré sur le gold réel est **nul**.

## 5. La définition (c) par tête est un no-op

`tete = Heuristique._tete_texte` rend le **verbe plein** s'il y en a un, sinon le **dernier mot**.

- Sur les **239 cibles**, **238 sont inchangées** ; une seule est réduite : `g003`
  `l'homme` → `homme`.
- Sur les **145 prédictions**, **aucune** n'est réduite (`_tete_texte` est l'identité sur tous les
  `meta.attachement.cible` observés).
- Aucune prédiction n'est `homme`. Donc **(c) = (b) = 143/145** en V3 ; les trois variantes
  (réduire prédiction et cibles, prédiction seule, cibles seules) donnent **143**.
- La branche « **verbe plein** » ne se déclenche jamais sur le gold : **aucune cible n'est une
  locution verbale multi-token** (toutes sont des tokens simples, dont `l'homme`, un token élidé).
  La branche « dernier mot » ne change que `l'homme`. La définition (c) n'est donc **pas
  identifiable** sur ce gold : elle ne teste pas la réduction de tête, elle ne fait que
  reproduire (b).
- Elle ne corrige pas non plus r230 (`appelle-moi` → `appelle`) : `_tete_texte("appelle-moi")`
  rend `appelle-moi` (le trait d'union est gardé) ; V3 le corrige par `_sans_enclitique`, un autre
  mécanisme.

**À retenir** : ne pas ajouter (c) au code. Si le gold encode un jour des cibles multi-tokens
(`a vu` → `vu`, `le chat` → `chat`), re-mesurer ; aujourd'hui, (c) coûte une fonction et ne change
aucun chiffre.

## 6. Contrôle négatif — permutation des cibles (1 000 tirages, V3)

Graine **20261105**, 1 000 tirages, deux contrôles complémentaires :

- **P1 global** : permutation des **239 listes de cibles** entre les 239 segments (longueurs
  conservées), puis recalcul de (b) sur les 145 labels. Casse l'association segment ↔ cibles.
- **P2 alternatives** : les **43 alternatives** sont permutées entre les 43 GP multi, les
  **premières cibles restant fixes** ; recalcul de (b) sur les 36 labels multi. C'est le contrôle
  **ciblé** : il teste si les alternatives sont les bonnes, pas seulement si la métrique est
  non-triviale.

| contrôle | observé | null (moyenne) | null 95 % | p |
|---|---:|---:|---:|---:|
| P1 global, (b) | 143/145 (98,62 %) | 1,251/145 (0,86 %) | [0 ; 4] | **0,001** |
| P1 global, gain (b−a) | 2 | 0,023 | [0 ; 0] | **0,001** |
| P2 alternatives, (b) | 35/36 (97,22 %) | 33,086/36 (91,91 %) | [33 ; 34] | **0,001** ; exact **1/903 = 0,0011** |
| P2 alternatives, gain (b−a) | 2 | 0,086 | [0 ; 1] | **0,001** |

- **P1** : le null est très bas (max 6/145) parce que le pool de cibles est fait de verbes
  largement uniques ; la métrique n'est donc pas satisfaite par hasard. Le gain nul (moyenne
  0,023, max 1) montre que le +2 n'est pas un artefact de permutation.
- **P2** : le null est **haut** (91,91 %) parce que 33/36 multi sont déjà justes par la première
  cible ; seuls 3 cas sont discordants (s108, s122, s041). Le null ne dépasse jamais **34/36** ;
  observé **35/36**. La probabilité exacte que les **deux** alternatives `papier` tombent sur
  **s108** et **s122** est `2/(43×42) = 1/903 = 0,0011` : les deux gains sont donc
  **spécifiquement** les alternatives du gold, pas n'importe quel nom.
- Le `p = 0,001` de P1/P2 est le **plancher Monte-Carlo** (0 tirage sur 1 000) ; pour P2, le
  calcul exact `1/903` est plus précis.

## 7. Incertitude, et ce qui pourrait rendre cette fiche fausse

| dénominateur | (a) | (b) | écart (b−a) |
|---|---:|---:|---:|
| 145 (span) | 141/145 = 97,24 % [93,12 ; 98,92] | 143/145 = 98,62 % [95,11 ; 99,62] | +1,38 pt ; bootstrap [0 ; +3,45] ; McNemar p=0,5 |
| 239 (rendement) | 141/239 = 59,00 % [52,67 ; 65,04] | 143/239 = 59,83 % [53,51 ; 65,84] | +0,84 pt |

- **L'écart n'est pas significatif** : 2 cas discordants pour 0 en sens inverse ; McNemar exact
  bilatéral **p = 0,5** (unilatéral 0,25) ; bootstrap du delta **[0 ; +3,45] pt**. C'est une
  **correction déterministe de 2 faux négatifs**, pas un gain de population. Il ne faut pas
  annoncer « +1,4 pt » comme un progrès robuste.
- **Les 2 gains sont synthétiques** (s108, s122) ; sur hand+reel, l'écart est **0 cas sur 115**.
  Le gold synthétique est agrammatical (« ce calme papier rêve », « vers les montagne ») : on ne
  généralise pas au texte réel.
- **La seconde cible est une tête nominale**, pas le gouverneur : compter l'attachement nominal
  comme juste est une **convention** (celle que A7 lit dans le gold), pas une vérité linguistique.
  Si la mesure visée est « gouverneur seul », (b) est trop **laxiste** : il faut alors nettoyer le
  gold, pas changer la métrique.
- **7 multi sans label** (g020, r038, r162, s027, s146, s148, s160) et **94 segments sans label**
  au total ; le 239 les compte faux, le 145 les exclut. La couverture (60,67 %) reste le facteur
  dominant du rendement.
- **Le gold peut ne pas lister toutes les alternatives** : on mesure les 43 déclarées, pas
  l'ambiguïté réelle de la langue.
- **Bloc heuristique seul** : la cascade et le neuronal ne sont pas mesurés ; leurs cibles
  peuvent différer.
- **La définition (c) est dégénérée** sur ce gold (toutes les cibles sont mono-token sauf
  `l'homme`) : son null n'est pas testé.
- **Le split verbe/nom actuel** classe par `cibles[0]` ; sous (b), s108/s122 sont justes via une
  cible **NOUN** et resteraient dans le seau « verbe » si on ne reclasse pas par la cible
  appariée. Le split actuel (116 cibles verbe / 112 justes ; 29 noms / 29 justes) deviendrait
  **114 cibles verbe / 112 justes (98,25 %)** et **31 noms / 31 justes (100,00 %)**.
- **Pin et concurrence** : la fiche vaut pour HEAD `b1b1292f`, bloc `9da6dee7…`. Le worktree
  (`9544f173…`) a encore changé ; il n'est pas inclus. Le pin V2 (`15ee10d3`, bloc `5640809e…`)
  donne 137 → 139, **même +2** et mêmes gains ; l'effet de la définition est invariant, seul le
  taux de base dépend de la version.

## 8. Recommandation sur la définition à retenir

1. **Adopter (b) `cible in cibles`** pour `exact` et, par cohérence, `topk_exact`. C'est la
   lecture fidèle du gold tel qu'il est écrit ; elle corrige **2 faux négatifs** (s108, s122),
   n'introduit **aucune** régression et ne change pas le top-k strict (142). Annoncer
   **143/145 = 98,62 %** (span) et **143/239 = 59,83 %** (rendement), avec la mention
   « +2 cas, dont 2 synthétiques ».
2. **Ne pas ajouter (c)** : no-op sur ce gold (`(c) = (b)`), et elle ne corrige ni s041 ni r309.
   À réévaluer seulement si le gold encode des cibles multi-tokens.
3. **Documenter la convention** dans `CONVENTION_CIBLE` (`gold_reel.py`) : GP multi =
   `[gouverneur, tête nominale]`, avec 39 VERB + 4 ADJ en tête et 41 NOUN + 1 PRON + 1 élidé en
   alternative. Décider explicitement si l'attachement nominal compte. Si non, **nettoyer le
   gold** plutôt que garder une liste `cibles` qui ne correspond pas à la mesure.
4. **Corriger à part s041** (cible vide) et **r309** (SUB `Peut-être` au lieu de `viendra`) ;
   (b) n'en corrige aucun. g012/r018 sont déjà corrigés par V3.
5. **Si (b) est adopté, reclasser le split verbe/nom par la cible appariée** (**114 cibles
   verbe / 112 justes**, **31 noms / 31 justes**) ; sinon les 2 gains nominaux restent comptés
   dans le seau « verbe ».
6. **Ajouter un test de non-régression** multi-cibles (s108/s122 justes sous (b), pas sous (a))
   et rejouer les portes. **Aucun code n'a été modifié dans cette fiche** ; la modification,
   si elle est retenue, est un changement séparé, testé et committé.

## 9. Reproduire

```python
import sys
sys.path.insert(0, "tools/tests/linguistique")
import evaluer_gold as eg, bloc_linguistique as bl

ph = eg.charger()                      # 612 phrases, 239 cibles
h = bl.Heuristique()
for p in ph:
    a = h.analyser(p["texte"], p["langue"])
    labels = {(e.type, e.debut, e.fin): e for e in a.etiquettes if e.niveau == "syntagme"}
    for s in p["segments"]:
        cs = s.get("cibles") or ([s["cible"]] if s.get("cible") else [])
        e = labels.get((s["type"], s["debut"], s["fin"]))
        if not cs or e is None:
            continue
        c = (((e.meta or {}).get("attachement") or {}).get("cible") or "").strip()
        juste_a = c == cs[0]
        juste_b = c in cs
        juste_c = c in [bl.Heuristique._tete_texte(x) or x for x in cs]
```

Pour la mesure **figée**, importer la copie HEAD de `tools/bloc_linguistique.py` (avec
`RACINE/tools/structures` lié au dépôt) et les trois gold de HEAD ; les hashes et les nombres
exacts sont dans [`pensee-multicibles.json`](pensee-multicibles.json) (`pin`, `definitions`,
`controle_negatif`, et `v2_contexte_A7` pour la comparaison). Le contrôle négatif se rejoue avec
`random.Random(20261105)` et 1 000 permutations.

## 10. Fichiers

- [`reports/rapport-multicibles.md`](rapport-multicibles.md) — cette fiche.
- [`reports/pensee-multicibles.json`](pensee-multicibles.json) — les 239 cibles, les 43 multi,
  les 3 définitions en V3 et en V2, les 2 gains, les 2 échecs restants, les deux contrôles
  négatifs, le pin et les limites.

Aucun fichier existant modifié ; aucun commit.
