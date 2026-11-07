# Session DSH — relecture

- identifiant : `599e9c0e-4252-43ca-a89a-3886d723c379`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-06 21:13:31
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7). Mission : **état de N2 et de sa porte** — lecture seule, aucun code.

Contexte : `docs/pilotage/roadmap.md` (chantier N2), `docs/pilotage/en-cours.md` (session N2), `reports/rapport-n2-*.md`, `tools/eval_n2_propre.py`, `tools/entrainer_native.py`, `tools/native_model.py`, `tools/porte-*.sh`. A23 a noté : « `tools/porte-n2.sh` n'existe pas ; `eval_n2_propre.py` exige un checkpoint ; la rouge de N2 est la porte propre à 0,29 ».

À faire :
1. **Inventaire** : quels checkpoints existent (chemins, tailles, dates, métadonnées) ; quels runs sont documentés (fiches) ; où est la porte propre (quelle commande, quel seuil, quel résultat) ; pourquoi 0,29.
2. **Vérifie** que `tools/eval_n2_propre.py` fonctionne sur le checkpoint le plus récent (si un checkpoint existe) : lance-le en lecture seule (ou explique précisément pourquoi tu ne peux pas), note le résultat.
3. **Propose** (sans l'écrire) une `tools/porte-n2.sh` : ce qu'elle devrait mesurer, le seuil, le temps, les dépendances.
4. Écris **uniquement** deux fichiers neufs : `reports/rapport-etat-n2.md` et `reports/pensee-etat-n2.json`.
5. Ne commite rien ; ne modifie aucun existant ; pas de `docs/pilotage/`, `AGENTS.md`, `journal/`, `tools/structures/`, `data/`, `tools/entrainer_native.py`, `tools/native_model.py`.

Rends un résumé : les checkpoints, le résultat de la porte propre, et ce que `porte-n2.sh` devrait faire.
Your parent agent id is "e181ce02-cd50-488a-a6be-e84b79d40dcc". Before you finish, send your result to that agent with send_message({ agent_id: "e181ce02-cd50-488a-a6be-e84b79d40dcc", message: "<self-contained result>" }). The parent shares your workspace but does not automatically receive your transcript, tool output, or reasoning. Send earlier messages as well when a finding changes what the parent should do next; sending a message does not end your turn.

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

You are a delegated subagent: your permission scope was fixed when you were started and cannot be widened from inside this session — operations that require approval are rejected automatically. When the task needs access beyond that scope, do not retry the denied operation; state the limitation in your reply so the delegating agent can handle it.

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

⏵ Inventaire des checkpoints N2 et de la porte propre

Je commence par explorer le dépôt : checkpoints, rapports N2, et les outils cités.

- **bash** `{"command": "git branch --show-current && git log --oneline -5 && ls", "description": "Afficher branche, derniers commits, racine"}`

  ```
s/v7
d31aa9a2 PRODUIT — --partition DANS LA CLI (alternative PAR DÉFAUT, filtrer EN OPTION), 10 TESTS, DOC À JOUR
6a1148c2 B13 — L'ÉLISION « que » → « qu » DANS LE TEST DES MARQUEURS (AUCUN EFFET MESURÉ, ROBUSTESSE) ; 183/183
4e6de0ee P0-3 — LES RAPPORTS FINAUX DE LA PARTITION (MESURES ÉPINGLÉES À fa1b0c6e) ; README DANS LE BUDGET
97f41554 B13 — LE STRIP DE LA FUSION : PLUS DE RÉFÉRENCE MORTE VERS UN SEGMENT DÉDUPLIQUÉ ; MESURES INCHANGÉES (0,85 / 0,6482 / 235-236)
5c0d5329 FICHE — LES PERTES DE R4 DITES HONNÊTEMENT (5/8 FAUX EN FRANÇAIS, NOMS NUS, PARTICIPES) ; README DANS LE BUDGET T1
AGENTS.md
bench
colab
data
docs
drave-core
journal
models
__pycache__
Qtrinet-bootstrap.md
README.md
reports
REPRISE.md
run_8bit_perfection.py
run_clusters.py
run_cpu.py
run_encoding.py
run_harness.py
run_list_mode.py
run_precision.py
run_quantify.py
run_real_clusters.py
run_sparsity.py
run_value_encoding.py
sprints
src
tools
work
  ```

- **glob** `{"pattern": "reports/rapport-n2-*"}`

  ```
reports/rapport-n2-hierarchie.md
reports/rapport-n2-distillation.md
reports/rapport-n2-budget.md
reports/rapport-n2-propre.md
reports/rapport-n2-diversite.md
reports/rapport-n2-combine.md
reports/rapport-n2-capacite.md
reports/rapport-n2-longueur.md
reports/rapport-n2-corpus-elargi.md
reports/rapport-n2-corpus-reel.md
reports/rapport-n2-multilingue.md
reports/rapport-n2-longueur-reelle.md
reports/rapport-n2-capacite-reelle.md
reports/rapport-n2-canal.md
reports/rapport-n2-distillation-reelle.md
reports/rapport-n2-anglais.md
reports/rapport-n2-anglais-distille.md
reports/rapport-n2-multilingue-distille.md
reports/rapport-n2-capacite-34m.md
reports/rapport-n2-multilingue-capacite.md
reports/rapport-n2-fenetre-r1.md
reports/rapport-n2-34m-distille.md
reports/rapport-n2-multilingue-34m.md
reports/rapport-n2-professeur.md
reports/rapport-n2-multilingue-34m-distille.md
reports/rapport-n2-anglais-34m.md
reports/rapport-n2-canal-distille.md
reports/rapport-n2-echantillon.md
reports/rapport-n2-canal-kd-34m.md
reports/rapport-n2-canal-34m.md
reports/rapport-n2-corpus-1go.md
reports/rapport-n2-pas-vs-texte.md
reports/rapport-n2-melange.md
reports/rapport-n2-r11.md
reports/rapport-n2-200k.md
r
… [177 caractères tronqués]
  ```

- **glob** `{"pattern": "tools/porte-*.sh"}`

  ```
tools/porte-mistral.sh
tools/porte-tokenizer-kimi.sh
tools/porte-peripherie.sh
tools/porte-memoire.sh
tools/porte-recurrence.sh
tools/porte-sauvegarde-modele.sh
tools/porte-occupation-elagage.sh
tools/porte-harnais-invariants.sh
tools/porte-audit-drapeaux.sh
tools/porte-poids-creux.sh
tools/porte-episodique.sh
tools/porte-horloge.sh
tools/porte-jumeaux.sh
tools/porte-registre.sh
tools/porte-occupation-moteur.sh
tools/porte-greffe.sh
tools/porte-melange.sh
tools/porte-push-paresseux.sh
tools/porte-echange-experts.sh
tools/porte-indice.sh
tools/porte-cerveau.sh
tools/porte-speculatif.sh
tools/porte-vision.sh
tools/porte-prechargement.sh
tools/porte-diff-couche.sh
tools/porte-document.sh
tools/porte-lecteur.sh
tools/porte-bloc-tableaux.sh
tools/porte-bloc-code.sh
tools/porte-etat.sh
tools/porte-bloc-maths.sh
tools/porte-miroir-blocs.sh
tools/porte-balayage.sh
tools/porte-budget.sh
tools/porte-pont.sh
tools/porte-coupe.sh
tools/porte-adaptateur-sortie.sh
tools/porte-cycle-c2.sh
tools/porte-n3-service.sh
tools/porte-n3-routes.sh
tools/porte-consolidation.sh
tools/porte-n3-profondeur.sh
tools/porte-n3-sparsite.sh
tools/porte-n3-sparsite-compte.sh
tools/porte-n3-composition.sh
tools/porte
… [976 caractères tronqués]
  ```

- **glob** `{"pattern": "tools/eval_n2_propre.py"}`

  ```
tools/eval_n2_propre.py
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-n2-porte-propre.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/eval_n2_propre.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-n2-porte-propre.md</path>
<type>file</type>
<content>
1: # N2 — La porte < 2,5 sur le corpus propre, attaquée avec la fenêtre
2: 
3: > **Ligne de roadmap** : N2 (la porte de perplexité) · **Date** : 2026-11-03 · **Verdict** :
4: > la porte **< 2,5 n'est pas atteinte** : le meilleur point est **2,7856** en
5: > validation et **2,8566** en test (fenêtre 512, contexte 1 024) — il manque **0,29**. Mais la
6: > fenêtre est le **seul bras dont la courbe descend avec la longueur** : à octets égaux (33 Mo),
7: > la fenêtre 512 fait **2,9726 → 2,8443 → 2,7856** de 128 à 1 024 octets, quand la fenêtre 128
8: > fait **2,9027 → 3,0464 → 3,1107** : elle gagne à courte longueur, puis elle est **0,33
9: > derrière** à 1 024.
10: > Les deux bras battent la chaîne honnête de N2.h (val **3,0904**, test **3,1960**). Et la
11: > **capacité ne ferme pas la porte** : à fenêtre 512, init aléatoire et 33 Mo vus, 11,47 M donne
12: > 2,8960 à 1 024 octets, 21,65 M 2,8688, 34,3 M **2,8662** — elle **sature** à 21,65 M et laisse
13: > encore **0,37**.
14: 
15: ## La question
16: 
17: La porte de N2 est **PPL < 2,5 sur le corpus propre**, te
… [6099 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/eval_n2_propre.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """eval_n2_propre.py — la porte honnête : PPL sur un corpus dédupliqué, et hors domaine.
3: 
4: Le corpus de `data/corpus_propre/` est construit par `tools/corpus_propre.py` : passages
5: répétés retirés, split par chunks contigus, **zéro fenêtre de validation dans
6: l'entraînement** (vérifié). Ce script évalue un point de contrôle :
7: 
8:   val / test        : in-domain, fenêtres tirées **dans** un chunk (jamais à cheval sur le
9:                       collage de deux chunks, qui est un artefact du split) ;
10:   litterature       : `data/corpus_fr_litterature.txt` (Verne, public domain) — jamais vu ;
11:   anglais           : `data/corpus_en.txt` (Wikipédia) — jamais vu ;
12:   wikitext2         : `data/wikitext2_test.txt` — jamais vu ;
13:   permute           : contrôle négatif, mêmes octets de validation, ordre détruit ;
14:   decomposition     : PPL des têtes précoces (après 2, 4, 6 blocs) et sans la boucle de
15:                       pensée — ce que chaque pièce porte, et ce que l'arrêt précoce coûte ;
16:   longueurs         : PPL à
… [6366 caractères tronqués]
  ```

- **bash** `{"command": "ls -la models/ 2>/dev/null | head -50; echo '---'; du -sh models/* 2>/dev/null | sort -h | tail -20", "description": "Lister le répertoire models et tailles"}`

  ```
total 863324
drwxr-xr-x. 1 stephane stephane       100  3 nov 09:12 .
drwxr-xr-x. 1 stephane stephane       686  6 nov 09:52 ..
-rw-r--r--. 1 stephane stephane 352972352 25 sep 17:13 Qwen2.5-0.5B-Q4_0.gguf
-rw-r--r--. 1 stephane stephane 531068480 25 sep 16:52 Qwen2.5-0.5B-Q8_0.gguf
drwxr-xr-x. 1 stephane stephane       138 15 oct 09:02 vision
---
337M	models/Qwen2.5-0.5B-Q4_0.gguf
507M	models/Qwen2.5-0.5B-Q8_0.gguf
1,6G	models/vision
  ```

- **bash** `{"command": "ls -la work/ 2>/dev/null; echo '=== .pt files ==='; find work -name '*.pt' -printf '%T@ %s %p\\n' 2>/dev/null | sort -n | awk '{printf \"%s %10.2f MB %s\\n\", strftime(\"%Y-%m-%d %H:%M\", $1), $2/1048576, $3}' | tail -60", "description": "Inventorier les checkpoints .pt dans work"}`

  ```
total 220
drwxr-xr-x. 1 stephane stephane  1490  6 nov 01:28 .
drwxr-xr-x. 1 stephane stephane   686  6 nov 09:52 ..
-rwxr-xr-x. 1 stephane stephane  2133  2 nov 16:46 attente_portes.sh
-rw-r--r--. 1 stephane stephane  6879  1 nov 12:49 corpus-wiki-langues.log
-rw-r--r--. 1 stephane stephane  1004  1 nov 11:14 corpus-wiki.log
-rw-r--r--. 1 stephane stephane  3985  1 nov 12:49 corpus-wiki-reste.log
drwxr-xr-x. 1 stephane stephane     8  1 nov 18:44 dr
-rw-r--r--. 1 stephane stephane   479  2 nov 20:32 entete-references.txt
-rw-------. 1 stephane stephane  5759  2 nov 01:21 finaliser_ocr.py
-rw-r--r--. 1 stephane stephane  9625  3 nov 05:55 hub-nuit.md
-rw-r--r--. 1 stephane stephane  3604  3 nov 05:52 maj_references2.py
-rw-r--r--. 1 stephane stephane  2954  3 nov 13:17 maj_references3.py
-rw-r--r--. 1 stephane stephane  3735  2 nov 20:41 maj_references.py
-rw-r--r--. 1 stephane stephane  2230  2 nov 21:28 maj_table_seule.py
-rw-r--r--. 1 stephane stephane   554  3 nov 13:31 msg-1335.txt
-rw-r--r--. 1 stephane stephane   652  3 nov 13:18 msg-80-2.txt
-rw-r--r--. 1 stephane stephane   640  3 nov 13:34 msg-backlog-n2.txt
-rw-r--r--. 1 stephane stephane   586  3 nov 07:16 msg-bilan.txt
… [6139 caractères tronqués]
  ```

- **bash** `{"command": "grep -n 'N2' docs/pilotage/roadmap.md | head -60", "description": "Chercher N2 dans la roadmap"}`

  ```
32:| **N — le natif** | DRVM, `drave-n0`, [distillation](../theorie/glossaire/entrees/distillation.md), usage, échelle | 🔬 N0/N1 mesurés ; **N0.3b close** ; **N0.1 6/6** ; N2.h : 3,0904 domaine, 3,85 hors dépôt ; **N2.ac (1 Go) : 3,49 / 6,03 / 8,34 — production** ; **200 k pas : val_fr 3,16, littérature 5,61, anglais 7,28, wikitext2 8,00** ; **fenêtre 1 024 : 2,4759 / 2,4373 au grand corpus — sous 2,5** ; porte propre **2,7856** ; **N3 couvert** (17 portes, inventaire ; deux conditions) ; N4 partiel | **N2** : **clôturée** le 03/11 11 h 25, la **fenêtre est la recette de production** ; **paire propre de distillation** (04/11) ; puis la **porte propre (0,29)** ; **N4** |
36:| **D — les données** | inventaire, corpus 10 langues, texte intégral, PDF/[OCR](../theorie/glossaire/entrees/ocr.md), documents, genres | ✅ inventaire ; **10 corpus texte intégral** (20,53 M art., 67,73 G car., 81,2 Go, **8 Ko 0**) ; **PDF** (1 927 doc., 322 Mo) ; **documents** (3 384 doc., 872 M car., 8 Ko 2,07 %) ; **OCR** (20 livres, 7 381 p, 15,36 M, 8 Ko 0 ; [CEGEP](../theorie/glossaire/entrees/cegep.md) **91 scans uniques**, 60 documents, 1 982 p, 4,41 M car., 8 Ko 0) ; **genres** mesurés | **l'OCR est clo
… [5051 caractères tronqués]
  ```

- **bash** `{"command": "grep -n 'N2' docs/pilotage/en-cours.md | head -60", "description": "Chercher N2 dans en-cours"}`

  ```
10:> 04/11** : hub `1e7ef596` (08 h 50), N2 09 h 41, S 09 h 46, L/B13 10 h 14 ; **N3** clos en
17:- **Fait** : index réparé ; **N3 intégré** ; N2/S/L actifs ; suivi docs (revue, liens, tableaux).
31:> **Bilan de 15 h** : reprises à 09 h ; **runs N2 arrêtés** (`kd2`, `rope2048` à 6 400/20 000) ; **perte α=0,9 0,8385 (−0,176), PPL 3,1119 (−0,06)** ;
43:- **Ce que font les autres** : **N2**, **S**, **Pensée**.
58:- **Ce que font les autres** : **hub**, **N2**, **Pensée**.
73:- **Ce que font les autres** : **N2**, **S**, **hub**.
79:### Session `0733c5bb-f90b-4f58-9241-3364fa32e46c` — N2 : la production et la capacité *(en pause)*
82:- **Rôle** : **N2** — la production et la capacité.
96:- **N2 — en pause** : **1 024** = recette de production ; **2 048 fini** (2×10 000 pas ; drvm `c50beff6` + `91a3028…`) ; la distillation est mesurée (bilan ci-dessus) ; prochaine : la **porte propre (0,29)** ; **GPUs libres** (claim `n2-jour` libéré).
122:| **N — le natif** | **N2, N4** | N2 : **fenêtre 1 024 — 2,3911 / 2,3522 au grand corpus (sous 2,5)** ; porte propre 2,7856 ; **N3 couvert** (17 portes, inventaire ; deux conditions) ; N4 0/4 ; N5 gelé | **les runs N2** ; puis la **porte propre (0,29)
… [992 caractères tronqués]
  ```

