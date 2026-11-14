# Session DSH — relecture

- identifiant : `session-9f876d8f-5661-44f0-b052-0770211328ec`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-13 21:52:53
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche J4.2 : la coordination S — 11 verdicts de `/paragraphes` non committés. **Ne touche pas `tools/structures/`**. Fiche `reports/rapport-coordination-s.md` + JSON : la liste exacte des 11 verdicts (fichier, lignes, statuts), la commande de commit pour la session S, le risque d'un clone à 523d8c1.

### 👤 Utilisateur

<system-reminder>
The following workspace instructions may be relevant to your work. Use them as guidance when applicable. More specific instructions take precedence over broader ones. They do not override system, developer, or direct user instructions.

Instructions from: AGENTS.md

# Directives de l'agent — Drave

> **Compteurs vivants.** Dans [`docs/pilotage/en-cours.md`](docs/pilotage/en-cours.md) ; ne pas les recopier ici.

> **Porte d'entrée.** Lis ce fichier en entier (2 min) : il porte la **vision**, les règles non négociables et le
> **routage** vers le document de chaque tâche. Le détail n'est pas ici : il est dans [`docs/methode/`](docs/methode/)
> (tableau § 3). L'**état courant** est dans [`docs/pilotage/en-cours.md`](docs/pilotage/en-cours.md) ; la **roadmap** dans
> [`docs/pilotage/roadmap.md`](docs/pilotage/roadmap.md) ; le récit daté dans [`journal/`](journal/).

## 1. La vision (l'essentiel)

**Drave est une vision de l'IA centrée sur les flots de données, pas sur le calcul brut.** Les activations d'un
réseau sont des **faits** regroupés en **listes valuées poussées** vers leurs lecteurs : le coût du calcul devient proportionnel à l'**activité**, et le modèle devient **décomposable**, **répartissable** et **observable**. Le principe : la structure bat la taille. Construire le moteur et modèle optimisé qui rend cette structure observable, décomposable, répartissable et rejouable permet d'atteindre de nouveaux sommets. L'approche par **bus d'événements** rend chaque bloc fonctionnel optimisable, comparable et substituable (neuronal là où l'intuition aide, computationnel là où la fiabilité prime).

Né du besoin de faire tourner des modèles **de types différents** sur des machines **limitées**, de les
**combiner**, de les **décomposer** en couches et grappes exécutables par du matériel divers, voire **distribué
en réseau**, de les **diagnostiquer** en étudiant leurs **flux**, et de **rejouer** des événements.


## 2. Les règles non négociables

1. **Rangement** : `docs/` = état, vision, concepts (ce qui reste vrai quand les chiffres changent) ; `reports/` =
   résultats mesurés, fiches, JSON ; `journal/` = récit daté ; `data/` = corpus. *Un résultat qui traîne dans
   `docs/` **déménage**.* → [`docs/methode/rangement.md`](docs/methode/rangement.md)
2. **Un résultat** porte le chiffre, la mesure, le dispositif, un **contrôle négatif**, et **ce qui pourrait le
   rendre faux** — puis un **commit**, la **fiche** dans `reports/`, le **récit** dans `journal/`, l'**état** dans
   `docs/pilotage/en-cours.md`, et il **nomme sa ligne de roadmap** (A… / B… / N… / R…). *Sans contrôle négatif, ce n'est pas un
   résultat.* → [`docs/methode/resultats.md`](docs/methode/resultats.md)
3. **Les portes** : `bash tools/toutes-les-portes.sh` ; le registre est dans `$JOURNAUX/registre.txt` (affiché au
   lancement) et le verdict se lit par `awk '$2 != 0'` — **jamais** par les marqueurs ni à travers un tube. Rouges
   tolérées : **celles listées dans [`docs/pilotage/references-non-regression.md`](docs/pilotage/references-non-regression.md)** ; toute autre est une régression. →
   [`docs/methode/portes.md`](docs/methode/portes.md)
4. **La revue de documentation** avant chaque commit de clôture : `python3 tools/revue_documentation.py` (et
   `tools/porte-tableaux.sh`) ; **corriger** ce qu'elle signale. → [`docs/methode/rangement.md`](docs/methode/rangement.md)
5. **Panini et Nipada** à chaque cycle : lire ce qui a bougé chez eux, confronter ; la théorie va dans
   [`docs/theorie/genealogie-des-langues.md`](docs/theorie/genealogie-des-langues.md), **jamais** les chiffres. Leur avertissement :
   la surface capte **l'époque** (β +0,138) bien plus que la **filiation** (β +0,049) — contrôler la date dans tout
   test de style, la surface dans tout test de famille. → [`docs/methode/panini-nipada.md`](docs/methode/panini-nipada.md)
6. **Le miroir entrée/sortie** : toute mesure d'entrée se double d'une mesure de **sortie** (restitution, boucle) ;
   la **fluidité n'est pas la fidélité**. → [`docs/methode/miroir.md`](docs/methode/miroir.md)
7. **La roadmap** ([`docs/pilotage/roadmap.md`](docs/pilotage/roadmap.md)) : chaque chantier a une **prochaine action** ; l'ordre est la **valeur** et les **dépendances**, jamais une date. Un chantier est **fini** quand il est
   mesuré, écrit et committé ; il est **marqué**, et le suivant désigné.
8. **Ne jamais bloquer, ne jamais rester en attente** : une question humaine se **consolide** dans `en-cours` et on **continue** ; si une ligne est bloquée (corpus, compte, matériel), on prend la suivante
   — la **file « jamais en attente »** de la roadmap. → [`docs/methode/ressources.md`](docs/methode/ressources.md)
9. **Les illustrations sont des SVG.** Aucun **ASCII art** dans un bloc de code. Un schéma est un
   **`.svg`** — direct, ou généré par **docwatch** depuis `.mmd`/`.puml` (l'image pointe vers
   `<source>.svg`) — avec `viewBox`, `<title>`, `<desc>`, liens relatifs ; il vit dans
   `docs/schemas/` ou `docs/theorie/synthese/schemas/`. Vérifier : `python3 tools/verifier_schemas.py`.
   → [`docs/methode/illustrations.md`](docs/methode/illustrations.md)
10. **Pilotage : cycles longs, sous-agents, état unique.** Un goal par programme (`max_goal_rounds`
    1 000) ; on s'arrête sur un résultat mesuré, écrit, committé, ou un blocage. Les tâches
    indépendantes : **sous-agents** (2–4), sans toucher `en-cours`/`roadmap`/`AGENTS` ; ils
    rendent un **diff**. **État** : une session écrit `en-cours` à la fois ; aucun fait
    sans sa ligne (hook `verifie_etat_a_jour.py`). Git : `git add` explicite. La clôture met `en-cours` à jour (≤ 2 000 mots).
    → [`docs/methode/continuite.md`](docs/methode/continuite.md)

11. **Les GPU sont exclusivement réservés à Drave** ; les **professeurs** passent par l'**API
    DeepSeek** (`tools/llm/enseignant.py`), jamais par un serveur local (`llama-server`,
    `ollama`). Garde-fous : `hauru-gpu-guard` (timer 30 s), `porte-ressources` (contrôle GPU).
    → [`docs/methode/ressources.md`](docs/methode/ressources.md)

## 3. Routage : lire le document de sa tâche, pas les autres

| si la tâche est… | lire |
|---|---|
| comprendre la **vision** (les flots, les cinq axes, ce qu'elle n'est pas) | [`docs/theorie/vision.md`](docs/theorie/vision.md) |
| la **roadmap** (A/B/N/R, l'ordre, la file « jamais en attente ») | [`docs/pilotage/roadmap.md`](docs/pilotage/roadmap.md) |
| **la lecture rapide** et son backlog (techniques, couches, fiches) | [`docs/theorie/lecture-rapide.md`](docs/theorie/lecture-rapide.md) · [`docs/pilotage/backlog/index.md`](docs/pilotage/backlog/index.md) |
| comprendre la mission et les priorités | [`docs/methode/mission.md`](docs/methode/mission.md) |
| écrire un résultat (fiche, JSON, commit, journal) | [`docs/methode/resultats.md`](docs/methode/resultats.md) |
| ranger un fichier, revue de documentation, synthèse | [`docs/methode/rangement.md`](docs/methode/rangement.md) |
| **charger le contexte** (budget, protocole, ce qu'on ne charge pas) | [`docs/methode/contexte.md`](docs/methode/contexte.md) |
| **cycles DSH, sous-agents, reprise** | [`docs/methode/continuite.md`](docs/methode/continuite.md) |
| **rapporter à l'humain, un round** | [`docs/methode/relations-humaines.md`](docs/methode/relations-humaines.md) |
| **dessiner un schéma**, convertir un diagramme, améliorer une illustration | [`docs/methode/illustrations.md`](docs/methode/illustrations.md) |
| lancer ou lire les portes | [`docs/methode/portes.md`](docs/methode/portes.md) |
| étudier Panini/Nipada, la généalogie | [`docs/methode/panini-nipada.md`](docs/methode/panini-nipada.md) |
| concevoir un test d'entrée/sortie, corriger | [`docs/methode/miroir.md`](docs/methode/miroir.md) |
| planifier une campagne, le matériel, carpe diem | [`docs/methode/ressources.md`](docs/methode/ressources.md) |
| **les jeux symboliques** (surface → RSN-jeu → pensée, 71 langues, maîtres) | [`docs/theorie/jeux-symboliques.md`](docs/theorie/jeux-symboliques.md) |
| **le protocole sémantique** (rejouer, convergence, sens → texte, raisonnement gelé) | [`docs/theorie/protocole-semantique.md`](docs/theorie/protocole-semantique.md) |
| **l'état courant** (synthèse + chantiers + questions) | [`docs/pilotage/en-cours.md`](docs/pilotage/en-cours.md) |
| le **vocabulaire** (couche vs étage, termes du dépôt) | [`docs/theorie/glossaire.md`](docs/theorie/glossaire.md) |
| **trouver un sujet** (un concept, un chantier, une phase) | [`docs/theorie/carte.md`](docs/theorie/carte.md) |
| la carte de la documentation | [`docs/README.md`](docs/README.md) |

> **Chargement facultatif.** Les documents de cette table, `docs/pilotage/en-cours.md`, `docs/pilotage/roadmap.md`, `reports/` et
> `journal/` ne se lisent **que pour la tâche en cours** : le fichier de tâche suffit. Ne pas les
> charger « pour être complet » : c'est du contexte qui coûte et périme.

> **Le contexte est un budget.** Par défaut : `AGENTS.md` + `docs/pilotage/en-cours.md` + **un** document de
> tâche. Le protocole, les budgets et les cas « ne pas charger » sont dans
> [`docs/methode/contexte.md`](docs/methode/contexte.md) ; la vérification est
> `python3 tools/taille_documents.py`.

## 4. Le minimum avant de conclure

- l'état est à jour dans [`docs/pilotage/en-cours.md`](docs/pilotage/en-cours.md) (synthèse, chantiers, questions en attente) ;
- la **roadmap** est à jour : le chantier fini y est marqué, le suivant est désigné ;
- la fiche est dans `reports/`, le récit dans `journal/`, le commit porte le chiffre ;
- les portes sont vertes, **hors les rouges tolérées listées dans `docs/pilotage/references-non-regression.md`** ;
- la revue de documentation passe, et les liens résolvent.
- le budget de contexte est vérifié : `python3 tools/taille_documents.py`.
- l'état est court et reprenable : `python3 tools/verifie_en_cours.py`.
- journal : dossiers/jour, sessions liées → `tools/verifie_journal.py`.
- les schémas sont des SVG valides et référencés : `python3 tools/verifier_schemas.py`.

</system-reminder>

### 👤 Utilisateur

Current runtime context. This snapshot supersedes earlier runtime-context snapshots.

Current DSH file policy: danger-full-access. The DSH file sandbox does not restrict file modifications by available operations.

Approval prompts are disabled in this session: actions that require approval are rejected automatically — do not request sandbox escalation (do not set `sandbox_permissions`).

### 👤 Utilisateur

<system-reminder>
A skill is a reusable set of task-specific instructions. The following skills are available in this session:

<available_skills>
- `microsoft-foundry`: Deploy, evaluate, fine-tune, and manage Foundry agents end-to-end with azd: hosted agent scaffold/run/deploy, prompt agent create, batch eval, continuous eval, prompt optimizer, Agent Optimizer scaffold, agent.yaml, dataset curation from traces, model fine-tuning (SFT/DPO/RFT). USE FOR: azd ai agent, azd provision/deploy, deploy agent, hosted agent, create agent, add tool to agent, invoke agent, evaluate agent, continuous eval, continuous monitoring, agent CI/CD, optimize prompt, improve prom...
</available_skills>

If the user names a skill, or the task clearly matches a skill's description, call the `skill` tool with the exact skill name before taking task actions. Load all applicable skills, then follow their full instructions. This catalog contains summaries only; do not infer or follow a skill's instructions until it has been loaded.
A user may also invoke a skill directly; its <skill_content> block then appears in this conversation. Follow it, and do not call the `skill` tool again for that skill.
</system-reminder>

- **bash** `{"command": "git status --short | head -50; echo '---'; git log --oneline -15; echo '---'; git rev-parse HEAD", "description": "Show git status and recent log"}`

  ```
M docs/pilotage/references-non-regression.md
D  journal/2026-11-13/README.md
D  journal/2026-11-13/docs.md
MM journal/README.md
MM journal/THEMES.md
MM journal/sessions/MANIFEST.md
MM journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
MM journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
MM journal/sessions/session-3ffa6026-9a7d-4905-ac06-6b9708d65ba7/digest.md
MM journal/sessions/session-3ffa6026-9a7d-4905-ac06-6b9708d65ba7/rapport.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 m tools/structures
?? journal/2026-11-13/
?? reports/rapport-coordination-n2.json
?? reports/rapport-coordination-n2.md
?? reports/rapport-s-paragraphes.md
---
ced21933 CHANTIER — PHASE 2 (12 H) : LE VERDICT ACCEPTATION D'ABORD (TIMEOUT APRÈS COMMIT = FAIT), 12 TÂCHES AJOUTÉES (J4 COORDINATION, J6 SPANS, J7-J10 PANINI/BILAN), ÉTAT CORRIGÉ
c7f26b35 DOCS — LA PASSE APRÈS LE CHANTIER : 8 FICHES INDEXÉES, L'ÉTAT PAR JOUR DU PLAN, LE JOURNAL
… [1490 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"J4.2\\|coordination S\\|523d8c1\" --include=*.md --include=*.json --include=*.txt . 2>/dev/null | head -40", "description": "Search for task references"}`

  ```
./reports/pensee-audit-attachement.json:25:  "submodule_structures": "523d8c1e8c6ca29ca415360a71bfab6c5b56102c",
./reports/pensee-audit-attachement.json:949:  "la mesure dépend du sous-module tools/structures au commit 523d8c1 (segmentation S) ; son fichier de données modifié (donnees/paragraphes-validations.jsonl) n'est lu que par serveur.py, pas par generateur.analyser.",
./reports/rapport-audit-attachement.md:155:  `523d8c1`. Son fichier de données modifié (`donnees/paragraphes-validations.jsonl`) n'est
./reports/rapport-audit-attachement.md:174:  (sous-module `523d8c1`).
./reports/rapport-audit-v2.md:291:  est au commit `523d8c1` ; sa modification de travail (`donnees/paragraphes-validations.jsonl`)
./reports/pensee-gold-anglais.json:15:  "generateur_commit": "523d8c1",
./reports/rapport-partition-syntagmes.md:45:| générateur S | `tools/structures/generateur.py` @ sous-module `523d8c1e`, sha256 `291df65a…765202d5` |
./reports/rapport-etat-s.md:22:| verdicts `/paragraphes` dans git | **8 committés**, **11 non committés** (a004–a009) | sous-module `523d8c1` + `git status` |
./reports/rapport-etat-s.md:34:est sur **`master`**, HEAD **`523d8c1`** (2026-11-04), avec **un fichier mod
… [46009 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"J4\\.2\\|J4\\.1\\|J4 \" docs/pilotage/en-cours.md docs/pilotage/roadmap.md 2>/dev/null | head -40", "description": "Find J4 task definitions"}`

  ```
(no output)
  ```

- **bash** `{"command": "wc -l reports/rapport-s-paragraphes.md reports/rapport-coordination-n2.md reports/rapport-etat-s.md 2>/dev/null; echo ---; head -60 reports/rapport-s-paragraphes.md", "description": "Inspect existing S reports"}`

  ```
58 reports/rapport-s-paragraphes.md
  421 reports/rapport-coordination-n2.md
  506 reports/rapport-etat-s.md
  985 total
---
# S — La banque de paragraphes passe à neuf : six paires d'Alice, sources anglaises et référents

> **Ligne de roadmap** : S · **Date** : 2026-11-03 · **Verdict** : la banque passe de **3 à 9
> paragraphes complets**. Les six nouveaux — l'ouverture d'Alice, la table de verre, l'attente à
> la petite porte, « Buvez-moi », « Je me sens toute drôle » et le gâteau oublié — portent chacun
> leur **contexte**, leur **antécédent** (Alice) et leur **source anglaise** (Project Gutenberg
> #11). La page `/paragraphes` en affiche neuf, avec l'arbre, les référents et la source ; les
> **55 tests** passent.

## Les six paires

| id | cible (français) | source (anglais) | réf. |
|---|---|---|---:|
| a004 | « ALICE, assise auprès de sa sœur… commençait à s'ennuyer… » | *Alice was beginning to get very tired…* | 1 |
| a005 | « Tout à coup elle rencontra… une petite table à trois pieds, en verre massif… » | *Suddenly she came upon a little three-legged table…* | 3 |
| a006 | « Comme cela n'avançait à rien… elle retourna vers la table… » | *There seemed to be no use in waiting
… [2621 caractères tronqués]
  ```

- **bash** `{"command": "git show --stat ced21933 | head -40; echo '==='; grep -rn \"J4\" journal/2026-11-13/ docs/pilotage/ 2>/dev/null | head -40", "description": "Inspect chantier commit and J4 references"}`

  ```
commit ced219338dabec2554c3a32d7c95ee8e8cdbfac0
Author: Stéphane <stephane@localhost>
Date:   Fri Nov 13 21:35:59 2026 -0500

    CHANTIER — PHASE 2 (12 H) : LE VERDICT ACCEPTATION D'ABORD (TIMEOUT APRÈS COMMIT = FAIT), 12 TÂCHES AJOUTÉES (J4 COORDINATION, J6 SPANS, J7-J10 PANINI/BILAN), ÉTAT CORRIGÉ

 docs/pilotage/chantiers.md                         |  2 +-
 docs/pilotage/en-cours.md                          |  2 +-
 journal/2026-11-13/README.md                       |  9 ++-
 journal/2026-11-13/docs.md                         | 29 ++++++++
 journal/README.md                                  |  3 +-
 journal/THEMES.md                                  |  1 +
 journal/sessions/MANIFEST.md                       |  2 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md | 32 ++++++++
 .../rapport.md                                     | 15 ++--
 tools/chantier/plan.json                           | 86 ++++++++++++++++++++++
 tools/chantier/superviseur.py                      |  5 +-
 11 files changed, 173 insertions(+), 13 deletions(-)
===
docs/pilotage/semaine-autonome.md:47:- **7 axes** ; le noyau J4 (ℝ, CIC-lite) est **actif** ; NIPADA (produit) est **bloqué** (DTP arrêté
docs/pi
… [391 caractères tronqués]
  ```

- **bash** `{"command": "head -80 reports/rapport-coordination-n2.md; echo '==== JSON ===='; head -60 reports/rapport-coordination-n2.json", "description": "Read coordination N2 precedent report"}`

  ```
# N2 — la coordination du mètre : `--rope` ne suffit pas, il faut le canal

> **Ligne de roadmap** : N2 (la porte de perplexité) · **Date** : 2026-11-13 · **HEAD mesuré** :
> `ced21933` · **Verdict** : `tools/eval_n2_propre.py` lit les checkpoints RoPE comme des positions
> absolues et rend **8,0225** sur `propre512-8k` à 128 octets, là où le mètre RoPE rend **2,9726**
> à 128 et **2,7856** à 1 024. Le correctif `--rope` est **nécessaire mais non suffisant** : le
> checkpoint de la porte a été entraîné **avec le canal**, et `--rope` seul rend **40,0658** à 128.
> Le correctif validé est **`--rope --canal-dir`** ; la commande qui donne 2,79 aujourd'hui est le
> mètre existant `work/n2ac/eval_longueurs.py --rope`. **Aucun fichier de N2 modifié**
> (`native_model.py`, `entrainer_native.py`, `work/` intacts).

**En trois lignes.** (1) `charge()` construit `NativeModel` absolu et `ppl_protocole()` oublie le
canal : **deux** causes, pas une. (2) `--rope` seul rend **40,07** ; `--rope --canal-dir` rend
**2,9726** à 128 et **2,7856** à 1 024. (3) La commande qui donne 2,79 aujourd'hui est
`work/n2ac/eval_longueurs.py --rope ... --val data/corpus_propre` (§ 4.A).

## Ce que cette fiche est,
… [6053 caractères tronqués]
  ```

- **bash** `{"command": "python3 -c \"\nimport json\nd=json.load(open('tools/chantier/plan.json'))\nprint(type(d), list(d)[:10] if isinstance(d,dict) else len(d))\n\" ; grep -n \"J4\" tools/chantier/plan.json | head -30", "description": "Inspect chantier plan for J4.2"}`

  ```
<class 'dict'> ['nom', 'principe', 'taches']
143:   "id": "J4.1",
146:   "mandat": "Tâche J4.1 : la coordination N2 — le mètre `eval_n2_propre.py` lit les checkpoints RoPE comme des positions absolues (8,02 au lieu de 2,79). **Ne modifie rien dans N2** (ni `entrainer_native.py`, ni `native_model.py`, ni `work/`). Écris une fiche de coordination `reports/rapport-coordination-n2.md` + JSON : le bug, le correctif proposé (--rope), les chiffres, la commande exacte pour la session N2.",
156:   "id": "J4.2",
159:   "mandat": "Tâche J4.2 : la coordination S — 11 verdicts de `/paragraphes` non committés. **Ne touche pas `tools/structures/`**. Fiche `reports/rapport-coordination-s.md` + JSON : la liste exacte des 11 verdicts (fichier, lignes, statuts), la commande de commit pour la session S, le risque d'un clone à 523d8c1.",
169:   "id": "J4.3",
172:   "mandat": "Tâche J4.3 : la coordination R — décider le tagger POS sur le gold 612 via l'API DeepSeek (clé absente). Fiche `reports/rapport-coordination-r.md` + JSON : le coût (~1 200 appels, ~360 k tokens, ~20 min), la décision (mesure < +2 pts → négatif nommé ; ≥ +5 → intégrer), la commande exacte avec la clé.",
182:   "id": "J4.4",
185:   
… [316 caractères tronqués]
  ```

- **bash** `{"command": "cd tools/structures && git rev-parse HEAD && git status --porcelain && echo '--- diffstat ---' && git diff --stat && echo '--- log ---' && git log --oneline -5", "description": "Read submodule status and HEAD (read-only)"}`

  ```
523d8c1e8c6ca29ca415360a71bfab6c5b56102c
 M donnees/paragraphes-validations.jsonl
--- diffstat ---
 donnees/paragraphes-validations.jsonl | 11 +++++++++++
 1 file changed, 11 insertions(+)
--- log ---
523d8c1 S — LE FAIT DIVERS EST TRANCHÉ : 61/61 TYPES, 144/144 RÔLES ; LA TÊTE DU GN ARRÊTE LE VERBE
4012729 S — LA BANQUE DE PARAGRAPHES PASSE À NEUF : SIX PAIRES D'ALICE, SOURCES ANGLAISES ET RÉFÉRENTS
7ccc60f S — VALIDATION HUMAINE : 8 VERDICTS DE RÉFÉRENTS SUR /PARAGRAPHES (a001–a003) + 8 VERDICTS BANQUE (p003, c010, c066, c067)
230d03a S — LES TROIS LIMITES DE LA V4 SONT FERMÉES : h050, h053, « SI FORT QUE » ; GOLD 60, 60/60 TYPES, 142/142 RÔLES
644ad3d S — LA TRADUCTION CONTRÔLE LE SENS : 14/14 RÉFÉRENTS ANAPHORIQUES CONFIRMÉS PAR L'ANGLAIS, « LES » → « IT » RETROUVÉ
  ```

- **bash** `{"command": "cd tools/structures && git diff -- donnees/paragraphes-validations.jsonl", "description": "Show the 11 uncommitted verdict lines"}`

  ```
diff --git a/donnees/paragraphes-validations.jsonl b/donnees/paragraphes-validations.jsonl
index 2ada51b..b34f8f5 100644
--- a/donnees/paragraphes-validations.jsonl
+++ b/donnees/paragraphes-validations.jsonl
@@ -6,3 +6,14 @@
 {"phrase_id": "a003", "candidat_id": "a003-c1", "statut": "exclu", "referents": {"Elle": "Alice", "sa": "Alice", "elle": "Alice", "se": "Alice"}, "note": "", "contexte": "Allons, à quoi bon pleurer ainsi, se dit Alice vivement.", "niveau": 2, "auteur": "humain", "horodatage": "2026-11-03T17:05:31"}
 {"phrase_id": "a003", "candidat_id": "a003-c2", "statut": "resolu", "referents": {"Elle": "Alice", "sa": "Alice", "elle": "Alice", "se": "Alice"}, "note": "", "contexte": "Allons, à quoi bon pleurer ainsi, se dit Alice vivement.", "niveau": 2, "auteur": "humain", "horodatage": "2026-11-03T17:05:40"}
 {"phrase_id": "a003", "candidat_id": "a003-c3", "statut": "exclu", "referents": {"Elle": "Alice", "sa": "Alice", "elle": "Alice", "se": "Alice"}, "note": "", "contexte": "Allons, à quoi bon pleurer ainsi, se dit Alice vivement.", "niveau": 2, "auteur": "humain", "horodatage": "2026-11-03T17:06:16"}
+{"phrase_id": "a004", "candidat_id": "a004-c1", "statut": "resolu", "
… [3571 caractères tronqués]
  ```

- **bash** `{"command": "cd tools/structures && wc -l donnees/paragraphes-validations.jsonl && git show HEAD:donnees/paragraphes-validations.jsonl | wc -l && head -3 donnees/paragraphes-validations.jsonl", "description": "Count committed and working lines"}`

  ```
19 donnees/paragraphes-validations.jsonl
8
{"phrase_id": "a001", "candidat_id": "a001-c1", "statut": "resolu", "referents": {"Elle": "Alice", "se": "Alice", "elle": "Alice", "lui": "Alice", "en": "Alice"}, "note": "", "contexte": "Allons, à quoi bon pleurer ainsi, se dit Alice vivement.", "niveau": 2, "auteur": "humain", "horodatage": "2026-11-03T16:49:32"}
{"phrase_id": "a001", "candidat_id": "a001-c2", "statut": "resolu", "referents": {"Elle": "Alice", "se": "Alice", "elle": "Alice", "lui": "Alice", "en": "Alice"}, "note": "", "contexte": "Allons, à quoi bon pleurer ainsi, se dit Alice vivement.", "niveau": 2, "auteur": "humain", "horodatage": "2026-11-03T16:49:59"}
{"phrase_id": "a002", "candidat_id": "a002-c1", "statut": "resolu", "referents": {"Elle": "Alice", "en": "Alice", "y": "Alice"}, "note": "", "contexte": "Allons, à quoi bon pleurer ainsi, se dit Alice vivement.", "niveau": 2, "auteur": "humain", "horodatage": "2026-11-03T17:02:06"}
  ```

- **bash** `{"command": "grep -n \"validations\\|verdict\\|statut\\|candidat\" reports/rapport-etat-s.md | head -40; echo '===='; sed -n '120,150p' reports/rapport-etat-s.md", "description": "Read existing analysis of uncommitted verdicts"}`

  ```
1:# S — 9/9 paragraphes jugés (19/19), 150 verdicts de banque ; la page `/` sert encore l'ancien arbre plat et la rétro-traduction n'existe pas
4:> désormais séparées. La passe de validation des candidats sur **`/paragraphes`** est **finie** :
5:> 9 paragraphes, 19 candidats,
6:> **19 verdicts**, **0 restant**, **11 acceptés** (10 `resolu` + 1 `compatible`) et **8 exclus**.
7:> La **banque de phrases** (`/`) ne l'est pas : **150 verdicts** sur **74 des 207 phrases**
8:> (35,7 %), **84 lectures acceptées**, mais la page sert les **369 candidats stockés le 02/11**,
9:> **sans `profondeur`** ; la mesure v7, elle, donne **359 candidats** et **99 à profondeur ≥ 3**.
10:> Les référents des 19 verdicts **ne sont pas un gold** : **12 des 28 mappings contredisent la
21:| page `/paragraphes` | **9/9** paragraphes, **19/19** candidats, **11** acceptés / **8** exclus / **1** `compatible` | `paragraphes.json`, `paragraphes-validations.jsonl` |
22:| verdicts `/paragraphes` dans git | **8 committés**, **11 non committés** (a004–a009) | sous-module `523d8c1` + `git status` |
23:| référents des 19 verdicts | **28** mappings, **16** justes, **12** faux, **2** manquants | audit source anglaise (§ 2) 
… [4437 caractères tronqués]
  ```

- **bash** `{"command": "cd tools/structures && grep -rn \"paragraphes-validations\\|candidat_id\\|statut\" --include=*.py . | head -40", "description": "Find validation logic in submodule"}`

  ```
./tests/test_export.py:24:            f.write(json.dumps({"phrase_id": pid, "candidat_id": cid, "verdict": verdict,
./tests/test_export.py:35:        self.assertEqual(lignes[0]["candidat_id"], "p001-c2")
./tests/test_export.py:63:    """Le banc écrit `statut` (resolu/compatible/double_sens) ; le corpus doit le lire."""
./tests/test_export.py:72:    def _statut(self, pid, cid, statut, contexte="", niveau=0):
./tests/test_export.py:74:            f.write(json.dumps({"phrase_id": pid, "candidat_id": cid, "statut": statut,
./tests/test_export.py:79:    def test_dernier_statut_gagne_et_exclu_ne_sort_pas(self):
./tests/test_export.py:80:        self._statut("p001", "p001-c1", "resolu", "Le chat dort.", 2)
./tests/test_export.py:81:        self._statut("p001", "p001-c1", "exclu")
./tests/test_export.py:82:        self._statut("p001", "p001-c2", "double_sens", "Jeu de mots.", 1)
./tests/test_export.py:83:        self._statut("p002", "p002-c1", "compatible")
./tests/test_export.py:88:        self.assertEqual({l["candidat_id"] for l in lignes}, {"p001-c2", "p002-c1"})
./tests/test_export.py:89:        self.assertEqual({l["statut"] for l in lignes}, {"double_sens", "compatible"})
./tests/test
… [2869 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '140,200p' tools/chantier/plan.json", "description": "Read J4 plan entries"}`

  ```
]
  },
  {
   "id": "J4.1",
   "jour": 4,
   "titre": "Coordination N2 — le mètre RoPE",
   "mandat": "Tâche J4.1 : la coordination N2 — le mètre `eval_n2_propre.py` lit les checkpoints RoPE comme des positions absolues (8,02 au lieu de 2,79). **Ne modifie rien dans N2** (ni `entrainer_native.py`, ni `native_model.py`, ni `work/`). Écris une fiche de coordination `reports/rapport-coordination-n2.md` + JSON : le bug, le correctif proposé (--rope), les chiffres, la commande exacte pour la session N2.",
   "budget_min": 90,
   "acceptation": [
    {
     "commande": "test -f reports/rapport-coordination-n2.md && echo FICHE-OK",
     "attendu": "FICHE-OK"
    }
   ]
  },
  {
   "id": "J4.2",
   "jour": 4,
   "titre": "Coordination S — les 11 verdicts",
   "mandat": "Tâche J4.2 : la coordination S — 11 verdicts de `/paragraphes` non committés. **Ne touche pas `tools/structures/`**. Fiche `reports/rapport-coordination-s.md` + JSON : la liste exacte des 11 verdicts (fichier, lignes, statuts), la commande de commit pour la session S, le risque d'un clone à 523d8c1.",
   "budget_min": 90,
   "acceptation": [
    {
     "commande": "test -f reports/rapport-coordination-s.md && echo FICHE-OK"
… [1621 caractères tronqués]
  ```

- **bash** `{"command": "git ls-tree HEAD tools/structures; echo '---'; git log --oneline -8 -- tools/structures; echo '--- parent status of submodule ---'; git diff --submodule=short -- tools/structures | head -20", "description": "Check parent gitlink and history"}`

  ```
160000 commit 523d8c1e8c6ca29ca415360a71bfab6c5b56102c	tools/structures
---
8189c4f3 S — LE FAIT DIVERS EST TRANCHÉ : 61/61 TYPES, 144/144 RÔLES ; LA TÊTE DU GN ARRÊTE LE VERBE
4449646d B13 — LE DÉFAUT DE LA FUSION : LA CONFIANCE (0,7424) BAT LE NIVEAU (0,3432) ; 141/141
047945c5 S — LA BANQUE DE PARAGRAPHES PASSE À NEUF : SIX PAIRES D'ALICE, SOURCES ANGLAISES ET RÉFÉRENTS
59329788 REPRISE — LES QUATRE SESSIONS INTERROMPUES SONT TRIÉES ; ÉTAT AU 04/11
8854fe8f S — LES TROIS LIMITES DE LA V4 SONT FERMÉES : h050, h053, « SI FORT QUE » ; GOLD 60, 60/60 TYPES, 142/142 RÔLES
f92c183b S — LA TRADUCTION CONTRÔLE LE SENS : 14/14 RÉFÉRENTS ANAPHORIQUES CONFIRMÉS, « LES » → « IT » RETROUVÉ ; SOURCE ANGLAISE DANS LA PAGE
af335d0d L — LA FUSION RÉPARÉE : PAR NIVEAU (NEURONAL POS/SYNTAGMES, HEURISTIQUE PRAGMATIQUE) — 0,9309 / 0,8226 / 0,8784 / 0,9954, LE MAXIMUM DES DEUX
ef530713 S — LES SVG RESTENT DANS LEUR CADRE : VIEWBOX CALCULÉ, PAGE RESPONSIVE, DÉFILEMENT ; 52 TESTS
--- parent status of submodule ---
diff --git a/tools/structures b/tools/structures
--- a/tools/structures
+++ b/tools/structures
@@ -1 +1 @@
-Subproject commit 523d8c1e8c6ca29ca415360a71bfab6c5b56102c
+Subproject commit 523d8
… [41 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json, subprocess\nfrom collections import Counter\np='tools/structures/donnees/paragraphes-validations.jsonl'\nwork=[json.loads(l) for l in open(p, encoding='utf-8')]\nhead=subprocess.run(['git','-C','tools/structures','show','HEAD:donnees/paragraphes-validation … [466 caractères tronqués]`

  ```
WORK 19 Counter({'resolu': 10, 'exclu': 8, 'compatible': 1})
HEAD 8 Counter({'resolu': 4, 'exclu': 4})
1 a001 a001-c1 resolu 2026-11-03T16:49:32 REF={"Elle": "Alice", "se": "Alice", "elle": "Alice", "lui": "Alice", "en": "Alice"}
2 a001 a001-c2 resolu 2026-11-03T16:49:59 REF={"Elle": "Alice", "se": "Alice", "elle": "Alice", "lui": "Alice", "en": "Alice"}
3 a002 a002-c1 resolu 2026-11-03T17:02:06 REF={"Elle": "Alice", "en": "Alice", "y": "Alice"}
4 a002 a002-c2 exclu 2026-11-03T17:02:30 REF={"Elle": "Alice", "en": "Alice", "y": "Alice"}
5 a002 a002-c3 exclu 2026-11-03T17:02:43 REF={"Elle": "Alice", "en": "Alice", "y": "Alice"}
6 a003 a003-c1 exclu 2026-11-03T17:05:31 REF={"Elle": "Alice", "sa": "Alice", "elle": "Alice", "se": "Alice"}
7 a003 a003-c2 resolu 2026-11-03T17:05:40 REF={"Elle": "Alice", "sa": "Alice", "elle": "Alice", "se": "Alice"}
8 a003 a003-c3 exclu 2026-11-03T17:06:16 REF={"Elle": "Alice", "sa": "Alice", "elle": "Alice", "se": "Alice"}
9 a004 a004-c1 resolu 2026-11-04T15:03:43 REF={"sa": "ALICE"}
10 a004 a004-c2 exclu 2026-11-04T15:04:02 REF={"sa": "ALICE"}
11 a005 a005-c1 resolu 2026-11-04T15:06:12 REF={"elle": "Alice", "son": "Alice", "en": "coup"}
12 a005 a005-c2 
… [784 caractères tronqués]
  ```

- **bash** `{"command": "cd tools/structures && sed -n '40,130p' serveur.py; echo '=== paragraphes ==='; python3 -c \"\nimport json\nd=json.load(open('donnees/paragraphes.json'))\nprint(type(d), len(d))\nfor p in d:\n    print(p.get('id'), p.get('titre','')[:40], len(p.get('candidats',[])), bool(p.get('source_e … [63 caractères tronqués]`

  ```
class Donnees:
    """Les phrases fixes + deux journaux append-only : validations humaines et évaluations LLM."""

    def __init__(self, dossier: pathlib.Path):
        self.dossier = pathlib.Path(dossier)
        self.verrou = threading.Lock()
        self.fichier_generees = self.dossier / "phrases_generees.json"
        self.fichier_paragraphes = self.dossier / "paragraphes.json"
        self.phrases = json.loads((self.dossier / "phrases.json").read_text(encoding="utf-8"))["phrases"]
        if self.fichier_generees.exists():
            self.phrases += json.loads(self.fichier_generees.read_text(encoding="utf-8"))["phrases"]


    def paragraphes(self) -> list[dict]:
        """Les paragraphes complets : cible, contexte, antécédent, candidats, référents, arbre SVG."""
        if not self.fichier_paragraphes.exists():
            return []
        source = json.loads(self.fichier_paragraphes.read_text(encoding="utf-8"))
        validations = self._journal("paragraphes-validations.jsonl")
        sortie = []
        for p in source.get("paragraphes", []):
            cands = generateur.analyser(p["cible"])
            for k, c in enumerate(cands, 1):
                c["id"] = f'{p
… [4013 caractères tronqués]
  ```

- **bash** `{"command": "cd tools/structures && python3 - <<'PY'\nimport json\nd=json.load(open('donnees/paragraphes.json'))\nprint(list(d))\nps=d['paragraphes']\nprint('n=',len(ps))\nfor p in ps:\n    print(p['id'], '|', p.get('titre','')[:50], '| keys=', list(p)[:12])\nPY", "description": "Inspect paragraph j … [10 caractères tronqués]`

  ```
['version', 'note', 'source', 'paragraphes', 'note_en', 'source_en_url']
n= 9
a001 |  | keys= ['id', 'contexte', 'cible', 'antecedent', 'contexte_en', 'source_en']
a002 |  | keys= ['id', 'contexte', 'cible', 'antecedent', 'contexte_en', 'source_en']
a003 |  | keys= ['id', 'contexte', 'cible', 'antecedent', 'contexte_en', 'source_en']
a004 |  | keys= ['id', 'contexte', 'cible', 'antecedent', 'contexte_en', 'source_en']
a005 |  | keys= ['id', 'contexte', 'cible', 'antecedent', 'contexte_en', 'source_en']
a006 |  | keys= ['id', 'contexte', 'cible', 'antecedent', 'contexte_en', 'source_en']
a007 |  | keys= ['id', 'contexte', 'cible', 'antecedent', 'contexte_en', 'source_en']
a008 |  | keys= ['id', 'contexte', 'cible', 'antecedent', 'contexte_en', 'source_en']
a009 |  | keys= ['id', 'contexte', 'cible', 'antecedent', 'contexte_en', 'source_en']
  ```

- **bash** `{"command": "cd tools/structures && grep -rn \"restant\\|validations\\|candidats\" static/paragraphes.html | head -30", "description": "Inspect page counting logic"}`

  ```
(no output)
  ```

- **bash** `{"command": "cd tools/structures && ls static | head -20; grep -rn \"rest\\|verdict\\|valid\" static/*.js 2>/dev/null | head -20; grep -rn \"restant\" . --include=*.py --include=*.html --include=*.js 2>/dev/null | head -20", "description": "Find restant computation"}`

  ```
app.js
index.html
paragraphes.html
paragraphes.js
style.css
static/app.js:4:let etat = { phrases: [], validations: [], llm: [] };
static/app.js:26:  const v = etat.validations.filter((x) => x.phrase_id === phraseId && x.candidat_id === candId);
static/app.js:31:  const v = etat.validations.filter((x) => x.phrase_id === phrase.id && (x.contexte || "").trim());
static/app.js:37:  const v = etat.validations.filter((x) => x.phrase_id === phrase.id && (x.contexte || "").trim());
static/app.js:44:  $("#s-valides").textContent = etat.validations.length;
static/app.js:45:  const gardes = etat.validations.filter((v) => ["resolu", "compatible", "double_sens"].includes(v.statut)).length;
static/app.js:53:      ? `<span class="verdict resolu">tranché au niveau ${mini}</span>` : "";
static/app.js:58:      const badge = v ? `<span class="verdict ${v.statut}">${v.statut.replace("_", " ")}</span>` : "";
static/app.js:103:async function valider(phraseId, candId, statut) {
static/app.js:107:  const r = await fetch("/api/valider", { method: "POST",
static/app.js:135:  if (b.dataset.s) valider(b.dataset.p, b.dataset.c, b.dataset.s);
static/paragraphes.js:26:  const v = (p.validations || []).filter((x)
… [719 caractères tronqués]
  ```

- **bash** `{"command": "cd tools/structures && sed -n '1,130p' static/paragraphes.js", "description": "Read paragraph page state logic"}`

  ```
const $ = (s) => document.querySelector(s);
const esc = (t) => String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
const STATUTS = [["resolu", "✓ résolu"], ["compatible", "~ compatible"],
                 ["exclu", "✗ exclu"], ["double_sens", "⇄ double sens"]];
let etat = { paragraphes: [] };

function phraseColoree(p, cand) {
  let html = "", curseur = 0;
  for (const s of cand.segments) {
    if (s.debut > curseur) html += esc(p.cible.slice(curseur, s.debut));
    html += `<span class="seg t-${s.type}" title="${s.type} · ${s.role}">${esc(s.texte)}</span>`;
    curseur = s.fin;
  }
  if (curseur < p.cible.length) html += esc(p.cible.slice(curseur));
  return html;
}

function blocs(cand) {
  return cand.segments.map((s) =>
    `<div class="bloc" style="margin-left:${s.niveau * 1.4}em">
       <span class="t-${s.type}">${esc(s.texte.trim())}</span>
       <em>${s.type} · ${s.role} · profondeur ${s.profondeur ?? s.niveau}</em></div>`).join("");
}

function dernier(p, c) {
  const v = (p.validations || []).filter((x) => x.candidat_id === c.id);
  return v.length ? v[v.length - 1] : null;
}

function referentsDe(p) {
  const uniques = new Map();
  for (const 
… [4018 caractères tronqués]
  ```

- **bash** `{"command": "cd tools/structures && echo \"HEAD=$(git rev-parse HEAD)\" && echo \"BLOB_HEAD=$(git rev-parse HEAD:donnees/paragraphes-validations.jsonl)\" && echo \"BLOB_WORK=$(git hash-object donnees/paragraphes-validations.jsonl)\" && sha256sum donnees/paragraphes-validations.jsonl && git show HEAD … [337 caractères tronqués]`

  ```
HEAD=523d8c1e8c6ca29ca415360a71bfab6c5b56102c
BLOB_HEAD=2ada51b5e8f227e65b764f504aae1a6e8a1ef8b4
BLOB_WORK=b34f8f548ed2d2e49c8e577e10fef96537522715
a3c54c9cf2b81904ce43b43685be78f18ed675df2745e7b72ddcf0943d531123  donnees/paragraphes-validations.jsonl
adf23efe0e8ebc77b397295521b1d1fccb4394c4c97e11bb859d0c1d2ada8862  -
TAILLE_WORK=6047
DATE_HEAD=2026-11-04T11:42:34-05:00
BRANCH=master
REMOTE=origin	/home/stephane/Data13TB/stephane/GitHub/drave-structures (fetch) origin	/home/stephane/Data13TB/stephane/GitHub/drave-structures (push)
  ```

- **bash** `{"command": "grep -n \"a001\\|a009\\|9/9\\|19/19\\|verdict\" docs/pilotage/en-cours.md docs/pilotage/roadmap.md | head -40", "description": "Check state docs claims about S verdicts"}`

  ```
docs/pilotage/en-cours.md:51:- **Prochaine action** : **reprise** : poursuivre la validation sur `/paragraphes` (a001–a003 faits, 8 restants), puis la rétro-traduction API et les 71 langues.
docs/pilotage/en-cours.md:64:- **Ce qu'elle fait** : l'API rejoue le gold (mêmes verdicts).
docs/pilotage/en-cours.md:87:- **S — les structures** : 61/61 types, 144/144 rôles, 56 tests, banque 84/67, 8 verdicts de référents ; page **`/paragraphes`**.
docs/pilotage/roadmap.md:31:| **B — l'intelligence** | langue, pensée, jeux, maîtres, [banc externe](../theorie/glossaire/entrees/banc-externe.md), sémantique, modules | ✅ B1–B12 ; **B1.5 [corpus](../theorie/glossaire/entrees/corpus.md)**, **B12.10, B10.2bis et B11.10 closes** ; le **décodeur** est levé (objectif mot : 32,5 ; JW 26,7), le `z` reste ; **B13** (moteur de pensée) : state store v0 + **AC-3/alpha-bêta** + **[DRVF](../theorie/glossaire/entrees/drvf.md) `thought`** + **[banc](../theorie/glossaire/entrees/banc.md) anytime** + **opérateurs hétérogènes** + **nécessaire** + **labyrinthe** + **[porte](../theorie/glossaire/entrees/porte.md)** + **apprise** + **courbe** + **seule** + **stochastique** + **sto seule** + **ferme** + **minute** + **
… [4538 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '100,180p' reports/rapport-etat-s.md", "description": "Read referent audit details"}`

  ```
le signal mesuré est bien le **sens lexical**, pas la structure de phrase.

**Ce qui pourrait le rendre faux.** Les 1 433 couples incluent 4 clés de variantes ; le compte
canonique est **1 429**. La détection de langue n'est pas stable au cas près : cinq runs donnent
**340, 342, 343, 343, 344** sur 449 — le taux (~76 %) est stable, le chiffre exact non ; la cause
probable est un départage non déterministe (hash), non élucidée. Le docstring de
`lexique_multilingue.py` dit encore « 53 langues » alors que la donnée en porte 71 : dérive de
documentation, sans effet sur la mesure. Enfin, 5 langues n'ont aucun item : le « 71/71 » de la
notation ne veut pas dire « 71/71 testées sur le corpus ».

## 2. La page `/paragraphes` : 9/9, 19/19, et le faux « 8 restants »

**Le compte.** `donnees/paragraphes.json` porte **9 paragraphes** (a001–a009), tous issus d'Alice.
Le serveur régénère leurs candidats à la volée (`generateur.analyser`) : **2, 3, 3, 2, 2, 1, 2, 1,
3** candidats, soit **19**. `paragraphes-validations.jsonl` porte **19 verdicts** : **10
`resolu`**, **8 `exclu`**, **1 `compatible`**, **0 `double_sens`**. Au sens de la page (résolu +
compatible + double sens), **11 lectures sont ac
… [4138 caractères tronqués]
  ```

- **bash** `{"command": "echo \"PARENT_BRANCH=$(git branch --show-current)\"; echo \"PARENT_REMOTE=$(git remote -v | tr '\\n' ' ')\"; echo '--- submodule status detail ---'; git -C tools/structures status --short --branch; echo '--- numstat ---'; git -C tools/structures diff --numstat; echo '--- porcelaine pare … [111 caractères tronqués]`

  ```
PARENT_BRANCH=s/v7
PARENT_REMOTE=origin	git@github.com:stephanedenis/drave.git (fetch) origin	git@github.com:stephanedenis/drave.git (push) 
--- submodule status detail ---
## master...origin/master
 M donnees/paragraphes-validations.jsonl
--- numstat ---
11	0	donnees/paragraphes-validations.jsonl
--- porcelaine parent ---
 M tools/structures
  ```

- **bash** `{"command": "ls -l reports/rapport-coordination-s.md reports/rapport-coordination-s.json 2>&1; echo '---'; ls reports/ | grep coordination", "description": "Check target files existence"}`

  ```
ls: cannot access 'reports/rapport-coordination-s.md': No such file or directory
ls: cannot access 'reports/rapport-coordination-s.json': No such file or directory
---
rapport-coordination-n2.json
rapport-coordination-n2.md
  ```

- **bash** `{"command": "set -e\ntmp=$(mktemp -d /tmp/coord-s-clone.XXXXXX)\ntrap 'rm -rf -- \"$tmp\"' EXIT\ngit clone -q tools/structures \"$tmp/structures\"\ncd \"$tmp/structures\"\necho \"CLONE_HEAD=$(git rev-parse HEAD)\"\necho \"CLONE_STATUS=$(git status --porcelain | wc -l) ligne(s)\"\necho \"CLONE_LIGNES … [570 caractères tronqués]`

  ```
CLONE_HEAD=523d8c1e8c6ca29ca415360a71bfab6c5b56102c
CLONE_STATUS=0 ligne(s)
CLONE_LIGNES=8
CLONE_VERDICTS 8 {'resolu': 4, 'exclu': 4}
CLONE_ACCEPTES 4
CLONE_PHRASES ['a001', 'a002', 'a003']
adf23efe0e8ebc77b397295521b1d1fccb4394c4c97e11bb859d0c1d2ada8862  donnees/paragraphes-validations.jsonl
  ```

- **bash** `{"command": "git show --stat --oneline 047945c5 | head -30; echo '==='; git show --stat --oneline 8189c4f3 | head -25; echo '==='; git log --oneline -5 -- tools/structures", "description": "Inspect parent pointer commit style"}`

  ```
047945c5 S — LA BANQUE DE PARAGRAPHES PASSE À NEUF : SIX PAIRES D'ALICE, SOURCES ANGLAISES ET RÉFÉRENTS
 docs/pilotage/en-cours.md                          |   2 +-
 journal/2026-11-04/README.md                       |   6 +-
 journal/2026-11-04/docs.md                         |   2 +-
 journal/2026-11-04/mesures.md                      |  23 +++
 journal/2026-11-04/modele.md                       |   2 +-
 journal/README.md                                  |   8 +-
 journal/THEMES.md                                  |   1 +
 .../0733c5bb-f90b-4f58-9241-3364fa32e46c/digest.md |  64 ++++++++
 .../rapport.md                                     |  15 +-
 .../29ad180d-38a5-4481-a9a7-ec6ab31c895f/digest.md | 146 +++++++++++++++++
 .../rapport.md                                     |  25 ++-
 journal/sessions/MANIFEST.md                       |  10 +-
 .../aeafe951-9c3d-4bb5-8af7-0246a4f3d51d/digest.md | 149 +++++++++++++++++
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md | 176 +++++++++++++++++++++
 .../rapport.md                                     |  13 +-
 reports/INDEX.md                                   |   1 +
 reports/rapport-s-paragraphes.md                   |  58 +++++++
… [2197 caractères tronqués]
  ```

- **bash** `{"command": "cd tools/structures && git show --stat --oneline 7ccc60f | head -20; echo '==='; git show 7ccc60f --format='%B' -s", "description": "Inspect prior human validation commit"}`

  ```
7ccc60f S — VALIDATION HUMAINE : 8 VERDICTS DE RÉFÉRENTS SUR /PARAGRAPHES (a001–a003) + 8 VERDICTS BANQUE (p003, c010, c066, c067)
 donnees/llm.jsonl                     | 2 ++
 donnees/paragraphes-validations.jsonl | 8 ++++++++
 donnees/validations.jsonl             | 8 ++++++++
 3 files changed, 18 insertions(+)
===
S — VALIDATION HUMAINE : 8 VERDICTS DE RÉFÉRENTS SUR /PARAGRAPHES (a001–a003) + 8 VERDICTS BANQUE (p003, c010, c066, c067)
  ```

- **bash** `{"command": "cd tools/structures && head -50 generateur.py; echo '---'; grep -n \"def analyser\\|def referents\\|if __name__\" generateur.py", "description": "Inspect generator entry points"}`

  ```
#!/usr/bin/env python3
"""generateur.py — une phrase brute → des structures candidates (v0 heuristique).

Ce n'est pas un analyseur syntaxique : c'est un **générateur de candidats** à faire valider par
un humain. Il segmente (GN, GV, GP, REL, SUB), devine des rôles par la préposition, puis produit
plusieurs candidats en variant l'**attachement** de chaque segment ambigu (GN le plus proche ou
GV le plus proche).

    python3 generateur.py "Le chat de la voisine qui dort sur le toit se réveille."
    python3 generateur.py --json "..."     # la structure complète
"""
from __future__ import annotations

import json
import re
import unicodedata

DET = set("le la les l un une ce cet cette ces mon ma mes ton ta tes son sa ses "
          "notre nos votre vos leur leurs quel quelle quels quelles".split())
PREP = set("a au aux de du des d en dans par pour sur sous avec sans chez vers entre depuis "
           "pendant durant contre malgre selon pres loin devant derriere apres avant".split())
RELATIFS = set("qui que qu dont ou quoi".split())
CONJ = set("et ou mais donc or ni car quand comme si parce puisque lorsque pendant quoique".split())
COORD = set("et ou mais donc or ni car".split())
SU
… [2026 caractères tronqués]
  ```

- **bash** `{"command": "cd tools/structures && git show HEAD:donnees/paragraphes.json | python3 -c \"\nimport json,sys\nd=json.load(sys.stdin)\nprint(len(d['paragraphes']), [p['id'] for p in d['paragraphes']])\n\"", "description": "Verify committed paragraph count"}`

  ```
9 ['a001', 'a002', 'a003', 'a004', 'a005', 'a006', 'a007', 'a008', 'a009']
  ```

- **bash** `{"command": "cd tools/structures && python3 -B - <<'PY'\nimport json, generateur\nfrom collections import Counter\nps=json.load(open('donnees/paragraphes.json',encoding='utf-8'))['paragraphes']\nval=[json.loads(l) for l in open('donnees/paragraphes-validations.jsonl',encoding='utf-8') if l.strip()]\ … [553 caractères tronqués]`

  ```
CANDIDATS 19 {'a001': 2, 'a002': 3, 'a003': 3, 'a004': 2, 'a005': 2, 'a006': 1, 'a007': 2, 'a008': 1, 'a009': 3}
SANS_VERDICT 0 []
VERDICTS_SANS_CANDIDAT []
  ```

- **bash** `{"command": "cat .gitmodules 2>/dev/null; echo '---'; git config -f .gitmodules --get-regexp 'submodule\\..*' 2>/dev/null; echo '--- pycache check ---'; git -C tools/structures status --porcelain", "description": "Check submodule config and cleanliness"}`

  ```
[submodule "tools/docwatch"]
	path = tools/docwatch
	url = https://github.com/stephanedenis/docwatch.git
[submodule "tools/structures"]
	path = tools/structures
	url = /home/stephane/Data13TB/stephane/GitHub/drave-structures
---
submodule.tools/docwatch.path tools/docwatch
submodule.tools/docwatch.url https://github.com/stephanedenis/docwatch.git
submodule.tools/structures.path tools/structures
submodule.tools/structures.url /home/stephane/Data13TB/stephane/GitHub/drave-structures
--- pycache check ---
 M donnees/paragraphes-validations.jsonl
  ```

- **bash** `{"command": "grep -n \"coordination-n2\\|coordination-s\" reports/INDEX.md | head; echo '---'; head -30 reports/INDEX.md", "description": "Check reports index convention"}`

  ```
---
# Index des fiches de reports/

> **Généré** par `tools/index_reports.py` — **710 fiches**. Les fichiers
> d'infrastructure (`README.md`, `INDEX.md`, `historique-*`) sont exclus du tableau ;
> la page d'état, elle, compte tous les `.md` de `reports/`.

| fiche | titre |
|---|---|
| [07-mesures-couche-commune.md](07-mesures-couche-commune.md) | 7. Les modèles alternatifs pour l'entrée et la sortie — vers une couche commune |
| [aiguille-30b.md](aiguille-30b.md) | aiguille v2 — /home/stephane/Data13TB/stephane/modeles/gguf/Qwen3-30B-A3B-Instruct-2507-Q4_K_M.gguf |
| [aiguille-gpt-oss.md](aiguille-gpt-oss.md) | aiguille v2 — /home/stephane/Data13TB/stephane/modeles/gguf/gpt-oss-120b-MXFP4.gguf |
| [alignement-verne.md](alignement-verne.md) | Alignement phrase à phrase — *Le Tour du monde en quatre-vingts jours* (français → anglais) |
| [bilan-b11.md](bilan-b11.md) | Bilan B11 — ce qui tient, ce qui ne tient pas |
| [bilan-multi-materiel.md](bilan-multi-materiel.md) | Bilan multi-matériel — CPU, FPGA, GPU |
| [campagne-benefices.md](campagne-benefices.md) | Campagne 24 h — où Drave est à son meilleur, tâche par tâche |
| [fiche-nuit-17-10.md](fiche-nuit-17-10.md) | La nuit du 17 au
… [1968 caractères tronqués]
  ```

- **bash** `{"command": "cd tools/structures && python3 -B - <<'PY'\nimport json\nps=json.load(open('donnees/paragraphes.json',encoding='utf-8'))['paragraphes']\nfor p in ps:\n    if p['id'] >= 'a004':\n        print(p['id'], '| ant=', p['antecedent'], '| cible=', p['cible'][:90])\nPY", "description": "Read a00 … [27 caractères tronqués]`

  ```
a004 | ant= Alice | cible= ALICE, assise auprès de sa sœur sur le gazon, commençait à s'ennuyer de rester là à ne rie
a005 | ant= Alice | cible= Tout à coup elle rencontra sur son passage une petite table à trois pieds, en verre massif
a006 | ant= Alice | cible= Comme cela n'avançait à rien de passer son temps à attendre à la petite porte, elle retour
a007 | ant= Alice | cible= C'est bien facile à dire « Buvez-moi », mais Alice était trop fine pour obéir à l'aveuglet
a008 | ant= Alice | cible= « Je me sens toute drôle, » dit Alice, « on dirait que je rentre en moi-même et que je me 
a009 | ant= Alice | cible= Un moment après, voyant qu'il ne se passait plus rien, elle se décida à aller de suite au
  ```

- **bash** `{"command": "cd tools/structures && echo \"SIZE_HEAD=$(git cat-file -s 2ada51b5e8f227e65b764f504aae1a6e8a1ef8b4)\" && echo \"SIZE_WORK=$(git cat-file -s b34f8f548ed2d2e49c8e577e10fef96537522715)\" && echo \"LIGNES_HEAD=$(git show HEAD:donnees/paragraphes-validations.jsonl | wc -l)\" && echo \"LIGNES … [129 caractères tronqués]`

  ```
SIZE_HEAD=2390
SIZE_WORK=
LIGNES_HEAD=8
LIGNES_WORK=19
11	0	donnees/paragraphes-validations.jsonl
[stderr]
fatal: git cat-file: could not get object info
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/rapport-coordination-n2.json'))\nprint(list(d))\nfor k in list(d)[-8:]:\n    print('\\n##',k)\n    print(json.dumps(d[k],ensure_ascii=False,indent=1)[:800])\nPY", "description": "Inspect N2 JSON end sections"}`

  ```
['date', 'head', 'ligne', 'objet', 'fiche', 'verdict', 'aucune_modification_n2', 'bug', 'checkpoints', 'chiffres', 'correctif', 'commande_n2', 'limites', 'fichiers_lus_non_modifies', 'references']

## bug
{
 "fichier": "tools/eval_n2_propre.py",
 "symptome": "val 8,0225 au lieu de 2,9726 à 128 et 2,7856 à 1024 sur work/n2ac/propre512-8k.pt",
 "causes": [
  {
   "rang": 1,
   "nom": "architecture",
   "detail": "charge() construit NativeModel (table de positions apprise absolue) au lieu de NativeModelRoPE ; les checkpoints N2 depuis le 02/11 sont des NativeModelRoPE, avec les mêmes noms de tenseurs et self.pos inutilisé.",
   "silence": "load_state_dict(strict=False) : 127 clés, 0 manquante, 0 inattendue ; pos.weight est chargé et appliqué par le NativeModel absolu, alors que le modèle RoPE ne l'a jamais appris."
  },
  {
   "rang": 2,
   "nom": "canal",
   "detail": "ppl_protocole() appelle m(x[:, :-1]) sans canal ; le checkpoint de la porte a été entraîné avec --canal data/corpus_propre/tr

## checkpoints
{
 "porte": {
  "fichier": "work/n2ac/propre512-8k.pt",
  "date": "2026-11-03 02:01",
  "octets": 137248474,
  "sha256": "37c5673b3d51f6f871c4391b97015b401f73c842d04d4a05f78a70c2
… [4528 caractères tronqués]
  ```

- **bash** `{"command": "git rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>&1; echo '---'; git -C tools/structures rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>&1; echo '---'; git status --short --branch | head -3", "description": "Check upstream branches"}`

  ```
fatal: no upstream configured for branch 's/v7'
---
origin/master
---
## s/v7
 M docs/pilotage/references-non-regression.md
D  journal/2026-11-13/README.md
  ```

- **bash** `{"command": "git branch -r | grep -E 's/v7|master|main' | head -10; echo '---'; git ls-remote --heads origin 's/v7' 2>&1 | head -5", "description": "Check remote branch existence"}`

  ```
origin/HEAD -> origin/master
  origin/master
  origin/s/v7
---
ced219338dabec2554c3a32d7c95ee8e8cdbfac0	refs/heads/s/v7
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/drave-structures 2>/dev/null && { echo \"BARE=$(git rev-parse --is-bare-repository)\"; echo \"HEAD=$(git rev-parse --short HEAD)\"; echo \"BRANCH=$(git branch --show-current)\"; git config --get receive.denyCurrentBranch || echo 'denyCurrentBra … [99 caractères tronqués]`

  ```
BARE=false
HEAD=523d8c1
BRANCH=master
updateInstead
  ```

### 🤖 Assistant

Now I have the exact state. Let me write the coordination sheet and its JSON, without modifying the submodule.

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-s.md", "content": "# S — les 11 verdicts de `/paragraphes` ne sont pas dans git\n\n> **Ligne de roadmap** : S · **Date** : 2026-11-13 · **HEAD parent mesuré** : `ced21933`\n> · **Sous-module `tools/structures … [16806 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-s.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **write** `{"content": "{\n  \"date\": \"2026-11-13\",\n  \"head\": \"ced21933\",\n  \"head_parent\": \"ced219338dabec2554c3a32d7c95ee8e8cdbfac0\",\n  \"ligne\": \"S\",\n  \"objet\": \"coordination S : les 11 verdicts de /paragraphes non committés\",\n  \"fiche\": \"reports/rapport-coordination-s.md\",\n  \"ve … [19540 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-s.json</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "python3 -m json.tool reports/rapport-coordination-s.json > /dev/null && echo 'JSON-OK'; python3 - <<'PY'\nimport json\nfrom collections import Counter\nj=json.load(open('reports/rapport-coordination-s.json'))\nrows=[json.loads(l) for l in open('tools/structures/donnees/paragraphes-valid … [558 caractères tronqués]`

  ```
JSON-OK
JSON vs JSONL: 11/11 lignes et champs identiques
statuts Counter({'resolu': 6, 'exclu': 4, 'compatible': 1}) acceptes 7
lignes [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
  ```

- **bash** `{"command": "echo '--- submodule status ---'; git -C tools/structures status --porcelain; echo '--- pycache/untracked ---'; git -C tools/structures status --porcelain --untracked-files=all | head; echo '--- parent new files ---'; git status --short -- reports/rapport-coordination-s.md reports/rappor … [99 caractères tronqués]`

  ```
--- submodule status ---
 M donnees/paragraphes-validations.jsonl
--- pycache/untracked ---
 M donnees/paragraphes-validations.jsonl
--- parent new files ---
 m tools/structures
?? reports/rapport-coordination-s.json
?? reports/rapport-coordination-s.md
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json,re,os\nbase='reports'\ntxt=open('reports/rapport-coordination-s.md',encoding='utf-8').read()\nlinks=re.findall(r'\\]\\(([^)#]+)(?:#[^)]*)?\\)',txt)\nbad=[]\nfor l in links:\n    if l.startswith('http'): continue\n    p=os.path.normpath(os.path.join(base,l)) … [519 caractères tronqués]`

  ```
liens 5 mauvais []
occurrences 26 uniques 16
  ```

- **bash** `{"command": "grep -n '^|' reports/rapport-coordination-s.md | wc -l; echo '--- headings ---'; grep -n '^#' reports/rapport-coordination-s.md; echo '--- word count ---'; wc -w reports/rapport-coordination-s.md", "description": "Inspect sheet structure"}`

  ```
50
--- headings ---
1:# S — les 11 verdicts de `/paragraphes` ne sont pas dans git
18:## Ce que cette fiche est, et n'est pas
29:## 1. Les 11 verdicts, ligne à ligne
75:### 1.1 Les référents enregistrés (inchangés par le commit)
104:## 2. Ce que git voit, ce que le working tree voit
106:### 2.1 Les totaux
125:### 2.2 Par paragraphe
145:### 2.3 Ce que le commit ne répare pas
152:## 3. La commande de commit pour la session S
162:# 1. vérifier l'état : un seul fichier, 11 ajouts, 0 suppression
164:# attendu : " M donnees/paragraphes-validations.jsonl" et rien d'autre
166:# attendu : 11	0	donnees/paragraphes-validations.jsonl
168:# 2. committer les 11 verdicts (add explicite)
172:# 3. publier le sous-module AVANT le pointeur parent
175:# 4. avancer le pointeur dans le dépôt parent
187:# attendu : 1 file changed, 11 insertions(+)
189:# attendu : 19
193:# attendu : 160000 commit <nouveau_sha> tools/structures, plus 523d8c1
202:## 4. Le risque d'un clone à `523d8c1`
204:### 4.1 Le contrôle négatif, mesuré
220:### 4.2 Les risques, par gravité
251:### 4.3 Ce que le commit change, et ce qu'il ne change pas
259:## 5. Ce qui pourrait rendre cette fiche fausse
279:## 6. Fichiers lus, non modifi
… [81 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '158,180p' reports/rapport-coordination-s.md | cat -A | head -25", "description": "Check tabs in command block"}`

  ```
$
```bash$
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures$
$
# 1. vM-CM-)rifier l'M-CM-)tat : un seul fichier, 11 ajouts, 0 suppression$
git status --porcelain$
# attendu : " M donnees/paragraphes-validations.jsonl" et rien d'autre$
git diff --numstat$
# attendu : 11^I0^Idonnees/paragraphes-validations.jsonl$
$
# 2. committer les 11 verdicts (add explicite)$
git add donnees/paragraphes-validations.jsonl$
git commit -m "S M-bM-^@M-^T VALIDATION HUMAINE : 11 VERDICTS SUR /PARAGRAPHES (a004M-bM-^@M-^Sa009), 7 ACCEPTM-CM-^IS (6 RM-CM-^ISOLUS, 1 COMPATIBLE), 4 EXCLUS"$
$
# 3. publier le sous-module AVANT le pointeur parent$
git push origin master$
$
# 4. avancer le pointeur dans le dM-CM-)pM-CM-4t parent$
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet$
git add tools/structures$
git commit -m "S M-bM-^@M-^T POINTEUR : 11 VERDICTS /PARAGRAPHES (a004M-bM-^@M-^Sa009) COMMITTM-CM-^IS"$
git push origin s/v7$
```$
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-s.md", "limit": 120}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-s.md</path>
<type>file</type>
<content>
1: # S — les 11 verdicts de `/paragraphes` ne sont pas dans git
2: 
3: > **Ligne de roadmap** : S · **Date** : 2026-11-13 · **HEAD parent mesuré** : `ced21933`
4: > · **Sous-module `tools/structures`** : `523d8c1` · **Verdict** : les 11 verdicts a004–a009
5: > sont **11 lignes non committées** de `donnees/paragraphes-validations.jsonl` (lignes **9–19**)
6: > : **6 `resolu`, 1 `compatible`, 4 `exclu`**, soit **7 acceptés et 4 exclus**. Le working tree
7: > voit **19 verdicts / 11 acceptés / 0 candidat sans verdict** ; un clone à `523d8c1` voit
8: > **8 verdicts / 4 acceptés / 11 candidats sans verdict**. **Aucun fichier de `tools/structures/`
9: > n'est modifié par cette fiche** : l'unique modification du sous-module est celle des 11
10: > verdicts, antérieure à la fiche.
11: 
12: **En trois lignes.** (1) Les 11 verdicts sont des verdicts de **candidat**, pas de paragraphe :
13: six paragraphes (`a004`–`a009`), onze candidats, ajoutés le **2026-11-04** entre **15:03:43** et
14: **15:10:08**. (2) Le fichier est **append-only** et le diff est **+11 / −0** ; rien n
… [6276 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-s.md", "offset": 121, "limit": 180}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-s.md</path>
<type>file</type>
<content>
121: seconds sont la somme des acceptés sur les 19 verdicts (a001–a009). Un clone à `523d8c1` n'a que
122: **4 acceptés** et **8 verdicts**. Les deux chiffres « 11 » sont vrais, mais dans deux ensembles
123: différents ; les confondre est l'erreur que la fiche `rapport-etat-s.md` avait déjà relevée.
124: 
125: ### 2.2 Par paragraphe
126: 
127: | phrase | candidats | verdicts HEAD | verdicts working | dont les 11 non committés |
128: |---|---:|---:|---:|---|
129: | a001 | 2 | 2 | 2 | — |
130: | a002 | 3 | 3 | 3 | — |
131: | a003 | 3 | 3 | 3 | — |
132: | a004 | 2 | **0** | 2 | c1 `resolu`, c2 `exclu` |
133: | a005 | 2 | **0** | 2 | c1 `resolu`, c2 `exclu` |
134: | a006 | 1 | **0** | 1 | c1 `resolu` |
135: | a007 | 2 | **0** | 2 | c1 `resolu`, c2 `exclu` |
136: | a008 | 1 | **0** | 1 | c1 `compatible` |
137: | a009 | 3 | **0** | 3 | c1 `resolu`, c2 `exclu`, c3 `resolu` |
138: | **total** | **19** | **8** | **19** | **11** |
139: 
140: Les 19 candidats sont **régénérés à la volée** par `generateur.analyser` (comptes 2, 3, 3, 2, 2, 1,
141: 2, 1, 3) : ils ne sont pas
… [9741 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-s.md", "old_string": "  `tools/structures` dans le parent : sans les deux, un clone reste à 8 verdicts.", "new_string": "  `tools/structures` dans le parent : sans les deux, un clone du parent reste à 8 verdi … [6 caractères tronqués]`

  ```
Error: old_string was not found in "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-s.md"
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-s.md", "old_string": "- **Ne tranche pas** la qualité des référents enregistrés : elle la signale (§ 2.3), parce que le", "new_string": "- **Ne tranche pas** la qualité des référents enregistrés : elle la sig … [28 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-s.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-s.md", "old_string": "# attendu : 160000 commit <nouveau_sha> tools/structures, plus 523d8c1", "new_string": "# attendu : 160000 commit <nouveau_sha> tools/structures (et non plus 523d8c1)"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-s.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-s.md", "new_string": "`tools/structures` dans le parent : sans les deux, un clone du parent reste à 8 verdicts.", "old_string": "`tools/structures` dans le parent : sans les deux, un clone reste à 8 verdicts. … [2 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-s.md has been updated successfully.
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json, subprocess, hashlib, os, re\nfrom collections import Counter\nbase='/home/stephane/Data13TB/stephane/GitHub/Qtrinet'\nos.chdir(base)\nj=json.load(open('reports/rapport-coordination-s.json',encoding='utf-8'))\nmd=open('reports/rapport-coordination-s.md',enc … [1506 caractères tronqués]`

  ```
AUDIT-OK : 11 lignes, statuts, hashes, totaux et présence dans la fiche
  ```

- **bash** `{"command": "python3 -m json.tool reports/rapport-coordination-s.json > /dev/null && echo JSON-OK; git -C tools/structures status --porcelain; git status --short -- reports/rapport-coordination-s.md reports/rapport-coordination-s.json", "description": "Final JSON and status checks"}`

  ```
JSON-OK
 M donnees/paragraphes-validations.jsonl
?? reports/rapport-coordination-s.json
?? reports/rapport-coordination-s.md
  ```

- **bash** `{"command": "ls -d /tmp/coord-s-clone.* 2>/dev/null || echo 'aucun clone temporaire restant'", "description": "Confirm temporary clone cleanup"}`

  ```
aucun clone temporaire restant
  ```

- **bash** `{"command": "git diff --stat -- reports/rapport-coordination-s.md reports/rapport-coordination-s.json; wc -l -w reports/rapport-coordination-s.md reports/rapport-coordination-s.json", "description": "Summarize deliverables"}`

  ```
298  2632 reports/rapport-coordination-s.md
  528  1831 reports/rapport-coordination-s.json
  826  4463 total
  ```

- **bash** `{"command": "cd tools/structures && git hash-object donnees/paragraphes-validations.jsonl && sha256sum donnees/paragraphes-validations.jsonl && git rev-parse HEAD", "description": "Reconfirm hashes unchanged"}`

  ```
b34f8f548ed2d2e49c8e577e10fef96537522715
a3c54c9cf2b81904ce43b43685be78f18ed675df2745e7b72ddcf0943d531123  donnees/paragraphes-validations.jsonl
523d8c1e8c6ca29ca415360a71bfab6c5b56102c
  ```

- **bash** `{"command": "git -C /home/stephane/Data13TB/stephane/GitHub/drave-structures status --porcelain | head -10; echo \"exit=$?\"", "description": "Check submodule origin cleanliness"}`

  ```
exit=0
  ```

- **bash** `{"command": "grep -n '[[:blank:]]$' reports/rapport-coordination-s.md reports/rapport-coordination-s.json | head -10; echo \"exit=$?\"", "description": "Check trailing whitespace"}`

  ```
exit=0
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nj=json.load(open('reports/rapport-coordination-s.json'))\nprint('clés:', list(j))\nprint('verdicts:', len(j['verdicts_non_committes']))\nprint('lignes:', len(open('reports/rapport-coordination-s.md').read().splitlines()))\nPY", "description": "Final struct … [14 caractères tronqués]`

  ```
clés: ['date', 'head', 'head_parent', 'ligne', 'objet', 'fiche', 'verdict', 'aucune_modification_s', 'lecture_seule', 'sous_module', 'fichier', 'verdicts_non_committes', 'bilan_non_committes', 'etat', 'referent_audit', 'commande_s', 'risque_clone', 'ce_qui_pourrait_le_rendre_faux', 'fichiers_lus_non_modifies', 'references']
verdicts: 11
lignes: 298
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py --help 2>&1 | head -30", "description": "Check documentation review usage"}`

  ```
revue de documentation · 715 fiche(s) · 808 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ❌ 2 anomalie(s) :
     · compteurs : en-cours.md dit 713 fichiers, le disque en a 715
     · compteurs : en-cours.md dit 806 JSON, le disque en a 808
  ```

- **bash** `{"command": "grep -n \"713\\|806\\|715\\|808\\|fichiers\\|JSON\" docs/pilotage/en-cours.md | head -20; echo '--- tool logic ---'; grep -n \"fichiers\\|JSON\\|compteurs\\|disque\" tools/revue_documentation.py | head -40", "description": "Inspect counter discrepancy"}`

  ```
102:| fichiers / JSON de résultats | **713** / **806** | `reports/*.md` / `reports/*.json` |
--- tool logic ---
12:     les compteurs de la page d'état sont ceux du disque (portes, chapitres, fiches, docs) ;
80:    """Les fichiers vivants dont les liens comptent pour la navigation (orphelins)."""
93:    """Les fichiers dont les liens doivent résoudre (docs, fiches courantes, racine)."""
172:    # 5. compteurs : la page d'état est la source unique, et elle dit le disque
176:    fiches = re.search(r"\|\s*fichiers / JSON de résultats\s*\|\s*\*\*(\d+)\*\*\s*/\s*\*\*(\d+)\*\*", t)
177:    for nom, valeur, disque in (
183:            alertes.append(f"compteurs : la ligne « {nom} » manque dans en-cours.md")
184:        elif valeur != disque:
185:            alertes.append(f"compteurs : en-cours.md dit {valeur} {nom}, le disque en a {disque}")
187:        alertes.append("compteurs : la ligne « fichiers / JSON » manque dans en-cours.md")
189:        for valeur, disque, quoi in (
190:            (int(fiches.group(1)), compte_fiches(), "fichiers"),
191:            (int(fiches.group(2)), compte_json(), "JSON"),
193:            if valeur != disque:
195:                    f"compteurs : en-cours
… [341 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py > /tmp/revue-j42.txt 2>&1; echo \"exit=$?\"; cat /tmp/revue-j42.txt", "description": "Run documentation review and capture result"}`

  ```
exit=1
  revue de documentation · 715 fiche(s) · 808 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ❌ 2 anomalie(s) :
     · compteurs : en-cours.md dit 713 fichiers, le disque en a 715
     · compteurs : en-cours.md dit 806 JSON, le disque en a 808
  ```

- **bash** `{"command": "date '+%Y-%m-%d %H:%M:%S %Z'", "description": "Check current system date"}`

  ```
2026-11-13 21:58:03 EST
  ```

- **bash** `{"command": "cd tools/structures && python3 -B - <<'PY'\nimport json\nps={p['id']:p for p in json.load(open('donnees/paragraphes.json',encoding='utf-8'))['paragraphes']}\nrows=[json.loads(l) for l in open('donnees/paragraphes-validations.jsonl',encoding='utf-8') if l.strip()]\nfor r in rows:\n    if … [330 caractères tronqués]`

  ```
a004 contexte_verdict= '' | contexte_paragraphe= '' | egal= True
a005 contexte_verdict= 'Il y avait des portes tout autour de la salle ; elles étaient toutes fermées ;  | contexte_paragraphe= 'Il y avait des portes tout autour de la salle ; elles étaient toutes fermées ;  | egal= True
a006 contexte_verdict= "Alice ouvrit la porte, et vit qu'elle conduisait dans un étroit passage ; elle  | contexte_paragraphe= "Alice ouvrit la porte, et vit qu'elle conduisait dans un étroit passage ; elle  | egal= True
a007 contexte_verdict= 'Cette fois elle trouva sur la table une petite bouteille, et au cou de la boute | contexte_paragraphe= 'Cette fois elle trouva sur la table une petite bouteille, et au cou de la boute | egal= True
a008 contexte_verdict= "Cependant, comme cette bouteille n'était pas marquée « Poison », Alice se hasar | contexte_paragraphe= "Cependant, comme cette bouteille n'était pas marquée « Poison », Alice se hasar | egal= True
a009 contexte_verdict= 'Elle attendit pourtant quelques minutes, pour voir si elle allait rapetisser en | contexte_paragraphe= 'Elle attendit pourtant quelques minutes, pour voir si elle allait rapetisser en | egal= True
  ```

- **bash** `{"command": "set -e\nbase=/home/stephane/Data13TB/stephane/GitHub/Qtrinet\ntmp=$(mktemp -d /tmp/j42-commit-test.XXXXXX)\ntrap 'rm -rf -- \"$tmp\"' EXIT\ngit clone -q \"$base/tools/structures\" \"$tmp/s\"\ncp \"$base/tools/structures/donnees/paragraphes-validations.jsonl\" \"$tmp/s/donnees/paragraphe … [922 caractères tronqués]`

  ```
M donnees/paragraphes-validations.jsonl
--- show ---
f5f7439 S — VALIDATION HUMAINE : 11 VERDICTS SUR /PARAGRAPHES (a004–a009), 7 ACCEPTÉS (6 RÉSOLUS, 1 COMPATIBLE), 4 EXCLUS
 donnees/paragraphes-validations.jsonl | 11 +++++++++++
 1 file changed, 11 insertions(+)
--- lignes ---
19
--- clone du commit ---
19
19 {'resolu': 10, 'exclu': 8, 'compatible': 1} 11
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-s.md", "new_string": "**Pourquoi deux commits et deux push.** Le parent ne stocke qu'un **pointeur** (gitlink) vers le\nsous-module. Committer le sous-module sans avancer le pointeur laisse un clone du parent … [988 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-s.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-s.json", "new_string": "    \"pourquoi_deux_commits\": \"Le parent ne stocke qu'un gitlink. Committer le sous-module sans avancer le pointeur laisse un clone du parent à 523d8c1 ; avancer le pointeur sans pub … [629 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-s.json has been updated successfully.
  ```

- **bash** `{"command": "python3 -m json.tool reports/rapport-coordination-s.json > /dev/null && echo JSON-OK; python3 - <<'PY'\nimport json\nj=json.load(open('reports/rapport-coordination-s.json'))\nprint(j['commande_s']['controle'])\nPY", "description": "Validate JSON after addition"}`

  ```
JSON-OK
{'dispositif': 'commande du sous-module rejouée dans un clone jetable, sans push', 'resultat': '1 file changed, 11 insertions(+) ; un clone de ce commit voit 19 verdicts (10 resolu, 1 compatible, 8 exclu) et 11 acceptés'}
  ```

- **bash** `{"command": "grep -n \"Contrôle de la commande\" -A 4 reports/rapport-coordination-s.md; echo '--- submodule status ---'; git -C tools/structures status --porcelain", "description": "Check added control text and submodule"}`

  ```
202:**Contrôle de la commande.** Rejouée dans un clone **jetable** du sous-module (sans push), la
203-commande du sous-module donne `1 file changed, 11 insertions(+)` ; un clone de ce commit voit
204-**19 verdicts** (10 `resolu`, 1 `compatible`, 8 `exclu`) et **11 acceptés**. La commande est donc
205-mécaniquement valide ; le seul risque restant est celui du § 4.
206-
--- submodule status ---
 M donnees/paragraphes-validations.jsonl
  ```

- **bash** `{"command": "git status --short | sed -n '1,40p'; echo '--- target files ---'; ls -l reports/rapport-coordination-s.md reports/rapport-coordination-s.json", "description": "Final workspace status"}`

  ```
M docs/pilotage/references-non-regression.md
D  journal/2026-11-13/README.md
D  journal/2026-11-13/docs.md
MM journal/README.md
MM journal/THEMES.md
MM journal/sessions/MANIFEST.md
MM journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
MM journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
MM journal/sessions/session-3ffa6026-9a7d-4905-ac06-6b9708d65ba7/digest.md
MM journal/sessions/session-3ffa6026-9a7d-4905-ac06-6b9708d65ba7/rapport.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 m tools/structures
?? journal/2026-11-13/
?? reports/rapport-coordination-n2.json
?? reports/rapport-coordination-n2.md
?? reports/rapport-coordination-s.json
?? reports/rapport-coordination-s.md
?? reports/rapport-s-paragraphes.md
--- target files ---
-rw-------. 1 stephane stephane 18398 13 nov 21:58 reports/rapport-coordination-s.json
-rw-------. 1 stephane stephane 17390 13 nov 21:58 reports/rapport-coordination-s.md
  ```

- **bash** `{"command": "ls -l reports/rapport-coordination-n2.md reports/rapport-coordination-n2.json reports/rapport-etat-s.md | cat", "description": "Compare report permissions"}`

  ```
-rw-r--r--. 1 stephane stephane 11915 13 nov 21:52 reports/rapport-coordination-n2.json
-rw-r--r--. 1 stephane stephane 20149 13 nov 21:52 reports/rapport-coordination-n2.md
-rw-------. 1 stephane stephane 33894  6 nov 22:39 reports/rapport-etat-s.md
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-s.md", "new_string": "Le diff est **`+11 / −0`**, **non indexé** (`git diff`, pas `git diff --cached`) ; le hunk est\n`@@ -6,3 +6,14 @@`, donc les lignes ajoutées sont **9 à 19** :", "old_string": "Le diff es … [96 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-s.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-s.json", "new_string": "    \"diff\": \"+11 / -0\",\n    \"indexe\": false,\n    \"hunk\": \"@@ -6,3 +6,14 @@\",", "old_string": "    \"diff\": \"+11 / -0\",\n    \"hunk\": \"@@ -6,3 +6,14 @@\","}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-s.json has been updated successfully.
  ```

- **bash** `{"command": "python3 -m json.tool reports/rapport-coordination-s.json > /dev/null && echo JSON-OK; sed -n '38,44p' reports/rapport-coordination-s.md", "description": "Validate after precision edits"}`

  ```
JSON-OK
| octets | 2 390 | 6 047 |

Le diff est **`+11 / −0`**, **non indexé** (`git diff`, pas `git diff --cached`) ; le hunk est
`@@ -6,3 +6,14 @@`, donc les lignes ajoutées sont **9 à 19** :

```text
tools/structures/donnees/paragraphes-validations.jsonl:9   a004-c1  resolu
  ```

- **bash** `{"command": "git -C tools/structures status --porcelain; git -C tools/structures diff --numstat; git status --short -- reports/rapport-coordination-s.md reports/rapport-coordination-s.json", "description": "Confirm no submodule change"}`

  ```
M donnees/paragraphes-validations.jsonl
11	0	donnees/paragraphes-validations.jsonl
?? reports/rapport-coordination-s.json
?? reports/rapport-coordination-s.md
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-s.md", "new_string": "   rebase interrompu ou une perte de machine les détruit **sans récupération possible**. C'est la\n   seule copie de six paragraphes jugés **neuf jours plus tôt**, le 2026-11-04.", "old_ … [165 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-s.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-s.json", "new_string": "        \"detail\": \"Les 11 verdicts n'existent que dans le working tree local : ni commit, ni reflog, ni remote. Un git reset --hard, git checkout -- ., git clean -fd, un rebase inte … [430 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-s.json has been updated successfully.
  ```

- **bash** `{"command": "python3 -m json.tool reports/rapport-coordination-s.json > /dev/null && echo JSON-OK; grep -n \"neuf jours\" reports/rapport-coordination-s.md reports/rapport-coordination-s.json", "description": "Final validation of edits"}`

  ```
JSON-OK
reports/rapport-coordination-s.md:230:   seule copie de six paragraphes jugés **neuf jours plus tôt**, le 2026-11-04.
reports/rapport-coordination-s.json:463:        "detail": "Les 11 verdicts n'existent que dans le working tree local : ni commit, ni reflog, ni remote. Un git reset --hard, git checkout -- ., git clean -fd, un rebase interrompu ou une perte de machine les détruit sans récupération possible. C'est la seule copie de six paragraphes jugés neuf jours plus tôt, le 2026-11-04."
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json, subprocess, hashlib, os\nfrom collections import Counter\nbase='/home/stephane/Data13TB/stephane/GitHub/Qtrinet'; os.chdir(base)\nj=json.load(open('reports/rapport-coordination-s.json',encoding='utf-8'))\np='tools/structures/donnees/paragraphes-validations … [1149 caractères tronqués]`

  ```
AUDIT-FINAL-OK
fiche 303 lignes
json 11 verdicts
  ```

- **bash** `{"command": "git -C tools/structures status --porcelain; echo '---'; git status --short -- reports/rapport-coordination-s.md reports/rapport-coordination-s.json tools/structures", "description": "Final cleanliness check"}`

  ```
M donnees/paragraphes-validations.jsonl
---
 m tools/structures
?? reports/rapport-coordination-s.json
?? reports/rapport-coordination-s.md
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nj=json.load(open('reports/rapport-coordination-s.json'))\nprint(j['verdict'])\nprint('---')\nprint(j['risque_clone']['controle_negatif'])\nprint('---')\nprint([r['nom'] for r in j['risque_clone']['risques']])\nPY", "description": "Read key JSON summaries"}`

  ```
Les 11 verdicts a004–a009 sont 11 lignes non committées (9–19) de tools/structures/donnees/paragraphes-validations.jsonl : 6 resolu, 1 compatible, 4 exclu, soit 7 acceptés et 4 exclus. Le working tree voit 19 verdicts / 11 acceptés / 0 candidat sans verdict ; un clone à 523d8c1 voit 8 verdicts / 4 acceptés / 11 candidats sans verdict.
---
{'commande': 'tmp=$(mktemp -d); git clone -q tools/structures "$tmp/s"; cd "$tmp/s"; git rev-parse HEAD; git status --porcelain; wc -l < donnees/paragraphes-validations.jsonl', 'head': '523d8c1e8c6ca29ca415360a71bfab6c5b56102c', 'statut': 'propre (0 ligne)', 'lignes': 8, 'statuts': {'resolu': 4, 'exclu': 4}, 'acceptes': 4, 'phrases': ['a001', 'a002', 'a003'], 'sha256': 'adf23efe0e8ebc77b397295521b1d1fccb4394c4c97e11bb859d0c1d2ada8862'}
---
['perte sèche', 'clone trompeur', 're-jugement et écrasement', 'référents figés', 'pointeur orphelin', 'sous-module non portable', 'arbre parent sale']
  ```

### 🤖 Assistant

**J4.2 terminé.** Fiche et JSON créés :

- [`reports/rapport-coordination-s.md`](reports/rapport-coordination-s.md)
- [`reports/rapport-coordination-s.json`](reports/rapport-coordination-s.json)

**Les 11 verdicts** — `tools/structures/donnees/paragraphes-validations.jsonl`, lignes **9–19**, diff **+11/−0**, non indexé :

- **6 `resolu`**, **1 `compatible`**, **4 `exclu`** → **7 acceptés / 4 exclus**
- paragraphes **a004–a009**, 11 candidats, horodatages du **2026-11-04 15:03:43 → 15:10:08**
- working tree : **19 verdicts / 11 acceptés / 0 candidat sans verdict**
- clone à `523d8c1` : **8 verdicts / 4 acceptés / 11 candidats sans verdict** (mesuré par clone local)

**Commande S** (détaillée § 3) : commit du JSONL dans le sous-module, `git push origin master`, puis `git add tools/structures` + commit du pointeur parent et `git push origin s/v7`. Les deux commits sont nécessaires : sans le pointeur, un clone du parent reste à 8 verdicts ; sans le push du sous-module, le clone ne peut pas récupérer le nouveau SHA. La commande du sous-module a été rejouée dans un clone jetable : `1 file changed, 11 insertions(+)`, puis 19 verdicts au clone.

**Risque principal** : les 11 verdicts n'existent que dans le working tree — ni commit, ni reflog, ni remote. Un `reset --hard`, `clean -fd` ou une perte de machine les détruit. La fiche signale aussi que le commit fige **9 référents faux sur 16** (`a008` en porte 5), avec deux options : committer pour préserver puis corriger, ou corriger avant.

**`tools/structures/` intact** : `git status` du sous-module reste `M donnees/paragraphes-validations.jsonl` uniquement ; aucune écriture, aucun `__pycache__`. JSON validé et recoupé 11/11 avec le JSONL.

À noter : `python3 tools/revue_documentation.py` signale 2 compteurs (`en-cours.md` dit 713/806, le disque 715/808) ; je n'ai pas touché à `en-cours.md`, état partagé.

