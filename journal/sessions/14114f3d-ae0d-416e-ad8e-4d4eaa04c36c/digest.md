# Session DSH — relecture

- identifiant : `14114f3d-ae0d-416e-ad8e-4d4eaa04c36c`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-06 09:31:04
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **auditer la fiabilité « produit » du bloc linguistique** — qu'est-ce qu'un utilisateur peut utiliser en autonomie, et qu'est-ce qui est encore fragile ?

Contexte : `tools/bloc_linguistique.py` (`Heuristique`, `analyser`), `tools/tests/linguistique/evaluer_gold.py` (`charger`, `evaluer_bloc`), `tools/tests/linguistique/gold_split.py` (dev/test), les fiches `reports/rapport-pensee-v12.md`, `rapport-audit-v10.md`, `rapport-dev-test-v10.md`, `rapport-coherence-fiches-v8.md`, `rapport-cache-chunker-applique.md`. État : exact 222/222 sur 222 labels, couverture 0,9289, F1 0,5849, POS 0,7581, 17 spans inatteignables, rouge `cascade_pos`.

À faire :
1. Mesure la **robustesse hors gold** : prends 50 phrases libres (écris-les toi-même, variées : longues, ponctuation, majuscules, questions, impératives, anglais), analyse-les, et note les plantages, les sorties vides, les incohérences (span hors texte, cible absente, chevauchements) — c'est le test « utilisateur ».
2. Mesure la **performance** : temps par phrase à 10/50/200 mots, mémoire, déterminisme (2 analyses identiques).
3. Mesure la **stabilité du contrat** : la structure d'`Annotation` (niveaux, types), les champs toujours présents, ceux qui peuvent être vides ; ce qu'un client peut parser sans casser.
4. Établis une **liste de correctifs produit** (bloquants / importants / confort), chiffrée, avec les lignes concernées.
5. Écris **uniquement** deux fichiers neufs : `reports/rapport-produit-bloc-l.md` et `reports/pensee-produit-bloc-l.json`.
6. Ne commite rien ; ne modifie aucun existant ; pas de `docs/pilotage/`, `AGENTS.md`, `journal/`, `tools/structures/`, `data/`, natifs.

Rends un résumé : plantages (nombre, causes), temps par phrase, contrat, et les 5 correctifs prioritaires.
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

⏵ Exploration du dépôt et lecture des fichiers cibles

- **bash** `{"command": "pwd && git branch --show-current && git status --short | head -20 && ls", "description": "Vérifier branche et état du dépôt"}`

  ```
/home/stephane/Data13TB/stephane/GitHub/Qtrinet
s/v7
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
D  journal/2026-11-06/mesures.md
D  journal/2026-11-06/modele.md
D  journal/2026-11-06/portes.md
MM journal/README.md
MM journal/THEMES.md
MM journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/digest.md
MM journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/rapport.md
D  journal/sessions/1b0cf09a-a77a-443d-82e2-68a5d6cacdf0/digest.md
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

- **bash** `{"command": "ls -la tools/ tools/tests/linguistique/ reports/ 2>/dev/null | head -80", "description": "Lister outils, tests linguistiques, rapports"}`

  ```
reports/:
total 19352
drwxr-xr-x. 1 stephane stephane   70748  6 nov 01:26 .
drwxr-xr-x. 1 stephane stephane     660  1 nov 10:50 ..
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
-rw-r--r--. 1 steph
… [4559 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture du module `bloc_linguistique.py` et des scripts d'évaluation

- **bash** `{"command": "wc -l tools/bloc_linguistique.py tools/tests/linguistique/evaluer_gold.py tools/tests/linguistique/gold_split.py 2>/dev/null; ls tools/tests/linguistique/", "description": "Compter lignes des fichiers cibles"}`

  ```
2192 tools/bloc_linguistique.py
   305 tools/tests/linguistique/evaluer_gold.py
    50 tools/tests/linguistique/gold_split.py
  2547 total
anaphore.py
classement_cible.py
evaluer_gold.py
gold_gele.json
gold.json
gold.py
gold_reel.json
gold_reel.py
gold_split.py
gold_synthetique.json
gold_synthetique.py
juge.py
miroir.py
__pycache__
qualifier_cascade.py
qualifier_frontiere_71.py
qualifier_lien_appris.py
qualifier_neuronal.py
qualifier_pragmatique.py
qualifier_quatre_modes.py
qualifier_syntagmes.py
replis_cible.py
test_bloc_linguistique.py
  ```

- **bash** `{"command": "ls reports/ | grep -E \"pensee|audit-v10|dev-test|coherence-fiches|cache-chunker\" ; echo \"---\"; ls -la reports/rapport-pensee-v12.md reports/rapport-audit-v10.md reports/rapport-dev-test-v10.md reports/rapport-coherence-fiches-v8.md reports/rapport-cache-chunker-applique.md 2>&1", "d … [45 caractères tronqués]`

  ```
native-pensee.json
pas-de-pensee-14b.json
pas-de-pensee-7b.json
pas-de-pensee-contracte-3b.json
pas-de-pensee-contracte-7b.json
pas-de-pensee-corrige-14b.json
pas-de-pensee-corrige-3b.json
pas-de-pensee-corrige-7b.json
pas-de-pensee-corrige-large.json
pas-de-pensee.json
pas-de-pensee-mlp-18.json
pas-de-pensee-mlp-6.json
pas-de-pensee-non-lineaire-3b.json
pas-de-pensee-non-lineaire-large.json
pas-de-pensee-recurrent.json
pensee-absents.json
pensee-ac3-alphabeta.json
pensee-adaptive.json
pensee-aleatoire.json
pensee-alternance.json
pensee-anaphore-103.json
pensee-anaphore-68.json
pensee-anaphore-bilan.json
pensee-anaphore-chaines.json
pensee-anaphore-corrige.json
pensee-anaphore-cv-graines.json
pensee-anaphore-cv.json
pensee-anaphore-hybride.json
pensee-anaphore.json
pensee-anaphore-kappa.json
pensee-anaphore-limite.json
pensee-anaphore-meta.json
pensee-anaphore-objets.json
pensee-anaphore-pieges.json
pensee-anaphore-pondere.json
pensee-anaphore-roles.json
pensee-anaphore-semantique.json
pensee-annotation-independante.json
pensee-asym.json
pensee-attachement-cible.json
pensee-attachement.json
pensee-attachement-parfait.json
pensee-attachement-v2.json
pensee-attachement-v3.json
pensee
… [12438 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 220}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """bloc_linguistique.py — le bloc d'étiquetage linguistique, du graphème à la pragmatique.
3: 
4: Un seul contrat (`BlocLinguistique.analyser`) et **plusieurs implémentations** :
5: 
6:   - `Heuristique` : CPU, déterministe, ultra-rapide ; elle étiquette la surface et produit des
7:     **candidats** pour l'ambigu ; elle déclare sa couverture et sa confiance ;
8:   - `MockNeuronal` : une implémentation neuronale **de contrat**, déterministe, pour tester la
9:     substitution et le parallèle sans GPU ;
10:   - `NeuronalLLM` : l'adaptateur réel, qui interroge un modèle local (`llama-cli`) et rend le
11:     même type d'annotation ;
12:   - `NeuronalLLMPOS` : le **tagger** neuronal réel — un modèle local, une liste de tokens, des
13:     POS alignés par grammaire GBNF ; c'est l'implémentation qualifiée sur le gold ;
14:   - `Parallele` et `Cascade` : les deux modes de composition. Le parallèle fusionne les
15:     étiquettes par confiance ; la cascade n'envoie au neuronal que le **résidu** des niveaux
16:     que l'heuristique ne couvre pas.
… [8798 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"^class \\|^def \\|^    def \" tools/bloc_linguistique.py | head -100", "description": "Lister classes et fonctions du module"}`

  ```
59:class Span:
63:    def json(self) -> dict:
68:class Etiquette:
81:    def json(self) -> dict:
92:class Annotation:
105:    def par_niveau(self) -> dict[str, list[Etiquette]]:
111:    def couverture(self) -> dict[str, float]:
116:    def json(self, avec_duree: bool = False) -> dict:
130:class BlocLinguistique(Protocol):
133:    def analyser(self, texte: str, langue: str | None = None,
137:class RefusNeuronal(RuntimeError):
144:def _normaliser(texte: str) -> str:
148:def _trigrammes(texte: str) -> list[str]:
153:def _profil(texte: str, top: int = 200) -> dict[str, int]:
158:def charger_profils_udhr(chemin: pathlib.Path, train=(0, 14), test=(15, 30),
192:def _score_profil(tri: collections.Counter, profil: dict[str, int]) -> float:
199:def detecter_langue(texte: str, profils: dict[str, dict] | None = None,
230:def _script_char(ch: str) -> str:
256:def detecter_script(texte: str) -> str:
461:def _est_adverbe_seul(g: dict) -> bool:
473:def _sans_enclitique(mot: str) -> str:
481:def _est_verbe(mot: str) -> bool:
500:def _role_gp(prep: str) -> str:
525:class Heuristique:
530:    def __init__(self, profils: dict[str, dict] | None = None, segmenter_s: bool = True,
540:    def _langue(self
… [4335 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "offset": 500, "limit": 180}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "offset": 995, "limit": 270}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
500: def _role_gp(prep: str) -> str:
501:     p = prep.casefold()
502:     if p in {"dans", "sur", "sous", "chez", "vers", "entre", "devant", "derrière", "près", "loin",
503:              "in", "on", "at", "under", "between"}:
504:         return "lieu"
505:     if p in {"pendant", "depuis", "durant", "avant", "après", "during", "since", "before", "after"}:
506:         return "temps"
507:     if p in {"pour", "afin", "for", "to"}:
508:         return "but"
509:     if p in {"par", "by"}:
510:         # `par` + GN est l'**agent** d'un passif (`Le chat est mangé par le chien`) ;
511:         # `avec`/`sans` restent le moyen.
512:         return "agent"
513:     if p in {"avec", "sans", "with", "without"}:
514:         return "moyen"
515:     if p in {"à", "a", "au", "aux", "to"}:
516:         return "destinataire"
517:     if p in {"de", "du", "des", "of", "from"}:
518:         return "theme"
519:     return "complément"
520: 
521: 
522: # --------------------------------------------------------------------------- heuristique
523: 
524: 
525: class Heuristique:
526:   
… [7985 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
995:                                  "debut": d, "fin": mots[j - 1][1],
996:                                  "texte": texte[d:mots[j - 1][1]], "candidats": []})
997:                 i = j
998:                 continue
999:             i += 1
1000:         return segments
1001: 
1002:     # -- analyse ------------------------------------------------------------
1003:     def analyser(self, texte: str, langue: str | None = None,
1004:                  contexte: str | None = None) -> Annotation:
1005:         t0 = time.perf_counter()
1006:         texte = texte or ""
1007:         trace: list[dict] = []
1008:         if not texte.strip() or not any(ch.isalpha() or ch.isdigit() for ch in texte):
1009:             return Annotation(texte=texte, refus="vide", source=self.nom,
1010:                               trace=[{"etape": "refus", "raison": "vide"}],
1011:                               cout={"octets": len(texte.encode()), "duree_s": round(time.perf_counter() - t0, 6)})
1012: 
1013:         lg, conf_lg, script = self._langue(texte, langue)
1014:         trace.append(
… [17144 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture du protocole d'évaluation gold et des fiches

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/evaluer_gold.py"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_split.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/evaluer_gold.py</path>
<type>file</type>
<content>
1: """evaluer_gold.py — mesure le bloc linguistique sur le gold réel (20) + synthétique (160).
2: 
3: Trois niveaux : POS (token, exact), syntagmes (exact + **par tête**), pragmatique. Quatre
4: lectures : heuristique, mock neuronal, parallèle, cascade. Le vrai modèle est optionnel
5: (`--reel`) : s'il ne répond pas, il est refusé, pas simulé.
6: """
7: from __future__ import annotations
8: 
9: import argparse
10: import json
11: import pathlib
12: import sys
13: from collections import Counter, defaultdict
14: 
15: RACINE = pathlib.Path(__file__).resolve().parents[3]
16: sys.path.insert(0, str(RACINE / "tools"))
17: import bloc_linguistique as bl  # noqa: E402
18: 
19: GOLD = pathlib.Path(__file__).with_name("gold.json")
20: REEL = pathlib.Path(__file__).with_name("gold_reel.json")
21: SYNTH = pathlib.Path(__file__).with_name("gold_synthetique.json")
22: 
23: 
24: def charger() -> list[dict]:
25:     hand = json.loads(GOLD.read_text(encoding="utf-8"))["phrases"]
26:     reel = json.loads(REEL.read_text(encoding="utf-8"))["phrases"]
27:     synth = json.
… [15928 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_split.py</path>
<type>file</type>
<content>
1: """gold_split.py — le gold 612 coupé en **dev** et **test**, de façon déterministe.
2: 
3: Le problème. Toutes les mesures de la session sont **in-sample** : les règles de segmentation et
4: d'attachement ont été dessinées en regardant les échecs du même gold qui les mesure. Pour juger
5: une règle, il faut un gold **tenu à l'écart** : on règle sur `dev`, on évalue sur `test`.
6: 
7: Protocole (fixé ici). Le split est un **hash stable de l'identifiant** (`crc32(id) % 3 == 0` →
8: test, sinon dev), donc reproductible, insensible à l'ordre et indépendant du contenu. Il est
9: **stratifié par source** (`hand`, `reel`, `synthetique`) et par langue : on vérifie l'équilibre
10: dans la fiche. Aucune phrase n'est dupliquée entre les deux ; l'union redonne les 612.
11: 
12: Usage :
13:     from tools.tests.linguistique.gold_split import dev, test, compter
14:     ph = charger(); d = dev(ph); t = test(ph)
15: """
16: from __future__ import annotations
17: 
18: import zlib
19: 
20: PART_TEST = 3  # une phrase sur trois va au test
21: 
22: 
23: def _est_test(phras
… [1070 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-v12.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-v12.md</path>
<type>file</type>
<content>
1: # B13 — 222/222 (1,0000) : le dernier marqueur ambigu, et 17 spans inatteignables
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-06 ·
4: > **État courant** · **Verdict** : ✅ — **la cible de A17 est atteinte**.
5: > **183/183 portes** : le dernier écart était un **marqueur ambigu** — « when » après un GN est
6: > une **relative** (« The day when we left »), ailleurs une **subordonnée** (« When it rains »).
7: > Résultat : **222 labels** sur 239, **exact 222/222 = 1,0000** (fr **136/136**, en **86/86**),
8: > **couverture 0,9289**, **F1 0,5893** (union ; S 0,5014, chunker 0,6203), tête **0,7392** ;
9: > **17 spans** restants (8 REL, 5 SUB, 4 GP) — **tous inatteignables** sans corriger le gold ou
10: > le lexique (12 formes synthétiques, 4 GP du gold sans préposition, une tokenisation `qu'il`).
11: > **dev 153/153, test 69/69.**
12: >
13: > **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`AMBIGUES_REL`,
14: > branche REL/SUB), [`autotest.py`](../tools/pensee/autotest.py) (16 assertions) ;
15: > JSO
… [2916 caractères tronqués]
  ```

- **bash** `{"command": "head -80 reports/rapport-audit-v10.md; echo \"==========\"; head -60 reports/rapport-dev-test-v10.md", "description": "Lire débuts des fiches audit et dev-test"}`

  ```
# Audit v10 — les chiffres rejouent, l'attribution des corrections ne rejoue pas

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Branche** : `s/v7` ·
> **Commit audité** : `710ec7f9` (parent `160d08ca`) · **Date** : 2026-11-05 ·
> **Verdict** : chiffres ✅ (deux écarts), règles ❌, portes ✅ (183/183, 11 docstrings périmées).
> **Aucun fichier existant modifié ; aucun commit.** Sorties : ce rapport et
> [`pensee-audit-v10.json`](pensee-audit-v10.json).

**En une phrase.** Les valeurs de la fiche [`rapport-pensee-v10.md`](rapport-pensee-v10.md)
rejouent presque toutes : **220/220**, couverture **0,9205**, **F1 0,5880** (gelé 602),
**tête 0,7388**, **fr 134/134**, **en 86/86**, **19 spans** (9 REL, 6 SUB, 4 GP),
**top-k 219**, **183/183 portes**. Mais la fiche attribue le gain à **deux** corrections :
la seconde, le **`-ée`**, est **antérieure à la v10** (commit `a408a909`, déjà dans v8 et v9)
et **inerte sur ce gold** (0 différence d'annotation sur 612 phrases) ; `r255` reste absent
car `acheter` n'est pas dans le lexique. Le **seul** gain v10 est la **garde DET du GP**
(`r153`, test), **+1 exact**. Les **19 spans** ne sont pas « 17 inatteignables + `r255` +
`r264` » 
… [8668 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 280, "offset": 220}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 220, "offset": 1800}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
220:         scores[indice] += 0.02
221:     if not scores or max(scores.values()) <= 0:
222:         return "und", 0.0, scores
223:     langue = max(scores, key=scores.get)
224:     return langue, round(min(1.0, scores[langue] * 2), 4), scores
225: 
226: 
227: # --------------------------------------------------------------------------- script
228: 
229: 
230: def _script_char(ch: str) -> str:
231:     if not ch.isalpha():
232:         return ""
233:     try:
234:         nom = unicodedata.name(ch)
235:     except ValueError:
236:         return ""
237:     prefixes = (
238:         ("LATIN", "Latn"), ("CYRILLIC", "Cyrl"), ("GREEK", "Grek"), ("ARABIC", "Arab"),
239:         ("HEBREW", "Hebr"), ("DEVANAGARI", "Deva"), ("THAI", "Thai"), ("HIRAGANA", "Jpan"),
240:         ("KATAKANA", "Jpan"), ("HANGUL", "Hang"), ("CJK", "Hani"), ("IDEOGRAPH", "Hani"),
241:         ("BENGALI", "Beng"), ("TAMIL", "Taml"), ("TELUGU", "Telu"), ("KANNADA", "Knda"),
242:         ("MALAYALAM", "Mlym"), ("GUJARATI", "Gujr"), ("GURMUKHI", "Guru"), ("SINHALA", "Sinh"),
243:         ("MYANMAR", "
… [18358 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
1800:         except Exception as e:
1801:             annotation = Annotation(texte=texte, langue=lg, script=script, source=self.nom,
1802:                                     refus=f"neuronal-pragmatique: {type(e).__name__}: {str(e)[:160]}",
1803:                                     trace=[{"etape": "neuronal-pragmatique", "erreur": str(e)[:160]}],
1804:                                     cout={"octets": len(texte.encode()),
1805:                                           "duree_s": round(time.perf_counter() - t0, 6)})
1806:         if self.cache:
1807:             self._cache[cle] = annotation
1808:         return annotation
1809: 
1810: 
1811: # --------------------------------------------------------------------------- compositions
1812: 
1813: 
1814: def _supprimer_chevauchements(etiquettes: list[Etiquette],
1815:                               priorite_syntagme: str = "heuristique") -> list[Etiquette]:
1816:     """Les alternatives se suppriment **par type** quand les types sont complémentaires.
1817: 
1818:     `pos` et `syntagme` sont des alternatives de **sp
… [11543 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification des mesures de référence sur le gold actuel

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 --version && PYTHONPATH=. timeout 600 python3 tools/tests/linguistique/evaluer_gold.py 2>&1 | tail -30", "description": "Rejouer l'évaluation gold de référence", "timeoutMs": 600000}`

  ```
Python 3.13.16
     "taux": 1.0
    },
    "nom": {
     "cibles": 70,
     "justes": 70,
     "taux": 1.0
    },
    "couverture": 0.8703,
    "par_langue": {
     "fr": {
      "cibles": 151,
      "labels": 122,
      "exact": 122,
      "topk": 121,
      "exact_taux_span": 1.0
     },
     "en": {
      "cibles": 88,
      "labels": 86,
      "exact": 86,
      "topk": 86,
      "exact_taux_span": 1.0
     }
    }
   },
   "attachement_tete": {
    "cibles": 208,
    "labels": 208,
    "top1"
heuristique all: {"pos": {"exactitude": 0.7581, "exactitude_ferme": 0.9004, "exactitude_ouvert": 0.6234, "tokens": 3179, "confusions": {"ADJ": {"ADJ": 50, "NOUN": 80, "VERB": 4}, "ADV": {"ADV": 117, "NOUN": 20, "PREP": 2, "ADJ": 1, "?": 1}, "AUX": {"PREP": 4, "AUX": 118, "?": 3, "NOUN": 3}, "CONJ": {"CONJ": 44, "PRON": 25, "DET": 12, "?": 13, "PREP": 2, "NOUN": 2}, "DET": {"DET": 586, "?": 2}, "NOUN": {"NOUN": 657, "ADJ": 17, "VERB": 7, "?": 1}, "NUM": {"NUM": 2}, "PONCT": {"?": 25}, "PREP": {"PREP": 114}, "PRON": {"PRON": 411, "NOUN": 8, "?": 30, "DET": 25, "CONJ": 1}, "VERB": {"VERB": 311, "NOUN": 450, "ADJ": 5, "PREP": 2, "?": 16, "AUX": 7, "ADV": 1}}}, "syntagme": {"precision": 0.6292
… [290 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log -1 --format='%H %ad %s' --date=iso && git status --short tools/bloc_linguistique.py tools/tests/linguistique/ reports/rapport-pensee-v12.md", "description": "Vérifier commit et propreté des fichiers cibles"}`

  ```
fa1b0c6eb90b3d27ec78f946d677817ba08b419e 2026-11-06 09:16:28 -0500 ÉTAT — MASTER EST À JOUR : s/v7 FAST-FORWARDÉ ET POUSSÉ (375 COMMITS, af28eadd..789b1284)
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 150, "offset": 853}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 160, "offset": 2020}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
853:         return proches
854: 
855:     def _syntagmes_simple(self, texte: str, langue: str,
856:                           pos_verbes: set[int] | None = None) -> list[dict]:
857:         mots = self._mots(texte)
858:         lex = POS_FERME.get(langue, POS_FERME["fr"])
859:         pos_verbes = pos_verbes or set()
860:         par_debut = {m[0]: k for k, m in enumerate(mots)}
861: 
862:         def est_sub(n: str) -> bool:
863:             """Le mot est-il un subordonnant **dans cette langue** ? (« car » est un nom anglais)"""
864:             if n in SUB_PAR_LANGUE.get(langue, set()):
865:                 return True
866:             return n in SUBORDONNANTS and not (langue == "en" and n == "car")
867: 
868:         def est_verbe(d: int, m: str) -> bool:
869:             """Le verbe : le lexique, le POS, ou la **position** après un pronom sujet."""
870:             if _est_verbe(m) or d in pos_verbes:
871:                 return True
872:             n2 = _normaliser(m)
873:             # A17 (R1a) : un pronom n'est jamais un verbe **par la position** (« that I 
… [8252 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
2020:     "it": "Il gatto della vicina che dorme sul tetto si sveglia. Vedi il gatto?",
2021: }
2022: 
2023: 
2024: def _resume_annotation(a: Annotation) -> dict:
2025:     par = a.par_niveau()
2026:     return {"langue": a.langue, "script": a.script, "source": a.source, "refus": a.refus,
2027:             "niveaux": {n: len(es) for n, es in sorted(par.items())},
2028:             "couverture": a.couverture(),
2029:             "fraction_semantique": round(a.fraction_semantique, 4),
2030:             "etiquettes": len(a.etiquettes)}
2031: 
2032: 
2033: def autotest(udhr: pathlib.Path, sortie: pathlib.Path | None = None) -> dict:
2034:     """Mesure la langue, le script, la substitution, le parallèle, la cascade et l'activation."""
2035:     rapport: dict = {"date": time.strftime("%Y-%m-%dT%H:%M:%S"), "niveaux": list(NIVEAUX)}
2036:     profils, tests = charger_profils_udhr(udhr, test=(15, 15), min_test=1)
2037:     t0 = time.perf_counter()
2038:     justes = 0
2039:     scripts_justes = 0
2040:     par_langue: dict[str, list[int]] = collections.defaultdict(lambda: [0,
… [7621 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 190, "offset": 665}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 40, "offset": 2178}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
665:                     for s in base}
666:         except Exception:
667:             return {}
668: 
669:     @staticmethod
670:     def _cible_precedent(texte: str, segment: dict, precedent: dict | None, verbes) -> str | None:
671:         """REL → tête du GN précédent ; SUB après un GV → son verbe (le gouverneur)."""
672:         if not precedent:
673:             return None
674:         if segment.get("type") == "REL" and precedent.get("type") == "GN":
675:             return Heuristique._tete_nom(texte, precedent["debut"], precedent["fin"])
676:         if segment.get("type") == "SUB" and precedent.get("type") == "GV":
677:             if _est_adverbe_seul(precedent):
678:                 return None
679:             return Heuristique._verbe_dans(texte, precedent["debut"], precedent["fin"], verbes)
680:         return None
681: 
682:     @staticmethod
683:     def _candidats_precedent(texte: str, segment: dict, precedent: dict | None) -> list[str]:
684:         """Les candidats que le **précédent** impose : l'antécédent d'une REL, le verbe d'une SUB."""
685: 
… [9251 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
2178:     if args.json:
2179:         print(json.dumps(a.json(avec_duree=args.duree), ensure_ascii=False, indent=1))
2180:     else:
2181:         print(f"langue={a.langue} script={a.script} source={a.source} refus={a.refus or '-'}")
2182:         for n, es in sorted(a.par_niveau().items()):
2183:             for e in es[:4]:
2184:                 print(f"  {n:12s} {e.type:14s} {e.valeur[:40]!r} [{e.debut}:{e.fin}] "
2185:                       f"conf={e.confiance:.2f} src={e.source}")
2186:         print(f"unités sémantiques : {len(a.unites_semantiques)} "
2187:               f"({a.fraction_semantique:.1%} du texte)")
2188:     return 0
2189: 
2190: 
2191: if __name__ == "__main__":
2192:     raise SystemExit(main())

(End of file - total 2192 lines)
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,200p tools/tests/linguistique/test_bloc_linguistique.py", "description": "Lire les tests existants du bloc"}`

  ```
"""Tests du bloc linguistique — contrat, substitution, parallèle, cascade, activation."""
import json
import pathlib
import stat
import sys
import tempfile
import unittest

RACINE = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RACINE / "tools"))
import bloc_linguistique as bl

TEXTE = "Le chat de la voisine qui dort sur le toit se réveille. Va voir le chat !"


class TestBlocLinguistique(unittest.TestCase):
    def setUp(self):
        self.h = bl.Heuristique(segmenter_s=False)
        self.n = bl.MockNeuronal()

    def test_niveaux_et_spans(self):
        a = self.h.analyser(TEXTE, "fr")
        niveaux = {e.niveau for e in a.etiquettes}
        self.assertEqual(set(bl.NIVEAUX) - niveaux, set(), f"niveaux manquants : {set(bl.NIVEAUX)-niveaux}")
        for e in a.etiquettes:
            self.assertGreaterEqual(e.debut, 0)
            self.assertLessEqual(e.fin, len(TEXTE))
            self.assertLessEqual(e.debut, e.fin)

    def test_langue_et_script(self):
        for texte, langue in (("Le chat dort dans la maison.", "fr"),
                              ("The cat sleeps in the house.", "en"),
                              ("Die Katze schläft im Haus.", "d
… [7615 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"bloc_linguistique\" tools/toutes-les-portes.sh tools/porte-bloc-linguistique.sh 2>/dev/null | head -30; ls tools/porte-bloc* 2>/dev/null; grep -n \"bloc_linguistique\" docs/implantation/bloc-linguistique.md 2>/dev/null | h … [56 caractères tronqués]`

  ```
tools/porte-bloc-linguistique.sh:7:python3 -m unittest discover -s tools/tests/linguistique -p 'test_bloc_linguistique.py' || { echo "❌ tests"; exit 1; }
tools/porte-bloc-linguistique.sh:8:python3 tools/bloc_linguistique.py --autotest --udhr data/udhr/articles.jsonl --sortie /tmp/bloc-linguistique-porte.json || { echo "❌ autotest"; exit 1; }
tools/porte-bloc-code.sh
tools/porte-bloc-linguistique.sh
tools/porte-bloc-maths.sh
tools/porte-bloc-tableaux.sh
7:> **fraction** des unités. Le code est [`bloc_linguistique.py`](../../tools/bloc_linguistique.py) ;
330:- Code : [`tools/bloc_linguistique.py`](../../tools/bloc_linguistique.py).
331:- Tests : [`tools/tests/linguistique/test_bloc_linguistique.py`](../../tools/tests/linguistique/test_bloc_linguistique.py).
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && wc -l docs/implantation/bloc-linguistique.md && sed -n 1,140p docs/implantation/bloc-linguistique.md", "description": "Lire le contrat documenté du bloc"}`

  ```
338 docs/implantation/bloc-linguistique.md
# Le bloc linguistique — un contrat, deux implémentations, neuf niveaux

> **Ce que ce document est.** La **spécification** du bloc d'étiquetage linguistique : ce qu'il
> étiquette du **graphème** à la **pragmatique**, ce que chaque étiquette porte, comment
> l'**heuristique CPU** et la **version neuronale** se substituent, se **parallélisent** ou se
> **cascadent**, et comment l'heuristique peut activer la **couche sémantique** sur une
> **fraction** des unités. Le code est [`bloc_linguistique.py`](../../tools/bloc_linguistique.py) ;
> la porte est [`porte-bloc-linguistique.sh`](../../tools/porte-bloc-linguistique.sh) ; la fiche
> est [`rapport-bloc-linguistique.md`](../../reports/rapport-bloc-linguistique.md).
>
> **Ce que ce n'est pas.** Ni un analyseur syntaxique complet, ni un modèle de langue, ni la
> couche sémantique. C'est une **couche de surface typée** : elle **déclare** ce qu'elle couvre,
> avec quelle confiance et quels candidats ; le neuronal (ou l'humain) tranche l'ambigu, et la
> couche sémantique ne reçoit que les unités qui en ont besoin.

## 1. Le besoin

Drave avait trois briques qui **touchaient** la langue sans être l
… [7513 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 140,340p docs/implantation/bloc-linguistique.md", "description": "Lire la suite du contrat documenté"}`

  ```
GBNF** une classe POS par token, dans l'ordre. Les spans sont ceux de la tokenisation du bloc ;
  le modèle ne les invente pas. La confiance par défaut (0,6) le destine à la **cascade** : il ne
  remplace que les tokens que l'heuristique déclare peu sûrs, et laisse les classes fermées à
  l'heuristique.
- **`NeuronalLLMChunks`** : le **tagger de syntagmes**. Il demande une étiquette **BIO** par token
  (`B-GN`/`I-GN`, `B-GV`/`I-GV`, `B-GP`/`I-GP`, `B-REL`/`I-REL`, `B-SUB`/`I-SUB`, `O`) sous
  grammaire GBNF, puis **reconstruit** les spans sur la tokenisation du bloc. Le prompt est
  **few-shot** (cinq exemples hors gold) : sans eux, les frontières (déterminant hors GN,
  auxiliaire hors GV) se perdent. Il ne rend que le niveau `syntagme`.
- **`NeuronalLLMCompose`** : le **bloc complet** — POS + syntagmes dans une seule annotation.
  Il appelle les deux taggers (chacun avec son cache), réunit leurs étiquettes et laisse la
  pragmatique à l'heuristique. C'est le bloc de la cascade complète ; un refus d'un des deux
  n'efface pas l'autre.
- **`NeuronalLLMPragmatique`** : le **tagger de pragmatique**. Un prompt d'analyse, une grammaire
  GBNF qui impose `{acte, negation, modalite, doub
… [10719 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 115, "offset": 1264}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
1264: class MockNeuronal:
1265:     """Le neuronal **de contrat** : même sortie, source `neuronal`, déterministe, sans GPU.
1266: 
1267:     Il ne prétend pas être un modèle : il prouve que le contrat accepte une autre implémentation,
1268:     que le parallèle fusionne et que la cascade n'appelle le neuronal que sur le résidu.
1269:     """
1270: 
1271:     nom = "neuronal"
1272: 
1273:     def __init__(self, profils: dict[str, dict] | None = None):
1274:         self.profils = profils
1275: 
1276:     def analyser(self, texte: str, langue: str | None = None,
1277:                  contexte: str | None = None) -> Annotation:
1278:         t0 = time.perf_counter()
1279:         lg = detecter_langue(texte, self.profils, langue)[0]
1280:         if lg == "und" and langue:
1281:             lg = langue
1282:         script = detecter_script(texte)
1283:         etiquettes: list[Etiquette] = []
1284:         unites: list[Span] = []
1285:         h = Heuristique(segmenter_s=False)
1286:         for d, f, t, typ in h._mots(texte):
1287:             if typ == "mot":
1288:   
… [5892 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la data/udhr/articles.jsonl 2>/dev/null; head -c 500 data/udhr/articles.jsonl 2>/dev/null; echo; grep -c '\"iso3\"' data/udhr/articles.jsonl 2>/dev/null", "description": "Vérifier le corpus UDHR et ses codes langue"}`

  ```
-rw-r--r--. 1 stephane stephane 7661342 17 oct 23:14 data/udhr/articles.jsonl
{"fichier": "udhr_007.xml", "iso3": "cri", "nom": "Sãotomense", "script": "Latn", "art": 0, "titre": "Préambule", "texte": "Punda dignidade di tudo nguê di mundu e dirêtu d'inem igual e andeji cu a na pô bêndê fa sá stê di liberdade, di justiça e di paz ni mundu; Punda fata di conheximentu e displêzu di dirêtu di hómé plovocá atu di malvadez cu ca revoltá cunxença di tudu hómé di mundu e punda ua mundu cu tudu nguê ca pô sa livli, pê pô flá e pê pô quêlê ni cuá cuê 
13996
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"DEEPSEEK_KEY_FILE=${DEEPSEEK_KEY_FILE:-<unset>}\" && ls -la tools/structures/generateur.py && python3 -c \"\nimport sys; sys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nprint('priorite_par_defaut =', bl.priorite_pa … [94 caractères tronqués]`

  ```
DEEPSEEK_KEY_FILE=<unset>
-rw-r--r--. 1 stephane stephane 30580  4 nov 11:41 tools/structures/generateur.py
priorite_par_defaut = None
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,80p tools/structures/generateur.py", "description": "Lire l'API du générateur S"}`

  ```
#!/usr/bin/env python3
"""generateur.py — une phrase brute → des structures candidates (v0 heuristique).

Ce n'est pas un analyseur syntaxique : c'est un **générateur de candidats** à faire valider par
un humain. Il segmente (GN, GV, GP, REL, SUB), devine des rôles par la préposition, puis produit
plusieurs candidats en variant l'**attachement** de chaque segment ambigu (GN le plus proche ou
GV le plus proche).

    python3 generateur.py "Le chat de la voisine qui dort sur le toit se réveille."
    python3 generateur.py --json "..."     # la structure complète
"""
from __future__ import annotations

import json
import re
import unicodedata

DET = set("le la les l un une ce cet cette ces mon ma mes ton ta tes son sa ses "
          "notre nos votre vos leur leurs quel quelle quels quelles".split())
PREP = set("a au aux de du des d en dans par pour sur sous avec sans chez vers entre depuis "
           "pendant durant contre malgre selon pres loin devant derriere apres avant".split())
RELATIFS = set("qui que qu dont ou quoi".split())
CONJ = set("et ou mais donc or ni car quand comme si parce puisque lorsque pendant quoique".split())
COORD = set("et ou mais donc or ni car".split())
SU
… [3976 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Construction du banc de 50 phrases libres et du harnais d'audit

- **bash** `{"command": "mkdir -p /tmp/audit_produit_bl && cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && (time PYTHONPATH=. python3 tools/tests/linguistique/evaluer_gold.py --json /tmp/audit_produit_bl/eval_baseline.json > /tmp/audit_produit_bl/eval_baseline.out 2>&1); echo \"exit=$?\"; tail -5 /tmp/aud … [151 caractères tronqués]`

  ```
started background job bash-2751
  ```

- **write** `{"file_path": "/tmp/audit_produit_bl/phrases.py", "content": "# -*- coding: utf-8 -*-\n\"\"\"50 phrases libres écrites pour l'audit produit du bloc linguistique.\n\nAucune ne vient du gold : elles sont écrites ici, à la main, pour représenters\nl'usage « utilisateur » (longueurs, ponctuation, majusc … [10326 caractères tronqués]`

  ```
<path>/tmp/audit_produit_bl/phrases.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

### 👤 Utilisateur

background job bash-2751 (bash: mkdir -p /tmp/audit_produit_bl && cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && (time PYTHONPATH=. python3 tools/tests/linguistique/evaluer_gold.py --json /tmp/audit_produit_bl/eval_baseline.json > /tmp/audit_produit_bl/eval_baseline.out 2>&1); echo "exit=$?"; tail -5 /tmp/audit_produit_bl/eval_baseline.out) finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "cd /tmp/audit_produit_bl && tail -12 eval_baseline.out && python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/audit_produit_bl/eval_baseline.json'))\nprint('keys:', list(d)[:10])\nh=d['heuristique']['all']; c=d['cascade']['all']\nprint('hand?', d['gold'])\nprint('heur POS', h['pos'][' … [506 caractères tronqués]`

  ```
"labels": 86,
      "exact": 86,
      "topk": 86,
      "exact_taux_span": 1.0
     }
    }
   },
   "attachement_tete": {
    "cibles": 208,
    "labels": 208,
    "top1"
heuristique all: {"pos": {"exactitude": 0.7581, "exactitude_ferme": 0.9004, "exactitude_ouvert": 0.6234, "tokens": 3179, "confusions": {"ADJ": {"ADJ": 50, "NOUN": 80, "VERB": 4}, "ADV": {"ADV": 117, "NOUN": 20, "PREP": 2, "ADJ": 1, "?": 1}, "AUX": {"PREP": 4, "AUX": 118, "?": 3, "NOUN": 3}, "CONJ": {"CONJ": 44, "PRON": 25, "DET": 12, "?": 13, "PREP": 2, "NOUN": 2}, "DET": {"DET": 586, "?": 2}, "NOUN": {"NOUN": 657, "ADJ": 17, "VERB": 7, "?": 1}, "NUM": {"NUM": 2}, "PONCT": {"?": 25}, "PREP": {"PREP": 114}, "PRON": {"PRON": 411, "NOUN": 8, "?": 30, "DET": 25, "CONJ": 1}, "VERB": {"VERB": 311, "NOUN": 450, "ADJ": 5, "PREP": 2, "?": 16, "AUX": 7, "ADV": 1}}}, "syntagme": {"precision": 0.6292, "rappel": 0.5464, "f1": 0.5849, "tp": 1018, "fp": 600, "fn": 845, "tete": {"precision": 0.81, "rappel": 0.6704, "f1": 0.7336, "tp": 1249, "fp": 293, "fn": 614}}, "pragmatique": {"acte": 0.9967, "negation": 0.9771, "modalite": 0.9886, "double_sens": 0.9444}, "fraction_semantique": 0.5537}
keys: ['date', 'heuristique', 'mock_neu
… [349 caractères tronqués]
  ```

- **write** `{"content": "# -*- coding: utf-8 -*-\n\"\"\"Harnais d'audit produit du bloc linguistique — robustesse, contrat, déterminisme.\n\nSort un JSON complet dans /tmp/audit_produit_bl/resultats.json. Ne touche pas au dépôt.\n\"\"\"\nfrom __future__ import annotations\n\nimport collections\nimport hashlib\n … [21682 caractères tronqués]`

  ```
<path>/tmp/audit_produit_bl/audit.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && time python3 audit.py > audit_stdout.txt 2> audit_stderr.txt; echo \"exit=$?\"; head -80 audit_stdout.txt; echo \"--- stderr ---\"; cat audit_stderr.txt | tail -20", "description": "Exécuter le harnais de robustesse et contrat", "timeoutMs": 600000}`

  ```
exit=0
{
 "meta": {
  "date": "2026-11-06T09:50:08",
  "python": "3.13.16",
  "module": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py",
  "commit": "fa1b0c6eb90b3d27ec78f946d677817ba08b419e",
  "phrases": 50,
  "cas_limites": 25,
  "duree_s": 1.51
 },
 "robustesse_50": {
  "crashes": 0,
  "refus": 0,
  "sorties_vides": 0,
  "phrases_avec_anomalie": 34,
  "anomalies_total": 148,
  "anomalies_par_type": {
   "chevauchement_syntagme": 132,
   "préfixe": 6,
   "acte": 4,
   "SUB": 4,
   "suffixe": 2
  },
  "langues": {
   "fr": 34,
   "en": 14,
   "und": 2
  },
  "scripts": {
   "Latn": 48,
   "Cyrl": 1,
   "Hani": 1
  },
  "niveaux_absents": {
   "morphème": 9,
   "syntagme": 2
  }
 },
 "mode_degrade": {
  "phrases_differentes": 34,
  "phrases": 50,
  "syntagmes_perdus": 132,
  "attachements_perdus": 119,
  "exemples": [
   {
    "id": "f01",
    "syntagmes_avec": 3,
    "sans": 2,
    "attachements_avec": 3
   },
   {
    "id": "f02",
    "syntagmes_avec": 14,
    "sans": 3,
    "attachements_avec": 11
   },
   {
    "id": "f03",
    "syntagmes_avec": 10,
    "sans": 3,
    "attachements_avec": 6
   },
   {
    "id": "f04",
    "syntagmes_avec": 7,
    "
… [263 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && python3 - <<'PY'\nimport re, pathlib\np=pathlib.Path('audit.py')\ns=p.read_text()\ns=s.replace('base = {\"niveau\": e.niveau, \"type\": e.type, \"valeur\": e.valeur[:60],\\n                \"debut\": e.debut, \"fin\": e.fin}',\n            'base = {\"niveau\" … [389 caractères tronqués]`

  ```
ok
exit=0
{
 "meta": {
  "date": "2026-11-06T09:50:45",
  "python": "3.13.16",
  "module": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py",
  "commit": "fa1b0c6eb90b3d27ec78f946d677817ba08b419e",
  "phrases": 50,
  "cas_limites": 25,
  "duree_s": 1.47
 },
 "robustesse_50": {
  "crashes": 0,
  "refus": 0,
  "sorties_vides": 0,
  "phrases_avec_anomalie": 34,
  "anomalies_total": 148,
  "anomalies_par_type": {
   "chevauchement_syntagme": 132,
   "valeur_hors_span": 8,
   "acte_hors_candidats": 4,
   "candidat_doublon": 4
  },
  "langues": {
   "fr": 34,
   "en": 14,
   "und": 2
  },
  "scripts": {
   "Latn": 48,
   "Cyrl": 1,
   "Hani": 1
  },
  "niveaux_absents": {
   "morphème": 9,
   "syntagme": 2
  }
 },
 "mode_degrade": {
  "phrases_differentes": 34,
  "phrases": 50,
  "syntagmes_perdus": 132,
  "attachements_perdus": 119,
  "exemples": [
   {
    "id": "f01",
    "syntagmes_avec": 3,
    "sans": 2,
    "attachements_avec": 3
   },
   {
    "id": "f02",
    "syntagmes_avec": 14,
    "sans": 3,
    "attachements_avec": 11
   },
   {
    "id": "f03",
    "syntagmes_avec": 10,
    "sans": 3,
    "attachements_avec": 6
   },
   {
    "id": "f04",
    "sy
… [848 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && python3 - <<'PY'\nimport json\nd=json.load(open('resultats.json'))\nr=d['robustesse_50']\nfor t in ('valeur_hors_span','acte_hors_candidats','candidat_doublon'):\n    print('###',t)\n    for ex in r['anomalies_par_type'][t]['exemples']:\n        print(json.du … [775 caractères tronqués]`

  ```
### valeur_hors_span
{"id": "f11", "type": "valeur_hors_span", "attendu": "TION", "niveau": "morphème", "type_etiquette": "suffixe", "valeur": "tion", "debut": 5, "fin": 9}
{"id": "f11", "type": "valeur_hors_span", "attendu": "PRO", "niveau": "morphème", "type_etiquette": "préfixe", "valeur": "pro", "debut": 15, "fin": 18}
{"id": "f11", "type": "valeur_hors_span", "attendu": "CO", "niveau": "morphème", "type_etiquette": "préfixe", "valeur": "co", "debut": 23, "fin": 25}
{"id": "f11", "type": "valeur_hors_span", "attendu": "CO", "niveau": "morphème", "type_etiquette": "préfixe", "valeur": "co", "debut": 49, "fin": 51}
{"id": "f11", "type": "valeur_hors_span", "attendu": "EZ", "niveau": "morphème", "type_etiquette": "suffixe", "valeur": "ez", "debut": 56, "fin": 58}
{"id": "f14", "type": "valeur_hors_span", "attendu": "Co", "niveau": "morphème", "type_etiquette": "préfixe", "valeur": "co", "debut": 0, "fin": 2}
### acte_hors_candidats
{"id": "f07", "type": "acte_hors_candidats", "candidats": ["assertion", "question", "ordre"], "niveau": "pragmatique", "type_etiquette": "acte", "valeur": "exclamation", "debut": 0, "fin": 70}
{"id": "f26", "type": "acte_hors_candidats", "candidats": ["
… [2224 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && python3 - <<'PY'\nimport json\nd=json.load(open('resultats.json'))\nprint('### cas limites')\nfor c in d['cas_limites']['cas']:\n    print(c['nom'], '| crash=',c['crash'], '| refus=',repr(c.get('refus')), '| etiq=',c.get('etiquettes'), '| langue=',c.get('lang … [337 caractères tronqués]`

  ```
### cas limites
vide | crash= False | refus= 'vide' | etiq= 0 | langue= und | script= Zyyy | anomalies= []
espaces | crash= False | refus= 'vide' | etiq= 0 | langue= und | script= Zyyy | anomalies= []
ponctuation-seule | crash= False | refus= 'vide' | etiq= 0 | langue= und | script= Zyyy | anomalies= []
emoji-seul | crash= False | refus= 'vide' | etiq= 0 | langue= und | script= Zyyy | anomalies= []
chiffres-seuls | crash= False | refus= '' | etiq= 6 | langue= und | script= Zyyy | anomalies= []
un-mot | crash= False | refus= '' | etiq= 7 | langue= und | script= Latn | anomalies= []
anglais-deux-mots | crash= False | refus= '' | etiq= 11 | langue= und | script= Latn | anomalies= []
mot-très-long | crash= False | refus= '' | etiq= 9 | langue= und | script= Latn | anomalies= []
nul | crash= False | refus= '' | etiq= 8 | langue= und | script= Latn | anomalies= []
espace-invisible | crash= False | refus= 'vide' | etiq= 0 | langue= und | script= Zyyy | anomalies= []
retour-ligne | crash= False | refus= 'vide' | etiq= 0 | langue= und | script= Zyyy | anomalies= []
accent-décomposé | crash= False | refus= '' | etiq= 18 | langue= und | script= Latn | anomalies= []
arabe | crash= False | refu
… [2123 caractères tronqués]
  ```

- **write** `{"content": "# -*- coding: utf-8 -*-\n\"\"\"Performance, mémoire, déterminisme inter-processus du bloc linguistique.\"\"\"\nfrom __future__ import annotations\n\nimport hashlib\nimport json\nimport pathlib\nimport resource\nimport statistics\nimport subprocess\nimport sys\nimport time\nimport tracem … [5402 caractères tronqués]`

  ```
<path>/tmp/audit_produit_bl/performance.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && time python3 performance.py > performance_stdout.txt 2> performance_stderr.txt; echo \"exit=$?\"; cat performance_stdout.txt; echo \"--- stderr ---\"; tail -20 performance_stderr.txt", "description": "Mesurer temps, mémoire et déterminisme", "timeoutMs": 9000 … [3 caractères tronqués]`

  ```
exit=0
{
 "machine": {
  "cpu": "Intel(R) Xeon(R) CPU E5-2687W v3 @ 3.10GHz",
  "python": "3.13.16"
 },
 "temps": [
  {
   "mots": 10,
   "caracteres": 51,
   "repetitions": 30,
   "froid_ms": 6.24,
   "median_ms": 1.09,
   "moyenne_ms": 1.09,
   "ecart_type_ms": 0.04,
   "min_ms": 1.04,
   "max_ms": 1.15,
   "p95_ms": 1.13,
   "ms_par_mot": 0.109,
   "phrases_par_s": 914.9,
   "etiquettes": 54,
   "etiquettes_par_mot": 5.4,
   "unites": 5,
   "attachements": 4
  },
  {
   "mots": 50,
   "caracteres": 268,
   "repetitions": 21,
   "froid_ms": 4.64,
   "median_ms": 4.47,
   "moyenne_ms": 4.49,
   "ecart_type_ms": 0.07,
   "min_ms": 4.43,
   "max_ms": 4.75,
   "p95_ms": 4.54,
   "ms_par_mot": 0.089,
   "phrases_par_s": 223.6,
   "etiquettes": 260,
   "etiquettes_par_mot": 5.2,
   "unites": 26,
   "attachements": 19
  },
  {
   "mots": 200,
   "caracteres": 1126,
   "repetitions": 11,
   "froid_ms": 18.64,
   "median_ms": 17.5,
   "moyenne_ms": 17.67,
   "ecart_type_ms": 0.65,
   "min_ms": 16.97,
   "max_ms": 18.8,
   "p95_ms": 18.4,
   "ms_par_mot": 0.088,
   "phrases_par_s": 57.1,
   "etiquettes": 1061,
   "etiquettes_par_mot": 5.3,
   "unites": 99,
   "attachements": 74
  }
 ],
 "m
… [3254 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && python3 - <<'PY'\nimport json\nd=json.load(open('resultats.json'))\nc=d['contrat']\nfor k in ('cles_annotation','cles_etiquette','champs_vides','langue_formats','refus_valeurs','sources_etiquettes','sources_annotation','valeur_egale_span','couts_par_mode'):\n … [350 caractères tronqués]`

  ```
### cles_annotation
[
 [
  "contexte",
  "cout",
  "etiquettes",
  "fraction_semantique",
  "langue",
  "refus",
  "script",
  "source",
  "texte",
  "trace",
  "unites_semantiques"
 ]
]
### cles_etiquette
[
 [
  "candidats",
  "confiance",
  "debut",
  "fin",
  "langue",
  "meta",
  "niveau",
  "script",
  "source",
  "type",
  "valeur"
 ]
]
### champs_vides
{
 "graphème.candidats": 1778,
 "graphème.meta": 1778,
 "mot.candidats": 963,
 "mot.meta": 963,
 "pos.candidats": 384,
 "discours.meta": 79,
 "document.candidats": 53,
 "document.meta": 53,
 "phrase.candidats": 76,
 "phrase.meta": 76,
 "pragmatique.meta": 69,
 "morphème.meta": 134
}
### langue_formats
{
 "2": 48,
 "3": 2
}
### refus_valeurs
{
 "": 50
}
### sources_etiquettes
{
 "heuristique": 4320
}
### sources_annotation
{
 "heuristique": 50
}
### valeur_egale_span
{
 "graphème": {
  "egales": 1778,
  "total": 1778
 },
 "mot": {
  "egales": 963,
  "total": 963
 },
 "pos": {
  "egales": 806,
  "total": 806
 },
 "syntagme": {
  "egales": 362,
  "total": 362
 },
 "morphème": {
  "egales": 126,
  "total": 134
 }
}
### couts_par_mode
{
 "heuristique": {
  "cles": [
   "caracteres",
   "duree_s",
   "etiquettes",
   "octets"
  ],
 
… [1441 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && python3 - <<'PY'\nimport json\nd=json.load(open('resultats.json'))\nprint(json.dumps(d['langue_profils'],ensure_ascii=False,indent=1))\nPY", "description": "Inspecter le format des codes langue"}`

  ```
{
 "disponible": true,
 "langues_profil": 398,
 "duree_chargement_s": 0.887,
 "details": [
  {
   "texte": "Le chat dort sur le canapé.",
   "sans_profils": [
    "fr",
    "Latn"
   ],
   "avec_profils": [
    "hns",
    "Latn"
   ]
  },
  {
   "texte": "The cat sleeps on the warm roof.",
   "sans_profils": [
    "en",
    "Latn"
   ],
   "avec_profils": [
    "sco",
    "Latn"
   ]
  },
  {
   "texte": "Die Katze schläft auf dem Dach.",
   "sans_profils": [
    "de",
    "Latn"
   ],
   "avec_profils": [
    "deu",
    "Latn"
   ]
  },
  {
   "texte": "El gato duerme en el tejado.",
   "sans_profils": [
    "es",
    "Latn"
   ],
   "avec_profils": [
    "und",
    "Latn"
   ]
  }
 ],
 "hint_fr_sans_profils": "en",
 "hint_fr_avec_profils": "sco"
}
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && python3 - <<'PY'\nimport json, sys, collections\nsys.path.insert(0,'/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools')\nsys.path.insert(0,'.')\nimport bloc_linguistique as bl\nfrom phrases import PHRASES\nh=bl.Heuristique()\nfor pid in ('f01','f02','e29' … [1093 caractères tronqués]`

  ```
====================================================================================================
f01 fr/courte | langue fr | script Latn | etiq 32 | fraction 0.5185
TEXTE: Le chat dort sur le canapé.
POS: Le/DET chat/NOUN dort/VERB sur/PREP le/DET canapé/NOUN
SYNTAGMES:
    ('GN', 0, 7, 'Le chat', 'dort', False)
    ('GV', 8, 12, 'dort', 'chat', False)
    ('GP', 13, 26, 'sur le canapé', 'dort', False)
PHRASES: [(0, 27, 'type', 'déclarative')]
PRAG: [('acte', 'assertion', ['assertion', 'question', 'ordre'])]
DOC: [('paragraphe', 'Le chat dort sur le canapé.', 0, 27)]
====================================================================================================
f02 fr/longue | langue fr | script Latn | etiq 140 | fraction 0.575
TEXTE: La voisine arrose les fleurs du jardin chaque matin avant de partir au travail, puis elle rentre vers dix-huit heures et prépare le dîner pour ses deux enfants.
POS: La/DET voisine/NOUN arrose/NOUN les/DET fleurs/NOUN du/PREP jardin/NOUN chaque/NOUN matin/NOUN avant/PREP de/PREP partir/NOUN au/PREP travail/NOUN puis/NOUN elle/PRON rentre/NOUN vers/PREP dix-huit/NOUN heures/NOUN et/CONJ prépare/NOUN le/DET dîner/NOUN pour/PREP ses/DET deux/NUM
… [10913 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && python3 - <<'PY'\nimport json, statistics, collections, sys\nsys.path.insert(0,'/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools')\nimport bloc_linguistique as bl\nd=json.load(open('resultats.json'))\nr=d['robustesse_50']\ndet=r['detail']\nprint('labels  … [3211 caractères tronqués]`

  ```
labels total 4320
labels/phrase min-med-max 14 78.0 417
fraction min-med-max 0.3529 0.5493 0.875
mots total 819
niveaux labels totaux Counter({'graphème': 1778, 'mot': 963, 'pos': 806, 'syntagme': 362, 'morphème': 134, 'discours': 79, 'phrase': 76, 'pragmatique': 69, 'document': 53})
sentences avec >=1 syntagme 48
sentences avec >=1 attachement 48
attachements total 265

overlap sentences 31 pairs 132
max [('x50', 16, 'fr', 84), ('f02', 9, 'fr', 28), ('f23', 9, 'fr', 18), ('x45', 9, 'fr', 18), ('f03', 6, 'fr', 18), ('f09', 6, 'fr', 21), ('f06', 5, 'fr', 11), ('f08', 5, 'fr', 12), ('f10', 5, 'fr', 19), ('f13', 5, 'fr', 14)]
median pairs among affected 3

overlap kinds {('même_type', 'inclusion'): 58, ('ratio', 'inclusion'): 113, ('même_type', 'chevauchement_partiel'): 3, ('ratio', 'partiel'): 19, ('types_différents', 'inclusion'): 55, ('types_différents', 'chevauchement_partiel'): 16}
labels syntagme impliqués 188 sur 362

POS couverture tous tokens: manquants 157 / 963 par type {'ponctuation': 137, 'nombre': 20}
tokens par type {'mot': 806, 'ponctuation': 137, 'nombre': 20}

graph coverage
x46 {'chars': 144, 'couverts': 137, 'taux': 0.9514, 'manquants': 7, 'categories': {'Cc': 7}}

… [38 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && python3 - <<'PY'\nimport json, sys, collections, re\nsys.path.insert(0,'/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools')\nsys.path.insert(0,'.')\nimport bloc_linguistique as bl\nfrom phrases import PHRASES, CAS_LIMITES\nh=bl.Heuristique()\n# 1) types d … [3773 caractères tronqués]`

  ```
MOTS 'https://example.com/a.pdf' [(0, 5, 'https', 'mot'), (5, 6, ':', 'ponctuation'), (6, 7, '/', 'ponctuation'), (7, 8, '/', 'ponctuation'), (8, 15, 'example', 'mot'), (15, 16, '.', 'ponctuation'), (16, 19, 'com', 'mot'), (19, 20, '/', 'ponctuation'), (20, 21, 'a', 'mot'), (21, 22, '.', 'ponctuation'), (22, 25, 'pdf', 'mot')]
MOTS 'Merci 😊 !' [(0, 5, 'Merci', 'mot'), (6, 7, '😊', 'ponctuation'), (8, 9, '!', 'ponctuation')]
MOTS 'contact@example.org' [(0, 7, 'contact', 'mot'), (7, 8, '@', 'ponctuation'), (8, 15, 'example', 'mot'), (15, 16, '.', 'ponctuation'), (16, 19, 'org', 'mot')]
MOTS '12,5 %' [(0, 2, '12', 'nombre'), (2, 3, ',', 'ponctuation'), (3, 4, '5', 'nombre'), (5, 6, '%', 'ponctuation')]
MOTS "aujourd'hui" [(0, 11, "aujourd'hui", 'mot')]

attachements 265 cibles fermées 16 ouvertes 249
cibles fermées top [('au', 3), ('was', 3), ('lui', 2), ('pas', 2), ('have', 2), ('entre', 2), ('ne', 1), ('Tu', 1)]
cibles ouvertes par classe Counter()
Counter()
classes cibles ouvertes Counter({'NOUN': 197, 'VERB': 37, 'DET': 8, 'ADJ': 7})
exemples cibles fermées ['au', 'lui', 'pas', 'ne', 'Tu', 'was', 'have', 'entre']

### document titres
x46 '# Notes de réunion' | span '# Notes de réun
… [620 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && python3 - <<'PY'\nimport json, sys, collections, re, os\nsys.path.insert(0,'/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools')\nsys.path.insert(0,'.')\nimport bloc_linguistique as bl\nfrom phrases import PHRASES, CAS_LIMITES\nh=bl.Heuristique()\n\ndef sa … [4907 caractères tronqués]`

  ```
document labels 53 tronqués 42 [('f02', 'paragraphe', 160, 60), ('f03', 'paragraphe', 87, 60), ('f04', 'paragraphe', 129, 60), ('f05', 'paragraphe', 100, 60), ('f06', 'paragraphe', 63, 60), ('f07', 'paragraphe', 70, 60), ('f08', 'paragraphe', 81, 60), ('f09', 'paragraphe', 110, 60)] titres [('x46', '# Notes de réunion'), ('x48', '今天天气很好，我们去公园散步吧。')]
titres cas limites [('chiffres-seuls', '1234567890'), ('arabe', 'مرحبا بالعالم، كيف حالك اليوم؟'), ('hébreu', 'שלום עולם, מה שלומך היום?'), ('japonais', '今日はいい天気ですね。散歩に行きましょう。')]
actes {'assertion': 50, 'question': 6, 'exclamation': 4} double_sens 9 | connecteurs attendus 26 émis 26 manqués []
URL phrases [(0, 21, "'Voir https://example.'"), (21, 45, "'com/rapports/2024/final.'"), (45, 63, "'pdf pour la suite.'")]
URL mot types Counter({'mot': 10, 'ponctuation': 9, 'nombre': 1})
contexte label [('pragmatique', 'contexte', 'réponse à la question précédente', 'humain', 0, 13)]
contexte annotation réponse à la question précédente
parallele source annotation parallele sources labels ['heuristique', 'neuronal'] langue fr langues labels ['fr']
parallele source annotation parallele sources labels ['heuristique', 'neuronal'] langue en langues l
… [896 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && python3 - <<'PY'\nimport sys, json, collections, time\nsys.path.insert(0,'/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools')\nsys.path.insert(0,'.')\nimport bloc_linguistique as bl\nfrom phrases import PHRASES\nRACINE='/home/stephane/Data13TB/stephane/Gi … [1005 caractères tronqués]`

  ```
attendu fr/en/und -> sans profils 50 / 50 avec profils 2 / 50
det sans {'fr': 34, 'en': 14, 'und': 2}
det avec {'hns': 1, 'fra': 28, 'und': 8, 'oci': 2, 'sco': 3, 'eng': 7, 'pcm': 1}
duree 50 avec profils 0.43 s
('f01', 'fr', 'fr', 'hns')
('f02', 'fr', 'fr', 'fra')
('f03', 'fr', 'fr', 'und')
('f04', 'fr', 'fr', 'fra')
('f05', 'fr', 'fr', 'fra')
('f06', 'fr', 'fr', 'fra')
('f07', 'fr', 'fr', 'oci')
('f08', 'fr', 'fr', 'fra')
('f09', 'fr', 'fr', 'fra')
('f10', 'fr', 'fr', 'fra')
('f11', 'fr', 'fr', 'fra')
('f12', 'fr', 'fr', 'fra')
('f13', 'fr', 'fr', 'fra')
('f14', 'fr', 'fr', 'fra')
('f15', 'fr', 'fr', 'fra')
('f16', 'fr', 'fr', 'fra')
('f17', 'fr', 'fr', 'fra')
('f18', 'fr', 'fr', 'fra')
('f19', 'fr', 'fr', 'fra')
('f20', 'fr', 'fr', 'fra')
('f21', 'fr', 'fr', 'fra')
('f22', 'fr', 'fr', 'fra')
('f23', 'fr', 'fr', 'und')
('f24', 'fr', 'fr', 'fra')
('f25', 'fr', 'fr', 'fra')
('f26', 'fr', 'fr', 'fra')
('f27', 'fr', 'fr', 'fra')
('f28', 'fr', 'fr', 'fra')
('e29', 'en', 'en', 'sco')
('e30', 'en', 'en', 'eng')
('e31', 'en', 'en', 'eng')
('e32', 'en', 'en', 'und')
('e33', 'en', 'en', 'eng')
('e34', 'en', 'en', 'eng')
('e35', 'en', 'en', 'sco')
('e36', 'en', 'en', 'und')
('e37', 'en', 'e
… [365 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && python3 - <<'PY'\nimport sys, json, collections\nsys.path.insert(0,'/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools')\nsys.path.insert(0,'.')\nimport bloc_linguistique as bl\nfrom phrases import PHRASES\nh=bl.Heuristique(); n=bl.MockNeuronal()\n# cascad … [2161 caractères tronqués]`

  ```
cascade appels 50 /50 residus {'morphème': 50, 'syntagme': 50, 'discours': 50, 'pragmatique': 50, 'pos': 2}
couverture f01 {'graphème': 0.99, 'mot': 0.98, 'pos': 0.92, 'syntagme': 0.4, 'discours': 0.5, 'document': 0.7, 'phrase': 0.85, 'pragmatique': 0.45}
parallele vide '... !!! ???' refus= '' etiq= 4 source= parallele
cascade vide '... !!! ???' refus= '' etiq= 4 source= cascade
parallele vide '' refus= '' etiq= 0 source= parallele
cascade vide '' refus= '' etiq= 0 source= cascade
parallele contexte annotation '' label humain [('contexte', 'contexte de test')]
cascade contexte annotation '' label humain [('contexte', 'contexte de test')]

TEXT La température est de 12.5 degrés. C'est chaud.
phrases [(0, 25, "'La température est de 12.'"), (25, 34, "'5 degrés.'"), (34, 47, '" C\'est chaud."')]
mots [(22, 24, '12', 'nombre'), (24, 25, '.', 'ponctuation'), (25, 26, '5', 'nombre'), (33, 34, '.', 'ponctuation'), (46, 47, '.', 'ponctuation')]

TEXT Le rendez-vous est le 12.03.2024 à 9 h.
phrases [(0, 25, "'Le rendez-vous est le 12.'"), (25, 28, "'03.'"), (28, 39, "'2024 à 9 h.'")]
mots [(22, 24, '12', 'nombre'), (24, 25, '.', 'ponctuation'), (25, 27, '03', 'nombre'), (27, 28, '.', 'ponct
… [602 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && python3 - <<'PY'\nimport json\nd=json.load(open('eval_baseline.json'))\nfor mode in ('heuristique','mock_neuronal','parallele','cascade'):\n    x=d[mode]['all']\n    print(mode,'POS',x['pos']['exactitude'],'F1',x['syntagme']['f1'],'couverture',x['attachement' … [204 caractères tronqués]`

  ```
heuristique POS 0.7581 F1 0.5849 couverture 0.9289
mock_neuronal POS 0.3454 F1 0.5763 couverture 0.8326
parallele POS 0.7465 F1 0.6141 couverture 0.8703
cascade POS 0.7465 F1 0.6141 couverture 0.8703
cascade appels neuronal 1676
cascade verdict {'pos_hand': True, 'pos_reel': True, 'pos_synthetique': True, 'syntagme_hand': True, 'syntagme_reel': True, 'syntagme_synthetique': True, 'tete': True, 'acte': True, 'cascade_pos': False, 'cascade_syntagme': True, 'attachement_topk': True, 'attachement_hasard': True, 'attachement_tete_couverture': True, 'attachement_tete_topk': True, 'attachement_tete_hasard': True, 'reel_non_requis': True}
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && python3 - <<'PY'\nimport sys,time,statistics,json\nsys.path.insert(0,'/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools')\nsys.path.insert(0,'.')\nimport bloc_linguistique as bl\nfrom phrases import PHRASES\nBASE=' '.join([p['texte'] for p in PHRASES if p … [687 caractères tronqués]`

  ```
heuristique median_ms 20.28 min 19.63 max 26.76 labels 1061
mock median_ms 4.02 min 3.96 max 4.42 labels 215
parallele median_ms 27.71 min 27.12 max 38.94 labels 1059
cascade median_ms 29.34 min 28.07 max 39.24 labels 1059
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && head -60 reports/pensee-v12.json && echo \"---\" && head -40 reports/pensee-audit-v10.json", "description": "Lire le style des JSON de fiches"}`

  ```
{
 "date": "2026-11-06",
 "ligne": "B13",
 "portes": "183/183",
 "avant": {
  "labels": 221,
  "exact": 221,
  "couverture": 0.9247,
  "spans": 18
 },
 "apres": {
  "labels": 222,
  "exact": 222,
  "exact_span": 1.0,
  "couverture": 0.9289,
  "f1": 0.5893,
  "f1_s": 0.5014,
  "f1_chunker": 0.6203,
  "tete": 0.7392,
  "fr": "136/136",
  "en": "86/86",
  "topk": 221,
  "topk_taux": 0.9247,
  "spans": {
   "REL": 8,
   "SUB": 5,
   "GP": 4,
   "total": 17
  },
  "dev": {
   "exact": 153,
   "labels": 153,
   "couverture": 0.9387
  },
  "test": {
   "exact": 69,
   "labels": 69,
   "couverture": 0.9079
  }
 },
 "correction": "AMBIGUES_REL : REL après un GN, SUB ailleurs",
 "controle_negatif": {
  "permutation": "1,997/220 (0,908 %) p=0",
  "candidat_aleatoire": "42,14 % top-1"
 },
 "limites": [
  "17 spans inatteignables",
  "in-sample",
  "gold 612"
 ]
}
---
{
 "rapport": "audit-v10",
 "ligne": "B13",
 "branche": "s/v7",
 "commit_audite": "710ec7f9",
 "commit_parent": "160d08ca",
 "date": "2026-11-05",
 "objet": "Audit de l'état v10 : rejeu des valeurs sur le vivant 612 et le gelé 602, ablations par règle, contrôles négatifs, dev/test, portes.",
 "methode": {
  "gold_vivant": {
   "so
… [1020 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,80p reports/rapport-coherence-fiches-v8.md", "description": "Lire le début de la fiche cohérence v8"}`

  ```
# Cohérence des fiches B13 du 2026-11-05 — v2 → v8 (état `f908d7b0`)

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ❌
> **8 fiches auditées** (1 courante, 7 historiques), **42 écarts** dont **7 critiques** ;
> **8/8** ont au moins un écart ; **3 contrôles négatifs invalides** (v4, v5, v6) et **2 absents**
> (v8, gold-split) ; **7 mentions d'historique obsolètes** (v2→v7) et **1 imprécise** (v8) ;
> **5 lignes** de `reports/README.md` à corriger ; **1 lien cassé** au commit (`rapport-spans-v7.md`,
> cité par la v8, absent de `f908d7b0`) ; **2 tableaux dont la somme visible ne tombe pas**
> (corrections de la v2, règles de la v8).
>
> **État audité** : commit **`f908d7b0`** (2026-11-05 21:08, branche `s/v7`), le commit demandé
> (avant `d497324b`). Les huit fiches, leurs huit JSON et `reports/README.md` sont lus **à ce
> commit** (`git show f908d7b0:…`), pas dans l'arbre de travail.
>
> **HEAD a bougé (note de version)** : pendant l'audit, HEAD est passé de `f908d7b0` à
> **`d497324b`** (« la v8 réécrite honnêtement : +17 net, 7 régressions ; audits A17/A19
> intégrés »). Ce commit corrige déjà une partie de ce rapport : la v8 es
… [4302 caractères tronqués]
  ```

- **write** `{"content": "# -*- coding: utf-8 -*-\n\"\"\"Mesures finales de performance : heuristique et compositions, 10/50/200 mots.\"\"\"\nfrom __future__ import annotations\n\nimport json\nimport pathlib\nimport resource\nimport statistics\nimport sys\nimport time\nimport tracemalloc\n\nRACINE = pathlib.Path … [3853 caractères tronqués]`

  ```
<path>/tmp/audit_produit_bl/performance_final.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('performance_final.py'); s=p.read_text()\ns=s.replace('''    t0 = time.perf_counter()\n    a2000 = h.analyser(texte2000)\n    stress = {\"mots\": 2000, \"duree_s\": round(time.perf_counter() - t0, 2),\n         … [1110 caractères tronqués]`

  ```
ok
exit=1
Traceback (most recent call last):
  File "/tmp/audit_produit_bl/performance_final.py", line 105, in <module>
    raise SystemExit(main())
                     ~~~~^^
  File "/tmp/audit_produit_bl/performance_final.py", line 62, in main
    r = mediane(bloc, texte, rep)
  File "/tmp/audit_produit_bl/performance_final.py", line 42, in mediane
    "ms_par_mot": round(statistics.median(temps) / n, 3),
                                                   ^
NameError: name 'n' is not defined
=== cold start ===
99.2 ms 32
0.14 s 27632 Kio
109.0 ms 32
0.15 s 27368 Kio
113.3 ms 32
0.15 s 27368 Kio
[stderr]

real	0m0,218s
user	0m0,188s
sys	0m0,029s
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('performance_final.py'); s=p.read_text()\ns=s.replace('def mediane(bloc, texte, repetitions):','def mediane(bloc, texte, repetitions, n):')\ns=s.replace('r = mediane(bloc, texte, rep)','r = mediane(bloc, texte, … [252 caractères tronqués]`

  ```
ok
exit=0
{
 "machine": {
  "cpu": "Intel Xeon E5-2687W v3 @ 3.10 GHz",
  "python": "3.13.16"
 },
 "temps": {
  "heuristique": [
   {
    "median_ms": 1.08,
    "moyenne_ms": 1.28,
    "ecart_type_ms": 0.28,
    "min_ms": 1.05,
    "max_ms": 1.75,
    "p95_ms": 1.72,
    "ms_par_mot": 0.108,
    "phrases_par_s": 922.8,
    "mots": 10,
    "caracteres": 51,
    "repetitions": 31
   },
   {
    "median_ms": 4.6,
    "moyenne_ms": 5.11,
    "ecart_type_ms": 0.93,
    "min_ms": 4.49,
    "max_ms": 7.42,
    "p95_ms": 7.05,
    "ms_par_mot": 0.092,
    "phrases_par_s": 217.5,
    "mots": 50,
    "caracteres": 268,
    "repetitions": 21
   },
   {
    "median_ms": 19.43,
    "moyenne_ms": 23.52,
    "ecart_type_ms": 6.58,
    "min_ms": 17.75,
    "max_ms": 32.77,
    "p95_ms": 32.74,
    "ms_par_mot": 0.097,
    "phrases_par_s": 51.5,
    "mots": 200,
    "caracteres": 1126,
    "repetitions": 11
   }
  ],
  "mock_neuronal": [
   {
    "median_ms": 0.3,
    "moyenne_ms": 0.31,
    "ecart_type_ms": 0.01,
    "min_ms": 0.29,
    "max_ms": 0.35,
    "p95_ms": 0.32,
    "ms_par_mot": 0.03,
    "phrases_par_s": 3319.7,
    "mots": 10,
    "caracteres": 51,
    "repetitions": 31
   },
   {
   
… [2475 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && python3 - <<'PY'\nimport sys,time\nsys.path.insert(0,'/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools')\nsys.path.insert(0,'.')\nimport bloc_linguistique as bl\nfrom phrases import PHRASES\nBASE=' '.join([p['texte'] for p in PHRASES if p['cat'].startswi … [515 caractères tronqués]`

  ```
200 median_s 0.019 ms/mot 0.096 labels 1061
500 median_s 0.07 ms/mot 0.139 labels 2613
1000 median_s 0.166 ms/mot 0.166 labels 5218
2000 median_s 0.482 ms/mot 0.241 labels 10438
4000 median_s 1.574 ms/mot 0.394 labels 20826
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && python3 - <<'PY'\nimport sys,cProfile,pstats,io\nsys.path.insert(0,'/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools')\nsys.path.insert(0,'.')\nimport bloc_linguistique as bl\nfrom phrases import PHRASES\nBASE=' '.join([p['texte'] for p in PHRASES if p[' … [389 caractères tronqués]`

  ```
2923335 function calls in 8.621 seconds

   Ordered by: cumulative time
   List reduced from 155 to 18 due to restriction <18>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.442    0.442    8.624    8.624 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py:1003(analyser)
      526    0.323    0.001    3.792    0.007 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py:800(_cible_proche)
   199302    1.426    0.000    3.159    0.000 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py:461(_est_adverbe_seul)
     1331    0.500    0.000    1.027    0.001 {built-in method builtins.sorted}
   122201    0.505    0.000    0.858    0.000 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py:144(_normaliser)
      972    0.013    0.000    0.838    0.001 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py:835(_verbes_proches)
     6031    0.283    0.000    0.766    0.000 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py:481(_est_verbe)
   520838    0.757    0.000    0.757    0.000 {method 'get' of 'dict' objects}
    
… [1254 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && python3 - <<'PY'\nimport sys, json, collections, random, copy\nsys.path.insert(0,'/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools')\nsys.path.insert(0,'.')\nimport bloc_linguistique as bl\nfrom phrases import PHRASES\nh=bl.Heuristique()\n\n# 1) simulati … [3518 caractères tronqués]`

  ```
SIMULATION dedupe: paires 132 -> 0 | syntagmes 362 -> 292 | attachements 265 -> 215 | phrases 31
labels syntagme retirés 70 attachements retirés 50
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 57, in <module>
NameError: name 'check_an' is not defined
[exit code: 1]
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && python3 - <<'PY'\nimport sys, json, copy\nsys.path.insert(0,'/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools')\nsys.path.insert(0,'/tmp/audit_produit_bl')\nimport bloc_linguistique as bl\nimport audit\nfrom phrases import PHRASES\nh=bl.Heuristique()\n\n … [3274 caractères tronqués]`

  ```
### mutations
span_hors_texte detectee True | ['chevauchement_syntagme', 'span_hors_texte']
cible_absente detectee True | ['chevauchement_syntagme', 'cible_absente']
chevauchement_syntagme detectee True | ['attachement_segment_mismatch', 'chevauchement_syntagme', 'valeur_hors_span']
confiance_hors_bornes detectee True | ['chevauchement_syntagme', 'confiance_hors_bornes']
valeur_hors_span detectee True | ['chevauchement_syntagme', 'valeur_hors_span']
fraction_incoherente detectee True | ['chevauchement_syntagme', 'fraction_incoherente']
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 41, in <module>
ModuleNotFoundError: No module named 'tools'
[exit code: 1]
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && python3 - <<'PY'\nimport sys\nRACINE='/home/stephane/Data13TB/stephane/GitHub/Qtrinet'\nsys.path.insert(0, RACINE)\nsys.path.insert(0, RACINE+'/tools')\nsys.path.insert(0, '/tmp/audit_produit_bl')\nimport bloc_linguistique as bl\nfrom tools.tests.linguistique … [2105 caractères tronqués]`

  ```
avant F1 0.5849 P 0.6292 R 0.5464 tp/fp/fn 1018 600 845 | tete 0.7336 | att exact 222 / 239 0.9289 | labels 17847 att 946 overlaps 363
apres F1 0.6141 P 0.7283 R 0.5309 tp/fp/fn 989 369 874 | tete 0.7432 | att exact 208 / 239 0.8703 | labels 17587 att 812 overlaps 0
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && python3 - <<'PY'\nimport sys, collections\nRACINE='/home/stephane/Data13TB/stephane/GitHub/Qtrinet'\nsys.path.insert(0, RACINE); sys.path.insert(0, RACINE+'/tools')\nimport bloc_linguistique as bl\nfrom tools.tests.linguistique import evaluer_gold as eg\nh=bl … [3025 caractères tronqués]`

  ```
aucune               F1 0.5849 P 0.6292 R 0.5464 | tete 0.7336 | att 222/239=0.9289 | labels 17847 att 946 ov 363
current              F1 0.6141 P 0.7283 R 0.5309 | tete 0.7432 | att 208/239=0.8703 | labels 17587 att 812 ov 0
union_dabord_court   F1 0.4961 P 0.6008 R 0.4224 | tete 0.6606 | att 199/239=0.8326 | labels 17539 att 849 ov 0
union_dabord_conf    F1 0.4961 P 0.6008 R 0.4224 | tete 0.6606 | att 199/239=0.8326 | labels 17539 att 849 ov 0
court_dabord         F1 0.6141 P 0.7283 R 0.5309 | tete 0.7432 | att 208/239=0.8703 | labels 17587 att 812 ov 0
long_dabord          F1 0.4920 P 0.6066 R 0.4138 | tete 0.6707 | att 196/239=0.8201 | labels 17500 att 805 ov 0
conf_dabord          F1 0.4961 P 0.6008 R 0.4224 | tete 0.6606 | att 199/239=0.8326 | labels 17539 att 849 ov 0
attachement_dabord   F1 0.4961 P 0.6008 R 0.4224 | tete 0.6606 | att 199/239=0.8326 | labels 17539 att 849 ov 0
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && python3 - <<'PY'\nimport json\nd=json.load(open('eval_baseline.json'))\nfor mode in ('heuristique','parallele','cascade'):\n    a=d[mode]['all']['attachement']\n    print(mode, {k:a[k] for k in ('cibles','labels','exact','exact_taux_span','couverture','topk_t … [84 caractères tronqués]`

  ```
heuristique {'cibles': 239, 'labels': 222, 'exact': 222, 'exact_taux_span': 1.0, 'couverture': 0.9289, 'topk_taux_span': 0.9955}
parallele {'cibles': 239, 'labels': 208, 'exact': 208, 'exact_taux_span': 1.0, 'couverture': 0.8703, 'topk_taux_span': 0.9952}
cascade {'cibles': 239, 'labels': 208, 'exact': 208, 'exact_taux_span': 1.0, 'couverture': 0.8703, 'topk_taux_span': 0.9952}
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && python3 - <<'PY'\nimport sys, json, collections\nsys.path.insert(0,'/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools')\nsys.path.insert(0,'.')\nimport bloc_linguistique as bl\nfrom phrases import PHRASES\nh=bl.Heuristique()\nlead=trail=multi=0; nphr=0\nf … [948 caractères tronqués]`

  ```
phrases total 60 textes multi-phrases 6 commencent par espace 6 finissent par espace 0
f03 "Le livre que tu m'as prêté hier soir était passionnant, même si la fin" | nb 1
f05 '« Je ne sais pas », répondit-elle en haussant les épaules ; son frère,' | nb 1
f14 'Combien de temps faudra-t-il encore attendre avant que la situation ne' | nb 1
f15 'Les prix ont augmenté de 12,5 % entre janvier et mars 2024, soit 3 poi' | nb 1
e34 'The prices rose by 12.5% between January and March 2024, three points ' | nb 1
x43 'Le rapport complet est disponible sur https://example.com/rapports/202' | nb 1
x45 'Ceci est une phrase sans ponctuation finale et elle continue longtemps' | nb 1
x46 "# Notes de réunion\n\nLe budget 2025 a été validé à l'unanimité.\n\n- Prio" | nb 1
x50 "Dans le petit village où je passais mes vacances quand j'étais enfant," | nb 1

phrase counts per text
f01 1 ; f02 1 ; f03 1 ; f04 1 ; f05 1 ; f06 1 ; f07 1 ; f08 1 ; f09 1 ; f10 2 ; f11 1 ; f12 1 ; f13 1 ; f14 1 ; f15 1 ; f16 1 ; f17 1 ; f18 1 ; f19 1 ; f20 1 ; f21 1 ; f22 1 ; f23 2 ; f24 1 ; f25 1 ; f26 1 ; f27 1 ; f28 1 ; e29 1 ; e30 1 ; e31 1 ; e32 1 ; e33 1 ; e34 2 ; e35 1 ; e36 1 ; e37 1 ; e38 1 ; e39 1 ; e40 1 ; e41 1 ; e
… [70 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && python3 - <<'PY'\nimport sys\nsys.path.insert(0,'/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools')\nsys.path.insert(0,'.')\nimport bloc_linguistique as bl\nfrom phrases import PHRASES\nh=bl.Heuristique()\nfor pid in ('f10','e34','x44','x46'):\n    p=nex … [379 caractères tronqués]`

  ```
### f10 "M. Dupont, le directeur de l'usine, a annoncé hier qu'il prendrait sa retraite à la fin de l'année, etc."
[(0, 104, '"M. Dupont, le directeur de l\'usine, a annoncé hier qu\'il prendrait sa retraite à la fin de l\'année, etc."'), (2, 104, '" Dupont, le directeur de l\'usine, a annoncé hier qu\'il prendrait sa retraite à la fin de l\'année, etc."')]
mots [(1, 2, '.', 'ponctuation'), (9, 10, ',', 'ponctuation'), (34, 35, ',', 'ponctuation'), (98, 99, ',', 'ponctuation'), (103, 104, '.', 'ponctuation')]
### e34 'The prices rose by 12.5% between January and March 2024, three points more than expected.'
[(0, 22, "'The prices rose by 12.'"), (22, 89, "'5% between January and March 2024, three points more than expected.'")]
mots [(19, 21, '12', 'nombre'), (21, 22, '.', 'ponctuation'), (22, 23, '5', 'nombre'), (23, 24, '%', 'ponctuation'), (51, 55, '2024', 'nombre'), (55, 56, ',', 'ponctuation'), (88, 89, '.', 'ponctuation')]
### x44 'rdv demain 9h pr le budget, faut valider les chiffres avt 18h!! merci :)'
[(0, 63, "'rdv demain 9h pr le budget, faut valider les chiffres avt 18h!!'"), (63, 72, "' merci :)'")]
mots [(11, 13, '9h', 'nombre'), (26, 27, ',', 'ponctuation'), (58, 61, '
… [808 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && python3 - <<'PY'\nimport sys\nsys.path.insert(0,'/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools')\nsys.path.insert(0,'.')\nimport bloc_linguistique as bl\nfrom phrases import PHRASES, CAS_LIMITES\nh=bl.Heuristique()\ndef spans(t):\n    a=h.analyser(t); … [1294 caractères tronqués]`

  ```
Le Dr. Martin est arrivé hier. Il repart demain.
   [(0, 30, "'Le Dr. Martin est arrivé hier.'"), (6, 30, "' Martin est arrivé hier.'"), (30, 48, "' Il repart demain.'")]
J'ai vu M. Dupont. Il était content.
   [(0, 18, '"J\'ai vu M. Dupont."'), (10, 18, "' Dupont.'"), (18, 36, "' Il était content.'")]
Il a lu l'article etc. Puis il est parti.
   [(0, 41, '"Il a lu l\'article etc. Puis il est parti."'), (22, 41, "' Puis il est parti.'")]
La réunion est à 9 h. Elle dure une heure.
   [(0, 21, "'La réunion est à 9 h.'"), (21, 42, "' Elle dure une heure.'")]
Le prix est de 12.5 euros. C'est cher.
   [(0, 18, "'Le prix est de 12.'"), (18, 26, "'5 euros.'"), (26, 38, '" C\'est cher."')]

### overlaps phrase dans les 50
f10 [((0, 104), (2, 104))] [(0, 104, '"M. Dupont, le directeur de l\'usine, a an"'), (2, 104, '" Dupont, le directeur de l\'usine, a anno"')]
textes avec chevauchement phrase 1

### cas limites phrase overlaps
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('audit.py'); s=p.read_text()\nold='''    # doublons exacts\n    vus = collections.Counter((e.niveau, e.type, e.debut, e.fin, e.valeur) for e in a.etiquettes)'''\nnew='''    # chevauchements de phrases (les type … [1124 caractères tronqués]`

  ```
patched
exit=0
crashes 0 refus 0 vides 0 phrases_anom 34 anom_total 149
{"chevauchement_syntagme": {"n": 132, "exemples": [{"id": "f02", "type": "chevauchement_syntagme", "a": ["GP", 29, 51], "b": ["GP", 29, 60]}, {"id": "f02", "type": "chevauchement_syntagme", "a": ["GP", 29, 60], "b": ["GP", 58, 67]}, {"id": "f02", "type": "chevauchement_syntagme", "a": ["GP", 58, 67], "b": ["GV", 61, 67]}, {"id": "f02", "type": "chevauchement_syntagme", "a": ["GP", 68, 78], "b": ["GV", 68, 78]}, {"id": "f02", "type": "chevauchement_syntagme", "a": ["GV", 80, 96], "b": ["GV", 90, 96]}, {"id": "f02", "type": "chevauchement_syntagme", "a": ["GP", 97, 117], "b": ["GP", 97, 159]}]}, "valeur_hors_span": {"n": 8, "exemples": [{"id": "f11", "type": "valeur_hors_span", "attendu": "TION", "niveau": "morphème", "type_etiquette": "suffixe", "valeur": "tion", "debut": 5, "fin": 9}, {"id": "f11", "type": "valeur_hors_span", "attendu": "PRO", "niveau": "morphème", "type_etiquette": "préfixe", "valeur": "pro", "debut": 15, "fin": 18}, {"id": "f11", "type": "valeur_hors_span", "attendu": "CO", "niveau": "morphème", "type_etiquette": "préfixe", "valeur": "co", "debut": 23, "fin": 25}, {"id": "f11", "type": "valeu
… [252 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && python3 - <<'PY'\nimport sys, random, collections\nsys.path.insert(0,'/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools')\nsys.path.insert(0,'.')\nimport bloc_linguistique as bl\nfrom phrases import PHRASES\nh=bl.Heuristique(); h0=bl.Heuristique(segmenter … [1103 caractères tronqués]`

  ```
### Mock sur entrées refusées
'' mock refus= '' etiq= 0 []
'... !!! ???' mock refus= '' etiq= 4 [('phrase', 'type'), ('pragmatique', 'acte'), ('phrase', 'type'), ('pragmatique', 'acte')]
'   ' mock refus= '' etiq= 0 []

### chunker seul : chevauchements syntagmes
chunker seul paires 0

### contrôle langue : caractères mélangés
fr -> fr 0.333 | 'curlaL a eaéh nttco.r desp '
fr -> fr 0.091 | '  tlprd tecdtea jrdr ee aiésfeneain'
fr -> en 0.235 | 'it rhelq  êo me êntaémia t r s iutu'
fr -> fr 0.222 | 'eotduo ln  elnunhcaeilqereemeuea-es'
en -> de 0.5 | 'ho    shoenwamoefres cTltpta .er'
en -> it 0.429 | 'g.ipyat a  htd una,eumy e  tiohepdl'
en -> und 0.0 | 'dt oyd  pi rac r.dr hsyw, ncrhdeans'
en -> en 0.25 | 'twenrsoew oshvgle inemwt tt obpuae '
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && python3 - <<'PY'\nimport sys, collections\nsys.path.insert(0,'/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools')\nsys.path.insert(0,'.')\nimport bloc_linguistique as bl\nfrom phrases import PHRASES\nh=bl.Heuristique(); pos=collections.Counter(); mot=coll … [386 caractères tronqués]`

  ```
pos {'DET': 122, 'NOUN': 365, 'VERB': 32, 'PREP': 103, 'PRON': 65, 'CONJ': 32, 'NUM': 4, 'AUX': 28, 'ADV': 40, 'ADJ': 13, 'MOT': 2} total 806
mot types {'mot': 806, 'ponctuation': 137, 'nombre': 20}
ratio VERB/NOUN 0.08767123287671233
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && time bash tools/porte-bloc-linguistique.sh; echo \"exit=$?\"", "description": "Rejouer la porte du bloc linguistique", "timeoutMs": 600000}`

  ```
=== PORTE BLOC LINGUISTIQUE ===
{
 "langue": {
  "langues_profil": 398,
  "articles_test": 447,
  "accuracy": 0.9687,
  "accuracy_script": 1.0,
  "duree_s": 4.706,
  "langues": {
   "hus": [
    3,
    3
   ],
   "oci": [
    7,
    6
   ],
   "roh": [
    7,
    7
   ],
   "ron": [
    3,
    3
   ]
  }
 },
 "controle_permute": {
  "accuracy": 0.0022,
  "attendu": "proche du hasard"
 },
 "niveaux_vus": [
  "discours",
  "document",
  "graphème",
  "morphème",
  "mot",
  "phrase",
  "pos",
  "pragmatique",
  "syntagme"
 ],
 "niveaux_manquants": [],
 "controles": {
  "vide_refus": "vide",
  "ponctuation_refus": "vide",
  "langue_inconnue": "und",
  "indice_faux": "und",
  "rejeu_identique": true
 },
 "verdicts": {
  "langue": true,
  "script": true,
  "permute_faible": true,
  "niveaux": true,
  "substitution": true,
  "parallele": true,
  "activation": true,
  "vide": true,
  "inconnue": true,
  "rejeu": true
 },
 "ok": true
}
✅ porte bloc linguistique verte
exit=0
[stderr]
................
----------------------------------------------------------------------
Ran 16 tests in 0.063s

OK

real	0m16,022s
user	0m15,829s
sys	0m0,192s
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && python3 - <<'PY'\nimport json, collections\nd=json.load(open('resultats.json'))\ndet=d['robustesse_50']['detail']\nsans=[]; autres=[]\nfor p in det:\n    ts={a['type'] for a in p.get('anomalies',[])}\n    if not ts: sans.append(p['id'])\n    elif ts-{'chevauc … [719 caractères tronqués]`

  ```
sans anomalie 16 ['f01', 'e29', 'e30', 'e31', 'e32', 'e33', 'e34', 'e36', 'e37', 'e38', 'e39', 'e40', 'e41', 'e42', 'x47', 'x48']
anomalies hors chevauchement syntagme [('f07', ['acte_hors_candidats']), ('f09', ['candidat_doublon']), ('f10', ['chevauchement_phrase']), ('f11', ['valeur_hors_span']), ('f14', ['valeur_hors_span']), ('f16', ['valeur_hors_span']), ('f23', ['candidat_doublon']), ('f26', ['acte_hors_candidats']), ('e35', ['candidat_doublon']), ('x44', ['acte_hors_candidats']), ('x46', ['valeur_hors_span']), ('x49', ['acte_hors_candidats'])]
anomalies totales detail 149
absent f01 ['morphème'] fr 6
absent f03 ['morphème'] fr 18
absent f07 ['morphème'] fr 13
absent f22 ['morphème'] fr 16
absent e29 ['morphème'] en 7
absent e33 ['morphème'] en 12
absent e35 ['morphème'] en 16
absent x47 ['morphème', 'syntagme'] und 13
absent x48 ['morphème', 'syntagme'] und 1
categories Counter({'fr': 29, 'en': 14, 'url+email': 1, 'sms': 1, 'sans-ponctuation-finale': 1, 'markdown': 1, 'cyrillique': 1, 'sinogrammes': 1, 'emoji': 1})
mots total 819 labels total 4320
attachments total 265
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && python3 - <<'PY'\nimport sys\nsys.path.insert(0,'/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools')\nsys.path.insert(0,'.')\nimport bloc_linguistique as bl\nfrom phrases import PHRASES\nh=bl.Heuristique()\nfor p in PHRASES:\n    a=h.analyser(p['texte'])\ … [465 caractères tronqués]`

  ```
f03 ['mots:livre']
f05 ['guillemets']
f14 ['mots:temps']
f15 ['mots:point']
e34 ['mots:point']
x43 ['ou']
x45 ['mots:temps']
x46 ['mots:note']
x50 ['mots:livre']
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && python3 - <<'PY'\nimport sys, collections\nsys.path.insert(0,'/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools')\nsys.path.insert(0,'.')\nimport bloc_linguistique as bl\nfrom phrases import PHRASES\nh=bl.Heuristique(); amb=0; tot=0; ex=[]\nfor p in PHRAS … [591 caractères tronqués]`

  ```
attachements 265 cible ambiguë (mot répété) 3 0.0113 ex [('x43', 'example', 2), ('x43', 'example', 2), ('x43', 'example', 2)]
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && python3 - <<'PY'\nimport sys, json\nRACINE='/home/stephane/Data13TB/stephane/GitHub/Qtrinet'\nsys.path.insert(0, RACINE); sys.path.insert(0, RACINE+'/tools')\nimport bloc_linguistique as bl\nfrom tools.tests.linguistique import evaluer_gold as eg, gold_split  … [565 caractères tronqués]`

  ```
split 422 190 {'phrases': 612, 'cibles': 239, 'sources': {'hand': 20, 'reel': 432, 'synthetique': 160}, 'langues': {'fr': 402, 'en': 210}} {'phrases': 422, 'cibles': 163, 'sources': {'hand': 15, 'reel': 302, 'synthetique': 105}, 'langues': {'fr': 277, 'en': 145}} {'phrases': 190, 'cibles': 76, 'sources': {'hand': 5, 'reel': 130, 'synthetique': 55}, 'langues': {'fr': 125, 'en': 65}}
dev phrases 422 POS 0.7547 F1 0.582 exact 153 labels 153 couverture 0.9387 spans 10
test phrases 190 POS 0.7656 F1 0.5914 exact 69 labels 69 couverture 0.9079 spans 7
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && python3 - <<'PY'\nimport json\nd=json.load(open('resultats.json'))\nfor c in d['cas_limites']['cas']:\n    if c['nom']=='surrogate': print(json.dumps(c,ensure_ascii=False,indent=1))\nprint(json.dumps(d['cas_limites']['hors_type'],ensure_ascii=False,indent=1)) … [65 caractères tronqués]`

  ```
{
 "nom": "surrogate",
 "n_chars": 4,
 "crash": true,
 "traceback": "UnicodeEncodeError: 'utf-8' codec can't encode character '\\ud800' in position 0: surrogates not allowed"
}
[
 {
  "nom": "None",
  "crash": false,
  "exception": "",
  "refus": "vide"
 },
 {
  "nom": "bytes",
  "crash": true,
  "exception": "AttributeError: 'int' object has no attribute 'isalpha'",
  "refus": null
 },
 {
  "nom": "int",
  "crash": true,
  "exception": "AttributeError: 'int' object has no attribute 'strip'",
  "refus": null
 },
 {
  "nom": "liste",
  "crash": true,
  "exception": "AttributeError: 'list' object has no attribute 'strip'",
  "refus": null
 }
]
  ```

- **write** `{"content": "# -*- coding: utf-8 -*-\n\"\"\"Mesures complémentaires de l'audit produit (langue, attachements, dédup, contrôles).\"\"\"\nfrom __future__ import annotations\n\nimport collections\nimport copy\nimport json\nimport pathlib\nimport random\nimport re\nimport sys\n\nRACINE = pathlib.Path(\" … [12732 caractères tronqués]`

  ```
<path>/tmp/audit_produit_bl/extra.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && time python3 extra.py > extra_stdout.txt 2> extra_stderr.txt; echo \"exit=$?\"; tail -30 extra_stdout.txt; echo \"---stderr---\"; tail -20 extra_stderr.txt", "description": "Exécuter les mesures complémentaires", "timeoutMs": 900000}`

  ```
exit=0
   "confiance": 0.2222
  },
  {
   "id": "e29",
   "origine": "en",
   "melange": "de",
   "confiance": 0.5
  },
  {
   "id": "e30",
   "origine": "en",
   "melange": "it",
   "confiance": 0.4286
  },
  {
   "id": "e31",
   "origine": "en",
   "melange": "und",
   "confiance": 0.0
  },
  {
   "id": "e39",
   "origine": "en",
   "melange": "en",
   "confiance": 0.25
  }
 ]
}
langue_profils 50/50 39/50 2/50
dedupe_gold {"avant": {"f1": 0.5849, "precision": 0.6292, "rappel": 0.5464, "tp": 1018, "fp": 600, "fn": 845, "tete": 0.7336, "att_exact": 222, "att_cibles": 239, "att_labels": 222, "couverture": 0.9289, "labels": 17847, "attachements": 946}, "apres": {"f1": 0.6141, "precision": 0.7283, "rappel": 0.5309, "tp": 989, "fp": 369, "fn": 874, "tete": 0.7432, "att_exact": 208, "att_cibles": 239, "att_labels": 208, "couverture": 0.8703, "labels": 17587, "attachements": 812}}
---stderr---
[stderr]

real	0m2,986s
user	0m2,926s
sys	0m0,059s
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && python3 - <<'PY'\nimport json, collections\ne=json.load(open('extra.json'))\nlp=e['langue_profils']\nprint(lp['sans_profils'],lp['avec_profils'],lp['avec_profils_egalite_stricte'])\nc=collections.Counter((d['attendu'],d['avec_profils'],d['avec_profils_mappe'] … [646 caractères tronqués]`

  ```
50/50 39/50 2/50
('en', 'eng', 'en') 7
('en', 'pcm', 'pcm') 1
('en', 'sco', 'sco') 3
('en', 'und', 'und') 3
('fr', 'fra', 'fr') 28
('fr', 'hns', 'hns') 1
('fr', 'oci', 'fr') 2
('fr', 'und', 'und') 3
('und', 'und', 'und') 2

non corrects:
{'id': 'f01', 'attendu': 'fr', 'sans_profils': 'fr', 'avec_profils': 'hns', 'avec_profils_mappe': 'hns'}
{'id': 'f03', 'attendu': 'fr', 'sans_profils': 'fr', 'avec_profils': 'und', 'avec_profils_mappe': 'und'}
{'id': 'f23', 'attendu': 'fr', 'sans_profils': 'fr', 'avec_profils': 'und', 'avec_profils_mappe': 'und'}
{'id': 'e29', 'attendu': 'en', 'sans_profils': 'en', 'avec_profils': 'sco', 'avec_profils_mappe': 'sco'}
{'id': 'e32', 'attendu': 'en', 'sans_profils': 'en', 'avec_profils': 'und', 'avec_profils_mappe': 'und'}
{'id': 'e35', 'attendu': 'en', 'sans_profils': 'en', 'avec_profils': 'sco', 'avec_profils_mappe': 'sco'}
{'id': 'e36', 'attendu': 'en', 'sans_profils': 'en', 'avec_profils': 'und', 'avec_profils_mappe': 'und'}
{'id': 'e37', 'attendu': 'en', 'sans_profils': 'en', 'avec_profils': 'pcm', 'avec_profils_mappe': 'pcm'}
{'id': 'e40', 'attendu': 'en', 'sans_profils': 'en', 'avec_profils': 'und', 'avec_profils_mappe': 'und'}
{'id': 'e42', 'at
… [2955 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && python3 - <<'PY'\nimport sys,random\nsys.path.insert(0,'/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools')\nsys.path.insert(0,'.')\nimport bloc_linguistique as bl\nfrom phrases import PHRASES\nh=bl.Heuristique(); rng=random.Random(0); non=0; res=[]\nfor  … [434 caractères tronqués]`

  ```
[('f01', 'fr', 0.333, 'fr'), ('f02', 'fr', 0.091, 'und'), ('f03', 'en', 0.235, 'en'), ('f20', 'fr', 0.222, 'fr'), ('e29', 'de', 0.5, 'de'), ('e30', 'it', 0.429, 'it'), ('e31', 'und', 0.0, 'und'), ('e39', 'en', 0.25, 'en')] non-und au niveau bloc 6 /8
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for f in reports/rapport-produit-bloc-l.md reports/pensee-produit-bloc-l.json; do if [ -e \"$f\" ]; then echo \"EXISTE $f\"; else echo \"neuf $f\"; fi; done", "description": "Vérifier que les deux fichiers sont neufs"}`

  ```
neuf reports/rapport-produit-bloc-l.md
neuf reports/pensee-produit-bloc-l.json
  ```

### 🤖 Assistant

⏵ Construction du JSON de fiche à partir des mesures brutes

- **write** `{"content": "# -*- coding: utf-8 -*-\n\"\"\"Construit reports/pensee-produit-bloc-l.json à partir des mesures de /tmp.\"\"\"\nfrom __future__ import annotations\n\nimport collections\nimport json\nimport pathlib\nimport sys\n\nRACINE = pathlib.Path(\"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\" … [32180 caractères tronqués]`

  ```
<path>/tmp/audit_produit_bl/construire_json.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('construire_json.py'); s=p.read_text()\ns=s.replace('''    \"niveaux\": list(__import__(\"bloc_linguistique\").NIVEAUX) if False else\n                [\"graphème\", \"morphème\", \"mot\", \"pos\", \"syntagme\" … [617 caractères tronqués]`

  ```
clean
[stderr]
Traceback (most recent call last):
  File "/tmp/audit_produit_bl/construire_json.py", line 41, in <module>
    modes = {nom: mode(nom) for nom in ("heuristique", "mock_neuronal", "parallele", "cascade")}
                  ~~~~^^^^^
  File "/tmp/audit_produit_bl/construire_json.py", line 27, in mode
    h = base["heuristique"][nom]
        ~~~~~~~~~~~~~~~~~~~^^^^^
KeyError: 'heuristique'
[exit code: 1]
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('construire_json.py'); s=p.read_text()\ns=s.replace('    h = base[\"heuristique\"][nom]','    h = base[nom][\"all\"]')\np.write_text(s); print('fix')\nPY\npython3 construire_json.py && python3 -m json.tool /hom … [277 caractères tronqués]`

  ```
fix
écrit /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-produit-bloc-l.json 81273 octets
JSON VALIDE
81273 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-produit-bloc-l.json
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-produit-bloc-l.json'))\nprint('top',list(d))\nprint('gold',d['gold']['exact'],d['gold']['couverture'],d['gold']['f1'],d['gold']['pos'],d['gold']['spans_perdus'],d['gold' … [787 caractères tronqués]`

  ```
top ['rapport', 'ligne', 'branche', 'commit', 'date', 'objet', 'verdict', 'dispositif', 'gold', 'banc_50', 'cas_limites', 'performance', 'contrat', 'compositions', 'correctifs', 'controle_negatif', 'limites', 'fichiers']
gold 222 0.9289 0.5849 0.7581 17 cascade_pos
modes {"heuristique": {"pos": 0.7581, "pos_ferme": 0.9004, "pos_ouvert": 0.6234, "f1": 0.5849, "precision": 0.6292, "rappel": 0.5464, "tete": 0.7336, "couverture": 0.9289, "labels": 222, "exact": 222, "exact_taux_span": 1.0}, "mock_neuronal": {"pos": 0.3454, "pos_ferme": 0.0757, "pos_ouvert": 0.6007, "f1": 0.5763, "precision": 0.72, "rappel": 0.4804, "tete": 0.7418, "couverture": 0.8326, "labels": 199, "exact": 0, "exact_taux_span": 0.0}, "parallele": {"pos": 0.7465, "pos_ferme": 0.9004, "pos_ouvert": 0.6007, "f1": 0.6141, "precision": 0.7283, "rappel": 0.5309, "tete": 0.7432, "couverture": 0.8703, "labels": 208, "exact": 208, "exact_taux_span": 1.0}, "cascade": {"pos": 0.7465, "pos_ferme": 0.9004, "pos_ouvert": 0.6007, "f1": 0.6141, "precision": 0.7283, "rappel": 0.5309, "tete": 0.7432, "couverture": 0.8703, "labels": 208, "exact": 208, "exact_taux_span": 1.0}}
banc 0 0 0 34 149
anom {"chevauchement_syntagme": 132, "che
… [2476 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-produit-bloc-l.json'))\nprint(json.dumps(d['contrat'],ensure_ascii=False,indent=1)[:5000])\nprint('\\nCOMPOSITIONS')\nprint(json.dumps(d['compositions'],ensure_ascii=Fal … [223 caractères tronqués]`

  ```
{
 "cles_annotation": [
  "contexte",
  "cout",
  "etiquettes",
  "fraction_semantique",
  "langue",
  "refus",
  "script",
  "source",
  "texte",
  "trace",
  "unites_semantiques"
 ],
 "cles_etiquette": [
  "candidats",
  "confiance",
  "debut",
  "fin",
  "langue",
  "meta",
  "niveau",
  "script",
  "source",
  "type",
  "valeur"
 ],
 "cles_annotation_stables": true,
 "cles_etiquette_stables": true,
 "niveaux": [
  "graphème",
  "morphème",
  "mot",
  "pos",
  "syntagme",
  "phrase",
  "discours",
  "pragmatique",
  "document"
 ],
 "niveaux_optionnels": {
  "morphème": 9,
  "syntagme": 2
 },
 "types_par_niveau": {
  "graphème": [
   "chiffres",
   "espace",
   "lettres",
   "ponctuation",
   "symbole"
  ],
  "mot": [
   "mot",
   "nombre",
   "ponctuation"
  ],
  "pos": [
   "ADJ",
   "ADV",
   "AUX",
   "CONJ",
   "DET",
   "MOT",
   "NOUN",
   "NUM",
   "PREP",
   "PRON",
   "VERB"
  ],
  "syntagme": [
   "GN",
   "GP",
   "GV",
   "REL",
   "SUB"
  ],
  "discours": [
   "connecteur",
   "paragraphe"
  ],
  "document": [
   "paragraphe",
   "titre"
  ],
  "phrase": [
   "modalité",
   "négation",
   "type"
  ],
  "pragmatique": [
   "acte",
   "double_sens"
  ],
  "morphème": 
… [5347 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('construire_json.py'); s=p.read_text()\ns=s.replace('\"sur_parcours_sur\": [','\"parse_sur\": [')\ns=s.replace('\"cible_close\": 16, \"cible_close_detail\"','\"cible_fermee\": 16, \"cible_fermee_detail\"')\np.w … [419 caractères tronqués]`

  ```
ok
ancien JSON retiré
écrit /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-produit-bloc-l.json 81268 octets
JSON VALIDE
3109:  "parse_sur": [
3133:   "cible_fermee": 16,
3134:   "cible_fermee_detail": {
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('construire_json.py'); s=p.read_text()\nold='''    \"langue_melangee\": {\"non_und\": sum(1 for x in extra[\"langue_melangee\"] if x[\"melange\"] != \"und\"),\n                        \"total\": len(extra[\"lan … [1579 caractères tronqués]`

  ```
patched
écrit /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-produit-bloc-l.json 81485 octets
JSON VALIDE
{
 "non_und_detecter": 7,
 "non_und_bloc": 6,
 "total": 8,
 "detail": [
  {
   "id": "f01",
   "origine": "fr",
   "melange": "fr",
   "confiance": 0.3333,
   "bloc": "fr"
  },
  {
   "id": "f02",
   "origine": "fr",
   "melange": "fr",
   "confiance": 0.0909,
   "bloc": "und"
  },
  {
   "id": "f03",
   "origine": "fr",
   "melange": "en",
   "confiance": 0.2353,
   "bloc": "en"
  },
  {
   "id": "f20",
   "origine": "fr",
   "melange": "fr",
   "confiance": 0.2222,
   "bloc": "fr"
  },
  {
   "id": "e29",
   "origine": "en",
   "melange": "de",
   "confiance": 0.5,
   "bloc": "de"
  },
  {
   "id": "e30",
   "origine": "en",
   "melange": "it",
   "confiance": 0.4286,
   "bloc": "it"
  },
  {
   "id": "e31",
   "origine": "en",
   "melange": "und",
   "confiance": 0.0,
   "bloc": "und"
  },
  {
   "id": "e39",
   "origine": "en",
   "melange": "en",
   "confiance": 0.25,
   "bloc": "en"
  }
 ],
 "lecture": "le détecteur par mots-outils n'est pas un rejeteur de bruit : au niveau du bloc (seuil 0,12), 6/8 textes à caractères mélangés reçoivent une langue, confia
… [18 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Rédaction de la fiche d'audit produit

- **write** `{"content": "# Audit produit du bloc linguistique — 0 plantage sur 50 phrases, 34/50 avec une anomalie de contrat\n\n> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Branche** : `s/v7` ·\n> **Commit mesuré** : `fa1b0c6e` (2026-11-06 09:16) · **Date** : 2026-11-06 ·\n> **Verdict** : ⚠ … [31266 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-produit-bloc-l.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && python3 - <<'PY'\nimport sys\nRACINE='/home/stephane/Data13TB/stephane/GitHub/Qtrinet'\nsys.path.insert(0, RACINE); sys.path.insert(0, RACINE+'/tools')\nimport bloc_linguistique as bl\nfrom tools.tests.linguistique import evaluer_gold as eg\nh=bl.Heuristique( … [445 caractères tronqués]`

  ```
vivant 612 F1 0.5849 P 0.6292 R 0.5464 tete 0.7336 POS 0.7581 couverture 0.9289 labels 222
gele 602 F1 0.5893 P 0.6319 R 0.5522 tete 0.7392 POS 0.7603 couverture 0.9289 labels 222
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('reports/rapport-produit-bloc-l.md')\ns=p.read_text()\ns=s.replace(\"> **Aucun fichier existant modifié ; aucun commit.** Sorties : ce rapport et\",\n            \"> **Aucun fichier ex … [3133 caractères tronqués]`

  ```
ok
6:> **Aucun fichier existant modifié par cet audit ; aucun commit.** Sorties : ce rapport et
56:Le rejeu du 2026-11-06 redonne l'**état fourni** (vivant 612) ; la fiche v12 publie, elle, les
57:valeurs du **gelé 602** pour le F1 et la tête :
65:| F1 syntagmes (vivant 612) | **0,5849** (P 0,6292 ; R 0,5464) |
66:| tête (vivant 612) | **0,7336** |
67:| F1 / tête gelé 602 | **0,5893** (P 0,6319 ; R 0,5522) / **0,7392** ; POS 0,7603 |
72:**Vivant 612 vs gelé 602.** L'exact (222/222) et la couverture (0,9289) sont **identiques** sur
86:**Les quatre modes** (vivant 612). Le mock est le double de contrat, pas un modèle :
308:| **P1-11** | **Petites incohérences de valeurs et de candidats** | **8/134** morphèmes normalisés ; **4/50** actes `exclamation` hors candidats ; **4/50** listes avec doublons | 626-638, 1045-1048, 1078, 1142-1150, 1172-1176, 1199-1203 | **2 h** | faible : casse d'origine, ajouter `exclamation`, dédupliquer |
371:- Les chiffres `222/222`, `0,9289`, `0,5849`, `0,7581`, `17` sont ceux du **vivant 612** au
372:  commit `fa1b0c6e` ; la fiche v12 publie le F1/tête du **gelé 602** (0,5893/0,7392, POS 0,7603).
386:- **Aucun fichier existant modifié par cet audit, aucun c
… [40 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('construire_json.py'); s=p.read_text()\nold='''        \"f1\": 0.5849, \"precision\": 0.6292, \"rappel\": 0.5464, \"tete\": 0.7336,\n        \"pos\": 0.7581, \"pos_ferme\": 0.9004, \"pos_ouvert\": 0.6234,'''\nn … [1055 caractères tronqués]`

  ```
patch
écrit /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-produit-bloc-l.json 81756 octets
JSON VALIDE
{"f1": 0.5893, "precision": 0.6319, "rappel": 0.5522, "tete": 0.7392, "pos": 0.7603, "exact": 222, "couverture": 0.9289, "note": "la fiche v12 publie le gelé pour F1/tête ; l'exact et la couverture sont identiques au vivant"}
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-produit-bloc-l.md", "limit": 220}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-produit-bloc-l.md</path>
<type>file</type>
<content>
1: # Audit produit du bloc linguistique — 0 plantage sur 50 phrases, 34/50 avec une anomalie de contrat
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Branche** : `s/v7` ·
4: > **Commit mesuré** : `fa1b0c6e` (2026-11-06 09:16) · **Date** : 2026-11-06 ·
5: > **Verdict** : ⚠️ **la surface est utilisable en autonomie ; la structure ne l'est pas encore.**
6: > **Aucun fichier existant modifié par cet audit ; aucun commit.** Sorties : ce rapport et
7: > [`pensee-produit-bloc-l.json`](pensee-produit-bloc-l.json).
8: >
9: > **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
10: > [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
11: > [`gold_split.py`](../tools/tests/linguistique/gold_split.py) ; **50 phrases libres** écrites pour
12: > l'audit (textes dans le JSON) ; harnais local non committé dans `/tmp/audit_produit_bl`.
13: > **Porte** : `bash tools/porte-bloc-linguistique.sh` → **verte** (16 tests, autotest UDHR
14: > **0,9687**, profils permutés **0,0022**).
15: 
16: **En une phrase.** Sur 50 phrase
… [14584 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-produit-bloc-l.md", "offset": 220, "limit": 220}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-produit-bloc-l.md</path>
<type>file</type>
<content>
220: - **Déterminisme** : même instance, instances fraîches, graines de hash **0/1/42** → **mêmes
221:   digests** ; `json()` par défaut **exclut `duree_s`** ; `json(avec_duree=True)` ne diffère que par
222:   la durée. Deux textes différents ont des digests différents.
223: 
224: ## 5. Stabilité du contrat
225: 
226: **Ce qui est stable.** `Annotation.json()` a **toujours les 11 mêmes clés** et `Etiquette.json()`
227: les **11 mêmes clés** sur les 50 textes et les quatre modes. Les spans sont dans le texte,
228: `debut <= fin`, **aucun span vide**, `niveau` dans les neuf, `type` non vide, `source` d'étiquette
229: dans `{heuristique, neuronal, humain}`, `confiance` dans [0,1] pour l'heuristique, unités triées
230: et disjointes, fraction recalculable, **0 cible absente**.
231: 
232: **Ce qui peut être vide ou absent.**
233: 
234: | élément | constat sur 50 textes |
235: |---|---|
236: | `etiquettes` | vide seulement sur refus (0/50 ici) |
237: | `unites_semantiques`, `fraction_semantique` | peuvent être vides / 0,0 (pas sur ce banc, mais sur du texte sans clas
… [17194 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && python3 - <<'PY'\nimport json\nd=json.load(open('resultats.json'))\nfor c in d['cas_limites']['cas']:\n    if c['nom'] in ('arabe','hébreu','grec','japonais','coréen','chinois','sinogrammes'):\n        print(c['nom'], 'niveaux=',c.get('niveaux'), 'etiquettes= … [86 caractères tronqués]`

  ```
arabe niveaux= ['discours', 'document', 'graphème', 'mot', 'phrase', 'pos', 'pragmatique'] etiquettes= 27
grec niveaux= ['discours', 'document', 'graphème', 'mot', 'phrase', 'pos', 'pragmatique'] etiquettes= 27
hébreu niveaux= ['discours', 'document', 'graphème', 'mot', 'phrase', 'pos', 'pragmatique'] etiquettes= 27
japonais niveaux= ['discours', 'document', 'graphème', 'mot', 'phrase', 'pos', 'pragmatique'] etiquettes= 14
coréen niveaux= ['discours', 'document', 'graphème', 'mot', 'phrase', 'pos', 'pragmatique'] etiquettes= 29
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('reports/rapport-produit-bloc-l.md')\ns=p.read_text()\n\ns=s.replace(\"\"\"  `MockNeuronal`, `Parallele`, `Cascade` pour les compositions. Les 50 phrases sont passées\n  **une fois** p … [3533 caractères tronqués]`

  ```
ok
156:- **Nombres, dates, URL** : « 12.5 » coupe la phrase en **deux fragments** ; « 12.03.2024 » en
157:  **trois** ; « 12,5 » (virgule) ne coupe pas la phrase mais découpe le nombre en `12`, `,`, `5`.
192:| `bytes`, `int`, `list` | **AttributeError** : `'int' object has no attribute 'isalpha'` (bytes) ; `'int' object has no attribute 'strip'` (int) ; `'list' object has no attribute 'strip'` (liste) |
295:| **P0-2** | **Réparer les frontières de phrase et la tokénisation numérique** (décimaux, dates, URL, emails, abréviations, espace initial) | « 12.5 » coupe une phrase en 2 fragments ; « 12.03.2024 » en 3 ; URL → 3–4 ; `M./Dr./etc.` duplique la phrase (f10 : 0-104 & 2-104) ; 6/60 spans commencent par un espace ; `url`/`emoji` : 0/963 | 550, 553-563, 568-587 (surtout 570, 579) | **0,5–1 j** | faible-moyen : change le nombre de phrases et les actes par phrase ; tests dédiés obligatoires |
344:c'est pour cela qu'elle perd ces 14 spans. Le rouge `cascade_pos` est un **autre** effet (le
397:   initial) et les types `url`/`emoji` morts : une URL crée 3–4 phrases, `12.5` coupe une phrase
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '348,355p' reports/rapport-produit-bloc-l.md", "description": "Vérifier la phrase de déterminisme"}`

  ```
- **Contrôle de langue négatif** : 8 textes à caractères mélangés ; au niveau du bloc (seuil 0,12),
  **6/8 reçoivent quand même une langue** (fr, en, de, it), avec une confiance jusqu'à **0,5**.
  Le détecteur par mots-outils n'est pas un rejeteur de bruit : `und` n'est pas garanti sur du
  charabia. C'est un point à documenter ou à corriger par un seuil/longueur minimale.
- **Déterminisme** : même instance, instances fraîches, graines 0/1/42 → identiques ; deux textes
  différents → digests différents. La seule nondétermination est `duree_s`, exclue par défaut.

## 9. Ce que ce banc ne dit pas — et ce qui pourrait le rendre faux
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('reports/rapport-produit-bloc-l.md'); s=p.read_text()\ns=s.replace(\"\"\"- **Déterminisme** : même instance, instances fraîches, graines 0/1/42 → identiques ; deux textes\n  différents … [528 caractères tronqués]`

  ```
ok
  charabia. C'est un point à documenter ou à corriger par un seuil/longueur minimale.
- **Déterminisme** : même instance, instances fraîches, graines 0/1/42 → identiques ; deux textes
  différents → digests différents. Dans un environnement fixé, la seule nondétermination est
  `duree_s`, exclue par défaut (mais `DEEPSEEK_KEY_FILE` peut changer la politique, § 6).
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short -- tools/ reports/ | head -40 && echo \"--- diff tools ---\" && git diff --stat -- tools/ | tail -5 && echo \"--- fichiers ---\" && ls -l reports/rapport-produit-bloc-l.md reports/pensee-produit-bloc-l.json", "desc … [63 caractères tronqués]`

  ```
M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-spans-chunker.md
 m tools/structures
?? reports/pensee-produit-bloc-l.json
?? reports/rapport-produit-bloc-l.md
?? reports/rapport-s-paragraphes.md
--- diff tools ---
 tools/structures | 0
 1 file changed, 0 insertions(+), 0 deletions(-)
--- fichiers ---
-rw-r--r--. 1 stephane stephane 81756  6 nov 11:05 reports/pensee-produit-bloc-l.json
-rw-------. 1 stephane stephane 33074  6 nov 11:07 reports/rapport-produit-bloc-l.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport re, pathlib\np=pathlib.Path('reports/rapport-produit-bloc-l.md')\ns=p.read_text()\nfor link in re.findall(r'\\]\\(([^)]+)\\)', s):\n    if link.startswith(('http','#')): continue\n    q=(p.parent/link).resolv … [133 caractères tronqués]`

  ```
OK  pensee-produit-bloc-l.json -> /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-produit-bloc-l.json
OK  ../tools/bloc_linguistique.py -> /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py
OK  ../tools/tests/linguistique/evaluer_gold.py -> /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/evaluer_gold.py
OK  ../tools/tests/linguistique/gold_split.py -> /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_split.py
OK  rapport-audit-v10.md -> /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-audit-v10.md
OK  ../tools/bloc_linguistique.py -> /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py
OK  ../tools/bloc_linguistique.py -> /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py
OK  ../tools/tests/linguistique/evaluer_gold.py -> /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/evaluer_gold.py
OK  ../tools/tests/linguistique/gold_split.py -> /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_split.py
OK  pensee-produit-bloc-l.json -> /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/
… [26 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"TODO\\|FIXME\\|XXX\\|PLACEHOLDER\\|lorem\" reports/rapport-produit-bloc-l.md reports/pensee-produit-bloc-l.json || echo \"aucun placeholder\"; echo \"---\"; python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-pr … [519 caractères tronqués]`

  ```
aucun placeholder
---
taille 65459 octets
detail ids 50 premier f01 dernier x50
anomalies detail total 149
cas 25 hors type 4
correctifs 18
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib, re\nlines=pathlib.Path('reports/rapport-produit-bloc-l.md').read_text().splitlines()\n# blocs de tableaux : lignes commençant par |\nbloc=[]\ndef check(bloc):\n    if len(bloc)<2: return []\n    n=[l … [722 caractères tronqués]`

  ```
tableaux déséquilibrés: 0
fences ``` 0
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('construire_json.py'); s=p.read_text()\ns=s.replace('\"parse_sur\": [','\"a_parser_sans_casser\": [')\np.write_text(s); print('ok')\nPY\nDEST=/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-produ … [274 caractères tronqués]`

  ```
ok
écrit /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-produit-bloc-l.json 81767 octets
JSON VALIDE
3119:  "a_parser_sans_casser": [
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('reports/rapport-produit-bloc-l.md'); s=p.read_text()\ns=s.replace(\"\"\"- **Débit** : 923 phrases/s à 10 mots, 218/s à 50, 51,5/s à 200. Le mode par défaut est\n  **largement assez ra … [1196 caractères tronqués]`

  ```
ok
67:| F1 / tête gelé 602 | **0,5893** (P 0,6319 ; R 0,5522) / **0,7392** ; POS 0,7603 |
75:publie les valeurs **gelées** (le POS 0,7603 est notre mesure du gelé, pas une valeur de la
211:  composante superlinéaire commence à se voir.
377:  commit `fa1b0c6e` ; la fiche v12 publie le F1/tête du **gelé 602** (0,5893/0,7392, POS 0,7603).
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '168,176p' reports/rapport-produit-bloc-l.md", "description": "Vérifier la phrase des profils de langue"}`

  ```
`meta.attachement` ne porte **pas l'offset de la cible**, seulement sa chaîne.
- **Double sens** : **9/50** phrases déclenchent `double_sens` (candidat à 0,25) : `livre` 2,
  `temps` 2, `point` 2, `note` 1, ` ou ` 1, guillemets 1. C'est du rappel, pas de la précision.
- **Langue** : défaut **50/50** (34 fr, 14 en, 2 `und`). Avec les **profils UDHR** : **39/50**
  après conversion ISO3→ISO2 (30/34 fr, 7/14 en, 2/2 `und` ; `oci` compté comme fr,
  `hns`/`sco`/`pcm` non), et **2/50** en égalité stricte de chaîne (les deux `und`). Exemples : f01 fr→`hns`, e29/e35/e42 en→`sco`, e37 en→`pcm`, f03/f23/
  x44 fr→`und`, e32/e36/e40 en→`und`. L'indice de langue `"fr"` est **ignoré** quand les profils
  sont chargés (les clés sont en ISO3).
- **Scripts non latins** : russe et chinois rendent graphème/mot/phrase/document, **0 syntagme**,
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"parse_sur\\|sur_parcours\\|cible_close\" reports/pensee-produit-bloc-l.json || echo \"aucune clé obsolète\"; python3 -m json.tool reports/pensee-produit-bloc-l.json > /dev/null && echo \"JSON OK\"", "description": "Vérifier … [24 caractères tronqués]`

  ```
aucune clé obsolète
JSON OK
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json, collections\nd=json.load(open('reports/pensee-produit-bloc-l.json'))\nb=d['banc_50']\nprint('gold', d['gold']['exact'], d['gold']['labels'], d['gold']['couverture'], d['gold']['f1'], d['gold']['pos'], d … [1436 caractères tronqués]`

  ```
gold 222 222 0.9289 0.5849 0.7581 17 0.5893 0.7392
banc {'labels': 60, 'textes_multi': 6, 'commencent_par_espace': 6, 'chevauchements': 1, 'exemples': [{'id': 'f10', 'a': [0, 104], 'b': [2, 104]}]} 819 4320 {'total': 265, 'cibles_fermees': 16, 'cibles_fermees_detail': {'au': 3, 'was': 3, 'lui': 2, 'pas': 2, 'have': 2, 'entre': 2, 'ne': 1, 'Tu': 1}, 'cible_absente': 0, 'cible_non_token': 0, 'segment_mismatch': 0, 'cible_ambigue': 3, 'offset_cible': False} 0 0 0 34 149
langues {'fr': 34, 'en': 14, 'und': 2} scripts {'Latn': 48, 'Cyrl': 1, 'Hani': 1}
fraction {'min': 0.3529, 'mediane': 0.5493, 'max': 0.875, 'doc': '0,51–0,76 sur 5 échantillons : la plage ne tient pas sur 50 phrases libres'}
pos 806 963 157 {'NOUN': 365, 'VERB': 32, 'DET': 122, 'PREP': 103, 'PRON': 65, 'CONJ': 32, 'ADV': 40, 'AUX': 28, 'ADJ': 13, 'NUM': 4, 'MOT': 2}
att {'total': 265, 'cibles_fermees': 16, 'cibles_fermees_detail': {'au': 3, 'was': 3, 'lui': 2, 'pas': 2, 'have': 2, 'entre': 2, 'ne': 1, 'Tu': 1}, 'cible_absente': 0, 'cible_non_token': 0, 'segment_mismatch': 0, 'cible_ambigue': 3, 'offset_cible': False}
doc {'labels': 53, 'tronques': 42, 'titres': 2, 'titres_faux_50': [{'id': 'x48', 'valeur': '今天天气很好，我们去公
… [859 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json, collections\nd=json.load(open('reports/pensee-produit-bloc-l.json'))\nprint('dedupe', json.dumps(d['controle_negatif']['dedupe_simulation'],ensure_ascii=False))\nprint('correctifs', collections.Counter( … [275 caractères tronqués]`

  ```
dedupe {"banc_50": {"paires_avant": 132, "paires_apres": 0, "textes": 31, "syntagmes_avant": 362, "syntagmes_apres": 292, "attachements_avant": 265, "attachements_apres": 215}, "gold": {"avant": {"f1": 0.5849, "precision": 0.6292, "rappel": 0.5464, "tp": 1018, "fp": 600, "fn": 845, "tete": 0.7336, "att_exact": 222, "att_cibles": 239, "att_labels": 222, "couverture": 0.9289, "labels": 17847, "attachements": 946}, "apres": {"f1": 0.6141, "precision": 0.7283, "rappel": 0.5309, "tp": 989, "fp": 369, "fn": 874, "tete": 0.7432, "att_exact": 208, "att_cibles": 239, "att_labels": 208, "couverture": 0.8703, "labels": 17587, "attachements": 812}}}
correctifs Counter({'important': 10, 'bloquant': 5, 'confort': 3})
cas 25 1
detail first {'id': 'f01', 'cat': 'fr/courte', 'texte': 'Le chat dort sur le canapé.', 'attendu': 'fr', 'langue': 'fr', 'script': 'Latn', 'mots': 6, 'etiquettes': 32, 'niveaux': {'graphème': 12, 'mot': 7, 'pos': 6, 'syntagme': 3, 'discours': 1, 'document': 1, 'phrase': 1, 'pragmatique': 1}, 'niveaux_absents': ['morphème'], 'fraction': 0.5185, 'attachements': 3, 'anomalies': [], 'anomalies_n': 0}
detail last {'id': 'x50', 'cat': 'fr/très-longue', 'texte': "Dans le petit vill
… [817 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('construire_json.py'); s=p.read_text()\ns=s.replace('        \"phrases\": extra[\"phrases\"],','        \"phrases_stats\": extra[\"phrases\"],')\np.write_text(s); print('ok')\nPY\nDEST=/home/stephane/Data13TB/s … [314 caractères tronqués]`

  ```
ok
écrit /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-produit-bloc-l.json 81790 octets
JSON VALIDE
307:  "phrases_stats": {
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"HEAD: $(git rev-parse --short HEAD)\" && git status --short -- reports/rapport-produit-bloc-l.md reports/pensee-produit-bloc-l.json && wc -l -c reports/rapport-produit-bloc-l.md reports/pensee-produit-bloc-l.json && python3 -  … [557 caractères tronqués]`

  ```
HEAD: 6ef2a3f5
?? reports/pensee-produit-bloc-l.json
?? reports/rapport-produit-bloc-l.md
   410  33260 reports/rapport-produit-bloc-l.md
  3636  81790 reports/pensee-produit-bloc-l.json
  4046 115050 total
reports/rapport-produit-bloc-l.md utf8 OK sans BOM
reports/pensee-produit-bloc-l.json utf8 OK sans BOM
JSON chargé OK
d657837c40f818dcd544a1cb7358bbd9230e36ce604eb439f06963a49b0971ab  reports/rapport-produit-bloc-l.md
abd5774159593f74568693eec1cf8d37b829b0940c88eadb7541b5d94848af84  reports/pensee-produit-bloc-l.json
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -6 --decorate && echo \"--- diff module fa1b0c6e..HEAD ---\" && git diff --stat fa1b0c6e..HEAD -- tools/bloc_linguistique.py tools/tests/linguistique/evaluer_gold.py tools/tests/linguistique/gold_split.py && echo \" … [166 caractères tronqués]`

  ```
6ef2a3f5 (HEAD -> s/v7, origin/s/v7, origin/master, origin/HEAD, master) JOURNAL ET ROADMAP — LA VAGUE PRODUIT : DRAVE V0 DOCUMENTÉ, PORTE PRODUIT VERTE, AUTOTEST ×2,4, MASTER POUSSÉ (7f73c17f)
7f73c17f PRODUIT — LA DOC D'USAGE ET LES 5 EXEMPLES VÉRIFIÉS (5/5 REJOUÉS) ; CASCADE_POS N'EST PLUS UNE ROUGE (PLANCHER 0,70)
f6c8132b A23 — LES 6 CORRECTIONS FACTUELLES DE LA FILE (GOLD 200+ = 13 OCCURRENCES, PASSES 2 H 11 À 2 H 29) ; T0 DANS LE BUDGET
fba3072a ÉTAT — T0 DANS LE BUDGET APRÈS LA FILE DES TÂCHES
266b1833 ROADMAP — LA LIGNE S CORRIGÉE (150 VERDICTS HUMAINS, 19 SUR LES PARAGRAPHES) ; LA FILE DES 29 TÂCHES INTÉGRÉE (8 AUTONOMES)
b2196cc7 PILOTAGE — LE PREMIER PRODUIT EST DEBOUT : DRAVE, PORTE PRODUIT, DOC D'USAGE ; 84 PORTES, 3 ROUGES
--- diff module fa1b0c6e..HEAD ---
 tools/tests/linguistique/evaluer_gold.py | 5 ++++-
 1 file changed, 4 insertions(+), 1 deletion(-)
--- status module ---
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff --stat fa1b0c6e..HEAD | tail -20", "description": "Voir les fichiers modifiés depuis le commit mesuré"}`

  ```
.../a0d33fb7-37a9-4834-8a94-0da119e3b18f/digest.md | 3369 +++++++++++++++
 .../rapport.md                                     |  205 +
 .../bd6322ed-6792-4188-9d4c-6cae09c3ef4e/digest.md | 1529 +++++++
 .../rapport.md                                     |  193 +
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md | 1521 +++++++
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md   |    2 +-
 .../rapport.md                                     |  108 +-
 reports/README.md                                  |    6 +-
 reports/pensee-autotest-parallele.json             |   21 +
 reports/pensee-file-taches.json                    |  854 ++++
 reports/pensee-produit-v0.json                     |   26 +
 reports/rapport-autotest-parallele.md              |   52 +
 reports/rapport-file-taches.md                     |  215 +
 reports/rapport-produit-v0.md                      |   66 +
 tools/drave.py                                     |  388 ++
 tools/pensee/autotest.py                           |  385 +-
 tools/porte-produit.sh                             |   50 +
 tools/tests/linguistique/evaluer_gold.py           |    5 +-
 tools/tests/test_produit.py                        |  110 +
 38 fil
… [49 caractères tronqués]
  ```

### 🤖 Assistant

⏵ HEAD a avancé pendant l'audit : vérification de l'impact sur les chiffres

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff fa1b0c6e..HEAD -- tools/tests/linguistique/evaluer_gold.py && echo \"=== log 7f73 ===\" && git show --stat --oneline 7f73c17f | head -20", "description": "Inspecter le changement du harnais et le commit cascade_pos"}`

  ```
diff --git a/tools/tests/linguistique/evaluer_gold.py b/tools/tests/linguistique/evaluer_gold.py
index b25e8677..83350674 100644
--- a/tools/tests/linguistique/evaluer_gold.py
+++ b/tools/tests/linguistique/evaluer_gold.py
@@ -277,7 +277,10 @@ def main() -> int:
         "syntagme_synthetique": h_syn["syntagme"]["f1"] >= 0.15,
         "tete": h_all["syntagme"]["tete"]["f1"] >= 0.35,
         "acte": h_all["pragmatique"]["acte"] >= 0.70,
-        "cascade_pos": c_all["pos"]["exactitude"] >= h_all["pos"]["exactitude"],
+        # la cascade n'est **pas** l'heuristique : le neuronal de contrat (MockNeuronal) ne rend
+        # que les classes ouvertes, donc son POS est structurellement plus bas — le verdict est un
+        # **plancher** (0,70), pas une comparaison à l'heuristique (mesuré : 0,7465 contre 0,7581).
+        "cascade_pos": c_all["pos"]["exactitude"] >= 0.70,
         "cascade_syntagme": c_all["syntagme"]["f1"] >= h_all["syntagme"]["f1"],
         "attachement_topk": h_all["attachement"]["topk_taux"] >= 0.30,
         "attachement_hasard": (h_all["attachement"]["top1_taux"]
=== log 7f73 ===
7f73c17f PRODUIT — LA DOC D'USAGE ET LES 5 EXEMPLES VÉRIFIÉS (5/5 REJOUÉS) ; CASC
… [1240 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline --all -- tools/bloc_linguistique.py | head -8 && echo \"--- diff module fa1b0c6e..HEAD ---\" && git diff --stat fa1b0c6e..HEAD -- tools/bloc_linguistique.py && echo \"(vide = inchangé)\"", "description": "Confirmer  … [30 caractères tronqués]`

  ```
0911ae29 B13 — 222/222 (1,0000) : LE DERNIER MARQUEUR AMBIGU (when APRÈS UN GN), COUVERTURE 0,9289, 17 SPANS TOUS INATTEIGNABLES ; 183/183
653a7981 B13 — LES DEUX DERNIÈRES RÉGRESSIONS (s037, r303) : EXACT 221/221 (1,0000), COUVERTURE 0,9247, 18 SPANS ; AUDIT V10 INTÉGRÉ, V10 CORRIGÉE ; 183/183
710ec7f9 B13 — LE FÉMININ -ÉE ET LA GARDE DÉTERMINANT DU GP : EXACT 220/220 (1,0000), COUVERTURE 0,9205, F1 0,5880, 19 SPANS ; 183/183
160d08ca B13 — LA GARDE PRON : EXACT 219/219 (1,0000), COUVERTURE 0,9163, F1 0,5822, DEV 152/152 ET TEST 67/67 ; AUDIT DE COHÉRENCE V8 INTÉGRÉ ; 183/183
d497324b B13 — TOP-K 211/239 (LE SITE D'APPEL prec = s), LA V8 RÉÉCRITE HONNÊTEMENT (+17 NET, 7 RÉGRESSIONS), AUDITS A17/A19 INTÉGRÉS ; 183/183
f908d7b0 B13 — R1/R2/R3 : EXACT 212/212 (1,0000), COUVERTURE 0,887, F1 0,5763, FR 1,0 / EN 1,0 ; 27 SPANS DONT 17 INATTEIGNABLES ; 183/183
69bd865e B13 — LA COUVERTURE À 0,8201 : POS CONTEXTUEL 0,7603, F1 0,5595, EXACT 195/196 (0,9949), 43 SPANS ; 183/183
0ec6c27d B13 — L'ATTACHEMENT PARFAIT SUR LES SPANS PRÉDITS : 187/187 (1,0000), FR 1,0, EN 1,0, DEV 126/126, TEST 61/61 ; RENDEMENT 0,7824 ; 183/183
--- diff module fa1b0c6e..HEAD ---
(vide = inchangé)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONPATH=. python3 tools/tests/linguistique/evaluer_gold.py --json /tmp/audit_produit_bl/eval_head.json > /tmp/audit_produit_bl/eval_head.out 2>&1; echo \"exit=$?\"; tail -12 /tmp/audit_produit_bl/eval_head.out; python3 - <<'PY'\ni … [470 caractères tronqués]`

  ```
exit=0
      "labels": 86,
      "exact": 86,
      "topk": 86,
      "exact_taux_span": 1.0
     }
    }
   },
   "attachement_tete": {
    "cibles": 208,
    "labels": 208,
    "top1"
heuristique all: {"pos": {"exactitude": 0.7581, "exactitude_ferme": 0.9004, "exactitude_ouvert": 0.6234, "tokens": 3179, "confusions": {"ADJ": {"ADJ": 50, "NOUN": 80, "VERB": 4}, "ADV": {"ADV": 117, "NOUN": 20, "PREP": 2, "ADJ": 1, "?": 1}, "AUX": {"PREP": 4, "AUX": 118, "?": 3, "NOUN": 3}, "CONJ": {"CONJ": 44, "PRON": 25, "DET": 12, "?": 13, "PREP": 2, "NOUN": 2}, "DET": {"DET": 586, "?": 2}, "NOUN": {"NOUN": 657, "ADJ": 17, "VERB": 7, "?": 1}, "NUM": {"NUM": 2}, "PONCT": {"?": 25}, "PREP": {"PREP": 114}, "PRON": {"PRON": 411, "NOUN": 8, "?": 30, "DET": 25, "CONJ": 1}, "VERB": {"VERB": 311, "NOUN": 450, "ADJ": 5, "PREP": 2, "?": 16, "AUX": 7, "ADV": 1}}}, "syntagme": {"precision": 0.6292, "rappel": 0.5464, "f1": 0.5849, "tp": 1018, "fp": 600, "fn": 845, "tete": {"precision": 0.81, "rappel": 0.6704, "f1": 0.7336, "tp": 1249, "fp": 293, "fn": 614}}, "pragmatique": {"acte": 0.9967, "negation": 0.9771, "modalite": 0.9886, "double_sens": 0.9444}, "fraction_semantique": 0.5537}
ok True
verdict cascade_po
… [69 caractères tronqués]
  ```

- **send_message** `{"agent_id": "e181ce02-cd50-488a-a6be-e84b79d40dcc", "message": "Point d'état important (audit produit bloc L, en cours) : HEAD a avancé pendant l'audit, de `fa1b0c6e` à `6ef2a3f5`. Le module `tools/bloc_linguistique.py` est **inchangé** (git diff vide), donc mes mesures restent valides. En revanche … [674 caractères tronqués]`

  ```
message delivered to agent e181ce02-cd50-488a-a6be-e84b79d40dcc
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && python3 - <<'PY'\nimport json\nd=json.load(open('eval_head.json'))\nprint('appels',d['cascade'].get('appels_neuronal'))\nprint('ok',d['ok'],'cascade_pos',d['verdict']['cascade_pos'])\nprint('compare', {k:(d['cascade']['all'][k] if k!='attachement' else d['cas … [127 caractères tronqués]`

  ```
appels 1676
ok True cascade_pos True
compare {'pos': {'exactitude': 0.7465, 'exactitude_ferme': 0.9004, 'exactitude_ouvert': 0.6007, 'tokens': 3179, 'confusions': {'ADJ': {'ADJ': 50, 'NOUN': 80, 'VERB': 4}, 'ADV': {'ADV': 117, 'NOUN': 20, 'PREP': 2, 'ADJ': 1, '?': 1}, 'AUX': {'PREP': 4, 'AUX': 118, '?': 3, 'NOUN': 3}, 'CONJ': {'CONJ': 44, 'PRON': 25, 'DET': 12, '?': 13, 'PREP': 2, 'NOUN': 2}, 'DET': {'DET': 586, '?': 2}, 'NOUN': {'NOUN': 617, 'ADJ': 17, 'VERB': 47, '?': 1}, 'NUM': {'NUM': 2}, 'PONCT': {'?': 25}, 'PREP': {'PREP': 114}, 'PRON': {'PRON': 411, 'NOUN': 8, '?': 30, 'DET': 25, 'CONJ': 1}, 'VERB': {'VERB': 314, 'NOUN': 447, 'ADJ': 5, 'PREP': 2, '?': 16, 'AUX': 7, 'ADV': 1}}}, 'syntagme': {'precision': 0.7283, 'rappel': 0.5309, 'f1': 0.6141, 'tp': 989, 'fp': 369, 'fn': 874, 'tete': {'precision': 0.8814, 'rappel': 0.6425, 'f1': 0.7432, 'tp': 1197, 'fp': 161, 'fn': 666}}}
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('construire_json.py'); s=p.read_text()\n\n# dispositif\nold='''        \"gold\": \"evaluer_gold.charger() + evaluer_bloc ; gold_split.dev/test ; module tools/bloc_linguistique.py au commit fa1b0c6e.\",'''\nnew= … [3470 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 42, in <module>
AssertionError
[exit code: 1]
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && grep -n \"chiffres.*222/222\\|cascade_pos.*rouge\\|P0-4\\|rouge_fa1b0c6e\\|head_au\" construire_json.py | head -20", "description": "Repérer les passages à patcher"}`

  ```
173:    {"id": "P0-4", "severite": "bloquant",
333:        "lecture": "cascade_pos est rouge parce que la fusion mélange le POS du mock (0,3454) ; par ailleurs Parallele et Cascade ont exactement les chiffres de la déduplication simulée (F1 0,6141, 208/208, couverture 0,8703).",
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && grep -n \"vivant 612\\|gelé 602\\|limites\" construire_json.py | head -20 && sed -n '395,430p' construire_json.py", "description": "Lire la section limites du constructeur"}`

  ```
58:# ------------------------------------------------------------------ cas limites
60:for c in raw["cas_limites"]["cas"]:
67:hors_type = raw["cas_limites"]["hors_type"]
204:     "preuve": "42/53 valeurs document font 60 caractères (paragraphe tronqué) ; x48 (chinois) et 4 cas limites (arabe, hébreu, japonais, chiffres) sont étiquetés titre parce que upper() == lower() sur les scripts sans casse.",
301:    "objet": "Audit de fiabilité produit du bloc linguistique : robustesse hors gold (50 phrases libres), performance, stabilité du contrat, cas limites, compositions et liste de correctifs chiffrés.",
302:    "verdict": "⚠️ utilisable en surface (graphème, mot, POS fermées, phrase, document) sur du français/anglais propre ; fragile en structure (syntagmes qui se chevauchent, frontières de phrase, compositions, langue). 0 plantage sur 50 phrases, mais 34/50 avec au moins une anomalie de contrat et 1 plantage sur 25 cas limites.",
394:    "cas_limites": {
420:    "limites": [
        "total": len(cas), "crashes": sum(1 for x in cas if x["crash"]),
        "cas": cas, "hors_type": hors_type,
        "lecture": "un seul plantage textuel : un surrogate isolé (UnicodeEncodeError à len(tex
… [2543 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('construire_json.py'); s=p.read_text()\n\nold='''        \"gold\": \"evaluer_gold.charger() + evaluer_bloc ; gold_split.dev/test ; module tools/bloc_linguistique.py au commit fa1b0c6e.\",'''\nnew='''        \"g … [3844 caractères tronqués]`

  ```
patched
écrit /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-produit-bloc-l.json 82851 octets
JSON VALIDE
{
 "rouge_fa1b0c6e": "cascade_pos",
 "verdict_cascade_pos_fa1b0c6e": false,
 "ok_fa1b0c6e": false,
 "verdict_cascade_pos_head": true,
 "ok_head": true,
 "note_verdict": "À HEAD (7f73c17f), evaluer_gold remplace la comparaison par un plancher 0,70 : cascade_pos passe à vrai et ok à vrai, sans changement du module ni des valeurs. La baisse de POS de la composition (0,7465 contre 0,7581) reste mesurée."
}
6ef2a3f5 7f73c17f : cascade_pos >= 0,70 au lieu de cascade >= heuristique
Le verdict cascade_pos a changé à HEAD (7f73c17f : plancher 0,70 au lieu de la comparaison à l'heuristique) : ok passe de faux à vrai sans changement du module ni des valeurs. Le rouge de l'état fourni est éteint par le harnais, pas par un correctif ; la baisse de POS de la composition reste mesurée (0,7465 contre 0,7581).
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('reports/rapport-produit-bloc-l.md'); s=p.read_text()\n\ns=s.replace(\"\"\"> **Commit mesuré** : `fa1b0c6e` (2026-11-06 09:16) · **Date** : 2026-11-06 ·\"\"\",\n\"\"\"> **Commit mesuré … [3808 caractères tronqués]`

  ```
ok
4:> **Commit mesuré** : `fa1b0c6e` (2026-11-06 09:16) · **HEAD pendant la rédaction** : `6ef2a3f5`
35:| compositions | ❌ | refus et contexte perdus, cascade **50/50** appels ; POS **0,7465 < 0,7581** (verdict `cascade_pos` vert à HEAD par plancher 0,70, pas par correctif) |
99:- **`cascade_pos` : rouge à `fa1b0c6e`, vert à HEAD par plancher.** À `fa1b0c6e`, le verdict
109:- **`ok`** : **faux à `fa1b0c6e`** (à cause de `cascade_pos`) ; **vrai à HEAD** (plancher 0,70),
387:- **Le verdict `cascade_pos` a changé à HEAD** (`7f73c17f` : plancher 0,70 au lieu de la
388:  comparaison à l'heuristique) : `ok` passe de faux à vrai **sans** changement du module ni des
418:   `cascade_pos` est vert à HEAD par plancher, pas par correction du comportement.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-produit-bloc-l.json'))\nprint(json.dumps(d['gold'],ensure_ascii=False,indent=1)[:2200])\nPY", "description": "Vérifier la section gold du JSON"}`

  ```
{
 "phrases": 612,
 "cibles": 239,
 "tokens": 3179,
 "sources": {
  "hand": 20,
  "reel": 432,
  "synthetique": 160
 },
 "langues": {
  "fr": 402,
  "en": 210
 },
 "exact": 222,
 "labels": 222,
 "exact_taux": 1.0,
 "couverture": 0.9289,
 "spans_perdus": 17,
 "f1": 0.5849,
 "precision": 0.6292,
 "rappel": 0.5464,
 "tete": 0.7336,
 "pos": 0.7581,
 "pos_ferme": 0.9004,
 "pos_ouvert": 0.6234,
 "gele_602": {
  "f1": 0.5893,
  "precision": 0.6319,
  "rappel": 0.5522,
  "tete": 0.7392,
  "pos": 0.7603,
  "exact": 222,
  "couverture": 0.9289,
  "note": "la fiche v12 publie le gelé pour F1/tête ; l'exact et la couverture sont identiques au vivant"
 },
 "pragmatique": {
  "acte": 0.9967,
  "negation": 0.9771,
  "modalite": 0.9886,
  "double_sens": 0.9444
 },
 "fraction_semantique": 0.5537,
 "dev": {
  "phrases": 422,
  "cibles": 163,
  "exact": 153,
  "labels": 153,
  "couverture": 0.9387,
  "spans": 10,
  "pos": 0.7547,
  "f1": 0.582
 },
 "test": {
  "phrases": 190,
  "cibles": 76,
  "exact": 69,
  "labels": 69,
  "couverture": 0.9079,
  "spans": 7,
  "pos": 0.7656,
  "f1": 0.5914
 },
 "modes": {
  "heuristique": {
   "pos": 0.7581,
   "pos_ferme": 0.9004,
   "pos_ouvert": 0.6234,
   "f1": 
… [1000 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-produit-bloc-l.json'))\nfor k in ('rouge_fa1b0c6e','verdict_cascade_pos_fa1b0c6e','ok_fa1b0c6e','verdict_cascade_pos_head','ok_head','note_verdict','lecture'):\n    prin … [210 caractères tronqués]`

  ```
rouge_fa1b0c6e : cascade_pos
verdict_cascade_pos_fa1b0c6e : False
ok_fa1b0c6e : False
verdict_cascade_pos_head : True
ok_head : True
note_verdict : À HEAD (7f73c17f), evaluer_gold remplace la comparaison par un plancher 0,70 : cascade_pos passe à vrai et ok à vrai, sans changement du module ni des valeurs. La baisse de POS de la composition (0,7465 contre 0,7581) reste mesurée.
lecture : La fusion mélange le POS du mock (0,3454) : cascade/parallele ont 0,7465 de POS, 0,5849→0,6141 de F1, 208/208 exacts et 0,8703 de couverture — exactement les chiffres de la déduplication simulée. Le vert de cascade_pos à HEAD est un choix de seuil, pas un correctif.
dispositif head: 6ef2a3f5
limites n 8
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && head -8 tools/porte-bloc-linguistique.sh && bash tools/porte-bloc-linguistique.sh > /tmp/audit_produit_bl/porte_head.out 2>&1; echo \"exit=$?\"; tail -8 /tmp/audit_produit_bl/porte_head.out", "description": "Rejouer la porte du bloc  … [38 caractères tronqués]`

  ```
#!/usr/bin/env bash
# Porte du bloc linguistique — tests de contrat + mesure UDHR (langue/script).
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
echo "=== PORTE BLOC LINGUISTIQUE ==="
python3 -m unittest discover -s tools/tests/linguistique -p 'test_bloc_linguistique.py' || { echo "❌ tests"; exit 1; }
python3 tools/bloc_linguistique.py --autotest --udhr data/udhr/articles.jsonl --sortie /tmp/bloc-linguistique-porte.json || { echo "❌ autotest"; exit 1; }
exit=0
  "activation": true,
  "vide": true,
  "inconnue": true,
  "rejeu": true
 },
 "ok": true
}
✅ porte bloc linguistique verte
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,45p' reports/rapport-produit-bloc-l.md && echo \"==== §2 ====\" && sed -n '56,120p' reports/rapport-produit-bloc-l.md", "description": "Relire l'en-tête et la section gold après mise à jour"}`

  ```
# Audit produit du bloc linguistique — 0 plantage sur 50 phrases, 34/50 avec une anomalie de contrat

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Branche** : `s/v7` ·
> **Commit mesuré** : `fa1b0c6e` (2026-11-06 09:16) · **HEAD pendant la rédaction** : `6ef2a3f5`
> (module `bloc_linguistique.py` inchangé ; `evaluer_gold.py` modifié en `7f73c17f`) ·
> **Date** : 2026-11-06 ·
> **Verdict** : ⚠️ **la surface est utilisable en autonomie ; la structure ne l'est pas encore.**
> **Aucun fichier existant modifié par cet audit ; aucun commit.** Sorties : ce rapport et
> [`pensee-produit-bloc-l.json`](pensee-produit-bloc-l.json).
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`gold_split.py`](../tools/tests/linguistique/gold_split.py) ; **50 phrases libres** écrites pour
> l'audit (textes dans le JSON) ; harnais local non committé dans `/tmp/audit_produit_bl`.
> **Porte** : `bash tools/porte-bloc-linguistique.sh` → **verte** (16 tests, autotest UDHR
> **0,9687**, profils permutés **0,0022**).

**En une phrase.** Sur 50 phrases libres, le bloc **ne plante pas**, **ne refu
… [5742 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\nlines=pathlib.Path('reports/rapport-produit-bloc-l.md').read_text().splitlines()\nbloc=[]; errs=[]\ndef check(b):\n    if len(b)<2: return []\n    n=[l.count('|') for l in b]\n    return [] if len(se … [648 caractères tronqués]`

  ```
tableaux déséquilibrés 0
lignes 423
JSON OK
5c6b3b43
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -4 --decorate && echo \"--- diff 6ef2a3f5..HEAD module/eval ---\" && git diff --stat 6ef2a3f5..HEAD -- tools/bloc_linguistique.py tools/tests/linguistique/evaluer_gold.py tools/tests/linguistique/test_bloc_linguisti … [240 caractères tronqués]`

  ```
5c6b3b43 (HEAD -> s/v7) PORTES — LA NUANCE cascade_pos : VERTE PAR PLANCHER, LA FUSION DÉGRADE ENCORE LE POS DE 1,16 PT (CORRECTIF À FAIRE)
e3db2cc8 OUTILLAGE — index_reports A UNE AIDE (--aide N'ÉCRIT PLUS), --verifier, INDEX 625 → 677 FICHES ; PLAN-TRAVAIL § 9 → § 13
6ef2a3f5 (origin/s/v7, origin/master, origin/HEAD, master) JOURNAL ET ROADMAP — LA VAGUE PRODUIT : DRAVE V0 DOCUMENTÉ, PORTE PRODUIT VERTE, AUTOTEST ×2,4, MASTER POUSSÉ (7f73c17f)
7f73c17f PRODUIT — LA DOC D'USAGE ET LES 5 EXEMPLES VÉRIFIÉS (5/5 REJOUÉS) ; CASCADE_POS N'EST PLUS UNE ROUGE (PLANCHER 0,70)
--- diff 6ef2a3f5..HEAD module/eval ---
(vide = inchangés)
--- status nos fichiers ---
?? reports/pensee-produit-bloc-l.json
?? reports/rapport-produit-bloc-l.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff --stat 6ef2a3f5..HEAD | tail -12", "description": "Voir les changements depuis le HEAD précédent"}`

  ```
.../rapport.md                                     |  21 +-
 journal/sessions/MANIFEST.md                       |   8 +-
 .../bf49d867-4b23-49e1-b214-9a2fd542fb1b/digest.md | 574 +++++++++++++++++++
 .../rapport.md                                     |  82 +++
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md | 283 ++++++++++
 .../rapport.md                                     |  91 ++-
 reports/INDEX.md                                   |  54 +-
 reports/README.md                                  |   2 +-
 reports/pensee-outillage-index.json                |  19 +
 reports/rapport-outillage-index.md                 |  52 ++
 tools/index_reports.py                             |  43 +-
 26 files changed, 2219 insertions(+), 57 deletions(-)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('reports/rapport-produit-bloc-l.md'); s=p.read_text()\ns=s.replace(\"> **Commit mesuré** : `fa1b0c6e` (2026-11-06 09:16) · **HEAD pendant la rédaction** : `6ef2a3f5`\",\n            \" … [1647 caractères tronqués]`

  ```
report ok
builder ok
JSON OK
11:  "head_au_moment_de_la_redaction": "5c6b3b43",
150:  "note_verdict": "Depuis 7f73c17f, evaluer_gold remplace la comparaison par un plancher 0,70 : cascade_pos passe à vrai et ok à vrai, sans changement du module ni des valeurs. La baisse de POS de la composition (0,7465 contre 0,7581) reste mesurée.",
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"6ef2a3f5\\|5c6b3b43\\|HEAD\" reports/rapport-produit-bloc-l.md | head -20 && echo \"--- HEAD actuel ---\" && git rev-parse --short HEAD", "description": "Vérifier les références HEAD de la fiche"}`

  ```
4:> **Commit mesuré** : `fa1b0c6e` (2026-11-06 09:16) · **Dernier HEAD vérifié** : `5c6b3b43`
58:Le rejeu du 2026-11-06 redonne l'**état fourni** (vivant 612 ; module inchangé à HEAD) ; la fiche
89:**Les quatre modes** (vivant 612 ; valeurs identiques à HEAD). Le mock est le double de contrat,
99:- **`cascade_pos` : rouge à `fa1b0c6e`, vert à HEAD par plancher.** À `fa1b0c6e`, le verdict
109:- **`ok`** : **faux à `fa1b0c6e`** (à cause de `cascade_pos`) ; **vrai à HEAD** (plancher 0,70),
--- HEAD actuel ---
37e2053c
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -3 --decorate && echo \"--- diff 5c6b3b43..HEAD module/eval ---\" && git diff --stat 5c6b3b43..HEAD -- tools/bloc_linguistique.py tools/tests/linguistique/evaluer_gold.py tools/tests/linguistique/test_bloc_linguisti … [100 caractères tronqués]`

  ```
37e2053c (HEAD -> s/v7) ÉTAT — T0 DANS LE BUDGET
5c6b3b43 PORTES — LA NUANCE cascade_pos : VERTE PAR PLANCHER, LA FUSION DÉGRADE ENCORE LE POS DE 1,16 PT (CORRECTIF À FAIRE)
e3db2cc8 OUTILLAGE — index_reports A UNE AIDE (--aide N'ÉCRIT PLUS), --verifier, INDEX 625 → 677 FICHES ; PLAN-TRAVAIL § 9 → § 13
--- diff 5c6b3b43..HEAD module/eval ---
(vide = inchangés)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('reports/rapport-produit-bloc-l.md'); s=p.read_text()\ns=s.replace('`5c6b3b43`','`37e2053c`')\ns=s.replace('module inchangé à HEAD','module inchangé de `fa1b0c6e` à `37e2053c` (dernier … [888 caractères tronqués]`

  ```
ok
4:> **Commit mesuré** : `fa1b0c6e` (2026-11-06 09:16) · **Dernier HEAD vérifié** : `37e2053c`
58:Le rejeu du 2026-11-06 redonne l'**état fourni** (vivant 612 ; module inchangé de `fa1b0c6e` à `37e2053c` (dernier contrôle)) ; la fiche
89:**Les quatre modes** (vivant 612 ; valeurs identiques à `37e2053c`). Le mock est le double de contrat,
99:- **`cascade_pos` : rouge à `fa1b0c6e`, vert au dernier contrôle (`37e2053c`) par plancher.** À `fa1b0c6e`, le verdict
109:- **`ok`** : **faux à `fa1b0c6e`** (à cause de `cascade_pos`) ; **vrai au dernier contrôle `37e2053c`** (plancher 0,70),
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '56,60p' reports/rapport-produit-bloc-l.md && sed -n '33,36p' reports/rapport-produit-bloc-l.md && grep -n \"vert à HEAD\\|à HEAD\" reports/rapport-produit-bloc-l.md || true", "description": "Corriger la parenthèse et vérifier … [18 caractères tronqués]`

  ```
## 2. État gold rejoué

Le rejeu du 2026-11-06 redonne l'**état fourni** (vivant 612 ; module inchangé de `fa1b0c6e` à `37e2053c` (dernier contrôle)) ; la fiche
v12 publie, elle, les valeurs du **gelé 602** pour le F1 et la tête :

| document | ⚠️ | toujours présent, mais **42/53** valeurs tronquées à 60 caractères, **1/50** faux titre (x48) + 4 en cas limites |
| langue fr/en | ✅ | **50/50** sur ce banc (34 fr, 14 en, 2 `und`) ; **39/50** seulement avec les profils UDHR, et le format change `fr`/`fra` |
| compositions | ❌ | refus et contexte perdus, cascade **50/50** appels ; POS **0,7465 < 0,7581** (verdict `cascade_pos` vert par plancher 0,70 depuis `7f73c17f`, pas par correctif) |
| scripts non latins | ⚠️ | russe et chinois : graphème/mot/phrase/document, **0 syntagme**, **0 morphème** |
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('reports/rapport-produit-bloc-l.md'); s=p.read_text()\ns=s.replace(\"(vivant 612 ; module inchangé de `fa1b0c6e` à `37e2053c` (dernier contrôle)) ; la fiche\",\n            \"(vivant 6 … [230 caractères tronqués]`

  ```
ok
## 2. État gold rejoué

Le rejeu du 2026-11-06 redonne l'**état fourni** (vivant 612 ; module inchangé de `fa1b0c6e` à `37e2053c`, dernier contrôle) ; la fiche
v12 publie, elle, les valeurs du **gelé 602** pour le F1 et la tête :
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('construire_json.py'); s=p.read_text()\ns=s.replace('\"head_au_moment_de_la_redaction\": \"5c6b3b43\"','\"head_au_moment_de_la_redaction\": \"37e2053c\",\\n        \"dernier_head_verifie\": \"37e2053c\"')\np.wr … [735 caractères tronqués]`

  ```
ok
JSON OK
37e2053c 37e2053c
True True
37e2053c
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"HEAD\\|5c6b3b43\\|6ef2a3f5\" reports/rapport-produit-bloc-l.md | head -20; echo \"---\"; python3 - <<'PY'\nimport pathlib\nlines=pathlib.Path('reports/rapport-produit-bloc-l.md').read_text().splitlines()\nbloc=[]; errs=[]\n … [665 caractères tronqués]`

  ```
4:> **Commit mesuré** : `fa1b0c6e` (2026-11-06 09:16) · **Dernier HEAD vérifié** : `37e2053c`
---
tableaux déséquilibrés 0 | lignes 423
JSON OK
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"HEAD: $(git rev-parse --short HEAD)\" && git status --short -- reports/rapport-produit-bloc-l.md reports/pensee-produit-bloc-l.json && ls -l reports/rapport-produit-bloc-l.md reports/pensee-produit-bloc-l.json && python3 - <<' … [635 caractères tronqués]`

  ```
HEAD: c6904284
?? reports/pensee-produit-bloc-l.json
?? reports/rapport-produit-bloc-l.md
-rw-r--r--. 1 stephane stephane 82886  6 nov 11:29 reports/pensee-produit-bloc-l.json
-rw-------. 1 stephane stephane 34505  6 nov 11:29 reports/rapport-produit-bloc-l.md
banc 0 0 0 34 149
gold 222 0.9289 0.5849 0.7581 17
perf [(10, 1.08), (50, 4.6), (200, 19.43)]
head 37e2053c ok_head True cascade_pos_head True
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -2 --decorate && echo \"--- diff 37e2053c..HEAD module/eval ---\" && git diff --stat 37e2053c..HEAD -- tools/bloc_linguistique.py tools/tests/linguistique/evaluer_gold.py tools/tests/linguistique/test_bloc_linguisti … [96 caractères tronqués]`

  ```
c6904284 (HEAD -> s/v7) ÉTAT — T0 À 4 000
37e2053c ÉTAT — T0 DANS LE BUDGET
--- diff 37e2053c..HEAD module/eval ---
(vide = inchangés)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('reports/rapport-produit-bloc-l.md'); s=p.read_text()\ns=s.replace(\"> **Commit mesuré** : `fa1b0c6e` (2026-11-06 09:16) · **Dernier HEAD vérifié** : `37e2053c`\\n> (module `bloc_lingu … [1452 caractères tronqués]`

  ```
report ok
builder ok
JSON OK
11:  "head_au_moment_de_la_redaction": "c6904284",
12:  "dernier_head_verifie": "c6904284",
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,10p' reports/rapport-produit-bloc-l.md && grep -n \"37e2053c\\|c6904284\" reports/rapport-produit-bloc-l.md && git rev-parse --short HEAD", "description": "Vérifier l'ancrage final"}`

  ```
# Audit produit du bloc linguistique — 0 plantage sur 50 phrases, 34/50 avec une anomalie de contrat

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Branche** : `s/v7` ·
> **Commit mesuré** : `fa1b0c6e` (2026-11-06 09:16) · **HEAD vérifié en fin d'audit** : `c6904284`
> (le HEAD a bougé pendant l'audit ; module `bloc_linguistique.py` inchangé ; `evaluer_gold.py`
> modifié en `7f73c17f`) ·
> **Date** : 2026-11-06 ·
> **Verdict** : ⚠️ **la surface est utilisable en autonomie ; la structure ne l'est pas encore.**
> **Aucun fichier existant modifié par cet audit ; aucun commit.** Sorties : ce rapport et
> [`pensee-produit-bloc-l.json`](pensee-produit-bloc-l.json).
4:> **Commit mesuré** : `fa1b0c6e` (2026-11-06 09:16) · **HEAD vérifié en fin d'audit** : `c6904284`
59:Le rejeu du 2026-11-06 redonne l'**état fourni** (vivant 612 ; module inchangé de `fa1b0c6e` à `c6904284`, dernier contrôle) ; la fiche
90:**Les quatre modes** (vivant 612 ; valeurs identiques à `c6904284`). Le mock est le double de contrat,
100:- **`cascade_pos` : rouge à `fa1b0c6e`, vert au dernier contrôle (`c6904284`) par plancher.** À `fa1b0c6e`, le verdict
110:- **`ok`** : **faux à `fa1b0c6e`** (à ca
… [89 caractères tronqués]
  ```

- **send_message** `{"agent_id": "e181ce02-cd50-488a-a6be-e84b79d40dcc", "message": "Audit produit du bloc linguistique terminé. Deux fichiers neufs, aucun existant modifié, aucun commit :\n- `reports/rapport-produit-bloc-l.md`\n- `reports/pensee-produit-bloc-l.json` (contient les 50 textes, les 25 cas limites, les 18  … [4831 caractères tronqués]`

  ```
message delivered to agent e181ce02-cd50-488a-a6be-e84b79d40dcc
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"HEAD $(git rev-parse --short HEAD)\" && git status --short -- reports/rapport-produit-bloc-l.md reports/pensee-produit-bloc-l.json && grep -n \"6ef2a3f5\\|5c6b3b43\\|37e2053c\\|c6904284\" reports/pensee-produit-bloc-l.json rep … [265 caractères tronqués]`

  ```
HEAD c6904284
?? reports/pensee-produit-bloc-l.json
?? reports/rapport-produit-bloc-l.md
reports/pensee-produit-bloc-l.json:10:  "gold": "evaluer_gold.charger() + evaluer_bloc ; gold_split.dev/test ; module tools/bloc_linguistique.py au commit fa1b0c6e (module inchangé à HEAD 6ef2a3f5).",
reports/pensee-produit-bloc-l.json:11:  "head_au_moment_de_la_redaction": "c6904284",
reports/pensee-produit-bloc-l.json:12:  "dernier_head_verifie": "c6904284",
reports/rapport-produit-bloc-l.md:4:> **Commit mesuré** : `fa1b0c6e` (2026-11-06 09:16) · **HEAD vérifié en fin d'audit** : `c6904284`
reports/rapport-produit-bloc-l.md:59:Le rejeu du 2026-11-06 redonne l'**état fourni** (vivant 612 ; module inchangé de `fa1b0c6e` à `c6904284`, dernier contrôle) ; la fiche
reports/rapport-produit-bloc-l.md:90:**Les quatre modes** (vivant 612 ; valeurs identiques à `c6904284`). Le mock est le double de contrat,
reports/rapport-produit-bloc-l.md:100:- **`cascade_pos` : rouge à `fa1b0c6e`, vert au dernier contrôle (`c6904284`) par plancher.** À `fa1b0c6e`, le verdict
reports/rapport-produit-bloc-l.md:110:- **`ok`** : **faux à `fa1b0c6e`** (à cause de `cascade_pos`) ; **vrai au dernier contrôle `c6904284`** (
… [140 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/audit_produit_bl && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('construire_json.py'); s=p.read_text()\ns=s.replace('module tools/bloc_linguistique.py au commit fa1b0c6e (module inchangé à HEAD 6ef2a3f5).',\n            'module tools/bloc_linguistique.py au commit fa1b0c6e  … [442 caractères tronqués]`

  ```
ok
JSON OK
10:  "gold": "evaluer_gold.charger() + evaluer_bloc ; gold_split.dev/test ; module tools/bloc_linguistique.py au commit fa1b0c6e (module inchangé de fa1b0c6e à c6904284).",
11:  "head_au_moment_de_la_redaction": "c6904284",
12:  "dernier_head_verifie": "c6904284",
  ```

### 🤖 Assistant

Audit terminé. J'ai écrit **uniquement deux fichiers neufs**, sans modifier d'existant et sans commit :

- [`reports/rapport-produit-bloc-l.md`](reports/rapport-produit-bloc-l.md)
- [`reports/pensee-produit-bloc-l.json`](reports/pensee-produit-bloc-l.json) — contient les 50 textes, les 25 cas limites, les 18 correctifs et tous les chiffres.

## Plantages

- **0 plantage sur les 50 phrases libres**, **0 refus**, **0 sortie vide**, **0 span hors texte**, **0 cible absente**.
- **34/50 textes** ont au moins une anomalie (**149** au total) :
  - **132 paires de syntagmes qui se chevauchent**, dans **31/50 textes**, soit **188/362 étiquettes (51,9 %)** ; le chunker seul n'en produit aucune, c'est le générateur S + l'union ;
  - 1 chevauchement de phrases (f10), dû à l'extension d'abréviation `M.` ;
  - 8 morphèmes normalisés (`tion` vs `TION`), 4 actes `exclamation` absents des candidats, 4 listes de candidats avec doublons.
- **Cas limites** : **1 plantage textuel** — un surrogate isolé, `UnicodeEncodeError` à `len(texte.encode())` (ligne 1246) — plus **3 entrées non-str** (`bytes`, `int`, `list` → `AttributeError`). `None` devient silencieusement `refus = "vide"`.
- Qualité libre : 365 `NOUN` pour 32 `VERB` ; « arrose », « rentre », « prépare », « warm » → `NOUN`. Les URL, décimaux et abréviations cassent les frontières de phrase ; les types `url` et `emoji` ne sortent **jamais** (0/963).

## Temps par phrase

| mode | 10 mots | 50 mots | 200 mots |
|---|---:|---:|---:|
| heuristique | **1,08 ms** | **4,60 ms** | **19,43 ms** |
| parallèle | 1,51 ms | 6,18 ms | 27,22 ms |
| cascade | 1,51 ms | 6,25 ms | 29,64 ms |

- Débit : **923 / 218 / 51,5 phrases/s** ; **0,09–0,11 ms/mot**.
- Mémoire : pic **540,6 Kio** pour 200 mots ; RSS **30,7 Mio**, **delta 0** après 100 analyses ; démarrage à froid **99–113 ms**.
- Au-delà de 200 mots, coût superlinéaire : **0,394 ms/mot à 4 000 mots** (1,57 s, exposant ≈ 1,45), à cause de `_cible_proche` (199 302 appels à `_est_adverbe_seul`).
- Déterminisme : **mêmes JSON** sur même instance, instances fraîches et graines de hash **0/1/42** ; seule `duree_s` varie, et elle est exclue par défaut.

## Contrat

**Stable** : 11 clés pour `Annotation`, 11 pour `Etiquette`, spans valides, aucun span vide, `confiance ∈ [0,1]` pour l'heuristique, unités triées/disjointes, fraction recalculable.

**Peut être vide/absent** : `etiquettes`, `unites_semantiques`, `fraction_semantique=0`, `refus`, `candidats`, `meta`, `contexte`, `langue="und"`, `script="Zyyy"` ; **morphème absent 9/50**, **syntagme absent 2/50**.

**Un client ne peut pas supposer** : syntagmes disjoints, neuf niveaux présents, `valeur` = surface (morphème normalisé, document tronqué à 60 : 42/53), `meta`/`cout`/`trace` à schéma fixe, `langue` ISO2 ou ISO3 (`fr` par défaut, `fra` avec profils), `Annotation.source` dans l'enum (ajoute `parallele`/`cascade`), `refus` enum (4 sémantiques), ni l'offset de la cible d'attachement. `couverture()` est un **max de confiance**, pas un taux.

## 5 correctifs prioritaires

1. **P0-1 — Expliciter les alternatives de syntagmes** : 132 paires/31 textes. Ne pas dédupliquer en silence : la déduplication simulée donne F1 0,5849→0,6141 mais **222→208 attachements exacts** (couverture 0,9289→0,8703).
2. **P0-2 — Réparer les frontières de phrase** (décimaux, dates, URL/emails, abréviations, espace initial) **et les types `url`/`emoji` morts** : une URL crée 3–4 phrases, `12.5` coupe une phrase en deux, `M./Dr./etc.` duplique la phrase.
3. **P0-3 — Compositions** : propager `refus` et `contexte`, rattraper `RefusNeuronal`, garder `MockNeuronal` ; aujourd'hui `"... !!! ???"` rend **4 étiquettes inventées**.
4. **P0-4 — Cascade sélective** : **50/50** appels, **1 676/1 676** sur le gold ; seuil 0,6 au-dessus des confiances déclarées et `couverture()` = max masque les POS ouvertes.
5. **P0-5 — Langue** : format `fr`/`fra` selon le mode, indice `fr` ignoré avec les profils, **39/50** avec profils contre **50/50** en défaut.

Juste derrière : **POS des nombres/ponctuation** (157/963 tokens sans POS) et **POS ouvertes** (0,6234 ; tagger réel documenté 0,9440).

## Point d'état important

HEAD a bougé pendant l'audit (`fa1b0c6e` → `c6904284`) ; le module `bloc_linguistique.py` est **inchangé**. Le rouge `cascade_pos` a été **éteint par un plancher 0,70** dans `7f73c17f`, pas par un correctif : à HEAD, `ok=true`, mais la cascade reste à **0,7465 < 0,7581** et perd toujours 14 spans d'attachement. La fiche distingue explicitement les deux états.

