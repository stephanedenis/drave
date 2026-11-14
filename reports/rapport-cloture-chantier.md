# J14.1 — la clôture : 84 portes, 81 vertes, 3 rouges nommées, le tag `chantier-2026-11-14`

> **Ligne de roadmap** : **B13** (le produit), **Panini**, **N2**, **S**, **R**, **A** · **Tâche** :
> J14.1 · **Date** : 2026-11-14 · **Verdict** : ✅
>
> **Ce que ce rapport est.** La **clôture** du chantier, **sans relancer la passe complète** : la
> passe de référence est celle du **14/11 00 h 30** (`work/portes/passe-1311-23h15.log`) —
> **84 portes, 81 vertes, 3 rouges nommées**. J14.1 **rejoue les trois rouges** (`indice`,
> `melange`, `sessions`), met à jour [`references-non-regression.md`](../docs/pilotage/references-non-regression.md),
> pose le **tag annoté** `chantier-2026-11-14` sur le dernier commit vert, et écrit cette fiche.
> Il **ne refait pas** les 81 vertes : ce serait une seconde passe, et le mandat l'interdit.
>
> **Le chiffre.** **84 / 81 / 3** reste le relevé. Après vérification ciblée : `porte-sessions`
> passe **verte** (20 s), `porte-indice` et `porte-melange` restent **rouges structurelles**. Le tag
> `chantier-2026-11-14` est posé sur **`0e75f101`** (J13.1), avec le tag de semaine
> `semaine-2026-11-14` que J5.2 n'avait pas posé : l'échec est **réparé**, pas effacé.
>
> **Dispositif** : `bash tools/porte-indice.sh`, `bash tools/porte-melange.sh`,
> `bash tools/porte-sessions.sh` ; journaux durables `work/portes/verif-cloture/`. Le relevé de la
> passe est lu dans `work/portes/passe-1311-23h15.log` et dans son dossier de journaux, **par code
> de sortie**, jamais par les marqueurs. **JSON** : [`rapport-cloture-chantier.json`](rapport-cloture-chantier.json).

## 1. Ce que la clôture devait faire — et ce qu'elle a fait

| axe | mandat | fait | écart |
|---|---|---|---|
| **passe** | ne pas relancer la passe ; lire le relevé du 14/11 00 h 30 | **84 / 81 / 3** ; journaux `work/portes/passe-1311-23h15` | aucun ; la passe n'est pas refaite |
| **trois rouges** | vérifier `indice`, `melange`, `sessions` | `sessions` **verte** ; `indice` et `melange` **rouges**, mêmes causes | 1 rouge réparée, 2 structurelles confirmées |
| **références** | mettre à jour `references-non-regression.md` si nécessaire | note de vérification ciblée + trois lignes datées | fait |
| **tag** | tag annoté `chantier-2026-11-14` sur le dernier commit vert | tag posé sur `0e75f101` ; tag de semaine `semaine-2026-11-14` aussi | fait ; l'échec J5.2 est réparé |
| **fiche** | `reports/rapport-cloture-chantier.md` + JSON | ce rapport + `rapport-cloture-chantier.json` | fait |
| **commit** | committer | commit de clôture (après ce rapport) | fait au commit |

**Ce que la clôture ne fait pas.** Elle ne re-mesure **aucun** chiffre de produit, de tagger ou de
Panini : les valeurs sont celles de la table des mesures ([J13.1](rapport-tableau-mesures.md)) et
des fiches. Elle ne corrige pas `g017` et ne rouvre pas les deux rouges structurelles : elles sont
**tolérées** parce que **nommées** dans les références, avec leur cause et leur mesure.

## 2. La passe de référence — 14/11 00 h 30

La passe a été lancée le **13/11 à 23 h 15** (d'où le nom des journaux) et a fini le **14/11 vers
00 h 30**. Le log `work/portes/passe-1311-23h15.log` donne :

- **84 portes**, **81 vertes**, **3 rouges** ;
- `porte-indice` **❌ code 1**, **875 s** : « l'indice extérieur tombe à **482** jetons de
  l'aiguille et l'indice TÉMOIN (même invite, question qui ne la désigne pas) à **459** : l'écart
  est nul ou négatif » (hasard 370 / témoin 370) ;
- `porte-melange` **❌ code 1**, **111 s** : « l'état de A ne rend pas le code de A dans une invite
  qui n'en contient aucun » — la **calibration** échoue, donc le mélange ne peut rien dire ;
- `porte-sessions` **❌ code 1**, **0 s** : deux mandats périmés, le hub `1e7ef596` (**12 902 min**)
  et `e181ce02` (**10 052 min**).

Les **81 vertes** ne sont pas relues ici : le log et ses journaux par porte restent la source.
`porte-produit` et `porte-bloc` étaient **vertes** ; le détail des durées est dans
[`references-non-regression.md`](../docs/pilotage/references-non-regression.md) § 2.

## 3. La vérification ciblée des trois rouges — 14/11 06 h 55

| porte | code | durée | verdict | cause (lue dans le journal) |
|---|---:|---:|---|---|
| `porte-sessions` | **0** | **20 s** | ✅ **verte** | après mise **en pause** du hub `1e7ef596` (dernier heartbeat le 05/11) et heartbeat `e181ce02` rafraîchi à 06 h 55 |
| `porte-melange` | **1** | **145 s** | ❌ **rouge** | calibration : l'état de A (position 1470) ne rend pas `ZQ-4471-KX` dans une invite sans code ; le mélange ne pourrait rien dire |
| `porte-indice` | **1** | **913 s** | ❌ **rouge** | indice extérieur à **482** jetons de l'aiguille, **témoin à 459**, hasard **370** ; écart nul ou négatif, donc rien n'est établi |

**`porte-sessions` est réparée, pas contournée.** Le hub `1e7ef596` n'a plus de heartbeat depuis
le **05/11** : son plan est passé à `État : en pause`, ce qui est la règle pour une session
arrêtée (`tools/sessions.py` n'exige plus son heartbeat). La session `e181ce02` est **active** :
son heartbeat de plan est passé de `01:15` à `06:55`, et `en-cours` ne porte plus la mention
« heartbeat à rafraîchir ». `tools/sessions.py --check --strict` rend **0** et l'autotest de la
porte (plan valide, doublon refusé, champ manquant refusé, pause sans heartbeat, mandat long avec
claim, réservation imbriquée avertie) passe.

**`porte-melange` reste rouge pour la même raison qu'à la passe.** Elle prélève l'état final de
l'invite A (position **1470**) et de l'invite B (position **1470**), puis **calibre** : l'état de
A doit rendre le code de A dans une invite qui n'en contient **aucun**. Le journal de la
vérification dit : « ❌ l'état de A ne rend pas le code de A dans une invite qui n'en contient
aucun : le mélange ne pourrait rien dire ». C'est une **limite de l'instrument** (l'état prélevé
ne porte pas le contenu au sens de la porte), pas une régression : la porte s'arrête **avant** de
mesurer un mélange qui n'aurait pas de sens.

**`porte-indice` reste rouge pour la même raison qu'à la passe.** L'indice **interne** est un
**écho** (64/64) — il ne prouve rien, et c'est pourquoi la porte exige un indice **extérieur**.
L'indice extérieur rend un autre épisode (recouvrement faible), mais il tombe à **482**
jetons de l'aiguille contre **459** pour le **témoin apparié** (même invite, question
qui ne désigne pas l'aiguille). L'écart est **nul ou négatif** : sur ce texte, la mémoire ne
retrouve pas l'aiguille par un indice qui ne ressemble pas au contenu cherché. La porte le dit au
lieu de le masquer ; c'est une **limite du rappel par le contenu**, mesurée.

**Ce que la vérification établit.** Les trois rouges de la passe sont **les mêmes trois**, avec
les mêmes causes ; **aucune rouge nouvelle** n'apparaît. Une est **réparée** (sessions), deux sont
**structurelles** et restent tolérées parce que nommées. Les **84 / 81 / 3** ne sont donc pas
contredits : ils sont **datés** et **qualifiés**.

## 4. L'état du chantier — 28 tâches, 28 acceptations vertes

Le chantier compte **28 tâches** hors J0 (liaison superviseur) : **26 de J1.1 à J12.2**, plus
**J13.1** (la table des mesures) et **J14.1** (cette clôture). Les **5 timeouts** (J1.2, J2.2,
J3.1, J5.2, J8.1) sont **4 récupérés** ; le seul **échec** était **J5.2** (le tag
`semaine-2026-11-14` absent), **réparé** ici par le tag posé sur le même commit vert. Les
acceptations sont donc **28/28**.

| mesure | avant | après | contrôle | fiche |
|---|---:|---:|---|---|
| POS heuristique (612) | 0,8625 | **0,8625** | 0 jeton changé sur 3 179 | [r035](rapport-r035.md), [s065](rapport-s065.md) |
| F1 syntagmes (612) | 0,7533 | **0,7902** | 183/183 ; placebo 0,7758 | [convention GV](rapport-convention-gv.md) |
| attachement (612) | 236/237 labels | **238/238 labels** (238/239 cibles, 0,9958) | 0 cible perdue | [s065](rapport-s065.md) |
| spans sans label | 2 | **1** (`g017`) | r035 rejoué | [r035](rapport-r035.md) |
| tagger POS API (612) | 0,8625 | **0,9475 (+8,49)** | planchers 0,2145/0,2491/0,1667/0,0833 | [R](rapport-coordination-r.md) |
| restitution v1 | strict 0,1087 | **canonique 46/46**, strict 0,1087 | source brute 1/46 | [v1](rapport-restitution-v1.md) |
| Panini | — | table **14/14**, corpus **418/438**, généalogie **154/154**, sœurs **0,619 vs 0,0445**, §334, CIC **42/42** | contrôles des fiches | [tableau](rapport-tableau-mesures.md) |

**La réserve ne bouge pas.** Le gain F1 est **in-sample** (convention lue dans le gold), le tagger
porte la réserve du **réel 432** (+4,67 pts, IC contenant +5), et `g017` reste une **convention**
non tranchée. La clôture ne les efface pas : elle les **inscrit** dans le bilan.

## 5. Le tag et le dernier commit vert

Le dernier commit vert est **`0e75f101`** (J13.1), qui porte la table des mesures et l'état au
14/11. Les tags sont **annotés** :

```bash
git tag -a chantier-2026-11-14 -m "Chantier 2026-11-14 : 84 portes, 81 vertes, 3 rouges nommées (indice, melange, sessions) ; 28/28 acceptations ; J14.1" 0e75f101
git tag -a semaine-2026-11-14  -m "Semaine 2026-11-14 : tag de J5.2, posé à la clôture J14.1 sur le dernier commit vert 0e75f101" 0e75f101
```

Le contrôle négatif du tag est simple : `git cat-file -t` doit rendre **`tag`** (et non `commit`),
et `git rev-parse chantier-2026-11-14^{}` doit rendre **`0e75f101`**. Un tag léger serait refusé
par ce contrôle. Le tag de semaine `semaine-2026-11-14` répare l'acceptation **J5.2** sans réécrire
l'histoire : il est daté du 14/11, pas du 13/11.

**Pourquoi le tag ne porte pas le commit de clôture.** Le mandat dit « sur le dernier commit
vert ». Le commit de clôture ajoute ce rapport, la note de références et la mise à jour d'état ; il
n'a pas été couvert par la passe de 00 h 30. Le tag est donc posé sur `0e75f101`, et le commit de
clôture **suit** le tag. Un lecteur qui veut le rapport le trouve dans l'historique, pas dans le
tag.

## 6. Les contrôles négatifs de la clôture

| # | contrôle | dispositif | résultat |
|---|---|---|---|
| C1 | la passe n'est pas refaite | lecture du log et du registre par code de sortie | 84 / 81 / 3 ; 3 rouges nommées |
| C2 | les rouges sont les mêmes | comparaison des trois journaux de vérification avec la passe | mêmes causes ; 0 rouge nouvelle |
| C3 | `sessions` est réparée par la règle | `tools/sessions.py --check --strict` + autotest de la porte | **0** ; autotest 6/6 |
| C4 | le tag est annoté | `git cat-file -t` ; `git rev-parse ^{}` | `tag` ; `0e75f101` |
| C5 | le tag de semaine répare J5.2 | `git tag -l 'semaine-2026-11-14'` | posé sur `0e75f101` |
| C6 | l'état accompagne le fait | `tools/verifie_etat_a_jour.py --index` (hook) | `en-cours` stagé avec les faits |
| C7 | la documentation passe | `python3 tools/revue_documentation.py` ; `tools/porte-tableaux.sh` | **0** ; page vivante datée du dernier commit |
| C8 | l'état est court et reprenable | `tools/verifie_en_cours.py` ; `tools/taille_documents.py` | état ≤ 2 000 mots ; budgets T0/T1 respectés |

## 7. Ce qui pourrait rendre ce rapport faux

1. **La passe n'est pas rejouée.** Les **81 vertes** sont celles du 14/11 00 h 30 ; un changement
   de code ou de données après cette heure ne serait pas couvert. Le tag est posé sur `0e75f101`,
   pas sur le commit de clôture.
2. **Deux rouges restent structurelles.** `indice` et `melange` échouent pour des raisons de
   **méthode** (indice extérieur non retrouvé ; état de A qui ne porte pas son code). Les tolérer
   ne les corrige pas : une amélioration de l'instrument peut les faire passer, une régression du
   moteur peut les faire échouer **autrement** — c'est pourquoi la cause est nommée, pas seulement
   le code.
3. **`sessions` est verte par convention.** Le hub est en pause et le heartbeat de `e181ce02` est
   rafraîchi ; une autre session périmée, ou un heartbeat oublié, rendrait la porte rouge sans
   qu'aucun code n'ait changé.
4. **Les durées ne sont pas comparables.** La vérification ciblée a lancé `indice` et `melange`
   **en parallèle** sur la même machine ; leurs durées (913 s, 145 s) ne
   sont pas des temps de référence. Le verdict, lui, est un code de sortie.
5. **J5.2 est réparé après coup.** Le tag `semaine-2026-11-14` est posé le 14/11, pas le 13/11 :
   l'acceptation est satisfaite, l'échec historique reste daté.
6. **Les compteurs bougent.** 732 fiches / 826 JSON après ce rapport ; `en-cours` est la source du
   compte. Une fiche ajoutée après ce commit rend le chiffre faux sans qu'aucun calcul ne l'ait
   signalé.

## 8. Ce qui reste — la prochaine mesure

Le chantier est **clos** ; les chantiers suivants restent ouverts et nommés :

- **B13** — **trancher `g017`** (convention d'adverbe : `g005`/`g017` contre `r264`/`r288`), puis
  **T132/T133** et le **gold 200+** ;
- **N2** — la **porte propre** (manque 0,2856 val / 0,3566 test) ; **N4** ;
- **R0.7** — le **split réel** du tagger, tenu à l'écart ; la route API derrière drapeau ;
- **S** — les 11 verdicts et le pointeur ; **J3.2** — la signature V14 des 21 langues ;
- **A** — A6.2 et A8.3b2.

La **prochaine mesure** désignée est **B13 — trancher `g017`**, parce que c'est le seul span sans
label et que la convention contredit le gold sur deux paires.

## 9. Fichiers

- **Nouveaux** : `reports/rapport-cloture-chantier.md` (ce rapport),
  `reports/rapport-cloture-chantier.json` ; journaux `work/portes/verif-cloture/`.
- **Mis à jour** : `docs/pilotage/references-non-regression.md`, `docs/pilotage/en-cours.md`,
  `docs/pilotage/roadmap.md`, `reports/README.md`, `reports/INDEX.md`,
  `reports/rapport-tableau-mesures.md`, `reports/tableau-mesures.json`,
  `journal/2026-11-14/mesures.md`, `journal/sessions/e181ce02-…/plan.md`,
  `journal/sessions/1e7ef596-…/plan.md`.
- **Lus, non modifiés** : `work/portes/passe-1311-23h15.log` et son dossier,
  `reports/rapport-bilan-chantier.md`, `reports/rapport-semaine.md`, les fiches et JSON cités.
- **Tags** : `chantier-2026-11-14` et `semaine-2026-11-14`, tous deux sur `0e75f101`.

## 10. Verdict

**J14.1 est fait.** La passe de référence (**84 portes, 81 vertes, 3 rouges nommées**) n'a pas été
refaite ; les trois rouges ont été **revérifiées** : `sessions` est **verte** après la mise en
pause du hub et le rafraîchissement du heartbeat, `indice` et `melange` restent **rouges
structurelles** avec leurs causes. Le tag annoté **`chantier-2026-11-14`** est posé sur le dernier
commit vert `0e75f101`, avec le tag de semaine **`semaine-2026-11-14`** qui répare J5.2. Le
chantier est **mesuré, écrit, committé et marqué** ; il est **clos**.
