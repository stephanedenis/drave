# B13 — s065 : la REL « qui commence » est attachée au sujet du GV qui la suit

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Tâche** : J6.2 · **Date** : 2026-11-14 ·
> **Verdict** : ✅ **règle intégrée**.
> La cible `s065` (« elle qui commence nage ») attend `elle` ; le bloc prédisait `nage`, le GV
> le plus proche. La règle **« REL suivie d'un GV → le sujet de ce GV »** corrige la cible
> **sans toucher un seul span, ni une seule POS** : **F1 0,7902 inchangé**, **attachement
> 237/238 → 238/238 labels** (238/239 cibles, **0,9958**), **exactitude sur les spans
> 0,9958 → 1,0**. Le gain est **en dev** ; le test ne contient aucun cas déclencheur et reste
> à **76/76**. La règle est intégrée avec un test unitaire, la porte du bloc est verte.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (règle intégrée),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) (`charger`, `evaluer_bloc`),
> [`gold_split.py`](../tools/tests/linguistique/gold_split.py) ; copies locales dans
> `/tmp/s065/` (`bloc_base.py` avant règle, `bloc_rel_gn.py`, `bloc_rel_apres_gv.py`,
> `bloc_placebo.py` pour les contrôles) ; **0 fichier du dépôt modifié pour la mesure**.
> JSON : [`pensee-s065.json`](pensee-s065.json).

## 1. Le span, la phrase, la règle

`s065` — « elle qui commence nage » (synthétique, français). Le gold :

| segment | span | cible |
|---|---|---|
| GN « elle » | 0:4 | — |
| **REL « qui commence »** | **5:17** | **`elle`** |
| GV « nage » | 18:22 | — |

Le bloc prédit le **même span** pour la REL courte (5:17), mais lui donne pour cible `nage`,
le GV le plus proche. Le gold attend `elle`, le **sujet de ce GV**. Le défaut est donc **la
cible, pas le span** : c'est la dernière cible fausse des 239 cibles, l'autre étant `g017`
(toujours sans label, span manquant).

**Une précision de mandat.** Le mandat écrit « elle nage qui commence » et « REL après GV ».
Le texte du gold est « elle **qui commence** nage » : l'ordre de surface est **GN REL GV**, pas
GV REL. La règle littérale « REL après un GV » ne s'applique à **aucun** segment du gold dans
le chemin union (**0 cas**) et laisse le compte à 237/238 (§ 5). La règle qui traite `s065`
est donc la règle **symétrique** : une REL **suivie** d'un GV prend pour cible le **sujet de
ce GV**, c'est-à-dire le GN le plus proche à sa gauche.

Le chemin d'analyse explique le défaut : le générateur S fournit le GN `elle` et une REL
longue 5:22 ; le chunker simple fournit la REL courte 5:17 et le GV 18:22. Dans l'union, la
REL courte n'a **aucun GN précédent dans le chunker simple** : `_cible_precedent` ne peut pas
la résoudre, et `_cible_proche` tombe sur le GV `nage`. La règle traverse la frontière des
deux chemins : elle cherche le GV à droite et le GN à gauche dans **l'ensemble** des segments
(S + chunker).

```python
# tools/bloc_linguistique.py — Heuristique._cible_rel_sujet
if segment.get("type") != "REL":
    return None
droites = [x for x in tous if x.get("type") == "GV"
           and x.get("debut", 0) >= segment.get("fin", 0)]
gauches = [x for x in tous if x.get("type") == "GN"
           and x.get("fin", 0) <= segment.get("debut", 0)]
if not droites or not gauches:
    return None
gn = max(gauches, key=lambda x: x["fin"])
return Heuristique._tete_nom(texte, gn["debut"], gn["fin"])
```

L'appel est placé dans la boucle **union**, après `_cible_precedent` et avant
`_repli_cible_gp`/`_cible_proche`. La règle exige **trois** conditions : le segment est une
REL, un GV commence à sa droite, un GN finit à sa gauche. Elle ne s'applique donc ni aux SUB,
ni aux GP, ni aux REL sans GV à droite.

## 2. La mesure

Gold vivant : **612 phrases**, **239 cibles**. Split déterministe `crc32(id) % 3` :
**dev 422 phrases / 163 cibles**, **test 190 / 76**. Base = le bloc avant la règle ; règle =
la production après intégration.

| mesure | base | règle | Δ |
|---|---:|---:|---:|
| **F1 all** | **0,7902** | **0,7902** | **0** |
| précision / rappel (all) | 0,7860 / 0,7944 | 0,7860 / 0,7944 | 0 / 0 |
| tp / fp / fn (all) | 1480 / 403 / 383 | 1480 / 403 / 383 | 0 / 0 / 0 |
| tête (F1) | 0,9029 | 0,9029 | 0 |
| **POS** | **0,8625** | **0,8625** | **0 token** (0/3179) |
| **attachement exact / labels** | **237 / 238** | **238 / 238** | **+1 / 0** |
| exact / cibles | 237/239 (0,9916) | **238/239 (0,9958)** | **+1** |
| **exactitude sur les spans** | **0,9958** | **1,0** | **+0,0042** |
| couverture | 0,9958 | 0,9958 | 0 |

| moitié | phrases | cibles | F1 base → règle | attachement base → règle | spans |
|---|---:|---:|---:|---:|---:|
| **dev** | 422 | 163 | 0,7875 → **0,7875** | 161/162 → **162/162** | 0,9938 → **1,0** |
| **test** | 190 | 76 | 0,7962 → **0,7962** | 76/76 → **76/76** | 1,0 → **1,0** |

Par source :

| source | n | F1 base | F1 règle | attachement base | attachement règle |
|---|---:|---:|---:|---:|---:|
| hand | 20 | 0,9016 | 0,9016 | 12/12 (13 cibles) | 12/12 (13 cibles) |
| reel | 432 | 0,7857 | 0,7857 | 171/171 | 171/171 |
| synthétique | 160 | 0,7888 | 0,7888 | **54/55** | **55/55** |

Le gain est **exactement un** : `s065`, en synthétique et en **dev**. Le test ne bouge pas
parce qu'il ne contient **aucun** cas qui déclenche la règle. Ce n'est pas une validation
hors échantillon : c'est l'absence de contre-exemple en test, pas une confirmation.

## 3. La phrase changée

Une seule annotation change dans les 612 phrases — diff complet des syntagmes et des POS :

| phrase | avant | après | effet |
|---|---|---|---|
| **s065** « elle qui commence nage » | REL 5:17 → **`nage`** | REL 5:17 → **`elle`** | **+1 cible exacte** |

Aucun span de syntagme, aucune POS, aucun autre attachement ne change. La REL longue 5:22,
elle, était déjà attachée à `elle` ; le GN `elle` reste attaché à `nage` (le gold ne lui donne
pas de cible, donc ce n'est pas mesuré).

## 4. Les contrôles négatifs

| contrôle | F1 | tp / fp / fn | attachement | spans | lecture |
|---|---:|---:|---:|---:|---|
| **règle littérale** : REL dont le **précédent** est un GV | 0,7902 | 1480 / 403 / 383 | **237/238** | 0,9958 | **0 cas** dans le chemin union ; ne corrige pas `s065`. La formulation du mandat, prise au mot, est vide sur ce gold. |
| **variante large** : REL → GN le plus proche à gauche, sans condition de GV | 0,7902 | 1480 / 403 / 383 | **238/238** | 1,0 | même résultat sur ce gold ; **non retenue** : elle attacherait une REL sans prédicat à droite, ce que le gold ne teste pas. |
| **placebo** : REL sans cible prend son propre verbe avant le GV le plus proche | 0,7902 | 1480 / 403 / 383 | **235/238** | 0,9874 | **−2 exacts** (`s065` et un autre) : le gain n'est pas un artefact de n'importe quel repli. |
| **hasard** : une cible tirée parmi les cibles du gold | — | — | 0,0042 | — | plancher de la métrique. |

La variante large et la règle retenue donnent le **même** compte sur ce gold. Le choix de la
règle étroite est un choix de **sens** (une REL suivie d'un GV a un prédicat à droite), pas un
gain de mesure. C'est dit ici pour que le chiffre ne soit pas lu comme une préférence
empirique entre les deux.

## 5. La convention du gold

Les **74 REL** du gold ont toutes un GN à gauche et un GV à droite. **73** étaient déjà
justes par la règle existante (`_cible_precedent` : REL après un GN → tête du GN). `s065` est
la seule où le GN sujet n'est pas dans le chunker simple : le GN vient de S, la REL courte du
chunker. La règle n'invente donc pas une convention : elle applique **le même antécédent**
que la règle existante quand le GN est fourni par l'autre chemin de segmentation.

C'est la différence avec `g017` ([fiche](rapport-g017.md)) : là, le gold se contredisait
(inclure/exclure l'adverbe final) ; ici, le gold est **cohérent** (REL → antécédent) et le
défaut venait du **chemin d'analyse**, pas de l'annotation.

## 6. Ce qui pourrait rendre cette fiche fausse

- **Un seul cas, en dev.** Le test ne contient aucun cas déclencheur : la règle n'est pas
  confirmée hors échantillon. Un gold tenu à l'écart avec la même structure (`GN REL GV` où
  le GN n'est fourni que par S) est nécessaire avant de la dire générale.
- **`s065` est synthétique et peu naturel** (« elle qui commence nage »). L'annotation peut
  être un artefact du générateur ; la phrase n'a pas été relue par un locuteur.
- **La règle dépend du générateur S.** Si S ne fournit pas le GN sujet, la règle ne
  s'applique pas ; elle ne remplace pas un chunker qui trouverait le GN tout seul.
- **« Le GN le plus proche à gauche » est supposé être le sujet.** Un GN antéposé (objet,
  circonstant) serait choisi à tort. Aucun cas du gold ne teste ce piège.
- **La règle littérale du mandat n'est pas mesurée sur un cas.** Si l'intention était
  « REL après GV », elle reste vide ici ; la fiche mesure la règle symétrique, qui est celle
  que `s065` demande.
- **Le compte est un compte de cibles.** 238/239 garde `g017` au dénominateur ; 238/238 est
  le taux sur les labels (couverture 0,9958). Les deux lectures sont dans le JSON.
- **Les 84 portes n'ont pas été rejouées.** La porte du bloc est verte et les 20 tests
  unitaires passent ; une passe complète reste à faire si la règle touche d'autres chemins.

## 7. La décision

**La règle est intégrée.** Le code est dans `_cible_rel_sujet` (appel union), le test
`test_rel_suivie_d_un_gv` verrouille `s065` et l'absence de cible inventée sans GV à droite.
Le bloc reste à **F1 0,7902**, **POS 0,8625**, **238/238 labels** et **238/239 cibles
(0,9958)**. `g017` reste le dernier écart : ce n'est pas une cible, c'est un **span** et une
**convention d'adverbe à trancher** ([fiche](rapport-g017.md)).

La suite, dans l'ordre :

1. **Trancher la convention d'adverbe** (`g017`), puis rejouer la variante étroite de J6.1.
2. **T132/T133**, puis le gold 200+.
3. **Une passe complète des portes** au prochain cycle, la porte du bloc étant verte.

## 8. Fichiers

- **Cette fiche** : `reports/rapport-s065.md`.
- **JSON** : [`pensee-s065.json`](pensee-s065.json) — reproduction, règle, mesures
  all/dev/test et par source, diff, contrôles, limites.
- **Code** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_cible_rel_sujet`,
  appel union).
- **Test** : [`test_bloc_linguistique.py`](../tools/tests/linguistique/test_bloc_linguistique.py)
  (`test_rel_suivie_d_un_gv`).
- **Mesure** : `/tmp/s065/mesure.py` (non commité) ; copies `/tmp/s065/bloc_base.py`,
  `bloc_regle.py`, `bloc_rel_gn.py`, `bloc_rel_apres_gv.py`, `bloc_placebo.py`.
- **Lecture seule** : [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
  [`gold_split.py`](../tools/tests/linguistique/gold_split.py),
  [`gold.py`](../tools/tests/linguistique/gold.py).
- **Contexte** : [`rapport-g017.md`](rapport-g017.md) § 9 (le dernier span et la convention
  d'adverbe), [`rapport-semaine.md`](rapport-semaine.md) (237/238, `g017` et `s065`).
