# Session DSH — relecture

- identifiant : `d300542e-6e9d-47ac-875b-b44a192eec35`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-05 14:22:47
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : mesurer le **repli « cible vide »** de l'attachement et deux autres retouches déterministes, sans modifier le code du dépôt.

Contexte : `tools/bloc_linguistique.py` (`Heuristique`, `_cible_proche`, `_tete_nom`, `_verbe_dans`, `_tete_texte`), `tools/tests/linguistique/evaluer_gold.py` (`charger`, `evaluer_bloc`). A3 (fiche `reports/rapport-classement-appris.md`) recommande trois retouches déterministes : (a) repli quand la cible est vide (cas `g002`, `s041`) ; (b) préférer un verbe à un nom proche (cas `g012`, `r018`, `s108`, `s122`) ; (c) cas de la complétive en tête (`r309`).

À faire :
1. Compte et liste les segments dont `meta.attachement.cible` est vide ou absente (sur les 145 au bon span et sur les 239 cibles), et ceux où la cible est un nom alors que le gold attend un verbe.
2. **Simule** chaque retouche sur une copie locale (par exemple en sous-classant `Heuristique` ou en recopiant la logique dans un module neuf `tools/tests/linguistique/replis_cible.py`) et mesure : exact, top1, régressions. Ne modifie pas `tools/bloc_linguistique.py`.
3. Chiffre chaque retouche : gain, régressions, gain net ; dis laquelle vaut la peine d'être intégrée (et laquelle non).
4. Écris **uniquement** trois fichiers neufs : `tools/tests/linguistique/replis_cible.py` (le prototype, non importé par ailleurs), `reports/rapport-replis-cible.md` (fiche : protocole, tableau par retouche, contrôles négatifs, limites, recommandation) et `reports/pensee-replis-cible.json`.

Règles strictes : ne committe rien ; ne modifie aucun fichier existant ; n'écris pas dans `docs/pilotage/`, `AGENTS.md`, `journal/`, `tools/structures/`, `data/`, `tools/entrainer_native.py`, `tools/native_model.py`. Rends un résumé avec le gain net de chaque retouche et ta recommandation.
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

⏵ Cartographie du dépôt et lecture des fichiers du protocole

- **bash** `{"command": "git status --porcelain; git branch --show-current; ls", "description": "Show git state and repo root", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
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
MM journal/README.md
MM journal/THEMES.md
MM journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/digest.md
MM journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/rapport.md
MM journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/digest.md
MM journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/rapport.md
D  journal/sessions/53bc3288-f2c1-4a7d-b1db-88d794074f70/digest.md
D  journal/sessions/53bc3288-f2c1-4a7d-b1db-88d794074f70/rapport.md
D  journal/sessions/63d4c619-63e8-41b9-a183-5c6f1ac05a21/digest.md
D  journal/sessions/63d4c619-63e8-41b9-a183-5c6f1ac05a21/rapport.md
D  journal/sessions/65495a29-10c0-4571-96be-e7729f1efebf/digest.md
D  journal/sessions/65495a29-10c0-4571-96be-e7729f1efebf/rapport.md
MM journal/sessions/MANIFEST.md
D  journal/sessions/a8035275-c7b9-4713-a6ab-7b859cd72306/digest.md
D  journal/sessions/a8035275-c7b9-4713-a6ab-7b859cd72306/rapp
… [1913 caractères tronqués]
  ```

- **bash** `{"command": "wc -l tools/bloc_linguistique.py tools/tests/linguistique/evaluer_gold.py reports/rapport-classement-appris.md 2>/dev/null", "description": "Line counts of key files", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
1929 tools/bloc_linguistique.py
   287 tools/tests/linguistique/evaluer_gold.py
   111 reports/rapport-classement-appris.md
  2327 total
  ```

### 🤖 Assistant

⏵ Lecture de la fiche A3, de l'évaluateur gold et du bloc linguistique

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-classement-appris.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/evaluer_gold.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-classement-appris.md</path>
<type>file</type>
<content>
1: # B13 — classement appris des candidats d'attachement : 142/145, mais la règle live est déjà à 137
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, attachement) · **Date** : 2026-11-05 · **Verdict** : ❌ **ne pas intégrer le classement appris en l'état** ; le signal utile est le **vivier ordonné** (rang 0 : 139/145), à tester.
4: >
5: > **142/145 (0,9793)** hors-pli contre **137/145 (0,9448)** pour la règle live (empreinte `6e843018`, 13:51) : **+5**, McNemar 7/2, **p = 0,18**, IC 95 % bootstrap **[-0,7 ; +7,6] pts** → **non significatif**. Contre la référence committée (123/145, audit `e1171032`), le même modèle donne **+19** (McNemar 21/2, p = 6,6e-05) : la règle live a absorbé l'essentiel pendant la session. Le classement ne lit pas la cible choisie par la règle (seule la comparaison la lit) ; ses **142/145 ne bougent pas** quand la règle passe de 123 à 137.
6: >
7: > **Dispositif** : [`classement_cible.py`](../tools/tests/linguistique/classement_cible.py), JSON [`pensee-classement-appris.json`](pensee-classement-appris.json). [`bloc_linguisti
… [10656 caractères tronqués]
  ```


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
… [14748 caractères tronqués]
  ```

- **grep** `{"pattern": "def (_cible_proche|_tete_nom|_verbe_dans|_tete_texte)|class Heuristique|attachement", "path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py"}`

  ```
Found 11 matches

tools/bloc_linguistique.py
Line 475: class Heuristique:
Line 620:     def _tete_texte(texte: str) -> str | None:
Line 635:     def _tete_nom(texte: str, debut: int, fin: int) -> str | None:
Line 642:     def _verbe_dans(texte: str, debut: int, fin: int,
Line 661:     def _cible_proche(texte: str, segment: dict, gvs: list[dict],
Line 690:         """Les verbes des `k` GV les plus proches — les **candidats** d'attachement."""
Line 716:             att = c.get("attachement") or {}
Line 860:             # candidat d'attachement (diagnostic des 33 échecs de T162).
Line 898:                         meta["attachement"] = {"segment": s.get("texte", ""), "cible": cible}
Line 918:                     meta["attachement"] = {"segment": s["texte"], "cible": cible}
Line 937:                     meta["attachement"] = {"segment": s["texte"], "cible": cible}
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "offset": 440, "limit": 280}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
440:                 "s", "ed", "ing", "en"):
441:         if n.endswith(suf) and n[:-len(suf)] in VERBES_CONNUS:
442:             return True
443:     # participes en -é/-és/-ée : `accroché` → `accrocher`
444:     for suf in ("ées", "ées", "ée", "és", "é"):
445:         if n.endswith(suf) and (n[:-len(suf)] + "er") in VERBES_CONNUS:
446:             return True
447:     return False
448: 
449: 
450: def _role_gp(prep: str) -> str:
451:     p = prep.casefold()
452:     if p in {"dans", "sur", "sous", "chez", "vers", "entre", "devant", "derrière", "près", "loin",
453:              "in", "on", "at", "under", "between"}:
454:         return "lieu"
455:     if p in {"pendant", "depuis", "durant", "avant", "après", "during", "since", "before", "after"}:
456:         return "temps"
457:     if p in {"pour", "afin", "for", "to"}:
458:         return "but"
459:     if p in {"par", "by"}:
460:         # `par` + GN est l'**agent** d'un passif (`Le chat est mangé par le chien`) ;
461:         # `avec`/`sans` restent le moyen.
462:         return "agent"
463:     if p in {"avec",
… [12974 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 300, "offset": 720}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
720:                 return att.get("cible")
721:             if meilleure is None:
722:                 meilleure = att.get("cible")
723:         return meilleure
724: 
725:     def _syntagmes_simple(self, texte: str, langue: str) -> list[dict]:
726:         mots = self._mots(texte)
727:         lex = POS_FERME.get(langue, POS_FERME["fr"])
728:         segments: list[dict] = []
729:         i = 0
730:         while i < len(mots):
731:             d, f, t, typ = mots[i]
732:             n = _normaliser(t)
733:             if typ == "mot" and n in lex.get("DET", set()):
734:                 j = i + 1
735:                 while j < len(mots) and mots[j][3] == "mot" and _normaliser(mots[j][2]) not in lex.get("PREP", set()) | lex.get("CONJ", set()) | lex.get("AUX", set()):
736:                     j += 1
737:                 role = "groupe nominal"
738:                 # le passif sans `par` : GN + AUX (être) + participe → le sujet est un patient
739:                 if j < len(mots) and _normaliser(mots[j][2]) in {
740:                         "est", "sont", "était", "ét
… [18000 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification des empreintes et lecture du prototype A3 existant

- **bash** `{"command": "sha256sum tools/bloc_linguistique.py; stat -c '%s %y' tools/bloc_linguistique.py; ls tools/tests/linguistique/", "description": "Hash and list linguistics test dir", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
6e8430180ccca615e330c33596ff3c4020666b9feb452c7b25f771b4066d3c65  tools/bloc_linguistique.py
101568 2026-11-05 13:51:26.638852086 -0500
anaphore.py
classement_cible.py
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
  ```

- **bash** `{"command": "git log --oneline -5 -- tools/bloc_linguistique.py; git diff --stat HEAD -- tools/bloc_linguistique.py", "description": "Recent history of bloc linguistique", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
9d5337ce B13 — L'ATTACHEMENT V2 : EXACT SPANS 0,8483 → 0,9448, TOP-K STRICT 0,6069 → 0,9724 ; 3 SOUS-AGENTS INTÉGRÉS, LE MODÈLE APPRIS REJETÉ ; 180/180
a408a909 B13 — LE LEXIQUE ÉLARGI (PARTICIPES IRRÉGULIERS ET EN -É) : EXACT 0,8082 → 0,8483 ; 174/174
23853cb7 B13 — L'ATTACHEMENT CIBLÉ : REL → ANTÉCÉDENT, GP → VERBE ; EXACT 0,6438 → 0,8082, VERBES 0,9412 ; 173/173
d8edd1d9 B13 — LE CLASSEMENT : EXACT 0,2260 → 0,6438 (CIBLE RÉDUITE À SA TÊTE) ; LE GOLD MÊLE DEUX CONVENTIONS (51 VERBES, 95 NOMS) ; 171/171
13e8bb2d B13 — LES SPANS PERDUS : 48 REL, 33 SUB, 12 GP (81 CHEZ S) ; LE GP EST BORNÉ AU VERBE ; 169/169
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py</path>
<type>file</type>
<content>
1: """classement_cible.py — prototype **autonome** d'un classement appris des candidats d'attachement.
2: 
3: Le problème. `bloc_linguistique.Heuristique` choisit la cible d'un segment par **type +
4: proximité** (REL/SUB → antécédent nominal à gauche, GP → verbe du GV le plus proche). Sur les
5: segments gold dont le span est prédit, cette règle donnait **123/145** en égalité exacte au
6: début de la session (référence de la consigne) ; un autre agent l'a modifiée pendant la
7: session (129 puis 137/145) — le run fige l'empreinte du fichier lu, et la fiche rapporte les
8: deux comparaisons. Ce fichier teste une autre sélection : un **score linéaire appris** sur des
9: features lisibles, candidat par candidat, sans toucher à `bloc_linguistique.py` (l'intégration
10: éventuelle est une autre décision).
11: 
12: Protocole (fixé ici). Limite assumée : le vivier, la liste des features et l'ordre de la liste
13: ont été dessinés après une passe exploratoire sur le corpus ; le découpage ne valide donc que
14: les **poids appris**, pas le dessin des feature
… [37244 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Inspection des cas cités dans le gold et des prédictions courantes

- **bash** `{"command": "python3 - <<'PY'\nimport json, pathlib\nbase = pathlib.Path('tools/tests/linguistique')\nids = {'g002','s041','g012','r018','s108','s122','r309','r048','r068','r230'}\nfor name in ('gold.json','gold_reel.json','gold_synthetique.json'):\n    d = json.loads((base/name).read_text(encoding= … [615 caractères tronqués]`

  ```
=== g002 fr | Le chat de la voisine dort.
    GP (8, 21) 'de la voisine' -> ['chat']
    mots: [(0, 2, 'Le', 'DET'), (3, 7, 'chat', 'NOUN'), (8, 10, 'de', 'PREP'), (11, 13, 'la', 'DET'), (14, 21, 'voisine', 'NOUN'), (22, 26, 'dort', 'VERB')]
=== g012 fr | Le canard est prêt à manger.
    GP (19, 27) 'à manger' -> ['prêt', 'canard']
    mots: [(0, 2, 'Le', 'DET'), (3, 9, 'canard', 'NOUN'), (10, 13, 'est', 'AUX'), (14, 18, 'prêt', 'ADJ'), (19, 20, 'à', 'PREP'), (21, 27, 'manger', 'VERB')]
=== r018 fr | La souris est prête à manger.
    GP (20, 28) 'à manger' -> ['prête', 'souris']
    mots: [(0, 2, 'La', 'DET'), (3, 9, 'souris', 'NOUN'), (10, 13, 'est', 'AUX'), (14, 19, 'prête', 'ADJ'), (20, 21, 'à', 'PREP'), (22, 28, 'manger', 'VERB')]
=== r048 fr | Il écrit une lettre à sa sœur.
    GP (20, 29) 'à sa sœur' -> ['écrit']
    mots: [(0, 2, 'Il', 'PRON'), (3, 8, 'écrit', 'VERB'), (9, 12, 'une', 'DET'), (13, 19, 'lettre', 'NOUN'), (20, 21, 'à', 'PREP'), (22, 24, 'sa', 'DET'), (25, 29, 'sœur', 'NOUN')]
=== r068 en | He writes a letter to his sister.
    GP (19, 32) 'to his sister' -> ['writes']
    mots: [(0, 2, 'He', 'PRON'), (3, 9, 'writes', 'VERB'), (10, 11, 'a', 'DET'), (12, 18, 'let
… [1335 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys, json, pathlib\nsys.dont_write_bytecode = True\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl\nfrom evaluer_gold import charger\nids = {'g002','s041','g012','r018','s108','s122','r309','r048','r068' … [462 caractères tronqués]`

  ```
=== g002 Le chat de la voisine dort.
   GN (0, 7) 'Le chat' meta= {'role': 'agent', 'niveau': 0} cands= ['« de la voisine dort » → Le chat', 'chat']
   GP (8, 21) 'de la voisine' meta= {'role': 'theme', 'niveau': 1, 'union': True} cands= ['GP']
   GP (8, 26) 'de la voisine dort' meta= {'role': 'possession', 'niveau': 1, 'attachement': {'segment': 'de la voisine dort', 'cible': 'chat'}} cands= ['« de la voisine dort » → Le chat', 'chat']
=== g012 Le canard est prêt à manger.
   GN (0, 9) 'Le canard' meta= {'role': 'agent', 'niveau': 1, 'attachement': {'segment': 'Le canard', 'cible': 'manger'}} cands= ['« à manger » → Le canard', '« à manger » → est prêt', 'est', 'manger', 'canard', 'prêt']
   GV (10, 18) 'est prêt' meta= {'role': 'predicat', 'niveau': 0, 'attachement': {'segment': 'est prêt', 'cible': 'canard'}} cands= ['« à manger » → Le canard', '« à manger » → est prêt', 'canard', 'prêt']
   GV (10, 27) 'est prêt à manger' meta= {'role': 'prédicat', 'niveau': 0, 'union': True} cands= ['GV']
   GP (19, 27) 'à manger' meta= {'role': 'but', 'niveau': 1, 'attachement': {'segment': 'à manger', 'cible': 'manger'}} cands= ['« à manger » → Le canard', '« à manger » → est prêt', 'manger'
… [3743 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Construction du banc d'essai : population 145/239 et diagnostic de la règle live

- **bash** `{"command": "python3 - <<'PY'\nimport sys, json, pathlib\nsys.dont_write_bytecode = True\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl\nfrom evaluer_gold import charger\nphrases = charger()\nh = bl.Heuristique()\nn_all=n_labels=0; empties= … [1722 caractères tronqués]`

  ```
gold segments avec cibles: 239 | span predit: 145
== vides/absentes sur les 145 ==
('g002', 'GP', 'de la voisine', ['chat'], 'NOUN', 'GP', {'role': 'theme', 'niveau': 1, 'union': True}, ['GP'])
('s041', 'GP', 'devant elles', ['marche', 'avocat'], 'VERB', 'GP', {'role': 'lieu', 'niveau': 1, 'union': True}, ['GP'])
nb vides sur 145: 2
== pred cible verbe, gold non-verbe ==
('g012', 'GP', 'à manger', ['prêt', 'canard'], 'manger', 'ADJ')
('r018', 'GP', 'à manger', ['prête', 'souris'], 'manger', 'ADJ')
nb: 2
== echecs exact == 8
('g002', 'GP', 'de la voisine', ['chat'], '', 'NOUN', None, {'role': 'theme', 'niveau': 1, 'union': True})
('g012', 'GP', 'à manger', ['prêt', 'canard'], 'manger', 'ADJ', True, {'role': 'but', 'niveau': 1, 'attachement': {'segment': 'à manger', 'cible': 'manger'}})
('r018', 'GP', 'à manger', ['prête', 'souris'], 'manger', 'ADJ', True, {'role': 'but', 'niveau': 1, 'attachement': {'segment': 'à manger', 'cible': 'manger'}})
('r230', 'SUB', 'Quand tu arrives', ['appelle'], 'appelle-moi', 'VERB', False, {'role': 'temps', 'niveau': 1, 'attachement': {'segment': 'Quand tu arrives', 'cible': 'appelle-moi'}})
('r309', 'SUB', "qu'il viendra", ['viendra'], 'Peut-être', 'V
… [583 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys, json\nsys.dont_write_bytecode = True\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl\nfrom evaluer_gold import charger\nids={'g002','s041','g012','r018','s108','s122','r309','r048'}\nh=bl.Heuristiqu … [1006 caractères tronqués]`

  ```
==================== g002 Le chat de la voisine dort.
cands type <class 'list'> len 1
 cles cands[0]: ['nom', 'lecture', 'attachement', 'segments']
  S seg: GN (0, 7) 'Le chat' nom= None att= None
  S seg: GP (8, 26) 'de la voisine dort' nom= None att= None
  brute pour 'de la voisine dort' -> Le chat
 cibles_s: {(0, 7, 'GN'): None, (8, 26, 'GP'): 'Le chat'}
 simples: [('GN', 0, 7, 'Le chat'), ('GP', 8, 21, 'de la voisine')]
==================== g012 Le canard est prêt à manger.
cands type <class 'list'> len 2
 cles cands[0]: ['nom', 'lecture', 'attachement', 'segments']
  S seg: GN (0, 9) 'Le canard' nom= None att= None
  S seg: GV (10, 18) 'est prêt' nom= None att= None
  S seg: GP (19, 27) 'à manger' nom= None att= None
  brute pour 'à manger' -> Le canard
 cibles_s: {(0, 9, 'GN'): None, (10, 18, 'GV'): 'Le canard', (19, 27, 'GP'): 'Le canard'}
 simples: [('GN', 0, 9, 'Le canard'), ('GV', 10, 27, 'est prêt à manger')]
==================== r018 La souris est prête à manger.
cands type <class 'list'> len 2
 cles cands[0]: ['nom', 'lecture', 'attachement', 'segments']
  S seg: GN (0, 9) 'La souris' nom= None att= None
  S seg: GV (10, 19) 'est prête' nom= None att= None
  S seg: GP
… [2486 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys\nsys.dont_write_bytecode=True\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nfor p,seg in [('ce calme papier rêve sous le nuage',(0,20)),('mon papier saute vers les montagne',(0,16)),('Le canard est prêt à manger.',(10,27)),('La souris est prêt … [532 caractères tronqués]`

  ```
'ce calme papier rêve sous le nuage' (0, 20) -> _verbe_dans= 'rêve' tete_texte= ['rêve']
    ce est_verbe False norm ce dans VERBES? False
    calme est_verbe False norm calme dans VERBES? False
    papier est_verbe False norm papier dans VERBES? False
    rêve est_verbe False norm rêve dans VERBES? False
    mon est_verbe False norm mon dans VERBES? False
    saute est_verbe False norm saute dans VERBES? False
    est est_verbe True norm est dans VERBES? False
    prêt est_verbe False norm prêt dans VERBES? False
    manger est_verbe True norm manger dans VERBES? False
    prête est_verbe False norm prête dans VERBES? False
'mon papier saute vers les montagne' (0, 16) -> _verbe_dans= 'saute' tete_texte= ['saute']
    ce est_verbe False norm ce dans VERBES? False
    calme est_verbe False norm calme dans VERBES? False
    papier est_verbe False norm papier dans VERBES? False
    rêve est_verbe False norm rêve dans VERBES? False
    mon est_verbe False norm mon dans VERBES? False
    saute est_verbe False norm saute dans VERBES? False
    est est_verbe True norm est dans VERBES? False
    prêt est_verbe False norm prêt dans VERBES? False
    manger est_verbe True norm manger dans VE
… [1332 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys\nsys.dont_write_bytecode=True\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl\nfrom evaluer_gold import charger\np=next(x for x in charger() if x['id']=='s108')\nh=bl.Heuristique()\ntexte=p['texte']; … [1004 caractères tronqués]`

  ```
verbes: [(9, 15, 'papier')]
seg GN ce calme papier rêve brute= None cible_proche= None
  attachement S= None
seg GP sous le nuage brute= 'ce calme papier rêve' cible_proche= None
  find= 0 verbe_dans= papier
  attachement S= None
top-level cands att: [{'segment': 'sous le nuage', 'cible': 'ce calme papier rêve', 'genre': 'GN'}]
  ```

- **grep** `{"pattern": "g002|s041|r309|repli.*cible|préférer un verbe|prefer.*verbe", "path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports"}`

  ```
Found 30 matches

reports/rapport-contrat-s.md
Line 316: | **POS gold vs `CONVENTION_CIBLE`** | SUB : **69/69 VERB** (42 gauche, 26 droite, 1 interne) ; REL : 73 NOUN + 1 PRON, à gauche | la convention écrite (`gold_reel.py:25-32`, « SUB → antécédent, tête du GN à gauche ») est **contredite par les données** ; le 28/36 SUB de l'état initial doit beaucoup au repli `_cible_proche` (les 6 erreurs synthétiques sont les cas où un GN à gauche existe) |

reports/rapport-classement-appris.md
Line 80: 4. **Les 8 erreurs de la règle live** : `g002` et `s041` (cible vide sur le doublon d'union), `g012` / `r018` (« à manger » → `manger` au lieu de `prêt` / `prête`), `s108` / `s122` (nom à gauche du GP au lieu du verbe), `r309` (« Peut-être qu'il viendra » → `Peut-être` au lieu de `viendra`), `r230`. Le modèle en répare 7, mais introduit `r048` / `r068`.
Line 100: 2. **Le fallback quand la cible est vide** (g002, s041) : +2 sans risque, indépendant du reste.
Line 102: 4. **`r309`** : accepter un candidat intérieur quand le segment est une complétive en tête de phrase.

reports/pensee-annotation-independante.json
Line 1062:      "id": "r309",
Line 1157:      "id": "g002",
Line 1270:      "id": "
… [2094 caractères tronqués]
  ```

- **grep** `{"pattern": "g002|s041|r309|repli.*cible|préférer un verbe", "path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs"}`

  ```
No matches found
  ```

### 🤖 Assistant

⏵ Lecture des fiches existantes sur la proximité de cible et le diagnostic top-k

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-cible-proximite.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-topk-diagnostic.md", "limit": 140, "offset": 60}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-cible-proximite.md</path>
<type>file</type>
<content>
1: # B13 — la cible par proximité : l'exact passe de 0,0042 à 0,0544 (×13)
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-04 · **Verdict** : ✅
4: > **164/164 portes** : la règle « la cible d'un segment est le **verbe du GV le plus proche** »
5: > remplit les `cible` que le générateur S laissait vides. Sur le même gold que T153 (612 phrases,
6: > **239 cibles**), l'attachement passe de **top1 82 (0,3431)** à **95 (0,3975)**, et surtout de
7: > **exact 1 (0,0042)** à **13 (0,0544)** — **×13**. La tête fait **94/145 (0,6483)** contre 81
8: > (0,5586).
9: >
10: > **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_cible_proche`),
11: > [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
12: > [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-cible-proximite.json`](pensee-cible-proximite.json).
13: 
14: ## 1. Avant / après (même gold, 612 phrases, 239 cibles)
15: 
16: | mesure | T153 (avant) | **règle de proximité** | écart |
17: |---|---:|---:|---:|
18: | top1 | 82 (0,
… [2577 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-topk-diagnostic.md</path>
<type>file</type>
<content>
60: **Lecture par cause.**
61: 
62: - **C1 (26 REL)** : le S nomme l'antécédent dans `« que j'ai lu » → Le livre` ; `_tete_nom`
63:   rendrait `livre`, mais `candidats` garde la chaîne entière (plus `est`). Exemple :
64:   `g011` « que j'ai lu » → `livre`, candidats `["« que j'ai lu » → Le livre", "est"]`.
65: - **C2 (17 GP)** : le S nomme le verbe dans `« dans le jardin » → Les fleurs poussent` ; la
66:   cible `poussent` est le **dernier token** de la queue. 15/17 ont déjà la bonne cible choisie ;
67:   **s108** et **s122** choisissent en plus le nom `papier` au lieu de `rêve`/`saute` (la cible
68:   nominale du S, `cible_nom`, passe avant `cible_verbe`).
69: - **C3 (2 GP)** : `g012` « à manger » → `prêt`, `r018` → `prête` ; la cible est l'adjectif
70:   attribut de `est prêt`/`est prête`, la cible choisie est le verbe `manger`.
71: - **C4 (8 GP anglais)** : `_est_verbe("fly")` est faux (absent de `VERBES_CONNUS`), le POS le
72:   tague NOUN et le GV du S n'est pas coupé au verbe ; les candidats sont `["GP", "lake"]` au
73:   lieu de contenir `fly`. Les 8 ve
… [8517 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-classement-appris.json',encoding='utf-8'))\nids={'g002','s041','g012','r018','s108','s122','r309','r230','r048','r068'}\nfor s in d['segments']:\n    if s['id'] in ids and s['type'] in ('GP','SUB'):\n        print('===',s[' … [482 caractères tronqués]`

  ```
=== g002 GP 'de la voisine' gold= chat live= '' modele= 'chat' ok True
    0 'chat' d= 1 cote= gauche verbe_lex= False pos= NOUN score= 0.8858 positif= 1
    1 'dort' d= 1 cote= droite verbe_lex= True pos= VERB score= 0.485352 positif= 0
    2 'voisine' d= 0 cote= dedans verbe_lex= False pos= NOUN score= -4.45794 positif= 0
=== g012 GP 'à manger' gold= prêt live= 'manger' modele= 'prêt' ok True
    0 'prêt' d= 1 cote= gauche verbe_lex= False pos= ADJ score= 0.969431 positif= 1
    1 'canard' d= 3 cote= gauche verbe_lex= False pos= NOUN score= -0.875487 positif= 0
    2 'manger' d= 0 cote= dedans verbe_lex= True pos= VERB score= -1.559971 positif= 0
=== r018 GP 'à manger' gold= prête live= 'manger' modele= 'prête' ok True
    0 'prête' d= 1 cote= gauche verbe_lex= False pos= ADJ score= 0.974593 positif= 1
    1 'souris' d= 3 cote= gauche verbe_lex= False pos= NOUN score= -0.875487 positif= 0
    2 'manger' d= 0 cote= dedans verbe_lex= True pos= VERB score= -1.559971 positif= 0
=== r048 GP 'à sa sœur' gold= écrit live= 'écrit' modele= 'lettre' ok False
    0 'lettre' d= 1 cote= gauche verbe_lex= False pos= NOUN score= 1.066298 positif= 0
    1 'écrit' d= 3 cote= gauche verbe_lex= Tru
… [1936 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Analyse exhaustive des 145 cibles : natures, rangs, règles candidates

- **bash** `{"command": "cat > /tmp/explo_replis.py <<'PY'\nimport sys, json, pathlib, re\nsys.dont_write_bytecode=True\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl\nfrom evaluer_gold import charger\nTYPES=('GP','REL','SUB')\nPOS_OUV={'NOUN','PROPN', … [4623 caractères tronqués]`

  ```
n rows 145

== Q1: vides/absentes ==
total cibles gold 239 ; spans predits 145
vides sur 145: 2
   g002 GP 'de la voisine' gold chat nom
   s041 GP 'devant elles' gold marche verbe
239: 239 non predits: 94 Counter({'REL': 48, 'SUB': 33, 'GP': 13}) predits vides: 2 [('g002', 'GP'), ('s041', 'GP')]

== Q1: croisement nature predite x nature gold (sur 145) ==
  ('', 'nom') 1
  ('', 'verbe') 1
  ('adv', 'verbe') 1
  ('nom', 'nom') 26
  ('nom', 'verbe') 3
  ('verbe', 'nom') 2
  ('verbe', 'verbe') 111
-- pred nom, gold verbe --
   r230 SUB 'Quand tu arrives' base 'appelle-moi' gold appelle ok False
   s108 GP 'sous le nuage' base 'papier' gold rêve ok False
   s122 GP 'vers les montagne' base 'papier' gold saute ok False
-- pred verbe, gold non-verbe --
   g012 GP 'à manger' base 'manger' gold prêt nom ok False
   r018 GP 'à manger' base 'manger' gold prête nom ok False

== echecs exact ==
   g002 GP 'de la voisine' base '' [(0, 'chat', 'gauche', 1, 'NOUN'), (1, 'dort', 'droite', 1, 'VERB'), (2, 'voisine', 'dedans', 0, 'NOUN')] gold chat
   g012 GP 'à manger' base 'manger' [(0, 'prêt', 'gauche', 1, 'ADJ'), (1, 'canard', 'gauche', 3, 'NOUN'), (2, 'manger', 'dedans', 0, 'VERB')] gold prêt

… [919 caractères tronqués]
  ```

- **bash** `{"command": "cat >> /tmp/explo_replis.py <<'PY'\n\ndef top1(pred, cs):\n    return bool(pred and any(c in pred or pred in c for c in cs))\ndef eval_rule(name, fn, scope=None):\n    fixed=[]; reg=[]; ok=0; t1=0; n=0\n    for r in rows:\n        if scope and not scope(r): continue\n        n+=1\n      … [4747 caractères tronqués]`

  ```
== regles candidates (sur les 145) ==
rang0 partout                          n=145 exact=139/145 (base 137) top1=142/145 (base 140) fix=7 reg=5 net=+2
    fix: [('g002', 'GP', '', 'chat'), ('g012', 'GP', 'manger', 'prêt'), ('r018', 'GP', 'manger', 'prête'), ('r309', 'SUB', 'Peut-être', 'viendra'), ('s041', 'GP', '', 'marche'), ('s108', 'GP', 'papier', 'rêve'), ('s122', 'GP', 'papier', 'saute')]
    REG: [('g003', 'GP', 'vu', 'homme', 'vu'), ('g014', 'GP', 'vu', 'homme', 'vu'), ('g016', 'GP', 'saw', 'man', 'saw'), ('r048', 'GP', 'écrit', 'lettre', 'écrit'), ('r068', 'GP', 'writes', 'letter', 'writes')]
verbe lexique le plus proche           n=145 exact=117/145 (base 137) top1=119/145 (base 140) fix=0 reg=20 net=-20
    REG: [('r015', 'REL', 'film', 'sorti', 'film'), ('r054', 'REL', 'livre', 'lis', 'livre'), ('r094', 'REL', 'film', 'vu', 'film'), ('r095', 'REL', 'maison', 'né', 'maison'), ('r201', 'REL', 'homme', 'parle', 'homme'), ('r209', 'REL', 'élève', 'parle', 'élève'), ('r212', 'SUB', 'faut', 'partes', 'faut'), ('r213', 'REL', 'film', 'parle', 'film'), ('r226', 'REL', 'jour', 'partis', 'jour'), ('r227', 'SUB', 'lit', 'dort', 'lit'), ('r232', 'SUB', 'pense', 'devons', 'pense'), 
… [19624 caractères tronqués]
  ```

- **bash** `{"command": "cat >> /tmp/explo_replis.py <<'PY'\n\nprint('\\n== TOP1 sans exact ==')\nfor r in rows:\n    if r['top1_base'] and not r['ok_base']:\n        print('  ',r['id'],r['type'],'base',repr(r['base']),'gold',r['gold_all'])\n\ndef cote_of(r, tok):\n    return next((c['cote'] for c in r['cands'] … [3549 caractères tronqués]`

  ```
== TOP1 sans exact ==
   r230 SUB base 'appelle-moi' gold ['appelle']
   s108 GP base 'papier' gold ['rêve', 'papier']
   s122 GP base 'papier' gold ['saute', 'papier']

== variantes autour du rang 0 sur les GP ==
T2b GP base dedans -> rang0            n=145 exact=139/145 (base 137) top1=142/145 (base 140) fix=2 reg=0 net=+2
    fix: [('g012', 'GP', 'manger', 'prêt'), ('r018', 'GP', 'manger', 'prête')]
T2c GP (nom ou dedans) -> rang0        n=145 exact=141/145 (base 137) top1=142/145 (base 140) fix=4 reg=0 net=+4
    fix: [('g012', 'GP', 'manger', 'prêt'), ('r018', 'GP', 'manger', 'prête'), ('s108', 'GP', 'papier', 'rêve'), ('s122', 'GP', 'papier', 'saute')]
T2d GP rang0 sauf verbe garde          n=145 exact=141/145 (base 137) top1=142/145 (base 140) fix=4 reg=0 net=+4
    fix: [('g012', 'GP', 'manger', 'prêt'), ('r018', 'GP', 'manger', 'prête'), ('s108', 'GP', 'papier', 'rêve'), ('s122', 'GP', 'papier', 'saute')]
T2e GP nom -> gauche plus proche       n=145 exact=139/145 (base 137) top1=140/145 (base 140) fix=2 reg=0 net=+2
    fix: [('s108', 'GP', 'papier', 'rêve'), ('s122', 'GP', 'papier', 'saute')]
T2f GP dedans -> gauche plus proche    n=145 exact=139/145 (base 137) top1=142/1
… [14835 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Prototype de simulation par sous-classe et post-traitement des cibles

- **bash** `{"command": "cat > /tmp/sim_replis.py <<'PY'\nimport sys\nsys.dont_write_bytecode=True\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl\nfrom evaluer_gold import charger, evaluer_bloc\n\nPOS_OUV={'NOUN','PROPN','VERB','ADJ'}\nAUX=bl.AUXILIAIR … [7310 caractères tronqués]`

  ```
phrases 612
baseline time 0.5
baseline att: {'cibles': 239, 'labels': 145, 'top1': 140, 'exact': 137, 'topk': 142, 'top1_taux': 0.5858, 'top1_taux_span': 0.9655, 'exact_taux': 0.5732, 'exact_taux_span': 0.9448, 'topk_exact': 141}
per_seg n 145 ok 137 top1 140
noop                   exact=137/239 (0.5732) top1=140/239 (0.5858) span exact=0.9448 top1span=0.9655 fix=0 reg=0 time=0.9s
T1_rang0               exact=137/239 (0.5732) top1=140/239 (0.5858) span exact=0.9448 top1span=0.9655 fix=0 reg=0 time=1.0s
   fix ids: []
   reg ids: []
T1_dernier(neg)        exact=137/239 (0.5732) top1=140/239 (0.5858) span exact=0.9448 top1span=0.9655 fix=0 reg=0 time=1.0s
   fix ids: []
   reg ids: []
T1_verbe               exact=137/239 (0.5732) top1=140/239 (0.5858) span exact=0.9448 top1span=0.9655 fix=0 reg=0 time=1.0s
   fix ids: []
   reg ids: []
T2_litteral            exact=137/239 (0.5732) top1=140/239 (0.5858) span exact=0.9448 top1span=0.9655 fix=0 reg=0 time=1.0s
   fix ids: []
   reg ids: []
T2_litteral_pos        exact=137/239 (0.5732) top1=140/239 (0.5858) span exact=0.9448 top1span=0.9655 fix=0 reg=0 time=1.0s
   fix ids: []
   reg ids: []
T2_litteral_ext        exact=137/239 (0.5732) 
… [1989 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\np='/tmp/sim_replis.py'\ns=open(p).read()\ns=s.replace(\"\"\"            cible=new\n            # T2\"\"\",\"\"\"            cible=new\n            # T2\"\"\")\n# rewrite modifier applying on a variable 'ancienne' and setting at end\nstart=s.index('    def modifier(self … [3057 caractères tronqués]`

  ```
phrases 612
baseline time 0.4
baseline att: {'cibles': 239, 'labels': 145, 'top1': 140, 'exact': 137, 'topk': 142, 'top1_taux': 0.5858, 'top1_taux_span': 0.9655, 'exact_taux': 0.5732, 'exact_taux_span': 0.9448, 'topk_exact': 141}
per_seg n 145 ok 137 top1 140
noop                   exact=137/239 (0.5732) top1=140/239 (0.5858) span exact=0.9448 top1span=0.9655 fix=0 reg=0 time=0.8s
T1_rang0               exact=139/239 (0.5816) top1=142/239 (0.5941) span exact=0.9586 top1span=0.9793 fix=2 reg=0 time=0.9s
   fix ids: [('g002', 'GP', 'chat'), ('s041', 'GP', 'marche')]
   reg ids: []
T1_dernier(neg)        exact=137/239 (0.5732) top1=141/239 (0.5900) span exact=0.9448 top1span=0.9724 fix=0 reg=0 time=0.9s
   fix ids: []
   reg ids: []
T1_verbe               exact=137/239 (0.5732) top1=140/239 (0.5858) span exact=0.9448 top1span=0.9655 fix=0 reg=0 time=0.9s
   fix ids: []
   reg ids: []
T2_litteral            exact=137/239 (0.5732) top1=140/239 (0.5858) span exact=0.9448 top1span=0.9655 fix=0 reg=0 time=0.9s
   fix ids: []
   reg ids: []
T2_litteral_pos        exact=131/239 (0.5481) top1=134/239 (0.5607) span exact=0.9034 top1span=0.9241 fix=0 reg=6 time=1.0s
   fix ids: []
   reg ids: [
… [2607 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Mesure de la surface de changement (toutes étiquettes, pas seulement les 145 gold)

- **bash** `{"command": "cat > /tmp/surface.py <<'PY'\nimport sys\nsys.dont_write_bytecode=True\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nexec(open('/tmp/sim_replis.py').read().split(\"phrases=charger()\")[0])\nphrases=charger()\ndef gold_spans():\n    s=set()\n    for p in phr … [2489 caractères tronqués]`

  ```
T1 total labels 863
T2_rang0_garde total labels 863
T2_rang0 total labels 863
T3_strict total labels 863
combine total labels 863
T1               total= 863 changes=114 dont gold=2 autres=112
   ex autres: [('g002', 'GN', 0, 7, 'Le chat', '', 'voisine'), ('g006', 'GN', 0, 8, 'Le chien', '', 'voisin'), ('r004', 'GN', 0, 16, 'Le soleil brille', '', 'soleil'), ('r019', 'GN', 0, 20, 'Le vent souffle fort', '', 'vent'), ('r042', 'GN', 0, 24, 'La mère prépare le repas', '', 'mère'), ('r046', 'GN', 0, 12, 'Le chat boit', '', 'lait'), ('r047', 'GN', 0, 19, 'Les fleurs poussent', '', 'jardin'), ('r051', 'GN', 0, 21, 'La voiture roule vite', '', 'voiture'), ('r057', 'GN', 0, 14, 'Le chien aboie', '', 'facteur'), ('r059', 'GN', 0, 30, 'Le cuisinier prépare un gâteau', '', 'cuisinier'), ('r060', 'GN', 0, 28, 'Les oiseaux volent au-dessus', '', 'lac'), ('r081', 'GN', 0, 29, 'Le facteur apporte une lettre', '', 'facteur')]
T2_rang0_garde   total= 863 changes=  0 dont gold=0 autres=0
T2_rang0         total= 863 changes=  7 dont gold=4 autres=3
   ex autres: [('r083', 'GP', 9, 22, 'entre en gare', 'gare', 'train'), ('r121', 'GP', 20, 30, 'des fleurs', 'jardinier', 'plante'), ('r227', 'GP', 0, 13,
… [157 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys\nsys.dont_write_bytecode=True\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nexec(open('/tmp/sim_replis.py').read().split(\"phrases=charger()\")[0])\nprint('est_verbe papier',bl._est_verbe('papier'),'reve',bl._est_verbe('rêve'),' … [369 caractères tronqués]`

  ```
est_verbe papier False reve False saute False
{'t2': 'rang0'} [('GN', 0, 20, {'role': 'agent', 'niveau': 0}), ('GP', 21, 34, {'role': 'lieu', 'niveau': 1, 'attachement': {'segment': 'sous le nuage', 'cible': 'rêve'}})]
{'t2': 'rang0_garde'} [('GN', 0, 20, {'role': 'agent', 'niveau': 0}), ('GP', 21, 34, {'role': 'lieu', 'niveau': 1, 'attachement': {'segment': 'sous le nuage', 'cible': 'papier'}})]
  ```

- **bash** `{"command": "sed -n '/def modifier/,/def per_seg/p' /tmp/sim_replis.py", "description": "Inspect modifier source"}`

  ```
def modifier(self,a,texte):
        pos=_pos(a); mots=bl.Heuristique._mots(texte)
        for e in a.etiquettes:
            if e.niveau!='syntagme' or e.type=='GV': continue
            seg={'type':e.type,'debut':e.debut,'fin':e.fin,'texte':e.valeur}
            cands=candidats_pour(texte,seg,a)
            if not cands: continue
            meta=e.meta or {}; att=meta.get('attachement') or {}
            ancienne=(att.get('cible') or '').strip()
            cible=ancienne
            # T1
            if self.t1 is not None and not cible:
                if self.t1=='rang0': cible=cands[0]['texte']
                elif self.t1=='dernier': cible=cands[-1]['texte']
                elif self.t1=='verbe': cible=next((c['texte'] for c in cands if self.est_verbe(c['texte'])),'')
                elif self.t1=='droite': cible=next((c['texte'] for c in cands if c['cote']=='droite'),'')
            actuel=next((c for c in cands if c['texte']==cible),None)
            # T2
            if self.t2 is not None and e.type=='GP' and cible:
                if self.t2=='litteral':
                    if not self.est_verbe(cible):
                        bd=actuel['dist'] if actuel else 99
         
… [1554 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\np='/tmp/sim_replis.py'\ns=open(p).read()\n# add t2_scope/t1_scope\ns=s.replace(\"def __init__(self, t1=None, t2=None, t3=None, extra_lex=()):\\n        super().__init__()\\n        self.t1=t1; self.t2=t2; self.t3=t3; self.extra=set(extra_lex)\",\n\"def __init__(self, t … [2724 caractères tronqués]`

  ```
T1_tous          labels=863 changes=114 or=2 autres=112 par_type={'GN': 111, 'GP': 3}
T1_GP            labels=863 changes=  3 or=2 autres=1 par_type={'GP': 3}
T2_garde_GP      labels=863 changes=  7 or=4 autres=3 par_type={'GP': 7}
T2_garde_tous    labels=863 changes=235 or=4 autres=231 par_type={'GN': 227, 'GP': 7, 'REL': 1}
T2_brut_GP       labels=863 changes=  7 or=4 autres=3 par_type={'GP': 7}
T2_brut_tous     labels=863 changes=235 or=4 autres=231 par_type={'GN': 227, 'GP': 7, 'REL': 1}
T3_strict        labels=863 changes=  1 or=1 autres=0 par_type={'SUB': 1}
combine_GP       labels=863 changes= 11 or=7 autres=4 par_type={'GP': 10, 'SUB': 1}
combine_tous     labels=863 changes=122 or=7 autres=115 par_type={'GN': 111, 'GP': 10, 'SUB': 1}
  ```

- **bash** `{"command": "cat > /tmp/surface3.py <<'PY'\nimport sys\nsys.dont_write_bytecode=True\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nexec(open('/tmp/sim_replis.py').read().split(\"phrases=charger()\")[0])\nphrases=charger()\ngs=set()\nfor p in phrases:\n    for seg in p[' … [1573 caractères tronqués]`

  ```
== T1_GP
   s027 GP (26, 33) 'avec il' -> 'marche' (avant '' )
       phrase: mon sombre village marche avec il
       gold segs: [('GP', 31, 33, 'il', ['marche', 'village'])]
== T2_garde_GP
   r083 GP (9, 22) 'entre en gare' -> 'train' (avant 'gare' )
       phrase: Le train entre en gare.
       gold segs: [('GP', 15, 22, 'en gare', ['entre'])]
   r121 GP (20, 30) 'des fleurs' -> 'plante' (avant 'jardinier' )
       phrase: Le jardinier plante des fleurs.
       gold segs: []
   r227 GP (0, 13) "Pendant qu'il" -> 'dort' (avant 'lit' )
       phrase: Pendant qu'il dort, elle lit.
       gold segs: [('SUB', 0, 18, "Pendant qu'il dort", ['lit'])]
== combine_GP
   r083 GP (9, 22) 'entre en gare' -> 'train' (avant 'gare' )
       phrase: Le train entre en gare.
       gold segs: [('GP', 15, 22, 'en gare', ['entre'])]
   r121 GP (20, 30) 'des fleurs' -> 'plante' (avant 'jardinier' )
       phrase: Le jardinier plante des fleurs.
       gold segs: []
   r227 GP (0, 13) "Pendant qu'il" -> 'dort' (avant 'lit' )
       phrase: Pendant qu'il dort, elle lit.
       gold segs: [('SUB', 0, 18, "Pendant qu'il dort", ['lit'])]
   s027 GP (26, 33) 'avec il' -> 'marche' (avant '' )
       phrase: 
… [97 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"def _normaliser\" -A 12 tools/bloc_linguistique.py | head -20", "description": "Check normalisation helper", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
144:def _normaliser(texte: str) -> str:
145-    return unicodedata.normalize("NFC", texte).casefold()
146-
147-
148-def _trigrammes(texte: str) -> list[str]:
149-    t = _normaliser(texte)
150-    return [t[i:i + 3] for i in range(max(0, len(t) - 2))]
151-
152-
153-def _profil(texte: str, top: int = 200) -> dict[str, int]:
154-    c = collections.Counter(_trigrammes(texte))
155-    return dict(c.most_common(top))
156-
  ```

### 🤖 Assistant

⏵ Vérification du format des JSON de pensée et des conventions de fiche

- **bash** `{"command": "python3 - <<'PY'\nimport json\nfor f in ['reports/pensee-cible-proximite.json','reports/pensee-quatre-modes.json']:\n    d=json.load(open(f,encoding='utf-8'))\n    print('==',f,'keys:',list(d.keys()))\n    for k,v in d.items():\n        if isinstance(v,(str,int,float,bool)) or v is None … [368 caractères tronqués]`

  ```
== reports/pensee-cible-proximite.json keys: ['date', 'ligne', 'portes', 'gold', 'cibles', 'avant', 'apres', 'inchanges', 'limites']
   date = '2026-11-04'
   ligne = 'B13'
   portes = '164/164'
   gold = 612
   cibles = 239
   avant : dict keys ['top1', 'top1_taux', 'exact', 'exact_taux', 'tete', 'tete_taux']
   apres : dict keys ['top1', 'top1_taux', 'exact', 'exact_taux', 'tete', 'tete_taux']
   inchanges : dict keys ['topk', 'couverture']
   limites : list 3 ex: ['226 échecs non qualifiés']
== reports/pensee-quatre-modes.json keys: ['date', 'gold', 'modes', 'seuils', 'refus', 'refus_detail', 'appels', 'api', 'latence_s', 'duree_totale_s', 'limites']
   date = '2026-11-04 10:37 EST'
   gold : dict keys ['phrases', 'tokens', 'modalite']
   modes : dict keys ['heuristique', 'neuronal', 'parallele', 'cascade', 'parallele_niveau', 'cascade_niveau']
   seuils : dict keys ['heuristique', 'neuronal', 'parallele', 'cascade', 'parallele_niveau', 'cascade_niveau', 'aucun_refus']
   refus = 0
   refus_detail : list 0 ex: []
   appels : dict keys ['pos', 'syntagmes']
   api : dict keys ['appels', 'tokens', 'latence_s']
   latence_s : dict keys ['moyenne', 'mediane']
   duree_totale_s = 0.0

… [108 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Génération des listes Q1 (94 spans absents, 2 vides, croisement des natures)

- **bash** `{"command": "python3 - <<'PY'\nimport sys, json\nsys.dont_write_bytecode=True\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl\nfrom evaluer_gold import charger\nphrases=charger(); h=bl.Heuristique()\ndef cibles(s): return s.get('cibles') or  … [851 caractères tronqués]`

  ```
GP 13
   g006, g020, r028, r038, r060, r083, r102, r153, r162, s027, s146, s148, s160
REL 48
   r034, r035, r074, r075, r114, r115, r204, r206, r214, r217, r220, r224, r236, r239, r241, r243, r246, r248, r250, r255, r273, r278, r280, r283, r285, r287, r289, r291, r293, r297, r299, r300, s010, s032, s035, s037, s050, s061, s065, s069, s070, s072, s075, s115, s125, s131, s135, s141
SUB 33
   g017, r205, r215, r216, r218, r219, r237, r238, r240, r242, r244, r245, r247, r249, r264, r279, r281, r282, r284, r286, r288, r290, r292, r294, r296, r298, r303, r313, s015, s044, s112, s114, s132
empty [('g002', 'GP', 'de la voisine', ['chat']), ('s041', 'GP', 'devant elles', ['marche', 'avocat'])]
  ```

### 🤖 Assistant

⏵ Écriture du prototype `tools/tests/linguistique/replis_cible.py`

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/replis_cible.py", "content": "\"\"\"replis_cible.py — prototype **autonome** des trois retouches d'attachement de A3.\n\nLe problème. La fiche `reports/rapport-classement-appris.md` (B13) recommande trois\nretouc … [40486 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/replis_cible.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

### 🤖 Assistant

⏵ Correction de la sérialisation JSON et premier run complet du prototype

- **bash** `{"command": "python3 - <<'PY'\np='tools/tests/linguistique/replis_cible.py'\ns=open(p,encoding='utf-8').read()\ns=s.replace('''def _empreinte_bloc() -> dict:''','''def _config_json(config: dict) -> dict:\n    \"\"\"Copie sérialisable d'une configuration (les frozensets deviennent des listes).\"\"\"\ … [606 caractères tronqués]`

  ```
== base ==
bloc: {'fichier': 'tools/bloc_linguistique.py', 'sha256_16': 'bb0205165cc2b0f8', 'octets': 103191, 'mtime': '2026-11-05T15:03:12'}
exact 137/145 (0.9448) | top1 140/145 (0.9655) | topk strict 141/239 | exact global 137/239 (0.5732)
== retouches ==
R1_repli_vide_GP                 exact 139/145 (0.9586) Δ+2 top1 142/145 (0.9793) Δ+2 reg  0 | surface   3 (2 gold / 1 hors)
R1_repli_vide_tous_non_GV        exact 139/145 (0.9586) Δ+2 top1 142/145 (0.9793) Δ+2 reg  0 | surface 114 (2 gold / 112 hors)
R1_dernier_temoin                exact 137/145 (0.9448) Δ+0 top1 141/145 (0.9724) Δ+1 reg  0 | surface   3 (2 gold / 1 hors)
R1_verbe_lexique_temoin          exact 137/145 (0.9448) Δ+0 top1 140/145 (0.9655) Δ+0 reg  0 | surface   1 (1 gold / 0 hors)
R2_litterale                     exact 137/145 (0.9448) Δ+0 top1 140/145 (0.9655) Δ+0 reg  0 | surface   3 (0 gold / 3 hors)
R2_litterale_POS                 exact 131/145 (0.9034) Δ-6 top1 134/145 (0.9241) Δ-6 reg  6 | surface  11 (6 gold / 5 hors)
R2_litterale_lexique_etendu      exact 139/145 (0.9586) Δ+2 top1 140/145 (0.9655) Δ+0 reg  0 | surface   5 (2 gold / 3 hors)
R2_preference_tete               exact 141/145 (0.9724) Δ+4 top1
… [1321 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Le bloc a changé pendant la session (autre agent) : inspection du diff et de l'impact

- **bash** `{"command": "git status --porcelain tools/bloc_linguistique.py; git diff --stat HEAD -- tools/bloc_linguistique.py; git diff HEAD -- tools/bloc_linguistique.py | head -120", "description": "Inspect concurrent change to bloc linguistique", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
M tools/bloc_linguistique.py
 tools/bloc_linguistique.py | 20 +++++++++++++++++++-
 1 file changed, 19 insertions(+), 1 deletion(-)
diff --git a/tools/bloc_linguistique.py b/tools/bloc_linguistique.py
index 07a41ec9..618994bc 100644
--- a/tools/bloc_linguistique.py
+++ b/tools/bloc_linguistique.py
@@ -428,9 +428,20 @@ am is are was were be been being have has had having do does did done
 """.split())
 
 
+ENCLITIQUES = ("-moi", "-toi", "-nous", "-vous", "-le", "-la", "-les", "-lui", "-leur", "-y", "-en")
+
+
+def _sans_enclitique(mot: str) -> str:
+    """`appelle-moi` → `appelle` (les enclitiques ne font pas partie de la tête)."""
+    for suf in ENCLITIQUES:
+        if mot.endswith(suf) and len(mot) > len(suf):
+            return mot[: -len(suf)]
+    return mot
+
+
 def _est_verbe(mot: str) -> bool:
     """Le mot est-il un verbe ? Lexique + désinences courantes (fr/en)."""
-    n = _normaliser(mot)
+    n = _normaliser(_sans_enclitique(mot))
     if not n:
         return False
     if n in VERBES_CONNUS:
@@ -644,6 +655,7 @@ class Heuristique:
                     strict: bool = False) -> str | None:
         """Le **verbe** du span : le lexique d'abord, puis le POS `VERB`, s
… [1017 caractères tronqués]
  ```

- **bash** `{"command": "sha256sum tools/bloc_linguistique.py; stat -c '%s %y' tools/bloc_linguistique.py; git log --oneline -3 -- tools/bloc_linguistique.py", "description": "Current fingerprint of bloc", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
bb0205165cc2b0f880f3df26c65ab56349c77301a7d9325025b35c28e145eb44  tools/bloc_linguistique.py
103191 2026-11-05 15:03:12.069753012 -0500
e0592c59 B13 — LE CACHE DU CHUNKER APPLIQUÉ : ×139 À 160 RÉPÉTITIONS, SORTIE IDENTIQUE (0/612) ; ×1 EN DÉFAUT, S DOMINE ; 181/181
9d5337ce B13 — L'ATTACHEMENT V2 : EXACT SPANS 0,8483 → 0,9448, TOP-K STRICT 0,6069 → 0,9724 ; 3 SOUS-AGENTS INTÉGRÉS, LE MODÈLE APPRIS REJETÉ ; 180/180
a408a909 B13 — LE LEXIQUE ÉLARGI (PARTICIPES IRRÉGULIERS ET EN -É) : EXACT 0,8082 → 0,8483 ; 174/174
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-replis-cible.json',encoding='utf-8'))\nprint('base',{k:d['base'][k] for k in ('exact','labels','top1','topk_exact','exact_taux_span','top1_taux_span')})\nfor nom,v in d['variantes'].items():\n    print('\\n==',nom,'| exact' … [758 caractères tronqués]`

  ```
base {'exact': 137, 'labels': 145, 'top1': 140, 'topk_exact': 141, 'exact_taux_span': 0.9448, 'top1_taux_span': 0.9655}

== R1_repli_vide_GP | exact {'justes': 139, 'n': 145, 'taux': 0.9586, 'gain': 2, 'regressions': 0, 'net': 2} | top1 {'justes': 142, 'n': 145, 'taux': 0.9793, 'gain': 2, 'regressions': 0, 'net': 2} | mcnemar 0.5
  gains: [('g002', 'GP', '', '->', 'chat', 'gold', 'chat'), ('s041', 'GP', '', '->', 'marche', 'gold', 'marche')]
  regs : []
  surface: {'changes': 3, 'dont_gold': 2, 'dont_hors_gold': 1}

== R1_repli_vide_tous_non_GV | exact {'justes': 139, 'n': 145, 'taux': 0.9586, 'gain': 2, 'regressions': 0, 'net': 2} | top1 {'justes': 142, 'n': 145, 'taux': 0.9793, 'gain': 2, 'regressions': 0, 'net': 2} | mcnemar 0.5
  gains: [('g002', 'GP', '', '->', 'chat', 'gold', 'chat'), ('s041', 'GP', '', '->', 'marche', 'gold', 'marche')]
  regs : []
  surface: {'changes': 114, 'dont_gold': 2, 'dont_hors_gold': 112}

== R1_dernier_temoin | exact {'justes': 137, 'n': 145, 'taux': 0.9448, 'gain': 0, 'regressions': 0, 'net': 0} | top1 {'justes': 141, 'n': 145, 'taux': 0.9724, 'gain': 1, 'regressions': 0, 'net': 1} | mcnemar 1.0
  gains: []
  regs : []
  surface: {'changes': 3, 'd
… [7702 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-replis-cible.json',encoding='utf-8'))\nfor nom in ['R2_preference_tete','R2_litterale','R2_litterale_lexique_etendu','combinaison','combinaison_R2_litterale','R3_completive_large']:\n    v=d['variantes'][nom]\n    print('== … [408 caractères tronqués]`

  ```
== R2_preference_tete changes 14 gold 4 hors 10
    r083 GP (9, 22) 'gare' -> 'train' | Le train entre en gare.
    r121 GP (20, 30) 'jardinier' -> 'plante' | Le jardinier plante des fleurs.
    r227 GP (0, 13) 'lit' -> 'dort' | Pendant qu'il dort, elle lit.
    r273 GP (20, 23) 'est' -> 'pousse' | La fleur qui pousse ici est rare.
    r324 GP (13, 25) 'est' -> 'livre' | Le livre est sur la table ; il est rouge.
    r336 GP (27, 33) 'her' -> 'speaks' | Paul sees Marie; he speaks to her.
    r342 GP (27, 33) 'her' -> 'speaks' | Paul sees Marie; he speaks to her; she listens.
    r349 GP (13, 25) 'est' -> 'livre' | Le livre est sur la table ; je le lis.
    r358 GP (27, 33) 'her' -> 'speaks' | Paul sees Marie; he speaks to her.
    r408 GP (16, 22) 'pas' -> 'viens-tu' | Ne viens-tu pas demain ?
== R2_litterale changes 3 gold 0 hors 3
    g002 GP (8, 26) 'chat' -> 'dort' | Le chat de la voisine dort.
    r083 GP (9, 22) 'gare' -> 'entre' | Le train entre en gare.
    r227 GP (0, 13) 'lit' -> 'dort' | Pendant qu'il dort, elle lit.
== R2_litterale_lexique_etendu changes 5 gold 2 hors 3
    g002 GP (8, 26) 'chat' -> 'dort' | Le chat de la voisine dort.
    r083 GP (9, 22) 'gare' -> 'entr
… [1468 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Test d'une forme étroite de R2 (moins de changements hors gold)

- **bash** `{"command": "cat > /tmp/test_r2_etroite.py <<'PY'\nimport sys, importlib.util, pathlib\nsys.dont_write_bytecode=True\nRACINE=pathlib.Path('/home/stephane/Data13TB/stephane/GitHub/Qtrinet')\nsys.path.insert(0,str(RACINE/'tools')); sys.path.insert(0,str(RACINE/'tools/tests/linguistique'))\nspec=import … [3055 caractères tronqués]`

  ```
dedans                       exact=141/145 top1=143/145 gains=0 regs=0 surface=1 (gold 0/hors 1)
   gains []
   hors [('r083', 'gare', '->', 'train')]
plus_proche                  exact=143/145 top1=143/145 gains=2 regs=0 surface=4 (gold 2/hors 2)
   gains [('s108', 'papier', '->', 'rêve'), ('s122', 'papier', '->', 'saute')]
   hors [('r121', 'jardinier', '->', 'plante'), ('r227', 'lit', '->', 'dort')]
dedans_ou_plus_proche        exact=143/145 top1=143/145 gains=2 regs=0 surface=5 (gold 2/hors 3)
   gains [('s108', 'papier', '->', 'rêve'), ('s122', 'papier', '->', 'saute')]
   hors [('r083', 'gare', '->', 'train'), ('r121', 'jardinier', '->', 'plante'), ('r227', 'lit', '->', 'dort')]
dedans_ou_nom_plus_proche    exact=141/145 top1=143/145 gains=0 regs=0 surface=1 (gold 0/hors 1)
   gains []
   hors [('r083', 'gare', '->', 'train')]
  ```

- **bash** `{"command": "sha256sum tools/bloc_linguistique.py; stat -c '%s %y' tools/bloc_linguistique.py; python3 - <<'PY'\nimport sys\nsys.dont_write_bytecode=True\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl\nfrom evaluer_gold import charger, eval … [288 caractères tronqués]`

  ```
64b7c5204f21e4c230dcd131469187f0c9789e06469f4e19af5f8819f87ab5fa  tools/bloc_linguistique.py
105381 2026-11-05 15:04:59.190598153 -0500
{'exact': 141, 'labels': 145, 'top1': 143, 'cibles': 239, 'topk_exact': 142}
  ```

### 🤖 Assistant

⏵ Le bloc a encore bougé (141/145) : nouvelle inspection du diff et des cas réparés

- **bash** `{"command": "git diff HEAD -- tools/bloc_linguistique.py | sed -n '1,220p'", "description": "Inspect latest accumulated diff", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
diff --git a/tools/bloc_linguistique.py b/tools/bloc_linguistique.py
index 07a41ec9..b171b5f2 100644
--- a/tools/bloc_linguistique.py
+++ b/tools/bloc_linguistique.py
@@ -428,9 +428,20 @@ am is are was were be been being have has had having do does did done
 """.split())
 
 
+ENCLITIQUES = ("-moi", "-toi", "-nous", "-vous", "-le", "-la", "-les", "-lui", "-leur", "-y", "-en")
+
+
+def _sans_enclitique(mot: str) -> str:
+    """`appelle-moi` → `appelle` (les enclitiques ne font pas partie de la tête)."""
+    for suf in ENCLITIQUES:
+        if mot.endswith(suf) and len(mot) > len(suf):
+            return mot[: -len(suf)]
+    return mot
+
+
 def _est_verbe(mot: str) -> bool:
     """Le mot est-il un verbe ? Lexique + désinences courantes (fr/en)."""
-    n = _normaliser(mot)
+    n = _normaliser(_sans_enclitique(mot))
     if not n:
         return False
     if n in VERBES_CONNUS:
@@ -616,6 +627,41 @@ class Heuristique:
         except Exception:
             return {}
 
+    @staticmethod
+    def _repli_cible_gp(texte: str, segment: dict, gns: list[dict]) -> str | None:
+        """Cible vide d'un GP : génitif → tête du GN à gauche (sinon None, le GV tranchera)."""
+        if s
… [5062 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Diagnostic du nouveau baseline 141/145 et des cas restants

- **bash** `{"command": "python3 - <<'PY'\nimport sys\nsys.dont_write_bytecode=True\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl\nfrom evaluer_gold import charger\nh=bl.Heuristique(); phrases=charger()\ndef cibles(s): return s.get('cibles') or ([s['c … [1209 caractères tronqués]`

  ```
n 145 exact 141 top1?
empties [('s041', 'GP', 'devant elles', ['marche', 'avocat'])]
fails
   ('r309', 'SUB', "qu'il viendra", ['viendra'], 'Peut-être')
   ('s041', 'GP', 'devant elles', ['marche', 'avocat'], '')
   ('s108', 'GP', 'sous le nuage', ['rêve', 'papier'], 'papier')
   ('s122', 'GP', 'vers les montagne', ['saute', 'papier'], 'papier')
key cases
== g002 Le chat de la voisine dort.
    GN (0, 7) 'Le chat' {'role': 'agent', 'niveau': 0}
    GP (8, 21) 'de la voisine' {'role': 'theme', 'niveau': 1, 'union': True, 'attachement': {'segment': 'de la voisine', 'cible': 'chat'}}
    GP (8, 26) 'de la voisine dort' {'role': 'possession', 'niveau': 1, 'attachement': {'segment': 'de la voisine dort', 'cible': 'chat'}}
== s041 les avocat marche devant elles
    GN (0, 17) 'les avocat marche' {'role': 'agent', 'niveau': 0}
    GP (18, 30) 'devant elles' {'role': 'lieu', 'niveau': 1, 'union': True}
    GN (25, 30) 'elles' {'role': 'agent', 'niveau': 1, 'attachement': {'segment': 'elles', 'cible': 'marche'}}
== g012 Le canard est prêt à manger.
    GN (0, 9) 'Le canard' {'role': 'agent', 'niveau': 1, 'attachement': {'segment': 'Le canard', 'cible': 'manger'}}
    GV (10, 18) 'est prêt' 
… [2461 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Alerte au parent sur la dérive du bloc et sauvegarde du snapshot A3 137

- **send_message** `{"agent_id": "e181ce02-cd50-488a-a6be-e84b79d40dcc", "message": "Point de situation (important pour la mesure) : `tools/bloc_linguistique.py` bouge en concurrence pendant ma session. Empreintes observées : 6e843018 (101 568 o, 13:51) → bb020516 (103 191 o, 15:03, baseline 137/145) → 64b7c520 (105 38 … [711 caractères tronqués]`

  ```
message delivered to agent e181ce02-cd50-488a-a6be-e84b79d40dcc
  ```

### 🤖 Assistant

⏵ Sauvegarde du snapshot 137 et ajout de la variante étroite de R2

- **bash** `{"command": "cp reports/pensee-replis-cible.json /tmp/pensee_replis_bb020516.json && python3 - <<'PY'\np='tools/tests/linguistique/replis_cible.py'\ns=open(p,encoding='utf-8').read()\n\n# 1) add R2 etroite branch\ns=s.replace('''                elif self.t2 in (\"litteral\", \"litteral_pos\"):''','' … [7094 caractères tronqués]`

  ```
patched
  ```

- **bash** `{"command": "grep -n \"note\\|protocole\\|limites\\|recommandation\\|controle_fidelite\\|R1_repli_vide_GP\\|R2_preference\" tools/tests/linguistique/replis_cible.py | head -40; sed -n '/variantes_principales =/,/^# --------------------------------------------------------------------------- CLI/p' to … [169 caractères tronqués]`

  ```
425:        {"nom": "R1_repli_vide_GP", "famille": "R1", "principal": True,
615:    cles = ("R1_repli_vide_GP", "R2_etroite", "R3_completive_etroite",
656:        "note": ("Prototype autonome : `bloc_linguistique.py` n'est pas modifié ; les "
659:        "protocole": {
668:            "controle_fidelite": "un run sans retouche redonne exactement 137/145 et "
689:        "limites": [
708:        "recommandation": {
    variantes_principales = {n: v for n, v in variantes.items() if v["principal"]}
    combo = variantes["combinaison"]
    empreinte_fin = _empreinte_bloc()
    return {
        "titre": "Trois retouches déterministes de l'attachement (replis de cible)",
        "date": "2026-11-05",
        "ligne_roadmap": "B13",
        "empreinte_bloc_linguistique": empreinte_debut,
        "empreinte_fin_de_run": empreinte_fin,
        "bloc_stable_pendant_le_run": (empreinte_debut["sha256_16"]
                                       == empreinte_fin["sha256_16"]),
        "note": ("Prototype autonome : `bloc_linguistique.py` n'est pas modifié ; les "
                 "retouches sont simulées par post-traitement des cibles. Le top-k et "
                 "les spans sont inchangés par
… [5055 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\np='tools/tests/linguistique/replis_cible.py'\ns=open(p,encoding='utf-8').read()\n\n# add no-op control at start of configurations\ns=s.replace('''    return [\n        {\"nom\": \"R1_repli_vide_GP\"''','''    return [\n        {\"nom\": \"temoin_noop\", \"famille\": \" … [12184 caractères tronqués]`

  ```
patched helpers
OK
  ```

- **bash** `{"command": "python3 - <<'PY'\np='tools/tests/linguistique/replis_cible.py'\ns=open(p,encoding='utf-8').read()\ns=s.replace('''def _recommandation(variantes: dict, base_att: dict) -> dict:''','''def _recommandation(variantes: dict, base_att: dict, base_mesures: dict) -> dict:''')\ns=s.replace('''    … [1501 caractères tronqués]`

  ```
patched
OK
64b7c5204f21e4c230dcd131469187f0c9789e06469f4e19af5f8819f87ab5fa  tools/bloc_linguistique.py
105381 2026-11-05 15:04:59.190598153 -0500
  ```

### 🤖 Assistant

⏵ Run complet sur l'empreinte live 64b7c520 (baseline 141/145)

- **bash** `{"command": "python3 tools/tests/linguistique/replis_cible.py", "description": "Run updated prototype on live bloc", "timeoutMs": 900000, "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
== base ==
bloc: {'fichier': 'tools/bloc_linguistique.py', 'sha256_16': '64b7c5204f21e4c2', 'octets': 105381, 'mtime': '2026-11-05T15:04:59'}
exact 141/145 (0.9724) | top1 143/145 (0.9862) | topk strict 142/239 | exact global 141/239 (0.5900)
== retouches ==
temoin_noop                      exact 141/145 (0.9724) Δ+0 top1 143/145 (0.9862) Δ+0 reg  0 | surface   0 (0 gold / 0 hors)
R1_repli_vide_GP                 exact 142/145 (0.9793) Δ+1 top1 144/145 (0.9931) Δ+1 reg  0 | surface   2 (1 gold / 1 hors)
R1_repli_vide_tous_non_GV        exact 142/145 (0.9793) Δ+1 top1 144/145 (0.9931) Δ+1 reg  0 | surface 113 (1 gold / 112 hors)
R1_dernier_temoin                exact 141/145 (0.9724) Δ+0 top1 144/145 (0.9931) Δ+1 reg  0 | surface   2 (1 gold / 1 hors)
R1_verbe_lexique_temoin          exact 141/145 (0.9724) Δ+0 top1 143/145 (0.9862) Δ+0 reg  0 | surface   0 (0 gold / 0 hors)
R2_litterale                     exact 138/145 (0.9517) Δ-3 top1 140/145 (0.9655) Δ-3 reg  3 | surface   6 (3 gold / 3 hors)
R2_litterale_POS                 exact 132/145 (0.9103) Δ-9 top1 134/145 (0.9241) Δ-9 reg  9 | surface  14 (9 gold / 5 hors)
R2_litterale_lexique_etendu      exact 140/145 (0.9655) Δ-1 top1
… [1574 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-replis-cible.json',encoding='utf-8'))\nprint('base', {k:d['base'][k] for k in ('exact','labels','top1','topk_exact')})\nfor nom in ['R1_repli_vide_GP','R2_etroite','R2_large','R3_completive_etroite','combinaison','combinais … [840 caractères tronqués]`

  ```
base {'exact': 141, 'labels': 145, 'top1': 143, 'topk_exact': 142}

== R1_repli_vide_GP exact {'justes': 142, 'n': 145, 'taux': 0.9793, 'gain': 1, 'regressions': 0, 'net': 1} | top1 {'justes': 144, 'n': 145, 'taux': 0.9931, 'gain': 1, 'regressions': 0, 'net': 1}
 gains [('s041', 'GP', '', '->', 'marche', 'marche')]
 regs  []
 surface {'changes': 2, 'dont_gold': 1, 'dont_hors_gold': 1}
 hors [('s027', 'GP', '', '->', 'marche')]

== R2_etroite exact {'justes': 143, 'n': 145, 'taux': 0.9862, 'gain': 2, 'regressions': 0, 'net': 2} | top1 {'justes': 143, 'n': 145, 'taux': 0.9862, 'gain': 0, 'regressions': 0, 'net': 0}
 gains [('s108', 'GP', 'papier', '->', 'rêve', 'rêve'), ('s122', 'GP', 'papier', '->', 'saute', 'saute')]
 regs  []
 surface {'changes': 4, 'dont_gold': 2, 'dont_hors_gold': 2}
 hors [('r121', 'GP', 'jardinier', '->', 'plante'), ('r227', 'GP', 'lit', '->', 'dort')]

== R2_large exact {'justes': 143, 'n': 145, 'taux': 0.9862, 'gain': 2, 'regressions': 0, 'net': 2} | top1 {'justes': 143, 'n': 145, 'taux': 0.9862, 'gain': 0, 'regressions': 0, 'net': 0}
 gains [('s108', 'GP', 'papier', '->', 'rêve', 'rêve'), ('s122', 'GP', 'papier', '->', 'saute', 'saute')]
 regs  []
 surface 
… [4041 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys\nsys.dont_write_bytecode=True\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nfor w in ['appelle','appelle-moi','Peut-être','viendra','arrives']:\n    print(w,'est_verbe',bl._est_verbe(w),'norm',bl._normaliser(w),'dans VERBES',bl._normaliser(w)  … [142 caractères tronqués]`

  ```
appelle est_verbe False norm appelle dans VERBES False
appelle-moi est_verbe False norm appelle-moi dans VERBES False
Peut-être est_verbe False norm peut-être dans VERBES False
viendra est_verbe False norm viendra dans VERBES False
arrives est_verbe True norm arrives dans VERBES True
  ```

### 🤖 Assistant

⏵ Correction de R3 : distinguer la complétive en tête du cas enclitique r230

- **bash** `{"command": "python3 - <<'PY'\np='tools/tests/linguistique/replis_cible.py'\ns=open(p,encoding='utf-8').read()\ns=s.replace('''    def _appliquer(self, annotation, texte: str) -> None:\n        for etiquette in annotation.etiquettes:''','''    def _appliquer(self, annotation, texte: str) -> None:\n  … [1325 caractères tronqués]`

  ```
patched R3
OK
64b7c5204f21e4c230dcd131469187f0c9789e06469f4e19af5f8819f87ab5fa  tools/bloc_linguistique.py
  ```

### 🤖 Assistant

⏵ Run de validation après correction de R3

- **bash** `{"command": "python3 tools/tests/linguistique/replis_cible.py", "description": "Rerun prototype after R3 fix", "timeoutMs": 900000, "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
== base ==
bloc: {'fichier': 'tools/bloc_linguistique.py', 'sha256_16': '64b7c5204f21e4c2', 'octets': 105381, 'mtime': '2026-11-05T15:04:59'}
exact 141/145 (0.9724) | top1 143/145 (0.9862) | topk strict 142/239 | exact global 141/239 (0.5900)
== retouches ==
temoin_noop                      exact 141/145 (0.9724) Δ+0 top1 143/145 (0.9862) Δ+0 reg  0 | surface   0 (0 gold / 0 hors)
R1_repli_vide_GP                 exact 142/145 (0.9793) Δ+1 top1 144/145 (0.9931) Δ+1 reg  0 | surface   2 (1 gold / 1 hors)
R1_repli_vide_tous_non_GV        exact 142/145 (0.9793) Δ+1 top1 144/145 (0.9931) Δ+1 reg  0 | surface 113 (1 gold / 112 hors)
R1_dernier_temoin                exact 141/145 (0.9724) Δ+0 top1 144/145 (0.9931) Δ+1 reg  0 | surface   2 (1 gold / 1 hors)
R1_verbe_lexique_temoin          exact 141/145 (0.9724) Δ+0 top1 143/145 (0.9862) Δ+0 reg  0 | surface   0 (0 gold / 0 hors)
R2_litterale                     exact 138/145 (0.9517) Δ-3 top1 140/145 (0.9655) Δ-3 reg  3 | surface   6 (3 gold / 3 hors)
R2_litterale_POS                 exact 132/145 (0.9103) Δ-9 top1 134/145 (0.9241) Δ-9 reg  9 | surface  14 (9 gold / 5 hors)
R2_litterale_lexique_etendu      exact 140/145 (0.9655) Δ-1 top1
… [1574 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification du JSON final (recommandation, dérive, contrôles)

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-replis-cible.json',encoding='utf-8'))\nprint('stable:',d['bloc_stable_pendant_le_run'],'| start',d['empreinte_bloc_linguistique']['sha256_16'],'| end',d['empreinte_fin_de_run']['sha256_16'])\nprint('keys:',list(d.keys()))\n … [671 caractères tronqués]`

  ```
stable: True | start 64b7c5204f21e4c2 | end 64b7c5204f21e4c2
keys: ['titre', 'date', 'ligne_roadmap', 'empreinte_bloc_linguistique', 'empreinte_fin_de_run', 'bloc_stable_pendant_le_run', 'note', 'protocole', 'corpus', 'base', 'etat_des_lieux', 'derive_du_bloc', 'retouches', 'variantes', 'principales', 'combinaison', 'segments_145', 'limites', 'recommandation']

PROTOCOLE:
  population : 612 phrases ; 239 segments gold porteurs d'une cible ; 145 dont le span (type, debut, fin) est prédit
  mesure : égalité exacte avec cibles[0] et top1 de evaluer_gold (sous-chaîne d'une des cibles), sur 145 (span) et 239 (global)
  vivier : tokens pleins (POS ouverte ou _est_verbe), auxiliaires exclus ; gauche → droite → dedans, puis distance
  simulation : sous-classe de Heuristique + post-traitement de meta.attachement.cible ; aucun autre champ modifié
  controle_fidelite : le témoin no-op redonne exactement 141/145 exact et 143/145 top1 (vérifié avant chaque variante)
  regression : segment exact avant → faux après ; le gain net = gains - régressions
  mcnemar : exact bilatéral sur les paires discordantes (descriptif : les cas ont servi à définir les règles)

DERIVE:
{
 "empreinte_mesuree": {
  "
… [7704 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/pensee_replis_bb020516.json',encoding='utf-8'))\nprint('base',{k:d['base'][k] for k in ('exact','labels','top1','topk_exact')})\nfor nom in ['R1_repli_vide_GP','R2_preference_tete','R3_completive_etroite','combinaison']:\n    v=d['va … [584 caractères tronqués]`

  ```
base {'exact': 137, 'labels': 145, 'top1': 140, 'topk_exact': 141}
R1_repli_vide_GP exact {'justes': 139, 'n': 145, 'taux': 0.9586, 'gain': 2, 'regressions': 0, 'net': 2} top1 {'justes': 142, 'n': 145, 'taux': 0.9793, 'gain': 2, 'regressions': 0, 'net': 2} surface 3 2 1
  gains [('g002', '', '->', 'chat'), ('s041', '', '->', 'marche')]
  regs  []
R2_preference_tete exact {'justes': 141, 'n': 145, 'taux': 0.9724, 'gain': 4, 'regressions': 0, 'net': 4} top1 {'justes': 142, 'n': 145, 'taux': 0.9793, 'gain': 2, 'regressions': 0, 'net': 2} surface 14 4 10
  gains [('g012', 'manger', '->', 'prêt'), ('r018', 'manger', '->', 'prête'), ('s108', 'papier', '->', 'rêve'), ('s122', 'papier', '->', 'saute')]
  regs  []
R3_completive_etroite exact {'justes': 138, 'n': 145, 'taux': 0.9517, 'gain': 1, 'regressions': 0, 'net': 1} top1 {'justes': 141, 'n': 145, 'taux': 0.9724, 'gain': 1, 'regressions': 0, 'net': 1} surface 1 1 0
  gains [('r309', 'Peut-être', '->', 'viendra')]
  regs  []
combinaison exact {'justes': 144, 'n': 145, 'taux': 0.9931, 'gain': 7, 'regressions': 0, 'net': 7} top1 {'justes': 145, 'n': 145, 'taux': 1.0, 'gain': 5, 'regressions': 0, 'net': 5} surface 18 7 11
  gains [('g002', 
… [598 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Nettoyage des textes et ajout du snapshot A3 137 au JSON

- **bash** `{"command": "python3 - <<'PY'\np='tools/tests/linguistique/replis_cible.py'\ns=open(p,encoding='utf-8').read()\n\n# docstring stale sentence\ns=s.replace('''Ce que le banc ne fait pas. Il ne touche ni au span, ni au vivier de `candidats` (le top-k\nreste donc inchangé), ni au lexique. Il simule la * … [5422 caractères tronqués]`

  ```
patched
OK
  ```

- **bash** `{"command": "sha256sum tools/bloc_linguistique.py; stat -c '%s %y' tools/bloc_linguistique.py; python3 tools/tests/linguistique/replis_cible.py", "description": "Regenerate final JSON with snapshot", "timeoutMs": 900000, "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
64b7c5204f21e4c230dcd131469187f0c9789e06469f4e19af5f8819f87ab5fa  tools/bloc_linguistique.py
105381 2026-11-05 15:04:59.190598153 -0500
== base ==
bloc: {'fichier': 'tools/bloc_linguistique.py', 'sha256_16': '64b7c5204f21e4c2', 'octets': 105381, 'mtime': '2026-11-05T15:04:59'}
exact 141/145 (0.9724) | top1 143/145 (0.9862) | topk strict 142/239 | exact global 141/239 (0.5900)
== retouches ==
temoin_noop                      exact 141/145 (0.9724) Δ+0 top1 143/145 (0.9862) Δ+0 reg  0 | surface   0 (0 gold / 0 hors)
R1_repli_vide_GP                 exact 142/145 (0.9793) Δ+1 top1 144/145 (0.9931) Δ+1 reg  0 | surface   2 (1 gold / 1 hors)
R1_repli_vide_tous_non_GV        exact 142/145 (0.9793) Δ+1 top1 144/145 (0.9931) Δ+1 reg  0 | surface 113 (1 gold / 112 hors)
R1_dernier_temoin                exact 141/145 (0.9724) Δ+0 top1 144/145 (0.9931) Δ+1 reg  0 | surface   2 (1 gold / 1 hors)
R1_verbe_lexique_temoin          exact 141/145 (0.9724) Δ+0 top1 143/145 (0.9862) Δ+0 reg  0 | surface   0 (0 gold / 0 hors)
R2_litterale                     exact 138/145 (0.9517) Δ-3 top1 140/145 (0.9655) Δ-3 reg  3 | surface   6 (3 gold / 3 hors)
R2_litterale_POS                 exact 132/145 (0.910
… [1710 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json, os\np='reports/pensee-replis-cible.json'\nd=json.load(open(p,encoding='utf-8'))\nprint('size',os.path.getsize(p),'bytes')\nprint('stable',d['bloc_stable_pendant_le_run'])\nprint('snapshot:',json.dumps(d['snapshot_a3_137'],ensure_ascii=False,indent=1)[:2500 … [418 caractères tronqués]`

  ```
size 269963 bytes
stable True
snapshot: {
 "empreinte": "bb020516",
 "octets": 103191,
 "mtime": "2026-11-05T15:03:12",
 "note": "mesure intermédiaire de ce prototype, avant l'intégration live ; baseline 137 = les 8 erreurs de la fiche A3. R2 y est la forme large (rang 0 gardé), R3 la forme étroite.",
 "baseline": {
  "exact_145": 137,
  "top1_145": 140,
  "topk_exact": 141,
  "cibles": 239
 },
 "erreurs_baseline": [
  "g002",
  "g012",
  "r018",
  "r230",
  "r309",
  "s041",
  "s108",
  "s122"
 ],
 "R1": {
  "gain": 2,
  "regressions": 0,
  "net": 2,
  "gains": [
   "g002",
   "s041"
  ],
  "surface": {
   "changes": 3,
   "dont_gold": 2,
   "dont_hors_gold": 1
  }
 },
 "R2_large": {
  "gain": 4,
  "regressions": 0,
  "net": 4,
  "gains": [
   "g012",
   "r018",
   "s108",
   "s122"
  ],
  "surface": {
   "changes": 14,
   "dont_gold": 4,
   "dont_hors_gold": 10
  }
 },
 "R3": {
  "gain": 1,
  "regressions": 0,
  "net": 1,
  "gains": [
   "r309"
  ],
  "surface": {
   "changes": 1,
   "dont_gold": 1,
   "dont_hors_gold": 0
  }
 },
 "combinaison": {
  "gain": 7,
  "regressions": 0,
  "net": 7,
  "exact_145": "144/145 (0,9931)",
  "top1_145": "145/145 (1,0000)",
  "gains": [
   "g00
… [2414 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Extraction des listes finales (gains, régressions, contrôles) pour la fiche

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-replis-cible.json',encoding='utf-8'))\ndef show(nom):\n    v=d['variantes'][nom]\n    print('\\n==',nom,'|',v['definition'])\n    print(' exact',v['detail']['exact_145'],'| top1',v['detail']['top1_145'],'| mcnemar',v['mcnem … [1009 caractères tronqués]`

  ```
== temoin_noop | témoin de fidélité : aucune retouche
 exact {'justes': 141, 'n': 145, 'taux': 0.9724, 'gain': 0, 'regressions': 0, 'net': 0} | top1 {'justes': 143, 'n': 145, 'taux': 0.9862, 'gain': 0, 'regressions': 0, 'net': 0} | mcnemar 1.0
 gains []
 regs  []
 surface 0 gold 0 hors 0 par type {}

== R1_repli_vide_GP | cible vide sur un GP → rang 0 du vivier (gauche d'abord)
 exact {'justes': 142, 'n': 145, 'taux': 0.9793, 'gain': 1, 'regressions': 0, 'net': 1} | top1 {'justes': 144, 'n': 145, 'taux': 0.9931, 'gain': 1, 'regressions': 0, 'net': 1} | mcnemar 1.0
 gains [('s041', 'GP', "''", '->', "'marche'", 'gold', 'marche')]
 regs  []
 surface 2 gold 1 hors 1 par type {'GP': 2}

== R1_repli_vide_tous_non_GV | même repli sur tous les types non-GV (surface large)
 exact {'justes': 142, 'n': 145, 'taux': 0.9793, 'gain': 1, 'regressions': 0, 'net': 1} | top1 {'justes': 144, 'n': 145, 'taux': 0.9931, 'gain': 1, 'regressions': 0, 'net': 1} | mcnemar 1.0
 gains [('s041', 'GP', "''", '->', "'marche'", 'gold', 'marche')]
 regs  []
 surface 113 gold 1 hors 112 par type {'GN': 111, 'GP': 2}

== R1_dernier_temoin | témoin : dernier candidat au lieu du rang 0
 exact {'justes': 141, 'n': 145
… [10007 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-replis-cible.json',encoding='utf-8'))\ne=d['etat_des_lieux']\nprint('par_type_239',json.dumps(e['par_type_239'],ensure_ascii=False))\nprint('absents',e['spans_non_predits']['total'],{k:len(v) for k,v in e['spans_non_predits … [352 caractères tronqués]`

  ```
par_type_239 {"GP": {"cibles": 96, "spans_predits": 83, "vides": 1, "absents": 13}, "REL": {"cibles": 74, "spans_predits": 26, "vides": 0, "absents": 48}, "SUB": {"cibles": 69, "spans_predits": 36, "vides": 0, "absents": 33}}
absents 94 {'GP': 13, 'REL': 48, 'SUB': 33}
GP g006, g020, r028, r038, r060, r083, r102, r153, r162, s027, s146, s148, s160
REL r034, r035, r074, r075, r114, r115, r204, r206, r214, r217, r220, r224, r236, r239, r241, r243, r246, r248, r250, r255, r273, r278, r280, r283, r285, r287, r289, r291, r293, r297, r299, r300, s010, s032, s035, s037, s050, s061, s065, s069, s070, s072, s075, s115, s125, s131, s135, s141
SUB g017, r205, r215, r216, r218, r219, r237, r238, r240, r242, r244, r245, r247, r249, r264, r279, r281, r282, r284, r286, r288, r290, r292, r294, r296, r298, r303, r313, s015, s044, s112, s114, s132
vides {'total': 1, 'liste': [{'id': 's041', 'type': 'GP', 'segment': 'devant elles', 'gold': 'marche', 'gold_all': ['marche', 'avocat']}]}
cross {'autre→verbe': 1, 'nom→nom': 29, 'nom→verbe': 2, 'verbe→verbe': 112, 'vide→verbe': 1}
top1only [{'id': 's108', 'type': 'GP', 'segment': 'sous le nuage', 'cible': 'papier', 'gold_all': ['rêve', 'papier']}, {'id': 
… [106 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Rédaction de la fiche `reports/rapport-replis-cible.md`

- **write** `{"content": "# B13 — les trois retouches A3 sur le live : +1, +2, +1, et 145/145 exact/top1\n\n> **Ligne de roadmap** : **B13** (moteur de pensée, attachement) · **Date** : 2026-11-05 · **Verdict** : ✅ **R1 (repli cible vide, GP)** et **R3 (complétive en tête, SUB)** à intégrer ; ⚠️ **R2** : ❌ sous  … [15301 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-replis-cible.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

### 🤖 Assistant

⏵ Contrôle final des fichiers, de l'état git et de la reproductibilité

- **bash** `{"command": "git status --porcelain | grep -E 'replis_cible|rapport-replis-cible|pensee-replis-cible|bloc_linguistique|__pycache__' || true; echo '---'; ls -l tools/tests/linguistique/replis_cible.py reports/rapport-replis-cible.md reports/pensee-replis-cible.json; echo '---'; sha256sum tools/bloc_l … [144 caractères tronqués]`

  ```
M  tools/bloc_linguistique.py
?? reports/pensee-replis-cible.json
?? reports/rapport-replis-cible.md
?? tools/tests/linguistique/replis_cible.py
---
-rw-r--r--. 1 stephane stephane 269963  5 nov 15:21 reports/pensee-replis-cible.json
-rw-------. 1 stephane stephane  15755  5 nov 15:28 reports/rapport-replis-cible.md
-rw-------. 1 stephane stephane  48559  5 nov 15:20 tools/tests/linguistique/replis_cible.py
---
9da6dee7118cfa576d159ccdf5d1241232e974544cd3a6c5cebaddcbbaccd059  tools/bloc_linguistique.py
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys, json\nsys.dont_write_bytecode=True\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport replis_cible as rc\nprint('module importable, fonctions:', [f for f in ('executer','HeuristiqueReplis','main') if hasattr(rc,f)])\nd=json.l … [540 caractères tronqués]`

  ```
module importable, fonctions: ['executer', 'HeuristiqueReplis', 'main']
base 141 145 143 142
R1_repli_vide_GP 142 144 1 0
R2_etroite 143 143 2 0
R3_completive_etroite 142 144 1 0
combinaison 145 145 4 0
  ```

### 🤖 Assistant

⏵ Le bloc a rebougé (9da6dee7) : vérification de l'impact avant de figer

- **bash** `{"command": "sha256sum tools/bloc_linguistique.py; stat -c '%s %y' tools/bloc_linguistique.py; git diff HEAD -- tools/bloc_linguistique.py | sed -n '1,260p'", "description": "Inspect newest bloc diff", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
9da6dee7118cfa576d159ccdf5d1241232e974544cd3a6c5cebaddcbbaccd059  tools/bloc_linguistique.py
105156 2026-11-05 15:22:00.127553628 -0500
diff --git a/tools/bloc_linguistique.py b/tools/bloc_linguistique.py
index b171b5f2..8d0ca1f8 100644
--- a/tools/bloc_linguistique.py
+++ b/tools/bloc_linguistique.py
@@ -922,10 +922,11 @@ class Heuristique:
         cands = self._syntagmes_s(texte)
         cibles_s = self._cibles_s(texte) if cands else {}
         cache_gv: dict = {}  # un GV n'est analysé qu'une fois par analyse
+        # **un seul chunking par analyse**, partagé par les trois chemins (S, union, chunker) :
+        # le O(n²) mesuré venait des re-chunkings (A6, A11) — sortie identique (T178).
+        simples = self._syntagmes_simple(texte, lg)
+        gvs_simple = [x for x in simples if x["type"] == "GV"]
         if cands:
-            # les GV du chunker complètent ceux du générateur S : sans eux, un GP n'a aucun
-            # candidat d'attachement (diagnostic des 33 échecs de T162).
-            gvs_simple = [x for x in self._syntagmes_simple(texte, lg) if x["type"] == "GV"]
             for c in cands[:1]:
                 noms = [x.get("nom", "") for x in cands]
      
… [1238 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys\nsys.dont_write_bytecode=True\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl\nfrom evaluer_gold import charger, evaluer_bloc\ne=evaluer_bloc('h',bl.Heuristique(),charger())\nprint({k:e['attachement' … [214 caractères tronqués]`

  ```
{'exact': 141, 'labels': 145, 'top1': 143, 'cibles': 239, 'topk_exact': 142, 'exact_taux_span': 0.9724, 'top1_taux_span': 0.9862}
  ```

### 🤖 Assistant

⏵ Re-run sur l'empreinte 9da6dee7 (refactor de cache, sortie annoncée identique)

- **bash** `{"command": "python3 tools/tests/linguistique/replis_cible.py 2>&1 | tail -30; echo '---'; sha256sum tools/bloc_linguistique.py", "description": "Rerun final simulation on newest bloc", "timeoutMs": 900000, "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
== base ==
bloc: {'fichier': 'tools/bloc_linguistique.py', 'sha256_16': '9da6dee7118cfa57', 'octets': 105156, 'mtime': '2026-11-05T15:22:00'}
exact 141/145 (0.9724) | top1 143/145 (0.9862) | topk strict 142/239 | exact global 141/239 (0.5900)
== retouches ==
temoin_noop                      exact 141/145 (0.9724) Δ+0 top1 143/145 (0.9862) Δ+0 reg  0 | surface   0 (0 gold / 0 hors)
R1_repli_vide_GP                 exact 142/145 (0.9793) Δ+1 top1 144/145 (0.9931) Δ+1 reg  0 | surface   2 (1 gold / 1 hors)
R1_repli_vide_tous_non_GV        exact 142/145 (0.9793) Δ+1 top1 144/145 (0.9931) Δ+1 reg  0 | surface 113 (1 gold / 112 hors)
R1_dernier_temoin                exact 141/145 (0.9724) Δ+0 top1 144/145 (0.9931) Δ+1 reg  0 | surface   2 (1 gold / 1 hors)
R1_verbe_lexique_temoin          exact 141/145 (0.9724) Δ+0 top1 143/145 (0.9862) Δ+0 reg  0 | surface   0 (0 gold / 0 hors)
R2_litterale                     exact 138/145 (0.9517) Δ-3 top1 140/145 (0.9655) Δ-3 reg  3 | surface   6 (3 gold / 3 hors)
R2_litterale_POS                 exact 132/145 (0.9103) Δ-9 top1 134/145 (0.9241) Δ-9 reg  9 | surface  14 (9 gold / 5 hors)
R2_litterale_lexique_etendu      exact 140/145 (0.9655) Δ-1 top1
… [1671 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Mise à jour de l'empreinte finale (9da6dee7) et de l'historique de dérive

- **bash** `{"command": "python3 - <<'PY'\np='tools/tests/linguistique/replis_cible.py'\ns=open(p,encoding='utf-8').read()\ns=s.replace('''                {\"empreinte\": \"bb020516\", \"octets\": 103191,\n                 \"mtime\": \"2026-11-05T15:03:12\", \"baseline_exact\": 137,\n                 \"retouche … [2013 caractères tronqués]`

  ```
patched
3:> **Ligne de roadmap** : **B13** (moteur de pensée, attachement) · **Date** : 2026-11-05 · **Verdict** : ✅ **R1 (repli cible vide, GP)** et **R3 (complétive en tête, SUB)** à intégrer ; ⚠️ **R2** : ❌ sous sa forme littérale (« préférer un verbe »), ✅ sous sa forme **étroite** (« tête la plus proche »), qui répare les mêmes cas. Sur l'empreinte live `9da6dee7`, les trois valent **+4 net, 0 régression** et amènent à **145/145 exact (1,0000)** et **145/145 top1** ; sur les **239 cibles** : **145/239 (0,6067)**, plafond des 94 spans non prédits. Sur le baseline A3 `bb020516` (137/145), les mêmes retouches valaient **+2/+4/+1 = +7** (144/145, top1 145/145) : le live a déjà absorbé `g002`, `g012`/`r018` et `r230`.
5:> **Dispositif** : [`replis_cible.py`](../tools/tests/linguistique/replis_cible.py), JSON [`pensee-replis-cible.json`](pensee-replis-cible.json). [`bloc_linguistique.py`](../tools/bloc_linguistique.py) **non modifié** ; son empreinte est figée dans le JSON (`9da6dee7`, 105 156 octets, 15:22:00). Le bloc a bougé pendant la session (`6e843018` → `bb020516` → `9da6dee7`) : les chiffres sont une photo de la dernière empreinte, stable pendant le run.
13:- **Dérive** : le
… [580 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\np='reports/rapport-replis-cible.md'\nr=open(p,encoding='utf-8').read()\nr=r.replace('(`6e843018` → `bb020516` → `9da6dee7`)', '(`6e843018` → `bb020516` → `64b7c520` → `9da6dee7`)')\nr=r.replace('`6e843018` → `bb020516` → `9da6dee7` pendant la session', '`6e843018` → `b … [219 caractères tronqués]`

  ```
5:> **Dispositif** : [`replis_cible.py`](../tools/tests/linguistique/replis_cible.py), JSON [`pensee-replis-cible.json`](pensee-replis-cible.json). [`bloc_linguistique.py`](../tools/bloc_linguistique.py) **non modifié** ; son empreinte est figée dans le JSON (`9da6dee7`, 105 156 octets, 15:22:00). Le bloc a bougé pendant la session (`6e843018` → `bb020516` → `64b7c520` → `9da6dee7`) : les chiffres sont une photo de la dernière empreinte, stable pendant le run.
135:- **Le bloc bouge** : `6e843018` → `bb020516` → `64b7c520` → `9da6dee7` pendant la session ; si le worktree change encore, relancer le prototype. Le JSON fige l'empreinte et `bloc_stable_pendant_le_run=true`.
  ```

### 🤖 Assistant

⏵ Run final de régénération du JSON (empreinte courante + historique complet)

- **bash** `{"command": "sha256sum tools/bloc_linguistique.py; python3 tools/tests/linguistique/replis_cible.py >/tmp/final_run.log 2>&1; tail -8 /tmp/final_run.log; echo '---'; sha256sum tools/bloc_linguistique.py; python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-replis-cible.json',encoding='utf … [577 caractères tronqués]`

  ```
9da6dee7118cfa576d159ccdf5d1241232e974544cd3a6c5cebaddcbbaccd059  tools/bloc_linguistique.py
== état des lieux ==
239 cibles : 145 spans prédits, 94 absents, 1 vides au span prédit, 144 remplis
croisement nature: {'autre→verbe': 1, 'nom→nom': 29, 'nom→verbe': 2, 'verbe→verbe': 112, 'vide→verbe': 1}
nom→verbe: [('s108', 'papier', 'rêve'), ('s122', 'papier', 'saute')]
verbe→non-verbe: []
== combinaison ==
exact 145/145 (1.0000) | top1 145/145 (1.0000) | global exact 145/239 (0.6067) | top1 145/239 (0.6067)
JSON -> /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-replis-cible.json
---
9da6dee7118cfa576d159ccdf5d1241232e974544cd3a6c5cebaddcbbaccd059  tools/bloc_linguistique.py
fingerprint 9da6dee7118cfa57 105156 2026-11-05T15:22:00
stable True
history ['6e843018', 'bb020516', '64b7c520']
base 141 143 combo {'justes': 145, 'n': 145, 'taux': 1.0, 'gain': 4, 'regressions': 0, 'net': 4} {'justes': 145, 'n': 145, 'taux': 1.0, 'gain': 2, 'regressions': 0, 'net': 2}
  ```

### 🤖 Assistant

⏵ Contrôle croisé fiche ↔ JSON (annexe, tableaux, chiffres clés)

- **bash** `{"command": "python3 - <<'PY'\nimport json, re, pathlib\nmd=pathlib.Path('reports/rapport-replis-cible.md').read_text(encoding='utf-8')\nd=json.load(open('reports/pensee-replis-cible.json',encoding='utf-8'))\n# extract appendix ids\nannexe=md.split('## Annexe')[1]\nids=re.findall(r'`([a-z]\\d{3})`', … [840 caractères tronqués]`

  ```
ids annexe 94 uniques 94
ids json 94 uniques 94
manquants []
en trop []
141/145 1
143/145 1
145/145 8
145/239 4
142/145 1
144/145 3
0,6067 2
0,9931 2
+4 net 1
+7 3
ok R2_preference_tete
ok +7 du combiné
ok 137/145 exact et 140/145
ok 4 étiquettes changées (2 gold / 2 hors)
  ```

### 🤖 Assistant

⏵ Relecture finale de la fiche avant transmission

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-replis-cible.md", "limit": 120}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-replis-cible.md</path>
<type>file</type>
<content>
1: # B13 — les trois retouches A3 sur le live : +1, +2, +1, et 145/145 exact/top1
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, attachement) · **Date** : 2026-11-05 · **Verdict** : ✅ **R1 (repli cible vide, GP)** et **R3 (complétive en tête, SUB)** à intégrer ; ⚠️ **R2** : ❌ sous sa forme littérale (« préférer un verbe »), ✅ sous sa forme **étroite** (« tête la plus proche »), qui répare les mêmes cas. Sur l'empreinte live `9da6dee7`, les trois valent **+4 net, 0 régression** et amènent à **145/145 exact (1,0000)** et **145/145 top1** ; sur les **239 cibles** : **145/239 (0,6067)**, plafond des 94 spans non prédits. Sur le baseline A3 `bb020516` (137/145), les mêmes retouches valaient **+2/+4/+1 = +7** (144/145, top1 145/145) : le live a déjà absorbé `g002`, `g012`/`r018` et `r230`.
4: >
5: > **Dispositif** : [`replis_cible.py`](../tools/tests/linguistique/replis_cible.py), JSON [`pensee-replis-cible.json`](pensee-replis-cible.json). [`bloc_linguistique.py`](../tools/bloc_linguistique.py) **non modifié** ; son empreinte est figée dans le JSON (`9da6d
… [9972 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-replis-cible.md", "offset": 120}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-replis-cible.md</path>
<type>file</type>
<content>
120: | R2 littérale | 138 | -3 | 3 | 6 | défait `g002`/`g012`/`r018` |
121: | R2 littérale + lexique | 140 | -1 | 3 | 8 | +2 `s108`/`s122` mais 3 régressions |
122: | R2 POS | 132 | -9 | 9 | 14 | le POS n'est pas un détecteur de verbe sûr |
123: | R2 large | 143 | +2 | 0 | 12 | même gain que l'étroite, 10 changements hors gold |
124: | R3 large | 109 | -32 | 33 | 36 | toute complétive → intérieur : catastrophe |
125: | rang 0 partout (A3 §7.1) | 139 | -2 | 6 | 470 | `g003`, `g014`, `g016`, `r048`, `r068`, `r230` ; 460 changements hors gold |
126: | combiné R2 large | 145 | +4 | 0 | 15 | 11 hors gold |
127: | combiné R2 littérale | 140 | -1 | 3 | 9 | interaction : `g002` perdu |
128: 
129: Lecture : les gains viennent du **scope** et des **gardes**, pas d'une règle générique « verbe » ou « rang 0 ».
130: 
131: ## 8. Ce qui pourrait rendre cette fiche fausse
132: 
133: - **145 segments, 4 gains marginaux** : les règles ont été dessinées sur les cas réparés (HARKing) ; aucun gold tenu à l'écart. Le +4 est une **borne haute**, pas une estimation.
134: - **Simulation 
… [4104 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification finale : aucun import externe, fichiers neufs uniquement, JSON stable

- **bash** `{"command": "grep -R \"replis_cible\\|pensee-replis-cible\" --exclude-dir=.git --exclude-dir=__pycache__ -l . | sort; echo '---'; git status --porcelain | grep -E 'replis_cible|rapport-replis-cible|pensee-replis-cible'; echo '---'; python3 -m py_compile tools/tests/linguistique/replis_cible.py && ec … [321 caractères tronqués]`

  ```
[still running after 60000ms; moved to background job bash-1491]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **job_kill** `{"job_id": "bash-1491", "reason": "Recherche récursive trop lente sur les données ; vérifications ciblées suffisantes"}`

  ```
requested cancellation of job bash-1491
  ```

- **bash** `{"command": "grep -R \"replis_cible\" tools reports --exclude-dir=__pycache__ -l; echo '---'; git status --porcelain | grep -E 'replis_cible|rapport-replis-cible|pensee-replis-cible'; echo '---'; python3 -m py_compile tools/tests/linguistique/replis_cible.py && echo 'compile ok'; python3 -c \"import … [304 caractères tronqués]`

  ```
tools/tests/linguistique/replis_cible.py
reports/rapport-replis-cible.md
---
?? reports/pensee-replis-cible.json
?? reports/rapport-replis-cible.md
?? tools/tests/linguistique/replis_cible.py
---
compile ok
json ok True 9da6dee7118cfa57
  ```

- **bash** `{"command": "ls -l tools/tests/linguistique/__pycache__/ 2>/dev/null | grep replis || true; pwd", "description": "Locate pyc artifact from compile check", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
-rw-------. 1 stephane stephane  54532  5 nov 15:36 replis_cible.cpython-313.pyc
/home/stephane/Data13TB/stephane/GitHub/Qtrinet
  ```

- **bash** `{"command": "target=\"$(realpath tools/tests/linguistique/__pycache__/replis_cible.cpython-313.pyc)\"; echo \"$target\"; case \"$target\" in /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/__pycache__/replis_cible.cpython-313.pyc) rm -f \"$target\" && echo removed;; *) echo  … [250 caractères tronqués]`

  ```
/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/__pycache__/replis_cible.cpython-313.pyc
removed
no replis pyc left
  ```

### 🤖 Assistant

⏵ Transmission du résultat final au parent

- **send_message** `{"agent_id": "e181ce02-cd50-488a-a6be-e84b79d40dcc", "message": "Mission terminée — 3 fichiers neufs, aucun fichier existant modifié, aucun commit :\n- tools/tests/linguistique/replis_cible.py (prototype autonome, non importé)\n- reports/rapport-replis-cible.md (fiche)\n- reports/pensee-replis-cible … [2111 caractères tronqués]`

  ```
message delivered to agent e181ce02-cd50-488a-a6be-e84b79d40dcc
  ```

- **job_list** `{}`

  ```
bash-1491 [bash] killed — grep -R "replis_cible\|pensee-replis-cible" --exclude-dir=.git --exclude-dir=__pycache__ -l . | sort; echo '---'; git status --porcelain | grep -E 'replis_cible|rapport-replis-cible|pensee-replis-cible'; echo '---'; python3 -m py_compile tools/tests/linguistique/replis_cible.py && echo 'compile ok'; python3 -c "import json; d=json.load(open('reports/pensee-replis-cible.json',encoding='utf-8')); print('json ok', d['bloc_stable_pendant_le_run'], d['empreinte_bloc_linguistique']['sha256_16'])"
  ```

### 🤖 Assistant

⏵ Récapitulatif final et fichiers livrés

**Trois fichiers neufs, aucun fichier existant modifié, aucun commit** (le `M tools/bloc_linguistique.py` du worktree vient d'un autre agent, je n'y ai pas touché) :

- [`tools/tests/linguistique/replis_cible.py`](tools/tests/linguistique/replis_cible.py) — prototype autonome (sous-classe + post-traitement des cibles), non importé ailleurs.
- [`reports/rapport-replis-cible.md`](reports/rapport-replis-cible.md) — fiche : protocole, Q1, tableau par retouche, contrôles négatifs, limites, recommandation.
- [`reports/pensee-replis-cible.json`](reports/pensee-replis-cible.json) — résultats, 145 audits, snapshot A3 137, dérive des empreintes.

**Empreinte mesurée** : `tools/bloc_linguistique.py = 9da6dee7` (105 156 o, 15:22:00), stable pendant le run. Le bloc a bougé pendant la session (`6e843018 → bb020516 → 64b7c520 → 9da6dee7`) : le live a déjà absorbé `g002` (`_repli_cible_gp`), `g012`/`r018` (`_cible_hors_span`) et `r230` (`_sans_enclitique`).

**Baseline live** : 141/145 exact, 143/145 top1, 142/239 top-k strict. **Baseline A3** (snapshot `bb020516`) : 137/145. 

**Q1** : sur 145 → 144 cibles remplies, **1 vide** (`s041`) ; sur 239 → **94 absentes** (48 REL, 33 SUB, 13 GP) + 1 vide = 95 sans cible utilisable. **2 cas nom prédit / verbe gold** : `s108` (`papier` vs `rêve`), `s122` (`papier` vs `saute`) ; sur le snapshot A3 il y avait aussi `r230` (depuis réparé), et 2 cas inverse (`g012`, `r018`, depuis réparés).

| retouche | gain live | régressions | net live | net A3 (137) | recommandation |
|---|---:|---:|---:|---:|---|
| R1 repli cible vide (GP only) | +1 (`s041`) | 0 | **+1** | +2 (`g002`, `s041`) | ✅ intégrer |
| R2 étroite (tête proche, GP) | +2 (`s108`, `s122`) | 0 | **+2** | +4 (forme large, 4 cas) | ✅ intégrer |
| R2 littérale (« préférer un verbe ») | 0 | 3 (`g002`, `g012`, `r018`) | **-3** | 0 | ❌ ne pas intégrer |
| R3 étroite (complétive en tête) | +1 (`r309`) | 0 | **+1** | +1 | ✅ intégrer |
| **combiné** | **+4** | **0** | **+4** | **+7** | **145/145 exact, 145/145 top1** |

Le combiné atteint **145/145 exact (1,0000)** et **145/145 top1** sur les 145, et **145/239 (0,6067)** sur les 239 : le plafond global reste les 94 spans non prédits. La R2 large de A3 donne le même +2 marginal que l'étroite mais change 12 étiquettes (10 hors gold) contre 4 (2 hors gold : `r121`, `r227`) ; la R2 littérale est néfaste (elle défait `g002`/`g012`/`r018`). La R3 large coûte 33 régressions. Le +4 live (contre +7 sur A3) est une **borne haute** (règles dessinées sur les cas) : avant intégration, gold tenu à l'écart, revue de `s027`/`r121`/`r227`, portes. Le top-k reste **142/239 strict**.

