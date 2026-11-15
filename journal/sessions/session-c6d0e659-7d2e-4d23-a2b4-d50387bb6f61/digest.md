# Session DSH — relecture

- identifiant : `session-c6d0e659-7d2e-4d23-a2b4-d50387bb6f61`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-15 12:40:17
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche X2 (J4 matin, la part du pilote) : le protocole d'annotation de l'**or de rôles** pour S — les champs (phrase, cadre, rôles : agent/prédicat/lieu/temps/destinataire/possession/complément), la **double annotation** (deux codeurs, le kappa), les 144 rôles existants du gold S (61 phrases / 144 rôles), le **gold v2 (46)** comme base de départ, et le contrôle négatif (l'or permuté doit s'effondrer). Écris `reports/rapport-or-roles-protocole.md` + JSON + un JSON de **schéma** (`reports/schema-or-roles.json`). **Ne modifie pas le gold S.**

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

- **bash** `{"command": "ls -la && echo \"---\" && ls reports/ | head -50 && echo \"---\" && ls data/ | head -50", "description": "List repository root, reports, data"}`

  ```
total 208
drwxr-xr-x. 1 stephane stephane   686  6 nov 09:52 .
drwxr-xr-x. 1 stephane stephane  2532  5 nov 10:41 ..
-rw-r--r--. 1 stephane stephane  9977  3 nov 09:19 AGENTS.md
drwxr-xr-x. 1 stephane stephane    40 25 sep 15:38 bench
drwxr-xr-x. 1 stephane stephane    56 30 sep 12:20 colab
drwxr-xr-x. 1 stephane stephane  2664  2 nov 18:33 data
drwxr-xr-x. 1 stephane stephane   138 15 nov 06:29 docs
drwxr-xr-x. 1 stephane stephane    92 28 oct 16:25 drave-core
drwxr-xr-x. 1 stephane stephane   220 15 nov 12:40 .git
-rw-r--r--. 1 stephane stephane   619 31 oct 17:33 .gitignore
-rw-r--r--. 1 stephane stephane   225  1 nov 10:50 .gitmodules
drwxr-xr-x. 1 stephane stephane   992 15 nov 12:34 journal
drwxr-xr-x. 1 stephane stephane   100  3 nov 09:12 models
drwxr-xr-x. 1 stephane stephane   114 25 sep 15:24 __pycache__
drwxr-xr-x. 1 stephane stephane    64  6 nov 09:52 .pytest_cache
-rw-r--r--. 1 stephane stephane  4992 25 sep 10:54 Qtrinet-bootstrap.md
-rw-r--r--. 1 stephane stephane 21293  6 nov 22:32 README.md
drwxr-xr-x. 1 stephane stephane 78338 15 nov 12:37 reports
-rw-r--r--. 1 stephane stephane 13100 28 oct 14:59 REPRISE.md
-rw-------. 1 stephane stephane  8566 30 sep 08:44 run
… [2997 caractères tronqués]
  ```

- **bash** `{"command": "cat docs/pilotage/en-cours.md | head -120", "description": "Read current state document"}`

  ```
# En ce moment

**Mis à jour : 2026-11-15, 12 h 40 HNE (semaine 2 : W1-W6, tag semaine-2-2026-11-20)**

> **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
> plan plus bas (**La carte**).

### Session `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — le hub de reprise du 04/11 *(en pause)*

- **Id** : `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — [`plan.md`](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/plan.md).
- **Rôle** : **Hub de reprise** — état, docs, intégration, passe.
- **Fait** : index réparé ; **N3 intégré** ; N2/S/L actifs ; suivi docs.
- **Prochaine action** : **suivi docs**, puis la **passe** après les runs.
- **État** : **en pause** depuis le 05/11 (dernier heartbeat) ; la clôture J14.1 est portée par `e181ce02`.
- **Bloquants** : aucun.
- **Journal** : [la session](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/).

## Sessions en cours

> Contrat : [`continuite.md`](../methode/continuite.md) · sessions terminées :
> [`journal/sessions/`](../../journal/sessions/). Chaque session expose son mandat dans son
> `plan.md` (`python3 tools/sessions.py --status`). **Une session écrit l'état à la fois** :
> le hook pr
… [9444 caractères tronqués]
  ```

- **bash** `{"command": "grep -rl \"144\" reports/*.md 2>/dev/null | head -30; echo \"---\"; ls reports | grep -i -E \"role|or-role|gold\" | head -60", "description": "Find role/gold reports"}`

  ```
reports/INDEX.md
reports/rapport-a80-indice-qualifie.md
reports/rapport-a80-melange-qualifie.md
reports/rapport-a80-porte-bus-socket.md
reports/rapport-architecture-memoire.md
reports/rapport-bilan-chantier.md
reports/rapport-classement-appris.md
reports/rapport-coherence-docs-2.md
reports/rapport-coherence-docs.md
reports/rapport-coherence-fiches-v7.md
reports/rapport-coherence-fiches-v8.md
reports/rapport-convention-gv.md
reports/rapport-coordination-a.md
reports/rapport-coordination-s-v2.md
reports/rapport-dev-test-v7.md
reports/rapport-dialogue-diabla.md
reports/rapport-drapeaux-ignores.md
reports/rapport-drvm-trace.md
reports/rapport-echecs-v2.md
reports/rapport-empreinte-memoire.md
reports/rapport-engram-etat.md
reports/rapport-etat-s.md
reports/rapport-fiabilite-produit.md
reports/rapport-gold-452.md
reports/rapport-gold-reel-50.md
reports/rapport-gpu-scores.md
reports/rapport-gpu-topk-selection.md
reports/rapport-gpu-topk-tout.md
reports/rapport-hc-permutation.md
reports/rapport-lecteur-multifichiers.md
---
pensee-anaphore-roles.json
pensee-gold-200.json
pensee-gold-342.json
pensee-gold-anglais.json
pensee-gold-cascade-200.json
pensee-gold-cascade.json
pensee-gold-complexes
… [1158 caractères tronqués]
  ```

- **bash** `{"command": "find . -path ./.git -prune -o -iname \"*gold*\" -print 2>/dev/null | head -80", "description": "Find gold files"}`

  ```
./reports/pensee-gold-linguistique.json
./reports/rapport-pensee-gold-linguistique.md
./reports/rapport-pensee-gold-200.md
./reports/pensee-gold-200.json
./reports/rapport-pensee-gold-200-subsets.md
./reports/pensee-gold-subsets.json
./reports/rapport-pensee-gold-complexes.md
./reports/pensee-gold-complexes.json
./reports/rapport-pensee-gold-complexes20.md
./reports/pensee-gold-complexes20.json
./reports/rapport-pensee-gold-complexes50.md
./reports/pensee-gold-complexes50.json
./reports/rapport-pensee-gold-complexes100.md
./reports/pensee-gold-complexes100.json
./reports/rapport-pensee-gold-discours.md
./reports/pensee-gold-discours.json
./reports/rapport-pensee-gold-342.md
./reports/pensee-gold-342.json
./reports/rapport-pensee-gold-gele.md
./reports/pensee-gold-gele.json
./reports/pensee-gold-neuronal.json
./reports/rapport-pensee-gold-neuronal.md
./reports/pensee-gold-syntagmes.json
./reports/rapport-pensee-gold-syntagmes.md
./reports/pensee-gold-cascade.json
./reports/rapport-pensee-gold-cascade.md
./reports/pensee-gold-pragmatique.json
./reports/pensee-gold-cascade-200.json
./reports/pensee-gold-reel-cascade.json
./reports/rapport-pensee-seuils-gold-reel.md
./reports/rapport-p
… [1215 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,200p' reports/rapport-s-analyseur-roles.md", "description": "Read S role analyzer report"}`

  ```
# S — Le contexte tranche les homographes : 54/55 types, 131/131 rôles, 55 structures au corpus

> **Ligne de roadmap** : S · **Date** : 2026-11-02 · **Verdict** : sur un gold de **55 phrases**
> (7 `dev`, 16 `test`, 32 `holdout` en quatre vagues), la structure de base retrouve la **séquence
> de types 54/55** (98,2 %), les **rôles 131/131** (100 %), les **compléments 47/47**, et couvre
> **1 466/1 475 octets** (99,4 % ; holdout **762/771**, 98,8 %). La **règle de contexte** corrige
> les homographes `h046` (« ferme ») et `h047` (« fait ») : un mot du lexique de verbes est un
> **nom** si le suivant est un auxiliaire ou un autre verbe. La **limite nommée** se déplace :
> `h050` (« fait » suivi d'un verbe **hors lexique**) et `h053` (« lit » après un adjectif, en
> fin de phrase). Le corpus de référence sort : **55 lignes**, SHA-256
> `76accf9dbd60a9fcc9fe58a56eecbdbb6aec0ffd5e8dbf0c69443e4a49dd1ac6`.

## Le dispositif

- **Gold** : [`tools/structures/donnees/gold-analyseur.json`](../tools/structures/donnees/gold-analyseur.json),
  **55 phrases** : **7 `dev`**, **16 `test`**, **32 `holdout`** en quatre vagues : `h024–h031`
  (première règle), `h032–h039` (copule), `h040–h047` (front
… [7001 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,160p' reports/rapport-restitution-v3.md 2>/dev/null; echo \"=== JSON ===\"; python3 -c \"import json;d=json.load(open('tools/tests/linguistique/gold_restitution_v2.json'));print(type(d));print(json.dumps(d,ensure_ascii=False)[:3000])\"", "description": "Read restitution v3 and … [15 caractères tronqués]`

  ```
# B13 — la restitution v3 : les rôles des GP se séparent, la fidélité du cadre ne suit pas

> **Ligne de roadmap** : **B13** (produit) · **Tâche** : W5 (J3 après-midi) · **Date** :
> 2026-11-15 · **Verdict** : **positif sur la séparation, négatif sur le produit** — les
> cinq rôles de GP se séparent sur le gold S (**18/18**, **144/144**, permutation **0/18**),
> mais le gold v2 ne gagne qu'un cadre : **20/46** contre 19/46, F1 **0,5406** contre
> 0,5270, `lieu` F1 **0,60** contre 0,40. La fidélité du cadre ne suit pas : le goulot est
> la segmentation et le choix du cadre, pas la préposition.
>
> **La question.** La v2 lisait la préposition seule (`à` → destinataire, `de` → thème,
> `avec` → moyen) ; le `lieu` restait son rôle le plus faible (F1 0,4000). La v3 peut-elle
> distinguer **lieu / temps / destinataire / possession / complément** avec le contexte, et
> la précision/rappel par rôle le montrent-ils sur les deux ors existants — le gold v2
> (46) et le gold S (61 phrases, 144 rôles) — sans que la mesure soit un rôle constant ?
>
> **La réponse.** Oui pour la **règle** : `_role_gp` sépare les cinq catégories avec le
> contexte (ce qui suit la préposition, ce qui la précède), *
… [9382 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"or de rôles\\|or-de-roles\\|or de roles\\|X2\\|J4\" docs reports journal work 2>/dev/null | head -60", "description": "Search for task references"}`

  ```
3bvBWgjiDImkfRLBTEXaoyCg9Hh78MoEzgsevfk3qF89VZre9R+1UFG77VTh/dXxgf+4jcizGexaJCPyAppGX44L1hm9O52m6dfvHR3LEkzgR+1e3lDsM/9EZ/NxwzqDYPoSrXOjRH+AbxkOZDkXD1+3wcxR2pNyDf36YZQtHhTf2O8njXc8poP9wX/Mro/q3jt725dPF2n4Tt7S0x54Vabh8hAzICwNth/w5l4eSYszHCxg4qItmir98aPPo0f/+fnGir0eN0ft1qipuwn5fvlz+DdfhwXpaYU2Ro6uMc+GvdYdGihm+mrhqWLbjqulrXmD0LE5Zhld3n/0fWTwo8tUOhFOch/KiVEFUWBjBMhUMf+z66WgZXp78EBPOay2dEJUU5JIsArcdOU0disiA5DjPF7ZZsFLL4bOASlE0iUmRaHK17cnk1B6CUwJ9I5wTR9mujyXpUr+a368uly1Av9WHniLxnLnWri/mXndXIyqrGJit5GddmNP8Oa2z9Lx9g53extedRCiS4itV/HgRa4UqWt0vFHl+UR8H8mVGse2llLFPz+1SlwIQFT2LTi1T7yFwW8EK7SSSeLwq9fJrXgV9gYD4U4EnSYqqQAE4PbtWmsk4y+bK7hoyulG9xnLIzbz/ueR2i0vFi1TEW+EcuIiiNrLA29Yh7LeHJswnl7wkgDaVQ5FWH8k4axsnov2mZ/qTiDmwihsIlntN/8yFnTmERH9sdx2tbp49DkD3wlanP16g0qFGo5tC96oCyVCUZQ7jiHY280Xnd4touHx6mES51eAGnSI0JHVeDwbKzRDGaEQT6P3aLj5So32u1heV74Xik8snB0rpCxApGX2xBWV8OpVO10tZQ2ST9UdjJmy22u2ku8I5h8HDnYasa6CjuqMFKYclUCP/jrxDrQdtyurxLg46nL5TTqo4reG1IKlmiCUKYyEXygOVBObYUijUxPri6LgWQ2KRXRwn0gswlLJrtQqV8u3BKBHB64ZlOthuuXy6Cb1tjs8Y56TsoYbE8w/FkbaTuWlDtKttd3zw85YBIbiuDVTBQ2X8iXGMpm/dKRzBKDYYDkBb+X0cVNAIgDMWuhOFjTip/tNKl13FJOHN0YPR6pAE8qDh1kO3310u7QM7XXEss9cMrIVUuab78ooWMogAA23k0ngA/bkmdJppFVvhgjg5axAaatC5xbyxGJq
… [48731 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\np='tools/structures/donnees/gold-analyseur.json'\nd=json.load(open(p))\nprint(type(d))\nif isinstance(d,dict):\n    print(d.keys())\n    for k,v in d.items():\n        print(k, type(v), (len(v) if hasattr(v,'__len__') else ''))\nEOF", "description": "Insp … [27 caractères tronqués]`

  ```
<class 'dict'>
dict_keys(['version', 'note', 'segments', 'phrases'])
version <class 'int'> 
note <class 'str'> 1107
segments <class 'list'> 3
phrases <class 'list'> 61
  ```

- **bash** `{"command": "sed -n '1,140p' docs/pilotage/semaine-2.md", "description": "Read week 2 plan"}`

  ```
# La semaine 2 — cinq jours, deux vagues, quatre chantiers et une décision

> **Ce que ce document est.** Le plan du **16 au 22 novembre 2026** : ce qui se fait, dans quel
> ordre, avec quelles dépendances, quels contrôles et quels livrables. Il **succède** à
> [`semaine-autonome.md`](semaine-autonome.md), qui reste l'**archive** de la semaine 1 et n'est
> **pas modifié**. L'état courant est dans [`en-cours.md`](en-cours.md) ; les chiffres sont dans
> les fiches citées, jamais recopiés ici.
>
> **Sources.** Le [bilan de la semaine](../../reports/rapport-bilan-semaine.md) et les fiches des
> tâches C/B/D/E : [C1](../../reports/rapport-coordination-n2-v2.md), [C2](../../reports/rapport-coordination-s-v2.md),
> [C3](../../reports/rapport-gold-reel-50.md), [B1](../../reports/rapport-protocole-date.md),
> [B2](../../reports/rapport-atomes-prediction.md), [B3](../../reports/rapport-cic-v2.md),
> [D1](../../reports/rapport-exemples-tagger.md), [D2](../../reports/rapport-restitution-v2.md),
> [D3](../../reports/rapport-faq.md), [E1](../../reports/rapport-faq-sommaire.md),
> [E2](../../reports/rapport-tagger-erreurs.md). Le plan ne promet aucun chiffre : il nomme la
> mesure, son **contrôle
… [13358 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '160,380p' reports/rapport-restitution-v3.md; echo \"=== JSON keys ===\"; python3 - <<'EOF'\nimport json\nd=json.load(open('reports/pensee-restitution-v3.json'))\nprint(d.keys())\nprint(json.dumps(d,ensure_ascii=False,indent=1)[:4000])\nEOF", "description": "Read rest of v3 repor … [12 caractères tronqués]`

  ```
### 3.3 Les cas de séparation (24)

[`roles_gp.CAS_SEPARATION`](../tools/roles_gp.py) : **24 cas** écrits pour couvrir les
distinctions que l'or ne couvre pas (surtout `complément`, `par` passif, l'anglais). Ce sont
des **tests de règle**, pas un or : ils montrent que la fonction ne renvoie pas un rôle
constant, ils ne remplacent pas une annotation.

## 4. Les chiffres

### 4.1 Gold v2 : le cadre principal

| mesure | v2 | v3 | Δ |
|---|---:|---:|---:|
| textes du banc / annotés / refus | 50 / 46 / 4 | 50 / 46 / 4 | — |
| cadres exacts | **19/46 = 0,4130** | **20/46 = 0,4348** | **+1** |
| dont non vides | **16/46 = 0,3478** | **17/46 = 0,3696** | **+1** |
| dont vides | 3 | 3 | 0 |
| cadres partiels | 42/46 = 0,9130 | 43/46 = 0,9348 | +1 |
| cadres exacts stricts (1re variante) | 16/46 = 0,3478 | 17/46 = 0,3696 | +1 |
| rôles exacts (cellules) | 91/138 = 0,6594 | **93/138 = 0,6739** | +2 |
| rôles justes / attendus | 39/77 | **40/77** | +1 |
| rôles prédits | 71 | 71 | 0 |
| précision | 0,5493 | **0,5634** | +0,0141 |
| rappel | 0,5065 | **0,5195** | +0,0130 |
| **F1** | **0,5270** | **0,5406** | **+0,0136** |
| faux positifs / faux négatifs | 32 / 38 | **31 / 37** | −1 / −1 |

Le
… [15105 caractères tronqués]
  ```

- **bash** `{"command": "find reports -maxdepth 1 -name \"schema*.json\" -o -name \"*protocole*.json\" | sort; echo \"---\"; sed -n '1,240p' tools/restitution_v3.py", "description": "List schema/protocol JSONs and read restitution v3"}`

  ```
reports/protocole-date.json
reports/schema-v2-doc.json
---
"""restitution_v3.py — la restitution v3 : les rôles des groupes prépositionnels.

La v2 lisait la préposition seule. La v3 ajoute le **contexte** et sépare les cinq rôles
nommés par la tâche : `lieu`, `temps`, `destinataire`, `possession`, `complement`
(plus `theme`, `moyen`, `but`, `agent`, `maniere`, `concession`, `source`).

Deux mesures, deux ors :

- le **gold v2** (46 textes) n'annote que `agent / prédicat / lieu` : on y mesure la
  précision et le rappel de ces trois rôles, avant (v2) et après (v3) ;
- le **gold S** (61 phrases, 144 rôles) annote les cinq catégories : on y mesure la
  précision et le rappel **par rôle**, avec les effectifs. Les cinq rôles n'y ont que
  18 occurrences — un `complement` zéro — et c'est une limite nommée, pas un résultat
  triomphal.

Le **contrôle négatif** permute les rôles prédits (les cinq, puis tous) : la mesure doit
s'effondrer. Le contrôle « rôle constant » et le contrôle « règles coupées » donnent les
planchers. Le codec `relire_roles(rendre_roles(a)) == principal` est mesuré à part : il
ne compte **pas** comme fidélité.

    python3 tools/drave.py restituer "Le voyage à Paris 
… [8426 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, collections\np='tools/structures/donnees/gold-analyseur.json'\nd=json.load(open(p))\nprint('version',d['version'])\nprint('note',d['note'])\nprint('phrases',len(d['phrases']))\nprint('segments',d['segments'][:3])\nprint('--- phrase keys ---')\nprint(d['ph … [357 caractères tronqués]`

  ```
version 1
note Gold de l'analyseur. split=dev : les 7 phrases du banc. split=test : 16 phrases écrites AVANT les règles. split=holdout : 32 phrases en quatre vagues — h024-h031 (première règle, h024 a révélé « est mon voisin », corrigé par la copule), h032-h039 (après la copule), h040-h047 (après la frontière GN-devant-verbe) et h048-h055 (après la règle de contexte des homographes, 02/11 20 h). h033, h046 et h047, qui avaient révélé les défauts, sont corrigés ; les vagues 2 et 3 ne sont donc plus aveugles à ces règles, et la vague 4 est écrite après la règle de contexte, mesurée une fois. Deux échecs de la vague 4 sont nommés : h050 (« fait » suivi d'un verbe hors lexique) et h053 (« lit » après un adjectif, en fin de phrase). Aucun attendu n'a été modifié après mesure. Cinquième vague h056-h060, écrite APRÈS les règles v6 (h050, h053, « si fort que ») et mesurée une fois : elle teste la conséquence, l'hypothèse conditionnelle, le nom après adjectif et le verbe « fait » après un nom. Sixième vague h061 : le nom après un adjectif hors lexique (« fait divers »), ajouté après la règle v7 et mesuré une fois.
phrases 61
segments ['texte', 'type', 'role']
--- phrase keys ---
dict_keys([
… [398 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, collections\nd=json.load(open('tools/structures/donnees/gold-analyseur.json'))\nc=collections.Counter(); ct=collections.Counter(); per=[]\nfor ph in d['phrases']:\n    roles=ph['attendus']\n    per.append(len(roles))\n    for span,typ,role in roles:\n     … [768 caractères tronqués]`

  ```
phrases 61 roles 144
role counts:
  predicat: 58
  agent: 34
  temps: 9
  qualite: 7
  patient: 5
  destinataire: 5
  contenu: 5
  theme: 4
  cause: 4
  lieu: 3
  but: 3
  hypothese: 2
  possession: 1
  instrument: 1
  concession: 1
  maniere: 1
  consequence: 1
type x role:
  ('GN', 'agent') 31
  ('GN', 'patient') 5
  ('GP', 'agent') 3
  ('GP', 'but') 2
  ('GP', 'destinataire') 5
  ('GP', 'instrument') 1
  ('GP', 'lieu') 3
  ('GP', 'possession') 1
  ('GP', 'temps') 4
  ('GP', 'theme') 4
  ('GV', 'predicat') 58
  ('REL', 'qualite') 7
  ('SUB', 'but') 1
  ('SUB', 'cause') 4
  ('SUB', 'concession') 1
  ('SUB', 'consequence') 1
  ('SUB', 'contenu') 5
  ('SUB', 'hypothese') 2
  ('SUB', 'maniere') 1
  ('SUB', 'temps') 5
roles per sentence: Counter({2: 32, 3: 21, 1: 5, 4: 3})
splits: Counter({'holdout': 38, 'test': 16, 'dev': 7})
empty attendus: []
predicat counts: Counter({1: 56, 0: 4, 2: 1})
phrases with >=2 predicates: [('h031', 2)]
  ```

- **bash** `{"command": "grep -rn \"kappa\\|Kappa\\|Cohen\" tools reports docs 2>/dev/null | head -40; echo \"--- protocole-date ---\"; sed -n '1,120p' reports/protocole-date.json; echo \"--- schema-v2-doc ---\"; sed -n '1,100p' reports/schema-v2-doc.json", "description": "Search kappa and inspect protocol/sche … [10 caractères tronqués]`

  ```
tools/cerveau/predictif.py:203:    def __init__(self, cible: str = "cible", ordre: int = 1, kappa: float = 10.0,
tools/cerveau/predictif.py:213:        self.kappa = float(kappa)
tools/cerveau/predictif.py:248:        jeu. Chaque niveau est interpolé avec `kappa` pseudo-comptes du niveau
tools/cerveau/predictif.py:263:        dist = {x: (p0[x] + self.kappa / v) / (total0 + self.kappa) for x in valeurs}
tools/cerveau/predictif.py:267:            dist = {x: (c[x] + self.kappa * dist[x]) / (total + self.kappa) for x in valeurs}
tools/cerveau/predictif.py:272:            dist = {x: (c[x] + self.kappa * dist[x]) / (total + self.kappa) for x in valeurs}
tools/cerveau/predictif.py:355:                p_base = (p0[y] + self.kappa / v) / (total0 + self.kappa)
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_vendor/distro/distro.py:2:# Copyright 2015-2021 Nir Cohen
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_vendor/pygments/filters/__init__.py:123:        '\\kappa'                : '\U000003ba',
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_vendor/pygments/filters/__init__.py:436:        '\\<kappa>'                : '\U000003ba',
tools/docwatch/.venv/lib/python3.13/s
… [13589 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('tools/chantier/plan.json'))\nprint(type(d), list(d.keys())[:20] if isinstance(d,dict) else len(d))\nEOF\nsed -n '640,760p' tools/chantier/plan.json", "description": "Inspect task plan JSON around X2"}`

  ```
<class 'dict'> ['nom', 'principe', 'taches']
   "titre": "J3 — Panini : le manifeste et le rejeu",
   "mandat": "Tâche W4 (J3 matin, la part du pilote) : le manifeste à envoyer à Panini — les **26 signatures manquantes** (la liste des œuvres du §334 sans signature V14), la commande exacte qu'ils doivent lancer, le format attendu ; et le **rejeu des 60 paires** du protocole (`rapport-protocole-date.md`) sur ce qui est disponible, avec le contrôle négatif. Fiche `reports/rapport-panini-manifeste.md` + JSON. **Ne modifie rien chez Panini.**",
   "budget_min": 90,
   "acceptation": [
    {
     "commande": "test -f reports/rapport-panini-manifeste.md && echo FICHE-OK",
     "attendu": "FICHE-OK"
    }
   ]
  },
  {
   "id": "W5",
   "jour": 17,
   "titre": "J3 — la restitution v3 : les rôles des GP",
   "mandat": "Tâche W5 (J3 après-midi) : la restitution v3 — `_role_gp` distingue **lieu / temps / destinataire / possession / complément** (des prépositions : `à` + lieu/temps/destinataire, `de` + possession, `avec` + moyen...) ; mesure la **précision et le rappel par rôle** sur le gold v2 (46) et le gold S (61/144 existants), avec le **contrôle négatif** (permuter les rôles doit tuer la 
… [3591 caractères tronqués]
  ```

- **bash** `{"command": "git status --short | head -40; echo \"---\"; git submodule status 2>/dev/null; echo \"---\"; git log -3 --oneline", "description": "Check git status and submodules"}`

  ```
M docs/pilotage/en-cours.md
 M docs/produit/README.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/plan.json
?? reports/rapport-page-s-mesure.json
?? reports/rapport-page-s-mesure.md
?? reports/rapport-s-paragraphes.md
?? tools/tests/linguistique/gold_reel_50.py
---
 d256888934b017ac024de2a8eed22ecf81e6c799 tools/docwatch (v0.4.1-3-gd256888)
 389b99f8383eb47c0cc008f5d3211c9d65d895fc tools/structures (heads/master)
---
2b5bd1cd JOURNAL — RÉGÉNÉRÉ APRÈS LA CLÔTURE DE LA SEMAINE 2 (W1-W6) ; LE TAG semaine-2-2026-11-20 REPOSÉ SUR LE COMMIT W5
049343d3 SEMAINE 2 — W6 : LA CLÔTURE (5 VAGUES, 3 POSITIVES, 1 BLOQUÉE, 1 MIXTE) ; 85 PORTES LUES (81/4), CIBLAGE 9/9 ; TAG ANNOTÉ semaine-2-2026-11-20 SUR 73edb3dd
9960b37f SEMAINE 2 — W5 : LA RESTITUTION v3 SÉPARE LES CINQ RÔLES (GOLD S 144/144, 18/18, PERMUTATION 0/18) ; LE GOLD v2 NE GAGNE QU'UN CADRE (20/46, F1 0,5406, LIEU 0,60) ; --roles-v3 OPT-IN
  ```

- **bash** `{"command": "python3 - <<'EOF'\ntry:\n import jsonschema; print('jsonschema', jsonschema.__version__)\nexcept Exception as e: print('no jsonschema', e)\ntry:\n import scipy; print('scipy', scipy.__version__)\nexcept Exception as e: print('no scipy', e)\ntry:\n import numpy; print('numpy', numpy.__ve … [297 caractères tronqués]`

  ```
jsonschema 4.26.0
scipy 1.18.1
numpy 2.5.3
--- schema files ---
tools/schemas/drave-annotation-v1.json
tools/schemas/drave-annotation-v2.json
--- validator ---
#!/usr/bin/env python3
"""verifier_schema_produit.py — valide une annotation `drave.annotation` contre le schéma de sa version.

Deux schémas sont publiés (Draft 2020-12) :

- `tools/schemas/drave-annotation-v1.json` — le contrat d'origine (version 1) ;
- `tools/schemas/drave-annotation-v2.json` — le contrat courant (version 2) : il ajoute
  `meta.partition` et `meta.alternative`, les deux champs qui documentent les syntagmes qui se
  chevauchent.

Le vérificateur lit `version` dans l'annotation et choisit le schéma correspondant : une
annotation v1 reste donc **lue** et validée par le schéma v1. Il compile les schémas une fois,
puis valide les annotations de cas choisis : français, anglais, refus (texte vide), entrée non
textuelle, texte très long, plus une annotation v1 de rétro-compatibilité. Il ne dépend que de
`fastjsonschema` (sinon il se rabat sur une validation minimale des champs obligatoires et de la
version). Un **contrôle négatif** vérifie que le schéma v2 refuse bien une annotation v1.

Usage :
    python3 tools
… [2509 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '240,520p' tools/restitution_v3.py; echo \"=== mesurer ===\"; sed -n '1,200p' tools/mesurer_restitution_v3.py", "description": "Read rest of restitution v3 and driver"}`

  ```
"mapping": cycle,
            "synthese": permute["synthese"],
        },
    }


# --------------------------------------------------------------------------- gold S


def apparier_v2(segments: list[dict], gold_spans: list[dict]) -> dict[int, int]:
    """L'appariement de la v2 : pour chaque or, le premier span à recouvrement maximal.

    Il est conservé pour **séparer** le gain de rôles du gain d'appariement : le chiffre
    v2 139/144 a été produit avec cet appariement, pas avec le nouveau.
    """
    appariement: dict[int, int] = {}
    pris_p: set[int] = set()
    for gi, g in enumerate(gold_spans):
        meilleur = None
        for pi, p in enumerate(segments):
            if pi in pris_p or p["type"] != g["type"]:
                continue
            inter = min(g["fin"], p["fin"]) - max(g["debut"], p["debut"])
            if inter > 0 and (meilleur is None or inter > meilleur[0]):
                meilleur = (inter, pi)
        if meilleur is not None:
            appariement[gi] = meilleur[1]
            pris_p.add(meilleur[1])
    return appariement


def apparier(segments: list[dict], gold_spans: list[dict]) -> dict[int, int]:
    """Apparie chaque span d'or à un span
… [20699 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, collections\ng=json.load(open('tools/tests/linguistique/gold_restitution_v2.json'))\nprint(g.keys(), g.get('schema'), g.get('version'), g.get('date'))\nt=g['textes']; print('textes',len(t))\nprint('langues',collections.Counter(x.get('langue') for x in t)) … [775 caractères tronqués]`

  ```
dict_keys(['schema', 'version', 'date', 'ligne', 'tache', 'note', 'textes']) drave.restitution.v2.gold 1 2026-11-15
textes 46
langues Counter({'fr': 35, 'en': 5, 'und': 5, 'it': 1})
variantes 65
first cells 138 nonempty 78 {'agent': 32, 'predicat': 39, 'lieu': 7} texts empty 0
all cells 195 nonempty 115 {'agent': 48, 'predicat': 58, 'lieu': 9} texts empty 0
ids ['f01', 'f02', 'f03', 'f04', 'f05', 'f06', 'f07', 'f08', 'f09', 'f10', 'f11', 'f12', 'f13', 'f18', 'f19', 'f20', 'f21', 'f22', 'f23', 'f24', 'f25', 'f26', 'f27', 'f28', 'f29', 'f30', 'f31', 'f32', 'f33', 'f34', 'f35', 'f36', 'f37', 'f38', 'f39', 'f40', 'f41', 'f42', 'f43', 'f44', 'f45', 'f46', 'f47', 'f48', 'f49', 'f50']
variant keys Counter({'agent': 65, 'predicat': 65, 'lieu': 65})
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\ng=json.load(open('tools/tests/linguistique/gold_restitution_v2.json'))\nfor x in g['textes']:\n    v=x['variantes'][0]\n    if v.get('lieu','').strip():\n        print(x['id'], x['langue'], repr(x['texte']), '=>', repr(v['lieu']))\nprint('--- empty agent/ … [319 caractères tronqués]`

  ```
f07 en 'The cat sleeps on the roof.' => 'on the roof'
f08 en 'Where is the nearest train station, please?' => 'Where'
f24 fr 'Il était une fois une petite fille qui vivait au bord de la forêt...' => 'au bord de la forêt'
f26 fr 'Où sont les toilettes ? Je cherche depuis dix minutes.' => 'Où'
f35 en 'The quick brown fox jumps over the lazy dog.' => 'over the lazy dog'
f46 fr "Il n'y a ni pain ni lait dans le réfrigérateur." => 'dans le réfrigérateur'
f49 fr 'La réunion est reportée à demain, 10 h 30, salle B12.' => 'salle B12'
--- empty agent/predicat ---
f04 agent= '' pred= 'Ferme' lieu= ''
f05 agent= '' pred= 'Ne touche pas' lieu= ''
f09 agent= '' pred= "Don't forget" lieu= ''
f11 agent= '' pred= 'Rendez-vous' lieu= ''
f12 agent= '' pred= 'Visitez' lieu= ''
f18 agent= '' pred= '' lieu= ''
f25 agent= '' pred= '' lieu= ''
f33 agent= '' pred= 'apporte' lieu= ''
f37 agent= '' pred= '' lieu= ''
f39 agent= '' pred= '' lieu= ''
f40 agent= '' pred= '' lieu= ''
f42 agent= '' pred= '' lieu= ''
f45 agent= '' pred= "N'oublie" lieu= ''
f48 agent= '' pred= '' lieu= ''
  ```

- **bash** `{"command": "grep -n \"def _agreger_resultats\\|def _comparer\\|attendus\\|justes\\|variante\" tools/restitution_v2.py | head -60; echo \"---\"; sed -n '250,520p' tools/restitution_v2.py", "description": "Inspect restitution v2 comparison logic"}`

  ```
10:que le **cadre principal** et quelques variantes d'ambiguïté ; il ne prétend pas annoter
266:def comparer_cadre(predit: dict, variantes: list[dict]) -> dict:
267:    """Compare un cadre prédit à une liste de cadres attendus (variantes d'ambiguïté).
270:    celle de l'or. Le meilleur variant est retenu : les variantes ne sont pas un droit à
273:    if not variantes:
274:        variantes = [{"agent": "", "predicat": "", "lieu": ""}]
276:    for rang, variante in enumerate(variantes):
280:            v = variante.get(role, "") or ""
290:        justes = sum(1 for x in par_role.values() if x["juste"])
293:        score = (exacts, justes, -fp, -fn, -rang)
295:            "variante": rang,
297:            "justes": justes,
298:            "attendus": sum(1 for v in variante.values() if v),
381:    total = justes = 0
388:            justes += 1
389:    return {"justes": justes, "total": total,
390:            "taux": round(justes / total, 4) if total else 0.0}
413:    variantes = (gold or {}).get("variantes") or []
414:    comparaison = comparer_cadre(principal, variantes) if variantes else None
415:    stricte = comparer_cadre(principal, variantes[:1]) if variantes else None
426:    
… [13867 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,80p' reports/INDEX.md; echo \"---\"; grep -n \"or-roles\\|restitution-v3\\|panini-manifeste\" reports/INDEX.md | head; echo \"--- revue docs ---\"; sed -n '1,120p' tools/revue_documentation.py", "description": "Inspect reports index and doc review"}`

  ```
# Index des fiches de reports/

> **Généré** par `tools/index_reports.py` — **751 fiches**. Les fichiers
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
| [fiche-nuit-17-10.md](fiche-nuit-17-10.md) | La nuit du 17 au 18 
… [13183 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' docs/methode/resultats.md; echo \"=== rangement ===\"; sed -n '1,100p' docs/methode/rangement.md", "description": "Read result and filing method docs"}`

  ```
# Ce qu'un résultat doit porter

> Document de tâche, chargé depuis [`AGENTS.md`](../../AGENTS.md). À lire **avant d'écrire une fiche**, un JSON de
> résultats, ou un message de commit.

## Les cinq pièces d'un résultat

1. **Le chiffre** — la valeur, avec son [unité](../theorie/glossaire/entrees/unite.md) et son arrondi utile (jamais plus de chiffres que l'instrument n'en
   [porte](../theorie/glossaire/entrees/porte.md)) ;
2. **La mesure qui le produit** — le calcul exact, la métrique ([chrF](../theorie/glossaire/entrees/chrf.md), précision, rappel, [AUC](../theorie/glossaire/entrees/auc.md)…), et ce qu'elle ne
   mesure pas ;
3. **Le dispositif** — quel [corpus](../theorie/glossaire/entrees/corpus.md) (et sa provenance), quel modèle (taille, [quantification](../theorie/glossaire/entrees/quantification.md), date de coupure),
   quelles **couches de neurones** sondées, quel découpage, **quelle unité de mesure** (unité de sens ou unité
   grammaticale ; si c'est un [jeton](../theorie/glossaire/entrees/jeton.md), le dire comme **technique**), quels réglages (prompt, gabarit, longueur de
   sortie, graine) ;
4. **Le [contrôle négatif](../theorie/glossaire/entrees/controle-negatif.md)
… [7723 caractères tronqués]
  ```

- **bash** `{"command": "date -I; git log -1 --format='%H %ad' --date=iso; python3 - <<'EOF'\nimport datetime; print(datetime.date.today().isoformat())\nEOF", "description": "Check current date"}`

  ```
2026-11-15
2b5bd1cdc35b3585fee0e1c4a45a035b96d1d553 2026-11-15 12:35:40 -0500
2026-11-15
  ```

- **bash** `{"command": "grep -n \"INDEX\\|orphelin\\|rapports()\\|index_reports\" tools/revue_documentation.py | head -40; sed -n '300,520p' tools/revue_documentation.py", "description": "Inspect doc review navigation checks"}`

  ```
14:  7. navigation : aucun document vivant n'est orphelin, et aucun chemin en code inline
75:def rapports():
80:    """Les fichiers vivants dont les liens comptent pour la navigation (orphelins)."""
81:    return (docs_vivants() + rapports()
109:    return len(rapports())
244:    # 7b. orphelins : tout document vivant doit avoir au moins un lien entrant
            continue
        for m in re.finditer(r"jeton[s]?\s+(sémantique|de sens|neutre)", f.read_text(), re.I):
            alertes.append(
                f"vocabulaire : {f.relative_to(RACINE)} → « {m.group(0)} » "
                "(la RSN est en unités de sens ; le jeton est technique)"
            )

    # 5bis. cohérence de la synthèse : huit chapitres, chapitres 7-8, B10–B12
    idx = RACINE / "docs/theorie/synthese/index.md"
    if idx.exists():
        it = idx.read_text()
        if "Huit chapitres" not in it:
            alertes.append("cohérence : l'index ne dit pas « Huit chapitres »")
        for cible in (
            "07-modeles-alternatifs-entree-sortie.md",
            "08-les-operations.md",
            "B10", "B11", "B12",
        ):
            if cible not in it:
                alertes.append(f"cohérence : 
… [3216 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '220,300p' tools/revue_documentation.py", "description": "Inspect orphan check"}`

  ```
and lab.endswith((".md", ".json", ".sh"))):
                continue
            p = (f.parent / cible).resolve()
            lp = (RACINE / lab).resolve()
            if p.exists() and lp != p:
                alertes.append(
                    f"libellé : {f.relative_to(RACINE)} annonce « {lab} » mais pointe {cible}"
                )

    # 7a. chemins morts en code inline (hors gabarits)
    for f in sources_propres():
        try:
            brut = f.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        texte = re.sub(r"\[[^\]]+\]\([^)]+\)", "", brut)
        for m in CHEMIN.finditer(texte):
            p = m.group(1).rstrip(".,;:)")
            if any(g in p for g in GABARIT):
                continue
            if not (RACINE / p).exists():
                ligne = texte[: m.start()].count("\n") + 1
                alertes.append(f"chemin mort : {f.relative_to(RACINE)}:{ligne} → {p}")

    # 7b. orphelins : tout document vivant doit avoir au moins un lien entrant
    entrants: set[pathlib.Path] = set()
    for f in sources_nav():
        try:
            texte = f.read_text(encoding="utf-8", errors="ignore")
        except OSErro
… [2188 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && time python3 - <<'EOF'\nimport json, sys\nsys.path.insert(0,'.')\nimport tools.restitution_v3 as v3\nm=v3.mesurer_gold_analyseur_v3()\nprint('base',m['base']['justes'],m['base']['total'],m['base']['cinq_roles']['justes'],m['base']['c … [705 caractères tronqués]`

  ```
base 144 144 18 18
perm5 126 144 0
permtous 58 144 0
constant 3 144 3
baseline 104 144
par role base {'agent': 34, 'but': 3, 'cause': 4, 'concession': 1, 'consequence': 1, 'contenu': 5, 'destinataire': 5, 'hypothese': 2, 'lieu': 3, 'maniere': 1, 'moyen': 1, 'patient': 5, 'possession': 1, 'predicat': 58, 'qualite': 7, 'temps': 9, 'theme': 4}
[stderr]

real	0m0,289s
user	0m0,257s
sys	0m0,032s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && time python3 - <<'EOF'\nimport json, sys\nsys.path.insert(0,'.')\nimport tools.restitution as restitution\nimport tools.restitution_v3 as v3\nbanc=json.load(open('reports/pensee-fiabilite-produit.json'))\ngold=json.load(open('tools/t … [644 caractères tronqués]`

  ```
base cadres 20 17 roles 40 77 0.5634 0.5195 0.5406
vide None None None None
constant_par_type None None None None
melange None None None None
permutation_gp None None None None
perm gp mapping {'lieu': 'temps', 'temps': 'destinataire', 'destinataire': 'possession', 'possession': 'complement', 'complement': 'lieu'}
[stderr]

real	0m0,546s
user	0m0,514s
sys	0m0,032s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, sys, pprint\nsys.path.insert(0,'.')\nimport tools.restitution as restitution\nimport tools.restitution_v3 as v3\nbanc=json.load(open('reports/pensee-fiabilite-produit.json'))\ngold=json.load(open('tool … [593 caractères tronqués]`

  ```
dict_keys(['base', 'vide', 'constant_par_type', 'melange', 'permutation_gp'])
vide <class 'dict'> ['exacts', 'total', 'taux', 'cadres_exacts', 'cadres_exacts_taux', 'cadres_partiels', 'justes', 'attendus', 'predits', 'precision', 'rappel', 'f1', 'faux_positifs', 'faux_negatifs', 'vrais_negatifs', 'par_role']
  cadre None roles None None None
constant_par_type <class 'dict'> ['exacts', 'total', 'taux', 'cadres_exacts', 'cadres_exacts_taux', 'cadres_partiels', 'justes', 'attendus', 'predits', 'precision', 'rappel', 'f1', 'faux_positifs', 'faux_negatifs', 'vrais_negatifs', 'par_role']
  cadre None roles None None None
melange <class 'dict'> ['exacts', 'total', 'taux', 'cadres_exacts', 'cadres_exacts_taux', 'cadres_partiels', 'justes', 'attendus', 'predits', 'precision', 'rappel', 'f1', 'faux_positifs', 'faux_negatifs', 'vrais_negatifs', 'par_role']
  cadre None roles None None None
permutation_gp <class 'dict'> ['mapping', 'synthese']
  cadre 17 roles 37 77 0.5139
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, sys, pprint\nsys.path.insert(0,'.')\nimport tools.restitution as restitution\nimport tools.restitution_v3 as v3\nbanc=json.load(open('reports/pensee-fiabilite-produit.json'))\ngold=json.load(open('tool … [848 caractères tronqués]`

  ```
base cont keys dict_keys(['vide', 'constant_par_type', 'roles_melanges', 'rendu', 'negatif_rendu', 'spans_dans_source'])
vide cadres 7 roles 0 / 77 f1 0.0
constant_par_type cadres 6 roles 39 / 77 f1 0.4382
roles_melanges cadres 3 roles 0 / 77 f1 0.0
rendu cadres None roles None / None f1 None
negatif_rendu cadres None roles None / None f1 None
spans_dans_source cadres None roles 194 / None f1 None
--- vide etc ---
vide roles 0 / 77 f1 0.0
constant_par_type roles 39 / 77 f1 0.4382
melange roles 0 / 77 f1 0.0
permutation gp 17 14 37 77 0.5139
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, json\nsys.path.insert(0,'.')\nimport tools.restitution_v3 as v3\nm=v3.mesurer_gold_analyseur_v3()\nprint('tous mapping', json.dumps(m['permutation_tous']['mapping'],ensure_ascii=False,indent=1))\nprint( … [370 caractères tronqués]`

  ```
tous mapping {
 "agent": "but",
 "but": "cause",
 "cause": "concession",
 "concession": "consequence",
 "consequence": "contenu",
 "contenu": "destinataire",
 "destinataire": "hypothese",
 "hypothese": "lieu",
 "lieu": "maniere",
 "maniere": "moyen",
 "moyen": "patient",
 "patient": "possession",
 "possession": "predicat",
 "predicat": "prédicat",
 "prédicat": "qualite",
 "qualite": "temps",
 "temps": "theme",
 "theme": "agent"
}
perm tous par role {'agent': (0, 34, 4), 'but': (0, 3, 34), 'cause': (0, 4, 3), 'concession': (0, 1, 4), 'consequence': (0, 1, 1), 'contenu': (0, 5, 1), 'destinataire': (0, 5, 5), 'hypothese': (0, 2, 5), 'lieu': (0, 3, 2), 'maniere': (0, 1, 3), 'moyen': (0, 1, 1), 'patient': (0, 5, 1), 'possession': (0, 1, 5), 'predicat': (58, 58, 59), 'qualite': (0, 7, 0), 'temps': (0, 9, 7), 'theme': (0, 4, 9)}
perm cinq mapping {'lieu': 'temps', 'temps': 'destinataire', 'destinataire': 'possession', 'possession': 'complement', 'complement': 'lieu'}
perm cinq par role {'agent': (34, 34), 'but': (3, 3), 'cause': (4, 4), 'complement': (0, 0), 'concession': (1, 1), 'consequence': (1, 1), 'contenu': (5, 5), 'destinataire': (0, 5), 'hypothese': (2, 2), 'lieu': (0, 3), 'manier
… [144 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\ng=json.load(open('tools/tests/linguistique/gold_restitution_v2.json'))\nmissing=[]\nfor x in g['textes']:\n    v=x['variantes'][0]\n    for role in ('agent','predicat','lieu'):\n        val=v.get(role,'')\n        if val and val not in x['texte']:\n       … [170 caractères tronqués]`

  ```
missing 0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, collections, random, math, statistics\n\ndef norm(r):\n    return {'instrument':'moyen'}.get(r,r)\n\nd=json.load(open('tools/structures/donnees/gold-analyseur.json'))\nlabels=[]\nfor ph in d['phrases'] … [2403 caractères tronqués]`

  ```
144 Counter({'predicat': 58, 'agent': 34, 'hors_cadre': 34, 'temps': 9, 'destinataire': 5, 'lieu': 3, 'possession': 1})
{'accord_cible': 0.8, 'pkeep': 0.7225, 'kappa_moy': 0.619, 'kappa_ci': [0.5258, 0.7175], 'accord_observe_moy': 0.7227, 'pe_moy': 0.2724}
{'accord_cible': 0.85, 'pkeep': 0.7919, 'kappa_moy': 0.7131, 'kappa_ci': [0.6189, 0.7958], 'accord_observe_moy': 0.7917, 'pe_moy': 0.2738}
{'accord_cible': 0.9, 'pkeep': 0.8612, 'kappa_moy': 0.8072, 'kappa_ci': [0.7251, 0.8751], 'accord_observe_moy': 0.8603, 'pe_moy': 0.2755}
{'accord_cible': 0.95, 'pkeep': 0.9306, 'kappa_moy': 0.9054, 'kappa_ci': [0.8384, 0.9614], 'accord_observe_moy': 0.9317, 'pe_moy': 0.2777}
indep -0.0017 [-0.0992, 0.0914] po 0.2785
perm -0.0007 [-0.0889, 0.0942] po 0.2788
N 144 se 0.0333 ci95 0.0653
N 188 se 0.0292 ci95 0.0572
N 222 se 0.0268 ci95 0.0526
N 278 se 0.024 ci95 0.047
N 400 se 0.02 ci95 0.0392
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, collections, random, statistics\n\ndef norm(r): return {'instrument':'moyen'}.get(r,r)\nd=json.load(open('tools/structures/donnees/gold-analyseur.json'))\nlabels=[]\nfor ph in d['phrases']:\n    for sp … [2089 caractères tronqués]`

  ```
n 144 pe 0.2793
{'accord_cible': 0.8, 'pkeep': 0.7225, 'kappa_moy': 0.7205, 'kappa_ci': [0.6358, 0.808], 'accord_observe_moy': 0.7986}
{'accord_cible': 0.85, 'pkeep': 0.7919, 'kappa_moy': 0.79, 'kappa_ci': [0.7165, 0.8658], 'accord_observe_moy': 0.8487}
{'accord_cible': 0.9, 'pkeep': 0.8612, 'kappa_moy': 0.8602, 'kappa_ci': [0.7889, 0.9229], 'accord_observe_moy': 0.8992}
{'accord_cible': 0.95, 'pkeep': 0.9306, 'kappa_moy': 0.9298, 'kappa_ci': [0.8749, 0.9807], 'accord_observe_moy': 0.9494}
{'kappa_cible': 0.7, 'pkeep': 0.7838, 'kappa_moy': 0.7009, 'kappa_ci': [0.6053, 0.7877], 'accord_observe_moy': 0.7826}
{'kappa_cible': 0.8, 'pkeep': 0.8559, 'kappa_moy': 0.8001, 'kappa_ci': [0.715, 0.8753], 'accord_observe_moy': 0.8551}
{'kappa_cible': 0.9, 'pkeep': 0.9279, 'kappa_moy': 0.8997, 'kappa_ci': [0.8443, 0.9613], 'accord_observe_moy': 0.9275}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport collections, random, statistics, math\n\ndef stats(counts):\n    n=sum(counts.values()); pe=sum((v/n)**2 for v in counts.values())\n    return n, pe\n\ndef sim(counts, accord, nsim=1000, seed=20261115):\n    … [1125 caractères tronqués]`

  ```
base (222, 0.3069556042529015)
  0.85 (222, 0.307, 0.7829, [0.7114, 0.851], 0.0569)
  0.9 (222, 0.307, 0.8558, [0.7986, 0.9095], 0.0569)
  0.95 (222, 0.307, 0.9272, [0.8833, 0.9675], 0.0569)
post (312, 0.18108974358974358)
  0.85 (312, 0.1811, 0.8172, [0.7683, 0.8668], 0.0407)
  0.9 (312, 0.1811, 0.8781, [0.8354, 0.9175], 0.0407)
  0.95 (312, 0.1811, 0.9391, [0.9061, 0.9649], 0.0407)
  ```

- **bash** `{"command": "sed -n '1,160p' tools/roles_gp.py; echo \"---\"; grep -n \"complement\\|ROLES_GP\\|normaliser\" tools/roles_gp.py", "description": "Inspect roles_gp definitions"}`

  ```
"""roles_gp.py — les rôles des groupes prépositionnels (restitution v3).

La v2 lisait la **préposition seule** : `à` était toujours un destinataire, `de` toujours
un thème, `avec` toujours un moyen. La v3 ajoute le **contexte** : ce qui suit la
préposition (un lieu, un temps, une personne, un infinitif) et ce qui la précède (un GN
ou un GV, un passif). Le rôle sort alors parmi les cinq catégories nommées par la tâche
— `lieu`, `temps`, `destinataire`, `possession`, `complement` — plus les rôles déjà
connus (`theme`, `moyen`, `but`, `agent`, `maniere`, `concession`, `source`).

Le module est **pur** (pas d'import du bloc linguistique) : il peut être testé seul, et
le bloc le réutilise. La fonction de compatibilité `_role_gp(prep)` du bloc garde son
ancien comportement quand aucun contexte n'est fourni ; c'est la v3 qui passe le
contexte.

    from tools.roles_gp import role_gp
    role_gp("à", suivant="la maison")          # lieu
    role_gp("à", suivant="14 h")               # temps
    role_gp("à", suivant="Marie")              # destinataire
    role_gp("de", suivant="la voisine", precedent="GN")   # possession
    role_gp("de", suivant="son projet", precedent="GV")   # theme
  
… [8686 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport collections, random, statistics, math\n\ndef sim(counts, accord, nsim=1000, seed=20261115):\n    n=sum(counts.values()); pe=sum((v/n)**2 for v in counts.values())\n    cats=list(counts); freq=counts\n    pke … [1172 caractères tronqués]`

  ```
base 222
  0.8 {'n': 222, 'pe': 0.2993, 'kappa_moy': 0.7128, 'ci': [0.6355, 0.7873], 'po': 0.7988, 'ci_analytique': 0.0751}
  0.85 {'n': 222, 'pe': 0.2993, 'kappa_moy': 0.7862, 'ci': [0.713, 0.8477], 'po': 0.8502, 'ci_analytique': 0.067}
  0.9 {'n': 222, 'pe': 0.2993, 'kappa_moy': 0.8572, 'ci': [0.8015, 0.9154], 'po': 0.9, 'ci_analytique': 0.0563}
  0.95 {'n': 222, 'pe': 0.2993, 'kappa_moy': 0.9283, 'ci': [0.8847, 0.9678], 'po': 0.9498, 'ci_analytique': 0.0409}
post 312
  0.8 {'n': 312, 'pe': 0.1801, 'kappa_moy': 0.756, 'ci': [0.703, 0.8076], 'po': 0.7999, 'ci_analytique': 0.0541}
  0.85 {'n': 312, 'pe': 0.1801, 'kappa_moy': 0.8176, 'ci': [0.7696, 0.8638], 'po': 0.8504, 'ci_analytique': 0.0483}
  0.9 {'n': 312, 'pe': 0.1801, 'kappa_moy': 0.8778, 'ci': [0.8355, 0.9143], 'po': 0.8998, 'ci_analytique': 0.0406}
  0.95 {'n': 312, 'pe': 0.1801, 'kappa_moy': 0.939, 'ci': [0.9062, 0.9649], 'po': 0.95, 'ci_analytique': 0.0295}
  ```

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/schema-or-roles.json", "content": "{\n  \"$schema\": \"https://json-schema.org/draft/2020-12/schema\",\n  \"$id\": \"https://drave.local/schemas/or-roles-v1.json\",\n  \"title\": \"Drave — or de rôles : phrase, cadres, sept rôles … [9983 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/schema-or-roles.json</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"protocole_or_roles.py — le protocole de l'or de rôles (tâche X2, J4 matin).\n\nCe script ne modifie **jamais** le gold S. Il le lit, il compte ses 144 rôles, il projette\nles 17 étiquettes sur les **sept champs** du protocole (agent, predicat, lieu, temps,\ … [53319 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/protocole_or_roles.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nfrom pathlib import Path\np=Path('tools/protocole_or_roles.py')\ns=p.read_text()\ns=s.replace('\"items\": len(base[\"textes\"]),\\n                \"note\": base[\"note\"],',\n            '\"items\": b … [828 caractères tronqués]`

  ```
patched
713:                "items": base["sources"]["gold_v2"] + base["sources"]["gold_s"],
857:                "items": base["items"],
858:                "note": "graine provisoire des 46 textes v2",
977:    BASE.write_text(json.dumps(graine, ensure_ascii=False, indent=1) + "\n",
979:    SORTIE.write_text(json.dumps(rapport, ensure_ascii=False, indent=1) + "\n",
  ```

- **bash** `{"command": "sed -n '950,990p' tools/protocole_or_roles.py", "description": "Inspect main"}`

  ```
gold_v2 = inventaire_gold_v2()
    base = base_combinee(gold_s, gold_v2)
    supplement = plan_supplement(base)
    simulations = {
        "base": simuler_kappa(base["sept_champs"] | {"hors_champ": base["hors_champ_total"]}),
        "apres": simuler_kappa(supplement["apres"] | {"hors_champ": base["hors_champ_total"]}),
        "lecture": ("l'accord brut est la cible ; le kappa est calculé sur les 8 "
                    "catégories (7 champs + hors_champ). Le codeur indépendant et le "
                    "codeur permuté donnent ~0."),
    }
    controles = controles_existants()
    graine = construire_base_v2(lire(GOLD_V2))
    schema = lire(SCHEMA)
    verification = verifier_base(graine, schema)

    if verification["erreurs"]:
        print(f"❌ {verification['erreurs']} erreur(s) de schéma")
        for e in verification["detail"]:
            print("  ·", e)
        return 1
    if args.verifier:
        print(f"✅ schéma {verification['schema']} : {verification['items']} items, 0 erreur")
        return 0

    rapport = construire(gold_s, gold_v2, base, supplement, simulations, controles,
                         verification)
    rapport["mesures"]["kappa_simulation"] = sim
… [805 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nfrom pathlib import Path\np=Path('tools/protocole_or_roles.py')\ns=p.read_text()\ns=s.replace('''    rapport = construire(gold_s, gold_v2, base, supplement, simulations, controles,\n                         verific … [905 caractères tronqués]`

  ```
patched
[stderr]
Traceback (most recent call last):
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/protocole_or_roles.py", line 1014, in <module>
    raise SystemExit(main())
                     ~~~~^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/protocole_or_roles.py", line 960, in main
    controles = controles_existants()
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/protocole_or_roles.py", line 461, in controles_existants
    "cadres_total": base_banc["cadre"]["total"],
                    ~~~~~~~~~~~~~~~~~~^^^^^^^^^
KeyError: 'total'
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json,sys\nsys.path.insert(0,'.')\nimport tools.restitution as restitution, tools.restitution_v3 as v3\nbanc=json.load(open('reports/pensee-fiabilite-produit.json'))\ngold=json.load(open('tools/tests/linguist … [196 caractères tronqués]`

  ```
dict_keys(['exacts', 'taux', 'exacts_non_vides', 'exacts_vides', 'partiels', 'partiels_taux', 'exacts_stricts', 'taux_strict', 'roles_exacts_moyens'])
{'exacts': 20, 'taux': 0.4348, 'exacts_non_vides': 17, 'exacts_vides': 3, 'partiels': 43, 'partiels_taux': 0.9348, 'exacts_stricts': 17, 'taux_strict': 0.3696, 'roles_exacts_moyens': 2.0217}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json,sys\nsys.path.insert(0,'.')\nimport tools.restitution as restitution, tools.restitution_v3 as v3\nbanc=json.load(open('reports/pensee-fiabilite-produit.json'))\ngold=json.load(open('tools/tests/linguist … [228 caractères tronqués]`

  ```
dict_keys(['n', 'annotations', 'refus', 'refus_ids', 'or', 'cadre', 'or_textes', 'roles', 'couverture', 'controles'])
50 46 4
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nfrom pathlib import Path\np=Path('tools/protocole_or_roles.py')\ns=p.read_text().replace('\"cadres_total\": base_banc[\"cadre\"][\"total\"],',\n                        '\"cadres_total\": base_banc[\"annotations\"], … [148 caractères tronqués]`

  ```
patched
✅ schéma reports/schema-or-roles.json : 46 items, 0 erreur
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && time python3 tools/protocole_or_roles.py", "description": "Run full protocol tool"}`

  ```
✅ reports/rapport-or-roles-protocole.json
✅ reports/or-roles-base-v1.json (46 textes)
✅ schéma : 46 items, 0 erreur(s)
   gold S : 61 phrases, 144 rôles, 117 dans les 7 champs, 27 hors_champ
   base   : 222 mentions, 195 dans les 7 champs
   kappa  : base 90% -> 0.8572, après supplément -> 0.8778
   or permuté : S cinq {'justes': 0, 'attendus': 18, 'taux': 0.0}, v2 cinq 37/77
[stderr]

real	0m2,661s
user	0m2,623s
sys	0m0,038s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nd=json.load(open('reports/rapport-or-roles-protocole.json'))\nprint('keys', list(d.keys()))\nprint('verdict', d['verdict'])\nprint('\\nSOURCES gold S')\nfor k,v in d['sources']['gold_s'].items(): print … [1442 caractères tronqués]`

  ```
keys ['schema', 'version', 'date', 'ligne', 'tache', 'titre', 'verdict', 'sources', 'inventaire', 'protocole', 'mesures', 'controles', 'limites', 'fichiers', 'commande']
verdict Protocole livré : 61 phrases / 144 rôles S se projettent en 117 mentions des sept champs et 27 hors_champ ; avec les 46 textes v2, la base donne 222 mentions, dont 195 dans les sept champs ; le supplément de 60 phrases / 90 mentions porte chaque rôle à >= 20 et le kappa simulé à 90 % d'accord de 0,857 à 0,878 ; l'or permuté existant tombe à 0/18 sur les cinq rôles de GP et 0,4028 (borne haute) sur tous les rôles.

SOURCES gold S
  chemin tools/structures/donnees/gold-analyseur.json
  sha256 4cebc6d75b61db35acd3b2cbfc2a23924b25df3f020dce6038a2730adc2f8879
  phrases 61
  roles 144
  etiquettes 17
  spans_exacts 144
  sept_champs {'agent': 34, 'complement': 7, 'destinataire': 5, 'lieu': 3, 'possession': 1, 'predicat': 58, 'temps': 9}
  hors_champ {'but': 1, 'cause': 4, 'concession': 1, 'consequence': 1, 'contenu': 5, 'hypothese': 2, 'maniere': 1, 'patient': 5, 'qualite': 7}

INVENTAIRE S
  phrases 61
  roles 144
  etiquettes 17
  spans_exacts 144
  sept_champs {'agent': 34, 'complement': 7, 'destinataire': 5, 
… [7694 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nv3=json.load(open('reports/pensee-restitution-v3.json'))\nprint('v3 gold_s_sha', v3.get('gold_s_sha256'))\nprint('v3 gold sha', v3.get('gold_sha256'))\nprint('v3 gold_s', v3.get('gold_s'))\nEOF\nsha256 … [141 caractères tronqués]`

  ```
v3 gold_s_sha 4cebc6d75b61db35acd3b2cbfc2a23924b25df3f020dce6038a2730adc2f8879
v3 gold sha 1b5af926e55f514e806528c88c92c6852b0839784553c21ed927516b06b6b5ed
v3 gold_s {'or': 'tools/structures/donnees/gold-analyseur.json', 'appariement': 'v3', 'prepare': True, 'phrases': 61, 'roles': 144, 'apparies': 61, 'par_phrase': [{'id': 'p001', 'roles': 4, 'apparies': 4, 'justes': 4}, {'id': 'p002', 'roles': 3, 'apparies': 3, 'justes': 3}, {'id': 'p003', 'roles': 4, 'apparies': 4, 'justes': 4}, {'id': 'p004', 'roles': 2, 'apparies': 2, 'justes': 2}, {'id': 'p005', 'roles': 3, 'apparies': 3, 'justes': 3}, {'id': 'p006', 'roles': 3, 'apparies': 3, 'justes': 3}, {'id': 'p007', 'roles': 3, 'apparies': 3, 'justes': 3}, {'id': 'g008', 'roles': 3, 'apparies': 3, 'justes': 3}, {'id': 'g009', 'roles': 2, 'apparies': 2, 'justes': 2}, {'id': 'g010', 'roles': 3, 'apparies': 3, 'justes': 3}, {'id': 'g011', 'roles': 2, 'apparies': 2, 'justes': 2}, {'id': 'g012', 'roles': 2, 'apparies': 2, 'justes': 2}, {'id': 'g013', 'roles': 2, 'apparies': 2, 'justes': 2}, {'id': 'g014', 'roles': 2, 'apparies': 2, 'justes': 2}, {'id': 'g015', 'roles': 3, 'apparies': 3, 'justes': 3}, {'id': 'g016', 'roles': 3, 'apparies': 3,
… [15224 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nb=json.load(open('reports/or-roles-base-v1.json'))\nprint(b['schema'], b['version'], len(b['textes']))\nfor x in b['textes'][:4]:\n    print(json.dumps(x,ensure_ascii=False,indent=1))\nprint('--- hors_ … [240 caractères tronqués]`

  ```
drave.or.roles.base 1 46
{
 "schema": "drave.or.roles",
 "version": 1,
 "id": "or-f01",
 "source": "gold_v2",
 "source_id": "f01",
 "split": "base",
 "texte": "Le chat dort.",
 "langue": "fr",
 "cadres": [
  {
   "id": "c1",
   "principal": true,
   "roles": {
    "agent": [],
    "predicat": [
     {
      "texte": "dort",
      "debut": 8,
      "fin": 12
     }
    ],
    "lieu": [],
    "temps": [],
    "destinataire": [],
    "possession": [],
    "complement": []
   }
  }
 ],
 "hors_cadre": [
  {
   "role": "agent",
   "mention": {
    "texte": "Le chat",
    "debut": 0,
    "fin": 7
   },
   "raison": "phrase sans prédicat : rôle hors cadre"
  }
 ],
 "meta": {
  "codeur": "base",
  "date": "2026-11-15",
  "statut": "base",
  "protocole": 1,
  "a_completer": [
   "temps",
   "destinataire",
   "possession",
   "complement"
  ],
  "sha256_source": "1b5af926e55f514e806528c88c92c6852b0839784553c21ed927516b06b6b5ed",
  "note": "graine dérivée de la première variante du gold v2 ; les quatre rôles absents de la v2 sont vides et à annoter"
 }
}
{
 "schema": "drave.or.roles",
 "version": 1,
 "id": "or-f02",
 "source": "gold_v2",
 "source_id": "f02",
 "split": "base",
 "texte": "Le ch
… [7439 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nfrom pathlib import Path\np=Path('tools/protocole_or_roles.py')\ns=p.read_text()\nold='''        roles = {role: [] for role in SEPT}\n        hors = []\n        for role in (\"agent\", \"predicat\", \"lieu\"):\n    … [2045 caractères tronqués]`

  ```
patched
✅ reports/rapport-or-roles-protocole.json
✅ reports/or-roles-base-v1.json (46 textes)
✅ schéma : 46 items, 0 erreur(s)
   gold S : 61 phrases, 144 rôles, 117 dans les 7 champs, 27 hors_champ
   base   : 222 mentions, 195 dans les 7 champs
   kappa  : base 90% -> 0.8572, après supplément -> 0.8778
   or permuté : S cinq {'justes': 0, 'attendus': 18, 'taux': 0.0}, v2 cinq 37/77
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nb=json.load(open('reports/or-roles-base-v1.json'))\nfor x in b['textes'][:3]:\n    print(x['id'], 'cadres', len(x['cadres']), 'principal', [c['principal'] for c in x['cadres']])\n    if x['cadres']:\n  … [406 caractères tronqués]`

  ```
or-f01 cadres 1 principal [True]
 roles {'agent': ['Le chat'], 'predicat': ['dort']}
 hors []
or-f02 cadres 1 principal [True]
 roles {'agent': ['Le chat de la voisine'], 'predicat': ['se réveille']}
 hors []
or-f03 cadres 1 principal [True]
 roles {'agent': ['vous'], 'predicat': ['allez']}
 hors []
--- no cadres ---
or-f18 1234567890 []
or-f25 Pourquoi ? Parce que. []
or-f37 Email: alice@example.org, phone: +33 6 12 34 56 78. []
or-f39 Un fichier /home/user/notes.txt et un chemin C:\Windows\System32. []
or-f40 Les caractères spéciaux : @ # $ % & * ( ) [ ] { } < > | \ ~ ` ^ []
or-f42 Un mot très long : anticonstitutionnellement. []
or-f48 Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. []
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nd=json.load(open('reports/rapport-or-roles-protocole.json'))\nfor c in d['inventaire']['gold_s']['cas_limites']:\n    print(c['id'], c['split'], c['predicats'], '|', c['texte'])\n    print('  ', c['att … [403 caractères tronqués]`

  ```
h031 holdout 2 | Il court mais il ne rit pas.
   [['Il court', 'GV', 'predicat'], ['il ne rit pas', 'GV', 'predicat']]
h043 holdout 0 | Une belle maison.
   [['Une belle maison', 'GN', 'agent']]
h052 holdout 0 | La ferme.
   [['La ferme', 'GN', 'agent']]
h053 holdout 0 | Le grand lit.
   [['Le grand lit', 'GN', 'agent']]
h059 holdout 0 | La vieille porte.
   [['La vieille porte', 'GN', 'agent']]

labels
predicat: 58
agent: 34
temps: 9
qualite: 7
contenu: 5
destinataire: 5
patient: 5
cause: 4
theme: 4
but: 3
lieu: 3
hypothese: 2
concession: 1
consequence: 1
instrument: 1
maniere: 1
possession: 1

type-role
GN/agent: 31
GN/patient: 5
GP/agent: 3
GP/but: 2
GP/destinataire: 5
GP/instrument: 1
GP/lieu: 3
GP/possession: 1
GP/temps: 4
GP/theme: 4
GV/predicat: 58
REL/qualite: 7
SUB/but: 1
SUB/cause: 4
SUB/concession: 1
SUB/consequence: 1
SUB/contenu: 5
SUB/hypothese: 2
SUB/maniere: 1
SUB/temps: 5

base sept {'agent': 66, 'predicat': 97, 'lieu': 10, 'temps': 9, 'destinataire': 5, 'possession': 1, 'complement': 7}
supp apres {'agent': 66, 'predicat': 97, 'lieu': 20, 'temps': 29, 'destinataire': 25, 'possession': 21, 'complement': 27}
  ```

- **write** `{"content": "# J4 — L'or de rôles : sept champs, deux codeurs, 144 rôles S, un or permuté\n\n> **Ligne de roadmap** : **B13 / R0.7** · **Tâche** : X2 (J4 matin, la part du pilote) ·\n> **Date** : 2026-11-15 · **Verdict** : protocole livré, **gold S non modifié**\n> (SHA-256 `4cebc6d7…f8879` avant et … [18804 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-or-roles-protocole.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nd=json.load(open('reports/rapport-or-roles-protocole.json'))\nprint('regles', len(d['protocole']['regles_de_decision']))\nprint('champs', list(d['protocole']['champs']))\nprint('limites', len(d['limite … [325 caractères tronqués]`

  ```
regles 27
champs ['phrase', 'cadre', 'roles', 'hors_cadre', 'meta']
limites 10
fichiers [{'chemin': 'reports/schema-or-roles.json', 'role': "schéma JSON du record d'annotation"}, {'chemin': 'reports/or-roles-base-v1.json', 'role': 'graine des 46 textes v2, provisoire'}, {'chemin': 'reports/rapport-or-roles-protocole.json', 'role': 'protocole, inventaire, simulations, contrôles'}, {'chemin': 'tools/structures/donnees/gold-analyseur.json', 'role': 'gold S, lecture seule'}, {'chemin': 'tools/tests/linguistique/gold_restitution_v2.json', 'role': 'gold v2, base de départ'}]
base sha {'chemin': 'reports/or-roles-base-v1.json', 'sha256': '17b74d9a4e40e4e5194730f229690a3e0927f473676d5e69b06a5c4626765c5c', 'items': 107, 'note': 'graine provisoire des 46 textes v2'}
gold s sha 4cebc6d75b61db35acd3b2cbfc2a23924b25df3f020dce6038a2730adc2f8879
   331 reports/rapport-or-roles-protocole.md
  1370 reports/rapport-or-roles-protocole.json
   240 reports/schema-or-roles.json
  2220 reports/or-roles-base-v1.json
  4161 total
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"def construire\\|construire(gold_s\\|items\\\": base\\[\\\"items\\\"\\]\" tools/protocole_or_roles.py", "description": "Locate construire signature"}`

  ```
508:def construire_base_v2(gold_v2: dict) -> dict:
825:def construire(gold_s: dict, gold_v2: dict, base: dict, supplement: dict,
858:                "items": base["items"],
977:    rapport = construire(gold_s, gold_v2, base, supplement, simulations, controles,
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nfrom pathlib import Path\np=Path('tools/protocole_or_roles.py')\ns=p.read_text()\ns=s.replace('def construire(gold_s: dict, gold_v2: dict, base: dict, supplement: dict,\\n               simulations: dict, controles … [858 caractères tronqués]`

  ```
patched
✅ reports/rapport-or-roles-protocole.json
✅ reports/or-roles-base-v1.json (46 textes)
✅ schéma : 46 items, 0 erreur(s)
   gold S : 61 phrases, 144 rôles, 117 dans les 7 champs, 27 hors_champ
   base   : 222 mentions, 195 dans les 7 champs
   kappa  : base 90% -> 0.8572, après supplément -> 0.8778
   or permuté : S cinq {'justes': 0, 'attendus': 18, 'taux': 0.0}, v2 cinq 37/77
{'chemin': 'reports/or-roles-base-v1.json', 'sha256': '17b74d9a4e40e4e5194730f229690a3e0927f473676d5e69b06a5c4626765c5c', 'items': 46, 'note': 'graine provisoire des 46 textes v2'}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '300,340p' reports/rapport-or-roles-protocole.md", "description": "Show end of report"}`

  ```
- **Le pilote ne modifie pas le gold S** : si S change ses étiquettes, la comparaison et
  les 144 rôles doivent être rejoués, et le SHA-256 publié.

## 5. La décision et la suite

**Pour S.** Valider le schéma, désigner le codeur B, faire la calibration, annoter les
**167 items**, adjudiquer, geler le gold avec un SHA-256, calculer le kappa et publier le
contrôle permuté. **Le pilote ne touche ni au gold S ni à `tools/structures/`** : il livre
le schéma, la graine, l'inventaire et le protocole.

**Ce que le protocole n'est pas.** Ce n'est pas un gold : la graine de 46 textes est
`provisoire`, les quatre rôles absents de la v2 sont vides, et les 61 phrases S ne sont pas
re-annotées ici. C'est un **contrat** : champs, définitions, échantillon, double annotation,
kappa, plafonds de permutation.

**La prochaine action.** S reprend le protocole ; le pilote peut, en attendant, étendre la
graine aux quatre rôles manquants sur les 46 textes (sans les compter comme gold) et
préparer les 60 phrases du supplément. La ligne B13 / R0.7 reste la même : le produit ne
gagne pas tant que le gold n'est pas double-annoté.

## 6. Fichiers

- `reports/schema-or-roles.json` — le schéma Draft 2020-12 (4
… [679 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nfrom pathlib import Path\np=Path('reports/rapport-or-roles-protocole.md')\ns=p.read_text()\nstart=s.index('## 5. La décision et la suite')\nnew='''## 5. La décision et la suite\n\n**Pour S.** Valider le schéma, dés … [1465 caractères tronqués]`

  ```
324 reports/rapport-or-roles-protocole.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n '^##\\|^###' reports/rapport-or-roles-protocole.md", "description": "List report sections"}`

  ```
29:## 1. Les sources et l'inventaire
31:### 1.1 Le gold S — 61 phrases, 144 rôles, 17 étiquettes
63:### 1.2 Le gold v2 — 46 textes, 65 variantes, 3 rôles
75:### 1.3 La base commune — 222 mentions, 195 dans les sept champs
98:## 2. Le protocole d'annotation
100:### 2.1 Les champs
118:### 2.2 Les définitions
144:### 2.3 Les cadres et le hors-cadre
156:### 2.4 L'échantillon
170:### 2.5 La double annotation
186:### 2.6 Le kappa
226:## 3. Le contrôle négatif : l'or permuté doit s'effondrer
228:### 3.1 Ce que la v3 mesure déjà
265:### 3.2 Les plafonds du nouveau gold
278:## 4. Ce qui pourrait rendre cette fiche fausse
303:## 5. La décision et la suite
316:## 6. Fichiers
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && awk 'BEGIN{b=0} /^$/{b++; if(b>1) print NR\": double blank\"; next} {b=0}' reports/rapport-or-roles-protocole.md | head -20; echo \"--- blank count ---\"; grep -c '^$' reports/rapport-or-roles-protocole.md", "description": "Count bla … [10 caractères tronqués]`

  ```
--- blank count ---
61
  ```

- **bash** `{"command": "grep -n \"300\\|lignes\\|fiches\" tools/taille_documents.py | head -30", "description": "Check size tool thresholds"}`

  ```
8:  3. les fiches de résultats trop longues pour être lues d'un bloc (avertissement, pas échec) ;
11:Les fiches de `reports/` (sauf `reports/README.md`) et le `journal/` sont **hors budget** :
97:    lignes: list[tuple[int, int, str, str, int]] = []
110:            lignes.append((n, t.count("\n") + 1, rel, cat, budget))
116:                    violations.append(f"{rel} : pas de résumé (blockquote) dans les 20 premières lignes")
125:    # fiches de résultats trop longues : avertissement, pas échec
131:        if n > 300:
136:            f"{len(longues)} fiche(s) > 300 lignes : lire le verdict + une section, jamais tout "
157:    lignes.sort(reverse=True)
159:    print(f"  {'mots':>6} {'lignes':>6} {'cat':>4} {'budget':>6}  document")
160:    for n, l, rel, cat, budget in lignes[:18]:
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py 2>&1 | tail -40", "description": "Run documentation review"}`

  ```
revue de documentation · 756 fiche(s) · 851 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ❌ 2 anomalie(s) :
     · compteurs : en-cours.md dit 755 fichiers, le disque en a 756
     · compteurs : en-cours.md dit 848 JSON, le disque en a 851
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nfrom pathlib import Path\np=Path('tools/protocole_or_roles.py')\ns=p.read_text()\ns=s.replace('import argparse\\nimport collections', 'import argparse\\nimport collections\\nimport copy')\nold='''def verifier_base( … [4964 caractères tronqués]`

  ```
patched
✅ schéma reports/schema-or-roles.json : 46 items, 0 erreur
✅ reports/rapport-or-roles-protocole.json
✅ reports/or-roles-base-v1.json (46 textes)
✅ schéma : 46 items, 0 erreur(s)
   gold S : 61 phrases, 144 rôles, 117 dans les 7 champs, 27 hors_champ
   base   : 222 mentions, 195 dans les 7 champs
   kappa  : base 90% -> 0.8572, après supplément -> 0.8778
   or permuté : S cinq {'justes': 0, 'attendus': 18, 'taux': 0.0}, v2 cinq 37/77
{
 "schema": "reports/schema-or-roles.json",
 "schema_sha256": "a0b40f109411cb96625ba04d0588e69ac2caeab2e723eba597363524855bf474",
 "items": 46,
 "erreurs": 0,
 "detail": [],
 "validateur": "jsonschema Draft 2020-12 + contrôles de spans",
 "negatif": {
  "cas": 4,
  "refuses": 4,
  "detail": [
   {
    "cas": "sans_agent",
    "refuse": true
   },
   {
    "cas": "deux_principaux",
    "refuse": true
   },
   {
    "cas": "span_faux",
    "refuse": true
   },
   {
    "cas": "sans_predicat",
    "refuse": true
   }
  ]
 }
}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nfrom pathlib import Path\np=Path('reports/rapport-or-roles-protocole.md')\ns=p.read_text()\nold='''Le schéma JSON est [`schema-or-roles.json`](schema-or-roles.json) (Draft 2020-12). Il est\nvalidé par [`protocole_o … [681 caractères tronqués]`

  ```
ok
326 reports/rapport-or-roles-protocole.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nfrom pathlib import Path\np=Path('reports/rapport-or-roles-protocole.md')\ns=p.read_text().replace('`theme`, `moyen`, `but`, `patient`, `qualite`…', '`theme`, `instrument`, `but`, `patient`, `qualite`…')\np.write_t … [135 caractères tronqués]`

  ```
ok
141:conserve (`theme`, `instrument`, `but`, `patient`, `qualite`…). La couche des sept champs est
287:  `instrument` et `but` prépositionnels tombent dans `complement` ; `patient`, `qualite`
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sha256sum reports/or-roles-base-v1.json reports/rapport-or-roles-protocole.json reports/schema-or-roles.json && python3 - <<'EOF'\nimport json,hashlib\np='reports/or-roles-base-v1.json'\nprint('base sha file', hashlib.sha256(open(p,' … [472 caractères tronqués]`

  ```
17b74d9a4e40e4e5194730f229690a3e0927f473676d5e69b06a5c4626765c5c  reports/or-roles-base-v1.json
f9499e466b30cfe45911ac38a7591d6cf0865f31d5923e46cb841e17089dcd00  reports/rapport-or-roles-protocole.json
a0b40f109411cb96625ba04d0588e69ac2caeab2e723eba597363524855bf474  reports/schema-or-roles.json
base sha file 17b74d9a4e40e4e5194730f229690a3e0927f473676d5e69b06a5c4626765c5c
base sha json 17b74d9a4e40e4e5194730f229690a3e0927f473676d5e69b06a5c4626765c5c
protocol sha file f9499e466b30cfe45911ac38a7591d6cf0865f31d5923e46cb841e17089dcd00
schema sha file a0b40f109411cb96625ba04d0588e69ac2caeab2e723eba597363524855bf474
schema sha json a0b40f109411cb96625ba04d0588e69ac2caeab2e723eba597363524855bf474
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport re, pathlib\np=pathlib.Path('reports/rapport-or-roles-protocole.md')\ns=p.read_text()\nlinks=re.findall(r'\\]\\(([^)]+)\\)',s)\nfor l in sorted(set(links)):\n    if l.startswith(('http://','https://','#')):  … [436 caractères tronqués]`

  ```
OK ../tools/protocole_or_roles.py -> /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/protocole_or_roles.py
OK ../tools/structures/donnees/gold-analyseur.json -> /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/donnees/gold-analyseur.json
OK ../tools/tests/linguistique/gold_restitution_v2.json -> /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_restitution_v2.json
OK or-roles-base-v1.json -> /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/or-roles-base-v1.json
OK rapport-or-roles-protocole.json -> /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-or-roles-protocole.json
OK rapport-restitution-v3.md -> /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-restitution-v3.md
OK schema-or-roles.json -> /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/schema-or-roles.json
OK tools/protocole_or_roles.py
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && bash tools/porte-tableaux.sh 2>&1 | tail -30; echo \"exit=$?\"", "description": "Run table gate"}`

  ```
✅ 1832 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4577 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-15)
exit=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, jsonschema\nschema=json.load(open('reports/schema-or-roles.json'))\njsonschema.Draft202012Validator.check_schema(schema)\nbase=json.load(open('reports/or-roles-base-v1.json'))\nv=jsonschema.Draft202012 … [395 caractères tronqués]`

  ```
schema OK, base items 46 errors 0
JSON OK reports/rapport-or-roles-protocole.json
JSON OK reports/or-roles-base-v1.json
JSON OK reports/schema-or-roles.json
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n 'role_etendu\\|moyen\\|instrument' tools/protocole_or_roles.py | head -30", "description": "Find moyen/instrument in tool"}`

  ```
59:GP_VERS_COMPLEMENT = {"theme", "instrument", "but"}
83:    - ``theme``, ``instrument`` et ``but`` **prépositionnels** sont des compléments
351:            "kappa_moyen": round(statistics.mean(ks), 4),
374:            "kappa_moyen": round(statistics.mean(indep), 4),
379:            "kappa_moyen": round(statistics.mean(perm), 4),
714:                           "avec le télescope, à la réunion. Le rôle étendu (theme, moyen, "
715:                           "but) est conservé dans role_etendu ; il ne crée pas une "
727:            {"regle": "à + infinitif", "exemples": ["à manger", "à faire"], "role": "complement", "role_etendu": "but"},
729:            {"regle": "de + GV / de + thème", "exemples": ["parler de son projet"], "role": "complement", "role_etendu": "theme"},
730:            {"regle": "avec + instrument", "exemples": ["avec le télescope"], "role": "complement", "role_etendu": "moyen"},
732:            {"regle": "par + moyen / lieu", "exemples": ["entrer par la porte"], "role": "complement", "role_etendu": "moyen"},
734:            {"regle": "pour + but", "exemples": ["pour la documentation"], "role": "complement", "role_etendu": "but"},
740:            {"regle": "en + véh
… [795 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nfrom pathlib import Path\np=Path('tools/protocole_or_roles.py')\ns=p.read_text()\ns=s.replace('Le rôle étendu (theme, moyen, \"\\n                           \"but) est conservé dans role_etendu',\n            'Le r … [582 caractères tronqués]`

  ```
patched
✅ reports/rapport-or-roles-protocole.json
✅ reports/or-roles-base-v1.json (46 textes)
✅ schéma : 46 items, 0 erreur(s)
   gold S : 61 phrases, 144 rôles, 117 dans les 7 champs, 27 hors_champ
   base   : 222 mentions, 195 dans les 7 champs
   kappa  : base 90% -> 0.8572, après supplément -> 0.8778
   or permuté : S cinq {'justes': 0, 'attendus': 18, 'taux': 0.0}, v2 cinq 37/77
714:                           "avec le télescope, à la réunion. Le rôle étendu (theme, instrument/moyen, "
730:            {"regle": "avec + instrument", "exemples": ["avec le télescope"], "role": "complement", "role_etendu": "instrument"},
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sha256sum reports/or-roles-base-v1.json && python3 - <<'EOF'\nimport json,hashlib\nd=json.load(open('reports/rapport-or-roles-protocole.json'))\nprint(d['sources']['base']['sha256'])\nprint(hashlib.sha256(open('reports/or-roles-base- … [87 caractères tronqués]`

  ```
17b74d9a4e40e4e5194730f229690a3e0927f473676d5e69b06a5c4626765c5c  reports/or-roles-base-v1.json
17b74d9a4e40e4e5194730f229690a3e0927f473676d5e69b06a5c4626765c5c
17b74d9a4e40e4e5194730f229690a3e0927f473676d5e69b06a5c4626765c5c
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nd=json.load(open('reports/rapport-or-roles-protocole.json'))\nprint('echantillon', json.dumps(d['protocole']['echantillon'],ensure_ascii=False,indent=1)[:1800])\nprint('double', json.dumps(d['protocole … [403 caractères tronqués]`

  ```
echantillon {
 "base": {
  "items": 107,
  "gold_v2": 46,
  "gold_s": 61,
  "mentions": 222,
  "sept_champs": 195,
  "hors_champ": 27
 },
 "supplement": {
  "phrases": 60,
  "mentions": 90,
  "cibles": {
   "temps": 20,
   "destinataire": 20,
   "possession": 20,
   "complement": 20,
   "lieu": 10
  },
  "apres": {
   "agent": 66,
   "predicat": 97,
   "lieu": 20,
   "temps": 29,
   "destinataire": 25,
   "possession": 21,
   "complement": 27
  },
  "apres_total_sept": 285,
  "apres_total": 312,
  "items_total": 167,
  "regle": "60 phrases neuves, 90 mentions ciblées : 20 temps, 20 destinataire, 20 possession, 20 complement, 10 lieu ; une phrase peut porter deux rôles, d'où 90 mentions pour 60 phrases.",
  "pourquoi": "chaque rôle des sept champs atteint au moins 20 mentions ; la prévalence attendue passe de 0,299 à 0,180, ce qui rend le kappa moins sensible au paradoxe de prévalence.",
  "limite": "supplément ciblé, pas un échantillon aléatoire : il sert au rappel par rôle et au kappa, pas à estimer la prévalence ni la F1 générale."
 },
 "total": {
  "items": 167,
  "mentions": 312,
  "sept_champs": 285,
  "hors_champ": 27
 },
 "aveugle": "les codeurs ne voient pas les étiquettes 
… [4108 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short | grep -E \"or-roles|protocole|schema-or|structures\" ; echo \"--- submodule ---\"; git -C tools/structures status --short 2>/dev/null | head; echo \"--- gold sha ---\"; sha256sum tools/structures/donnees/gold-anal … [68 caractères tronqués]`

  ```
?? reports/or-roles-base-v1.json
?? reports/rapport-or-roles-protocole.json
?? reports/rapport-or-roles-protocole.md
?? reports/schema-or-roles.json
?? tools/protocole_or_roles.py
--- submodule ---
--- gold sha ---
4cebc6d75b61db35acd3b2cbfc2a23924b25df3f020dce6038a2730adc2f8879  tools/structures/donnees/gold-analyseur.json
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/taille_documents.py 2>&1 | tail -25", "description": "Check document size tool"}`

  ```
mots lignes  cat budget  document
    9000    493   T1   9000  docs/pilotage/roadmap.md
    5999    597 DATÉ      0  docs/implantation/contexte-long.md
    4858    515   T1   5000  docs/theorie/glossaire/10-le-pont-linguistico-semantique-le-vocabu.md
    4085    431 DATÉ      0  docs/implantation/numa-segregation.md
    3310    317   T1   3500  README.md
    3072    341 DATÉ      0  docs/implantation/convertisseur.md
    2962    364   T1   5000  docs/theorie/glossaire/02-modeles-et-architectures.md
    2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2663    229   T1   2800  reports/README.md
    2433    164   T1   2500  docs/pilotage/references-non-regression.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/th
… [457 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"datetime\\|argparse\" tools/protocole_or_roles.py | head; python3 -m py_compile tools/protocole_or_roles.py && echo \"py_compile OK\"", "description": "Check unused imports and compile"}`

  ```
32:import argparse
35:import datetime
986:    parser = argparse.ArgumentParser(description=__doc__)
py_compile OK
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nfrom pathlib import Path\np=Path('tools/protocole_or_roles.py')\ns=p.read_text().replace('import datetime\\n','')\np.write_text(s)\nprint('removed datetime')\nEOF\npython3 -m py_compile tools/protocole_or_roles.py  … [101 caractères tronqués]`

  ```
removed datetime
✅ schéma reports/schema-or-roles.json : 46 items, 0 erreur
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py 2>&1 | tail -10; echo \"---\"; bash tools/porte-tableaux.sh 2>&1 | tail -4", "description": "Re-run docs review and table gate"}`

  ```
revue de documentation · 756 fiche(s) · 851 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ❌ 2 anomalie(s) :
     · compteurs : en-cours.md dit 755 fichiers, le disque en a 756
     · compteurs : en-cours.md dit 848 JSON, le disque en a 851
---
  ✅ 1832 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4577 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-15)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff --stat docs/pilotage/en-cours.md && git diff docs/pilotage/en-cours.md | head -80", "description": "Inspect en-cours diff"}`

  ```
docs/pilotage/en-cours.md | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index be629f05..9d6c13ce 100644
--- a/docs/pilotage/en-cours.md
+++ b/docs/pilotage/en-cours.md
@@ -102,7 +102,7 @@
 |---|---|---|
 | portes | **85** (dont `porte-cic` le 14/11) | `tools/porte-*.sh` |
 | chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
-| fichiers / JSON de résultats | **754** / **847** | `reports/*.md` / `reports/*.json` |
+| fichiers / JSON de résultats | **755** / **848** | `reports/*.md` / `reports/*.json` |
 | documents de `docs/` | **124** (hors archive et README) | `docs/**/*.md` |
 | dernière passe | **15/11 09 h 53 → 12 h 15** (85, **81/4**) ; rouges `indice`, `melange` (structurelles), `sessions` (**réparée** à 12 h 20), `prechargement` (**environnementale**) ; ciblage W6 **9/9** | `work/portes-1115-09h53/registre.txt` ; `work/portes/w6-final/` |
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,30p' reports/rapport-or-roles-protocole.md", "description": "Show report intro"}`

  ```
# J4 — L'or de rôles : sept champs, deux codeurs, 144 rôles S, un or permuté

> **Ligne de roadmap** : **B13 / R0.7** · **Tâche** : X2 (J4 matin, la part du pilote) ·
> **Date** : 2026-11-15 · **Verdict** : protocole livré, **gold S non modifié**
> (SHA-256 `4cebc6d7…f8879` avant et après). Les **61 phrases / 144 rôles** du gold S se
> projettent en **117 mentions des sept champs** et **27 hors_champ** ; avec les **46 textes**
> du gold v2, la base donne **222 mentions** dont **195** dans les sept champs. Les quatre
> rôles rares n'y sont pas mesurables : `temps` 9, `destinataire` 5, `possession` 1,
> `complement` 7. Un **supplément de 60 phrases / 90 mentions** porte chaque rôle à ≥ 20 ;
> le kappa simulé à 90 % d'accord passe de **0,857** à **0,878**, et l'or permuté existant
> s'effondre à **0/18** sur les cinq rôles de GP. Le protocole est prêt pour S ; le pilote
> n'écrit ni dans le gold S ni dans `tools/structures/`.

**La question.** Le gold v2 (46 textes) n'annote que **trois** rôles (`agent`, `predicat`,
`lieu`) et un **cadre principal** ; le gold S (61 phrases) annote **144 rôles** en **17
étiquettes**, mais seulement **117** dans les sept champs du produit et **0** `comp
… [879 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nfrom pathlib import Path\np=Path('reports/rapport-or-roles-protocole.md')\ns=p.read_text()\ns=s.replace(\"mais seulement **117** dans les sept champs du produit et **0** `complement`\\nau sens strict de la v3.\",\n … [304 caractères tronqués]`

  ```
ok
**La question.** Le gold v2 (46 textes) n'annote que **trois** rôles (`agent`, `predicat`,
`lieu`) et un **cadre principal** ; le gold S (61 phrases) annote **144 rôles** en **17
étiquettes**, mais seulement **117** dans les sept champs du produit et **0** étiquette
`complement` (7 seulement par projection des GP `theme`/`instrument`/`but`). Comment construire un or qui mesure les **sept champs**
(`agent`, `predicat`, `lieu`, `temps`, `destinataire`, `possession`, `complement`), avec
**deux codeurs**, un **kappa publiable**, les seconds cadres et les rôles hors cadre — sans
toucher au gold S, et avec un **or permuté qui tue la mesure** ?
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nfrom pathlib import Path\np=Path('reports/rapport-or-roles-protocole.md')\ns=p.read_text()\nold='''**La question.** Le gold v2 (46 textes) n'annote que **trois** rôles (`agent`, `predicat`,\n`lieu`) et un **cadre p … [1368 caractères tronqués]`

  ```
ok
327 reports/rapport-or-roles-protocole.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nd=json.load(open('reports/rapport-or-roles-protocole.json'))\ns=d['inventaire']['gold_s']; b=d['inventaire']['base_combinee']; sup=d['inventaire']['supplement']\nprint('S sept sum', sum(s['sept_champs' … [789 caractères tronqués]`

  ```
S sept sum 117 117
S hors sum 27 27
S total 144 144
base sept sum 195 195
base hors 27 base total 222 222
supp cibles sum 90 90
supp apres sum 285 285
supp total 312 312
items 167 167
base source sum 222 222
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nfrom pathlib import Path\np=Path('reports/rapport-or-roles-protocole.md')\ns=p.read_text()\nold='''C'est un or de **cadre principal**, pas une annotation complète : les seconds cadres, les\nsubordonnées et les quat … [692 caractères tronqués]`

  ```
ok
328 reports/rapport-or-roles-protocole.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && test -f reports/rapport-or-roles-protocole.md && echo FICHE-OK; test -f reports/schema-or-roles.json && echo SCHEMA-OK; test -f reports/rapport-or-roles-protocole.json && echo JSON-OK; test -f reports/or-roles-base-v1.json && echo BA … [47 caractères tronqués]`

  ```
FICHE-OK
SCHEMA-OK
JSON-OK
BASE-OK
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sha256sum reports/schema-or-roles.json && python3 -c \"import json;d=json.load(open('reports/rapport-or-roles-protocole.json'));print(d['sources']['schema']['sha256']);print(d['controles']['gold_s_inchange'])\"", "description": "Veri … [34 caractères tronqués]`

  ```
a0b40f109411cb96625ba04d0588e69ac2caeab2e723eba597363524855bf474  reports/schema-or-roles.json
a0b40f109411cb96625ba04d0588e69ac2caeab2e723eba597363524855bf474
{'sha256_avant': '4cebc6d75b61db35acd3b2cbfc2a23924b25df3f020dce6038a2730adc2f8879', 'sha256_apres': '4cebc6d75b61db35acd3b2cbfc2a23924b25df3f020dce6038a2730adc2f8879', 'identique': True, 'note': 'le script ne fait que lire le gold S ; aucun écrivain ne le touche.'}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && set -e\npython3 tools/protocole_or_roles.py >/tmp/final_proto.txt\ncat /tmp/final_proto.txt\npython3 -m json.tool reports/rapport-or-roles-protocole.json >/dev/null && echo JSON-PROTO-OK\npython3 -m json.tool reports/schema-or-roles. … [626 caractères tronqués]`

  ```
✅ reports/rapport-or-roles-protocole.json
✅ reports/or-roles-base-v1.json (46 textes)
✅ schéma : 46 items, 0 erreur(s)
   gold S : 61 phrases, 144 rôles, 117 dans les 7 champs, 27 hors_champ
   base   : 222 mentions, 195 dans les 7 champs
   kappa  : base 90% -> 0.8572, après supplément -> 0.8778
   or permuté : S cinq {'justes': 0, 'attendus': 18, 'taux': 0.0}, v2 cinq 37/77
JSON-PROTO-OK
JSON-SCHEMA-OK
JSON-BASE-OK
SCHEMA-VALID 46 items 0 errors
4cebc6d75b61db35acd3b2cbfc2a23924b25df3f020dce6038a2730adc2f8879  tools/structures/donnees/gold-analyseur.json
0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nfrom pathlib import Path\np=Path('reports/rapport-or-roles-protocole.md')\ns=p.read_text()\nold='''**Le point dur est là** : sans supplément, `possession` a **1** mention, `destinataire` 5,\n`complement` 7, `temps` … [499 caractères tronqués]`

  ```
ok
331 reports/rapport-or-roles-protocole.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && bash tools/porte-tableaux.sh 2>&1 | tail -4", "description": "Re-run table gate"}`

  ```
✅ 1832 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4577 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-15)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nfrom pathlib import Path\n# Report\np=Path('reports/rapport-or-roles-protocole.md')\ns=p.read_text()\ns=s.replace('Un **supplément de 60 phrases / 90 mentions** porte chaque rôle à ≥ 20 ;',\n            'Le protoco … [657 caractères tronqués]`

  ```
patched
✅ reports/rapport-or-roles-protocole.json
✅ reports/or-roles-base-v1.json (46 textes)
✅ schéma : 46 items, 0 erreur(s)
   gold S : 61 phrases, 144 rôles, 117 dans les 7 champs, 27 hors_champ
   base   : 222 mentions, 195 dans les 7 champs
   kappa  : base 90% -> 0.8572, après supplément -> 0.8778
   or permuté : S cinq {'justes': 0, 'attendus': 18, 'taux': 0.0}, v2 cinq 37/77
reports/rapport-or-roles-protocole.md:9:> `complement` 7. Le protocole prévoit un **supplément de 60 phrases / 90 mentions** qui porte chaque rôle à ≥ 20 ;
reports/rapport-or-roles-protocole.json:8: "verdict": "Protocole livré : 61 phrases / 144 rôles S se projettent en 117 mentions des sept champs et 27 hors_champ ; avec les 46 textes v2, la base donne 222 mentions, dont 195 dans les sept champs ; le supplément de 60 phrases / 90 mentions porte chaque rôle à >= 20 et le kappa simulé à 90 % d'accord de 0,857 à 0,878 ; l'or permuté existant tombe à 0/18 sur les cinq rôles de GP et 0,4028 (borne haute) sur tous les rôles.",
reports/rapport-or-roles-protocole.json:1361:  "Le supplément de 60 phrases est ciblé, pas aléatoire : il sert au rappel par rôle et au kappa, pas à estimer la prévalence ni une F1 gé
… [9 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"supplément de 60\" tools/protocole_or_roles.py", "description": "Find verdict string"}`

  ```
877:                    "supplément de 60 phrases / 90 mentions porte chaque rôle à >= 20 "
965:            "Le supplément de 60 phrases est ciblé, pas aléatoire : il sert au rappel par rôle et au kappa, pas à estimer la prévalence ni une F1 générale.",
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nfrom pathlib import Path\np=Path('tools/protocole_or_roles.py')\ns=p.read_text()\nold='''                    \"supplément de 60 phrases / 90 mentions porte chaque rôle à >= 20 \"\n                    \"et le kappa  … [594 caractères tronqués]`

  ```
patched
Protocole livré : 61 phrases / 144 rôles S se projettent en 117 mentions des sept champs et 27 hors_champ ; avec les 46 textes v2, la base donne 222 mentions, dont 195 dans les sept champs ; le protocole prévoit un supplément de 60 phrases / 90 mentions qui porte chaque rôle à >= 20 et le kappa simulé à 90 % d'accord de 0,857 à 0,878 ; l'or permuté existant tombe à 0/18 sur les cinq rôles de GP et 0,4028 (borne haute) sur tous les rôles.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,14p' reports/rapport-or-roles-protocole.md", "description": "Check report header wrapping"}`

  ```
# J4 — L'or de rôles : sept champs, deux codeurs, 144 rôles S, un or permuté

> **Ligne de roadmap** : **B13 / R0.7** · **Tâche** : X2 (J4 matin, la part du pilote) ·
> **Date** : 2026-11-15 · **Verdict** : protocole livré, **gold S non modifié**
> (SHA-256 `4cebc6d7…f8879` avant et après). Les **61 phrases / 144 rôles** du gold S se
> projettent en **117 mentions des sept champs** et **27 hors_champ** ; avec les **46 textes**
> du gold v2, la base donne **222 mentions** dont **195** dans les sept champs. Les quatre
> rôles rares n'y sont pas mesurables : `temps` 9, `destinataire` 5, `possession` 1,
> `complement` 7. Le protocole prévoit un **supplément de 60 phrases / 90 mentions** qui porte chaque rôle à ≥ 20 ;
> le kappa simulé à 90 % d'accord passe de **0,857** à **0,878**, et l'or permuté existant
> s'effondre à **0/18** sur les cinq rôles de GP. Le protocole est prêt pour S ; le pilote
> n'écrit ni dans le gold S ni dans `tools/structures/`.

**La question.** Le gold v2 (46 textes) n'annote que **trois** rôles (`agent`, `predicat`,
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nfrom pathlib import Path\np=Path('reports/rapport-or-roles-protocole.md')\ns=p.read_text()\nold='''> `complement` 7. Le protocole prévoit un **supplément de 60 phrases / 90 mentions** qui porte chaque rôle à ≥ 20 ; … [767 caractères tronqués]`

  ```
ok
331 reports/rapport-or-roles-protocole.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && set -e\npython3 tools/protocole_or_roles.py >/tmp/final.txt\ncat /tmp/final.txt\npython3 - <<'EOF'\nimport json, jsonschema, hashlib\nschema=json.load(open('reports/schema-or-roles.json'))\njsonschema.Draft202012Validator.check_schem … [956 caractères tronqués]`

  ```
✅ reports/rapport-or-roles-protocole.json
✅ reports/or-roles-base-v1.json (46 textes)
✅ schéma : 46 items, 0 erreur(s)
   gold S : 61 phrases, 144 rôles, 117 dans les 7 champs, 27 hors_champ
   base   : 222 mentions, 195 dans les 7 champs
   kappa  : base 90% -> 0.8572, après supplément -> 0.8778
   or permuté : S cinq {'justes': 0, 'attendus': 18, 'taux': 0.0}, v2 cinq 37/77
BASE 46 SCHEMA ERRORS 0
SCHEMA NEGATIF 4 / 4
GOLD S SHA 4cebc6d75b61db35acd3b2cbfc2a23924b25df3f020dce6038a2730adc2f8879
BASE SHA OK True
SCHEMA SHA OK True
  ✅ 1832 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4577 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-15)
4cebc6d75b61db35acd3b2cbfc2a23924b25df3f020dce6038a2730adc2f8879  tools/structures/donnees/gold-analyseur.json
0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nfrom pathlib import Path\np=Path('reports/rapport-or-roles-protocole.md')\ns=p.read_text()\nold='''conserve (`theme`, `instrument`, `but`, `patient`, `qualite`…). La couche des sept champs est\ncelle du **score** ; … [969 caractères tronqués]`

  ```
ok
334 reports/rapport-or-roles-protocole.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nfrom pathlib import Path\np=Path('reports/rapport-or-roles-protocole.md')\ns=p.read_text().replace('sont enregistrés dans\\n`hors_cadre` avec', 'seront enregistrés dans\\n`hors_cadre` avec')\np.write_text(s)\nprint … [134 caractères tronqués]`

  ```
ok
150:hors des sept champs (`patient`, `qualite`, subordonnées) seront enregistrés dans
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short | grep -E \"or-roles|protocole|schema-or\"; echo \"---\"; ls -l reports/rapport-or-roles-protocole.md reports/rapport-or-roles-protocole.json reports/schema-or-roles.json reports/or-roles-base-v1.json tools/protoco … [239 caractères tronqués]`

  ```
?? reports/or-roles-base-v1.json
?? reports/rapport-or-roles-protocole.json
?? reports/rapport-or-roles-protocole.md
?? reports/schema-or-roles.json
?? tools/protocole_or_roles.py
---
-rw-r--r--. 1 stephane stephane 51057 15 nov 12:52 reports/or-roles-base-v1.json
-rw-r--r--. 1 stephane stephane 38319 15 nov 12:52 reports/rapport-or-roles-protocole.json
-rw-------. 1 stephane stephane 19473 15 nov 12:52 reports/rapport-or-roles-protocole.md
-rw-------. 1 stephane stephane  9316 15 nov 12:45 reports/schema-or-roles.json
-rw-------. 1 stephane stephane 51924 15 nov 12:51 tools/protocole_or_roles.py
---
   334 reports/rapport-or-roles-protocole.md
  1392 reports/rapport-or-roles-protocole.json
   240 reports/schema-or-roles.json
  2220 reports/or-roles-base-v1.json
  1056 tools/protocole_or_roles.py
  5242 total
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && chmod 644 reports/rapport-or-roles-protocole.md reports/rapport-or-roles-protocole.json reports/schema-or-roles.json reports/or-roles-base-v1.json tools/protocole_or_roles.py && ls -l reports/rapport-or-roles-protocole.md reports/sch … [92 caractères tronqués]`

  ```
-rw-r--r--. 1 stephane stephane 19473 15 nov 12:52 reports/rapport-or-roles-protocole.md
-rw-r--r--. 1 stephane stephane  9316 15 nov 12:45 reports/schema-or-roles.json
-rw-r--r--. 1 stephane stephane 51924 15 nov 12:51 tools/protocole_or_roles.py
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -l tools/mesurer_restitution_v3.py tools/roles_gp.py | cat", "description": "Check tool permissions"}`

  ```
-rw-------. 1 stephane stephane 12589 15 nov 11:53 tools/mesurer_restitution_v3.py
-rw-------. 1 stephane stephane 16455 15 nov 11:13 tools/roles_gp.py
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py 2>&1 | tail -8", "description": "Final docs review"}`

  ```
revue de documentation · 756 fiche(s) · 851 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ❌ 2 anomalie(s) :
     · compteurs : en-cours.md dit 755 fichiers, le disque en a 756
     · compteurs : en-cours.md dit 848 JSON, le disque en a 851
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short | head -30", "description": "Final git status"}`

  ```
M docs/pilotage/en-cours.md
 M docs/produit/README.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/plan.json
?? reports/or-roles-base-v1.json
?? reports/rapport-or-roles-protocole.json
?? reports/rapport-or-roles-protocole.md
?? reports/rapport-page-s-mesure.json
?? reports/rapport-page-s-mesure.md
?? reports/rapport-s-paragraphes.md
?? reports/schema-or-roles.json
?? tools/protocole_or_roles.py
?? tools/tests/linguistique/gold_reel_50.py
  ```

### 🤖 Assistant

Livré.

**Fichiers**
- [`reports/rapport-or-roles-protocole.md`](reports/rapport-or-roles-protocole.md) — le protocole, l'inventaire, le kappa, l'or permuté.
- [`reports/rapport-or-roles-protocole.json`](reports/rapport-or-roles-protocole.json) — les mêmes chiffres, SHA-256, simulations et contrôles.
- [`reports/schema-or-roles.json`](reports/schema-or-roles.json) — schéma Draft 2020-12 des records `phrase / cadres / 7 rôles`.
- [`reports/or-roles-base-v1.json`](reports/or-roles-base-v1.json) — la graine des 46 textes v2 (provisoire, **pas un gold**).
- [`tools/protocole_or_roles.py`](tools/protocole_or_roles.py) — script reproductible, lecture seule du gold S.

**Les chiffres**
- Gold S : **61 phrases / 144 rôles / 17 étiquettes** ; **117** se projettent dans les 7 champs, **27** restent `hors_champ` (`patient`, `qualite`, subordonnées).
- Gold v2 : **46 textes / 65 variantes** ; **78 rôles** non vides dans la première variante ; **3/7** champs.
- Base commune : **222 mentions** dont **195** dans les 7 champs ; rôles rares : `temps` 9, `destinataire` 5, `possession` 1, `complement` 7.
- Supplément prévu : **60 phrases / 90 mentions** → **312 mentions** (285 dans les 7 champs + 27 `hors_champ`) ; chaque rôle à **20–29**.
- Kappa simulé à 90 % d'accord : **0,857** [0,802 ; 0,915] sur la base, **0,878** [0,836 ; 0,914] après supplément. À 85 % : **0,786** / **0,818**.
- Contrôles négatifs : gold S cinq rôles **0/18** ; tous rôles **0,4028** (borne haute, à cause de l’alias `predicat`/`prédicat`) ; rôle constant **3/18, F1 0,037** ; gold v2 cinq rôles **0/6** `lieu`, **37/77**, F1 0,5139.
- Schéma : **46 items validés, 0 erreur** ; **4/4** mutations refusées (sans agent, deux principaux, span faux, sans prédicat).

**Gold S intact**
SHA-256 `4cebc6d75b61db35acd3b2cbfc2a23924b25df3f020dce6038a2730adc2f8879` avant et après ; sous-module `tools/structures` propre.

**Validation**
`python3 tools/protocole_or_roles.py` et `--verifier` passent ; `porte-tableaux.sh` passe ; la revue de documentation ne signale que les **2 compteurs** de `en-cours.md` (755 → 756 fiches, 848 → 851 JSON), à mettre à jour par le principal. Les fichiers sont écrits mais non commités.

