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

### 🤖 Assistant

⏵ Inspection fine de quelques erreurs et du POS gold des cibles

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, json, collections\nsys.path.insert(0,\"tools/tests/linguistique\"); sys.path.insert(0,\"tools\")\nfrom evaluer_gold import charger, _pos_map\nimport bloc_linguistique as bl\nh=bl.Heuristique()\nph={p[\" … [834 caractères tronqués]`

  ```
================================================================================
r080 The birds fly over the lake.
mots gold: [('The', 'DET', 0), ('birds', 'NOUN', 4), ('fly', 'VERB', 10), ('over', 'PREP', 14), ('the', 'DET', 19), ('lake', 'NOUN', 23)]
segments: [('GP', 'over the lake', ['fly'])]
  SEG GN 'The birds fly' 0 13 | cands ['GN', 'lake'] | meta {'role': 'groupe nominal', 'niveau': 0, 'union': True, 'attachement': {'segment': 'The birds fly', 'cible': 'lake'}}
  SEG GV 'The birds fly over the lake' 0 27 | cands ['structure la plus proche'] | meta {'role': 'predicat', 'niveau': 0}
  POS NOUN 'birds' 4 9
  POS NOUN 'fly' 10 13
  SEG GP 'over the lake' 14 27 | cands ['GP', 'lake'] | meta {'role': 'complément', 'niveau': 1, 'union': True, 'attachement': {'segment': 'over the lake', 'cible': 'lake'}}
  POS NOUN 'lake' 23 27
================================================================================
r120 The river flows to the sea.
mots gold: [('The', 'DET', 0), ('river', 'NOUN', 4), ('flows', 'VERB', 10), ('to', 'PREP', 16), ('the', 'DET', 19), ('sea', 'NOUN', 23)]
segments: [('GP', 'to the sea', ['flows'])]
  SEG GN 'The river flows' 0 15 | cands ['GN', 'river'] | meta {
… [3888 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Analyse de la couverture du vivier de candidats et des cas non tokenisables

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, re, json, collections\nsys.path.insert(0,\"tools/tests/linguistique\"); sys.path.insert(0,\"tools\")\nfrom evaluer_gold import charger\nimport bloc_linguistique as bl\n\ndef toks(texte):\n    return [(m … [1695 caractères tronqués]`

  ```
n 145 multi [] pool_cov Counter({True: 144, False: 1})
== misses cible non token
('r230', 'reel', 'Quand tu arrives, appelle-moi.', 'SUB', 'Quand tu arrives', 'appelle')
== pool manque
r230 SUB appelle [(9, 16, 'arrives', 'VERB'), (18, 29, 'appelle-moi', 'NOUN')]
  ```

### 🤖 Assistant

⏵ Revue des 145 cas et test de règles simples de repérage

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, re, collections\nsys.path.insert(0,\"tools/tests/linguistique\"); sys.path.insert(0,\"tools\")\nfrom evaluer_gold import charger\nimport bloc_linguistique as bl\nh=bl.Heuristique(); ph=charger()\n\ndef  … [3861 caractères tronqués]`

  ```
segments 145
plus proche (gauche d'abord): 7/145 = 0.0483
REL=noms proches, sinon proche: 22/145 = 0.1517
REL=gauche, sinon proche: 33/145 = 0.2276
GP 83 nearest 5 truc absent 0
REL 26 nearest 0 truc absent 0
SUB 36 nearest 2 truc absent 1
== SUB détails
g005 Elle a dit qu'elle viendrait hier. | gold dit | pred dit True | [('viendrait', 'VERB', False, 'I', 0), ('dit', 'VERB', True, 'G', 1), ('a', 'PREP', True, 'G', 2)]
r202 Je pense que tu as raison. | gold pense | pred pense True | [('as', 'AUX', True, 'I', 0), ('raison', 'NOUN', False, 'I', 0), ('pense', 'NOUN', False, 'G', 1)]
r207 Quand il pleut, je reste. | gold reste | pred reste True | [('pleut', 'VERB', False, 'I', 0), ('reste', 'NOUN', True, 'D', 3)]
r208 Elle dit qu'il vient. | gold dit | pred dit True | [('vient', 'VERB', True, 'I', 0), ('dit', 'VERB', True, 'G', 1)]
r210 Bien qu'il soit tard, il travaille. | gold travaille | pred travaille True | [('soit', 'NOUN', False, 'I', 0), ('travaille', 'NOUN', True, 'D', 3)]
r211 Je sais que tu viens. | gold sais | pred sais True | [('viens', 'VERB', True, 'I', 0), ('sais', 'NOUN', True, 'G', 1)]
r212 Il faut que tu partes. | gold faut | pred faut True | [('partes', 'NOUN', True
… [5191 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification du calcul « plus proche » (incohérence apparente)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, re\nsys.path.insert(0,\"tools/tests/linguistique\"); sys.path.insert(0,\"tools\")\nfrom evaluer_gold import charger\nimport bloc_linguistique as bl\nh=bl.Heuristique(); ph={p[\"id\"]:p for p in charger( … [552 caractères tronqués]`

  ```
pos {(0, 3): 'DET', (4, 9): 'NOUN', (10, 13): 'NOUN', (14, 18): 'PREP', (19, 22): 'DET', (23, 27): 'NOUN'} mots [(0, 3, 'The', 'mot'), (4, 9, 'birds', 'mot'), (10, 13, 'fly', 'mot'), (14, 18, 'over', 'mot'), (19, 22, 'the', 'mot'), (23, 27, 'lake', 'mot'), (27, 28, '.', 'ponctuation')]
seg {'type': 'GP', 'texte': 'over the lake', 'role': 'lieu', 'debut': 14, 'fin': 27, 'cibles': ['fly'], 'cible': 'fly'}
all idx [(0, (0, 3, 'The', 'mot')), (1, (4, 9, 'birds', 'mot')), (2, (10, 13, 'fly', 'mot')), (3, (14, 18, 'over', 'mot')), (4, (19, 22, 'the', 'mot')), (5, (23, 27, 'lake', 'mot')), (6, (27, 28, '.', 'ponctuation'))]
sidx [3, 4, 5]
  ```

### 🤖 Assistant

⏵ Statistiques par type de segment pour calibrer les features

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, re, collections\nsys.path.insert(0,\"tools/tests/linguistique\"); sys.path.insert(0,\"tools\")\nfrom evaluer_gold import charger\nimport bloc_linguistique as bl\nh=bl.Heuristique(); ph=charger()\ndef pr … [4340 caractères tronqués]`

  ```
par type/prep/nature gold
('GP', 'autre', 'N') 2
('GP', 'autre', 'V') 3
('GP', 'but', 'N') 2
('GP', 'but', 'V') 1
('GP', 'dat', 'N') 10
('GP', 'dat', 'V') 16
('GP', 'gen', 'N') 3
('GP', 'loc', 'N') 19
('GP', 'loc', 'V') 23
('GP', 'moy', 'N') 2
('GP', 'moy', 'V') 2
('REL', '', 'N') 26
('SUB', '', 'N') 18
('SUB', '', 'V') 18
main rule 0 145
GP 83 0
REL 26 0
SUB 36 0
== GP ratés par règle main
g002 hand | de la voisine prep gen gold chat N | pick None | [('chat', 'NOUN', 'N', 'G', 1), ('dort', 'VERB', 'V', 'D', 1)]
g003 hand | dans le parc prep loc gold vu V | pick None | [('femme', 'NOUN', 'N', 'G', 5), ('a', 'PREP', 'V', 'G', 4), ('vu', 'VERB', 'V', 'G', 3), ('homme', 'NOUN', 'N', 'G', 1)]
g004 hand | pour attraper le bus prep but gold couru V | pick None | [('a', 'PREP', 'V', 'G', 2), ('couru', 'NOUN', 'V', 'G', 1)]
g007 hand | dans le jardin prep loc gold jouent V | pick None | [('enfants', 'NOUN', 'N', 'G', 2), ('jouent', 'VERB', 'V', 'G', 1)]
g010 hand | ici prep autre gold Viens V | pick None | [('Viens', 'VERB', 'V', 'G', 1)]
g012 hand | à manger prep dat gold prêt N | pick None | [('canard', 'NOUN', 'N', 'G', 3), ('est', 'AUX', 'V', 'G', 2), ('prêt', 'ADJ', 'N', 'G', 1)]
g014
… [9904 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification des cibles-auxiliaires et du vivier final

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys\nsys.path.insert(0,\"tools/tests/linguistique\"); sys.path.insert(0,\"tools\")\nfrom evaluer_gold import charger\nimport bloc_linguistique as bl\nph=charger()\ncibles=[c for p in ph for s in p[\"segments … [412 caractères tronqués]`

  ```
cibles 282 distinctes 175
cibles aux []
AUXILIAIRES type <class 'set'> 73
dist cibles ['Emma', 'Paul', 'Viens', 'aboie', 'accroché', 'appartient', 'appelle', 'attendent', 'avocat', 'barks', 'believe', 'belongs', 'bird', 'book', 'boy', 'bread', 'bridge', 'call', 'canard', 'car']
  ```

### 🤖 Assistant

⏵ Recherche d'une fiche de résultats existante comme modèle de style

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date -I && ls reports/*.md | tail -5 && grep -rl \"attachement\" reports/*.md 2>/dev/null | head -5", "description": "Trouver fiches existantes sur l'attachement"}`

  ```
2026-11-05
reports/rapport-vision-qwen2vl.md
reports/rapport-vitesse-v41.md
reports/rapport-vram-transfert.md
reports/README.md
reports/toutes-langues.md
reports/INDEX.md
reports/rapport-bloc-linguistique.md
reports/rapport-pensee-attachement-cible.md
reports/rapport-pensee-attachement.md
reports/rapport-pensee-cible-proximite.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls reports/ | grep -i -E \"lingu|attache|syntag|gold|cible\" | head -20", "description": "Lister fiches linguistiques"}`

  ```
bloc-linguistique.json
composition-multilingue.json
multilingue.json
pensee-attachement-cible.json
pensee-attachement.json
pensee-cible-proximite.json
pensee-cibles-500.json
pensee-cibles.json
pensee-echecs-attachement.json
pensee-echecs-cible.json
pensee-gold-200.json
pensee-gold-342.json
pensee-gold-cascade-200.json
pensee-gold-cascade.json
pensee-gold-complexes100.json
pensee-gold-complexes20.json
pensee-gold-complexes50.json
pensee-gold-complexes.json
pensee-gold-discours.json
pensee-gold-gele.json
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-attachement-cible.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-attachement-cible.md</path>
<type>file</type>
<content>
1: # B13 — l'attachement ciblé : l'exact passe de 0,6438 à 0,8082
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
4: > **173/173 portes** : la nature de la cible dépend du **type du segment**, et la règle le dit
5: > maintenant : pour un **REL/SUB**, l'attachement est l'**antécédent** (la tête du GN à gauche,
6: > élision séparée : `L'homme` → `homme`) ; pour un **GP**, c'est le **verbe du GV** le plus
7: > proche. Sur les 146 segments au bon span : **exact 94 → 118** (0,6438 → **0,8082**), top1
8: > 0,8356, top-k 0,9041. Par convention : **verbes 48/51 (0,9412)**, **noms 70/95 (0,7368)**.
9: >
10: > **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_tete_nom`),
11: > [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
12: > [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-attachement-cible.json`](pensee-attachement-cible.json).
13: 
14: ## 1. Avant / après (146 segments au bon span)
15: 
16: | mesure | avant | **attachement ciblé** | écart 
… [2494 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Écriture du prototype `classement_cible.py`

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py", "content": "\"\"\"classement_cible.py — prototype **autonome** d'un classement appris des candidats d'attachement.\n\nLe problème. `bloc_linguistique.Heuristique` choisit la cible d'un segme … [32448 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

### 🤖 Assistant

⏵ Nettoyage du prototype (code mort dans `main` et contrôles)

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py", "old_string": "def _mcnemar_exact(b: int, c: int) -> float:", "new_string": "def _mcnemar_exact(b: int, c: int) -> float:\n    \"\"\"p bilatéral exact du test de McNemar (binomiale sur les p … [257 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"_mcnemar_exact\\|_bootstrap_difference\\|_index_candidats\\|_prediction_pool\\|def executer\\|def main\\|hasard_vivier_attendu\" tools/tests/linguistique/classement_cible.py", "description": "Repérer les blocs à nettoyer"}`

  ```
378:def _mcnemar_exact(b: int, c: int) -> float:
388:def _mcnemar_exact_doc(b: int, c: int) -> float:
398:def _bootstrap_difference(segments: list[dict], modele_pool: dict[int, list[float]],
416:def _index_candidats(seg: dict) -> dict:
420:def _prediction_pool(seg: dict, modeles: dict[int, list[float]]) -> str:
424:def executer(phrases: list[dict], graine: int = 0, stabilite: int = 10,
497:               "p_exact": _mcnemar_exact(b, c)}
601:            "hasard_vivier_attendu": _taux(sum(
626:def main() -> int:
651:    # `hasard_vivier_attendu` a été calculé dans le contrôle négatif ; on le complète ici.
655:    json_resultat["controle_negatif"]["hasard_vivier_attendu"] = round(attendu, 4)
656:    resultat["controle_negatif"]["hasard_vivier_attendu"] = round(attendu, 4)
658:    resultat["controle_negatif"].pop("hasard_vivier_attendu", None)
659:    resultat["controle_negatif"]["hasard_vivier_attendu"] = round(attendu, 4)
686:    print("hasard vivier attendu:", json_resultat["controle_negatif"]["hasard_vivier_attendu"])
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py", "offset": 370, "limit": 65}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py</path>
<type>file</type>
<content>
370:     """Deux hasards : uniforme dans le vivier, et tirage d'une cible parmi les distinctes."""
371:     ok = sum(1 for s in segments if _argmax_aleatoire(s, rng) == s["cible"])
372:     attendu = sum((sum(c["positif"] for c in s["candidats"]) / len(s["candidats"]))
373:                   for s in segments if s["candidats"]) / max(1, len(segments))
374:     return {"n": len(segments), "justes": ok, "taux": _taux(ok, len(segments)),
375:             "taux_attendu": round(attendu, 4)}
376: 
377: 
378: def _mcnemar_exact(b: int, c: int) -> float:
379:     """p bilatéral exact du test de McNemar (binomiale sur les paires discordantes)."""
380:     n = b + c
381:     if n == 0:
382:         return 1.0
383:     k = min(b, c)
384:     p = 2.0 * sum(math.comb(n, i) for i in range(k + 1)) / (2.0 ** n)
385:     return round(min(1.0, p), 6)
386: 
387: 
388: def _mcnemar_exact_doc(b: int, c: int) -> float:
389:     """p bilatéral exact du test de McNemar (binomiale sur les paires discordantes)."""
390:     n = b + c
391:     if n == 0:
392:         return 1.0
… [1887 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py", "old_string": "def _mcnemar_exact_doc(b: int, c: int) -> float:\n    \"\"\"p bilatéral exact du test de McNemar (binomiale sur les paires discordantes).\"\"\"\n    n = b + c\n    if n == 0:\ … [1258 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py", "offset": 548, "limit": 120}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py</path>
<type>file</type>
<content>
548:                    "tokens": sum(len(p["mots"]) for p in phrases),
549:                    **stats},
550:         "protocole": {
551:             "segments_mesures": len(segments_tries),
552:             "par_plis": {"pairs": compte_parite[0], "impairs": compte_parite[1]},
553:             "vivier": "tokens pleins (POS ouverte ou _est_verbe), auxiliaires exclus",
554:             "liste": "gauche → droite → dedans, puis distance (rang 0 = plus proche à gauche)",
555:             "modele": "régression logistique binaire, descente de gradient, L2, classes pondérées",
556:             "selection": "argmax du score sur le vivier",
557:             "mesure": "égalité exacte avec cibles[0] (celle de evaluer_gold.py)",
558:             "decoupage": "parité du numéro d'id de phrase ; apprentissage pair → test impair, "
559:                          "puis inverse ; regroupé hors-pli",
560:         },
561:         "features": list(FEATURES),
562:         "poids": poids,
563:         "resultats": {"sens": sens, "moyenne_des_sens": moyenne, "regroupe_hors_p
… [6066 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py", "old_string": "        \"controle_negatif\": {\n            \"regle_actuelle_regroupee\": regroupe[\"regle_actuelle\"],\n            \"hasard_vivier_attendu\": _taux(sum(\n                su … [923 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py", "old_string": "    phrases = charger()\n    resultat = executer(phrases, graine=args.graine, stabilite=args.stabilite,\n                        epochs=args.epochs, lr=args.lr, l2=args.l2)\n  … [1423 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py", "old_string": "    print(\"hasard vivier attendu:\", json_resultat[\"controle_negatif\"][\"hasard_vivier_attendu\"])", "new_string": "    print(\"hasard vivier attendu:\", resultat[\"control … [42 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py has been updated successfully.
  ```

### 🤖 Assistant

⏵ Premier lancement du prototype (sans stabilité pour itérer vite)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && time python3 tools/tests/linguistique/classement_cible.py --json /tmp/classement.json --stabilite 0 --verbeux 2>&1 | tail -60", "description": "Premier run du prototype", "timeoutMs": 300000}`

  ```
== corpus ==
{"phrases": 612, "segments_gold_avec_cible": 239, "span_non_predit": 94}
{"pairs": 79, "impairs": 66}
== par sens ==
pairs->impairs: modèle 66/66 (1.0000) | règle 60/66 (0.9091) | hasard 0.3485
impairs->pairs: modèle 76/79 (0.9620) | règle 63/79 (0.7975) | hasard 0.3671
== regroupé hors-pli ==
modèle 142/145 (0.9793) | règle 123/145 (0.8483)
moyenne des sens: {'modele': 0.981, 'regle_actuelle': 0.8533, 'gain': 0.1277}
McNemar: {'modele_juste_regle_fausse': 21, 'regle_juste_modele_fausse': 2, 'p_exact': 6.6e-05}
bootstrap: {'tirages': 2000, 'difference': 0.131, 'ic95': [0.069, 0.2]}
hasard vivier attendu: 0.3876
repères: {'exactitude_entrainement': 0.9931, 'rang0_justes': 139, 'rang0_taux': 0.9586}
stabilité: {}
== poids (moyenne des plis) ==
  biais            +0.5714
  distance         -0.6254
  rang             -3.3357
  longueur         -0.1883
  cote_gauche      +1.1321
  cote_dedans      -0.8069
  type_GP          -0.5100
  type_REL         +0.1215
  prep_gen         -0.1201
  prep_dat         -0.0741
  prep_loc         -0.2202
  prep_but         -0.0621
  prep_moy         -0.0565
  prep_autre       +0.0230
  nat_verbe        +0.8807
  pos_verbe        +0.3298
  p
… [319 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Résultat surprenant (142/145) : audit des erreurs et des fuites possibles

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nd=json.load(open(\"/tmp/classement.json\"))\nprint(\"corpus\", d[\"corpus\"])\nprint(\"regroupé\", json.dumps(d[\"resultats\"][\"regroupe_hors_pli\"], ensure_ascii=False, indent=1))\nprint(\"== erreurs … [1198 caractères tronqués]`

  ```
corpus {'phrases': 612, 'tokens': 3179, 'segments_gold_avec_cible': 239, 'span_non_predit': 94, 'cible_hors_vivier': 1}
regroupé {
 "n": 145,
 "modele": {
  "justes": 142,
  "taux": 0.9793,
  "par_type": {
   "GP": {
    "n": 83,
    "justes": 81,
    "taux": 0.9759
   },
   "REL": {
    "n": 26,
    "justes": 26,
    "taux": 1.0
   },
   "SUB": {
    "n": 36,
    "justes": 35,
    "taux": 0.9722
   }
  }
 },
 "regle_actuelle": {
  "justes": 123,
  "taux": 0.8483,
  "par_type": {
   "GP": {
    "n": 83,
    "justes": 69,
    "taux": 0.8313
   },
   "REL": {
    "n": 26,
    "justes": 26,
    "taux": 1.0
   },
   "SUB": {
    "n": 36,
    "justes": 28,
    "taux": 0.7778
   }
  }
 }
}
== erreurs modèle
r048 GP | Il écrit une lettre à sa sœur. | seg à sa sœur | gold écrit | actuel 'écrit' | modèle lettre
   cands [('lettre', 'gauche', 1, 0, False, 'NOUN', 1.125734, 0), ('écrit', 'gauche', 3, 1, True, 'NOUN', 0.591418, 1), ('sœur', 'dedans', 0, 2, False, 'NOUN', -4.277564, 0)]
r068 GP | He writes a letter to his sister. | seg to his sister | gold writes | actuel 'writes' | modèle letter
   cands [('letter', 'gauche', 1, 0, False, 'VERB', 2.243707, 0), ('writes', 'gauche', 3, 1, True, 
… [1822 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Stabilité sur 10 découpages aléatoires et contrôle de sensibilité

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && time python3 tools/tests/linguistique/classement_cible.py --json /tmp/classement.json --stabilite 10 --verbeux 2>&1 | tail -50", "description": "Run avec stabilité", "timeoutMs": 300000}`

  ```
== corpus ==
{"phrases": 612, "segments_gold_avec_cible": 239, "span_non_predit": 94}
{"pairs": 79, "impairs": 66}
== par sens ==
pairs->impairs: modèle 66/66 (1.0000) | règle 60/66 (0.9091) | hasard 0.3485
impairs->pairs: modèle 76/79 (0.9620) | règle 63/79 (0.7975) | hasard 0.3671
== regroupé hors-pli ==
modèle 142/145 (0.9793) | règle 123/145 (0.8483)
moyenne des sens: {'modele': 0.981, 'regle_actuelle': 0.8533, 'gain': 0.1277}
McNemar: {'modele_juste_regle_fausse': 21, 'regle_juste_modele_fausse': 2, 'p_exact': 6.6e-05}
bootstrap: {'tirages': 2000, 'difference': 0.131, 'ic95': [0.069, 0.2]}
hasard vivier attendu: 0.3876
repères: {'exactitude_entrainement': 0.9931, 'rang0_justes': 139, 'rang0_taux': 0.9586}
stabilité: {'decoupages': 10, 'modele_moyen': 0.9807, 'modele_ecart_type': 0.0153, 'regle_moyenne': 0.8521, 'regle_ecart_type': 0.0328, 'gain_moyen': 0.1286}
== poids (moyenne des plis) ==
  biais            +0.5714
  distance         -0.6254
  rang             -3.3357
  longueur         -0.1883
  cote_gauche      +1.1321
  cote_dedans      -0.8069
  type_GP          -0.5100
  type_REL         +0.1215
  prep_gen         -0.1201
  prep_dat         -0.0741
  prep_loc         -0
… [465 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Mesure du recouvrement de paraphrases entre moitiés et ablations à ajouter

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, json, collections\nsys.path.insert(0,\"tools/tests/linguistique\"); sys.path.insert(0,\"tools\")\nfrom evaluer_gold import charger\nd=json.load(open(\"/tmp/classement.json\"))\nseg=d[\"segments\"]\ntext … [970 caractères tronqués]`

  ```
segments avec texte présent dans les deux moitiés: 0 / 145
exemples: []
phrases avec >1 ponctuation forte: 2
vivier: moyenne 2.8620689655172415 médiane 3 max 6 taille1 5
distribution Counter({3: 76, 2: 41, 4: 16, 5: 6, 1: 5, 6: 1})
rang0 139
  ```

### 🤖 Assistant

⏵ Ajout des ablations (sans rang, sans position, sans interactions)

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py", "old_string": "# --------------------------------------------------------------------------- évaluation\ndef executer(", "new_string": "# ---------------------------------------------------- … [1559 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"repere = \\|# moyenne des deux sens\\|\\\"poids\\\": poids\" tools/tests/linguistique/classement_cible.py", "description": "Localiser l'insertion des ablations"}`

  ```
557:    repere = {"exactitude_entrainement": _taux(app_ok, app_n),
560:    # moyenne des deux sens (moyenne de taux, pas regroupée)
596:        "poids": poids,
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py", "offset": 552, "limit": 55}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py</path>
<type>file</type>
<content>
552:     for s in segments_tries:
553:         pred_train, _ = _predire(modeles[s["parite"]], s)
554:         app_ok += int(pred_train == s["cible"])
555:         app_n += 1
556:         rang0_ok += int(s["candidats"][0]["texte"] == s["cible"])
557:     repere = {"exactitude_entrainement": _taux(app_ok, app_n),
558:               "rang0_justes": rang0_ok, "rang0_taux": _taux(rang0_ok, app_n)}
559: 
560:     # moyenne des deux sens (moyenne de taux, pas regroupée)
561:     taux = [sens[k]["modele"]["taux"] for k in sens]
562:     taux_regle = [sens[k]["regle_actuelle"]["taux"] for k in sens]
563:     moyenne = {
564:         "modele": round(sum(taux) / len(taux), 4),
565:         "regle_actuelle": round(sum(taux_regle) / len(taux_regle), 4),
566:         "gain": round(sum(taux) / len(taux) - sum(taux_regle) / len(taux_regle), 4),
567:     }
568: 
569:     poids = {
570:         "pairs->impairs": dict(zip(FEATURES, [round(v, 4) for v in modeles[0]])),
571:         "impairs->pairs": dict(zip(FEATURES, [round(v, 4) for v in modeles[1]])),
572:         "m
… [2210 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py", "old_string": "    # moyenne des deux sens (moyenne de taux, pas regroupée)\n    taux = [sens[k][\"modele\"][\"taux\"] for k in sens]", "new_string": "    # ablations : que porte le résultat … [1415 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py", "old_string": "        \"features\": list(FEATURES),\n        \"poids\": poids,\n        \"resultats\": {\"sens\": sens, \"moyenne_des_sens\": moyenne, \"regroupe_hors_pli\": regroupe},", "n … [327 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py", "old_string": "    print(\"repères:\", resultat[\"controle_negatif\"][\"repere\"])\n    print(\"stabilité:\", resultat[\"stabilite_decoupages_aleatoires\"])", "new_string": "    print(\"repè … [281 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py has been updated successfully.
  ```

### 🤖 Assistant

⏵ Deuxième run : ablations et vérification de cohérence

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && time python3 tools/tests/linguistique/classement_cible.py --json /tmp/classement.json --stabilite 10 --verbeux 2>&1 | tail -55", "description": "Run avec ablations", "timeoutMs": 300000}`

  ```
== corpus ==
{"phrases": 612, "segments_gold_avec_cible": 239, "span_non_predit": 94}
{"pairs": 79, "impairs": 66}
== par sens ==
pairs->impairs: modèle 66/66 (1.0000) | règle 60/66 (0.9091) | hasard 0.3485
impairs->pairs: modèle 76/79 (0.9620) | règle 63/79 (0.7975) | hasard 0.3671
== regroupé hors-pli ==
modèle 142/145 (0.9793) | règle 123/145 (0.8483)
moyenne des sens: {'modele': 0.981, 'regle_actuelle': 0.8533, 'gain': 0.1277}
McNemar: {'modele_juste_regle_fausse': 21, 'regle_juste_modele_fausse': 2, 'p_exact': 6.6e-05}
bootstrap: {'tirages': 2000, 'difference': 0.131, 'ic95': [0.069, 0.2]}
hasard vivier attendu: 0.3876
repères: {'exactitude_entrainement': 0.9931, 'rang0_justes': 139, 'rang0_taux': 0.9586}
ablations: {'sans_rang': 0.9379, 'sans_prior_de_position': 0.6276, 'sans_interactions': 0.9724, 'sans_nature': 0.9586}
hors vivier unique: {'n': 140, 'modele': 0.9786, 'regle_actuelle': 0.85, 'segments_vivier_unique': 5}
stabilité: {'decoupages': 10, 'modele_moyen': 0.9807, 'modele_ecart_type': 0.0153, 'regle_moyenne': 0.8521, 'regle_ecart_type': 0.0328, 'gain_moyen': 0.1286}
== poids (moyenne des plis) ==
  biais            +0.5714
  distance         -0.6254
  rang          
… [686 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Contrôle des poids par pli, convergence et cohérence des scores

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nd=json.load(open(\"/tmp/classement.json\"))\nprint(\"== convergence\")\nfor nom,b in d[\"resultats\"][\"sens\"].items():\n    e=b[\"entrainement\"]\n    print(nom, {k:e[k] for k in (\"segments\",\"lign … [952 caractères tronqués]`

  ```
== convergence
pairs->impairs {'segments': 79, 'lignes': 224, 'positifs': 79, 'negatifs': 145, 'epochs_effectues': 1500, 'perte_finale': 52.185774, 'poids_positif': 1.4177, 'poids_negatif': 0.7724}
impairs->pairs {'segments': 66, 'lignes': 191, 'positifs': 66, 'negatifs': 125, 'epochs_effectues': 1500, 'perte_finale': 31.788627, 'poids_positif': 1.447, 'poids_negatif': 0.764}
== poids par pli
biais             +0.9150  +0.2279 OK
distance          -0.4661  -0.7847 OK
rang              -3.2324  -3.4390 OK
longueur          -0.4146  +0.0381 SIGNES OPPOSES
cote_gauche       +0.7489  +1.5153 OK
cote_dedans       -1.0402  -0.5735 OK
type_GP           -0.4171  -0.6029 OK
type_REL          +0.0156  +0.2273 OK
prep_gen          -0.0795  -0.1608 OK
prep_dat          -0.1616  +0.0133 SIGNES OPPOSES
prep_loc          -0.1600  -0.2805 OK
prep_but          -0.0047  -0.1194 OK
prep_moy          -0.1097  -0.0032 OK
prep_autre        +0.0984  -0.0524 SIGNES OPPOSES
nat_verbe         +1.0912  +0.6701 OK
pos_verbe         +0.0283  +0.6313 OK
pos_nom           +0.0710  +0.0839 OK
GP_x_verbe        +0.8996  +0.7798 OK
REL_x_verbe       -0.0849  -0.3449 OK
SUB_x_verbe       +0.2765  +0.2352 OK
GP_x_pos
… [410 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Convergence propre (critère relatif) et rang 0 par type

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py", "old_string": "def entrainer(segments: list[dict], epochs: int = 1500, lr: float = 0.6,\n              l2: float = 0.01) -> tuple[list[float], dict]:", "new_string": "def entrainer(segments: … [113 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py", "old_string": "        if perte_prec is not None and abs(perte_prec - perte) < 1e-9:\n            arret += 1\n            if arret >= 15:\n                break\n        else:\n            a … [829 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"epochs: int = 1500\\|default=1500\\|rang0_ok\\|repere = \" tools/tests/linguistique/classement_cible.py", "description": "Repérer les défauts d'époques et le repère"}`

  ```
425:             epochs: int = 1500, lr: float = 0.6, l2: float = 0.01) -> dict:
552:    rang0_ok = 0
557:        rang0_ok += int(s["candidats"][0]["texte"] == s["cible"])
558:    repere = {"exactitude_entrainement": _taux(app_ok, app_n),
559:              "rang0_justes": rang0_ok, "rang0_taux": _taux(rang0_ok, app_n)}
664:    ap.add_argument("--epochs", type=int, default=1500)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport re, pathlib\np=pathlib.Path(\"tools/tests/linguistique/classement_cible.py\")\nt=p.read_text(encoding=\"utf-8\")\nt=t.replace(\"epochs: int = 1500, lr: float = 0.6, l2: float = 0.01) -> dict:\",\n            … [322 caractères tronqués]`

  ```
ok
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py", "offset": 544, "limit": 22}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py</path>
<type>file</type>
<content>
544:                                 - _moy([r["regle"] for r in stabilite_res]), 4),
545:         }
546:     else:
547:         stabilite_resume = {}
548: 
549:     # repères : accuracy d'entraînement (sur-apprentissage) et rang 0 (prior de proximité)
550:     app_ok = 0
551:     app_n = 0
552:     rang0_ok = 0
553:     for s in segments_tries:
554:         pred_train, _ = _predire(modeles[s["parite"]], s)
555:         app_ok += int(pred_train == s["cible"])
556:         app_n += 1
557:         rang0_ok += int(s["candidats"][0]["texte"] == s["cible"])
558:     repere = {"exactitude_entrainement": _taux(app_ok, app_n),
559:               "rang0_justes": rang0_ok, "rang0_taux": _taux(rang0_ok, app_n)}
560: 
561:     # ablations : que porte le résultat ? On retire des groupes de features, à modèle égal.
562:     ablations = {}
563:     for nom, masque in (
564:         ("sans_rang", {"rang"}),
565:         ("sans_prior_de_position", {"rang", "distance", "cote_gauche", "cote_dedans"}),

(Showing lines 544-565 of 713. Use offset=566 to continue.)
</conte
… [3 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py", "old_string": "    app_ok = 0\n    app_n = 0\n    rang0_ok = 0\n    for s in segments_tries:\n        pred_train, _ = _predire(modeles[s[\"parite\"]], s)\n        app_ok += int(pred_train == … [1093 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py has been updated successfully.
  ```

### 🤖 Assistant

⏵ Run de convergence (max 6000 époques) et chronométrage

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && time python3 tools/tests/linguistique/classement_cible.py --json /tmp/classement.json --stabilite 10 --verbeux 2>&1 | tail -45", "description": "Run convergence", "timeoutMs": 600000}`

  ```
== corpus ==
{"phrases": 612, "segments_gold_avec_cible": 239, "span_non_predit": 94}
{"pairs": 79, "impairs": 66}
== par sens ==
pairs->impairs: modèle 66/66 (1.0000) | règle 60/66 (0.9091) | hasard 0.3485
impairs->pairs: modèle 76/79 (0.9620) | règle 63/79 (0.7975) | hasard 0.3671
== regroupé hors-pli ==
modèle 142/145 (0.9793) | règle 123/145 (0.8483)
moyenne des sens: {'modele': 0.981, 'regle_actuelle': 0.8533, 'gain': 0.1277}
McNemar: {'modele_juste_regle_fausse': 21, 'regle_juste_modele_fausse': 2, 'p_exact': 6.6e-05}
bootstrap: {'tirages': 2000, 'difference': 0.131, 'ic95': [0.069, 0.2]}
hasard vivier attendu: 0.3876
repères: {'exactitude_entrainement': 0.9931, 'rang0_justes': 139, 'rang0_taux': 0.9586, 'rang0_par_type': {'GP': {'n': 83, 'justes': 78, 'taux': 0.9398}, 'REL': {'n': 26, 'justes': 26, 'taux': 1.0}, 'SUB': {'n': 36, 'justes': 35, 'taux': 0.9722}}}
ablations: {'sans_rang': 0.9379, 'sans_prior_de_position': 0.6276, 'sans_interactions': 0.9724, 'sans_nature': 0.9586}
hors vivier unique: {'n': 140, 'modele': 0.9786, 'regle_actuelle': 0.85, 'segments_vivier_unique': 5}
stabilité: {'decoupages': 10, 'modele_moyen': 0.9807, 'modele_ecart_type': 0.0153, 'regle_moyenne':
… [846 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nd=json.load(open(\"/tmp/classement.json\"))\nfor nom,b in d[\"resultats\"][\"sens\"].items():\n    e=b[\"entrainement\"]\n    print(nom, \"epochs\",e[\"epochs_effectues\"],\"perte\",e[\"perte_finale\"] … [336 caractères tronqués]`

  ```
pairs->impairs epochs 1977 perte 52.18016 moy 0.232947 lignes 224
impairs->pairs epochs 1538 perte 31.788506 moy 0.166432 lignes 191
poids par pli (écarts)
biais             +0.9202  +0.2282  mm
distance          -0.4672  -0.7848  mm
rang              -3.2328  -3.4390  mm
longueur          -0.4167  +0.0380  !!
cote_gauche       +0.7475  +1.5152  mm
cote_dedans       -1.0414  -0.5736  mm
type_GP           -0.4177  -0.6029  mm
type_REL          +0.0144  +0.2272  mm
prep_gen          -0.0796  -0.1608  mm
prep_dat          -0.1618  +0.0133  !!
prep_loc          -0.1600  -0.2805  mm
prep_but          -0.0048  -0.1194  mm
prep_moy          -0.1098  -0.0032  mm
prep_autre        +0.0983  -0.0524  !!
nat_verbe         +1.0908  +0.6701  mm
pos_verbe         +0.0271  +0.6313  mm
pos_nom           +0.0691  +0.0838  mm
GP_x_verbe        +0.8998  +0.7798  mm
REL_x_verbe       -0.0849  -0.3449  mm
SUB_x_verbe       +0.2759  +0.2352  mm
GP_x_posV         -0.0240  +0.5705  !!
REL_x_posV        -0.0286  -0.1624  mm
SUB_x_posV        +0.0797  +0.2231  mm
GEN_x_verbe       -0.1899  +0.0000  !!
GEN_x_posV        -0.1899  +0.0791  !!
  ```

### 🤖 Assistant

⏵ Test de sensibilité aux hyperparamètres (hors protocole, pour la robustesse)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for l2 in 0.001 0.01 0.1; do for ep in 500 6000; do out=$(python3 tools/tests/linguistique/classement_cible.py --json /tmp/sens.json --stabilite 0 --epochs $ep --l2 $l2 2>/dev/null | grep \"regroupé\" -A1); echo \"l2=$l2 epochs=$ep : … [107 caractères tronqués]`

  ```
l2=0.001 epochs=500 :: == regroupé hors-pli == modèle 142/145 (0.9793) | règle 123/145 (0.8483) 
l2=0.001 epochs=6000 :: == regroupé hors-pli == modèle 141/145 (0.9724) | règle 123/145 (0.8483) 
l2=0.01 epochs=500 :: == regroupé hors-pli == modèle 142/145 (0.9793) | règle 123/145 (0.8483) 
l2=0.01 epochs=6000 :: == regroupé hors-pli == modèle 142/145 (0.9793) | règle 123/145 (0.8483) 
l2=0.1 epochs=500 :: == regroupé hors-pli == modèle 142/145 (0.9793) | règle 123/145 (0.8483) 
l2=0.1 epochs=6000 :: == regroupé hors-pli == modèle 142/145 (0.9793) | règle 123/145 (0.8483)
  ```

### 🤖 Assistant

⏵ Identifier la ligne de roadmap liée à l'attachement (pour la fiche)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n -i \"attachement\\|B13\\|cible\" docs/pilotage/roadmap.md | head -20", "description": "Chercher la ligne roadmap attachement"}`

  ```
23:  native ; R est la **nouvelle ligne lecteur**, qui donne une cible mesurable aux deux autres. On [charge](../theorie/glossaire/entrees/charge-flux-chargeflux.md) **un**
31:| **B — l'intelligence** | langue, pensée, jeux, maîtres, [banc externe](../theorie/glossaire/entrees/banc-externe.md), sémantique, modules | ✅ B1–B12 ; **B1.5 [corpus](../theorie/glossaire/entrees/corpus.md)**, **B12.10, B10.2bis et B11.10 closes** ; le **décodeur** est levé (objectif mot : 32,5 ; JW 26,7), le `z` reste ; **B13** (moteur de pensée) : state store v0 + **AC-3/alpha-bêta** + **[DRVF](../theorie/glossaire/entrees/drvf.md) `thought`** + **[banc](../theorie/glossaire/entrees/banc.md) anytime** + **opérateurs hétérogènes** + **nécessaire** + **labyrinthe** + **[porte](../theorie/glossaire/entrees/porte.md)** + **apprise** + **courbe** + **seule** + **stochastique** + **sto seule** + **ferme** + **minute** + **minute apprise** + **minute seule** + **minute entraînée** + **shaping** + **réseau** + **MLP** + **[professeur](../theorie/glossaire/entrees/professeur.md)** + **sans None** + **correction** + **audit** + **ouverte** + **graines** + **mobile** + **mobile graines** + **bruit** + **bouge** + **
… [7127 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Ajout du bloc de sensibilité aux hyperparamètres

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py", "old_string": "    # hors segments à vivier unique : la mesure ne dépend pas du classement\n    uniques = [s for s in segments_tries if len(s[\"candidats\"]) == 1]", "new_string": "    # sen … [556 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py", "old_string": "                      \"ablations_hors_pli\": ablations,\n                      \"hors_vivier_unique\": hors_uniques},", "new_string": "                      \"ablations_hors_ … [150 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py", "old_string": "    print(\"ablations:\", {k: v[\"taux\"] for k, v in r[\"ablations_hors_pli\"].items()})\n    print(\"hors vivier unique:\", r[\"hors_vivier_unique\"])", "new_string": "    p … [251 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py has been updated successfully.
  ```

### 🤖 Assistant

⏵ Relecture complète du prototype avant le run final

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py", "offset": 1, "limit": 210}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py</path>
<type>file</type>
<content>
1: """classement_cible.py — prototype **autonome** d'un classement appris des candidats d'attachement.
2: 
3: Le problème. `bloc_linguistique.Heuristique` choisit la cible d'un segment par **type +
4: proximité** (REL/SUB → antécédent nominal à gauche, GP → verbe du GV le plus proche). Sur les
5: segments gold dont le span est prédit, cette règle donne **123/145** en égalité exacte. Ce
6: fichier teste une autre sélection : un **score linéaire appris** sur des features lisibles,
7: candidat par candidat, sans toucher à `bloc_linguistique.py` (l'intégration éventuelle est une
8: autre décision).
9: 
10: Protocole (pré-enregistré ici, avant de regarder les scores).
11: 
12: 1. On garde les segments gold qui portent une cible (`cibles`) **et** dont le span
13:    `(type, debut, fin)` est prédit par l'heuristique — exactement les 145 segments de la
14:    mesure courante (123/145). Le gold et la mesure sont ceux de `evaluer_gold.py`.
15: 2. Pour chaque segment, le **vivier** est l'ensemble des tokens pleins de la phrase : POS
16:    ouverte (`NOUN`, `PRO
… [9053 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py", "offset": 210, "limit": 220}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py</path>
<type>file</type>
<content>
210:                 c["rang"] = rang
211:                 c["x"] = _vecteur(s["type"], prep, c, len(candidats))
212:                 c["positif"] = int(c["texte"] == cibles[0])
213:             positif = sum(c["positif"] for c in candidats)
214:             if positif == 0:
215:                 stats["cible_hors_vivier"] += 1
216:             att = (etiquette.meta or {}).get("attachement") or {}
217:             segments.append({
218:                 "id": phrase["id"], "source": phrase["source"], "parite": _parite(phrase["id"]),
219:                 "texte": phrase["texte"], "type": s["type"], "segment": s.get("texte", ""),
220:                 "cible": cibles[0], "prep": prep, "pred_actuelle": (att.get("cible") or "").strip(),
221:                 "ok_actuelle": (att.get("cible") or "").strip() == cibles[0],
222:                 "candidats": candidats,
223:             })
224:     return segments, dict(stats)
225: 
226: 
227: def _vecteur(type_segment: str, prep: str, c: dict, n: int) -> list[float]:
228:     verbe = 1.0 if c["verbe_lex"] else 0.0
… [8898 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py", "offset": 430, "limit": 180}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py</path>
<type>file</type>
<content>
430:     segments_tries = sorted(segments, key=lambda s: (s["parite"], s["id"]))
431:     compte_parite = Counter(s["parite"] for s in segments_tries)
432: 
433:     def entrainer_sur(parite: int):
434:         return entrainer([s for s in segments_tries if s["parite"] == parite],
435:                          epochs=epochs, lr=lr, l2=l2)
436: 
437:     modeles, infos = {}, {}
438:     for parite in (0, 1):
439:         w, info = entrainer_sur(parite)
440:         modeles[parite] = w
441:         infos[parite] = info
442: 
443:     sens = {}
444:     for parite_train in (0, 1):
445:         test = [s for s in segments_tries if s["parite"] != parite_train]
446:         train = [s for s in segments_tries if s["parite"] == parite_train]
447:         modele = modeles[parite_train]
448:         res_modele = evaluer(modele, test)
449:         res_regle = evaluer_regle(test)
450:         res_hasard = evaluer_hasard(test, random.Random(graine))
451:         sens[f"{'pairs' if parite_train == 0 else 'impairs'}->{'impairs' if parite_train == 0 else 'pairs'}"] 
… [8461 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérifier l'unicité des ids par segment (bootstrap) et corriger

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, collections\nd=json.load(open(\"/tmp/classement.json\"))\nc=collections.Counter(s[\"id\"] for s in d[\"segments\"])\nprint(\"ids en double:\", {k:v for k,v in c.items() if v>1})\nprint(\"segments\",len … [147 caractères tronqués]`

  ```
ids en double: {}
segments 145 phrases distinctes 145
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py", "old_string": "Protocole (pré-enregistré ici, avant de regarder les scores).", "new_string": "Protocole (fixé ici). Limite assumée : le vivier, la liste des features et l'ordre de la liste\n … [162 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py", "old_string": "def evaluer_hasard(segments: list[dict], rng: random.Random) -> dict:\n    \"\"\"Deux hasards : uniforme dans le vivier, et tirage d'une cible parmi les distinctes.\"\"\"\n    … [347 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py", "old_string": "        segments_audit.append({\n            \"id\": s[\"id\"], \"source\": s[\"source\"], \"plis\": s[\"parite\"],", "new_string": "        segments_audit.append({\n          … [120 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py", "old_string": "    rng = random.Random(graine)\n    predictions = {s[\"id\"]: int(s[\"ok_modele\"]) for s in segments_audit}\n    regle_ok = {s[\"id\"]: int(s[\"ok_actuelle\"]) for s in segm … [678 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py has been updated successfully.
  ```

### 🤖 Assistant

⏵ Run final vers `reports/pensee-classement-appris.json`

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -m py_compile tools/tests/linguistique/classement_cible.py && echo \"compile ok\" && time python3 tools/tests/linguistique/classement_cible.py --stabilite 10 --verbeux 2>&1 | tail -50", "description": "Run final et compilatio … [24 caractères tronqués]`

  ```
compile ok
== corpus ==
{"phrases": 612, "segments_gold_avec_cible": 239, "span_non_predit": 94}
{"pairs": 79, "impairs": 66}
== par sens ==
pairs->impairs: modèle 66/66 (1.0000) | règle 62/66 (0.9394) | hasard 0.3485
impairs->pairs: modèle 76/79 (0.9620) | règle 67/79 (0.8481) | hasard 0.3671
== regroupé hors-pli ==
modèle 142/145 (0.9793) | règle 129/145 (0.8897)
moyenne des sens: {'modele': 0.981, 'regle_actuelle': 0.8938, 'gain': 0.0872}
McNemar: {'modele_juste_regle_fausse': 15, 'regle_juste_modele_fausse': 2, 'p_exact': 0.00235}
bootstrap: {'tirages': 2000, 'difference': 0.0897, 'ic95': [0.0345, 0.1448]}
hasard vivier attendu: 0.3876
repères: {'exactitude_entrainement': 0.9931, 'rang0_justes': 139, 'rang0_taux': 0.9586, 'rang0_par_type': {'GP': {'n': 83, 'justes': 78, 'taux': 0.9398}, 'REL': {'n': 26, 'justes': 26, 'taux': 1.0}, 'SUB': {'n': 36, 'justes': 35, 'taux': 0.9722}}}
ablations: {'sans_rang': 0.9379, 'sans_prior_de_position': 0.6276, 'sans_interactions': 0.9724, 'sans_nature': 0.9586}
sensibilité: {'l2=0.001,epochs=6000': 0.9724, 'l2=0.1,epochs=500': 0.9793, 'l2=0.1,epochs=6000': 0.9793}
hors vivier unique: {'n': 140, 'modele': 0.9786, 'regle_actuelle': 0.8929, 'segm
… [1034 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Alerte : la règle actuelle a bougé (123 → 129) pendant mes runs ; inspection

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short tools/bloc_linguistique.py tools/tests/linguistique/evaluer_gold.py && ls -l --time-style=full-iso tools/bloc_linguistique.py tools/tests/linguistique/evaluer_gold.py && git diff --stat tools/bloc_linguistique.py & … [103 caractères tronqués]`

  ```
M tools/bloc_linguistique.py
-rw-------. 1 stephane stephane 101602 2026-11-05 13:50:17.493577016 -0500 tools/bloc_linguistique.py
-rw-r--r--. 1 stephane stephane  14095 2026-11-05 10:54:02.946094475 -0500 tools/tests/linguistique/evaluer_gold.py
 tools/bloc_linguistique.py | 67 +++++++++++++++++++++++++++++++++++++++-------
 1 file changed, 58 insertions(+), 9 deletions(-)
diff --git a/tools/bloc_linguistique.py b/tools/bloc_linguistique.py
index 65fb0d76..cf80dc68 100644
--- a/tools/bloc_linguistique.py
+++ b/tools/bloc_linguistique.py
@@ -613,6 +613,21 @@ class Heuristique:
         except Exception:
             return {}
 
+    @staticmethod
+    def _tete_texte(texte: str) -> str | None:
+        """La tête d'un texte de candidat : le verbe plein s'il y en a un, sinon le dernier mot.
+
+        `« … → Le livre »` → `livre` ; `« … → Les fleurs poussent »` → `poussent` ;
+        `« … → est prêt »` → `prêt` (l'auxiliaire n'est pas la tête).
+        """
+        mots = re.findall(r"\b[ldmtsnLDMTNS]['’](?=\w)|[\wÀ-ÿ]+(?:['’\-][\wÀ-ÿ]+)*", texte)
+        if not mots:
+            return None
+        for m in mots:
+            if _est_verbe(m) and _normaliser(m) not in AUXILIAI
… [3476 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sha256sum tools/bloc_linguistique.py | cut -c1-16 && ls -l --time-style=full-iso tools/bloc_linguistique.py && python3 tools/tests/linguistique/evaluer_gold.py --json /tmp/eval_now.json >/dev/null 2>&1; python3 - <<'EOF'\nimport json … [254 caractères tronqués]`

  ```
6e28396a04fb9ac2
-rw-------. 1 stephane stephane 101338 2026-11-05 13:50:29.860379091 -0500 tools/bloc_linguistique.py
{'cibles': 239, 'labels': 145, 'exact': 129, 'exact_taux_span': 0.8897, 'top1_taux_span': 0.9103}
  ```

### 🤖 Assistant

⏵ Comparer les prédictions du modèle entre le run à 123 et le run à 129

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\na=json.load(open(\"/tmp/classement.json\"))   # run à 123\nb=json.load(open(\"reports/pensee-classement-appris.json\"))  # run à 129\nA={(s[\"id\"],s[\"type\"],s[\"segment\"]):s for s in a[\"segments\" … [1285 caractères tronqués]`

  ```
clés égales True 145 145
prédictions modèle différentes: 0
prédictions règle différentes: 6
viviers différents: 0
exact modèle 142 142
exact règle 123 129
== changements règle
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 20, in <module>
KeyError: (('s012', 'SUB', 'que Lucas trouve'), 'étoile', 'écoute')
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\na=json.load(open(\"/tmp/classement.json\")); b=json.load(open(\"reports/pensee-classement-appris.json\"))\nA={(s[\"id\"],s[\"type\"],s[\"segment\"]):s for s in a[\"segments\"]}\nB={(s[\"id\"],s[\"type\ … [336 caractères tronqués]`

  ```
s012 SUB | que Lucas trouve | étoile -> écoute | gold écoute | modèle écoute
s030 SUB | que le voyage crie | lettre -> cherche | gold cherche | modèle cherche
s052 SUB | que un sombre village trouve | cuisine -> ouvre | gold ouvre | modèle ouvre
s124 SUB | que elles compte | fenêtre -> commence | gold commence | modèle commence
s097 SUB | que cette chanson nage | chanson -> commence | gold commence | modèle commence
s139 SUB | que le calme nuage observe | lettre -> crie | gold crie | modèle crie
  ```

### 🤖 Assistant

⏵ Point au parent : dérive de la règle live et résultat stable

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -l --time-style=full-iso tools/bloc_linguistique.py && sha256sum tools/bloc_linguistique.py | cut -c1-16 && date \"+%H:%M:%S\"", "description": "Vérifier stabilité du fichier"}`

  ```
-rw-------. 1 stephane stephane 101568 2026-11-05 13:51:26.638852086 -0500 tools/bloc_linguistique.py
6e8430180ccca615
13:53:03
  ```

- **send_message** `{"agent_id": "e181ce02-cd50-488a-a6be-e84b79d40dcc", "message": "Point intermédiaire (prototype classement appris, autonome) :\n\n- Résultat stable : modèle appris **142/145** en exact sur les 145 segments au span prédit, hors-pli (pairs→impairs 66/66, impairs→pairs 76/79).\n- **Attention** : `tools … [1183 caractères tronqués]`

  ```
message delivered to agent e181ce02-cd50-488a-a6be-e84b79d40dcc
  ```

### 🤖 Assistant

⏵ Le fichier a encore changé ; inspection de la nouvelle règle et du score

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff tools/bloc_linguistique.py | sed -n '1,140p'", "description": "Voir le diff courant"}`

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

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/tests/linguistique/evaluer_gold.py --json /tmp/eval_now2.json >/dev/null 2>&1; python3 - <<'EOF'\nimport json\nd=json.load(open(\"/tmp/eval_now2.json\"))\na=d[\"heuristique\"][\"all\"][\"attachement\"]\nprint({k:a[k] fo … [127 caractères tronqués]`

  ```
{'labels': 145, 'exact': 137, 'exact_taux_span': 0.9448, 'top1_taux_span': 0.9655}
  ```

### 🤖 Assistant

⏵ La règle live est à 137/145 ; mesure du modèle sur cet état

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sha256sum tools/bloc_linguistique.py | cut -c1-16 && ls -l --time-style=full-iso tools/bloc_linguistique.py && time python3 tools/tests/linguistique/classement_cible.py --json /tmp/classement_live.json --stabilite 0 2>&1 | grep -E \" … [156 caractères tronqués]`

  ```
6e8430180ccca615
-rw-------. 1 stephane stephane 101568 2026-11-05 13:51:26.638852086 -0500 tools/bloc_linguistique.py
== par sens ==
pairs->impairs: modèle 66/66 (1.0000) | règle 64/66 (0.9697) | hasard 0.3485
impairs->pairs: modèle 76/79 (0.9620) | règle 73/79 (0.9241) | hasard 0.3671
== regroupé hors-pli ==
modèle 142/145 (0.9793) | règle 137/145 (0.9448)
hasard vivier attendu: 0.3876
repères: {'exactitude_entrainement': 0.9931, 'rang0_justes': 139, 'rang0_taux': 0.9586, 'rang0_par_type': {'GP': {'n': 83, 'justes': 78, 'taux': 0.9398}, 'REL': {'n': 26, 'justes': 26, 'taux': 1.0}, 'SUB': {'n': 36, 'justes': 35, 'taux': 0.9722}}}
ablations: {'sans_rang': 0.9586, 'sans_prior_de_position': 0.6552, 'sans_interactions': 0.9724, 'sans_nature': 0.9586}
sensibilité: {'l2=0.001,epochs=6000': 0.9724, 'l2=0.1,epochs=500': 0.9793, 'l2=0.1,epochs=6000': 0.9793}
[stderr]

real	0m16,648s
user	0m16,624s
sys	0m0,024s
  ```

### 🤖 Assistant

⏵ Analyser le gain résiduel (+5) face à la règle live à 137

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nd=json.load(open(\"/tmp/classement_live.json\"))\nprint(\"modèle\",sum(s[\"ok_modele\"] for s in d[\"segments\"]),\"règle\",sum(s[\"ok_actuelle\"] for s in d[\"segments\"]))\nprint(\"== règle fausse, m … [993 caractères tronqués]`

  ```
modèle 142 règle 137
== règle fausse, modèle juste
g002 GP | gold chat | règle '' -> chat | Le chat de la voisine dort.
g012 GP | gold prêt | règle 'manger' -> prêt | Le canard est prêt à manger.
r018 GP | gold prête | règle 'manger' -> prête | La souris est prête à manger.
s108 GP | gold rêve | règle 'papier' -> rêve | ce calme papier rêve sous le nuage
s122 GP | gold saute | règle 'papier' -> saute | mon papier saute vers les montagne
r309 SUB | gold viendra | règle 'Peut-être' -> viendra | Peut-être qu'il viendra.
s041 GP | gold marche | règle '' -> marche | les avocat marche devant elles
== règle juste, modèle faux
r048 GP | gold écrit | modèle lettre | Il écrit une lettre à sa sœur.
r068 GP | gold writes | modèle letter | He writes a letter to his sister.
== les deux faux
r230 SUB | gold appelle | règle 'appelle-moi' | modèle appelle-moi
McNemar {'modele_juste_regle_fausse': 7, 'regle_juste_modele_fausse': 2, 'p_exact': 0.179688}
bootstrap {'tirages': 2000, 'difference': 0.0345, 'ic95': [-0.0069, 0.0759]}
par type {"n": 145, "modele": {"justes": 142, "taux": 0.9793, "par_type": {"GP": {"n": 83, "justes": 81, "taux": 0.9759}, "REL": {"n": 26, "justes": 26, "taux": 1.0}, "SUB": 
… [247 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Ajout de l'empreinte du bloc au JSON et mise à jour du parent

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py", "old_string": "import argparse\nimport json\nimport math\nimport pathlib\nimport random\nimport re\nfrom collections import Counter", "new_string": "import argparse\nimport datetime\nimport  … [110 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py", "old_string": "def _parite(identifiant: str) -> int:\n    \"\"\"La moitié d'une phrase : la parité du nombre final de son id (`g001`, `r202`…).\"\"\"\n    m = re.search(r\"(\\d+)$\", identif … [791 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py", "old_string": "        \"titre\": \"Classement appris des candidats d'attachement (prototype autonome)\",\n        \"date\": \"2026-11-05\",\n        \"graine\": graine,", "new_string": "    … [214 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py has been updated successfully.
  ```

- **send_message** `{"agent_id": "e181ce02-cd50-488a-a6be-e84b79d40dcc", "message": "Mise à jour importante (ta règle live monte) :\n\n- Ta version actuelle de `bloc_linguistique.py` (empreinte sha256 **6e8430180ccca615**, mtime 13:51:26) donne **137/145** (0,9448) en exact sur les spans prédits. Tu as ajouté fly/climb … [1492 caractères tronqués]`

  ```
message delivered to agent e181ce02-cd50-488a-a6be-e84b79d40dcc
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -l --time-style=full-iso tools/bloc_linguistique.py && sha256sum tools/bloc_linguistique.py | cut -c1-16 && date \"+%H:%M:%S\"", "description": "Vérifier l'état du bloc"}`

  ```
-rw-------. 1 stephane stephane 101568 2026-11-05 13:51:26.638852086 -0500 tools/bloc_linguistique.py
6e8430180ccca615
13:56:24
  ```

### 🤖 Assistant

⏵ Ajout de la note sur la dérive et du run final à l'empreinte courante

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py", "old_string": "        \"graine\": graine,\n        \"empreinte_bloc_linguistique\": _empreinte_bloc(),", "new_string": "        \"graine\": graine,\n        \"empreinte_bloc_linguistique\": … [522 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py", "old_string": "    print(\"== corpus ==\")\n    print(json.dumps({k: resultat[\"corpus\"][k] for k in\n                      (\"phrases\", \"segments_gold_avec_cible\", \"span_non_predit\")} … [348 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py", "old_string": "proximité** (REL/SUB → antécédent nominal à gauche, GP → verbe du GV le plus proche). Sur les\nsegments gold dont le span est prédit, cette règle donne **123/145** en égalité  … [835 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py has been updated successfully.
  ```

### 🤖 Assistant

⏵ Run final (photo de l'empreinte 6e843018) et vérification

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sha256sum tools/bloc_linguistique.py | cut -c1-16 && python3 -m py_compile tools/tests/linguistique/classement_cible.py && time python3 tools/tests/linguistique/classement_cible.py --stabilite 10 --verbeux 2>&1 | tail -48 && sha256su … [112 caractères tronqués]`

  ```
6e8430180ccca615
== corpus ==
bloc: {'fichier': 'tools/bloc_linguistique.py', 'sha256_16': '6e8430180ccca615', 'octets': 101568, 'mtime': '2026-11-05T13:51:26'}
{"phrases": 612, "segments_gold_avec_cible": 239, "span_non_predit": 94}
{"pairs": 79, "impairs": 66}
== par sens ==
pairs->impairs: modèle 66/66 (1.0000) | règle 64/66 (0.9697) | hasard 0.3485
impairs->pairs: modèle 76/79 (0.9620) | règle 73/79 (0.9241) | hasard 0.3671
== regroupé hors-pli ==
modèle 142/145 (0.9793) | règle 137/145 (0.9448)
moyenne des sens: {'modele': 0.981, 'regle_actuelle': 0.9469, 'gain': 0.0341}
McNemar: {'modele_juste_regle_fausse': 7, 'regle_juste_modele_fausse': 2, 'p_exact': 0.179688}
bootstrap: {'tirages': 2000, 'difference': 0.0345, 'ic95': [-0.0069, 0.0759]}
hasard vivier attendu: 0.3876
repères: {'exactitude_entrainement': 0.9931, 'rang0_justes': 139, 'rang0_taux': 0.9586, 'rang0_par_type': {'GP': {'n': 83, 'justes': 78, 'taux': 0.9398}, 'REL': {'n': 26, 'justes': 26, 'taux': 1.0}, 'SUB': {'n': 36, 'justes': 35, 'taux': 0.9722}}}
ablations: {'sans_rang': 0.9586, 'sans_prior_de_position': 0.6552, 'sans_interactions': 0.9724, 'sans_nature': 0.9586}
sensibilité: {'l2=0.001,epochs=6000': 0.9724, '
… [1187 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Extraire les chiffres finaux et les écarts pour la fiche

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nd=json.load(open(\"reports/pensee-classement-appris.json\"))\nprint(\"empreinte\",d[\"empreinte_bloc_linguistique\"])\nprint(\"sens\", {k:(v[\"modele\"][\"justes\"],v[\"modele\"][\"n\"],v[\"regle_actue … [1303 caractères tronqués]`

  ```
empreinte {'fichier': 'tools/bloc_linguistique.py', 'sha256_16': '6e8430180ccca615', 'octets': 101568, 'mtime': '2026-11-05T13:51:26'}
sens {'pairs->impairs': (66, 66, 64, 66, 0.3485), 'impairs->pairs': (76, 79, 73, 79, 0.3671)}
regroupe {'n': 145, 'modele': {'justes': 142, 'taux': 0.9793, 'par_type': {'GP': {'n': 83, 'justes': 81, 'taux': 0.9759}, 'REL': {'n': 26, 'justes': 26, 'taux': 1.0}, 'SUB': {'n': 36, 'justes': 35, 'taux': 0.9722}}}, 'regle_actuelle': {'justes': 137, 'taux': 0.9448, 'par_type': {'GP': {'n': 83, 'justes': 77, 'taux': 0.9277}, 'REL': {'n': 26, 'justes': 26, 'taux': 1.0}, 'SUB': {'n': 36, 'justes': 34, 'taux': 0.9444}}}}
moyenne {'modele': 0.981, 'regle_actuelle': 0.9469, 'gain': 0.0341}
mcnemar {'modele_juste_regle_fausse': 7, 'regle_juste_modele_fausse': 2, 'p_exact': 0.179688}
bootstrap {'tirages': 2000, 'difference': 0.0345, 'ic95': [-0.0069, 0.0759]}
hasard {'hasard_vivier_attendu': 0.3876, 'hasard_cibles_distinctes': 0.0097}
repere {'exactitude_entrainement': 0.9931, 'rang0_justes': 139, 'rang0_taux': 0.9586, 'rang0_par_type': {'GP': {'n': 83, 'justes': 78, 'taux': 0.9398}, 'REL': {'n': 26, 'justes': 26, 'taux': 1.0}, 'SUB': {'n': 36, 'justes': 35, 'taux
… [1470 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Test apparié modèle vs prior de rang (le gain du « appris »)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, math\nd=json.load(open(\"reports/pensee-classement-appris.json\"))\nb=c=0; fixes=[]; casses=[]\nfor s in d[\"segments\"]:\n    rang0 = s[\"candidats\"][0][\"texte\"] == s[\"cible\"]\n    modele = s[\"o … [841 caractères tronqués]`

  ```
modèle juste, rang0 faux: 3 ['g014', 'g016', 'g003']
rang0 juste, modèle faux: 0 []
McNemar exact p= 0.25
règle juste, rang0 faux: 5 ['g014', 'g016', 'r048', 'r068', 'g003']
rang0 juste, règle faux: 7 ['g002', 'g012', 'r018', 's108', 's122', 'r309', 's041']
p= 0.774414
  ```

### 🤖 Assistant

⏵ Rédaction de la fiche `reports/rapport-classement-appris.md`

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-classement-appris.md", "content": "# B13 — classement appris des candidats d'attachement : 142/145, mais la règle live est déjà à 137\n\n> **Ligne de roadmap** : **B13** (moteur de pensée, attachement) · **Date** : 2026-1 … [10944 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-classement-appris.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

### 🤖 Assistant

⏵ Correction de la table des poids (doublon) et d'une formulation

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-classement-appris.md", "old_string": "| rang | -3,112 | -3,380 | **-3,246** |\n| cote_gauche | +0,760 | +1,526 | **+1,143** |\n| cote_dedans | -1,054 | -0,580 | **-0,817** |\n| nat_verbe (`_est_verbe`) | +1,172 | +0,735 | … [625 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-classement-appris.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-classement-appris.md", "old_string": "4. **Les 8 erreurs de la règle live** : `g002` et `s041` (cible vide sur le doublon d'union), `g012` / `r018` (« à manger » → `manger` au lieu de `prêt` / `prête`), `s108` / `s122` (n … [548 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-classement-appris.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-classement-appris.md", "old_string": "3. **La préférence verbe / nom intérieur** (g012, r018, s108, s122) : +4, mais elle casse r048 / r068 si elle n'est pas gardée par le lexique — à traiter seulement si le lexique verba … [221 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-classement-appris.md has been updated successfully.
  ```

### 🤖 Assistant

⏵ Vérification du JSON, des liens et de l'état du dépôt

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -m json.tool reports/pensee-classement-appris.json > /dev/null && echo \"JSON valide\" && ls -l reports/rapport-classement-appris.md reports/pensee-classement-appris.json tools/tests/linguistique/classement_cible.py && python … [493 caractères tronqués]`

  ```
JSON valide
-rw-r--r--. 1 stephane stephane 135906  5 nov 13:58 reports/pensee-classement-appris.json
-rw-------. 1 stephane stephane  11291  5 nov 14:02 reports/rapport-classement-appris.md
-rw-------. 1 stephane stephane  34857  5 nov 13:57 tools/tests/linguistique/classement_cible.py
clés ['titre', 'date', 'graine', 'empreinte_bloc_linguistique', 'note_regle_actuelle', 'hyperparametres', 'corpus', 'protocole', 'features', 'poids', 'resultats', 'controle_negatif', 'stabilite_decoupages_aleatoires', 'limites', 'segments']
segments audités 145
../tools/tests/linguistique/classement_cible.py OK
pensee-classement-appris.json OK
../tools/bloc_linguistique.py OK
../tools/tests/linguistique/classement_cible.py OK
pensee-classement-appris.json OK
../tools/bloc_linguistique.py OK
../tools/tests/linguistique/evaluer_gold.py OK
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -l --time-style=full-iso tools/bloc_linguistique.py && sha256sum tools/bloc_linguistique.py | cut -c1-16 && git status --short | grep -E \"classement|pensee-classement|rapport-classement|bloc_linguistique|evaluer_gold\"", "descrip … [36 caractères tronqués]`

  ```
-rw-------. 1 stephane stephane 101568 2026-11-05 13:51:26.638852086 -0500 tools/bloc_linguistique.py
6e8430180ccca615
 M tools/bloc_linguistique.py
 M tools/tests/linguistique/evaluer_gold.py
?? reports/pensee-classement-appris.json
?? reports/rapport-classement-appris.md
?? tools/tests/linguistique/classement_cible.py
  ```

### 🤖 Assistant

⏵ `evaluer_gold.py` a aussi été modifié ; vérifier l'impact sur `charger()`

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -l --time-style=full-iso tools/tests/linguistique/evaluer_gold.py && git diff tools/tests/linguistique/evaluer_gold.py | head -80", "description": "Diff de evaluer_gold.py"}`

  ```
-rw-r--r--. 1 stephane stephane 14489 2026-11-05 13:51:45.675060894 -0500 tools/tests/linguistique/evaluer_gold.py
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
+            if (pos_cible == "VERB") if pos_cible else bl
… [112 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Revue de documentation (lecture seule) pour valider la fiche

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py 2>&1 | tail -30; echo \"code=$?\"", "description": "Revue de documentation", "timeoutMs": 300000}`

  ```
revue de documentation · 645 fiche(s) · 738 JSON · 120 doc(s) · 83 porte(s) · 8 chapitre(s)
  ❌ 2 anomalie(s) :
     · compteurs : en-cours.md dit 641 fichiers, le disque en a 645
     · compteurs : en-cours.md dit 734 JSON, le disque en a 738
code=0
  ```

### 🤖 Assistant

⏵ Test de reproduction depuis un autre répertoire et lint éventuel

- **bash** `{"command": "cd /tmp && python3 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/classement_cible.py --json /tmp/repro.json --stabilite 0 2>&1 | grep -E \"bloc:|regroupé|modèle |McNemar\" ; python3 - <<'EOF'\nimport json\na=json.load(open(\"/tmp/repro.json\")); b=json.load(op … [450 caractères tronqués]`

  ```
bloc: {'fichier': 'tools/bloc_linguistique.py', 'sha256_16': '6e8430180ccca615', 'octets': 101568, 'mtime': '2026-11-05T13:51:26'}
pairs->impairs: modèle 66/66 (1.0000) | règle 64/66 (0.9697) | hasard 0.3485
impairs->pairs: modèle 76/79 (0.9620) | règle 73/79 (0.9241) | hasard 0.3671
== regroupé hors-pli ==
modèle 142/145 (0.9793) | règle 137/145 (0.9448)
McNemar: {'modele_juste_regle_fausse': 7, 'regle_juste_modele_fausse': 2, 'p_exact': 0.179688}
mêmes prédictions: True
modèle 142 règle 137
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && (ruff --version 2>/dev/null || echo \"pas de ruff\") && ls pyproject.toml setup.cfg .ruff.toml 2>/dev/null", "description": "Vérifier l'outil de lint"}`

  ```
pas de ruff
[exit code: 2]
  ```

### 🤖 Assistant

⏵ Relecture finale de la fiche et du JSON

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-classement-appris.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-classement-appris.md</path>
<type>file</type>
<content>
1: # B13 — classement appris des candidats d'attachement : 142/145, mais la règle live est déjà à 137
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, attachement) · **Date** : 2026-11-05 · **Verdict** : ❌ **ne pas intégrer le classement appris en l'état** ; le signal utile est le **vivier ordonné** (rang 0 : 139/145), à tester.
4: >
5: > **142/145 (0,9793)** hors-pli contre **137/145 (0,9448)** pour la règle live (empreinte `6e843018`, 13:51) : **+5**, McNemar 7/2, **p = 0,18**, IC 95 % bootstrap **[-0,7 ; +7,6] pts** → **non significatif**. Contre la référence de la consigne (123/145), le même modèle donne **+19** (McNemar 21/2, p = 6,6e-05) : la règle live a absorbé l'essentiel pendant la session. Le prototype ne lit pas la cible choisie par la règle ; ses **142/145 ne bougent pas** quand la règle passe de 123 à 137.
6: >
7: > **Dispositif** : [`classement_cible.py`](../tools/tests/linguistique/classement_cible.py), JSON [`pensee-classement-appris.json`](pensee-classement-appris.json). [`bloc_linguistique.py`](../tools/bloc_linguistique.py) **no
… [10394 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-classement-appris.md", "old_string": "> **142/145 (0,9793)** hors-pli contre **137/145 (0,9448)** pour la règle live (empreinte `6e843018`, 13:51) : **+5**, McNemar 7/2, **p = 0,18**, IC 95 % bootstrap **[-0,7 ; +7,6] pts … [852 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-classement-appris.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-classement-appris.md", "old_string": "État intermédiaire : à 129/145 (empreinte `6e28396a`), le modèle donnait déjà 142, les deux sens 62/66 et 67/79. Les six cas réparés par la règle entre 123 et 129 sont les SUB synthét … [312 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-classement-appris.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -l --time-style=full-iso tools/bloc_linguistique.py tools/tests/linguistique/evaluer_gold.py && sha256sum tools/bloc_linguistique.py | cut -c1-16 && date \"+%H:%M:%S\"", "description": "Vérifier si le bloc a encore bougé"}`

  ```
-rw-------. 1 stephane stephane 101568 2026-11-05 13:51:26.638852086 -0500 tools/bloc_linguistique.py
-rw-r--r--. 1 stephane stephane  14489 2026-11-05 13:51:45.675060894 -0500 tools/tests/linguistique/evaluer_gold.py
6e8430180ccca615
14:06:01
  ```

### 🤖 Assistant

⏵ Contrôle programmatique de cohérence fiche ↔ JSON

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, re, pathlib\nd=json.load(open(\"reports/pensee-classement-appris.json\"))\nt=pathlib.Path(\"reports/rapport-classement-appris.md\").read_text(encoding=\"utf-8\")\nr=d[\"resultats\"]; g=r[\"regroupe_hor … [1317 caractères tronqués]`

  ```
OK modèle 142
OK règle 137
OK sens pairs 66
OK sens impairs 76
OK regle pairs 64
OK regle impairs 73
OK moyenne 0.981
OK rang0 139
OK mcnemar 7/2
OK bootstrap +0.0345
argmax incohérents: []
142/145 présent
137/145 présent
123/145 présent
0,9793 présent
0,9448 présent
p = 0,18 présent
6e843018 présent
B13 présent
Verdict présent
  ```

### 🤖 Assistant

⏵ Harmonisation des permissions des trois livrables

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && chmod 644 tools/tests/linguistique/classement_cible.py reports/rapport-classement-appris.md reports/pensee-classement-appris.json && ls -l tools/tests/linguistique/classement_cible.py reports/rapport-classement-appris.md reports/pens … [105 caractères tronqués]`

  ```
-rw-r--r--. 1 stephane stephane 135906  5 nov 13:58 reports/pensee-classement-appris.json
-rw-r--r--. 1 stephane stephane  11326  5 nov 14:05 reports/rapport-classement-appris.md
-rw-r--r--. 1 stephane stephane  34857  5 nov 13:57 tools/tests/linguistique/classement_cible.py
?? reports/rapport-annotation-independante.md
?? reports/rapport-audit-attachement.md
?? reports/rapport-classement-appris.md
?? reports/rapport-coherence-fiches.md
?? reports/rapport-contrat-s.md
?? reports/rapport-s-paragraphes.md
?? reports/rapport-topk-diagnostic.md
?? tools/tests/linguistique/classement_cible.py
  ```

### 🤖 Assistant

⏵ D'autres sous-agents travaillent sur l'attachement ; lecture rapide pour cohérence

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && head -40 reports/rapport-audit-attachement.md 2>/dev/null; echo \"-----\"; head -25 reports/rapport-topk-diagnostic.md 2>/dev/null", "description": "Lire les fiches voisines"}`

  ```
# Audit de reproductibilité — l'attachement du bloc linguistique (B13)

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 ·
> **Verdict** : ✅ **reproduit — 14/14 valeurs, écart 0** ; ⚠️ **réserve documentaire** :
> **3 des 5 JSON sont des instantanés antérieurs**, reproduits à leur commit mais pas à
> l'état courant. L'audit n'a modifié aucun fichier existant et n'a fait aucun commit.

> **Dispositif** : depuis la racine, `sys.path.insert(0, '.')` ;
> `from tools.bloc_linguistique import Heuristique` ;
> `from tools.tests.linguistique.evaluer_gold import charger, evaluer_bloc` ;
> `evaluer_bloc("heuristique", Heuristique(), charger())` pour l'attachement ; pour les spans,
> même boucle que `T166` : chaque `segment` du gold est comparé aux étiquettes de niveau
> `syntagme` par `(type, debut, fin)`. Mesure rejouée sur `s/v7`, commit **`e1171032`**,
> `bloc_linguistique.py` sha256 **`d9c9d559…`**, `evaluer_gold.py` sha256 **`dbbcfe90…`**,
> gold inchangé (612 phrases : 20 `hand` + 432 `reel` + 160 synthétiques). Durée : 0,45–0,55 s.
> Les cinq JSON sont lus dans leur version du commit **`e1171032`** ; la note de concurrence
> du § 3 dit ce qui a boug
… [2971 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Préciser 123 = état committé vs 137 = worktree dans la fiche

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path(\"reports/rapport-classement-appris.md\")\nt=p.read_text(encoding=\"utf-8\")\nt=t.replace(\"Contre la référence de la consigne (123/145), le même modèle donne\",\n            \"Contre … [1427 caractères tronqués]`

  ```
ok
5:> **142/145 (0,9793)** hors-pli contre **137/145 (0,9448)** pour la règle live (empreinte `6e843018`, 13:51) : **+5**, McNemar 7/2, **p = 0,18**, IC 95 % bootstrap **[-0,7 ; +7,6] pts** → **non significatif**. Contre la référence committée (123/145, audit `e1171032`), le même modèle donne **+19** (McNemar 21/2, p = 6,6e-05) : la règle live a absorbé l'essentiel pendant la session. Le classement ne lit pas la cible choisie par la règle (seule la comparaison la lit) ; ses **142/145 ne bougent pas** quand la règle passe de 123 à 137.
16:- **Empreinte** : les 123/145 sont l'état **committé** (audit `e1171032`) ; un autre agent a modifié `bloc_linguistique.py` pendant la session (129 puis 137/145 dans le worktree). Le JSON fige le fichier lu (`sha256[:16] = 6e843018`, 101 568 octets, mtime 13:51:26) ; les trois états sont rapportés ci-dessous.
20:| sens (test) | modèle appris | règle live 137 (worktree) | règle committée 123 |
27:Par type (regroupé) : GP **81/83** contre 77/83 (live) et 69/83 (consigne) ; REL **26/26** partout ; SUB **35/36** contre 34/36 et 28/36.
58:| règle committée (123) | 123/145 | 0,8483 |
86:- **La règle live bouge** : la fiche est une photo du worktree à l'
… [242 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path(\"reports/rapport-classement-appris.md\")\nt=p.read_text(encoding=\"utf-8\")\nt=t.replace(\"GP **81/83** contre 77/83 (live) et 69/83 (consigne)\",\n            \"GP **81/83** contre  … [219 caractères tronqués]`

  ```
ok
plus de 'consigne'
  ```

### 🤖 Assistant

⏵ Vérifier le commit de référence et l'état final

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log -1 --oneline && git diff --stat | tail -5 && git status --short | grep -E \"rapport-classement|pensee-classement|classement_cible\"", "description": "Commit HEAD et fichiers livrés"}`

  ```
e1171032 PILOTAGE — PROTOCOLE D'INTÉGRATION DES SOUS-AGENTS (REJOUER, REJETER, COMMITTER VÉRIFIÉ) ; § 9
 tools/pensee/autotest.py                           |   93 +-
 tools/structures                                   |    0
 tools/tests/linguistique/evaluer_gold.py           |    8 +-
 tools/tests/linguistique/gold_reel.py              |   10 +-
 32 files changed, 4196 insertions(+), 449 deletions(-)
?? reports/pensee-classement-appris.json
?? reports/rapport-classement-appris.md
?? tools/tests/linguistique/classement_cible.py
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short | grep -E \"gold|tests/linguistique\" && sha256sum tools/tests/linguistique/gold.json tools/tests/linguistique/gold_reel.json tools/tests/linguistique/gold_synthetique.json | cut -c1-16", "description": "Vérifier s … [19 caractères tronqués]`

  ```
M tools/tests/linguistique/evaluer_gold.py
 M tools/tests/linguistique/gold_reel.py
?? tools/tests/linguistique/classement_cible.py
3663be6cea2f22e2
05d4f6dfae67dc72
e3e704ce9cb599db
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-classement-appris.md", "old_string": "- **Population** : les 145 segments gold qui portent une cible (`cibles`) **et** dont le span `(type, debut, fin)` est prédit par l'heuristique — exactement la population de la mesure … [420 caractères tronqués]`

  ```
Error: cannot edit "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-classement-appris.md": file changed since it was read — re-read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-classement-appris.md", "offset": 9, "limit": 10}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-classement-appris.md</path>
<type>file</type>
<content>
9: ## 1. Protocole
10: 
11: - **Population** : les 145 segments gold qui portent une cible (`cibles`) **et** dont le span `(type, debut, fin)` est prédit par l'heuristique — exactement la population de la mesure d'attachement de `evaluer_gold.py` (GP 83, REL 26, SUB 36).
12: - **Vivier** : les tokens pleins de la phrase (POS ouverte ou `_est_verbe`), auxiliaires exclus. Construit sans le gold ; il contient la cible dans **144/145** cas (le cas manquant est `appelle` contre le token `appelle-moi`).
13: - **Features par candidat** : distance en tokens au segment, côté (gauche / droite / dedans), type du segment (GP/REL/SUB), préposition éventuelle (6 familles), longueur, nature `_est_verbe` et POS heuristique, rang dans la liste ordonnée **gauche → droite → dedans, puis distance**. S'y ajoutent des interactions lisibles (type × nature, génitif × nature) : 25 features au total.
14: - **Modèle** : régression logistique binaire (« ce candidat est-il la cible ? »), descente de gradient pleine bataille, L2 = 0,01, classes pondérées, arrêt sur convergence relative. 
… [714 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-classement-appris.md", "old_string": "- **Population** : les 145 segments gold qui portent une cible (`cibles`) **et** dont le span `(type, debut, fin)` est prédit par l'heuristique — exactement la population de la mesure … [420 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-classement-appris.md has been updated successfully.
  ```

### 🤖 Assistant

⏵ Vérifier les artefacts `__pycache__` éventuels et nettoyer

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -l tools/tests/linguistique/__pycache__/ 2>/dev/null | grep -i classement; git check-ignore -v tools/tests/linguistique/__pycache__/classement_cible.cpython-*.pyc 2>/dev/null; git status --short --ignored tools/tests/linguistique/ … [71 caractères tronqués]`

  ```
-rw-------. 1 stephane stephane  47190  5 nov 13:58 classement_cible.cpython-313.pyc
.gitignore:1:__pycache__/	tools/tests/linguistique/__pycache__/classement_cible.cpython-313.pyc
?? tools/tests/linguistique/classement_cible.py
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && target=\"/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/__pycache__/classement_cible.cpython-313.pyc\" && [ -f \"$target\" ] && rm -- \"$target\" && echo \"supprimé: $target\" && git status --short | grep -E … [85 caractères tronqués]`

  ```
supprimé: /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/__pycache__/classement_cible.cpython-313.pyc
?? reports/pensee-classement-appris.json
?? reports/rapport-classement-appris.md
?? tools/tests/linguistique/classement_cible.py
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"consigne\\|129\\|6e28396a\" reports/rapport-classement-appris.md; echo \"---\"; grep -n \"124\\|145\\|142\" reports/rapport-classement-appris.md | head -8; echo \"---\"; python3 -m json.tool reports/pensee-classement-appris … [92 caractères tronqués]`

  ```
16:- **Empreinte** : les 123/145 sont l'état **committé** (audit `e1171032`) ; un autre agent a modifié `bloc_linguistique.py` pendant la session (129 puis 137/145 dans le worktree). Le JSON fige le fichier lu (`sha256[:16] = 6e843018`, 101 568 octets, mtime 13:51:26) ; les trois états sont rapportés ci-dessous.
29:État intermédiaire mesuré pendant la session : à 129/145, le modèle donnait déjà 142, les deux sens 62/66 et 67/79. Les six cas réparés par la règle entre 123 et 129 sont les SUB synthétiques `s012`, `s030`, `s052`, `s097`, `s124`, `s139`.
---
1:# B13 — classement appris des candidats d'attachement : 142/145, mais la règle live est déjà à 137
3:> **Ligne de roadmap** : **B13** (moteur de pensée, attachement) · **Date** : 2026-11-05 · **Verdict** : ❌ **ne pas intégrer le classement appris en l'état** ; le signal utile est le **vivier ordonné** (rang 0 : 139/145), à tester.
5:> **142/145 (0,9793)** hors-pli contre **137/145 (0,9448)** pour la règle live (empreinte `6e843018`, 13:51) : **+5**, McNemar 7/2, **p = 0,18**, IC 95 % bootstrap **[-0,7 ; +7,6] pts** → **non significatif**. Contre la référence committée (123/145, audit `e1171032`), le même modèle donne **+19** (McN
… [1457 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Envoi du résultat complet au parent

- **send_message** `{"agent_id": "e181ce02-cd50-488a-a6be-e84b79d40dcc", "message": "Résultat — prototype autonome de classement appris des candidats d'attachement. Livrables **non committés** (je n'ai rien committé, ni modifié de fichier existant) :\n- `tools/tests/linguistique/classement_cible.py` (stdlib seulement ; … [4029 caractères tronqués]`

  ```
message delivered to agent e181ce02-cd50-488a-a6be-e84b79d40dcc
  ```

### 🤖 Assistant

⏵ Conclusion et résumé final

**Livrables créés (aucun fichier existant modifié, aucun commit) :**
- `tools/tests/linguistique/classement_cible.py` — prototype autonome, stdlib seule, n'écrit que le JSON.
- `reports/rapport-classement-appris.md` — fiche complète.
- `reports/pensee-classement-appris.json` — résultats, poids par pli, 145 prédictions auditées, empreinte du bloc.

**Protocole.** 145 segments gold au span prédit (GP 83, REL 26, SUB 36) ; vivier de tokens pleins construit sans le gold (cible couverte 144/145) ; features demandées + interactions type×nature et génitif×nature ; régression logistique maison (descente de gradient, L2, classes pondérées) ; split par parité d'id de phrase dans les deux sens, puis regroupé hors-pli.

**Taux d'exactitude :**

| | modèle appris | règle live 137 | règle committée 123 |
|---|---:|---:|---:|
| pairs → impairs (66) | **66 (1,0000)** | 64 (0,9697) | 60 (0,9091) |
| impairs → pairs (79) | **76 (0,9620)** | 73 (0,9241) | 63 (0,7975) |
| moyenne | **0,9810** | 0,9469 | 0,8533 |
| regroupé (145) | **142 (0,9793)** | 137 (0,9448) | 123 (0,8483) |

**Contrôles.** Hasard uniforme dans le vivier : 0,3876 attendu ; le **rang 0 seul** (premier candidat de la liste gauche→droite→dedans) fait déjà **139/145** (0,9586). Contre la règle live à 137 : **+5**, McNemar 7/2, **p = 0,18**, bootstrap **[−0,7 ; +7,6] pts** → non significatif. Contre l'état committé 123 : +19, p = 6,6e-05.

**Recommandation : ne pas intégrer le classement appris en l'état.** La règle live a absorbé l'essentiel pendant la session (123 → 129 → 137, empreinte `6e843018`) ; il ne reste que +5 non significatif, avec 2 régressions (`r048`, `r068`) et 25 poids pour +3 sur le simple prior de rang. En revanche, deux signaux sont à retenir : le **vivier ordonné** (139/145, gratuit) et le **fallback quand la cible est vide** (`g002`, `s041`, +2 sans risque). Le modèle à 142/145 reste la meilleure borne trouvée sur ce gold, mais son dessin de features a été informé par les 145 segments : il n'est pas validé pour un corpus neuf.

**Réserve de provenance :** `bloc_linguistique.py` et `evaluer_gold.py` ont été modifiés par d'autres agents pendant la session ; le JSON fige l'empreinte du bloc lu et le script se relance en ~25 s si la règle bouge encore.

