# Session DSH — relecture

- identifiant : `082fe8ca-3e1e-4454-b91b-12586843e880`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-06 11:17:08
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **auditer la fiabilité du produit hors gold** — le test « utilisateur » qui manque.

Contexte : `tools/drave.py` (CLI : `analyser`, `evaluer`, `rejouer`, `--version`), `tools/bloc_linguistique.py` (`Heuristique.analyser` → `Annotation`), la doc `docs/produit/README.md`. État mesuré : gold 222/222, couverture 0,9289, POS 75,81 %, F1 58,49 %.

À faire :
1. **50 phrases libres** (écris-les toi-même : longues, ponctuation variée, majuscules, questions, impératives, négations, anglais, chiffres, URL, emoji, texte vide, très long) — analyse-les avec la CLI et note : plantages, sorties vides, spans hors texte ou chevauchants, cibles absentes, JSON invalide, temps.
2. **Robustesse des entrées** : texte vide, espaces, un seul mot, 10 000 caractères, caractères spéciaux, encodage ; codes de sortie.
3. **Contrat de sortie** : les champs toujours présents, ceux qui peuvent être vides, ce qui casserait un client ; propose un **schéma minimal versionné** (les 8 champs clés) et un test de non-régression du schéma.
4. **Liste de correctifs produit** (bloquants / importants / confort) chiffrée, avec les lignes concernées.
5. Écris **uniquement** deux fichiers neufs : `reports/rapport-fiabilite-produit.md` et `reports/pensee-fiabilite-produit.json`.
6. Ne commite rien ; ne modifie aucun existant ; pas de `docs/pilotage/`, `AGENTS.md`, `journal/`, `tools/structures/`, `data/`, natifs.

Rends un résumé : plantages (nombre, causes), temps par phrase, contrat, les 5 correctifs prioritaires.
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

⏵ Lecture des fichiers clés du produit (CLI, annotation, doc)

- **bash** `{"command": "pwd && git -C . status --short | head -20 && git -C . branch --show-current", "description": "Check working directory and git status"}`

  ```
/home/stephane/Data13TB/stephane/GitHub/Qtrinet
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
D  journal/sessions/14114f3d-ae0d-416e-ad8e-4d4eaa04c36c/digest.md
s/v7
  ```

- **bash** `{"command": "ls -la /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports | head -40", "description": "List repo root and reports directory"}`

  ```
total 204
drwxr-xr-x. 1 stephane stephane   686  6 nov 09:52 .
drwxr-xr-x. 1 stephane stephane  2532  5 nov 10:41 ..
-rw-r--r--. 1 stephane stephane  9977  3 nov 09:19 AGENTS.md
drwxr-xr-x. 1 stephane stephane    40 25 sep 15:38 bench
drwxr-xr-x. 1 stephane stephane    56 30 sep 12:20 colab
drwxr-xr-x. 1 stephane stephane  2664  2 nov 18:33 data
drwxr-xr-x. 1 stephane stephane   138  6 nov 10:08 docs
drwxr-xr-x. 1 stephane stephane    92 28 oct 16:25 drave-core
drwxr-xr-x. 1 stephane stephane   180  6 nov 11:17 .git
-rw-r--r--. 1 stephane stephane   619 31 oct 17:33 .gitignore
-rw-r--r--. 1 stephane stephane   225  1 nov 10:50 .gitmodules
drwxr-xr-x. 1 stephane stephane   912  6 nov 00:08 journal
drwxr-xr-x. 1 stephane stephane   100  3 nov 09:12 models
drwxr-xr-x. 1 stephane stephane   114 25 sep 15:24 __pycache__
drwxr-xr-x. 1 stephane stephane    64  6 nov 09:52 .pytest_cache
-rw-r--r--. 1 stephane stephane  4992 25 sep 10:54 Qtrinet-bootstrap.md
-rw-r--r--. 1 stephane stephane 19956 29 oct 08:14 README.md
drwxr-xr-x. 1 stephane stephane 71144  6 nov 11:15 reports
-rw-r--r--. 1 stephane stephane 13100 28 oct 14:59 REPRISE.md
-rw-------. 1 stephane stephane  8566 30 sep 08:44 run
… [3796 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de `tools/drave.py`, `tools/bloc_linguistique.py` et de la doc produit

- **bash** `{"command": "wc -l tools/drave.py tools/bloc_linguistique.py docs/produit/README.md 2>&1; ls docs/produit/", "description": "Count lines of key files"}`

  ```
388 tools/drave.py
  2192 tools/bloc_linguistique.py
   370 docs/produit/README.md
  2950 total
exemples.md
README.md
  ```

- **bash** `{"command": "git log --oneline -5 && git status --short --untracked-files=all -- reports/ | head", "description": "Check recent commits and reports status"}`

  ```
6ef2a3f5 JOURNAL ET ROADMAP — LA VAGUE PRODUIT : DRAVE V0 DOCUMENTÉ, PORTE PRODUIT VERTE, AUTOTEST ×2,4, MASTER POUSSÉ (7f73c17f)
7f73c17f PRODUIT — LA DOC D'USAGE ET LES 5 EXEMPLES VÉRIFIÉS (5/5 REJOUÉS) ; CASCADE_POS N'EST PLUS UNE ROUGE (PLANCHER 0,70)
f6c8132b A23 — LES 6 CORRECTIONS FACTUELLES DE LA FILE (GOLD 200+ = 13 OCCURRENCES, PASSES 2 H 11 À 2 H 29) ; T0 DANS LE BUDGET
fba3072a ÉTAT — T0 DANS LE BUDGET APRÈS LA FILE DES TÂCHES
266b1833 ROADMAP — LA LIGNE S CORRIGÉE (150 VERDICTS HUMAINS, 19 SUR LES PARAGRAPHES) ; LA FILE DES 29 TÂCHES INTÉGRÉE (8 AUTONOMES)
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-spans-chunker.md
?? reports/pensee-produit-bloc-l.json
?? reports/rapport-produit-bloc-l.md
?? reports/rapport-s-paragraphes.md
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """drave.py — le point d'entrée produit du bloc linguistique.
3: 
4: Une seule commande, trois gestes, hors ligne et déterministe :
5: 
6:     python3 tools/drave.py analyser "Le chat dort."
7:     python3 tools/drave.py analyser "The cat sleeps on the roof." --langue en --json
8:     python3 tools/drave.py evaluer
9:     python3 tools/drave.py evaluer --gold --json
10:     python3 tools/drave.py rejouer "Le chat de la voisine qui dort sur le toit se réveille."
11:     python3 tools/drave.py --version
12: 
13: Ce que la commande expose : l'analyse **heuristique** (`Heuristique.analyser`) — POS, syntagmes
14: avec rôle et cible d'attachement, pragmatique, unités sémantiques — et sa mesure sur le gold.
15: Ce qu'elle n'expose pas encore : le neuronal (`llama-cli` ou endpoint local), la restitution
16: (annotation → texte), la traduction et la génération : ils demandent des poids, un service ou
17: un GPU, alors que ce prototype est hors ligne, CPU et sans réseau.
18: 
19: Codes de sortie : 0 succès · 2 usage · 1 erreur (ou refus d'analyse).
20: """
21: 
… [17183 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"^class \\|^def \\|^    def \" tools/bloc_linguistique.py | head -120", "description": "List classes and methods in bloc_linguistique.py"}`

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
8: > **Vérifié le 2026-11-06** sur la branche `s/v7`. Le point d'entrée `tools/drave.py` est
9: > **livré** (version **0.1.0**) : `analyser`, `evaluer`, `rejouer` et `--version` existent, et la
10: > porte produit est verte. Les exemples du § 3 sont réels : ils ont été lancés pour ce document.
11: > Ce qui manque encore au contrat est nommé au § 7, sans être présenté comme acquis.
12: >
13: > **Le produit en une phrase.** Vous donnez un texte ; il rend une **annotation** — langue,
14: > classes de mots, syntagmes, attachements, acte de parole — avec ses spans, sa confiance et ses
15: > candidats, de façon **déterministe**, et il sait **se mesurer** sur un gold de 612 phrases.
16: 
17: ## 1. À qui s'adres
… [22657 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Inspection du cœur d'annotation (`Span`, `Annotation`, `Heuristique.analyser`)

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "offset": 1, "limit": 300}`

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
… [13516 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 160, "offset": 525}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
525: class Heuristique:
526:     """L'implémentation CPU : elle étiquette la surface et **déclare** ce qu'elle ne couvre pas."""
527: 
528:     nom = "heuristique"
529: 
530:     def __init__(self, profils: dict[str, dict] | None = None, segmenter_s: bool = True,
531:                  seuil_ouvert: float = 0.55, seuil_langue: float = 0.12,
532:                  union: bool = True):
533:         self.profils = profils
534:         self.segmenter_s = segmenter_s
535:         self.seuil_ouvert = seuil_ouvert
536:         self.seuil_langue = seuil_langue
537:         self.union = union
538: 
539:     # -- langues / script ---------------------------------------------------
540:     def _langue(self, texte: str, indice: str | None) -> tuple[str, float, str]:
541:         langue, conf, _ = detecter_langue(texte, self.profils, indice)
542:         script = detecter_script(texte)
543:         if conf < self.seuil_langue:
544:             return "und", conf, script
545:         return langue, conf, script
546: 
547:     # -- tokens ---------------------------------------------
… [7192 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 255, "offset": 1003}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
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
1014:         trace.append({"etape": "langue", "langue": lg, "script": script, "confiance": conf_lg,
1015:                       "indice": langue or ""})
1016:         etiquettes: list[Etiquette] = []
1017:         unites: list[Span] = []
1018: 
1019:         # 1. graphème — des plages de classes, pas un caractère par étiquette
1020:         classes = {"L": "lettres", "N": "chiffres", "P":
… [16609 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 320, "offset": 684}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
684:         """Les candidats que le **précédent** impose : l'antécédent d'une REL, le verbe d'une SUB."""
685:         if not precedent:
686:             return []
687:         if segment.get("type") == "REL" and precedent.get("type") == "GN":
688:             tete = Heuristique._tete_nom(texte, precedent["debut"], precedent["fin"])
689:             return [tete] if tete else []
690:         if segment.get("type") == "SUB" and precedent.get("type") == "GV":
691:             v = Heuristique._verbe_dans(texte, precedent["debut"], precedent["fin"])
692:             return [v] if v else []
693:         if segment.get("type") == "GP":
694:             # GP génitif (« de la voisine ») : le nom qu'il complète est un candidat
695:             premier = (segment.get("texte") or "").split()[:1]
696:             if premier and _normaliser(premier[0]) in ("de", "du", "des", "d", "of", "from"):
697:                 if precedent.get("type") == "GN":
698:                     tete = Heuristique._tete_nom(texte, precedent["debut"], precedent["fin"])
699:                     return [t
… [17577 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des tests produit et de la porte existante

- **bash** `{"command": "ls tools/tests/ | head -30; echo ---; sed -n 1,120p tools/tests/test_produit.py 2>/dev/null; echo ---; sed -n 1,80p tools/porte-produit.sh", "description": "Read product test and gate"}`

  ```
code
documents
linguistique
maths
__pycache__
qualifier_politique_drvm.py
qualifier_porte_bouge_drvm.py
qualifier_porte_drvm.py
qualifier_porte_fenetre_drvm.py
qualifier_porte_minute_drvm.py
qualifier_porte_mobile_drvm.py
qualifier_porte_sto_drvm.py
qualifier_porte_sto_graines.py
tableaux
test_pensee_politique.py
test_pensee_store.py
test_produit.py
---
"""test_produit.py — le smoke test de bout en bout du point d'entrée `tools/drave.py`.

Huit assertions, deux phrases (fr/en), le déterminisme et les codes de sortie. Le test passe
aussi bien par `python3 tools/tests/test_produit.py` que par `pytest` : il n'importe rien du
dépôt directement, il lance la commande comme un utilisateur.
"""
from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys
import unittest

RACINE = pathlib.Path(__file__).resolve().parents[2]
CLI = RACINE / "tools" / "drave.py"


def drave(*arguments: str) -> subprocess.CompletedProcess[str]:
    """Lance la commande depuis la racine du dépôt, en UTF-8, sans réseau."""
    return subprocess.run(
        [sys.executable, str(CLI), *arguments],
        cwd=str(RACINE),
        capture_output=True,
        text=True,
    
… [5380 caractères tronqués]
  ```

- **bash** `{"command": "ls tools/tests/linguistique/ 2>/dev/null; echo ---; python3 tools/drave.py --version; echo \"exit=$?\"", "description": "List linguistic tests and check CLI version"}`

  ```
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
---
drave 0.1.0
exit=0
  ```

### 🤖 Assistant

⏵ Lecture de deux rapports récents pour caler le format

- **bash** `{"command": "ls reports/ | grep -i -E \"produit|fia|audit\" | head -20; echo ---; head -c 2500 reports/pensee-produit-bloc-l.json 2>/dev/null", "description": "List product reports and inspect JSON format"}`

  ```
a80-audit-final.json
b1110-audit.json
pensee-audit-attachement.json
pensee-audit.json
pensee-audit-r1r3.json
pensee-audit-v10.json
pensee-audit-v2.json
pensee-audit-v7.json
pensee-produit-bloc-l.json
pensee-produit-v0.json
r06-cascade-confiance.json
rapport-a80-audit-final.md
rapport-audit-attachement.md
rapport-audit-r1r3.md
rapport-audit-v10.md
rapport-audit-v2.md
rapport-audit-v7.md
rapport-b1110-audit.md
rapport-hebbien-produits.md
rapport-pensee-audit.md
---
{
 "rapport": "produit-bloc-l",
 "ligne": "B13",
 "branche": "s/v7",
 "commit": "fa1b0c6eb90b3d27ec78f946d677817ba08b419e",
 "date": "2026-11-06",
 "objet": "Audit de fiabilité produit du bloc linguistique : robustesse hors gold (50 phrases libres), performance, stabilité du contrat, cas limites, compositions et liste de correctifs chiffrés.",
 "verdict": "⚠️ utilisable en surface (graphème, mot, POS fermées, phrase, document) sur du français/anglais propre ; fragile en structure (syntagmes qui se chevauchent, frontières de phrase, compositions, langue). 0 plantage sur 50 phrases, mais 34/50 avec au moins une anomalie de contrat et 1 plantage sur 25 cas limites.",
 "dispositif": {
  "gold": "evaluer_gold.charger() + evalue
… [1744 caractères tronqués]
  ```

- **bash** `{"command": "head -80 reports/rapport-produit-bloc-l.md 2>/dev/null; echo ===; head -50 reports/rapport-audit-v10.md 2>/dev/null", "description": "Inspect recent report markdown styles"}`

  ```
# Audit produit du bloc linguistique — 0 plantage sur 50 phrases, 34/50 avec une anomalie de contrat

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Branche** : `s/v7` ·
> **Commit mesuré** : `fa1b0c6e` (2026-11-06 09:16) · **Date** : 2026-11-06 ·
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

**En une phrase.** Sur 50 phrases libres, le bloc **ne plante pas**, **ne refuse pas**, **ne rend
jamais une sortie vide** et garde **tous les offsets** ; mais **34/50 textes** portent au moins une
anomalie, do
… [7811 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification de l'antériorité d'un rapport voisin (pour ne pas le dupliquer)

- **bash** `{"command": "stat -c '%y %n' reports/pensee-produit-bloc-l.json reports/rapport-produit-bloc-l.md reports/rapport-fiabilite-produit.md reports/pensee-fiabilite-produit.json 2>&1; echo ---; grep -o '\"verdict\"[^,]*' reports/pensee-produit-bloc-l.json | head -2; echo ---; grep -n \"correctif\\|priori … [118 caractères tronqués]`

  ```
2026-11-06 11:22:25.305136552 -0500 reports/pensee-produit-bloc-l.json
2026-11-06 11:13:58.463844021 -0500 reports/rapport-produit-bloc-l.md
stat: cannot statx 'reports/rapport-fiabilite-produit.md': No such file or directory
stat: cannot statx 'reports/pensee-fiabilite-produit.json': No such file or directory
---
"verdict": "⚠️ utilisable en surface (graphème
---
282:- **Priorité par défaut** : `priorite_syntagme="heuristique"` garde le découpage heuristique ; le
294:| # | correctif | preuve chiffrée | lignes | coût | risque |
304:| # | correctif | preuve chiffrée | lignes | coût | risque |
319:| # | correctif | preuve chiffrée | lignes | coût |
323:| **P2-18** | Nettoyages sans effet produit | `_verbe_dans` : boucle dupliquée 777-782 ; `trace` à schéma variable ; `priorite_syntagme="heuristique"` par défaut = mauvais choix pour le tagger réel | 777-782, 116-127, 1931, 1957 | **1 h** |
386:  limites, les 18 correctifs, tous les chiffres et les contrôles.
394:## 11. Les 5 correctifs prioritaires
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\np='reports/pensee-produit-bloc-l.json'\nd=json.load(open(p))\nprint(list(d.keys()))\nprint(json.dumps({k:v for k,v in d.items() if k not in ('banc_50','cas_limites','compositions','performance')}, ensure_ascii=False, indent=1)[:3000])\nPY", "description":  … [34 caractères tronqués]`

  ```
['rapport', 'ligne', 'branche', 'commit', 'date', 'objet', 'verdict', 'dispositif', 'gold', 'banc_50', 'cas_limites', 'performance', 'contrat', 'compositions', 'correctifs', 'controle_negatif', 'limites', 'fichiers']
{
 "rapport": "produit-bloc-l",
 "ligne": "B13",
 "branche": "s/v7",
 "commit": "fa1b0c6eb90b3d27ec78f946d677817ba08b419e",
 "date": "2026-11-06",
 "objet": "Audit de fiabilité produit du bloc linguistique : robustesse hors gold (50 phrases libres), performance, stabilité du contrat, cas limites, compositions et liste de correctifs chiffrés.",
 "verdict": "⚠️ utilisable en surface (graphème, mot, POS fermées, phrase, document) sur du français/anglais propre ; fragile en structure (syntagmes qui se chevauchent, frontières de phrase, compositions, langue). 0 plantage sur 50 phrases, mais 34/50 avec au moins une anomalie de contrat et 1 plantage sur 25 cas limites.",
 "dispositif": {
  "gold": "evaluer_gold.charger() + evaluer_bloc ; gold_split.dev/test ; module tools/bloc_linguistique.py au commit fa1b0c6e (module inchangé à HEAD 6ef2a3f5).",
  "head_au_moment_de_la_redaction": "6ef2a3f5",
  "module_inchange_fa1b0c6e_head": true,
  "evaluateur_modifie": "7f73c17f : casca
… [2013 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Sondage rapide des cas limites avant le harnais complet

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nfor t in \"🚀\" \"...\" \"123\" \"   \" \"a\" \"Élodie sourit.\"; do\n  out=$(python3 tools/drave.py analyser \"$t\" --json 2>/tmp/e); rc=$?\n  echo \"TEXTE=[$t] rc=$rc stdout_len=${#out} stderr=$(head -1 /tmp/e)\"\ndone", "description" … [40 caractères tronqués]`

  ```
TEXTE=[🚀] rc=1 stdout_len=0 stderr=drave: refus d'analyse : vide (le texte doit contenir au moins une lettre ou un chiffre)
TEXTE=[...] rc=1 stdout_len=0 stderr=drave: refus d'analyse : vide (le texte doit contenir au moins une lettre ou un chiffre)
TEXTE=[123] rc=0 stdout_len=2085 stderr=
TEXTE=[   ] rc=1 stdout_len=0 stderr=drave: refus d'analyse : vide (le texte doit contenir au moins une lettre ou un chiffre)
TEXTE=[a] rc=0 stdout_len=2639 stderr=
TEXTE=[Élodie sourit.] rc=0 stdout_len=3881 stderr=
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 tools/drave.py analyser \"Visitez https://example.com/docs?page=2 pour la documentation.\" --json > /tmp/url.json 2>/tmp/url.err; echo \"rc=$?\"; python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/url.json'))\nfor e in d['et … [196 caractères tronqués]`

  ```
rc=0
mot mot 'Visitez' 0 7
phrase type 'déclarative' 0 24
mot mot 'https' 8 13
mot ponctuation ':' 13 14
mot ponctuation '/' 14 15
mot ponctuation '/' 15 16
mot mot 'example' 16 23
mot ponctuation '.' 23 24
mot mot 'com' 24 27
phrase type 'interrogative' 24 33
mot ponctuation '/' 27 28
mot mot 'docs' 28 32
mot ponctuation '?' 32 33
mot mot 'page' 33 37
phrase type 'déclarative' 33 62
mot ponctuation '=' 37 38
mot nombre '2' 38 39
mot mot 'pour' 40 44
mot mot 'la' 45 47
mot mot 'documentation' 48 61
mot ponctuation '.' 61 62
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\n# argument ressemblant à une option\npython3 tools/drave.py analyser \"-3 degrés\" >/tmp/a.out 2>/tmp/a.err; echo \"dash rc=$? err=$(cat /tmp/a.err)\"\npython3 tools/drave.py analyser -- \"-3 degrés\" >/tmp/a.out 2>/tmp/a.err; echo \"d … [571 caractères tronqués]`

  ```
dash rc=0 err=
dash-- rc=0 out=langue=und script=Latn source=heuristique · 12 étiquettes · unités sémantiques=1 (66.7% du texte)
dd rc=2 err=drave analyser: erreur d'usage : the following arguments are required: TEXTE
ff rc=1 outlen=0 err=drave: erreur : UnicodeEncodeError : 'utf-8' codec can't encode character '\udcff' in position 0: surrogates not allowed
affb rc=1 outlen=0 err=drave: erreur : UnicodeEncodeError : 'utf-8' codec can't encode character '\udcff' in position 1: surrogates not allowed
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 - <<'PY'\nimport pathlib\nbase = \"Le chat de la voisine qui dort sur le toit se réveille. \"\np = pathlib.Path('/tmp/t10k.txt')\ntxt = (base * 300)[:10000]\np.write_text(txt, encoding='utf-8')\nprint(len(txt), len(txt.encode() … [439 caractères tronqués]`

  ```
10000 10178
rc=0
wall=0.63 rss=51492kB
etiquettes 10362 syntagmes 893 unites 894
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nLC_ALL=C python3 tools/drave.py analyser \"Élodie sourit.\" >/tmp/c.out 2>/tmp/c.err; echo \"LC_ALL=C rc=$? out=$(wc -c </tmp/c.out)\"; cat /tmp/c.err\nPYTHONIOENCODING=ascii python3 tools/drave.py analyser \"Élodie sourit.\" >/tmp/c.o … [268 caractères tronqués]`

  ```
LC_ALL=C rc=0 out=473
ascii rc=1 out=0
drave: erreur : UnicodeEncodeError : 'ascii' codec can't encode character '\u2014' in position 12: ordinal not in range(128)
C-noaccent rc=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nset -o pipefail\npython3 tools/drave.py analyser \"Le chat de la voisine qui dort sur le toit se réveille.\" --json 2>/tmp/p.err | head -c 100 >/dev/null\necho \"pipe statuses=${PIPESTATUS[*]}\"; cat /tmp/p.err\npython3 tools/drave.py  … [254 caractères tronqués]`

  ```
pipe statuses=0 0
'déclarative' 0 8
'déclarative' 8 15
  ```

- **bash** `{"command": "sed -n '150,340p' reports/rapport-produit-bloc-l.md", "description": "Read existing report contract and fixes sections"}`

  ```
détail de bord : un client qui construit un arbre, un index par offset ou une partition de la
phrase casse sur près d'un texte sur deux. Et le chunker simple, seul, ne produit **aucun**
chevauchement (`Heuristique(segmenter_s=False, union=False)` : 0) : le problème vient du
générateur S et de l'union, pas de la tokénisation.

**Autres écarts de forme** : **60 étiquettes phrase** pour 50 textes (6 textes multi-phrases),
dont **6 spans commencent par un espace** ; **53 étiquettes document**, dont **42 valeurs
tronquées à 60 caractères** et **2 titres** (x46, vrai titre markdown ; x48, faux titre chinois) ;
**graphème** : 49/50 textes à 100 %, x46 à **95,14 %** (7 newlines, catégorie `Cc`, non couvertes).

### 3.3 Qualité observable (sans gold libre)

- **POS ouvertes** : 365 `NOUN` pour 32 `VERB` sur les 50 textes. f02 : « arrose », « rentre »,
  « prépare » → `NOUN` ; e29 : « warm » → `NOUN`. Le gold mesure 0,6234 sur l'ouvert ; les
  exemples libres sont cohérents avec cette faiblesse.
- **Nombres, dates, URL** : « 12.5 » coupe la phrase en **deux fragments** ; « 12.03.2024 » en
  **trois** ; « 12,5 » (virgule) ne coupe pas la phrase mais découpe le nombre en `12`, `,`, `5`.
  Une 
… [16659 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification de la ligne de roadmap et de l'environnement de mesure

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ndate '+%Y-%m-%d %H:%M'; python3 -V; nproc; lscpu | grep -m1 'Model name'; git rev-parse HEAD; git status --short --untracked-files=no | wc -l\ngrep -n -i \"produit\" docs/pilotage/roadmap.md | head -15", "description": "Check date, env … [27 caractères tronqués]`

  ```
2026-11-06 11:33
Python 3.13.16
40
Model name:                              Intel(R) Xeon(R) CPU E5-2687W v3 @ 3.10GHz
c6904284dff1ad090b67939597911d914ee34873
96
38:**État au 06/11 11 h 15.** B13 est à **183/183** ; **attachement 222/222 (1,0000)** (fr 136/136, en 86/86), **couverture 0,9289** ; dev 153/153, test 69/69 ; **le premier produit est debout et documenté** : `python3 tools/drave.py analyser|evaluer|rejouer`, **porte produit** (6 contrôles, ~2 min), **doc d'usage** (`docs/produit/`) et 5 exemples rejoués ; **autotest parallèle** (×2,4) ; **84 portes, 3 rouges** (`indice`, `melange`, `sessions` du hub) ; **17 spans** inatteignables ; **file des 29 tâches** (8 autonomes) ; `master` et `s/v7` poussés à `7f73c17f` ;
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nsed -n '1,80p' docs/pilotage/roadmap.md | head -80", "description": "Read roadmap header"}`

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
… [13228 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 45, "offset": 455}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
455: 
456: ADVERBES_SEULS = {"peut-être", "vite", "bien", "mal", "hier", "demain", "aujourd'hui", "ici",
457:                   "là", "souvent", "toujours", "jamais", "déjà", "encore", "enfin", "alors",
458:                   "puis", "donc", "aussi", "très", "trop", "plus", "moins", "maybe", "perhaps"}
459: 
460: 
461: def _est_adverbe_seul(g: dict) -> bool:
462:     """Un GV d'un seul token adverbe n'est pas un gouverneur (« Peut-être »)."""
463:     return (len((g.get("texte") or "").split()) == 1
464:             and _normaliser(g.get("texte") or "") in ADVERBES_SEULS)
465: 
466: 
467: MODAUX = {"would", "must", "can", "could", "should", "will", "shall", "may", "might", "ought",
468:           "could", "cannot"}
469: 
470: ENCLITIQUES = ("-moi", "-toi", "-nous", "-vous", "-le", "-la", "-les", "-lui", "-leur", "-y", "-en")
471: 
472: 
473: def _sans_enclitique(mot: str) -> str:
474:     """`appelle-moi` → `appelle` (les enclitiques ne font pas partie de la tête)."""
475:     for suf in ENCLITIQUES:
476:         if mot.endswith(suf) and len(mot) > len(suf):
477:     
… [989 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 - <<'PY'\nimport json,subprocess,sys\ndef run(t):\n    p=subprocess.run([sys.executable,'tools/drave.py','analyser',t,'--json'],capture_output=True,text=True)\n    return p\nfor t in [\"M. Dupont, le Dr Martin et Mme Leroy sont … [610 caractères tronqués]`

  ```
TEXTE 'M. Dupont, le Dr Martin et Mme Leroy sont arrivés vers 9 h.' rc 0
 phrase 0 59 'M. Dupont, le Dr Martin et Mme Leroy sont arrivés vers 9 h.' déclarative
 phrase 2 59 ' Dupont, le Dr Martin et Mme Leroy sont arrivés vers 9 h.' déclarative
 ligne lisible: []
TEXTE 'Le Dr. Martin est arrivé hier. Il repart demain.' rc 0
 phrase 0 30 'Le Dr. Martin est arrivé hier.' déclarative
 phrase 6 30 ' Martin est arrivé hier.' déclarative
 phrase 30 48 ' Il repart demain.' déclarative
 ligne lisible: []
TEXTE 'Bonjour. Salut.' rc 0
 phrase 0 8 'Bonjour.' déclarative
 phrase 8 15 ' Salut.' déclarative
 ligne lisible: []
TEXTE 'The cat sleeps.' rc 0
 phrase 0 15 'The cat sleeps.' déclarative
 ligne lisible: []
  ```

### 🤖 Assistant

⏵ Écriture du harnais d'audit CLI (50 phrases, contrat, temps)

- **write** `{"file_path": "/tmp/audit_cli.py", "content": "#!/usr/bin/env python3\n\"\"\"Audit CLI de drave.py — 50 phrases libres + robustesse + contrat. Écrit /tmp/audit_cli_results.json.\"\"\"\nfrom __future__ import annotations\n\nimport hashlib\nimport json\nimport os\nimport pathlib\nimport subprocess\nim … [27713 caractères tronqués]`

  ```
<path>/tmp/audit_cli.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'PY'\nimport re\np='/tmp/audit_cli.py'\ns=open(p).read()\ns=s.replace('''    doublons = {}\n''','''    doublons = {}\n''')\ns=s.replace('''    doublons = {k: v for k, v in vus.items() if v > 1}\n''','''    doublons = {k: v for k, v in vus.items() if v > 1}\n    do … [970 caractères tronqués]`

  ```
patched
OK
  ```

### 🤖 Assistant

⏵ Lancement du banc complet (50 phrases + robustesse + timings)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 /tmp/audit_cli.py 2>&1 | tee /tmp/audit_cli.log | tail -40", "description": "Run full CLI audit harness", "timeoutMs": 900000}`

  ```
f50 rc=0 wall=  226.6ms json=True labels=1990 ovl={'discours': {'paires': 7, 'etiquettes': 11, 'exemples': [['connecteur', 0, 182, 'paragraphe', 0, 716], ['paragraphe', 0, 716, 'connecteur', 182, 268], ['connecteur', 716, 974, 'paragraphe', 718, 1156]]}, 'phrase': {'paires': 5, 'etiquettes': 24, 'exemples': [['type', 454, 716, 'négation', 454, 716], ['type', 716, 974, 'négation', 716, 974], ['type', 1363, 1444, 'négation', 1363, 1444]]}, 'pragmatique': {'paires': 6, 'etiquettes': 25, 'exemples': [['acte', 0, 182, 'double_sens', 0, 182], ['acte', 1065, 1130, 'double_sens', 1065, 1130], ['acte', 1277, 1363, 'double_sens', 1277, 1363]]}, 'syntagme': {'paires': 50, 'etiquettes': 171, 'exemples': [['GP', 8, 26, 'GP', 8, 40], ['GP', 8, 40, 'GP', 27, 40], ['REL', 41, 61, 'REL', 41, 97]]}}
== temps API ==
== robustesse ==
rob version: rc=0 out=12 stderr=''
rob aide: rc=0 out=770 stderr=''
rob sans_commande: rc=2 out=0 stderr="usage: drave [-h] [-V] {analyser,evaluer,rejouer} ...\ndrave: erreur d'usage : the followin"
rob commande_inconnue: rc=2 out=0 stderr="usage: drave [-h] [-V] {analyser,evaluer,rejouer} ...\ndrave: erreur d'usage : argument {an"
rob analyser_sans_texte: rc=2 out=0 stde
… [2554 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Dépouillement du banc : synthèse et anomalies

- **bash** `{"command": "cd /tmp && head -55 audit_cli.log", "description": "Read benchmark per-sentence output"}`

  ```
== benchmark 50 ==
f01 rc=0 wall=  150.8ms json=True labels=19 ovl={}
f02 rc=0 wall=  193.9ms json=True labels=59 ovl={'syntagme': {'paires': 2, 'etiquettes': 5, 'exemples': [['REL', 22, 42, 'REL', 22, 54], ['REL', 22, 54, 'GV', 43, 54]]}}
f03 rc=0 wall=  149.9ms json=True labels=37 ovl={}
f04 rc=0 wall=  157.2ms json=True labels=38 ovl={}
f05 rc=0 wall=  181.6ms json=True labels=30 ovl={'phrase': {'paires': 1, 'etiquettes': 2, 'exemples': [['type', 0, 20, 'négation', 0, 20]]}, 'syntagme': {'paires': 1, 'etiquettes': 3, 'exemples': [['GP', 14, 18, 'GN', 16, 18]]}}
f06 rc=0 wall=  154.1ms json=True labels=62 ovl={'discours': {'paires': 1, 'etiquettes': 2, 'exemples': [['connecteur', 0, 61, 'paragraphe', 0, 61]]}, 'phrase': {'paires': 1, 'etiquettes': 2, 'exemples': [['type', 0, 61, 'négation', 0, 61]]}, 'syntagme': {'paires': 4, 'etiquettes': 6, 'exemples': [['GV', 0, 15, 'GV', 3, 36], ['GV', 3, 36, 'SUB', 16, 29], ['GV', 3, 36, 'GP', 30, 36]]}}
f07 rc=0 wall=  149.3ms json=True labels=32 ovl={}
f08 rc=0 wall=  149.7ms json=True labels=37 ovl={}
f09 rc=0 wall=  145.2ms json=True labels=33 ovl={'discours': {'paires': 1, 'etiquettes': 2, 'exemples': [['connecteur', 0, 36, 'paragraphe'
… [7191 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'PY'\nimport json\nd=json.load(open('audit_cli_results.json'))\nb=d['banc_50']\nprint('n=',len(b))\nprint('rcs', {r['rc'] for r in b})\nprint('json ok', sum(1 for r in b if r.get('json') is True), 'refus', sum(1 for r in b if r['rc']==1))\nprint('determinisme', su … [1883 caractères tronqués]`

  ```
n= 50
rcs {0, 1}
json ok 46 refus 4
determinisme 50 / 50
stderr non vide succès []
tracebacks []
span_hors 0 []
surface_ko 4 ['f03', 'f11', 'f19', 'f29']
cles_label_ko 0
types_inconnus 0
cibles_absentes 0
sans_attachement 76
sans_pos 0
unites_hors 0 unites_chev 0
fraction_ecart max 5e-05
phrase_leading 19 ['f03', 'f20', 'f25', 'f26', 'f29', 'f50']
overlap texts 28
syntagme overlap pairs total 107
phrase overlap pairs total 14
doc titles [('f18', ['1234567890']), ('f31', ['ÇA NE MARCHE PAS !!!']), ('f50', ['# Notes de terrain\nLe chat de la voisine qui dort sur le toi', '## Le protocole\nNous avons observé pendant 30 jours, de 6 h ', '## Ce que nous croyons savoir\nUne question reste ouverte : p', '## Annexes\nVisitez https://example.org/corpus/2026?page=3 po'])]
langues {'en', 'it', 'fr', 'und'}
temps wall ms: min/med/max 136.77 153.01 226.64
temps med hors startup approx 153.01
json sizes max 533611
  ```

