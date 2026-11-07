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

- **bash** `{"command": "date; echo '---'; find . -path ./.git -prune -o -name '*.pt' -print 2>/dev/null | wc -l; echo '--- top 25 recents, tous les .pt du dépôt'; find . -path ./.git -prune -o -name '*.pt' -printf '%T@ %s %p\\n' -print 2>/dev/null | grep -v '^\\./' | sort -n | tail -25 | awk '{printf \"%s %10. … [127 caractères tronqués]`

  ```
ven 06 nov 2026 21:15:00 EST
---
124
--- top 25 recents, tous les .pt du dépôt
2026-11-02 23:51     130.89 MB ./work/n2ac/mix2048-3.75k.pt
2026-11-03 01:33     130.89 MB ./work/n2ac/rope2048-12.5k.pt
2026-11-03 02:01     130.89 MB ./work/n2ac/propre512-8k.pt
2026-11-03 02:33     130.89 MB ./work/n2ac/propre128-32k.pt
2026-11-03 02:45     130.89 MB ./work/n2ac/mix1024-30k.pt
2026-11-03 03:26      82.62 MB ./work/n2ac/cap-2165m-512.pt
2026-11-03 03:33      45.12 MB ./work/n2ac/cap-1147m-512.pt
2026-11-03 03:49     130.89 MB ./work/n2ac/mix512-zero-15k.pt
2026-11-03 03:55      82.62 MB ./work/n2ac/cap-2165m-128.pt
2026-11-03 04:04      45.12 MB ./work/n2ac/cap-1147m-128.pt
2026-11-03 13:49      45.12 MB ./work/n2ac/propre-1147m-512z.pt
2026-11-03 14:10      82.62 MB ./work/n2ac/propre-2165m-512z.pt
2026-11-03 14:35     130.89 MB ./work/n2ac/propre-3430m-512z.pt
2026-11-03 15:39      45.12 MB ./work/n2ac/kd-1147m-512-a0.5.pt
2026-11-03 16:15      45.12 MB ./work/n2ac/kd-1147m-512-a0.9.pt
2026-11-03 17:22     130.89 MB ./work/n2ac/mix1024-60k.pt
2026-11-03 18:13     130.89 MB ./work/n2ac/kd-mix512-15k.pt
2026-11-04 11:01      45.12 MB ./work/n2ac/kdp-1147m-a0.pt
2026-11-04 12:18      45
… [403 caractères tronqués]
  ```

- **bash** `{"command": "ls -la work/n2ac/ | head -80", "description": "Lister work/n2ac"}`

  ```
total 8032656
drwxr-xr-x. 1 stephane stephane     10412  5 nov 10:19 .
drwxr-xr-x. 1 stephane stephane      1490  6 nov 01:28 ..
-rw-r--r--. 1 stephane stephane 137224476  2 nov 17:31 absolu-pos1152.drvm
-rw-r--r--. 1 stephane stephane     21807  2 nov 17:31 absolu-pos1152.log
-rw-r--r--. 1 stephane stephane 137248740  2 nov 17:30 absolu-pos1152.pt
-rw-r--r--. 1 stephane stephane       561  2 nov 17:31 absolu-pos1152.pt.json
-rw-------. 1 stephane stephane      2763  2 nov 21:05 agrege_fenetre.py
-rw-r--r--. 1 stephane stephane      1680  2 nov 23:31 agrege_production.py
-rw-------. 1 stephane stephane      3151  2 nov 18:50 agrege_r11.py
-rw-r--r--. 1 stephane stephane  47283932  3 nov 04:04 cap-1147m-128.drvm
-rw-r--r--. 1 stephane stephane     35105  3 nov 04:04 cap-1147m-128.log
-rw-r--r--. 1 stephane stephane  47308063  3 nov 04:04 cap-1147m-128.pt
-rw-r--r--. 1 stephane stephane       505  3 nov 04:04 cap-1147m-128.pt.json
-rw-r--r--. 1 stephane stephane  47283932  3 nov 03:33 cap-1147m-512.drvm
-rw-r--r--. 1 stephane stephane      9444  3 nov 03:33 cap-1147m-512.log
-rw-r--r--. 1 stephane stephane  47308063  3 nov 03:33 cap-1147m-512.pt
-rw-r--r--. 1 stephane stephane       
… [4700 caractères tronqués]
  ```

- **bash** `{"command": "ls -la data/corpus_propre/ 2>/dev/null; echo '---'; wc -c data/corpus_propre/*.txt 2>/dev/null; echo '--- corpus-fr-litterature etc'; ls -la data/corpus_fr_litterature.txt data/corpus_litt_propre/val.txt data/corpus_en.txt data/wikitext2_test.txt 2>&1", "description": "Vérifier corpus p … [25 caractères tronqués]`

  ```
total 7364
drwxr-xr-x. 1 stephane stephane     122  3 nov 02:03 .
drwxr-xr-x. 1 stephane stephane    2664  2 nov 18:33 ..
-rw-r--r--. 1 stephane stephane  320314 31 oct 22:21 dev.txt
-rw-r--r--. 1 stephane stephane  180224  3 nov 02:03 test.canal
-rw-r--r--. 1 stephane stephane  180224 31 oct 22:20 test.txt
-rw-r--r--. 1 stephane stephane 3244858  2 nov 23:07 train.canal
-rw-r--r--. 1 stephane stephane 3244858 31 oct 22:20 train.txt
-rw-r--r--. 1 stephane stephane  180224  2 nov 23:07 val.canal
-rw-r--r--. 1 stephane stephane  180224 31 oct 22:20 val.txt
---
 320314 data/corpus_propre/dev.txt
 180224 data/corpus_propre/test.txt
3244858 data/corpus_propre/train.txt
 180224 data/corpus_propre/val.txt
3925620 total
--- corpus-fr-litterature etc
-rw-r--r--. 1 stephane stephane 100276153  8 oct 09:42 data/corpus_en.txt
-rw-r--r--. 1 stephane stephane  17031747 17 oct 18:26 data/corpus_fr_litterature.txt
-rw-r--r--. 1 stephane stephane    843776 31 oct 22:24 data/corpus_litt_propre/val.txt
-rw-r--r--. 1 stephane stephane    359041 25 sep 18:02 data/wikitext2_test.txt
  ```

- **bash** `{"command": "nvidia-smi --query-gpu=name,memory.total,memory.used,utilization.gpu --format=csv 2>&1 | head; echo '---'; ls -la ~/gpu-env/bin/python 2>&1; echo '---'; ~/gpu-env/bin/python -c 'import torch; print(torch.__version__, torch.cuda.is_available(), torch.cuda.get_device_name(0) if torch.cuda … [99 caractères tronqués]`

  ```
name, memory.total [MiB], memory.used [MiB], utilization.gpu [%]
Quadro RTX 5000, 16384 MiB, 154 MiB, 2 %
Quadro RTX 5000, 16384 MiB, 4 MiB, 0 %
---
lrwxrwxrwx. 1 stephane stephane 7 31 jui 08:53 /home/stephane/gpu-env/bin/python -> python3
---
2.11.0+cu130 True Quadro RTX 5000
  ```

- **bash** `{"command": "echo \"JOURNAUX=${JOURNAUX:-<non défini>}\"; ls -la \"${JOURNAUX:-/tmp/nope}\" 2>&1 | head; echo '--- registre'; find . -maxdepth 3 -name 'registre.txt' 2>/dev/null | head; echo '--- toutes-les-portes'; ls -la tools/toutes-les-portes.sh 2>&1", "description": "Localiser le registre des p … [7 caractères tronqués]`

  ```
JOURNAUX=<non défini>
ls: cannot access '/tmp/nope': No such file or directory
--- registre
./work/portes-n3-cloture/registre.txt
./work/portes-1106-01h03/registre.txt
./work/portes-1106-01h28/registre.txt
--- toutes-les-portes
-rwxr-xr-x. 1 stephane stephane 4422  2 nov 15:55 tools/toutes-les-portes.sh
  ```

- **bash** `{"command": "grep -rn \"eval_n2_propre\\|porte-n2\\|porte propre\" --include='*.sh' --include='*.md' --include='*.txt' --include='*.py' . 2>/dev/null | grep -v '^\\./\\.git' | head -50", "description": "Chercher les usages de eval_n2_propre et porte-n2"}`

  ```
[still running after 60000ms; moved to background job bash-3915]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/toutes-les-portes.sh"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/toutes-les-portes.sh</path>
<type>file</type>
<content>
1: #!/bin/bash
2: # toutes-les-portes.sh — LA PASSE COMPLÈTE, et l'instrument qui manquait.
3: #
4: # POURQUOI CETTE PORTE EXISTE. Le 12 octobre, `tools/porte-gain.sh` §9 exigeait un REFUS
5: # (`--attn-window` en réparti) que le v7 avait **délibérément retiré** en faisant voyager les
6: # trois réglages dans la trame (`main.rs:4432`). La porte ne pouvait donc plus passer — et
7: # personne ne l'a vu, parce que les portes étaient lancées **une par une**, à la main, quand
8: # on touchait la fonctionnalité du jour. Une porte qu'on croit verte et qui n'a pas tourné est
9: # exactement le défaut que ce dépôt traque (un drapeau inerte, une mesure qui ne mesure rien) :
10: # ici, appliqué aux instruments eux-mêmes.
11: #
12: # Ce que fait ce script, et ce qu'aucun autre ne faisait :
13: #   1. il lance **TOUTES** les `tools/porte-*.sh`, séquentiellement ;
14: #   2. il ne s'arrête PAS à la première rouge — il veut le tableau, pas la première tuile ;
15: #   3. il borne chaque porte dans le temps (`DELAI`, 1800 s par défaut) : une porte qui pend
16: #      est une porte ROU
… [3618 caractères tronqués]
  ```

- **bash** `{"command": "cat work/portes-1106-01h28/registre.txt 2>/dev/null | head -40; echo '--- lignes non vertes'; awk '$2 != 0' work/portes-1106-01h28/registre.txt 2>/dev/null; echo '--- 01h03'; awk '$2 != 0' work/portes-1106-01h03/registre.txt 2>/dev/null", "description": "Lire le registre des portes le p … [12 caractères tronqués]`

  ```
porte-adaptateur-sortie 0 74
porte-audit-drapeaux 0 181
porte-b1110-hybride 0 0
porte-balayage 0 1
porte-bloc-code 0 13
porte-bloc-linguistique 1 17
porte-bloc-maths 0 1
porte-bloc-tableaux 0 2
porte-budget 0 51
porte-bus 0 84
porte-bus-socket 0 98
porte-c4-retard 0 33
porte-cerveau 0 9
porte-consolidation 0 83
porte-coupe 0 149
porte-cycle-c2 0 139
porte-deepseek 0 0
porte-delais 0 23
porte-diff-couche 0 20
porte-document 0 7
porte-echange-experts 0 60
porte-episodique 0 199
porte-etat 0 0
porte-flux 0 27
porte-fusion 0 8
porte-gain 0 241
porte-greffe 0 791
porte-harnais-invariants 0 122
porte-homeostasie 0 612
porte-horloge 0 28
porte-indice 1 1130
porte-jeux 0 125
porte-jumeaux 0 31
porte-lecteur 0 0
porte-lecture 0 2
porte-m5-brouillon 0 1
porte-melange 1 137
porte-memoire 0 10
porte-miroir-blocs 0 9
porte-mistral 0 10
--- lignes non vertes
porte-bloc-linguistique 1 17
porte-indice 1 1130
porte-melange 1 137
porte-sessions 1 0
--- 79 vertes, 4 rouges ---
--- 01h03
porte-bloc-linguistique 1 17
  ```

- **bash** `{"command": "cat reports/n2-porte-propre.json 2>&1; echo '--- chaine_porte.sh'; cat work/n2ac/chaine_porte.sh; echo '--- chaine_porte.out'; cat work/n2ac/chaine_porte.out", "description": "Lire mesures et chaîne de la porte propre"}`

  ```
{
 "propre512_8k": {
  "fichier": "propre512-8k.pt",
  "val": "data/corpus_propre",
  "positions": "rope",
  "L128": 2.9726,
  "L256": 2.8988,
  "L512": 2.8443,
  "L1024": 2.7856
 },
 "propre512_8k_test": {
  "fichier": "propre512-8k.pt",
  "val": "/tmp/propre_test",
  "positions": "rope",
  "L128": 3.0649,
  "L512": 2.8875,
  "L1024": 2.8566
 },
 "propre128_32k": {
  "fichier": "propre128-32k.pt",
  "val": "data/corpus_propre",
  "positions": "rope",
  "L128": 2.9027,
  "L256": 2.9034,
  "L512": 3.0464,
  "L1024": 3.1107
 },
 "propre128_32k_test": {
  "fichier": "propre128-32k.pt",
  "val": "/tmp/propre_test",
  "positions": "rope",
  "L128": 3.015,
  "L512": 3.1104,
  "L1024": 3.1876
 },
 "entrainement_512": {
  "modele": "drave-n0-rope",
  "parametres": 34301224,
  "corpus": "data/corpus_propre/train.txt",
  "octets": 3244858,
  "pas": 8000,
  "seq": 512,
  "lot": 8,
  "lr": 0.0003,
  "graine": 1,
  "window": 512,
  "positions": "rope",
  "init": "work/n2j/base-wiki-45m.pt",
  "perte_finale": 0.8525079488754272,
  "ppl_val": 3.363862704237594,
  "jetons_val": 32768,
  "tetes": true,
  "drvm": "work/n2ac/propre512-8k.drvm",
  "sha256_drvm": "b2034de3cd0d84f4ea2481fe5f7b449eabf553
… [3020 caractères tronqués]
  ```

- **bash** `{"command": "cat work/n2ac/rope2048-20k.pt.json 2>&1; echo '--- 10k'; cat work/n2ac/rope2048-10k.pt.json 2>&1; echo '--- propre512 json'; cat work/n2ac/propre512-8k.pt.json 2>&1; echo '--- git status'; git status --porcelain | head -20; echo '--- git branch'; git branch --show-current", "description … [60 caractères tronqués]`

  ```
{
 "modele": "drave-n0-rope",
 "parametres": 34301224,
 "corpus": "data/wiki_fr/propre/train.txt",
 "octets": 186089472,
 "pas": 10000,
 "seq": 2048,
 "lot": 8,
 "lr": 0.0003,
 "graine": 1,
 "window": 2048,
 "positions": "rope",
 "init": "work/n2ac/rope2048-10k.pt",
 "perte_finale": 0.8965461254119873,
 "ppl_val": 2.4953209637199847,
 "jetons_val": 131072,
 "tetes": true,
 "drvm": "work/n2ac/rope2048-20k.drvm",
 "sha256_drvm": "91a302872988691e1a489ea1dea88a3e1787bd6ababaf637041ef2f3c1c6c529",
 "duree_s": 10220.861443519592
}
--- 10k
{
 "modele": "drave-n0-rope",
 "parametres": 34301224,
 "corpus": "data/wiki_fr/propre/train.txt",
 "octets": 186089472,
 "pas": 10000,
 "seq": 2048,
 "lot": 8,
 "lr": 0.0003,
 "graine": 1,
 "window": 2048,
 "positions": "rope",
 "init": "work/n2j/base-wiki-45m.pt",
 "perte_finale": 0.9408763647079468,
 "ppl_val": 2.6140776459917356,
 "jetons_val": 131072,
 "tetes": true,
 "drvm": "work/n2ac/rope2048-10k.drvm",
 "sha256_drvm": "c50beff61dc067b80690e9769e503e2c4e8e5184c0eb68277fcebd5bb0f4da69",
 "duree_s": 10224.105374336243
}
--- propre512 json
{
 "modele": "drave-n0-rope",
 "parametres": 34301224,
 "corpus": "data/corpus_propre/train.txt",
 "octets": 
… [1073 caractères tronqués]
  ```

- **bash** `{"command": "cat work/n2ac/chaine_2048_20k.sh; echo '--- log tail rope2048-20k'; tail -20 work/n2ac/rope2048-20k.log 2>&1", "description": "Lire la chaîne et le log du checkpoint récent"}`

  ```
#!/usr/bin/env bash
# chaine_2048_20k.sh — le complément 2 048 « mêmes pas » : 20 000 pas, comme le run 1 024 / 20 000.
set -u
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet || exit 1
export PYTHONPATH=. CUDA_VISIBLE_DEVICES=${1:-1}
~/gpu-env/bin/python work/n2ac/entrainer_rope.py \
  --corpus data/wiki_fr/propre/train.txt --canal data/wiki_fr/propre/train.canal \
  --seq 2048 --window 2048 --lot 8 --lr 3e-4 --graine 1 --dim 384 --expert-hidden 512 \
  --init work/n2j/base-wiki-45m.pt --pas 20000 \
  --sortie work/n2ac/rope2048-20k.pt --drvm work/n2ac/rope2048-20k.drvm \
  > work/n2ac/rope2048-20k.log 2>&1
echo "rope2048-20k fini $(date '+%H:%M:%S')"
--- log tail rope2048-20k
 "modele": "drave-n0-rope",
 "parametres": 34301224,
 "corpus": "data/wiki_fr/propre/train.txt",
 "octets": 186089472,
 "pas": 10000,
 "seq": 2048,
 "lot": 8,
 "lr": 0.0003,
 "graine": 1,
 "window": 2048,
 "positions": "rope",
 "init": "work/n2ac/rope2048-10k.pt",
 "perte_finale": 0.8965461254119873,
 "ppl_val": 2.4953209637199847,
 "jetons_val": 131072,
 "tetes": true,
 "drvm": "work/n2ac/rope2048-20k.drvm",
 "sha256_drvm": "91a302872988691e1a489ea1dea88a3e1787bd6ababaf637041ef2f3c1c6c529",
 "duree_s": 10
… [18 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-3915"}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "cat work/ressources.json 2>&1; echo '--- claims'; ls -la work/claims* 2>/dev/null; find . -maxdepth 2 -iname '*claim*' 2>/dev/null | head; echo '--- guard'; which hauru-gpu-guard 2>&1; systemctl --user list-timers 2>/dev/null | head -10", "description": "Vérifier claims GPU et garde-fou … [3 caractères tronqués]`

  ```
{
  "claims": [],
  "queue": []
}
--- claims
./work/msg-claims.txt
--- guard
/home/stephane/.local/bin/hauru-gpu-guard
NEXT                          LEFT LAST                              PASSED UNIT                           ACTIVATES
Fri 2026-11-06 21:20:01 EST    17s Fri 2026-11-06 21:19:31 EST      12s ago hauru-gpu-guard.timer          hauru-gpu-guard.service
Sat 2026-11-07 19:39:58 EST    22h Fri 2026-11-06 19:39:58 EST 1h 39min ago systemd-tmpfiles-clean.timer   systemd-tmpfiles-clean.service
Mon 2026-11-09 00:00:00 EST 2 days -                                      - drkonqi-coredump-cleanup.timer drkonqi-coredump-cleanup.service
Mon 2026-11-09 07:01:24 EST 2 days -                                      - financemeteo-catchup.timer     financemeteo@daily.service
-                                - Fri 2026-11-06 20:01:44 EST 1h 17min ago financemeteo-watch.timer       financemeteo@watch.service
-                                - Tue 2026-11-03 19:35:42 EST   3 days ago verif-affichage.timer          verif-affichage.service

6 timers listed.
Pass --all to see loaded but inactive timers, too.
  ```

- **bash** `{"command": "sed -n '1,120p' work/n2ac/eval_longueurs.py 2>&1", "description": "Lire eval_longueurs.py"}`

  ```
#!/usr/bin/env python3
"""eval_longueurs.py — la courbe de longueur d'un point de contrôle (absolu ou RoPE).

Le mètre est celui de N2 (`work/n2j/evalue_canal.py`) : canal fourni, fenêtres Van der Corput
dans des chunks de 8192 octets, 8 lots × 16 fenêtres. On peut demander n'importe quelle
longueur, y compris **1 000 octets** (la porte R1.1).

Usage :
  PYTHONPATH=. ~/gpu-env/bin/python work/n2ac/eval_longueurs.py <point.pt> \
      --longueurs 128,256,512,1000 [--rope] [--val data/wiki_fr/propre]
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

sys.path.insert(0, ".")
sys.path.insert(0, "work/n2j")

import torch  # noqa: E402

from tools.eval_n2_propre import charge, charger_bytes  # noqa: E402
import evalue_canal as ec  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("point")
    ap.add_argument("--longueurs", default="128,256,512")
    ap.add_argument("--rope", action="store_true")
    ap.add_argument("--val", default="data/wiki_fr/propre")
    ap.add_argument("--sortie", default=None)
    a = ap.parse_args()

    if a.rope:
        from work.n2ac.rope_model import charge_rope
        m = ch
… [732 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '55,100p' docs/pilotage/roadmap.md; echo '=== EN-COURS 75-145 ==='; sed -n '75,145p' docs/pilotage/en-cours.md", "description": "Lire les sections N2 de roadmap et en-cours"}`

  ```
L'ordre est **la valeur / le coût**, pas la date. La dernière mise à jour est le **2026-11-03 13 h 30**.

1. **R0 — le lecteur v0** : **R0.1, R0.2 et R0.3 sont mesurés** (51 pages ; récupération **1,000** à
   30 % sur 5 types et **249 questions**) ; **R0.4** ([tête](../theorie/glossaire/entrees/tete.md) de survol) et **R0.5** ([routeur](../theorie/glossaire/entrees/routeur.md)) sont
   **closes en négatif** — 0,540 contre BM25 0,720 sur le corpus gelé, et un signal qui prédit
   ([AUC](../theorie/glossaire/entrees/auc.md) 0,839) sans règle qui transfère.
   **R4.1 — le bloc tableaux** est **mesurée** (996 cellules, **802** exactes, texte plat **0/3**),
   **R4.2 — le bloc code** aussi (294 fichiers, 24/24 extraits, texte seul **0/3**) et **R4.3 —
   le bloc maths** (32 formules, 10/10 dérivées, surface **0/3**) ; **R4.4 est mesurée** sur
   **100 scans simulés** : la photo passe de **55,9 %** à **6,7 %** de [WER](../theorie/glossaire/entrees/wer.md) (test **5,7 %**) et la
   **préservation** du lecteur atteint **90–97 %** sur **4 familles sur 5** (propre **96,7 %** ;
   fax **56,7 %**, la limite d'information) ; les **colonnes** tombent de **89,4 %** à **0,5 %**,
   les **tableaux
… [8828 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"class NativeConfig\" -A 60 tools/native_model.py | head -80; echo '=== class NativeModel init ==='; grep -n \"class NativeModel\" -A 40 tools/native_model.py | head -60; echo '=== rope mentions ==='; grep -n \"rope\\|RoPE\\|position\" tools/native_model.py | head -30", "descri … [45 caractères tronqués]`

  ```
25:class NativeConfig:
26-    vocab: int = 256
27-    d_model: int = 224
28-    n_blocks: int = 6
29-    n_heads: int = 4
30-    expert_hidden: int = 288
31-    n_experts: int = 8
32-    top_k: int = 2
33-    kwta: float = 0.25
34-    window: int = 256
35-    max_pos: int = 2048
36-    thought_steps: int = 2
37-    early_blocks: tuple[int, ...] = (1, 3, 5)  # 0-based : après 2, 4, 6
38-    rsn_dim: int = 120
39-
40-
41-class SparseFFN(nn.Module):
42-    def __init__(self, cfg: NativeConfig):
43-        super().__init__()
44-        self.cfg = cfg
45-        self.router = nn.Linear(cfg.d_model, cfg.n_experts)
46-        self.gate = nn.Linear(cfg.d_model, cfg.n_experts * cfg.expert_hidden)
47-        self.up = nn.Linear(cfg.d_model, cfg.n_experts * cfg.expert_hidden)
48-        self.down = nn.Linear(cfg.n_experts * cfg.expert_hidden, cfg.d_model)
49-
50-    def forward(self, x):
51-        b, s, d = x.shape
52-        logits = self.router(x)
53-        poids, idx = logits.topk(self.cfg.top_k, dim=-1)
54-        poids = poids.softmax(-1)
55-        g = self.gate(x).view(b, s, self.cfg.n_experts, self.cfg.expert_hidden)
56-        u = self.up(x).view(b, s, self.cfg.n_experts, self.cfg.
… [3867 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,140p' work/n2ac/rope_model.py 2>&1; echo '=== vdc ==='; ls -la tools/vdc.py; head -30 tools/vdc.py", "description": "Lire rope_model.py et vdc"}`

  ```
#!/usr/bin/env python3
"""rope_model.py — la variante **positions relatives** du modèle natif (R1.1/R1.2).

Le modèle de `tools/native_model.py` ajoute une **position apprise absolue** (`self.pos`) et
compte sur les positions aléatoires à l'entraînement (N2.j2) : le gain à 512 octets est réel
(÷2,1 à ÷2,4) mais c'est une **astuce d'entraînement**, pas une propriété de l'architecture.
Ce module remplace la position absolue par un **RoPE** (rotation des q/k, aucune position
apprise) : le score d'attention ne dépend plus que de l'**écart** entre positions, donc
l'extrapolation en longueur est acquise par construction.

Rien n'est modifié dans `tools/` : les blocs réutilisent les **mêmes noms de paramètres**
(`ln1`, `qkv`, `out`, `ln2`, `ffn`), ce qui permet de charger un point de contrôle absolu
comme initialisation (`strict=False`, `pos` reste inutilisé).

Usage :
  PYTHONPATH=. python3 -c "from work.n2ac.rope_model import charge_rope; ..."
"""
from __future__ import annotations

import math

import torch
import torch.nn as nn
import torch.nn.functional as F

from tools.native_model import Block, NativeConfig, NativeModel, exporter_drvm


def rope(x: torch.Tensor, base: float = 10_00
… [4996 caractères tronqués]
  ```

- **bash** `{"command": "~/gpu-env/bin/python - <<'PY'\nimport torch, json\nck = torch.load('work/n2ac/rope2048-20k.pt', map_location='cpu', weights_only=False)\nprint(type(ck), list(ck.keys()))\nprint('config:', json.dumps(ck['config'], indent=1))\nsd = ck['state']\nks = list(sd.keys())\nprint('n state keys:', … [296 caractères tronqués]`

  ```
<class 'dict'> ['config', 'state']
config: {
 "vocab": 256,
 "d_model": 384,
 "n_blocks": 6,
 "n_heads": 4,
 "expert_hidden": 512,
 "n_experts": 8,
 "top_k": 2,
 "kwta": 0.25,
 "window": 2048,
 "max_pos": 2048,
 "thought_steps": 2,
 "early_blocks": [
  1,
  3,
  5
 ],
 "rsn_dim": 120
}
n state keys: 127
first 20 keys: ['embed.weight', 'pos.weight', 'blocks.0.ln1.weight', 'blocks.0.ln1.bias', 'blocks.0.qkv.weight', 'blocks.0.qkv.bias', 'blocks.0.out.weight', 'blocks.0.out.bias', 'blocks.0.ln2.weight', 'blocks.0.ln2.bias', 'blocks.0.ffn.router.weight', 'blocks.0.ffn.router.bias', 'blocks.0.ffn.gate.weight', 'blocks.0.ffn.gate.bias', 'blocks.0.ffn.up.weight', 'blocks.0.ffn.up.bias', 'blocks.0.ffn.down.weight', 'blocks.0.ffn.down.bias', 'blocks.1.ln1.weight', 'blocks.1.ln1.bias']
last 10 keys: ['bridge.bias', 'thought.weight', 'thought.bias', 'thought_in.weight', 'thought_in.bias', 'head_byte.weight', 'head_byte.bias', 'embed_canal.weight', 'head_rsn.weight', 'head_rsn.bias']
rope-ish keys: ['pos.weight']
  ```

- **bash** `{"command": "grep -n \"rope\\|NativeModel\\|import\" work/n2ac/entrainer_rope.py | head -30; echo '=== eval used in fiche? grep journaux ==='; grep -rn \"propre512-8k\\|eval_longueurs\" journal/2026-11-03* reports/rapport-n2-porte-propre.md 2>/dev/null | head -20", "description": "Vérifier l'archite … [38 caractères tronqués]`

  ```
2:"""entrainer_rope.py — la recette N2 avec positions **relatives** (R1.1/R1.2).
7:  - les blocs sont des `BlockRoPE` (`work/n2ac/rope_model.py`) : plus de table de positions ;
16:  PYTHONPATH=. ~/gpu-env/bin/python work/n2ac/entrainer_rope.py \
19:      --sortie work/n2ac/rope-20k.pt --drvm work/n2ac/rope-20k.drvm
21:from __future__ import annotations
23:import argparse
24:import json
25:import pathlib
26:import time
28:import torch
29:import torch.nn.functional as F
31:from tools.native_model import NativeConfig, exporter_drvm
32:from tools.entrainer_native import charger, charger_canal, lot, ppl
33:from work.n2ac.rope_model import NativeModelRoPE
45:    ap.add_argument("--sortie", default="work/n2ac/rope.pt")
46:    ap.add_argument("--drvm", default="work/n2ac/rope.drvm")
68:    modele = NativeModelRoPE(cfg).to(a.device)
98:    res = {"modele": "drave-n0-rope", "parametres": modele.nb_parametres(),
101:           "positions": "rope", "init": a.init,
=== eval used in fiche? grep journaux ===
reports/rapport-n2-porte-propre.md:33:- **Mètre** : `eval_longueurs.py --val data/corpus_propre --rope` (val et test du corpus propre,
reports/rapport-n2-porte-propre.md:107:- Modèles : `work
… [173 caractères tronqués]
  ```

- **bash** `{"command": "ls -la /tmp/propre_test 2>&1; echo '---'; grep -rn \"eval_n2_propre\" journal/ reports/ 2>/dev/null | head -20", "description": "Vérifier le corpus test temporaire et usages d'eval_n2_propre"}`

  ```
ls: cannot access '/tmp/propre_test': No such file or directory
---
journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/plan.md:9:- **Fichiers réservés** : `data/`, `tools/corpus*`, `tools/eval_n2_propre.py`,
journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/digest.md:5151:- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"eval_n2_propre.py — la porte honnête : PPL sur un corpus dédupliqué, et hors domaine.\n\nLe corpus de `data/corpus_propre/` est construit par `tools/corpus_propre.py` : passages\nrépétés retirés, split par chunks contigus, **zéro fenêtre de validation dans\ … [6378 caractères tronqués]`
journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/digest.md:5154:<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/eval_n2_propre.py</path>
journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/digest.md:5161:- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONPATH=. CUDA_VISIBLE_DEVICES=1 timeout 900 ~/gpu-env/bin/python tools/eval_n2_propre.py \\\n  /home/stephane/Data13TB/stephane/backups/n2/2026-10-31/artefacts/temoin-g1.pt --decomposition --longueurs 2>&1 | grep -v Loading", "de … [66 caractères tronqués]`
journal/sess
… [4838 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,60p' reports/rapport-n2-propre.md", "description": "Lire la fiche N2 propre (référence)"}`

  ```
# N2.h1 — Le corpus propre : la validation n'était pas tenue à l'écart, et la porte honnête vaut 3,09

> **Ligne de roadmap** : N2 · **Date** : 2026-11-01 · **Verdict** : le corpus de N2 se recopiait
> (**32,8 %** des fenêtres de validation étaient verbatim dans l'entraînement) ; dédupliqué, il
> perd **22,2 %** de son texte et la contamination tombe à **zéro**. La chaîne refaite vaut
> **3,0904** en domaine — pas 2,85 — et **16,70** sur de la littérature jamais vue : la
> porte < 2,5 est **redéfinie**, et elle est à **0,59**.

## La question

N2.d a montré que la PPL de N2 se mesurait sur un jeu où un tiers des fenêtres étaient
mémorisables (2,5862 sur les fenêtres contaminées contre 2,9795 sur les propres). La question
n'est plus « quel levier fait baisser la PPL » mais « **quel chiffre dit la vérité** ». Ce travail
construit le mètre, refait la chaîne dessus, et mesure ce que le mètre change.

## Le corpus propre — la méthode

`tools/corpus_propre.py` retire les passages répétés par **shingles de 96 octets** (hachage
roulant de Rabin-Karp, première occurrence gardée, runs ≥ 64 octets joints par `\n`), puis découpe
le texte nettoyé en **chunks contigus de 8 192 octets** dont un s
… [2123 caractères tronqués]
  ```

- **bash** `{"command": "cat ~/.local/bin/hauru-gpu-guard 2>&1 | head -80", "description": "Lire le garde-fou GPU"}`

  ```
#!/bin/bash
# hauru-gpu-guard — les GPU de Hauru sont exclusivement réservés à Drave.
# Tout serveur local d'inférence (llama-server, ollama, llama-cpp) est arrêté.
# Les tâches Drave (python tools/*, gpu-env, ref_logits) ne sont pas touchées.
set -u
LOG="${HAURU_GPU_LOG:-/tmp/hauru-gpu-guard.log}"
pids="$(nvidia-smi --query-compute-apps=pid,process_name --format=csv,noheader 2>/dev/null)" || exit 0
while IFS=, read -r pid name; do
    [ -n "${pid:-}" ] || continue
    pid="$(echo "$pid" | tr -d ' ')"; name="$(echo "$name" | tr -d ' ')"
    case "$name" in
        llama-server|ollama|llama-cpp)
            kill "$pid" 2>/dev/null && echo "$(date -Is) arrêté $name (pid $pid)" >> "$LOG"
            ;;
    esac
done <<< "$pids"
  ```

- **bash** `{"command": "sed -n '1,120p' tools/porte-ressources.sh 2>&1", "description": "Lire la porte ressources"}`

  ```
#!/bin/bash
# porte-ressources.sh — le registre des ressources tient : autotest et cohérence.
#
# POURQUOI CETTE PORTE EXISTE. Le registre `tools/ressources.py` est consultatif : il n'empêche
# pas un job de tourner, il rend le conflit visible. Une porte doit vérifier ce qui est
# vérifiable sans la machine : le code du registre (autotest des 9 cas : claim, conflit, file,
# admission, check) et la cohérence du registre courant (aucune ressource sur-réservée).
#
# CE QU'ELLE NE VÉRIFIE PAS : le réel (processus GPU non déclarés, charge CPU, espace disque) —
# c'est `--actual`, informatif, et le mapping processus→claim reste manuel. Les avertissements
# de stockage (RAID à 33 Gio) et de NUMA (un GPU avec des fils sur cpu1) restent VISIBLES mais
# ne font pas échouer la porte : ce sont des limites nommées, pas des régressions.
#
# Usage : tools/porte-ressources.sh
set -u
cd "$(dirname "$0")/.."
echo "=== PORTE RESSOURCES — REGISTRE, CLAIMS, COHÉRENCE ==="
if ! python3 tools/ressources.py --autotest; then
    echo "  ❌ autotest du registre en échec"
    exit 1
fi
if ! python3 tools/ressources.py --check; then
    echo "  ❌ registre incohérent : une ressource est sur-réservée"
    exit 1
… [591 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"def ppl\" -A 40 work/n2ac/evalue_canal.py 2>&1; echo '--- wiki_fr propre'; ls -la data/wiki_fr/propre/ 2>&1 | head", "description": "Lire le mètre ppl et le corpus wiki"}`

  ```
grep: work/n2ac/evalue_canal.py: No such file or directory
--- wiki_fr propre
total 603712
drwxr-xr-x. 1 stephane stephane       160  1 nov 18:42 .
drwxr-xr-x. 1 stephane stephane        36  1 nov 11:54 ..
-rw-r--r--. 1 stephane stephane  18604032  1 nov 18:30 dev.txt
-rw-r--r--. 1 stephane stephane  10330245  1 nov 18:36 test.canal
-rw-r--r--. 1 stephane stephane  10330245  1 nov 11:54 test.txt
-rw-r--r--. 1 stephane stephane 186089472  1 nov 18:38 train.canal
-rw-r--r--. 1 stephane stephane 186089472  1 nov 18:42 train.canal-placebo
-rw-r--r--. 1 stephane stephane 186089472  1 nov 11:54 train.txt
-rw-r--r--. 1 stephane stephane  10330112  1 nov 18:35 val.canal
  ```

- **bash** `{"command": "grep -n \"def ppl\" -A 45 work/n2j/evalue_canal.py; echo '--- entete'; sed -n '1,40p' work/n2j/evalue_canal.py", "description": "Lire le mètre evalue_canal"}`

  ```
28:def ppl(m, data, canal, long=128, n_lots=8, avec_canal=True):
29-    m.eval(); tot, n = 0.0, 0
30-    with torch.no_grad():
31-        for k in range(n_lots):
32-            x, c = fenetres(data, canal, 16, long + 1, k * 16)
33-            logits = m(x[:, :-1], canal=(c[:, :-1] if (avec_canal and c is not None) else None))["logits"]
34-            tot += float(F.cross_entropy(logits.reshape(-1, 256), x[:, 1:].reshape(-1), reduction="sum"))
35-            n += x[:, 1:].numel()
36-    return round(math.exp(tot / n), 4)
37-
38-
39-def melange_texte(texte, graine, tout):
40-    rng = random.Random(graine)
41-    sortie, mot = [], []
42-    for ch in texte:
43-        if ch.isalpha() or ch in "'’":
44-            mot.append(ch)
45-        else:
46-            if mot:
47-                sortie.append(_mot(''.join(mot), rng, tout)); mot = []
48-            sortie.append(ch)
49-    if mot:
50-        sortie.append(_mot(''.join(mot), rng, tout))
51-    return ''.join(sortie)
52-
53-
54-def _mot(m, rng, tout):
55-    l = list(m)
56-    if len(l) <= 3:
57-        return m
58-    if tout:
59-        rng.shuffle(l); return ''.join(l)
60-    mid = l[1:-1]; rng.shuffle(mid)
61-    return l[0] 
… [2156 caractères tronqués]
  ```

- **bash** `{"command": "PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. CUDA_VISIBLE_DEVICES=1 ~/gpu-env/bin/python - <<'PY'\nimport torch, time\nfrom tools.eval_n2_propre import charge, charger_bytes\nt0=time.time()\nm = charge('work/n2ac/rope2048-20k.pt', 'cuda')\nprint('charge ok', time.time()-t0, 'params', m.nb_par … [424 caractères tronqués]`

  ```
charge ok 1.146162986755371 params 34301224
logits (1, 256, 256) early 3
ppl 256 10.93146352563721
  ```

- **bash** `{"command": "date '+%Y-%m-%d %H:%M:%S'; PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. CUDA_VISIBLE_DEVICES=1 ~/gpu-env/bin/python tools/eval_n2_propre.py work/n2ac/rope2048-20k.pt --device cuda; echo \"EXIT=$?\"; date '+%Y-%m-%d %H:%M:%S'", "description": "Évaluer le checkpoint récent avec eval_n2_propre.p … [30 caractères tronqués]`

  ```
started background job bash-4009
  ```

- **bash** `{"command": "date '+%Y-%m-%d %H:%M:%S'; PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. CUDA_VISIBLE_DEVICES=0 ~/gpu-env/bin/python work/n2ac/eval_longueurs.py work/n2ac/rope2048-20k.pt --rope --longueurs 128,256,512,1024 --val data/corpus_propre; echo \"EXIT=$?\"; date '+%Y-%m-%d %H:%M:%S'", "description":  … [90 caractères tronqués]`

  ```
started background job bash-4010
  ```

- **bash** `{"command": "ls -la work/n2h/*.pt 2>/dev/null | head -10; echo '--- n2h json'; ls work/n2h/*.json 2>/dev/null | head -5", "description": "Vérifier checkpoints absolus disponibles"}`

  ```
-rw-r--r--. 1 stephane stephane 47302035 31 oct 23:12 work/n2h/A-propre-g1.pt
-rw-r--r--. 1 stephane stephane 47302035 31 oct 23:35 work/n2h/A-propre-g2.pt
-rw-r--r--. 1 stephane stephane 47302035 31 oct 23:58 work/n2h/A-propre-g3.pt
-rw-r--r--. 1 stephane stephane 86626843  1 nov 04:20 work/n2h/base-capacite.pt
-rw-r--r--. 1 stephane stephane 47301903 31 oct 23:18 work/n2h/base-mixte.pt
-rw-r--r--. 1 stephane stephane 47302035 31 oct 22:35 work/n2h/base-propre.pt
-rw-r--r--. 1 stephane stephane 86622655  1 nov 04:52 work/n2h/CAP-g1.pt
-rw-r--r--. 1 stephane stephane 86622655  1 nov 05:24 work/n2h/CAP-g2.pt
-rw-r--r--. 1 stephane stephane 47302035  1 nov 00:10 work/n2h/C-propre-g1.pt
-rw-r--r--. 1 stephane stephane 47302035  1 nov 00:21 work/n2h/C-propre-g2.pt
--- n2h json
work/n2h/A-propre-g1.json
work/n2h/A-propre-g2.json
work/n2h/A-propre-g3.json
work/n2h/base-capacite.pt.json
work/n2h/base-mixte.pt.json
  ```

- **bash** `{"command": "grep -rn \"2,4759\\|2.4759\\|2,3911\\|2.3911\\|2,4373\\|2.4373\\|2,3522\\|2.3522\" reports/*.md reports/*.json docs/pilotage/*.md 2>/dev/null | head -30", "description": "Traquer les chiffres de la fenêtre 1024"}`

  ```
reports/rapport-n2-production-fenetre.md:10:> **sous 2,5 sur la validation du grand corpus** (2,3911 à 1 000, 2,3522 à 2 000) — une première
reports/rapport-n2-production-fenetre.md:92:à partir de 1 000 octets — **2,4759** à 1 000, **2,4373** à 2 000. Ce n'est pas la porte (qui se
reports/rapport-n2-production-fenetre.md:113:  (**2,3911** et **2,3522**) et à **2,53 / 2,48** sur la validation française ;
reports/m7-frequence.json:3498:     -0.028352262861581594,
reports/m7-frequence.json:4058:     -0.028352262861581594,
reports/m7-frequence.json:4842:     -0.028352262861581594,
reports/m7-frequence.json:5392:     -0.06676534126391104
reports/n2-production-fenetre.json:128:    "1000": 2.4759,
reports/n2-production-fenetre.json:129:    "2000": 2.4373
reports/n2-production-fenetre.json:257:    "1000": 2.3911,
reports/n2-production-fenetre.json:258:    "2000": 2.3522
reports/restitution-udhr.json:56:  "exactitude_jamais_vue": 78.62745821475983
docs/pilotage/chantiers.md:93:**N2** : 200 k pas (**3,16 / 5,61 / 7,28 / 8,00**) puis la **fenêtre 1 024** — **2,4759 / 2,4373 au grand
docs/pilotage/en-cours.md:122:| **N — le natif** | **N2, N4** | N2 : **fenêtre 1 024 — 2,3911 / 2,3522 au grand
… [2038 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,70p' reports/rapport-n2-production-fenetre.md", "description": "Lire la fiche production fenêtre"}`

  ```
# N2 — La production à fenêtre entraînée (512 / 1 024 / 2 048) et le compute qui va avec

> **Ligne de roadmap** : N2 (le modèle de production) · **Date** : 2026-11-03 · **Verdict** :
> à **octets ajoutés constants** (61,4 Mo, le budget de N2.ac), les trois fenêtres écrasent N2.ac
> et le run de 200 000 pas ; **1 024 est la meilleure au long** (2,7342 à 2 000 octets) et **512 la
> meilleure hors domaine** (anglais 7,05, wikitext2 7,90), **2 048 ne paie pas** (3 750 pas
> seulement). En poussant la fenêtre 1 024 à **30 000 pas (307 Mo)**, le modèle de production
> atteint **2,9121** en domaine à 128 octets (60 000 pas, 552 Mo), **2,5276** à 1 000, **2,4761** à
> 2 000, et il passe
> **sous 2,5 sur la validation du grand corpus** (2,3911 à 1 000, 2,3522 à 2 000) — une première
> pour un modèle natif, **obtenue par la fenêtre et non en rabotant la longueur**. Le même compute
> à fenêtre 128 (200 k pas, 205 Mo) donne 3,1591 à 128 et **8,2262** à 1 000 : la fenêtre n'est pas
> un raffinement, c'est la condition pour que le compute serve au-delà de 128 octets.

## La question

La fiche [`rapport-n2-fenetre`](rapport-n2-fenetre.md) a montré qu'à **octets ajoutés constants**
(61,4 Mo, le b
… [3241 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"A23\" docs/ reports/ journal/ 2>/dev/null | head -20", "description": "Chercher la note A23"}`

  ```
lp9qnz4jPO6DHumXX3daNRBjD0YJqv1OAJ3SqHZ2jK0M1zu3hx0cKBBUthjZl8s366ZzfjSXfsw97BhCAOEGJI4c79y54rehwrbXqvqiGfl5b4mx53sHpsKSbj+6MCu8PorXNdwKGJKiZdkBcoiK8/6CsqxWpyItjcHduqhEANAUF/AIJMovlXYzJVP9AWkt5ySp0BErtLaC9OKNWUs82lK8lASKigcgO0dNODSDM6x0QSBEIY2xRTrtVtpGOf6f3wiGB5OZa/PBqyhQ6hjlKzPSmcSIYZuKOp1pW1jIpEwpBjlk+g3NxPZuxTM4S8laNm1DEO15E+XBNDnak3Rc/4EEKg44tFb6WEVq1cvSBGFs9kJgIElWbKDZt5M2CcDoXeB8EWiE1TOoGEb2OsOJUzjgLdNHb/gDVVBGlsLotzdOeqHTlM9O+8lHKXuZA5thYniuwjCLwcGwzK4oGCAKHi6XD4Rsvts5kcrgbMT9w/m7J3IHSSKEc+e++tLgENGDxUgnBKIix4ApwYYhC9xA6YCAxJ00HR3TPTUkbDezYrX6NypMj3t3Xg70rE/N+ofoyhmvroXtW6MV1ykx3kvTHFYOv0IyaHHjW4Z/bwE3zqlgbaiEfn77F8yUEfA3qOEKehZMIisln1AzmADDAAT/5jbVCg/sTC9XUsnFA3HgP+V+LUO8ugB9zvnXqXvPgBb9dez/j95+g2RFLub1xLZ/xjShj6GRBVezmjtjsuSeue9wnlCFeKi9gslo3begrEbef86FNtT/PwjRu7YZndZa2p7+oJRdNAOPMwoQ2fI0nfv4tFli6/0XGBhlgxbgJG6W2DUBGiz6CBcgzF8BA5hElj0AIHsFe+PbcuE3Mxe/ioqo/CeZeQ4WiuMMMCmS4fkIZlCHr64ghUqkEI02DigU1u3H94WO8HIZeLtB/s8GLvyf+QV/9Dh5Kf85RtreQjHGINOmAsviG7NqKPWM77OJwHaTvKTBe/a2iofPq17+q18zGiMP2KU+3bDbJ6iKUmljlFmWHoQZ0eRWIt3JscqxGObn/33NHy0ZgGGGibDRYLLSzFUspx0JVKpvqMSkUnftmfcZBlNAJdBKg1riuUxnPSiQ6MZuqd1dEz0OHz1r2gzyG6+CfikZFW7GQsJvoMzoXYU+5ntAWPH+wAw4zVi2//KcrczG5UXjbBcN+yPrldjcdu69
… [48731 caractères tronqués]
  ```

### 👤 Utilisateur

background job bash-4010 (bash: date '+%Y-%m-%d %H:%M:%S'; PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. CUDA_VISIBLE_DEVICES=0 ~/gpu-env/bin/python work/n2ac/eval_longueurs.py work/n2ac/rope2048-20k.pt --rope --longueurs 128,256,512,1024 --val data/corpus_propre; echo "EXIT=$?"; date '+%Y-%m-%d %H:%M:%S') finished [status: completed, exit code: 0]. Read its output with job_output.

### 👤 Utilisateur

background job bash-4009 (bash: date '+%Y-%m-%d %H:%M:%S'; PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. CUDA_VISIBLE_DEVICES=1 ~/gpu-env/bin/python tools/eval_n2_propre.py work/n2ac/rope2048-20k.pt --device cuda; echo "EXIT=$?"; date '+%Y-%m-%d %H:%M:%S') finished [status: completed, exit code: 0]. Read its output with job_output.

### 🤖 Assistant

⏵ Lecture des résultats de la porte propre et du mètre RoPE

Les deux évaluations sont terminées ; je récupère leurs sorties.

- **job_output** `{"job_id": "bash-4009"}`

  ```
2026-11-06 21:25:14
{"fichier": "rope2048-20k.pt", "params": 34301224, "val": 12.9098, "test": 12.5881, "litterature": 11.5343, "litterature_propre": 11.942, "anglais": 16.9982, "wikitext2": 17.8491, "permute": 272.4992}
EXIT=0
2026-11-06 21:25:37
[status: completed, exit code: 0]
  ```

- **job_output** `{"job_id": "bash-4010"}`

  ```
2026-11-06 21:25:15
  L128 : 5.4773
  L256 : 5.0476
  L512 : 4.8859
  L1024 : 4.6321
{"fichier": "rope2048-20k.pt", "val": "data/corpus_propre", "positions": "rope", "L128": 5.4773, "L256": 5.0476, "L512": 4.8859, "L1024": 4.6321}
EXIT=0
2026-11-06 21:25:24
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "date '+%Y-%m-%d %H:%M:%S'; PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. CUDA_VISIBLE_DEVICES=0 ~/gpu-env/bin/python work/n2ac/eval_longueurs.py work/n2ac/propre512-8k.pt --rope --longueurs 128,256,512,1024 --val data/corpus_propre; echo \"EXIT=$?\"; date '+%Y-%m-%d %H:%M:%S'", "description":  … [80 caractères tronqués]`

  ```
started background job bash-4042
  ```

- **bash** `{"command": "date '+%Y-%m-%d %H:%M:%S'; PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. CUDA_VISIBLE_DEVICES=1 ~/gpu-env/bin/python tools/eval_n2_propre.py work/n2h/A-propre-g1.pt --device cuda; echo \"EXIT=$?\"; date '+%Y-%m-%d %H:%M:%S'", "description": "Contrôle eval_n2_propre sur un checkpoint absolu N2. … [30 caractères tronqués]`

  ```
started background job bash-4044
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json, pathlib, datetime\nrows=[]\nfor j in pathlib.Path('work').rglob('*.pt.json'):\n    p=j.with_suffix('')  # remove .json -> .pt\n    try:\n        d=json.loads(j.read_text())\n    except Exception as e:\n        continue\n    mtime=datetime.datetime.fromtime … [847 caractères tronqués]`

  ```
date               taille      param    pas   seq   win   pos  ppl_val  checkpoint  (corpus, init)
2026-11-02 04:27   130.89   34301224  20000   128  None  None 3.683441  work/n2j/base-34m-canal.pt
                 corpus=data/wiki_fr/propre/train.txt init=None
2026-11-02 05:38   130.89   34301224  20000   128  None  None 3.689124  work/n2j/base-34m-canal-g2.pt
                 corpus=data/wiki_fr/propre/train.txt init=None
2026-11-02 10:48   130.89   34301224  20000   128  None  None 3.823934  work/n2w/base-big.pt
                 corpus=data/wiki_big/propre/train.txt init=None
2026-11-02 11:09   130.89   34301224  20000   128  None  None 3.393584  work/n2w/base-big-canal.pt
                 corpus=data/wiki_big/propre/train.txt init=None
2026-11-02 12:10   130.89   34301224  60000   128  None  None 3.260694  work/n2w/big-60k.pt
                 corpus=data/wiki_big/propre/train.txt init=None
2026-11-02 12:10   130.88   34301224  60000   128  None  None 3.597846  work/n2w/fr-60k.pt
                 corpus=data/wiki_fr/propre/train.txt init=None
2026-11-02 13:23   130.89   34301224  60000   128  None  None 3.355563  work/n2w/mix-60k.pt
                 corpus=data/wiki_mix/propre/t
… [6544 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib, re\nfor p in sorted(pathlib.Path('reports').glob('rapport-n2-*.md')):\n    t=p.read_text(errors='replace')\n    lines=t.splitlines()\n    titre=next((l for l in lines if l.startswith('# ')), '')[:120]\n    date=''\n    for l in lines[:12]:\n        m=re … [413 caractères tronqués]`

  ```
rapport-n2-200k.md
  # N2.ae — 200 000 pas sur le mélange 1 Go : −0,33 en domaine, −1,06 en largeur, et la porte 2,5 à un million de pas
  date=2026-11-02 | à recette constante (34,3 M,
rapport-n2-34m-distille.md
  # N2.r — Le 34,3 M distillé : **3,69**, le meilleur modèle de la nuit, et la courbe plate
  date=2026-11-02 | le modèle de **34,3 M** distillé
rapport-n2-anglais-34m.md
  # N2.w — L'anglais à 34,3 M distillé : 3,77, et 4,18 à 512 octets
  date=2026-11-02 | la chaîne anglaise complète
rapport-n2-anglais-distille.md
  # N2.n — La distillation anglaise : 4,42 → 3,94, la chaîne complète sur 204 Mo
  date=2026-11-01 | le professeur 23,57 M entraîné
rapport-n2-anglais.md
  # N2.m — L'anglais seul : 4,42 sur 204 Mo, et ce que le multilingue coûte (1,6 PPL)
  date=2026-11-01 | la base **anglaise
rapport-n2-budget.md
  # N2 — le budget paie, les quatre sources coûtent, et la validation n'est pas tenue à l'écart
  date=2026-10-31 | le budget
rapport-n2-canal-34m.md
  # N2.z — Le canal à 34,3 M : 4,00 → 3,51, le meilleur modèle de la nuit
  date=2026-11-02 | le canal de structure, qui
rapport-n2-canal-distille.md
  # N2.x — La distillation du canal : −0,03 en domaine, +0,24 à 512 o
… [5069 caractères tronqués]
  ```

### 👤 Utilisateur

background job bash-4042 (bash: date '+%Y-%m-%d %H:%M:%S'; PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. CUDA_VISIBLE_DEVICES=0 ~/gpu-env/bin/python work/n2ac/eval_longueurs.py work/n2ac/propre512-8k.pt --rope --longueurs 128,256,512,1024 --val data/corpus_propre; echo "EXIT=$?"; date '+%Y-%m-%d %H:%M:%S') finished [status: completed, exit code: 0]. Read its output with job_output.

### 👤 Utilisateur

background job bash-3915 (bash: grep -rn "eval_n2_propre\|porte-n2\|porte propre" --include='*.sh' --include='*.md' --include='*.txt' --include='*.py' . 2>/dev/null | grep -v '^\./\.git' | head -50) finished [status: completed, exit code: 0]. Read its output with job_output.

### 👤 Utilisateur

background job bash-4044 (bash: date '+%Y-%m-%d %H:%M:%S'; PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. CUDA_VISIBLE_DEVICES=1 ~/gpu-env/bin/python tools/eval_n2_propre.py work/n2h/A-propre-g1.pt --device cuda; echo "EXIT=$?"; date '+%Y-%m-%d %H:%M:%S') finished [status: completed, exit code: 0]. Read its output with job_output.

- **job_output** `{"job_id": "bash-4042"}`

  ```
2026-11-06 21:28:03
  L128 : 2.9726
  L256 : 2.8988
  L512 : 2.8443
  L1024 : 2.7856
{"fichier": "propre512-8k.pt", "val": "data/corpus_propre", "positions": "rope", "L128": 2.9726, "L256": 2.8988, "L512": 2.8443, "L1024": 2.7856}
EXIT=0
2026-11-06 21:28:15
[status: completed, exit code: 0]
  ```

- **job_output** `{"job_id": "bash-4044"}`

  ```
2026-11-06 21:28:04
{"fichier": "A-propre-g1.pt", "params": 11816136, "val": 3.0971, "test": 3.2098, "litterature": 15.9854, "litterature_propre": 17.0838, "anglais": 60.6957, "wikitext2": 59.729, "permute": 1356.6433}
EXIT=0
2026-11-06 21:28:26
[status: completed, exit code: 0]
  ```

- **job_output** `{"job_id": "bash-3915"}`

  ```
./reports/rapport-n2-propre.md:143:  [`tools/eval_n2_propre.py`](../tools/eval_n2_propre.py) · agrégat
./reports/rapport-n2-diversite.md:74:  [`tools/eval_n2_propre.py`](../tools/eval_n2_propre.py).
./reports/rapport-n2-combine.md:57:  [`tools/eval_n2_propre.py`](../tools/eval_n2_propre.py).
./reports/rapport-n2-corpus-elargi.md:63:  [`tools/eval_n2_propre.py`](../tools/eval_n2_propre.py).
./reports/rapport-file-taches.md:51:| T09 | N2 | La porte propre (0,29 manquant à 2,7856) : données ou capacité | reports/n2-*, work/n2ac/, tools/entrainer_native.py, GPU | recette N2 1 024 | aucun externe ; GPU libres (0 %) | python3 tools/eval_n2_propre.py <checkpoint> (pas de commande unique) | P0 |
./reports/rapport-file-taches.md:53:| T11 | N4 | Consigne courte : construire le jeu, entraîner, évaluer tenu à l'écart (24/24 vus, 0/4 tenus) | backlog/N4-usage-sft.md ; reports/n4-* ; N2/GPU | recette N2 | aucun externe ; GPU libres | python3 tools/eval_n2_propre.py <checkpoint> (pas de commande unique) | P1 |
./reports/rapport-file-taches.md:135:| H12 | eval_n2_propre.py exige un checkpoint | argparse : point positionnel | Pas de commande unique pour N2 ; nommer le checkpoint |
./reports/rapport
… [21706 caractères tronqués]
  ```

- **bash** `{"command": "date '+%H:%M:%S'; PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. CUDA_VISIBLE_DEVICES=0 ~/gpu-env/bin/python tools/eval_n2_propre.py work/n2ac/propre512-8k.pt --device cuda; echo \"EXIT=$?\"; date '+%H:%M:%S'", "description": "Mesurer la porte avec le mauvais mètre (absolu)", "run_in_background … [8 caractères tronqués]`

  ```
started background job bash-4073
  ```

- **bash** `{"command": "echo '--- tracked?'; git ls-files work/n2ac/rope_model.py work/n2ac/eval_longueurs.py work/n2ac/entrainer_rope.py tools/eval_n2_propre.py; echo '--- ignore'; git check-ignore -v work/n2ac/rope_model.py work/n2ac/eval_longueurs.py 2>&1; echo '--- gitignore work'; grep -n \"work\" .gitign … [86 caractères tronqués]`

  ```
--- tracked?
tools/eval_n2_propre.py
--- ignore
.gitignore:23:work/	work/n2ac/rope_model.py
.gitignore:23:work/	work/n2ac/eval_longueurs.py
--- gitignore work
23:work/
  ```

- **bash** `{"command": "sed -n '78,125p' reports/rapport-n2-production-fenetre.md; echo '=== per-seed A-propre'; cat work/n2h/A-propre-g1.json 2>&1 | head -30", "description": "Lire les deux validations de production et le JSON A-propre-g1"}`

  ```
| run | octets totaux | 128 | 512 | 1 000 | 2 000 | litt. | angl. | wt2 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 200 k × 128 | 205 Mo | 3,1591 | 3,6577 | 8,2262 | 12,8723 | 5,6056 | 7,2770 | 8,0018 |
| **1 024, 30 k pas** | **307 Mo** | **2,9943** | **2,7221** | **2,6143** | **2,5628** | **5,3122** | **6,5118** | **7,1544** |
| écart | | −0,165 | −0,936 | −5,612 | −10,310 | −0,293 | −0,765 | −0,847 |

Trois choses :
1. **à 128 octets, le compute paie encore** : 3,1591 → 2,9943 (−0,165) pour 1,5× les octets ;
2. **au-delà, l'écart n'est plus une marge** : −0,94 à 512, −5,6 à 1 000, −10,3 à 2 000 ;
3. **le hors domaine s'améliore avec lui** : anglais 7,28 → **6,51**, wikitext2 8,00 → **7,15**,
   littérature 5,61 → **5,31**. La fenêtre entraînée **ne coûte pas la largeur** : elle la sert.

Et le fait le plus net : sur la **validation du grand corpus**, ce modèle passe **sous 2,5**
à partir de 1 000 octets — **2,4759** à 1 000, **2,4373** à 2 000. Ce n'est pas la porte (qui se
mesure sur le corpus propre, fiche [`n2-porte-propre`](rapport-n2-porte-propre.md)) mais c'est la
première fois qu'un modèle natif passe 2,5 sur une validation tenue à part, et il le fait **avec
la fenê
… [2572 caractères tronqués]
  ```

- **bash** `{"command": "ls reports/pensee-*.json 2>/dev/null | tail -10; echo '--- exemple'; python3 -c \"\nimport json,pathlib\nfor p in sorted(pathlib.Path('reports').glob('pensee-*.json'))[-2:]:\n    print('###',p)\n    d=json.loads(p.read_text())\n    print(type(d).__name__, list(d)[:20] if isinstance(d,di … [133 caractères tronqués]`

  ```
reports/pensee-v11.json
reports/pensee-v12.json
reports/pensee-v9.json
reports/pensee-variance.json
reports/pensee-verbe-gv.json
reports/pensee-verite.json
reports/pensee-votante3.json
reports/pensee-votante.json
reports/pensee-vote.json
reports/pensee-vrais-absents.json
--- exemple
### reports/pensee-vote.json
dict ['date', 'ligne', 'portes', 'looks', 'erreurs', 'cause', 'limites']
{"date": "2026-11-02", "ligne": "B13", "portes": "84/84", "looks": {"3": {"but0": 0, "but1": 20}, "5": {"but0": 0, "but1": 20}, "9": {"but0": 0, "but1": 19}}, "erreurs": {"3": 0.028, "5": 0.009, "9": 0.001}, "cause": "cycle (3,0)<->(4,0)", "limites": ["un seul tirage", "toy"]}
### reports/pensee-vrais-absents.json
dict ['date', 'ligne', 'portes', 'phrases_reelles', 'liens', 'absents_mesures', 'absents_reels', 'limites']
{"date": "2026-11-02", "ligne": "B13", "portes": "140/140", "phrases_reelles": 432, "liens": 116, "absents_mesures": 0, "absents_reels": 5, "limites": ["le coref n'est pas annoté pour les absents", "5 phrases", "heuristique seule"]}
  ```

- **bash** `{"command": "sed -n '1,120p' docs/methode/portes.md", "description": "Lire la méthode des portes"}`

  ```
# Les portes : lancer, lire le verdict, ne pas se tromper de rouge

> Document de tâche, chargé depuis [`AGENTS.md`](../../AGENTS.md). À lire **avant de lancer ou de lire les portes**.

## La commande

```bash
bash tools/toutes-les-portes.sh
```

Elle lance **toutes** les `tools/porte-*.sh`, séquentiellement, **sans s'arrêter à la première rouge** (on veut le
[tableau](../theorie/glossaire/entrees/tableau.md), pas la première tuile), et borne **chaque** [porte](../theorie/glossaire/entrees/porte.md) à `DELAI=1800` s. Durée observée d'une passe complète :
**1 h 30 – 2 h** sur Hauru (**83 portes** ; certaines entraînent de petits modèles, d'autres utilisent les [GPU](../theorie/glossaire/entrees/gpu-quadro-rtx-5000-miroir-vram-deport.md) ;
`porte-deepseek` est **hors réseau** et rapide). La dernière passe complète à **82 portes** (03/11 11 h 30, **machine au repos**, **1 h 48**) a donné
**80 vertes, 2 rouges** (les 2 connues : `indice`, `melange`) ;
`porte-reparti-moteur` (ré-étalonnée à 8,7434) et `porte-homeostasie` (auto-générée) sont **vertes** ;
la liste et le diagnostic sont dans
[`references-non-regression.md`](../pilotage/references-non-regression.md). `porte-deepseek` est **
… [3931 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,80p' tools/porte-produit.sh", "description": "Lire une porte récente comme modèle de style"}`

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
… [1844 caractères tronqués]
  ```

### 👤 Utilisateur

background job bash-4073 (bash: date '+%H:%M:%S'; PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. CUDA_VISIBLE_DEVICES=0 ~/gpu-env/bin/python tools/eval_n2_propre.py work/n2ac/propre512-8k.pt --device cuda; echo "EXIT=$?"; date '+%H:%M:%S') finished [status: completed, exit code: 0]. Read its output with job_output.

- **job_output** `{"job_id": "bash-4073"}`

  ```
21:32:07
{"fichier": "propre512-8k.pt", "params": 34301224, "val": 8.0225, "test": 8.0126, "litterature": 18.5021, "litterature_propre": 18.8906, "anglais": 43.2434, "wikitext2": 47.3566, "permute": 1404.2994}
EXIT=0
21:32:28
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "sed -n '40,60p' reports/rapport-file-taches.md; echo '...'; sed -n '125,145p' reports/rapport-file-taches.md; echo '...'; sed -n '185,200p' reports/rapport-file-taches.md", "description": "Lire les constats A23 sur N2"}`

  ```
| T05 | PRODUIT | Écrire la doc d'usage docs/produit/ : commandes, exemples, limites, codes de sortie | docs/produit/ (neuf) ; tools/drave.py | produit v0 (62dad657) | aucun | python3 tools/drave.py --help ; python3 tools/drave.py analyser "Le chat dort sur le toit." ; python3 tools/drave.py evaluer ; python3 tools/drave.py rejouer "Le chat dort." ; python3 tools/verifier_liens.py | P0 |
| T06 | PILOTAGE | Mettre l'état B13 à jour : 222/222, T132/T133 verts, 17 spans, passe du 06/11, prochaine action | docs/pilotage/en-cours.md, roadmap.md, chantiers.md, plan-travail.md | T03, T05 | un seul écrivain (agent principal) | python3 tools/revue_documentation.py ; python3 tools/verifie_en_cours.py ; python3 tools/taille_documents.py | P0 |
| T07 | PILOTAGE | Références de non-régression : 84 portes, ligne porte-produit, 4 rouges nommées (indice, melange, sessions, bloc-linguistique), lecteur vert | docs/pilotage/references-non-regression.md | T01 | aucun | ls tools/porte-*.sh ; bash tools/porte-produit.sh ; bash tools/porte-sessions.sh ; bash tools/porte-bloc-linguistique.sh | P1 |
| T08 | DOC | Corriger le double ## 9 de plan-travail.md (lignes 163 et 403) ; corriger le commentaire « 81 
… [7717 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"N2\\|n2\" docs/pilotage/references-non-regression.md | head -20; echo '---'; sed -n '1,40p' docs/pilotage/references-non-regression.md", "description": "Vérifier les rouges tolérées et N2"}`

  ```
19:> `porte-sessions` (coordination, rejouée verte à 08 h 10 après la pause de N2/S).
28:> (journaux `/tmp/portes-1101-n2h`). Mêmes rouges que la passe du 31/10 : `porte-indice` (921 s),
33:> (journaux `/tmp/portes-1031-n2d`) : mêmes rouges ; `porte-ocr` (48 s) était verte.
---
# Références de non-régression

> **Passe — 2026-11-06 :** 83 portes, **79 vertes, 4 rouges** (voir la ligne `bloc-linguistique`).

> **Passe précédente — 2026-11-04 23 h 43 → 2026-11-05 02 h 12 :** **83 portes, 79 vertes,
> 4 rouges**, **2 h 29** (journaux durables `work/portes/passe-2404-23h45`), **machine au repos**
> (GPU libres, aucune réservation). Les **2 rouges structurelles connues** restent : `porte-indice`
> (1 207 s), `porte-melange` (148 s). Deux rouges nouvelles, **hors dépôt** : `porte-lecteur` (0 s)
> échouait sur une ancre du banc pilote (« < 2,5 ») que la réécriture de la roadmap du 04/11
> (« sous 2,5 ») avait rendue introuvable — **corrigée et rejouée verte** ; `porte-sessions` (0 s)
> signale les heartbeats périmés du hub et de `e181ce02` au moment de la passe — le hub l'a rafraîchi
> à 01 h 55, **`e181ce02` reste à rafraîchir par sa session**. Longues vertes : `greffe` **840 s**,
> `hom
… [1606 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"pensee-\\*\\|pensee-\" tools/*.py docs/methode/*.md 2>/dev/null | head -20; echo '--- corpus propre header'; sed -n '1,50p' tools/corpus_propre.py", "description": "Chercher le validateur des pensée et l'origine du corpus propre"}`

  ```
tools/pas_de_pensee_contracte.py:43:    ap.add_argument("--sortie", default="reports/pas-de-pensee-contracte.json")
tools/pas_de_pensee_mlp.py:29:    ap.add_argument("--sortie", default="reports/pas-de-pensee-mlp.json")
tools/pas_de_pensee_recurrent.py:45:    ap.add_argument("--sortie", default="reports/pas-de-pensee-recurrent.json")
tools/pas_latent.py:6:     rien** ✗✓ : ce n'est pas une question d'échelle (`rapport-pensee-silencieuse.md` § 2) ;
tools/pensee_multilingue.py:71:    ap.add_argument("--sortie", default="reports/pensee-multilingue.json")
tools/pensee_multilingue.py:72:    ap.add_argument("--etats", default="reports/pensee-multilingue-etats.npz")
tools/pensee_silencieuse.py:166:    travail = pathlib.Path(tempfile.mkdtemp(prefix="pensee-"))
tools/pont_abstrait.py:6:`rapport-pensee-silencieuse.md` § 2 ✓). C'est un **mode de fonctionnement différent** ✓ : il faut un
--- corpus propre header
#!/usr/bin/env python3
"""corpus_propre.py — un corpus sans répétition, et un split qui ne fuit pas.

POURQUOI. N2.d a mesuré que **32,8 %** des fenêtres du protocole de validation
apparaissent **verbatim** dans l'entraînement : le corpus empile des passages qui se
recopient (127 blocs 
… [1850 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"rope2048-20k\\|20 000\\|2,4953\\|2.4953\" reports/rapport-n2-r12-2048.md reports/rapport-n2-fenetre.md 2>/dev/null | head -20; echo '--- files'; grep -n \"Fichiers\" -A 15 reports/rapport-n2-r12-2048.md", "description": "Relier le checkpoint récent à sa fiche"}`

  ```
reports/rapport-n2-r12-2048.md:9:> à 128 octets, 2,4383 contre 2,5429 à 4 000). À **pas constants** (20 000), la même
reports/rapport-n2-r12-2048.md:21:compute** (la même recette à 20 000 pas).
reports/rapport-n2-r12-2048.md:27:| fenêtre 256 | 128 | 20 000 | 20,5 Mo | `base-wiki-45m` |
reports/rapport-n2-r12-2048.md:31:| **fenêtre 1 024, 20 k pas** | 1 024 | 20 000 | 164 Mo | `base-wiki-45m` (puis suite) |
reports/rapport-n2-r12-2048.md:43:| 256 (20 000 pas) | 3,3696 | 3,2892 | 3,2545 | 3,2459 | 3,2305 |
reports/rapport-n2-r12-2048.md:59:Même recette (RoPE, 1 024), mais **20 000 pas** — donc **8× plus d'octets** que le run à
reports/rapport-n2-r12-2048.md:64:| fenêtre 256, 20 000 pas | 20,5 Mo | 3,3696 | 3,2892 | 3,2545 | 3,2459 | 3,2305 |
reports/rapport-n2-r12-2048.md:65:| **fenêtre 1 024, 20 000 pas** | **164 Mo** | **2,9955** | **2,7201** | **2,6256** | **2,5757** | **2,5429** |
reports/rapport-n2-r12-2048.md:70:(20 000 pas, fenêtre 256, **20,5 Mo**) contre celui-ci (20 000 pas, fenêtre 1 024, **164 Mo**) :
reports/rapport-n2-r12-2048.md:139:  (20 000 / 5 000 / 2 500 / 1 250) : c'est précisément ce que le § 2 mesure, mais chaque point de
reports/rapport-n2-r12-2048.md:144:- **L
… [1743 caractères tronqués]
  ```

- **bash** `{"command": "ls tools/porte-*.sh | wc -l; echo '--- checkpoints'; find work -name '*.pt' | wc -l; du -sh work/n2ac work/n2h work/n2j work/n2k work/n2w work/n2d work/n2i 2>/dev/null; echo '--- total .pt'; find work -name '*.pt' -printf '%s\\n' | awk '{s+=$1} END {printf \"%.2f Go\\n\", s/2^30}'; echo … [116 caractères tronqués]`

  ```
84
--- checkpoints
123
7,7G	work/n2ac
1,5G	work/n2h
2,8G	work/n2j
1,9G	work/n2k
1,3G	work/n2w
633M	work/n2d
316M	work/n2i
--- total .pt
9.52 Go
--- json metadata
67
  ```

- **bash** `{"command": "cat reports/corpus-propre.json 2>/dev/null | head -40; echo '--- sha corpus'; sha256sum data/corpus_propre/val.txt data/corpus_propre/test.txt data/corpus_propre/train.txt 2>/dev/null", "description": "Lire le manifeste du corpus propre"}`

  ```
{
 "source": "data/corpus_fr.txt",
 "source_octets": 4633889,
 "source_sha256": "1e39f1a8aeac403d7b7ff5adc598fd8dd14233287707d5849a37c3e667f145d4",
 "methode": {
  "deduplication": "shingles de Rabin-Karp (base 257, mod 2^61−1), première occurrence gardée, runs gardés ≥ 64 octets, joints par \\n",
  "fenetre_shingle": 96,
  "chunk_octets": 8192,
  "split": "un chunk sur 20 en validation, le suivant sur 20 en test"
 },
 "propre_octets": 3605306,
 "deduplication": {
  "retires": 1029993,
  "runs": 1411,
  "plus_long_run": 540086,
  "retires_pct": 22.23
 },
 "train_octets": 3244858,
 "val_octets": 180224,
 "test_octets": 180224,
 "chunks": {
  "train": 397,
  "val": 22,
  "test": 22
 },
 "sha256": {
  "train": "8a1856022ed5eb58e773652fb2fcba827cb9d30958a39c3f2cf05c69efb73a71",
  "val": "d9ffb0bb49d5fe088062d411e0b1b7b1d373c2d602e2c6f4556c93a101819f57",
  "test": "566d467e3c7ecdbd280fbc6766627adc6d8d37560c04a69d6b8c554be6983531"
 },
 "contamination": {
  "validation": {
   "fenetres": 2814,
   "contaminees": 0,
   "taux": 0.0
  },
  "test": {
   "fenetres": 2814,
   "contaminees": 0,
   "taux": 0.0
--- sha corpus
d9ffb0bb49d5fe088062d411e0b1b7b1d373c2d602e2c6f4556c93a101819f57  data/co
… [208 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '145,195p' reports/rapport-n2-r12-2048.md", "description": "Lire la section 2048 20k de la fiche R12"}`

  ```
l'effet isolé de la fenêtre (les octets ont été multipliés par 8).
- **La validation interne et les validations d'évaluation** ne sont pas le même texte ; les
  écarts inférieurs à 0,05 ne sont pas interprétables.
**Le coût d'inférence ne quadruple pas.** Mesuré à batch 8 (`work/n2ac/cout_fenetre.py`),
le débit passe de **22 306** octets/s (fenêtre 256) à **22 730** (512), **21 156** (1 024) et
**19 405** (2 048) : l'attention quadruple à chaque doublement, mais le FFN **domine** à 34,3 M,
donc le débit ne perd que **13 %** de 256 à 2 048. La fenêtre est presque gratuite à cette
taille — elle ne le resterait pas à plus grande échelle.

## 5. Le complément 2 048, mesuré en deux moitiés (10 000 puis 20 000 pas)

Le reboot du 03/11 et la contention du 04/11 avaient interrompu ce complément deux fois ; il a
été relancé **en deux segments de 10 000 pas** (un point de contrôle par segment) et mesuré :

| run (wiki_fr, RoPE, init `base-wiki-45m`) | octets vus | 128 | 512 | 1 000 | 2 000 | 4 000 |
|---|---:|---:|---:|---:|---:|---:|
| fenêtre 1 024, 2 500 pas | 20,5 Mo | 3,3878 | 3,1098 | 2,9950 | 2,9449 | 2,9108 |
| **fenêtre 2 048, 10 000 pas** | **164 Mo** | 3,0466 | 2,7581 | 2,6501 | 2
… [1760 caractères tronqués]
  ```

- **bash** `{"command": "head -30 work/n2ac/rope2048-20k.log; echo '...'; tail -50 work/n2ac/rope2048-20k.log; echo '--- stat'; stat -c '%y %s %n' work/n2ac/rope2048-20k.pt work/n2ac/rope2048-20k.pt.json work/n2ac/rope2048-20k.log work/n2ac/rope2048-10k.pt", "description": "Lire le log du run 2048 20k et ses da … [5 caractères tronqués]`

  ```
init : work/n2ac/rope2048-10k.pt
/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/n2ac/entrainer_rope.py:89: UserWarning: Converting a tensor with requires_grad=True to a scalar may lead to unexpected behavior.
Consider using tensor.detach() first. (Triggered internally at /pytorch/torch/csrc/autograd/generated/python_variable_methods.cpp:836.)
  pertes.append(float(perte))
pas      1 · perte 1.0549 · PPL val 2.515 · 2 s
pas     50 · perte 1.0010 · PPL val 2.500 · 52 s
pas    100 · perte 1.0009 · PPL val 2.507 · 103 s
pas    150 · perte 0.9622 · PPL val 2.507 · 154 s
pas    200 · perte 1.0191 · PPL val 2.501 · 205 s
pas    250 · perte 0.9889 · PPL val 2.494 · 256 s
pas    300 · perte 0.9273 · PPL val 2.502 · 307 s
pas    350 · perte 0.9944 · PPL val 2.497 · 358 s
pas    400 · perte 0.9712 · PPL val 2.498 · 409 s
pas    450 · perte 1.0159 · PPL val 2.492 · 460 s
pas    500 · perte 0.9825 · PPL val 2.496 · 511 s
pas    550 · perte 1.0514 · PPL val 2.493 · 562 s
pas    600 · perte 0.9751 · PPL val 2.492 · 614 s
pas    650 · perte 0.9593 · PPL val 2.502 · 665 s
pas    700 · perte 0.9692 · PPL val 2.494 · 716 s
pas    750 · perte 1.1020 · PPL val 2.500 · 767 s
pas    800 · perte 1.0
… [2796 caractères tronqués]
  ```

- **bash** `{"command": "ls -la data/wiki_fr/propre/val.txt data/wiki_fr/propre/val.canal 2>&1; date '+%H:%M:%S'; PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. CUDA_VISIBLE_DEVICES=0 ~/gpu-env/bin/python work/n2ac/eval_longueurs.py work/n2ac/rope2048-20k.pt --rope --longueurs 128,512,1000,2000,4000 --val data/wiki_fr/ … [137 caractères tronqués]`

  ```
started background job bash-4123
  ```

- **bash** `{"command": "set -u; test -d /tmp/propre_test && { echo '/tmp/propre_test existe déjà — abandon'; exit 3; }; mkdir -p /tmp/propre_test && cp data/corpus_propre/test.txt /tmp/propre_test/val.txt && cp data/corpus_propre/test.canal /tmp/propre_test/val.canal && echo 'temp prêt'; date '+%H:%M:%S'; PYTH … [422 caractères tronqués]`

  ```
started background job bash-4124
  ```

- **job_output** `{"job_id": "bash-4123"}`

  ```
-rw-r--r--. 1 stephane stephane 10330112  1 nov 18:35 data/wiki_fr/propre/val.canal
-rw-r--r--. 1 stephane stephane 10330112  1 nov 11:54 data/wiki_fr/propre/val.txt
21:37:42
  L128 : 2.9121
  L512 : 2.636
  L1000 : 2.5375
  L2000 : 2.4779
  L4000 : 2.4383
{"fichier": "rope2048-20k.pt", "val": "data/wiki_fr/propre", "positions": "rope", "L128": 2.9121, "L512": 2.636, "L1000": 2.5375, "L2000": 2.4779, "L4000": 2.4383}
EXIT=0
21:38:13
[status: completed, exit code: 0]
  ```

- **job_output** `{"job_id": "bash-4124"}`

  ```
temp prêt
21:37:43
  L128 : 3.0649
  L512 : 2.8875
  L1024 : 2.8566
{"fichier": "propre512-8k.pt", "val": "/tmp/propre_test", "positions": "rope", "L128": 3.0649, "L512": 2.8875, "L1024": 2.8566}
EXIT=0
21:37:51
temp supprimé
[status: completed, exit code: 0]
  ```

### 👤 Utilisateur

background job bash-4124 (bash: set -u; test -d /tmp/propre_test && { echo '/tmp/propre_test existe déjà — abandon'; exit 3; }; mkdir -p /tmp/propre_test && cp data/corpus_propre/test.txt /tmp/propre_test/val.txt && cp data/corpus_propre/test.canal /tmp/propre_test/val.canal && echo 'temp prêt'; date '+%H:%M:%S'; PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. CUDA_VISIBLE_DEVICES=1 ~/gpu-env/bin/python work/n2ac/eval_longueurs.py work/n2ac/propre512-8k.pt --rope --longueurs 128,512,1024 --val /tmp/propre_test; code=$?; echo "EXIT=$code"; date '+%H:%M:%S'; test -d /tmp/propre_test && rm -rf /tmp/propre_test && echo 'temp supprimé'; exit $code) finished [status: completed, exit code: 0]. Read its output with job_output.

### 👤 Utilisateur

background job bash-4123 (bash: ls -la data/wiki_fr/propre/val.txt data/wiki_fr/propre/val.canal 2>&1; date '+%H:%M:%S'; PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. CUDA_VISIBLE_DEVICES=0 ~/gpu-env/bin/python work/n2ac/eval_longueurs.py work/n2ac/rope2048-20k.pt --rope --longueurs 128,512,1000,2000,4000 --val data/wiki_fr/propre; echo "EXIT=$?"; date '+%H:%M:%S') finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "date '+%H:%M:%S'; PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. CUDA_VISIBLE_DEVICES=0 ~/gpu-env/bin/python - <<'PY'\nimport json, pathlib, sys, torch\nsys.path.insert(0, '.')\nsys.path.insert(0, 'work/n2j')\nfrom work.n2ac.rope_model import charge_rope\nfrom tools.eval_n2_propre import charge … [790 caractères tronqués]`

  ```
21:41:02
{"checkpoint": "propre512-8k.pt", "val_L1024_a": 2.7856, "val_L1024_b": 2.7856, "identique": true, "permute_L1024": 1692.3919}
EXIT=0
21:41:15
  ```

- **bash** `{"command": "echo '--- corpus suivi ?'; git ls-files data/corpus_propre/ | head; echo '--- HEAD'; git rev-parse --short HEAD; echo '--- fiches N2'; ls reports/rapport-n2-*.md | wc -l; echo '--- rapports total'; ls reports/rapport-*.md | wc -l; echo '--- json total'; ls reports/*.json | wc -l; echo ' … [105 caractères tronqués]`

  ```
--- corpus suivi ?
--- HEAD
bfd98892
--- fiches N2
40
--- rapports total
683
--- json total
789
--- date du jour
2026-11-06
  ```

- **bash** `{"command": "git log --oneline -3; echo '--- statut'; git status --porcelain | head -15; echo '--- corpus ignoré ?'; git check-ignore -v data/corpus_propre/val.txt data/corpus_propre/train.txt 2>&1; echo '--- diff n2 récent'; git log --oneline -3 --name-only | head -40", "description": "Vérifier le  … [31 caractères tronqués]`

  ```
bfd98892 DOC PRODUIT — RESYNCHRONISÉE : POS 85,00 %, F1 0,6482, ATTACHEMENT 235/236, GELÉ 85,32 / 0,6511 ; SORTIE D'EVALUER REJOUÉE
9e4cde3b README — LA SECTION « ESSAYEZ » : LA CLI drave, LE FORMAT VERSIONNÉ, LA PORTE PRODUIT, LES CHIFFRES DU 06/11
ea1a68a2 ÉTAT — T0 DANS LE BUDGET (NUIT DES P0)
--- statut
M  docs/pilotage/en-cours.md
MM journal/2026-11-05/README.md
D  journal/2026-11-05/attention.md
MM journal/2026-11-05/distribue.md
MM journal/2026-11-05/docs.md
MM journal/2026-11-05/memoire.md
MM journal/2026-11-05/mesures.md
MM journal/2026-11-05/modele.md
MM journal/2026-11-05/moteur.md
MM journal/2026-11-05/portes.md
MM journal/2026-11-06/README.md
D  journal/2026-11-06/distribue.md
D  journal/2026-11-06/docs.md
D  journal/2026-11-06/memoire.md
D  journal/2026-11-06/mesures.md
--- corpus ignoré ?
.gitignore:5:data/	data/corpus_propre/val.txt
.gitignore:5:data/	data/corpus_propre/train.txt
--- diff n2 récent
bfd98892 DOC PRODUIT — RESYNCHRONISÉE : POS 85,00 %, F1 0,6482, ATTACHEMENT 235/236, GELÉ 85,32 / 0,6511 ; SORTIE D'EVALUER REJOUÉE
docs/produit/README.md
journal/2026-11-06/README.md
journal/2026-11-06/distribue.md
journal/2026-11-06/docs.md
journal/2026-11-06/memoire.md
… [1606 caractères tronqués]
  ```

- **bash** `{"command": "grep -ln \"PPL\\|perplex\" tools/porte-*.sh | head; echo '--- dépendances work/'; grep -l \"work/\" tools/porte-*.sh | head -20; echo '--- absents'; grep -n \"absent\\|introuvable\\|! -f\\|! -e\" tools/porte-*.sh | head -30", "description": "Voir comment les portes gèrent les artefacts  … [8 caractères tronqués]`

  ```
tools/porte-adaptateur-sortie.sh
tools/porte-budget.sh
tools/porte-bus.sh
tools/porte-bus-socket.sh
tools/porte-c4-retard.sh
tools/porte-consolidation.sh
tools/porte-coupe.sh
tools/porte-cycle-c2.sh
tools/porte-delais.sh
tools/porte-diff-couche.sh
--- dépendances work/
tools/porte-ocr-scans.sh
--- absents
tools/porte-adaptateur-sortie.sh:28:[ -s "$M" ] || { echo "  ❌ modèle absent : $M"; exit 2; }
tools/porte-adaptateur-sortie.sh:29:[ -x "$D" ] || { echo "  ❌ binaire du moteur absent : $D"; exit 2; }
tools/porte-adaptateur-sortie.sh:120:refus "fichier absent" "--couches 0:$COUCHES --tete-partielle --adaptateur-sortie $T/inexistant.f32"
tools/porte-balayage.sh:7:# contrôles négatifs (terme absent, terme d'un autre document).
tools/porte-budget.sh:24:[ -s "$M" ] && [ -s "$IDS" ] || { echo "  modèle ou identifiants absents"; exit 2; }
tools/porte-bus.sh:25:[ -s "$M" ] && [ -s "$IDS" ] || { echo "  modèle ou identifiants absents"; exit 2; }
tools/porte-bus-socket.sh:50:[ -s "$M" ] && [ -s "$IDS" ] || { echo "  modèle ou identifiants absents"; exit 2; }
tools/porte-c4-retard.sh:27:[ -s "$M" ] && [ -s "$IDS" ] || { echo "  modèle ou identifiants absents"; exit 2; }
tools/porte-cerveau.sh
… [2298 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' tools/porte-melange.sh", "description": "Lire porte-melange comme modèle de porte de mesure"}`

  ```
#!/bin/bash
# porte-melange.sh — C2 : DEUX ENTRÉES, UNE RÈGLE DE MÉLANGE. Que fait une somme ?
#
# LA QUESTION DE C2, SANS TOUCHER AU MOTEUR. Deux flux qui se rencontrent : que devient
# leur contenu ? La greffe d'état a fourni l'instrument (`--fusion-etat`), et une somme
# de deux états prélevés s'écrit sans une ligne de code de plus. Il y a deux réponses
# possibles, très différentes :
#   · la somme ARBITRE entre les deux contenus (l'un ou l'autre) ⇒ il y a un POINT DE
#     BASCULE à mesurer, et la fusion par somme est utilisable ;
#   · la somme produit un TROISIÈME contenu (ni l'un ni l'autre) ⇒ elle DÉTRUIT
#     l'information, et aucune architecture ne peut fusionner ainsi.
#
# LA CALIBRATION, ET POURQUOI ELLE EST LÀ. Prélever « la dernière position » ne va pas
# de soi : `--tokenize` et `--prompt` ne comptent PAS les mêmes jetons pour un texte qui
# finit par un saut de ligne (17 contre 16, mesuré), et la première version de cette
# porte a donc prélevé l'état qui prédit le DERNIER JETON DU TEXTE au lieu de celui qui
# prédit le code — les deux états purs rendaient alors « 1234 », et la porte a échoué
# pour cette raison, pas pour une raison de fond. La porte CALIBRE donc 
… [5529 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/n2-propre.json'))\nprint(type(d).__name__, list(d)[:12] if isinstance(d,dict) else len(d))\nprint(json.dumps(d, ensure_ascii=False)[:1800])\nPY", "description": "Lire les résultats N2.h par graine"}`

  ```
dict ['A', 'C', 'D', 'R', 'longueurs_A', 'longueurs_R', 'decomposition_A', 'base_propre']
{"A": {"val": 3.0904, "test": 3.1959666666666666, "litterature_propre": 16.703433333333333, "anglais": 57.577333333333335, "wikitext2": 56.8821}, "C": {"val": 3.080433333333333, "test": 3.1878666666666664, "litterature_propre": 16.817233333333334}, "D": {"val": 3.2625333333333333, "test": 3.3221333333333334, "litterature_propre": 3.8546, "anglais": 25.6755, "wikitext2": 26.058933333333332}, "R": {"val": 3.2380999999999998, "test": 3.3426666666666667, "litterature_propre": 16.816466666666667}, "longueurs_A": {"129": 3.1318, "192": 8.5551, "256": 14.105333333333332, "384": 23.902633333333334, "512": 32.4114}, "longueurs_R": {"129": 3.2429333333333332, "192": 3.2338666666666667, "256": 3.2482666666666664, "384": 5.057666666666667, "512": 5.9328}, "decomposition_A": {"apres_2_blocs": 3.8244666666666665, "apres_4_blocs": 3.2237666666666667, "apres_6_blocs": 3.0462333333333333, "complete": 3.1161666666666665, "sans_pensee": 23632397.258}, "base_propre": {"val": 3.2402, "test": 3.288, "litterature_propre": 12.2861, "anglais": 32.9009, "wikitext2": 33.2883}}
  ```

- **bash** `{"command": "echo '--- models suivi ?'; git ls-files models/ | head -3; echo '--- data suivi ?'; git ls-files data/ | head -3; echo '--- taille porte propre artifact'; ls -la work/n2ac/propre512-8k.pt work/n2ac/propre512-8k.pt.json work/n2ac/propre512-8k.drvm 2>&1; echo '--- sha pt (peut prendre 2 s … [119 caractères tronqués]`

  ```
--- models suivi ?
--- data suivi ?
--- taille porte propre artifact
-rw-r--r--. 1 stephane stephane 137224476  3 nov 02:01 work/n2ac/propre512-8k.drvm
-rw-r--r--. 1 stephane stephane 137248474  3 nov 02:01 work/n2ac/propre512-8k.pt
-rw-r--r--. 1 stephane stephane       524  3 nov 02:01 work/n2ac/propre512-8k.pt.json
--- sha pt (peut prendre 2 s)
37c5673b3d51f6f871c4391b97015b401f73c842d04d4a05f78a70c2b264eefc  work/n2ac/propre512-8k.pt
  ```

