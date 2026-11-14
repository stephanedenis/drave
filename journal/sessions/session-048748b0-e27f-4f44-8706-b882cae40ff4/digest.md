# Session DSH — relecture

- identifiant : `session-048748b0-e27f-4f44-8706-b882cae40ff4`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-13 23:11:32
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche J5.2 : la passe complète des portes (`bash tools/toutes-les-portes.sh`), le relevé des rouges, la mise à jour de `docs/pilotage/references-non-regression.md`, et un **tag annoté** `semaine-2026-11-14` sur le dernier commit vert. Ne pas forcer : si des rouges non nommées apparaissent, écris la fiche et ne tague pas.

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

### 🤖 Assistant

I'll start by reading the key documents for this task: the gates method, the non-regression references, and the current state.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/methode/portes.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/references-non-regression.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/methode/portes.md</path>
<type>file</type>
<content>
1: # Les portes : lancer, lire le verdict, ne pas se tromper de rouge
2: 
3: > Document de tâche, chargé depuis [`AGENTS.md`](../../AGENTS.md). À lire **avant de lancer ou de lire les portes**.
4: 
5: ## La commande
6: 
7: ```bash
8: bash tools/toutes-les-portes.sh
9: ```
10: 
11: Elle lance **toutes** les `tools/porte-*.sh`, séquentiellement, **sans s'arrêter à la première rouge** (on veut le
12: [tableau](../theorie/glossaire/entrees/tableau.md), pas la première tuile), et borne **chaque** [porte](../theorie/glossaire/entrees/porte.md) à `DELAI=1800` s. Durée observée d'une passe complète :
13: **1 h 30 – 2 h** sur Hauru (**83 portes** ; certaines entraînent de petits modèles, d'autres utilisent les [GPU](../theorie/glossaire/entrees/gpu-quadro-rtx-5000-miroir-vram-deport.md) ;
14: `porte-deepseek` est **hors réseau** et rapide). La dernière passe complète à **82 portes** (03/11 11 h 30, **machine au repos**, **1 h 48**) a donné
15: **80 vertes, 2 rouges** (les 2 connues : `indice`, `melange`) ;
16: `porte-reparti-moteur` (ré-étalonnée à 8,7434) et `porte-homeostasie` (
… [4409 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/references-non-regression.md</path>
<type>file</type>
<content>
1: # Références de non-régression
2: 
3: > **Passe — 2026-11-06 :** 83 portes, **79 vertes, 4 rouges** (voir la ligne `bloc-linguistique`).
4: 
5: > **Passe précédente — 2026-11-04 23 h 43 → 2026-11-05 02 h 12 :** **83 portes, 79 vertes,
6: > 4 rouges**, **2 h 29** (journaux durables `work/portes/passe-2404-23h45`), **machine au repos**
7: > (GPU libres, aucune réservation). Les **2 rouges structurelles connues** restent : `porte-indice`
8: > (1 207 s), `porte-melange` (148 s). Deux rouges nouvelles, **hors dépôt** : `porte-lecteur` (0 s)
9: > échouait sur une ancre du banc pilote (« < 2,5 ») que la réécriture de la roadmap du 04/11
10: > (« sous 2,5 ») avait rendue introuvable — **corrigée et rejouée verte** ; `porte-sessions` (0 s)
11: > signale les heartbeats périmés du hub et de `e181ce02` au moment de la passe — le hub l'a rafraîchi
12: > à 01 h 55, **`e181ce02` reste à rafraîchir par sa session**. Longues vertes : `greffe` **840 s**,
13: > `homeostasie` **755 s**, `profondeur-routee` **700 s**, `vision` **670 s**, `ocr-scans` **529 s**.
14: 
15: 
… [13278 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short && echo \"---BRANCH---\" && git branch --show-current && echo \"---LOG---\" && git log --oneline -15 && echo \"---TAGS---\" && git tag --list | tail -20", "description": "Check git state, log, tags"}`

  ```
M docs/pilotage/references-non-regression.md
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
---BRANCH---
s/v7
---LOG---
34e3e4ab J5.1 — LE RAPPORT DE SEMAINE : F1 0,7533 → 0,7902, ATTACHEMENT 236 → 237, TAGGER 0,9475 (+8,49, INTÉGRER), INTÉGRATION BORNÉE (TABLE 14/14, CORPUS 418/438), 13 DÉCISIONS, 21 REJETS
dc78f223 ÉTAT — T0 DANS LE BUDGET (3 991 MOTS) : LA LIGNE R0.7 PORTE LE TAGGER 612 (0,9475, +8,49, INTÉGRER)
a934d779 R0.7 — LE TAGGER POS SUR LE GOLD 612 : 0,9475 (3012/3179), +8,49 PTS, LA RÈGLE DIT INTÉGRER ; LA CLÉ ÉTAIT PRÉSENTE ET 0,8500 ÉTAIT DATÉ (0,8625)
ced21933 CHANTIER — PHASE 2 (12 H) : LE VERDICT ACCEPTATION D'ABORD (TIMEOUT APRÈS COMMIT = FAIT), 12 TÂCHES AJOUTÉES (J4 COORDINATION, J6 SPANS, J7-J10 PANINI/BILAN), ÉTAT CORRIGÉ
c7f26b35 DOCS — LA PASSE APRÈS LE CHANTIER : 8 FICHES INDEXÉES, L'ÉTAT PAR JOUR DU PLAN, LE JOURNAL DU CHANTIER, CHA
… [1239 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"===TAGS ALL===\" && git tag --list && echo \"===DIFF non-regression===\" && git diff docs/pilotage/references-non-regression.md && echo \"===STATUS===\" && git status --short", "description": "Inspect tags and pending diff"}`

  ```
===TAGS ALL===
===DIFF non-regression===
diff --git a/docs/pilotage/references-non-regression.md b/docs/pilotage/references-non-regression.md
index 1e1f58b8..d99dd15d 100644
--- a/docs/pilotage/references-non-regression.md
+++ b/docs/pilotage/references-non-regression.md
@@ -46,7 +46,7 @@
 | quoi | commande | attendu |
 |---|---|---|
 | tests unitaires | `cargo test --release` (dans `drave-core/`) | **138 tests** (le compte est dans la sortie) |
-| toutes les portes | `tools/toutes-les-portes.sh` | **83 portes** ; dernière passe **79 vertes, 4 rouges** (04/11 23 h 43 → 05/11 02 h 12, machine au repos) : 2 connues (`indice`, `melange`), 1 **corrigée** (`lecteur`, ancre du banc), 1 de **coordination** (`sessions`, heartbeat de `e181ce02`) · ⚠ **ne jamais lire une porte à travers un `tail`** |
+| toutes les portes | `tools/toutes-les-portes.sh` | **84 portes** ; voir la **passe du 07/11** ci-dessus · ⚠ **ne jamais lire une porte à travers un `tail`** |
 | une porte | `tools/porte-<nom>.sh` | la dernière ligne dit ce qu'elle verrouille |
 
 > **16/10 — l'audit des 46 portes** (deux vrais défauts corrigés, des faux positifs
===STATUS===
 M docs/pilotage/references-non-regression.md
 M r
… [371 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls journal/ | tail -20 && echo \"===PLAN===\" && python3 -c \"\nimport json\nd=json.load(open('tools/chantier/plan.json'))\nprint(type(d))\nprint(json.dumps(d, ensure_ascii=False)[:3000])\n\"", "description": "List journal and inspec … [8 caractères tronqués]`

  ```
2026-10-23
2026-10-24
2026-10-25
2026-10-26
2026-10-27
2026-10-28
2026-10-29
2026-10-30
2026-10-31
2026-11-01
2026-11-02
2026-11-03
2026-11-04
2026-11-05
2026-11-06
2026-11-07
2026-11-13
README.md
sessions
THEMES.md
===PLAN===
<class 'dict'>
{"nom": "Semaine 07/11 → 14/11 — le produit et l'intégration Panini", "principe": "Une tâche n'est finie que si son acceptation passe ; l'agent commite, le superviseur vérifie.", "taches": [{"id": "J0", "jour": 0, "titre": "Le contrôle du superviseur", "mandat": "Réponds exactement le mot OK, sans autre texte. C'est un test de liaison du superviseur.", "budget_min": 2, "acceptation": [{"commande": "python3 -c \"print('LIAISON-OK')\"", "attendu": "LIAISON-OK"}]}, {"id": "J1.1", "jour": 1, "titre": "r035 : la relative zéro", "mandat": "Tâche J1.1 du chantier : la relative zéro (r035, « The film she talks about is out. »). Reproduis, explique, propose UNE règle générale mesurée sur dev/test ; si elle tient (attachement 236→237, POS/F1 stables), intègre-la et commite avec une fiche `reports/rapport-r035.md` + `reports/pensee-r035.json`. Sinon, écris la fiche du rejet (chiffres, raison) et commite-la. Règles : ne touche pas S/D/N2 ; 183/183 portes ;
… [2042 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -c \"\nimport json\nd=json.load(open('tools/chantier/plan.json'))\nfor t in d['taches']:\n    if t['id'].startswith('J4') or t['id'].startswith('J5') or t['id'].startswith('J6'):\n        print('='*70)\n        print(t['id'], … [230 caractères tronqués]`

  ```
======================================================================
J4.1 | jour 4 | Coordination N2 — le mètre RoPE | budget 90
MANDAT: Tâche J4.1 : la coordination N2 — le mètre `eval_n2_propre.py` lit les checkpoints RoPE comme des positions absolues (8,02 au lieu de 2,79). **Ne modifie rien dans N2** (ni `entrainer_native.py`, ni `native_model.py`, ni `work/`). Écris une fiche de coordination `reports/rapport-coordination-n2.md` + JSON : le bug, le correctif proposé (--rope), les chiffres, la commande exacte pour la session N2.
  ACC: {'commande': 'test -f reports/rapport-coordination-n2.md && echo FICHE-OK', 'attendu': 'FICHE-OK'}
======================================================================
J4.2 | jour 4 | Coordination S — les 11 verdicts | budget 90
MANDAT: Tâche J4.2 : la coordination S — 11 verdicts de `/paragraphes` non committés. **Ne touche pas `tools/structures/`**. Fiche `reports/rapport-coordination-s.md` + JSON : la liste exacte des 11 verdicts (fichier, lignes, statuts), la commande de commit pour la session S, le risque d'un clone à 523d8c1.
  ACC: {'commande': 'test -f reports/rapport-coordination-s.md && echo FICHE-OK', 'attendu': 'FICHE-OK'}
========
… [3490 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la journal/2026-11-13 journal/2026-11-07 2>/dev/null && echo \"===13 INDEX===\" && cat journal/2026-11-13/*.md 2>/dev/null | head -100", "description": "List journal 13 and 07"}`

  ```
journal/2026-11-07:
total 44
drwxr-xr-x. 1 stephane stephane   132  7 nov 15:13 .
drwxr-xr-x. 1 stephane stephane   952 13 nov 21:34 ..
-rw-r--r--. 1 stephane stephane  3042  7 nov 18:21 distribue.md
-rw-r--r--. 1 stephane stephane  5092  7 nov 18:21 docs.md
-rw-r--r--. 1 stephane stephane  2798  7 nov 18:21 memoire.md
-rw-r--r--. 1 stephane stephane  6424  7 nov 18:21 mesures.md
-rw-r--r--. 1 stephane stephane  2233  7 nov 18:21 modele.md
-rw-r--r--. 1 stephane stephane  2679  7 nov 18:21 portes.md
-rw-r--r--. 1 stephane stephane 11408 13 nov 21:31 README.md

journal/2026-11-13:
total 16
drwxr-xr-x. 1 stephane stephane   76 13 nov 23:10 .
drwxr-xr-x. 1 stephane stephane  952 13 nov 21:34 ..
-rw-r--r--. 1 stephane stephane 1103 13 nov 23:10 distribue.md
-rw-r--r--. 1 stephane stephane 1516 13 nov 23:10 docs.md
-rw-r--r--. 1 stephane stephane 1321 13 nov 23:10 memoire.md
-rw-r--r--. 1 stephane stephane 1783 13 nov 23:10 README.md
===13 INDEX===
# 2026-11-13 — Régions, flux, protocoles, budgets, pannes

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, U
… [4150 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"semaine-2026\\|tag annoté\\|dernier commit vert\\|git tag\" --include=\"*.md\" --include=\"*.sh\" --include=\"*.py\" . 2>/dev/null | grep -v node_modules | head -40", "description": "Search tag conventions"}`

  ```
./reports/rapport-semaine.md:227:| **J5.2** | passe complète, revue docs, tag annoté, release | `toutes-les-portes.sh` ; `revue_documentation.py` ; tag | temps (~2 h) | — |
./journal/sessions/00221850-90de-4287-90ee-324a35e504cd/digest.md:3039:- **bash** `{"command": "cd ~/Data13TB/stephane/GitHub/mdserve && git tag -a v0.1.0 -m \"mdserve 0.1.0 — première version autonome\" && git push origin v0.1.0 2>&1 | tail -3 && gh release create v0.1.0 --title \"mdserve v0.1.0 — lecteur Markdown local autonome\" --notes \"Première version autonome, extraite de  … [513 caractères tronqués]`
./journal/sessions/00221850-90de-4287-90ee-324a35e504cd/digest.md:4572:- **bash** `{"command": "set -e\ncd ~/Data13TB/stephane/GitHub/mdserve\ngit tag -a v0.2.0 -m \"docwatch 0.2.0 — affichage vivant de collections documentaires\"\ngit push origin v0.2.0 2>&1 | tail -3\ngh release create v0.2.0 --title \"docwatch v0.2.0 — service d'affichage vivant de collections documentaires\" - … [511 caractères tronqués]`
./journal/sessions/00221850-90de-4287-90ee-324a35e504cd/digest.md:8022:- **bash** `{"command": "set -e\ncd ~/Data13TB/stephane/GitHub/Qtrinet/tools/docwatch\ngit tag -a v0.3.0 -m \"docwatch 0.3.0 — nav
… [1901 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"===DIFFSTAT===\" && git diff --stat && echo \"===PLAN DIFF===\" && git diff tools/chantier/plan.json | head -80 && echo \"===PENDING reports names===\" && git diff --name-only", "description": "Inspect pending modifications"}`

  ```
===DIFFSTAT===
 docs/pilotage/references-non-regression.md |   2 +-
 reports/pensee-coherence-fiches-v7.json    |  19 +
 reports/pensee-dev-test-v10.json           |   2 +-
 reports/pensee-quatre-modes.json           | 734 ++++++++++++++++-------------
 reports/rapport-audit-v7.md                |   6 +-
 reports/rapport-coherence-fiches-v7.md     |  17 +-
 reports/rapport-dev-test-v10.md            |   2 +-
 reports/rapport-pensee-v12.md              |   4 +-
 reports/rapport-spans-chunker.md           |  13 +-
 tools/chantier/plan.json                   | 116 +++++
 tools/structures                           |   0
 11 files changed, 577 insertions(+), 338 deletions(-)
===PLAN DIFF===
diff --git a/tools/chantier/plan.json b/tools/chantier/plan.json
index 21ea0cf4..b1ece0d6 100644
--- a/tools/chantier/plan.json
+++ b/tools/chantier/plan.json
@@ -306,6 +306,122 @@
      "attendu": "FICHE-OK"
     }
    ]
+  },
+  {
+   "id": "J11.1",
+   "jour": 11,
+   "titre": "Le produit — les exemples rejoués",
+   "mandat": "Tâche J11.1 : les exemples de la doc produit — rejoue les 5 blocs de `docs/produit/exemples.md` avec le code courant (F1 0,7902, 237/238, le schéma v2) et corrige les sorti
… [3038 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date && echo \"===work/portes===\" && ls -lat work/portes/ 2>/dev/null | head -20 && echo \"===work dirs===\" && ls -lat work/ | head -20 && echo \"===GPU===\" && nvidia-smi --query-gpu=index,name,memory.used,memory.total,utilization … [81 caractères tronqués]`

  ```
ven 13 nov 2026 23:11:54 EST
===work/portes===
total 24
drwxr-xr-x. 1 stephane stephane  1816  7 nov 18:22 ..
-rw-r--r--. 1 stephane stephane 13701  5 nov 02:05 passe-2404-23h45.log
drwxr-xr-x. 1 stephane stephane  3478  5 nov 01:54 passe-2404-23h45
drwxr-xr-x. 1 stephane stephane   360  4 nov 23:42 .
-rw-r--r--. 1 stephane stephane    17  4 nov 23:42 passe-2404-23h45.debut
drwxr-xr-x. 1 stephane stephane  1080  4 nov 08:31 passe-1104-08h00
drwxr-xr-x. 1 stephane stephane  3432  3 nov 13:07 passe-0303-11h30
drwxr-xr-x. 1 stephane stephane  3432  3 nov 05:42 passe-0303-04h10
-rw-r--r--. 1 stephane stephane   322  2 nov 21:57 tableaux-rejeu.log
drwxr-xr-x. 1 stephane stephane  3392  2 nov 21:13 passe-1102-19h32
drwxr-xr-x. 1 stephane stephane    22  2 nov 16:45 passe-1102-apres-n2
drwxr-xr-x. 1 stephane stephane   316  2 nov 16:35 sous-passe-1102-16h35
===work dirs===
total 220
drwxr-xr-x. 1 stephane stephane    82 13 nov 21:38 chantier
drwxr-xr-x. 1 stephane stephane  3370  7 nov 18:50 portes-1107-16h48
drwxr-xr-x. 1 stephane stephane    88  7 nov 18:22 portes-1107-18h22
drwxr-xr-x. 1 stephane stephane  1816  7 nov 18:22 .
drwxr-xr-x. 1 stephane stephane   242  7 nov 18:18 portes-11
… [1070 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ps aux | grep -E \"toutes-les-portes|porte-.*\\.sh\" | grep -v grep | head -20; echo \"---\"; ls -la work/portes/ 2>/dev/null | head", "description": "Check running gates"}`

  ```
stephane 1032921 21.9  0.1 1880736 238892 ?      Rl   23:11   0:05 node26 /home/stephane/.local/share/../bin/dsh --profile headless Tâche J5.2 : la passe complète des portes (`bash tools/toutes-les-portes.sh`), le relevé des rouges, la mise à jour de `docs/pilotage/references-non-regression.md`, et un **tag annoté** `semaine-2026-11-14` sur le dernier commit vert. Ne pas forcer : si des rouges non nommées apparaissent, écris la fiche et ne tague pas.
---
total 24
drwxr-xr-x. 1 stephane stephane   360  4 nov 23:42 .
drwxr-xr-x. 1 stephane stephane  1816  7 nov 18:22 ..
drwxr-xr-x. 1 stephane stephane  3432  3 nov 05:42 passe-0303-04h10
drwxr-xr-x. 1 stephane stephane  3432  3 nov 13:07 passe-0303-11h30
drwxr-xr-x. 1 stephane stephane  3392  2 nov 21:13 passe-1102-19h32
drwxr-xr-x. 1 stephane stephane    22  2 nov 16:45 passe-1102-apres-n2
drwxr-xr-x. 1 stephane stephane  1080  4 nov 08:31 passe-1104-08h00
drwxr-xr-x. 1 stephane stephane  3478  5 nov 01:54 passe-2404-23h45
-rw-r--r--. 1 stephane stephane    17  4 nov 23:42 passe-2404-23h45.debut
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for d in work/portes-1107-18h22 work/portes-1107-18h17 work/portes-1107-16h48; do echo \"=== $d ===\"; ls -la \"$d\" | head; if [ -f \"$d/registre.txt\" ]; then echo \"--- registre reds ---\"; awk '$2 != 0' \"$d/registre.txt\"; echo  … [97 caractères tronqués]`

  ```
=== work/portes-1107-18h22 ===
total 12
drwxr-xr-x. 1 stephane stephane   88  7 nov 18:22 .
drwxr-xr-x. 1 stephane stephane 1816  7 nov 18:22 ..
-rw-r--r--. 1 stephane stephane  418  7 nov 18:22 porte-etat.log
-rw-r--r--. 1 stephane stephane  388  7 nov 18:22 porte-sessions.log
-rw-r--r--. 1 stephane stephane   61  7 nov 18:22 registre.txt
--- registre reds ---
porte-sessions 1 0
--- 1 vertes, 1 rouges ---
--- count ---
3
=== work/portes-1107-18h17 ===
total 28
drwxr-xr-x. 1 stephane stephane  242  7 nov 18:18 .
drwxr-xr-x. 1 stephane stephane 1816  7 nov 18:22 ..
-rw-r--r--. 1 stephane stephane 1035  7 nov 18:17 porte-bloc-tableaux.log
-rw-r--r--. 1 stephane stephane 1175  7 nov 18:18 porte-document.log
-rw-r--r--. 1 stephane stephane  418  7 nov 18:18 porte-etat.log
-rw-r--r--. 1 stephane stephane  453  7 nov 18:18 porte-registre.log
-rw-r--r--. 1 stephane stephane  388  7 nov 18:18 porte-sessions.log
-rw-r--r--. 1 stephane stephane  279  7 nov 18:18 porte-tableaux.log
-rw-r--r--. 1 stephane stephane  143  7 nov 18:18 registre.txt
--- registre reds ---
porte-sessions 1 0
--- 5 vertes, 1 rouges ---
--- count ---
7
=== work/portes-1107-16h48 ===
total 348
drwxr-xr-x. 1 stephane ste
… [719 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== log references ===\" && git log --oneline -8 -- docs/pilotage/references-non-regression.md && echo \"=== show HEAD refs top ===\" && git show HEAD:docs/pilotage/references-non-regression.md | head -30 && echo \"=== last co … [99 caractères tronqués]`

  ```
=== log references ===
d73e7d1f DOCS — LE LIEN DE LA FICHE COMPOSITION CORRIGÉ
2b3e1796 B13 — LES COMPOSITIONS NE PERDENT PLUS : CASCADE = HEURISTIQUE (0,8383, 235/236), VERDICT COMPARATIF RESTAURÉ ; 183/183
5c6b3b43 PORTES — LA NUANCE cascade_pos : VERTE PAR PLANCHER, LA FUSION DÉGRADE ENCORE LE POS DE 1,16 PT (CORRECTIF À FAIRE)
b2196cc7 PILOTAGE — LE PREMIER PRODUIT EST DEBOUT : DRAVE, PORTE PRODUIT, DOC D'USAGE ; 84 PORTES, 3 ROUGES
789b1284 DOCS — LA PASSE DU 06/11 EN UNE LIGNE ET L'ANCIENNE COMPRESSÉE (BUDGET T1)
f0e3f46a DOCS — LA PASSE DU 06/11 EN UNE LIGNE
b578f95b DOCS — LA PASSE DU 06/11 EN DEUX LIGNES (BUDGET T1)
ea7d3275 PORTES — LA PASSE COMPLÈTE DU 06/11 CONSIGNÉE : 79 VERTES / 4 ROUGES (2 STRUCTURELLES, SESSIONS D'AUTRUI, CASCADE_POS DOCUMENTÉE)
=== show HEAD refs top ===
# Références de non-régression

> **Passe — 2026-11-06 :** 83 portes, **79 vertes, 4 rouges** (voir la ligne `bloc-linguistique`).

> **Passe précédente — 2026-11-04 23 h 43 → 2026-11-05 02 h 12 :** **83 portes, 79 vertes,
> 4 rouges**, **2 h 29** (journaux durables `work/portes/passe-2404-23h45`), **machine au repos**
> (GPU libres, aucune réservation). Les **2 rouges structurelles connues** reste
… [2495 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== structures status ===\" && git -C tools/structures status --short | head -20 && echo \"=== submodule log ===\" && git -C tools/structures log --oneline -3 && echo \"=== all porte scripts count ===\" && ls tools/porte-*.sh  … [134 caractères tronqués]`

  ```
=== structures status ===
 M donnees/paragraphes-validations.jsonl
=== submodule log ===
523d8c1 S — LE FAIT DIVERS EST TRANCHÉ : 61/61 TYPES, 144/144 RÔLES ; LA TÊTE DU GN ARRÊTE LE VERBE
4012729 S — LA BANQUE DE PARAGRAPHES PASSE À NEUF : SIX PAIRES D'ALICE, SOURCES ANGLAISES ET RÉFÉRENTS
7ccc60f S — VALIDATION HUMAINE : 8 VERDICTS DE RÉFÉRENTS SUR /PARAGRAPHES (a001–a003) + 8 VERDICTS BANQUE (p003, c010, c066, c067)
=== all porte scripts count ===
84
=== script ===
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
# Ce que fait ce script, et ce qu'au
… [3273 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls tools/porte-*.sh | sed 's|tools/||' | tr '\\n' ' ' && echo && echo \"=== sessions ===\" && ls journal/sessions/ | head && python3 tools/verifie_sessions.py 2>&1 | tail -20", "description": "List gates and check sessions"}`

  ```
porte-adaptateur-sortie.sh porte-audit-drapeaux.sh porte-b1110-hybride.sh porte-balayage.sh porte-bloc-code.sh porte-bloc-linguistique.sh porte-bloc-maths.sh porte-bloc-tableaux.sh porte-budget.sh porte-bus.sh porte-bus-socket.sh porte-c4-retard.sh porte-cerveau.sh porte-consolidation.sh porte-coupe.sh porte-cycle-c2.sh porte-deepseek.sh porte-delais.sh porte-diff-couche.sh porte-document.sh porte-echange-experts.sh porte-episodique.sh porte-etat.sh porte-flux.sh porte-fusion.sh porte-gain.sh porte-greffe.sh porte-harnais-invariants.sh porte-homeostasie.sh porte-horloge.sh porte-indice.sh porte-jeux.sh porte-jumeaux.sh porte-lecteur.sh porte-lecture.sh porte-m5-brouillon.sh porte-melange.sh porte-memoire.sh porte-miroir-blocs.sh porte-mistral.sh porte-n3-cache.sh porte-n3-composition.sh porte-n3-deux-processus.sh porte-n3-deux-regions.sh porte-n3-generation.sh porte-n3-inventaire.sh porte-n3-placement.sh porte-n3-pont.sh porte-n3-positions.sh porte-n3-profondeur.sh porte-n3-refus.sh porte-n3-reseau.sh porte-n3-routes.sh porte-n3-service-briques.sh porte-n3-service.sh porte-n3-seuil.sh porte-n3-sparsite-compte.sh porte-n3-sparsite.sh porte-occupation-elagage.sh porte-occupation-mote
… [998 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la --time-style=+%H:%M reports/pensee-quatre-modes.json reports/rapport-spans-chunker.md tools/chantier/plan.json docs/pilotage/references-non-regression.md reports/rapport-s-paragraphes.md && echo \"=== dsh processes ===\" && ps … [146 caractères tronqués]`

  ```
-rw-r--r--. 1 stephane stephane 14098 15:57 docs/pilotage/references-non-regression.md
-rw-r--r--. 1 stephane stephane 18573 10:37 reports/pensee-quatre-modes.json
-rw-------. 1 stephane stephane 15801 16:03 reports/rapport-spans-chunker.md
-rw-r--r--. 1 stephane stephane  3859 09:46 reports/rapport-s-paragraphes.md
-rw-r--r--. 1 stephane stephane 18388 23:05 tools/chantier/plan.json
=== dsh processes ===
 264909 mer nov  4 09:39:31 2026 node /home/stephane/.local/share/../bin/dsh --profile dsh-tui --resume e181ce02-cd50-488a-a6be-e84b79d40dcc
 287431 mer nov  4 10:39:34 2026 node /home/stephane/.local/share/../bin/dsh --profile dsh-tui
1032921 ven nov 13 23:11:30 2026 node26 /home/stephane/.local/share/../bin/dsh --profile headless Tâche J5.2 : la passe complète des portes (`bash tools/toutes-les-portes.sh`), le relevé des rouges, la mise à jour de `docs/pilotage/references-non-regression.md`, et un **tag annoté** `semaine-2026-11-14` sur le dernier commit vert. Ne pas forcer : si des rouges non nommées apparaissent, écris la fiche et ne tague pas.
2041058 jeu nov  5 10:41:40 2026 node /home/stephane/.local/share/../bin/dsh --profile dsh-tui
  ```

### 🤖 Assistant

The gates pass is the long pole (~2 h), so I'll start it now on an idle machine (both GPUs free, no other gate running), with a durable log.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && test ! -e work/portes/passe-1311-23h15 && mkdir -p work/portes/passe-1311-23h15 && JOURNAUX=work/portes/passe-1311-23h15 bash tools/toutes-les-portes.sh > work/portes/passe-1311-23h15.log 2>&1; echo \"PASS_EXIT=$?\"", "description":  … [63 caractères tronqués]`

  ```
started background job bash-15
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '190,260p' reports/rapport-semaine.md && echo \"=== semaine-autonome J5 ===\" && sed -n '80,200p' docs/pilotage/semaine-autonome.md", "description": "Read weekly report tail and plan day 5"}`

  ```
| **R1** | L'**adverbe large** (tout `ADV` final hors GV) | F1 0,7552 (+0,0003) ; test 0,7656 < 0,7663 | 12 FP d'adverbe corrigés, 11 FP de troncature créés ; le gold se contredit |
| **R2** | L'**objet hors du GV** | F1 0,7531 (en baisse) | 20 FP d'objet corrigés, 13 FP de troncature créés |
| **R3** | Le **placebo sujet** (déplacer le premier token sans condition) | F1 0,7758 ; 38 phrases perdantes | 0 phrase perdante pour la règle conditionnelle |
| **R4** | Le **placebo adverbe** (arrêter au dernier token) | F1 0,7440 ; 627 FP contre 555 | tronquer au hasard détruit des GV |
| **R5** | « Le **schéma v2** prouve le sens » | 26 cas / 0 échec | il valide la **forme**, pas la réciprocité, les rangs ni l'unicité |
| **R6** | **Corriger** les 20 écarts de surface Panini ↔ Drave | 20 exclus sur 438 appariables | corriger une source pour l'autre **fabrique** l'accord |
| **R7** | Un **effet d'époque** dans le retrieval | brut 0,238 vs 0,427 ; à script contrôlé 0,710 vs 0,710 ; date −0,034, p = 0,19 | effet de **composition** (60 % vs 33 % de même écriture) |
| **R8** | « La **filiation** de Panini = la **famille** de Drave » | 3/655 paires inter-langues, 479 avec une langue vide | deux
… [16105 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
1: # En ce moment
2: 
3: **Mis à jour : 2026-11-13, 23 h 10 HNE (heure locale, EST).**
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
… [11279 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/methode/resultats.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/methode/resultats.md</path>
<type>file</type>
<content>
1: # Ce qu'un résultat doit porter
2: 
3: > Document de tâche, chargé depuis [`AGENTS.md`](../../AGENTS.md). À lire **avant d'écrire une fiche**, un JSON de
4: > résultats, ou un message de commit.
5: 
6: ## Les cinq pièces d'un résultat
7: 
8: 1. **Le chiffre** — la valeur, avec son [unité](../theorie/glossaire/entrees/unite.md) et son arrondi utile (jamais plus de chiffres que l'instrument n'en
9:    [porte](../theorie/glossaire/entrees/porte.md)) ;
10: 2. **La mesure qui le produit** — le calcul exact, la métrique ([chrF](../theorie/glossaire/entrees/chrf.md), précision, rappel, [AUC](../theorie/glossaire/entrees/auc.md)…), et ce qu'elle ne
11:    mesure pas ;
12: 3. **Le dispositif** — quel [corpus](../theorie/glossaire/entrees/corpus.md) (et sa provenance), quel modèle (taille, [quantification](../theorie/glossaire/entrees/quantification.md), date de coupure),
13:    quelles **couches de neurones** sondées, quel découpage, **quelle unité de mesure** (unité de sens ou unité
14:    grammaticale ; si c'est un [jeton](../theorie/glossaire/entrees/jeton.md), le dire co
… [2865 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,120p' tools/revue_documentation.py && echo \"=== verifie_en_cours ===\" && sed -n '1,80p' tools/verifie_en_cours.py", "description": "Read revue and en-cours checker"}`

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
… [5863 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"dernière passe\\|compte_portes\\|fiches\\|json\\|docs\\b\\|date\" tools/revue_documentation.py | head -50 && echo \"=== etat a jour ===\" && cat tools/verifie_etat_a_jour.py", "description": "Read counters checks and state  … [11 caractères tronqués]`

  ```
5:  1. classement : pas de résultats dans docs/ (les fiches sont dans reports/ et citées) ;
7:  3. annotation : les liens relatifs des docs/ et reports/ résolvent, et leur libellé ne
9:  4. fraîcheur  : en-cours.md date du dernier commit, ET aucun fait n'a été commité après
10:     le dernier état (comparaison de commits, pas de dates : voir verifie_etat_a_jour.py) ;
12:     les compteurs de la page d'état sont ceux du disque (portes, chapitres, fiches, docs) ;
22:from datetime import date
30:    r"`((?:docs|reports|tools|journal|data|drave-core|sprints)/"
31:    r"[^`\s]+?\.(?:md|json|sh|py|rs|txt|svg|csv|jsonl))`"
43:def date_dernier_commit() -> str:
46:            ["git", "log", "-1", "--format=%ad", "--date=short"], cwd=RACINE, text=True
52:def date_dernier_changement(chemin: str) -> str:
55:            ["git", "log", "-1", "--format=%ad", "--date=short", "--", chemin],
67:    return [p for p in (RACINE / "docs").rglob("*.md")
72:    return list((RACINE / "docs").rglob("*.md"))
82:            + [RACINE / "docs/README.md", RACINE / "README.md",
93:    """Les fichiers dont les liens doivent résoudre (docs, fiches courantes, racine)."""
100:def compte_portes() -> int:
105:    retu
… [10724 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"tag\" docs/pilotage/roadmap.md docs/pilotage/semaine-autonome.md docs/methode/*.md | head -30", "description": "Search tag conventions in pilotage docs"}`

  ```
docs/pilotage/roadmap.md:31:| **B — l'intelligence** | langue, pensée, jeux, maîtres, [banc externe](../theorie/glossaire/entrees/banc-externe.md), sémantique, modules | ✅ B1–B12 ; **B1.5 [corpus](../theorie/glossaire/entrees/corpus.md)**, **B12.10, B10.2bis et B11.10 closes** ; le **décodeur** est levé (objectif mot : 32,5 ; JW 26,7), le `z` reste ; **B13** (moteur de pensée) : state store v0 + **AC-3/alpha-bêta** + **[DRVF](../theorie/glossaire/entrees/drvf.md) `thought`** + **[banc](../theorie/glossaire/entrees/banc.md) anytime** + **opérateurs hétérogènes** + **nécessaire** + **labyrinthe** + **[porte](../theorie/glossaire/entrees/porte.md)** + **apprise** + **courbe** + **seule** + **stochastique** + **sto seule** + **ferme** + **minute** + **minute apprise** + **minute seule** + **minute entraînée** + **shaping** + **réseau** + **MLP** + **[professeur](../theorie/glossaire/entrees/professeur.md)** + **sans None** + **correction** + **audit** + **ouverte** + **graines** + **mobile** + **mobile graines** + **bruit** + **bouge** + **bouge graines** + **période** + **phase** + **phase graines** + **aléatoire** + **hasard** + **partielle** + **croyance** + **curiosité** + **observ
… [10621 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && tail -8 work/portes/passe-1311-23h15.log && echo \"=== registre ===\" && cat work/portes/passe-1311-23h15/registre.txt 2>/dev/null | tail -5", "description": "Check gates progress"}`

  ```
=== PASSE COMPLÈTE DES PORTES (84 portes, borne 1800 s) ===
    journaux : work/portes/passe-1311-23h15
=== registre ===
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== 03/11 adaptateur ===\" && grep -E \"✅|❌|TENUE\" work/portes/passe-0303-11h30/porte-adaptateur-sortie.log | tail -1 && echo \"=== 07/11 adaptateur ===\" && grep -E \"✅|❌|TENUE\" work/portes-1107-16h48/porte-adaptateur-sorti … [259 caractères tronqués]`

  ```
=== 03/11 adaptateur ===
  ✅ porte tenue (écriture fidèle · invariant · effet · refus)
=== 07/11 adaptateur ===
  ✅ porte tenue (écriture fidèle · invariant · effet · refus)
=== 07/11 melange ===
  ❌ l'état de A ne rend pas le code de A dans une
=== 07/11 log tail ===
=== 2. CALIBRATION : quelle position porte vraiment le contenu ? ===
  ❌ l'état de A ne rend pas le code de A dans une
     invite qui n'en contient aucun : le mélange ne pourrait rien dire
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls reports/ | grep -i \"passe\\|pass\" && echo \"=== reports json pass ===\" && ls reports/*passe* 2>/dev/null; ls reports/*.json | tail -5", "description": "Find prior pass fiches"}`

  ```
historique-passes-portes.md
pensee-passifs-corriges.json
pensee-passifs.json
pensee-passifs-sans-par.json
pensee-troisieme-passe.json
rapport-passage-a-l-echelle.md
rapport-passe-complete-13-octobre.md
rapport-passe-complete-portes.md
rapport-passe-k3-disque.md
rapport-pensee-passifs-corriges.md
rapport-pensee-passifs.md
rapport-pensee-passifs-sans-par.md
rapport-pensee-troisieme-passe.md
=== reports json pass ===
reports/historique-passes-portes.md
reports/pensee-troisieme-passe.json
reports/rapport-passe-complete-13-octobre.md
reports/rapport-passe-complete-portes.md
reports/rapport-passe-k3-disque.md
reports/rapport-pensee-troisieme-passe.md
reports/xnli-3b.json
reports/xnli-3b-l30.json
reports/xnli-entrainement-3b.json
reports/xnli-mlp-3b.json
reports/xnli-train-complet-3b.json
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-passe-complete-portes.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-passe-complete-portes.md</path>
<type>file</type>
<content>
1: # Passe COMPLÈTE des portes : de 22 à 47 portes — et une porte qui était verte en ne mesurant RIEN
2: 
3: > Campagne : **outillage** · expérience : la passe complète (`tools/toutes-les-portes.sh`)
4: > Question : les portes du dépôt passent-elles **toutes**, quand on les lance **toutes** ?
5: > Verdict : **oui, à chaque passe** — **22 sur 22** au premier passage (2026-10-10, 11 h 07), puis les passes
6: > successives consignées ci-dessous, jusqu'à la **47ᵉ porte** (`porte-diff-couche`, ajoutée le 24/10 — elle vérifie
7: > la reproductibilité du flux et nomme les divergences). Et la passe a trouvé ce qu'une porte lancée seule ne
8: > pouvait pas montrer : `porte-tokenizer-kimi` sortait **verte en comparant zéro jeton** (elle lisait `stdin`, que
9: > personne ne lui fournissait). Corrigée, elle compare maintenant **10 textes** en **7,5 s**.
10: >
11: > *Les sections 2 bis à 2 quater consignent les passes historiques ; la section 2 quinquies attend le verdict de
12: > la passe du 24/10 (47 portes) — elle n'est pas écrite d'avance.*
13: > Date réelle : **
… [11596 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && head -40 reports/historique-passes-portes.md && echo \"...\" && tail -40 reports/historique-passes-portes.md", "description": "Read pass history fiche"}`

  ```
# Historique des passes de portes

> **Document daté — dernière vérification : 2026-10-27.** Ce fichier conserve les
> passes complètes antérieures à la dernière (26/10 14 h 30). Les repères courants
> sont dans [`docs/pilotage/references-non-regression.md`](../docs/pilotage/references-non-regression.md).
> Il est **hors du chargement par défaut** : on y va pour retrouver une valeur ou une
> durée ancienne, pas pour connaître l'état courant.

> **2026-10-11 06 h 30 HAE** (heure lue sur la machine). Ces valeurs sont les **verdicts imprimés
> par la passe complète des portes** (`tools/toutes-les-portes.sh`, **34 vertes sur
> 34**, 85 min 8 s). Elles ne sont pas recopiées de mémoire : elles sortent du journal de la
> passe. **Une modification du chemin d'exécution qui déplace l'un de ces chiffres a changé le
> calcul** — il faut alors relancer la porte, comprendre, et écrire à côté de l'ancienne valeur
> (jamais à sa place).
>
> Détail complet : `reports/rapport-passe-complete-portes.md`.
> Les mesures de campagne (perplexités, budgets, latences) sont dans `reports/` — une fiche par
> expérience — et non ici : ce fichier ne porte que ce qu'une **porte** vérifie.
>
> **Passe du 2026-10
… [5379 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && tail -6 work/portes/passe-1311-23h15.log && echo \"---\" && cat work/portes/passe-1311-23h15/registre.txt 2>/dev/null", "description": "Check gates progress"}`

  ```
=== PASSE COMPLÈTE DES PORTES (84 portes, borne 1800 s) ===
    journaux : work/portes/passe-1311-23h15
---
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date && ls -la work/portes/passe-1311-23h15/ && echo \"=== log ===\" && cat work/portes/passe-1311-23h15.log && echo \"=== ps ===\" && ps -eo pid,etime,args | grep -E \"porte-|toutes-les-portes|dsh --profile headless\" | grep -v grep … [47 caractères tronqués]`

  ```
ven 13 nov 2026 23:12:59 EST
total 4
drwxr-xr-x. 1 stephane stephane  54 13 nov 23:12 .
drwxr-xr-x. 1 stephane stephane 432 13 nov 23:12 ..
-rw-r--r--. 1 stephane stephane  86 13 nov 23:12 porte-adaptateur-sortie.log
=== log ===
=== PASSE COMPLÈTE DES PORTES (84 portes, borne 1800 s) ===
    journaux : work/portes/passe-1311-23h15
=== ps ===
1032921       01:27 node26 /home/stephane/.local/share/../bin/dsh --profile headless Tâche J5.2 : la passe complète des portes (`bash tools/toutes-les-portes.sh`), le relevé des rouges, la mise à jour de `docs/pilotage/references-non-regression.md`, et un **tag annoté** `semaine-2026-11-14` sur le dernier commit vert. Ne pas forcer : si des rouges non nommées apparaissent, écris la fiche et ne tague pas.
1033400       00:38 bash -c cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && test ! -e work/portes/passe-1311-23h15 && mkdir -p work/portes/passe-1311-23h15 && JOURNAUX=work/portes/passe-1311-23h15 bash tools/toutes-les-portes.sh > work/portes/passe-1311-23h15.log 2>&1; echo "PASS_EXIT=$?"
1033408       00:38 bash tools/toutes-les-portes.sh
1033419       00:38 timeout 1800 bash tools/porte-adaptateur-sortie.sh
1033420       00:38 bash tool
… [249 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls .git/hooks/ | grep -v sample && echo \"=== pre-commit ===\" && cat .git/hooks/pre-commit 2>/dev/null | head -60", "description": "Inspect git hooks"}`

  ```
pre-commit
=== pre-commit ===
#!/bin/sh
# pre-commit — l'état accompagne le fait, le journal accompagne le code.
#
# Versionné dans tools/hooks/ et installé par tools/installe_hooks.sh : un hook qui
# ne vit que dans .git/hooks ne survit ni au clone ni au nettoyage.
set -u
cd "$(git rev-parse --show-toplevel)" || exit 0

# 1. Aucun fait (reports/, roadmap, backlog) ne se commite sans sa ligne d'état.
#    C'est la garantie de fraîcheur de docs/pilotage/en-cours.md : elle ne dépend
#    pas de la survie d'une session « principale », elle est vérifiée au commit.
if ! python3 tools/verifie_etat_a_jour.py --index; then
    echo "  ⛔ commit refusé : un fait sans ligne d'état."
    echo "     mets docs/pilotage/en-cours.md à jour, puis :"
    echo "     git add docs/pilotage/en-cours.md"
    exit 1
fi

# 2. Archive les traces de session DSH avant chaque commit : le journal doit
#    accompagner le code, pas le suivre.
python3 tools/archive_sessions.py --quiet >/dev/null || { echo "  ⛔ archivage des sessions en échec"; exit 1; }
python3 tools/session_report.py --quiet >/dev/null || { echo "  ⛔ rapport de session en échec"; exit 1; }
# Le journal du jour, par thème (sources : git + journal
… [264 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,80p' docs/pilotage/roadmap.md", "description": "Read roadmap head"}`

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
… [14824 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls tools/ | grep -i \"porte\\|registre\" && echo \"=== grep rapports passe json ===\" && grep -rln \"registre.txt\" reports/*.md tools/*.py 2>/dev/null | head", "description": "Find pass tooling"}`

  ```
exporter_gguf_dense.py
exporter_gguf.py
importer_udhr.py
porte-adaptateur-sortie.sh
porte-audit-drapeaux.sh
porte-b1110-hybride.sh
porte-balayage.sh
porte-bloc-code.sh
porte-bloc-linguistique.sh
porte-bloc-maths.sh
porte-bloc-tableaux.sh
porte-budget.sh
porte-bus.sh
porte-bus-socket.sh
porte-c4-retard.sh
porte-cerveau.sh
porte-consolidation.sh
porte-coupe.sh
porte-cycle-c2.sh
porte-deepseek.sh
porte-delais.sh
porte-diff-couche.sh
porte-document.sh
porte-echange-experts.sh
porte-episodique.sh
porte-etat.sh
porte-flux.sh
porte-fusion.sh
porte-gain.sh
porte-greffe.sh
porte-harnais-invariants.sh
porte-homeostasie.sh
porte-horloge.sh
porte-indice.sh
porte-jeux.sh
porte-jumeaux.sh
porte-lecteur.sh
porte-lecture.sh
porte-m5-brouillon.sh
porte-melange.sh
porte-memoire.sh
porte-miroir-blocs.sh
porte_mistral.py
porte-mistral.sh
porte_moteur.py
porte-n3-cache.sh
porte-n3-composition.sh
porte-n3-deux-processus.sh
porte-n3-deux-regions.sh
porte-n3-generation.sh
porte-n3-inventaire.sh
porte-n3-placement.sh
porte-n3-pont.sh
porte-n3-positions.sh
porte-n3-profondeur.sh
porte-n3-refus.sh
porte-n3-reseau.sh
porte-n3-routes.sh
porte-n3-service-briques.sh
porte-n3-service.sh
porte-n3-seuil.sh
porte-n3
… [789 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && tail -5 work/portes/passe-1311-23h15.log && echo \"--- registre ---\" && cat work/portes/passe-1311-23h15/registre.txt 2>/dev/null", "description": "Check pass progress"}`

  ```
=== PASSE COMPLÈTE DES PORTES (84 portes, borne 1800 s) ===
    journaux : work/portes/passe-1311-23h15
--- registre ---
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat tools/porte-tableaux.sh", "description": "Read porte-tableaux"}`

  ```
#!/bin/bash
# porte-tableaux.sh — un tableau Markdown qui ne rend pas est un tableau qui n'existe PAS.
#
# POURQUOI CETTE PORTE EXISTE. Le 13/10, le premier tableau de `docs/etat-cerveau.md` s'affichait
# comme du TEXTE dans docwatch : une seule ligne (`| **C2 (cycle 2 régions)** | … |`) avait
# **4 cellules pour 5 colonnes** — un lien qui avait glissé d'une colonne. Le rendu (mistune,
# puis markdown_it, puis markdown) refuse alors le tableau ENTIER, sans rien dire : les 13 lignes
# disparaissent de la page et personne ne le voit, parce que le texte est toujours là, en gris.
#
# CE QU'ELLE VÉRIFIE (trois conditions, toutes nécessaires au rendu) :
#   1. l'en-tête et le séparateur d'un tableau ont le MÊME nombre de cellules ;
#   2. chaque ligne du corps a ce nombre de cellules ;
#   3. aucun `\|` ne subsiste : mistune ne le déséchappe NI dans un espace de code NI dans la
#      prose (il s'affiche alors littéralement). Pour une barre de valeur absolue dans du code,
#      on écrit `∣` (U+2223), qui rend partout et ne casse pas la lecture.
# Les tableaux DANS une citation (`> | … |`) sont valides et vérifiés aussi.
#
# CE QU'ELLE NE VÉRIFIE PAS : les tableaux « écrasés » sur une se
… [6759 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date && tail -4 work/portes/passe-1311-23h15.log && echo \"---\" && cat work/portes/passe-1311-23h15/registre.txt 2>/dev/null | tail -8", "description": "Check pass progress"}`

  ```
ven 13 nov 2026 23:13:20 EST
=== PASSE COMPLÈTE DES PORTES (84 portes, borne 1800 s) ===
    journaux : work/portes/passe-1311-23h15
---
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport re, pathlib, subprocess\nt = pathlib.Path('docs/pilotage/references-non-regression.md').read_text()\nrows = re.findall(r'^\\| `(porte-[^`]+\\.sh)` \\| (\\d+) s \\| (.*?) \\|$', t, re.M)\nprint('rows:', len(ro … [316 caractères tronqués]`

  ```
rows: 83
missing: ['porte-produit.sh']
extra: []
header: ["| porte | durée | ce qu'elle vérifie, chiffré (passe du 2026-11-03 11:30) |"]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"references-non-regression\\|pilotage\" docs/methode/contexte.md | head -20 && echo \"=== taille ===\" && wc -w docs/pilotage/references-non-regression.md && grep -rn \"references-non-regression\" tools/taille_documents.py | … [48 caractères tronqués]`

  ```
7:> **Règle d'or.** `AGENTS.md` + `docs/pilotage/en-cours.md` + **un** document de tâche. Tout le reste est
14:| **T0 — toujours** | les règles, l'[état](../theorie/glossaire/entrees/etat.md), **un** document de tâche | **≤ 4 000 mots** | `AGENTS.md` · `docs/pilotage/en-cours.md` · `docs/methode/<tâche>.md` |
21:2. Lire [`docs/pilotage/en-cours.md`](../pilotage/en-cours.md) — l'état courant, pas l'historique.
44:| `docs/pilotage/en-cours.md` | 2 000 | **T0** — toujours |
49:| `docs/pilotage/roadmap.md` | 8 500 | **T1** — résumé + un programme |
50:| `docs/pilotage/backlog/index.md` | 1 500 | **T1** — une fiche, pas le dossier |
59:| `docs/pilotage/utilisation.md` | 2 500 | **T1** — les commandes qui marchent |
=== taille ===
2404 docs/pilotage/references-non-regression.md
48:    ("T1", "docs/pilotage/references-non-regression.md", 2500),
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,120p' tools/taille_documents.py", "description": "Read doc size checker"}`

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
… [3928 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport re, pathlib\nt=pathlib.Path('docs/pilotage/references-non-regression.md').read_text()\nrows=re.findall(r'^\\| `(porte-[^`]+\\.sh)` \\| (\\d+) s \\| (.*?) \\|$', t, re.M)\nfor n,d,s in rows:\n    if n in ('por … [176 caractères tronqués]`

  ```
porte-audit-drapeaux.sh 90 '✅ porte audit des drapeaux : occupation, ratio de signes et densité de croissance — chacun'
porte-coupe.sh 100 '✅ le coût du pont va de +0.52 % (coupe 18/24) à +17.09 % (coupe 15/24) — il y a un bon endroit pour '
porte-gain.sh 100 '✅ drapeau VIVANT mais conditionnel : 0 casse (29.0206 → 1297.5437), 24 améliore (27.4439), sans fenê'
porte-indice.sh 100 "❌ l'indice extérieur tombe à 482 jetons de l'aiguille et l'indice TÉMOIN (même invite, question qui "
porte-vision.sh 100 '✅ porte tenue (refus dit · embedding NON comparé · formes · couches isolées NON vérifiées · projecte'
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for p in porte-coupe porte-gain porte-indice porte-vision; do echo \"=== $p ===\"; grep -E \"✅|❌|ÉCHEC|TENUE\" work/portes/passe-0303-11h30/$p.log | tail -1 | cat -A | head -2; grep -E \"✅|❌|ÉCHEC|TENUE\" work/portes/passe-0303-11h30 … [77 caractères tronqués]`

  ```
=== porte-coupe ===
  M-bM-^\M-^E le coM-CM-;t du pont va de +0.52 % (coupe 18/24) M-CM-  +17.09 % (coupe 15/24) M-bM-^@M-^T il y a un bon endroit pour couper$
115
=== porte-gain ===
  M-bM-^\M-^E drapeau VIVANT mais conditionnel : 0 casse (29.0206 M-bM-^FM-^R 1297.5437), 24 amM-CM-)liore (27.4439), sans fenM-CM-*tre il se tait$
123
=== porte-indice ===
  M-bM-^]M-^L l'indice extM-CM-)rieur tombe M-CM-  482 jetons de l'aiguille et l'indice TM-CM-^IMOIN (mM-CM-*me invite, question qui ne la dM-CM-)signe pas) M-CM-  459 : l'M-CM-)cart est nul ou nM-CM-)gatif, donc rien n'est M-CM-)tabli sur ce texte (hasard 370 / tM-CM-)moin 370)$
231
=== porte-vision ===
  M-bM-^\M-^E porte tenue (refus dit M-BM-7 embedding NON comparM-CM-) M-BM-7 formes M-BM-7 couches isolM-CM-)es NON vM-CM-)rifiM-CM-)es M-BM-7 projecteur juste)$
122
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport re, pathlib\nt=pathlib.Path('docs/pilotage/references-non-regression.md').read_text()\nrows=re.findall(r'^\\| `(porte-[^`]+\\.sh)` \\| (\\d+) s \\| (.*?) \\|$', t, re.M)\nfrom collections import Counter\nc=Co … [162 caractères tronqués]`

  ```
[(11, 3), (20, 1), (21, 2), (22, 2), (23, 1), (24, 1), (27, 1), (40, 1), (46, 1), (47, 1), (51, 1), (53, 1), (57, 1), (59, 2), (61, 1), (64, 3), (67, 1), (69, 2), (70, 1), (71, 1), (72, 1), (75, 1), (77, 4), (78, 1), (79, 3), (81, 4), (82, 2), (83, 2), (84, 2), (85, 4), (86, 3), (87, 3), (88, 4), (89, 1), (90, 2), (91, 4), (92, 1), (93, 2), (98, 1), (100, 9), (178, 1)]
max ('porte-bloc-linguistique.sh', '17', "✅ verte (`cascade_pos` : **comparaison** restaurée ; la cascade rend 0,8383 = l'heuristique depuis le [correctif de composition](../../reports/rapport-composition-sans-perte.md))")
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for p in porte-bloc-linguistique porte-produit porte-etat; do echo \"=== $p 07/11 ===\"; grep -E \"✅|❌|ÉCHEC|TENUE\" work/portes-1107-16h48/$p.log | tail -1; done", "description": "Check 07/11 lines for special gates"}`

  ```
=== porte-bloc-linguistique 07/11 ===
✅ porte bloc linguistique verte
=== porte-produit 07/11 ===
✅ porte produit verte
=== porte-etat 07/11 ===
✅ porte état verte : aucun fait commité après le dernier état
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rln \"paragraphes-validations\\|tools/structures\" tools/*.sh tools/*.py 2>/dev/null | head -20 && echo \"=== diff submodule ===\" && git -C tools/structures diff --stat", "description": "Check if dirty submodule affects gates" … [1 caractères tronqués]`

  ```
tools/bloc_linguistique.py
tools/canal_structure.py
=== diff submodule ===
 donnees/paragraphes-validations.jsonl | 11 +++++++++++
 1 file changed, 11 insertions(+)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date && tail -3 work/portes/passe-1311-23h15.log && cat work/portes/passe-1311-23h15/registre.txt 2>/dev/null | tail", "description": "Check pass progress"}`

  ```
ven 13 nov 2026 23:13:57 EST
=== PASSE COMPLÈTE DES PORTES (84 portes, borne 1800 s) ===
    journaux : work/portes/passe-1311-23h15
  porte-adaptateur-sortie ✅                          81 s    ✅ porte tenue (écriture fidèle · invariant · effet · refus)
porte-adaptateur-sortie 0 81
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"paragraphes-validations\" tools/bloc_linguistique.py tools/canal_structure.py", "description": "Locate submodule data use"}`

  ```
(no output)
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/sessions.py --status 2>&1 | head -40", "description": "Check session heartbeats"}`

  ```
sessions · plans de mandat
    0733c5bb-f90b-4f58 · terminé  · 12292 min · N2 (200 000 pas sur le mélange, PPL domaine/littérature/anglais/wikitext2, courbe de longueur), R1.1/R1.2 mesurés depuis N2
      → **surveiller les runs relancés à 09 h 30** — `kd2` (gpu0, chargement du corpus) et `rope2048` (gpu1, en cours) ; puis mesurer et committer ; ensuite la **porte propre (0,29)**.
    0b0a6a0d-05f5-4308 · terminé  · 18159 min · N2.h — corpus propre, porte honnête, généralité, verrou de longueur
      → close — N2.i (3,13 / 12,93 / 33,83) et Pensée v0 (6/6 portes) sont committés.
    0b69f616-5c75-4c34 · terminé  · 20233 min · R0.4, R0.5, R13, R4.1–R4.3, en-cours, roadmap, backlog
      → clôture reprise par la session `22e518ee` — commit, archives, état.
  ⏰ 1e7ef596-93e6-45f1 · actif    · 12799 min · docs/pilotage/` (en-cours, roadmap, chantiers, plan-travail, références), journal/` (hors `sessions/<id>/`), reports/README.md, reports/INDEX.md, tools/sessions.py, tools/ressources.py, tools/index_reports.py, tools/surveille_sessions.py, l'index git.
      → **suivi docs** (N3 intégré, état au 04/11), puis la **passe** après les runs.
    22e518ee-81b8-4081 · terminé  · 19404 min · a
… [2708 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,80p' tools/porte-sessions.sh && echo \"=== sessions.py heartbeat ===\" && grep -n \"heartbeat\\|battre\\|battement\\|périmé\\|perime\" tools/sessions.py | head -30", "description": "Read sessions gate and heartbeat logic"}`

  ```
#!/bin/bash
# porte-sessions.sh — les plans de session sont lisibles et le linter refuse un doublon.
set -u
cd "$(dirname "$0")/.."
python3 tools/sessions.py --autotest || exit 1
python3 tools/sessions.py --check --strict || exit 1
echo "PORTE TENUE : plans lisibles · autotest doublon/champ manquant/pause · check strict"
=== sessions.py heartbeat ===
5:périmètre, fichiers réservés, heartbeat, prochaine action, état. Les autres
8:et les heartbeats périmés (le `--check` seul les signale). Les **fichiers
16:l'état, son heartbeat n'est plus exigé, et la reprise la remet `actif`.
18:`work/ressources.json` : le heartbeat n'est pas exigé ; le registre distingue le
34:CHAMPS = ("session", "rôle", "périmètre", "fichiers réservés", "heartbeat",
63:    for alias, cible in (("role", "rôle"), ("perimetre", "périmètre"),
71:    hb = champs.get("heartbeat", "")
72:    heartbeat = None
77:            heartbeat = datetime.fromisoformat(brut)
79:            heartbeat = datetime.strptime(brut, "%Y-%m-%d %H:%M")
80:        age = (datetime.now() - heartbeat).total_seconds() / 60.0
83:    return {"id": sid, "chemin": chemin, "champs": champs, "perimetre": per,
84:            "fichiers": fic, "heartbeat"
… [1147 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '175,205p' tools/sessions.py && echo \"=== ressources claims ===\" && cat work/ressources.json && echo && grep -n \"claim\" tools/ressources.py | head -20", "description": "Read strict check and claims"}`

  ```
claims = sessions_avec_claim(racine)
    vus: dict[str, str] = {}
    for p in plans:
        manquants = [c for c in CHAMPS if c not in p["champs"]]
        if manquants:
            erreurs.append(f"{p['chemin']} : champ(s) manquant(s) — {', '.join(manquants)}")
        if p["etat"] not in ETATS_CONNUS:
            erreurs.append(f"{p['chemin']} : état inconnu {p['etat']!r}")
        if p["etat"] in A_CONFIRMER:
            (erreurs if strict else avertissements).append(
                f"plan à confirmer : {p['id']} — la session doit le compléter")
        if p["age"] is None:
            erreurs.append(f"{p['chemin']} : heartbeat illisible")
        if p["id"] in vus:
            erreurs.append(f"id dupliqué : {p['id']} ({vus[p['id']]} et {p['chemin']})")
        vus[p["id"]] = str(p["chemin"])
    for i, a in enumerate(actifs):
        if a["age"] is not None and a["age"] > PEREMPTION_MIN:
            if any(a["id"].startswith(c) for c in claims):
                avertissements.append(
                    f"mandat long ({a['age']:.0f} min) : {a['id']} — claim actif, heartbeat non exigé")
            else:
                msg = f"mandat périmé ({a['age']:.0f} min) : {a['id']} —
… [1499 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"add_argument\" tools/sessions.py && echo \"=== plan 1e7 ===\" && head -20 journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/plan.md && echo \"=== plan e181 ===\" && head -20 journal/sessions/e181ce02-cd50-488a-a6be-e84b … [69 caractères tronqués]`

  ```
330:    ap.add_argument("--racine", default=str(RACINE))
331:    ap.add_argument("--status", action="store_true")
332:    ap.add_argument("--check", action="store_true")
333:    ap.add_argument("--strict", action="store_true")
334:    ap.add_argument("--modele", action="store_true")
335:    ap.add_argument("--autotest", action="store_true")
336:    ap.add_argument("--depuis-en-cours", action="store_true",
=== plan 1e7 ===
# Plan de session — le hub de reprise du 04/11

> **Mandat vivant.** Ouvert le 2026-11-04 08 h 50 HNE après le reboot du 03/11 19 h 33.
> Ce plan est le contrat de la reprise : il dit ce que la session analyse, ce qu'elle commite,
> et ce qu'elle laisse aux sessions interrompues.

- **Session** : `1e7ef596-93e6-45f1-b7f2-2940044b6e3a`
- **Rôle** : **Hub de reprise** — analyse des quatre sessions interrompues (N2, S, Pensée/L, hub),
  tâches courtes, état, journal, intégration, compteurs.
- **Périmètre** : `docs/pilotage/` (en-cours, roadmap, chantiers, plan-travail, références),
  `journal/` (hors `sessions/<id>/`), `reports/README.md`, `reports/INDEX.md`, `tools/sessions.py`,
  `tools/ressources.py`, `tools/index_reports.py`, `tools/surveille_sessions.py`, l'inde
… [2086 caractères tronqués]
  ```

- **write** `{"file_path": "/tmp/analyse_passe.py", "content": "#!/usr/bin/env python3\n\"\"\"Analyse une passe de portes : registre + journaux -> tableau markdown, JSON, récapitulatif.\"\"\"\nimport json\nimport pathlib\nimport re\nimport sys\nfrom datetime import datetime\n\nd = pathlib.Path(sys.argv[1])\nreg  … [2263 caractères tronqués]`

  ```
<path>/tmp/analyse_passe.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls reports/ | head -20 && echo \"=== index_reports ===\" && head -40 tools/index_reports.py && echo \"=== reports README head ===\" && head -40 reports/README.md", "description": "Understand reports indexing"}`

  ```
07
07-mesures-couche-commune.md
a26-bilan.json
a26-lot-disque.json
a80-audit-final.json
a80-indice-qualifie.json
a80-melange-qualifie.json
a80-pannes-ppl.json
a80-porte-adaptateur.json
a80-porte-budget.json
a80-porte-bus.json
a80-porte-bus-socket.json
a80-porte-c4-retard.json
a80-porte-consolidation.json
a80-porte-cycle-c2.json
a80-porte-delais.json
a80-porte-flux.json
a80-porte-fusion.json
a80-porte-gain.json
a80-porte-pont.json
=== index_reports ===
#!/usr/bin/env python3
"""index_reports.py — génère reports/INDEX.md à partir des en-têtes de fiches.

L'index est **exhaustif** et **déterministe** : une ligne par fiche, triée par nom,
avec son titre (premier `# `). Les fichiers d'infrastructure (`README.md`, `INDEX.md`
et `historique-*`) sont exclus du tableau ; les compteurs de `docs/pilotage/en-cours.md`
comptent, eux, tous les `.md` de `reports/`.

Usage :
    python3 tools/index_reports.py              # réécrit reports/INDEX.md
    python3 tools/index_reports.py --verifier   # ne réécrit rien, sort 1 si périmé
    python3 tools/index_reports.py --aide       # affiche l'aide (ne touche à rien)
"""
from __future__ import annotations

import argparse
import pathlib

RACINE = path
… [4130 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat tools/porte-document.sh | head -60 && echo \"=== INDEX tracked? ===\" && git ls-files reports/INDEX.md && wc -w reports/README.md", "description": "Check document gate and INDEX"}`

  ```
#!/bin/bash
# porte-document.sh — R0.1 : le document est un graphe, et le graphe se vérifie.
#
# POURQUOI CETTE PORTE EXISTE. Une découpe de document qui « a l'air bonne » n'est pas une
# découpe : sans partition exacte, un offset faux ne se voit pas ; sans extraction
# indépendante, un extracteur qui invente des mots ne se voit pas non plus. Cette porte
# exige donc les trois choses ensemble — partition, fidélité, rejeu — plus trois contrôles
# négatifs qui doivent ÉCHOUER (texte plat, deux colonnes, notes hors corps).
set -u
cd "$(dirname "$0")/.."
echo "=== PORTE R0.1 — LE GRAPHE DE DOCUMENT ==="
python3 tools/graphe_document.py --porte
CODE=$?
[ "$CODE" = 0 ] && echo "✅ porte document verte" || echo "❌ porte document ROUGE (code $CODE)"
exit "$CODE"
=== INDEX tracked? ===
reports/INDEX.md
2661 reports/README.md
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/methode/rangement.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/methode/rangement.md</path>
<type>file</type>
<content>
1: # Le rangement, et la revue de documentation
2: 
3: > Document de tâche, chargé depuis [`AGENTS.md`](../../AGENTS.md). La règle la plus souvent violée du dépôt : à lire
4: > **avant de classer un fichier** ou de clore un sous-chantier.
5: 
6: ## Les quatre dossiers (règle stricte)
7: 
8: | dossier | ce qu'il contient | ce qu'il ne contient **jamais** |
9: |---|---|---|
10: | **`docs/`** | quatre familles : **méthode**, **pilotage**, **théorie**, **implantation** — ce qui reste vrai quand les chiffres changent | des **résultats** de mesure, des tableaux de chiffres, des comptes rendus de round |
11: | **`reports/`** | les **résultats mesurés** : fiches, séries de mesures, tableaux, erratums, récits de round, JSON de résultats | la documentation de référence |
12: | **`journal/`** | le **récit daté** : ce qui a été fait, quand, et ce qu'on en a appris | les chiffres seuls (ils vont dans `reports/`) |
13: | **`data/`** | les corpus et leur généalogie (`data/udhr/`, `data/corpus_*.txt`, `data/eurlex/`) | du code |
14: 
15: Dans `docs/`, les quatre familles sont **séparé
… [4461 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date +%H:%M:%S && tail -5 work/portes/passe-1311-23h15.log && echo \"--- registre ---\" && cat work/portes/passe-1311-23h15/registre.txt 2>/dev/null", "description": "Check pass progress"}`

  ```
23:14:42
=== PASSE COMPLÈTE DES PORTES (84 portes, borne 1800 s) ===
    journaux : work/portes/passe-1311-23h15
  porte-adaptateur-sortie ✅                          81 s    ✅ porte tenue (écriture fidèle · invariant · effet · refus)
--- registre ---
porte-adaptateur-sortie 0 81
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"md: $(ls reports/*.md | wc -l)\" && echo \"json: $(ls reports/*.json | wc -l)\" && echo \"portes: $(ls tools/porte-*.sh | wc -l)\" && echo \"docs: $(find docs -name '*.md' -not -path 'docs/archive/*' -not -name README.md | wc  … [122 caractères tronqués]`

  ```
md: 718
json: 812
portes: 84
docs: 458
104:| fichiers / JSON de résultats | **718** / **812** | `reports/*.md` / `reports/*.json` |
105:| documents de `docs/` | **123** (hors archive et README) | `docs/**/*.md` |
  ```

- **bash** `{"command": "cd /tmp && rm -rf ctl-passe && mkdir ctl-passe && printf 'faux-vert 0 1\\nfaux-rouge 1 2\\nfaux-borne 124 3\\n' > ctl-passe/registre.txt && echo \"ROUGES DETECTEES:\" && awk '$2 != 0' ctl-passe/registre.txt && echo \"TOTAL: $(awk 'END{print NR}' ctl-passe/registre.txt) lignes, $(awk '$2 … [101 caractères tronqués]`

  ```
ROUGES DETECTEES:
faux-rouge 1 2
faux-borne 124 3
TOTAL: 3 lignes, 1 vertes
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date +%H:%M:%S && tail -4 work/portes/passe-1311-23h15.log && echo \"n=$(wc -l < work/portes/passe-1311-23h15/registre.txt 2>/dev/null || echo 0)\"", "description": "Check pass progress"}`

  ```
23:15:01
=== PASSE COMPLÈTE DES PORTES (84 portes, borne 1800 s) ===
    journaux : work/portes/passe-1311-23h15
  porte-adaptateur-sortie ✅                          81 s    ✅ porte tenue (écriture fidèle · invariant · effet · refus)
n=1
  ```

- **job_output** `{"job_id": "bash-15", "wait": true, "timeout_ms": 600000}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date +%H:%M:%S && tail -12 work/portes/passe-1311-23h15.log && echo \"n=$(wc -l < work/portes/passe-1311-23h15/registre.txt 2>/dev/null || echo 0)\" && echo \"=== reds ===\" && awk '$2 != 0' work/portes/passe-1311-23h15/registre.txt  … [62 caractères tronqués]`

  ```
23:25:06
  porte-b1110-hybride    ✅                           0 s  PORTE TENUE : 4/4 routées · 4/4 lues · E4 = requête de case
  porte-balayage         ✅                           0 s  ✅ porte balayage verte
  porte-bloc-code        ✅                          12 s  ✅ porte bloc code verte
  porte-bloc-linguistique ✅                          15 s  ✅ porte bloc linguistique verte
  porte-bloc-maths       ✅                           1 s  ✅ porte bloc maths verte
  porte-bloc-tableaux    ✅                           1 s  ✅ porte bloc tableaux verte
  porte-budget           ✅                          47 s    ✅ paires depassees : nommees (total, budget, pas, plafond), code 9, AUCUNE perplexite
  porte-bus              ✅                          80 s    ✅ le canal diffusé par fichier change la région du milieu
  porte-bus-socket       ✅                          96 s    ✅ le bus du pilote agit (113.0068 -> 148.9144)
  porte-c4-retard        ✅                          31 s  PORTE TENUE : un état n'est valide qu'à sa position (×633 pour un pas), et l'asynchronisme ne
  porte-cerveau          ✅                          10 s    ✅ porte tenue (quatre facultés composent, chacune reste active, le 
… [192 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-15", "timeout_ms": 600000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date +%H:%M:%S && tail -8 work/portes/passe-1311-23h15.log && echo \"n=$(grep -c . work/portes/passe-1311-23h15/registre.txt)\" && echo \"=== reds ===\" && awk '$2 != 0' work/portes/passe-1311-23h15/registre.txt", "description": "Che … [18 caractères tronqués]`

  ```
23:35:11
  porte-delais           ✅                          21 s    ✅ le temps, lui, augmente : 7.00 s → 10.42 s (+3.4 s ≈ 50 ms × 64 pas)
  porte-diff-couche      ✅                          19 s    ✅ le contrat est tenu : la divergence commence à la couche 1, premier jeton tracé
  porte-document         ✅                           6 s  ✅ porte document verte
  porte-echange-experts  ✅                          54 s    PORTE TENUE
  porte-episodique       ✅                         174 s    ✅ la porte C6 est franchie — et elle dit ses conditions : 300 états consécutifs d'un
  porte-etat             ✅                           0 s  ✅ porte état verte : aucun fait commité après le dernier état
  porte-flux             ✅                          25 s    mode 4 — lot en listes           4.45e-3  ✅  (réf 60.8135 / deux nœuds 60.5427)
  porte-fusion           ✅                           8 s    ✅ v1 refusée (code 2), trace seule refusée (code 2)
n=25
=== reds ===
  ```

- **job_output** `{"job_id": "bash-15", "timeout_ms": 600000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date +%H:%M:%S && tail -6 work/portes/passe-1311-23h15.log && echo \"n=$(grep -c . work/portes/passe-1311-23h15/registre.txt)\" && echo \"=== reds ===\" && awk '$2 != 0' work/portes/passe-1311-23h15/registre.txt", "description": "Che … [18 caractères tronqués]`

  ```
23:45:16
  porte-echange-experts  ✅                          54 s    PORTE TENUE
  porte-episodique       ✅                         174 s    ✅ la porte C6 est franchie — et elle dit ses conditions : 300 états consécutifs d'un
  porte-etat             ✅                           0 s  ✅ porte état verte : aucun fait commité après le dernier état
  porte-flux             ✅                          25 s    mode 4 — lot en listes           4.45e-3  ✅  (réf 60.8135 / deux nœuds 60.5427)
  porte-fusion           ✅                           8 s    ✅ v1 refusée (code 2), trace seule refusée (code 2)
  porte-gain             ✅                         219 s    ✅ drapeau VIVANT mais conditionnel : 0 casse (29.0206 → 1297.5437), 24 améliore (27.4439), san
n=26
=== reds ===
  ```

- **job_output** `{"job_id": "bash-15", "timeout_ms": 600000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date +%H:%M:%S && tail -5 work/portes/passe-1311-23h15.log && echo \"n=$(grep -c . work/portes/passe-1311-23h15/registre.txt)\" && echo \"=== reds ===\" && awk '$2 != 0' work/portes/passe-1311-23h15/registre.txt", "description": "Che … [18 caractères tronqués]`

  ```
23:55:20
  porte-flux             ✅                          25 s    mode 4 — lot en listes           4.45e-3  ✅  (réf 60.8135 / deux nœuds 60.5427)
  porte-fusion           ✅                           8 s    ✅ v1 refusée (code 2), trace seule refusée (code 2)
  porte-gain             ✅                         219 s    ✅ drapeau VIVANT mais conditionnel : 0 casse (29.0206 → 1297.5437), 24 améliore (27.4439), san
  porte-greffe           ✅                         657 s    ✅ la porte est franchie. Ce qu'elle établit : l'injection d'état est BRANCHÉE
  porte-harnais-invariants ✅                         117 s  ✅ porte harnais : installer une reparamétrisation laisse le modèle intact, et l'élagage
n=28
=== reds ===
  ```

- **job_output** `{"job_id": "bash-15", "timeout_ms": 600000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date +%H:%M:%S && tail -4 work/portes/passe-1311-23h15.log && echo \"n=$(grep -c . work/portes/passe-1311-23h15/registre.txt)\" && echo \"=== reds ===\" && awk '$2 != 0' work/portes/passe-1311-23h15/registre.txt", "description": "Che … [18 caractères tronqués]`

  ```
00:05:24
  porte-greffe           ✅                         657 s    ✅ la porte est franchie. Ce qu'elle établit : l'injection d'état est BRANCHÉE
  porte-harnais-invariants ✅                         117 s  ✅ porte harnais : installer une reparamétrisation laisse le modèle intact, et l'élagage
  porte-homeostasie      ✅                         529 s    ✅ porte tenue (×0 exact · activité monotone · dominance reproduite)
  porte-horloge          ✅                          26 s    ✅ borne atteinte : arrêt EXPLICITE (code 5) et AUCUNE perplexité rendue
n=30
=== reds ===
  ```

- **job_output** `{"job_id": "bash-15", "timeout_ms": 600000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date +%H:%M:%S && tail -4 work/portes/passe-1311-23h15.log && echo \"n=$(grep -c . work/portes/passe-1311-23h15/registre.txt)\" && echo \"=== reds ===\" && awk '$2 != 0' work/portes/passe-1311-23h15/registre.txt", "description": "Che … [18 caractères tronqués]`

  ```
00:15:30
  porte-homeostasie      ✅                         529 s    ✅ porte tenue (×0 exact · activité monotone · dominance reproduite)
  porte-horloge          ✅                          26 s    ✅ borne atteinte : arrêt EXPLICITE (code 5) et AUCUNE perplexité rendue
  porte-indice           ❌ code 1                  875 s    ❌ l'indice extérieur tombe à 482 jetons de l'aiguille et l'indice TÉMOIN (même invite, questio
  porte-jeux             ✅                         111 s    ✅ la porte des jeux tient : 100 % au niveau 4, 33/33 paires invariantes, 0 collision,
n=32
=== reds ===
porte-indice 1 875
  ```

- **job_output** `{"job_id": "bash-15", "timeout_ms": 600000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date +%H:%M:%S && tail -6 work/portes/passe-1311-23h15.log && echo \"n=$(grep -c . work/portes/passe-1311-23h15/registre.txt)\" && echo \"=== reds ===\" && awk '$2 != 0' work/portes/passe-1311-23h15/registre.txt", "description": "Che … [18 caractères tronqués]`

  ```
00:25:35
  porte-n3-service       ✅                           6 s  PORTE TENUE : service natif vivant · /sante exact · génération déterministe · 404
  porte-n3-seuil         ✅                           5 s  PORTE TENUE : décision à seuil comptée · 0/1 aux extrêmes · mixte à 0,01 · déterministe
  porte-n3-sparsite-compte ✅                           5 s  PORTE TENUE : compteurs réels · top_k agit sur les experts · kwta agit sur les canaux · A déterm
  porte-n3-sparsite      ✅                           5 s  PORTE TENUE : kwta et top_k agissent séparément · A déterministe
  porte-occupation-elagage ✅                          61 s  ✅ porte occupation × élagage : la cible annoncée est VÉRIFIÉE dans le fichier exporté
  porte-occupation-moteur ✅                          56 s  ✅ porte occupation du moteur : la ligne « occupation des poids » est annoncée, elle COLLE à
n=60
=== reds ===
porte-indice 1 875
porte-melange 1 111
  ```

- **job_output** `{"job_id": "bash-15", "timeout_ms": 600000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date +%H:%M:%S && tail -6 work/portes/passe-1311-23h15.log && echo \"n=$(grep -c . work/portes/passe-1311-23h15/registre.txt)\" && echo \"=== reds ===\" && awk '$2 != 0' work/portes/passe-1311-23h15/registre.txt", "description": "Che … [18 caractères tronqués]`

  ```
00:35:40
  porte-occupation-elagage ✅                          61 s  ✅ porte occupation × élagage : la cible annoncée est VÉRIFIÉE dans le fichier exporté
  porte-occupation-moteur ✅                          56 s  ✅ porte occupation du moteur : la ligne « occupation des poids » est annoncée, elle COLLE à
  porte-ocr-scans        ✅                         452 s  ✅ porte OCR-scans verte : familles, colonnes et tableaux tiennent leurs planchers
  porte-ocr              ✅                          49 s  ✅ porte OCR verte : 10 pages lues, WER sous le seuil, parité tenue et contrôles en échec
  porte-pannes           ✅                          46 s    ✅ pair absent : échec annoncé en 2 s (code 7), aucune perplexité
  porte-peripherie       ✅                          16 s  PORTE TENUE : l'entrée est injectée, la sortie est écrite, le délai est exact, les refus sont
n=64
=== reds ===
porte-indice 1 875
porte-melange 1 111
  ```

- **job_output** `{"job_id": "bash-15", "timeout_ms": 600000, "wait": true}`
