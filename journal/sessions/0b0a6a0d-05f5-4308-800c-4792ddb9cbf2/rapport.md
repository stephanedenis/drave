# Session 0b0a6a0d — Continue session work

> **Journaux :** [le jour](../../2026-10-31/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `0b0a6a0d-05f5-4308-800c-4792ddb9cbf2` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-31 17:17 |
| Durée | 32.4 h |
| Tours | 18 |
| Messages | 1297 |
| Appels d'outils | 1204 |
| Fichiers touchés | 11 |
| Commandes | 968 |
| Sous-agents | 0 |
| Commits | 50 |
| Compactages de contexte | 1 |

## Objectifs déclarés

- **create** — N2 — mesurer le curriculum et les données sur le dispositif reconstruit (budget complet 41 Mo / 20 000 pas, 4 sources contre français seul, puis curriculum 129), avec contrôle négatif et trois graines ; écrire la fiche dans reports/, le récit dans journal/, committer avec le chiffre et mettre docs/p
… [41 caractères tronqués]
- **complete** — N2 — mesurer le curriculum et les données sur le dispositif reconstruit (budget complet 41 Mo / 20 000 pas, 4 sources contre français seul, puis curriculum 129), avec contrôle négatif et trois graines ; écrire la fiche dans reports/, le récit dans journal/, committer avec le chiffre et mettre docs/p
… [41 caractères tronqués]
- **create** — N2.h — le mètre propre : construire un corpus dédupliqué avec split train/val/test sans répétition (outil versionné + manifeste + vérification), refaire toute la chaîne sur ce corpus (professeur 23,5 M, base supervisée, distillation 20k × 3 graines, curriculum 129), mesurer la porte honnête et le pr
… [344 caractères tronqués]
- **edit** — Suivre le plan de travail (docs/pilotage/plan-travail.md) et avancer la ligne N2 en autonomie jusqu'à 08 h 00 le 2026-11-02 : distillation sur le corpus réel (professeur 23,57 M, 3 graines, positions aléatoires), canal d'annotation de structure (avec placebo et ablation), base anglaise monolingue, s
… [189 caractères tronqués]
- **resume** — Suivre le plan de travail (docs/pilotage/plan-travail.md) et avancer la ligne N2 en autonomie jusqu'à 08 h 00 le 2026-11-02 : distillation sur le corpus réel (professeur 23,57 M, 3 graines, positions aléatoires), canal d'annotation de structure (avec placebo et ablation), base anglaise monolingue, s
… [189 caractères tronqués]

## 1. Ce qui a été demandé

**Tour 1** — continue

**Tour 2** — <goal_round> Objective: "N2 — mesurer le curriculum et les données sur le dispositif reconstruit (budget complet 41 Mo / 20 000 pas, 4 sources contre français seul, puis curriculum 129), avec contrôle négatif et trois graines ; écrire la fiche dans reports/, le récit dans journal/, committer avec le chiffre et mettre docs/pilotage/en-cours.md et la roadmap à jour." Round: 1/1000  Continue working  … [511 caractères tronqués]

**Tour 3** — je te donnes 10h de liberté totale. impressionne-moi. je serai décu si tu as terminé à temps.

**Tour 4** — en-cours.md doit contenir pour chaque session tout ton plan, ambition et stratégie et objectif final. Continue ton bon travail en maintenant ce document à jour pour que les autres sessions locales puissent être en synergie avec tes travaux.

**Tour 5** — continue

**Tour 6** — vérifie l'état des autres sessions dsh et mets à jour les fichiers en-cours.md et roadmap.md

**Tour 7** — fais les deux en parallèle

**Tour 8** — Est-on encore loin de pouvoir utiliser le système pour du vrai travail?

**Tour 9** — peut-on s'éloigner du modèle octet et modèle token pour aller vers un modèle qui voit la structure du texte en surface avant un peu comme la perception humaine le fait avec la saccade et les mots dont on peut mélanger les lettres du milieu sans qu'on s'en rende compte à la lecture rapide.

**Tour 10** — en tant que programmeur, j'apprécie la coloration du code, syntaxe et structure indentée. On pourrait imaginer un outil semblable pour la linguistique. C'est à dire une coloration et découpage visuel de la structure des phrases et paragraphes. Bref quand j'apprends un nouvelle langue c'est le genre d'outil que j'aimerais avoir. Il serait profitable d'avoir un tel outil en entrée de notre modèle po … [63 caractères tronqués]

**Tour 11** — allons-y, mais créons d'abord un outil pour humain dans un projet distinct (submodule git) qui permet d'afficher en web un ensemble de structures d'interprétation candidatees. On a donc un moyen de voir et valider les interprétations par un humain. On peut aussi soumettre cet ensemble à au grss modèle comme DeepSeek via l'API pour étudier son évaluation. et se construire ainsi un banque de corpus  … [28 caractères tronqués]

**Tour 12** — lance le serveur et continue

**Tour 13** — Les phrases présentées sont ambigues et ne peuvent être résolues hors contexte, même par un humain. En contexte, cette ambiguité peut avoir une intention humouristique. on doit donc avoir un nuveau pragmatique pour trancher et conserver les 2 sens.

**Tour 14** — ça va prendre des contextes plus larges pour trancher sur les interprétations ambigues.

**Tour 15** — peux-tu comencer l'entrainement avec des phrases non ambigue et étudier les effets  sur la qualité du bloc linguistique.

**Tour 16** — continue avec de trèes gros corpus multilingues

**Tour 17** — lire docs/pilotage/plan-travail.md et avancer

**Tour 18** — suis le plan, continue jusqu'à 8h demain matin

## 2. Déroulé, étape par étape

### Tour 1 — continue

*96 appels d'outils.* Actions notables :

- get_goal
- bash — Show git status and recent commits
- bash — Check state file sizes and recent journal
- read
- bash — Inspect uncommitted changes
- bash — Check session status
- bash — Check today's journal files
- bash — Find N2 section in roadmap
- bash — Read roadmap N2 details
- bash — List N2 reports and tooling
- bash — Find curriculum references and distiller scripts
- bash — Check GPU availability
- bash — Read R12 curriculum backlog card
- bash — Read distillation script header
- … et 79 autres

**Synthèse produite :**

⏵ Réponse sur l'état et la carte des conflits

**Non, il ne l'était pas** — la page datait de 17 h 15 et disait encore « aucune session active ». C'est corrigé, validé et committé : `54dc7a26`. `tools/sessions.py --status` me voit maintenant « en cours ».

**Ce que l'autre session lira dans `en-cours`**

- Session active `0b0a6a0d-05f5-4308-800c-4792ddb9cbf2`, rôle **N2 — le budget complet** (campagne GPU en cours : français seul, manifeste 4 sources, quotas égaux, curriculum 129 ; 3 graines).
- Fichiers réservés : `work/n2d/`, `tools/distiller_budget.py`, `reports/n2-*`, `journal/sessions/0b0a6a0d-…/`.

**Ce qu'elle peut prendre sans collision**

- La documentation, le backlog, **N4** (consigne courte, sans GPU), et les portes **documentaires** (`PORTES="..."`).
- Tout ce qui ne touche ni mes fichiers réservés ni les GPU.

**Ce qu'elle ne doit pas prendre (conflits réels, pas théoriques)**

- `bash tools/toutes-les-portes.sh` : la passe complète utilise les **deux cartes** et fausserait mes mesures (c'est écrit dans `docs/methode/portes.md` : portes et mesure GPU ne cohabitent pas). Je la lancerai moi-même à la fin, seule.
- Un entraînement GPU, pour la même raison.
- `docs/pilotage/en-cours.md` : **une session écrit à la fois**. Si elle doit y mettre un fait, qu'elle me le dise — je libère la page.
- La `roadmap` et `reports/n2-*` : je les édite à la clôture.

**Horaires** : la campagne tourne jusqu'à ~19 h 40 (6 runs restants), puis agrégation, fiche, et passe complète des portes (1 h 30–2 h) avant le commit de clôture. Si elle a besoin d'un GPU avant, elle me le dit et je réordonne.

Au passage : `work/` est désormais dans `.gitignore` — sinon un `git add -A` aurait stagé 1–2 Go de points de contrôle. `tools/docwatch` reste modifié en local (sous-module, pas à moi).

### Tour 2 — <goal_round> Objective: "N2 — mesurer le curriculum et les données sur le dispositif reconstruit (budget complet 41 Mo / … [791 caractères tronqués]

*206 appels d'outils.* Actions notables :

- bash — Check campaign status
- bash — Compute manifest source shares
- bash — Check working tree and generated journal file
- bash — Quantify the sampling-grid difference
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/n2d/evalue-final.py`
- bash — Check seed 1 completion
- bash — Check train/val overlap for contamination
- bash — Read seed 1 final results
- bash — Check run logs and processes
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/n2d/agrege.py`
- read
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/n2d/agrege.py`
- bash — Check for seed 1 final results
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/n2d/robustesse.py`
- … et 154 autres

**Synthèse produite :**

⏵ Clôture : N2.d mesuré, écrit, committé, portes vertes

\## Ce qui est établi

**La campagne N2.d** — 12 distillations, 3 graines par bras, deux GPU, ~3 h :

| bras | protocole 8×16×128 | fenêtres propres | 8×15×129 |
|---|---:|---:|---:|
| base supervisée | 3,2161 | 3,2450 | 3,2653 |
| **T5k** (5 000 pas, réf.) | 2,9355 | 3,0534 | 2,9623 |
| **A** — 20 000 pas, français seul | **2,8527** | **2,9795** | 2,8743 |
| **B** — 4 sources (82,5 % anglais) | 3,7591 | 3,8573 | 3,8218 |
| **B′** — 4 sources à quotas égaux | 3,4350 | 3,5634 | 3,4848 |
| **C** — curriculum 129 sur A | 2,8471 | 2,9783 | **2,8327** |

- **Le budget paie peu** : −0,0828, du même ordre que la chaîne historique ; la porte < 2,5 reste à 0,35 (protocole) / 0,48 (fenêtres propres).
- **Les données coûtent** : +0,91 pour le manifeste, +0,58 même à quotas égaux (professeur français sur octets anglais : confondant nommé).
- **Le curriculum 129** gagne 0,0416 à 129, 0,0056 à 128.

**Le résultat qui change la lecture** : la validation n'est **pas** tenue à l'écart. 32,8 % des fenêtres du protocole (42/128) sont **verbatim** dans l'entraînement ; 23,5 % des fenêtres d'entraînement y apparaissent plus d'une fois. Les fenêtres contaminées donnent 0,39 de PPL de moins que les propres, et l'écart croît avec le budget (0,17 → 0,35 → 0,39). **2,7078 et 2,6998 sont mesurés sur ce même jeu contaminé** : la porte < 2,5 n'a jamais été une mesure de généralisation.

\## Vérification

- Trois graines par bras, écart-type 0,002–0,008 ; comparaison appariée (mêmes fenêtres).
- Contrôles : permutation (PPL ≈ 1087), base sans distillation, distillation courte, B′ contre B, C contre A graine par graine.
- Robustesse : sur quatre grilles de fenêtres, A reste sous T5k (−0,083 à −0,118).
- **Portes** : passe complète 79 portes, **75 vertes, 4 rouges** — les quatre connues et tolérées (`porte-indice`, `porte-melange`, `porte-homéostasie`, `porte-reparti-moteur`) ; `porte-ocr` verte. Journaux `/tmp/portes-1031-n2d`, 1 h 39.
- Revue de documentation, budget de contexte, état, journal, backlog et schémas : tous verts.

\## Artefacts

- Fiche : `reports/rapport-n2-budget.md` · agrégat `reports/n2-budget.json` · récit `journal/2026-10-31/apprentissage.md`.
- Code : `tools/distiller_budget.py`, `tools/eval_n2_budget.py`.
- Points de contrôle : 542 Mo sur deux disques (`backups/n2/2026-10-31/n2d/`, `IA/artefacts/n2/2026-10-31/n2d/`).
- Commits : **`c3bcbe99`** (résultat) et `10fa4f42` (références des portes).
- État et roadmap 
… [593 caractères tronqués]

### Tour 3 — je te donnes 10h de liberté totale. impressionne-moi. je serai décu si tu as terminé à temps.

*37 appels d'outils.* Actions notables :

- bash — Determine which repo files compose the French corpus
- bash — Measure the size of duplicated passages
- bash — Check teacher time and external corpora
- bash — Extract teacher and base training durations
- bash — Read the teacher log for duration
- create_goal
- todo_write
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/corpus_propre.py`
- bash — Test dedupe on a synthetic text
- bash — Build the deduplicated corpus
- bash — Inspect clean corpus seams and trainer CLI
- bash — Check whether the teacher early-stops on validation
- bash — Check checkpoint selection in the teacher trainer
- bash — Launch teacher and base training on the clean corpus
- … et 22 autres

**Synthèse produite :**

⏵ Ajout des positions aléatoires (attaque du verrou de longueur) au modèle et au distillateur

### Tour 4 — en-cours.md doit contenir pour chaque session tout ton plan, ambition et stratégie et objectif final. Continue ton bon t … [120 caractères tronqués]

*291 appels d'outils.* Actions notables :

- bash — Check active sessions, state, and campaign
- bash — Measure the context budget headroom
- read
- bash — Rewrite the state with the full session plan
- bash — Add the Id field and restore the remaining-work section
- bash — Read the session plan file
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/plan.md`
- bash — Re-read the session plan
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/plan.md`
- bash — Write the session plan and validate
- bash — Commit the state update for other sessions
- job_output
- bash — Check campaign state after the state commit
- bash — Draft the clean-corpus report
- … et 210 autres

**Synthèse produite :**

⏵ Bilan de la nuit et vérification finale

Tout est committé, les portes sont vertes, l'état est clos. Voici ce que les dix heures ont produit.

\## Le problème que j'ai attaqué

N2 avait un défaut plus grave que son plateau : **son mètre mesurait de la mémoire**. 32,8 % des fenêtres de validation étaient verbatim dans l'entraînement. Plutôt que d'ajouter un levier de plus, j'ai reconstruit le mètre, refait la chaîne, puis posé les trois leviers que les chiffres contaminés ne pouvaient pas trancher.

\## Les résultats

| question | réponse | contrôle |
|---|---|---|
| la validation fuit ? | **32,8 % → 0 / 2 814** après déduplication (−22,2 % de texte) | `tools/corpus_propre.py`, manifeste |
| la porte honnête ? | **3,09** en domaine (3,20 au test), pas 2,85 → la porte < 2,5 est à **0,59** | chaîne entièrement réentraînée |
| un modèle de français ? | **non** : 16,70 sur de la littérature jamais vue, 57,6 en anglais | corpus externe, 3 graines |
| la distillation ? | elle **spécialise** : base 12,29 hors domaine, élève 16,70 | base vs distillé |
| la diversité ? | **16,70 → 3,85** (÷ 4,3), anglais ÷ 2,2, pour **+0,17** en domaine | professeur et base mixtes |
| le verrou de longueur ? | **14,11 → 3,25** à 256 octets avec des positions aléatoires ; au-delà, c'est la **fenêtre locale** (5,93 à 512) | 3 graines, 129→512 |
| les deux ensemble ? | **oui** : 3,47 / 4,10 / 3,49 à 256 — les coûts s'additionnent comme les gains | 3 graines |
| la capacité ? | elle **paie** −0,06 en domaine (21,65 M), mais ne couvre ni la généralité ni la longueur | 2 graines |

**Le résultat qui compte pour la suite** : le modèle de N2 n'est pas un mauvais modèle de français, c'est un **spécialiste du dépôt**. Ce n'est pas la distillation qui est en cause, c'est ce qu'elle distille — et le corpus est le levier, pas le budget.

\## Livrables

- **5 fiches** : `n2-propre`, `n2-diversite`, `n2-longueur`, `n2-combine`, `n2-capacite`, plus l'agrégat `n2-propre.json`.
- **2 corpus propres** avec manifestes et empreintes (`corpus-propre.json`, `corpus-litt-propre.json`).
- **20 points de contrôle (1,4 Go)** archivés sur **deux disques** (`backups/n2h/2026-11-01/` et `IA/artefacts/n2h/2026-11-01/`).
- **5 commits** : `e36e8185` (corpus + porte + longueur), `1da58752` (journal), `52cf5853` (combinaison), `88f598c3` (clôture), `3a6ae9ca` (capacité).
- **Portes** : passe complète 80 portes, **76 vertes**, 4 rouges — les quatre connues (indice, melange, homeostasie, reparti-moteur). Aucune régress
… [839 caractères tronqués]

### Tour 5 — continue

*19 appels d'outils.* Actions notables :

- bash — Test whether the local window mask is the second lock
- bash — Add the mask test to the report, roadmap and state
- bash — Trim the mask addition to fit the budget
- bash — Final trim for the context budget
- bash — Commit the mask experiment
- job_output
- bash — Census of the unique French text available in the repo
- bash — Run the corpus census in the background
- bash — Check the actual system time and last commit time
- bash — Read the census result
- bash — Read the full census result
- bash — Record the census in the repo and the state
- bash — Trim the state to fit after the census
- bash — Commit the census
- … et 1 autres

**Synthèse produite :**

⏵ Clôture — deux ajouts depuis le bilan, et l'état est propre

\## Ce que j'ai ajouté après le bilan

**1. Le second verrou n'est pas le masque** (`d2613e8f`). À 512 octets, l'attention locale ne laisse voir que les 256 précédents. J'ai élargi la fenêtre **à l'inférence** sur les mêmes modèles : 6,13 (fenêtre 256) → **6,37** (512) → 6,37 (1 024) pour R, et 5,46 → 5,42 pour DR. Élargir le masque **ne récupère rien**. Le second verrou est donc l'**entraînement** — le modèle n'a jamais vu plus de 128 octets de contexte — et non la fenêtre. Pour R1, lire 1 000 octets demandera des contextes longs à l'entraînement (les positions aléatoires étant la condition pour que les positions suivent), pas un réglage de masque.

**2. Le levier « plus de texte » a un chiffre** (`18f28437`). Recensement avec les mêmes shingles que le corpus propre : `docs+journal` (995 documents) contient **27,67 Mo uniques** sur 48,73 bruts (−43,3 %), et avec `reports` (1 540 documents), **30,35 Mo**. Le corpus d'entraînement de N2.h fait 3,24 Mo : il y a **8,5 fois plus de français disponible** dans le dépôt que ce qui a été mangé. Réserve : `journal/sessions` contient des transcripts, à filtrer avant d'en faire un corpus. Manifeste : `reports/recensement-francais.json`.

\## État final

- **7 commits** cette nuit : `e36e8185` (corpus + porte honnête + longueur), `1da58752` (journal), `52cf5853` (combinaison), `88f598c3` (clôture), `3a6ae9ca` (capacité), `d2613e8f` (masque), `18f28437` (recensement).
- **5 fiches** + 4 manifestes (`corpus-propre`, `corpus-litt-propre`, `n2-propre`, `recensement-francais`).
- **20 points de contrôle (1,4 Go)** archivés sur deux disques (`backups/n2h/2026-11-01/`, `IA/artefacts/n2h/2026-11-01/`).
- **Portes** : 80 portes, 76 vertes, 4 rouges connues ; les portes documentaires repassent vertes après le dernier commit.
- **Revue de documentation, budget de contexte, état, journal, backlog, schémas** : tous verts, arbre de travail propre.
- `docs/pilotage/en-cours.md` porte le plan, l'ambition, la stratégie, les résultats et **le prochain levier chiffré** (27,7 Mo de français unique, 8,5×).

\## La question qui reste, désormais bien posée

N2 n'a plus de levier d'entraînement à essayer : la position est réglée, la diversité mesurée, la capacité tranchée. Ce qui manque tient en une ligne — **le corpus est huit fois plus petit que ce que le dépôt contient**. Le prochain cycle n'a pas besoin de GPU pour commencer : il a besoin d'un corpus de français propre, filtré (
… [75 caractères tronqués]

### Tour 6 — vérifie l'état des autres sessions dsh et mets à jour les fichiers en-cours.md et roadmap.md

*30 appels d'outils.* Actions notables :

- bash — List session statuses
- bash — Recent commits from all sessions
- bash — Read the Pensée session plan and reports
- bash — Read the R4.4 session plan and final report
- bash — Read the R4.4 final verdict
- bash — Check the Pensée session's deliverables
- bash — Check the Pensée session's commits and code
- bash — Read the R4.4 verdict and limits
- bash — Locate R4.4 and Pensée references in the state
- bash — Read the Pensée block and the in-progress bullets
- bash — Locate R4.4 in the roadmap
- bash — Find Pensée in the roadmap and read the order of day
- bash — Inspect the B program table for a Pensée slot
- bash — Measure budgets before editing
- … et 16 autres

**Synthèse produite :**

⏵ Bilan de la vérification des sessions et des mises à jour

\## L'état des trois sessions

| session | état | dernier travail | prochaine action |
|---|---|---|---|
| `0b0a6a0d` — **N2.h** | **close** | 7 commits, 5 fiches, portes vertes | close — le levier est chiffré (27,7 Mo de français unique) |
| `fe3c05f0` — **R4.4** | **close** (plan clos le 01/11 02 h 55) | 100 scans simulés, 5 familles, 3 vrais scans | reste pour une autre session : **scans réels de bout en bout** avec vérité humaine, fax, exposant fusionné |
| `e181ce02` — **Pensée** | **plan actif, session en pause** depuis le 31/10 22 h 49 (heartbeat périmé de 504 min) | théorie (`pensee-iterative.md`, 10 tours, 9 schémas) **et** implantation (`moteur-de-pensee.md`) écrites ; `tools/pensee/` absent | **state store v0** — c'est la seule chose qui manque pour démarrer le moteur |

Rien n'est bloqué côté ressource. Le seul point d'hygiène est le heartbeat du plan de Pensée, resté au 31/10 22 h 45 : la session ne tourne plus, mais son plan dit encore « actif ». Je l'ai **noté dans l'état** plutôt que de réécrire son fichier (il est réservé) ; à rafraîchir ou à clore à sa reprise.

\## Ce que j'ai mis à jour

**`docs/pilotage/en-cours.md`**
- **R4.4** : le bloc passe de « ce qu'elle fait » à **« terminée »** (plan clos le 01/11 02 h 55), avec les chiffres alignés sur la fiche (`r44-scans`) : photo **55,9 → 6,7 %** de WER, **4/5 familles ≥ 90 %** de parité, fax **56,7 %** (limite d'information), colonnes **89,4 → 0,5 %**, tableaux **92,6 %**, trois vrais scans **7,10 / 88,4 %**. La prochaine action dit désormais **close**, et ce qui reste est nommé pour une autre session.
- **Pensée** : « théorie et implantation écrites, `tools/pensee/` absent, **session en pause** ».
- **Puce R4.4** de « Ce qui est en cours » condensée (elle dupliquait le bloc de session), ligne **R** des chantiers mise à jour, horodatage **2026-11-01 07 h 20 HNE**.
- Les trois blocs de session ont été **condensés** pour que le budget de contexte repasse sous la barre : **T0 = 3 994 mots** (plafond 4 000), sans perdre le plan, l'ambition, la stratégie et l'objectif de chaque session.

**`docs/pilotage/roadmap.md`**
- Ligne **R** du tableau des programmes : `R4.4 partiel` → **`R4.1–R4.4 mesurées`** (4/5 ≥ 90 %), la prochaine action devenant les **scans réels de bout en bout**.
- **Ordre du jour, item 1** : R4.4 y est dite **mesurée** (et non « partielle »), avec le test à **5,7 %** (la fiche disait 5,68 %, l'ancien texte 5,3 %).
- Lig
… [1382 caractères tronqués]

### Tour 7 — fais les deux en parallèle

*70 appels d'outils.* Actions notables :

- bash — Measure corpus candidates
- bash — Read the Pensée implementation spec
- bash — Inspect a session digest
- bash — Build the enlarged clean corpus from the current repo
- bash — Launch the teacher and base on the enlarged corpus
- bash — Read the rest of the Pensée implementation spec
- bash — Write the core types and test the Merkle fingerprint
- bash — Write the state store and smoke-test it
- bash — Refactor the frontier to insertion order
- bash — Write the engine and strategies
- bash — Fix the frozen state and remove the dead stub
- bash — Write the water-jug problem and run the four strategies
- bash — Debug the engine loop
- bash — Fix the budget counting and MCTS applicability
- … et 46 autres

**Synthèse produite :**

⏵ Bilan des deux chantiers menés en parallèle

\## Les deux ont abouti, et chacun a sa leçon

\### 1. N2.i — le corpus élargi (GPU, 3 graines)

**Le dispositif.** Le dépôt courant (docs + journal + rapports) donne 1 308 documents, 6,39 Mo bruts ; la déduplication en retire 16,2 % → **4,84 Mo d'entraînement** (contre 3,24), **0 fuite** vérifiée. Même recette : professeur 23,57 M, base 11,47 M, distillation 20 000 pas × 3 graines.

| | N2.h (3,24 Mo) | N2.i (4,84 Mo) |
|---|---:|---:|
| validation (son corpus) | 3,0904 | **3,1278** |
| validation (ancien corpus) | 3,0904 | **3,6996** |
| littérature | 16,70 | **12,93** (−22 %) |
| anglais | 57,58 | **33,83** (−40 %) |
| wikitext2 | 56,88 | **35,53** (−38 %) |
| 256 octets | 14,11 | 14,28 |

**La lecture.** Le corpus du dépôt **n'est pas un levier de porte** : il dilue la prose (les rapports et les tableaux sont un autre registre), et la validation « domaine » ne se compare même plus entre les deux modèles. Mais sur des textes **identiques**, il **généralise fort** : anglais ÷1,7, littérature −22 %. C'est un levier de **lecteur** (R), pas de perplexité en domaine. Pour viser 2,5, il faut un corpus d'un autre ordre — du français réel en volume.

\### 2. Pensée v0 — le state store (CPU, en parallèle)

Pendant que les GPU tournaient, le contrat `moteur-de-pensee.md` a reçu son implémentation :

- **`coeur.py`** — types canoniques (`Candidat`, `Etat`, `Decision`), JSON sans flottant, empreinte **Merkle** des candidats triés : deux ordres d'insertion donnent la même empreinte.
- **`store.py`** — store content-addressed : `put/get/edge/children/frontier/compact/chemin`, plus `replay`, `diff` et `justification_valide`.
- **`moteur.py`** — boucle anytime (budget de nœuds, trace rejouable, décision justifiée) et quatre stratégies : BFS, greedy, A*, MCTS-lite.
- **`cruches.py`** — le jouet (3 L, 5 L, mesurer 4) avec l'heuristique **exacte** par BFS sur le graphe inversé — le piège étant que les opérateurs ne sont pas inversibles un pas pour un pas.
- **`autotest.py`** — **6/6 portes tenues**, chacune avec son contrôle négatif : store canonique, rejeu (93 événements), divergence de graine, stratégies substituables, anytime non décroissant, justification valide. BFS/A*/greedy trouvent `(3,4)` en 92 nœuds ; MCTS-lite échoue à 200 nœuds — **limite mesurée**, pas excusée.

\## Commits et état

- **`a20de579`** — Pensée v0 (state store + moteur + 6 portes)
- **`17ececfc`** — N2.i (corpus élargi, 3 graines, fiche + manifeste)
- *
… [957 caractères tronqués]

### Tour 8 — Est-on encore loin de pouvoir utiliser le système pour du vrai travail?

*4 appels d'outils.* Actions notables :

- bash — Find generation and end-to-end reports
- bash — Check the service and reader numbers
- bash — Read the reader numbers and a generation sample
- bash — Check the service tools and generation output

**Synthèse produite :**

⏵ Réponse appuyée sur les mesures du dépôt

\## La réponse courte

Pour du travail **étroit et mesuré** — lire un document, en extraire les tableaux, le code, les formules, retrouver un passage — les briques existent et tiennent leurs portes. Pour du travail **général** — écrire, répondre, suivre une consigne — on en est loin, et la distance n'est pas une question de finition : c'est encore une question de **nature du modèle**.

\## Ce qui marche déjà, avec ses chiffres

| capacité | état mesuré |
|---|---|
| OCR de scans | **4 familles sur 5 ≥ 90 %** de parité (propre 96,7 %, photocopie 93,3 %, photo 90,0 %, papier 90,0 %) ; fax 56,7 % — limite d'information nommée |
| tableaux | **92,6 %** de cellules exactes ; texte plat : 0/3 |
| code | **24/24** fichiers, 294 extraits |
| maths | **10/10** dérivées, 32 formules |
| colonnes | **89,4 % → 0,5 %** de WER ; ordre prouvé sur un lexique réel (15,3 % contre 98,0 %) |
| récupération | **1,000 à 30 %** du document, 249 questions, 5 types |
| bus et modèle natif | DRVM/DRVF, `drave-n0` 11,47 M, cache 19,25×, service minimal 69 octets / 611 ms |
| moteur de pensée | state store v0, **6/6 portes**, recherche tracée et rejouable sur petits problèmes |

C'est déjà utilisable **comme outil de numérisation structurée** : on peut lui donner un PDF scanné et récupérer des tableaux, du code et des formules avec un taux d'erreur connu. C'est étroit, mais c'est réel.

\## Ce qui ne marche pas, et qui bloque l'usage général

**1. Le modèle n'écrit pas.** L'échantillon de `drave-n0` sur « La France est un pays » :

> « La France est un pays de la couche 1 (le plafond de la porte de la couche 0 et le plus grand (le plus grand que le contexte de latinesplaronsesexinuiteuxin-cloraratesenouxitetrnsons »

Localement français, globalement du **saladier de mots**. Ce n'est pas un problème de réglage : à 11,47 M de paramètres et 5 Mo de texte, le modèle calcule des régularités locales, il ne **sait** rien. La PPL de 3,09 par octet (≈ 1,63 bit/octet) est deux fois moins bonne qu'un modèle de français utilisable (≈ 0,8–1,0 bit/octet), et surtout elle ne mesure pas la cohérence.

**2. La consigne ne tient pas.** SFT : **24/24 vus, 0/4 tenus**. Le modèle ne suit pas une instruction qu'il n'a pas vue — c'est le signe d'un modèle qui a mémorisé des formes, pas appris une tâche.

**3. La restitution n'existe pas.** Le lecteur sait **retrouver** un passage (récupération), pas encore le **lire** et le **redire** : R21 (le gist) et R31 (la rest
… [2367 caractères tronqués]

### Tour 9 — peut-on s'éloigner du modèle octet et modèle token pour aller vers un modèle qui voit la structure du texte en surface a … [169 caractères tronqués]

*7 appels d'outils.* Actions notables :

- bash — Measure the model on letter-scrambled text
- bash — Read the evaluation helpers
- bash — Check the byte loader
- bash — Fix the tensor conversion and run the scrambled-text test
- bash — Write the typoglycemia report and update the state
- bash — Commit the typoglycemia diagnostic
- job_output

**Synthèse produite :**

⏵ Réponse : mesurée, argumentée, et reliée à la vision du projet

\## D'abord la mesure, parce qu'elle tranche

J'ai pris le texte de validation et je l'ai mélangé de deux façons, à octets et longueur identiques :

| variante | PPL | ×propre |
|---|---:|---:|
| propre | **3,0555** | 1,0 |
| intérieur des mots mélangé (première et dernière gardées) | **54,2655** | **×17,8** |
| toutes les lettres mélangées | **191,4059** | **×62,7** |

**Le modèle actuel ne fait pas ce que fait l'humain : il lit des lettres.** L'effet dont tu parles — « je lis vite, l'ordre du milieu ne compte pas » — est un effet de **supériorité du mot** : un lexique de dizaines de milliers de mots, une prédiction top-down qui choisit le mot avant de le lire, et une forme globale (longueur + lettres extérieures). Ce modèle n'a ni lexique ni top-down : mélanger l'intérieur d'un mot détruit exactement ce qu'il exploite. La différence milieu/tout (×3,5) montre que les lettres extérieures portent encore un peu de signal — mais rien qui ressemble à une lecture par formes.

\## Oui, on peut s'en approcher — et c'est même trois idées distinctes

**1. Le mot comme forme apprise (micro).** Un encodeur qui représente un mot par un *pooling* de n-grammes de caractères (forme globale, ordre interne libre), avec des **positions relatives** entre mots. Le modèle voit un **ensemble de formes** et l'ordre vient d'un code de position relatif, pas absolu. C'est la version « mots d'abord, lettres ensuite » de ton intuition — et elle attaque directement le verrou que N2.h a mesuré : la position absolue (14,11 → 3,25 quand on la randomise).

**2. La page comme champ visuel (macro).** Les humains ne lisent pas une ligne : ils *balayent* une page en 2D. Le projet a déjà les briques de la structure de page — colonnes (89,4 % → 0,5 %), tableaux (92,6 %), ordre de lecture. Un encodeur qui voit la page comme un **champ de patchs** (positions 2D, régions) avant de linéariser est la version « surface » au sens propre. C'est ce que fait un ViT sur une image, et c'est cohérent avec ta lecture : la structure **avant** le flux de lettres.

**3. La saccade comme politique active (le lien avec la vision du projet).** Une saccade, c'est **lire ce qu'on regarde, pas tout le texte** : 4 à 5 fixations par seconde, 7 à 9 lettres par fixation, et l'intégration se fait dans un état. C'est exactement le principe du projet — *le coût du calcul proportionnel à l'activité* : un modèle qui **échantillonne** des fenêtres de mots au lieu 
… [2608 caractères tronqués]

### Tour 10 — en tant que programmeur, j'apprécie la coloration du code, syntaxe et structure indentée. On pourrait imaginer un outil  … [343 caractères tronqués]

*4 appels d'outils.* Actions notables :

- bash — Find the RSN parser and semantic layer
- bash — Check for existing coloring or role concepts
- bash — Read the universal semantics schema
- bash — Sketch a French syntax highlighter

**Synthèse produite :**

⏵ Réponse : l'idée, sa forme concrète, et comment la tester

\## L'idée est juste — et elle a déjà un statut dans le projet

Ce que tu décris est exactement un **bloc classique** au sens de Drave : déterministe, auditable, rejouable, pas cher, et qui rend visible une structure que le modèle neuronal, lui, devrait deviner. Le parallèle avec l'IDE est profond : la coloration syntaxique ne rend pas le compilateur plus intelligent, elle rend **la structure lisible pour celui qui lit**. Pour un modèle, l'équivalent n'est pas cosmétique : c'est un **prior**.

Et le dépôt a déjà la moitié de la matière : les **universaux RSN** (types, rôles, cas), le **codec B11** (449 surfaces), la structure de **page** (R4.4 : colonnes, tableaux, ordre de lecture). Ce qui manque est exactement le niveau que tu décris : **la phrase**.

\## À quoi ça ressemble (esquisse d'aujourd'hui)

J'ai écrit un v0 de 40 lignes (`work/n2i/coloration.py`) : il colore les mots grammaticaux contre les mots pleins et indente les propositions aux frontières (virgule + subordonnant) :

```
┌─ Le chat noir,
├─ qui dormait sur le toit,
├─ se réveilla quand la pluie tomba,
└─ et il rentra parce que la nuit était froide.
```

C'est une esquisse, pas un analyseur — mais elle montre les trois couches qu'un vrai outil devrait porter :

| couche | ce qu'elle colore | l'équivalent en code |
|---|---|---|
| **lexicale** | mots grammaticaux / mots pleins, temps et personne | les mots-clés contre les identifiants |
| **syntagmatique** | GN, GV, GP, propositions (indentation) | les blocs et l'indentation |
| **actancielle** | rôles RSN : agent, patient, but, lieu, instrument | les types et les signatures |

La troisième est la vraie différenciation : spaCy, Stanza ou displaCy colorient des **POS** ; personne ne colorie des **rôles sémantiques** avec une palette **cross-lingue**. Les universaux du projet permettent exactement ça : le même agent est de la même couleur en français, en anglais et en latin — c'est ça, l'outil dont un apprenant a besoin : voir la **charpente** avant la traduction.

\## Les sorties

- **ANSI** : le terminal, pour l'apprenant.
- **HTML** : les couches activables (voir / masquer les rôles, mode examen).
- **SVG** : les arcs de dépendance, comme un AST — et le projet sait déjà faire des SVG propres.
- **Linéarisé** : `<GN>le chat</GN> <GV>dort</GV>` — le format qui sert au modèle.

\## Les deux usages, et ils ne se testent pas pareil

**Pour l'apprenant** : la qualité se juge sur la **couver
… [2794 caractères tronqués]

### Tour 11 — allons-y, mais créons d'abord un outil pour humain dans un projet distinct (submodule git) qui permet d'afficher en web  … [308 caractères tronqués]

*25 appels d'outils.* Actions notables :

- bash — Check the environment for the sub-project
- bash — Create the structures repository with seed data
- bash — Build the seed data with verified spans
- bash — Write the LLM evaluation module and test the baseline
- bash — Add explicit attachment targets to the candidates
- bash — Fix the baseline heuristic with attachment targets
- bash — Write the HTTP server
- bash — Write the web interface
- bash — Write and run the tests
- bash — Test the running server end-to-end
- bash — Write the README and commit the sub-project
- bash — Add the tool as a git submodule
- bash — Retry the submodule with the file transport allowed
- bash — Add the structures tool to the state
- … et 11 autres

**Synthèse produite :**

⏵ Bilan : le banc de structures est en place, testé et branché

\## Ce qui existe maintenant

**Un sous-projet autonome** — `drave-structures` — monté dans le dépôt principal comme **submodule** : `tools/structures` (commit `ccb1006`, dépôt local `../drave-structures` ; un remote pourra être ajouté pour le rendre portable).

**Une interface web sans aucune dépendance** (stdlib : HTTP, JSON, `urllib`), qui montre pour chaque phrase **plusieurs structures d'interprétation candidates** :

- la phrase **colorée par type de segment** — GN, GV, GP, REL, SUB, PHRASE ;
- les **blocs indentés** par profondeur d'attachement — l'indentation *est* la structure ;
- l'**attachement explicite** : `qui dort → le chat` contre `qui dort → la voisine` ;
- une **lecture en français courant** pour chaque candidat ;
- trois verdicts — **✓ acceptable / ~ discutable / ✗ non** — avec une note libre.

**Le geste central est la validation humaine.** Chaque verdict s'ajoute à `donnees/validations.jsonl` (append-only, jamais réécrit). L'export `/api/export` ne garde que les candidats **acceptés** et rend **une ligne JSONL par structure** — la banque, prête à devenir un corpus d'entraînement.

**Le grand modèle est branché** : `llm.py` appelle l'API DeepSeek (`chat/completions`, température 0) et demande un JSON `{choix, justification, confiance, ambigu}`. **Sans clé, on ne simule pas** : la **baseline** locale — *attachement à la cible la plus proche*, une heuristique explicable — est rendue et le mode est marqué `sans-clé`. C'est le témoin auquel comparer humains et grand modèle.

\## Le contenu v0

**6 phrases, 12 candidats, 6 ambiguïtés réelles** : relative (`qui dort`), GP (`avec le télescope`, `dans le parc`), portée (`hier`), rôle (`pour`), possession (`son projet`). Les spans sont **vérifiés par sous-chaîne** (`construire_donnees.py`) — un segment qui n'apparaît pas dans la phrase est refusé, pas deviné.

\## Lancer et tester

```bash
python3 tools/structures/serveur.py          # http://127.0.0.1:8765
export DEEPSEEK_API_KEY=sk-…                 # pour l'évaluation par le grand modèle
cd tools/structures && python3 -m unittest discover -s tests   # 5 tests, OK
```

Tests : alignement des spans, validation + export, verdict invalide refusé, baseline, page statique.

\## L'intégration au projet

- La ligne **S — les structures** entre au plan : `v0 (outil web)`, prochaine action « générer les candidats par un analyseur, brancher l'export au corpus d'entraînement ».
- L'état la menti
… [837 caractères tronqués]

### Tour 12 — lance le serveur et continue

*18 appels d'outils.* Actions notables :

- bash — Launch the structures server in the background
- bash — Write the candidate generator and test it
- bash — Fix the classifier and clause boundaries
- bash — Add PP-head and adverb handling to the generator
- bash — Fix the slots and retest the generator
- bash — Rewrite the candidate generator with role ambiguity
- bash — Write and run the generator tests
- bash — Integrate the generator into the server and UI
- bash — Test the generate-validate-export loop end-to-end
- bash — Diagnose the /api/ajouter failure
- bash — Commit the generator in the sub-project
- bash — Update the submodule checkout to the new commit
- bash — Test the full generate-validate-export loop
- bash — Clean the demo artifacts and update the plan
- … et 4 autres

**Synthèse produite :**

⏵ Serveur en ligne ; le générateur de candidats est branché et testé

\## Le serveur tourne

**http://127.0.0.1:8765** — 6 phrases, 0 validation, données propres. Pour l'arrêter : `fuser -k 8765/tcp` ; pour le relancer : `python3 tools/structures/serveur.py`. Sur le réseau local : `--hote 0.0.0.0`.

\## Ce que j'ai ajouté depuis le lancement : le générateur

Le banc ne se contente plus de phrases écrites à la main — **il analyse** :

- **Segmentation** par lexique de mots grammaticaux et règles de frontière : GN, GV, GP, REL, SUB ;
- **Rôles devinés par la préposition** : lieu, temps, but, moyen, thème, destinataire ;
- **Attachements candidats** : pour un GP ou une relative, il propose la tête du GP, le GN et le GV — exactement les ambiguïtés qui comptent ;
- **Rôles ambigus** : `pour` → but *ou* cause, `avec` → moyen *ou* attribut, `de` → thème *ou* possession.

**La boucle est complète** : on tape une phrase, `POST /api/ajouter` génère et persiste les candidats, on valide (✓ / ~ / ✗), et l'export ne garde que les acceptés. Vérifié de bout en bout :

> « Le chien du voisin qui aboie la nuit réveille tout le quartier. » → **2 candidats** (`→ voisin`, `→ Le chien`), validation acceptée, export JSONL correct.

**Dix tests passent** (cinq serveur, cinq générateur) : alignement des segments, deux lectures de la relative, rôle `pour` ambigu, deux lectures du GP, et l'invariant **« une seule variation par candidat »**.

\## L'état

- Sous-projet `drave-structures` : commit **`a407095`** (générateur + intégration + tests).
- Dépôt principal : commit **`0ca545eb`** (pointeur du submodule + ligne S).
- `tools/structures` est **propre** ; les seuls changements restants dans l'arbre sont ceux de l'autre session.
- Vérifications : revue ✅, état ✅, **T0 3 646 / 4 000**, journal ✅.

\## À quoi ça sert, concrètement

1. **Voir** : la phrase colorée par type, les blocs indentés par profondeur, l'attachement affiché — la charpente avant la traduction.
2. **Trancher** : l'humain valide les lectures ; chaque ✓ devient une ligne de la banque.
3. **Comparer** : le bouton « interroger le modèle » oppose la baseline (attachement le plus proche) — et DeepSeek dès que `DEEPSEEK_API_KEY` est exportée, sans simulation.
4. **Grandir** : le générateur permet d'ingérer n'importe quelle phrase, pas seulement les six écrites à la main.

\## La suite immédiate

- **Enrichir l'analyseur** : subordonnées (que/parce que), coordination, pronoms objets — les cas où le générateur se trompe aujourd'
… [312 caractères tronqués]

### Tour 13 — Les phrases présentées sont ambigues et ne peuvent être résolues hors contexte, même par un humain. En contexte, cette a … [128 caractères tronqués]

*16 appels d'outils.* Actions notables :

- bash — Add the pragmatic statuses to the server
- bash — Rewrite the LLM client with context and pragmatic statuses
- bash — Update the UI for context and pragmatic statuses
- bash — Update the tests for pragmatic statuses
- bash — Add a humorous ambiguity to the seed data
- bash — Update the tests and README for the pragmatic layer
- bash — Commit the pragmatic layer in the sub-project
- bash — Update the submodule and test the pragmatic loop
- bash — Clean the demo and update the plan for the pragmatic layer
- bash — Find the current S bullet
- bash — Replace the S bullet with the pragmatic version
- bash — Commit the pragmatic layer integration
- job_output
- bash — Restart the server cleanly and run the final checks
- … et 1 autres

**Synthèse produite :**

⏵ Le niveau pragmatique est en place, vérifié de bout en bout

\## Le point était juste, et il a changé le modèle de l'outil

Les phrases du banc étaient ambiguës **par construction** — c'était le but : exposer des lectures concurrentes. Mais forcer un verdict unique par candidat est le mauvais geste : hors contexte, personne ne peut trancher, et en contexte l'ambiguïté peut être **voulue**. L'outil enregistre donc désormais un **statut pragmatique**, pas une vérité.

\## Ce qui a changé

| avant | maintenant |
|---|---|
| ✓ acceptable / ~ discutable / ✗ non | **résolu** / **compatible** / **exclu** / **⇄ double sens** |
| pas de contexte | un **champ de contexte** libre par phrase, enregistré avec chaque verdict |
| export = candidats acceptés | export = **lectures conservées**, avec statut, contexte et **groupe** |
| LLM = un choix | LLM = une **liste de lectures** + une **intention** (sérieux / humour / ambigu) |
| baseline = un choix | baseline **aveugle au contexte** — le témoin qui montre ce que coûte l'absence de pragmatique |

**Le double sens se conserve.** Deux lectures marquées « double sens » sortent ensemble, avec le même `groupe` (`p007-double`) : l'ambiguïté intentionnelle est un **fait** à conserver, pas un défaut à trancher.

**Une phrase pour l'incarner** : « Le canard est prêt à manger. » — le canard est cuit (patient) ou il a faim (agent). Vérifié de bout en bout : deux validations `double_sens` sur `p007` avec un contexte → **export 2 lignes, groupe `p007-double`, contexte conservé**.

\## L'état

- Sous-projet : commit **`7366191`** (pragmatique + contexte + export groupé) ; **11 tests** passent (6 serveur, 5 générateur), dont le groupe double sens et le contexte.
- Dépôt principal : **`5a5915a5`** (pointeur + plan) et **`1145834c`** (compteurs).
- **Serveur en ligne** : http://127.0.0.1:8765 — 7 phrases, 0 validation, sous-module propre.
- Vérifications : revue ✅, état ✅, **T0 3 743 / 4 000**.

\## Ce que ça relie dans le projet

Ce n'est pas un détail d'interface : c'est la **RSN plurielle** appliquée à l'interprétation. Un sens n'est pas un parse unique mais un **état à plusieurs lectures**, chacune avec un statut ; le contexte est ce qui **décide**, et quand l'intention est humoristique, la décision est de **garder les deux**. C'est exactement ce que le moteur de pensée v0 sait représenter (états pluriels, justification, trace) — et le corpus qui en sort est rare : des **lectures doubles validées avec leur contexte**, ce qu'aucun corp
… [734 caractères tronqués]

### Tour 14 — ça va prendre des contextes plus larges pour trancher sur les interprétations ambigues.

*15 appels d'outils.* Actions notables :

- bash — Add example contexts at different levels
- bash — Add context levels and the minimal level metric to the server
- bash — Add the context level to the LLM prompt
- bash — Update the UI with context levels
- bash — Test the context levels and minimal level
- bash — Read the failing test
- bash — Fix the JSON key access in the test
- bash — Commit the context levels in the sub-project
- bash — Update the submodule and test the level flow
- bash — Inspect the validation journal
- bash — Update the plan for context levels
- bash — Find the current S roadmap line
- bash — Fix the S line and commit the context levels
- job_output
- … et 1 autres

**Synthèse produite :**

⏵ Oui — et le banc mesure maintenant **combien** de contexte il faut

\## Le contexte est devenu gradué

| niveau | ce qu'on donne | exemple du banc |
|---|---|---|
| 0 | rien | la phrase seule |
| 1 | la phrase d'avant | « Il a couru. » |
| 2 | le paragraphe | « La voisine est partie ; son chat est resté sur le toit. » |
| 3 | la section, le document | « Dans ce dessin animé, le canard parle… » |
| 4 | le genre, le registre | fable, fait divers, slogan |

Chaque verdict enregistre **son niveau** et le texte du contexte. L'outil en déduit le **niveau minimal** : le plus petit niveau où une lecture a été **tranchée** (résolue ou exclue). C'est la mesure exacte de ta remarque — « il faut des contextes plus larges » — transformée en chiffre.

**Vérifié en direct** : p001 (« Le chat de la voisine qui dort… ») tranché au **niveau 2** avec le paragraphe ; les deux autres phrases déjà tranchées l'ont été au **niveau 0** (leur phrase suffisait). L'export porte `niveau_contexte`.

\## Ce qui est branché

- **Interface** : un sélecteur de niveau + un textarea par phrase, préremplis avec un **contexte d'exemple** (p001 et p002 au paragraphe, p007 au document) ; un badge « tranché au niveau N » par phrase.
- **Grand modèle** : il reçoit le niveau et le contexte, et rend un `niveau_requis` — la comparaison directe entre « ce qu'il lui faut » et « ce qu'il a fallu à l'humain ».
- **Export** : chaque lecture conservée porte son `niveau_contexte` ; la banque devient un corpus de **(phrase, contexte, niveau, verdict)**.

\## L'état

- Sous-projet : **`733b1a4`** — 12 tests passent, dont le niveau minimal.
- Dépôt principal : **`8aaa3c13`** — pointeur + plan à jour.
- **Serveur en ligne** : http://127.0.0.1:8765 — 7 phrases, **8 validations** (dont les tiennes : double sens sur p001/p002, résolu/exclu sur p003, résolu sur p004 ; plus une ligne de test que j'ai ajoutée sur p001 au niveau 2 — la dernière l'emporte à l'affichage, l'historique garde tout).
- Revue ✅, état ✅, **T0 3 746 / 4 000**.

\## Le point qui compte pour le modèle

Il y a deux « contextes » dans cette histoire, et il ne faut pas les confondre :

1. **Le contexte du juge** (humain ou grand modèle) — c'est ce que le banc gradue et mesure.
2. **Le contexte du modèle** — `drave-n0` voit **256 octets**. Même avec un juge parfait, un modèle qui ne lit que 256 octets ne peut pas utiliser un paragraphe. C'est **R1** (la fenêtre), et la mesure du niveau minimal dit précisément **de combien** il faudra l'agrandir : si l
… [276 caractères tronqués]

### Tour 15 — peux-tu comencer l'entrainement avec des phrases non ambigue et étudier les effets  sur la qualité du bloc linguistique.

*59 appels d'outils.* Actions notables :

- bash — Measure the unambiguous subset of the clean corpus
- bash — Build the unambiguous and control corpora and launch two bases
- bash — Read the data inventory report
- bash — Inspect the paired Wikipedia corpus
- bash — Locate the Wikipedia data on disk
- job_output
- bash — Inspect the French Wikipedia text files
- bash — Check the actual file sizes per language
- bash — Inspect the local Wikipedia data
- bash — List the Wikipedia databases and dumps
- bash — Inspect the French Wikipedia sqlite schema
- bash — Sample the French Wikipedia text
- bash — Extract 120k French Wikipedia articles
- bash — Deduplicate and split the Wikipedia corpus
- … et 32 autres

**Synthèse produite :**

⏵ Résultat : le corpus réel tient ses promesses, le filtre non ambigu non

\## Ce qui a été fait

J'ai utilisé l'inventaire : la base FR de Wikipédia (`data/wikipedia/db/frwiki_v14.db`, 7,25 Go) contient **2,76 M d'articles** et **7,0 Go de texte**. J'en ai extrait **120 000 articles** (237,5 Mo bruts), dédupliqué par shingles (−13,0 %) → **186,1 Mo d'entraînement**, 10,3 de validation, 10,3 de test, **0/100 fenêtres contaminées**. Puis la base 11,47 M, 20 000 pas, recette identique à N2.h.

\## Le bloc linguistique sur du vrai français

| base | val (son corpus) | val du dépôt | littérature | anglais | wikitext2 | 256 octets |
|---|---:|---:|---:|---:|---:|---:|
| dépôt (3,24 Mo) | 3,2402 | 3,2402 | 12,29 | 32,90 | 33,29 | 11,72 |
| **wiki (186 Mo)** | 4,0284 | 6,7194 | **7,42** | **12,41** | **13,91** | **9,28** |

**×1,7 en littérature, ×2,65 en anglais, ×2,4 sur wikitext2** — à recette et budget identiques. Sur le dépôt, 6,72 : c'est le décalage de domaine (le wiki est encyclopédique, le dépôt est de la prose de projet). Le corpus réel est bien **le levier hors domaine** que N2.i annonçait.

\## Le filtre « phrases non ambiguës » — essayé, mesuré, négatif

- Il garde **29,8 %** des phrases du dépôt et **15,4 %** d'un échantillon de 200 000 phrases de wiki — et ce sont les **courtes** (55 caractères contre 153).
- À taille égale (345 Ko, même recette) : **non ambigu 11,81** contre **témoin aléatoire 10,11** sur la validation du dépôt — le filtre **transfère moins bien** que le hasard. (Les deux sont de toute façon très loin de la base pleine à 3,24 Mo : à cette taille, le volume domine tout.)
- En **curriculum** — 2 000 pas sur le non ambigu puis 18 000 sur le wiki — il **dégrade légèrement les cinq mesures** : 4,05 contre 4,03, 7,57 contre 7,42, 13,05 contre 12,41, 6,78 contre 6,72.

**La conclusion** : retirer l'ambiguïté du texte, c'est retirer du signal. Si la structure doit aider, elle doit être **ajoutée** au texte — un canal d'annotation par octet — et non retirée. C'est exactement l'expérience E2 que la discussion avait posée, et elle a maintenant un corpus digne de ce nom : 186 Mo.

\## L'état

- **`c96eb475`** — fiche `reports/rapport-n2-corpus-reel.md`, manifeste `reports/corpus-wiki-propre.json`, `--init` ajouté au trainer (curriculum).
- Points de contrôle : `work/n2j/` (5 bases) ; corpus : `data/wiki_fr/` (424 Mo, non versionné).
- Vérifications : revue ✅, état ✅, **T0 3 811 / 4 000**, journal ✅. **Serveur du banc toujours en ligne** (HTTP 200
… [781 caractères tronqués]

### Tour 16 — continue avec de trèes gros corpus multilingues

*34 appels d'outils.* Actions notables :

- bash — List the Wikipedia language bases and GPU status
- bash — Extract 10-language Wikipedia articles
- bash — Extract the multilingual Wikipedia corpus
- bash — Build and deduplicate the multilingual corpus
- bash — Re-extract from a different page range to avoid overlap
- bash — Rebuild the multilingual corpus and deduplicate
- bash — Write the per-language evaluation script
- bash — Wait for the multilingual dedup
- job_output
- bash — Check contamination per language and launch the multilingual base
- bash — Evaluate the monolingual French base on all ten languages
- bash — Wait for the multilingual base training
- bash — Check the multilingual training progress
- bash — Wait for the multilingual base to finish
- … et 14 autres

**Synthèse produite :**

⏵ Résultat : dix langues entraînées, et la dilution mesurée séparément de l'effet de données

\## Ce qui a été fait

**Dix langues** extraites des bases sqlite locales (fr, en, de, es, it, pt, ru, ar, ja, zh), **11 000 articles chacune** (page_ids 200 000+, disjoints de N2.j), entrelacées par chunks de 8 Ko pour que chaque langue soit partout : **275,5 Mo bruts → 237,0 Mo** d'entraînement après déduplication, **0/60 fenêtres contaminées par langue**. Une base 11,47 M, 20 000 pas, recette N2.h.

Et le contrôle qui sépare la **dilution** de l'**effet de données** : la même base entraînée sur les **21 Mo de français seuls** du corpus (sans les 9 autres langues).

\## Les mesures

| langue | FR seul (186 Mo) | FR seul (21 Mo) | **10 langues** | écart multi / FR 21 Mo |
|---|---:|---:|---:|---:|
| **fr** | 3,7633 | 3,6230 | **5,6842** | **+57 %** |
| en | 11,0366 | 10,9509 | **6,3024** | −42 % |
| de | 16,3009 | 17,5431 | **6,5047** | −63 % |
| es | 13,0054 | 13,3105 | **6,0866** | −54 % |
| it | 13,6259 | 13,8877 | **6,0605** | −56 % |
| pt | 15,2688 | 15,9746 | **6,8002** | −57 % |
| ru | 10,7419 | 8,3772 | **3,6809** | −56 % |
| ar | 13,0103 | 16,5414 | **3,6064** | −78 % |
| ja | 53,8382 | 43,5327 | **5,7423** | −87 % |
| zh | 85,0273 | 107,8443 | **9,6509** | −91 % |

**La lecture.** Le français paie **+0,65 bit/octet** — et ce n'est pas un manque de données : à 21 Mo de français seuls, la base vaut **3,62**, *mieux* que les 186 Mo (3,76) sur cette validation. C'est donc bien la **dilution** : dix langues partagent 11,47 M de paramètres. En face, les gains sont énormes : anglais ÷1,7, allemand ÷2,7, japonais ÷7,6, chinois ÷11,2 — les écritures non latines, que la base française ne lisait pas du tout, deviennent lisibles.

Sur les jeux externes français (littérature, anglais, wikitext2), le multilingue vaut **8,81 / 7,05 / 7,34** contre 7,42 / 12,41 / 13,91 pour la base française : il perd en français, il gagne largement en anglais.

\## Ce que ça dit pour le projet

- **Pour la porte N2**, la base française seule reste la référence : à 11,47 M, on ne peut pas être à la fois précis en français et polyglotte.
- **Pour la ligne R** (lire des documents dans dix langues), c'est un levier direct : un lecteur n'a pas besoin d'un français au bit près, il a besoin de lire dix langues.
- **La question ouverte est une loi d'échelle** : combien de langues par million de paramètres ? Elle se mesure en refaisant tourner les trois bases à 21,65 M (le bras capacité de N2.h5 
… [771 caractères tronqués]

### Tour 17 — lire docs/pilotage/plan-travail.md et avancer

*35 appels d'outils.* Actions notables :

- bash — Read the work plan
- bash — Read the batch sampler and the position support
- bash — Read the native model forward
- bash — Add position randomization and train the wiki base with it
- bash — Declare the new work directories in the N2 territory
- bash — Wait for the position-randomized wiki base
- job_output
- bash — Check the position-randomized training
- bash — Wait for the position-randomized base to finish
- bash — Evaluate the position-randomized wiki base
- bash — Write the length report and launch the capacity arm on the real corpus
- bash — Update the plan with the length result and check the capacity run
- bash — Trim the state under budget
- bash — Read the N2 bullet in full
- … et 14 autres

**Synthèse produite :**

⏵ Plan lu, action N2 avancée : verrou de longueur et capacité sur le corpus réel

\## Ce que le plan demandait à la session N2

> « N2 sur les corpus wiki fr/en ; le verrou 129→512 ; la capacité »

Le wiki FR est fait (N2.j), l'anglais est couvert par le multilingue (N2.k). Restaient **le verrou** et **la capacité** — les deux sont faits, sur 186 Mo de Wikipédia.

\## Le verrou de longueur tombe encore (N2.j2)

Même base, mêmes 186 Mo, avec des **positions tirées dans [0, 384]** :

| | 129 | 192 | **256** | 384 | **512** | val | littérature | anglais |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| positions fixes | 4,07 | 7,07 | **9,28** | 11,85 | **13,37** | 4,03 | 7,42 | 12,41 |
| positions 0–384 | 4,39 | 4,37 | **4,49** | 5,05 | **5,67** | 4,39 | 7,90 | 13,72 |
| | +8 % | **−38 %** | **−52 %** | **−57 %** | **−58 %** | +9 % | +6 % | +11 % |

Le verrou n'était pas une propriété du petit corpus : **il est architectural**, et la randomisation le lève à l'échelle — pour +0,36 en domaine. C'est le second résultat qui se transporte, après le corpus réel lui-même.

\## La capacité paie — quand les données suivent (N2.j3)

| modèle | val wiki | littérature | anglais | 512 | val du dépôt |
|---|---:|---:|---:|---:|---:|
| 11,47 M | 4,3893 | 7,90 | 13,72 | 5,67 | 7,11 |
| **21,65 M** | **4,2013** | **7,46** | **13,55** | **5,03** | **6,88** |

Sur 3,24 Mo, N2.h5 ne gagnait que **−0,06** et rien hors domaine. Sur 186 Mo, le même doublement donne **−0,19** et un gain **partout**. C'est une **interaction données × capacité** : un modèle plus gros a besoin de plus de texte pour amortir ses paramètres. La taille se choisit **après** le corpus — le prochain palier (40–50 M) ne se justifiera qu'avec quelques centaines de Mo de plus.

\## L'état et les voisins

- **`4db5aac0`** (N2.j2), **`1520b875`** (N2.j3) ; fiches `rapport-n2-longueur-reelle.md` et `rapport-n2-capacite-reelle.md`.
- Le **plan de travail** a été mis à jour : le territoire N2 déclare désormais `work/n2j/`, `work/n2k/`, `data/wiki_*`, `reports/rapport-n2-*` et `tools/entrainer_native.py` — les fichiers que j'écris réellement.
- Vérifications : revue ✅, état ✅, **T0 3 995 / 4 000**, plans cohérents ✅, serveur du banc toujours en ligne.
- Les autres sessions avancent en parallèle : **D** a extrait le texte intégral de Wikipédia (pilote FR, 100 000 articles, 1,082 Go, 0 fuite) ; **L** a ajouté AC-3 et alpha-bêta au moteur de pensée (8/8 portes).

\## Ce qui reste à N2

1. **La distillation sur le corpus réel*
… [515 caractères tronqués]

### Tour 18 — suis le plan, continue jusqu'à 8h demain matin

*238 appels d'outils.* Actions notables :

- create_goal
- get_goal
- update_goal
- bash — Launch the teacher on the real corpus
- bash — Check the teacher launch
- bash — Write the structure channel tool and test its speed
- bash — Fix the canal regex and check the teacher
- bash — Check the teacher process
- bash — Add the channel to the model and the trainer
- bash — Compute the structure channel for the wiki corpus
- job_output
- bash — Check the canal files and the teacher
- bash — Check the processes and output files
- bash — Run the canal computation directly on the validation file
- … et 159 autres

**Synthèse produite :**

⏵ Mémoire libérée : je lance la loi d'échelle — capacité 45 M en français, 21,65 M en multilingue

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/distiller_budget.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/plan.md` | 3 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md` | 0 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/n2d/evalue-final.py` | 2 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/n2d/agrege.py` | 3 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/n2d/robustesse.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/n2d/fiche.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/eval_n2_budget.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/n2d/journal-notes.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/corpus_propre.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/eval_n2_propre.py` | 1 | 0 |

### Commandes exécutées (échantillon)

- **T1** Show git status and recent commits
- **T1** Check state file sizes and recent journal
- **T1** Inspect uncommitted changes
- **T1** Check session status
- **T1** Check today's journal files
- **T1** Find N2 section in roadmap
- **T1** Read roadmap N2 details
- **T1** List N2 reports and tooling
- **T1** Find curriculum references and distiller scripts
- **T1** Check GPU availability
- **T1** Read R12 curriculum backlog card
- **T1** Read distillation script header
- **T1** Check original distillation script for curriculum
- **T1** Read original distillation report
- **T1** Locate the 2.6998 result and ctx129 report
- **T1** Find capacity result at 21.63M
- **T1** List corpus sources
- **T1** Read capacity reports
- **T1** Find 4-source distillation recipe
- **T1** Check archived checkpoints
- **T1** Read multi-source corpus report
- **T1** List archived artefacts and read backup README
- **T1** Read distillation training loop
- **T1** Inspect multi-source manifest
- **T1** Read native model config
- **T1** Read historical protocol JSON
- **T1** List native reports
- **T1** Find reports using multi corpus
- **T1** Read multi-source distillation report
- **T1** List all native PPL results sorted
- **T1** Inspect the best chain checkpoints
- **T1** Find multi-source corpus consumer
- **T1** Read native corpus builder
- **T1** Check gitignore and GPU environment
- **T1** Locate the GPU Python environment
- **T1** Verify GPU env at home
- **T1** Read campaign checkpoint notes
- **T1** Compute historical-protocol PPL for archived checkpoints
- **T1** Read model forward and VDC helpers
- **T1** Fix window shapes in campaign script
- … et 928 autres

## 4. Mesures et résultats marquants

- **T1** `4442c64c N2 — L'ÉTAT DE SECTION NE SE DISTINGUE PAS D'UN ÉTAT ÉTRANGER (+0,36 % CONTRE +0,37 %)`
- **T1** `21a361f9 R13.4 — DEUX GRAINES : BPE512 DANS LE BRUIT, BPE1024 PERD 4,09 %`
- **T1** `85:[N2] lasts 4 days and is 30% complete and is colored in #b26a00`
- **T1** `30 % sur 5 types et **249 questions**) ; **R0.4** (tête de survol) et **R0.5** (routeur) sont`
- **T1** `611 ms. La restitution depuis un document lu est **R31**.`
- **T1** `suivante, jamais l'attente. **N5 est gelé** jusqu'au verdict de R11 sur le contexte ; B10.3 attend un **z qui porte** : l'objectif mot a levé le décodeur (32,5 ; **26,7 sur JW, au-dessus du plancher 1`
- **T1** `| **N1** | `drave-n0` : 11,47 M, 6 blocs, octets, attention locale, FFN creux, 3 têtes précoces | ✅ | aucune — PPL **3,465** avec pont (**4,080** sans) ; têtes **57,6 / 61,6 / 62,1 %** contre **62,7 %`
- **T1** `2. **Le saut de calcul existe, le saut de contenu n'existe pas.** La sortie précoce gagne **24,05 %** de temps en`
- **T1** `Quadro RTX 5000, 16384 MiB, 1 MiB, 0 %`
- **T1** `/dev/mapper/system-root   11T  8,9T  2,0T  82% /home/stephane/Data13TB`
- **T1** `- Corpus : `data/corpus_fr_train.txt` ; validation : derniers 5 %.`
- **T1** `| **gain** | **−4,85 %** |`
- **T1** `- La distillation **améliore** le student de **4,85 %** sans changer son architecture.`
- **T1** `| précision principale | 72,80 % | **72,40 %** |`
- **T1** `| tête 3 | 72,60 % | **72,53 %** |`
- **T1** `| latence service 53 octets | **650,1 ms** |`
- **T1** `- **650 ms** pour 53 octets : le service paie le cache par requête, pas la qualité.`
- **T1** `**N0.15/N4.7 — meilleur student servi** : PPL **2,6998**, parité native, **650 ms**, texte plus`
- **T1** `# N2.5b — capacité à budget égal : 21,63 M bat 11,47 M de 4,1 %`
- **T1** `| **écart moyen** | — | **−8,1 %** |`
- **T1** `| précision principale (moyenne) | **59,23 %** | **60,16 %** |`
- **T1** `| tête 3 (moyenne) | **57,13 %** | **57,81 %** |`
- **T1** `- À **budget égal** et **initialisation égale**, le modèle plus gros est **meilleur de 8,1 % en moyenne**`
- **T1** `- Les précisions sont **proches** (59,1 % vs 58,8 %) : le gain de PPL ne se voit pas encore en top-1.`
- **T1** `**N2.5b — capacité : positif** (−8,1 % de PPL à budget égal sur trois graines), **mais le prior`
- **T1** `| précision principale | 67,96 % | **66,80 %** |`
- **T1** `| tête 3 | 68,01 % | **65,43 %** |`
- **T1** `- **Plus gros, toujours moins bon** : **3,381** contre **3,123**, soit **+8,3 %**.`
- **T1** `- La tête 1 reste faible (**34,7 %**) : les premières couches du gros modèle ne sont pas assez`
- **T1** `49 999 fenêtres, 4 sources ; professeur 30k 1,734 (0,794 bit/octet) ; student 3,123 à 20 000 pas ; meilleur 2,6998 ; plateau 2,708. Le 21,63 M à budget égal donne −8,1 %, mais à 20 000 pas il est pire`
- **T1** `| `corpus_fr.txt` | 4,63 Mo, 72 403 fenêtres possibles |`
- **T1** `| `udhr_train.txt` | 4,38 Mo, 68 433 |`
- **T1** `| `corpus_en.txt` | 100,28 Mo, 1 566 813 |`
- **T1** `| `corpus_mixte_litt.txt` | 12,23 Mo, 191 143 |`
- **T1** `- Quotas **équilibrés** : l'anglais, 100 Mo, est sous-représenté par rapport à son volume.`
- **T1** `| `artefacts/route-teacher-20k/` | 90 Mo | professeur byte-level 23,57 M, 20 000 pas, 0,9195 bit/octet (dossier HF) |`
- **T1** `| `artefacts/drave-n0-base-20k.pt` | 46 Mo | élève de base, 20 000 pas, PPL 3,2064 |`
- **T1** `| `artefacts/{temoin,hierarchie,controle}-g{1,2,3}.pt` | 9 × 47 Mo | les neuf points de contrôle de la distillation |`
- **T1** `| `artefacts/*.pt.drvm` | 9 × 47 Mo | exports DRVM des mêmes points (lecture par le moteur) |`
- **T1** `distillation 3 bras × 3 graines, 5 000 pas, lot 8, 4 segments de 128, lr 1e-4, T=2, α=0,7.`
- **T1** ``/home/stephane/Data13TB/stephane/backups/qtrinet/qtrinet-2026-10-31.bundle` (31 Mo, historique`
- **T1** `- Corpus : `data/corpus_multi_train.txt` (115,4 Mo) ; validation 6,08 Mo.`
- **T1** `| précision principale | — | **36,34 %** |`
- **T1** `| têtes précoces | — | **30,10 / 34,08 / 36,83 %** |`
- **T1** `- **Écart student − professeur** : **-0.055** de PPL (**-0.6 %**).`
- **T1** `- La **précision** tombe à **36,3 %** : le multi-sources est un autre problème.`
- **T1** `| précision principale | 72,62 % | **72,80 %** |`
- **T1** `| tête 3 | 72,69 % | **72,60 %** |`
- **T1** `- La précision monte à **72,80 %** ; la tête 3 recule légèrement à **72,60 %**.`
- **T1** `3 bras (temoin, hierarchie, controle) × 3 graines, 5 000 pas, lot 8, 4 segments de 128`
- **T1** `(= 20,48 Mo vus par run), lr 1e-4, T=2, alpha=0,7, distillation + CE + têtes.`
- **T1** `(4×128, état transporté). Elles ne sont **pas** comparables à 2,6998 / 3,123 : les fenêtres`
- **T1** `| bras | standard 128 | segmenté 4×128 | segmenté sans état |`
- **T1** `Écart total entre les trois bras : **0,0039** (0,13 %). L'état ne domine pas le témoin, et il est`
- **T1** ``(graine-1) × 10 000 019` ; contrôle : perte au pas 1 = 106,5571 (g1) contre 121,5763 (g2).`
- **T1** `Loading weights:   0%|          | 0/68 [00:00<?, ?it/s]`
- **T1** `Loading weights: 100%|██████████| 68/68 [00:00<00:00, 932.90it/s]`
- **T1** `[still running after 60000ms; moved to background job bash-48]`
- **T1** `0, 1164 MiB, 82 %`
- **T1** `1, 1164 MiB, 78 %`
- **T1** `À côté : 232 transcripts de sessions (413 Mo) et un bundle git du dépôt (31 Mo, historique`
- **T1** `0, 1164 MiB, 83 %`
- **T1** `1, 1164 MiB, 83 %`
- **T1** `# fenêtres (82 %). `equilibre` donne le même quota à chaque source.`
- **T1** `| 13:01 | `4442c64c` | N2 — L'ÉTAT DE SECTION NE SE DISTINGUE PAS D'UN ÉTAT ÉTRANGER (+0,36 % CONTRE +0,37 %) |`
- **T1** `[still running after 60000ms; moved to background job bash-81]`
- **T1** `4 sources, **B′** quotas égaux (le manifeste est à **82 % anglais**), **C** curriculum 129`
- **T1** `sur A ; la hiérarchie est écartée deux fois, restent **le curriculum et les données** (41 Mo,`
- **T2** `1, 1164 MiB, 81 %`
- **T2** `data/corpus_fr.txt                 1907    3.8 %`
- **T2** `data/udhr/udhr_train.txt           1802    3.6 %`
- **T2** `data/corpus_en.txt                41257   82.5 %`
- **T2** `data/corpus_mixte_litt.txt         5033   10.1 %`
- **T2** `[still running after 60000ms; moved to background job bash-95]`
- **T2** `> connues**. `porte-homeostasie` (exit 2) : **environnementale** — `/tmp/n4/rang4-lora.pt` effacé`
- **T2** `> livre 10/10, go 9×9 10/10 contre 3/10, dames 0 défaite, cartes 44,7 % contre 51,0 %). Les **deux rouges**`
- **T2** `> `porte-pont` **+2,81 % / +25,35 %**, `porte-coupe` **+0,52 % → +17,09 %**, `porte-gain` **29,0206 →`
- **T2** `> 1297,5437**, `porte-topologie` **42,5477**, `porte-reparti-moteur` **0,0000 %**, `porte-greffe` **branchée**,`
- **T2** `tools/adaptateur_langue.py:19:      --fr data/corpus_fr.txt --pas 2000 [--rang 8] [--sortie /tmp/adaptateur-fr.pt]`
- **T2** `- **Un seul corpus**, français, 4,63 Mo.`
- **T2** `fenêtres de train présentes >1 fois dans train : 47 / 200 (23.5 %)`
- **T2** `[still running after 60000ms; moved to background job bash-121]`
- **T2** `- **R0** : un contrôleur **classique** + un modèle externe atteint-il **90 %** de la compréhension à **30 %** du`
- **T2** `> **168 mesures** en **10 parties** (`07/p1.md` … `07/p10.md`), pas un fichier de 150 Ko. La lire **par`
- **T2** `0, 1164 MiB, 78 %`
- **T2** `1, 1164 MiB, 80 %`
- **T2** `| [2026-09-29](2026-09-29/attention.md) | `+6 %` · `×2,8` · `×1,8` · `×2,3` |`
- **T2** `| [2026-09-30](2026-09-30/attention.md) | `−61 %` · `−24 %` · `7,59 ms` |`
- **T2** `| [2026-10-01](2026-10-01/attention.md) | `85,1 s` · `× 3` |`
- **T2** `| [2026-10-02](2026-10-02/attention.md) | `×9,34` · `4,5 %` · `1003 ms` · `×3` |`
- **T2** `| bras | graines | protocole 8×16×128 | fenêtres propres | fenêtres contaminées |`
- **T2** `| B — 20 000 pas, manifeste 4 sources (82,5 % anglais) | 3 | **3.7591** | **3.8573** | **3.4554** |`
- **T2** `| Bp — 20 000 pas, 4 sources à quotas égaux (25 %) | 3 | **3.4350** | **3.5634** | **3.1177** |`
- **T2** `> complet (20 000 pas, 41 Mo) fait baisser la PPL de **2,9355 à 2,8527** sous le protocole de N2.19 ;`
- **T2** `> le corpus à quatre sources la fait **monter** à **3,7591** ; et **32,8 % des fenêtres du protocole`
- **T2** `**20,48 Mo d'un seul corpus en 5 000 pas**, la moitié du budget de N2 (41 Mo, 20 000 pas, quatre`
- **T2** `| distillation courte | 5 000 pas · 20,48 Mo · **2,9355** (3 graines) | `artefacts/temoin-g{1,2,3}.pt` |`
- **T2** `Corput), et un décalage de fenêtres par graine `(graine − 1) × 10 000 019` — sans lui, deux graines`
- **T2** `Plan des bras, **budget strictement égal** (20 000 pas × 16 × 128 = **41 Mo vus**), lr 1e-4 sur`
- **T2** `| **B** | manifeste 4 sources : fr 3,8 %, UDHR 3,6 %, **en 82,5 %**, litt. 10,1 % | la diversité, telle que le manifeste la définit |`
- **T2** `| **B′** | 4 sources à **quotas égaux** (25 % chacune) | la part de l'anglais dans l'effet de B |`
- **T2** `| bras | graines | protocole 8×16×128 | fenêtres propres | fenêtres contaminées | 8×15×129 |`
- **T2** `| **B** — 20 000 pas, manifeste 4 sources (82,5 % anglais) | 3 | 3,7591 ±0,0075 | 3,8573 ±0,0161 | 3,4554 ±0,0109 | 3,8218 ±0,0092 |`
- **T2** `| **Bp** — 20 000 pas, 4 sources à quotas égaux (25 %) | 3 | 3,4350 ±0,0022 | 3,5634 ±0,0039 | 3,1177 ±0,0052 | 3,4848 ±0,0041 |`
- **T2** `- **30,7 %** d'un échantillon de 300 fenêtres de validation apparaissent **verbatim** dans`
- **T2** `l'entraînement ; **32,8 %** des 128 fenêtres du protocole (42 sur 128) ;`
- **T2** `- **23,5 %** d'un échantillon de 200 fenêtres d'entraînement apparaissent **plus d'une fois** dans`
- **T2** `protocole. Le manifeste est à 82,5 % anglais alors que le professeur est **français** : les`
- **T2** `- **B11.10** : **hybride 4/4** — codec **161/161**, ambiguïtés refusées ; **69,3 %** natif ;`
- **T2** `-  **N2.h2** (distillation, professeur refait, 3 graines) : **2,9935** contre **2,9927** (+0,029 %) ;`
- **T2** `+- **N2** : GPU ; **N2.d** — le budget plein (20 000 pas, 41 Mo, 3 graines) paie`
- **T2** `+  **2,9355 → 2,8527** ; les quatre sources coûtent **+0,9064** (professeur français, 82,5 %`
- **T2** `+  à 129. **La validation n'est pas tenue à l'écart : 32,8 % des fenêtres du protocole sont`
- **T2** `+129 ; et **32,8 % des fenêtres du protocole de validation sont verbatim dans l'entraînement**`
- **T2** `+| **N — le natif** | DRVM, `drave-n0`, distillation, usage, échelle | 🔬 N0/N1 mesurés ; **N0.3b close** ; N2 : budget **−0,08**, **validation contaminée (32,8 %)** ; N4 partiel | **N2** (le corpus dé`
- **T2** `+| **N2** | la distillation : 49 999 fenêtres, 4 sources, professeur Qwen/DeepSeek | 🔬 | **N2.d** — le budget plein paie **2,936 → 2,853** ; les quatre sources coûtent **+0,906** ; **la validation est`
- **T2** `+   jeu **contaminé à 32,8 %** — voir [N2.d](../../reports/rapport-n2-budget.md)) ; **130** est négatif`
- **T2** `+  recopie (32,8 % des fenêtres du protocole sont verbatim dans l'entraînement) : la question n'a de`
- **T2** `0088fc2f R4.4 — L'OCR LIT DIX PAGES À 4,48 % DE WER, LA PARITÉ DE PASSAGE TIENT À 90 %, LA PAGE « PHOTO » TOMBE À 26,7 %`
- **T2** `la question était simple : le dispositif reconstruit hier n'avait vu que **20,48 Mo** d'un seul`
- … (tronqué)

## 5. Erreurs rencontrées

64 sorties en erreur ou divergentes. Les premières :

- **T1** : __pycache__/ *.pyc reports/*.tmp models/ data/ qtrinet-core/target/  # Traces de session : la copie brute reste sur disque (volumineuse, binaire), # le digest markdown est versionné. journal/sessions/
- **T1** : -rw-r--r--. 1 stephane stephane 610 31 oct 17:24 work/n2d/essai-fr.json -rw-r--r--. 1 stephane stephane 650 31 oct 17:24 work/n2d/essai-multi.json === logs === -- A-fr-g1 pas  2250 · seq 128 · perte 5
- **T1** : 54dc7a26 ÉTAT — LA CAMPAGNE N2 BUDGET ET DONNÉES EST OUVERTE, LES GPU RÉSERVÉS JUSQU'À 19 h 40 9f1dcaae N2 — LES POINTS DE CONTRÔLE SONT CONSERVÉS SUR DEUX DISQUES (1,4 GO, EMPREINTES VÉRIFIÉES) === é
- **T2** : 17:35 -- A-fr-g1 pas  8750 · seq 128 · perte 48.6506 · PPL 128/4 2.4483 · 592 s -- B-multi-g1 pas  8750 · seq 128 · perte 91.2001 · PPL 128/4 3.7502 · 591 s -- A-fr-g2 -- B-multi-g2 [exit code: 1]
- **T2** : 17:37 pas 10250 · seq 128 · perte 51.3992 · PPL 128/4 2.4407 · 695 s pas 10500 · seq 128 · perte 48.7937 · PPL 128/4 2.4455 · 712 s [exit code: 1]
- **T2** : 17:37 pas 10750 · seq 128 · perte 53.3267 · PPL 128/4 2.4458 · 730 s pas 11000 · seq 128 · perte 44.5797 · PPL 128/4 2.4276 · 748 s [exit code: 2]
- **T2** : 17:38 pas 12000 · seq 128 · perte 49.2191 · PPL 128/4 2.4135 · 818 s [exit code: 1]
- **T2** : 17:40:04 pas 13000 · seq 128 · perte 53.7650 · PPL 128/4 2.4008 · 886 s pas 13000 · seq 128 · perte 84.8568 · PPL 128/4 3.7372 · 877 s [exit code: 1]
- **T2** : 17:42:32 pas 15250 · seq 128 · perte 45.0087 · PPL 128/4 2.4105 · 1037 s pas 15250 · seq 128 · perte 81.7393 · PPL 128/4 3.7293 · 1027 s [exit code: 1]
- **T2** : 18:19 6 -- A-fr-g3 pas  6750 · seq 128 · perte 53.3343 · PPL 128/4 2.5292 · 453 s -- B-multi-g3 pas  6500 · seq 128 · perte 87.6959 · PPL 128/4 3.7325 · 442 s -- C-129-g1 -- Bp-equilibre-g1 [exit code
- **T2** : 18:29 work/n2d/A-fr-g1.json work/n2d/A-fr-g2.json work/n2d/B-multi-g1.json work/n2d/B-multi-g2.json work/n2d/contamination.json work/n2d/evaluations-finales.json -- A-fr-g3 pas 16000 · seq 128 · perte
- **T2** : 18:40 8 -- C-129-g1 pas  6000 · seq 129 · perte 51.6991 · PPL 128/4 2.4037 · 403 s -- Bp-equilibre-g1 pas  5750 · seq 128 · perte 104.8664 · PPL 128/4 3.3953 · 377 s -- C-129-g2 -- Bp-equilibre-g2 [ex
- **T2** : 18:40 [exit code: 2]
- **T2** : 18:51 work/n2d/A-fr-g1.json work/n2d/A-fr-g2.json work/n2d/A-fr-g3.json work/n2d/B-multi-g1.json work/n2d/B-multi-g2.json work/n2d/B-multi-g3.json work/n2d/C-129-g1.json work/n2d/contamination.json wo
- **T2** : 19:03 [exit code: 2]

## 6. Commits

- ÉTAT — LA CAMPAGNE N2 BUDGET ET DONNÉES EST OUVERTE, LES GPU RÉSERVÉS JUSQU'À 19 h 40  Une seconde session peut démarrer : en-cours nomme désormais la session a
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add .gitignore docs/pilotage/en-cours.md docs/pilotage/roadmap.md docs/pilotage/backlog/N2-distillatio
- RÉFÉRENCES — LA PASSE DU 31 À 19 h 42 ENTRE EN TÊTE, LA PAGE RESTE SOUS SON BUDGET  La passe complète de clôture (79 portes, 75 vertes, 4 rouges, 1 h 39, journa
- ÉTAT — LA SESSION N2.h PORTE SON PLAN, SON AMBITION ET SA STRATÉGIE DANS LA PAGE D'ÉTAT  La page d'état doit suffire à une autre session : en-cours expose maint
- ÉTAT — N2.h : LA CHAÎNE PROPRE DONNE 3,10 EN DOMAINE, PAS 2,85  Le premier point de contrôle de la chaîne refaite sur le corpus dédupliqué est évalué : 3,10 en 
- ÉTAT — N2.h : LA DIVERSITÉ FRANÇAISE DIVISE LA PPL HORS DÉPÔT PAR 4,4  Le bras diversité (moitié dépôt, moitié littérature française, même budget, mêmes trois g
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add docs/pilotage/backlog/N2-distillation.md docs/pilotage/en-cours.md docs/pilotage/references-non-re
- JOURNAL — N2.h : LE MÈTRE PROPRE, LA GÉNÉRALITÉ, ET LE VERROU DE LONGUEUR  Le récit de la nuit : la validation se recopiait (32,8 %), le corpus dédupliqué tombe
- N2.h4 — LES DEUX LEVIERS SE COMPOSENT : 3,47 EN DOMAINE, 4,10 HORS DÉPÔT, 3,49 À 256 OCTETS  Le corpus mixte (moitié dépôt, moitié littérature) et les positions
- ÉTAT — N2.h CLOSE : QUATRE FICHES COMMITTÉES, PORTES VERTES  La page d'état passe la session N2.h en close : les quatre fiches (n2-propre, n2-diversite, n2-long
- N2.h5 — LA CAPACITÉ PAIE EN DOMAINE (−0,06) MAIS NE COUVRE PAS  À données, professeur et budget égaux, le modèle de 21,65 M (d_model 296, expert_hidden 416, ×1,
- N2.h3b — LE SECOND VERROU N'EST PAS LE MASQUE : ÉLARGIR LA FENÊTRE À L'INFÉRENCE NE RÉCUPÈRE RIEN  À 512 octets, l'attention locale (fenêtre 256) ne laisse voir
- RECENSEMENT — 27,7 Mo DE FRANÇAIS UNIQUE DANS LE DÉPÔT, 8,5 FOIS LE CORPUS UTILISÉ  Le levier « plus de texte français unique » a un chiffre : avec les mêmes sh
- ÉTAT — R4.4 CLOSE, PENSÉE EN PAUSE, B13 AU PLAN : LES SCANS RÉELS SONT LA LIMITE NOMMÉE  Vérification des trois sessions : N2.h close (0b0a6a0d), R4.4 close (fe
- PENSÉE v0 — LE STATE STORE EXISTE ET TIENT SES SIX PORTES  Le contrat docs/implantation/moteur-de-pensee.md a son implémentation : types canoniques (Candidat, E
- N2.i — LE CORPUS ÉLARGI GÉNÉRALISE (ANGLAIS ÷1,7) SANS RELEVER LE DOMAINE  À recette égale, le corpus du dépôt courant (docs + journal + rapports, 1 308 documen
- SESSION — N2.i ET PENSÉE v0 CLOS : LE CORPUS ÉLARGI GÉNÉRALISE, LE MOTEUR TIENT SES PORTES  Les deux chantiers menés en parallèle sont committés : N2.i (17ececf
- LA TYPOGLYCÉMIE DU MODÈLE : IL LIT LES LETTRES, PAS LES FORMES (×17,8 AU MÉLANGE)  Trois variantes du même texte de validation, mêmes octets, même protocole : p
- S — LE BANC DE STRUCTURES : UN OUTIL HUMAIN POUR VOIR ET VALIDER LES INTERPRÉTATIONS  Nouveau sous-projet (submodule : tools/structures, dépôt local drave-struc
- S — LE GÉNÉRATEUR DE CANDIDATS : UNE PHRASE BRUTE → DES STRUCTURES À VALIDER  Le banc de structures gagne son analyseur v0 (submodule tools/structures, commit a
- S — LE NIVEAU PRAGMATIQUE : LE CONTEXTE TRANCHE, LE DOUBLE SENS SE CONSERVE  Le banc de structures ne force plus un verdict unique (submodule 7366191). Chaque l
- ÉTAT — COMPTEURS APRÈS LE BANC DE STRUCTURES : 381 FICHIERS, 458 JSON  Le compteur JSON suit les dépôts des autres sessions (corpus-wiki-fr.json) ; la revue rep
- S — DES CONTEXTES PLUS LARGES, ET LA MESURE DE CE QU'IL FAUT POUR TRANCHER  Le contexte n'est plus un champ unique : il est gradué (0 sans contexte, 1 phrase d'
- N2.j — 186 Mo DE VRAI FRANÇAIS : LE BLOC LINGUISTIQUE GAGNE ×1,7 À ×2,6 HORS DOMAINE  Sur l'inventaire local (132 Go de Wikipédia, base FR de 7,25 Go) : 120 000
- N2.k — DIX LANGUES : LE FRANÇAIS PAIE 0,65 BIT/OCTET, LES AUTRES GAGNENT 0,8 À 3,4  Dix langues extraites des bases sqlite (fr, en, de, es, it, pt, ru, ar, ja, 
- ÉTAT — COMPTEUR JSON 471 (DIX LANGUES)  Les corpus et les évaluations multilingues de l'autre session font passer le compteur à 471 ; la revue repasse." && git 
- N2.j2 — POSITIONS ALÉATOIRES SUR 186 Mo : LE VERROU DE LONGUEUR TOMBE ENCORE (÷2,4 À 512)  La base du corpus réel (186 Mo de Wikipédia, N2.j) entraînée avec des
- N2.j3 — LA CAPACITÉ SUR 186 Mo : 21,65 M PAIE (4,39 → 4,20), DONNÉES × CAPACITÉ  À données et budget égaux (20 000 pas, positions 0–384), le modèle de 21,65 M v
- N2.l — LE CANAL DE STRUCTURE : +5 % DE PPL POUR 1 344 PARAMÈTRES, ET LE MÊME ALPHABET  Donner au modèle une classe de structure par octet (mot plein, grammatica
- N2.l — LE CANAL DE STRUCTURE : +5 % DE PPL POUR 1 344 PARAMÈTRES, ET LE MÊME ALPHABET  Donner au modèle une classe de structure par octet (mot plein, grammatica
- N2.j4 — LA DISTILLATION SUR LE CORPUS RÉEL : 4,39 → 3,88, ET TOUT LE RESTE BAISSE  Professeur 23,57 M sur les 186 Mo de Wikipédia (1,6655 bit/octet), distillé d
- N2.m — L'ANGLAIS SEUL : 4,42 SUR 204 Mo, ET LE MULTILINGUE COÛTE 1,6 PPL  La base anglaise monolingue (120 000 articles, 204,6 Mo d'entraînement, positions aléa
- N2.m — L'ANGLAIS SEUL : 4,42 SUR 204 Mo, ET LE MULTILINGUE COÛTE 1,6 PPL  La base anglaise monolingue (120 000 articles, 204,6 Mo d'entraînement, positions aléa
- S — L'ANALYSEUR PLUS RICHE : SUBORDONNÉES, COORDINATION, ET L'EXPORT VERS LE CORPUS  Le générateur distingue le « que » complément (après un verbe → SUB) de la 
- ÉTAT — INTÉGRATION L : GOLD 220, 36 AMBIGUËS, ATTACHEMENT TÊTE 0,972/0,889  Le hub intègre le bloc de la session L : gold 220 (60 réels + 160 synthétiques), POS
- N2.n — LA DISTILLATION ANGLAISE : 4,42 → 3,94, LA CHAÎNE COMPLÈTE SUR 204 Mo  Le professeur 23,57 M entraîné sur les 204,6 Mo d'anglais, distillé dans la base a
- N2.n — LA DISTILLATION ANGLAISE : 4,42 → 3,94, LA CHAÎNE COMPLÈTE SUR 204 Mo  Le professeur 23,57 M entraîné sur les 204,6 Mo d'anglais, distillé dans la base a
- N2.n — LA DISTILLATION ANGLAISE : 4,42 → 3,94, LA CHAÎNE COMPLÈTE SUR 204 Mo  Le professeur 23,57 M entraîné sur les 204,6 Mo d'anglais, distillé dans la base a
- N2.o — LA DISTILLATION MULTILINGUE : DIX LANGUES S'AMÉLIORENT, LA DILUTION RESTE  Le professeur 23,57 M entraîné sur les 237 Mo des dix langues, distillé dans l
- JOURNAL — LA NUIT N2 : DU CORPUS PROPRE AU CORPUS RÉEL  Récit de la session N2 : le mètre honnête (3,09), les leviers (diversité, positions, capacité, canal), l
- N2.p — LA CAPACITÉ À 34,3 M : −0,19 PAR PALIER, ET LE VERROU DE LONGUEUR S'EFFACE  Sur les 186 Mo du corpus réel, la base passe de 4,3893 (11,47 M) à 4,2013 (21
- N2.p — LA CAPACITÉ À 34,3 M : −0,19 PAR PALIER, ET LE VERROU DE LONGUEUR S'EFFACE  Sur les 186 Mo du corpus réel, la base passe de 4,3893 (11,47 M) à 4,2013 (21
- N2.q — LA CAPACITÉ MULTILINGUE : À RECETTE ÉGALE, 21,65 M GAGNE 0,79  À recette égale (20 000 pas, positions [0, 384]), le modèle 21,65 M bat le 11,47 M sur les
- N2.q — LA CAPACITÉ MULTILINGUE : À RECETTE ÉGALE, 21,65 M GAGNE 0,79  À recette égale (20 000 pas, positions [0, 384]), le modèle 21,65 M bat le 11,47 M sur les
- N2 → R1 — CE QUE LA NUIT DIT À LA FENÊTRE : POSITION RELATIVE, FENÊTRE ENTRAÎNÉE, CAPACITÉ  Note de passage vers la ligne R : trois faits mesurés (la position a
- N2 → R1 — CE QUE LA NUIT DIT À LA FENÊTRE : POSITION RELATIVE, FENÊTRE ENTRAÎNÉE, CAPACITÉ  Trois faits mesurés (la position absolue est un défaut d'architectur
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > /tmp/msg-r1.txt <<'EOF' N2 → R1 — CE QUE LA NUIT DIT À LA FENÊTRE : POSITION RELATIVE, FENÊTRE ENTRA
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib, re p = pathlib.Path('docs/pilotage/en-cours.md'); s = p.read_text() s = r
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib, re p = pathlib.Path('docs/pilotage/en-cours.md'); s = p.read_text() s = r
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib, re p = pathlib.Path('docs/pilotage/en-cours.md'); s = p.read_text() s = r

