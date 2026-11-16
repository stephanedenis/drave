# Session DSH — relecture

- identifiant : `session-8217267f-fd89-462c-8112-cba3ba9877b3`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-15 21:37:29
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche T1 (exploitable, 1/5) : **l'empaquetage** — écris un **`pyproject.toml`** minimal (le nom `drave`, la version 0.1.0, le `requires-python >= 3.10`, **aucune dépendance**, le `console_scripts` `drave = tools.drave:main` ou un module d'entrée propre), vérifie `python3 -m pip install -e .` dans un **venv temporaire** (`/tmp/venv-drave`), puis `drave --version` et `drave analyser "Le chat dort."` depuis un **autre répertoire** (pas la racine du dépôt) ; le contrôle négatif : sans install, `drave` doit échouer proprement. Fiche `reports/rapport-empaquetage.md` + JSON, un test dans `tools/tests/` (ou une note), et la doc `docs/produit/README.md` § 8.10 mise à jour (l'install). **Ne casse pas** `python3 tools/drave.py` (le chemin historique).

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

### 🤖 Assistant

I'll start by exploring the repository structure and understanding the existing code.

- **bash** `{"command": "pwd && ls -la", "description": "List repository root contents"}`

  ```
/home/stephane/Data13TB/stephane/GitHub/Qtrinet
total 208
drwxr-xr-x. 1 stephane stephane   686  6 nov 09:52 .
drwxr-xr-x. 1 stephane stephane  2532  5 nov 10:41 ..
-rw-r--r--. 1 stephane stephane  9977  3 nov 09:19 AGENTS.md
drwxr-xr-x. 1 stephane stephane    40 25 sep 15:38 bench
drwxr-xr-x. 1 stephane stephane    56 30 sep 12:20 colab
drwxr-xr-x. 1 stephane stephane  2664  2 nov 18:33 data
drwxr-xr-x. 1 stephane stephane   138 15 nov 06:29 docs
drwxr-xr-x. 1 stephane stephane    92 28 oct 16:25 drave-core
drwxr-xr-x. 1 stephane stephane   220 15 nov 21:37 .git
-rw-r--r--. 1 stephane stephane   619 31 oct 17:33 .gitignore
-rw-r--r--. 1 stephane stephane   225  1 nov 10:50 .gitmodules
drwxr-xr-x. 1 stephane stephane   992 15 nov 12:34 journal
drwxr-xr-x. 1 stephane stephane   100  3 nov 09:12 models
drwxr-xr-x. 1 stephane stephane   114 25 sep 15:24 __pycache__
drwxr-xr-x. 1 stephane stephane    64  6 nov 09:52 .pytest_cache
-rw-r--r--. 1 stephane stephane  4992 25 sep 10:54 Qtrinet-bootstrap.md
-rw-r--r--. 1 stephane stephane 21293  6 nov 22:32 README.md
drwxr-xr-x. 1 stephane stephane 78772 15 nov 14:25 reports
-rw-r--r--. 1 stephane stephane 13100 28 oct 14:59 REPRISE.md
-rw---
… [971 caractères tronqués]
  ```

- **bash** `{"command": "git status --short && git log --oneline -5", "description": "Show git status and recent commits"}`

  ```
M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/plan.json
?? reports/rapport-s-paragraphes.md
?? tools/tests/linguistique/gold_reel_50.py
71fdf72c CLÔTURE — LE PLAN (51 TÂCHES) ET LE PROTOCOLE OR-ROLES (X2) COMMITTÉS ; L'ÉTAT HORODATÉ
c9067a39 INDEX — RÉGÉNÉRÉ APRÈS LA SEMAINE 2 (W1-W6, X1-X3, Y1)
b8248b2d ÉTAT — T0 VERT (LA LIGNE W5 RACCOURCIE)
75dc9259 ÉTAT — T0 VERT
a1c45477 ÉTAT — T0 TENU (LES LIGNES R ET N RACCOURCIES)
  ```

- **bash** `{"command": "ls -la tools/ | head -60 && echo \"---\" && ls tools/tests/ 2>/dev/null | head -40", "description": "List tools and tests directories"}`

  ```
total 5748
drwxr-xr-x. 1 stephane stephane  18264 15 nov 14:25 .
drwxr-xr-x. 1 stephane stephane    686  6 nov 09:52 ..
-rw-------. 1 stephane stephane   8428 24 oct 21:16 adaptateur_langue.py
-rwx--x--x. 1 stephane stephane  11640  1 oct 04:21 aiguille.py
-rw-r--r--. 1 stephane stephane  80950 19 oct 14:33 aligneur_litteraire.py
-rw-------. 1 stephane stephane   7797  6 oct 22:04 amplification.py
-rw-------. 1 stephane stephane   3848 21 oct 00:56 analyse_alignement.py
-rwx--x--x. 1 stephane stephane   8850  1 oct 17:40 analyse_empreinte.py
-rw-------. 1 stephane stephane   4614  2 oct 17:28 analyse_engram.py
-rwx--x--x. 1 stephane stephane  11086  1 oct 20:13 analyse_experts_statique.py
-rwxr-xr-x. 1 stephane stephane   5449  3 oct 04:19 analyse_flux.py
-rwx--x--x. 1 stephane stephane   6767  3 oct 09:42 analyse_hc.py
-rw-------. 1 stephane stephane   6681 20 oct 08:52 analyse_litteraire.py
-rwx--x--x. 1 stephane stephane   6364  3 oct 08:11 analyse_octets_par_jeton.py
-rwx--x--x. 1 stephane stephane   6029  3 oct 11:51 analyse_reutilisation_experts.py
-rw-------. 1 stephane stephane   5049  3 oct 13:04 analyse_union_experts.py
-rw-------. 1 stephane stephane   4815  7 oct 10:32 
… [3592 caractères tronqués]
  ```

- **bash** `{"command": "ls -la tools/drave.py 2>/dev/null; wc -l tools/drave.py 2>/dev/null; head -80 tools/drave.py 2>/dev/null", "description": "Inspect tools/drave.py entry point"}`

  ```
-rw-------. 1 stephane stephane 61289 15 nov 14:25 tools/drave.py
1254 tools/drave.py
#!/usr/bin/env python3
"""drave.py — le point d'entrée produit du bloc linguistique.

Une seule commande, quatre gestes, hors ligne et déterministe :

    python3 tools/drave.py analyser "Le chat dort."
    python3 tools/drave.py analyser "The cat sleeps on the roof." --langue en --json
    python3 tools/drave.py analyser "Le chat dort." --tagger          # API DeepSeek (clé, réseau)
    python3 tools/drave.py analyser "Le chat dort." --tagger auto     # API si clé, sinon heuristique
    python3 tools/drave.py evaluer
    python3 tools/drave.py evaluer --gold --json
    python3 tools/drave.py evaluer --tagger --json                    # heuristique + cascade API
    python3 tools/drave.py rejouer "Le chat de la voisine qui dort sur le toit se réveille."
    python3 tools/drave.py restituer "Le chat dort."
    python3 tools/drave.py restituer "Le chat dort." --roles
    python3 tools/drave.py restituer --banc reports/pensee-fiabilite-produit.json --json
    python3 tools/drave.py --version

Ce que la commande expose : l'analyse **heuristique** (`Heuristique.analyser`) — POS, syntagmes
avec rôle et 
… [2895 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"def main\\|__main__\\|--version\\|def construire\\|argparse\" tools/drave.py | head -40", "description": "Find main and version handling"}`

  ```
17:    python3 tools/drave.py --version
40:import argparse
412:class _Formateur(argparse.RawDescriptionHelpFormatter):
501:def _lire_entree(args: argparse.Namespace) -> str:
508:def _analyser_jsonl(texte: str, args: argparse.Namespace, h: bl.Heuristique, bloc,
541:def _mode_tagger(args: argparse.Namespace) -> str | None:
553:def cmd_analyser(args: argparse.Namespace) -> int:
758:def cmd_evaluer(args: argparse.Namespace) -> int:
872:def cmd_rejouer(args: argparse.Namespace) -> int:
900:def cmd_restituer(args: argparse.Namespace) -> int:
1027:class _Parseur(argparse.ArgumentParser):
1073:def construire_parseur() -> argparse.ArgumentParser:
1098:    parseur.add_argument("-V", "--version", action="version", version=f"{NOM} {VERSION}",
1134:    analyser.add_argument("--tagger-auto", action="store_true", help=argparse.SUPPRESS)
1159:    evaluer.add_argument("--tagger-auto", action="store_true", help=argparse.SUPPRESS)
1226:def main(argv: list[str] | None = None) -> int:
1253:if __name__ == "__main__":
  ```

- **bash** `{"command": "ls -la pyproject.toml setup.py setup.cfg 2>/dev/null; echo \"---\"; ls docs/produit/ 2>/dev/null; echo \"---\"; ls reports/ | grep -i \"empaquet\\|packag\" | head", "description": "Check existing packaging and docs"}`

  ```
---
exemples.md
README.md
---
  ```

- **bash** `{"command": "sed -n '1027,1254p' tools/drave.py", "description": "Read parser and main functions"}`

  ```
class _Parseur(argparse.ArgumentParser):
    """Un parseur francophone : `-h`, `--help` et `--aide` partout, sans doublon."""

    def __init__(self, *args, **kwargs):
        kwargs["add_help"] = False
        super().__init__(*args, **kwargs)
        self._positionals.title = "arguments"
        self._optionals.title = "options"
        self.add_argument("-h", "--help", "--aide", action="help",
                          help="afficher cette aide et quitter")

    def error(self, message: str) -> None:  # type: ignore[override]
        self.print_usage(sys.stderr)
        self.exit(2, f"{self.prog}: erreur d'usage : {message}\n")


def _normaliser_tagger(argv: list[str]) -> list[str]:
    """`--tagger auto` → `--tagger-auto`, sans avaler le TEXTE qui suit.

    Un `--tagger` à valeur optionnelle (`nargs="?"`) mangerait le texte positionnel quand
    l'utilisateur écrit `analyser --tagger "Le chat dort."`. On garde donc `--tagger` comme
    drapeau et on ne transforme que les deux valeurs explicites `auto` et `api`.
    """
    sortie: list[str] = []
    i = 0
    while i < len(argv):
        jeton = argv[i]
        if jeton == "--tagger" and i + 1 < len(argv) and argv[i + 1] in ("
… [12062 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"8\\.10\\|## 8\\|### 8\" docs/produit/README.md | head -40; echo \"---\"; wc -l docs/produit/README.md", "description": "Locate section 8.10 in product README"}`

  ```
738:## 8. FAQ — dix questions
748:### 8.1 Quelles langues le produit reconnaît-il ?
758:### 8.2 Est-ce que ça marche hors ligne ?
765:### 8.3 Combien ça coûte ?
774:### 8.4 Qu'est-ce que `--tagger` change ?
785:### 8.5 Quel est le format de sortie, et est-il stable ?
795:### 8.6 Que veut dire « attachement », et à quel point est-il fiable ?
806:### 8.7 Pourquoi reste-t-il un span inatteignable ?
816:### 8.8 Que peut-on restituer : la surface, la forme, les rôles ?
827:### 8.9 Quelles limites faut-il connaître avant de s'en servir ?
839:### 8.10 Comment l'installer et le lancer ?
---
871 docs/produit/README.md
  ```

- **bash** `{"command": "sed -n '738,871p' docs/produit/README.md", "description": "Read FAQ section 8 including 8.10"}`

  ```
## 8. FAQ — dix questions

> **Vérifié le 2026-11-15** contre le code courant (`drave 0.1.0`) par
> [`tools/verifier_faq.py`](../../tools/verifier_faq.py) : **10/10** réponses passent et le
> **contrôle négatif** est détecté. Le détail des commandes, les sorties observées et ce qui
> pourrait rendre chaque réponse fausse sont dans
> [`reports/rapport-faq.md`](../../reports/rapport-faq.md) et
> [`reports/faq.json`](../../reports/faq.json). Si le code bouge, relancer
> `python3 tools/verifier_faq.py`.

### 8.1 Quelles langues le produit reconnaît-il ?

Le **bloc** détecte la langue et le script : ses profils UDHR couvrent **398 langues**
(**0,9687** sur l'autotest), mais le **CLI** n'expose que `fr` et `en` comme **indice**
(`--langue`). Sans indice, il rend la langue détectée — `de` pour « Der Hund schläft. », `es`
pour « El perro duerme. » — ou `und` quand la confiance passe sous le seuil (**0,12**) :
« Élodie sourit. » rend `und`, **même avec `--langue fr`**. `--langue` est un **indice**, pas
une contrainte ; `--langue de` sort **2** (usage invalide). Les 398 profils ne sont pas
versionnés : `data/` est hors dépôt.

### 8.2 Est-ce que ça marche hors ligne ?

**Oui, par défaut.** `
… [8466 caractères tronqués]
  ```

- **bash** `{"command": "ls reports/ | head -40; echo \"---\"; ls reports/*.json | head -10; echo \"---\"; grep -l \"contrôle négatif\" reports/*.md | head -5", "description": "Inspect reports conventions"}`

  ```
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
a80-porte-profondeur.json
a80-porte-reflexe.json
a80-porte-reparti.json
a80-portes-ppl.json
a80-porte-topologie.json
a80-porte-trace.json
a83a-coupe.json
a83a-flux.json
a83a-pont.json
a83b-decision.json
a83b-lot.json
a83b-regimes.json
a83c-ctx.json
a83c-lot.json
a83-defaut.json
a83d-lot-threads.json
aiguille-30b.md
aiguille-gpt-oss.md
alignement-3b.json
alignement-7b.json
---
reports/a26-bilan.json
reports/a26-lot-disque.json
reports/a80-audit-final.json
reports/a80-indice-qualifie.json
reports/a80-melange-qualifie.json
reports/a80-pannes-ppl.json
reports/a80-porte-adaptateur.json
reports/a80-porte-budget.json
reports/a80-porte-bus.json
reports/a80-porte-bus-socket.json
---
reports/alignement-verne.md
reports/fiche-nuit-17-10.md
reports/rapport-a26-bilan.m
… [173 caractères tronqués]
  ```

- **bash** `{"command": "ls tools/__init__.py 2>/dev/null || echo \"no tools/__init__.py\"; python3 --version; python3 -m pip --version; echo \"---gitignore---\"; cat .gitignore", "description": "Check package marker, Python and gitignore"}`

  ```
no tools/__init__.py
Python 3.13.16
pip 26.2.2 from /usr/lib/python3.13/site-packages/pip (python 3.13)
---gitignore---
__pycache__/
*.pyc
reports/*.tmp
models/
data/
qtrinet-core/target/

# Traces de session : la copie brute reste sur disque (volumineuse, binaire),
# le digest markdown est versionné.
journal/sessions/*/session*.jsonl.zstd
journal/sessions/archive.log

# Outil de référence : la source est versionnée, le binaire se recompile
# (commande exacte dans tools/ref_logits.md).
tools/ref_logits
target/

# docwatch — SVG générés depuis les sources .puml/.mmd (docwatch les produit)
docs/**/*.puml.svg
docs/**/*.mmd.svg

# Campagnes GPU : points de contrôle et journaux de run (hors dépôt, archivés à part)
work/
  ```

- **bash** `{"command": "grep -n \"RACINE\\|Path(__file__)\\|tests/linguistique\\|data/\" tools/drave.py | head -40", "description": "Check path assumptions in drave.py"}`

  ```
54:RACINE = pathlib.Path(__file__).resolve().parent.parent
55:sys.path.insert(0, str(RACINE / "tools"))
56:sys.path.insert(0, str(RACINE))
633:    chemin = RACINE / "tools" / "tests" / "linguistique" / "evaluer_gold.py"
1212:                                "(défaut : tools/tests/linguistique/gold_restitution_v2.json)")
  ```

- **bash** `{"command": "sed -n '1,120p' reports/rapport-tagger-option.md", "description": "Read a representative report format"}`

  ```
# R0.7 / 1A — le tagger POS en option : +8,57 pts sur 20 phrases, +8,49 sur le gold 612 ; le défaut reste hors ligne

> **Ligne de roadmap** : **R0.7** (le lecteur) · **Décision** : **1A** du 14/11 · **Date** :
> 2026-11-14 · **Verdict** : ✅ **option livrée** — `--tagger` sur `analyser` et `evaluer` ; POS
> **88,57 % → 97,14 %** sur 20 phrases `hand` (**+8,57 pts**), cohérent avec le **0,9475 contre
> 0,8625** du gold 612 (**+8,49**) ; **40 appels**, **11 868 tokens** (cache neuf), **0 refus** ;
> le **défaut** reste l'**heuristique**, CPU, hors ligne, déterministe. Le gain est **+4,67** sur
> le seul gold réel 432 : lire le chiffre avec sa source.

## 1 bis. Les deux défauts corrigés (15/11)

| défaut | avant | **après** |
|---|---|---|
| **2 appels par phrase** (le tagger de syntagmes était appelé sans être utilisé) | 2 appels | **1 appel** |
| **`PONCT` perdu** (le tagger ne reçoit que mots et nombres) | 0 ponctuation étiquetée | **25/25** (restituée depuis l'heuristique) |

**La mesure sur le gold 612** (avec la clé, cache partiel) : POS **0,9575** contre 0,8625 pour
l'heuristique — **+9,5 points** (le `PONCT` restitué ajoute 0,25 pt ; le reste vient du tagger).
**Sur la base r
… [5591 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,100p' reports/rapport-faq.md; echo \"=== JSON ===\"; head -40 reports/faq.json", "description": "Read report and JSON conventions"}`

  ```
# B13 / D3 — la FAQ du produit : dix questions, dix réponses vérifiées

> **Ligne de roadmap** : **B13** (produit) · **Tâche** : **D3** · **Date** : 2026-11-15 ·
> **Verdict** : ✅ **10/10 réponses vérifiées** contre le code courant (`drave 0.1.0`) ;
> **contrôle négatif détecté** (deux affirmations fausses sont rejetées par le code).
>
> **La question.** Un utilisateur qui découvre le produit se pose dix questions concrètes :
> la langue, le hors-ligne, le coût, le tagger, le schéma, l'attachement, les spans
> inatteignables, la restitution, les limites, l'installation. La notice y répond-elle
> encore, ou répète-t-elle des chiffres d'hier ?
>
> **La réponse.** La section **§ 8** de [`docs/produit/README.md`](../docs/produit/README.md)
> porte les dix questions ; chacune est adossée à une commande, à une constante du code ou à
> un JSON de `reports/`, et **dix contrôles exécutables** les rejouent. Les dix passent. Le
> contrôle négatif est explicite : le CLI **refuse** `--langue de` (code 2) et le schéma v2
> **refuse** une annotation v1 — si ces deux refus disparaissaient, la FAQ serait fausse.
>
> **Le chiffre.** **10/10** réponses ; **26 cas** de schéma (dont le cas v1) ; **238/
… [6633 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"T1\\|empaquet\\|pyproject\\|pip install\" docs/pilotage/en-cours.md docs/pilotage/roadmap.md reports/*.json 2>/dev/null | head -40", "description": "Find packaging task context in state docs"}`

  ```
docs/pilotage/en-cours.md:67:- **Prochaine action** : **J4 — l'or de rôles** (seconds cadres, rôles hors cadre) ; T132/T133, gold de pensée.
docs/pilotage/en-cours.md:117:| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, F1 0,7902, 238/239, schéma v2, restit v1, produit (J11)** | **`g017` tranché** ; T132/T133, **[gold 452](../../reports/rapport-gold-452.md)** ; **B10.3 bloquée** |
docs/pilotage/en-cours.md:127:**N2** — porte (0,2856/0,3566) ; **Pensée** — `g017`, T132/T133, gold de pensée, **J4 — or de rôles** (seconds cadres) ; **S** — page `/` : décision et recette (106/41), référents ; **Panini** — les 26 signatures V14, puis le test à date contrôlée ; **R0.7** — `auto` prototype livré (opt-in, défaut inchangé ; décision humaine), coût 1 000 extrapolé, fermé 402 ouvert ; **A** — A6.2, A8.3b2.
docs/pilotage/roadmap.md:31:| **B — l'intelligence** | langue, pensée, jeux, maîtres, [banc externe](../theorie/glossaire/entrees/banc-externe.md), sémantique, modules | ✅ B1–B12 ; **B1.5 [corpus](../theorie/glossaire/entrees/corpus.md)**, **B12.10, B10.2bis et B11.10 closes** ; le **décodeur** est levé (objectif mot : 32,5 ; JW 26,7), le `z` re
… [9550 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' docs/pilotage/en-cours.md", "description": "Read current state doc"}`

  ```
# En ce moment

**Mis à jour : 2026-11-15, 15 h 05 HNE (clôture : le plan et le protocole or-roles committés)**

> **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
> plan plus bas (**La carte**).

### Session `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — le hub de reprise du 04/11 *(en pause)*

- **Id** : `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — [`plan.md`](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/plan.md).
- **Rôle** : **Hub de reprise** — état, docs, intégration, passe.
- **Fait** : index réparé ; **N3 intégré** ; N2/S/L actifs ; suivi docs.
- **Prochaine action** : **suivi docs**, puis la **passe** après les runs.
- **État** : **en pause** depuis le 05/11 (dernier heartbeat) ; la clôture J14.1 est portée par `e181ce02`.
- **Bloquants** : aucun.
- **Journal** : [la session](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/).

## Sessions en cours

> Contrat : [`continuite.md`](../methode/continuite.md) · sessions terminées :
> [`journal/sessions/`](../../journal/sessions/). Chaque session expose son mandat dans son
> `plan.md` (`python3 tools/sessions.py --status`). **Une session écrit l'état à la fois** :
> l
… [9421 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"exploitable\" docs/pilotage reports journal README.md 2>/dev/null | head -20", "description": "Search for the T1 task terminology"}`

  ```
reports/rapport-modele-reel.md:79:Seule structure réellement préexistante et exploitable : **les têtes GQA**, déjà
reports/rapport-optimisations.md:16:**0,484 ms → 0,011 ms** (×44). C'est ce qui rend le débit *variable* exploitable :
reports/rapport-greffon.md:28:*(C'est la version exploitable de la conclusion du capteur hebbien : un nœud
reports/rapport-localite-activation.md:25:| parcimonie exploitable | `--act-topk`, `--act-thresh`, `--act-renorm` | courbe qualité/octets mesurée ; conclusion identique à la leur : la parcimonie imposée coûte, elle se gagne à l'entraînement |
reports/rapport-empreinte-memoire.md:36:Et la sparsité des activations, elle, **n'est pas exploitable** :
reports/rapport-architecture-memoire.md:276:### Ce qui reste exploitable de la topologie
reports/rapport-hc-permutation.md:91:- **Conséquence exploitable** : un raccord pourrait se calculer comme une
reports/rapport-cycle-rapide.md:42:| langues avec un article 1 exploitable | **399** |
reports/archive/rapport-toutes-langues.md:2297:paires exploitables :
reports/archive/rapport-campagne-benefices.md:882:**exploitable** ? Sorties **telles quelles**, `temp 0`, 64 jetons.
reports/toutes-langues/046-46-deuxiem
… [2211 caractères tronqués]
  ```

- **bash** `{"command": "ls -la tools/tests/ | tail -30; echo \"---\"; find tools/tests -maxdepth 1 -name \"*.py\" | wc -l; python3 -m pytest --version 2>/dev/null || echo \"no pytest\"", "description": "List tests and check pytest"}`

  ```
total 200
drwxr-xr-x. 1 stephane stephane  1062 15 nov 14:19 .
drwxr-xr-x. 1 stephane stephane 18264 15 nov 14:25 ..
drwxr-xr-x. 1 stephane stephane    90 15 nov 04:00 cic
drwxr-xr-x. 1 stephane stephane    76 29 oct 15:50 code
drwxr-xr-x. 1 stephane stephane   230 30 oct 12:57 documents
drwxr-xr-x. 1 stephane stephane  1056 15 nov 13:10 linguistique
drwxr-xr-x. 1 stephane stephane    26 29 oct 15:58 maths
drwxr-xr-x. 1 stephane stephane  1522 15 nov 14:14 __pycache__
-rw-------. 1 stephane stephane  7758  3 nov 11:21 qualifier_politique_drvm.py
-rw-------. 1 stephane stephane  6567  2 nov 21:15 qualifier_porte_bouge_drvm.py
-rw-------. 1 stephane stephane  5290  2 nov 18:45 qualifier_porte_drvm.py
-rw-r--r--. 1 stephane stephane  5997  4 nov 08:44 qualifier_porte_fenetre_drvm.py
-rw-------. 1 stephane stephane  5982  3 nov 11:21 qualifier_porte_minute_drvm.py
-rw-------. 1 stephane stephane  7580  2 nov 20:11 qualifier_porte_mobile_drvm.py
-rw-------. 1 stephane stephane  6445  2 nov 21:22 qualifier_porte_sto_drvm.py
-rw-------. 1 stephane stephane  6007  2 nov 21:29 qualifier_porte_sto_graines.py
drwxr-xr-x. 1 stephane stephane   240 29 oct 14:47 tableaux
-rw-r--r--. 1 stephane s
… [871 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' tools/tests/test_produit_libre.py", "description": "Read a test file example"}`

  ```
#!/usr/bin/env python3
"""test_produit_libre.py — non-régression sur les **50 textes libres** de l'audit A26.

Ce que le test fige :
- la vue **`filtrer`** ne produit **aucun** chevauchement de syntagmes (0/50) ;
- la vue **`alternative`** (défaut) documente les chevauchements dans `meta.alternative` ;
- les **5 textes non linguistiques** (emoji, vide, espaces, ponctuation, nombre nu) n'ont
  **aucun** syntagme ;
- l'analyse est **déterministe** (deux passes identiques).
"""
from __future__ import annotations

import json
import pathlib
import sys
import unittest

RACINE = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RACINE))

BANC = RACINE / "reports" / "pensee-fiabilite-produit.json"
NON_LINGUISTIQUES = {"f14", "f15", "f16", "f17", "f18"}


def _textes() -> list[tuple[str, str]]:
    donnees = json.loads(BANC.read_text(encoding="utf-8"))
    return [(item["id"], item["texte"]) for item in donnees["banc_50"]["resultats"]]


def _segments(annotation) -> list:
    return [e for e in annotation.etiquettes if e.niveau == "syntagme"]


def _chevauchements(segments: list) -> int:
    return sum(1 for i, a in enumerate(segments) for b in segments[i + 1:]
           
… [1439 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"pytest\\|unittest\" tools/tests/test_produit_libre.py tools/tests/test_schema_produit.py | head -20; echo \"---\"; grep -rn \"test_produit_libre\\|tools/tests\" tools/toutes-les-portes.sh tools/porte-*.sh 2>/dev/null | head -20", "description": "Check test framework and gate  … [13 caractères tronqués]`

  ```
tools/tests/test_produit_libre.py:16:import unittest
tools/tests/test_produit_libre.py:39:class TestProduitLibre(unittest.TestCase):
tools/tests/test_produit_libre.py:75:    unittest.main(verbosity=2)
tools/tests/test_schema_produit.py:19:import unittest
tools/tests/test_schema_produit.py:34:class TestSchemaDuProduit(unittest.TestCase):
tools/tests/test_schema_produit.py:84:class TestSchemaV2(unittest.TestCase):
tools/tests/test_schema_produit.py:96:class TestRetrocompatibilite(unittest.TestCase):
tools/tests/test_schema_produit.py:110:    unittest.main(verbosity=2)
---
tools/porte-bloc-linguistique.sh:7:python3 -m unittest discover -s tools/tests/linguistique -p 'test_bloc_linguistique.py' || { echo "❌ tests"; exit 1; }
tools/porte-bloc-linguistique.sh:9:python3 tools/tests/linguistique/gold.py >/dev/null || { echo "❌ gold"; exit 1; }
tools/porte-bloc-linguistique.sh:10:python3 tools/tests/linguistique/evaluer_gold.py --json /tmp/pensee-gold-porte.json >/dev/null || { echo "❌ évaluation gold"; exit 1; }
tools/porte-cic.sh:85:src = "tools/tests/cic/corpus_dor_cic_v1.json"
tools/porte-cic.sh:104:src = "tools/tests/cic/corpus_dor_cic_v1.json"
tools/porte-cic.sh:119:python3 tools/test
… [975 caractères tronqués]
  ```

- **bash** `{"command": "find . -maxdepth 3 -name \"pyproject.toml\" -o -maxdepth 3 -name \"setup.py\" -o -maxdepth 3 -name \"setup.cfg\" 2>/dev/null | head -20", "description": "Find existing packaging files"}`

  ```
./tools/docwatch/pyproject.toml
  ```

- **bash** `{"command": "ls ~/.cache/pip 2>/dev/null | head; python3 -c \"import setuptools; print(setuptools.__version__)\" 2>/dev/null || echo \"no setuptools system\"; python3 -c \"import wheel; print(wheel.__version__)\" 2>/dev/null || echo \"no wheel system\"", "description": "Check local pip cache and bui … [10 caractères tronqués]`

  ```
http-v2
selfcheck
wheels
84.0.0
0.48.0
  ```

- **bash** `{"command": "python3 -m pip cache list 2>/dev/null | grep -i -E \"setuptools|wheel|build\" | head -20; echo \"---\"; cat tools/docwatch/pyproject.toml", "description": "Check cached build wheels and docwatch packaging example"}`

  ```
---
[build-system]
requires = ["hatchling>=1.24"]
build-backend = "hatchling.build"

[project]
name = "docwatch"
dynamic = ["version"]
description = "Service local d'affichage vivant pour collections de documents Markdown éditées par d'autres processus."
readme = "README.md"
requires-python = ">=3.9"
license = { file = "LICENSE" }
authors = [{ name = "Stéphane Denis" }]
keywords = ["markdown", "documentation", "viewer", "live", "watch", "reload", "local"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Environment :: Web Environment",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Topic :: Documentation",
    "Topic :: Text Processing :: Markup :: Markdown",
]
dependencies = [
    "mistune>=2.0",
    "tomli>=2.0; python_version < '3.11'",
]

[project.optional-dependencie
… [741 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp && PYTHONPATH=/home/stephane/Data13TB/stephane/GitHub/Qtrinet python3 -c \"from tools.drave import main; print('import ok', main(['--version']))\"", "description": "Test tools.drave import from another directory"}`

  ```
drave 0.1.0
  ```

- **bash** `{"command": "grep -n \"llm\\|import deepseek\\|tools.llm\\|from .\" tools/drave.py | head -40; echo \"---\"; ls tools/llm/__init__.py 2>/dev/null || echo \"no llm init\"; sed -n '1,60p' tools/llm/deepseek.py 2>/dev/null | head -20", "description": "Check lazy imports and llm package layout"}`

  ```
38:from __future__ import annotations
149:    from tools.llm.deepseek import DeepSeek
---
tools/llm/__init__.py
#!/usr/bin/env python3
"""deepseek.py — le professeur externe, sans poids locaux.

POURQUOI CE MODULE. Le dépôt garde ses GPU et ses CPU pour le **modèle natif**
Drave (`entrainer_moteur.py`, `drave-core`) et pour les mesures **boîte blanche**
(perplexité, activations, flux, sondes). Le **langage** — traduire, juger,
générer, évaluer — passe par une API : on ne charge plus un Qwen de 7/14/32 B
pour cela. DeepSeek est ce **professeur externe** ; ses sorties peuvent servir à
entraîner/distiller l'élève natif (autorisation explicite du propriétaire de la
licence).

CE QUE LE MODULE NE FAIT PAS. Il ne remplace pas les mesures d'états internes :
une API ne donne pas les poids ni les activations. Il ne met **jamais** la clé
dans le dépôt, dans un cache ou dans un message d'erreur. Il ne dépend d'aucun
paquet externe : `urllib` suffit.

CONTRAT.
- `DEEPSEEK_API_KEY` (ou `DSH_API_KEY`) : la clé, lue dans l'environnement ;
- `DEEPSEEK_BASE_URL` (ou `DSH_BASE_URL`) : `https://api.deepseek.com` par défaut ;
- `DEEPSEEK_MODEL` (ou `DSH_MODEL`) : `deepseek-chat` par défaut ;
  ```

### 🤖 Assistant

Now I'll create the packaging file and test it in a temporary venv.

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/pyproject.toml", "content": "[build-system]\nrequires = [\"setuptools>=61\"]\nbuild-backend = \"setuptools.build_meta\"\n\n[project]\nname = \"drave\"\nversion = \"0.1.0\"\ndescription = \"Le point d'entrée produit du bloc linguistique d … [159 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/pyproject.toml</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "ls -ld /tmp/venv-drave 2>/dev/null || echo \"absent\"; python3 -m venv /tmp/venv-drave && /tmp/venv-drave/bin/python --version && /tmp/venv-drave/bin/python -m pip --version", "description": "Create temporary virtual environment"}`

  ```
absent
Python 3.13.16
pip 26.2.1 from /tmp/venv-drave/lib64/python3.13/site-packages/pip (python 3.13)
  ```

- **bash** `{"command": "/tmp/venv-drave/bin/python -m pip install -e . 2>&1 | tail -40", "description": "Install project editable in temp venv", "timeoutMs": 180000}`

  ```
Obtaining file:///home/stephane/Data13TB/stephane/GitHub/Qtrinet
  Installing build dependencies: started
  Installing build dependencies: finished with status 'done'
  Checking if build backend supports build_editable: started
  Checking if build backend supports build_editable: finished with status 'done'
  Getting requirements to build editable: started
  Getting requirements to build editable: finished with status 'done'
  Preparing editable metadata (pyproject.toml): started
  Preparing editable metadata (pyproject.toml): finished with status 'done'
Building wheels for collected packages: drave
  Building editable for drave (pyproject.toml): started
  Building editable for drave (pyproject.toml): finished with status 'done'
  Created wheel for drave: filename=drave-0.1.0-0.editable-py3-none-any.whl size=2919 sha256=f7f405ce00daee29f9beed68d3e99b84ab38448bb343c9d821c615a9759bf16d
  Stored in directory: /tmp/pip-ephem-wheel-cache-v_acwg57/wheels/96/02/a3/318108f401dc37bb3a575e67c80cf111852262a4b3c9f691ec
Successfully built drave
Installing collected packages: drave
Successfully installed drave-0.1.0

[notice] A new release of pip is available: 26.2.1 -> 26.3
[notice] To update, 
… [60 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp && /tmp/venv-drave/bin/drave --version; echo \"code=$?\"", "description": "Run installed drave version from /tmp"}`

  ```
drave 0.1.0
code=0
  ```

- **bash** `{"command": "cd /tmp && /tmp/venv-drave/bin/drave analyser \"Le chat dort.\"; echo \"code=$?\"", "description": "Run installed drave analyser from /tmp"}`

  ```
drave 0.1.0 — analyse heuristique (CPU, hors ligne)
langue=fr script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (61.5% du texte)
POS  Le/DET chat/NOUN dort/VERB ./PONCT
SYNTAGMES
  GN   [0:7]   Le chat  rôle=agent     → dort
  GV   [8:12]  dort     rôle=predicat  → chat
PRAGMATIQUE
  phrase [0:13] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
COUVERTURE  (confiance max par niveau)  graphème=0.99 · mot=0.98 · pos=0.95 · syntagme=0.55 ·
            phrase=0.85 · discours=0.50 · pragmatique=0.45 · document=0.70
code=0
  ```

- **bash** `{"command": "cd /tmp && env -u PYTHONPATH PATH=/usr/bin:/bin bash -c 'command -v drave >/dev/null 2>&1 && echo \"TROUVE: $(command -v drave)\" || echo \"absent\"; drave --version' 2>&1; echo \"code=$?\"", "description": "Negative control without installed drave"}`

  ```
absent
bash: line 1: drave: command not found
code=127
  ```

- **bash** `{"command": "cd /tmp && /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py --version 2>&1 | head -5; echo \"direct_code=${PIPESTATUS[0]}\"", "description": "Check direct execution attempt from /tmp"}`

  ```
bash: line 1: /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py: Permission denied
direct_code=126
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/drave.py --version && python3 tools/drave.py analyser \"Le chat dort.\" | head -5; echo \"code=${PIPESTATUS[0]}\"", "description": "Verify historical entry point still works"}`

  ```
drave 0.1.0
drave 0.1.0 — analyse heuristique (CPU, hors ligne)
langue=fr script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (61.5% du texte)
POS  Le/DET chat/NOUN dort/VERB ./PONCT
SYNTAGMES
  GN   [0:7]   Le chat  rôle=agent     → dort
code=0
  ```

- **bash** `{"command": "cd /tmp && /tmp/venv-drave/bin/python -c \"import tools, tools.drave; print(tools.__path__); print(tools.drave.__file__)\"", "description": "Inspect editable install mapping"}`

  ```
_NamespacePath(['/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools', '/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools', '/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools', '__editable__.drave-0.1.0.finder.__path_hook__'])
/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py
  ```

- **bash** `{"command": "git status --short; echo \"---\"; ls -d *.egg-info 2>/dev/null || echo \"no egg-info\"", "description": "Check generated packaging artifacts"}`

  ```
M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/plan.json
?? drave.egg-info/
?? pyproject.toml
?? reports/rapport-s-paragraphes.md
?? tools/tests/linguistique/gold_reel_50.py
---
drave.egg-info
  ```

- **bash** `{"command": "grep -rn \"T1\\b\\|1/5\\|exploitable\" journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md journal/sessions/*/plan.md 2>/dev/null | tail -30", "description": "Search session plans for T1 task"}`

  ```
(no output)
  ```

- **bash** `{"command": "grep -rn \"empaquet\\|pip\\|install\" docs/pilotage/backlog docs/pilotage/*.md journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md 2>/dev/null | head -30", "description": "Search backlog for packaging mentions"}`

  ```
docs/pilotage/backlog/R44-encodeur-visuel.md:3:> **Statut** : partiel · **Priorité** : P3 · **Programme** : R · **Dépend de** : R41, R42, R43 · **Bloqué par** : — (l'OCR est installé ; restent les scans réels, le layout et les exposants)
docs/pilotage/backlog/R44-encodeur-visuel.md:64:1. ~~choisir l'OCR~~ — **fait** : tesseract 5.5.3, sans root (`tools/installer_ocr.sh`).
docs/pilotage/backlog/R44-encodeur-visuel.md:80:- [La fiche des scans](../../../reports/rapport-r44-scans.md) · [le pilote](../../../reports/rapport-r44-ocr-pilote.md) · [l'installeur](../../../tools/installer_ocr.sh) · [la porte](../../../tools/porte-ocr.sh) · [la porte des scans](../../../tools/porte-ocr-scans.sh)
docs/pilotage/backlog/B12.10-pipeline-m1-m4-m8.md:10:Le pipeline rend 528/528 et 96,33 % de complétion, mais M4 ne généralise pas et M8 est la marginale. Le chiffre est tautologique : il faut une mesure qui ne contienne pas la réponse.
docs/pilotage/backlog/B12.10-pipeline-m1-m4-m8.md:14:M1 solide (528/528) ; M2 vu seulement ; M3/M4 structurels ; M5/M6/M7 négatifs ; M8 marginal ; M9 table. **Le 29/10, la plomberie du contexte est réparée** : `ItemType.contexte` était une chaîne, le codec attendait un R
… [4199 caractères tronqués]
  ```

### 🤖 Assistant

The editable install works. Now let me run the exact verification protocol (including the negative control) and capture results.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && source /tmp/venv-drave/bin/activate && echo \"which python3: $(command -v python3)\" && python3 -m pip install -e . 2>&1 | tail -6 && echo \"--- version depuis /tmp ---\" && cd /tmp && drave --version && echo \"code=$?\" && echo \"-- … [263 caractères tronqués]`

  ```
which python3: /tmp/venv-drave/bin/python3
    Uninstalling drave-0.1.0:
      Successfully uninstalled drave-0.1.0
Successfully installed drave-0.1.0

[notice] A new release of pip is available: 26.2.1 -> 26.3
[notice] To update, run: pip install --upgrade pip
--- version depuis /tmp ---
drave 0.1.0
code=0
--- analyser depuis /tmp ---
code=0
drave 0.1.0 — analyse heuristique (CPU, hors ligne)
langue=fr script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (61.5% du texte)
POS  Le/DET chat/NOUN dort/VERB ./PONCT
SYNTAGMES
  GN   [0:7]   Le chat  rôle=agent     → dort
  GV   [8:12]  dort     rôle=predicat  → chat
PRAGMATIQUE
  phrase [0:13] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
COUVERTURE  (confiance max par niveau)  graphème=0.99 · mot=0.98 · pos=0.95 · syntagme=0.55 ·
            phrase=0.85 · discours=0.50 · pragmatique=0.45 · document=0.70
  ```

- **bash** `{"command": "cd /tmp && env -i PATH=/usr/bin:/bin HOME=/tmp bash -c 'drave --version' >/tmp/drave-negative.out 2>/tmp/drave-negative.err; echo \"code=$?\"; echo \"stdout:\"; cat /tmp/drave-negative.out; echo \"stderr:\"; cat /tmp/drave-negative.err", "description": "Capture negative control without  … [9 caractères tronqués]`

  ```
code=127
stdout:
stderr:
bash: line 1: drave: command not found
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/drave.py --version > /tmp/drave-historique-version.txt 2>&1; echo \"version_code=$?\"; cat /tmp/drave-historique-version.txt; python3 tools/drave.py analyser \"Le chat dort.\" > /tmp/drave-historique-analyser.txt 2>&1;  … [127 caractères tronqués]`

  ```
version_code=0
drave 0.1.0
analyser_code=0
drave 0.1.0 — analyse heuristique (CPU, hors ligne)
langue=fr script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (61.5% du texte)
POS  Le/DET chat/NOUN dort/VERB ./PONCT
SYNTAGMES
  GN   [0:7]   Le chat  rôle=agent     → dort
  ```

### 🤖 Assistant

Now I'll add a fast packaging test that covers metadata, both entry points, and the negative control.

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"test_empaquetage.py — le paquet `drave` et ses deux entrées.\n\nCe que le test fige :\n\n- `pyproject.toml` : nom **drave**, version **0.1.0**, `requires-python >= 3.10`,\n  **aucune dépendance**, script console `drave = tools.drave:main` ;\n- le **chemin h … [4726 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_empaquetage.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/tests/test_empaquetage.py 2>&1", "description": "Run the packaging test"}`

  ```
test_sans_installation_echec_propre (__main__.TestControleNegatif.test_sans_installation_echec_propre)
PATH vide : le nom `drave` n'est pas résolu, et l'échec est lisible. ... ok
test_analyser (__main__.TestEntreeHistorique.test_analyser) ... ok
test_version (__main__.TestEntreeHistorique.test_version) ... ok
test_import_depuis_un_autre_repertoire (__main__.TestEntreeInstallable.test_import_depuis_un_autre_repertoire) ... ok
test_aucune_dependance (__main__.TestMetadonnees.test_aucune_dependance) ... ok
test_identite_et_python (__main__.TestMetadonnees.test_identite_et_python) ... ok
test_pyproject_existe (__main__.TestMetadonnees.test_pyproject_existe) ... ok
test_script_console (__main__.TestMetadonnees.test_script_console) ... ok

----------------------------------------------------------------------
Ran 8 tests in 0.527s

OK
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/.gitignore", "old_string": "__pycache__/\n*.pyc\nreports/*.tmp", "new_string": "__pycache__/\n*.pyc\n*.egg-info/\n/build/\n/dist/\nreports/*.tmp"}`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/.gitignore": file has not been read — read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/.gitignore"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/.gitignore</path>
<type>file</type>
<content>
1: __pycache__/
2: *.pyc
3: reports/*.tmp
4: models/
5: data/
6: qtrinet-core/target/
7: 
8: # Traces de session : la copie brute reste sur disque (volumineuse, binaire),
9: # le digest markdown est versionné.
10: journal/sessions/*/session*.jsonl.zstd
11: journal/sessions/archive.log
12: 
13: # Outil de référence : la source est versionnée, le binaire se recompile
14: # (commande exacte dans tools/ref_logits.md).
15: tools/ref_logits
16: target/
17: 
18: # docwatch — SVG générés depuis les sources .puml/.mmd (docwatch les produit)
19: docs/**/*.puml.svg
20: docs/**/*.mmd.svg
21: 
22: # Campagnes GPU : points de contrôle et journaux de run (hors dépôt, archivés à part)
23: work/

(End of file - total 23 lines)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/.gitignore", "new_string": "__pycache__/\n*.pyc\n*.egg-info/\n/build/\n/dist/\nreports/*.tmp", "old_string": "__pycache__/\n*.pyc\nreports/*.tmp"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/.gitignore has been updated successfully.
  ```

- **bash** `{"command": "grep -rn \"pas de pip install\\|pas d'empaquetage\\|aucun empaquetage\\|pas de commande \\`drave\\`\\|pip install\" docs/ README.md tools/verifier_faq.py reports/rapport-faq.md reports/faq.json 2>/dev/null | head -40", "description": "Find all mentions of no packaging"}`

  ```
docs/produit/README.md:726:| **l'empaquetage** | pas de `pip install`, pas de commande `drave` dans le `PATH` ; tout part de la racine du dépôt |
docs/produit/README.md:843:`pip install`, pas de commande `drave` dans le `PATH`, pas d'empaquetage. Le CLI tourne même
tools/verifier_faq.py:343:                   "pip install"],
tools/verifier_faq.py:380:        "empaquetage": "aucun (pas de pip install, pas de commande drave dans le PATH)",
reports/faq.json:267:     "pip install"
reports/faq.json:302:    "empaquetage": "aucun (pas de pip install, pas de commande drave dans le PATH)",
  ```

- **bash** `{"command": "sed -n '700,735p' docs/produit/README.md; echo \"=== verifier ===\"; sed -n '320,400p' tools/verifier_faq.py", "description": "Inspect FAQ limitations table and verifier q10"}`

  ```
| `--jsonl` | `analyser` | une ligne JSON par phrase (avec `--fichier`) |
| `--fichier CHEMIN` | `analyser`, `restituer` | lit un texte UTF-8 au lieu de l'argument |
| `--banc CHEMIN` | `restituer` | mesure un banc JSON de textes (les 50 textes libres) |
| `--canonique` | `restituer` | ajoute la forme canonique v1 (segments + rôles + cibles) et son miroir |
| `--roles` | `restituer` | ajoute la forme lisible des rôles (agent, prédicat, lieu) ; avec `--banc`, mesure leur fidélité à l'or |
| `--partition MODE` | `analyser`, `rejouer` | `alternative` (défaut), `filtrer_union`, `filtrer`, `brut` |
| `--contexte TEXTE` | `analyser`, `restituer` | mémoire de discours portée dans le JSON |
| `--gold` | `evaluer` | gold gelé 602 au lieu du vivant 612 |
| `--par-langue` | `evaluer` | détail **fr/en** : POS, syntagmes, attachement et contrôle négatif par langue |
| `-V`, `--version` | global | `drave 0.1.0` |
| `-h`, `--aide` | global | l'aide, largeur fixe |

**Ce qui manque encore** (le contrat cible, non livré) :

| manque | conséquence |
|---|---|
| **l'entrée standard** | `--fichier` lit un fichier, mais pas de pipe (`cat corpus.txt \| drave analyser`) |
| **`--sortie`** | pas d'écritur
… [6274 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' tools/verifier_faq.py; echo \"=== fin ===\"; sed -n '400,520p' tools/verifier_faq.py", "description": "Read FAQ verifier structure and negative control"}`

  ```
#!/usr/bin/env python3
"""verifier_faq.py — les dix réponses de la FAQ produit, vérifiées contre le code courant.

La FAQ de `docs/produit/README.md` (§ 8) ne doit pas être une prose recopiée : chaque
réponse est adossée à une commande, à un chiffre de `reports/` ou à une constante du
code. Ce vérificateur exécute les dix contrôles, imprime un JSON (ou un résumé) et sort
avec le code 1 si une réponse ne tient plus.

Ce qu'il ne fait pas : aucune mesure nouvelle, aucun appel réseau, aucune clé lue. Il
rejoue le CLI en local, lit les JSON de résultats déjà publiés et inspecte le source.

Usage :
    python3 tools/verifier_faq.py            # résumé lisible
    python3 tools/verifier_faq.py --json     # le JSON de reports/faq.json

Le **contrôle négatif** est explicite : on vérifie qu'une affirmation fausse (« le CLI
accepte --langue de ») est bien rejetée par le code. Si ce contrôle passait, le
vérificateur ne prouverait rien.
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import pathlib
import subprocess
import sys
import tempfile

RACINE = pathlib.Path(__file__).resolve().parent.parent
DRAVE = RACINE / "tools" / "drave.py"
DATE = "2026-11-1
… [7066 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"verifier_faq\" tools/*.sh tools/**/*.sh 2>/dev/null | head -20; echo \"---\"; grep -rn \"faq\" tools/toutes-les-portes.sh tools/porte-produit.sh 2>/dev/null | head -20", "description": "Find gates invoking FAQ verifier"}`

  ```
---
  ```

- **bash** `{"command": "grep -n \"def q9_limites\" tools/verifier_faq.py; sed -n '270,365p' tools/verifier_faq.py", "description": "Read q9 limitations check"}`

  ```
311:def q9_limites() -> dict:
    }


def q8_restitution() -> dict:
    """Trois vues : surface exacte, forme canonique, rôles lisibles mais peu fidèles."""
    banc = "reports/pensee-fiabilite-produit.json"
    v0 = _json(["restituer", "--banc", banc])
    s0 = v0["synthese"]
    assert s0["annotations"] == 46 and s0["surface"]["exacts"] == 46, s0
    assert s0["miroir"]["fidelite"] == 0.1087, s0["miroir"]
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
    assert s2["controles"]["spans_dans_source"] == {"justes": 198, "tota
… [3913 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"pip\\|empaquet\\|installation\\|install\" reports/rapport-faq.md | head -30; echo \"---\"; sed -n '100,220p' reports/rapport-faq.md", "description": "Find installation mentions in FAQ report"}`

  ```
9:> inatteignables, la restitution, les limites, l'installation. La notice y répond-elle
65:| 10 | **L'installation ?** | `drave 0.1.0`, Python **3.10** (grammaire), `python3 -S` code 0, **0** dépendance, gold versionnés | `q10_installation` |
102:| installation | `drave 0.1.0`, `python3 -S` **0**, grammaire **3.10**, **0** paquet externe |
---
| restitution v1 | **46/46** canonique, strict **0,1087**, **395** segments, **315** cibles |
| restitution v2 | **19/46** cadres exacts, **16** non vides, **F1 0,5270**, **198/198** spans, **46/46** rendus |
| installation | `drave 0.1.0`, `python3 -S` **0**, grammaire **3.10**, **0** paquet externe |

## 5. Le contrôle négatif

Le vérificateur ne se contente pas de confirmer : il vérifie que le code **rejette** deux
affirmations fausses.

| affirmation fausse | ce que le code fait | détecté |
|---|---|---|
| « le CLI accepte `--langue de` » | `analyser … --langue de` sort **2** (usage invalide) | ✅ |
| « le schéma v2 accepte une annotation v1 » | `verifier_schema_produit.py` publie `v2_refuse_v1: true` | ✅ |

Si l'une des deux tombait, `controle_negatif.detecte` serait `false` et le script sortirait 1 :
c'est le garde-fou contre une FAQ qu
… [2410 caractères tronqués]
  ```

- **bash** `{"command": "grep -rni \"empaquetage\\|pip install\\|commande .drave\\|dans le .PATH\" README.md docs reports tools/verifier_faq.py 2>/dev/null | grep -v \"reports/archive\\|journal\" | head -60", "description": "Search all packaging claims across docs and tools"}`

  ```
docs/produit/README.md:726:| **l'empaquetage** | pas de `pip install`, pas de commande `drave` dans le `PATH` ; tout part de la racine du dépôt |
docs/produit/README.md:843:`pip install`, pas de commande `drave` dans le `PATH`, pas d'empaquetage. Le CLI tourne même
reports/faq.json:267:     "pip install"
reports/faq.json:302:    "empaquetage": "aucun (pas de pip install, pas de commande drave dans le PATH)",
tools/verifier_faq.py:343:                   "pip install"],
tools/verifier_faq.py:380:        "empaquetage": "aucun (pas de pip install, pas de commande drave dans le PATH)",
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "| **la publication** | `pip install -e .` et la commande `drave` existent ; **pas de wheel publiée** ni de paquet sur PyPI — l'installation pointe vers le dépôt |", "old_string": "| **l'empaquetage … [103 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md": file has not been read — read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "offset": 718, "limit": 18}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "offset": 837, "limit": 18}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md</path>
<type>file</type>
<content>
718: | **`rejouer` sur un JSON sauvegardé** | `rejouer` prend un **texte**, pas une annotation ; on ne peut pas rejouer un fichier produit hier |
719: | **`--mode` / la cascade locale** | le CLI expose l'heuristique et la cascade **API** (`--tagger`) ; `parallele` et la cascade **locale** demandent le code Python |
720: | **`--profils`** | les 398 langues de l'autotest UDHR ne sont pas accessibles par le CLI |
721: | **`--duree`** | pas de durée dans le JSON du CLI (le bloc l'a avec `--duree`) |
722: | **un répertoire** | `--fichier` lit un fichier ; pas de parcours de répertoire |
723: | **`candidats` structurés** | ce sont des **chaînes d'affichage** (« « qui dort » → voisine »), pas des objets `{span, cible}` ; un programme doit les reparser |
724: | **`role` normalisé** | les valeurs mélangent `predicat`/`prédicat` et `qualite`/`qualité` ; fragile pour un filtre |
725: | **`--strict`** | `evaluer` ne mesure pas la cascade **locale** et n'applique pas son plancher (0,70) ; c'est le banc de recherche (`evaluer_gold.py`) qui le fait |
726: | **l'empaquetage** | pas de `p
… [1008 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md</path>
<type>file</type>
<content>
837: linguistique** ne l'est pas.
838: 
839: ### 8.10 Comment l'installer et le lancer ?
840: 
841: Cloner le dépôt, puis lancer `python3 tools/drave.py …` **depuis la racine** : Python **3.10+**
842: (le code parse en 3.10, mesuré ici en 3.13), **aucune dépendance externe**, aucun GPU. Pas de
843: `pip install`, pas de commande `drave` dans le `PATH`, pas d'empaquetage. Le CLI tourne même
844: avec `python3 -S` (sans `site-packages`) ; les gold sont versionnés dans
845: `tools/tests/linguistique/`. Le corpus UDHR, lui, n'est pas versionné (`data/` hors dépôt).
846: Vérifier l'installation : `python3 tools/drave.py --version` → `drave 0.1.0`, puis
847: `python3 tools/drave.py analyser "Le chat dort."`.
848: 
849: ## 9. Où aller ensuite
850: 
851: | si vous voulez… | allez à |
852: |---|---|
853: | **voir cinq JSON commentés** | [`exemples.md`](exemples.md) |
854: | **la FAQ du produit** (dix questions vérifiées) | [§ 8](#8-faq--dix-questions) · [`reports/rapport-faq.md`](../../reports/rapport-faq.md) · [`reports/faq.json`](../../reports/faq.json) |

(Showing lines 837-854
… [48 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "| **la publication** | `pip install -e .` et la commande `drave` existent ; **pas de wheel publiée** ni de paquet sur PyPI — l'installation pointe vers le dépôt |", "old_string": "| **l'empaquetage … [103 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "### 8.10 Comment l'installer et le lancer ?\n\nDeux chemins, le même CLI. **Depuis le dépôt, sans rien installer** : `python3 tools/drave.py …`\ndepuis la racine (Python **3.10+**, mesuré ici en 3. … [1835 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_faq.py", "limit": 80, "offset": 311}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_faq.py</path>
<type>file</type>
<content>
311: def q9_limites() -> dict:
312:     """Les limites nommées : pas de génération, de serveur, de local, ni d'options fantômes."""
313:     aide = _run(["--aide"])
314:     assert aide.returncode == 0
315:     for commande in ("analyser", "evaluer", "rejouer", "restituer"):
316:         assert commande in aide.stdout, commande
317:     for fantome in ("--sortie", "--mode", "--strict"):
318:         assert fantome not in aide.stdout, fantome
319:         r = _run(["analyser", "Le chat dort.", fantome])
320:         assert r.returncode == 2, (fantome, r.returncode)
321: 
322:     source = DRAVE.read_text(encoding="utf-8")
323:     for interdit in ("http.server", "transformers", "torch", "sys.stdin"):
324:         assert interdit not in source, interdit
325:     for nom in ("pyproject.toml", "setup.py", "setup.cfg", "requirements.txt"):
326:         assert not (RACINE / nom).exists(), nom
327: 
328:     # Les rôles ne sont pas normalisés : les deux chemins du bloc n'écrivent pas pareil.
329:     bloc = (RACINE / "tools/bloc_linguistique.py").read_text(encoding="utf-8")
330: 
… [3606 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_faq.py", "new_string": "    source = DRAVE.read_text(encoding=\"utf-8\")\n    for interdit in (\"http.server\", \"transformers\", \"torch\", \"sys.stdin\"):\n        assert interdit not in source, interdit\n\n    # Les rôl … [506 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_faq.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_faq.py", "new_string": "        \"absent\": [\"génération\", \"traduction\", \"serveur HTTP\", \"RSN/DRVM\",\n                   \"neuronal local\", \"classement appris\", \"calibration des confiances\",\n                  … [786 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_faq.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_faq.py", "new_string": "def q10_installation() -> dict:\n    \"\"\"Source et pyproject : Python 3.10+, stdlib, installation éditable, gold versionnés.\"\"\"\n    version = _run([\"--version\"])\n    assert version.returnco … [3883 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_faq.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifier_faq.py 2>&1 | tail -30; echo \"code=${PIPESTATUS[0]}\"", "description": "Run FAQ verifier after packaging change", "timeoutMs": 300000}`

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
code=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifier_faq.py --json > /tmp/faq-new.json && diff -u reports/faq.json /tmp/faq-new.json | head -80", "description": "Generate new FAQ JSON and inspect diff", "timeoutMs": 300000}`

  ```
--- reports/faq.json	2026-11-15 06:06:50.281806848 -0500
+++ /tmp/faq-new.json	2026-11-15 21:42:02.071484813 -0500
@@ -264,8 +264,12 @@
      "--sortie",
      "parcours de répertoire",
      "rejeu d'une annotation sauvegardée",
-     "pip install"
+     "publication PyPI"
     ],
+    "empaquetage": {
+     "livre": "pip install -e . + commande drave",
+     "non_livre": "wheel / paquet PyPI"
+    },
     "options_fantomes": {
      "--sortie": "code 2",
      "--mode": "code 2",
@@ -299,14 +303,23 @@
      "sans_site_packages": "code 0"
     },
     "dependances_externes": 0,
-    "empaquetage": "aucun (pas de pip install, pas de commande drave dans le PATH)",
+    "empaquetage": {
+     "fichier": "pyproject.toml",
+     "nom": "drave",
+     "version": "0.1.0",
+     "requires_python": ">=3.10",
+     "dependances": [],
+     "script_console": "drave = tools.drave:main",
+     "installation": "python3 -m pip install -e . (venv)",
+     "hors_depot": "commande drave depuis n'importe quel répertoire"
+    },
     "gold_versionnes": [
      "gold.json",
      "gold_gele.json",
      "gold_reel.json",
      "gold_synthetique.json"
     ],
-    "racine": "tout part de la racine du 
… [123 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cp /tmp/faq-new.json reports/faq.json && git diff --stat reports/faq.json", "description": "Update FAQ JSON with regenerated report"}`

  ```
reports/faq.json | 19 ++++++++++++++++---
 1 file changed, 16 insertions(+), 3 deletions(-)
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-faq.md", "limit": 18, "offset": 55}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-faq.md", "limit": 12, "offset": 95}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-faq.md</path>
<type>file</type>
<content>
55: |---:|---|---|---|
56: | 1 | **Quelles langues ?** | détection `de`/`es`, `und` sous le seuil ; `--langue` limité à `fr`/`en` ; `--langue de` → code 2 ; 398 profils UDHR (0,9687) | `q1_langue` |
57: | 2 | **Hors ligne ?** | socket interdite : analyse code 0 ; module réseau non importé ; `--tagger` sans clé → code 4, `stdout` vide | `q2_hors_ligne` |
58: | 3 | **Combien ça coûte ?** | défaut : 0 $ d'API ; tagger : **609 appels**, **22 299 tokens**, **155 s**, **~0,02 $** ; 3 exemples : **441 tokens**, **3,7 s** | `q3_cout` |
59: | 4 | **Que change `--tagger` ?** | POS seul : **95,75 %** contre **86,25 %** (612) ; **95,00 %** contre **88,91 %** (réel 452) ; ponctuation **25/25** | `q4_tagger` |
60: | 5 | **Quel schéma ?** | `drave.annotation` **v2**, v1 lue ; **6 cas**, **26** avec `--gold 20`, **0 échec** ; v2 refuse v1 | `q5_schema` |
61: | 6 | **L'attachement ?** | **238/239** cibles (**0,9958**) ; **1,0000** sur les spans prédits ; top-k **0,9874** ; hasard **1,67 %** ; audit **42,14 %** / **0,908 %** | `q6_attachement` |
62: | 7 | **Les spans inatteignables ?** | *
… [1052 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-faq.md</path>
<type>file</type>
<content>
95: | schéma | **6/6** cas, **26/26** avec `--gold 20`, versions **[1, 2]**, `v1_lue`, `v2_refuse_v1` |
96: | attachement | **238/239** labels, **0,9958**, exact sur span **1,0000**, top-k **0,9874** |
97: | contrôles négatifs | cible au hasard **0,0167** ; candidat aléatoire **0,4214** ; permutation **0,00908** |
98: | `g017` | gold **[9:28]**, prédit **[9:38]**, cible `said` juste ; règle **rejetée** |
99: | restitution v0 | **46/46** surfaces, miroir strict **0,1087**, **46** contrôles négatifs détectés |
100: | restitution v1 | **46/46** canonique, strict **0,1087**, **395** segments, **315** cibles |
101: | restitution v2 | **19/46** cadres exacts, **16** non vides, **F1 0,5270**, **198/198** spans, **46/46** rendus |
102: | installation | `drave 0.1.0`, `python3 -S` **0**, grammaire **3.10**, **0** paquet externe |
103: 
104: ## 5. Le contrôle négatif
105: 
106: Le vérificateur ne se contente pas de confirmer : il vérifie que le code **rejette** deux

(Showing lines 95-106 of 153. Use offset=107 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-faq.md", "new_string": "| 9 | **Les limites ?** | pas de génération, serveur, RSN, local, classement, calibration, `--langue-forcee`, garantie hors domaine ; `--sortie`/`--mode`/`--strict` → code 2 ; **pas de wheel/PyPI** … [563 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-faq.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-faq.md", "new_string": "| installation | `drave 0.1.0`, `python3 -S` **0**, grammaire **3.10**, **0** paquet externe ; `pyproject.toml` éditable (`drave = tools.drave:main`) |", "old_string": "| installation | `drave 0.1. … [68 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-faq.md has been updated successfully.
  ```

- **bash** `{"command": "date -Iseconds; date -u +%Y-%m-%dT%H:%M:%SZ", "description": "Get current date for the report"}`

  ```
2026-11-15T21:42:15-05:00
2026-11-16T02:42:15Z
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport importlib.metadata as md\ntry:\n    d = md.distribution('drave')\n    print('dist', d.version, d.metadata['Name'])\nexcept Exception as e:\n    print('not installed in system python:', type(e).__name__, e)\nP … [394 caractères tronqués]`

  ```
dist 0.1.0 drave
name drave
version 0.1.0
requires None
entry_points [('drave', 'tools.drave:main')]
files_sample ['README.md', 'pyproject.toml', 'drave.egg-info/PKG-INFO', 'drave.egg-info/SOURCES.txt', 'drave.egg-info/dependency_links.txt', 'drave.egg-info/entry_points.txt', 'drave.egg-info/top_level.txt', 'tools/adaptateur_langue.py']
  ```

### 🤖 Assistant

I'll now collect the full verification results into a structured JSON for the report.

- **bash** `{"command": "cat > /tmp/collecte_empaquetage.py <<'PY'\nfrom __future__ import annotations\nimport json, os, pathlib, subprocess, sys, tomllib\n\nRACINE = pathlib.Path(\"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\")\nVENV = pathlib.Path(\"/tmp/venv-drave\")\nPY = VENV / \"bin\" / \"python\"\nDR … [4556 caractères tronqués]`

  ```
{
 "pyproject": {
  "fichier": "pyproject.toml",
  "nom": "drave",
  "version": "0.1.0",
  "requires_python": ">=3.10",
  "dependances": [],
  "script_console": "tools.drave:main",
  "build_system": "setuptools.build_meta"
 },
 "controle_negatif": {
  "condition": "sans installation : PATH=/usr/bin:/bin, cwd=/tmp, aucun venv active",
  "resultat": {
   "commande": "/bin/bash -c drave --version",
   "cwd": "/tmp",
   "code": 127,
   "stdout": "",
   "stderr": "/bin/bash: line 1: drave: command not found\n"
  },
  "echec_propre": true
 },
 "test": {
  "fichier": "tools/tests/test_empaquetage.py",
  "resultat": {
   "commande": "/usr/bin/python3 tools/tests/test_empaquetage.py",
   "cwd": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet",
   "code": 0,
   "stdout": "",
   "stderr": "test_sans_installation_echec_propre (__main__.TestControleNegatif.test_sans_installation_echec_propre)\nPATH vide : le nom `drave` n'est pas résolu, et l'échec est lisible. ... ok\ntest_analyser (__main__.TestEntreeHistorique.test_analyser) ... ok\ntest_version (__main__.TestEntreeHistorique.test_version) ... ok\ntest_import_depuis_un_autre_repertoire (__main__.TestEntreeInstallable.test_import_depuis_un_a
… [609 caractères tronqués]
  ```

- **bash** `{"command": "wc -l /tmp/empaquetage.json; sed -n '1,120p' /tmp/empaquetage.json", "description": "Inspect generated packaging JSON"}`

  ```
90 /tmp/empaquetage.json
{
 "schema": "drave.empaquetage.verification",
 "version": 1,
 "date": "2026-11-15",
 "tache": "T1 (exploitable, 1/5)",
 "produit": "0.1.0",
 "pyproject": {
  "fichier": "pyproject.toml",
  "nom": "drave",
  "version": "0.1.0",
  "requires_python": ">=3.10",
  "dependances": [],
  "script_console": "tools.drave:main",
  "build_system": "setuptools.build_meta"
 },
 "environnement": {
  "venv": "/tmp/venv-drave",
  "python": "Python 3.13.16",
  "pip": "pip 26.2.1 from /tmp/venv-drave/lib64/python3.13/site-packages/pip (python 3.13)",
  "commande_installation": "/tmp/venv-drave/bin/python -m pip install -e .",
  "installation": {
   "commande": "/tmp/venv-drave/bin/python -m pip install -e .",
   "cwd": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet",
   "code": 0,
   "stdout": "Obtaining file:///home/stephane/Data13TB/stephane/GitHub/Qtrinet\n  Installing build dependencies: started\n  Installing build dependencies: finished with status 'done'\n  Checking if build backend supports build_editable: started\n  Checking if build backend supports build_editable: finished with status 'done'\n  Getting requirements to build editable: started\n  Getting requirement
… [5251 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp && env -u DEEPSEEK_KEY_FILE -u DEEPSEEK_API_KEY -u DSH_KEY_FILE -u DSH_API_KEY HOME=/tmp /tmp/venv-drave/bin/drave analyser \"Le chat dort.\" --tagger >/tmp/drave-tagger-installed.out 2>/tmp/drave-tagger-installed.err; echo \"code=$?\"; echo \"stdout:\"; cat /tmp/drave-tagger-in … [146 caractères tronqués]`

  ```
code=4
stdout:
stderr:
drave: dépendance absente : clé DeepSeek absente : exportez DEEPSEEK_KEY_FILE, déposez la clé dans ~/.config/drave/deepseek.key, ou exportez DEEPSEEK_API_KEY. Sans --tagger, le défaut reste l'heuristique hors ligne.
  ```

- **bash** `{"command": "cd /tmp && /tmp/venv-drave/bin/drave evaluer --json > /tmp/drave-evaluer-installed.json 2>/tmp/drave-evaluer-installed.err; echo \"code=$?\"; head -5 /tmp/drave-evaluer-installed.json; echo \"stderr:\"; head -5 /tmp/drave-evaluer-installed.err", "description": "Check installed CLI can r … [46 caractères tronqués]`

  ```
code=0
{
 "version": "0.1.0",
 "gold": {
  "nom": "vivant (hand + reel + synthétique)",
  "gele": false,
stderr:
  ```

### 🤖 Assistant

Now I'll write the curated report JSON and the markdown report.

- **write** `{"content": "{\n \"schema\": \"drave.empaquetage.verification\",\n \"version\": 1,\n \"date\": \"2026-11-15\",\n \"tache\": \"T1 (exploitable, 1/5)\",\n \"produit\": \"0.1.0\",\n \"pyproject\": {\n  \"fichier\": \"pyproject.toml\",\n  \"nom\": \"drave\",\n  \"version\": \"0.1.0\",\n  \"requires_pyth … [4323 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/empaquetage.json</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **write** `{"content": "# T1 — l'empaquetage : `pip install -e .`, `drave` hors du dépôt, chemin historique intact\n\n> **Ligne de roadmap** : **B13** (produit) · **Tâche** : **T1** (exploitable, 1/5) ·\n> **Date** : 2026-11-15 · **Verdict** : ✅ **empaquetage minimal livré**.\n>\n> **Le chiffre.** `pyproject.t … [8484 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-empaquetage.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -m json.tool reports/empaquetage.json >/dev/null && echo \"JSON OK\" && python3 -m json.tool reports/faq.json >/dev/null && echo \"FAQ JSON OK\"", "description": "Validate report JSON files"}`

  ```
JSON OK
FAQ JSON OK
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/tests/test_empaquetage.py 2>&1 | tail -6", "description": "Re-run packaging test"}`

  ```
test_script_console (__main__.TestMetadonnees.test_script_console) ... ok

----------------------------------------------------------------------
Ran 8 tests in 0.552s

OK
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py 2>&1 | tail -40; echo \"code=${PIPESTATUS[0]}\"", "description": "Run documentation review", "timeoutMs": 300000}`

  ```
revue de documentation · 760 fiche(s) · 854 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ❌ 2 anomalie(s) :
     · compteurs : en-cours.md dit 759 fichiers, le disque en a 760
     · compteurs : en-cours.md dit 853 JSON, le disque en a 854
code=1
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifie_en_cours.py 2>&1 | tail -20; echo \"code=${PIPESTATUS[0]}\"", "description": "Check state doc consistency", "timeoutMs": 120000}`

  ```
en-cours · 1630 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
code=0
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 10, "offset": 128}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
128: 
129: ## Les questions ouvertes
130: 
131: - **R1** : **1 024 octets** ? → **R1.2** (3,0107 à octets constants).
132: - **N2** : **< 2,5** ? → **oui par la fenêtre** : 2,4759 / 2,4373 au grand corpus (1 024, 30 k pas) ; la porte **propre** reste à 2,7856.
133: - **N2 (nuit)** : la distillation tient-elle à 30 000 pas / 122 Mo ? → **non** à parité stricte (erratum) ; la repondération vaut **−0,05**.
134: - **R1 (nuit)** : 2 048 à 20 000 pas ? → **oui** : 2×10 000 pas finis (perte 0,9409 → 0,8965 ; PPL 2,614 → 2,4953).
135: - **Pensée** : l'**absence** est-elle annotable ? → le **v0 suivant** tranche ; la
136:   **restitution v1** : le miroir strict **ne monte pas** (0,1087), la forme canonique vaut
137:   **46/46** ; la **v3** sépare les cinq rôles (**18/18** au gold S) mais le gold v2

(Showing lines 128-137 of 145. Use offset=138 to continue.)
</content>
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 14, "offset": 113}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
113: 
114: | chantier | frontière (graphe) | bloquant (ressource) | prochaine action |
115: |---|---|---|---|
116: | **A — le moteur** | **A2.6** | A3.4 Colab ; A5.4 FPGA ; **A6.2 libre** (MoE 18,56 Go, PPL 37,2013 ; résidence 16 GiB) | **A2.6** (experts et tête) ; **A6.2** rapport + A8.3b2 |
117: | **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, F1 0,7902, 238/239, schéma v2, restit v1, produit (J11)** | **`g017` tranché** ; T132/T133, **[gold 452](../../reports/rapport-gold-452.md)** ; **B10.3 bloquée** |
118: | **N — le natif** | **N2, N4** | N2 : **1 024 — 2,3911 / 2,3522** ; porte 2,7856 ; **[v2](../../reports/rapport-coordination-n2-v2.md)** ; N3 couvert ; N4 0/4 ; N5 gelé | **les runs N2** ; puis la **porte propre** ; **N4** |
119: | **R — le lecteur** | **R0.7** | **R0.7 — tagger 612 0,9575, réel 452 0,9500 ; W2 : 402 0,9643, H50 0,8607 ; W3 : défaut hors ligne, clé invalide 4, 1 000 phrases = 143 870 tokens / 0,031 $ hors pointe ; X3 : lot 1 000, 672 appels, 99 971 tokens, 0,02177 $ ; W5 : restitution v3, 20/46 (F1 
… [1091 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 12, "offset": 101}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
101: | invariant | valeur | contrôle |
102: |---|---|---|
103: | portes | **85** (dont `porte-cic` le 14/11) | `tools/porte-*.sh` |
104: | chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
105: | fichiers / JSON de résultats | **759** / **853** | `reports/*.md` / `reports/*.json` |
106: | documents de `docs/` | **124** (hors archive et README) | `docs/**/*.md` |
107: | dernière passe | **15/11 09 h 53 → 12 h 15** (85, **81/4**) ; rouges `indice`, `melange` (structurelles), `sessions` (**réparée** à 12 h 20), `prechargement` (**environnementale**) ; ciblage W6 **9/9** | `work/portes-1115-09h53/registre.txt` ; `work/portes/w6-final/` |
108: 
109: ## Les chantiers et leurs bloquants
110: 
111: **Dépendances** : [le graphe](backlog/dependances.md) ; cette table ne garde que les **bloquants
112: externes** et la **prochaine action**.

(Showing lines 101-112 of 145. Use offset=113 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "| fichiers / JSON de résultats | **760** / **854** | `reports/*.md` / `reports/*.json` |", "old_string": "| fichiers / JSON de résultats | **759** / **853** | `reports/*.md` / `reports/*.json` | … [2 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py 2>&1 | tail -20; echo \"code=${PIPESTATUS[0]}\"", "description": "Re-run documentation review", "timeoutMs": 300000}`

  ```
revue de documentation · 760 fiche(s) · 854 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
code=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifier_faq.py 2>&1 | tail -15; echo \"code=${PIPESTATUS[0]}\"; python3 tools/verifier_faq.py --autotest 2>&1 | tail -3; echo \"autotest_code=${PIPESTATUS[0]}\"", "description": "Re-run FAQ verifier and autotest", "tim … [16 caractères tronqués]`

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
code=0
✅ autotest : l'affirmation fausse est rejetée
autotest_code=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/taille_documents.py 2>&1 | tail -15; echo \"code=${PIPESTATUS[0]}\"; python3 tools/verifier_schemas.py 2>&1 | tail -8; echo \"schemas_code=${PIPESTATUS[0]}\"", "description": "Check document budget and SVG schemas", "ti … [17 caractères tronqués]`

  ```
2433    164   T1   2500  docs/pilotage/references-non-regression.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4000 mots (budget 4 000)

  avertissements :
     · 63 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
code=0
  schémas · 464 document(s) · 67 SVG · 2 source(s)
  ✅ aucun ASCII art, SVG valides et référencés, blocs PlantUML inline valides,
     sources et images relatives.
sche
… [10 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short | grep -E \"pyproject|empaquetage|verifier_faq|produit/README|faq|en-cours|gitignore|test_empaquetage\"", "description": "Show our changed files"}`

  ```
M .gitignore
 M docs/pilotage/en-cours.md
 M docs/produit/README.md
 M reports/faq.json
 M reports/rapport-faq.md
 M tools/verifier_faq.py
?? pyproject.toml
?? reports/empaquetage.json
?? reports/rapport-empaquetage.md
?? tools/tests/test_empaquetage.py
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff --stat -- pyproject.toml .gitignore tools/verifier_faq.py reports/faq.json docs/produit/README.md docs/pilotage/en-cours.md reports/rapport-faq.md 2>/dev/null; echo \"--- untracked ---\"; ls -l reports/rapport-empaquetage.md … [122 caractères tronqués]`

  ```
.gitignore                |  3 +++
 docs/pilotage/en-cours.md |  2 +-
 docs/produit/README.md    | 29 ++++++++++++++++++++++-------
 reports/faq.json          | 19 ++++++++++++++++---
 reports/rapport-faq.md    |  6 +++---
 tools/verifier_faq.py     | 32 +++++++++++++++++++++++++-------
 6 files changed, 70 insertions(+), 21 deletions(-)
--- untracked ---
-rw-------. 1 stephane stephane  334 15 nov 21:38 pyproject.toml
-rw-------. 1 stephane stephane 4133 15 nov 21:43 reports/empaquetage.json
-rw-------. 1 stephane stephane 8654 15 nov 21:43 reports/rapport-empaquetage.md
-rw-------. 1 stephane stephane 4723 15 nov 21:39 tools/tests/test_empaquetage.py
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && stat -c '%a %n' pyproject.toml reports/rapport-tagger-option.md reports/faq.json tools/tests/test_produit_libre.py docs/produit/README.md", "description": "Compare file permissions"}`

  ```
600 pyproject.toml
600 reports/rapport-tagger-option.md
644 reports/faq.json
644 tools/tests/test_produit_libre.py
644 docs/produit/README.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"pyproject.toml\" tools docs reports --include=\"*.py\" --include=\"*.sh\" --include=\"*.md\" 2>/dev/null | grep -v \"reports/archive\\|journal\" | head -40", "description": "Search for other pyproject assumptions"}`

  ```
tools/docwatch/.venv/lib/python3.13/site-packages/pip/__pip-runner__.py:11:# Copied from pyproject.toml
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_internal/exceptions.py:215:    """Raised when pyproject.toml has `build-system`, but no `build-system.requires`."""
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_internal/exceptions.py:223:                "This package has an invalid pyproject.toml file.\n"
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_internal/exceptions.py:232:    """Raised when pyproject.toml an invalid `build-system.requires`."""
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_internal/exceptions.py:241:                f"pyproject.toml.\n{reason}"
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_internal/exceptions.py:1028:                "pyproject.toml based projects"
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_internal/pyproject.py:23:    return os.path.join(unpacked_source_directory, "pyproject.toml")
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_internal/pyproject.py:31:def load_pyproject_toml(
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_internal/pyproject.py:32:    pyproject_toml: str, se
… [4719 caractères tronqués]
  ```

### 🤖 Assistant

Let me re-run the install from a clean venv to confirm the result is reproducible.

- **bash** `{"command": "python3 -m venv --clear /tmp/venv-drave && /tmp/venv-drave/bin/python --version && cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /tmp/venv-drave/bin/python -m pip install -e . 2>&1 | tail -8", "description": "Recreate venv and reinstall editable", "timeoutMs": 240000}`

  ```
Python 3.13.16
  Created wheel for drave: filename=drave-0.1.0-0.editable-py3-none-any.whl size=2919 sha256=b5a23913fd09bb901469e6729ff48013a54cb7e9ba9b633ae0fe7130cd463d21
  Stored in directory: /tmp/pip-ephem-wheel-cache-bq_ddv3y/wheels/96/02/a3/318108f401dc37bb3a575e67c80cf111852262a4b3c9f691ec
Successfully built drave
Installing collected packages: drave
Successfully installed drave-0.1.0

[notice] A new release of pip is available: 26.2.1 -> 26.3
[notice] To update, run: /tmp/venv-drave/bin/python -m pip install --upgrade pip
  ```

- **bash** `{"command": "cd /tmp && /tmp/venv-drave/bin/drave --version && /tmp/venv-drave/bin/drave analyser \"Le chat dort.\" | head -7; echo \"code=${PIPESTATUS[0]}\"", "description": "Verify installed CLI after clean reinstall"}`

  ```
drave 0.1.0
drave 0.1.0 — analyse heuristique (CPU, hors ligne)
langue=fr script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (61.5% du texte)
POS  Le/DET chat/NOUN dort/VERB ./PONCT
SYNTAGMES
  GN   [0:7]   Le chat  rôle=agent     → dort
  GV   [8:12]  dort     rôle=predicat  → chat
PRAGMATIQUE
code=0
  ```

- **bash** `{"command": "cd /tmp && env -i PATH=/usr/bin:/bin HOME=/tmp bash -c 'drave --version' >/tmp/neg.out 2>/tmp/neg.err; echo \"code=$?\"; cat /tmp/neg.err", "description": "Verify negative control after clean reinstall"}`

  ```
code=127
bash: line 1: drave: command not found
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/drave.py --version && python3 tools/drave.py analyser \"Le chat dort.\" >/dev/null; echo \"historique_code=$?\"", "description": "Confirm historical path after reinstall"}`

  ```
drave 0.1.0
historique_code=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -m pytest tools/tests/test_empaquetage.py -q 2>&1 | tail -12; echo \"code=${PIPESTATUS[0]}\"", "description": "Run packaging test under pytest", "timeoutMs": 120000}`

  ```
........                                                                 [100%]
8 passed in 0.66s
code=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,130p' tools/porte-produit.sh", "description": "Inspect product gate"}`

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
… [4225 caractères tronqués]
  ```

### 🤖 Assistant

I'll run the product gate in the background while I review the final diff.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && bash tools/porte-produit.sh", "description": "Run product gate", "run_in_background": true}`

  ```
started background job bash-74
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff -- docs/produit/README.md tools/verifier_faq.py .gitignore docs/pilotage/en-cours.md reports/rapport-faq.md | sed -n '1,240p'", "description": "Review diff of modified docs and verifier"}`

  ```
diff --git a/.gitignore b/.gitignore
index e85c4a81..7937dc3f 100644
--- a/.gitignore
+++ b/.gitignore
@@ -1,5 +1,8 @@
 __pycache__/
 *.pyc
+*.egg-info/
+/build/
+/dist/
 reports/*.tmp
 models/
 data/
diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index 85803db9..902b90b0 100644
--- a/docs/pilotage/en-cours.md
+++ b/docs/pilotage/en-cours.md
@@ -102,7 +102,7 @@
 |---|---|---|
 | portes | **85** (dont `porte-cic` le 14/11) | `tools/porte-*.sh` |
 | chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
-| fichiers / JSON de résultats | **759** / **853** | `reports/*.md` / `reports/*.json` |
+| fichiers / JSON de résultats | **760** / **854** | `reports/*.md` / `reports/*.json` |
 | documents de `docs/` | **124** (hors archive et README) | `docs/**/*.md` |
 | dernière passe | **15/11 09 h 53 → 12 h 15** (85, **81/4**) ; rouges `indice`, `melange` (structurelles), `sessions` (**réparée** à 12 h 20), `prechargement` (**environnementale**) ; ciblage W6 **9/9** | `work/portes-1115-09h53/registre.txt` ; `work/portes/w6-final/` |
 
diff --git a/docs/produit/README.md b/docs/produit/README.md
index 184a7c11..7b76a5ad 100644
--- a/docs/produit/README.md
+++ b/
… [8987 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-74", "wait": false}`

  ```
✅ version : drave 0.1.0
  ✅ analyser fr : JSON valide, étiquettes et syntagmes
  ✅ analyser en : JSON valide, étiquettes et syntagmes
  ✅ rejeu : sha256 f4b7822076a4203d deux fois
[status: running]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && rm -rf /tmp/drave-wheel && mkdir -p /tmp/drave-wheel && /tmp/venv-drave/bin/python -m pip wheel . -w /tmp/drave-wheel --no-deps 2>&1 | tail -8 && python3 - <<'PY'\nimport pathlib, zipfile\nw = next(pathlib.Path('/tmp/drave-wheel').gl … [434 caractères tronqués]`

  ```
Building wheel for drave (pyproject.toml): started
  Building wheel for drave (pyproject.toml): finished with status 'done'
  Created wheel for drave: filename=drave-0.1.0-py3-none-any.whl size=1412100 sha256=8bf763474af374a6d39113a30aa7d9b7c5f51cc116f8e9add9475b41b4c894d6
  Stored in directory: /tmp/pip-ephem-wheel-cache-6pgz5jop/wheels/96/02/a3/318108f401dc37bb3a575e67c80cf111852262a4b3c9f691ec
Successfully built drave

[notice] A new release of pip is available: 26.2.1 -> 26.3
[notice] To update, run: /tmp/venv-drave/bin/python -m pip install --upgrade pip
wheel drave-0.1.0-py3-none-any.whl 1412100
entries 370
tools/adaptateur_langue.py
tools/aiguille.py
tools/aligneur_litteraire.py
tools/amplification.py
tools/analyse_alignement.py
tools/analyse_empreinte.py
tools/analyse_engram.py
tools/analyse_experts_statique.py
tools/analyse_flux.py
tools/analyse_hc.py
tools/analyse_litteraire.py
tools/analyse_octets_par_jeton.py
tools/analyse_reutilisation_experts.py
tools/analyse_union_experts.py
tools/ancre_professeur.py
...
tools/llm: []
golds: []
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && du -sh tools/tests/linguistique; ls tools/tests/linguistique | head; du -sh tools/llm; find tools -maxdepth 2 -name \"__init__.py\" | head -20", "description": "Check gold sizes and subpackages"}`

  ```
2,1M	tools/tests/linguistique
anaphore.py
classement_cible.py
classer_gv.py
evaluer_gold.py
gold_gele.json
gold.json
gold.py
gold_reel_50.py
gold_reel.json
gold_reel.py
552K	tools/llm
tools/jeux/__init__.py
tools/llm/__init__.py
tools/semantique/__init__.py
tools/cerveau/__init__.py
tools/pensee/__init__.py
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short | grep -E \"build/|dist/|egg-info|wheel\" || true; ls -d build dist 2>/dev/null || true", "description": "Check for build artifacts in repo"}`

  ```
build
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -ld build && find build -maxdepth 2 -type d | head -10 && rm -rf -- /home/stephane/Data13TB/stephane/GitHub/Qtrinet/build && echo \"build removed\"", "description": "Remove temporary build directory from repo"}`

  ```
drwxr-xr-x. 1 stephane stephane 42 15 nov 21:45 build
build
build/lib
build/lib/tools
build/bdist.linux-x86_64
build removed
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -ld drave.egg-info && rm -rf -- /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave.egg-info && echo \"egg-info removed\"", "description": "Remove generated egg-info artifact"}`

  ```
drwxr-xr-x. 1 stephane stephane 136 15 nov 21:45 drave.egg-info
egg-info removed
  ```

- **bash** `{"command": "cd /tmp && /tmp/venv-drave/bin/drave --version; echo \"code=$?\"", "description": "Confirm installed command still works after artifact cleanup"}`

  ```
drave 0.1.0
code=0
  ```

- **job_output** `{"job_id": "bash-74", "wait": false}`

  ```
✅ smoke test : Ran 20 tests
  ✅ schéma v2 validé (5 cas v2 + 1 cas v1 + 20 phrases du gold)
  ✅ 50 textes libres : Ran 4 tests
  ✅ restitution v0 : surface exacte (miroir affiché)
  ✅ restitution v1 : forme canonique exacte, miroir strict distinct
  ✅ restitution v2 : rôles lisibles, rendu relu, contrôle détecté
  ✅ restitution v0/v1 : Ran 22 tests
[status: running]
  ```

- **job_output** `{"job_id": "bash-74", "wait": false}`

  ```
✅ restitution v2 : Ran 17 tests
  ✅ schéma v2 : Ran 8 tests
  ✅ refus : JSON avec refus, code 3
[status: running]
  ```

- **job_output** `{"job_id": "bash-74", "wait": true, "timeout_ms": 120000}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifier_faq.py --json > /tmp/faq-check.json && diff -q reports/faq.json /tmp/faq-check.json && echo \"faq.json a jour\"", "description": "Verify FAQ JSON is reproducible", "timeoutMs": 300000}`

  ```
faq.json a jour
  ```

### 👤 Utilisateur

background job bash-74 (bash: cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && bash tools/porte-produit.sh) finished [status: completed, exit code: 0]. Read its output with job_output.

- **job_output** `{"job_id": "bash-74", "wait": false}`

  ```
✅ autotest parallèle : 183/183 portes tenues
✅ porte produit verte
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short | grep -E \"pyproject|empaquetage|verifier_faq|produit/README|faq|en-cours|gitignore|test_empaquetage|build|egg-info\" || true", "description": "Final status of task files"}`

  ```
M .gitignore
 M docs/pilotage/en-cours.md
 M docs/produit/README.md
 M reports/faq.json
 M reports/rapport-faq.md
 M tools/verifier_faq.py
?? pyproject.toml
?? reports/empaquetage.json
?? reports/rapport-empaquetage.md
?? tools/tests/test_empaquetage.py
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py 2>&1 | tail -3; echo \"code=${PIPESTATUS[0]}\"", "description": "Final documentation review", "timeoutMs": 300000}`

  ```
revue de documentation · 760 fiche(s) · 854 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
code=0
  ```

### 🤖 Assistant

Let me also check that the built wheel (non-editable) can run the two required commands, even though the task only requires editable.

- **bash** `{"command": "python3 -m venv --clear /tmp/venv-drave-wheel && /tmp/venv-drave-wheel/bin/python -m pip install --no-deps /tmp/drave-wheel/drave-0.1.0-py3-none-any.whl 2>&1 | tail -4 && cd /tmp && /tmp/venv-drave-wheel/bin/drave --version; echo \"version_code=$?\"; /tmp/venv-drave-wheel/bin/drave anal … [146 caractères tronqués]`

  ```
Successfully installed drave-0.1.0

[notice] A new release of pip is available: 26.2.1 -> 26.3
[notice] To update, run: /tmp/venv-drave-wheel/bin/python -m pip install --upgrade pip
version_code=1
analyser_code=1
[stderr]
Traceback (most recent call last):
  File "/tmp/venv-drave-wheel/bin/drave", line 3, in <module>
    from tools.drave import main
  File "/tmp/venv-drave-wheel/lib64/python3.13/site-packages/tools/drave.py", line 59, in <module>
    import restitution  # noqa: E402  (la restitution v0 : annotation → surface)
    ^^^^^^^^^^^^^^^^^^
  File "/tmp/venv-drave-wheel/lib/python3.13/site-packages/tools/restitution.py", line 40, in <module>
    from tools.tests.linguistique import miroir as _miroir  # noqa: E402
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ModuleNotFoundError: No module named 'tools.tests'
Traceback (most recent call last):
  File "/tmp/venv-drave-wheel/bin/drave", line 3, in <module>
    from tools.drave import main
  File "/tmp/venv-drave-wheel/lib64/python3.13/site-packages/tools/drave.py", line 59, in <module>
    import restitution  # noqa: E402  (la restitution v0 : annotation → surface)
    ^^^^^^^^^^^^^^^^^^
  File "/tmp/venv-drave-wh
… [259 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && find tools/tests -maxdepth 2 -name \"__init__.py\" -print; ls tools/tests/linguistique | head -20; grep -n \"from tools.tests\\|import tools.tests\" tools/restitution.py tools/restitution_v2.py tools/restitution_v3.py tools/bloc_ling … [81 caractères tronqués]`

  ```
anaphore.py
classement_cible.py
classer_gv.py
evaluer_gold.py
gold_gele.json
gold.json
gold.py
gold_reel_50.py
gold_reel.json
gold_reel.py
gold_restitution_v2.json
gold_split.py
gold_synthetique.json
gold_synthetique.py
juge.py
miroir.py
__pycache__
qualifier_cascade.py
qualifier_frontiere_71.py
qualifier_lien_appris.py
tools/restitution.py:40:from tools.tests.linguistique import miroir as _miroir  # noqa: E402
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,80p' tools/tests/linguistique/miroir.py; echo \"---\"; grep -n \"^import\\|^from\" tools/tests/linguistique/miroir.py", "description": "Inspect miroir module imports"}`

  ```
"""Le miroir entrée/sortie du bloc linguistique : restitution et fidélité.

Règle 6 : toute mesure d'entrée se double d'une mesure de sortie. `rendre` reconstruit
le texte depuis les étiquettes de **surface** (`graphème`, `mot`) ; `fidelite` le compare
à la source. La **fluidité** (longueur, ponctuation) n'est pas la **fidélité** : une
restitution peut être fluide et infidèle, ou fidèle et hachée.
"""
from __future__ import annotations

import re

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
import tools.bloc_linguistique as bl
from tools.tests.linguistique.evaluer_gold import charger, evaluer_bloc


def rendre(a: bl.Annotation) -> str:
    """Reconstruit le texte depuis les étiquettes de surface, sans lire `a.texte`."""
    g = [e for e in a.etiquettes if e.niveau == "graphème"]
    if not g:
        return ""
    return "".join(e.valeur for e in sorted(g, key=lambda e: (e.debut, e.fin)))


def fidelite(a: bl.Annotation, source: str) -> float:
    """1.0 si la restitution égale la source, 0.0 sinon (la mesure est binaire ici)."""
    return 1.0 if rendre(a) == source else 0.0


def rendre_mots(a: bl.Annotation) -> str:
    """Rest
… [2113 caractères tronqués]
  ```

### 🤖 Assistant

The editable install is solid. I also probed a non-editable wheel and found a real scope limit; I'll document it honestly rather than hide it.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-empaquetage.md", "limit": 20, "offset": 45}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-empaquetage.md", "limit": 18, "offset": 140}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-empaquetage.md</path>
<type>file</type>
<content>
45:   module que `python3 tools/drave.py`.
46: - **Aucune dépendance d'exécution** (`dependencies = []`). `setuptools>=61` est une dépendance
47:   de **construction**, installée par pip en isolation de build, pas au runtime.
48: - **Le code historique n'est pas modifié** : `tools/drave.py` continue de calculer sa racine
49:   depuis `__file__`, d'ajouter `tools/` à `sys.path` et de fonctionner lancé directement.
50: - **Les artefacts d'installation** sont ignorés (`*.egg-info/`, `/build/`, `/dist/` dans
51:   [`.gitignore`](../.gitignore)).
52: - **Le test** [`tools/tests/test_empaquetage.py`](../tools/tests/test_empaquetage.py) vérifie
53:   les métadonnées, les deux entrées et le contrôle négatif, sans créer de venv ni télécharger.
54: - **La doc** [`docs/produit/README.md`](../docs/produit/README.md) § 8.10 porte désormais les
55:   deux chemins d'installation (historique et `drave`).
56: 
57: **Ce qui n'est pas livré.** Aucune **wheel** n'est construite ni publiée sur PyPI ; l'installation
58: est **éditable** et pointe vers le dépôt. Un wheel non éditable n'
… [224 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-empaquetage.md</path>
<type>file</type>
<content>
140: 4. script console `drave = tools.drave:main` ;
141: 5. `python3 tools/drave.py --version` → `drave 0.1.0` ;
142: 6. `python3 tools/drave.py analyser "Le chat dort."` → `0`, avec `GN` et `Le chat` ;
143: 7. `from tools.drave import main` depuis un **autre** répertoire ;
144: 8. sans installation, `drave` échoue **proprement** (127, `command not found`, pas de trace).
145: 
146: Le test **ne crée pas de venv** et ne télécharge rien : c'est la vérification réelle
147: `pip install -e .` de ce rapport qui couvre l'installation ; le test couvre ce qui doit rester
148: vrai à chaque passe.
149: 
150: ## 6. Ce qui pourrait rendre ce résultat faux
151: 
152: 1. **Le plancher 3.10 n'est pas exécuté.** La mesure tourne en **3.13.16** ; `>= 3.10` est
153:    vérifié par la métadonnée et par l'AST (`ast.parse(..., feature_version=(3, 10))` dans la
154:    FAQ), pas par une exécution réelle en 3.10.
155: 2. **Le build a besoin du réseau ou d'un cache.** pip installe `setuptools>=61` en isolation ;
156:    sur une machine **sans réseau ni cache**, `pip install -e .` échoue
… [197 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-empaquetage.md", "limit": 14, "offset": 158}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-empaquetage.md</path>
<type>file</type>
<content>
158: 3. **L'installation est éditable.** Un wheel non éditable n'a pas été construit ni testé ; il
159:    n'embarquerait pas les gold de `tools/tests/linguistique/`, et `data/` est hors dépôt.
160: 4. **Le contrôle négatif est un `PATH` vidé.** Si un binaire `drave` existait dans `/usr/bin`,
161:    ce contrôle ne représenterait plus « sans installation ». Dans l'environnement mesuré, il
162:    n'y en avait pas.
163: 5. **Le script console dépend du namespace `tools`.** Il a été vérifié depuis `/tmp` avec le
164:    Python du venv ; un autre interpréteur, ou un `tools` homonyme sur le `PYTHONPATH`, pourrait
165:    changer la résolution.
166: 
167: ## 7. Les fichiers
168: 
169: - [`pyproject.toml`](../pyproject.toml) — le paquet minimal.
170: - [`tools/tests/test_empaquetage.py`](../tools/tests/test_empaquetage.py) — les 8 contrôles.
171: - [`reports/empaquetage.json`](empaquetage.json) — le relevé complet.

(Showing lines 158-171 of 174. Use offset=172 to continue.)
</content>
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-empaquetage.md", "limit": 30, "offset": 105}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-empaquetage.md</path>
<type>file</type>
<content>
105: **Deux vérifications de plus, propres à l'installation.** `drave evaluer --json` depuis `/tmp`
106: rend `0` et lit le gold **vivant** : sous installation éditable, `RACINE` dans
107: `tools/drave.py` résout bien le dépôt, pas le répertoire courant. `drave analyser … --tagger`
108: sans clé rend **4** avec `stdout` vide : le sous-module optionnel `tools.llm.deepseek` est
109: importable sous l'installation éditable, et l'absence de clé reste un refus propre.
110: 
111: ## 4. Le contrôle négatif
112: 
113: Le contrôle négatif est le **même nom de commande, sans l'installation**. On vide le `PATH` et
114: on retire `PYTHONPATH` / `VIRTUAL_ENV`, puis on lance depuis `/tmp` :
115: 
116: ```bash
117: env -i PATH=/usr/bin:/bin HOME=/tmp bash -c 'drave --version'
118: # code 127
119: # stdout : (vide)
120: # stderr : bash: line 1: drave: command not found
121: ```
122: 
123: **Lecture.** L'échec est **propre** : c'est un échec de **résolution** (127), pas une trace
124: Python, pas un import partiel, pas un code 0 trompeur. Si `drave` restait résolu sans
125: instal
… [285 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-empaquetage.md", "new_string": "**Ce qui n'est pas livré.** Aucune **wheel** n'est construite ni publiée sur PyPI ; l'installation\nest **éditable** et pointe vers le dépôt. Un wheel non éditable, construit à part pour vé … [560 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-empaquetage.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-empaquetage.md", "new_string": "**Deux vérifications de plus, propres à l'installation.** `drave evaluer --json` depuis `/tmp`\nrend `0` et lit le gold **vivant** : sous installation éditable, `RACINE` dans\n`tools/drave. … [1168 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-empaquetage.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-empaquetage.md", "new_string": "3. **L'installation est éditable.** Un wheel non éditable, construit à part, **échoue à\n   l'import** (`No module named 'tools.tests'`) : il n'embarque ni `tools/tests` ni les gold de\n    … [295 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-empaquetage.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/empaquetage.json", "new_string": " \"test\": {\n  \"fichier\": \"tools/tests/test_empaquetage.py\",\n  \"commande\": \"python3 tools/tests/test_empaquetage.py\",\n  \"code\": 0,\n  \"tests\": 8,\n  \"echecs\": 0,\n  \"resultat\": … [2024 caractères tronqués]`

  ```
Error: old_string was not found in "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/empaquetage.json"
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/empaquetage.json", "limit": 22, "offset": 95}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/empaquetage.json</path>
<type>file</type>
<content>
95:   "code": 0,
96:   "tests": 8,
97:   "echecs": 0,
98:   "resultat": "OK"
99:  },
100:  "ce_qui_pourrait_rendre_faux": [
101:   "La mesure tourne en Python 3.13.16 ; le plancher >=3.10 est vérifié par la métadonnée et l'AST, pas par une exécution en 3.10.",
102:   "pip installe setuptools>=61 en isolation de build : une machine sans réseau ni cache échoue avant l'installation.",
103:   "L'installation est éditable ; un wheel non éditable n'embarque pas les gold de tools/tests/linguistique (data/ est hors dépôt).",
104:   "Le contrôle négatif utilise un PATH vidé ; si un binaire drave existait dans /usr/bin, il ne représenterait plus « sans installation ».",
105:   "Le script console dépend du namespace package tools ; il a été vérifié depuis /tmp, pas depuis un autre interpréteur."
106:  ],
107:  "fichiers": [
108:   "pyproject.toml",
109:   "tools/tests/test_empaquetage.py",
110:   "reports/rapport-empaquetage.md",
111:   "reports/empaquetage.json",
112:   "docs/produit/README.md#810-comment-linstaller-et-le-lancer"
113:  ],
114:  "conclusion": "pyproject minimal in
… [291 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/empaquetage.json", "new_string": " \"hors_perimetre\": {\n  \"wheel_non_editable\": {\n   \"construit\": true,\n   \"installation\": \"pip install --no-deps drave-0.1.0-py3-none-any.whl\",\n   \"code\": 1,\n   \"erreur\": \"Modul … [1606 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/empaquetage.json has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -m json.tool reports/empaquetage.json >/dev/null && echo \"JSON OK\" && python3 tools/revue_documentation.py 2>&1 | tail -3; echo \"code=${PIPESTATUS[0]}\"", "description": "Validate JSON and docs after edit", "timeoutMs": 30 … [5 caractères tronqués]`

  ```
JSON OK
  revue de documentation · 760 fiche(s) · 854 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
code=0
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-empaquetage.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-empaquetage.md</path>
<type>file</type>
<content>
1: # T1 — l'empaquetage : `pip install -e .`, `drave` hors du dépôt, chemin historique intact
2: 
3: > **Ligne de roadmap** : **B13** (produit) · **Tâche** : **T1** (exploitable, 1/5) ·
4: > **Date** : 2026-11-15 · **Verdict** : ✅ **empaquetage minimal livré**.
5: >
6: > **Le chiffre.** `pyproject.toml` : nom **drave**, version **0.1.0**, `requires-python >= 3.10`,
7: > **0** dépendance d'exécution, script console `drave = tools.drave:main`.
8: > `python3 -m pip install -e .` dans **`/tmp/venv-drave`** (Python **3.13.16**, pip **26.2.1**)
9: > rend **0** et `Successfully installed drave-0.1.0` ; `drave --version` rend **`drave 0.1.0`**
10: > et `drave analyser "Le chat dort."` rend **0** depuis **`/tmp`**. Le **contrôle négatif** —
11: > le même nom sans installation — échoue **proprement** : code **127**, `command not found`,
12: > **aucune** trace Python. Le chemin historique `python3 tools/drave.py` reste **vert**.
13: >
14: > **Dispositif** : [`pyproject.toml`](../pyproject.toml),
15: > [`tools/tests/test_empaquetage.py`](../tools/tests/test_empaquetage.py),
1
… [9007 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-empaquetage.md", "new_string": "**Ce qui n'est pas livré.** Aucune **wheel** n'est livrée ni publiée sur PyPI ; l'installation\nest **éditable** et pointe vers le dépôt. Un wheel non éditable, construit à part pour vérifi … [791 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-empaquetage.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/tests/test_empaquetage.py 2>&1 | tail -4 && python3 tools/verifier_faq.py 2>&1 | tail -2 && python3 tools/revue_documentation.py 2>&1 | tail -2", "description": "Final tests, FAQ, and doc review", "timeoutMs": 300000}`

  ```
----------------------------------------------------------------------
Ran 8 tests in 0.541s

OK
  ✅ 10. Comment l'installer et le lancer ?
✅ FAQ vérifiée
  revue de documentation · 760 fiche(s) · 854 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ```

- **bash** `{"command": "cd /tmp && /tmp/venv-drave/bin/drave --version && /tmp/venv-drave/bin/drave analyser \"Le chat dort.\" >/dev/null; echo \"installed_analyser_code=$?\"; env -i PATH=/usr/bin:/bin HOME=/tmp bash -c 'drave --version' >/dev/null 2>/tmp/final-neg.err; echo \"negative_code=$?\"; cat /tmp/fina … [206 caractères tronqués]`

  ```
drave 0.1.0
installed_analyser_code=0
negative_code=127
bash: line 1: drave: command not found
historical_code=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short | grep -E \"pyproject|empaquetage|verifier_faq|produit/README|faq|en-cours|gitignore|test_empaquetage\" && echo \"--- artifacts ---\" && (ls -d build dist *.egg-info 2>/dev/null || echo \"aucun artefact de build\") … [57 caractères tronqués]`

  ```
M .gitignore
 M docs/pilotage/en-cours.md
 M docs/produit/README.md
 M reports/faq.json
 M reports/rapport-faq.md
 M tools/verifier_faq.py
?? pyproject.toml
?? reports/empaquetage.json
?? reports/rapport-empaquetage.md
?? tools/tests/test_empaquetage.py
--- artifacts ---
aucun artefact de build
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_empaquetage.py", "limit": 16, "offset": 105}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_empaquetage.py</path>
<type>file</type>
<content>
105:         """PATH vide : le nom `drave` n'est pas résolu, et l'échec est lisible."""
106:         with tempfile.TemporaryDirectory() as tmp:
107:             env = dict(os.environ)
108:             env["PATH"] = tmp  # aucun binaire, donc aucun `drave`
109:             for cle in ("PYTHONPATH", "VIRTUAL_ENV", "PYTHONHOME"):
110:                 env.pop(cle, None)
111:             bash = shutil.which("bash") or "/bin/bash"
112:             r = _executer([bash, "-c", "drave --version"], pathlib.Path(tmp), env=env)
113:             self.assertEqual(r.returncode, 127, (r.stdout, r.stderr))
114:             self.assertIn("command not found", r.stderr.lower())
115:             self.assertNotIn("traceback", r.stderr.lower())
116: 
117: 
118: if __name__ == "__main__":
119:     unittest.main(verbosity=2)

(End of file - total 119 lines)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_empaquetage.py", "new_string": "            env = dict(os.environ)\n            env[\"PATH\"] = tmp  # aucun binaire, donc aucun `drave`\n            for cle in (\"PYTHONPATH\", \"VIRTUAL_ENV\", \"PYTHONHOME\", \"BASH_EN … [285 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_empaquetage.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/tests/test_empaquetage.py 2>&1 | tail -4", "description": "Re-run test after robustness edit"}`

  ```
----------------------------------------------------------------------
Ran 8 tests in 0.577s

OK
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,140p' reports/empaquetage.json", "description": "Review final report JSON"}`

  ```
{
 "schema": "drave.empaquetage.verification",
 "version": 1,
 "date": "2026-11-15",
 "tache": "T1 (exploitable, 1/5)",
 "produit": "0.1.0",
 "pyproject": {
  "fichier": "pyproject.toml",
  "nom": "drave",
  "version": "0.1.0",
  "requires_python": ">=3.10",
  "dependances": [],
  "script_console": "drave = tools.drave:main",
  "build_backend": "setuptools.build_meta",
  "build_requires": ["setuptools>=61"],
  "packages": ["tools"]
 },
 "environnement": {
  "venv": "/tmp/venv-drave",
  "python": "3.13.16",
  "pip": "26.2.1",
  "commande": "python3 -m pip install -e .",
  "cwd": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet",
  "code": 0,
  "resultat": "Successfully installed drave-0.1.0",
  "editable": true,
  "pip_show": {
   "name": "drave",
   "version": "0.1.0",
   "requires": [],
   "editable_project_location": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"
  }
 },
 "sorties": {
  "drave_version": {
   "commande": "drave --version",
   "cwd": "/tmp",
   "code": 0,
   "stdout": "drave 0.1.0"
  },
  "drave_analyser": {
   "commande": "drave analyser \"Le chat dort.\"",
   "cwd": "/tmp",
   "code": 0,
   "stdout_extrait": [
    "drave 0.1.0 — analyse heuristique (CPU, hors 
… [3231 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifie_en_cours.py 2>&1 | tail -4; echo \"code=${PIPESTATUS[0]}\"", "description": "Final state doc check", "timeoutMs": 120000}`

  ```
en-cours · 1630 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
code=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/taille_documents.py 2>&1 | tail -3; echo \"code=${PIPESTATUS[0]}\"", "description": "Final context budget check", "timeoutMs": 120000}`

  ```
· 63 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
code=0
  ```

### 🤖 Assistant

## T1 — empaquetage : terminé

### Livré

- **`pyproject.toml`** : nom `drave`, version `0.1.0`, `requires-python = ">=3.10"`, `dependencies = []`, backend `setuptools.build_meta`, script console :
  ```toml
  [project.scripts]
  drave = "tools.drave:main"
  ```
- **`tools/tests/test_empaquetage.py`** : 8 tests (métadonnées, script console, chemin historique, import hors dépôt, contrôle négatif).
- **`reports/rapport-empaquetage.md`** + **`reports/empaquetage.json`**.
- **`docs/produit/README.md` § 8.10** : les deux chemins d'installation (historique et `drave`).
- **FAQ mise à jour** : `tools/verifier_faq.py`, `reports/faq.json`, `reports/rapport-faq.md` ne prétendent plus qu'il n'y a pas d'empaquetage.
- **`.gitignore`** : `*.egg-info/`, `/build/`, `/dist/`.
- Compteurs d'état ajustés (`760` fiches / `854` JSON).

### Vérifications réelles

| contrôle | résultat |
|---|---|
| `python3 -m pip install -e .` dans `/tmp/venv-drave` (Python 3.13.16, pip 26.2.1) | **0**, `Successfully installed drave-0.1.0` |
| `drave --version` depuis `/tmp` | **0**, `drave 0.1.0` |
| `drave analyser "Le chat dort."` depuis `/tmp` | **0**, `GN Le chat rôle=agent`, `GV dort` |
| `drave evaluer --json` depuis `/tmp` | **0**, gold vivant lu (donc `RACINE` résout bien le dépôt) |
| `drave … --tagger` sans clé | **4**, `stdout` vide, message propre |
| `python3 tools/drave.py --version` | **0** — chemin historique intact |
| **contrôle négatif** : `drave` avec `PATH` vidé, sans install | **127**, `command not found`, aucune trace Python |
| `python3 tools/tests/test_empaquetage.py` | **8/8 OK** |
| `python3 tools/verifier_faq.py` | **10/10** + contrôle négatif détecté |
| `python3 tools/revue_documentation.py` | ✅ |
| `bash tools/porte-produit.sh` | ✅ **183/183 portes tenues** |

### Limite documentée

Un wheel **non éditable** construit à part échoue à l'import : `ModuleNotFoundError: No module named 'tools.tests'` (il n'embarque ni `tools/tests` ni les gold). Ce n'est pas le chemin demandé — l'installation validée est **éditable** — mais la limite est écrite dans la fiche et le JSON.

Les changements sont dans l'arbre de travail, **non committés**.

