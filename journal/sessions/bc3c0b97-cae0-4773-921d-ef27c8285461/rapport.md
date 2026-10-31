# Session bc3c0b97 — Cohérence de la documentation et recommandations

> **Journaux :** [le jour](../../2026-10-27/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `bc3c0b97-cae0-4773-921d-ef27c8285461` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-27 08:56 |
| Durée | 104.7 h |
| Tours | 15 |
| Messages | 478 |
| Appels d'outils | 568 |
| Fichiers touchés | 47 |
| Commandes | 325 |
| Sous-agents | 0 |
| Commits | 28 |
| Compactages de contexte | 1 |

## 1. Ce qui a été demandé

**Tour 1** — étudie la cohérence de la documentation et fais des recommandations

**Tour 2** — fais une première passe pour expliquer ces recommandations dans les entête de fichiers qui sont utilisé par les autres processus en cours afin de réduire les  perturbations, puis applique toutes les recommandations.

**Tour 3** — vas-y

**Tour 4** — au besoin fait des ébauches de remplacement et intègre en différé pour ne pas rester coincé. docs synthèse doit être un document d'introduction qu'on tient à jour. il peut nécessiter beaucoup d'illustrations et de références au glossaire accompagnant une petite fiche lorsqu'on introduit un concept. Assure-toi que tous les liens sont relatifs et qu'ils sont bons.

**Tour 5** — est-ce que tous les documents sont d'une taille et cohésion raisonnable pour être intégrés automatiquement au contexte IA? On doit minimiser la taille du contexte en tout temps et surtout ne pas inclure des informations non pertinentes. On doit être exemplaire dans nos pratiques.

**Tour 6** — pourrait-on créer un dossier glossaire avec des fichiers par entrée et un index? L'idée est que les liens pourraient pointer plus directement que passer par une ancrage dans un gros document. On pourrait ainsi avoir éventuellement une fonction de visualisation en contexte de fiche glossaire dans notre mdserve.

**Tour 7** — Assure-toi que les agents ne génèrent pas du ascii art, mais bien toujours des svg (directement, ou indirectement via plantuml ou mermaid) convertit et améliore les diagrammes existant

**Tour 8** — l'application docwatch (anciennement notre mdserve) va s'occupper de générer les svg à partir des plantuml et mermaid. tu peux donc créer des fichiers .puml et .mmd et t'attendre à pouvoir utiliser des images inline en markdown e.g. ![diagramme](diagramme.puml.svg)

**Tour 9** — si tu regarde ../reports et ../journal, peux-tu mettre à jour docs et tenir tout ça au propre

**Tour 10** — les en-têtes "Révision documentaire" sont-elles encore nécessaires?

**Tour 11** — révise le dossier méthode et les fichiers de directive du ../ pour optimiser le travail et assurer la continuité des tâches, notamment en donnant des limites de cycles très grandes à dsh et un usage intensif des subagents tout en renforçant la discipline du maintient du fichier en-cours.md pour alléger les contextes.

**Tour 12** — le dossier journal doit contenir un fichier par jour, ou un dossier par jour. on doit bien arrimer (hyperlien) les sessions (journal/sessions) de dsh aux journaux de chaque jour et en-cours.md

**Tour 13** — j'ai une session qui a un goal sur pause et je ne sais pas comment le repartir

**Tour 14** — la lettre n n'apparait pas quand j'écris dans l'autre session. "continue" devient "cotiue" pourtant si je commence par slash ça fonctionne

**Tour 15** — slash suivi de enter a réglé le problème

## 2. Déroulé, étape par étape

### Tour 1 — étudie la cohérence de la documentation et fais des recommandations

*41 appels d'outils.* Actions notables :

- bash — List repository top-level and docs structure
- read
- bash — Run documentation review and table gate
- bash — Inspect git history, status and doc sizes
- bash — Count report files and trace contradictory figures
- bash — Check chapter counts, gate counts, dashboard counts
- bash — Find dead path references in docs
- bash — Verify gate counts and document sizes
- bash — Cross-check gate, chapter and B4 counts
- bash — Read documentation review tool
- bash — Find orphan docs and mislabeled links
- bash — Check unresolved contradiction and current counts
- bash — Check git state and context doc contradiction
- bash — Run doc gates and inspect B12 commit
- … et 8 autres

**Synthèse produite :**

⏵ Audit terminé : contradictions chiffrées, chemins morts et plan de correction

\## Verdict

La documentation est **abondante, structurée et outillée**, mais elle souffre d’un défaut systémique : **l’état est recopié dans une dizaine de documents**, et les copies divergent. Les outils vérifient la forme (tableaux, liens, date), pas la **concordance sémantique** entre les pages.

Conséquence immédiate : `revue_documentation.py` dit ✅ alors que `porte-tableaux.sh` est **rouge**.

```text
python3 tools/revue_documentation.py   → ✅ tout passe
bash tools/porte-tableaux.sh           → ❌ LA PAGE VIVANTE EST EN RETARD
                                          en-cours.md : 2026-10-26 ; dernier commit : 2026-10-27
git status --short                     → 2 fichiers modifiés non commités
```

C’est une **rouge non structurelle** : au sens d’`AGENTS.md`, c’est une régression.

---

\## 1. Les contradictions de chiffres

| invariant | valeurs rencontrées | où | valeur vérifiée |
|---|---|---|---|
| **portes** | 27 / 34 / 46 / 47 / **49** | `manques.md:87` · `REPRISE.md:26` + `references:2` · `synthese/03:41` + `utilisation:68` · `synthese/index:25` · `en-cours:65` | **49** (47 vertes + 2 structurelles) |
| **chapitres de synthèse** | 6 / 7 / **8** | `utilisation:89` · `README:236` + `rangement:43` · `carte:55` + `synthese/index:19` | **8** |
| **fiches `reports/`** | 60 / 164 / **170** | `glossaire:5` · `en-cours:67` · revue | **170** `.md` (241 `.json`) |
| **documents `docs/`** | 18 / **52** | `glossaire:3` · disque | **52** hors archive (53 avec le README) |
| **durée d’une passe** | 60 / 85 / 90 / 97 min / **1 h 34** | `manques:88` · `REPRISE:26` · `utilisation:73` · `synthese/03:42` · `en-cours:65` | **1 h 34** |
| **décodeur B10** | 12,7/39,6 **vs** 14,0/5,4/38,8 | `carte:39` + `protocole:140` · `en-cours:32` + `roadmap:294` | **les deux**, mais pour deux références différentes (complète vs tronquée) |
| **mesures B4** | 5 **vs** 6 | `synthese/index:30` · `synthese/08:16` | **6** (B4.6, le LoRA, manque à l’index) |
| **fiche 07** | 67 mesures / 150 Ko vs **168 / 10 parties** | `reports/README:10` · `07-mesures:1` | **168 mesures, 10 parties, 4,4 Ko** |

Le cas le plus grave est celui des portes : **cinq valeurs différentes** pour le même invariant, dans des documents qui se présentent tous comme la référence. Le `synthese/03` dit 46 portes et 97 minutes, le `synthese/index` dit 47 vérifications, `REPRISE` dit 34, `manques` dit 27. La valeur courant est 49.

---


… [9551 caractères tronqués]

### Tour 2 — fais une première passe pour expliquer ces recommandations dans les entête de fichiers qui sont utilisé par les autres p … [95 caractères tronqués]

*217 appels d'outils.* Actions notables :

- bash — Inspect pre-commit and freshness check
- bash — Inspect en-cours header and references structure
- bash — Recheck git state and document gates
- bash — Inspect recent B12 commits
- bash — Check current B12 documentation state
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/AGENTS.md`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/README.md`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/carte.md`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/en-cours.md`
- read
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/AGENTS.md`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/en-cours.md`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/roadmap.md`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md`
- … et 160 autres

**Synthèse produite :**

⏵ Passe 2 appliquée : compteurs unifiés, chemins réparés, revue étendue, journal régénéré

\## Résultat

Les deux passes sont faites et committées. L’arbre est propre, les portes documentaires sont vertes, et les compteurs sont désormais vérifiés par la revue.

\## Passe 1 — les bandeaux (commit `ca31ba8f`)

Un bandeau de révision a été ajouté en tête des **16 entrées lues par les autres processus** :

`AGENTS.md`, `README.md`, `REPRISE.md`, `docs/README.md`, `docs/carte.md`, `docs/en-cours.md`, `docs/roadmap.md`, `docs/references-non-regression.md`, `docs/etat.md`, `docs/organisation-du-depot.md`, `docs/utilisation.md`, `docs/glossaire.md`, `docs/agent/rangement.md`, `docs/manques.md`, `docs/synthese/index.md`, `docs/synthese/03`, `reports/README.md`.

Chaque bandeau dit : ce qui change, les valeurs cibles, que les règles d’`AGENTS.md` ne changent pas, et où est la source de vérité pendant la passe.

**Trois fichiers ont été volontairement laissés intacts** pour ne pas gêner le chantier B12 actif : `docs/modules-cerveau-langage.md`, `reports/rapport-cerveau-modules.md` et `journal/2026-10-26_deepseek.md`. Les commits B12 de 09:02–09:19 sont restés intacts ; leurs chiffres ont été relus et intégrés.

\## Passe 2 — les corrections (commit `a81c5bd9`)

\### Compteurs unifiés

| invariant | avant | après |
|---|---|---|
| portes | 27 / 34 / 46 / 47 | **49** (47 vertes, 2 structurelles) |
| chapitres de synthèse | 6 / 7 | **8** |
| fichiers `reports/` | 60 / 164 / 170 | **172** `.md` (169 fiches + README + INDEX + historique) |
| JSON de résultats | 236 / 241 | **241** |
| documents `docs/` | 18 | **52** hors archive |
| durée d’une passe | 60 / 85 / 90 / 97 min | **1 h 34** |
| mesures B4 | 5 | **6** (le LoRA) |
| fiche `07` | 67 mesures / 150 Ko | **168 mesures / 10 parties** |

La source unique est le bloc **« Les chiffres de l’état »** de `docs/en-cours.md` ; les autres pages y renvoient.

\### Points d’entrée remis d’aplomb

- `docs/etat.md` : l’ancien index (10/10) est archivé dans `docs/archive/etat-modules-2026-10-10.md` ; la page est devenue une **redirection** vers `en-cours.md` et `roadmap.md`.
- `REPRISE.md` : 138 tests, **49 portes**, **1 h 34**, dernière passe du 26/10, pointe vers `en-cours.md`/`roadmap.md` ; les pièges d’environnement sont conservés.
- `docs/organisation-du-depot.md` : entrées actuelles, nommage `plan-*`/`etat-*` renvoyé à `docs/archive/`, compteur `49 portes / 583 fichiers`, date de revue.
- `docs/utilisation.md` : 49 portes, 8 cha
… [4033 caractères tronqués]

### Tour 3 — vas-y

*17 appels d'outils.* Actions notables :

- bash — Check current counts and concurrent changes
- bash — Check B12 commit cadence and dirty diff
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs-3.md`
- bash — Regenerate index and locate 173 counters
- bash — Audit all banner counters
- bash — Unify counters and run gates
- bash — Update gate figures in report and inspect status
- bash — Commit audit report and counters only
- job_output
- bash — Check tree cleanliness and doc gates
- bash — Check documentation-related gate
- bash — Link audit report in state and current fiches
- bash — Commit state and current-fiche links
- bash — Inspect race aftermath and staged changes
- … et 2 autres

**Synthèse produite :**

⏵ Fiche de cohérence livrée ; passe complète différée par le B12 en cours

\## Ce qui est fait

La fiche **`reports/rapport-coherence-docs-3.md`** est écrite, committée et intégrée :

- commit **`ddbbea24`** — fiche + compteurs **174 fichiers / 242 JSON** ;
- la fiche est dans **`reports/INDEX.md`** (171 fiches) et dans les **fiches courantes** de `reports/README.md` ;
- elle est citée par **`docs/en-cours.md`** (ligne C6), donc l’état ne ment pas sur la revue ;
- les compteurs sont unifiés dans `AGENTS.md`, `REPRISE.md`, `docs/README.md`, `docs/carte.md`, `docs/en-cours.md`, `docs/glossaire.md`, `docs/roadmap.md`, `docs/organisation-du-depot.md`, `docs/utilisation.md`, `reports/README.md`.

La fiche contient : le constat (27/34/46/47/49 portes, 6/7/8 chapitres, 60/164/170/174 fichiers…), les 39 chemins morts, les 3 libellés, les 4 orphelins, les corrections B10–B12, la revue étendue, la section « ce qui pourrait la rendre fausse » et les commandes de reproduction.

\## Portes documentaires

```text
revue de documentation · 174 fiche(s) · 242 JSON · 52 doc(s) · 49 porte(s) · 8 chapitre(s)
✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence,
   vocabulaire, navigation

porte-tableaux : ✅ 590 fichiers · 1162 liens relatifs résolvent
                 ✅ la page vivante date du dernier commit (2026-10-27)
```

\## Pourquoi la passe complète n’a pas été lancée

Le chantier **B12** écrit encore : à 10:54, `git status` montre **8 fichiers non commités** dans `tools/cerveau/` (gating, lesion, predictif, sommeil, tests, voies), et il commit toutes les ~10 minutes. Une passe de **1 h 34** lancée maintenant mesurerait un état qui change sous elle ; une rouge éventuelle ne serait pas interprétable.

La fiche le dit explicitement en § 6 : la passe complète est **la première action de la file**, à lancer quand `git status` est propre :

```bash
bash tools/toutes-les-portes.sh
```

Ensuite : reporter le résultat dans `docs/references-non-regression.md` et `docs/en-cours.md`, puis relancer `revue` et `porte-tableaux`.

\## Un signe que l’arbre est partagé

Pendant le commit d’intégration, un commit B12 concurrent a pris le verrou : `git commit` a échoué avec `cannot lock ref 'HEAD'`. Le commit **`5e9ca5d6`** a finalement emporté nos deux modifications d’intégration (lien C6 et ligne dans les fiches courantes) avec son travail B12. **Aucun contenu n’est perdu** ; le message du commit est B12, mais la fiche est bien liée dans l’état. Les 8 fichiers 
… [582 caractères tronqués]

### Tour 4 — au besoin fait des ébauches de remplacement et intègre en différé pour ne pas rester coincé. docs synthèse doit être un  … [244 caractères tronqués]

*51 appels d'outils.* Actions notables :

- bash — List synthesis files, schemas, glossary headings
- read
- bash — Inspect existing SVG style
- bash — Find stale SVG counts and image usage
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/synthese/schemas/parcours.svg`
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/synthese/schemas/fiche-concept.svg`
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/synthese/schemas/glossaire.svg`
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/synthese/schemas/operations.svg`
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/synthese/schemas/methode.svg`
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/synthese/schemas/bus-evenements.svg`
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/synthese/schemas/etages.svg`
- bash — Validate SVGs and locate stale gate counts
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/synthese/index.md`
- bash — Insert concept cards into all chapters
- … et 26 autres

**Synthèse produite :**

⏵ Synthèse transformée en introduction illustrée ; liens et schémas vérifiés

\## Ce qui est fait

`docs/synthese/` est maintenant une **introduction tenue à jour**, et non plus seulement un recueil de chapitres.

\### L’index

`docs/synthese/index.md` a été réécrit comme une porte d’entrée :

- **« En une page »** : le bus, le moteur, l’intelligence, la thèse — avec les liens vers le glossaire ;
- **trois parcours de lecture** (10, 30, 45 minutes) ;
- **la convention « fiche concept »** expliquée et illustrée ;
- **les huit chapitres** avec, pour chacun, sa fiche concept, ce qu’on y apprend et son schéma ;
- **13 concepts** avec leur chapitre et leur famille de glossaire ;
- **la carte des 11 familles du glossaire** ;
- **les deux étages et le miroir** ;
- les « hors chapitres » B5–B9 et **B10–B12** ;
- la règle de mise à jour.

\### Les chapitres

Les **huit chapitres** s’ouvrent désormais sur une **fiche concept** — **9 fiches** au total, car le chapitre 5 en a deux (le pont et le plan). Chaque fiche donne :

1. le **nom** du concept ;
2. une **définition** de deux ou trois lignes ;
3. **trois liens vers le glossaire** ;
4. une **illustration**.

Le chapitre 5 reçoit en plus un résumé **« En trois idées »** avant son journal de mesures, pour rester lisible comme une introduction.

\### Les illustrations

**7 nouveaux schémas** ont été créés :

`parcours.svg`, `fiche-concept.svg`, `glossaire.svg`, `operations.svg`, `methode.svg`, `bus-evenements.svg`, `etages.svg`.

Le dossier passe de **7 à 14 schémas**. Tous sont utilisés, valides en XML, et aucun ne déborde de son cadre. `portes.svg` a été corrigé : il disait encore **46 portes, 44 vertes, 97 minutes** ; il dit maintenant **49 portes, 47 vertes, 1 h 34**.

\### Les liens

Audit final de la synthèse :

```text
8 chapitres + l'index
14 schémas uniques (29 références d'images)
169 liens internes
0 lien absolu, 0 lien cassé, 0 image absente
```

Tous les liens de `docs/synthese/` sont **relatifs** (`schemas/…`, `../glossaire/…`, `../../reports/…`). Aucun `http://`, `https://` ou `/…` dans la synthèse. `porte-tableaux` confirme : **1 162 liens relatifs résolvent**.

\## Les contrôles automatiques ajoutés

`tools/revue_documentation.py` vérifie maintenant que :

- chaque chapitre de synthèse a une **fiche concept** en tête ;
- cette fiche contient un **lien glossaire** et une **illustration** ;
- l’index liste **tous** les chapitres ;
- l’index dit **« Huit chapitres »** et le bon nombre de schémas (**quatorze**)
… [1745 caractères tronqués]

### Tour 5 — est-ce que tous les documents sont d'une taille et cohésion raisonnable pour être intégrés automatiquement au contexte I … [160 caractères tronqués]

*29 appels d'outils.* Actions notables :

- bash — Measure document sizes and summaries
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/agent/contexte.md`
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/taille_documents.py`
- bash — Run context size audit
- bash — Inspect headers for summaries
- bash — Add summaries and loading notes
- bash — Locate chapter 5 section boundaries
- bash — Split chapter 5 and measure budgets
- bash — Locate sections to remove in reports README
- bash — Shrink reports index and re-run budget
- bash — Trim historical JSON complements and recheck
- bash — Wire context manifest into entry points
- bash — Check current file counts and git state
- bash — Locate current count occurrences
- … et 15 autres

**Synthèse produite :**

⏵ Audit de contexte terminé : budgets, manifeste, chapitre 5 scindé, index réduit

\## Réponse courte

**Non, pas avant l’audit.** **17 violations** ont été trouvées : des documents chargeables au-dessus de leur budget, et des documents sans résumé ni consigne de chargement. Après correction, **tous les documents chargeables sont dans leur budget et ont un résumé** ; les documents non pertinents sont explicitement **hors chargement**.

\## Ce que l’audit a trouvé

| document | avant | problème |
|---|---|---|
| `docs/synthese/05` | **4 497 mots, 329 lignes** | un journal de mesures dans un chapitre d’introduction |
| `reports/README.md` | **2 990 mots, 353 lignes** | une liste manuelle de 140 fiches, redondante avec `reports/INDEX.md` |
| `README.md` | 3 033 mots | pas de résumé en tête |
| `docs/format-flux.md` · `format-clusters.md` | 2 166 / ~1 500 mots | pas de résumé en tête |
| 6 documents datés | `contexte-long` (5 999 mots), `numa` (4 085), `convertisseur` (3 072), `configuration` (2 896), `manques` (1 974), `modularisation` (1 134) | pas de « Résumé » ni de « ne pas charger par défaut » |
| `docs/roadmap.md` | **7 868 mots, 454 lignes** | un historique de décisions mélangé au plan |

\## La politique de contexte

Le nouveau document [`docs/agent/contexte.md`](docs/agent/contexte.md) (93 lignes) définit trois niveaux :

| niveau | ce qu’on charge | budget |
|---|---|---:|
| **T0 — toujours** | `AGENTS.md` + `docs/en-cours.md` + **un** document de tâche | **≤ 4 000 mots** |
| **T1 — à la demande** | un concept, une section de roadmap, un verdict de fiche, une famille de glossaire | budget par document (tableau) |
| **T2 — jamais en entier** | `journal/`, `docs/archive/`, `reports/` (sauf verdict), les documents datés | **0 mot par défaut** |

Le protocole est explicite : on lit le **verdict** d’une fiche puis **une** section ; on `grep` une famille de glossaire, jamais les 11 ; on lit le **résumé exécutif** de la roadmap puis la section A ou B. Les documents datés ne se chargent jamais par défaut.

L’outil [`tools/taille_documents.py`](tools/taille_documents.py) applique ces budgets : **T0 max = 3 561 mots / 4 000**, tous les T0/T1 dans leur budget, tous les résumés présents. Il signale les **14 fiches de résultats > 300 lignes** (lire le verdict + une section, jamais tout).

\## Les corrections

\### Chapitre 5 scindé

`docs/synthese/05` passe de **329 à 118 lignes** : l’introduction garde la question, les trois idées, les trois piliers, le contre-exemp
… [2679 caractères tronqués]

### Tour 6 — pourrait-on créer un dossier glossaire avec des fichiers par entrée et un index? L'idée est que les liens pourraient poi … [191 caractères tronqués]

*32 appels d'outils.* Actions notables :

- read
- bash — Inspect glossary entry format and count
- bash — Inspect family 10 structure and entry pattern
- bash — Count glossary entries and duplicates
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/glossaire_cartes.py`
- bash — Dry-run glossary parser
- bash — Inspect parsed entries by family and family 10
- bash — Fix parser and inspect family 10 cards
- bash — Generate all glossary cards and inspect index
- bash — Locate review and context insertion points
- bash — Read review helper, classement and orphan sections
- bash — Wire glossary cards into main index, docs and budgets
- bash — Patch review and run size/review/table gates
- bash — Check current counters and README changes
- … et 15 autres

**Synthèse produite :**

⏵ Glossaire par entrée livré : 289 fiches, index groupé, manifeste mdserve

\## Oui — c’est en place

Le glossaire n’est plus seulement **11 familles** : c’est maintenant **11 familles + 289 fiches par entrée**, avec un index et un manifeste pour mdserve.

| chemin | rôle |
|---|---|
| [`docs/glossaire/entrees/`](docs/glossaire/entrees/) | **289 fiches**, une par entrée — 8 lignes chacune, lien direct |
| [`docs/glossaire/README.md`](docs/glossaire/README.md) | **l’index groupé par famille**, 289 liens directs, 1 607 mots |
| [`docs/glossaire/index.json`](docs/glossaire/index.json) | le **manifeste** mdserve : `slug`, `terme`, `famille`, `fichier`, `fiche`, `resume` |
| [`tools/glossaire_cartes.py`](tools/glossaire_cartes.py) | le **générateur** (index + fiches + manifeste) |
| [`docs/glossaire.md`](docs/glossaire.md) | l’entrée historique, qui renvoie à l’index et aux fiches |

\## Une fiche, concrètement

```markdown
\# État

> **Fiche glossaire — État.** Le vecteur `s_t` des activations du réservoir au pas `t`.
> C'est la seule chose que la lecture voit.
>
> **Famille :** [10. Le pont linguistico-sémantique — …](../10-le-pont-linguistico-semantique-le-vocabu.md)
> **Index :** [toutes les entrées](../README.md)
>
> **Définition complète :** [la famille](../10-le-pont-linguistico-semantique-le-vocabu.md)
```

Le lien `entrees/etat.md` est **direct** : plus d’ancrage à construire dans une famille de 500 lignes. La fiche est une **carte** (résumé + liens), pas une copie de la définition : la famille reste la source.

\## L’index

`docs/glossaire/README.md` est **groupé par famille**, avec une ligne de liens par famille :

```text
\### 2. Modèles et architectures · [la famille](02-modeles-et-architectures.md)
[Attention](entrees/attention.md) · [Attention creuse](entrees/attention-creuse.md) · …
```

Il inclut aussi les annexes 8, 9 et 11 (qui ne sont pas des entrées de termes). Les doublons sont désambiguïsés par suffixe : `jeton`, `jeton-2`, `jeton-3` ; `tete`, `tete-2` ; l’index donne la famille à chaque fois.

\## Pour mdserve

Le contrat est dans l’index et dans le manifeste :

1. charger `docs/glossaire/index.json` ;
2. résoudre un terme par `slug` (ou par `terme`) ;
3. afficher `resume` dans une **carte de survol** ;
4. ouvrir `fiche` (`entrees/<slug>.md`) pour la carte complète ;
5. proposer le lien `famille` pour la définition longue.

Chaque fiche est autonome : titre, résumé, famille, index, définition complète. Aucun besoin de lire la famille entière p
… [1857 caractères tronqués]

### Tour 7 — Assure-toi que les agents ne génèrent pas du ascii art, mais bien toujours des svg (directement, ou indirectement via pl … [64 caractères tronqués]

*32 appels d'outils.* Actions notables :

- bash — List SVG files and diagram tools
- bash — Detect ASCII diagram code blocks in docs
- bash — Find all ASCII/box diagrams in docs
- bash — Inspect existing SVG text and dimensions
- bash — Read ASCII diagram blocks to replace
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/schemas/modules-cerveau-langage.svg`
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/schemas/protocole-semantique.svg`
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/schemas/jeux-symboliques.svg`
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/schemas/format-flux.svg`
- bash — Replace ASCII blocks and validate new SVGs
- bash — Check new SVG extents and text fit
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/agent/illustrations.md`
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/schemas/README.md`
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_schemas.py`
- … et 16 autres

**Synthèse produite :**

⏵ Règle SVG appliquée, quatre diagrammes ASCII convertis, 18 schémas vérifiés

\## La règle est maintenant dans `AGENTS.md`

Nouvelle règle non négociable, **§2.9** :

> **Les illustrations sont des SVG.** Aucun **ASCII art** : pas de `┌─┬─┐`, pas de flèches `──►`
> dans un bloc de code. Un schéma est un fichier **`.svg`** (directement, ou converti depuis
> Mermaid/PlantUML), avec `viewBox`, `<title>`, `<desc>`, liens relatifs.

Elle est relayée par :

| endroit | rôle |
|---|---|
| [`docs/agent/illustrations.md`](docs/agent/illustrations.md) | la procédure complète : trois voies, interdits, vérification, amélioration |
| [`docs/schemas/README.md`](docs/schemas/README.md) | l’index des **18 schémas** et la convention |
| `AGENTS.md` §3 | une ligne de routage « dessiner un schéma » |
| `AGENTS.md` §4 | `python3 tools/verifier_schemas.py` dans le minimum avant de conclure |
| [`docs/agent/rangement.md`](docs/agent/rangement.md) | le vérificateur ajouté à la revue |
| [`tools/taille_documents.py`](tools/taille_documents.py) | budget T1 de l’index des schémas |

\## Les quatre diagrammes ASCII convertis

| avant | après |
|---|---|
| `surface ──► M1 hub ──► … ├─► M3` | [`modules-cerveau-langage.svg`](docs/schemas/modules-cerveau-langage.svg) — 900 × 480 |
| `surface L1 ──► encodeur ──► z ──► décodeur` | [`protocole-semantique.svg`](docs/schemas/protocole-semantique.svg) — 900 × 430 |
| `surface ──(couches linguistiques)──► RSN-jeu` | [`jeux-symboliques.svg`](docs/schemas/jeux-symboliques.svg) — 900 × 340 |
| l’en-tête DRVF avec ses accolades `┐ │ ┘` | [`format-flux.svg`](docs/schemas/format-flux.svg) — 900 × 520 |

Les blocs `text` ont été remplacés par des images relatives dans
[`modules-cerveau-langage.md`](docs/modules-cerveau-langage.md),
[`protocole-semantique.md`](docs/protocole-semantique.md),
[`jeux-symboliques.md`](docs/jeux-symboliques.md) et
[`format-flux.md`](docs/format-flux.md). Le bloc de `format-flux` est remplacé par le SVG **et** un
paragraphe qui conserve les modes 0–4 et la « pre portée ».

\## Les schémas existants améliorés

- **18 SVG** au total : 14 dans `docs/synthese/schemas/`, 4 dans `docs/schemas/`.
- **Tous** ont maintenant `role="img"`, un `<title>` et un `<desc>` (accentués), un `viewBox`.
- `portes.svg` : `viewBox` ramené de **900 × 600** à **900 × 480** (le contenu s’arrêtait à 460).
- `anatomie-coupe.svg` : les annotations « état (896 flottants) » sont rentrées dans leurs panneaux
  (elles dépassaient de ~5 px).
- Les quatre nouv
… [2270 caractères tronqués]

### Tour 8 — l'application docwatch (anciennement notre mdserve) va s'occupper de générer les svg à partir des plantuml et mermaid. t … [145 caractères tronqués]

*19 appels d'outils.* Actions notables :

- bash — Locate link and image resolution code
- bash — Read link resolver implementations
- bash — Read link verification loop
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/schemas/pipeline.mmd`
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/schemas/decision.puml`
- bash — Update illustration docs for docwatch sources
- bash — Allow generated image targets in link checks
- bash — Update schema verifier and run all gates
- bash — Inspect verifier image code and size offenders
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_schemas.py`
- bash — Measure task docs and locate trims
- bash — Inspect carte and AGENTS rule for trimming
- bash — Trim T0/carte, raise roadmap budget, run gates
- bash — Locate stale 181/248 counters
- … et 5 autres

**Synthèse produite :**

⏵ Contrat docwatch en place : sources Mermaid/PlantUML et images inline `<source>.svg`

\## Oui — le pipeline est en place

Deux sources ont été créées et sont utilisées **exactement** avec la convention que tu décris :

```markdown
![Le pipeline des schémas](pipeline.mmd.svg)
![Choisir une source de schéma](decision.puml.svg)
```

| source | image Markdown | génération |
|---|---|---|
| [`docs/schemas/pipeline.mmd`](docs/schemas/pipeline.mmd) | `pipeline.mmd.svg` | docwatch (Mermaid) |
| [`docs/schemas/decision.puml`](docs/schemas/decision.puml) | `decision.puml.svg` | docwatch (PlantUML) |

Le SVG généré **n'est pas versionné** : c'est docwatch qui le produit à la demande. Si le fichier est présent, docwatch le régénère.

\## La convention

```text
docs/schemas/
  pipeline.mmd          ← source Mermaid
  pipeline.mmd.svg      ← généré par docwatch (pas committé)
  decision.puml         ← source PlantUML
  decision.puml.svg     ← généré par docwatch (pas committé)
```

- **Mermaid** : `foo.mmd` → `foo.mmd.svg`.
- **PlantUML** : `foo.puml` → `foo.puml.svg`.
- **Image Markdown** : `![texte](foo.puml.svg)` — relative, dans le même dossier.
- **SVG direct** : toujours autorisé pour les schémas sur mesure (les 18 SVG actuels restent directs).

\## Ce que les outils acceptent maintenant

\### `tools/verifier_schemas.py`

```text
schémas · 346 document(s) · 18 SVG · 2 source(s)
✅ aucun ASCII art, SVG valides et référencés, sources et images relatives.
```

Il vérifie :

1. **aucun ASCII art** dans un bloc de code ;
2. un **SVG direct** : XML, `viewBox`, `<title>`, `<desc>`, `role="img"`, aucune ressource externe ;
3. un **SVG généré** (`*.puml.svg`, `*.mmd.svg`) : XML, `viewBox`, aucune ressource externe — les
   métadonnées `title`/`desc` ne sont pas exigées, docwatch les produit ;
4. une image `<source>.svg` peut être **absente** si la source `.mmd`/`.puml` existe ;
5. chaque **source** `.mmd`/`.puml` doit être référencée par `<source>.svg` ;
6. chaque **image** est relative, en `.svg`, avec un texte alternatif.

\### `revue_documentation.py` et `verifier_liens.py`

Ils acceptent une cible `*.puml.svg` / `*.mmd.svg` **si la source existe**, même si le SVG n'est pas
encore généré. Un document normal (pas seulement un README) peut donc utiliser une image docwatch
sans casser la revue.

\## La documentation mise à jour

| document | ce qui change |
|---|---|
| [`AGENTS.md`](AGENTS.md) §2.9 | la règle cite docwatch et `<source>.svg` |
| [`docs/agent/illustrations.md`](d
… [1860 caractères tronqués]

### Tour 9 — si tu regarde ../reports et ../journal, peux-tu mettre à jour docs et tenir tout ça au propre

*27 appels d'outils.* Actions notables :

- bash — List latest reports, journals and commits
- bash — Read current state document
- bash — Inspect roadmap, journal and gate pass
- bash — Read latest report verdicts
- bash — Inspect report index, README and roadmap B section
- bash — Inspect references and sprint journal
- bash — Check B23 files and reports index state
- bash — Find latest gate pass references and roadmap actions
- bash — Locate exact state lines to update
- bash — Read court terme paragraph
- bash — Update state with B22/B23 and latest pass
- bash — Trim B12 line and adjust carte budget
- bash — Remove redundant B12 pipeline line
- bash — Inspect lines after B12 pipeline
- … et 12 autres

**Synthèse produite :**

⏵ Passe de cohérence terminée : état, références, roadmap et index alignés sur les rapports

\## Oui — la passe est faite

J’ai lu les **derniers rapports** (B19, B21, B22, B23, routeur M1→M2) et le **journal du sprint** (passe finale des portes du 27/10, `12 h 45 → 14 h 33`). Les documents étaient globalement à jour, mais il restait des **chiffres périmés**, une **passe de portes ancienne** et des **prochaines actions** non nommées.

\## Ce que les rapports et le journal disaient

| source | ce qui a été retenu |
|---|---|
| `rapport-m2-secours.md` (B19) | M1 100 % original, 98,7 % casse, 86,6 % phrase ; M2 typos **71,2 / 76,7** contre **36,6** ; phrase M2 **0** |
| `rapport-m9-dose.md` (B21) | M3 span **0/4/8/12/12** (tautologique) ; M5 ordre 2 **+4,25 pts** ; sham **nul** ; double lésion **non additive** |
| `rapport-m2-typo.md` (B22) | M2 **62–80 %** contre M1 **24–45 %** sur les quatre typos ; avantage **+21,9 à +46,5 pts** |
| `rapport-routeur-m1-m2.md` (B23) | routeur espaces **41,8 % vs 11,6 %** ; typo **56,2 % < M2 68,3 %** ; collision de lexique, pas un oracle |
| `journal/2026-10-27_sprint-24h.md` | passe finale **49 portes, 47 vertes, 2 rouges structurelles**, `porte-indice` **843 s**, `porte-melange` **112 s**, aucune régression |

\## Ce qui a été mis à jour

\### `docs/en-cours.md`

- **Mis à jour : 27/10, 16 h 30 HAE** (au lieu de 11 h 40).
- Ligne **B12** resserrée ; ligne **B12 pipeline** retirée (redondante avec la ligne B12 et la roadmap).
- Tableau « Où l’on en est » : la ligne B12 est remplacée par **B22/B23 — M2 et le routeur**.
- « Ce qui reste » nomme les suites :
  - **B23** : un score de confiance M1 (la collision de lexique laisse la typo à 56,2 %) ;
  - **B22** : typos réelles et secours conditionnel ;
  - **B21** : reproduire la dose M5 sur une autre lésion ;
  - puis **B10.3**, **B12.10**, **B9**.
- Dernière passe : **1 h 48 (27/10 14 h 33)**, au lieu de 1 h 34 (26/10).

\### `docs/references-non-regression.md`

- Nouvelle section **Passe du 2026-10-27 à 14 h 33** : **49 portes, 47 vertes, 2 rouges**, **1 h 48**,
  `porte-indice` 843 s, `porte-melange` 112 s, aucune régression.
- La passe du 26/10 devient **Passe précédente**.
- Bandeau, tableau des commandes et ligne d’historique alignés.

\### `docs/roadmap.md`

- Bloc **« Suites B19–B23 »** ajouté avant « L’ordre du jour » :
  - B23 → score de confiance M1 ;
  - B22 → typos réelles / secours conditionnel ;
  - B21 → reproduire la dose M5 ;
  - B19 → la niche est la typo et les e
… [2916 caractères tronqués]

### Tour 10 — les en-têtes "Révision documentaire" sont-elles encore nécessaires?

*23 appels d'outils.* Actions notables :

- bash — Locate revision banners across docs
- bash — Read special banner contents
- bash — Remove revision banners and keep useful notes
- bash — Inspect tops of all modified docs
- bash — Inspect T0 computation and word counts
- bash — Measure state sections and B lines
- bash — Remove A7 log, restore manques summary, adjust budget
- bash — Locate B12 additions in bloated docs
- bash — Measure sections of bloated docs
- bash — Compact A7 and B24-B27 into summaries
- bash — Locate rows to compact for budgets
- bash — Compact B rows and run all gates
- bash — Find stale counts and regenerate reports index
- bash — Update final counts and run gates
- … et 8 autres

**Synthèse produite :**

⏵ Non : les 16 en-têtes sont retirés, remplacés par des notes locales utiles

\## Non — elles ne sont plus nécessaires

Je les ai **toutes retirées** (16 occurrences). Elles étaient devenues contre-productives :

1. **Elles recopiaient les compteurs globaux** dans 16 fichiers, alors que la règle dit l’inverse : les compteurs vivent dans [`docs/en-cours.md`](docs/en-cours.md). Elles étaient déjà périmées (174/242, puis 185/252, puis 215/282).
2. **Elles racontaient une passe unique** (« passe 2/2, appliquée »), alors que le dépôt a depuis connu B12, B19–B27, docwatch et plusieurs passes de portes. C’était de l’histoire, pas de l’état.
3. **Elles coûtaient du contexte** : elles alourdissaient T0 (`AGENTS.md`, `en-cours`) et les budgets T1, sans être vérifiées par aucune porte.
4. **Les portes vérifient déjà les compteurs** dans `en-cours` ; le bandeau n’ajoutait aucune garantie.

\## Ce qui les remplace, quand une note locale est vraiment utile

| document | note conservée |
|---|---|
| `AGENTS.md` | **« Compteurs vivants »** → `docs/en-cours.md` ; ne pas les recopier ici |
| `docs/etat.md` | **« Redirection »** vers l’état courant et l’archive |
| `docs/glossaire/08` | **« Audit daté du 2026-10-10 »** + pointeur vers les compteurs vivants |
| `docs/references-non-regression.md` | **« Dernière passe »** (49 portes, 1 h 48, 27/10 14 h 33) |
| `docs/manques.md` | **« Dernière vérification : 2026-10-27 »** |
| `docs/synthese/03` | bandeau retiré ; la fiche concept porte **49/47/2 (27/10, 1 h 48)** |
| `docs/agent/rangement.md` | bandeau retiré ; le document décrit déjà la revue |

Les autres bandeaux (`REPRISE`, `docs/README`, `docs/carte`, `docs/organisation`, `docs/glossaire`, `docs/roadmap`, `docs/utilisation`, `docs/en-cours`, `reports/README`) sont **supprimés sans remplacement** : leur introduction suffit.

\## Le retrait a révélé un vrai problème de contexte

En enlevant les bandeaux, j’ai trouvé que l’état avait gonflé à **2 646 mots** : le chantier B12 y avait ajouté le journal **A7.5–A7.26** (22 mesures de cache KV/grappe réseau) et **B24–B27**. C’est exactement ce que la politique de contexte interdit — des résultats dans l’état.

J’ai compacté :

| document | avant | après | ce qui reste |
|---|---:|---:|---|
| `docs/en-cours.md` | 2 646 | **1 962** | ligne A7 + résumé **B24–B27** |
| `docs/carte.md` | 1 607 | **1 076** | une ligne A7, une ligne B24–B27 |
| `docs/roadmap.md` | 9 345 | **8 483** | une ligne A7 de campagne |
| `reports/README.md` | 3 345
… [1560 caractères tronqués]

### Tour 11 — révise le dossier méthode et les fichiers de directive du ../ pour optimiser le travail et assurer la continuité des tâc … [198 caractères tronqués]

*23 appels d'outils.* Actions notables :

- bash — Inventory new docs structure and root directives
- bash — Find DSH, cycle and subagent guidance
- bash — Read state page and context protocol
- bash — Run gates and find stale paths
- bash — Read result, filing and human-relations method docs
- bash — Read reprise, inventory and public README
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/methode/continuite.md`
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifie_en_cours.py`
- bash — Run en-cours checker and locate edits
- bash — Update en-cours and run checker/size
- bash — Update AGENTS with cycle rule and routes
- bash — Update REPRISE startup and DSH cycle
- bash — Update method docs with cycle and state discipline
- bash — Check method budgets and portes reds
- … et 9 autres

**Synthèse produite :**

⏵ Révision terminée : cycles DSH, sous-agents et discipline `en-cours` sont outillés

\## Oui — le dossier méthode et les directives racines sont révisés

J’ai relu les **12 documents de `docs/methode/`**, modifié les cinq qui portaient la continuité, et ajouté un document de pilotage. Les autres (`mission`, `miroir`, `panini-nipada`, `illustrations`, `ressources`, `modularisation`, `organisation-du-depot`) restent valides.

\## Les trois axes demandés

| axe | ce qui est désormais écrit | où |
|---|---|---|
| **Cycles DSH** | `max_goal_rounds` **1 000** (filet, pas objectif) ; **un goal par programme**, pas un par tâche ; reprise par `update_goal resume` ; un cycle se termine sur **résultat mesuré + fiche + commit + `en-cours` + roadmap**, jamais sur un compteur | `AGENTS` règle 10 · `REPRISE` · [`continuite.md`](docs/methode/continuite.md) |
| **Sous-agents** | **2 à 4 en parallèle** dès qu’il y a deux tâches indépendantes ; `subagent`, `subagent_fork`, `workflow` ; contrat de prompt en 7 points ; **rapport de 10 lignes** ; **diff d’état** ; le sous-agent ne touche **jamais** `en-cours`, `roadmap` ou `AGENTS` ; un seul écrivain par fichier | `continuite.md` · `resultats.md` · `relations-humaines.md` |
| **`en-cours`** | **seule source de l’état**, **≤ 2 000 mots**, mise à jour **à chaque cycle** ; une ligne par résultat + lien ; prochaine action nommée ; sous-agents actifs ; **5 questions ouvertes au plus** ; pas de logs ni de tableaux de mesures ; **seul le principal écrit** | `en-cours.md` · `contexte.md` · `resultats.md` · `rangement.md` |

\### Le nouveau document de référence

[`docs/methode/continuite.md`](docs/methode/continuite.md) contient :

- les **cycles DSH** (réglage 1 000, goal unique, reprise, fin de cycle) ;
- le **protocole des sous-agents** (quand, comment, contrat, rapport, intégration, anti-patterns) ;
- la **discipline de `en-cours`** (budget, cadence, contenu, lecture, écriture, dépassement) ;
- la **passation** (ce qu’un agent qui n’a rien vu doit pouvoir reprendre) ;
- les **commandes de vérification**.

\### Le vérificateur

Nouveau : [`tools/verifie_en_cours.py`](tools/verifie_en_cours.py).

```text
en-cours · 858 mots · 8 sections · 6 puces · 4 questions
✅ état court, structuré et reprenable
```

Il échoue si `en-cours` dépasse 2 000 mots, s’il manque une section, si « Ce qui est en cours » dépasse 10 puces ou contient un doublon, si les questions ouvertes dépassent 5, ou si la prochaine action n’est pas nommée.

\## Les directives
… [3175 caractères tronqués]

### Tour 12 — le dossier journal doit contenir un fichier par jour, ou un dossier par jour. on doit bien arrimer (hyperlien) les sessi … [72 caractères tronqués]

*46 appels d'outils.* Actions notables :

- bash — Inventory journal days, themes and sessions
- bash — Inspect journal generator and daily index
- bash — Read journal generator writing and session logic
- bash — Inspect session report and journal links
- bash — Read global indexes and session report writer
- bash — Read session report day scan and args
- bash — Patch journal_auto paths and session links
- bash — Rewrite day index for folder and sessions
- bash — Patch theme index for day folders
- bash — Patch session report links and folder index
- bash — Move journal files into day folders
- bash — Rewrite links to day folders
- bash — Global date path replacement
- bash — Regenerate session reports and journal README
- … et 31 autres

**Synthèse produite :**

⏵ Journal réorganisé : 34 dossiers de jour, 60 sessions ancrées, portes vertes

\## Oui — le journal est maintenant en dossiers par jour

Le choix retenu est **un dossier par jour** (et non un fichier unique) : une journée contient un index, plusieurs thèmes et parfois des pièces longues ; un seul fichier deviendrait illisible.

```text
journal/
  2026-09-25/ … 2026-10-28/   34 dossiers
    README.md                 index du jour
    <thème>.md                commits, sessions, mesures
    <récit>.md                pièce longue éventuelle
  README.md                   index général : 34 jours, 60 sessions
  THEMES.md                   index des thèmes
  sessions/<id>/              rapports et digests DSH
```

- **0 fichier de jour à la racine** (`journal/2026-*.md`).
- **34 dossiers** de jour, du **25/09** au **28/10**.
- **60 sessions** dans `journal/sessions/`.
- Le contrôle [`tools/verifie_journal.py`](tools/verifie_journal.py) vérifie la règle, les sections et les liens :

```text
journal · 34 jour(s) · 60 session(s) · 1379 lien(s)
✅ un dossier par jour, sessions ancrées, liens relatifs résolus
```

\## Les sessions sont ancrées dans les deux sens

\### Jour → session

Chaque `journal/AAAA-MM-JJ/README.md` a une section **« Sessions DSH »** :

- les sessions du jour, avec l’**identifiant complet** et les liens vers `rapport.md` et `digest.md` ;
- pour la journée en cours, la ligne **« Session en cours »** avec l’identifiant DSH, le lien vers `en-cours.md` et l’index des sessions.

Exemple, jour 28 :

```markdown
\## Sessions DSH

- **Session en cours** : `f0969e87-…` — [l'état](../../docs/pilotage/en-cours.md) ·
  [l'index des sessions](../README.md#sessions) ; rapport à la fin de la session.
```

\### Session → jour + état

Chaque `journal/sessions/<id>/rapport.md` commence par :

```markdown
> **Journaux :** [le jour](../../2026-09-28/README.md) · [l'état](../../../docs/pilotage/en-cours.md) ·
> [l'index des sessions](../../README.md#sessions).
```

Les 60 rapports ont ce bloc ; les sessions du 25/09 au 08/10 ont désormais leur **dossier de jour** — le journal ne commence plus artificiellement au 09/10.

\### État → sessions

[`docs/pilotage/en-cours.md`](docs/pilotage/en-cours.md) porte maintenant :

```markdown
- **Journaux** : [l'index des sessions](../../journal/README.md#sessions) ·
  [le journal du jour](../../journal/2026-10-28/README.md).
```

La session en cours `f0969e87` n’a pas encore de rapport (il sera produit à la fin de la session) : le jou
… [2521 caractères tronqués]

### Tour 13 — j'ai une session qui a un goal sur pause et je ne sais pas comment le repartir

*6 appels d'outils.* Actions notables :

- get_goal
- bash — Document paused goal resume procedure
- bash — Locate continuite rows and reports row to trim
- bash — Trim continuity/reports and run gates
- bash — Commit paused goal resume procedure
- job_output

**Synthèse produite :**

⏵ Ici, aucun goal : la reprise doit se faire dans la session qui le porte

\## Le goal est lié à sa session

`get_goal` sur **cette** session renvoie `null`. Un goal DSH est **attaché à la session qui l’a créé** : on ne peut pas le repartir depuis une autre session.

\## La marche à suivre

Dans la session qui affiche le goal en pause, écris simplement :

> **« Reprends le goal en pause. »**

C’est une demande humaine directe : l’agent de cette session a le droit d’appeler `update_goal`. Il doit alors faire :

1. `get_goal` → récupérer `goal_id` et `revision` ;
2. `update_goal` avec `action="resume"`, `goal_id` et `revision` ;
3. si la pause vient de la **limite de cycles**, faire d’abord `update_goal` avec `action="edit"` et `max_goal_rounds=1000`, puis `resume` ;
4. relire `docs/pilotage/en-cours.md` (« Session en cours » + « Ce qui reste ») avant de continuer.

\## Si la session est fermée

Rouvre **la même session** dans le harnais : le goal est persistant, il n’est pas perdu. Ensuite, envoie le message ci-dessus. Ne crée pas un nouveau goal : tu repartirais de zéro au lieu de reprendre l’historique.

\## Si l’agent répond « aucun goal »

C’est que tu n’es pas dans la bonne session. Le goal appartient à la session où il a été créé ; son identifiant est celui affiché dans cette session (l’`Id DSH`). Un fork ou une session voisine n’hérite pas du goal.

\## Ce qui est maintenant documenté

La procédure est écrite dans :

- [`docs/methode/continuite.md`](docs/methode/continuite.md), §5 « Reprendre un goal en pause » ;
- [`REPRISE.md`](REPRISE.md), étape 6 du cycle DSH.

Commit : `bedeebae MÉTHODE — REPRENDRE UN GOAL EN PAUSE (GET_GOAL → UPDATE_GOAL RESUME) ; INDEX 230`.

### Tour 14 — la lettre n n'apparait pas quand j'écris dans l'autre session. "continue" devient "cotiue" pourtant si je commence par s … [18 caractères tronqués]

*5 appels d'outils.* Actions notables :

- bash — Inspect DSH client environment and keybindings
- bash — Inspect DSH shortcuts package for n binding
- bash — Locate DSH shortcuts package and binary
- bash — Find DSH TUI shortcuts and n binding
- bash — Inspect DSH shortcut packages for n

**Synthèse produite :**

⏵ Lecture ciblée des raccourcis du client DSH

### Tour 15 — slash suivi de enter a réglé le problème

**Synthèse produite :**

⏵ Problème résolu : le passage par `/` + Entrée rétablit la saisie

Content que ça marche. Et c’est cohérent avec ce que fait le client :

- **`/` ouvre le menu de commandes** (une couche modale).
- **Cette modale bloque les raccourcis globaux** du client.
- **Entrée ferme la modale et rend le focus à la saisie** ; le raccourci qui mangeait `n` n’est plus prioritaire.

La cause probable est donc un **raccourci application lié à la touche `n`** (nouvelle session, suivant, etc.) : dans le client DSH, les raccourcis effectifs ont priorité sur les éditeurs, les terminaux et les champs de saisie. D’où « continue » → « cotiue », alors que le mode commande fonctionnait.

**Si ça revient**, le correctif durable :

1. ouvrir **Keyboard shortcuts** (`Mod+/`, ou Settings → « Edit shortcuts ») ;
2. chercher `N` ou la commande liée (probablement « New session » / « Next ») ;
3. **supprimer** le binding `N`, ou le rebinder en `Mod+N` ;
4. en Web, l’override est dans `dsh.keybindings.v1` (localStorage) ; en Desktop, dans `userData/keybindings.json`.

Et pour le goal en pause : dans l’autre session, tu peux maintenant écrire ou coller **« Reprends le goal en pause. »** — l’agent fera `get_goal` puis `update_goal` avec `action="resume"`.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/AGENTS.md` | 0 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/README.md` | 0 | 4 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/carte.md` | 0 | 4 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/en-cours.md` | 0 | 14 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/roadmap.md` | 0 | 7 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md` | 0 | 6 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/references-non-regression.md` | 0 | 5 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/REPRISE.md` | 0 | 5 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/etat.md` | 1 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/organisation-du-depot.md` | 0 | 8 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/utilisation.md` | 0 | 14 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/glossaire.md` | 0 | 6 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/agent/rangement.md` | 0 | 3 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/synthese/index.md` | 1 | 5 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/synthese/03-les-modes-et-les-portes.md` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/manques.md` | 0 | 3 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/revue_documentation.py` | 2 | 11 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/archive/README.md` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/README.md` | 0 | 4 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/glossaire/08-points-releves-non-corriges.md` | 0 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/index_reports.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/bilan-b11.md` | 0 | 5 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/glossaire/07-mesure-qualite-et-methode-experimentale.md` | 0 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-restitution.md` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs-3.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/synthese/schemas/parcours.svg` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/synthese/schemas/fiche-concept.svg` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/synthese/schemas/glossaire.svg` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/synthese/schemas/operations.svg` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/synthese/schemas/methode.svg` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/synthese/schemas/bus-evenements.svg` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/synthese/schemas/etages.svg` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/agent/contexte.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/taille_documents.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/glossaire_cartes.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/schemas/modules-cerveau-langage.svg` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/schemas/protocole-semantique.svg` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/schemas/jeux-symboliques.svg` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/schemas/format-flux.svg` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/agent/illustrations.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/schemas/README.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_schemas.py` | 2 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/schemas/pipeline.mmd` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/schemas/decision.puml` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/methode/continuite.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifie_en_cours.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifie_journal.py` | 1 | 0 |

### Commandes exécutées (échantillon)

- **T1** List repository top-level and docs structure
- **T1** Run documentation review and table gate
- **T1** Inspect git history, status and doc sizes
- **T1** Count report files and trace contradictory figures
- **T1** Check chapter counts, gate counts, dashboard counts
- **T1** Find dead path references in docs
- **T1** Verify gate counts and document sizes
- **T1** Cross-check gate, chapter and B4 counts
- **T1** Read documentation review tool
- **T1** Find orphan docs and mislabeled links
- **T1** Check unresolved contradiction and current counts
- **T1** Check git state and context doc contradiction
- **T1** Run doc gates and inspect B12 commit
- **T1** Compare B12 report, journal and synthesis
- **T1** Inspect headers and dates of key docs
- **T1** Read journal tail, archive policy and B11 bilan
- **T1** Count dead inline paths and README coverage
- **T1** Check subfolder counts and doc dates
- **T1** Separate dead prose paths from misleading link labels
- **T1** Read prior coherence audit and journal index
- **T1** Inspect uncommitted changes and test count
- **T2** Inspect pre-commit and freshness check
- **T2** Inspect en-cours header and references structure
- **T2** Recheck git state and document gates
- **T2** Inspect recent B12 commits
- **T2** Check current B12 documentation state
- **T2** Check working tree before phase 1 commit
- **T2** Commit phase 1 revision banners
- **T2** Run extended documentation review
- **T2** Re-run restricted review
- **T2** Bulk-fix archived path references
- **T2** Archive old module index
- **T2** Check remaining review alerts
- **T2** Verify both documentation gates
- **T2** Locate remaining old state references
- **T2** Check remaining stale mentions in utilisation
- **T2** Measure current line and byte counts
- **T2** Locate reference sections and history boundary
- **T2** Split current references and historical passes
- **T2** Diagnose history boundary string
- … et 285 autres

## 4. Mesures et résultats marquants

- **T1** `f8977255 2026-10-26 23:13:09 -0400 B11 — BILAN : CODEC 100 % ET RESTITUTION CANONIQUE 100 %, NATIF 59,8 % / INVARIANCE 40,7 %, RAISONNEMENT NON BRANCHÉ ; OBJECTIF NON ATTEINT`
- **T1** `386e59d5 2026-10-26 23:10:46 -0400 B11.9 — RESTITUTION CANONIQUE : 79/79 ET 449/449 ALLER-RETOUR RSN EXACT (100 %), SANS DÉCODEUR NEURONAL`
- **T1** `532ddd07 2026-10-26 23:08:12 -0400 B11.8 — CONTEXTE SÉPARÉ : 59,1 % / 40,7 %, AUCUN GAIN SUR LE SUFFIXE (59,8 / 40,7) ; LE VERROU EST AILLEURS`
- **T1** `38c3d880 2026-10-26 23:00:31 -0400 B11.7 — CONTEXTE SUFFIXÉ : 59,8 % DE CODE EXACT ET 40,7 % D'INVARIANCE ; PRÉFIXE 0,4 / 88,9 (COLLAPSE)`
- **T1** `c0f1e845 2026-10-26 22:52:47 -0400 B11.6 — CODEC + CONTEXTE : 528/528 (100 %), SANS CONTEXTE 374/528 (70,8 %) ; MÉMOIRE DE TRADUCTION 470 CIBLES, PAS UN MODÈLE`
- **T1** `docs/contexte-long.md:362:gpt-oss, 32 jetons de décodage) : **5,12 → 5,43 jetons/s, soit +6 %**, avec`
- **T1** `docs/convertisseur.md:249:le 30B-A3B à 20 Go/s ; nous en mesurons 5,4. Les tranches d'experts sont lues à`
- **T1** `docs/convertisseur.md:252:chiffre maintenant aussi ce régime — 4,81 tok/s prévus contre 5,4 mesurés.`
- **T1** `docs/configuration-nvme-raid-amd.md:296:   `lecteurs = 16` (« le NVMe passe de 5,4 à 31,1 Go/s ») et **ne s'en sert`
- **T1** `docs/roadmap.md:329:| B11.5 | **Cohérence inter-langues du natif** | ⚠️ **partiel** | normalisation lexicale : **55,7 %** de code exact et **37,0 %** d'invariance (contre 45,1 / 7,4) ; consistance sof`
- **T1** `docs/en-cours.md:43:  l'**adversaire de langue** (39,6 %, invariance 0) restent deux **négatifs**. Le codec reste à **100 %**. Avec le **contexte**, le codec lit **528/528** (100 %) ; sans contexte, *`
- **T1** `docs/archive/plan-mla-vision.md:581:| embedding de patchs, projecteur | **validés** contre numpy (5,4e-7 et 1,7e-6, à 28 × 28) |`
- **T1** `docs/archive/plan-kimi-k3.md:49:| planchers qui en découlent | disque dur **173 s/jeton** · NVMe (2 Go/s) **17 s** · PCIe x8 (6,5 Go/s) **5,4 s** · RAM (40 Go/s, mesuré) **2,17 s** | débits mesurés le`
- **T1** `docs/archive/plan-deepseek41-complet.md:853:> **115 521,8693** contre **74 328,5818**, soit **+55,4 %**. Plus de contexte =`
- **T1** `docs/archive/plan-deepseek41-complet.md:943:> | `proj+mlp` | 3 046,73 ms/token | **1 315,43 ms/token** |`
- **T1** `docs/archive/comparaison-spiking.md:106:(2,0 ms à 64 tokens, 12,7 ms à 512, ~200 ms extrapolé à 8 192) et ses poids`
- **T1** `docs/archive/cerveau-facultes.md:72:| **embedding de patchs** (`--banc-vision`, convolution 14 × 14 sur une image 28 × 28) | ✅ **vérifiée** contre la référence numpy (`tools/vision_ref.py`) : écart ma`
- **T1** `docs/archive/etat-cerveau.md:54:| **C8** | périphérie et réflexes (plan § C8) | ✅ **périphérie + mémoire livrées, réflexe mesuré** | sur **le même texte**, le chemin tronqué à 16 couches passe de **45`
- **T1** `docs/archive/etat-cerveau.md:375:déplace : (512, 512) coûte **+5,4 %** (12,8824 contre 12,2177) et (1 024, 1 024) **+1,9 %**`
- **T1** `docs/archive/etat-cerveau.md:382:corpus l'ordre s'inverse : 256 bat 128 de 5,4 %), et à 512 jetons **fenêtre 384 + 64 puits = +0,3 %**`
- **T1** `docs/archive/etat-cerveau.md:481:**adaptateur** sur **un texte** : **845,45** contre 456 586,60 (÷540), à ×59 du modèle complet.`
- **T1** `20:> 1297,5437**, `porte-topologie` **42,5477**, `porte-reparti-moteur` **0,0000 %**, `porte-greffe` **branchée**,`
- **T1** `26:> 449/449 au niveau 4, 11/11 paires, permutation 12/275, livre 10/10, go 9×9 10/10 contre 3/10). Les **deux`
- **T1** `30:> `porte-gain` **29,0206 → 1297,5437**, `porte-topologie` **42,5477**, `porte-reparti-moteur` **0,0000 %**,`
- **T1** `44:> `porte-topologie` **42,5477**, `porte-reparti-moteur` **0,0000 %**, `porte-greffe` **branchée**.`
- **T1** `63:> `porte-gain` **29,0206 → 1297,5437** · `porte-topologie` **42,5477** · `porte-reparti-moteur` **0,0000 %**.`
- **T1** `79:> `porte-coupe` **+0,52 % → +17,09 %**, `porte-gain` **29,0206 → 1297,5437**, `porte-topologie` **42,5477**,`
- **T1** `docs/references-non-regression.md:142:> passe à 46 portes** : `porte-homeostasie` (E9 : ×0 rend le modèle, l'activité est monotone,`
- **T1** `docs/synthese/index.md:30:| 8 | [les opérations : ce que l'état porte, et ce qu'il ne calcule pas](08-les-operations.md) | les **cinq mesures** de B4 (la négation : pas une direction, apprenable, un s`
- **T1** `> livre 10/10, go 9×9 10/10 contre 3/10, dames 0 défaite, cartes 44,7 % contre 51,0 %). Les **deux rouges**`
- **T1** `> `porte-pont` **+2,81 % / +25,35 %**, `porte-coupe` **+0,52 % → +17,09 %**, `porte-gain` **29,0206 →`
- **T1** `> 1297,5437**, `porte-topologie` **42,5477**, `porte-reparti-moteur` **0,0000 %**, `porte-greffe` **branchée**,`
- **T1** `> 449/449 au niveau 4, 11/11 paires, permutation 12/275, livre 10/10, go 9×9 10/10 contre 3/10). Les **deux`
- **T1** `> est **verte** (504 s, ×0 exact, activité monotone, dominance reproduite). Les références sont stables :`
- **T1** `> `porte-flux` **60,8135**, `porte-pont` **+2,81 % / +25,35 %**, `porte-coupe` **+0,52 % → +17,09 %**,`
- **T1** `> `porte-gain` **29,0206 → 1297,5437**, `porte-topologie` **42,5477**, `porte-reparti-moteur` **0,0000 %**,`
- **T1** `llama.cpp reste meilleur (+0,8 %) — son cache q8_0 garde une échelle par bloc`
- **T1** `2. **Le 4 bits est ici MEILLEUR que llama.cpp** (+364 % contre +494 %) tout en`
- **T1** `| **clés f16 · valeurs int8** | 3,125 | **39 %** | **+0,018 %** |`
- **T1** `| clés f32 · valeurs int8 | 5,125 | 64 % | +0,023 % |`
- **T1** `| clés f32 · valeurs int4 | 4,625 | 58 % | +0,46 % |`
- **T1** `| clés f16 · valeurs int4 | 2,625 | 33 % | +0,61 % |`
- **T1** `| int8 · int8 | 2,25 | 28 % | +3,04 % |`
- **T1** `| int4 · int4 | 1,25 | 16 % | +364 % |`
- **T1** `À taille ÉGALE (5,125 octets), mettre les bits sur les clés donne **+0,023 %** et`
- **T1** `sur les valeurs **+3,01 %** : facteur 130. À 4,625 octets, +0,46 % contre +385 % :`
- **T1** `le même à 4 096 (+0,011 % contre +2,25 % pour l'int8 complet), donc ce n'est pas un`
- **T1** `à 2 048 jetons). L'écart de +3,0 % contre +0,8 % à 8 192 **ne vient pas des valeurs** : le`
- **T1** `+0,023 %, `DRAVE_KV_V_F32=1` ne change rien : +3,01 %), et `docs/roadmap.md``
- **T1** `- **M5** : sans transitions → 1,1 %.`
- **T1** `- **M6** : sans porte → 30 %.`
- **T1** `- **M8** : sans sommeil → 0 %.`
- **T1** `1. **M1** est un **hub de lecture fiable** : 528/528 avec contexte, 100 % en canonique et en invariance.`
- **T1** `2. **M4** est une **mémoire épisodique exacte** sur le corpus : rappel 1,0, complétion 97,9 %,`
- **T1** `ne bat pas la majorité ; la porte est à 70 % ; la neuromodulation ne change rien ; le sommeil dégrade.`
- **T1** `> NVMe à ~3,5 Go/s, 20 cœurs Haswell AVX2).`
- **T1** `> l'array rend **7,45 Go/s** en lecture à 8 flux pour **6-7 Go/s** attendus au § 8, et **2,86 Go/s**`
- **T1** `**La base d’universaux typés (B11).** Après l’échec du décodeur libre, la sortie devient un **code typé** : 15 champs fixes (jeu, action, source, cible, carte, point, chemin…), 502 classes, one-hot dé`
- **T1** `**La distillation synthétique (B11).** Le parseur natif typé, nul en validation quand il n’avait que 377 surfaces réelles (48,3 % train / 0 % val), est **débloqué par la synthèse** : 10 556 surfaces m`
- **T1** `**Deux négatifs de cohérence (B11.5).** Pour rendre le parseur natif cohérent entre langues, deux régularisations ont été testées sur la distillation synthétique : la **consistance softmax** entre sur`
- **T1** `**La normalisation lexicale (B11.5).** Les mots du lexique (jeux, pièces, rangs, enseignes, passe) sont remplacés par des **concepts canoniques** avant le parseur. Sur le même entraînement synthétique`
- **T1** `**Le codec avec contexte (B11.6).** Le codec classique lit **528/528** coups B5/B7 quand il reçoit le **contexte** (position/trait) ; sans contexte, **374/528** (70,8 %). La **mémoire de traduction** `
- **T1** `**Le contexte suffixé (B11.7).** Le contexte RSN (trait, cases, plateau) a été ajouté au parseur natif, en deux positions. En **préfixe**, il collapse : **0,4 %** de code exact, **88,9 %** d’invarianc`
- **T1** `**Le contexte séparé (B11.8).** Un vecteur de contexte à hash stable (trigrammes, 512 dims, MLP) est ajouté aux états de surface, au lieu du texte suffixé. Résultat : **59,1 %** de code exact et **40,`
- **T1** `**La restitution canonique (B11.9).** Le codec rend les RSN dans un format canonique par jeu (`cellule`, `san`, `numerique`, `gtp`, `carte`) et les relit : **79/79** et **449/449** aller-retours RSN e`
- **T1** `**Bilan B11.** Le codec classique lit **528/528** coups et la restitution canonique fait **79/79 + 449/449** aller-retours RSN exacts (**100 %**). Le natif normalisé + contexte reste à **59,8 %** de c`
- **T1** `**Les modules M1–M9 (B12).** Premier prototype Python de la couche cerveau-langage : bus d’événements, hub typé, voies ventrales/dorsales, mémoire de travail, mémoire épisodique, prédictif, gating, ne`
- **T1** `> lecture et la restitution canonique, mais le **natif** ne lit qu'à **59,8 %** et le **raisonnement n'est pas`
- **T1** `| **(2) sens → texte** | codec canonique | **79/79 + 449/449**, aller-retour **100 %** | ✅ **canonique** |`
- **T1** `| | natif normalisé + contexte | **59,8 %** de code exact, invariance **40,7 %** | ⚠️ **partiel** |`
- **T1** `- **Restitution canonique** : **79/79** et **449/449**, aller-retour RSN exact **100 %**, sans décodeur`
- **T1** `- **Natif synthétique** : 45,1 % sans normalisation, **55,7 %** avec normalisation, **59,8 %** avec le`
- **T1** `contexte suffixé ; l'invariance passe de **7,4 %** à **40,7 %**.`
- **T1** `- **Natif** : 59,8 % de code exact, **40,7 %** d'invariance ; `carte` **69,3 %** ; les ambiguïtés de surface`
- **T1** `vecteur latent. Résultat du premier passage : le codec lit **100 %** des coups B5/B7, le parseur natif typé`
- **T1** `**surapprend** (48,3 % train, 0 % validation). Détail :`
- **T1** `cache KV** (« 75 % / 50 % » contre « 64 % / 28 % » dans le rapport qui l'a mesuré) et`
- **T1** `| 16:07 | `4ab50c03` | B9 — 31,63 M / 610 EXEMPLES : 4,40 % (3/3), MEILLEUR ÉCART ; LA CAPACITÉ NE PAIE QU'AVEC LES DONNÉES |`
- **T1** `| 22:28 | `325c1dec` | B11 — BASE D'UNIVERSAUX TYPÉS : CODEC 100 % (79/79, 449/449), PARSEUR NATIF TYPÉ SURAPPREND (48,3 % TRAIN / 0 % VAL) |`
- **T1** `| 22:35 | `1968af92` | B11 — DISTILLATION SYNTHÉTIQUE : 45,1 % DE CODE EXACT SUR 528 SURFACES RÉELLES (JEU 83 %, DE/VERS 90 %), INVARIANCE 7,4 % |`
- **T1** `| 22:43 | `0584fd74` | B11 — COHÉRENCE INTER-LANGUES : CONSISTANCE 38,3 % (INVARIANCE 0) ET ADVERSAIRE 39,6 % (0), DEUX NÉGATIFS ; LE BASELINE SYNTHÉTIQUE RESTE À 45,1 % |`
- **T1** `| 22:49 | `bb94843f` | B11.5 — NORMALISATION LEXICALE : 55,7 % DE CODE EXACT ET 37,0 % D'INVARIANCE (CONTRE 45,1 / 7,4), LE CODEC RESTE À 100 % |`
- **T1** `| 22:52 | `c0f1e845` | B11.6 — CODEC + CONTEXTE : 528/528 (100 %), SANS CONTEXTE 374/528 (70,8 %) ; MÉMOIRE DE TRADUCTION 470 CIBLES, PAS UN MODÈLE |`
- **T1** `| 23:00 | `38c3d880` | B11.7 — CONTEXTE SUFFIXÉ : 59,8 % DE CODE EXACT ET 40,7 % D'INVARIANCE ; PRÉFIXE 0,4 / 88,9 (COLLAPSE) |`
- **T1** `| 23:08 | `532ddd07` | B11.8 — CONTEXTE SÉPARÉ : 59,1 % / 40,7 %, AUCUN GAIN SUR LE SUFFIXE (59,8 / 40,7) ; LE VERROU EST AILLEURS |`
- **T1** `| 23:10 | `386e59d5` | B11.9 — RESTITUTION CANONIQUE : 79/79 ET 449/449 ALLER-RETOUR RSN EXACT (100 %), SANS DÉCODEUR NEURONAL |`
- **T2** `- **A7 la grappe déportée** — **faite** : le relais rend le même chiffre, la grappe exacte à 21 %, le transport à`
- **T2** `distillation est **4,40 % à 31,63 M / 610 exemples** ; la **fenêtre** (3,71 % à 500 pas, 1,29 % à 750, −0,49 % à`
- **T2** `8cf29faf 2026-10-27 09:19:34 -0400 B12 — M5 ORDRE 2 SANS GAIN, M7 NOUVEAUTÉ PAR SURFACE SANS EFFET ; M6 72,9 %`
- **T2** `091203d1 2026-10-27 09:16:22 -0400 B12 — M2 ACTION 98,6 % / DE 93,2 % (LÉSIONS 19,2 / 3,4) ; M7 NUL À CAPACITÉ 16`
- **T2** `28c09f51 2026-10-27 09:12:56 -0400 B12 — M7 NEUTRE (13,9 % VS 13,7 %), M8 96,48 % HORS STOCK ; M2/M3/M4 TIENNENT, M5/M6 NÉGATIFS`
- **T2** `c92ccf83 2026-10-27 09:10:08 -0400 B12 — M8 SOMMEIL GÉNÉRALISE : 96,48 % SUR ÉPISODES NON STOCKÉS (BASELINE 0) ; M2 LÉSIONS 17,8 / 2,7`
- **T2** `e6985d94 2026-10-27 09:06:46 -0400 B12 — M2 DOUBLE DISSOCIATION : DE 93,2 %, LÉSIONS 19,2 / 1,4 ; LE DERNIER ÉTAT DÉBLOQUE`
- **T2** `8cf29faf B12 — M5 ORDRE 2 SANS GAIN, M7 NOUVEAUTÉ PAR SURFACE SANS EFFET ; M6 72,9 %`
- **T2** `091203d1 B12 — M2 ACTION 98,6 % / DE 93,2 % (LÉSIONS 19,2 / 3,4) ; M7 NUL À CAPACITÉ 16`
- **T2** `28c09f51 B12 — M7 NEUTRE (13,9 % VS 13,7 %), M8 96,48 % HORS STOCK ; M2/M3/M4 TIENNENT, M5/M6 NÉGATIFS`
- **T2** `c92ccf83 B12 — M8 SOMMEIL GÉNÉRALISE : 96,48 % SUR ÉPISODES NON STOCKÉS (BASELINE 0) ; M2 LÉSIONS 17,8 / 2,7`
- **T2** `e6985d94 B12 — M2 DOUBLE DISSOCIATION : DE 93,2 %, LÉSIONS 19,2 / 1,4 ; LE DERNIER ÉTAT DÉBLOQUE`
- **T2** `db87e70f B12 — M2 SYNTHÉTIQUE : DE 6,2 % (146), M3 N-BACK CONTRÔLE 1,0 ; PAS DE DOUBLE DISSOCIATION`
- **T2** `f8977255 B11 — BILAN : CODEC 100 % ET RESTITUTION CANONIQUE 100 %, NATIF 59,8 % / INVARIANCE 40,7 %, RAISONNEMENT NON BRANCHÉ ; OBJECTIF NON ATTEINT`
- **T2** `2026-10-27 09:19:34 -0400 B12 — M5 ORDRE 2 SANS GAIN, M7 NOUVEAUTÉ PAR SURFACE SANS EFFET ; M6 72,9 %`
- **T2** `2026-10-27 09:16:22 -0400 B12 — M2 ACTION 98,6 % / DE 93,2 % (LÉSIONS 19,2 / 3,4) ; M7 NUL À CAPACITÉ 16`
- **T2** `2026-10-27 09:12:56 -0400 B12 — M7 NEUTRE (13,9 % VS 13,7 %), M8 96,48 % HORS STOCK ; M2/M3/M4 TIENNENT, M5/M6 NÉGATIFS`
- **T2** `2026-10-27 09:10:08 -0400 B12 — M8 SOMMEIL GÉNÉRALISE : 96,48 % SUR ÉPISODES NON STOCKÉS (BASELINE 0) ; M2 LÉSIONS 17,8 / 2,7`
- **T2** `2026-10-27 09:06:46 -0400 B12 — M2 DOUBLE DISSOCIATION : DE 93,2 %, LÉSIONS 19,2 / 1,4 ; LE DERNIER ÉTAT DÉBLOQUE`
- **T2** `53:  **M2** double dissociation (`action` **98,6 %**, `de` **93,2 %**, lésions **9,6 / 0,7 %**), **M5** ne bat pas la majorité, **M6** 72,9 %, **M7** nul (3,64 % = 3,64 %) ; **M8** généralise aux épis`
- **T2** `| **M1 hub** | surface → code RSN, retour canonique | **528/528** exact ; sans contexte **70,8 %** ; canonique **100 %** ; invariance **100 %** | ✅ **tient** |`
- **T2** `| **M2 voies** | ventrale (`action`) / dorsale (`de`) | `action` **98,6 %** ; `de` **93,2 %** (n=146) ; lésion ventrale `action` **9,6 %**, `de` **93,2 %** ; lésion dorsale `action` **98,6 %**, `de` *`
- **T2** `| **M3 mémoire de travail** | tampon de codes, span, n-back | span **12/12**, exact **1,0** ; n-back contrôle (5 codes répétés) **1,0** ; n-back brut **0,06 %** (test invalide) | ✅ **tampon** |`
- **T2** `| **M4 épisodique** | rappel par contenu, complétion, séparation | rappel **1,0** ; complétion **97,9 %** ; séparation **1,0** | ✅ **tient** |`
- **T2** `| **M5 prédictif** | action suivante, ordre 2 | exact **98,9 %** = majoritaire **98,9 %** | ❌ **aucun gain** |`
- **T2** `| **M6 gating** | langue cible, inhibition, commutation | exact **72,9 %** ; FP **1**, FN **18** ; coût **−0,11** | ❌ **faible** |`
- **T2** `| **M7 neuromodulation** | nouveauté par surface, mémoire bornée (16) | rétention **3,64 %** (fixe) = **3,64 %** (modulée) | ❌ **aucun effet** |`
- **T2** `| **M8 sommeil** | prototypes par (jeu, action), test **non stocké** | **96,48 %** sur 106 épisodes non stockés ; baseline épisodique **0 %** | ✅ **généralise** |`
- **T2** `| **M9 lésion** | privations déclarées | contexte **29,2 %** ; mémoire **0** ; prédictif **1,1 %** | ✅ **table de dépendances** |`
- **T2** `- **M1 sans contexte** : 70,8 % → le contexte est nécessaire.`
- **T2** `- **M2 lésion ventrale** : `action` 98,6 → 9,6 % ; `de` reste 93,2 %.`
- **T2** `| B12.1 | **Bus + hub M1** | ✅ **mesuré** | **528/528** exact avec contexte ; sans contexte **70,8 %** ; canonique **100 %** ; invariance **100 %** ; 1 584 événements |`
- **T2** `| B12.2 | **M2 voies ventrales/dorsales** | ✅ **double dissociation** | `action` **98,6 %** ; `de` **93,2 %** (n=146) ; lésion ventrale `action` **9,6 %**, `de` **93,2 %** ; lésion dorsale `action` **`
- **T2** `| B12.3 | **M3 mémoire de travail** | ✅ **tampon** | span **12/12**, exact **1,0** ; n-back contrôle **1,0** ; n-back brut **0,06 %** (test invalide) |`
- … (tronqué)

## 5. Erreurs rencontrées

5 sorties en erreur ou divergentes. Les premières :

- **T1** : == portes == 49 2:> par la passe complète des portes** (`tools/toutes-les-portes.sh`, **34 vertes sur 3:> 34**, 85 min 8 s). Elles ne sont pas recopiées de mémoire : elles sortent du journal de la 12:
- **T2** : [py_compile: ok] docs/references-non-regression.md:145: new blank line at EOF. [exit code: 2]
- **T7** : == log == 75bc27af ILLUSTRATIONS — SVG OBLIGATOIRE, 4 DIAGRAMMES ASCII CONVERTIS, 18 SCHÉMAS ACCESSIBLES ET VÉRIFIÉS (54 DOCS) 71e6035d BILAN — SPRINT 24 H : M1 SOLIDE, M5 CONTEXTE, M7 FRÉQUENCE, M8 M
- **T9** : == roadmap B == 363:| B23.1 | **Routeur M1→M2** | ⚠️ **partiel** | original **100 %**, casse **99,3 %**, phrase **92,5 %** = M1 ; espaces **41,8 %** vs M1 **11,6 %** ; typo **56,2 %** < M2 **68,3 %** 
- **T9** : == references == # Références de non-régression  > **Révision documentaire — 2026-10-27 (passe 2/2, appliquée).** Dernière passe : > **49 portes, 47 vertes, 2 structurelles, 1 h 34** (26/10 14 h 30). 

## 6. Commits

- DOCS — PASSE 1/2 : BANDEAUX DE RÉVISION SUR LES ENTRÉES (49 PORTES, 8 CHAPITRES, 170/241, 52 DOCS)" && echo "---" && git log -1 --format='%h %ad %s' --date=iso 
- DOCS — PASSE 2/2 : COHÉRENCE APPLIQUÉE (49 PORTES, 8 CHAPITRES, 172/241, 52 DOCS) ; 39 CHEMINS, 4 ORPHELINS, B10–B12, REVUE ÉTENDUE" && echo "---" && git log -1
- JOURNAL — RÉGÉNÉRATION APRÈS LE COMMIT DE COHÉRENCE (9 COMMITS DU 27/10, PASSE 2 VISIBLE)" && echo "---" && git log -1 --format='%h %ad %s' --date=iso && git st
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%Y-%m-%d %H:%M %Z' && python3 - <<'PY' import pathlib, subprocess p = pathlib.Path('docs/en-cours.m
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path('docs/en-cours.md') t = p.read_text(encoding='utf-8') old
- DOCS — FICHE DE COHÉRENCE (PASSAGE 3) ET COMPTEURS 174/242 ; REVUE, TABLEAUX ET REGISTRE VERTS" && echo "---" && git log -1 --format='%h %ad %s' --date=iso
- DOCS — LA FICHE DE COHÉRENCE ENTRE DANS L'ÉTAT ET LES FICHES COURANTES" && echo "---" && git log -1 --format='%h %ad %s' --date=iso && echo "---" && git status 
- DOCS — SYNTHÈSE COMME INTRODUCTION : 9 FICHES CONCEPT, 14 SCHÉMAS, GLOSSAIRE ET LIENS RELATIFS"
- DOCS — SCHÉMA MÉTHODE : TEXTES DANS LES CADRES" && echo "---" && git log -1 --format='%h %ad %s' --date=iso && git status --short
- DOCS — LA FICHE DE COHÉRENCE ENREGISTRE L'INTRODUCTION DE LA SYNTHÈSE"
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path('docs/roadmap.md'); t = p.read_text(encoding='utf-8') t =
- DOCS — CONTEXTE IA : BUDGETS ET MANIFESTE, CHAPITRE 5 SCINDÉ, INDEX RÉDUIT (175/242/53, T0 3 561 MOTS)"
- GLOSSAIRE — 289 FICHES PAR ENTRÉE, INDEX GROUPÉ, MANIFESTE MDSERVE ; COMPTEURS 179/246/53"
- GLOSSAIRE — 289 FICHES PAR ENTRÉE, INDEX ET MANIFESTE MDSERVE (FICHE)"
- GLOSSAIRE — CONTRAT MDSERVE DANS L'INDEX (289 FICHES)"
- GLOSSAIRE — MODE --VERIFIER ET LIENS CONDITIONNELS (289 FICHES)"
- ILLUSTRATIONS — SVG OBLIGATOIRE, 4 DIAGRAMMES ASCII CONVERTIS, 18 SCHÉMAS ACCESSIBLES ET VÉRIFIÉS (54 DOCS)"
- ILLUSTRATIONS — ANNOTATION ÉTAT DANS LE PANNEAU (ANATOMIE)"
- ILLUSTRATIONS — MÉTADONNÉES ACCENTUÉES DES SCHÉMAS (TITLES ET DESCRIPTIONS)"
- DOCWATCH — SOURCES .MMD/.PUML, IMAGES <SOURCE>.SVG, VÉRIFICATEURS ADAPTÉS (184/251/54)"
- DOCS — ÉTAT ET RÉFÉRENCES À JOUR (B22/B23, PASSE 27/10, 185/252/54) ; SVG DOCWATCH IGNORÉS"
- DOCS — DOCWATCH MULTI-RACINES, 87 TESTS, SVG GÉNÉRÉS ; ÉTAT C6 À JOUR"
- DOCS — RETRAIT DES EN-TÊTES « RÉVISION DOCUMENTAIRE » ; ÉTAT, CARTE, ROADMAP ET INDEX COMPACTÉS (215/282/54)"
- DOCS — DATE DU 28/10 (ÉTAT ET SYNTHÈSE)"
- MÉTHODE — CYCLES DSH 1000, SOUS-AGENTS INTENSIFS, EN-COURS SOUS CONTRÔLE (56 DOCS)"
- JOURNAL — GÉNÉRATEURS EN DOSSIERS PAR JOUR (SESSION → JOUR/ÉTAT)"
- JOURNAL — UN DOSSIER PAR JOUR (34 JOURS), SESSIONS DSH ANCRÉES AUX JOURS ET À EN-COURS ; 57 DOCS"
- MÉTHODE — REPRENDRE UN GOAL EN PAUSE (GET_GOAL → UPDATE_GOAL RESUME) ; INDEX 230"

