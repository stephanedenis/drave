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

