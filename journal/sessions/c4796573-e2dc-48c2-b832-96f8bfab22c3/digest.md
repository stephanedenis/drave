# Session DSH — relecture

- identifiant : `c4796573-e2dc-48c2-b832-96f8bfab22c3`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-05 13:16:52
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : écrire le **contrat d'interface** entre le bloc linguistique (`tools/bloc_linguistique.py`, territoire L) et le générateur de structures S (`tools/structures/generateur.py`, territoire S), en particulier pour les **subordonnées REL/SUB**, et mesurer l'écart actuel.

Contexte mesuré le 2026-11-05 : sur 239 cibles d'attachement du gold, **94 n'ont pas de segment prédit au bon span** — 48 REL, 33 SUB, 13 GP ; 81 des 94 sont des REL/SUB que la segmentation ne produit pas (ou produit avec un span plus large). Le bloc consomme S via `_syntagmes_s` (dicts `type/debut/fin/role/cible_*`) et `_cibles_s`.

À faire :
1. Lis `tools/bloc_linguistique.py` (classe `Heuristique`, `_syntagmes_s`, `_cibles_s`, `_cible_proche`, `_tete_nom`) et `tools/structures/generateur.py` (classe `Segment`, `_segmente`, `construire_arbre`, les cibles `cible_nom/cible_gp/cible_verbe`).
2. Écris le **contrat** : ce que S doit fournir (types, spans, rôles, cibles) pour que le bloc attache correctement, et ce que le bloc peut/devrait faire lui-même (repli). Nomme précisément les fonctions et champs.
3. Mesure l'écart : combien de REL/SUB du gold S produit-il ? Avec quel span ? Combien de cibles S fournit-il (`cible_*`) et lesquelles sont justes ?
4. Écris **uniquement** deux fichiers neufs : `reports/rapport-contrat-s.md` (fiche : titre, verdict, le contrat, le tableau des écarts mesurés, contrôle négatif, limites) et `reports/pensee-contrat-s.json`.
5. **N'écris rien** dans `tools/structures/` : c'est un document de spécification, pas une modification de S.

Règles strictes : ne committe rien ; ne modifie aucun fichier existant ; n'écris pas dans `docs/pilotage/`, `AGENTS.md`, `journal/`, `tools/structures/`, `data/`, `tools/entrainer_native.py`, `tools/native_model.py`. Rends un résumé : ce que S ne fournit pas, ce que le bloc doit faire, l'écart chiffré.
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

⏵ Exploration du dépôt et lecture des deux fichiers cibles

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git branch --show-current && git status --short | head -20 && ls", "description": "Vérifier branche et état du dépôt"}`

  ```
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
MM journal/README.md
MM journal/THEMES.md
MM journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/digest.md
MM journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/rapport.md
MM journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/digest.md
MM journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/rapport.md
D  journal/sessions/63d4c619-63e8-41b9-a183-5c6f1ac05a21/digest.md
D  journal/sessions/63d4c619-63e8-41b9-a183-5c6f1ac05a21/rapport.md
MM journal/sessions/MANIFEST.md
D  journal/sessions/a8035275-c7b9-4713-a6ab-7b859cd72306/digest.md
D  journal/sessions/a8035275-c7b9-4713-a6ab-7b859cd72306/rapport.md
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
… [45 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && wc -l tools/bloc_linguistique.py tools/structures/generateur.py && ls reports/ | head -40", "description": "Compter lignes et lister reports"}`

  ```
1881 tools/bloc_linguistique.py
   648 tools/structures/generateur.py
  2529 total
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

### 🤖 Assistant

⏵ Lecture du générateur de structures S

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/generateur.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/generateur.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """generateur.py — une phrase brute → des structures candidates (v0 heuristique).
3: 
4: Ce n'est pas un analyseur syntaxique : c'est un **générateur de candidats** à faire valider par
5: un humain. Il segmente (GN, GV, GP, REL, SUB), devine des rôles par la préposition, puis produit
6: plusieurs candidats en variant l'**attachement** de chaque segment ambigu (GN le plus proche ou
7: GV le plus proche).
8: 
9:     python3 generateur.py "Le chat de la voisine qui dort sur le toit se réveille."
10:     python3 generateur.py --json "..."     # la structure complète
11: """
12: from __future__ import annotations
13: 
14: import json
15: import re
16: import unicodedata
17: 
18: DET = set("le la les l un une ce cet cette ces mon ma mes ton ta tes son sa ses "
19:           "notre nos votre vos leur leurs quel quelle quels quelles".split())
20: PREP = set("a au aux de du des d en dans par pour sur sous avec sans chez vers entre depuis "
21:            "pendant durant contre malgre selon pres loin devant derriere apres avant".split())
22: REL
… [32441 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Repérage des fonctions clés du bloc linguistique

- **grep** `{"pattern": "^\\s*(def |class )|_syntagmes_s|_cibles_s|_cible_proche|_tete_nom", "path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py"}`

  ```
Found 100 matches

tools/bloc_linguistique.py
Line 59: class Span:
Line 63:     def json(self) -> dict:
Line 68: class Etiquette:
Line 81:     def json(self) -> dict:
Line 92: class Annotation:
Line 105:     def par_niveau(self) -> dict[str, list[Etiquette]]:
Line 111:     def couverture(self) -> dict[str, float]:
Line 116:     def json(self, avec_duree: bool = False) -> dict:
Line 130: class BlocLinguistique(Protocol):
Line 133:     def analyser(self, texte: str, langue: str | None = None,
Line 137: class RefusNeuronal(RuntimeError):
Line 144: def _normaliser(texte: str) -> str:
Line 148: def _trigrammes(texte: str) -> list[str]:
Line 153: def _profil(texte: str, top: int = 200) -> dict[str, int]:
Line 158: def charger_profils_udhr(chemin: pathlib.Path, train=(0, 14), test=(15, 30),
Line 192: def _score_profil(tri: collections.Counter, profil: dict[str, int]) -> float:
Line 199: def detecter_langue(texte: str, profils: dict[str, dict] | None = None,
Line 230: def _script_char(ch: str) -> str:
Line 256: def detecter_script(texte: str) -> str:
Line 428: def _est_verbe(mot: str) -> bool:
Line 447: def _role_gp(prep: str) -> str:
Line 472: class Heuristique:
Line 477:     def __init__
… [5311 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "offset": 1, "limit": 140}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "offset": 400, "limit": 300}`

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
… [4774 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
400: bu cru sue pu voulu dû venue venu partie parti sorti mort née né ouvert offerte souffert couru
401: reçu aperçu déçu attendu entendu répondu perdu rendu vendu descendu monté resté tombé arrivé
402: entré rentré retourné passé tenu obtenu devenu revenu
403: travailles travaillent travaillait regarder regarde regardes regardent regardait écouter écoute
404: écoutes écoutent écoutait aimer aime aimes aiment aimait finir finis finit finissent finissait
405: grandir grandis grandit grandissent ouvrir ouvre ouvres ouvrent ouvrait fermer ferme fermes
406: ferment fermait donner donne donnes donnent donnait chercher cherche cherches cherchent trouvait
407: talk talks talked talking play plays played playing leave leaves left leaving write writes wrote
408: written writing read reads reading listen listens listened listening sleep sleeps slept sleeping
409: grow grows grew grown growing bark barks barked barking run runs ran running walk walks walked
410: walking sing sings sang sung singing dance dances danced dancing work works worked working
411: watch watches watched 
… [14640 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 250, "offset": 700}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
700:                 role = "groupe nominal"
701:                 # le passif sans `par` : GN + AUX (être) + participe → le sujet est un patient
702:                 if j < len(mots) and _normaliser(mots[j][2]) in {
703:                         "est", "sont", "était", "étaient", "été", "sera", "seront",
704:                         "suis", "es", "sommes", "êtes"}:
705:                     role = "patient"
706:                 segments.append({"type": "GN", "role": role, "niveau": 0,
707:                                  "debut": d, "fin": mots[j - 1][1],
708:                                  "texte": texte[d:mots[j - 1][1]], "candidats": []})
709:                 i = j
710:                 continue
711:             if typ == "mot" and n in lex.get("PREP", set()) and i + 1 < len(mots):
712:                 j = i + 1
713:                 # le GP s'arrête au verbe ou au relatif : « de la voisine | dort » et non
714:                 # « de la voisine dort » (mesuré : 25 spans « plus large » sur le gold).
715:                 while (j < len(mots) and mots[j][3] == "mot"
71
… [15384 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Recherche du gold et du dispositif de mesure T162

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rl \"239\" reports/ tools/ docs/ 2>/dev/null | head -20; echo ---; ls tools/ | grep -i -E \"mesure|analyse|gold|t162|attache\" ", "description": "Chercher le dispositif de mesure"}`

  ```
reports/rapport-phase3-reparti.md
reports/rapport-mode4-lot-listes.md
reports/rapport-aiguille-topk.md
reports/archive/rapport-toutes-langues.md
reports/toutes-langues/060-60-le-retrecissement-est-reel-mais-ce-nest.md
reports/rapport-c9-lateralite.md
reports/rapport-vision-qwen2vl.md
reports/restitution-udhr.json
reports/restitution-udhr-flux.json
reports/traduction-legal.json
reports/traduction-legal-0.5b-6.json
reports/traduction-eurlex-3b.json
reports/traduction-eurlex-0.5b.json
reports/traduction-langues-3b.json
reports/traduction-24langues-B.json
reports/traduction-24langues-3b-B.json
reports/traduction-24langues-3b-A.json
reports/traduction-onu-3b.json
reports/traduction-onu6-7b.json
reports/traduction-onu6-3b.json
---
analyse_alignement.py
analyse_empreinte.py
analyse_engram.py
analyse_experts_statique.py
analyse_flux.py
analyse_hc.py
analyse_litteraire.py
analyse_octets_par_jeton.py
analyse_reutilisation_experts.py
analyse_union_experts.py
mesure_fenetres.sh
mesure_jeux.py
mesure_langues.py
mesure_lot_disque.sh
mesure_maitres.py
mesure-prefill-lot.sh
mesurer_colonnes.py
mesurer_cout.py
mesurer_lecture_experts.py
mesurer_ocr.py
mesurer_reel.py
mesurer_scans.py
mesurer_tables
… [3 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rln \"attachement\" reports/*.md tools/*.py tools/*.sh 2>/dev/null | head -30", "description": "Lister fichiers parlant d'attachement"}`

  ```
reports/INDEX.md
reports/rapport-bloc-linguistique.md
reports/rapport-pensee-attachement-cible.md
reports/rapport-pensee-attachement.md
reports/rapport-pensee-cible-proximite.md
reports/rapport-pensee-cibles-500.md
reports/rapport-pensee-cibles.md
reports/rapport-pensee-classement.md
reports/rapport-pensee-convention-doc.md
reports/rapport-pensee-conventions.md
reports/rapport-pensee-denominateur.md
reports/rapport-pensee-echecs-attachement.md
reports/rapport-pensee-echecs-cible.md
reports/rapport-pensee-gold-342.md
reports/rapport-pensee-gold-linguistique.md
reports/rapport-pensee-gold-neuronal.md
reports/rapport-pensee-relation.md
reports/rapport-pensee-roles.md
reports/rapport-pensee-spans.md
reports/rapport-s-arbre-referents.md
reports/README.md
tools/bloc_linguistique.py
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rln \"gold\" tools/*.py | head -20; echo ---; ls data/ | head -30; echo ---; find data -iname \"*gold*\" -o -iname \"*attache*\" | head -20", "description": "Chercher fichier gold"}`

  ```
tools/banc_complet.py
tools/banc_durci.py
tools/banc_lecture.py
tools/bloc_linguistique.py
tools/bloc_tableaux.py
tools/calibrer.py
tools/corpus_gele.py
tools/index_spans.py
tools/mesurer_ocr.py
tools/tete_survol.py
tools/xnli_entrainement.py
tools/xnli_latent.py
tools/xnli_train_complet.py
---
adaptateurs
alignement
composition-etats.npz
composition-verne-14b-etats.npz
composition-verne-7b-etats.npz
composition-verne-etats.npz
composition-verne-large-etats.npz
composition-verne-plan-etats.npz
consignes_train.jsonl
consignes_val.jsonl
corpus_en.txt
corpus_en_val.txt
corpus_fr_litterature.txt
corpus_fr_train.txt
corpus_fr.txt
corpus_fr_val.txt
corpus_litt_propre
corpus_mixte_dev.txt
corpus_mixte_litt2.txt
corpus_mixte_litt.txt
corpus_mixte_propre.txt
corpus_mixte.txt
corpus_multi_train.txt
corpus_multi.txt
corpus_multi_val.txt
corpus_nonambigu
corpus_ocr
corpus_ocr_cegep
corpus_ocr_cegep_avant_micro
corpus_ocr_cegep_micro
---
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && head -80 reports/rapport-pensee-echecs-attachement.md", "description": "Lire fiche échecs attachement"}`

  ```
# B13 — les 127 échecs qualifiés : 94 de span, 33 de cible

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-04 · **Verdict** : ✅
> **166/166 portes** : les **127 échecs** de l'attachement (avant ce round) se répartissent en
> **94 de span** (aucun segment prédit au même span) et **33 de cible** (le span est bon, la cible
> n'est pas dans les candidats) — **32** après le correctif. Le correctif testé — ajouter les GV du chunker aux GV du générateur S et
> remplir les segments d'union — ne répare **qu'un** des 33. Les 32 autres ont un GV qui couvre
> **toute la phrase** : le dernier token n'est pas le verbe (`… in the park` → `park`, pas `saw`).
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-echecs-attachement.json`](pensee-echecs-attachement.json).

## 1. La répartition

| cause | nombre | part |
|---|---:|---:|
| **span faux** (aucun segment prédit au même span) | **94** | 74,0 % |
| **cible hors des candidats** (span bon) | **33** → **32** après le correctif | 26,0 % |
| **tout** | **127**
… [2193 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rln \"48 REL\\|81 des 94\\|48.*REL.*33.*SUB\" reports/ docs/ journal/ 2>/dev/null | head -20", "description": "Chercher la qualification 48 REL/33 SUB"}`

  ```
reports/README.md
reports/rapport-pensee-spans.md
docs/pilotage/roadmap.md
docs/implantation/moteur-de-pensee.md
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/digest.md
journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/digest.md
journal/sessions/aeafe951-9c3d-4bb5-8af7-0246a4f3d51d/digest.md
journal/sessions/63d4c619-63e8-41b9-a183-5c6f1ac05a21/digest.md
journal/sessions/ff7e786c-3ece-4eae-864e-19dddfead93c/digest.md
journal/sessions/c4796573-e2dc-48c2-b832-96f8bfab22c3/digest.md
journal/2026-11-04/README.md
journal/2026-11-04/docs.md
journal/2026-11-05/README.md
journal/2026-11-05/mesures.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls reports/*attache* reports/*cible* reports/*gold* 2>/dev/null; echo ---; head -60 reports/rapport-pensee-attachement-cible.md", "description": "Lister fiches attachement/cible"}`

  ```
reports/pensee-attachement-cible.json
reports/pensee-attachement-cible.json
reports/pensee-attachement.json
reports/pensee-cible-proximite.json
reports/pensee-cibles-500.json
reports/pensee-cibles.json
reports/pensee-echecs-attachement.json
reports/pensee-echecs-cible.json
reports/pensee-gold-200.json
reports/pensee-gold-342.json
reports/pensee-gold-cascade-200.json
reports/pensee-gold-cascade.json
reports/pensee-gold-complexes100.json
reports/pensee-gold-complexes20.json
reports/pensee-gold-complexes50.json
reports/pensee-gold-complexes.json
reports/pensee-gold-discours.json
reports/pensee-gold-gele.json
reports/pensee-gold-linguistique.json
reports/pensee-gold-neuronal.json
reports/pensee-gold-pragmatique.json
reports/pensee-gold-reel-cascade.json
reports/pensee-gold-subsets.json
reports/pensee-gold-syntagmes.json
reports/rapport-pensee-attachement-cible.md
reports/rapport-pensee-attachement-cible.md
reports/rapport-pensee-attachement.md
reports/rapport-pensee-cible-proximite.md
reports/rapport-pensee-cibles-500.md
reports/rapport-pensee-cibles.md
reports/rapport-pensee-echecs-attachement.md
reports/rapport-pensee-echecs-cible.md
reports/rapport-pensee-gold-200.md
reports/rapport
… [3591 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat reports/rapport-pensee-spans.md", "description": "Lire fiche spans"}`

  ```
# B13 — les 94 spans : 48 REL, 33 SUB, 12 GP

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
> **169/169 portes** : les échecs d'attachement par **span** (93 après le correctif) sont
> **48 REL**, **33 SUB** et **12 GP** — les subordonnées ne sont **pas produites** (65 cas) ou le
> sont avec un span plus large (25). Le correctif testé — borner le GP au verbe et au relatif —
> gagne **un span** (couverture 0,6067 → 0,6109, F1 0,2864 → 0,2869) mais **perd une cible** :
> le total des échecs ne bouge pas (107).
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-spans.json`](pensee-spans.json).

## 1. Les 93 spans

| type | échecs de span |
|---|---:|
| **REL** | **48** |
| **SUB** | **33** |
| **GP** | **12** |
| **tout** | **93** |

| catégorie | nombre |
|---|---:|
| aucun segment du même type | 65 |
| plus large | 25 |
| plus étroit | 3 |
| coupé en plusieurs | 1 |

| mesure | avant | **après le GP borné** |
|---|---:|---:|
| segments au bon span (labels) | 145 | **146** |
… [1894 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n -A5 -B5 \"48 REL\\|81 des 94\\|contrat\" journal/2026-11-05/mesures.md | head -80", "description": "Chercher chiffres dans mesures du jour"}`

  ```
9-| heure | commit | fait | fichiers |
10-|---|---|---|---|
11-| 01:10 | `01107366` | BANC DE LECTURE — L'ANCRE « < 2,5 » DEVIENT « SOUS 2,5 » ; PORTE-LECTEUR REJOUÉE VERTE | `en-cours.md`, `README.md`, `distribue.md` (+9) |
12-| 08:58 | `9ff4adda` | B13 — LE VERBE DU GV-PHRASE : EXACT 0,0586 → 0,0962, TOP-K 0,5105, TÊTE 0,8414 ; 167/167 | `moteur-de-pensee.md`, `chantiers.md`, `en-cours.md` (+18) |
13-| 09:11 | `d400e188` | B13 — LE LEXIQUE VERBAL : EXACT 0,0962 → 0,1381, TÊTE 0,9034 ; 168/168 | `moteur-de-pensee.md`, `chantiers.md`, `en-cours.md` (+19) |
14:| 09:35 | `13e8bb2d` | B13 — LES SPANS PERDUS : 48 REL, 33 SUB, 12 GP (81 CHEZ S) ; LE GP EST BORNÉ AU VERBE ; 169/169 | `moteur-de-pensee.md`, `chantiers.md`, `en-cours.md` (+19) |
15-| 09:42 | `f8f5bc04` | B13 — LE DÉNOMINATEUR DE L'ATTACHEMENT : RENDEMENT (÷239) ET EXACTITUDE SPANS (÷146), 0,7877/0,9041/0,2260 ; 170/170 | `moteur-de-pensee.md`, `chantiers.md`, `en-cours.md` (+18) |
16-| 10:18 | `23853cb7` | B13 — L'ATTACHEMENT CIBLÉ : REL → ANTÉCÉDENT, GP → VERBE ; EXACT 0,6438 → 0,8082, VERBES 0,9412 ; 173/173 | `moteur-de-pensee.md`, `chantiers.md`, `en-cours.md` (+23) |
17-| 10:39 | `a408a909` | B13 — LE LEXIQUE ÉLARGI (
… [468 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls tools/tests/linguistique/ && wc -l tools/tests/linguistique/*.py", "description": "Lister tests linguistiques"}`

  ```
anaphore.py
evaluer_gold.py
gold_gele.json
gold.json
gold.py
gold_reel.json
gold_reel.py
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
test_bloc_linguistique.py
   407 tools/tests/linguistique/anaphore.py
   283 tools/tests/linguistique/evaluer_gold.py
   120 tools/tests/linguistique/gold.py
  1383 tools/tests/linguistique/gold_reel.py
   204 tools/tests/linguistique/gold_synthetique.py
    75 tools/tests/linguistique/juge.py
   535 tools/tests/linguistique/miroir.py
   195 tools/tests/linguistique/qualifier_cascade.py
   134 tools/tests/linguistique/qualifier_frontiere_71.py
   156 tools/tests/linguistique/qualifier_lien_appris.py
   309 tools/tests/linguistique/qualifier_neuronal.py
   195 tools/tests/linguistique/qualifier_pragmatique.py
   135 tools/tests/linguistique/qualifier_quatre_modes.py
   237 tools/tests/linguistique/qualifier_syntagmes.py
   191 tools/tests/linguistique/test_bloc_linguistique.py
  4559 total
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"GOLD\\|gold\" tools/tests/linguistique/evaluer_gold.py | head -30", "description": "Repérer le gold dans evaluateur"}`

  ```
1:"""evaluer_gold.py — mesure le bloc linguistique sur le gold réel (20) + synthétique (160).
19:GOLD = pathlib.Path(__file__).with_name("gold.json")
20:REEL = pathlib.Path(__file__).with_name("gold_reel.json")
21:SYNTH = pathlib.Path(__file__).with_name("gold_synthetique.json")
25:    hand = json.loads(GOLD.read_text(encoding="utf-8"))["phrases"]
35:GELE = pathlib.Path(__file__).with_name("gold_gele.json")
39:    """Le gold **gelé** : une copie figée pour les portes à nombre absolu.
41:    Le gold vivant grandit (phrases, liens) ; les portes qui codent un chiffre exact
106:        pred_seg, gold_seg = _seg(a), {(s["type"], s["debut"], s["fin"]) for s in phrase["segments"]}
107:        tp += len(pred_seg & gold_seg)
108:        fp += len(pred_seg - gold_seg)
109:        fn += len(gold_seg - pred_seg)
111:        gold_tete = {(s["type"], s["debut"]) for s in phrase["segments"]}
112:        ttp += len(pred_tete & gold_tete)
113:        tfp += len(pred_tete - gold_tete)
114:        tfn += len(gold_tete - pred_tete)
130:            # le gold mêle deux conventions : la cible est un verbe (le gouverneur) ou un nom
145:            # attachement par tête : le segment prédit qui couvre la t
… [145 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/evaluer_gold.py"}`

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
… [14340 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Inspection de la structure du gold

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, pathlib\nbase = pathlib.Path(\"tools/tests/linguistique\")\nph = []\nfor f in (\"gold.json\",\"gold_reel.json\",\"gold_synthetique.json\"):\n    d = json.loads((base/f).read_text())\n    print(f, len(d … [561 caractères tronqués]`

  ```
gold.json 20
gold_reel.json 432
gold_synthetique.json 160
total 612
{
 "id": "g001",
 "langue": "fr",
 "texte": "Le chat dort.",
 "mots": [
  {
   "texte": "Le",
   "pos": "DET",
   "debut": 0,
   "fin": 2
  },
  {
   "texte": "chat",
   "pos": "NOUN",
   "debut": 3,
   "fin": 7
  },
  {
   "texte": "dort",
   "pos": "VERB",
   "debut": 8,
   "fin": 12
  }
 ],
 "segments": [
  {
   "type": "GN",
   "texte": "Le chat",
   "role": "agent",
   "debut": 0,
   "fin": 7
  },
  {
   "type": "GV",
   "texte": "dort",
   "role": "prédicat",
   "debut": 8,
   "fin": 12
  }
 ],
 "pragma": {
  "acte": "assertion"
 }
}
segments avec cible par type Counter({'GP': 96, 'REL': 74, 'SUB': 69}) total 239
segments par type Counter({'GN': 828, 'GV': 712, 'GP': 105, 'REL': 74, 'SUB': 70, 'ADJ': 35, 'ADV': 30, 'PONCT': 9}) total 1863
  ```

### 🤖 Assistant

⏵ Vérification des commits et de l'état du code de mesure

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -8 -- tools/bloc_linguistique.py tools/structures/generateur.py && git log --oneline -3 && git diff --stat -- tools/ | tail -5", "description": "Historique des fichiers S et bloc"}`

  ```
a408a909 B13 — LE LEXIQUE ÉLARGI (PARTICIPES IRRÉGULIERS ET EN -É) : EXACT 0,8082 → 0,8483 ; 174/174
23853cb7 B13 — L'ATTACHEMENT CIBLÉ : REL → ANTÉCÉDENT, GP → VERBE ; EXACT 0,6438 → 0,8082, VERBES 0,9412 ; 173/173
d8edd1d9 B13 — LE CLASSEMENT : EXACT 0,2260 → 0,6438 (CIBLE RÉDUITE À SA TÊTE) ; LE GOLD MÊLE DEUX CONVENTIONS (51 VERBES, 95 NOMS) ; 171/171
13e8bb2d B13 — LES SPANS PERDUS : 48 REL, 33 SUB, 12 GP (81 CHEZ S) ; LE GP EST BORNÉ AU VERBE ; 169/169
d400e188 B13 — LE LEXIQUE VERBAL : EXACT 0,0962 → 0,1381, TÊTE 0,9034 ; 168/168
9ff4adda B13 — LE VERBE DU GV-PHRASE : EXACT 0,0586 → 0,0962, TOP-K 0,5105, TÊTE 0,8414 ; 167/167
425754c3 B13 — LES 127 ÉCHECS QUALIFIÉS : 94 DE SPAN, 33 DE CIBLE (32 APRÈS L'UNION) ; 166/166
f7195ce0 B13 — LES CANDIDATS VERBES : TOP-K 0,3264 → 0,4686, TÊTE 0,7655 ; 165/165
4a65d44f PILOTAGE — VAGUE 1 DES SOUS-AGENTS NOTÉE ; HORODATAGES ALIGNÉS SUR 13 H 15
dfc860a4 ÉTAT — LE LIEN VERS PLAN-TRAVAIL EST RÉPARÉ (../PLAN-TRAVAIL.MD → PLAN-TRAVAIL.MD) ; LA REVUE DE DOCUMENTATION REPASSE VERTE
56d70431 ÉTAT — B13 177/177, TRIM T0 ; LA TRANCHE SOUS-AGENTS CONTINUE
 tools/structures | 0
 1 file changed, 0 insertions(+), 0 deletions(-)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -c \"RELATIFS\" tools/bloc_linguistique.py; git log -1 --format=%H%n%ci%n%s", "description": "Vérifier commit courant"}`

  ```
2
4a65d44f1ce05002226da775a69785f3531ed3bd
2026-11-05 13:14:11 -0500
PILOTAGE — VAGUE 1 DES SOUS-AGENTS NOTÉE ; HORODATAGES ALIGNÉS SUR 13 H 15
  ```

### 🤖 Assistant

⏵ Écriture du script de mesure (hors dépôt, dans /tmp)

- **write** `{"file_path": "/tmp/mesure_contrat_s.py", "content": "#!/usr/bin/env python3\n\"\"\"Mesure l'écart de contrat S (generateur) / bloc linguistique sur le gold 612.\n\nSortie JSON sur stdout. Ne modifie rien dans le dépôt.\n\"\"\"\nfrom __future__ import annotations\n\nimport collections\nimport json\n … [6846 caractères tronqués]`

  ```
<path>/tmp/mesure_contrat_s.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 /tmp/mesure_contrat_s.py > /tmp/mesure_contrat_s.json 2>/tmp/mesure_contrat_s.err; echo exit=$?; head -c 3000 /tmp/mesure_contrat_s.json; echo; tail -5 /tmp/mesure_contrat_s.err", "description": "Exécuter la mesure sur le gol … [3 caractères tronqués]`

  ```
exit=0
{
 "gold": {
  "phrases": 612
 },
 "bloc_par_categorie": {
  "exact": 145,
  "plus large": 25,
  "aucun": 65,
  "plus étroit": 4
 },
 "s_par_categorie": {
  "plus large": 23,
  "exact": 113,
  "aucun": 99,
  "plus étroit": 4
 },
 "bloc_par_type": {
  "GP": {
   "exact": 83,
   "plus large": 6,
   "aucun": 5,
   "plus étroit": 2
  },
  "SUB": {
   "exact": 36,
   "aucun": 32,
   "plus étroit": 1
  },
  "REL": {
   "exact": 26,
   "aucun": 28,
   "plus large": 19,
   "plus étroit": 1
  }
 },
 "s_par_type": {
  "GP": {
   "plus large": 5,
   "exact": 51,
   "aucun": 39,
   "plus étroit": 1
  },
  "SUB": {
   "exact": 36,
   "aucun": 32,
   "plus étroit": 1
  },
  "REL": {
   "exact": 26,
   "aucun": 28,
   "plus large": 18,
   "plus étroit": 2
  }
 },
 "s_cibles_non_nulles": {
  "cible_nom": 73,
  "cible_verbe": 57
 },
 "s_cibles_justes": {
  "verbe": 54,
  "nom": 43
 },
 "s_cibles_non_nulles_par_type": {
  "GP": {
   "cible_nom": 41,
   "cible_verbe": 34
  },
  "SUB": {
   "cible_verbe": 23,
   "cible_nom": 6
  },
  "REL": {
   "cible_nom": 26
  }
 },
 "s_cibles_justes_par_type": {
  "GP": {
   "verbe": 32,
   "nom": 17
  },
  "SUB": {
   "verbe": 22
  },
  "REL": {
   "nom": 
… [1792 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Analyse fine : convention du gold, cibles S, attachement sur spans exacts

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"Détail : convention du gold, cibles S par tête, attachement du bloc sur spans exacts.\"\"\"\nfrom __future__ import annotations\nimport collections, json, pathlib, sys, unicodedata\nRACINE = pathlib.Path(\"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\")\ … [3432 caractères tronqués]`

  ```
<path>/tmp/mesure_detail.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 /tmp/mesure_detail.py > /tmp/mesure_detail.txt 2>&1; echo exit=$?; head -120 /tmp/mesure_detail.txt", "description": "Mesurer convention gold et cibles S par tête"}`

  ```
exit=0
{
 "gold_convention": {
  "GP|nom": 50,
  "GP|verbe": 46,
  "SUB|verbe": 35,
  "REL|nom": 74,
  "SUB|nom": 34
 },
 "bloc_exact_att": {
  "GP|faux": 14,
  "GP|juste": 69,
  "SUB|juste": 28,
  "REL|juste": 26,
  "SUB|faux": 8
 },
 "s_head": {
  "GP|trouve": 53,
  "SUB|trouve": 37,
  "REL|trouve": 46
 },
 "s_head_span": {
  "GP|diff": 2,
  "GP|exact": 51,
  "SUB|exact": 36,
  "REL|exact": 26,
  "REL|diff": 20,
  "SUB|diff": 1
 },
 "s_head_cible": {
  "GP|juste": 51,
  "SUB|juste": 23,
  "REL|juste": 46,
  "GP|faux": 2,
  "SUB|faux": 14
 },
 "s_head_cible_canal": {
  "GP|nom": 19,
  "GP|verbe": 32,
  "SUB|verbe": 23,
  "REL|nom": 44,
  "GP|aucun": 2,
  "SUB|aucun": 14,
  "REL|verbe": 2
 }
}

EXEMPLES
{
 "GP": [
  {
   "texte": "Le chat de la voisine dort.",
   "gold": {
    "type": "GP",
    "texte": "de la voisine",
    "role": "possession",
    "debut": 8,
    "fin": 21,
    "cibles": [
     "chat"
    ],
    "cible": "chat"
   },
   "pred": "",
   "meta": {
    "role": "theme",
    "niveau": 1,
    "union": true
   },
   "cands": [
    "GP"
   ]
  },
  {
   "texte": "Le canard est prêt à manger.",
   "gold": {
    "type": "GP",
    "texte": "à manger",
    "role": "but",
    
… [672 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Mesure de l'origine des labels, des modes d'échec et du contrôle négatif

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"Détails 2 : origine des labels REL/SUB, modes d'échec, contrôle négatif.\"\"\"\nfrom __future__ import annotations\nimport collections, json, pathlib, sys, unicodedata\nRACINE = pathlib.Path(\"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\")\nsys.path.ins … [4150 caractères tronqués]`

  ```
<path>/tmp/mesure_detail2.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 /tmp/mesure_detail2.py > /tmp/mesure_detail2.txt 2>&1; echo exit=$?; head -200 /tmp/mesure_detail2.txt", "description": "Exécuter mesure détaillée 2"}`

  ```
exit=1
Traceback (most recent call last):
  File "/tmp/mesure_detail2.py", line 74, in <module>
    print(json.dumps({k: {f"{a}|{b}" if isinstance(b, str) else b: n for (a, *b), n in
          ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                          (((a, b) if len((a,)+tuple(b)) == 2 else (a, "|".join(map(str, b)))) if False else ((a, "") if False else (a,)))}
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                      for k, v in []}.items(), ensure_ascii=False))
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib64/python3.13/json/__init__.py", line 242, in dumps
    **kw).encode(obj)
          ~~~~~~^^^^^
  File "/usr/lib64/python3.13/json/encoder.py", line 202, in encode
    chunks = self.iterencode(o, _one_shot=True)
  File "/usr/lib64/python3.13/json/encoder.py", line 263, in iterencode
    return _iterencode(o, 0)
  File "/usr/lib64/python3.13/json/encoder.py", line 182, in default
    raise TypeError(f'Object of type {o.__class__.__name__} '
                    f'is not JSON serializable')
TypeEr
… [55 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'EOF'\np = \"/tmp/mesure_detail2.py\"\ns = open(p).read()\nstart = s.index('print(json.dumps({k: {f\"')\nend = s.index('# sortie brute lisible')\ns = s[:start] + s[end:]\nopen(p, \"w\").write(s)\nEOF\ncd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 / … [156 caractères tronqués]`

  ```
exit=0

## origine_rel_sub
51 ('REL', 'S')
38 ('SUB', 'S')
15 ('REL', 'union')

## cat_marqueur
16 ('REL', 'qui', 'plus large')
14 ('REL', 'that', 'aucun')
14 ('SUB', 'que', 'exact')
9 ('REL', 'que', 'exact')
9 ('SUB', 'that', 'aucun')
6 ('REL', 'dont', 'exact')
6 ('REL', 'ou', 'exact')
6 ('REL', 'where', 'aucun')
5 ('REL', 'qui', 'exact')
5 ('SUB', 'que', 'aucun')
4 ('SUB', 'quand', 'exact')
4 ('SUB', "qu'il", 'exact')
4 ('SUB', 'when', 'aucun')
4 ('SUB', 'because', 'aucun')
3 ('SUB', 'bien', 'exact')
3 ('REL', 'whom', 'aucun')
3 ('SUB', 'although', 'aucun')
3 ('SUB', 'parce', 'exact')
2 ('SUB', "qu'elle", 'exact')
2 ('REL', 'who', 'aucun')
2 ('REL', 'que', 'plus large')
2 ('SUB', 'si', 'exact')
2 ('SUB', 'pendant', 'exact')
2 ('SUB', 'comme', 'exact')
2 ('SUB', 'if', 'aucun')
2 ('SUB', 'while', 'aucun')
2 ('SUB', 'as', 'aucun')
1 ('REL', 'she', 'aucun')
1 ('REL', 'dont', 'plus large')
1 ('REL', 'whose', 'aucun')
1 ('REL', 'when', 'aucun')
1 ('SUB', "qu'il", 'plus étroit')
1 ('REL', 'qui', 'plus étroit')
1 ('SUB', 'car', 'aucun')

## couverture_par_type
36 ('SUB', 'exact', 'SUB')
28 ('REL', 'aucun', 'GV')
26 ('REL', 'exact', 'REL')
26 ('SUB', 'aucun', 'GV')
19 ('REL', 'plus large'
… [1837 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '160,520p' /tmp/mesure_detail2.txt", "description": "Lire exemples REL plus large et SUB"}`

  ```
{
   "texte": "She says that he comes.",
   "gold": {
    "type": "SUB",
    "texte": "that he comes",
    "role": "complément",
    "debut": 9,
    "fin": 22,
    "cibles": [
     "says"
    ],
    "cible": "says"
   },
   "s_cover": [
    {
     "type": "GV",
     "debut": 0,
     "fin": 22,
     "texte": "She says that he comes"
    }
   ],
   "s_all": [
    {
     "type": "GV",
     "debut": 0,
     "fin": 22,
     "texte": "She says that he comes"
    }
   ]
  }
 ],
 "REL|aucun": [
  {
   "texte": "The book that I read is exciting.",
   "gold": {
    "type": "REL",
    "texte": "that I read",
    "role": "qualité",
    "debut": 9,
    "fin": 20,
    "cibles": [
     "book"
    ],
    "cible": "book"
   },
   "s_cover": [
    {
     "type": "GV",
     "debut": 0,
     "fin": 32,
     "texte": "The book that I read is exciting"
    }
   ],
   "s_all": [
    {
     "type": "GV",
     "debut": 0,
     "fin": 32,
     "texte": "The book that I read is exciting"
    }
   ]
  },
  {
   "texte": "The film she talks about is out.",
   "gold": {
    "type": "REL",
    "texte": "she talks about",
    "role": "qualité",
    "debut": 9,
    "fin": 24,
    "cibles": [
     "film"
    ],
   
… [4592 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Mesure des erreurs d'attachement et des canaux `cible_*` de S

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"Détails 3 : erreurs d'attachement du bloc, canaux cible_* de S.\"\"\"\nfrom __future__ import annotations\nimport collections, json, pathlib, sys, unicodedata\nRACINE = pathlib.Path(\"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\")\nsys.path.insert(0, st … [3788 caractères tronqués]`

  ```
<path>/tmp/mesure_detail3.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /tmp && sed -i '/tete_gp = S._segmente/d' mesure_detail3.py && cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 /tmp/mesure_detail3.py > /tmp/mesure_detail3.txt 2>&1; echo exit=$?; head -140 /tmp/mesure_detail3.txt", "description": "Exécuter mesure détaillée 3"}`

  ```
exit=0
== bloc sur span exact (REL/SUB)
26 ('REL', 'exact_span', 'juste')
8 ('SUB', 'exact_span', 'faux')
28 ('SUB', 'exact_span', 'juste')

== SUB erreurs d'attachement span exact 8
[
 {
  "texte": "Quand tu arrives, appelle-moi.",
  "gold": {
   "type": "SUB",
   "texte": "Quand tu arrives",
   "role": "temps",
   "debut": 0,
   "fin": 16,
   "cibles": [
    "appelle"
   ],
   "cible": "appelle"
  },
  "pred": "appelle-moi",
  "pred_type_verbe": false,
  "cible_type_verbe": false
 },
 {
  "texte": "Peut-être qu'il viendra.",
  "gold": {
   "type": "SUB",
   "texte": "qu'il viendra",
   "role": "complément",
   "debut": 10,
   "fin": 23,
   "cibles": [
    "viendra"
   ],
   "cible": "viendra"
  },
  "pred": "Peut-être",
  "pred_type_verbe": false,
  "cible_type_verbe": false
 },
 {
  "texte": "cette douce étoile écoute que Lucas trouve",
  "gold": {
   "type": "SUB",
   "texte": "que Lucas trouve",
   "role": "sub",
   "debut": 26,
   "fin": 42,
   "cibles": [
    "écoute"
   ],
   "cible": "écoute"
  },
  "pred": "étoile",
  "pred_type_verbe": false,
  "cible_type_verbe": true
 },
 {
  "texte": "les rapide lettre cherche que le voyage crie",
  "gold": {
   "type": "SUB",
   "tex
… [1436 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -c \"voisine\" tools/tests/linguistique/gold*.json; grep -o \"Le chat de la voisine[^\\\"]*\" tools/tests/linguistique/gold*.json | head -5", "description": "Chercher le cas antécédent dans un GP"}`

  ```
tools/tests/linguistique/gold_gele.json:3
tools/tests/linguistique/gold.json:3
tools/tests/linguistique/gold_reel.json:0
tools/tests/linguistique/gold_synthetique.json:0
tools/tests/linguistique/gold_gele.json:Le chat de la voisine dort.
tools/tests/linguistique/gold.json:Le chat de la voisine dort.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, pathlib, collections, unicodedata\nbase = pathlib.Path(\"tools/tests/linguistique\")\nph=[]\nfor f in (\"gold.json\",\"gold_reel.json\",\"gold_synthetique.json\"):\n    ph += json.loads((base/f).read_t … [1110 caractères tronqués]`

  ```
('GP', 'gauche') 96
('REL', 'gauche') 74
('SUB', 'dedans') 1
('SUB', 'droite') 26
('SUB', 'gauche') 42

('GP', 'gauche') [('Le chat de la voisine dort.', 'de la voisine', 'chat'), ("La femme a vu l'homme dans le parc.", 'dans le parc', 'vu'), ('Il a couru pour attraper le bus.', 'pour attraper le bus', 'couru'), ('Le chien du voisin aboie la nuit.', 'du voisin', 'chien')]
('SUB', 'gauche') [("Elle a dit qu'elle viendrait hier.", "qu'elle viendrait", 'dit'), ('She said that she would come yesterday.', 'that she would come', 'said'), ('Je pense que tu as raison.', 'que tu as raison', 'pense'), ('I think that you are right.', 'that you are right', 'think')]
('REL', 'gauche') [("Le livre que j'ai lu est intéressant.", "que j'ai lu", 'livre'), ("Le livre que j'ai lu est passionnant.", "que j'ai lu", 'livre'), ('Le film dont elle parle est sorti.', 'dont elle parle', 'film'), ('The book that I read is exciting.', 'that I read', 'book')]
('SUB', 'droite') [('Quand il pleut, je reste.', 'Quand il pleut', 'reste'), ("Bien qu'il soit tard, il travaille.", "Bien qu'il soit tard", 'travaille'), ('When it rains, I stay.', 'When it rains', 'stay'), ('Although it is late, he works.', 'Although it
… [97 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -o \"Le chat de la voisine qui[^\\\"]*\" tools/tests/linguistique/gold*.json | head; echo ---; python3 - <<'EOF'\nimport json, pathlib, collections, unicodedata\nbase=pathlib.Path(\"tools/tests/linguistique\"); ph=[]\nfor f in ( … [1000 caractères tronqués]`

  ```
---
Counter({('REL', 'non'): 74, ('SUB', 'non'): 69})
[]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, pathlib, random, collections, unicodedata\nbase=pathlib.Path(\"tools/tests/linguistique\"); ph=[]\nfor f in (\"gold.json\",\"gold_reel.json\",\"gold_synthetique.json\"):\n    ph += json.loads((base/f). … [786 caractères tronqués]`

  ```
hasard top1 1 239 0.0042
hasard meme type/phrase 239 239 1.0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/structures/generateur.py --json \"Le livre que j'ai lu est passionnant.\" | head -80; echo ===; python3 tools/structures/generateur.py \"Quand il pleut, je reste.\"", "description": "Inspecter la sortie réelle de S"}`

  ```
[
 {
  "nom": "« que j'ai lu » → Le livre",
  "lecture": "« que j'ai lu » se rattache à « Le livre »",
  "attachement": {
   "segment": "que j'ai lu",
   "cible": "Le livre",
   "genre": "GN"
  },
  "segments": [
   {
    "debut": 0,
    "fin": 8,
    "texte": "Le livre",
    "type": "GN",
    "role": "agent",
    "niveau": 1,
    "parent": 2,
    "profondeur": 1
   },
   {
    "debut": 9,
    "fin": 20,
    "texte": "que j'ai lu",
    "type": "REL",
    "role": "qualite",
    "niveau": 1,
    "parent": 0,
    "profondeur": 2
   },
   {
    "debut": 21,
    "fin": 36,
    "texte": "est passionnant",
    "type": "GV",
    "role": "predicat",
    "niveau": 0,
    "parent": null,
    "profondeur": 0
   }
  ]
 }
]
===
- structure la plus proche
     'Quand il pleut' [SUB · temps]
   'je reste' [GV · predicat]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, json\nsys.path.insert(0,\"tools\"); sys.path.insert(0,\"tools/structures\")\nimport generateur as S\nfor t in [\"Le livre que j'ai lu est passionnant.\", \"Quand il pleut, je reste.\",\n          \"Le c … [462 caractères tronqués]`

  ```
== Le livre que j'ai lu est passionnant.
  GN    0- 8 'Le livre'                                    role=agent        nom=None gp=None verbe=None parent=2 prof=1
  REL   9-20 "que j'ai lu"                                 role=qualite      nom='Le livre' gp=None verbe=None parent=0 prof=2
  GV   21-36 'est passionnant'                             role=predicat     nom='Le livre' gp=None verbe=None parent=None prof=0
  dict: {"debut": 0, "fin": 8, "texte": "Le livre", "type": "GN", "role": "agent", "niveau": 1, "parent": 2, "profondeur": 1}
== Quand il pleut, je reste.
  SUB   0-14 'Quand il pleut'                              role=temps        nom=None gp=None verbe=None parent=1 prof=1
  GV   16-24 'je reste'                                    role=predicat     nom=None gp=None verbe=None parent=None prof=0
  dict: {"debut": 0, "fin": 14, "texte": "Quand il pleut", "type": "SUB", "role": "temps", "niveau": 1, "parent": 1, "profondeur": 1}
== Le chat que j'ai vu dormait.
  GN    0- 7 'Le chat'                                     role=agent        nom=None gp=None verbe=None parent=None prof=0
  REL   8-27 "que j'ai vu dormait"                         role=qualite      nom='Le chat' 
… [575 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Répartition par langue et couverture des canaux de cibles

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, json, pathlib, collections, unicodedata\nsys.path.insert(0,\"tools\"); sys.path.insert(0,\"tools/structures\")\nimport bloc_linguistique as bl, generateur as S\nbase=pathlib.Path(\"tools/tests/linguisti … [1981 caractères tronqués]`

  ```
== REL/SUB échecs par langue
28 ('REL', 'en', 'aucun')
26 ('REL', 'fr', 'exact')
19 ('REL', 'fr', 'plus large')
1 ('REL', 'fr', 'plus étroit')
26 ('SUB', 'en', 'aucun')
6 ('SUB', 'fr', 'aucun')
36 ('SUB', 'fr', 'exact')
1 ('SUB', 'fr', 'plus étroit')

== canaux cible_* par type de segment S (tous segments)
252 ('GN', 'aucune')
1 ('GN', 'gp')
34 ('GN', 'nom')
55 ('GN', 'verbe')
56 ('GP', 'nom')
51 ('GP', 'verbe')
360 ('GV', 'aucune')
3 ('GV', 'gp')
180 ('GV', 'nom')
97 ('GV', 'verbe')
49 ('REL', 'nom')
2 ('REL', 'verbe')
13 ('SUB', 'aucune')
6 ('SUB', 'nom')
25 ('SUB', 'verbe')

types S {'GN': 315, 'GV': 619, 'GP': 78, 'SUB': 38, 'REL': 51}
  ```

### 🤖 Assistant

⏵ Recherche du contrat existant de S et du vocabulaire du dépôt

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rln \"generateur\\|générateur S\\|structures/generateur\" docs/ --include=\"*.md\" | head -20", "description": "Chercher docs sur le générateur S"}`

  ```
docs/pilotage/plan-travail.md
docs/pilotage/roadmap.md
docs/theorie/pre-traitement-linguistique.md
docs/implantation/moteur-de-pensee.md
docs/implantation/bloc-linguistique.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"cible_nom\\|cible_gp\\|cible_verbe\\|_syntagmes_s\\|_cibles_s\" --include=\"*.py\" --include=\"*.md\" . | grep -v \"/journal/\" | head -40", "description": "Trouver tous les consommateurs des cibles S"}`

  ```
./reports/rapport-pensee-segmenteur.md:53:- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — `_syntagmes_simple`, `_syntagmes_s`.
./reports/rapport-pensee-passifs-sans-par.md:16:| `_syntagmes_simple` (chunker, mon code) | **patient** | ✅ corrigé |
./reports/rapport-pensee-passifs-sans-par.md:20:| test | `_syntagmes_simple` |
./reports/rapport-pensee-passifs-sans-par.md:59:- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — `_syntagmes_simple` (passif).
./reports/rapport-pensee-cible-proximite.md:43:- **Le coût** : la règle ajoute un `_syntagmes_simple` par segment dans le chemin chunker (à
./reports/rapport-pensee-echecs-attachement.md:44:  chunker, pas de `cible_verbe` pour ces phrases).
./tools/llm/prompts_publics.py:72:                         "cible_iso3": iso3, "cible_nom": nom, "reference": reference,
./tools/structures/generateur.py:294:    __slots__ = ("debut", "fin", "type", "role", "niveau", "texte", "cible_nom", "cible_gp",
./tools/structures/generateur.py:295:                 "cible_verbe", "parent", "profondeur")
./tools/structures/generateur.py:300:        self.cible_nom = None   # le GN le plus proche à gauche
./tools/structures/generateur.py:301:   
… [2832 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n -i -B3 -A12 \"générateur\\|generateur\\|structures/\" docs/implantation/bloc-linguistique.md | head -80", "description": "Lire le contrat du bloc sur S"}`

  ```
21-  maths, figure) — c'est du **document**, pas du mot ni de la phrase ;
22-- **R4.1–R4.4** lisent la **structure** (tableaux, code, maths, scans) — c'est de la forme, pas
23-  de la langue ;
24:- la **coloration** (`tools/structures/generateur.py`) segmente en GN/GV/GP/REL/SUB, devine des
25:  rôles et produit des **candidats d'attachement** — c'est un générateur de candidats français,
26-  un banc de validation humaine, pas un bloc avec un contrat, une trace et une porte.
27-
28-Il manquait le **bloc** : un objet typé qui prend un texte, rend une **annotation** multi-niveaux
29-avec `source`, `confiance` et `candidats`, et que l'on peut remplacer par une version neuronale
30-sans changer le consommateur. C'est ce que spécifie ce document.
31-
32-## 2. Les neuf niveaux
33-
34-![Les neuf niveaux du bloc](../schemas/bloc-linguistique-niveaux.svg)
35-
36-| niveau | ce qu'on étiquette | heuristique CPU | neuronal | ce que le consommateur en fait |
37-|---|---|---|---|---|
--
113-  nombres, et des **candidats** de classe ouverte par suffixe ; une classe ouverte est marquée
114-  `ouvert` et devient une **unité sémantique** ;
115-- **morphème** : des suffixes et préfixes productifs, en
… [2302 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n -i -B3 -A15 \"cible\\|generateur\\|générateur\" docs/implantation/moteur-de-pensee.md | head -120", "description": "Lire le doc moteur sur les cibles"}`

  ```
254-| **T82** | la pénalité -1 casse-t-elle le cycle ? | 0/20 au but 0, (3,0) stale 1,517 | non : la pénalité ne suffit pas |
255-| **T83** | où est le seuil sur 20 graines ? | 20 % à 0,35, 100 % à 0,41 | le seuil est ~0,41, gradué |
256-| **T84** | où est le bord fin ? | 73 % à 0,38, 100 % à 0,41 (400 essais) | le seuil robuste est 0,41 |
257:| **T85** | le gold à 200 réels tient-il ? | POS 0,7738, 1 782 tokens, 200 phrases | la cible 200 est atteinte |
258-| **T86** | les 20 nouvelles sont-elles meilleures ? | POS 0,8214 contre 0,7897 | POS mieux, syntagme moins bien |
259-| **T87** | les phrases complexes tiennent-elles ? | POS 0,6471, syntagme 0,4828 | POS ouvert en baisse, segments mieux |
260-| **T88** | les 20 complexes confirment-ils ? | POS 0,6829, syntagme 0,2963 | les deux effets se modèrent |
261-| **T89** | les 50 complexes stabilisent-ils ? | POS 0,7013, syntagme 0,3060 | −0,09 / +0,12 se stabilisent |
262-| **T90** | les 100 complexes tiennent-ils ? | POS 0,6984, syntagme 0,2677 | POS stable, syntagme +0,08 |
263-| **T91** | le discours tient-il ? | acte 0,9, négation 1,0, modalité 0,9 | les actes simples manquent |
264-| **T92** | l'anaphore tient-elle ? | 4/4 liens
… [10104 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture du style des JSON de fiches existants

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -c \"\nimport json\nfor f in ('reports/pensee-spans.json','reports/pensee-echecs-attachement.json','reports/pensee-attachement-cible.json'):\n    d=json.load(open(f)); print('==',f); print(json.dumps(d,ensure_ascii=False,inde … [80 caractères tronqués]`

  ```
== reports/pensee-spans.json
{
 "date": "2026-11-05",
 "ligne": "B13",
 "portes": "169/169",
 "gold": 612,
 "cibles": 239,
 "spans": {
  "REL": 48,
  "SUB": 33,
  "GP": 12,
  "total": 93
 },
 "categories": {
  "aucun": 65,
  "plus_large": 25,
  "plus_etroit": 3,
  "coupe": 1
 },
 "avant": {
  "labels": 145,
  "couverture": 0.6067,
  "f1": 0.2864,
  "span": 94,
  "cible": 13
 },
 "apres": {
  "labels": 146,
  "couverture": 0.6109,
  "f1": 0.2869,
  "span": 93,
  "cible": 14
 },
 "limites": [
  "81 REL/SUB chez S",
  "dénominateur de l'attachement à corriger",
  "gold 612"
 ]
}

== reports/pensee-echecs-attachement.json
{
 "date": "2026-11-04",
 "ligne": "B13",
 "portes": "166/166",
 "echecs": {
  "span": 94,
  "cible_avant": 33,
  "cible_apres": 32,
  "total_avant": 127,
  "total_apres": 126
 },
 "avant": {
  "top1": 95,
  "topk": 112,
  "exact": 13,
  "tete_top1": 94,
  "tete_topk": 111
 },
 "apres": {
  "top1": 96,
  "topk": 113,
  "exact": 14,
  "tete_top1": 96,
  "tete_topk": 113
 },
 "cause_32": "le GV couvre la phrase : le dernier token n'est pas le verbe",
 "limites": [
  "les 94 spans non qualifiés",
  "pas d'identification du verbe",
  "gold 612"
 ]
}

== reports/pensee-att
… [660 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Contrôles négatifs : baselines et test de permutation

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, json, pathlib, collections, unicodedata, random\nsys.path.insert(0,\"tools\"); sys.path.insert(0,\"tools/structures\")\nimport bloc_linguistique as bl, generateur as S\nbase=pathlib.Path(\"tools/tests/l … [3466 caractères tronqués]`

  ```
invariant texte S 0 / 1101
invariant texte gold 0 / 1863
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 43, in <module>
  File "<stdin>", line 43, in <lambda>
TypeError: 'Segment' object is not subscriptable
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, json, pathlib, collections, unicodedata, random\nsys.path.insert(0,\"tools\"); sys.path.insert(0,\"tools/structures\")\nimport bloc_linguistique as bl, generateur as S\nbase=pathlib.Path(\"tools/tests/l … [2722 caractères tronqués]`

  ```
baselines REL {'REL|exact|premier_GN': 26, 'REL|exact|plus_proche_GN': 26, 'REL|exact|total': 26}
permutation 74 REL : moyenne 1.31 p95 3 max 6 observé 44

== rôles REL/SUB (type, S, gold) top
10 ('REL', 'qualite', 'objet')
10 ('SUB', 'contenu', 'sub')
9 ('SUB', 'contenu', 'complement')
7 ('REL', 'qualite', 'qualite')
6 ('SUB', 'temps', 'temps')
5 ('REL', 'qualite', 'sujet')
5 ('SUB', 'cause', 'cause')
3 ('SUB', 'concession', 'concession')
3 ('REL', 'qualite', 'lieu')
2 ('SUB', 'hypothese', 'condition')
1 ('SUB', 'contenu', 'contenu')
1 ('REL', 'qualite', 'temps')
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, json, pathlib, collections, unicodedata\nsys.path.insert(0,\"tools\"); sys.path.insert(0,\"tools/structures\")\nimport bloc_linguistique as bl, generateur as S\nbase=pathlib.Path(\"tools/tests/linguisti … [1760 caractères tronqués]`

  ```
phrases 612 chevauchements 0 doublons 0 parents invalides 0
roles {('SUB', True, 'contenu'): 1, ('REL', True, 'qualite'): 7, ('REL', False, 'sujet'): 5, ('SUB', False, 'complement'): 9, ('REL', False, 'objet'): 10, ('SUB', True, 'temps'): 6, ('SUB', True, 'concession'): 3, ('REL', False, 'lieu'): 3, ('SUB', False, 'condition'): 2, ('SUB', True, 'cause'): 5, ('REL', False, 'temps'): 1, ('SUB', False, 'sub'): 10}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, json, pathlib, collections, unicodedata\nsys.path.insert(0,\"tools\"); sys.path.insert(0,\"tools/structures\")\nimport bloc_linguistique as bl, generateur as S\nbase=pathlib.Path(\"tools/tests/linguisti … [1866 caractères tronqués]`

  ```
1 ('REL', 'hand', 'fr', 'exact')
28 ('REL', 'reel', 'en', 'aucun')
25 ('REL', 'reel', 'fr', 'exact')
3 ('REL', 'reel', 'fr', 'plus large')
1 ('REL', 'reel', 'fr', 'plus étroit')
16 ('REL', 'synthetique', 'fr', 'plus large')
1 ('SUB', 'hand', 'en', 'aucun')
1 ('SUB', 'hand', 'fr', 'exact')
25 ('SUB', 'reel', 'en', 'aucun')
1 ('SUB', 'reel', 'fr', 'aucun')
25 ('SUB', 'reel', 'fr', 'exact')
1 ('SUB', 'reel', 'fr', 'plus étroit')
5 ('SUB', 'synthetique', 'fr', 'aucun')
10 ('SUB', 'synthetique', 'fr', 'exact')

FR SUB absent
('reel', 'Je pars car il est tard.', 'car il est tard', 'pars', [('GV', 'Je pars'), ('GV', 'il est'), ('GP', 'tard')])
('synthetique', 'ma fenêtre marche que les fenêtre ouvre', 'que les fenêtre ouvre', 'marche', [('GN', 'ma fenêtre marche'), ('REL', 'que les fenêtre ouvre')])
('synthetique', 'une fenêtre nage que ils crie', 'que ils crie', 'nage', [('GN', 'une fenêtre nage'), ('REL', 'que ils crie')])
('synthetique', 'la brillante forêt nage que Lucas ferme', 'que Lucas ferme', 'nage', [('GN', 'la brillante forêt nage'), ('REL', 'que Lucas ferme')])
('synthetique', 'ce doux nuage dessine que les avocat compte', 'que les avocat compte', 'dessine', [('GN', 'ce doux n
… [719 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, json, pathlib, collections\nsys.path.insert(0,\"tools\"); sys.path.insert(0,\"tools/structures\")\nimport bloc_linguistique as bl, generateur as S\nbase=pathlib.Path(\"tools/tests/linguistique\"); ph=[] … [1384 caractères tronqués]`

  ```
{('gauche', 'juste'): 16, ('droite', 'juste'): 12, ('droite', 'faux'): 1, ('dedans', 'faux'): 1, ('gauche', 'faux'): 6} total 36
  ```

### 🤖 Assistant

⏵ Reproduction indépendante via l'évaluateur du dépôt

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 300 python3 tools/tests/linguistique/evaluer_gold.py --json /tmp/eval_gold.json > /tmp/eval_gold.out 2>&1; echo exit=$?; tail -5 /tmp/eval_gold.out; python3 - <<'EOF'\nimport json\nd=json.load(open(\"/tmp/eval_gold.json\"))\n … [288 caractères tronqués]`

  ```
exit=0
    "exactitude_ouvert": 0.6061,
    "tokens": 2480,
    "confusions": {
     "ADJ"
heuristique all: {"pos": {"exactitude": 0.7455, "exactitude_ferme": 0.8984, "exactitude_ouvert": 0.6007, "tokens": 3179, "confusions": {"ADJ": {"ADJ": 50, "NOUN": 80, "VERB": 4}, "ADV": {"ADV": 117, "NOUN": 21, "PREP": 1, "ADJ": 1, "?": 1}, "AUX": {"PREP": 4, "AUX": 118, "?": 3, "NOUN": 3}, "CONJ": {"CONJ": 44, "PRON": 25, "DET": 12, "?": 13, "PREP": 2, "NOUN": 2}, "DET": {"DET": 586, "?": 2}, "NOUN": {"NOUN": 617, "ADJ": 17, "VERB": 47, "?": 1}, "NUM": {"NUM": 2}, "PONCT": {"?": 25}, "PREP": {"PREP": 111, "NOUN": 3}, "PRON": {"PRON": 411, "NOUN": 8, "?": 30, "DET": 25, "CONJ": 1}, "VERB": {"VERB": 314, "NOUN": 447, "ADJ": 5, "PREP": 2, "?": 16, "AUX": 7, "ADV": 1}}}, "syntagme": {"precision": 0.3154, "rappel": 0.2619, "f1": 0.2862, "tp": 488, "fp": 1059, "fn": 1375, "tete": {"precision": 0.5862, "rappel": 0.4342, "f1": 0.4989, "tp": 809, "fp": 571, "fn": 1054}}, "pragmatique": {"acte": 0.9967, "negation": 0.9771, "modalite": 0.9886, "double_sens": 0.9444}, "fraction_semantique": 0.5551}
{
 "gold": {
  "phrases": 612,
  "reel": 452,
  "hand": 20,
  "reel_new": 432,
  "synthetique": 160,
  "to
… [824 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,80p' reports/rapport-pensee-convention-doc.md 2>/dev/null; echo ===; sed -n '1,60p' reports/rapport-pensee-cible-proximite.md", "description": "Lire la convention documentée"}`

  ```
# B13 — la convention des cibles est documentée dans le gold

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
> **177/177 portes** : le gold ne disait pas ce qu'était une `cible` ; la lecture des données
> (T169, T172) est désormais **écrite dans le gold** (`CONVENTION_CIBLE`) et vérifiée par une
> porte. REL/SUB → **antécédent** (tête du GN à gauche) ; GP → **verbe gouverneur**, ou **nom
> complété** pour un génitif ; GN/GV → nom ou verbe dont le segment dépend.
>
> **Dispositif** : [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-convention-doc.json`](pensee-convention-doc.json).

## 1. Ce qui est écrit

| type | convention de la cible |
|---|---|
| **REL** | antécédent (tête du GN à gauche) |
| **SUB** | antécédent (tête du GN à gauche) |
| **GP** | verbe gouverneur ; nom complété pour un génitif |
| **GN / GV** | nom ou verbe dont le segment dépend |

**Ce que ça dit** :

- **Deux conventions coexistent** dans le même champ : c'est mesuré (63 cibles verbes, 82 noms
  sur 145 segments) 
… [4580 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Classification des cibles par le POS du gold (plus fiable que le lexique)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, pathlib, collections, unicodedata\nbase=pathlib.Path(\"tools/tests/linguistique\"); ph=[]\nfor f in (\"gold.json\",\"gold_reel.json\",\"gold_synthetique.json\"):\n    ph += json.loads((base/f).read_tex … [1233 caractères tronqués]`

  ```
73 ('REL', 'gauche', 'NOUN')
1 ('REL', 'gauche', 'PRON')
1 ('SUB', 'dedans', 'VERB')
26 ('SUB', 'droite', 'VERB')
42 ('SUB', 'gauche', 'VERB')

74 ('REL', 'gauche', 'nom/autre')
1 ('SUB', 'dedans', 'verbe')
26 ('SUB', 'droite', 'verbe')
42 ('SUB', 'gauche', 'verbe')
  ```

### 🤖 Assistant

⏵ Lecture de la convention écrite dans le gold

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n -B3 -A22 \"CONVENTION_CIBLE\" tools/tests/linguistique/gold_reel.py | head -60", "description": "Lire CONVENTION_CIBLE"}`

  ```
22-# Deux conventions coexistent donc dans le même champ `cible` : la mesure les publie
23-# séparément (`evaluer_gold` → `attachement.verbe` / `attachement.nom`) et le taux global
24-# n'est comparable qu'à convention constante.
25:CONVENTION_CIBLE = {
26-    "REL": "antécédent (tête du GN à gauche)",
27-    "SUB": "antécédent (tête du GN à gauche)",
28-    "GP": "verbe gouverneur, ou nom complété pour un génitif",
29-    "GN": "nom ou verbe dont le segment dépend",
30-    "GV": "nom ou verbe dont le segment dépend",
31-    "note": "deux conventions dans le même champ ; mesurées séparément (verbe / nom)",
32-}
33-
34-PHRASES = [
35-    ("r001", "fr", "Le chien mange une pomme.",
36-     [("Le", "DET"), ("chien", "NOUN"), ("mange", "VERB"), ("une", "DET"), ("pomme", "NOUN")],
37-     [("GN", "Le chien", "agent"), ("GV", "mange", "prédicat"), ("GN", "une pomme", "patient")], {"acte": "assertion"}),
38-    ("r002", "fr", "La fille lit le journal.",
39-     [("La", "DET"), ("fille", "NOUN"), ("lit", "VERB"), ("le", "DET"), ("journal", "NOUN")],
40-     [("GN", "La fille", "agent"), ("GV", "lit", "prédicat"), ("GN", "le journal", "patient")], {"acte": "assertion"}),
41-    ("r003", "fr
… [486 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Simulation de la règle SUB → verbe gouverneur sur les spans exacts

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, json, pathlib, collections, unicodedata\nsys.path.insert(0,\"tools\"); sys.path.insert(0,\"tools/structures\")\nimport bloc_linguistique as bl, generateur as S\nbase=pathlib.Path(\"tools/tests/linguisti … [1508 caractères tronqués]`

  ```
règle SUB/GP -> _cible_proche (verbe du GV le plus proche), spans exacts
{('SUB', 'juste'): 2, ('REL', 'faux'): 26, ('SUB', 'faux'): 34}
exemples faux [('Je pense que tu as raison.', 'pense', None), ('Quand il pleut, je reste.', 'reste', None), ("Elle dit qu'il vient.", 'dit', None), ("Bien qu'il soit tard, il travaille.", 'travaille', None), ('Je sais que tu viens.', 'sais', None), ('Il faut que tu partes.', 'faut', None), ('Si tu viens, nous partirons.', 'partirons', None), ("Elle chante parce qu'elle est heureuse.", 'chante', 'est')]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, json, pathlib, collections, unicodedata\nsys.path.insert(0,\"tools\"); sys.path.insert(0,\"tools/structures\")\nimport bloc_linguistique as bl, generateur as S\nbase=pathlib.Path(\"tools/tests/linguisti … [1712 caractères tronqués]`

  ```
{('SUB', 'juste'): 34, ('REL', 'faux'): 26, ('SUB', 'faux'): 2}
exemples faux [('Quand tu arrives, appelle-moi.', 'appelle', 'appelle-moi'), ("Peut-être qu'il viendra.", 'viendra', 'Peut-être')]
  ```

### 🤖 Assistant

⏵ Vérification d'une incohérence de comptage par source

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, json, pathlib, collections\nsys.path.insert(0,\"tools\"); sys.path.insert(0,\"tools/structures\")\nimport bloc_linguistique as bl, generateur as S\nbase=pathlib.Path(\"tools/tests/linguistique\"); ph=[] … [992 caractères tronqués]`

  ```
{('SUB', 'hand', 'exact'): 1, ('REL', 'hand', 'exact'): 1, ('SUB', 'hand', 'non'): 1, ('REL', 'reel', 'exact'): 25, ('REL', 'reel', 'non'): 32, ('SUB', 'reel', 'exact'): 25, ('SUB', 'reel', 'non'): 27, ('REL', 'synthetique', 'non'): 16, ('SUB', 'synthetique', 'exact'): 10, ('SUB', 'synthetique', 'non'): 5}
synthetic REL exact 0
  ```

### 🤖 Assistant

⏵ Consolidation de tous les chiffres cités dans une synthèse unique

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"Synthèse chiffrée du contrat L↔S (REL/SUB). Sortie JSON.\"\"\"\nfrom __future__ import annotations\nimport collections, json, pathlib, random, sys, unicodedata\nRACINE = pathlib.Path(\"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\")\nsys.path.insert(0, s … [8185 caractères tronqués]`

  ```
<path>/tmp/synthese_contrat.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 /tmp/synthese_contrat.py > /tmp/synthese_contrat.json 2>/tmp/synthese_contrat.err; echo exit=$?; python3 - <<'EOF'\nimport json\nd=json.load(open(\"/tmp/synthese_contrat.json\"))\nfor k in (\"gold\",\"gold_cibles_par_type\",\ … [392 caractères tronqués]`

  ```
exit=1
  File "/usr/lib64/python3.13/json/encoder.py", line 263, in iterencode
    return _iterencode(o, 0)
TypeError: keys must be str, int, float, bool or None, not tuple
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
  File "/usr/lib64/python3.13/json/__init__.py", line 298, in load
    return loads(fp.read(),
        cls=cls, object_hook=object_hook,
        parse_float=parse_float, parse_int=parse_int,
        parse_constant=parse_constant, object_pairs_hook=object_pairs_hook, **kw)
  File "/usr/lib64/python3.13/json/__init__.py", line 352, in loads
    return _default_decoder.decode(s)
           ~~~~~~~~~~~~~~~~~~~~~~~^^^
  File "/usr/lib64/python3.13/json/decoder.py", line 345, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
               ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib64/python3.13/json/decoder.py", line 363, in raw_decode
    raise JSONDecodeError("Expecting value", s, err.value) from None
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'EOF'\np=\"/tmp/synthese_contrat.py\"\ns=open(p).read()\nold='''print(json.dumps(out, ensure_ascii=False, indent=1, default=deep))'''\nnew='''def clean(o):\n    if isinstance(o, dict):\n        return {(k if isinstance(k, str) else \"|\".join(map(str, k)) if isins … [575 caractères tronqués]`

  ```
exit=0
{
 "gold": {
  "phrases": 612,
  "par_source": {
   "hand": 20,
   "reel": 432,
   "synthetique": 160
  },
  "segments": 1863,
  "cibles": 239
 },
 "gold_cibles_par_type": {
  "GP": 96,
  "SUB": 69,
  "REL": 74
 },
 "gold_rel_sub_par_source": {
  "hand|SUB": 2,
  "hand|REL": 1,
  "reel|REL": 57,
  "reel|SUB": 52,
  "synthetique|REL": 16,
  "synthetique|SUB": 15
 },
 "bloc": {
  "exact": 145,
  "plus large": 25,
  "aucun": 65,
  "plus étroit": 4
 },
 "bloc_type": {
  "GP": {
   "exact": 83,
   "plus large": 6,
   "aucun": 5,
   "plus étroit": 2
  },
  "SUB": {
   "exact": 36,
   "aucun": 32,
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nd=json.load(open(\"/tmp/synthese_contrat.json\"))\nfor k in (\"bloc_type\",\"s\",\"s_type\",\"bloc_source\",\"s_source\",\"rel_sub\",\"canaux\",\"canaux_justes\",\"regle_actuelle\",\"regle_verbe\",\"ne … [171 caractères tronqués]`

  ```
== bloc_type
{
 "GP": {
  "exact": 83,
  "plus large": 6,
  "aucun": 5,
  "plus étroit": 2
 },
 "SUB": {
  "exact": 36,
  "aucun": 32,
  "plus étroit": 1
 },
 "REL": {
  "exact": 26,
  "aucun": 28,
  "plus large": 19,
  "plus étroit": 1
 }
}
== s
{
 "plus large": 23,
 "exact": 113,
 "aucun": 99,
 "plus étroit": 4
}
== s_type
{
 "GP": {
  "plus large": 5,
  "exact": 51,
  "aucun": 39,
  "plus étroit": 1
 },
 "SUB": {
  "exact": 36,
  "aucun": 32,
  "plus étroit": 1
 },
 "REL": {
  "exact": 26,
  "aucun": 28,
  "plus large": 18,
  "plus étroit": 2
 }
}
== bloc_source
{
 "hand|exact": 10,
 "hand|plus large": 1,
 "hand|aucun": 2,
 "reel|exact": 105,
 "reel|aucun": 58,
 "reel|plus étroit": 4,
 "reel|plus large": 4,
 "synthetique|exact": 30,
 "synthetique|plus large": 20,
 "synthetique|aucun": 5
}
== s_source
{
 "hand|plus large": 2,
 "hand|exact": 8,
 "hand|aucun": 3,
 "reel|exact": 77,
 "reel|aucun": 88,
 "reel|plus étroit": 4,
 "reel|plus large": 2,
 "synthetique|aucun": 8,
 "synthetique|exact": 28,
 "synthetique|plus large": 19
}
== rel_sub
{
 "SUB|fr|exact": 36,
 "REL|fr|exact": 26,
 "SUB|en|aucun": 26,
 "REL|en|aucun": 28,
 "REL|fr|plus large": 19,
 "SUB|fr|plus étroit": 1,
 "REL|f
… [804 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Identification des cas limites (REL pronom, SUB interne)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, pathlib, unicodedata\nbase=pathlib.Path(\"tools/tests/linguistique\"); ph=[]\nfor f,src in ((\"gold.json\",\"hand\"),(\"gold_reel.json\",\"reel\"),(\"gold_synthetique.json\",\"synthetique\")):\n    for … [1025 caractères tronqués]`

  ```
SUB dedans VERB | Peut-être qu'il viendra. | seg: qu'il viendra | cible: viendra
REL gauche PRON | elle qui commence nage | seg: qui commence | cible: elle
  ```

### 🤖 Assistant

⏵ Vérification que les deux fichiers cibles n'existent pas déjà

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -l reports/rapport-contrat-s.md reports/pensee-contrat-s.json 2>&1; git status --short reports/ | head", "description": "Vérifier l'absence des fichiers cibles"}`

  ```
ls: cannot access 'reports/rapport-contrat-s.md': No such file or directory
ls: cannot access 'reports/pensee-contrat-s.json': No such file or directory
 M reports/README.md
 M reports/pensee-quatre-modes.json
 M reports/pensee-spans.json
 M reports/rapport-pensee-spans.md
?? reports/pensee-audit-attachement.json
?? reports/pensee-topk-diagnostic.json
?? reports/rapport-audit-attachement.md
?? reports/rapport-s-paragraphes.md
?? reports/rapport-topk-diagnostic.md
  ```

### 🤖 Assistant

⏵ Rédaction de la fiche `reports/rapport-contrat-s.md`

- **write** `{"content": "# B13 — Contrat d'interface L ↔ S : les subordonnées REL/SUB\n\n> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅\n> mesure faite — le contrat `s/v1` **n'est pas tenu** par S aujourd'hui. **Aucun code modifié** :\n> `tools/structures/ … [23111 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

### 🤖 Assistant

⏵ Corrections factuelles de la fiche (arithmétique du gold, canal REL, 93 vs 94)

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md", "old_string": "- **Le gold** : 612 phrases, dont 160 synthétiques ; 452 réelles + 20 `gold.py`. Les 16 REL larges\n  synthétiques gonflent l'effet « plus large » ; sur le réel seul, **52/112** spans exacts  … [395 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md", "old_string": "- **Le 93 de la fiche précédente** ([`rapport-pensee-spans.md`](rapport-pensee-spans.md)) est le\n  même gold après le bornage du GP et avec l'ancien lexique ; l'arbre courant donne **94**\n  … [452 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md", "old_string": "tête** (même `debut`, quelle que soit la `fin`), S trouve **46/74 REL** et **37/69 SUB** ; parmi\nles trouvées, la cible nominale est juste **46/46** pour REL et la cible verbale **23/37** po … [622 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md has been updated successfully.
  ```

### 🤖 Assistant

⏵ Écriture du JSON `reports/pensee-contrat-s.json` (structuré et validé)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json, pathlib\n\nd = {\n \"date\": \"2026-11-05\",\n \"ligne\": \"B13\",\n \"objet\": \"contrat d'interface L (bloc_linguistique) ↔ S (structures/generateur) pour les subordonnées REL/SUB\",\n \"verdict\": \" … [11173 caractères tronqués]`

  ```
écrit reports/pensee-contrat-s.json 10785 octets
JSON valide
  ```

### 🤖 Assistant

⏵ Relecture de la fiche et validation du JSON

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md</path>
<type>file</type>
<content>
1: # B13 — Contrat d'interface L ↔ S : les subordonnées REL/SUB
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
4: > mesure faite — le contrat `s/v1` **n'est pas tenu** par S aujourd'hui. **Aucun code modifié** :
5: > `tools/structures/` reste intact ; cette fiche est une spécification, pas un correctif.
6: > **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
7: > [`generateur.py`](../tools/structures/generateur.py),
8: > [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) rejoué (`ok: true`, **labels
9: > 145, exact 123, exactitude spans 0,8483, hasard 0,0042**).
10: > **Le chiffre** : sur **239** cibles d'attachement du gold, **94** n'ont pas de segment prédit au
11: > bon span — **48 REL, 33 SUB, 13 GP**. **81** sont des REL/SUB : **60 absentes**, **19 plus
12: > larges**, **2 plus étroites**. Le bloc ne répare aucune des 81 ; S seul place **62/143** spans
13: > REL/SUB (43,4 %). L'interface réelle est **privée** (`_segmente`, `_tokens`) et **incomplète**
14: > (pas 
… [23618 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Corrections de précision (surfaces publiques, ligne source, formulations)

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md", "new_string": "S n'expose aujourd'hui que deux surfaces publiques, et aucune ne porte le contrat complet ; le\nbloc complète avec une troisième, privée :", "old_string": "S n'expose aujourd'hui que deux sur … [48 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md", "new_string": "nominale, alors que la mesure (§ 4, POS du gold) montre que le gold veut un **antécédent\nnominal** pour REL (74/74) et un **verbe gouverneur** pour SUB (69/69).", "old_string": "nominale, al … [140 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md", "new_string": "  (`Le livre`), `cible.tete` = sa tête (`livre`). Gold : **74/74** cibles sont un antécédent\n  nominal (73 `NOUN`, 1 `PRON`) à gauche. C'est le seul **type** où la règle « tête du GN à\n  ga … [222 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md", "new_string": "  `direction = \"gauche\"`. Le canal `cible_gp` actuel n'est **pas** ce champ : c'est la tête du GP\n  le plus proche à gauche, il vaut `None` sur 1097/1101 segments et **0/89** REL/SUB — il  … [266 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md", "new_string": "| reel | 109 | 50 | 59 (53 anglais + 6 français) |", "old_string": "| reel | 109 | 50 | 59 (54 anglais + 5 français) |"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md", "new_string": "| **POS gold vs `CONVENTION_CIBLE`** | SUB : **69/69 VERB** (42 gauche, 26 droite, 1 interne) ; REL : 73 NOUN + 1 PRON, à gauche | la convention écrite (`gold_reel.py:25-32`, « SUB → antécéde … [521 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md", "new_string": "- **Le 93 de la fiche précédente** ([`rapport-pensee-spans.md`](rapport-pensee-spans.md)) est le\n  même gold après le bornage du GP ; l'arbre courant donne **94** (13 GP), pas 93 (12 GP). L' … [523 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md has been updated successfully.
  ```

### 🤖 Assistant

⏵ Vérification des deux derniers chiffres (union et larges par source)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, json, pathlib, collections\nsys.path.insert(0,\"tools\"); sys.path.insert(0,\"tools/structures\")\nimport bloc_linguistique as bl, generateur as S\nbase=pathlib.Path(\"tools/tests/linguistique\"); ph=[] … [1875 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 23, in <module>
  File "<stdin>", line 9, in cat
TypeError: 'Etiquette' object is not subscriptable
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, json, pathlib, collections\nsys.path.insert(0,\"tools\"); sys.path.insert(0,\"tools/structures\")\nimport bloc_linguistique as bl, generateur as S\nbase=pathlib.Path(\"tools/tests/linguistique\"); ph=[] … [1943 caractères tronqués]`

  ```
union REL/SUB {('REL', 'plus large'): 5, ('REL', 'sans_gold'): 10} total 15
S REL larges par source {'reel': 2, 'synthetique': 16} total 18
S REL étroites par source {'reel': 2} total 2
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, json, pathlib\nsys.path.insert(0,\"tools\"); sys.path.insert(0,\"tools/structures\")\nimport bloc_linguistique as bl, generateur as S\nbase=pathlib.Path(\"tools/tests/linguistique\"); ph=[]\nfor f,src i … [1225 caractères tronqués]`

  ```
plus large | L'homme qui parle est mon père. | union: qui parle est mon père | gold: qui parle | src: reel
plus large | L'élève dont je parle est absent. | union: dont je parle est absent | gold: dont je parle | src: reel
plus large | L'homme dont la voiture est rouge arrive. | union: dont la voiture est rouge arrive | gold: dont la voiture est rouge | src: reel
plus large | L'endroit où nous allons est loin. | union: où nous allons est loin | gold: où nous allons | src: reel
plus large | L'oiseau qui vole est bleu. | union: qui vole est bleu | gold: qui vole | src: reel
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md", "new_string": "Les **81** REL/SUB se répartissent en **60 absentes**, **19 plus larges** et **2 plus étroites**.\nL'union du chunker ne répare **aucune** des 81 : elle ajoute 15 labels `REL`, dont 5 recouvr … [362 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md has been updated successfully.
  ```

### 🤖 Assistant

⏵ Vérification des lexiques cités (`marche`, `car`, `demain`)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys\nsys.path.insert(0,\"tools/structures\")\nimport generateur as S\nfor w in (\"marche\",\"nage\",\"crie\",\"dessine\",\"compte\",\"car\",\"demain\",\"ici\"):\n    print(w, \"VERBES_FINIS\" if w in S.VERBE … [179 caractères tronqués]`

  ```
marche - - -
nage - - -
crie VERBES_FINIS - -
dessine - - -
compte - - -
car - COORD -
demain - - ADVERBES_TEMPS
ici - - ADVERBES_TEMPS
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -m json.tool reports/pensee-contrat-s.json > /dev/null && echo \"JSON valide\" && sed -n '1,120p' reports/pensee-contrat-s.json", "description": "Valider et lire le début du JSON"}`

  ```
JSON valide
{
 "date": "2026-11-05",
 "ligne": "B13",
 "objet": "contrat d'interface L (bloc_linguistique) ↔ S (structures/generateur) pour les subordonnées REL/SUB",
 "verdict": "mesure faite ; le contrat s/v1 n'est pas tenu par S aujourd'hui ; aucun code modifié",
 "chiffre": "94 / 239 cibles sans segment au bon span : 48 REL, 33 SUB, 13 GP ; 81 REL/SUB (60 absentes, 19 plus larges, 2 plus étroites) ; S seul : 62/143 exacts (0,4336)",
 "gold": {
  "phrases": 612,
  "par_source": {
   "hand": 20,
   "reel": 432,
   "synthetique": 160
  },
  "segments": 1863,
  "cibles": 239,
  "cibles_par_type": {
   "GP": 96,
   "REL": 74,
   "SUB": 69
  },
  "cibles_rel_sub": 143
 },
 "ecart_bloc": {
  "cibles_sans_span_exact": 94,
  "par_type": {
   "REL": 48,
   "SUB": 33,
   "GP": 13
  },
  "categories": {
   "aucun": 65,
   "plus_large": 25,
   "plus_etroit": 4,
   "coupe": 0
  },
  "rel_sub": {
   "total": 81,
   "aucun": 60,
   "plus_large": 19,
   "plus_etroit": 2
  },
  "labels_exacts": 145,
  "lecture": "le bloc ne répare aucune des 81 REL/SUB ; l'union ajoute 15 labels REL, 0 exact"
 },
 "s_seul": {
  "cibles": 143,
  "exact": 62,
  "taux": 0.4336,
  "aucun": 60,
  "plus_large": 18,
  
… [1006 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '120,360p' reports/pensee-contrat-s.json", "description": "Lire la suite du JSON"}`

  ```
"echecs": 1
   },
   "reel": {
    "cibles": 109,
    "exact": 50,
    "echecs": 59
   },
   "synthetique": {
    "cibles": 31,
    "exact": 10,
    "echecs": 21
   },
   "reel_hand": {
    "cibles": 112,
    "exact": 52,
    "echecs": 60
   },
   "tout": {
    "cibles": 143,
    "exact": 62,
    "echecs": 81
   }
  },
  "causes_fr": {
   "REL_plus_large": 18,
   "REL_plus_etroit": 2,
   "SUB_absent": 6,
   "SUB_plus_etroit": 1,
   "detail": "18 larges = 16 synthétiques + 2 réelles ; 6 absentes = 1 'car' + 5 GN qui avalent le verbe ; 2 REL étroites = AUX(est) + adverbe(demain/ici)"
  },
  "causes_en": {
   "REL_absent": 28,
   "SUB_absent": 26,
   "detail": "marqueurs anglais (that/where/who/because/although/when/if/while…) absents du lexique français de S"
  }
 },
 "cibles_s": {
  "champs": [
   "cible_nom",
   "cible_gp",
   "cible_verbe"
  ],
  "forme": "textes complets (GN/GV), pas des têtes ; cible_gp = tête du GP le plus à gauche ; aucune direction",
  "sur_spans_exacts": {
   "REL": {
    "labels": 26,
    "nom_non_nul": 26,
    "nom_juste": 26,
    "verbe_non_nul": 0,
    "verbe_juste": 0,
    "aucune": 0
   },
   "SUB": {
    "labels": 36,
    "nom_non_nul": 6,
    "nom_ju
… [5390 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '360,520p' reports/pensee-contrat-s.json", "description": "Lire la fin du JSON"}`

  ```
"ne pas produire un GV couvrant la phrase pour une langue non couverte",
   "ne pas exposer les cibles seulement via des fonctions privées",
   "ne pas utiliser cible_gp comme cible REL/SUB (0/89)"
  ],
  "repli_L": [
   "REL → _tete_nom du GN antécédent (26/26)",
   "SUB → _verbe_dans du GV gouverneur, direction gauche ou droite (34/36 simulé)",
   "GP → _cible_proche (69/83)",
   "langue : passer lg ; si refus, repli chunker ou aucun label + trace",
   "une seule segmentation : structure() ; si s/v0, adaptateur isolé et meta.contrat=s/v0",
   "rôle : ne pas l'utiliser pour l'attachement ; sous_type est le champ structurel"
  ],
  "refus": {
   "statut": "refus",
   "raisons": [
    "langue_non_couverte",
    "texte_vide",
    "conflit",
    "version"
   ]
  }
 },
 "limites": [
  "gold 612 (452 réelles dont 20 gold.py + 160 synthétiques) ; réel seul 52/112 exacts",
  "les 16 REL larges synthétiques gonflent l'effet « plus large »",
  "classement des spans heuristique ; un cas change de catégorie entre S et le bloc",
  "le 93 de la fiche précédente vs 94 courant : écart d'un GP à qualifier (lexique verbal modifié)",
  "_est_verbe classe 34 cibles SUB comme des noms ; le POS du gold
… [744 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json, pathlib\np = pathlib.Path(\"reports/pensee-contrat-s.json\")\nd = json.loads(p.read_text(encoding=\"utf-8\"))\nd[\"cibles_s\"][\"forme\"] = \"textes complets (GN/GV), pas des têtes ; cible_gp = tête du  … [706 caractères tronqués]`

  ```
ok 10833
JSON valide
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"plus à gauche\\|6 erreurs\\|artefact\" reports/rapport-contrat-s.md", "description": "Repérer les formulations à corriger"}`

  ```
34:- pour un REL/SUB, le bloc n'utilise pas ce canal : il prend le `GN` le plus à gauche dans
256:`cible_verbe = "Je pense"`, pas `pense`. `cible_gp` est la tête du GP le plus à gauche :
295:| **POS gold vs `CONVENTION_CIBLE`** | SUB : **69/69 VERB** (42 gauche, 26 droite, 1 interne) ; REL : 73 NOUN + 1 PRON, à gauche | la convention écrite (`gold_reel.py:25-32`, « SUB → antécédent, tête du GN à gauche ») est **contredite par les données** ; le 28/36 SUB du bloc doit beaucoup au repli `_cible_proche` (les 6 erreurs sont les cas où un GN à gauche existe) |
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md", "new_string": "`cible_verbe = \"Je pense\"`, pas `pense`. `cible_gp` est la tête du GP le plus proche à gauche :", "old_string": "`cible_verbe = \"Je pense\"`, pas `pense`. `cible_gp` est la tête du GP le p … [16 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md", "new_string": "la convention écrite (`gold_reel.py:25-32`, « SUB → antécédent, tête du GN à gauche ») est **contredite par les données** ; le 28/36 SUB du bloc doit beaucoup au repli `_cible_proche` (les 6  … [320 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md has been updated successfully.
  ```

### 🤖 Assistant

⏵ Contrôle final : seuls les deux fichiers neufs, aucun code touché

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short reports/rapport-contrat-s.md reports/pensee-contrat-s.json; echo \"-- tools diff --\"; git diff --stat -- tools/; echo \"-- structures --\"; git status --short tools/structures/; echo \"-- pycache --\"; ls -la tool … [167 caractères tronqués]`

  ```
?? reports/pensee-contrat-s.json
?? reports/rapport-contrat-s.md
-- tools diff --
 tools/bloc_linguistique.py               | 66 +++++++++++++++++++++++++++-----
 tools/pensee/autotest.py                 | 62 +++++++++++++++++++++---------
 tools/structures                         |  0
 tools/tests/linguistique/evaluer_gold.py |  8 +++-
 4 files changed, 106 insertions(+), 30 deletions(-)
-- structures --
 m tools/structures
-- pycache --
total 172
drwxr-xr-x. 1 stephane stephane   564  4 nov 11:41 .
drwxr-xr-x. 1 stephane stephane   438  3 nov 16:22 ..
-rw-r--r--. 1 stephane stephane 10664  3 nov 17:08 arbre_svg.cpython-313.pyc
-rw-------. 1 stephane stephane  6944  2 nov 20:04 candidats_corpus.cpython-313.pyc
-rw-------. 1 stephane stephane 129848  5 nov 13:51 tools/__pycache__/bloc_linguistique.cpython-313.pyc
  ```

### 🤖 Assistant

⏵ Inspection des changements préexistants dans `tools/` (non miens) pour cadrer la mesure

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff -- tools/bloc_linguistique.py | head -120", "description": "Lire le diff préexistant du bloc"}`

  ```
diff --git a/tools/bloc_linguistique.py b/tools/bloc_linguistique.py
index 65fb0d76..5cc3858f 100644
--- a/tools/bloc_linguistique.py
+++ b/tools/bloc_linguistique.py
@@ -413,6 +413,9 @@ come comes came coming take takes took taken taking put puts putting say says sa
 see sees saw seen seeing know knows knew known knowing want wants wanted wanting need needs
 needed needing help helps helped helping look looks looked looking give gives gave given
 find finds found finding open opens opened opening close closes closed closing
+fly flies flew flown flying climb climbs climbed climbing flow flows flowed flowing
+swim swims swam swum swimming get gets got gotten getting smile smiles smiled smiling
+wait waits waited waiting belong belongs belonged belonging
 """.split())
 
 
@@ -613,6 +616,21 @@ class Heuristique:
         except Exception:
             return {}
 
+    @staticmethod
+    def _tete_texte(texte: str) -> str | None:
+        """La tête d'un texte de candidat : le verbe plein s'il y en a un, sinon le dernier mot.
+
+        `« … → Le livre »` → `livre` ; `« … → Les fleurs poussent »` → `poussent` ;
+        `« … → est prêt »` → `prêt` (l'auxiliaire n'est pas la tête).
+  
… [4867 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git -C tools/structures status --short 2>&1 | head; git -C tools/structures diff --stat 2>&1 | head; git log -1 --format=\"%h %ci %s\" -C tools/structures 2>&1", "description": "État du sous-module S"}`

  ```
M donnees/paragraphes-validations.jsonl
 donnees/paragraphes-validations.jsonl | 11 +++++++++++
 1 file changed, 11 insertions(+)
8189c4f3 2026-11-04 11:54:36 -0500 S — LE FAIT DIVERS EST TRANCHÉ : 61/61 TYPES, 144/144 RÔLES ; LA TÊTE DU GN ARRÊTE LE VERBE
  ```

### 🤖 Assistant

⏵ Alerte concurrence : le bloc a changé pendant la mesure ; je vérifie l'état courant

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && stat -c '%y %n' tools/bloc_linguistique.py tools/tests/linguistique/evaluer_gold.py tools/structures/generateur.py 2>/dev/null; date; echo ---; sed -n '860,910p' tools/bloc_linguistique.py", "description": "Vérifier mtime et code cou … [14 caractères tronqués]`

  ```
2026-11-05 13:51:26.638852086 -0500 tools/bloc_linguistique.py
2026-11-05 13:51:45.675060894 -0500 tools/tests/linguistique/evaluer_gold.py
2026-11-04 11:41:49.129836555 -0500 tools/structures/generateur.py
jeu 05 nov 2026 14:01:41 EST
---
            # candidat d'attachement (diagnostic des 33 échecs de T162).
            gvs_simple = [x for x in self._syntagmes_simple(texte, lg) if x["type"] == "GV"]
            for c in cands[:1]:
                noms = [x.get("nom", "") for x in cands]
                gvs_s = [x for x in c.get("segments", []) if x.get("type") == "GV"]
                deja = {(x["debut"], x["fin"]) for x in gvs_s}
                gvs = gvs_s + [x for x in gvs_simple if (x["debut"], x["fin"]) not in deja]
                for s in c.get("segments", []):
                    # la cible de S **convertie en son verbe** : « Les enfants jouent » →
                    # `jouent` (le gold attend le verbe, pas le GN) ; à défaut, le GV le plus
                    # proche. Mesuré : 82 cibles justes dans les candidats, 33 choisies avant.
                    brute = (self._cible_s_par_genre(cands, s.get("texte", ""), s.get("type", ""))
                             or cibles_s
… [2635 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Remesure sur l'état courant du bloc (correctif concurrent) et diff de l'évaluateur

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff -- tools/tests/linguistique/evaluer_gold.py tools/pensee/autotest.py | head -140", "description": "Lire le diff de l'évaluateur et de l'autotest"}`

  ```
diff --git a/tools/pensee/autotest.py b/tools/pensee/autotest.py
index ffb42e0d..1eef90d0 100644
--- a/tools/pensee/autotest.py
+++ b/tools/pensee/autotest.py
@@ -2223,8 +2223,8 @@ def t153_attachement() -> tuple[bool, str]:
     import tools.bloc_linguistique as bl
     from ..tests.linguistique.evaluer_gold import charger, evaluer_bloc
     r = evaluer_bloc("h", bl.Heuristique(), charger())["attachement"]
-    return (r["cibles"] == 239 and abs(r["top1_taux"] - 0.5272) < 0.001
-            and abs(r["exact_taux"] - 0.5146) < 0.001), (
+    return (r["cibles"] == 239 and abs(r["top1_taux"] - 0.5858) < 0.001
+            and abs(r["exact_taux"] - 0.5732) < 0.001), (
         f"attachement : top1 {r['top1_taux']}, exact {r['exact_taux']}, "
         f"couverture {r['couverture']}")
 
@@ -2341,7 +2341,7 @@ def t161_cible_proximite() -> tuple[bool, str]:
     from ..tests.linguistique.evaluer_gold import charger, evaluer_bloc
     r = evaluer_bloc("h", bl.Heuristique(), charger())
     a, th = r["attachement"], r["attachement_tete"]
-    return (a["cibles"] == 239 and a["top1"] == 126 and a["exact"] == 123), (
+    return (a["cibles"] == 239 and a["top1"] == 140 and a["exact"] == 137)
… [6454 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, json, pathlib, collections, unicodedata\nsys.path.insert(0,\"tools\"); sys.path.insert(0,\"tools/structures\")\nimport bloc_linguistique as bl, generateur as S\nbase=pathlib.Path(\"tools/tests/linguisti … [1202 caractères tronqués]`

  ```
{('SUB', 'juste'): 34, ('REL', 'juste'): 26, ('SUB', 'faux'): 2} total 62
('SUB', 'Quand tu arrives, appelle-moi.', 'appelle', 'appelle-moi')
('SUB', "Peut-être qu'il viendra.", 'viendra', 'Peut-être')
  ```

### 🤖 Assistant

⏵ Remesure complète de l'état courant (correctif concurrent inclus)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 300 python3 tools/tests/linguistique/evaluer_gold.py --json /tmp/eval_gold_courant.json > /tmp/eval_gold_courant.out 2>&1; echo exit=$?; python3 - <<'EOF'\nimport json\nd=json.load(open(\"/tmp/eval_gold_courant.json\"))\nh=d[ … [498 caractères tronqués]`

  ```
exit=0
{
 "labels": 145,
 "top1": 140,
 "exact": 137,
 "top1_span": 0.9655,
 "exact_span": 0.9448,
 "verbe": {
  "cibles": 116,
  "justes": 111,
  "taux": 0.9569
 },
 "nom": {
  "cibles": 29,
  "justes": 26,
  "taux": 0.8966
 },
 "hasard": {
  "cibles": 239,
  "top1_taux": 0.0042
 },
 "ok": true
}
     
heuristique all: {"pos": {"exactitude": 0.7455, "exactitude_ferme": 0.8984, "exactitude_ouvert": 0.6007, "tokens": 3179, "confusions": {"ADJ": {"ADJ": 50, "NOUN": 80, "VERB": 4}, "ADV": {"ADV": 117, "NOUN": 21, "PREP": 1, "ADJ": 1, "?": 1}, "AUX": {"PREP": 4, "AUX": 118, "?": 3, "NOUN": 3}, "CONJ": {"CONJ": 44, "PRON": 25, "DET": 12, "?": 13, "PREP": 2, "NOUN": 2}, "DET": {"DET": 586, "?": 2}, "NOUN": {"NOUN": 617, "ADJ": 17, "VERB": 47, "?": 1}, "NUM": {"NUM": 2}, "PONCT": {"?": 25}, "PREP": {"PREP": 111, "NOUN": 3}, "PRON": {"PRON": 411, "NOUN": 8, "?": 30, "DET": 25, "CONJ": 1}, "VERB": {"VERB": 314, "NOUN": 447, "ADJ": 5, "PREP": 2, "?": 16, "AUX": 7, "ADV": 1}}}, "syntagme": {"precision": 0.3154, "rappel": 0.2619, "f1": 0.2862, "tp": 488, "fp": 1059, "fn": 1375, "tete": {"precision": 0.5862, "rappel": 0.4342, "f1": 0.4989, "tp": 809, "fp": 571, "fn": 1054}}, "pragmatique": {"ac
… [107 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 /tmp/synthese_contrat.py > /tmp/synthese_courant.json 2>/tmp/synthese_courant.err; echo exit=$?; python3 - <<'EOF'\nimport json\nd=json.load(open(\"/tmp/synthese_courant.json\"))\nfor k in (\"bloc\",\"bloc_type\",\"s\",\"s_ty … [245 caractères tronqués]`

  ```
exit=0
== bloc
{
 "exact": 145,
 "plus large": 25,
 "aucun": 65,
 "plus étroit": 4
}
== bloc_type
{
 "GP": {
  "exact": 83,
  "plus large": 6,
  "aucun": 5,
  "plus étroit": 2
 },
 "SUB": {
  "exact": 36,
  "aucun": 32,
  "plus étroit": 1
 },
 "REL": {
  "exact": 26,
  "aucun": 28,
  "plus large": 19,
  "plus étroit": 1
 }
}
== s
{
 "plus large": 23,
 "exact": 113,
 "aucun": 99,
 "plus étroit": 4
}
== s_type
{
 "GP": {
  "plus large": 5,
  "exact": 51,
  "aucun": 39,
  "plus étroit": 1
 },
 "SUB": {
  "exact": 36,
  "aucun": 32,
  "plus étroit": 1
 },
 "REL": {
  "exact": 26,
  "aucun": 28,
  "plus large": 18,
  "plus étroit": 2
 }
}
== regle_actuelle
{
 "GP|faux": 6,
 "GP|juste": 77,
 "SUB|juste": 34,
 "REL|juste": 26,
 "SUB|faux": 2
}
== regle_verbe
{
 "juste": 34,
 "faux": 2
}
== rel_sub
{
 "SUB|fr|exact": 36,
 "REL|fr|exact": 26,
 "SUB|en|aucun": 26,
 "REL|en|aucun": 28,
 "REL|fr|plus large": 19,
 "SUB|fr|plus étroit": 1,
 "REL|fr|plus étroit": 1,
 "SUB|fr|aucun": 6
}
== canaux
{
 "GP": {
  "nom": 41,
  "verbe": 34
 },
 "SUB": {
  "verbe": 23,
  "nom": 6
 },
 "REL": {
  "nom": 26
 }
}
== canaux_justes
{
 "GP": {
  "verbe": 32,
  "nom": 17
 },
 "SUB": {
  "verbe": 22
 },
 "REL":
… [19 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff -- tools/tests/linguistique/evaluer_gold.py", "description": "Lire le diff de l'évaluateur"}`

  ```
diff --git a/tools/tests/linguistique/evaluer_gold.py b/tools/tests/linguistique/evaluer_gold.py
index 729b1567..c8e05b00 100644
--- a/tools/tests/linguistique/evaluer_gold.py
+++ b/tools/tests/linguistique/evaluer_gold.py
@@ -128,8 +128,12 @@ def evaluer_bloc(nom: str, bloc, phrases: list[dict]) -> dict:
             if juste:
                 att_exact += 1
             # le gold mêle deux conventions : la cible est un verbe (le gouverneur) ou un nom
-            # (l'antécédent d'un REL, la tête d'un GP). On mesure les deux séparément.
-            if bl._est_verbe(cibles[0]):
+            # (l'antécédent d'un REL, la tête d'un GP). On mesure les deux séparément — en
+            # suivant le **POS du gold** (plus fiable que le lexique : « poussent », « aboie »
+            # y sont VERB), avec `_est_verbe` en repli si la cible n'est pas un token.
+            pos_cible = next((m["pos"] for m in phrase.get("mots", [])
+                              if phrase["texte"][m["debut"]:m["fin"]] == cibles[0]), None)
+            if (pos_cible == "VERB") if pos_cible else bl._est_verbe(cibles[0]):
                 att_v_n += 1
                 att_v_ok += int(juste)
             else:
  ```

### 🤖 Assistant

⏵ Mise à jour de la fiche pour l'état courant (correctif non committé) vs état initial

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md", "new_string": "> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅\n> mesure faite — le contrat `s/v1` **n'est pas tenu** par S. Le générateur S n'a pas ét … [2223 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md", "new_string": "- pour un REL/SUB, l'**état initial** n'utilisait pas ce canal : il prenait le `GN` le plus à\n  gauche dans `cands[0][\"segments\"]` et le réduisait avec `_tete_nom` (`:838-844`) ; à défaut\ … [1524 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md", "new_string": "toujours ni le type d'antécédent, ni la direction du gouverneur : le contrat reste implicite, et\nles 81 spans REL/SUB restent chez S. Or la mesure (§ 4, POS du gold) montre que le gold veut  … [242 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md", "new_string": "2. **SUB → verbe gouverneur** : `cible.genre == \"GV\"`, réduire avec `_verbe_dans`, **accepter\n   `direction=\"droite\"`**. Ne **jamais** prendre le GN sujet à gauche : c'est l'erreur des 6 … [574 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md", "new_string": "- **Deux états** : l'**état initial** (celui du début de session, avant le correctif du bloc) et\n  l'**état courant** (correctif non committé de 13:51, qui applique SUB → segment précédent e … [922 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md", "new_string": "Sur les **62** labels REL/SUB au span exact, l'attachement passe de **54/62** (état initial) à\n**60/62** (état courant) :\n\n| type | labels | juste initial | juste courant | écart |\n|---|- … [2792 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md", "new_string": "| **cible au hasard** parmi les 239 cibles | **1/239 = 0,0042** | 60/62 (état courant) n'est pas du hasard |", "old_string": "| **cible au hasard** parmi les 239 cibles | **1/239 = 0,0042** | … [47 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md", "new_string": "Le dernier contrôle est le plus important : `_est_verbe` classait **34** cibles SUB comme des noms\n(« marche », « commence »…), ce qui a fait croire à une convention mixte. Le correctif cour … [748 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '300,355p' reports/rapport-contrat-s.md", "description": "Lire la section limites actuelle"}`

  ```
subordonnée**, pas le gouverneur ; le bloc rend `Peut-être`. C'est le seul `direction="interne"`
  du gold ; **reste faux**, la convention doit être tranchée.

Le correctif courant laisse donc **2** erreurs nommées. Il ne répare pas les 81 spans : il ne
s'applique qu'aux 36 SUB déjà segmentées.

## 4. Contrôle négatif

| contrôle | résultat | lecture |
|---|---|---|
| **S coupé** (`Heuristique(segmenter_s=False)`) | **0/143** exact REL/SUB ; 135 absentes, 8 larges | les 62 exacts viennent **tous** de S ; le chunker seul n'en produit aucun |
| **cible au hasard** parmi les 239 cibles | **1/239 = 0,0042** | 60/62 (état courant) n'est pas du hasard |
| **permutation** des 74 cibles REL (2 000 tirages) | observé **44**, moyenne **1,31**, p95 **3**, max **6** | le canal nominal de S est prédictif sur **tout** le gold REL, pas seulement sur les 26 exacts |
| **premier GN de la phrase** sur les 26 REL exactes | **26/26** | le 26/26 REL **n'est pas** une preuve de la règle « plus proche » : sur ce sous-ensemble, le premier GN suffit. La preuve est la permutation sur 74 |
| **POS gold vs `CONVENTION_CIBLE`** | SUB : **69/69 VERB** (42 gauche, 26 droite, 1 interne) ; REL : 73 NOUN + 1 PRON, 
… [3155 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md", "new_string": "| **POS gold vs `CONVENTION_CIBLE`** | SUB : **69/69 VERB** (42 gauche, 26 droite, 1 interne) ; REL : 73 NOUN + 1 PRON, à gauche | la convention écrite (`gold_reel.py:25-32`, « SUB → antécéde … [605 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md", "new_string": "- **Le gold** : 612 phrases, dont 160 synthétiques ; 452 réelles (dont 20 de `gold.py`). Les 16\n  REL larges synthétiques gonflent l'effet « plus large » ; sur le réel seul, **52/112** spans … [715 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md", "new_string": "- **La règle SUB n'est plus une simulation** : le correctif non committé l'applique et donne\n  **34/36** (60/62 REL/SUB) ; les 2 échecs restants sont l'impératif (`appelle-moi`) et la cible\ … [341 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md", "new_string": "- **Portes non rejouées** : le correctif du bloc n'est pas committé ; l'évaluateur gold courant\n  rend `ok: true` (exact 137, 0,9448). Le parent doit committer le correctif et rejouer\n  `to … [271 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md", "new_string": "4. **L — la cible (fait dans l'arbre courant, non committé)** : SUB → `_cible_proche` (verbe),\n   REL → `_tete_nom` (antécédent), GP → `_cible_proche` ; lire les `cible` typées, ne plus\n    … [1316 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md", "new_string": "- [`generateur.py`](../tools/structures/generateur.py) — lu, **non modifié** : `Segment` (`:293`),\n  `_segmente` (`:346`), `construire_arbre` (`:319`), cibles (`:485-497`), `analyser` (`:516 … [1393 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"REL/SUB : c'est le\\|# 5 bis\\|def _syntagmes_s\\|def _cibles_s\\|def _tete_nom\\|def _cible_proche\" tools/bloc_linguistique.py", "description": "Vérifier les numéros de ligne courants"}`

  ```
591:    def _syntagmes_s(self, texte: str) -> list[dict] | None:
602:    def _cibles_s(self, texte: str) -> dict:
635:    def _tete_nom(texte: str, debut: int, fin: int) -> str | None:
661:    def _cible_proche(texte: str, segment: dict, gvs: list[dict],
725:    def _syntagmes_simple(self, texte: str, langue: str) -> list[dict]:
875:                        # REL/SUB : c'est le **segment précédent** qui tranche — après un GV
924:        # 5 bis. union : les segments du chunker que le générateur S ne fournit pas
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"bloc_linguistique.py:\\|(`:[0-9]\\|(:[0-9]\\|:838\\|:642\\|:588\\|:599\\|:616\\|:868\\|:900\" reports/rapport-contrat-s.md", "description": "Lister les références de ligne à corriger"}`

  ```
[stderr]
bash: -c: line 1: unexpected EOF while looking for matching ``'
[exit code: 2]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -nE \"bloc_linguistique\\.py:|:838|:642|:588|:599|:616|:868|:900\" reports/rapport-contrat-s.md", "description": "Lister les références de ligne à corriger"}`

  ```
33:- `Heuristique._syntagmes_s` (`bloc_linguistique.py:588`) importe `generateur.analyser(texte)` ;
34:- `Heuristique._cibles_s` (`:599`) importe `generateur._segmente` et `generateur._tokens`, **re-segmente
39:  gauche dans `cands[0]["segments"]` et le réduisait avec `_tete_nom` (`:838-844`) ; à défaut
40:  seulement, il retombait sur `_cible_proche` (le verbe du GV le plus proche, `:642`). Le
386:  committé (13:51) est celui du chantier en cours, pas de cette fiche : `_syntagmes_s` (`:588`),
387:  `_cibles_s` (`:599`), `_tete_nom` (`:616`), `_cible_proche` (`:642`), branche REL/SUB
388:  (`:868-889`), union (`:900-917`).
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np = pathlib.Path(\"reports/rapport-contrat-s.md\")\ns = p.read_text(encoding=\"utf-8\")\ns = s.replace(\"- `Heuristique._syntagmes_s` (`bloc_linguistique.py:588`) importe `generateur.analyser(texte)` … [1455 caractères tronqués]`

  ```
ok
aucune référence de ligne au bloc
  ```

### 🤖 Assistant

⏵ Mise à jour du JSON pour les deux états (initial / courant)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json, pathlib\np = pathlib.Path(\"reports/pensee-contrat-s.json\")\nd = json.loads(p.read_text(encoding=\"utf-8\"))\n\nd[\"verdict\"] = (\"mesure faite ; le contrat s/v1 n'est pas tenu par S ; deux états mesu … [4653 caractères tronqués]`

  ```
ok 12118
JSON valide
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -nE \"simulation|129/145|règle proposée|123/145|exact 123|0,8483|28/36|54/62|60/62|137\" reports/rapport-contrat-s.md", "description": "Vérifier les mentions des deux états"}`

  ```
10:> **état courant : labels 145, exact 137, exactitude spans 0,9448, hasard 0,0042** ; état
11:> initial, avant le correctif : exact 123, 0,8483).
15:> REL/SUB (43,4 %). L'attachement REL/SUB passe de **54/62** (état initial) à **60/62** (état
47:le correctif courant la code en dur (`GV → verbe`, `GN → nom`) et valide 60/62, mais S ne fournit
132:   précédent GV → verbe ») : **34/36** sur les SUB au span exact, contre **28/36** dans l'état
171:  l'attachement change (123/145 → 137/145).
175:  `labels 145`, `exact 137`, `exact_taux_span 0,9448` ; initial `exact 123`, `0,8483` ;
277:Sur les **62** labels REL/SUB au span exact, l'attachement passe de **54/62** (état initial) à
278:**60/62** (état courant) :
285:| **tout** | **145** | **123 (0,8483)** | **137 (0,9448)** | **+14** |
311:| **cible au hasard** parmi les 239 cibles | **1/239 = 0,0042** | 60/62 (état courant) n'est pas du hasard |
314:| **POS gold vs `CONVENTION_CIBLE`** | SUB : **69/69 VERB** (42 gauche, 26 droite, 1 interne) ; REL : 73 NOUN + 1 PRON, à gauche | la convention écrite (`gold_reel.py:25-32`, « SUB → antécédent, tête du GN à gauche ») est **contredite par les données** ; le 28/36 SUB de l'état initial doit be
… [648 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"proposée\\|simul\\|non_implementee\\|123\\|129\\|8483\\|9448\\|137\\|28/36\\|34/36\" reports/pensee-contrat-s.json | head -40", "description": "Vérifier les mentions d'état dans le JSON"}`

  ```
6: "chiffre": "94 / 239 cibles sans segment au bon span : 48 REL, 33 SUB, 13 GP ; 81 REL/SUB (60 absentes, 19 plus larges, 2 plus étroites) ; S seul : 62/143 exacts (0,4336) ; attachement REL/SUB : 54/62 initial, 60/62 courant ; total 123/145 (0,8483) → 137/145 (0,9448)",
216:   "exact": 123,
217:   "taux_span": 0.8483,
225:   "exact": 137,
226:   "taux_span": 0.9448,
235:    "exact": 137,
237:    "exact_taux_span": 0.9448,
255:   "total": "+14 (123 → 137/145 ; 0,8483 → 0,9448)",
375:   "SUB → _verbe_dans du GV gouverneur, direction gauche ou droite (34/36 observé dans l'état courant)",
395:  "deux états dans l'arbre : correctif non committé du bloc (13:51) + POS de l'évaluateur ; spans 94/81/62 stables, attachement 123/145 → 137/145",
399:  "règle SUB appliquée par le correctif non committé (34/36) ; 2 échecs restants nommés ; +8 GP du même lot non attribué à cette fiche",
402:  "portes non rejouées ; le correctif du bloc n'est pas committé ; evaluer_gold.py rejoué (ok: true, 137, 0,9448)"
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '18,58p' reports/rapport-contrat-s.md; echo \"----\"; sed -n '160,185p' reports/rapport-contrat-s.md; echo \"----\"; sed -n '270,305p' reports/rapport-contrat-s.md", "description": "Relire les sections modifiées"}`

  ```
> pas de refus).

## 1. Le constat : l'interface actuelle est un couplage privé

S n'expose aujourd'hui que deux surfaces publiques, et aucune ne porte le contrat complet ; le
bloc complète avec une troisième, privée :

| surface | fichier | ce qu'elle rend | ce qui manque |
|---|---|---|---|
| `analyser(texte, max_candidats=4)` | `generateur.py:516` | jusqu'à 4 candidats ; **seul le dernier segment ambigu** (GP/REL, jamais SUB) porte `attachement` | les cibles des autres segments, les SUB, un type de cible |
| `structure(texte, roles=True)` | `generateur.py:621` | `[s.dict() for s in segs]` | `Segment.dict()` (`:306`) **omet** `cible_nom`, `cible_gp`, `cible_verbe` |
| `_segmente(texte, toks)`, `_tokens(texte)` | `generateur.py:346, 175` | la liste complète des `Segment` avec leurs `cible_*` | ce sont des **fonctions privées** |

Le bloc fait donc de S un usage de fait privé :

- `Heuristique._syntagmes_s` importe `generateur.analyser(texte)` ;
- `Heuristique._cibles_s` importe `generateur._segmente` et `generateur._tokens`, **re-segmente
  la phrase une seconde fois**, puis écrase les trois canaux en un seul :
  `(s.cible_gp or s.cible_nom or s.cible_verbe)` — priorité **GP > nom
… [5127 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys\nsys.path.insert(0,\"tools/structures\")\nimport generateur as S\nfor t in [\"La fleur qui pousse ici est rare.\", \"L'homme dont la voiture est rouge arrive.\", \"Je sais qu'il vient demain.\"]:\n    pr … [171 caractères tronqués]`

  ```
== La fleur qui pousse ici est rare.
  GN 0 8 'La fleur'
  REL 9 19 'qui pousse'
  GP 20 23 'ici'
  GV 24 32 'est rare'
== L'homme dont la voiture est rouge arrive.
  GN 0 7 "L'homme"
  REL 8 23 'dont la voiture'
  GV 24 40 'est rouge arrive'
== Je sais qu'il vient demain.
  GV 0 7 'Je sais'
  SUB 8 19 "qu'il vient"
  GP 20 26 'demain'
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md", "new_string": "- **3 REL/SUB étroites.** `L'homme dont la voiture est rouge arrive.` → REL `dont la voiture`\n  (8-23 au lieu de 8-33) : la boucle coupe sur `est` (`AUX` après un mot), alors que `est rouge` … [1083 caractères tronqués]`

  ```
Error: cannot edit "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md": file changed since it was read — re-read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md", "offset": 210, "limit": 30}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md</path>
<type>file</type>
<content>
210: | **tout** | 74 | 26 | 69 | 36 | **81** |
211: 
212: **54 des 81 échecs sont anglais** : S ne connaît que les marqueurs français (`RELATIFS`,
213: `SUBORD_SIMPLE`, `SUBORD_QUE`, `SUBORD_ELIDE`, `generateur.py:22, 52-58`) et traite `that`,
214: `where`, `who`, `because`, `although`, `when`, `if`, `while` comme des mots ordinaires. Les **27
215: échecs français** se répartissent en **18 REL larges**, **2 REL étroites**, **6 SUB absentes** et
216: **1 SUB étroite**.
217: 
218: | source | cibles REL/SUB | exact | échecs |
219: |---|---:|---:|---:|
220: | hand | 3 | 2 | 1 (anglais) |
221: | reel | 109 | 50 | 59 (53 anglais + 6 français) |
222: | synthetique | 31 | 10 | 21 (16 REL larges + 5 SUB absentes) |
223: | **tout** | **143** | **62** | **81** |
224: 
225: Les 18 REL larges de S sont **16 synthétiques + 2 réelles** ; l'union en ajoute une troisième,
226: réelle, en déplaçant une étroite. Le gold synthétique gonfle donc l'effet « plus large », mais le
227: gold réel garde **52/112** spans exacts (46,4 %) et **60** échecs.
228: 
229: ### 3.4 Ce que S ne produit 
… [944 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md", "limit": 28, "offset": 240}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md</path>
<type>file</type>
<content>
240:   **aucun GV** : le verbe principal `dormait` est avalé, donc la phrase n'a plus de prédicat.
241:   `Le chat que j'ai vu dormait.` est l'exemple canonique : le span faux détruit aussi une cible
242:   potentielle (`dormait`).
243: - **3 REL/SUB étroites.** `L'homme dont la voiture est rouge arrive.` → REL `dont la voiture`
244:   (8-23 au lieu de 8-33) : la boucle coupe sur `est` (`AUX` après un mot), alors que `est rouge`
245:   est le prédicat **de la relative**. `Je sais qu'il vient demain.` → SUB `qu'il vient` (8-19 au
246:   lieu de 8-26) : la boucle coupe sur `demain`, adverbe de temps **de la subordonnée**. La règle
247:   « un prédicat par clause » manque : après le premier verbe plein, c'est le **second** verbe
248:   conjugué qui ouvre la principale, pas un auxiliaire ni un adverbe.
249: 
250: ### 3.5 Les cibles de S
251: 
252: Sur les **62** labels REL/SUB au span exact de S :
253: 
254: | type | labels | `cible_nom` | dont juste | `cible_verbe` | dont juste | aucune |
255: |---|---:|---:|---:|---:|---:|---:|
256: | **REL** | 26 | 26 | **26** | 0 | 
… [930 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md", "new_string": "- **3 REL/SUB étroites.** `L'homme dont la voiture est rouge arrive.` → REL `dont la voiture`\n  (8-23 au lieu de 8-33) : la boucle coupe sur `est` (`AUX` après un mot), alors que `est rouge` … [1083 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json, pathlib\np = pathlib.Path(\"reports/pensee-contrat-s.json\")\nd = json.loads(p.read_text(encoding=\"utf-8\"))\nd[\"fichiers\"] = [\n \"tools/structures/generateur.py (lu, non modifié)\",\n \"tools/bloc_ … [619 caractères tronqués]`

  ```
ok
JSON valide
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -nE \"proposée|simulation|non_implementee|129|0,8897|28/36|54/62\" reports/pensee-contrat-s.json || echo \"aucune mention obsolète\"; echo ---; python3 - <<'EOF'\nimport json\nd=json.load(open(\"reports/pensee-contrat-s.json\")) … [156 caractères tronqués]`

  ```
6: "chiffre": "94 / 239 cibles sans segment au bon span : 48 REL, 33 SUB, 13 GP ; 81 REL/SUB (60 absentes, 19 plus larges, 2 plus étroites) ; S seul : 62/143 exacts (0,4336) ; attachement REL/SUB : 54/62 initial, 60/62 courant ; total 123/145 (0,8483) → 137/145 (0,9448)",
---
{
 "labels_exacts": 145,
 "etat_initial": {
  "exact": 123,
  "taux_span": 0.8483,
  "par_type": {
   "REL": 26,
   "SUB": 28,
   "GP": 69
  }
 },
 "etat_courant": {
  "exact": 137,
  "taux_span": 0.9448,
  "par_type": {
   "REL": 26,
   "SUB": 34,
   "GP": 77
  },
  "evaluateur": {
   "labels": 145,
   "top1": 140,
   "exact": 137,
   "top1_taux_span": 0.9655,
   "exact_taux_span": 0.9448,
   "verbe": {
    "cibles": 116,
    "justes": 111,
    "taux": 0.9569
   },
   "nom": {
    "cibles": 29,
    "justes": 26,
    "taux": 0.8966
   }
  }
 },
 "regle_initiale": "REL/SUB → GN le plus à gauche, réduit par _tete_nom ; à défaut _cible_proche ; GP → _cible_proche",
 "regle_courante": "REL/SUB → segment précédent : GV → _verbe_dans (SUB), GN → _tete_nom (REL) ; puis _cible_proche ; GP → _cible_proche",
 "gain_observe": {
  "REL_SUB": "+6 (54 → 60/62)",
  "GP": "+8 (69 → 77/83)",
  "total": "+14 (123 → 137/145 ; 0,
… [821 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Relecture finale des sections 4 à 7 et contrôle d'état git

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md", "limit": 120, "offset": 300}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-contrat-s.md</path>
<type>file</type>
<content>
300:   token, le trait d'union n'est pas séparé) au lieu de `appelle` ; **reste faux**.
301: - **1 cas gold** : `Peut-être qu'il viendra.` → la cible gold est `viendra`, le verbe **de la
302:   subordonnée**, pas le gouverneur ; le bloc rend `Peut-être`. C'est le seul `direction="interne"`
303:   du gold ; **reste faux**, la convention doit être tranchée.
304: 
305: Le correctif courant laisse donc **2** erreurs nommées. Il ne répare pas les 81 spans : il ne
306: s'applique qu'aux 36 SUB déjà segmentées.
307: 
308: ## 4. Contrôle négatif
309: 
310: | contrôle | résultat | lecture |
311: |---|---|---|
312: | **S coupé** (`Heuristique(segmenter_s=False)`) | **0/143** exact REL/SUB ; 135 absentes, 8 larges | les 62 exacts viennent **tous** de S ; le chunker seul n'en produit aucun |
313: | **cible au hasard** parmi les 239 cibles | **1/239 = 0,0042** | 60/62 (état courant) n'est pas du hasard |
314: | **permutation** des 74 cibles REL (2 000 tirages) | observé **44**, moyenne **1,31**, p95 **3**, max **6** | le canal nominal de S est prédictif sur **tout** le gold REL,
… [6711 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification finale des livrables et de l'état du dépôt

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -l reports/rapport-contrat-s.md reports/pensee-contrat-s.json && wc -l reports/rapport-contrat-s.md && python3 -m json.tool reports/pensee-contrat-s.json > /dev/null && echo \"JSON OK\" && git status --short reports/rapport-contra … [91 caractères tronqués]`

  ```
-rw-r--r--. 1 stephane stephane 12288  5 nov 14:13 reports/pensee-contrat-s.json
-rw-------. 1 stephane stephane 26094  5 nov 14:13 reports/rapport-contrat-s.md
394 reports/rapport-contrat-s.md
JSON OK
?? reports/pensee-contrat-s.json
?? reports/rapport-contrat-s.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff --stat -- tools/structures/generateur.py; git -C tools/structures status --short | head -3; echo \"---\"; git status --short | grep -c '^??'", "description": "Confirmer que generateur.py n'a pas bougé"}`

  ```
M donnees/paragraphes-validations.jsonl
---
16
  ```

