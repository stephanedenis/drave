# Session DSH — relecture

- identifiant : `bd6322ed-6792-4188-9d4c-6cae09c3ef4e`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-06 09:31:04
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python, dépôt Drave). Mission : **prototyper le point d'entrée produit** — une CLI unique qui expose le bloc linguistique.

Contexte : `tools/bloc_linguistique.py` expose `Heuristique` (méthode `analyser(texte, langue) -> Annotation` avec `.etiquettes` (niveau/type/valeur/debut/fin/confiance/candidats/meta), `.unites`, `.trace`, `.cout`) ; `NeuronalLLM`, `Parallele`, `Cascade`, `MockNeuronal` ; `tools/tests/linguistique/evaluer_gold.py` (`charger`, `evaluer_bloc`). Lis d'abord le module pour connaître l'API exacte.

À faire :
1. Écris **`tools/drave.py`** (fichier neuf, autonome, `python3 tools/drave.py ...`) avec des sous-commandes :
   - `analyser TEXTE [--langue fr|en] [--json]` : sortie lisible (POS compact, syntagmes avec rôle et cible d'attachement, pragmatique) ou JSON complet ;
   - `evaluer [--gold]` : mesure l'heuristique sur le gold (POS, syntagmes F1/tête, attachement exact/couverture) ;
   - `rejouer TEXTE` : analyse deux fois et vérifie le déterminisme (rejeu identique) ;
   - `--version` et `--aide`.
   Contraintes : n'importe **que** le dépôt (`sys.path.insert(0, '.')`), aucun réseau, aucun GPU, sortie déterministe, codes de sortie 0/2 (usage) /1 (erreur).
2. Écris **`tools/tests/test_produit.py`** (fichier neuf) : un smoke test de bout en bout (5–8 assertions) — analyse d'une phrase française et d'une phrase anglaise (types attendus), déterminisme, JSON valide, `--version`, code de sortie d'usage. Il doit passer en `python3 tools/tests/test_produit.py` **et** être compatible `pytest`.
3. Mesure et note dans ton résumé : temps d'exécution, taille de la sortie JSON pour 1 phrase et pour le gold, et tout ce qui n'est **pas** exposable aujourd'hui (par ex. la restitution, la traduction).
4. **N'écris que ces deux fichiers neufs.** Ne modifie aucun fichier existant ; ne touche pas `docs/pilotage/`, `AGENTS.md`, `journal/`, `tools/structures/`, `data/`, `tools/entrainer_native.py`, `tools/native_model.py`. Ne commite rien.

Rends un résumé : les commandes, la sortie d'exemple, les mesures, les limites.
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

⏵ Reading the linguistic block module and existing tools

- **bash** `{"command": "ls tools/ | head -50; echo ---; ls tools/tests/linguistique/ 2>/dev/null | head; echo ---; git status --porcelain | head -20; git branch --show-current", "description": "List tools and check branch status"}`

  ```
adaptateur_langue.py
aiguille.py
aligneur_litteraire.py
amplification.py
analyse_alignement.py
analyse_empreinte.py
analyse_engram.py
analyse_experts_statique.py
analyse_flux.py
analyse_hc.py
analyse_litteraire.py
analyse_octets_par_jeton.py
analyse_reutilisation_experts.py
analyse_union_experts.py
ancre_professeur.py
applique_pont.py
approximabilite_bloc.py
apres-telechargement-k3.sh
archive_sessions.py
audit_drapeaux_harnais.py
banc_complet.py
banc_durci.py
banc-experts.py
banc_lecteur.py
banc_lecture.py
banc-prelire.py
blanchiment_entree.py
bloc_code.py
bloc_linguistique.py
bloc_maths.py
bloc_tableaux.py
boucle-cerveau.sh
boucle_directe.py
bruit_entree.py
budget_execution_locale.py
c4_retard.sh
c8_carte_profondeur.sh
c8_corpus.sh
c8_entrainer_tete.py
c8_sonde_lineaire.py
cache_pont.py
calibre_modes.py
calibrer.py
campagne-benefices.sh
campagne_synthese.py
canal_structure.py
cancellation_langue.py
carte_chantiers.py
carte_coupe.sh
carte_decisions.py
---
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
---
MM journal/2026-11-05/README.md
D  journal/2026-11-05/attention.md
MM journal/202
… [693 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py"}`

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
… [54475 caractères tronqués]
  ```

- **bash** `{"command": "wc -l tools/bloc_linguistique.py tools/tests/linguistique/evaluer_gold.py; echo ---; grep -n \"^class \\|^def \\|^    def \\|^if __name__\" tools/bloc_linguistique.py | tail -80", "description": "Inspect structure of module"}`

  ```
2192 tools/bloc_linguistique.py
   305 tools/tests/linguistique/evaluer_gold.py
  2497 total
---
199:def detecter_langue(texte: str, profils: dict[str, dict] | None = None,
230:def _script_char(ch: str) -> str:
256:def detecter_script(texte: str) -> str:
461:def _est_adverbe_seul(g: dict) -> bool:
473:def _sans_enclitique(mot: str) -> str:
481:def _est_verbe(mot: str) -> bool:
500:def _role_gp(prep: str) -> str:
525:class Heuristique:
530:    def __init__(self, profils: dict[str, dict] | None = None, segmenter_s: bool = True,
540:    def _langue(self, texte: str, indice: str | None) -> tuple[str, float, str]:
549:    def _mots(texte: str) -> list[tuple[int, int, str, str]]:
568:    def _phrases(texte: str) -> list[tuple[int, int, str, str]]:
590:    def _negation(phrase: str) -> bool:
595:    def _modalite(phrase: str) -> bool:
601:    def _pos(self, langue: str, mot: str) -> tuple[str, bool, float]:
627:    def _morphemes(mot: str) -> list[tuple[str, int, int, str]]:
641:    def _syntagmes_s(self, texte: str) -> list[dict] | None:
652:    def _cibles_s(self, texte: str) -> dict:
670:    def _cible_precedent(texte: str, segment: dict, precedent: dict | None, verbes) -> str | None:

… [3723 caractères tronqués]
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
… [15928 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "offset": 981, "limit": 330}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
981:                 continue
982:             if typ == "mot" and n in lex.get("PREP", set()) and i + 1 < len(mots):
983:                 j = i + 1
984:                 # le GP s'arrête au verbe ou au relatif : « de la voisine | dort » et non
985:                 # « de la voisine dort » (mesuré : 25 spans « plus large » sur le gold).
986:                 while (j < len(mots) and mots[j][3] == "mot"
987:                        and not (est_verbe(mots[j][0], mots[j][2])
988:                                 and not (j > i + 1 and _normaliser(mots[j - 1][2]) in lex.get("DET", set())))
989:                        and _normaliser(mots[j][2]) not in RELATIFS):
990:                     j += 1
991:                 # « à manger » : un GP réduit à sa préposition prend le verbe qui suit
992:                 if j == i + 1 and j < len(mots) and est_verbe(mots[j][0], mots[j][2]):
993:                     j += 1
994:                 segments.append({"type": "GP", "role": _role_gp(t), "niveau": 1,
995:                                  "debut": d, "fin": mots[j - 1][1],
996:         
… [21048 caractères tronqués]
  ```

- **bash** `{"command": "ls tools/drave.py 2>&1; python3 --version; git log --oneline -3; echo ---; sed -n '2120,2192p' tools/bloc_linguistique.py", "description": "Check CLI conventions and Python version"}`

  ```
ls: cannot access 'tools/drave.py': No such file or directory
Python 3.13.16
fa1b0c6e ÉTAT — MASTER EST À JOUR : s/v7 FAST-FORWARDÉ ET POUSSÉ (375 COMMITS, af28eadd..789b1284)
789b1284 DOCS — LA PASSE DU 06/11 EN UNE LIGNE ET L'ANCIENNE COMPRESSÉE (BUDGET T1)
f0e3f46a DOCS — LA PASSE DU 06/11 EN UNE LIGNE
---
        sortie.write_text(json.dumps(rapport, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return rapport


# --------------------------------------------------------------------------- CLI


def _annotation_depuis_args(args) -> Annotation:
    if args.texte:
        texte = args.texte
    elif args.fichier:
        texte = pathlib.Path(args.fichier).read_text(encoding="utf-8")
    else:
        texte = sys.stdin.read()
    profils = None
    if args.profils:
        profils, _ = charger_profils_udhr(pathlib.Path(args.profils))
    h = Heuristique(profils=profils)
    n = MockNeuronal(profils)
    if args.mode == "heuristique":
        return h.analyser(texte, args.langue, args.contexte)
    if args.mode == "neuronal":
        if args.neuronal_reel:
            return NeuronalLLM(args.modele).analyser(texte, args.langue, args.contexte)
        return n.analyser(
… [2495 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys, time, json\nsys.path.insert(0, 'tools')\nimport bloc_linguistique as bl\nh = bl.Heuristique()\nfor t, lg in [(\"Le chat de la voisine qui dort sur le toit se réveille.\", \"fr\"),\n              (\"The cat that sleeps on the roof wakes up.\", \"en\"),\n     … [596 caractères tronqués]`

  ```
==== fr Le chat de la voisine qui dort sur le toit se réveille. duree 0.0064 langue fr
pos DET 'Le' 0 2 meta {'ouvert': False} cand []
syntagme GN 'Le chat' 0 7 meta {'role': 'agent', 'niveau': 1, 'attachement': {'segment': 'Le chat', 'cible': 'réveille'}} cand ['« qui dort sur le toit » → voisine', '« qui dort sur le toit » → Le chat', 'réveille', 'voisine']
phrase type 'déclarative' 0 55 meta {} cand []
pragmatique acte 'assertion' 0 55 meta {} cand ['assertion', 'question', 'ordre']
pos NOUN 'chat' 3 7 meta {'ouvert': True} cand ['noun']
pos PREP 'de' 8 10 meta {'ouvert': False} cand []
syntagme GP 'de la voisine' 8 21 meta {'role': 'possession', 'niveau': 2, 'attachement': {'segment': 'de la voisine', 'cible': 'réveille'}} cand ['« qui dort sur le toit » → voisine', '« qui dort sur le toit » → Le chat', 'réveille', 'voisine']
pos DET 'la' 11 13 meta {'ouvert': False} cand []
pos NOUN 'voisine' 14 21 meta {'ouvert': True} cand ['noun']
pos PRON 'qui' 22 25 meta {'ouvert': False} cand []
syntagme REL 'qui dort sur le toit' 22 42 meta {'role': 'qualite', 'niveau': 2, 'attachement': {'segment': 'qui dort sur le toit', 'cible': 'voisine'}} cand ['« qui dort sur le toit » → voisine',
… [2791 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys, time, json\nsys.path.insert(0, 'tools')\nimport bloc_linguistique as bl\nh = bl.Heuristique()\nfor t, lg in [(\"The cat sleeps on the roof.\", \"en\"),\n              (\"Le chat dort.\", \"fr\"),\n              (\"La voisine prépare un gâteau.\", \"fr\"),\n … [543 caractères tronqués]`

  ```
==== en 'The cat sleeps on the roof.' langue= en
POS: [('The', 'DET'), ('cat', 'NOUN'), ('sleeps', 'VERB'), ('on', 'PREP'), ('the', 'DET'), ('roof', 'NOUN')]
SYN: [('GN', 'The cat', 'groupe nominal', 'sleeps'), ('GV', 'sleeps', 'prédicat', None), ('GP', 'on the roof', 'lieu', 'sleeps')]
PRAG: [('acte', 'assertion')]
==== fr 'Le chat dort.' langue= fr
POS: [('Le', 'DET'), ('chat', 'NOUN'), ('dort', 'VERB')]
SYN: [('GN', 'Le chat', 'agent', 'dort'), ('GV', 'dort', 'predicat', 'chat')]
PRAG: [('acte', 'assertion')]
==== fr 'La voisine prépare un gâteau.' langue= fr
POS: [('La', 'DET'), ('voisine', 'NOUN'), ('prépare', 'NOUN'), ('un', 'DET'), ('gâteau', 'NOUN')]
SYN: [('GN', 'La voisine prépare un gâteau', 'agent', None)]
PRAG: [('acte', 'assertion')]
==== en 'The dog runs in the garden.' langue= en
POS: [('The', 'DET'), ('dog', 'NOUN'), ('runs', 'NOUN'), ('in', 'PREP'), ('the', 'DET'), ('garden', 'NOUN')]
SYN: [('GN', 'The dog', 'groupe nominal', 'runs'), ('GV', 'runs', 'prédicat', None), ('GP', 'in the garden', 'lieu', 'runs')]
PRAG: [('acte', 'assertion')]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys, time, json, importlib.util\nsys.path.insert(0, 'tools')\nspec = importlib.util.spec_from_file_location(\"eg\", \"tools/tests/linguistique/evaluer_gold.py\")\neg = importlib.util.module_from_spec(spec); spec.loader.exec_module(eg)\nt0=time.perf_counter(); ph … [571 caractères tronqués]`

  ```
phrases 612 chargement 0.0122
eval duree 0.363
{"pos": {"exactitude": 0.7581, "exactitude_ferme": 0.9004, "exactitude_ouvert": 0.6234, "tokens": 3179, "confusions": {"ADJ": {"ADJ": 50, "NOUN": 80, "VERB": 4}, "ADV": {"ADV": 117, "NOUN": 20, "PREP": 2, "ADJ": 1, "?": 1}, "AUX": {"PREP": 4, "AUX": 118, "?": 3, "NOUN": 3}, "CONJ": {"CONJ": 44, "PRON": 25, "DET": 12, "?": 13, "PREP": 2, "NOUN": 2}, "DET": {"DET": 586, "?": 2}, "NOUN": {"NOUN": 657, "ADJ": 17, "VERB": 7, "?": 1}, "NUM": {"NUM": 2}, "PONCT": {"?": 25}, "PREP": {"PREP": 114}, "PRON": {"PRON": 411, "NOUN": 8, "?": 30, "DET": 25, "CONJ": 1}, "VERB": {"VERB": 311, "NOUN": 450, "ADJ": 5, "PREP": 2, "?": 16, "AUX": 7, "ADV": 1}}}, "syntagme": {"precision": 0.6292, "rappel": 0.5464, "f1": 0.5849, "tp": 1018, "fp": 600, "fn": 845, "tete": {"precision": 0.81, "rappel": 0.6704, "f1": 0.7336, "tp": 1249, "fp": 293, "fn": 614}}, "attachement": {"cibles": 239, "labels": 222, "top1": 222, "topk": 221, "exact": 222, "top1_taux": 0.9289, "topk_taux": 0.9247, "exact_taux": 0.9289, "exact_any": 222, "exact_any_taux_span": 1.0, "top1_taux_span": 1.0, "topk_taux_span": 0.9955, "topk_exact": 221, "topk_exact_taux": 0.9247, "topk_exact_taux_s
… [374 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"drave.py\\|point d'entrée produit\\|CLI unique\\|interface produit\" --include=*.md --include=*.py --include=*.sh . 2>/dev/null | head -20", "description": "Search repo for entry-point mentions"}`

  ```
./reports/rapport-e5-distillation.md:126:  --adapter-sortie`, (c) la mesure de l'**accord** par `speculatif_drave.py` (le **taux
./reports/rapport-speculatif-reflexe.md:19:> Protocole : `tools/speculatif_drave.py` (nouveau) · le brouillon et le vérificateur sont **le même
./reports/rapport-speculatif-reflexe.md:64:  **exécutable dans ce dépôt** (`tools/speculatif_drave.py`), avec ses chiffres ;
./reports/rapport-speculatif-reflexe.md:194:(`tools/speculatif_drave.py`, bras **`ngram:N`**, coût **mesuré**, pas décrété ✗). Avec `c ≈ 0`, toute
./tools/speculatif_drave.py:2:"""speculatif_drave.py — LE RÉFLEXE PROPOSE, LE CERVEAU VÉRIFIE — et on mesure le taux.
./tools/speculatif_drave.py:25:  python tools/speculatif_drave.py --n 24 --K 4 \\
./tools/porte-speculatif.sh:40:$P tools/speculatif_drave.py --n "$N" --K 4 --invite "$INVITE" --json "$T/pilote.json" \
./tools/porte-speculatif.sh:76:    $P tools/speculatif_drave.py --n 12 --K 4 --invite "$INVITE" --json "$T/distille.json" \
./tools/porte-speculatif.sh:95:$P tools/speculatif_drave.py --n 4 --K 2 --invite "$INVITE" \
./tools/n4_dessin_b.py:601:                         "s'évalue par son TAUX D'ACCEPTATION (`tools/speculatif_drave.py`)
… [3280 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,60p' tools/tests/linguistique/gold_gele.json | head -5; echo ---; python3 - <<'PY'\nimport json\nfor f in [\"tools/tests/linguistique/gold_gele.json\",\"tools/tests/linguistique/gold.json\",\"tools/tests/linguistique/gold_reel.json\",\"tools/tests/linguistique/gold_synthetique … [203 caractères tronqués]`

  ```
{
"gele": "2026-11-02",
"phrases": [
{
"id": "g001",
---
tools/tests/linguistique/gold_gele.json ['gele', 'phrases'] 602
  cles phrase: ['id', 'langue', 'texte', 'mots', 'segments', 'pragma', 'source']
tools/tests/linguistique/gold.json ['version', 'phrases', 'note'] 20
  cles phrase: ['id', 'langue', 'texte', 'mots', 'segments', 'pragma']
tools/tests/linguistique/gold_reel.json ['version', 'source', 'note', 'phrases'] 432
  cles phrase: ['id', 'langue', 'texte', 'mots', 'segments', 'pragma', 'source']
tools/tests/linguistique/gold_synthetique.json ['version', 'source', 'graine', 'note', 'phrases'] 160
  cles phrase: ['id', 'langue', 'texte', 'pragma', 'source', 'mots', 'segments']
  ```

- **bash** `{"command": "for i in 1 2 3 4 5; do python3 tools/bloc_linguistique.py --texte \"Le chat de la voisine qui dort sur le toit se réveille.\" --langue fr --json > /tmp/dr_$i.json; done; md5sum /tmp/dr_*.json; echo ---; for i in 1 2 3; do python3 tools/bloc_linguistique.py --texte \"The cat sleeps on th … [195 caractères tronqués]`

  ```
b23f2019ee1fa0e50686534b8531cacc  /tmp/dr_1.json
b23f2019ee1fa0e50686534b8531cacc  /tmp/dr_2.json
b23f2019ee1fa0e50686534b8531cacc  /tmp/dr_3.json
b23f2019ee1fa0e50686534b8531cacc  /tmp/dr_4.json
b23f2019ee1fa0e50686534b8531cacc  /tmp/dr_5.json
---
2819098e0ea83d01fef651d849bad1e9  /tmp/de_1.json
2819098e0ea83d01fef651d849bad1e9  /tmp/de_2.json
2819098e0ea83d01fef651d849bad1e9  /tmp/de_3.json
---
16100 /tmp/dr_1.json
 8704 /tmp/de_1.json
24804 total
  ```

- **bash** `{"command": "grep -rn \"__version__\\|VERSION = \\|--version\" --include=*.py tools/ | head -20", "description": "Look at version conventions"}`

  ```
tools/flux_codec.py:31:VERSION = 2        # ce que ce fichier ÉCRIT ; il LIT la 1, la 2 et la 3
tools/exporter_gguf.py:39:GGUF_VERSION = 3
tools/jeux/rsn.py:38:VERSION = 1
tools/semantique/universaux.py:49:VERSION = 1
tools/cerveau/pipeline_semantique_m2.py:792:            "torch": torch.__version__,
tools/docwatch/src/docwatch/cli.py:10:from . import __version__
tools/docwatch/src/docwatch/cli.py:56:    p.add_argument("--version", action="version", version="%(prog)s " + __version__)
tools/docwatch/src/docwatch/docopen.py:22:from . import __version__
tools/docwatch/src/docwatch/docopen.py:104:    p.add_argument("--version", action="version", version="%(prog)s " + __version__)
tools/docwatch/src/docwatch/__init__.py:7:__version__ = "0.6.0"
tools/docwatch/src/docwatch/__init__.py:8:__all__ = ["__version__"]
tools/docwatch/src/docwatch/server.py:22:from . import __version__, diagrams
tools/docwatch/src/docwatch/server.py:64:        server_version = "docwatch/" + __version__
tools/docwatch/tests/test_cli.py:9:from docwatch import __version__
tools/docwatch/tests/test_cli.py:16:        main(["--version"])
tools/docwatch/tests/test_cli.py:18:    assert __version__ in capsys.readouterr().
… [476 caractères tronqués]
  ```

- **bash** `{"command": "ls tools/tests/ | head; echo ---; ls tools/tests/*.py | head; echo ---; python3 - <<'PY'\nimport sys\nsys.path.insert(0,'.')\nimport pytest\nprint(\"pytest\", pytest.__version__)\nPY", "description": "Check tests layout and pytest availability"}`

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
---
tools/tests/qualifier_politique_drvm.py
tools/tests/qualifier_porte_bouge_drvm.py
tools/tests/qualifier_porte_drvm.py
tools/tests/qualifier_porte_fenetre_drvm.py
tools/tests/qualifier_porte_minute_drvm.py
tools/tests/qualifier_porte_mobile_drvm.py
tools/tests/qualifier_porte_sto_drvm.py
tools/tests/qualifier_porte_sto_graines.py
tools/tests/test_pensee_politique.py
tools/tests/test_pensee_store.py
---
pytest 9.1.1
  ```

- **bash** `{"command": "sed -n '1,80p' tools/tests/test_pensee_politique.py", "description": "Read existing test style"}`

  ```
"""Tests de la politique DRVM/native — le contrat sans modèle, puis le refus."""
import pathlib
import sys
import unittest

RACINE = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RACINE))
from tools.pensee.operateurs import (BUT_C, CADENAS, LABYRINTHE, LABYRINTHE_PORTE,  # noqa: E402
                                     L_BUT, P_BUT, PolitiqueLLM)


class TestPolitiqueLLM(unittest.TestCase):
    def test_cadenas(self):
        p = PolitiqueLLM("faux", jeu="cadenas", transport=lambda *_: "avant")
        self.assertEqual(p.propose(CADENAS.initial(), BUT_C), "avant")
        self.assertGreater(p.latence, 0.0)

    def test_cadenas_variantes(self):
        etat = CADENAS.initial()
        minimal = PolitiqueLLM("faux", jeu="cadenas", variante="minimal")
        regle = PolitiqueLLM("faux", jeu="cadenas", variante="regle")
        self.assertNotIn("augmente", minimal._invite(etat, BUT_C))
        self.assertIn("augmente", regle._invite(etat, BUT_C))

    def test_porte(self):
        p = PolitiqueLLM("faux", jeu="porte", transport=lambda *_: "bas")
        self.assertEqual(p.propose(LABYRINTHE_PORTE.initial(), P_BUT), "bas")
        invite = p._invite(LABYRINTHE_PO
… [2106 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,80p' tools/tests/test_pensee_store.py", "description": "Read second test style"}`

  ```
"""Tests du store de Pensée — la file FIFO ne se fige pas.

Le bug (03/11) : `push` numérotait avec `len(self.ouverts)`. Après un `pop`, la
longueur baisse et le nœud suivant **réutilise** un numéro déjà pris — deux nœuds
à égalité de score sont alors départagés par leur empreinte, pas par l'ordre
d'ouverture, et le BFS voit une frontière qui ne suit plus la file.

Le correctif : un compteur monotone `_seq`, et un nœud re-poussé **après un pop**
reprend un numéro neuf. Ces tests échouent sur l'ancien code (2/3) et passent sur
le nouveau : c'est le contrôle négatif.
"""
import pathlib
import sys
import unittest

RACINE = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RACINE))
from tools.pensee.store import Store  # noqa: E402


class TestFileFIFO(unittest.TestCase):
    def test_pas_de_collision_apres_pop(self):
        s = Store()
        s.push("z", 1.0)  # 0
        s.push("b", 1.0)  # 1
        self.assertEqual([f for _, _, f in s.frontier()], ["z", "b"])
        self.assertEqual(s.pop(), "z")
        s.push("a", 1.0)  # 2 ; l'ancien code donnait 1, en collision avec b
        self.assertEqual([f for _, _, f in s.frontier()], ["b", "a"])

    def test_repush_
… [490 caractères tronqués]
  ```

- **bash** `{"command": "ls tools/ | grep -Ei \"resti|tradu|gener|surface|sortie|decode|realis|texte\" | head -40", "description": "Find restitution/translation modules"}`

  ```
carte-sortie-profondeur.sh
corpus_wikipedia_texte.py
generer_natif.py
generer_par_langue.py
loi-fenetre-textes.sh
pont_generatif.py
porte-adaptateur-sortie.sh
porte-n3-generation.sh
restitution_udhr.py
style_traducteur.py
traduire_bench.py
  ```

- **bash** `{"command": "grep -rln \"restitution\\|traduction\\|traduire\" --include=*.py tools/ | head -30", "description": "Locate restitution and translation code"}`

  ```
tools/convertir_clusters.py
tools/analyse_union_experts.py
tools/extrait_udhr.py
tools/extrait_wikipedia.py
tools/extrait_article1.py
tools/premiere_couche_semantique.py
tools/pensee_silencieuse.py
tools/adaptateur_langue.py
tools/retrieval_parallele.py
tools/cribler_corpus.py
tools/importer_udhr.py
tools/udhr_commun.py
tools/sonder_udhr.py
tools/retrieval_udhr.py
tools/restitution_udhr.py
tools/style_traducteur.py
tools/miroir_boucle.py
tools/traduire_bench.py
tools/test_contamination.py
tools/corpus_eurlex.py
tools/aligneur_litteraire.py
tools/seuil_bruit.py
tools/analyse_litteraire.py
tools/carte_langues.py
tools/test_contamination_udhr.py
tools/corpus_jw.py
tools/pensee_multilingue.py
tools/composition_multilingue.py
tools/pidgin_fewshot.py
tools/lora_pidgin_mono.py
  ```

- **bash** `{"command": "for f in tools/restitution_udhr.py tools/traduire_bench.py tools/generer_natif.py tools/pont_generatif.py; do echo \"===== $f\"; sed -n '1,45p' \"$f\"; done", "description": "Read headers of generation and translation tools"}`

  ```
===== tools/restitution_udhr.py
#!/usr/bin/env python3
"""restitution_udhr.py (v2) — LA RESTITUTION, MESURÉE EN FLUX (avec du contexte).

CE QUE LA v1 FAISAIT DE MAL ✗✗, et c'est un piège que je me suis tendu moi-même : elle encodait chaque article
**isolé** ✓✗. Ses premiers octets n'ont alors **aucun contexte** ✓✗ — ils sont imprévisibles par construction ✓✓ —
et un article ne peut **jamais** être exact, même parfaitement mémorisé ✗✗. Le « 0 article exact sur 13 222 » de la
première version était donc **un artefact de mon propre outil** ✓✗, pas un fait du modèle ✓✓.

CE QUE LA v2 FAIT ✓ : elle évalue le texte **en flux** ✓✓ — on donne au modèle les 256 octets qui précèdent le
fragment ✓, et on ne mesure que le fragment ✓. C'est la condition dans laquelle le modèle a été entraîné ✓ (le
corpus est un flux continu ✓), et la seule où la restitution exacte **peut** exister ✓✓.

TROIS CHIFFRES ✗ :
  · **bits/octet** (vue / jamais vue ✓) ;
  · **exactitude par octet** (vue / jamais vue ✓) ;
  · **fragments exacts** ✓✓ : la fraction des **fenêtres de 32 octets** où **tous** les octets sont justes ✓ —
    c'est la « restitution parfaite » à une granularité où elle est possible ✓✓.

⚠️ CE Q
… [7650 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Writing the new product CLI `tools/drave.py`

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "content": "#!/usr/bin/env python3\n\"\"\"drave.py — le point d'entrée produit du bloc linguistique.\n\nUne seule commande, trois gestes, hors ligne et déterministe :\n\n    python3 tools/drave.py analyser \"Le chat dort … [16688 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "python3 tools/drave.py --version; echo \"code=$?\"; echo ===; python3 tools/drave.py --aide | head -30; echo \"code=${PIPESTATUS[0]}\"", "description": "Test version and help"}`

  ```
drave 0.1.0
code=0
===
usage: drave [-h] [-V] {analyser,evaluer,rejouer} ...

Point d'entrée produit du bloc linguistique (analyse heuristique).

positional arguments:
  {analyser,evaluer,rejouer}
    analyser            étiqueter un texte (POS, syntagmes, pragmatique)
    evaluer             mesurer l'heuristique sur le gold
    rejouer             analyser deux fois et vérifier le déterminisme

options:
  -h, --help, --aide    afficher cette aide et quitter
  -V, --version         show program's version number and exit

Codes de sortie : 0 succès · 2 usage · 1 erreur (ou refus d'analyse).
Limites : heuristique CPU, hors ligne, déterministe ; ni neuronal, ni restitution, ni traduction.
Exemples :
  python3 tools/drave.py analyser "Le chat dort."
  python3 tools/drave.py evaluer --gold --json
code=0
  ```

- **bash** `{"command": "python3 tools/drave.py analyser \"Le chat dort.\"; echo \"code=$?\"; echo ===; python3 tools/drave.py analyser \"The cat sleeps on the roof.\" --langue en; echo \"code=$?\"", "description": "Test readable analysis in French and English"}`

  ```
drave 0.1.0 — analyse heuristique (CPU, hors ligne)
langue=fr script=Latn source=heuristique · 19 étiquettes · unités sémantiques=2 (61.5% du texte)
POS  Le/DET chat/NOUN dort/VERB
SYNTAGMES
  GN   [0:7]   Le chat  rôle=agent     → dort
  GV   [8:12]  dort     rôle=predicat  → chat
PRAGMATIQUE
  phrase [0:13] déclarative · acte=assertion · négation=non · modalité=non · double_sens=non
COUVERTURE (confiance max par niveau)  graphème=0.99 · mot=0.98 · pos=0.92 · syntagme=0.55 · phrase=0.85 · discours=0.50 · pragmatique=0.45 · document=0.70
code=0
===
drave 0.1.0 — analyse heuristique (CPU, hors ligne)
langue=en script=Latn source=heuristique · 32 étiquettes · unités sémantiques=3 (48.1% du texte)
POS  The/DET cat/NOUN sleeps/VERB on/PREP the/DET roof/NOUN
SYNTAGMES
  GN   [0:7]    The cat      rôle=groupe nominal  → sleeps
  GV   [8:14]   sleeps       rôle=prédicat        → —
  GP   [15:26]  on the roof  rôle=lieu            → sleeps
PRAGMATIQUE
  phrase [0:27] déclarative · acte=assertion · négation=non · modalité=non · double_sens=non
COUVERTURE (confiance max par niveau)  graphème=0.99 · mot=0.98 · pos=0.92 · syntagme=0.35 · phrase=0.85 · discours=0.50 · pragmatique=0.45 · documen
… [13 caractères tronqués]
  ```

- **bash** `{"command": "/usr/bin/time -f \"duree=%e s maxrss=%M Ko\" python3 tools/drave.py evaluer; echo \"code=$?\"", "description": "Measure readable gold evaluation"}`

  ```
code=1
[stderr]
drave: erreur : KeyError : 'négation'
Command exited with non-zero status 1
duree=0.50 s maxrss=30732 Ko
  ```

- **bash** `{"command": "python3 tools/drave.py analyser \"Le chat de la voisine qui dort sur le toit se réveille.\" --langue fr --json > /tmp/drave_fr.json; echo \"code=$?\"; wc -c /tmp/drave_fr.json; python3 -c \"import json; d=json.load(open('/tmp/drave_fr.json')); print('cles', sorted(d)); print('etiquettes … [218 caractères tronqués]`

  ```
code=0
16100 /tmp/drave_fr.json
cles ['contexte', 'cout', 'etiquettes', 'fraction_semantique', 'langue', 'refus', 'script', 'source', 'texte', 'trace', 'unites_semantiques']
etiquettes 59 False
===
rejeu identique : oui
  texte      : 'Le chat de la voisine qui dort sur le toit se réveille.'
  langue     : fr
  étiquettes : 59
  JSON       : 11700 octets · sha256 b0a1709a97abe8d4…
code=0
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "old_string": "        f\"PRAGMATIQUE acte {_pct(prag['acte'])} · négation {_pct(prag['négation'])} \"\n        f\"· modalité {_pct(prag['modalité'])} · double sens {_pct(prag['double_sens'])}\",", "new_string": "        … [175 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "old_string": "        kwargs[\"add_help\"] = False\n        super().__init__(*args, **kwargs)\n        self.add_argument(\"-h\", \"--help\", \"--aide\", action=\"help\",\n                          help=\"afficher cette  … [355 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "new_string": "    parseur.add_argument(\"-V\", \"--version\", action=\"version\", version=f\"{NOM} {VERSION}\",\n                         help=\"afficher la version et quitter\")", "old_string": "    parseur.add_argumen … [76 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **bash** `{"command": "/usr/bin/time -f \"duree=%e s maxrss=%M Ko\" python3 tools/drave.py evaluer; echo \"code=$?\"; echo ===GOLD===; /usr/bin/time -f \"duree=%e s maxrss=%M Ko\" python3 tools/drave.py evaluer --gold; echo \"code=$?\"", "description": "Test gold evaluations and measure runtime"}`

  ```
drave 0.1.0 — évaluation de l'heuristique sur le gold
gold vivant (hand + reel + synthétique) · 612 phrases · 3179 tokens · 239 cibles d'attachement

POS         exactitude 75.81 %  (fermé 90.04 %, ouvert 62.34 %)
SYNTAGMES   F1 58.49 %  (P 62.92 % / R 54.64 %)
  tête      F1 73.36 %  (P 81.00 % / R 67.04 %)
ATTACHEMENT exact 92.89 % · couverture 92.89 % · exact sur span 100.00 % · top-k 92.47 %
  tête      couverture 100.00 % · top-k 99.55 %
PRAGMATIQUE acte 99.67 % · négation 97.71 % · modalité 98.86 % · double sens 94.44 %
FRACTION SÉMANTIQUE 55.37 %
CONTRÔLE NÉGATIF cible exacte tirée au hasard 1.67 % (graine 0, 239 cibles)
code=0
===GOLD===
drave 0.1.0 — évaluation de l'heuristique sur le gold
gold gelé (référence figée) · 602 phrases · 3141 tokens · 239 cibles d'attachement

POS         exactitude 76.03 %  (fermé 90.07 %, ouvert 62.69 %)
SYNTAGMES   F1 58.93 %  (P 63.19 % / R 55.22 %)
  tête      F1 73.92 %  (P 81.36 % / R 67.72 %)
ATTACHEMENT exact 92.89 % · couverture 92.89 % · exact sur span 100.00 % · top-k 92.47 %
  tête      couverture 100.00 % · top-k 99.55 %
PRAGMATIQUE acte 99.67 % · négation 97.67 % · modalité 98.84 % · double sens 94.35 %
FRACTION SÉMANTIQUE 55.54 
… [151 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/drave.py --aide | head -18; echo ===; python3 tools/drave.py 2>&1; echo \"code=$?\"; echo ===; python3 tools/drave.py analyser \"Le chat dort.\" --langue de 2>&1; echo \"code=$?\"; echo ===; python3 tools/drave.py analyser \"\" 2>&1; echo \"code=$?\"", "description": "Test … [33 caractères tronqués]`

  ```
usage: drave [-h] [-V] {analyser,evaluer,rejouer} ...

Point d'entrée produit du bloc linguistique (analyse heuristique).

arguments:
  {analyser,evaluer,rejouer}
    analyser            étiqueter un texte (POS, syntagmes, pragmatique)
    evaluer             mesurer l'heuristique sur le gold
    rejouer             analyser deux fois et vérifier le déterminisme

options:
  -h, --help, --aide    afficher cette aide et quitter
  -V, --version         afficher la version et quitter

Codes de sortie : 0 succès · 2 usage · 1 erreur (ou refus d'analyse).
Limites : heuristique CPU, hors ligne, déterministe ; ni neuronal, ni restitution, ni traduction.
Exemples :
  python3 tools/drave.py analyser "Le chat dort."
===
usage: drave [-h] [-V] {analyser,evaluer,rejouer} ...
drave: erreur d'usage : the following arguments are required: {analyser,evaluer,rejouer}
code=2
===
usage: drave analyser [-h] [--langue {fr,en}] [--json] TEXTE
drave analyser: erreur d'usage : argument --langue: invalid choice: 'de' (choose from 'fr', 'en')
code=2
===
drave: refus d'analyse : vide (le texte doit contenir au moins une lettre ou un chiffre)
code=1
  ```

- **bash** `{"command": "python3 tools/drave.py evaluer --json > /tmp/drave_eval.json; echo \"code=$?\"; wc -c /tmp/drave_eval.json; python3 -c \"import json; d=json.load(open('/tmp/drave_eval.json')); print(sorted(d)); print(d['gold']); print(d['heuristique']['syntagme']['f1']); print(d['controle_negatif'])\"; … [176 caractères tronqués]`

  ```
code=0
2748 /tmp/drave_eval.json
['controle_negatif', 'gold', 'heuristique', 'version']
{'nom': 'vivant (hand + reel + synthétique)', 'gele': False, 'phrases': 612, 'tokens': 3179, 'cibles_attachement': 239}
0.5849
{'nom': 'cible exacte tirée au hasard dans le gold', 'graine': 0, 'cibles': 239, 'exact_taux': 0.0167}
===
2740 /tmp/drave_eval_gele.json
  ```

- **bash** `{"command": "for i in 1 2 3; do python3 tools/drave.py analyser \"Le chat de la voisine qui dort sur le toit se réveille.\" --langue fr --json > /tmp/drave_json_$i.json; done; md5sum /tmp/drave_json_*.json; echo ===; for i in 1 2 3; do python3 tools/drave.py evaluer --json > /tmp/drave_eval_$i.json; … [263 caractères tronqués]`

  ```
b23f2019ee1fa0e50686534b8531cacc  /tmp/drave_json_1.json
b23f2019ee1fa0e50686534b8531cacc  /tmp/drave_json_2.json
b23f2019ee1fa0e50686534b8531cacc  /tmp/drave_json_3.json
===
7bb1d8f4b03635030a0fb73107d392dd  /tmp/drave_eval_1.json
7bb1d8f4b03635030a0fb73107d392dd  /tmp/drave_eval_2.json
7bb1d8f4b03635030a0fb73107d392dd  /tmp/drave_eval_3.json
2c13989e5a13deb30d97b3fa546970e2  /tmp/drave_eval_gele.json
===
c849ffc565cb862c5c275feeb2aac36f  /tmp/drave_txt_1.txt
c849ffc565cb862c5c275feeb2aac36f  /tmp/drave_txt_2.txt
  ```

### 🤖 Assistant

⏵ Writing the end-to-end smoke test `tools/tests/test_produit.py`

- **write** `{"content": "\"\"\"test_produit.py — le smoke test de bout en bout du point d'entrée `tools/drave.py`.\n\nHuit assertions, deux phrases (fr/en), le déterminisme et les codes de sortie. Le test passe\naussi bien par `python3 tools/tests/test_produit.py` que par `pytest` : il n'importe rien du\ndépôt  … [4073 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_produit.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "/usr/bin/time -f \"duree=%e s maxrss=%M Ko\" python3 tools/tests/test_produit.py; echo \"code=$?\"", "description": "Run the smoke test directly"}`

  ```
code=0
[stderr]
test_analyser_anglais (__main__.TestProduit.test_analyser_anglais) ... ok
test_analyser_francais (__main__.TestProduit.test_analyser_francais) ... ok
test_codes_usage (__main__.TestProduit.test_codes_usage) ... ok
test_json_valide_et_deterministe (__main__.TestProduit.test_json_valide_et_deterministe) ... ok
test_rejouer_deterministe (__main__.TestProduit.test_rejouer_deterministe) ... ok
test_version_et_aide (__main__.TestProduit.test_version_et_aide) ... ok

----------------------------------------------------------------------
Ran 6 tests in 1.224s

OK
duree=1.32 s maxrss=28476 Ko
  ```

- **bash** `{"command": "/usr/bin/time -f \"duree=%e s\" python3 -m pytest tools/tests/test_produit.py -q; echo \"code=$?\"", "description": "Run the smoke test with pytest"}`

  ```
......                                                                   [100%]
6 passed in 1.29s
code=0
[stderr]
duree=2.03 s
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "new_string": "def _envelopper(prefixe: str, contenu: str, largeur: int = LARGEUR) -> list[str]:\n    \"\"\"Coupe une ligne trop longue en gardant l'alignement sous le préfixe.\"\"\"\n    lignes = textwrap.wrap(contenu,  … [947 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "new_string": "            lignes.append(\n                f\"  phrase [{p.debut}:{p.fin}] {p.valeur} · acte={acte} \"\n                f\"· négation={negation} · modalité={modalite} · double sens={double_sens}\"\n       … [239 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "new_string": "    couverture = a.couverture()\n    if couverture:\n        ordre = [n for n in bl.NIVEAUX if n in couverture]\n        ordre += sorted(n for n in couverture if n not in bl.NIVEAUX)\n        lignes.extend … [609 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport re, pathlib\np = pathlib.Path('tools/drave.py')\ns = p.read_text()\ns = s.replace('formatter_class=argparse.RawDescriptionHelpFormatter,', 'formatter_class=_Formateur,')\ns = s.replace('help=\"indice de langue ; sans lui, le bloc détecte (fr/en)\"',\n            … [282 caractères tronqués]`

  ```
5 2
323:        formatter_class=_Formateur,
335:        formatter_class=_Formateur,
339:                          help="indice de langue (fr/en) ; sans lui, le bloc détecte")
350:        formatter_class=_Formateur,
364:        formatter_class=_Formateur,
368:                         help="indice de langue (fr/en) ; sans lui, le bloc détecte")
  ```

- **bash** `{"command": "python3 -m py_compile tools/drave.py tools/tests/test_produit.py && echo \"compile ok\"; awk 'length($0)>100 {print FILENAME\":\"FNR\": \"length($0)}' tools/drave.py tools/tests/test_produit.py", "description": "Compile and check line lengths"}`

  ```
compile ok
tools/drave.py:378: 101
  ```

- **bash** `{"command": "python3 tools/drave.py --aide; echo \"code=$?\"; echo =====; python3 tools/drave.py analyser --aide; echo \"code=$?\"", "description": "Check deterministic help rendering"}`

  ```
usage: drave [-h] [-V] {analyser,evaluer,rejouer} ...

Point d'entrée produit du bloc linguistique (analyse heuristique).

arguments:
  {analyser,evaluer,rejouer}
    analyser            étiqueter un texte (POS, syntagmes, pragmatique)
    evaluer             mesurer l'heuristique sur le gold
    rejouer             analyser deux fois et vérifier le déterminisme

options:
  -h, --help, --aide    afficher cette aide et quitter
  -V, --version         afficher la version et quitter

Codes de sortie : 0 succès · 2 usage · 1 erreur (ou refus d'analyse).
Limites : heuristique CPU, hors ligne, déterministe ; ni neuronal, ni restitution, ni traduction.
Exemples :
  python3 tools/drave.py analyser "Le chat dort."
  python3 tools/drave.py evaluer --gold --json
code=0
=====
usage: drave analyser [-h] [--langue {fr,en}] [--json] TEXTE

Analyse un texte avec l'heuristique et rend la lecture compacte ou le JSON.

arguments:
  TEXTE               texte à analyser (entre guillemets)

options:
  -h, --help, --aide  afficher cette aide et quitter
  --langue {fr,en}    indice de langue (fr/en) ; sans lui, le bloc détecte
  --json              sortie JSON complète (annotation, sans durée)

Exemple : 
… [61 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "limit": 20, "offset": 370}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py</path>
<type>file</type>
<content>
370:     return parseur
371: 
372: 
373: def main(argv: list[str] | None = None) -> int:
374:     args = construire_parseur().parse_args(argv)
375:     try:
376:         return args.fonction(args)
377:     except BrokenPipeError:
378:         # `drave analyser ... | head` : la sortie est fermée par le lecteur, ce n'est pas une erreur.
379:         return 0
380:     except KeyboardInterrupt:
381:         print(f"{NOM}: interrompu", file=sys.stderr)
382:         return 1
383:     except Exception as exc:  # noqa: BLE001 — le point d'entrée rend un code, pas une trace
384:         print(f"{NOM}: erreur : {type(exc).__name__} : {exc}", file=sys.stderr)
385:         return 1
386: 
387: 
388: if __name__ == "__main__":
389:     raise SystemExit(main())

(End of file - total 389 lines)
</content>
  ```

- **bash** `{"command": "set -o pipefail; python3 tools/drave.py analyser \"Le chat de la voisine qui dort sur le toit se réveille.\" --json | head -1; echo \"pipe codes=${PIPESTATUS[*]}\"", "description": "Test broken pipe behavior"}`

  ```
{
pipe codes=0 0
  ```

- **bash** `{"command": "grep -n \"\\bre\\.\\|import re\" tools/drave.py; echo ---; grep -n \"^import\\|^from\" tools/drave.py", "description": "Check unused import"}`

  ```
29:import re
---
21:from __future__ import annotations
23:import argparse
24:import hashlib
25:import importlib.util
26:import json
27:import pathlib
28:import random
29:import re
30:import sys
31:import textwrap
41:import bloc_linguistique as bl  # noqa: E402  (import après l'installation des chemins)
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "new_string": "import pathlib\nimport random\nimport sys", "old_string": "import pathlib\nimport random\nimport re\nimport sys"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "new_string": "        # `drave analyser ... | head` : le lecteur a fermé la sortie, ce n'est pas une erreur.", "old_string": "        # `drave analyser ... | head` : la sortie est fermée par le lecteur, ce n'est pas une … [10 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
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

- **bash** `{"command": "sed -n '1,40p' tools/structures/generateur.py; echo ---; grep -n \"import torch\\|import numpy\\|urllib\\|requests\" tools/structures/generateur.py tools/bloc_linguistique.py", "description": "Check dependencies of the S generator"}`

  ```
#!/usr/bin/env python3
"""generateur.py — une phrase brute → des structures candidates (v0 heuristique).

Ce n'est pas un analyseur syntaxique : c'est un **générateur de candidats** à faire valider par
un humain. Il segmente (GN, GV, GP, REL, SUB), devine des rôles par la préposition, puis produit
plusieurs candidats en variant l'**attachement** de chaque segment ambigu (GN le plus proche ou
GV le plus proche).

    python3 generateur.py "Le chat de la voisine qui dort sur le toit se réveille."
    python3 generateur.py --json "..."     # la structure complète
"""
from __future__ import annotations

import json
import re
import unicodedata

DET = set("le la les l un une ce cet cette ces mon ma mes ton ta tes son sa ses "
          "notre nos votre vos leur leurs quel quelle quels quelles".split())
PREP = set("a au aux de du des d en dans par pour sur sous avec sans chez vers entre depuis "
           "pendant durant contre malgre selon pres loin devant derriere apres avant".split())
RELATIFS = set("qui que qu dont ou quoi".split())
CONJ = set("et ou mais donc or ni car quand comme si parce puisque lorsque pendant quoique".split())
COORD = set("et ou mais donc or ni car".split())
SU
… [1872 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp && python3 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py analyser \"Le chat dort.\" | head -8; echo \"code=${PIPESTATUS[0]}\"", "description": "Run CLI from outside the repo"}`

  ```
drave 0.1.0 — analyse heuristique (CPU, hors ligne)
langue=fr script=Latn source=heuristique · 19 étiquettes · unités sémantiques=2 (61.5% du texte)
POS  Le/DET chat/NOUN dort/VERB
SYNTAGMES
  GN   [0:7]   Le chat  rôle=agent     → dort
  GV   [8:12]  dort     rôle=predicat  → chat
PRAGMATIQUE
  phrase [0:13] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
code=0
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json, statistics, subprocess, sys, time\nCLI = [sys.executable, \"tools/drave.py\"]\ncas = [\n    (\"version\", [\"--version\"]),\n    (\"aide\", [\"--aide\"]),\n    (\"analyser fr court\", [\"analyser\", \"Le chat dort.\"]),\n    (\"analyser fr long\", [\"analy … [1102 caractères tronqués]`

  ```
commande                      median s    min s    max s   octets code
version                          0.128    0.125    0.139       12    0
aide                             0.127    0.126    0.129      770    0
analyser fr court                0.131    0.124    0.137      585    0
analyser fr long                 0.131    0.127    0.136     1005    0
analyser en                      0.130    0.129    0.133      699    0
analyser fr long --json          0.133    0.126    0.138    16100    0
rejouer fr long                  0.133    0.129    0.135      191    0
evaluer                          0.492    0.477    0.516      659    0
evaluer --gold --json            0.489    0.489    0.502     2740    0
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport importlib.util, json, sys, time\nsys.path.insert(0, 'tools')\nimport bloc_linguistique as bl\nspec = importlib.util.spec_from_file_location(\"eg\", \"tools/tests/linguistique/evaluer_gold.py\")\neg = importlib.util.module_from_spec(spec); spec.loader.exec_module … [869 caractères tronqués]`

  ```
gold vivant: 612 phrases
analyses: 0.537 s (0.88 ms/phrase)
JSON annotation totale (indent=1): 4938465 octets = 4.938 Mo
JSON annotation totale (compact): 3574776 octets = 3.575 Mo
moyenne par phrase (indent=1): 8069 octets
  ```

- **bash** `{"command": "/usr/bin/time -f \"test direct: %e s, %M Ko\" python3 tools/tests/test_produit.py >/tmp/test_direct.out 2>/tmp/test_direct.err; code=$?; tail -3 /tmp/test_direct.err; echo \"code=$code\"; /usr/bin/time -f \"pytest: %e s\" python3 -m pytest tools/tests/test_produit.py -q >/tmp/test_pytes … [160 caractères tronqués]`

  ```
OK
test direct: 1.33 s, 28532 Ko
code=0
......                                                                   [100%]
6 passed in 1.28s
pytest: 1.93 s
code=0
  ```

- **bash** `{"command": "python3 tools/drave.py analyser \"Le chat dort.\" --json > /tmp/json_court.json; python3 tools/drave.py analyser \"The cat sleeps on the roof.\" --langue en --json > /tmp/json_en.json; wc -c /tmp/json_court.json /tmp/json_en.json; python3 - <<'PY'\nimport json\nfor f in [\"/tmp/json_cou … [426 caractères tronqués]`

  ```
5561 /tmp/json_court.json
 8704 /tmp/json_en.json
14265 total
/tmp/json_court.json langue fr etiquettes 19 compact 4013
/tmp/json_en.json langue en etiquettes 32 compact 6278
===
rejeu identique : oui
  texte      : 'Le chat dort.'
  langue     : fr
  étiquettes : 19
  JSON       : 4013 octets · sha256 6b6def477a493444…
3f30031fe91a9c27d580cddafbe67112  -
  ```

- **bash** `{"command": "git status --porcelain tools/drave.py tools/tests/test_produit.py; echo ---; git status --porcelain | grep '^??' | head -20; echo ---; git diff --stat | tail -5", "description": "Verify only the two new files are added"}`

  ```
A  tools/drave.py
A  tools/tests/test_produit.py
---
?? journal/2026-11-05/attention.md
?? journal/2026-11-06/distribue.md
?? journal/2026-11-06/docs.md
?? journal/2026-11-06/mesures.md
?? journal/2026-11-06/modele.md
?? journal/2026-11-06/portes.md
?? journal/sessions/14114f3d-ae0d-416e-ad8e-4d4eaa04c36c/
?? journal/sessions/1555bdd3-27e9-4779-b1e7-716e32399c11/
?? journal/sessions/1b0cf09a-a77a-443d-82e2-68a5d6cacdf0/
?? journal/sessions/24001907-4f19-4ea5-87f6-98334496719f/
?? journal/sessions/24529ced-6556-4491-9633-9401c2dffb0c/
?? journal/sessions/2cc1ad4a-373e-4362-a341-3c4a630c2e0c/
?? journal/sessions/3144cf23-6004-46ef-bc3d-f05d81c0cff6/
?? journal/sessions/3f8f2bb8-781b-44a6-9e14-58025004b6fc/
?? journal/sessions/3fb87dc7-7d24-42e2-a68e-e37e2734b755/
?? journal/sessions/53bc3288-f2c1-4a7d-b1db-88d794074f70/
?? journal/sessions/63d4c619-63e8-41b9-a183-5c6f1ac05a21/
?? journal/sessions/65495a29-10c0-4571-96be-e7729f1efebf/
?? journal/sessions/7263ca42-cd56-4c36-a6dd-8ff2d1024a43/
?? journal/sessions/a0d33fb7-37a9-4834-8a94-0da119e3b18f/
---
 reports/rapport-coherence-fiches-v7.md             |    17 +-
 reports/rapport-dev-test-v10.md                    |     2 +-
 reports
… [171 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json, subprocess, sys\nCLI=[sys.executable,\"tools/drave.py\"]\n# aide déterministe : largeur fixe, même sortie en pipe et avec COLUMNS variable\na=subprocess.run(CLI+[\"--aide\"], capture_output=True, text=True).stdout\nfor col in (\"40\",\"200\"):\n    import  … [540 caractères tronqués]`

  ```
COLUMNS 40 identique: True
COLUMNS 200 identique: True
['--version'] -> 0 | drave 0.1.0
['analyser', 'Le chat dort.'] -> 0 | drave 0.1.0 — analyse heuristique (CPU, hors ligne)
['evaluer', '--gold'] -> 0 | drave 0.1.0 — évaluation de l'heuristique sur le gold
['rejouer', 'Le chat dort.'] -> 0 | rejeu identique : oui
  ```

