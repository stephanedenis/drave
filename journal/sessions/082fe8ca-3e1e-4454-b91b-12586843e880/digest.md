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

### 🤖 Assistant

⏵ Analyse détaillée des anomalies (surface, cibles, langue, chevauchements)

- **bash** `{"command": "cd /tmp && python3 - <<'PY'\nimport json\nd=json.load(open('audit_cli_results.json'))\nb={r['id']:r for r in d['banc_50']}\nfor i in ['f03','f11','f19','f29']:\n    print(i, json.dumps(b[i]['exemples']['surface_ko'], ensure_ascii=False))\n    print('  texte:', repr(b[i].get('phrase_text … [1220 caractères tronqués]`

  ```
f03 [{"niveau": "morphème", "type": "préfixe", "valeur": "co", "tranche": "Co"}]
  texte: ['Bonjour !', " Comment allez-vous aujourd'hui ?"]
f11 [{"niveau": "morphème", "type": "préfixe", "valeur": "re", "tranche": "Re"}]
  texte: ['Rendez-vous le 12/03/2026 à 14h30.']
f19 [{"niveau": "morphème", "type": "préfixe", "valeur": "co", "tranche": "CO"}]
  texte: ["COVID-19 : la situation s'améliore-t-elle vraiment ?"]
f29 [{"niveau": "morphème", "type": "préfixe", "valeur": "re", "tranche": "Re"}]
  texte: ['Il a dit : « Rentre avant minuit.', ' »']
--- langues
f13 und ["J'ai trouvé ça génial 😍🔥"]
f18 und ['1234567890']
f27 und ['Élodie sourit.']
f33 it ['Si tu viens, apporte le dessert.']
f37 und ['Email: alice@example.', 'org, phone: +33 6 12 34 56 78.']
f48 und ['Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.']
--- tokens_non_pos total 302 [('f01', 1), ('f02', 1), ('f03', 2), ('f04', 2), ('f05', 1), ('f06', 2), ('f07', 1), ('f08', 2), ('f09', 1), ('f10', 7), ('f11', 7), ('f12', 9), ('f13', 2), ('f18', 1), ('f19', 2), ('f20', 4), ('f21', 4), ('f22', 3), ('f23', 2), ('f24', 3), ('f25', 2), ('f26', 2), ('f27', 
… [4138 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'PY'\nimport subprocess, sys, os\nR='/home/stephane/Data13TB/stephane/GitHub/Qtrinet'\nfor args in ([b'\\xff'], [b'a\\xffb']):\n    cmd=[sys.executable, R+'/tools/drave.py', 'analyser', *args]\n    p=subprocess.run(cmd,cwd=R,capture_output=True)\n    print('bytes  … [530 caractères tronqués]`

  ```
bytes args [b'\xff'] rc 1 out 0 err b"drave: refus d'analyse : vide (le texte doit contenir au moins une lettre ou un chiffre)\n"
bytes args [b'a\xffb'] rc 1 out 0 err b"drave: erreur : UnicodeEncodeError : 'utf-8' codec can't encode character '\\udcff' in position 231: surrogates not allowed\n"
str surrogate '\udcff' rc 1 out 0 err drave: refus d'analyse : vide (le texte doit contenir au moins une lettre ou un chiffre)

str surrogate 'a\udcffb' rc 1 out 0 err drave: erreur : UnicodeEncodeError : 'utf-8' codec can't encode character '\udcff' in position 231: surrogates not allowed
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 - <<'PY'\nimport subprocess,sys,os\nR=os.getcwd()\np=subprocess.run([sys.executable,'-c','import sys; print([repr(a) for a in sys.argv])','analyser',b'\\xff'],capture_output=True)\nprint('argv bytes:',p.stdout,p.stderr)\np=subp … [553 caractères tronqués]`

  ```
argv bytes: b'["\'-c\'", "\'analyser\'", "\'\\\\udcff\'"]\n' b''
cli bytes: 1 b'' b"drave: refus d'analyse : vide (le texte doit contenir au moins une lettre ou un chiffre)\n"
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 7, in <module>
ModuleNotFoundError: No module named 'bloc_linguistique'
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 - <<'PY'\nimport sys; sys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nfor s in ['\\udcff','a\\udcffb']:\n    print('repr',repr(s),'isalpha',any(c.isalpha() for c in s))\n    try:\n        a=bl.Heuristique().analyser … [212 caractères tronqués]`

  ```
repr '\udcff' isalpha False
  refus 'vide' etiquettes 0 cout {'octets': 1, 'duree_s': 9e-06}
repr 'a\udcffb' isalpha True
  refus '' etiquettes 13 cout {'octets': 3, 'caracteres': 3, 'etiquettes': 13, 'duree_s': 0.00537}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 - <<'PY'\nimport subprocess,sys,os\n# instrument drave by running a copy that prints argv repr\nsrc=open('tools/drave.py').read()\nsrc=src.replace('if __name__ == \"__main__\":', 'if __name__ == \"__main__\":\\n    print(\"ARGV … [321 caractères tronqués]`

  ```
rc 1
ERR b'Traceback (most recent call last):\n  File "/tmp/drave_dbg.py", line 40, in <module>\n    import bloc_linguistique as bl  # noqa: E402  (import apr\xc3\xa8s l\'installation des chemins)\n    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nModuleNotFoundError: No module named \'bloc_linguistique\'\n'
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys\nprint(sys.version)\ns='\\udcff'\nfor errors in (None,'strict','surrogateescape','replace'):\n    try:\n        b=s.encode() if errors is None else s.encode(errors=errors)\n        print(errors, b, len(b))\n    except Exception as e:\n        print(errors,'E … [134 caractères tronqués]`

  ```
3.13.16 (main, Oct 16 2026, 19:23:15) [GCC]
None EXC UnicodeEncodeError 'utf-8' codec can't encode character '\udcff' in position 0: surrogates not allowed
strict EXC UnicodeEncodeError 'utf-8' codec can't encode character '\udcff' in position 0: surrogates not allowed
surrogateescape b'\xff' 1
replace b'?' 1
b'\xed\xb3\xbf'
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nstat -c '%y %n' tools/bloc_linguistique.py tools/drave.py; git status --short tools/bloc_linguistique.py tools/drave.py; sed -n '1003,1013p' tools/bloc_linguistique.py; grep -n \"def analyser\" tools/bloc_linguistique.py | head", "desc … [55 caractères tronqués]`

  ```
2026-11-06 11:34:28.080011149 -0500 tools/bloc_linguistique.py
2026-11-06 09:55:57.489575761 -0500 tools/drave.py
M  tools/bloc_linguistique.py
    def analyser(self, texte: str, langue: str | None = None,
                 contexte: str | None = None) -> Annotation:
        t0 = time.perf_counter()
        if not isinstance(texte, str):
            # une entrée non textuelle est **refusée** proprement (le produit ne plante pas)
            return Annotation(texte=str(texte)[:200], refus="non_texte", source=self.nom,
                              trace=[{"etape": "refus", "raison": "non_texte",
                                      "type": type(texte).__name__}],
                              cout={"octets": 0, "duree_s": round(time.perf_counter() - t0, 6)})
        texte = texte or ""
        trace: list[dict] = []
133:    def analyser(self, texte: str, langue: str | None = None,
1003:    def analyser(self, texte: str, langue: str | None = None,
1282:    def analyser(self, texte: str, langue: str | None = None,
1351:    def analyser(self, texte: str, langue: str | None = None,
1461:    def analyser(self, texte: str, langue: str | None = None,
1595:    def analyser(self, texte: str,
… [295 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 - <<'PY'\nimport sys; sys.path.insert(0,'tools')\nimport bloc_linguistique as bl, inspect\nsrc=inspect.getsource(bl.Heuristique.analyser)\nprint(src[:600])\nprint('module',bl.__file__)\nPY", "description": "Inspect loaded analy … [12 caractères tronqués]`

  ```
def analyser(self, texte: str, langue: str | None = None,
                 contexte: str | None = None) -> Annotation:
        t0 = time.perf_counter()
        if not isinstance(texte, str):
            # une entrée non textuelle est **refusée** proprement (le produit ne plante pas)
            return Annotation(texte=str(texte)[:200], refus="non_texte", source=self.nom,
                              trace=[{"etape": "refus", "raison": "non_texte",
                                      "type": type(texte).__name__}],
                              cout={"octets": 0, "duree_s": round(time.pe
module /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py
  ```

### 🤖 Assistant

⏵ Un pair a modifié `bloc_linguistique.py` pendant l'audit : je fige l'état mesuré

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngit diff HEAD --stat -- tools/bloc_linguistique.py tools/drave.py; echo ---; git diff HEAD -- tools/bloc_linguistique.py | head -120; echo ---; sha256sum tools/bloc_linguistique.py tools/drave.py; git hash-object tools/bloc_linguistiqu … [84 caractères tronqués]`

  ```
---
---
084517d9c10088b3adedc01658adbb33e3de69e7f5ca8c2f563f427abdd79f4f  tools/bloc_linguistique.py
59a06f3e4f7d633ae8caa30412fd4c01e14374914226f5e54629f544e47aea8c  tools/drave.py
c1a0858841b9128e1f9743d164b903e243454e5e
7c715a34926827fe4810997e869de972793de827
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngit log --oneline -6; echo ---; git diff --stat 6ef2a3f5..HEAD -- tools/bloc_linguistique.py tools/drave.py; echo ---; git diff 6ef2a3f5..HEAD -- tools/bloc_linguistique.py | head -160", "description": "Show new commits and module diff … [20 caractères tronqués]`

  ```
1962eb15 PRODUIT — LA ROBUSTESSE : SURROGATE ET NON-STR FERMÉS (refus non_texte), 8 TESTS ; L'AUDIT A24 (50 PHRASES, 132 CHEVAUCHEMENTS, 18 CORRECTIFS)
c6904284 ÉTAT — T0 À 4 000
37e2053c ÉTAT — T0 DANS LE BUDGET
5c6b3b43 PORTES — LA NUANCE cascade_pos : VERTE PAR PLANCHER, LA FUSION DÉGRADE ENCORE LE POS DE 1,16 PT (CORRECTIF À FAIRE)
e3db2cc8 OUTILLAGE — index_reports A UNE AIDE (--aide N'ÉCRIT PLUS), --verifier, INDEX 625 → 677 FICHES ; PLAN-TRAVAIL § 9 → § 13
6ef2a3f5 JOURNAL ET ROADMAP — LA VAGUE PRODUIT : DRAVE V0 DOCUMENTÉ, PORTE PRODUIT VERTE, AUTOTEST ×2,4, MASTER POUSSÉ (7f73c17f)
---
 tools/bloc_linguistique.py | 28 +++++++++++++++++-----------
 1 file changed, 17 insertions(+), 11 deletions(-)
---
diff --git a/tools/bloc_linguistique.py b/tools/bloc_linguistique.py
index 8f1b658f..c1a08588 100644
--- a/tools/bloc_linguistique.py
+++ b/tools/bloc_linguistique.py
@@ -1003,12 +1003,18 @@ class Heuristique:
     def analyser(self, texte: str, langue: str | None = None,
                  contexte: str | None = None) -> Annotation:
         t0 = time.perf_counter()
+        if not isinstance(texte, str):
+            # une entrée non textuelle est **refusée** proprement (le p
… [7242 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngit log -1 --format='%H %ci %s' -- tools/bloc_linguistique.py; stat -c '%y' tools/bloc_linguistique.py; git status --short tools/bloc_linguistique.py tools/drave.py; echo ---; sha256sum tools/bloc_linguistique.py tools/drave.py", "desc … [46 caractères tronqués]`

  ```
1962eb15a2dc709649ec3baa62c8bfb58827f78c 2026-11-06 11:43:06 -0500 PRODUIT — LA ROBUSTESSE : SURROGATE ET NON-STR FERMÉS (refus non_texte), 8 TESTS ; L'AUDIT A24 (50 PHRASES, 132 CHEVAUCHEMENTS, 18 CORRECTIFS)
2026-11-06 11:34:28.080011149 -0500
---
084517d9c10088b3adedc01658adbb33e3de69e7f5ca8c2f563f427abdd79f4f  tools/bloc_linguistique.py
59a06f3e4f7d633ae8caa30412fd4c01e14374914226f5e54629f544e47aea8c  tools/drave.py
  ```

- **bash** `{"command": "stat -c '%y %n' /tmp/audit_cli_results.json /tmp/audit_cli.log /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py; date '+%Y-%m-%d %H:%M:%S'", "description": "Compare harness and module timestamps"}`

  ```
2026-11-06 11:40:32.317732641 -0500 /tmp/audit_cli_results.json
2026-11-06 11:40:32.317732641 -0500 /tmp/audit_cli.log
2026-11-06 11:34:28.080011149 -0500 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py
2026-11-06 11:48:32
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nfor s in $'\\xff' $'a\\xffb'; do\n  python3 tools/drave.py analyser \"$s\" >/tmp/x.out 2>/tmp/x.err; echo \"rc=$? out=$(wc -c </tmp/x.out) err=$(cat /tmp/x.err)\"\ndone\npython3 - <<'PY'\nimport sys; sys.path.insert(0,'tools')\nimport  … [292 caractères tronqués]`

  ```
rc=1 out=0 err=drave: refus d'analyse : vide (le texte doit contenir au moins une lettre ou un chiffre)
rc=1 out=0 err=drave: erreur : UnicodeEncodeError : 'utf-8' codec can't encode character '\udcff' in position 231: surrogates not allowed
NoneType refus= 'non_texte' texte= 'None' etiquettes= 0 cout= {'octets': 0, 'duree_s': 6e-06}
int refus= 'non_texte' texte= '3' etiquettes= 0 cout= {'octets': 0, 'duree_s': 5e-06}
list refus= 'non_texte' texte= '[1, 2]' etiquettes= 0 cout= {'octets': 0, 'duree_s': 4e-06}
bytes refus= 'non_texte' texte= "b'abc'" etiquettes= 0 cout= {'octets': 0, 'duree_s': 4e-06}
  ```

### 🤖 Assistant

⏵ Classification fine des chevauchements, cibles et POS manquantes

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"Détail des anomalies du banc CLI (relit /tmp/audit_cli_results.json pour la liste des textes).\"\"\"\nfrom __future__ import annotations\n\nimport json\nimport pathlib\nimport subprocess\nimport sys\n\nRACINE = pathlib.Path(\"/home/stephane/Data13TB/stephan … [10588 caractères tronqués]`

  ```
<path>/tmp/audit_cli_detail.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 /tmp/audit_cli_detail.py 2>&1 | tail -40", "description": "Run detailed overlap/target analysis", "timeoutMs": 300000}`

  ```
Traceback (most recent call last):
  File "/tmp/audit_cli_detail.py", line 212, in <module>
    main()
    ~~~~^^
  File "/tmp/audit_cli_detail.py", line 43, in main
    p, d = run(texte)
           ~~~^^^^^^^
  File "/tmp/audit_cli_detail.py", line 36, in run
    d = json.loads(p.stdout.decode("utf-8"))
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

- **bash** `{"command": "cd /tmp && python3 - <<'PY'\np='/tmp/audit_cli_detail.py'\ns=open(p).read()\ns=s.replace('''    d = json.loads(p.stdout.decode(\"utf-8\"))\n    return p, d\n''','''    d = json.loads(p.stdout.decode(\"utf-8\")) if p.returncode == 0 else None\n    return p, d\n''')\nopen(p,'w').write(s)\ … [195 caractères tronqués]`

  ```
n 50
langues attendues/observées:
Counter({('fr', 'fr'): 35, ('en', 'en'): 5, ('fr', 'und'): 5, ('refus', None): 4, ('fr', 'it'): 1})
syntagmes par type (somme):
{'GN': {'total': 87, 'attaches': 83, 'sans': 4, 'union': 11, 'conflits_textes': 0}, 'GV': {'total': 145, 'attaches': 75, 'sans': 70, 'union': 35, 'conflits_textes': 0}, 'GP': {'total': 86, 'attaches': 84, 'sans': 2, 'union': 28, 'conflits_textes': 0}, 'REL': {'total': 28, 'attaches': 28, 'sans': 0, 'union': 10, 'conflits_textes': 0}, 'SUB': {'total': 14, 'attaches': 14, 'sans': 0, 'union': 1, 'conflits_textes': 0}}
GN textes 28 sans 4 total 87
GP textes 24 sans 2 total 86
REL textes 9 sans 0 total 28
SUB textes 8 sans 0 total 14
GV textes 36 sans 70 total 145
conflits sans union 0
conflits après filtre union 0
textes conflits après filtre []
trous POS: {}
{'mot': {'total': 766, 'sans_pos': 0}, 'ponctuation': {'total': 257, 'sans_pos': 257}, 'nombre': {'total': 45, 'sans_pos': 45}}
cibles fermées 18 Counter({'ADV': 9, 'AUX': 4, 'DET': 4, 'PRON': 1})
cibles absentes 0
phrase chevauchement type 1 [('f20', 1)]
phrases espaces initiaux 19 [('f03', 1), ('f20', 1), ('f25', 1), ('f26', 1), ('f29', 1), ('f50', 14)]
documents 49 tro
… [565 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification de `evaluer`, des codes de sortie et du contrat de refus

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 - <<'PY'\nimport subprocess,sys,json,time\nR='.'\ndef run(*a):\n    t=time.perf_counter(); p=subprocess.run([sys.executable,'tools/drave.py',*a],capture_output=True,text=True); return p,(time.perf_counter()-t)*1000\nfor args in … [641 caractères tronqués]`

  ```
('evaluer', '--json') rc 0 ms 536.4 bytes 2746 err 
 keys ['version', 'gold', 'heuristique', 'controle_negatif']
 gold {'nom': 'vivant (hand + reel + synthétique)', 'gele': False, 'phrases': 612, 'tokens': 3179, 'cibles_attachement': 239}
 pos {'exactitude': 0.7581, 'exactitude_ferme': 0.9004, 'exactitude_ouvert': 0.6234, 'tokens': 3179, 'confusions': {'ADJ': {'ADJ': 50, 'NOUN': 80, 'VERB': 4}, 'ADV': {'ADV': 117, 'NOUN': 20, 'PREP': 2, 'ADJ': 1, '?': 1}, 'AUX': {'PREP': 4, 'AUX': 118, '?': 3, 'NOUN': 3}, 'CONJ': {'CONJ': 44, 'PRON': 25, 'DET': 12, '?': 13, 'PREP': 2, 'NOUN': 2}, 'DET': {'DET': 586, '?': 2}, 'NOUN': {'NOUN': 657, 'ADJ': 17, 'VERB': 7, '?': 1}, 'NUM': {'NUM': 2}, 'PONCT': {'?': 25}, 'PREP': {'PREP': 114}, 'PRON': {'PRON': 411, 'NOUN': 8, '?': 30, 'DET': 25, 'CONJ': 1}, 'VERB': {'VERB': 311, 'NOUN': 450, 'ADJ': 5, 'PREP': 2, '?': 16, 'AUX': 7, 'ADV': 1}}}
 syn {'precision': 0.6292, 'rappel': 0.5464, 'f1': 0.5849, 'tp': 1018, 'fp': 600, 'fn': 845, 'tete': {'precision': 0.81, 'rappel': 0.6704, 'f1': 0.7336, 'tp': 1249, 'fp': 293, 'fn': 614}}
 att {'cibles': 239, 'labels': 222, 'top1': 222, 'topk': 221, 'exact': 222, 'top1_taux': 0.9289, 'topk_taux': 0.9247, 'exact_taux
… [2762 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\necho '--- refus JSON'; python3 tools/drave.py analyser \"\" --json >/tmp/r.out 2>/tmp/r.err; echo \"rc=$? stdout=$(wc -c </tmp/r.out) stderr=$(cat /tmp/r.err)\"\necho '--- rejouer refus'; python3 tools/drave.py rejouer \"\" >/tmp/r.out … [515 caractères tronqués]`

  ```
--- refus JSON
rc=1 stdout=0 stderr=drave: refus d'analyse : vide (le texte doit contenir au moins une lettre ou un chiffre)
--- rejouer refus
rc=1 stdout=0 stderr=drave: refus d'analyse : vide (le texte doit contenir au moins une lettre ou un chiffre)
--- depuis /tmp
rc=0 bytes=5561 err=
--- code 3/4
  ```

### 🤖 Assistant

⏵ Relevé des lignes exactes pour la liste de correctifs

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngrep -n \"def _mots\\|def _phrases\\|def _pos\\|def _morphemes\\|def _syntagmes_simple\\|def _supprimer_chevauchements\\|def _verbe_dans\\|def detecter_langue\\|def json\\|def couverture\\|def analyser\\|unites_semantiques\\|fraction_s … [415 caractères tronqués]`

  ```
20:La couche sémantique ne reçoit que `unites_semantiques` ; l'heuristique peut donc l'activer à
63:    def json(self) -> dict:
81:    def json(self) -> dict:
100:    unites_semantiques: list[Span] = field(default_factory=list)
101:    fraction_semantique: float = 0.0
111:    def couverture(self) -> dict[str, float]:
116:    def json(self, avec_duree: bool = False) -> dict:
124:            "unites_semantiques": [u.json() for u in self.unites_semantiques],
125:            "fraction_semantique": round(float(self.fraction_semantique), 4),
133:    def analyser(self, texte: str, langue: str | None = None,
199:def detecter_langue(texte: str, profils: dict[str, dict] | None = None,
549:    def _mots(texte: str) -> list[tuple[int, int, str, str]]:
568:    def _phrases(texte: str) -> list[tuple[int, int, str, str]]:
601:    def _pos(self, langue: str, mot: str) -> tuple[str, bool, float]:
627:    def _morphemes(mot: str) -> list[tuple[str, int, int, str]]:
770:    def _verbe_dans(texte: str, debut: int, fin: int,
855:    def _syntagmes_simple(self, texte: str, langue: str,
1003:    def analyser(self, texte: str, langue: str | None = None,
1145:                    meta = {"role": s.get("role
… [3337 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nsed -n '1210,1260p' tools/bloc_linguistique.py; echo ===; sed -n '1810,1860p' tools/bloc_linguistique.py", "description": "Inspect document and overlap-removal code"}`

  ```
prec = s
    
        # 6. discours / document
        for d, f, p, _ in self._phrases(texte):
            mots_p = set(_normaliser(p).split())
            for relation, marqueurs in CONNECTEURS.items():
                touche = sorted(mots_p & marqueurs)
                if touche:
                    etiquettes.append(Etiquette("discours", "connecteur", touche[0], d, f,
                                                self.nom, 0.55, candidats=[relation],
                                                langue=lg, script=script))
                    break
        paragraphes = []
        for m in re.finditer(r"[^\n]+(?:\n(?!\s*\n)[^\n]+)*", texte):
            if m.group().strip():
                paragraphes.append((m.start(), m.end(), m.group()))
        for d, f, p in paragraphes:
            etiquettes.append(Etiquette("discours", "paragraphe", "suite", d, f, self.nom, 0.5,
                                        candidats=["suite", "contraste", "cause", "conséquence"],
                                        langue=lg, script=script))
            titre = (p.lstrip().startswith("#") or
                     bool(re.match(r"^\s*(?:\d+[.)]|[IVXLC]+[.)])\s+", p)) or
                
… [4709 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Inventaire du contrat de sortie (clés, types, valeurs vides)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 - <<'PY'\nimport json,subprocess,sys,collections,importlib.util\nR='.'\nspec=importlib.util.spec_from_file_location('a','/tmp/audit_cli.py'); a=importlib.util.module_from_spec(spec); spec.loader.exec_module(a)\nTOP=collections. … [1995 caractères tronqués]`

  ```
TOP Counter({('contexte', 'cout', 'etiquettes', 'fraction_semantique', 'langue', 'refus', 'script', 'source', 'texte', 'trace', 'unites_semantiques'): 46})
LAB Counter({('candidats', 'confiance', 'debut', 'fin', 'langue', 'meta', 'niveau', 'script', 'source', 'type', 'valeur'): 4501})
TRACE Counter({('confiance', 'etape', 'indice', 'langue', 'script'): 46, ('etape', 'etiquettes', 'fraction', 'niveaux', 'unites_semantiques'): 46})
COUT Counter({('caracteres', 'etiquettes', 'octets'): 46})
META {'graphème': Counter({(): 1912}), 'mot': Counter({(): 1068}), 'pos': Counter({('ouvert',): 755, ('contexte', 'ouvert'): 11}), 'syntagme': Counter({('attachement', 'niveau', 'role'): 234, ('attachement', 'niveau', 'role', 'union'): 50, ('niveau', 'role'): 41, ('niveau', 'role', 'union'): 35}), 'discours': Counter({(): 67}), 'document': Counter({(): 49}), 'phrase': Counter({(): 89}), 'pragmatique': Counter({(): 86}), 'morphème': Counter({(): 104})}
TYPES {'graphème': ['chiffres', 'espace', 'lettres', 'ponctuation', 'symbole'], 'mot': ['mot', 'nombre', 'ponctuation'], 'pos': ['ADJ', 'ADV', 'AUX', 'CONJ', 'DET', 'NOUN', 'NUM', 'PREP', 'PRON', 'VERB'], 'syntagme': ['GN', 'GP', 'GV', 'REL', 'SUB'], 
… [844 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Mesures de temps : démarrage, échelle 1k→50k, coût par phrase

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 - <<'PY'\nimport subprocess,sys,time,statistics,json,pathlib\nCLI='tools/drave.py'\ndef wall(args,n=5):\n    ts=[]\n    for _ in range(n):\n        t=time.perf_counter(); p=subprocess.run([sys.executable,CLI,*args],capture_outp … [1215 caractères tronqués]`

  ```
version (134.3, 146.0, 192.0, 0)
aide (128.9, 139.6, 157.0, 0)
analyser f01 (146.5, 151.4, 164.9, 0)
evaluer (530.0, 542.7, 578.9, 0)
rejouer (145.6, 148.5, 162.8, 0)
scale 1000 chars 27.48 ms labels 1042 json_bytes 228118
scale 2000 chars 37.5 ms labels 2077 json_bytes 455423
scale 5000 chars 125.02 ms labels 5187 json_bytes 1129928
scale 10000 chars 331.56 ms labels 10362 json_bytes 2263467
scale 20000 chars 1025.66 ms labels 20719 json_bytes 4593108
scale 50000 chars 5438.9 ms labels 51792 json_bytes 11518138
no-space 1000 21.81 ms labels 7
no-space 10000 9.85 ms labels 7
no-space 50000 51.94 ms labels 7
  ```

### 🤖 Assistant

⏵ Sondage des rôles, cibles internes, URL et encodages NFD/BOM

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 - <<'PY'\nimport json,subprocess,sys,collections,importlib.util\nspec=importlib.util.spec_from_file_location('a','/tmp/audit_cli.py'); a=importlib.util.module_from_spec(spec); spec.loader.exec_module(a)\nroles=collections.Count … [1279 caractères tronqués]`

  ```
roles Counter({'predicat': 106, 'patient': 60, 'prédicat': 39, 'theme': 18, 'agent': 17, 'qualite': 17, 'destinataire': 15, 'groupe nominal': 13, 'lieu': 12, 'qualité': 11, 'temps': 11, 'possession': 10, 'but': 8, 'complément': 6, 'moyen': 5, 'hypothese': 4, 'contenu': 3, 'cause': 3, 'concession': 1, 'maniere': 1})
GV total 145 cible dans son span 3 hors span 72
top cibles [('haie', 6), ('nommer', 5), ('choses', 5), ('example', 4), ('jour', 4), ('ø', 4), ('voisine', 3), ('f', 3), ('simple', 3), ('URL', 2), ('user', 2), ('cour', 2)]
NUM f26 dix 42 45 texte 'dix'
NUM f50 deux 441 445 texte 'deux'
NUM f50 six 695 698 texte 'six'
NUM f50 trois 830 835 texte 'trois'
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 - <<'PY'\nimport subprocess,sys,json\ndef run(t, *args):\n    p=subprocess.run([sys.executable,'tools/drave.py','analyser',t,'--json',*args],capture_output=True,text=True)\n    return p\nfor name,t in [('NFD','e\\u0301lodie sou … [801 caractères tronqués]`

  ```
NFD rc 0 out 5063 err 
  langue und script Latn labels 18 mots [('e', 0, 1, 'mot'), ('́', 1, 2, 'ponctuation'), ('lodie', 2, 7, 'mot'), ('sourit', 8, 14, 'mot'), ('.', 14, 15, 'ponctuation')] synt 0 pos [('e', 'NOUN'), ('lodie', 'NOUN'), ('sourit', 'NOUN')]
BOM rc 0 out 5779 err 
  langue fr script Latn labels 20 mots [('\ufeff', 0, 1, 'ponctuation'), ('Le', 1, 3, 'mot'), ('chat', 4, 8, 'mot'), ('dort', 9, 13, 'mot'), ('.', 13, 14, 'ponctuation')] synt 2 pos [('Le', 'DET'), ('chat', 'NOUN'), ('dort', 'VERB')]
tab rc 0 out 5108 err 
  langue fr script Latn labels 17 mots [('Le', 0, 2, 'mot'), ('chat', 3, 7, 'mot'), ('dort', 8, 12, 'mot'), ('.', 12, 13, 'ponctuation')] synt 2 pos [('Le', 'DET'), ('chat', 'NOUN'), ('dort', 'VERB')]
CRLF rc 0 out 6318 err 
  langue fr script Latn labels 22 mots [('Le', 0, 2, 'mot'), ('chat', 3, 7, 'mot'), ('.', 7, 8, 'ponctuation'), ('Salut', 10, 15, 'mot'), ('.', 15, 16, 'ponctuation')] synt 2 pos [('Le', 'DET'), ('chat', 'NOUN'), ('Salut', 'NOUN')]
zero-width rc 0 out 5552 err 
  langue fr script Latn labels 19 mots [('Le', 0, 2, 'mot'), ('chat', 3, 7, 'mot'), ('\u200b', 7, 8, 'ponctuation'), ('dort', 8, 12, 'mot'), ('.', 12, 13, 'ponctuation')] synt
… [598 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Contrôle négatif : le détecteur attrape-t-il 8 mutations ?

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 - <<'PY'\nimport json,copy,subprocess,sys,importlib.util\nspec=importlib.util.spec_from_file_location('a','/tmp/audit_cli.py'); a=importlib.util.module_from_spec(spec); spec.loader.exec_module(a)\ntexte=\"Le chat dort.\"\np=sub … [2024 caractères tronqués]`

  ```
base overlaps {} sans_att 0 surface_ko 0
mutations {'span_hors': 1, 'chevauchement': 1, 'cible_absente': 1, 'confiance': 1, 'cle_manquante': 1, 'fraction': 1, 'valeur': 1, 'sans_attachement': 1, 'niveau_inconnu': 1}
detectees 9 / 9
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 - <<'PY'\nimport json,subprocess,sys\ndef run(t):\n    p=subprocess.run([sys.executable,'tools/drave.py','analyser',t,'--json'],capture_output=True,text=True)\n    return p, (json.loads(p.stdout) if p.returncode==0 else None)\n … [749 caractères tronqués]`

  ```
TEXTE 'Le prix est 12.5 euros.' rc 0
  phrase 0 15 'Le prix est 12.' type déclarative
  phrase 15 23 '5 euros.' type déclarative
  acte assertion
  acte assertion
TEXTE 'Le vol part à 12.03.2024.' rc 0
  phrase 0 17 'Le vol part à 12.' type déclarative
  phrase 17 20 '03.' type déclarative
  phrase 20 25 '2024.' type déclarative
  acte assertion
  acte assertion
  acte assertion
TEXTE 'Écrivez à alice@example.org.' rc 0
  phrase 0 24 'Écrivez à alice@example.' type déclarative
  phrase 24 28 'org.' type déclarative
  acte assertion
  acte assertion
TEXTE 'Visitez https://example.com/docs?page=2.' rc 0
  phrase 0 24 'Visitez https://example.' type déclarative
  phrase 24 33 'com/docs?' type interrogative
  phrase 33 40 'page=2.' type déclarative
  acte assertion
  acte question
  acte assertion
TEXTE 'M. Dupont est là. Il repart.' rc 0
  phrase 0 17 'M. Dupont est là.' type déclarative
  phrase 2 17 ' Dupont est là.' type déclarative
  phrase 17 28 ' Il repart.' type déclarative
  acte assertion
  acte assertion
  acte assertion
TEXTE 'Le Dr. Martin est arrivé hier. Il repart demain.' rc 0
  phrase 0 30 'Le Dr. Martin est arrivé hier.' type déclarative
  phrase 6 30 ' Martin est arr
… [236 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Consolidation des statistiques du banc et des vides du contrat

- **bash** `{"command": "cd /tmp && python3 - <<'PY'\nimport json,statistics\nr=json.load(open('audit_cli_results.json')); b=r['banc_50']; det={x['id']:x for x in json.load(open('audit_cli_detail.json'))}\nok=[x for x in b if x['rc']==0]; ref=[x for x in b if x['rc']==1]\nprint('ok',len(ok),'refus',len(ref))\nw … [1965 caractères tronqués]`

  ```
ok 46 refus 4
wall {'min': 136.8, 'med': 152.7, 'mean': 157.3, 'p95': 180.3, 'max': 226.6}
api {'min': 0.2, 'med': 1.0, 'mean': 2.2, 'p95': 2.0, 'max': 45.1}
json sizes {'min': 2126, 'med': 13510.5, 'mean': 26204.8, 'p95': 22841, 'max': 533611}
labels 4501 mots 1068 pos 766
synt 360 att 284 sans 76
overlap texts 28 syn pairs 107
phrase leading 19 doc tronq 17
unites vides ['f18'] fraction0 ['f18']
sans synt ['f13', 'f18', 'f27', 'f37'] sans pos ['f18']
langues {'it', 'fr', 'und', 'en'}
phrase labels 76 documents 49
slowest [('f50', 226.6, 45.088), ('f02', 193.8, 1.738), ('f05', 181.6, 1.03), ('f35', 180.3, 0.509), ('f44', 179.1, 1.804)]
api slowest [('f50', 45.088), ('f43', 7.877), ('f20', 2.414), ('f06', 2.012), ('f38', 1.893)]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 - <<'PY'\nimport json,subprocess,sys,collections,importlib.util\nspec=importlib.util.spec_from_file_location('a','/tmp/audit_cli.py'); a=importlib.util.module_from_spec(spec); spec.loader.exec_module(a)\ntotal=0; nonsurface=0;  … [902 caractères tronqués]`

  ```
total labels 4501 nonsurface 295 pct 6.55
bylevel Counter({'graphème': 1912, 'mot': 1068, 'pos': 766, 'syntagme': 360, 'morphème': 104, 'phrase': 89, 'pragmatique': 86, 'discours': 67, 'document': 49})
nonsurf Counter({'phrase': 89, 'pragmatique': 86, 'discours': 67, 'document': 49, 'morphème': 4})
surface levels 4210
  ```

### 🤖 Assistant

⏵ Analyse des cibles d'attachement (ambiguïté, hors span, classes fermées)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 - <<'PY'\nimport json,subprocess,sys,collections,importlib.util\nspec=importlib.util.spec_from_file_location('a','/tmp/audit_cli.py'); a=importlib.util.module_from_spec(spec); spec.loader.exec_module(a)\namb=[]; self_=[]; hors= … [1179 caractères tronqués]`

  ```
total attachments 284
cible apparaît >1 fois 56 [('f20', 'M', 3, 'GV'), ('f38', 'c', 3, 'GN'), ('f38', 'c', 3, 'GP'), ('f38', 'f', 2, 'GV'), ('f38', 'f', 2, 'GV'), ('f38', 'f', 2, 'GV'), ('f43', 'fin', 2, 'GN'), ('f43', 'ce', 2, 'REL'), ('f43', 'ce', 2, 'REL'), ('f43', 'fin', 2, 'REL'), ('f50', 'voisine', 2, 'REL'), ('f50', 'voisine', 2, 'GV')]
cible dans le span 10 [('f02', 'réveille', 'REL', 22, 54), ('f08', 'station', 'REL', 0, 34), ('f24', 'fille', 'GN', 9, 34), ('f33', 'viens', 'SUB', 0, 11), ('f38', 'f', 'GV', 46, 68), ('f39', 'user', 'GN', 0, 21), ('f43', 'phrase', 'GN', 9, 19), ('f50', 'réveille', 'REL', 41, 97)]
cible hors span 274
cible mot fermé 18 [('f05', 'pas', 'ADV', 'GP'), ('f05', 'pas', 'ADV', 'GN'), ('f06', 'pas', 'ADV', 'SUB'), ('f06', 'pas', 'ADV', 'GP'), ('f10', 'est', 'AUX', 'GN'), ('f10', 'est', 'AUX', 'GP'), ('f10', 'est', 'AUX', 'GP'), ('f30', 'hier', 'ADV', 'GV'), ('f32', 'pas', 'ADV', 'GN'), ('f32', 'pas', 'ADV', 'GN'), ('f43', 'ce', 'DET', 'REL'), ('f43', 'ce', 'DET', 'REL')]
cible longueur 1 9
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 - <<'PY'\nimport json,subprocess,sys,re,importlib.util\nspec=importlib.util.spec_from_file_location('a','/tmp/audit_cli.py'); a=importlib.util.module_from_spec(spec); spec.loader.exec_module(a)\nurlbad=[]; urlq=[]; ph_counts=[] … [1050 caractères tronqués]`

  ```
phrases par texte >1 [('f03', 2), ('f12', 3), ('f20', 2), ('f25', 2), ('f26', 2), ('f29', 2), ('f37', 2), ('f38', 4), ('f39', 2), ('f50', 19)]
phrases coupées dans URL/email [('f12', 'https://example.com/docs?page=2', (0, 24)), ('f12', 'https://example.com/docs?page=2', (24, 33)), ('f12', 'https://example.com/docs?page=2', (33, 62)), ('f37', 'alice@example.org', (0, 21)), ('f37', 'alice@example.org', (21, 51)), ('f38', 'https://a.b/c?d=e#f', (0, 24)), ('f38', 'https://a.b/c?d=e#f', (24, 28)), ('f38', 'https://a.b/c?d=e#f', (28, 46)), ('f38', 'http://x.y', (28, 46)), ('f38', 'http://x.y', (46, 69)), ('f50', 'https://example.org/corpus/2026?page=3', (1691, 1728)), ('f50', 'https://example.org/corpus/2026?page=3', (1728, 1744)), ('f50', 'https://example.org/corpus/2026?page=3', (1744, 1805)), ('f50', 'corpus@example.org', (1744, 1805)), ('f50', 'corpus@example.org', (1805, 1869))]
fausses interrogatives URL [('f12', 'com/docs?'), ('f38', 'b/c?'), ('f50', 'org/corpus/2026?')]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nfor t in \"1234567890\" \"Élodie sourit.\" \"J'ai trouvé ça génial 😍🔥\" \"Email: alice@example.org, phone: +33 6 12 34 56 78.\"; do\n  echo \"===== $t\"\n  python3 tools/drave.py analyser \"$t\" 2>&1 | head -25\ndone", "description": " … [33 caractères tronqués]`

  ```
===== 1234567890
drave 0.1.0 — analyse heuristique (CPU, hors ligne)
langue=und script=Zyyy source=heuristique · 6 étiquettes · unités sémantiques=0 (0.0% du texte)
POS  —
SYNTAGMES —
PRAGMATIQUE
  phrase [0:10] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
COUVERTURE  (confiance max par niveau)  graphème=0.99 · mot=0.98 · phrase=0.85 · discours=0.50 ·
            pragmatique=0.45 · document=0.70
===== Élodie sourit.
drave 0.1.0 — analyse heuristique (CPU, hors ligne)
langue=und script=Latn source=heuristique · 13 étiquettes · unités sémantiques=2 (85.7% du texte)
POS  Élodie/NOUN sourit/NOUN
SYNTAGMES —
PRAGMATIQUE
  phrase [0:14] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
COUVERTURE  (confiance max par niveau)  graphème=0.99 · mot=0.98 · pos=0.55 · phrase=0.85 ·
            discours=0.50 · pragmatique=0.45 · document=0.70
===== J'ai trouvé ça génial 😍🔥
drave 0.1.0 — analyse heuristique (CPU, hors ligne)
langue=und script=Latn source=heuristique · 26 étiquettes · unités sémantiques=2 (50.0% du texte)
POS  J'ai/PRON trouvé/NOUN ça/PRON génial/ADJ
SYNTAGMES —
PRAGMATIQUE
  phrase [0:24] déclarative · acte=assertion · n
… [845 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Rédaction et essai à blanc du test de non-régression du schéma

- **write** `{"content": "\"\"\"test_schema_produit.py — le contrat de sortie de `drave analyser --json`.\n\nDeux contrats cohabitent :\n\n- **actuel** (drave 0.1.0) : 11 champs racine, 11 champs par étiquette, spans valides,\n  déterminisme. Ce test passe sur le produit livré ; il gèle l'enveloppe et attrape un … [7888 caractères tronqués]`

  ```
<path>/tmp/test_schema_produit.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && DRAVE_RACINE=$PWD python3 /tmp/test_schema_produit.py 2>&1 | tail -20", "description": "Dry-run schema non-regression test"}`

  ```
test_codes_de_sortie (__main__.TestContratActuel.test_codes_de_sortie) ... ok
test_determinisme (__main__.TestContratActuel.test_determinisme) ... ok
test_enveloppe_et_etiquettes (__main__.TestContratActuel.test_enveloppe_et_etiquettes) ... ok
test_refus_actuel (__main__.TestContratActuel.test_refus_actuel)
0.1.0 : refus = code 1, stdout vide, message sur stderr (le manque P0-2). ... ok
setUpClass (__main__.TestSchemaV1) ... skipped "schéma v1 non livré : `schema` absent de l'annotation"

----------------------------------------------------------------------
Ran 4 tests in 2.950s

OK (skipped=1)
  ```

### 🤖 Assistant

⏵ Robustesse finale : cas limites, encodages, refus et déterminisme

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"Robustesse finale du CLI drave — écrit /tmp/audit_robustesse_final.json.\"\"\"\nfrom __future__ import annotations\n\nimport json\nimport os\nimport pathlib\nimport subprocess\nimport sys\nimport time\n\nRACINE = pathlib.Path(\"/home/stephane/Data13TB/steph … [8014 caractères tronqués]`

  ```
<path>/tmp/audit_robustesse_final.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 /tmp/audit_robustesse_final.py 2>&1 | tail -45", "description": "Run final robustness suite", "timeoutMs": 600000}`

  ```
version: rc=0 out=12 attendu=0 err=''
aide: rc=0 out=770 attendu=0 err=''
sans_commande: rc=2 out=0 attendu=2 err="usage: drave [-h] [-V] {analyser,evaluer,rejouer} ...\ndrave: erreur d'usage : th"
commande_inconnue: rc=2 out=0 attendu=2 err="usage: drave [-h] [-V] {analyser,evaluer,rejouer} ...\ndrave: erreur d'usage : ar"
analyser_sans_texte: rc=2 out=0 attendu=2 err='usage: drave analyser [-h] [--langue {fr,en}] [--json] TEXTE\ndrave analyser: err'
langue_hors_choix: rc=2 out=0 attendu=2 err='usage: drave analyser [-h] [--langue {fr,en}] [--json] TEXTE\ndrave analyser: err'
langue_majuscule: rc=2 out=0 attendu=2 err='usage: drave analyser [-h] [--langue {fr,en}] [--json] TEXTE\ndrave analyser: err'
option_inconnue: rc=2 out=0 attendu=2 err="usage: drave [-h] [-V] {analyser,evaluer,rejouer} ...\ndrave: erreur d'usage : un"
texte_double_tiret: rc=2 out=0 attendu=0 err='usage: drave analyser [-h] [--langue {fr,en}] [--json] TEXTE\ndrave analyser: err'
texte_double_tiret_sep: rc=0 out=460 attendu=0 err=''
texte_tiret_simple: rc=0 out=460 attendu=0 err=''
json_avant_texte: rc=0 out=5561 attendu=0 err=''
nouvelle_ligne: rc=0 out=754 attendu=0 err=''
tab_et_crlf: rc=0 out=688 attendu=0
… [1598 caractères tronqués]
  ```

- **bash** `{"command": "nl -ba /tmp/audit_robustesse_final.py | sed -n '74,92p'; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; python3 tools/drave.py analyser $'\\ufeffLe chat dort.' --json >/tmp/bom.out 2>/tmp/bom.err; echo \"bom rc=$? out=$(wc -c </tmp/bom.out) err=$(cat /tmp/bom.err)\"", "description" … [37 caractères tronqués]`

  ```
74	    a = bl.Heuristique().analyser(valeur)
    75	    cas.append({"nom": f"api_non_str_{type(valeur).__name__}", "api": True, "attendu": "non_texte",
    76	                "refus": a.refus, "texte": a.texte, "etiquettes": len(a.etiquettes),
    77	                "cles_cout": sorted(a.cout)})
    78	
    79	# --- encodages
    80	p = lancer("utf8_valide", ["analyser", "Élodie sourit."], attendu=0)
    81	p = lancer("nfd", ["analyser", "e\u0301lodie sourit."], attendu=0)
    82	if p.returncode == 0:
    83	    d = json.loads(p.stdout)
    84	    cas[-1]["mots"] = [(e["valeur"], e["debut"], e["fin"]) for e in d["etiquettes"]
    85	                       if e["niveau"] == "mot"]
    86	    cas[-1]["syntagmes"] = sum(1 for e in d["etiquettes"] if e["niveau"] == "syntagme")
    87	    cas[-1]["pos"] = [(e["valeur"], e["type"]) for e in d["etiquettes"] if e["niveau"] == "pos"]
    88	p = lancer("bom", ["analyser", "\ufeffLe chat dort."], attendu=0)
    89	p = lancer("surrogate_seul", [b"\xff"], attendu="refus_encodage")
    90	p = lancer("surrogate_dans_mot", [b"a\xffb"], attendu="refus_encodage")
    91	env_ascii = os.environ.copy(); env_ascii["PYTHONIOENCODING"] = "ascii"
    92	la
… [101 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'PY'\np='/tmp/audit_robustesse_final.py'\ns=open(p).read()\ns=s.replace('[\"analyser\", \"Élodie sourit.\"], attendu=0)\\np = lancer(\"nfd\"', '[\"analyser\", \"Élodie sourit.\", \"--json\"], attendu=0)\\np = lancer(\"nfd\"')\ns=s.replace('[\"analyser\", \"e\\\\u0 … [535 caractères tronqués]`

  ```
80:p = lancer("utf8_valide", ["analyser", "Élodie sourit.", "--json"], attendu=0)
81:p = lancer("nfd", ["analyser", "e\u0301lodie sourit.", "--json"], attendu=0)
88:p = lancer("bom", ["analyser", "\ufeffLe chat dort.", "--json"], attendu=0)
texte_tiret_simple: rc=0 out=460 attendu=0 err=''
json_avant_texte: rc=0 out=5561 attendu=0 err=''
nouvelle_ligne: rc=0 out=754 attendu=0 err=''
tab_et_crlf: rc=0 out=688 attendu=0 err=''
evaluation: rc=0 out=659 attendu=0 err=''
evaluation_gold: rc=0 out=2740 attendu=0 err=''
rejeu_ok: rc=0 out=147 attendu=0 err=''
vide: rc=1 out=0 attendu=1 err="drave: refus d'analyse : vide (le texte doit contenir au moins une lettre ou un "
un_espace: rc=1 out=0 attendu=1 err="drave: refus d'analyse : vide (le texte doit contenir au moins une lettre ou un "
espaces_et_tabs: rc=1 out=0 attendu=1 err="drave: refus d'analyse : vide (le texte doit contenir au moins une lettre ou un "
ponctuation_seule: rc=1 out=0 attendu=1 err="drave: refus d'analyse : vide (le texte doit contenir au moins une lettre ou un "
emoji_seul: rc=1 out=0 attendu=1 err="drave: refus d'analyse : vide (le texte doit contenir au moins une lettre ou un "
invisible: rc=1 out=0 attendu=1 err=
… [1142 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'PY'\np='/tmp/audit_robustesse_final.py'\ns=open(p).read()\ns=s.replace('lancer(\"surrogate_seul\", [b\"\\\\xff\"], attendu=\"refus_encodage\")','lancer(\"surrogate_seul\", [\"analyser\", b\"\\\\xff\"], attendu=\"refus_encodage\")')\ns=s.replace('lancer(\"surrogat … [383 caractères tronqués]`

  ```
surrogate_seul: rc=1 out=0 attendu=refus_encodage err="drave: refus d'analyse : vide (le texte doit contenir au moins une lettre ou un "
surrogate_dans_mot: rc=1 out=0 attendu=refus_encodage err="drave: erreur : UnicodeEncodeError : 'utf-8' codec can't encode character '\\udcf"
écrit /tmp/audit_robustesse_final.json 49 cas
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'PY'\nimport json\nc=json.load(open('audit_robustesse_final.json'))\nfor x in c:\n    if x.get('api'):\n        print(x['nom'], 'refus=',repr(x.get('refus')), 'etiquettes=',x.get('etiquettes'), 'cles_cout=',x.get('cles_cout'), 'json_cles=',x.get('json_cles'))\n    … [369 caractères tronqués]`

  ```
api_'' refus= 'vide' etiquettes= 0 cles_cout= ['duree_s', 'octets'] json_cles= ['contexte', 'cout', 'etiquettes', 'fraction_semantique', 'langue', 'refus', 'script', 'source', 'texte', 'trace', 'unites_semantiques']
api_'   ' refus= 'vide' etiquettes= 0 cles_cout= ['duree_s', 'octets'] json_cles= ['contexte', 'cout', 'etiquettes', 'fraction_semantique', 'langue', 'refus', 'script', 'source', 'texte', 'trace', 'unites_semantiques']
api_'...' refus= 'vide' etiquettes= 0 cles_cout= ['duree_s', 'octets'] json_cles= ['contexte', 'cout', 'etiquettes', 'fraction_semantique', 'langue', 'refus', 'script', 'source', 'texte', 'trace', 'unites_semantiques']
api_'🚀' refus= 'vide' etiquettes= 0 cles_cout= ['duree_s', 'octets'] json_cles= ['contexte', 'cout', 'etiquettes', 'fraction_semantique', 'langue', 'refus', 'script', 'source', 'texte', 'trace', 'unites_semantiques']
api_'1234567890' refus= '' etiquettes= 6 cles_cout= ['caracteres', 'duree_s', 'etiquettes', 'octets'] json_cles= ['contexte', 'cout', 'etiquettes', 'fraction_semantique', 'langue', 'refus', 'script', 'source', 'texte', 'trace', 'unites_semantiques']
api_non_str_NoneType refus= 'non_texte' etiquettes= 0 cles_cout= ['duree_s', 'o
… [48729 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification du commit courant et des fichiers voisins avant rédaction

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngit log --oneline -3; git rev-parse HEAD; git status --short --untracked-files=all -- reports/ | head -10; echo ---; git ls-files reports/rapport-produit-bloc-l.md reports/pensee-produit-bloc-l.json; echo ---; ls -l reports/rapport-fia … [174 caractères tronqués]`

  ```
56eb43af INDEX — RÉGÉNÉRÉ (679 FICHES) APRÈS LES DEUX FICHES DE ROBUSTESSE ; --verifier SORT 0
108faf92 DOCS — LE README DES FICHES DANS LE BUDGET T1 (LIGNES ANCIENNES RACCOURCIES)
3601764a ÉTAT — T0 DANS LE BUDGET (AUDIT A24)
56eb43af207de7e231463100778934db8bebe970
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-spans-chunker.md
?? reports/rapport-s-paragraphes.md
---
reports/pensee-produit-bloc-l.json
reports/rapport-produit-bloc-l.md
---
ls: cannot access 'reports/rapport-fiabilite-produit.md': No such file or directory
ls: cannot access 'reports/pensee-fiabilite-produit.json': No such file or directory
59a06f3e4f7d633ae8caa30412fd4c01e14374914226f5e54629f544e47aea8c  tools/drave.py
084517d9c10088b3adedc01658adbb33e3de69e7f5ca8c2f563f427abdd79f4f  tools/bloc_linguistique.py
  ```

### 🤖 Assistant

⏵ Récapitulatif chiffré final pour la rédaction

- **bash** `{"command": "cd /tmp && python3 - <<'PY'\nimport json,statistics\nr=json.load(open('audit_cli_results.json')); b=r['banc_50']; det={x['id']:x for x in json.load(open('audit_cli_detail.json'))}\nok=[x for x in b if x['rc']==0]; ref=[x for x in b if x['rc']==1]\nwall=[x['wall_ms'] for x in b]; api=[r[ … [2102 caractères tronqués]`

  ```
WALL (136.8, 152.7, 157.3, 180.3, 226.6)
API (0.2, 1.0, 2.2, 2.0, 45.1)
JSON sizes (2126, 13510.5, 26204.8, 22841, 533611)
labels 4501 mots 1068 pos 766 synt 360 att 284 sans 76
overlap texts 28 pairs 107
phrase leading 19 doc tronq 17 documents 49
sans synt ['f13', 'f18', 'f27', 'f37'] sans pos ['f18'] unites vides ['f18']
slowest [('f50', 226.6, 45.088), ('f02', 193.8, 1.738), ('f05', 181.6, 1.03), ('f35', 180.3, 0.509), ('f44', 179.1, 1.804)]
api slowest [('f50', 45.088), ('f43', 7.877), ('f20', 2.414), ('f06', 2.012), ('f38', 1.893)]
refus [('f14', 1, "drave: refus d'analyse : vide (le texte doit contenir au moins une lettre ou un chiffre)"), ('f15', 0, "drave: refus d'analyse : vide (le texte doit contenir au moins une lettre ou un chiffre)"), ('f16', 3, "drave: refus d'analyse : vide (le texte doit contenir au moins une lettre ou un chiffre)"), ('f17', 3, "drave: refus d'analyse : vide (le texte doit contenir au moins une lettre ou un chiffre)")]
langues {'f01': 'fr', 'f02': 'fr', 'f03': 'fr', 'f04': 'fr', 'f05': 'fr', 'f06': 'fr', 'f07': 'en', 'f08': 'en', 'f09': 'en', 'f10': 'fr', 'f11': 'fr', 'f12': 'fr', 'f13': 'und', 'f18': 'und', 'f19': 'fr', 'f20': 'fr', 'f21': 'fr', '
… [1209 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nnl -ba tools/bloc_linguistique.py | sed -n '1003,1050p'; echo ===; nl -ba tools/bloc_linguistique.py | sed -n '1216,1258p'; echo ===; nl -ba tools/bloc_linguistique.py | sed -n '1818,1852p'", "description": "Get exact line numbers for  … [15 caractères tronqués]`

  ```
1003	    def analyser(self, texte: str, langue: str | None = None,
  1004	                 contexte: str | None = None) -> Annotation:
  1005	        t0 = time.perf_counter()
  1006	        if not isinstance(texte, str):
  1007	            # une entrée non textuelle est **refusée** proprement (le produit ne plante pas)
  1008	            return Annotation(texte=str(texte)[:200], refus="non_texte", source=self.nom,
  1009	                              trace=[{"etape": "refus", "raison": "non_texte",
  1010	                                      "type": type(texte).__name__}],
  1011	                              cout={"octets": 0, "duree_s": round(time.perf_counter() - t0, 6)})
  1012	        texte = texte or ""
  1013	        trace: list[dict] = []
  1014	        if not texte.strip() or not any(ch.isalpha() or ch.isdigit() for ch in texte):
  1015	            return Annotation(texte=texte, refus="vide", source=self.nom,
  1016	                              trace=[{"etape": "refus", "raison": "vide"}],
  1017	                              cout={"octets": len(texte.encode("utf-8", "replace")), "duree_s": round(time.perf_counter() - t0, 6)})
  1018	
  1019	        lg, conf_lg, script =
… [7152 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Construction du rapport JSON structuré (banc, contrat, schéma, correctifs)

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"Construit reports/pensee-fiabilite-produit.json à partir des mesures /tmp.\"\"\"\nfrom __future__ import annotations\n\nimport hashlib\nimport json\nimport pathlib\nimport statistics\nimport subprocess\nimport sys\n\nRACINE = pathlib.Path(\"/home/stephane/D … [29742 caractères tronqués]`

  ```
<path>/tmp/build_json_report.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'PY'\np='/tmp/build_json_report.py'\ns=open(p).read()\ns=s.replace('''                \"phrases\": d.get(\"documents\") and r.get(\"phrases\"),''','''                \"phrases\": r.get(\"phrases\"),''')\ns=s.replace('''                \"sans_pos\": r.get(\"pos\",  … [828 caractères tronqués]`

  ```
écrit /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-fiabilite-produit.json 102879 octets
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 - <<'PY'\nimport json\np='reports/pensee-fiabilite-produit.json'\nd=json.load(open(p))\nprint('top keys',list(d))\nprint('banc',len(d['banc_50']['resultats']),'synthese keys',list(d['banc_50']['synthese'])[:10])\ns=d['banc_50'] … [850 caractères tronqués]`

  ```
top keys ['rapport', 'ligne', 'branche', 'commit_mesure', 'commit_module', 'date', 'objet', 'verdict', 'snapshot', 'dispositif', 'banc_50', 'robustesse', 'contrat', 'schema_propose', 'test_non_regression', 'correctifs', 'controle_negatif', 'limites', 'fichiers']
banc 50 synthese keys ['n', 'succes', 'refus', 'plantages', 'json_invalide', 'sorties_vides_sur_succes', 'spans_hors_texte', 'spans_vides', 'valeurs_vides', 'cles_racine_ko']
n = 50
succes = 46
refus = 4
labels = 4501
mots = 1068
pos = 766
syntagmes = 360
attachements = 284
sans_attachement = 76
chevauchements = {'textes': 28, 'paires': 107, 'union_labels': 85, 'apres_filtre_union': 0, 'tous_impliquent_union': True}
temps_cli_ms = {'min': 136.77, 'mediane': 152.72, 'moyenne': 157.34, 'p95': 180.3, 'max': 226.64}
temps_api_ms = {'min': 0.18, 'mediane': 1.01, 'moyenne': 2.16, 'p95': 2.01, 'max': 45.09}
json_octets = {'min': 2126, 'mediane': 13510.5, 'moyenne': 26204.83, 'p95': 22841, 'max': 533611}
langues = {'fr': 35, 'en': 5, 'und': 5, 'it': 1}
sans_syntagme = ['f13', 'f18', 'f27', 'f37']
sans_pos = ['f18']
tokens_sans_pos = {'mot': [0, 766], 'ponctuation': [257, 257], 'nombre': [45, 45]}
cibles_fermees = 18
cibles_ambigues
… [469 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-fiabilite-produit.json'))\nfor x in d['banc_50']['resultats']:\n    if x['id'] in ('f01','f18','f27','f50','f12','f20'):\n        print(x['id'], {k:v for k,v in x.items()  … [77 caractères tronqués]`

  ```
f01 {'id': 'f01', 'categorie': 'fr', 'attendu': 'fr', 'caracteres': 13, 'octets_utf8': 13, 'rc': 0, 'temps_cli_ms': 150.79, 'temps_api_ms': 0.796, 'deterministe': True, 'json_octets': 5561, 'json_valide': True, 'langue': 'fr', 'script': 'Latn', 'labels': 19, 'mots': 4, 'pos': 3, 'syntagmes': 2, 'attaches': 2, 'sans_attachement': 0, 'chevauchements_syntagme': 0, 'chevauchements_phrase_type': 0, 'syntagmes_union': 0, 'conflits_apres_filtre_union': 0, 'cibles_fermees': 0, 'cibles_absentes': 0, 'phrases': 1, 'phrases_espaces_initiaux': 0, 'documents': 1, 'doc_tronquees': 0, 'doc_titres': [], 'unites_semantiques': 2, 'fraction_semantique': 0.6154, 'trous_pos': {'mot': {'total': 3, 'sans_pos': 0}, 'ponctuation': {'total': 1, 'sans_pos': 1}}, 'sans_syntagme': False, 'sans_pos': False}
f12 {'id': 'f12', 'categorie': 'fr', 'attendu': 'fr', 'caracteres': 62, 'octets_utf8': 62, 'rc': 0, 'temps_cli_ms': 153.01, 'temps_api_ms': 1.768, 'deterministe': True, 'json_octets': 17092, 'json_valide': True, 'langue': 'fr', 'script': 'Latn', 'labels': 63, 'mots': 18, 'pos': 9, 'syntagmes': 5, 'attaches': 4, 'sans_attachement': 1, 'chevauchements_syntagme': 0, 'chevauchements_phrase_type': 0, 'syntagmes_u
… [4029 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Rédaction du rapport principal (mesures, contrat, schéma, correctifs)

- **write** `{"content": "# Fiabilité du produit hors gold — 0 plantage sur 50 phrases, 4 refus sans JSON, 28/46 textes à chevauchement\n\n> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Branche** : `s/v7` ·\n> **Commit mesuré** : `56eb43af` (module `c1a08588`, `tools/drave.py` `59a06f3e`) ·\n>  … [29659 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

### 🤖 Assistant

⏵ Insertion du test complet dans le rapport et vérifications de cohérence

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 - <<'PY'\nimport pathlib\nmd = pathlib.Path('reports/rapport-fiabilite-produit.md')\ncode = pathlib.Path('/tmp/test_schema_produit.py').read_text(encoding='utf-8')\ns = md.read_text(encoding='utf-8')\nassert '@@TEST_CODE@@' in  … [333 caractères tronqués]`

  ```
md bytes 37350 lines 626
78:| syntagmes qui se chevauchent | **107 paires** dans **28/46** textes ; **85/360** étiquettes `meta.union` | f02 : `REL 22-42` et `REL 22-54` ; f50 : 50 paires |
253:3. **Chevauchements** : 107 paires / 28 textes ; un arbre ou un index par offset casse. Filtrer
351:`/tmp` : `Ran 4 tests ... OK (skipped=1)` — les 4 tests du contrat actuel passent, la classe
535:| **P0-3** | **Partition explicite des syntagmes** : `meta.alternative` + filtre `union` documenté (ou suppression mesurée) | **107 paires / 28 textes** ; 85 `union` ; 0 conflit après filtre | `bloc_linguistique.py` 1099-1156, 1179-1204, 1820-1849 | **0,5–1 j** | moyen : change F1/attachement ; préférer l'alternative étiquetée à la suppression |
598:- **Chevauchements** : les **107 paires** dépendent du banc ; l'audit A24 en compte **132** sur
608:3. **P0-3 — Partition explicite des syntagmes** : 107 paires sur 28/46 textes ; le filtre
  ```

### 🤖 Assistant

⏵ Validation du rapport : fences, schéma JSON, liens et cohérence des chiffres

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 - <<'PY'\nimport pathlib,re,json\np=pathlib.Path('reports/rapport-fiabilite-produit.md'); s=p.read_text(encoding='utf-8')\nprint('placeholders', s.count('@@'), s.count('{{'))\nprint('fences', s.count('```'))\n# extraire les blo … [1184 caractères tronqués]`

  ```
placeholders 0 0
fences 6
blocs [('', 244), ('json', 2012), ('python', 7683)]
json blocks 1
schema JSON valide, required= ['schema', 'version', 'texte', 'langue', 'script', 'refus', 'etiquettes', 'unites_semantiques']
python blocks 1 [7683]
test compile OK
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngrep -n \"242\\|fr|en\\|fr\\\\\\\\|en\\|6/2\" reports/rapport-fiabilite-produit.md | head -20; echo ---; grep -n \"non-GV\" reports/rapport-fiabilite-produit.md; echo ---; grep -n \"choix\" reports/rapport-fiabilite-produit.md | head", … [51 caractères tronqués]`

  ```
92:| cibles ambiguës par chaîne | **56/284** | cible présente >1 fois ; 9 cibles d'un caractère (`M`, `c`, `f`) |
93:| syntagmes sans cible | **76/360** | 70 GV, 4 GN, 2 GP ; **6/242** non-GV |
167:| `--langue de`, `--langue FR`, option inconnue | 2 | **2** | 0 | conforme (choix `fr\|en`) |
255:4. **Cible sans offset** : 56/284 cibles apparaissent plusieurs fois ; 18 mots fermés ; 9 cibles
542:| **P1-1** | **Cible d'attachement offsettée** (`cible_debut`/`cible_fin`) et désambiguïsée | **56/284** cibles apparaissent >1 fois ; **18** mots fermés ; **9** cibles de 1 caractère | `bloc_linguistique.py` 1145-1156, 1168-1176, 1195-1203 | **4 h** | faible : ajout dans `meta.attachement` |
612:5. **P1-1 — Cibles d'attachement offsettées** : 56/284 cibles ambiguës, 18 mots fermés, 0 offset ;
---
93:| syntagmes sans cible | **76/360** | 70 GV, 4 GN, 2 GP ; **6/242** non-GV |
---
167:| `--langue de`, `--langue FR`, option inconnue | 2 | **2** | 0 | conforme (choix `fr\|en`) |
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md", "old_string": "| syntagmes sans cible | **76/360** | 70 GV, 4 GN, 2 GP ; **6/242** non-GV |", "new_string": "| syntagmes sans cible | **76/360** | 70 GV, 4 GN, 2 GP ; **6/215** non-GV |"}`

  ```
Error: cannot edit "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md": file changed since it was read — re-read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md", "offset": 86, "limit": 12}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md</path>
<type>file</type>
<content>
86: | phrases commençant par un espace | **19/76** | f03, f20, f25, f26, f29, f50 (14) |
87: | documents tronqués à 60 caractères | **17/49** | f50 : 4 titres tronqués |
88: | faux titres de document | **2/49** | f18 (`1234567890`), f31 (`ÇA NE MARCHE PAS !!!`) |
89: | langue fausse | **1/41 fr** | f33 « Si tu viens… » → `it` |
90: | langue `und` | **5** | f13, f18 (chiffres), f27, f37, f48 (latin) |
91: | cibles en mot fermé | **18/284** | `pas` (5), `est` (3), `ce` (2), `hier`, `M`… |
92: | cibles ambiguës par chaîne | **56/284** | cible présente >1 fois ; 9 cibles d'un caractère (`M`, `c`, `f`) |
93: | syntagmes sans cible | **76/360** | 70 GV, 4 GN, 2 GP ; **6/242** non-GV |
94: | rôles non normalisés | **106** `predicat` vs **39** `prédicat` ; **17** `qualite` vs **11** `qualité` | filtre client fragile |
95: | `valeur` non uniforme | **295/4501** | phrase = type, pragmatique = acte, document tronqué, 4 morphèmes normalisés |
96: 
97: **Le cas « Élodie sourit. »** — une phrase canonique, 13 étiquettes, 2 unités sémantiques, mais

(Showing lines 86-97 of
… [44 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md", "new_string": "| syntagmes sans cible | **76/360** | 70 GV, 4 GN, 2 GP ; **6/215** non-GV |", "old_string": "| syntagmes sans cible | **76/360** | 70 GV, 4 GN, 2 GP ; **6/242** non-GV |"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 - <<'PY'\nimport pathlib,re\nlines=pathlib.Path('reports/rapport-fiabilite-produit.md').read_text(encoding='utf-8').splitlines()\nin_code=False; groups=[]; cur=[]\nfor i,l in enumerate(lines,1):\n    if l.strip().startswith('`` … [823 caractères tronqués]`

  ```
tables 14
tables incohérentes 0
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md", "limit": 40, "offset": 1}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md</path>
<type>file</type>
<content>
1: # Fiabilité du produit hors gold — 0 plantage sur 50 phrases, 4 refus sans JSON, 28/46 textes à chevauchement
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Branche** : `s/v7` ·
4: > **Commit mesuré** : `56eb43af` (module `c1a08588`, `tools/drave.py` `59a06f3e`) ·
5: > **Date** : 2026-11-06 · **Verdict** : ⚠️ **la surface est fiable ; le contrat ne l'est pas encore.**
6: > **Aucun fichier existant modifié ; aucun commit.** Sorties : ce rapport et
7: > [`pensee-fiabilite-produit.json`](pensee-fiabilite-produit.json).
8: >
9: > **Dispositif** : [`tools/drave.py`](../tools/drave.py) (CLI : `analyser`, `evaluer`, `rejouer`,
10: > `--version`) et [`tools/bloc_linguistique.py`](../tools/bloc_linguistique.py) ;
11: > **50 phrases libres** écrites pour l'audit (textes dans le JSON) ; harnais local non committé
12: > dans `/tmp` ; machine **Xeon E5-2687W v3**, Python **3.13.16**.
13: >
14: > **Snapshot.** HEAD a bougé pendant l'audit (`6ef2a3f5` → `56eb43af`). Le module a reçu à
15: > **11 h 34** le correctif « non-str / surrogate » (`c1a0
… [1638 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nsed -n '330,370p' reports/rapport-fiabilite-produit.md; echo '...'; sed -n '490,520p' reports/rapport-fiabilite-produit.md; echo '...'; tail -25 reports/rapport-fiabilite-produit.md", "description": "Inspect test insertion and closing  … [10 caractères tronqués]`

  ```
"confiance": {"type": "number", "minimum": 0, "maximum": 1},
        "candidats": {"type": "array", "items": {"type": "string"}},
        "langue": {"type": "string"},
        "script": {"type": "string"},
        "meta": {"type": "object"}
      },
      "additionalProperties": true
    }
  }
}
```

**Politique de version.** MAJOR pour toute suppression, renommage ou changement de type/sémantique
d'un des 8 champs ; MINOR pour un champ optionnel, une valeur de `type` ou un code de `refus`.
`schema` et `version` sont présents **sur succès et sur refus** ; le refus est un code **3** avec
un JSON d'annotation vide (`etiquettes: []`), pas un stdout vide.

### 4.5 Le test de non-régression du schéma

Le test ci-dessous est **proposé** pour `tools/tests/test_schema_produit.py` (il n'est pas écrit
dans le dépôt : la mission n'autorise que deux fichiers neufs). Il a été **essayé à blanc** depuis
`/tmp` : `Ran 4 tests ... OK (skipped=1)` — les 4 tests du contrat actuel passent, la classe
`TestSchemaV1` est sautée tant que `schema` n'existe pas. Elle deviendra stricte dès P0-1 livré.

```python
"""test_schema_produit.py — le contrat de sortie de `drave analyser --json`.

Deux contrats cohab
… [3760 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-fiabilite-produit.json'))\n# longest strings\ndef walk(o,path=''):\n    if isinstance(o,str):\n        yield len(o),path,o[:80]\n    elif isinstance(o,dict):\n        for  … [629 caractères tronqués]`

  ```
7682 /test_non_regression/code '"""test_schema_produit.py — le contrat de sortie de `drave analyser --json`.\n\nDe'
2144 /banc_50/resultats[49]/texte '# Notes de terrain\nLe chat de la voisine qui dort sur le toit se réveille dès qu'
390 /banc_50/resultats[42]/texte 'Ceci est une phrase qui contient beaucoup de mots afin de tester la longueur et '
226 /verdict '⚠️ surface fiable (0 plantage, 0 JSON invalide, 0 span hors texte, 50/50 détermi'
211 /snapshot/note "HEAD est passé de 6ef2a3f5 à 56eb43af pendant l'audit ; le module a reçu le corr"
187 /robustesse/cas[3]/stderr "usage: drave [-h] [-V] {analyser,evaluer,rejouer} ...\ndrave: erreur d'usage : ar"
173 /dispositif/harnais 'scripts locaux non committés dans /tmp (audit_cli.py, audit_cli_detail.py, audit'
170 /dispositif/mesure 'CLI en subprocess (python3 tools/drave.py analyser TEXTE --json), deux passages '
--- rob 10k
10k_phrases ['drave', 'analyser', '<10000 caractères>', '--json'] 0 2763666 None
10k_sans_espace ['drave', 'analyser', '<10000 caractères>', '--json'] 0 42482 None
10k_ponctuation ['drave', 'analyser', '<10000 caractères>', '--json'] 1 None None
10k_lisible_sans_espace ['drave', 'analyser', '<10000 caractères>']
… [424 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-fiabilite-produit.json'))\nr=d['banc_50']['resultats']; ok=[x for x in r if x['rc']==0]\nfor k in ['labels','mots','pos','syntagmes','attaches','sans_attachement','chevauc … [414 caractères tronqués]`

  ```
labels 4501
mots 1068
pos 766
syntagmes 360
attaches 284
sans_attachement 76
chevauchements_syntagme 107
cibles_fermees 18
phrases 76
documents 49
doc_tronquees 17
unites_semantiques 413
refus 4 succes 46
langues {'it': 1, 'en': 5, 'und': 5, 'fr': 35}
temps max 226.64
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-fiabilite-produit.json'))\nok=[x for x in d['banc_50']['resultats'] if x['rc']==0]\nprint('union sum',sum(x.get('syntagmes_union',0) for x in ok))\nprint('conflits apres f … [277 caractères tronqués]`

  ```
union sum 85
conflits apres filtre sum 0
phrase chev sum 1
leading sum 19
  ```

### 🤖 Assistant

⏵ Contrôle final : seuls les deux fichiers neufs sont de moi, rien n'est committé

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngit status --short --untracked-files=all -- reports/rapport-fiabilite-produit.md reports/pensee-fiabilite-produit.json tools/ docs/produit/README.md\necho ---\ngit status --short --untracked-files=all | grep -E 'fiabilite' \necho ---\n … [172 caractères tronqués]`

  ```
m tools/structures
?? reports/pensee-fiabilite-produit.json
?? reports/rapport-fiabilite-produit.md
---
?? reports/pensee-fiabilite-produit.json
?? reports/rapport-fiabilite-produit.md
---
-rw-r--r--. 1 stephane stephane 102879  6 nov 12:29 reports/pensee-fiabilite-produit.json
-rw-------. 1 stephane stephane  37350  6 nov 12:37 reports/rapport-fiabilite-produit.md
---
56eb43af INDEX — RÉGÉNÉRÉ (679 FICHES) APRÈS LES DEUX FICHES DE ROBUSTESSE ; --verifier SORT 0
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md", "limit": 25, "offset": 158}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md</path>
<type>file</type>
<content>
158: 
159: ## 3. Robustesse des entrées
160: 
161: ### 3.1 Codes et arguments
162: 
163: | cas | code attendu | code observé | stdout | constat |
164: |---|---:|---:|---:|---|
165: | `--version`, `--aide` | 0 | **0** | oui | conforme |
166: | aucune commande, commande inconnue, texte manquant | 2 | **2** | 0 | conforme |
167: | `--langue de`, `--langue FR`, option inconnue | 2 | **2** | 0 | conforme (choix `fr\|en`) |
168: | texte commençant par `--` (`--bonjour`) | 0 | **2** | 0 | **anomalie** : pris pour une option |
169: | même texte avec `--` séparateur | 0 | **0** | oui | conforme |
170: | texte `-3 degrés` | 0 | **0** | oui | conforme (argparse accepte) |
171: | texte vide / espace / tabs | 1 | **1** | **0** | conforme, refus |
172: | ponctuation seule / emoji / espace invisible | 1 | **1** | **0** | refus correct, **raison `vide` fausse** |
173: | `--json` avant le texte | 0 | **0** | oui | conforme |
174: | nouvelle ligne, tabulation, CRLF | 0 | **0** | oui | conforme |
175: 
176: Les codes **0 / 1 / 2** existent ; les codes **3 (refus distinct)** et
… [251 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md", "new_string": "| texte `-3 degrés` | 0 | **0** | oui | conforme (argparse accepte) |\n| un mot (`Bonjour`), un caractère (`a`) | 0 | **0** | oui | conforme ; 7 et 5 étiquettes |\n| caractères spécia … [390 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md", "new_string": "| caractères spéciaux (f40 : `@ # $ % & * ( ) [ ] { } < > ~ ^`, barre verticale et antislash) | 0 | **0** | oui | 76 étiquettes, 0 plantage ; la barre et l'antislash sont des tokens d … [215 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 - <<'PY'\nimport pathlib\nlines=pathlib.Path('reports/rapport-fiabilite-produit.md').read_text(encoding='utf-8').splitlines()\nin_code=False; groups=[]; cur=[]\nfor i,l in enumerate(lines,1):\n    if l.strip().startswith('```') … [654 caractères tronqués]`

  ```
tables 14 incoherentes 0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 - <<'PY'\nimport pathlib,re,json\ns=pathlib.Path('reports/rapport-fiabilite-produit.md').read_text(encoding='utf-8')\nbloc=re.search(r'```json\\n(.*?)```',s,re.S).group(1)\nmd=json.loads(bloc)\nd=json.load(open('reports/pensee- … [444 caractères tronqués]`

  ```
egal True
-rw-r--r--. 1 stephane stephane 102879  6 nov 12:29 reports/pensee-fiabilite-produit.json
-rw-r--r--. 1 stephane stephane  37646  6 nov 12:40 reports/rapport-fiabilite-produit.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 - <<'PY'\nimport pathlib,re\ns=pathlib.Path('reports/rapport-fiabilite-produit.md').read_text(encoding='utf-8')\nblocs=re.findall(r'```python\\n(.*?)```',s,re.S)\ncode=blocs[0]\norig=pathlib.Path('/tmp/test_schema_produit.py'). … [206 caractères tronqués]`

  ```
identique False 7683 7682
compile OK
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 - <<'PY'\nimport json,collections\nd=json.load(open('reports/pensee-fiabilite-produit.json'))\n# recompute from detail file? detail has lists\ndet=json.load(open('/tmp/audit_cli_detail.json'))\nc=collections.Counter()\nfor x in … [193 caractères tronqués]`

  ```
Counter({('pas', 'ADV'): 7, ('est', 'AUX'): 4, ('ce', 'DET'): 2, ('Ce', 'DET'): 2, ('hier', 'ADV'): 1, ('Nous', 'PRON'): 1, ('ici', 'ADV'): 1})
total 18
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md", "limit": 6, "offset": 89}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md</path>
<type>file</type>
<content>
89: | langue fausse | **1/41 fr** | f33 « Si tu viens… » → `it` |
90: | langue `und` | **5** | f13, f18 (chiffres), f27, f37, f48 (latin) |
91: | cibles en mot fermé | **18/284** | `pas` (5), `est` (3), `ce` (2), `hier`, `M`… |
92: | cibles ambiguës par chaîne | **56/284** | cible présente >1 fois ; 9 cibles d'un caractère (`M`, `c`, `f`) |
93: | syntagmes sans cible | **76/360** | 70 GV, 4 GN, 2 GP ; **6/215** non-GV |
94: | rôles non normalisés | **106** `predicat` vs **39** `prédicat` ; **17** `qualite` vs **11** `qualité` | filtre client fragile |

(Showing lines 89-94 of 628. Use offset=95 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md", "new_string": "| cibles en mot fermé | **18/284** | `pas` (7), `est` (4), `ce`/`Ce` (4), `hier`, `ici`, `Nous` |", "old_string": "| cibles en mot fermé | **18/284** | `pas` (5), `est` (3), `ce` (2), … [17 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md has been updated successfully.
  ```

### 🤖 Assistant

⏵ Durcissement du test : compatible avec l'ajout de `schema`/`version` et du code 3

- **bash** `{"command": "cd /tmp && python3 - <<'PY'\np='/tmp/test_schema_produit.py'\ns=open(p).read()\ns=s.replace('''                self.assertEqual(set(d), CHAMPS_ACTUELS)\n''','''                # Les 11 champs actuels restent obligatoires ; les 8 champs du schéma v1\n                # peuvent s'ajouter s … [1682 caractères tronqués]`

  ```
patched
test_codes_de_sortie (__main__.TestContratActuel.test_codes_de_sortie) ... ok
test_determinisme (__main__.TestContratActuel.test_determinisme) ... ok
test_enveloppe_et_etiquettes (__main__.TestContratActuel.test_enveloppe_et_etiquettes) ... ok
test_refus_actuel_ou_cible (__main__.TestContratActuel.test_refus_actuel_ou_cible)
0.1.0 : refus = code 1, stdout vide. Cible : code 3 + JSON. Les deux passent. ... ok
setUpClass (__main__.TestSchemaV1) ... skipped "schéma v1 non livré : `schema` absent de l'annotation"

----------------------------------------------------------------------
Ran 4 tests in 2.817s

OK (skipped=1)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\n# 1) régénérer le JSON (le builder lit /tmp/test_schema_produit.py)\npython3 /tmp/build_json_report.py\n# 2) remplacer le bloc python du MD par le test à jour\npython3 - <<'PY'\nimport pathlib,re\np=pathlib.Path('reports/rapport-fiabil … [791 caractères tronqués]`

  ```
écrit /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-fiabilite-produit.json 103675 octets
md updated 38433
json code == md code True
compile OK
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 - <<'PY'\nimport pathlib,re,json\ns=pathlib.Path('reports/rapport-fiabilite-produit.md').read_text(encoding='utf-8')\nprint('fences',s.count('```'),'python blocks',len(re.findall(r'```python',s)),'json blocks',len(re.findall(r' … [940 caractères tronqués]`

  ```
fences 6 python blocks 1 json blocks 1
placeholders 0 0
tables 14 incoherentes 0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 - <<'PY'\nimport hashlib,json,pathlib,subprocess\nd=json.load(open('reports/pensee-fiabilite-produit.json'))\nfor name,path,key in [('drave','tools/drave.py','drave_py_sha256'),('bloc','tools/bloc_linguistique.py','bloc_linguis … [521 caractères tronqués]`

  ```
drave json 59a06f3e4f7d633a reel 59a06f3e4f7d633a ok True
bloc json 084517d9c10088b3 reel 084517d9c10088b3 ok True
head 56eb43af json 56eb43af
git blob bloc c1a08588 json c1a08588
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngrep -n '^#\\|^##\\|^###' reports/rapport-fiabilite-produit.md | head -40; echo ---; wc -l reports/rapport-fiabilite-produit.md; echo ---; grep -n \"6/215\\|pas.*(7)\\|Ran 4 tests\" reports/rapport-fiabilite-produit.md", "description": … [47 caractères tronqués]`

  ```
1:# Fiabilité du produit hors gold — 0 plantage sur 50 phrases, 4 refus sans JSON, 28/46 textes à chevauchement
42:## 1. Dispositif
61:## 2. Les 50 phrases : ce qui tient, ce qui casse
63:### 2.1 Ce qui tient
74:### 2.2 Ce qui casse (chiffré)
117:### 2.3 Les 4 refus du banc
131:### 2.4 Temps
159:## 3. Robustesse des entrées
161:### 3.1 Codes et arguments
181:### 3.2 Encodages
197:### 3.3 Les 10 000 caractères
210:### 3.4 Scripts non latins et entrées non-str
217:## 4. Le contrat de sortie
219:### 4.1 Ce qui est toujours présent
231:### 4.2 Ce qui peut être vide
249:### 4.3 Ce qui casserait un client
274:### 4.4 Le schéma minimal versionné (8 champs)
349:### 4.5 Le test de non-régression du schéma
538:## 5. Correctifs produit
544:### Bloquants
553:### Importants
567:### Confort
583:## 6. Contrôle négatif
603:## 7. Limites de l'audit
617:## 8. Conclusion — les 5 correctifs prioritaires
635:## Fichiers
---
641 reports/rapport-fiabilite-produit.md
---
91:| cibles en mot fermé | **18/284** | `pas` (7), `est` (4), `ce`/`Ce` (4), `hier`, `ici`, `Nous` |
93:| syntagmes sans cible | **76/360** | 70 GV, 4 GN, 2 GP ; **6/215** non-GV |
353:`/tmp` : `Ran 4 tests ... OK (skipped=1)` — les 4 tes
… [39 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 - <<'PY'\nimport json,pathlib\nd=json.load(open('reports/pensee-fiabilite-produit.json'))\nprint('json bytes',pathlib.Path('reports/pensee-fiabilite-produit.json').stat().st_size)\nprint('top keys',len(d),'banc',len(d['banc_50' … [341 caractères tronqués]`

  ```
json bytes 103675
top keys 19 banc 50 rob 49
verdict ⚠️ surface fiable (0 plantage, 0 JSON invalide, 0 span hors texte, 50/50 déterminisme) ; contrat non versionné et struct
statut test essayé à blanc depuis /tmp : 4 tests OK, 1 classe sautée (schéma v1 absent)
schema version 1.0
correctifs [4, 9, 8]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md", "limit": 12, "offset": 249}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md</path>
<type>file</type>
<content>
249: ### 4.3 Ce qui casserait un client
250: 
251: 1. **Pas de version de format** : 0/46 annotations portent `schema`/`version` ; `--version` ne
252:    rend que `drave 0.1.0`. Impossible d'épingler un rejeu à un format.
253: 2. **Refus sans JSON** : `--json` + texte vide/emoji/ponctuation → **stdout 0 octet**, code 1.
254:    Un pipeline `... --json | jq` casse ; le refus est confondu avec une erreur.
255: 3. **Chevauchements** : 107 paires / 28 textes ; un arbre ou un index par offset casse. Filtrer
256:    `meta.union` donne **0 conflit**, mais ce n'est pas dans le schéma : le client doit le deviner.
257: 4. **Cible sans offset** : 56/284 cibles apparaissent plusieurs fois ; 18 mots fermés ; 9 cibles
258:    d'un caractère. `texte.find(cible)` est ambigu ; il n'y a pas `cible_debut`/`cible_fin`.
259: 5. **POS trouées** : 302/1068 tokens sans POS (toute la ponctuation, tous les nombres) ; un
260:    alignement token → POS a des trous ; `POS —` sur les chiffres.

(Showing lines 249-260 of 641. Use offset=261 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md", "new_string": "3. **Chevauchements** : 107 paires / 28 textes ; un arbre ou un index par offset casse. Filtrer\n   `meta.union` donne **0 conflit**, mais ce n'est pas dans le schéma : le client doit … [275 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nfor t in \"Bonjour\" \"a\"; do python3 tools/drave.py analyser \"$t\" --json | python3 -c \"import json,sys;d=json.load(sys.stdin);print(repr('$t'),len(d['etiquettes']),sum(e['niveau']=='syntagme' for e in d['etiquettes']),sum(e['nivea … [97 caractères tronqués]`

  ```
'Bonjour' 7 0 1
'a' 8 1 1
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md", "new_string": "| un mot (`Bonjour`), un caractère (`a`) | 0 | **0** | oui | conforme ; 7 et 8 étiquettes (0 et 1 syntagme) |", "old_string": "| un mot (`Bonjour`), un caractère (`a`) | 0 | **0** | o … [37 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md", "limit": 10, "offset": 44}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md</path>
<type>file</type>
<content>
44: - **Banc libre** : 50 phrases écrites à la main pour cet audit — **41 françaises**, **5 anglaises**,
45:   **4 refus** (vide, espaces, ponctuation, emoji), **1 très longue** (f50 : 2 144 caractères,
46:   4 paragraphes). Les textes couvrent questions, impératives, négations, majuscules, chiffres,
47:   dates, URL, emails, chemins, caractères spéciaux, accents, emoji, abréviations, citations,
48:   ellipses, latin et un texte multi-paragraphes. **Aucune phrase ne vient du gold.**
49: - **Mesure** : `python3 tools/drave.py analyser TEXTE --json` en **subprocess** (comme un
50:   utilisateur), deux passages par texte, plus `analyser` lisible en parallèle. Validation de
51:   **20 invariants** : clés, spans, `valeur` vs tranche, chevauchements, cibles, POS, unités,
52:   fraction, types, sources, confiance, tri, doublons, déterminisme.
53: - **Temps** : horloge murale du processus CLI (démarrage Python compris) et `Heuristique().analyser`

(Showing lines 44-53 of 642. Use offset=54 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md", "new_string": "- **Banc libre** : 50 phrases écrites à la main pour cet audit — **41 françaises** (dont\n  **1 très longue**, f50 : 2 144 caractères, 4 paragraphes), **5 anglaises**, **4 refus**\n   … [787 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngit status --short --untracked-files=all | grep '^??' | head -20; echo ---; git status --short --untracked-files=all | wc -l; echo ---; git diff --stat HEAD -- tools/drave.py tools/bloc_linguistique.py reports/rapport-fiabilite-produit … [111 caractères tronqués]`

  ```
?? journal/2026-11-05/attention.md
?? journal/2026-11-06/distribue.md
?? journal/2026-11-06/docs.md
?? journal/2026-11-06/mesures.md
?? journal/2026-11-06/modele.md
?? journal/2026-11-06/outils.md
?? journal/2026-11-06/portes.md
?? journal/sessions/082fe8ca-3e1e-4454-b91b-12586843e880/digest.md
?? journal/sessions/082fe8ca-3e1e-4454-b91b-12586843e880/rapport.md
?? journal/sessions/14114f3d-ae0d-416e-ad8e-4d4eaa04c36c/digest.md
?? journal/sessions/14114f3d-ae0d-416e-ad8e-4d4eaa04c36c/rapport.md
?? journal/sessions/1555bdd3-27e9-4779-b1e7-716e32399c11/digest.md
?? journal/sessions/1555bdd3-27e9-4779-b1e7-716e32399c11/rapport.md
?? journal/sessions/1b0cf09a-a77a-443d-82e2-68a5d6cacdf0/digest.md
?? journal/sessions/1b0cf09a-a77a-443d-82e2-68a5d6cacdf0/rapport.md
?? journal/sessions/24001907-4f19-4ea5-87f6-98334496719f/digest.md
?? journal/sessions/24001907-4f19-4ea5-87f6-98334496719f/rapport.md
?? journal/sessions/24529ced-6556-4491-9633-9401c2dffb0c/digest.md
?? journal/sessions/24529ced-6556-4491-9633-9401c2dffb0c/rapport.md
?? journal/sessions/2cc1ad4a-373e-4362-a341-3c4a630c2e0c/digest.md
---
166
---
[stderr]
grep: write error: Broken pipe
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngrep -n \"test_refus_actuel_ou_cible\\|CHAMPS_ACTUELS | CHAMPS_V1\\|La classe TestSchemaV1\" reports/rapport-fiabilite-produit.md | head; python3 -c \"import json;d=json.load(open('reports/pensee-fiabilite-produit.json'));print('test c … [145 caractères tronqués]`

  ```
435:                self.assertTrue(set(d) <= (CHAMPS_ACTUELS | CHAMPS_V1),
436:                                sorted(set(d) - (CHAMPS_ACTUELS | CHAMPS_V1)))
470:    def test_refus_actuel_ou_cible(self) -> None:
473:        La classe TestSchemaV1 exige le code 3 ; ce test-ci ne gèle que le fait qu'un refus
test code updated True
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md", "limit": 14, "offset": 52}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md</path>
<type>file</type>
<content>
52:   **20 invariants** : clés, spans, `valeur` vs tranche, chevauchements, cibles, POS, unités,
53:   fraction, types, sources, confiance, tri, doublons, déterminisme.
54: - **Temps** : horloge murale du processus CLI (démarrage Python compris) et `Heuristique().analyser`
55:   en direct (durée interne, hors démarrage). Les deux sont rapportés par phrase dans le JSON.
56: - **Contrôle négatif** : **9 mutations** injectées dans une annotation valide (span hors texte,
57:   chevauchement, cible absente, confiance 1,7, clé manquante, fraction fausse, valeur hors span,
58:   attachement retiré, niveau inconnu) ; **9/9 détectées** (§ 6).
59: - **Portée** : le **CLI** et l'heuristique par défaut. Le neuronal, `Parallele`, `Cascade` et les
60:   profils UDHR ne sont pas mesurés ici ; un audit parallèle (A24) couvre l'API du bloc.
61: 
62: ## 2. Les 50 phrases : ce qui tient, ce qui casse
63: 
64: ### 2.1 Ce qui tient
65: 

(Showing lines 52-65 of 643. Use offset=66 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md", "new_string": "- **Portée** : le **CLI** et l'heuristique par défaut. Le neuronal, `Parallele`, `Cascade` et les\n  profils UDHR ne sont pas mesurés ici ; un audit parallèle (A24) couvre l'API du bl … [781 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 - <<'PY'\nimport pathlib\ns=pathlib.Path('reports/rapport-fiabilite-produit.md').read_text(encoding='utf-8')\nprint('fences',s.count('```'),'lines',s.count('\\n'))\nlines=s.splitlines(); in_code=False; groups=[]; cur=[]\nfor i, … [499 caractères tronqués]`

  ```
fences 8 lines 654
tables 14 incoherentes 0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-fiabilite-produit.json'))\nok=[x for x in d['banc_50']['resultats'] if x['rc']==0]\nsyn=[x['id'] for x in ok if x.get('chevauchements_syntagme',0)>0]\nprint('textes avec c … [327 caractères tronqués]`

  ```
textes avec chevauchement syntagme 23 ['f02', 'f05', 'f06', 'f10', 'f11', 'f20', 'f21', 'f22', 'f23', 'f24', 'f26', 'f29', 'f31', 'f32', 'f34', 'f38', 'f39', 'f41', 'f43', 'f44', 'f45', 'f46', 'f50']
textes avec un chevauchement quelconque (harness) 28; phrase type ['f20']
union texts ['f02', 'f05', 'f06', 'f10', 'f11', 'f20', 'f21', 'f22', 'f23', 'f24', 'f26', 'f29', 'f31', 'f32', 'f34', 'f38', 'f39', 'f41', 'f43', 'f44', 'f45', 'f46', 'f50']
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngrep -n \"28/46\\|28 textes\\|28/28\\|107 paires\" reports/rapport-fiabilite-produit.md; echo ---; grep -n '\"textes\": 28\\|28 textes\\|107 paires' reports/pensee-fiabilite-produit.json | head", "description": "Locate all 28-text over … [12 caractères tronqués]`

  ```
1:# Fiabilité du produit hors gold — 0 plantage sur 50 phrases, 4 refus sans JSON, 28/46 textes à chevauchement
21:mais **4 refus n'ont pas de JSON** (stdout vide, code 1), **28/46 succès** portent des syntagmes
36:| chevauchements de syntagmes | **28/46** textes, **107** paires |
90:| syntagmes qui se chevauchent | **107 paires** dans **28/46** textes ; **85/360** étiquettes `meta.union` | f02 : `REL 22-42` et `REL 22-54` ; f50 : 50 paires |
267:3. **Chevauchements** : 107 paires / 28 textes ; un arbre ou un index par offset casse. Filtrer
563:| **P0-3** | **Partition explicite des syntagmes** : `meta.alternative` + filtre `union` documenté (ou suppression mesurée) | **107 paires / 28 textes** ; 85 `union` ; 0 conflit après filtre | `bloc_linguistique.py` 1099-1156, 1179-1204, 1820-1849 | **0,5–1 j** | moyen : change F1/attachement ; préférer l'alternative étiquetée à la suppression |
626:- **Chevauchements** : les **107 paires** dépendent du banc ; l'audit A24 en compte **132** sur
636:3. **P0-3 — Partition explicite des syntagmes** : 107 paires sur 28/46 textes ; le filtre
---
80:    "textes": 28,
3467:   "Chevauchements : 107 paires sur 28/46 textes ; un arbre ou un index par o
… [355 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'PY'\np='/tmp/build_json_report.py'\ns=open(p).read()\ns=s.replace('''    \"chevauchements\": {\"textes\": 28, \"paires\": 107, \"union_labels\": 85,\n                       \"apres_filtre_union\": 0,\n                       \"tous_impliquent_union\": True},''','' … [583 caractères tronqués]`

  ```
patched
écrit /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-fiabilite-produit.json 103706 octets
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md", "limit": 40, "offset": 1}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md", "limit": 10, "offset": 86}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md</path>
<type>file</type>
<content>
1: # Fiabilité du produit hors gold — 0 plantage sur 50 phrases, 4 refus sans JSON, 28/46 textes à chevauchement
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Branche** : `s/v7` ·
4: > **Commit mesuré** : `56eb43af` (module `c1a08588`, `tools/drave.py` `59a06f3e`) ·
5: > **Date** : 2026-11-06 · **Verdict** : ⚠️ **la surface est fiable ; le contrat ne l'est pas encore.**
6: > **Aucun fichier existant modifié ; aucun commit.** Sorties : ce rapport et
7: > [`pensee-fiabilite-produit.json`](pensee-fiabilite-produit.json).
8: >
9: > **Dispositif** : [`tools/drave.py`](../tools/drave.py) (CLI : `analyser`, `evaluer`, `rejouer`,
10: > `--version`) et [`tools/bloc_linguistique.py`](../tools/bloc_linguistique.py) ;
11: > **50 phrases libres** écrites pour l'audit (textes dans le JSON) ; harnais local non committé
12: > dans `/tmp` ; machine **Xeon E5-2687W v3**, Python **3.13.16**.
13: >
14: > **Snapshot.** HEAD a bougé pendant l'audit (`6ef2a3f5` → `56eb43af`). Le module a reçu à
15: > **11 h 34** le correctif « non-str / surrogate » (`c1a0
… [1638 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md</path>
<type>file</type>
<content>
86: ### 2.2 Ce qui casse (chiffré)
87: 
88: | anomalie | mesure | où / exemple |
89: |---|---:|---|
90: | syntagmes qui se chevauchent | **107 paires** dans **28/46** textes ; **85/360** étiquettes `meta.union` | f02 : `REL 22-42` et `REL 22-54` ; f50 : 50 paires |
91: | partition après filtre `meta.union` | **0 conflit** | le filtre marche, mais n'est pas dans le schéma |
92: | textes sans aucun syntagme | **4/46** | f13 (emoji), f18 (chiffres), f27 « Élodie sourit. », f37 (email/téléphone) |
93: | POS manquantes | **302/1068** tokens | 257/257 ponctuations, 45/45 nombres ; 0/766 mots |
94: | `POS —` | **1/46** | f18, `1234567890` |
95: | frontière de phrase cassée | **6/46** textes | URL (f12, f38, f50), email (f37, f50), chemin (f39), abréviation (f20) |

(Showing lines 86-95 of 654. Use offset=96 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md", "new_string": "# Fiabilité du produit hors gold — 0 plantage sur 50 phrases, 4 refus sans JSON, 23/46 textes à chevauchement de syntagmes", "old_string": "# Fiabilité du produit hors gold — 0 planta … [68 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md", "new_string": "mais **4 refus n'ont pas de JSON** (stdout vide, code 1), **23/46 succès** portent des syntagmes", "old_string": "mais **4 refus n'ont pas de JSON** (stdout vide, code 1), **28/46 suc … [29 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md", "new_string": "| chevauchements de syntagmes | **23/46** textes, **107** paires |", "old_string": "| chevauchements de syntagmes | **28/46** textes, **107** paires |"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md", "new_string": "| syntagmes qui se chevauchent | **107 paires** dans **23/46** textes ; **85/360** étiquettes `meta.union` | f02 : `REL 22-42` et `REL 22-54` ; f50 : 50 paires |", "old_string": "| sy … [159 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md", "limit": 14, "offset": 95}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md</path>
<type>file</type>
<content>
95: | frontière de phrase cassée | **6/46** textes | URL (f12, f38, f50), email (f37, f50), chemin (f39), abréviation (f20) |
96: | fausses questions | **3** | `?page=2` dans une URL → phrase `interrogative` |
97: | phrases qui se chevauchent | **1** paire | f20 : `[0:59]` et `[2:59]` sur `M. Dupont…` |
98: | phrases commençant par un espace | **19/76** | f03, f20, f25, f26, f29, f50 (14) |
99: | documents tronqués à 60 caractères | **17/49** | f50 : 4 titres tronqués |
100: | faux titres de document | **2/49** | f18 (`1234567890`), f31 (`ÇA NE MARCHE PAS !!!`) |
101: | langue fausse | **1/41 fr** | f33 « Si tu viens… » → `it` |
102: | langue `und` | **5** | f13, f18 (chiffres), f27, f37, f48 (latin) |
103: | cibles en mot fermé | **18/284** | `pas` (7), `est` (4), `ce`/`Ce` (4), `hier`, `ici`, `Nous` |
104: | cibles ambiguës par chaîne | **56/284** | cible présente >1 fois ; 9 cibles d'un caractère (`M`, `c`, `f`) |
105: | syntagmes sans cible | **76/360** | 70 GV, 4 GN, 2 GP ; **6/215** non-GV |
106: | rôles non normalisés | **106** `predicat` vs **39** `p
… [274 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md", "new_string": "| `valeur` non uniforme | **295/4501** | phrase = type, pragmatique = acte, document tronqué, 4 morphèmes normalisés |\n\n**23 ou 28 ?** Les **107 paires de syntagmes** concernent **2 … [478 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngrep -n \"28/46\\|28 textes\\|/ 28 textes\\|sur 28\" reports/rapport-fiabilite-produit.md", "description": "Find remaining 28-text claims"}`

  ```
110:étiquettes de **même span** (`phrase` type/négation, `pragmatique` acte/double sens), **28 textes**
272:3. **Chevauchements** : 107 paires / 28 textes ; un arbre ou un index par offset casse. Filtrer
568:| **P0-3** | **Partition explicite des syntagmes** : `meta.alternative` + filtre `union` documenté (ou suppression mesurée) | **107 paires / 28 textes** ; 85 `union` ; 0 conflit après filtre | `bloc_linguistique.py` 1099-1156, 1179-1204, 1820-1849 | **0,5–1 j** | moyen : change F1/attachement ; préférer l'alternative étiquetée à la suppression |
641:3. **P0-3 — Partition explicite des syntagmes** : 107 paires sur 28/46 textes ; le filtre
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md", "new_string": "3. **Chevauchements** : 107 paires / 23 textes ; un arbre ou un index par offset casse. Filtrer", "old_string": "3. **Chevauchements** : 107 paires / 28 textes ; un arbre ou un index  … [27 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md", "new_string": "| **P0-3** | **Partition explicite des syntagmes** : `meta.alternative` + filtre `union` documenté (ou suppression mesurée) | **107 paires / 23 textes** ; 85 `union` ; 0 conflit après … [531 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md", "new_string": "3. **P0-3 — Partition explicite des syntagmes** : 107 paires sur 23/46 textes ; le filtre", "old_string": "3. **P0-3 — Partition explicite des syntagmes** : 107 paires sur 28/46 texte … [15 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-fiabilite-produit.json'))\nprint(d['banc_50']['synthese']['chevauchements'])\nprint([x for x in d['contrat']['ce_qui_casse_un_client'] if 'Chevauchements' in x])\nprint([x … [226 caractères tronqués]`

  ```
{'textes': 23, 'textes_tous_niveaux': 28, 'paires': 107, 'union_labels': 85, 'apres_filtre_union': 0, 'tous_impliquent_union': True}
["Chevauchements : 107 paires sur 23/46 textes ; un arbre ou un index par offset casse ; filtrer `meta.union` rend 0 conflit mais n'est pas dans le schéma."]
['107 paires / 23 textes ; 85 étiquettes `union` ; 0 conflit après filtrage ; un arbre client casse']
110:étiquettes de **même span** (`phrase` type/négation, `pragmatique` acte/double sens), **28 textes**
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngrep -n \"evaluer.*530\\|530–543\\|rejouer.*146\" reports/rapport-fiabilite-produit.md", "description": "Locate evaluer timing claim"}`

  ```
158:`evaluer` coûte **530–543 ms** ; `rejouer` **146–149 ms**. Les cinq textes les plus lents en CLI
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md", "new_string": "`evaluer` coûte **530–543 ms** sur le gold vivant et **577–600 ms** avec `--gold` ; `rejouer`\n**146–149 ms**. Les cinq textes les plus lents en CLI", "old_string": "`evaluer` coûte * … [81 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngrep -n \"gèle l'enveloppe\" reports/rapport-fiabilite-produit.md", "description": "Find test description sentence"}`

  ```
381:  déterminisme. Ce test passe sur le produit livré ; il gèle l'enveloppe et attrape une
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngrep -n \"test actuel\\|11+11\\|11 + 11\" reports/rapport-fiabilite-produit.md", "description": "Find contract test sentence"}`

  ```
554:(après le smoke test) et faire échouer la porte si le code sort ≠ 0. Le test actuel gèle
555:l'enveloppe 11+11 ; le test v1 gèle les 8 champs, `schema`, `version` et le refus code 3.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md", "new_string": "(après le smoke test) et faire échouer la porte si le code sort ≠ 0. Le test actuel gèle\nles 11 champs de l'enveloppe et n'admet, en plus, que les 8 champs du schéma v1 ; le test v1\ … [258 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-fiabilite-produit.md has been updated successfully.
  ```

### 🤖 Assistant

⏵ Validation finale des deux livrables (JSON, MD, tests, liens, fences)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 - <<'PY'\nimport json,pathlib,re\njsonp=pathlib.Path('reports/pensee-fiabilite-produit.json')\nmdp=pathlib.Path('reports/rapport-fiabilite-produit.md')\nd=json.loads(jsonp.read_text(encoding='utf-8'))\ns=mdp.read_text(encoding= … [1495 caractères tronqués]`

  ```
JSON valide; clés: 19 | banc: 50 | robustesse: 49
MD lignes: 661 | fences: 8 | placeholders: 0
test python compile OK 8454 chars
schema JSON parse OK ['schema', 'version', 'texte', 'langue', 'script', 'refus', 'etiquettes', 'unites_semantiques']
tables: 14 incohérentes: 0
liens morts: []
test JSON==MD: True
tailles: 103706 39588
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngrep -n \"23/46\\|23 textes\\|textes_tous_niveaux\" reports/rapport-fiabilite-produit.md reports/pensee-fiabilite-produit.json | head -20; echo ---; grep -n \"28/46\" reports/rapport-fiabilite-produit.md reports/pensee-fiabilite-produi … [63 caractères tronqués]`

  ```
reports/rapport-fiabilite-produit.md:1:# Fiabilité du produit hors gold — 0 plantage sur 50 phrases, 4 refus sans JSON, 23/46 textes à chevauchement de syntagmes
reports/rapport-fiabilite-produit.md:21:mais **4 refus n'ont pas de JSON** (stdout vide, code 1), **23/46 succès** portent des syntagmes
reports/rapport-fiabilite-produit.md:36:| chevauchements de syntagmes | **23/46** textes, **107** paires |
reports/rapport-fiabilite-produit.md:90:| syntagmes qui se chevauchent | **107 paires** dans **23/46** textes ; **85/360** étiquettes `meta.union` | f02 : `REL 22-42` et `REL 22-54` ; f50 : 50 paires |
reports/rapport-fiabilite-produit.md:109:**23 ou 28 ?** Les **107 paires de syntagmes** concernent **23 textes**. Si l'on compte aussi les
reports/rapport-fiabilite-produit.md:112:conflits de structure. Le chiffre à retenir pour un client qui construit un arbre est **23/46**.
reports/rapport-fiabilite-produit.md:273:3. **Chevauchements** : 107 paires / 23 textes ; un arbre ou un index par offset casse. Filtrer
reports/rapport-fiabilite-produit.md:570:| **P0-3** | **Partition explicite des syntagmes** : `meta.alternative` + filtre `union` documenté (ou suppression mesurée) | **107 paire
… [778 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification finale de l'état git et envoi du résultat au parent

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngit status --short --untracked-files=all -- reports/rapport-fiabilite-produit.md reports/pensee-fiabilite-produit.json\necho \"HEAD $(git rev-parse --short=8 HEAD)\"\necho \"fichiers: $(wc -c < reports/rapport-fiabilite-produit.md) o m … [479 caractères tronqués]`

  ```
?? reports/pensee-fiabilite-produit.json
?? reports/rapport-fiabilite-produit.md
HEAD 56eb43af
fichiers: 39588 o md / 103706 o json
banc 46 succès, 4 refus, 0 plantages
chevauchements {'textes': 23, 'textes_tous_niveaux': 28, 'paires': 107, 'union_labels': 85, 'apres_filtre_union': 0, 'tous_impliquent_union': True}
robustesse {'cas': 49, 'conformes': 33, 'anomalies': 9, 'limites': 7, 'echecs_internes': 2, 'codes_observes': [0, 1, 2], 'codes_3_4': 'non implémentés'}
  ```

- **send_message** `{"agent_id": "e181ce02-cd50-488a-a6be-e84b79d40dcc", "message": "Audit fiabilité produit terminé. **Deux fichiers neufs, aucun existant modifié, aucun commit** :\n- `reports/rapport-fiabilite-produit.md` (661 lignes, 39,6 Ko)\n- `reports/pensee-fiabilite-produit.json` (103,7 Ko : 50 textes + mesures … [3296 caractères tronqués]`

  ```
message delivered to agent e181ce02-cd50-488a-a6be-e84b79d40dcc
  ```

### 🤖 Assistant

⏵ Clôture : résumé de l'audit et des deux livrables

Audit terminé. **Deux fichiers neufs**, aucun existant modifié, aucun commit :

- [`reports/rapport-fiabilite-produit.md`](reports/rapport-fiabilite-produit.md) — 661 lignes
- [`reports/pensee-fiabilite-produit.json`](reports/pensee-fiabilite-produit.json) — 103,7 Ko (50 textes, mesures par phrase, robustesse, contrat, schéma, test, correctifs)

**Snapshot mesuré** : HEAD `56eb43af`, module `bloc_linguistique.py` git `c1a08588` / sha256 `084517d9`, `drave.py` sha256 `59a06f3e`. HEAD a bougé pendant l'audit (`6ef2a3f5` → `56eb43af`) ; le module a reçu à 11 h 34 le correctif non-str/surrogate (`c1a08588`), le banc a tourné à 11 h 40 après ce correctif ; `drave.py` n'a pas changé.

**50 phrases libres** (41 fr dont 1 de 2 144 car., 5 en, 4 refus) :
- **0 plantage**, **0 JSON invalide**, **0 sortie vide sur succès**, **0 span hors texte/vide**, **0 clé manquante**, **0 cible absente du texte**, **50/50 déterminisme**, 0 `stderr` sur succès.
- **4 refus** : code 1, stdout 0 octet, message `vide` ; **4/46 succès sans aucun syntagme** (dont « Élodie sourit. »), **1/46 sans POS** (chiffres).
- **23/46 textes** avec chevauchement de syntagmes (**107 paires**, 85 `meta.union`, 0 conflit après filtrage union ; 28/46 avec les mêmes-span multi-label).
- **302/1068 tokens sans POS** (257 ponctuation, 45 nombres) ; **18/284 cibles mots fermés**, **56/284 cibles ambiguës**, **0 offset de cible** ; **6/46 frontières de phrase cassées**, **3 fausses questions**.
- **Temps CLI** : 136,8–226,6 ms, médiane **152,7 ms** (démarrage ~146 ms) ; **interne** : 0,2–45,1 ms, médiane **1,0 ms**. **10 k** : 590–765 ms CLI, 331,6 ms interne, 2,76 Mo de JSON ; **50 k** : 5,44 s, 11,5 Mo.
- **Hors banc, 2 échecs internes** : UTF-8 invalide mêlé à des lettres (`UnicodeEncodeError` à l'écriture JSON) et stdout ASCII. NFD → tokens coupés, 0 syntagme. Codes 3/4 absents.

**Contrat** : 11 clés racine + 11 par étiquette stables (46/46, 4501/4501), mais **ni `schema` ni `version`**, **refus sans JSON**, **cible sans offset**, `meta`/`candidats`/`trace`/`cout` à schéma variable, `valeur` non uniforme sur 295/4501. Le schéma v1 proposé a **8 champs obligatoires** (`schema`, `version`, `texte`, `langue`, `script`, `refus`, `etiquettes`, `unites_semantiques`) + JSON Schema 2020-12 + test complet prêt pour `tools/tests/test_schema_produit.py` (essai à blanc : 4 tests OK, classe v1 sautée). Contrôle négatif : **9 mutations, 9/9 détectées**.

**5 correctifs prioritaires** :
1. **P0-1** versionner le format — 2 h.
2. **P0-2** refus JSON + code 3 — 2 h.
3. **P0-3** partition explicite des syntagmes — 0,5–1 j.
4. **P0-4** frontières de phrase/tokénisation — 0,5–1 j.
5. **P1-1** cibles d'attachement offsettées — 4 h.

Juste derrière : **P1-2** POS (302/1068) et **P1-4** syntagmes vides (4/46). Limites : pas de gold libre, banc écrit à la main, une seule machine ; l'audit A24 (API) compte 132 paires sur son propre banc, non comparables.

