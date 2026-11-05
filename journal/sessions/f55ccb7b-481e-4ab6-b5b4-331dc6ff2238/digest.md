# Session DSH — relecture

- identifiant : `f55ccb7b-481e-4ab6-b5b4-331dc6ff2238`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-05 13:11:54
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **prototype autonome d'un classement appris** des candidats d'attachement.

Contexte : `tools/tests/linguistique/evaluer_gold.py` expose `charger()` (612 phrases, segments gold avec `cibles`) et `evaluer_bloc` ; `tools/bloc_linguistique.py` expose `Heuristique` (annotation avec étiquettes de niveau `syntagme`, `candidats`, `meta.attachement.cible`) et `_est_verbe`. La règle actuelle choisit la cible par type + proximité et donne **123/145** en égalité exacte.

À faire :
1. Crée **un seul fichier neuf** : `tools/tests/linguistique/classement_cible.py`. Il ne modifie rien d'autre et n'est importé par rien.
2. Pour chaque segment gold dont le span est prédit, construis des features par candidat : distance en tokens au segment, côté (gauche/droite), type du segment (GP/REL/SUB), préposition éventuelle, longueur du candidat, nature (verbe/nom via `_est_verbe`), rang dans la liste.
3. Apprends un score simple (régression logistique implémentée à la main avec descente de gradient, ou recherche de poids par grille — pas de dépendance nouvelle si possible) sur une **moitié** des phrases (ids pairs) et évalue sur l'autre (ids impairs), puis l'inverse. Rapporte l'exact des deux sens et la moyenne, contre la règle actuelle sur les mêmes segments.
4. Écris **uniquement** ce fichier plus deux fichiers neufs de résultat : `reports/rapport-classement-appris.md` (fiche : titre, verdict, protocole, résultats par moitié, poids, contrôle négatif — hasard et règle actuelle —, limites dont la petite taille) et `reports/pensee-classement-appris.json`.
5. Ne touche **pas** `tools/bloc_linguistique.py` : le prototype est autonome, l'intégration sera faite par l'agent principal.

Règles strictes : ne committe rien ; ne modifie aucun fichier existant ; n'écris pas dans `docs/pilotage/`, `AGENTS.md`, `journal/`, `tools/structures/`, `data/`, `tools/entrainer_native.py`, `tools/native_model.py`. Rends un résumé avec les taux obtenus et ta recommandation (intégrer / ne pas intégrer).
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

⏵ Exploration du dépôt et lecture des deux fichiers clés

- **bash** `{"command": "pwd && git branch --show-current && git status --short | head -20 && ls tools/tests/linguistique/ && ls reports/ | head -30", "description": "Vérifier branche et arborescence"}`

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
qualif
… [790 caractères tronqués]
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

⏵ Lecture ciblée de `bloc_linguistique.py` (Heuristique, attachement, `_est_verbe`)

- **bash** `{"command": "wc -l tools/bloc_linguistique.py && grep -n \"_est_verbe\\|def _attacher\\|attachement\\|candidats\\|class Heuristique\\|def analyser\" tools/bloc_linguistique.py | head -80", "description": "Localiser les fonctions utiles"}`

  ```
1881 tools/bloc_linguistique.py
7:    **candidats** pour l'ambigu ; elle déclare sa couverture et sa confiance ;
19:`niveau`, son `span`, sa `source`, sa `confiance`, sa `langue`, son `script` et ses `candidats`.
76:    candidats: list[str] = field(default_factory=list)
86:            "candidats": list(self.candidats), "langue": self.langue,
133:    def analyser(self, texte: str, langue: str | None = None,
428:def _est_verbe(mot: str) -> bool:
472:class Heuristique:
631:            if _est_verbe(m) and _normaliser(m) not in AUXILIAIRES:
634:            if _est_verbe(m):
672:        """Les verbes des `k` GV les plus proches — les **candidats** d'attachement."""
708:                                 "texte": texte[d:mots[j - 1][1]], "candidats": []})
716:                       and not _est_verbe(mots[j][2])
721:                                 "texte": texte[d:mots[j - 1][1]], "candidats": []})
730:                                 "texte": texte[d:mots[j - 1][1]], "candidats": []})
739:                                 "texte": texte[d:mots[j - 1][1]], "candidats": []})
746:    def analyser(self, texte: str, langue: str | None = None,
783:                                            can
… [2554 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, pathlib\nfor f in [\"gold.json\",\"gold_reel.json\",\"gold_synthetique.json\"]:\n    p = pathlib.Path(\"tools/tests/linguistique\")/f\n    d = json.loads(p.read_text(encoding=\"utf-8\"))\n    print(f,  … [260 caractères tronqués]`

  ```
gold.json dict_keys(['version', 'phrases', 'note']) 20
gold_reel.json dict_keys(['version', 'source', 'note', 'phrases']) 432
gold_synthetique.json dict_keys(['version', 'source', 'graine', 'note', 'phrases']) 160
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
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "offset": 420, "limit": 120}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "offset": 640, "limit": 270}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
420: suis es est sommes êtes sont étais était étions étiez étaient été sera serai seras seront
421: serais serait serions seriez seraient sois soit soyons soyez soient étant
422: ai as a avons avez ont avais avait avions aviez avaient aurai auras aura aurons aurez auront
423: aurais aurait aurions auriez auraient aie aies ait ayons ayez aient ayant eu
424: am is are was were be been being have has had having do does did done
425: """.split())
426: 
427: 
428: def _est_verbe(mot: str) -> bool:
429:     """Le mot est-il un verbe ? Lexique + désinences courantes (fr/en)."""
430:     n = _normaliser(mot)
431:     if not n:
432:         return False
433:     if n in VERBES_CONNUS:
434:         return True
435:     for suf in ("er", "ir", "e", "es", "ent", "ait", "aient", "é", "ée", "és", "i", "u",
436:                 "ez", "ons", "iez", "ais", "ra", "rai", "ras", "rons", "rez", "ront",
437:                 "s", "ed", "ing", "en"):
438:         if n.endswith(suf) and n[:-len(suf)] in VERBES_CONNUS:
439:             return True
440:     # participes en -é/-és/-ée : `accroch
… [4652 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
640:         return None if strict else (mots[-1][1] if mots else None)
641: 
642:     @staticmethod
643:     def _cible_proche(texte: str, segment: dict, gvs: list[dict],
644:                       verbes: list[tuple[int, int, str]] | None = None) -> str | None:
645:         """La cible d'un segment : le **verbe du GV le plus proche** (règle de proximité).
646: 
647:         Rend `None` si le segment est lui-même un GV ou s'il n'y a pas de GV. Le verbe est le
648:         dernier token du GV (`a vu` → `vu`, `est mangé` → `mangé`).
649:         """
650:         if segment.get("type") == "GV" or not gvs:
651:             return None
652:         # le plus proche, tous côtés mêlés : la variante « GV de gauche d'abord » a été
653:         # mesurée (2026-11-05) et donne **le même** exact — elle n'est pas retenue.
654:         def ecart(g: dict) -> int:
655:             if g["fin"] <= segment["debut"]:
656:                 return segment["debut"] - g["fin"]
657:             if g["debut"] >= segment["fin"]:
658:                 return g["debut"] - segment["fin"]
659:      
… [16095 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Mesure du socle actuel et analyse des cibles gold

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && time python3 tools/tests/linguistique/evaluer_gold.py 2>&1 | tail -20", "description": "Lancer l'évaluation gold actuelle", "timeoutMs": 300000}`

  ```
"cibles": 136,
    "labels": 136,
    "top1": 118,
    "topk": 126,
    "top1_taux": 0.8676,
    "topk_taux": 0.9265,
    "couverture": 1.0
   }
  },
  "reel": {
   "bloc": "parallele",
   "phrases": 452,
   "pos": {
    "exactitude": 0.7512,
    "exactitude_ferme": 0.8885,
    "exactitude_ouvert": 0.6061,
    "tokens": 2480,
    "confusions": {
     "ADJ"
heuristique all: {"pos": {"exactitude": 0.7455, "exactitude_ferme": 0.8984, "exactitude_ouvert": 0.6007, "tokens": 3179, "confusions": {"ADJ": {"ADJ": 50, "NOUN": 80, "VERB": 4}, "ADV": {"ADV": 117, "NOUN": 21, "PREP": 1, "ADJ": 1, "?": 1}, "AUX": {"PREP": 4, "AUX": 118, "?": 3, "NOUN": 3}, "CONJ": {"CONJ": 44, "PRON": 25, "DET": 12, "?": 13, "PREP": 2, "NOUN": 2}, "DET": {"DET": 586, "?": 2}, "NOUN": {"NOUN": 617, "ADJ": 17, "VERB": 47, "?": 1}, "NUM": {"NUM": 2}, "PONCT": {"?": 25}, "PREP": {"PREP": 111, "NOUN": 3}, "PRON": {"PRON": 411, "NOUN": 8, "?": 30, "DET": 25, "CONJ": 1}, "VERB": {"VERB": 314, "NOUN": 447, "ADJ": 5, "PREP": 2, "?": 16, "AUX": 7, "ADV": 1}}}, "syntagme": {"precision": 0.3154, "rappel": 0.2619, "f1": 0.2862, "tp": 488, "fp": 1059, "fn": 1375, "tete": {"precision": 0.5862, "rappel": 0.4342, "f1": 0.4989, "
… [212 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, json, pathlib, collections\nsys.path.insert(0,\"tools/tests/linguistique\"); sys.path.insert(0,\"tools\")\nfrom evaluer_gold import charger\nimport bloc_linguistique as bl\nph = charger()\nprint(\"phras … [853 caractères tronqués]`

  ```
phrases 612 tokens 3179
segments avec cibles 239 Counter({'GP': 96, 'REL': 74, 'SUB': 69})
== GP
('hand', 'g002', 'Le chat de la voisine dort.', 'GP', 'de la voisine', ['chat'], 'possession')
('hand', 'g003', "La femme a vu l'homme dans le parc.", 'GP', 'dans le parc', ['vu', "l'homme"], 'lieu')
('hand', 'g004', 'Il a couru pour attraper le bus.', 'GP', 'pour attraper le bus', ['couru'], 'but')
('hand', 'g006', 'Le chien du voisin aboie la nuit.', 'GP', 'du voisin', ['chien'], 'possession')
('hand', 'g007', 'Les enfants jouent dans le jardin.', 'GP', 'dans le jardin', ['jouent', 'enfants'], 'lieu')
('hand', 'g010', 'Viens ici !', 'GP', 'ici', ['Viens'], 'lieu')
== SUB
('hand', 'g005', "Elle a dit qu'elle viendrait hier.", 'SUB', "qu'elle viendrait", ['dit'], 'contenu')
('hand', 'g017', 'She said that she would come yesterday.', 'SUB', 'that she would come', ['said'], 'contenu')
('reel', 'r202', 'Je pense que tu as raison.', 'SUB', 'que tu as raison', ['pense'], 'complément')
('reel', 'r205', 'I think that you are right.', 'SUB', 'that you are right', ['think'], 'complément')
('reel', 'r207', 'Quand il pleut, je reste.', 'SUB', 'Quand il pleut', ['reste'], 'temps')
('reel', 'r208', 
… [672 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Extraction du détail d'attachement et vérification des spans prédits

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/tests/linguistique/evaluer_gold.py --json /tmp/eval_gold.json >/dev/null 2>&1; python3 - <<'EOF'\nimport json\nd=json.load(open(\"/tmp/eval_gold.json\"))\nfor bloc in (\"heuristique\",):\n    for scope in (\"all\",\"ree … [306 caractères tronqués]`

  ```
heuristique all {'cibles': 239, 'labels': 145, 'top1': 126, 'topk': 134, 'topk_exact': 88, 'exact': 123, 'exact_taux_span': 0.8483, 'top1_taux_span': 0.869, 'topk_taux_span': 0.9241}
heuristique reel {'cibles': 184, 'labels': 115, 'top1': 103, 'topk': 105, 'topk_exact': 69, 'exact': 102, 'exact_taux_span': 0.887, 'top1_taux_span': 0.8957, 'topk_taux_span': 0.913}
heuristique hand {'cibles': 13, 'labels': 10, 'top1': 8, 'topk': 9, 'topk_exact': 7, 'exact': 8, 'exact_taux_span': 0.8, 'top1_taux_span': 0.8, 'topk_taux_span': 0.9}
heuristique synthetique {'cibles': 55, 'labels': 30, 'top1': 23, 'topk': 29, 'topk_exact': 19, 'exact': 21, 'exact_taux_span': 0.7, 'top1_taux_span': 0.7667, 'topk_taux_span': 0.9667}
  ```

### 🤖 Assistant

⏵ Diagnostic des 145 cas prédits : nature et position de la cible gold

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, json, pathlib, collections, re\nsys.path.insert(0,\"tools/tests/linguistique\"); sys.path.insert(0,\"tools\")\nfrom evaluer_gold import charger, _seg, _pos_map, _tete\nimport bloc_linguistique as bl\n\n … [2819 caractères tronqués]`

  ```
labels 145 ok 123
nature Counter({('GP', 'verbe'): 45, ('GP', 'nom'): 38, ('REL', 'nom'): 26, ('SUB', 'verbe'): 18, ('SUB', 'nom'): 18})
ok par type/nature Counter({('GP', 'verbe', True): 45, ('REL', 'nom', True): 26, ('GP', 'nom', True): 24, ('SUB', 'verbe', True): 15, ('GP', 'nom', False): 14, ('SUB', 'nom', True): 13, ('SUB', 'nom', False): 5, ('SUB', 'verbe', False): 3})
side Counter({('GP', 'gauche'): 83, ('SUB', 'gauche'): 22, ('REL', 'gauche'): 22, ('SUB', 'droite'): 12, ('REL', ''): 4, ('SUB', ''): 1, ('SUB', 'dedans'): 1})
prep GP Counter({'à': 13, 'to': 9, 'in': 8, 'dans': 7, 'vers': 6, 'at': 5, 'sur': 4, 'on': 4, 'de': 3, 'pour': 3, 'avec': 3, 'devant': 3, 'sous': 3, 'depuis': 2, 'au': 2, 'aux': 2, 'ici': 1, 'en': 1, 'contre': 1, 'with': 1, 'over': 1, 'chez': 1})
posg Counter({('GP', '?'): 82, ('SUB', '?'): 36, ('REL', '?'): 26, ('GP', 'VERB'): 1})
occ Counter({1: 139, 0: 5, 2: 1})
== erreurs
hand g002 GP | Le chat de la voisine dort. | de la voisine | gold chat nom gauche | pred  | cands ['GP']
hand g012 GP | Le canard est prêt à manger. | à manger | gold prêt nom gauche | pred manger | cands ['« à manger » → Le canard', '« à manger » → est prêt', 'manger', 'est']
reel 
… [2991 caractères tronqués]
  ```

