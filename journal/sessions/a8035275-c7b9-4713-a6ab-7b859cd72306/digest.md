# Session DSH — relecture

- identifiant : `a8035275-c7b9-4713-a6ab-7b859cd72306`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-05 13:11:54
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **diagnostiquer les 57 échecs du top-k strict** de l'attachement.

Contexte : `tools/tests/linguistique/evaluer_gold.py` expose `charger()` (612 phrases) et `evaluer_bloc` ; `tools/bloc_linguistique.py` expose `Heuristique`. Sur les 145 segments gold dont le span est prédit, la cible du gold est dans les `candidats` du segment 134 fois en **sous-chaîne** mais seulement **88 fois en égalité exacte**. Les candidats viennent du générateur S (chaînes du type « « dans le parc » → a vu ») et de `_verbes_proches` (verbes des GV proches).

À faire :
1. Écris un script Python (exécuté via heredoc, sans fichier temporaire dans le dépôt) qui, pour chacun des 57 segments en échec strict, relève : type du segment, texte du segment, cible du gold, cible choisie (`meta.attachement.cible`), liste des candidats, et la raison probable de l'échec.
2. Classe les causes en catégories **explicites** (par ex. : candidat textuel non réduit à sa tête ; candidat de phrase et non de segment ; cible hors lexique verbal ; cible nommée par un GN non couvert ; autre) avec les effectifs.
3. Propose **3 correctifs concrets**, ordonnés par gain attendu (nombre de segments concernés), en précisant pour chacun le fichier et la fonction à modifier (sans les modifier).
4. Écris **uniquement** deux fichiers neufs : `reports/rapport-topk-diagnostic.md` (fiche : titre, verdict, tableau des causes, les 3 correctifs, contrôle négatif, limites) et `reports/pensee-topk-diagnostic.json`.

Règles strictes : ne committe rien ; ne modifie aucun fichier existant ; n'écris pas dans `docs/pilotage/`, `AGENTS.md`, `journal/`, `tools/structures/`, `data/`, `tools/entrainer_native.py`, `tools/native_model.py`. Rends un résumé avec les effectifs par cause et les 3 correctifs chiffrés.
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

⏵ Exploration du dépôt et des fichiers d'évaluation gold

Let me start by exploring the repository structure and the relevant files.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short | head -20 && echo \"---BRANCH---\" && git branch --show-current && echo \"---LS---\" && ls", "description": "Check git status and repo layout"}`

  ```
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
MM journal/sessions/MANIFEST.md
MM journal/sessions/aeafe951-9c3d-4bb5-8af7-0246a4f3d51d/digest.md
MM journal/sessions/aeafe951-9c3d-4bb5-8af7-0246a4f3d51d/rapport.md
MM journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
MM journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
---BRANCH---
s/v7
---LS---
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
run_real_clust
… [67 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && wc -l tools/tests/linguistique/evaluer_gold.py tools/bloc_linguistique.py 2>&1 && ls reports/ 2>&1 | head -20", "description": "Count lines in key files and list reports"}`

  ```
283 tools/tests/linguistique/evaluer_gold.py
  1881 tools/bloc_linguistique.py
  2164 total
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

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"attachement\\|def charger\\|def evaluer_bloc\\|candidats\" tools/bloc_linguistique.py | head -80", "description": "Locate attachment logic in bloc_linguistique"}`

  ```
7:    **candidats** pour l'ambigu ; elle déclare sa couverture et sa confiance ;
19:`niveau`, son `span`, sa `source`, sa `confiance`, sa `langue`, son `script` et ses `candidats`.
76:    candidats: list[str] = field(default_factory=list)
86:            "candidats": list(self.candidats), "langue": self.langue,
158:def charger_profils_udhr(chemin: pathlib.Path, train=(0, 14), test=(15, 30),
672:        """Les verbes des `k` GV les plus proches — les **candidats** d'attachement."""
708:                                 "texte": texte[d:mots[j - 1][1]], "candidats": []})
721:                                 "texte": texte[d:mots[j - 1][1]], "candidats": []})
730:                                 "texte": texte[d:mots[j - 1][1]], "candidats": []})
739:                                 "texte": texte[d:mots[j - 1][1]], "candidats": []})
783:                                            candidats=[] if not ouvert else [classe.lower()],
790:                                                self.nom, 0.32, candidats=[genre],
808:                                        candidats=["assertion", "question", "ordre"],
813:                                            self.nom, 0.25, candidats=["littéral
… [1711 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture du générateur S et de la logique d'attachement

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "offset": 620, "limit": 290}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
620:                           texte[debut:fin])
621:         return mots[-1] if mots else None
622: 
623:     @staticmethod
624:     def _verbe_dans(texte: str, debut: int, fin: int,
625:                     verbes: list[tuple[int, int, str]] | None = None,
626:                     strict: bool = False) -> str | None:
627:         """Le **verbe** du span : le lexique d'abord, puis le POS `VERB`, sinon le dernier mot."""
628:         mots = [(m.start() + debut, m.group()) for m in re.finditer(r"[\wÀ-ÿ'-]+", texte[debut:fin])]
629:         # le verbe **plein** d'abord : « J'ai vu » donne `vu`, pas `ai`
630:         for _, m in mots:
631:             if _est_verbe(m) and _normaliser(m) not in AUXILIAIRES:
632:                 return m
633:         for _, m in mots:
634:             if _est_verbe(m):
635:                 return m
636:         if verbes:
637:             for d, f, v in verbes:
638:                 if d >= debut and f <= fin:
639:                     return v
640:         return None if strict else (mots[-1][1] if mots else None)
641: 
642:     @staticmeth
… [17081 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls tools/tests/linguistique/ && python3 -c \"\nimport json\np=json.load(open('tools/tests/linguistique/gold.json'))['phrases']\nprint('gold.json', len(p))\nprint(json.dumps(p[0], ensure_ascii=False)[:800])\n\"", "description": "List  … [37 caractères tronqués]`

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
gold.json 20
{"id": "g001", "langue": "fr", "texte": "Le chat dort.", "mots": [{"texte": "Le", "pos": "DET", "debut": 0, "fin": 2}, {"texte": "chat", "pos": "NOUN", "debut": 3, "fin": 7}, {"texte": "dort", "pos": "VERB", "debut": 8, "fin": 12}], "segments": [{"type": "GN", "texte": "Le chat", "role": "agent", "debut": 0, "fin": 7}, {"type": "GV", "texte": "dort", "role": "prédicat", "debut": 8, "fin": 12}], "pragma": {"acte": "assertion"}}
  ```

### 🤖 Assistant

⏵ Reproduction des chiffres 145 / 134 / 88 par script heredoc

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, json, collections\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nsys.path.insert(0,'tools/tests/linguistique')\nfrom evaluer_gold import charger\nph = charger()\nprint('phrases', len(ph))\n … [899 caractères tronqués]`

  ```
phrases 612
cibles 239 labels 145 sous-chaine 134 exact 88
Counter({'reel': 432, 'synthetique': 160, 'hand': 20})
  ```

### 🤖 Assistant

⏵ Extraction des 57 échecs stricts et premiers motifs

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, json, collections\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl\nfrom evaluer_gold import charger\nph=charger(); h=bl.Heuristique()\nrows=[]\n … [1215 caractères tronqués]`

  ```
57 echecs stricts; 46 en sous-chaine
---
hand g002 GP 'de la voisine' | cible= 'chat' | choisie= '' | substr= False
  cands= ['GP']
---
hand g011 REL "que j'ai lu" | cible= 'livre' | choisie= 'livre' | substr= True
  cands= ["« que j'ai lu » → Le livre", 'est']
---
hand g012 GP 'à manger' | cible= 'prêt' | choisie= 'manger' | substr= True
  cands= ['« à manger » → Le canard', '« à manger » → est prêt', 'manger', 'est']
---
reel r014 REL "que j'ai lu" | cible= 'livre' | choisie= 'livre' | substr= True
  cands= ["« que j'ai lu » → Le livre", 'est']
---
reel r015 REL 'dont elle parle' | cible= 'film' | choisie= 'film' | substr= True
  cands= ['« dont elle parle » → Le film', 'sorti']
---
reel r018 GP 'à manger' | cible= 'prête' | choisie= 'manger' | substr= True
  cands= ['« à manger » → La souris', '« à manger » → est prête', 'manger', 'est']
---
reel r047 GP 'dans le jardin' | cible= 'poussent' | choisie= 'poussent' | substr= True
  cands= ['« dans le jardin » → Les fleurs poussent']
---
reel r054 REL 'que tu lis' | cible= 'livre' | choisie= 'livre' | substr= True
  cands= ['« que tu lis » → Le livre', 'est']
---
reel r055 REL 'où nous vivons' | cible= 'ville' | choisie= 'ville' | s
… [6636 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Inspection du générateur S et de `_cibles_s` pour expliquer les cas S

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"structure la plus proche\\|def _cibles_s\\|def _syntagmes_s\\|attachement\" tools/bloc_linguistique.py | head -40", "description": "Locate S generator and cibles_s"}`

  ```
588:    def _syntagmes_s(self, texte: str) -> list[dict] | None:
599:    def _cibles_s(self, texte: str) -> dict:
672:        """Les verbes des `k` GV les plus proches — les **candidats** d'attachement."""
688:    def _syntagmes_simple(self, texte: str, langue: str) -> list[dict]:
823:            # candidat d'attachement (diagnostic des 33 échecs de T162).
834:                    att = c.get("attachement") or {}
857:                        meta["attachement"] = {"segment": s.get("texte", ""), "cible": cible}
870:                    meta["attachement"] = {"segment": s["texte"], "cible": cible}
889:                    meta["attachement"] = {"segment": s["texte"], "cible": cible}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"structure la plus proche\" tools/ | head -10", "description": "Find the literal source of structure la plus proche"}`

  ```
tools/structures/donnees/phrases_generees.json:912:     "nom": "structure la plus proche",
tools/structures/donnees/phrases_generees.json:4781:     "nom": "structure la plus proche",
tools/structures/donnees/phrases_generees.json:6176:     "nom": "structure la plus proche",
tools/structures/donnees/phrases_generees.json:7031:     "nom": "structure la plus proche",
tools/structures/donnees/phrases_generees.json:7376:     "nom": "structure la plus proche",
tools/structures/donnees/phrases_generees.json:7415:     "nom": "structure la plus proche",
tools/structures/donnees/phrases_generees.json:7851:     "nom": "structure la plus proche",
tools/structures/donnees/phrases_generees.json:9870:     "nom": "structure la plus proche",
tools/structures/donnees/phrases_generees.json:9917:     "nom": "structure la plus proche",
tools/structures/donnees/phrases_generees.json:11109:     "nom": "structure la plus proche",
[stderr]
grep: tools/structures/__pycache__/generateur.cpython-313.pyc: binary file matches
grep: write error: Broken pipe
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 40, "offset": 580}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
580:                 break
581:         for pre in PREFIXES:
582:             if len(n) > len(pre) + 2 and n.startswith(pre):
583:                 sortie.append(("préfixe", 0, len(pre), pre))
584:                 break
585:         return sortie
586: 
587:     # -- syntagmes ----------------------------------------------------------
588:     def _syntagmes_s(self, texte: str) -> list[dict] | None:
589:         if not self.segmenter_s:
590:             return None
591:         try:
592:             if str(RACINE / "tools/structures") not in sys.path:
593:                 sys.path.insert(0, str(RACINE / "tools/structures"))
594:             import generateur  # le générateur S, importé en lecture seule
595:             return generateur.analyser(texte)
596:         except Exception:
597:             return None
598: 
599:     def _cibles_s(self, texte: str) -> dict:
600:         """Toutes les cibles du générateur S (pas seulement le dernier segment ambigu).
601: 
602:         Lecture seule de l'API interne du S : `_tokens`/`_segmente` rendent les `Segment` avec
603:    
… [944 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls tools/structures/ && grep -n \"attachement\" tools/structures/generateur.py | head -20", "description": "Inspect structures generator attachment"}`

  ```
arbre_svg.py
candidats_corpus.py
construire_donnees.py
donnees
exporter_corpus.py
generateur.py
llm.py
mesure_analyseur.py
mesure_arbre.py
mesure_corpus.py
__pycache__
README.md
serveur.py
static
tests
verifier_corpus.py
6:plusieurs candidats en variant l'**attachement** de chaque segment ambigu (GN le plus proche ou
485:    # les cibles d'attachement : GN, tête du GP et GV les plus proches à gauche
506:    """Le rôle change avec l'attachement : instrument/attribut, possession/thème."""
550:        attachement = ({"segment": s.texte, "cible": cible[1], "genre": cible[0]}
557:        clé = json.dumps([[(x.debut, x.fin, x.type, x.role, x.niveau) for x in segs], attachement],
562:        candidats.append({"nom": nom, "lecture": lecture, "attachement": attachement,
622:    """La structure de base, sans variantes d'attachement ; `roles=False` coupe les règles.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/generateur.py", "limit": 120, "offset": 480}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/generateur.py</path>
<type>file</type>
<content>
480:                     break
481:             for g in segs[k + 1:]:
482:                 if g.type == "GP" and _norm(g.texte).split()[:1] == ["par"]:
483:                     g.role = "agent"
484:                     break
485:     # les cibles d'attachement : GN, tête du GP et GV les plus proches à gauche
486:     def _tete_gp(g):
487:         mots = [m for m in MOTIF.finditer(texte, g.debut, g.fin) if m.group().strip()
488:                 and _norm(m.group()) not in PREP | DET]
489:         return mots[-1].group() if mots else None
490:     for k, s in enumerate(segs):
491:         for g in reversed(segs[:k]):
492:             if g.type == "GN" and s.cible_nom is None:
493:                 s.cible_nom = g.texte
494:             if g.type == "GP" and s.cible_gp is None:
495:                 s.cible_gp = _tete_gp(g)
496:             if g.type == "GV" and s.cible_verbe is None:
497:                 s.cible_verbe = g.texte
498:     construire_arbre(segs)
499:     return segs
500: 
501: 
502: ROLES_AMBIGUS = {"pour": ["cause"]}
503: 
504: 
505: def _role_attache(
… [4853 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 620,720p tools/structures/generateur.py", "description": "Read base segmentation and analyser"}`

  ```
def structure(texte: str, roles: bool = True) -> list[dict]:
    """La structure de base, sans variantes d'attachement ; `roles=False` coupe les règles.

    C'est ce que mesure `mesure_analyseur.py` : la segmentation et les rôles, pas le choix
    d'un candidat. `roles=False` rend les rôles par défaut (le contrôle « règles coupées »).
    """
    segs = _segmente(texte, _tokens(texte))
    sortie = []
    for s in segs:
        d = s.dict()
        if not roles and s.type in ROLES_DEFAUT:
            d["role"] = ROLES_DEFAUT[s.type]
        sortie.append(d)
    return sortie


if __name__ == "__main__":
    import sys
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    texte = args[0] if args else "Le chat de la voisine qui dort sur le toit se réveille."
    cs = analyser(texte)
    if "--json" in sys.argv:
        print(json.dumps(cs, ensure_ascii=False, indent=1))
    else:
        for c in cs:
            print(f"- {c['nom']}")
            for s in c["segments"]:
                print("   " + "  " * s["niveau"] + f"{s['texte']!r} [{s['type']} · {s['role']}]")
  ```

### 🤖 Assistant

⏵ Diagnostic fin des cas anglais, sans candidat et SUB

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl\nfrom evaluer_gold import charger\nph={p.get('id'):p for p in charger()}\nh=bl.Heuristique()\nfor … [1051 caractères tronqués]`

  ```
================================================================================
r080 reel 'The birds fly over the lake.' | langue en
segments gold: [('GP', 'over the lake', 'fly')]
pred syntagmes: [('GN', 'The birds fly', 0, 13, ['GN', 'lake'], {'segment': 'The birds fly', 'cible': 'lake'}), ('GV', 'The birds fly over the lake', 0, 27, ['structure la plus proche'], None), ('GP', 'over the lake', 14, 27, ['GP', 'lake'], {'segment': 'over the lake', 'cible': 'lake'})]
pos: [('The', 'DET'), ('birds', 'NOUN'), ('fly', 'NOUN'), ('over', 'PREP'), ('the', 'DET'), ('lake', 'NOUN')]
simple: [('GN', 'The birds fly'), ('GP', 'over the lake')]
S candidates: [('structure la plus proche', None)]
est_verbe cibles: [('fly', False)]
================================================================================
r120 reel 'The river flows to the sea.' | langue en
segments gold: [('GP', 'to the sea', 'flows')]
pred syntagmes: [('GN', 'The river flows', 0, 15, ['GN', 'river'], {'segment': 'The river flows', 'cible': 'river'}), ('GV', 'The river flows to the sea', 0, 26, ['structure la plus proche'], None), ('GP', 'to the sea', 16, 26, ['GP', 'river'], {'segment': 'to the sea', 'cible': 'river'})]
po
… [3656 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de `_est_verbe`, `_pos` et des lexiques anglais

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"def _est_verbe\\|def _pos\\|VERBES_\\|AUXILIAIRES\\s*=\" tools/bloc_linguistique.py | head -40", "description": "Locate verb lexicon and POS function"}`

  ```
369:VERBES_IMPERATIFS = set("va viens prends fais dis regarde écoute donne cherche trouve ouvre ferme "
374:VERBES_CONNUS = set("""
419:AUXILIAIRES = set("""
428:def _est_verbe(mot: str) -> bool:
433:    if n in VERBES_CONNUS:
438:        if n.endswith(suf) and n[:-len(suf)] in VERBES_CONNUS:
442:        if n.endswith(suf) and (n[:-len(suf)] + "er") in VERBES_CONNUS:
548:    def _pos(self, langue: str, mot: str) -> tuple[str, bool, float]:
806:                    "ordre" if premier.casefold() in VERBES_IMPERATIFS else "assertion")
1133:    def _post(self, invite: str, grammaire: str, max_jetons: int) -> str:
1267:    def _post(self, invite: str, grammaire: str, max_jetons: int) -> str:
1437:    def _post(self, invite: str, grammaire: str, max_jetons: int) -> str:
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 75, "offset": 369}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 40, "offset": 548}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
369: VERBES_IMPERATIFS = set("va viens prends fais dis regarde écoute donne cherche trouve ouvre ferme "
370:                         "go take come look give find open close".split())
371: 
372: # Un lexique verbal minimal, bilingue, pour arbitrer les classes ouvertes : le POS de surface
373: # tague « talks » NOUN et « brother » VERB (mesuré le 05/11 sur les 22 GP restants).
374: VERBES_CONNUS = set("""
375: parler parle parles parlent parlait parlaient parlerai jouer joue joues jouent jouait jouaient
376: manger mange manges mangent mangeait mangeaient écrire écrit écris écrivent écrivait écrivaient
377: lire lis lisent lisait lisaient dormir dort dorment dormait dormaient partir part pars partent
378: partait partaient venir viens vient viennent venait venaient prendre prend prends prennent
379: prenait prenaient mettre mets met mettent mettait mettaient dire dis dit disent disait disaient
380: voir vois voit voient voyait voyaient vu vue vus vues savoir sais sait savent savait savaient su
381: pouvoir peux peut
382: pouvons peuvent pouvait pouvaient vouloir veux v
… [4633 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
548:     def _pos(self, langue: str, mot: str) -> tuple[str, bool, float]:
549:         lex = POS_FERME.get(langue, POS_FERME["fr"])
550:         n = _normaliser(mot).split("'")[0].split("’")[0]
551:         for classe, mots in lex.items():
552:             if n in mots:
553:                 return classe, False, 0.92
554:         if n in VERBES.get(langue, VERBES["fr"]):
555:             return "VERB", True, 0.72
556:         if n in ADJECTIFS.get(langue, ADJECTIFS["fr"]):
557:             return "ADJ", True, 0.68
558:         if re.fullmatch(r"\d+(?:[.,]\d+)*", mot):
559:             return "NUM", False, 0.95
560:         if mot[:1].isupper() and mot[1:].islower() and mot not in {"Le", "La", "Les", "Un", "Une", "The"}:
561:             return "NOUN", True, 0.55
562:         if len(n) >= 4 and n.endswith(("ment", "ly")):
563:             return "ADV", True, 0.45
564:         if len(n) >= 4 and n.endswith(("tion", "sion", "ness", "ity", "ité", "ance", "ence")):
565:             return "NOUN", True, 0.45
566:         if len(n) >= 4 and n.endswith(("er", "ir", "ing", "e
… [1093 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Simulation des correctifs candidats pour mesurer les gains réels

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, re, collections\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl\nfrom evaluer_gold import charger\nph=charger(); h=bl.Heuristique()\n\ndef colle … [2289 caractères tronqués]`

  ```
base fails: 57
F1 fixes fails: 41 / 57
F1 total exact: 129
F1b (last token all) total exact: 129 fixes fails: 41
remaining after F1:
  g002 fr GP 'de la voisine' -> 'chat' cands ['GP']
  r080 en GP 'over the lake' -> 'fly' cands ['GP', 'lake']
  r108 en GP 'on the roof' -> 'climbs' cands ['GP', 'roof']
  r120 en GP 'to the sea' -> 'flows' cands ['GP', 'river']
  r156 en GP 'in the water' -> 'swims' cands ['GP', 'water']
  r166 en GP 'on the train' -> 'get' cands ['GP', 'train']
  r169 en GP 'at his mother' -> 'smiles' cands ['GP', 'mother']
  r177 en GP 'in front of the door' -> 'wait' cands ['GP', 'door']
  r180 en GP 'to the library' -> 'belongs' cands ['GP', 'library']
  r201 fr REL 'qui parle' -> 'homme' cands ["« qui parle » → L'homme", 'est']
  r209 fr REL 'dont je parle' -> 'élève' cands ["« dont je parle » → L'élève", 'est']
  r230 fr SUB 'Quand tu arrives' -> 'appelle' cands ['structure la plus proche', 'appelle-moi']
  r235 fr REL 'où nous allons' -> 'endroit' cands ["« où nous allons » → L'endroit", 'est']
  r263 fr REL 'qui vole' -> 'oiseau' cands ["« qui vole » → L'oiseau", 'est']
  r309 fr SUB "qu'il viendra" -> 'viendra' cands ['structure la plus proche', 'Peut-être'
… [54 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Simulation du correctif lexique anglais (F2) et contrôle négatif

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, re, importlib\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl\nfrom evaluer_gold import charger\nph=charger()\n\nEN = set(\"\"\"fly flies flew f … [1824 caractères tronqués]`

  ```
baseline labels 145 exact 88
F2 lexicon EN labels 145 exact 96
F2 fixes 8 breaks 0 remaining 49
  + ('r180', 17, 31, 'GP')
  + ('r166', 18, 30, 'GP')
  + ('r169', 16, 29, 'GP')
  + ('r108', 15, 26, 'GP')
  + ('r177', 19, 39, 'GP')
  + ('r080', 14, 27, 'GP')
  + ('r120', 16, 26, 'GP')
  + ('r156', 15, 27, 'GP')
remaining after F2: 49
  g002 fr GP 'de la voisine' -> 'chat' cands ['GP']
  g011 fr REL "que j'ai lu" -> 'livre' cands ["« que j'ai lu » → Le livre", 'est']
  g012 fr GP 'à manger' -> 'prêt' cands ['« à manger » → Le canard', '« à manger » → est prêt', 'manger', 'est']
  r014 fr REL "que j'ai lu" -> 'livre' cands ["« que j'ai lu » → Le livre", 'est']
  r015 fr REL 'dont elle parle' -> 'film' cands ['« dont elle parle » → Le film', 'sorti']
  r018 fr GP 'à manger' -> 'prête' cands ['« à manger » → La souris', '« à manger » → est prête', 'manger', 'est']
  r047 fr GP 'dans le jardin' -> 'poussent' cands ['« dans le jardin » → Les fleurs poussent']
  r054 fr REL 'que tu lis' -> 'livre' cands ['« que tu lis » → Le livre', 'est']
  r055 fr REL 'où nous vivons' -> 'ville' cands ['« où nous vivons » → La ville', 'est']
  r057 fr GP 'contre le facteur' -> 'aboie' cands ['« contre le
… [3650 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Validation de F1 avec tête à élision et simulation F3

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, re\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl\nfrom evaluer_gold import charger\nph=charger(); h=bl.Heuristique()\n\ndef rows_now():\n    r … [1512 caractères tronqués]`

  ```
F1 tete (elision) fixes: 45
controle premier token fixes: 0 []
s108 tail heads: ['rêve'] cible rêve
s122 tail heads: ['saute'] cible saute
g012 tail heads: ['canard', 'prêt', None, None] cible prêt
r018 tail heads: ['souris', 'prête', None, None] cible prête
r201 tail heads: ['homme', None] cible homme
  ```

### 🤖 Assistant

⏵ Recherche du format des fiches et JSON « pensée » existants

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls reports/ | grep -i \"pensee\\|topk\\|attachement\" | head -20 && echo \"---\" && grep -rln \"pensee-\" reports/ | head -10", "description": "Find existing pensee JSON conventions"}`

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
---
reports/rapport-pensee-sans-verbaliser.md
reports/rapport-pensee-ac3-alphabeta.md
reports/rapport-pensee-drvf.md
reports/rapport-pensee-banc.md
reports/rapport-pensee-gold-linguistique.md
reports/rapport-pensee-operateurs.md
reports/rapport-pensee-necessaire.md
reports/rapport-pensee-labyrinthe.md
reports/rapport-pensee-porte.md
reports/rapport-pensee-porte-apprise.md
[stderr]
grep: write error: Broken pipe
grep: write error: Broken pipe
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls reports/*.json | head -5 && python3 -c \"\nimport json,glob\nfor f in glob.glob('reports/pensee*.json')[:3]:\n    d=json.load(open(f)); print(f, list(d)[:10])\n\" 2>&1 | head -20", "description": "Inspect JSON report schemas"}`

  ```
reports/a26-bilan.json
reports/a26-lot-disque.json
reports/a80-audit-final.json
reports/a80-indice-qualifie.json
reports/a80-melange-qualifie.json
reports/pensee-multilingue.json ['n', 'couches', 'langues', 'resultats']
reports/pensee-ac3-alphabeta.json ['date', 'ligne', 'verdict', 'ac3', 'alphabeta', 'portes']
reports/pensee-drvf.json ['date', 'ligne', 'verdict', 'drvf', 'portes']
[stderr]
ls: write error: Broken pipe
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rln \"top-k strict\\|topk_exact\\|attachement\" reports/*.md | head -10", "description": "Find reports mentioning attachment top-k"}`

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
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,60p reports/rapport-pensee-gold-linguistique.md 2>/dev/null; echo '===JSON==='; python3 -c \"\nimport json; d=json.load(open('reports/pensee-ac3-alphabeta.json')); print(json.dumps(d,ensure_ascii=False,indent=1)[:1500])\"",  … [54 caractères tronqués]`

  ```
# L — le gold 360 : 200 réels + 160 synthétiques, POS 0,772, tête 0,966

> **Ligne de roadmap** : **R0.7** (bloc linguistique) / **L** · **Date** : 2026-11-01 ·
> **Verdict** : ✅ **le gold étendu et l'attachement sont mesurés** — **180 phrases** (20 réelles écrites à la main,
> 160 synthétiques d'une grammaire indépendante), **804 tokens** ; POS **0,751** (fermé
> **0,939**, ouvert **0,621**), syntagmes exacts **0,194**, **par tête 0,560**, pragmatique
> **1,0/1,0/0,994/0,889**, cascade **67,1 %**, **attachement par tête couverture 1,0 / top-1 0,957 / top-k 1,0** (span 0,323/0,338), hasard 0,015 ; **36 cibles ambiguës annotées en double lecture**. ⚠️ **le vrai modèle
> neuronal est refusé** (`llama-cli` local) ; la cascade est mesurée avec le **mock de contrat**.
>
> **Dispositif** : [`gold.py`](../tools/tests/linguistique/gold.py) (20 réels),
> [`gold_synthetique.py`](../tools/tests/linguistique/gold_synthetique.py) (160 synthétiques),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py), JSON
> [`pensee-gold-linguistique.json`](pensee-gold-linguistique.json).

## 1. Le gold étendu

- **20 phrases réelles** (14 françaises, 6 anglaises), écrites après le bloc, avec PO
… [4244 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,80p reports/rapport-pensee-attachement-cible.md", "description": "Read prior attachment-target report"}`

  ```
# B13 — l'attachement ciblé : l'exact passe de 0,6438 à 0,8082

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
> **173/173 portes** : la nature de la cible dépend du **type du segment**, et la règle le dit
> maintenant : pour un **REL/SUB**, l'attachement est l'**antécédent** (la tête du GN à gauche,
> élision séparée : `L'homme` → `homme`) ; pour un **GP**, c'est le **verbe du GV** le plus
> proche. Sur les 146 segments au bon span : **exact 94 → 118** (0,6438 → **0,8082**), top1
> 0,8356, top-k 0,9041. Par convention : **verbes 48/51 (0,9412)**, **noms 70/95 (0,7368)**.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_tete_nom`),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-attachement-cible.json`](pensee-attachement-cible.json).

## 1. Avant / après (146 segments au bon span)

| mesure | avant | **attachement ciblé** | écart |
|---|---:|---:|---:|
| top1 | 114 (0,7808) | **122 (0,8356)** | +8 |
| top-k | 132 (0,9041) | 132 (0,9041) | 0 |
| **exact** | **94 (0,6438)** | **118 (0,8082)** | **+24** |
| **verbes**
… [2071 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,60p reports/rapport-pensee-cible-proximite.md", "description": "Read prior proximity-target report"}`

  ```
# B13 — la cible par proximité : l'exact passe de 0,0042 à 0,0544 (×13)

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-04 · **Verdict** : ✅
> **164/164 portes** : la règle « la cible d'un segment est le **verbe du GV le plus proche** »
> remplit les `cible` que le générateur S laissait vides. Sur le même gold que T153 (612 phrases,
> **239 cibles**), l'attachement passe de **top1 82 (0,3431)** à **95 (0,3975)**, et surtout de
> **exact 1 (0,0042)** à **13 (0,0544)** — **×13**. La tête fait **94/145 (0,6483)** contre 81
> (0,5586).
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_cible_proche`),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-cible-proximite.json`](pensee-cible-proximite.json).

## 1. Avant / après (même gold, 612 phrases, 239 cibles)

| mesure | T153 (avant) | **règle de proximité** | écart |
|---|---:|---:|---:|
| top1 | 82 (0,3431) | **95 (0,3975)** | +13 (+0,0544) |
| top-k | 78 (0,3264) | 78 (0,3264) | 0 |
| **exact** | **1 (0,0042)** | **13 (0,0544)** | **+12 (×13)** |
| tête top1 | 81/145 (0,5586) | **94/145 (0,6
… [1907 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -c \"\nimport json; d=json.load(open('reports/pensee-attachement-cible.json')); print(json.dumps(d,ensure_ascii=False,indent=1)[:1200])\"", "description": "Read prior attachment JSON numbers"}`

  ```
{
 "date": "2026-11-05",
 "ligne": "B13",
 "portes": "173/173",
 "gold": 612,
 "cibles": 239,
 "labels": 146,
 "avant": {
  "exact": 94,
  "exact_span": 0.6438,
  "top1": 114,
  "top1_span": 0.7808,
  "verbe": 0.7255,
  "nom": 0.6
 },
 "apres": {
  "exact": 118,
  "exact_span": 0.8082,
  "top1": 122,
  "top1_span": 0.8356,
  "verbe": 0.9412,
  "nom": 0.7368
 },
 "rendement": {
  "top1": 0.5105,
  "topk": 0.5523,
  "exact": 0.4937
 },
 "regle": "REL/SUB → antécédent (tête du GN à gauche, élision séparée) ; GP → verbe du GV",
 "limites": [
  "28 échecs non qualifiés",
  "convention non documentée",
  "top-k lenient",
  "gold 612"
 ]
}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -5 -- tools/bloc_linguistique.py && git status --short tools/bloc_linguistique.py tools/tests/linguistique/ | head", "description": "Check recent history of bloc and gold"}`

  ```
a408a909 B13 — LE LEXIQUE ÉLARGI (PARTICIPES IRRÉGULIERS ET EN -É) : EXACT 0,8082 → 0,8483 ; 174/174
23853cb7 B13 — L'ATTACHEMENT CIBLÉ : REL → ANTÉCÉDENT, GP → VERBE ; EXACT 0,6438 → 0,8082, VERBES 0,9412 ; 173/173
d8edd1d9 B13 — LE CLASSEMENT : EXACT 0,2260 → 0,6438 (CIBLE RÉDUITE À SA TÊTE) ; LE GOLD MÊLE DEUX CONVENTIONS (51 VERBES, 95 NOMS) ; 171/171
13e8bb2d B13 — LES SPANS PERDUS : 48 REL, 33 SUB, 12 GP (81 CHEZ S) ; LE GP EST BORNÉ AU VERBE ; 169/169
d400e188 B13 — LE LEXIQUE VERBAL : EXACT 0,0962 → 0,1381, TÊTE 0,9034 ; 168/168
  ```

### 🤖 Assistant

⏵ Vérification des chiffres courants via `evaluer_gold.py`

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 300 python3 tools/tests/linguistique/evaluer_gold.py 2>&1 | head -30", "description": "Run evaluer_gold current output"}`

  ```
{
 "parallele": {
  "all": {
   "bloc": "parallele",
   "phrases": 612,
   "pos": {
    "exactitude": 0.7455,
    "exactitude_ferme": 0.8984,
    "exactitude_ouvert": 0.6007,
    "tokens": 3179,
    "confusions": {
     "ADJ": {
      "ADJ": 50,
      "NOUN": 80,
      "VERB": 4
     },
     "ADV": {
      "ADV": 117,
      "NOUN": 21,
      "PREP": 1,
      "ADJ": 1,
      "?": 1
     },
     "AUX": {
      "PREP": 4,
      "AUX": 118,
      "?": 3,
      "NOUN": 3
     },
     "CONJ": {
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log -1 --oneline && git diff HEAD --stat -- tools/bloc_linguistique.py tools/tests/linguistique/gold.json tools/tests/linguistique/gold_reel.json && git status --short tools/tests/linguistique/ | head", "description": "Check HEAD … [33 caractères tronqués]`

  ```
e1171032 PILOTAGE — PROTOCOLE D'INTÉGRATION DES SOUS-AGENTS (REJOUER, REJETER, COMMITTER VÉRIFIÉ) ; § 9
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 300 python3 tools/tests/linguistique/evaluer_gold.py 2>&1 | grep -o '\"attachement[^}]*}' | head -20", "description": "Extract attachment numbers from eval"}`

  ```
(no output)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -4 -- tools/tests/linguistique/gold.json tools/tests/linguistique/gold_reel.json tools/tests/linguistique/gold_synthetique.json", "description": "Check gold file history"}`

  ```
702b368c B13 — LES VRAIS ABSENTS : 5 PHRASES, 0 LIEN, GOLD 432 ; 140/140
651c1fc0 B13 — LE LIEN AUTOMATIQUE RÉPARÉ : 5/5 APRÈS RÉORDONNANCEMENT ET REPLI PRON/NOUN ; 136/136
297c4f17 B13 — LA RÉPONSE CONTEXTUELLE : 5/5, LA PHRASE PRÉCÉDENTE TRANCHE ; 134/134
26e4df27 B13 — LES QUESTIONS PIÈGES : 29/34, LE SI EST UNE CONVENTION ; 132/132
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline a408a909..HEAD -- tools/bloc_linguistique.py tools/tests/linguistique/ | head -20 && echo '--- files changed since a408a909 ---' && git diff --stat a408a909..HEAD -- tools/bloc_linguistique.py tools/tests/linguistiq … [71 caractères tronqués]`

  ```
0ddd4fb9 B13 — LA CONVENTION DES CIBLES EST DOCUMENTÉE DANS LE GOLD (REL/SUB → ANTÉCÉDENT, GP → VERBE) ; 177/177
e223a98d B13 — LE TOP-K STRICT : 0,6069 EN ÉGALITÉ EXACTE, PAS 0,9241 (SOUS-CHAÎNES) ; 176/176
--- files changed since a408a909 ---
 tools/tests/linguistique/evaluer_gold.py |  7 +++++++
 tools/tests/linguistique/gold_reel.py    | 22 ++++++++++++++++++++++
 2 files changed, 29 insertions(+)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show --stat 0ddd4fb9 | head -20 && git show 0ddd4fb9 -- tools/tests/linguistique/gold_reel.py | head -60", "description": "Inspect convention commit changes"}`

  ```
commit 0ddd4fb943706e732951dc86b6ba78cb08e3ef31
Author: Stéphane <stephane@localhost>
Date:   Thu Nov 5 11:10:13 2026 -0500

    B13 — LA CONVENTION DES CIBLES EST DOCUMENTÉE DANS LE GOLD (REL/SUB → ANTÉCÉDENT, GP → VERBE) ; 177/177

 docs/implantation/moteur-de-pensee.md              |  5 +-
 docs/pilotage/chantiers.md                         |  8 +-
 docs/pilotage/en-cours.md                          | 12 +--
 docs/pilotage/roadmap.md                           |  6 +-
 journal/2026-11-05/README.md                       |  7 +-
 journal/2026-11-05/attention.md                    |  2 +-
 journal/2026-11-05/distribue.md                    |  2 +-
 journal/2026-11-05/docs.md                         |  7 +-
 journal/2026-11-05/memoire.md                      |  2 +-
 journal/2026-11-05/mesures.md                      |  2 +-
 journal/2026-11-05/modele.md                       |  2 +-
 journal/2026-11-05/moteur.md                       |  2 +-
 journal/2026-11-05/portes.md                       |  2 +-
 journal/README.md                                  |  2 +-
commit 0ddd4fb943706e732951dc86b6ba78cb08e3ef31
Author: Stéphane <stephane@localhost>
Date:   Thu Nov 5 11:10:13 2026 -0500


… [1831 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Script final de diagnostic : catégories exclusives, gains simulés, contrôles

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\n# Diagnostic complet top-k strict — lecture seule, aucun fichier écrit.\nimport sys, re, json, random, collections\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique … [4211 caractères tronqués]`

  ```
classes: {'C5_GN_gauche_non_candidat': 2, 'C1_S_non_reduit_nom': 43, 'C3_S_non_reduit_attribut': 2, 'C4_verbe_en_hors_lexique': 8, 'C7_enclitique': 1, 'C8_gv_S_mal_delimite': 1}
types: {'GP': 29, 'REL': 26, 'SUB': 2}
sources: {'hand': 3, 'reel': 43, 'synthetique': 11}
top1 deja juste parmi les 57: 41
sous-chaine: 46
absent: 11
C5_GN_gauche_non_candidat|hand|g002|GP|de la voisine|chat||GP|absent
C1_S_non_reduit_nom|hand|g011|REL|que j'ai lu|livre|livre|« que j'ai lu » → Le livre;est|sub
C3_S_non_reduit_attribut|hand|g012|GP|à manger|prêt|manger|« à manger » → Le canard;« à manger » → est prêt;manger;est|sub
C1_S_non_reduit_nom|reel|r014|REL|que j'ai lu|livre|livre|« que j'ai lu » → Le livre;est|sub
C1_S_non_reduit_nom|reel|r015|REL|dont elle parle|film|film|« dont elle parle » → Le film;sorti|sub
C3_S_non_reduit_attribut|reel|r018|GP|à manger|prête|manger|« à manger » → La souris;« à manger » → est prête;manger;est|sub
C1_S_non_reduit_nom|reel|r047|GP|dans le jardin|poussent|poussent|« dans le jardin » → Les fleurs poussent|sub
C1_S_non_reduit_nom|reel|r054|REL|que tu lis|livre|livre|« que tu lis » → Le livre;est|sub
C1_S_non_reduit_nom|reel|r055|REL|où nous vivons|ville|ville|« où 
… [4922 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification des catégories corrigées et des contrôles négatifs

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, re, collections\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl\nfrom evaluer_gold import charger\nph=charger()\n\ndef head(nom):\n    if '→' no … [5048 caractères tronqués]`

  ```
Counter({'C1': 26, 'C2': 17, 'C4': 8, 'C3': 2, 'C5': 1, 'C7': 1, 'C8': 1, 'C6': 1})
AUTRE: []
F1: 45 Counter({'C1': 26, 'C2': 17, 'C3': 2})
F2 topk: 96 fixes: 8 cause: Counter({'C4': 8})
top1 baseline: 123 apres F2: 131
F2 controle 8 verbes non pertinents fixes: 0
F1 controle premier token: 0
F3 fixes: 12 ['g002', 'r080', 'r108', 'r120', 'r156', 'r166', 'r169', 'r177', 'r180', 'r230', 'r309', 's041']
F3 controle premier mot: 0
oracle (cible ajoutee): 57
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl\nfor w in ['fly','climbs','flows','swims','get','smiles','wait','belongs','marche','appelle','vie … [126 caractères tronqués]`

  ```
fly False False
climbs False False
flows False False
swims False False
get False False
smiles False False
wait False False
belongs False False
marche False False
appelle False False
viendra False False
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, re\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl\nfrom evaluer_gold import charger\nph={p['id']:p for p in charger()}\np=ph['r080']; print(rep … [192 caractères tronqués]`

  ```
'The birds fly over the lake.'
'The' False
'birds' False
'fly' False
'over' False
'the' False
'lake' False
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, re\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl\nfrom evaluer_gold import charger\nph={p['id']:p for p in charger()}\nh=bl.Heuristique()\nfor … [1010 caractères tronqués]`

  ```
r080 cible fly cands ['GP', 'lake'] extra ['fly'] hit True
g002 cible chat cands ['GP'] extra ['chat', 'dort'] hit True
r230 cible appelle cands ['structure la plus proche', 'appelle-moi'] extra ['arrives'] hit False
r309 cible viendra cands ['structure la plus proche', 'Peut-être'] extra ['Peut'] hit False
s041 cible marche cands ['GP'] extra ['marche'] hit True
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"VERBES_CONNUS\" tools/bloc_linguistique.py", "description": "Find all mutations of VERBES_CONNUS"}`

  ```
374:VERBES_CONNUS = set("""
433:    if n in VERBES_CONNUS:
438:        if n.endswith(suf) and n[:-len(suf)] in VERBES_CONNUS:
442:        if n.endswith(suf) and (n[:-len(suf)] + "er") in VERBES_CONNUS:
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl\nprint('avant', bl._est_verbe('fly'), len(bl.VERBES_CONNUS))\nh=bl.Heuristique(); a=h.analyser('T … [244 caractères tronqués]`

  ```
avant False 522
apres False 522 False
[]
  ```

### 🤖 Assistant

⏵ Génération du JSON de diagnostic (57 segments qualifiés)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && test ! -e reports/pensee-topk-diagnostic.json && echo \"JSON absent (ok)\" && test ! -e reports/rapport-topk-diagnostic.md && echo \"MD absent (ok)\"", "description": "Verify deliverable filenames are new"}`

  ```
JSON absent (ok)
MD absent (ok)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\n# Diagnostic top-k strict de l'attachement — lecture seule du code, écrit le JSON de fiche.\nimport sys, re, json, pathlib, collections\nsys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/tests/linguistique')\ni … [16009 caractères tronqués]`

  ```
JSON écrit: /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-topk-diagnostic.json
mesure: {"phrases": 612, "cibles_gold": 239, "segments_span_predit": 145, "topk_sous_chaine": 134, "topk_exact": 88, "echecs_stricts": 57, "top1_exact": 123, "taux_span": {"topk_sous_chaine": 0.9241, "topk_exact": 0.6069, "top1_exact": 0.8483}, "rendement_239": {"topk_sous_chaine": 0.5607, "topk_exact": 0.3682}}
causes: {'C1': 26, 'C2': 17, 'C3': 2, 'C4': 8, 'C5': 1, 'C6': 1, 'C7': 1, 'C8': 1}
F1: 45 F2: 8 F3: 4 F3 isolé: 29 contrôles: 0 57 0
top1: 123 -> 131
  ```

### 🤖 Assistant

⏵ Correction des compteurs de contrôle et du gain isolé F3

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, re, json, pathlib, collections\nsys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/tests/linguistique')\nimport bloc_linguistique as bl\nfrom evaluer_gold import charger\nRACINE = pathlib.Path('.').r … [14476 caractères tronqués]`

  ```
JSON écrit: /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-topk-diagnostic.json 29506 octets
mesure: {"phrases": 612, "cibles_gold": 239, "segments_span_predit": 145, "topk_sous_chaine": 134, "topk_exact": 88, "echecs_stricts": 57, "top1_exact": 123, "taux_span": {"topk_sous_chaine": 0.9241, "topk_exact": 0.6069, "top1_exact": 0.8483}, "rendement_239": {"topk_sous_chaine": 0.5607, "topk_exact": 0.3682}}
causes: {'C1': 26, 'C2': 17, 'C3': 2, 'C4': 8, 'C5': 1, 'C6': 1, 'C7': 1, 'C8': 1}
F1 45 F2 8 F3 4 F3 isole 29
controles: 0 / 45 | 0 / 8 | 0 / 4
F2 top1: 123 -> 131
F3 fixes ids: ['g002', 'r230', 'r309', 's041']
F3 isole ids: ['g002', 'r047', 'r057', 'r080', 'r088', 'r100', 'r108', 'r120', 'r126', 'r139', 'r150', 'r156', 'r166', 'r169', 'r177', 'r180', 'r230', 'r309', 's041', 's045', 's047', 's058', 's064', 's108', 's109', 's120', 's122', 's144', 's150']
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-topk-diagnostic.json'))\nprint(list(d))\nprint('segments:',len(d['segments']),'causes:',len(d['causes']),'correctifs:',len(d['correctifs']))\nprint(json.dumps(d['causes' … [457 caractères tronqués]`

  ```
['date', 'ligne', 'titre', 'verdict', 'non_applique', 'gold', 'mesure', 'causes', 'correctifs', 'controle_negatif', 'limites', 'segments']
segments: 57 causes: 8 correctifs: 3
[
 {
  "code": "C1",
  "libelle": "candidat S non réduit à sa tête — cible nominale",
  "raison": "La cible est un nom (antécédent REL) présent seulement dans la chaîne de présentation « « segment » → Le X » ; la liste des candidats garde la chaîne entière, pas `X`.",
  "effectif": 26,
  "dont_sous_chaine": 26,
  "types": {
   "REL": 26
  },
  "sources": {
   "hand": 1,
   "reel": 25
  },
  "top1_deja_juste": 26,
  "correctif": "F1",
  "exemples": [
   "g011 · REL « que j'ai lu » → livre",
   "r014 · REL « que j'ai lu » → livre",
   "r015 · REL « dont elle parle » → film"
  ]
 },
 {
  "code": "C2",
  "libelle": "candidat S non réduit à sa tête — cible verbale",
  "raison": "La cible est le verbe du GV, présent seulement dans « « segment » → GN + V » ; la liste garde la phrase entière, pas `V`.",
  "effectif": 17,
  "dont_sous_chaine": 17,
  "types": {
   "GP": 17
  },
  "sources": {
   "reel": 7,
   "synthetique": 10
  },
  "top1_deja_juste": 15,
  "correctif": "F1",
  "exemples": [
   "r047 · GP « dans le ja
… [2389 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Extraction des identifiants par cause pour l'annexe de la fiche

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json, collections\nd=json.load(open('reports/pensee-topk-diagnostic.json'))\ng=collections.defaultdict(list)\nfor s in d['segments']: g[s['cause']].append(s['id'])\nfor c in sorted(g): print(c, len(g[c]), ',  … [264 caractères tronqués]`

  ```
C1 26 g011, r014, r015, r054, r055, r094, r095, r201, r203, r209, r213, r221, r226, r228, r231, r233, r235, r253, r257, r259, r261, r263, r265, r267, r269, r275
C2 17 r047, r057, r088, r100, r126, r139, r150, s045, s047, s058, s064, s108, s109, s120, s122, s144, s150
C3 2 g012, r018
C4 8 r080, r108, r120, r156, r166, r169, r177, r180
C5 1 g002
C6 1 s041
C7 1 r230
C8 1 r309
total 57
C1 26 {'REL': 26} {'hand': 1, 'reel': 25} top1 26
C2 17 {'GP': 17} {'reel': 7, 'synthetique': 10} top1 15
C3 2 {'GP': 2} {'hand': 1, 'reel': 1} top1 0
C4 8 {'GP': 8} {'reel': 8} top1 0
C5 1 {'GP': 1} {'hand': 1} top1 0
C6 1 {'GP': 1} {'synthetique': 1} top1 0
C7 1 {'SUB': 1} {'reel': 1} top1 0
C8 1 {'SUB': 1} {'reel': 1} top1 0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"^VERBES\\s*=\\|^ADJECTIFS\\s*=\\|^POS_FERME\" tools/bloc_linguistique.py && sed -n '/^VERBES = /,/^}/p' tools/bloc_linguistique.py | head -20", "description": "Inspect VERBES POS lexicons"}`

  ```
298:POS_FERME = {
319:VERBES = {
340:ADJECTIFS = {
VERBES = {
    "fr": set("dort dorment dormait mange mangeons mangent mangeait court courent courait vu voir vois "
              "voit voyons voyez voient dit disons dites disent viendrait viens vient venons venez "
              "viennent aboie aboient joue jouons jouent jouait lit lisons lisez lisent pars partons "
              "partez partent fini finis finit finissons finissez finissent arrive arrives arrivez "
              "arrivent pleut pleuvoir habite habites habitent parle parlons parlez parlent explique "
              "expliquons expliquez expliquent souffle soufflent chante chantent chantes peut peux "
              "pouvons pouvez peuvent doit devons devez doivent pourrait pourrais pourrions pourriez "
              "pourraient devrait devrais voudrais voudrait veux veut voulons voulez veulent prend "
              "prends prenons prenez prennent donne donnes donnons donnez donnent trouve trouves "
              "trouvons trouvez trouvent cherche cherches cherchons cherchez cherchent regarde "
              "regardes regardons regardez regardent écoute écoutes écoutons écoutez écoutent ouvre "
              "ouvres 
… [725 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Rédaction de la fiche `reports/rapport-topk-diagnostic.md`

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-topk-diagnostic.md", "content": "# B13 — le top-k strict de l'attachement : 57 échecs, dont 45 d'emballage\n\n> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 ·\n> **Verdict** : ✅ **les … [12841 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-topk-diagnostic.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

### 🤖 Assistant

⏵ Validation des deux livrables, liens et intégrité Git

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json, pathlib, re\nd = json.load(open('reports/pensee-topk-diagnostic.json'))\nprint('JSON valide, clés:', list(d))\nprint('segments:', len(d['segments']), '| causes:', sum(c['effectif'] for c in d['causes']) … [638 caractères tronqués]`

  ```
JSON valide, clés: ['date', 'ligne', 'titre', 'verdict', 'non_applique', 'gold', 'mesure', 'causes', 'correctifs', 'controle_negatif', 'limites', 'segments']
segments: 57 | causes: 57
liens: ['../tools/bloc_linguistique.py', '../tools/tests/linguistique/evaluer_gold.py', 'pensee-topk-diagnostic.json', '../tools/bloc_linguistique.py', 'pensee-topk-diagnostic.json', 'pensee-topk-diagnostic.json', '../tools/bloc_linguistique.py', '../tools/tests/linguistique/evaluer_gold.py']
  ../tools/bloc_linguistique.py -> True
  ../tools/tests/linguistique/evaluer_gold.py -> True
  pensee-topk-diagnostic.json -> True
  ../tools/bloc_linguistique.py -> True
  pensee-topk-diagnostic.json -> True
  pensee-topk-diagnostic.json -> True
  ../tools/bloc_linguistique.py -> True
  ../tools/tests/linguistique/evaluer_gold.py -> True
mots MD: 2228
taille JSON: 29506
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short | grep -E \"reports/(rapport-topk|pensee-topk)\" && git status --short | grep -vE \"journal/\" | head -20", "description": "Check only new reports changed"}`

  ```
?? reports/pensee-topk-diagnostic.json
?? reports/rapport-topk-diagnostic.md
 M reports/pensee-quatre-modes.json
 M reports/pensee-spans.json
 M reports/rapport-pensee-spans.md
 m tools/structures
?? reports/pensee-audit-attachement.json
?? reports/pensee-topk-diagnostic.json
?? reports/rapport-audit-attachement.md
?? reports/rapport-s-paragraphes.md
?? reports/rapport-topk-diagnostic.md
?? tools/tests/linguistique/classement_cible.py
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-topk-diagnostic.md", "limit": 80}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-topk-diagnostic.md</path>
<type>file</type>
<content>
1: # B13 — le top-k strict de l'attachement : 57 échecs, dont 45 d'emballage
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 ·
4: > **Verdict** : ✅ **les 57 échecs du top-k strict sont qualifiés** (0 « autre »). Sur les
5: > **145 segments gold dont le span est prédit**, la cible est dans les candidats **134 fois en
6: > sous-chaîne** (0,9241) mais **88 fois en égalité exacte** (0,6069) : **57 échecs**. **45** sont
7: > des **candidats du générateur S non réduits à leur tête** — la cible est déjà dans la chaîne
8: > « « segment » → … », il suffit d'en extraire la tête ; **8** sont des **verbes anglais hors
9: > lexique** ; **4** sont de la **couverture locale** (génitif, enclitique, GV mal délimité).
10: > Le **top-1 est déjà juste 41 fois sur 57** : le top-k strict mesure surtout l'**emballage** des
11: > candidats, pas le choix de la cible. Trois correctifs **simulés, non appliqués**, couvrent
12: > **45 + 8 + 4 = 57** — borne haute, mesurée sur le même gold.
13: >
14: > **Dispositif** : [`bloc_linguistique.py`](..
… [4797 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"173\\|portes\" reports/rapport-topk-diagnostic.md", "description": "Locate gates wording in report"}`

  ```
166:  gains sont des simulations, pas un diff. Les 173+ portes restent à rejouer après application.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-topk-diagnostic.md", "old_string": "  gains sont des simulations, pas un diff. Les 173+ portes restent à rejouer après application.", "new_string": "  gains sont des simulations, pas un diff. Les portes restent à rejouer  … [20 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-topk-diagnostic.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-topk-diagnostic.md", "offset": 80, "limit": 120}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-topk-diagnostic.md</path>
<type>file</type>
<content>
80: - **C7 (1)** : `r230` « Quand tu arrives, appelle-moi » — la cible est `appelle`, le candidat
81:   est le token entier `appelle-moi` : le trait d'union n'est pas découpé.
82: - **C8 (1)** : `r309` « Peut-être qu'il viendra » — le S prend `Peut-être` pour un GV et
83:   `viendra` n'est ni reconnu ni candidat.
84: 
85: ## 3. Trois correctifs, ordonnés par gain
86: 
87: Tous sont **simulés** (greffe de lexique et ajout de candidats en mémoire), **aucun n'est
88: appliqué** : le code du dépôt est inchangé. La colonne « gain » est **incrémentale** dans
89: l'ordre proposé. Fichier commun : [`tools/bloc_linguistique.py`](../tools/bloc_linguistique.py).
90: 
91: | ordre | correctif | fonction à modifier | gain top-k strict | top-1 |
92: |---|---|---|---:|---:|
93: | 1 | **F1 — réduire chaque candidat S à sa tête** | `Heuristique.analyser`, branche « 5. syntagmes » (construction de `noms` l. 826 et de `candidats` l. 858/874/892) ; helper existant `_tete_nom` (l. 616) | **+45** | 0 |
94: | 2 | **F2 — compléter le lexique verbal anglais** | `_est_verbe` (l. 428) vi
… [6927 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Enrichissement du JSON (raison détaillée par segment) et retouches de la fiche

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json, pathlib\np = pathlib.Path('reports/pensee-topk-diagnostic.json')\nd = json.loads(p.read_text(encoding='utf-8'))\nraisons = {c['code']: c['raison'] for c in d['causes']}\ncorr = {c['code']: c['correctif' … [723 caractères tronqués]`

  ```
ok 41334 octets; 57 segments
{'id': 'g002', 'source': 'hand', 'langue': 'fr', 'type': 'GP', 'segment': 'de la voisine', 'cible_gold': 'chat', 'cible_choisie': '', 'candidats': ['GP'], 'sous_chaine': False, 'cause': 'C5', 'raison': 'GP génitif — tête du GN à gauche jamais candidate', 'raison_detail': "Pour un génitif (`de la voisine` → `chat`), la cible est le nom complété ; le GV est avalé par le GP dans le S et aucun candidat nominal de gauche n'est produit.", 'correctif': 'F3'}
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-topk-diagnostic.md", "new_string": "**F3 — 4 segments (C5, C6, C7, C8).** Quatre ajouts coordonnés à la source de candidats :", "old_string": "**F3 — 4 segments (C5, C6, C7, C8).** Trois ajouts coordonnés à la source de c … [12 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-topk-diagnostic.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-topk-diagnostic.md", "new_string": "\\* conditionnel : le top-1 de F3 n'est pas simulé ; seule la colonne top-k est mesurée.", "old_string": "\\* conditionnel ; seule la colonne top-k est mesurée pour F3."}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-topk-diagnostic.md has been updated successfully.
  ```

### 🤖 Assistant

⏵ Contrôle final des chiffres et de la cohérence fiche/JSON

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, json\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl\nfrom evaluer_gold import charger\nph=charger(); h=bl.Heuristique()\nn_tot=n_lab=n_sub=n_ex … [1350 caractères tronqués]`

  ```
cibles 239 labels 145 sous-chaine 134 exact 88 echecs 57
JSON mesure: 145 134 88 57
cumuls: 88 133 141 145 | taux: 0.9172 0.9724
MD présent: True
--- git status (mes fichiers) ---
?? reports/pensee-topk-diagnostic.json
?? reports/rapport-topk-diagnostic.md
  ```

### 🤖 Assistant

⏵ Envoi du résultat au parent et résumé final

- **send_message** `{"agent_id": "e181ce02-cd50-488a-a6be-e84b79d40dcc", "message": "DIAGNOSTIC TOP-K STRICT TERMINÉ — 57/57 échecs qualifiés, 0 « autre ». Deux fichiers neufs seulement, aucun code modifié, aucun commit : `reports/rapport-topk-diagnostic.md` et `reports/pensee-topk-diagnostic.json` (57 lignes détaillée … [2974 caractères tronqués]`

  ```
message delivered to agent e181ce02-cd50-488a-a6be-e84b79d40dcc
  ```

### 🤖 Assistant

⏵ Diagnostic livré : 57 échecs qualifiés, 3 correctifs chiffrés

## Verdict

Les **57 échecs du top-k strict** sont tous qualifiés (0 « autre »), sur **145 segments au bon span** : cible en sous-chaîne **134** (0,9241), en égalité exacte **88** (0,6069). Le **top-1 est déjà juste 123/145** (0,8483), et **41 des 57 échecs ont déjà la bonne cible choisie** : le top-k strict mesure surtout la **forme des candidats**, pas la règle d'attachement.

## Effectifs par cause

| # | Cause | Eff. | Dont sous-chaîne |
|---|---|---:|---:|
| C1 | Candidat S non réduit — cible nominale REL (« … → Le livre ») | 26 | 26 |
| C2 | Candidat S non réduit — cible verbale GP (« … → Les fleurs poussent ») | 17 | 17 |
| C3 | Candidat S non réduit — cible attribut (« … → est prêt ») | 2 | 2 |
| C4 | Verbe anglais hors lexique (`fly`, `climbs`, `flows`, `swims`, `get`, `smiles`, `wait`, `belongs`) | 8 | 0 |
| C5 | GP génitif — tête du GN à gauche jamais candidate | 1 | 0 |
| C6 | Verbe français hors lexique, aucun GV (`marche`) | 1 | 0 |
| C7 | Candidat tokenisé avec enclitique (`appelle-moi`) | 1 | 1 |
| C8 | GV du S mal délimité (`Peut-être`, `viendra`) | 1 | 0 |
| | **Total** | **57** | **46** |

Types : REL 26, GP 29, SUB 2 — sources : hand 3, reel 43, synthétique 11.

## 3 correctifs (simulés, non appliqués)

1. **F1 — réduire chaque candidat S à sa tête : +45 segments.** `tools/bloc_linguistique.py`, `Heuristique.analyser` (branche 5. syntagmes, construction de `noms` l. 826 et `candidats` l. 858/874/892) + helper existant `_tete_nom` (l. 616). Réduit `« … → Le livre »` à `livre`, `« … → Les fleurs poussent »` à `poussent`. Top-1 inchangé.
2. **F2 — compléter le lexique verbal anglais : +8 segments.** `_est_verbe` (l. 428) via `VERBES_CONNUS` (l. 374), et `VERBES["en"]` (l. 319) pour le POS. Ajoute `fly, climb, flow, swim, get, smile, wait, belong` + flexions. **+8 top-1, 0 régression.**
3. **F3 — repli par tokens : +4 segments.** `Heuristique._verbes_proches` (l. 670) et `_cible_proche` (l. 643) : tête du GN à gauche pour un GP, verbes reconnus dans une fenêtre, découpe des enclitiques, formes manquantes (`marche`, `appelle`, `viendra`). Top-1 +4 conditionnel.

**Cumul simulé** : 88 → 133 (0,9172) → 141 (0,9724) → **145/145 (1,0)**. Top-1 : 123 → 123 → 131 → 135\*. Ces gains sont des **bornes hautes sur le même gold**, pas une généralisation.

## Contrôle négatif et limites

- F1 avec le **premier** token au lieu de la tête : **0/45** ; F2 avec 8 verbes anglais non pertinents : **0/8** ; F3 avec le premier mot de la phrase : **0/4** ; oracle « ajouter la cible du gold » : 57/57 (plafond trivial).
- Limites : correctifs déduits du même gold (F3(d) et F2 les plus exposés au sur-apprentissage) ; F1 ne répare pas le top-1 de s108/s122/g012/r018 ; couplage au format d'affichage `« … » → …` du S ; F3 isolé vaut 29 mais 25 recouvrent F1/F2 ; rendement global plafonné à 145/239 = 0,6067 par la couverture de span ; aucune porte rejouée (code inchangé).

## Fichiers

- `reports/rapport-topk-diagnostic.md` — fiche (verdict, tableau des causes, 3 correctifs, contrôle négatif, limites, annexe des 57 ids).
- `reports/pensee-topk-diagnostic.json` — 57 lignes détaillées (type, segment, cible gold, cible choisie, candidats, cause, raison) + mesure, correctifs, contrôles.

Aucun fichier existant modifié, aucun commit, aucun fichier temporaire dans le dépôt ; le script de diagnostic a été exécuté par heredoc en lecture seule.

