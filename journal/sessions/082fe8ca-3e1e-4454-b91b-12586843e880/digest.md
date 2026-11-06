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

