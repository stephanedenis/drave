# Session DSH — relecture

- identifiant : `session-9e0eeeb8-7572-4a68-a74e-7405d06e3757`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-16 02:13:27
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche V1 (exploitable, la suite du bilan T6) : `evaluer --strict` — le banc de recherche (`evaluer_gold.py`) mesure quatre modes et la cascade locale avec le plancher 0,70 ; le CLI ne le fait pas. Ajoute `--strict` à `evaluer` : mesure la **cascade locale** (`MockNeuronal`) sur 612 et le réel 452, **applique le plancher 0,70** (un échec = code 1), affiche les quatre modes (heuristique, neuronal, parallèle, cascade) et le delta ; le **contrôle négatif** (la cascade sous le plancher doit échouer). Fiche `reports/rapport-evaluer-strict.md` + JSON, un test, la doc § 3.3.

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

### 👤 Utilisateur

<system-reminder>
A skill is a reusable set of task-specific instructions. The following skills are available in this session:

<available_skills>
- `microsoft-foundry`: Deploy, evaluate, fine-tune, and manage Foundry agents end-to-end with azd: hosted agent scaffold/run/deploy, prompt agent create, batch eval, continuous eval, prompt optimizer, Agent Optimizer scaffold, agent.yaml, dataset curation from traces, model fine-tuning (SFT/DPO/RFT). USE FOR: azd ai agent, azd provision/deploy, deploy agent, hosted agent, create agent, add tool to agent, invoke agent, evaluate agent, continuous eval, continuous monitoring, agent CI/CD, optimize prompt, improve prom...
</available_skills>

If the user names a skill, or the task clearly matches a skill's description, call the `skill` tool with the exact skill name before taking task actions. Load all applicable skills, then follow their full instructions. This catalog contains summaries only; do not infer or follow a skill's instructions until it has been loaded.
A user may also invoke a skill directly; its <skill_content> block then appears in this conversation. Follow it, and do not call the `skill` tool again for that skill.
</system-reminder>

- **bash** `{"command": "ls -la && git status --short | head -50 && git log --oneline -5", "description": "List repo root and git state"}`

  ```
total 212
drwxr-xr-x. 1 stephane stephane   760 16 nov 02:01 .
drwxr-xr-x. 1 stephane stephane  2532  5 nov 10:41 ..
-rw-r--r--. 1 stephane stephane  9977  3 nov 09:19 AGENTS.md
drwxr-xr-x. 1 stephane stephane    40 25 sep 15:38 bench
drwxr-xr-x. 1 stephane stephane    42 16 nov 02:01 build
drwxr-xr-x. 1 stephane stephane    56 30 sep 12:20 colab
drwxr-xr-x. 1 stephane stephane  2664  2 nov 18:33 data
drwxr-xr-x. 1 stephane stephane    56 16 nov 00:38 dist
drwxr-xr-x. 1 stephane stephane   138 15 nov 22:25 docs
drwxr-xr-x. 1 stephane stephane    92 28 oct 16:25 drave-core
drwxr-xr-x. 1 stephane stephane   136 16 nov 02:01 drave.egg-info
drwxr-xr-x. 1 stephane stephane   220 16 nov 02:13 .git
-rw-r--r--. 1 stephane stephane   653 15 nov 22:25 .gitignore
-rw-r--r--. 1 stephane stephane   225  1 nov 10:50 .gitmodules
drwxr-xr-x. 1 stephane stephane  1012 16 nov 00:22 journal
drwxr-xr-x. 1 stephane stephane   100  3 nov 09:12 models
drwxr-xr-x. 1 stephane stephane   114 25 sep 15:24 __pycache__
-rw-------. 1 stephane stephane  1272 16 nov 01:44 pyproject.toml
drwxr-xr-x. 1 stephane stephane    64  6 nov 09:52 .pytest_cache
-rw-r--r--. 1 stephane stephane  4992 25 sep 10:54 Qtrinet-boot
… [2783 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"evaluer_gold\" --include=*.py --include=*.md --include=*.sh -l . | head -50", "description": "Find references to evaluer_gold"}`

  ```
./reports/rapport-pensee-gold-linguistique.md
./reports/rapport-pensee-gold-200.md
./reports/rapport-pensee-gold-200-subsets.md
./reports/rapport-pensee-gold-complexes.md
./reports/rapport-pensee-gold-complexes20.md
./reports/rapport-pensee-gold-complexes50.md
./reports/rapport-pensee-gold-complexes100.md
./reports/rapport-pensee-gold-discours.md
./reports/rapport-pensee-gold-342.md
./reports/rapport-pensee-segmenteur.md
./reports/rapport-pensee-segmenteur-hybride.md
./reports/rapport-pensee-segmenteur-union.md
./reports/rapport-pensee-segmenteur-defaut.md
./reports/rapport-pensee-cascade-union.md
./reports/rapport-pensee-cascade-tete.md
./reports/rapport-pensee-gold-gele.md
./reports/rapport-b13-porte-134.md
./reports/rapport-pensee-defaut-niveau.md
./reports/rapport-pensee-attachement.md
./reports/rapport-pensee-cibles.md
./reports/rapport-pensee-cibles-500.md
./reports/rapport-pensee-relation.md
./reports/rapport-pensee-roles.md
./reports/rapport-pensee-cible-proximite.md
./reports/rapport-pensee-candidats-verbes.md
./reports/rapport-pensee-echecs-attachement.md
./reports/rapport-pensee-verbe-gv.md
./reports/rapport-pensee-lexique-verbal.md
./reports/rapport-pensee-spans.md
./re
… [797 caractères tronqués]
  ```

- **bash** `{"command": "find . -name \"evaluer_gold.py\" -o -name \"*evaluer*\" | head -50", "description": "Find evaluer files"}`

  ```
./reports/evaluer-langue.json
./reports/rapport-evaluer-langue.md
./tools/evaluer_sft.py
./tools/tests/linguistique/__pycache__/evaluer_gold.cpython-313.pyc
./tools/tests/linguistique/evaluer_gold.py
./tools/evaluer_consignes.py
./build/lib/tools/evaluer_sft.py
./build/lib/tools/evaluer_consignes.py
./build/lib/tools/tests/linguistique/evaluer_gold.py
  ```

- **bash** `{"command": "grep -rn \"def .*evaluer\\|evaluer_gold\\|--strict\" tools/drave.py tools/*.py | head -80", "description": "Search evaluer in tools"}`

  ```
tools/drave.py:746:    """Charge `evaluer_gold.py` et vérifie que les gold de la roue sont là.
tools/drave.py:754:    chemin = dossier / "evaluer_gold.py"
tools/drave.py:768:    spec = importlib.util.spec_from_file_location("_drave_evaluer_gold", chemin)
tools/drave.py:890:def cmd_evaluer(args: argparse.Namespace) -> int:
tools/aligneur_litteraire.py:576:def evaluer_ancres(
tools/bloc_maths.py:282:def evaluer(noeud, env: dict | None = None):
tools/drave.py:746:    """Charge `evaluer_gold.py` et vérifie que les gold de la roue sont là.
tools/drave.py:754:    chemin = dossier / "evaluer_gold.py"
tools/drave.py:768:    spec = importlib.util.spec_from_file_location("_drave_evaluer_gold", chemin)
tools/drave.py:890:def cmd_evaluer(args: argparse.Namespace) -> int:
tools/essai_decharge.py:375:def evaluer(modele, ids, seq, lot, rap=None, max_lots=20):
tools/mesurer_contrat_json.py:98:    from tools.tests.linguistique.evaluer_gold import charger
tools/mesurer_robustesse_semaine.py:162:def _evaluer() -> dict:
tools/mesurer_schema_v2_doc.py:66:    from tools.tests.linguistique.evaluer_gold import charger
tools/ressources.py:31:  python3 tools/ressources.py --check [--strict]
tools/ressources
… [867 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,200p' tools/tests/linguistique/evaluer_gold.py", "description": "Read evaluer_gold.py start"}`

  ```
"""evaluer_gold.py — mesure le bloc linguistique sur le gold réel (20) + synthétique (160).

Trois niveaux : POS (token, exact), syntagmes (exact + **par tête**), pragmatique. Quatre
lectures : heuristique, mock neuronal, parallèle, cascade. Le vrai modèle est optionnel
(`--reel`) : s'il ne répond pas, il est refusé, pas simulé.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
from collections import Counter, defaultdict

RACINE = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RACINE / "tools"))
import bloc_linguistique as bl  # noqa: E402

GOLD = pathlib.Path(__file__).with_name("gold.json")
REEL = pathlib.Path(__file__).with_name("gold_reel.json")
SYNTH = pathlib.Path(__file__).with_name("gold_synthetique.json")


def charger() -> list[dict]:
    hand = json.loads(GOLD.read_text(encoding="utf-8"))["phrases"]
    reel = json.loads(REEL.read_text(encoding="utf-8"))["phrases"]
    synth = json.loads(SYNTH.read_text(encoding="utf-8"))["phrases"]
    for p in hand:
        p["source"] = "hand"
    for p in reel:
        p["source"] = "reel"
    return hand + reel + synth


GELE = pathlib.Path(__file__).with_name("gold_ge
… [8215 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '700,1050p' tools/drave.py", "description": "Read evaluer CLI section"}`

  ```
# un repli du tagger n'est pas un refus du texte : l'analyse est rendue
                print(f"{NOM}: tagger : refus partiel : {annotation.refus}", file=sys.stderr)
            else:
                # refus du texte : code 3, que la clé existe ou non
                if args.json:
                    sys.stdout.write(_dumps(annotation.json(avec_duree=duree)))
                else:
                    print(f"{NOM}: refus d'analyse : {annotation.refus} "
                          "(le texte doit contenir au moins une lettre ou un chiffre)",
                          file=sys.stderr)
                print(f"{NOM}: tagger auto · {auto.message()}", file=sys.stderr)
                return 3
        elif stats is not None:
            # un refus du tagger n'est pas un refus du texte : on le nomme, on ne le déguise pas
            pos = [e for e in annotation.etiquettes if e.niveau == "pos"]
            if not pos:
                print(f"{NOM}: tagger : {annotation.refus}", file=sys.stderr)
                return 1
            print(f"{NOM}: tagger : refus partiel : {annotation.refus}", file=sys.stderr)
        else:
            # un refus est une **réponse** : le JSON la porte, le code 
… [16470 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '200,520p' tools/tests/linguistique/evaluer_gold.py", "description": "Read remainder of evaluer_gold.py"}`

  ```
"exact_any_taux_span": round(att_exact_any / max(1, att_labels), 4),
                        # exactitude sur les segments au bon span : l'attachement seul
                        "top1_taux_span": round(att_top1 / max(1, att_labels), 4),
                        "topk_taux_span": round(att_topk / max(1, att_labels), 4),
                        "topk_exact": att_topk_exact,
                        "topk_exact_taux": round(att_topk_exact / max(1, att_n), 4),
                        "topk_exact_taux_span": round(att_topk_exact / max(1, att_labels), 4),
                        "exact_taux_span": round(att_exact / max(1, att_labels), 4),
                        "verbe": {"cibles": att_v_n, "justes": att_v_ok,
                                  "taux": round(att_v_ok / max(1, att_v_n), 4)},
                        "nom": {"cibles": att_n_n, "justes": att_n_ok,
                                "taux": round(att_n_ok / max(1, att_n_n), 4)},
                        "couverture": round(att_labels / max(1, att_n), 4),
                        "par_langue": {lg: {"cibles": v["cibles"], "labels": v["labels"],
                                            "exact": v["exact"], "topk": v["topk"],
     
… [5171 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"evaluer\\|MockNeuronal\\|cascade\\|plancher\\|0.70\\|0,70\\|seuil\" tools/drave.py | head -100", "description": "Search drave.py for relevant terms"}`

  ```
10:    python3 tools/drave.py evaluer
11:    python3 tools/drave.py evaluer --gold --json
15:    python3 tools/drave.py evaluer --tagger --json                    # heuristique + cascade API
29:En **option** (`--tagger`, `analyser` et `evaluer`), le POS (et lui seul) vient du tagger de
128:    Sans eux, `evaluer` ne peut pas inventer une référence : il sort en **4**, nomme les
210:    - **aucun appel réseau sans clé** : la cascade n'est même pas construite ;
220:    def __init__(self, heuristique: bl.Heuristique, cascade=None, stats: dict | None = None):
222:        self.cascade = cascade
224:        self.cle_presente = cascade is not None
233:        if self.cascade is not None and not self.panne:
235:                annotation = self.cascade.analyser(texte, langue, contexte)
264:        if self.cascade is None:
282:        if self.cascade is None:
288:            return f"{NOM} {VERSION} — analyse cascade POS (tagger auto : API DeepSeek, réseau)"
323:    """La cascade du tagger, avec le **refus** du neuronal reporté sur l'annotation fusionnée.
330:    nom = "cascade"
332:    def __init__(self, cascade, compose, stats: dict | None = None):
333:        self.cascade = cascade
336:  
… [4856 caractères tronqués]
  ```

- **bash** `{"command": "grep -rln \"bilan T6\\|T6\" reports docs journal | head -40", "description": "Find T6 references"}`

  ```
reports/rapport-pensee-ac3-alphabeta.md
reports/pensee-ac3-alphabeta.json
reports/rapport-pensee-drvf.md
reports/pensee-drvf.json
reports/rapport-pensee-hasard2.md
reports/rapport-pensee-intra.md
reports/rapport-pensee-asym.md
reports/rapport-pensee-rare.md
reports/rapport-pensee-tres-rare.md
reports/rapport-pensee-ultra-rare.md
reports/rapport-pensee-un-look.md
reports/rapport-pensee-look-tardif.md
reports/rapport-pensee-oubli.md
reports/rapport-pensee-oubli-fort.md
reports/rapport-pensee-oubli-total.md
reports/rapport-pensee-seuil.md
reports/INDEX.md
reports/rapport-bilan-exploitable.json
reports/rapport-bilan-exploitable.md
reports/README.md
docs/schemas/pipeline.mmd.svg
docs/pilotage/en-cours.md
docs/pilotage/roadmap.md
docs/implantation/moteur-de-pensee.md
journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/session.jsonl.zstd
journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/rapport.md
journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md
journal/sessions/27c99b10-c57e-4599-a23a-f7b1a54c17a1/session.jsonl.zstd
journal/sessions/27c99b10-c57e-4599-a23a-f7b1a54c17a1/digest.md
journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/session.jsonl.zstd
journal/sessions
… [704 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"MockNeuronal\\|ClasseNeuronal\\|class Cascade\\|class Parallele\" tools/bloc_linguistique.py | head -30", "description": "Find block classes"}`

  ```
8:  - `MockNeuronal` : une implémentation neuronale **de contrat**, déterministe, pour tester la
2136:class MockNeuronal:
2196:    `RefusNeuronal`. Le `MockNeuronal` sert aux tests de contrat, pas à la qualité.
2957:class Parallele:
2982:class Cascade:
3101:    n = MockNeuronal(profils)
3170:    n = MockNeuronal(profils)
  ```

- **bash** `{"command": "sed -n '1,240p' reports/rapport-bilan-exploitable.md", "description": "Read T6 bilan report"}`

  ```
# T6 — le bilan exploitable : installable, rejouable, mesuré, mais pas encore général

> **Ligne de roadmap** : **B13** (le produit) · **Tâche** : **T6** (clôture de la nuit
> exploitable) · **Date** : 2026-11-15 · **Verdict** : ✅ **les cinq briques T1–T5 tiennent
> ensemble** ; ❌ **trois limites restent nommées et bornées** (clone public dégradé, croissance
> O(k²), or de rôles humain absent).
>
> **Le chiffre, en une ligne.** Un débutant installe **`drave 0.1.0`** en **13,64 s** de machine
> (`pip install -e .`), lance **3/3** commandes, obtient un JSON **v2** de **5 899 octets** avec
> **2 139** candidats objets et **8** rôles normalisés ; **10 000 mots** passent en **4,01 s**
> (**2 493 mots/s**, **126 Mio**, **14,8 Mo** de JSON) ; la CLI rend **20/20** cas et **cinq
> codes** (0/3/4/5/1). Le **contrôle de linéarité échoue** (α = **1,55**), le **clone public**
> perd le sous-module S (attachement **88,70 %** au lieu de **99,58 %**), et le **gold de S**
> n'est pas un or humain indépendant. La passe complète **n'est pas relancée** : le relevé lu est
> celui du **15/11 09 h 53 → 12 h 15** (`work/portes-1115-09h53/`), **85 portes, 81 vertes,
> 4 rouges nommées**, plus le ciblage `
… [12587 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '2120,2220p' tools/bloc_linguistique.py && sed -n '2940,3040p' tools/bloc_linguistique.py", "description": "Read MockNeuronal and Cascade classes"}`

  ```
def _fusionner(spans: Sequence[Span]) -> list[Span]:
    spans = sorted(set(spans), key=lambda s: (s.debut, s.fin))
    sortie: list[Span] = []
    for s in spans:
        if not sortie or s.debut > sortie[-1].fin:
            sortie.append(s)
        else:
            sortie[-1] = Span(sortie[-1].debut, max(sortie[-1].fin, s.fin))
    return sortie


# --------------------------------------------------------------------------- neuronal


class MockNeuronal:
    """Le neuronal **de contrat** : même sortie, source `neuronal`, déterministe, sans GPU.

    Il ne prétend pas être un modèle : il prouve que le contrat accepte une autre implémentation,
    que le parallèle fusionne et que la cascade n'appelle le neuronal que sur le résidu.
    """

    nom = "neuronal"

    def __init__(self, profils: dict[str, dict] | None = None):
        self.profils = profils

    def analyser(self, texte: str, langue: str | None = None,
                 contexte: str | None = None) -> Annotation:
        t0 = time.perf_counter()
        lg = detecter_langue(texte, self.profils, langue)[0]
        if lg == "und" and langue:
            lg = langue
        script = detecter_script(texte)
        etique
… [8660 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"V1\\|T6\\|--strict\\|strict\" docs/pilotage/en-cours.md docs/pilotage/roadmap.md | head -60", "description": "Find V1/T6 mentions in state docs"}`

  ```
docs/pilotage/en-cours.md:75:- **Ce qu'elle fait** : **erratum 04/11** : la distillation native ne gagne rien à parité stricte ; `kd2` et `rope2048` **arrêtés** ; **paire propre** : **3,1500** → **3,1119** ; **2 048** ne bat pas 1 024 ; fiches [fenêtre](../../reports/rapport-n2-fenetre.md), [erratum](../../reports/rapport-n2-distillation-native.md), [porte](../../reports/rapport-n2-porte-propre.md).
docs/pilotage/en-cours.md:88:- **Panini** : **14 atomes** ; UDHR **418/438** ; J3.2 **5/21** langues, **V14 3/21** ; B2 **négatif** ; [atomes](../../reports/rapport-atomes-niveaux.md), [corpus](../../reports/rapport-corpus-commun.md), [B2](../../reports/rapport-atomes-prediction.md), [familles](../../reports/rapport-retrieval-familles.md).
docs/pilotage/en-cours.md:113:| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, F1 0,7902, 238/239, schéma v2, restit v1, produit T1–T6 ; U1 : α 1,08, 10 000 mots 0,82 s ; U2 : roue 1 727 201 o, mêmes JSON, sans gold → evaluer 4 ; U3 : profils 398 langues, 20/20, ambigu und** | **`g017` tranché** ; **J4** ; T132/T133, **[gold 452](../../reports/rapport-gold-452.md)** ; **B10.3 bloquée** |
docs/pilotage/en-c
… [16863 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1260,1360p' tools/drave.py && sed -n '1180,1260p' tools/drave.py", "description": "Read parser construction"}`

  ```
analyser.add_argument("--jsonl", action="store_true",
                          help="une ligne JSON par phrase (traitement de corpus)")
    analyser.add_argument("--contexte", default=None,
                          help="le texte qui précède (mémoire de discours : coréférence, connecteurs)")
    analyser.add_argument("--langue", choices=("fr", "en"), default=None,
                          help="indice de langue (fr/en) ; sans lui, le bloc détecte")
    analyser.add_argument("--profils", action="store_true",
                          help="détecter la langue avec les 398 profils UDHR (texte long) "
                               "et le prior des mots-outils (texte court) ; sans lui, le "
                               "repli à sept langues du bloc")
    analyser.add_argument("--tagger", action="store_true",
                          help="tagger POS par l'API DeepSeek (clé et réseau ; défaut : heuristique) ; "
                               "`--tagger auto` : API si une clé existe, sinon heuristique, sans "
                               "changer le code de sortie")
    analyser.add_argument("--tagger-auto", action="store_true", help=argparse.SUPPRESS)
    analyser.add_argument("
… [10120 caractères tronqués]
  ```

- **bash** `{"command": "grep -rln \"cascade locale\\|MockNeuronal\\|quatre modes\\|plancher 0,70\\|plancher 0.70\" reports docs journal | head -40", "description": "Find cascade local reports"}`

  ```
reports/rapport-coherence-docs-2.md
reports/rapport-bloc-linguistique.md
reports/rapport-pensee-cascade-union.md
reports/rapport-pensee-frontiere-71.md
reports/rapport-pensee-quatre-modes.md
reports/rapport-pensee-fusion-reparee.md
reports/rapport-pensee-defaut-niveau.md
reports/rapport-pensee-quatre-modes-432.md
reports/rapport-cout-chunker.md
reports/rapport-cache-chunker.md
reports/rapport-produit-v0.md
reports/rapport-file-taches.md
reports/pensee-file-taches.json
reports/rapport-produit-bloc-l.md
reports/pensee-produit-bloc-l.json
reports/rapport-robustesse-produit.md
reports/rapport-composition-sans-perte.md
reports/pensee-composition-sans-perte.json
reports/rapport-partition-syntagmes.md
reports/rapport-partition-integree.md
reports/INDEX.md
docs/schemas/bloc-linguistique-substitution.svg
docs/pilotage/roadmap.md
docs/theorie/lecture-rapide.md
docs/theorie/contrat-bloc-langue.md
docs/implantation/moteur-de-pensee.md
docs/implantation/bloc-linguistique.md
docs/produit/exemples.md
docs/produit/README.md
journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md
journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md
journal/sessions/aa5f9fc5-9450-4118-b65f-e8b99a
… [570 caractères tronqués]
  ```

- **bash** `{"command": "ls tools/tests/linguistique/gold*.json && python3 - <<'PY'\nimport json,pathlib\nfor f in [\"gold.json\",\"gold_reel.json\",\"gold_synthetique.json\",\"gold_gele.json\"]:\n p=pathlib.Path(\"tools/tests/linguistique\")/f\n d=json.loads(p.read_text())\n print(f, len(d.get(\"phrases\",[])) … [77 caractères tronqués]`

  ```
tools/tests/linguistique/gold_gele.json
tools/tests/linguistique/gold.json
tools/tests/linguistique/gold_reel.json
tools/tests/linguistique/gold_restitution_v2.json
tools/tests/linguistique/gold_synthetique.json
gold.json 20 ['version', 'phrases', 'note']
gold_reel.json 432 ['version', 'source', 'note', 'phrases']
gold_synthetique.json 160 ['version', 'source', 'graine', 'note', 'phrases']
gold_gele.json 602 ['gele', 'phrases']
  ```

- **bash** `{"command": "sed -n '1,220p' reports/rapport-pensee-quatre-modes.md", "description": "Read four modes report"}`

  ```
# L — la porte des quatre modes sur le gold 432 : le neuronal API domine (0,9309 / 0,8226 / 0,8784), la fusion dégrade (0,928 / 0,802 / 0,857)

> **Ligne de roadmap** : **L** (le bloc langue) · **Date** : 2026-11-03 · **Verdict** : ⚠️ **le neuronal
> seul est le meilleur sur les niveaux linguistiques** — POS **0,9309**, syntagmes **0,8226**, tête
> **0,8784** —, l'**heuristique** garde la **pragmatique** (acte **0,9954** contre **0,0**), et la
> **fusion** (parallèle et cascade) **régresse** : **0,928 / 0,802 / 0,857**. Un **refus** ; 858
> appels API, **254 341 tokens**, 13,3 min. La porte des quatre modes **révèle le problème de la
> fusion**, pas celui des blocs.

## 1. Le dispositif

- **Gold réel 432** (2 375 tokens), le même pour les quatre modes.
- **Neuronal** : `NeuronalLLMCompose` (POS + syntagmes) via l'**API DeepSeek** (`deepseek-chat`,
  `DEEPSEEK_KEY_FILE`), **aucun serveur local**, **aucun GPU** (règle 11).
- **Parallèle** : `Parallele([heuristique, neuronal], priorite_syntagme="confiance")`.
- **Cascade** : `Cascade(heuristique, neuronal, seuil=0,6, priorite_syntagme="confiance")`.
- **Mesures** : POS, syntagmes F1, tête F1, acte, fraction, refus ; **coût** : appels
… [3330 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,200p' reports/rapport-pensee-quatre-modes-432.md", "description": "Read four modes 432 report"}`

  ```
# B13 — les quatre modes sur le gold 432 : le niveau gagne avec le réel

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6 et règle 11) · **Date** : 2026-11-04 ·
> **Verdict** : ✅ **143/143 portes** : les **six modes** du contrat de L sont mesurés sur le
> **gold réel 432**, avec le **neuronal réel** (l'API DeepSeek, `deepseek-chat`, température 0).
> Le **niveau** (`PRIORITE_NIVEAU`) gagne : POS **0,9309**, syntagmes **0,8226**, tête **0,8784**,
> et garde la pragmatique de l'heuristique (**0,9954**). Le **mock** avait conclu l'inverse :
> le défaut par défaut reste la confiance **faute de clé dans les portes**, pas par choix.
>
> **Dispositif** : [`qualifier_quatre_modes.py`](../tools/tests/linguistique/qualifier_quatre_modes.py),
> [`pensee-quatre-modes-432.json`](pensee-quatre-modes-432.json),
> [`autotest.py`](../tools/pensee/autotest.py).

## 1. Les six modes (432 phrases, API réelle)

| mode | POS | syntagmes F1 | tête F1 | acte |
|---|---:|---:|---:|---:|
| heuristique | 0,7394 | 0,2520 | 0,4511 | **0,9954** |
| neuronal (compose) | **0,9309** | **0,8226** | **0,8784** | 0,0000 |
| parallèle (confiance) | 0,9280 | 0,8020 | 0,8570 | 0,9954 |
| cascade (confiance) |
… [2477 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys,time,json\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nsys.path.insert(0,'tools/tests/linguistique')\nimport evaluer_gold as ev\nph=ev.charger()\nprint(\"phrases\",len(ph),\"reel\",len([p for p in ph if p.get('source') in ('hand','reel')]))\n … [705 caractères tronqués]`

  ```
phrases 612 reel 452
heuristique all POS 0.8625 F1 0.7902 tete 0.9029 acte 0.9967 att 0.9958 couv 0.9958
heuristique reel POS 0.8891 F1 0.7906 tete 0.899 acte 0.9956 att 0.9946 couv 0.9946
neuronal all POS 0.754 F1 0.7651 tete 0.8807 acte 0.9967 att 0.0 couv 0.9331
neuronal reel POS 0.7621 F1 0.7448 tete 0.8697 acte 0.9956 att 0.0 couv 0.913
parallele all POS 0.8625 F1 0.7902 tete 0.9029 acte 0.9967 att 0.9958 couv 0.9958
parallele reel POS 0.8891 F1 0.7906 tete 0.899 acte 0.9956 att 0.9946 couv 0.9946
cascade all POS 0.8625 F1 0.7902 tete 0.9029 acte 0.9967 att 0.9958 couv 0.9958
cascade reel POS 0.8891 F1 0.7906 tete 0.899 acte 0.9956 att 0.9946 couv 0.9946
durée 4.11
  ```

- **bash** `{"command": "ls tools/tests | head -80 && grep -rln \"evaluer\" tools/tests | head -40", "description": "List tests and evaluer tests"}`

  ```
cic
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
test_banc_performance.py
test_empaquetage.py
test_panini_334.py
test_pensee_politique.py
test_pensee_store.py
test_produit_libre.py
test_produit.py
test_profils.py
test_restitution.py
test_restitution_v2.py
test_restitution_v3.py
test_schema_produit.py
test_tagger_api.py
test_verificateur_cic.py
test_verificateur_cic_v2.py
test_verifier_performance_fix.py
tools/tests/linguistique/__pycache__/juge.cpython-313.pyc
tools/tests/linguistique/__pycache__/qualifier_syntagmes.cpython-313.pyc
tools/tests/linguistique/__pycache__/qualifier_pragmatique.cpython-313.pyc
tools/tests/linguistique/__pycache__/qualifier_cascade.cpython-313.pyc
tools/tests/linguistique/__pycache__/miroir.cpython-313.pyc
tools/tests/linguistique/__pycache__/qualifier_quatre_modes.cpython-313.pyc
tools/tests/linguistique/__pycache__/evaluer_gold.cpython-313.pyc
tools/tests/linguistique/__pycache__/classer_gv.cpython-313.pyc
tools
… [1099 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"construire_parseur\\|cmd_evaluer\\|_module_evaluation\" tools/tests | head -40", "description": "Find CLI tests"}`

  ```
tools/tests/test_tagger_api.py:314:        evaluateur = drave._module_evaluation()
tools/tests/test_tagger_api.py:317:        ancien_module = drave._module_evaluation
tools/tests/test_tagger_api.py:318:        drave._module_evaluation = lambda: evaluateur
tools/tests/test_tagger_api.py:322:            drave._module_evaluation = ancien_module
tools/tests/test_tagger_api.py:511:        evaluateur = drave._module_evaluation()
tools/tests/test_tagger_api.py:519:        ancien_module = drave._module_evaluation
tools/tests/test_tagger_api.py:521:        drave._module_evaluation = lambda: evaluateur
tools/tests/test_tagger_api.py:528:            drave._module_evaluation = ancien_module
[stderr]
grep: tools/tests/__pycache__/test_tagger_api.cpython-313.pyc: binary file matches
grep: tools/tests/__pycache__/test_tagger_api.cpython-313-pytest-9.1.1.pyc: binary file matches
  ```

- **bash** `{"command": "sed -n '1,180p' tools/tests/test_produit.py", "description": "Read product test style"}`

  ```
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
        encoding="utf-8",
        timeout=120,
    )


def detail(resultat: subprocess.CompletedProcess[str]) -> str:
    return (f"code={resultat.returncode}\n"
            f"stdout={resultat.stdout}\n"
            f"stderr={resultat.stderr}")


class TestProduit(unittest.TestCase):
    """Le contrat produit : version/aide, analyse, JSON, rejeu, usage."""


… [6909 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '280,360p' tools/tests/test_tagger_api.py && sed -n '490,550p' tools/tests/test_tagger_api.py", "description": "Read tagger evaluer tests"}`

  ```
"""La CLI de bout en bout, client injecté : le chemin `--tagger` et son coût."""

    def setUp(self) -> None:
        self.client = _FauxClient()
        self._ancien_client = drave._client_tagger
        drave._client_tagger = lambda: self.client

    def tearDown(self) -> None:
        drave._client_tagger = self._ancien_client

    def _lancer(self, *arguments: str) -> tuple[int, str, str]:
        sortie, erreur = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(sortie), contextlib.redirect_stderr(erreur):
            code = drave.main(list(arguments))
        return code, sortie.getvalue(), erreur.getvalue()

    def test_analyser_tagger_json(self) -> None:
        code, sortie, erreur = self._lancer("analyser", TEXTE, "--tagger", "--json")
        self.assertEqual(code, 0, erreur)
        donnees = json.loads(sortie)
        self.assertEqual(_pos_map(donnees), {(0, 2): "VERB", (3, 7): "DET", (8, 12): "ADV", (12, 13): "PONCT"})
        self.assertEqual(donnees["source"], "cascade")
        self.assertIn("TAGGER API", erreur)
        self.assertEqual(self.client.demandes, 1)

    def test_analyser_tagger_lisible(self) -> None:
        code, sortie, erreur =
… [5831 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"3\\.3\\|### 3.3\\|## 3\" docs/implantation/bloc-linguistique.md docs/theorie/contrat-bloc-langue.md docs/produit/README.md | head -40", "description": "Find doc section 3.3"}`

  ```
docs/implantation/bloc-linguistique.md:56:## 3. La sortie : une annotation, pas un corps
docs/theorie/contrat-bloc-langue.md:76:## 3. Les quatre modes
docs/theorie/contrat-bloc-langue.md:85:### 3.1 Le parallèle
docs/theorie/contrat-bloc-langue.md:91:### 3.2 La cascade
docs/produit/README.md:20:> **06/11**, et l'`evaluer` du § 3.3 a été relancé le **14/11** (gold vivant 612, `--par-langue
docs/produit/README.md:98:## 3. Comment l'utiliser — cinq exemples réels
docs/produit/README.md:104:### 3.1 Analyser une phrase
docs/produit/README.md:127:### 3.2 Analyser en JSON et lire l'attachement
docs/produit/README.md:164:### 3.3 Mesurer sur le gold
docs/produit/README.md:220:### 3.3 quater Traiter un corpus
docs/produit/README.md:230:### 3.3 bis La vue des syntagmes qui se chevauchent — les champs du schéma v2
docs/produit/README.md:345:### 3.3 ter Le contexte (mémoire de discours)
docs/produit/README.md:354:### 3.4 Rejouer et vérifier le déterminisme
docs/produit/README.md:371:### 3.5 Le refus, et la langue inconnue
docs/produit/README.md:389:### 3.6 Restituer la surface (v0)
docs/produit/README.md:424:### 3.6 bis La base honnête — `--reel`
docs/produit/README.md:434:### 3.7 Le tagger en o
… [93 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/drave.py evaluer --aide | sed -n '1,120p'", "description": "Show evaluer help"}`

  ```
usage: drave evaluer [-h] [--gold] [--reel] [--par-langue] [--tagger] [--json]

Mesure POS, syntagmes (F1/tête) et attachement (exact/couverture) sur le gold, avec un contrôle négatif reproductible. Avec --par-langue, donne le même détail pour le français et l'anglais. Avec --tagger, mesure en plus la cascade POS de l'API DeepSeek et son écart.

options:
  -h, --help, --aide  afficher cette aide et quitter
  --gold              mesurer le gold gelé gold_gele.json (livré avec la roue) au lieu du gold
                      vivant ; si les gold manquent, evaluer sort en 4 et dit quoi faire
  --reel              mesurer la base honnête : les phrases réelles (hand + reel), sans synthétique
  --par-langue        scinder la mesure en français et en anglais
  --tagger            mesurer en plus la cascade POS de l'API DeepSeek (clé et réseau)
  --json              sortie JSON des mesures complètes

Exemples : python3 tools/drave.py evaluer --gold --json ; python3 tools/drave.py evaluer --par-langue ; python3 tools/drave.py evaluer --tagger
  ```

- **bash** `{"command": "sed -n '150,240p' docs/produit/README.md", "description": "Read product README section 3.3"}`

  ```
| jq -r '.etiquettes[] | select(.niveau=="syntagme")
           | "\(.type) \(.valeur) role=\(.meta.role) → \(.meta.attachement.cible) · " +
             ([.meta.attachement.candidats[] | "\(.cible)[\(.span.debut):\(.span.fin)]"] | join(", "))'
```
```
GN Le chat role=agent → dort · dort[8:12]
GV dort role=predicat → chat · chat[3:7]
```

Un consommateur n'a plus à parser « « qui dort » → voisine » : il lit `cible` et `span`.
La **cible choisie** est toujours le premier objet ; un candidat dont la cible n'est pas
retrouvée dans le texte est écarté. Le détail et la mesure sont dans
[`rapport-contrat-json.md`](../../reports/rapport-contrat-json.md).

### 3.3 Mesurer sur le gold

```bash
python3 tools/drave.py evaluer
```
```
drave 0.1.0 — évaluation de l'heuristique sur le gold
gold vivant (hand + reel + synthétique) · 612 phrases · 3179 tokens · 239 cibles d'attachement

POS         exactitude 86.25 %  (fermé 93.73 %, ouvert 79.18 %)
SYNTAGMES   F1 79.02 %  (P 78.60 % / R 79.44 %)
  tête      F1 90.29 %  (P 92.61 % / R 88.08 %)
  vue linéaire (partition filtrer) F1 81.44 %  · attachement 93.72 % de couverture
ATTACHEMENT exact 99.58 % · couverture 99.58 % · exact sur span 100.00 % ·
… [3530 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,60p' docs/produit/README.md && sed -n '424,470p' docs/produit/README.md", "description": "Read README context and reel"}`

  ```
# Le premier produit — analyser un texte avec Drave

> **Ce que ce document est.** La notice d'usage du **premier produit** de Drave : le bloc
> linguistique, utilisable **aujourd'hui**, sur un CPU, sans modèle et sans réseau. Il dit à qui
> il s'adresse, ce qu'il fait, comment l'exécuter, ce qu'il ne fait pas, ce qu'il coûte et ce
> qu'il garantit.
>
> **Vérifié le 2026-11-15** sur la branche `s/v7`. Le point d'entrée `tools/drave.py` est
> **livré** (version **0.1.0**) : `analyser`, `evaluer`, `rejouer`, `restituer` et `--version`
> existent, et la
> porte produit est verte. Le **tagger POS par API** est livré **en option** (`--tagger`,
> § 3.7) : clé et réseau pour qui le demande, **heuristique hors ligne par défaut**. Le
> **prototype `--tagger auto`** (complété le **2026-11-15**, § 3.7) choisit l'API si une clé
> existe, l'heuristique sinon, **sans changer le code de sortie** ; il ne change pas le défaut.
> Le format
> est **version 2** (`schema: "drave.annotation"`,
> `version: 2`) : le schéma v2 ajoute `meta.partition` et `meta.alternative`, et la **version 1
> reste lue** ([`tools/schemas/`](../../tools/schemas/)). Les sorties du § 3.1, du § 3.4 et du
> § 3.5 ont été relanc
… [4785 caractères tronqués]
  ```

- **bash** `{"command": "git diff --stat && git diff -- docs/produit/README.md | head -60 && git diff -- tools/drave.py | head -80", "description": "Inspect existing uncommitted diffs"}`

  ```
docs/implantation/bloc-linguistique.md  |  13 +
 docs/pilotage/en-cours.md               |  14 +-
 docs/pilotage/roadmap.md                |   7 +-
 docs/produit/README.md                  |  92 +++-
 docs/produit/demarrage.md               |  38 +-
 pyproject.toml                          |   9 +-
 reports/INDEX.md                        |   1 +
 reports/README.md                       |   1 +
 reports/pensee-coherence-fiches-v7.json |  19 +
 reports/pensee-dev-test-v10.json        |   2 +-
 reports/pensee-quatre-modes.json        | 734 ++++++++++++++++++--------------
 reports/rapport-audit-v7.md             |   6 +-
 reports/rapport-bloc-linguistique.md    |   7 +
 reports/rapport-coherence-fiches-v7.md  |  17 +-
 reports/rapport-dev-test-v10.md         |   2 +-
 reports/rapport-pensee-v12.md           |   4 +-
 reports/rapport-roue.md                 |   6 +-
 reports/rapport-spans-chunker.md        |  13 +-
 tools/chantier/plan.json                | 188 ++++++++
 tools/drave.py                          | 130 +++++-
 tools/porte-bloc-linguistique.sh        |   2 +
 tools/porte-produit.sh                  |  15 +
 tools/tests/test_empaquetage.py         |  10 +-
 tools/tests/tes
… [8515 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,180p' docs/methode/resultats.md", "description": "Read results method"}`

  ```
# Ce qu'un résultat doit porter

> Document de tâche, chargé depuis [`AGENTS.md`](../../AGENTS.md). À lire **avant d'écrire une fiche**, un JSON de
> résultats, ou un message de commit.

## Les cinq pièces d'un résultat

1. **Le chiffre** — la valeur, avec son [unité](../theorie/glossaire/entrees/unite.md) et son arrondi utile (jamais plus de chiffres que l'instrument n'en
   [porte](../theorie/glossaire/entrees/porte.md)) ;
2. **La mesure qui le produit** — le calcul exact, la métrique ([chrF](../theorie/glossaire/entrees/chrf.md), précision, rappel, [AUC](../theorie/glossaire/entrees/auc.md)…), et ce qu'elle ne
   mesure pas ;
3. **Le dispositif** — quel [corpus](../theorie/glossaire/entrees/corpus.md) (et sa provenance), quel modèle (taille, [quantification](../theorie/glossaire/entrees/quantification.md), date de coupure),
   quelles **couches de neurones** sondées, quel découpage, **quelle unité de mesure** (unité de sens ou unité
   grammaticale ; si c'est un [jeton](../theorie/glossaire/entrees/jeton.md), le dire comme **technique**), quels réglages (prompt, gabarit, longueur de
   sortie, graine) ;
4. **Le [contrôle négatif](../theorie/glossaire/entrees/controle-negatif.md)
… [2500 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"0\\.70\\|0,70\\|plancher\\|seuil\\|verdict\\|cascade\" tools/tests/linguistique/qualifier_quatre_modes.py | head -80", "description": "Inspect four modes qualification thresholds"}`

  ```
10:  4. cascade (`Cascade`, seuil 0,6).
12:Mêmes mesures que la cascade : POS, syntagmes F1, tête F1, acte, fraction, refus.
36:from tools.tests.linguistique.qualifier_cascade import _sources, charger
44:    ap.add_argument("--seuil", type=float, default=0.6)
72:        "cascade": Cascade(h, compose, seuil=a.seuil, priorite_syntagme="confiance"),
76:        "cascade_niveau": Cascade(h, compose, seuil=a.seuil, priorite_syntagme="confiance",
90:    seuils = {
96:        "cascade": mesures["cascade"]["all"]["pos"]["exactitude"]
101:        "cascade_niveau": mesures["cascade_niveau"]["all"]["pos"]["exactitude"]
111:        "seuils": seuils,
  ```

- **bash** `{"command": "grep -rn \"0\\.70\\|0,70\\|plancher\" tools/tests/linguistique/evaluer_gold.py tools/tests/linguistique/qualifier_*.py reports/rapport-pensee-*.md | head -80", "description": "Search floor 0.70 references"}`

  ```
tools/tests/linguistique/evaluer_gold.py:273:        "pos_reel": h_reel["pos"]["exactitude"] >= 0.70,
tools/tests/linguistique/evaluer_gold.py:279:        "acte": h_all["pragmatique"]["acte"] >= 0.70,
tools/tests/linguistique/qualifier_cascade.py:118:        # Seuils : le gold 180 (hand+synth) et le gold réel n'ont pas le même plancher.
tools/tests/linguistique/qualifier_syntagmes.py:164:            "neuronal_tete_all": mesures["neuronal"]["all"]["tete"]["f1"] >= 0.70,
tools/tests/linguistique/qualifier_tagger_h50.py:358:    """Deux planchers POS : classe majoritaire et classe tirée au hasard (graine 0)."""
reports/rapport-pensee-anaphore-chaines.md:5:> entrent dans le gold (342 phrases). La règle « dernier nom » tombe à **7/10** (0,70) : elle
reports/rapport-pensee-anaphore-chaines.md:17:| **r337–r342 (long)** | **10** | **7** | **0,70** | r337 `il→sophie`, r339 `elle→livre`, r341 `she→book` |
reports/rapport-pensee-bruit.md:20:| 0,70 | **oui** | 10 | 3 |
reports/rapport-pensee-courbe20.md:20:| 0,37 | 70/100 | 0,70 |
reports/rapport-pensee-gold-complexes100.md:7:> autour de 0,70 ; le gain de syntagme se **réduit** à +0,08.
reports/rapport-pensee-gold-complexes100.md:22:- **Le POS 
… [1094 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,180p' tools/tests/linguistique/qualifier_quatre_modes.py", "description": "Read qualifier_quatre_modes"}`

  ```
#!/usr/bin/env python3
"""qualifier_quatre_modes.py — la porte des quatre modes du contrat de L sur le gold 432.

Les quatre modes du contrat (`docs/theorie/contrat-bloc-langue.md`) mesurés sur le
**même** gold réel 432 :

  1. heuristique seule ;
  2. neuronal seul (le composite POS + syntagmes, via l'API DeepSeek — règle 11) ;
  3. parallèle (`Parallele`) ;
  4. cascade (`Cascade`, seuil 0,6).

Mêmes mesures que la cascade : POS, syntagmes F1, tête F1, acte, fraction, refus.
Le coût est mesuré : appels du tagger, tokens API, latence, durée.

Usage :
    DEEPSEEK_KEY_FILE=~/.config/drave/deepseek.key \
    python3 tools/tests/linguistique/qualifier_quatre_modes.py --limite 3
"""
from __future__ import annotations

import argparse
import json
import pathlib
import statistics
import sys
import time

RACINE = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RACINE))

from tools.bloc_linguistique import (PRIORITE_NIVEAU, PRIORITE_TYPE, Cascade, Heuristique,
                                     NeuronalLLMChunks, NeuronalLLMCompose,
                                     NeuronalLLMPOS, NeuronalLLMPragmatique, Parallele)
from tools.llm.deepseek import DeepSeek
from tool
… [5308 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '90,170p' tools/tests/linguistique/qualifier_cascade.py && sed -n '1,100p' reports/rapport-pensee-seuils-gold-reel.md", "description": "Read cascade thresholds and floors report"}`

  ```
if not _sante(endpoint):
        if not args.demarrer:
            raise SystemExit(f"serveur absent sur {endpoint} — relancer avec --demarrer")
        proc = demarrer_serveur(modele, args.port, pathlib.Path("/tmp/qualifier-cascade-serveur.log"))

    pos = bl.NeuronalLLMPOS(modele, endpoint=endpoint, confiance=args.confiance)
    chunks = bl.NeuronalLLMChunks(modele, endpoint=endpoint, confiance=args.confiance)
    compose = bl.NeuronalLLMCompose(pos, chunks)
    h = bl.Heuristique()
    t0 = time.perf_counter()
    try:
        # Le composite d'abord : il remplit les deux caches ; les ablations relisent.
        mesures = {"neuronal": _sources(compose, phrases)}
        mesures["heuristique"] = _sources(h, phrases)
        mesures["cascade_pos"] = _sources(bl.Cascade(h, pos), phrases)
        mesures["cascade_syntagmes"] = _sources(
            bl.Cascade(h, chunks, priorite_syntagme="confiance"), phrases)
        mesures["cascade_complete"] = _sources(
            bl.Cascade(h, compose, priorite_syntagme="confiance"), phrases)
        mesures["cascade_complete_defaut"] = _sources(bl.Cascade(h, compose), phrases)
        refus = [p["id"] for p in phrases
                 if comp
… [6138 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"class Etiquette\\|@dataclass\" tools/bloc_linguistique.py | head -20 && sed -n '250,330p' tools/bloc_linguistique.py", "description": "Inspect Etiquette dataclass"}`

  ```
66:@dataclass(frozen=True)
75:@dataclass
76:class Etiquette:
126:@dataclass
            return "und", 0.0, scores
        confiance = min(1.0, (meilleur - second) / meilleur + 0.2 * meilleur)
        return langue, round(confiance, 4), scores
    # profil de secours : mots-outils de quelques langues
    mots = set(re.findall(r"[a-zà-ÿ']+", _normaliser(texte)))
    scores = {l: len(mots & set(LEXIQUES[l])) / max(1, len(mots)) for l in LEXIQUES}
    if indice and indice in scores:
        scores[indice] += 0.02
    if not scores or max(scores.values()) <= 0:
        return "und", 0.0, scores
    langue = max(scores, key=scores.get)
    return langue, round(min(1.0, scores[langue] * 2), 4), scores


# --------------------------------------------------------------------------- script


def _script_char(ch: str) -> str:
    if not ch.isalpha():
        return ""
    try:
        nom = unicodedata.name(ch)
    except ValueError:
        return ""
    prefixes = (
        ("LATIN", "Latn"), ("CYRILLIC", "Cyrl"), ("GREEK", "Grek"), ("ARABIC", "Arab"),
        ("HEBREW", "Hebr"), ("DEVANAGARI", "Deva"), ("THAI", "Thai"), ("HIRAGANA", "Jpan"),
        ("KATAKANA", "Jpan"), ("HANGUL", "Hang")
… [3269 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"class Annotation\" tools/bloc_linguistique.py | head -5 && sed -n '330,430p' tools/bloc_linguistique.py", "description": "Inspect Annotation class"}`

  ```
127:class Annotation:
    "nl": set("de het een en of maar want dat die dit deze ik jij hij zij wij jullie zij mij "
              "jou hem haar ons hen mijn jouw zijn haar ons jullie hun is zijn was waren hebben "
              "heeft had niet geen zeer in op aan met van voor door".split()),
}

POS_FERME = {
    "fr": {
        "DET": set("le la les l un une ce cet cette ces mon ma mes ton ta tes son sa ses notre nos votre vos leur leurs quel quelle quels quelles".split()),
        "PREP": set("à a au aux de du des d en dans par pour sur sous avec sans chez vers entre depuis pendant durant contre malgré selon près loin devant derrière après avant au-dessus au-dessous vis-à-vis en-dehors".split()),
        "PRON": set("je j tu il elle on nous vous ils elles me te se lui leur moi toi soi y en ce cela ça qui que quoi dont où".split()),
        "CONJ": set("et ou mais donc or ni car quand comme si parce puisque lorsque pendant qu".split()),
        "AUX": set("est sont était étaient été être ai as a avons avez ont avait avaient eu avoir suis es sommes êtes".split()),
        "ADV": set("ne n pas plus jamais rien très bien mal ici hier demain aujourd'hui peut-être fort souvent toujours
… [6458 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '55,150p' tools/bloc_linguistique.py", "description": "Read Etiquette and Annotation definitions"}`

  ```
except ImportError:  # script : `python3 tools/bloc_linguistique.py`
    import roles_gp as _roles_gp
    from roles_vocabulaire import normaliser_role as _normaliser_role
NIVEAUX = ("graphème", "morphème", "mot", "pos", "syntagme", "phrase", "discours",
           "pragmatique", "document")
SOURCES = ("heuristique", "neuronal", "humain")
SCRIPT_NEUTRE = "Zyyy"

# --------------------------------------------------------------------------- types


@dataclass(frozen=True)
class Span:
    debut: int
    fin: int

    def json(self) -> dict:
        return {"debut": self.debut, "fin": self.fin}


@dataclass
class Etiquette:
    niveau: str
    type: str
    valeur: str
    debut: int
    fin: int
    source: str = "heuristique"
    confiance: float = 0.5
    candidats: list[str] = field(default_factory=list)
    langue: str = "und"
    script: str = SCRIPT_NEUTRE
    meta: dict = field(default_factory=dict)

    def json(self) -> dict:
        return {
            "niveau": self.niveau, "type": self.type, "valeur": self.valeur,
            "debut": self.debut, "fin": self.fin, "source": self.source,
            "confiance": round(float(self.confiance), 4),
            "candidats": list
… [2213 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl, evaluer_gold as ev\nph=ev.charger(); reel=[p for p in ph if p.get('source') in ('hand','reel')]\nh=bl.Heuristique(); n=bl.MockNeuronal(); c=bl.Cascade … [248 caractères tronqués]`

  ```
all 0.8625 612 612
reel 0.8891 452 452
  ```

- **bash** `{"command": "cat pyproject.toml", "description": "Read pyproject"}`

  ```
[build-system]
requires = ["setuptools>=61"]
build-backend = "setuptools.build_meta"

[project]
name = "drave"
version = "0.1.0"
description = "Le point d'entrée produit du bloc linguistique de Drave."
requires-python = ">=3.10"
dependencies = []

[project.scripts]
drave = "tools.drave:main"

[tool.setuptools]
# Le paquet est un **namespace** (`tools/` n'a pas d'`__init__.py`) : on déclare les
# sous-ensembles dont le CLI a besoin. `tools.tests` reste un namespace implicite
# (son répertoire existe par `tools.tests.linguistique`) : on n'embarque pas les
# scripts de test, seulement les modules et les gold de la mesure.
packages = ["tools", "tools.llm", "tools.structures", "tools.tests.linguistique"]

[tool.setuptools.package-data]
# Les gold et l'artefact de profils sont **dans la roue** : `drave evaluer` et
# `drave profils` doivent marcher hors du dépôt. Le contrôle négatif (une roue
# amputée de ces fichiers) est décrit dans reports/rapport-roue.md et
# reports/rapport-profils.md : la mesure et la détection échouent alors en code 4,
# sans trace et sans stdout.
"tools.tests.linguistique" = [
    "gold.json",
    "gold_gele.json",
    "gold_reel.json",
    "gold_restitution_v2.js
… [60 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' tools/porte-produit.sh && sed -n '1,100p' tools/porte-bloc-linguistique.sh", "description": "Read product gates"}`

  ```
#!/usr/bin/env bash
# porte-produit — le premier produit : la CLI répond, le JSON est valide, le rejeu est identique.
#
# Ce qu'elle vérifie : `drave --version`, `analyser` (fr et en) rend un JSON parsable avec des
# étiquettes, `rejouer` rend le même sha256 deux fois, et le smoke test passe.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1
ko=0
dit() { printf '  %s %s\n' "$1" "$2"; }

ver=$(python3 tools/drave.py --version 2>&1)
case "$ver" in drave*) dit ✅ "version : $ver" ;; *) dit ❌ "version : $ver"; ko=1 ;; esac

for langue in fr en; do
  case "$langue" in
    fr) texte="Le chat dort sur le toit." ;;
    en) texte="The cat sleeps on the roof." ;;
  esac
  sortie=$(python3 tools/drave.py analyser "$texte" --langue "$langue" --json 2>&1)
  if printf '%s' "$sortie" | python3 -c "
import json, sys
d = json.load(sys.stdin)
assert d['langue'] == '$langue', d.get('langue')
assert len(d['etiquettes']) > 5, len(d['etiquettes'])
assert any(e['niveau'] == 'syntagme' for e in d['etiquettes'])
assert any(e['niveau'] == 'pos' for e in d['etiquettes'])
" 2>/dev/null; then
    dit ✅ "analyser $langue : JSON valide, étiquettes et syntagmes"
  else
    dit ❌ "analyser $langue : JSON invalide 
… [4863 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"def _dumps\\|_dumps =\" tools/drave.py | head -10 && sed -n '90,130p' tools/drave.py", "description": "Inspect _dumps"}`

  ```
91:def _dumps(objet) -> str:

def _dumps(objet) -> str:
    """JSON stable (pas d'horodatage, pas de durée) et lisible."""
    return _sur(json.dumps(objet, ensure_ascii=False, indent=1)) + "\n"


def _canonique(a: bl.Annotation) -> str:
    """La forme comparée par `rejouer` : clés triées, durée exclue, sans espaces inutiles."""
    return _sur(json.dumps(a.json(), ensure_ascii=False, sort_keys=True, separators=(",", ":")))


# --------------------------------------------------------------------------- le tagger (option)


class CleTaggerAbsente(RuntimeError):
    """Aucune clé : le tagger est une option, jamais un prérequis du produit."""


class CleTaggerRefusee(RuntimeError):
    """L'API refuse la clé (HTTP 401/403) : ce n'est pas un refus de phrase, c'est un arrêt.

    Une clé absente et une clé refusée sont la même dépendance manquante du point de vue du
    produit : le code 4, un message qui nomme les trois sources de la clé, et rien sur `stdout`.
    """

    def __init__(self, code: int) -> None:
        self.code = int(code)
        super().__init__(
            f"clé DeepSeek refusée (HTTP {self.code}) : vérifiez DEEPSEEK_KEY_FILE, "
            f"~/.config/drave/deep
… [577 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,80p' reports/INDEX.md && tail -40 reports/INDEX.md", "description": "Read reports index"}`

  ```
# Index des fiches de reports/

> **Généré** par `tools/index_reports.py` — **764 fiches**. Les fichiers
> d'infrastructure (`README.md`, `INDEX.md`, `historique-*`) sont exclus du tableau ;
> la page d'état, elle, compte tous les `.md` de `reports/`.

| fiche | titre |
|---|---|
| [07-mesures-couche-commune.md](07-mesures-couche-commune.md) | 7. Les modèles alternatifs pour l'entrée et la sortie — vers une couche commune |
| [aiguille-30b.md](aiguille-30b.md) | aiguille v2 — /home/stephane/Data13TB/stephane/modeles/gguf/Qwen3-30B-A3B-Instruct-2507-Q4_K_M.gguf |
| [aiguille-gpt-oss.md](aiguille-gpt-oss.md) | aiguille v2 — /home/stephane/Data13TB/stephane/modeles/gguf/gpt-oss-120b-MXFP4.gguf |
| [alignement-verne.md](alignement-verne.md) | Alignement phrase à phrase — *Le Tour du monde en quatre-vingts jours* (français → anglais) |
| [bilan-b11.md](bilan-b11.md) | Bilan B11 — ce qui tient, ce qui ne tient pas |
| [bilan-multi-materiel.md](bilan-multi-materiel.md) | Bilan multi-matériel — CPU, FPGA, GPU |
| [campagne-benefices.md](campagne-benefices.md) | Campagne 24 h — où Drave est à son meilleur, tâche par tâche |
| [fiche-nuit-17-10.md](fiche-nuit-17-10.md) | La nuit du 17 au 18 
… [13990 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,100p' reports/README.md && tail -60 reports/README.md", "description": "Read reports README"}`

  ```
# Les rapports — données intermédiaires et références

> **Ce dossier porte les résultats et les données de nos travaux**, jamais la documentation de référence
> (elle est dans [`docs/`](../docs/)). Les fiches courantes sont citées depuis le tableau de bord
> [`docs/pilotage/en-cours.md`](../docs/pilotage/en-cours.md).

> **Navigation** : [la carte des sujets](../docs/theorie/carte.md) · [l'état du moment](../docs/pilotage/en-cours.md) ·
> [l'inventaire des docs](../docs/README.md) · [le journal](../journal/README.md).
>
> **Contexte** : la fiche [`07-mesures-couche-commune.md`](07-mesures-couche-commune.md) est un **hub** de
> **168 mesures** en **10 parties** (`07/p1.md` … `07/p10.md`), pas un fichier de 150 Ko. La lire **par
> partie**, jamais en entier ; l'index exhaustif des fiches est [`INDEX.md`](INDEX.md).

## Les fiches courantes

| fichier | ce qu'il porte |
|---|---|
| [`rapport-bilan-jour-1115.md`](rapport-bilan-jour-1115.md) | **Bilan** — le 15/11 : la semaine 2 en un jour, la décision du tagger |
| [`rapport-bilan-semaine.md`](rapport-bilan-semaine.md) | **Bilan** — la semaine 07 → 15/11 : le produit, Panini, la coordination, le harnais |
| [`rapport-bilan-nuit.md`](r
… [15111 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,160p' docs/pilotage/en-cours.md", "description": "Read en-cours state"}`

  ```
# En ce moment

**Mis à jour : 2026-11-16, 02 h 15 HNE (U3 : les profils de langue)**

> **État courant, pas histoire** : une sous-section par session active ; preuves et plan plus bas (**La carte**).

### Session `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — le hub de reprise du 04/11 *(en pause)*

- **Id** : `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — [`plan.md`](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/plan.md).
- **Rôle** : **Hub de reprise** — état, docs, intégration, passe.
- **Fait** : index réparé ; **N3 intégré** ; N2/S/L actifs.
- **Prochaine action** : **suivi docs**, puis la **passe**.
- **État** : **en pause** depuis le 05/11 ; la clôture J14.1 est portée par `e181ce02`.
- **Bloquants** : aucun.
- **Journal** : [la session](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/).

## Sessions en cours

> Contrat : [`continuite.md`](../methode/continuite.md) · sessions terminées :
> [`journal/sessions/`](../../journal/sessions/). Chaque session expose son mandat dans son
> `plan.md` (`python3 tools/sessions.py --status`). **Une session écrit l'état à la fois** :
> le hook pre-commit refuse un fait sans ligne d'état ; une session arrêtée passe `État : en
… [11091 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '160,230p' docs/pilotage/roadmap.md", "description": "Read roadmap near T6"}`

  ```
gold B13 ; **E2** ([fiche](../../reports/rapport-tagger-erreurs.md)).

**T4 — la performance (15/11).** 10 000 mots : **4,01 s**, **2 493 mots/s**, **126 Mio**,
**14,8 Mo** JSON ; α = **1,55**, `_groupes_partition`/`_cible_proche` **O(k²)**.
[Fiche](../../reports/rapport-performance.md) · [JSON](../../reports/performance.json).

**U1 — les O(k²) bornés (16/11).** 10 000 mots : **3,99 → 0,82 s** (×4,9),
**12 259 mots/s**, **127,4 Mio** ; JSON identique. **α = 1,076** (1,530 avant), +0,00077 de R² ; sorties identiques (612/452). [Fiche](../../reports/rapport-performance-fix.md) ·
[JSON](../../reports/performance-fix.json) · [contrôle](../../tools/verifier_performance_fix.py).
**U2 — la roue (16/11)** : **1 727 201 o** ; sans gold, `evaluer` **4**
([fiche](../../reports/rapport-roue.md)).

**U3** : **398 profils UDHR** ; **20/20**, **433/447** ; ambigu **`und`**
([fiche](../../reports/rapport-profils.md)).

**T6 — le bilan exploitable (15/11, 23 h 35).** Cinq briques : installation éditable,
quickstart 3/3, API (2 139 objets, 8 rôles), performance (10 000 mots 4,01 s, 126 Mio), CLI
20/20. Trois limites : clone public 88,70 % d'attachement au lieu de 99,58 %, O(k²) (α = 1,55),
gold de 
… [4350 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"SEUIL_TAGGER\\|MODELE_TAGGER\\|PRIORITE_TAGGER\" tools/drave.py | head -20 && sed -n '40,90p' tools/drave.py", "description": "Find constants and imports"}`

  ```
74:MODELE_TAGGER = "deepseek-chat"
75:SEUIL_TAGGER = 0.6
79:PRIORITE_TAGGER = dict(bl.PRIORITE_NIVEAU)
80:PRIORITE_TAGGER["syntagme"] = "heuristique"
384:    pos = bl.NeuronalLLMPOS(MODELE_TAGGER, transport=transport)
386:                         seuil=SEUIL_TAGGER, priorite_syntagme="confiance",
387:                         priorite_par_niveau=PRIORITE_TAGGER)
403:    return {"modele": MODELE_TAGGER, "appels": stats["appels"],
424:        "modele": cout.get("modele", MODELE_TAGGER),
435:    return (f"modèle={MODELE_TAGGER} · appels={stats['appels']} "
955:            "modele": MODELE_TAGGER,
956:            "seuil": SEUIL_TAGGER,
Codes de sortie : 0 succès · 3 refus d'analyse · 4 clé/dépendance absente
(ou fichier introuvable) · 5 usage · 1 autre erreur.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import pathlib
import random
import sys
import textwrap

# Le dépôt d'abord — `sys.path.insert(0, '.')` quand on lance depuis sa racine, et les chemins
# déduits du fichier pour que la commande marche aussi depuis un autre répertoire. Aucun paquet
# externe n'est importé : le point d'entrée est autonome.
sys.path.inse
… [1377 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1400,1500p' tools/drave.py", "description": "Read main error handling"}`

  ```
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
    brut = list(sys.argv[1:] if argv is None else argv)
    args = construire_parseur().parse_args(_normaliser_tagger(brut))
    args.tagger_mode = ("auto" if getattr(args, "tagger_auto", False)
                        else "api" if getattr(args, "tagger", False) else None)
    try:
        return args.fonction(args)
    except BrokenPipeError:
        # `drave analyser ... | head` : le lecteur a fermé la sortie, ce n'est pas une erreur.
        return 0
    except KeyboardInterrupt:
        print(f"{NOM}: interrompu", file=sys.stderr)
        return 1
    except ErreurEntree as exc:
        # --fichier : dépendance (4) ou usage (5), message clair, rien sur stdout, pas de trace
        prefixe = "erreur d'usage" if exc.code == 5 else "dépendance absente"
        print(f"{NOM}: {prefixe} : {exc}", file=sys.stderr)
        return exc.code
    except pu.ProfilsAbsents as exc:
        # les profils sont une dépendance de données : code 4, rien sur stdout, pas de trace
        print(f"{NOM}: dépendance absente : {exc}", file=sys.stderr)
        return 4
    except GoldAbsent 
… [649 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nfor f in [\"gold_synthetique.json\",\"gold_reel.json\"]:\n d=json.load(open(\"tools/tests/linguistique/\"+f))\n print(f, d[\"phrases\"][0].get(\"source\"), d[\"phrases\"][0].keys())\nPY", "description": "Check synth source field"}`

  ```
gold_synthetique.json synthetique dict_keys(['id', 'langue', 'texte', 'pragma', 'source', 'mots', 'segments'])
gold_reel.json reel dict_keys(['id', 'langue', 'texte', 'mots', 'segments', 'pragma', 'source'])
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "old_string": "PRIORITE_TAGGER = dict(bl.PRIORITE_NIVEAU)\nPRIORITE_TAGGER[\"syntagme\"] = \"heuristique\"\n\n\n# --------------------------------------------------------------------------- sorties JSON", "new_string": " … [475 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py": file has not been read — read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "offset": 70, "limit": 20}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py</path>
<type>file</type>
<content>
70: VERSION = "0.1.0"
71: LARGEUR = 100
72: 
73: # Le tagger est une **option** : sans `--tagger`, rien de ce bloc n'est importé ni exécuté.
74: MODELE_TAGGER = "deepseek-chat"
75: SEUIL_TAGGER = 0.6
76: # La fusion de l'option : le POS vient du tagger, tout le reste de l'heuristique. On ne force
77: # pas les syntagmes du neuronal (`PRIORITE_NIVEAU` le ferait) parce qu'ils n'ont ni rôle ni
78: # cible : l'attachement mesuré du produit serait perdu. Le gain mesuré porte sur le POS.
79: PRIORITE_TAGGER = dict(bl.PRIORITE_NIVEAU)
80: PRIORITE_TAGGER["syntagme"] = "heuristique"
81: 
82: 
83: # --------------------------------------------------------------------------- sorties JSON
84: 
85: 
86: def _sur(s: str) -> str:
87:     """Une chaîne toujours **écrivable** : un surrogate isolé devient U+FFFD (jamais d'exception)."""
88:     return s.encode("utf-8", "replace").decode("utf-8", "replace")
89: 

(Showing lines 70-89 of 1438. Use offset=90 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "old_string": "PRIORITE_TAGGER = dict(bl.PRIORITE_NIVEAU)\nPRIORITE_TAGGER[\"syntagme\"] = \"heuristique\"\n\n\n# --------------------------------------------------------------------------- sorties JSON", "new_string": " … [475 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "limit": 30, "offset": 875}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py</path>
<type>file</type>
<content>
875:                 f"{a['cibles']} cibles d'attachement",
876:                 f"      POS {_pct(p['exactitude'])} (fermé {_pct(p['exactitude_ferme'])}, "
877:                 f"ouvert {_pct(p['exactitude_ouvert'])}) · SYNTAGMES F1 {_pct(s['f1'])} "
878:                 f"(tête {_pct(s['tete']['f1'])})",
879:                 f"      ATTACHEMENT exact {_pct(a['exact_taux'])} · "
880:                 f"couverture {_pct(a['couverture'])} · top-k {_pct(a['topk_taux'])} · "
881:                 f"PRAGMATIQUE acte {_pct(pr['acte'])}",
882:                 f"      CONTRÔLE NÉGATIF cible exacte tirée au hasard {_pct(c['exact_taux'])} "
883:                 f"(graine {c['graine']}, {c['cibles']} cibles)",
884:             ]
885:             t = m.get("tagger")
886:             if t:
887:                 lignes.append(
888:                     f"      TAGGER POS {_pct(t['pos']['exactitude'])} "
889:                     f"· Δ {_points(t['delta_pos'])} "
890:                     f"· SYNTAGMES F1 {_pct(t['syntagme']['f1'])} "
891:                     f"(tête {_pct(t['syntagme']['tete']['f1'
… [749 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "old_string": "    return \"\\n\".join(lignes)\n\n\ndef cmd_evaluer(args: argparse.Namespace) -> int:\n    if getattr(args, \"tagger_auto\", False):", "new_string": "    return \"\\n\".join(lignes)\n\n\n# --------------- … [7809 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "limit": 25, "offset": 1060}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py</path>
<type>file</type>
<content>
1060:     ]
1061:     c = rapport["controle_negatif"]
1062:     lignes.append(
1063:         f"CONTRÔLE NÉGATIF {c['nom']} · POS {_pct(c['pos'])} < {c['plancher']:.2f} "
1064:         f"{'✅' if c['ok'] else '❌'} (échec attendu, code {c['code']})"
1065:     )
1066:     return "\n".join(lignes)
1067: 
1068: 
1069: def cmd_evaluer(args: argparse.Namespace) -> int:
1070:     if getattr(args, "tagger_auto", False):
1071:         print(f"{NOM}: erreur d'usage : --tagger auto n'est disponible que pour analyser",
1072:               file=sys.stderr)
1073:         return 5
1074:     evaluateur = _module_evaluation(gele=bool(args.gold))
1075:     phrases = evaluateur.charger_gele() if args.gold else evaluateur.charger()
1076:     if getattr(args, "reel", False):
1077:         # la **base honnête** : les phrases réelles (main + corpus), sans le synthétique
1078:         phrases = [p for p in phrases if p.get("source") in ("hand", "reel")]
1079:     cascade = None
1080:     stats = None
1081:     if getattr(args, "tagger", False):
1082:         try:
1083:             cascade, stats = _constr
… [135 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "new_string": "def cmd_evaluer(args: argparse.Namespace) -> int:\n    if getattr(args, \"tagger_auto\", False):\n        print(f\"{NOM}: erreur d'usage : --tagger auto n'est disponible que pour analyser\",\n              … [1378 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "limit": 40, "offset": 1495}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py</path>
<type>file</type>
<content>
1495:     evaluer.add_argument("--reel", action="store_true",
1496:                          help="mesurer la base honnête : les phrases réelles (hand + reel), sans synthétique")
1497:     evaluer.add_argument("--par-langue", action="store_true",
1498:                          help="scinder la mesure en français et en anglais")
1499:     evaluer.add_argument("--tagger", action="store_true",
1500:                          help="mesurer en plus la cascade POS de l'API DeepSeek (clé et réseau)")
1501:     evaluer.add_argument("--tagger-auto", action="store_true", help=argparse.SUPPRESS)
1502:     evaluer.add_argument("--json", action="store_true",
1503:                          help="sortie JSON des mesures complètes")
1504:     evaluer.set_defaults(fonction=cmd_evaluer)
1505: 
1506:     profils = sous.add_parser(
1507:         "profils",
1508:         help="détecter la langue d'un texte (398 profils UDHR)",
1509:         description="Détecte la langue probable, le script et la confiance d'un texte avec "
1510:                     "les profils de trigrammes UDHR (398 langues, articl
… [1785 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "limit": 30, "offset": 1470}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py</path>
<type>file</type>
<content>
1470:                                "changer le code de sortie")
1471:     analyser.add_argument("--tagger-auto", action="store_true", help=argparse.SUPPRESS)
1472:     analyser.add_argument("--json", action="store_true",
1473:                           help="sortie JSON complète (annotation, sans durée sauf avec --duree)")
1474:     analyser.add_argument("--duree", action="store_true",
1475:                           help="ajouter la durée de l'analyse (cout.duree_s) au JSON "
1476:                                "ou à chaque ligne de --jsonl")
1477:     analyser.set_defaults(fonction=cmd_analyser)
1478: 
1479:     evaluer = sous.add_parser(
1480:         "evaluer",
1481:         help="mesurer l'heuristique sur le gold",
1482:         description="Mesure POS, syntagmes (F1/tête) et attachement (exact/couverture) "
1483:                     "sur le gold, avec un contrôle négatif reproductible. Avec --par-langue, "
1484:                     "donne le même détail pour le français et l'anglais. Avec --tagger, mesure "
1485:                     "en plus la cascade POS de l'API DeepS
… [1078 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "new_string": "    evaluer = sous.add_parser(\n        \"evaluer\",\n        help=\"mesurer l'heuristique sur le gold\",\n        description=\"Mesure POS, syntagmes (F1/tête) et attachement (exact/couverture) \"\n       … [2059 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **bash** `{"command": "python3 -m py_compile tools/drave.py && echo OK", "description": "Compile drave.py"}`

  ```
OK
  ```

- **bash** `{"command": "python3 tools/drave.py evaluer --strict --json > /tmp/evaluer-strict.json; code=$?; echo \"EXIT=$code\"; python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/evaluer-strict.json'))\nprint(d['gold'])\nprint(d['verdict'])\nfor g in ('612','452'):\n print(g, {m: (d['modes'][g][m]['pos'][' … [265 caractères tronqués]`

  ```
EXIT=0
{'vivant': {'nom': 'vivant (hand + reel + synthétique)', 'phrases': 612, 'tokens': 3179}, 'reel': {'nom': 'réel (hand + reel, sans synthétique)', 'phrases': 452, 'tokens': 2480}}
{'plancher': 0.7, 'cascade_pos_612': 0.8625, 'cascade_pos_452': 0.8891, 'passe_612': True, 'passe_452': True, 'ok': True}
612 {'heuristique': (0.8625, 0.7902), 'neuronal': (0.754, 0.7651), 'parallele': (0.8625, 0.7902), 'cascade': (0.8625, 0.7902)}
452 {'heuristique': (0.8891, 0.7906), 'neuronal': (0.7621, 0.7448), 'parallele': (0.8891, 0.7906), 'cascade': (0.8891, 0.7906)}
negative {'nom': 'cascade dégradée (POS forcé à X)', 'gold': 'réel 452', 'phrases': 452, 'pos': 0.0, 'plancher': 0.7, 'passe': False, 'code': 1, 'attendu': 'échec (code 1)', 'ok': True}
delta 452 {'neuronal': {'pos': -0.127, 'syntagme_f1': -0.0458, 'syntagme_tete_f1': -0.0293, 'attachement_exact': -0.9946, 'pragmatique_acte': 0.0}, 'parallele': {'pos': 0.0, 'syntagme_f1': 0.0, 'syntagme_tete_f1': 0.0, 'attachement_exact': 0.0, 'pragmatique_acte': 0.0}, 'cascade': {'pos': 0.0, 'syntagme_f1': 0.0, 'syntagme_tete_f1': 0.0, 'attachement_exact': 0.0, 'pragmatique_acte': 0.0}}
  ```

- **bash** `{"command": "python3 tools/drave.py evaluer --strict; echo \"EXIT=$?\"", "description": "Run strict human output", "timeoutMs": 300000}`

  ```
drave 0.1.0 — évaluation stricte (cascade locale, plancher 0.70)
gold vivant 612 phrases · 3179 tokens · gold réel 452 phrases · 2480 tokens

GOLD VIVANT 612
mode               POS      ΔPOS  SYNT. F1       ΔF1   TÊTE F1     ΔTÊTE
heuristique    86.25 %         —   79.02 %         —   90.29 %         —
neuronal       75.40 % -10.85 pts   76.51 % -2.51 pts   88.07 % -2.22 pts
parallele      86.25 % +0.00 pts   79.02 % +0.00 pts   90.29 % +0.00 pts
cascade        86.25 % +0.00 pts   79.02 % +0.00 pts   90.29 % +0.00 pts
cascade : 612 appels neuronaux sur 612 phrases

GOLD RÉEL 452
mode               POS      ΔPOS  SYNT. F1       ΔF1   TÊTE F1     ΔTÊTE
heuristique    88.91 %         —   79.06 %         —   89.90 %         —
neuronal       76.21 % -12.70 pts   74.48 % -4.58 pts   86.97 % -2.93 pts
parallele      88.91 % +0.00 pts   79.06 % +0.00 pts   89.90 % +0.00 pts
cascade        88.91 % +0.00 pts   79.06 % +0.00 pts   89.90 % +0.00 pts
cascade : 452 appels neuronaux sur 452 phrases

PLANCHER 0.70 — cascade POS 86.25 % (612) ✅ · 88.91 % (452) ✅ — code 0
CONTRÔLE NÉGATIF cascade dégradée (POS forcé à X) · POS 0.00 % < 0.70 ✅ (échec attendu, code 1)
EXIT=0
  ```

- **bash** `{"command": "sed -n '1,50p' tools/tests/test_tagger_api.py", "description": "Read test import style"}`

  ```
"""test_tagger_api.py — le tagger POS par API, **en option**, sans réseau.

Ce que le fichier verrouille, avec un **transport factice** (une fonction qui rend un JSON de
POS valide) :

1. la cascade remplace bien les POS par ceux du tagger (et garde les syntagmes de l'heuristique,
   avec leurs rôles et leurs cibles) ;
2. le JSON reste valide : le schéma **déclaré** (v2) le lit, et le contrat **v1** reste lisible ;
3. deux analyses du même texte ne refont pas d'appel (cache mémoire des taggers) ;
4. le défaut est inchangé : `analyser --json` sans `--tagger` rend exactement l'heuristique ;
5. les quatre cas d'erreur, chacun avec un transport factice :
   - **clé absente** → code **4**, message clair, `stdout` vide (`TestCle.test_sans_cle_code_4`) ;
   - **clé invalide** (HTTP 401/403) → code **4**, message clair, `stdout` vide, pas de repli ;
   - **réseau coupé** → **repli heuristique**, code **0**, `refus` non vide et message sur `stderr` ;
   - **refus du modèle** (texte non JSON, JSON incomplet) → **repli heuristique**, code **0**,
     `refus` non vide ;
6. l'ordre de résolution de la clé : `DEEPSEEK_KEY_FILE`, puis `~/.config/drave/deepseek.key`,
   puis `DEEPSEEK_API_KEY` ;
7
… [1027 caractères tronqués]
  ```

- **bash** `{"command": "wc -c /tmp/evaluer-strict.json && python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/evaluer-strict.json'))\nprint(list(d['modes']['612']['heuristique'].keys()))\nPY", "description": "Check strict JSON size"}`

  ```
23260 /tmp/evaluer-strict.json
['bloc', 'phrases', 'pos', 'syntagme', 'pragmatique', 'fraction_semantique', 'attachement', 'attachement_tete']
  ```

- **bash** `{"command": "cat > tools/tests/test_evaluer_strict.py <<'PY'\n\"\"\"test_evaluer_strict.py — le mode `evaluer --strict` : quatre modes, plancher 0,70, code 1.\n\nCe que le fichier verrouille :\n\n1. `evaluer --strict --json` mesure les **quatre modes** (heuristique, neuronal, parallèle,\n   cascade) … [5593 caractères tronqués]`

  ```
[stderr]
.....
----------------------------------------------------------------------
Ran 5 tests in 10.707s

OK
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-produit.sh", "limit": 80, "offset": 40}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-produit.sh</path>
<type>file</type>
<content>
40: assert d['script'] == 'Latn', d.get('script')
41: assert d['profils']['langues'] == 398, d.get('profils')
42: assert 0.0 < d['confiance'] <= 1.0, d.get('confiance')
43: " 2>/dev/null; then
44:   dit ✅ "profils : langue, script, confiance, 398 profils"
45: else
46:   dit ❌ "profils : sortie inattendue : $sortie"; ko=1
47: fi
48: 
49: a=$(python3 tools/drave.py rejouer "Le chat dort." 2>&1 | grep -o 'sha256 [0-9a-f]*' | head -1)
50: b=$(python3 tools/drave.py rejouer "Le chat dort." 2>&1 | grep -o 'sha256 [0-9a-f]*' | head -1)
51: if [ -n "$a" ] && [ "$a" = "$b" ]; then dit ✅ "rejeu : $a deux fois"; else dit ❌ "rejeu instable : '$a' vs '$b'"; ko=1; fi
52: 
53: if python3 tools/tests/test_produit.py >/tmp/porte-produit-tests.log 2>&1; then
54:   dit ✅ "smoke test : $(grep -oE 'Ran [0-9]+ tests' /tmp/porte-produit-tests.log | head -1)"
55: else
56:   dit ❌ "smoke test en échec (voir /tmp/porte-produit-tests.log)"; ko=1
57: fi
58: 
59: if python3 tools/verifier_schema_produit.py --gold 20 >/tmp/porte-produit-valide.log 2>&1; then
60:   dit ✅ "schéma v2 validé (5 cas v2 + 1
… [2906 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-produit.sh", "new_string": "if python3 tools/tests/test_produit.py >/tmp/porte-produit-tests.log 2>&1; then\n  dit ✅ \"smoke test : $(grep -oE 'Ran [0-9]+ tests' /tmp/porte-produit-tests.log | head -1)\"\nelse\n  dit ❌ \"smok … [633 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-produit.sh has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "limit": 35, "offset": 1380}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py</path>
<type>file</type>
<content>
1380:     i = 0
1381:     while i < len(argv):
1382:         jeton = argv[i]
1383:         if jeton == "--tagger" and i + 1 < len(argv) and argv[i + 1] in ("auto", "api", "explicite"):
1384:             valeur = argv[i + 1]
1385:             sortie.append("--tagger-auto" if valeur == "auto" else "--tagger")
1386:             i += 2
1387:             continue
1388:         if jeton.startswith("--tagger="):
1389:             valeur = jeton.split("=", 1)[1]
1390:             if valeur == "auto":
1391:                 sortie.append("--tagger-auto")
1392:             elif valeur in ("api", "explicite"):
1393:                 sortie.append("--tagger")
1394:             else:
1395:                 sortie.append(jeton)
1396:         else:
1397:             sortie.append(jeton)
1398:         i += 1
1399:     return sortie
1400: 
1401: 
1402: def construire_parseur() -> argparse.ArgumentParser:
1403:     epilogue = (
1404:         "Commandes : analyser, evaluer, profils, rejouer, restituer.\n"
1405:         "Codes de sortie : 0 succès · 3 refus d'analyse (JSON) · 4 clé/dépendance absente\n
… [952 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "new_string": "        \"Options : --json, --jsonl, --duree, --fichier CHEMIN, --langue fr|en,\\n\"\n        \"--partition brut|alternative|filtrer_union|filtrer, --contexte, --banc, --tagger [auto],\\n\"\n        \"--st … [1267 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "limit": 25, "offset": 1}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """drave.py — le point d'entrée produit du bloc linguistique.
3: 
4: Une seule commande, cinq gestes, hors ligne et déterministe :
5: 
6:     python3 tools/drave.py analyser "Le chat dort."
7:     python3 tools/drave.py analyser "The cat sleeps on the roof." --langue en --json
8:     python3 tools/drave.py analyser "Le chat dort." --tagger          # API DeepSeek (clé, réseau)
9:     python3 tools/drave.py analyser "Le chat dort." --tagger auto     # API si clé, sinon heuristique
10:     python3 tools/drave.py evaluer
11:     python3 tools/drave.py evaluer --gold --json
12:     python3 tools/drave.py profils --texte "Le chat dort."
13:     python3 tools/drave.py profils --texte "Привет мир" --json
14:     python3 tools/drave.py analyser "Le chat dort." --profils
15:     python3 tools/drave.py evaluer --tagger --json                    # heuristique + cascade API
16:     python3 tools/drave.py rejouer "Le chat de la voisine qui dort sur le toit se réveille."
17:     python3 tools/drave.py restituer "Le chat dort."
18:     python3 tools/drave.py restitu
… [626 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "new_string": "    python3 tools/drave.py evaluer\n    python3 tools/drave.py evaluer --gold --json\n    python3 tools/drave.py evaluer --strict --json                    # quatre modes, plancher 0,70\n", "old_string": " … [88 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "limit": 32, "offset": 1025}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py</path>
<type>file</type>
<content>
1025:         f"{rapport['plancher']:.2f})",
1026:         f"gold vivant {rapport['gold']['vivant']['phrases']} phrases · "
1027:         f"{rapport['gold']['vivant']['tokens']} tokens · "
1028:         f"gold réel {rapport['gold']['reel']['phrases']} phrases · "
1029:         f"{rapport['gold']['reel']['tokens']} tokens",
1030:     ]
1031:     for nom_gold, titre in (("612", "GOLD VIVANT 612"), ("452", "GOLD RÉEL 452")):
1032:         mesures = rapport["modes"][nom_gold]
1033:         deltas = rapport["delta"][nom_gold]
1034:         lignes += [
1035:             "",
1036:             titre,
1037:             f"{'mode':<12} {'POS':>9} {'ΔPOS':>9} {'SYNT. F1':>9} {'ΔF1':>9} "
1038:             f"{'TÊTE F1':>9} {'ΔTÊTE':>9}",
1039:         ]
1040:         for nom in ("heuristique", "neuronal", "parallele", "cascade"):
1041:             m = mesures[nom]
1042:             d = deltas.get(nom)
1043:             delta_pos = _points(d["pos"]) if d else "—"
1044:             delta_f1 = _points(d["syntagme_f1"]) if d else "—"
1045:             delta_tete = _points(d["syntagme_tete_f1"]) i
… [616 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "new_string": "            f\"{'mode':<12} {'POS':>9} {'ΔPOS':>11} {'SYNT. F1':>9} {'ΔF1':>11} \"\n            f\"{'TÊTE F1':>9} {'ΔTÊTE':>11}\",\n        ]\n        for nom in (\"heuristique\", \"neuronal\", \"parallele … [1333 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/drave.py evaluer --strict --json > reports/evaluer-strict.json && echo \"EXIT=$?\" && wc -c reports/evaluer-strict.json && python3 tools/drave.py evaluer --strict", "description": "Generate report JSON and human output", "timeoutMs": 300000}`

  ```
EXIT=0
23260 reports/evaluer-strict.json
drave 0.1.0 — évaluation stricte (cascade locale, plancher 0.70)
gold vivant 612 phrases · 3179 tokens · gold réel 452 phrases · 2480 tokens

GOLD VIVANT 612
mode               POS        ΔPOS  SYNT. F1         ΔF1   TÊTE F1       ΔTÊTE
heuristique    86.25 %           —   79.02 %           —   90.29 %           —
neuronal       75.40 %  -10.85 pts   76.51 %   -2.51 pts   88.07 %   -2.22 pts
parallele      86.25 %   +0.00 pts   79.02 %   +0.00 pts   90.29 %   +0.00 pts
cascade        86.25 %   +0.00 pts   79.02 %   +0.00 pts   90.29 %   +0.00 pts
cascade : 612 appels neuronaux sur 612 phrases

GOLD RÉEL 452
mode               POS        ΔPOS  SYNT. F1         ΔF1   TÊTE F1       ΔTÊTE
heuristique    88.91 %           —   79.06 %           —   89.90 %           —
neuronal       76.21 %  -12.70 pts   74.48 %   -4.58 pts   86.97 %   -2.93 pts
parallele      88.91 %   +0.00 pts   79.06 %   +0.00 pts   89.90 %   +0.00 pts
cascade        88.91 %   +0.00 pts   79.06 %   +0.00 pts   89.90 %   +0.00 pts
cascade : 452 appels neuronaux sur 452 phrases

PLANCHER 0.70 — cascade POS 86.25 % (612) ✅ · 88.91 % (452) ✅ — code 0
CONTRÔLE NÉGATIF cascade dégra
… [65 caractères tronqués]
  ```

- **bash** `{"command": "cat > reports/rapport-evaluer-strict.md <<'MD'\n# V1 — `evaluer --strict` : les quatre modes locaux, la cascade à 86,25 % / 88,91 %, le plancher 0,70 qui mord\n\n> **Ligne de roadmap** : **B13** (le produit) · **Tâche** : **V1** (la suite du bilan T6) ·\n> **Date** : 2026-11-16 · **Verd … [7763 caractères tronqués]`

  ```
126 reports/rapport-evaluer-strict.md
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "limit": 55, "offset": 164}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md</path>
<type>file</type>
<content>
164: ### 3.3 Mesurer sur le gold
165: 
166: ```bash
167: python3 tools/drave.py evaluer
168: ```
169: ```
170: drave 0.1.0 — évaluation de l'heuristique sur le gold
171: gold vivant (hand + reel + synthétique) · 612 phrases · 3179 tokens · 239 cibles d'attachement
172: 
173: POS         exactitude 86.25 %  (fermé 93.73 %, ouvert 79.18 %)
174: SYNTAGMES   F1 79.02 %  (P 78.60 % / R 79.44 %)
175:   tête      F1 90.29 %  (P 92.61 % / R 88.08 %)
176:   vue linéaire (partition filtrer) F1 81.44 %  · attachement 93.72 % de couverture
177: ATTACHEMENT exact 99.58 % · couverture 99.58 % · exact sur span 100.00 % · top-k 98.74 %
178:   tête      couverture 100.00 % · top-k 99.16 %
179: PRAGMATIQUE acte 99.67 % · négation 97.71 % · modalité 98.86 % · double sens 94.44 %
180: FRACTION SÉMANTIQUE 54.76 %
181: CONTRÔLE NÉGATIF cible exacte tirée au hasard 1.67 % (graine 0, 239 cibles)
182: ```
183: 
184: **Lecture.** `exact 99.58 %` est le **rendement** (238/239 cibles) ; `exact sur span 100.00 %` est
185: l'**exactitude** sur les 238 segments dont le span est prédit. La seule cible r
… [2390 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "**Lecture.** `exact 99.58 %` est le **rendement** (238/239 cibles) ; `exact sur span 100.00 %` est\nl'**exactitude** sur les 238 segments dont le span est prédit. La seule cible restante (`g017`)\n … [666 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "**confondu avec la source**. Lire la langue avec la source, jamais l'une sans l'autre. La fiche\ncomplète est [`rapport-evaluer-langue.md`](../../reports/rapport-evaluer-langue.md).\n\n**Le mode st … [2846 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "limit": 14, "offset": 14}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md</path>
<type>file</type>
<content>
14: > existe, l'heuristique sinon, **sans changer le code de sortie** ; il ne change pas le défaut.
15: > Le format
16: > est **version 2** (`schema: "drave.annotation"`,
17: > `version: 2`) : le schéma v2 ajoute `meta.partition` et `meta.alternative`, et la **version 1
18: > reste lue** ([`tools/schemas/`](../../tools/schemas/)). Les sorties du § 3.1, du § 3.4 et du
19: > § 3.5 ont été relancées le 07/11 pour le format v2 ; les mesures chiffrées du § 2 datent du
20: > **06/11**, et l'`evaluer` du § 3.3 a été relancé le **14/11** (gold vivant 612, `--par-langue
21: > fr/en`). Ce qui manque encore au contrat est nommé au § 7, sans être présenté comme acquis.
22: > La **FAQ** (§ 8) est vérifiée à part le **2026-11-15** par
23: > [`tools/verifier_faq.py`](../../tools/verifier_faq.py) : **10/10** réponses.
24: >
25: > **Le produit en une phrase.** Vous donnez un texte ; il rend une **annotation** — langue,
26: > classes de mots, syntagmes, attachements, acte de parole — avec ses spans, sa confiance et ses
27: > candidats, de façon **déterministe**, et il sait **se mesurer** s
… [96 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "> **06/11**, et l'`evaluer` du § 3.3 a été relancé le **16/11** (gold vivant 612, `--par-langue\n> fr/en`, `--strict`) ; la fiche du mode strict est [`rapport-evaluer-strict.md`](../../reports/rapp … [237 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "> **06/11**, et l'`evaluer` du § 3.3 a été relancé le **16/11** (gold vivant 612, `--par-langue\n> fr/en`, `--strict`) ; la fiche du mode strict est [`rapport-evaluer-strict.md`](../../reports/rapp … [353 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **bash** `{"command": "grep -n \"cascade\\|--strict\\|teste pas\" docs/produit/README.md | head -60", "description": "Search README for cascade mentions"}`

  ```
21:> fr/en`, `--strict`) ; la fiche du mode strict est [`rapport-evaluer-strict.md`](../../reports/rapport-evaluer-strict.md).
189:teste pas la cascade ; c'est le rôle de `--strict`.
221:**Le mode strict — `--strict`.** Le banc de recherche mesure quatre modes et un plancher ; le CLI
225:python3 tools/drave.py evaluer --strict
228:drave 0.1.0 — évaluation stricte (cascade locale, plancher 0.70)
236:cascade        86.25 %   +0.00 pts   79.02 %   +0.00 pts   90.29 %   +0.00 pts
237:cascade : 612 appels neuronaux sur 612 phrases
244:cascade        88.91 %   +0.00 pts   79.06 %   +0.00 pts   89.90 %   +0.00 pts
245:cascade : 452 appels neuronaux sur 452 phrases
247:PLANCHER 0.70 — cascade POS 86.25 % (612) ✅ · 88.91 % (452) ✅ — code 0
248:CONTRÔLE NÉGATIF cascade dégradée (POS forcé à X) · POS 0.00 % < 0.70 ✅ (échec attendu, code 1)
252:parallèle, cascade — sur le gold vivant **612** et sur le réel **452**, puis affiche le
254:l'**exactitude POS de la cascade** : si l'un des deux golds est sous 0,70, la commande sort en
255:**code 1**. Ici la cascade vaut **86,25 %** (612) et **88,91 %** (452) : **code 0**.
257:**Le contrôle négatif est dans la passe.** Une cascade dont le POS est forc
… [2407 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "limit": 60, "offset": 680}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "limit": 40, "offset": 860}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md</path>
<type>file</type>
<content>
680: `contenu`, `theme` et `groupe nominal` tombent sur `objet` ; `attribut`, `maniere`,
681: `concession`, `hypothese`, `cause` et `consequence` sur `qualite`. C'est une
682: **normalisation**, pas une annotation plus fine : `objet` et `qualite` sont des catégories
683: larges, et le rapport [`rapport-contrat-json.md`](../../reports/rapport-contrat-json.md)
684: nomme ce que la table ne dit pas.
685: 
686: **2. Un span reste inatteignable.** Sur **239 cibles**, **238** sont attachées (couverture
687: **0,9958**) ; **1** ne l'est pas : `g017` (une convention du gold, déclarée inatteignable le
688: 14/11 — la règle coûtait deux autres spans). Elles sont
689: **inatteignables sans corriger le gold ou le lexique** — quatre sont des cas réels nommés dans
690: l'audit v10 (`r035`, `r255`, `r264`, `g017`), les autres viennent du gold synthétique, dont le
691: lexique est disjoint. Conséquence : **238/239 (0,9958)** est l'exactitude **conditionnelle aux
692: spans prédits**, pas la couverture du langage. Lire les deux ensemble.
693: 
694: **Le doublon REL de l'union.** Deux REL 
… [3461 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md</path>
<type>file</type>
<content>
860: 
861: | option | commande | sens |
862: |---|---|---|
863: | `--langue fr\|en` | `analyser`, `rejouer`, `restituer` | **indice** de langue, pas une contrainte ; hors `fr`/`en` → code 5 |
864: | `--json` | `analyser`, `evaluer`, `profils`, `restituer` | sortie machine UTF-8 |
865: | `--duree` | `analyser` | ajoute `cout.duree_s` au JSON (ou à chaque ligne de `--jsonl`) ; absent par défaut |
866: | `--tagger` | `analyser`, `evaluer` | POS par l'API DeepSeek (clé et réseau ; défaut : heuristique) ; `evaluer` mesure en plus la cascade et le Δ (§ 3.7) |
867: | `--jsonl` | `analyser` | une ligne JSON par phrase (avec `--fichier`) |
868: | `--fichier CHEMIN` | `analyser`, `profils`, `restituer` | lit un texte UTF-8 au lieu de l'argument |
869: | `--banc CHEMIN` | `restituer` | mesure un banc JSON de textes (les 50 textes libres) |
870: | `--canonique` | `restituer` | ajoute la forme canonique v1 (segments + rôles + cibles) et son miroir |
871: | `--roles` | `restituer` | ajoute la forme lisible des rôles (agent, prédicat, lieu) ; avec `--banc`, mesure leur fidélité à l'or |
… [2675 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "limit": 30, "offset": 645}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md</path>
<type>file</type>
<content>
645: constructeur).
646: 
647: **La mesure.** Sur les **20 langues stratifiées** de l'échantillon UDHR (5 familles × 4,
648: 10 écritures), article 15 tenu à l'écart : **20/20** langues et **20/20** scripts ; sur les
649: articles 15–30 : **313/320 = 0,9781** (script **320/320**). L'autotest complet 398 langues
650: donne **433/447 = 0,9687** avec les profils bruts et **431/447 = 0,9642** par le chemin CLI.
651: Le texte ambigu bilingue rend **`und`** (0,0836 < 0,12) ; les profils permutés tombent à
652: **0/20** (0,0022 sur 447). Dispositif, JSON et limites :
653: [`rapport-profils.md`](../../reports/rapport-profils.md) et
654: [`profils.json`](../../reports/profils.json).
655: 
656: **Ce que ce n'est pas.** Une précision de déploiement : l'échantillon est **stratifié**, pas
657: aléatoire, l'UDHR est propre et parallèle, et la confiance n'est **pas calibrée**. Les langues
658: proches (mandarin/jinyu, anglais/scots) et le texte court hors des sept langues à mots-outils
659: restent les points faibles.
660: 
661: ## 4. Ce que le produit ne fait pas encore
662: 
663: **1.
… [982 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "**3. `cascade_pos` : le plancher, désormais mesuré par le CLI.** `evaluer --strict` applique le\n**plancher 0,70** à la cascade locale (`MockNeuronal`) et sort en **1** sous le seuil. Sur le\ngold  … [1649 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "| `--gold` | `evaluer` | gold gelé 602 au lieu du vivant 612 |\n| `--strict` | `evaluer` | quatre modes locaux sur 612 et 452, plancher 0,70 sur la cascade POS (échec = code 1) ; exclusif avec `--g … [348 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "| **`--mode` / la cascade locale en analyse** | `evaluer --strict` **mesure** les quatre modes locaux ; `analyser` n'expose pas `--mode` : la cascade locale en production demande encore le code Pyt … [853 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "limit": 15, "offset": 894}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md</path>
<type>file</type>
<content>
894: **Ce qui est déjà tenu** : `--version`, `--aide`, les **cinq** sous-commandes, les **398
895: profils de langue** (`drave profils`, `analyser --profils`), le JSON
896: déterministe, le rejeu par empreinte, le **format versionné** (schéma v2, v1 lue),
897: `--fichier`/`--jsonl`, `--duree`, `--banc`, `--partition`, le **tagger API en option** (`--tagger`, code 4,
898: cache), la **restitution v0** (46/46 surfaces exactes,
899: miroir strict 0,1087), la **forme canonique v1** (`--canonique`, 46/46 canonique, strict
900: inchangé), les **candidats d'attachement en objets** `{span, cible, source}` et le
901: **vocabulaire fermé des rôles** (`predicat` sans accent ; 21 rôles bruts → 8, 0 hors
902: table sur le gold 612), la porte produit et le smoke test. Le reste est nommé ci-dessus,
903: sans être présenté comme acquis.
904: 
905: ## 8. FAQ — dix questions
906: 
907: > **Vérifié le 2026-11-15** contre le code courant (`drave 0.1.0`) par
908: > [`tools/verifier_faq.py`](../../tools/verifier_faq.py) : **10/10** réponses passent et le

(Showing lines 894-908 of 1073. Use of
… [33 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "`--fichier`/`--jsonl`, `--duree`, `--banc`, `--partition`, le **tagger API en option** (`--tagger`, code 4,\ncache), le **mode strict** (`--strict`, quatre modes, plancher 0,70, code 1), la **resti … [219 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **bash** `{"command": "sed -n '280,380p' tools/verifier_faq.py", "description": "Inspect FAQ verifier phantom options"}`

  ```
assert s0["controle_negatif"]["detectes"] == 46, s0["controle_negatif"]

    v1 = _json(["restituer", "--banc", banc, "--canonique"])
    s1 = v1["synthese"]
    assert s1["canonique"]["exacts"] == 46, s1["canonique"]
    assert s1["strict"]["fidelite"] == 0.1087, s1["strict"]
    assert s1["structure"]["segments"] == 395, s1["structure"]
    assert s1["structure"]["attachements"] == 315, s1["structure"]

    v2 = _json(["restituer", "--banc", banc, "--roles"])
    s2 = v2["synthese"]
    assert s2["cadre"]["exacts"] == 19 and s2["cadre"]["exacts_non_vides"] == 16, s2["cadre"]
    assert s2["roles"]["f1"] == 0.527, s2["roles"]
    assert s2["controles"]["rendu"]["exacts"] == 46, s2["controles"]["rendu"]
    assert s2["controles"]["spans_dans_source"] == {"justes": 198, "total": 198,
                                                    "taux": 1.0}, s2["controles"]

    une = _json(["restituer", "Le chat dort.", "--roles"])
    principal = une["roles"]["principal"]
    assert (principal["agent"], principal["predicat"], principal["lieu"]) == ("Le chat", "dort", ""), principal
    assert une["rendu"]["exact"] is True and une["controle_negatif_rendu"]["detecte"] is True
    return {
   
… [4279 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"strict\" docs/produit/README.md tools/verifier_faq.py | head -30", "description": "Search strict in FAQ"}`

  ```
docs/produit/README.md:21:> fr/en`, `--strict`) ; la fiche du mode strict est [`rapport-evaluer-strict.md`](../../reports/rapport-evaluer-strict.md).
docs/produit/README.md:189:teste pas la cascade ; c'est le rôle de `--strict`.
docs/produit/README.md:221:**Le mode strict — `--strict`.** Le banc de recherche mesure quatre modes et un plancher ; le CLI
docs/produit/README.md:225:python3 tools/drave.py evaluer --strict
docs/produit/README.md:228:drave 0.1.0 — évaluation stricte (cascade locale, plancher 0.70)
docs/produit/README.md:259:`strict`, `plancher`, `modes`, `delta`, `verdict` et `controle_negatif` ; le test
docs/produit/README.md:260:[`test_evaluer_strict.py`](../../tools/tests/test_evaluer_strict.py) vérifie aussi qu'un
docs/produit/README.md:261:verdict faux fait sortir `cmd_evaluer` en **1**. `--strict` est **exclusif** avec `--gold`
docs/produit/README.md:264:[`rapport-evaluer-strict.md`](../../reports/rapport-evaluer-strict.md).
docs/produit/README.md:456:**surface est exacte** ; le **miroir strict** est le minimum des fidélités surface/mots/POS, et
docs/produit/README.md:459:surfaces exactes**, miroir strict **0,1087**, contrôle négatif **46/46**. C'est un **codec de
d
… [1851 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"fantôme\\|fantomes\\|options\" docs/produit/README.md | head -30", "description": "Find FAQ phantom mention"}`

  ```
262:(le gold gelé), `--tagger` (l'API) et `--par-langue` : ces options sortent en **5** plutôt
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_faq.py", "limit": 18, "offset": 312}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_faq.py</path>
<type>file</type>
<content>
312:     """Les limites nommées : pas de génération, de serveur, de local, ni d'options fantômes."""
313:     aide = _run(["--aide"])
314:     assert aide.returncode == 0
315:     for commande in ("analyser", "evaluer", "rejouer", "restituer"):
316:         assert commande in aide.stdout, commande
317:     for fantome in ("--sortie", "--mode", "--strict"):
318:         assert fantome not in aide.stdout, fantome
319:         r = _run(["analyser", "Le chat dort.", fantome])
320:         assert r.returncode == 5, (fantome, r.returncode)
321: 
322:     source = DRAVE.read_text(encoding="utf-8")
323:     for interdit in ("http.server", "transformers", "torch", "sys.stdin"):
324:         assert interdit not in source, interdit
325: 
326:     # Les rôles sont normalisés par une table unique et un vocabulaire fermé.
327:     try:
328:         from roles_vocabulaire import CORRESPONDANCES, ROLES, normaliser_role
329:     except ImportError:

(Showing lines 312-329 of 509. Use offset=330 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_faq.py", "new_string": "    for fantome in (\"--sortie\", \"--mode\"):\n        assert fantome not in aide.stdout, fantome\n        r = _run([\"analyser\", \"Le chat dort.\", fantome])\n        assert r.returncode == 5, (f … [405 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_faq.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_faq.py", "new_string": "        \"options_fantomes\": {\"--sortie\": \"code 5\", \"--mode\": \"code 5\"},", "old_string": "        \"options_fantomes\": {\"--sortie\": \"code 5\", \"--mode\": \"code 5\", \"--strict\": \"co … [10 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_faq.py has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/verifier_faq.py 2>&1 | tail -20; echo \"PIPE=${PIPESTATUS[0]}\"", "description": "Run FAQ verifier", "timeoutMs": 300000}`

  ```
FAQ produit — 10/10 réponses vérifiées · contrôle négatif détecté
  ✅  1. Quelles langues le produit reconnaît-il ?
  ✅  2. Est-ce que ça marche hors ligne ?
  ✅  3. Combien ça coûte ?
  ✅  4. Qu'est-ce que --tagger change ?
  ✅  5. Quel est le format de sortie, et est-il stable ?
  ✅  6. Que veut dire « attachement », et à quel point est-il fiable ?
  ✅  7. Pourquoi reste-t-il un span inatteignable ?
  ✅  8. Que peut-on restituer : la surface, la forme, les rôles ?
  ✅  9. Quelles limites faut-il connaître avant de s'en servir ?
  ✅ 10. Comment l'installer et le lancer ?
✅ FAQ vérifiée
PIPE=0
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 6, "offset": 1}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
1: # En ce moment
2: 
3: **Mis à jour : 2026-11-16, 02 h 15 HNE (U3 : les profils de langue)**
4: 
5: > **État courant, pas histoire** : une sous-section par session active ; preuves et plan plus bas (**La carte**).
6: 

(Showing lines 1-6 of 143. Use offset=7 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**Mis à jour : 2026-11-16 (V1 : `evaluer --strict`, la cascade locale et le plancher 0,70)**", "old_string": "**Mis à jour : 2026-11-16, 02 h 15 HNE (U3 : les profils de langue)**"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 14, "offset": 49}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
49: - **Ce qu'elle fait** : **session close** ; **`/paragraphes`** v7, **`/`** ancien arbre (369) ; **`s/v7`** à fusionner.
50: - **Ce que font les autres** : **hub**, **N2**, **Pensée**.
51: - **Prochaine action** : **migration `/` v7** (106/41) ; référents ; rétro-traduction.
52: - **Bloquants** : aucun ; 8765 pris (lancer 9000) ; migration = choix.
53: - **Journal** : [la session](../../journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/).
54: 
55: ### Session `e181ce02-cd50-488a-a6be-e84b79d40dcc` — Pensée, la RSN plurielle et le moteur N3 *(actif)*
56: 
57: - **Id** : `e181ce02-cd50-488a-a6be-e84b79d40dcc` — [`plan.md`](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md).
58: - **Rôle** : **Pensée** — RSN, arbre d'états, N3 ; heuristique ; bloc linguistique.
59: - **Plan** : B13 · **Stratégie** : v0 · **Ambition** : tracé · **Objectif final** : moteur v0.
60: - **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**.
61: - **Ce que font les autres** : N2.
62: - **Ce qu'elle fait** : **W5** restitution v3 (gold S **144/144**, v2 **20/46**) ; *
… [378 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 8, "offset": 63}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
63: - **Prochaine action** : **J4** ; T132/T133 ; la décision `auto`.
64: - **Bloquants** : 7B locales interdites (règle 11) ; **gold de pensée**.
65: - **Journal** : [la session](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/).
66: 
67: ### Session `0733c5bb-f90b-4f58-9241-3364fa32e46c` — N2 : la production et la capacité *(en pause)*
68: 
69: - **Id** : `0733c5bb-f90b-4f58-9241-3364fa32e46c` — [`plan.md`](../../journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/plan.md).
70: - **Rôle** : **N2** — la production et la capacité.

(Showing lines 63-70 of 143. Use offset=71 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Ce qu'elle fait** : **W5** restitution v3 (gold S **144/144**, v2 **20/46**) ; **U1** O(k²) : **4,0 → 0,82 s**, α **1,53 → 1,08** ([fiche](../../reports/rapport-performance-fix.md)) ; **U2** … [827 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 8, "offset": 80}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
80: 
81: ## Ce qui est en cours
82: 
83: - **S — les structures** : 61/61 types, 144/144 rôles ; **19/19 verdicts `389b99f`** ; [v2](../../reports/rapport-coordination-s-v2.md).
84: - **N2 — en pause** : commande **`eval_longueurs.py --rope --val <dir>`** (**2,7856**) ; **jamais `--rope` seul** (**40,0658**) ; [v2 : 3,09 tenu](../../reports/rapport-coordination-n2-v2.md) ; puis **porte propre (0,29)**.
85: - **Pensée — B13 (actif)** : **183/183** ; **v2** **19/46** (F1 **0,5270**), **W5 — v3** **20/46** (F1 **0,5406**), gold S **144/144** ; **U2 — la roue** (autonome, gold dedans, roue sans gold → 4) ; **U3** profils 20/20 ; [v2](../../reports/rapport-restitution-v2.md), [v3](../../reports/rapport-restitution-v3.md), [roue](../../reports/rapport-roue.md), [profils](../../reports/rapport-profils.md).
86: - **L — le bloc langue** : contrat ; frontière script 1,0 / langue 0,137/0,9687 ; fusion réparée **0,9309/0,8226/0,8784/0,9954**.
87: - **W2/W3 — le tagger** : 402 **0,9198 → 0,9643** (+4,45), H50 **0,6842 → 0,8607** (+17,65) ; défaut **code 0 / 0 socket** ; `--tagger` 
… [179 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Pensée — B13 (actif)** : **183/183** ; **v2** **19/46** (F1 **0,5270**), **W5 — v3** **20/46** (F1 **0,5406**), gold S **144/144** ; **U2 — la roue** (autonome, gold dedans, roue sans gold → … [780 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 4, "offset": 112}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
112: | **A — le moteur** | **A2.6** | A3.4 Colab ; A5.4 FPGA ; **A6.2 libre** (MoE 18,56 Go, PPL 37,2013 ; résidence 16 GiB) | **A2.6** (experts et tête) ; **A6.2** rapport + A8.3b2 |
113: | **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, F1 0,7902, 238/239, schéma v2, restit v1, produit T1–T6 ; U1 : α 1,08, 10 000 mots 0,82 s ; U2 : roue 1 727 201 o, mêmes JSON, sans gold → evaluer 4 ; U3 : profils 398 langues, 20/20, ambigu und** | **`g017` tranché** ; **J4** ; T132/T133, **[gold 452](../../reports/rapport-gold-452.md)** ; **B10.3 bloquée** |
114: | **N — le natif** | **N2, N4** | N2 : **1 024 — 2,3911 / 2,3522** ; porte 2,7856 ; **[v2](../../reports/rapport-coordination-n2-v2.md)** ; N3 couvert ; N4 0/4 ; N5 gelé | **les runs N2** ; puis la **porte propre** ; **N4** |
115: | **R — le lecteur** | **R0.7** | **R0.7 — tagger 612 0,9575, réel 452 0,9500 ; W2 : 402 0,9643, H50 0,8607 ; W3 : défaut hors ligne, clé invalide 4, 1 000 phrases = 143 870 tokens / 0,031 $ hors pointe ; X3 : lot 1 000, 672 appels, 99 971 tokens, 0,021
… [809 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, F1 0,7902, 238/239, schéma v2, restit v1, produit T1–T6 ; U1 : α 1,08, 10 000 mots 0,82 s ; U2 : ro … [715 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 5, "offset": 122}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
122: 
123: **T1–T6 — livré** ; **U1 — les deux O(k²) bornés** (α 1,08, 10 000 mots 0,82 s) ; **U2 — la roue** (1 727 201 o, sans gold → 4) ; **U3** profils 20/20 ; [bilan](../../reports/rapport-bilan-exploitable.md), [U1](../../reports/rapport-performance-fix.md), [U2](../../reports/rapport-roue.md), [U3](../../reports/rapport-profils.md).
124: 
125: **Pensée** — `g017`, T132/T133, gold de pensée ; **J4 — l'or de rôles** (seconds cadres). **Le gold de S** (61 phrases/144 rôles) n'est pas un or humain indépendant ; **S** — page `/` : décision et recette (106/41), **12/28** référents faux.
126: 

(Showing lines 122-126 of 143. Use offset=127 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**T1–T6 — livré** ; **U1 — les deux O(k²) bornés** (α 1,08, 10 000 mots 0,82 s) ; **U2 — la roue** (1 727 201 o, sans gold → 4) ; **U3** profils 20/20 ; **V1 — `evaluer --strict`** (quatre modes … [632 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "limit": 18, "offset": 168}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md</path>
<type>file</type>
<content>
168: [JSON](../../reports/performance-fix.json) · [contrôle](../../tools/verifier_performance_fix.py).
169: **U2 — la roue (16/11)** : **1 727 201 o** ; sans gold, `evaluer` **4**
170: ([fiche](../../reports/rapport-roue.md)).
171: 
172: **U3** : **398 profils UDHR** ; **20/20**, **433/447** ; ambigu **`und`**
173: ([fiche](../../reports/rapport-profils.md)).
174: 
175: **T6 — le bilan exploitable (15/11, 23 h 35).** Cinq briques : installation éditable,
176: quickstart 3/3, API (2 139 objets, 8 rôles), performance (10 000 mots 4,01 s, 126 Mio), CLI
177: 20/20. Trois limites : clone public 88,70 % d'attachement au lieu de 99,58 %, O(k²) (α = 1,55),
178: gold de S non humain. [Fiche](../../reports/rapport-bilan-exploitable.md) ·
179: [JSON](../../reports/rapport-bilan-exploitable.json). **U1 livré** ; restent **J4**, **Panini** et `auto`.
180: 
181: **La vue d'ensemble** est dans [`chantiers.md`](chantiers.md) ; carte,
182: [`chantiers-vision.svg`](../schemas/chantiers-vision.svg) ; plan,
183: [`plan-travail.md`](plan-travail.md).
184: 
185: ## L'ordre du jour (carpe die
… [74 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "new_string": "**U3** : **398 profils UDHR** ; **20/20**, **433/447** ; ambigu **`und`**\n([fiche](../../reports/rapport-profils.md)).\n\n**V1 — `evaluer --strict` (16/11).** Le CLI mesure les **quatre modes lo … [700 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **bash** `{"command": "grep -n \"U1 — les deux O(k²)\" docs/pilotage/roadmap.md | head", "description": "Find B13 row U1 text"}`

  ```
31:| **B — l'intelligence** | langue, pensée, jeux, maîtres, [banc externe](../theorie/glossaire/entrees/banc-externe.md), sémantique, modules | ✅ B1–B12 ; **B1.5 [corpus](../theorie/glossaire/entrees/corpus.md)**, **B12.10, B10.2bis et B11.10 closes** ; le **décodeur** est levé (objectif mot : 32,5 ; JW 26,7), le `z` reste ; **B13** (moteur de pensée) : state store v0 + **AC-3/alpha-bêta** + **[DRVF](../theorie/glossaire/entrees/drvf.md) `thought`** + **[banc](../theorie/glossaire/entrees/banc.md) anytime** + **opérateurs hétérogènes** + **nécessaire** + **labyrinthe** + **[porte](../theorie/glossaire/entrees/porte.md)** + **apprise** + **courbe** + **seule** + **stochastique** + **sto seule** + **ferme** + **minute** + **minute apprise** + **minute seule** + **minute entraînée** + **shaping** + **réseau** + **MLP** + **[professeur](../theorie/glossaire/entrees/professeur.md)** + **sans None** + **correction** + **audit** + **ouverte** + **graines** + **mobile** + **mobile graines** + **bruit** + **bouge** + **bouge graines** + **période** + **phase** + **phase graines** + **aléatoire** + **hasard** + **partielle** + **croyance** + **curiosité** + **observatrice** + **bruitée** + 
… [2065 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "new_string": "**U1 — les deux O(k²) bornés** (α **1,08**, 10 000 mots **0,82 s**, sorties identiques, [fiche](../../reports/rapport-performance-fix.md)) ; **V1 — `evaluer --strict`** (quatre modes locaux, casc … [279 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **bash** `{"command": "grep -n \"rapport-profils\\|rapport-bilan-exploitable\" reports/README.md", "description": "Find rows in reports README"}`

  ```
42:| [`rapport-bilan-exploitable.md`](rapport-bilan-exploitable.md) | **T6/B13** — le bilan exploitable : installable, quickstart **3/3**, JSON v2 (**2 139** objets, **8** rôles), 10 000 mots **4,01 s**, CLI **20/20** ; trois limites nommées (clone public, O(k²), or de S), passe **85/81/4** lue |
43:| [`rapport-profils.md`](rapport-profils.md) | **U3/B13** — `drave profils` : les **398 profils UDHR** exposés, **20/20** sur l'échantillon, ambigu **`und`**, artefact de 802 110 o dans la roue |
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md", "new_string": "| [`rapport-profils.md`](rapport-profils.md) | **U3/B13** — `drave profils` : les **398 profils UDHR** exposés, **20/20** sur l'échantillon, ambigu **`und`**, artefact de 802 110 o dans la roue |\n| [`r … [443 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md": file has not been read — read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md", "limit": 5, "offset": 41}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md</path>
<type>file</type>
<content>
41: | [`rapport-semaine-2.md`](rapport-semaine-2.md) | **W6** — la semaine 2 : W1-W5, le tagger, Panini bloqué, la restitution v3 |
42: | [`rapport-bilan-exploitable.md`](rapport-bilan-exploitable.md) | **T6/B13** — le bilan exploitable : installable, quickstart **3/3**, JSON v2 (**2 139** objets, **8** rôles), 10 000 mots **4,01 s**, CLI **20/20** ; trois limites nommées (clone public, O(k²), or de S), passe **85/81/4** lue |
43: | [`rapport-profils.md`](rapport-profils.md) | **U3/B13** — `drave profils` : les **398 profils UDHR** exposés, **20/20** sur l'échantillon, ambigu **`und`**, artefact de 802 110 o dans la roue |
44: | [`rapport-passe-honnetete.md`](rapport-passe-honnetete.md) | **J9.1** — la passe d'honnêteté : **19** fiches |
45: | [`rapport-coordination-n2.md`](rapport-coordination-n2.md) | **N2** — le mètre RoPE : 8,0225 → |

(Showing lines 41-45 of 232. Use offset=46 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md", "new_string": "| [`rapport-profils.md`](rapport-profils.md) | **U3/B13** — `drave profils` : les **398 profils UDHR** exposés, **20/20** sur l'échantillon, ambigu **`und`**, artefact de 802 110 o dans la roue |\n| [`r … [443 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/index_reports.py 2>&1 | tail -20; echo \"EXIT=${PIPESTATUS[0]}\"; git diff --stat reports/INDEX.md", "description": "Regenerate reports index", "timeoutMs": 120000}`

  ```
766 fiches → reports/INDEX.md
EXIT=0
 reports/INDEX.md | 4 +++-
 1 file changed, 3 insertions(+), 1 deletion(-)
  ```

- **bash** `{"command": "git diff -- reports/INDEX.md | head -40 && grep -n \"rapport-evaluer-strict\" reports/INDEX.md", "description": "Inspect index diff"}`

  ```
diff --git a/reports/INDEX.md b/reports/INDEX.md
index 7035466f..8420ddad 100644
--- a/reports/INDEX.md
+++ b/reports/INDEX.md
@@ -1,6 +1,6 @@
 # Index des fiches de reports/
 
-> **Généré** par `tools/index_reports.py` — **764 fiches**. Les fichiers
+> **Généré** par `tools/index_reports.py` — **766 fiches**. Les fichiers
 > d'infrastructure (`README.md`, `INDEX.md`, `historique-*`) sont exclus du tableau ;
 > la page d'état, elle, compte tous les `.md` de `reports/`.
 
@@ -185,6 +185,7 @@
 | [rapport-etat-r.md](rapport-etat-r.md) | État du chantier R — le lecteur : le tagger n'est pas à 0,944 contre 0,85, R1.2-1024 est mesuré, R4.4 attend la vérité humaine |
 | [rapport-etat-s.md](rapport-etat-s.md) | S — 9/9 paragraphes jugés (19/19), 150 verdicts de banque ; la page `/` sert encore l'ancien arbre plat et la rétro-traduction n'existe pas |
 | [rapport-evaluer-langue.md](rapport-evaluer-langue.md) | J11.2 — la mesure par langue : l'anglais devant, mais le gold n'est pas le même |
+| [rapport-evaluer-strict.md](rapport-evaluer-strict.md) | V1 — `evaluer --strict` : les quatre modes locaux, la cascade à 86,25 % / 88,91 %, le plancher 0,70 qui mord |
 | [rapport-execution-v41.md](ra
… [1629 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"evaluer --strict\\|--strict\\|cascade locale\\|plancher 0,70\\|plancher 0.70\" README.md docs reports/rapport-bilan-exploitable.md docs/pilotage/references-non-regression.md | head -60", "description": "Search strict references outside changed docs"}`

  ```
docs/pilotage/plan-travail.md:127:| `python3 tools/sessions.py --check --strict` | plans complets, états connus, heartbeats < 45 min (hors `en pause`), **périmètres et fichiers réservés qui se recouvrent**, sessions de l'état sans plan | avant d'ouvrir une session, et au checkpoint |
docs/pilotage/plan-travail.md:158:2. **Vérifier** : `sessions.py --check --strict` (aucun recouvrement), `surveille_sessions.py` (les
docs/pilotage/plan-travail.md:181:| vérifier les mandats | `python3 tools/sessions.py --check --strict` |
docs/pilotage/plan-travail.md:324:- Une **porte** `porte-ressources.sh` (`--check --strict`) pourra être ajoutée après validation :
docs/pilotage/en-cours.md:3:**Mis à jour : 2026-11-16 (V1 : `evaluer --strict`, la cascade locale et le plancher 0,70)**
docs/pilotage/en-cours.md:62:- **Ce qu'elle fait** : **W5** restitution v3 (gold S **144/144**, v2 **20/46**) ; **U1** O(k²) : **4,0 → 0,82 s**, α **1,53 → 1,08** ([fiche](../../reports/rapport-performance-fix.md)) ; **U2** la roue : **1 727 201 o**, mêmes JSON hors dépôt, sans gold → **4** ([fiche](../../reports/rapport-roue.md)) ; **U3** profils **20/20**, ambigu **`und`** ([fiche](../../reports/rapport-profils.md)) 
… [7107 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"cascade\\|strict\" reports/rapport-bilan-exploitable.md | head -30", "description": "Check T6 report for contradictions"}`

  ```
(no output)
  ```

- **bash** `{"command": "python3 tools/tests/test_evaluer_strict.py && python3 tools/tests/test_produit.py", "description": "Run strict and product tests", "timeoutMs": 300000}`

  ```
[stderr]
.....
----------------------------------------------------------------------
Ran 5 tests in 10.755s

OK
..............................
----------------------------------------------------------------------
Ran 30 tests in 17.353s

OK
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -80; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Run documentation review", "timeoutMs": 300000}`

  ```
revue de documentation · 769 fiche(s) · 864 JSON · 125 doc(s) · 86 porte(s) · 8 chapitre(s)
  ❌ 2 anomalie(s) :
     · compteurs : en-cours.md dit 768 fichiers, le disque en a 769
     · compteurs : en-cours.md dit 863 JSON, le disque en a 864
EXIT=1
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 6, "offset": 96}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
96: 
97: | invariant | valeur | contrôle |
98: |---|---|---|
99: | portes | **86** (dont `porte-banc-performance` le 15/11) | `tools/porte-*.sh` |
100: | chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
101: | fichiers / JSON de résultats | **768** / **863** | `reports/*.md` / `reports/*.json` |

(Showing lines 96-101 of 143. Use offset=102 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "| fichiers / JSON de résultats | **769** / **864** | `reports/*.md` / `reports/*.json` |", "old_string": "| fichiers / JSON de résultats | **768** / **863** | `reports/*.md` / `reports/*.json` | … [2 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -40; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Re-run documentation review", "timeoutMs": 300000}`

  ```
revue de documentation · 769 fiche(s) · 864 JSON · 125 doc(s) · 86 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
EXIT=0
  ```

- **bash** `{"command": "python3 tools/verifie_en_cours.py; echo \"EXIT=$?\"", "description": "Verify en-cours structure", "timeoutMs": 120000}`

  ```
en-cours · 1697 mots · 7 sections · 4 session(s) · 9 puces · 3 questions
  ✅ état court, structuré, multi-session et reprenable
EXIT=0
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -30; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Check doc size budget", "timeoutMs": 120000}`

  ```
budget de contexte · documents chargeables
    mots lignes  cat budget  document
    9075    520   T1   9000  docs/pilotage/roadmap.md
    5999    597 DATÉ      0  docs/implantation/contexte-long.md
    4858    515   T1   5000  docs/theorie/glossaire/10-le-pont-linguistico-semantique-le-vocabu.md
    4085    431 DATÉ      0  docs/implantation/numa-segregation.md
    3310    317   T1   3500  README.md
    3072    341 DATÉ      0  docs/implantation/convertisseur.md
    2962    364   T1   5000  docs/theorie/glossaire/02-modeles-et-architectures.md
    2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2829    234   T1   2800  reports/README.md
    2433    164   T1   2500  docs/pilotage/references-non-regression.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/form
… [645 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/verifie_journal.py 2>&1 | tail -30; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Verify journal", "timeoutMs": 120000}`

  ```
journal · 48 jour(s) · 226 session(s) · 2719 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
EXIT=0
  ```

- **bash** `{"command": "python3 tools/verifier_schemas.py 2>&1 | tail -20; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Verify schemas", "timeoutMs": 120000}`

  ```
schémas · 465 document(s) · 67 SVG · 2 source(s)
  ✅ aucun ASCII art, SVG valides et référencés, blocs PlantUML inline valides,
     sources et images relatives.
EXIT=0
  ```

- **bash** `{"command": "wc -w AGENTS.md docs/pilotage/en-cours.md docs/pilotage/roadmap.md reports/README.md docs/produit/README.md reports/rapport-evaluer-strict.md", "description": "Word counts"}`

  ```
1196 AGENTS.md
  1697 docs/pilotage/en-cours.md
  9401 docs/pilotage/roadmap.md
  2829 reports/README.md
 10396 docs/produit/README.md
  1274 reports/rapport-evaluer-strict.md
 26793 total
  ```

- **bash** `{"command": "grep -n \"T0\\|budget\\|roadmap\\|reports/README\" tools/taille_documents.py | head -40", "description": "Inspect budget tool"}`

  ```
2:"""taille_documents.py — le budget de contexte et la cohésion des documents.
5:  1. la taille des documents **chargeables** (T0/T1) en mots, avec un budget par catégorie ;
11:Les fiches de `reports/` (sauf `reports/README.md`) et le `journal/` sont **hors budget** :
12:ils ne sont pas chargés automatiquement. Le budget est en **mots** ; l'estimation de tokens
16:elles ne comptent pas dans le budget ; le document les porte, la page montre le SVG.
25:# (catégorie, budget en mots). Les globs sont résolus dans l'ordre ; le premier match gagne.
27:    ("T0", "AGENTS.md", 1200),
28:    ("T0", "docs/pilotage/en-cours.md", 2000),
32:    ("T0", "docs/methode/*.md", 1200),
37:    ("T1", "docs/pilotage/roadmap.md", 9000),
44:    ("T1", "reports/README.md", 2800),
77:#: pas dans le budget de contexte. Le rendu (docwatch) est ce que voit le lecteur ;
90:    for cat, motif, budget in BUDGETS:
92:            return cat, budget
101:    for cat, motif, budget in BUDGETS:
110:            lignes.append((n, t.count("\n") + 1, rel, cat, budget))
112:            if cat in ("T0", "T1"):
122:            if budget and n > budget:
123:                violations.append(f"{rel} : {n} mots > budget {budget} 
… [959 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**Mis à jour : 2026-11-16 (V1 : `evaluer --strict`)**", "old_string": "**Mis à jour : 2026-11-16 (V1 : `evaluer --strict`, la cascade locale et le plancher 0,70)**"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Ce qu'elle fait** : **W5** restitution v3 (gold S **144/144**, v2 **20/46**) ; **U1** O(k²) : **4,0 → 0,82 s**, α **1,53 → 1,08** ([fiche](../../reports/rapport-performance-fix.md)) ; **U2** … [976 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Pensée — B13 (actif)** : **183/183** ; **v2** **19/46** (F1 **0,5270**), **W5 — v3** **20/46** (F1 **0,5406**), gold S **144/144** ; **U2 — la roue** (autonome, gold dedans, roue sans gold → … [780 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, F1 0,7902, 238/239, schéma v2, restit v1, produit T1–T6 ; U1 : α 1,08, 10 000 mots 0,82 s ; U2 : ro … [715 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**T1–T6 — livré** ; **U1 — les deux O(k²) bornés** (α 1,08, 10 000 mots 0,82 s) ; **U2 — la roue** (1 727 201 o, sans gold → 4) ; **U3** profils 20/20 ; [bilan](../../reports/rapport-bilan-explo … [632 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -12; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Recheck doc budgets", "timeoutMs": 120000}`

  ```
1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4009 mots (budget 4 000)

  avertissements :
     · 65 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 3 violation(s) :
     · docs/pilotage/roadmap.md : 9075 mots > budget 9000 (T1)
     · reports/README.md : 2829 mots > budget 2800 (T1)
     · T0 : 4009 mots (AGENTS + en-cours + une tâche) > budget 4 000
EXIT=1
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Ce qu'elle fait** : **W5** restitution v3 (gold S **144/144**, v2 **20/46**) ; **U1** O(k²) : **4,0 → 0,82 s**, α **1,53 → 1,08** ([fiche](../../reports/rapport-performance-fix.md)) ; **U2** … [877 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "new_string": "**U1 — les deux O(k²) bornés** (α **1,08**, 10 000 mots **0,82 s**, sorties identiques, [fiche](../../reports/rapport-performance-fix.md)) |", "old_string": "**U1 — les deux O(k²) bornés** (α **1 … [279 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "new_string": "**V1 — `evaluer --strict` (16/11).** Quatre modes locaux sur **612** et **452** ; cascade POS\n**0,8625** / **0,8891**, plancher **0,70**, code **0** ; négatif **0,0000** → **1**.\n[Fiche](../../ … [554 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "new_string": "**T6 — le bilan exploitable (15/11, 23 h 35).** Cinq briques (installation éditable, quickstart\n3/3, JSON **2 139** objets / **8** rôles, 10 000 mots **4,01 s**, CLI **20/20**) ; trois limites\n … [681 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -12; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Recheck budgets", "timeoutMs": 120000}`

  ```
1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4004 mots (budget 4 000)

  avertissements :
     · 65 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 3 violation(s) :
     · docs/pilotage/roadmap.md : 9015 mots > budget 9000 (T1)
     · reports/README.md : 2829 mots > budget 2800 (T1)
     · T0 : 4004 mots (AGENTS + en-cours + une tâche) > budget 4 000
EXIT=1
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**Mis à jour : 2026-11-16 (`evaluer --strict`)**", "old_string": "**Mis à jour : 2026-11-16 (V1 : `evaluer --strict`)**"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Ce qu'elle fait** : **W5** restitution v3 (gold S **144/144**, v2 **20/46**) ; **U1** O(k²) : **4,0 → 0,82 s**, α **1,53 → 1,08** ([fiche](../../reports/rapport-performance-fix.md)) ; **U2** … [825 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "new_string": "**V1 — `evaluer --strict` (16/11).** Quatre modes, cascade **0,8625** / **0,8891**, plancher\n**0,70** ; négatif **0,0000** → **1**. [Fiche](../../reports/rapport-evaluer-strict.md) ·\n[JSON](../ … [984 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md", "new_string": "| [`rapport-evaluer-strict.md`](rapport-evaluer-strict.md) | **V1** — `--strict` : cascade **0,8625** / **0,8891**, plancher **0,70**, négatif **1** |", "old_string": "| [`rapport-evaluer-strict.md`](ra … [201 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -12; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Recheck budgets", "timeoutMs": 120000}`

  ```
1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4000 mots (budget 4 000)

  avertissements :
     · 65 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 1 violation(s) :
     · reports/README.md : 2816 mots > budget 2800 (T1)
EXIT=1
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md", "new_string": "| [`rapport-bilan-exploitable.md`](rapport-bilan-exploitable.md) | **T6/B13** — installable, quickstart **3/3**, JSON v2 (**2 139** objets, **8** rôles), 10 000 mots **4,01 s**, CLI **20/20** ; trois li … [340 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md", "new_string": "| [`rapport-evaluer-strict.md`](rapport-evaluer-strict.md) | **V1** — `--strict` : cascade **0,8625** / **0,8891**, plancher **0,70** |", "old_string": "| [`rapport-evaluer-strict.md`](rapport-evaluer-s … [103 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -8; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Recheck budgets", "timeoutMs": 120000}`

  ```
1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4000 mots (budget 4 000)

  avertissements :
     · 65 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 1 violation(s) :
     · reports/README.md : 2802 mots > budget 2800 (T1)
EXIT=1
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md", "new_string": "| [`rapport-evaluer-strict.md`](rapport-evaluer-strict.md) | **V1** — `--strict` : cascade **0,8625/0,8891**, plancher **0,70** |", "old_string": "| [`rapport-evaluer-strict.md`](rapport-evaluer-strict. … [82 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -8; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Recheck budgets", "timeoutMs": 120000}`

  ```
1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4000 mots (budget 4 000)

  avertissements :
     · 65 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
EXIT=0
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -20; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Re-run documentation review", "timeoutMs": 300000}`

  ```
revue de documentation · 769 fiche(s) · 864 JSON · 125 doc(s) · 86 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
EXIT=0
  ```

- **bash** `{"command": "python3 tools/tests/test_verifier_faq.py 2>&1 | tail -30; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Run FAQ tests", "timeoutMs": 300000}`

  ```
python3: can't open file '/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_verifier_faq.py': [Errno 2] No such file or directory
EXIT=2
  ```

- **bash** `{"command": "bash tools/porte-tableaux.sh 2>&1 | tail -30; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Run table gate", "timeoutMs": 300000}`

  ```
✅ 1850 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4775 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-16)
EXIT=0
  ```

- **bash** `{"command": "python3 tools/verifie_en_cours.py && python3 tools/verifie_journal.py >/dev/null && echo OK", "description": "Verify state and journal", "timeoutMs": 120000}`

  ```
en-cours · 1630 mots · 7 sections · 4 session(s) · 9 puces · 3 questions
  ✅ état court, structuré, multi-session et reprenable
OK
  ```

- **bash** `{"command": "bash tools/porte-produit.sh 2>&1 | tail -40; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Run product gate", "timeoutMs": 600000}`

  ```
✅ version : drave 0.1.0
  ✅ analyser fr : JSON valide, étiquettes et syntagmes
  ✅ analyser en : JSON valide, étiquettes et syntagmes
  ✅ profils : langue, script, confiance, 398 profils
  ✅ rejeu : sha256 f6355d8175a75854 deux fois
  ✅ smoke test : Ran 30 tests
  ✅ evaluer --strict : Ran 5 tests
  ✅ schéma v2 validé (5 cas v2 + 1 cas v1 + 20 phrases du gold)
  ✅ 50 textes libres : Ran 4 tests
  ✅ restitution v0 : surface exacte (miroir affiché)
  ✅ restitution v1 : forme canonique exacte, miroir strict distinct
  ✅ restitution v2 : rôles lisibles, rendu relu, contrôle détecté
  ✅ restitution v0/v1 : Ran 22 tests
  ✅ restitution v2 : Ran 17 tests
  ✅ schéma v2 : Ran 9 tests
  ✅ refus : JSON avec refus, code 3
  ✅ autotest parallèle : 183/183 portes tenues
✅ porte produit verte
EXIT=0
  ```

- **bash** `{"command": "bash tools/porte-bloc-linguistique.sh 2>&1 | tail -20; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Run block gate", "timeoutMs": 600000}`

  ```
"ponctuation_refus": "vide",
  "langue_inconnue": "und",
  "indice_faux": "und",
  "rejeu_identique": true
 },
 "verdicts": {
  "langue": true,
  "script": true,
  "permute_faible": true,
  "niveaux": true,
  "substitution": true,
  "parallele": true,
  "activation": true,
  "vide": true,
  "inconnue": true,
  "rejeu": true
 },
 "ok": true
}
✅ porte bloc linguistique verte
EXIT=0
  ```

- **bash** `{"command": "python3 tools/drave.py evaluer --strict --json > /tmp/evaluer-strict-2.json && cmp reports/evaluer-strict.json /tmp/evaluer-strict-2.json && echo \"JSON identique\" && sha256sum reports/evaluer-strict.json", "description": "Check strict JSON determinism", "timeoutMs": 300000}`

  ```
JSON identique
678a414763eff4716c47fb70057458534e247b6fb22cd7dc172507c997491876  reports/evaluer-strict.json
  ```

- **bash** `{"command": "git status --short && echo '--- diff stat ---' && git diff --stat && echo '--- untracked target files ---' && ls -l reports/rapport-evaluer-strict.md reports/evaluer-strict.json tools/tests/test_evaluer_strict.py", "description": "Inspect final status"}`

  ```
M docs/implantation/bloc-linguistique.md
 M docs/pilotage/en-cours.md
 M docs/pilotage/roadmap.md
 M docs/produit/README.md
 M docs/produit/demarrage.md
 M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
 M pyproject.toml
 M reports/INDEX.md
 M reports/README.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-bloc-linguistique.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-roue.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/plan.json
 M tools/drave.py
 M tools/porte-bloc-linguistique.sh
 M tools/porte-produit.sh
 M tools/tests/test_empaquetage.py
 M tools/tests/test_produit.py
 M tools/verifier_faq.py
?? journal/sessions/session-9e0eeeb8-7572-4a68-a74e-7405d06e3757/
?? reports/evaluer-strict.json
?? reports/profils.json
?? reports/rapport-evaluer-strict.md
?? reports/rapport-profils.md
?? reports/rapport-s-paragraphes.md
?? tools/construir
… [2381 caractères tronqués]
  ```

- **bash** `{"command": "ls journal | tail -20 && ls journal/2026-11-16 2>/dev/null || true && sed -n '1,120p' journal/README.md", "description": "Inspect journal structure"}`

  ```
2026-10-26
2026-10-27
2026-10-28
2026-10-29
2026-10-30
2026-10-31
2026-11-01
2026-11-02
2026-11-03
2026-11-04
2026-11-05
2026-11-06
2026-11-07
2026-11-13
2026-11-14
2026-11-15
2026-11-16
README.md
sessions
THEMES.md
docs.md
memoire.md
mesures.md
README.md
# Journal

Le journal consigne les **événements datés**, avec des liens vers le reste : les
**mesures** sont dans `reports/` (une fiche par expérience) et l'**état** dans
`docs/pilotage/en-cours.md` — convention : `docs/methode/organisation-du-depot.md`.
Tout horodatage est en heure locale de la machine (**HAE = EDT, UTC−4**).

**Une journée = un dossier** `journal/AAAA-MM-JJ/` : `README.md` (index), les thèmes
et les autres pièces datées. Les sessions DSH sont dans `journal/sessions/<id>/` ;
chaque rapport renvoie à son jour et à `en-cours`.

## Journées

| jour | index | thèmes |
|---|---|---|
| **2026-11-16** | [2026-11-16/README.md](2026-11-16/README.md) | [docs](2026-11-16/docs.md) · [memoire](2026-11-16/memoire.md) · [mesures](2026-11-16/mesures.md) |
| **2026-11-15** | [2026-11-15/README.md](2026-11-15/README.md) | [distribue](2026-11-15/distribue.md) · [docs](2026-11-15/docs.md) · [memoire](2026-11-15/memoire.md) · [mesure
… [23611 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"evaluer\\|--strict\" README.md | head -30", "description": "Search top-level README"}`

  ```
24:python3 tools/drave.py evaluer        # la mesure sur le gold (POS, F1, attachement)
  ```

- **bash** `{"command": "python3 -m pytest -q tools/tests/test_evaluer_strict.py tools/tests/test_produit.py 2>&1 | tail -20; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Run pytest on strict and product tests", "timeoutMs": 300000}`

  ```
...................................                                      [100%]
35 passed in 28.88s
EXIT=0
  ```

- **bash** `{"command": "git diff -- tools/drave.py tools/verifier_faq.py tools/porte-produit.sh | sed -n '1,260p'", "description": "Review code diff"}`

  ```
diff --git a/tools/drave.py b/tools/drave.py
index e5469d2f..835d22d0 100644
--- a/tools/drave.py
+++ b/tools/drave.py
@@ -1,7 +1,7 @@
 #!/usr/bin/env python3
 """drave.py — le point d'entrée produit du bloc linguistique.
 
-Une seule commande, quatre gestes, hors ligne et déterministe :
+Une seule commande, cinq gestes, hors ligne et déterministe :
 
     python3 tools/drave.py analyser "Le chat dort."
     python3 tools/drave.py analyser "The cat sleeps on the roof." --langue en --json
@@ -9,6 +9,10 @@ Une seule commande, quatre gestes, hors ligne et déterministe :
     python3 tools/drave.py analyser "Le chat dort." --tagger auto     # API si clé, sinon heuristique
     python3 tools/drave.py evaluer
     python3 tools/drave.py evaluer --gold --json
+    python3 tools/drave.py evaluer --strict --json                    # quatre modes, plancher 0,70
+    python3 tools/drave.py profils --texte "Le chat dort."
+    python3 tools/drave.py profils --texte "Привет мир" --json
+    python3 tools/drave.py analyser "Le chat dort." --profils
     python3 tools/drave.py evaluer --tagger --json                    # heuristique + cascade API
     python3 tools/drave.py rejouer "Le chat de la
… [11496 caractères tronqués]
  ```

- **bash** `{"command": "git show HEAD:tools/drave.py | grep -n \"cmd_profils\\|_HeuristiqueProfils\" | head; git show --stat HEAD | head -30", "description": "Check HEAD contents and commit stat"}`

  ```
commit 2e6170343a8f9bc35b525862cf47848b359fd375
Author: Stéphane <stephane@localhost>
Date:   Mon Nov 16 02:10:08 2026 -0500

    EXPLOITABLE — U3 : LES PROFILS DE LANGUE (LA DÉTECTION EXPOSÉE, LA MESURE SUR L'ÉCHANTILLON UDHR, LE CONTRÔLE NÉGATIF)

 journal/2026-11-16/README.md                       |    6 +-
 journal/2026-11-16/docs.md                         |   19 +
 journal/2026-11-16/memoire.md                      |    2 +-
 journal/2026-11-16/mesures.md                      |    2 +-
 journal/README.md                                  |    7 +-
 journal/THEMES.md                                  |    1 +
 journal/sessions/MANIFEST.md                       |    7 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md |  118 +
 .../rapport.md                                     |   18 +-
 .../digest.md                                      |  139 +
 .../rapport.md                                     |   14 +-
 .../digest.md                                      | 4640 ++++++++++++++++++++
 .../rapport.md                                     |  268 ++
 13 files changed, 5216 insertions(+), 25 deletions(-)
  ```

- **bash** `{"command": "grep -n \"dernière mise à jour\" docs/pilotage/roadmap.md", "description": "Find roadmap date"}`

  ```
189:L'ordre est **la valeur / le coût**, pas la date. La dernière mise à jour est le **2026-11-15 23 h 35**.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "new_string": "L'ordre est **la valeur / le coût**, pas la date. La dernière mise à jour est le **2026-11-16**.", "old_string": "L'ordre est **la valeur / le coût**, pas la date. La dernière mise à jour est le  … [25 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -6; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Final budget check", "timeoutMs": 120000}`

  ```
T0 max : 4000 mots (budget 4 000)

  avertissements :
     · 65 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
EXIT=0
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -6; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Final doc review", "timeoutMs": 300000}`

  ```
revue de documentation · 769 fiche(s) · 864 JSON · 125 doc(s) · 86 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
EXIT=0
  ```

- **bash** `{"command": "bash tools/porte-tableaux.sh 2>&1 | tail -6; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Final table gate", "timeoutMs": 300000}`

  ```
✅ 1850 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4775 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-16)
EXIT=0
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "new_string": "        for nom in (\"heuristique\", \"neuronal\", \"parallele\", \"cascade\"):\n            m = mesures[nom]\n            d = deltas.get(nom)\n            delta_pos = _points(d[\"pos\"]) if d else \"—\"\n … [1127 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **bash** `{"command": "grep -n \"parallele\" tools/tests/test_evaluer_strict.py docs/produit/README.md | head -20", "description": "Find parallele occurrences"}`

  ```
tools/tests/test_evaluer_strict.py:56:                {"heuristique", "neuronal", "parallele", "cascade"},
tools/tests/test_evaluer_strict.py:73:        for attendu in ("heuristique", "neuronal", "parallele", "cascade",
docs/produit/README.md:235:parallele      86.25 %   +0.00 pts   79.02 %   +0.00 pts   90.29 %   +0.00 pts
docs/produit/README.md:243:parallele      88.91 %   +0.00 pts   79.06 %   +0.00 pts   89.90 %   +0.00 pts
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/tests/test_evaluer_strict.py')\ns=p.read_text()\ns=s.replace('for attendu in (\"heuristique\", \"neuronal\", \"parallele\", \"cascade\",', 'for attendu in (\"heuristique\", \"neuronal\", \"parallèle\", \"cascade\",')\np.write_text( … [571 caractères tronqués]`

  ```
drave 0.1.0 — évaluation stricte (cascade locale, plancher 0.70)
gold vivant 612 phrases · 3179 tokens · gold réel 452 phrases · 2480 tokens

GOLD VIVANT 612
mode               POS        ΔPOS  SYNT. F1         ΔF1   TÊTE F1       ΔTÊTE
heuristique    86.25 %           —   79.02 %           —   90.29 %           —
neuronal       75.40 %  -10.85 pts   76.51 %   -2.51 pts   88.07 %   -2.22 pts
parallèle      86.25 %   +0.00 pts   79.02 %   +0.00 pts   90.29 %   +0.00 pts
cascade        86.25 %   +0.00 pts   79.02 %   +0.00 pts   90.29 %   +0.00 pts
cascade : 612 appels neuronaux sur 612 phrases

GOLD RÉEL 452
  ```

- **bash** `{"command": "python3 tools/tests/test_evaluer_strict.py && python3 tools/revue_documentation.py >/tmp/revue.log 2>&1; code=$?; tail -3 /tmp/revue.log; echo \"REVUE=$code\"", "description": "Re-run strict test and doc review", "timeoutMs": 300000}`

  ```
revue de documentation · 769 fiche(s) · 864 JSON · 125 doc(s) · 86 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
REVUE=0
[stderr]
.....
----------------------------------------------------------------------
Ran 5 tests in 10.820s

OK
  ```

- **bash** `{"command": "grep -n \"strict\\|evaluer\\|options\" tools/tests/test_empaquetage.py | head -40", "description": "Check empaquetage tests for strict"}`

  ```
15:- **sans gold**, `evaluer` échoue **proprement** : code 4, message qui dit quoi faire, et
150:    """Le contrôle négatif de la roue : sans gold, `evaluer` refuse de mesurer."""
152:    def test_evaluer_sans_gold_code_4(self):
162:            (dossier / "evaluer_gold.py").write_text("", encoding="utf-8")
166:                    code = drave.main(["evaluer"])
  ```

- **bash** `{"command": "sed -n '1,80p' journal/2026-11-16/mesures.md && echo '---README---' && sed -n '1,60p' journal/2026-11-16/README.md", "description": "Inspect today's journal measures"}`

  ```
# 2026-11-16 — Campagnes et mesures

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (3)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 00:19 | `d19f0fc7` | U1 — LES DEUX O(K²) BORNÉS : 10 000 MOTS 4,0 → 0,82 S (×4,9), α 1,53 → 1,08, QUADRATIQUE +0,00077 R² ; 612/452 ET 10 000 MOTS IDENTIQUES AU BIT PRÈS (DIFF VIDE), 127,4 MIO | `en-cours.md`, `roadmap.md`, `README.md` (+17) |
| 00:28 | `04894aea` | U1 — LE CONTRÔLE DE L'INSTRUMENT EST CELUI DE LA PASSE : LINÉAIRE 0,71, QUADRATIQUE 2,11 (ET NON LES VALEURS DE T4) | `en-cours.md`, `README.md`, `memoire.md` (+7) |
| 00:45 | `c77ed4b6` | U2 — LA ROUE AUTONOME : 1 727 201 OCTETS, 422 ENTRÉES, MÊMES JSON HORS DÉPÔT ; SANS GOLD `EVALUER` SORT EN 4, STDOUT VIDE | `en-cours.md`, `roadmap.md`, `README.md` (+19) |

## Chiffres du jour

`×4,9`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.
… [3553 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '16,24p' docs/produit/README.md && sed -n '219,266p' docs/produit/README.md", "description": "Review README changes"}`

  ```
> est **version 2** (`schema: "drave.annotation"`,
> `version: 2`) : le schéma v2 ajoute `meta.partition` et `meta.alternative`, et la **version 1
> reste lue** ([`tools/schemas/`](../../tools/schemas/)). Les sorties du § 3.1, du § 3.4 et du
> § 3.5 ont été relancées le 07/11 pour le format v2 ; les mesures chiffrées du § 2 datent du
> **06/11**, et l'`evaluer` du § 3.3 a été relancé le **16/11** (gold vivant 612, `--par-langue
> fr/en`, `--strict`) ; la fiche du mode strict est [`rapport-evaluer-strict.md`](../../reports/rapport-evaluer-strict.md).
> Ce qui manque encore au contrat est nommé au § 7, sans être présenté comme acquis.
> La **FAQ** (§ 8) est vérifiée à part le **2026-11-15** par
> [`tools/verifier_faq.py`](../../tools/verifier_faq.py) : **10/10** réponses.
complète est [`rapport-evaluer-langue.md`](../../reports/rapport-evaluer-langue.md).

**Le mode strict — `--strict`.** Le banc de recherche mesure quatre modes et un plancher ; le CLI
le fait maintenant en une commande, **hors ligne** (`MockNeuronal`, pas de GPU, pas de clé) :

```bash
python3 tools/drave.py evaluer --strict
```
```
drave 0.1.0 — évaluation stricte (cascade locale, plancher 0.70)
gold vivant 612 phr
… [2307 caractères tronqués]
  ```

- **bash** `{"command": "git diff --check -- tools/drave.py tools/tests/test_evaluer_strict.py tools/porte-produit.sh tools/verifier_faq.py docs/produit/README.md docs/pilotage/en-cours.md docs/pilotage/roadmap.md reports/README.md reports/INDEX.md; echo \"EXIT=$?\"", "description": "Check whitespace in diffs"}`

  ```
EXIT=0
  ```

- **bash** `{"command": "python3 -m py_compile tools/drave.py tools/tests/test_evaluer_strict.py tools/verifier_faq.py && echo OK", "description": "Compile modified Python"}`

  ```
OK
  ```

### 🤖 Assistant

## V1 — `evaluer --strict` livré

### Ce qui a été ajouté

- **`tools/drave.py`** : nouveau drapeau `--strict` sur `evaluer`.
  - mesure les **quatre modes** : heuristique, `MockNeuronal`, parallèle, cascade ;
  - sur le **gold vivant 612** et le **gold réel 452** ;
  - affiche POS, F1, tête et le **delta contre l'heuristique** ;
  - applique le **plancher 0,70** à la cascade POS sur les deux golds ;
  - sort en **code 1** si l'un des deux est sous le plancher ;
  - contrôle négatif intégré : cascade dégradée (POS forcé à `X`) → **0,0000**, `code: 1` ;
  - exclusif avec `--gold`, `--tagger`, `--par-langue` (code 5).

### Chiffres mesurés

| gold | mode | POS | F1 | tête | ΔPOS vs heuristique |
|---|---|---:|---:|---:|---:|
| **612** | heuristique | **0,8625** | 0,7902 | 0,9029 | — |
| 612 | neuronal | 0,7540 | 0,7651 | 0,8807 | −10,85 pts |
| 612 | parallèle | 0,8625 | 0,7902 | 0,9029 | +0,00 |
| 612 | **cascade** | **0,8625** | 0,7902 | 0,9029 | +0,00 |
| **452** | heuristique | **0,8891** | 0,7906 | 0,8990 | — |
| 452 | neuronal | 0,7621 | 0,7448 | 0,8697 | −12,70 pts |
| 452 | parallèle | 0,8891 | 0,7906 | 0,8990 | +0,00 |
| 452 | **cascade** | **0,8891** | 0,7906 | 0,8990 | +0,00 |

**Plancher** : cascade POS **0,8625** (612) et **0,8891** (452) → **code 0**.  
**Contrôle négatif** : cascade dégradée **0,0000** → **code 1** ; un test vérifie aussi que `cmd_evaluer` rend bien 1 quand le verdict est faux.

### Fichiers

- `tools/drave.py` — `--strict`, `PLANCHER_STRICT`, `_evaluer_strict`, `_verdict_strict`, `_formater_strict`.
- `tools/tests/test_evaluer_strict.py` — **5 tests** (quatre modes, sortie lisible, négatif code 1, options exclusives, aide).
- `tools/porte-produit.sh` — exécute le nouveau test.
- `tools/verifier_faq.py` — `--strict` n’est plus une option fantôme.
- `docs/produit/README.md` **§ 3.3** — notice du mode strict, sortie réelle, limites.
- `docs/pilotage/en-cours.md` et `docs/pilotage/roadmap.md` — état et ligne V1.
- `reports/rapport-evaluer-strict.md` — fiche complète.
- `reports/evaluer-strict.json` — rapport JSON.
- `reports/README.md` et `reports/INDEX.md` — indexation.

### Vérifications

- `tools/tests/test_evaluer_strict.py` : **5/5**.
- `pytest` strict + produit : **35 passed**.
- `tools/porte-produit.sh` : **verte**, dont `evaluer --strict : Ran 5 tests`.
- `tools/porte-bloc-linguistique.sh` : **verte**.
- `revue_documentation.py`, `taille_documents.py`, `porte-tableaux.sh`, `verifier_faq.py` (10/10), `verifie_en_cours.py`, `verifie_journal.py`, `verifier_schemas.py` : **verts**.

Je n’ai pas créé de commit : l’arbre de travail contenait déjà des modifications non liées (U3, journal) ; un `git add` global les aurait mélangées à V1. Les fichiers V1 sont en place dans l’arbre, prêts à être commités ciblé.

