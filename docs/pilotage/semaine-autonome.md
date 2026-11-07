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
| 2 spans inatteignables (`r035` relative zéro, `g017` arbitrage d'adverbe) | attachement **236/237 (0,9916)** | [`rapport-gn-pronom-sujet.md`](../../reports/rapport-gn-pronom-sujet.md) |
| la convention des GV (322 FP / 180 FN) | F1 **0,7535** (linéaire 0,8104) | [`rapport-gn-pronom-sujet.md`](../../reports/rapport-gn-pronom-sujet.md) |
| `meta.alternative` hors schéma v1 | le schéma publié | [`tools/schemas/`](../../tools/schemas/) |
| la restitution (annotation → texte) | miroir **0,2276** | [`../methode/miroir.md`](../methode/miroir.md) |

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
| **J1 · 07/11** | matin | le produit : les **2 spans**, la **convention des GV** | attachement et F1, fiche v13 |
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
