# Session DSH — relecture

- identifiant : `7f247e9c-00ab-4bdf-bfba-2dc5c20d7cf0`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-07 02:09:33
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission **courte et ciblée** : les **2 spans restants** de l'attachement, diagnostic et règles candidates mesurées — sans modifier le code du dépôt.

Contexte : `tools/bloc_linguistique.py` (`_syntagmes_simple`, `_cible_precedent`), `tools/tests/linguistique/evaluer_gold.py` (`charger`, `evaluer_bloc`), `tools/tests/linguistique/gold_split.py` (`dev`, `test`). État : **attachement 236/237 (0,9916)**, POS 86,25 %, F1 0,7535. Les 2 spans perdus :
- `r035` : « The film she talks about is out. » — le gold attend une REL « she talks about » ; aucune n'est produite (relative zéro, sans pronom relatif).
- `g017` : « She said that she would come yesterday. » — le gold attend une SUB « that she would come » (sans « yesterday »).

À faire :
1. Reproduire les deux cas, expliquer **précisément** (quelle branche, quel test échoue), et proposer **une** règle générale par cas, mesurée sur **dev** puis **test**, avec le patch exact (3-8 lignes).
2. Vérifier que l'attachement **ne baisse pas** et que le POS/F1 ne bougent pas (ou montent).
3. Écris **uniquement** deux fichiers neufs : `reports/rapport-spans-restants.md` et `reports/pensee-spans-restants.json` (patchs exacts inclus).
4. Ne commite rien ; ne modifie aucun existant ; pas de `docs/pilotage/`, `AGENTS.md`, `journal/`, `tools/structures/`, `data/`, natifs.

Sois **bref** : 2 pages maximum. Rends un résumé : les causes, les deux patchs, les chiffres dev/test, les rejets.
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

⏵ Cartographie du dépôt et lecture des fichiers clés de l'attachement

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short && git branch --show-current && ls reports/ | head -30", "description": "Check repo status and branch"}`

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
D  journal/2026-11-06/distribue.md
D  journal/2026-11-06/docs.md
D  journal/2026-11-06/memoire.md
D  journal/2026-11-06/mesures.md
D  journal/2026-11-06/modele.md
D  journal/2026-11-06/moteur.md
D  journal/2026-11-06/outils.md
D  journal/2026-11-06/portes.md
MM journal/2026-11-07/README.md
D  journal/2026-11-07/distribue.md
D  journal/2026-11-07/docs.md
D  journal/2026-11-07/mesures.md
D  journal/2026-11-07/portes.md
MM journal/README.md
MM journal/THEMES.md
MM journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/digest.md
MM journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/rapport.md
D  journal/sessions/082fe8ca-3e1e-4454-b91b-12586843e880/digest.md
D  journal/sessions/082fe8ca-3e1e-4454-b91b-12586843e880/rapport.md
D  journal/sessions/14114f3d-ae0d-416e-ad8e-4d4eaa04c36c/digest.md
D  journal/sessions/14114f3d-ae0d-416e-ad8e-4d4eaa04c36c/rapport.md
D  journal/sessions/1555bdd3-27e9-4779
… [9107 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && wc -l tools/bloc_linguistique.py tools/tests/linguistique/evaluer_gold.py tools/tests/linguistique/gold_split.py", "description": "Line counts of key files"}`

  ```
2737 tools/bloc_linguistique.py
   307 tools/tests/linguistique/evaluer_gold.py
    50 tools/tests/linguistique/gold_split.py
  3094 total
  ```

### 🤖 Assistant

⏵ Lecture du protocole d'évaluation et du split gold

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_split.py"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/evaluer_gold.py"}`

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
… [16119 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Localisation des fonctions de syntagmes et d'attachement

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"_syntagmes_simple\\|_cible_precedent\\|def _est_verbe\\|REL\\b\" tools/bloc_linguistique.py | head -80", "description": "Locate functions and REL references"}`

  ```
385:AMBIGUES_REL = {"when", "where", "why", "how", "quand", "où", "pourquoi", "comment"}
501:def _est_verbe(mot: str) -> bool:
931:    def _cible_precedent(texte: str, segment: dict, precedent: dict | None, verbes) -> str | None:
932:        """REL → tête du GN précédent ; SUB après un GV → son verbe (le gouverneur)."""
935:        if segment.get("type") == "REL" and precedent.get("type") == "GN":
945:        """Les candidats que le **précédent** impose : l'antécédent d'une REL, le verbe d'une SUB."""
948:        if segment.get("type") == "REL" and precedent.get("type") == "GN":
980:        """Sans gouverneur extérieur, une SUB/REL prend son propre verbe (« qu'il viendra »)."""
981:        if cible or segment.get("type") not in ("SUB", "REL"):
1116:    def _syntagmes_simple(self, texte: str, langue: str,
1169:                    # en tête reste une REL (« Paul qui marche »)
1170:                    if precedent == "GN" and n in AMBIGUES_REL:
1171:                        stype = "REL"   # « The day when we left »
1175:                                          or precedent == "GV") else "REL"
1493:        simples = self._syntagmes_simple(texte, lg, pos_verbes)
1509:                  
… [648 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -c \"\nimport json\nfrom tools.tests.linguistique.evaluer_gold import charger\nph = charger()\nfor p in ph:\n    if p.get('id') in ('r035','g017'):\n        print(p['id'], p.get('source'), p['langue'])\n        print(json.dum … [84 caractères tronqués]`

  ```
g017 hand en
{
 "id": "g017",
 "langue": "en",
 "texte": "She said that she would come yesterday.",
 "mots": [
  {
   "texte": "She",
   "pos": "PRON",
   "debut": 0,
   "fin": 3
  },
  {
   "texte": "said",
   "pos": "VERB",
   "debut": 4,
   "fin": 8
  },
  {
   "texte": "that",
   "pos": "CONJ",
   "debut": 9,
   "fin": 13
  },
  {
   "texte": "she",
   "pos": "PRON",
   "debut": 14,
   "fin": 17
  },
  {
   "texte": "would",
   "pos": "AUX",
   "debut": 18,
   "fin": 23
  },
  {
   "texte": "come",
   "pos": "VERB",
   "debut": 24,
   "fin": 28
  },
  {
   "texte": "yesterday",
   "pos": "ADV",
   "debut": 29,
   "fin": 38
  }
 ],
 "segments": [
  {
   "type": "GN",
   "texte": "She",
   "role": "agent",
   "debut": 0,
   "fin": 3
  },
  {
   "type": "GV",
   "texte": "said",
   "role": "prédicat",
   "debut": 4,
   "fin": 8
  },
  {
   "type": "SUB",
   "texte": "that she would come",
   "role": "contenu",
   "debut": 9,
   "fin": 28,
   "cibles": [
    "said"
   ],
   "cible": "said"
  }
 ],
 "pragma": {
  "acte": "assertion",
  "modalite": true
 },
 "source": "hand"
}
r035 reel en
{
 "id": "r035",
 "langue": "en",
 "texte": "The film she talks about is out.",
 "mots": [
  {

… [955 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des branches de segmentation et d'attachement

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "offset": 1100, "limit": 180}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "offset": 900, "limit": 140}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
1100:         """Les verbes des `k` GV les plus proches — les **candidats** d'attachement."""
1101:         if segment.get("type") == "GV" or not gvs:
1102:             return []
1103:         def ecart(g: dict) -> int:
1104:             if g["fin"] <= segment["debut"]:
1105:                 return segment["debut"] - g["fin"]
1106:             if g["debut"] >= segment["fin"]:
1107:                 return g["debut"] - segment["fin"]
1108:             return 0
1109:         proches: list[str] = []
1110:         for g in sorted(gvs, key=ecart)[:k]:
1111:             v = Heuristique._verbe_gv(texte, g, verbes, cache)
1112:             if v and v not in proches:
1113:                 proches.append(v)
1114:         return proches
1115: 
1116:     def _syntagmes_simple(self, texte: str, langue: str,
1117:                           pos_verbes: set[int] | None = None) -> list[dict]:
1118:         mots = self._mots(texte)
1119:         lex = POS_FERME.get(langue, POS_FERME["fr"])
1120:         pos_verbes = pos_verbes or set()
1121:         par_debut = {m[0]: k for k, m in enum
… [10672 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
900: 
901:     # -- syntagmes ----------------------------------------------------------
902:     def _syntagmes_s(self, texte: str) -> list[dict] | None:
903:         if not self.segmenter_s:
904:             return None
905:         try:
906:             if str(RACINE / "tools/structures") not in sys.path:
907:                 sys.path.insert(0, str(RACINE / "tools/structures"))
908:             import generateur  # le générateur S, importé en lecture seule
909:             return generateur.analyser(texte)
910:         except Exception:
911:             return None
912: 
913:     def _cibles_s(self, texte: str) -> dict:
914:         """Toutes les cibles du générateur S (pas seulement le dernier segment ambigu).
915: 
916:         Lecture seule de l'API interne du S : `_tokens`/`_segmente` rendent les `Segment` avec
917:         `cible_nom`/`cible_gp`/`cible_verbe`. Le défaut retenu est la cible la plus proche
918:         (GP, puis GN, puis GV), comme le premier candidat de `analyser`.
919:         """
920:         if not self.segmenter_s:
921:             return {
… [6737 caractères tronqués]
  ```

