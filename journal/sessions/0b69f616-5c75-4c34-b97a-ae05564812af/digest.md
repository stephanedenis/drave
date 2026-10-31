# Session DSH — relecture

- identifiant : `0b69f616-5c75-4c34-b97a-ae05564812af`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-10-30 21:46:19
- agent : standard


## Tour 1

### 👤 Utilisateur

continue

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
réseau sont des **faits** regroupés en **listes valuées poussées** vers leurs lecteurs : le coût du calcul devient proportionnel à l'**activité**, et le modèle devient **décomposable**, **répartissable** et **observable**. Le projet a pour principe que la structure bat la taille. Construire le moteur et modèle optimisé qui rend cette structure observable, décomposable, répartissable et rejouable permet d'atteindre de nouveaux sommets. Bref, révolutionner l'IA avec une approche par bus d'événements où chaque bloc fonctionnel est optimisable, comparable et substituable par des alternatives ayant des architectures différentes. e.g. Blocs neuronaux là où l'intuition est un avantage, blocs computationnels classiques pour les opérations où l'informatique classique est plus fiable et performante.

Le projet est né du besoin de faire tourner des modèles **de types différents** sur des machines **limitées**, de
les **combiner**, de les **décomposer en couches et grappes de neurones** exécutables par du matériel divers, voire
**distribué en réseau**, de les **diagnostiquer et faire évoluer** en étudiant leurs **flux**, et de **rejouer à
volonté** des événements.


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

⏵ Reprise de session : lecture de l'état courant et de la roadmap

- **get_goal** `{}`

  ```
{"goal":null}
  ```

- **bash** `{"command": "git status --short | head -50; echo \"---\"; git log --oneline -12", "description": "Show git status and recent commits"}`

  ```
MM journal/2026-10-29/README.md
D  journal/2026-10-29/attention.md
MM journal/2026-10-29/distribue.md
MM journal/2026-10-29/docs.md
MM journal/2026-10-29/memoire.md
MM journal/2026-10-29/mesures.md
MM journal/2026-10-29/modele.md
MM journal/2026-10-29/moteur.md
MM journal/2026-10-29/portes.md
MM journal/2026-10-30/README.md
D  journal/2026-10-30/distribue.md
D  journal/2026-10-30/docs.md
D  journal/2026-10-30/memoire.md
D  journal/2026-10-30/mesures.md
D  journal/2026-10-30/modele.md
D  journal/2026-10-30/moteur.md
D  journal/2026-10-30/portes.md
MM journal/README.md
MM journal/THEMES.md
D  reports/r13.3-anglais.json
D  reports/rapport-r13.3-anglais.md
 m tools/docwatch
?? =
?? journal/2026-10-29/attention.md
?? journal/2026-10-30/distribue.md
?? journal/2026-10-30/docs.md
?? journal/2026-10-30/memoire.md
?? journal/2026-10-30/mesures.md
?? journal/2026-10-30/modele.md
?? journal/2026-10-30/moteur.md
?? journal/2026-10-30/portes.md
?? reports/r13.3-anglais.json
?? reports/r4e-bloc-*.json
?? reports/r4s-bloc-*.json
?? reports/r4x-bloc-*.json
?? reports/rapport-r13.3-anglais.md
?? tools/r13_anglais.py
---
f590d884 DOCS — CONTINUITÉ 1 134 MOTS, ORGANISATION 1 579 : T0 3 989
b33b56ab L
… [894 caractères tronqués]
  ```

- **bash** `{"command": "wc -l docs/pilotage/en-cours.md docs/pilotage/roadmap.md 2>/dev/null; echo \"---\"; date", "description": "Check state file sizes and date"}`

  ```
137 docs/pilotage/en-cours.md
  339 docs/pilotage/roadmap.md
  476 total
---
ven 30 oct 2026 21:46:33 EDT
  ```

- **read** `{"file_path": "docs/pilotage/en-cours.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
1: # En ce moment
2: 
3: **Mis à jour : 2026-10-30, 13 h 05 HAE (heure locale, EDT).**
4: 
5: > **État courant, pas histoire.** Une sous-section par **session active** ; une ligne par **chantier** avec son
6: > **bloquant**. Les détails de méthode sont dans [`methode/`](../methode/) — chargement et budget dans
7: > [`contexte.md`](../methode/contexte.md), contrat des sessions dans [`continuite.md`](../methode/continuite.md).
8: > Les résultats sont dans [`reports/`](../../reports/) ; l'histoire dans
9: > [`journal/`](../../journal/) ; le plan dans [`roadmap.md`](roadmap.md).
10: 
11: ## Sessions en cours
12: 
13: > Contrat et budget : [`continuite.md`](../methode/continuite.md) ; sessions terminées :
14: > [`journal/sessions/`](../../journal/sessions/).
15: 
16: > **Plan d'abord.** Chaque session active expose son mandat dans
17: > [`journal/sessions/`](../../journal/sessions/) (`<id>/plan.md`) ; `python3 tools/sessions.py --status`
18: > avant d'écrire ici.
19: 
20: > **Écriture.** Toute session écrit l'état, **une à la fois** : un commit est atomique, et
21: > aucun 
… [8390 caractères tronqués]
  ```

- **bash** `{"command": "git diff --stat | tail -20; echo \"=== staged ===\"; git diff --cached --stat | tail -20; echo \"=== untracked ===\"; ls -la reports/r4e-bloc-*.json reports/r4s-bloc-*.json reports/r4x-bloc-*.json tools/r13_anglais.py reports/r13.3-anglais.json reports/rapport-r13.3-anglais.md 2>/dev/nu … [135 caractères tronqués]`

  ```
journal/2026-10-29/README.md    | 70 +++++++++++++++++++++++++++++++++++------
 journal/2026-10-29/distribue.md | 23 ++++++++++++--
 journal/2026-10-29/docs.md      | 11 ++++++-
 journal/2026-10-29/memoire.md   | 25 ++++++++++++++-
 journal/2026-10-29/mesures.md   | 41 ++++++++++++++++++++++--
 journal/2026-10-29/modele.md    | 23 ++++++++++++--
 journal/2026-10-29/moteur.md    |  4 ++-
 journal/2026-10-29/portes.md    | 56 +++++++++++++++++++++++++++++++--
 journal/2026-10-30/README.md    |  9 +++---
 journal/README.md               |  3 +-
 journal/THEMES.md               | 18 ++++++++---
 tools/docwatch                  |  0
 12 files changed, 252 insertions(+), 31 deletions(-)
=== staged ===
 journal/2026-10-29/distribue.md  | 23 ++-----------
 journal/2026-10-29/docs.md       | 11 +------
 journal/2026-10-29/memoire.md    | 25 +-------------
 journal/2026-10-29/mesures.md    | 41 ++---------------------
 journal/2026-10-29/modele.md     | 23 ++-----------
 journal/2026-10-29/moteur.md     |  4 +--
 journal/2026-10-29/portes.md     | 56 ++------------------------------
 journal/2026-10-30/README.md     |  9 +++---
 journal/2026-10-30/distribue.md  | 26 ---------------
 journal/
… [1161 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' docs/pilotage/roadmap.md", "description": "Read roadmap head"}`

  ```
# La roadmap de Drave — un seul plan, quatre chantiers

> **Un seul document de plan.** Le **moteur** (A), l'**intelligence** (B), le **natif** (N) et le **lecteur** (R).
> L'ordre se décide par la **valeur** et les **dépendances**, jamais par une date. Les chiffres, les séries et les
> contrôles vivent dans [`reports/`](../../reports/) ; ici : l'état, la prochaine action, et ce qui bloque.
>
> **Détail et histoire** : l'ancien plan A/B est archivé dans
> [`roadmap-detail-2026-10-29.md`](../archive/roadmap-detail-2026-10-29.md), le détail N dans
> [`roadmap-native-2026-10-29.md`](../archive/roadmap-native-2026-10-29.md). Les **fiches de fonctionnalité** sont
> dans [`backlog/index.md`](backlog/index.md) ; le **graphe des dépendances** est dans
> [`backlog/dependances.md`](backlog/dependances.md). La **page vivante** est [`en-cours.md`](en-cours.md).

## Comment lire cette roadmap

- **Les états** : ✅ mesuré et écrit · 🔬 en cours · ⏳ à faire · 🧱 bloqué par une infra absente.
- **Le carpe diem** : pas d'échéance. Un chantier est **fait** quand il est **mesuré**, **écrit** (fiche + docs) et
  **committé** ; tant qu'il ne l'est pas, il reste dans la liste — et on ne l'annonce pas avant
… [7235 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/sessions.py --status 2>&1 | head -40; echo \"=== journal recent ===\"; ls -lt journal/2026-10-30/ | head -20; echo \"=== sessions ===\"; ls -lt journal/sessions/ 2>/dev/null | head -10", "description": "Check sessions status and recent journal files"}`

  ```
sessions · plans de mandat
    71d57f53-8b41-4220 · terminé  · 641 min · docs/pilotage/en-cours.md, docs/methode/continuite.md, tools/sessions.py
      → coordination publiée ; migrer les trois sessions actives vers leur plan
  ⏰ 8156fdcb           · actif    · 522 min · R0.1–R0.5
      → la boucle de lecture (R11, dépend de N2) ou la restitution (R31, dépend de R21) — toutes deux hors R0 ; sinon consolidation.
  ⏰ N2-GPU             · actif    · 522 min · N2
      → N2 — la **hiérarchie** (état de section), porte **< 2,5** (meilleur **2,6998**, plateau **2,708**) ; **N5 gelé**.
  ⏰ c3d0f0bd           · actif    · 522 min · R4.1–R4.3, B10.2bis, A8.3b
      → **B10.2bis** suite (encodeur) ; **A8.3b** ; **R4.4 bloqué**.
  ⚠ mandat périmé (522 min) : 8156fdcb — heartbeat à rafraîchir
  ⚠ mandat périmé (522 min) : N2-GPU — heartbeat à rafraîchir
  ⚠ mandat périmé (522 min) : c3d0f0bd — heartbeat à rafraîchir
=== journal recent ===
total 36
-rw-r--r--. 1 stephane stephane 6202 30 oct 13:36 README.md
-rw-r--r--. 1 stephane stephane 1503 30 oct 13:36 portes.md
-rw-r--r--. 1 stephane stephane 1035 30 oct 13:36 moteur.md
-rw-r--r--. 1 stephane stephane 1435 30 oct 13:36 modele.md
-rw-r--r--
… [880 caractères tronqués]
  ```

- **bash** `{"command": "ls -lt reports/*.md | head -12; echo \"=== recent reports json ===\"; ls -lt reports/*.json | head -12; echo \"=== R13 mentions in roadmap ===\"; grep -n \"R13\\|R4e\\|R4s\\|R4x\\|anglais\" docs/pilotage/roadmap.md | head -30", "description": "List recent reports and roadmap R13 lines"}`

  ```
-rw-r--r--. 1 stephane stephane  2095 30 oct 13:30 reports/rapport-r13.4-graines.md
-rw-r--r--. 1 stephane stephane 48712 30 oct 13:06 reports/INDEX.md
-rw-r--r--. 1 stephane stephane  4320 30 oct 13:05 reports/rapport-a83c-lot.md
-rw-------. 1 stephane stephane  3141 30 oct 13:05 reports/rapport-a83d-lot-threads.md
-rw-r--r--. 1 stephane stephane  2332 30 oct 12:59 reports/rapport-sessions-plans.md
-rw-r--r--. 1 stephane stephane  4214 30 oct 12:58 reports/rapport-r06-publication.md
-rw-------. 1 stephane stephane  2970 30 oct 10:45 reports/rapport-n3.6-service-briques.md
-rw-r--r--. 1 stephane stephane  4005 30 oct 09:16 reports/rapport-b10-contraste.md
-rw-r--r--. 1 stephane stephane  4781 30 oct 09:03 reports/rapport-b10-mots-jw.md
-rw-r--r--. 1 stephane stephane  2487 30 oct 08:57 reports/rapport-a80-audit-final.md
-rw-r--r--. 1 stephane stephane  1488 30 oct 08:57 reports/rapport-a80-pannes-ppl.md
-rw-r--r--. 1 stephane stephane  2510 30 oct 08:53 reports/rapport-r13.3-anglais.md
=== recent reports json ===
-rw-r--r--. 1 stephane stephane     809 30 oct 13:30 reports/r13.4-graines.json
-rw-------. 1 stephane stephane     603 30 oct 13:05 reports/a83d-lot-threads.json
-rw-r--r
… [1572 caractères tronqués]
  ```

- **bash** `{"command": "git diff HEAD -- journal/README.md journal/THEMES.md journal/2026-10-30/README.md | head -200", "description": "Inspect journal diffs"}`

  ```
(no output)
  ```

- **bash** `{"command": "git log --oneline -5 -- reports/rapport-r13.3-anglais.md reports/r13.3-anglais.json journal/2026-10-30/; echo \"=== last commit files ===\"; git show --stat --oneline HEAD | head -30", "description": "History of deleted files and last commit"}`

  ```
f590d884 DOCS — CONTINUITÉ 1 134 MOTS, ORGANISATION 1 579 : T0 3 989
b33b56ab LA CARTE DE DÉCISION DES CHANTIERS — LA PROFONDEUR DE DÉPENDANCE COMME AXE, LES SOURCES NOMMÉES
21a361f9 R13.4 — DEUX GRAINES : BPE512 DANS LE BRUIT, BPE1024 PERD 4,09 %
842e1770 SESSIONS — LES TROIS PLANS CONFIRMÉS : PÉRIMÈTRES, FICHIERS, HEARTBEAT 13:05
68590bf0 LE GRAPHE CONFRONTE L'INDEX, L'ÉTAT POINTE LA FRONTIÈRE — SIX STATUTS DIVERGENTS CORRIGÉS
=== last commit files ===
f590d884 DOCS — CONTINUITÉ 1 134 MOTS, ORGANISATION 1 579 : T0 3 989
 docs/methode/continuite.md            | 39 ++++++-----------------------------
 docs/methode/organisation-du-depot.md |  3 +--
 journal/2026-10-30/README.md          |  5 +++--
 journal/2026-10-30/mesures.md         |  3 ++-
 4 files changed, 12 insertions(+), 38 deletions(-)
  ```

- **bash** `{"command": "git diff -- journal/2026-10-29/README.md | head -80; echo \"=== 10-30 mesures diff ===\"; git diff -- journal/2026-10-30/mesures.md | head -60", "description": "Inspect worktree vs index diffs"}`

  ```
diff --git a/journal/2026-10-29/README.md b/journal/2026-10-29/README.md
index 65093451..7c67f453 100644
--- a/journal/2026-10-29/README.md
+++ b/journal/2026-10-29/README.md
@@ -5,20 +5,20 @@
 > le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
 > [l'index des sessions](../README.md#sessions).
 
-**107 commits** · **0 session(s)** · **8 thème(s)**
+**160 commits** · **0 session(s)** · **8 thème(s)**
 
 ## Thèmes du jour
 
 | thème | commits | fichier |
 |---|---|---|
 | attention | 1 | [attention.md](attention.md) |
-| distribue | 10 | [distribue.md](distribue.md) |
-| docs | 23 | [docs.md](docs.md) |
-| memoire | 5 | [memoire.md](memoire.md) |
-| mesures | 41 | [mesures.md](mesures.md) |
-| modele | 7 | [modele.md](modele.md) |
-| moteur | 5 | [moteur.md](moteur.md) |
-| portes | 15 | [portes.md](portes.md) |
+| distribue | 16 | [distribue.md](distribue.md) |
+| docs | 27 | [docs.md](docs.md) |
+| memoire | 10 | [memoire.md](memoire.md) |
+| mesures | 52 | [mesures.md](mesures.md) |
+| modele | 12 | [modele.md](modele.md) |
+| moteur | 6 | [moteur.md](moteur.md) |
+| portes | 36 | [portes.md](portes.md) |
 
 ## Autres pièces du jour
 
@@ -140,6 +14
… [4530 caractères tronqués]
  ```

- **bash** `{"command": "git diff --cached --stat; echo \"=== show staged deletion of r13.3 ===\"; git log --oneline -3 --all -- reports/rapport-r13.3-anglais.md", "description": "Show staged changes summary"}`

  ```
journal/2026-10-29/README.md     | 70 ++++++----------------------------------
 journal/2026-10-29/attention.md  | 21 ------------
 journal/2026-10-29/distribue.md  | 23 ++-----------
 journal/2026-10-29/docs.md       | 11 +------
 journal/2026-10-29/memoire.md    | 25 +-------------
 journal/2026-10-29/mesures.md    | 41 ++---------------------
 journal/2026-10-29/modele.md     | 23 ++-----------
 journal/2026-10-29/moteur.md     |  4 +--
 journal/2026-10-29/portes.md     | 56 ++------------------------------
 journal/2026-10-30/README.md     |  9 +++---
 journal/2026-10-30/distribue.md  | 26 ---------------
 journal/2026-10-30/docs.md       | 19 -----------
 journal/2026-10-30/memoire.md    | 26 ---------------
 journal/2026-10-30/mesures.md    | 35 --------------------
 journal/2026-10-30/modele.md     | 30 -----------------
 journal/2026-10-30/moteur.md     | 27 ----------------
 journal/2026-10-30/portes.md     | 25 --------------
 journal/README.md                |  3 +-
 journal/THEMES.md                | 18 +++--------
 reports/r13.3-anglais.json       | 51 -----------------------------
 reports/rapport-r13.3-anglais.md | 51 -----------------------------
 21 files changed, 
… [143 caractères tronqués]
  ```

- **bash** `{"command": "ps aux | grep -E \"docwatch|journal|sessions.py|python3 tools\" | grep -v grep | head -20; echo \"=== reflog ===\"; git reflog -8", "description": "Check running processes and reflog"}`

  ```
root         926  0.0  0.2 442176 267716 ?       Ss   oct25   2:26 /usr/lib/systemd/systemd-journald
stephane 2218562  2.2  0.0 478736 34308 ?        Ssl  12:58  11:38 /home/stephane/.local/share/pipx/venvs/docwatch/bin/python -E /home/stephane/.local/bin/docwatch --config /home/stephane/.config/docwatch/config.toml --no-browser
=== reflog ===
f590d884 HEAD@{0}: commit: DOCS — CONTINUITÉ 1 134 MOTS, ORGANISATION 1 579 : T0 3 989
b33b56ab HEAD@{1}: commit: LA CARTE DE DÉCISION DES CHANTIERS — LA PROFONDEUR DE DÉPENDANCE COMME AXE, LES SOURCES NOMMÉES
21a361f9 HEAD@{2}: commit: R13.4 — DEUX GRAINES : BPE512 DANS LE BRUIT, BPE1024 PERD 4,09 %
842e1770 HEAD@{3}: commit: SESSIONS — LES TROIS PLANS CONFIRMÉS : PÉRIMÈTRES, FICHIERS, HEARTBEAT 13:05
68590bf0 HEAD@{4}: commit: LE GRAPHE CONFRONTE L'INDEX, L'ÉTAT POINTE LA FRONTIÈRE — SIX STATUTS DIVERGENTS CORRIGÉS
277103ff HEAD@{5}: commit: A8.3d — LE LOT N'EST PAS LES THREADS : L'ÉCART DE 1,90 % SURVIT À 1 THREAD
ac60b79a HEAD@{6}: commit: ÉTAT — WBS 13:00, B11.10 4/4
10a05c30 HEAD@{7}: commit: SESSIONS — MIGRATION DOUCE : 3 PLANS À CONFIRMER, STRICT ROUGE, EN-COURS RECALÉ
  ```

- **bash** `{"command": "git status --porcelain=v2 | head -30; echo \"=== docwatch submodule ===\"; git -C tools/docwatch status --short | head -20; git -C tools/docwatch log --oneline -3", "description": "Detailed status and docwatch submodule state"}`

  ```
1 MM N... 100644 100644 100644 7c67f453bf473856dfcc9dbce45e8052cf4e4550 6509345123ed5832f75b387fc69dad89b0db4099 journal/2026-10-29/README.md
1 D. N... 100644 000000 000000 50bd9d35d9833a19f98e276722f69e6e8bf63e2b 0000000000000000000000000000000000000000 journal/2026-10-29/attention.md
1 MM N... 100644 100644 100644 ace81e7fe9c27318f4342186239534a2a2cc560a 1ade158d118554c37bdf7f7d04981f4a7de17b43 journal/2026-10-29/distribue.md
1 MM N... 100644 100644 100644 cad68264240c5685659b4205760ea53358f2afda 914ed13bc899e2fd6003f77fc646d3bf77520bbc journal/2026-10-29/docs.md
1 MM N... 100644 100644 100644 6125835b8ae268f3122911e793adac83476fdd3c 7a881f1efa18d7da9bc6b4634e3318fb6dd19ed1 journal/2026-10-29/memoire.md
1 MM N... 100644 100644 100644 6a0a61aa999ac2763c3e5d33eba7cfcf237306f8 306b1eef94e62a4b2067b71306cba36bd2c37b5a journal/2026-10-29/mesures.md
1 MM N... 100644 100644 100644 d09a82c4078b4527474d5a141d1f2bf49806f667 e99e8e9a558b9604e4f173583c70c055d22ece5e journal/2026-10-29/modele.md
1 MM N... 100644 100644 100644 b0ed7e0056b385b0ae0933f1c27e422d5c958ce5 1508efba6c425564398888cfcb4ada13b9d663ff journal/2026-10-29/moteur.md
1 MM N... 100644 100644 100644 ecd1fe9f0385a4cf63a916f6d0a
… [2683 caractères tronqués]
  ```

- **bash** `{"command": "git log -1 --format='%ci %h %s'; echo \"=== journal tools ===\"; ls tools/ | grep -i -E \"journal|commit|index\" ; echo \"=== hooks ===\"; ls .git/hooks/ | grep -v sample", "description": "Check commit time and journal tooling"}`

  ```
2026-10-30 13:35:56 -0400 f590d884 DOCS — CONTINUITÉ 1 134 MOTS, ORGANISATION 1 579 : T0 3 989
=== journal tools ===
index_reports.py
index_spans.py
index_wiki_en.py
journal_auto.py
verifie_journal.py
=== hooks ===
pre-commit
  ```

- **bash** `{"command": "grep -rn \"journal/README\\|THEMES\" tools/*.py tools/*.sh 2>/dev/null | head -20", "description": "Find journal index generator"}`

  ```
tools/journal_auto.py:16:     (début et durée lus dans l'index `journal/README.md`, régénéré par
tools/journal_auto.py:48:THEMES: list[tuple[str, str, list[str], list[str]]] = [
tools/journal_auto.py:97:    for slug, _, mots, chemins in THEMES:
tools/journal_auto.py:100:    for slug, _, _, chemins in THEMES:
tools/journal_auto.py:107:    for s, titre, _, _ in THEMES:
tools/journal_auto.py:139:    """Les sessions dont la fenêtre [début, début+durée] couvre le jour (index journal/README.md)."""
tools/journal_auto.py:389:    connus = {s_[0] for s_ in THEMES} | {THEME_DEFAUT[0]}
tools/journal_auto.py:455:             "> table `THEMES` du script et relancer : rien d'autre n'est à toucher.", "",
tools/journal_auto.py:457:    for slug, titre, mots, chemins in THEMES:
tools/journal_auto.py:464:    tous = [s_ for s_, _, _, _ in THEMES] + [THEME_DEFAUT[0]]
tools/journal_auto.py:477:    ecrire(JOURNAL / "THEMES.md", "\n".join(table), dry, trace)
tools/journal_auto.py:490:        for slug, titre, mots, chemins in THEMES:
tools/session_report.py:8:  journal/README.md                  l'index des sessions
tools/session_report.py:334:        if f.name not in ("README.md", "THEMES.md"):
tools/sess
… [370 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"git\\|rm \\|unlink\\|index\" tools/journal_auto.py | head -40; echo \"=== head ===\"; sed -n '1,40p' tools/journal_auto.py", "description": "Inspect journal_auto git behaviour"}`

  ```
2:"""journal_auto.py — le journal quotidien, ÉCRIT PAR JOUR (UN DOSSIER) ET PAR THÈME, à partir de git et des sessions.
12:  1. **git** — les commits du jour (heure d'auteur, en heure locale de la machine) et les
16:     (début et durée lus dans l'index `journal/README.md`, régénéré par
113:def git_commits(jour: str) -> list[dict]:
123:        ["git", "log", f"--since={jour} 00:00:00", f"--until={jour} 23:59:59",
139:    """Les sessions dont la fenêtre [début, début+durée] couvre le jour (index journal/README.md)."""
296:    commits = git_commits(jour)
323:            "> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).",
325:            "> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : "
396:            vieux.unlink()
399:    # l'index du jour, DANS le dossier du jour
402:        "> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier",
404:        "> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·",
405:        "> [l'index des sessions](../README.md#sessions).", "",
423:                      f"[l'index des sessions](../README.md#sessions) ; rapport à la fin de la session.")
432:
… [2049 caractères tronqués]
  ```

### 👤 Utilisateur

tu es la seule session active. termine l;es chantiers en cours

### 🤖 Assistant

⏵ Stabilisation du dépôt : état de l'index, hook, puis chantiers restants

- **bash** `{"command": "sed -n '1,80p' .git/hooks/pre-commit", "description": "Read pre-commit hook"}`

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
python3 tools/archive_sessions.py --quiet >/dev/null 2>&1 || true
python3 tools/session_report.py --quiet >/dev/null 2>&1 || true
# Le journal du jour, par thème (sources : git + journal/sessions). L'index README est
# régénéré ensuite pour lister les fichiers produits.
python3 tools/journal_auto.py --q
… [135 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '280,340p' docs/pilotage/roadmap.md", "description": "Read roadmap tail (never-wait queue)"}`

  ```
- **Ce n'est pas « lire à 1 000 mots/minute »** : la revue de Rayner et al. (2016) montre que la vitesse élevée
  avec compréhension pleine n'est pas au rendez-vous ; le levier est l'**allocation**, pas le débit.
- **Ce n'est pas « ajouter des paramètres »** : à 20 000 pas, le student 21,63 M fait **3,381** contre **3,123**
  pour 11,47 M ; la capacité à budget égal donne **−8,1 %**, mais le prior domine. La structure d'abord.
- **Ce n'est pas « la vision avant le texte »** : la plupart des documents sont du texte structuré ; les parseurs
  classiques sont moins chers et mesurables. R4.4 vient après R4.1–R4.3.
- **Ce n'est pas « un résumeur avant un lecteur »** : le décodeur est sous le plancher ; on mesurerait le plancher.

**Les fiches de fonctionnalité** : [`backlog/index.md`](backlog/index.md) — une fiche par fonctionnalité R, avec le
contrat, la porte, les contrôles négatifs et ce qui pourrait la rendre fausse.
**Les termes** : [glossaire, famille 12](../theorie/glossaire/12-la-lecture-le-document-et-ses-mesures.md) — lecture
rapide, graphe de document, gist, mesures et blocs structurels.

---

## La file « jamais en attente »

Quand une ligne est bloquée (corpus, compte, maté
… [2949 caractères tronqués]
  ```

- **bash** `{"command": "git reset -q; git status --short | head -30; echo \"=== diff stat ===\"; git diff --stat | tail -15; echo \"=== untracked count ===\"; git status --porcelain | grep '^??' | wc -l", "description": "Reset index to HEAD and inspect clean status"}`

  ```
m tools/docwatch
?? =
?? reports/r4e-bloc-*.json
?? reports/r4s-bloc-*.json
?? reports/r4x-bloc-*.json
?? tools/r13_anglais.py
=== diff stat ===
 tools/docwatch | 0
 1 file changed, 0 insertions(+), 0 deletions(-)
=== untracked count ===
5
  ```

- **bash** `{"command": "for f in reports/r4e-bloc-*.json reports/r4s-bloc-*.json reports/r4x-bloc-*.json; do echo \"== $f\"; head -c 400 \"$f\"; echo; done", "description": "Inspect untracked bloc JSONs"}`

  ```
== reports/r4e-bloc-*.json
{
 "date": "2026-10-29",
 "ligne": "R4.2",
 "dispositif": {
  "corpus": "tools/*.py",
  "fixtures": "tools/tests/code/",
  "langage": "Python 3 (ast), interpréteur en sable",
  "machine": "CPU, aucun modèle chargé"
 },
 "parseur": {
  "fichiers": 296,
  "acceptes": 296,
  "refuses": [],
  "noeuds": 462429,
  "fonctions": 1786,
  "classes": 76,
  "secondes": 3.296
 },
 "execution": {
  "justes":
== reports/r4s-bloc-*.json
{
 "date": "2026-10-29",
 "ligne": "R4.3",
 "dispositif": {
  "corpus": "tools/tests/maths/formules.json (le dépôt n'a pas de corpus LaTeX)",
  "langage": "sous-ensemble LaTeX",
  "arithmetique": "fractions.Fraction (exacte) ; flottant pour les irrationnels",
  "oracle": "sympy (évaluation, dérivée, solution)",
  "machine": "CPU, aucun modèle chargé"
 },
 "formules": {
  "exactes": 32,
  "s
== reports/r4x-bloc-*.json
{
 "date": "2026-10-29",
 "ligne": "R4.1",
 "dispositif": {
  "corpus_fichiers": 9,
  "corpus_tableaux": 35,
  "corpus_cellules": 996,
  "formats": [
   "csv",
   "html",
   "markdown"
  ],
  "machine": "CPU, aucun modèle chargé"
 },
 "grille": {
  "cellules_markdown_mesurees": 802,
  "provenance_exacte": 802,
  "avec_entete"
… [71 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '210,260p' docs/pilotage/roadmap.md", "description": "Read roadmap R section"}`

  ```
C'est la **priorité** : un lecteur au niveau **système**, avec le moteur existant et un modèle externe, pour
établir la cible avant de la porter dans le natif.

| # | fonctionnalité | état | porte |
|---|---|---|---|
| **R0.1** | **graphe de document** : régions typées (titre, section, paragraphe, tableau, code, maths, figure), offsets, provenance ; parseurs PDF/HTML/DOCX/Markdown ; sans modèle | ✅ **51 pages**, fidélité **1,000** | 50 pages découpées, provenance exacte, rejeu identique |
| **R0.2** | **contrôleur de lecture** : `survol`, `balayage`, `lecture`, `relecture`, `arrêt` ; budget en octets ; classique d'abord (TOC, titres, premières/dernières phrases, BM25/regex) | ✅ **1,000** à 30 % sur **5 types** | à 30 % du budget, **≥ 90 %** de la réponse de la lecture intégrale sur **3 types** |
| **R0.3** | **banc de lecture rapide** : 30 documents, 5 types, 10 questions/spans gold, modes intégral/écrémage/balayage/sélectif, contrôles closed-book, régions aléatoires, sections mélangées | ✅ **249 questions** : extractif **1,000** à 30 % ; modèle **0,231** contre début **0,042**. **Durci** (84 paraphrases) : modèle **0,375**, lexical **0,269** | une courbe vitesse-compréhension par 
… [3871 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"R4\\.\\|R13\" docs/pilotage/roadmap.md | sed -n '1,60p'", "description": "Grep R4/R13 roadmap rows"}`

  ```
33:| **R — le lecteur** | document, politique de lecture, fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; R0.4 **pilote négatif** ; **R4.1–R4.3 mesurées** | **R0.4** — négatifs difficiles ; **R4.4 bloqué** (OCR) |
42:   **R4.1 — le bloc tableaux** est **mesurée** (996 cellules, **802** exactes, texte plat **0/3**),
43:   **R4.2 — le bloc code** aussi (294 fichiers, 24/24 extraits, texte seul **0/3**) et **R4.3 —
44:   le bloc maths** (32 formules, 10/10 dérivées, surface **0/3**) ; **R4.4 est bloqué** (OCR).
53:7. **N3, R13** — les autonomes restants, qui remplissent la file « jamais en attente ».
79:[R4.1–R4.3] lasts 1 day and is 100% complete and is colored in #2e7d32
81:[R4.4] lasts 1 day and is colored in #b03a2e
94:[R4.1–R4.3] starts at [R0.1–R0.3]'s end
96:[R4.4] starts at [R4.1–R4.3]'s end
169:| **N5** | l'échelle : 50–100 M, corpus élargi | ⏸ **gelé** | après le verdict de **R11** sur le contexte ; BPE si R13 le justifie |
263:| **R4.1** | **tableaux** : parseur 2D, en-têtes, cellules, opérations classiques (filtre, jointure, agrégat) | ✅ **996 cellules**, **802** exactes, texte plat **0/3** | extraction exacte sur 100 cellules ; contrôle : texte plat |
264:| **R4
… [890 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"r4e-bloc\\|r4s-bloc\\|r4x-bloc\\|r13_anglais\" --include=*.md --include=*.py --include=*.sh --include=*.json . 2>/dev/null | grep -v \"^./reports/r4\" | head -20", "description": "Find references to untracked evidence files"}`

  ```
./tools/r13_anglais.py:2:"""r13_anglais.py — R13.3/R13.4 : le BPE perd-il à octets égaux, sur l'anglais ?
./tools/r13_anglais.py:17:  python3 tools/r13_anglais.py --graine 2 --sortie reports/r13.4-anglais.json
./tools/r13_anglais.py:18:  python3 tools/r13_anglais.py --graine 2 --pas-bytes 20 --pas-512 10 --pas-1024 8   # pipeline
./tools/r13_anglais.py:134:        "dispositif": "tools/r13_anglais.py",
  ```

- **bash** `{"command": "grep -rn \"reports/r4\\|r4e-bloc\\|r4s-bloc\\|r4x-bloc\" tools/bloc_*.py tools/porte-bloc-*.sh 2>/dev/null | head -20", "description": "Check bloc scripts output naming"}`

  ```
tools/bloc_code.py:26:  python3 tools/bloc_code.py --mesure reports/r42-bloc-code.json
tools/bloc_maths.py:27:  python3 tools/bloc_maths.py --mesure reports/r43-bloc-maths.json
tools/bloc_tableaux.py:27:  python3 tools/bloc_tableaux.py --mesure reports/r41-bloc-tableaux.json
  ```

- **bash** `{"command": "ls checks 2>/dev/null; ls reports | grep -E \"^r4|bloc\" | head -20; echo \"=== reports INDEX r4e ===\"; grep -n \"r4e\\|r4s\\|r4x\" reports/INDEX.md reports/README.md 2>/dev/null | head", "description": "List R4 reports and index mentions"}`

  ```
kv-cache-int8-bloc.json
r41-bloc-tableaux.json
r42-bloc-code.json
r43-bloc-maths.json
r4e-bloc-*.json
r4s-bloc-*.json
r4x-bloc-*.json
rapport-kv-cache-int8-bloc.md
rapport-miroir-blocs.md
rapport-r41-bloc-tableaux.md
rapport-r42-bloc-code.md
rapport-r43-bloc-maths.md
=== reports INDEX r4e ===
  ```

- **bash** `{"command": "ls -b reports/ | grep -E \"r4[e-sx]-bloc\"; echo \"=== compare ===\"; for pair in \"r4x r41-bloc-tableaux\" \"r4e r42-bloc-code\" \"r4s r43-bloc-maths\"; do set -- $pair; echo \"-- $1 vs $2\"; diff <(sed 's/\"date\": \"[^\"]*\"/\"date\": \"X\"/' \"reports/$1-bloc-*.json\") <(sed 's/\"da … [171 caractères tronqués]`

  ```
r4e-bloc-*.json
r4s-bloc-*.json
r4x-bloc-*.json
=== compare ===
-- r4x vs r41-bloc-tableaux
differ
-- r4e vs r42-bloc-code
differ
-- r4s vs r43-bloc-maths
differ
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nfor f in [\"reports/r4x-bloc-*.json\",\"reports/r4e-bloc-*.json\",\"reports/r4s-bloc-*.json\",\"reports/r41-bloc-tableaux.json\",\"reports/r42-bloc-code.json\",\"reports/r43-bloc-maths.json\"]:\n    d=json.load(open(f))\n    print(f, \"->\", list(d.keys() … [55 caractères tronqués]`

  ```
reports/r4x-bloc-*.json -> ['date', 'ligne', 'dispositif', 'grille', 'operations', 'controles', 'fusions', 'sans_entete', 'refus_fixtures', 'cout', 'miroir', 'rejeu']
reports/r4e-bloc-*.json -> ['date', 'ligne', 'dispositif', 'parseur', 'execution', 'portee_et_flux', 'controles', 'refus', 'cout', 'miroir', 'rejeu']
reports/r4s-bloc-*.json -> ['date', 'ligne', 'dispositif', 'formules', 'derivees', 'equations', 'controles', 'refus', 'cout', 'miroir', 'rejeu']
reports/r41-bloc-tableaux.json -> ['date', 'ligne', 'dispositif', 'grille', 'operations', 'controles', 'fusions', 'sans_entete', 'refus_fixtures', 'cout', 'miroir', 'rejeu']
reports/r42-bloc-code.json -> ['date', 'ligne', 'dispositif', 'parseur', 'execution', 'portee_et_flux', 'controles', 'refus', 'cout', 'miroir', 'rejeu']
reports/r43-bloc-maths.json -> ['date', 'ligne', 'dispositif', 'formules', 'derivees', 'equations', 'controles', 'refus', 'cout', 'miroir', 'rejeu']
  ```

- **bash** `{"command": "diff <(python3 -m json.tool \"reports/r4x-bloc-*.json\") <(python3 -m json.tool reports/r41-bloc-tableaux.json) | head -20; echo \"=== dates ===\"; python3 - <<'EOF'\nimport json\nfor f in [\"reports/r4x-bloc-*.json\",\"reports/r41-bloc-tableaux.json\",\"reports/r4e-bloc-*.json\",\"repo … [123 caractères tronqués]`

  ```
68,70c68,70
<         "secondes_corpus": 0.0385,
<         "millisecondes_par_1000_cellules": 38.6,
<         "ratio_x4": 4.92
---
>         "secondes_corpus": 0.0499,
>         "millisecondes_par_1000_cellules": 50.1,
>         "ratio_x4": 3.55
=== dates ===
reports/r4x-bloc-*.json 2026-10-29
reports/r41-bloc-tableaux.json 2026-10-29
reports/r4e-bloc-*.json 2026-10-29
reports/r42-bloc-code.json 2026-10-29
  ```

- **bash** `{"command": "ls reports/ | grep -iE \"^r0[45]|^r13|^r41|^r42|^r43|r13\" | sort; echo \"=== r13.4 fiche ===\"; sed -n '1,60p' reports/rapport-r13.4-graines.md", "description": "List R0/R13 fiches and read R13.4"}`

  ```
r04-tete-survol.json
r04-tete-survol-v2.json
r04-tete-survol-v3.json
r04-tete-survol-v4.json
r05-balayage.json
r13.1-bpe.json
r13.1-campagne.json
r13.1-condition.json
r13.2-vocab1024.json
r13.3-anglais.json
r13.4-graines.json
r13-tokenisation.json
r41-bloc-tableaux.json
r42-bloc-code.json
r43-bloc-maths.json
rapport-r13.1-bpe.md
rapport-r13.1-campagne.md
rapport-r13.1-condition.md
rapport-r13.2-vocab1024.md
rapport-r13.3-anglais.md
rapport-r13.4-graines.md
rapport-r13-tokenisation.md
=== r13.4 fiche ===
# R13.4 — deux graines : le BPE 512 est dans le bruit, le 1024 perd

> **Ligne de roadmap** : R13.4 · **Date** : 2026-10-30 · **Verdict** : ⛔ **pas de gain à octets
> égaux** — sur deux graines, BPE 512 est à **+0,39 %** (dans le bruit : +0,67 % puis +0,10 %)
> et BPE 1024 à **+4,09 %** contre bytes. Le signe négatif est stable ; l’ampleur du 512 ne l’est pas.
>
> **Dispositif** : mêmes ids/val/architecture que R13.1c, graines 1 et 2 ; bytes 10 k, BPE 512 5 k,
> BPE 1024 4 k ; données [`r13.4-graines.json`](r13.4-graines.json).

## Ce qui est mesuré

| modèle | graine 1 | graine 2 | moyenne | écart moyen |
|---|---:|---:|---:|---:|
| bytes | 1,8021 | 1,7982 | **1,8001** | — |
| BPE 
… [1336 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"R13\" docs/pilotage/backlog/index.md | head -20; echo \"=== backlog R0.4/R0.5 ===\"; grep -n \"R0\\.4\\|R0\\.5\" docs/pilotage/backlog/index.md | head -20", "description": "Check backlog entries for R13/R0.4/R0.5"}`

  ```
59:| R13 | [Tokenisation : octets ou BPE](R13-tokenisation-bpe.md) | prête | P2 | — | R1.3 |
=== backlog R0.4/R0.5 ===
53:| R04 | [Tête de survol](R04-tete-survol.md) | partiel | P1 | R03, R01 | R0.4 |
54:| R05 | [Tête de balayage](R05-tete-balayage.md) | partiel | P1 | R03, R01 | R0.4 |
55:| R06 | [Tête de relecture](R06-tete-relecture.md) | partiel | P2 | R03, R21, R22 | R0.4 |
56:| R07 | [Routeur extractif / génératif](R07-routeur-extractif-generatif.md) | partiel | P1 | R02, R03 | R0.5 |
  ```

- **bash** `{"command": "git ls-files reports/ | grep -E \"r04|r05|r13\" | sort; echo \"=== v4 mtime ===\"; ls -l reports/r04-tete-survol-v4.json reports/r04-tete-survol-v3.json 2>/dev/null; echo \"=== v4 content ===\"; head -c 1200 reports/r04-tete-survol-v4.json", "description": "Check tracked R0.4 files and  … [12 caractères tronqués]`

  ```
reports/r04-tete-survol.json
reports/r04-tete-survol-v2.json
reports/r04-tete-survol-v3.json
reports/r04-tete-survol-v4.json
reports/r05-balayage.json
reports/r13.1-bpe.json
reports/r13.1-campagne.json
reports/r13.1-condition.json
reports/r13.2-vocab1024.json
reports/r13.3-anglais.json
reports/r13.4-graines.json
reports/r13-tokenisation.json
reports/rapport-r04-tete-survol.md
reports/rapport-r05-balayage.md
reports/rapport-r13.1-bpe.md
reports/rapport-r13.1-campagne.md
reports/rapport-r13.1-condition.md
reports/rapport-r13.2-vocab1024.md
reports/rapport-r13.3-anglais.md
reports/rapport-r13.4-graines.md
reports/rapport-r13-tokenisation.md
=== v4 mtime ===
-rw-r--r--. 1 stephane stephane 5271 29 oct 16:19 reports/r04-tete-survol-v3.json
-rw-r--r--. 1 stephane stephane 5878 29 oct 17:26 reports/r04-tete-survol-v4.json
=== v4 content ===
{
 "date": "2026-10-29",
 "ligne": "R0.4",
 "paires": 498,
 "positifs": 83,
 "couches": "8:11",
 "negatifs": "durs (même section)",
 "modele": "Qwen2.5-0.5B-Q8_0",
 "partage": "leave-one-document-out",
 "resultats": [
  {
   "document": "tools/tests/documents/corpus/code/configuration-nvme-raid-amd.md",
   "type": "code",
   "n_test": 18,
   "auc_tete"
… [842 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' journal/sessions/MANIFEST.md", "description": "Read sessions manifest"}`

  ```
# Sessions DSH archivées

Régénéré par `tools/archive_sessions.py`. Le digest est versionnable ; la
trace brute (`session.jsonl.zstd`) reste sur disque et n'est pas suivie par git.

| Session | Début | Trace | Digest | Tours | Messages | Outils | Erreurs | Compactages |
|---|---|---|---|---|---|---|---|---|
| `04ed1834` | 2026-10-08 09:21 | 0.3 Mo | 67 Ko | 1 | 27 | 42 | 0 | 0 |
| `11b2d312` | 2026-10-01 02:56 | 0.5 Mo | 82 Ko | 1 | 42 | 60 | 0 | 0 |
| `13446299` | 2026-10-01 01:07 | 0.5 Mo | 84 Ko | 1 | 50 | 68 | 0 | 0 |
| `15fd322f` | 2026-09-30 12:00 | 0.6 Mo | 66 Ko | 1 | 57 | 67 | 0 | 0 |
| `1820cf6b` | 2026-10-02 19:36 | 0.3 Mo | 30 Ko | 1 | 23 | 21 | 0 | 0 |
| `18b8879c` | 2026-10-02 15:12 | 0.4 Mo | 78 Ko | 1 | 33 | 55 | 3 | 0 |
| `18c3f6d0` | 2026-10-01 05:26 | 0.3 Mo | 51 Ko | 1 | 26 | 38 | 0 | 0 |
| `1966e052` | 2026-10-08 09:20 | 0.3 Mo | 57 Ko | 1 | 22 | 33 | 0 | 0 |
| `22bcae27` | 2026-09-28 14:45 | 14.8 Mo | 1398 Ko | 54 | 1250 | 1227 | 19 | 4 |
| `27c99b10` | 2026-09-25 19:50 | 1.0 Mo | 61 Ko | 1 | 57 | 54 | 1 | 0 |
| `2c2a6595` | 2026-10-02 15:11 | 0.4 Mo | 66 Ko | 1 | 29 | 44 | 0 | 0 |
| `31f26a6e` | 2026-10-02 19:48 | 0.9 Mo | 171 Ko | 1 | 85 | 111 | 0 | 0 |
| `3
… [3588 caractères tronqués]
  ```

- **bash** `{"command": "nvidia-smi --query-gpu=index,name,memory.used,memory.total,utilization.gpu --format=csv 2>/dev/null | head; echo \"=== latest checkpoints ===\"; ls -lt reports/*.log 2>/dev/null | head -5; ps aux | grep -E \"distill|train|python3 tools/n\" | grep -v grep | head", "description": "Check G … [27 caractères tronqués]`

  ```
index, name, memory.used [MiB], memory.total [MiB], utilization.gpu [%]
0, Quadro RTX 5000, 1 MiB, 16384 MiB, 0 %
1, Quadro RTX 5000, 1 MiB, 16384 MiB, 0 %
=== latest checkpoints ===
  ```

- **bash** `{"command": "for d in journal/sessions/8156fdcb journal/sessions/c3d0f0bd journal/sessions/N2-GPU; do echo \"===== $d\"; ls \"$d\"; for f in \"$d\"/*; do echo \"--- $f\"; sed -n '1,50p' \"$f\"; done; done 2>/dev/null | head -160", "description": "Read session plans"}`

  ```
===== journal/sessions/8156fdcb
plan.md
--- journal/sessions/8156fdcb/plan.md
# Plan de session — 8156fdcb

> **Mandat confirmé** le 2026-10-30 13:05 depuis `en-cours` — le heartbeat est celui de
> l'état ; la session le met à jour à chaque cycle.

- **Session** : `8156fdcb`
- **Rôle** : R0.1–R0.5 (lecteur)
- **Périmètre** : R0.1–R0.5
- **Fichiers réservés** : `tools/lecteur_modele.py`, `tools/routeur.py`, `reports/r03-*`, `reports/r07-*`
- **Heartbeat** : 2026-10-30 13:05 HAE
- **Prochaine action** : la boucle de lecture (R11, dépend de N2) ou la restitution (R31, dépend de R21) — toutes deux hors R0 ; sinon consolidation.
- **État** : actif
===== journal/sessions/c3d0f0bd
plan.md
--- journal/sessions/c3d0f0bd/plan.md
# Plan de session — c3d0f0bd

> **Mandat confirmé** le 2026-10-30 13:05 depuis `en-cours` — le heartbeat est celui de
> l'état ; la session le met à jour à chaque cycle.

- **Session** : `c3d0f0bd`
- **Rôle** : R4, B10.2bis, A8.3b
- **Périmètre** : R4.1–R4.3, B10.2bis, A8.3b
- **Fichiers réservés** : `tools/bloc_*.py`, `tools/porte-bloc-*.sh`, `tools/tests/tableaux/`, `tools/tests/code/`, `tools/tests/maths/`, `reports/r4*`, `docs/implantation/bloc-*.md`
- **Heartbea
… [713 caractères tronqués]
  ```

- **bash** `{"command": "ls reports/ | grep -iE \"routeur|r05|r07|r04\" ; echo \"=== routeur tool ===\"; ls -l tools/routeur.py tools/lecteur_modele.py 2>/dev/null; echo \"=== r0.5 json ===\"; ls -l reports/*routeur* 2>/dev/null", "description": "Locate router artifacts"}`

  ```
r04-tete-survol.json
r04-tete-survol-v2.json
r04-tete-survol-v3.json
r04-tete-survol-v4.json
r05-balayage.json
r07-routeur.json
rapport-r04-tete-survol.md
rapport-r05-balayage.md
rapport-r07-routeur.md
rapport-routeur-confiance.md
rapport-routeur-m1-m2.md
routeur-confiance.json
routeur-m1-m2.json
=== routeur tool ===
-rwxr-xr-x. 1 stephane stephane 6023 29 oct 14:14 tools/lecteur_modele.py
-rwxr-xr-x. 1 stephane stephane 9363 29 oct 15:25 tools/routeur.py
=== r0.5 json ===
-rw-r--r--. 1 stephane stephane 115862 29 oct 15:59 reports/r07-routeur.json
-rw-------. 1 stephane stephane   7724 29 oct 16:19 reports/rapport-r07-routeur.md
-rw-r--r--. 1 stephane stephane   2160 28 oct 09:17 reports/rapport-routeur-confiance.md
-rw-r--r--. 1 stephane stephane   1962 28 oct 09:17 reports/rapport-routeur-m1-m2.md
-rw-r--r--. 1 stephane stephane    775 27 oct 19:06 reports/routeur-confiance.json
-rw-r--r--. 1 stephane stephane   2842 27 oct 16:15 reports/routeur-m1-m2.json
  ```

- **bash** `{"command": "grep -rn \"routeur\\|R0\\.5\" reports/rapport-*.md | head -20", "description": "Find router report text"}`

  ```
reports/rapport-a80-porte-profondeur.md:32:- **L’oracle par jeton** est une analyse hors-ligne, pas un routeur réel.
reports/rapport-a83c-lot.md:39:bits changent, et « un routeur au voisinage d'une égalité peut choisir un autre expert ».
reports/rapport-a83c-lot.md:54:  non-équivalence (routeur à l'égalité, sommes réordonnées) ou l'assumer dans les références.
reports/rapport-a83c-lot.md:61:  coupe et du routeur ; il peut être plus petit ailleurs (0,15 % sur le 30B).
reports/rapport-a83d-lot-threads.md:39:pas celles du pool de threads. Sur ce modèle **dense**, le routeur ne peut pas être la cause (il n'y
reports/rapport-architecture-memoire.md:293:Le routeur connaît ses `k` experts **avant** de les calculer : on peut donc
reports/rapport-c9-echange-experts.md:24:remplace la sélection du routeur, en gardant les **poids du modèle** pour les experts imposés
reports/rapport-c9-echange-experts.md:25:(c'est « et si le routeur avait choisi ceux-là ? », pas « et si on avait pris d'autres poids ? »).
reports/rapport-cache-experts-vram.md:86:2. **prélecture par le routeur de la couche suivante** — non mesuré. Recouvrir
reports/rapport-cache-experts-vram.md:87:   la latence disque a du sens q
… [1614 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,90p' reports/rapport-r07-routeur.md", "description": "Read router report"}`

  ```
# R0.5 — le routeur : le signal prédit (0,826), la règle ne transfère pas

> **Ligne de roadmap** : R0.5 · **Date** : 2026-10-29 · **Verdict** : ⚠️ **partiel** — le signal
> BM25 **prédit** quel lecteur gagne (AUC **0,785**, contrôles à 0,41), mais un **seuil
> absolu ne transfère pas** d'un banc à l'autre (0,496 et 0,421, contre 0,855 et 0,737 pour le
> choix fixe). Le routeur n'est **pas déployé**.
>
> **Dispositif** : ré-analyse des mesures de R0.3 — 267 questions (248 lexicales, 19
> paraphrases), deux lecteurs, quatre JSON ; deux signaux (max BM25, couverture question ↔
> document) ; transfert par leave-one-bench-out ; JSON brut
> [`r07-routeur.json`](r07-routeur.json).

## La question

Deux régimes mesurés : le **lexical** gagne sur les questions qui partagent les mots du document
(0,72–1,00 contre 0,23), le **modèle** gagne sur les paraphrases (0,717 contre 0,30). Un seul
lecteur perd la moitié des cas. Le routeur doit choisir — la seule question qui compte est :
**le signal prédit-il quel lecteur va gagner, et la règle tient-elle d'un banc à l'autre ?**

## Le dispositif

- **267 questions** : 248 du banc complet (lexicales) + 19 du banc durci (paraphrases) ;
- **deux lecte
… [3691 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,80p' reports/rapport-r04-tete-survol.md", "description": "Read survol report"}`

  ```
# R0.4 — la tête de survol perd contre BM25 (0,601 contre 0,836), et gagne sur le juridique

> **Ligne de roadmap** : R0.4 · **Date** : 2026-10-29 · **Verdict** : ❌ **la tête ne bat jamais le
> scoreur classique** — v1 0,601 contre 0,836 ; v2 0,448 contre 0,811 ; **v3 (498 paires) 0,575
> contre 0,745**. La donnée paie (+13 points), mais une sonde linéaire ne rattrape pas BM25. ✅ le contrôle des étiquettes mélangées (**0,467**) montre que le
> signal est réel mais faible, pas une fuite.
>
> **Dispositif** : 114 paires (question, passage) — 19 questions du banc durci × (1 gold +
> 5 négatifs du même document) ; **états précoces** après les 4 premières couches de
> Qwen2.5-0.5B (896 valeurs, capturés par le moteur) ; tête logistique ridge ; partage
> **leave-one-document-out** ; JSON bruts [`r04-tete-survol.json`](r04-tete-survol.json) et
> [`r04-tete-survol-v2.json`](r04-tete-survol-v2.json) (version 2 : couches 8–11, négatifs durs).

## La question

Le contrôleur de R0.2 décide avec BM25 : il partage le scoreur du lecteur extractif et ne sait
pas ce qu'est une paraphrase. R0.4 demande une **tête apprise** : lire la question et le début
d'un passage, et prédire s'il vaut la peine d'
… [3419 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/r07-routeur.json'))\ndef walk(o,p=\"\"):\n    if isinstance(o,dict):\n        for k,v in o.items():\n            walk(v,p+\"/\"+k)\n    elif isinstance(o,list):\n        print(p,\"[list len\",len(o),\"]\")\n    else:\n        pri … [74 caractères tronqués]`

  ```
/date = 2026-10-29
/ligne = R0.5
/questions = 332
/differes = 201
/auc_signal = 0.826
/auc_longueur = 0.438
/auc_aleatoire = 0.409
/fixe_extractif = 0.708
/fixe_modele = 0.271
/oracle = 0.792
/transferts [list len 2 ]
/lignes [list len 332 ]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/r07-routeur.json'))\nprint(json.dumps(d['transferts'],indent=1,ensure_ascii=False)[:2000])\nprint(\"lignes[0]:\", json.dumps(d['lignes'][0],ensure_ascii=False))\nEOF", "description": "Inspect router transfers"}`

  ```
[
 {
  "banc_test": "lexical",
  "n": 248,
  "signaux": {
   "z": {
    "seuil": 4.614,
    "exactitude": 0.802
   },
   "ratio": {
    "seuil": 24.761,
    "exactitude": 0.69
   },
   "etendue": {
    "seuil": 0.174,
    "exactitude": 0.234
   },
   "couverture": {
    "seuil": 0.667,
    "exactitude": 0.488
   },
   "signal": {
    "seuil": 7.921,
    "exactitude": 0.524
   }
  },
  "fixe_extractif": 0.855,
  "fixe_modele": 0.234,
  "oracle": 0.899
 },
 {
  "banc_test": "paraphrase",
  "n": 84,
  "signaux": {
   "z": {
    "seuil": 3.125,
    "exactitude": 0.321
   },
   "ratio": {
    "seuil": 8.029,
    "exactitude": 0.321
   },
   "etendue": {
    "seuil": 0.005,
    "exactitude": 0.298
   },
   "couverture": {
    "seuil": 0.2,
    "exactitude": 0.31
   },
   "signal": {
    "seuil": 3.853,
    "exactitude": 0.31
   }
  },
  "fixe_extractif": 0.274,
  "fixe_modele": 0.381,
  "oracle": 0.476
 }
]
lignes[0]: {"banc": "lexical", "document": "docs/theorie/vision.md", "question": "Quelle valeur le document associe-t-il à « activations » et « couche » ?", "type": "prose", "signal": 6.204, "z": 6.011, "ratio": 29.193, "etendue": 0.046, "couverture": 0.6, "extractif": 1, "modele": 0,
… [15 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/r04-tete-survol-v4.json'))\nfor k,v in d.items():\n    if k!='resultats': print(k,\"=\",v if not isinstance(v,(dict,list)) else \"...\")\nprint(\"n resultats\", len(d.get('resultats',[])))\nprint(json.dumps(d.get('resultats'),ind … [60 caractères tronqués]`

  ```
date = 2026-10-29
ligne = R0.4
paires = 498
positifs = 83
couches = 8:11
negatifs = durs (même section)
modele = Qwen2.5-0.5B-Q8_0
partage = leave-one-document-out
moyennes = ...
n resultats 28
[
 {
  "document": "tools/tests/documents/corpus/code/configuration-nvme-raid-amd.md",
  "type": "code",
  "n_test": 18,
  "auc_tete": 0.533,
  "auc_bm25": 0.644,
  "auc_etiquettes_melangees": 0.356
 },
 {
  "document": "tools/tests/documents/corpus/code/format-clusters.md",
  "type": "code",
  "n_test": 18,
  "auc_tete": 0.778,
  "auc_bm25": 0.767,
  "auc_etiquettes_melangees": 0.689
 },
 {
  "document": "tools/tests/documents/corpus/code/numa-segregation.md",
  "type": "code",
  "n_test": 12,
  "auc_tete": 0.5,
  "auc_bm25": 0.9,
  "auc_etiquettes_melangees": 0.6
 },
 {
  "document": "tools/tests/documents/corpus/code/portes.md",
  "type": "code",
  "n_test": 36,
  "auc_tete": 0.589,
  "auc_bm25": 0.875,
  "auc_etiquettes_melangees": 0.394
 },
 {
  "document": "tools/tests/documents/corpus/code/utilisation.md",
  "type": "code",
  "n_test": 24,
  "auc_tete": 0.812,
  "auc_bm25": 0.625,
  "auc_etiquettes_melangees": 0.263
 },
 {
  "document": "tools/tests/documents/corpus/juridique/A_RES_80
… [494 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '80,200p' reports/rapport-r04-tete-survol.md", "description": "Read rest of R0.4 fiche"}`

  ```
0,556 est du bruit d'échantillon, pas une fuite.

**Pourquoi c'est pire, et pourquoi c'est utile** : les négatifs faciles de la version 1
aidaient BM25 (0,836) *et* la tête (0,601) ; les négatifs durs retirent cette béquille, et la
tête — 90 paires pour 896 dimensions — s'effondre. Les états plus profonds n'y changent rien :
le problème n'est pas la couche, c'est le **nombre de paires**.

**Conclusion des deux versions** : une **sonde linéaire** sur les états d'un 0,5 B, avec 114
paires, ne bat pas BM25. Ce n'est pas « R0.4 est impossible » — c'est « R0.4 demande des
**centaines ou des milliers** de paires, et sans doute un encodeur **ajusté**, pas une sonde ».
La victoire juridique de la version 1 était du bruit : la version 2 la retourne (0,400 contre
0,600).

## La version 3 (498 paires, 84 questions) : la donnée paie, mais ne suffit pas

Avec le banc élargi (84 questions × 6 paires = 504, 498 après écart d'un gold déplacé), la tête
dispose de **~450 paires d'entraînement par pli** au lieu de 90. Mêmes états (couches 8–11),
mêmes négatifs durs.

| type | AUC tête | AUC BM25 | mélangé |
|---|---:|---:|---:|
| prose | 0,684 | 0,882 | 0,603 |
| tableau | 0,605 | 0,728 | 0,505 |
| t
… [2274 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/r04-tete-survol-v4.json'))\nprint(json.dumps(d['moyennes'],indent=1)[:1200])\nEOF", "description": "Inspect v4 averages"}`

  ```
{
 "tete": 0.54,
 "bm25": 0.72,
 "etiquettes_melangees": 0.528
}
  ```

- **bash** `{"command": "grep -rn \"survol-v4\\|v4\\b\" reports/rapport-r04-tete-survol.md reports/rapport-r05-balayage.md docs/pilotage/*.md docs/pilotage/backlog/*.md 2>/dev/null | head -20; echo \"=== balayage ===\"; sed -n '1,60p' reports/rapport-r05-balayage.md", "description": "Check v4 references and bal … [14 caractères tronqués]`

  ```
docs/pilotage/programme-r.md:24:| ~~déclencheur de la cascade~~ | **levé** (R06 v4/v5) : cascade à confiance **calibrée** = oracle (0,911 / 0,415) avec **~50 golds** | il fallait **calibrer par corpus**, pas transférer un seuil — **publié** (R06 v6 : fichier daté, `--calibration`) |
docs/pilotage/backlog/R06-tete-relecture.md:4:> **Ligne de roadmap** : R0.4 · **Résultat** : [rapport-r06-relecture.md](../../../reports/rapport-r06-relecture.md) (triple négatif : relire plus ne change rien, 0/249) ; **v2** [rapport-r06-cascade.md](../../../reports/rapport-r06-cascade.md) — la **cascade** span → extractif → modèle : **0,325** contre 0,313 sur les paraphrases, 0,976 sur le lexical, 0,450 au pilote ; +1,2 point pour 9 appels. **v3** [rapport-r06-declencheur.md](../../../reports/rapport-r06-declencheur.md) : signaux sans échelle (couverture 0,906, accord 0,848) ; **v4** [rapport-r06-cascade-confiance.md](../../../reports/rapport-r06-cascade-confiance.md) : **cascade à confiance calibrée = oracle hors échantillon** (0,911 / 0,415). Le verrou est levé. **v5** [rapport-r06-calibration.md](../../../reports/rapport-r06-calibration.md) : **~50 golds** suffisent pour calibrer (0,906 à k=49), les
… [3208 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '120,210p' docs/pilotage/roadmap.md", "description": "Read N section of roadmap"}`

  ```
| **A6** | apprendre des flux : capteur hebbien, routage MoE, élagage | ✅ / ⏳ | **A6.2 bloqué** (pas de MoE local) ; A6.1/A6.3 ont rendu leurs négatifs |
| **A7** | la grappe déportée : relais, grappe intra-couche, format sparse | ✅ | la suite (WAN) est **hors plan** |
| **A8** | l'ordonnanceur place **et** perte : `choisir_avec_perte` | ✅ **opt-in** ; 6 portes épinglées, A8.3 **échoue** (−5,9 % … +19,5 %) | **A8.3c/d** : le lot change la PPL, pas les threads ; réduire le lot ou l'assumer |

**Ce qui compte pour R** : le moteur sait déjà exécuter un modèle externe (Qwen 0,5 B à 12 288 jetons), tracer,
rejouer et payer le calcul au prorata de l'activité. C'est le support de R0.

---

## Programme B — L'intelligence (les deux étages)

L'étage 1 (langue) est mesuré ; l'étage 2 (pensée) est mesuré dans ses opérations, avec des négatifs nommés.
La ligne ouverte est **B10.3** (décodeur) ; **B12.10** et **B10.2bis** sont **closes** (négatif) ; **B1.5** est bloquée par le corpus.

| # | chantier | état | prochaine action |
|---|---|---|---|
| **B1** | l'entrée-sortie linguistique : juge, chrF, registres, 24 langues, dialogue | ✅ | **B1.5 bloquée** (aucun corpus parallèle humain d'articles)
… [6594 caractères tronqués]
  ```

- **bash** `{"command": "ls reports/ | grep -iE \"^n2|rapport-n2|hierarch\" | sort | head -30; echo \"=== N2 tools ===\"; ls tools/ | grep -iE \"distill|natif|n2|hierarch\" | head -20", "description": "List N2 artifacts"}`

  ```
=== N2 tools ===
corpus_natif.py
distiller_natif.py
generer_natif.py
serveur_natif.py
sft_natif.py
  ```

- **bash** `{"command": "sed -n '1,120p' journal/2026-10-30/README.md", "description": "Read today's journal index"}`

  ```
# 2026-10-30

> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
> [`journal/2026-10-30/`](README.md). Le récit écrit à la main est conservé plus bas, dans
> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
> [l'index des sessions](../README.md#sessions).

**21 commits** · **0 session(s)** · **7 thème(s)**

## Thèmes du jour

| thème | commits | fichier |
|---|---|---|
| distribue | 1 | [distribue.md](distribue.md) |
| docs | 5 | [docs.md](docs.md) |
| memoire | 1 | [memoire.md](memoire.md) |
| mesures | 6 | [mesures.md](mesures.md) |
| modele | 3 | [modele.md](modele.md) |
| moteur | 1 | [moteur.md](moteur.md) |
| portes | 4 | [portes.md](portes.md) |

## Sessions DSH

Aucune session indexée pour ce jour ; voir
[l'index des sessions](../README.md#sessions).

## Tous les commits (heure réelle)

| heure | commit | fait |
|---|---|---|
| 00:04 | `da038e34` | R13.2 + A8.0 — VOCAB 1024 PERD 3,9 % À OCTETS ÉGAUX ; PORTE-INDICE ROUGE QUALIFIÉE |
| 00:06 | `336a2271` | ÉTAT — DATE ALIGNÉE SUR LE COMMIT DU 30 |
| 08:34 | `733232ff` | R06 v5 — LA CALIBRATION COÛTE ~50 GOLDS, LES POIDS APPRIS N'AJOUTENT RIEN, LE PILOTE EST COMPLÉT
… [4791 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,60p' reports/rapport-r13-tokenisation.md; echo \"=== R13 backlog ===\"; sed -n '1,60p' docs/pilotage/backlog/R13-tokenisation-bpe.md", "description": "Read R13 synthesis and backlog"}`

  ```
# R13.0 — BPE : 3,4 à 5,2 octets par jeton, réversible ; la PPL reste à mesurer

> **Ligne de roadmap** : R1.3 / R13 · **Date** : 2026-10-29 · **Verdict** : 🔬 **pré-mesure** —
> le BPE réduit la longueur de **3,4 à 5,2×** sur le latin et reste **réversible** ; le contrôle
> aléatoire tombe à **1,63 octet/jeton**. La **PPL à budget égal** n’est pas mesurée : R13 reste
> **ouverte**.
>
> **Dispositif** : tokenizer Qwen2.5-0.5B (BPE byte-level, 151 936 jetons), `--tokenize` du moteur ;
> échantillons de 200 lignes (anglais, français, multilingue, arabe, cyrillique, CJK) et un
> contrôle aléatoire ; données [`r13-tokenisation.json`](r13-tokenisation.json).

## Ce qui est mesuré

| échantillon | octets | jetons BPE | octets/jeton | jetons/mot | réversible |
|---|---:|---:|---:|---:|---|
| anglais | 47 214 | 9 146 | **5,16** | 1,34 | ✅ |
| français | 14 304 | 4 250 | **3,37** | 1,77 | ✅ |
| multilingue | 12 632 | 3 444 | **3,67** | 1,76 | ✅ |
| arabe | 12 575 | 4 444 | **2,83** | 4,03 | ✅ |
| cyrillique | 16 809 | 6 038 | **2,78** | 5,80 | ✅ |
| CJK | 6 445 | 1 402 | **4,60** | — | ✅ |
| **aléatoire** | 16 804 | 10 321 | **1,63** | 51,6 | ✅ |

- Les octets sont le **plancher** : 1 jeton 
… [4213 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,70p' reports/rapport-r13.1-bpe.md", "description": "Read R13.1 BPE report"}`

  ```
# R13.1 — pilote : le BPE gagne 11,9 % à 200/400 pas (corrigé 11,0 %)

> **Ligne de roadmap** : R13.1 · **Date** : 2026-10-29 · **Verdict pilote** : ✅ **le BPE natif bat
> l’octet** — à budget d’**octets** égal (~405–410 k octets vus), le modèle BPE 512 fait
> **3,249 bits/octet** contre **3,689** pour le modèle octets ; après correction du ratio de validation,
> le chiffre exact est **3,2823** contre **3,689**, soit **−11,0 %**. Le tokenizer
> est **réversible** (1,977 octet/jeton). **Mise à jour 10 k** : à octets égaux, le BPE perd 0,7 % (1,8142 contre 1,8021) ; voir
> [`rapport-r13.1-campagne.md`](rapport-r13.1-campagne.md). Le pilote est conservé comme mesure
> à son budget, pas comme verdict.
>
> **Dispositif** : `tools/tokenizer_bpe.py` + `tools/entrainer_native_tokens.py`, corpus
> `data/corpus_fr.txt`, mêmes architecture/graine/seed ; porte `tools/porte-r13-bpe.sh` ;
> données [`r13.1-bpe.json`](r13.1-bpe.json).

## Ce qui est mesuré

| modèle | vocab | paramètres | PPL/jeton | bits/octet | octets vus |
|---|---:|---:|---:|---:|---:|
| octets, 200 pas | 256 | 11 814 792 | 14,11 | 3,818 | 204 800 |
| octets, 400 pas | 256 | 11 814 792 | 12,90 | **3,689** | 409 600 |
| **BPE,
… [2608 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,50p' reports/rapport-r13.1-condition.md; echo ====; sed -n '1,45p' reports/rapport-r13.2-vocab1024.md", "description": "Read R13.1 condition and R13.2"}`

  ```
# R13.1 — la PPL BPE-native n’est pas mesurable sans un modèle BPE natif

> **Ligne de roadmap** : R13.1 · **Date** : 2026-10-29 · **Verdict** : ⛔ **condition nommée** —
> la longueur BPE est mesurée (R13.0), mais la **PPL BPE-native** ne peut pas l’être : le modèle
> natif est en **octets** (`vocab = 256`), et aucun checkpoint BPE natif n’existe. Comparer la PPL
> de Qwen BPE à celle de `drave-n0` comparerait **deux modèles**, pas deux tokenisations.
>
> **Dispositif** : lecture du code (`tools/native_model.py:26`, `:192`), R13.0, aucun nouveau run ;
> données [`r13.1-condition.json`](r13.1-condition.json).

## La condition

| élément | état |
|---|---|
| modèle natif | **octets**, `NativeConfig.vocab = 256` |
| tokenizer déclaré | `{"kind": "bytes", "vocab": 256}` |
| tokenizer BPE | Qwen2.5, **151 936** jetons, **autre modèle** |
| checkpoint BPE natif | **aucun** |

**R13.1 exige** un modèle de **même architecture** et de **même budget**, mais avec un vocabulaire
BPE et son tokenizer. Ce modèle n’existe pas ; le fabriquer est une **campagne** (embedding
151 936 × d_model, entraînement, tokenizer versionné), pas un patch de mesure.

## Ce que R13.0 a établi

Le BPE divise la séq
… [3041 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/sessions.py --help 2>&1 | head -40; echo \"=== gates script ===\"; sed -n '1,50p' tools/toutes-les-portes.sh", "description": "Check sessions tool and gates script"}`

  ```
usage: sessions.py [-h] [--racine RACINE] [--status] [--check] [--strict]
                   [--modele] [--autotest] [--depuis-en-cours]

sessions.py — plans de session : qui fait quoi, avant d'écrire `en-cours`.
Chaque session active expose son mandat dans `journal/sessions/<id>/plan.md` :
périmètre, fichiers réservés, heartbeat, prochaine action, état. Les autres
sessions consultent `--status` avant de claim, et `--check` refuse les mandats
incomplets, les identifiants dupliqués, les périmètres qui se recouvrent et
les heartbeats périmés. `en-cours` reste la seule source de l'état : ce plan
est le **contrat de travail** qui le précède.

options:
  -h, --help         show this help message and exit
  --racine RACINE
  --status
  --check
  --strict
  --modele
  --autotest
  --depuis-en-cours  crée des plans à confirmer depuis les sections de en-
                     cours
=== gates script ===
#!/bin/bash
# toutes-les-portes.sh — LA PASSE COMPLÈTE, et l'instrument qui manquait.
#
# POURQUOI CETTE PORTE EXISTE. Le 12 octobre, `tools/porte-gain.sh` §9 exigeait un REFUS
# (`--attn-window` en réparti) que le v7 avait **délibérément retiré** en faisant voyager les
# trois réglages dans l
… [2089 caractères tronqués]
  ```

- **bash** `{"command": "git diff --stat reports/r04-tete-survol-v4.json 2>/dev/null; python3 - <<'EOF'\nimport json\nfor f in [\"reports/r04-tete-survol-v3.json\",\"reports/r04-tete-survol-v4.json\"]:\n    d=json.load(open(f))\n    print(f, {k:v for k,v in d.items() if k not in ('resultats',)})\n    print(\" n … [76 caractères tronqués]`

  ```
reports/r04-tete-survol-v3.json {'date': '2026-10-29', 'ligne': 'R0.4', 'paires': 498, 'positifs': 83, 'couches': '8:11', 'negatifs': 'durs (même section)', 'modele': 'Qwen2.5-0.5B-Q8_0', 'partage': 'leave-one-document-out', 'moyennes': {'tete': 0.575, 'bm25': 0.745, 'etiquettes_melangees': 0.548}}
 n= 28
reports/r04-tete-survol-v4.json {'date': '2026-10-29', 'ligne': 'R0.4', 'paires': 498, 'positifs': 83, 'couches': '8:11', 'negatifs': 'durs (même section)', 'modele': 'Qwen2.5-0.5B-Q8_0', 'partage': 'leave-one-document-out', 'moyennes': {'tete': 0.54, 'bm25': 0.72, 'etiquettes_melangees': 0.528}}
 n= 28
  ```

- **bash** `{"command": "git log --oneline -3 -- reports/r04-tete-survol-v4.json; echo \"=== commit body ===\"; git log -1 --format='%H %s%n%b' -- reports/r04-tete-survol-v4.json; echo \"=== diff v3 v4 per doc ===\"; python3 - <<'EOF'\nimport json\na={r['document']:r for r in json.load(open('reports/r04-tete-su … [414 caractères tronqués]`

  ```
981e4bbf CORPUS GELÉ — LA DÉRIVE DES BANCS EST CLOSE : 30 DOCUMENTS, MANIFESTE SHA256, 0 PROBLÈME
=== commit body ===
981e4bbf706103f231a00c6eca0fffd15525fad0 CORPUS GELÉ — LA DÉRIVE DES BANCS EST CLOSE : 30 DOCUMENTS, MANIFESTE SHA256, 0 PROBLÈME
Les bancs de R0.3 étaient adossés à des documents vivants : la réécriture de continuite.md par
une session voisine a fait perdre deux questions (84 → 83). Le corpus est maintenant figé :
copie des 30 documents (1,4 Mo) dans tools/tests/documents/corpus/, manifeste source → copie +
sha256, vérification --verifie (0 problème). Les constructeurs lisent la copie ; le JSON du banc
porte la copie ET la source.

Bancs régénérés sur le corpus gelé : 248 questions lexicales, 83 paraphrases (recouvrement 0,16,
max 0,43), 0 problème des deux côtés. Mesures rejouées : extractif 1,000/0,878 (lexical) et
0,609/0,258 (paraphrases) ; modèle 0,228 et 0,369 ; tête 0,540 contre BM25 0,720. Les
conclusions des fiches tiennent aux arrondis près.

Ce qui n'est pas gelé : l'extraction (le code de R0.1) — nommé, pas fait.

=== diff v3 v4 per doc ===
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 4, in <module>
KeyError: 'data/onu/pdf/A_RES_80
… [25 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '45,62p' docs/pilotage/backlog/index.md; echo \"=== R04/R05/R06/R07 headers ===\"; for f in docs/pilotage/backlog/R04-tete-survol.md docs/pilotage/backlog/R05-tete-balayage.md docs/pilotage/backlog/R06-tete-relecture.md docs/pilotage/backlog/R07-routeur-extractif-generatif.md; do … [94 caractères tronqués]`

  ```
contraintes mesurées sont dans chaque fiche et dans le [graphe](dependances.md). Le chemin le plus
long est `R01 → R02 → R03 → R31 → R32 → R51`.

| id | fiche | statut | prio | dépend de | ligne |
|---|---|---|---|---|---|
| R01 | [Graphe de document et registre de régions](R01-graphe-document.md) | mesurée | P0 | — | R0.1 |
| R02 | [Contrôleur de lecture](R02-controleur-lecture.md) | mesurée | P0 | R01 | R0.2 |
| R03 | [Banc de lecture rapide](R03-banc-lecture-rapide.md) | mesurée | P0 | R01, R02 | R0.3 |
| R04 | [Tête de survol](R04-tete-survol.md) | partiel | P1 | R03, R01 | R0.4 |
| R05 | [Tête de balayage](R05-tete-balayage.md) | partiel | P1 | R03, R01 | R0.4 |
| R06 | [Tête de relecture](R06-tete-relecture.md) | partiel | P2 | R03, R21, R22 | R0.4 |
| R07 | [Routeur extractif / génératif](R07-routeur-extractif-generatif.md) | partiel | P1 | R02, R03 | R0.5 |
| R11 | [Contexte hiérarchique et état de section](R11-contexte-hierarchique.md) | spécifiée | P1 | R01, N1, N2 | R1.1 |
| R12 | [Curriculum de contexte long](R12-curriculum-contexte.md) | spécifiée | P1 | R11 | R1.2 |
| R13 | [Tokenisation : octets ou BPE](R13-tokenisation-bpe.md) | prête | P2 | — | R1.3 |
| R21 | [Mémo
… [4592 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json,itertools\nd=json.load(open('reports/r07-routeur.json'))\nL=d['lignes']\nprint(\"n\",len(L),\"differes\",sum(1 for r in L if r['extractif']!=r['modele']))\ndef auc(vals, labels):\n    # labels: 1 if extractif wins\n    pairs=sorted(zip(vals,labels))\n    n … [933 caractères tronqués]`

  ```
n 332 differes 201
signal 0.733
z 0.633
ratio 0.597
etendue 0.385
couverture 0.588
longueur 0.431
  ```

- **bash** `{"command": "grep -n \"auc\\|differ\\|oracle\\|exactitude\" tools/routeur.py | head -40; echo \"=== relevant section ===\"; sed -n '1,140p' tools/routeur.py", "description": "Read router computation"}`

  ```
16:  - l'**exactitude du routeur** au seuil, et le **transfert** : seuil réglé sur un banc, testé
18:  - le **regret** contre un oracle qui choisirait toujours le bon lecteur ;
90:def auc(scores: list[float], labels: list[int]) -> float:
99:def exactitude_sur(lignes: list[dict], seuil: float, champ: str = "signal") -> float:
106:    return max(sorted({l[champ] for l in lignes}), key=lambda s: exactitude_sur(lignes, s, champ))
109:def exactitude(lignes: list[dict], seuil: float) -> float:
122:    return max(candidats, key=lambda s: exactitude(lignes, s))
131:        raise SystemExit("aucune question : les JSON de lecteurs manquent")
134:    differes = [l for l in lignes if l["extractif"] != l["modele"]]
135:    labels = [l["extractif"] for l in differes]
136:    signal_auc = auc([l["signal"] for l in differes], labels)
137:    couverture_auc = auc([l["couverture"] for l in differes], labels)
138:    longueur_auc = auc([l["longueur"] for l in differes], labels)
140:    aleatoire_auc = auc([hasard.random() for _ in differes], labels)
142:    # 2. exactitude : choix fixes, oracle, routeur réglé sur un banc et testé sur l'autre
145:    oracle = sum(max(l["extractif"], l["modele"]) for l
… [7601 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/r07-routeur.json'))\nL=[r for r in d['lignes'] if r['extractif']!=r['modele']]\nlabels=[r['extractif'] for r in L]\ndef auc(scores,labels):\n    P=[s for s,l in zip(scores,labels) if l==1]; N=[s for s,l in zip(scores,labels) if l … [308 caractères tronqués]`

  ```
signal 0.826
z 0.784
ratio 0.729
etendue 0.262
couverture 0.584
longueur 0.438
n diff 201 pos 173
  ```

- **todo_write** `{"todos": [{"content": "Nettoyer les artefacts parasites (JSON au nom glob, fichier =)", "status": "in_progress"}, {"content": "R0.5 — re-générer le JSON avec toutes les AUC, réécrire la fiche sur le corpus gelé", "status": "pending"}, {"content": "R0.4 — documenter la réplication v4 (corpus gelé) e … [334 caractères tronqués]`

  ```
Updated todo list: 5 pending, 1 in progress, 0 completed.
  ```

- **bash** `{"command": "grep -n \"R0\\.4\\|R0\\.5\\|R13\\|0,826\\|0,785\\|0,601\" docs/pilotage/programme-r.md | head -30; echo \"=== length ===\"; wc -l docs/pilotage/programme-r.md", "description": "Find R0.4/R0.5/R13 in programme-r"}`

  ```
21:| **têtes de lecture** (R0.4) | 0,601/0,836 puis 0,448/0,811 puis **0,540/0,720** | une sonde linéaire sur un 0,5 B, avec 500 paires, ne bat pas BM25 ; la donnée et l'encodeur manquent |
22:| **routeur** (R0.5) | signal AUC **0,826**, transfert 0,802/0,321 | un signe qui **prédit** n'est pas une règle qui **décide** : un seuil absolu ne transfère pas d'un corpus à l'autre |
31:2. **Un signal qui prédit n'est pas une règle qui décide.** L'AUC du signal BM25 est 0,826,
=== length ===
49 docs/pilotage/programme-r.md
  ```

- **bash** `{"command": "pwd; ls -b reports | grep -E \"r4[e-sx]-bloc\"; echo \"---\"; for f in 'reports/r4e-bloc-*.json' 'reports/r4s-bloc-*.json' 'reports/r4x-bloc-*.json' '='; do [ -f \"$f\" ] && echo \"OK $f $(stat -c%s \"$f\") octets\"; done", "description": "Verify junk paths before deletion"}`

  ```
/home/stephane/GitHub/Qtrinet
r4e-bloc-*.json
r4s-bloc-*.json
r4x-bloc-*.json
---
OK reports/r4e-bloc-*.json 4111 octets
OK reports/r4s-bloc-*.json 11840 octets
OK reports/r4x-bloc-*.json 1456 octets
OK = 0 octets
  ```

- **bash** `{"command": "rm -v 'reports/r4e-bloc-*.json' 'reports/r4s-bloc-*.json' 'reports/r4x-bloc-*.json' '='; git status --short", "description": "Delete junk artifacts"}`

  ```
removed 'reports/r4e-bloc-*.json'
removed 'reports/r4s-bloc-*.json'
removed 'reports/r4x-bloc-*.json'
removed '='
 m tools/docwatch
?? tools/r13_anglais.py
  ```

- **read** `{"file_path": "tools/routeur.py", "offset": 130, "limit": 80}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/routeur.py</path>
<type>file</type>
<content>
130:     if not lignes:
131:         raise SystemExit("aucune question : les JSON de lecteurs manquent")
132: 
133:     # 1. le signal prédit-il le gagnant ? (sur les questions où les deux diffèrent)
134:     differes = [l for l in lignes if l["extractif"] != l["modele"]]
135:     labels = [l["extractif"] for l in differes]
136:     signal_auc = auc([l["signal"] for l in differes], labels)
137:     couverture_auc = auc([l["couverture"] for l in differes], labels)
138:     longueur_auc = auc([l["longueur"] for l in differes], labels)
139:     hasard = random.Random(GRAINE)
140:     aleatoire_auc = auc([hasard.random() for _ in differes], labels)
141: 
142:     # 2. exactitude : choix fixes, oracle, routeur réglé sur un banc et testé sur l'autre
143:     extractif_fixe = sum(l["extractif"] for l in lignes) / len(lignes)
144:     modele_fixe = sum(l["modele"] for l in lignes) / len(lignes)
145:     oracle = sum(max(l["extractif"], l["modele"]) for l in lignes) / len(lignes)
146:     transferts = []
147:     champs = ("z", "ratio", "etendue", "couverture", "signal")
148:     for ba
… [2776 caractères tronqués]
  ```

- **edit** `{"file_path": "tools/routeur.py", "old_string": "    # 1. le signal prédit-il le gagnant ? (sur les questions où les deux diffèrent)\n    differes = [l for l in lignes if l[\"extractif\"] != l[\"modele\"]]\n    labels = [l[\"extractif\"] for l in differes]\n    signal_auc = auc([l[\"signal\"] for l  … [1201 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/routeur.py has been updated successfully.
  ```

- **edit** `{"file_path": "tools/routeur.py", "new_string": "        args.json.write_text(json.dumps({\n            \"date\": \"2026-10-29\", \"ligne\": \"R0.5\", \"questions\": len(lignes),\n            \"differes\": len(differes), \"differes_extractif\": sum(labels),\n            \"auc_signal\": round(signal_ … [509 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/routeur.py has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/routeur.py --json reports/r07-routeur.json 2>&1 | tail -30", "description": "Regenerate router JSON with all AUCs"}`

  ```
=== ROUTEUR EXTRACTIF / GÉNÉRATIF ===
  330 questions · 202 où les deux lecteurs diffèrent
  AUC du signal BM25   : 0.844
  AUC couverture       : 0.599
  AUC z                : 0.788
  AUC ratio            : 0.720
  AUC etendue          : 0.272
  AUC longueur (faux)  : 0.451
  AUC aléatoire        : 0.448
  exactitude : fixe extractif 0.721 · fixe modèle 0.267 · oracle 0.800
  testé sur lexical     (n=247) · fixe ext 0.874 · fixe modèle 0.231 · oracle 0.915
     seuil appris ailleurs · z           (seuil   4.62) → exactitude 0.822
     seuil appris ailleurs · ratio       (seuil  24.76) → exactitude 0.704
     seuil appris ailleurs · etendue     (seuil   0.17) → exactitude 0.231
     seuil appris ailleurs · couverture  (seuil   0.83) → exactitude 0.231
     seuil appris ailleurs · signal      (seuil   6.30) → exactitude 0.757
  testé sur paraphrase  (n= 83) · fixe ext 0.265 · fixe modèle 0.373 · oracle 0.458
     seuil appris ailleurs · z           (seuil   3.12) → exactitude 0.313
     seuil appris ailleurs · ratio       (seuil   8.03) → exactitude 0.313
     seuil appris ailleurs · etendue     (seuil   0.01) → exactitude 0.289
     seuil appris ailleurs · couverture  (seuil   0.4
… [135 caractères tronqués]
  ```

- **bash** `{"command": "ls -l reports/r03-banc-*.json reports/r07-routeur.json; echo \"=== last commits on benches ===\"; git log --oneline -3 -- reports/r03-banc-extractif.json reports/r03-banc-modele.json reports/r03-banc-durci-extractif.json reports/r03-banc-durci-modele.json; echo \"=== git diff ===\"; git … [79 caractères tronqués]`

  ```
-rw-r--r--. 1 stephane stephane 146499 29 oct 17:05 reports/r03-banc-durci-extractif.json
-rw-r--r--. 1 stephane stephane  66968 29 oct 17:26 reports/r03-banc-durci-modele.json
-rw-r--r--. 1 stephane stephane 433263 29 oct 17:05 reports/r03-banc-extractif.json
-rw-r--r--. 1 stephane stephane 202359 29 oct 17:21 reports/r03-banc-modele.json
-rw-r--r--. 1 stephane stephane 122319 30 oct 21:50 reports/r07-routeur.json
=== last commits on benches ===
981e4bbf CORPUS GELÉ — LA DÉRIVE DES BANCS EST CLOSE : 30 DOCUMENTS, MANIFESTE SHA256, 0 PROBLÈME
3328e0ec LE BANC DURCI PASSE À 84 PARAPHRASES : MODÈLE 0,375 CONTRE LEXICAL 0,269, TÊTE 0,575 CONTRE BM25 0,745
de9afbc9 R0.3 DURCI — 19 PARAPHRASES : LE LEXIQUE TOMBE À 0,30, LE MODÈLE PREND LA TÊTE À 0,717
=== git diff ===
 M reports/r07-routeur.json
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nb=json.load(open('tools/tests/documents/bench-complet.json'))\nprint(\"bench-complet keys\",list(b.keys()))\nq=[(d['chemin'],x) for d in b['documents'] for x in d.get('questions',[])]\nprint(\"questions bench\",len(q))\nfor f in ['reports/r03-banc-extract … [331 caractères tronqués]`

  ```
bench-complet keys ['version', 'date', 'note', 'documents', 'questions']
questions bench 248
reports/r03-banc-extractif.json 248 {'date': '2026-10-29', 'ligne': 'R0.2', 'graine': 20261029, 'critere': 'bm25', 'questions': 248}
reports/r03-banc-modele.json 248 {'date': '2026-10-29', 'ligne': 'R0.2', 'graine': 20261029, 'critere': 'bm25', 'questions': 248}
reports/r03-banc-durci-extractif.json 83 {'date': '2026-10-29', 'ligne': 'R0.2', 'graine': 20261029, 'critere': 'bm25', 'questions': 83}
reports/r03-banc-durci-modele.json 83 {'date': '2026-10-29', 'ligne': 'R0.2', 'graine': 20261029, 'critere': 'bm25', 'questions': 83}
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nb=json.load(open('tools/tests/documents/bench-complet.json'))\nq={(d['chemin'],x) for d in b['documents'] for x in d.get('questions',[])}\nprint(len(q))\next=json.load(open('reports/r03-banc-extractif.json'))['details']\nmod=json.load(open('reports/r03-ba … [542 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 3, in <module>
TypeError: unhashable type: 'dict'
[exit code: 1]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\next=json.load(open('reports/r03-banc-extractif.json'))['details']\nmod=json.load(open('reports/r03-banc-modele.json'))['details']\nke={(d['document'],d['question']) for d in ext}\nkm={(d['document'],d['question']) for d in mod}\nprint(len(ke),len(km),len( … [456 caractères tronqués]`

  ```
247 247 247
doublons ext [('tools/tests/documents/corpus/technique/format-flux.md', 'Quelle valeur le document associe-t-il à « jetons » et « dense » ?')]
doublons mod [('tools/tests/documents/corpus/technique/format-flux.md', 'Quelle valeur le document associe-t-il à « jetons » et « dense » ?')]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nkey=('tools/tests/documents/corpus/technique/format-flux.md','Quelle valeur le document associe-t-il à « jetons » et « dense » ?')\nfor f in ['reports/r03-banc-extractif.json','reports/r03-banc-modele.json']:\n    d=json.load(open(f))['details']\n    rows … [651 caractères tronqués]`

  ```
reports/r03-banc-extractif.json 2
{"document": "tools/tests/documents/corpus/technique/format-flux.md", "type": "technique", "question": "Quelle valeur le document associe-t-il à « jetons » et « dense » ?", "or": "trace dense, 512 jetons\t132 396 736 o\t66 370 408 o (−49,87 %)", "integrale": {"recupere": true, "f1": 0.0, "valeur": false, "cout": 10441, "reponse": "Ce que ce document est."}, "controlee_0.10": {"recupere": true, "f1": 0.0, "valeur": false, "cout": 968, "reponse": "Ce que ce document est."}, "controlee_0.30": {"rec
{"document": "tools/tests/documents/corpus/technique/format-flux.md", "type": "technique", "question": "Quelle valeur le document associe-t-il à « jetons » et « dense » ?", "or": "trace dense, 512 jetons\t66 370 408 o\t45 079 930 o (−32,1 %)", "integrale": {"recupere": true, "f1": 0.0, "valeur": false, "cout": 10441, "reponse": "Ce que ce document est."}, "controlee_0.10": {"recupere": true, "f1": 0.0, "valeur": false, "cout": 968, "reponse": "Ce que ce document est."}, "controlee_0.30": {"recup
reports/r03-banc-modele.json 2
{"document": "tools/tests/documents/corpus/technique/format-flux.md", "type": "technique", "question": "Quelle valeur le document ass
… [1507 caractères tronqués]
  ```

- **read** `{"file_path": "tools/routeur.py", "offset": 55, "limit": 45}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/routeur.py</path>
<type>file</type>
<content>
55:         index_par_document = {}
56:         jetons_par_document = {}
57:         for document in bench["documents"]:
58:             passages = lc.passages(graphe_document.manifeste(RACINE / document["chemin"]))
59:             index_par_document[document["chemin"]] = lc.Index(passages)
60:             jetons_par_document[document["chemin"]] = set(
61:                 j for p in passages for j in lc.jetons(p["texte"]))
62:         for cle, detail in ext.items():
63:             if cle not in modele:
64:                 continue
65:             scores = index_par_document[cle[0]].scores(cle[1])
66:             mots = set(lc.jetons(cle[1]))
67:             couverture = (len(mots & jetons_par_document[cle[0]]) / len(mots)) if mots else 0.0
68:             import statistics
69:             sommet = max(scores) if scores else 0.0
70:             moyenne = statistics.fmean(scores) if scores else 0.0
71:             ecart = statistics.pstdev(scores) if len(scores) > 1 else 1.0
72:             # signaux SANS ÉCHELLE : le sommet rapporté à la distribution du document
73:            
… [1486 caractères tronqués]
  ```

- **edit** `{"file_path": "tools/routeur.py", "new_string": "        ext = {(d[\"document\"], d[\"question\"], d.get(\"or\")): d for d in\n               json.loads(chemin_ext.read_text(encoding=\"utf-8\"))[\"details\"]}\n        modele = {(d[\"document\"], d[\"question\"], d.get(\"or\")): d for d in\n          … [397 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/routeur.py has been updated successfully.
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport re,pathlib\np=pathlib.Path('tools/routeur.py'); s=p.read_text()\ns=s.replace('scores = index_par_document[cle[0]].scores(cle[1])','scores = index_par_document[cle[0]].scores(cle[1])')\ns=s.replace('\"banc\": banc, \"document\": cle[0], \"question\": cle[1],','\ … [230 caractères tronqués]`

  ```
331 questions · 203 où les deux lecteurs diffèrent
  AUC du signal BM25   : 0.839
  AUC couverture       : 0.584
  AUC z                : 0.793
  AUC ratio            : 0.727
  AUC etendue          : 0.265
  AUC longueur (faux)  : 0.453
  AUC aléatoire        : 0.510
  exactitude : fixe extractif 0.719 · fixe modèle 0.269 · oracle 0.801
  testé sur lexical     (n=248) · fixe ext 0.871 · fixe modèle 0.234 · oracle 0.915
     seuil appris ailleurs · z           (seuil   4.62) → exactitude 0.819
     seuil appris ailleurs · ratio       (seuil  24.76) → exactitude 0.706
     seuil appris ailleurs · etendue     (seuil   0.17) → exactitude 0.234
     seuil appris ailleurs · couverture  (seuil   0.83) → exactitude 0.234
     seuil appris ailleurs · signal      (seuil   6.30) → exactitude 0.754
  testé sur paraphrase  (n= 83) · fixe ext 0.265 · fixe modèle 0.373 · oracle 0.458
     seuil appris ailleurs · z           (seuil   3.12) → exactitude 0.313
     seuil appris ailleurs · ratio       (seuil   8.03) → exactitude 0.313
     seuil appris ailleurs · etendue     (seuil   0.01) → exactitude 0.289
     seuil appris ailleurs · couverture  (seuil   0.40) → exactitude 0.325
     seuil appris 
… [95 caractères tronqués]
  ```

- **bash** `{"command": "grep -rln \"routeur\" tools/porte-*.sh tools/tests 2>/dev/null | head; echo \"=== json summary ===\"; python3 - <<'EOF'\nimport json\nd=json.load(open('reports/r07-routeur.json'))\nfor k in ['questions','differes','differes_extractif','auc_signal','aucs','fixe_extractif','fixe_modele',' … [260 caractères tronqués]`

  ```
tools/porte-profondeur-routee.sh
tools/tests/documents/bench-complet.json
tools/tests/documents/bench-durci.json
tools/tests/documents/corpus/technique/convertisseur.md
tools/tests/documents/corpus/tableau/en-cours.md
tools/tests/documents/corpus/tableau/index.md
tools/tests/documents/corpus/tableau/manques.md
tools/tests/documents/corpus/tableau/roadmap.md
=== json summary ===
questions 331
differes 203
differes_extractif 176
auc_signal 0.839
aucs {'signal': 0.839, 'z': 0.793, 'ratio': 0.727, 'etendue': 0.265, 'couverture': 0.584, 'longueur': 0.453, 'aleatoire': 0.51}
fixe_extractif 0.719
fixe_modele 0.269
oracle 0.801
lexical 248 0.871 0.234 0.915 {'z': 0.819, 'ratio': 0.706, 'etendue': 0.234, 'couverture': 0.234, 'signal': 0.754}
paraphrase 83 0.265 0.373 0.458 {'z': 0.313, 'ratio': 0.313, 'etendue': 0.289, 'couverture': 0.325, 'signal': 0.301}
  ```

- **bash** `{"command": "grep -rn \"0,826\\|0,802\\|332 questions\\|332\" docs/ reports/rapport-r07-routeur.md docs/pilotage/backlog/R07-routeur-extractif-generatif.md 2>/dev/null | grep -v \"reports/r07-routeur.json\" | head -30", "description": "Find all 0.826 and 332 references"}`

  ```
7kKs19DZAgl0W6m4avN1EAoFsX1IipxIKrkmlfzLMbX14afxyM7VKI8SrYJ4dE3DbLUG4xzZ3rQvBn282jpxU56J29YP3t8jVN/aqb6QqXpWRtXItUQ3R7DFK5TJlaQnP2SpDo2T81I4LAdTB/QxLAOdp10DN2IpnZGq5rJ9ivS0vDyP7QVQzMNekzb7PjociF3Krdu18cabBI3bCuW+LJ7Va6ONbrWrj3rn9tv7eKDcVw+7nW6V/aWPqkv6muHbFw9aTy1nw4CvLjIMI2IkTJajTtKtlFclLOUG9TlNB7tLfpehphxhdnCQnnfZz1k/cs+6guxjWwv+w6nmtPGecxdzB3m7uAe517kpfku/hn+Vf6H/Lv83wSYYq/gsFAjAkSLRGtFv4rRIa9YKXaKY+KPJdMkP0mXSf+RLZNtke2XvSa7BmrAr+RdCnTCo4AUO6HZyvWqmFqjvq4RaplahQ5dfbBuWLddH9Hv039lYBsaDK8YPjEi69LGpcbPTHST17TL9JZ5IqyBb1vWWz02Uvp6e5OD4TjtLHV+5Jrh/qNskYfl2e61eL/1zfRz/COBqkBLYGJgQWB14IXAocAbgXcCdwL3giXt9cF0cHzwYogdqg1tCxcirMii6NbopRi+uy02J3Y77o8vjN9PqBLjEv9LTk75U5NSR1NnUzcqaiv2V/yaXlupq6yunFn5e5WsKlvdnKnMNteQc8U1sZrFNXdzylwsdyKPKszmd9XiRret3VVIF57WYSc89U8a3m282rS6Od58pEXRArdMaJnbsrRlQ8vOlqMtI60z2xa0t7bvgTiBXmof61jRcebM+rnT2Lmm824XeiHZtajrTtf33YnuZ7sv9LB7zvaO74P63u3fPi4w7tH4lyZ4JhK223Pi8ok/TVpgsfWHJY5d9zwFEIn6pwAAf6Dk6crMMOnNAhJDEI0tUHhsIJAPLrgZ4wRdhG9ITVHo+2fsf3atDiAAFW6Vxba/3mXXItb3T17PPvdL9MVYOcbhgCnUDpX5f3w+j778gEjJawyi4jLwvhAPnqQ5gItlntzLbGT+4Ws0eYYBlI9q+83lydPc15pQ2bSnWT6MkNIgMHke+Qm2Y9jPTWvHUPMXkkmVtDInM+cOhXNKU/y1PyWAlYzs/+/6pbP3AAByXx76QC76QD3QWtw8qIelZwALfnt/o87q4YvvpBLv7k6MU
… [48731 caractères tronqués]
  ```

- **bash** `{"command": "wc -l reports/rapport-r07-routeur.md; sed -n '86,200p' reports/rapport-r07-routeur.md", "description": "Read remainder of router report"}`

  ```
147 reports/rapport-r07-routeur.md
donc « large » ne veut pas dire « facile ».

**Conclusion** : le signal est bon, la **calibration par document** est la bonne direction, mais
le banc des paraphrases (19 questions) ne permet pas d'apprendre le régime. Il faut **plus de
paraphrases** avant de rejouer le routeur — pas un autre signal.

## La version 3 (332 questions) : le signal monte à 0,826

Le banc élargi ajoute 84 paraphrases aux 248 questions lexicales. Le signal et les contrôles :

| mesure | valeur |
|---|---:|
| questions où les lecteurs diffèrent | 201 / 332 |
| **AUC du signal BM25** | **0,826** |
| AUC du z-score | 0,782 |
| AUC du ratio | 0,729 |
| AUC de la couverture | 0,584 |
| AUC de l'étendue | 0,264 |
| AUC de la longueur (faux signal) | 0,438 |
| AUC aléatoire | 0,409 |

Le signal **monte** (0,781 → 0,826) et les contrôles restent au hasard ou en dessous. Le
transfert s'améliore aussi :

| seuil appris sur l'autre banc, testé sur | z-score | brut | choix fixe |
|---|---:|---:|---:|
| le banc lexical (n=248) | **0,802** | 0,524 | 0,855 |
| les paraphrases (n=84) | 0,321 | 0,310 | **0,381** |

**Mais le routeur ne bat toujours pas le choix fixe** : 0,802 contre 0,85
… [1803 caractères tronqués]
  ```

- **read** `{"file_path": "reports/rapport-r07-routeur.md", "limit": 22}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-r07-routeur.md</path>
<type>file</type>
<content>
1: # R0.5 — le routeur : le signal prédit (0,826), la règle ne transfère pas
2: 
3: > **Ligne de roadmap** : R0.5 · **Date** : 2026-10-29 · **Verdict** : ⚠️ **partiel** — le signal
4: > BM25 **prédit** quel lecteur gagne (AUC **0,785**, contrôles à 0,41), mais un **seuil
5: > absolu ne transfère pas** d'un banc à l'autre (0,496 et 0,421, contre 0,855 et 0,737 pour le
6: > choix fixe). Le routeur n'est **pas déployé**.
7: >
8: > **Dispositif** : ré-analyse des mesures de R0.3 — 267 questions (248 lexicales, 19
9: > paraphrases), deux lecteurs, quatre JSON ; deux signaux (max BM25, couverture question ↔
10: > document) ; transfert par leave-one-bench-out ; JSON brut
11: > [`r07-routeur.json`](r07-routeur.json).
12: 
13: ## La question
14: 
15: Deux régimes mesurés : le **lexical** gagne sur les questions qui partagent les mots du document
16: (0,72–1,00 contre 0,23), le **modèle** gagne sur les paraphrases (0,717 contre 0,30). Un seul
17: lecteur perd la moitié des cas. Le routeur doit choisir — la seule question qui compte est :
18: **le signal prédit-il quel lecte
… [252 caractères tronqués]
  ```

- **edit** `{"file_path": "reports/rapport-r07-routeur.md", "new_string": "# R0.5 — le routeur : le signal prédit (0,839), la règle ne transfère pas\n\n> **Ligne de roadmap** : R0.5 · **Date** : 2026-10-30 · **Verdict** : ❌ **négatif** — sur le\n> corpus **gelé**, le signal BM25 **prédit** quel lecteur gagne (A … [1331 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-r07-routeur.md has been updated successfully.
  ```

- **read** `{"file_path": "reports/rapport-r07-routeur.md", "offset": 20, "limit": 20}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-r07-routeur.md</path>
<type>file</type>
<content>
20: 
21: ## Le dispositif
22: 
23: - **267 questions** : 248 du banc complet (lexicales) + 19 du banc durci (paraphrases) ;
24: - **deux lecteurs** : extractif (R0.2) et modèle (R0.3), sur les mêmes questions ;
25: - **deux signaux** : le **meilleur score BM25** des passages du document (avec son échelle, donc
26:   non comparable d'un document à l'autre), et la **couverture** — la fraction des mots de la
27:   question présents dans le document (sans échelle) ;
28: - **le transfert** : le seuil est appris sur un banc, **testé sur l'autre** ; c'est la seule
29:   façon de savoir si la règle est portable.
30: 
31: ## Ce qui est mesuré
32: 
33: | mesure | valeur |
34: |---|---|
35: | questions où les deux lecteurs **diffèrent** | **184** / 267 |
36: | **AUC du signal BM25** | **0,781** |
37: | AUC de la couverture | 0,529 |
38: | AUC du signal aléatoire | 0,407 |
39: | AUC de la longueur de la question (faux signal) | 0,395 |

(Showing lines 20-39 of 148. Use offset=40 to continue.)
</content>
  ```

- **edit** `{"file_path": "reports/rapport-r07-routeur.md", "new_string": "## Le dispositif (v1, 267 questions)\n\n> Les versions 1 et 2 ont été mesurées sur les **documents vivants** ; la version 3 les rejoue sur\n> le **corpus gelé**. Les chiffres des sections v1/v2 sont conservés comme histoire — le verdict\ … [249 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-r07-routeur.md has been updated successfully.
  ```

- **edit** `{"file_path": "reports/rapport-r07-routeur.md", "new_string": "## La version 3, rejouée sur le corpus gelé (331 questions)\n\nLe banc élargi ajoute les paraphrases aux questions lexicales. Sur le **corpus gelé** (copie\n`tools/tests/documents/corpus/`, manifeste SHA256), le dispositif compte **331 q … [3197 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-r07-routeur.md has been updated successfully.
  ```

- **read** `{"file_path": "reports/rapport-r07-routeur.md", "offset": 128}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-r07-routeur.md</path>
<type>file</type>
<content>
128: deux lecteurs deviennent **moins complémentaires**.
129: 
130: **Un bug de clé corrigé au passage** : deux questions de `format-flux.md` ont le **même libellé**
131: mais deux passages d'or différents (« jetons » et « dense »). L'ancien appariement
132: `(document, question)` en écrasait une ; la clé porte désormais le passage d'or, et les **331**
133: questions sont toutes comptées (330 avant le correctif).
134: 
135: **Conclusion** : le signal prédit de mieux en mieux, la règle ne décide pas. Il faudrait une
136: calibration par document **apprise** et un banc de **plusieurs centaines de paraphrases** — la
137: condition est nommée, pas atteinte.
138: 
139: ## Ce qui pourrait le rendre faux
140: 
141: - **19 questions paraphrases** : le seuil appris dessus est une estimation à ±0,1 ;
142: - **deux bancs de natures différentes** (questions générées vs écrites) : le transfert mesure
143:   aussi ce changement de nature, pas seulement l'échelle ;
144: - **la valeur binaire** (juste/faux) : une réponse partielle compte comme fausse ;
145: - **les lecteurs ne so
… [1043 caractères tronqués]
  ```

- **edit** `{"file_path": "reports/rapport-r07-routeur.md", "new_string": "## Ce qui pourrait le rendre faux\n\n- **83 questions paraphrases** : le seuil appris dessus reste une estimation à ±0,1 ;\n- **deux bancs de natures différentes** (questions générées vs écrites) : le transfert mesure\n  aussi ce changem … [2788 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-r07-routeur.md has been updated successfully.
  ```

- **bash** `{"command": "sed -n '15,40p' docs/pilotage/programme-r.md", "description": "Read programme-r context"}`

  ```
| **le balayage** (R05) | index de spans, offsets exacts | rappel@10 **0,984** (lexical), **0,1 ms** | `rapport-r05-balayage` |

## 2. Ce qui ne tient pas — et pourquoi, nommé

| tentative | chiffre | la raison |
|---|---|---|
| **têtes de lecture** (R0.4) | 0,601/0,836 puis 0,448/0,811 puis **0,540/0,720** | une sonde linéaire sur un 0,5 B, avec 500 paires, ne bat pas BM25 ; la donnée et l'encodeur manquent |
| **routeur** (R0.5) | signal AUC **0,826**, transfert 0,802/0,321 | un signe qui **prédit** n'est pas une règle qui **décide** : un seuil absolu ne transfère pas d'un corpus à l'autre |
| **relecture** (R06) | relire plus : **0/249** | le lecteur extractif répond avec le passage le mieux scoré, toujours lu ; la relecture doit changer de **modalité** |
| ~~déclencheur de la cascade~~ | **levé** (R06 v4/v5) : cascade à confiance **calibrée** = oracle (0,911 / 0,415) avec **~50 golds** | il fallait **calibrer par corpus**, pas transférer un seuil — **publié** (R06 v6 : fichier daté, `--calibration`) |

## 3. Les trois lois du programme

1. **Le corpus décide du lecteur, pas la question.** Le vrai gain de la voie auto est sur un
   corpus de valeurs (+0,109) ; sur un corpus mixt
… [709 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('docs/pilotage/programme-r.md'); s=p.read_text()\ns=s.replace(\"| **routeur** (R0.5) | signal AUC **0,826**, transfert 0,802/0,321 |\",\n            \"| **routeur** (R0.5) | signal AUC **0,839**, transfert 0,819/0,313 |\")\ns=s.replace … [1324 caractères tronqués]`

  ```
ok
docs/pilotage/programme-r.md:22:| **routeur** (R0.5) | signal AUC **0,839**, transfert 0,819/0,313 | un signe qui **prédit** n'est pas une règle qui **décide** : un seuil absolu ne transfère pas d'un corpus à l'autre |
docs/pilotage/programme-r.md:31:2. **Un signal qui prédit n'est pas une règle qui décide.** L'AUC du signal BM25 est 0,839,
docs/pilotage/backlog/R07-routeur-extractif-generatif.md:3:> **Statut** : mesurée (négatif) · **Priorité** : P1 · **Programme** : R · **Dépend de** : R02, R03
docs/pilotage/backlog/R07-routeur-extractif-generatif.md:4:> **Ligne de roadmap** : R0.5 · **Résultat** : [rapport-r07-routeur.md](../../../reports/rapport-r07-routeur.md) — signal AUC **0,839** (331 questions, corpus gelé) ; transfert z-score **0,819** / 0,313, toujours sous le choix fixe (0,871 / 0,373). La règle n'existe pas ; le chemin nommé est une calibration apprise par document et un banc de plusieurs centaines de paraphrases.
docs/pilotage/backlog/index.md:56:| R07 | [Routeur extractif / génératif](R07-routeur-extractif-generatif.md) | mesurée (négatif) | P1 | R02, R03 | R0.5 |
  ```

- **bash** `{"command": "sed -n '208,225p' docs/pilotage/roadmap.md", "description": "Read roadmap R0 rows for edit"}`

  ```
### R0 — le lecteur v0 (système, sans entraînement)

C'est la **priorité** : un lecteur au niveau **système**, avec le moteur existant et un modèle externe, pour
établir la cible avant de la porter dans le natif.

| # | fonctionnalité | état | porte |
|---|---|---|---|
| **R0.1** | **graphe de document** : régions typées (titre, section, paragraphe, tableau, code, maths, figure), offsets, provenance ; parseurs PDF/HTML/DOCX/Markdown ; sans modèle | ✅ **51 pages**, fidélité **1,000** | 50 pages découpées, provenance exacte, rejeu identique |
| **R0.2** | **contrôleur de lecture** : `survol`, `balayage`, `lecture`, `relecture`, `arrêt` ; budget en octets ; classique d'abord (TOC, titres, premières/dernières phrases, BM25/regex) | ✅ **1,000** à 30 % sur **5 types** | à 30 % du budget, **≥ 90 %** de la réponse de la lecture intégrale sur **3 types** |
| **R0.3** | **banc de lecture rapide** : 30 documents, 5 types, 10 questions/spans gold, modes intégral/écrémage/balayage/sélectif, contrôles closed-book, régions aléatoires, sections mélangées | ✅ **249 questions** : extractif **1,000** à 30 % ; modèle **0,231** contre début **0,042**. **Durci** (84 paraphrases) : modèle **0,375**, lexi
… [1468 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('docs/pilotage/roadmap.md'); s=p.read_text()\nold_r05=\"| **R0.5** | **routeur extractif / génératif** : choisir le lecteur selon la question (signal BM25), parce qu'aucun des deux ne gagne partout | ⚠️ **signal AUC 0,826** ; z-score t … [2270 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "sed -n '36,58p' docs/pilotage/roadmap.md", "description": "Read agenda section"}`

  ```
L'ordre est **la valeur / le coût**, pas la date. La dernière mise à jour est le **2026-10-29**.

1. **R0 — le lecteur v0** : **R0.1, R0.2 et R0.3 sont mesurés** (51 pages ; récupération **1,000** à
   30 % sur 5 types et **249 questions**) ; **R0.4** (tête de survol) est un **pilote négatif**
   (0,601 contre BM25 0,836) et **R0.5** (routeur) un **signal** (AUC 0,785, règle non transférable).
   **R4.1 — le bloc tableaux** est **mesurée** (996 cellules, **802** exactes, texte plat **0/3**),
   **R4.2 — le bloc code** aussi (294 fichiers, 24/24 extraits, texte seul **0/3**) et **R4.3 —
   le bloc maths** (32 formules, 10/10 dérivées, surface **0/3**) ; **R4.4 est bloqué** (OCR).
2. **N2 — la distillation et la hiérarchie** (en cours) : 49 999 fenêtres, 4 sources ; professeur 30k **1,734**
   (0,794 bit/octet) ; student **3,123** à 20 000 pas ; meilleur **2,6998** ; plateau **2,708** ; porte **< 2,5 non
   atteinte**. Le levier retenu est la **hiérarchie** (état de section), portée par N2.
3. ~~N0.3b — la parité de perplexité DRVM ↔ GGUF~~ **close** : conversion **68,1917 / 92,1875**, natif **4,6585 / 18,6394**.
4. **N4 — l'usage** : la **consigne courte** tenue à l'écart ; SFT **24
… [764 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('docs/pilotage/roadmap.md'); s=p.read_text()\nold=\"\"\"L'ordre est **la valeur / le coût**, pas la date. La dernière mise à jour est le **2026-10-29**.\n\n1. **R0 — le lecteur v0** : **R0.1, R0.2 et R0.3 sont mesurés** (51 pages ; réc … [804 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json,collections,statistics\nfor f in ['reports/r04-tete-survol-v3.json','reports/r04-tete-survol-v4.json']:\n    d=json.load(open(f)); by=collections.defaultdict(list)\n    for r in d['resultats']: by[r['type']].append(r)\n    print(f)\n    for t,rs in sorted( … [309 caractères tronqués]`

  ```
reports/r04-tete-survol-v3.json
  code 5 0.581 0.762 0.517
  juridique 6 0.422 0.646 0.559
  prose 6 0.684 0.882 0.603
  tableau 6 0.605 0.728 0.505
  technique 5 0.583 0.705 0.553
  mean {'tete': 0.575, 'bm25': 0.745, 'etiquettes_melangees': 0.548}
reports/r04-tete-survol-v4.json
  code 5 0.642 0.762 0.46
  juridique 6 0.389 0.646 0.47
  prose 6 0.723 0.882 0.611
  tableau 6 0.433 0.61 0.59
  technique 5 0.527 0.705 0.49
  mean {'tete': 0.54, 'bm25': 0.72, 'etiquettes_melangees': 0.528}
  ```

- **read** `{"file_path": "reports/rapport-r04-tete-survol.md", "limit": 14}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-r04-tete-survol.md</path>
<type>file</type>
<content>
1: # R0.4 — la tête de survol perd contre BM25 (0,601 contre 0,836), et gagne sur le juridique
2: 
3: > **Ligne de roadmap** : R0.4 · **Date** : 2026-10-29 · **Verdict** : ❌ **la tête ne bat jamais le
4: > scoreur classique** — v1 0,601 contre 0,836 ; v2 0,448 contre 0,811 ; **v3 (498 paires) 0,575
5: > contre 0,745**. La donnée paie (+13 points), mais une sonde linéaire ne rattrape pas BM25. ✅ le contrôle des étiquettes mélangées (**0,467**) montre que le
6: > signal est réel mais faible, pas une fuite.
7: >
8: > **Dispositif** : 114 paires (question, passage) — 19 questions du banc durci × (1 gold +
9: > 5 négatifs du même document) ; **états précoces** après les 4 premières couches de
10: > Qwen2.5-0.5B (896 valeurs, capturés par le moteur) ; tête logistique ridge ; partage
11: > **leave-one-document-out** ; JSON bruts [`r04-tete-survol.json`](r04-tete-survol.json) et
12: > [`r04-tete-survol-v2.json`](r04-tete-survol-v2.json) (version 2 : couches 8–11, négatifs durs).
13: 
14: ## La question

(Showing lines 1-14 of 143. Use offset=15 to continue.)
</content
… [1 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('reports/rapport-r04-tete-survol.md'); s=p.read_text()\nold=\"\"\"# R0.4 — la tête de survol perd contre BM25 (0,601 contre 0,836), et gagne sur le juridique\n\n> **Ligne de roadmap** : R0.4 · **Date** : 2026-10-29 · **Verdict** : ❌ ** … [2020 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('reports/rapport-r04-tete-survol.md'); s=p.read_text()\ns=s.replace(\"> **Dispositif** : 498 paires (question, passage) — 84 questions × (1 gold + 5 négatifs durs de\\n> la même section) ;\", \"> **Dispositif** : 498 paires (question,  … [223 caractères tronqués]`

  ```
ok
9:> **Dispositif** : 498 paires (question, passage) — 83 questions × (1 gold + 5 négatifs durs de
10-> la même section) ; **états précoces** après les couches 8–11 de Qwen2.5-0.5B (896 valeurs,
11-> capturés par le moteur) ; tête logistique ridge ; partage **leave-one-document-out** ; JSON
12-> bruts [`r04-tete-survol.json`](r04-tete-survol.json), [`v2`](r04-tete-survol-v2.json),
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('reports/rapport-r04-tete-survol.md'); s=p.read_text()\nold=\"\"\"**Ce que ça dit** : la donnée est bien le facteur limitant (×5,5 de paires → +13 points d'AUC),\nmais une **sonde linéaire** sur les états d'un 0,5 B ne rattrapera pas B … [1720 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "grep -n \"Ce qui pourrait le rendre faux\" reports/rapport-r04-tete-survol.md; sed -n '150,190p' reports/rapport-r04-tete-survol.md", "description": "Read R0.4 caveats and changes"}`

  ```
142:## Ce qui pourrait le rendre faux
- **États d'un modèle de 0,5 B** : les états précoces d'un modèle plus grand encodent sans doute
  plus de contenu.

## Ce que ça change

1. **La porte de R0.4 n'est pas atteinte** : la fiche reste ouverte, avec un chemin nommé —
   plus de paires, des états plus profonds, des négatifs difficiles, une tête non linéaire.
2. **Le seul signal positif est le régime paraphrase** : la tête gagne là où BM25 est faible.
   Si elle doit exister, c'est pour ce régime — pas pour remplacer BM25 partout.
3. **La leçon de méthode** : une tête jugée sur des négatifs faciles est une tête jugée sur un
   banc qui ne peut pas perdre. Le prochain jeu doit tirer ses négatifs dans le même voisinage
   lexical que le gold.

## Fichiers

- `tools/tete_survol.py` — capture des états, tête ridge, partage par document, contrôle.
- `reports/r04-tete-survol.json` — les mesures brutes.
- `tools/tests/documents/bench-durci.json` — les 19 questions et leurs golds.
  ```

- **bash** `{"command": "sed -n '142,152p' reports/rapport-r04-tete-survol.md", "description": "Read caveats lines"}`

  ```
## Ce qui pourrait le rendre faux

- **Petit N** : 114 paires, 5 plis de 18–24 ; une AUC à ±0,1 par pli.
- **Une seule tête linéaire** : une petite MLP ou une régression sur des états plus profonds
  peut changer la conclusion — c'est un négatif **de ce dispositif**, pas de l'idée.
- **Un seul format de prompt** : « Question / Passage » n'est pas la seule façon d'apparier.
- **Négatifs aléatoires** : le résultat dit « la tête ne bat pas BM25 sur des négatifs
  faciles », pas « la tête est inutile ».
- **États d'un modèle de 0,5 B** : les états précoces d'un modèle plus grand encodent sans doute
  plus de contenu.
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('reports/rapport-r04-tete-survol.md'); s=p.read_text()\nold=\"\"\"## Ce qui pourrait le rendre faux\n\n- **Petit N** : 114 paires, 5 plis de 18–24 ; une AUC à ±0,1 par pli.\n- **Une seule tête linéaire** : une petite MLP ou une régress … [1765 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('reports/rapport-r04-tete-survol.md'); s=p.read_text()\nold=\"\"\"## Fichiers\n\n- `tools/tete_survol.py` — capture des états, tête ridge, partage par document, contrôle.\n- `reports/r04-tete-survol.json` — les mesures brutes.\n- `tool … [504 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "grep -n \"statut\\|STATUTS\\|mesurée\\|partiel\" tools/verifie_backlog.py | head -30", "description": "Check backlog status vocabulary"}`

  ```
18:  5. le vocabulaire (statut, priorité, programme) est celui de l'index ;
43:STATUTS = {
44:    "idée", "spécifiée", "prête", "à faire", "en cours", "partiel", "mesurée",
50:# Les lignes mesurées ou closes de la roadmap. Une fiche peut en dépendre : elles ne
66:# Les contraintes mesurées n'ont pas d'arête : elles sont portées par la clé
115:            "statut": c.get("Statut", ""),
129:            "titre": titre, "fiche": "", "statut": "sans fiche", "prio": "—",
156:    """L'index et les fiches disent-ils le MÊME statut ? Le backlog est écrit deux fois (la
158:    outil. Sans ce contrôle, l'index peut annoncer « spécifiée » une fiche mesurée depuis
166:        nid, statut_index = m.group(1).strip(), m.group(2).strip()
170:        if noeuds[nid]["statut"] != statut_index:
171:            erreurs.append(f"{nid} : l'index dit « {statut_index} », la fiche dit "
172:                           f"« {noeuds[nid]['statut']} »")
193:        if d["statut"] not in STATUTS:
194:            erreurs.append(f"{n} : statut « {d['statut']} » hors vocabulaire")
220:    leve = {"mesurée", "abandonnée"}
222:        if d["statut"] != "prête":
225:            if cible in noeuds and noeuds[cible]["stat
… [555 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('docs/pilotage/backlog/index.md'); s=p.read_text()\ns=s.replace(\"| R07 | [Routeur extractif / génératif](R07-routeur-extractif-generatif.md) | mesurée (négatif) | P1 | R02, R03 | R0.5 |\",\n            \"| R07 | [Routeur extractif / g … [414 caractères tronqués]`

  ```
ok
=== GRAPHE DU BACKLOG ===
  fiches 37 · lignes sans fiche 1 · arêtes dures 42 · plafonds 3
  profondeur 5 : R01 → R02 → R03 → R31 → R32 → R51
  frontière (10) : A2.6, B10.3, B11.10, N2, N3, N4, R04, R05, R13, R44

✅ le graphe est cohérent : aucune arête morte, aucun cycle, aucune priorité inversée.
  ```

- **bash** `{"command": "sed -n '1,30p' reports/rapport-r13.3-anglais.md; echo \"=== r13.1 campagne ===\"; sed -n '1,30p' reports/rapport-r13.1-campagne.md", "description": "Read R13.3 and R13.1 campaign headers"}`

  ```
# R13.3 — anglais 100 Mo : le BPE perd encore à octets égaux

> **Ligne de roadmap** : R13.3 · **Date** : 2026-10-30 · **Verdict** : ⛔ **négatif confirmé** —
> sur l’anglais, à budget d’octets égal, BPE 512 fait **2,7522** et BPE 1024 **2,8147** bits/octet
> contre **2,6408** pour bytes : ils perdent **4,2 %** et **6,6 %**. Le signe est le même qu’en
> français ; ce n’est pas un artefact du corpus.
>
> **Dispositif** : tokenizers 512/1024 entraînés sur `corpus_en.txt` (100 276 153 octets), val
> `corpus_en_val.txt` (2 032 162 octets), bytes 10 k, BPE 512 5 k, BPE 1024 4 k (octets vus
> égaux), même graine/architecture ; données [`r13.3-anglais.json`](r13.3-anglais.json).

## Ce qui est mesuré

| modèle | pas | PPL val | bits/octet val | écart |
|---|---:|---:|---:|---:|
| bytes | 10 000 | **6,2366** | **2,6408** | — |
| BPE 512 | 5 000 | 26,4523 | 2,7522 | **+4,22 %** |
| BPE 1024 | 4 000 | 52,6075 | 2,8147 | **+6,59 %** |

- **Validation séparée** : tokenizers entraînés sur le train, évalués sur `corpus_en_val`.
- **Octets vus** : bytes 10,24 M ; BPE 512 5,12 M jetons ×1,7169 = 8,79 M octets (val ratio)
  — le contrôle exact est le ratio de **train** ; les deux restent dans la mêm
… [1854 caractères tronqués]
  ```

- **bash** `{"command": "ls docs/implantation/ | head -40; echo \"=== tokenisation refs ===\"; grep -rln \"BPE\\|tokenisation\" docs/implantation docs/theorie/architecture-native.md 2>/dev/null | head", "description": "Check implantation docs and tokenisation refs"}`

  ```
banc-lecture.md
bloc-code.md
bloc-maths.md
bloc-tableaux.md
configuration-nvme-raid-amd.md
contexte-long.md
convertisseur.md
corpus-gele.md
document-graph.md
format-clusters.md
format-flux.md
lecteur-controleur.md
llm-externe.md
numa-segregation.md
pipeline-lecture.md
tete-balayage.md
=== tokenisation refs ===
docs/implantation/tete-balayage.md
docs/theorie/architecture-native.md
  ```

- **bash** `{"command": "sed -n '1,70p' docs/implantation/bloc-maths.md", "description": "Read implantation doc style"}`

  ```
# Le bloc maths — un AST exact, un oracle indépendant

> **Ce que ce document est.** La spécification de **R4.3** : le sous-ensemble LaTeX lu, le
> type des valeurs, les règles de dérivation et de résolution, et ce qui est refusé. Le code
> est `tools/bloc_maths.py` ; la porte est
> [`porte-bloc-maths.sh`](../../tools/porte-bloc-maths.sh) ; les chiffres sont dans
> [`rapport-r43-bloc-maths.md`](../../reports/rapport-r43-bloc-maths.md).
>
> **Chargement** : lire § 2 et § 3 pour coder contre le bloc ; § 6 pour les limites.
>
> **Ce que ce bloc n'est pas** : un moteur de calcul formel général. Pas d'intégrale, pas de
> somme, pas de matrice, pas d'équation non linéaire — et un refus nommé plutôt qu'une
> approximation.

## 1. Le besoin

Une formule mathématique n'est pas du texte : `\frac{1}{3}+\frac{1}{6}` vaut `1/2`, et cette
valeur n'est écrite nulle part. R0.1 range les formules en région `maths` et le texte reste du
texte ; un lecteur de surface retrouve les chiffres, jamais le résultat. Un bloc classique
parse la formule, l'évalue **exactement**, la dérive et la résout — pour un coût constant.

## 2. Le contrat

| élément | contenu |
|---|---|
| **entrée** | une formule ou une é
… [2534 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"BPE\\|token\" docs/theorie/architecture-native.md | head -20", "description": "Check native architecture BPE mentions"}`

  ```
34:1. **Manifeste** (CBOR ou JSON compact) : magie `DRVM`, version, hash, provenance, tokenizer,
60:| **entrée** | octets 256 + mélangeur local (fenêtre 8) | pas de tokeniseur ; séquences plus longues, mais tête minuscule |
68:monolithique, pas de tokenizer BPE au v0, pas de chat avant les mécanismes.
110:tokenizer imposé, le chat avant les mécanismes.
122:- **Octets** : séquences 3–4× plus longues ; le BPE est une **décision de v1**, pas un prérequis.
  ```

- **write** `{"file_path": "reports/rapport-r13-decision.md", "content": "# R13 — la décision : rester en octets, parce que le BPE ne gagne pas à octets égaux\n\n> **Ligne de roadmap** : R13 / R1.3 · **Date** : 2026-10-30 · **Verdict** : ✅ **décision\n> mesurée — le natif reste en octets** (`vocab = 256`). À bud … [5335 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-r13-decision.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('reports/rapport-r13-decision.md'); s=p.read_text()\ns=s.replace(\"[`r13.3-anglais.json`](r13.3-anglais.json).\\n> [`r13.4-graines.json`](r13.4-graines.json).\",\n            \"[`r13.3-anglais.json`](r13.3-anglais.json),\\n> [`r13.4-gr … [117 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "grep -n \"vocab\\|tokenizer\" tools/native_model.py | head -8; echo \"=== tokenizer_bpe head ===\"; sed -n '1,25p' tools/tokenizer_bpe.py; echo \"=== entrainer ===\"; sed -n '1,20p' tools/entrainer_native_tokens.py", "description": "Verify native tokenizer code facts"}`

  ```
26:    vocab: int = 256
100:        self.embed = nn.Embedding(self.cfg.vocab, self.cfg.d_model)
103:        self.early_heads = nn.ModuleList([nn.Linear(self.cfg.d_model, self.cfg.vocab)
108:        self.local_heads = nn.ModuleList([nn.Linear(self.cfg.d_model, self.cfg.vocab)
113:        self.head_byte = nn.Linear(self.cfg.d_model, self.cfg.vocab)
185:                  "architecture": {"kind": "drave-n0", "vocab": cfg.vocab,
192:                  "tokenizer": {"kind": "bytes", "vocab": cfg.vocab}},
=== tokenizer_bpe head ===
#!/usr/bin/env python3
"""tokenizer_bpe.py — R13.1 : entraîne un BPE byte-level et tokenise un corpus.

Sortie : le tokenizer (JSON), les identifiants BPE (.pt) et les identifiants
octets (.pt), plus un JSON de stats (vocab, octets, jetons, octets/jeton,
réversibilité). Aucun modèle n'est entraîné ici.
"""
from __future__ import annotations

import argparse
import json
import pathlib

import torch
from tokenizers import Tokenizer, decoders, models, pre_tokenizers, trainers


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default="data/corpus_fr.txt")
    ap.add_argument("--vocab", type=int, default=512)
    ap.add_argument
… [802 caractères tronqués]
  ```

- **bash** `{"command": "ls tools/ | grep -E \"token|entrainer\" ; echo \"---\"; ls -l tools/tokenizer_bpe.py tools/entrainer_native_tokens.py 2>&1", "description": "Check tokenizer training tools exist"}`

  ```
c8_entrainer_tete.py
entrainer_moteur.py
entrainer_native.py
entrainer_native_tokens.py
porte-tokenizer-kimi.sh
tokenize_llama
tokenize_llama.cpp
tokenizer_bpe.py
tokenizer_kimi
---
-rw-r--r--. 1 stephane stephane 5937 30 oct 00:00 tools/entrainer_native_tokens.py
-rwxr-xr-x. 1 stephane stephane 2288 29 oct 23:38 tools/tokenizer_bpe.py
  ```

- **bash** `{"command": "git ls-files tools/ | grep -E \"tokenizer_bpe|entrainer_native_tokens|r13_anglais\"; echo \"---\"; git log --oneline -2 -- tools/tokenizer_bpe.py tools/entrainer_native_tokens.py", "description": "Check tracking of R13 tools"}`

  ```
tools/entrainer_native_tokens.py
tools/tokenizer_bpe.py
---
da038e34 R13.2 + A8.0 — VOCAB 1024 PERD 3,9 % À OCTETS ÉGAUX ; PORTE-INDICE ROUGE QUALIFIÉE
fa343715 R13.1 — À OCTETS ÉGAUX LE BPE PERD 0,7 % : LE PILOTE 11 % NE SE REPRODUIT PAS
  ```

- **write** `{"content": "# La tokenisation native — octets, par décision mesurée\n\n> **Ce que ce document est.** La spécification de **R13 / R1.3** : ce que le natif tokenise,\n> comment la décision a été mesurée, et dans quelles conditions elle serait rouverte. Le code\n> est `tools/native_model.py` (`NativeC … [5046 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/implantation/tokenisation.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "sed -n '1,10p' docs/pilotage/backlog/R13-tokenisation-bpe.md; echo \"=== README implantation ===\"; grep -n \"implantation\" docs/README.md | head; ", "description": "Read R13 fiche header and README inventory"}`

  ```
# R13 — Tokenisation : octets ou BPE (décision mesurée)

> **Statut** : prête · **Priorité** : P2 · **Programme** : R · **Dépend de** : — · **Plafonné par** : N2 (la qualité du corpus)
> **Ligne de roadmap** : R1.3 · **Fiche de résultat** : [rapport-r13-tokenisation.md](../../../reports/rapport-r13-tokenisation.md)
> **Résumé** : Décider par la mesure si le natif doit rester en octets ou passer au BPE.
> **Glossaire** : [BPE](../../theorie/glossaire/entrees/bpe.md) · [tokeniseur](../../theorie/glossaire/entrees/tokeniser-tokenizer.md) · [perplexité](../../theorie/glossaire/entrees/perplexite.md).

## Le besoin

Les octets allongent les séquences de 3–4× et réduisent l'empan utile. Le BPE est une décision de v1, pas un prérequis : il faut la chiffrer, pas la supposer.
=== README implantation ===
3:> **`docs/` dit ce qui reste vrai** : la méthode, l'état, la théorie, l'implantation. Les **chiffres** et les
70:| [`implantation/format-flux.md`](implantation/format-flux.md) | la spécification DRVF : trace, rejeu, transport |
71:| [`implantation/format-clusters.md`](implantation/format-clusters.md) | le modèle éclaté en clusters |
72:| [`implantation/convertisseur.md`](implantation/conve
… [646 caractères tronqués]
  ```

- **read** `{"file_path": "docs/pilotage/backlog/R13-tokenisation-bpe.md", "offset": 30}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/backlog/R13-tokenisation-bpe.md</path>
<type>file</type>
<content>
30: 2. pas de régression sur les langues et les scripts non latins
31: 3. le découpage est réversible (surface exacte)
32: 
33: ## Contrôles négatifs
34: 
35: - même graine, même budget, même corpus
36: - vocabulaire vide ou aléatoire (le gain doit disparaître)
37: 
38: ## Ce qui pourrait le rendre faux
39: 
40: - le BPE change les données effectives (mêmes octets, autres frontières)
41: - le vocabulaire contient les réponses du test
42: - la comparaison ne tient pas compte des longueurs de séquence
43: 
44: ## Étapes
45: 
46: 1. implémenter les deux tokenisations et le même entraînement
47: 2. mesurer PPL, coût, empan ; écrire la fiche
48: 3. décider et documenter dans la roadmap
49: 
50: ## Documents à écrire
51: 
52: - `tokenisation.md` (vocabulaire, découpage, mesures, décision, dans `docs/implantation/`)
53: - mettre à jour R1.3
54: 
55: ## Voir aussi
56: 
57: - [Programme R](../roadmap.md#r1--la-fenêtre-native)
58: - [Architecture native](../../theorie/architecture-native.md)

(End of file - total 58 lines)
</content>
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('docs/pilotage/backlog/R13-tokenisation-bpe.md'); s=p.read_text()\ns=s.replace(\"> **Statut** : prête · **Priorité** : P2 · **Programme** : R · **Dépend de** : — · **Plafonné par** : N2 (la qualité du corpus)\\n> **Ligne de roadmap** : … [2031 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\n# index\np=Path('docs/pilotage/backlog/index.md'); s=p.read_text()\ns=s.replace(\"| R04 | [Tête de survol](R04-tete-survol.md) | partiel | P1 | R03, R01 | R0.4 |\",\n            \"| R04 | [Tête de survol](R04-tete-survol.md) | mesurée | P1 |  … [1409 caractères tronqués]`

  ```
ok
=== GRAPHE DU BACKLOG ===
  fiches 37 · lignes sans fiche 1 · arêtes dures 42 · plafonds 3
  profondeur 5 : R01 → R02 → R03 → R31 → R32 → R51
  frontière (7) : A2.6, B10.3, B11.10, N2, N3, N4, R44

✅ le graphe est cohérent : aucune arête morte, aucun cycle, aucune priorité inversée.
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('docs/pilotage/roadmap.md'); s=p.read_text()\nold=\"| **R1.3** | **tokenisation** : octets ou BPE ; la décision est **mesurée**, pas doctrinale | 🔬 **condition** | à octets égaux, français 2 graines BPE512 **1,8071** contre **1,8001**, … [2018 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "sed -n '58,86p' docs/README.md", "description": "Read docs README implantation table"}`

  ```
| [`theorie/jeux-symboliques.md`](theorie/jeux-symboliques.md) | surface → RSN-jeu → pensée, 71 langues, maîtres |
| [`theorie/genealogie-des-langues.md`](theorie/genealogie-des-langues.md) | la généalogie et l'avertissement époque/filiation |
| [`theorie/synthese/index.md`](theorie/synthese/index.md) | la synthèse en 8 chapitres |
| [`theorie/glossaire.md`](theorie/glossaire.md) | le vocabulaire : couche vs étage, unité de sens, RSN |
| [`theorie/architecture-native.md`](theorie/architecture-native.md) | DRVM, `drave-n0` : le format et le modèle natifs |
| [`theorie/lecture-rapide.md`](theorie/lecture-rapide.md) | la lecture rapide humaine, les 14 techniques et les cinq couches qui manquent |
| [`theorie/glossaire/README.md`](theorie/glossaire/README.md) | les 316 fiches du glossaire |

## Implantation — comment c'est construit

| document | pour quoi |
|---|---|
| [`implantation/format-flux.md`](implantation/format-flux.md) | la spécification DRVF : trace, rejeu, transport |
| [`implantation/format-clusters.md`](implantation/format-clusters.md) | le modèle éclaté en clusters |
| [`implantation/convertisseur.md`](implantation/convertisseur.md) | le convertisseur et le chargement |
… [747 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"orphelin\\|README\\|référenc\\|reference\" tools/revue_documentation.py | head -20", "description": "Check doc review checks"}`

  ```
14:  7. navigation : aucun document vivant n'est orphelin, et aucun chemin en code inline
68:            if "archive" not in p.parts and p.name != "README.md" and not est_carte(p)]
80:    """Les fichiers vivants dont les liens comptent pour la navigation (orphelins)."""
82:            + [RACINE / "docs/README.md", RACINE / "README.md",
89:            + [RACINE / "README.md", RACINE / "REPRISE.md", RACINE / "AGENTS.md"])
97:               RACINE / "README.md", RACINE / "REPRISE.md", RACINE / "AGENTS.md"])
169:    if not (RACINE / "reports/README.md").exists():
170:        alertes.append("classement : reports/ n'a pas d'index (reports/README.md)")
244:    # 7b. orphelins : tout document vivant doit avoir au moins un lien entrant
264:        idx_cartes = RACINE / "docs/theorie/glossaire/README.md"
266:            alertes.append("glossaire : docs/theorie/glossaire/README.md manque")
271:                    alertes.append(f"glossaire : {c.name} n'est pas listé dans glossaire/README.md")
365:                alertes.append(f"synthèse : schéma non référencé → {s.name}")
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('docs/README.md'); s=p.read_text()\nold=\"| [`implantation/contexte-long.md`](implantation/contexte-long.md) | ce que 1 M de contexte veut dire, et par où ça casse |\"\nnew=old+\"\\n| [`implantation/tokenisation.md`](implantation/token … [205 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "grep -n \"État\\|etat\\|actif\\|terminé\\|heartbeat\\|HEARTBEAT\" tools/sessions.py | head -40", "description": "Inspect sessions.py state handling"}`

  ```
5:périmètre, fichiers réservés, heartbeat, prochaine action, état. Les autres
8:les heartbeats périmés. `en-cours` reste la seule source de l'état : ce plan
23:CHAMPS = ("session", "rôle", "périmètre", "fichiers réservés", "heartbeat",
25:ACTIFS = {"actif", "active", "en cours", "bloqué", "bloquee", "bloqué(e)"}
27:ETATS_CONNUS = ACTIFS | {"terminé", "termine", "libre", "libre."} | A_CONFIRMER
48:                         ("prochaine", "prochaine action"), ("etat", "état")):
54:    hb = champs.get("heartbeat", "")
55:    heartbeat = None
60:            heartbeat = datetime.fromisoformat(brut)
62:            heartbeat = datetime.strptime(brut, "%Y-%m-%d %H:%M")
63:        age = (datetime.now() - heartbeat).total_seconds() / 60.0
67:            "fichiers": fic, "heartbeat": heartbeat, "age": age,
68:            "etat": _cle(champs.get("état", ""))}
96:    heartbeat = f"{m.group(1)} {int(m.group(2)):02d}:{m.group(3)} HAE" if m else ""
107:                    "heartbeat": heartbeat})
119:        heartbeat = s["heartbeat"] or datetime.now().strftime("%Y-%m-%d %H:%M HAE")
126:> session : le heartbeat est celui de l'état, pas une preuve de vie.
132:- **Heartbeat** : {heartbeat}
134:- **Éta
… [1108 caractères tronqués]
  ```

- **bash** `{"command": "env | grep -i \"DSH\\|SESSION\" | head -20", "description": "Check DSH session env vars"}`

  ```
SESSION_MANAGER=local/Hauru:@/tmp/.ICE-unix/2291849,unix/Hauru:/tmp/.ICE-unix/2291849
XDG_SESSION_PATH=/org/freedesktop/DisplayManager/Session3
DSH_PROFILE=dsh-tui
SHELL_SESSION_ID=029763a5dedb454996450f02c24c4fbf
DSH_PROFILE_DIR=/home/stephane/.dsh/profiles/dsh-tui
DESKTOP_SESSION=plasma6
DSH_SHELL=1
XDG_SESSION_DESKTOP=KDE
XDG_SESSION_TYPE=x11
DSH_SESSION_ID=0b69f616-5c75-4c34-b97a-ae05564812af
MEMORY_PRESSURE_WATCH=/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/session.slice/plasma-plasmashell.service/memory.pressure
KONSOLE_DBUS_SESSION=/Sessions/1
XSESSION_IS_UP=yes
KDE_SESSION_UID=1000
XDG_SESSION_CLASS=user
KDE_SESSION_VERSION=6
XDG_SESSION_ID=7
DSH_HOME=/home/stephane/.dsh
KDE_FULL_SESSION=true
DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py --help 2>&1 | head -20; echo \"=== verifie_en_cours ===\"; python3 tools/verifie_en_cours.py --help 2>&1 | head -20", "description": "Check doc review and state checker options"}`

  ```
revue de documentation · 367 fiche(s) · 435 JSON · 109 doc(s) · 78 porte(s) · 8 chapitre(s)
  ❌ 3 anomalie(s) :
     · compteurs : en-cours.md dit 108 documents, le disque en a 109
     · compteurs : en-cours.md dit 366 fichiers, le disque en a 367
     · compteurs : en-cours.md dit 438 JSON, le disque en a 435
=== verifie_en_cours ===
  en-cours · 1210 mots · 7 sections · 3 session(s) · 7 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\nfor d in [\"8156fdcb\",\"c3d0f0bd\",\"N2-GPU\"]:\n    p=Path(\"journal/sessions\")/d/\"plan.md\"\n    s=p.read_text()\n    s=s.replace(\"- **État** : actif\",\"- **État** : terminé\")\n    p.write_text(s)\nprint(\"ok\")\nEOF\npython3 tools/se … [84 caractères tronqués]`

  ```
ok
sessions · plans de mandat
    71d57f53-8b41-4220 · terminé  · 649 min · docs/pilotage/en-cours.md, docs/methode/continuite.md, tools/sessions.py
      → coordination publiée ; migrer les trois sessions actives vers leur plan
    8156fdcb           · terminé  · 530 min · R0.1–R0.5
      → la boucle de lecture (R11, dépend de N2) ou la restitution (R31, dépend de R21) — toutes deux hors R0 ; sinon consolidation.
    N2-GPU             · terminé  · 530 min · N2
      → N2 — la **hiérarchie** (état de section), porte **< 2,5** (meilleur **2,6998**, plateau **2,708**) ; **N5 gelé**.
    c3d0f0bd           · terminé  · 530 min · R4.1–R4.3, B10.2bis, A8.3b
      → **B10.2bis** suite (encodeur) ; **A8.3b** ; **R4.4 bloqué**.
  ```

- **bash** `{"command": "date '+%Y-%m-%d %H:%M'; mkdir -p journal/sessions/0b69f616", "description": "Get time and create session dir"}`

  ```
2026-10-30 21:55
  ```

- **write** `{"content": "# Plan de session — 0b69f616\n\n> **Mandat confirmé** le 2026-10-30 21:55 depuis `en-cours` — session **unique** : les trois\n> mandats précédents sont terminés, la coordination multi-session n'a plus lieu d'être.\n\n- **Session** : `0b69f616-5c75-4c34-b97a-ae05564812af`\n- **Rôle** : c … [662 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/0b69f616/plan.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "ls tools/porte-*.sh | sed 's|tools/||' | tr '\\n' ' '; echo; ls tools/porte-*.sh | wc -l", "description": "List gates"}`

  ```
porte-adaptateur-sortie.sh porte-audit-drapeaux.sh porte-b1110-hybride.sh porte-balayage.sh porte-bloc-code.sh porte-bloc-maths.sh porte-bloc-tableaux.sh porte-budget.sh porte-bus.sh porte-bus-socket.sh porte-c4-retard.sh porte-cerveau.sh porte-consolidation.sh porte-coupe.sh porte-cycle-c2.sh porte-deepseek.sh porte-delais.sh porte-diff-couche.sh porte-document.sh porte-echange-experts.sh porte-episodique.sh porte-etat.sh porte-flux.sh porte-fusion.sh porte-gain.sh porte-greffe.sh porte-harnais-invariants.sh porte-homeostasie.sh porte-horloge.sh porte-indice.sh porte-jeux.sh porte-jumeaux.sh porte-lecteur.sh porte-lecture.sh porte-m5-brouillon.sh porte-melange.sh porte-memoire.sh porte-miroir-blocs.sh porte-mistral.sh porte-n3-cache.sh porte-n3-composition.sh porte-n3-deux-processus.sh porte-n3-deux-regions.sh porte-n3-generation.sh porte-n3-placement.sh porte-n3-pont.sh porte-n3-positions.sh porte-n3-profondeur.sh porte-n3-refus.sh porte-n3-reseau.sh porte-n3-routes.sh porte-n3-service-briques.sh porte-n3-service.sh porte-n3-seuil.sh porte-n3-sparsite-compte.sh porte-n3-sparsite.sh porte-occupation-elagage.sh porte-occupation-moteur.sh porte-pannes.sh porte-peripherie.sh porte-po
… [357 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,40p' tools/porte-document.sh; echo \"=== porte-etat ===\"; sed -n '1,40p' tools/porte-etat.sh", "description": "Read doc and state gates"}`

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
=== porte-etat ===
#!/bin/bash
# porte-etat.sh — l'état est COURT, STRUCTURÉ, et À JOUR (le fait et sa ligne).
#
# POURQUOI CETTE PORTE EXISTE. `verifie_en_cours.py` vérifie la forme ; il ne peut pas
# savoir qu'un fait a été commité sans sa ligne. Le 29/10, A8.0 (15 h 51) est passé
# après le dernier état (15 h 34) : la revue comparait des DATES, donc deux commits du
# même jour passaient. Cette porte compare des COMMITS, et vérifi
… [779 caractères tronqués]
  ```

- **write** `{"content": "# En ce moment\n\n**Mis à jour : 2026-10-30, 22 h 00 HAE (heure locale, EDT).**\n\n> **État courant, pas histoire.** Une sous-section par **session active** ; une ligne par **chantier** avec son\n> **bloquant**. Les détails de méthode sont dans [`methode/`](../methode/) — chargement et  … [7922 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
Updated file
</content>
  ```

- **bash** `{"command": "python3 tools/sessions.py --status 2>&1 | head -10; echo \"=== check ===\"; python3 tools/sessions.py --check 2>&1 | tail -6; echo \"=== en-cours ===\"; python3 tools/verifie_en_cours.py 2>&1 | tail -4", "description": "Validate sessions and state form"}`

  ```
sessions · plans de mandat
    0b69f616-5c75-4c34 · actif    ·   1 min · R0.4, R0.5, R13, R4.1–R4.3, en-cours, roadmap, backlog
      → commit de clôture — portes, revue de documentation, journal, état
    71d57f53-8b41-4220 · terminé  · 650 min · docs/pilotage/en-cours.md, docs/methode/continuite.md, tools/sessions.py
      → coordination publiée ; migrer les trois sessions actives vers leur plan
    8156fdcb           · terminé  · 531 min · R0.1–R0.5
      → la boucle de lecture (R11, dépend de N2) ou la restitution (R31, dépend de R21) — toutes deux hors R0 ; sinon consolidation.
    N2-GPU             · terminé  · 531 min · N2
      → N2 — la **hiérarchie** (état de section), porte **< 2,5** (meilleur **2,6998**, plateau **2,708**) ; **N5 gelé**.
    c3d0f0bd           · terminé  · 531 min · R4.1–R4.3, B10.2bis, A8.3b
=== check ===
  ⚠ session en-cours sans plan : 0b69f616
  ⚠ plan actif non listé dans en-cours : 0b69f616-5c75-4c34-b97a-ae05564812af
=== en-cours ===
  en-cours · 1045 mots · 7 sections · 1 session(s) · 8 puces · 5 questions
  ❌ 1 anomalie(s) :
     · session « Session `0b69f616` — clôture du lecteur (R0.4, R0.5, R13) » ne dit pas « **Ce que font les autres** »
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('journal/sessions/0b69f616/plan.md'); s=p.read_text()\ns=s.replace(\"- **Session** : `0b69f616-5c75-4c34-b97a-ae05564812af`\",\"- **Session** : `0b69f616`\")\np.write_text(s)\np=Path('docs/pilotage/en-cours.md'); s=p.read_text()\nold=\ … [480 caractères tronqués]`

  ```
ok
  ✅ plans cohérents
  en-cours · 1056 mots · 7 sections · 1 session(s) · 8 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  ```

- **bash** `{"command": "grep -rn \"0,826\\|0,785\\|332 questions\\|0,802\" --include=*.md docs/ reports/rapport-r07-routeur.md reports/rapport-r04-tete-survol.md 2>/dev/null | grep -v \"archive\" | head -20", "description": "Find remaining stale router numbers"}`

  ```
reports/rapport-r07-routeur.md:48:**Le signal BM25 sait quelque chose** (0,785 contre 0,407 au hasard ; la longueur, faux signal,
reports/rapport-r07-routeur.md:65:1. **Le signal existe** : l'AUC 0,785 n'est pas du hasard, et les contrôles le confirment.
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('reports/rapport-r07-routeur.md'); s=p.read_text()\ns=s.replace(\"**Le signal BM25 sait quelque chose** (0,785 contre 0,407 au hasard\",\"**Le signal BM25 sait quelque chose** (0,781 contre 0,407 au hasard\")\ns=s.replace(\"1. **Le sig … [254 caractères tronqués]`

  ```
ok
  revue de documentation · 367 fiche(s) · 435 JSON · 109 doc(s) · 78 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ```

- **bash** `{"command": "head -8 reports/INDEX.md; echo \"=== usage ===\"; python3 tools/index_reports.py --help 2>&1 | head -10", "description": "Check reports index generator"}`

  ```
# Index des fiches de reports/

> **Généré** par `tools/index_reports.py` — **362 fiches**. Les fichiers
> d'infrastructure (`README.md`, `INDEX.md`, `historique-*`) sont exclus du tableau ;
> la page d'état, elle, compte tous les `.md` de `reports/`.

| fiche | titre |
|---|---|
=== usage ===
  364 fiches → reports/INDEX.md
  ```

- **bash** `{"command": "grep -n \"argparse\\|add_argument\\|write_text\\|dry\" tools/index_reports.py | head -20", "description": "Inspect index_reports options"}`

  ```
39:    (RACINE / "reports/INDEX.md").write_text("\n".join(lignes) + "\n", encoding="utf-8")
  ```

- **bash** `{"command": "python3 tools/index_reports.py; head -4 reports/INDEX.md; git diff --stat reports/INDEX.md", "description": "Regenerate reports index"}`

  ```
364 fiches → reports/INDEX.md
# Index des fiches de reports/

> **Généré** par `tools/index_reports.py` — **364 fiches**. Les fichiers
> d'infrastructure (`README.md`, `INDEX.md`, `historique-*`) sont exclus du tableau ;
 reports/INDEX.md | 8 +++++---
 1 file changed, 5 insertions(+), 3 deletions(-)
  ```

- **bash** `{"command": "sed -n '38,55p' docs/pilotage/programme-r.md", "description": "Read programme-r conclusion"}`

  ```
## 4. La prochaine action

**Le déclencheur de la cascade** est le verrou unique de R04, R06 et de la relecture : un signal
**sans échelle** (accord entre lecteurs, dispersion, couverture de la réponse) — ou
l'acceptation que, sur un corpus de paraphrases, le **modèle seul** est la bonne politique et
que la cascade n'existe que pour les corpus mixtes.

## 5. Voir aussi

- [La roadmap](roadmap.md) — l'ordre des chantiers et la prochaine action.
- [Le banc](../implantation/banc-lecture.md) · [Le corpus gelé](../implantation/corpus-gele.md) ·
  [Le pipeline](../implantation/pipeline-lecture.md) · [Le balayage](../implantation/tete-balayage.md).
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('docs/pilotage/programme-r.md'); s=p.read_text()\nold=\"\"\"## 4. La prochaine action\n\n**Le déclencheur de la cascade** est le verrou unique de R04, R06 et de la relecture : un signal\n**sans échelle** (accord entre lecteurs, dispers … [825 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "grep -n \"R0\\.4\\|R0\\.5\\|R13\" docs/pilotage/roadmap.md", "description": "Review roadmap mentions"}`

  ```
33:| **R — le lecteur** | document, politique de lecture, fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ; **R4.1–R4.3 mesurées** | **R4.4 bloqué** (OCR) ; R1/R2/R3 attendent N2 |
40:   30 % sur 5 types et **249 questions**) ; **R0.4** (tête de survol) et **R0.5** (routeur) sont
81:[R0.5] lasts 2 days and is 60% complete and is colored in #b26a00
96:[R0.5] starts at [R0.1–R0.3]'s end
170:| **N5** | l'échelle : 50–100 M, corpus élargi | ⏸ **gelé** | après le verdict de **R11** sur le contexte ; R13 close — **octets**, le BPE n'est pas un prérequis |
220:| **R0.5** | **routeur extractif / génératif** : choisir le lecteur selon la question (signal BM25), parce qu'aucun des deux ne gagne partout | ❌ **close (négatif)** : signal AUC **0,839** (331 questions, corpus gelé) ; z-score transfère **0,819 / 0,313**, sous le choix fixe (**0,871 / 0,373**) | non atteinte — condition nommée : calibration apprise par document, banc de plusieurs centaines de paraphrases |
221:| **R0.4** | **têtes de lecture** : `survol` (pertinence d'une région), `balayage` (requête → spans), `relecture` (confiance/contradiction), greffées sur les têtes précoces 
… [837 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('docs/pilotage/roadmap.md'); s=p.read_text()\ns=s.replace(\"[R0.5] lasts 2 days and is 60% complete and is colored in #b26a00\",\n            \"[R0.4] lasts 2 days and is 100% complete and is colored in #6a1b9a\\n[R0.5] lasts 2 days an … [335 caractères tronqués]`

  ```
ok
81:[R0.4] lasts 2 days and is 100% complete and is colored in #6a1b9a
82:[R0.5] lasts 2 days and is 100% complete and is colored in #6a1b9a
97:[R0.4] starts at [R0.1–R0.3]'s end
98:[R0.5] starts at [R0.1–R0.3]'s end
  ```

- **bash** `{"command": "sed -n '1,30p' tools/porte-r13-bpe.sh; echo \"=== porte-budget ===\"; sed -n '1,25p' tools/porte-budget.sh", "description": "Read R13 and budget gates"}`

  ```
#!/bin/bash
# porte-r13-bpe.sh — R13.1 : un petit modèle natif BPE bat-il le modèle octets
# à budget d'OCTETS égal ?
#
# Deux modèles de même architecture (224, 6 blocs), même graine, même corpus
# français : le baseline est en octets (400 pas), le BPE en 512 jetons (200 pas)
# — 200 pas BPE voient ~405 k octets, 400 pas octets en voient ~410 k. On compare
# les BITS PAR OCTET, pas la PPL par jeton : le BPE a 1,98 octet/jeton.
set -u
cd "$(dirname "$0")/.."
PY=${PY:-/home/stephane/gpu-env/bin/python}
T=$(mktemp -d "${TMPDIR:-/tmp}/porte-r13-bpe-XXXXXX")
trap 'rm -rf "$T"' EXIT
[ -x "$PY" ] || { echo "  ❌ $PY absent"; exit 2; }
"$PY" -c "import torch, tokenizers" 2>/dev/null || { echo "  ❌ torch/tokenizers absents"; exit 2; }

echo "=== 1. tokenizer BPE 512 et corpus d'identifiants ==="
PYTHONPATH=. "$PY" tools/tokenizer_bpe.py --corpus data/corpus_fr.txt --vocab 512 \
  --sortie-tokenizer "$T/tok.json" --sortie-ids "$T/bpe_ids.pt" \
  --sortie-octets "$T/octets.pt" --stats "$T/stats.json" > "$T/tok.log" 2>&1 \
  || { echo "  ❌ tokenizer"; tail -3 "$T/tok.log"; exit 2; }
OCTETS=$("$PY" -c "import json;d=json.load(open('$T/stats.json'));print(d['octets'])")
REV=$("$PY" -c "import js
… [1842 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -8; echo \"=== journal ===\"; python3 tools/verifie_journal.py 2>&1 | tail -8; echo \"=== schemas ===\"; python3 tools/verifier_schemas.py 2>&1 | tail -5", "description": "Run doc size, journal, schema checks"}`

  ```
1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
    1818    147   T1   2000  docs/theorie/synthese/07-modeles-alternatifs-entree-sortie.md
  T0 max : 3835 mots (budget 4 000)

  avertissements :
     · 14 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 597 l. rapport-e5-distillation.md, 546 l. rapport-empreinte-memoire.md, 491 l. rapport-passe-k3-disque.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
=== journal ===
  journal · 36 jour(s) · 60 session(s) · 1437 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
=== schemas ===
  schémas · 428 document(s) · 22 SVG · 2 source(s)
  ✅ aucun ASCII art, SVG valides et référencés, blocs PlantUML inline valides,
     sources et images relatives.
  ```

- **bash** `{"command": "grep -ln \"revue_documentation\\|verifie_en_cours\\|taille_documents\" tools/porte-*.sh; echo \"---\"; grep -l \"verifie_backlog\" tools/porte-*.sh", "description": "Find doc/backlog gates"}`

  ```
tools/porte-etat.sh
---
[exit code: 1]
  ```

- **bash** `{"command": "JOURNAUX=/tmp/portes-cloture-$(date +%H%M) bash tools/toutes-les-portes.sh > /tmp/passe-cloture.log 2>&1; echo \"code=$?\"; tail -20 /tmp/passe-cloture.log", "description": "Run full gates pass in background", "run_in_background": true}`

  ```
started background job bash-122
  ```

- **bash** `{"command": "git status --short; echo \"=== diff stat ===\"; git diff --stat", "description": "Review working tree changes"}`

  ```
M docs/README.md
 M docs/pilotage/backlog/R04-tete-survol.md
 M docs/pilotage/backlog/R05-tete-balayage.md
 M docs/pilotage/backlog/R07-routeur-extractif-generatif.md
 M docs/pilotage/backlog/R13-tokenisation-bpe.md
 M docs/pilotage/backlog/index.md
 M docs/pilotage/en-cours.md
 M docs/pilotage/programme-r.md
 M docs/pilotage/roadmap.md
 M docs/theorie/architecture-native.md
 M journal/sessions/8156fdcb/plan.md
 M journal/sessions/N2-GPU/plan.md
 M journal/sessions/c3d0f0bd/plan.md
 M reports/INDEX.md
 M reports/r07-routeur.json
 M reports/rapport-r04-tete-survol.md
 M reports/rapport-r07-routeur.md
 m tools/docwatch
 M tools/routeur.py
?? docs/implantation/tokenisation.md
?? journal/sessions/0b69f616/
?? reports/rapport-r13-decision.md
?? tools/r13_anglais.py
=== diff stat ===
 docs/README.md                                     |    1 +
 docs/pilotage/backlog/R04-tete-survol.md           |    4 +-
 docs/pilotage/backlog/R05-tete-balayage.md         |    2 +-
 .../backlog/R07-routeur-extractif-generatif.md     |    4 +-
 docs/pilotage/backlog/R13-tokenisation-bpe.md      |   31 +-
 docs/pilotage/backlog/index.md                     |    8 +-
 docs/pilotage/en-cours.md              
… [836 caractères tronqués]
  ```

- **bash** `{"command": "grep -rln \"hierarch\\|hiérarch\" tools/*.py docs/pilotage/backlog/R11-contexte-hierarchique.md 2>/dev/null | head; echo \"=== R11 fiche head ===\"; sed -n '1,30p' docs/pilotage/backlog/R11-contexte-hierarchique.md", "description": "Check for hierarchy implementation"}`

  ```
tools/bloc_tableaux.py
docs/pilotage/backlog/R11-contexte-hierarchique.md
=== R11 fiche head ===
# R11 — Contexte hiérarchique et état de section

> **Statut** : spécifiée · **Priorité** : P1 · **Programme** : R · **Dépend de** : R01, N1, N2
> **Ligne de roadmap** : R1.1 · **Fiche de résultat attendue** : rapport-r11-contexte-hierarchique.md (à créer dans `reports/`)
> **Résumé** : Lire par sections avec un état de section, sans exiger que l'attention voie toute la page.
> **Glossaire** : [perplexité](../../theorie/glossaire/entrees/perplexite.md) · [test de l'aiguille](../../theorie/glossaire/entrees/test-de-l-aiguille.md) · [graphe de document](../../theorie/glossaire/entrees/graphe-de-document.md).

## Le besoin

Le natif surapprend 129 octets et échoue à 130–256. Avant d'allonger le contexte brut, il faut une hiérarchie : span → paragraphe → section → document, avec un état qui résume chaque section.

**Ordre arrêté le 2026-10-29** : c'est **N2** qui porte la hiérarchie (l'état de section, 3 graines) ; R11 mesure la fenêtre qui en résulte et n'ouvre donc qu'après N2. La mesure reste ici : PPL à 1 000 octets, aiguille native, stabilité.

## Le contrat

| élément | contenu |
|---
… [446 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('tools/routeur.py'); s=p.read_text()\ns=s.replace('\"date\": \"2026-10-29\", \"ligne\": \"R0.5\"','\"date\": \"2026-10-30\", \"ligne\": \"R0.5\"')\np.write_text(s)\nprint('ok')\nEOF\npython3 tools/routeur.py --json reports/r07-routeur. … [71 caractères tronqués]`

  ```
ok
=== ROUTEUR EXTRACTIF / GÉNÉRATIF ===
  331 questions · 203 où les deux lecteurs diffèrent
  AUC du signal BM25   : 0.839
  AUC couverture       : 0.584
  ```

- **bash** `{"command": "tail -12 /tmp/passe-cloture.log; echo \"---\"; grep -c \"✅\\|❌\" /tmp/passe-cloture.log", "description": "Check gates pass progress"}`

  ```
=== PASSE COMPLÈTE DES PORTES (78 portes, borne 1800 s) ===
    journaux : /tmp/portes-cloture-2156
---
0
[exit code: 1]
  ```

- **bash** `{"command": "ps aux | grep -E \"porte-|toutes-les-portes\" | grep -v grep | head; ls /tmp/portes-cloture-2156/ 2>/dev/null | head; tail -5 /tmp/portes-cloture-2156/*.log 2>/dev/null | head -20", "description": "Inspect running gate and logs"}`

  ```
stephane 2321141  0.7  0.0   7692  4036 ?        Ss   21:56   0:00 bash -c JOURNAUX=/tmp/portes-cloture-$(date +%H%M) bash tools/toutes-les-portes.sh > /tmp/passe-cloture.log 2>&1; echo "code=$?"; tail -20 /tmp/passe-cloture.log
stephane 2321149  0.0  0.0   7824  4128 ?        S    21:56   0:00 bash tools/toutes-les-portes.sh
stephane 2321162  0.0  0.0   5844  2436 ?        S    21:56   0:00 timeout 1800 bash tools/porte-adaptateur-sortie.sh
stephane 2321163  0.0  0.0   7824  4124 ?        S    21:56   0:00 bash tools/porte-adaptateur-sortie.sh
stephane 2323357  0.0  0.0   7824  2148 ?        S    21:57   0:00 bash tools/porte-adaptateur-sortie.sh
stephane 2323358  104  0.1 9601116 139976 ?      Rl   21:57   0:00 ./drave-core/target/release/drave /tmp/porte-adaptateur/reecrit.gguf --ppl /tmp/porte-adaptateur/morceau.txt --limit 256 --ctx 256 --threads 8
porte-adaptateur-sortie.log
porte de l'adaptateur de sortie — Qwen2.5-0.5B-Q8_0.gguf · plage 0:8 · 256 jetons
  ```

- **bash** `{"command": "sed -n '1,60p' docs/pilotage/references-non-regression.md", "description": "Read tolerated red gates"}`

  ```
# Références de non-régression

> **Dernière passe complète — 2026-10-29 à 22 h 09 :**
> **62 portes, 60 vertes, 2 rouges, 1 h 46**. Les deux rouges sont les **structurelles connues**
> (`porte-indice`, 895 s ; `porte-melange`, 110 s), avec les mêmes diagnostics ; **aucune
> régression**. Depuis, **6 portes ajoutées** dans la journée (le compte du disque est **68**) :
> elles sont vertes individuellement, mais n'ont pas encore pris leur tour dans une passe
> complète. Journaux : `/tmp/portes-1029-20h23`. L'historique des passes est dans
> [`reports/historique-passes-portes.md`](../../reports/historique-passes-portes.md). Les
> compteurs de la page d'état sont vérifiés par `tools/revue_documentation.py`.

> **Ce que ce fichier porte.** Les repères chiffrés qu'une passe complète imprime, et
> les invariants qui ne sont pas des chiffres. Les mesures de campagne (perplexités,
> budgets, latences) sont dans `reports/` — une fiche par expérience — et non ici :
> ce fichier ne porte que ce qu'une **porte** vérifie.

> **Passe du 2026-10-28 à 00 h 12** (**49 portes, 46 vertes, 3 rouges**, **1 h 40 min**) — la passe
> du programme N. Les deux rouges structurelles (`porte-indice`, `porte-mel
… [3151 caractères tronqués]
  ```

- **bash** `{"command": "head -20 reports/historique-passes-portes.md; echo \"...\"; tail -12 reports/historique-passes-portes.md", "description": "Read gate pass history format"}`

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
… [927 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"notes\\|carte de décision\\|</notes>\" journal/2026-10-30/README.md | head; sed -n '95,120p' journal/2026-10-30/README.md", "description": "Locate journal notes end"}`

  ```
5:> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
55:<!-- notes -->
87:**La carte de décision, et l'arrimage des écrans.** Trois vues avaient échoué à aider la
98:<!-- /notes -->
Et une convention pour l'humain : le **premier item** de la liste de tâches d'un écran TUI porte
`Session <id> — <rôle>`, le même id que le titre du bloc d'`en-cours` et que le champ `Session`
du plan. Trois supports, une identité — écrite dans `continuite.md` § 4.
<!-- /notes -->
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('journal/2026-10-30/README.md'); s=p.read_text()\nnote=\"\"\"\n**Session `0b69f616` — les chantiers du lecteur sont clos, l'état redevient unique.**\n\nLes trois mandats actifs sont terminés : il n'y a plus qu'une session, et elle ferm … [2124 caractères tronqués]`

  ```
ok
1
  ```

- **bash** `{"command": "git status --short journal/ | head -20; echo \"=== gates progress ===\"; tail -8 /tmp/passe-cloture.log; grep -c \"✅\\|❌\" /tmp/passe-cloture.log", "description": "Check journal changes and gate progress"}`

  ```
M journal/2026-10-30/README.md
 M journal/2026-10-30/docs.md
 M journal/sessions/8156fdcb/plan.md
 M journal/sessions/N2-GPU/plan.md
 M journal/sessions/c3d0f0bd/plan.md
?? journal/sessions/0b69f616/
=== gates progress ===
=== PASSE COMPLÈTE DES PORTES (78 portes, borne 1800 s) ===
    journaux : /tmp/portes-cloture-2156
0
[exit code: 1]
  ```

- **bash** `{"command": "tail -6 /tmp/portes-cloture-2156/porte-adaptateur-sortie.log 2>/dev/null; ps aux | grep -E \"porte-adaptateur|drave \" | grep -v grep | head -4", "description": "Check first gate log"}`

  ```
porte de l'adaptateur de sortie — Qwen2.5-0.5B-Q8_0.gguf · plage 0:8 · 256 jetons
  écriture  : complet 17.4315 → 17.4315 · tronqué 2687292.8165 → 2687292.8165
  ✅ PPL épinglées : complet 17.4315 · tronqué 2687292.8165
  ✅ l'écriture est fidèle (mêmes chiffres sur les deux chemins)
  ✅ invariant d'identité : 2687292.8165 (écart 0.00e+00)
stephane 2321162  0.0  0.0   5844  2436 ?        S    21:56   0:00 timeout 1800 bash tools/porte-adaptateur-sortie.sh
stephane 2321163  0.0  0.0   7824  4136 ?        S    21:56   0:00 bash tools/porte-adaptateur-sortie.sh
stephane 2331765  0.0  0.0   7824  2160 ?        S    21:57   0:00 bash tools/porte-adaptateur-sortie.sh
stephane 2331766  788  0.5 10704168 671892 ?     Rl   21:57   0:29 ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --ppl /tmp/porte-adaptateur/morceau.txt --limit 256 --ctx 256 --threads 8 --couches 0:8 --tete-partielle --adaptateur-sortie /tmp/porte-adaptateur/demi-echelle.f32
  ```

- **bash** `{"command": "git diff docs/pilotage/roadmap.md | head -120", "description": "Review roadmap diff"}`

  ```
diff --git a/docs/pilotage/roadmap.md b/docs/pilotage/roadmap.md
index 2f9d3f29..1d3d29c9 100644
--- a/docs/pilotage/roadmap.md
+++ b/docs/pilotage/roadmap.md
@@ -30,15 +30,16 @@
 | **A — le moteur** | formats, placement, transport, rejeu, matériels, ordonnanceur | ✅ A1–A8 ; **A3.4, A5.4, A6.2 bloqués** ; A2.6 partiel ; A3.2/A3.3 mesurées ; **A8.3c/d expliqués** | **A2.6** (experts : A6.2 bloqué) ; réduire le lot |
 | **B — l'intelligence** | langue, pensée, jeux, maîtres, banc externe, sémantique, modules | ✅ B1–B12 ; **B1.5 corpus**, **B12.10 et B10.2bis closes** ; le **décodeur** est levé (objectif mot : 32,5 ; JW 26,7), le `z` reste | B11.10 (cartes) ; B10.3 attend un **encodeur qui porte** |
 | **N — le natif** | DRVM, `drave-n0`, distillation, usage, échelle | 🔬 N0/N1 mesurés ; **N0.3b close** ; N2 plafonne à 2,708 ; N4 partiel | **N2** (la hiérarchie), **N4** (consigne courte) |
-| **R — le lecteur** | document, politique de lecture, fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; R0.4 **pilote négatif** ; **R4.1–R4.3 mesurées** | **R0.4** — négatifs difficiles ; **R4.4 bloqué** (OCR) |
+| **R — le lecteur** | document, politique de lecture, fenêtre, mémoire, resti
… [9347 caractères tronqués]
  ```

- **bash** `{"command": "tail -5 /tmp/passe-cloture.log; echo \"--- dernier journal ---\"; ls -t /tmp/portes-cloture-2156/*.log | head -2 | xargs -I{} sh -c 'echo {}; tail -3 {}'", "description": "Check gate progress again"}`

  ```
=== PASSE COMPLÈTE DES PORTES (78 portes, borne 1800 s) ===
    journaux : /tmp/portes-cloture-2156
  porte-adaptateur-sortie ✅                          65 s    ✅ porte tenue (écriture fidèle · invariant · effet · refus)
--- dernier journal ---
/tmp/portes-cloture-2156/porte-audit-drapeaux.log
/tmp/portes-cloture-2156/porte-adaptateur-sortie.log
  ✅ le drapeau agit : demi-échelle ⇒ 7740947.0594 (×2.8805744621019786)
  ✅ les trois cas invalides sont REFUSÉS (code 2), pas ignorés
  ✅ porte tenue (écriture fidèle · invariant · effet · refus)
  ```

- **bash** `{"command": "sed -n '1,45p' reports/rapport-r13-decision.md", "description": "Review decision fiche"}`

  ```
# R13 — la décision : rester en octets, parce que le BPE ne gagne pas à octets égaux

> **Ligne de roadmap** : R13 / R1.3 · **Date** : 2026-10-30 · **Verdict** : ✅ **décision
> mesurée — le natif reste en octets** (`vocab = 256`). À budget d'**octets** égal, le BPE perd
> partout : **+0,39 %** (512, deux graines), **+4,09 %** (1024), **+4,22 % / +6,59 %** (anglais).
> Le « gain de 11 % » du pilote était un **artefact de budget** : à pas égaux, le BPE voit deux
> fois plus d'octets.
>
> **Dispositif** : synthèse de six fiches et de cinq JSON — français (4,4 Mo) et anglais
> (100 Mo), vocabulaires 512 et 1024, deux graines ; comparaison en **bits/octet** à octets vus
> égaux, train/val séparés ; `tools/tokenizer_bpe.py`, `tools/entrainer_native_tokens.py`,
> `tools/r13_anglais.py` ; données [`r13-tokenisation.json`](r13-tokenisation.json),
> [`r13.1-bpe.json`](r13.1-bpe.json), [`r13.1-campagne.json`](r13.1-campagne.json),
> [`r13.2-vocab1024.json`](r13.2-vocab1024.json), [`r13.3-anglais.json`](r13.3-anglais.json),
> [`r13.4-graines.json`](r13.4-graines.json).

## La question

Le natif lit des **octets** : 1 jeton par octet, vocabulaire de 256. Le BPE promet des séquences
**3 à 5 fois
… [1373 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('reports/rapport-r13-decision.md'); s=p.read_text()\ns=s.replace(\"partout : **+0,39 %** (512, deux graines), **+4,09 %** (1024), **+4,22 % / +6,59 %** (anglais).\",\n            \"partout : **+0,39 %** (512, deux graines), **+3,92 à + … [289 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "grep -rn \"R13\" --include=*.md docs/pilotage docs/theorie | grep -v \"R13\\.\\|archive\" | head -20", "description": "Check remaining R13 references"}`

  ```
docs/pilotage/backlog/R13-tokenisation-bpe.md:1:# R13 — Tokenisation : octets ou BPE (décision mesurée)
docs/pilotage/backlog/dependances.md:104:| **R13** | spécifiée | — | N2 (plafond) | — | [R13-tokenisation-bpe.md](R13-tokenisation-bpe.md) |
docs/pilotage/backlog/dependances.md:166:| **R13** | spécifiée | aucune arête dure ; `N1` suffit à deux tokenisations | chiffrer octets contre BPE à budget égal |
docs/pilotage/backlog/dependances.md:209:| **P2** | `R22`, `R06`, `R32`, `R41`, `R42`, `R13` | le reste du lecteur, dans l'ordre du graphe |
docs/pilotage/backlog/dependances.md:239:(R04, R05, R06, R13, B10.2bis, et A8.3 absente de l'index) ; un graphe qui annonce « spécifiée »
docs/pilotage/backlog/index.md:59:| R13 | [Tokenisation : octets ou BPE](R13-tokenisation-bpe.md) | mesurée | P2 | — | R1.3 |
docs/pilotage/roadmap.md:172:| **N5** | l'échelle : 50–100 M, corpus élargi | ⏸ **gelé** | après le verdict de **R11** sur le contexte ; R13 close — **octets**, le BPE n'est pas un prérequis |
docs/pilotage/roadmap.md:237:| **R1.3** | **tokenisation** : octets ou BPE ; la décision est **mesurée**, pas doctrinale | ✅ **décidée : octets** (R13 close) | à octets égaux, français 2 graines
… [703 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/verifie_backlog.py 2>&1 | tail -4; grep -n \"R13\" docs/pilotage/backlog/dependances.md | head -5; git status --short docs/pilotage/backlog/dependances.md", "description": "Rerun backlog check and inspect dependances"}`

  ```
profondeur 5 : R01 → R02 → R03 → R31 → R32 → R51
  frontière (7) : A2.6, B10.3, B11.10, N2, N3, N4, R44

✅ le graphe est cohérent : aucune arête morte, aucun cycle, aucune priorité inversée.
104:| **R13** | spécifiée | — | N2 (plafond) | — | [R13-tokenisation-bpe.md](R13-tokenisation-bpe.md) |
166:| **R13** | spécifiée | aucune arête dure ; `N1` suffit à deux tokenisations | chiffrer octets contre BPE à budget égal |
209:| **P2** | `R22`, `R06`, `R32`, `R41`, `R42`, `R13` | le reste du lecteur, dans l'ordre du graphe |
239:(R04, R05, R06, R13, B10.2bis, et A8.3 absente de l'index) ; un graphe qui annonce « spécifiée »
  ```

- **bash** `{"command": "sed -n '96,110p' docs/pilotage/backlog/dependances.md; echo ---; sed -n '160,170p' docs/pilotage/backlog/dependances.md", "description": "Read dependances R13 rows"}`

  ```
| **R01** | mesurée | — | — | R02, R03, R04, R05, R11, R21, R22, R31, R32, R41, R42, R43, R51 | [R01-graphe-document.md](R01-graphe-document.md) |
| **R02** | mesurée | R01 (dure) | — | R03 | [R02-controleur-lecture.md](R02-controleur-lecture.md) |
| **R03** | partiel | R01 (dure), R02 (dure) | — | R04, R05, R06, R31, R51 | [R03-banc-lecture-rapide.md](R03-banc-lecture-rapide.md) |
| **R04** | spécifiée | R03 (dure), R01 (dure) | — | — | [R04-tete-survol.md](R04-tete-survol.md) |
| **R05** | spécifiée | R03 (dure), R01 (dure) | le manque M4 (aucun encodeur exécutable) | — | [R05-tete-balayage.md](R05-tete-balayage.md) |
| **R06** | spécifiée | R03 (dure), R21 (dure), R22 (dure) | — | — | [R06-tete-relecture.md](R06-tete-relecture.md) |
| **R11** | spécifiée | R01 (dure), N1 (acquis), N2 (dure) | — | R12, R21 | [R11-contexte-hierarchique.md](R11-contexte-hierarchique.md) |
| **R12** | spécifiée | R11 (dure) | les cinq négatifs 129–256 | — | [R12-curriculum-contexte.md](R12-curriculum-contexte.md) |
| **R13** | spécifiée | — | N2 (plafond) | — | [R13-tokenisation-bpe.md](R13-tokenisation-bpe.md) |
| **R21** | spécifiée | R01 (dure), R11 (dure) | la mémoire à 8 pas est négative (mesur
… [1868 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"dependances\\|ecrire\\|write_text\" tools/verifie_backlog.py | head -20; echo \"=== markers ===\"; grep -n \"<!--\" docs/pilotage/backlog/dependances.md | head", "description": "Check dependances regeneration"}`

  ```
31:  python3 tools/verifie_backlog.py --svg docs/schemas/backlog-dependances.svg
493:    chemin.write_text("\n".join(sortie) + "\n", encoding="utf-8")
=== markers ===
  ```

- **bash** `{"command": "sed -n '470,500p' tools/verifie_backlog.py; grep -n \"add_argument\" tools/verifie_backlog.py", "description": "Read verifie_backlog output writer"}`

  ```
f'  <text x="{x + 16}" y="{y0 + 19}" font-family="Verdana, DejaVu Sans, sans-serif" '
        f'font-size="8.5" fill="#333333">sans fiche (trou nommé)</text>'
    )
    x += 178
    sortie.append(
        f'  <path d="M {x} {y0 + 16} H {x + 30}" stroke="#3a3a3a" stroke-width="1.3" '
        f'fill="none" marker-end="url(#fleche)"/>'
    )
    sortie.append(
        f'  <text x="{x + 38}" y="{y0 + 19}" font-family="Verdana, DejaVu Sans, sans-serif" '
        f'font-size="8.5" fill="#333333">dépendance dure</text>'
    )
    x += 152
    sortie.append(
        f'  <path d="M {x} {y0 + 16} H {x + 30}" stroke="#b26a00" stroke-width="1.1" '
        f'stroke-dasharray="4 3" fill="none" marker-end="url(#fleche-douce)"/>'
    )
    sortie.append(
        f'  <text x="{x + 38}" y="{y0 + 19}" font-family="Verdana, DejaVu Sans, sans-serif" '
        f'font-size="8.5" fill="#333333">plafond</text>'
    )
    sortie.append("</svg>")
    chemin.parent.mkdir(parents=True, exist_ok=True)
    chemin.write_text("\n".join(sortie) + "\n", encoding="utf-8")


def tables(noeuds: dict) -> str:
    """Les quatre tables du graphe, dans l'ordre des chantiers. Générees, jamais recopiees :
    une table ecrit
… [333 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/verifie_backlog.py --tables 2>/dev/null | head -40; echo \"...\"; grep -n \"^## \\|^### \" docs/pilotage/backlog/dependances.md", "description": "Compare generated tables with dependances structure"}`

  ```
### A — le moteur

| item | état | dépend de (dure) | plafond / contrainte | débloque | fiche |
|---|---|---|---|---|---|
| **A2.6** | partiel | A2 (acquis) | — | — | [A2.6-ordonnanceur.md](A2.6-ordonnanceur.md) |
| **A3.2** | mesurée | A3 (acquis) | — | A3.3 | [A3.2-granularite.md](A3.2-granularite.md) |
| **A3.3** | mesurée | A3.2 (dure) | — | — | [A3.3-seuil.md](A3.3-seuil.md) |
| **A3.4** | bloquée | A3 (acquis) | bloqué : le compte et le runtime Colab | — | [A3.4-colab.md](A3.4-colab.md) |
| **A5.4** | bloquée | A5 (acquis) | bloqué : la carte Stratix V | — | [A5.4-fpga.md](A5.4-fpga.md) |
| **A6.2** | bloquée | A6 (acquis) | bloqué : aucun MoE local dans 16 Go de VRAM | — | [A6.2-moe-local.md](A6.2-moe-local.md) |
| **A8.0** | mesurée | A8 (acquis) | — | A8.3 | [A8.0-portes-ppl.md](A8.0-portes-ppl.md) |
| **A8.3** | mesurée | A8.0 (dure) | — | — | [A8.3-defaut.md](A8.3-defaut.md) |

### B — l'intelligence

| item | état | dépend de (dure) | plafond / contrainte | débloque | fiche |
|---|---|---|---|---|---|
| **B1.5** | bloquée | B1 (acquis) | bloqué : aucun corpus parallèle humain d'articles | — | [B1.5-prose-scientifique.md](B1.5-prose-scientifique.md) |
| **B10.2bis** | me
… [2058 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '52,60p' docs/pilotage/backlog/dependances.md; echo \"=== end of section 3 ===\"; sed -n '108,120p' docs/pilotage/backlog/dependances.md", "description": "Read section 3 boundaries"}`

  ```
## 3. Le graphe, par chantier

Les tables sont **générées** depuis les fiches (`python3 tools/verifie_backlog.py --tables`) : une
table recopiée à la main diverge au premier ajout. « Acquis » = la ligne est mesurée ou close, elle
ne demande aucun travail ; « sans fiche » = une ligne ouverte de la roadmap qui n'a pas encore de
contrat, donc pas de porte ni de contrôle négatif.

### A — le moteur

=== end of section 3 ===
| **R32** | spécifiée | R31 (dure), R01 (dure), R21 (dure) | — | R51, R52 | [R32-citations-provenance.md](R32-citations-provenance.md) |
| **R41** | spécifiée | R01 (dure) | — | R44 | [R41-bloc-tableaux.md](R41-bloc-tableaux.md) |
| **R42** | spécifiée | R01 (dure) | — | R44 | [R42-bloc-code.md](R42-bloc-code.md) |
| **R43** | spécifiée | R01 (dure) | — | R44 | [R43-bloc-maths.md](R43-bloc-maths.md) |
| **R44** | spécifiée | R41 (dure), R42 (dure), R43 (dure) | — | — | [R44-encodeur-visuel.md](R44-encodeur-visuel.md) |
| **R51** | spécifiée | R31 (dure), R32 (dure), R03 (dure), R01 (dure) | le manque M4 (aucun encodeur exécutable) | — | [R51-lecture-croisee.md](R51-lecture-croisee.md) |
| **R52** | spécifiée | B10.3 (dure), R31 (dure), R32 (dure) | — | — | [R52-mult
… [204 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport subprocess, pathlib\nout = subprocess.run([\"python3\",\"tools/verifie_backlog.py\",\"--tables\"],capture_output=True,text=True).stdout\n# garder à partir de la première sous-section\ni = out.index(\"### A — le moteur\")\ntables = out[i:].rstrip()+\"\\n\"\np=pa … [403 caractères tronqués]`

  ```
section 3 régénérée, 57 lignes
49:- **Le chemin critique passe par le banc** (`R03`) : `R04`, `R05`, `R06`, `R31`, `R51` en dépendent.
96:| **R01** | mesurée | — | — | R02, R03, R04, R05, R11, R21, R22, R31, R32, R41, R42, R43, R51 | [R01-graphe-document.md](R01-graphe-document.md) |
97:| **R02** | mesurée | R01 (dure) | — | R03, R07 | [R02-controleur-lecture.md](R02-controleur-lecture.md) |
98:| **R03** | mesurée | R01 (dure), R02 (dure) | — | R04, R05, R06, R07, R31, R51 | [R03-banc-lecture-rapide.md](R03-banc-lecture-rapide.md) |
99:| **R04** | mesurée | R03 (dure), R01 (dure) | — | — | [R04-tete-survol.md](R04-tete-survol.md) |
102:| **R07** | mesurée | R02 (dure), R03 (dure) | — | — | [R07-routeur-extractif-generatif.md](R07-routeur-extractif-generatif.md) |
105:| **R13** | mesurée | — | N2 (plafond) | — | [R13-tokenisation-bpe.md](R13-tokenisation-bpe.md) |
143:   provenance (`R32`) pour leur porte « deux sources citées » ; `R04` et `R05` des régions.
  ```

- **bash** `{"command": "grep -n \"^## \" docs/pilotage/backlog/dependances.md; sed -n '/^## 5\\. La frontière/,/^## 6\\./p' docs/pilotage/backlog/dependances.md | head -40", "description": "Read frontier section"}`

  ```
13:## 1. Trois types d'arête, et pourquoi un seul ne suffit pas
30:## 2. Le graphe
52:## 3. Le graphe, par chantier
117:## 4. Les défauts trouvés le 2026-10-29
154:## 5. La frontière : ce qui est réellement non bloqué
178:## 6. Les priorités (arrêtées le 2026-10-29)
221:## 7. Les sous-items : là où un item cache deux contrats
230:## 8. Ce que le graphe ne dit pas
245:## Voir aussi
## 5. La frontière : ce qui est réellement non bloqué

Douze items, dont sept fiches et cinq lignes sans fiche. C'est la file « jamais en attente »
réelle : elle est plus large que l'ordre du jour de la roadmap, et c'est voulu.

| item | état | pourquoi c'est libre | la prochaine action |
|---|---|---|---|
| **R01** | prête | aucune dépendance ; le contrat est écrit | écrire le schéma de manifeste, brancher un parseur, mesurer 50 pages |
| **N0.3b** | prête | N0 est mesuré sauf elle | reproduire la PPL GGUF puis DRVM, sur 59 et 1 076 octets |
| **N4** | partiel | aucune arête dure ; `N2` n'est qu'un plafond | SFT avec partage par document, évalué tenu à l'écart |
| **N2** | en cours | `N1` acquis ; le levier reste à choisir | données et capacité, 3 graines — laisser la hiérarchie à `R11` |
| **B11.10** | 
… [1056 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"frontière\\|frontiere\" tools/verifie_backlog.py | head; sed -n '/def frontiere/,/return/p' tools/verifie_backlog.py | head -40", "description": "Read frontier computation"}`

  ```
19:  6. il calcule la **frontière** : ce qui est réellement non bloqué aujourd'hui, et la
252:def frontiere(noeuds: dict) -> list[str]:
540:    libres = frontiere(noeuds)
552:    print(f"  frontière ({len(libres)}) : {', '.join(libres) if libres else 'aucune'}")
def frontiere(noeuds: dict) -> list[str]:
    """Ce sur quoi on peut travailler aujourd'hui : aucune dépendance dure non levée, et
    aucun blocage externe nommé. Une ligne « en cours » ou « partielle » en fait partie :
    non bloquée ne veut pas dire non commencée."""
    leve = {"mesurée", "abandonnée"}
    out = []
    for n, d in sorted(noeuds.items()):
        if d["statut"] in leve or d["bloque"]:
            continue
        libre = True
        for cible, _ in d["dures"]:
            if cible in noeuds and noeuds[cible]["statut"] not in leve:
                libre = False
        if libre:
            out.append(n)
    return out
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport sys; sys.path.insert(0,'tools')\nimport verifie_backlog as vb\nnoeuds=vb.lit_fiches() if hasattr(vb,'lit_fiches') else None\nprint([n for n in dir(vb) if 'lit' in n or 'charge' in n or 'noeud' in n][:10])\nEOF", "description": "Inspect backlog module functions" … [1 caractères tronqués]`

  ```
[]
  ```

- **bash** `{"command": "grep -n \"^def \\|^    return\" tools/verifie_backlog.py | head -20; sed -n '530,560p' tools/verifie_backlog.py", "description": "Find node loading function"}`

  ```
70:def fiches() -> list[pathlib.Path]:
73:    return sorted(p for p in BACKLOG.glob("*.md") if id_de(p) != p.stem)
76:def id_de(p: pathlib.Path) -> str:
78:    return m.group(1) if m else p.stem
80:def champs(p: pathlib.Path) -> dict[str, str]:
89:    return out
92:def liste(valeur: str | None) -> list[tuple[str, str]]:
102:    return out
105:def construire():
134:    return noeuds
137:def arreter(noeuds: dict, erreurs: list[str], avertissements: list[str]) -> None:
155:def controler_index(noeuds: dict, erreurs: list[str]) -> None:
178:def controler(noeuds: dict):
249:    return erreurs, avert, niveau
252:def frontiere(noeuds: dict) -> list[str]:
267:    return out
270:def chemin_le_plus_long(noeuds: dict, niveau: dict) -> tuple[int, str]:
281:    return niveau.get(fin, 0), " → ".join(reversed(chemin))
296:def decouper(texte: str, largeur: int = 23, lignes_max: int = 2) -> list[str]:
315:    return lignes
    ap = argparse.ArgumentParser(description="Vérifie le graphe des dépendances du backlog.")
    ap.add_argument("--svg", type=pathlib.Path, help="écrit aussi le graphe en SVG")
    ap.add_argument("--tables", action="store_true", help="imprime les tables du graphe")
    args = a
… [1072 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport sys; sys.path.insert(0,'tools')\nimport verifie_backlog as vb\nn=vb.construire()\nfor k in vb.frontiere(n):\n    d=n[k]\n    print(k, \"|\", d['statut'], \"| bloque:\", d.get('bloque'), \"| dures:\", [c for c,_ in d['dures']], \"| douces:\", [c for c,_ in d['do … [61 caractères tronqués]`

  ```
A2.6 | partiel | bloque:  | dures: ['A2'] | douces: []
B10.3 | bloquée | bloque:  | dures: [] | douces: []
B11.10 | prête | bloque:  | dures: ['B11'] | douces: []
N2 | en cours | bloque:  | dures: ['N1'] | douces: []
N3 | partiel | bloque:  | dures: ['N1'] | douces: []
N4 | partiel | bloque:  | dures: [] | douces: ['N2']
R44 | spécifiée | bloque:  | dures: ['R41', 'R42', 'R43'] | douces: []
  ```

- **bash** `{"command": "sed -n '1,8p' docs/pilotage/backlog/R44-encodeur-visuel.md; echo \"=== A3.4 ===\"; sed -n '1,8p' docs/pilotage/backlog/A3.4-colab.md; echo \"=== champs parse ===\"; sed -n '80,105p' tools/verifie_backlog.py", "description": "Compare blocked fiche headers"}`

  ```
# R44 — Encodeur visuel / OCR (scans, figures, layout)

> **Statut** : spécifiée · **Priorité** : P3 · **Programme** : R · **Dépend de** : R41, R42, R43
> **Ligne de roadmap** : R4.4 · **Fiche de résultat attendue** : rapport-r44-encodeur-visuel.md (à créer dans `reports/`)
> **Résumé** : Lire les pages scannées, les figures et le layout, et retrouver la réponse du texte natif.
> **Glossaire** : [OCR](../../theorie/glossaire/entrees/ocr.md) · [layout](../../theorie/glossaire/entrees/layout.md) · [WER](../../theorie/glossaire/entrees/wer.md).

## Le besoin
=== A3.4 ===
# A3.4 — Démonstration Colab (préremplissage réparti)

> **Statut** : bloquée · **Priorité** : P3 · **Programme** : A · **Dépend de** : A3 · **Bloqué par** : le compte et le runtime Colab
> **Ligne de roadmap** : A3.4 · **Fiche de résultat attendue** : rapport-a34-colab.md (à créer dans `reports/`)
> **Résumé** : Exécuter le préremplissage réparti sur un runtime Colab.
> **Glossaire** : [préremplissage](../../theorie/glossaire/entrees/preremplissage.md) · [Colab](../../theorie/glossaire/entrees/colab-notebook-tunnel.md) · [fidélité](../../theorie/glossaire/entrees/fidelite.md).

## Le besoin
=== champs parse ===
def c
… [986 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '43,50p' tools/verifie_backlog.py; grep -n \"| R44\" docs/pilotage/backlog/index.md", "description": "Check status vocabulary and R44 index"}`

  ```
STATUTS = {
    "idée", "spécifiée", "prête", "à faire", "en cours", "partiel", "mesurée",
    "bloquée", "abandonnée",
}
PRIORITES = {"P0", "P1", "P2", "P3"}
PROGRAMMES = {"A", "B", "N", "R"}

# Les lignes mesurées ou closes de la roadmap. Une fiche peut en dépendre : elles ne
67:| R44 | [Encodeur visuel / OCR](R44-encodeur-visuel.md) | spécifiée | P3 | R41, R42, R43 | R4.4 |
  ```

- **bash** `{"command": "sed -n '1,7p' docs/pilotage/backlog/B11.10-cartes-ambiguites.md; echo \"=== B10.3 ===\"; sed -n '1,7p' docs/pilotage/backlog/B10.3-raisonnement-z.md; echo \"=== index B ===\"; grep -n \"| B10.3 \\|| B11.10 \" docs/pilotage/backlog/index.md", "description": "Check B10.3/B11.10 statuses"}`

  ```
# B11.10 — Cartes et ambiguïtés de la RSN

> **Statut** : prête · **Priorité** : P2 · **Programme** : B · **Dépend de** : B11
> **Ligne de roadmap** : B11.10 · **Fiche de résultat attendue** : rapport-b1110-cartes.md (à créer dans `reports/`)
> **Résumé** : Traiter les cartes et les surfaces ambiguës (symbole du morpion, chemin des dames).
> **Glossaire** : [RSN](../../theorie/glossaire/entrees/representation-semantique-neutre.md) · [RSN-jeu](../../theorie/glossaire/entrees/rsn-jeu.md).

=== B10.3 ===
# B10.3 — Raisonnement sur `z` gelé

> **Statut** : bloquée · **Priorité** : P2 · **Programme** : B · **Dépend de** : [B10.2bis](B10.2bis-decodeur-attention-croisee.md) · **Contraint par** : B10.2bis négatif (chrF 11.2 / 16.4 contre 39,6)
> **Ligne de roadmap** : B10.3 · **Fiche de résultat attendue** : rapport-b103-raisonnement-z.md (à créer dans `reports/`)
> **Résumé** : Brancher un opérateur de raisonnement sur l'embedding sémantique `z`, une fois le décodeur au-dessus du plancher.
> **Glossaire** : [RSN](../../theorie/glossaire/entrees/representation-semantique-neutre.md) · [chrF](../../theorie/glossaire/entrees/chrf.md) · [contrôle négatif](../../theorie/glossaire/entrees/contro
… [240 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\n# 1. outil : une ligne « bloquée » n'est pas dans la frontière\np=Path('tools/verifie_backlog.py'); s=p.read_text()\nold=\"\"\"        if d[\"statut\"] in leve or d[\"bloque\"]:\n            continue\"\"\"\nnew=\"\"\"        if d[\"statut\"]  … [1900 caractères tronqués]`

  ```
ok
  fiches 37 · lignes sans fiche 1 · arêtes dures 42 · plafonds 3
  profondeur 5 : R01 → R02 → R03 → R31 → R32 → R51
  frontière (4) : A2.6, N2, N3, N4

✅ le graphe est cohérent : aucune arête morte, aucun cycle, aucune priorité inversée.
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport subprocess, pathlib\nout = subprocess.run([\"python3\",\"tools/verifie_backlog.py\",\"--tables\"],capture_output=True,text=True).stdout\ni = out.index(\"### A — le moteur\")\ntables = out[i:].rstrip()+\"\\n\"\np=pathlib.Path('docs/pilotage/backlog/dependances.m … [316 caractères tronqués]`

  ```
ok
## 5. La frontière : ce qui est réellement non bloqué

Douze items, dont sept fiches et cinq lignes sans fiche. C'est la file « jamais en attente »
réelle : elle est plus large que l'ordre du jour de la roadmap, et c'est voulu.

| item | état | pourquoi c'est libre | la prochaine action |
|---|---|---|---|
| **R01** | prête | aucune dépendance ; le contrat est écrit | écrire le schéma de manifeste, brancher un parseur, mesurer 50 pages |
| **N0.3b** | prête | N0 est mesuré sauf elle | reproduire la PPL GGUF puis DRVM, sur 59 et 1 076 octets |
| **N4** | partiel | aucune arête dure ; `N2` n'est qu'un plafond | SFT avec partage par document, évalué tenu à l'écart |
| **N2** | en cours | `N1` acquis ; le levier reste à choisir | données et capacité, 3 graines — laisser la hiérarchie à `R11` |
| **B11.10** | prête | `B11` mesuré ; le codec lit 100 % | étendre le codec aux cartes, nommer les ambiguïtés |
| **B12.10** | partiel | `B12` acquis ; les modules existent | jeu de codes neufs et ablation de M4 |
| **R13** | spécifiée | aucune arête dure ; `N1` suffit à deux tokenisations | chiffrer octets contre BPE à budget égal |
| **A2.6** | partiel | `A2` mesuré | experts et tête dans la
… [675 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('docs/pilotage/backlog/dependances.md'); s=p.read_text()\na=s.index(\"## 5. La frontière\"); b=s.index(\"## 6. Les priorités\")\nnew=\"\"\"## 5. La frontière : ce qui est réellement non bloqué\n\n**Quatre items** — c'est la file « jama … [1264 caractères tronqués]`

  ```
ok
  profondeur 5 : R01 → R02 → R03 → R31 → R32 → R51
  frontière (4) : A2.6, N2, N3, N4

✅ le graphe est cohérent : aucune arête morte, aucun cycle, aucune priorité inversée.
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('docs/pilotage/en-cours.md'); s=p.read_text()\ns=s.replace(\"- **Backlog — graphe** : 37 fiches, 42 arêtes, **7 à la frontière** ; `tools/verifie_backlog.py`.\",\n            \"- **Backlog — graphe** : 37 fiches, 42 arêtes, **4 à la fr … [1420 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('docs/pilotage/roadmap.md'); s=p.read_text()\ns=s.replace(\"| **B — l'intelligence** | langue, pensée, jeux, maîtres, banc externe, sémantique, modules | ✅ B1–B12 ; **B1.5 corpus**, **B12.10 et B10.2bis closes** ; le **décodeur** est l … [1495 caractères tronqués]`

  ```
ok
31:| **B — l'intelligence** | langue, pensée, jeux, maîtres, banc externe, sémantique, modules | ✅ B1–B12 ; **B1.5 corpus**, **B12.10, B10.2bis et B11.10 closes** ; le **décodeur** est levé (objectif mot : 32,5 ; JW 26,7), le `z` reste | B10.3 attend un **encodeur qui porte** |
77:[B11.10] lasts 1 day and is 100% complete and is colored in #2e7d32
94:[B11.10] starts at [B1–B12]'s end
95:[B12.10] starts at [B11.10]'s end
149:| **B11** | la base d'universaux typés : schéma, parseur, codec, contexte | ✅ | **B11.10 close** (cartes, ambiguïtés refusées) ; le codec lit **100 %** |
  ```

- **bash** `{"command": "tail -6 /tmp/passe-cloture.log; grep -c \"✅\\|❌\" /tmp/passe-cloture.log", "description": "Check gates progress"}`

  ```
=== PASSE COMPLÈTE DES PORTES (78 portes, borne 1800 s) ===
    journaux : /tmp/portes-cloture-2156
  porte-adaptateur-sortie ✅                          65 s    ✅ porte tenue (écriture fidèle · invariant · effet · refus)
1
  ```

- **bash** `{"command": "tail -5 /tmp/portes-cloture-2156/porte-audit-drapeaux.log 2>/dev/null; ps aux | grep -E \"porte-audit|drave|python3\" | grep -v grep | head -5", "description": "Check second gate status"}`

  ```
root        1630  0.0  0.0 145532 53496 ?        Ssl  oct25   0:01 /usr/bin/python3.13 /usr/sbin/firewalld --nofork --nopid
root        1799  0.0  0.0 490620 47684 ?        Ssl  oct25   5:40 /usr/bin/python3.13 /usr/bin/fail2ban-server -xf start
stephane 2333998  0.0  0.0   5844  2436 ?        S    21:58   0:00 timeout 1800 bash tools/porte-audit-drapeaux.sh
stephane 2333999  0.0  0.0   7824  4120 ?        S    21:58   0:00 bash tools/porte-audit-drapeaux.sh
stephane 2334059  0.0  0.0   5844  2436 ?        S    21:58   0:00 timeout 1800 /home/stephane/gpu-env/bin/python -u tools/audit_drapeaux_harnais.py --pas 200 --sortie /tmp/porte-audit-drapeaux
  ```

- **bash** `{"command": "ps -o pid,etime,%cpu,rss,cmd -p 2334059 2>/dev/null; ls -la /tmp/porte-audit-drapeaux 2>/dev/null | head; date", "description": "Inspect audit process progress"}`

  ```
PID     ELAPSED %CPU   RSS CMD
2334059       02:05  0.0  2436 timeout 1800 /home/stephane/gpu-env/bin/python -u tools/audit_drapeaux_harnais.py --pas 200 --sortie /tmp/porte-audit-drapeaux
total 22364
drwxr-xr-x.    7 stephane stephane     360 30 oct 22:00 .
drwxrwxrwt. 1107 root     root      603920 30 oct 22:00 ..
drwxr-xr-x.    2 stephane stephane     100 30 oct 22:00 croissance
-rw-r--r--.    1 stephane stephane 4574656 30 oct 22:00 croissance.gguf
-rw-r--r--.    1 stephane stephane     798 30 oct 22:00 croissance.log
drwxr-xr-x.    2 stephane stephane     100 30 oct 21:58 elagage25
-rw-r--r--.    1 stephane stephane 4574656 30 oct 21:58 elagage25.gguf
-rw-r--r--.    1 stephane stephane    1265 30 oct 21:58 elagage25.log
drwxr-xr-x.    2 stephane stephane     100 30 oct 21:59 masque10
ven 30 oct 2026 22:00:14 EDT
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -4; echo \"=== en-cours ===\"; python3 tools/verifie_en_cours.py 2>&1 | tail -3; echo \"=== sessions ===\"; python3 tools/sessions.py --check 2>&1 | tail -2", "description": "Re-run doc, state, session checks"}`

  ```
revue de documentation · 367 fiche(s) · 435 JSON · 109 doc(s) · 78 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
=== en-cours ===
  en-cours · 1059 mots · 7 sections · 1 session(s) · 8 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
=== sessions ===
  ✅ plans cohérents
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nfor f in ['reports/r04-tete-survol-v3.json','reports/r04-tete-survol-v4.json']:\n    d=json.load(open(f))\n    g=[r['document'] for r in d['resultats'] if r['auc_tete']>r['auc_bm25']]\n    print(f,len(g),g)\nEOF", "description": "Count documents won by he … [13 caractères tronqués]`

  ```
reports/r04-tete-survol-v3.json 6 ['data/onu/pdf/A_RES_80_10-en.pdf', 'docs/implantation/contexte-long.md', 'docs/implantation/format-clusters.md', 'docs/pilotage/en-cours.md', 'docs/pilotage/references-non-regression.md', 'docs/theorie/semantique-universaux.md']
reports/r04-tete-survol-v4.json 8 ['tools/tests/documents/corpus/code/format-clusters.md', 'tools/tests/documents/corpus/code/utilisation.md', 'tools/tests/documents/corpus/juridique/A_RES_80_10-es.pdf', 'tools/tests/documents/corpus/prose/lecture-rapide.md', 'tools/tests/documents/corpus/prose/semantique-universaux.md', 'tools/tests/documents/corpus/tableau/en-cours.md', 'tools/tests/documents/corpus/tableau/references-non-regression.md', 'tools/tests/documents/corpus/technique/contexte-long.md']
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('reports/rapport-r04-tete-survol.md'); s=p.read_text()\nold=\"reste de **18 points**. Le seul changement notable est le **tableau** (0,605 → 0,433), dont les\\ndocuments ont changé au gel ; la tête gagne toujours **un** document sur 28 … [500 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('reports/rapport-r04-tete-survol.md'); s=p.read_text()\ns=s.replace(\"- **N moyen** : 498 paires, 28 plis ; une AUC à ±0,1 par pli, et un seul document gagné.\",\n            \"- **N moyen** : 498 paires, 28 plis ; une AUC à ±0,1 par p … [157 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "ls -la data/corpus_fr_train.txt data/corpus_fr_val.txt data/corpus_en.txt data/corpus_en_val.txt 2>&1 | head; echo \"=== r13.3 json ===\"; python3 -c \"import json;d=json.load(open('reports/r13.3-anglais.json'));print(list(d.keys())[:12])\"", "description": "Verify corpus file names"}`

  ```
-rw-r--r--. 1 stephane stephane 100276153  8 oct 09:42 data/corpus_en.txt
-rw-r--r--. 1 stephane stephane   2032162  8 oct 09:42 data/corpus_en_val.txt
-rw-r--r--. 1 stephane stephane   4402195 28 oct 12:45 data/corpus_fr_train.txt
-rw-r--r--. 1 stephane stephane    231694 28 oct 12:45 data/corpus_fr_val.txt
=== r13.3 json ===
['date', 'ligne', 'corpus', 'donnees', 'modeles', 'ecarts_pct', 'verdict', 'controle', 'limites', 'prochain']
  ```

- **bash** `{"command": "head -3 tools/r13_anglais.py; stat -c '%a %n' tools/r13_anglais.py tools/routeur.py", "description": "Check script permissions"}`

  ```
#!/usr/bin/env python3
"""r13_anglais.py — R13.3/R13.4 : le BPE perd-il à octets égaux, sur l'anglais ?

600 tools/r13_anglais.py
755 tools/routeur.py
  ```

- **bash** `{"command": "chmod 755 tools/r13_anglais.py; stat -c '%a %n' tools/r13_anglais.py; python3 -m py_compile tools/r13_anglais.py tools/routeur.py tools/verifie_backlog.py && echo \"compile ok\"", "description": "Fix permissions and compile check"}`

  ```
755 tools/r13_anglais.py
compile ok
  ```

- **bash** `{"command": "tail -8 /tmp/passe-cloture.log; date", "description": "Check gate pass progress"}`

  ```
=== PASSE COMPLÈTE DES PORTES (78 portes, borne 1800 s) ===
    journaux : /tmp/portes-cloture-2156
  porte-adaptateur-sortie ✅                          65 s    ✅ porte tenue (écriture fidèle · invariant · effet · refus)
ven 30 oct 2026 22:00:50 EDT
  ```

- **bash** `{"command": "grep -n \"session\\|Session\" docs/methode/continuite.md | head -30; wc -l docs/methode/continuite.md", "description": "Check continuity doc for session references"}`

  ```
52:**Un seul écrivain par fichier** : la session qui clôt garde l'état, la roadmap et les directives ; le sous-agent
72:La session **vérifie** (porte, lien, contrôle), **met à jour `en-cours`**, **commite** et
87:| **écriture** | toute session écrit `en-cours`, **une à la fois** ; aucun fait (`reports/`, roadmap, backlog) ne se commite sans sa ligne (hook `pre-commit`) |
88:| **sessions actives** | une sous-section par session : Id, rôle, action, autres sessions, prochaine action, bloquants, journal ; le rôle nomme le chantier |
89:| **plan** | `journal/sessions/<id>/plan.md` |
95:**Lecture** : `AGENTS.md` + `en-cours` (« Sessions en cours », « Les chantiers et leurs bloquants »,
98:**Écriture** : toute session écrit `en-cours`, **une à la fois** ; aucun fait (`reports/`, roadmap,
106:- **« Sessions en cours »** : une sous-section par session active, avec ses sept champs (Id, rôle, action,
107:  autres sessions, prochaine action, bloquants, journal) ;
113:**Sessions terminées** : archivées dans `journal/sessions/<id>/rapport.md`, elles **sortent** d'`en-cours` ;
117:Le journal ne se lit que pour le **récit** d'une journée ; chaque rapport de session renvoie à son jour,
118:à l'inde
… [540 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('docs/pilotage/backlog/dependances.md'); s=p.read_text()\ns=s.replace(\"## 6. Les priorités (arrêtées le 2026-10-29)\",\n            \"## 6. Les priorités (instantané du 2026-10-29 ; la frontière vivante est § 5)\")\np.write_text(s)\np … [76 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "grep -n \"| R41 \\|| R42 \\|| R43 \\|| R44 \" docs/pilotage/backlog/index.md; echo ---; grep -n \"| \\*\\*R41\\*\\*\\| \\*\\*R42\\*\\*\\| \\*\\*R43\\*\\*\\| \\*\\*R44\\*\\*\" docs/pilotage/backlog/dependances.md", "description": "Check R41-R44 statuses"}`

  ```
64:| R41 | [Bloc tableaux](R41-bloc-tableaux.md) | mesurée | P2 | R01 | R4.1 |
65:| R42 | [Bloc code (AST, exécution)](R42-bloc-code.md) | mesurée | P2 | R01 | R4.2 |
66:| R43 | [Bloc maths](R43-bloc-maths.md) | mesurée | P3 | R01 | R4.3 |
67:| R44 | [Encodeur visuel / OCR](R44-encodeur-visuel.md) | bloquée | P3 | R41, R42, R43 | R4.4 |
---
110:| **R41** | mesurée | R01 (dure) | — | R44 | [R41-bloc-tableaux.md](R41-bloc-tableaux.md) |
111:| **R42** | mesurée | R01 (dure) | — | R44 | [R42-bloc-code.md](R42-bloc-code.md) |
112:| **R43** | mesurée | R01 (dure) | — | R44 | [R43-bloc-maths.md](R43-bloc-maths.md) |
113:| **R44** | bloquée | R41 (dure), R42 (dure), R43 (dure) | bloqué : aucun OCR installé (ni tesseract ni pytesseract) | — | [R44-encodeur-visuel.md](R44-encodeur-visuel.md) |
168:ressource externe nommée ; **R44** est bloqué par l'absence d'OCR ; `B10.3` attend un **encodeur
  ```

- **todo_write** `{"todos": [{"content": "Nettoyer les artefacts parasites (JSON au nom glob, fichier =)", "status": "completed"}, {"content": "R0.5 — re-générer le JSON avec toutes les AUC, réécrire la fiche sur le corpus gelé", "status": "completed"}, {"content": "R0.4 — documenter la réplication v4 (corpus gelé) e … [453 caractères tronqués]`

  ```
Updated todo list: 0 pending, 1 in progress, 6 completed.
  ```

- **bash** `{"command": "tail -6 /tmp/passe-cloture.log; date", "description": "Check gates progress"}`

  ```
porte-audit-drapeaux   ✅                         171 s  ✅ porte audit des drapeaux : occupation, ratio de signes et densité de croissance — chacun
  porte-b1110-hybride    ✅                           0 s  PORTE TENUE : 4/4 routées · 4/4 lues · E4 = requête de case
  porte-balayage         ✅                           0 s  ✅ porte balayage verte
  porte-bloc-code        ✅                           9 s  ✅ porte bloc code verte
  porte-bloc-maths       ✅                           1 s  ✅ porte bloc maths verte
  porte-bloc-tableaux    ✅                           2 s  ✅ porte bloc tableaux verte
ven 30 oct 2026 22:01:15 EDT
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -4; python3 tools/taille_documents.py 2>&1 | tail -3", "description": "Re-run doc review and size check"}`

  ```
revue de documentation · 367 fiche(s) · 435 JSON · 109 doc(s) · 78 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
     · 14 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 597 l. rapport-e5-distillation.md, 546 l. rapport-empreinte-memoire.md, 491 l. rapport-passe-k3-disque.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ```

- **bash** `{"command": "sed -n '1,60p' tools/verifie_etat_a_jour.py", "description": "Read state freshness checker"}`

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
… [1326 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/r07-routeur.json'))\nL=d['lignes']\nprint(len(L), len({(r['document'],r['question'],r['or']) for r in L}))\nprint(set(r['banc'] for r in L), d['date'])\nprint(json.dumps({k:d[k] for k in ['questions','differes','differes_extracti … [101 caractères tronqués]`

  ```
331 331
{'paraphrase', 'lexical'} 2026-10-30
{"questions": 331, "differes": 203, "differes_extractif": 176, "auc_signal": 0.839, "aucs": {"signal": 0.839, "z": 0.793, "ratio": 0.727, "etendue": 0.265, "couverture": 0.584, "longueur": 0.453, "aleatoire": 0.51}}
  ```

- **bash** `{"command": "tail -12 /tmp/passe-cloture.log; date", "description": "Check gates progress"}`

  ```
=== PASSE COMPLÈTE DES PORTES (78 portes, borne 1800 s) ===
    journaux : /tmp/portes-cloture-2156
  porte-adaptateur-sortie ✅                          65 s    ✅ porte tenue (écriture fidèle · invariant · effet · refus)
  porte-audit-drapeaux   ✅                         171 s  ✅ porte audit des drapeaux : occupation, ratio de signes et densité de croissance — chacun
  porte-b1110-hybride    ✅                           0 s  PORTE TENUE : 4/4 routées · 4/4 lues · E4 = requête de case
  porte-balayage         ✅                           0 s  ✅ porte balayage verte
  porte-bloc-code        ✅                           9 s  ✅ porte bloc code verte
  porte-bloc-maths       ✅                           1 s  ✅ porte bloc maths verte
  porte-bloc-tableaux    ✅                           2 s  ✅ porte bloc tableaux verte
ven 30 oct 2026 22:01:35 EDT
  ```

- **job_output** `{"job_id": "bash-122", "wait": true, "timeout_ms": 600000}`
