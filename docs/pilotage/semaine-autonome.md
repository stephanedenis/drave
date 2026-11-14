# Le chantier autonome — une semaine (7 → 14 novembre 2026)

> **Ce que ce document est.** Le **plan du chantier d'une semaine** : tous les travaux ouverts du
> dépôt et l'**intégration avec l'écosystème Panini**. Il dit **quoi**, **dans quel ordre**, **avec
> quels sous-agents**, **comment on mesure**, et **ce qui peut faire échouer**. L'état courant est
> dans [`en-cours.md`](en-cours.md) ; la théorie de la généalogie dans
> [`../theorie/genealogie-des-langues.md`](../theorie/genealogie-des-langues.md) ; la méthode
> Panini/Nipada dans [`../methode/panini-nipada.md`](../methode/panini-nipada.md).
> *À relire chaque matin du chantier.*

## 1. L'objet

**Une semaine, un système utilisable, une intégration mesurée.** Le produit `drave` (CLI, contrat,
porte) est la **priorité** ; l'intégration avec Panini/Nipada est le **second axe** ; les chantiers
N2/S/R/A sont **coordonnés** (jamais écrits par cette session). Chaque vague produit un
**résultat mesuré**, une **fiche** et son **JSON**, la mise à jour de l'**état** et un **commit
vérifié** — jamais une intention.

## 2. L'inventaire — ce qui est ouvert

### 2.1 Drave — le produit (priorité)

| reste | mesure | où |
|---|---|---|
| 1 span (`g017` arbitrage d'adverbe) ; `r035` relative zéro **réglé** | attachement exact **237/238 (0,9958)** | [`rapport-r035.md`](../../reports/rapport-r035.md) |
| la convention des GV (322 FP / 180 FN) — **réglée** (sujet hors du GV + adverbe final) | F1 **0,7902** (linéaire 0,8144) ; attachement **237/238** | [`rapport-convention-gv.md`](../../reports/rapport-convention-gv.md) |
| `meta.alternative` / `meta.partition` — **publiés en v2** (v1 lue) | 26 cas, 0 échec | [`rapport-schema-v2.md`](../../reports/rapport-schema-v2.md) |
| la restitution (annotation → texte) — **v0 faite** | surface **46/46**, miroir strict **0,1087** (50 textes libres) | [`rapport-restitution-v0.md`](../../reports/rapport-restitution-v0.md) |

### 2.2 Drave — les chantiers voisins (coordination)

| chantier | état | ce qui reste | territoire |
|---|---|---|---|
| **N2** | porte propre **2,7856** à 1 024 (manque 0,29) | `porte-n2.sh` (deux seuils), le mètre RoPE à corriger | N2 (lecture seule) |
| **S** | `/paragraphes` fini 19/19 ; banque 150/207 | **11 verdicts non committés**, la page `/` sert la v7, la rétro-traduction | S (lecture seule) |
| **R** | R0.7 heuristique ; R1.2-1024 mesuré | le tagger sur 612 (**clé absente**), R1.1, R2.1 | R (lecture seule) |
| **A** | A6.2 **libre** (MoE local 18 Go), A8.3a 3/19 | A6.2 routage, A8.3b2 | A (lecture seule) |
| **B10.3** | bloqué (encodeur) | — | bloqué |

### 2.3 Panini — l'écosystème (intégration)

- **14 dépôts**, inventoriés le 07/11 ([`rapport-inventaire-panini.md`](../../reports/rapport-inventaire-panini.md)) :
  **Panini** (hôte, non propre, `research` pinné 6f8b67b alors que le checkout est e10d695),
  **Panini-Research** (NIPADA, 182 194 l. Python, 546 k fichiers non suivis),
  **Panini-FS** (retard de 140 commits), 7 échafaudages, et **ExecutionOrchestrator** (seul
  squelette exécutable).
- **7 axes** ; le noyau J4 (ℝ, CIC-lite) est **actif** ; NIPADA (produit) est **bloqué** (DTP arrêté
  depuis le 3 juillet, 54 tests cassés) ; **l'axe 6 « Drave » est déclaré mais non instrumenté**.
- Les **14 atomes V14** (source canonique `research/src/nipada/core/hardware_mapping.py` ;
  ∃ ÊTRE, ∆ DIFFÉRENCE, ∼ RAPPORT, ↗ ORIENTATION, ⊙ SUJET, ⧖ TEMPS, ◇ MODALITÉ, № NOMBRE,
  ⊕ ESPACE, ⊗ OPÉRATION, λ FONCTION, ⊞ STRUCTURE, ≍ SYMÉTRIE, ≡ ÉQUATION) et les **9 dhātus**.
  Utilisables par Drave **en JSON plat, sans dépendance**.
- **La généalogie** : `src/nipada/signing/language_genealogy.py` (29 langues) et l'**UDHR 532
  langues** — la **même source XML** que Drave (456 langues avec glottocodes).
- Leur **avertissement** (à ne jamais oublier) : β **époque +0,138** vs **filiation +0,049**
  (R² 0,30) — la surface capte l'époque ; tout test de style contrôle la date, tout test de famille
  contrôle la surface.

**Les trois intégrations les plus mûres** (inventaire du 07/11) :

| # | intégration | livrable | contrôle négatif | risque |
|---|---|---|---|---|
| 1 | **UDHR + généalogie** (même source XML des deux côtés) | table iso3/famille/branche + échantillon 20 langues | familles différentes = retrieval faible ; sœurs = fort | codes ISO (007/008 vs iso3) |
| 2 | **atomes V14 ↔ niveaux** (44 œuvres × 14 flottants, JSON pur) | table + 20 exemples mesurés | permuter les colonnes doit tuer le prédictif | signature lexicale : contrôler la date |
| 3 | **corpus d'or CIC** (42 verdicts, preuve + sha256) | vérificateur indépendant, 42/42 | altérer un octet doit être rejeté | aucun (le plus vérifiable) |

**Trop immature pour la semaine** : le produit NIPADA, le noyau comme service, les 11 modules,
Panini-FS, l'API REST.

### 2.4 La surface d'intégration

| Panini / NIPADA apporte | Drave apporte | premier livrable commun |
|---|---|---|
| les **14 atomes**, les universaux | nos **niveaux** (POS, syntagmes, pragmatique) et leurs mesures | une **table de correspondance** atomes ↔ niveaux, sur un corpus commun |
| les **corpus** (Gutenberg, UDHR) et leur découpage | le **retrieval** inter-langues (mesures 49) | une mesure de retrieval **à époque contrôlée** |
| la **généalogie** (théorie) | l'**alignement Glottolog** (chiffré) | une fiche de généalogie **avec les deux faces** |
| le **noyau formel** (ce qui est prouvé) | le **moteur d'exécution** (flots, AER) | un **schéma** partagé (JSON) validé des deux côtés |

## 3. La semaine — cinq jours, deux vagues par jour

**Chaque vague** : 2 à 4 sous-agents, un **résultat mesuré**, un **contrôle négatif**, une **fiche**
+ son **JSON**, la mise à jour de l'**état**, un **commit vérifié** par l'agent principal (les
sous-agents ne committent jamais).

| jour | vague | objet | livrable mesuré |
|---|---|---|---|
| **J1 · 07/11** | matin | le produit : le **span `g017`**, la **convention des GV** | attachement et F1, fiche v13 |
| | après-midi | le **schéma v2** (`meta.alternative`, `meta.partition`) et la **restitution v0** | schéma validé, miroir mesuré |
| **J2 · 08/11** | matin | **Panini I** : l'inventaire croisé, la **table atomes ↔ niveaux** | la table, 20 exemples mesurés |
| | après-midi | **Panini I** : le **corpus commun** (format, échantillon) | un corpus partagé + sa fiche |
| **J3 · 09/11** | matin | **Panini II** : le **retrieval à époque contrôlée** | une mesure (double contrôle) |
| | après-midi | **Panini II** : la **généalogie** (Glottolog + leur théorie) | une fiche à deux faces |
| **J4 · 10/11** | matin | la **coordination** N2 (le mètre RoPE), S (les 11 verdicts), R (R1.1) | des fiches de coordination, 0 écriture S/D/N2 |
| | après-midi | la **coordination** A (A6.2), B10.3 (l'encodeur) | un état daté, les décisions |
| **J5 · 11/11** | matin | la **consolidation** : docs, roadmap, la semaine | le rapport de semaine |
| | après-midi | la **passe complète**, le **tag**, la **release** | les portes, un tag annoté |

**Chaque jour** : la passe complète des portes, la revue de documentation, l'état, le journal.

## 4. Les règles du chantier

1. **Le pilote** (l'agent principal) tient seul le dossier : `en-cours`, `roadmap`, `chantiers`,
   `plan-travail`, `journal` et ce document. Les sous-agents rendent des **fiches** et des **JSON**,
   jamais de commit.
2. **S / D / N2 sont en lecture seule** : on lit, on mesure, on propose ; jamais d'écriture. Les
   actions qui les concernent passent par une **fiche de coordination** datée.
3. **Chaque vague** : mesure + **contrôle négatif** + fiche + JSON + état + commit. Sans contrôle
   négatif, ce n'est pas un résultat.
4. **Les portes** : la passe complète chaque jour (`bash tools/toutes-les-portes.sh`) ; les rouges
   tolérées sont **nommées** dans [`references-non-regression.md`](references-non-regression.md) ;
   toute autre est une régression.
5. **L'honnêteté** : un chiffre porte sa **base** (gold vivant 612 / gelé 602), son **commit**, son
   **contrôle**, et **ce qui pourrait le rendre faux**. Les fiches historiques portent
   « instantané historique ».
6. **La file « jamais en attente »** : une ligne bloquée (clé, GPU, corpus, verdict humain) est
   consolidée dans `en-cours` et on prend la **suivante**.

## 5. Les risques, nommés

| risque | effet | parade |
|---|---|---|
| **la clé DeepSeek absente** | le tagger sur 612 et la rétro-traduction sont bloqués | décider : mesure < +2 pts → négatif nommé ; sinon demander la clé |
| **les GPU** (N2, A6.2) | les runs sont lents ou interdits | coordination par fiches ; les runs N2 appartiennent à N2 |
| **la concurrence des sessions** | index.lock, états qui bougent, mesures qui dérivent | commits par chemins explicites, re-mesure avant chaque fiche |
| **les sous-agents** (40-90 min) | les vagues débordent | 2-4 sous-agents, mandats courts, livrables partiels acceptés |
| **le gold** | les 2 spans restants sont des cas isolés | les déclarer, ne pas surapprendre |

## 6. La file (rappel)

Les **29 tâches** de [`rapport-file-taches.md`](../../reports/rapport-file-taches.md) : **8
autonomes** (faites ou en cours), **11 en coordination**, **10 bloquées**. Les tâches autonomes
restantes sont dans le tableau du § 2.1 ; les autres sont des fiches de coordination.

## 7. Ce que la semaine doit avoir produit

- le **produit** : 2 spans tranchés (ou déclarés), le schéma v2, la restitution v0, la porte verte ;
- **l'intégration** : une table atomes ↔ niveaux, un corpus commun, une mesure de retrieval à
  époque contrôlée, une fiche de généalogie à deux faces ;
- **la coordination** : un état daté de N2/S/R/A, les décisions prises et nommées ;
- **la consolidation** : la passe complète, un tag, le rapport de semaine, la roadmap à jour.

## 3 bis. L'état du chantier (12 h 18, 07/11 → 23 h 00, 13/11)

Le superviseur a lancé **10 tâches** (budget 21 600 s consommé). **Six sont « faites »**, trois ont
un **commit livré** mais un verdict « échec » (timeout de l'agent après le commit — l'acceptation
prime désormais), une était bloquée. La reprise du **13/11** a ajouté **quatre coordinations**
(N2, S, R, A) et la consolidation J5.

| tâche | verdict | livrable | commit |
|---|---|---|---|
| J0 (contrôle) | ✅ fait | la liaison superviseur ↔ dsh | — |
| J1.1 `r035` | ✅ fait | exact **237/238**, couverture **0,9958** | `25a6c0ff` |
| J1.2 convention GV | ✅ livré (timeout) | F1 **0,7549 → 0,7902** | `92652984` |
| J1.3 schéma v2 | ✅ fait | `meta.partition`/`meta.alternative`, 26 cas | `9a259953` |
| J1.4 restitution v0 | ✅ fait | 46/46 surfaces exactes | `8eb0cc49` |
| J2.1 atomes ↔ niveaux | ✅ fait | 14/14 lignes | `9c7f71dc` |
| J2.2 + J3.1 corpus/retrieval | ✅ livré (timeout) | 418/438 paires exactes | `c3467170` |
| J3.2 généalogie | ✅ fait | 154/154 paires hors script | `c2e629b3` |
| J4 N2/S/R/A | ✅ fait (13/11) | 4 fiches + 4 JSON ; D1–D8 | `commit J5.1` |
| J5.1 rapport de semaine | ✅ fait (13/11) | [`rapport-semaine.md`](../../reports/rapport-semaine.md) + JSON | `commit J5.1` |
| J5.2 passe, tag, release | ⏳ à faire | — | — |

**Reste** : J5.2 (passe complète, revue de documentation, tag annoté, release), les commits de
S (11 verdicts + pointeur), le rapport A6.2, et la relance de la boucle.

## 8. L'état de chaque jour — bilan du 13/11

> **Les dates réelles diffèrent du plan.** J1–J3 ont été exécutés le **07/11** (le plan les
> plaçait du 07 au 09) ; J4 le **13/11** (plan : 10/11) ; J5.1 le **13/11** (plan : 11/11). Le
> décalage vient de la reprise de la boucle après épuisement du budget, pas d'un changement de
> périmètre. Ce tableau est l'état **constaté**, pas le calendrier prévu. Le détail des chiffres,
> des décisions et des rejets est dans [`rapport-semaine.md`](../../reports/rapport-semaine.md).

| jour | vague | état | livrable mesuré | commit | reste |
|---|---|---|---|---|---|
| **J1** | matin : `r035` + convention GV | ✅ fait | exact **237/238**, couverture **0,9958**, F1 **0,7533 → 0,7902**, POS inchangée | `25a6c0ff`, `92652984` | `g017`, `s065`, objet (75 FP / 51 FN), 5 FP sujet |
| **J1** | après-midi : schéma v2 + restitution v0 | ✅ fait | **26 cas / 0 échec**, **1 836 annotations / 0 échec** ; **46/46** surfaces, miroir **0,1087** | `9a259953`, `8eb0cc49` | invariants sémantiques, v0.1 ponctuation, gold de restitution |
| **J2** | matin : inventaire + table atomes ↔ niveaux | ✅ fait | **14/14 lignes**, 8 niveaux, 33 paires colinéaires, 4 composantes > 1 | `9c7f71dc` (+ `fffbbe5d`) | aucune correspondance mesurée : protocole J2.2 |
| **J2** | après-midi : corpus commun | ✅ fait | **21 textes**, 5 familles, 10 écritures, **418/438** paires exactes (95,4 %), 8/8 contrôles | `c3467170` (avec J3.1) | corpus multi-époques / multi-genres |
| **J3** | matin : retrieval à époque contrôlée | ✅ fait | **B7 4 004 paires**, **UDHR 420**, **Bible 132** ; script **+0,609**, famille **+0,181**, date **−0,034/siècle** (p = 0,19) | `c3467170` | réplication neuronale |
| **J3** | après-midi : généalogie à deux faces | ✅ fait | **154/154** paires hors script au hasard ; **5/21 / 15/21 / 21/21** ; R² **0,256 / 0,230** | `c2e629b3` | signature V14 des 21 langues, matrice 9 dhātus, distance continue, corpus équilibré |
| **J4** | matin : coordination N2 / S / R | ✅ fiches (13/11) | N2 **8,0225 → 2,9726 / 2,7856** ; S **11 verdicts** (7 acceptés / 4 exclus) ; R **0,8625 → 0,9475 (+8,49)** | `commit J5.1` | appliquer N2, committer S + pointeur, route R + split tenu |
| **J4** | après-midi : coordination A | ✅ fiche (13/11) | A6.2 **libre** (MoE 18,56 Go, PPL **37,2013**, porte **54,5202**) ; A8.3b2 libre hors graphe | `commit J5.1` | rapport A6.2, harnais A8.3b2, D1–D8 |
| **J5** | matin : rapport de semaine | ✅ fait (13/11) | [`rapport-semaine.md`](../../reports/rapport-semaine.md) + JSON : chiffres, décisions, rejets, reste | `commit J5.1` | — |
| **J5** | après-midi : passe, tag, release | ⏳ à faire | — | — | `toutes-les-portes.sh`, `revue_documentation.py`, tag annoté |

**Ce que la semaine a produit.** Le **produit** : `r035` tranché (237/238, 0,9958), la convention
des GV (F1 **0,7902**), le schéma v2 (26 cas / 0 échec, v1 lue), la restitution v0 (46/46
surfaces, miroir **0,1087**). Le **tagger** : 0,9475 (+8,49 pts), décision **intégrer**, réserve
sur le réel 432 (+4,67). L'**intégration** : table 14/14, corpus 418/438, retrieval à script
dominant, généalogie à deux faces. La **coordination** : N2 (2,9726/2,7856, `--rope --canal-dir`),
S (11 verdicts, 7/4), R (0,9475, intégrer), A (A6.2 libre, A8.3b2 hors graphe).

**Ce que la semaine n'a pas produit.** Le **deuxième span** (`g017`), la **preuve** de la théorie
des atomes (la table est une hypothèse, V14 couvre 3/21 langues), la **durabilité** des résultats
S (non committés) et N2 (`rope_model.py` dans `work/`), et la **passe complète** : J5.2 doit
lancer les 84 portes, la revue de documentation, le tag et la release. L'autotest **183/183**
n'est pas la passe complète.
