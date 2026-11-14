# Session DSH — relecture

- identifiant : `session-9d3b2074-c5f0-4f11-be10-31d317bac657`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-14 04:33:44
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche J11.2 : ajouter `evaluer --par-langue` (le détail fr/en) et le documenter dans `docs/produit/README.md` ; test dans `tools/tests/test_produit.py` ; fiche `reports/rapport-evaluer-langue.md` + JSON, commit.

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

- **bash** `{"command": "pwd && git status --short && git log --oneline -5", "description": "Show working dir and git status"}`

  ```
/home/stephane/Data13TB/stephane/GitHub/Qtrinet
MM journal/2026-11-14/README.md
MM journal/2026-11-14/docs.md
MM journal/2026-11-14/memoire.md
MM journal/2026-11-14/mesures.md
MM journal/2026-11-14/portes.md
MM journal/README.md
MM journal/THEMES.md
MM journal/sessions/MANIFEST.md
MM journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
MM journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
D  journal/sessions/session-b0a87524-43a4-4935-a248-72c1d42c8471/digest.md
D  journal/sessions/session-b0a87524-43a4-4935-a248-72c1d42c8471/rapport.md
MM journal/sessions/session-ce875934-0cf6-4434-a91d-cbca647b11b3/digest.md
MM journal/sessions/session-ce875934-0cf6-4434-a91d-cbca647b11b3/rapport.md
 M reports/INDEX.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/plan.json
 m tools/structures
?? journal/sessions/session-b0a87524-43a4-4935-a248-72c1d42c8471/
?? reports/rapport-s-paragraphes.md
84e393bb J11.1 — LE
… [593 caractères tronqués]
  ```

- **bash** `{"command": "ls -la docs/produit/ tools/ reports/ 2>&1 | head -80", "description": "List key directories"}`

  ```
docs/produit/:
total 56
drwxr-xr-x. 1 stephane stephane    40 14 nov 04:20 .
drwxr-xr-x. 1 stephane stephane   138  6 nov 10:08 ..
-rw-r--r--. 1 stephane stephane 22928 14 nov 04:20 exemples.md
-rw-r--r--. 1 stephane stephane 28699 14 nov 01:57 README.md

reports/:
total 26512
drwxr-xr-x. 1 stephane stephane   75568 14 nov 04:23 .
drwxr-xr-x. 1 stephane stephane     686  6 nov 09:52 ..
drwxr-xr-x. 1 stephane stephane     102 24 oct 15:52 07
-rw-r--r--. 1 stephane stephane    4447 28 oct 09:17 07-mesures-couche-commune.md
-rw-r--r--. 1 stephane stephane     907 29 oct 16:25 a26-bilan.json
-rw-r--r--. 1 stephane stephane    1163  1 nov 20:40 a26-lot-disque.json
-rw-r--r--. 1 stephane stephane    1121 30 oct 08:57 a80-audit-final.json
-rw-r--r--. 1 stephane stephane     560 30 oct 00:04 a80-indice-qualifie.json
-rw-r--r--. 1 stephane stephane     672 29 oct 23:42 a80-melange-qualifie.json
-rw-r--r--. 1 stephane stephane     430 30 oct 08:57 a80-pannes-ppl.json
-rw-r--r--. 1 stephane stephane     630 29 oct 17:07 a80-porte-adaptateur.json
-rw-r--r--. 1 stephane stephane     521 29 oct 16:40 a80-porte-budget.json
-rw-r--r--. 1 stephane stephane     625 29 oct 22:07 a80-porte-bus.json
-r
… [4243 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"evaluer\" --include=\"*.py\" tools/ | head -40; echo \"---\"; find tools -iname \"*produit*\" -o -iname \"*evaluer*\" | head -40", "description": "Find evaluer/produit files"}`

  ```
tools/essai_decharge.py:375:def evaluer(modele, ids, seq, lot, rap=None, max_lots=20):
tools/essai_decharge.py:461:                bpc = evaluer(modele, val, a.seq, a.lot)
tools/essai_decharge.py:472:        bpc = evaluer(modele, val, a.seq, a.lot, rap, max_lots=40)
tools/essai_blocs.py:49:    COUT_EV_NS, COUT_POIDS_NS, NormeLot, Rapport, charger, decharge, evaluer,
tools/essai_blocs.py:317:                bpc = evaluer(modele, val, a.seq, a.lot)
tools/essai_blocs.py:324:        bpc = evaluer(modele, val, a.seq, a.lot, rap, max_lots=40)
tools/aligneur_litteraire.py:576:def evaluer_ancres(
tools/aligneur_litteraire.py:730:        global_ = evaluer_ancres(perles, ancres_fr, ancres_en, rayon=rayon)
tools/aligneur_litteraire.py:731:        distinct = evaluer_ancres(perles, ancres_fr, ancres_en, rayon=rayon, seulement=distinctives)
tools/aligneur_litteraire.py:751:        "global": evaluer_ancres(perles, ancres_fr, ancres_en, rayon=rayon),
tools/aligneur_litteraire.py:752:        "distinctives": evaluer_ancres(perles, ancres_fr, ancres_en, rayon=rayon, seulement=distinctives),
tools/aligneur_litteraire.py:779:                "global": evaluer_ancres(perles, ancres_fr, ancres_en_melangee
… [3319 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"evaluer\\|--par-langue\\|par langue\" docs/produit/README.md | head -40", "description": "Search evaluer in produit README"}`

  ```
9:> **livré** (version **0.1.0**) : `analyser`, `evaluer`, `rejouer`, `restituer` et `--version`
122:python3 tools/drave.py evaluer
274:`drave evaluer` ne mesure qu'elle. La cascade avec le vrai tagger 7B a été mesurée à **0,9415**
315:| **`drave evaluer`** | **0,55 s** au total | une lecture (heuristique), démarrage Python compris |
342:| **gold versionné** | les 4 gold sont dans le dépôt ; `evaluer` rejoue hors ligne | `tools/tests/linguistique/gold*.json` |
357:| **0** | succès : annotation rendue, évaluation rendue, rejeu identique, restitution rendue | `analyser`, `evaluer`, `rejouer`, `restituer` |
377:python3 tools/drave.py evaluer [--gold] [--json]
383:**Sorties réelles des commandes** (07/11 pour le format ; les valeurs d'`evaluer` sont celles
390:$ python3 tools/drave.py evaluer --gold
412:| `--json` | `analyser`, `evaluer`, `restituer` | sortie machine UTF-8 |
419:| `--gold` | `evaluer` | gold gelé 602 au lieu du vivant 612 |
437:| **`--strict`** | `evaluer` ne mesure pas la cascade et n'applique pas son plancher (0,70) ; c'est le banc de recherche (`evaluer_gold.py`) qui le fait |
  ```

- **bash** `{"command": "grep -n \"evaluer\\|par-langue\\|par_langue\" tools/drave.py | head -60", "description": "Find evaluer in drave.py"}`

  ```
8:    python3 tools/drave.py evaluer
9:    python3 tools/drave.py evaluer --gold --json
210:    """Charge `evaluer_gold.py` (le gold et sa mesure) sans dépendre du répertoire courant."""
211:    chemin = RACINE / "tools" / "tests" / "linguistique" / "evaluer_gold.py"
214:    spec = importlib.util.spec_from_file_location("_drave_evaluer_gold", chemin)
280:def cmd_evaluer(args: argparse.Namespace) -> int:
283:    mesure = evaluateur.evaluer_bloc("heuristique", bl.Heuristique(), phrases)
285:    _lineaire = evaluateur.evaluer_bloc("lineaire", bl.Heuristique(partition="filtrer"), phrases)
429:        "Commandes : analyser, evaluer, rejouer, restituer.\n"
437:        "  python3 tools/drave.py evaluer --gold --json\n"
450:                                  metavar="{analyser,evaluer,rejouer,restituer}",
477:    evaluer = sous.add_parser(
478:        "evaluer",
482:        epilog="Exemple : python3 tools/drave.py evaluer --gold --json",
485:    evaluer.add_argument("--gold", action="store_true",
487:    evaluer.add_argument("--json", action="store_true",
489:    evaluer.set_defaults(fonction=cmd_evaluer)
  ```

- **bash** `{"command": "sed -n '1,120p' tools/tests/test_produit.py", "description": "Read start of test_produit"}`

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


… [3244 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '180,360p' tools/drave.py", "description": "Read evaluer implementation"}`

  ```
sys.stdout.write(_sur(json.dumps(a.json(), ensure_ascii=False)) + "\n")
        n += 1
    if n == 0:
        print(f"{NOM}: refus d'analyse : vide", file=sys.stderr)
        return 3
    return 0


def cmd_analyser(args: argparse.Namespace) -> int:
    texte = _lire_entree(args)
    if args.jsonl:
        return _analyser_jsonl(texte, args)
    annotation = bl.Heuristique(partition=args.partition).analyser(texte, args.langue,
                                                                   args.contexte)
    if annotation.refus:
        # un refus est une **réponse** : le JSON la porte, le code 3 la distingue d'une erreur
        if args.json:
            sys.stdout.write(_dumps(annotation.json()))
        else:
            print(f"{NOM}: refus d'analyse : {annotation.refus} "
                  "(le texte doit contenir au moins une lettre ou un chiffre)", file=sys.stderr)
        return 3
    if args.json:
        sys.stdout.write(_dumps(annotation.json()))
    else:
        print(_sur(formater_annotation(annotation)))
    return 0


def _module_evaluation():
    """Charge `evaluer_gold.py` (le gold et sa mesure) sans dépendre du répertoire courant."""
    chemin = RACINE / "too
… [6756 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '360,520p' tools/drave.py", "description": "Read CLI args of drave.py"}`

  ```
except (OSError, ValueError) as exc:
            print(f"{NOM}: erreur : banc illisible : {exc}", file=sys.stderr)
            return 1
        if args.canonique:
            rapport = restitution.mesurer_banc_v1(items, args.langue)
        else:
            rapport = restitution.mesurer_banc(items, args.langue)
        rapport["banc"] = args.banc
        if args.json:
            sys.stdout.write(_dumps(rapport))
        else:
            formateur = (restitution.formater_banc_v1 if args.canonique
                         else restitution.formater_banc)
            print(_sur(formateur(rapport, args.banc)))
        return 0

    texte = _lire_entree(args)
    if args.texte is None and not args.fichier:
        print(f"{NOM}: erreur d'usage : TEXTE ou --fichier requis", file=sys.stderr)
        return 2
    annotation = bl.Heuristique().analyser(texte, args.langue, args.contexte)
    if annotation.refus:
        print(f"{NOM}: refus d'analyse : {annotation.refus} "
              "(le texte doit contenir au moins une lettre ou un chiffre)", file=sys.stderr)
        return 3
    if args.canonique:
        mesure_v1 = restitution.mesurer_annotation_v1(annotation, texte)
        if arg
… [6916 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,220p' tools/tests/linguistique/evaluer_gold.py", "description": "Read evaluateur_gold.py part 1"}`

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
… [9827 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"langue\\|def evaluer_bloc\\|def charger\\|par_langue\\|par langue\" tools/tests/linguistique/evaluer_gold.py | head -60", "description": "Search langue in evaluateur_gold"}`

  ```
24:def charger() -> list[dict]:
38:def charger_gele() -> list[dict]:
80:def evaluer_bloc(nom: str, bloc, phrases: list[dict]) -> dict:
89:    par_langue = {"fr": {"cibles": 0, "labels": 0, "exact": 0, "topk": 0},
94:        a = bloc.analyser(phrase["texte"], phrase["langue"])
119:        langue = phrase.get("langue", "fr")
120:        bloc_langue = par_langue.get(langue, par_langue["fr"])
126:            bloc_langue["cibles"] += 1
131:            bloc_langue["labels"] += 1
137:                bloc_langue["exact"] += 1
157:                bloc_langue["topk"] += 1
213:                        "par_langue": {lg: {"cibles": v["cibles"], "labels": v["labels"],
216:                                       for lg, v in par_langue.items()}},
  ```

- **bash** `{"command": "grep -rn \"J11.2\\|par-langue\\|par_langue\\|rapport-evaluer\" --include=\"*.md\" --include=\"*.json\" --include=\"*.py\" --include=\"*.sh\" . 2>/dev/null | grep -v \".git/\" | head -60", "description": "Search J11.2 references"}`

  ```
./reports/07/p1.md:434:`tools/generer_par_langue.py` ✓ — deux amorces (une par langue ✓), trois adaptateurs (aucun, français,
./reports/jeux-langues-mesures.json:43:  "par_langue": {
./reports/jeux-langues-mesures.json:116:  "moyenne_concepts_par_langue": 20.13,
./reports/jeux-langues-mesures.json:186:  "par_langue": {
./reports/deepseek-mesures.json:12: "par_langue": {
./reports/deepseek-mesures-300.json:12: "par_langue": {
./reports/cerveau-mesures-corrigees.json:956:    "par_langue": {
./reports/cerveau-mesures-corrigees.json:68086:    "par_langue": {
./reports/pipeline-semantique.json:80:   "par_langue": {
./reports/multilingue.json:1249: "par_langue": {
./reports/multilingue.json:9152: "par_langue_jeu": {
./reports/pipeline-m2.json:10213:   "par_langue": {
./reports/toutes-langues.md:86:| 071 · 71 | 71. Blanchir l'entrée par langue : écarté — et un chiffre qui tombe | 2026-10-07 00:13 HAE (`2a70119`) | [071-71-blanchir-lentree-par-langue-ecarte-et-un.md](toutes-langues/071-71-blanchir-lentree-par-langue-ecarte-et-un.md) |
./reports/pensee-frontiere-71.json:12:    "duree_par_langue_ms": 0.11
./reports/pensee-frontiere-71.json:24:  "par_langue": {
./reports/pensee-contrat-s.json
… [2987 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '220,340p' tools/tests/linguistique/evaluer_gold.py", "description": "Read rest of evaluer_bloc"}`

  ```
"topk_taux": round(att_t_topk / max(1, att_t_n), 4),
                             "couverture": round(att_t_labels / max(1, att_t_n), 4)},
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", default="")
    ap.add_argument("--reel", action="store_true")
    args = ap.parse_args()
    phrases = charger()
    h, n = bl.Heuristique(), bl.MockNeuronal()
    cascade = bl.Cascade(h, n)
    blocs = {"heuristique": h, "mock_neuronal": n,
             "parallele": bl.Parallele([h, n]), "cascade": cascade}
    sources = {"all": phrases,
               "reel": [p for p in phrases if p["source"] in ("hand", "reel")],
               "hand": par_source(phrases, "hand"),
               "reel_new": par_source(phrases, "reel"),
               "synthetique": par_source(phrases, "synthetique")}
    resultats = {nom: {src: evaluer_bloc(nom, bloc, ps) for src, ps in sources.items()}
                 for nom, bloc in blocs.items()}
    resultats["cascade"]["appels_neuronal"] = cascade.appels_neuronal
    reel = {"statut": "non demandé"}
    if args.reel:
        try:
            from bloc_linguistique import NeuronalLLM
            m = NeuronalL
… [3543 caractères tronqués]
  ```

- **bash** `{"command": "cat reports/rapport-pensee-par-langue.md; echo \"===== JSON =====\"; sed -n '1,120p' reports/pensee-par-langue.json", "description": "Read existing per-language report"}`

  ```
# B13 — la mesure par langue : l'exact tient, la couverture anglaise non

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
> **183/183 portes** : la mesure d'attachement est désormais **scindée par langue**. Le français
> donne **113/117 (0,9658)** et l'anglais **28/28 (1,000)** — mais l'anglais n'a que **28 labels
> sur 88 cibles** (contre 117/151 en français). L'échec anglais est un échec de **couverture**
> (segmentation), pas d'attachement — ce que A14 avait établi (60 des 94 spans perdus sont anglais).
>
> **Dispositif** : [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py)
> (`attachement.par_langue`), [`autotest.py`](../tools/pensee/autotest.py) (T180) ;
> fiche A14 [gold anglais](rapport-gold-anglais.md) ; JSON [`pensee-par-langue.json`](pensee-par-langue.json).

## 1. Les deux langues

| langue | cibles | labels | exact | top-k | exact / spans |
|---|---:|---:|---:|---:|---:|
| **français** | 151 | **117** (77,5 %) | 113 | 114 | **0,9658** |
| **anglais** | 88 | **28** (31,8 %) | 28 | 28 | **1,0000** |
| tout | 239 | 145 | 141 | 142 | 0,9724 |

**Ce que ça dit** :

- **L'attachement est juste dans les deux 
… [2019 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\np=json.load(open('tools/chantier/plan.json'))\nprint(type(p), list(p)[:20] if isinstance(p,dict) else len(p))\nEOF", "description": "Inspect plan.json structure"}`

  ```
<class 'dict'> ['nom', 'principe', 'taches']
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\np=json.load(open('tools/chantier/plan.json'))\nfor t in p['taches']:\n    if 'J11' in str(t) or 'par-langue' in str(t) or 'langue' in str(t).lower():\n        print(json.dumps(t, ensure_ascii=False, indent=1))\nEOF", "description": "Find J11.2 task in pla … [3 caractères tronqués]`

  ```
{
 "id": "J2.1",
 "jour": 2,
 "titre": "Panini I — la table atomes ↔ niveaux",
 "mandat": "Tâche J2.1 : la table de correspondance entre les **14 atomes** de Panini (∃ ∆ ∼ ↗ ⊙ ⧖ ◇ № ⊕ ⊗ λ ⊞ ≍ ≡) et nos **niveaux** (graphème, mot, pos, syntagme, phrase, pragmatique, discours, document). Lis `../Panini/README.md`, `../Panini-Research/`, `docs/theorie/genealogie-des-langues.md`. Produis `reports/rapport-atomes-niveaux.md` + JSON : 14 lignes, ce que chaque atome capte, quel niveau le porte, la mesure possible. Aucune écriture dans Panini.",
 "budget_min": 90,
 "acceptation": [
  {
   "commande": "test -f reports/rapport-atomes-niveaux.md && echo FICHE-OK",
   "attendu": "FICHE-OK"
  },
  {
   "commande": "grep -c '∃' reports/rapport-atomes-niveaux.md",
   "attendu": ""
  }
 ]
}
{
 "id": "J2.2",
 "jour": 2,
 "titre": "Panini I — le corpus commun",
 "mandat": "Tâche J2.2 : le corpus commun — choisir un échantillon (10-50 textes) présent des deux côtés (Panini/NIPADA et Drave), le normaliser (UTF-8, une phrase par ligne, métadonnées langue/époque), l'écrire dans `work/corpus-commun/` (non versionné) + une fiche `reports/rapport-corpus-commun.md` + JSON. Lire les corpus Panini sans les mod
… [4207 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,160p' docs/produit/README.md", "description": "Read produit README beginning"}`

  ```
# Le premier produit — analyser un texte avec Drave

> **Ce que ce document est.** La notice d'usage du **premier produit** de Drave : le bloc
> linguistique, utilisable **aujourd'hui**, sur un CPU, sans modèle et sans réseau. Il dit à qui
> il s'adresse, ce qu'il fait, comment l'exécuter, ce qu'il ne fait pas, ce qu'il coûte et ce
> qu'il garantit.
>
> **Vérifié le 2026-11-07** sur la branche `s/v7`. Le point d'entrée `tools/drave.py` est
> **livré** (version **0.1.0**) : `analyser`, `evaluer`, `rejouer`, `restituer` et `--version`
> existent, et la
> porte produit est verte. Le format est **version 2** (`schema: "drave.annotation"`,
> `version: 2`) : le schéma v2 ajoute `meta.partition` et `meta.alternative`, et la **version 1
> reste lue** ([`tools/schemas/`](../../tools/schemas/)). Les sorties du § 3.1, du § 3.4 et du
> § 3.5 ont été relancées le 07/11 pour le format v2 ; les mesures chiffrées du § 2 et du § 3.3
> datent du **06/11**, quand le format était v1. Ce qui manque encore au contrat est nommé au § 7,
> sans être présenté comme acquis.
>
> **Le produit en une phrase.** Vous donnez un texte ; il rend une **annotation** — langue,
> classes de mots, syntagmes, attachements
… [7760 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '260,460p' docs/produit/README.md", "description": "Read produit README evaluer section"}`

  ```
lexique est disjoint. Conséquence : **235/236 (0,9958)** est l'exactitude **conditionnelle aux
spans prédits**, pas la couverture du langage. Lire les deux ensemble.

**Le doublon REL de l'union.** Deux REL peuvent se chevaucher : la plus longue porte
`meta.union: true`. C'est une **lecture concurrente** publiée par l'union, pas un second
attachement ; la sortie lisible la montre comme un **doublon REL**, et il faut la filtrer pour
une lecture unique (garder `union: null`, ou le segment qui en contient un autre).

**3. `cascade_pos` : le plancher, pas le gain.** La « rouge » historique est devenue un
**plancher** : le banc exige **0,70** et la cascade rend **0,7465**, donc la porte
`porte-bloc-linguistique.sh` est **verte**. Mais la cascade (heuristique + `MockNeuronal`) reste
**sous l'heuristique (0,7581)** en POS : la fusion par confiance laisse gagner le stub. Ce n'est
pas un gain de POS ; c'est un **échange** — les syntagmes sont meilleurs (F1 **0,6141** contre
**0,6482**, tête **0,7709** contre **0,7671**). Le produit par défaut reste l'heuristique, et
`drave evaluer` ne mesure qu'elle. La cascade avec le vrai tagger 7B a été mesurée à **0,9415**
en POS sur 180 phrases, mais e
… [12114 caractères tronqués]
  ```

- **bash** `{"command": "grep -rIn \"J11\\.2\\|par-langue\\|par_langue\" docs/ tools/chantier/ journal/ 2>/dev/null | head -80", "description": "Search J11.2 in docs/plan/journal"}`

  ```
docs/pilotage/semaine-autonome.md:251:**La suite.** **J11.1–J11.4** (produit : exemples, par-langue, robustesse, schéma documenté) ;
docs/pilotage/roadmap.md:72:[`fiche`](../../reports/rapport-exemples-rejoues.md) + JSON. La suite produit est **J11.2**
docs/pilotage/roadmap.md:73:(`evaluer --par-langue`), **J11.3** (50 textes libres), **J11.4** (schéma v2 documenté).
docs/pilotage/en-cours.md:117:| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, gold 432, r035 + convention GV (0,7902), s065 (238/239), g017 rejeté, schéma v2, restitution v1 (canonique 46/46, strict 0,1087), J11.1 (exemples rejoués)** | **J11.2–J11.4** (produit) ; **trancher `g017`** ; puis T132/T133, gold 200+ ; **B10.3 bloquée** |
docs/pilotage/en-cours.md:127:**N2** — porte (0,2856/0,3566) ; **Pensée** — `g017`, T132/T133, gold 200+ ; **J3.2** — V14 des 21 langues ; **J7.1** — réplication neuronale ; **S** — 11 verdicts + pointeur ; **R0.7** — split réel ; **A** — A6.2, A8.3b2 ; **J14.1** — passe + tag ; **J11.2–J11.4** — produit, Panini, table.
tools/chantier/plan.json:328:   "id": "J11.2",
tools/chantier/plan.json:331:   "mandat": "Tâche J11.2 : ajouter `evaluer --par
… [17059 caractères tronqués]
  ```

- **bash** `{"command": "git log --all --oneline --grep=\"J11\" | head -20; echo \"---\"; git branch -a | head -20", "description": "Search git history for J11"}`

  ```
84e393bb J11.1 — LES 5 EXEMPLES REJOUÉS : 4 BLOCS SUR 5 CORRIGÉS, r035 DÉSORMAIS PRÉDIT ; F1 0,7902, ATTACHEMENT 238/238
---
  backup/pre-scrub-20261101-133055
  master
  s/close
* s/v7
  remotes/origin/HEAD -> origin/master
  remotes/origin/master
  remotes/origin/s/close
  remotes/origin/s/v7
  ```

- **bash** `{"command": "sed -n '55,85p' docs/pilotage/roadmap.md; echo \"=== semaine ===\"; sed -n '235,260p' docs/pilotage/semaine-autonome.md", "description": "Read roadmap and week plan around J11"}`

  ```
**J10.1 — le bilan du chantier.** **20 tâches sur 21** passent l'acceptation ; **5 timeouts**
(J1.2, J2.2, J3.1, J5.2, J8.1), dont **4 récupérés** par une acceptation verte ou le commit de la
tâche suivante, et **1 vrai échec** (J5.2, le tag absent). Le produit gagne **2 attachements**
(236 → 238 labels) et **+0,0369 de F1** (0,7533 → 0,7902), la POS ne bouge pas ; Panini est
**mesuré et borné** (table 14/14, corpus 418/438, retrieval J3.1, généalogie J3.2, familles
J7.1) ; la coordination N2/S/R/A est **datée**. La **clôture formelle** reste à faire : **J14.1**
doit refaire la passe et poser le tag `chantier-2026-11-14`. Le détail — chiffres, décisions
D1–D20, rejets R1–R30, échecs, reste — est dans
[`rapport-bilan-chantier.md`](../../reports/rapport-bilan-chantier.md) + JSON.

**J11.1 — les exemples rejoués.** Les **5 blocs** de `docs/produit/exemples.md` sont reproduits
avec le code courant ; **4 sont corrigés** : la ponctuation finale entre dans le POS (`g001`,
`r241`), le refus sort en **3** et `r035` — l'ancien échec connu — rend exactement le gold
(`REL [9:24] « she talks about » → film`). Le seul bloc identique est `g011`. F1 **0,7902**,
attachement **238/238 labels** (238/
… [3588 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,80p' reports/INDEX.md; echo \"...\"; tail -40 reports/INDEX.md", "description": "Read reports index"}`

  ```
# Index des fiches de reports/

> **Généré** par `tools/index_reports.py` — **722 fiches**. Les fichiers
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
… [13904 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '120,260p' tools/tests/test_produit.py; echo \"=== porte ===\"; cat tools/porte-produit.sh", "description": "Read rest of tests and product gate"}`

  ```
sys.path.insert(0, str(RACINE))
        import tools.bloc_linguistique as bl
        h = bl.Heuristique()
        for valeur in (b"octets", 42, ["liste"], None):
            a = h.analyser(valeur, "fr")
            self.assertEqual(a.refus, "non_texte", type(valeur).__name__)
            self.assertEqual(a.etiquettes, [])



class TestPartition(unittest.TestCase):
    """La vue des syntagmes est un choix explicite (`--partition`)."""

    def test_filtrer_donne_une_vue_lineaire(self):
        sortie = drave("analyser", "Le chat de la voisine qui dort sur le toit se réveille.",
                      "--partition", "filtrer", "--json")
        self.assertEqual(sortie.returncode, 0, sortie.stderr[:300])
        segs = [e for e in json.loads(sortie.stdout)["etiquettes"] if e["niveau"] == "syntagme"]
        self.assertTrue(segs)
        for a, b in zip(segs, segs[1:]):
            self.assertTrue(a["fin"] <= b["debut"], (a, b))

    def test_alternative_etiquette_les_chevauchements(self):
        sortie = drave("analyser", "Le chat de la voisine qui dort sur le toit se réveille.",
                      "--json")
        self.assertEqual(sortie.returncode, 0, sortie.stderr[:300])
      
… [7978 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, collections\nfor f in ['gold.json','gold_reel.json','gold_synthetique.json','gold_gele.json']:\n    d=json.load(open('tools/tests/linguistique/'+f))\n    c=collections.Counter(p.get('langue','fr') for p in d['phrases'])\n    print(f, len(d['phrases']), di … [182 caractères tronqués]`

  ```
gold.json 20 {'fr': 14, 'en': 6} segments avec cible 13
gold_reel.json 432 {'fr': 228, 'en': 204} segments avec cible 171
gold_synthetique.json 160 {'fr': 160} segments avec cible 55
gold_gele.json 602 {'fr': 394, 'en': 208} segments avec cible 239
  ```

- **bash** `{"command": "sed -n '160,265p' docs/produit/README.md", "description": "Read README sections 3.3-4"}`

  ```
Quatre vues (`--partition`) : `alternative` (défaut : les deux segments restent, `meta.alternative`
dit lequel est préféré — **aucune perte**), `filtrer` (vue linéaire : **F1 +0,047** mais **18
attachements en moins**), `filtrer_union` (variante économique, 91 paires résiduelles) et `brut`
(l'ancienne sortie). Le défaut est `alternative`. Un segment qui appartient à un groupe de
chevauchement porte `meta.partition` (`{groupe, rang, membres, vue}`) et `meta.alternative`
(`[{type, debut, fin, source, union, relation, rang, …}]`) ; les deux champs sont typés dans le
[schéma v2](../../tools/schemas/drave-annotation-v2.json).

### 3.3 ter Le contexte (mémoire de discours)

```bash
python3 tools/drave.py analyser "Il dort." --contexte "Le chat est sur le toit."
```

Le champ `contexte` est porté dans le JSON ; il alimente la mémoire de discours (coréférence,
connecteurs) sans changer le texte analysé.

### 3.4 Rejouer et vérifier le déterminisme

```bash
python3 tools/drave.py rejouer "Le chat de la voisine qui dort sur le toit se réveille."
```
```
rejeu identique : oui
  texte      : 'Le chat de la voisine qui dort sur le toit se réveille.'
  langue     : fr
  étiquettes : 60
  JSON   
… [4317 caractères tronqués]
  ```

- **bash** `{"command": "git show --stat --oneline 84e393bb | head -60", "description": "Show J11.1 commit files"}`

  ```
84e393bb J11.1 — LES 5 EXEMPLES REJOUÉS : 4 BLOCS SUR 5 CORRIGÉS, r035 DÉSORMAIS PRÉDIT ; F1 0,7902, ATTACHEMENT 238/238
 docs/pilotage/en-cours.md                          |   15 +-
 docs/pilotage/roadmap.md                           |    9 +
 docs/produit/exemples.md                           |  151 +-
 journal/2026-11-14/README.md                       |    7 +-
 journal/2026-11-14/docs.md                         |    2 +-
 journal/2026-11-14/memoire.md                      |    5 +-
 journal/2026-11-14/mesures.md                      |    2 +-
 journal/2026-11-14/portes.md                       |    2 +-
 journal/README.md                                  |    4 +-
 journal/sessions/MANIFEST.md                       |    6 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md |   26 +
 .../rapport.md                                     |   14 +-
 .../digest.md                                      | 2096 ++++++++++++++++++++
 .../rapport.md                                     |   54 +-
 reports/rapport-exemples-rejoues.json              |  500 +++++
 reports/rapport-exemples-rejoues.md                |  171 ++
 16 files changed, 2970 insertions(+), 94 deletions(-)
  ```

- **bash** `{"command": "cat reports/rapport-exemples-rejoues.md | head -80; echo \"=== JSON head ===\"; sed -n '1,60p' reports/exemples-rejoues.json 2>/dev/null || ls reports/*exemples*", "description": "Read J11.1 report style"}`

  ```
# J11.1 — les cinq exemples rejoués : 4 blocs sur 5 ont bougé, `r035` n'est plus un échec

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Tâche** : **J11.1** · **Date** : 2026-11-14 ·
> **Verdict** : ✅
> **Cinq blocs rejoués** avec le code courant, **4 corrigés**, **1 identique** : la ponctuation
> finale entre dans le POS (`g001`, `r241`), le refus sort en **3**, et **`r035` est désormais
> prédit** — span `REL [9:24] « she talks about »` et cible `film`, exactement le gold.
> **Le chiffre.** F1 syntagmes **0,7902** ; POS **0,8625** (fermé 0,9373, ouvert 0,7918) ;
> attachement **238/238 labels** (238/239 cibles, **0,9958**). Le mandat porte encore **237/238** :
> c'est l'état d'avant `s065` (J6.2), qui a ajouté un label **sans toucher un span** — F1 inchangé.
> **Dispositif** : [`docs/produit/exemples.md`](../docs/produit/exemples.md) (les 5 blocs),
> [`tools/drave.py`](../tools/drave.py) 0.1.0, [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
> `jq` ; mesure par `python3 tools/drave.py evaluer --json` sur le gold vivant (612 phrases).
> **JSON** : [`rapport-exemples-rejoues.json`](rapport-exemples-rejoues.json).

## 1. Le verdict du rejeu

Les cinq commandes de 
… [3216 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '105,135p' docs/pilotage/en-cours.md; echo \"=== roadmap 60-80 ===\"; sed -n '60,80p' docs/pilotage/roadmap.md", "description": "Read current state lines"}`

  ```
| fichiers / JSON de résultats | **725** / **819** | `reports/*.md` / `reports/*.json` |
| documents de `docs/` | **123** (hors archive et README) | `docs/**/*.md` |
| dernière passe | **14/11 00 h 30** (84, **81/3**) ; rouges tolérées `indice`, `melange`, `sessions` | `docs/pilotage/references-non-regression.md` |

## Les chantiers et leurs bloquants

**Dépendances** : [le graphe](backlog/dependances.md) ; cette table ne garde que les **bloquants
externes** et la **prochaine action**.

| chantier | frontière (graphe) | bloquant (ressource) | prochaine action |
|---|---|---|---|
| **A — le moteur** | **A2.6** | A3.4 Colab ; A5.4 FPGA ; **A6.2 libre** (MoE 18,56 Go, PPL 37,2013 ; résidence 16 GiB) | **A2.6** (experts et tête) ; **A6.2** rapport + A8.3b2 |
| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, gold 432, r035 + convention GV (0,7902), s065 (238/239), g017 rejeté, schéma v2, restitution v1 (canonique 46/46, strict 0,1087), J11.1 (exemples rejoués)** | **J11.2–J11.4** (produit) ; **trancher `g017`** ; puis T132/T133, gold 200+ ; **B10.3 bloquée** |
| **N — le natif** | **N2, N4** | N2 : **fenêtre 1 024 — 2,3911 / 2,3522 au grand c
… [3323 caractères tronqués]
  ```

- **bash** `{"command": "git show 84e393bb -- docs/pilotage/en-cours.md docs/pilotage/roadmap.md | head -120", "description": "See J11.1 state/roadmap diff"}`

  ```
commit 84e393bb3f72fdae0e0f13278b17a684ab284b4b
Author: Stéphane <stephane@localhost>
Date:   Sat Nov 14 04:28:47 2026 -0500

    J11.1 — LES 5 EXEMPLES REJOUÉS : 4 BLOCS SUR 5 CORRIGÉS, r035 DÉSORMAIS PRÉDIT ; F1 0,7902, ATTACHEMENT 238/238
    
    Les 5 blocs de docs/produit/exemples.md sont rejoués sur le code courant
    (CLI drave 0.1.0, schéma v2) : 5/5 reproduits, 4 corrigés, 1 identique (g011).
    
    - g001 : 19 → 20 étiquettes, ./PONCT ajouté, couverture pos 0,92 → 0,95.
    - r241 : left NOUN 0,3 → VERB 0,85, ./PONCT ajouté.
    - refus : code de sortie 1 → 3 ; avec --json, annotation de refus sur stdout.
    - r035 : l'ancien échec connu est prédit — REL [9:24] « she talks about » → film,
      GN [0:8] et GV [25:31] exacts ; il ne reste que g017 comme cible sans span.
    
    Mesure : gold vivant 612 phrases, F1 0,7902, POS 0,8625 (ouvert 0,7918),
    attachement 238/238 labels (238/239 cibles, 0,9958). Le mandat 237/238 est l'état
    d'avant s065 ; J6.2 a ajouté un label sans toucher un span.
    
    Contrôle négatif : mutation d'un token (left/VERB → NOUN) dans une copie de la doc ;
    le comparateur signale 4/5 et l'écart exact. Doc réelle : 5/5.
    
    Por
… [9782 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "old_string": "def _formater_evaluation(rapport: dict) -> str:\n    gold = rapport[\"gold\"]\n    mesure = rapport[\"heuristique\"]\n    pos = mesure[\"pos\"]\n    syn = mesure[\"syntagme\"]\n    tete = syn[\"tete\"]\n   … [4895 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py": file has not been read — read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "offset": 230, "limit": 90}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py</path>
<type>file</type>
<content>
230:     Graine fixe, donc reproductible : c'est un plancher, pas une mesure de qualité.
231:     """
232:     cibles = _cibles_gold(phrases)
233:     if not cibles:
234:         return 0.0
235:     univers = sorted(set(cibles))
236:     rng = random.Random(0)
237:     justes = sum(1 for c in cibles if rng.choice(univers) == c)
238:     return round(justes / len(cibles), 4)
239: 
240: 
241: def _pct(valeur: float) -> str:
242:     return f"{100.0 * float(valeur):.2f} %"
243: 
244: 
245: def _formater_evaluation(rapport: dict) -> str:
246:     gold = rapport["gold"]
247:     mesure = rapport["heuristique"]
248:     pos = mesure["pos"]
249:     syn = mesure["syntagme"]
250:     tete = syn["tete"]
251:     att = mesure["attachement"]
252:     att_tete = mesure["attachement_tete"]
253:     prag = mesure["pragmatique"]
254:     controle = rapport["controle_negatif"]
255:     return "\n".join([
256:         f"{NOM} {VERSION} — évaluation de l'heuristique sur le gold",
257:         f"gold {gold['nom']} · {gold['phrases']} phrases · {gold['tokens']} tokens · "
258:         f"{gold['cible
… [3550 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "old_string": "    controle = rapport[\"controle_negatif\"]\n    return \"\\n\".join([\n        f\"{NOM} {VERSION} — évaluation de l'heuristique sur le gold\",", "new_string": "    controle = rapport[\"controle_negatif\" … [92 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "new_string": "        f\"CONTRÔLE NÉGATIF cible exacte tirée au hasard {_pct(controle['exact_taux'])} \"\n        f\"(graine {controle['graine']}, {controle['cibles']} cibles)\",\n    ]\n    par_langue = rapport.get(\"p … [1300 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "new_string": "        \"controle_negatif\": {\n            \"nom\": \"cible exacte tirée au hasard dans le gold\",\n            \"graine\": 0,\n            \"cibles\": len(_cibles_gold(phrases)),\n            \"exact_ta … [1165 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "limit": 40, "offset": 495}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py</path>
<type>file</type>
<content>
495:                           help="texte à analyser (entre guillemets) ou --fichier")
496:     analyser.add_argument("--partition", choices=("brut", "alternative", "filtrer_union", "filtrer"),
497:                           default="alternative",
498:                           help="la vue des syntagmes qui se chevauchent (défaut : alternative)")
499:     analyser.add_argument("--fichier", default=None, metavar="CHEMIN",
500:                           help="lire le texte dans un fichier UTF-8 (au lieu de l'argument)")
501:     analyser.add_argument("--jsonl", action="store_true",
502:                           help="une ligne JSON par phrase (traitement de corpus)")
503:     analyser.add_argument("--contexte", default=None,
504:                           help="le texte qui précède (mémoire de discours : coréférence, connecteurs)")
505:     analyser.add_argument("--langue", choices=("fr", "en"), default=None,
506:                           help="indice de langue (fr/en) ; sans lui, le bloc détecte")
507:     analyser.add_argument("--json", action="store_true",
508:              
… [1618 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "new_string": "        description=\"Mesure POS, syntagmes (F1/tête) et attachement (exact/couverture) \"\n                    \"sur le gold, avec un contrôle négatif reproductible. Avec --par-langue, \"\n                … [1285 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **bash** `{"command": "time python3 tools/drave.py evaluer --par-langue", "description": "Run evaluer --par-langue"}`

  ```
drave 0.1.0 — évaluation de l'heuristique sur le gold
gold vivant (hand + reel + synthétique) · 612 phrases · 3179 tokens · 239 cibles d'attachement

POS         exactitude 86.25 %  (fermé 93.73 %, ouvert 79.18 %)
SYNTAGMES   F1 79.02 %  (P 78.60 % / R 79.44 %)
  tête      F1 90.29 %  (P 92.61 % / R 88.08 %)
  vue linéaire (partition filtrer) F1 81.44 %  · attachement 93.72 % de couverture
ATTACHEMENT exact 99.58 % · couverture 99.58 % · exact sur span 100.00 % · top-k 98.74 %
  tête      couverture 100.00 % · top-k 99.16 %
PRAGMATIQUE acte 99.67 % · négation 97.71 % · modalité 98.86 % · double sens 94.44 %
FRACTION SÉMANTIQUE 54.76 %
CONTRÔLE NÉGATIF cible exacte tirée au hasard 1.67 % (graine 0, 239 cibles)

PAR LANGUE
  en  210 phrases · 1148 tokens · 88 cibles d'attachement
      POS 94.51 % (fermé 98.30 %, ouvert 90.54 %) · SYNTAGMES F1 86.56 % (tête 95.27 %)
      ATTACHEMENT exact 98.86 % · couverture 98.86 % · top-k 98.86 % · PRAGMATIQUE acte 99.52 %
      CONTRÔLE NÉGATIF cible exacte tirée au hasard 2.27 % (graine 0, 88 cibles)
  fr  402 phrases · 2031 tokens · 151 cibles d'attachement
      POS 81.59 % (fermé 90.92 %, ouvert 73.25 %) · SYNTAGMES F1 74.75 % (tête 87.33 %)
… [231 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/drave.py evaluer --par-langue --json > /tmp/eval-pl.json && python3 - <<'EOF'\nimport json\nd=json.load(open('/tmp/eval-pl.json'))\nprint('top keys', list(d))\nfor lg,m in d['par_langue'].items():\n    print('\\n==',lg, 'phrases',m['phrases'],'tokens',m['pos']['tokens'])\n … [569 caractères tronqués]`

  ```
top keys ['version', 'gold', 'heuristique', 'syntagmes_lineaire', 'attachement_lineaire', 'controle_negatif', 'par_langue']

== en phrases 210 tokens 1148
pos {'exactitude': 0.9451, 'exactitude_ferme': 0.983, 'exactitude_ouvert': 0.9054, 'tokens': 1148}
syn {'precision': 0.8988, 'rappel': 0.8348, 'f1': 0.8656, 'tp': 586, 'fp': 66, 'fn': 116}
tete {'precision': 0.9893, 'rappel': 0.9188, 'f1': 0.9527, 'tp': 645, 'fp': 7, 'fn': 57}
att {'cibles': 88, 'labels': 87, 'exact': 87, 'exact_taux': 0.9886, 'couverture': 0.9886, 'exact_taux_span': 1.0, 'topk': 87, 'topk_taux': 0.9886}
pragma {'acte': 0.9952, 'negation': 1.0, 'modalite': 0.9857, 'double_sens': 0.9952}
frac 0.4954
ctrl {'nom': 'cible exacte tirée au hasard dans le gold de la langue', 'graine': 0, 'cibles': 88, 'exact_taux': 0.0227}

== fr phrases 402 tokens 2031
pos {'exactitude': 0.8159, 'exactitude_ferme': 0.9092, 'exactitude_ouvert': 0.7325, 'tokens': 2031}
syn {'precision': 0.7262, 'rappel': 0.77, 'f1': 0.7475, 'tp': 894, 'fp': 337, 'fn': 267}
tete {'precision': 0.8893, 'rappel': 0.8579, 'f1': 0.8733, 'tp': 996, 'fp': 124, 'fn': 165}
att {'cibles': 151, 'labels': 151, 'exact': 151, 'exact_taux': 1.0, 'couverture': 1.0, 'exac
… [270 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport importlib.util, pathlib, sys\nRACINE=pathlib.Path('.').resolve()\nsys.path.insert(0,str(RACINE/'tools'))\nimport bloc_linguistique as bl\nspec=importlib.util.spec_from_file_location('eg', RACINE/'tools/tests/linguistique/evaluer_gold.py')\neg=importlib.util.mod … [712 caractères tronqués]`

  ```
hand         fr n= 14 tok=  74 POS=0.8378 F1=0.8889 tete=0.9639 att_exact=1.0000 cov=1.0000 span=1.0000
hand         en n=  6 tok=  31 POS=1.0000 F1=0.9375 tete=1.0000 att_exact=0.6667 cov=0.6667 span=1.0000
reel         fr n=228 tok=1258 POS=0.8410 F1=0.7158 tete=0.8449 att_exact=1.0000 cov=1.0000 span=1.0000
reel         en n=204 tok=1117 POS=0.9436 F1=0.8638 tete=0.9516 att_exact=1.0000 cov=1.0000 span=1.0000
synthetique  fr n=160 tok= 699 POS=0.7682 F1=0.7888 tete=0.9178 att_exact=1.0000 cov=1.0000 span=1.0000
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_produit.py", "limit": 45, "offset": 195}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_produit.py</path>
<type>file</type>
<content>
195: 
196:     def test_fichier_et_jsonl(self):
197:         import tempfile, pathlib as _p
198:         with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
199:             f.write("Le chat dort.\n\nLa voisine parle au chat. Il dort encore.\n")
200:             chemin = f.name
201:         try:
202:             sortie = drave("analyser", "--fichier", chemin, "--jsonl")
203:             self.assertEqual(sortie.returncode, 0, detail(sortie))
204:             lignes = [json.loads(l) for l in sortie.stdout.splitlines() if l.strip()]
205:             self.assertEqual(len(lignes), 3)
206:             self.assertEqual(lignes[0]["schema"], "drave.annotation")
207:         finally:
208:             _p.Path(chemin).unlink(missing_ok=True)
209: 
210:     def test_fichier_seul(self):
211:         import tempfile, pathlib as _p
212:         with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
213:             f.write("Le chat dort.")
214:             chemin = f.name
215:         try:
216:             so
… [397 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_produit.py", "new_string": "class TestParLangue(unittest.TestCase):\n    \"\"\"`evaluer --par-langue` scinde la mesure fr/en sans la changer.\"\"\"\n\n    def test_par_langue_json(self) -> None:\n        global_ = drave( … [1823 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_produit.py has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/tests/test_produit.py 2>&1 | tail -8", "description": "Run product smoke tests"}`

  ```
..................
----------------------------------------------------------------------
Ran 18 tests in 7.450s

OK
  ```

- **bash** `{"command": "python3 -m py_compile tools/drave.py tools/tests/test_produit.py && python3 tools/drave.py evaluer --par-langue --gold --json > /tmp/eval-pl-gold.json; echo code=$?; python3 - <<'EOF'\nimport json\nd=json.load(open('/tmp/eval-pl-gold.json'))\nprint('gold', d['gold'])\nfor k,v in d['par_ … [210 caractères tronqués]`

  ```
code=0
gold {'nom': 'gelé (référence figée)', 'gele': True, 'phrases': 602, 'tokens': 3141, 'cibles_attachement': 239}
en 208 1141 88 87 87
fr 394 2000 151 147 147
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "limit": 40, "offset": 110}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md</path>
<type>file</type>
<content>
110: GN Le livre → intéressant · REL que j'ai lu → livre · REL que j'ai lu est intéressant → livre · GV est intéressant → livre
111: ```
112: 
113: **Lecture.** Un appel = **une annotation** ; les phrases sont des étiquettes de niveau `phrase`,
114: pas des objets séparés. La REL « que j'ai lu » est bien rattachée à « livre » (cas `g011` du
115: gold). Le JSON publie aussi une **seconde lecture d'union** (`meta.union: true`, span plus
116: large) : dans la sortie lisible, elle apparaît comme un **doublon REL** ; le JSON la marque
117: `union: true`, à filtrer pour une lecture unique (voir [`exemples.md`](exemples.md) § 2).
118: 
119: ### 3.3 Mesurer sur le gold
120: 
121: ```bash
122: python3 tools/drave.py evaluer
123: ```
124: ```
125: drave 0.1.0 — évaluation de l'heuristique sur le gold
126: gold vivant (hand + reel + synthétique) · 612 phrases · 3179 tokens · 239 cibles d'attachement
127: 
128: POS         exactitude 86.25 %  (fermé 93.73 %, ouvert 79.18 %)
129: SYNTAGMES   F1 75.33 %  (P 72.39 % / R 78.53 %)
130:   tête      F1 86.40 %  (P 85.19 % / R 87.65 %)
131: 
… [1189 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/drave.py evaluer --gold", "description": "Get current gold evaluation output"}`

  ```
drave 0.1.0 — évaluation de l'heuristique sur le gold
gold gelé (référence figée) · 602 phrases · 3141 tokens · 239 cibles d'attachement

POS         exactitude 86.25 %  (fermé 93.73 %, ouvert 79.14 %)
SYNTAGMES   F1 78.82 %  (P 78.18 % / R 79.46 %)
  tête      F1 90.25 %  (P 92.34 % / R 88.26 %)
  vue linéaire (partition filtrer) F1 81.27 %  · attachement 92.05 % de couverture
ATTACHEMENT exact 97.91 % · couverture 97.91 % · exact sur span 100.00 % · top-k 97.07 %
  tête      couverture 100.00 % · top-k 99.15 %
PRAGMATIQUE acte 99.67 % · négation 97.67 % · modalité 98.84 % · double sens 94.35 %
FRACTION SÉMANTIQUE 54.96 %
CONTRÔLE NÉGATIF cible exacte tirée au hasard 1.67 % (graine 0, 239 cibles)
  ```

- **bash** `{"command": "sed -n '1,120p' tools/revue_documentation.py", "description": "Inspect doc review tool"}`

  ```
#!/usr/bin/env python3
"""revue_documentation.py — LA REVUE DE FIN DE SOUS-CHANTIER (AGENTS.md §4).

Ce qu'elle vérifie, et qu'il faut corriger AVANT le commit de clôture :
  1. classement : pas de résultats dans docs/ (les fiches sont dans reports/ et citées) ;
  2. structure  : les sept chantiers de en-cours.md ont leur entrée, leur état et leur fiche ;
  3. annotation : les liens relatifs des docs/ et reports/ résolvent, et leur libellé ne
     ment pas sur la cible ; les sources externes sont citées ;
  4. fraîcheur  : en-cours.md date du dernier commit, ET aucun fait n'a été commité après
     le dernier état (comparaison de commits, pas de dates : voir verifie_etat_a_jour.py) ;
  5. cohérence  : la synthèse (index.md) liste les huit chapitres, le chapitre 7 et B10–B12 ;
     les compteurs de la page d'état sont ceux du disque (portes, chapitres, fiches, docs) ;
  6. vocabulaire : « jeton » ne désigne **jamais** la représentation sémantique neutre (RSN) ;
  7. navigation : aucun document vivant n'est orphelin, et aucun chemin en code inline
     ne pointe vers un fichier absent (hors gabarits `AAAA`, `<...>`, `*`).

Sortie : un rapport lisible, code 0 si tout passe, 1 sinon (u
… [2953 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "### 3.3 Mesurer sur le gold\n\n```bash\npython3 tools/drave.py evaluer\n```\n```\ndrave 0.1.0 — évaluation de l'heuristique sur le gold\ngold vivant (hand + reel + synthétique) · 612 phrases · 3179 … [4211 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "limit": 18, "offset": 1}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "limit": 35, "offset": 400}`

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
8: > **Vérifié le 2026-11-07** sur la branche `s/v7`. Le point d'entrée `tools/drave.py` est
9: > **livré** (version **0.1.0**) : `analyser`, `evaluer`, `rejouer`, `restituer` et `--version`
10: > existent, et la
11: > porte produit est verte. Le format est **version 2** (`schema: "drave.annotation"`,
12: > `version: 2`) : le schéma v2 ajoute `meta.partition` et `meta.alternative`, et la **version 1
13: > reste lue** ([`tools/schemas/`](../../tools/schemas/)). Les sorties du § 3.1, du § 3.4 et du
14: > § 3.5 ont été relancées le 07/11 pour le format v2 ; les mesures chiffrées du § 2 et du § 3.3
15: > datent du **06/11**, quand le format était v1. Ce qui manque encore au contrat est nommé au § 7,
16: > sa
… [200 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md</path>
<type>file</type>
<content>
400: 
401: ```bash
402: python3 tools/drave.py --version
403: python3 tools/drave.py --aide
404: python3 tools/drave.py analyser "Le chat dort." [--langue fr|en] [--json] \
405:     [--partition brut|alternative|filtrer_union|filtrer] [--contexte TEXTE]
406: python3 tools/drave.py analyser --fichier corpus.txt [--jsonl|--json]
407: python3 tools/drave.py evaluer [--gold] [--json]
408: python3 tools/drave.py rejouer "TEXTE" [--langue fr|en]
409: python3 tools/drave.py restituer "TEXTE" [--langue fr|en] [--json] [--fichier CHEMIN]
410: python3 tools/drave.py restituer --banc reports/pensee-fiabilite-produit.json [--json]
411: ```
412: 
413: **Sorties réelles des commandes** (07/11 pour le format ; les valeurs d'`evaluer` sont celles
414: mesurées le 06/11) :
415: 
416: ```
417: $ python3 tools/drave.py --version
418: drave 0.1.0
419: 
420: $ python3 tools/drave.py evaluer --gold
421: drave 0.1.0 — évaluation de l'heuristique sur le gold
422: gold gelé (référence figée) · 602 phrases · 3141 tokens · 239 cibles d'attachement
423: ...
424: SYNTAGMES   F1 58.93 %  (P 63.19 % / 
… [453 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "limit": 25, "offset": 435}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md</path>
<type>file</type>
<content>
435: ```
436: 
437: **Options du CLI** :
438: 
439: | option | commande | sens |
440: |---|---|---|
441: | `--langue fr\|en` | `analyser`, `rejouer`, `restituer` | **indice** de langue, pas une contrainte ; hors `fr`/`en` → code 2 |
442: | `--json` | `analyser`, `evaluer`, `restituer` | sortie machine UTF-8 |
443: | `--jsonl` | `analyser` | une ligne JSON par phrase (avec `--fichier`) |
444: | `--fichier CHEMIN` | `analyser`, `restituer` | lit un texte UTF-8 au lieu de l'argument |
445: | `--banc CHEMIN` | `restituer` | mesure un banc JSON de textes (les 50 textes libres) |
446: | `--canonique` | `restituer` | ajoute la forme canonique v1 (segments + rôles + cibles) et son miroir |
447: | `--partition MODE` | `analyser`, `rejouer` | `alternative` (défaut), `filtrer_union`, `filtrer`, `brut` |
448: | `--contexte TEXTE` | `analyser`, `restituer` | mémoire de discours portée dans le JSON |
449: | `--gold` | `evaluer` | gold gelé 602 au lieu du vivant 612 |
450: | `-V`, `--version` | global | `drave 0.1.0` |
451: | `-h`, `--aide` | global | l'aide, largeur fixe |
452: 
453: *
… [527 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "> **Vérifié le 2026-11-14** sur la branche `s/v7`. Le point d'entrée `tools/drave.py` est\n> **livré** (version **0.1.0**) : `analyser`, `evaluer`, `rejouer`, `restituer` et `--version`\n> existent … [1315 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "python3 tools/drave.py evaluer [--gold] [--json] [--par-langue]", "old_string": "python3 tools/drave.py evaluer [--gold] [--json]"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "**Sorties réelles des commandes** (07/11 pour le format ; les valeurs d'`evaluer` sont celles\nmesurées le 14/11) :", "old_string": "**Sorties réelles des commandes** (07/11 pour le format ; les va … [53 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "SYNTAGMES   F1 78.82 %  (P 78.18 % / R 79.46 %)\n  tête      F1 90.25 %  (P 92.34 % / R 88.26 %)\n...", "old_string": "SYNTAGMES   F1 58.93 %  (P 63.19 % / R 55.22 %)\n  tête      F1 73.92 %  (P 81 … [25 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "| `--gold` | `evaluer` | gold gelé 602 au lieu du vivant 612 |\n| `--par-langue` | `evaluer` | détail **fr/en** : POS, syntagmes, attachement et contrôle négatif par langue |", "old_string": "| `-- … [59 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "limit": 22, "offset": 483}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md</path>
<type>file</type>
<content>
483: |---|---|
484: | **voir cinq JSON commentés** | [`exemples.md`](exemples.md) |
485: | **le schéma du JSON** (v2 : `meta.partition`, `meta.alternative`) | [`tools/schemas/drave-annotation-v2.json`](../../tools/schemas/drave-annotation-v2.json) · [v1](../../tools/schemas/drave-annotation-v1.json) |
486: | **la fiche du schéma v2** | [`reports/rapport-schema-v2.md`](../../reports/rapport-schema-v2.md) |
487: | **le contrat du bloc** (9 niveaux, substitution, activation) | [`docs/implantation/bloc-linguistique.md`](../implantation/bloc-linguistique.md) |
488: | **les chiffres de l'attachement** (v12, instantané) | [`reports/rapport-pensee-v12.md`](../../reports/rapport-pensee-v12.md) · [`reports/pensee-v12.json`](../../reports/pensee-v12.json) |
489: | **l'audit des mesures** (contrôles, spans, bases) | [`reports/rapport-audit-v10.md`](../../reports/rapport-audit-v10.md) |
490: | **la performance du cache** (×139, conditions) | [`reports/rapport-cache-chunker-applique.md`](../../reports/rapport-cache-chunker-applique.md) |
491: | **la cascade réelle** (0,9415, 7B, non li
… [885 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "| **l'audit des mesures** (contrôles, spans, bases) | [`reports/rapport-audit-v10.md`](../../reports/rapport-audit-v10.md) |\n| **la mesure par langue** (fr/en, source contrôlée) | [`reports/rappor … [208 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('/tmp/eval-pl.json'))\nfor lg,m in d['par_langue'].items():\n    a=m['attachement']; s=m['syntagme']\n    print(lg, 'cibles',a['cibles'],'labels',a['labels'],'exact',a['exact'],\n          'exact_taux',a['exact_taux'],'cov',a['couverture' … [441 caractères tronqués]`

  ```
en cibles 88 labels 87 exact 87 exact_taux 0.9886 cov 0.9886 span 1.0 topk 87 topk_taux 0.9886
  syn tp/fp/fn 586 66 116
  ctrl {'nom': 'cible exacte tirée au hasard dans le gold de la langue', 'graine': 0, 'cibles': 88, 'exact_taux': 0.0227}
fr cibles 151 labels 151 exact 151 exact_taux 1.0 cov 1.0 span 1.0 topk 149 topk_taux 0.9868
  syn tp/fp/fn 894 337 267
  ctrl {'nom': 'cible exacte tirée au hasard dans le gold de la langue', 'graine': 0, 'cibles': 151, 'exact_taux': 0.0199}
global {'cibles': 239, 'labels': 238, 'exact': 238, 'exact_taux': 0.9958, 'couverture': 0.9958, 'exact_taux_span': 1.0, 'topk': 236, 'topk_taux': 0.9874}
global ctrl {'nom': 'cible exacte tirée au hasard dans le gold', 'graine': 0, 'cibles': 239, 'exact_taux': 0.0167}
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport importlib.util, json, pathlib, subprocess, sys\nRACINE = pathlib.Path('.').resolve()\ncli = json.loads(subprocess.check_output([sys.executable, 'tools/drave.py', 'evaluer', '--par-langue', '--json'], text=True))\nsys.path.insert(0, str(RACINE / 'tools'))\nimpor … [2980 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 32, in <module>
  File "<stdin>", line 22, in resume
KeyError: 'controle_negatif'
[exit code: 1]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport importlib.util, json, pathlib, subprocess, sys\nRACINE = pathlib.Path('.').resolve()\ncli = json.loads(subprocess.check_output([sys.executable, 'tools/drave.py', 'evaluer', '--par-langue', '--json'], text=True))\nsys.path.insert(0, str(RACINE / 'tools'))\nimpor … [3201 caractères tronqués]`

  ```
reports/evaluer-langue.json 7868
en {'phrases': 210, 'tokens': 1148, 'pos': {'exactitude': 0.9451, 'exactitude_ferme': 0.983, 'exactitude_ouvert': 0.9054}, 'syntagme': {'precision': 0.8988, 'rappel': 0.8348, 'f1': 0.8656, 'tp': 586, 'fp': 66, 'fn': 116}, 'tete': {'precision': 0.9893, 'rappel': 0.9188, 'f1': 0.9527}, 'attachement': {'cibles': 88, 'labels': 87, 'exact': 87, 'couverture': 0.9886, 'exact_taux': 0.9886, 'exact_taux_span': 1.0, 'topk': 87, 'topk_taux': 0.9886}, 'pragmatique': {'acte': 0.9952, 'negation': 1.0, 'modalite': 0.9857, 'double_sens': 0.9952}, 'fraction_semantique': 0.4954, 'controle_negatif': {'nom': 'cible exacte tirée au hasard dans le gold de la langue', 'graine': 0, 'cibles': 88, 'exact_taux': 0.0227}}
fr {'phrases': 402, 'tokens': 2031, 'pos': {'exactitude': 0.8159, 'exactitude_ferme': 0.9092, 'exactitude_ouvert': 0.7325}, 'syntagme': {'precision': 0.7262, 'rappel': 0.77, 'f1': 0.7475, 'tp': 894, 'fp': 337, 'fn': 267}, 'tete': {'precision': 0.8893, 'rappel': 0.8579, 'f1': 0.8733}, 'attachement': {'cibles': 151, 'labels': 151, 'exact': 151, 'couverture': 1.0, 'exact_taux': 1.0, 'exact_taux_span': 1.0, 'topk': 149, 'topk_taux': 0.9868}, 'pragmatique': {'acte
… [416 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport importlib.util, pathlib, sys\nRACINE=pathlib.Path('.').resolve(); sys.path.insert(0,str(RACINE/'tools'))\nimport bloc_linguistique as bl\nspec=importlib.util.spec_from_file_location('eg', RACINE/'tools/tests/linguistique/evaluer_gold.py')\neg=importlib.util.mod … [862 caractères tronqués]`

  ```
hand+reel  fr n=242 tok=1332 POS=0.8408 F1=0.7258 tete=0.8513 att=1.0000 cov=1.0000 span=1.0000
hand+reel  en n=210 tok=1148 POS=0.9451 F1=0.8656 tete=0.9527 att=0.9886 cov=0.9886 span=1.0000
reel seul  fr n=228 tok=1258 POS=0.8410 F1=0.7158 tete=0.8449 att=1.0000 cov=1.0000 span=1.0000
reel seul  en n=204 tok=1117 POS=0.9436 F1=0.8638 tete=0.9516 att=1.0000 cov=1.0000 span=1.0000
hand seul  fr n= 14 tok=  74 POS=0.8378 F1=0.8889 tete=0.9639 att=1.0000 cov=1.0000 span=1.0000
hand seul  en n=  6 tok=  31 POS=1.0000 F1=0.9375 tete=1.0000 att=0.6667 cov=0.6667 span=1.0000
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "le français ajoute **160 phrases synthétiques** au lexique disjoint. Le contrôle sur le seul\ngold réel (`hand` + `reel`) donne encore l'anglais devant (POS 94,51 contre 84,08 ; F1 86,56\ncontre 72 … [725 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-evaluer-langue.md", "content": "# J11.2 — la mesure par langue : l'anglais devant, mais le gold n'est pas le même\n\n> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Tâche** : **J11.2** ·\n> **Date** : 202 … [6632 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-evaluer-langue.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\np=json.load(open('tools/chantier/plan.json'))\nfor t in p['taches']:\n    if t['id']=='J11.2': print(json.dumps(t, ensure_ascii=False, indent=1))\nprint('keys plan', list(p))\nEOF\ngit status --short tools/chantier/plan.json", "description": "Inspect task … [16 caractères tronqués]`

  ```
{
 "id": "J11.2",
 "jour": 11,
 "titre": "Le produit — la mesure par langue",
 "mandat": "Tâche J11.2 : ajouter `evaluer --par-langue` (le détail fr/en) et le documenter dans `docs/produit/README.md` ; test dans `tools/tests/test_produit.py` ; fiche `reports/rapport-evaluer-langue.md` + JSON, commit.",
 "budget_min": 90,
 "acceptation": [
  {
   "commande": "python3 tools/drave.py evaluer --par-langue >/dev/null 2>&1; echo PL-$?",
   "attendu": "PL-0"
  },
  {
   "commande": "python3 tools/tests/test_produit.py 2>&1 | tail -1",
   "attendu": "OK"
  }
 ]
}
keys plan ['nom', 'principe', 'taches']
 M tools/chantier/plan.json
  ```

- **bash** `{"command": "date '+%Y-%m-%d %H h %M (%Z)'", "description": "Current local time"}`

  ```
2026-11-14 04 h 37 (EST)
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 105}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
1: # En ce moment
2: 
3: **Mis à jour : 2026-11-14, 04 h 25 HNE (heure locale, EST).**
4: 
5: > **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
6: > plan plus bas (**La carte**).
7: 
8: ### Session `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — le hub de reprise du 04/11
9: 
10: - **Id** : `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — [`plan.md`](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/plan.md).
11: - **Rôle** : **Hub de reprise** — état, docs, intégration, passe.
12: - **Fait** : index réparé ; **N3 intégré** ; N2/S/L actifs ; suivi docs (revue, liens, tableaux).
13: - **Prochaine action** : **suivi docs**, puis la **passe** après les runs.
14: - **Bloquants** : aucun.
15: - **Journal** : [la session](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/).
16: 
17: ## Sessions en cours
18: 
19: > Contrat : [`continuite.md`](../methode/continuite.md) · sessions terminées :
20: > [`journal/sessions/`](../../journal/sessions/). Chaque session expose son mandat dans son
21: > `plan.md` (`python3 tools/sessions
… [8551 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**Mis à jour : 2026-11-14, 04 h 38 HNE (heure locale, EST).**", "old_string": "**Mis à jour : 2026-11-14, 04 h 25 HNE (heure locale, EST).**"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**J11.1** (5/5 blocs rejoués, 4 corrigés ; [fiche](../../reports/rapport-exemples-rejoues.md)) ; **J11.2** (`evaluer --par-langue`, fr/en ; [fiche](../../reports/rapport-evaluer-langue.md)) ; ** … [177 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **J11.1** : **5/5**, **4 corrigés** ; `r035` prédit, refus **3** ; F1 **0,7902**, attachement **238/238** (238/239) ; [fiche](../../reports/rapport-exemples-rejoues.md) + JSON.\n- **J11.2** :  … [435 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "| fichiers / JSON de résultats | **726** / **820** | `reports/*.md` / `reports/*.json` |", "old_string": "| fichiers / JSON de résultats | **725** / **819** | `reports/*.md` / `reports/*.json` | … [2 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**B13 : 183/183, gold 432, r035 + convention GV (0,7902), s065 (238/239), g017 rejeté, schéma v2, restitution v1 (canonique 46/46, strict 0,1087), J11.1 (exemples rejoués), J11.2 (par-langue)**  … [392 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**J14.1** — passe + tag ; **J11.3–J11.4** — produit, Panini, table.", "old_string": "**J14.1** — passe + tag ; **J11.2–J11.4** — produit, Panini, table."}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**J9.1** passe d'honnêteté (**19** fiches ; [fiche](../../reports/rapport-passe-honnetete.md)) ; **J11.2** par-langue ([fiche](../../reports/rapport-evaluer-langue.md)) ; [restitution v0](../../ … [288 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "limit": 18, "offset": 68}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md</path>
<type>file</type>
<content>
68: `r241`), le refus sort en **3** et `r035` — l'ancien échec connu — rend exactement le gold
69: (`REL [9:24] « she talks about » → film`). Le seul bloc identique est `g011`. F1 **0,7902**,
70: attachement **238/238 labels** (238/239 cibles, 0,9958) ; le mandat 237/238 est l'état d'avant
71: `s065`. Le contrôle négatif (mutation d'un token dans une copie de la doc) est détecté 4/5.
72: [`fiche`](../../reports/rapport-exemples-rejoues.md) + JSON. La suite produit est **J11.2**
73: (`evaluer --par-langue`), **J11.3** (50 textes libres), **J11.4** (schéma v2 documenté).
74: 
75: **La vue d'ensemble des chantiers** — huit chantiers (A, B, N, R, **S**, **L**, **D**, B13), leurs relations, leurs chemins critiques et les tensions à trancher — est dans [`chantiers.md`](chantiers.md) ; la carte est [`chantiers-vision.svg`](../schemas/chantiers-vision.svg) ; le **plan de travail multi-sessions** (qui fait quoi, où, à quelle cadence) est dans [`plan-travail.md`](plan-travail.md). Les demandes des 48 h y sont reliées à ce qu'elles ont déplacé.
76: 
77: ## L'ordre du jour (carpe d
… [768 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "new_string": "[`fiche`](../../reports/rapport-exemples-rejoues.md) + JSON. La suite produit est **J11.2**\n(`evaluer --par-langue`), **J11.3** (50 textes libres), **J11.4** (schéma v2 documenté).\n\n**J11.2 —  … [1036 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -40; echo \"code=${PIPESTATUS[0]}\"", "description": "Run documentation review"}`

  ```
revue de documentation · 726 fiche(s) · 820 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
code=0
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -20; echo \"code=${PIPESTATUS[0]}\"; echo \"=== en-cours ===\"; python3 tools/verifie_en_cours.py 2>&1 | tail -15; echo \"code=${PIPESTATUS[0]}\"", "description": "Check doc budget and state"}`

  ```
3072    341 DATÉ      0  docs/implantation/convertisseur.md
    2962    364   T1   5000  docs/theorie/glossaire/02-modeles-et-architectures.md
    2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2746    203   T1   2800  reports/README.md
    2450    166   T1   2500  docs/pilotage/references-non-regression.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4043 mots (budget 4 000)

  avertissements :
     · 49 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-f
… [273 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"T0\\|tâche\\|tache\\|en-cours\\|4000\" tools/taille_documents.py | head -40", "description": "Inspect context budget tool"}`

  ```
5:  1. la taille des documents **chargeables** (T0/T1) en mots, avec un budget par catégorie ;
27:    ("T0", "AGENTS.md", 1200),
28:    ("T0", "docs/pilotage/en-cours.md", 2000),
32:    ("T0", "docs/methode/*.md", 1200),
112:            if cat in ("T0", "T1"):
140:    # T0 : la somme des trois lectures par défaut
145:    # Le T0 est « AGENTS + en-cours + UN document de tâche », et le document de tâche est un
146:    # T0 (≤ 1 200 mots) : les trois documents `specifiques` ci-dessus sont des T1, avec leur
147:    # propre budget. Les compter ici faisait payer 1 579 mots au T0 (organisation-du-depot.md)
148:    # au lieu des 1 134 du plus gros T0 — un budget faux de 445 mots, dans le sens qui bloque.
150:    t0 = poids("AGENTS.md") + poids("docs/pilotage/en-cours.md") + max(
153:    if t0 > 4000:
154:        violations.append(f"T0 : {t0} mots (AGENTS + en-cours + une tâche) > budget 4 000")
163:    print(f"  T0 max : {t0} mots (budget 4 000)")
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport re, pathlib\ndef poids(p):\n    t=pathlib.Path(p).read_text(encoding='utf-8')\n    # likely script uses split()\n    return len(t.split())\nfor f in ['AGENTS.md','docs/pilotage/en-cours.md']:\n    print(f, poids(f))\nEOF\nsed -n '140,156p' tools/taille_document … [44 caractères tronqués]`

  ```
AGENTS.md 1196
docs/pilotage/en-cours.md 1673
    # T0 : la somme des trois lectures par défaut
    def poids(rel: str) -> int:
        q = RACINE / rel
        return mots_hors_diagrammes(q.read_text(encoding="utf-8", errors="ignore")) if q.exists() else 0

    # Le T0 est « AGENTS + en-cours + UN document de tâche », et le document de tâche est un
    # T0 (≤ 1 200 mots) : les trois documents `specifiques` ci-dessus sont des T1, avec leur
    # propre budget. Les compter ici faisait payer 1 579 mots au T0 (organisation-du-depot.md)
    # au lieu des 1 134 du plus gros T0 — un budget faux de 445 mots, dans le sens qui bloque.
    agents = [a for a in (RACINE / "docs/methode").glob("*.md") if a.name not in specifiques]
    t0 = poids("AGENTS.md") + poids("docs/pilotage/en-cours.md") + max(
        (poids(str(a.relative_to(RACINE))) for a in agents), default=0
    )
    if t0 > 4000:
        violations.append(f"T0 : {t0} mots (AGENTS + en-cours + une tâche) > budget 4 000")

    # classement
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **J11.1/J11.2** : 5/5 blocs rejoués, `r035` prédit ; `--par-langue` fr/en ; F1 **0,7902**, att. **238/239** ; [J11.1](../../reports/rapport-exemples-rejoues.md), [J11.2](../../reports/rapport- … [470 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**J9.1** passe d'honnêteté (**19** fiches ; [fiche](../../reports/rapport-passe-honnetete.md)) ; [restitution v0](../../reports/rapport-restitution-v0.md), [g017](../../reports/rapport-g017.md). … [288 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**J11.1–J11.2** (produit : [exemples](../../reports/rapport-exemples-rejoues.md), [par-langue](../../reports/rapport-evaluer-langue.md)) ; **contrat v1**, **`drave` v0**.", "old_string": "**J11. … [219 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**B13 : 183/183, gold 432, r035 + convention GV (0,7902), s065 (238/239), g017 rejeté, schéma v2, restitution v1 (canonique 46/46, strict 0,1087), J11.1–J11.2 (produit)** | **J11.3–J11.4** (prod … [389 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | grep -E \"T0 max|violation|T0 :\"; echo \"code=${PIPESTATUS[0]}\"", "description": "Recheck context budget"}`

  ```
T0 max : 3994 mots (budget 4 000)
code=0
  ```

- **bash** `{"command": "python3 tools/verifie_en_cours.py 2>&1 | tail -4; echo \"code=${PIPESTATUS[0]}\"", "description": "Recheck state file"}`

  ```
en-cours · 1624 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
code=0
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -4; echo \"code=${PIPESTATUS[0]}\"; python3 tools/verifie_en_cours.py >/dev/null 2>&1; echo \"encours=$?\"; python3 tools/verifier_schemas.py 2>&1 | tail -3; echo \"schemas=${PIPESTATUS[0]}\"", "description": "Doc review, state, schemas"}`

  ```
revue de documentation · 726 fiche(s) · 820 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
code=0
encours=0
  schémas · 463 document(s) · 67 SVG · 2 source(s)
  ✅ aucun ASCII art, SVG valides et référencés, blocs PlantUML inline valides,
     sources et images relatives.
schemas=0
  ```

- **bash** `{"command": "bash tools/porte-tableaux.sh 2>&1 | tail -5; echo \"tableaux=${PIPESTATUS[0]}\"", "description": "Run tables gate"}`

  ```
✅ 1791 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4125 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-14)
tableaux=0
  ```

- **bash** `{"command": "python3 tools/tests/test_produit.py 2>&1 | tail -3", "description": "Run product tests again"}`

  ```
Ran 18 tests in 7.492s

OK
  ```

- **bash** `{"command": "bash tools/porte-produit.sh", "description": "Run product gate", "run_in_background": true}`

  ```
started background job bash-51
  ```

- **bash** `{"command": "git status --short | sed -n '1,80p'; echo \"=== staged names ===\"; git diff --cached --name-only | head -40; echo \"=== unstaged journal stat ===\"; git diff --stat -- journal | tail -20", "description": "Inspect dirty working tree"}`

  ```
M docs/pilotage/en-cours.md
 M docs/pilotage/roadmap.md
 M docs/produit/README.md
MM journal/2026-11-14/README.md
MM journal/2026-11-14/docs.md
MM journal/2026-11-14/memoire.md
MM journal/2026-11-14/mesures.md
MM journal/2026-11-14/portes.md
MM journal/README.md
MM journal/THEMES.md
MM journal/sessions/MANIFEST.md
MM journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
MM journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
D  journal/sessions/session-b0a87524-43a4-4935-a248-72c1d42c8471/digest.md
D  journal/sessions/session-b0a87524-43a4-4935-a248-72c1d42c8471/rapport.md
MM journal/sessions/session-ce875934-0cf6-4434-a91d-cbca647b11b3/digest.md
MM journal/sessions/session-ce875934-0cf6-4434-a91d-cbca647b11b3/rapport.md
 M reports/INDEX.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/plan.json
 M tools/drave.py
 m tools/structures
 M tools/tests/test_produit.py
?? journal/sessions/session-b0a87524-4
… [1634 caractères tronqués]
  ```

- **bash** `{"command": "ls -la journal/2026-11-14/; sed -n '1,80p' journal/2026-11-14/README.md", "description": "Inspect journal day files"}`

  ```
total 24
drwxr-xr-x. 1 stephane stephane   90 14 nov 01:58 .
drwxr-xr-x. 1 stephane stephane  972 14 nov 00:51 ..
-rw-r--r--. 1 stephane stephane 3205 14 nov 04:31 docs.md
-rw-r--r--. 1 stephane stephane 1208 14 nov 04:31 memoire.md
-rw-r--r--. 1 stephane stephane 2013 14 nov 04:31 mesures.md
-rw-r--r--. 1 stephane stephane 1633 14 nov 04:31 portes.md
-rw-r--r--. 1 stephane stephane 7633 14 nov 04:31 README.md
# 2026-11-14

> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
> [`journal/2026-11-14/`](README.md). Le récit écrit à la main est conservé plus bas, dans
> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
> [l'index des sessions](../README.md#sessions).

**11 commits** · **1 session(s)** · **4 thème(s)**

## Thèmes du jour

| thème | commits | fichier |
|---|---|---|
| docs | 3 | [docs.md](docs.md) |
| memoire | 2 | [memoire.md](memoire.md) |
| mesures | 4 | [mesures.md](mesures.md) |
| portes | 2 | [portes.md](portes.md) |

## Sessions DSH

| session | titre | début | durée | liens |
|---|---|---|---|---|
| `e181ce02-cd50-488a-a6be-e84b79d40dcc` | Documentation Drave avec diagrammes et implémentation | 2026-10-3
… [5187 caractères tronqués]
  ```

- **bash** `{"command": "git diff -- journal/2026-11-14/README.md | head -80; echo \"=== cached diff ===\"; git diff --cached -- journal/2026-11-14/README.md | head -60", "description": "Inspect journal diff"}`

  ```
diff --git a/journal/2026-11-14/README.md b/journal/2026-11-14/README.md
index a5012ccd..4d99d6bb 100644
--- a/journal/2026-11-14/README.md
+++ b/journal/2026-11-14/README.md
@@ -5,22 +5,22 @@
 > le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
 > [l'index des sessions](../README.md#sessions).
 
-**9 commits** · **1 session(s)** · **4 thème(s)**
+**11 commits** · **1 session(s)** · **4 thème(s)**
 
 ## Thèmes du jour
 
 | thème | commits | fichier |
 |---|---|---|
 | docs | 3 | [docs.md](docs.md) |
-| memoire | 1 | [memoire.md](memoire.md) |
-| mesures | 3 | [mesures.md](mesures.md) |
+| memoire | 2 | [memoire.md](memoire.md) |
+| mesures | 4 | [mesures.md](mesures.md) |
 | portes | 2 | [portes.md](portes.md) |
 
 ## Sessions DSH
 
 | session | titre | début | durée | liens |
 |---|---|---|---|---|
-| `e181ce02-cd50-488a-a6be-e84b79d40dcc` | Documentation Drave avec diagrammes et implémentation | 2026-10-31 17:40 | 323.3 h | [rapport](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md) · [digest](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md) |
+| `e181ce02-cd50-488a-a6be-e84b79d40dcc` | Documentation Drave avec diagrammes et i
… [3147 caractères tronqués]
  ```

- **bash** `{"command": "ls .git/hooks/ | grep -v sample; echo \"=== pre-commit ===\"; sed -n '1,120p' .git/hooks/pre-commit 2>/dev/null", "description": "Inspect git hooks"}`

  ```
pre-commit
=== pre-commit ===
#!/bin/sh
# pre-commit — l'état accompagne le fait, le journal accompagne le code.
#
# Versionné dans tools/hooks/ et installé par tools/installe_hooks.sh : un hook qui
# ne vit que dans .git/hooks ne survit ni au clone ni au nettoyage.
set -u
cd "$(git rev-parse --show-toplevel)" || exit 0

# 1. Aucun fait (reports/, roadmap, backlog) ne se commite sans sa ligne d'état.
#    C'est la garantie de fraîcheur de docs/pilotage/en-cours.md : elle ne dépend
#    pas de la survie d'une session « principale », elle est vérifiée au commit.
if ! python3 tools/verifie_etat_a_jour.py --index; then
    echo "  ⛔ commit refusé : un fait sans ligne d'état."
    echo "     mets docs/pilotage/en-cours.md à jour, puis :"
    echo "     git add docs/pilotage/en-cours.md"
    exit 1
fi

# 2. Archive les traces de session DSH avant chaque commit : le journal doit
#    accompagner le code, pas le suivre.
python3 tools/archive_sessions.py --quiet >/dev/null || { echo "  ⛔ archivage des sessions en échec"; exit 1; }
python3 tools/session_report.py --quiet >/dev/null || { echo "  ⛔ rapport de session en échec"; exit 1; }
# Le journal du jour, par thème (sources : git + journal
… [264 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-51", "wait": true, "timeout_ms": 120000}`

  ```
✅ version : drave 0.1.0
  ✅ analyser fr : JSON valide, étiquettes et syntagmes
  ✅ analyser en : JSON valide, étiquettes et syntagmes
  ✅ rejeu : sha256 f4b7822076a4203d deux fois
  ✅ smoke test : Ran 18 tests
  ✅ schéma v2 validé (5 cas v2 + 1 cas v1 + 20 phrases du gold)
  ✅ 50 textes libres : Ran 4 tests
  ✅ restitution v0 : surface exacte (miroir affiché)
  ✅ restitution v1 : forme canonique exacte, miroir strict distinct
  ✅ restitution v0/v1 : Ran 22 tests
  ✅ schéma v2 : Ran 8 tests
  ✅ refus : JSON avec refus, code 3
[status: running]
  ```

- **bash** `{"command": "git diff -- tools/drave.py tools/tests/test_produit.py | sed -n '1,220p'", "description": "Review code diff"}`

  ```
diff --git a/tools/drave.py b/tools/drave.py
index 371473c5..9dc37b89 100644
--- a/tools/drave.py
+++ b/tools/drave.py
@@ -252,7 +252,7 @@ def _formater_evaluation(rapport: dict) -> str:
     att_tete = mesure["attachement_tete"]
     prag = mesure["pragmatique"]
     controle = rapport["controle_negatif"]
-    return "\n".join([
+    lignes = [
         f"{NOM} {VERSION} — évaluation de l'heuristique sur le gold",
         f"gold {gold['nom']} · {gold['phrases']} phrases · {gold['tokens']} tokens · "
         f"{gold['cibles_attachement']} cibles d'attachement",
@@ -274,7 +274,26 @@ def _formater_evaluation(rapport: dict) -> str:
         f"FRACTION SÉMANTIQUE {_pct(mesure['fraction_semantique'])}",
         f"CONTRÔLE NÉGATIF cible exacte tirée au hasard {_pct(controle['exact_taux'])} "
         f"(graine {controle['graine']}, {controle['cibles']} cibles)",
-    ])
+    ]
+    par_langue = rapport.get("par_langue") or {}
+    if par_langue:
+        lignes += ["", "PAR LANGUE"]
+        for langue, m in par_langue.items():
+            p, s, a, c = m["pos"], m["syntagme"], m["attachement"], m["controle_negatif"]
+            pr = m["pragmatique"]
+            lignes += [
+       
… [5222 caractères tronqués]
  ```

### 👤 Utilisateur

background job bash-51 (bash: bash tools/porte-produit.sh) finished [status: completed, exit code: 0]. Read its output with job_output.

- **job_output** `{"job_id": "bash-51", "timeout_ms": 1000}`

  ```
✅ autotest parallèle : 183/183 portes tenues
✅ porte produit verte
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "sed -n '1,80p' tools/toutes-les-portes.sh; wc -l tools/toutes-les-portes.sh", "description": "Inspect all gates script"}`

  ```
#!/bin/bash
# toutes-les-portes.sh — LA PASSE COMPLÈTE, et l'instrument qui manquait.
#
# POURQUOI CETTE PORTE EXISTE. Le 12 octobre, `tools/porte-gain.sh` §9 exigeait un REFUS
# (`--attn-window` en réparti) que le v7 avait **délibérément retiré** en faisant voyager les
# trois réglages dans la trame (`main.rs:4432`). La porte ne pouvait donc plus passer — et
# personne ne l'a vu, parce que les portes étaient lancées **une par une**, à la main, quand
# on touchait la fonctionnalité du jour. Une porte qu'on croit verte et qui n'a pas tourné est
# exactement le défaut que ce dépôt traque (un drapeau inerte, une mesure qui ne mesure rien) :
# ici, appliqué aux instruments eux-mêmes.
#
# Ce que fait ce script, et ce qu'aucun autre ne faisait :
#   1. il lance **TOUTES** les `tools/porte-*.sh`, séquentiellement ;
#   2. il ne s'arrête PAS à la première rouge — il veut le tableau, pas la première tuile ;
#   3. il borne chaque porte dans le temps (`DELAI`, 1800 s par défaut) : une porte qui pend
#      est une porte ROUGE, pas une porte qu'on attend ;
#   4. il garde le journal de chacune (`JOURNAUX`) et n'affiche qu'une ligne par porte ;
#   5. il sort en 1 s'il y a la moindre rouge, en
… [2830 caractères tronqués]
  ```

- **bash** `{"command": "git add tools/drave.py tools/tests/test_produit.py docs/produit/README.md docs/pilotage/en-cours.md docs/pilotage/roadmap.md reports/rapport-evaluer-langue.md reports/evaluer-langue.json && git status --short | sed -n '1,40p'", "description": "Stage task files"}`

  ```
M  docs/pilotage/en-cours.md
M  docs/pilotage/roadmap.md
M  docs/produit/README.md
MM journal/2026-11-14/README.md
MM journal/2026-11-14/docs.md
MM journal/2026-11-14/memoire.md
MM journal/2026-11-14/mesures.md
MM journal/2026-11-14/portes.md
MM journal/README.md
MM journal/THEMES.md
MM journal/sessions/MANIFEST.md
MM journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
MM journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
D  journal/sessions/session-b0a87524-43a4-4935-a248-72c1d42c8471/digest.md
D  journal/sessions/session-b0a87524-43a4-4935-a248-72c1d42c8471/rapport.md
MM journal/sessions/session-ce875934-0cf6-4434-a91d-cbca647b11b3/digest.md
MM journal/sessions/session-ce875934-0cf6-4434-a91d-cbca647b11b3/rapport.md
 M reports/INDEX.md
A  reports/evaluer-langue.json
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
A  reports/rapport-evaluer-langue.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/plan.json
M  tools/drave.py
 m tools/structures

… [132 caractères tronqués]
  ```

- **bash** `{"command": "git commit -m \"J11.2 — EVALUER --PAR-LANGUE : FR 0,8159/0,7475 (151/151), EN 0,9451/0,8656 (87/88), GLOBAL INCHANGÉ\" -m \"evaluer --par-langue rejoue la même mesure sur les deux sous-golds et publie le\ndétail fr/en (texte et clé par_langue du JSON) : phrases, tokens, POS, syntagmes,\ … [1078 caractères tronqués]`

  ```
[stderr]
  ✅ index : aucun fait stagé sans état
[still running after 60000ms; moved to background job bash-59]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **job_output** `{"job_id": "bash-59", "timeout_ms": 240000, "wait": true}`

  ```
[s/v7 09e54143] J11.2 — EVALUER --PAR-LANGUE : FR 0,8159/0,7475 (151/151), EN 0,9451/0,8656 (87/88), GLOBAL INCHANGÉ
 21 files changed, 2957 insertions(+), 56 deletions(-)
 create mode 100644 journal/sessions/session-9d3b2074-c5f0-4f11-be10-31d317bac657/digest.md
 create mode 100644 journal/sessions/session-9d3b2074-c5f0-4f11-be10-31d317bac657/rapport.md
 create mode 100644 reports/evaluer-langue.json
 create mode 100644 reports/rapport-evaluer-langue.md
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "git show --stat --oneline HEAD | sed -n '1,40p'; echo \"=== status ===\"; git status --short | sed -n '1,40p'", "description": "Verify commit and remaining status"}`

  ```
09e54143 J11.2 — EVALUER --PAR-LANGUE : FR 0,8159/0,7475 (151/151), EN 0,9451/0,8656 (87/88), GLOBAL INCHANGÉ
 docs/pilotage/en-cours.md                          |   12 +-
 docs/pilotage/roadmap.md                           |   10 +
 docs/produit/README.md                             |   66 +-
 journal/2026-11-14/README.md                       |    7 +-
 journal/2026-11-14/docs.md                         |    2 +-
 journal/2026-11-14/memoire.md                      |    2 +-
 journal/2026-11-14/mesures.md                      |    8 +-
 journal/2026-11-14/portes.md                       |    2 +-
 journal/README.md                                  |    5 +-
 journal/THEMES.md                                  |    2 +-
 journal/sessions/MANIFEST.md                       |    7 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md |   12 +
 .../rapport.md                                     |   14 +-
 .../digest.md                                      | 1883 ++++++++++++++++++++
 .../rapport.md                                     |  192 ++
 .../digest.md                                      |  147 ++
 .../rapport.md                                     |   61 +-
 reports/evaluer-lan
… [694 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -3; echo \"revue=${PIPESTATUS[0]}\"; python3 tools/verifie_en_cours.py 2>&1 | tail -3; echo \"encours=${PIPESTATUS[0]}\"", "description": "Post-commit doc review and state"}`

  ```
revue de documentation · 726 fiche(s) · 820 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
revue=0
  en-cours · 1624 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
encours=0
  ```

- **bash** `{"command": "python3 tools/verifie_journal.py 2>&1 | tail -8; echo \"journal=${PIPESTATUS[0]}\"; python3 tools/taille_documents.py 2>&1 | grep \"T0 max\"; echo \"budget=${PIPESTATUS[0]}\"", "description": "Journal and budget checks"}`

  ```
journal · 46 jour(s) · 187 session(s) · 2475 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
journal=0
  T0 max : 3994 mots (budget 4 000)
budget=0
  ```

- **bash** `{"command": "python3 tools/drave.py evaluer --par-langue >/dev/null 2>&1; echo PL-$?; python3 tools/tests/test_produit.py 2>&1 | tail -1", "description": "Acceptance commands"}`

  ```
PL-0
OK
  ```

### 🤖 Assistant

**J11.2 terminé et committé** — `09e54143`

## Ce qui a été ajouté

- **`evaluer --par-langue`** dans [`tools/drave.py`](tools/drave.py) : rejoue la même mesure sur les sous-golds **fr** et **en**, en texte (`PAR LANGUE`) et en JSON (`par_langue`), avec un **contrôle négatif recalculé par langue**.
- **Documentation** dans [`docs/produit/README.md`](docs/produit/README.md) : § 3.3 (sortie actuelle + bloc par langue + lecture), § 7 (syntaxe et tableau des options), lien vers la fiche.
- **Tests** dans [`tools/tests/test_produit.py`](tools/tests/test_produit.py) : `TestParLangue` (JSON, texte, non-régression de la mesure globale, cohérence des comptes). **18 tests OK**.
- **Fiche + JSON** : [`reports/rapport-evaluer-langue.md`](reports/rapport-evaluer-langue.md), [`reports/evaluer-langue.json`](reports/evaluer-langue.json).
- **État/roadmap** : `en-cours` et `roadmap` à jour, J11.2 marqué, suite = J11.3–J11.4.

## Les chiffres

| langue | phrases | tokens | POS | F1 | attachement | top-k |
|---|---:|---:|---:|---:|---:|---:|
| **fr** | 402 | 2 031 | **0,8159** | **0,7475** | **151/151** | 0,9868 |
| **en** | 210 | 1 148 | **0,9451** | **0,8656** | **87/88** (span 87/87) | 0,9886 |
| global | 612 | 3 179 | 0,8625 | **0,7902** | **238/239** | 0,9874 |

**Contrôle négatif** : cible exacte au hasard **1,99 %** (fr), **2,27 %** (en), **1,67 %** (tout), graine 0.

**Le point de méthode** : l'anglais est devant, mais son gold est **100 % réel** quand le français ajoute **160 synthétiques**. Sur le réel seul l'écart tient (POS 0,9451 contre 0,8408 ; F1 0,8656 contre 0,7258), donc il reste **confondu avec la source** — la fiche le dit explicitement.

## Vérifications

- `python3 tools/drave.py evaluer --par-langue` → **PL-0**
- `python3 tools/tests/test_produit.py` → **OK**, 18 tests
- `bash tools/porte-produit.sh` → **verte**, 183/183 autotest
- Revue de documentation, tableaux, schémas, journal, budget T0 (3 994/4 000) → **verts**

Les modifications préexistantes hors périmètre (`reports/INDEX.md`, `tools/chantier/plan.json`, `tools/structures`, etc.) n'ont pas été touchées.

