# Session DSH — relecture

- identifiant : `session-631f4ba2-5c36-4fdc-b751-fa0a2cce9d21`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-14 04:58:17
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche J11.4 : documenter le schéma v2 dans `docs/produit/README.md` (les champs de `meta.partition`/`meta.alternative`, la rétro-compatibilité v1) et vérifier que `tools/verifier_schema_produit.py` valide les deux versions ; fiche `reports/rapport-schema-v2-doc.md` + JSON, commit.

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

- **bash** `{"command": "pwd && ls -la && git status --short | head -50 && git log --oneline -5", "description": "Inspect repository root and git state"}`

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
drwxr-xr-x. 1 stephane stephane   180 14 nov 04:58 .git
-rw-r--r--. 1 stephane stephane   619 31 oct 17:33 .gitignore
-rw-r--r--. 1 stephane stephane   225  1 nov 10:50 .gitmodules
drwxr-xr-x. 1 stephane stephane   972 14 nov 00:51 journal
drwxr-xr-x. 1 stephane stephane   100  3 nov 09:12 models
drwxr-xr-x. 1 stephane stephane   114 25 sep 15:24 __pycache__
drwxr-xr-x. 1 stephane stephane    64  6 nov 09:52 .pytest_cache
-rw-r--r--. 1 stephane stephane  4992 25 sep 10:54 Qtrinet-bootstrap.md
-rw-r--r--. 1 stephane stephane 21293  6 nov 22:32 README.md
drwxr-xr-x. 1 stephane stephane 75774 14 nov 04:49 reports
-rw-r--r--. 1 stephane stephane 13100 28 oct 14:59 REPRISE.md
-rw---
… [2033 caractères tronqués]
  ```

- **bash** `{"command": "ls -la docs/produit/ 2>/dev/null; ls -la tools/verifier_schema_produit.py 2>/dev/null; ls reports/ | head -40", "description": "List product docs and verifier script"}`

  ```
total 56
drwxr-xr-x. 1 stephane stephane    40 14 nov 04:36 .
drwxr-xr-x. 1 stephane stephane   138  6 nov 10:08 ..
-rw-r--r--. 1 stephane stephane 22928 14 nov 04:20 exemples.md
-rw-r--r--. 1 stephane stephane 30997 14 nov 04:36 README.md
-rw-r--r--. 1 stephane stephane 7222  7 nov 14:14 tools/verifier_schema_produit.py
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
a80-porte-profondeur.json
a80-porte-reflexe.json
a80-porte-reparti.json
a80-portes-ppl.json
a80-porte-topologie.json
a80-porte-trace.json
a83a-coupe.json
a83a-flux.json
a83a-pont.json
a83b-decision.json
a83b-lot.json
a83b-regimes.json
a83c-ctx.json
a83c-lot.json
a83-defaut.json
a83d-lot-threads.json
aiguille-30b.md
aiguille-gpt-oss.md
alignement-3b.json
alignement-7b.json
[stderr]
ls: write error: Broken pipe
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_schema_produit.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_schema_produit.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """verifier_schema_produit.py — valide une annotation `drave.annotation` contre le schéma de sa version.
3: 
4: Deux schémas sont publiés (Draft 2020-12) :
5: 
6: - `tools/schemas/drave-annotation-v1.json` — le contrat d'origine (version 1) ;
7: - `tools/schemas/drave-annotation-v2.json` — le contrat courant (version 2) : il ajoute
8:   `meta.partition` et `meta.alternative`, les deux champs qui documentent les syntagmes qui se
9:   chevauchent.
10: 
11: Le vérificateur lit `version` dans l'annotation et choisit le schéma correspondant : une
12: annotation v1 reste donc **lue** et validée par le schéma v1. Il compile les schémas une fois,
13: puis valide les annotations de cas choisis : français, anglais, refus (texte vide), entrée non
14: textuelle, texte très long, plus une annotation v1 de rétro-compatibilité. Il ne dépend que de
15: `fastjsonschema` (sinon il se rabat sur une validation minimale des champs obligatoires et de la
16: version). Un **contrôle négatif** vérifie que le schéma v2 refuse bien une annotation v1.
17: 
18: 
… [6831 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"J11.4\\|schema v2\\|schéma v2\\|verifier_schema_produit\" --include=\"*.md\" --include=\"*.json\" --include=\"*.py\" docs tools reports work | head -60", "description": "Search references to J11.4 and schema v2"}`

  ```
docs/pilotage/semaine-autonome.md:94:| | après-midi | le **schéma v2** (`meta.alternative`, `meta.partition`) et la **restitution v0** | schéma validé, miroir mesuré |
docs/pilotage/semaine-autonome.md:142:- le **produit** : 2 spans tranchés (ou déclarés), le schéma v2, la restitution v0, la porte verte ;
docs/pilotage/semaine-autonome.md:161:| J1.3 schéma v2 | ✅ fait | `meta.partition`/`meta.alternative`, 26 cas | `9a259953` |
docs/pilotage/semaine-autonome.md:195:| **J1** | après-midi : schéma v2 + restitution v0 | ✅ fait | **26 cas / 0 échec**, **1 836 annotations / 0 échec** ; **46/46** surfaces, miroir **0,1087** | `9a259953`, `8eb0cc49` | invariants sémantiques, v0.1 ponctuation, gold de restitution |
docs/pilotage/semaine-autonome.md:212:des GV (F1 **0,7902**), `s065` réglé (**238/238** labels, 238/239 cibles), le schéma v2 (26 cas /
docs/pilotage/semaine-autonome.md:242:**Les décisions.** **D1–D20** : le produit (relative zéro, convention GV, schéma v2, restitution,
docs/pilotage/semaine-autonome.md:251:**La suite.** **J11.1–J11.4** (produit : exemples, par-langue, robustesse, schéma documenté) ;
docs/pilotage/roadmap.md:73:(`evaluer --par-langue`), **J11.3** (50 textes lib
… [8001 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md</path>
<type>file</type>
<content>
1: # Le premier produit — analyser un texte avec Drave
2: 
3: > **Ce que ce document est.** La notice d'usage du **premier produit** de Drave : le bloc
4: > linguistique, utilisable **aujourd'hui**, sur un CPU, sans modèle et sans réseau. Il dit à qui
5: > il s'adresse, ce qu'il fait, comment l'exécuter, ce qu'il ne fait pas, ce qu'il coûte et ce
6: > qu'il garantit.
7: >
8: > **Vérifié le 2026-11-14** sur la branche `s/v7`. Le point d'entrée `tools/drave.py` est
9: > **livré** (version **0.1.0**) : `analyser`, `evaluer`, `rejouer`, `restituer` et `--version`
10: > existent, et la
11: > porte produit est verte. Le format est **version 2** (`schema: "drave.annotation"`,
12: > `version: 2`) : le schéma v2 ajoute `meta.partition` et `meta.alternative`, et la **version 1
13: > reste lue** ([`tools/schemas/`](../../tools/schemas/)). Les sorties du § 3.1, du § 3.4 et du
14: > § 3.5 ont été relancées le 07/11 pour le format v2 ; les mesures chiffrées du § 2 datent du
15: > **06/11**, et l'`evaluer` du § 3.3 a été relancé le **14/11** (gold vivant 612, `--par-langue
16: > fr/en`)
… [31657 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,240p' tools/schemas/drave-annotation-v2.json", "description": "Read v2 schema part 1"}`

  ```
{
 "$schema": "https://json-schema.org/draft/2020-12/schema",
 "$id": "https://drave.local/schema/annotation-v2.json",
 "title": "drave.annotation v2",
 "description": "L'annotation du bloc linguistique heuristique, version 2 : identique à la v1 et documente, dans `meta`, la partition des syntagmes qui se chevauchent (`meta.partition`) et les segments alternatifs du groupe (`meta.alternative`). Les deux champs sont additifs et optionnels : v1 reste lue.",
 "type": "object",
 "required": [
  "schema",
  "version",
  "texte",
  "langue",
  "script",
  "refus",
  "etiquettes",
  "unites_semantiques"
 ],
 "properties": {
  "schema": {
   "const": "drave.annotation"
  },
  "version": {
   "const": 2
  },
  "texte": {
   "type": "string"
  },
  "langue": {
   "type": "string",
   "pattern": "^[a-z]{2,3}$|^und$"
  },
  "script": {
   "type": "string"
  },
  "source": {
   "type": "string"
  },
  "refus": {
   "type": "string",
   "enum": [
    "",
    "vide",
    "non_texte",
    "trop_long",
    "neuronal"
   ]
  },
  "etiquettes": {
   "type": "array",
   "items": {
    "type": "object",
    "required": [
     "niveau",
     "type",
     "valeur",
     "debut",
     "fin",
     "source"
… [3413 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,220p' tools/schemas/drave-annotation-v1.json", "description": "Read v1 schema"}`

  ```
{
 "$schema": "https://json-schema.org/draft/2020-12/schema",
 "$id": "https://drave.local/schema/annotation-v1.json",
 "title": "drave.annotation v1",
 "description": "L'annotation du bloc linguistique heuristique : un texte, ses étiquettes par niveau, ses unités sémantiques et son refus éventuel.",
 "type": "object",
 "required": [
  "schema",
  "version",
  "texte",
  "langue",
  "script",
  "refus",
  "etiquettes",
  "unites_semantiques"
 ],
 "properties": {
  "schema": {
   "const": "drave.annotation"
  },
  "version": {
   "const": 1
  },
  "texte": {
   "type": "string"
  },
  "langue": {
   "type": "string",
   "pattern": "^[a-z]{2,3}$|^und$"
  },
  "script": {
   "type": "string"
  },
  "source": {
   "type": "string"
  },
  "refus": {
   "type": "string",
   "enum": [
    "",
    "vide",
    "non_texte",
    "trop_long",
    "neuronal"
   ]
  },
  "etiquettes": {
   "type": "array",
   "items": {
    "type": "object",
    "required": [
     "niveau",
     "type",
     "valeur",
     "debut",
     "fin",
     "source",
     "confiance"
    ],
    "properties": {
     "niveau": {
      "type": "string"
     },
     "type": {
      "type": "string"
     },
     "valeur": {
 
… [1056 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-schema-v2.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-schema-v2.md</path>
<type>file</type>
<content>
1: # B13 — le schéma v2 : `meta.partition` et `meta.alternative` typés, version 2, v1 toujours lue
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée) · **Tâche** : J1.3 · **Date** : 2026-11-07 ·
4: > **Verdict** : ✅
5: > **Ce qui change pour un client** : l'annotation porte `schema: "drave.annotation"` et
6: > `version: 2`. Le schéma v2 publie les deux champs qui documentent les syntagmes qui se
7: > chevauchent : `meta.partition` (`{groupe, rang, membres, vue}`) et `meta.alternative` (la liste
8: > des autres segments du groupe, avec `relation`, `union`, `rang`, `retire`, `role`,
9: > `attachement`). Les champs sont **additifs** : un client qui ne lit pas `meta` continue de lire
10: > l'annotation. **La version 1 reste lue** : `verifier_schema_produit.py` choisit le schéma
11: > d'après `version`, et un **contrôle négatif** vérifie que le schéma v2 refuse bien une
12: > annotation v1.
13: >
14: > **Dispositif** : [`drave-annotation-v2.json`](../tools/schemas/drave-annotation-v2.json),
15: > [`drave-annotation-v1.json`](../tools/schemas/drave-annotation-v1.j
… [5497 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,220p' tools/tests/test_schema_produit.py", "description": "Read schema tests"}`

  ```
#!/usr/bin/env python3
"""test_schema_produit.py — le **contrat** du produit : schéma v2, v1 lue, refus, entrées hostiles.

Ce que le test fige (et qu'un client peut supposer) :
- 8 champs **obligatoires** à la racine : `schema`, `version`, `texte`, `langue`, `script`,
  `refus`, `etiquettes`, `unites_semantiques` ;
- `schema == "drave.annotation"` et `version == 2` ;
- `meta.partition` et `meta.alternative` sont déclarés dans le schéma v2 ;
- une annotation **v1 reste lue** par le vérificateur (schéma v1), et le schéma v2 la refuse ;
- un refus est une **réponse** : JSON valide avec `refus`, code de sortie 3 ;
- un surrogate isolé et une entrée non textuelle ne font pas planter.
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import unittest

RACINE = pathlib.Path(__file__).resolve().parents[2]
SCHEMA_V1 = RACINE / "tools" / "schemas" / "drave-annotation-v1.json"
SCHEMA_V2 = RACINE / "tools" / "schemas" / "drave-annotation-v2.json"
VERIFICATEUR = RACINE / "tools" / "verifier_schema_produit.py"
OBLIGATOIRES = ("schema", "version", "texte", "langue", "script", "refus",
                "etiquettes", "unites_semantiques")


def _cli(*arg
… [3967 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '330,390p' tools/chantier/plan.json; echo ---; sed -n '1,80p' reports/rapport-robustesse-semaine.md; echo ---; ls reports/ | grep -i robustesse", "description": "Read plan J11.4 and recent J11.3 report"}`

  ```
"titre": "Le produit — la mesure par langue",
   "mandat": "Tâche J11.2 : ajouter `evaluer --par-langue` (le détail fr/en) et le documenter dans `docs/produit/README.md` ; test dans `tools/tests/test_produit.py` ; fiche `reports/rapport-evaluer-langue.md` + JSON, commit.",
   "budget_min": 90,
   "acceptation": [
    {
     "commande": "python3 tools/drave.py evaluer --par-langue >/dev/null 2>&1; echo PL-$?",
     "attendu": "PL-0"
    },
    {
     "commande": "python3 tools/tests/test_produit.py 2>&1 | tail -1",
     "attendu": "OK"
    }
   ]
  },
  {
   "id": "J11.3",
   "jour": 11,
   "titre": "Le produit — la robustesse des 50 textes",
   "mandat": "Tâche J11.3 : re-mesurer les 50 textes libres avec le code de la semaine (F1 0,7902, le schéma v2, la restitution) : plantages, chevauchements (les deux vues), les 8 champs, le temps. Fiche `reports/rapport-robustesse-semaine.md` + JSON, comparaison avec l'audit A26.",
   "budget_min": 90,
   "acceptation": [
    {
     "commande": "test -f reports/rapport-robustesse-semaine.md && echo FICHE-OK",
     "attendu": "FICHE-OK"
    }
   ]
  },
  {
   "id": "J11.4",
   "jour": 11,
   "titre": "Le contrat — le schéma v2 documenté",
   "m
… [6389 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,140p' reports/rapport-schema-v1.md; echo ---; cat reports/pensee-schema-v2.json 2>/dev/null | head -80", "description": "Read schema v1 report and JSON sidecar"}`

  ```
# B13 — le contrat v1 : `schema`/`version`, refus en JSON (code 3), entrées hostiles tolérées

> **Instantané historique** — les chiffres publiés ici sont ceux du commit de la fiche ; ils ne
> décrivent pas l'état courant. L'état courant du bloc est dans
> [`en-cours`](../docs/pilotage/en-cours.md) et [`la roadmap`](../docs/pilotage/roadmap.md).

> **Ligne de roadmap** : **B13** (produit) · **Date** : 2026-11-06 · **Verdict** : ✅
> **Ce qui change pour un client** : le JSON porte désormais **`schema`** (`"drave.annotation"`)
> et **`version`** (`1`) ; un **refus** est une **réponse** (JSON avec `refus`, code de sortie
> **3**) et non plus un stdout vide ; un **surrogate isolé** et une **entrée non textuelle** ne
> font plus planter la CLI ; `--json` est stable (clés triées, sans durée).
> **Le schéma est publié** : [`tools/schemas/drave-annotation-v1.json`](../tools/schemas/drave-annotation-v1.json)
> (Draft 2020-12) et **validé** par `tools/verifier_schema_produit.py` (5 cas : fr, en, vide,
> ponctuation, long) avec `fastjsonschema`.
> **Porte produit** : **10 contrôles** (dont le **validateur de schéma**), **verte** ;
> **183/183** portes d'autotest.
>
> **Dispositif** : [`bloc_l
… [4503 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"J11.4\\|schema-v2-doc\" docs/pilotage/en-cours.md docs/pilotage/roadmap.md reports/INDEX.md tools/chantier/plan.json | head -30; echo ---; sed -n '1,50p' reports/INDEX.md", "description": "Locate J11.4 state and INDEX conventions"}`

  ```
docs/pilotage/en-cours.md:117:| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, gold 432, r035 + convention GV (0,7902), s065 (238/239), g017 rejeté, schéma v2, restitution v1 (canonique 46/46, strict 0,1087), J11.1–J11.3 (produit)** | **J11.4** (schéma v2 documenté) ; **trancher `g017`** ; puis T132/T133, gold 200+ ; **B10.3 bloquée** |
docs/pilotage/en-cours.md:127:**N2** — porte (0,2856/0,3566) ; **Pensée** — `g017`, T132/T133, gold 200+ ; **J3.2** — V14 des 21 langues ; **J7.1** — réplication neuronale ; **S** — 11 verdicts + pointeur ; **R0.7** — split réel ; **A** — A6.2, A8.3b2 ; **J14.1** — passe + tag ; **J11.4** — schéma v2 documenté.
docs/pilotage/roadmap.md:73:(`evaluer --par-langue`), **J11.3** (50 textes libres), **J11.4** (schéma v2 documenté).
docs/pilotage/roadmap.md:83:JSON. La suite produit est **J11.3** (50 textes libres), **J11.4** (schéma v2 documenté).
docs/pilotage/roadmap.md:94:produit est **J11.4** (schéma v2 documenté).
tools/chantier/plan.json:358:   "id": "J11.4",
tools/chantier/plan.json:361:   "mandat": "Tâche J11.4 : documenter le schéma v2 dans `docs/produit/README.md` (les champs de `meta.partition`/`met
… [6040 caractères tronqués]
  ```

- **bash** `{"command": "grep -rln \"J11.3\\|J11.1\\|J11.2\" journal | head; echo ---; ls journal | tail -10; echo ---; grep -rn \"J11\" journal | head -30", "description": "Inspect journal entries for J11 tasks"}`

  ```
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
journal/sessions/session-048748b0-e27f-4f44-8706-b882cae40ff4/digest.md
journal/sessions/session-e9ee2692-96f9-42d2-886c-c5abfb51ce07/digest.md
journal/sessions/session-ce875934-0cf6-4434-a91d-cbca647b11b3/digest.md
journal/sessions/session-b0a87524-43a4-4935-a248-72c1d42c8471/digest.md
journal/sessions/session-b0a87524-43a4-4935-a248-72c1d42c8471/rapport.md
journal/sessions/session-9d3b2074-c5f0-4f11-be10-31d317bac657/digest.md
journal/sessions/session-9d3b2074-c5f0-4f11-be10-31d317bac657/rapport.md
journal/sessions/session-6b997dd9-9a2e-4d72-b31a-5a6d40609d56/digest.md
journal/sessions/session-6b997dd9-9a2e-4d72-b31a-5a6d40609d56/rapport.md
---
2026-11-03
2026-11-04
2026-11-05
2026-11-06
2026-11-07
2026-11-13
2026-11-14
README.md
sessions
THEMES.md
---
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md:61521:  [a_faire ] J11.1  j11 — Le produit — les exemples rejoués
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md:61580:  [a_faire ] J11.1  j11 — Le produit — les exemples rejoués
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md:61581:  [a_faire ] J11.2  j11 — Le produit — la
… [8111 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '50,110p' docs/pilotage/roadmap.md; echo ---; sed -n '100,130p' docs/pilotage/en-cours.md; echo ---; sed -n '1,60p' docs/pilotage/en-cours.md", "description": "Read roadmap and en-cours context"}`

  ```
(`porte-ressources`) est validée ; compteurs **574 fiches / 660 JSON**.

**J3.2** : les deux faces ne mesurent pas le même objet — Panini §150 est une distance de tradition (3/655 paires inter-langues), sa fonction `lang_distance` couvre 5/21 langues (200/210 paires « inconnues »), Glottolog 21/21 ; 154/154 paires hors script au hasard exact, le signal de famille vit dans 2-3 paires ; la face atomes n'est pas disponible (V14 3/21) ([fiche](../../reports/rapport-genealogie-deux-faces.md)).

**J7.1** sépare la **sœur** de la **famille lointaine** : sur 532 textes Panini (445 langues, 1948), le top-1 est de la même famille **66,1 %** (hasard 10,3 %) et de la même branche **26,1 %** (hasard 2,5 %), mais **hors écriture tout est au hasard** ; sur les 25 langues LANG_TREE, les sœurs valent **0,619** contre **0,0445** pour les familles différentes (**13,9×**, coefficient **+0,448**, p=0,002, 11/11 langues positives), alors que l'échantillon 20 ne montre **aucun** contraste de sœur (0,058 vs 0,039, p=0,078). J3.1 est **reproduit à l'identique** (écart 0) ; son coefficient de famille (+0,056) était un **minorant** dilué. L'époque est mono-époque par construction (1948) ; le placebo de dates
… [11162 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/verifier_schema_produit.py --json; echo EXIT=$?", "description": "Run schema verifier on both versions"}`

  ```
{
 "schemas": {
  "1": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/schemas/drave-annotation-v1.json",
  "2": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/schemas/drave-annotation-v2.json"
 },
 "versions_lues": [
  1,
  2
 ],
 "validateur": true,
 "retrocompatibilite": {
  "v1_lue": true,
  "v2_refuse_v1": true
 },
 "cas": [
  {
   "cas": "fr",
   "version": 2,
   "ok": true,
   "erreurs": []
  },
  {
   "cas": "en",
   "version": 2,
   "ok": true,
   "erreurs": []
  },
  {
   "cas": "vide",
   "version": 2,
   "ok": true,
   "erreurs": []
  },
  {
   "cas": "ponctuation",
   "version": 2,
   "ok": true,
   "erreurs": []
  },
  {
   "cas": "long",
   "version": 2,
   "ok": true,
   "erreurs": []
  },
  {
   "cas": "v1",
   "version": 1,
   "ok": true,
   "erreurs": []
  }
 ]
}
EXIT=0
  ```

- **bash** `{"command": "grep -n \"JSON :\" reports/rapport-evaluer-langue.md reports/rapport-exemples-rejoues.md reports/rapport-restitution-v1.md 2>/dev/null | head; echo ---; ls reports | grep -E \"evaluer-langue|exemples-rejoues|restitution-v1\"", "description": "Check JSON sidecar naming conventions"}`

  ```
---
evaluer-langue.json
pensee-restitution-v1.json
rapport-evaluer-langue.md
rapport-exemples-rejoues.json
rapport-exemples-rejoues.md
rapport-restitution-v1.md
  ```

- **bash** `{"command": "grep -rn \"schema v2\\|schema-v2\\|schéma v2\" README.md docs/README.md docs/produit/exemples.md | head -30", "description": "Check other schema v2 mentions"}`

  ```
docs/produit/exemples.md:10:> ([schéma v2](../../tools/schemas/drave-annotation-v2.json)).
  ```

- **bash** `{"command": "git log --oneline --all -- reports/rapport-schema-v1.md | head; echo ---; git show --stat --oneline 9a259953 2>/dev/null | head -30; echo ---; git show --stat --oneline 8eb0cc49 2>/dev/null | head -20", "description": "Inspect schema v2 commit history"}`

  ```
ecef7250 J9.1 — PASSE D'HONNÊTETÉ : 19 FICHES « INSTANTANÉ HISTORIQUE », 4 CHIFFRES DÉPASSÉS NE SE LISENT PLUS COMME L'ÉTAT COURANT
1f61caaa FICHES — DIX FICHES ANNOTÉES « INSTANTANÉ HISTORIQUE » (L'ÉTAT COURANT EST 86,25 / 0,7535 / 236-237)
550d6d07 PRODUIT — LE TEST DES 50 TEXTES LIBRES (0 CHEVAUCHEMENT EN filtrer, 4 TESTS) ENTRE DANS LA PORTE : 10 CONTRÔLES
97918c05 PRODUIT — LE SCHÉMA V1 PUBLIÉ (tools/schemas/drave-annotation-v1.json, Draft 2020-12) ET VALIDÉ SUR 5 CAS ; PORTE À 9 CONTRÔLES ; 183/183
037fe041 PRODUIT — LE CONTRAT V1 : schema/version, REFUS EN JSON (CODE 3), SURROGATE ET NON-STR TOLÉRÉS ; PORTE À 8 CONTRÔLES ; 183/183
---
9a259953 B13 — SCHÉMA v2 : meta.partition + meta.alternative, 26 CAS VALIDÉS (0 ÉCHEC), v1 TOUJOURS LUE
 docs/pilotage/en-cours.md                          |   19 +-
 docs/pilotage/roadmap.md                           |    2 +-
 docs/pilotage/semaine-autonome.md                  |    2 +-
 docs/produit/README.md                             |  102 +-
 docs/produit/exemples.md                           |   19 +-
 journal/2026-11-07/README.md                       |    7 +-
 journal/2026-11-07/distribue.md                    |    2 +-
 journal/202
… [2262 caractères tronqués]
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

- **bash** `{"command": "sed -n '1,120p' docs/methode/rangement.md; echo ---; sed -n '1,100p' docs/methode/portes.md", "description": "Read filing and gate method docs"}`

  ```
# Le rangement, et la revue de documentation

> Document de tâche, chargé depuis [`AGENTS.md`](../../AGENTS.md). La règle la plus souvent violée du dépôt : à lire
> **avant de classer un fichier** ou de clore un sous-chantier.

## Les quatre dossiers (règle stricte)

| dossier | ce qu'il contient | ce qu'il ne contient **jamais** |
|---|---|---|
| **`docs/`** | quatre familles : **méthode**, **pilotage**, **théorie**, **implantation** — ce qui reste vrai quand les chiffres changent | des **résultats** de mesure, des tableaux de chiffres, des comptes rendus de round |
| **`reports/`** | les **résultats mesurés** : fiches, séries de mesures, tableaux, erratums, récits de round, JSON de résultats | la documentation de référence |
| **`journal/`** | le **récit daté** : ce qui a été fait, quand, et ce qu'on en a appris | les chiffres seuls (ils vont dans `reports/`) |
| **`data/`** | les corpus et leur généalogie (`data/udhr/`, `data/corpus_*.txt`, `data/eurlex/`) | du code |

Dans `docs/`, les quatre familles sont **séparées** : `methode/` (comment on travaille), `pilotage/` (où l'on en
est), `theorie/` (ce qui reste vrai), `implantation/` (comment c'est construit). Une page de `docs/`
… [9140 caractères tronqués]
  ```

- **bash** `{"command": "ls -la journal/2026-11-14/; echo ---; sed -n '1,80p' journal/2026-11-14/README.md 2>/dev/null; echo ---; grep -n \"J11.3\\|J11.4\" journal/2026-11-14/*.md | head -30", "description": "Inspect today's journal notes"}`

  ```
total 28
drwxr-xr-x. 1 stephane stephane   90 14 nov 04:52 .
drwxr-xr-x. 1 stephane stephane  972 14 nov 00:51 ..
-rw-r--r--. 1 stephane stephane 3205 14 nov 04:57 docs.md
-rw-r--r--. 1 stephane stephane 1208 14 nov 04:57 memoire.md
-rw-r--r--. 1 stephane stephane 2595 14 nov 04:57 mesures.md
-rw-r--r--. 1 stephane stephane 1633 14 nov 04:57 portes.md
-rw-r--r--. 1 stephane stephane 9075 14 nov 04:57 README.md
---
# 2026-11-14

> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
> [`journal/2026-11-14/`](README.md). Le récit écrit à la main est conservé plus bas, dans
> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
> [l'index des sessions](../README.md#sessions).

**13 commits** · **1 session(s)** · **4 thème(s)**

## Thèmes du jour

| thème | commits | fichier |
|---|---|---|
| docs | 3 | [docs.md](docs.md) |
| memoire | 2 | [memoire.md](memoire.md) |
| mesures | 6 | [mesures.md](mesures.md) |
| portes | 2 | [portes.md](portes.md) |

## Sessions DSH

| session | titre | début | durée | liens |
|---|---|---|---|---|
| `e181ce02-cd50-488a-a6be-e84b79d40dcc` | Documentation Drave avec diagrammes et implémentation | 2026-
… [5406 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -30; echo EXIT=$?", "description": "Check document size budget"}`

  ```
budget de contexte · documents chargeables
    mots lignes  cat budget  document
    8114    427   T1   9000  docs/pilotage/roadmap.md
    5999    597 DATÉ      0  docs/implantation/contexte-long.md
    4858    515   T1   5000  docs/theorie/glossaire/10-le-pont-linguistico-semantique-le-vocabu.md
    4085    431 DATÉ      0  docs/implantation/numa-segregation.md
    3310    317   T1   3500  README.md
    3072    341 DATÉ      0  docs/implantation/convertisseur.md
    2962    364   T1   5000  docs/theorie/glossaire/02-modeles-et-architectures.md
    2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2746    203   T1   2800  reports/README.md
    2450    166   T1   2500  docs/pilotage/references-non-regression.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/form
… [511 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -60; echo EXIT=$?", "description": "Run documentation review baseline"}`

  ```
revue de documentation · 727 fiche(s) · 821 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
EXIT=0
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | grep -E \"produit/README|schema-v2|rapport-schema\" || true; echo ---; grep -n \"produit/README\" docs/methode/contexte.md", "description": "Check README budget category"}`

  ```
---
[exit code: 1]
  ```

- **bash** `{"command": "sed -n '80,140p' journal/2026-11-14/README.md; echo ---; sed -n '1,60p' journal/2026-11-14/docs.md", "description": "Read J11.3 journal note and docs theme"}`

  ```
sœur dépasse même celui de l'écriture (+0,213) une fois la famille séparée. Fiche
[`reports/rapport-retrieval-familles.md`](../../reports/rapport-retrieval-familles.md), JSON
[`reports/retrieval-familles.json`](../../reports/retrieval-familles.json), outil
[`tools/retrieval_familles.py`](../../tools/retrieval_familles.py).
**J8.1 — la restitution v1 : le miroir strict ne monte pas, la forme canonique vaut 1,0000.**
La v0 restitue la surface **46/46** mais le miroir strict tombe à **5/46 = 0,1087** parce que
`rendre_mots`/`rendre_pos` séparent la ponctuation (`dort .`). La v1 construit une **forme
canonique** depuis les **segments + rôles + cibles** : **46/46 formes exactes** contre une
source canonisée (casse repliée, ponctuation retirée), mais **1/46 = 0,0217** contre la source
brute — et le **miroir strict reste 0,1087**. C'est la réponse : le strict ne doit pas monter,
il mesure la surface ; la forme canonique mesure autre chose. La structure tient : **395
segments**, **395 rôles**, **315 cibles**, **315/315 résolues**, **313/315** portées par un
autre segment ; couverture **65,84 % des jetons**, **75,19 % des caractères**. La limite est la
**stabilité structurelle** : **18/46**
… [4801 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' tools/revue_documentation.py", "description": "Understand doc review checks"}`

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
… [2953 caractères tronqués]
  ```

- **bash** `{"command": "ls -la .git/hooks/ | head -20; echo ---; sed -n '1,160p' tools/verifie_etat_a_jour.py", "description": "Inspect pre-commit hook state"}`

  ```
total 68
drwxr-xr-x. 1 stephane stephane  576 31 oct 12:55 .
drwxr-xr-x. 1 stephane stephane  180 14 nov 04:58 ..
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
#!/usr/bin/env python3
"""ver
… [6312 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '120,280p' tools/revue_documentation.py", "description": "Read freshness and counter checks"}`

  ```
def extrait_entier(texte: str, motif: str):
    m = re.search(motif, texte)
    return int(m.group(1)) if m else None


def main() -> int:
    alertes: list[str] = []
    en = RACINE / "docs/pilotage/en-cours.md"
    if not en.exists():
        print("✗ docs/pilotage/en-cours.md absent")
        return 1
    t = en.read_text()

    # 2. les sept chantiers
    ids = sorted(set(re.findall(r"\*\*(C[1-7])\*\*", t)))
    if len(ids) < 7:
        alertes.append(f"structure : {len(ids)} chantiers sur 7 dans en-cours.md ({ids})")

    # 4. fraîcheur : la date de la page, ET aucun fait commité après le dernier état.
    #    La date seule ne suffit pas : deux commits du même jour passaient (A8.0, 29/10).
    m = re.search(r"Mis à jour : (\d{4}-\d\d-\d\d)", t)
    if not m:
        alertes.append("fraîcheur : en-cours.md n'a pas de date « Mis à jour : AAAA-MM-JJ »")
    else:
        page, dernier = m.group(1), date_dernier_commit()
        if dernier and page != dernier:
            alertes.append(
                f"fraîcheur : en-cours.md dit {page}, le dernier commit date du {dernier}"
            )
    retard = retards(RACINE)
    if retard and not etat_modifie(RACINE):
        etat, _fa
… [5922 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\nr=pathlib.Path('reports')\nprint('md', len(list(r.glob('*.md'))))\nprint('json', len(list(r.glob('*.json'))))\nEOF\ngit status --short reports | wc -l; git status --short reports | head", "description": "Count reports and JSON files"}`

  ```
md 727
json 821
10
 M reports/INDEX.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
?? reports/rapport-s-paragraphes.md
  ```

- **bash** `{"command": "grep -n \"fichiers / JSON\\|documents de\\|portes\\*\\*\\|chapitres de\" docs/pilotage/en-cours.md | head", "description": "Find counters in en-cours"}`

  ```
104:| chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
105:| fichiers / JSON de résultats | **727** / **821** | `reports/*.md` / `reports/*.json` |
106:| documents de `docs/` | **123** (hors archive et README) | `docs/**/*.md` |
  ```

- **bash** `{"command": "git show 9a259953 -- docs/produit/README.md | sed -n '1,220p'", "description": "Inspect original schema v2 README diff"}`

  ```
commit 9a259953dff03514c40fe3eb0403a3d3bc95703c
Author: Stéphane <stephane@localhost>
Date:   Sat Nov 7 14:23:24 2026 -0500

    B13 — SCHÉMA v2 : meta.partition + meta.alternative, 26 CAS VALIDÉS (0 ÉCHEC), v1 TOUJOURS LUE

diff --git a/docs/produit/README.md b/docs/produit/README.md
index 59627082..fa7c3492 100644
--- a/docs/produit/README.md
+++ b/docs/produit/README.md
@@ -5,10 +5,14 @@
 > il s'adresse, ce qu'il fait, comment l'exécuter, ce qu'il ne fait pas, ce qu'il coûte et ce
 > qu'il garantit.
 >
-> **Vérifié le 2026-11-06** sur la branche `s/v7`. Le point d'entrée `tools/drave.py` est
+> **Vérifié le 2026-11-07** sur la branche `s/v7`. Le point d'entrée `tools/drave.py` est
 > **livré** (version **0.1.0**) : `analyser`, `evaluer`, `rejouer` et `--version` existent, et la
-> porte produit est verte. Les exemples du § 3 sont réels : ils ont été lancés pour ce document.
-> Ce qui manque encore au contrat est nommé au § 7, sans être présenté comme acquis.
+> porte produit est verte. Le format est **version 2** (`schema: "drave.annotation"`,
+> `version: 2`) : le schéma v2 ajoute `meta.partition` et `meta.alternative`, et la **version 1
+> reste lue** ([`tools/schemas/`](../..
… [11897 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/drave.py analyser \"Le chat de la voisine qui dort sur le toit se réveille.\" --partition alternative --json > /tmp/ann.json 2>/tmp/ann.err; echo EXIT=$?; python3 - <<'EOF'\nimport json\nd=json.load(open('/tmp/ann.json'))\nprint('version', d['version'], 'nb', len(d['etique … [325 caractères tronqués]`

  ```
EXIT=0
version 2 nb 60
{
 "type": "REL",
 "debut": 22,
 "fin": 42,
 "valeur": "qui dort sur le toit",
 "meta": {
  "role": "qualite",
  "niveau": 2,
  "attachement": {
   "segment": "qui dort sur le toit",
   "cible": "voisine"
  },
  "partition": {
   "groupe": 0,
   "rang": 2,
   "membres": 3,
   "vue": "alternative"
  },
  "alternative": [
   {
    "type": "REL",
    "debut": 22,
    "fin": 54,
    "source": "heuristique",
    "union": true,
    "relation": "inclus",
    "rang": 1,
    "attachement": {
     "segment": "qui dort sur le toit se réveille",
     "cible": "réveille"
    },
    "role": "qualité"
   },
   {
    "type": "GV",
    "debut": 43,
    "fin": 54,
    "source": "heuristique",
    "union": false,
    "relation": "croise",
    "rang": 3,
    "attachement": {
     "segment": "se réveille",
     "cible": "voisine"
    },
    "role": "predicat"
   }
  ]
 }
}
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\ns=json.load(open('tools/schemas/drave-annotation-v2.json'))\np=s['properties']['etiquettes']['items']['properties']['meta']['properties']\nprint(json.dumps(p['partition'], ensure_ascii=False, indent=1))\nprint(json.dumps(p['alternative'], ensure_ascii=Fal … [80 caractères tronqués]`

  ```
{
 "type": "object",
 "required": [
  "groupe",
  "rang",
  "membres",
  "vue"
 ],
 "properties": {
  "groupe": {
   "type": "integer",
   "minimum": 0
  },
  "rang": {
   "type": "integer",
   "minimum": 1
  },
  "membres": {
   "type": "integer",
   "minimum": 2
  },
  "vue": {
   "enum": [
    "alternative",
    "filtrer_union",
    "filtrer"
   ]
  }
 },
 "additionalProperties": true
}
{
 "type": "array",
 "minItems": 1,
 "items": {
  "type": "object",
  "required": [
   "type",
   "debut",
   "fin",
   "source",
   "union",
   "relation",
   "rang"
  ],
  "properties": {
   "type": {
    "enum": [
     "GN",
     "GV",
     "GP",
     "REL",
     "SUB"
    ]
   },
   "debut": {
    "type": "integer",
    "minimum": 0
   },
   "fin": {
    "type": "integer",
    "minimum": 1
   },
   "source": {
    "enum": [
     "heuristique",
     "neuronal",
     "humain"
    ]
   },
   "union": {
    "type": "boolean"
   },
   "relation": {
    "enum": [
     "inclut",
     "inclus",
     "meme_span",
     "croise"
    ]
   },
   "rang": {
    "type": "integer",
    "minimum": 1
   },
   "retire": {
    "type": "boolean"
   },
   "attachement": {
    "type": "object",
    "required": [
   
… [275 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"alternative\\|partition\\|groupe\\|membres\\|relation\\|retire\\|union\" tools/bloc_linguistique.py | head -80", "description": "Locate partition construction in bloc"}`

  ```
92:# v2 : ajoute `meta.partition` et `meta.alternative` (partition des syntagmes qui se
525:    # 1er groupe : `nage` → `nager`, `commence` → `commencer` (la voyelle finale tombe)
532:    # formes du 1er groupe : `range` → `ranger` (le e reste, le g durcit)
803:                 union: bool = True, partition: str = "alternative"):
808:        self.union = union
809:        # "brut" : la sortie d'avant (chevauchements non documentés) ; "alternative" :
810:        # les deux segments restent, `meta.alternative` dit lequel est préféré ;
811:        # "filtrer_union" : on retire le S qui **contient** un segment chunker (le filtre
812:        # union du P0-3) ; "filtrer" : partition stricte, le chunker est la partition.
813:        # Dans les deux filtres, le segment retiré reste dans `meta.alternative` (`retire`).
814:        if partition not in ("brut", "alternative", "filtrer_union", "filtrer"):
815:            raise ValueError("partition attend 'brut', 'alternative', 'filtrer_union' ou 'filtrer'")
816:        self.partition = partition
1033:        chemin courant (union S/chunker) et exige un GV à droite **et** un GN à gauche.
1316:                    prec_aux = False      # le mot p
… [4513 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"def .*partition\\|def .*alternative\\|_partition\\|_alternative\" tools/*.py | head -40", "description": "Find partition helpers"}`

  ```
tools/bloc_linguistique.py:1806:            _expliciter_partition(etiquettes, filtrer=(
tools/bloc_linguistique.py:2385:def _relation_partition(x: Etiquette, y: Etiquette) -> str:
tools/bloc_linguistique.py:2407:def _groupes_partition(segs: list[Etiquette]) -> list[list[Etiquette]]:
tools/bloc_linguistique.py:2431:def _expliciter_partition(etiquettes: list[Etiquette], filtrer: str = "") -> None:
tools/bloc_linguistique.py:2445:    groupes = _groupes_partition(segs)
tools/bloc_linguistique.py:2494:                       "relation": _relation_partition(e, autre),
tools/clusters_moe.py:60:def partition_equilibree(co, ne, g, frequences=None, passes=6):
tools/mesurer_robustesse_semaine.py:56:    "chevauchements_alternative": "107 paires / 23/46 textes",
tools/mesurer_robustesse_semaine.py:301:            "api_alternative_schema_v2": api_alt_ok,
tools/mesurer_robustesse_semaine.py:303:            "api_alternative_champs_8": api_alt_champs,
tools/mesurer_robustesse_semaine.py:443:             "a26": A26["chevauchements_alternative"],
tools/mesurer_robustesse_semaine.py:503:                "cli_alternative": sum(1 for r in resultats if r["champs_8"]),
tools/mesurer_robustesse_semaine.py:50
… [664 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '2375,2515p' tools/bloc_linguistique.py", "description": "Read partition semantics implementation"}`

  ```
cout={"octets": len(texte.encode("utf-8", "replace")),
                                          "duree_s": round(time.perf_counter() - t0, 6)})
        if self.cache:
            self._cache[cle] = annotation
        return annotation


# --------------------------------------------------------------------------- compositions


def _relation_partition(x: Etiquette, y: Etiquette) -> str:
    """La relation de `y` vue **depuis** `x` : `inclut` = x contient y."""
    if x.debut == y.debut and x.fin == y.fin:
        return "meme_span"
    if x.debut <= y.debut and x.fin >= y.fin:
        return "inclut"
    if y.debut <= x.debut and y.fin >= x.fin:
        return "inclus"
    return "croise"


def _cle_preferee(e: Etiquette) -> tuple:
    """La vue préférée : le segment du chunker (union), le plus large, puis le plus sûr.

    Mesuré sur le gold 612 : dans 179/207 groupes ambigus qui portent un span du gold, le
    chunker le plus large **est** ce span (86,5 %) ; le S le plus large ne l'est que 25 fois sur 244.
    La préférence ne supprime rien par défaut : elle **classe**.
    """
    return (0 if (e.meta or {}).get("union") else 1, -(e.fin - e.debut), -e.confiance,
            e.d
… [5332 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/verifier_schema_produit.py --gold 20; echo EXIT=$?; echo ---; python3 tools/tests/test_schema_produit.py 2>&1 | tail -15; echo EXIT=${PIPESTATUS[0]}", "description": "Run verifier with gold 20 and schema tests"}`

  ```
✅ fr (v2)
  ✅ en (v2)
  ✅ vide (v2)
  ✅ ponctuation (v2)
  ✅ long (v2)
  ✅ v1 (v1)
  ✅ gold:g001 (v2)
  ✅ gold:g002 (v2)
  ✅ gold:g003 (v2)
  ✅ gold:g004 (v2)
  ✅ gold:g005 (v2)
  ✅ gold:g006 (v2)
  ✅ gold:g007 (v2)
  ✅ gold:g008 (v2)
  ✅ gold:g009 (v2)
  ✅ gold:g010 (v2)
  ✅ gold:g011 (v2)
  ✅ gold:g012 (v2)
  ✅ gold:g013 (v2)
  ✅ gold:g014 (v2)
  ✅ gold:g015 (v2)
  ✅ gold:g016 (v2)
  ✅ gold:g017 (v2)
  ✅ gold:g018 (v2)
  ✅ gold:g019 (v2)
  ✅ gold:g020 (v2)
  ✅ rétro-compatibilité : annotation v1 lue par le schéma v1
  ✅ contrôle négatif : le schéma v2 refuse une annotation v1
  ✅ validateur JSON Schema · 26 cas
EXIT=0
---
test_anglais_meme_schema (__main__.TestSchemaDuProduit.test_anglais_meme_schema) ... ok
test_les_huit_champs_obligatoires (__main__.TestSchemaDuProduit.test_les_huit_champs_obligatoires) ... ok
test_mutation_detectee (__main__.TestSchemaDuProduit.test_mutation_detectee)
Contrôle négatif : un JSON amputé d'un champ obligatoire est bien refusé par le test. ... ok
test_refus_est_une_reponse_json (__main__.TestSchemaDuProduit.test_refus_est_une_reponse_json) ... ok
test_rejeu_identique (__main__.TestSchemaDuProduit.test_rejeu_identique) ... ok
test_surrogate_isole_n
… [479 caractères tronqués]
  ```

- **bash** `{"command": "ls tools/porte-*.sh | sed 's#tools/##' | tr '\\n' ' '; echo; sed -n '1,80p' tools/porte-produit.sh", "description": "List gates and read product gate"}`

  ```
porte-adaptateur-sortie.sh porte-audit-drapeaux.sh porte-b1110-hybride.sh porte-balayage.sh porte-bloc-code.sh porte-bloc-linguistique.sh porte-bloc-maths.sh porte-bloc-tableaux.sh porte-budget.sh porte-bus.sh porte-bus-socket.sh porte-c4-retard.sh porte-cerveau.sh porte-consolidation.sh porte-coupe.sh porte-cycle-c2.sh porte-deepseek.sh porte-delais.sh porte-diff-couche.sh porte-document.sh porte-echange-experts.sh porte-episodique.sh porte-etat.sh porte-flux.sh porte-fusion.sh porte-gain.sh porte-greffe.sh porte-harnais-invariants.sh porte-homeostasie.sh porte-horloge.sh porte-indice.sh porte-jeux.sh porte-jumeaux.sh porte-lecteur.sh porte-lecture.sh porte-m5-brouillon.sh porte-melange.sh porte-memoire.sh porte-miroir-blocs.sh porte-mistral.sh porte-n3-cache.sh porte-n3-composition.sh porte-n3-deux-processus.sh porte-n3-deux-regions.sh porte-n3-generation.sh porte-n3-inventaire.sh porte-n3-placement.sh porte-n3-pont.sh porte-n3-positions.sh porte-n3-profondeur.sh porte-n3-refus.sh porte-n3-reseau.sh porte-n3-routes.sh porte-n3-service-briques.sh porte-n3-service.sh porte-n3-seuil.sh porte-n3-sparsite-compte.sh porte-n3-sparsite.sh porte-occupation-elagage.sh porte-occupation-mote
… [3933 caractères tronqués]
  ```

- **bash** `{"command": "cat > /tmp/mesurer_schema_v2_doc.py <<'PY'\n#!/usr/bin/env python3\n\"\"\"Mesure J11.4 : validation des deux versions du schéma de l'annotation.\"\"\"\nfrom __future__ import annotations\nimport copy, json, pathlib, subprocess, sys\nRACINE = pathlib.Path('/home/stephane/Data13TB/stephan … [4561 caractères tronqués]`

  ```
EXIT=0
{
 "date": "2026-11-14",
 "tache": "J11.4",
 "ligne": "B13",
 "objet": "documentation et validation du schéma v2",
 "code_measuré": "09e54143",
 "schemas": {
  "1": "tools/schemas/drave-annotation-v1.json",
  "2": "tools/schemas/drave-annotation-v2.json"
 },
 "validation_verificateur": {
  "commande": "python3 tools/verifier_schema_produit.py --json",
  "code_sortie": 0,
  "versions_lues": [
   1,
   2
  ],
  "validateur": true,
  "cas": 6,
  "echecs": 0,
  "versions_cas": [
   1,
   2
  ],
  "retrocompatibilite": {
   "v1_lue": true,
   "v2_refuse_v1": true
  }
 },
 "validation_gold20": {
  "commande": "python3 tools/verifier_schema_produit.py --gold 20",
  "code_sortie": 0,
  "cas": 26,
  "echecs": 0
 },
 "validation_gold_les_deux_versions": {
  "phrases": 612,
  "annotations_v2": 612,
  "echecs_v2": 0,
  "annotations_v1_derivees": 612,
  "echecs_v1": 0,
  "v2_refuse_v1": 612,
  "v1_refuse_v2": 612,
  "mutation_champ_obligatoire_refusee": true
 },
 "champs_vus_sur_le_gold": {
  "vue": "alternative",
  "porteurs_de_partition": 437,
  "groupes": 144,
  "alternatives": 930,
  "types": {
   "GV": 357,
   "GP": 49,
   "GN": 393,
   "SUB": 28,
   "REL": 103
  },
  "relations": {
… [255 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport sys, json\nsys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl\nfrom tools.tests.linguistique.evaluer_gold import charger\nh=bl.Heuristique(partition='alternative')\ntot=0; texts=set(); per=[]\nfor p in charger():\n    a=h.analyser(p['texte'], p['langu … [393 caractères tronqués]`

  ```
sum group ids per annotation 146 distinct texts 609 texts 612
annotations with groups 136
  ```

- **bash** `{"command": "python3 - <<'EOF'\np='/tmp/mesurer_schema_v2_doc.py'\ns=open(p).read()\ns=s.replace(\"groupes = set()\\n\", \"groupes = 0\\n\")\ns=s.replace(\"            groupes.add((a['texte'], m['partition']['groupe']))\\n\", \"\")\ns=s.replace(\"for a in v2_anns:\\n    for e in a.get('etiquettes',  … [565 caractères tronqués]`

  ```
{
 "vue": "alternative",
 "porteurs_de_partition": 437,
 "groupes": 146,
 "alternatives": 930,
 "types": {
  "GV": 357,
  "GP": 49,
  "GN": 393,
  "SUB": 28,
  "REL": 103
 },
 "relations": {
  "croise": 386,
  "inclus": 263,
  "inclut": 263,
  "meme_span": 18
 },
 "sources": {
  "heuristique": 930
 }
}
  ```

- **bash** `{"command": "grep -rn \"3\\.3 bis\\|3.3bis\\|vue des syntagmes\" docs reports README.md | head -20", "description": "Check references to section 3.3 bis"}`

  ```
docs/produit/README.md:185:### 3.3 bis La vue des syntagmes qui se chevauchent
reports/pensee-partition-syntagmes.json:883:   "diff": "--- a/tools/drave.py\n+++ b/tools/drave.py\n@@ -114,9 +114,17 @@\n         lr = max(len(r) for r in roles)\n         lignes.append(\"SYNTAGMES\")\n         for e, valeur, role, cible, span in zip(syntagmes, valeurs, roles, cibles, spans):\n+            part = (e.meta or {}).get(\"partition\")\n+            suffixe = \"\"\n+            if part:\n+                alts = (e.meta or {}).get(\"alternative\") or []\n+                retires = sum(1 for v in alts if v.get(\"retire\"))\n+                suffixe = (f\"  [g{part['groupe']} r{part['rang']}/{part['membres']}\"\n+                           f\" · alt={len(alts)}\"\n+                           + (f\" · {retires} retiré(s)\" if retires else \"\") + \"]\")\n             lignes.append(\n                 f\"  {e.type:<{lt}}  {span:<{lsp}}  {valeur:<{lv}}  \"\n-                f\"rôle={role:<{lr}}  → {cible}\"\n+                f\"rôle={role:<{lr}}  → {cible}{suffixe}\"\n             )\n     else:\n         lignes.append(\"SYNTAGMES —\")\n@@ -157,7 +165,7 @@\n \n \n def cmd_analyser(args: argparse.Name
… [1323 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "old_string": "### 3.3 bis La vue des syntagmes qui se chevauchent\n\n```bash\npython3 tools/drave.py analyser \"Le chat de la voisine qui dort sur le toit se réveille.\" --partition filtrer\n```\n\nQuatre vues ( … [6656 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **bash** `{"command": "sed -n '1,130p' docs/pilotage/en-cours.md", "description": "Read en-cours top and B13 paragraphs"}`

  ```
# En ce moment

**Mis à jour : 2026-11-14, 04 h 38 HNE (heure locale, EST).**

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
… [10200 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '60,100p' docs/pilotage/roadmap.md", "description": "Read roadmap B13 paragraphs"}`

  ```
**mesuré et borné** (table 14/14, corpus 418/438, retrieval J3.1, généalogie J3.2, familles
J7.1) ; la coordination N2/S/R/A est **datée**. La **clôture formelle** reste à faire : **J14.1**
doit refaire la passe et poser le tag `chantier-2026-11-14`. Le détail — chiffres, décisions
D1–D20, rejets R1–R30, échecs, reste — est dans
[`rapport-bilan-chantier.md`](../../reports/rapport-bilan-chantier.md) + JSON.

**J11.1 — les exemples rejoués.** Les **5 blocs** de `docs/produit/exemples.md` sont reproduits
avec le code courant ; **4 sont corrigés** : la ponctuation finale entre dans le POS (`g001`,
`r241`), le refus sort en **3** et `r035` — l'ancien échec connu — rend exactement le gold
(`REL [9:24] « she talks about » → film`). Le seul bloc identique est `g011`. F1 **0,7902**,
attachement **238/238 labels** (238/239 cibles, 0,9958) ; le mandat 237/238 est l'état d'avant
`s065`. Le contrôle négatif (mutation d'un token dans une copie de la doc) est détecté 4/5.
[`fiche`](../../reports/rapport-exemples-rejoues.md) + JSON. La suite produit est **J11.2**
(`evaluer --par-langue`), **J11.3** (50 textes libres), **J11.4** (schéma v2 documenté).

**J11.2 — la mesure par langue.** `evaluer --p
… [2256 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json, pathlib\nbase = json.loads(pathlib.Path('/tmp/schema-v2-doc.json').read_text(encoding='utf-8'))\nbase['documentation'] = {\n    'fichier': 'docs/produit/README.md',\n    'section': '3.3 bis — La vue des syntagmes qui se chevauchent — les champs du schéma v … [1614 caractères tronqués]`

  ```
reports/schema-v2-doc.json 2877
JSON_OK
  ```

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-schema-v2-doc.md", "content": "# J11.4 — le contrat : le schéma v2 documenté, 6 cas / 0 échec, v1 toujours lue\n\n> **Ligne de roadmap** : **B13** (produit) · **Tâche** : **J11.4** · **Date** : 2026-11-14 ·\n> **Verdict** … [11205 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-schema-v2-doc.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "grep -n \"J11.3\\|La vue d'ensemble\" docs/pilotage/en-cours.md docs/pilotage/roadmap.md", "description": "Locate J11.3 narrative lines"}`

  ```
docs/pilotage/en-cours.md:94:- **J11.1–J11.3** : `--par-langue` fr/en ; **J11.3** 50 textes libres, **115/0** chevauchements ; F1 **0,7902**, att. **238/239** ; [J11.1](../../reports/rapport-exemples-rejoues.md), [J11.2](../../reports/rapport-evaluer-langue.md), [J11.3](../../reports/rapport-robustesse-semaine.md).
docs/pilotage/en-cours.md:117:| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, gold 432, r035 + convention GV (0,7902), s065 (238/239), g017 rejeté, schéma v2, restitution v1 (canonique 46/46, strict 0,1087), J11.1–J11.3 (produit)** | **J11.4** (schéma v2 documenté) ; **trancher `g017`** ; puis T132/T133, gold 200+ ; **B10.3 bloquée** |
docs/pilotage/roadmap.md:73:(`evaluer --par-langue`), **J11.3** (50 textes libres), **J11.4** (schéma v2 documenté).
docs/pilotage/roadmap.md:83:JSON. La suite produit est **J11.3** (50 textes libres), **J11.4** (schéma v2 documenté).
docs/pilotage/roadmap.md:85:**J11.3 — les 50 textes libres.** Les **50 phrases de l'audit A26** sont rejouées avec le
docs/pilotage/roadmap.md:96:**La vue d'ensemble des chantiers** — huit chantiers (A, B, N, R, **S**, **L**, **D**, B13), leurs relations, leurs c
… [347 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (porte produit 183/183 ; [fiche](.. … [1233 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md": file has not been read — read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 200}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
1: # En ce moment
2: 
3: **Mis à jour : 2026-11-14, 04 h 38 HNE (heure locale, EST).**
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
… [11970 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (porte produit 183/183 ; [fiche](.. … [1233 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **J11.1–J11.4** : `--par-langue` fr/en ; **J11.3** 50 textes libres, **115/0** chevauchements ; **J11.4** schéma v2 documenté, **6 cas / 0 échec**, v1 lue ; F1 **0,7902**, att. **238/239** ; [ … [510 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "| fichiers / JSON de résultats | **728** / **822** | `reports/*.md` / `reports/*.json` |", "old_string": "| fichiers / JSON de résultats | **727** / **821** | `reports/*.md` / `reports/*.json` | … [2 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, gold 432, r035 + convention GV (0,7902), s065 (238/239), g017 rejeté, schéma v2, restitution v1 (ca … [500 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**N2** — porte (0,2856/0,3566) ; **Pensée** — `g017`, T132/T133, gold 200+ ; **J3.2** — V14 des 21 langues ; **J7.1** — réplication neuronale ; **S** — 11 verdicts + pointeur ; **R0.7** — split  … [356 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "limit": 120}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md</path>
<type>file</type>
<content>
1: # La roadmap de [Drave](../theorie/glossaire/entrees/drave.md) — un seul plan, quatre chantiers
2: 
3: > **Un seul document de plan.** Le **moteur** (A), l'**intelligence** (B), le **natif** (N) et le **lecteur** (R).
4: > L'ordre se décide par la **valeur** et les **dépendances**, jamais par une date. Les chiffres, les séries et les
5: > contrôles vivent dans [`reports/`](../../reports/) ; ici : l'[état](../theorie/glossaire/entrees/etat.md), la prochaine action, et ce qui bloque.
6: >
7: > **Détail et histoire** : l'ancien plan [A/B](../theorie/glossaire/entrees/a-b.md) est archivé dans
8: > [`roadmap-detail-2026-10-29.md`](../archive/roadmap-detail-2026-10-29.md), le détail N dans
9: > [`roadmap-native-2026-10-29.md`](../archive/roadmap-native-2026-10-29.md). Les **fiches de fonctionnalité** sont
10: > dans [`backlog/index.md`](backlog/index.md) ; le **graphe des dépendances** est dans
11: > [`backlog/dependances.md`](backlog/dependances.md). La **page vivante** est [`en-cours.md`](en-cours.md).
12: 
13: ## Comment lire cette roadmap
14: 
15: - **Les états** : ✅ m
… [19132 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "new_string": "**code 3 avec JSON**. [`fiche`](../../reports/rapport-robustesse-semaine.md) + JSON. La suite\nproduit est **J11.4** (schéma v2 documenté).\n\n**J11.4 — le schéma v2 documenté.** La notice produi … [1180 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-14/README.md", "offset": 90, "limit": 40}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-14/README.md</path>
<type>file</type>
<content>
90: il mesure la surface ; la forme canonique mesure autre chose. La structure tient : **395
91: segments**, **395 rôles**, **315 cibles**, **315/315 résolues**, **313/315** portées par un
92: autre segment ; couverture **65,84 % des jetons**, **75,19 % des caractères**. La limite est la
93: **stabilité structurelle** : **18/46** seulement après re-analyse de la surface canonique (le
94: lexique, lui, est stable 46/46). Contrôles : mélange/troncature canoniques **0/46**, détection
95: **46/46** ; rôles/cibles retirés, clé changée **43/43** textes éligibles. Fiche
96: [`reports/rapport-restitution-v1.md`](../../reports/rapport-restitution-v1.md), JSON
97: [`reports/pensee-restitution-v1.json`](../../reports/pensee-restitution-v1.json), outil
98: [`tools/mesurer_restitution_v1.py`](../../tools/mesurer_restitution_v1.py).
99: **J11.3 — les 50 textes libres : le contrat tient, la vue linéaire ne chevauche pas.** Les
100: **50 phrases de l'audit A26** sont rejouées avec le code du 14/11 (F1 **0,7902**, schéma
101: **v2**, restitution **v1**) : **0 plantage**, **50/50 JSO
… [1025 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-14/README.md", "new_string": "[`reports/pensee-robustesse-semaine.json`](../../reports/pensee-robustesse-semaine.json), outil\n[`tools/mesurer_robustesse_semaine.py`](../../tools/mesurer_robustesse_semaine.py).\n**J11.4 — … [1432 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-14/README.md has been updated successfully.
  ```

- **bash** `{"command": "git diff --stat reports/INDEX.md; git diff reports/INDEX.md | head -60", "description": "Inspect existing INDEX modification"}`

  ```
reports/INDEX.md | 9 ++++++++-
 1 file changed, 8 insertions(+), 1 deletion(-)
diff --git a/reports/INDEX.md b/reports/INDEX.md
index 5506faf4..f782d6e5 100644
--- a/reports/INDEX.md
+++ b/reports/INDEX.md
@@ -1,6 +1,6 @@
 # Index des fiches de reports/
 
-> **Généré** par `tools/index_reports.py` — **718 fiches**. Les fichiers
+> **Généré** par `tools/index_reports.py` — **724 fiches**. Les fichiers
 > d'infrastructure (`README.md`, `INDEX.md`, `historique-*`) sont exclus du tableau ;
 > la page d'état, elle, compte tous les `.md` de `reports/`.
 
@@ -78,6 +78,7 @@
 | [rapport-b13-porte-134.md](rapport-b13-porte-134.md) | B13 — la porte est à 134/140 : le 140/140 de 702b368c ne se rejoue pas ; quatre rouges viennent du sous-module S |
 | [rapport-b13-porte-138.md](rapport-b13-porte-138.md) | B13 — la porte est à 138/140 : les six attendus du sous-module S 00d2a01 sont fixés ; T132/T133 restent |
 | [rapport-b13-porte-140.md](rapport-b13-porte-140.md) | B13 — la porte est à 140/140 : les six attendus du sous-module S 00d2a01 sont fixés ; T132/T133 alignés sur 2/5 (distracteurs r428–r432) |
+| [rapport-bilan-chantier.md](rapport-bilan-chantier.md) | J10.1 — le bilan du chantier : F1
… [5903 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"rapport-schema-v2-doc\\|rapport-robustesse-semaine\\|rapport-s-paragraphes\" reports/INDEX.md reports/README.md || true", "description": "Check report index entries"}`

  ```
reports/INDEX.md:682:| [rapport-robustesse-semaine.md](rapport-robustesse-semaine.md) | J11.3 — les 50 textes libres : 0 plantage, 50/50 au schéma v2, 115 chevauchements en `alternative`, 0 en `filtrer` |
reports/INDEX.md:693:| [rapport-s-paragraphes.md](rapport-s-paragraphes.md) | S — La banque de paragraphes passe à neuf : six paires d'Alice, sources anglaises et référents |
  ```

- **bash** `{"command": "head -20 reports/rapport-s-paragraphes.md; wc -l reports/rapport-s-paragraphes.md; git log --oneline --all -- reports/rapport-s-paragraphes.md | head", "description": "Inspect untracked S report"}`

  ```
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
| a006 | « Comme cela n'avançait à rien… elle retourna vers la table… » | *There seemed to be no use in waiting by the little door…* | 4 |
| a007 | « C'est bien facile à dire « Buvez-moi », mais Alice était trop fine… » | *It was all ve
… [539 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,200p' tools/index_reports.py", "description": "Read report index generator"}`

  ```
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

RACINE = pathlib.Path(__file__).resolve().parent.parent


def titre(p: pathlib.Path) -> str:
    for ligne in p.read_text(encoding="utf-8", errors="ignore").splitlines():
        if ligne.startswith("# "):
            return ligne[2:].strip().replace("|", "—")
    return p.stem.replace("-", " ")


def fiches() -> list[pathlib.Path]:
    return sorted(
        p for p in (RACINE / "reports").glob("*.md")
        if p.name not in ("README.md", "INDEX.md") and not p.n
… [1392 caractères tronqués]
  ```

- **bash** `{"command": "ls reports/historique-* 2>/dev/null; python3 - <<'EOF'\nimport pathlib\nr=pathlib.Path('reports')\nfs=[p for p in r.glob('*.md') if p.name not in ('README.md','INDEX.md') and not p.name.startswith('historique-')]\nprint(len(fs))\nprint([p.name for p in fs if 'paragraphes' in p.name])\nE … [46 caractères tronqués]`

  ```
reports/historique-passes-portes.md
725
['rapport-s-paragraphes.md']
  ```

- **bash** `{"command": "set -euo pipefail\nsrc=\"reports/rapport-s-paragraphes.md\"\ntmp=\"/tmp/rapport-s-paragraphes.md.$$\"\ntest -f \"$src\" || { echo \"absent: $src\"; exit 1; }\nmv -- \"$src\" \"$tmp\"\ntrap 'mv -- \"$tmp\" \"$src\"' EXIT\npython3 tools/index_reports.py\nmv -- \"$tmp\" \"$src\"\ntrap - EX … [219 caractères tronqués]`

  ```
724 fiches → reports/INDEX.md
RESTAURE
697:| [rapport-schema-v2-doc.md](rapport-schema-v2-doc.md) | J11.4 — le contrat : le schéma v2 documenté, 6 cas / 0 échec, v1 toujours lue |
# Index des fiches de reports/

> **Généré** par `tools/index_reports.py` — **724 fiches**. Les fichiers
> d'infrastructure (`README.md`, `INDEX.md`, `historique-*`) sont exclus du tableau ;
> la page d'état, elle, compte tous les `.md` de `reports/`.
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -40; echo EXIT=$?", "description": "Run doc review after changes"}`

  ```
revue de documentation · 728 fiche(s) · 822 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
EXIT=0
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -8; echo EXIT=$?", "description": "Check document budgets"}`

  ```
1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4003 mots (budget 4 000)

  avertissements :
     · 49 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 1 violation(s) :
     · T0 : 4003 mots (AGENTS + en-cours + une tâche) > budget 4 000
EXIT=0
  ```

- **bash** `{"command": "python3 tools/verifier_schema_produit.py --json >/tmp/schema-json-final.json; echo SCHEMA_EXIT=$?; python3 - <<'EOF'\nimport json\nd=json.load(open('/tmp/schema-json-final.json'))\nprint(d['versions_lues'], d['validateur'], len(d['cas']), sum(1 for r in d['cas'] if not r['ok']), d['retr … [71 caractères tronqués]`

  ```
SCHEMA_EXIT=0
[1, 2] True 6 0 {'v1_lue': True, 'v2_refuse_v1': True}
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib,re\nfor p in ['AGENTS.md','docs/pilotage/en-cours.md','docs/methode/resultats.md']:\n    t=pathlib.Path(p).read_text()\n    print(p, len(t.split()))\nEOF\nsed -n '1,120p' tools/taille_documents.py", "description": "Measure T0 components"}`

  ```
AGENTS.md 1196
docs/pilotage/en-cours.md 1633
docs/methode/resultats.md 524
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

# (catégorie, budget en mots). Les globs sont réso
… [4004 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '120,260p' tools/taille_documents.py", "description": "Read T0 max calculation"}`

  ```
if "ne pas charger" not in tete.lower() and "ne jamais charger" not in tete.lower():
                    violations.append(f"{rel} : document daté sans consigne « ne pas charger par défaut »")
            if budget and n > budget:
                violations.append(f"{rel} : {n} mots > budget {budget} ({cat})")

    # fiches de résultats trop longues : avertissement, pas échec
    longues = []
    for p in sorted((RACINE / "reports").glob("*.md")):
        if p.name in ("README.md", "INDEX.md") or p.name.startswith("historique-"):
            continue
        n = p.read_text(encoding="utf-8", errors="ignore").count("\n") + 1
        if n > 300:
            longues.append((n, p.name))
    if longues:
        longues.sort(reverse=True)
        avertissements.append(
            f"{len(longues)} fiche(s) > 300 lignes : lire le verdict + une section, jamais tout "
            f"(plus longues : {', '.join(f'{n} l. {nom}' for n, nom in longues[:5])})"
        )

    # T0 : la somme des trois lectures par défaut
    def poids(rel: str) -> int:
        q = RACINE / rel
        return mots_hors_diagrammes(q.read_text(encoding="utf-8", errors="ignore")) if q.exists() else 0

    # Le T0 est «
… [1498 caractères tronqués]
  ```

- **bash** `{"command": "git show HEAD:docs/pilotage/en-cours.md | python3 -c \"import sys,re;print(len(re.findall(r'\\\\S+',sys.stdin.read())))\"; git diff --stat docs/pilotage/en-cours.md", "description": "Compare en-cours word count before edits"}`

  ```
1628
 docs/pilotage/en-cours.md | 10 +++++-----
 1 file changed, 5 insertions(+), 5 deletions(-)
  ```

- **bash** `{"command": "git diff docs/pilotage/en-cours.md", "description": "Show en-cours diff"}`

  ```
diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index 1159fac1..9aa71659 100644
--- a/docs/pilotage/en-cours.md
+++ b/docs/pilotage/en-cours.md
@@ -60,7 +60,7 @@
 - **Stratégie** : v0 mesuré.
 - **Ambition** : un runtime cognitif tracé.
 - **Objectif final** : un moteur de pensée v0.
-- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (porte produit 183/183 ; [fiche](../../reports/rapport-s065.md)) ; **`r035`**, **convention des GV** (0,7902, 0 perte) ; **J6.1 rejetée** (test −0,0028, att. 236/237 ; [fiche](../../reports/rapport-g017.md)) ; **restitution v1** (46/46 canonique, strict 0,1087 ; [fiche](../../reports/rapport-restitution-v1.md)) ; **J11.1–J11.2** (produit : [exemples](../../reports/rapport-exemples-rejoues.md), [par-langue](../../reports/rapport-evaluer-langue.md)) ; **contrat v1**, **`drave` v0**.
+- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (porte produit 183/183 ; [fiche](../../reports/rapport-s065.md)) ; **`r035`**, **conventio
… [5713 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (porte produit 183/183 ; [fiche](.. … [1332 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **J11.1–J11.4** : `--par-langue` fr/en ; **J11.3** 50 textes libres, **115/0** chevauchements ; **J11.4** schéma v2, **6 cas / 0 échec** ; F1 **0,7902**, att. **238/239** ; [J11.1](../../repor … [602 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -5; echo EXIT=${PIPESTATUS[0]}", "description": "Recheck T0 budget"}`

  ```
avertissements :
     · 49 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
EXIT=0
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -5; echo EXIT=$?", "description": "Recheck doc review"}`

  ```
revue de documentation · 728 fiche(s) · 822 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
EXIT=0
  ```

- **bash** `{"command": "bash tools/porte-produit.sh 2>&1 | tail -20; echo EXIT=${PIPESTATUS[0]}", "description": "Run product gate", "timeoutMs": 600000}`

  ```
✅ version : drave 0.1.0
  ✅ analyser fr : JSON valide, étiquettes et syntagmes
  ✅ analyser en : JSON valide, étiquettes et syntagmes
  ✅ rejeu : sha256 f4b7822076a4203d deux fois
  ✅ smoke test : Ran 18 tests
  ✅ schéma v2 validé (5 cas v2 + 1 cas v1 + 20 phrases du gold)
  ✅ 50 textes libres : Ran 4 tests
  ✅ restitution v0 : surface exacte (miroir affiché)
  ✅ restitution v1 : forme canonique exacte, miroir strict distinct
  ✅ restitution v0/v1 : Ran 22 tests
  ✅ schéma v2 : Ran 8 tests
  ✅ refus : JSON avec refus, code 3
  ✅ autotest parallèle : 183/183 portes tenues
✅ porte produit verte
EXIT=0
  ```

- **bash** `{"command": "bash tools/porte-tableaux.sh 2>&1 | tail -15; echo EXIT=${PIPESTATUS[0]}", "description": "Run table gate", "timeoutMs": 600000}`

  ```
✅ 1793 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4157 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-14)
EXIT=0
  ```

- **bash** `{"command": "bash tools/porte-document.sh 2>&1 | tail -20; echo EXIT=${PIPESTATUS[0]}", "description": "Run document gate", "timeoutMs": 600000}`

  ```
=== PORTE R0.1 — LE GRAPHE DE DOCUMENT ===
=== PORTE R0.1 — LE GRAPHE DE DOCUMENT ===
  30 documents · 51 pages · 1477 régions
  types : {'blanc': 1447, 'code': 4, 'figure': 3, 'legende': 1, 'liste': 238, 'note': 120, 'paragraphe': 819, 'section': 230, 'tableau': 30, 'titre': 32}
  deux colonnes : 6 G puis 6 D, 0 retour(s)
  contrôle texte plat : échoue comme attendu
  notes hors corps : 120 région(s), 0 fuite(s)
    data/onu/pdf/A_RES_80_1-en.pdf                         85 régions  fidélité 1.000
    data/onu/pdf/A_RES_80_1-es.pdf                         93 régions  fidélité 1.000
    data/onu/pdf/A_RES_80_1-fr.pdf                         91 régions  fidélité 1.000
    data/onu/pdf/A_RES_80_1-ru.pdf                         95 régions  fidélité 1.000
    data/onu/pdf/A_RES_80_1-zh.pdf                         83 régions  fidélité 1.000
    data/onu/pdf/A_RES_80_10-en.pdf                       155 régions  fidélité 1.000
    … et 24 autres

✅ les 50 pages sont découpées, les partitions exactes, le rejeu identique,
   la fidélité ≥ 0,99 et les trois contrôles négatifs se comportent comme prévu.
✅ porte document verte
EXIT=0
  ```

- **bash** `{"command": "bash tools/porte-etat.sh 2>&1 | tail -15; echo EXIT=${PIPESTATUS[0]}", "description": "Run state gate", "timeoutMs": 600000}`

  ```
=== PORTE ÉTAT — LE FAIT ET SA LIGNE ===
  en-cours · 1627 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  état · dernier fait 55bde5c5 · dernier état 55bde5c5
  ✅ aucun fait commité après le dernier état
  ✅ autotest : 6 cas, dont 3 refus attendus et 3 passes
✅ porte état verte : aucun fait commité après le dernier état
EXIT=0
  ```

- **bash** `{"command": "git log -1 --format='%h %s' -- tools/bloc_linguistique.py tools/schemas tools/verifier_schema_produit.py tools/tests/test_schema_produit.py; echo ---; git log -1 --format='%h %s'; echo ---; git status --short | head -30", "description": "Identify last code commit for schema"}`

  ```
b6e474dc J6.2 — s065 : LA REL SUIVIE D'UN GV PREND LE SUJET DU GV (238/238 LABELS, 238/239 CIBLES, F1 0,7902 INCHANGÉ, 0 SPAN, 0 POS)
---
55bde5c5 J11.3 — LES 50 TEXTES LIBRES : 0 PLANTAGE, 50/50 SCHÉMA V2, 115 CHEVAUCHEMENTS ALTERNATIVE / 0 FILTRER ; RESTITUTION 46/46, STRICT 0,1087 (F1 0,7902)
---
 M docs/pilotage/en-cours.md
 M docs/pilotage/roadmap.md
 M docs/produit/README.md
 M journal/2026-11-14/README.md
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
?? reports/rapport-schema-v2-doc.md
?? reports/schema-v2-doc.json
  ```

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"mesurer_schema_v2_doc.py — mesure J11.4 : le schéma v2 documenté, les deux versions validées.\n\nCe que le banc mesure, sur le code du dépôt :\n\n- `tools/verifier_schema_produit.py --json` : 5 cas v2 + 1 cas v1, sélection par `version` ;\n- `tools/verifier … [9527 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/mesurer_schema_v2_doc.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "python3 tools/mesurer_schema_v2_doc.py; echo EXIT=$?; python3 -c \"import json;d=json.load(open('reports/schema-v2-doc.json'));print(d['validation_verificateur']);print(d['validation_gold_les_deux_versions']);print(d['champs_vus_sur_le_gold'])\"", "description": "Generate report JSON wi … [13 caractères tronqués]`

  ```
612 annotations v2 (0 échec) · 612 annotations v1 (0 échec)
  vérificateur : 6 cas, 0 échec · versions lues [1, 2]
  → /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/schema-v2-doc.json
EXIT=0
{'commande': 'python3 tools/verifier_schema_produit.py --json', 'code_sortie': 0, 'versions_lues': [1, 2], 'validateur': True, 'cas': 6, 'echecs': 0, 'versions_cas': [1, 2], 'retrocompatibilite': {'v1_lue': True, 'v2_refuse_v1': True}}
{'phrases': 612, 'annotations_v2': 612, 'echecs_v2': 0, 'annotations_v1_derivees': 612, 'echecs_v1': 0, 'v2_refuse_v1': 612, 'v1_refuse_v2': 612, 'mutation_champ_obligatoire_refusee': True}
{'vue': 'alternative', 'porteurs_de_partition': 437, 'groupes': 146, 'alternatives': 930, 'types': {'GN': 393, 'GP': 49, 'GV': 357, 'REL': 103, 'SUB': 28}, 'relations': {'croise': 386, 'inclus': 263, 'inclut': 263, 'meme_span': 18}, 'sources': {'heuristique': 930}}
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-schema-v2-doc.md", "new_string": "> [`verifier_schema_produit.py`](../tools/verifier_schema_produit.py),\n> [`mesurer_schema_v2_doc.py`](../tools/mesurer_schema_v2_doc.py),\n> [`test_schema_produit.py`](../tools/tests/tes … [403 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-schema-v2-doc.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-schema-v2-doc.md", "new_string": "- [`tools/verifier_schema_produit.py`](../tools/verifier_schema_produit.py) — sélection par version, cas v1, contrôle négatif.\n- [`tools/mesurer_schema_v2_doc.py`](../tools/mesurer_schem … [420 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-schema-v2-doc.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-schema-v2-doc.md", "new_string": "- **Le code mesuré** est celui du commit `09e54143` (F1 **0,7902**, attachement **238/239**,\n  schéma v2, restitution v1) ; J11.4 ne modifie **ni le bloc, ni le vérificateur, ni les\n  s … [307 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-schema-v2-doc.md has been updated successfully.
  ```

- **bash** `{"command": "python3 -m py_compile tools/mesurer_schema_v2_doc.py && echo PY_OK; git diff --check; echo DIFF_CHECK=$?", "description": "Compile new tool and check whitespace"}`

  ```
PY_OK
DIFF_CHECK=0
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -10; echo EXIT=$?", "description": "Run doc review after final edits"}`

  ```
revue de documentation · 728 fiche(s) · 822 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
EXIT=0
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -3; echo EXIT=${PIPESTATUS[0]}", "description": "Recheck context budget"}`

  ```
· 49 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
EXIT=0
  ```

- **bash** `{"command": "bash tools/porte-tableaux.sh 2>&1 | tail -5; echo EXIT=${PIPESTATUS[0]}", "description": "Recheck tables and links"}`

  ```
✅ 1793 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4160 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-14)
EXIT=0
  ```

- **bash** `{"command": "git diff --stat reports/INDEX.md; git diff reports/INDEX.md | grep -E '^\\+' | head -20; echo ---; grep -c \"^| \\[\" reports/INDEX.md", "description": "Verify INDEX diff and entries"}`

  ```
reports/INDEX.md | 9 ++++++++-
 1 file changed, 8 insertions(+), 1 deletion(-)
+++ b/reports/INDEX.md
+> **Généré** par `tools/index_reports.py` — **724 fiches**. Les fichiers
+| [rapport-bilan-chantier.md](rapport-bilan-chantier.md) | J10.1 — le bilan du chantier : F1 0,7533 → 0,7902, attachement 236 → 238, Panini mesuré et borné |
+| [rapport-evaluer-langue.md](rapport-evaluer-langue.md) | J11.2 — la mesure par langue : l'anglais devant, mais le gold n'est pas le même |
+| [rapport-exemples-rejoues.md](rapport-exemples-rejoues.md) | J11.1 — les cinq exemples rejoués : 4 blocs sur 5 ont bougé, `r035` n'est plus un échec |
+| [rapport-passe-honnetete.md](rapport-passe-honnetete.md) | Passe d'honnêteté — 19 fiches portent « instantané historique », les quatre chiffres dépassés ne se lisent plus comme l'état courant |
+| [rapport-restitution-v1.md](rapport-restitution-v1.md) | B13 — la restitution v1 : la forme canonique à 46/46, le miroir strict reste à 0,1087 |
+| [rapport-robustesse-semaine.md](rapport-robustesse-semaine.md) | J11.3 — les 50 textes libres : 0 plantage, 50/50 au schéma v2, 115 chevauchements en `alternative`, 0 en `filtrer` |
+| [rapport-schema-v2-doc.md](rapport-s
… [106 caractères tronqués]
  ```

- **bash** `{"command": "git diff -- docs/produit/README.md | sed -n '1,220p'", "description": "Review README diff"}`

  ```
diff --git a/docs/produit/README.md b/docs/produit/README.md
index 86f4c8b5..9c43373b 100644
--- a/docs/produit/README.md
+++ b/docs/produit/README.md
@@ -182,7 +182,7 @@ python3 tools/drave.py analyser --fichier corpus.txt --json    # le texte entier
 `--fichier` lit un texte UTF-8 ; `--jsonl` rend une **ligne JSON par phrase** (le format des
 traitements de corpus), chaque ligne portant le schéma **v2** complet (`version: 2`).
 
-### 3.3 bis La vue des syntagmes qui se chevauchent
+### 3.3 bis La vue des syntagmes qui se chevauchent — les champs du schéma v2
 
 ```bash
 python3 tools/drave.py analyser "Le chat de la voisine qui dort sur le toit se réveille." --partition filtrer
@@ -191,10 +191,91 @@ python3 tools/drave.py analyser "Le chat de la voisine qui dort sur le toit se r
 Quatre vues (`--partition`) : `alternative` (défaut : les deux segments restent, `meta.alternative`
 dit lequel est préféré — **aucune perte**), `filtrer` (vue linéaire : **F1 +0,047** mais **18
 attachements en moins**), `filtrer_union` (variante économique, 91 paires résiduelles) et `brut`
-(l'ancienne sortie). Le défaut est `alternative`. Un segment qui appartient à un groupe de
-chevauchement porte `
… [5693 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/verifie_journal.py 2>&1 | tail -15; echo EXIT=${PIPESTATUS[0]}", "description": "Verify journal structure"}`

  ```
journal · 46 jour(s) · 188 session(s) · 2484 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
EXIT=0
  ```

- **bash** `{"command": "python3 tools/verifie_en_cours.py 2>&1 | tail -15; echo EXIT=${PIPESTATUS[0]}", "description": "Verify en-cours structure"}`

  ```
en-cours · 1627 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
EXIT=0
  ```

- **bash** `{"command": "python3 tools/verifier_schemas.py 2>&1 | tail -10; echo EXIT=${PIPESTATUS[0]}", "description": "Verify SVG schemas"}`

  ```
schémas · 463 document(s) · 67 SVG · 2 source(s)
  ✅ aucun ASCII art, SVG valides et référencés, blocs PlantUML inline valides,
     sources et images relatives.
EXIT=0
  ```

- **bash** `{"command": "git status --short", "description": "Show working tree status before staging"}`

  ```
M docs/pilotage/en-cours.md
 M docs/pilotage/roadmap.md
 M docs/produit/README.md
 M journal/2026-11-14/README.md
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
?? reports/rapport-schema-v2-doc.md
?? reports/schema-v2-doc.json
?? tools/mesurer_schema_v2_doc.py
  ```

- **bash** `{"command": "git add docs/pilotage/en-cours.md docs/pilotage/roadmap.md docs/produit/README.md journal/2026-11-14/README.md reports/INDEX.md reports/rapport-schema-v2-doc.md reports/schema-v2-doc.json tools/mesurer_schema_v2_doc.py && git status --short && echo --- && git diff --cached --stat", "des … [41 caractères tronqués]`

  ```
M  docs/pilotage/en-cours.md
M  docs/pilotage/roadmap.md
M  docs/produit/README.md
M  journal/2026-11-14/README.md
M  reports/INDEX.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
A  reports/rapport-schema-v2-doc.md
 M reports/rapport-spans-chunker.md
A  reports/schema-v2-doc.json
 M tools/chantier/plan.json
A  tools/mesurer_schema_v2_doc.py
 m tools/structures
?? reports/rapport-s-paragraphes.md
---
 docs/pilotage/en-cours.md        |  10 +-
 docs/pilotage/roadmap.md         |  13 +++
 docs/produit/README.md           |  91 +++++++++++++++++-
 journal/2026-11-14/README.md     |  13 +++
 reports/INDEX.md                 |   9 +-
 reports/rapport-schema-v2-doc.md | 190 ++++++++++++++++++++++++++++++++++++
 reports/schema-v2-doc.json       | 112 +++++++++++++++++++++
 tools/mesurer_schema_v2_doc.py   | 203 +++++++++++++++++++++++++++++++++++++++
 8 files changed, 630 insertions(+), 11 deletions(-)
  ```

- **bash** `{"command": "sed -n '1,120p' .git/hooks/pre-commit", "description": "Read pre-commit hook"}`

  ```
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
# Le journal du jour, par thème (sources : git + journal/sessions). L'index README est
… [234 caractères tronqués]
  ```

- **bash** `{"command": "git commit -F - <<'MSG'\nJ11.4 — SCHÉMA v2 DOCUMENTÉ : 4 CHAMPS PARTITION + 10 CHAMPS ALTERNATIVE, 6 CAS / 0 ÉCHEC, LES DEUX VERSIONS LUES (612 v2 + 612 v1)\n\nLa notice docs/produit/README.md § 3.3 bis documente les champs de meta.partition\n(groupe, rang, membres, vue) et de meta.alte … [924 caractères tronqués]`
