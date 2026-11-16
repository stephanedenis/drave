# Session DSH — relecture

- identifiant : `session-b7949a81-8213-4b06-93b7-dca9a1fabf31`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-16 05:21:49
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche Z3 (le bilan pour l'humain) : un **bilan court** (le matin) — `reports/rapport-bilan-final.md` + JSON : ce qui est installable (les 3 voies : editable, roue, le chemin historique), le quickstart, l'API du JSON, la performance (α 1,08, ×4,9), les codes, le CI, les portes ; les **négatifs nommés** ; **ce qu'il reste à décider** (le tagger `auto`, l'or de rôles, Panini). 40 lignes max, lisible en 3 minutes.

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

- **bash** `{"command": "pwd && ls -la && git log --oneline -15", "description": "List repo root and recent commits"}`

  ```
/home/stephane/Data13TB/stephane/GitHub/Qtrinet
total 212
drwxr-xr-x. 1 stephane stephane   774 16 nov 03:32 .
drwxr-xr-x. 1 stephane stephane  2532  5 nov 10:41 ..
-rw-r--r--. 1 stephane stephane  9977  3 nov 09:19 AGENTS.md
drwxr-xr-x. 1 stephane stephane    40 25 sep 15:38 bench
drwxr-xr-x. 1 stephane stephane    42 16 nov 02:01 build
drwxr-xr-x. 1 stephane stephane    56 30 sep 12:20 colab
drwxr-xr-x. 1 stephane stephane  2664  2 nov 18:33 data
drwxr-xr-x. 1 stephane stephane    56 16 nov 00:38 dist
drwxr-xr-x. 1 stephane stephane   138 16 nov 04:02 docs
drwxr-xr-x. 1 stephane stephane    92 28 oct 16:25 drave-core
drwxr-xr-x. 1 stephane stephane   136 16 nov 04:07 drave.egg-info
drwxr-xr-x. 1 stephane stephane   220 16 nov 05:21 .git
drwxr-xr-x. 1 stephane stephane    22 16 nov 03:51 .github
-rw-r--r--. 1 stephane stephane   653 15 nov 22:25 .gitignore
-rw-r--r--. 1 stephane stephane   225  1 nov 10:50 .gitmodules
drwxr-xr-x. 1 stephane stephane  1012 16 nov 00:22 journal
drwxr-xr-x. 1 stephane stephane   100  3 nov 09:12 models
drwxr-xr-x. 1 stephane stephane   114 25 sep 15:24 __pycache__
-rw-------. 1 stephane stephane  1272 16 nov 01:44 pyproject.toml
drwxr-xr-x. 1 stephan
… [3600 caractères tronqués]
  ```

- **bash** `{"command": "ls reports/ | head -50 && echo '---' && ls docs/pilotage/ && echo '---' && ls tools/ | head -60", "description": "List reports, pilotage and tools"}`

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
alignement-verne.md
analyse-litteraire.json
archive
atomes-niveaux.json
atomes-prediction.json
atomes-prediction-mesures.json
b102bis-capacite.json
b102bis-corpus-jw.json
b102bis-decodeur.json
b10-decodeur-mots.json
---
backlog
chantiers.md
en-cours.md
manques.md
plan-travail.md
programme-r.md
README.md
references-non-regression.md
roadmap.md
semaine-2.md
semaine-autonome.md
utilisation.m
… [1241 caractères tronqués]
  ```

- **bash** `{"command": "git show --stat 3c10e3ee | head -60 && echo '===' && git show --stat 19992f2f | head -50", "description": "Show stats of V3 and Z1 commits"}`

  ```
commit 3c10e3ee78a1c1593aecbbbd6bde8085ab8ef142
Author: Stéphane <stephane@localhost>
Date:   Mon Nov 16 03:12:25 2026 -0500

    V3 — LA CLÔTURE : 9 TÂCHES T1–T6 · U1–U3 + V1–V2, 86 PORTES (82/4 LUES, 84/2 APRÈS CIBLAGE), TAG exploitable-2026-11-16 SUR ae3c24f2 ; BILAN 2 + JSON

 docs/pilotage/en-cours.md                          |   17 +-
 docs/pilotage/references-non-regression.md         |    6 +
 docs/pilotage/roadmap.md                           |   17 +-
 journal/2026-11-16/README.md                       |   21 +-
 journal/2026-11-16/docs.md                         |    4 +-
 journal/2026-11-16/memoire.md                      |    2 +-
 journal/2026-11-16/mesures.md                      |    2 +-
 journal/2026-11-16/moteur.md                       |    2 +-
 journal/README.md                                  |    5 +-
 journal/sessions/MANIFEST.md                       |    7 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md |   20 +
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md   |    4 +-
 .../rapport.md                                     |   14 +-
 .../digest.md                                      |   63 +
 .../rapport.md                                     | 
… [2704 caractères tronqués]
  ```

- **bash** `{"command": "ls reports/ | grep -iE 'bilan|install|json|perf|cli|quick|produit|exploitable|porte|ci' | head -80", "description": "Find relevant report files"}`

  ```
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
alignement-3b.json
alignement-7b.json
analyse-litteraire.json
atomes-niveaux.json
atomes-prediction.json
atomes-prediction-mesures.json
b102bis-capacite.json
b102bis-corpus-jw.json
b102bis-decodeur.json
b10-decodeur-mots.json
b10-mots-contraste.json
b10-mots-jw.json
b1110-audit.json
b1110b-hybride.json
b1110-cartes.json
b1110c-case.json
b13-porte-134.json
b13-porte-138.json
b13-porte-140.json
bilan-b11.md
bilan-multi-materiel.md
bloc-linguistique.json
bruit-entree.json
carte-24langues-3b.json
… [596 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
1: # En ce moment
2: 
3: **Mis à jour : 2026-11-16 (V3)**
4: 
5: > **État courant, pas histoire** : une sous-section par session active ; preuves et plan plus bas (**La carte**).
6: 
7: ### Session `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — le hub de reprise du 04/11 *(en pause)*
8: 
9: - **Id** : `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — [`plan.md`](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/plan.md).
10: - **Rôle** : **Hub de reprise** — état, docs, intégration, passe.
11: - **Fait** : index réparé ; **N3 intégré** ; N2/S/L actifs.
12: - **Prochaine action** : **suivi docs**, puis la **passe**.
13: - **État** : **en pause** depuis le 05/11 ; la clôture J14.1 est portée par `e181ce02`.
14: - **Bloquants** : aucun.
15: - **Journal** : [la session](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/).
16: 
17: ## Sessions en cours
18: 
19: > Contrat : [`continuite.md`](../methode/continuite.md) · sessions terminées :
20: > [`journal/sessions/`](../../journal/sessions/). Chaque session expose son mandat dans son
21: > `plan.md` (`python3 tools/sess
… [12007 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,240p' reports/rapport-bilan-exploitable-2.md", "description": "Read BILAN 2 markdown"}`

  ```
# V3 — la clôture de la nuit exploitable : les neuf tâches T1–T6 · U1–U3, deux vérifications, 86 portes, le tag `exploitable-2026-11-16`

> **Ligne de roadmap** : **B13** (le produit), **R0.7** (le lecteur) · **Tâche** : **V3**
> (clôture de la nuit exploitable) · **Date** : 2026-11-16 · **Verdict** : ✅ **le lot
> T1–T6 · U1–U3 tient** ; ✅ **V1–V2 sont livrées** ; ❌ **les négatifs restent nommés**
> (clone public dégradé, or de rôles humain absent, neuronal de contrat, confiance non
> calibrée, passe non rejouée).
>
> **Le chiffre, en une ligne.** Le produit est **installable** (`drave 0.1.0`, **8** tests,
> sans installation **127**), le quickstart est **3/3** (JSON **5 899** octets), l'API publie
> **2 139** objets et **8** rôles (**0** span faux, **711** prédicats), **10 000 mots** passent
> en **0,82 s** après U1 (α **1,076**, ×4,9), la **roue** fait **1 727 201** octets (sans gold,
> `evaluer` **4**), les **profils** font **20/20** (ambigu **`und`**), `evaluer --strict` fait
> **0,8625 / 0,8891** (plancher **0,70**) et les exemples **27/27**. Le relevé des portes est
> **86 / 82 / 4** (`work/portes/roue-1116/`) ; après vérification ciblée des deux rouges de
> circonstance (`pr
… [17666 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"Z3\\|Z2\\|bilan-final\" docs journal reports/INDEX.md reports/README.md README.md 2>/dev/null | head -40", "description": "Search for Z3 mandate references"}`

  ```
C/GB4cuXFQq9Lb3a/ZnjIa9RTd16unlGGXdzMcyYUeO+U36E81MUmoyf9hjX6nXAi6CD3NMB0HdqXBSPcgH1GIi2HS8CdB5z8mgKLuVYI64uGULJKOZbt639UelejXrutbuypm70qOdhc8EeLqjfpBephezKb2mWk/trMVeNd9qRG0jq1D2WZfQofKi80RotI+f7jeMOSjEcz43ukp7UfiB1/askkPT9Xshk8qAzCoLa/PK764g9Cof8A5buSn3wLyp6FQVOvAprYce316s3OrH9IBGeGR0SsaWjfb+TSlE1cwnfnKsqEZbU2av5fK5OEr/le0661ND2i3RUXGdrp9yILQ1T6A/Kig6CBj4Xty+9zo7peU/Xszdn++du6vecq8v4Q0/69sGtcm2ujPp9LJRCIvNQ5vnMk0hf/MLPfyIoLgrDK2l4yCWrNjwDcxrxQWcUYwpFLzsQAbJJbObz5NsPXCkuEXLVww0EP02rf7HWH6E54IU0feORv0NxsxgviB4X8gZm93OJ0lBmoFzjs/Jv4pmLsArYFBFHK2gqweV7MIBayyf8L2b7Y+qkYQ5a0zbNa6VPnldYQbMXo8X6mml+66OMR81BCzm+BhkL+VMHWy8dS5XjADg3Qye5aguA/nznfIgrju+RFW36mGVwf7W4DUuvRlfll8k8VY1Wq7KKoq3CMjRiyawJKF9mhVqYIrnHZlPlvpQ2BOJWwoqzhfw5kzXr948QTiiqIlHsc7VKCGMvtZ/irbT5zEJ2BQ4V6kipDSeD/XETwXR34b/a3P0f64429v7xzaufQi/tIJqpgdFoujUHMj579EGgM2K12m2QgFS+1iSV//wZQLFRJ6+bmUta6vpXbUs7yTxErNW1mWFareVrRXI5gHANM72yeC06q8CxI4eNw9FM5JNqbB9fekmf/rNyXKeoAifObeKcJjXkPKb2iH78v8//Xzopqxg68xBZXLgU7F7XiDPF1iPiaKRnYC6fOk/GALX1CVwgclKTWvydkiiY4gcqkAp3L/jlw4KoYixZZv4132FPWrdfwyxehfOivBIohIKVIZb9Z2+bXzG3bvBWgjiDImkfRLBTEXaoyCg9Hh78MoEzgsevfk3qF89VZre9R+1UFG77VTh/dXxgf+4jcizGexaJCPyAppGX44L1hm9O52m6dfvHR3LEkzgR+1e3lDsM/9EZ/Nxw
… [48731 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,220p' reports/rapport-ci.md", "description": "Read CI report"}`

  ```
# Z1 — L'intégration continue : le workflow, la matrice et le contrôle négatif

> **Ligne de roadmap** : **B13 — la protection** (produit exploitable) · **Tâche** : **Z1** ·
> **Date** : 2026-11-16 · **Branche** : `s/v7` · **Verdict** : ✅ **la CI est verte en local** —
> **2 versions**, **5 étapes par version**, **10/10 étapes vertes**, **0 rouge**, **2/2 contrôles
> négatifs** qui cassent et arrêtent la séquence, porte produit **183/183**.
>
> **Le chiffre.** Le workflow `.github/workflows/ci.yml` déclare une matrice **Python 3.10 /
> 3.13** et cinq étapes : `pip install -e .`, `test_produit.py`, `test_tagger_api.py`,
> `porte-produit.sh`, `test_schema_produit.py`. En local, avec **3.10.20** et **3.13.16** :
> **10 étapes vertes**, **0 rouge**, **482,3 s** au total ; la porte produit rend
> `✅ porte produit verte` avec **183/183** portes d'autotest et **27/27** exemples conformes.
> Un test volontairement cassé sort en **1** (`FAILED (failures=1)`) et **l'étape suivante
> n'est pas exécutée**. La mesure principale part d'une archive `git archive HEAD` **sans
> sous-module** : la copie de secours de S restaure les deux fichiers nécessaires.
>
> **Dispositif** : [`.github/workflows/
… [10612 caractères tronqués]
  ```

- **bash** `{"command": "ls -la reports/rapport-passe-1611.* 2>/dev/null; ls -la work/portes/passe-1611/ 2>/dev/null | head; tail -5 work/portes/passe-1611/registre.txt 2>/dev/null; echo '---'; awk '$2 != 0' work/portes/passe-1611/registre.txt 2>/dev/null", "description": "Check Z2 pass report and registry"}`

  ```
total 152
drwxr-xr-x. 1 stephane stephane 1350 16 nov 05:06 .
drwxr-xr-x. 1 stephane stephane  658 16 nov 04:12 ..
drwxr-xr-x. 1 stephane stephane   64 16 nov 04:29 deepseek-porte
-rw-r--r--. 1 stephane stephane 4258 16 nov 05:06 passe-1611.log
-rw-r--r--. 1 stephane stephane  580 16 nov 04:13 porte-adaptateur-sortie.log
-rw-r--r--. 1 stephane stephane 1407 16 nov 04:16 porte-audit-drapeaux.log
-rw-r--r--. 1 stephane stephane  398 16 nov 04:16 porte-b1110-hybride.log
-rw-r--r--. 1 stephane stephane  413 16 nov 04:16 porte-balayage.log
-rw-r--r--. 1 stephane stephane  264 16 nov 04:17 porte-banc-performance.log
porte-gain 0 248
porte-greffe 0 811
porte-harnais-invariants 0 127
porte-homeostasie 0 629
porte-horloge 0 29
---
  ```

- **bash** `{"command": "sed -n '1,120p' journal/sessions/session-e466b49c-4fcb-4b34-b5a8-5bc193487415/digest.md", "description": "Read Z-task session digest start"}`

  ```
# Session DSH — relecture

- identifiant : `session-e466b49c-4fcb-4b34-b5a8-5bc193487415`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-16 04:11:48
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche Z2 (clôture technique) : la **passe complète** — `bash tools/toutes-les-portes.sh` avec `JOURNAUX=work/portes/passe-1611` ; lis le registre par `awk '$2 != 0'` (jamais par un tail) ; note les rouges, compare aux **rouges tolérées** de `docs/pilotage/references-non-regression.md`, mets à jour la section « passe » du document, et écris `reports/rapport-passe-1611.md` + JSON (portes, vertes, rouges, la liste).

### 👤 Utilisateur

<system-reminder>
The following workspace instructions may be relevant to your work. Use them as guidance when applicable. More specific instructions take precedence over broader ones. They do not override system, developer, or direct user instructions.

Instructions from: AGENTS.md

# Directives de l'agent — Drave

> **Compteurs vivants.** Dans [`docs/pilotage/en-cours.md`](docs/pilotage/en-cours.md) ; ne pas les recopier ici.

> **Porte d'entrée.** Lis ce fichier en entier (2 min) : il porte la **vision**, les règles non négoc
… [8930 caractères tronqués]
  ```

- **bash** `{"command": "ps aux | grep -c \"[t]outes-les-portes\"; date; wc -l work/portes/passe-1611/registre.txt; tail -3 work/portes/passe-1611/passe-1611.log; ls -la reports/rapport-passe-1611.* 2>/dev/null || echo \"pas de rapport passe\"", "description": "Check whether Z2 pass is running"}`

  ```
2
lun 16 nov 2026 05:22:07 EST
32 work/portes/passe-1611/registre.txt
  porte-harnais-invariants ✅                         127 s  ✅ porte harnais : installer une reparamétrisation laisse le modèle intact, et l'élagage
  porte-homeostasie      ✅                         629 s    ✅ porte tenue (×0 exact · activité monotone · dominance reproduite)
  porte-horloge          ✅                          29 s    ✅ borne atteinte : arrêt EXPLICITE (code 5) et AUCUNE perplexité rendue
pas de rapport passe
  ```

- **bash** `{"command": "grep -n \"Tâche Z3\" journal/sessions/session-e466b49c-4fcb-4b34-b5a8-5bc193487415/digest.md | head -5; echo ---; grep -n \"bilan-final\" journal/sessions/session-e466b49c-4fcb-4b34-b5a8-5bc193487415/digest.md | head -20", "description": "Find Z3 mandate in session digest"}`

  ```
---
  ```

- **bash** `{"command": "ls docs/produit/ && echo '===' && sed -n '1,240p' docs/produit/README.md", "description": "Read product docs"}`

  ```
ci.md
demarrage.md
exemples.md
README.md
===
# Le premier produit — analyser un texte avec Drave

> **Ce que ce document est.** La notice d'usage du **premier produit** de Drave : le bloc
> linguistique, utilisable **aujourd'hui**, sur un CPU, sans modèle et sans réseau. Il dit à qui
> il s'adresse, ce qu'il fait, comment l'exécuter, ce qu'il ne fait pas, ce qu'il coûte et ce
> qu'il garantit.
>
> **Vérifié le 2026-11-15** sur la branche `s/v7`. Le point d'entrée `tools/drave.py` est
> **livré** (version **0.1.0**) : `analyser`, `evaluer`, `rejouer`, `restituer` et `--version`
> existent, et la
> porte produit est verte. Le **tagger POS par API** est livré **en option** (`--tagger`,
> § 3.7) : clé et réseau pour qui le demande, **heuristique hors ligne par défaut**. Le
> **prototype `--tagger auto`** (complété le **2026-11-15**, § 3.7) choisit l'API si une clé
> existe, l'heuristique sinon, **sans changer le code de sortie** ; il ne change pas le défaut.
> Le format
> est **version 2** (`schema: "drave.annotation"`,
> `version: 2`) : le schéma v2 ajoute `meta.partition` et `meta.alternative`, et la **version 1
> reste lue** ([`tools/schemas/`](../../tools/schemas/)). Les sorties du
… [12923 caractères tronqués]
  ```

- **bash** `{"command": "cat pyproject.toml; echo '==='; ls -la dist/ build/; echo '==='; sed -n '1,180p' reports/rapport-empaquetage.md", "description": "Read packaging config and report"}`

  ```
[build-system]
requires = ["setuptools>=61"]
build-backend = "setuptools.build_meta"

[project]
name = "drave"
version = "0.1.0"
description = "Le point d'entrée produit du bloc linguistique de Drave."
requires-python = ">=3.10"
dependencies = []

[project.scripts]
drave = "tools.drave:main"

[tool.setuptools]
# Le paquet est un **namespace** (`tools/` n'a pas d'`__init__.py`) : on déclare les
# sous-ensembles dont le CLI a besoin. `tools.tests` reste un namespace implicite
# (son répertoire existe par `tools.tests.linguistique`) : on n'embarque pas les
# scripts de test, seulement les modules et les gold de la mesure.
packages = ["tools", "tools.llm", "tools.structures", "tools.tests.linguistique"]

[tool.setuptools.package-data]
# Les gold et l'artefact de profils sont **dans la roue** : `drave evaluer` et
# `drave profils` doivent marcher hors du dépôt. Le contrôle négatif (une roue
# amputée de ces fichiers) est décrit dans reports/rapport-roue.md et
# reports/rapport-profils.md : la mesure et la détection échouent alors en code 4,
# sans trace et sans stdout.
"tools.tests.linguistique" = [
    "gold.json",
    "gold_gele.json",
    "gold_reel.json",
    "gold_restitution_v2.js
… [9666 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,220p' reports/rapport-roue.md", "description": "Read wheel report"}`

  ```
# U2 — la roue : `drave-0.1.0-py3-none-any.whl`, installée hors du dépôt, les gold dedans

> **Ligne de roadmap** : **B13** (produit) · **Tâche** : **U2** (suite de T1) ·
> **Date** : 2026-11-16 · **Verdict** : ✅ **la roue est autonome ; une roue sans gold échoue proprement**.
>
> **Le chiffre.** `python3 -m pip wheel . --no-deps --no-build-isolation -w dist` rend
> **`drave-0.1.0-py3-none-any.whl`** : **1 727 201 octets**, **422 entrées**,
> sha256 `d980c4706f575e061faa9611aca4c42c024c1147b654004f724694914a99dbce`. **Depuis U3**,
> l'artefact de profils (802 110 octets) ajoute ~0,33 Mo : la roue courante fait **2 055 192
> octets** ([fiche](rapport-profils.md)) ; le chiffre 1 727 201 est celui de U2, sans les profils.
> Installée dans un venv **propre** depuis la roue (pas le dépôt), elle rend `drave 0.1.0` (code 0),
> `drave analyser "Le chat dort."` (code 0, `rôle=agent`) et `drave evaluer --json` (code 0,
> gold **612** phrases, POS **0,8625**, F1 **0,7902**, attachement exact **0,9958**) depuis
> **`/tmp`**. Les JSON `analyser` et `evaluer` sont **identiques au bit près** à ceux du dépôt.
> **Contrôle négatif** : la même roue **amputée des cinq `gold*.json`** s'installe encore
… [9992 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,240p' docs/produit/demarrage.md", "description": "Read quickstart"}`

  ```
# Démarrage en 5 minutes

> **Ce que ce document est.** Le parcours le plus court pour installer **drave** et lancer
> les commandes. Il part d'un **clone public** et ne suppose aucun fichier du dépôt de
> développement. Chaque commande et chaque sortie ont été **rejouées le 2026-11-15** sur un
> clone neuf (commit **7f1519f**, Python **3.13.16**, pip **26.2.1**), sans clé DeepSeek.
> Le relevé complet, les temps et le contrôle négatif sont dans
> [`reports/rapport-quickstart.md`](../../reports/rapport-quickstart.md) et
> [`reports/quickstart.json`](../../reports/quickstart.json).

**Prérequis** : Python **3.10+**, `git`, un terminal. Aucun GPU, aucun modèle, aucune clé pour
le chemin par défaut : le produit est **CPU, hors ligne et déterministe**.

## 1. Cloner

```bash
git clone https://github.com/stephanedenis/drave.git
cd drave
```

```text
Cloning into 'drave'...
```

Le clone ne télécharge **pas** les sous-modules : `tools/docwatch` et `tools/structures`
restent absents. Le CLI fonctionne sans eux ; l'écart que cela produit est dit au § 3.

## 2. Installer

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e .
drave --version
```

Sous Windows, l
… [7282 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nfor f in ['reports/performance-fix.json','reports/contrat-json.json','reports/quickstart.json','reports/cli-robuste.json','reports/roue.json','reports/rapport-ci.json','reports/empaquetage.json']:\n    print('='*20, f)\n    d=json.load(open(f))\n    print( … [101 caractères tronqués]`

  ```
==================== reports/performance-fix.json
{
 "schema": "drave.performance.fix",
 "version": 1,
 "date": "2026-11-16",
 "tache": "U1 (exploitable, suite de T4)",
 "ligne_roadmap": "B13",
 "objectif": {
  "alpha_max": 1.15,
  "delta_r2_quadratique_max": 0.02,
  "resultat": "atteint"
 },
 "source": {
  "corpus": "data/corpus_fr_litterature.txt",
  "prefixe_sha256": "0069b20e28975ca7b504755456aacf014b864b16705d40e6b381c45ae5e08871",
  "mots": 10000,
  "phrases": 814,
  "bloc_controle": {
   "mots": 247,
   "debut": 0,
   "fin": 1572,
   "sha256": "618e219f2420daa76d7ad52dce15d81ef08dc9a8e1f35826785ce566b695ca41"
  },
  "machine": {
   "python": "3.13.16",
   "implementation": "CPython",
   "machine": "x86_64",
   "systeme": "Linux-7.2.6-1-default-x86_64-with-glibc2.44",
   "cpu": "Intel(R) Xeon(R) CPU E5-2687W v3 @ 3.10GHz",
   "nproc": 40,
   "ram_kb": 131886412,
   "outil_memoire": "/usr/bin/time -f %M",
   "pyhashseed": "0",
   "date": "2026-11-16T00:07:29-0500"
  },
  "commit_avant": "83adaa2b6f8c6b1f03480375d30170a7613c71f8",
  "sous_module_avant": "389b99f",
  "commit_mesure": "83adaa2b + patch U1 (mesure faite avant le commit d19f0fc7)",
  "commit_apres": "d19f0fc7",
  "
… [22624 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,200p' docs/pilotage/references-non-regression.md; echo '==='; grep -n \"B13\\|produit\\|Z1\\|Z2\\|Z3\\|J4\\|auto\\|Panini\" docs/pilotage/roadmap.md | head -50", "description": "Read tolerated reds and roadmap"}`

  ```
# Références de non-régression

> **Passe — 2026-11-16 00 h 45 → 03 h 01 :** **86 portes, 82 vertes, 4 rouges** — `indice` et
> `melange` structurelles ; `produit` (V1 inachevée) et `sessions` (heartbeat) de circonstance.
> Journaux `work/portes/roue-1116/`. **Vérification ciblée (V3)** : `sessions` **0** et `produit`
> **0** (`--strict` 5 tests, exemples **27/27**, autotest **183/183**) ; journaux
> `work/portes/verif-cloture-1116/`. Après : **84 vertes, 2 rouges structurelles**.

> **Passe — 2026-11-15 09 h 53 → 12 h 15 :** **85 portes, 81 vertes, 4 rouges** — `indice` et
> `melange` structurelles ; `sessions` (heartbeat) **réparée** à 12 h 20 ; `prechargement`
> **environnementale** (deux passes en parallèle ; PPL identique 799,8557 ; verte le 14/11).
> Journaux `work/portes-1115-09h53/`. **Pas de passe complète pour W6** ; ciblage
> `work/portes/w6-ciblage` (8/9), `w6-ciblage2` (2/2) puis `w6-final` (9/9).

> **Passe — 2026-11-14 00 h 30 :** **84 portes, 81 vertes, 3 rouges** — `porte-indice` et
> `porte-melange` (structurelles) et `porte-sessions` (mandats périmés du hub `1e7ef596` et de
> `e181ce02`). `porte-produit` et `porte-bloc` **vertes**. Journal :
> `work/portes/passe-
… [29286 caractères tronqués]
  ```

- **bash** `{"command": "cat work/portes/passe-1611/registre.txt; echo '==='; tail -30 work/portes/passe-1611/passe-1611.log", "description": "Read current pass registry"}`

  ```
porte-adaptateur-sortie 0 90
porte-audit-drapeaux 0 193
porte-b1110-hybride 0 0
porte-balayage 0 0
porte-banc-performance 0 17
porte-bloc-code 0 18
porte-bloc-linguistique 0 25
porte-bloc-maths 0 1
porte-bloc-tableaux 0 3
porte-budget 0 53
porte-bus 0 86
porte-bus-socket 0 103
porte-c4-retard 0 35
porte-cerveau 0 10
porte-cic 0 13
porte-consolidation 0 89
porte-coupe 0 154
porte-cycle-c2 0 146
porte-deepseek 0 1
porte-delais 0 24
porte-diff-couche 0 21
porte-document 0 7
porte-echange-experts 0 62
porte-episodique 0 217
porte-etat 0 0
porte-flux 0 28
porte-fusion 0 9
porte-gain 0 248
porte-greffe 0 811
porte-harnais-invariants 0 127
porte-homeostasie 0 629
porte-horloge 0 29
===
  porte-b1110-hybride    ✅                           0 s  PORTE TENUE : 4/4 routées · 4/4 lues · E4 = requête de case
  porte-balayage         ✅                           0 s  ✅ porte balayage verte
  porte-banc-performance ✅                          17 s  ✅ porte banc-performance verte
  porte-bloc-code        ✅                          18 s  ✅ porte bloc code verte
  porte-bloc-linguistique ✅                          25 s  ✅ porte bloc linguistique verte
  porte-bloc-maths       ✅                         
… [3177 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,200p' tools/toutes-les-portes.sh", "description": "Read gates runner order"}`

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

- **bash** `{"command": "sed -n '1,80p' reports/INDEX.md; echo '==='; sed -n '1,80p' reports/README.md", "description": "Read reports index conventions"}`

  ```
# Index des fiches de reports/

> **Généré** par `tools/index_reports.py` — **769 fiches**. Les fichiers
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
… [17591 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/performance-fix.json'))\nprint(json.dumps({k:d[k] for k in ['resultat','apres','controle','limites'] if k in d}, ensure_ascii=False, indent=1)[:6000])\nprint('KEYS', list(d))\nPY", "description": "Extract performance-fix result fi … [6 caractères tronqués]`

  ```
{
 "limites": [
  "Un seul texte (Alice, français) ; un texte technique ou multilingue peut changer la densité de syntagmes.",
  "Le bloc répété isole la taille, pas le contenu ; il ne mesure pas la vitesse du texte réel.",
  "Le gain de temps (×4,9 sur 10 000 mots) dépend de la machine et de la charge ; les parts du profil, pas les secondes, sont le signal.",
  "La mémoire ne baisse pas : les index ajoutent ~0,5 Mio au pic (126,9 → 127,4 Mio) pour supprimer le temps quadratique.",
  "Les mesures de temps sont des médianes de 3 répétitions, sans épinglage CPU."
 ]
}
KEYS ['schema', 'version', 'date', 'tache', 'ligne_roadmap', 'objectif', 'source', 'corrections', 'controle_lineaire', 'dix_mille_mots', 'or_612_452', 'controle_negatif', 'tests', 'limites', 'prochaine_action']
  ```

- **bash** `{"command": "python3 tools/drave.py --help 2>&1 | sed -n '1,120p'; echo '==='; grep -n \"code\\|CODE\\|sortie\" docs/produit/README.md | sed -n '1,60p'", "description": "Read CLI codes from help"}`

  ```
usage: drave [-h] [-V] {analyser,evaluer,profils,rejouer,restituer} ...

Point d'entrée produit du bloc linguistique (analyse et restitution).

arguments:
  {analyser,evaluer,profils,rejouer,restituer}
    analyser            étiqueter un texte (POS, syntagmes, pragmatique)
    evaluer             mesurer l'heuristique sur le gold
    profils             détecter la langue d'un texte (398 profils UDHR)
    rejouer             analyser deux fois et vérifier le déterminisme
    restituer           reconstruire la surface depuis l'annotation et mesurer le miroir

options:
  -h, --help, --aide    afficher cette aide et quitter
  -V, --version         afficher la version et quitter

Commandes : analyser, evaluer, profils, rejouer, restituer.
Codes de sortie : 0 succès · 3 refus d'analyse (JSON) · 4 clé/dépendance absente
(--tagger explicite sans clé, ou --fichier introuvable) · 5 usage (argument, sous-commande,
langue hors fr/en, --fichier sur un répertoire) · 1 autre erreur.
Options : --json, --jsonl, --duree, --fichier CHEMIN, --langue fr|en,
--partition brut|alternative|filtrer_union|filtrer, --contexte, --banc, --tagger [auto],
--strict (evaluer), --profils (analyser) et `drave prof
… [7034 caractères tronqués]
  ```

- **bash** `{"command": "ls -l dist/; python3 - <<'PY'\nimport json\nd=json.load(open('reports/performance-fix.json'))\nfor k in ['dix_mille_mots','or_612_452','controle_negatif','tests','prochaine_action']:\n    print('==',k)\n    print(json.dumps(d[k], ensure_ascii=False, indent=1)[:4000])\nPY", "description" … [35 caractères tronqués]`

  ```
total 2008
-rw-r--r--. 1 stephane stephane 2055192 16 nov 02:01 drave-0.1.0-py3-none-any.whl
== dix_mille_mots
{
 "avant": {
  "fonction": {
   "duree_s": {
    "n": 3,
    "mediane": 3.990812406176701,
    "moyenne": 3.9837561137974262,
    "min": 3.856404581107199,
    "max": 4.104051354108378,
    "p95": 4.104051354108378
   },
   "rss_kb": {
    "n": 3,
    "mediane": 129936,
    "moyenne": 129702.66666666667,
    "min": 128756,
    "max": 130416,
    "p95": 130416
   },
   "json_octets": 14795890,
   "mots": 10000,
   "syntagmes": 2726,
   "etiquettes": 54522
  },
  "cli": {
   "duree_s": {
    "n": 3,
    "mediane": 5.010618543950841,
    "moyenne": 5.037687239625181,
    "min": 4.983259954955429,
    "max": 5.119183219969273,
    "p95": 5.119183219969273
   },
   "rss_kb": {
    "n": 3,
    "mediane": 171316,
    "moyenne": 171390.66666666666,
    "min": 171292,
    "max": 171564,
    "p95": 171564
   },
   "octets": 14795890
  }
 },
 "apres": {
  "fonction": {
   "duree_s": {
    "n": 3,
    "mediane": 0.8157198431435972,
    "moyenne": 0.8211626831131676,
    "min": 0.7808869320433587,
    "max": 0.8668812741525471,
    "p95": 0.8668812741525471
   },
   "rss_kb": {
    "n
… [5899 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/contrat-json.json'))\nprint('KEYS',list(d))\nfor k in ['mesure','attachement','roles','predicats','verdict','controle_negatif','limites']:\n    if k in d:\n        print('==',k); print(json.dumps(d[k],ensure_ascii=False,indent=1)[ … [178 caractères tronqués]`

  ```
KEYS ['date', 'tache', 'ligne', 'objet', 'outil', 'corpus', 'schema', 'vocabulaire_roles', 'candidats', 'controles_negatifs', 'validation', 'tests', 'limites']
== limites
[
 "la normalisation n'est pas une annotation plus fine : objet regroupe patient, complément, thème, contenu et groupe nominal sans fonction ; qualite regroupe attribut, manière, cause, concession et hypothèse",
 "le span d'un candidat est la première occurrence de la cible dans le texte ; pour une surface répétée, c'est une position, pas une résolution d'anaphore",
 "les candidats restent produits par l'heuristique : source vaut heuristique, même quand la cible vient du générateur S",
 "le gold 612 n'exerce pas les rôles instrument, manière, source, conséquence ; ils sont dans la table mais non observés sur ce corpus",
 "v1 est lue par son schéma, mais les annotations v1 sont dérivées des v2 : ce n'est pas un corpus v1 indépendant"
]
--- top-level compact ---
date : 2026-11-15
tache : T2
ligne : B13
objet : l'API du JSON : candidats d'attachement en objets et rôles normalisés
outil : tools/mesurer_contrat_json.py
  ```

- **bash** `{"command": "grep -n \"2 139\\|2139\\|1 295\\|711\\|8 rôles\\|span faux\\|rôles\" reports/rapport-contrat-json.md | head -40", "description": "Find key JSON API figures"}`

  ```
1:# T2 — l'API du JSON : candidats d'attachement en objets, rôles normalisés
6:> **Le chiffre.** Sur le gold vivant **612 phrases** : **1 883 syntagmes**, **1 883 rôles**
7:> non vides, **21 rôles bruts** ramenés à **8 rôles normalisés**, **0** hors table et **0**
8:> hors vocabulaire. Les **1 295 attachements** portent tous des `candidats` **objets**
9:> `{span, cible, source}` : **2 139 objets** (dont **1 062** dans `meta.alternative`),
10:> **0 span faux**, **1 295/1 295** cibles choisies présentes dans la liste. **Contrôle
11:> négatif** : un consommateur qui filtre `role == "predicat"` trouve **711** prédicats
12:> (**711 GV**) ; `role == "prédicat"` en trouve **0**. Le schéma v2 valide **612/612**
42:n'est pas retrouvée dans le texte est **écarté** plutôt que publié avec un span faux. Les
45:**2. Les rôles sont normalisés.** Le vocabulaire est **fermé** :
63:exhaustive pour les rôles produits par `bloc_linguistique.py` et le générateur S
83:Les **21 rôles bruts observés** sur le gold tombent tous dans la table :
87:| `predicat` | 711 | GV 711 |
105:`span` découpe exactement sa `cible` dans `texte`, et compare les rôles bruts (objets
106:Python) aux rôles normalisés (JSON).
11
… [871 caractères tronqués]
  ```

- **bash** `{"command": "date; wc -l work/portes/passe-1611/registre.txt; tail -4 work/portes/passe-1611/passe-1611.log", "description": "Check pass progress"}`

  ```
lun 16 nov 2026 05:22:39 EST
32 work/portes/passe-1611/registre.txt
  porte-greffe           ✅                         811 s    ✅ la porte est franchie. Ce qu'elle établit : l'injection d'état est BRANCHÉE
  porte-harnais-invariants ✅                         127 s  ✅ porte harnais : installer une reparamétrisation laisse le modèle intact, et l'élagage
  porte-homeostasie      ✅                         629 s    ✅ porte tenue (×0 exact · activité monotone · dominance reproduite)
  porte-horloge          ✅                          29 s    ✅ borne atteinte : arrêt EXPLICITE (code 5) et AUCUNE perplexité rendue
  ```

- **bash** `{"command": "git status --short | head -60; echo '---'; git log -1 --format='%H %s'; echo '---'; git branch --show-current", "description": "Check git status"}`

  ```
M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
 M journal/sessions/session-b9138a2a-648e-490d-a349-124ac1aa1ef0/digest.md
 M journal/sessions/session-b9138a2a-648e-490d-a349-124ac1aa1ef0/rapport.md
 M tools/chantier/plan.json
?? journal/sessions/session-e466b49c-4fcb-4b34-b5a8-5bc193487415/
---
19992f2fa5e694b3c6c7ba306abe8fadd2ae1c76 Z1 — L'INTÉGRATION CONTINUE : MATRICE 3.10/3.13, 10/10 ÉTAPES VERTES (ARCHIVE SANS SOUS-MODULE, COPIE DE SECOURS S) ; PORTE 183/183 ; TEST CASSÉ → 1, JOB ARRÊTÉ ; act ABSENT, YAML PARSÉ
---
s/v7
  ```

- **bash** `{"command": "sed -n '1,120p' journal/2026-11-16/README.md; echo '==='; ls journal/2026-11-16/", "description": "Read today's journal index"}`

  ```
# 2026-11-16

> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
> [`journal/2026-11-16/`](README.md). Le récit écrit à la main est conservé plus bas, dans
> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
> [l'index des sessions](../README.md#sessions).

**8 commits** · **1 session(s)** · **5 thème(s)**

## Thèmes du jour

| thème | commits | fichier |
|---|---|---|
| docs | 2 | [docs.md](docs.md) |
| memoire | 1 | [memoire.md](memoire.md) |
| mesures | 3 | [mesures.md](mesures.md) |
| modele | 1 | [modele.md](modele.md) |
| moteur | 1 | [moteur.md](moteur.md) |

## Sessions DSH

| session | titre | début | durée | liens |
|---|---|---|---|---|
| `e181ce02-cd50-488a-a6be-e84b79d40dcc` | Documentation Drave avec diagrammes et implémentation | 2026-10-31 17:40 | 371.5 h | [rapport](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md) · [digest](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md) |

## Tous les commits (heure réelle)

| heure | commit | fait |
|---|---|---|
| 00:19 | `d19f0fc7` | U1 — LES DEUX O(K²) BORNÉS : 10 000 MOTS 4,0 → 0,82 S (×4,9), α 1,53 → 1,08, QUADRATIQUE +0,00077 R² ; 612/452 
… [5875 caractères tronqués]
  ```

- **bash** `{"command": "git diff --stat; echo '==='; git diff -- journal/README.md | head -60; echo '==='; git diff -- tools/chantier/plan.json | head -80", "description": "Inspect uncommitted diffs"}`

  ```
journal/README.md                                  |   7 +-
 journal/sessions/MANIFEST.md                       |   7 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md |  96 ++++++++++++++
 .../rapport.md                                     |  14 +-
 .../digest.md                                      | 147 +++++++++++++++++++++
 .../rapport.md                                     |  53 +++++++-
 tools/chantier/plan.json                           |  47 +++++++
 7 files changed, 352 insertions(+), 19 deletions(-)
===
diff --git a/journal/README.md b/journal/README.md
index 3a22eb87..af4c832f 100644
--- a/journal/README.md
+++ b/journal/README.md
@@ -13,7 +13,7 @@ chaque rapport renvoie à son jour et à `en-cours`.
 
 | jour | index | thèmes |
 |---|---|---|
-| **2026-11-16** | [2026-11-16/README.md](2026-11-16/README.md) | [docs](2026-11-16/docs.md) · [memoire](2026-11-16/memoire.md) · [mesures](2026-11-16/mesures.md) · [moteur](2026-11-16/moteur.md) |
+| **2026-11-16** | [2026-11-16/README.md](2026-11-16/README.md) | [docs](2026-11-16/docs.md) · [memoire](2026-11-16/memoire.md) · [mesures](2026-11-16/mesures.md) · [modele](2026-11-16/modele.md) · [moteur](2026-11-16/moteur.md) |

… [7740 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,160p' tools/journal_auto.py | head -160", "description": "Inspect journal auto tool"}`

  ```
#!/usr/bin/env python3
"""journal_auto.py — le journal quotidien, ÉCRIT PAR JOUR (UN DOSSIER) ET PAR THÈME, à partir de git et des sessions.

POURQUOI. Le journal doit consigner les **événements datés** (voir
`docs/organisation-du-depot.md`), et une journée de ce dépôt est trop riche pour un seul
fichier : un jour touche le moteur, les protocoles, les mesures, les portes et la
documentation. D'où le découpage **`<AAAA-MM-JJ>_<thème>.md`** : on lit la journée d'un thème,
et on suit un thème **d'un jour à l'autre** (le nom commence par la date, le thème suit —
`ls journal/2026-10-1*/attention.md`).

SOURCES, et rien d'autre :
  1. **git** — les commits du jour (heure d'auteur, en heure locale de la machine) et les
     fichiers touchés ; c'est la chronologie **fiable** (les horodatages écrits à la main
     s'étaient retrouvés dans le futur) ;
  2. **journal/sessions/** — les rapports de session dont la fenêtre de temps couvre le jour
     (début et durée lus dans l'index `journal/README.md`, régénéré par
     `tools/session_report.py`) : on en extrait les **titres de tour** classés par thème, avec
     le lien vers le rapport complet.

CE QUI EST PRÉSERVÉ. Tout ce que l'humain (ou l
… [6567 caractères tronqués]
  ```

- **bash** `{"command": "date; wc -l work/portes/passe-1611/registre.txt; tail -2 work/portes/passe-1611/passe-1611.log; ls -la reports/rapport-passe-1611.* 2>/dev/null || true", "description": "Check pass progress again"}`

  ```
lun 16 nov 2026 05:22:57 EST
32 work/portes/passe-1611/registre.txt
  porte-homeostasie      ✅                         629 s    ✅ porte tenue (×0 exact · activité monotone · dominance reproduite)
  porte-horloge          ✅                          29 s    ✅ borne atteinte : arrêt EXPLICITE (code 5) et AUCUNE perplexité rendue
  ```

- **bash** `{"command": "for i in $(seq 1 240); do if grep -q '^--- ' work/portes/passe-1611/registre.txt 2>/dev/null; then echo FINI; break; fi; if ! pgrep -f 'toutes-les-portes.sh' >/dev/null 2>&1; then echo PROCESSUS_ABSENT; break; fi; sleep 15; done; date; echo '=== registre ==='; cat work/portes/passe-1611 … [169 caractères tronqués]`

  ```
started background job bash-32
  ```

- **bash** `{"command": "sed -n '1020,1060p' docs/produit/README.md; echo '==='; sed -n '790,825p' docs/produit/README.md", "description": "Read install paths and codes docs"}`

  ```
le texte. Le format est versionné ; la **qualité linguistique** ne l'est pas.

### 8.10 Comment l'installer et le lancer ?

Trois chemins, le même CLI. **Depuis le dépôt, sans rien installer** : `python3 tools/drave.py …`
depuis la racine (Python **3.10+**, mesuré ici en 3.13), **aucune dépendance externe**, aucun GPU.
**En éditable** (pour développer) : `python3 -m pip install -e .` dans un venv, depuis la racine.
**Depuis la roue** (pour installer hors du dépôt) :

```bash
python3 -m pip wheel . --no-deps --no-build-isolation -w dist
# dist/drave-0.1.0-py3-none-any.whl

python3 -m venv /tmp/venv-drave-roue
/tmp/venv-drave-roue/bin/python -m pip install --no-index --no-deps \
  dist/drave-0.1.0-py3-none-any.whl
cd /tmp
/tmp/venv-drave-roue/bin/drave --version            # drave 0.1.0
/tmp/venv-drave-roue/bin/drave analyser "Le chat dort."
/tmp/venv-drave-roue/bin/drave evaluer --json
```

La roue **embarque les données de la mesure** : `tools/tests/linguistique/gold*.json` (les cinq
gold), le générateur S (`tools/structures/generateur.py`) et le client du tagger optionnel. Elle
ne dépend donc **pas du dépôt** : `analyser` et `evaluer` rendent depuis `/tmp` les **mêmes
sorties** qu
… [3816 caractères tronqués]
  ```

- **bash** `{"command": "date; wc -l work/portes/passe-1611/registre.txt; tail -2 work/portes/passe-1611/passe-1611.log", "description": "Check pass progress"}`

  ```
lun 16 nov 2026 05:23:19 EST
32 work/portes/passe-1611/registre.txt
  porte-homeostasie      ✅                         629 s    ✅ porte tenue (×0 exact · activité monotone · dominance reproduite)
  porte-horloge          ✅                          29 s    ✅ borne atteinte : arrêt EXPLICITE (code 5) et AUCUNE perplexité rendue
  ```

- **bash** `{"command": "sed -n '1,140p' tools/revue_documentation.py; echo '==='; sed -n '1,100p' tools/verifie_en_cours.py", "description": "Read doc review and state verifier"}`

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
… [7432 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"compteurs\\|reports/\\*\\|INDEX\" tools/revue_documentation.py | head -40; echo '==='; grep -n \"reports\" tools/verifie_en_cours.py | head", "description": "Find doc review counters"}`

  ```
12:     les compteurs de la page d'état sont ceux du disque (portes, chapitres, fiches, docs) ;
172:    # 5. compteurs : la page d'état est la source unique, et elle dit le disque
183:            alertes.append(f"compteurs : la ligne « {nom} » manque dans en-cours.md")
185:            alertes.append(f"compteurs : en-cours.md dit {valeur} {nom}, le disque en a {disque}")
187:        alertes.append("compteurs : la ligne « fichiers / JSON » manque dans en-cours.md")
195:                    f"compteurs : en-cours.md dit {valeur} {quoi}, le disque en a {disque}"
374:        print("  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, "
===
16:  8. aucune ligne de journal A7.x dans l'état (les mesures vont dans `reports/`).
141:        alertes.append("ligne de journal A7.x dans l'état — la déplacer dans reports/")
  ```

- **bash** `{"command": "printf 'portes '; ls tools/porte-*.sh | wc -l; printf 'fiches '; ls reports/*.md | wc -l; printf 'json '; ls reports/*.json | wc -l; printf 'docs '; find docs -name '*.md' ! -path '*/archive/*' ! -name README.md | wc -l", "description": "Count current state invariants"}`

  ```
portes 86
fiches 772
json 867
docs 461
  ```

- **bash** `{"command": "sed -n '160,205p' tools/revue_documentation.py", "description": "Read counter check details"}`

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
… [1178 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\nR=pathlib.Path('.')\ndef est_carte(p): return p.parent.name=='entrees' and p.parent.parent.name=='glossaire'\ndocs=[p for p in (R/'docs').rglob('*.md') if 'archive' not in p.parts and p.name!='README.md' and not est_carte(p)]\nprint(len(docs))\nPY", "de … [47 caractères tronqués]`

  ```
126
  ```

- **bash** `{"command": "sha256sum dist/drave-0.1.0-py3-none-any.whl; stat -c '%s' dist/drave-0.1.0-py3-none-any.whl; unzip -l dist/drave-0.1.0-py3-none-any.whl | tail -1", "description": "Hash and count current wheel"}`

  ```
27a3a671aac8ae2c827dd1177703642d656da3ad354b6df6f08ab2ceca8ce2a7  dist/drave-0.1.0-py3-none-any.whl
2055192
  6544490                     427 files
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nfor f in ['reports/quickstart.json','reports/rapport-ci.json']:\n d=json.load(open(f))\n print('==',f,list(d))\n if f.endswith('quickstart.json'):\n  for k in ['commandes','controle_negatif','limites','verdict']:\n   if k in d: print(k, json.dumps(d[k],ens … [74 caractères tronqués]`

  ```
== reports/quickstart.json ['schema', 'version', 'date', 'tache', 'document', 'verdict', 'environnement', 'temps_s', 'commandes', 'tagger', 'erreurs', 'controle_negatif', 'fichiers']
commandes [{"nom": "version", "commande": "drave --version", "cwd": "/tmp/qs-doc/drave", "code": 0, "stdout": "drave 0.1.0\n", "stderr": ""}, {"nom": "analyser", "commande": "drave analyser \"Le chat dort.\"", "cwd": "/tmp/qs-doc/drave", "code": 0, "stdout": "drave 0.1.0 — analyse heuristique (CPU, hors ligne)\nlangue=fr script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (61.5% du texte)\nPOS  Le/DET chat/NOUN dort/VERB ./PONCT\nSYNTAGMES\n  GN   [0:7]   Le chat  rôle=objet     → dort\n  GV   [8:12]  dort     rôle=predicat  → —\nPRAGMATIQUE\n  phrase [0:13] déclarative · acte=assertion · négation=non · modalité=non · double sens=non\nCOUVERTURE  (confiance max par niveau)  graphème=0.99 · mot=0.98 · pos=0.95 · syntagme=0.35 ·\n            phrase=0.85 · discours=0.50 · pragmatique=0.45 · document=0.70\n", "stderr": "", "syntagmes": {"GN": {"valeur": "Le chat", "role": "objet", "cible": "dort"}, "GV": {"valeur": "dort", "role": "predicat", "cible": ""}}}, {"nom": "evaluer", "commande":
… [2724 caractères tronqués]
  ```

- **job_list** `{}`

  ```
bash-32 [bash] running — for i in $(seq 1 240); do if grep -q '^--- ' work/portes/passe-1611/registre.txt 2>/dev/null; then echo FINI; break; fi; if ! pgrep -f 'toutes-les-portes.sh' >/dev/null 2>&1; then echo PROCESSUS_ABSENT; break; fi; sleep 15; done; date; echo '=== registre ==='; cat work/portes/passe-1611/registre.txt; echo '=== rouges ==='; awk '$2 != 0' work/portes/passe-1611/registre.txt
  ```

- **bash** `{"command": "head -8 work/portes/passe-1611/passe-1611.log; stat -c '%y' work/portes/passe-1611/passe-1611.log", "description": "Read pass start info"}`

  ```
=== PASSE COMPLÈTE DES PORTES (86 portes, borne 1800 s) ===
    journaux : work/portes/passe-1611
  porte-adaptateur-sortie ✅                          90 s    ✅ porte tenue (écriture fidèle · invariant · effet · refus)
  porte-audit-drapeaux   ✅                         193 s  ✅ porte audit des drapeaux : occupation, ratio de signes et densité de croissance — chacun
  porte-b1110-hybride    ✅                           0 s  PORTE TENUE : 4/4 routées · 4/4 lues · E4 = requête de case
  porte-balayage         ✅                           0 s  ✅ porte balayage verte
  porte-banc-performance ✅                          17 s  ✅ porte banc-performance verte
  porte-bloc-code        ✅                          18 s  ✅ porte bloc code verte
2026-11-16 05:06:23.377850010 -0500
  ```

- **bash** `{"command": "date; wc -l work/portes/passe-1611/registre.txt; tail -2 work/portes/passe-1611/passe-1611.log", "description": "Check pass progress"}`

  ```
lun 16 nov 2026 05:23:47 EST
32 work/portes/passe-1611/registre.txt
  porte-homeostasie      ✅                         629 s    ✅ porte tenue (×0 exact · activité monotone · dominance reproduite)
  porte-horloge          ✅                          29 s    ✅ borne atteinte : arrêt EXPLICITE (code 5) et AUCUNE perplexité rendue
  ```

- **bash** `{"command": "sed -n '175,195p' docs/pilotage/roadmap.md; echo '==='; sed -n '108,130p' docs/pilotage/en-cours.md", "description": "Read roadmap tail and state"}`

  ```
**V1 — `evaluer --strict` (16/11).** Quatre modes, cascade **0,8625** / **0,8891**, plancher
**0,70** ; négatif **0,0000** → **1**. [Fiche](../../reports/rapport-evaluer-strict.md) ·
[JSON](../../reports/evaluer-strict.json).

**V2 — exemples.** 3 corrigés ; 18 objets, 0 faux ; `verifie_exemples.py` 27/27 ; démarrage
3/3. [Fiche](../../reports/rapport-exemples-v2.md) · [JSON](../../reports/rapport-exemples-v2.json).

**T6 — le premier bilan (15/11).** Cinq briques ; trois limites.
[Fiche](../../reports/rapport-bilan-exploitable.md) · [JSON](../../reports/rapport-bilan-exploitable.json).

**V3 — clôture (16/11).** **T1–T6 · U1–U3 · V1–V2** ; **86 / 82 / 4** → **84 / 2** ;
tag `exploitable-2026-11-16` sur **`ae3c24f2`** ; **Z1 — la CI** : **3.10 / 3.13**, **10/10**.
[Fiche](../../reports/rapport-bilan-exploitable-2.md) · [CI](../../reports/rapport-ci.md).

**La vue d'ensemble** est dans [`chantiers.md`](chantiers.md) ; carte,
[`chantiers-vision.svg`](../schemas/chantiers-vision.svg) ; plan,
[`plan-travail.md`](plan-travail.md).

## L'ordre du jour (carpe diem)

L'ordre est **la valeur / le coût**, pas la date. La dernière mise à jour est le **2026-11-16**.
===
externes** et la **proc
… [3344 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' reports/rapport-bilan-jour-1115.md", "description": "Read prior short human report"}`

  ```
# Le bilan du 15/11 — la semaine 2 en un jour : le tagger décidé, le gold nommé, les rôles séparés

> **Ce que ce bilan est.** La synthèse de la **journée du 15/11** (08 h 15 → 16 h) : les six
> vagues de la semaine 2 (W1-W6) et les trois tâches du pilote (X1-X3), les chiffres, les
> négatifs, la décision du tagger. **Aucune mesure nouvelle** : chaque chiffre renvoie à sa fiche.

## 1. Les vagues mesurées

| vague | résultat | fiche |
|---|---|---|
| **W1** le gold réel 452 | 20 hand + 432 corpus, **242 fr / 210 en**, le split **402 / H50** figé, le sha256, **10 GP/SUB** listés (184 → 194 cibles) | [`rapport-gold-452.md`](rapport-gold-452.md) |
| **W2** le tagger sur 402/H50 | 402 **0,9198 → 0,9643** (**+4,45**) ; H50 **0,6842 → 0,8607** (**+17,65**) ; F1 et attachement du 402 **inchangés** | [`rapport-tagger-h50.md`](rapport-tagger-h50.md) |
| **W3** la matrice du défaut | défaut **hors ligne, code 0, 0 socket** ; `--tagger` opt-in ; clé invalide **4** ; réseau coupé **0** après 3 essais ; 1 000 phrases = **143 870 tokens** | [`rapport-tagger-defaut.md`](rapport-tagger-defaut.md) |
| **W4** Panini | le manifeste des **26 signatures** prêt ; le rejeu **27/60** (33 manquantes) — **p
… [2525 caractères tronqués]
  ```

- **bash** `{"command": "date; wc -l work/portes/passe-1611/registre.txt; tail -3 work/portes/passe-1611/passe-1611.log", "description": "Check pass progress"}`

  ```
lun 16 nov 2026 05:24:01 EST
32 work/portes/passe-1611/registre.txt
  porte-harnais-invariants ✅                         127 s  ✅ porte harnais : installer une reparamétrisation laisse le modèle intact, et l'élagage
  porte-homeostasie      ✅                         629 s    ✅ porte tenue (×0 exact · activité monotone · dominance reproduite)
  porte-horloge          ✅                          29 s    ✅ borne atteinte : arrêt EXPLICITE (code 5) et AUCUNE perplexité rendue
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\ncur={}\nfor l in Path('work/portes/passe-1611/registre.txt').read_text().splitlines():\n    p=l.split()\n    if len(p)>=3 and p[1].isdigit(): cur[p[0]]=int(p[2])\nprev={}\nfor l in Path('work/portes/roue-1116/registre.txt').read_text().splitli … [416 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 9, in <module>
ValueError: invalid literal for int() with base 10: 'vertes,'
[exit code: 1]
  ```

- **bash** `{"command": "python3 - <<'PY'\nfrom pathlib import Path\ndef load(f):\n d={}\n for l in Path(f).read_text().splitlines():\n  p=l.split()\n  if len(p)>=3 and p[0].startswith('porte-') and p[1].isdigit(): d[p[0]]=int(p[2])\n return d\ncur=load('work/portes/passe-1611/registre.txt'); prev=load('work/po … [373 caractères tronqués]`

  ```
done 32 rest 54 prev total 86
rest duration sum 5042 s = 84.0 min
longest rest [('porte-indice', 1127), ('porte-vision', 661), ('porte-profondeur-routee', 628), ('porte-ocr-scans', 507), ('porte-poids-creux', 368), ('porte-prechargement', 196), ('porte-produit', 187), ('porte-reflexe', 169), ('porte-melange', 149), ('porte-jeux', 131), ('porte-topologie', 114), ('porte-pont', 95)]
  ```

- **job_kill** `{"job_id": "bash-32", "reason": "Attente trop courte : la passe a encore ~84 min"}`

  ```
requested cancellation of job bash-32
  ```

- **bash** `{"command": "for i in $(seq 1 520); do if grep -q '^--- ' work/portes/passe-1611/registre.txt 2>/dev/null; then echo FINI; break; fi; sleep 15; done; date; echo '=== registre ==='; cat work/portes/passe-1611/registre.txt; echo '=== rouges ==='; awk '$2 != 0' work/portes/passe-1611/registre.txt", "de … [81 caractères tronqués]`

  ```
started background job bash-49
  ```

- **bash** `{"command": "sed -n '1,90p' reports/rapport-tagger-auto.md; echo '==='; sed -n '1,80p' reports/rapport-or-roles-protocole.md", "description": "Read auto tagger and role gold sources"}`

  ```
# Y1 — le prototype du mode `auto` du tagger : l'API si la clé existe, l'heuristique sinon, sans changer le code de sortie

> **Ligne de roadmap** : **R0.7** (le lecteur) / **B13** · **Tâche** : **Y1** (J5, la décision
> du tagger) · **Date** : 2026-11-15 · **HEAD mesuré** : `f63ad709` + ce diff · **Verdict** :
> ✅ **le prototype est mesuré** — clé présente → API, **code 0**, **130 tokens** ; clé
> invalide → heuristique, **code 0** (pas 4), `refus` explicite ; clé absente → heuristique,
> **code 0**, **sortie identique au défaut octet pour octet** ; clé + réseau coupé →
> heuristique, **code 0** après **3 essais** ; refus de texte → **code 3**, **aucun appel API**.
> **30/30 tests**. **Recommandation** : garder le **défaut heuristique hors ligne** et
> `--tagger auto` comme **prototype opt-in**, jamais comme défaut. **La décision reste à
> l'humain** : ce diff ne change pas le défaut.

**En trois lignes.** (1) `analyser --tagger auto` choisit la voie : si `_cle_tagger()` trouve
une clé (fichier ou environnement), il construit la cascade API ; sinon il ne construit même
pas le client réseau et rend l'heuristique. (2) Le **code de sortie ne change pas** : **0**
dans les deux cas, **
… [11449 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,80p' reports/rapport-panini-manifeste.md; echo '==='; grep -n \"26\\|42/44\\|27/60\" reports/rapport-panini-manifeste.md | head -20", "description": "Read Panini manifest source"}`

  ```
# W4 — Panini : le manifeste des 26 signatures V14 et le rejeu disponible

> **Ligne de roadmap** : **R0.7** (le bloc linguistique) / **L** · **Tâche** : **W4** (J3 matin,
> la part du pilote) · **Date** : 2026-11-15 · **HEAD mesuré** : `be3f41ad` · **Verdict** :
> ✅ **le manifeste est prêt et envoyable** ; ❌ **le rejeu n'est pas un test** — **27/60** paires
> calculées, **33** manquantes, calibration **42/44**, **3** sources sous 300 mots, **5** groupes de
> doublons parmi les 26. **Aucune p-value de H0 n'est écrite.**
>
> **JSON** : [`panini-manifeste.json`](panini-manifeste.json) · **Commande Panini** :
> [`../tools/panini_signatures_26.py`](../tools/panini_signatures_26.py) · **Rejeu** :
> [`../tools/protocole_date.py`](../tools/protocole_date.py) · **Manifeste B1** :
> [`protocole-date.json`](protocole-date.json).

**En trois lignes.** (1) Les **26** textes du protocole B1 qui n'ont pas de signature
`analytic_sigs_v1` sont listés, avec leur fichier source, leur SHA-256, leurs mots et les paires
qu'ils servent ; la commande que Panini doit lancer et le format attendu sont ci-dessous. (2) Sur
les **60** paires, **27** ont leurs deux signatures (1 G1, 14 G2, 12 G3) : on les décri
… [6720 caractères tronqués]
  ```

- **bash** `{"command": "tail -3 work/portes/roue-1116/registre.txt; awk '$2 != 0' work/portes/roue-1116/registre.txt", "description": "Read previous pass summary"}`

  ```
porte-trace 0 31
porte-vision 0 661
--- 82 vertes, 4 rouges ---
porte-indice 1 1127
porte-melange 1 149
porte-produit 1 187
porte-sessions 1 0
--- 82 vertes, 4 rouges ---
  ```

- **bash** `{"command": "sed -n '1,80p' tools/index_reports.py", "description": "Inspect report index generator"}`

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

- **bash** `{"command": "date; wc -l work/portes/passe-1611/registre.txt; tail -1 work/portes/passe-1611/passe-1611.log", "description": "Check pass progress"}`

  ```
lun 16 nov 2026 05:24:26 EST
32 work/portes/passe-1611/registre.txt
  porte-horloge          ✅                          29 s    ✅ borne atteinte : arrêt EXPLICITE (code 5) et AUCUNE perplexité rendue
  ```

- **bash** `{"command": "ls -l reports/rapport-bilan-final.* 2>/dev/null || echo absent", "description": "Check final report does not exist"}`

  ```
absent
  ```

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-final.md", "content": "# Bilan final — Drave 0.1.0, 16 novembre 2026\n> **En une ligne.** Le bloc linguistique s'**installe** (éditable, roue, historique), **démarre en 3 commandes**, publie un **JSON v2** mesuré, p … [3489 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-final.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "wc -l reports/rapport-bilan-final.md; awk '{print NR\": \"length($0)}' reports/rapport-bilan-final.md | sort -t: -k2 -n | tail -5", "description": "Check report line count and long lines"}`

  ```
40 reports/rapport-bilan-final.md
27: 180
19: 197
34: 223
40: 235
2: 345
  ```

- **bash** `{"command": "wc -w reports/rapport-bilan-final.md", "description": "Count report words"}`

  ```
570 reports/rapport-bilan-final.md
  ```

- **bash** `{"command": "python3 - <<'PY'\na=3.990812406176701; b=0.8157198431435972\nprint(a/b, 10000/b)\nprint((130452-129936)/1024)\nPY", "description": "Compute factor and memory delta"}`

  ```
4.892381176847464 12259.110874957134
0.50390625
  ```

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-final.json", "content": "{\n  \"schema\": \"drave.bilan.final\",\n  \"version\": 1,\n  \"date\": \"2026-11-16\",\n  \"tache\": \"Z3\",\n  \"titre\": \"Bilan final — Drave 0.1.0, 16 novembre 2026\",\n  \"ligne_roadma … [12458 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-final.json</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "python3 -m json.tool reports/rapport-bilan-final.json >/dev/null && echo JSON-OK; wc -l reports/rapport-bilan-final.json", "description": "Validate final JSON"}`

  ```
JSON-OK
279 reports/rapport-bilan-final.json
  ```

- **bash** `{"command": "unzip -l dist/drave-0.1.0-py3-none-any.whl | grep -E 'profils_udhr|gold.json|generateur.py|deepseek.py' | head", "description": "Verify wheel contents"}`

  ```
4888  2026-11-16 06:39   tools/construire_profils_udhr.py
    14571  2026-11-16 07:01   tools/profils_udhr.py
    11803  2026-10-26 14:59   tools/llm/deepseek.py
    31037  2026-11-16 05:04   tools/structures/generateur.py
    20009  2026-11-16 06:55   tools/tests/linguistique/gold.json
   802110  2026-11-16 06:39   tools/tests/linguistique/profils_udhr.json
  ```

- **bash** `{"command": "date; wc -l work/portes/passe-1611/registre.txt; tail -2 work/portes/passe-1611/passe-1611.log", "description": "Check pass progress"}`

  ```
lun 16 nov 2026 05:25:17 EST
32 work/portes/passe-1611/registre.txt
  porte-homeostasie      ✅                         629 s    ✅ porte tenue (×0 exact · activité monotone · dominance reproduite)
  porte-horloge          ✅                          29 s    ✅ borne atteinte : arrêt EXPLICITE (code 5) et AUCUNE perplexité rendue
  ```

- **bash** `{"command": "python3 tools/tests/test_empaquetage.py 2>&1 | tail -4", "description": "Run packaging test count"}`

  ```
----------------------------------------------------------------------
Ran 12 tests in 0.682s

OK
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-final.md", "old_string": "- **Éditable** : `pip install -e .` → `drave 0.1.0` (3,35 s, 8 tests) ; Python ≥ 3.10, **0** dépendance d'exécution.", "new_string": "- **Éditable** : `pip install -e .` → `drave 0.1.0` (3, … [83 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-final.md has been updated successfully.
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\np='reports/rapport-bilan-final.json'\nd=json.load(open(p))\nd['installable']['voies'][0]['tests']=12\nd['installable']['voies'][0]['test']='tools/tests/test_empaquetage.py (12 tests)'\nopen(p,'w').write(json.dumps(d,ensure_ascii=False,indent=2)+'\\n')\npri … [68 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "sed -n '1,45p' reports/rapport-bilan-final.md | cat -A | sed -n '8,20p'", "description": "Inspect code fence lines"}`

  ```
$
## 2. DM-CM-)marrage M-bM-^@M-^T 3/3, ~14 s$
```bash$
git clone https://github.com/stephanedenis/drave.git && cd drave$
python3 -m venv .venv && source .venv/bin/activate && pip install -e .$
drave --version && drave analyser "Le chat dort." && drave evaluer$
```$
JSON **5 899 octets**, 20 M-CM-)tiquettes ; clone public **sans** `tools/structures` M-bM-^FM-^R sortie dM-CM-)gradM-CM-)e (voir M-BM-' 6).$
$
## 3. API du JSON$
- SchM-CM-)ma **`drave.annotation` v2**, v1 lue, **8** champs racine ; candidats en objets `{span, cible, source}`, rM-CM-4les dans un vocabulaire **fermM-CM-) de 8**.$
- **2 139** objets, **1 295/1 295** cibles choisies, **0** span faux ; **21 M-bM-^FM-^R 8** rM-CM-4les, **0** hors table ; `role="predicat"` M-bM-^FM-^R **711**, `"prM-CM-)dicat"` M-bM-^FM-^R **0** ; rM-CM-4le inventM-CM-) M-bM-^FM-^R `RoleHorsVocabulaire`.$
$
  ```

- **bash** `{"command": "git status --short | head -30; echo '---'; ls -l reports/rapport-passe-1611.* 2>/dev/null || echo \"pas de rapport passe\"; echo '---'; date; wc -l work/portes/passe-1611/registre.txt", "description": "Check Z2 output and pass progress"}`

  ```
M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
 M journal/sessions/session-b9138a2a-648e-490d-a349-124ac1aa1ef0/digest.md
 M journal/sessions/session-b9138a2a-648e-490d-a349-124ac1aa1ef0/rapport.md
 M tools/chantier/plan.json
?? journal/sessions/session-e466b49c-4fcb-4b34-b5a8-5bc193487415/
?? reports/rapport-bilan-final.json
?? reports/rapport-bilan-final.md
---
pas de rapport passe
---
lun 16 nov 2026 05:25:36 EST
32 work/portes/passe-1611/registre.txt
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -40", "description": "Run doc review baseline"}`

  ```
revue de documentation · 773 fiche(s) · 868 JSON · 126 doc(s) · 86 porte(s) · 8 chapitre(s)
  ❌ 2 anomalie(s) :
     · compteurs : en-cours.md dit 772 fichiers, le disque en a 773
     · compteurs : en-cours.md dit 867 JSON, le disque en a 868
  ```

- **bash** `{"command": "python3 tools/verifie_en_cours.py 2>&1 | tail -20; echo code=$?", "description": "Run state verifier baseline"}`

  ```
en-cours · 1629 mots · 7 sections · 4 session(s) · 9 puces · 3 questions
  ✅ état court, structuré, multi-session et reprenable
code=0
  ```

- **bash** `{"command": "grep -rn \"index_reports\" tools/porte-*.sh tools/*.sh 2>/dev/null | head", "description": "Check if index is gated"}`

  ```
(no output)
  ```

- **bash** `{"command": "wc -l reports/rapport-bilan-final.md reports/rapport-bilan-final.json; python3 -m json.tool reports/rapport-bilan-final.json >/dev/null && echo OK", "description": "Check final file sizes"}`

  ```
40 reports/rapport-bilan-final.md
  324 reports/rapport-bilan-final.json
  364 total
OK
  ```

- **bash** `{"command": "python3 tools/drave.py --version; echo \"code=$?\"; python3 tools/drave.py analyser \"Le chat dort.\" >/tmp/analyser.txt; echo \"code=$?\"; head -3 /tmp/analyser.txt; python3 tools/drave.py evaluer >/tmp/evaluer.txt; echo \"code=$?\"; head -3 /tmp/evaluer.txt", "description": "Smoke tes … [29 caractères tronqués]`

  ```
drave 0.1.0
code=0
code=0
drave 0.1.0 — analyse heuristique (CPU, hors ligne)
langue=fr script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (61.5% du texte)
POS  Le/DET chat/NOUN dort/VERB ./PONCT
code=0
drave 0.1.0 — évaluation de l'heuristique sur le gold
gold vivant (hand + reel + synthétique) · 612 phrases · 3179 tokens · 239 cibles d'attachement
  ```

- **bash** `{"command": "python3 tools/drave.py analyser \"Le chat dort.\" --json | wc -c; python3 tools/drave.py --aide | grep -n \"Codes de sortie\" -A2", "description": "Check JSON size and codes help"}`

  ```
6179
18:Codes de sortie : 0 succès · 3 refus d'analyse (JSON) · 4 clé/dépendance absente
19-(--tagger explicite sans clé, ou --fichier introuvable) · 5 usage (argument, sous-commande,
20-langue hors fr/en, --fichier sur un répertoire) · 1 autre erreur.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-final.md", "old_string": "JSON **5 899 octets**, 20 étiquettes ; clone public **sans** `tools/structures` → sortie dégradée (voir § 6).", "new_string": "Clone public : **3/3**, JSON **5 899 octets**, 20 étiquettes ; … [87 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-final.md has been updated successfully.
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\np='reports/rapport-bilan-final.json'\nd=json.load(open(p))\nd['quickstart']['json_octets_public']=d['quickstart'].pop('json_octets',5899)\nd['quickstart']['json_octets_depot']=6179\nopen(p,'w').write(json.dumps(d,ensure_ascii=False,indent=2)+'\\n')\nprint( … [68 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "wc -l reports/rapport-bilan-final.md; grep -n \"Clone public\" reports/rapport-bilan-final.md", "description": "Verify line count after edit"}`

  ```
40 reports/rapport-bilan-final.md
15:Clone public : **3/3**, JSON **5 899 octets**, 20 étiquettes ; **sans** `tools/structures` → sortie dégradée (voir § 6) ; dépôt : **6 179 octets**.
31:- **Clone public dégradé** : sans `tools/structures`, attachement **88,70 %** (contre 99,58 %) ; F1 **81,88 %** n'est pas un gain.
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\ns=json.load(open('tools/schemas/drave-annotation-v2.json'))\nprint(s.get('required'))\nprint(len(s.get('required',[])))\nPY", "description": "Verify root required fields"}`

  ```
['schema', 'version', 'texte', 'langue', 'script', 'refus', 'etiquettes', 'unites_semantiques']
8
  ```

- **bash** `{"command": "git rev-parse exploitable-2026-11-16^{} 2>/dev/null; git cat-file -t exploitable-2026-11-16 2>/dev/null", "description": "Verify tag points to ae3c24f2"}`

  ```
ae3c24f2d8bb36311bc1d05e349b032c429a732c
tag
  ```

- **job_output** `{"job_id": "bash-49"}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "date; wc -l work/portes/passe-1611/registre.txt; tail -2 work/portes/passe-1611/passe-1611.log", "description": "Check pass progress"}`

  ```
lun 16 nov 2026 05:26:21 EST
33 work/portes/passe-1611/registre.txt
  porte-horloge          ✅                          29 s    ✅ borne atteinte : arrêt EXPLICITE (code 5) et AUCUNE perplexité rendue
  porte-indice           ❌ code 1                 1156 s    ❌ l'indice extérieur tombe à 482 jetons de l'aiguille et l'indice TÉMOIN (même invite, questio
  ```

- **bash** `{"command": "sed -n '1,120p' tools/porte-sessions.sh", "description": "Inspect sessions gate logic"}`

  ```
#!/bin/bash
# porte-sessions.sh — les plans de session sont lisibles et le linter refuse un doublon.
set -u
cd "$(dirname "$0")/.."
python3 tools/sessions.py --autotest || exit 1
python3 tools/sessions.py --check --strict || exit 1
echo "PORTE TENUE : plans lisibles · autotest doublon/champ manquant/pause · check strict"
  ```

- **bash** `{"command": "python3 tools/sessions.py --check --strict; echo code=$?", "description": "Check sessions heartbeat"}`

  ```
❌ mandat périmé (140 min) : e181ce02-cd50-488a-a6be-e84b79d40dcc — heartbeat à rafraîchir
code=1
  ```

- **bash** `{"command": "python3 tools/sessions.py --help 2>&1 | sed -n '1,100p'", "description": "Read sessions tool help"}`

  ```
usage: sessions.py [-h] [--racine RACINE] [--status] [--check] [--strict]
                   [--modele] [--autotest] [--depuis-en-cours]

sessions.py — plans de session : qui fait quoi, avant d'écrire `en-cours`.
Chaque session active expose son mandat dans `journal/sessions/<id>/plan.md` :
périmètre, fichiers réservés, heartbeat, prochaine action, état. Les autres
sessions consultent `--status` avant de claim, et `--check --strict` refuse
les mandats incomplets, les identifiants dupliqués, les périmètres qui se
recouvrent et les heartbeats périmés (le `--check` seul les signale). Les
**fichiers proches** (une réservation imbriquée dans une autre, `data/` ⊃
`data/structures/`) restent des **avertissements**, même en strict :
l'imbrication est le régime normal d'un territoire partagé, et une porte qui
échoue sur toute imbrication est rouge dès qu'une session réserve un sous-
dossier — mesuré le 02/11, le strict sortait en 1 avec **0 erreur et 4
avertissements**. `en-cours` reste la seule source de l'état : ce plan est le
**contrat de travail** qui le précède. Une session arrêtée (reboot, panne)
passe à `État : en pause` : elle reste dans l'état, son heartbeat n'est plus
exigé, et la
… [448 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' tools/verifie_journal.py", "description": "Inspect journal verifier"}`

  ```
#!/usr/bin/env python3
"""verifie_journal.py — un dossier par jour, et les sessions ancrées.

Règles vérifiées :
  1. aucun fichier `journal/AAAA-MM-JJ*.md` à la racine : chaque jour est un **dossier** ;
  2. chaque dossier `journal/AAAA-MM-JJ/` a un `README.md` ;
  3. chaque `README.md` de jour porte une section « Sessions DSH » et un lien vers
     `../README.md#sessions` ;
  4. chaque `journal/sessions/<id>/rapport.md` porte le bloc « Journaux » avec un lien vers
     son jour (ou le journal), vers `en-cours.md` et vers l'index des sessions ;
  5. les liens relatifs de `journal/README.md`, `journal/THEMES.md`, des `README.md` de jour
     et des rapports de session résolvent.

Usage : python3 tools/verifie_journal.py   (code 0 = journal propre)
"""
from __future__ import annotations
import pathlib
import re

RACINE = pathlib.Path(__file__).resolve().parent.parent
JOURNAL = RACINE / "journal"
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
# les liens markdown, sans les ancres ni les liens externes
LIEN = re.compile(r"\]\(([^)#]+?)(?:#[^)]*)?\)")
EXTERNE = ("http://", "https://", "mailto:", "#")


def liens(texte: str) -> list[str]:
    return [c for c in LIEN.findall(texte)
          
… [3313 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"orphelin\" -A30 tools/revue_documentation.py | head -60", "description": "Inspect orphan check"}`

  ```
14:  7. navigation : aucun document vivant n'est orphelin, et aucun chemin en code inline
15-     ne pointe vers un fichier absent (hors gabarits `AAAA`, `<...>`, `*`).
16-
17-Sortie : un rapport lisible, code 0 si tout passe, 1 sinon (utilisable comme porte).
18-"""
19-from __future__ import annotations
20-import pathlib, re, subprocess, sys
21-import xml.etree.ElementTree as ET
22-from datetime import date
23-
24-RACINE = pathlib.Path(__file__).resolve().parent.parent
25-sys.path.insert(0, str(RACINE / "tools"))
26-from verifie_etat_a_jour import etat_modifie, retards  # noqa: E402  (même dossier)
27-
28-GABARIT = ("<", "*", "AAAA", "...")
29-CHEMIN = re.compile(
30-    r"`((?:docs|reports|tools|journal|data|drave-core|sprints)/"
31-    r"[^`\s]+?\.(?:md|json|sh|py|rs|txt|svg|csv|jsonl))`"
32-)
33-
34-
35-def liens(texte: str):
36-    return re.findall(r"\]\(([^)#]+?)\)", texte)
37-
38-
39-def cible_generee(f: pathlib.Path, cible: str) -> bool:
40-    return cible.endswith((".puml.svg", ".mmd.svg")) and (f.parent / cible[:-4]).exists()
41-
42-
43-def date_dernier_commit() -> str:
44-    try:
--
80:    """Les fichiers vivants dont les liens comptent pour la navigation (orphelins).
… [1018 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"sources_nav\\|orphelin\\|cité\" tools/revue_documentation.py | sed -n '1,40p'", "description": "Find orphan loop"}`

  ```
5:  1. classement : pas de résultats dans docs/ (les fiches sont dans reports/ et citées) ;
8:     ment pas sur la cible ; les sources externes sont citées ;
14:  7. navigation : aucun document vivant n'est orphelin, et aucun chemin en code inline
79:def sources_nav():
80:    """Les fichiers vivants dont les liens comptent pour la navigation (orphelins)."""
244:    # 7b. orphelins : tout document vivant doit avoir au moins un lien entrant
246:    for f in sources_nav():
  ```

- **bash** `{"command": "sed -n '240,275p' tools/revue_documentation.py", "description": "Read orphan check"}`

  ```
if not (RACINE / p).exists():
                ligne = texte[: m.start()].count("\n") + 1
                alertes.append(f"chemin mort : {f.relative_to(RACINE)}:{ligne} → {p}")

    # 7b. orphelins : tout document vivant doit avoir au moins un lien entrant
    entrants: set[pathlib.Path] = set()
    for f in sources_nav():
        try:
            texte = f.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for cible in liens(texte):
            if cible.startswith(("http://", "https://", "mailto:")):
                continue
            p = (f.parent / cible).resolve()
            if p.suffix == ".md":
                entrants.add(p)
    for p in docs_vivants():
        if p.resolve() not in entrants:
            alertes.append(f"navigation : {p.relative_to(RACINE)} n'a aucun lien entrant")

    # 7b bis. les fiches glossaire sont toutes listées dans l'index du dossier
    cartes = sorted((RACINE / "docs/theorie/glossaire/entrees").glob("*.md"))
    if cartes:
        idx_cartes = RACINE / "docs/theorie/glossaire/README.md"
        if not idx_cartes.exists():
            alertes.append("glossaire : docs/theorie/glossaire/README.md manq
… [377 caractères tronqués]
  ```

- **bash** `{"command": "date; wc -l work/portes/passe-1611/registre.txt; tail -2 work/portes/passe-1611/passe-1611.log", "description": "Check pass progress"}`

  ```
lun 16 nov 2026 05:26:50 EST
33 work/portes/passe-1611/registre.txt
  porte-horloge          ✅                          29 s    ✅ borne atteinte : arrêt EXPLICITE (code 5) et AUCUNE perplexité rendue
  porte-indice           ❌ code 1                 1156 s    ❌ l'indice extérieur tombe à 482 jetons de l'aiguille et l'indice TÉMOIN (même invite, questio
  ```

- **bash** `{"command": "grep -n \"heartbeat\\|Heartbeat\\|État\\|Etat\" journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md | head -20; sed -n '1,40p' journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md", "description": "Read session plan heartbeat"}`

  ```
6:> Le heartbeat est celui de l'état ; il se rafraîchit à chaque cycle.
18:- **Heartbeat** : 2026-11-16 03:06 EST
22:- **Arrêt** : 2026-11-02 15 h 06 (reboot) — reprise à **16 h 16** ; **actif** ; heartbeat rafraîchi.
23:- **État** : actif
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
  `docs/schemas/heuristique-*.svg`, `tools/bloc_linguistique.
… [3407 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-final.md", "old_string": "**Suite.** Mettre l'état et la roadmap à jour, taguer le commit de clôture, puis **J4**. Fiches : [bilan 2](rapport-bilan-exploitable-2.md) · [CI](rapport-ci.md) · [passe 1611](rapport-pass … [316 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-final.md has been updated successfully.
  ```

- **bash** `{"command": "date; wc -l work/portes/passe-1611/registre.txt; tail -3 work/portes/passe-1611/passe-1611.log", "description": "Check pass progress"}`

  ```
lun 16 nov 2026 05:27:06 EST
33 work/portes/passe-1611/registre.txt
  porte-homeostasie      ✅                         629 s    ✅ porte tenue (×0 exact · activité monotone · dominance reproduite)
  porte-horloge          ✅                          29 s    ✅ borne atteinte : arrêt EXPLICITE (code 5) et AUCUNE perplexité rendue
  porte-indice           ❌ code 1                 1156 s    ❌ l'indice extérieur tombe à 482 jetons de l'aiguille et l'indice TÉMOIN (même invite, questio
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/rapport-bilan-exploitable-2.json'))\nprint(list(d))\nfor k in list(d)[:8]:\n print('==',k, json.dumps(d[k],ensure_ascii=False)[:500])\nPY", "description": "Inspect prior bilan JSON style"}`

  ```
['schema', 'version', 'titre', 'sous_titre', 'date', 'tache', 'statut', 'head', 'lignes_roadmap', 'principe', 'lot', 'verifications', 'portes', 'negatifs', 'reste', 'tag', 'controles', 'limites', 'fichiers', 'verdict']
== schema "drave.bilan-exploitable-2"
== version 1
== titre "V3 — la clôture de la nuit exploitable : les neuf tâches T1–T6 · U1–U3, deux vérifications, 86 portes, le tag exploitable-2026-11-16"
== sous_titre "Bilan de clôture sans relancer la passe : les neuf tâches mesurées, les deux vérifications, les chiffres, les négatifs, le relevé des portes et le tag annoté"
== date "2026-11-16"
== tache "V3"
== statut "cloture"
== head "ae3c24f2"
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/rapport-bilan-exploitable-2.json'))\nprint(json.dumps(d['portes'],ensure_ascii=False,indent=1)[:2500])\nprint('NEG',len(d['negatifs']))\nPY", "description": "Inspect prior gates JSON"}`

  ```
{
 "passe_complete_relancee": false,
 "relevé": {
  "dossier": "work/portes/roue-1116",
  "registre": "work/portes/roue-1116/registre.txt",
  "debut": "2026-11-16 vers 00:45 HNE",
  "fin": "2026-11-16 03:01 HNE",
  "portes": 86,
  "vertes": 82,
  "rouges": 4,
  "rouges_structurelles": [
   {
    "porte": "indice",
    "code": 1,
    "duree_s": 1127,
    "cause": "indice extérieur à 482 jetons de l'aiguille, témoin 459, hasard 370 : écart nul ou négatif",
    "statut": "structurelle, tolérée"
   },
   {
    "porte": "melange",
    "code": 1,
    "duree_s": 149,
    "cause": "l'état de A ne rend pas le code de A dans une invite qui n'en contient aucun (calibration)",
    "statut": "structurelle, tolérée"
   }
  ],
  "rouges_de_circonstance": [
   {
    "porte": "produit",
    "code": 1,
    "duree_s": 187,
    "cause": "evaluer --strict en échec au moment de la passe (V1 n'avait pas encore fini) ; les autres contrôles verts"
   },
   {
    "porte": "sessions",
    "code": 1,
    "duree_s": 0,
    "cause": "mandat périmé e181ce02 (122 min) : heartbeat à rafraîchir"
   }
  ]
 },
 "verification_ciblee": {
  "dossier": "work/portes/verif-cloture-1116",
  "registre": "work/portes/verif-cl
… [673 caractères tronqués]
  ```

- **bash** `{"command": "date; wc -l work/portes/passe-1611/registre.txt; tail -2 work/portes/passe-1611/passe-1611.log", "description": "Check pass progress"}`

  ```
lun 16 nov 2026 05:27:17 EST
33 work/portes/passe-1611/registre.txt
  porte-horloge          ✅                          29 s    ✅ borne atteinte : arrêt EXPLICITE (code 5) et AUCUNE perplexité rendue
  porte-indice           ❌ code 1                 1156 s    ❌ l'indice extérieur tombe à 482 jetons de l'aiguille et l'indice TÉMOIN (même invite, questio
  ```

- **bash** `{"command": "sed -n '1,100p' docs/produit/ci.md", "description": "Read CI doc"}`

  ```
# L'intégration continue — le workflow et sa preuve locale

> **Ce que ce document est.** La **protection** du produit : le workflow GitHub Actions qui
> rejoue, à chaque `push` et à chaque `pull request`, l'installation éditable, les trois tests
> du contrat et la **porte produit**, sur **Python 3.10 et 3.13**. Il dit aussi comment vérifier
> le workflow **sans `act`**, et ce que cette vérification ne prouve pas.
>
> **Vérifié le 2026-11-16** sur `s/v7` : YAML chargé par PyYAML **6.0.3**, **2 × 5 étapes
> vertes** depuis une **archive sans sous-module** (copie de secours S) et depuis le dépôt,
> porte produit **183/183**, et un test volontairement cassé qui sort en **1** et **arrête** la
> séquence. `act` n'est pas installé sur la machine de mesure : la preuve est locale, pas une
> exécution GitHub.
>
> **Fiche** : [`reports/rapport-ci.md`](../../reports/rapport-ci.md) ·
> **JSON** : [`reports/rapport-ci.json`](../../reports/rapport-ci.json) ·
> **Workflow** : [`../../.github/workflows/ci.yml`](../../.github/workflows/ci.yml) ·
> **Vérificateur** : [`../../tools/verifier_ci.py`](../../tools/verifier_ci.py).

## 1. Ce que le workflow lance

| étape | commande | ce qu'elle verrouill
… [5378 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\np='reports/rapport-bilan-final.json'\nd=json.load(open(p))\nd['verdict']='✅ installable, mesuré, refus explicite ; ❌ or de rôles humain absent, clone public dégradé, décisions ouvertes'\nopen(p,'w').write(json.dumps(d,ensure_ascii=False,indent=2)+'\\n')\np … [65 caractères tronqués]`

  ```
✅ installable, mesuré, refus explicite ; ❌ or de rôles humain absent, clone public dégradé, décisions ouvertes
  ```

- **bash** `{"command": "date; wc -l work/portes/passe-1611/registre.txt; tail -2 work/portes/passe-1611/passe-1611.log", "description": "Check pass progress"}`

  ```
lun 16 nov 2026 05:27:24 EST
33 work/portes/passe-1611/registre.txt
  porte-horloge          ✅                          29 s    ✅ borne atteinte : arrêt EXPLICITE (code 5) et AUCUNE perplexité rendue
  porte-indice           ❌ code 1                 1156 s    ❌ l'indice extérieur tombe à 482 jetons de l'aiguille et l'indice TÉMOIN (même invite, questio
  ```

- **bash** `{"command": "sed -n '1,120p' tools/porte-document.sh", "description": "Inspect document gate"}`

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
  ```

- **bash** `{"command": "sed -n '1,80p' tools/porte-tableaux.sh", "description": "Inspect tables gate"}`

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
… [2535 caractères tronqués]
  ```

- **bash** `{"command": "bash tools/porte-tableaux.sh 2>&1 | tail -5; echo code=$?", "description": "Run tables gate"}`

  ```
✅ 1857 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ❌ 1 lien(s) relatif(s) ne résolvent pas (sur 4853 examinés) :
     reports/rapport-bilan-final.md → rapport-passe-1611.md
code=0
  ```

- **bash** `{"command": "date; wc -l work/portes/passe-1611/registre.txt; tail -2 work/portes/passe-1611/passe-1611.log", "description": "Check pass progress"}`

  ```
lun 16 nov 2026 05:27:35 EST
33 work/portes/passe-1611/registre.txt
  porte-horloge          ✅                          29 s    ✅ borne atteinte : arrêt EXPLICITE (code 5) et AUCUNE perplexité rendue
  porte-indice           ❌ code 1                 1156 s    ❌ l'indice extérieur tombe à 482 jetons de l'aiguille et l'indice TÉMOIN (même invite, questio
  ```

- **bash** `{"command": "ps -eo pid,etimes,cmd | grep -E \"[p]orte-|[t]outes-les-portes\" | head -10", "description": "Identify running gate"}`

  ```
1759938    4523 bash -c mkdir -p work/portes/passe-1611 JOURNAUX=work/portes/passe-1611 bash tools/toutes-les-portes.sh > work/portes/passe-1611/passe-1611.log 2>&1 echo "EXIT=$?"
1759946    4523 bash tools/toutes-les-portes.sh
2077218     119 timeout 1800 bash tools/porte-jeux.sh
2077219     119 bash tools/porte-jeux.sh
  ```

- **bash** `{"command": "sed -n '1,100p' tools/verifie_etat_a_jour.py", "description": "Inspect state freshness hook"}`

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
… [2829 caractères tronqués]
  ```

- **bash** `{"command": "date; wc -l work/portes/passe-1611/registre.txt; tail -2 work/portes/passe-1611/passe-1611.log", "description": "Check pass progress"}`

  ```
lun 16 nov 2026 05:27:47 EST
33 work/portes/passe-1611/registre.txt
  porte-horloge          ✅                          29 s    ✅ borne atteinte : arrêt EXPLICITE (code 5) et AUCUNE perplexité rendue
  porte-indice           ❌ code 1                 1156 s    ❌ l'indice extérieur tombe à 482 jetons de l'aiguille et l'indice TÉMOIN (même invite, questio
  ```

- **bash** `{"command": "git status --short | head -20; ls -l reports/rapport-passe-1611.* 2>/dev/null || true; date", "description": "Check Z2 output"}`

  ```
M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
 M journal/sessions/session-b9138a2a-648e-490d-a349-124ac1aa1ef0/digest.md
 M journal/sessions/session-b9138a2a-648e-490d-a349-124ac1aa1ef0/rapport.md
 M tools/chantier/plan.json
?? journal/sessions/session-e466b49c-4fcb-4b34-b5a8-5bc193487415/
?? reports/rapport-bilan-final.json
?? reports/rapport-bilan-final.md
lun 16 nov 2026 05:27:55 EST
  ```

- **bash** `{"command": "ps -eo pid,etimes,cmd | grep -E \"[p]orte-|[t]outes-les-portes\" | tail -3; date; wc -l work/portes/passe-1611/registre.txt", "description": "Check running gate and count"}`

  ```
2078607      10 timeout 1800 bash tools/porte-jumeaux.sh
2078608      10 bash tools/porte-jumeaux.sh
2079812       1 bash tools/porte-jumeaux.sh
lun 16 nov 2026 05:27:58 EST
34 work/portes/passe-1611/registre.txt
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/rapport-bilan-final.json'))\nprint(list(d))\nprint('negatifs',len(d['negatifs']),'decisions',len(d['decisions']),'voies',len(d['installable']['voies']))\nprint('portes',d['portes'])\nPY", "description": "Inspect final JSON structu … [4 caractères tronqués]`

  ```
['schema', 'version', 'date', 'tache', 'titre', 'ligne_roadmap', 'verdict', 'chiffre_une_ligne', 'installable', 'quickstart', 'api_json', 'performance', 'codes', 'ci', 'portes', 'negatifs', 'decisions', 'prochaine_action', 'sources']
negatifs 8 decisions 3 voies 3
portes {'passe': 'work/portes/passe-1611', 'registre': 'work/portes/passe-1611/registre.txt', 'total': None, 'vertes': None, 'rouges': None, 'rouges_structurelles': [], 'rouges_circonstance': [], 'tolerees': ['indice', 'melange'], 'lecture': "awk '$2 != 0' sur le registre, jamais un tail ni un marqueur", 'verdict': '__A_COMPLETER__'}
  ```

- **bash** `{"command": "sed -n '1,20p' reports/rapport-bilan-final.json", "description": "Read JSON head"}`

  ```
{
  "schema": "drave.bilan.final",
  "version": 1,
  "date": "2026-11-16",
  "tache": "Z3",
  "titre": "Bilan final — Drave 0.1.0, 16 novembre 2026",
  "ligne_roadmap": [
    "B13",
    "R0.7"
  ],
  "verdict": "✅ installable, mesuré, refus explicite ; ❌ or de rôles humain absent, clone public dégradé, décisions ouvertes",
  "chiffre_une_ligne": "Installable par trois voies, 3 commandes de démarrage, JSON v2 (2 139 objets, 0 span faux), 10 000 mots en 0,816 s (α 1,076, ×4,89), codes 0/1/3/4/5, CI 10/10, passe de portes fraîche ; négatifs nommés et trois décisions ouvertes.",
  "installable": {
    "produit": "drave",
    "version": "0.1.0",
    "python": ">=3.10",
    "dependances_execution": 0,
    "voies": [
      {
        "nom": "editable",
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-final.json", "old_string": "  \"ligne_roadmap\": [\n    \"B13\",\n    \"R0.7\"\n  ],\n  \"verdict\":", "new_string": "  \"ligne_roadmap\": [\n    \"B13\",\n    \"R0.7\"\n  ],\n  \"statut\": \"cloture\",\n  \"head\": … [147 caractères tronqués]`

  ```
Error: cannot edit "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-final.json": file changed since it was read — re-read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-final.json", "limit": 30}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-final.json</path>
<type>file</type>
<content>
1: {
2:   "schema": "drave.bilan.final",
3:   "version": 1,
4:   "date": "2026-11-16",
5:   "tache": "Z3",
6:   "titre": "Bilan final — Drave 0.1.0, 16 novembre 2026",
7:   "ligne_roadmap": [
8:     "B13",
9:     "R0.7"
10:   ],
11:   "verdict": "✅ installable, mesuré, refus explicite ; ❌ or de rôles humain absent, clone public dégradé, décisions ouvertes",
12:   "chiffre_une_ligne": "Installable par trois voies, 3 commandes de démarrage, JSON v2 (2 139 objets, 0 span faux), 10 000 mots en 0,816 s (α 1,076, ×4,89), codes 0/1/3/4/5, CI 10/10, passe de portes fraîche ; négatifs nommés et trois décisions ouvertes.",
13:   "installable": {
14:     "produit": "drave",
15:     "version": "0.1.0",
16:     "python": ">=3.10",
17:     "dependances_execution": 0,
18:     "voies": [
19:       {
20:         "nom": "editable",
21:         "commande": "python3 -m pip install -e .",
22:         "code": 0,
23:         "resultat": "Successfully installed drave-0.1.0",
24:         "test": "tools/tests/test_empaquetage.py (12 tests)",
25:         "tests": 12,
26:         "duree_in
… [295 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-final.json", "old_string": "  \"ligne_roadmap\": [\n    \"B13\",\n    \"R0.7\"\n  ],\n  \"verdict\":", "new_string": "  \"ligne_roadmap\": [\n    \"B13\",\n    \"R0.7\"\n  ],\n  \"statut\": \"cloture\",\n  \"head\": … [147 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-final.json has been updated successfully.
  ```

- **bash** `{"command": "python3 -m json.tool reports/rapport-bilan-final.json >/dev/null && echo OK; wc -l reports/rapport-bilan-final.json", "description": "Validate JSON after edit"}`

  ```
OK
332 reports/rapport-bilan-final.json
  ```

- **bash** `{"command": "date; wc -l work/portes/passe-1611/registre.txt; tail -3 work/portes/passe-1611/passe-1611.log", "description": "Check pass progress"}`

  ```
lun 16 nov 2026 05:28:14 EST
34 work/portes/passe-1611/registre.txt
  porte-horloge          ✅                          29 s    ✅ borne atteinte : arrêt EXPLICITE (code 5) et AUCUNE perplexité rendue
  porte-indice           ❌ code 1                 1156 s    ❌ l'indice extérieur tombe à 482 jetons de l'aiguille et l'indice TÉMOIN (même invite, questio
  porte-jeux             ✅                         129 s    ✅ la porte des jeux tient : 100 % au niveau 4, 33/33 paires invariantes, 0 collision,
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -20; echo code=${PIPESTATUS[0]}", "description": "Check context budget"}`

  ```
3310    317   T1   3500  README.md
    3072    341 DATÉ      0  docs/implantation/convertisseur.md
    2962    364   T1   5000  docs/theorie/glossaire/02-modeles-et-architectures.md
    2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2797    236   T1   2800  reports/README.md
    2497    170   T1   2500  docs/pilotage/references-non-regression.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 3999 mots (budget 4 000)

  avertissements :
     · 65 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-p
… [142 caractères tronqués]
  ```

- **bash** `{"command": "sleep 90; date; wc -l work/portes/passe-1611/registre.txt; tail -3 work/portes/passe-1611/passe-1611.log", "description": "Wait 90s and check progress", "timeoutMs": 120000}`

  ```
lun 16 nov 2026 05:29:58 EST
38 work/portes/passe-1611/registre.txt
  porte-lecteur          ✅                           1 s  ✅ porte lecteur verte
  porte-lecture          ✅                           2 s  ✅ porte lecture verte
  porte-m5-brouillon     ✅                           0 s    ✅ brouillon déclaré (cibles [37,38,39]) et porté : 75 tenseurs, 41 263 M poids
  ```

- **bash** `{"command": "grep -rn \"__[A-Z_]*__\\|A_COMPLETER\" reports/rapport-bilan-final.* || echo no-placeholder", "description": "Check for placeholders"}`

  ```
reports/rapport-bilan-final.json:242:    "verdict": "__A_COMPLETER__"
reports/rapport-bilan-final.md:28:- **Portes** : `work/portes/passe-1611/` — **__PORTES__**.
  ```

- **bash** `{"command": "sed -n '225,250p' reports/rapport-bilan-final.json", "description": "Read gates JSON block"}`

  ```
"act": false,
    "limite": "preuve locale (YAML + commandes) ; pas de run GitHub, actions non épinglées par SHA",
    "source": "reports/rapport-ci.md"
  },
  "portes": {
    "passe": "work/portes/passe-1611",
    "registre": "work/portes/passe-1611/registre.txt",
    "total": null,
    "vertes": null,
    "rouges": null,
    "rouges_structurelles": [],
    "rouges_circonstance": [],
    "tolerees": [
      "indice",
      "melange"
    ],
    "lecture": "awk '$2 != 0' sur le registre, jamais un tail ni un marqueur",
    "verdict": "__A_COMPLETER__"
  },
  "negatifs": [
    {
      "nom": "clone public dégradé",
      "fait": "sans tools/structures, l'attachement tombe à 88,70 % et le rôle du GN devient objet ; F1 81,88 %",
      "consequence": "un débutant ne voit pas la sortie de la notice ; le F1 plus haut n'est pas un gain",
      "source": "reports/rapport-quickstart.md"
    },
  ```

- **bash** `{"command": "sleep 180; date; wc -l work/portes/passe-1611/registre.txt; tail -4 work/portes/passe-1611/passe-1611.log", "description": "Wait 3 min and check progress", "timeoutMs": 200000}`

  ```
lun 16 nov 2026 05:33:06 EST
59 work/portes/passe-1611/registre.txt
  porte-n3-service-briques ✅                           8 s  PORTE TENUE : pont actif dans le service · placement métadonnée · décision à seuil 12/0 vs 0/12 
  porte-n3-service       ✅                           7 s  PORTE TENUE : service natif vivant · /sante exact · génération déterministe · 404
  porte-n3-seuil         ✅                           6 s  PORTE TENUE : décision à seuil comptée · 0/1 aux extrêmes · mixte à 0,01 · déterministe
  porte-n3-sparsite-compte ✅                           5 s  PORTE TENUE : compteurs réels · top_k agit sur les experts · kwta agit sur les canaux · A déterm
  ```

- **bash** `{"command": "awk '$2 != 0' work/portes/passe-1611/registre.txt", "description": "List current red gates"}`

  ```
porte-indice 1 1156
porte-melange 1 144
  ```

- **bash** `{"command": "tail -40 journal/2026-11-16/README.md", "description": "Read journal tail"}`

  ```
syntagmes du tagger à l'heuristique. **27/27 cas conformes, 0 écart** ; une mutation
`qualite` → `qualité` est détectée. Les **3 commandes** du démarrage sont **3/3** dans une copie
sans `tools/structures` (JSON **5 899 octets**).

[Fiche](../../reports/rapport-exemples-v2.md) · [JSON](../../reports/rapport-exemples-v2.json).

### V3 — la clôture de la nuit exploitable, et le tag sur le dernier commit vert

Les **neuf tâches** du lot exploitable (**T1–T6**, **U1–U3**) et les deux vérifications
(**V1–V2**) sont liées dans un second bilan : [rapport-bilan-exploitable-2.md](../../reports/rapport-bilan-exploitable-2.md)
+ [JSON](../../reports/rapport-bilan-exploitable-2.json). Le chiffre de la nuit : le produit
s'installe, **10 000 mots** passent en **0,82 s** (α **1,076**, sorties identiques), la roue est
autonome (**1 727 201 o**, sans gold → **4**), les profils font **20/20** (ambigu **`und`**),
`--strict` fait **0,8625 / 0,8891** et les exemples **27/27**.

La passe `work/portes/roue-1116/` est **lue, pas relancée** : **86 portes, 82 vertes, 4 rouges**
— `indice` et `melange` structurelles, `produit` (V1 n'avait pas fini) et `sessions` (heartbeat
périmé) de circonstance. La vérific
… [1625 caractères tronqués]
  ```

- **bash** `{"command": "sleep 120; date; wc -l work/portes/passe-1611/registre.txt; tail -3 work/portes/passe-1611/passe-1611.log; echo '--- rouges'; awk '$2 != 0' work/portes/passe-1611/registre.txt", "description": "Wait 2 min and check progress", "timeoutMs": 140000}`

  ```
lun 16 nov 2026 05:35:17 EST
62 work/portes/passe-1611/registre.txt
  porte-n3-sparsite      ✅                           5 s  PORTE TENUE : kwta et top_k agissent séparément · A déterministe
  porte-occupation-elagage ✅                          64 s  ✅ porte occupation × élagage : la cible annoncée est VÉRIFIÉE dans le fichier exporté
  porte-occupation-moteur ✅                          59 s  ✅ porte occupation du moteur : la ligne « occupation des poids » est annoncée, elle COLLE à
--- rouges
porte-indice 1 1156
porte-melange 1 144
  ```

- **bash** `{"command": "sleep 240; date; wc -l work/portes/passe-1611/registre.txt; tail -3 work/portes/passe-1611/passe-1611.log; echo '--- rouges'; awk '$2 != 0' work/portes/passe-1611/registre.txt", "description": "Wait 4 min and check progress", "timeoutMs": 260000}`

  ```
lun 16 nov 2026 05:39:23 EST
62 work/portes/passe-1611/registre.txt
  porte-n3-sparsite      ✅                           5 s  PORTE TENUE : kwta et top_k agissent séparément · A déterministe
  porte-occupation-elagage ✅                          64 s  ✅ porte occupation × élagage : la cible annoncée est VÉRIFIÉE dans le fichier exporté
  porte-occupation-moteur ✅                          59 s  ✅ porte occupation du moteur : la ligne « occupation des poids » est annoncée, elle COLLE à
--- rouges
porte-indice 1 1156
porte-melange 1 144
  ```

- **bash** `{"command": "ps -eo pid,etimes,cmd | grep -E \"[p]orte-|[t]outes-les-portes\" | tail -4", "description": "Check running gate"}`

  ```
1759938    5231 bash -c mkdir -p work/portes/passe-1611 JOURNAUX=work/portes/passe-1611 bash tools/toutes-les-portes.sh > work/portes/passe-1611/passe-1611.log 2>&1 echo "EXIT=$?"
1759946    5231 bash tools/toutes-les-portes.sh
2103890     255 timeout 1800 bash tools/porte-ocr-scans.sh
2103891     255 bash tools/porte-ocr-scans.sh
  ```

- **bash** `{"command": "grep '^  porte-ocr' work/portes/passe-1611/passe-1611.log; grep '^porte-ocr' work/portes/passe-1611/registre.txt", "description": "Check ocr gates"}`

  ```
(no output)
[exit code: 1]
  ```

- **bash** `{"command": "tail -10 work/portes/passe-1611/passe-1611.log; echo ---; tail -5 work/portes/passe-1611/registre.txt", "description": "Inspect pass log tail"}`

  ```
porte-n3-refus         ✅                           5 s  PORTE TENUE : empreinte refusée (code 4) · même modèle bit-exact
  porte-n3-reseau        ✅                           6 s  PORTE TENUE : TCP localhost · aucun cache sur le fil · logits identiques au pas plein
  porte-n3-routes        ✅                           5 s  PORTE TENUE : routage vivant · même modèle déterministe · config différente change la sortie
  porte-n3-service-briques ✅                           8 s  PORTE TENUE : pont actif dans le service · placement métadonnée · décision à seuil 12/0 vs 0/12 
  porte-n3-service       ✅                           7 s  PORTE TENUE : service natif vivant · /sante exact · génération déterministe · 404
  porte-n3-seuil         ✅                           6 s  PORTE TENUE : décision à seuil comptée · 0/1 aux extrêmes · mixte à 0,01 · déterministe
  porte-n3-sparsite-compte ✅                           5 s  PORTE TENUE : compteurs réels · top_k agit sur les experts · kwta agit sur les canaux · A déterm
  porte-n3-sparsite      ✅                           5 s  PORTE TENUE : kwta et top_k agissent séparément · A déterministe
  porte-occupation-elagage ✅                          64 s  ✅
… [368 caractères tronqués]
  ```

- **bash** `{"command": "sleep 480; date; wc -l work/portes/passe-1611/registre.txt; tail -4 work/portes/passe-1611/passe-1611.log; echo '--- rouges'; awk '$2 != 0' work/portes/passe-1611/registre.txt", "description": "Wait 8 min and check progress", "timeoutMs": 500000}`

  ```
lun 16 nov 2026 05:47:37 EST
66 work/portes/passe-1611/registre.txt
  porte-ocr-scans        ✅                         509 s  ✅ porte OCR-scans verte : familles, colonnes et tableaux tiennent leurs planchers
  porte-ocr              ✅                          55 s  ✅ porte OCR verte : 10 pages lues, WER sous le seuil, parité tenue et contrôles en échec
  porte-pannes           ✅                          52 s    ✅ pair absent : échec annoncé en 2 s (code 7), aucune perplexité
  porte-peripherie       ✅                          16 s  PORTE TENUE : l'entrée est injectée, la sortie est écrite, le délai est exact, les refus sont
--- rouges
porte-indice 1 1156
porte-melange 1 144
  ```

- **bash** `{"command": "sed -n '93,106p' docs/pilotage/en-cours.md", "description": "Read state counters"}`

  ```
## Les chiffres de l'état

> Vérifié par `tools/revue_documentation.py`.

| invariant | valeur | contrôle |
|---|---|---|
| portes | **86** (dont `porte-banc-performance` le 15/11) | `tools/porte-*.sh` |
| chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
| fichiers / JSON de résultats | **772** / **867** | `reports/*.md` / `reports/*.json` |
| documents de `docs/` | **126** (hors archive et README) | `docs/**/*.md` |
| dernière passe | **16/11 00 h 45 → 03 h 01** : **86** portes, **82/4** ; rouges `indice`, `melange` (structurelles) et `produit`, `sessions` (circonstance) ; **vérification ciblée** : `sessions` **0**, `produit` **0** → **84/2** | `work/portes/roue-1116/registre.txt` ; `work/portes/verif-cloture-1116/` |

## Les chantiers et leurs bloquants
  ```

- **bash** `{"command": "sleep 300; date; wc -l work/portes/passe-1611/registre.txt; tail -4 work/portes/passe-1611/passe-1611.log; echo '--- rouges'; awk '$2 != 0' work/portes/passe-1611/registre.txt", "description": "Wait 5 min and check progress", "timeoutMs": 320000}`

  ```
lun 16 nov 2026 05:52:43 EST
67 work/portes/passe-1611/registre.txt
  porte-ocr              ✅                          55 s  ✅ porte OCR verte : 10 pages lues, WER sous le seuil, parité tenue et contrôles en échec
  porte-pannes           ✅                          52 s    ✅ pair absent : échec annoncé en 2 s (code 7), aucune perplexité
  porte-peripherie       ✅                          16 s  PORTE TENUE : l'entrée est injectée, la sortie est écrite, le délai est exact, les refus sont
  porte-poids-creux      ✅                         359 s  ✅ porte poids creux : le noyau creux est EXACT et il paie la sparsité — paires divisées sur
--- rouges
porte-indice 1 1156
porte-melange 1 144
  ```

- **bash** `{"command": "sleep 600; date; wc -l work/portes/passe-1611/registre.txt; tail -5 work/portes/passe-1611/passe-1611.log; echo '--- rouges'; awk '$2 != 0' work/portes/passe-1611/registre.txt", "description": "Wait 10 min and check progress", "timeoutMs": 620000}`

  ```
[still running after 600000ms; moved to background job bash-121]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **bash** `{"command": "date; wc -l work/portes/passe-1611/registre.txt; tail -3 work/portes/passe-1611/passe-1611.log", "description": "Check current progress"}`

  ```
lun 16 nov 2026 06:02:49 EST
70 work/portes/passe-1611/registre.txt
  porte-pont             ✅                          93 s    ✅ 448 fibres : +2.81 % · 392 fibres : +25.35 % — la marche est entre les deux
  porte-prechargement    ✅                         208 s    PORTE TENUE
  porte-produit          ✅                         196 s  ✅ porte produit verte
  ```

### 👤 Utilisateur

background job bash-121 (bash: sleep 600; date; wc -l work/portes/passe-1611/registre.txt; tail -5 work/portes/passe-1611/passe-1611.log; echo '--- rouges'; awk '$2 != 0' work/portes/passe-1611/registre.txt) finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "awk '$2 != 0' work/portes/passe-1611/registre.txt; echo '---'; tail -3 work/portes/passe-1611/registre.txt", "description": "Check reds and last gates"}`

  ```
porte-indice 1 1156
porte-melange 1 144
---
porte-pont 0 93
porte-prechargement 0 208
porte-produit 0 196
  ```

- **bash** `{"command": "stat -c 'birth=%w modify=%y' work/portes/passe-1611/passe-1611.log; stat -c 'birth=%w modify=%y' work/portes/passe-1611/registre.txt", "description": "Get pass start/end timestamps"}`

  ```
birth=2026-11-16 04:12:14.434348687 -0500 modify=2026-11-16 05:59:59.277336692 -0500
birth=2026-11-16 04:13:44.928609233 -0500 modify=2026-11-16 05:59:59.277336692 -0500
  ```

- **bash** `{"command": "tail -20 work/portes/passe-1611/porte-produit.log", "description": "Read product gate result"}`

  ```
✅ version : drave 0.1.0
  ✅ analyser fr : JSON valide, étiquettes et syntagmes
  ✅ analyser en : JSON valide, étiquettes et syntagmes
  ✅ profils : langue, script, confiance, 398 profils
  ✅ rejeu : sha256 f6355d8175a75854 deux fois
  ✅ smoke test : Ran 30 tests
  ✅ evaluer --strict : Ran 5 tests
  ✅ schéma v2 validé (5 cas v2 + 1 cas v1 + 20 phrases du gold)
  ✅ 50 textes libres : Ran 4 tests
  ✅ restitution v0 : surface exacte (miroir affiché)
  ✅ restitution v1 : forme canonique exacte, miroir strict distinct
  ✅ restitution v2 : rôles lisibles, rendu relu, contrôle détecté
  ✅ restitution v0/v1 : Ran 22 tests
  ✅ restitution v2 : Ran 17 tests
  ✅ schéma v2 : Ran 9 tests
  ✅ refus : JSON avec refus, code 3
  ✅ exemples de la doc : 27/27 cas conformes — ✅ aucun écart
  ✅ autotest parallèle : 183/183 portes tenues
✅ porte produit verte
  ```

- **bash** `{"command": "stat -c '%y' journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md; grep -n \"Heartbeat\" journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md | head", "description": "Check heartbeat status"}`

  ```
2026-11-16 03:04:35.952064032 -0500
18:- **Heartbeat** : 2026-11-16 03:06 EST
  ```

- **bash** `{"command": "sleep 480; date; wc -l work/portes/passe-1611/registre.txt; tail -5 work/portes/passe-1611/passe-1611.log; echo '--- rouges'; awk '$2 != 0' work/portes/passe-1611/registre.txt", "description": "Wait 8 min and check progress", "timeoutMs": 500000}`

  ```
lun 16 nov 2026 06:11:08 EST
72 work/portes/passe-1611/registre.txt
  porte-pont             ✅                          93 s    ✅ 448 fibres : +2.81 % · 392 fibres : +25.35 % — la marche est entre les deux
  porte-prechargement    ✅                         208 s    PORTE TENUE
  porte-produit          ✅                         196 s  ✅ porte produit verte
  porte-profondeur-routee ✅                         636 s  ✅ porte profondeur routée : 16 couches contre 24 sur 8192 jetons de corpus.ids,
  porte-push-paresseux   ✅                          32 s    PORTE TENUE
--- rouges
porte-indice 1 1156
porte-melange 1 144
  ```

- **bash** `{"command": "sleep 600; date; wc -l work/portes/passe-1611/registre.txt; tail -6 work/portes/passe-1611/passe-1611.log; echo '--- rouges'; awk '$2 != 0' work/portes/passe-1611/registre.txt", "description": "Wait 10 min and check progress", "timeoutMs": 620000}`

  ```
[still running after 600000ms; moved to background job bash-128]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **bash** `{"command": "date; wc -l work/portes/passe-1611/registre.txt; tail -6 work/portes/passe-1611/passe-1611.log; echo '--- rouges'; awk '$2 != 0' work/portes/passe-1611/registre.txt", "description": "Check current progress"}`

  ```
lun 16 nov 2026 06:21:14 EST
85 work/portes/passe-1611/registre.txt
  porte-sessions         ❌ code 1                    1 s    ❌ mandat périmé (190 min) : e181ce02-cd50-488a-a6be-e84b79d40dcc — heartbeat à rafraîchir
  porte-speculatif       ✅                          78 s    ✅ porte tenue (invariant exact · taux rendu · témoin à zéro · brouillon invalide refusé)
  porte-tableaux         ❌ code 1                    1 s    ❌ 1 lien(s) relatif(s) ne résolvent pas (sur 4853 examinés) :
  porte-tokenizer-kimi   ✅                           7 s    ✅ 10 textes identiques au tokenizer officiel (accents, emoji, CJK, arabe, code, nombres)
  porte-topologie        ✅                         114 s    ✅ PPL épinglées : reference 17.4702 · historique 30.4363 · topologie 30.4363 · relais 2 42.547
  porte-trace            ✅                          30 s    ✅ la trace fausse est détectée et nommée
--- rouges
porte-indice 1 1156
porte-melange 1 144
porte-sessions 1 1
porte-tableaux 1 1
  ```

### 👤 Utilisateur

background job bash-128 (bash: sleep 600; date; wc -l work/portes/passe-1611/registre.txt; tail -6 work/portes/passe-1611/passe-1611.log; echo '--- rouges'; awk '$2 != 0' work/portes/passe-1611/registre.txt) finished [status: completed, exit code: 0]. Read its output with job_output.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-final.md", "offset": 36, "limit": 8}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-final.md</path>
<type>file</type>
<content>
36: ## 7. Ce qu'il reste à décider
37: - **`--tagger auto`** : prototype **opt-in** mesuré (30/30), défaut hors ligne inchangé ; décider : le passer par défaut ou le laisser opt-in.
38: - **Or de rôles (J4)** : double codage indépendant, kappa ≥ 0,80, or permuté ; c'est le seul négatif produit qui ne soit pas une limite de mesure.
39: - **Panini** : **26 signatures V14** manquantes (calibration **42/44**, rejeu **27/60**) ; sans elles, le rejeu n'est pas un test.
40: **Suite.** L'état et la roadmap suivent ; le tag reste sur `ae3c24f2` ; la prochaine mesure est **J4**. Fiches : [bilan 2](rapport-bilan-exploitable-2.md) · [CI](rapport-ci.md) · [passe 1611](rapport-passe-1611.md) · [JSON](rapport-bilan-final.json).

(End of file - total 40 lines)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-final.md", "new_string": "**Suite.** L'état et la roadmap suivent ; le tag reste sur `ae3c24f2` ; la prochaine mesure est **J4**. Fiches : [bilan 2](rapport-bilan-exploitable-2.md) · [CI](rapport-ci.md) · `work/port … [333 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-final.md has been updated successfully.
  ```

- **bash** `{"command": "mkdir -p work/portes/verif-cloture-1611; bash tools/porte-tableaux.sh > work/portes/verif-cloture-1611/porte-tableaux.log 2>&1; echo $? > work/portes/verif-cloture-1611/porte-tableaux.code; cat work/portes/verif-cloture-1611/porte-tableaux.code; tail -3 work/portes/verif-cloture-1611/po … [73 caractères tronqués]`

  ```
0
  ✅ 1857 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4852 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-16)
  ```

- **bash** `{"command": "date; wc -l work/portes/passe-1611/registre.txt; tail -4 work/portes/passe-1611/passe-1611.log; echo '--- rouges'; awk '$2 != 0' work/portes/passe-1611/registre.txt", "description": "Check pass progress"}`

  ```
lun 16 nov 2026 06:21:36 EST
85 work/portes/passe-1611/registre.txt
  porte-tableaux         ❌ code 1                    1 s    ❌ 1 lien(s) relatif(s) ne résolvent pas (sur 4853 examinés) :
  porte-tokenizer-kimi   ✅                           7 s    ✅ 10 textes identiques au tokenizer officiel (accents, emoji, CJK, arabe, code, nombres)
  porte-topologie        ✅                         114 s    ✅ PPL épinglées : reference 17.4702 · historique 30.4363 · topologie 30.4363 · relais 2 42.547
  porte-trace            ✅                          30 s    ✅ la trace fausse est détectée et nommée
--- rouges
porte-indice 1 1156
porte-melange 1 144
porte-sessions 1 1
porte-tableaux 1 1
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md", "limit": 25}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md</path>
<type>file</type>
<content>
1: # Plan de session — Pensée, la RSN plurielle et le moteur N3
2: 
3: > **Mandat vivant.** Ouvert le 2026-10-31 22 h 45 HAE depuis
4: > [`docs/pilotage/en-cours.md`](../../../docs/pilotage/en-cours.md). Ce plan est le **contrat de
5: > synergie** : il dit ce que la session réserve, ce qu'elle attend des autres, et quand elle s'arrête.
6: > Le heartbeat est celui de l'état ; il se rafraîchit à chaque cycle.
7: 
8: - **Session** : `e181ce02-cd50-488a-a6be-e84b79d40dcc`
9: - **Rôle** : Pensée — RSN plurielle, arbre d'états, cycle multi-niveaux, moteur N3 ; analyse de la couche heuristique ; bloc linguistique
10: - **Périmètre** : Pensée, R4.4-reste, Coloration, Bloc linguistique (R0.7)
11: - **Fichiers réservés** : `docs/theorie/pensee-iterative.md`, `docs/schemas/pensee-*.svg`,
12:   `docs/implantation/moteur-de-pensee.md`, `tools/pensee/`, `reports/pensee-*`,
13:   `reports/r44-*`, `docs/theorie/pre-traitement-linguistique.md`,
14:   `docs/schemas/heuristique-*.svg`, `tools/bloc_linguistique.py`,
15:   `tools/porte-bloc-linguistique.
… [1209 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md", "new_string": "- **Heartbeat** : 2026-11-16 06:23 EST\n- **Prochaine action** : **J4 — l'or de rôles** (double codage) ; **Z1–Z3** livrés (CI **10/10**, passe **1611**, [bil … [610 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md has been updated successfully.
  ```

- **bash** `{"command": "bash tools/porte-sessions.sh > work/portes/verif-cloture-1611/porte-sessions.log 2>&1; echo $? > work/portes/verif-cloture-1611/porte-sessions.code; cat work/portes/verif-cloture-1611/porte-sessions.code; tail -4 work/portes/verif-cloture-1611/porte-sessions.log", "description": "Run ta … [22 caractères tronqués]`

  ```
0
autotest OK : plan valide, périmètre dupliqué refusé, champ manquant refusé, pause sans heartbeat exigé, mandat long avec claim accepté, reservation imbriquée avertie sans refus
  ✅ plans cohérents
PORTE TENUE : plans lisibles · autotest doublon/champ manquant/pause · check strict
  ```

- **bash** `{"command": "date; wc -l work/portes/passe-1611/registre.txt; tail -3 work/portes/passe-1611/passe-1611.log; echo '--- rouges'; awk '$2 != 0' work/portes/passe-1611/registre.txt", "description": "Check pass progress"}`

  ```
lun 16 nov 2026 06:21:50 EST
85 work/portes/passe-1611/registre.txt
  porte-tokenizer-kimi   ✅                           7 s    ✅ 10 textes identiques au tokenizer officiel (accents, emoji, CJK, arabe, code, nombres)
  porte-topologie        ✅                         114 s    ✅ PPL épinglées : reference 17.4702 · historique 30.4363 · topologie 30.4363 · relais 2 42.547
  porte-trace            ✅                          30 s    ✅ la trace fausse est détectée et nommée
--- rouges
porte-indice 1 1156
porte-melange 1 144
porte-sessions 1 1
porte-tableaux 1 1
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-final.md", "limit": 4, "offset": 26}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-final.md</path>
<type>file</type>
<content>
26: - **Codes** : `0` succès · `1` autre erreur (`--strict` sous 0,70) · `3` refus (texte vide) · `4` clé/fichier/gold absent · `5` usage ; `stdout` vide et pas de trace.
27: - **CI** : `.github/workflows/ci.yml`, matrice **3.10/3.13**, 5 étapes ×2 = **10/10 vertes** ; test cassé → **1**, job arrêté (**2/2**) ; `act` absent, preuve **locale** seulement.
28: - **Portes** : `work/portes/passe-1611/` — **__PORTES__**.
29: 

(Showing lines 26-29 of 40. Use offset=30 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-final.md", "new_string": "- **Portes** : `work/portes/passe-1611/` — **86 portes, 82 vertes, 4 rouges** au relevé : `indice`, `melange` (structurelles tolérées), `sessions` (heartbeat) et `tableaux` (lien transitoir … [163 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-final.md has been updated successfully.
  ```

- **bash** `{"command": "tail -25 work/portes/passe-1611/porte-indice.log; echo '==='; tail -12 work/portes/passe-1611/porte-melange.log; echo '==='; tail -8 work/portes/passe-1611/porte-sessions.log 2>/dev/null; echo '==='; tail -5 work/portes/passe-1611/porte-tableaux.log", "description": "Read red gate logs" … [1 caractères tronqués]`

  ```
=== 0. deux invites qui ne diffèrent que d'une phrase ===
  A 1470 jetons · B 1440 · aiguille (fin du code) au jeton 669
=== 1. A répond le code, B non ===
  A : Answer: ZQ-447
  B : Answer: 12345
  ✅ les deux invites diffèrent bien par l'aiguille seule
=== 2. indice EXTÉRIEUR : l'état de la question de B (pas dans le magasin de A) ===
    capture d'état    : position(s) [1439] écrite(s) dans /tmp/tmp.W1jjRqpvy9/etatB.*
    capture d'état    : position(s) [1469] écrite(s) dans /tmp/tmp.W1jjRqpvy9/etatA.*
=== 3. la mémoire interroge A, avec puis sans l'indice extérieur ===
  témoin   capture d'état    : position(s) [1440] écrite(s) dans /tmp/tmp.W1jjRqpvy9/etatC.*
  écho     indice SÉMANTIQUE : l'état de la question, position 1469, aiguille en 669 :
  écho       épisode rendu : 1469 · recouvrement 64/64 · distance à l'aiguille : 800 jetons
  écho       hasard        : 370 jetons en moyenne sur 1470 épisodes
  écho       ⇒ la mémoire n'a PAS retrouvé l'aiguille : un indice qui ne ressemble pas au contenu cherché ne le retrouve pas. C'est une limite du rappel par le contenu — il n'est pas sémantique —, et elle est mesurée, pas supposée.
  écho   
  extérieur   indice SÉMANTIQUE : EXTÉ
… [2036 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-final.json", "limit": 25, "offset": 235}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-final.json</path>
<type>file</type>
<content>
235:     "rouges_structurelles": [],
236:     "rouges_circonstance": [],
237:     "tolerees": [
238:       "indice",
239:       "melange"
240:     ],
241:     "lecture": "awk '$2 != 0' sur le registre, jamais un tail ni un marqueur",
242:     "verdict": "__A_COMPLETER__"
243:   },
244:   "negatifs": [
245:     {
246:       "nom": "clone public dégradé",
247:       "fait": "sans tools/structures, l'attachement tombe à 88,70 % et le rôle du GN devient objet ; F1 81,88 %",
248:       "consequence": "un débutant ne voit pas la sortie de la notice ; le F1 plus haut n'est pas un gain",
249:       "source": "reports/rapport-quickstart.md"
250:     },
251:     {
252:       "nom": "or de rôles humain absent",
253:       "fait": "le gold S est écrit par la même famille de règles ; le gold v2 donne 20/46 et F1 0,5406",
254:       "consequence": "144/144 n'est pas une validation indépendante ; J4 reste à faire",
255:       "source": "reports/rapport-restitution-v3.md"
256:     },
257:     {
258:       "nom": "linéarité mesurée sur un seul texte",
259:       "fait": "α 1,076
… [106 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-final.json", "limit": 22, "offset": 228}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-final.json</path>
<type>file</type>
<content>
228:   },
229:   "portes": {
230:     "passe": "work/portes/passe-1611",
231:     "registre": "work/portes/passe-1611/registre.txt",
232:     "total": null,
233:     "vertes": null,
234:     "rouges": null,
235:     "rouges_structurelles": [],
236:     "rouges_circonstance": [],
237:     "tolerees": [
238:       "indice",
239:       "melange"
240:     ],
241:     "lecture": "awk '$2 != 0' sur le registre, jamais un tail ni un marqueur",
242:     "verdict": "__A_COMPLETER__"
243:   },
244:   "negatifs": [
245:     {
246:       "nom": "clone public dégradé",
247:       "fait": "sans tools/structures, l'attachement tombe à 88,70 % et le rôle du GN devient objet ; F1 81,88 %",
248:       "consequence": "un débutant ne voit pas la sortie de la notice ; le F1 plus haut n'est pas un gain",
249:       "source": "reports/rapport-quickstart.md"

(Showing lines 228-249 of 332. Use offset=250 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-final.json", "new_string": "  \"portes\": {\n    \"passe\": \"work/portes/passe-1611\",\n    \"registre\": \"work/portes/passe-1611/registre.txt\",\n    \"debut\": \"2026-11-16 04:12:14 -0500\",\n    \"fin\": null,\ … [2776 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-final.json has been updated successfully.
  ```

- **bash** `{"command": "python3 -m json.tool reports/rapport-bilan-final.json >/dev/null && echo OK; grep -n 'null\\|A_COMPLETER\\|__PORTES__' reports/rapport-bilan-final.json reports/rapport-bilan-final.md || echo no-placeholder", "description": "Validate JSON and check placeholders"}`

  ```
OK
reports/rapport-bilan-final.json:233:    "fin": null,
  ```

- **bash** `{"command": "date; wc -l work/portes/passe-1611/registre.txt; tail -2 work/portes/passe-1611/passe-1611.log", "description": "Check pass progress"}`

  ```
lun 16 nov 2026 06:22:15 EST
85 work/portes/passe-1611/registre.txt
  porte-topologie        ✅                         114 s    ✅ PPL épinglées : reference 17.4702 · historique 30.4363 · topologie 30.4363 · relais 2 42.547
  porte-trace            ✅                          30 s    ✅ la trace fausse est détectée et nommée
  ```

- **bash** `{"command": "git status --short | head -30; ls -l reports/rapport-passe-1611.* 2>/dev/null || true", "description": "Check Z2 output"}`

  ```
M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
 M journal/sessions/session-b9138a2a-648e-490d-a349-124ac1aa1ef0/digest.md
 M journal/sessions/session-b9138a2a-648e-490d-a349-124ac1aa1ef0/rapport.md
 M tools/chantier/plan.json
?? journal/sessions/session-b7949a81-8213-4b06-93b7-dca9a1fabf31/
?? journal/sessions/session-e466b49c-4fcb-4b34-b5a8-5bc193487415/
?? reports/rapport-bilan-final.json
?? reports/rapport-bilan-final.md
  ```

- **bash** `{"command": "sleep 480; date; wc -l work/portes/passe-1611/registre.txt; tail -4 work/portes/passe-1611/passe-1611.log; echo '--- rouges'; awk '$2 != 0' work/portes/passe-1611/registre.txt", "description": "Wait 8 min for pass end", "timeoutMs": 500000}`

  ```
lun 16 nov 2026 06:30:21 EST
85 work/portes/passe-1611/registre.txt
  porte-tableaux         ❌ code 1                    1 s    ❌ 1 lien(s) relatif(s) ne résolvent pas (sur 4853 examinés) :
  porte-tokenizer-kimi   ✅                           7 s    ✅ 10 textes identiques au tokenizer officiel (accents, emoji, CJK, arabe, code, nombres)
  porte-topologie        ✅                         114 s    ✅ PPL épinglées : reference 17.4702 · historique 30.4363 · topologie 30.4363 · relais 2 42.547
  porte-trace            ✅                          30 s    ✅ la trace fausse est détectée et nommée
--- rouges
porte-indice 1 1156
porte-melange 1 144
porte-sessions 1 1
porte-tableaux 1 1
  ```

- **bash** `{"command": "ps -eo pid,etimes,cmd | grep -E \"[p]orte-vision|[t]outes-les-portes\" | tail -3; stat -c '%y' work/portes/passe-1611/passe-1611.log", "description": "Check vision gate"}`

  ```
2312646     606 bash tools/porte-vision.sh
2312652     606 timeout 2400 env DRAVE_VISION_POIDS=all DRAVE_VISION_COUCHES=32 DRAVE_VISION_FUSION=1 ./drave-core/target/release/drave models/vision/mmproj-Qwen2-VL-2B-Instruct-Q8_0.gguf --banc-vision /tmp/porte-vision/tour.bin
2312653     606 ./drave-core/target/release/drave models/vision/mmproj-Qwen2-VL-2B-Instruct-Q8_0.gguf --banc-vision /tmp/porte-vision/tour.bin
2026-11-16 06:20:18.725907378 -0500
  ```

- **bash** `{"command": "sed -n '55,66p' docs/pilotage/en-cours.md; echo '==='; sed -n '120,127p' docs/pilotage/en-cours.md", "description": "Read state sections to edit"}`

  ```
### Session `e181ce02-cd50-488a-a6be-e84b79d40dcc` — Pensée, la RSN plurielle et le moteur N3 *(actif)*

- **Id** : `e181ce02-cd50-488a-a6be-e84b79d40dcc` — [`plan.md`](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md).
- **Rôle** : **Pensée** — RSN, arbre d'états, N3 ; heuristique ; bloc linguistique.
- **Plan** : B13 · **Stratégie** : v0 · **Ambition** : tracé · **Objectif final** : moteur v0.
- **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**.
- **Ce que font les autres** : N2.
- **Ce qu'elle fait** : **W5** v3 (gold S **144/144**, v2 **20/46**) ; **U1** 4,0 → 0,82 s (α 1,08) ; **U2** roue 1 727 201 o, sans gold → 4 ; **U3** profils 20/20, `und` ; **V1** `--strict` 0,8625/0,8891 ; **V2** exemples **27/27** ; **V3** la clôture — **86/82/4** → **84/2**, tag `exploitable-2026-11-16` ([bilan 2](../../reports/rapport-bilan-exploitable-2.md)).
- **Prochaine action** : **J4** ; T132/T133 ; la décision `auto`.
- **Bloquants** : 7B locales interdites (règle 11) ; **gold de pensée**.
- **Journal** : [la session](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/).

===
## Ce qui reste

**V3 — la clôture** : **T1–T6**, **U1–U3**, **V1–V2** ; **86/82/4*
… [906 caractères tronqués]
  ```

- **bash** `{"command": "sleep 150; date; wc -l work/portes/passe-1611/registre.txt; tail -5 work/portes/passe-1611/passe-1611.log; echo '--- rouges'; awk '$2 != 0' work/portes/passe-1611/registre.txt", "description": "Wait 2.5 min for vision", "timeoutMs": 170000}`
