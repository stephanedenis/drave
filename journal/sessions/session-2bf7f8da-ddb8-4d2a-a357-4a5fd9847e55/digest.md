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

