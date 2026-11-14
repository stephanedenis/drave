# Session DSH — relecture

- identifiant : `session-ce875934-0cf6-4434-a91d-cbca647b11b3`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-14 03:46:12
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche J10.1 : le bilan — relis les fiches du chantier, écris `reports/rapport-bilan-chantier.md` + JSON : les chiffres avant/après (POS, F1, attachement, le produit, Panini), les décisions, les rejets, les échecs (J1.2/J2.2/J3.1 : timeout après commit), ce qui reste pour la suite. Mets à jour `docs/pilotage/semaine-autonome.md`.

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

- **bash** `{"command": "pwd && ls -la && git log --oneline -15 && git status --short | head -50", "description": "Explore repository root and git state"}`

  ```
/home/stephane/Data13TB/stephane/GitHub/Qtrinet
total 208
drwxr-xr-x. 1 stephane stephane   686  6 nov 09:52 .
drwxr-xr-x. 1 stephane stephane  2532  5 nov 10:41 ..
-rw-r--r--. 1 stephane stephane  9977  3 nov 09:19 AGENTS.md
drwxr-xr-x. 1 stephane stephane    40 25 sep 15:38 bench
drwxr-xr-x. 1 stephane stephane    56 30 sep 12:20 colab
drwxr-xr-x. 1 stephane stephane  2664  2 nov 18:33 data
drwxr-xr-x. 1 stephane stephane   138  6 nov 10:08 docs
drwxr-xr-x. 1 stephane stephane    92 28 oct 16:25 drave-core
drwxr-xr-x. 1 stephane stephane   180 14 nov 03:46 .git
-rw-r--r--. 1 stephane stephane   619 31 oct 17:33 .gitignore
-rw-r--r--. 1 stephane stephane   225  1 nov 10:50 .gitmodules
drwxr-xr-x. 1 stephane stephane   972 14 nov 00:51 journal
drwxr-xr-x. 1 stephane stephane   100  3 nov 09:12 models
drwxr-xr-x. 1 stephane stephane   114 25 sep 15:24 __pycache__
drwxr-xr-x. 1 stephane stephane    64  6 nov 09:52 .pytest_cache
-rw-r--r--. 1 stephane stephane  4992 25 sep 10:54 Qtrinet-bootstrap.md
-rw-r--r--. 1 stephane stephane 21293  6 nov 22:32 README.md
drwxr-xr-x. 1 stephane stephane 75352 14 nov 03:27 reports
-rw-r--r--. 1 stephane stephane 13100 28 oct 14:59 REPRISE.md
-rw---
… [3433 caractères tronqués]
  ```

- **bash** `{"command": "ls -la docs/pilotage/ reports/ journal/ 2>/dev/null | head -80", "description": "List key directories"}`

  ```
docs/pilotage/:
total 232
drwxr-xr-x. 1 stephane stephane   298 14 nov 03:28 .
drwxr-xr-x. 1 stephane stephane   138  6 nov 10:08 ..
drwxr-xr-x. 1 stephane stephane  1686  4 nov 11:53 backlog
-rw-r--r--. 1 stephane stephane 26128 14 nov 01:05 chantiers.md
-rw-r--r--. 1 stephane stephane 12353 14 nov 03:29 en-cours.md
-rw-r--r--. 1 stephane stephane 12411 28 oct 09:17 manques.md
-rw-r--r--. 1 stephane stephane 34739  7 nov 00:50 plan-travail.md
-rw-r--r--. 1 stephane stephane 22138  1 nov 13:46 programme-r.md
-rw-r--r--. 1 stephane stephane  4380  2 nov 20:20 README.md
-rw-r--r--. 1 stephane stephane 14438 14 nov 01:16 references-non-regression.md
-rw-r--r--. 1 stephane stephane 53633 14 nov 03:28 roadmap.md
-rw-r--r--. 1 stephane stephane 15419 13 nov 23:05 semaine-autonome.md
-rw-r--r--. 1 stephane stephane 14336 28 oct 09:17 utilisation.md

journal/:
total 80
drwxr-xr-x. 1 stephane stephane   972 14 nov 00:51 .
drwxr-xr-x. 1 stephane stephane   686  6 nov 09:52 ..
drwxr-xr-x. 1 stephane stephane   132 28 oct 14:12 2026-09-25
drwxr-xr-x. 1 stephane stephane    36 28 oct 14:12 2026-09-26
drwxr-xr-x. 1 stephane stephane   144 28 oct 14:12 2026-09-27
drwxr-xr-x. 1 stephane stephane  
… [3379 caractères tronqués]
  ```

- **bash** `{"command": "cat tools/chantier/plan.json | head -200", "description": "Read chantier plan JSON"}`

  ```
{
 "nom": "Semaine 07/11 → 14/11 — le produit et l'intégration Panini",
 "principe": "Une tâche n'est finie que si son acceptation passe ; l'agent commite, le superviseur vérifie.",
 "taches": [
  {
   "id": "J0",
   "jour": 0,
   "titre": "Le contrôle du superviseur",
   "mandat": "Réponds exactement le mot OK, sans autre texte. C'est un test de liaison du superviseur.",
   "budget_min": 2,
   "acceptation": [
    {
     "commande": "python3 -c \"print('LIAISON-OK')\"",
     "attendu": "LIAISON-OK"
    }
   ]
  },
  {
   "id": "J1.1",
   "jour": 1,
   "titre": "r035 : la relative zéro",
   "mandat": "Tâche J1.1 du chantier : la relative zéro (r035, « The film she talks about is out. »). Reproduis, explique, propose UNE règle générale mesurée sur dev/test ; si elle tient (attachement 236→237, POS/F1 stables), intègre-la et commite avec une fiche `reports/rapport-r035.md` + `reports/pensee-r035.json`. Sinon, écris la fiche du rejet (chiffres, raison) et commite-la. Règles : ne touche pas S/D/N2 ; 183/183 portes ; en-cours à jour.",
   "budget_min": 90,
   "acceptation": [
    {
     "commande": "test -f reports/rapport-r035.md && echo FICHE-OK",
     "attendu": "FICHE-OK"
    },
   
… [7690 caractères tronqués]
  ```

- **bash** `{"command": "cat docs/pilotage/semaine-autonome.md", "description": "Read semaine-autonome doc"}`

  ```
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
| 1 
… [13735 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\np=json.load(open('tools/chantier/plan.json'))\nprint(p.get('nom'))\nprint(p.get('principe'))\nfor t in p['taches']:\n    print(t['id'], '|', t['titre'], '|', t.get('jour'))\nEOF", "description": "List tasks from plan JSON"}`

  ```
Semaine 07/11 → 14/11 — le produit et l'intégration Panini
Une tâche n'est finie que si son acceptation passe ; l'agent commite, le superviseur vérifie.
J0 | Le contrôle du superviseur | 0
J1.1 | r035 : la relative zéro | 1
J1.2 | La convention des GV | 1
J1.3 | Le schéma v2 | 1
J1.4 | La restitution v0 | 1
J2.1 | Panini I — la table atomes ↔ niveaux | 2
J2.2 | Panini I — le corpus commun | 2
J3.1 | Panini II — le retrieval à époque contrôlée | 3
J3.2 | Panini II — la généalogie à deux faces | 3
J4.1 | Coordination N2 — le mètre RoPE | 4
J4.2 | Coordination S — les 11 verdicts | 4
J4.3 | Coordination R — le tagger sur 612 | 4
J4.4 | Coordination A — A6.2 et A8.3b2 | 4
J5.1 | Le rapport de semaine | 5
J5.2 | La passe complète et le tag | 5
J6.1 | Le dernier span g017 | 6
J6.2 | La cible s065 | 6
J7.1 | Panini — le retrieval approfondi | 7
J8.1 | La restitution v1 | 8
J9.1 | La passe d'honnêteté des fiches | 9
J10.1 | Le bilan de la semaine | 10
J11.1 | Le produit — les exemples rejoués | 11
J11.2 | Le produit — la mesure par langue | 11
J11.3 | Le produit — la robustesse des 50 textes | 11
J11.4 | Le contrat — le schéma v2 documenté | 11
J12.1 | Panini — le §334 et les 44 œuvres | 1
… [134 caractères tronqués]
  ```

- **bash** `{"command": "cat docs/pilotage/en-cours.md", "description": "Read current state doc"}`

  ```
# En ce moment

**Mis à jour : 2026-11-14, 03 h 30 HNE (heure locale, EST).**

> **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
> plan plus bas (**La carte**).

### Session `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — le hub de reprise du 04/11

- **Id** : `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — [`plan.md`](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/plan.md).
- **Rôle** : **Hub de reprise** — état, docs, intégration, passe.
- **Fait** : index réparé ; **N3 intégré** ; N2/S/L actifs ; suivi docs (revue, liens, tableaux).
- **Prochaine action** : **suivi docs**, puis la **passe** après les runs.
- **Bloquants** : aucun.
- **Journal** : [la session](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/).

## Sessions en cours

> Contrat : [`continuite.md`](../methode/continuite.md) · sessions terminées :
> [`journal/sessions/`](../../journal/sessions/). Chaque session expose son mandat dans son
> `plan.md` (`python3 tools/sessions.py --status`). **Une session écrit l'état à la fois** :
> le hook pre-commit refuse un fait sans ligne d'état ; une session arrêtée passe `État : en pause`.
>
> **Règle 11** : serveurs loca
… [10864 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\np=json.load(open('tools/chantier/plan.json'))\nfor t in p['taches']:\n    if t['id'] in ('J5.1','J5.2','J6.1','J6.2','J7.1','J8.1','J9.1','J10.1'):\n        print('='*80)\n        print(t['id'], t['titre'], '| jour', t.get('jour'), '| budget', t.get('budg … [194 caractères tronqués]`

  ```
================================================================================
J5.1 Le rapport de semaine | jour 5 | budget 90
Tâche J5.1 : le rapport de semaine — relis les fiches des jours 1 à 4, écris `reports/rapport-semaine.md` + JSON : les chiffres avant/après (POS, F1, attachement, le produit, l'intégration), les décisions, les rejets, ce qui reste. Mets à jour `docs/pilotage/semaine-autonome.md` (l'état de chaque jour).
acceptation: [
 {
  "commande": "test -f reports/rapport-semaine.md && echo FICHE-OK",
  "attendu": "FICHE-OK"
 }
]
================================================================================
J5.2 La passe complète et le tag | jour 5 | budget 90
Tâche J5.2 : la passe complète des portes (`bash tools/toutes-les-portes.sh`), le relevé des rouges, la mise à jour de `docs/pilotage/references-non-regression.md`, et un **tag annoté** `semaine-2026-11-14` sur le dernier commit vert. Ne pas forcer : si des rouges non nommées apparaissent, écris la fiche et ne tague pas.
acceptation: [
 {
  "commande": "git tag -l 'semaine-2026-11-14'",
  "attendu": "semaine-2026-11-14"
 },
 {
  "commande": "python3 tools/revue_documentation.py >/dev/null 2>&1; echo REVUE-$?",
… [3690 caractères tronqués]
  ```

- **bash** `{"command": "git status --short && git diff --stat", "description": "Check working tree diff stats"}`

  ```
M reports/INDEX.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/plan.json
 m tools/structures
?? reports/rapport-s-paragraphes.md
 reports/INDEX.md                        |   4 +-
 reports/pensee-coherence-fiches-v7.json |  19 +
 reports/pensee-dev-test-v10.json        |   2 +-
 reports/pensee-quatre-modes.json        | 734 ++++++++++++++++++--------------
 reports/rapport-audit-v7.md             |   6 +-
 reports/rapport-coherence-fiches-v7.md  |  17 +-
 reports/rapport-dev-test-v10.md         |   2 +-
 reports/rapport-pensee-v12.md           |   4 +-
 reports/rapport-spans-chunker.md        |  13 +-
 tools/chantier/plan.json                | 116 +++++
 tools/structures                        |   0
 11 files changed, 579 insertions(+), 338 deletions(-)
  ```

- **bash** `{"command": "ls -la reports/ | grep -E 'rapport-(r035|convention-gv|schema-v2|restitution-v0|atomes|corpus-commun|retrieval-epoque|genealogie|coordination|g017|s065|retrieval-familles|restitution-v1|passe-honnetete|semaine|bilan)'", "description": "List relevant report files"}`

  ```
-rw-------. 1 stephane stephane   22407  7 nov 14:53 rapport-atomes-niveaux.md
-rw-------. 1 stephane stephane   15441 14 nov 03:26 rapport-convention-gv.md
-rw-------. 1 stephane stephane   17340 13 nov 22:59 rapport-coordination-a.json
-rw-------. 1 stephane stephane   31979 13 nov 22:59 rapport-coordination-a.md
-rw-r--r--. 1 stephane stephane   11915 13 nov 21:52 rapport-coordination-n2.json
-rw-r--r--. 1 stephane stephane   20149 13 nov 21:52 rapport-coordination-n2.md
-rw-r--r--. 1 stephane stephane   13019 13 nov 22:35 rapport-coordination-r.json
-rw-r--r--. 1 stephane stephane   22988 13 nov 22:36 rapport-coordination-r.md
-rw-------. 1 stephane stephane   18503 13 nov 21:58 rapport-coordination-s.json
-rw-------. 1 stephane stephane   17471 13 nov 21:58 rapport-coordination-s.md
-rw-------. 1 stephane stephane   21491  7 nov 15:16 rapport-corpus-commun.md
-rw-------. 1 stephane stephane   12948 14 nov 03:26 rapport-g017.md
-rw-r--r--. 1 stephane stephane   27574  7 nov 18:19 rapport-genealogie-deux-faces.md
-rw-------. 1 stephane stephane   10866 14 nov 03:29 rapport-passe-honnetete.md
-rw-------. 1 stephane stephane    7456 14 nov 03:26 rapport-r035.md
-rw-------. 1 steph
… [591 caractères tronqués]
  ```

- **bash** `{"command": "git tag -l && echo '---' && git log --oneline --decorate -30", "description": "List tags and recent commits"}`

  ```
---
81fc9ecf (HEAD -> s/v7) JOURNAL — 2026-11-14 : J9.1 AU RÉCIT (19 FICHES « INSTANTANÉ HISTORIQUE »)
ecef7250 J9.1 — PASSE D'HONNÊTETÉ : 19 FICHES « INSTANTANÉ HISTORIQUE », 4 CHIFFRES DÉPASSÉS NE SE LISENT PLUS COMME L'ÉTAT COURANT
229098ec J8.1 — RESTITUTION V1 : FORME CANONIQUE 46/46, MIROIR STRICT 0,1087 (NE MONTE PAS)
d31e8788 (origin/s/v7, origin/master, origin/HEAD, master) J7.1 — RETRIEVAL PAR FAMILLE : 532 TEXTES (445 LANGUES), SŒURS 0,619 VS 0,0445 (13,9×), J3.1 REPRODUIT ; PORTE D'ÉCRITURE, PUIS SŒUR > FAMILLE-AUTRE > ÉPOQUE
e4288023 J6.2 — PORTE PRODUIT VERTE (183/183) : FIXTURES D'ATTACHEMENT À 238/238, FICHE ET JSON À JOUR
2d6f5bff PORTES — LA PASSE DU 14/11 : 84 PORTES, 81 VERTES, 3 ROUGES (INDICE, MELANGE, SESSIONS DU HUB) ; MANDAT E181CE02 RAFRAÎCHI
6ecc9763 JOURNAL — 2026-11-14 : J6.2 AU RÉCIT (2 COMMITS, LE THÈME MESURES), s065 238/238
b6e474dc J6.2 — s065 : LA REL SUIVIE D'UN GV PREND LE SUJET DU GV (238/238 LABELS, 238/239 CIBLES, F1 0,7902 INCHANGÉ, 0 SPAN, 0 POS)
64d9dd23 J6.1 — g017 : LA RÈGLE DE L'ADVERBE FINAL HORS SUB EST REJETÉE (G017 GAGNÉ EN DEV, R264/R288 PERDUS EN TEST ; F1 0,7901, TEST −0,0028, ATTACHEMENT 236/237) ; CONVENTION DU GOLD À TRANCHER

… [2491 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-semaine.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-semaine.md</path>
<type>file</type>
<content>
1: # J5.1 — le rapport de semaine : le produit gagne 3,69 points de F1, l'intégration est bornée
2: 
3: > **Instantané historique** — les chiffres publiés ici sont ceux du commit de la fiche ; ils ne
4: > décrivent pas l'état courant. L'état courant du bloc est dans
5: > [`en-cours`](../docs/pilotage/en-cours.md) et [`la roadmap`](../docs/pilotage/roadmap.md).
6: 
7: > **Ligne de roadmap** : **B13** (le moteur de pensée), **R0.7** (le bloc langue), **N2**, **S**,
8: > **R**, **A**, **Panini** · **Tâche** : J5.1 · **Date** : 2026-11-13 · **Verdict** : ✅
9: >
10: > **Ce que ce rapport est.** La **relecture consolidée** des fiches des jours 1 à 4 : les chiffres
11: > avant/après, les décisions, les rejets et ce qui reste. **Aucune mesure nouvelle** : chaque
12: > chiffre est celui de sa fiche, avec sa base, son contrôle négatif et sa limite.
13: >
14: > **Base.** Gold vivant **612 phrases / 239 cibles / 3 179 jetons** ; POS heuristique **0,8625** ;
15: > F1 **0,7533** au départ de la semaine ; commits J1–J3 `25a6c0ff` → `c2e629b3` ; fiches J4 du
16: > **13/11** (HEAD `dc
… [29226 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-g017.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-s065.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-g017.md</path>
<type>file</type>
<content>
1: # B13 — g017 : l'adverbe final hors de la SUB est rejeté (g017 gagné, r264 et r288 perdus)
2: 
3: > **Instantané historique** — les chiffres publiés ici sont ceux du commit de la fiche ; ils ne
4: > décrivent pas l'état courant. L'état courant du bloc est dans
5: > [`en-cours`](../docs/pilotage/en-cours.md) et [`la roadmap`](../docs/pilotage/roadmap.md).
6: 
7: > **Ligne de roadmap** : **B13** (moteur de pensée) · **Tâche** : J6.1 · **Date** : 2026-11-14 ·
8: > **Verdict** : ❌ **règle rejetée**.
9: > La règle demandée — **l'adverbe final de temps hors de la SUB** — corrige bien `g017`
10: > (`that she would come` au lieu de `that she would come yesterday`) et retire un faux positif
11: > de `g005`, mais elle **casse `r264`** (`qu'il vient demain`) et **`r288`**
12: > (`that he comes tomorrow`) : **F1 0,7902 → 0,7901 (−0,0001)**, **dev +0,0011**, **test
13: > −0,0028**, **attachement 237/238 → 236/237**, **couverture 0,9958 → 0,9916**. Les deux cas
14: > favorables sont en **dev**, les deux cas défavorables en **test** : le gain est in-sample, la
15: > perte est hors é
… [12488 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-s065.md</path>
<type>file</type>
<content>
1: # B13 — s065 : la REL « qui commence » est attachée au sujet du GV qui la suit
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée) · **Tâche** : J6.2 · **Date** : 2026-11-14 ·
4: > **Verdict** : ✅ **règle intégrée**.
5: > La cible `s065` (« elle qui commence nage ») attend `elle` ; le bloc prédisait `nage`, le GV
6: > le plus proche. La règle **« REL suivie d'un GV → le sujet de ce GV »** corrige la cible
7: > **sans toucher un seul span, ni une seule POS** : **F1 0,7902 inchangé**, **attachement
8: > 237/238 → 238/238 labels** (238/239 cibles, **0,9958**), **exactitude sur les spans
9: > 0,9958 → 1,0**. Le gain est **en dev** ; le test ne contient aucun cas déclencheur et reste
10: > à **76/76**. La règle est intégrée avec un test unitaire, la porte du bloc est verte.
11: >
12: > **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (règle intégrée),
13: > [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) (`charger`, `evaluer_bloc`),
14: > [`gold_split.py`](../tools/tests/linguistique/gold_split.py) ; copies locales dans
15: >
… [11173 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-retrieval-familles.md", "limit": 220}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-restitution-v1.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-retrieval-familles.md</path>
<type>file</type>
<content>
1: # J7.1 — Le retrieval approfondi par famille Glottolog
2: 
3: > **Ligne de roadmap** : R0.7 (le bloc langue) / L · **Chantier** : Panini, J7.1 · **Date** : 2026-11-14
4: > **Verdict** : ✅ **le retrieval retrouve la famille, mais seulement dans la même écriture — et il faut
5: > des sœurs pour le voir.** Sur les 532 textes UDHR (445 langues distinctes après déduplication, 1948),
6: > le top-1 de voisinage est de la même famille dans **66,1 %** des cas (hasard 10,3 %) et de la même
7: > branche (sœur) dans **26,1 %** (hasard 2,5 %). Mais **hors écriture, tout retombe au hasard** :
8: > famille 9,9 % contre 8,1 %, sœur 0,7 % contre 0,8 %. Dans la même écriture, la famille monte à
9: > **69,8 %** (hasard 16,2 %) et la sœur à **27,8 %** (hasard 5,7 %). Le retrieval parallèle 30 articles
10: > le confirme et le chiffre : sur les **25 langues LANG_TREE** disponibles, les sœurs valent **0,619**
11: > (60 paires), les mêmes familles d'une autre branche **0,170** (216), les familles différentes
12: > **0,0445** (324) — **13,9×**, Δ **+0,574** [0,490 ; 0,655], coef
… [14625 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-restitution-v1.md</path>
<type>file</type>
<content>
1: # B13 — la restitution v1 : la forme canonique à 46/46, le miroir strict reste à 0,1087
2: 
3: > **Ligne de roadmap** : **B13** (produit) · **Tâche** : J8.1 · **Date** : 2026-11-14 ·
4: > **Verdict** : ✅
5: >
6: > **La question.** Au-delà de la surface exacte (46/46), produire une **forme canonique**
7: > depuis l'annotation — **segments + rôles + cibles** — et la mesurer : le **miroir strict**
8: > (0,1087) doit-il monter ?
9: >
10: > **La réponse.** **Non — et il ne doit pas.** Le miroir strict compare une sortie à la
11: > **surface brute** ; la forme canonique replie la casse, retire la ponctuation et réduit
12: > les espaces. Contre la source canonisée, elle est exacte **46/46 = 1,0000** ; contre la
13: > source brute, elle tombe à **1/46 = 0,0217** (seul `f18`, `1234567890`, n'a ni casse ni
14: > ponctuation). Le **miroir strict reste 5/46 = 0,1087** : la v1 ne fabrique pas de
15: > surface, elle mesure autre chose. Le chiffre utile de la v1 est **1,0000 canonique**,
16: > pas 0,1087 strict.
17: >
18: > **Le chiffre.** 46 annotations, **46/46 formes ca
… [13140 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-passe-honnetete.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-passe-honnetete.md</path>
<type>file</type>
<content>
1: # Passe d'honnêteté — 19 fiches portent « instantané historique », les quatre chiffres dépassés ne se lisent plus comme l'état courant
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée) · **Tâche** : J9.1 · **Date** : 2026-11-14 ·
4: > **Verdict** : ✅
5: >
6: > **Ce que la passe fait.** Les fiches qui publient l'instantané **POS 85 / F1 0,7535 / 236/237 /
7: > 2 spans** portent désormais un encart **« instantané historique »** qui ne recopie **aucune
8: > valeur** : il renvoie à [`en-cours`](../docs/pilotage/en-cours.md) et à
9: > [`la roadmap`](../docs/pilotage/roadmap.md). Dix encarts qui copiaient un état devenu faux sont
10: > réécrits ; neuf sont ajoutés.
11: >
12: > **Le chiffre.** **19/19** fiches annotées, **19/19** encarts en ligne 3, **38/38** liens qui
13: > résolvent. Après la passe, **0 fiche de résultats** ne publie un des quatre marqueurs sans
14: > mention, hors **2 faux positifs nommés** (`2 spans` de phrase, autre unité) et les index.
15: >
16: > **État courant, mesuré à HEAD `229098ec`** (J8.1 ; le produit n'a pas bougé depuis `b6
… [10288 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '220,513p' reports/rapport-retrieval-familles.md", "description": "Read rest of retrieval-familles report"}`

  ```
exacts (retirés) ; restent `cnr`/`hrv` 0,917, `bos_cyrl`/`srp_cyrl` 0,909, `pes_1`/`pes_2` 0,887,
`041`/`lav` 0,860, `046`/`ind` 0,840 (sœurs), `cjy`/`hsn` 0,791 (même famille, autre branche),
`glg`/`spa` 0,763 (sœurs), `dan`/`nob` 0,737 (sœurs). Les **20 paires les plus proches sont toutes
de la même famille** : dans le global, la proximité maximale est d'abord une proximité de famille et
d'écriture. Les paires de **familles différentes** ne remontent qu'avec l'écriture partagée (voir
§ 4.2 : `arb`/`pes_1` 0,567, `jpn`/`cmn_hant` 0,500).

### 4.2 LANG_TREE 25 — les sœurs dominent, et le coefficient de famille était dilué

**25 langues, 600 paires ordonnées, 30 articles.** Top-1 moyen **0,1471** ; même écriture **0,3480** ;
écriture différente **0,0357** (proche du hasard 0,0333). Le 2×2 :

| | même écriture | écriture différente |
|---|---:|---:|
| **sœurs** | **0,7360** (50) | 0,0333 (10) |
| **même famille, autre branche** | **0,3760** (86) | 0,0333 (130) |
| **familles différentes** | **0,0684** (78) | 0,0370 (246) |

La ligne des sœurs est le résultat : **0,619** toutes écritures, **0,736** à écriture contrôlée, contre
**0,0445** pour les familles différentes (toutes) et **0,0
… [17545 caractères tronqués]
  ```

- **bash** `{"command": "ls -la tools/chantier/ && find tools/chantier -maxdepth 2 -type f | head -50", "description": "List chantier tooling files"}`

  ```
total 36
drwxr-xr-x. 1 stephane stephane    46  7 nov 10:42 .
drwxr-xr-x. 1 stephane stephane 17608 14 nov 01:59 ..
-rw-r--r--. 1 stephane stephane 18388 13 nov 23:05 plan.json
-rw-r--r--. 1 stephane stephane 13450  7 nov 14:16 superviseur.py
tools/chantier/superviseur.py
tools/chantier/plan.json
  ```

- **bash** `{"command": "grep -rn \"J10.1\\|bilan-chantier\" --include=*.md --include=*.json --include=*.py . 2>/dev/null | head -40", "description": "Search for J10.1 references"}`

  ```
./tools/chantier/plan.json:298:   "id": "J10.1",
./tools/chantier/plan.json:301:   "mandat": "Tâche J10.1 : le bilan — relis les fiches du chantier, écris `reports/rapport-bilan-chantier.md` + JSON : les chiffres avant/après (POS, F1, attachement, le produit, Panini), les décisions, les rejets, les échecs (J1.2/J2.2/J3.1 : timeout après commit), ce qui reste pour la suite. Mets à jour `docs/pilotage/semaine-autonome.md`.",
./tools/chantier/plan.json:305:     "commande": "test -f reports/rapport-bilan-chantier.md && echo FICHE-OK",
./journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md:60969:  [a_faire ] J10.1  j10 — Le bilan de la semaine
./journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md:61520:  [a_faire ] J10.1  j10 — Le bilan de la semaine
  ```

- **bash** `{"command": "find . -maxdepth 3 -iname '*chantier*' -o -iname '*superviseur*' | grep -v '.git/' | head -40; ls -la work/ 2>/dev/null | head -40", "description": "Find chantier state files"}`

  ```
./tools/__pycache__/carte_chantiers.cpython-313.pyc
./tools/carte_chantiers.py
./tools/chantier
./tools/chantier/superviseur.py
./docs/schemas/chantiers-decision.svg
./docs/schemas/chantiers-vision.svg
./docs/methode/chantier-autonome.md
./docs/pilotage/chantiers.md
./work/chantier
total 220
drwxr-xr-x. 1 stephane stephane  1856 14 nov 03:29 .
drwxr-xr-x. 1 stephane stephane   686  6 nov 09:52 ..
-rwxr-xr-x. 1 stephane stephane  2133  2 nov 16:46 attente_portes.sh
drwxr-xr-x. 1 stephane stephane    82 13 nov 21:38 chantier
drwxr-xr-x. 1 stephane stephane   168  7 nov 15:06 corpus-commun
-rw-r--r--. 1 stephane stephane  6879  1 nov 12:49 corpus-wiki-langues.log
-rw-r--r--. 1 stephane stephane  1004  1 nov 11:14 corpus-wiki.log
-rw-r--r--. 1 stephane stephane  3985  1 nov 12:49 corpus-wiki-reste.log
drwxr-xr-x. 1 stephane stephane     8  1 nov 18:44 dr
-rw-r--r--. 1 stephane stephane   479  2 nov 20:32 entete-references.txt
-rw-------. 1 stephane stephane  5759  2 nov 01:21 finaliser_ocr.py
-rw-r--r--. 1 stephane stephane  9625  3 nov 05:55 hub-nuit.md
drwxr-xr-x. 1 stephane stephane   200  7 nov 18:06 j32
drwxr-xr-x. 1 stephane stephane   312 14 nov 01:34 j71
-rw-r--r--. 1 stephane 
… [1613 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' tools/chantier/superviseur.py", "description": "Read supervisor script start"}`

  ```
#!/usr/bin/env python3
"""superviseur.py — le méta-harnais du chantier autonome : file de tâches, exécution, vérification.

**Le problème.** DSH donne l'**agent** : des rounds, une session reprenable (`--session-id`), la
compaction du contexte, des sous-agents. Il **ne donne pas** la couche de contrôle d'un chantier de
plusieurs jours : file de tâches persistante, vérification d'acceptation **indépendante** de
l'agent, budget, reprise après crash, escalade, journal d'audit. Ce superviseur est cette couche.

**Les trois garanties.**
1. **Une tâche n'est finie que si son acceptation passe** — une commande, un attendu, exécutés par
   le superviseur, pas par l'agent.
2. **Rien n'est perdu** : l'état (`work/chantier/etat.json`) et le journal (`work/chantier/journal.log`)
   sont écrits après **chaque** étape ; une relance reprend la première tâche non finie.
3. **On s'arrête proprement** : le fichier `work/chantier/STOP` (ou le budget, ou le nombre de
   tâches) arrête la boucle ; l'agent n'est jamais tué au milieu d'un commit.

**Usage.**
    python3 tools/chantier/superviseur.py etat          # où en est-on ?
    python3 tools/chantier/superviseur.py prochaine     # la prochaine tâch
… [3389 caractères tronqués]
  ```

- **bash** `{"command": "cat work/chantier/etat.json", "description": "Read supervisor state"}`

  ```
{
 "taches": {
  "J1.1": {
   "titre": "r035 : la relative zéro",
   "statut": "fait",
   "debut": "2026-11-07 12:41:17",
   "duree_s": 1347.7,
   "code_agent": 0,
   "acceptation": [
    "✅ test -f reports/rapport-r035.md && echo FICHE-OK",
    "✅ python3 tools/revue_documentation.py >/dev/null 2>&1; echo REVUE-$?"
   ],
   "sortie_agent": "avant | après |\n|---|---:|---:|\n| exact / labels | 236/237 | **237/238** |\n| couverture | 0,9916 | **0,9958** |\n| POS | 0,8625 | **0,8625** |\n| F1 syntagmes | 0,7533 | **0,7549** |\n| dev exact / labels | 160/161 | **161/162** |\n| test exact / labels | 76/76 | **76/76** |\n\n`r035` est en dev ; le test ne bouge pas (il ne contient pas de relative zéro). Une seule phrase sur 612 change, **0 POS modifiée sur 3 179 tokens**.\n\n**Contrôles négatifs** : pas de REL devant `about the book`, `about it`, `about today`, sans pronom sujet, ni en français. Généralisation : « The book **he reads about** is good. » → REL [9:23], cible `book`. **183/183** portes, 17 tests unitaires, `porte-bloc-linguistique` et `porte-produit` vertes.\n\n**Intégration.** `tools/bloc_linguistique.py` (`relative_zero`), test unitaire `test_relative_zero`, valeurs d’attac
… [28786 caractères tronqués]
  ```

- **bash** `{"command": "cat work/chantier/journal.log 2>/dev/null | tail -80; echo '---'; ls -la work/chantier/", "description": "Read supervisor journal"}`

  ```
2026-11-07 10:42:52 · ⏹ STOP demandé
2026-11-07 10:44:20 · ↺ J1.1 remise en file
2026-11-07 10:45:08 · ↺ J1.1 remise en file
2026-11-07 10:45:46 · ▶ J0 — Le contrôle du superviseur (timeout 240 s)
2026-11-07 10:45:48 · ✘ J0 en 2.2 s (code 1) — ✅ python3 -c "print('LIAISON-OK')"
2026-11-07 10:47:58 · ↺ J0 remise en file
2026-11-07 10:47:58 · ▶ J0 — Le contrôle du superviseur (timeout 300 s)
2026-11-07 10:48:02 · ✔ J0 en 3.5 s (code 0) — ✅ python3 -c "print('LIAISON-OK')"
2026-11-07 12:18:48 · ▶ J1.1 — r035 : la relative zéro (timeout 5400 s)
2026-11-07 12:41:17 · ✔ J1.1 en 1347.7 s (code 0) — ✅ test -f reports/rapport-r035.md && echo FICHE-OK; ✅ python3 tools/revue_documentation.py >/dev/null 2>&1; echo REVUE-$?
2026-11-07 12:41:17 · ▶ J1.2 — La convention des GV (timeout 5400 s)
2026-11-07 14:11:35 · ✘ J1.2 en 5400.1 s (code 124) — ✅ test -f reports/rapport-convention-gv.md && echo FICHE-OK; ✅ bash tools/porte-bloc-linguistique.sh 2>&1 | tail -1
2026-11-07 14:11:35 · ▶ J1.3 — Le schéma v2 (timeout 5400 s)
2026-11-07 14:26:08 · ✔ J1.3 en 873.4 s (code 0) — ✅ test -f tools/schemas/drave-annotation-v2.json && echo V2-OK; ✅ python3 tools/verifier_schema_produit.py --gold 20 >/dev/null 
… [3828 caractères tronqués]
  ```

- **bash** `{"command": "git show -s --format='%H%n%an <%ae>%n%ad%n%s%n%b' c3467170; echo '===='; git show -s --format='%H%n%an <%ae>%n%ad%n%s%n%b' 92652984; echo '===='; git show -s --format='%H%n%an <%ae>%n%ad%n%s%n%b' 229098ec", "description": "Inspect commit metadata for timeout tasks"}`

  ```
c3467170b1d7001f09e0e6e9aa966aaccbf59077
Stéphane <stephane@localhost>
Sat Nov 7 18:12:33 2026 -0500
PANINI — J2.2 ET J3.1 : LE CORPUS COMMUN (418/438 PAIRES EXACTES, 8/8 CONTRÔLES) ET LE RETRIEVAL À ÉPOQUE CONTRÔLÉE (SCRIPT +0,609, ÉPOQUE −0,034/SIÈCLE, p=0,19)

====
9265298475b5ce49260eb6110ee40faa10eed2ea
Stéphane <stephane@localhost>
Sat Nov 7 13:44:53 2026 -0500
B13 — LA CONVENTION DES GV : SUJET HORS DU GV + ADVERBE FINAL, F1 0,7549 → 0,7902, ATTACHEMENT 237/238 ; 183/183

====
229098ecb3915486d5378076cdd2a5ea9ef4b665
Stéphane <stephane@localhost>
Sat Nov 14 03:23:33 2026 -0500
J8.1 — RESTITUTION V1 : FORME CANONIQUE 46/46, MIROIR STRICT 0,1087 (NE MONTE PAS)
`restituer --canonique` construit la forme canonique (segments, rôles, cibles) depuis
l'annotation, sans lire la surface. Contre la source canonisée : 46/46 formes exactes
(1,0000), 395 segments, 395 rôles, 315 cibles dont 315 résolues. Contre la source brute :
1/46 (0,0217). Le miroir strict reste 5/46 (0,1087) : la v1 ne fabrique pas de surface.

Contrôles : mélange et troncature canoniques 0/46, détection 46/46 ; rôles/cibles retirés,
clé changée 43/43. Limite : stabilité structurelle 18/46 ; le test ne couvre pas la 
… [92 caractères tronqués]
  ```

- **bash** `{"command": "git log --format='%h %ad %s' --date=format:'%Y-%m-%d %H:%M' --since='2026-11-07' --until='2026-11-15' | tail -40", "description": "Show chantier commit timeline"}`

  ```
81fc9ecf 2026-11-14 03:40 JOURNAL — 2026-11-14 : J9.1 AU RÉCIT (19 FICHES « INSTANTANÉ HISTORIQUE »)
ecef7250 2026-11-14 03:32 J9.1 — PASSE D'HONNÊTETÉ : 19 FICHES « INSTANTANÉ HISTORIQUE », 4 CHIFFRES DÉPASSÉS NE SE LISENT PLUS COMME L'ÉTAT COURANT
229098ec 2026-11-14 03:23 J8.1 — RESTITUTION V1 : FORME CANONIQUE 46/46, MIROIR STRICT 0,1087 (NE MONTE PAS)
d31e8788 2026-11-14 01:41 J7.1 — RETRIEVAL PAR FAMILLE : 532 TEXTES (445 LANGUES), SŒURS 0,619 VS 0,0445 (13,9×), J3.1 REPRODUIT ; PORTE D'ÉCRITURE, PUIS SŒUR > FAMILLE-AUTRE > ÉPOQUE
e4288023 2026-11-14 01:19 J6.2 — PORTE PRODUIT VERTE (183/183) : FIXTURES D'ATTACHEMENT À 238/238, FICHE ET JSON À JOUR
2d6f5bff 2026-11-14 01:16 PORTES — LA PASSE DU 14/11 : 84 PORTES, 81 VERTES, 3 ROUGES (INDICE, MELANGE, SESSIONS DU HUB) ; MANDAT E181CE02 RAFRAÎCHI
6ecc9763 2026-11-14 01:08 JOURNAL — 2026-11-14 : J6.2 AU RÉCIT (2 COMMITS, LE THÈME MESURES), s065 238/238
b6e474dc 2026-11-14 01:06 J6.2 — s065 : LA REL SUIVIE D'UN GV PREND LE SUJET DU GV (238/238 LABELS, 238/239 CIBLES, F1 0,7902 INCHANGÉ, 0 SPAN, 0 POS)
64d9dd23 2026-11-14 00:52 J6.1 — g017 : LA RÈGLE DE L'ADVERBE FINAL HORS SUB EST REJETÉE (G017 GAGNÉ EN DEV, R264/R288 PERDUS EN T
… [3218 caractères tronqués]
  ```

- **bash** `{"command": "git show -s --format='%s%n%b' 2d6f5bff; echo '===='; git show -s --format='%s%n%b' ced21933; echo '===='; git show -s --format='%s%n%b' 229098ec", "description": "Inspect gate pass and phase 2 commits"}`

  ```
PORTES — LA PASSE DU 14/11 : 84 PORTES, 81 VERTES, 3 ROUGES (INDICE, MELANGE, SESSIONS DU HUB) ; MANDAT E181CE02 RAFRAÎCHI

====
CHANTIER — PHASE 2 (12 H) : LE VERDICT ACCEPTATION D'ABORD (TIMEOUT APRÈS COMMIT = FAIT), 12 TÂCHES AJOUTÉES (J4 COORDINATION, J6 SPANS, J7-J10 PANINI/BILAN), ÉTAT CORRIGÉ

====
J8.1 — RESTITUTION V1 : FORME CANONIQUE 46/46, MIROIR STRICT 0,1087 (NE MONTE PAS)
`restituer --canonique` construit la forme canonique (segments, rôles, cibles) depuis
l'annotation, sans lire la surface. Contre la source canonisée : 46/46 formes exactes
(1,0000), 395 segments, 395 rôles, 315 cibles dont 315 résolues. Contre la source brute :
1/46 (0,0217). Le miroir strict reste 5/46 (0,1087) : la v1 ne fabrique pas de surface.

Contrôles : mélange et troncature canoniques 0/46, détection 46/46 ; rôles/cibles retirés,
clé changée 43/43. Limite : stabilité structurelle 18/46 ; le test ne couvre pas la sémantique.
Tests restitution 22/22 ; fiche reports/rapport-restitution-v1.md, JSON associé.
  ```

- **bash** `{"command": "sed -n '1,80p' docs/pilotage/references-non-regression.md; echo '...'; grep -n \"indice\\|melange\\|sessions\\|84\" docs/pilotage/references-non-regression.md | head -30", "description": "Read tolerated red references"}`

  ```
# Références de non-régression

> **Passe — 2026-11-14 00 h 30 :** **84 portes, 81 vertes, 3 rouges** — `porte-indice` et
> `porte-melange` (structurelles, antérieures) et `porte-sessions` (le mandat du hub
> `1e7ef596`, périmé de 9 jours ; le mien est rafraîchi). `porte-produit` **verte**, `porte-bloc`
> **verte**. Journal : `work/portes/passe-1311-23h15.log`.
> **Passe — 2026-11-06 :** 83 portes, **79 vertes, 4 rouges** (voir la ligne `bloc-linguistique`).

> **Passe précédente — 2026-11-04 23 h 43 → 2026-11-05 02 h 12 :** **83 portes, 79 vertes,
> 4 rouges**, **2 h 29** (journaux durables `work/portes/passe-2404-23h45`), **machine au repos**
> (GPU libres, aucune réservation). Les **2 rouges structurelles connues** restent : `porte-indice`
> (1 207 s), `porte-melange` (148 s). Deux rouges nouvelles, **hors dépôt** : `porte-lecteur` (0 s)
> échouait sur une ancre du banc pilote (« < 2,5 ») que la réécriture de la roadmap du 04/11
> (« sous 2,5 ») avait rendue introuvable — **corrigée et rejouée verte** ; `porte-sessions` (0 s)
> signale les heartbeats périmés du hub et de `e181ce02` au moment de la passe — le hub l'a rafraîchi
> à 01 h 55, **`e181ce02` reste à rafraîchir par sa s
… [5607 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,200p' docs/methode/resultats.md", "description": "Read results method doc"}`

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
… [2500 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\np=json.load(open('reports/rapport-semaine.json'))\nprint(json.dumps(p, ensure_ascii=False, indent=1)[:8000])\nEOF", "description": "Inspect week report JSON structure"}`

  ```
{
 "titre": "J5.1 — le rapport de semaine : le produit gagne 3,69 points de F1, l'intégration est bornée",
 "version": 1,
 "date": "2026-11-13",
 "tache": "J5.1",
 "lignes_roadmap": [
  "B13",
  "R0.7",
  "N2",
  "S",
  "R",
  "A",
  "Panini"
 ],
 "statut": "consolide",
 "base": {
  "gold_phrases": 612,
  "gold_cibles": 239,
  "pos_jetons": 3179,
  "pos_heuristique": 0.8625,
  "f1_depart": 0.7533,
  "commits_j1_j3": [
   "25a6c0ff",
   "92652984",
   "9a259953",
   "8eb0cc49",
   "9c7f71dc",
   "c3467170",
   "c2e629b3"
  ],
  "head_j4": "dc78f223",
  "note": "Aucune mesure nouvelle : ce rapport relit les fiches des jours 1 à 4."
 },
 "chiffres": {
  "produit": {
   "pos": {
    "production_avant": 0.8625,
    "production_apres": 0.8625,
    "delta": 0.0,
    "jetons": 3179,
    "jetons_changes": 0,
    "lecture": "J1.1 et J1.2 sont des regles de syntagmes ; la POS ne bouge pas."
   },
   "f1": {
    "avant": {
     "all": 0.7533,
     "dev": 0.7476,
     "test": 0.7663,
     "lineaire": 0.812
    },
    "apres": {
     "all": 0.7902,
     "dev": 0.7875,
     "test": 0.7962,
     "lineaire": 0.8144
    },
    "delta": {
     "all": 0.0369,
     "dev": 0.0399,
     "test": 0.0299,
 
… [6798 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\np=json.load(open('reports/rapport-semaine.json'))\nfor k in p:\n    print(k, '->', type(p[k]).__name__, (list(p[k]) if isinstance(p[k], dict) else len(p[k]) if isinstance(p[k], list) else p[k]))\nprint('--- decisions sample')\nprint(json.dumps(p.get('deci … [324 caractères tronqués]`

  ```
titre -> str J5.1 — le rapport de semaine : le produit gagne 3,69 points de F1, l'intégration est bornée
version -> int 1
date -> str 2026-11-13
tache -> str J5.1
lignes_roadmap -> list 7
statut -> str consolide
base -> dict ['gold_phrases', 'gold_cibles', 'pos_jetons', 'pos_heuristique', 'f1_depart', 'commits_j1_j3', 'head_j4', 'note']
chiffres -> dict ['produit', 'tagger', 'integration', 'coordination']
decisions -> list 13
rejets -> list 21
reste -> list 12
chronologie -> list 10
limites -> list 10
fichiers -> dict ['nouveaux', 'relus_j1', 'relus_j2_j3', 'relus_j4', 'mis_a_jour', 'non_modifies']
--- decisions sample
[
 {
  "id": "D1",
  "objet": "Adopter la relative zero a preposition orpheline",
  "preuve": "237/238, couverture 0,9958 ; 5 controles negatifs ; generalisation The book he reads about",
  "etat": "fait",
  "suite": "g017 reste"
 },
 {
  "id": "D2",
  "objet": "Adopter sujet hors du GV + adverbe final de temps etroit ; rejeter l'adverbe large et l'objet hors GV",
  "preuve": "F1 0,7902, 0 perte d'attachement ; placebo 0,7758 ; adverbe large 0,7552",
  "etat": "fait",
  "suite": "objet 75 FP / 51 FN ouvert"
 }
]
--- rejets sample
[
 {
  "id": "R1",
  "objet": "Adverb
… [2813 caractères tronqués]
  ```

- **bash** `{"command": "date '+%Y-%m-%d %H:%M:%S %Z'; echo '---'; tail -5 work/chantier/boucle2.log", "description": "Check current date and supervisor log tail"}`

  ```
2026-11-14 03:47:05 EST
---
 "sortie_agent": "e plus aucune valeur : il pointe vers `en-cours` et `roadmap`, ce qui le rend durable.\n\n### État courant mesuré (HEAD `229098ec`, avant nos commits)\n| gold | POS | F1 | attachement | spans sans label |\n|---|---:|---:|---:|---:|\n| vivant 612 | **0,8625** | **0,7902** | **238/238 labels (238/239 cibles)** | **1** (`g017`) |\n| gelé 602 | **0,8625** | **0,7882** | **234/239** | **1** |\n\n### Contrôles\n- **19/19** notices en ligne 3, **38/38** liens résolus.\n- **0 fiche de résultats** ne publie un des quatre marqueurs sans mention, hors **2 faux positifs nommés** (`2 spans` de phrase) et les index.\n- `rapport-s065.md` (état courant) n'est **pas** annotée : la frontière historique/courant est explicite.\n\n### Portes\nVertes : `revue_documentation` (`REVUE-0`), `porte-tableaux`, `taille_documents` (T0 dans le budget), `verifie_en_cours`, `verifie_journal`, `porte-produit` (183/183).\nLa passe complète des 84 portes a été lancée : **14/14 vertes** avant arrêt (elle durait ~70 min et un autre passage tournait déjà en parallèle).\n\n### Commits\n- `229098ec` — **J8.1** : restitution v1 (travail antérieur non committé, vérifié et commit
… [455 caractères tronqués]
  ```

- **bash** `{"command": "git status --short; echo '---diff names'; git diff --name-only; echo '---untracked'; git ls-files --others --exclude-standard | head -30", "description": "Check working tree precisely"}`

  ```
M reports/INDEX.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/plan.json
 m tools/structures
?? reports/rapport-s-paragraphes.md
---diff names
reports/INDEX.md
reports/pensee-coherence-fiches-v7.json
reports/pensee-dev-test-v10.json
reports/pensee-quatre-modes.json
reports/rapport-audit-v7.md
reports/rapport-coherence-fiches-v7.md
reports/rapport-dev-test-v10.md
reports/rapport-pensee-v12.md
reports/rapport-spans-chunker.md
tools/chantier/plan.json
tools/structures
---untracked
reports/rapport-s-paragraphes.md
  ```

- **bash** `{"command": "ls tools/ | grep -E 'index|revue|journal|tableau|taille|en_cours|schemas' | head -40; echo '---'; grep -n \"INDEX\" tools/index_reports.py 2>/dev/null | head -20", "description": "Find index/review tools"}`

  ```
bloc_tableaux.py
extraire_tableaux.py
index_reports.py
index_spans.py
index_wiki_en.py
journal_auto.py
porte-bloc-tableaux.sh
porte-tableaux.sh
revue_documentation.py
schemas
taille_documents.py
verifie_en_cours.py
verifie_journal.py
verifier_schemas.py
---
2:"""index_reports.py — génère reports/INDEX.md à partir des en-têtes de fiches.
5:avec son titre (premier `# `). Les fichiers d'infrastructure (`README.md`, `INDEX.md`
10:    python3 tools/index_reports.py              # réécrit reports/INDEX.md
32:        if p.name not in ("README.md", "INDEX.md") and not p.name.startswith("historique-")
42:        "> d'infrastructure (`README.md`, `INDEX.md`, `historique-*`) sont exclus du tableau ;",
53:    ap = argparse.ArgumentParser(description="Génère reports/INDEX.md (déterministe).")
61:    sortie = RACINE / "reports/INDEX.md"
67:    print(f"  {len(fiches())} fiches → reports/INDEX.md")
  ```

- **bash** `{"command": "sed -n '1,120p' docs/pilotage/roadmap.md", "description": "Read roadmap head"}`

  ```
# La roadmap de [Drave](../theorie/glossaire/entrees/drave.md) — un seul plan, quatre chantiers

> **Un seul document de plan.** Le **moteur** (A), l'**intelligence** (B), le **natif** (N) et le **lecteur** (R).
> L'ordre se décide par la **valeur** et les **dépendances**, jamais par une date. Les chiffres, les séries et les
> contrôles vivent dans [`reports/`](../../reports/) ; ici : l'[état](../theorie/glossaire/entrees/etat.md), la prochaine action, et ce qui bloque.
>
> **Détail et histoire** : l'ancien plan [A/B](../theorie/glossaire/entrees/a-b.md) est archivé dans
> [`roadmap-detail-2026-10-29.md`](../archive/roadmap-detail-2026-10-29.md), le détail N dans
> [`roadmap-native-2026-10-29.md`](../archive/roadmap-native-2026-10-29.md). Les **fiches de fonctionnalité** sont
> dans [`backlog/index.md`](backlog/index.md) ; le **graphe des dépendances** est dans
> [`backlog/dependances.md`](backlog/dependances.md). La **page vivante** est [`en-cours.md`](en-cours.md).

## Comment lire cette roadmap

- **Les états** : ✅ mesuré et écrit · 🔬 en cours · ⏳ à faire · 🧱 bloqué par une infra absente.
- **Le carpe diem** : pas d'échéance. Un chantier est **[fait](../theorie/glossaire/entrees
… [19035 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,80p' reports/INDEX.md; echo '...'; grep -n \"rapport-semaine\\|rapport-passe-honnetete\\|rapport-restitution-v1\" reports/INDEX.md reports/README.md | head -20", "description": "Inspect reports index and README"}`

  ```
# Index des fiches de reports/

> **Généré** par `tools/index_reports.py` — **719 fiches**. Les fichiers
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
… [9606 caractères tronqués]
  ```

- **bash** `{"command": "git diff reports/INDEX.md | head -40; echo '---'; head -40 reports/rapport-s-paragraphes.md", "description": "Check INDEX diff and untracked report"}`

  ```
diff --git a/reports/INDEX.md b/reports/INDEX.md
index 5506faf4..e5dd4473 100644
--- a/reports/INDEX.md
+++ b/reports/INDEX.md
@@ -1,6 +1,6 @@
 # Index des fiches de reports/
 
-> **Généré** par `tools/index_reports.py` — **718 fiches**. Les fichiers
+> **Généré** par `tools/index_reports.py` — **719 fiches**. Les fichiers
 > d'infrastructure (`README.md`, `INDEX.md`, `historique-*`) sont exclus du tableau ;
 > la page d'état, elle, compte tous les `.md` de `reports/`.
 
@@ -669,6 +669,7 @@
 | [rapport-regle-placement-perte.md](rapport-regle-placement-perte.md) | A8.3 — la règle place et perte choisit le KV comme la main |
 | [rapport-replis-cible.md](rapport-replis-cible.md) | B13 — les trois retouches A3 sur le live : +1, +2, +1, et 145/145 exact/top1 |
 | [rapport-restitution-v0.md](rapport-restitution-v0.md) | B13 — la restitution v0 : 46/46 surfaces exactes, le miroir strict à 0,1087 |
+| [rapport-restitution-v1.md](rapport-restitution-v1.md) | B13 — la restitution v1 : la forme canonique à 46/46, le miroir strict reste à 0,1087 |
 | [rapport-restitution.md](rapport-restitution.md) | B18 — restitution canonique : 528/528, mais pas un décodeur |
 | [rapport-retrieval-epoque.md]
… [3956 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,160p' tools/revue_documentation.py", "description": "Read documentation review script"}`

  ```
#!/usr/bin/env python3
"""revue_documentation.py — LA REVUE DE FIN DE SOUS-CHANTIER (AGENTS.md §4).

Ce qu'elle vérifie, et qu'il faut corriger AVANT le commit de clôture :
  1. classement : pas de résultats dans docs/ (les fiches sont dans reports/ et citées) ;
  2. structure  : les sept chantiers de en-cours.md ont leur entrée, leur état et leur fiche ;
  3. annotation : les liens relatifs des docs/ et reports/ résolvent, et leur libellé ne
     ment pas sur la cible ; les sources externes sont citées ;
  4. fraîcheur  : en-cours.md date du dernier commit, ET aucun fait n'a été commité après
     le dernier état (comparaison de commits, pas de dates : voir verifie_etat_a_jour.py) ;
  5. cohérence  : la synthèse (index.md) liste les huit chapitres, le chapitre 7 et B10–B12 ;
     les compteurs de la page d'état sont ceux du disque (portes, chapitres, fiches, docs) ;
  6. vocabulaire : « jeton » ne désigne **jamais** la représentation sémantique neutre (RSN) ;
  7. navigation : aucun document vivant n'est orphelin, et aucun chemin en code inline
     ne pointe vers un fichier absent (hors gabarits `AAAA`, `<...>`, `*`).

Sortie : un rapport lisible, code 0 si tout passe, 1 sinon (u
… [4497 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\nr=pathlib.Path('reports')\nprint('md', len(list(r.glob('*.md'))))\nprint('json', len(list(r.glob('*.json'))))\nEOF\ngrep -n \"fichiers / JSON\\|fiches\\*\\* /\\|JSON\" docs/pilotage/en-cours.md | head", "description": "Count reports files and en-cours  … [10 caractères tronqués]`

  ```
md 723
json 817
94:- **J5.1** : rapport de semaine (F1 **0,7533 → 0,7902**, tagger **0,9475**, **13 décisions**, **21 rejets**) ; [rapport](../../reports/rapport-semaine.md) + JSON.
105:| fichiers / JSON de résultats | **723** / **817** | `reports/*.md` / `reports/*.json` |
  ```

- **bash** `{"command": "sed -n '160,360p' tools/revue_documentation.py", "description": "Read rest of documentation review"}`

  ```
# 1. classement : aucune donnée de résultat dans docs/
    for f in (RACINE / "docs").rglob("*"):
        if f.suffix in (".json", ".csv", ".npz", ".jsonl") and f.is_file():
            if f.name == "index.json" and f.parent.name == "glossaire":
                continue
            alertes.append(f"classement : donnée de résultat dans docs/ → {f.relative_to(RACINE)}")
    for nom in ("07-mesures-couche-commune.md", "fiche-nuit-17-10.md"):
        if not (RACINE / "reports" / nom).exists():
            alertes.append(f"classement : la fiche courante reports/{nom} manque")
    if not (RACINE / "reports/README.md").exists():
        alertes.append("classement : reports/ n'a pas d'index (reports/README.md)")

    # 5. compteurs : la page d'état est la source unique, et elle dit le disque
    portes = extrait_entier(t, r"\|\s*portes\s*\|\s*\*\*(\d+)\*\*")
    chapitres = extrait_entier(t, r"\|\s*chapitres de la synthèse\s*\|\s*\*\*(\d+)\*\*")
    documents = extrait_entier(t, r"\|\s*documents de[^|]*\|\s*\*\*(\d+)\*\*")
    fiches = re.search(r"\|\s*fichiers / JSON de résultats\s*\|\s*\*\*(\d+)\*\*\s*/\s*\*\*(\d+)\*\*", t)
    for nom, valeur, disque in (
        ("portes", portes, comp
… [8348 caractères tronqués]
  ```

- **bash** `{"command": "ls reports/*.json | grep -E 'r035|convention|schema-v2|restitution-v0|atomes|corpus-commun|retrieval-epoque|genealogie|coordination|g017|s065|retrieval-familles|restitution-v1|passe-honnetete'", "description": "List relevant JSON files"}`

  ```
reports/atomes-niveaux.json
reports/corpus-commun.json
reports/genealogie-deux-faces.json
reports/passe-honnetete.json
reports/pensee-convention-doc.json
reports/pensee-convention-gv.json
reports/pensee-conventions.json
reports/pensee-g017.json
reports/pensee-r035.json
reports/pensee-restitution-v0.json
reports/pensee-restitution-v1.json
reports/pensee-s065.json
reports/pensee-schema-v2.json
reports/rapport-coordination-a.json
reports/rapport-coordination-n2.json
reports/rapport-coordination-r.json
reports/rapport-coordination-s.json
reports/retrieval-epoque.json
reports/retrieval-familles.json
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, pathlib\nfor f in ['reports/pensee-r035.json','reports/pensee-convention-gv.json','reports/pensee-schema-v2.json','reports/pensee-restitution-v0.json']:\n    p=json.load(open(f))\n    print('='*70); print(f, '->', list(p.keys()))\n    print(json.dumps(p,  … [79 caractères tronqués]`

  ```
======================================================================
reports/pensee-r035.json -> ['date', 'ligne', 'tache', 'cas', 'phrase', 'regle', 'avant', 'apres', 'delta', 'gold', 'controles_negatifs', 'generalisation', 'portes', 'reste', 'limites']
{"date": "2026-11-07", "ligne": "B13", "tache": "J1.1", "cas": "r035", "phrase": "The film she talks about is out.", "regle": "relative zéro à préposition orpheline : [GN antécédent] [pronom sujet] [verbe] [préposition sans complément nominal] → REL ; la cible est la tête du GN. Anglais seulement.", "avant": {"all": {"phrases": 612, "pos": 0.8625, "f1": 0.7533, "precision": 0.7239, "rappel": 0.7853, "tete": 0.864, "exact": 236, "labels": 237, "cibles": 239, "couverture": 0.9916}, "dev": {"phrases": 422, "pos": 0.8618, "f1": 0.7476, "precision": 0.7223, "rappel": 0.7747, "tete": 0.8603, "exact": 160, "labels": 161, "cibles": 163, "couverture": 0.9877}, "test": {"phrases": 190, "pos": 0.8642, "f1": 0.7663, "precision": 0.7274, "rappel": 0.8095, "tete": 0.8724, "exact": 76, "labels": 76, "cibles": 76, "couverture": 1.0}}, "apres": {"all": {"phrases": 612, "pos": 0.8625, "f1": 0.7549, "precision": 0.7254, "rappel": 0.7869, "tete": 0.
… [5910 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\n# g017\np=json.load(open('reports/pensee-g017.json'))\nprint('g017 keys', list(p))\nfor k in ['mesures','controles','phrases_changees','convention','limites','verdict','decision']:\n    if k in p: print(k, '=>', json.dumps(p[k], ensure_ascii=False)[:1200] … [294 caractères tronqués]`

  ```
g017 keys ['date', 'ligne', 'tache', 'objet', 'verdict', 'dispositif', 'reproduction', 'regle', 'mesures', 'phrases_changees', 'sub_gold_fin_adverbe', 'convention', 'controles', 'limites', 'suite', 'fichiers']
mesures => {"base": {"all": {"phrases": 612, "syntagme": {"precision": 0.786, "rappel": 0.7944, "f1": 0.7902, "tp": 1480, "fp": 403, "fn": 383}, "attachement": {"cibles": 239, "labels": 238, "exact": 237, "top1_taux": 0.9916, "topk_taux": 0.9874, "exact_taux": 0.9916, "exact_taux_span": 0.9958, "couverture": 0.9958}}, "dev": {"phrases": 422, "syntagme": {"precision": 0.7887, "rappel": 0.7863, "f1": 0.7875, "tp": 1019, "fp": 273, "fn": 277}, "attachement": {"cibles": 163, "labels": 162, "exact": 161, "top1_taux": 0.9877, "topk_taux": 0.9877, "exact_taux": 0.9877, "exact_taux_span": 0.9938, "couverture": 0.9939}}, "test": {"phrases": 190, "syntagme": {"precision": 0.78, "rappel": 0.8131, "f1": 0.7962, "tp": 461, "fp": 130, "fn": 106}, "attachement": {"cibles": 76, "labels": 76, "exact": 76, "top1_taux": 1.0, "topk_taux": 0.9868, "exact_taux": 1.0, "exact_taux_span": 1.0, "couverture": 1.0}}, "hand": {"phrases": 20, "syntagme": {"precision": 0.8333, "rappel": 0.9821, "f1": 0.901
… [8755 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nfor f in ['reports/pensee-restitution-v1.json','reports/passe-honnetete.json']:\n    p=json.load(open(f))\n    print('='*60); print(f, list(p))\n    print(json.dumps(p, ensure_ascii=False)[:3000])\nEOF", "description": "Inspect v1 and honesty JSON"}`

  ```
============================================================
reports/pensee-restitution-v1.json ['schema', 'version', 'date', 'ligne', 'tache', 'titre', 'banc', 'banc_sha256', 'commande', 'dispositif', 'synthese', 'resultats', 'limites']
{"schema": "drave.restitution.canonique.banc", "version": 1, "date": "2026-11-14", "ligne": "B13", "tache": "J8.1", "titre": "La restitution v1 — la forme canonique, et la réponse au miroir strict", "banc": "reports/pensee-fiabilite-produit.json", "banc_sha256": "bd54b1ff7fa14e203dcfeaced908b8dec699995c2ff3fe910c7956ac64d18a48", "commande": "python3 tools/drave.py restituer --banc reports/pensee-fiabilite-produit.json --canonique --json", "dispositif": {"outil": "tools/restitution.py", "cli": "python3 tools/drave.py restituer TEXTE --canonique", "analyse": "bloc_linguistique.Heuristique().analyser(texte, langue=None)", "forme": "segments (type, rôle, span, valeur), linéarisation sans chevauchement, squelette « type/rôle : valeur -> cible », plancher de jetons (mot > POS > graphème) et empreinte sha256 du corps canonique", "miroir_strict": "minimum des fidélités binaires de la surface (graphème), des mots et des POS ; une sortie n'est fidèle que si 
… [5287 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nfor f in ['reports/atomes-niveaux.json','reports/corpus-commun.json','reports/retrieval-epoque.json','reports/genealogie-deux-faces.json']:\n    p=json.load(open(f))\n    print('='*70); print(f, 'keys:', list(p))\n    # print selected top-level values com … [381 caractères tronqués]`

  ```
======================================================================
reports/atomes-niveaux.json keys: ['fiche', 'version', 'date', 'titre', 'statut', 'sources', 'niveaux', 'niveaux_du_contrat', 'principe', 'atomes', 'calibration_44_oeuvres', 'protocole', 'limites', 'prochaine_etape', 'fichiers']
  fiche = "reports/rapport-atomes-niveaux.md"
  version = "1.0"
  date = "2026-11-07"
  titre = "Table de correspondance — 14 atomes V14 de Panini et 8 niveaux Drave"
  statut = "hypothese_de_lecture_et_protocole_non_mesure"
  sources = {"atomes": {"depot": "../../Panini/research", "head": "e10d695", "head_date": "2026-10-25", "fichiers": ["../../Panini/README.md", "../../Panini/research/docs/CADRES_THEORIQUES_ET_IDEES_ORIGINALES.md", "../../Panini/research/philosophy-theory/GRILLE_ABLATION_V14_v0.1.md", "../../Panini/research/nipada/falsification/analytic_sigs_v1.json"], "note": "V14 de Research uniquement ; les 34 atomes de Panini-FS et les 9 dhatus de l'ancien docs/ de l'hote ne sont pas utilises."}, "niveaux": {"fichiers": ["../docs/theorie/contrat-bloc-langue.md", "../docs/theorie/pre-traitement-linguistique.md", "rapport-bloc-linguistique.md"], "note": "Le contrat compte 9 niveaux 
… [12512 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\np=json.load(open('reports/corpus-commun.json'))\nprint('intersection', json.dumps(p['intersection'], ensure_ascii=False)[:2500])\nprint('--- controle', json.dumps(p['controle_negatif'], ensure_ascii=False)[:1500])\np=json.load(open('reports/retrieval-epoq … [566 caractères tronqués]`

  ```
intersection {"appariables_article1": 438, "article1_drave": 440, "drave_article1_hors_panini": 2, "drave_langues": 456, "ecarts_surface": 20, "exacts": 418, "familles_exactes": {"(inconnue)": 10, "Abkhaz-Adyge": 2, "Afro-Asiatic": 12, "Algic": 1, "Araucanian": 1, "Arawakan": 7, "Artificial Language": 3, "Athabaskan-Eyak-Tlingit": 1, "Atlantic-Congo": 81, "Austroasiatic": 3, "Austronesian": 37, "Aymaran": 1, "Barbacoan": 1, "Cahuapanan": 1, "Chicham": 4, "Dravidian": 5, "Eskimo-Aleut": 1, "Guaicuruan": 1, "Harakmbut": 1, "Hmong-Mien": 3, "Huitotoan": 1, "Indo-European": 120, "Iroquoian": 2, "Japonic": 1, "Koreanic": 1, "Mande": 7, "Mayan": 11, "Misumalpan": 1, "Mixe-Zoque": 1, "Mongolic-Khitan": 1, "Muskogean": 1, "Nilotic": 4, "Otomanguean": 7, "Pano-Tacanan": 5, "Peba-Yagua": 1, "Quechuan": 11, "Saharan": 1, "Sino-Tibetan": 17, "Songhay": 1, "Tai-Kadai": 7, "Tarascan": 1, "Ticuna-Yuri": 1, "Totonacan": 1, "Tucanoan": 2, "Tungusic": 4, "Tupian": 2, "Turkic": 17, "Uralic": 8, "Uto-Aztecan": 2, "Yanomamic": 1, "Zaparoan": 2}, "intersection_fichiers": 453, "listes": {"drave_article1_hors_panini": ["udhr_012.xml", "udhr_prq.xml"], "ecarts_surface": ["udhr_ady.xml", "udhr_bfa.xml", "ud
… [20316 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nfor f in ['reports/rapport-coordination-n2.json','reports/rapport-coordination-s.json','reports/rapport-coordination-r.json','reports/rapport-coordination-a.json']:\n    p=json.load(open(f))\n    print('='*70); print(f, list(p))\n    for k,v in p.items(): … [280 caractères tronqués]`

  ```
======================================================================
reports/rapport-coordination-n2.json ['date', 'head', 'ligne', 'objet', 'fiche', 'verdict', 'aucune_modification_n2', 'bug', 'checkpoints', 'chiffres', 'correctif', 'commande_n2', 'limites', 'fichiers_lus_non_modifies', 'references']
  date = "2026-11-13"
  head = "ced21933"
  ligne = "N2"
  objet = "coordination du mètre eval_n2_propre.py pour les checkpoints RoPE"
  fiche = "reports/rapport-coordination-n2.md"
  verdict = "eval_n2_propre.py lit les checkpoints RoPE comme des positions absolues et rend 8,0225 sur propre512-8k à 128 octets, contre 2,9726 à 128 et 2,7856 à 1024 au mètre RoPE. --rope est nécessaire mais non suffisant : le checkpoint de la porte a été entraîné avec le canal, et --rope seul rend 40,0658. Le correctif validé est --rope --canal-dir."
  aucune_modification_n2 = ["tools/native_model.py", "tools/entrainer_native.py", "work/"]
  bug -> ['fichier', 'symptome', 'causes', 'piege_de_longueur', 'pourquoi_strict_false_ne_le_detecte_pas']
  checkpoints = {"porte": {"fichier": "work/n2ac/propre512-8k.pt", "date": "2026-11-03 02:01", "octets": 137248474, "sha256": "37c5673b3d51f6f871c4391b97015b40
… [17665 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,180p' tools/taille_documents.py; echo '---'; grep -n \"semaine-autonome\\|en-cours\\|budget\" tools/taille_documents.py | head -40", "description": "Read document size budget tool"}`

  ```
#!/usr/bin/env python3
"""taille_documents.py — le budget de contexte et la cohésion des documents.

Ce que l'outil vérifie :
  1. la taille des documents **chargeables** (T0/T1) en mots, avec un budget par catégorie ;
  2. la cohésion minimale : un titre, un résumé en tête, et pour les documents datés un
     « Résumé » + « ne pas charger par défaut » ;
  3. les fiches de résultats trop longues pour être lues d'un bloc (avertissement, pas échec) ;
  4. le classement des plus gros documents, pour voir où le contexte part.

Les fiches de `reports/` (sauf `reports/README.md`) et le `journal/` sont **hors budget** :
ils ne sont pas chargés automatiquement. Le budget est en **mots** ; l'estimation de tokens
est donnée à titre indicatif (≈ caractères / 4).

Les **sources de diagrammes** (` ```plantuml `, ` ```mermaid `) sont **rendues, pas lues** :
elles ne comptent pas dans le budget ; le document les porte, la page montre le SVG.
"""
from __future__ import annotations
import pathlib
import re
import sys

RACINE = pathlib.Path(__file__).resolve().parent.parent

# (catégorie, budget en mots). Les globs sont résolus dans l'ordre ; le premier match gagne.
BUDGETS: list[tuple[str, str, int
… [8424 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | head -40", "description": "Run document size budget"}`

  ```
budget de contexte · documents chargeables
    mots lignes  cat budget  document
    7632    387   T1   9000  docs/pilotage/roadmap.md
    5999    597 DATÉ      0  docs/implantation/contexte-long.md
    4858    515   T1   5000  docs/theorie/glossaire/10-le-pont-linguistico-semantique-le-vocabu.md
    4085    431 DATÉ      0  docs/implantation/numa-segregation.md
    3310    317   T1   3500  README.md
    3072    341 DATÉ      0  docs/implantation/convertisseur.md
    2962    364   T1   5000  docs/theorie/glossaire/02-modeles-et-architectures.md
    2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2718    202   T1   2800  reports/README.md
    2450    166   T1   2500  docs/pilotage/references-non-regression.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/form
… [504 caractères tronqués]
  ```

- **bash** `{"command": "ls -la .git/hooks/ | head -20; echo '---'; sed -n '1,160p' .git/hooks/pre-commit 2>/dev/null", "description": "Inspect pre-commit hook"}`

  ```
total 68
drwxr-xr-x. 1 stephane stephane  576 31 oct 12:55 .
drwxr-xr-x. 1 stephane stephane  180 14 nov 03:47 ..
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
---
#!/bin/sh
# pre-commit — l'ét
… [1405 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' tools/verifie_etat_a_jour.py; echo '---journal'; sed -n '1,120p' tools/verifie_journal.py", "description": "Read state/journal verifiers"}`

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
… [8065 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport re\nt=open('docs/pilotage/en-cours.md').read()\nprint('en-cours words', len(re.findall(r'\\S+',t)))\nt=open('docs/pilotage/semaine-autonome.md').read()\nprint('semaine words', len(re.findall(r'\\S+',t)))\nt=open('reports/rapport-semaine.md').read()\nprint('rapp … [98 caractères tronqués]`

  ```
en-cours words 1620
semaine words 2447
rapport-semaine words 4849
  ```

- **bash** `{"command": "grep -n \"J5.2\\|J10\\|prochaine action\\|Reste\\|reste\" docs/pilotage/semaine-autonome.md | head -40", "description": "Locate update points in semaine-autonome"}`

  ```
23:| reste | mesure | où |
32:| chantier | état | ce qui reste | territoire |
161:| J5.2 passe, tag, release | ⏳ à faire | — | — |
163:**Reste** : J5.2 (passe complète, revue de documentation, tag annoté, release), les commits de
174:| jour | vague | état | livrable mesuré | commit | reste |
184:| **J5** | matin : rapport de semaine | ✅ fait (13/11) | [`rapport-semaine.md`](../../reports/rapport-semaine.md) + JSON : chiffres, décisions, rejets, reste | `commit J5.1` | — |
196:S (non committés) et N2 (`rope_model.py` dans `work/`), et la **passe complète** : J5.2 doit
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-autonome.md", "offset": 125, "limit": 90}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-autonome.md</path>
<type>file</type>
<content>
125: | **les sous-agents** (40-90 min) | les vagues débordent | 2-4 sous-agents, mandats courts, livrables partiels acceptés |
126: | **le gold** | les 2 spans restants sont des cas isolés | les déclarer, ne pas surapprendre |
127: 
128: ## 6. La file (rappel)
129: 
130: Les **29 tâches** de [`rapport-file-taches.md`](../../reports/rapport-file-taches.md) : **8
131: autonomes** (faites ou en cours), **11 en coordination**, **10 bloquées**. Les tâches autonomes
132: restantes sont dans le tableau du § 2.1 ; les autres sont des fiches de coordination.
133: 
134: ## 7. Ce que la semaine doit avoir produit
135: 
136: - le **produit** : 2 spans tranchés (ou déclarés), le schéma v2, la restitution v0, la porte verte ;
137: - **l'intégration** : une table atomes ↔ niveaux, un corpus commun, une mesure de retrieval à
138:   époque contrôlée, une fiche de généalogie à deux faces ;
139: - **la coordination** : un état daté de N2/S/R/A, les décisions prises et nommées ;
140: - **la consolidation** : la passe complète, un tag, le rapport de semaine, la roadmap à jour.
141:
… [5515 caractères tronqués]
  ```

- **bash** `{"command": "ls reports/ | grep -i bilan; echo '---'; grep -rn \"rapport-bilan\" reports/README.md docs/ 2>/dev/null | head", "description": "Look for existing bilan reports"}`

  ```
a26-bilan.json
bilan-b11.md
bilan-multi-materiel.md
pensee-anaphore-bilan.json
rapport-a26-bilan.md
rapport-pensee-anaphore-bilan.md
---
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\np=json.load(open('reports/rapport-semaine.json'))\nfor d in p['decisions']:\n    print(d['id'], '|', d['objet'], '|', d['etat'], '|', d.get('suite'))\nprint('--- rejets')\nfor r in p['rejets']:\n    print(r['id'], '|', r['objet'], '|', r['chiffre'])\nEOF" … [68 caractères tronqués]`

  ```
D1 | Adopter la relative zero a preposition orpheline | fait | g017 reste
D2 | Adopter sujet hors du GV + adverbe final de temps etroit ; rejeter l'adverbe large et l'objet hors GV | fait | objet 75 FP / 51 FN ouvert
D3 | Publier le schema v2 additif (meta.partition, meta.alternative), garder v1 lue | fait | invariants semantiques a tester
D4 | La restitution v0 est un codec de surface, pas un decodeur ; ajouter la categorie C | fait | v0.1 ponctuation, gold de restitution
D5 | La table atomes <-> niveaux est une grille de lecture, pas une mesure ; protocole CLR / permutations / BH / split-half | fait | V14 des 21 langues a mesurer
D6 | Le corpus commun est l'UDHR article 1, 21 textes ; exclure les 20 ecarts, ne pas les corriger | fait | corpus multi-epoques a construire
D7 | Le retrieval est de surface ; stratifier par ecriture ; ne pas lire le brut | fait | replication neuronale ouverte
D8 | Comparer les deux genealogies sur les paires couvertes ; inconnu=1,0 n'est pas une distance | fait | V14, 9 dhatus, distance continue
D9 | Ne pas livrer --rope seul ; valider --rope --canal-dir et eval_longueurs.py --rope ; promouvoir rope_model.py | fait | porte propre 0,2856/0,3566
D10 | Co
… [2167 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,50p' reports/README.md", "description": "Read reports README head"}`

  ```
# Les rapports — données intermédiaires et références

> **Ce dossier porte les résultats et les données de nos travaux**, jamais la documentation de référence
> (elle est dans [`docs/`](../docs/)). Les fiches courantes sont citées depuis le tableau de bord
> [`docs/pilotage/en-cours.md`](../docs/pilotage/en-cours.md).

> **Navigation** : [la carte des sujets](../docs/theorie/carte.md) · [l'état du moment](../docs/pilotage/en-cours.md) ·
> [l'inventaire des docs](../docs/README.md) · [le journal](../journal/README.md).
>
> **Contexte** : la fiche [`07-mesures-couche-commune.md`](07-mesures-couche-commune.md) est un **hub** de
> **168 mesures** en **10 parties** (`07/p1.md` … `07/p10.md`), pas un fichier de 150 Ko. La lire **par
> partie**, jamais en entier ; l'index exhaustif des fiches est [`INDEX.md`](INDEX.md).

## Les fiches courantes

| fichier | ce qu'il porte |
|---|---|
| [`rapport-semaine.md`](rapport-semaine.md) | **J5.1** — le rapport de semaine : produit, intégration, décisions, rejets, reste |
| [`rapport-passe-honnetete.md`](rapport-passe-honnetete.md) | **J9.1** — la passe d'honnêteté : **19** fiches « instantané historique », 0 chiffre dépassé lu comme courant |
| [
… [3531 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\np=json.load(open('tools/chantier/plan.json'))\nfor t in p['taches']:\n    if t['id'] in ('J11.1','J11.2','J11.3','J11.4','J12.1','J12.2','J13.1','J14.1'):\n        print('='*70)\n        print(t['id'], t['titre'], '| jour', t.get('jour'), '| budget', t.ge … [180 caractères tronqués]`

  ```
======================================================================
J11.1 Le produit — les exemples rejoués | jour 11 | budget 90
Tâche J11.1 : les exemples de la doc produit — rejoue les 5 blocs de `docs/produit/exemples.md` avec le code courant (F1 0,7902, 237/238, le schéma v2) et corrige les sorties qui ont bougé ; fiche `reports/rapport-exemples-rejoues.md` + JSON, commit.
acceptation: [{"commande": "test -f reports/rapport-exemples-rejoues.md && echo FICHE-OK", "attendu": "FICHE-OK"}, {"commande": "bash tools/porte-produit.sh 2>&1 | tail -1", "attendu": "verte"}]
======================================================================
J11.2 Le produit — la mesure par langue | jour 11 | budget 90
Tâche J11.2 : ajouter `evaluer --par-langue` (le détail fr/en) et le documenter dans `docs/produit/README.md` ; test dans `tools/tests/test_produit.py` ; fiche `reports/rapport-evaluer-langue.md` + JSON, commit.
acceptation: [{"commande": "python3 tools/drave.py evaluer --par-langue >/dev/null 2>&1; echo PL-$?", "attendu": "PL-0"}, {"commande": "python3 tools/tests/test_produit.py 2>&1 | tail -1", "attendu": "OK"}]
=====================================================================
… [3165 caractères tronqués]
  ```

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-chantier.md", "content": "# J10.1 — le bilan du chantier : F1 0,7533 → 0,7902, attachement 236 → 238, Panini mesuré et borné\n\n> **Instantané historique** — les chiffres publiés ici sont ceux du commit de la fiche  … [37170 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-chantier.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cat > /tmp/gen_bilan_json.py <<'PY'\nimport json, pathlib\n\ndata = {\n \"schema\": \"drave.bilan-chantier\",\n \"version\": 1,\n \"titre\": \"J10.1 — le bilan du chantier : F1 0,7533 → 0,7902, attachement 236 → 238, Panini mesuré et borné\",\n \"date\": \"2026-11-14\",\n \"tache\": \"J … [38225 caractères tronqués]`

  ```
écrit reports/rapport-bilan-chantier.json 39198 octets
decisions 20 rejets 30 reste 15
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-autonome.md", "limit": 20}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-autonome.md</path>
<type>file</type>
<content>
1: # Le chantier autonome — une semaine (7 → 14 novembre 2026)
2: 
3: > **Ce que ce document est.** Le **plan du chantier d'une semaine** : tous les travaux ouverts du
4: > dépôt et l'**intégration avec l'écosystème Panini**. Il dit **quoi**, **dans quel ordre**, **avec
5: > quels sous-agents**, **comment on mesure**, et **ce qui peut faire échouer**. L'état courant est
6: > dans [`en-cours.md`](en-cours.md) ; la théorie de la généalogie dans
7: > [`../theorie/genealogie-des-langues.md`](../theorie/genealogie-des-langues.md) ; la méthode
8: > Panini/Nipada dans [`../methode/panini-nipada.md`](../methode/panini-nipada.md).
9: > *À relire chaque matin du chantier.*
10: 
11: ## 1. L'objet
12: 
13: **Une semaine, un système utilisable, une intégration mesurée.** Le produit `drave` (CLI, contrat,
14: porte) est la **priorité** ; l'intégration avec Panini/Nipada est le **second axe** ; les chantiers
15: N2/S/R/A sont **coordonnés** (jamais écrits par cette session). Chaque vague produit un
16: **résultat mesuré**, une **fiche** et son **JSON**, la mise à jour de l'**
… [180 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-autonome.md", "old_string": "> Panini/Nipada dans [`../methode/panini-nipada.md`](../methode/panini-nipada.md).\n> *À relire chaque matin du chantier.*", "new_string": "> Panini/Nipada dans [`../methode/panini-nipad … [449 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-autonome.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-autonome.md", "new_string": "## 3 bis. L'état du chantier (14/11, 03 h 55 — après J10.1)\n\nLe superviseur a lancé **21 tâches** (budget **22 032 s** au 14/11 03 h 46, hors J10.1). **20\npassent l'acceptation** ; ** … [3842 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-autonome.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-autonome.md", "new_string": "## 8. L'état de chaque jour — bilan du 14/11\n\n> **Les dates réelles diffèrent du plan.** J1–J3 ont été exécutés le **07/11** (le plan les\n> plaçait du 07 au 09) ; J4 le **13/11** (pla … [1079 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-autonome.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-autonome.md", "offset": 190, "limit": 55}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-autonome.md</path>
<type>file</type>
<content>
190: > (J1–J5) et [`rapport-bilan-chantier.md`](../../reports/rapport-bilan-chantier.md) (J1–J10).
191: 
192: | jour | vague | état | livrable mesuré | commit | reste |
193: |---|---|---|---|---|---|
194: | **J1** | matin : `r035` + convention GV | ✅ fait | exact **237/238**, couverture **0,9958**, F1 **0,7533 → 0,7902**, POS inchangée | `25a6c0ff`, `92652984` | `g017`, `s065`, objet (75 FP / 51 FN), 5 FP sujet |
195: | **J1** | après-midi : schéma v2 + restitution v0 | ✅ fait | **26 cas / 0 échec**, **1 836 annotations / 0 échec** ; **46/46** surfaces, miroir **0,1087** | `9a259953`, `8eb0cc49` | invariants sémantiques, v0.1 ponctuation, gold de restitution |
196: | **J2** | matin : inventaire + table atomes ↔ niveaux | ✅ fait | **14/14 lignes**, 8 niveaux, 33 paires colinéaires, 4 composantes > 1 | `9c7f71dc` (+ `fffbbe5d`) | aucune correspondance mesurée : protocole J2.2 |
197: | **J2** | après-midi : corpus commun | ✅ fait | **21 textes**, 5 familles, 10 écritures, **418/438** paires exactes (95,4 %), 8/8 contrôles | `c3467170` (avec J3.1) | corpus multi-ép
… [2373 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-autonome.md", "new_string": "| **J5** | matin : rapport de semaine | ✅ fait (13/11) | [`rapport-semaine.md`](../../reports/rapport-semaine.md) + JSON : chiffres, décisions, rejets, reste | `34e3e4ab` | — |\n| **J5** … [6244 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-autonome.md has been updated successfully.
  ```

- **bash** `{"command": "grep -n \"Mis à jour\\|Pensée — B13\\|J5.1\\|dernière passe\\|fichiers / JSON\\|Ce qui reste\\|J5.2\\|J9.1\" docs/pilotage/en-cours.md", "description": "Locate en-cours edit points"}`

  ```
3:**Mis à jour : 2026-11-14, 03 h 30 HNE (heure locale, EST).**
90:- **Pensée — B13 (actif)** : **183/183**, gold 432 ; **`r035`** (238/238) ; **convention des GV** (0,7902) ; **`s065` réglé** (238/238 ; [fiche](../../reports/rapport-s065.md)) ; **J6.1 rejetée** (test −0,0028 ; g017 à trancher) ; **schéma v2** (v1 lue) ; **restitution v1** (46/46 canonique, strict 0,1087 ; [fiche](../../reports/rapport-restitution-v1.md)) ; **J9.1** passe d'honnêteté (**19** fiches ; [fiche](../../reports/rapport-passe-honnetete.md)) ; [restitution v0](../../reports/rapport-restitution-v0.md), [g017](../../reports/rapport-g017.md).
94:- **J5.1** : rapport de semaine (F1 **0,7533 → 0,7902**, tagger **0,9475**, **13 décisions**, **21 rejets**) ; [rapport](../../reports/rapport-semaine.md) + JSON.
105:| fichiers / JSON de résultats | **723** / **817** | `reports/*.md` / `reports/*.json` |
107:| dernière passe | **03/11 11 h 30** (82, **80/2**) ; N3 **17/17** à 11 h 32 | `docs/pilotage/references-non-regression.md` |
125:## Ce qui reste
127:**N2** — porte (0,2856 val / 0,3566 test) ; **Pensée** — convention d'adverbe `g017`, T132/T133, gold 200+ ; **J3.2** — **V14 des 21 langues** ; **J7.1** — **réplic
… [167 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**Mis à jour : 2026-11-14, 03 h 55 HNE (heure locale, EST).**", "old_string": "**Mis à jour : 2026-11-14, 03 h 30 HNE (heure locale, EST).**"}`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md": file has not been read — read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
1: # En ce moment
2: 
3: **Mis à jour : 2026-11-14, 03 h 30 HNE (heure locale, EST).**
4: 
5: > **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
6: > plan plus bas (**La carte**).
7: 
8: ### Session `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — le hub de reprise du 04/11
9: 
10: - **Id** : `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — [`plan.md`](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/plan.md).
11: - **Rôle** : **Hub de reprise** — état, docs, intégration, passe.
12: - **Fait** : index réparé ; **N3 intégré** ; N2/S/L actifs ; suivi docs (revue, liens, tableaux).
13: - **Prochaine action** : **suivi docs**, puis la **passe** après les runs.
14: - **Bloquants** : aucun.
15: - **Journal** : [la session](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/).
16: 
17: ## Sessions en cours
18: 
19: > Contrat : [`continuite.md`](../methode/continuite.md) · sessions terminées :
20: > [`journal/sessions/`](../../journal/sessions/). Chaque session expose son mandat dans son
21: > `plan.md` (`python3 tools/sessions
… [11630 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**Mis à jour : 2026-11-14, 03 h 55 HNE (heure locale, EST).**", "old_string": "**Mis à jour : 2026-11-14, 03 h 30 HNE (heure locale, EST).**"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "| fichiers / JSON de résultats | **724** / **818** | `reports/*.md` / `reports/*.json` |\n| documents de `docs/` | **123** (hors archive et README) | `docs/**/*.md` |\n| dernière passe | **14/11 … [437 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Pensée — B13 (actif)** : **183/183**, gold 432 ; **`r035`** (238/238) ; **convention des GV** (0,7902) ; **`s065` réglé** (238/238 ; [fiche](../../reports/rapport-s065.md)) ; **J6.1 rejetée* … [1039 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **J5.1** : rapport de semaine (F1 **0,7533 → 0,7902**, tagger **0,9475**, **13 décisions**, **21 rejets**) ; [rapport](../../reports/rapport-semaine.md) + JSON.\n- **J10.1 — le bilan** : **20  … [429 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, gold 432, r035 et convention des GV (0,7902, 238/238), s065 réglé (238/239), J6.1 rejeté (conventio … [616 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**N2** — porte (0,2856 val / 0,3566 test) ; **Pensée** — convention d'adverbe `g017`, T132/T133, gold 200+ ; **J3.2** — **V14 des 21 langues** ; **J7.1** — **réplication neuronale** des 30 artic … [571 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "grep -n \"État au 14/11\\|J9.1 passe\\|J7.1\" docs/pilotage/roadmap.md | head -10", "description": "Locate roadmap state paragraph"}`

  ```
35:| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 langues à 0,9687**, script 1,0000 ; analyse heuristique (5 schémas) ; **contrat de substitution écrit** ([`contrat-bloc-langue.md`](../theorie/contrat-bloc-langue.md)) ; **frontière : script 1,0, langue 0,137 (libellés) / 0,9687 (texte long)** ; **porte des quatre modes : neuronal 0,9309/0,8226/0,8784 ; fusion 0,928/0,802/0,857** ; **fusion réparée par niveau : 0,9309/0,8226/0,8784/0,9954 (le max)** ([fiche](../../reports/rapport-pensee-fusion-reparee.md)) ; **corpus commun UDHR : 21 textes, 418/438 paires exactes (95,4 %), 20 écarts exclus** ([fiche](../../reports/rapport-corpus-commun.md)) ; **J3.1 retrieval à époque contrôlée : l'écriture domine (+0,609), l'époque ne pèse pas à écriture contrôlée (−0,034/siècle, p=0,19), le brut est un effet de composition (0,238 vs 0,427)** ([fiche](../../reports/rapport-retrieval-epoque.md)) ; **J3.2 généalogie à deux faces : Panini couvre 5/21 langues (200/210 paires « inconnues »), Glottolog 21/21 ; 154/154 paires hors script au hasard exact, le signal de famille vit dans 
… [4330 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "limit": 8, "offset": 38}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md</path>
<type>file</type>
<content>
38: **État au 14/11 03 h 30.** B13 : **POS 86,25 %**, **attachement exact 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (REL suivie d'un GV → le sujet du GV : 238/238, 0 span, 0 POS ; [fiche](../../reports/rapport-s065.md)) ; **183/183** ; **`r035`** (relative zéro) réglé ; **convention des GV** réglée (sujet hors du GV + adverbe final : GV F1 0,7549 → 0,7902, 0 perte d'attachement) ; **contrat v2 publié et validé** (`meta.partition`/`meta.alternative`, version 2, **v1 lue** : 26 cas, 0 échec) ; **restitution v1** (`restituer --canonique` : **46/46 formes canoniques exactes** contre la source canonisée, **miroir strict 0,1087 inchangé**, **395 segments / 395 rôles / 315 cibles dont 315 résolues**, stabilité **18/46** ; le strict ne monte pas, la v1 n'est pas la surface ; [fiche](../../reports/rapport-restitution-v1.md)) ; **J9.1 passe d'honnêteté** (**19** fiches « instantané historique » : 10 encarts réécrits, 9 ajoutés ; **0 fiche de résultats** ne publie les quatre marqueurs sans mention, hors 2 faux positifs ; [fich
… [1437 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "limit": 12, "offset": 45}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md</path>
<type>file</type>
<content>
45: → 2,9950** (256/512/1 024 à 1 000 octets), **2,9449** à 2 000 pour 1 024, et la **2 048** s'arrête à
46: 1 024 ; la **production** (N2.ac + RoPE 512) **bat les 200 k pas** (littérature 5,52, anglais 7,05,
47: wikitext2 7,90) ; le run **20 k** de la 2 048 finit à **2,6609** de PPL val ; la **fenêtre 1 024** passe **sous 2,5** au grand corpus (**2,4759 / 2,4373**), la porte **propre** reste **2,7856** ; **R1.1/R1.2** mesurées.
48: **S** : **54/55** types, **131/131** rôles, **47/47** compléments, gold **55**. **D/R/A** close (OCR
49: CEGEP **91 scans uniques**, 1 982 p). **Passe** : 81 portes, **76/5**, 1 h 52 ; la **82e**
50: (`porte-ressources`) est validée ; compteurs **574 fiches / 660 JSON**.
51: 
52: **J3.2** : les deux faces ne mesurent pas le même objet — Panini §150 est une distance de tradition (3/655 paires inter-langues), sa fonction `lang_distance` couvre 5/21 langues (200/210 paires « inconnues »), Glottolog 21/21 ; 154/154 paires hors script au hasard exact, le signal de famille vit dans 2-3 paires ; la face atomes n'est pas disponible (V14 3/21) ([fich
… [1462 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "new_string": "**J10.1 — le bilan du chantier.** **20 tâches sur 21** passent l'acceptation ; **5 timeouts**\n(J1.2, J2.2, J3.1, J5.2, J8.1), dont **4 récupérés** par une acceptation verte ou le commit de la\nt … [729 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md", "limit": 25}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md</path>
<type>file</type>
<content>
1: # Les rapports — données intermédiaires et références
2: 
3: > **Ce dossier porte les résultats et les données de nos travaux**, jamais la documentation de référence
4: > (elle est dans [`docs/`](../docs/)). Les fiches courantes sont citées depuis le tableau de bord
5: > [`docs/pilotage/en-cours.md`](../docs/pilotage/en-cours.md).
6: 
7: > **Navigation** : [la carte des sujets](../docs/theorie/carte.md) · [l'état du moment](../docs/pilotage/en-cours.md) ·
8: > [l'inventaire des docs](../docs/README.md) · [le journal](../journal/README.md).
9: >
10: > **Contexte** : la fiche [`07-mesures-couche-commune.md`](07-mesures-couche-commune.md) est un **hub** de
11: > **168 mesures** en **10 parties** (`07/p1.md` … `07/p10.md`), pas un fichier de 150 Ko. La lire **par
12: > partie**, jamais en entier ; l'index exhaustif des fiches est [`INDEX.md`](INDEX.md).
13: 
14: ## Les fiches courantes
15: 
16: | fichier | ce qu'il porte |
17: |---|---|
18: | [`rapport-semaine.md`](rapport-semaine.md) | **J5.1** — le rapport de semaine : produit, intégration, décisions, rejets, reste |
19: | [`
… [960 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md", "new_string": "| fichier | ce qu'il porte |\n|---|---|\n| [`rapport-bilan-chantier.md`](rapport-bilan-chantier.md) | **J10.1** — le bilan du chantier : F1 **0,7533 → 0,7902**, attachement **236 → 238**, Panini borné,  … [364 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-chantier.md", "new_string": "| **extension J6–J10** | `g017`, `s065`, Panini approfondi, restitution v1, honnêteté, bilan | `g017` **rejeté** ; `s065` **intégré** ; J7.1 **mesuré** ; v1 **mesurée** ; **19 fiches** a … [380 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-chantier.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-chantier.md", "new_string": "- **Le gain F1 se décompose** : `r035` apporte **+0,0016** (0,7533 → 0,7549), la convention des\n  GV **+0,0353** (0,7549 → 0,7902). Les deux règles sont des règles de **syntagmes** ou\n … [796 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-chantier.md has been updated successfully.
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, pathlib\np=pathlib.Path('reports/rapport-bilan-chantier.json')\nd=json.loads(p.read_text())\nfor row in d['chronologie']:\n    if row['tache'] in ('J4.1','J4.2','J4.4') and row.get('commit') == 'J5.1':\n        row['commit'] = '34e3e4ab'\np.write_text(jso … [229 caractères tronqués]`

  ```
ok
J0 None fait
J1.1 25a6c0ff fait
J1.2 92652984 fait (timeout)
J1.3 9a259953 fait
J1.4 8eb0cc49 fait
J2.1 9c7f71dc fait
J2.2 c3467170 fait (timeout)
J3.1 c3467170 fait (timeout)
J3.2 c2e629b3 fait
J4.1 34e3e4ab fait
J4.2 34e3e4ab fait
J4.3 a934d779 fait
J4.4 34e3e4ab fait
J5.1 34e3e4ab fait
J5.2 None echec
J6.1 64d9dd23 fait (rejet)
J6.2 b6e474dc fait
J7.1 d31e8788 fait
J8.1 229098ec fait (timeout)
J9.1 ecef7250 fait
J10.1 à venir fait
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, pathlib, re\np=pathlib.Path('reports/rapport-bilan-chantier.json')\nd=json.loads(p.read_text())\nprint('JSON valide,', p.stat().st_size, 'octets')\nprint('clés', list(d))\nprint('decisions', len(d['decisions']), 'rejets', len(d['rejets']), 'reste', len(d[ … [600 caractères tronqués]`

  ```
JSON valide, 39210 octets
clés ['schema', 'version', 'titre', 'date', 'tache', 'lignes_roadmap', 'statut', 'head', 'base', 'chiffres', 'decisions', 'rejets', 'echecs', 'reste', 'suite_plan', 'chronologie', 'limites', 'fichiers', 'verdict']
decisions 20 rejets 30 reste 15
liens 64 manquants []
--- counts
md 724 json 818
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -40", "description": "Run documentation review"}`

  ```
revue de documentation · 724 fiche(s) · 818 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -12; echo '---'; python3 tools/verifie_en_cours.py 2>&1 | tail -15; echo '---'; python3 tools/verifie_journal.py 2>&1 | tail -8", "description": "Run size, state, journal checks"}`

  ```
1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4051 mots (budget 4 000)

  avertissements :
     · 49 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 1 violation(s) :
     · T0 : 4051 mots (AGENTS + en-cours + une tâche) > budget 4 000
---
  en-cours · 1681 mots · 7 sections · 4 session(s) · 10 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
---
  journal · 46 jour(s) · 184 session(s) · 2463 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
  ```

- **bash** `{"command": "bash tools/porte-tableaux.sh 2>&1 | tail -8; echo '---'; python3 tools/verifier_schemas.py 2>&1 | tail -8", "description": "Run tables and schemas gates"}`

  ```
✅ 1789 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4101 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-14)
---
  schémas · 463 document(s) · 67 SVG · 2 source(s)
  ✅ aucun ASCII art, SVG valides et référencés, blocs PlantUML inline valides,
     sources et images relatives.
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport re\nlines=open('docs/pilotage/en-cours.md').read().splitlines()\nfor i,l in enumerate(lines,1):\n    n=len(re.findall(r'\\S+',l))\n    if n>25: print(f'{i:3d} {n:3d} {l[:150]}')\nEOF", "description": "Find long lines in en-cours"}`

  ```
48  37 - **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ; page **`/
 63  59 - **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065`
 79  56 - **Ce qu'elle fait** : **erratum 04/11** : la distillation native ne gagne rien à parité stricte (−0,03/−0,01/−0,004 ; +0,14–0,18 = repondération) ; 
 88  36 - **N2 — en pause** : **1 024** = recette de production ; **2 048 fini** ; la distillation est mesurée (bilan ci-dessus) ; prochaine : la **porte prop
 90  69 - **Pensée — B13 (actif)** : **183/183**, gold 432 ; **`r035`** (238/238) ; **convention des GV** (0,7902) ; **`s065` réglé** (238/238 ; [fiche](../..
 92  48 - **Panini J2.1/J2.2/J3.1/J3.2** : table **14 atomes** ; UDHR **418/438** ; **J3.1** : script domine, date non significative ; **J3.2** : `lang_distan
 93  41 - **Panini J7.1** : 532 textes (445 langues) ; **porte d'écriture** (hors script, hasard) ; famille **66,1 %** / sœur **26,1 %** (hasard 10,3/2,5) ; L
 95  39 - **J10.1 — le bilan** : **20 tâches sur 21** ; F1 **0,7533 → 0,7902**, attachem
… [1284 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Pensée — B13 (actif)** : **183/183**, gold 432 ; **`r035`** (238/238) ; **convention des GV** (0,7902) ; **`s065` réglé** (238/238 ; [fiche](../../reports/rapport-s065.md)) ; **J6.1 rejetée* … [1039 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **J10.1 — le bilan** : **20/21** ; F1 **0,7533 → 0,7902**, attachement **236 → 238 labels**, POS inchangée ; **5 timeouts**, **1 échec** (J5.2, tag absent) ; **D1–D20**, **R1–R30** ; [bilan](. … [344 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**N2** — porte (0,2856/0,3566) ; **Pensée** — `g017`, T132/T133, gold 200+ ; **J3.2** — V14 des 21 langues ; **J7.1** — réplication neuronale ; **S** — 11 verdicts + pointeur ; **R0.7** — split  … [527 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -8", "description": "Recheck document budget"}`

  ```
1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4020 mots (budget 4 000)

  avertissements :
     · 49 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 1 violation(s) :
     · T0 : 4020 mots (AGENTS + en-cours + une tâche) > budget 4 000
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, gold 432, r035 + convention GV (0,7902), s065 (238/239), g017 rejeté, schéma v2, restitution v1 (ca … [545 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **N2 — en pause** : **1 024** = recette ; **2 048 fini** ; distillation mesurée ; prochaine : **porte propre (0,29)** ; **GPUs libres**.", "old_string": "- **N2 — en pause** : **1 024** = rece … [169 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -6; echo '---'; python3 tools/verifie_en_cours.py 2>&1 | tail -4", "description": "Recheck budget and state"}`

  ```
T0 max : 3998 mots (budget 4 000)

  avertissements :
     · 49 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
---
  en-cours · 1628 mots · 7 sections · 4 session(s) · 10 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -5; echo '---'; python3 tools/verifie_journal.py 2>&1 | tail -3; echo '---'; python3 tools/verifier_schemas.py 2>&1 | tail -3", "description": "Re-run review and gates"}`

  ```
revue de documentation · 724 fiche(s) · 818 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
---
  journal · 46 jour(s) · 184 session(s) · 2463 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
---
  schémas · 463 document(s) · 67 SVG · 2 source(s)
  ✅ aucun ASCII art, SVG valides et référencés, blocs PlantUML inline valides,
     sources et images relatives.
  ```

- **bash** `{"command": "bash tools/porte-tableaux.sh 2>&1 | tail -4; echo '---'; python3 tools/taille_documents.py 2>&1 | grep -E 'README|T0 max|violation'", "description": "Re-run tables and check README budget"}`

  ```
✅ 1789 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4101 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-14)
---
    3310    317   T1   3500  README.md
    2746    203   T1   2800  reports/README.md
  T0 max : 3998 mots (budget 4 000)
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-chantier.md", "limit": 130, "offset": 60}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-chantier.md</path>
<type>file</type>
<content>
60:   d'**attachement** ; le diff token par token donne **0 token changé** sur 3 179. Ce n'est pas un
61:   échec : c'est le contrôle qui dit que les gains ne viennent pas d'une dérive des étiquettes.
62: - **Le gain F1 se décompose** : `r035` apporte **+0,0016** (0,7533 → 0,7549), la convention des
63:   GV **+0,0353** (0,7549 → 0,7902). Les deux règles sont des règles de **syntagmes** ou
64:   d'**attachement** ; aucune ne touche la POS.
65: - **Le gain F1 est in-sample.** La convention du sujet est **lue dans le gold** (712 GV sur 712
66:   commencent par un `VERB`, un `AUX` ou un `ADV` de négation) puis appliquée au gold. Le test ne
67:   la choisit pas, il ne la contredit pas non plus : c'est une **convention**, pas une
68:   généralisation hors échantillon. La règle `s065` est, elle, un seul cas, en dev.
69: - **Le dénominateur compte.** 238/238 est le taux sur les **labels** ; 238/239 (0,9958) est le
70:   taux sur les **cibles**. Le 239e span, `g017`, n'a pas de label : c'est le **1 span** de l'état
71:   courant, et il ne se règle pas par une règle de 
… [10449 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-chantier.md", "limit": 60}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-chantier.md</path>
<type>file</type>
<content>
1: # J10.1 — le bilan du chantier : F1 0,7533 → 0,7902, attachement 236 → 238, Panini mesuré et borné
2: 
3: > **Instantané historique** — les chiffres publiés ici sont ceux du commit de la fiche ; ils ne
4: > décrivent pas l'état courant. L'état courant du bloc est dans
5: > [`en-cours`](../docs/pilotage/en-cours.md) et [`la roadmap`](../docs/pilotage/roadmap.md).
6: 
7: > **Ligne de roadmap** : **B13** (le moteur de pensée), **R0.7** (le bloc langue), **N2**, **S**,
8: > **R**, **A**, **Panini** · **Tâche** : J10.1 · **Date** : 2026-11-14 · **Verdict** : ✅
9: >
10: > **Ce que ce rapport est.** La **relecture consolidée** des fiches du chantier, de J1.1 à J9.1 :
11: > les chiffres avant/après, les décisions, les rejets, les échecs de la boucle et ce qui reste.
12: > **Aucune mesure nouvelle** : chaque chiffre est celui de sa fiche, avec sa base, son contrôle
13: > négatif et sa limite. Le bilan **ne remplace pas** les fiches ; il les ordonne.
14: >
15: > **Base.** HEAD `81fc9ecf` (J9.1) ; gold vivant **612 phrases / 239 cibles / 3 179 jetons** ;
16: > gold gel
… [4574 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-chantier.md", "limit": 130, "offset": 220}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-chantier.md</path>
<type>file</type>
<content>
220: | **D3** | Publier le **schéma v2 additif** (`meta.partition`, `meta.alternative`), garder v1 lue | 26 cas / 0 échec ; 1 836 annotations / 0 échec ; v2 refuse v1 | ✅ ; invariants sémantiques à tester |
221: | **D4** | La **restitution v0** est un codec de surface, pas un décodeur ; ajouter la catégorie `C` | 46/46 surfaces ; miroir 0,1087 ; sans `C` 45/46 | ✅ ; v0.1 ponctuation, gold de restitution |
222: | **D14** | **Rejeter** la règle de l'adverbe final hors de la SUB (`g017`) | F1 0,7901 ; test −0,0028 ; attachement 236/237 | ✅ ; la convention du gold reste à trancher |
223: | **D15** | **Intégrer** la règle « REL suivie d'un GV → le sujet de ce GV » (`s065`) | 238/238 labels, 238/239 cibles, 0 span, 0 POS ; test unitaire | ✅ ; un seul cas, en dev |
224: | **D17** | La **forme canonique** est une lecture structurelle, **pas** un codec ; publier strict **et** canonique | canonique 46/46 ; strict 0,1087 inchangé ; strict sur canonique 1/46 | ✅ ; gold de forme canonique à faire |
225: 
226: ### 3.2 Panini
227: 
228: | # | décision | preuve | état / suite 
… [12677 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nb=json.load(open('reports/rapport-bilan-chantier.json'))\nw=json.load(open('reports/rapport-semaine.json'))\nerrors=[]\ndef check(name, got, exp):\n    if abs(got-exp)>1e-9: errors.append((name,got,exp))\n# compare to week report JSON\ncheck('F1 avant', b … [1464 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 19, in <module>
  File "<stdin>", line 6, in check
TypeError: unsupported operand type(s) for -: 'int' and 'str'
[exit code: 1]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nb=json.load(open('reports/rapport-bilan-chantier.json'))\nw=json.load(open('reports/rapport-semaine.json'))\nerrors=[]\ndef check(name, got, exp):\n    if abs(float(got)-float(exp))>1e-9: errors.append((name,got,exp))\ncheck('F1 avant', b['chiffres']['pro … [1413 caractères tronqués]`

  ```
retrieval-familles keys: ['tache', 'titre', 'date', 'ligne_roadmap', 'chantier', 'statut', 'question', 'sources', 'methode', 'couverture', 'global_532', 'lang_tree', 'echantillon_20', 'j31_21', 'union_39', 'verification_j31', 'comparaison_j31', 'epoque', 'controles_negatifs', 'limites', 'fichiers']
errors: []
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nf=json.load(open('reports/retrieval-familles.json'))\nfor k in ['global_532','lang_tree','echantillon_20','verification_j31','epoque']:\n    print('='*30,k)\n    v=f[k]\n    if isinstance(v,dict):\n        for kk,vv in v.items():\n            s=json.dumps … [288 caractères tronqués]`

  ```
============================== global_532
  n_requetes = 445
  n_candidats = 444
  agregats -> ['toutes', 'script_meme', 'script_different']
  par_famille -> ['Abkhaz-Adyge', 'Afro-Asiatic', 'Algic', 'Arawakan', 'Artificial Language', 'Atlantic-Congo', 'Austroasiatic', 'Austronesian', 'Chicham', 'Dravidian', 'Hmong-Mien', 'Indo-European', 'Mande', 'Mayan', 'Nilotic']
  par_script -> ['Arab', 'Cans', 'Cyrl', 'Deva', 'Hans', 'Latn', 'Mymr']
  top_paires -> list 20
  controles -> ['permutation_etiquettes', 'requetes_permutees']
  lignes -> list 445
============================== lang_tree
  n_langues = 25
  langues = ["arb", "ben", "cmn_hant", "dan", "deu_1996", "ell_monotonic", "eng", "fin", "fra", "heb", "hin", "hun", "ita", "jpn", "kor", "lat", "nld", "nob", "pes_1", "por_PT", "ron_2006", "san", "spa", "swe", "tur"]
  n_paires = 600
  epoque = 1948
  agregats -> ['toutes', 'script_meme', 'script_different', 'famille_meme', 'famille_differente', 'soeur', 'soeur_stricte', 'famille_autre_branche', 'script_meme_soeur', 'script_meme_famille_autre', 'script_meme_famille_differente', 'script_different_soeur', 'script_different_famille_meme', 'script_different_famille_differente']
  regres
… [2469 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nf=json.load(open('reports/retrieval-familles.json'))\nfor setname in ['lang_tree','echantillon_20']:\n    print('='*40,setname)\n    a=f[setname]['agregats']\n    for k in ['toutes','soeur','famille_differente','famille_autre_branche','script_meme_soeur'] … [389 caractères tronqués]`

  ```
======================================== lang_tree
toutes {'n_paires': 600, 'top1_moyen': 0.14705555555555555, 'top1_median': 0.03333333333333333, 'ic_bas': 0.03333333333333333, 'ic_haut': 0.9333333333333333, 'mrr_moyen': 0.24604793114771278}
soeur {'n_paires': 60, 'top1_moyen': 0.6188888888888889, 'top1_median': 0.6833333333333333, 'ic_bas': 0.03333333333333333, 'ic_haut': 1.0, 'mrr_moyen': 0.6898523975018575}
famille_differente {'n_paires': 324, 'top1_moyen': 0.04454732510288066, 'top1_median': 0.03333333333333333, 'ic_bas': 0.0, 'ic_haut': 0.13333333333333333, 'mrr_moyen': 0.14742749098171765}
famille_autre_branche {'n_paires': 216, 'top1_moyen': 0.16975308641975306, 'top1_median': 0.03333333333333333, 'ic_bas': 0.03333333333333333, 'ic_haut': 0.8875000000000001, 'mrr_moyen': 0.27069957296499864}
script_meme_soeur {'n_paires': 50, 'top1_moyen': 0.7359999999999998, 'top1_median': 0.8333333333333334, 'ic_bas': 0.26666666666666666, 'ic_haut': 1.0, 'mrr_moyen': 0.8011896294627598}
regressions {"j31_compatible": {"n_paires": 600, "variables": ["script_match", "famille_match", "chance"], "coef": {"constante": -0.020449989972574908, "script_match": 0.27008323180560706, "famille_match":
… [6646 caractères tronqués]
  ```

- **bash** `{"command": "git diff --check; echo '--- status'; git status --short; echo '--- our diff stat'; git diff --stat -- docs/pilotage/en-cours.md docs/pilotage/roadmap.md docs/pilotage/semaine-autonome.md reports/README.md", "description": "Check diff and status"}`

  ```
--- status
 M docs/pilotage/en-cours.md
 M docs/pilotage/roadmap.md
 M docs/pilotage/semaine-autonome.md
 M reports/INDEX.md
 M reports/README.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/plan.json
 m tools/structures
?? reports/rapport-bilan-chantier.json
?? reports/rapport-bilan-chantier.md
?? reports/rapport-s-paragraphes.md
--- our diff stat
 docs/pilotage/en-cours.md         |  13 +++--
 docs/pilotage/roadmap.md          |  10 ++++
 docs/pilotage/semaine-autonome.md | 113 ++++++++++++++++++++++++++++----------
 reports/README.md                 |   1 +
 4 files changed, 103 insertions(+), 34 deletions(-)
  ```

- **bash** `{"command": "wc -l -w reports/rapport-bilan-chantier.md reports/rapport-bilan-chantier.json docs/pilotage/semaine-autonome.md docs/pilotage/en-cours.md", "description": "Check file sizes"}`

  ```
432   6133 reports/rapport-bilan-chantier.md
  1347   4788 reports/rapport-bilan-chantier.json
   255   3225 docs/pilotage/semaine-autonome.md
   144   1628 docs/pilotage/en-cours.md
  2178  15774 total
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -3 && git add reports/rapport-bilan-chantier.md reports/rapport-bilan-chantier.json docs/pilotage/semaine-autonome.md docs/pilotage/en-cours.md docs/pilotage/roadmap.md reports/README.md && git status --short | grep -E '^[MA] ' ", "descri … [45 caractères tronqués]`

  ```
revue de documentation · 724 fiche(s) · 818 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
M  docs/pilotage/en-cours.md
M  docs/pilotage/roadmap.md
M  docs/pilotage/semaine-autonome.md
M  reports/README.md
A  reports/rapport-bilan-chantier.json
A  reports/rapport-bilan-chantier.md
  ```

- **bash** `{"command": "git commit -m \"J10.1 — LE BILAN DU CHANTIER : F1 0,7533 → 0,7902, ATTACHEMENT 236 → 238, 20/21 TÂCHES, 5 TIMEOUTS, 1 ÉCHEC (LE TAG) ; PANINI MESURÉ ET BORNÉ\n\nLe bilan relit les fiches J1.1–J9.1 : POS inchangée (0,8625), F1 0,7533 → 0,7902 (+0,0369),\nattachement 236/237 → 238/238 lab … [680 caractères tronqués]`

  ```
✅ index : aucun fait stagé sans état
[s/v7 03ecee41] J10.1 — LE BILAN DU CHANTIER : F1 0,7533 → 0,7902, ATTACHEMENT 236 → 238, 20/21 TÂCHES, 5 TIMEOUTS, 1 ÉCHEC (LE TAG) ; PANINI MESURÉ ET BORNÉ
 19 files changed, 4380 insertions(+), 58 deletions(-)
 create mode 100644 journal/sessions/session-ce875934-0cf6-4434-a91d-cbca647b11b3/digest.md
 create mode 100644 journal/sessions/session-ce875934-0cf6-4434-a91d-cbca647b11b3/rapport.md
 create mode 100644 reports/rapport-bilan-chantier.json
 create mode 100644 reports/rapport-bilan-chantier.md
  ```

- **bash** `{"command": "test -f reports/rapport-bilan-chantier.md && echo FICHE-OK; python3 tools/revue_documentation.py >/dev/null 2>&1; echo REVUE-$?; python3 tools/taille_documents.py 2>&1 | tail -3; echo '--- status'; git status --short | head -20", "description": "Run acceptance and final checks"}`

  ```
FICHE-OK
REVUE-0
     · 49 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
--- status
 M reports/INDEX.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/plan.json
 m tools/structures
?? reports/rapport-s-paragraphes.md
  ```

- **bash** `{"command": "git show --stat --oneline HEAD | head -30; echo '---'; git log --oneline -3", "description": "Inspect commit contents"}`

  ```
03ecee41 J10.1 — LE BILAN DU CHANTIER : F1 0,7533 → 0,7902, ATTACHEMENT 236 → 238, 20/21 TÂCHES, 5 TIMEOUTS, 1 ÉCHEC (LE TAG) ; PANINI MESURÉ ET BORNÉ
 docs/pilotage/en-cours.md                          |   13 +-
 docs/pilotage/roadmap.md                           |   10 +
 docs/pilotage/semaine-autonome.md                  |  113 +-
 journal/2026-11-14/README.md                       |    7 +-
 journal/2026-11-14/docs.md                         |    5 +-
 journal/2026-11-14/memoire.md                      |    2 +-
 journal/2026-11-14/mesures.md                      |    2 +-
 journal/2026-11-14/portes.md                       |    2 +-
 journal/README.md                                  |    5 +-
 journal/sessions/MANIFEST.md                       |    7 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md |    7 +
 .../rapport.md                                     |    8 +-
 .../digest.md                                      | 2049 ++++++++++++++++++++
 .../rapport.md                                     |  198 ++
 .../digest.md                                      |  181 ++
 .../rapport.md                                     |   49 +-
 reports/README.md                       
… [583 caractères tronqués]
  ```

- **bash** `{"command": "git show HEAD:reports/rapport-bilan-chantier.md | head -8; echo '...'; git show HEAD:reports/rapport-bilan-chantier.json | python3 -c \"import json,sys; d=json.load(sys.stdin); print('JSON HEAD ok', d['tache'], len(d['decisions']), len(d['rejets']))\"", "description": "Verify committed  … [17 caractères tronqués]`

  ```
# J10.1 — le bilan du chantier : F1 0,7533 → 0,7902, attachement 236 → 238, Panini mesuré et borné

> **Instantané historique** — les chiffres publiés ici sont ceux du commit de la fiche ; ils ne
> décrivent pas l'état courant. L'état courant du bloc est dans
> [`en-cours`](../docs/pilotage/en-cours.md) et [`la roadmap`](../docs/pilotage/roadmap.md).

> **Ligne de roadmap** : **B13** (le moteur de pensée), **R0.7** (le bloc langue), **N2**, **S**,
> **R**, **A**, **Panini** · **Tâche** : J10.1 · **Date** : 2026-11-14 · **Verdict** : ✅
...
JSON HEAD ok J10.1 20 30
  ```

- **bash** `{"command": "git show HEAD:docs/pilotage/semaine-autonome.md | grep -n \"J10.1\\|Bilan J10.1\\|Le bilan du 14/11\" | head; echo '---'; git show HEAD:docs/pilotage/en-cours.md | grep -n \"J10.1\\|724\\|14/11 00 h 30\" | head", "description": "Verify doc updates in commit"}`

  ```
11:> **Bilan J10.1 (14/11).** Le chantier est **mesuré et écrit** ; la **clôture formelle** (tag,
148:## 3 bis. L'état du chantier (14/11, 03 h 55 — après J10.1)
150:Le superviseur a lancé **21 tâches** (budget **22 032 s** au 14/11 03 h 46, hors J10.1). **20
174:| J10.1 bilan | ✅ fait | [`rapport-bilan-chantier.md`](../../reports/rapport-bilan-chantier.md) + JSON | `commit J10.1` |
209:| **J10** | le bilan | ✅ fait | [`rapport-bilan-chantier.md`](../../reports/rapport-bilan-chantier.md) + JSON : chiffres, décisions, rejets, échecs, reste | `commit J10.1` | J14.1 (passe + tag) |
226:## 9. Le bilan du 14/11 (J10.1)
---
95:- **J10.1 — le bilan** : **20/21** ; F1 **0,7533 → 0,7902**, attachement **236 → 238 labels**, POS inchangée ; **5 timeouts**, **1 échec** (J5.2, tag absent) ; **D1–D20**, **R1–R30** ; [bilan](../../reports/rapport-bilan-chantier.md) + JSON.
106:| fichiers / JSON de résultats | **724** / **818** | `reports/*.md` / `reports/*.json` |
108:| dernière passe | **14/11 00 h 30** (84, **81/3**) ; rouges tolérées `indice`, `melange`, `sessions` | `docs/pilotage/references-non-regression.md` |
  ```

- **bash** `{"command": "git show HEAD:reports/README.md | grep -n \"bilan\"; echo '---'; git show HEAD:docs/pilotage/roadmap.md | grep -n \"J10.1\" | head", "description": "Verify README and roadmap updates"}`

  ```
18:| [`rapport-bilan-chantier.md`](rapport-bilan-chantier.md) | **J10.1** — le bilan du chantier : F1 **0,7533 → 0,7902**, attachement **236 → 238**, Panini borné, **20/21**, 5 timeouts, 1 échec (le tag) |
113:| [`rapport-pensee-anaphore-bilan.md`](rapport-pensee-anaphore-bilan.md) | **B13** — le bilan de l'anaphore : 27/30, CV 0,847, huit mesures, **109/109** |
---
56:**J10.1 — le bilan du chantier.** **20 tâches sur 21** passent l'acceptation ; **5 timeouts**
  ```

- **bash** `{"command": "python3 tools/verifie_en_cours.py 2>&1 | tail -3; python3 tools/verifie_journal.py 2>&1 | tail -3; python3 tools/verifier_schemas.py 2>&1 | tail -3; bash tools/porte-tableaux.sh 2>&1 | tail -3", "description": "Final gate checks after commit"}`

  ```
en-cours · 1628 mots · 7 sections · 4 session(s) · 10 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  journal · 46 jour(s) · 185 session(s) · 2467 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
  schémas · 463 document(s) · 67 SVG · 2 source(s)
  ✅ aucun ASCII art, SVG valides et référencés, blocs PlantUML inline valides,
     sources et images relatives.
  ✅ 1789 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4101 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-14)
  ```

### 🤖 Assistant

**J10.1 terminé et committé** — `03ecee41`.

## Livrables

- `reports/rapport-bilan-chantier.md` (432 lignes, 6 133 mots) + `reports/rapport-bilan-chantier.json`
- `docs/pilotage/semaine-autonome.md` : § 3 bis (état 14/11), § 8 (jours J1–J10) et § 9 (bilan)
- `docs/pilotage/en-cours.md` : ligne J10.1, compteurs **724 / 818**, reste et prochaines actions
- `docs/pilotage/roadmap.md` : paragraphe J10.1 et suite J11–J14
- `reports/README.md` : fiche courante ajoutée

## Chiffres avant/après

| mesure | avant | après |
|---|---:|---:|
| POS (612) | 0,8625 | **0,8625** (0 token changé) |
| F1 syntagmes | 0,7533 | **0,7902** (+0,0369) |
| attachement | 236/237 labels (236/239 cibles, 0,9916) | **238/238 labels** (238/239 cibles, 0,9958) |
| schéma | v1 | **v2** (26 cas / 0 échec) |
| restitution | v0 : 46/46, strict 0,1087 | **v1** : canonique 46/46, strict 0,1087, 395/395/315/313 |
| tagger | 0,8625 | **0,9475** (+8,49) ; réel 432 **+4,67** |
| Panini | 0 mesure | table 14/14 ; corpus 418/438 ; J3.1 ; J3.2 ; J7.1 sœurs **0,619** contre **0,0445** |

## Bilan

- **20 tâches sur 21** passent l'acceptation ; **5 timeouts** (J1.2, J2.2, J3.1, J5.2, J8.1), **1 seul échec d'acceptation** : **J5.2** (tag absent).
- Le détail factuel corrige la formule « timeout après commit » : **J1.2** a bien committé avant son timeout ; **J2.2/J3.1** ont expiré **avant** le commit, récupéré par J3.2 (`c3467170`) ; **J8.1** a été committé après coup par J9.1 (`229098ec`). J5.2 reste rouge : le tag `semaine-2026-11-14` n'existe pas, et J14.1 doit poser `chantier-2026-11-14`.
- **D1–D20** décisions, **R1–R30** rejets ; le reste est nommé : `g017` (convention), `s065` (hors échantillon), split réel du tagger, V14 des 21 langues, porte N2, commit S, rapport A6.2, passe générique d'honnêteté, J11–J14.

## Vérifications

`FICHE-OK`, `REVUE-0`, T0 **3 998 / 4 000**, `verifie_en_cours`, `verifie_journal`, `verifier_schemas`, `porte-tableaux` : verts. Les modifications préexistantes (`reports/INDEX.md`, fiches d'audit, `tools/chantier/plan.json`, `tools/structures`, `rapport-s-paragraphes.md`) n'ont pas été touchées.

