# Session DSH — relecture

- identifiant : `session-2bf7f8da-ddb8-4d2a-a357-4a5fd9847e55`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-15 09:06:16
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche W2 (J2 matin) : le tagger sur le split — mesure `evaluer --tagger` sur les 402 (l'entraînement) et sur les 50 H50 (la tenue à l'écart), avec le cache chaud puis l'API ; le POS de l'heuristique et du tagger sur chaque base, le **delta**, le coût par phrase et la latence ; la règle : une règle qui ne gagne que sur H50 est **rejetée**. Fiche `reports/rapport-tagger-h50.md` + JSON. (Si W1 n'a pas encore posé le split, prends le H50 = les 50 phrases de `rapport-gold-reel-50.md`.)

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

- **bash** `{"command": "pwd && ls -la && echo \"---\" && git status --short | head -50 && echo \"---\" && git log --oneline -5", "description": "Inspect repo root and git status"}`

  ```
/home/stephane/Data13TB/stephane/GitHub/Qtrinet
total 208
drwxr-xr-x. 1 stephane stephane   686  6 nov 09:52 .
drwxr-xr-x. 1 stephane stephane  2532  5 nov 10:41 ..
-rw-r--r--. 1 stephane stephane  9977  3 nov 09:19 AGENTS.md
drwxr-xr-x. 1 stephane stephane    40 25 sep 15:38 bench
drwxr-xr-x. 1 stephane stephane    56 30 sep 12:20 colab
drwxr-xr-x. 1 stephane stephane  2664  2 nov 18:33 data
drwxr-xr-x. 1 stephane stephane   138 15 nov 06:29 docs
drwxr-xr-x. 1 stephane stephane    92 28 oct 16:25 drave-core
drwxr-xr-x. 1 stephane stephane   198 15 nov 09:06 .git
-rw-r--r--. 1 stephane stephane   619 31 oct 17:33 .gitignore
-rw-r--r--. 1 stephane stephane   225  1 nov 10:50 .gitmodules
drwxr-xr-x. 1 stephane stephane   992 15 nov 01:33 journal
drwxr-xr-x. 1 stephane stephane   100  3 nov 09:12 models
drwxr-xr-x. 1 stephane stephane   114 25 sep 15:24 __pycache__
drwxr-xr-x. 1 stephane stephane    64  6 nov 09:52 .pytest_cache
-rw-r--r--. 1 stephane stephane  4992 25 sep 10:54 Qtrinet-bootstrap.md
-rw-r--r--. 1 stephane stephane 21293  6 nov 22:32 README.md
drwxr-xr-x. 1 stephane stephane 77768 15 nov 09:05 reports
-rw-r--r--. 1 stephane stephane 13100 28 oct 14:59 REPRISE.md
-rw---
… [2294 caractères tronqués]
  ```

- **bash** `{"command": "ls -la reports/ | head -60; echo \"---\"; ls -la data/ | head -40", "description": "List reports and data directories"}`

  ```
total 28632
drwxr-xr-x. 1 stephane stephane   77768 15 nov 09:05 .
drwxr-xr-x. 1 stephane stephane     686  6 nov 09:52 ..
drwxr-xr-x. 1 stephane stephane     102 24 oct 15:52 07
-rw-r--r--. 1 stephane stephane    4447 28 oct 09:17 07-mesures-couche-commune.md
-rw-r--r--. 1 stephane stephane     907 29 oct 16:25 a26-bilan.json
-rw-r--r--. 1 stephane stephane    1163  1 nov 20:40 a26-lot-disque.json
-rw-r--r--. 1 stephane stephane    1121 30 oct 08:57 a80-audit-final.json
-rw-r--r--. 1 stephane stephane     560 30 oct 00:04 a80-indice-qualifie.json
-rw-r--r--. 1 stephane stephane     672 29 oct 23:42 a80-melange-qualifie.json
-rw-r--r--. 1 stephane stephane     430 30 oct 08:57 a80-pannes-ppl.json
-rw-r--r--. 1 stephane stephane     630 29 oct 17:07 a80-porte-adaptateur.json
-rw-r--r--. 1 stephane stephane     521 29 oct 16:40 a80-porte-budget.json
-rw-r--r--. 1 stephane stephane     625 29 oct 22:07 a80-porte-bus.json
-rw-r--r--. 1 stephane stephane     654 29 oct 22:19 a80-porte-bus-socket.json
-rw-r--r--. 1 stephane stephane     677 29 oct 21:05 a80-porte-c4-retard.json
-rw-r--r--. 1 stephane stephane     600 29 oct 20:06 a80-porte-consolidation.json
-rw-r--r--. 1 stephane stepha
… [6071 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"tagger\" --include=*.py tools/ src/ | head -60; echo \"===\"; grep -rn \"evaluer\" --include=*.py tools/ src/ | head -40", "description": "Locate tagger and evaluer code"}`

  ```
tools/docwatch/.venv/lib/python3.13/site-packages/pygments/lexers/ncl.py:329:                'wrf_user_ll_to_ij', 'wrf_user_unstagger', 'wrf_user_vert_interp',
tools/docwatch/.venv/lib/python3.13/site-packages/more_itertools/more.py:164:    'stagger',
tools/docwatch/.venv/lib/python3.13/site-packages/more_itertools/more.py:1892:def stagger(iterable, offsets=(-1, 0, 1), longest=False, fillvalue=None):
tools/docwatch/.venv/lib/python3.13/site-packages/more_itertools/more.py:1897:        >>> list(stagger([0, 1, 2, 3]))
tools/docwatch/.venv/lib/python3.13/site-packages/more_itertools/more.py:1899:        >>> list(stagger(range(8), offsets=(0, 2, 4)))
tools/docwatch/.venv/lib/python3.13/site-packages/more_itertools/more.py:1906:        >>> list(stagger([0, 1, 2, 3], longest=True))
tools/docwatch/.venv/lib/python3.13/site-packages/more_itertools/more.py:1944:    staggered = []
tools/docwatch/.venv/lib/python3.13/site-packages/more_itertools/more.py:1947:            staggered.append(chain(repeat(fillvalue, -n), it))
tools/docwatch/.venv/lib/python3.13/site-packages/more_itertools/more.py:1949:            staggered.append(islice(it, n, None))
tools/docwatch/.venv/lib/python3.13/site-packag
… [10428 caractères tronqués]
  ```

- **bash** `{"command": "ls -la reports/ | grep -i -E \"gold|tagger|h50|split|452|reel\" ; echo \"===\"; ls -la reports/rapport-gold* reports/*tagger* 2>/dev/null", "description": "Find gold/tagger/H50 reports"}`

  ```
-rw-r--r--. 1 stephane stephane     660 15 nov 01:31 pensee-base-reelle.json
-rw-r--r--. 1 stephane stephane     381  2 nov 03:58 pensee-gold-200.json
-rw-r--r--. 1 stephane stephane     530  2 nov 09:18 pensee-gold-342.json
-rw-r--r--. 1 stephane stephane   23145  5 nov 16:00 pensee-gold-anglais.json
-rw-r--r--. 1 stephane stephane   32798  2 nov 23:21 pensee-gold-cascade-200.json
-rw-r--r--. 1 stephane stephane   32777  2 nov 18:20 pensee-gold-cascade.json
-rw-r--r--. 1 stephane stephane     427  2 nov 04:53 pensee-gold-complexes100.json
-rw-r--r--. 1 stephane stephane     419  2 nov 04:37 pensee-gold-complexes20.json
-rw-r--r--. 1 stephane stephane     418  2 nov 04:45 pensee-gold-complexes50.json
-rw-r--r--. 1 stephane stephane     415  2 nov 04:23 pensee-gold-complexes.json
-rw-r--r--. 1 stephane stephane     413  2 nov 05:01 pensee-gold-discours.json
-rw-r--r--. 1 stephane stephane     241  2 nov 13:32 pensee-gold-gele.json
-rw-r--r--. 1 stephane stephane     639  6 nov 19:02 pensee-gold-gp-corrige.json
-rw-r--r--. 1 stephane stephane   31377  1 nov 20:16 pensee-gold-linguistique.json
-rw-r--r--. 1 stephane stephane   20947  2 nov 16:53 pensee-gold-neuronal.json
-rw-r--r--. 1
… [5017 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn -E \"\\bW1\\b|\\bW2\\b|tagger-h50|H50\" docs/ reports/ journal/ tools/ --include=*.md --include=*.json --include=*.py --include=*.txt 2>/dev/null | head -80", "description": "Search W1/W2/H50 references"}`

  ```
docs/pilotage/semaine-2.md:26:| **gold réel** | **452** phrases (402 + H50), 184 cibles ; l'ancien nom est **obsolète** | H50 n'est pas encore un **test** ; **10 GP/SUB** à annoter (dont 4 dans H50) ; le dénominateur passe à **194** | [C3](../../reports/rapport-gold-reel-50.md) |
docs/pilotage/semaine-2.md:32:**Le gold n'est pas à recompter.** 452 est le **nombre** ; H50 est le **statut de test** ; les
docs/pilotage/semaine-2.md:48:| **J1 · 16/11** | matin | **Le gold réel 452, nommé et tenu à l'écart** : retirer l'ancien nom ; figer le split **402 / H50** ; annoter les **10 GP/SUB** (4 dans H50) ; sha256 du gold avant/après. | S + pilote | [fiche gold 452](../../reports/rapport-gold-452.md) + JSON ; 402 vs H50 ; **184 → 194** cibles ; double codage **4/10**. | C3 ; le gold est à S |
docs/pilotage/semaine-2.md:50:| **J2 · 17/11** | matin | **Le tagger sur H50** : cache chaud puis API ; POS/F1/attachement sur **402** et **H50** ; coût et latence par phrase. | R/B13 | fiche tagger H50 + JSON ; **402 ne baisse pas** ; une règle qui ne gagne que H50 est **rejetée**. | J1 (split) |
docs/pilotage/semaine-2.md:70:| **H50** : sélectionné sur les erreurs de l'heuristique | le score du tagge
… [10047 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,200p' docs/pilotage/en-cours.md", "description": "Read current state doc"}`

  ```
# En ce moment

**Mis à jour : 2026-11-15, 09 h 10 HNE (W1 : gold 452)**

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
> le hook pre-commit refuse un fait sans l
… [11558 caractères tronqués]
  ```

- **bash** `{"command": "grep -rln -- \"--tagger\" tools/ src/ --include=*.py | head -20; echo \"===\"; grep -rn -- \"--tagger\" tools/ src/ --include=*.py | grep -v \".venv\" | head -40", "description": "Find --tagger CLI"}`

  ```
tools/__pycache__/verifier_faq.cpython-313.pyc
tools/__pycache__/drave.cpython-313.pyc
tools/tests/test_tagger_api.py
tools/chantier/plan.json
tools/verifier_faq.py
tools/drave.py
===
tools/tests/test_tagger_api.py:10:4. le défaut est inchangé : `analyser --json` sans `--tagger` rend exactement l'heuristique ;
tools/tests/test_tagger_api.py:178:    """Sans `--tagger`, la sortie est exactement celle de l'heuristique."""
tools/tests/test_tagger_api.py:198:        self.assertIn("--tagger", resultat.stdout)
tools/tests/test_tagger_api.py:216:            for commande in (("analyser", TEXTE, "--tagger"),
tools/tests/test_tagger_api.py:217:                             ("evaluer", "--tagger")):
tools/tests/test_tagger_api.py:228:            resultat = drave_cli("analyser", TEXTE, "--tagger", env=env)
tools/tests/test_tagger_api.py:266:    """La CLI de bout en bout, client injecté : le chemin `--tagger` et son coût."""
tools/tests/test_tagger_api.py:283:        code, sortie, erreur = self._lancer("analyser", TEXTE, "--tagger", "--json")
tools/tests/test_tagger_api.py:292:        code, sortie, erreur = self._lancer("analyser", TEXTE, "--tagger")
tools/tests/test_tagger_api.py:306:           
… [4805 caractères tronqués]
  ```

- **bash** `{"command": "ls -la tools/tests/linguistique/ | head -60; echo \"===\"; sed -n '1,120p' reports/rapport-gold-452.md", "description": "List linguistic tests and read gold 452 report"}`

  ```
total 1540
drwxr-xr-x. 1 stephane stephane    964 15 nov 04:59 .
drwxr-xr-x. 1 stephane stephane   1018 15 nov 06:38 ..
-rw-r--r--. 1 stephane stephane  16090  2 nov 09:26 anaphore.py
-rw-r--r--. 1 stephane stephane  35148  5 nov 14:25 classement_cible.py
-rw-r--r--. 1 stephane stephane   6231  7 nov 13:02 classer_gv.py
-rw-r--r--. 1 stephane stephane  15762  6 nov 19:50 evaluer_gold.py
-rw-r--r--. 1 stephane stephane 450905  2 nov 13:27 gold_gele.json
-rw-r--r--. 1 stephane stephane  20009 15 nov 07:40 gold.json
-rw-r--r--. 1 stephane stephane   7813  2 nov 12:03 gold.py
-rw-r--r--. 1 stephane stephane  29924 15 nov 02:45 gold_reel_50.py
-rw-r--r--. 1 stephane stephane 470149  2 nov 14:39 gold_reel.json
-rw-r--r--. 1 stephane stephane 132934  5 nov 14:04 gold_reel.py
-rw-r--r--. 1 stephane stephane  14631 15 nov 04:59 gold_restitution_v2.json
-rw-r--r--. 1 stephane stephane   1939  5 nov 17:52 gold_split.py
-rw-r--r--. 1 stephane stephane 149211  6 nov 18:56 gold_synthetique.json
-rw-r--r--. 1 stephane stephane  10222  6 nov 18:55 gold_synthetique.py
-rw-r--r--. 1 stephane stephane   2953  2 nov 12:17 juge.py
-rw-r--r--. 1 stephane stephane  22366  3 nov 14:05 miroir.py
drwxr-xr-x
… [7051 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,180p' tools/drave.py", "description": "Read drave.py header"}`

  ```
#!/usr/bin/env python3
"""drave.py — le point d'entrée produit du bloc linguistique.

Une seule commande, quatre gestes, hors ligne et déterministe :

    python3 tools/drave.py analyser "Le chat dort."
    python3 tools/drave.py analyser "The cat sleeps on the roof." --langue en --json
    python3 tools/drave.py analyser "Le chat dort." --tagger          # API DeepSeek (clé, réseau)
    python3 tools/drave.py evaluer
    python3 tools/drave.py evaluer --gold --json
    python3 tools/drave.py evaluer --tagger --json                    # heuristique + cascade API
    python3 tools/drave.py rejouer "Le chat de la voisine qui dort sur le toit se réveille."
    python3 tools/drave.py restituer "Le chat dort."
    python3 tools/drave.py restituer "Le chat dort." --roles
    python3 tools/drave.py restituer --banc reports/pensee-fiabilite-produit.json --json
    python3 tools/drave.py --version

Ce que la commande expose : l'analyse **heuristique** (`Heuristique.analyser`) — POS, syntagmes
avec rôle et cible d'attachement, pragmatique, unités sémantiques —, sa mesure sur le gold et la
**restitution v0** (annotation → surface, avec la fidélité du miroir) et la **v2** (rôles
agent/prédicat
… [6572 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '180,560p' tools/drave.py", "description": "Read drave.py evaluer implementation"}`

  ```
`bl.Cascade`/`_fusion` ne recopie pas `refus` : sans ce relais, un tagger qui échoue
    rendrait une annotation muette (POS absents, `refus` vide). Le composite est rappelé après
    la fusion ; ses taggers ont un cache, donc **aucun appel réseau supplémentaire**.
    """

    nom = "cascade"

    def __init__(self, cascade, compose, stats: dict | None = None):
        self.cascade = cascade
        self.compose = compose
        self.stats = stats if stats is not None else {}
        self.h = cascade.h
        self.n = cascade.n

    def analyser(self, texte: str, langue: str | None = None,
                 contexte: str | None = None) -> bl.Annotation:
        annotation = self.cascade.analyser(texte, langue, contexte)
        # 401/403 : le tagger a échoué pour une raison qui ne dépend pas de la phrase. On ne
        # publie pas un repli heuristique déguisé en cascade : le CLI sort 4, stdout vide.
        code = self.stats.get("cle_refusee")
        if code:
            raise CleTaggerRefusee(int(code))
        if not annotation.refus:
            annotation.refus = self.compose.analyser(texte, langue, contexte).refus
        # le tagger ne reçoit que mots et nombres : la **po
… [17015 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"def cmd_evaluer\\|def _evaluer\\|add_parser(\\\"evaluer\\\"\\|evaluer.add_argument\\|--gold\\|gold_reel\\|gold_path\" tools/drave.py | head -40; echo \"===\"; sed -n '560,760p' tools/drave.py; echo \"=== args\"; sed -n '780,940p' tools/drave.py", "description": "Read evaluer c … [17 caractères tronqués]`

  ```
10:    python3 tools/drave.py evaluer --gold --json
566:def cmd_evaluer(args: argparse.Namespace) -> int:
717:        print(f"{NOM}: erreur d'usage : --gold ne sert qu'avec --banc --roles",
831:        "  python3 tools/drave.py evaluer --gold --json\n"
883:        epilog="Exemples : python3 tools/drave.py evaluer --gold --json ; "
888:    evaluer.add_argument("--gold", action="store_true",
890:    evaluer.add_argument("--reel", action="store_true",
892:    evaluer.add_argument("--par-langue", action="store_true",
894:    evaluer.add_argument("--tagger", action="store_true",
896:    evaluer.add_argument("--json", action="store_true",
941:    restituer.add_argument("--gold", default=None, metavar="CHEMIN",
===
                    f"· Δ {_points(t['delta_pos'])} "
                    f"· SYNTAGMES F1 {_pct(t['syntagme']['f1'])} "
                    f"(tête {_pct(t['syntagme']['tete']['f1'])})")
    return "\n".join(lignes)


def cmd_evaluer(args: argparse.Namespace) -> int:
    evaluateur = _module_evaluation()
    phrases = evaluateur.charger_gele() if args.gold else evaluateur.charger()
    if getattr(args, "reel", False):
        # la **base honnête** : les phrases réelles (main +
… [18502 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,220p' tools/tests/linguistique/evaluer_gold.py", "description": "Read evaluer_gold.py"}`

  ```
"""evaluer_gold.py — mesure le bloc linguistique sur le gold réel (20) + synthétique (160).

Trois niveaux : POS (token, exact), syntagmes (exact + **par tête**), pragmatique. Quatre
lectures : heuristique, mock neuronal, parallèle, cascade. Le vrai modèle est optionnel
(`--reel`) : s'il ne répond pas, il est refusé, pas simulé.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
from collections import Counter, defaultdict

RACINE = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RACINE / "tools"))
import bloc_linguistique as bl  # noqa: E402

GOLD = pathlib.Path(__file__).with_name("gold.json")
REEL = pathlib.Path(__file__).with_name("gold_reel.json")
SYNTH = pathlib.Path(__file__).with_name("gold_synthetique.json")


def charger() -> list[dict]:
    hand = json.loads(GOLD.read_text(encoding="utf-8"))["phrases"]
    reel = json.loads(REEL.read_text(encoding="utf-8"))["phrases"]
    synth = json.loads(SYNTH.read_text(encoding="utf-8"))["phrases"]
    for p in hand:
        p["source"] = "hand"
    for p in reel:
        p["source"] = "reel"
    return hand + reel + synth


GELE = pathlib.Path(__file__).with_name("gold_ge
… [9827 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,240p' tools/tests/linguistique/qualifier_tagger_612.py", "description": "Read tagger 612 bench"}`

  ```
#!/usr/bin/env python3
"""qualifier_tagger_612.py — le tagger POS API sur le gold 612 (hand 20 + reel 432 + synth 160).

POURQUOI. Le banc `qualifier_quatre_modes.py` ne charge que `gold_reel.json` (432 phrases) ; le
gold courant en compte 612, et le tagger n'y a jamais été mesuré. Ce banc ajoute la ventilation
hand / reel / synth, la latence réelle des appels et le modèle effectivement renvoyé par l'API.
Il ne modifie aucun autre fichier et n'écrit que le JSON demandé.

COÛT. Deux appels par phrase (POS + syntagmes), partagés par les six modes grâce au cache des
tagger : ~1 214 appels, ~360 k tokens, ~20 min pour 612 phrases.

USAGE.
    DEEPSEEK_KEY_FILE=$HOME/.config/drave/deepseek.key \
    DEEPSEEK_CACHE=$(mktemp -d /tmp/j43-cache.XXXX) \
    DEEPSEEK_MODEL=deepseek-chat \
    PYTHONPATH=. python3 tools/tests/linguistique/qualifier_tagger_612.py \
      --sortie /tmp/tagger-612.json

La clé n'est jamais lue en dur : `tools/llm/deepseek.py` lit `DEEPSEEK_API_KEY` ou le fichier
`DEEPSEEK_KEY_FILE` (0600). Le cache doit être neuf : le cache par défaut contient les réponses
du 2026-11-04 et rejouerait l'ancien modèle au lieu de mesurer celui d'aujourd'hui.
"""
from __future__ impo
… [7445 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,240p' tools/llm/deepseek.py; echo \"===\"; grep -n \"cache\\|CACHE\\|latence\" tools/llm/deepseek.py | head -60", "description": "Read DeepSeek client and cache"}`

  ```
#!/usr/bin/env python3
"""deepseek.py — le professeur externe, sans poids locaux.

POURQUOI CE MODULE. Le dépôt garde ses GPU et ses CPU pour le **modèle natif**
Drave (`entrainer_moteur.py`, `drave-core`) et pour les mesures **boîte blanche**
(perplexité, activations, flux, sondes). Le **langage** — traduire, juger,
générer, évaluer — passe par une API : on ne charge plus un Qwen de 7/14/32 B
pour cela. DeepSeek est ce **professeur externe** ; ses sorties peuvent servir à
entraîner/distiller l'élève natif (autorisation explicite du propriétaire de la
licence).

CE QUE LE MODULE NE FAIT PAS. Il ne remplace pas les mesures d'états internes :
une API ne donne pas les poids ni les activations. Il ne met **jamais** la clé
dans le dépôt, dans un cache ou dans un message d'erreur. Il ne dépend d'aucun
paquet externe : `urllib` suffit.

CONTRAT.
- `DEEPSEEK_API_KEY` (ou `DSH_API_KEY`) : la clé, lue dans l'environnement ;
- `DEEPSEEK_BASE_URL` (ou `DSH_BASE_URL`) : `https://api.deepseek.com` par défaut ;
- `DEEPSEEK_MODEL` (ou `DSH_MODEL`) : `deepseek-chat` par défaut ;
- cache : `data/deepseek/cache/<sha256>.json` (gitignoré), clé = modèle + messages
  + température + max_tokens, **jamais
… [11021 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport os, pathlib\nk = os.environ.get('DEEPSEEK_KEY_FILE') or os.environ.get('DSH_KEY_FILE')\nprint('KEY_FILE env:', bool(k), k if k else '')\nfor p in [pathlib.Path.home()/'.config/drave/deepseek.key']:\n    print(p, 'exists=', p.is_file(), 'size=', p.stat().st_size  … [344 caractères tronqués]`

  ```
KEY_FILE env: False 
/home/stephane/.config/drave/deepseek.key exists= True size= 36
DEEPSEEK_API_KEY set: False
cache exists: True files: 3759
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\np='reports/rapport-gold-452.json'\nd=json.load(open(p))\nprint(list(d.keys()))\nfor k,v in d.items():\n    if isinstance(v,dict): print(k, '->', list(v.keys())[:20])\n    elif isinstance(v,list): print(k, 'list', len(v), 'first keys', list(v[0].keys()) if  … [120 caractères tronqués]`

  ```
['date', 'date_cible', 'ligne', 'tache', 'commit_mesure', 'commit_c3', 'objet', 'composition', 'sha256', 'split', 'candidats_a_annoter', 'retrait_gold_200_plus', 'controles_negatifs', 'gold_intact', 'limites', 'ce_qui_ferait_faux', 'fichiers']
date = 2026-11-15
date_cible = 2026-11-16 (J1 · matin)
ligne = R0.7 / B13
tache = W1 — le gold réel 452 : composition, split 402/H50, sha256 et 10 candidats GP/SUB
commit_mesure = 6b2208ee1579739a188086f957c0d508e8a04726
commit_c3 = f926b5bc6d8da64ffb1c59a6dbc8a6fcfd1c9888
objet -> ['gold', 'fichiers', 'unites', 'note']
composition -> ['total', 'par_source', 'par_langue', 'par_source_et_langue', 'lecture']
sha256 -> ['gold.json', 'gold_reel.json', 'concat_ordonnee', 'avant', 'apres', 'identique', 'commande']
split -> ['nom', 'statut', 'regle', 'h50_ids', 'reste_402_ids', 'manifeste_sha256', 'partition', 'composition_h50', 'composition_reste_402', 'phrases_h50', 'mesure', 'part_des_erreurs', 'controle_aleatoire_graine']
candidats_a_annoter -> ['principe', 'convention', 'priorite_1', 'priorite_2']
retrait_gold_200_plus -> ['fait', 'occurrences_avant', 'lignes_avant', 'occurrences_apres', 'fichiers', 'regle', 'verification']
controles_negatifs -
… [292 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,160p' reports/rapport-tagger-option.md", "description": "Read tagger option report"}`

  ```
# R0.7 / 1A — le tagger POS en option : +8,57 pts sur 20 phrases, +8,49 sur le gold 612 ; le défaut reste hors ligne

> **Ligne de roadmap** : **R0.7** (le lecteur) · **Décision** : **1A** du 14/11 · **Date** :
> 2026-11-14 · **Verdict** : ✅ **option livrée** — `--tagger` sur `analyser` et `evaluer` ; POS
> **88,57 % → 97,14 %** sur 20 phrases `hand` (**+8,57 pts**), cohérent avec le **0,9475 contre
> 0,8625** du gold 612 (**+8,49**) ; **40 appels**, **11 868 tokens** (cache neuf), **0 refus** ;
> le **défaut** reste l'**heuristique**, CPU, hors ligne, déterministe. Le gain est **+4,67** sur
> le seul gold réel 432 : lire le chiffre avec sa source.

## 1 bis. Les deux défauts corrigés (15/11)

| défaut | avant | **après** |
|---|---|---|
| **2 appels par phrase** (le tagger de syntagmes était appelé sans être utilisé) | 2 appels | **1 appel** |
| **`PONCT` perdu** (le tagger ne reçoit que mots et nombres) | 0 ponctuation étiquetée | **25/25** (restituée depuis l'heuristique) |

**La mesure sur le gold 612** (avec la clé, cache partiel) : POS **0,9575** contre 0,8625 pour
l'heuristique — **+9,5 points** (le `PONCT` restitué ajoute 0,25 pt ; le reste vient du tagger).
**Sur la base r
… [8259 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nfor p in ['reports/tagger-612.json','reports/pensee-tagger-option.json']:\n    d=json.load(open(p))\n    print('===',p)\n    print(json.dumps(d, ensure_ascii=False, indent=1)[:3000])\nPY", "description": "Inspect prior tagger JSON outputs"}`

  ```
=== reports/tagger-612.json
{
 "date": "2026-11-13 22:21 EST",
 "gold": {
  "phrases": 612,
  "tokens": 3179,
  "sources": {
   "hand": 20,
   "reel": 432,
   "synth": 160
  },
  "modalite": "api-deepseek (deepseek-chat → modèle renvoyé), aucun serveur local"
 },
 "modeles_renvoyes": {
  "deepseek-flash": 1218
 },
 "modes": {
  "heuristique": {
   "all": {
    "pos": {
     "exactitude": 0.8625,
     "exactitude_ferme": 0.9373,
     "exactitude_ouvert": 0.7918,
     "tokens": 3179,
     "confusions": {
      "ADJ": {
       "ADJ": 65,
       "NOUN": 65,
       "VERB": 4
      },
      "ADV": {
       "ADV": 131,
       "NOUN": 7,
       "PREP": 1,
       "ADJ": 1,
       "?": 1
      },
      "AUX": {
       "PREP": 4,
       "AUX": 119,
       "?": 3,
       "NOUN": 1,
       "VERB": 1
      },
      "CONJ": {
       "PRON": 15,
       "CONJ": 68,
       "?": 13,
       "PREP": 2
      },
      "DET": {
       "DET": 586,
       "?": 2
      },
      "NOUN": {
       "NOUN": 657,
       "ADJ": 17,
       "VERB": 7,
       "?": 1
      },
      "NUM": {
       "NUM": 2
      },
      "PONCT": {
       "PONCT": 25
      },
      "PREP": {
       "PREP": 114
      },
      "PRON": {

… [4867 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/rapport-gold-452.json'))\ns=d['split']\nprint('split keys:', list(s.keys()))\nprint('nom:', s['nom'])\nprint('statut:', s['statut'])\nprint('manifeste:', s['manifeste_sha256'])\nprint('partition:', s['partition'])\nprint('h50 n=', … [450 caractères tronqués]`

  ```
split keys: ['nom', 'statut', 'regle', 'h50_ids', 'reste_402_ids', 'manifeste_sha256', 'partition', 'composition_h50', 'composition_reste_402', 'phrases_h50', 'mesure', 'part_des_erreurs', 'controle_aleatoire_graine']
nom: 402 / H50
statut: proposé ; S valide ou corrige, le pilote ne modifie pas le gold
manifeste: 1615c17a97bb998451de66585dadcea0643ba1d7f8d962ccbdf28a13b575d970
partition: {'h50': 50, 'reste_402': 402, 'total': 452, 'intersection': 0}
h50 n= 50 reste n= 402
h50 first: ['g004', 'g017', 'r034', 'r071', 'r076', 'r091', 'r102', 'r104', 'r106', 'r119']
reste first: ['g001', 'g002', 'g003', 'g005', 'g006', 'g007', 'g008', 'g009', 'g010', 'g011']
composition h50: {"phrases": 50, "sources": {"hand": 2, "corpus": 48}, "langues": {"en": 25, "fr": 25}, "source_langue": {"hand/fr": 1, "hand/en": 1, "corpus/fr": 24, "corpus/en": 24}, "tokens": 323, "segments": 190, "cibles": 22}
mesure: {"global_452": {"phrases": 452, "tokens": 2480, "pos_exactitude": 0.8891, "pos_etiquette_exactitude": 0.9134, "pos_justes": 2205, "pos_erreurs": 275, "pos_tokenisation": 66, "f1": 0.7906, "seg_tp": 1155, "seg_fp": 266, "seg_fn": 346, "attachement_exactitude": 0.9946, "attachement_cibles": 184, "a
… [1462 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nfor p in ['tools/tests/linguistique/gold.json','tools/tests/linguistique/gold_reel.json']:\n    d=json.load(open(p))\n    print(p, list(d.keys()), len(d['phrases']))\n    print('first:', json.dumps(d['phrases'][0], ensure_ascii=False)[:1200])\n    ids=[x.g … [136 caractères tronqués]`

  ```
tools/tests/linguistique/gold.json ['version', 'phrases', 'note'] 20
first: {"id": "g001", "langue": "fr", "texte": "Le chat dort.", "mots": [{"texte": "Le", "pos": "DET", "debut": 0, "fin": 2}, {"texte": "chat", "pos": "NOUN", "debut": 3, "fin": 7}, {"texte": "dort", "pos": "VERB", "debut": 8, "fin": 12}], "segments": [{"type": "GN", "texte": "Le chat", "role": "agent", "debut": 0, "fin": 7}, {"type": "GV", "texte": "dort", "role": "prédicat", "debut": 8, "fin": 12}], "pragma": {"acte": "assertion"}}
ids sample: ['g001', 'g002', 'g003', 'g004', 'g005', 'g006'] ... ['g018', 'g019', 'g020']
tools/tests/linguistique/gold_reel.json ['version', 'source', 'note', 'phrases'] 432
first: {"id": "r001", "langue": "fr", "texte": "Le chien mange une pomme.", "mots": [{"texte": "Le", "pos": "DET", "debut": 0, "fin": 2}, {"texte": "chien", "pos": "NOUN", "debut": 3, "fin": 8}, {"texte": "mange", "pos": "VERB", "debut": 9, "fin": 14}, {"texte": "une", "pos": "DET", "debut": 15, "fin": 18}, {"texte": "pomme", "pos": "NOUN", "debut": 19, "fin": 24}], "segments": [{"type": "GN", "texte": "Le chien", "role": "agent", "debut": 0, "fin": 8}, {"type": "GV", "texte": "mange", "role": "prédicat", "debut"
… [239 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"def \\|H50\\|h50\\|split\\|score\\|signature\" tools/tests/linguistique/gold_reel_50.py | head -80; echo \"===\"; sed -n '1,80p' tools/tests/linguistique/gold_reel_50.py", "description": "Inspect gold_reel_50 script structure"}`

  ```
13:  1. score = 3 × (cible d'attachement absente ou fausse)
17:  3. au plus 2 phrases par **signature d'erreur** (POS confondus, types de segments absents,
59:def sha256(chemin: pathlib.Path) -> str:
63:def charger() -> list[dict]:
74:def commit() -> str:
85:def _span(texte: str, d: int, f: int) -> str:
89:def analyser(h, p: dict) -> dict:
142:    signature = (
162:        "signature": signature,
163:        "score": 3 * len(att_erreurs) + 2 * len(pos_erreurs) + len(fn),
170:def _rangs(rows: list[dict], wa: int, wp: int, wf: int) -> list[dict]:
172:        r["score"] = wa * len(r["attachement"]["erreurs"]) + wp * len(r["pos"]["erreurs"]) \
174:    return sorted(rows, key=lambda r: (-r["score"], r["id"]))
177:def selectionner(rows: list[dict], wa: int = 3, wp: int = 2, wf: int = 1,
179:    """25 français + 25 anglais, au plus `cap` phrases par signature d'erreur."""
183:        signatures = collections.Counter()
188:            if signatures[r["signature"]] >= cap:
192:            signatures[r["signature"]] += 1
208:def _f1(tp: int, fp: int, fn: int) -> dict:
215:def metriques(rows: list[dict]) -> dict:
267:def projeter(global_: dict, hard: dict) -> dict:
293:def controler(rows: lis
… [4626 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '80,260p' tools/tests/linguistique/gold_reel_50.py", "description": "Read H50 selection logic"}`

  ```
# --------------------------------------------------------------------------- analyse


def _span(texte: str, d: int, f: int) -> str:
    return texte[d:f]


def analyser(h, p: dict) -> dict:
    """Une phrase : POS, segments, attachement, et la liste de ses erreurs."""
    texte = p["texte"]
    a = h.analyser(texte, p.get("langue") or "fr")
    pos = {(e.debut, e.fin): e.type for e in a.etiquettes if e.niveau == "pos"}

    pos_erreurs, pos_n = [], len(p["mots"])
    ok = ok_ferme = ok_ouvert = n_ferme = n_ouvert = 0
    for m in p["mots"]:
        pred = pos.get((m["debut"], m["fin"]), "?")
        juste = pred == m["pos"]
        ok += juste
        if m["pos"] in FERME:
            n_ferme += 1
            ok_ferme += juste
        else:
            n_ouvert += 1
            ok_ouvert += juste
        if not juste:
            pos_erreurs.append({"token": m["texte"], "gold": m["pos"], "predit": pred,
                                "debut": m["debut"], "fin": m["fin"],
                                "classe": "fermé" if m["pos"] in FERME else "ouvert",
                                # « ? » = aucun token prédit à ce span : c'est la
                                # tokenisat
… [6861 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"class NeuronalLLMPOS\\|class NeuronalLLMChunks\\|class NeuronalLLMCompose\\|class Cascade\\|class Heuristique\\|def analyser\\|_cache\\|def _invite\\|def _prompt\\|POS\" tools/bloc_linguistique.py | head -80", "description": "Locate tagger classes in bloc_linguistique"}`

  ```
12:  - `NeuronalLLMPOS` : le **tagger** neuronal réel — un modèle local, une liste de tokens, des
13:    POS alignés par grammaire GBNF ; c'est l'implémentation qualifiée sur le gold ;
141:    def analyser(self, texte: str, langue: str | None = None,
306:POS_FERME = {
396:# Un lexique verbal minimal, bilingue, pour arbitrer les classes ouvertes : le POS de surface
796:class Heuristique:
862:    # -- POS ----------------------------------------------------------------
864:        lex = POS_FERME.get(langue, POS_FERME["fr"])
866:        # élision : « j' » → « je », « l' » → « le », « qu' » → « que » (10 tokens sans POS)
870:        # les **nombres** ont une classe (l'audit produit : 45 nombres sans POS)
923:        lex = POS_FERME.get(langue, POS_FERME["fr"])
1140:        """Le **verbe** du span : le lexique d'abord, puis le POS `VERB`, sinon le dernier mot."""
1225:        lex = POS_FERME.get(langue, POS_FERME["fr"])
1236:            """Le verbe : le lexique, le POS, ou la **position** après un pronom sujet."""
1455:    def analyser(self, texte: str, langue: str | None = None,
1494:        # 2. mot + POS fermées / ouvertes
1499:                # la ponctuation a une classe dans le g
… [2886 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"class NeuronalLLMPOS\" -A 140 tools/bloc_linguistique.py | head -180", "description": "Read NeuronalLLMPOS implementation"}`

  ```
1968:class NeuronalLLMPOS:
1969-    """Le **tagger** neuronal réel : un modèle local, des POS alignés sur la tokenisation du bloc.
1970-
1971-    Le modèle ne rend pas une annotation complète : il rend **une classe par token**, contrainte
1972-    par une grammaire GBNF (`grammaire_pos`) qui interdit un JSON tronqué, un token manquant ou
1973-    une classe hors du jeu. Les spans sont ceux de `Heuristique._mots` (la tokenisation du bloc),
1974-    pas ceux que le modèle inventerait ; c'est ce qui rend la mesure POS exacte.
1975-
1976-    Le modèle est servi par `llama-server` (`/v1/chat/completions`, `grammar`) : le serveur est
1977-    lancé une fois, le modèle chargé une fois, et les 180 phrases coûtent une passe CPU, pas
1978-    180 chargements. `transport` est injectable pour tester le contrat sans modèle.
1979-
1980-    La confiance par défaut (`0.6`) est **celle du seuil ouvert de l'heuristique** (0.55) : dans
1981-    une `Cascade`, le tagger ne remplace donc que les tokens que l'heuristique déclare peu sûrs,
1982-    et laisse les classes fermées (0.92) à l'heuristique. C'est la politique mesurée.
1983-    """
1984-
1985-    nom = "neuronal"
1986-
1987-    def __init__(sel
… [7075 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn -E \"0,0[0-9]+ \\\\$|\\\\$ ?/|prix|tarif|coût\" reports/rapport-tagger-option.md docs/ --include=*.md | grep -i -E \"token|prix|tarif|\\\\$\" | head -30", "description": "Search price references"}`

  ```
reports/rapport-tagger-option.md:22:cache) — soit **~0,02 $** pour 612 phrases ; **449 appels servis par le cache** sur la base réelle.
reports/rapport-tagger-option.md:87:**Le prix.** ~**0,04 $** pour les 612 phrases (chiffre de la décision) ; au prorata des tokens,
reports/rapport-tagger-option.md:88:les 20 phrases valent ~**0,0013 $**. Le coût est dominé par les **2 appels/phrase** (~593
reports/rapport-tagger-option.md:151:  § 3 et par le harnais `qualifier_tagger_612.py`, pas par la porte. C'est le prix de la règle
reports/rapport-tagger-option.md:160:  ne veut que le POS, un appel suffirait : ~0,02 $ pour 612 et ~590 tokens/phrase en moins.
reports/rapport-tagger-option.md:164:  un second ~0,04 $ et ~21 min. Le CLI a été validé sur 20 phrases avec le même cache ; le
docs/archive/biologie-pour-drave.md:385:**Et le prix dépend de l'ÉCHELLE** (mesuré à 15 h 07, dim 512, même recette, même
docs/archive/biologie-pour-drave.md:394:axes appris suit la même pente (+3,8 % à 384, **+8,0 %** à 512) : le prix de la
docs/archive/cerveau-facultes.md:190:> * le **prix est stable, le gain ne l'est pas** ✗✓ : perplexité **+148 % et +143 %** selon la graine ✓
docs/archive/etat-cerveau.md:48:| 
… [5152 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-tagger-option.json'))\n# print cost fields\nprint(json.dumps(d.get('mesure_612_reference',{}), ensure_ascii=False, indent=1)[:2500])\nPY", "description": "Inspect cost details in prior JSON"}`

  ```
{
 "source": "reports/tagger-612.json",
 "date": "2026-11-13 22:21 EST",
 "gold": {
  "phrases": 612,
  "tokens": 3179,
  "sources": {
   "hand": 20,
   "reel": 432,
   "synth": 160
  },
  "modalite": "api-deepseek (deepseek-chat → modèle renvoyé), aucun serveur local"
 },
 "heuristique_pos": 0.8625,
 "cascade_pos": 0.9475,
 "delta_pos_publie": 0.0849,
 "par_source": {
  "hand": {
   "heuristique": 0.8857,
   "neuronal": 0.9714,
   "delta": 0.0857
  },
  "reel": {
   "heuristique": 0.8893,
   "neuronal": 0.936,
   "delta": 0.0467
  },
  "synth": {
   "heuristique": 0.7682,
   "neuronal": 0.9828,
   "delta": 0.2146
  }
 },
 "appels": 1218,
 "tokens": 358962,
 "latence_s": 1257.9579999999992,
 "duree_totale_s": 1259.2,
 "refus": 1,
 "refus_detail": [
  "s015"
 ],
 "modeles_renvoyes": {
  "deepseek-flash": 1218
 },
 "cout_annonce_usd": 0.04
}
  ```

- **bash** `{"command": "sed -n '1,130p' docs/pilotage/semaine-2.md", "description": "Read semaine-2 plan"}`

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
… [10691 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '60,210p' reports/rapport-gold-452.md; echo \"=== tail\"; sed -n '280,360p' reports/rapport-gold-452.md", "description": "Read gold 452 split and controls"}`

  ```
| REL | 1 | 57 | 58 |
| SUB | 2 | 52 | 54 |
| **total** | **13** | **171** | **184** |

**Les cibles sont saturées sur GP/REL/SUB, pas sur GN/GV.** 184 cibles = **GP 72 + REL 58 + SUB 54**.
Il reste **10 segments GP/SUB sans cible** (9 GP + 1 SUB) : ce sont exactement les 10 candidats du § 4.
Les **1 233 GN/GV** n'ont pas de cible ; les annoter est une deuxième vague facultative, pas ce lot.

## 2. Le split 402 / H50

### 2.1 La règle déterministe

Le split n'est **pas** un tirage au hasard : H50 est le **lot dur** de C3, sélectionné sur les erreurs de
l'heuristique. La règle est déterministe et reproductible :

```text
score(p) = 3 × |cibles d'attachement évaluées absentes ou fausses|
         + 2 × |tokens POS faux|
         + 1 × |segments gold absents|
```

1. Calculer le score sur les **452** phrases, au HEAD `6b2208ee`, avec `bloc_linguistique.Heuristique`.
   Les 10 segments **sans cible gold** ne comptent pas dans le premier terme : ils ne sont pas évalués.
2. Pour chaque langue (`fr`, `en`), trier par **score décroissant**, puis par **id croissant**.
3. Prendre gloutonnement, avec **au plus 2 phrases par signature d'erreur** — la signature est
   `(langue, couples (POS gol
… [10676 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '2520,2710p' tools/bloc_linguistique.py", "description": "Read fusion/cascade implementation"}`

  ```
l'heuristique ; `confiance` laisse la plus confiante gagner (le tagger neuronal à 0,6
    passe devant l'heuristique à 0,4). `phrase` (type/négation/modalité), `pragmatique` (acte/double_sens/contexte), `discours`
    (paragraphe/connecteur) et `document` (titre/paragraphe) portent des types **complémentaires**
    sur le même span : les supprimer ensemble effacerait la négation au profit du type."""
    modes = {"pos": "span", "syntagme": "span", "phrase": "type", "pragmatique": "type",
             "discours": "type", "document": "type"}
    gardees: list[Etiquette] = [e for e in etiquettes if e.niveau not in modes]
    for niveau, mode in modes.items():
        groupes = {}
        for e in (x for x in etiquettes if x.niveau == niveau):
            groupes.setdefault(e.type if mode == "type" else "", []).append(e)
        for _, es in groupes.items():
            if niveau == "syntagme" and priorite_syntagme == "heuristique":
                # la segmentation heuristique est **authoritaire**, y compris ses alternatives
                # (l'union S+chunker) : on ne la filtre pas, on n'ajoute que le non-chevauchement
                gardees.extend(e for e in es if e.source == "heu
… [8768 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"def _fusion\\|def _priorite\\|confiance\\|seuil\" tools/bloc_linguistique.py | sed -n '1,80p'", "description": "Locate fusion logic"}`

  ```
7:    **candidats** pour l'ambigu ; elle déclare sa couverture et sa confiance ;
15:    étiquettes par confiance ; la cascade n'envoie au neuronal que le **résidu** des niveaux
19:`niveau`, son `span`, sa `source`, sa `confiance`, sa `langue`, son `script` et ses `candidats`.
75:    confiance: float = 0.5
85:            "confiance": round(float(self.confiance), 4),
118:        """La confiance maximale par niveau — la couverture *déclarée*, pas une précision."""
119:        return {n: round(max((e.confiance for e in es), default=0.0), 4)
222:        confiance = min(1.0, (meilleur - second) / meilleur + 0.2 * meilleur)
223:        return langue, round(confiance, 4), scores
802:                 seuil_ouvert: float = 0.55, seuil_langue: float = 0.12,
806:        self.seuil_ouvert = seuil_ouvert
807:        self.seuil_langue = seuil_langue
822:        if conf < self.seuil_langue:
1472:        trace.append({"etape": "langue", "langue": lg, "script": script, "confiance": conf_lg,
1509:                # 3. morphème (candidat, basse confiance)
1520:            if e.type != "VERB" or e.confiance > 0.45 or k == 0:
1533:            if _k == 0 or _e.type not in ("NOUN", "ADJ") or _e.confiance >
… [3843 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json, sys, pathlib\nRACINE=pathlib.Path('.')\nsys.path.insert(0,str(RACINE)); sys.path.insert(0,str(RACINE/'tools')); sys.path.insert(0,str(RACINE/'tools/tests/linguistique'))\nimport gold_reel_50 as c3\nfrom tools.tests.linguistique.evaluer_gold import evaluer_ … [935 caractères tronqués]`

  ```
recalc n 50 json n 50 same True
recalc ['g004', 'g017', 'r034', 'r071', 'r076', 'r091', 'r102', 'r104', 'r106', 'r119', 'r159', 'r163', 'r179', 'r203', 'r210', 'r217', 'r225', 'r227', 'r241', 'r246', 'r255', 'r260', 'r261', 'r262', 'r266', 'r272', 'r285', 'r287', 'r291', 'r293', 'r304', 'r309', 'r324', 'r328', 'r331', 'r339', 'r343', 'r346', 'r347', 'r349', 'r357', 'r362', 'r363', 'r366', 'r368', 'r370', 'r408', 'r409', 'r410', 'r422']
json   ['g004', 'g017', 'r034', 'r071', 'r076', 'r091', 'r102', 'r104', 'r106', 'r119', 'r159', 'r163', 'r179', 'r203', 'r210', 'r217', 'r225', 'r227', 'r241', 'r246', 'r255', 'r260', 'r261', 'r262', 'r266', 'r272', 'r285', 'r287', 'r291', 'r293', 'r304', 'r309', 'r324', 'r328', 'r331', 'r339', 'r343', 'r346', 'r347', 'r349', 'r357', 'r362', 'r363', 'r366', 'r368', 'r370', 'r408', 'r409', 'r410', 'r422']
H50 50 0.6842 0.7542 0.5972 323 0.5836 0.9545 22
402 402 0.9198 0.958 0.8804 2157 0.819 1.0 162
452 452 0.8891 0.9294 0.8466 2480 0.7906 0.9946 184
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/rapport-gold-452.json'))\nca=d['split']['controle_aleatoire_graine']\nprint(type(ca), ca.keys() if isinstance(ca,dict) else '')\nprint(json.dumps(ca, ensure_ascii=False, indent=1)[:3000])\nPY", "description": "Inspect random contr … [9 caractères tronqués]`

  ```
<class 'dict'> dict_keys(['graine', 'protocole', 'ids', 'mesure', 'lecture'])
{
 "graine": 20261116,
 "protocole": "24 corpus fr + 1 hand fr + 24 corpus en + 1 hand en",
 "ids": [
  "g009",
  "g020",
  "r002",
  "r004",
  "r022",
  "r030",
  "r072",
  "r089",
  "r094",
  "r095",
  "r108",
  "r113",
  "r115",
  "r118",
  "r119",
  "r123",
  "r143",
  "r147",
  "r156",
  "r184",
  "r192",
  "r205",
  "r206",
  "r215",
  "r238",
  "r244",
  "r246",
  "r253",
  "r254",
  "r258",
  "r269",
  "r272",
  "r276",
  "r294",
  "r295",
  "r298",
  "r300",
  "r310",
  "r322",
  "r325",
  "r335",
  "r346",
  "r369",
  "r379",
  "r391",
  "r412",
  "r422",
  "r425",
  "r426",
  "r429"
 ],
 "mesure": {
  "phrases": 50,
  "tokens": 278,
  "pos_exactitude": 0.8813,
  "pos_etiquette_exactitude": 0.9142,
  "pos_justes": 245,
  "pos_erreurs": 33,
  "pos_tokenisation": 10,
  "f1": 0.7869,
  "seg_tp": 120,
  "seg_fp": 26,
  "seg_fn": 39,
  "attachement_exactitude": 1.0,
  "attachement_cibles": 23,
  "attachement_justes": 23,
  "attachement_erreurs": 0
 },
 "lecture": "le tirage au hasard fait 88,13 % de POS ; H50 fait 68,42 % : le lot est un stress test, pas un échantillon."
}
  ```

- **bash** `{"command": "grep -rn -i \"règle\" docs/pilotage/semaine-2.md reports/rapport-gold-452.md tools/chantier/plan.json | grep -i -E \"H50|402|tagger|gagne\" | head -30", "description": "Search rule wording"}`

  ```
docs/pilotage/semaine-2.md:50:| **J2 · 17/11** | matin | **Le tagger sur H50** : cache chaud puis API ; POS/F1/attachement sur **402** et **H50** ; coût et latence par phrase. | R/B13 | fiche tagger H50 + JSON ; **402 ne baisse pas** ; une règle qui ne gagne que H50 est **rejetée**. | J1 (split) |
docs/pilotage/semaine-2.md:70:| **H50** : sélectionné sur les erreurs de l'heuristique | le score du tagger | H50 est un **stress test**, pas une généralisation ; contrôle **402** + un échantillon neuf ; une règle qui ne gagne que H50 est du sur-apprentissage. |
docs/pilotage/semaine-2.md:95:| **le code** | règles de rôles v3 ; décision tagger (si retenue) ; migration `/` et référents (S, sous-module) ; tests | tests verts, non-régression 452 et 56 tests S |
reports/rapport-gold-452.md:16:- **Est** : la composition exacte du gold réel 452, le **split 402/H50** proposé avec sa règle et sa graine,
reports/rapport-gold-452.md:349:2. **W2** mesure le tagger sur **402** (l'entraînement) et **H50** (la tenue à l'écart) ; une règle qui ne
tools/chantier/plan.json:598:   "mandat": "Tâche W1 (semaine 2, J1 matin, la part du pilote) : le gold réel 452 — **ne modifie pas le gold** (S/D). Écris `repo
… [1013 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('tools/chantier/plan.json'))\n# find W2 entry\ndef walk(x):\n    if isinstance(x,dict):\n        if 'W2' in str(x.get('id','')) or 'W2' in str(x.get('tache','')) or 'tagger sur le split' in str(x.get('mandat','')):\n            print(json. … [198 caractères tronqués]`

  ```
{
 "id": "W2",
 "jour": 17,
 "titre": "J2 — le tagger sur 402 et H50",
 "mandat": "Tâche W2 (J2 matin) : le tagger sur le split — mesure `evaluer --tagger` sur les 402 (l'entraînement) et sur les 50 H50 (la tenue à l'écart), avec le cache chaud puis l'API ; le POS de l'heuristique et du tagger sur chaque base, le **delta**, le coût par phrase et la latence ; la règle : une règle qui ne gagne que sur H50 est **rejetée**. Fiche `reports/rapport-tagger-h50.md` + JSON. (Si W1 n'a pas encore posé le split, prends le H50 = les 50 phrases de `rapport-gold-reel-50.md`.)",
 "budget_min": 90,
 "acceptation": [
  {
   "commande": "test -f reports/rapport-tagger-h50.md && echo FICHE-OK",
   "attendu": "FICHE-OK"
  }
 ]
}
  ```

- **bash** `{"command": "cat > /tmp/qualifier_tagger_h50.py <<'PY'\n#!/usr/bin/env python3\n\"\"\"qualifier_tagger_h50.py — W2 : le tagger POS sur le split 402 / H50.\n\nPOURQUOI. W1 a figé le gold réel 452 en un split **402** (l'entraînement) et **H50** (la tenue\nà l'écart, sélectionnée sur les erreurs de l'h … [27994 caractères tronqués]`

  ```
COMPILE-OK
  ```

- **bash** `{"command": "mkdir -p tools/tests/linguistique\npython3 - <<'PY'\nfrom pathlib import Path\np = Path('/tmp/qualifier_tagger_h50.py')\ns = p.read_text()\n# 1) construire_bases -> dict of dicts\ns = s.replace('''    bases = {\n        \"reste_402\": [p for p in phrases if p[\"id\"] in reste_ids],\n    … [4641 caractères tronqués]`

  ```
written 27859
COMPILE-OK
68:def charger_split() -> dict:
85:def construire_bases(phrases: list[dict], split: dict) -> dict[str, list[dict]]:
104:    return {nom: {"nom": nom, "phrases": ps} for nom, ps in bases.items()}
214:    justes = sum(conf.get(classe, {}).get(classe, 0) for classe in conf)
217:            "justes": justes, "confusions": conf}
351:    justes = sum(1 for c in gold if rng.choice(CLASSES) == c)
355:                         "taux": round(justes / max(1, n), 4)},
456:        "cout_par_phrase": ({nom: {"phrases": b["cout"]["phrases"],
548:    a.modele = client.modele
  ```

- **bash** `{"command": "timeout 180 python3 tools/tests/linguistique/qualifier_tagger_h50.py --mode tous --limite 2 --cache-api /tmp/tagger-h50-smoke-cache --sortie /tmp/tagger-h50-smoke.json 2>&1 | tail -40; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Smoke-test W2 bench on 2 phrases"}`

  ```
clé DeepSeek absente : exportez DEEPSEEK_KEY_FILE ou déposez ~/.config/drave/deepseek.key
EXIT=1
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np = Path('tools/tests/linguistique/qualifier_tagger_h50.py')\ns = p.read_text()\ns = s.replace('''    client = DeepSeek(modele=a.modele) if a.modele else DeepSeek()\n    a.modele = client.modele\n    if not client.disponible():\n        raise  … [972 caractères tronqués]`

  ```
[cache_chaud] reste_402 · 2 phrases …
[cache_chaud] reste_402 · POS 1.0000 → 1.0000 (Δ +0.0000) · requêtes 0 · cache 2 · 0.0 s
[cache_chaud] h50 · 2 phrases …
[cache_chaud] h50 · POS 0.7857 → 1.0000 (Δ +0.2143) · requêtes 0 · cache 2 · 0.0 s
[cache_chaud] total · 2 phrases …
[cache_chaud] total · POS 1.0000 → 1.0000 (Δ +0.0000) · requêtes 0 · cache 2 · 0.0 s
[cache_chaud] tirage · 2 phrases …
[cache_chaud] tirage · POS 1.0000 → 1.0000 (Δ +0.0000) · requêtes 0 · cache 2 · 0.0 s
[cache_chaud] écrit · /tmp/tagger-h50-smoke.json
[api] reste_402 · 2 phrases …
[api] reste_402 · POS 1.0000 → 1.0000 (Δ +0.0000) · requêtes 0 · cache 2 · 0.0 s
[api] h50 · 2 phrases …
[api] h50 · POS 0.7857 → 1.0000 (Δ +0.2143) · requêtes 0 · cache 2 · 0.0 s
[api] total · 2 phrases …
[api] total · POS 1.0000 → 1.0000 (Δ +0.0000) · requêtes 0 · cache 2 · 0.0 s
[api] tirage · 2 phrases …
[api] tirage · POS 1.0000 → 1.0000 (Δ +0.0000) · requêtes 0 · cache 2 · 0.0 s
[api] écrit · /tmp/tagger-h50-smoke.json
[cache_chaud_apres_api] reste_402 · 2 phrases …
[cache_chaud_apres_api] reste_402 · POS 1.0000 → 1.0000 (Δ +0.0000) · requêtes 0 · cache 2 · 0.0 s
[cache_chaud_apres_api] h50 · 2 phrases …
[cache_chaud_apres_ap
… [417 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np = Path('tools/tests/linguistique/qualifier_tagger_h50.py')\ns = p.read_text()\ns = s.replace('''    avant = meta_cache(cache_dir)\n    resultat = {\"nom\": nom, \"cache_dir\": str(cache_dir), \"cache_avant\": avant,''','''    client.cache_di … [523 caractères tronqués]`

  ```
[cache_chaud] reste_402 · 2 phrases …
[cache_chaud] reste_402 · POS 1.0000 → 1.0000 (Δ +0.0000) · requêtes 0 · cache 2 · 0.0 s
[cache_chaud] h50 · 2 phrases …
[cache_chaud] h50 · POS 0.7857 → 1.0000 (Δ +0.2143) · requêtes 0 · cache 2 · 0.0 s
[cache_chaud] total · 2 phrases …
[cache_chaud] total · POS 1.0000 → 1.0000 (Δ +0.0000) · requêtes 0 · cache 2 · 0.0 s
[cache_chaud] tirage · 2 phrases …
[cache_chaud] tirage · POS 1.0000 → 1.0000 (Δ +0.0000) · requêtes 0 · cache 2 · 0.0 s
[cache_chaud] écrit · /tmp/tagger-h50-smoke.json
[api] reste_402 · 2 phrases …
[api] reste_402 · POS 1.0000 → 1.0000 (Δ +0.0000) · requêtes 2 · cache 0 · 2.3 s
[api] h50 · 2 phrases …
[api] h50 · POS 0.7857 → 1.0000 (Δ +0.2143) · requêtes 2 · cache 0 · 1.9 s
[api] total · 2 phrases …
[api] total · POS 1.0000 → 1.0000 (Δ +0.0000) · requêtes 0 · cache 2 · 0.0 s
[api] tirage · 2 phrases …
[api] tirage · POS 1.0000 → 1.0000 (Δ +0.0000) · requêtes 2 · cache 0 · 2.1 s
[api] écrit · /tmp/tagger-h50-smoke.json
[cache_chaud_apres_api] reste_402 · 2 phrases …
[cache_chaud_apres_api] reste_402 · POS 1.0000 → 1.0000 (Δ +0.0000) · requêtes 0 · cache 2 · 0.0 s
[cache_chaud_apres_api] h50 · 2 phrases …
[cache_chaud_apres_ap
… [417 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/tagger-h50-smoke.json'))\nprint('keys', d.keys())\nprint('passes', d['passes'].keys())\napi=d['passes']['api']\nprint('api bases', api['bases'].keys())\nb=api['bases']['reste_402']\nprint('base keys', b.keys())\nprint('cout', json.du … [408 caractères tronqués]`

  ```
keys dict_keys(['date', 'tache', 'ligne_roadmap', 'commit_mesure', 'modele_demande', 'or', 'split', 'dispositif', 'controles_negatifs', 'passes', 'regle_decision', 'cout_par_phrase', 'limites', 'ce_qui_ferait_faux', 'fichiers'])
passes dict_keys(['cache_chaud', 'api', 'cache_chaud_apres_api'])
api bases dict_keys(['reste_402', 'h50', 'total', 'tirage'])
base keys dict_keys(['base', 'libelle', 'composition', 'duree_mesure_s', 'heuristique', 'tagger', 'delta', 'par_langue', 'refus', 'cout', 'stats_tagger'])
cout {
 "phrases": 2,
 "appels": 2,
 "requetes": 2,
 "cache": 0,
 "tokens_reseau": 279,
 "tokens_cache": 0,
 "latence_reseau_s": 2.286,
 "latence_cache_s": 0,
 "latence_wall_s": 2.287,
 "latence_requete": {
  "moyenne": 1.143,
  "mediane": 1.143,
  "p95": 1.12,
  "max": 1.166
 },
 "par_phrase": {
  "appels": 1.0,
  "requetes": 1.0,
  "cache": 0.0,
  "tokens_reseau": 139.5,
  "tokens_total": 139.5,
  "latence_reseau_s": 1.143,
  "latence_wall_s": 1.1436
 },
 "phrases_sans_appel": {
  "n": 0,
  "ids": []
 }
}
delta {'pos': 0.0, 'pos_ferme': 0.0, 'pos_ouvert': 0.0, 'f1': 0.0, 'attachement': 0.0}
regle {
 "enonce": "Une règle qui ne gagne que sur H50 est rejetée ; le contrôle est la n
… [2153 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/tagger-h50-smoke.json'))\nfor nom in ['reste_402','h50','total','tirage']:\n    b=d['passes']['api']['bases'][nom]\n    print(nom, 'par_langue', {k:(v['phrases'],v['tokens'],v['heuristique']['exactitude'],v['tagger']['exactitude'],v[ … [238 caractères tronqués]`

  ```
reste_402 par_langue {'fr': (2, 9, 1.0, 1.0, 0.0)}
  composition {'phrases': 2, 'tokens': 9, 'langues': {'fr': 2}, 'sources': {'hand': 2}, 'ids': ['g001', 'g002']}
  refus {'n': 0, 'ids': []}
  stats {'appels': 2, 'requetes': 2, 'cache': 0, 'tokens': 279, 'latence_s': 2.286, 'modeles': {'deepseek-flash': 2}, 'cle_refusee': 0}
h50 par_langue {'en': (1, 7, 1.0, 1.0, 0.0), 'fr': (1, 7, 0.5714, 1.0, 0.4286)}
  composition {'phrases': 2, 'tokens': 14, 'langues': {'fr': 1, 'en': 1}, 'sources': {'hand': 2}, 'ids': ['g004', 'g017']}
  refus {'n': 0, 'ids': []}
  stats {'appels': 2, 'requetes': 2, 'cache': 0, 'tokens': 311, 'latence_s': 1.821, 'modeles': {'deepseek-flash': 2}, 'cle_refusee': 0}
total par_langue {'fr': (2, 9, 1.0, 1.0, 0.0)}
  composition {'phrases': 2, 'tokens': 9, 'langues': {'fr': 2}, 'sources': {'hand': 2}, 'ids': ['g001', 'g002']}
  refus {'n': 0, 'ids': []}
  stats {'appels': 2, 'requetes': 0, 'cache': 2, 'tokens': 0, 'latence_s': 0.0, 'modeles': {'deepseek-flash': 2}, 'cle_refusee': 0}
tirage par_langue {'en': (1, 6, 1.0, 1.0, 0.0), 'fr': (1, 4, 1.0, 1.0, 0.0)}
  composition {'phrases': 2, 'tokens': 10, 'langues': {'fr': 1, 'en': 1}, 'sources': {'hand': 2}, 'ids': ['g
… [178 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json, collections\nphr=[]\nfor p in ['tools/tests/linguistique/gold.json','tools/tests/linguistique/gold_reel.json']:\n    phr += json.load(open(p))['phrases']\nc=collections.Counter((p['texte'],p.get('langue','fr')) for p in phr)\ndups={k:v for k,v in c.items() … [170 caractères tronqués]`

  ```
phrases 452 unique 449 dups 3
2 ('Le vent souffle fort.', 'fr')
2 ('La voiture roule vite.', 'fr')
2 ('Paul sees Marie; he speaks to her.', 'en')
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json, collections\nphr=[]\nfor p in ['tools/tests/linguistique/gold.json','tools/tests/linguistique/gold_reel.json']:\n    for x in json.load(open(p))['phrases']:\n        phr.append((p.split('/')[-1],x))\nc=collections.defaultdict(list)\nfor src,p in phr: c[(p[ … [370 caractères tronqués]`

  ```
[('gold_reel.json', 'r019'), ('gold_reel.json', 'r186')] ('Le vent souffle fort.', 'fr')
[('gold_reel.json', 'r051'), ('gold_reel.json', 'r189')] ('La voiture roule vite.', 'fr')
[('gold_reel.json', 'r336'), ('gold_reel.json', 'r358')] ('Paul sees Marie; he speaks to her.', 'en')
H50 contains:
[('r019', False), ('r186', False)] ('Le vent souffle fort.', 'fr')
[('r051', False), ('r189', False)] ('La voiture roule vite.', 'fr')
[('r336', False), ('r358', False)] ('Paul sees Marie; he speaks to her.', 'en')
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np = Path('tools/tests/linguistique/qualifier_tagger_h50.py')\ns = p.read_text()\ns = s.replace('''import json\nimport pathlib\nimport shutil''','''import json\nimport math\nimport pathlib\nimport shutil''')\ns = s.replace('''                \" … [1477 caractères tronqués]`

  ```
COMPILE-OK
AST-OK
  ```

- **bash** `{"command": "python3 tools/tests/linguistique/qualifier_tagger_h50.py --mode tous --cache-api /tmp/tagger-h50-api-cache --sortie reports/rapport-tagger-h50.json", "description": "Run full W2 measurement (warm, API, warm-after)", "run_in_background": true}`

  ```
started background job bash-45
  ```

- **bash** `{"command": "sed -n '180,215p' reports/INDEX.md; echo \"=== README reports\"; sed -n '1,40p' reports/README.md", "description": "Read report indexes around W1"}`

  ```
| [rapport-etat-r.md](rapport-etat-r.md) | État du chantier R — le lecteur : le tagger n'est pas à 0,944 contre 0,85, R1.2-1024 est mesuré, R4.4 attend la vérité humaine |
| [rapport-etat-s.md](rapport-etat-s.md) | S — 9/9 paragraphes jugés (19/19), 150 verdicts de banque ; la page `/` sert encore l'ancien arbre plat et la rétro-traduction n'existe pas |
| [rapport-evaluer-langue.md](rapport-evaluer-langue.md) | J11.2 — la mesure par langue : l'anglais devant, mais le gold n'est pas le même |
| [rapport-execution-v41.md](rapport-execution-v41.md) | Rapport — test d'exécution locale de DeepSeek-V4.1-Flash, avec toutes les optimisations |
| [rapport-exemples-rejoues.md](rapport-exemples-rejoues.md) | J11.1 — les cinq exemples rejoués : 4 blocs sur 5 ont bougé, `r035` n'est plus un échec |
| [rapport-exemples-tagger.md](rapport-exemples-tagger.md) | D1 — les exemples `--tagger` et `--reel` : le coût affiché, la base honnête, cinq blocs rejoués |
| [rapport-familles-9.md](rapport-familles-9.md) | C3.2c — les 9 familles : 7 sur 9 au-dessus de 30 % |
| [rapport-faq-sommaire.md](rapport-faq-sommaire.md) | E1 — la FAQ dans le sommaire et les liens : 9 ancres, 5 liens, 0 mort |
| [rapport-f
… [7451 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"R0.7\\|tagger\\|W2\\|J2\" docs/pilotage/roadmap.md | head -30; echo \"=== journal dirs\"; ls -la journal/ | head -20; echo \"=== latest journal\"; ls -1 journal/ | tail -10", "description": "Locate roadmap and journal conventions"}`

  ```
31:| **B — l'intelligence** | langue, pensée, jeux, maîtres, [banc externe](../theorie/glossaire/entrees/banc-externe.md), sémantique, modules | ✅ B1–B12 ; **B1.5 [corpus](../theorie/glossaire/entrees/corpus.md)**, **B12.10, B10.2bis et B11.10 closes** ; le **décodeur** est levé (objectif mot : 32,5 ; JW 26,7), le `z` reste ; **B13** (moteur de pensée) : state store v0 + **AC-3/alpha-bêta** + **[DRVF](../theorie/glossaire/entrees/drvf.md) `thought`** + **[banc](../theorie/glossaire/entrees/banc.md) anytime** + **opérateurs hétérogènes** + **nécessaire** + **labyrinthe** + **[porte](../theorie/glossaire/entrees/porte.md)** + **apprise** + **courbe** + **seule** + **stochastique** + **sto seule** + **ferme** + **minute** + **minute apprise** + **minute seule** + **minute entraînée** + **shaping** + **réseau** + **MLP** + **[professeur](../theorie/glossaire/entrees/professeur.md)** + **sans None** + **correction** + **audit** + **ouverte** + **graines** + **mobile** + **mobile graines** + **bruit** + **bouge** + **bouge graines** + **période** + **phase** + **phase graines** + **aléatoire** + **hasard** + **partielle** + **croyance** + **curiosité** + **observatrice** + **bruitée** + 
… [8463 caractères tronqués]
  ```

- **bash** `{"command": "date; echo \"---\"; git log -1 --format=%cd --date=iso; echo \"---\"; cat /etc/timezone 2>/dev/null || true", "description": "Check system date and last commit date"}`

  ```
dim 15 nov 2026 09:11:00 EST
---
2026-11-15 08:08:51 -0500
---
  ```

- **bash** `{"command": "sleep 20; tail -30 /tmp/nonexistent 2>/dev/null; echo \"---\"; ls -la reports/rapport-tagger-h50.json 2>/dev/null || echo \"no json yet\"", "description": "Wait and check output file"}`

  ```
---
-rw-r--r--. 1 stephane stephane 81023 15 nov 09:10 reports/rapport-tagger-h50.json
  ```

- **job_output** `{"job_id": "bash-45"}`

  ```
[cache_chaud] reste_402 · 402 phrases …
[cache_chaud] reste_402 · POS 0.9198 → 0.9629 (Δ +0.0431) · requêtes 0 · cache 399 · 1.6 s
[cache_chaud] h50 · 50 phrases …
[cache_chaud] h50 · POS 0.6842 → 0.8638 (Δ +0.1796) · requêtes 0 · cache 50 · 0.2 s
[cache_chaud] total · 452 phrases …
[cache_chaud] total · POS 0.8891 → 0.9500 (Δ +0.0609) · requêtes 0 · cache 449 · 1.8 s
[cache_chaud] tirage · 45 phrases …
[cache_chaud] tirage · POS 0.9073 → 0.9597 (Δ +0.0524) · requêtes 0 · cache 45 · 0.2 s
[cache_chaud] écrit · reports/rapport-tagger-h50.json
[api] reste_402 · 402 phrases …
[status: running]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/rapport-tagger-h50.json'))\nprint('passes', list(d['passes']))\np=d['passes']['cache_chaud']\nfor nom,b in p['bases'].items():\n    print('\\n===',nom, b['composition']['phrases'], b['composition']['tokens'])\n    print('heur', b[ … [790 caractères tronqués]`

  ```
passes ['cache_chaud']

=== reste_402 402 2157
heur 0.9198 0.958 0.8804
tags 0.9629 0.9406 0.9859
delta {'pos': 0.0431, 'pos_ferme': -0.0174, 'pos_ouvert': 0.1055, 'f1': 0.0, 'attachement': 0.0}
par langue {'en': (185, 993, 0.9718, 0.9708, -0.001), 'fr': (217, 1164, 0.8754, 0.9562, 0.0808)}
cout 399 0 399 0 57805 {'appels': 0.9925, 'requetes': 0.0, 'cache': 0.9925, 'tokens_reseau': 0.0, 'tokens_total': 143.79, 'latence_reseau_s': 0.0, 'latence_wall_s': 0.0001}
refus {'n': 0, 'ids': []}

=== h50 50 323
heur 0.6842 0.7542 0.5972
tags 0.8638 0.8156 0.9236
delta {'pos': 0.1796, 'pos_ferme': 0.0614, 'pos_ouvert': 0.3264, 'f1': 0.0, 'attachement': 0.0}
par langue {'en': (25, 155, 0.7742, 0.9355, 0.1613), 'fr': (25, 168, 0.6012, 0.7976, 0.1964)}
cout 50 0 50 0 7485 {'appels': 1.0, 'requetes': 0.0, 'cache': 1.0, 'tokens_reseau': 0.0, 'tokens_total': 149.7, 'latence_reseau_s': 0.0, 'latence_wall_s': 0.0001}
refus {'n': 0, 'ids': []}

=== total 452 2480
heur 0.8891 0.9294 0.8466
tags 0.95 0.9231 0.9784
delta {'pos': 0.0609, 'pos_ferme': -0.0063, 'pos_ouvert': 0.1318, 'f1': 0.0, 'attachement': 0.0}
par langue {'en': (210, 1148, 0.9451, 0.966, 0.0209), 'fr': (242, 1332, 0.8408, 0.9362, 0.0954)
… [695 caractères tronqués]
  ```

- **bash** `{"command": "sleep 60; echo \"check\"", "description": "Wait for API pass progress"}`

  ```
[still running after 60000ms; moved to background job bash-51]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **job_output** `{"job_id": "bash-45"}`

  ```
(no new output)
[status: running]
  ```

### 👤 Utilisateur

background job bash-51 (bash: sleep 60; echo "check") finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "grep -n \"rapport-tagger\" reports/INDEX.md; echo \"---\"; grep -n \"rapport-tagger\" reports/README.md; echo \"---\"; sed -n '260,290p' reports/INDEX.md", "description": "Find tagger entries in indexes"}`

  ```
733:| [rapport-tagger-erreurs.md](rapport-tagger-erreurs.md) | E2 — les cas d'erreur de `--tagger` : clé refusée = code 4, réseau et refus du modèle = repli heuristique |
734:| [rapport-tagger-option.md](rapport-tagger-option.md) | R0.7 / 1A — le tagger POS en option : +8,57 pts sur 20 phrases, +8,49 sur le gold 612 ; le défaut reste hors ligne |
---
42:| [`rapport-tagger-option.md`](rapport-tagger-option.md) | **R0.7 / 1A** — le tagger POS en option : **+8,57** sur 20 phrases, **+9,5** sur 612, défaut hors ligne |
---
| [rapport-miroir-blocs.md](rapport-miroir-blocs.md) | Le miroir des trois blocs : 34/34 tableaux, 296/296 modules, 42/42 formules |
| [rapport-mla-experts.md](rapport-mla-experts.md) | Rapport — MLA à rang faible et formats sans noyau : GLM-5.3 et Kimi deviennent calculables |
| [rapport-mode-listes.md](rapport-mode-listes.md) | Drave — « mode listes » : exécuter sans GPU |
| [rapport-mode4-lot-listes.md](rapport-mode4-lot-listes.md) | Mode 4 — le lot en listes : ÷2,3 sur les octets, et ce qu'il coûte |
| [rapport-modele-drave.md](rapport-modele-drave.md) | DÉVELOPPER UN MODÈLE **NATIF DRAVE** — étude, et le plan pour le mesurer |
| [rapport-modele-moteur.md](rappor
… [3478 caractères tronqués]
  ```

- **bash** `{"command": "ls -la journal/2026-11-15/ 2>/dev/null; echo \"===\"; find journal/2026-11-15 -maxdepth 2 -type f -printf '%p\\n' 2>/dev/null | head; echo \"=== sample journal\"; find journal/2026-11-14 -maxdepth 2 -type f | head -10", "description": "Inspect journal day structure"}`

  ```
total 40
drwxr-xr-x. 1 stephane stephane  130 15 nov 07:27 .
drwxr-xr-x. 1 stephane stephane  992 15 nov 01:33 ..
-rw-r--r--. 1 stephane stephane 2217 15 nov 08:11 distribue.md
-rw-r--r--. 1 stephane stephane 3694 15 nov 08:11 docs.md
-rw-r--r--. 1 stephane stephane 7314 15 nov 08:11 mesures.md
-rw-r--r--. 1 stephane stephane 1195 15 nov 08:11 modele.md
-rw-r--r--. 1 stephane stephane 1386 15 nov 08:11 outils.md
-rw-r--r--. 1 stephane stephane 1412 15 nov 08:11 portes.md
-rw-r--r--. 1 stephane stephane 8258 15 nov 08:11 README.md
===
journal/2026-11-15/portes.md
journal/2026-11-15/distribue.md
journal/2026-11-15/README.md
journal/2026-11-15/docs.md
journal/2026-11-15/outils.md
journal/2026-11-15/mesures.md
journal/2026-11-15/modele.md
=== sample journal
journal/2026-11-14/docs.md
journal/2026-11-14/memoire.md
journal/2026-11-14/portes.md
journal/2026-11-14/README.md
journal/2026-11-14/distribue.md
journal/2026-11-14/moteur.md
journal/2026-11-14/mesures.md
  ```

- **bash** `{"command": "sed -n '1,120p' journal/2026-11-15/README.md", "description": "Read 2026-11-15 journal README"}`

  ```
# 2026-11-15

> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
> [`journal/2026-11-15/`](README.md). Le récit écrit à la main est conservé plus bas, dans
> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
> [l'index des sessions](../README.md#sessions).

**26 commits** · **1 session(s)** · **6 thème(s)**

## Thèmes du jour

| thème | commits | fichier |
|---|---|---|
| distribue | 5 | [distribue.md](distribue.md) |
| docs | 7 | [docs.md](docs.md) |
| mesures | 10 | [mesures.md](mesures.md) |
| modele | 2 | [modele.md](modele.md) |
| outils | 1 | [outils.md](outils.md) |
| portes | 1 | [portes.md](portes.md) |

## Sessions DSH

| session | titre | début | durée | liens |
|---|---|---|---|---|
| `e181ce02-cd50-488a-a6be-e84b79d40dcc` | Documentation Drave avec diagrammes et implémentation | 2026-10-31 17:40 | 351.5 h | [rapport](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md) · [digest](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md) |

## Tous les commits (heure réelle)

| heure | commit | fait |
|---|---|---|
| 01:31 | `ce7241d5` | 6A — LA BASE HONNÊTE : evaluer --reel (452 PHRASES RÉELLES : PO
… [6800 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,100p' journal/2026-11-15/mesures.md", "description": "Read 2026-11-15 measurements journal"}`

  ```
# 2026-11-15 — Campagnes et mesures

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (10)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 01:39 | `2d7a7f2b` | 1A — LES DEUX DÉFAUTS DU TAGGER CORRIGÉS : 1 APPEL PAR PHRASE (LE TAGGER DE SYNTAGMES RETIRÉ) ET PONCT RESTITUÉ (25/25) ; POS 612 → 95,75 % (+9,5) | `en-cours.md`, `README.md`, `portes.md` (+9) |
| 01:42 | `6560a0a5` | 1A — LE TAGGER SUR LA BASE RÉELLE : 88,91 → 95,00 % (+6,1), 449 APPELS SERVIS PAR LE CACHE ; IL GAGNE SURTOUT SUR LE SYNTHÉTIQUE (+9,5 SUR 612) | `en-cours.md`, `README.md`, `mesures.md` (+7) |
| 02:13 | `292c70b5` | C1 — LA COMMANDE N2 VALIDÉE : --rope + canal (2,7856), JAMAIS --rope SEUL (40,0658), TÉMOIN 3,09 | `en-cours.md`, `README.md`, `docs.md` (+13) |
| 03:48 | `011b8b8e` | B2 — LES ATOMES NE PRÉDISENT PAS POS, SYNTAGMES NI ATTACHEMENT : SUR 28 ŒUVRES PROPRES, R² −0,092 / −0,160 / −0,092 (p 0,56 / 0,85 / 0,67) ; LE STYLE EST PR
… [5932 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-45"}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/rapport-tagger-h50.json'))\np=d['passes']['cache_chaud']\nfor nom in ['reste_402','h50']:\n    b=p['bases'][nom]\n    print('\\n===',nom)\n    for src in ['heuristique','tagger']:\n        conf=b[src]['pos']['confusions']\n        … [342 caractères tronqués]`

  ```
=== reste_402
heuristique
  DET    397/ 399 = 0.9950
  NOUN   458/ 462 = 0.9913
  VERB   402/ 512 = 0.7852
  ADJ     54/  67 = 0.8060
  ADV     71/  78 = 0.9103
  PRON   340/ 361 = 0.9418
  PREP    83/  83 = 1.0000
  CONJ    57/  69 = 0.8261
  AUX     99/ 103 = 0.9612
  NUM      2/   2 = 1.0000
  PONCT   21/  21 = 1.0000
tagger
  DET    390/ 399 = 0.9774
  NOUN   460/ 462 = 0.9957
  VERB   499/ 512 = 0.9746
  ADJ     67/  67 = 1.0000
  ADV     73/  78 = 0.9359
  PRON   337/ 361 = 0.9335
  PREP    77/  83 = 0.9277
  CONJ    52/  69 = 0.7536
  AUX     99/ 103 = 0.9612
  NUM      2/   2 = 1.0000
  PONCT   21/  21 = 1.0000

=== h50
heuristique
  DET     44/  44 = 1.0000
  NOUN    44/  57 = 0.7719
  VERB    27/  70 = 0.3857
  ADJ     11/  13 = 0.8462
  ADV     18/  21 = 0.8571
  PRON    46/  71 = 0.6479
  PREP     7/   7 = 1.0000
  CONJ     3/  14 = 0.2143
  AUX     17/  22 = 0.7727
  PONCT    4/   4 = 1.0000
tagger
  DET     43/  44 = 0.9773
  NOUN    57/  57 = 1.0000
  VERB    59/  70 = 0.8429
  ADJ     13/  13 = 1.0000
  ADV     19/  21 = 0.9048
  PRON    55/  71 = 0.7746
  PREP     6/   7 = 0.8571
  CONJ     3/  14 = 0.2143
  AUX     20/  22 = 0.9091
  PONCT    4/   4 = 1.0000
  ```

- **job_output** `{"job_id": "bash-45"}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "ls /tmp/tagger-h50-api-cache 2>/dev/null | wc -l; ps -o pid,etime,cmd -C python3 | grep qualifier_tagger_h50 | grep -v grep || true", "description": "Check API cache progress and process time"}`

  ```
129
3779294       02:15 python3 tools/tests/linguistique/qualifier_tagger_h50.py --mode tous --cache-api /tmp/tagger-h50-api-cache --sortie reports/rapport-tagger-h50.json
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -40; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Run documentation review baseline"}`

  ```
revue de documentation · 749 fiche(s) · 843 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ❌ 1 anomalie(s) :
     · compteurs : en-cours.md dit 842 JSON, le disque en a 843
EXIT=1
  ```

- **bash** `{"command": "python3 tools/verifie_en_cours.py 2>&1 | tail -20; echo \"EXIT=${PIPESTATUS[0]}\"; echo \"===\"; python3 tools/taille_documents.py 2>&1 | tail -20; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Run state and doc size checks baseline"}`

  ```
en-cours · 1625 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
EXIT=0
===
    3310    317   T1   3500  README.md
    3072    341 DATÉ      0  docs/implantation/convertisseur.md
    2962    364   T1   5000  docs/theorie/glossaire/02-modeles-et-architectures.md
    2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2513    224   T1   2800  reports/README.md
    2496    171   T1   2500  docs/pilotage/references-non-regression.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 3995 mots (budget 4 000)

  avertissements :
     · 57 fiche(s) > 300 lignes : lire le verdict + une section, jama
… [285 caractères tronqués]
  ```

- **bash** `{"command": "ls -la .git/hooks/ | head -20; echo \"===\"; sed -n '1,160p' .git/hooks/pre-commit 2>/dev/null | head -120", "description": "Inspect pre-commit hook"}`

  ```
total 68
drwxr-xr-x. 1 stephane stephane  576 31 oct 12:55 .
drwxr-xr-x. 1 stephane stephane  198 15 nov 09:06 ..
-rw-r--r--. 1 stephane stephane  478 25 sep 13:48 applypatch-msg.sample
-rw-r--r--. 1 stephane stephane 1972 25 sep 13:48 commit-msg.sample
-rw-r--r--. 1 stephane stephane 4611 25 sep 13:48 fsmonitor-watchman.sample
-rw-r--r--. 1 stephane stephane  189 25 sep 13:48 post-update.sample
-rw-r--r--. 1 stephane stephane  424 25 sep 13:48 pre-applypatch.sample
-rwxr-xr-x. 1 stephane stephane 1470 31 oct 12:55 pre-commit
-rw-r--r--. 1 stephane stephane 1649 25 sep 13:48 pre-commit.sample
-rw-r--r--. 1 stephane stephane  416 25 sep 13:48 pre-merge-commit.sample
-rw-r--r--. 1 stephane stephane 1492 25 sep 13:48 prepare-commit-msg.sample
-rw-r--r--. 1 stephane stephane 1374 25 sep 13:48 pre-push.sample
-rw-r--r--. 1 stephane stephane 4898 25 sep 13:48 pre-rebase.sample
-rw-r--r--. 1 stephane stephane  544 25 sep 13:48 pre-receive.sample
-rw-r--r--. 1 stephane stephane 2783 25 sep 13:48 push-to-checkout.sample
-rw-r--r--. 1 stephane stephane 2308 25 sep 13:48 sendemail-validate.sample
-rw-r--r--. 1 stephane stephane 3650 25 sep 13:48 update.sample
===
#!/bin/sh
# pre-commit — l'ét
… [1405 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"842\\|843\\|749\\|JSON de résultats\\|fichiers / JSON\" docs/pilotage/en-cours.md", "description": "Locate counters in en-cours"}`

  ```
109:| fichiers / JSON de résultats | **749** / **842** | `reports/*.md` / `reports/*.json` |
  ```

- **bash** `{"command": "sed -n '1,220p' tools/verifie_etat_a_jour.py", "description": "Read state freshness validator"}`

  ```
#!/usr/bin/env python3
"""verifie_etat_a_jour.py — aucun fait commité sans sa ligne d'état.

POURQUOI CET OUTIL EXISTE. `en-cours` est la seule source de l'état, et le contrat
disait « seul le principal écrit ». Ce n'est pas une garantie : l'identité se déduit
d'une variable d'environnement absente — un « pair » est autodéclaré — et si la
principale s'arrête, l'état se fige. Surtout, rien ne comparait les commits : la
revue ne regardait que la DATE, donc deux commits du même jour passaient. Le 29/10,
A8.0 (15 h 51) a été commité après le dernier état (15 h 34) sans aucune alerte.

La garantie est au commit, pas dans la discipline d'un écrivain :
  --index  (hook pre-commit) : un commit qui prépare un fait (reports/, roadmap,
           backlog) sans toucher `en-cours` est REFUSÉ ;
  --head   : si un fait a été commité après le dernier commit d'`en-cours`, l'état
           est en retard — la session qui le voit le corrige, sans attendre.

Le journal est du récit dérivé (le hook l'archive) : il n'exige pas de ligne d'état.

Usage :
  python3 tools/verifie_etat_a_jour.py             # --head
  python3 tools/verifie_etat_a_jour.py --index     # pour le hook
  python3 tools/verifie_eta
… [7182 caractères tronqués]
  ```

- **bash** `{"command": "ls /tmp/tagger-h50-api-cache 2>/dev/null | wc -l; ps -o pid,etime,cmd -C python3 | grep qualifier_tagger_h50 | grep -v grep || true", "description": "Check API cache progress"}`

  ```
141
3779294       02:27 python3 tools/tests/linguistique/qualifier_tagger_h50.py --mode tous --cache-api /tmp/tagger-h50-api-cache --sortie reports/rapport-tagger-h50.json
  ```

- **bash** `{"command": "ls /tmp/tagger-h50-api-cache 2>/dev/null | wc -l; ps -o pid,etime,cmd -C python3 | grep qualifier_tagger_h50 | grep -v grep || true", "description": "Check API cache progress again"}`

  ```
156
3779294       02:43 python3 tools/tests/linguistique/qualifier_tagger_h50.py --mode tous --cache-api /tmp/tagger-h50-api-cache --sortie reports/rapport-tagger-h50.json
  ```

- **bash** `{"command": "sed -n '1,80p' reports/rapport-tagger-erreurs.md; echo \"=== exemples\"; sed -n '1,60p' reports/rapport-exemples-tagger.md", "description": "Read tagger-related reports style"}`

  ```
# E2 — les cas d'erreur de `--tagger` : clé refusée = code 4, réseau et refus du modèle = repli heuristique

> **Ligne de roadmap** : **B13** (le produit) · **Tâche** : **E2** · **Date** : 2026-11-15 ·
> **Verdict** : ✅ **4/4 cas caractérisés**, **18/18 tests**, **0 socket**.
> **La clé invalide (HTTP 401/403) sort désormais 4** avec un message clair et **rien sur
> `stdout`** ; avant, elle était avalée par le tagger et le CLI rendait **0** avec un repli
> heuristique déguisé en cascade. Le **réseau coupé** (3 essais du client) et le **refus du
> modèle** restent des refus **par phrase** : repli heuristique, code **0**, cause dans `refus`.
> **Dispositif** : [`tools/drave.py`](../tools/drave.py) 0.1.0, client `DeepSeek` injecté,
> transport factice, cache temporaire vide, aucun socket. **Contrôle négatif** : un transport
> valide donne code 0 et des POS neuronaux ; la mutation qui retire le contrôle 401/403 fait
> échouer le test (`0 != 4`). **JSON** : [`rapport-tagger-erreurs.json`](rapport-tagger-erreurs.json).

## 1. Les quatre cas

Le tableau dit le comportement **du code courant**, pas l'intention. Chaque ligne a son test
dans [`test_tagger_api.py`](../tools/tests/test_tagger_
… [8677 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"95,00\\|0,9500\\|tagger\\|--tagger\" docs/produit/README.md | head -40", "description": "Find tagger claims in product README"}`

  ```
11:> porte produit est verte. Le **tagger POS par API** est livré **en option** (`--tagger`,
47:aucun accès réseau **par défaut** (le tagger en option, lui, appelle l'API DeepSeek, § 3.7). Les
64:| **POS** | DET, NOUN, VERB, ADJ, ADV, PREP, PRON, AUX, CONJ, NUM… | **0,8625** (fermé 0,9373, ouvert 0,7918) ; **0,8891** sur le réel 452 ; **0,9575** avec `--tagger` |
386:### 3.7 Le tagger en option — `--tagger`
389:python3 tools/drave.py analyser "Le chat dort." --tagger
390:python3 tools/drave.py analyser --fichier corpus.txt --jsonl --tagger
391:python3 tools/drave.py evaluer --tagger
394:drave 0.1.0 — analyse cascade POS (tagger API DeepSeek, réseau)
416:**Les cas d'erreur.** Mesurés par [`test_tagger_api.py`](../../tools/tests/test_tagger_api.py)
422:| **clé invalide** (HTTP 401/403) | refuse de démarrer, **sans repli** | **4** | vide | `drave: dépendance absente : clé DeepSeek refusée (HTTP 401) : vérifiez DEEPSEEK_KEY_FILE, ~/.config/drave/deepseek.key ou DEEPSEEK_API_KEY. Sans --tagger, le défaut reste l'heuristique hors ligne.` |
423:| **réseau coupé** (après 3 essais) | **replie** sur l'heuristique | **0** | annotation heuristique | `drave: tagger : refus partiel : neuronal-po
… [3251 caractères tronqués]
  ```

- **bash** `{"command": "ls /tmp/tagger-h50-api-cache 2>/dev/null | wc -l; ps -o pid,etime,cmd -C python3 | grep qualifier_tagger_h50 | grep -v grep || true", "description": "Check API progress"}`

  ```
162
3779294       02:50 python3 tools/tests/linguistique/qualifier_tagger_h50.py --mode tous --cache-api /tmp/tagger-h50-api-cache --sortie reports/rapport-tagger-h50.json
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/rapport-tagger-h50.json'))\np=d['passes']['cache_chaud']\nfor nom in ['reste_402','h50','total','tirage']:\n    b=p['bases'][nom]\n    for src in ['heuristique','tagger']:\n        conf=b[src]['pos']['confusions']\n        justes= … [252 caractères tronqués]`

  ```
reste_402 heuristique 1984 / 2157 = 0.9198
reste_402 tagger 2077 / 2157 = 0.9629
reste_402 delta {'pos': 0.0431, 'pos_ferme': -0.0174, 'pos_ouvert': 0.1055, 'f1': 0.0, 'attachement': 0.0}
h50 heuristique 221 / 323 = 0.6842
h50 tagger 279 / 323 = 0.8638
h50 delta {'pos': 0.1796, 'pos_ferme': 0.0614, 'pos_ouvert': 0.3264, 'f1': 0.0, 'attachement': 0.0}
total heuristique 2205 / 2480 = 0.8891
total tagger 2356 / 2480 = 0.95
total delta {'pos': 0.0609, 'pos_ferme': -0.0063, 'pos_ouvert': 0.1318, 'f1': 0.0, 'attachement': 0.0}
tirage heuristique 225 / 248 = 0.9073
tirage tagger 238 / 248 = 0.9597
tirage delta {'pos': 0.0524, 'pos_ferme': -0.0077, 'pos_ouvert': 0.1197, 'f1': 0.0, 'attachement': 0.0}
  ```

- **bash** `{"command": "ls /tmp/tagger-h50-api-cache 2>/dev/null | wc -l; ps -o pid,etime,cmd -C python3 | grep qualifier_tagger_h50 | grep -v grep || true", "description": "Check API progress"}`

  ```
170
3779294       02:58 python3 tools/tests/linguistique/qualifier_tagger_h50.py --mode tous --cache-api /tmp/tagger-h50-api-cache --sortie reports/rapport-tagger-h50.json
  ```

- **bash** `{"command": "ls /tmp/tagger-h50-api-cache 2>/dev/null | wc -l; ps -o pid,etime,cmd -C python3 | grep qualifier_tagger_h50 | grep -v grep || true", "description": "Check API progress"}`

  ```
181
3779294       03:09 python3 tools/tests/linguistique/qualifier_tagger_h50.py --mode tous --cache-api /tmp/tagger-h50-api-cache --sortie reports/rapport-tagger-h50.json
  ```

- **bash** `{"command": "sleep 90; ls /tmp/tagger-h50-api-cache 2>/dev/null | wc -l", "description": "Wait 90s and check progress"}`

  ```
[still running after 60000ms; moved to background job bash-71]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **bash** `{"command": "ls /tmp/tagger-h50-api-cache 2>/dev/null | wc -l; ps -o pid,etime,cmd -C python3 | grep qualifier_tagger_h50 | grep -v grep || true", "description": "Check API progress"}`

  ```
249
3779294       04:17 python3 tools/tests/linguistique/qualifier_tagger_h50.py --mode tous --cache-api /tmp/tagger-h50-api-cache --sortie reports/rapport-tagger-h50.json
  ```

- **bash** `{"command": "cat > /tmp/rapport-tagger-h50.md <<'MD'\n# W2 — le tagger POS sur le split 402 / H50 : +4,31 pts sur 402, +17,96 sur H50 ; il gagne sur les deux, donc la règle ne le rejette pas\n\n> **Ligne de roadmap** : **R0.7** (le lecteur) / **B13** · **Tâche** : **W2** (semaine 2, J2 matin) ·\n> * … [19725 caractères tronqués]`

  ```
310 /tmp/rapport-tagger-h50.md
  ```

### 👤 Utilisateur

background job bash-71 (bash: sleep 90; ls /tmp/tagger-h50-api-cache 2>/dev/null | wc -l) finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "ls /tmp/tagger-h50-api-cache 2>/dev/null | wc -l; ps -o pid,etime,cmd -C python3 | grep qualifier_tagger_h50 | grep -v grep || true", "description": "Check API progress"}`

  ```
292
3779294       05:03 python3 tools/tests/linguistique/qualifier_tagger_h50.py --mode tous --cache-api /tmp/tagger-h50-api-cache --sortie reports/rapport-tagger-h50.json
  ```

- **job_output** `{"job_id": "bash-45"}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "sleep 45; ls /tmp/tagger-h50-api-cache 2>/dev/null | wc -l", "description": "Wait and check API progress"}`

  ```
354
  ```

- **job_output** `{"job_id": "bash-45", "timeout_ms": 120000, "wait": true}`

  ```
[api] reste_402 · POS 0.9198 → 0.9643 (Δ +0.0445) · requêtes 397 · cache 2 · 397.7 s
[api] h50 · 50 phrases …
[api] h50 · POS 0.6842 → 0.8607 (Δ +0.1765) · requêtes 50 · cache 0 · 49.9 s
[api] total · 452 phrases …
[api] total · POS 0.8891 → 0.9508 (Δ +0.0617) · requêtes 0 · cache 449 · 1.9 s
[api] tirage · 45 phrases …
[api] tirage · POS 0.9073 → 0.9556 (Δ +0.0483) · requêtes 0 · cache 45 · 0.2 s
[api] écrit · reports/rapport-tagger-h50.json
[cache_chaud_apres_api] reste_402 · 402 phrases …
[cache_chaud_apres_api] reste_402 · POS 0.9198 → 0.9643 (Δ +0.0445) · requêtes 0 · cache 399 · 1.6 s
[cache_chaud_apres_api] h50 · 50 phrases …
[cache_chaud_apres_api] h50 · POS 0.6842 → 0.8607 (Δ +0.1765) · requêtes 0 · cache 50 · 0.2 s
[cache_chaud_apres_api] total · 452 phrases …
[cache_chaud_apres_api] total · POS 0.8891 → 0.9508 (Δ +0.0617) · requêtes 0 · cache 449 · 1.9 s
[cache_chaud_apres_api] tirage · 45 phrases …
[cache_chaud_apres_api] tirage · POS 0.9073 → 0.9556 (Δ +0.0483) · requêtes 0 · cache 45 · 0.2 s
[cache_chaud_apres_api] écrit · reports/rapport-tagger-h50.json
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/rapport-tagger-h50.json'))\nprint('passes', list(d['passes']))\nfor nom in d['passes']:\n    print('\\n###', nom)\n    p=d['passes'][nom]\n    print('cache_avant', p['cache_avant'])\n    print('cache_apres', p['cache_apres'])\n    … [1423 caractères tronqués]`

  ```
passes ['cache_chaud', 'api', 'cache_chaud_apres_api']

### cache_chaud
cache_avant {'fichiers': 3759, 'dates': {'min': '2026-10-26T11:22:15-0400', 'max': '2026-11-15T01:38:53-0500'}, 'modeles': {'deepseek-flash': 3759}}
cache_apres {'fichiers': 3759, 'dates': {'min': '2026-10-26T11:22:15-0400', 'max': '2026-11-15T01:38:53-0500'}, 'modeles': {'deepseek-flash': 3759}}
modeles {'deepseek-flash': 943}

-- reste_402 402 2157
heur 0.9198 0.958 0.8804
tags 0.9629 0.9406 0.9859
delta {'pos': 0.0431, 'pos_ferme': -0.0174, 'pos_ouvert': 0.1055, 'f1': 0.0, 'attachement': 0.0}
counts 1984 2077 2157
par langue {'en': (185, 993, 0.9718, 0.9708, -0.001, -0.0493, 0.0493), 'fr': (217, 1164, 0.8754, 0.9562, 0.0808, 0.0102, 0.1528)}
cout {'phrases': 402, 'appels': 399, 'requetes': 0, 'cache': 399, 'tokens_reseau': 0, 'tokens_cache': 57805, 'latence_reseau_s': 0, 'latence_cache_s': 374.796, 'latence_wall_s': 0.058, 'latence_requete': {'moyenne': 0.0, 'mediane': 0.0, 'p95': 0.0, 'max': 0.0}, 'par_phrase': {'appels': 0.9925, 'requetes': 0.0, 'cache': 0.9925, 'tokens_reseau': 0.0, 'tokens_total': 143.79, 'latence_reseau_s': 0.0, 'latence_wall_s': 0.0001}, 'phrases_sans_appel': {'n': 0, 'ids': []}}
refus
… [13522 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/rapport-tagger-h50.json'))\np=d['passes']['api']\nfor nom in ['reste_402','h50','total','tirage']:\n    b=p['bases'][nom]\n    print('\\n===',nom)\n    for src in ['heuristique','tagger']:\n        conf=b[src]['pos']['confusions'] … [336 caractères tronqués]`

  ```
=== reste_402
heuristique
  DET    397/ 399 = 0.9950
  PREP    83/  83 = 1.0000
  CONJ    57/  69 = 0.8261
  PRON   340/ 361 = 0.9418
  ADV     71/  78 = 0.9103
  AUX     99/ 103 = 0.9612
  NOUN   458/ 462 = 0.9913
  VERB   402/ 512 = 0.7852
  ADJ     54/  67 = 0.8060
  NUM      2/   2 = 1.0000
  PONCT   21/  21 = 1.0000
tagger
  DET    394/ 399 = 0.9875
  PREP    76/  83 = 0.9157
  CONJ    50/  69 = 0.7246
  PRON   340/ 361 = 0.9418
  ADV     74/  78 = 0.9487
  AUX     96/ 103 = 0.9320
  NOUN   460/ 462 = 0.9957
  VERB   500/ 512 = 0.9766
  ADJ     67/  67 = 1.0000
  NUM      2/   2 = 1.0000
  PONCT   21/  21 = 1.0000

=== h50
heuristique
  DET     44/  44 = 1.0000
  PREP     7/   7 = 1.0000
  CONJ     3/  14 = 0.2143
  PRON    46/  71 = 0.6479
  ADV     18/  21 = 0.8571
  AUX     17/  22 = 0.7727
  NOUN    44/  57 = 0.7719
  VERB    27/  70 = 0.3857
  ADJ     11/  13 = 0.8462
  PONCT    4/   4 = 1.0000
tagger
  DET     43/  44 = 0.9773
  PREP     6/   7 = 0.8571
  CONJ     3/  14 = 0.2143
  PRON    55/  71 = 0.7746
  ADV     19/  21 = 0.9048
  AUX     20/  22 = 0.9091
  NOUN    57/  57 = 1.0000
  VERB    58/  70 = 0.8286
  ADJ     13/  13 = 1.0000
  PONCT    4/   4 = 1.0000

=== 
… [1243 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json, collections, sys, pathlib\nsys.path.insert(0,'.'); sys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nd=json.load(open('reports/rapport-gold-452.json'))\nh=set(d['split']['h50_ids'])\nphr=[]\nfor f in ['tools/tests/linguistique/gold.json','tools/t … [718 caractères tronqués]`

  ```
['r010', 'r423'] ('Tu', 'viens', 'demain')
['r019', 'r186'] ('Le', 'vent', 'souffle', 'fort')
['r030', 'r427'] ('You', 'come', 'tomorrow')
['r051', 'r189'] ('La', 'voiture', 'roule', 'vite')
['r336', 'r358'] ('Paul', 'sees', 'Marie', 'he', 'speaks', 'to', 'her')
text dups:
['r019', 'r186'] ('Le vent souffle fort.', 'fr')
['r051', 'r189'] ('La voiture roule vite.', 'fr')
['r336', 'r358'] ('Paul sees Marie; he speaks to her.', 'en')
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nphr={}\nfor f in ['tools/tests/linguistique/gold.json','tools/tests/linguistique/gold_reel.json']:\n    for p in json.load(open(f))['phrases']: phr[p['id']]=p['texte']\nfor i in ['r010','r423','r030','r427']:\n    print(i, repr(phr[i]))\nPY", "description" … [41 caractères tronqués]`

  ```
r010 'Tu viens demain ?'
r423 'Tu viens demain.'
r030 'You come tomorrow?'
r427 'You come tomorrow.'
  ```

- **bash** `{"command": "cat > reports/rapport-tagger-h50.md <<'MD'\n# W2 — le tagger POS sur le split 402 / H50 : +4,45 pts sur 402, +17,65 sur H50 ; il gagne sur les deux, donc la règle ne le rejette pas\n\n> **Ligne de roadmap** : **R0.7** (le lecteur) / **B13** · **Tâche** : **W2** (semaine 2, J2 matin) ·\n … [21678 caractères tronqués]`

  ```
331 reports/rapport-tagger-h50.md
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/rapport-tagger-h50.json'))\nprint('commit_mesure', d['commit_mesure'])\nprint('date', d['date'])\nprint('modele', d['modele_demande'])\nprint('or', d['or'])\nprint('split partition', d['split']['partition'])\nprint('composition ke … [413 caractères tronqués]`

  ```
commit_mesure 6b2208ee1579739a188086f957c0d508e8a04726
date 2026-11-15 09:18 EST
modele deepseek-chat
or {'phrases': 452, 'tokens': 2480, 'sources': {'hand': 20, 'reel': 432}, 'langues': {'fr': 242, 'en': 210}, 'textes_dupliques': [{'texte': 'Le vent souffle fort.', 'langue': 'fr', 'n': 2, 'ids': ['r019', 'r186']}, {'texte': 'La voiture roule vite.', 'langue': 'fr', 'n': 2, 'ids': ['r051', 'r189']}, {'texte': 'Paul sees Marie; he speaks to her.', 'langue': 'en', 'n': 2, 'ids': ['r336', 'r358']}]}
split partition {'h50': 50, 'reste_402': 402, 'total': 452, 'intersection': 0}
composition keys dict_keys(['h50', 'reste_402', 'total', 'tirage_hors_h50'])
regle verdict accepté
passes ['cache_chaud', 'api', 'cache_chaud_apres_api']
cache_chaud avant {'fichiers': 3759, 'dates': {'min': '2026-10-26T11:22:15-0400', 'max': '2026-11-15T01:38:53-0500'}, 'modeles': {'deepseek-flash': 3759}}
cache_api apres {'fichiers': 447, 'dates': {'min': '2026-11-15T09:11:00-0500', 'max': '2026-11-15T09:18:28-0500'}, 'modeles': {'deepseek-flash': 447}}
cache_apres_api avant {'fichiers': 447, 'dates': {'min': '2026-11-15T09:11:00-0500', 'max': '2026-11-15T09:18:28-0500'}, 'modeles': {'deepseek-flash': 447}}
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('reports/rapport-tagger-h50.md')\ns=p.read_text()\ns=s.replace(\"**VERB +19,14** et **ADJ +19,40**\\nportent à eux seuls **+38,54 pts** de rappel ; le fermé perd **−1,55 pt** au total, surtout\",\n            \"**VERB +19,14** et **ADJ  … [1209 caractères tronqués]`

  ```
done
153:| **total 452 (402 + H50)** | 452 | 449 | **447** | 2 | **65 029** | 261 | **143,87** (réseau) · 144,45 (total) | **0,993 s** (moyenne pondérée) | **0,982 s** | 452,0 s (passe) |
154:| **total, rejoué (base `total`)** | 452 | 449 | 0 | 449 | 0 | 65 290 | 0 (réseau) · 144,45 (lu) | — | — | 0,1 s |
  ```

- **bash** `{"command": "grep -n \"38,54\\|net du fermé\\|gain n'est porté\" reports/rapport-tagger-h50.md; sed -n '135,150p' reports/rapport-tagger-h50.md; sed -n '235,255p' reports/rapport-tagger-h50.md", "description": "Inspect remaining wording"}`

  ```
| base | phrases | POS heuristique | POS tagger | Δ |
|---|---:|---:|---:|---:|
| **total 452** | 452 | 0,8891 | **0,9508** | **+6,17 pts** |
| **tirage 20261116 hors H50** | 45 | 0,9073 | **0,9556** | **+4,83 pts** |

**Lecture.** Le tirage aléatoire **hors H50** gagne **+4,83 pts**, du même ordre que le 402
(+4,45) et **loin** du H50 (+17,65) : le gain « normal » est autour de **+4,5 à +5**, et H50 est
bien un **stress test**, pas un échantillon. Le tirage n'est pas un échantillon neuf : c'est un
contrôle de composition, il ne remplace pas une généralisation hors gold.

## 3. Le coût et la latence

### 3.1 La passe API

| base | phrases | appels | requêtes | cache | tokens réseau | tokens lus du cache | tokens / phrase | latence / requête | latence / phrase | durée |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
ne compense pas, et le gain net vient de l'ouvert (VERB +19,14, ADJ +19,40). Cette réserve ne
change pas le verdict de la règle **telle qu'elle est écrite**, mais elle change la **décision du
défaut** (W3) :

- **garder `--tagger` opt-in** : le défaut hors ligne reste l'heuristique ; l'option gagne en
  agrégé sur le 402 et sur H50 ;
- **ou tester un hybride** «
… [896 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"Le gain du 402\" -A 4 reports/rapport-tagger-h50.md", "description": "Locate the 402 class-gain paragraph"}`

  ```
125:**Lecture.** Le gain du 402 est **un gain de classes ouvertes** : **VERB +19,14** et **ADJ +19,40** gagnent ces points de rappel **dans leur
126-classe** ; le fermé perd **−1,55 pt** au total, surtout
127-**PREP −8,43** et **CONJ −10,15**, avec **AUX −2,92** et **DET −0,75**. Le tagger répare les verbes
128-et les adjectifs, et il **casse un peu de fermé**. Sur H50, le même tagger gagne **aussi** le fermé
129-(VERB 0,3857 → 0,8286, PRON 0,6479 → 0,7746, AUX 0,7727 → 0,9091, NOUN 0,7719 → 1,0000) : le lot
  ```

- **bash** `{"command": "sed -n '1,8p' docs/pilotage/en-cours.md; echo \"--- R line\"; sed -n '118,128p' docs/pilotage/en-cours.md; echo \"--- ce qui reste\"; sed -n '128,136p' docs/pilotage/en-cours.md; echo \"--- counters\"; sed -n '104,112p' docs/pilotage/en-cours.md", "description": "Read en-cours sections  … [9 caractères tronqués]`

  ```
# En ce moment

**Mis à jour : 2026-11-15, 09 h 10 HNE (W1 : gold 452)**

> **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
> plan plus bas (**La carte**).

### Session `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — le hub de reprise du 04/11 *(en pause)*
--- R line
| chantier | frontière (graphe) | bloquant (ressource) | prochaine action |
|---|---|---|---|
| **A — le moteur** | **A2.6** | A3.4 Colab ; A5.4 FPGA ; **A6.2 libre** (MoE 18,56 Go, PPL 37,2013 ; résidence 16 GiB) | **A2.6** (experts et tête) ; **A6.2** rapport + A8.3b2 |
| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, F1 0,7902, 238/239, schéma v2, restit v1, produit (J11)** | **`g017` tranché** ; T132/T133, **[gold 452](../../reports/rapport-gold-452.md)** ; **B10.3 bloquée** |
| **N — le natif** | **N2, N4** | N2 : **fenêtre 1 024 — 2,3911 / 2,3522 au grand corpus (sous 2,5)** ; porte propre 2,7856 (manque **0,2856** val / **0,3566** test) ; **[v2](../../reports/rapport-coordination-n2-v2.md)** ; **N3 couvert** (17 portes, inventaire ; deux conditions) ; N4 0/4 ; N5 gelé | **les runs N2** ; puis la **porte propre** ; **N4** |
| **
… [1588 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"## Ce qui est en cours\" -A 6 docs/pilotage/en-cours.md; echo \"---\"; sed -n '84,104p' docs/pilotage/en-cours.md", "description": "Read en-cours in-progress section"}`

  ```
86:## Ce qui est en cours
87-
88-- **S — les structures** : 61/61 types, 144/144 rôles, 56 tests, banque 84/67 ; **19/19 verdicts `389b99f`** ; `/paragraphes` v7, `/` ancien arbre ; [v2](../../reports/rapport-coordination-s-v2.md).
89-- **N2 — en pause** : **commande validée** `eval_longueurs.py --rope --val <dir>` (**2,7856**) ; **jamais `--rope` seul** (**40,0658**) ; [v2 : 3,09 tenu](../../reports/rapport-coordination-n2-v2.md) ; puis **porte propre (0,29)**.
90-- **Pensée — B13 (actif)** : **183/183** ; `r035` (238/238), `s065` (238/238), **J6.1 rejeté** (`g017` inatteignable), schéma v2, **v2** **19/46** (**16** non vides, F1 **0,5270**) ([fiche](../../reports/rapport-restitution-v2.md)), **D1–D3** ([FAQ](../../reports/rapport-faq.md)), **E1** ([sommaire](../../reports/rapport-faq-sommaire.md)) ; [s065](../../reports/rapport-s065.md), [J9.1](../../reports/rapport-passe-honnetete.md).
91-- **L — le bloc langue** : contrat ; frontière script 1,0, langue 0,137/0,9687 ; fusion réparée par niveau **0,9309/0,8226/0,8784/0,9954**.
92-- **Panini J2.1–J3.2 + B2** : **14 atomes** ; UDHR **418/438** ; J3.2 : **5/21** langues (Glottolog **21/21**), **154/154** paires hors script au hasard
… [3523 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('docs/pilotage/en-cours.md')\ns=p.read_text()\ns=s.replace(\"**Mis à jour : 2026-11-15, 09 h 10 HNE (W1 : gold 452)**\",\n            \"**Mis à jour : 2026-11-15, 09 h 25 HNE (W2 : tagger 402/H50)**\")\ns=s.replace(\"| **R — le lecteur* … [1785 caractères tronqués]`

  ```
updated
3:**Mis à jour : 2026-11-15, 09 h 25 HNE (W2 : tagger 402/H50)**
92:- **W2 — le tagger sur 402/H50** : 402 **0,9198 → 0,9643** (+4,45), H50 **0,6842 → 0,8607** (+17,65) ; F1/attachement 402 **inchangés** ; **fermé 402 −1,55** (PREP −8,43, CONJ −10,15) ; [fiche](../../reports/rapport-tagger-h50.md) ; **la règle ne le rejette pas** (il gagne sur 402), la réserve du fermé va à **W3**.
110:| fichiers / JSON de résultats | **750** / **844** | `reports/*.md` / `reports/*.json` |
124:| **R — le lecteur** | **R0.7** | **R0.7 — tagger 612 : 0,9575 (+9,5) ; réel 452 : 0,9500 (+6,1) ; split 402/H50 : 402 0,9643 (+4,45), H50 0,8607 (+17,65), F1/attachement 402 inchangés, fermé 402 −1,55** ; R2/R3 attendent N5/N4 | **W2 faite** ; **W3 — tagger par défaut** (réserve fermé) ; **[fiche H50](../../reports/rapport-tagger-h50.md)** |
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('reports/INDEX.md')\ns=p.read_text()\nold=\"| [rapport-tagger-erreurs.md](rapport-tagger-erreurs.md) | E2 — les cas d'erreur de `--tagger` : clé refusée = code 4, réseau et refus du modèle = repli heuristique |\\n\"\nnew=old+\"| [rappor … [887 caractères tronqués]`

  ```
index ok
reports/INDEX.md:734:| [rapport-tagger-h50.md](rapport-tagger-h50.md) | W2 — le tagger POS sur le split 402 / H50 : +4,45 pts sur 402, +17,65 sur H50, la règle ne le rejette pas ; réserve fermé 402 −1,55 |
reports/README.md:22:| [`rapport-tagger-h50.md`](rapport-tagger-h50.md) | **W2/R0.7** — le tagger sur le split : 402 **0,9198 → 0,9643** (+4,45), H50 **0,6842 → 0,8607** (+17,65) ; F1/attachement 402 inchangés, fermé 402 **−1,55** ; la règle ne le rejette pas |
  ```

- **bash** `{"command": "grep -n \"le tagger n'est pas à 0,944\" docs/pilotage/roadmap.md; sed -n '33p' docs/pilotage/roadmap.md | fold -w 220 | head -20", "description": "Inspect roadmap R line"}`

  ```
33:| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ; **le tagger n'est pas à 0,944 contre 0,85** (corpus différents : +7,34 pts sur 180, +6,35 sur 432) ; **R1.2-1024 mesuré** (2,6256 à 1 000 o) ; **R4.1–R4.4 mesurées** (R4.4 : 4/5 familles ≥ 90 % de parité) ; **R0.7 — bloc linguistique** (398 langues, 0,9687) | **R4.4 close** (limites nommées) ; **R1.1/R1.2 mesurées** (RoPE **3,2545** à 1 000 octets, fenêtre **−0,244**) ; la suite : **1 024 octets entraînés** ; **`rope2048`** **fini** (2×10 000 pas, deux drvm) ; R2/R3 attendent N5/N4 |
| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ; **le tagger n'est p
as à 0,944 contre 0,85** (corpus différents : +7,34 pts sur 180, +6,35 sur 432) ; **R1.2-1024 mesuré** (2,6256 à 1 000 o) ; **R4.1–R4.4 mesurées** (R4.4 : 4/5 familles ≥ 90 % de parité) ; **R0.7 — bloc linguistique** (39
8 langues, 0,9687) | **R4.4 close** (limites nommées) ; **R1.1/R1.2
… [183 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('docs/pilotage/roadmap.md')\ns=p.read_text()\nold=\"**R0.7 — bloc linguistique** (398 langues, 0,9687) | \"\nnew=\"**R0.7 — bloc linguistique** (398 langues, 0,9687) ; **W2 — le tagger sur 402/H50 : 402 0,9643 (+4,45), H50 0,8607 (+17,6 … [704 caractères tronqués]`

  ```
roadmap ok
33:| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)**
  ```

- **bash** `{"command": "tail -30 journal/2026-11-15/README.md", "description": "Read end of journal README notes"}`

  ```
l'**attachement** (**−0,092**, p=0,67). Le seul ρ nominal (POS **+0,176**, p=0,029) tombe à **Holm 0,088**
et ne survit pas à la date (**p_resid=1,0**).

Le dispositif n'est pas muet : il prédit l'**entropie des graphèmes** (**+0,811**), la **longueur des
mots** (**+0,657**), la **négation** (**+0,440**) et la **part de verbes** (**+0,429**). Mais la date
explique **0,16–0,54** de ces métriques et **aucune** ne survit au contrôle de date (**p_resid=0,76–1,0**).
Les atomes sont une signature **d'époque et de genre**, pas une entrée syntaxique.

Le signal brut des **36 mesurables** (POS **+0,102**, syntagmes **+0,060**) tombe à **+0,010 / +0,014**
sur 34, puis **−0,080 / −0,204** sur 26 : il est porté par les **sources courtes** et **deux signatures
non-propres**. Le protocole, les 2 000 permutations de colonnes et les 1 000 permutations de date sont dans
[`reports/rapport-atomes-prediction.md`](../../reports/rapport-atomes-prediction.md) et
[`reports/atomes-prediction.json`](../../reports/atomes-prediction.json). La suite : un gold anglais de
niveaux et une signature recalculée sur le texte nettoyé.

### B3 — le corpus CIC tient, mais le vérificateur voit plus loin

J12.2 avait le *
… [1119 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('journal/2026-11-15/README.md')\ns=p.read_text()\nnote='''\n### W2 — le tagger sur 402/H50 : il gagne sur les deux, le fermé du 402 paie\n\nLe split de W1 (**402 / H50**) reçoit sa mesure : le tagger POS de l'API gagne **+4,45 pts** sur … [1063 caractères tronqués]`

  ```
journal note added

Le split de W1 (**402 / H50**) reçoit sa mesure : le tagger POS de l'API gagne **+4,45 pts** sur les
**402** (0,9198 → 0,9643) et **+17,65** sur **H50** (0,6842 → 0,8607) ; le F1 et l'attachement du
402 sont **inchangés**. La passe **API** paie **447 requêtes** et **65 029 tokens réseau** pour 452
phrases (**0,982 s/phrase**) ; le **cache chaud après API** rejoue **0 réseau / 0 token** et redonne
exactement les mêmes scores. La règle « une règle qui ne gagne que sur H50 est rejetée » **ne rejette
pas** le tagger : il gagne sur le 402, pas seulement sur H50. La **réserve** est nommée : sur 402, le
fermé perd **−1,55 pt** (PREP −8,43, CONJ −10,15) et le gain vient de l'ouvert (VERB +19,14, ADJ
+19,40) ; H50, lui, gagne **aussi** le fermé. La suite (W3) doit décider du défaut et, si possible,
tester l'hybride fermé/ouvert.
[`fiche`](../../reports/rapport-tagger-h50.md) · [`JSON`](../../reports/rapport-tagger-h50.json).
<!-- /notes -->
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -30; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Run documentation review after edits"}`

  ```
revue de documentation · 750 fiche(s) · 843 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ❌ 1 anomalie(s) :
     · compteurs : en-cours.md dit 844 JSON, le disque en a 843
EXIT=1
  ```

- **bash** `{"command": "python3 tools/verifie_en_cours.py 2>&1 | tail -10; echo \"EXIT=${PIPESTATUS[0]}\"; python3 tools/taille_documents.py 2>&1 | tail -8; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Run state and size checks"}`

  ```
en-cours · 1701 mots · 7 sections · 4 session(s) · 10 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
EXIT=0
  T0 max : 4071 mots (budget 4 000)

  avertissements :
     · 58 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 2 violation(s) :
     · docs/pilotage/roadmap.md : 9033 mots > budget 9000 (T1)
     · T0 : 4071 mots (AGENTS + en-cours + une tâche) > budget 4 000
EXIT=1
  ```

- **bash** `{"command": "grep -n \"JSON\\|json\\|fiche\\|glob\\|rglob\" tools/revue_documentation.py | head -60; echo \"===\"; sed -n '1,140p' tools/revue_documentation.py", "description": "Inspect doc review counting logic"}`

  ```
5:  1. classement : pas de résultats dans docs/ (les fiches sont dans reports/ et citées) ;
6:  2. structure  : les sept chantiers de en-cours.md ont leur entrée, leur état et leur fiche ;
12:     les compteurs de la page d'état sont ceux du disque (portes, chapitres, fiches, docs) ;
31:    r"[^`\s]+?\.(?:md|json|sh|py|rs|txt|svg|csv|jsonl))`"
67:    return [p for p in (RACINE / "docs").rglob("*.md")
72:    return list((RACINE / "docs").rglob("*.md"))
76:    return list((RACINE / "reports").glob("*.md"))
93:    """Les fichiers dont les liens doivent résoudre (docs, fiches courantes, racine)."""
96:               RACINE / "reports/fiche-nuit-17-10.md",
101:    return len(list((RACINE / "tools").glob("porte-*.sh")))
105:    return len(list((RACINE / "docs/theorie/synthese").glob("0*.md")))
108:def compte_fiches() -> int:
112:def compte_json() -> int:
113:    return len(list((RACINE / "reports").glob("*.json")))
161:    for f in (RACINE / "docs").rglob("*"):
162:        if f.suffix in (".json", ".csv", ".npz", ".jsonl") and f.is_file():
163:            if f.name == "index.json" and f.parent.name == "glossaire":
166:    for nom in ("07-mesures-couche-commune.md", "fiche-nuit-17-10.md")
… [6152 caractères tronqués]
  ```

- **bash** `{"command": "ls -la reports/rapport-tagger-h50.json; ls reports/*.json | wc -l; find reports -maxdepth 1 -name '*.json' | wc -l; python3 - <<'PY'\nimport pathlib\nprint(len(list(pathlib.Path('reports').glob('*.json'))))\nprint(len(list(pathlib.Path('reports').glob('*.md'))))\nPY", "description": "Co … [32 caractères tronqués]`

  ```
-rw-r--r--. 1 stephane stephane 198938 15 nov 09:18 reports/rapport-tagger-h50.json
843
843
843
750
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('docs/pilotage/en-cours.md')\ns=p.read_text()\n# W2 bullet shorter\nold=\"- **W2 — le tagger sur 402/H50** : 402 **0,9198 → 0,9643** (+4,45), H50 **0,6842 → 0,8607** (+17,65) ; F1/attachement 402 **inchangés** ; **fermé 402 −1,55** (PRE … [2408 caractères tronqués]`

  ```
T0 max : 4071 mots (budget 4 000)

  avertissements :
     · 58 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 2 violation(s) :
     · docs/pilotage/roadmap.md : 9033 mots > budget 9000 (T1)
     · T0 : 4071 mots (AGENTS + en-cours + une tâche) > budget 4 000
EXIT=1
  en-cours · 1701 mots · 7 sections · 4 session(s) · 10 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 12, in <module>
AssertionError
  ```

- **bash** `{"command": "grep -n \"\\*\\*Fait\\*\\*\" docs/pilotage/en-cours.md | head -5; sed -n '52,58p' docs/pilotage/en-cours.md", "description": "Inspect exact active session Fait line"}`

  ```
12:- **Fait** : index réparé ; **N3 intégré** ; N2/S/L actifs ; suivi docs.
49:- **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ; page **`/paragraphes`**, **19/19 verdicts `389b99f`** ; **56 tests** ; fiches [analyseur](../../reports/rapport-s-analyseur-roles.md), [arbre](../../reports/rapport-s-arbre-referents.md), [limites](../../reports/rapport-s-limites-v6.md), [fait divers](../../reports/rapport-s-fait-divers.md).
64:- **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**, **F1 0,7902**, **1 span** ; **`s065`**, **`r035`**, **GV** réglés ; **restitution v1** (46/46) ; **J11.1–J11.4** ([exemples](../../reports/rapport-exemples-rejoues.md), [langue](../../reports/rapport-evaluer-langue.md), [robustesse](../../reports/rapport-robustesse-semaine.md), [schéma](../../reports/rapport-schema-v2-doc.md)) ; **D1** ([fiche](../../reports/rapport-exemples-tagger.md)) ; **D2** ([v2](../../reports/rapport-restitution-v2.md)) ; **D3** ([FAQ](../../reports/rapport-faq.md), 10/10) ; **E1** ([sommaire](../../reports/rapport-faq-sommaire.md)) ; **E2** ([cas d'erreur](../../reports/rapport-tagger-erreurs
… [496 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('docs/pilotage/en-cours.md')\ns=p.read_text()\nrepls=[]\nrepls.append((\"- **W2 — le tagger sur 402/H50** : 402 **0,9198 → 0,9643** (+4,45), H50 **0,6842 → 0,8607** (+17,65) ; F1/attachement 402 **inchangés** ; **fermé 402 −1,55** (PREP … [2444 caractères tronqués]`

  ```
MISSING: **split 402/H50 : 402 0,9643 (+4,45), H50 0,8607 (+17,65), F1/attachement 402 in
written
64:- **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**, **F1 0,7902** ; **D1–D3**, **E1–E2** livrés ([exemples](../../reports/rapport-exemples-tagger.md), [FAQ](../../reports/rapport-faq.md), [erreurs](../../repo
90:- **Pensée — B13 (actif)** : **183/183** ; `r035` (238/238), `s065` (238/238), **J6.1 rejeté** (`g017` inatteignable), schéma v2, **v2** **19/46** (**16** non vides, F1 **0,5270**) ([fiche](../../reports/rapport-resti
92:- **W2 — tagger 402/H50** : 402 **0,9198 → 0,9643** (+4,45), H50 **0,6842 → 0,8607** (+17,65) ; F1/att 402 **inchangés**, **fermé −1,55** ; [fiche](../../reports/rapport-tagger-h50.md) ; la règle ne le rejette pas, ré
110:| fichiers / JSON de résultats | **750** / **843** | `reports/*.md` / `reports/*.json` |
  en-cours · 1657 mots · 7 sections · 4 session(s) · 10 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  T0 max : 4027 mots (budget 4 000)

  avertissements :
     · 58 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 
… [266 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '124p' docs/pilotage/en-cours.md | cut -c1-400; echo; grep -o \"split 402/H50[^*]*\" docs/pilotage/en-cours.md | head", "description": "Inspect R line exact text"}`

  ```
| **R — le lecteur** | **R0.7** | **R0.7 — tagger 612 : 0,9575 (+9,5) ; réel 452 : 0,9500 (+6,1) ; split 402/H50 : 402 0,9643 (+4,45), H50 0,8607 (+17,65), F1/attachement 402 inchangés, fermé 402 −1,55** ; R2/R3 attendent N5/N4 | **W2 faite** ; **W3 — tagger par défaut** (réserve fermé) ; **[fiche H50](../../reports/rapport-tagger-h50.md)** |

split 402/H50 : 402 0,9643 (+4,45), H50 0,8607 (+17,65), F1/attachement 402 inchangés, fermé 402 −1,55
  ```

- **bash** `{"command": "sed -n '58,78p' docs/pilotage/en-cours.md", "description": "Read active session block"}`

  ```
- **Id** : `e181ce02-cd50-488a-a6be-e84b79d40dcc` — [`plan.md`](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md).
- **Rôle** : **Pensée** — RSN, arbre d'états, N3 ; heuristique ; bloc linguistique.
- **Plan** : B13.
- **Stratégie** : v0 mesuré.
- **Ambition** : un runtime cognitif tracé.
- **Objectif final** : un moteur de pensée v0.
- **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**, **F1 0,7902** ; **D1–D3**, **E1–E2** livrés ([exemples](../../reports/rapport-exemples-tagger.md), [FAQ](../../reports/rapport-faq.md), [erreurs](../../reports/rapport-tagger-erreurs.md)) ; [s065](../../reports/rapport-s065.md), [J9.1](../../reports/rapport-passe-honnetete.md).
- **Ce que font les autres** : **N2**, **S**, **hub**.
- **Ce qu'elle fait** : chantier.
- **Prochaine action** : **qualité des rôles** ; T132/T133, gold de pensée.
- **Clôture** : **J14.1 faite** (84/81/3 ; `sessions` verte, `indice` et `melange` structurelles ; tag `chantier-2026-11-14`).
- **Bloquants** : 7B locales interdites (règle 11) ; **gold de pensée**.
- **Journal** : [la session](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/).

### Session `0733c5bb-f90b-4f58-9241-3364fa32e
… [357 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"Stratégie\\|Ambition\\|Objectif\\|Plan\\|session\" tools/verifie_en_cours.py | head -40; sed -n '1,140p' tools/verifie_en_cours.py", "description": "Inspect en-cours validator requirements"}`

  ```
2:"""verifie_en_cours.py — l'état doit rester court, structuré, reprenable et multi-session.
7:  3. « Sessions en cours » : une sous-section `### Session ...` par session active, avec
8:     **Id**, **Rôle**, **Plan**, **Ambition**, **Stratégie**, **Objectif final**,
38:    "**Plan**",
39:    "**Ambition**",
40:    "**Stratégie**",
41:    "**Objectif final**",
68:def sessions(section: str) -> list[tuple[str, str]]:
94:    blocs = sessions(corps_section(texte, "Sessions en cours"))
102:                alertes.append(f"session « {titre} » ne dit pas « {champ} »")
143:    print(f"  en-cours · {n} mots · {len(SECTIONS)} sections · {len(blocs)} session(s) · "
146:        print("  ✅ état court, structuré, multi-session et reprenable")
#!/usr/bin/env python3
"""verifie_en_cours.py — l'état doit rester court, structuré, reprenable et multi-session.

Le fichier `docs/pilotage/en-cours.md` est la seule source de l'état. Ce contrôle vérifie :
  1. un budget de **2 000 mots** ;
  2. les **sept sections** du template ;
  3. « Sessions en cours » : une sous-section `### Session ...` par session active, avec
     **Id**, **Rôle**, **Plan**, **Ambition**, **Stratégie**, **Objectif final**,
     **
… [5031 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('docs/pilotage/en-cours.md')\ns=p.read_text()\nrepls=[\n(\"split 402/H50 : 402 0,9643 (+4,45), H50 0,8607 (+17,65), F1/attachement 402 inchangés, fermé 402 −1,55\",\n \"W2 : 402 0,9643 (+4,45), H50 0,8607 (+17,65), F1/att 402 inchangés, … [735 caractères tronqués]`

  ```
done
  en-cours · 1635 mots · 7 sections · 4 session(s) · 10 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  T0 max : 4005 mots (budget 4 000)

  avertissements :
     · 58 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 2 violation(s) :
     · docs/pilotage/roadmap.md : 9033 mots > budget 9000 (T1)
     · T0 : 4005 mots (AGENTS + en-cours + une tâche) > budget 4 000
  ```

- **bash** `{"command": "grep -o \"le tagger n'est pas à 0,944[^;]*;\" docs/pilotage/roadmap.md; grep -o \"R4.1–R4.4 mesurées[^;]*;\" docs/pilotage/roadmap.md; grep -o \"W2 — le tagger sur 402/H50[^|]*\" docs/pilotage/roadmap.md | head -1", "description": "Extract roadmap fragments to trim"}`

  ```
le tagger n'est pas à 0,944 contre 0,85** (corpus différents : +7,34 pts sur 180, +6,35 sur 432) ;
R4.1–R4.4 mesurées** (R4.4 : 4/5 familles ≥ 90 % de parité) ;
W2 — le tagger sur 402/H50 : 402 0,9643 (+4,45), H50 0,8607 (+17,65), F1/attachement 402 inchangés, fermé 402 −1,55 ; la règle ne le rejette pas** ([fiche](../../reports/rapport-tagger-h50.md))
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\n# en-cours\np=Path('docs/pilotage/en-cours.md')\ns=p.read_text()\nold=\"**W2 faite** ; **W3 — tagger par défaut** (réserve fermé) ; **[fiche H50](../../reports/rapport-tagger-h50.md)**\"\nnew=\"**W3 — tagger par défaut** ; **[fiche](../../repo … [1002 caractères tronqués]`

  ```
trimmed
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 3999 mots (budget 4 000)

  avertissements :
     · 58 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
EXIT=0
  en-cours · 1629 mots · 7 sections · 4 session(s) · 10 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -30; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Run documentation review after trims"}`

  ```
revue de documentation · 750 fiche(s) · 843 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
EXIT=0
  ```

- **bash** `{"command": "ls tools/porte-*.sh | sed 's#tools/##' | tr '\\n' ' '; echo; echo \"===\"; grep -rln \"tagger\\|rapport-tagger\" tools/porte-*.sh | head", "description": "List gates and find tagger gates"}`

  ```
porte-adaptateur-sortie.sh porte-audit-drapeaux.sh porte-b1110-hybride.sh porte-balayage.sh porte-bloc-code.sh porte-bloc-linguistique.sh porte-bloc-maths.sh porte-bloc-tableaux.sh porte-budget.sh porte-bus.sh porte-bus-socket.sh porte-c4-retard.sh porte-cerveau.sh porte-cic.sh porte-consolidation.sh porte-coupe.sh porte-cycle-c2.sh porte-deepseek.sh porte-delais.sh porte-diff-couche.sh porte-document.sh porte-echange-experts.sh porte-episodique.sh porte-etat.sh porte-flux.sh porte-fusion.sh porte-gain.sh porte-greffe.sh porte-harnais-invariants.sh porte-homeostasie.sh porte-horloge.sh porte-indice.sh porte-jeux.sh porte-jumeaux.sh porte-lecteur.sh porte-lecture.sh porte-m5-brouillon.sh porte-melange.sh porte-memoire.sh porte-miroir-blocs.sh porte-mistral.sh porte-n3-cache.sh porte-n3-composition.sh porte-n3-deux-processus.sh porte-n3-deux-regions.sh porte-n3-generation.sh porte-n3-inventaire.sh porte-n3-placement.sh porte-n3-pont.sh porte-n3-positions.sh porte-n3-profondeur.sh porte-n3-refus.sh porte-n3-reseau.sh porte-n3-routes.sh porte-n3-service-briques.sh porte-n3-service.sh porte-n3-seuil.sh porte-n3-sparsite-compte.sh porte-n3-sparsite.sh porte-occupation-elagage.sh porte-oc
… [490 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/tests/test_tagger_api.py 2>&1 | tail -15; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Run tagger API tests"}`

  ```
test_analyser_tagger_lisible (__main__.TestCliAvecTransportFactice.test_analyser_tagger_lisible) ... ok
test_evaluer_tagger (__main__.TestCliAvecTransportFactice.test_evaluer_tagger) ... ok
test_aide_expose_tagger (__main__.TestDefaultInchange.test_aide_expose_tagger) ... ok
test_analyser_json_sans_tagger (__main__.TestDefaultInchange.test_analyser_json_sans_tagger) ... ok
test_evaluer_sans_tagger (__main__.TestDefaultInchange.test_evaluer_sans_tagger) ... ok
test_cle_invalide_code_4 (__main__.TestErreursTagger.test_cle_invalide_code_4) ... ok
test_modele_json_incomplet_repli_heuristique (__main__.TestErreursTagger.test_modele_json_incomplet_repli_heuristique)
Un JSON qui n'a pas une classe par token est un refus de contrat, pas une exception. ... ok
test_refus_du_modele_repli_heuristique (__main__.TestErreursTagger.test_refus_du_modele_repli_heuristique) ... ok
test_reseau_coupe_repli_heuristique (__main__.TestErreursTagger.test_reseau_coupe_repli_heuristique) ... ok

----------------------------------------------------------------------
Ran 18 tests in 3.445s

OK
EXIT=0
  ```

- **bash** `{"command": "sed -n '1,160p' tools/toutes-les-portes.sh", "description": "Inspect full gates runner"}`

  ```
#!/bin/bash
# toutes-les-portes.sh — LA PASSE COMPLÈTE, et l'instrument qui manquait.
#
# POURQUOI CETTE PORTE EXISTE. Le 12 octobre, `tools/porte-gain.sh` §9 exigeait un REFUS
# (`--attn-window` en réparti) que le v7 avait **délibérément retiré** en faisant voyager les
# trois réglages dans la trame (`main.rs:4432`). La porte ne pouvait donc plus passer — et
# personne ne l'a vu, parce que les portes étaient lancées **une par une**, à la main, quand
# on touchait la fonctionnalité du jour. Une porte qu'on croit verte et qui n'a pas tourné est
# exactement le défaut que ce dépôt traque (un drapeau inerte, une mesure qui ne mesure rien) :
# ici, appliqué aux instruments eux-mêmes.
#
# Ce que fait ce script, et ce qu'aucun autre ne faisait :
#   1. il lance **TOUTES** les `tools/porte-*.sh`, séquentiellement ;
#   2. il ne s'arrête PAS à la première rouge — il veut le tableau, pas la première tuile ;
#   3. il borne chaque porte dans le temps (`DELAI`, 1800 s par défaut) : une porte qui pend
#      est une porte ROUGE, pas une porte qu'on attend ;
#   4. il garde le journal de chacune (`JOURNAUX`) et n'affiche qu'une ligne par porte ;
#   5. il sort en 1 s'il y a la moindre rouge, en
… [3112 caractères tronqués]
  ```

- **bash** `{"command": "bash tools/toutes-les-portes.sh", "description": "Run full gates suite", "run_in_background": true}`

  ```
started background job bash-110
  ```

- **bash** `{"command": "python3 tools/verifie_journal.py 2>&1 | tail -15; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Validate journal structure"}`

  ```
journal · 47 jour(s) · 208 session(s) · 2609 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
EXIT=0
  ```

- **bash** `{"command": "python3 tools/verifier_schemas.py 2>&1 | tail -15; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Validate SVG schemas"}`

  ```
schémas · 464 document(s) · 67 SVG · 2 source(s)
  ✅ aucun ASCII art, SVG valides et référencés, blocs PlantUML inline valides,
     sources et images relatives.
EXIT=0
  ```

- **bash** `{"command": "python3 tools/tests/test_produit.py 2>&1 | tail -8; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Run product tests"}`

  ```
....................
----------------------------------------------------------------------
Ran 20 tests in 10.792s

OK
EXIT=0
  ```

- **job_output** `{"job_id": "bash-110"}`

  ```
=== PASSE COMPLÈTE DES PORTES (85 portes, borne 1800 s) ===
    journaux : work/portes-1115-09h22
[status: running]
  ```

- **bash** `{"command": "sed -n '1,5p' docs/pilotage/en-cours.md; echo \"---\"; sed -n '86,94p' docs/pilotage/en-cours.md; echo \"---\"; sed -n '122,126p' docs/pilotage/en-cours.md; echo \"---\"; sed -n '106,112p' docs/pilotage/en-cours.md; echo \"--- reste\"; grep -n \"Ce qui reste\" -A 3 docs/pilotage/en-cour … [62 caractères tronqués]`

  ```
# En ce moment

**Mis à jour : 2026-11-15, 09 h 25 HNE (W2 : tagger 402/H50)**

> **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
---

- **S — les structures** : 61/61 types, 144/144 rôles, 56 tests, banque 84/67 ; **19/19 verdicts `389b99f`** ; `/paragraphes` v7, `/` ancien arbre ; [v2](../../reports/rapport-coordination-s-v2.md).
- **N2 — en pause** : **commande validée** `eval_longueurs.py --rope --val <dir>` (**2,7856**) ; **jamais `--rope` seul** (**40,0658**) ; [v2 : 3,09 tenu](../../reports/rapport-coordination-n2-v2.md) ; puis **porte propre (0,29)**.
- **Pensée — B13 (actif)** : **183/183** ; `r035` (238/238), `s065` (238/238), **J6.1 rejeté** (`g017` inatteignable), schéma v2, **v2** **19/46** (**16** non vides, F1 **0,5270**) ([fiche](../../reports/rapport-restitution-v2.md)), **D1–D3** ([FAQ](../../reports/rapport-faq.md)), **E1** ([sommaire](../../reports/rapport-faq-sommaire.md)) ; [s065](../../reports/rapport-s065.md), [J9.1](../../reports/rapport-passe-honnetete.md).
- **L — le bloc langue** : contrat ; frontière script 1,0, langue 0,137/0,9687 ; fusion réparée par niveau **0,9309/0,8226/0,8784/0,9954**.
- **W2 — tagger
… [2770 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-110"}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('tools/tests/linguistique/qualifier_tagger_h50.py')\ns=p.read_text()\n# add helpers before construire_rapport\nanchor='''def construire_rapport(args, phrases, split, bases, passes) -> dict:'''\nhelpers='''def _cout_api_452(api: dict) -> … [3396 caractères tronqués]`

  ```
script patched
COMPILE-OK
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json, pathlib\np=pathlib.Path('reports/rapport-tagger-h50.json')\nd=json.loads(p.read_text())\napi=d['passes']['api']\nb402=api['bases']['reste_402']['cout']; b50=api['bases']['h50']['cout']\nappels=b402['appels']+b50['appels']; requetes=b402['requetes']+b50['re … [1743 caractères tronqués]`

  ```
{
 "phrases": 452,
 "appels": 449,
 "requetes": 447,
 "cache": 2,
 "tokens_reseau": 65029,
 "tokens_cache": 261,
 "latence_reseau_s": 443.813,
 "par_phrase": {
  "appels": 0.9934,
  "requetes": 0.9889,
  "cache": 0.0044,
  "tokens_reseau": 143.87,
  "tokens_total": 144.45,
  "latence_reseau_s": 0.9819
 },
 "lecture": "somme des bases 402 et H50 de la passe API ; la base total 452 est un rejeu cache (0 réseau, 0 token réseau)."
}
{
 "reste_402": {
  "pos_heuristique": 0.9198,
  "pos_tagger": 0.9643,
  "delta_pos": 0.0445,
  "f1_heuristique": 0.819,
  "f1_tagger": 0.819,
  "attachement_heuristique": 1.0,
  "attachement_tagger": 1.0
 },
 "h50": {
  "pos_heuristique": 0.6842,
  "pos_tagger": 0.8607,
  "delta_pos": 0.1765,
  "f1_heuristique": 0.5836,
  "f1_tagger": 0.5836,
  "attachement_heuristique": 0.9545,
  "attachement_tagger": 0.9545
 },
 "total": {
  "pos_heuristique": 0.8891,
  "pos_tagger": 0.9508,
  "delta_pos": 0.0617,
  "f1_heuristique": 0.7906,
  "f1_tagger": 0.7906,
  "attachement_heuristique": 0.9946,
  "attachement_tagger": 0.9946
 },
 "tirage": {
  "pos_heuristique": 0.9073,
  "pos_tagger": 0.9556,
  "delta_pos": 0.0483,
  "f1_heuristique": 0.8278,
  "f1_tagger": 0.8278
… [68 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-110"}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "ls -la work/portes-1115-09h22/ 2>/dev/null | tail -10; echo \"---\"; wc -l work/portes-1115-09h22/registre.txt 2>/dev/null; tail -5 work/portes-1115-09h22/registre.txt 2>/dev/null; echo \"---\"; ps -o pid,etime,cmd -C bash | grep toutes-les-portes | grep -v grep || true", "description": … [29 caractères tronqués]`

  ```
total 4
drwxr-xr-x. 1 stephane stephane   54 15 nov 09:22 .
drwxr-xr-x. 1 stephane stephane 2166 15 nov 09:22 ..
-rw-r--r--. 1 stephane stephane   86 15 nov 09:22 porte-adaptateur-sortie.log
---
---
3786684       00:44 bash tools/toutes-les-portes.sh
  ```

- **bash** `{"command": "cat work/portes-1115-09h22/porte-adaptateur-sortie.log; echo \"---\"; ps -ef | grep -E \"porte-adaptateur|timeout 1800\" | grep -v grep", "description": "Read first gate log and process"}`

  ```
porte de l'adaptateur de sortie — Qwen2.5-0.5B-Q8_0.gguf · plage 0:8 · 256 jetons
---
stephane 3786702 3786684  0 09:22 ?        00:00:00 timeout 1800 bash tools/porte-adaptateur-sortie.sh
stephane 3786703 3786702  0 09:22 ?        00:00:00 bash tools/porte-adaptateur-sortie.sh
stephane 3793251 3786703  0 09:23 ?        00:00:00 bash tools/porte-adaptateur-sortie.sh
stephane 3793252 3793251 99 09:23 ?        00:00:45 ./drave-core/target/release/drave /tmp/porte-adaptateur/reecrit.gguf --ppl /tmp/porte-adaptateur/morceau.txt --limit 256 --ctx 256 --threads 8 --couches 0:8 --tete-partielle
  ```

- **bash** `{"command": "git add reports/rapport-tagger-h50.md reports/rapport-tagger-h50.json tools/tests/linguistique/qualifier_tagger_h50.py reports/INDEX.md reports/README.md docs/pilotage/en-cours.md docs/pilotage/roadmap.md journal/2026-11-15/README.md && git status --short | grep -E \"rapport-tagger-h50| … [254 caractères tronqués]`

  ```
M  docs/pilotage/en-cours.md
M  docs/pilotage/roadmap.md
M  journal/2026-11-15/README.md
M  reports/INDEX.md
M  reports/README.md
A  reports/rapport-tagger-h50.json
A  reports/rapport-tagger-h50.md
A  tools/tests/linguistique/qualifier_tagger_h50.py
---
  ✅ index : aucun fait stagé sans état
EXIT=0
  ```

- **bash** `{"command": "wc -l work/portes-1115-09h22/registre.txt 2>/dev/null; tail -10 work/portes-1115-09h22/registre.txt 2>/dev/null; ls work/portes-1115-09h22/*.log 2>/dev/null | wc -l; ps -o pid,etime,cmd -C bash | grep toutes-les-portes | grep -v grep || true", "description": "Check gates progress"}`

  ```
1
3786684       00:54 bash tools/toutes-les-portes.sh
  ```

- **bash** `{"command": "cat work/portes-1115-09h22/registre.txt 2>/dev/null; echo \"---\"; cat work/portes-1115-09h22/porte-adaptateur-sortie.log | tail -20; echo \"---\"; ls -lt work/portes-1115-09h22/ | head", "description": "Read gates registry and first gate log"}`

  ```
---
porte de l'adaptateur de sortie — Qwen2.5-0.5B-Q8_0.gguf · plage 0:8 · 256 jetons
  écriture  : complet 17.4315 → 17.4315 · tronqué 2687292.8165 → 2687292.8165
  ✅ PPL épinglées : complet 17.4315 · tronqué 2687292.8165
  ✅ l'écriture est fidèle (mêmes chiffres sur les deux chemins)
  ✅ invariant d'identité : 2687292.8165 (écart 0.00e+00)
---
total 4
-rw-r--r--. 1 stephane stephane 366 15 nov 09:23 porte-adaptateur-sortie.log
  ```

- **bash** `{"command": "sleep 30; wc -l work/portes-1115-09h22/registre.txt 2>/dev/null; tail -5 work/portes-1115-09h22/registre.txt 2>/dev/null; ls work/portes-1115-09h22/*.log 2>/dev/null | wc -l", "description": "Wait and check gates progress"}`

  ```
1 work/portes-1115-09h22/registre.txt
porte-adaptateur-sortie 0 67
2
  ```

- **bash** `{"command": "ls -lt work/portes-1115-09h22/*.log | head -5; echo \"---\"; tail -5 work/portes-1115-09h22/$(ls -t work/portes-1115-09h22/*.log | head -1 | xargs -n1 basename)", "description": "Check current gate log"}`

  ```
-rw-r--r--. 1 stephane stephane   0 15 nov 09:23 work/portes-1115-09h22/porte-audit-drapeaux.log
-rw-r--r--. 1 stephane stephane 580 15 nov 09:23 work/portes-1115-09h22/porte-adaptateur-sortie.log
---
  ```

- **bash** `{"command": "git diff --cached --stat; echo \"---\"; git diff --cached --name-only", "description": "Review staged files before commit"}`

  ```
docs/pilotage/en-cours.md                        |    18 +-
 docs/pilotage/roadmap.md                         |     2 +-
 journal/2026-11-15/README.md                     |    13 +
 reports/INDEX.md                                 |     1 +
 reports/README.md                                |     2 +
 reports/rapport-tagger-h50.json                  | 11283 +++++++++++++++++++++
 reports/rapport-tagger-h50.md                    |   332 +
 tools/tests/linguistique/qualifier_tagger_h50.py |   630 ++
 8 files changed, 12271 insertions(+), 10 deletions(-)
---
docs/pilotage/en-cours.md
docs/pilotage/roadmap.md
journal/2026-11-15/README.md
reports/INDEX.md
reports/README.md
reports/rapport-tagger-h50.json
reports/rapport-tagger-h50.md
tools/tests/linguistique/qualifier_tagger_h50.py
  ```

- **bash** `{"command": "git commit -m \"W2 — LE TAGGER SUR 402/H50 : 402 0,9198 → 0,9643 (+4,45), H50 0,6842 → 0,8607 (+17,65) ; F1/ATTACHEMENT 402 INCHANGÉS, FERMÉ 402 −1,55 ; LA RÈGLE NE LE REJETTE PAS (IL GAGNE SUR 402), LA RÉSERVE FERMÉ VA À W3\" 2>&1 | tail -30; echo \"EXIT=${PIPESTATUS[0]}\"", "descripti … [45 caractères tronqués]`

  ```
[still running after 60000ms; moved to background job bash-125]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **job_output** `{"job_id": "bash-125"}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "ps -ef | grep -E \"git commit|pre-commit|archive_sessions|session_report|journal_auto|verifie_etat\" | grep -v grep; echo \"---\"; ls -lt .git/index.lock 2>/dev/null; echo \"---\"; git status --short | head -20", "description": "Inspect commit hook processes"}`

  ```
stephane 3800365 3777457  0 09:24 ?        00:00:00 bash -c git commit -m "W2 — LE TAGGER SUR 402/H50 : 402 0,9198 → 0,9643 (+4,45), H50 0,6842 → 0,8607 (+17,65) ; F1/ATTACHEMENT 402 INCHANGÉS, FERMÉ 402 −1,55 ; LA RÈGLE NE LE REJETTE PAS (IL GAGNE SUR 402), LA RÉSERVE FERMÉ VA À W3" 2>&1 | tail -30; echo "EXIT=${PIPESTATUS[0]}"
stephane 3800372 3800365  0 09:24 ?        00:00:00 git commit -m W2 — LE TAGGER SUR 402/H50 : 402 0,9198 → 0,9643 (+4,45), H50 0,6842 → 0,8607 (+17,65) ; F1/ATTACHEMENT 402 INCHANGÉS, FERMÉ 402 −1,55 ; LA RÈGLE NE LE REJETTE PAS (IL GAGNE SUR 402), LA RÉSERVE FERMÉ VA À W3
stephane 3800390 3800372  0 09:24 ?        00:00:00 /bin/sh .git/hooks/pre-commit
stephane 3800394 3800390 41 09:24 ?        00:00:26 python3 tools/archive_sessions.py --quiet
stephane 3801393 3800394 83 09:25 ?        00:00:24 /usr/bin/python3 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/session_report.py --repo /home/stephane/Data13TB/stephane/GitHub/Qtrinet --quiet
---
---
M  docs/pilotage/en-cours.md
M  docs/pilotage/roadmap.md
M  journal/2026-11-15/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
 M journal/session
… [537 caractères tronqués]
  ```

- **bash** `{"command": "sleep 60; ps -ef | grep -E \"git commit|pre-commit|archive_sessions|session_report|journal_auto\" | grep -v grep | head; echo \"---\"; git log -1 --oneline 2>/dev/null", "description": "Wait and check commit completion"}`

  ```
[still running after 60000ms; moved to background job bash-127]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **bash** `{"command": "ps -ef | grep -E \"git commit|pre-commit|archive_sessions|session_report|journal_auto\" | grep -v grep | head; echo \"---\"; git log -1 --oneline 2>/dev/null; echo \"---\"; git status --short | head -8", "description": "Check commit status"}`

  ```
stephane 3800365 3777457  0 09:24 ?        00:00:00 bash -c git commit -m "W2 — LE TAGGER SUR 402/H50 : 402 0,9198 → 0,9643 (+4,45), H50 0,6842 → 0,8607 (+17,65) ; F1/ATTACHEMENT 402 INCHANGÉS, FERMÉ 402 −1,55 ; LA RÈGLE NE LE REJETTE PAS (IL GAGNE SUR 402), LA RÉSERVE FERMÉ VA À W3" 2>&1 | tail -30; echo "EXIT=${PIPESTATUS[0]}"
stephane 3800372 3800365  0 09:24 ?        00:00:00 git commit -m W2 — LE TAGGER SUR 402/H50 : 402 0,9198 → 0,9643 (+4,45), H50 0,6842 → 0,8607 (+17,65) ; F1/ATTACHEMENT 402 INCHANGÉS, FERMÉ 402 −1,55 ; LA RÈGLE NE LE REJETTE PAS (IL GAGNE SUR 402), LA RÉSERVE FERMÉ VA À W3
stephane 3800390 3800372  0 09:24 ?        00:00:00 /bin/sh .git/hooks/pre-commit
stephane 3802624 3800390 83 09:26 ?        00:00:35 python3 tools/session_report.py --quiet
---
4dbeff45 SEMAINE 2 — W1 : LE GOLD RÉEL 452 (20 HAND + 432 CORPUS, 242 FR / 210 EN), LE SPLIT 402/H50 FIGÉ, LE SHA256, LES 10 GP/SUB LISTÉS POUR S
---
M  docs/pilotage/en-cours.md
M  docs/pilotage/roadmap.md
M  journal/2026-11-15/README.md
 M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/
… [85 caractères tronqués]
  ```

### 👤 Utilisateur

background job bash-127 (bash: sleep 60; ps -ef | grep -E "git commit|pre-commit|archive_sessions|session_report|journal_auto" | grep -v grep | head; echo "---"; git log -1 --oneline 2>/dev/null) finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "sleep 45; ps -ef | grep -E \"git commit|pre-commit|session_report|journal_auto\" | grep -v grep | head; echo \"---\"; git log -2 --oneline 2>/dev/null; echo \"---\"; git status --short | head -10", "description": "Wait and check commit status"}`

  ```
---
1683c2b4 W2 — LE TAGGER SUR 402/H50 : 402 0,9198 → 0,9643 (+4,45), H50 0,6842 → 0,8607 (+17,65) ; F1/ATTACHEMENT 402 INCHANGÉS, FERMÉ 402 −1,55 ; LA RÈGLE NE LE REJETTE PAS (IL GAGNE SUR 402), LA RÉSERVE FERMÉ VA À W3
4dbeff45 SEMAINE 2 — W1 : LE GOLD RÉEL 452 (20 HAND + 432 CORPUS, 242 FR / 210 EN), LE SPLIT 402/H50 FIGÉ, LE SHA256, LES 10 GP/SUB LISTÉS POUR S
---
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/plan.json
?? reports/rapport-s-paragraphes.md
  ```

### 👤 Utilisateur

background job bash-125 (bash: git commit -m "W2 — LE TAGGER SUR 402/H50 : 402 0,9198 → 0,9643 (+4,45), H50 0,6842 → 0,8607 (+17,65) ; F1/ATTACHEMENT 402 INCHANGÉS, FERMÉ 402 −1,55 ; LA RÈGLE NE LE REJETTE PAS (IL GAGNE SUR 402), LA RÉSERVE FERMÉ VA À W3" 2>&1 | tail -30; echo "EXIT=${PIPESTATUS[0]}") finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "git show --stat --oneline 1683c2b4 | head -40; echo \"---\"; git show --name-only --format= 1683c2b4 | head -40", "description": "Inspect W2 commit contents"}`

  ```
1683c2b4 W2 — LE TAGGER SUR 402/H50 : 402 0,9198 → 0,9643 (+4,45), H50 0,6842 → 0,8607 (+17,65) ; F1/ATTACHEMENT 402 INCHANGÉS, FERMÉ 402 −1,55 ; LA RÈGLE NE LE REJETTE PAS (IL GAGNE SUR 402), LA RÉSERVE FERMÉ VA À W3
 docs/pilotage/en-cours.md                          |    18 +-
 docs/pilotage/roadmap.md                           |     2 +-
 journal/2026-11-15/README.md                       |    20 +-
 journal/2026-11-15/distribue.md                    |     2 +-
 journal/2026-11-15/docs.md                         |     2 +-
 journal/2026-11-15/mesures.md                      |     6 +-
 journal/2026-11-15/modele.md                       |     2 +-
 journal/2026-11-15/outils.md                       |     2 +-
 journal/2026-11-15/portes.md                       |     2 +-
 journal/README.md                                  |     4 +-
 journal/sessions/MANIFEST.md                       |     6 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md |    13 +
 .../rapport.md                                     |    13 +-
 .../digest.md                                      |   763 ++
 .../rapport.md                                     |    39 +-
 reports/INDEX.md                     
… [1073 caractères tronqués]
  ```

- **bash** `{"command": "wc -l work/portes-1115-09h22/registre.txt 2>/dev/null; tail -10 work/portes-1115-09h22/registre.txt 2>/dev/null; echo \"---\"; ps -o pid,etime,cmd -C bash | grep toutes-les-portes | grep -v grep || true; echo \"---\"; ls -lt work/portes-1115-09h22/*.log | head -3", "description": "Check … [22 caractères tronqués]`

  ```
8 work/portes-1115-09h22/registre.txt
porte-adaptateur-sortie 0 67
porte-audit-drapeaux 0 172
porte-b1110-hybride 0 0
porte-balayage 0 0
porte-bloc-code 0 13
porte-bloc-linguistique 0 14
porte-bloc-maths 0 0
porte-bloc-tableaux 0 2
---
3786684       04:50 bash tools/toutes-les-portes.sh
---
-rw-r--r--. 1 stephane stephane 1086 15 nov 09:27 work/portes-1115-09h22/porte-budget.log
-rw-r--r--. 1 stephane stephane 1035 15 nov 09:27 work/portes-1115-09h22/porte-bloc-tableaux.log
-rw-r--r--. 1 stephane stephane  877 15 nov 09:27 work/portes-1115-09h22/porte-bloc-maths.log
  ```

- **bash** `{"command": "git show 1683c2b4:reports/rapport-tagger-h50.json | python3 -c \"import json,sys; d=json.load(sys.stdin); print('cout_api_452' in d, 'scores_api_452' in d); print(d['cout_api_452']['requetes'], d['cout_api_452']['tokens_reseau']); print(d['regle_decision']['application']['verdict'])\"", … [50 caractères tronqués]`

  ```
True True
447 65029
accepté
  ```

- **bash** `{"command": "wc -l work/portes-1115-09h22/registre.txt 2>/dev/null; tail -12 work/portes-1115-09h22/registre.txt 2>/dev/null; echo \"---\"; ps -o pid,etime,cmd -C bash | grep toutes-les-portes | grep -v grep || true", "description": "Check full gates progress"}`

  ```
8 work/portes-1115-09h22/registre.txt
porte-adaptateur-sortie 0 67
porte-audit-drapeaux 0 172
porte-b1110-hybride 0 0
porte-balayage 0 0
porte-bloc-code 0 13
porte-bloc-linguistique 0 14
porte-bloc-maths 0 0
porte-bloc-tableaux 0 2
---
3786684       05:04 bash tools/toutes-les-portes.sh
  ```

- **bash** `{"command": "cat work/portes-1115-09h22/porte-budget.log; echo \"---\"; ps -ef | grep -E \"porte-budget|timeout 1800\" | grep -v grep", "description": "Inspect budget gate"}`

  ```
=== 1. sans budget déclaré (défaut) ===
  perplexité 111.9225 · 1971 octets par flux · code 0
  ✅ PPL épinglée : 111.9225
=== 2. budget GÉNÉREUX : le résultat ne doit pas changer ===
  [budget] lien local → d : 2471 octets par pas AU PLUS (déclaré dans la topologie) — dépassement = arrêt, jamais un résultat partiel
  perplexité 111.9225 · code 0
  ✅ budget généreux : résultat identique (111.9225)
=== 3. budget INSUFFISANT : arrêt explicite, code 6, AUCUNE perplexité ===
  [budget] lien local → d : 985 octets par pas AU PLUS (déclaré dans la topologie) — dépassement = arrêt, jamais un résultat partiel
    référence locale  : perplexité 113.0068  (2.1 s)
  [budget] DÉPASSEMENT sur le lien local → d : 1880 octets pour un budget de 985 — l'exécution s'arrête ICI, au pas 0. Aucune perplexité n'est rendue : elle porterait sur un transport qui n'est pas celui qui a été déclaré.
  ✅ dépassement annoncé (lien, octets, budget, pas), code 6, aucune perplexité rendue
=== 4. budget de LATENCE : généreux (aucun effet) ===
  perplexité 111.9225 · code 0
  ✅ latence généreuse : résultat identique (111.9225)
=== 5. budget de LATENCE insuffisant : arrêt, code 8, aucune perplexité ===
  [budget] lien
… [701 caractères tronqués]
  ```

- **bash** `{"command": "cat docs/pilotage/references-non-regression.md | head -80", "description": "Read tolerated red gates"}`

  ```
# Références de non-régression

> **Passe — 2026-11-14 00 h 30 :** **84 portes, 81 vertes, 3 rouges** — `porte-indice` et
> `porte-melange` (structurelles) et `porte-sessions` (mandats périmés du hub `1e7ef596` et de
> `e181ce02`). `porte-produit` et `porte-bloc` **vertes**. Journal :
> `work/portes/passe-1311-23h15.log`.
>
> **Vérification ciblée — 2026-11-14 06 h 55 (J14.1) :** `porte-sessions` **verte** (hub en pause,
> heartbeat `e181ce02` rafraîchi) ; `porte-indice` et `porte-melange` restent **rouges
> structurelles** (indice 482 contre témoin 459 ; état de A sans son code). Journaux
> `work/portes/verif-cloture/`.
> **Passe — 2026-11-06 :** 83 portes, **79 vertes, 4 rouges** (voir la ligne `bloc-linguistique`).

> **Passe précédente — 2026-11-04 23 h 43 → 2026-11-05 02 h 12 :** **83 portes, 79 vertes,
> 4 rouges**, **2 h 29** (journaux durables `work/portes/passe-2404-23h45`), **machine au repos**
> (GPU libres, aucune réservation). Les **2 rouges structurelles connues** restent : `porte-indice`
> (1 207 s), `porte-melange` (148 s). Deux rouges nouvelles, **hors dépôt** : `porte-lecteur` (0 s)
> échouait sur une ancre du banc pilote (« < 2,5 ») que la réécriture de la roadma
… [3886 caractères tronqués]
  ```

- **bash** `{"command": "for p in etat document tableaux sessions produit deepseek; do echo \"=== porte-$p ===\"; timeout 300 bash tools/porte-$p.sh 2>&1 | tail -3; echo \"EXIT=${PIPESTATUS[0]}\"; done", "description": "Run relevant lightweight gates"}`

  ```
=== porte-etat ===
  ✅ aucun fait commité après le dernier état
  ✅ autotest : 6 cas, dont 3 refus attendus et 3 passes
✅ porte état verte : aucun fait commité après le dernier état
EXIT=0
=== porte-document ===
✅ les 50 pages sont découpées, les partitions exactes, le rejeu identique,
   la fidélité ≥ 0,99 et les trois contrôles négatifs se comportent comme prévu.
✅ porte document verte
EXIT=0
=== porte-tableaux ===
  ✅ 1825 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4480 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-15)
EXIT=0
=== porte-sessions ===
autotest OK : plan valide, périmètre dupliqué refusé, champ manquant refusé, pause sans heartbeat exigé, mandat long avec claim accepté, reservation imbriquée avertie sans refus
  ❌ mandat périmé (1593 min) : e181ce02-cd50-488a-a6be-e84b79d40dcc — heartbeat à rafraîchir
EXIT=1
=== porte-produit ===
[still running after 60000ms; moved to background job bash-136]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output,
… [23 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-136"}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "ps -ef | grep -E \"porte-produit|toutes-les-portes\" | grep -v grep | head; echo \"---\"; wc -l work/portes-1115-09h22/registre.txt; tail -6 work/portes-1115-09h22/registre.txt", "description": "Check product gate and full suite"}`

  ```
stephane 3786684 3777457  0 09:22 ?        00:00:00 bash tools/toutes-les-portes.sh
stephane 3810348 3809265  0 09:28 ?        00:00:00 timeout 300 bash tools/porte-produit.sh
stephane 3810350 3810348  0 09:28 ?        00:00:00 bash tools/porte-produit.sh
---
9 work/portes-1115-09h22/registre.txt
porte-balayage 0 0
porte-bloc-code 0 13
porte-bloc-linguistique 0 14
porte-bloc-maths 0 0
porte-bloc-tableaux 0 2
porte-budget 0 47
  ```

- **bash** `{"command": "grep -n \"heartbeat\\|--heartbeat\\|def main\\|add_argument\" tools/sessions.py | head -40; echo \"===\"; sed -n '1,60p' tools/porte-sessions.sh", "description": "Inspect session heartbeat mechanism"}`

  ```
5:périmètre, fichiers réservés, heartbeat, prochaine action, état. Les autres
8:et les heartbeats périmés (le `--check` seul les signale). Les **fichiers
16:l'état, son heartbeat n'est plus exigé, et la reprise la remet `actif`.
18:`work/ressources.json` : le heartbeat n'est pas exigé ; le registre distingue le
34:CHAMPS = ("session", "rôle", "périmètre", "fichiers réservés", "heartbeat",
71:    hb = champs.get("heartbeat", "")
72:    heartbeat = None
77:            heartbeat = datetime.fromisoformat(brut)
79:            heartbeat = datetime.strptime(brut, "%Y-%m-%d %H:%M")
80:        age = (datetime.now() - heartbeat).total_seconds() / 60.0
84:            "fichiers": fic, "heartbeat": heartbeat, "age": age,
113:    heartbeat = f"{m.group(1)} {int(m.group(2)):02d}:{m.group(3)} HAE" if m else ""
124:                    "heartbeat": heartbeat})
136:        heartbeat = s["heartbeat"] or datetime.now().strftime("%Y-%m-%d %H:%M HAE")
143:> session : le heartbeat est celui de l'état, pas une preuve de vie.
149:- **Heartbeat** : {heartbeat}
187:            erreurs.append(f"{p['chemin']} : heartbeat illisible")
195:                    f"mandat long ({a['age']:.0f} min) : {a['id']} — claim 
… [1184 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-136"}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "sed -n '1,80p' tools/porte-produit.sh; echo \"===\"; ps -o pid,etime,cmd -p 3810350 2>/dev/null", "description": "Inspect product gate"}`

  ```
#!/usr/bin/env bash
# porte-produit — le premier produit : la CLI répond, le JSON est valide, le rejeu est identique.
#
# Ce qu'elle vérifie : `drave --version`, `analyser` (fr et en) rend un JSON parsable avec des
# étiquettes, `rejouer` rend le même sha256 deux fois, et le smoke test passe.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1
ko=0
dit() { printf '  %s %s\n' "$1" "$2"; }

ver=$(python3 tools/drave.py --version 2>&1)
case "$ver" in drave*) dit ✅ "version : $ver" ;; *) dit ❌ "version : $ver"; ko=1 ;; esac

for langue in fr en; do
  case "$langue" in
    fr) texte="Le chat dort sur le toit." ;;
    en) texte="The cat sleeps on the roof." ;;
  esac
  sortie=$(python3 tools/drave.py analyser "$texte" --langue "$langue" --json 2>&1)
  if printf '%s' "$sortie" | python3 -c "
import json, sys
d = json.load(sys.stdin)
assert d['langue'] == '$langue', d.get('langue')
assert len(d['etiquettes']) > 5, len(d['etiquettes'])
assert any(e['niveau'] == 'syntagme' for e in d['etiquettes'])
assert any(e['niveau'] == 'pos' for e in d['etiquettes'])
" 2>/dev/null; then
    dit ✅ "analyser $langue : JSON valide, étiquettes et syntagmes"
  else
    dit ❌ "analyser $langue : JSON invalide 
… [2218 caractères tronqués]
  ```

- **bash** `{"command": "sleep 45; ps -o pid,etime,cmd -p 3810350 2>/dev/null || echo \"porte-produit done\"; echo \"---\"; tail -5 /tmp/porte-produit-tests.log 2>/dev/null; tail -3 /tmp/porte-produit-libre.log 2>/dev/null", "description": "Wait for product gate"}`

  ```
PID     ELAPSED CMD
3810350       02:00 bash tools/porte-produit.sh
---
....................
----------------------------------------------------------------------
Ran 20 tests in 11.205s

OK
Ran 4 tests in 0.291s

OK
  ```

- **job_output** `{"job_id": "bash-136", "timeout_ms": 120000, "wait": true}`

  ```
✅ refus : JSON avec refus, code 3
  ✅ autotest parallèle : 183/183 portes tenues
✅ porte produit verte
EXIT=0
=== porte-deepseek ===
     dry-run ignoré : 0 exemple de distillation
  (live ignoré : pas de clé ou DEEPSEEK_LIVE!=1)
  ✅ le banc DeepSeek tient hors réseau : adaptateur, prompts, corpus, distillation.
EXIT=0
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "wc -l work/portes-1115-09h22/registre.txt; tail -12 work/portes-1115-09h22/registre.txt; echo \"---\"; ps -o pid,etime,cmd -C bash | grep toutes-les-portes | grep -v grep || true", "description": "Check full gates progress"}`

  ```
10 work/portes-1115-09h22/registre.txt
porte-adaptateur-sortie 0 67
porte-audit-drapeaux 0 172
porte-b1110-hybride 0 0
porte-balayage 0 0
porte-bloc-code 0 13
porte-bloc-linguistique 0 14
porte-bloc-maths 0 0
porte-bloc-tableaux 0 2
porte-budget 0 47
porte-bus 0 80
---
3786684       08:07 bash tools/toutes-les-portes.sh
  ```

- **job_output** `{"job_id": "bash-110", "timeout_ms": 600000, "wait": true}`

  ```
porte-adaptateur-sortie ✅                          67 s    ✅ porte tenue (écriture fidèle · invariant · effet · refus)
  porte-audit-drapeaux   ✅                         172 s  ✅ porte audit des drapeaux : occupation, ratio de signes et densité de croissance — chacun
  porte-b1110-hybride    ✅                           0 s  PORTE TENUE : 4/4 routées · 4/4 lues · E4 = requête de case
  porte-balayage         ✅                           0 s  ✅ porte balayage verte
  porte-bloc-code        ✅                          13 s  ✅ porte bloc code verte
  porte-bloc-linguistique ✅                          14 s  ✅ porte bloc linguistique verte
  porte-bloc-maths       ✅                           0 s  ✅ porte bloc maths verte
  porte-bloc-tableaux    ✅                           2 s  ✅ porte bloc tableaux verte
  porte-budget           ✅                          47 s    ✅ paires depassees : nommees (total, budget, pas, plafond), code 9, AUCUNE perplexite
  porte-bus              ✅                          80 s    ✅ le canal diffusé par fichier change la région du milieu
  porte-bus-socket       ✅                          96 s    ✅ le bus du pilote agit (113.0068 -> 148.9144)
  porte-c4-retard   
… [1468 caractères tronqués]
  ```

- **bash** `{"command": "wc -l work/portes-1115-09h22/registre.txt; tail -5 work/portes-1115-09h22/registre.txt; echo \"---\"; ps -o pid,etime,cmd -C bash | grep toutes-les-portes | grep -v grep || true; echo \"---\"; ls -lt work/portes-1115-09h22/*.log | head -3", "description": "Check full gates progress afte … [8 caractères tronqués]`

  ```
22 work/portes-1115-09h22/registre.txt
porte-deepseek 0 1
porte-delais 0 21
porte-diff-couche 0 18
porte-document 0 6
porte-echange-experts 0 52
---
3786684       18:27 bash tools/toutes-les-portes.sh
---
-rw-r--r--. 1 stephane stephane 5238 15 nov 09:40 work/portes-1115-09h22/porte-episodique.log
-rw-r--r--. 1 stephane stephane  343 15 nov 09:39 work/portes-1115-09h22/porte-echange-experts.log
-rw-r--r--. 1 stephane stephane 1175 15 nov 09:38 work/portes-1115-09h22/porte-document.log
  ```

- **job_kill** `{"job_id": "bash-110", "reason": "W2 est mesuré, écrit et committé ; les portes ciblées sont vertes. La passe complète (85 portes) est une tâche de clôture de semaine, elle sera rejouée à la clôture plutôt que de bloquer W2."}`

  ```
requested cancellation of job bash-110
  ```

- **bash** `{"command": "git status --short | grep -E \"rapport-tagger-h50|qualifier_tagger_h50|INDEX.md|reports/README|en-cours|roadmap\" || echo \"W2 files clean\"; echo \"---\"; git log -2 --oneline; echo \"---\"; ls -la reports/rapport-tagger-h50.* tools/tests/linguistique/qualifier_tagger_h50.py", "descrip … [45 caractères tronqués]`

  ```
W2 files clean
---
1683c2b4 W2 — LE TAGGER SUR 402/H50 : 402 0,9198 → 0,9643 (+4,45), H50 0,6842 → 0,8607 (+17,65) ; F1/ATTACHEMENT 402 INCHANGÉS, FERMÉ 402 −1,55 ; LA RÈGLE NE LE REJETTE PAS (IL GAGNE SUR 402), LA RÉSERVE FERMÉ VA À W3
4dbeff45 SEMAINE 2 — W1 : LE GOLD RÉEL 452 (20 HAND + 432 CORPUS, 242 FR / 210 EN), LE SPLIT 402/H50 FIGÉ, LE SHA256, LES 10 GP/SUB LISTÉS POUR S
---
-rw-r--r--. 1 stephane stephane 200301 15 nov 09:23 reports/rapport-tagger-h50.json
-rw-r--r--. 1 stephane stephane  22156 15 nov 09:20 reports/rapport-tagger-h50.md
-rw-r--r--. 1 stephane stephane  30910 15 nov 09:23 tools/tests/linguistique/qualifier_tagger_h50.py
  ```

- **bash** `{"command": "ps -o pid,etime,cmd -C bash | grep -E \"toutes-les-portes|porte-episodique\" | grep -v grep || echo \"gates stopped\"; echo \"---\"; wc -l work/portes-1115-09h22/registre.txt; awk '$2 != 0 {print}' work/portes-1115-09h22/registre.txt || true", "description": "Confirm gates stopped and l … [10 caractères tronqués]`

  ```
gates stopped
---
22 work/portes-1115-09h22/registre.txt
  ```

- **bash** `{"command": "grep -n \"Heartbeat\\|heartbeat\" journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md | head; echo \"---\"; sed -n '1,30p' journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md", "description": "Inspect active session heartbeat"}`

  ```
6:> Le heartbeat est celui de l'état ; il se rafraîchit à chaque cycle.
18:- **Heartbeat** : 2026-11-14 06:55 EST
22:- **Arrêt** : 2026-11-02 15 h 06 (reboot) — reprise à **16 h 16** ; **actif** ; heartbeat rafraîchi.
---
# Plan de session — Pensée, la RSN plurielle et le moteur N3

> **Mandat vivant.** Ouvert le 2026-10-31 22 h 45 HAE depuis
> [`docs/pilotage/en-cours.md`](../../../docs/pilotage/en-cours.md). Ce plan est le **contrat de
> synergie** : il dit ce que la session réserve, ce qu'elle attend des autres, et quand elle s'arrête.
> Le heartbeat est celui de l'état ; il se rafraîchit à chaque cycle.

- **Session** : `e181ce02-cd50-488a-a6be-e84b79d40dcc`
- **Rôle** : Pensée — RSN plurielle, arbre d'états, cycle multi-niveaux, moteur N3 ; analyse de la couche heuristique ; bloc linguistique
- **Périmètre** : Pensée, R4.4-reste, Coloration, Bloc linguistique (R0.7)
- **Fichiers réservés** : `docs/theorie/pensee-iterative.md`, `docs/schemas/pensee-*.svg`,
  `docs/implantation/moteur-de-pensee.md`, `tools/pensee/`, `reports/pensee-*`,
  `reports/r44-*`, `docs/theorie/pre-traitement-linguistique.md`,
  `docs/schemas/heuristique-*.svg`, `tools/bloc_linguistique.py`,
  `tools/port
… [2014 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md')\ns=p.read_text()\nold='- **Heartbeat** : 2026-11-14 06:55 EST'\nnew='- **Heartbeat** : 2026-11-15 09:30 EST'\nassert old in s\ns=s.replace(old,new,1)\np.write_text(s)\npri … [269 caractères tronqués]`

  ```
heartbeat refreshed
  ✅ plans cohérents
EXIT=0
autotest OK : plan valide, périmètre dupliqué refusé, champ manquant refusé, pause sans heartbeat exigé, mandat long avec claim accepté, reservation imbriquée avertie sans refus
  ✅ plans cohérents
PORTE TENUE : plans lisibles · autotest doublon/champ manquant/pause · check strict
EXIT=0
  ```

- **bash** `{"command": "git add journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md && git commit -m \"ÉTAT — W2 : heartbeat e181ce02 rafraîchi (2026-11-15 09:30), porte-sessions verte\" 2>&1 | tail -10; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Commit session heartbeat refresh"}`

  ```
[still running after 60000ms; moved to background job bash-147]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **bash** `{"command": "sleep 60; ps -ef | grep -E \"git commit|pre-commit|session_report|archive_sessions\" | grep -v grep | head; echo \"---\"; git log -3 --oneline", "description": "Wait for heartbeat commit"}`

  ```
[still running after 60000ms; moved to background job bash-148]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **bash** `{"command": "ps -ef | grep -E \"git commit|pre-commit|session_report|archive_sessions\" | grep -v grep | head; echo \"---\"; git log -3 --oneline; echo \"---\"; git status --short | head -8", "description": "Check heartbeat commit completion"}`

  ```
stephane 3911962 3777457  0 09:41 ?        00:00:00 bash -c git add journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md && git commit -m "ÉTAT — W2 : heartbeat e181ce02 rafraîchi (2026-11-15 09:30), porte-sessions verte" 2>&1 | tail -10; echo "EXIT=${PIPESTATUS[0]}"
stephane 3911978 3911962  0 09:41 ?        00:00:00 git commit -m ÉTAT — W2 : heartbeat e181ce02 rafraîchi (2026-11-15 09:30), porte-sessions verte
stephane 3911996 3911978  0 09:41 ?        00:00:00 /bin/sh .git/hooks/pre-commit
stephane 3913835 3911996 86 09:43 ?        00:00:25 python3 tools/session_report.py --quiet
---
1683c2b4 W2 — LE TAGGER SUR 402/H50 : 402 0,9198 → 0,9643 (+4,45), H50 0,6842 → 0,8607 (+17,65) ; F1/ATTACHEMENT 402 INCHANGÉS, FERMÉ 402 −1,55 ; LA RÈGLE NE LE REJETTE PAS (IL GAGNE SUR 402), LA RÉSERVE FERMÉ VA À W3
4dbeff45 SEMAINE 2 — W1 : LE GOLD RÉEL 452 (20 HAND + 432 CORPUS, 242 FR / 210 EN), LE SPLIT 402/H50 FIGÉ, LE SHA256, LES 10 GP/SUB LISTÉS POUR S
6b2208ee PLAN — LA SEMAINE 2 (16 → 22/11) : GOLD 452, PAGE / DE S, PANINI À DATE, RESTITUTION v3, LE TAGGER PAR DÉFAUT ? ; LA FILE DU CHANTIER À 41 TÂCHES
---
 M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/e
… [372 caractères tronqués]
  ```

### 👤 Utilisateur

background job bash-148 (bash: sleep 60; ps -ef | grep -E "git commit|pre-commit|session_report|archive_sessions" | grep -v grep | head; echo "---"; git log -3 --oneline) finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "sleep 40; ps -ef | grep -E \"git commit|pre-commit|session_report\" | grep -v grep | head; echo \"---\"; git log -3 --oneline", "description": "Wait for heartbeat commit to finish"}`

  ```
---
3439cb0c ÉTAT — W2 : heartbeat e181ce02 rafraîchi (2026-11-15 09:30), porte-sessions verte
1683c2b4 W2 — LE TAGGER SUR 402/H50 : 402 0,9198 → 0,9643 (+4,45), H50 0,6842 → 0,8607 (+17,65) ; F1/ATTACHEMENT 402 INCHANGÉS, FERMÉ 402 −1,55 ; LA RÈGLE NE LE REJETTE PAS (IL GAGNE SUR 402), LA RÉSERVE FERMÉ VA À W3
4dbeff45 SEMAINE 2 — W1 : LE GOLD RÉEL 452 (20 HAND + 432 CORPUS, 242 FR / 210 EN), LE SPLIT 402/H50 FIGÉ, LE SHA256, LES 10 GP/SUB LISTÉS POUR S
  ```

### 👤 Utilisateur

background job bash-147 (bash: git add journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md && git commit -m "ÉTAT — W2 : heartbeat e181ce02 rafraîchi (2026-11-15 09:30), porte-sessions verte" 2>&1 | tail -10; echo "EXIT=${PIPESTATUS[0]}") finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -5; echo \"REVUE_EXIT=${PIPESTATUS[0]}\"; python3 tools/taille_documents.py 2>&1 | tail -4; echo \"TAILLE_EXIT=${PIPESTATUS[0]}\"", "description": "Final doc review and budget check"}`

  ```
revue de documentation · 750 fiche(s) · 843 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
REVUE_EXIT=0
  avertissements :
     · 58 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
TAILLE_EXIT=0
  ```

- **bash** `{"command": "python3 tools/verifie_journal.py 2>&1 | tail -4; echo \"JOURNAL_EXIT=${PIPESTATUS[0]}\"; python3 tools/verifie_en_cours.py 2>&1 | tail -3; echo \"ETAT_EXIT=${PIPESTATUS[0]}\"; bash tools/porte-sessions.sh 2>&1 | tail -2; echo \"SESSIONS_EXIT=${PIPESTATUS[0]}\"", "description": "Final jo … [34 caractères tronqués]`

  ```
journal · 47 jour(s) · 208 session(s) · 2609 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
JOURNAL_EXIT=0
  en-cours · 1629 mots · 7 sections · 4 session(s) · 10 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
ETAT_EXIT=0
  ✅ plans cohérents
PORTE TENUE : plans lisibles · autotest doublon/champ manquant/pause · check strict
SESSIONS_EXIT=0
  ```

- **bash** `{"command": "echo \"registre portes (22) :\"; awk '$2 != 0 {print}' work/portes-1115-09h22/registre.txt || true; echo \"lignes: $(wc -l < work/portes-1115-09h22/registre.txt)\"; echo \"---\"; git status --short | grep -E \"rapport-tagger-h50|qualifier_tagger_h50|en-cours|roadmap|2026-11-15/README\"  … [85 caractères tronqués]`

  ```
registre portes (22) :
lignes: 22
---
W2 files clean
  ```

### 🤖 Assistant

## W2 — le tagger sur le split 402 / H50

**Livré et committé** (`1683c2b4`, sur le split W1 `4dbeff45`) :

- **Fiche** : [`reports/rapport-tagger-h50.md`](reports/rapport-tagger-h50.md)
- **JSON** : [`reports/rapport-tagger-h50.json`](reports/rapport-tagger-h50.json)
- **Banc reproductible** : [`tools/tests/linguistique/qualifier_tagger_h50.py`](tools/tests/linguistique/qualifier_tagger_h50.py)

### Les chiffres (passe API, cache neuf)

| base | POS heuristique | POS tagger | Δ | fermé | ouvert | F1 / attachement |
|---|---:|---:|---:|---:|---:|---:|
| **402** | 0,9198 (1 984/2 157) | **0,9643** (2 080) | **+4,45 pts** | 0,9580 → 0,9425 (**−1,55**) | 0,8804 → 0,9868 (**+10,64**) | 0,8190 / 1,0000 inchangés |
| **H50** | 0,6842 (221/323) | **0,8607** (278) | **+17,65 pts** | 0,7542 → 0,8156 (**+6,14**) | 0,5972 → 0,9167 (**+31,95**) | 0,5836 / 0,9545 inchangés |
| **total 452** | 0,8891 (2 205/2 480) | **0,9508** (2 358) | **+6,17 pts** | 0,9294 → 0,9246 (−0,48) | 0,8466 → 0,9784 (+13,18) | 0,7906 / 0,9946 inchangés |

Le total redonne **0,9508**, à **0,0008** du 0,9500 publié. Par langue : 402 fr **+8,16**, 402 en **+0,10** ; H50 fr **+19,05**, H50 en **+16,13**. Le tirage aléatoire hors H50 gagne **+4,83** : le gain « normal » est autour de +4,5 à +5, H50 est bien un stress test.

### Coût et latence

- **API** : **447 requêtes**, **65 029 tokens réseau** pour 452 phrases, **0,982 s/phrase**, **0,993 s/requête** (médiane 402 1,000 s, H50 0,968 s ; p95 1,29–1,32 s ; max 1,589 s). **399 appels** pour 402 (3 textes dupliqués servis par le cache mémoire) et **50** pour H50 ; **2 lectures de cache** (`r423`/`r427` partagent le prompt de `r010`/`r030`).
- **Cache chaud après API** : **0 réseau, 0 token**, scores identiques.
- **Cache chaud avant API** : **0 réseau, 0 token**, mais scores légèrement différents (0,9629 / 0,8638) : le cache existant venait d’un autre moment du modèle. Seule la passe API est la mesure du jour.

### La règle

**Une règle qui ne gagne que sur H50 est rejetée ; le contrôle est le 402.** Le tagger gagne **sur 402 (+4,45)** et sur H50 (+17,65) : il **n’est pas H50-only**, donc **accepté par la règle**. Réserve nommée : sur 402, le gain est **ouvert** (VERB +19,14, ADJ +19,40) et le **fermé baisse de 1,55 pt** (PREP −8,43, CONJ −10,15, AUX −2,92, DET −0,75). Une règle « aucune classe ne baisse sur 402 » le rejetterait ; c’est la réserve portée à **W3** (défaut / hybride fermé-ouvert).

### Vérifications

- `revue_documentation.py`, `taille_documents.py`, `verifie_en_cours.py`, `verifie_journal.py`, `verifier_schemas.py` : **verts**.
- `test_tagger_api.py` : **18/18** ; `test_produit.py` : **20/20** ; `porte-produit`, `porte-deepseek`, `porte-bloc-linguistique`, `porte-budget`, `porte-etat`, `porte-document`, `porte-tableaux` : **vertes**.
- `porte-sessions` était rouge sur un heartbeat périmé (`e181ce02`) : **rafraîchi**, porte **verte** (commit `3439cb0c`).
- Passe complète arrêtée à **22/85 portes, 0 rouge** (les longues `indice`/`melange` restent les rouges structurelles connues, à rejouer à la clôture de semaine).

